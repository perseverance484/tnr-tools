#!/usr/bin/env python3
"""Render docs/DOCTRINE.md into its checked projections."""

import difflib
import hashlib
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

ASSERTION = re.compile(r"^### (D-[a-z0-9-]+)\s*$")
MARK = re.compile(r"<!-- doctrine:begin[^>]*-->.*?<!-- doctrine:end -->", re.S)
BMARK = re.compile(r"<!-- builder-version:begin -->.*?<!-- builder-version:end -->", re.S)


def blob_sha7(path):
    data = open(path, "rb").read()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()[:7]


def parse_doctrine():
    assertions = []
    current = None
    for line in open(DOCTRINE, encoding="utf-8"):
        match = ASSERTION.match(line)
        if match:
            current = {"id": match.group(1), "targets": [], "short": None, "body": []}
            assertions.append(current)
            continue
        if current is None:
            continue
        if line.startswith("targets:"):
            current["targets"] = line.split(":", 1)[1].split()
        elif line.startswith("short:"):
            current["short"] = line.split(":", 1)[1].strip()
        else:
            current["body"].append(line.rstrip("\n"))

    seen = set()
    for assertion in assertions:
        assertion["body"] = "\n".join(assertion["body"]).strip()
        if not assertion["targets"]:
            raise SystemExit(f"DOCTRINE: {assertion['id']} has no targets line")
        if not assertion["body"]:
            raise SystemExit(f"DOCTRINE: {assertion['id']} has an empty body")
        if assertion["id"] in seen:
            raise SystemExit(f"DOCTRINE: duplicate id: {assertion['id']}")
        seen.add(assertion["id"])
    return assertions


def render_mounted(assertions, sha7):
    by_id = {assertion["id"]: assertion for assertion in assertions}
    stamp = (
        "<!-- projection of docs/DOCTRINE.md@%s + mounted_instructions.tmpl@%s"
        " - edit the sources and run render_doctrine.py --write; never edit"
        " this file -->" % (sha7, blob_sha7(TMPL))
    )
    template = open(TMPL, encoding="utf-8").read()

    def replace(match):
        key = match.group(1)
        if key == "STAMP":
            return stamp
        if key == "PAT":
            return "<<<INSERT tnr-container PAT HERE WHEN PASTING>>>"
        assertion = by_id.get(key)
        if assertion is None:
            raise SystemExit(f"template references undefined {key}")
        if "mounted" not in assertion["targets"]:
            raise SystemExit(f"template uses {key} but it is not targeted 'mounted'")
        return assertion["short"] or assertion["body"]

    return re.sub(r"\{\{(STAMP|PAT|D-[a-z0-9-]+)\}\}", replace, template)


def doctrine_block(assertions, target, sha7):
    body = "\n\n".join(a["body"] for a in assertions if target in a["targets"])
    header = (
        "<!-- doctrine:begin @%s target=%s - RENDERED from docs/DOCTRINE.md; "
        "edit there, then render_doctrine.py --write -->" % (sha7, target)
    )
    return f"{header}\n\n{body}\n\n<!-- doctrine:end -->"


def render_skill(path, assertions, target, sha7):
    text = open(path, encoding="utf-8").read()
    if not MARK.search(text):
        raise SystemExit(f"{path}: doctrine markers missing")
    block = doctrine_block(assertions, target, sha7)
    return MARK.sub(lambda _: block, text, count=1)


def builder_version():
    head = open(BUNDLE, encoding="utf-8").read(300)
    match = re.search(r"v4\.\d+", head)
    return match.group(0) if match else "v?"


def render_pipeline():
    text = open(PIPELINE, encoding="utf-8").read()
    if not BMARK.search(text):
        raise SystemExit("pipeline.md: builder-version markers missing")
    block = (
        "<!-- builder-version:begin -->Current live builder: **%s** "
        "(generated from builder_bundle.js - do not hand-edit)"
        "<!-- builder-version:end -->" % builder_version()
    )
    return BMARK.sub(lambda _: block, text, count=1)


def render_all():
    assertions = parse_doctrine()
    sha7 = blob_sha7(DOCTRINE)
    rendered = {MOUNTED: render_mounted(assertions, sha7)}
    rendered.update(
        (path, render_skill(path, assertions, target, sha7))
        for target, path in SKILLS.items()
    )
    rendered[PIPELINE] = render_pipeline()
    return rendered


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    rendered = render_all()
    if mode == "--write":
        for path, text in rendered.items():
            open(path, "w", encoding="utf-8").write(text)
            print("wrote  %s" % os.path.relpath(path, ROOT))
        return 0

    drift = False
    for path, text in rendered.items():
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if current == text:
            print("same   %s" % os.path.relpath(path, ROOT))
            continue
        drift = True
        print("DRIFT  %s" % os.path.relpath(path, ROOT))
        for line in list(
            difflib.unified_diff(
                current.splitlines(), text.splitlines(), "on-disk", "rendered", lineterm=""
            )
        )[:12]:
            print("   " + line)

    if drift:
        print("\nprojections drift from docs/DOCTRINE.md - run --write and commit (exit 1)")
        return 1
    print("\nall projections current (exit 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
