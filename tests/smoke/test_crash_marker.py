
import pathlib, subprocess

def test_crash_marker_cli(tmp_path):
    root = pathlib.Path(".").resolve()
    proj = tmp_path / "proj"
    proj.mkdir()
    # simulate crash via CLI
    r = subprocess.run([str(root/".venv/Scripts/python.exe"), "-m", "base_app.services.crash_handler", "--project", str(proj)], capture_output=True, text=True)
    assert r.returncode != 0  # non-zero on simulated crash
    marker = proj/"tmp"/"crash_marker.json"
    assert marker.exists(), f"marker not found: {marker}"
