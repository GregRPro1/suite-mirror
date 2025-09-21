from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
class LogsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.text = QTextEdit(self); self.text.setReadOnly(True)
        self.text.setPlainText("Logs (skeleton)")
        lay = QVBoxLayout(self); lay.addWidget(self.text)