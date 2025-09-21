from pathlib import Path
from configurator.gui import write_profile
def test_config_gui_writer(tmp_path):
    y, q = write_profile('CoX', '#111111', '#eeeeee', tmp_path/'profiles', tmp_path/'ui'/'qss')
    assert y.exists() and q.exists()
