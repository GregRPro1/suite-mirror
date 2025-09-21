from pathlib import Path
from base_app.core.feedback_service import FeedbackService, WebhookTransport

def test_webhook_file_transport(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    svc = FeedbackService(results_dir=Path('_results'))
    svc.set_crash_marker('test')
    z = svc.bundle('fb')
    t = WebhookTransport('file://' + str((tmp_path/'_results'/'webhook.json').as_posix()))
    out = t.send(z)
    assert out.exists()
