#!/usr/bin/env python3
"""Job 671, HIDDEN: Isonade v11, the one proposal from the v10 QA pass.

The director (2026-11-20 14:07Z, in the Isonade thread) answered "Yes" to "Should I build v11 hidden and test it at
full HP?". The proposal is state/flooded_stores_build/isonade_v11_proposal.md, simulated with
isonade_v11_sim/v11_proposal.json (engine pin 3314d122, 16 seeds per read).

What this writes, all hidden:
  create  "Isonade The Hold Floods" (jutsuType AI): the sim's iso-hold-floods. Cooldown 1, 30 AP, single target on the
          player (Harpoon's targeting). Pierce 15 (Harpoon's pierce shape), +12% damage taken on the player for 99
          rounds and +20% damage taken on Isonade for 99 rounds, both stacking per use.
  jutsu   Barnacle Hide cooldown 3 -> 6; Harpoon Line 2 -> 4; Scour 5 -> 8; Silt Cloud 5 -> 8 (the proposal's text;
          the sim ran Silt at 10, see the write-up); Omen: Black Water's two visual marks last 2 rounds (was 1);
          Brine Brand's description says the Undertow comes either way and a Cleanse softens it; Arm Lash damage
          power 45 -> 20.
  law 18  Every edited jutsu comes off its AI first (phase 10), is edited (20), and the full kit goes back (30):
          Isonade (6 jutsu) and the Grasping Arm (Arm Lash). No other AI equips them.
  ai      Isonade poolsMultiplier 2.5 -> 2.1, kit 18 -> 19 (the new jutsu). It Rises stays equipped; only its rule goes.
  rules   20 rules, at the cap: It Rises' rule goes; The Undertow and Breaker move above Scour and Silt; The Hold
          Floods (round > 10) sits last before end_turn, so it only uses AP left after the round's real move.
Unchanged: record effects (stun guard, 70% hull, 5-round seal guard), Old Hull on CHEST at drop 0, the avatar.
Rollback: the captures in state/stolen_stores_captures/isonade_v11_live_2026-11-20.

Two stages (law 17: an AI's jutsus array and its rules take literal ids):
  python3 push/671_isonade_v11.gen.py                      writes push/671_isonade_v11_create.json (the create)
  python3 push/671_isonade_v11.gen.py --bundle=<results>   also writes push/671_isonade_v11.json (everything else),
                                                           with the new jutsu's id from the create's results bundle
Do not hand-edit either manifest.
"""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_v11_live_2026-11-20")
PFX = "iv11_"
DROP = {"id", "createdAt", "updatedAt"}

ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
ARM_AI = "lJAnVI4eBn5YjCgghqBji"
IT_RISES = "Kaebmb1nzNi3sMadz0W12"
UNDERTOW = "49k-zlISWsouayutA7kJr"
BREAKER = "z97QVlWZs8uqYcWBQkk-9"
DEEP_OMEN = "M7TFsshDCNlvyuvOj8JFp"
SCOUR = "rKct7MpftVKwfq6z27DCZ"
SILT = "UCnpSa7BTroijfDgkHDQx"
HARPOON = "CgmXwQ1PoWi0Y5h7lSEUj"
BARNACLE = "YNaD1O971Ymn0XKNTIynt"
BW_OMEN = "vGtG2yV8WqaRTHh-19nVg"
BRINE = "csR7tJYXd6rkQp2oGi7ai"
ARM_LASH = "QMXGlGM34xcBfDLWfJYoB"
FLOOD_AFTER = 10
POOLS = 2.1


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


def editable(rec):
    return {k: v for k, v in copy.deepcopy(rec).items() if k not in DROP}


ai = cap("getAi_isonade.json")
arm = cap("getAi_grasping_arm.json")
prof = cap("aiProfile_isonade.json")
assert ai["userId"] == ISONADE and arm["userId"] == ARM_AI and prof["userId"] == ISONADE
live_kit = [j["jutsuId"] for j in ai["jutsus"]]
assert len(live_kit) == 18 and all(j["equipped"] for j in ai["jutsus"]), live_kit
assert ai["poolsMultiplier"] == 2.5
assert [(i["itemId"], i["equipped"]) for i in ai["items"]] == [("ZBfu0h3K6U1g45Q4gTOG7", "CHEST")]
arm_kit = [j["jutsuId"] for j in arm["jutsus"]]
assert arm_kit == [ARM_LASH] and arm["jutsus"][0]["equipped"] and arm["items"] == []

# ---------------------------------------------------------------- jutsu edits (whole record, read back first)
edits = {}  # id -> (name, label, data)

rec = cap("jutsu_barnacle.json"); assert rec["id"] == BARNACLE and rec["cooldown"] == 3
d = editable(rec); d["cooldown"] = 6; edits[BARNACLE] = (rec["name"], "cooldown 3 -> 6", d)

rec = cap("jutsu_harpoon.json"); assert rec["id"] == HARPOON and rec["cooldown"] == 2
harpoon = rec
d = editable(rec); d["cooldown"] = 4; edits[HARPOON] = (rec["name"], "cooldown 2 -> 4", d)

for jid, f in ((SCOUR, "jutsu_scour.json"), (SILT, "jutsu_silt.json")):
    rec = cap(f); assert rec["id"] == jid and rec["cooldown"] == 5, (f, rec["cooldown"])
    d = editable(rec); d["cooldown"] = 8; edits[jid] = (rec["name"], "cooldown 5 -> 8", d)

rec = cap("jutsu_bw_omen.json"); assert rec["id"] == BW_OMEN
d = editable(rec)
vis = [e for e in d["effects"] if e["type"] == "visual"]
assert len(vis) == 2 and all(e["rounds"] == 1 for e in vis), vis
for e in vis:
    e["rounds"] = 2
edits[BW_OMEN] = (rec["name"], "red and crate marks last 2 rounds (was 1)", d)

rec = cap("jutsu_brine_brand.json"); assert rec["id"] == BRINE
assert rec["description"].startswith("It brands you with brine.")
d = editable(rec)
d["description"] = "It brands you with brine. The Undertow comes next either way. Cleanse the brand and it hits far softer."
edits[BRINE] = (rec["name"], "description: the Undertow comes either way", d)

rec = cap("jutsu_arm_lash.json"); assert rec["id"] == ARM_LASH
d = editable(rec)
dmg = [e for e in d["effects"] if e["type"] == "damage"]
assert len(dmg) == 1 and dmg[0]["power"] == 45
dmg[0]["power"] = 20
edits[ARM_LASH] = (rec["name"], "damage power 45 -> 20", d)

for jid, (_, _, d) in edits.items():
    assert d["hidden"] is True and d["jutsuType"] == "AI", jid

# ---------------------------------------------------------------- the new jutsu (Harpoon's targeting and pierce shape)
flood = editable(harpoon)
pierce = copy.deepcopy([e for e in harpoon["effects"] if e["type"] == "pierce"][0])
assert pierce["dmgModifier"] == 2 and pierce["calculation"] == "formula"
pierce["power"] = 15
pierce["description"] = "The hold floods"


def pct(power, target, desc, **extra):
    e = {"type": "increasedamagetaken", "power": power, "rounds": 99, "target": target, "appearSfx": "",
         "direction": "offence", "calculation": "percentage", "description": desc, "disappearSfx": "",
         "powerPerLevel": 0, "animationScale": 1, "appearAnimation": "", "staticAnimation": "",
         "staticAssetPath": "", "disappearAnimation": ""}
    e.update(extra)
    return e


flood.update({
    "name": "Isonade The Hold Floods",
    "description": "The hold is filling. Every turn from now on the black water hits harder, on you and on it.",
    "battleDescription": "Black water pours into the hold and drags at %target.",
    "cooldown": 1,
    "actionCostPerc": 30,
    "hidden": True,
    "effects": [pierce,
                pct(12, "INHERIT", "The hold floods", friendlyFire="ENEMIES"),
                pct(20, "SELF", "The flood cracks its hull")],
})
SRC = f"{PFX}hold_floods"
BUNDLES = [a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--bundle=")]
idmap = {}
for b in BUNDLES:
    idmap.update(json.load(open(b)).get("idmap") or {})
FLOOD_REF = idmap.get(SRC, f"@jutsu:{SRC}")

# ---------------------------------------------------------------- rules
rules = copy.deepcopy(prof["rules"])
assert len(rules) == 20 and prof["includeDefaultRules"] is False
ids = [r["action"].get("jutsuId") for r in rules]
assert ids[0] == IT_RISES and rules[0]["conditions"] == [], rules[0]
assert ids[-1] is None and rules[-1]["action"]["type"] == "end_turn"
rules.pop(0)
moved = []
for jid in (UNDERTOW, BREAKER):
    i = [r["action"].get("jutsuId") for r in rules].index(jid)
    moved.append(rules.pop(i))
at = [r["action"].get("jutsuId") for r in rules].index(DEEP_OMEN) + 1
rules[at:at] = moved
flood_rule = copy.deepcopy(rules[0])  # a use_specific_jutsu on SELF, as every rule here
flood_rule["action"]["jutsuId"] = FLOOD_REF
flood_rule["conditions"] = [{"type": "round_greater_than", "value": FLOOD_AFTER,
                             "description": "Current round is greater than specified value"}]
assert flood_rule["action"]["type"] == "use_specific_jutsu" and flood_rule["action"]["target"] == "SELF"
rules.insert(len(rules) - 1, flood_rule)
new_ids = [r["action"].get("jutsuId") for r in rules]
assert len(rules) == 20
assert new_ids[:10] == ["ElPPRbYnPihCt4iPT6EmW", "UF0ZDasJZjLiCaPzeXxlW", "EclVg14en924oVI7WtZ6M",
                        "5_izyS8vstAh6Yt9RPOwz", "0eIhyLEPAN1KsSs7P3Kzd", DEEP_OMEN, UNDERTOW, BREAKER, SCOUR, SILT], new_ids
assert new_ids[-2:] == [FLOOD_REF, None], new_ids[-2:]
assert IT_RISES not in new_ids

# ---------------------------------------------------------------- manifest
iso_edited = [j for j in edits if j in live_kit]
assert len(iso_edited) == 6
create = {"_note": ("push/671 stage 1, HIDDEN: create Isonade The Hold Floods (jutsuType AI, equipped by nothing yet). "
                   "Generated by push/671_isonade_v11.gen.py; do not hand-edit."),
          "dedupNames": False,
          "items": [{"entity": "jutsu", "slot": "create", "srcId": SRC, "phase": 5, "name": flood["name"], "data": flood}]}
out = os.path.join(ROOT, "push", "671_isonade_v11_create.json")
with open(out, "w") as f:
    json.dump(create, f, separators=(",", ":"))
print(f"wrote {out}: 1 item")
if FLOOD_REF.startswith("@"):
    print("stage 2 NOT written: pass --bundle=<the create's results bundle>")
    sys.exit(0)
assert len(FLOOD_REF) == 21, FLOOD_REF

items = [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
     "name": "Isonade: 6 jutsu off for their edits (law 18)",
     "data": {"jutsus": [j for j in live_kit if j not in iso_edited]}},
    {"entity": "ai", "slot": "edit", "targetId": ARM_AI, "phase": 10,
     "name": "Grasping Arm: Arm Lash off for its edit (law 18)", "data": {"jutsus": []}},
]
for jid, (name, label, data) in edits.items():
    items.append({"entity": "jutsu", "slot": "edit", "targetId": jid, "phase": 20, "name": f"{name}: {label}", "data": data})
items += [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
     "name": f"Isonade: full kit back plus The Hold Floods ({len(live_kit) + 1}); pools {ai['poolsMultiplier']} -> {POOLS}",
     "data": {"jutsus": live_kit + [FLOOD_REF], "poolsMultiplier": POOLS}},
    {"entity": "ai", "slot": "edit", "targetId": ARM_AI, "phase": 30,
     "name": "Grasping Arm: Arm Lash back on", "data": {"jutsus": arm_kit}},
    {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40,
     "name": f"Isonade: v11 rules (It Rises out, payoffs above reactions, The Hold Floods after round {FLOOD_AFTER}; 20)",
     "data": {"rules": rules, "includeDefaultRules": False}},
]
m = {"_note": ("push/671, HIDDEN: Isonade v11 (new The Hold Floods, cooldowns, rule order, pools 2.1, Arm Lash 20, "
               "Black Water marks 2 rounds, Brine Brand text). Law 18 on Isonade and the Grasping Arm. "
               "Generated by push/671_isonade_v11.gen.py; do not hand-edit."),
     "items": items}
out = os.path.join(ROOT, "push", "671_isonade_v11.json")
with open(out, "w") as f:
    json.dump(m, f, separators=(",", ":"))
print(f"wrote {out}: {len(items)} items; rules:", [i if i else "end" for i in new_ids])
