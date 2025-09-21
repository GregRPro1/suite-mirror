import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PyQt6 import QtWidgets
from base_app.core.main_window import MainWindow

def test_palette_invokes_registered_action(monkeypatch):
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    win = MainWindow()
    # Register test action and invoke through registry (palette would call registry.invoke)
    triggered = {'ok': False}
    win.registry.register_simple('test.hello', 'Hello', lambda: triggered.__setitem__('ok', True))
    win.registry.invoke('test.hello')
    assert triggered['ok'] is True
