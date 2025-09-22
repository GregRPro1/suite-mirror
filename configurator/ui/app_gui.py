from __future__ import annotations
import sys, pathlib, subprocess, tempfile, shutil, json
from typing import Optional
from PyQt6 import QtWidgets, QtGui, QtCore

ROOT = pathlib.Path(".").resolve()

def _python_exe() -> str:
    venv = ROOT / ".venv" / "Scripts" / "python.exe"
    return str(venv if venv.exists() else sys.executable)

class DropLogoLabel(QtWidgets.QLabel):
    fileSelected = QtCore.pyqtSignal(str)
    def __init__(self):
        super().__init__("Drop logo here or click to choose…")
        self.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)

    def mousePressEvent(self, e):
        dlg = QtWidgets.QFileDialog(self, "Choose logo", str(ROOT))
        dlg.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)
        dlg.setNameFilters(["Images (*.png *.jpg *.jpeg *.svg *.ico)", "All files (*.*)"])
        if dlg.exec():
            paths = dlg.selectedFiles()
            if paths:
                self.fileSelected.emit(paths[0])

    def dragEnterEvent(self, e: QtGui.QDragEnterEvent):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e: QtGui.QDropEvent):
        for url in e.mimeData().urls():
            if url.isLocalFile():
                self.fileSelected.emit(url.toLocalFile())
                break

class ColorField(QtWidgets.QWidget):
    changed = QtCore.pyqtSignal(str)
    def __init__(self, label: str):
        super().__init__()
        self._line = QtWidgets.QLineEdit()
        self._btn  = QtWidgets.QPushButton("Pick")
        self._btn.clicked.connect(self._pick)
        layout = QtWidgets.QHBoxLayout(self); layout.setContentsMargins(0,0,0,0)
        layout.addWidget(QtWidgets.QLabel(label))
        layout.addWidget(self._line, 1)
        layout.addWidget(self._btn)
        self._line.textChanged.connect(self._on_text)

    def set(self, value: str):
        self._line.setText(value or "")

    def value(self) -> str:
        return self._line.text().strip()

    def _on_text(self, s: str):
        self.changed.emit(self.value())

    def _pick(self):
        col = QtWidgets.QColorDialog.getColor(parent=self)
        if col.isValid():
            self._line.setText(col.name())
            self.changed.emit(self.value())

class ConfiguratorWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suite Configurator")
        self.resize(900, 600)

        # central
        cw = QtWidgets.QWidget(); self.setCentralWidget(cw)
        grid = QtWidgets.QGridLayout(cw); grid.setContentsMargins(8,8,8,8); grid.setHorizontalSpacing(12); grid.setVerticalSpacing(8)

        # profile / output
        self.profile = QtWidgets.QLineEdit("barsim")
        self.outdir  = QtWidgets.QLineEdit(str((ROOT / "_demo" / "proj").resolve()))
        browse = QtWidgets.QPushButton("Browse…"); browse.clicked.connect(self._choose_outdir)
        grid.addWidget(QtWidgets.QLabel("Profile"), 0,0); grid.addWidget(self.profile, 0,1,1,2)
        grid.addWidget(QtWidgets.QLabel("Output dir"), 1,0); grid.addWidget(self.outdir, 1,1); grid.addWidget(browse, 1,2)

        # feature toggles
        self.chk_db = QtWidgets.QCheckBox("Enable database integration"); self.chk_db.setChecked(False)
        self.chk_rec = QtWidgets.QCheckBox("Enable recorder/macro"); self.chk_rec.setChecked(True)
        grid.addWidget(QtWidgets.QLabel("Features"), 2,0); grid.addWidget(self.chk_db, 2,1); grid.addWidget(self.chk_rec, 2,2)

        # colors
        self.base_color = ColorField("Base HEX"); self.base_color.set("#0b3d91")
        self.accent_color = ColorField("Accent HEX"); self.accent_color.set("#ffcc00")
        grid.addWidget(QtWidgets.QLabel("Branding"), 3,0); grid.addWidget(self.base_color, 3,1,1,2)
        grid.addWidget(QtWidgets.QLabel(""), 4,0); grid.addWidget(self.accent_color, 4,1,1,2)

        # window defaults
        self.width  = QtWidgets.QSpinBox(); self.width.setRange(300, 9999); self.width.setValue(1400)
        self.height = QtWidgets.QSpinBox(); self.height.setRange(200, 9999); self.height.setValue(900)
        self.maximized = QtWidgets.QCheckBox("Start maximized"); self.maximized.setChecked(False)
        hl = QtWidgets.QHBoxLayout(); hl.addWidget(QtWidgets.QLabel("W")); hl.addWidget(self.width); hl.addWidget(QtWidgets.QLabel("H")); hl.addWidget(self.height); hl.addWidget(self.maximized); hl.addStretch(1)
        grid.addWidget(QtWidgets.QLabel("Window"), 5,0); grid.addLayout(hl, 5,1,1,2)

        # layout + panels
        self.layout_preset = QtWidgets.QComboBox(); self.layout_preset.addItems(["wide-right", "wide-left", "single"])
        self.panels = QtWidgets.QLineEdit("ProjectExplorer,Jobs,Logs,Settings")
        grid.addWidget(QtWidgets.QLabel("Layout"), 6,0); grid.addWidget(self.layout_preset, 6,1,1,2)
        grid.addWidget(QtWidgets.QLabel("Panels (CSV)"), 7,0); grid.addWidget(self.panels, 7,1,1,2)

        # logo
        self.logo = DropLogoLabel()
        self.logo.fileSelected.connect(self._on_logo_pick)
        self.logo_path: Optional[pathlib.Path] = None
        grid.addWidget(QtWidgets.QLabel("Logo"), 8,0); grid.addWidget(self.logo, 8,1,1,2)

        # actions
        self.btn_generate = QtWidgets.QPushButton("Generate")
        self.btn_run = QtWidgets.QPushButton("Generate && Run")
        self.btn_generate.clicked.connect(self._on_generate_clicked)
        self.btn_run.clicked.connect(lambda: self._on_generate_clicked(run_after=True))
        bl = QtWidgets.QHBoxLayout(); bl.addStretch(1); bl.addWidget(self.btn_generate); bl.addWidget(self.btn_run)
        grid.addLayout(bl, 9,0,1,3)

        # status
        self.statusBar().showMessage("Ready")

    def _choose_outdir(self):
        d = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose output directory", self.outdir.text())
        if d:
            self.outdir.setText(d)

    def _on_logo_pick(self, path: str):
        p = pathlib.Path(path)
        self.logo_path = p if p.exists() else None
        self.logo.setText(str(p))

    def _cli_args(self, outdir: pathlib.Path):
        args = [
            _python_exe(), "-m", "configurator.cli.configure",
            "--profile", self.profile.text().strip(),
            "--out", str(outdir),
            "--brand-base-color", self.base_color.value(),
            "--brand-accent-color", self.accent_color.value(),
            "--window-width", str(self.width.value()),
            "--window-height", str(self.height.value()),
            "--window-maximized", "true" if self.maximized.isChecked() else "false",
            "--layout", self.layout_preset.currentText(),
            "--panels", self.panels.text().strip()
        ]
        if self.chk_db.isChecked():
            args += ["--feature-db", "on"]
        return args

    def _on_generate_clicked(self, run_after: bool=False):
        outdir = pathlib.Path(self.outdir.text().strip())
        outdir.mkdir(parents=True, exist_ok=True)

        # copy logo if chosen
        if self.logo_path and self.logo_path.exists():
            (outdir / "assets").mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.logo_path, outdir / "assets" / self.logo_path.name)

        args = self._cli_args(outdir)
        r = subprocess.run(args, capture_output=True, text=True)
        if r.returncode != 0:
            QtWidgets.QMessageBox.critical(self, "Configurator", f"CLI failed:\\n{r.stderr}")
            self.statusBar().showMessage("Configurator failed")
            return

        self.statusBar().showMessage("Project generated")
        if run_after:
            self._run_demo(outdir)

    def _run_demo(self, project_dir: pathlib.Path):
        script = ROOT / "scripts" / "run_demo.ps1"
        if script.exists():
            subprocess.Popen(["pwsh", str(script)], cwd=str(ROOT))
        else:
            subprocess.Popen([_python_exe(), "-m", "base_app.demo_app", "--project", str(project_dir)], cwd=str(ROOT))

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = ConfiguratorWindow()
    w.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
