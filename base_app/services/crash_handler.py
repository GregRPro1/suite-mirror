
from __future__ import annotations
import pathlib, json, datetime, sys

def write_crash_marker(dir_path: pathlib.Path, exc: str="SimulatedCrash"):
    dir_path = pathlib.Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    marker = dir_path / "crash_marker.json"
    data = {"ts": datetime.datetime.utcnow().isoformat()+"Z", "exc": exc}
    marker.write_text(json.dumps(data), encoding="utf-8")
    return marker

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    args = ap.parse_args()
    proj = pathlib.Path(args.project)
    # Write marker under project/tmp or project/
    marker = write_crash_marker(proj / "tmp")
    print(str(marker))
    sys.exit(1)
