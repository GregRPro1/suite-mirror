
from __future__ import annotations
from collections import deque
from time import time

class Notifications:
    def __init__(self, max_items: int=100):
        self._q = deque(maxlen=max_items)

    def add(self, title: str, body: str=""):
        self._q.append({"ts": time(), "title": title, "body": body})

    def list(self):
        return list(self._q)
