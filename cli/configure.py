from __future__ import annotations
import argparse, pathlib, sys, yaml, json
from ..core.model import load_profile, emit_project

def parse_args():
    \1    ap.add_argument("--brand-base-color", default="#2d2d2d")
    ap.add_argument("--brand-accent-color", default="#4a90e2")
    ap.add_argument("--logo", default="")
    ap.add_argument("--window-width", type=int, default=1280)
    ap.add_argument("--window-height", type=int, default=800)
    ap.add_argument("--window-maximized", type=str, default="false")
    ap.add_argument("--panels", default="ProjectExplorer,Jobs,Logs")
    ap.add_argument("--layout", default="default")
    ap.add_argument("--profile", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--dry-run", action="store_true")
    return ap.parse_args()

def main():
    args = parse_args()
    profiles_dir = pathlib.Path("profiles")
    pfile = profiles_dir / f"{args.profile}.yaml"
    if not pfile.exists():
        print(f"Profile not found: {pfile}", file=sys.stderr)
        sys.exit(2)
    prof = load_profile(pfile)
    if args.dry_run:
        print(yaml.safe_dump(prof, sort_keys=False))
        return
    out = emit_project(prof, pathlib.Path(args.out))
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()