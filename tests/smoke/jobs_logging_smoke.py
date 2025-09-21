import os, sys, importlib, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

def safe_import(modname):
    try:
        return importlib.import_module(modname)
    except Exception as e:
        # Not fatal for smokes; presence/integrity is separately checked
        return None

def test_job_runner_and_logs_dirs():
    assert (REPO_ROOT / 'job_runner.py').exists() or (REPO_ROOT/'base_app'/'core'/'job_runner.py').exists()
    logs_dir = REPO_ROOT / 'tmp' / 'logs'
    logs_dir.mkdir(parents=True, exist_ok=True)
    assert logs_dir.exists()
