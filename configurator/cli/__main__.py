
from __future__ import annotations
import argparse
from pathlib import Path
from .configure import write_yaml, write_qss

def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="configurator.cli", description="Legacy CLI to emit profile + QSS")
    p.add_argument("--name", required=True)
    p.add_argument("--profiles-dir", required=True)
    p.add_argument("--qss-dir", required=True)
    args = p.parse_args(argv)
    profiles = Path(args.profiles_dir)
    qss_dir = Path(args.qss_dir)
    write_yaml(profiles / f"{args.name}.yaml", {
        "name": args.name,
        "created": "legacy",
        "theme": {"primary": "#2d6cdf", "secondary": "#f0f2f5"},
        "window": {"width": 1200, "height": 800, "maximized": False},
        "layout": "",
        "panels": []
    })
    write_qss(qss_dir / f"{args.name}.qss", "#2d6cdf", "#f0f2f5")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
