
from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QCheckBox, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from ...services.feedback_service import submit_ticket
import pathlib

class FeedbackPanel(QWidget):
    def __init__(self, parent=None, project_dir: pathlib.Path | None=None):
        super().__init__(parent)
        self.project_dir = project_dir
        self.setObjectName("panel.feedback")
        self._build()

    def _build(self):
        self.type = QComboBox(self)
        self.type.addItems(["bug","feature","question"])
        self.title = QLineEdit(self); self.title.setPlaceholderText("Title")
        self.desc = QTextEdit(self); self.desc.setPlaceholderText("Describe the issue or request...")
        self.attach_logs = QCheckBox("Include logs (if any)", self); self.attach_logs.setChecked(True)

        self.btn_submit = QPushButton("Submit", self)
        self.btn_submit.clicked.connect(self._submit)

        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Type:")); lay.addWidget(self.type)
        lay.addWidget(QLabel("Title:")); lay.addWidget(self.title)
        lay.addWidget(QLabel("Description:")); lay.addWidget(self.desc)
        lay.addWidget(self.attach_logs)
        lay.addWidget(self.btn_submit); lay.addStretch(1)

    def _submit(self):
        if not self.project_dir:
            d = QFileDialog.getExistingDirectory(self, "Select project directory")
            if not d: 
                return
            self.project_dir = pathlib.Path(d)
        kind = self.type.currentText()
        title = self.title.text().strip() or "(untitled)"
        desc = self.desc.toPlainText().strip()
        bundle = submit_ticket(self.project_dir, title, desc, kind)
        QMessageBox.information(self, "Feedback", f"Ticket written: {bundle}")
