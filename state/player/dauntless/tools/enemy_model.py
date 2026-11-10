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
            "kunai": (20, 4, ["burst"]),
            # 2026-11-10 fights 4-6 (ids below): AP fitted from his full turns
            "potency": (40, 7, ["buff"]),            # 8NfE: +20.8% given, +10 tag power (Water)
            "absorbstack": (40, 7, ["buff", "absorb"]),  # Xd1n: +40% given, absorb 40 (his R1 + R7-10 opener)
            "shieldbreak": (60, 7, ["burst", "pierce", "wound"]),  # J6HT: ~735, pierces/destroys my shield, wound 182
            "absorbhit": (60, 7, ["burst", "absorb"]),  # qe40: ~450-600 + absorb 30-40
            "lsdebuff": (40, 7, ["debuff_me", "lifesteal"]),  # GGms: me +30% taken, LS 35
            "afterburnme": (20, 6, ["debuff_me"]),  # mlCQ: me +15% taken, afterburn 20
            "draingiven": (40, 7, ["drain", "buff"]),  # WoaNq: drain 150 x2, +30% elemental given
            "afterburnground": (60, 7, ["burst"]),  # oh9C: ~500-630 + afterburn ground
            "lsshield": (60, 7, ["lifesteal", "shield"]),  # dKeY: LS 35 + small shield
            "decree": (40, 6, ["burst", "debuff_me"]),  # PhP5 Captain's Decree: ~400, me +20% taken, afterburn 10
        },
        # action ids seen in battle entries (2026-11-10), so live logs map straight to kit names
        "ids": {"FytS2iqFInf1go6WhOvUU": "dki", "rsc2uO5QuffXzejfhwF_F": "panacea", "eUWCeXAqVdIFHfUpmxQWD": "eternaldark",
                "osJq3k77YPGoFWgof12FQ": "nights", "eHXoPCV2QdZuKEs2ykGzS": "ironbo", "CTYkpwuoqS9mJkOB3Lm8U": "stone",
                "TtYPd-LcXKeK3sMuhq1TP": "smoke", "e2eC-x4UXc5m6QexNbx8w": "overflow", "0nIgI7oNn-PSesn8T8kGl": "leech",
                "QE05DhEhb09fhnC1573Vj": "vacuum", "KPq6qR4CQphpiMJQiK3sa": "tranquil", "clear": "clear", "cleanse": "cleanse",
                "nThwqBAKNrl1_4UTL-D_m": "pill2", "r2QGirLcf1lpWvYCHS60g": "middleguard", "ou7VyChQ-SFCm8T8yGS7I": "eclipse",
                "VHU4A-vVGvUFTasBelWP2": "echo", "replacementTechnique": "replace", "l6iUf3mc7LZQQEDDif1zW": "veil",
                "8Un5MzB4EiECVOSLwc9bf": "resward", "6DnJn4x6LWWXtBu7UZybb": "kims", "i4lGrYY5HNN2Q2GPToKUS": "adamantine",
                "XmFscRje4vUzUorOI5plt": "healitem", "u9mXSgVW_QjkRzCejGXZ1": "kunai",
                "8NfEZTMQDK25fgerqjtXB": "potency", "Xd1nYH0TryplDPd6fORFm": "absorbstack",
                "J6HTCnlUw84zOyaf9xxmD": "shieldbreak", "qe40i5VoewLPvjJfTI4Vi": "absorbhit",
                "GGms9iTcZq_gICEuZYF2Q": "lsdebuff", "mlCQd6nbegRsYiO28cTPp": "afterburnme",
                "WoaNqRnyBBXRwmKbq8h1D": "draingiven", "oh9CmLX8nltc2WfrkvswH": "afterburnground",
                "dKeYkS3A9dB_eRPoBuFUJ": "lsshield", "PhP5ZEF5iVa97jcumJ15c": "decree",
                "lXlcfj4ZrhX8mzkOgy0oI": "resward", "GAyHRgaa1lkYGhE9WxlRL": "phantom",
                "VHU4A-vVGvUFTasBelWP2": "echo", "eUWCeXAqVdIFHfUpmxQWD": "eternaldark",
                "r2QGirLcf1lpWvYCHS60g": "middleguard", "FytS2iqFInf1go6WhOvUU": "dki"},
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
            # vs dauntless 2026-11-10 19:14 (he attacked; won R6)
            [["replace", "potency", "vacuum"], ["resward", "absorbstack"], ["middleguard", "lsdebuff", "pill2"],
             ["dki", "draingiven"], ["shieldbreak", "decree"], ["afterburnground", "kunai"]],
            # vs dauntless 2026-11-10 19:24 (he attacked; won R11)
            [["panacea", "absorbstack", "potency"], ["middleguard", "absorbhit"], ["lsdebuff", "resward"],
             ["dki", "decree"], ["vacuum", "afterburnme", "phantom"], ["lsshield", "kunai", "kims"],
             ["pill2", "smoke"], ["shieldbreak", "draingiven"], ["eternaldark", "echo", "afterburnme"],
             ["potency", "absorbstack", "panacea"], ["afterburnground", "decree"]],
            # vs dauntless 2026-11-10 19:35 (I attacked, PvP 2; won R11)
            [["potency", "absorbstack", "pill2"], ["middleguard", "lsdebuff"], ["shieldbreak", "afterburnme"],
             ["dki", "kunai", "smoke"], ["clear", "vacuum"], ["resward", "panacea", "pill2"],
             ["potency", "absorbhit"], ["absorbstack", "afterburnme", "draingiven"], ["eternaldark", "decree"],
             ["shieldbreak", "replace"]],
        ],
        # Pattern (6 fights): R1 always buffs (potency + absorbstack [+pill/panacea/vacuum]); R2 Middle Guard
        # (debuff-immune R3, DR 35, +35 given) + a debuff/LS piece; R3-R5 burst (resward / shieldbreak / dki) with
        # debuffs on me; Clear once (~R5) right after I buff; Smoke once (R4-R7); re-buff cycle ~R7-R10;
        # shieldbreak (pierces Chakra Shield) every 7 rounds from R3-R5.
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
    "absorb": "Absorb live on him: hits heal him back 40-60%. Clear it, or deal drains (Yuki/Leech/Night's drain are not absorbed) and pierce; don't spend 60-AP bursts into it.",
    "lifesteal": "His lifesteal is up: Severed Pulse (-50% healing) before trading hits; recoil/reflect feed his LS.",
    "wound": "Wound on me next: keep Cleanse for the round my HP is under ~2x the tick (it removes wound before it ticks).",
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
    for t in ["burst", "buff", "immune", "recoil_me", "stun", "pierce", "clear", "drain", "pull", "smoke", "kite",
              "absorb", "lifesteal", "wound"]:
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
        ids = PROFILES[opp].get("ids", {})
        acts = [ids.get(a, a) for a in acts if ids.get(a, a) not in ("move", "defensiveStance", "offensiveStance")]
        for a in acts:
            assert a in PROFILES[opp]["kit"], a
        d[rnd] = acts
        json.dump(d, open(path(opp, b), "w"))
        predict(opp, b, int(rnd) + 1)
    elif cmd == "predict":
        predict(opp, sys.argv[3], int(sys.argv[4]))
