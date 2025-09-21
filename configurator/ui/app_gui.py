
from __future__ import annotations
from PyQt6 import QtWidgets, QtGui, QtCore
import subprocess, sys, pathlib

class ConfiguratorGui(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Suite Configurator")
        lay = QtWidgets.QFormLayout(self)
        self.profile = QtWidgets.QLineEdit("barsim", self)
        self.out = QtWidgets.QLineEdit(str(pathlib.Path("./_demo/proj").resolve()), self); btnOut = QtWidgets.QPushButton("Browse…")
        self.base = QtWidgets.QLineEdit("#0b3d91", self)
        self.accent = QtWidgets.QLineEdit("#ffcc00", self)
        self.w = QtWidgets.QSpinBox(self); self.w.setRange(400, 4000); self.w.setValue(1400)
        self.h = QtWidgets.QSpinBox(self); self.h.setRange(300, 4000); self.h.setValue(900)
        self.maxi = QtWidgets.QCheckBox("Maximized", self)
        self.layout = QtWidgets.QLineEdit("wide-right", self)
        self.panels = QtWidgets.QLineEdit("ProjectExplorer,Jobs,Logs,Settings", self)
        def browse_out(): 
            d = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Project Output", str(pathlib.Path(".").resolve()))
            if d: self.out.setText(d)
        btnOut.clicked.connect(browse_out)
        row = QtWidgets.QHBoxLayout(); row.addWidget(self.out); row.addWidget(btnOut)
        lay.addRow("Profile", self.profile)
        lay.addRow("Out Dir", row)
        lay.addRow("Base Color", self.base); lay.addRow("Accent Color", self.accent)
        lay.addRow("Width", self.w); lay.addRow("Height", self.h); lay.addRow(self.maxi)
        lay.addRow("Layout preset", self.layout); lay.addRow("Panels (csv)", self.panels)

        self.btnGen = QtWidgets.QPushButton("Generate", self)
        lay.addRow(self.btnGen)
        self.btnGen.clicked.connect(self._run_cli)

        self.log = QtWidgets.QPlainTextEdit(self); self.log.setReadOnly(True)
        lay.addRow(self.log)

    def _run_cli(self):
        py = str(pathlib.Path("./.venv/Scripts/python.exe").resolve())
        args = [
            py, "-m", "configurator.cli.configure",
            "--profile", self.profile.text(),
            "--out", self.out.text(),
            "--brand-base-color", self.base.text(),
            "--brand-accent-color", self.accent.text(),
            "--window-width", str(self.w.value()),
            "--window-height", str(self.h.value()),
            "--window-maximized", "true" if self.maxi.isChecked() else "false",
            "--layout", self.layout.text(),
            "--panels", self.panels.text()
        ]
        p = subprocess.run(args, capture_output=True, text=True)
        self.log.appendPlainText(" ".join(args))
        self.log.appendPlainText(p.stdout.strip())
        if p.stderr.strip():
            self.log.appendPlainText(p.stderr.strip())

def main():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    w = ConfiguratorGui(); w.resize(680, 420); w.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())
