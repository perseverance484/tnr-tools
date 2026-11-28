#!/usr/bin/env python3
"""Job 666, HIDDEN: Isonade v7 marker key. The Undertow fires off a self mark no player can make.

The director (2026-11-20 00:00Z, "Test both and we'll use the better solution"). This is fix A3 in
state/flooded_stores_build/isonade_v7_rule_keys.md, the marker key.

Rule thresholds are capped at 100 (validators/ai.ts) and prevent tags reset to power 100 when they land (tags.ts), so a
marker must be a tag that keeps its power and that a player cannot stack to 100 on Isonade. elementalseal fits: it
keeps its power, lands at chance power/100, and the only player jutsu with it carries 80. It blocks only elemental
jutsu, and every Isonade move is classified "None", so on Isonade it does nothing else.

Changes:
  Brine Brand  self "Isonade's rotation" moveprevent 100 (2 rounds)  ->  elementalseal 100 (2 rounds), same text.
  Breaker      drops its self elementalseal 100 (it called the Harpoon); the Harpoon now reads the Breaker's
               self weakness 100 instead. No player jutsu carries weakness.
  rule 9       Undertow: has_effect moveprevent >= 1    ->  has_effect elementalseal >= 100.
  rule 11      Harpoon:  has_effect elementalseal >= 1  ->  has_effect weakness >= 100.
  law 18       Brine and Breaker off Isonade (10), edited (20), the full live kit back on (30), rules (40).
Black Water Floods and Surfaces also put weakness 100 on Isonade, so a Harpoon may follow them too.
Rollback: getAi_isonade_pre658.json (kit), aiProfile_isonade.json, jutsu_brine.json and jutsu_breaker.json in
state/stolen_stores_captures/isonade_v7_live_2026-11-20.

Usage: python3 push/666_isonade_v7_marker_key.gen.py
Writes push/666_isonade_v7_marker_key.json. Do not hand-edit.
"""
import copy
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_v7_live_2026-11-20")
ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
BRINE = "csR7tJYXd6rkQp2oGi7ai"
BREAKER = "z97QVlWZs8uqYcWBQkk-9"
UNDERTOW = "49k-zlISWsouayutA7kJr"
HARPOON = "CgmXwQ1PoWi0Y5h7lSEUj"
DROP = {"id", "createdAt", "updatedAt"}


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


ai = cap("getAi_isonade_pre658.json")
assert ai["userId"] == ISONADE
live_kit = [j["jutsuId"] for j in ai["jutsus"]]
assert len(live_kit) == 18 and BRINE in live_kit and BREAKER in live_kit, live_kit

brine = cap("jutsu_brine.json")
breaker = cap("jutsu_breaker.json")
assert brine["id"] == BRINE and brine["hidden"] is True and breaker["id"] == BREAKER and breaker["hidden"] is True
seal = [e for e in breaker["effects"] if e["type"] == "elementalseal"]
assert len(seal) == 1 and seal[0]["power"] == 100 and seal[0]["rounds"] == 2 and seal[0]["target"] == "SELF", seal
assert any(e["type"] == "weakness" and e["power"] == 100 and e["target"] == "SELF" for e in breaker["effects"])
mp = [i for i, e in enumerate(brine["effects"]) if e["type"] == "moveprevent"]
assert len(mp) == 1 and brine["effects"][mp[0]]["target"] == "SELF" and brine["effects"][mp[0]]["rounds"] == 2

b_data = {k: v for k, v in copy.deepcopy(brine).items() if k not in DROP}
b_data["effects"][mp[0]] = copy.deepcopy(seal[0])  # elementalseal 100, 2 rounds, SELF, "Isonade's rotation"
k_data = {k: v for k, v in copy.deepcopy(breaker).items() if k not in DROP}
k_data["effects"] = [e for e in k_data["effects"] if e["type"] != "elementalseal"]
assert len(k_data["effects"]) == len(breaker["effects"]) - 1

prof = cap("aiProfile_isonade.json")
rules = copy.deepcopy(prof["rules"])
assert len(rules) == 20 and prof["includeDefaultRules"] is False
assert rules[9]["action"]["jutsuId"] == UNDERTOW and rules[11]["action"]["jutsuId"] == HARPOON
assert [c["effectType"] for c in rules[9]["conditions"]] == ["moveprevent"]
assert [c["effectType"] for c in rules[11]["conditions"]] == ["elementalseal"]
has = lambda t: [{"type": "has_effect", "threshold": 100, "effectType": t, "description": "AI is affected by a specific effect"}]
rules[9]["conditions"] = has("elementalseal")
rules[11]["conditions"] = has("weakness")
for r in rules:
    for c in r["conditions"]:
        assert 0 <= c.get("threshold", 0) <= 100 and 0 <= c.get("value", 0) <= 100, c

items = [{"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
          "name": "Isonade: Brine Brand and Breaker off (law 18)",
          "data": {"jutsus": [j for j in live_kit if j not in (BRINE, BREAKER)]}},
         {"entity": "jutsu", "slot": "edit", "targetId": BRINE, "phase": 20,
          "name": "Isonade Brine Brand: self move-lock -> self elementalseal 100 (marker)", "data": b_data},
         {"entity": "jutsu", "slot": "edit", "targetId": BREAKER, "phase": 20,
          "name": "Isonade Breaker: self elementalseal removed", "data": k_data},
         {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
          "name": f"Isonade: live kit back on ({len(live_kit)})", "data": {"jutsus": live_kit}},
         {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40,
          "name": "Isonade: Undertow on elementalseal 100, Harpoon on weakness 100 (20 rules)",
          "data": {"rules": rules, "includeDefaultRules": False}}]
m = {"_note": ("push/666, HIDDEN: Isonade v7 marker key. Brine's self marker becomes elementalseal 100; Breaker drops "
               "its elementalseal; Undertow keyed on elementalseal 100, Harpoon on weakness 100. Law 18. Generated by "
               "push/666_isonade_v7_marker_key.gen.py; do not hand-edit."),
     "items": items}
out = os.path.join(ROOT, "push", "666_isonade_v7_marker_key.json")
with open(out, "w") as f:
    json.dump(m, f, separators=(",", ":"))
print(f"wrote {out}: {len(items)} items")
