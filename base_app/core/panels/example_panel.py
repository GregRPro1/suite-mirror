
from __future__ import annotations
from PyQt6 import QtWidgets

class ExamplePanel(QtWidgets.QWidget):
    def __init__(self, name: str, parent=None):
        super().__init__(parent)
        self.setObjectName(name)
        lay = QtWidgets.QVBoxLayout(self)
        txt = QtWidgets.QTextEdit(self)
        txt.setPlaceholderText(f"Panel: {name} — type here...")
        lay.addWidget(txt)
