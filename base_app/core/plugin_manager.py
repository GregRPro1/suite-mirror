
from __future__ import annotations
import importlib, pkgutil, json, sys
from pathlib import Path
from typing import Callable, Dict, Any

class PluginManager:
    def __init__(self, plugins_dir: str | Path = 'plugins'):
        self.plugins_dir = Path(plugins_dir)
        self.actions: Dict[str, Callable[..., Any]] = {}
        self.meta: Dict[str, dict] = {}

    def discover(self) -> list[str]:
        found = []
        if not self.plugins_dir.exists():
            return found
        sys.path.insert(0, str(self.plugins_dir.resolve()))
        for pkg in pkgutil.iter_modules([str(self.plugins_dir)]):
            name = pkg.name
            # metadata (optional)
            meta_path = self.plugins_dir / name / 'plugin.json'
            if meta_path.exists():
                try:
                    self.meta[name] = json.loads(meta_path.read_text(encoding='utf-8'))
                except Exception:
                    self.meta[name] = {}
            # code
            mod = None
            for candidate in (f"{name}.plugin", f"{name}"):
                try:
                    mod = importlib.import_module(candidate)
                    break
                except Exception:
                    continue
            if not mod:
                continue
            if hasattr(mod, 'register'):
                mod.register(self)
                found.append(name)
        return found

    def register_action(self, name: str, func: Callable[..., Any]):
        self.actions[name] = func

    def get_actions(self) -> dict:
        return dict(self.actions)
