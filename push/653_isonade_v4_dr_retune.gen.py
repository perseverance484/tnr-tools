#!/usr/bin/env python3
"""Job 653, HIDDEN: Isonade v4 damage-reduction retune.

The director (2026-11-19 17:06Z), after the 16:46Z hidden test: "Yes, lower its damage reduction to one generic
25-30%/2 rounds, and one stronger one it uses in anticipation of a big hit at 40%/1 round".

  Barnacle Hide   DR 40 -> HIDE_DR (2 rounds): the one generic layer. Its 1,500 shield stays.
  Tide Draws Back DR 40 removed (its +50% damage given and the Brine Brand stay).
  Swell Builds    DR 30 removed (same).
  Shed            DR 40 removed (just the cleanse now).
  Silt Cloud      becomes the brace: 40% DR for 1 round, cast when the player's damage-given buffs reach 60.
                  Its -50% damage given on the player is dropped (it was a second damage cut).
  Rules           the Silt Cloud rule moves from slot 17 (below Barnacle Hide, so it almost never fired) to slot 7,
                  just above the Drowned Anchor follow-up: it fires the turn the player stacks a burst, and a buff
                  cast on Isonade's turn is live for the player's next turn (law: effects skip the round they're cast).
                  Still 20 rules.

Law 18: the five edited jutsu come off Isonade (phase 10), are edited (20) and go back on in the same order (30).
Full records from today's capture (state/stolen_stores_captures/isonade_v4_live_2026-11-19), read back first.
The AI profile edit (40) is refused while anyone has a Flooded Stores run open.
Rollback: the captured records and aiProfile_isonade.json in that folder.

Usage: python3 push/653_isonade_v4_dr_retune.gen.py [--hide-dr=30]
Writes push/653_isonade_v4_dr_retune.json. Do not hand-edit.
"""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_v4_live_2026-11-19")
ARGS = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)
HIDE_DR = int(ARGS.get("hide-dr", 30))
assert 25 <= HIDE_DR <= 30, "the director's range is 25-30%"
BRACE_DR, BRACE_ROUNDS = 40, 1
DROP = {"id", "createdAt", "updatedAt"}

ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
HIDE, TIDE, SWELL, SHED, SILT = ("YNaD1O971Ymn0XKNTIynt", "BKfXoZ6Y3YLSoH4WzXvq6", "Aj0gB5-yP38_hSIMVnsXO",
                                 "xfSK_Tu8o4POZeBk2lo4Z", "UCnpSa7BTroijfDgkHDQx")
ANCHOR = "Okp32QuoVFnYKlC9KIrLt"
EDITED = [HIDE, TIDE, SWELL, SHED, SILT]


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


def record(name, jid):
    rec = cap(name)
    assert rec["id"] == jid, (name, rec["id"])
    return {k: v for k, v in copy.deepcopy(rec).items() if k not in DROP}


def dr_index(effs):
    idx = [i for i, e in enumerate(effs) if e["type"] == "decreasedamagetaken"]
    assert len(idx) == 1, idx
    return idx[0]


hide = record("jutsu_barnacle_hide.json", HIDE)
i = dr_index(hide["effects"])
assert hide["effects"][i]["power"] == 40 and hide["effects"][i]["rounds"] == 2
hide["effects"][i]["power"] = HIDE_DR

stripped = {}
for name, jid, old in (("jutsu_tide.json", TIDE, 40), ("jutsu_swell.json", SWELL, 30), ("jutsu_shed.json", SHED, 40)):
    r = record(name, jid)
    i = dr_index(r["effects"])
    assert r["effects"][i]["power"] == old and r["effects"][i]["target"] == "SELF"
    del r["effects"][i]
    stripped[jid] = r

silt = record("jutsu_silt.json", SILT)
assert [e["type"] for e in silt["effects"]] == ["decreasedamagegiven", "decreasedamagetaken"]
assert silt["effects"][1]["power"] == 25 and silt["effects"][1]["rounds"] == 2
silt["effects"] = [silt["effects"][1]]
silt["effects"][0].update(power=BRACE_DR, rounds=BRACE_ROUNDS)
silt["description"] = "It churns up silt and braces: it takes far less damage next round."
silt["battleDescription"] = "%user thrashes and braces. Silt clouds the hold."

ai = cap("getAi_isonade.json")
kit = [j["jutsuId"] for j in ai["jutsus"]]
assert len(kit) == 16 and all(j in kit for j in EDITED)
prof = cap("aiProfile_isonade.json")
rules = copy.deepcopy(prof["rules"])
assert len(rules) == 20
si = [n for n, r in enumerate(rules) if r["action"].get("jutsuId") == SILT]
ai_ = [n for n, r in enumerate(rules) if r["action"].get("jutsuId") == ANCHOR]
assert si == [17] and ai_ == [7], (si, ai_)
silt_rule = rules.pop(17)
assert silt_rule["conditions"][0]["effectType"] == "increasedamagegiven" and silt_rule["conditions"][0]["threshold"] == 60
rules.insert(7, silt_rule)
assert len(rules) == 20

items = [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10, "name": "Isonade: 5 DR jutsu off (law 18)",
     "data": {"jutsus": [j for j in kit if j not in EDITED]}},
    {"entity": "jutsu", "slot": "edit", "targetId": HIDE, "phase": 20, "name": f"Barnacle Hide: DR {HIDE_DR}% 2 rounds", "data": hide},
    {"entity": "jutsu", "slot": "edit", "targetId": TIDE, "phase": 20, "name": "Tide Draws Back: DR removed", "data": stripped[TIDE]},
    {"entity": "jutsu", "slot": "edit", "targetId": SWELL, "phase": 20, "name": "Swell Builds: DR removed", "data": stripped[SWELL]},
    {"entity": "jutsu", "slot": "edit", "targetId": SHED, "phase": 20, "name": "Shed: DR removed", "data": stripped[SHED]},
    {"entity": "jutsu", "slot": "edit", "targetId": SILT, "phase": 20, "name": "Silt Cloud: brace, 40% DR 1 round", "data": silt},
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30, "name": "Isonade: 16-jutsu kit back (law 18)",
     "data": {"jutsus": kit}},
    {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40, "name": "Isonade: Silt Cloud rule above the Anchor (20 rules)",
     "data": {"rules": rules, "includeDefaultRules": False}},
]
m = {"_note": (f"push/653, HIDDEN: Isonade v4 DR retune (Hide {HIDE_DR}%/2r, brace 40%/1r, other DR removed). "
               "Generated by push/653_isonade_v4_dr_retune.gen.py; do not hand-edit."),
     "items": items}
out = os.path.join(ROOT, "push", "653_isonade_v4_dr_retune.json")
with open(out, "w") as f:
    json.dump(m, f, separators=(",", ":"))
print(f"wrote {out}: {len(items)} items (Hide DR {HIDE_DR})")
