from __future__ import annotations
import yaml, json, pathlib
from jsonschema import validate

def load_profile(profile_path: pathlib.Path) -> dict:
    return yaml.safe_load(profile_path.read_text(encoding="utf-8"))

def emit_project(profile: dict, out_dir: pathlib.Path) -> pathlib.Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    project = {
        "generator": {"tool":"Configurator","version":"1.0.0"},
        "project": {"id": out_dir.name, "name": out_dir.name, "version":"0.1.0", "profile": profile.get("profile_id","base")},
        "ui": profile.get("ui", {"brand_id":"base","window_defaults":{"width":1280,"height":800,"maximized":False}}),
        "capabilities": profile.get("capabilities", {}),
        "plugins": profile.get("plugins", {"include":[],"exclude":[]}),
    }
    
    project["feedback"] = {
        "enabled": True,
        "sinks": [
            {"kind":"fileshare","id":"local_inbox","config":{"path":"./inbox"}}
        ]
    }
    
    out_path = out_dir / "project.yaml"
    out_path.write_text(yaml.safe_dump(project, sort_keys=False), encoding="utf-8")
    return out_path