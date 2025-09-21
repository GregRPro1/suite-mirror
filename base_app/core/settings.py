
from __future__ import annotations
from PyQt6 import QtCore

_ORG = "Suite"
_APP = "BaseApp"

class AppSettings:
    def __init__(self):
        self._s = QtCore.QSettings(_ORG, _APP)

    def get(self, key: str, default=None):
        v = self._s.value(key, defaultValue=default)
        return v

    def set(self, key: str, value) -> None:
        self._s.setValue(key, value)

    def sync(self) -> None:
        self._s.sync()
