
from __future__ import annotations
from typing import Callable, Optional

from PyQt6.QtWidgets import QStatusBar, QMainWindow, QLabel, QWidget
from PyQt6.QtCore import QTimer

# --------------------------------------------------------------------------------------
# Flexible StatusBarController
# Accepts either:
#   - StatusBarController(window: QMainWindow)
#   - StatusBarController(statusbar: QStatusBar, toggle_fn: Optional[Callable]=None, is_enabled_fn: Optional[Callable]=None)
#   - StatusBarController(*args, **kwargs)  # extra args ignored gracefully
# --------------------------------------------------------------------------------------
class StatusBarController:
    def __init__(self, *args, **kwargs):
        # Determine primary object
        first = args[0] if args else kwargs.get("window") or kwargs.get("statusbar")
        sb: QStatusBar

        if isinstance(first, QMainWindow):
            window = first
            sb = window.statusBar() or QStatusBar(window)
            window.setStatusBar(sb)
        elif isinstance(first, QStatusBar):
            sb = first
        else:
            # If nothing sensible passed, create a detached status bar (still works)
            sb = QStatusBar()

        # Optional callbacks (accept both kwargs and positional for backward compat)
        toggle_fn = kwargs.get("toggle_fn")
        is_enabled_fn = kwargs.get("is_enabled_fn")

        # Allow positional 2/3 args pattern: (statusbar, toggle_fn, is_enabled_fn)
        if toggle_fn is None and len(args) >= 2 and callable(args[1]):
            toggle_fn = args[1]
        if is_enabled_fn is None and len(args) >= 3 and callable(args[2]):
            is_enabled_fn = args[2]

        self._status = sb
        self._toggle_fn: Optional[Callable[[], None]] = toggle_fn
        self._is_enabled_fn: Optional[Callable[[], bool]] = is_enabled_fn

        # Recording indicator (non-intrusive)
        self._rec_label = QLabel("Rec: off")
        self._rec_label.setToolTip("Keystroke recording status")
        try:
            self._status.addPermanentWidget(self._rec_label)
        except Exception:
            pass

        # Periodic refresh of the indicator (safe even without callback)
        self._timer = QTimer()
        self._timer.timeout.connect(self._refresh)
        self._timer.start(1000)  # 1 Hz is plenty
        self._refresh()

    def _refresh(self) -> None:
        enabled = False
        try:
            if callable(self._is_enabled_fn):
                enabled = bool(self._is_enabled_fn())
        except Exception:
            enabled = False
        try:
            self._rec_label.setText("Rec: on" if enabled else "Rec: off")
        except Exception:
            pass

    @property
    def status_bar(self) -> QStatusBar:
        return self._status

    def show_message(self, text: str, timeout_ms: int = 3000) -> None:
        try:
            self._status.showMessage(text, timeout_ms)
        except Exception:
            pass

    def add_permanent(self, widget: QWidget) -> None:
        try:
            self._status.addPermanentWidget(widget)
        except Exception:
            pass


# --------------------------------------------------------------------------------------
# Lightweight monitors (optional; used by smokes and status bar)
# --------------------------------------------------------------------------------------
class SystemMonitor:
    """CPU/MEM monitor using psutil if available; otherwise shows placeholders."""
    def __init__(self, parent_statusbar: QStatusBar, poll_ms: int = 1500):
        self.label = QLabel("CPU: --%  MEM: --%")
        try:
            parent_statusbar.addPermanentWidget(self.label)
        except Exception:
            pass
        # psutil is optional
        try:
            import psutil  # type: ignore
            self._psutil = psutil
        except Exception:
            self._psutil = None

        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(poll_ms)
        self._tick()

    def _tick(self):
        if self._psutil:
            try:
                cpu = int(self._psutil.cpu_percent(interval=None))
                mem = int(self._psutil.virtual_memory().percent)
                self.label.setText(f"CPU: {cpu}%  MEM: {mem}%")
                return
            except Exception:
                pass
        self.label.setText("CPU: --%  MEM: --%")


class JobsCounter:
    def __init__(self, parent_statusbar: QStatusBar, poll_ms: int = 1000):
        self.label = QLabel("Jobs: 0 active / 0 queued")
        try:
            parent_statusbar.addPermanentWidget(self.label)
        except Exception:
            pass
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(poll_ms)
        self._tick()

    def _tick(self):
        try:
            from ..services import job_runner as jr
            a = getattr(jr, "active_count", lambda: 0)()
            q = getattr(jr, "queued_count", lambda: 0)()
            self.label.setText(f"Jobs: {a} active / {q} queued")
        except Exception:
            pass
