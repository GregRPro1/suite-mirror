
import yaml, pathlib

def test_layout_keys_roundtrip(tmp_path):
    # Create a minimal project.yaml with UI keys; ensure we can read them back
    proj = tmp_path / "proj"; proj.mkdir()
    data = {
        "project": {"id":"x","name":"x","version":"0.0.1","profile":"test"},
        "ui": {
            "theme": {"base_color":"#111","accent_color":"#eee"},
            "window": {"default_size":[1200,800], "maximized": False},
            "layout": {"preset":"wide-right"},
            "statusbar": {"pinned_macros":[]}
        },
        "panels": ["ProjectExplorer","Jobs","Logs"]
    }
    (proj/"project.yaml").write_text(yaml.safe_dump(data), encoding="utf-8")
    # read via yaml (simulating ProjectManager)
    y = yaml.safe_load((proj/"project.yaml").read_text(encoding="utf-8"))
    ui = y.get("ui", {})
    assert ui.get("layout", {}).get("preset") == "wide-right"
    assert ui.get("window", {}).get("default_size") == [1200,800]
