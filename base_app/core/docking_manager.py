
from __future__ import annotations
from pathlib import Path
from PyQt6 import QtCore, QtWidgets

class DockingManager:
    """Save/restore QMainWindow geometry + dock state.
    - If project_id is provided, persists to .suite/layouts/<project_id>.ini
    - Else uses the explicit ini_path
    """
    def __init__(self, main_window: QtWidgets.QMainWindow):
        self.win = main_window

    @staticmethod
    def project_ini(project_id: str) -> Path:
        base = Path('.suite') / 'layouts'
        base.mkdir(parents=True, exist_ok=True)
        return base / f"{project_id}.ini"

    def save_layout(self, ini_path: str | Path | None = None, project_id: str | None = None):
        if project_id:
            ini_path = self.project_ini(project_id)
        if ini_path is None:
            raise ValueError('ini_path or project_id required')
        ini = Path(ini_path)
        ini.parent.mkdir(parents=True, exist_ok=True)
        settings = QtCore.QSettings(str(ini), QtCore.QSettings.Format.IniFormat)
        settings.setValue('geometry', self.win.saveGeometry())
        settings.setValue('windowState', self.win.saveState())
        settings.sync()
        return ini

    def load_layout(self, ini_path: str | Path | None = None, project_id: str | None = None) -> bool:
        if project_id:
            ini_path = self.project_ini(project_id)
        if ini_path is None:
            raise ValueError('ini_path or project_id required')
        ini = Path(ini_path)
        if not ini.exists():
            return False
        settings = QtCore.QSettings(str(ini), QtCore.QSettings.Format.IniFormat)
        geom = settings.value('geometry', None)
        state = settings.value('windowState', None)
        if geom is not None:
            self.win.restoreGeometry(geom)
        if state is not None:
            self.win.restoreState(state)
        return True
