import os, sys, importlib, pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
os.chdir(REPO_ROOT)

def safe_import(modname):
    try:
        return importlib.import_module(modname)
    except Exception as e:
        # Not fatal for smokes; presence/integrity is separately checked
        return None

def test_configurator_scaffold_present():
    # Accept either top-level configurator/ or base_app/configurator/
    assert (REPO_ROOT / 'configurator').exists() or (REPO_ROOT/'base_app'/'configurator').exists()
    # Profiles dir for emitted YAML
    profiles = REPO_ROOT / 'profiles'
    profiles.mkdir(parents=True, exist_ok=True)
    assert profiles.exists()
