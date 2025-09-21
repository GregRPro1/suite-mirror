
from __future__ import annotations
import datetime, json, pathlib, os, uuid

class InteractionRecorder:
    def __init__(self, project_dir: pathlib.Path | None=None):
        self.enabled = False
        self.project_dir = pathlib.Path(project_dir) if project_dir else None
        self._events_path: pathlib.Path | None = None

    def set_project_dir(self, p: pathlib.Path):
        self.project_dir = pathlib.Path(p)

    def toggle(self):
        if not self.enabled:
            self.start()
        else:
            self.stop()

    def start(self):
        if self.enabled: return
        self.enabled = True
        base = self._recordings_dir()
        base.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now(datetime.UTC).strftime("%Y%m%dT%H%M%SZ")
        self._events_path = base / f"trace_{ts}_{uuid.uuid4().hex[:6]}.jsonl"
        self._write({"type":"trace.start","ts":self._ts()})

    def stop(self):
        if not self.enabled: return
        self._write({"type":"trace.stop","ts":self._ts()})
        self.enabled = False
        self._events_path = None

    def observer(self, event_type: str, action_id: str, args: dict):
        if not self.enabled: return
        self._write({"type": event_type, "ts": self._ts(), "action_id": action_id, "args": args})

    def _recordings_dir(self) -> pathlib.Path:
        base = self.project_dir if self.project_dir else pathlib.Path(".")
        return base / "recordings"

    def _write(self, obj: dict):
        if not self._events_path: return
        line = json.dumps(obj, separators=(",",":"))
        with open(self._events_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    @staticmethod
    def _ts():
        return datetime.datetime.now(datetime.UTC).isoformat(timespec="milliseconds")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True, help="Project directory containing project.yaml")
    args = ap.parse_args()
    rec = InteractionRecorder(pathlib.Path(args.project))
    rec.start()
    # simple demo event
    rec.observer("action.invoke", "demo.action", {"x":1})
    rec.stop()
    print("Recorded to", rec._recordings_dir())
