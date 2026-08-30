#!/usr/bin/env python3
"""doctrinemap.py - mechanical audit of the doctrine layer (lawmap's sibling).

docs/DOCTRINE.md defines every cross-surface rule once, with a stable
`### D-id`. Rendered projections carry the text; other docs reference an
assertion as `[[D-id]]`; the mounted template consumes ids as `{{D-id}}`.
This tool asserts the layer is coherent:

  ERRORS (exit 1)
  - a duplicate id, missing targets line, or empty body in DOCTRINE.md
    (parse_doctrine raises on these)
  - a [[D-id]] or {{D-id}} reference to an id that does not exist
  - a projection surface missing its doctrine/builder-version markers

  WARNS (exit 0)
  - a defined id that is neither rendered to any target nor referenced
    anywhere (dead doctrine)

Scanned for references: docs/*.md, docs/mounted_instructions.tmpl, both
SKILL.md files. Rendered blocks are excluded from reference scanning (they
carry text, not refs). Stdlib only; run from anywhere.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, HERE)
from render_doctrine import parse_doctrine, SKILLS, PIPELINE, MARK, BMARK  # noqa: E402

REF = re.compile(r"\[\[(D-[a-z0-9-]+)\]\]|\{\{(D-[a-z0-9-]+)\}\}")


def main():
    assertions = parse_doctrine()          # raises on dupes/empty/no-targets
    ids = {a["id"] for a in assertions}
    errs, warns = [], []

    scan = [os.path.join(ROOT, "docs", f) for f in os.listdir(os.path.join(ROOT, "docs"))
            if f.endswith((".md", ".tmpl"))] + list(SKILLS.values())
    referenced = set()
    for path in scan:
        txt = open(path, encoding="utf-8").read()
        if os.path.basename(path) == "DOCTRINE.md":
            continue
        txt = MARK.sub("", txt)            # rendered blocks are not references
        for m in REF.finditer(txt):
            rid = m.group(1) or m.group(2)
            referenced.add(rid)
            if rid not in ids:
                errs.append("%s: reference to undefined %s"
                            % (os.path.relpath(path, ROOT), rid))

    for tgt, path in SKILLS.items():
        if not MARK.search(open(path, encoding="utf-8").read()):
            errs.append("%s: doctrine markers missing" % os.path.relpath(path, ROOT))
    if not BMARK.search(open(PIPELINE, encoding="utf-8").read()):
        errs.append("pipeline.md: builder-version markers missing")

    for a in assertions:
        rendered = any(t in ("mounted", "skill-build", "skill-art") for t in a["targets"])
        if not rendered and a["id"] not in referenced:
            warns.append("%s: defined but never rendered or referenced (dead)" % a["id"])

    for e in errs:
        print("error  " + e)
    for w in warns:
        print("warn   " + w)
    n_ref = len(referenced & ids)
    print("%d assertion(s), %d referenced, %d surface(s) scanned; %d error(s), %d warning(s)"
          % (len(ids), n_ref, len(scan), len(errs), len(warns)))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
