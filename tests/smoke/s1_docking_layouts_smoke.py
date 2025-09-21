import os, sys
from pathlib import Path
os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # headless
from PyQt6 import QtWidgets
from base_app.core.main_window import MainWindow

def test_layout_save_restore(tmp_path):
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    win = MainWindow()
    ini = tmp_path / 'layouts' / 'proj1.ini'
    saved = win.dm.save_layout(ini)
    assert saved.exists()
    # move docks to modify state
    win.tabifyDockWidget(win.example_left, win.example_bottom)
    assert win.dm.load_layout(ini)  # restore succeeds
