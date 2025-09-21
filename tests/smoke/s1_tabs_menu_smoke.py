
import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
from PyQt6 import QtWidgets, QtCore
from base_app.core.main_window import MainWindow

def test_tabify_two_new_panels():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    win = MainWindow()
    win.add_panel()
    win.add_panel()
    app.processEvents()
    # collect right-area docks
    rights = [d for d in win.findChildren(QtWidgets.QDockWidget) if win.dockWidgetArea(d) == QtCore.Qt.DockWidgetArea.RightDockWidgetArea]
    assert len(rights) >= 2
    tabbed = win.tabifiedDockWidgets(rights[0])
    assert any(d is rights[1] for d in tabbed) or any(d is rights[0] for d in win.tabifiedDockWidgets(rights[1]))
