
from __future__ import annotations
import pathlib, json, zipfile, datetime, yaml, sys

def _project_dir_and_config(project_path: pathlib.Path):
    p = pathlib.Path(project_path)
    if p.is_dir():
        y = p / "project.yaml"
    else:
        y = p
        p = p.parent
    cfg = yaml.safe_load(y.read_text(encoding="utf-8"))
    return p, cfg

def submit_ticket(project: pathlib.Path, title: str, description: str, kind: str="bug") -> pathlib.Path:
    proj_dir, cfg = _project_dir_and_config(project)
    sinks = (cfg.get("feedback") or {}).get("sinks") or []
    target = None
    for s in sinks:
        if s.get("kind")=="fileshare":
            target = s.get("config",{}).get("path","./inbox")
            break
    if target is None:
        target = "./inbox"
    inbox = (proj_dir / target).resolve()
    inbox.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    bundle = inbox / f"ticket_{ts}.zip"
    ticket = {"type": kind, "title": title, "description": description, "app": {"name":"SuiteBaseApp"}}
    with zipfile.ZipFile(bundle, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("ticket.json", json.dumps(ticket, indent=2))
    return bundle

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--desc", default="")
    ap.add_argument("--type", default="bug")
    args = ap.parse_args()
    b = submit_ticket(pathlib.Path(args.project), args.title, args.desc, args.type)
    print(str(b))
    sys.exit(0)
