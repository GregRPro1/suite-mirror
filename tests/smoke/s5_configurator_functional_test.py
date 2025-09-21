import sys, subprocess, os
from pathlib import Path
def test_configurator_cli(tmp_path):
    profiles = tmp_path/'profiles'
    qss = tmp_path/'ui'/'qss'
    profiles.mkdir(parents=True, exist_ok=True)
    qss.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, '-m', 'configurator.cli', '--name', 'TestCo', '--profiles-dir', str(profiles), '--qss-dir', str(qss)]
    rc = subprocess.call(cmd)
    assert rc == 0
    assert (profiles/'TestCo.yaml').exists()
    assert (qss/'TestCo.qss').exists()
