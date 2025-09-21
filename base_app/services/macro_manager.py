
from __future__ import annotations
from typing import List, Dict

class MacroManager:
    """Very small pin registry + runner stub for macros."""
    def __init__(self):
        self._pinned: List[str] = []  # action IDs

    def pin(self, action_id: str):
        if action_id not in self._pinned:
            self._pinned.append(action_id)

    def unpin(self, action_id: str):
        if action_id in self._pinned:
            self._pinned.remove(action_id)

    def pinned(self) -> List[str]:
        return list(self._pinned)

    def run(self, action_registry, action_id: str):
        # delegate to existing actions
        action_registry.invoke(action_id, {})
