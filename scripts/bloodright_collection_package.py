#!/usr/bin/env python3
"""Build the naming-pass Bloodright collection packages for Forge.

Splits the structural designs into two collections:
  A - trees whose bonuses use only the original ten potency tags;
  B - trees that use the seven tags added upstream at TheNinjaRPG 133e2c7
      (needs the re-pinned Forge contract, and a live game running that code).
Trees with unresolved or director-review qualifying elements are left out and listed.

Icons are expected at art/bloodright/<slug>/{foundation,hidden_art,advanced_art}.webp.
With --icons-ref <commit>, every icon is bound to an immutable imagePack at that commit.
Without it, or with any icon missing, the package is written as a BLOCKED template.

  python3 scripts/bloodright_collection_package.py [--icons-ref SHA] [--check]
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESIGNS = "docs/design/bloodright/structural"
OUT = {"a": ROOT / "forge/bloodright/naming_pass_collection_a.json",
       "b": ROOT / "forge/bloodright/naming_pass_collection_b.json"}
ORIGINAL_TAGS = {"damage", "increasedamagegiven", "decreasedamagegiven", "increasedamagetaken",
                 "decreasedamagetaken", "afterburn", "lifesteal", "reflect", "increaseheal", "heal"}
# BEE's live folder and Hungry Pulse (RUL-2026-10-08-002, RUL-2026-10-17-002).
HUNGRY_PULSE = "HWq7986PPhl5emkAM3L4a"
BEE = {"bloodline": "ovZIWu28ANn-Cij5TjT8S", "folder": "kvxMu9ntHbNcD6FFHKGo3", "nodes": {"p2_t1": HUNGRY_PULSE}}
SILVER, ROUNDS = 20, 99  # placeholders for every node (see docs/RULINGS.md)
ICONS = {"Foundation": "foundation", "Hidden Art": "hidden_art", "Advanced Art": "advanced_art"}


def git(*args, binary=False):
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True,
                          text=not binary).stdout


# The exact commit the packages pin. Update it (and rerun) whenever the designs change.
# Explicit rather than derived from history, so squash/rebase merges and shallow clones
# cannot silently move it; design_ref() proves the working tree still matches it.
DESIGN_REF = "6d97f2eea4bc64992f316d221060cc2896cd9e01"


def design_ref():
    if git("status", "--porcelain", "--", DESIGNS).strip():
        raise SystemExit(f"{DESIGNS} has uncommitted changes; commit them first")
    try:
        same = not git("diff", "--name-only", DESIGN_REF, "--", DESIGNS).strip()
    except subprocess.CalledProcessError:
        raise SystemExit(f"DESIGN_REF {DESIGN_REF} is not available in this clone")
    if not same:
        raise SystemExit(f"{DESIGNS} differs from DESIGN_REF {DESIGN_REF}; update DESIGN_REF")
    return DESIGN_REF


def blob(ref, path):
    try:
        return git("show", f"{ref}:{path}", binary=True)
    except subprocess.CalledProcessError:
        return None


def build(icons_ref):
    ref = design_ref()
    packages = {"a": [], "b": []}
    skipped, missing, files, sizes = [], [], {"a": {}, "b": {}}, {"a": {}, "b": {}}
    for path in sorted((ROOT / DESIGNS).glob("*.json")):
        slug, design = path.stem, json.loads(blob(ref, f"{DESIGNS}/{path.name}"))
        cls = design["classification"]
        if not cls["qualifying_elements"]:
            skipped.append(f"{design['bloodline']['name']}: no qualifying element")
            continue
        if "director review" in (cls.get("classification_status") or ""):
            # User-owned until confirmed (CLAUDE.md section 10); never imported on a guess.
            skipped.append(f"{design['bloodline']['name']}: elements {'+'.join(cls['qualifying_elements'])} await director review")
            continue
        tags = {t for n in design["nodes"] for t in n["bonuses"]}
        group = "a" if tags <= ORIGINAL_TAGS else "b"
        bee = design["bloodline"]["id"] == BEE["bloodline"]
        tree = {
            "version": 1,
            "source": {"path": f"{DESIGNS}/{path.name}", "ref": ref},
            "hiddenProbeId": HUNGRY_PULSE,
            "bindings": {"folderId": BEE["folder"], "nodes": BEE["nodes"]} if bee else {},
            **({} if bee else {"folder": {"name": design["bloodline"]["name"]}}),
            "nodes": {n["id"]: {"seichiSilverCost": SILVER, "rounds": ROUNDS} for n in design["nodes"]},
            "icons": {},
        }
        for category, stem in ICONS.items():
            name = f"bloodright_{slug}_{stem}.webp"
            tree["icons"][category] = f"@img:{name}"
            art = f"art/bloodright/{slug}/{stem}.webp"
            data = blob(icons_ref, art) if icons_ref else None
            if data is None:
                missing.append(art)
                continue
            files[group][name] = {"path": art, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
            sizes[group][name] = len(data)
        packages[group].append(tree)
    out = {}
    for group, trees in packages.items():
        blocked = [m for m in missing if any(m.startswith(f"art/bloodright/{Path(t['source']['path']).stem}/") for t in trees)]
        note = ("BLOCKED TEMPLATE: icons missing (" + ", ".join(blocked) + "). Do not stage in push/ yet."
                if blocked else f"Naming-pass collection {group.upper()}: {len(trees)} trees, scorer-v1 rebalance values (RUL-2026-10-19-001); Shiroi Youso keeps its placeholder.")
        out[group] = {
            "_note": note,
            "_skipped": skipped,
            "bloodrightCollection": {"version": 1, "trees": trees},
            **({"imagePack": {"ref": icons_ref, "files": files[group]}, "imgSizes": sizes[group]} if not blocked else {}),
        }
    return out


def main():
    args = sys.argv[1:]
    icons_ref = args[args.index("--icons-ref") + 1] if "--icons-ref" in args else None
    if icons_ref and not re.fullmatch(r"[0-9a-f]{40}", icons_ref):
        raise SystemExit("--icons-ref must be a 40-hex commit")
    stale = []
    for group, package in build(icons_ref).items():
        text = json.dumps(package, indent=1, ensure_ascii=False) + "\n"
        if "--check" in args:
            if not OUT[group].is_file() or OUT[group].read_text() != text:
                stale.append(OUT[group].name)
        else:
            OUT[group].write_text(text)
        print(f"{group.upper()}: {len(package['bloodrightCollection']['trees'])} trees - {package['_note'][:90]}")
    if stale:
        print("stale:", *stale)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
