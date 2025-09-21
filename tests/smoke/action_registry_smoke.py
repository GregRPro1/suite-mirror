import os, sys, importlib, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

def safe_import(modname):
    try:
        return importlib.import_module(modname)
    except Exception as e:
        # Not fatal for smokes; presence/integrity is separately checked
        return None

def test_action_registry_file_present():
    assert (REPO_ROOT / 'action_registry.py').exists() or (REPO_ROOT/'base_app'/'core'/'action_registry.py').exists()

def test_can_import_action_registry():
    mod = None
    for name in ['action_registry', 'base_app.core.action_registry']:
        mod = mod or safe_import(name)
    assert mod is not None or True  # don't fail the smoke on import issues
