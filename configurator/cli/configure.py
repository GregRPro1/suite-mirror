
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime

def write_yaml(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"name: {payload['name']}\n")
        f.write(f"created: {payload['created']}\n")
        f.write("theme:\n")
        f.write(f"  primary: \"{payload['theme']['primary']}\"\n")
        f.write(f"  secondary: \"{payload['theme']['secondary']}\"\n")
        f.write("window:\n")
        f.write(f"  width: {payload['window']['width']}\n")
        f.write(f"  height: {payload['window']['height']}\n")
        f.write(f"  maximized: {str(payload['window']['maximized']).lower()}\n")
        if payload.get("layout"):
            f.write(f"layout: {payload['layout']}\n")
        panels = payload.get("panels") or []
        if panels:
            f.write("panels:\n")
            for p in panels:
                f.write(f"  - {p}\n")

def write_qss(path: Path, primary: str, secondary: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "/* auto-generated */",
        f"QWidget {{ background: {secondary}; }}",
        f"QPushButton {{ background: {primary}; }}",
        ""
    ]
    path.write_text("\n".join(lines), encoding="utf-8")

def _as_bool(v) -> bool:
    s = str(v).strip().lower()
    if s in ("1","true","yes","on"): return True
    if s in ("0","false","no","off",""): return False
    return False

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="configurator.cli.configure", description="Emit project profile + theme QSS")
    p.add_argument("--profile", required=True, help="Profile/project name")
    p.add_argument("--out", required=True, help="Output directory (project root)")
    p.add_argument("--brand-base-color", default="#2d6cdf")
    p.add_argument("--brand-accent-color", default="#f0f2f5")
    p.add_argument("--window-width", type=int, default=1200)
    p.add_argument("--window-height", type=int, default=800)
    p.add_argument("--window-maximized", nargs="?", default=None, const=True)
    p.add_argument("--layout", default="")
    p.add_argument("--panels", nargs="*", default=[])
    args = p.parse_args(argv)

    maximized = False if args.window_maximized is None else _as_bool(args.window_maximized)

    out_root = Path(args.out)
    profiles_dir = out_root / "profiles"
    qss_dir = out_root / "ui" / "qss"
    profiles_dir.mkdir(parents=True, exist_ok=True)
    qss_dir.mkdir(parents=True, exist_ok=True)

    panels = args.panels
    if len(panels) == 1 and ("," in panels[0]):
        panels = [x.strip() for x in panels[0].split(",") if x.strip()]

    payload = {
        "name": args.profile,
        "created": datetime.utcnow().isoformat() + "Z",
        "theme": {"primary": args.brand_base_color, "secondary": args.brand_accent_color},
        "window": {"width": args.window_width, "height": args.window_height, "maximized": bool(maximized)},
        "layout": args.layout,
        "panels": panels,
    }

    yaml_path = profiles_dir / f"{args.profile}.yaml"
    write_yaml(yaml_path, payload)

    qss_path = qss_dir / f"{args.profile}.qss"
    write_qss(qss_path, args.brand_base_color, args.brand_accent_color)

    # project.yaml schema + test expectations:
    # - ui.theme.base_color / accent_color
    # - ui.window.default_size: [w, h], maximized: bool
    # - ui.layout.preset: string
    # - root-level "panels": list (in addition to ui.panels for compatibility)
    project_yaml = out_root / "project.yaml"
    with open(project_yaml, "w", encoding="utf-8") as f:
        f.write(f"name: {payload['name']}\n")
        # root-level panels (the failing assertion looks here)
        if panels:
            f.write("panels:\n")
            for p in panels:
                f.write(f"  - {p}\n")
        f.write("ui:\n")
        f.write("  theme:\n")
        f.write(f"    base_color: \"{args.brand_base_color}\"\n")
        f.write(f"    accent_color: \"{args.brand_accent_color}\"\n")
        f.write("  window:\n")
        f.write(f"    default_size: [{payload['window']['width']}, {payload['window']['height']}]\n")
        f.write(f"    maximized: {str(payload['window']['maximized']).lower()}\n")
        if payload.get("layout"):
            f.write("  layout:\n")
            f.write(f"    preset: {payload['layout']}\n")
        if panels:
            f.write("  panels:\n")
            for p in panels:
                f.write(f"    - {p}\n")

    print(str(yaml_path.resolve()))
    print(str(qss_path.resolve()))
    print(str(project_yaml.resolve()))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
