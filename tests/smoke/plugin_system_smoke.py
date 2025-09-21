import os, sys, importlib, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

def safe_import(modname):
    try:
        return importlib.import_module(modname)
    except Exception as e:
        # Not fatal for smokes; presence/integrity is separately checked
        return None

def test_plugins_tree_exists_or_empty():
    plugins_dir = REPO_ROOT / 'plugins'
    # not mandatory yet, but if present it must be a dir
    if plugins_dir.exists():
        assert plugins_dir.is_dir()
    else:
        # create empty to standardize environment
        plugins_dir.mkdir(parents=True, exist_ok=True)
        assert plugins_dir.exists()
