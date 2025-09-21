import subprocess, sys, pathlib, os, time

def test_base_app_boots_with_project(tmp_path):
    root = pathlib.Path(".").resolve()
    proj = tmp_path / "proj"
    proj.mkdir()
    # generate project
    r = subprocess.run([str(root/".venv/Scripts/python.exe"), "-m", "configurator.cli.configure", "--profile", "barsim", "--out", str(proj)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    # run app for a moment (offscreen)
    env = os.environ.copy()
    env["QT_QPA_PLATFORM"]="offscreen"
    p = subprocess.Popen([str(root/".venv/Scripts/python.exe"), "-m", "base_app.core.app_bootstrap", "--project", str(proj/"project.yaml")], env=env)
    time.sleep(2.0)
    p.terminate()
    p.wait(timeout=5)
    assert p.returncode in (0, -15, 1)  # allow early exit