
from __future__ import annotations
from PyQt6 import QtWidgets
from base_app.ui.options_dialog import OptionsDialog

def show_settings_dialog(parent: QtWidgets.QWidget | None = None):
    dlg = OptionsDialog(parent)
    dlg.setModal(True); dlg.exec()
