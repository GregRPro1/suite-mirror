
import pathlib, subprocess, os

def test_feedback_fileshare(tmp_path):
    root = pathlib.Path(".").resolve()
    proj = tmp_path / "proj"
    proj.mkdir()
    # generate project
    r = subprocess.run([str(root/".venv/Scripts/python.exe"), "-m", "configurator.cli.configure", "--profile", "barsim", "--out", str(proj)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    # submit ticket via CLI
    r = subprocess.run([str(root/".venv/Scripts/python.exe"), "-m", "base_app.services.feedback_service", "--project", str(proj), "--title", "Smoke bug", "--desc", "desc"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    inbox = proj/"inbox"
    zips = list(inbox.glob("ticket_*.zip"))
    assert zips, "no ticket bundle created"
