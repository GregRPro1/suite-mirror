
# Placeholder (non-PyQt) log panel shim for headless tests
from pathlib import Path
class LogPanel:
    def __init__(self, log_path: str | Path):
        self.path = Path(log_path)
    def tail(self, n: int = 50) -> list[str]:
        if not self.path.exists():
            return []
        with open(self.path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return [l.rstrip('\n') for l in lines[-n:]]
