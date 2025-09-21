import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from base_app.core.action_registry import ActionRegistry
from base_app.core.command_palette import CommandPalette
from PyQt6 import QtWidgets

def test_registry_and_palette_filtering():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    reg = ActionRegistry()
    reg.register_simple('file.new', 'New File', lambda: 'ok', category='File')
    reg.register_simple('edit.copy', 'Copy', lambda: 'ok', category='Edit')
    pal = CommandPalette(reg)
    pal._refilter('new')
    # after filtering, ensure at least one item shown and correct selection logic works
    assert pal.list.count() >= 1
    pal.list.setCurrentRow(0)
    act_id = pal.current_action_id()
    assert act_id in ('file.new', 'edit.copy')
