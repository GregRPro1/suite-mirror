
import pathlib, subprocess

def test_feedback_panel_submit(tmp_path):
    # Use service directly: submit a bundle into inbox
    from base_app.services.feedback_service import submit_ticket
    proj = tmp_path / "proj"; proj.mkdir()
    # minimal project.yaml
    (proj/"project.yaml").write_text("project:\n  id: x\n  name: x\n  version: 0.0.1\n  profile: test\nfeedback:\n  enabled: true\n  sinks:\n    - kind: fileshare\n      id: local\n      config: { path: './inbox' }\n", encoding="utf-8")
    b = submit_ticket(proj, "Smoke-Feedback", "desc", "bug")
    assert b.exists()
    assert b.parent.name == "inbox"
