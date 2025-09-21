import subprocess, sys, pathlib, os

def test_configurator_emits_project(tmp_path):
    root = pathlib.Path(".").resolve()
    out = tmp_path / "proj"
    out.mkdir()
    cmd = [str(root/".venv/Scripts/python.exe"), "-m", "configurator.cli.configure", "--profile", "barsim", "--out", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert (out/"project.yaml").exists()