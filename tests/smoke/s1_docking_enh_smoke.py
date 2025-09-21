import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from pathlib import Path
from PyQt6 import QtWidgets
from base_app.core.main_window import MainWindow
from base_app.core.docking_manager import DockingManager

def test_project_layout_paths(tmp_path, monkeypatch):
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    monkeypatch.chdir(tmp_path)
    win = MainWindow()
    ini = win.dm.save_layout(project_id='demo')
    assert ini.name == 'demo.ini' and ini.exists()
    # mutate state and restore
    win.dm.load_layout(project_id='demo')
