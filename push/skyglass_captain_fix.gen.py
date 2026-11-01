#!/usr/bin/env python3
"""The Captain fix: Unbroken Command gets a once-per-fight cooldown; the Captains chase and resist stuns (RUL-2026-10-31-091).

    python3 push/skyglass_captain_fix.gen.py   -> push/398_unbroken_command_unequip.json   (5 AI edits: Unbroken Command off)
                                               -> push/399_unbroken_command_cooldown.json  (1 jutsu edit: cooldown 2 -> 99)
                                               -> push/400_captains_reequip.json           (5 AI edits: kit back on; the
                                                  base and Faded Captain also get the approach rule and stun immunity)

Evidence: the director's log (battle lIKSZTazonCWc7MgJNHZ6, full Skyglass Wreck floor 5, level-100 solo with two pets).
The Captain's rule 8 (Hold the Line) casts Unbroken Command (hidden AI jutsu 0Y10JpChssDwFUxNRk6p3: cooldown 2, +80%
damage given and +30% offence for 99 rounds) whenever the nearest player is 3+ hexes away. The buffs stack: 11 casts,
Keelbind 4,407 (round 14) -> 400,930 (round 27). Nothing else in his list reaches past 5 hexes and he has no approach rule,
so between casts he ended his turn.

Fix (director: "We should fix it not make a copy"; "I dont want them to just stand still casting it"):
  * Unbroken Command cooldown 99: once per fight. It is an AI-type hidden jutsu held only by the five Skyglass Captains
    (The Captain, Faded Captain, the three Veteran Captains; push/377 kits). Saving a hidden jutsu and law 18 both sever
    the holders, hence 398 (off) -> 399 (edit) -> 400 (back on), the push/375-377 pattern.
  * The Captain and the Faded Captain: Stolen Form's rule (13) is cut (15 casts, no damage, harness Crownhold report) and
    move_towards_opponent ends the list (law 41's unconditional tail), with the basic attack above it gated to a player
    within 1 hex, so a player out of reach is chased. 20 rules kept.
  * The Captain and the Faded Captain: innate stunprevent 100 for 99 rounds (no Skyglass mark uses stunprevent as its
    marker, so no collision of the RUL-2026-10-28-015 kind).
Kits, rules and effects are the committed live ones: jutsus from push/377, rules/effects from push/361 (The Captain) and
push/344 (Faded Captain); nothing has edited them since. Do not hand-edit the outputs.
"""
import copy
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UC = "0Y10JpChssDwFUxNRk6p3"  # Unbroken Command
BASE, FADED = "QY69h271Nx9uHrBeR6jwW", "nR5okP-MiRsnSpiJQ8CM-"
STOLEN_FORM_RULE = 13
INJECTABLE = False  # law 20: sent explicitly; the live value (tnr_results_1792900120886.json), re-checked by push/397
ID = re.compile(r"^[A-Za-z0-9_-]{21}$")
STUNPREVENT = {"type": "stunprevent", "power": 100, "rounds": 99, "target": "INHERIT", "appearSfx": "",
               "direction": "offence", "calculation": "percentage", "description": "Prevents being stunned",
               "disappearSfx": "", "powerPerLevel": 0, "appearAnimation": "", "staticAnimation": "",
               "staticAssetPath": "", "disappearAnimation": ""}
MOVE = {"conditions": [], "action": {"type": "move_towards_opponent", "description": "Close on the nearest player (none in reach)",
                                     "target": "CLOSEST_OPPONENT"}}


def load(n):
    return json.load(open(os.path.join(ROOT, "push", n)))


def kits():
    out = {}
    for it in load("377_skyglass_fx_reequip.json")["items"]:
        js = it["data"].get("jutsus", [])
        if UC in js:
            out[it["targetId"]] = (it["name"].split(":")[0], js)
    assert len(out) == 5 and BASE in out and FADED in out, out
    return out


def rules_effects():
    base = next(it["data"] for it in load("361_skyglass_crew_upgrade.json")["items"] if it.get("targetId") == BASE)
    faded = next(it["data"] for it in load("344_skyglass_copies_1.json")["items"] if it.get("srcId") == "sg344_faded-the-captain")
    out = {}
    for tid, d in ((BASE, base), (FADED, faded)):
        rules = copy.deepcopy(d["rules"])
        assert len(rules) == 20 and rules[STOLEN_FORM_RULE]["action"]["description"].startswith("Stolen Form"), tid
        assert rules[8]["action"]["jutsuId"] == UC and rules[-1]["action"]["jutsuId"] == "basicAttack", tid
        for r in rules:
            j = r["action"].get("jutsuId")
            assert j is None or j == "basicAttack" or ID.match(j), (tid, j)
        del rules[STOLEN_FORM_RULE]
        # law 41: the last rule is unconditional, so the basic attack takes an adjacency gate and the chase ends the list
        rules[-1]["conditions"] = [{"type": "player_within_range", "description": "", "minRange": 0, "maxRange": 1}]
        rules.append(copy.deepcopy(MOVE))
        assert len(rules) == 20
        effects = copy.deepcopy(d["effects"])
        assert not any(e["type"] == "stunprevent" for e in effects)
        out[tid] = (rules, effects + [copy.deepcopy(STUNPREVENT)])
    return out


def write(n, slug, note, items):
    p = os.path.join(ROOT, f"push/{n}_{slug}.json")
    with open(p, "w") as f:
        json.dump({"_note": note + " Generated by push/skyglass_captain_fix.gen.py; do not hand-edit.", "items": items},
                  f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{n}_{slug}.json: {len(items)} items")


def main():
    K, RE = kits(), rules_effects()
    write(398, "unbroken_command_unequip",
          "push/398, step 1 of 3 (RUL-2026-10-31-091): Unbroken Command off its five holders before its edit (law 18; a "
          "hidden jutsu's save severs its holders). Kits from push/377 minus Unbroken Command.",
          [{"entity": "ai", "slot": "edit", "targetId": t, "name": f"{n}: Unbroken Command off",
            "data": {"jutsus": [j for j in js if j != UC]}} for t, (n, js) in K.items()])
    write(399, "unbroken_command_cooldown",
          "push/399, step 2 of 3 (RUL-2026-10-31-091): Unbroken Command cooldown 2 -> 99, once per fight (its 99-round buffs "
          "stacked: 11 casts, Keelbind 400,930). Fetch-merge edit sending only cooldown.",
          [{"entity": "jutsu", "slot": "edit", "targetId": UC, "name": "Unbroken Command: once per fight",
            "data": {"cooldown": 99, "injectableInBattle": INJECTABLE}}])
    items = []
    for t, (n, js) in K.items():
        data = {"jutsus": js}
        if t in RE:
            data["rules"], data["effects"] = RE[t]
        items.append({"entity": "ai", "slot": "edit", "targetId": t,
                      "name": f"{n}: kit back on" + (", approach rule, stun immunity" if t in RE else ""), "data": data})
    write(400, "captains_reequip",
          "push/400, step 3 of 3 (RUL-2026-10-31-091): the push/377 kits back on all five holders. The Captain and the Faded "
          "Captain also: Stolen Form's rule cut, the basic attack gated to a player within 1, move_towards_opponent as the unconditional last rule (20 rules), innate "
          "stunprevent 100 for 99 rounds.", items)


if __name__ == "__main__":
    main()
