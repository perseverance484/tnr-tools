#!/usr/bin/env python3
"""
Build push/97: create the three crafting caches, HIDDEN (release step A, RUL-2026-10-13-001..003, D10 (b)).

This generator never contacts the game. Every value comes from committed state:

  loot tables   docs/design/crafting_caches/caches_draft.json (checked by harness/crafting_caches/check_draft.py)
  chassis       the live Common Gatherer's Chest row in push/95 results
                (harvests/inbox/tnr_results_1791863274945.json): the chest family that already sits in the
                restricted vault. Field SET = push/90's Skyglass Reliquary create (a proven chest create);
                field VALUES = the donor row. Only name, description, image, effects and hidden are set here.
  effect        the donor's own noncombatconsumereward (full editor key set, item reference H12) with
                reward_items replaced by the draft lines and the description renamed.
  text          ITEM_TEXT below. It is drafted by Fable and needs dauntless approval (D11).
  art           art/crafting_caches/<file>, committed. --final pins it as a repo-backed imagePack.

Usage, from the repository root:

    python3 push/97_crafting_caches_create.gen.py --draft [--check]
    python3 push/97_crafting_caches_create.gen.py --final --image-ref <40-hex commit> [--check]

--draft  writes the manifest without an imagePack. Forge would fall back to the manual picker for the
         three @img files. This is a review artifact.
--final  requires all three icons at --image-ref (an ancestor of HEAD). It binds them by path, sha256
         and bytes, and writes imgSizes.
--check  rebuilds in memory and fails if the committed push/97 JSON differs.

Both modes run validate.py the doctrine way (from the skill data/ directory) and
forge/tools/check_manifest.mjs. Every validate.py line must fall in a known-stale class (CLASSES).
Forge must pass in --final; in --draft it may refuse only for the unbound icons. Running the final
manifest needs dauntless's release-specific validate.py exception (decision D12), as push/90 did.
Push B (unhide + quest edits) is a separate manifest.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "push", "97_crafting_caches_create.json")
DRAFT = os.path.join(ROOT, "docs", "design", "crafting_caches", "caches_draft.json")
P95 = os.path.join(ROOT, "harvests", "inbox", "tnr_results_1791863274945.json")
P90 = os.path.join(ROOT, "push", "90_ghost_ship_skyglass_release.json")
DONOR_NAME = "Common Gatherer's Chest"
DONOR_ID = "gb6vxdzWTYZR--7s-4kTX"
ART_DIR = "art/crafting_caches"

# Icon filenames are fixed by docs/handoffs/CRAFTING_CACHES_IMAGE_GEN_HANDOFF.md.
ITEM_TEXT = {
    "pills": {
        "srcId": "crafting_cache_medicine_inro",
        "image": "icon-medicine-inro.webp",
        "description": "A lacquered medicine case from the Ghost Ship's restricted vault. Its tiers are packed "
                       "with the herbs and beast parts every field pill is made from.",
    },
    "kunai": {
        "srcId": "crafting_cache_shinobi_tool_pouch",
        "image": "icon-shinobi-tool-pouch.webp",
        "description": "A buckled hip pouch from the Ghost Ship's restricted vault, heavy with iron and the "
                       "reagents a kunai smith works with.",
    },
    "high_tier": {
        "srcId": "crafting_cache_sages_strongbox",
        "image": "icon-sages-strongbox.webp",
        "description": "A sealed strongbox from the Ghost Ship's restricted vault. Behind its paper seals lie "
                       "the rare reagents of the most potent pills and forbidden scrolls.",
    },
}
DROP_FROM_DONOR = {"id", "createdAt", "updatedAt", "name", "description", "image", "effects", "hidden"}


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", ROOT, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def donor_row() -> dict:
    bundle = json.load(open(P95, encoding="utf-8"))
    rows = [c["data"] for c in bundle["captures"]
            if c.get("proc") == "item.get" and isinstance(c.get("data"), dict) and c["data"].get("id") == DONOR_ID]
    if len(rows) != 1 or rows[0].get("name") != DONOR_NAME:
        sys.exit(f"refusing: push/95 does not hold exactly one {DONOR_NAME} row ({DONOR_ID})")
    return rows[0]


def proven_field_set() -> list[str]:
    m = json.load(open(P90, encoding="utf-8"))
    rel = [it for it in m["items"] if it.get("entity") == "item" and it.get("srcId") == "skyglass_reliquary"]
    if len(rel) != 1:
        sys.exit("refusing: push/90 Skyglass Reliquary create not found")
    return list(rel[0]["data"].keys())


def build_items(draft: dict, donor: dict) -> list[dict]:
    fields = proven_field_set()
    missing = [k for k in fields if k not in DROP_FROM_DONOR and k not in donor]
    if missing:
        sys.exit(f"refusing: donor row lacks proven create fields {missing}")
    effects = [e for e in donor["effects"] if e.get("type") == "noncombatconsumereward"]
    if len(donor["effects"]) != 1 or len(effects) != 1:
        sys.exit("refusing: donor must carry exactly one noncombatconsumereward effect")
    allowed = set((draft.get("quantity_policy") or {}).get("allowed") or [])
    items = []
    for cache in draft["caches"]:
        text = ITEM_TEXT[cache["key"]]
        eff = copy.deepcopy(effects[0])
        eff["description"] = f"{cache['name']} loot table"
        eff["reward_items"] = []
        for ln in cache["lines"]:
            if allowed and ln["quantity"] not in allowed:
                sys.exit(f"refusing: {cache['name']} line {ln['name']} quantity {ln['quantity']} not in {sorted(allowed)}")
            eff["reward_items"].append({"ids": [ln["id"]], "number": ln["chance"], "quantity": ln["quantity"]})
        data = {}
        for k in fields:
            if k == "name":
                data[k] = cache["name"]
            elif k == "description":
                data[k] = text["description"]
            elif k == "image":
                data[k] = f"@img:{text['image']}"
            elif k == "hidden":
                data[k] = True
            else:
                data[k] = copy.deepcopy(donor[k])
        data["effects"] = [eff]
        items.append({"entity": "item", "slot": "create", "phase": 1, "name": cache["name"],
                      "srcId": text["srcId"], "data": data})
    return items


def image_pack(image_ref: str) -> tuple[dict, dict]:
    if not re.fullmatch(r"[0-9a-f]{40}", image_ref or ""):
        sys.exit("refusing: --image-ref must be a 40-hex commit")
    if git("merge-base", "--is-ancestor", image_ref, "HEAD").returncode != 0:
        sys.exit(f"refusing: {image_ref} is not an ancestor of HEAD")
    files, sizes = {}, {}
    for t in ITEM_TEXT.values():
        path = f"{ART_DIR}/{t['image']}"
        blob = subprocess.run(["git", "-C", ROOT, "show", f"{image_ref}:{path}"], stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, check=False)
        if blob.returncode != 0:
            sys.exit(f"refusing: {path} is not in commit {image_ref}")
        data = blob.stdout
        if not data.startswith(b"RIFF") or data[8:12] != b"WEBP":
            sys.exit(f"refusing: {path} is not a WebP file")
        if len(data) > 460800:
            sys.exit(f"refusing: {path} is {len(data)} bytes, over the 460,800-byte working ceiling")
        files[t["image"]] = {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        sizes[t["image"]] = len(data)
    return {"ref": image_ref, "files": files}, sizes


# validate.py's generated contracts lag the pinned engine (RUL-2026-10-12-013; contract adoption is an
# open Lane A follow-up). These are the only diagnostic classes push/97 may produce. Any other line refuses.
# The exception itself is dauntless's to rule for this manifest (decision D12); this gate only proves
# that nothing outside the known-stale classes is present.
CLASSES = {
    "stale_effect_field": re.compile(r"^ERROR\s+\[item:[^\]]+\]\.effects\[0\]: noncombatconsumereward: unknown field "
                                     r"'(reward_[a-z_]+|description|direction)'\."),
    "stale_farm_nullability": re.compile(r"^warn\s+\[item:[^\]]+\]: law 72: '(farmYieldItemId|farmExtractSeedItemId)' is null"),
    "draft_unbound_art": re.compile(r"^ERROR\s+manifest: @img:icon-[a-z-]+\.webp has no imgSizes entry"),
}


def gates(path: str, final: bool) -> dict:
    data_dir = os.path.join(ROOT, "skills/building-tnr-content/data")
    v = subprocess.run([sys.executable, "../scripts/validate.py", os.path.abspath(path)], cwd=data_dir,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    counts, unknown = {}, []
    for line in v.stdout.splitlines():
        line = line.strip()
        if not re.match(r"^(ERROR|warn)\b", line):
            continue
        cls = next((k for k, rx in CLASSES.items() if rx.match(line)), None)
        if cls is None or (final and cls == "draft_unbound_art"):
            unknown.append(line)
        else:
            counts[cls] = counts.get(cls, 0) + 1
    if unknown:
        sys.exit("validate.py produced diagnostics outside the known-stale classes:\n" + "\n".join(unknown))
    f = subprocess.run(["node", os.path.join(ROOT, "forge/tools/check_manifest.mjs"), path],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if f.returncode != 0:
        problems = [l for l in f.stdout.splitlines() if l.startswith("L") or "imgSizes" in l]
        art_only = all(re.match(r"^L17 @img:icon-[a-z-]+\.webp has no imgSizes byte entry$", l) for l in problems)
        if final or not problems or not art_only:
            sys.exit("forge check_manifest failed:\n" + f.stdout)
        counts["forge_draft_unbound_art"] = len(problems)
    return counts


def build(final: bool, image_ref: str | None) -> dict:
    check = subprocess.run([sys.executable, os.path.join(ROOT, "harness/crafting_caches/check_draft.py"), "--check"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if check.returncode != 0:
        sys.exit("refusing: the cache draft fails check_draft.py --check:\n" + check.stdout)
    draft = json.load(open(DRAFT, encoding="utf-8"))
    items = build_items(draft, donor_row())
    note = ("Crafting caches release step A (RUL-2026-10-13-001..003, D10 (b)). Creates Medicine Inro, Shinobi Tool "
            "Pouch and Sage's Strongbox HIDDEN, with loot tables from docs/design/crafting_caches/caches_draft.json "
            "and the chassis of the live Common Gatherer's Chest (push/95). dedupNames refuses any live name "
            "collision before a write. Forge reads every created item back. No quest is touched: step B "
            "(unhide + restricted-vault lines in both Ghost Ship quests) is a separate manifest. "
            "Generated by push/97_crafting_caches_create.gen.py; do not hand-edit.")
    manifest = {"_note": note + ("" if final else " DRAFT: no imagePack; icons are not yet committed."),
                "dedupNames": True}
    if final:
        pack, sizes = image_pack(image_ref)
        manifest["imgSizes"] = sizes
        manifest["imagePack"] = pack
    manifest["items"] = items
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--draft", action="store_true")
    mode.add_argument("--final", action="store_true")
    ap.add_argument("--image-ref")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if a.final and not a.image_ref:
        ap.error("--final needs --image-ref")
    manifest = build(a.final, a.image_ref)
    text = json.dumps(manifest, indent=1, ensure_ascii=False) + "\n"
    if a.check:
        cur = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else None
        if cur != text:
            print(f"{OUT} is stale; rerun without --check", file=sys.stderr)
            return 1
        counts = gates(OUT, a.final)
        print(f"{os.path.relpath(OUT, ROOT)} current; gates: {counts}")
        return 0
    tmp = OUT + ".tmp.json"
    open(tmp, "w", encoding="utf-8").write(text)
    try:
        counts = gates(tmp, a.final)
    except SystemExit:
        os.remove(tmp)
        raise
    os.replace(tmp, OUT)
    print(f"wrote {os.path.relpath(OUT, ROOT)} ({'final' if a.final else 'draft'}): "
          f"{len(manifest['items'])} hidden item creates, dedupNames on; gates: {counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
