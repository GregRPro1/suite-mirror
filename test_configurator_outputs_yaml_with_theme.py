
import subprocess, pathlib, json, sys
import yaml, jsonschema

def test_configurator_outputs_yaml_with_theme(tmp_path):
    root = pathlib.Path(".").resolve()
    outdir = tmp_path / "proj"
    args = [
        str(root/".venv/Scripts/python.exe"), "-m", "configurator.cli.configure",
        "--profile", "barsim",
        "--out", str(outdir),
        "--brand-base-color", "#0b3d91",
        "--brand-accent-color", "#ffcc00",
        "--window-width", "1400", "--window-height", "900", "--window-maximized", "false",
        "--layout", "wide-right",
        "--panels", "ProjectExplorer,Jobs,Logs,Settings"
    ]
    r = subprocess.run(args, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    proj_yaml = outdir / "project.yaml"
    assert proj_yaml.exists()

    data = yaml.safe_load(proj_yaml.read_text(encoding="utf-8"))
    # schema validation
    schema_path = root / "data/schema/project.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.validate(instance=data, schema=schema)

    # key checks
    ui = data.get("ui", {})
    assert ui.get("theme", {}).get("base_color") == "#0b3d91"
    assert ui.get("theme", {}).get("accent_color") == "#ffcc00"
    assert ui.get("window", {}).get("default_size") == [1400, 900]
    assert ui.get("layout", {}).get("preset") == "wide-right"
    assert "panels" in data and isinstance(data["panels"], list) and data["panels"]
