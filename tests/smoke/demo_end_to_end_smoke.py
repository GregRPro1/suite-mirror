
import os, pathlib, subprocess, sys, json
def test_demo_headless(tmp_path):
    root = pathlib.Path('.').resolve()
    outdir = tmp_path / 'proj'
    py = root/'.venv/Scripts/python.exe'
    args = [
        str(py), '-m','configurator.cli.configure',
        '--profile','barsim','--out', str(outdir),
        '--brand-base-color','#0b3d91','--brand-accent-color','#ffcc00',
        '--window-width','1200','--window-height','800','--window-maximized','false',
        '--layout','wide-right','--panels','ProjectExplorer,Jobs,Logs,Settings'
    ]
    r = subprocess.run(args, capture_output=True, text=True)
    assert r.returncode == 0
    proj_yaml = outdir / 'project.yaml'
    assert proj_yaml.exists()
    # launch demo headless
    r2 = subprocess.run([str(py), '-m','base_app.demo_app','--project', str(outdir),'--profile','barsim','--headless'], capture_output=True, text=True)
    assert r2.returncode == 0
