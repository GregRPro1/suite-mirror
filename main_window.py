from __future__ import annotations
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QTabWidget, QStatusBar, QLabel, QFileDialog, QMessageBox
from ..services.action_registry import ActionRegistry
from ..services.job_runner import JobRunner
from ..services.theme_manager import ThemeManager
from ..services.plugin_manager import PluginManager
from ..services.project_manager import ProjectManager
from ..services.settings_manager import SettingsManager

from .status_bar import StatusBarController
from ..services.interaction_recorder import InteractionRecorder
from ..services.feedback_service import submit_ticket
from ..services.crash_handler import write_crash_marker
import pathlib
class MainWindow(QMainWindow):
    def __init__(self, actions: ActionRegistry, jobs: JobRunner, themes: ThemeManager, plugins: PluginManager, projects: ProjectManager, settings: SettingsManager):
        super().__init__()
        self.actions=actions; self.jobs=jobs; self.themes=themes; self.plugins=plugins; self.projects=projects; self.settings=settings

        self.setWindowTitle("Suite Base App (Skeleton)")
        self.resize(1200, 800)

        self._center = QTabWidget(self)
        self.setCentralWidget(self._center)

        self._status = QStatusBar(self)
        self.setStatusBar(self._status)
        # Recorder
        self.recorder = InteractionRecorder()
        self.actions.attach_recorder(self.recorder.observer)
        self.status_ctrl = StatusBarController(self._status, self._toggle_recorder, lambda: self.recorder.enabled)

        self._setup_menus()
        self._register_builtin_actions()
        self.plugins.load_builtin_panels(self)

    def _setup_menus(self):
        mb = self.menuBar()
        self.menu_file = mb.addMenu("&File")
        self.menu_view = mb.addMenu("&View")
        self.menu_tools = mb.addMenu("&Tools")
        self.menu_help = mb.addMenu("&Help")

        self.menu_file.addAction("New Project…", self._new_project)
        self.menu_file.addAction("Open Project…", self._open_project)
        self.menu_file.addSeparator()
        self.menu_file.addAction("Exit", self.close)

        self.menu_view.addAction("Toggle Jobs Panel", lambda: self.plugins.toggle_panel(self, "panel.jobs"))
        self.menu_view.addAction("Toggle Logs Panel", lambda: self.plugins.toggle_panel(self, "panel.logs"))

        self.menu_tools.addAction("Command Palette (stub)", lambda: self._status.showMessage("Palette not implemented in skeleton", 3000))

        self.menu_help.addAction("Report Issue", self._report_issue)
        self.menu_help.addAction("Simulate Crash", self._simulate_crash)
        self.menu_help.addAction("About", self._about)

    def _register_builtin_actions(self):
        # minimal action for recorder toggle; just flips label in skeleton
        def toggle_recorder(_ctx=None, _args=None):
            self._toggle_recorder()
        self.actions.register({"id":"recorder.toggle","text":"Toggle Recorder","handler":toggle_recorder})

    def _new_project(self):
        QMessageBox.information(self, "New", "Use configurator CLI to create projects in this skeleton.")

    def _open_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open project.yaml", "", "YAML Files (*.yaml)")
        if path:
            import pathlib
            self.projects.open_project(pathlib.Path(path))
            self._status.showMessage(f"Project opened: {path}", 3000)

    def _about(self):
        QMessageBox.information(self, "About", "Suite Base App Skeleton\nPyQt6")


    def _report_issue(self):
        proj_dir = None
        if self.projects.current:
            # heuristic: project.yaml path unknown, ask for dir
            proj_dir = QFileDialog.getExistingDirectory(self, "Select project directory (where project.yaml lives)")
        if not proj_dir:
            QMessageBox.information(self, "Report", "Select project dir to drop a ticket bundle into its inbox.")
            return
        bundle = submit_ticket(pathlib.Path(proj_dir), "User report", "Issue description")
        self._status.showMessage(f"Ticket written: {bundle}", 4000)

    def _simulate_crash(self):
        pdir = QFileDialog.getExistingDirectory(self, "Select project directory for crash marker")
        if not pdir:
            return
        write_crash_marker(pathlib.Path(pdir)/"tmp")
        QMessageBox.critical(self, "Crash", "Simulated crash marker written. The app would exit in real scenario.")
