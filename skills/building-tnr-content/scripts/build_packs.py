#!/usr/bin/env python3
"""build_packs.py - section TOCs + per-build-type task packs (WO-09).

The heavy references (ai.md 68K, quest.md 64K, pipeline.md 48K) price accuracy
against tokens: a jutsu build should not pay for the whole quest engine. Two
artifacts fix that:

  TOC sidecars   references/_toc/<name>.json - every ##/### heading with its
                 byte range, so a session can fetch-then-slice one section
                 instead of reading a file whole.
  Task packs     packs/<type>.md - the minimal excerpt set for one build
                 type, defined in packs/PACKS.json as (file, section-title-
                 prefix) pairs and concatenated verbatim with a per-section
                 trace line. Deterministic: the stamp carries source blob
                 sha7s, no timestamps, so --check is byte-exact.

Usage
  python3 build_packs.py --write     # regenerate TOCs + packs in place
  python3 build_packs.py --check     # re-render to memory, exit 1 on drift
                                     # or on a PACKS.json prefix that no
                                     # longer matches a heading

Reading order for a build: SKILL doctrine block, then packs/<type>.md, then
data files. A pack section going stale is impossible - it IS the reference
bytes; a reference edit changes the sha and --check forces a re-render.
Stdlib only; paths resolve from the repo root.
"""
import difflib
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SKILL = os.path.join(ROOT, "skills", "building-tnr-content")
REFS = os.path.join(SKILL, "references")
TOC_DIR = os.path.join(REFS, "_toc")
PACK_DIR = os.path.join(SKILL, "packs")
PACKS_JSON = os.path.join(PACK_DIR, "PACKS.json")
TOC_FILES = ["jutsu.md", "ai.md", "quest.md", "pipeline.md", "item.md"]
HEAD = re.compile(r"^(#{2,3}) (.+)$", re.M)


def blob7(b):
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()[:7]


def toc_of(path):
    b = open(path, "rb").read()
    txt = b.decode("utf-8")
    heads = [(m.start(), len(m.group(1)), m.group(2).strip())
             for m in HEAD.finditer(txt)]
    out = []
    for i, (start, lvl, title) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(txt)
        out.append({"level": lvl, "title": title,
                    "start": len(txt[:start].encode()), 
                    "end": len(txt[:end].encode())})
    return {"file": os.path.relpath(path, ROOT), "sha7": blob7(b),
            "sections": out}, txt


def render():
    """-> {path: content} for every TOC and pack; raises on a broken prefix."""
    out, texts, shas = {}, {}, {}
    for fn in TOC_FILES:
        p = os.path.join(REFS, fn)
        toc, txt = toc_of(p)
        texts[fn], shas[fn] = txt, toc["sha7"]
        out[os.path.join(TOC_DIR, fn.replace(".md", ".json"))] = \
            json.dumps(toc, indent=1) + "\n"
    packs = json.load(open(PACKS_JSON))
    for name, spec in packs.items():
        parts, srcs = [], []
        for src in spec["sources"]:
            fn = os.path.basename(src["file"])
            txt = texts[fn]
            toc, _ = toc_of(os.path.join(REFS, fn))
            for prefix in src["sections"]:
                hit = [s for s in toc["sections"]
                       if s["title"].startswith(prefix)]
                if not hit:
                    raise SystemExit("PACKS.json: pack '%s' wants '%s' in %s "
                                     "- no such heading" % (name, prefix, fn))
                s = hit[0]
                body = txt.encode()[s["start"]:s["end"]].decode()
                parts.append("<!-- pack-trace: %s @%s '%s' -->\n%s"
                             % (fn, shas[fn], s["title"], body.rstrip()))
            srcs.append("%s@%s" % (fn, shas[fn]))
        head = ("<!-- RENDERED pack '%s' from %s via build_packs.py - edit the "
                "sources, never this file -->\n# Pack: %s\n\n%s\n\n"
                % (name, " + ".join(srcs), name, spec.get("note", "")))
        out[os.path.join(PACK_DIR, name + ".md")] = \
            head + "\n\n---\n\n".join(parts) + "\n"
    return out


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    for d in (TOC_DIR, PACK_DIR):
        os.makedirs(d, exist_ok=True)
    out = render()
    if mode == "--write":
        for path, txt in out.items():
            open(path, "w", encoding="utf-8").write(txt)
            print("wrote  %s" % os.path.relpath(path, ROOT))
        return 0
    drift = 0
    for path, txt in out.items():
        cur = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if cur != txt:
            drift = 1
            print("DRIFT  %s" % os.path.relpath(path, ROOT))
            for ln in list(difflib.unified_diff(cur.splitlines(),
                                                txt.splitlines(),
                                                lineterm=""))[:8]:
                print("   " + ln)
        else:
            print("same   %s" % os.path.relpath(path, ROOT))
    if drift:
        print("\npacks/TOCs drift from their sources - run --write (exit 1)")
        return 1
    print("\nall packs and TOCs current (exit 0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
