from __future__ import annotations
import re, sys, pathlib, datetime

ROOT = pathlib.Path('.').resolve()
TARGET = ROOT / 'main_window.py'
BACKUP_DIR = ROOT / '_packs'

def backup(p: pathlib.Path):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bp = BACKUP_DIR / f'backup_main_window_{ts}.py'
    bp.write_text(p.read_text(encoding='utf-8'), encoding='utf-8')
    return bp

def ensure_imports(src: str) -> str:
    need = []
    if 'from base_app.ui.open_settings import show_settings_dialog' not in src:
        need.append('from base_app.ui.open_settings import show_settings_dialog')
    if 'from PyQt6 import QtGui' not in src:
        need.append('from PyQt6 import QtGui')
    if need:
        src = '\n'.join(need) + '\n' + src
    return src

def insert_block_after_def(src: str, def_rx: str, block: str) -> tuple[str,bool]:
    m = re.search(def_rx, src, re.M)
    if not m:
        return src, False
    end = m.end()
    indent = '        '
    for ln in src[end:].splitlines(True):
        if ln.strip():
            indent = ln[:len(ln) - len(ln.lstrip())]
            break
    block = block.replace('{IND}', indent)
    return src[:end] + block + src[end:], True

def inject(src: str) -> tuple[str,bool]:
    changed = False
    if 'settings.open' not in src or 'Settings…' not in src:
        block = """
{IND}# --- Settings menu wiring (idempotent) ---
{IND}try:
{IND}    _ = self.actSettings
{IND}except Exception:
{IND}    self.actSettings = QtGui.QAction("Settings…", self)
{IND}    self.actSettings.setShortcut("Ctrl+,")
{IND}    self.actSettings.triggered.connect(lambda: show_settings_dialog(self))
{IND}    try:
{IND}        menu = getattr(self, "menuWindow", None)
{IND}        if menu is None and hasattr(self, "menuBar"):
{IND}            mb = self.menuBar() if callable(getattr(self, "menuBar", None)) else None
{IND}            if mb is not None:
{IND}                menu = getattr(self, "menu_tools", None) or getattr(self, "menuWindow", None)
{IND}                if menu is None:
{IND}                    menu = mb.addMenu("&Window")
{IND}        if menu is not None:
{IND}            try: menu.addAction(self.actSettings)
{IND}            except Exception: pass
{IND}    except Exception:
{IND}        pass
{IND}    try:
{IND}        reg = getattr(self, "actions", None)
{IND}        if reg is not None and hasattr(reg, "register_simple"):
{IND}            reg.register_simple("settings.open", "Settings…", lambda: show_settings_dialog(self),
{IND}                                 category="General", shortcut="Ctrl+,")
{IND}    except Exception:
{IND}        pass

"""
        src, ok = insert_block_after_def(src, r'^\s*def\s+__init__\s*\(\s*self[^\)]*\)\s*:\s*', block)
        changed = changed or ok

    block2 = """
{IND}# --- Ensure Settings… appears in menus (idempotent) ---
{IND}try:
{IND}    st = QtGui.QAction("Settings…", self)
{IND}    st.setShortcut("Ctrl+,")
{IND}    st.triggered.connect(lambda: show_settings_dialog(self))
{IND}    added = False
{IND}    for mname in ("menu_tools","menu_view","menu_file","menu_help"):
{IND}        menu = getattr(self, mname, None)
{IND}        if menu is not None:
{IND}            try:
{IND}                texts = [a.text() for a in menu.actions()]
{IND}                if "Settings…" not in texts:
{IND}                    menu.addAction(st)
{IND}                    added = True
{IND}                    break
{IND}            except Exception:
{IND}                pass
{IND}    if not added and hasattr(self, "menuBar"):
{IND}        mb = self.menuBar() if callable(getattr(self, "menuBar", None)) else None
{IND}        if mb is not None:
{IND}            mw = mb.addMenu("&Window")
{IND}            mw.addAction(st)
{IND}except Exception:
{IND}    pass

"""
    src, ok2 = insert_block_after_def(src, r'^\s*def\s+_setup_menus\s*\(\s*self[^\)]*\)\s*:\s*', block2)
    changed = changed or ok2
    return src, changed

def main():
    if not TARGET.exists():
        print('[WARN] main_window.py not found'); return
    txt = TARGET.read_text(encoding='utf-8')
    before = txt
    txt = ensure_imports(txt)
    txt, _ = inject(txt)
    if txt != before:
        backup(TARGET)
        TARGET.write_text(txt, encoding='utf-8')
        print('[OK] Patched main_window.py.')
    else:
        print('[OK] No changes needed.')
if __name__ == '__main__':
    main()
