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
VOLATILE = {"updatedAt", "regenAt", "curHealth", "curChakra", "curStamina", "curEnergy",
            "unreadNews", "unreadNotifications", "inboxNews"}
# Effect-tag keys the pinned validators no longer define are stripped by the server on any save
# (e.g. lifesteal statTypes, removed upstream; the engine no longer reads it: tags.ts
# getEfficiencyRatio limits damage-derived tags by generalTypes only). Compare effects on the keys
# allowed at the pin, from forge/src/runner/nested.json, and report what was dropped separately.
_NESTED = json.loads((ROOT / "forge/src/runner/nested.json").read_text())
ALLOWED = {t: set(_NESTED["sets"][i]) for t, i in _NESTED["effects"].items()}


def pinned(effects):
    out, dropped = [], []
    for e in effects or []:
        keep = ALLOWED.get(e.get("type"))
        if keep is None:
            out.append(e)
            continue
        out.append({k: v for k, v in e.items() if k in keep})
        dropped += [f"{e.get('type')}.{k}" for k in e if k not in keep]
    return out, dropped


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
        if k == "effects":
            (eb, gone), (ea, _) = pinned(before.get(k)), pinned(after.get(k))
            if eb != ea:
                problems.append(f"effects (keys allowed at the pin) differ: {json.dumps(eb)[:120]} -> {json.dumps(ea)[:120]}")
            continue
        if before.get(k) != after.get(k):
            problems.append(f"{k}: {json.dumps(before.get(k))[:80]} -> {json.dumps(after.get(k))[:80]}")
    kb, ka = kit(before), kit(after)
    for j in sorted(set(kb) | set(ka)):
        # RUL-2026-10-18-005: a jutsu that was unequipped before and is now absent from the kit is
        # battle-equivalent (battles load only equipped jutsu), so it is not a difference.
        if j in kb and j not in ka and kb[j][2] is False:
            continue
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
        stripped = set(pinned(before[u].get("effects"))[1]) - set(pinned(a.get("effects"))[1])
        if stripped:
            print(f"       note: obsolete effect keys dropped by the server on save: {sorted(set(stripped))}")
        for p in problems:
            print("       " + p)
        bad += bool(problems)
    print(f"{len(after)} AI(s) read back, {bad} with differences")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
