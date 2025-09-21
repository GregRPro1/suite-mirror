
from __future__ import annotations
from PyQt6 import QtWidgets, QtGui
from pathlib import Path

def write_profile(name: str, primary: str, secondary: str, profiles: Path, qss_dir: Path):
    profiles.mkdir(parents=True, exist_ok=True)
    qss_dir.mkdir(parents=True, exist_ok=True)
    y = profiles / f"{name}.yaml"
    y.write_text(f"name: {name}\ncreated: gui\ntheme:\n  primary: {primary}\n  secondary: {secondary}\n", encoding='utf-8')
    q = qss_dir / f"{name}.qss"
    q.write_text(f"QWidget {{ background: {secondary}; }}\nQPushButton {{ background: {primary}; }}\n", encoding='utf-8')
    return y, q

class ConfiguratorWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Configurator')
        self.name = QtWidgets.QLineEdit('Company')
        self.primary = QtWidgets.QLineEdit('#2d6cdf')
        self.secondary = QtWidgets.QLineEdit('#f0f2f5')
        self.btn = QtWidgets.QPushButton('Write Theme')
        self.out = QtWidgets.QTextEdit()
        lay = QtWidgets.QFormLayout(self)
        lay.addRow('Name', self.name)
        lay.addRow('Primary', self.primary)
        lay.addRow('Secondary', self.secondary)
        lay.addRow(self.btn)
        lay.addRow(self.out)
        self.btn.clicked.connect(self.on_write)

    def on_write(self):
        name = self.name.text().strip() or 'Company'
        y, q = write_profile(name, self.primary.text().strip(), self.secondary.text().strip(), Path('profiles'), Path('ui/qss'))
        self.out.append(f"Wrote: {y} \nWrote: {q}")
