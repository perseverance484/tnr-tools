#!/usr/bin/env python3
"""Job 667, HIDDEN: Isonade v8. Every chain marker becomes a tag no player effect can put on Isonade.

The director (2026-11-20 00:25Z, "Key all five"): key Black Water Floods, Swell Rises, Brine Brand, Breaker and Tide
the same way the Undertow was keyed in job 666, so no player debuff sets off a move out of turn.

Why these types (state/flooded_stores_build/isonade_v8_inert_markers.md):
- The old markers (seal, increasepoolcost, healprevent, increasecooldown, fleeprevent, elementalseal) are all
  effects that player jutsu or items can put on an enemy (catalog harvest tnr_results_1794368544997). has_effect sums
  every effect of a type from any caster, so a player seal set off Black Water Floods, and so on.
- The new types are out-of-combat tags (regeneration, repair, marriage slots, reskin slots, item-variant unlock, skill
  grant). The jutsu validator accepts them, combat applies them as plain timed effects with no handler, and no visible
  player jutsu or item can put one on an enemy. Clear and Cleanse match neither list (isPositiveUserEffect,
  isNegativeUserEffect), so a player's Clear or Cleanse, or Isonade's own Deep cleanse, cannot cut a chain either.
- Each keeps its power (no prevent-style reset), so the rules read them at 100.

Changes (power 100, same rounds, SELF, same "Isonade's rotation" text and animation fields):
  Barnacle Hide   fleeprevent 100 (2)              -> noncombatgainskill       rule 13 Tide
  Tide Draws Back increasecooldown 1 (2)           -> unlockitemvariant        rule 12 Breaker
  Harpoon Line    healprevent 100 (2)              -> marriageslotincrease     rule 10 Brine Brand
  Brine Brand     elementalseal 100 (2)            -> increaseregeneration     rule 9  Undertow
  Omen: B. Water  seal 100 (2) kept, + noncombatincreasereskins           rule 3  Black Water Floods
                  (the self seal stays: it switches off Isonade's hull DR and stun guard for the Black Water window,
                  because AI passives are realised as bloodline effects and a seal blocks those; only the key moves)
  Swell Builds    increasepoolcost 100% Health (3) -> repair                   rules 5 Swell Rises, 4 Tidal Bore (+robprevent)
Unchanged: disarm (The Deep), weakness (Harpoon after a hit), robprevent (Swell Rises; positive, no player source).
Law 18: the six off Isonade (10), edited (20), the full live kit back on (30), rules (40).
Rollback: state/stolen_stores_captures/isonade_v8_live_2026-11-20 (read back 2026-11-20, same as post-666).

Usage: python3 push/667_isonade_v8_inert_markers.gen.py
Writes push/667_isonade_v8_inert_markers.json. Do not hand-edit.
"""
import copy
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/isonade_v8_live_2026-11-20")
ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
DROP = {"id", "createdAt", "updatedAt"}
KEEP = ("rounds", "target", "description", "direction", "powerPerLevel", "animationScale", "appearAnimation",
        "staticAnimation", "staticAssetPath", "disappearAnimation", "appearSfx", "disappearSfx")
EXTRA = {"increaseregeneration": {}, "repair": {}, "marriageslotincrease": {"rank": "D"},
         "noncombatincreasereskins": {"rank": "D"}, "unlockitemvariant": {"variantId": None},
         "noncombatgainskill": {"skillId": ""}}

# (jutsu id, capture, old marker type, old rounds, new type, rule index, rule action jutsu)
CHAIN = [
    ("YNaD1O971Ymn0XKNTIynt", "jutsu_barnacle_hide.json", "fleeprevent", 2, "noncombatgainskill", 13, "BKfXoZ6Y3YLSoH4WzXvq6"),
    ("BKfXoZ6Y3YLSoH4WzXvq6", "jutsu_tide.json", "increasecooldown", 2, "unlockitemvariant", 12, "z97QVlWZs8uqYcWBQkk-9"),
    ("CgmXwQ1PoWi0Y5h7lSEUj", "jutsu_harpoon.json", "healprevent", 2, "marriageslotincrease", 10, "csR7tJYXd6rkQp2oGi7ai"),
    ("csR7tJYXd6rkQp2oGi7ai", "jutsu_brine.json", "elementalseal", 2, "increaseregeneration", 9, "49k-zlISWsouayutA7kJr"),
    ("vGtG2yV8WqaRTHh-19nVg", "jutsu_omen_black_water.json", "seal", 2, "noncombatincreasereskins", 3, "EclVg14en924oVI7WtZ6M"),
    ("Aj0gB5-yP38_hSIMVnsXO", "jutsu_swell_builds.json", "increasepoolcost", 3, "repair", 5, "0eIhyLEPAN1KsSs7P3Kzd"),
]
BORE_RULE, BORE = 4, "5_izyS8vstAh6Yt9RPOwz"
OMEN = "vGtG2yV8WqaRTHh-19nVg"


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


def has(t, thr=100):
    return {"type": "has_effect", "threshold": thr, "effectType": t, "description": "AI is affected by a specific effect"}


ai = cap("getAi_isonade.json")
assert ai["userId"] == ISONADE
live_kit = [j["jutsuId"] for j in ai["jutsus"]]
assert len(live_kit) == 18 and all(j["equipped"] for j in ai["jutsus"]), live_kit

edits = []
for jid, capfile, old, rounds, new, _, _ in CHAIN:
    rec = cap(capfile)
    assert rec["id"] == jid and rec["hidden"] is True and jid in live_kit, capfile
    idx = [i for i, e in enumerate(rec["effects"]) if e["type"] == old]
    assert len(idx) == 1, (capfile, old)
    e = rec["effects"][idx[0]]
    assert e["target"] == "SELF" and e["rounds"] == rounds and e["description"] == "Isonade's rotation", (capfile, e)
    tag = {"type": new, "power": 100, "calculation": "static", **{k: e[k] for k in KEEP if k in e}, **EXTRA[new]}
    data = {k: v for k, v in copy.deepcopy(rec).items() if k not in DROP}
    if jid == OMEN:
        # The omen keeps its self seal: it is what switches off Isonade's hull DR and stun guard for the Black Water
        # window (passives are realised as bloodline effects, and a seal blocks those). Only the key moves.
        tag.update({k: "" for k in ("appearAnimation", "appearSfx")})
        data["effects"].append(tag)
        assert len(data["effects"]) == len(rec["effects"]) + 1
    else:
        data["effects"][idx[0]] = tag
        assert len(data["effects"]) == len(rec["effects"])
    edits.append((jid, rec["name"], old, new, data))

# No two chain markers share a type, and none of the new types appears anywhere else in the kit.
new_types = [c[4] for c in CHAIN]
assert len(set(new_types)) == len(new_types)
for j in ai["jutsus"]:
    if j["jutsuId"] in {c[0] for c in CHAIN}:
        continue
    assert not {e["type"] for e in j["jutsu"]["effects"]} & set(new_types), j["jutsu"]["name"]

prof = cap("aiProfile_isonade.json")
rules = copy.deepcopy(prof["rules"])
assert len(rules) == 20 and prof["includeDefaultRules"] is False
for _, _, old, _, new, ri, action in CHAIN:
    r = rules[ri]
    assert r["action"]["jutsuId"] == action, (ri, r["action"])
    want_old = "elementalseal" if old == "elementalseal" else old
    assert [c["effectType"] for c in r["conditions"]] == [want_old], (ri, r["conditions"])
    r["conditions"] = [has(new)]
assert rules[BORE_RULE]["action"]["jutsuId"] == BORE
assert [c["effectType"] for c in rules[BORE_RULE]["conditions"]] == ["increasepoolcost", "robprevent"]
rules[BORE_RULE]["conditions"] = [has("repair"), has("robprevent", 1)]
for r in rules:
    for c in r["conditions"]:
        assert 0 <= c.get("threshold", 0) <= 100 and 0 <= c.get("value", 0) <= 100, c
used = {c["effectType"] for r in rules for c in r["conditions"] if c["type"] == "has_effect"}
assert used == set(new_types) | {"disarm", "shield", "weakness", "robprevent"}, used

edited = [e[0] for e in edits]
items = [{"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
          "name": f"Isonade: {len(edited)} chain jutsu off (law 18)",
          "data": {"jutsus": [j for j in live_kit if j not in edited]}}]
for jid, name, old, new, data in edits:
    items.append({"entity": "jutsu", "slot": "edit", "targetId": jid, "phase": 20,
                  "name": (f"{name}: adds self marker {new} 100 (keeps its seal)" if jid == OMEN else
                           f"{name}: self marker {old} -> {new} 100"), "data": data})
items += [
    {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
     "name": f"Isonade: live kit back on ({len(live_kit)})", "data": {"jutsus": live_kit}},
    {"entity": "aiProfile", "slot": "edit", "targetId": ISONADE, "phase": 40,
     "name": "Isonade: chain rules read the inert markers at 100 (20 rules)",
     "data": {"rules": rules, "includeDefaultRules": False}},
]
m = {"_note": ("push/667, HIDDEN: Isonade v8. The six chain markers become out-of-combat tag types no player effect "
               "can put on Isonade; rules 3, 4, 5, 9, 10, 12 and 13 read them at 100. Law 18. Generated by "
               "push/667_isonade_v8_inert_markers.gen.py; do not hand-edit."),
     "items": items}
out = os.path.join(ROOT, "push", "667_isonade_v8_inert_markers.json")
with open(out, "w") as f:
    json.dump(m, f, separators=(",", ":"))
print(f"wrote {out}: {len(items)} items")
