from base_app.core.feedback_service import FeedbackService
from pathlib import Path

def test_crash_marker_and_bundle(tmp_path, monkeypatch):
    # ensure default dirs map to tmp
    monkeypatch.chdir(tmp_path)
    svc = FeedbackService(results_dir=Path('_results'))
    m = svc.set_crash_marker('test-crash')
    assert m.exists()
    z = svc.bundle('bundle')
    assert z.exists() and z.suffix == '.zip'
    svc.clear_crash_marker()
    assert not m.exists()
