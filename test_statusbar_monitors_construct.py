
import os
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

def test_statusbar_monitors_construct():
    from PyQt6.QtWidgets import QApplication, QMainWindow, QStatusBar
    from PyQt6.QtCore import QTimer, QEventLoop
    from base_app.core.status_bar import SystemMonitor, JobsCounter
    from base_app.services import job_runner as jr

    app = QApplication.instance() or QApplication([])
    w = QMainWindow()
    sb = QStatusBar(w); w.setStatusBar(sb)
    sysmon = SystemMonitor(sb, poll_ms=50)
    jobs = JobsCounter(sb, poll_ms=50)

    if hasattr(jr, "increment_queue"): jr.increment_queue(2)
    if hasattr(jr, "increment_active"): jr.increment_active(1)

    loop = QEventLoop()
    QTimer.singleShot(150, loop.quit)
    loop.exec()

    assert sysmon.label.text()
    assert "Jobs:" in jobs.label.text()
