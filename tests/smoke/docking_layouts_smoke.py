import os, sys, importlib, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

def safe_import(modname):
    try:
        return importlib.import_module(modname)
    except Exception as e:
        # Not fatal for smokes; presence/integrity is separately checked
        return None

def test_base_dirs_present():
    assert (REPO_ROOT / 'base_app').exists(), 'base_app/ missing'
    assert (REPO_ROOT / 'ui').exists() or (REPO_ROOT / 'widgets').exists(), 'ui/ or widgets/ missing'

def test_main_window_present():
    candidates = [REPO_ROOT/'main_window.py', REPO_ROOT/'base_app'/'core'/'main_window.py']
    assert any(p.exists() for p in candidates), 'main_window.py not found'

def test_layout_artifacts_dirs():
    # Ensure directories where layouts/logs would be saved exist or are creatable
    for d in ['_results', 'profiles', 'projects']:
        p = REPO_ROOT / d
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        assert p.exists()
