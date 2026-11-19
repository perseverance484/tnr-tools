#!/usr/bin/env python3
"""Job 658, HIDDEN: Isonade v6 (The Deep always called at 35%, Scour and Silt Cloud back sooner).

The director (2026-11-19 23:19Z, "Go ahead") on: move Scour and Silt ahead of the rotation, force The Deep at 35%,
then one hidden retest on dauntless with a smoke bomb and a pierce kit. All hidden.

What the v5 live test showed (isonade_v5_results.md): The Deep never fired and Scour fired once. The Deep's omen sat at
rule 15 and costs 70 AP, so any 60 AP action earlier in the list that turn left too little AP for it. Scour and Silt
already sit ahead of the chain (rules 6 and 7); what kept them quiet was their 10-round cooldown, not their place.

Changes (sim: state/flooded_stores_build/isonade_v6_results.md):
  rules  The Deep's omen moves from 15 to 6: right after the set-piece lands (so it never cuts a landing in half, and
         the crash rule above it can't fire the same turn) and ahead of Scour, Silt and the chain. It keeps 70 AP, so
         nothing else rides along on the omen turn and the pierce window stays clean. Still 20 rules.
  jutsu  Scour and Silt Cloud cooldown 10 -> CD (a balance value: a REVERSIBLE HIDDEN PLACEHOLDER picked from the sim
         until the director settles it; CLAUDE.md section 10).
  law 18 Scour and Silt off Isonade (phase 10), edited (20), the full live kit back on (30), rules (40).
Rollback: getAi_isonade.json, aiProfile_isonade.json, jutsu_scour.json and jutsu_silt.json in
state/stolen_stores_captures/isonade_v6_live_2026-11-19.

Usage: python3 push/658_isonade_v6_reactions.gen.py --cd=N
Writes push/658_isonade_v6_reactions.json. Do not hand-edit.
"""
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_v6_live_2026-11-19")
CD = [int(a.split("=", 1)[1]) for a in sys.argv[1:] if a.startswith("--cd=")]
assert len(CD) == 1 and 1 <= CD[0] <= 10, "pass --cd=N (1..10)"
CD = CD[0]

ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
DEEP_OMEN = "M7TFsshDCNlvyuvOj8JFp"
SCOUR = "rKct7MpftVKwfq6z27DCZ"
SILT = "UCnpSa7BTroijfDgkHDQx"
SET_PIECE_LANDS = ["ElPPRbYnPihCt4iPT6EmW", "UF0ZDasJZjLiCaPzeXxlW", "EclVg14en924oVI7WtZ6M",
                   "5_izyS8vstAh6Yt9RPOwz", "0eIhyLEPAN1KsSs7P3Kzd"]  # Deep Crashes, Surfaces, BW Floods, Bore, Swell Rises
DROP = {"id", "createdAt", "updatedAt"}


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


ai = cap("getAi_isonade.json")
assert ai["userId"] == ISONADE
live_kit = [j["jutsuId"] for j in ai["jutsus"]]
assert len(live_kit) == 18 and all(j["equipped"] for j in ai["jutsus"]), live_kit
assert SCOUR in live_kit and SILT in live_kit and DEEP_OMEN in live_kit

# ---- jutsu edits: whole record, read back first (the captures), cooldown only
edits = []
for jid, capfile in ((SCOUR, "jutsu_scour.json"), (SILT, "jutsu_silt.json")):
    rec = cap(capfile)
    assert rec["id"] == jid and rec["hidden"] is True and rec["cooldown"] == 10, (capfile, rec["cooldown"])
    data = {k: v for k, v in copy.deepcopy(rec).items() if k not in DROP}
    data["cooldown"] = CD
    edits.append((jid, rec["name"], data))

# ---- rules: move The Deep's omen to sit right after the set-piece lands
prof = cap("aiProfile_isonade.json")
rules = copy.deepcopy(prof["rules"])
assert len(rules) == 20 and prof["includeDefaultRules"] is False
ids = [r["action"].get("jutsuId") for r in rules]
assert ids[0] == "Kaebmb1nzNi3sMadz0W12" and ids[1:6] == SET_PIECE_LANDS, ids[:6]
old = ids.index(DEEP_OMEN)
assert old == 15 and rules[old]["conditions"] == [{"type": "health_below", "value": 35,
                                                     "description": "Health below given percentage"}]
omen = rules.pop(old)
rules.insert(6, omen)
new_ids = [r["action"].get("jutsuId") for r in rules]
assert new_ids[6] == DEEP_OMEN and new_ids[7] == SCOUR and new_ids[8] == SILT and len(rules) == 20
assert sorted(map(str, ids)) == sorted(map(str, new_ids))
for r in rules:
    for c in r["conditions"]:
        assert 0 <= c.get("threshold", 0) <= 100 and 0 <= c.get("value", 0) <= 100, c

edited = [e[0] for e in edits]
items = [{"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
          "name": "Isonade: Scour and Silt Cloud off (law 18)",
          "data": {"jutsus": [j for j in live_kit if j not in edited]}}]
for jid, name, data in edits:
    items.append({"entity": "jutsu", "slot": "edit", "targetId": jid, "phase": 20,
                  "name": f"{name}: cooldown 10 -> {CD} (placeholder)", "data": data})
items += [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
     "name": f"Isonade: live kit back on ({len(live_kit)})", "data": {"jutsus": live_kit}},
    {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40,
     "name": "Isonade: The Deep's omen moved from rule 15 to rule 6 (20 rules)",
     "data": {"rules": rules, "includeDefaultRules": False}},
]
m = {"_note": (f"push/658, HIDDEN: Isonade v6. The Deep's omen moves to rule 6; Scour and Silt Cloud cooldown 10 -> {CD} "
               "(reversible placeholder). Law 18 on both. Generated by push/658_isonade_v6_reactions.gen.py; do not hand-edit."),
     "items": items}
out = os.path.join(ROOT, "push", "658_isonade_v6_reactions.json")
with open(out, "w") as f:
    json.dump(m, f, separators=(",", ":"))
print(f"wrote {out}: {len(items)} items; rule order:", new_ids)
