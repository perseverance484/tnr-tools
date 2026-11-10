#!/usr/bin/env python3
"""Build section TOCs and per-task reference packs."""

import difflib
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
# One row per skill that has section TOCs. A skill gets packs only if it has packs/PACKS.json.
# Add a skill here; never build its TOCs or packs by another route.
SKILL_TOCS = {
    "building-tnr-content": ["jutsu.md", "ai.md", "quest.md", "pipeline.md", "item.md"],
    "designing-tnr-content": ["sheet.md", "writing.md"],
}
HEADING = re.compile(r"^(#{2,3}) (.+)$", re.M)


def blob7(data):
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()[:7]


def toc_of(path):
    data = open(path, "rb").read()
    text = data.decode("utf-8")
    headings = [
        (match.start(), len(match.group(1)), match.group(2).strip())
        for match in HEADING.finditer(text)
    ]
    sections = []
    for index, (start, level, title) in enumerate(headings):
        end = headings[index + 1][0] if index + 1 < len(headings) else len(text)
        sections.append(
            {
                "level": level,
                "title": title,
                "start": len(text[:start].encode()),
                "end": len(text[:end].encode()),
            }
        )
    return {
        "file": os.path.relpath(path, ROOT),
        "sha7": blob7(data),
        "sections": sections,
    }, text


def render():
    rendered = {}
    for skill_name, toc_files in SKILL_TOCS.items():
        rendered.update(render_skill(os.path.join(ROOT, "skills", skill_name), toc_files))
    return rendered


def render_skill(skill, toc_files):
    refs = os.path.join(skill, "references")
    toc_dir = os.path.join(refs, "_toc")
    pack_dir = os.path.join(skill, "packs")
    packs_json = os.path.join(pack_dir, "PACKS.json")
    os.makedirs(toc_dir, exist_ok=True)
    rendered, texts, tocs = {}, {}, {}
    for filename in toc_files:
        path = os.path.join(refs, filename)
        toc, text = toc_of(path)
        texts[filename] = text
        tocs[filename] = toc
        rendered[os.path.join(toc_dir, filename.replace(".md", ".json"))] = (
            json.dumps(toc, indent=1) + "\n"
        )

    if not os.path.exists(packs_json):
        return rendered
    packs = json.load(open(packs_json))
    for name, spec in packs.items():
        parts, sources = [], []
        for source in spec["sources"]:
            filename = os.path.basename(source["file"])
            text = texts[filename]
            toc = tocs[filename]
            for prefix in source["sections"]:
                matches = [section for section in toc["sections"] if section["title"].startswith(prefix)]
                if not matches:
                    raise SystemExit(
                        "PACKS.json: pack '%s' wants '%s' in %s - no such heading"
                        % (name, prefix, filename)
                    )
                section = matches[0]
                body = text.encode()[section["start"]:section["end"]].decode()
                parts.append(
                    "<!-- pack-trace: %s @%s '%s' -->\n%s"
                    % (filename, toc["sha7"], section["title"], body.rstrip())
                )
            sources.append("%s@%s" % (filename, toc["sha7"]))

        header = (
            "<!-- RENDERED pack '%s' from %s via build_packs.py - edit the "
            "sources, never this file -->\n# Pack: %s\n\n%s\n\n"
            % (name, " + ".join(sources), name, spec.get("note", ""))
        )
        rendered[os.path.join(pack_dir, name + ".md")] = (
            header + "\n\n---\n\n".join(parts) + "\n"
        )
    return rendered


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    rendered = render()

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
            difflib.unified_diff(current.splitlines(), text.splitlines(), lineterm="")
        )[:8]:
            print("   " + line)

    if drift:
        print("\npacks/TOCs drift from their sources - run --write (exit 1)")
        return 1
    print("\nall packs and TOCs current (exit 0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
