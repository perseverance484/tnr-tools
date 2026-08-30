#!/usr/bin/env python3
"""scrub_check.py - fail-closed secret/privacy scrub, runnable pre-push.

Mirrors the staged CI gate (state/staged_workflows/scrub.yml): FAIL-CLOSED.
An empty or missing pattern list is a failure, not a pass - on a public repo
"no patterns configured" must never read as "clean".

Usage
  python3 scrub_check.py PATTERN_FILE [ROOT]

PATTERN_FILE: one literal pattern per line (tokens, names); blank lines
ignored. Keep it OUTSIDE the repo (e.g. /tmp/scrub_patterns.txt) - the
patterns are themselves secrets and must never be committed. ROOT defaults
to the current directory; .git is skipped; files are scanned as bytes so
binaries are safe to walk.

Exit 1 on any hit OR on an empty/unreadable pattern list; exit 0 clean.
Hits print the file path only, never the matched content.
"""
import os
import sys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    pat_path = sys.argv[1]
    root = sys.argv[2] if len(sys.argv) > 2 else "."
    try:
        pats = [ln.strip().encode() for ln in open(pat_path, encoding="utf-8")
                if ln.strip()]
    except OSError as e:
        print("FAIL-CLOSED: cannot read pattern file (%s)" % e)
        return 1
    if not pats:
        print("FAIL-CLOSED: pattern list is empty - configure patterns before "
              "trusting a clean result")
        return 1
    hits, scanned = [], 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                blob = open(p, "rb").read()
            except OSError:
                continue
            scanned += 1
            if any(pat in blob for pat in pats):
                hits.append(p)
    for h in hits:
        print("HIT  %s" % h)
    print("%d file(s) scanned, %d pattern(s), %d hit(s) -> %s"
          % (scanned, len(pats), len(hits), "SCRUB FAILED" if hits else "clean"))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main())
