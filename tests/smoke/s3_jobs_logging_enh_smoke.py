import sys, time, subprocess
from pathlib import Path
from base_app.core.job_runner import JobRunner

def _busy(handle, t=2.0):
    import time
    start = time.time()
    while time.time()-start < t:
        if handle.cancelled:
            return 'cancelled'
        time.sleep(0.05)
    return 'done'

def test_cancellable_thread():
    jr = JobRunner(log_dir=Path('tmp')/'logs')
    h = jr.submit_thread_cancellable(_busy, 2.0)
    time.sleep(0.1)
    h.cancel()
    h.wait(2.0)
    assert h.done and h.cancelled

def test_cancellable_process():
    jr = JobRunner(log_dir=Path('tmp')/'logs')
    cmd = [sys.executable, '-c', 'import time; time.sleep(5)']
    h = jr.submit_process_cancellable(cmd)
    time.sleep(0.2)
    h.cancel()
    h.wait(3.0)
    assert h.done and h.cancelled
