#!/usr/bin/env python3
"""Enemy move predictor (director, 2026-11-10: "Your issue is you're not running any kind of predictions for the
enemy moves, so you're always behind").

Per-opponent profile = kit (AP, cooldown, role tags) + recorded fights (their actions per round). In a live fight
log their actions each round, then `predict` gives: which of their actions are off cooldown, their most likely
next bundle (round-number habit + what they did last round, from past fights), the threat it carries, and my
pre-planned counter. Run it during THEIR turn, then pre-check my primary + backup with cd_plan.py.

Usage:
  enemy_model.py OPP new BATTLE               start a live log
  enemy_model.py OPP log BATTLE ROUND a,b,c   record their actions in ROUND (kit short names)
  enemy_model.py OPP predict BATTLE ROUND     predict their bundle for ROUND
  enemy_model.py OPP kit                      list kit short names
"""
import collections
import json
import sys

# role tags: burst (big hit), buff (+given/-taken on self, live next round), immune (debuff immunity),
# recoil_me (recoil on me), stun, pierce, clear, drain, heal, shield, pull, kite, smoke, debuff_me, absorb
PROFILES = {
    "luka": {
        "ap": 100,
        "kit": {
            "stone": (60, 7, ["burst", "lifesteal"]), "veil": (60, 7, ["burst", "absorb"]),
            "resward": (60, 7, ["burst", "recoil_me"]), "tranquil": (60, 7, ["burst", "shield", "debuff_me"]),
            "dki": (60, 7, ["burst", "buff", "wound"]), "resonance": (60, 7, ["stun", "burst"]),
            "leech": (60, 7, ["drain", "absorb"]), "stonepillar": (60, 7, ["burst"]),
            "echo": (40, 7, ["stun", "recoil_me"]), "vacuum": (40, 7, ["pull", "debuff_me"]),
            "middleguard": (40, 7, ["buff", "immune"]), "eclipse": (40, 7, ["buff", "lifesteal"]),
            "overflow": (40, 7, ["buff"]), "eternaldark": (40, 7, ["debuff_me", "buff"]),
            "adamantine": (40, 7, ["buff", "shield"]), "phantom": (40, 6, ["kite", "buff"]),
            "ironbo": (40, 6, ["burst", "debuff_me"]), "nights": (40, 6, ["pierce", "drain"]),
            "clear": (60, 10, ["clear"]), "cleanse": (60, 10, ["cleanse"]),
            "pill2": (20, 4, ["buff"]), "panacea": (20, 6, ["buff"]), "smoke": (20, 10, ["smoke"]),
            "kims": (20, 10, ["immune"]), "healitem": (20, 6, ["heal", "buff"]), "replace": (20, 2, ["kite"]),
        },
        "fights": [
            # vs dauntless 2026-11-10 15:18 (he won)
            [["stone", "pill2", "panacea"], ["resward", "ironbo"], ["veil", "stonepillar", "replace"],
             ["clear", "echo"], ["eclipse", "middleguard", "pill2"], ["tranquil", "vacuum"], ["leech", "overflow"],
             ["stone", "ironbo"], ["nights", "eternaldark", "panacea"], ["dki"]],
            # spar vs 4qua 2026-11-10 15:30
            [["phantom", "ironbo", "pill2"], ["veil", "middleguard"], ["echo", "replace", "adamantine"],
             ["stone", "overflow", "replace"], ["nights", "leech"], ["vacuum", "eclipse", "panacea"],
             ["tranquil", "phantom"], ["resonance", "eternaldark"], ["veil", "pill2"], ["resward", "smoke"]],
            # vs dauntless 2026-11-10 15:47 (he won)
            [["stone", "pill2", "panacea"], ["resonance", "ironbo"], ["leech", "adamantine"],
             ["overflow", "eclipse", "kims"], ["nights", "dki"], ["healitem", "echo", "smoke"],
             ["vacuum", "pill2", "phantom"], ["tranquil"]],
        ],
    },
}

COUNTERS = {
    "burst": "Big hit due: Fury recoil ground if his pierce is on cooldown, else Chakra Shield (instant) / Subaku "
             "(instant, not through immunity) / seal (Danse) - keep absorb up.",
    "buff": "He is stacking for next round: Seal of Nullification NOW (blocks buffs applied next round), or plan Clear "
            "for my next turn once the stack is live.",
    "immune": "Debuff immunity coming: Subaku/Smoke/Disaster will fail that round; seal and Clear still work.",
    "recoil_me": "Recoil on me likely: next turn deal pierce (Stormblade/Night's) or drain, not big hits; or Cleanse.",
    "stun": "Stun likely: pre-plan an 80-AP bundle for my next turn (60+20 / 40+40).",
    "pierce": "Pierce available: don't rely on shield/recoil this round; absorb still works; smoke rounds are when he "
              "pierces.",
    "clear": "Clear available: don't stack my buffs into his turn unprotected; Dr. Kim's first, or buff after he uses it.",
    "drain": "Drain coming: flat HP loss through DR; Cleanse removes it.",
    "kite": "He repositions off my ground: keep Replacement/Phantom ready; don't drop ground effects he can walk out of.",
    "pull": "Pull + damage-taken debuff: expect his burst at close range next.",
    "smoke": "Smoke: the next round is dead for damage; he pierces in it. Set up, keep absorb.",
}


def path(opp, b):
    return f"/tmp/enemy_{opp}_{b}.json"


def threat_features(opp, b, rnd):
    """For policy.py: (burst, buff, stun, immune, pierce_ready, clear_ready) in 0..1; zeros if not profiled."""
    opp = (opp or "").lower()
    if opp not in PROFILES:
        return [0.0] * 6
    bundle, threats, ready, kit, _ = _predict(opp, b, rnd)
    has = lambda t: float(any(ready[a] and t in kit[a][2] for a in kit))
    dmg = threats.get("burst") or threats.get("pierce") or threats.get("drain")  # any damage they are likely to land
    return [float(bool(dmg)), float(bool(threats.get("buff"))), float(bool(threats.get("stun"))),
            float(bool(threats.get("immune"))), has("pierce"), has("clear")]


def _predict(opp, b, rnd):
    prof = PROFILES[opp]
    kit = prof["kit"]
    try:
        live = json.load(open(path(opp, b)))
    except FileNotFoundError:
        live = {}
    used = {int(k): v for k, v in live.items()}
    ready = {}
    for a, (ap, cd, _) in kit.items():
        last = max([r for r, acts in used.items() if a in acts], default=-99)
        ready[a] = last + cd <= rnd
    # habit scores
    score = collections.Counter()
    prev = used.get(rnd - 1, [])
    for fight in prof["fights"]:
        if rnd - 1 < len(fight):
            for a in fight[rnd - 1]:
                score[a] += 2
        for i in range(1, len(fight)):
            if set(prev) & set(fight[i - 1]):
                for a in fight[i]:
                    score[a] += 1
    cands = sorted((s, a) for a, s in score.items() if ready.get(a) and a in kit)
    cands.reverse()
    bundle, ap = [], prof["ap"]
    for s, a in cands:
        if kit[a][0] <= ap:
            bundle.append(a)
            ap -= kit[a][0]
    threats = collections.Counter(t for a in bundle for t in kit[a][2])
    return bundle, threats, ready, kit, cands


def predict(opp, b, rnd):
    bundle, threats, ready, kit, cands = _predict(opp, b, rnd)
    print(f"{opp} round {rnd}: likely {' + '.join(bundle) or '?'}  (habit scores: "
          + ", ".join(f"{a}:{s}" for s, a in cands[:6]) + ")")
    print("off cooldown: " + ", ".join(a for a in kit if ready[a]))
    print("on cooldown: " + ", ".join(a for a in kit if not ready[a]))
    for t in ["burst", "buff", "immune", "recoil_me", "stun", "pierce", "clear", "drain", "pull", "smoke", "kite"]:
        if threats.get(t) or (t in ("pierce", "clear") and any(ready[a] and t in kit[a][2] for a in kit)):
            print(f"  [{t}] {COUNTERS[t]}")


if __name__ == "__main__":
    opp, cmd = sys.argv[1], sys.argv[2]
    if cmd == "kit":
        print(", ".join(f"{a}({v[0]})" for a, v in PROFILES[opp]["kit"].items()))
    elif cmd == "new":
        json.dump({}, open(path(opp, sys.argv[3]), "w"))
        print("tracking", opp, sys.argv[3])
    elif cmd == "log":
        b, rnd, acts = sys.argv[3], sys.argv[4], sys.argv[5].split(",")
        d = json.load(open(path(opp, b)))
        for a in acts:
            assert a in PROFILES[opp]["kit"], a
        d[rnd] = acts
        json.dump(d, open(path(opp, b), "w"))
        predict(opp, b, int(rnd) + 1)
    elif cmd == "predict":
        predict(opp, sys.argv[3], int(sys.argv[4]))
