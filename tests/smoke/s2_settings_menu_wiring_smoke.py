import pathlib
def test_settings_menu_wiring_present():
    p = pathlib.Path('main_window.py')
    assert p.exists(), 'main_window.py missing'
    t = p.read_text(encoding='utf-8')
    assert 'from base_app.ui.open_settings import show_settings_dialog' in t
    assert 'QtGui.QAction' in t
    assert ('settings.open' in t) or ('Settings…' in t)
