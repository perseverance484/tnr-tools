#!/usr/bin/env python3
"""Jobs 651 + 652, HIDDEN: Isonade v4 (the director: "Yes, build it", 2026-11-19 16:16Z).

The engine-tested v4 fight (state/flooded_stores_build/isonade_v4_spec.json, rev 3, results in isonade_v4_results.md):
a one-beat-a-round rotation (Barnacle Hide -> The Tide Draws Back -> The Swell Builds -> Breaker -> Harpoon Line),
two Black Water set pieces on HP gates (75% flood, 40% The Deep shield), reactive Scour/Shed/Silt Cloud with the
Drowned Anchor, and Isonade's own Clearable DR layers. 20 rules, 16 jutsu on Isonade, Arm Lash on the Grasping Arm.

Job 651 (creates): the 14 new jutsu, hidden, dedupNames on (names are PLACEHOLDERS: the director's call).
Job 652 (edits, needs 651's results bundle for literal ids, law 17):
  phase 10  law 18: Grasping Arm Rises off Isonade, Arm Lash off the Grasping Arm
  phase 20  Arm Lash power 70 -> 45; Grasping Arm Rises 40 -> 30 AP (full records from today's capture, one field each)
  phase 30  Isonade: the v4 kit (16, literal ids) and pools x8.4 -> x4; the Grasping Arm: Arm Lash back
  phase 40  Isonade's AI profile: the 20 v4 rules (profile edits are refused while anyone has a Flooded Stores run open)
It Rises is reused as live (only its description differs from the spec). The v3 jutsu are only unequipped; they stay
hidden in the catalog. Rollback = push/648's kit + the rules captured in
state/stolen_stores_captures/isonade_live_2026-11-19/aiProfile_isonade.json + pools x8.4.

Usage: python3 push/651_isonade_v4.gen.py [--bundle=<651 results bundle>]
Writes push/651_isonade_v4_jutsu.json and push/652_isonade_v4_kit.json (652 is NOT READY until --bundle). Do not hand-edit.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = json.load(open(os.path.join(ROOT, "state/flooded_stores_build/isonade_v4_spec.json")))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_live_2026-11-19")
V3_BUNDLE = os.path.join(ROOT, "harvests/inbox/tnr_results_1795038853279.json")  # job 648; idmap carries every v3 id
BUNDLES = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--bundle=")]
PFX = "iv4_"

sys.path.insert(0, os.path.join(ROOT, "skills/building-tnr-content/scripts"))
_cwd = os.getcwd()
os.chdir(os.path.join(ROOT, "skills/building-tnr-content/data"))
from factory import Factory  # noqa: E402
F = Factory()
os.chdir(_cwd)

V3 = json.load(open(V3_BUNDLE))["idmap"]
ISONADE = V3["fsb_iso-isonade"]
ARM = V3["fsb_iso-grasping-arm"]
ARM_LASH = V3["fsb_iso-arm-lash"]
ARM_RISES = V3["fsb_iso-grasping-arm-rises"]
IT_RISES = V3["fsb_iso-it-rises"]
ANIM = {k[4:]: v for k, v in V3.items() if k.startswith("fsb_anim_")}
FX = json.load(open(os.path.join(ROOT, "state/skyglass_fx/asset_ids.json")))["assets"]
MARK_FX = {"tg_heavy": (FX["Skyglass Mark - Heavy (tile)"], FX["Skyglass Mark - Heavy (glint)"]),
           "tg_safe": (FX["Skyglass Mark - Safe (tile)"], FX["Skyglass Mark - Safe (floating emblem)"])}

REUSED = {"iso-it-rises": IT_RISES, "iso-grasping-arm-rises": ARM_RISES, "iso-arm-lash": ARM_LASH}
NAMES = {  # PLACEHOLDER names (live names must be unique; v3 convention "Isonade X", "Isonade Omen: X" for a warning)
    "iso-barnacle-hide": "Isonade Barnacle Hide", "iso-tide-draws-back": "Isonade Tide Draws Back",
    "iso-the-swell": "Isonade Swell Builds", "iso-breaker": "Isonade Breaker", "iso-harpoon-line": "Isonade Harpoon Line",
    "iso-black-water-mark": "Isonade Omen: Black Water", "iso-black-water": "Isonade Black Water Floods",
    "iso-the-deep": "Isonade Omen: The Deep", "iso-the-deep-crash": "Isonade The Deep Crashes",
    "iso-the-deep-surface": "Isonade Surfaces", "iso-scour": "Isonade Scour", "iso-shed": "Isonade Shed",
    "iso-drowned-anchor": "Isonade Drowned Anchor", "iso-silt-cloud": "Isonade Silt Cloud",
}
JUTSU_DROP = {"id", "createdAt", "updatedAt"}


def fx(effects):
    out = []
    for e in copy.deepcopy(effects):
        sa = e.get("staticAnimation", "")
        if sa in MARK_FX:
            tile, glint = MARK_FX[sa]
            e["staticAnimation"] = glint
            if not e.get("staticAssetPath"):
                e["staticAssetPath"] = tile
        for f in ("staticAnimation", "appearAnimation", "disappearAnimation"):
            v = e.get(f, "")
            if v.startswith("anim_"):
                assert v in ANIM, v
                e[f] = ANIM[v]
        out.append(e)
    return out


def jutsu_create(jid):
    rec = SPEC["newJutsu"][jid]
    nullable = set(F.checks["nullable"]["fields"].get("jutsu", []))
    data = {k: v for k, v in rec.items() if k not in JUTSU_DROP and (v is not None or k in nullable)}
    data["name"] = NAMES[jid]
    data["hidden"] = True
    effs = fx(data.pop("effects"))
    try:
        F._effects("jutsu", effs)
    except Exception as err:  # noqa: BLE001  (law 4 generalTypes check is stale at the pin; see flooded_stores_build.gen.py)
        if "generalTypes" not in str(err):
            raise
    e = F.entry("jutsu", "create", name=data["name"], srcId=PFX + jid, data=data)
    e["data"]["effects"] = effs
    e["phase"] = 20
    return e


idmap = {}
for b in BUNDLES:
    idmap.update(json.load(open(b)).get("idmap") or {})


def lit(jid):
    if jid in REUSED:
        return REUSED[jid]
    return idmap.get(PFX + jid, f"@jutsu:{PFX}{jid}")


def rule(r):
    conds = [F.condition(c["type"], **{k: v for k, v in c.items() if k not in ("type", "description")}) for c in r["conditions"]]
    a = {k: v for k, v in r["action"].items() if k != "type"}
    if a.get("jutsuId"):
        a["jutsuId"] = lit(a["jutsuId"])
    if not a.get("description"):
        a.pop("description", None)
    return {"conditions": conds, "action": F.action(r["action"]["type"], **a)}


def full_edit(capfile, changes):
    rec = json.load(open(os.path.join(CAP, capfile)))
    data = {k: v for k, v in rec.items() if k not in JUTSU_DROP}
    for path, (old, new) in changes.items():
        o = data
        keys = path.split(".")
        for k in keys[:-1]:
            o = o[int(k)] if k.isdigit() else o[k]
        assert o[keys[-1]] == old, (capfile, path, o[keys[-1]])
        o[keys[-1]] = new
    return data


# ---------------------------------------------------------------- 651: creates
new_ids = [j for j in SPEC["newJutsu"] if j not in REUSED]
assert sorted(new_ids) == sorted(NAMES), (new_ids, NAMES)
assert len(set(NAMES.values())) == len(NAMES)
items651 = [jutsu_create(j) for j in new_ids]
m651 = {"_note": ("push/651, HIDDEN: Isonade v4's 14 new jutsu (rev 3 spec, engine-tested offline). Names are placeholders. "
                  "Generated by push/651_isonade_v4.gen.py; do not hand-edit."),
        "dedupNames": True, "items": items651}

# ---------------------------------------------------------------- 652: law 18 + kit + rules
iso = SPEC["ais"]["iso-isonade"]
old_kit = [j["jutsuId"] for j in json.load(open(os.path.join(CAP, "getAi_isonade.json")))["jutsus"]]
assert ARM_RISES in old_kit and len(old_kit) == 17
kit = [lit(j) for j in iso["jutsus"]]
assert len(kit) == 16 and len(set(kit)) == 16
rules = [rule(r) for r in iso["rules"]]
assert len(rules) == 20
arm_rises = full_edit("jutsu_grasping_arm_rises.json", {"actionCostPerc": (40, SPEC["newJutsu"]["iso-grasping-arm-rises"]["actionCostPerc"])})
arm_lash = full_edit("jutsu_arm_lash.json", {"effects.0.power": (70, SPEC["newJutsu"]["iso-arm-lash"]["effects"][0]["power"])})
assert arm_rises["actionCostPerc"] == 30 and arm_lash["effects"][0]["power"] == 45
items652 = [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10, "name": "Isonade: Grasping Arm Rises off (law 18)",
     "data": {"jutsus": [j for j in old_kit if j != ARM_RISES]}},
    {"entity": "ai", "slot": "edit", "targetId": ARM, "phase": 10, "name": "Grasping Arm: Arm Lash off (law 18)",
     "data": {"jutsus": []}},
    {"entity": "jutsu", "slot": "edit", "targetId": ARM_RISES, "phase": 20, "name": "Grasping Arm Rises: 30 AP", "data": arm_rises},
    {"entity": "jutsu", "slot": "edit", "targetId": ARM_LASH, "phase": 20, "name": "Arm Lash: power 45", "data": arm_lash},
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30, "name": "Isonade: v4 kit (16), pools x4",
     "data": {"jutsus": kit, "poolsMultiplier": iso["poolsMultiplier"]}},
    {"entity": "ai", "slot": "edit", "targetId": ARM, "phase": 30, "name": "Grasping Arm: Arm Lash back (law 18)",
     "data": {"jutsus": [ARM_LASH]}},
    {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40, "name": "Isonade: v4 rules (20)",
     "data": {"rules": rules, "includeDefaultRules": False}},
]
open_refs = sorted(set(re.findall(r'"(@jutsu:[^"]+)"', json.dumps(items652))))
m652 = {"_note": ("push/652, HIDDEN: Isonade v4 kit and rules; law 18 on Grasping Arm Rises and Arm Lash. "
                  + (f"NOT READY: {len(open_refs)} refs wait on 651's results bundle. " if open_refs else "Refs resolved. ")
                  + "Generated by push/651_isonade_v4.gen.py; do not hand-edit."),
        "items": items652}

for name, m in (("651_isonade_v4_jutsu", m651), ("652_isonade_v4_kit", m652)):
    out = os.path.join(ROOT, "push", f"{name}.json")
    with open(out, "w") as f:
        json.dump(m, f, separators=(",", ":"))
    print(f"wrote {out}: {len(m['items'])} items")
print("open refs in 652:", len(open_refs))
