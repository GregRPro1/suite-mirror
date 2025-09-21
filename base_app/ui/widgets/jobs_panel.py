from __future__ import annotations
import pathlib
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class JobsPanel(QWidget):
    def __init__(self, parent, jobs):
        super().__init__(parent)
        self.jobs = jobs
        self.lbl = QLabel("No jobs running", self)
        self.btn = QPushButton("Run Dummy Job", self)
        self.btn.clicked.connect(self._run)
        lay = QVBoxLayout(self); lay.addWidget(self.btn); lay.addWidget(self.lbl)

    def _run(self):
        dir = QFileDialog.getExistingDirectory(self, "Choose artifacts folder")
        if not dir: return
        jid = self.jobs.run_dummy(pathlib.Path(dir))
        self.lbl.setText(f"Job started: {jid}")