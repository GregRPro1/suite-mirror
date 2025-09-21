
from __future__ import annotations
import sys, os, json, datetime, traceback
from pathlib import Path

class CrashGuard:
    """
    Installs robust crash/exit handlers.
    - Writes a running session file on start
    - Marks clean exit on aboutToQuit()
    - sys.excepthook -> crash.jsonl + last_crash.json
    - Qt message handler -> qt_messages.jsonl
    - On next launch, if prior session missing clean flag -> marks unclean_exit.json
    """
    def __init__(self, app=None, log_dir: str | Path = "_results\\crash"):
        self.app = app
        self.log_root = Path(log_dir)
        self.log_root.mkdir(parents=True, exist_ok=True)
        self.session_file = self.log_root / "session.json"
        self.crash_jsonl = self.log_root / "crash.jsonl"
        self.qt_jsonl = self.log_root / "qt_messages.jsonl"
        self.last_crash = self.log_root / "last_crash.json"
        self.unclean_exit = self.log_root / "unclean_exit.json"
        self._prev_sys_hook = None

    def _ts(self):
        return datetime.datetime.now(datetime.UTC).isoformat()

    def install(self):
        # Detect previous unclean exit
        try:
            if self.session_file.exists():
                prior = json.loads(self.session_file.read_text(encoding="utf-8"))
                if not prior.get("clean_exit", False):
                    self.unclean_exit.write_text(json.dumps({
                        "ts": self._ts(),
                        "note": "Previous session ended uncleanly (no clean_exit flag)."
                    }, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

        # Write current session start
        self.session_file.write_text(json.dumps({
            "ts": self._ts(), "pid": os.getpid(), "clean_exit": False
        }, ensure_ascii=False, indent=2), encoding="utf-8")

        # Hook Python exceptions
        self._prev_sys_hook = sys.excepthook
        def _hook(exc_type, exc, tb):
            rec = {
                "ts": self._ts(),
                "type": getattr(exc_type, "__name__", str(exc_type)),
                "message": str(exc),
                "trace": "".join(traceback.format_exception(exc_type, exc, tb))
            }
            with open(self.crash_jsonl, "a", encoding="utf-8") as f:
                json.dump(rec, f, ensure_ascii=False); f.write("\n")
            self.last_crash.write_text(json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            try:
                self.session_file.write_text(json.dumps({
                    "ts": self._ts(), "pid": os.getpid(), "clean_exit": False, "error": rec
                }, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception:
                pass
            if self._prev_sys_hook:
                try: self._prev_sys_hook(exc_type, exc, tb)
                except Exception: pass
        sys.excepthook = _hook

        # Qt messages if available
        try:
            from PyQt6 import QtCore
            def qt_handler(msg_type, context, message):
                rec = {"ts": self._ts(), "type": int(msg_type), "message": str(message)}
                with open(self.qt_jsonl, "a", encoding="utf-8") as f:
                    json.dump(rec, f, ensure_ascii=False); f.write("\n")
            QtCore.qInstallMessageHandler(qt_handler)
            if self.app:
                self.app.aboutToQuit.connect(self.mark_clean_exit)  # type: ignore[attr-defined]
        except Exception:
            pass

    def mark_clean_exit(self):
        try:
            self.session_file.write_text(json.dumps({
                "ts": self._ts(), "pid": os.getpid(), "clean_exit": True
            }, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass


def install_crash_handlers(app=None, log_dir: str | Path = "_results\\crash") -> CrashGuard:
    cg = CrashGuard(app=app, log_dir=log_dir)
    cg.install()
    return cg
