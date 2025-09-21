from __future__ import annotations
import sys, json, argparse, pathlib
from PyQt6.QtWidgets import QApplication
from .main_window import MainWindow
from ..services.project_manager import ProjectManager
from ..services.plugin_manager import PluginManager
from ..services.action_registry import ActionRegistry
from ..services.theme_manager import ThemeManager
from ..services.job_runner import JobRunner
from ..services.settings_manager import SettingsManager

def parse_args():
    ap = argparse.ArgumentParser("base_app")
    ap.add_argument("--project", type=str, help="Path to project.yaml")
    ap.add_argument("--headless", action="store_true")
    return ap.parse_args()

def main():
    args = parse_args()
    if args.headless:
        print("Headless mode not implemented in skeleton.")
        sys.exit(0)

    app = QApplication(sys.argv)
    app.setApplicationName("SuiteBaseApp")

    settings = SettingsManager()
    jobs = JobRunner()
    actions = ActionRegistry()
    themes = ThemeManager()
    plugins = PluginManager(actions=actions, jobs=jobs, themes=themes)
    projects = ProjectManager()

    mw = MainWindow(actions=actions, jobs=jobs, themes=themes, plugins=plugins, projects=projects, settings=settings)

    if args.project:
        projects.open_project(pathlib.Path(args.project))

    mw.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()