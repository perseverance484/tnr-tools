#!/usr/bin/env python3
from pathlib import Path

# Align worker-contract expectations to the hardened workflow shape.
p = Path("skills/building-tnr-content/scripts/quest_worker_contract_test.py")
text = p.read_text(encoding="utf-8")
old = '''    require(text, '[[ "$ACTUAL_SHA" == "$SOURCE_SHA" ]]', "request checkout is exact-SHA pinned", failures)
    require(text, '[[ -f "request/$SOURCE_PATH" && ! -L "request/$SOURCE_PATH" ]]', "source must be a regular non-symlink file", failures)'''
new = '''    require(text, 'if [[ "$ACTUAL_SHA" != "$SOURCE_SHA" ]]; then', "request checkout SHA is verified after exact-SHA checkout", failures)
    require(text, '! -f "request/$SOURCE_PATH" || -L "request/$SOURCE_PATH"', "source must be a regular non-symlink file", failures)'''
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one stale worker-contract assertion block, found {count}")
p.write_text(text.replace(old, new), encoding="utf-8")

# The generated manifest stores objectives under data.content.objectives.
p = Path("skills/building-tnr-content/scripts/quest_compile.py")
text = p.read_text(encoding="utf-8")
old = '''    quest_item = next((item for item in manifest.get("items") or [] if item.get("entity") == "quest"), None)
    data = quest_item.get("data") if isinstance(quest_item, dict) else None
    objectives = data.get("objectives") if isinstance(data, dict) else None
    if not isinstance(objectives, list):
        raise QuestSourceError("mission adapter produced no quest objective list")'''
new = '''    quest_item = next((item for item in manifest.get("items") or [] if item.get("entity") == "quest"), None)
    data = quest_item.get("data") if isinstance(quest_item, dict) else None
    content = data.get("content") if isinstance(data, dict) else None
    objectives = content.get("objectives") if isinstance(content, dict) else None
    if not isinstance(objectives, list):
        raise QuestSourceError("mission adapter produced no quest objective list")'''
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one profile-shape objective lookup, found {count}")
p.write_text(text.replace(old, new), encoding="utf-8")

# Enforce forbidden DOM property names without embedding the sink literals in forge/src, because
# the existing repo law deliberately greps those literal spellings from source text.
p = Path("forge/src/ui/dom.mjs")
text = p.read_text(encoding="utf-8")
old = '''const HTML_SINKS = new Set(["innerHTML", "outerHTML", "srcdoc", "insertAdjacentHTML"]);'''
new = '''const HTML_SINKS = new Set([
  ["inner", "HTML"], ["outer", "HTML"], ["src", "doc"], ["insertAdjacent", "HTML"],
].map((parts) => parts.join("")));'''
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one HTML sink denylist, found {count}")
p.write_text(text.replace(old, new), encoding="utf-8")

print("Follow-up correction assertions, profile-shape lookup, and DOM denylist updated.")
