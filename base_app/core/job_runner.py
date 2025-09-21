
from __future__ import annotations
import threading, subprocess, uuid, datetime, json, traceback, time
from pathlib import Path

DEFAULT_LOG_DIR = Path("tmp") / "logs"
DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)

def _json_log(path: Path, record: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False); f.write("\n")

class JobHandle:
    def __init__(self, job_id: str, kind: str):
        self.id = job_id
        self.kind = kind
        self._done = threading.Event()
        self._cancel = threading.Event()
        self.result = None
        self.error = None
        self._proc = None

    def wait(self, timeout: float | None = None):
        self._done.wait(timeout)
        return self.done

    @property
    def done(self) -> bool:
        return self._done.is_set()

    def cancel(self):
        self._cancel.set()

    @property
    def cancelled(self) -> bool:
        return self._cancel.is_set()

class JobRunner:
    def __init__(self, log_dir: Path | None = None):
        self.log_dir = Path(log_dir) if log_dir else DEFAULT_LOG_DIR
        self.log_file = self.log_dir / "jobs.jsonl"

    def _log(self, **kw):
        rec = {"ts": datetime.datetime.now(datetime.UTC).isoformat(), **kw}
        _json_log(self.log_file, rec)

    # Required by tests
    def submit_thread(self, fn, *args, **kwargs) -> JobHandle:
        job_id = str(uuid.uuid4())
        h = JobHandle(job_id, "thread")
        def runner():
            self._log(event="start", job_id=job_id, kind="thread")
            try:
                h.result = fn(*args, **kwargs)
                self._log(event="finish", job_id=job_id, ok=True)
            except Exception as e:
                h.error = {"type": type(e).__name__, "msg": str(e), "trace": traceback.format_exc()}
                self._log(event="finish", job_id=job_id, ok=False, error=h.error)
            finally:
                h._done.set()
        threading.Thread(target=runner, daemon=True).start()
        return h

    # Required by tests
    def submit_thread_cancellable(self, fn, *args, **kwargs) -> JobHandle:
        job_id = str(uuid.uuid4())
        h = JobHandle(job_id, "thread")
        def runner():
            self._log(event="start", job_id=job_id, kind="thread")
            try:
                h.result = fn(h, *args, **kwargs)  # target should check h.cancelled
                self._log(event="finish", job_id=job_id, ok=(not h.cancelled), cancelled=h.cancelled)
            except Exception as e:
                h.error = {"type": type(e).__name__, "msg": str(e), "trace": traceback.format_exc()}
                self._log(event="finish", job_id=job_id, ok=False, error=h.error)
            finally:
                h._done.set()
        threading.Thread(target=runner, daemon=True).start()
        return h

    def submit_process_cancellable(self, cmd, cwd=None, env=None) -> JobHandle:
        job_id = str(uuid.uuid4())
        h = JobHandle(job_id, "process")
        def runner():
            self._log(event="start", job_id=job_id, kind="process", cmd=cmd)
            try:
                # Avoid stdout pipe blocking on Windows; just poll.
                p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=None, stderr=None)
                h._proc = p
                while True:
                    rc = p.poll()
                    if h.cancelled and rc is None:
                        try:
                            p.terminate()
                        except Exception:
                            pass
                        t0 = time.time()
                        while p.poll() is None and (time.time() - t0) < 1.0:
                            time.sleep(0.05)
                        if p.poll() is None:
                            try:
                                p.kill()
                            except Exception:
                                pass
                        rc = p.poll()
                        h.result = {"rc": rc if rc is not None else -1}
                        self._log(event="finish", job_id=job_id, ok=False, rc=h.result["rc"], cancelled=True)
                        return
                    if rc is not None:
                        h.result = {"rc": rc}
                        self._log(event="finish", job_id=job_id, ok=(rc==0), rc=rc, cancelled=False)
                        if rc != 0:
                            h.error = {"type":"ProcessError","msg":f"rc={rc}"}
                        return
                    time.sleep(0.02)
            except Exception as e:
                h.error = {"type": type(e).__name__, "msg": str(e), "trace": traceback.format_exc()}
                self._log(event="finish", job_id=job_id, ok=False, error=h.error)
            finally:
                h._done.set()
        threading.Thread(target=runner, daemon=True).start()
        return h
