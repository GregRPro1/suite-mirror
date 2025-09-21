

# === Sprint5 additions: System monitor & Jobs counter ===
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel
import importlib

class SystemMonitor:
    """CPU/MEM monitor using psutil if available; otherwise shows placeholders."""
    def __init__(self, parent_statusbar: QStatusBar, poll_ms: int = 1500):
        self.label = QLabel("CPU: --%  MEM: --%")
        self.label.setToolTip("System utilization (psutil optional)")
        parent_statusbar.addPermanentWidget(self.label)
        self._psutil = importlib.util.find_spec("psutil") is not None
        if self._psutil:
            import psutil  # type: ignore
            self._psutil_mod = psutil
        else:
            self._psutil_mod = None
        self._timer = QTimer()
        self._timer.timeout.connect(self._tick)
        self._timer.start(poll_ms)
        self._tick()

    def _tick(self):
        if self._psutil_mod:
            try:
                cpu = int(self._psutil_mod.cpu_percent(interval=None))
                mem = int(self._psutil_mod.virtual_memory().percent)
                self.label.setText(f"CPU: {cpu}%  MEM: {mem}%")
            except Exception:
                self.label.setText("CPU: --%  MEM: --%")

class JobsCounter:
    """Shows active/queued counts pulled from job_runner."""
    def __init__(self, parent_statusbar: QStatusBar, poll_ms: int = 1000):
        self.label = QLabel("Jobs: 0 active / 0 queued")
        self.label.setToolTip("Job activity (active/queued)")
        parent_statusbar.addPermanentWidget(self.label)
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
