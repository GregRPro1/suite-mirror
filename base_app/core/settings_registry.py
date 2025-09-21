
from __future__ import annotations
from typing import Callable, Dict, List, Tuple

# Providers should be callables returning (title:str, widget:QWidget)
_Providers: List[Callable] = []

def register_settings_page(provider: Callable) -> None:
    _Providers.append(provider)

def providers() -> List[Callable]:
    return list(_Providers)
