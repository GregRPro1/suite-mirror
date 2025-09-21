
from __future__ import annotations
from PyQt6 import QtWidgets, QtCore, QtGui
from .docking_manager import DockingManager
from .action_registry import ActionRegistry
from .command_palette import CommandPalette
from .panels.example_panel import ExamplePanel

def default_project_id() -> str:
    return 'default'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName('MainWindow')
        self.setWindowTitle('Suite Base App')
        self.dm = DockingManager(self)
        self.registry = ActionRegistry()

        # central
        cw = QtWidgets.QWidget(self); self.setCentralWidget(cw)
        cw.setLayout(QtWidgets.QVBoxLayout())

        # initial example docks
        self._dock_counter = 0
        self.dockLeft = self._make_dock('Left', area=QtCore.Qt.DockWidgetArea.LeftDockWidgetArea)
        self.dockBottom = self._make_dock('Bottom', area=QtCore.Qt.DockWidgetArea.BottomDockWidgetArea)

        # menus / toolbar / shortcuts
        self._build_menus()
        self._build_toolbar()
        self._register_actions()
        self._bind_shortcuts()

    # ----- UI builders -----
    def _build_menus(self):
        mb = self.menuBar()
        self.menuFile = mb.addMenu('&File')
        self.menuView = mb.addMenu('&View')
        self.menuWindow = mb.addMenu('&Window')
        self.menuHelp = mb.addMenu('&Help')

        self.actNewPanel = QtGui.QAction('New Panel', self)
        self.actNewPanel.triggered.connect(self.add_panel)
        self.menuFile.addAction(self.actNewPanel)

        self.actSaveLayout = QtGui.QAction('Save Layout', self)
        self.actSaveLayout.triggered.connect(lambda: self.dm.save_layout(project_id=default_project_id()))
        self.menuWindow.addAction(self.actSaveLayout)

        self.actRestoreLayout = QtGui.QAction('Restore Layout', self)
        self.actRestoreLayout.triggered.connect(lambda: self.dm.load_layout(project_id=default_project_id()))
        self.menuWindow.addAction(self.actRestoreLayout)

        self.actShowPalette = QtGui.QAction('Command Palette', self)
        self.actShowPalette.triggered.connect(self.show_palette)
        self.menuHelp.addAction(self.actShowPalette)

    def _build_toolbar(self):
        tb = self.addToolBar('Main')
        tb.setObjectName('MainToolbar')
        tb.addAction(self.actNewPanel)
        tb.addSeparator()
        tb.addAction(self.actSaveLayout)
        tb.addAction(self.actRestoreLayout)
        tb.addSeparator()
        tb.addAction(self.actShowPalette)

    def _register_actions(self):
        # Also expose via registry (palette)
        self.registry.register_simple('panel.new', 'New Panel', self.add_panel, category='Panels', shortcut='Ctrl+N')
        self.registry.register_simple('layout.save', 'Save Layout',
                                      lambda: self.dm.save_layout(project_id=default_project_id()),
                                      category='Layout', shortcut='Ctrl+Alt+S')
        self.registry.register_simple('layout.restore', 'Restore Layout',
                                      lambda: self.dm.load_layout(project_id=default_project_id()),
                                      category='Layout', shortcut='Ctrl+Alt+R')
        self.registry.register_simple('palette.show', 'Show Command Palette', self.show_palette,
                                      category='General', shortcut='Ctrl+Shift+P')

    def _bind_shortcuts(self):
        for act in self.registry.all().values():
            if act.shortcut:
                sc = QtGui.QShortcut(QtGui.QKeySequence(act.shortcut), self)
                sc.activated.connect(lambda a=act: self.registry.invoke(a.id))

    # ----- Panels / docking -----
    def _make_dock(self, title: str, area: QtCore.Qt.DockWidgetArea):
        dock = QtWidgets.QDockWidget(title, self)
        dock.setObjectName(f'dock_{title}')
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable |
                         QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                         QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        panel = ExamplePanel(name=title, parent=dock)
        dock.setWidget(panel)
        self.addDockWidget(area, dock)
        return dock

    def add_panel(self):
        self._dock_counter += 1
        name = f'Panel{self._dock_counter}'
        dock = QtWidgets.QDockWidget(name, self)
        dock.setObjectName(f'dock_{name}')
        dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetMovable |
                         QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetFloatable |
                         QtWidgets.QDockWidget.DockWidgetFeature.DockWidgetClosable)
        dock.setAllowedAreas(QtCore.Qt.DockWidgetArea.AllDockWidgetAreas)
        dock.setWidget(ExamplePanel(name=name, parent=dock))
        # place on right if left exists, otherwise left
        self.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dock)
        # if there is already a dock on the right, tabify with it
        rights = [d for d in self.findChildren(QtWidgets.QDockWidget) if self.dockWidgetArea(d) == QtCore.Qt.DockWidgetArea.RightDockWidgetArea and d is not dock]
        if rights:
            self.tabifyDockWidget(rights[0], dock)
        dock.raise_()

    def show_palette(self):
        dlg = CommandPalette(self.registry, self)
        dlg.setModal(True)
        dlg.show(); dlg.raise_(); dlg.activateWindow()
