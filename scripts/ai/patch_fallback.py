#!/usr/bin/env python
import sys, pathlib
def apply_patch(patch_text: str, root: pathlib.Path):
    files = {}; new_lines = []; hdr_new = None
    lines = patch_text.splitlines(keepends=True); i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith('diff --git'):
            if hdr_new and new_lines: files[hdr_new] = ''.join(new_lines); new_lines = []
            hdr_new = None; i += 1; continue
        if line.startswith('+++ '):
            hdr_new = line.split(' ',1)[1].strip()
            if hdr_new.startswith(('a/','b/')): hdr_new = hdr_new[2:]
            i += 1; continue
        if line.startswith('@@ '):
            i += 1
            while i < len(lines) and not lines[i].startswith('diff --git'):
                new_lines.append(lines[i]); i += 1
            continue
        i += 1
    if hdr_new and new_lines: files[hdr_new] = ''.join(new_lines)
    applied = []
    for rel, hunk in files.items():
        target = root / rel; target.parent.mkdir(parents=True, exist_ok=True)
        out = []
        for hl in hunk.splitlines():
            if hl.startswith('+') and not hl.startswith('+++'): out.append(hl[1:])
            elif hl.startswith(' '): out.append(hl[1:])
        data = '\n'.join(out) + ('\n' if out and not out[-1].endswith('\n') else '')
        target.write_text(data, encoding='utf-8'); applied.append(str(target))
    return applied
def main():
    root = pathlib.Path('.').resolve()
    patch_path = root / '._ai' / 'last.patch'
    if not patch_path.exists(): print(f"No patch at {patch_path}", file=sys.stderr); return 1
    text = patch_path.read_text(encoding='utf-8'); applied = apply_patch(text, root)
    print("Applied (fallback):"); [print(f" - {p}") for p in applied]; return 0
if __name__ == "__main__": raise SystemExit(main())
