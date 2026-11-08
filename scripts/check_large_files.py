#!/usr/bin/env python3
"""Refuse new large files: every tracked file over LIMIT must be on the allowlist.

    python3 scripts/check_large_files.py            check (exit 1 on a new large file)
    python3 scripts/check_large_files.py --write    rewrite the allowlist from what is tracked now

The repository's checkout is about 1 GB and its history about 1 GB, mostly preview GIFs and raw
art. The files already over the limit are grandfathered in .github/large-files-allowlist.txt (path
and size); a new file over the limit, or a grandfathered one that grew, fails. Keep previews and
raws small (a shortened GIF, a contact sheet, a webp), or attach them to the review rather than
committing them. Raising the limit or adding to the allowlist is a director decision.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMIT = 5 * 1024 * 1024
ALLOW = os.path.join(ROOT, ".github", "large-files-allowlist.txt")


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True).stdout
    for rel in out.decode("utf-8").split("\0"):
        if rel:
            p = os.path.join(ROOT, rel)
            if os.path.isfile(p):
                yield rel, os.path.getsize(p)


def main():
    big = sorted(((r, s) for r, s in tracked() if s > LIMIT), key=lambda x: -x[1])
    if "--write" in sys.argv:
        with open(ALLOW, "w", encoding="utf-8") as fh:
            fh.write(f"# Files over {LIMIT // 1048576} MB grandfathered on 2026-11-08 (scripts/check_large_files.py). "
                     "path<TAB>bytes. Adding a line is a director decision.\n")
            fh.writelines(f"{r}\t{s}\n" for r, s in big)
        print(f"check_large_files: wrote {len(big)} grandfathered file(s)")
        return 0
    allowed = {}
    for line in open(ALLOW, encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            r, s = line.rstrip("\n").split("\t")
            allowed[r] = int(s)
    bad = [(r, s) for r, s in big if r not in allowed or s > allowed[r]]
    for r, s in bad:
        why = "grew past its grandfathered size" if r in allowed else f"is over {LIMIT // 1048576} MB"
        print(f"check_large_files: {r} ({s / 1048576:.1f} MB) {why}")
    print(f"check_large_files: {len(big)} file(s) over the limit, {len(bad)} not allowed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
