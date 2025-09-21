
from __future__ import annotations
from PyQt6 import QtCore, QtWidgets
from typing import List
from .action_registry import ActionRegistry

class CommandPalette(QtWidgets.QDialog):
    def __init__(self, registry: ActionRegistry, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Command Palette')
        self.registry = registry

        self.input = QtWidgets.QLineEdit(self)
        self.list = QtWidgets.QListWidget(self)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.input); lay.addWidget(self.list)

        self.input.textChanged.connect(self._refilter)
        self.input.returnPressed.connect(self._accept_enter)
        self._actions_cache = list(self.registry.all().values())
        self._refilter('')

    def _refilter(self, text: str):
        self.list.clear()
        text = (text or '').lower()
        for act in self._actions_cache:
            if text in act.title.lower() or text in act.id.lower():
                self.list.addItem(f"{act.title} [{act.id}]")

    def _accept_enter(self):
        aid = self.current_action_id()
        if aid:
            self.registry.invoke(aid)
            self.accept()

    def current_action_id(self) -> str | None:
        item = self.list.currentItem()
        if not item:
            return None
        txt = item.text()
        if '[' in txt and txt.endswith(']'):
            return txt[txt.rfind('[')+1:-1]
        return None
