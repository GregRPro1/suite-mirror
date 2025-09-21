
import os, pathlib, subprocess, time

def test_crash_marker_on_exception(tmp_path):
    root = pathlib.Path('.').resolve()
    outdir = tmp_path / 'proj'
    py = root/'.venv/Scripts/python.exe'
    cfg = [str(py), '-m','configurator.cli.configure','--profile','barsim','--out', str(outdir)]
    r = subprocess.run(cfg, capture_output=True, text=True); assert r.returncode == 0

    env = os.environ.copy(); env['DEMO_RAISE'] = '1'
    r2 = subprocess.run([str(py), '-m','base_app.demo_app','--project', str(outdir),'--profile','barsim','--headless'], capture_output=True, text=True, env=env)
    crash_dir = root / '_results' / 'crash'
    time.sleep(0.1)
    assert (crash_dir / 'last_crash.json').exists()
    assert (crash_dir / 'crash.jsonl').exists()
