
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

@dataclass
class Action:
    id: str
    title: str
    handler: Callable
    category: str = 'General'
    shortcut: Optional[str] = None
    description: Optional[str] = None

class ActionRegistry:
    def __init__(self):
        self._actions: Dict[str, Action] = {}

    def register(self, action: Action):
        self._actions[action.id] = action

    def register_simple(self, id: str, title: str, handler: Callable, **kw):
        self.register(Action(id=id, title=title, handler=handler, **kw))

    def get(self, id: str) -> Optional[Action]:
        return self._actions.get(id)

    def all(self) -> Dict[str, Action]:
        return dict(self._actions)

    def invoke(self, id: str, *args, **kwargs):
        act = self.get(id)
        if not act:
            raise KeyError(id)
        return act.handler(*args, **kwargs)
