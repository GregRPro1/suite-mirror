from __future__ import annotations
import threading, time, uuid, pathlib

class JobRunner:
    def __init__(self):
        self._jobs = {}

    def run_dummy(self, artifacts_dir: pathlib.Path) -> str:
        jid = f"J-{uuid.uuid4().hex[:8]}"
        def work():
            time.sleep(0.3)
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            (artifacts_dir / f"{jid}.txt").write_text("dummy artifact")
        threading.Thread(target=work, daemon=True).start()
        self._jobs[jid]= "running"
        return jid