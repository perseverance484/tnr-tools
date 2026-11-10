#!/usr/bin/env python3
"""PvP cooldown planner: what is usable this round and the next two (director, 2026-11-10: "Dont lose turns.
Cooldown planning and awareness should already be done. You should be thinking 1-2 turns out").

Usage:
  cd_plan.py new BATTLE [pvp1|pvp2]          start tracking a battle with a loadout
  cd_plan.py use BATTLE ROUND ACTION [...]   record actions I used in ROUND (short names below)
  cd_plan.py show BATTLE ROUND               print usable now / next / +2, with AP and lock notes
State: /tmp/cd_plan_<BATTLE>.json. Rule (observed 2026-11-10): used in round N with cooldown C -> usable from
round N + C. Shared tag locks (combat_rules.md): pierce 3, stun 4, clear/cleanse family 3 (on top of own cd).
"""
import json
import sys

# short name: (AP, cooldown, shared-lock tag or None, note)
ACTIONS = {
    "rebirth": (60, 8, None, "dmg + absorb 35 (3 r, from next round)"),
    "shrapnel": (60, 7, None, "AoE dmg + afterburn"),
    "lotus": (60, 7, None, "dmg + buff prevent"),
    "fury": (60, 7, None, "ground recoil ~40%, instant, uncleansable"),
    "ember": (60, 7, None, "self +35 given, target +35 taken"),
    "danse": (60, 8, "seal", "dmg + bloodline seal (instant)"),
    "stormblade": (60, 7, "pierce", "pierce 707 + reflect 35 (reflect from next round)"),
    "resonance": (60, 7, "stun", "dmg + stun"),
    "leech": (60, 7, None, "drain 300 x2 + absorb ~21"),
    "subaku": (40, 7, None, "ground -25% their given (instant), me +30%"),
    "overflow": (40, 7, None, "self +35 x2 (next round)"),
    "thunders": (40, 7, None, "self +dmg, reflect 35 (next round)"),
    "parry": (40, 7, None, "self +dmg, parry 20"),
    "eclipse": (40, 7, None, "lifesteal 35 + 30 given (next round)"),
    "sealnull": (40, 7, None, "their buffs blocked next round; I can't be debuffed 2 r"),
    "phantom": (40, 6, None, "move 5 + DR ground + 30 given"),
    "shield": (40, 7, None, "500 shield (instant) + absorb 35 (next round)"),
    "severed": (40, 7, None, "-50% healing, +30% taken"),
    "smoke": (20, 10, None, "-70% given both, NEXT round"),
    "kims": (20, 10, None, "clear/debuff prevent"),
    "pill": (20, 4, None, "+15 given, lifesteal 20"),
    "panacea": (20, 6, None, "-25% taken 2 r"),
    "jewel": (20, 6, None, "+15 given, -10 taken 3 r"),
    "kunai": (20, 4, None, "thrown dmg"),
    "disaster": (20, 5, None, "+20% taken + poison"),
    "nights": (40, 6, "pierce", "pierce 631 + 200 heal, buff-prevent immunity"),
    "aetherion": (40, 6, None, "elemental dmg + target taken"),
    "yuki": (40, 7, None, "drain 200 x2 + -25% given"),
    "clear": (60, 10, None, "strip their positives"),
    "cleanse": (60, 10, None, "strip my negatives (not stun)"),
    "replace": (20, 2, None, "move up to 5"),
    "defstance": (20, 1, None, "-15% taken next round (filler)"),
    "offstance": (20, 1, None, "filler"),
}
LOCKS = {"pierce": 3, "stun": 4, "seal": 3}
LOADOUTS = {
    "pvp1": ["rebirth", "shrapnel", "lotus", "fury", "ember", "danse", "stormblade", "subaku", "overflow",
             "thunders", "parry", "eclipse", "sealnull", "phantom", "shield",
             "smoke", "kims", "pill", "panacea", "jewel", "kunai", "nights", "aetherion",
             "clear", "cleanse", "replace", "defstance", "offstance"],
    "pvp2": ["rebirth", "leech", "severed", "fury", "ember", "danse", "stormblade", "subaku", "overflow",
             "thunders", "resonance", "eclipse", "sealnull", "phantom", "shield",
             "smoke", "kims", "pill", "panacea", "jewel", "disaster", "nights", "yuki",
             "clear", "cleanse", "replace", "defstance", "offstance"],
}


def path(b):
    return f"/tmp/cd_plan_{b}.json"


def load(b):
    with open(path(b)) as f:
        return json.load(f)


def save(b, s):
    with open(path(b), "w") as f:
        json.dump(s, f)


def ready_round(s, name):
    ap, cd, tag, _ = ACTIONS[name]
    r = 0
    for used_round, used in s["used"]:
        if used == name:
            r = max(r, used_round + cd)
        if tag and ACTIONS[used][2] == tag and used != name:
            r = max(r, used_round + LOCKS[tag])
    return r


def show(b, rnd):
    s = load(b)
    for off, label in ((0, "NOW"), (1, "NEXT"), (2, "+2")):
        R = rnd + off
        avail = [n for n in s["loadout"] if ready_round(s, n) <= R]
        print(f"round {R} ({label}): " + ", ".join(f"{n}({ACTIONS[n][0]})" for n in avail))
    waiting = sorted((ready_round(s, n), n) for n in s["loadout"] if ready_round(s, n) > rnd)
    print("on cooldown: " + ", ".join(f"{n}->r{r}" for r, n in waiting))


if __name__ == "__main__":
    cmd, b = sys.argv[1], sys.argv[2]
    if cmd == "new":
        save(b, {"loadout": LOADOUTS[sys.argv[3] if len(sys.argv) > 3 else "pvp1"], "used": []})
        print("tracking", b)
    elif cmd == "use":
        s = load(b)
        rnd = int(sys.argv[3])
        for a in sys.argv[4:]:
            assert a in ACTIONS, a
            s["used"].append([rnd, a])
        save(b, s)
        show(b, rnd)
    elif cmd == "show":
        show(b, int(sys.argv[3]))
