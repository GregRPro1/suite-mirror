import os, sys, importlib, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

def safe_import(modname):
    try:
        return importlib.import_module(modname)
    except Exception as e:
        # Not fatal for smokes; presence/integrity is separately checked
        return None

def test_feedback_and_markers():
    # Files may or may not exist; ensure directories for outputs exist
    core = REPO_ROOT / 'base_app' / 'core'
    core.mkdir(parents=True, exist_ok=True)
    marker = core / 'crash.marker'
    if marker.exists():
        marker.unlink()
    marker.write_text('ok')
    assert marker.exists()
    marker.unlink()
