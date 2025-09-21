from __future__ import annotations
import pathlib, yaml

class ProjectManager:
    def __init__(self):
        self.current: dict | None = None

    def open_project(self, path: pathlib.Path):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict) or "project" not in data:
            raise ValueError("Invalid project.yaml in skeleton")
        self.current = data
        return data