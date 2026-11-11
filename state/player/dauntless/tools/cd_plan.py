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
    "leech": (60, 7, "drain", "drain 300 x2 + absorb ~21"),
    "subaku": (40, 7, None, "ground -25% their given (instant), me +30%"),
    "overflow": (40, 7, None, "self +35 x2 (next round)"),
    "thunders": (40, 7, None, "self +dmg, reflect 35 (next round)"),
    "parry": (40, 7, None, "self +dmg, parry 20"),
    "resist": (40, 7, None, "self -30% dmg taken 2r (lvl 25), his next casts -10 potency"),
    "eclipse": (40, 7, None, "lifesteal 35 + 30 given (next round)"),
    "sealnull": (40, 7, None, "their buffs blocked next round; I can't be debuffed 2 r"),
    "phantom": (40, 6, None, "move 5 + DR ground + 30 given"),
    "shield": (40, 7, None, "500 shield (instant) + absorb 35 (next round)"),
    "severed": (40, 7, None, "-50% healing, +30% taken"),
    "smoke": (20, 10, None, "-70% given both, NEXT round"),
    "kims": (20, 10, "clearprevent", "clear/debuff prevent, next round only"),
    "pill": (20, 4, None, "+15 given, lifesteal 20"),
    "panacea": (20, 6, None, "-25% taken 2 r"),
    "jewel": (20, 6, None, "+15 given, -10 taken 3 r"),
    "kunai": (20, 4, None, "Bloodthorn Kunai (thrown, wound) - Ikazuchi ran out 2026-11-10"),
    "disaster": (20, 5, "poison", "+20% taken + poison"),
    "nights": (40, 6, "pierce", "pierce 631 + 200 heal, buff-prevent immunity"),
    "aetherion": (40, 6, None, "elemental dmg + target taken"),
    "yuki": (40, 7, "drain", "drain 200 x2 + -25% given"),
    "clear": (60, 10, "clear", "strip their positives"),
    "cleanse": (60, 10, "cleanse", "strip my negatives (not stun)"),
    "replace": (20, 2, None, "move up to 5"),
    "basicheal": (60, 5, None, "heal 600 instant (engine actions.ts)"),
    "basic": (20, 1, None, "basic attack, range 1 (finisher)"),
    "defstance": (20, 1, None, "-15% taken next round (filler)"),
    "offstance": (20, 1, None, "filler"),
}
# range to the enemy each action needs (hexes, from live jutsu/item data 2026-11-10). 0 = self/no target needed.
# opponent jutsu 4; Yuki's 3; kunai/smoke/disaster/Night's/Aetherion/Clear 4; ground (Fury/Subaku) placed within 4.
RANGE = {"basic": 1, "rebirth": 4, "shrapnel": 4, "lotus": 4, "fury": 4, "ember": 4, "danse": 4, "stormblade": 4,
         "resonance": 4, "leech": 4, "subaku": 4, "severed": 4, "sealnull": 4, "smoke": 4, "kunai": 4,
         "disaster": 4, "nights": 4, "aetherion": 4, "yuki": 3, "clear": 4}
MOVES = {"phantom": 5, "replace": 5, "step": 1}  # reposition before targeted actions
ACTIONS["step"] = (10, 0, None, "basic move 1 hex (last resort)")
# live misc.getSharedCooldowns (2026-11-10 23:58 UTC; supersedes the pinned source's flat 3): using an action with
# cooldown > 0 locks every other action carrying the SAME tag type. Clear and Cleanse are different tag types, so they
# do NOT lock each other (old "clearfam" grouping was wrong). Night's Testament is pierce + immunity (no drain).
LOCKS = {"barrier": 3, "buffprevent": 4, "cleanse": 3, "cleanseprevent": 3, "clear": 3, "clearprevent": 3,
         "consume": 3, "debuffprevent": 4, "drain": 3, "increasepoolcost": 3, "increasepotency": 3, "moveprevent": 3,
         "pierce": 3, "poison": 3, "seal": 3, "siphon": 3, "stun": 4, "summon": 3, "vamp": 3}
EXTRA_TAGS = {"kims": ("debuffprevent",), "sealnull": ("buffprevent", "debuffprevent"), "lotus": ("buffprevent",)}  # 2026-11-10 Hikuro R5: Seal refused 2 rounds after Kim's  # secondary tags that also take a shared lock
LOADOUTS = {
    "pvp1": ["rebirth", "shrapnel", "lotus", "fury", "ember", "danse", "stormblade", "subaku", "overflow",
             "thunders", "resist", "eclipse", "sealnull", "phantom", "shield",
             "smoke", "kims", "pill", "panacea", "jewel", "kunai", "nights", "aetherion",
             "clear", "cleanse", "replace", "defstance", "offstance", "basic"],
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


def tags_of(name):
    t = ACTIONS[name][2]
    return set(EXTRA_TAGS.get(name, ())) | ({t} if t else set())


def ready_round(s, name):
    ap, cd, tag, _ = ACTIONS[name]
    r = 0
    mine = tags_of(name)
    for used_round, used in s["used"]:
        if used == name:
            r = max(r, used_round + cd)
        elif used in ACTIONS:
            for t in mine & tags_of(used):
                r = max(r, used_round + LOCKS[t])
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
    elif cmd == "check":
        # cd_plan.py check BATTLE ROUND AP_AVAILABLE ACTION [...] [dist=N]  (AP_AVAILABLE = 100 - stun; dist = hexes to enemy)
        s = load(b)
        rnd, ap = int(sys.argv[3]), int(sys.argv[4])
        acts = sys.argv[5:]
        dist = next((int(x[5:]) for x in acts if x.startswith("dist=")), None)
        acts = [x for x in acts if not x.startswith("dist=")]
        total = sum(ACTIONS[a][0] for a in acts)
        bad = [f"{a} ready r{ready_round(s, a)}" for a in acts if ready_round(s, a) > rnd]
        tags = [ACTIONS[a][2] for a in acts if ACTIONS[a][2]]
        dup = sorted({t for t in tags if tags.count(t) > 1})
        ok = total <= ap and not bad and not dup
        rng = []
        if dist is not None:
            d = max(1, dist - sum(MOVES.get(a, 0) for a in acts))
            rng = [f"{a} range {RANGE[a]} < {d}" for a in acts if RANGE.get(a, 0) and RANGE[a] < d]
        ok = ok and not rng and total <= ap and not bad
        print(f"{'OK' if ok else 'NO'}: {'+'.join(acts)} = {total}/{ap} AP" + (f"; RANGE: {', '.join(rng)}" if rng else "")
              + (f"; cooldown: {', '.join(bad)}" if bad else "")
              + (f"; shared lock: {', '.join(dup)}" if dup else "")
              + ("" if total == ap or total > ap else f"; {ap - total} AP unused"))
