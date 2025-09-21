
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PyQt6 import QtWidgets
from base_app.ui.options_dialog import OptionsDialog
from base_app.core.settings import AppSettings

def test_settings_roundtrip_and_apply():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    dlg = OptionsDialog()
    # Simulate a couple of changes
    dlg.general.fontSize.setValue(13)
    dlg.theme.mode.setCurrentText("Dark")
    dlg._apply_only()
    s = AppSettings()
    assert int(s.get("ui/fontSize")) == 13
    assert s.get("ui/themeMode") == "Dark"
    # Style should be non-empty in dark mode
    assert bool(QtWidgets.QApplication.instance().styleSheet()) is True
