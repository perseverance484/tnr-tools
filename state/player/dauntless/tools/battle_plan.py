#!/usr/bin/env python3
"""Move + battle planner (director, 2026-11-10: "you need a move planner that figures out the highest value move
per round, and a battle planner that plans out remaining rounds").

Enumerates every legal AP bundle per round (AP budget incl. stun, cooldowns from cd_plan.py state, shared locks),
simulates buff timing (most tags live from NEXT round; instant: damage, pierce, seal, shield, ground effects, stun),
scores damage dealt + damage prevented, and beam-searches the next N rounds.

Usage:
  battle_plan.py BATTLE ROUND [--ap 100] [--rounds 3] [--enemy-hp 3000] [--incoming 1200]
                 [--enemy-dr 0.0] [--enemy-immune] [--enemy-pierce] [--my-hp 5050]
                 [--live "ember_taken:4,overflow:4,..."]
--live lists tags already live with the last round they cover (see TAG names below).
--incoming = expected enemy damage per round before my mitigation (their stack size).
Prints the best plan and the top single-round bundles. Advisory: read the enemy log first; this does not know
their Clear/Cleanse/pierce timing beyond the flags.
"""
import argparse
import itertools

from cd_plan import ACTIONS, LOCKS, load, ready_round

DMG_PER_POWER = 13.0  # observed 2026-11-10: Rebirth 45 power -> ~590 unbuffed
# action -> dict: dmg power (boostable), pierce flat, and tags applied (name, value, rounds, instant?)
FX = {
    "rebirth": dict(dmg=45, tags=[("absorb", .35, 3, False), ("my_given", -.15, 2, False)]),
    "shrapnel": dict(dmg=45, tags=[("afterburn", .30, 2, False)]),
    "lotus": dict(dmg=35, tags=[("buffprevent", 1, 2, False)]),
    "fury": dict(dmg=35, tags=[("recoil", .40, 2, True)]),
    "ember": dict(dmg=30, tags=[("my_given", .35, 2, False), ("en_taken", .35, 2, False)]),
    "danse": dict(dmg=23, tags=[("seal", .286, 3, True)]),
    "stormblade": dict(pierce=707, tags=[("reflect", .35, 2, False)]),
    "resonance": dict(dmg=28, tags=[("stun", 20, 2, True)]),
    "leech": dict(drain=600, tags=[("absorb", .21, 2, False)]),
    "subaku": dict(tags=[("en_given", -.25, 3, True), ("my_given", .30, 2, False)], needs_debuffable=True),
    "overflow": dict(tags=[("my_given", .82, 2, False)]),
    "thunders": dict(tags=[("my_given", .30, 2, False), ("reflect", .35, 2, False)]),
    "parry": dict(tags=[("my_given", .30, 2, False), ("parry", .20, 2, False)]),
    "eclipse": dict(tags=[("my_given", .30, 2, False), ("lifesteal", .35, 2, False)]),
    "sealnull": dict(tags=[("buffprevent", 1, 1, False)]),
    "phantom": dict(dmg=20, tags=[("my_given", .30, 2, False), ("my_dr", .20, 2, True)]),
    "shield": dict(shield=500, tags=[("absorb", .35, 2, False)]),
    "severed": dict(tags=[("en_taken", .30, 2, False), ("healcut", .5, 2, False)], needs_debuffable=True),
    "smoke": dict(tags=[("en_given", -.70, 1, False), ("my_given_smoke", -.70, 1, False)]),
    "kims": dict(tags=[("clearprevent", 1, 1, True)]),
    "pill": dict(tags=[("my_given", .15, 2, False), ("lifesteal", .20, 2, False)]),
    "panacea": dict(tags=[("my_dr", .25, 2, False)]),
    "jewel": dict(tags=[("my_given", .15, 3, False), ("my_dr", .10, 3, False)]),
    "kunai": dict(dmg=22),
    "disaster": dict(tags=[("en_taken", .20, 2, False)], needs_debuffable=True),
    "nights": dict(pierce=631, heal=200),
    "aetherion": dict(dmg=30, tags=[("en_taken", .20, 2, False)]),
    "yuki": dict(drain=400, tags=[("en_given", -.25, 2, False)], needs_debuffable=True),
    "clear": dict(special="clear"),
    "cleanse": dict(special="cleanse"),
    "replace": dict(), "defstance": dict(tags=[("my_dr", .15, 1, False)]), "offstance": dict(),
}
CAPS = {"absorb": .60, "lifesteal": .60, "reflect": .60}


def tag_value(live, name, rnd):
    """Sum (absorb/lifesteal/reflect capped) or product for multipliers of tags live in rnd."""
    vals = [v for (n, v, a, b) in live if n == name and a <= rnd <= b]
    if name in CAPS:
        return min(sum(vals), CAPS[name])
    return vals


def mult(vals):
    m = 1.0
    for v in vals:
        m *= (1 + v)
    return m


def apply(live, act, rnd):
    out = list(live)
    for (n, v, r, inst) in FX[act].get("tags", []):
        start = rnd if inst else rnd + 1
        out.append((n, v, start, start + r - 1))
    return out


def score_round(live, bundle, rnd, a):
    """Damage dealt this round + damage prevented on the enemy's turn this round."""
    for act in bundle:  # instant tags first so same-round damage sees them? No: only instants count now.
        pass
    new_live = live
    dealt = 0.0
    for act in bundle:
        fx = FX[act]
        if fx.get("needs_debuffable") and a.enemy_immune:
            continue
        given = mult(tag_value(new_live, "my_given", rnd)) * mult(tag_value(new_live, "en_taken", rnd))
        given *= mult(tag_value(new_live, "my_given_smoke", rnd))
        dealt += fx.get("dmg", 0) * DMG_PER_POWER * given * (1 - a.enemy_dr) * (
            1 + min(sum(v for v in tag_value(new_live, "afterburn", rnd)) if False else 0, 1))
        dealt += fx.get("pierce", 0) + fx.get("drain", 0) / 2
        new_live = apply(new_live, act, rnd)
    # enemy turn this round
    inc = a.incoming * mult(tag_value(new_live, "en_given", rnd))
    seal = [v for (n, v, s, e) in new_live if n == "seal" and s <= rnd <= e]
    if seal:
        inc *= (1 - seal[0])
    dr = mult([-v for v in tag_value(new_live, "my_dr", rnd)])
    inc_after = max(inc * dr, inc * 0.10)
    shield = sum(FX[x].get("shield", 0) for x in bundle)
    absorb = tag_value(new_live, "absorb", rnd)
    reflect = tag_value(new_live, "reflect", rnd)
    recoil = sum(v for (n, v, s, e) in new_live if n == "recoil" and s <= rnd <= e)
    if a.enemy_pierce:
        recoil = 0
    taken = max(0, inc_after - shield) * (1 - absorb)
    dealt += inc_after * (reflect + min(recoil, .4))
    prevented = a.incoming - taken
    return dealt, prevented, new_live


def legal_bundles(state, rnd, ap, a):
    names = [n for n in state["loadout"] if ready_round(state, n) <= rnd]
    out = []
    for k in (1, 2, 3, 4):
        for combo in itertools.combinations(names, k):
            cost = sum(ACTIONS[c][0] for c in combo)
            if cost > ap or ap - cost >= 20 and k < 4 and cost + 20 <= ap and not any(
                    ACTIONS[n][0] <= ap - cost for n in names if n not in combo) is False:
                pass
            if cost > ap:
                continue
            tags = [ACTIONS[c][2] for c in combo if ACTIONS[c][2]]
            if len(tags) != len(set(tags)):
                continue
            out.append(combo)
    return out


def sim_state(state, used):
    s = {"loadout": state["loadout"], "used": state["used"] + used}
    return s


def plan(a):
    state = load(a.battle)
    live = []
    for item in filter(None, a.live.split(",")):
        n, end = item.split(":")
        val = {"ember_taken": ("en_taken", .35), "overflow": ("my_given", .82), "ember_given": ("my_given", .35),
               "absorb": ("absorb", .35), "seal": ("seal", .286), "recoil": ("recoil", .40),
               "reflect": ("reflect", .35), "lifesteal": ("lifesteal", .35), "en_given": ("en_given", -.25)}[n]
        live.append((val[0], val[1], a.round, int(end)))
    beam = [(0.0, [], live, [], a.enemy_hp)]
    for step in range(a.rounds):
        rnd = a.round + step
        ap = a.ap if step == 0 else 100
        nxt = []
        for total, used, lv, path, ehp in beam:
            if ehp <= 0:  # already won on this path
                nxt.append((total, used, lv, path, ehp))
                continue
            st = sim_state(state, used)
            for b in legal_bundles(st, rnd, ap, a):
                cost = sum(ACTIONS[c][0] for c in b)
                d, p, nl = score_round(lv, b, rnd, a)
                waste = (ap - cost) * 4  # unspent AP is lost value
                val = d + p - waste
                left = ehp - d
                if left <= 0:
                    val += 5000 * (a.rounds - step)  # a kill now beats any later plan
                nxt.append((total + val, used + [[rnd, c] for c in b], nl,
                            path + [(rnd, b, round(d), round(p))], left))
        nxt.sort(key=lambda x: -x[0])
        beam = nxt[:60]
    best = beam[0]
    print(f"Best {a.rounds}-round plan (value {best[0]:.0f}):")
    for rnd, b, d, p in best[3]:
        print(f"  r{rnd}: {' + '.join(b)} ({sum(ACTIONS[c][0] for c in b)} AP)  dealt~{d} prevented~{p}")
    print(f"  enemy HP after plan ~{max(0, best[4]):.0f}" + ("  (KILL)" if best[4] <= 0 else ""))
    # top single-round moves
    st = sim_state(state, [])
    singles = []
    for b in legal_bundles(st, a.round, a.ap, a):
        d, p, _ = score_round(live, b, a.round, a)
        singles.append((d + p - (a.ap - sum(ACTIONS[c][0] for c in b)) * 4, b, d, p))
    singles.sort(key=lambda x: -x[0])
    print("Top moves this round:")
    for v, b, d, p in singles[:5]:
        print(f"  {' + '.join(b)}  value {v:.0f} (dealt~{d:.0f}, prevented~{p:.0f})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("battle")
    ap.add_argument("round", type=int)
    ap.add_argument("--ap", type=int, default=100)
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--enemy-hp", type=float, default=3000)
    ap.add_argument("--incoming", type=float, default=1200)
    ap.add_argument("--enemy-dr", type=float, default=0.0)
    ap.add_argument("--enemy-immune", action="store_true")
    ap.add_argument("--enemy-pierce", action="store_true")
    ap.add_argument("--my-hp", type=float, default=5050)
    ap.add_argument("--live", default="")
    plan(ap.parse_args())
