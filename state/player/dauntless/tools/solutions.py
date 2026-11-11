#!/usr/bin/env python3
"""Solution library (director 2026-11-11: "a library of 'solutions' to things we encounter, like best scored moves or
answers to opponents. A way to quickly pull the correct response without having to mull it over").

1. Situation key: a position compressed to what decides the right answer: turn order (P1 = I act first this round,
   so his reply lands before my new tags; P2 = my tags cover his next turn), both HP bands, my next-hit and his
   next-hit multiplier bands, immunities, ground, his live buff count, his Clear / pierce, my key cooldowns, a copier
   in his kit.
2. Solver: for a position from a simulated fight, planner2's top candidates are each played out to the end several
   times (fightsim: planner2 for me with a fast shortlist, his bot sampling his lines), with common random seeds
   across candidates. The candidate with the best mean outcome is the solution. This is where turn order, damage
   windows and cadence get learned: a move is judged by how the fight actually goes after it, not by a one-turn score.
3. Library: solutions.json {key: {best, votes, value, alts, why}}; repeated keys vote.
4. Lookup at play time (planner2.rank): ~1 ms; a confident entry gets a bonus if that bundle is legal. The live
   simulation and guards still check it.

Usage:
  solutions.py build [--fights 6] [--rollouts 4] [--cands 6]   simulate fights, solve each of my turns, merge
  solutions.py show [N]                                        library summary
Offline only; run under `nice`.
"""
import argparse
import copy
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import planner2 as P2  # noqa: E402

LIB = os.path.join(HERE, "solutions.json")
PIERCE = ("stormblade", "nights")


# ------------------------------------------------------------------ situation key
def band(x, edges):
    for i, e in enumerate(edges):
        if x < e:
            return i
    return len(edges)


def situation_key(P, ctx, st, R):
    import cd_plan
    m, e = P.me0, P.en0
    hr = P.hr
    ready = {n for n in st["loadout"] if n in cd_plan.ACTIONS and cd_plan.ready_round(st, n) <= R}
    mine = m.given(1) * e.g(P2.TAKEN, 1) * e.g(P2.DR, 1)
    his = e.given(hr) * m.g(P2.TAKEN, hr) * m.g(P2.DR, hr)
    parts = [
        "P2" if P.en_acted else "P1",
        f"h{band(m.hp / 5050, (0.2, 0.4, 0.6, 0.8))}{band(e.hp / 5050, (0.2, 0.4, 0.6, 0.8))}",
        f"x{band(mine, (0.6, 0.9, 1.2, 1.7))}{band(his, (0.6, 0.9, 1.2, 1.7))}",
        f"b{min(3, int(e.g(P2.NSTK, hr)))}",
        "".join(c for c, f in (("D", m.g(P2.DIMM, hr)), ("d", e.g(P2.DIMM, 0)), ("c", e.g(P2.CIMM, 0)),
                              ("g", m.g(P2.GGRD, 0) < 0.999), ("s", m.g(P2.STUN, 0)),
                              ("n", m.g(P2.TAKEN, 0) > 1.001 or m.g(P2.GDN, 0) < 0.999 or m.g(P2.WND, 0)))
                if f) or "-",
        ("C" if ctx.get("clear_held") else "") + ("P" if ctx.get("pierce_ready") else "")
        + ("Y" if any("copy" in str(x) for x in P.clockd.get("copy", ())) else ""),
        "".join(c for c, n in (("K", "clear"), ("L", "cleanse"), ("M", "smoke"), ("S", "sealnull"), ("I", "kims"))
                if n in ready) + ("X" if ready & set(PIERCE) else ""),
    ]
    return "|".join(parts)


# ------------------------------------------------------------------ library
_LIB = None


def load():
    global _LIB
    if _LIB is None:
        try:
            _LIB = json.load(open(LIB))
        except (OSError, ValueError):
            _LIB = {}
    return _LIB


def lookup(key):
    """(bundle tuple, confidence) or None. Confidence = vote share x a margin factor, 0..1."""
    ent = load().get(key)
    if not ent:
        return None
    votes = ent["votes"]
    tot = sum(votes.values())
    best, n = max(votes.items(), key=lambda kv: kv[1])
    conf = (n / tot) * min(1.0, tot / 3) * min(1.0, ent.get("margin", 0) / 0.15)
    return tuple(best.split("+")), conf


# ------------------------------------------------------------------ solver
def fast_policy(f, ap, keep=40):
    """Planner2 on a shortlist: every legal bundle pre-scored by its own turn (damage now, my next-turn potential),
    the best `keep` fully ranked. ~10x faster than the full rank, for rollouts."""
    P, st = f.planner(ap)
    bundles = P2.legal_bundles(st, f.R, ap, 1, f.loadout, P.me0, P.en0)
    if not bundles:
        return ()
    pre = []
    for b in bundles:
        m, e = P.me0.copy(), P.en0.copy()
        if "cleanse" in b:
            m.wipe(P2.NEGK)
        d, t = P2.run_turn(m, e, [P.my_kit[x] for x in b if x in P.my_kit], 0, 5050, 5050)
        pot, _ = P.my_potential(b, m, e)
        pre.append((d - t + 0.5 * pot, b))
    pre.sort(key=lambda x: -x[0])
    short = [b for _, b in pre[:keep]]
    return P2.rank(P, short, ap, P2.load_weights())[0][1]


def outcome(f):
    r = f.result()
    v = (r["me"] - r["him"]) / 5050
    if r["ko"]:
        v += 1.0 if r["win"] else -1.0
    return v


def rollout(snap, first, seed):
    f = copy.copy(snap)
    f.me, f.en = snap.me.copy(), snap.en.copy()
    f.rows, f.used, f.log = list(snap.rows), [list(x) for x in snap.used], list(snap.log)
    f.rng = random.Random(seed)
    forced = [tuple(first)]
    f.policy = lambda ap: forced.pop() if forced else fast_policy(f, ap)
    f.resume_from_my_turn()
    return outcome(f)


def solve(snap, cands=6, rollouts=4):
    ap = 100 - (20 if snap.me.g(P2.STUN, 0) else 0)
    P, st = snap.planner(ap)
    bundles = P2.legal_bundles(st, snap.R, ap, 1, snap.loadout, P.me0, P.en0)
    ranked = P2.rank(P, bundles, ap, P2.load_weights())
    top = [r[1] for r in ranked[:cands]]
    vals = []
    for b in top:
        v = sum(rollout(snap, b, 1000 + k) for k in range(rollouts)) / rollouts
        vals.append((v, b))
    vals.sort(key=lambda x: -x[0])
    key = situation_key(P, P.ctx, st, snap.R)
    return key, vals, top[0]


def merge(lib, key, vals, planner_pick):
    best_v, best = vals[0]
    margin = best_v - (vals[1][0] if len(vals) > 1 else best_v - 1)
    ent = lib.setdefault(key, {"votes": {}, "value": {}, "margin": 0.0, "n": 0})
    name = "+".join(best)
    ent["votes"][name] = ent["votes"].get(name, 0) + 1
    ent["value"][name] = round(best_v, 3)
    ent["margin"] = round((ent["margin"] * ent["n"] + margin) / (ent["n"] + 1), 3)
    ent["n"] += 1
    ent["planner"] = "+".join(planner_pick)
    ent["alts"] = [["+".join(b), round(v, 3)] for v, b in vals[1:4]]


def build(n_fights, rollouts, cands):
    import fightsim
    opps = fightsim.opponents()
    lib = load()
    t0 = time.time()
    solved = changed = 0
    names = list(opps)
    for i in range(n_fights):
        name = names[i % len(names)]
        acts, prof = opps[name]
        first = (i // len(names)) % 2 == 0
        f = fightsim.Fight(acts, prof, first, seed=500 + i)
        snaps = []
        f.on_my_turn = lambda fight: snaps.append(fight.snapshot())
        f.run()
        for s in snaps:
            key, vals, pick = solve(s, cands, rollouts)
            merge(lib, key, vals, pick)
            solved += 1
            changed += tuple(vals[0][1]) != tuple(pick)
            print(f"[{time.time() - t0:5.0f}s] {name[:14]:14} {'P1' if first else 'P2'} R{s.R} {key:42} "
                  f"planner {'+'.join(pick):28} -> solved {'+'.join(vals[0][1]):28} ({vals[0][0]:+.2f})", flush=True)
        json.dump(lib, open(LIB, "w"), indent=0, sort_keys=True)
    print(f"solved {solved} positions, {changed} changed from the planner's pick; library {len(lib)} keys")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "show"])
    ap.add_argument("n", nargs="?", type=int, default=20)
    ap.add_argument("--fights", type=int, default=6)
    ap.add_argument("--rollouts", type=int, default=4)
    ap.add_argument("--cands", type=int, default=6)
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.fights, a.rollouts, a.cands)
    else:
        lib = load()
        for k, ent in sorted(lib.items(), key=lambda kv: -kv[1]["n"])[:a.n]:
            print(k, lookup(k), ent.get("planner"))


if __name__ == "__main__":
    main()
