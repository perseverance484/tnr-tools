#!/usr/bin/env python3
"""Jobs 655 + 656, HIDDEN: Isonade v5 (Strict, base DR, one clear window per answer).

The director (2026-11-19 19:28Z): "Strict. And lets look at adding some base DR to Isonade as an AI tag so player hits
aren't so large. Players will use lifesteal with big hits to ignore mechanics if their hits are too large. Make sure
you test for this using Eclipse Drain with dauntless. There should be very clear windows to use Clear, Cleanse, Smoke,
Pierce(the deep) and movement(crates) windows". Marks (2026-11-19 22:32Z, his pick): Silt 90 / Scour 100, both on the
player's damage given.

The engine-tested fight is state/flooded_stores_build/isonade_v5_spec.json (results in isonade_v5_results.md):
  r1 Hide, The Tide Draws Back (Clear it), Breaker, Harpoon Line, Brine Brand (Cleanse it), Undertow;
  75% Black Water (stand on a crate); 55% The Swell, Swell Rises, Tidal Bore (Smoke it);
  35% The Deep (pierce its shield); Scour/Silt Cloud react to a damage-given stack; Grasping Arm; base DR on the AI.
Each set piece runs once (cooldown 99). Shed and Drowned Anchor leave the kit (stay hidden in the catalog).

Job 655 (creates): Brine Brand, Undertow, Swell Rises, Tidal Bore, hidden, dedupNames on (names are PLACEHOLDERS).
Job 656 (edits, needs 655's results bundle for literal ids, law 17):
  phase 10  law 18: every edited jutsu off Isonade, plus Shed and Drowned Anchor
  phase 20  full-record edits from today's capture (state/stolen_stores_captures/isonade_v5_live_2026-11-19)
  phase 30  Isonade: the v5 kit (literal ids), pools, effects = stunprevent + base DR (decreasedamagetaken, 99 rounds)
  phase 40  Isonade's AI profile: the v5 rules, Scour/Silt marks at the live values (refused while any Flooded Stores
            or Isonade Test run is open)
Rollback: the captured records, getAi_isonade.json and aiProfile_isonade.json in that capture folder.

Usage: python3 push/655_isonade_v5_windows.gen.py [--bundle=<655 results bundle>]
Writes push/655_isonade_v5_jutsu.json and push/656_isonade_v5_kit.json (656 NOT READY until --bundle). Do not hand-edit.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = json.load(open(os.path.join(ROOT, "state/flooded_stores_build/isonade_v5_spec.json")))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_v5_live_2026-11-19")
V3_BUNDLE = os.path.join(ROOT, "harvests/inbox/tnr_results_1795038853279.json")  # job 648; idmap carries the anim ids
BUNDLES = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--bundle=")]
PFX = "iv5_"
MARKS = {"iso-scour": 100, "iso-silt-cloud": 90}  # the director's pick, live values (validator caps at 100)

sys.path.insert(0, os.path.join(ROOT, "skills/building-tnr-content/scripts"))
_cwd = os.getcwd()
os.chdir(os.path.join(ROOT, "skills/building-tnr-content/data"))
from factory import Factory  # noqa: E402
F = Factory()
os.chdir(_cwd)

V3 = json.load(open(V3_BUNDLE))["idmap"]
ANIM = {k[4:]: v for k, v in V3.items() if k.startswith("fsb_anim_")}
FX = json.load(open(os.path.join(ROOT, "state/skyglass_fx/asset_ids.json")))["assets"]
MARK_FX = {"tg_heavy": (FX["Skyglass Mark - Heavy (tile)"], FX["Skyglass Mark - Heavy (glint)"]),
           "tg_safe": (FX["Skyglass Mark - Safe (tile)"], FX["Skyglass Mark - Safe (floating emblem)"])}

ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
LIVE = {  # sim id -> (live id, capture file)
    "iso-it-rises": ("Kaebmb1nzNi3sMadz0W12", "jutsu_it_rises.json"),
    "iso-barnacle-hide": ("YNaD1O971Ymn0XKNTIynt", "jutsu_barnacle_hide.json"),
    "iso-tide-draws-back": ("BKfXoZ6Y3YLSoH4WzXvq6", "jutsu_tide.json"),
    "iso-breaker": ("z97QVlWZs8uqYcWBQkk-9", "jutsu_breaker.json"),
    "iso-harpoon-line": ("CgmXwQ1PoWi0Y5h7lSEUj", "jutsu_harpoon.json"),
    "iso-black-water-mark": ("vGtG2yV8WqaRTHh-19nVg", "jutsu_bw_omen.json"),
    "iso-black-water": ("EclVg14en924oVI7WtZ6M", "jutsu_bw_floods.json"),
    "iso-the-deep": ("M7TFsshDCNlvyuvOj8JFp", "jutsu_deep_omen.json"),
    "iso-the-deep-crash": ("ElPPRbYnPihCt4iPT6EmW", "jutsu_deep_crashes.json"),
    "iso-the-deep-surface": ("UF0ZDasJZjLiCaPzeXxlW", "jutsu_surfaces.json"),
    "iso-the-swell": ("Aj0gB5-yP38_hSIMVnsXO", "jutsu_swell.json"),  # live "Isonade Swell Builds" becomes the telegraph
    "iso-scour": ("rKct7MpftVKwfq6z27DCZ", "jutsu_scour.json"),
    "iso-silt-cloud": ("UCnpSa7BTroijfDgkHDQx", "jutsu_silt.json"),
    "iso-grasping-arm-rises": ("6w0MWbsSIB2j02MADv1nK", "jutsu_grasping_arm_rises.json"),
}
DROPPED = {"xfSK_Tu8o4POZeBk2lo4Z": "Shed", "Okp32QuoVFnYKlC9KIrLt": "Drowned Anchor"}
NAMES = {  # PLACEHOLDER names for the creates (live names must be unique)
    "iso-brine-brand": "Isonade Brine Brand", "iso-undertow": "Isonade Undertow",
    "iso-the-swell-rises": "Isonade Swell Rises", "iso-tidal-bore": "Isonade Tidal Bore",
}
NEVER_OVERLAY = {"iso-it-rises", "iso-grasping-arm-rises"}  # reused as live; the arm's summon carries the live aiId
OVERLAY = ["description", "battleDescription", "target", "method", "range", "methodSize", "coordinateTargeting",
           "cooldown", "actionCostPerc", "effects"]
DROP = {"id", "createdAt", "updatedAt"}


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


def canon(v):
    """Comparable form: key order, coordinate key order and the editor-only animationScale don't matter."""
    if isinstance(v, dict):
        return {k: canon(x) for k, x in sorted(v.items()) if k != "animationScale"}
    if isinstance(v, list):
        return [canon(x) for x in v]
    return v


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


idmap = {}
for b in BUNDLES:
    idmap.update(json.load(open(b)).get("idmap") or {})


def lit(jid):
    if jid in LIVE:
        return LIVE[jid][0]
    assert jid in NAMES, jid
    return idmap.get(PFX + jid, f"@jutsu:{PFX}{jid}")


# ---------------------------------------------------------------- 655: creates
def jutsu_create(jid):
    rec = SPEC["newJutsu"][jid]
    nullable = set(F.checks["nullable"]["fields"].get("jutsu", []))
    data = {k: v for k, v in rec.items() if k not in DROP and (v is not None or k in nullable)}
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


iso = SPEC["ais"]["iso-isonade"]
kit_sim = iso["jutsus"]
assert set(NAMES) <= set(kit_sim), set(NAMES) - set(kit_sim)
assert set(kit_sim) <= set(LIVE) | set(NAMES), set(kit_sim) - set(LIVE) - set(NAMES)
items655 = [jutsu_create(j) for j in NAMES]
m655 = {"_note": ("push/655, HIDDEN: Isonade v5's 4 new jutsu (Brine Brand, Undertow, Swell Rises, Tidal Bore). "
                  "Names are placeholders. Generated by push/655_isonade_v5_windows.gen.py; do not hand-edit."),
        "dedupNames": True, "items": items655}

# ---------------------------------------------------------------- 656: law 18, edits, kit, rules
edits, unchanged = [], []
for jid in kit_sim:
    if jid not in LIVE:
        continue
    live_id, capfile = LIVE[jid]
    rec = cap(capfile)
    assert rec["id"] == live_id, (capfile, rec["id"])
    data = {k: v for k, v in copy.deepcopy(rec).items() if k not in DROP}
    spec = SPEC["newJutsu"][jid]
    if jid in NEVER_OVERLAY:
        diff = [k for k in OVERLAY if k != "effects" and canon(spec.get(k)) != canon(rec.get(k))]
        print(f"  {jid}: reused as live; spec differs on {diff or 'nothing'} (not applied)")
        unchanged.append(live_id)
        continue
    for k in OVERLAY:
        data[k] = fx(spec[k]) if k == "effects" else copy.deepcopy(spec.get(k))
    changed = [k for k in OVERLAY if canon(data.get(k)) != canon(rec.get(k))]
    if not changed:
        unchanged.append(live_id)
        continue
    edits.append((jid, live_id, rec["name"], changed, data))

live_kit = [j["jutsuId"] for j in cap("getAi_isonade.json")["jutsus"]]
assert len(live_kit) == 16 and all(d in live_kit for d in DROPPED), live_kit
edited_ids = [e[1] for e in edits]
assert all(i in live_kit for i in edited_ids), [i for i in edited_ids if i not in live_kit]
kit = [lit(j) for j in kit_sim]
assert len(kit) == len(set(kit)) == len(kit_sim)


def rule(r):
    conds = []
    for c in r["conditions"]:
        kw = {k: v for k, v in c.items() if k not in ("type", "description")}
        conds.append(F.condition(c["type"], **kw))
    a = {k: v for k, v in r["action"].items() if k != "type"}
    sim_jid = a.get("jutsuId")
    if sim_jid in MARKS:
        assert len(conds) == 1 and conds[0]["type"] == "target_has_effect" and conds[0]["effectType"] == "increasedamagegiven"
        conds[0]["threshold"] = MARKS[sim_jid]
    if sim_jid:
        a["jutsuId"] = lit(sim_jid)
    if not a.get("description"):
        a.pop("description", None)
    return {"conditions": conds, "action": F.action(r["action"]["type"], **a)}


rules = [rule(r) for r in iso["rules"]]
assert len(rules) <= 20, len(rules)
for r in rules:
    for c in r["conditions"]:
        assert 0 <= c.get("threshold", 0) <= 100, c
live_stun = [e for e in cap("getAi_isonade.json")["effects"] if e["type"] == "stunprevent"]
base_dr = [e for e in iso["effects"] if e["type"] == "decreasedamagetaken"]
assert len(live_stun) == 1 and len(base_dr) == 1 and base_dr[0]["rounds"] == 99
ai_effects = live_stun + base_dr

items656 = [{"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
             "name": f"Isonade: {len(edited_ids)} edited jutsu off, Shed and Drowned Anchor off (law 18)",
             "data": {"jutsus": [j for j in live_kit if j not in edited_ids and j not in DROPPED]}}]
for jid, live_id, name, changed, data in edits:
    items656.append({"entity": "jutsu", "slot": "edit", "targetId": live_id, "phase": 20,
                     "name": f"{name}: v5 ({', '.join(changed)})", "data": data})
items656 += [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
     "name": f"Isonade: v5 kit ({len(kit)}), pools x{iso['poolsMultiplier']}, base DR {base_dr[0]['power']}%",
     "data": {"jutsus": kit, "poolsMultiplier": iso["poolsMultiplier"], "effects": ai_effects}},
    {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40,
     "name": f"Isonade: v5 rules ({len(rules)}), Scour {MARKS['iso-scour']} / Silt {MARKS['iso-silt-cloud']}",
     "data": {"rules": rules, "includeDefaultRules": False}},
]
open_refs = sorted(set(re.findall(r'"(@jutsu:[^"]+)"', json.dumps(items656))))
m656 = {"_note": ("push/656, HIDDEN: Isonade v5 kit, edits, base DR and rules (law 18 on every edited jutsu). "
                  + (f"NOT READY: {len(open_refs)} refs wait on 655's results bundle. " if open_refs else "Refs resolved. ")
                  + "Generated by push/655_isonade_v5_windows.gen.py; do not hand-edit."),
        "items": items656}

for name, m in (("655_isonade_v5_jutsu", m655), ("656_isonade_v5_kit", m656)):
    out = os.path.join(ROOT, "push", f"{name}.json")
    with open(out, "w") as f:
        json.dump(m, f, separators=(",", ":"))
    print(f"wrote {out}: {len(m['items'])} items")
print("edited:", [(e[2], e[3]) for e in edits])
print("unchanged live:", unchanged)
print("open refs in 656:", len(open_refs))
