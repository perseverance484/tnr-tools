#!/usr/bin/env python3
"""render_doctrine.py - project docs/DOCTRINE.md outward; fail CI on drift.

docs/DOCTRINE.md is the single source for every cross-surface rule. This tool
renders it into:

  1. state/mounted_instructions.txt - the project-instructions paste, from
     docs/mounted_instructions.tmpl. {{D-id}} placeholders take the
     assertion's `short:` form (body when absent). {{PAT}} stays a literal
     slot the user fills when pasting (the repo is public; the token never
     lands here). {{STAMP}} becomes a deterministic provenance line carrying
     DOCTRINE.md's git blob sha7 - no timestamp, so --check is byte-exact.
  2. Doctrine blocks in each SKILL.md, between
     `<!-- doctrine:begin ... -->` and `<!-- doctrine:end -->` markers:
     the full body of every assertion targeted at that skill, in file order.
  3. The live-builder-version line in references/pipeline.md, between
     `<!-- builder-version:begin -->` / `end` markers, read from
     builder_bundle.js - the doc can no longer lie about the version.

Usage
  python3 render_doctrine.py --write   # regenerate all projections in place
  python3 render_doctrine.py --check   # re-render to memory, diff vs disk,
                                       # exit 1 on any delta (CI gate)

Run from anywhere; paths resolve from the repo root (parent of docs/).
Stdlib only.
"""
import difflib
import hashlib
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DOCTRINE = os.path.join(ROOT, "docs", "DOCTRINE.md")
TMPL = os.path.join(ROOT, "docs", "mounted_instructions.tmpl")
MOUNTED = os.path.join(ROOT, "state", "mounted_instructions.txt")
SKILLS = {
    "skill-build": os.path.join(ROOT, "skills", "building-tnr-content", "SKILL.md"),
    "skill-art": os.path.join(ROOT, "skills", "producing-tnr-art", "SKILL.md"),
}
PIPELINE = os.path.join(ROOT, "skills", "building-tnr-content", "references", "pipeline.md")
BUNDLE = os.path.join(ROOT, "builder_bundle.js")

A_HDR = re.compile(r"^### (D-[a-z0-9-]+)\s*$")


def blob_sha7(path):
    b = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()[:7]


def parse_doctrine():
    """-> ordered list of {id, targets, short, body}; raises on malformed."""
    out, cur = [], None
    for ln in open(DOCTRINE, encoding="utf-8"):
        m = A_HDR.match(ln)
        if m:
            cur = {"id": m.group(1), "targets": [], "short": None, "body": []}
            out.append(cur)
            continue
        if cur is None:
            continue
        if ln.startswith("targets:"):
            cur["targets"] = ln.split(":", 1)[1].split()
        elif ln.startswith("short:"):
            cur["short"] = ln.split(":", 1)[1].strip()
        else:
            cur["body"].append(ln.rstrip("\n"))
    for a in out:
        a["body"] = "\n".join(a["body"]).strip()
        if not a["targets"]:
            raise SystemExit("DOCTRINE: %s has no targets line" % a["id"])
        if not a["body"]:
            raise SystemExit("DOCTRINE: %s has an empty body" % a["id"])
    ids = [a["id"] for a in out]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise SystemExit("DOCTRINE: duplicate id(s): %s" % ", ".join(sorted(dupes)))
    return out


def render_mounted(assertions, sha7):
    by_id = {a["id"]: a for a in assertions}
    stamp = ("<!-- projection of docs/DOCTRINE.md@%s - edit DOCTRINE.md and run "
             "render_doctrine.py --write; never edit this file -->" % sha7)
    txt = open(TMPL, encoding="utf-8").read()

    def sub(m):
        key = m.group(1)
        if key == "STAMP":
            return stamp
        if key == "PAT":
            return "<<<INSERT tnr-container PAT HERE WHEN PASTING>>>"
        a = by_id.get(key)
        if a is None:
            raise SystemExit("template references undefined %s" % key)
        if "mounted" not in a["targets"]:
            raise SystemExit("template uses %s but it is not targeted 'mounted'" % key)
        return a["short"] if a["short"] else a["body"]

    return re.sub(r"\{\{(STAMP|PAT|D-[a-z0-9-]+)\}\}", sub, txt)


def doctrine_block(assertions, target, sha7):
    parts = [a["body"] for a in assertions if target in a["targets"]]
    head = ("<!-- doctrine:begin @%s target=%s - RENDERED from docs/DOCTRINE.md; "
            "edit there, then render_doctrine.py --write -->" % (sha7, target))
    return head + "\n\n" + "\n\n".join(parts) + "\n\n<!-- doctrine:end -->"


MARK = re.compile(r"<!-- doctrine:begin[^>]*-->.*?<!-- doctrine:end -->", re.S)
BMARK = re.compile(r"<!-- builder-version:begin -->.*?<!-- builder-version:end -->", re.S)


def render_skill(path, assertions, target, sha7):
    txt = open(path, encoding="utf-8").read()
    if not MARK.search(txt):
        raise SystemExit("%s: doctrine markers missing" % path)
    return MARK.sub(lambda m: doctrine_block(assertions, target, sha7), txt, count=1)


def builder_version():
    head = open(BUNDLE, encoding="utf-8").read(300)
    m = re.search(r"v4\.\d+", head)
    return m.group(0) if m else "v?"


def render_pipeline():
    txt = open(PIPELINE, encoding="utf-8").read()
    if not BMARK.search(txt):
        raise SystemExit("pipeline.md: builder-version markers missing")
    block = ("<!-- builder-version:begin -->Current live builder: **%s** "
             "(generated from builder_bundle.js - do not hand-edit)"
             "<!-- builder-version:end -->" % builder_version())
    return BMARK.sub(block, txt, count=1)


def targets_of(path):
    return {"skill-build": SKILLS["skill-build"], "skill-art": SKILLS["skill-art"]}


def render_all():
    assertions = parse_doctrine()
    sha7 = blob_sha7(DOCTRINE)
    out = {MOUNTED: render_mounted(assertions, sha7)}
    for tgt, path in SKILLS.items():
        out[path] = render_skill(path, assertions, tgt, sha7)
    out[PIPELINE] = render_pipeline()
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    out = render_all()
    if mode == "--write":
        for path, txt in out.items():
            open(path, "w", encoding="utf-8").write(txt)
            print("wrote  %s" % os.path.relpath(path, ROOT))
        return 0
    drift = 0
    for path, txt in out.items():
        on_disk = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if on_disk != txt:
            drift = 1
            print("DRIFT  %s" % os.path.relpath(path, ROOT))
            for ln in list(difflib.unified_diff(
                    on_disk.splitlines(), txt.splitlines(),
                    "on-disk", "rendered", lineterm=""))[:12]:
                print("   " + ln)
        else:
            print("same   %s" % os.path.relpath(path, ROOT))
    if drift:
        print("\nprojections drift from docs/DOCTRINE.md - run --write and commit (exit 1)")
        return 1
    print("\nall projections current (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
