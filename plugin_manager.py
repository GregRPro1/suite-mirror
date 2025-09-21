from __future__ import annotations
from typing import Dict
from PyQt6.QtWidgets import QDockWidget
from ..ui.widgets.jobs_panel import JobsPanel
from ..ui.widgets.logs_panel import LogsPanel

class PluginManager:
    def __init__(self, actions, jobs, themes):
        self.actions = actions; self.jobs=jobs; self.themes=themes
        self._panels: Dict[str, QDockWidget] = {}

    def load_builtin_panels(self, main_window):
        self.register_panel(main_window, "panel.jobs", "Jobs", JobsPanel(main_window, self.jobs))
        self.register_panel(main_window, "panel.logs", "Logs", LogsPanel(main_window))

    def register_panel(self, main_window, panel_id: str, title: str, widget):
        dock = QDockWidget(title, main_window)
        dock.setObjectName(panel_id)
        dock.setWidget(widget)
        main_window.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, dock)
        self._panels[panel_id] = dock

    def toggle_panel(self, main_window, panel_id: str):
        dock = self._panels.get(panel_id)
        if dock:
            dock.setVisible(not dock.isVisible())