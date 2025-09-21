
import pathlib
from base_app.services.action_registry import ActionRegistry
from base_app.services.interaction_recorder import InteractionRecorder

def test_semantic_recorder_records(tmp_path):
    rec = InteractionRecorder(tmp_path)
    ar = ActionRegistry()
    ar.attach_recorder(rec.observer)
    # register and record
    called = {"v": False}
    def handler(_ctx, _args): called["v"] = True
    ar.register({"id":"demo.action","text":"Demo","handler":handler})
    rec.start()
    ar.invoke("demo.action", {"a":1})
    rec.stop()
    rec_dir = tmp_path/"recordings"
    assert rec_dir.exists()
    files = list(rec_dir.glob("trace_*.jsonl"))
    assert files, "no trace file"
    assert called["v"] is True
