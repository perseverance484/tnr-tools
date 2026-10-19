#!/usr/bin/env python3
"""Generate five-point structural Bloodright designs from the naming-pass CSV.

Inputs (both pinned, so output is deterministic):
  - docs/design/bloodright/naming_pass/review.csv  (names and placeholder bonuses)
  - legacy tree JSON in docs/design/bloodright/trees (bloodline ID, rank, elements)

Output: docs/design/bloodright/structural/<slug>.json, one per CSV bloodline.
The CSV's "Previous name" column holds template names, not each tree's legacy names, so it is
not copied into the designs.

The legacy trees are byte-identical copies of fable/bloodright-planning-20261003 @ LEGACY_REF,
listed with their git blob ids in docs/design/bloodright/trees/SOURCE.json. The generator refuses
any copy whose blob id differs, so the branch itself is no longer needed.

  python3 scripts/bloodright_from_naming.py          # write
  python3 scripts/bloodright_from_naming.py --check  # exit 1 if any output differs
"""
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = "docs/design/bloodright/naming_pass/review.csv"
OUT_DIR = ROOT / "docs/design/bloodright/structural"
LEGACY_REF = "7c1dfdd5e3ee163b90c22694dbb2de94ede08866"
READINESS = ROOT / "forge/bloodright/collection.readiness.json"
# Rebalance overlay (RUL-2026-10-19-001): node bonuses that replace the CSV placeholders, keyed by
# design slug. Names still come from the naming-pass CSV.
BALANCE = ROOT / "docs/design/bloodright/balance/scorer_v1/trees.json"
# Drafted names for nodes whose effects the rebalance changed (keyed by slug, then node id).
NAMES = ROOT / "docs/design/bloodright/balance/scorer_v1/names.json"
CATEGORY = {1: "Foundation", 2: "Hidden Art", 3: "Advanced Art"}
# Element left unresolved for now (RUL-2026-10-17-004). "None" limits their bonuses to jutsu
# without an element; an empty list would instead apply them to every jutsu.
NO_ELEMENT_PLACEHOLDER = {"Cosmic Ascendant", "Shiroi Youso"}
NODE = re.compile(r"^p([1-4])_t([1-3])$")


def number(v):
    return int(v) if float(v).is_integer() else v


SOURCE = json.loads((ROOT / "docs/design/bloodright/trees/SOURCE.json").read_text())


def legacy(path):
    file = ROOT / path
    expected = SOURCE["files"].get(file.name) if SOURCE["source_ref"] == LEGACY_REF else None
    blob = subprocess.run(["git", "hash-object", str(file)], check=True, capture_output=True,
                          text=True).stdout.strip() if file.is_file() else None
    if not expected or blob != expected:
        raise SystemExit(f"{path}: missing or differs from its {LEGACY_REF[:7]} copy")
    return json.loads(file.read_text())


def build():
    raw = (ROOT / CSV_PATH).read_bytes()
    rows = list(csv.DictReader(raw.decode("utf-8-sig").splitlines()))
    trees = {t["bloodline"]: t for t in json.loads(READINESS.read_text())["trees"]}
    by_line = {}
    for r in rows:
        by_line.setdefault(r["Bloodline"], []).append(r)
    balance = json.loads(BALANCE.read_text()) if BALANCE.is_file() else {}
    renames = json.loads(NAMES.read_text()) if NAMES.is_file() else {}
    designs = {}
    for name, nodes in by_line.items():
        rebalanced = balance.get(slug(name), {})
        overlay = rebalanced.get("nodes") if rebalanced.get("status") == "rebalanced" else None
        t = trees.get(name)
        if not t or t["source"]["ref"] != LEGACY_REF:
            raise SystemExit(f"{name}: no legacy tree at {LEGACY_REF}")
        old = legacy(t["source"]["path"])
        if old["bloodline"]["id"] != t["bloodlineId"]:
            raise SystemExit(f"{name}: bloodline ID mismatch")
        ids = sorted(r["Node"] for r in nodes)
        if ids != sorted(f"p{p}_t{n}" for p in range(1, 5) for n in range(1, 4)):
            raise SystemExit(f"{name}: expected the 12-node four-path shape, got {ids}")
        out_nodes = []
        for r in sorted(nodes, key=lambda r: r["Node"]):
            path, tier = map(int, NODE.match(r["Node"]).groups())
            if CATEGORY[tier] != r["Tier"]:
                raise SystemExit(f"{name} {r['Node']}: tier {r['Tier']} does not match node")
            bonuses = {k: number(v) for k, v in json.loads(r["Bonuses"]).items()}
            if overlay is not None:
                bonuses = {k: number(v) for k, v in overlay[r["Node"]].items()}
            drafted = renames.get(slug(name), {}).get(r["Node"]) if overlay is not None else None
            out_nodes.append({
                "id": r["Node"], "name": drafted["name"] if drafted else r["Name"].strip(), "category": CATEGORY[tier], "tier": tier,
                "branch": f"p{path}", "cost": 1,
                "parents": [] if tier == 1 else [f"p{path}_t{tier - 1}"], "parent_rule": "ALL",
                "bonuses": bonuses,
            })
        cls = dict(old.get("classification", {}))
        if name in NO_ELEMENT_PLACEHOLDER:
            cls = {"qualifying_elements": ["None"],
                   "classification_status": "placeholder: no element until resolved (RUL-2026-10-17-004)",
                   "applies_to": "matching supported tags on jutsu without an element"}
        provenance = {
            "naming_csv": CSV_PATH,
            "naming_csv_sha256": hashlib.sha256(raw).hexdigest(),
            "legacy_tree": {"path": t["source"]["path"], "ref": LEGACY_REF},
        }
        if overlay is not None:
            drafted = renames.get(slug(name), {})
            provenance["balance"] = {"path": str(BALANCE.relative_to(ROOT)), "ruling": "RUL-2026-10-19-001",
                                     "rename_needed": [x["id"] for x in rebalanced.get("rename_needed", [])
                                                       if x["id"] not in drafted]}
            if drafted:
                provenance["drafted_names"] = {"path": str(NAMES.relative_to(ROOT)), "nodes": sorted(drafted)}
        designs[name] = {
            "title": f"{name} - " + ("rebalanced (scorer v1)" if overlay is not None else "naming pass (placeholder values)"),
            "revision": "Generated by scripts/bloodright_from_naming.py; " + (
                "names from the naming pass, bonuses from the scorer-v1 rebalance" if overlay is not None
                else "values are placeholders pending rebalance"),
            "provenance": provenance,
            "bloodline": {k: old["bloodline"][k] for k in ("id", "review_id", "name", "rank", "statClassification", "traits") if k in old["bloodline"]},
            "build_rules": {"max_bp": 5, "skill_cost": 1, "max_advanced": 2, "max_advanced_reachable": 1, "prerequisites": "ALL"},
            "classification": {
                "qualifying_elements": cls.get("qualifying_elements", []),
                "classification_status": cls.get("classification_status"),
                "applies_to": cls.get("applies_to"),
            },
            "nodes": out_nodes,
        }
    return designs


def slug(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def main():
    check = "--check" in sys.argv
    stale = []
    for name, design in build().items():
        path = OUT_DIR / f"{slug(name)}.json"
        text = json.dumps(design, indent=1, ensure_ascii=False) + "\n"
        if check:
            if not path.is_file() or path.read_text() != text:
                stale.append(str(path.relative_to(ROOT)))
        else:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    if check and stale:
        print("stale:", *stale, sep="\n  ")
        return 1
    print(f"{'checked' if check else 'wrote'} {len(build())} structural designs")
    return 0


if __name__ == "__main__":
    sys.exit(main())
