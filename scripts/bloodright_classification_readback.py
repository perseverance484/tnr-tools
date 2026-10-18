#!/usr/bin/env python3
"""Compare post-edit profile.getAi read-backs with the push/109-110 before-image (RUL-2026-10-18-003).

The classification batches unequip, edit and re-equip kit jutsu on live AIs (laws 18, 60). Forge
verifies only the keys a manifest asserts, so this checks the rest: every scalar column, the
equipped kit (per jutsu: present, level, experience, equipped) and the item list (itemId,
quantity, dropChancePerc). It also reports each kit jutsu's elementClassification as now read.

  python3 scripts/bloodright_classification_readback.py harvests/inbox/tnr_results_<after>.json [...]

Exit 1 when any AI differs from its before-image in anything but the expected fields.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEFORE = ["harvests/inbox/tnr_results_1792352813119.json", "harvests/inbox/tnr_results_1792352829484.json"]
# Columns that legitimately move on any write or with time.
VOLATILE = {"updatedAt", "regenAt", "curHealth", "curChakra", "curStamina", "curEnergy"}


def ais(paths):
    out = {}
    for f in paths:
        for c in json.loads(Path(f).read_text())["captures"]:
            if c.get("proc") == "profile.getAi" and c.get("ok") and c.get("persistOk"):
                out[c["data"]["userId"]] = c["data"]
    return out


def kit(a):
    return {r["jutsuId"]: (r.get("level"), r.get("experience"), r.get("equipped")) for r in a.get("jutsus") or []}


def items(a):
    return sorted((r.get("itemId"), r.get("quantity"), r.get("dropChancePerc")) for r in a.get("items") or [])


def compare(before, after):
    problems = []
    for k in sorted(set(before) | set(after)):
        if k in VOLATILE or k in ("jutsus", "items"):
            continue
        if before.get(k) != after.get(k):
            problems.append(f"{k}: {json.dumps(before.get(k))[:80]} -> {json.dumps(after.get(k))[:80]}")
    kb, ka = kit(before), kit(after)
    for j in sorted(set(kb) | set(ka)):
        if kb.get(j) != ka.get(j):
            problems.append(f"jutsu {j}: {kb.get(j)} -> {ka.get(j)}")
    if items(before) != items(after):
        problems.append(f"items: {items(before)} -> {items(after)}")
    return problems


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    before = ais(ROOT / f for f in BEFORE)
    after = ais(argv)
    bad = 0
    for u, a in sorted(after.items(), key=lambda kv: kv[1]["username"].lower()):
        if u not in before:
            print(f"?  {a['username']} ({u}): no before-image")
            bad += 1
            continue
        problems = compare(before[u], a)
        classes = sorted({(r["jutsu"]["name"], r["jutsu"].get("elementClassification")) for r in a.get("jutsus") or []
                          if r.get("jutsu") and r["jutsu"].get("elementClassification") not in (None, "None")})
        mark = "ok" if not problems else "DIFF"
        print(f"{mark:4} {a['username']} ({u}): {len(a.get('jutsus') or [])} jutsu, classified {classes}")
        for p in problems:
            print("       " + p)
        bad += bool(problems)
    print(f"{len(after)} AI(s) read back, {bad} with differences")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
