from __future__ import annotations
from typing import Callable, Dict

class ActionRegistry:
    def __init__(self) -> None:
        self._actions: Dict[str, dict] = {}
        self._observer: Callable[[str, str, dict], None] | None = None  # event_type, action_id, args

    def attach_recorder(self, observer: Callable[[str, str, dict], None]) -> None:
        """Attach a semantic event observer. Called as observer('action.invoke', action_id, args)."""
        self._observer = observer

    def register(self, spec: dict) -> None:
        if "id" not in spec or "handler" not in spec:
            raise ValueError("ActionSpec requires id and handler")
        self._actions[spec["id"]] = spec

    def invoke(self, action_id: str, args: dict | None = None) -> None:
        spec = self._actions[action_id]
        args = args or {}
        if self._observer:
            try:
                self._observer("action.invoke", action_id, args)
            except Exception:
                pass  # Never let observer failures break actions
        spec["handler"](None, args)

    def list(self) -> list[dict]:
        return list(self._actions.values())
