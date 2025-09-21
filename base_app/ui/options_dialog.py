
from __future__ import annotations
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import QFile, QIODevice
from base_app.core.settings import AppSettings
from base_app.core import settings_registry

class GeneralPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = AppSettings()
        lay = QtWidgets.QFormLayout(self)
        self.fontFamily = QtWidgets.QFontComboBox(self)
        self.fontSize = QtWidgets.QSpinBox(self); self.fontSize.setRange(8, 48)
        self.scale = QtWidgets.QDoubleSpinBox(self); self.scale.setRange(0.5, 3.0); self.scale.setSingleStep(0.1)
        self.fontFamily.setCurrentText(str(s.get("ui/fontFamily", "Segoe UI")))
        self.fontSize.setValue(int(s.get("ui/fontSize", 10)))
        self.scale.setValue(float(s.get("ui/scale", 1.0)))
        lay.addRow("Font family", self.fontFamily)
        lay.addRow("Font size", self.fontSize)
        lay.addRow("UI scale", self.scale)

class ThemePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = AppSettings()
        lay = QtWidgets.QFormLayout(self)
        self.mode = QtWidgets.QComboBox(self); self.mode.addItems(["Light","Dark","Custom QSS"])
        self.qssPath = QtWidgets.QLineEdit(self); self.btnBrowse = QtWidgets.QPushButton("Browse…", self)
        self.qssPath.setEnabled(False); self.btnBrowse.setEnabled(False)
        self.mode.currentTextChanged.connect(lambda t: self._toggle_qss(t))
        self.btnBrowse.clicked.connect(self._browse)
        self.mode.setCurrentText(str(s.get("ui/themeMode","Light")))
        self.qssPath.setText(str(s.get("ui/themeQss","")))
        self._toggle_qss(self.mode.currentText())
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.qssPath); row.addWidget(self.btnBrowse)
        lay.addRow("Theme", self.mode); lay.addRow("Custom QSS", row)

    def _toggle_qss(self, t: str):
        custom = (t == "Custom QSS")
        self.qssPath.setEnabled(custom); self.btnBrowse.setEnabled(custom)

    def _browse(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select QSS", "", "QSS files (*.qss);;All files (*.*)")
        if path:
            self.qssPath.setText(path)

class DirsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = AppSettings()
        lay = QtWidgets.QFormLayout(self)
        self.logs = QtWidgets.QLineEdit(str(s.get("paths/logs", "_results")))
        self.projects = QtWidgets.QLineEdit(str(s.get("paths/projects", "_demo")))
        self.temp = QtWidgets.QLineEdit(str(s.get("paths/temp", "tmp")))
        lay.addRow("Logs", self.logs); lay.addRow("Projects", self.projects); lay.addRow("Temp", self.temp)

class DbPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        s = AppSettings()
        lay = QtWidgets.QFormLayout(self)
        self.driver = QtWidgets.QComboBox(self); self.driver.addItems(["sqlite","postgres","mysql"])
        self.host = QtWidgets.QLineEdit(str(s.get("db/host","localhost")))
        self.port = QtWidgets.QSpinBox(self); self.port.setRange(0,65535); self.port.setValue(int(s.get("db/port",5432)))
        self.user = QtWidgets.QLineEdit(str(s.get("db/user","")))
        self.name = QtWidgets.QLineEdit(str(s.get("db/name","suite")))
        lay.addRow("Driver", self.driver); lay.addRow("Host", self.host); lay.addRow("Port", self.port)
        lay.addRow("User", self.user); lay.addRow("Database", self.name)

def _apply_theme_to_app(mode: str, qss_path: str | None):
    app = QtWidgets.QApplication.instance()
    if not app: 
        return
    if mode == "Custom QSS" and qss_path:
        f = QFile(qss_path)
        if f.exists() and f.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
            data = bytes(f.readAll()).decode("utf-8", errors="ignore")
            app.setStyleSheet(data)
            f.close()
            return
    if mode == "Dark":
        app.setStyleSheet("QWidget { background: #2b2b2b; color: #d0d0d0; } QMenuBar::item:selected { background: #444; }")
    else:
        app.setStyleSheet("")

class OptionsDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.tabs = QtWidgets.QTabWidget(self)
        self.general = GeneralPage(self); self.theme = ThemePage(self); self.dirs = DirsPage(self); self.db = DbPage(self)
        self.tabs.addTab(self.general, "General")
        self.tabs.addTab(self.theme, "Theme")
        self.tabs.addTab(self.dirs, "Directories")
        self.tabs.addTab(self.db, "Database")
        for prov in settings_registry.providers():
            try:
                title, widget = prov()
                self.tabs.addTab(widget, title)
            except Exception:
                pass

        self.chkProject = QtWidgets.QCheckBox("Also save visual choices into current project's project.yaml (ui.*)", self)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                          QtWidgets.QDialogButtonBox.StandardButton.Cancel |
                                          QtWidgets.QDialogButtonBox.StandardButton.Apply, self)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.tabs); lay.addWidget(self.chkProject); lay.addWidget(btns)

        btns.accepted.connect(self._on_accept)
        btns.rejected.connect(self.reject)
        btns.button(QtWidgets.QDialogButtonBox.StandardButton.Apply).clicked.connect(self._apply_only)

    def _persist(self):
        s = AppSettings()
        s.set("ui/fontFamily", self.general.fontFamily.currentText())
        s.set("ui/fontSize", self.general.fontSize.value())
        s.set("ui/scale", float(self.general.scale.value()))
        s.set("ui/themeMode", self.theme.mode.currentText())
        s.set("ui/themeQss", self.theme.qssPath.text())
        s.set("paths/logs", self.dirs.logs.text())
        s.set("paths/projects", self.dirs.projects.text())
        s.set("paths/temp", self.dirs.temp.text())
        s.set("db/driver", self.db.driver.currentText())
        s.set("db/host", self.db.host.text())
        s.set("db/port", self.db.port.value())
        s.set("db/user", self.db.user.text())
        s.set("db/name", self.db.name.text())
        s.sync()
        _apply_theme_to_app(self.theme.mode.currentText(), self.theme.qssPath.text())

        if self.chkProject.isChecked():
            from pathlib import Path
            import yaml
            root = Path(self.parent().current_project_root() if hasattr(self.parent(),'current_project_root') else '.')
            pj = root / "project.yaml"
            data = {}
            if pj.exists():
                data = yaml.safe_load(pj.read_text(encoding="utf-8")) or {}
            ui = data.setdefault("ui", {})
            theme = ui.setdefault("theme", {})
            theme["base_color"] = theme.get("base_color", "#2d6cdf")
            theme["accent_color"] = theme.get("accent_color", "#f0f2f5")
            ui["window"] = ui.get("window", {})
            pj.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")

    def _apply_only(self):
        self._persist()

    def _on_accept(self):
        self._persist()
        self.accept()
