
from __future__ import annotations
import sys, os
from pathlib import Path
from PyQt6 import QtWidgets, QtCore
try:
    import yaml  # type: ignore
except Exception:
    yaml = None

from base_app.core.main_window import MainWindow
from base_app.core.docking_manager import DockingManager
from base_app.core.crash_guard import install_crash_handlers

def load_project(project_root: Path) -> dict:
    pj = project_root / "project.yaml"
    if pj.exists() and yaml:
        return yaml.safe_load(pj.read_text(encoding="utf-8"))
    return {}

def apply_theme(win: QtWidgets.QMainWindow, project_root: Path, name: str):
    qss = project_root / "ui" / "qss" / f"{name}.qss"
    if qss.exists():
        QtWidgets.QApplication.instance().setStyleSheet(qss.read_text(encoding="utf-8"))

def run(project_root: str, profile: str, headless: bool = False):
    if headless:
        os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])

    cg = install_crash_handlers(app, "_results\\crash")

    win = MainWindow()
    win.resize(1200, 800)

    if os.environ.get("DEMO_RAISE") == "1":
        QtCore.QTimer.singleShot(50, lambda: 1/0)

    try:
        win.dm.load_layout(project_id=profile)
    except Exception:
        pass

    if not headless:
        win.show()

    ret = 0
    try:
        if headless:
            QtWidgets.QApplication.processEvents()
        else:
            ret = app.exec()
    finally:
        cg.mark_clean_exit()
    return ret

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--project", required=True)
    p.add_argument("--profile", required=True)
    p.add_argument("--headless", action="store_true")
    args = p.parse_args()
    raise SystemExit(run(args.project, args.profile, headless=args.headless))
