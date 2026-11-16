#!/usr/bin/env python3
"""Fit planner2's numbers to the game's own combat code (director 2026-11-11: "Check the simulator against source
and get it within ~1% on numbers").

Controlled states, not logs: both sides at 5050 HP, adjacent, round 3, with chosen tags injected into the TNR engine
(harness/pvp_turn/engine/turn_sim.ts, the pinned upstream source, offline). Each of my damage actions is fired
alone; the engine's damage is compared with planner2's for the same tags.
  1. no tags        -> each action's base damage (what planner2 should use as base)
  2. one tag         -> how each tag type changes damage (multiplicative? capped? applied where?)
  3. tag pairs       -> how tags stack
Prints engine/python ratios per scenario; --write saves the fitted bases to fights/engine_bases.json, which
planner2 then uses in place of the log-calibrated bases.

Usage: engine_fit.py [--write] [--actions rebirth,ember,...]
"""
import argparse
import json
import os
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402
import planner2 as P2  # noqa: E402
import shotplan  # noqa: E402
import turn  # noqa: E402
import value_model  # noqa: E402

BASES = os.path.join(HERE, "..", "fights", "engine_bases.json")
R = 3
DAMAGE = ["rebirth", "shrapnel", "lotus", "fury", "ember", "danse", "stormblade", "nights", "aetherion", "kunai", "basic"]
# (label, [(side, kind, value)]) tags live this round (first <= R <= last); side "me" = dauntless, "en" = him
SCEN = [
    ("none", []),
    ("me given +35", [("me", "given", 0.35)]),
    ("me given +35 x2", [("me", "given", 0.35), ("me", "given", 0.35)]),
    ("me given -30", [("me", "given", -0.30)]),
    ("en taken +35", [("en", "taken", 0.35)]),
    ("en dr 35", [("en", "dr", 0.35)]),
    ("en dr 35 x2", [("en", "dr", 0.35), ("en", "dr", 0.25)]),
    ("en absorb 35", [("en", "absorb", 0.35)]),
    ("en reflect 35", [("en", "reflect", 0.35)]),
    ("en parry 20", [("en", "parry", 0.20)]),
    ("en shield 500", [("en", "shield", 500)]),
    ("me lifesteal 35", [("me", "lifesteal", 0.35)]),
    ("given+35 & taken+35", [("me", "given", 0.35), ("en", "taken", 0.35)]),
    ("given+35 & dr35", [("me", "given", 0.35), ("en", "dr", 0.35)]),
    ("taken+35 & dr35", [("en", "taken", 0.35), ("en", "dr", 0.35)]),
]


def sides(tags):
    me, en = shotplan.Side(5050.0), shotplan.Side(5050.0)
    for side, kind, val in tags:
        (me if side == "me" else en).tags.append([kind, val, R - 1 if kind == "shield" else R, R + 1])
    return me, en


def engine_run(tags, acts):
    me0, en0 = sides(tags)
    me = {"curHealth": 5050, "maxHealth": 5050}
    en = {"curHealth": 5050, "maxHealth": 5050}
    cands = [[(a, turn.ACTION_ID[a], (6, 4) if a not in turn.SELF_T else (7, 4))] for a in acts]
    res = EB.evaluate(cands, me, en, (7, 4), (6, 4), R, me0, en0, {}, {}, [], value_model.load_cal(), timeout=120)
    out = {}
    for a, r in zip(acts, res or []):
        if r.get("legal"):
            out[a] = (5050 - r["afterMe"]["him"], 5050 - r["afterMe"]["me"])
    return out


def python_run(tags, acts, kit):
    me0, en0 = sides(tags)
    out = {}
    for a in acts:
        m, e = P2.from_shotplan(me0, R), P2.from_shotplan(en0, R)
        P2.run_turn(m, e, [kit[a]], 0, 1e9, 1e9)
        out[a] = (5050 - e.hp, 5050 - m.hp)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--actions", default=",".join(DAMAGE))
    a = ap.parse_args()
    acts = a.actions.split(",")
    cal = value_model.load_cal()
    value_model.calibrate_kit(cal)
    kit = {k: P2.compile_spec(v, True) for k, v in shotplan.MINE.items()}
    base_e = engine_run([], acts)
    print("base damage, engine vs planner2 (calibrated):")
    for x in acts:
        if x in base_e:
            print(f"  {x:10} engine {base_e[x][0]:7.1f}  planner2 {kit[x][0]:7.1f}  ratio {base_e[x][0] / max(1, kit[x][0]):.3f}")
    # planner2 with the engine's bases: from here every gap is the tag math
    fitted = {x: base_e[x][0] for x in acts if x in base_e and base_e[x][0] > 0}
    for x, v in fitted.items():
        kit[x] = (v,) + tuple(kit[x][1:])
    if os.environ.get("BASE_ONLY"):
        json.dump(fitted, open(BASES, "w"), indent=1) if a.write else None
        return
    print("\nwith engine bases, engine / planner2 per scenario (dealt; self in brackets):")
    worst = []
    for label, tags in SCEN:
        e = engine_run(tags, acts)
        p = python_run(tags, acts, kit)
        rs, ss = [], []
        for x in acts:
            if x in e and e[x][0] > 20 and p[x][0] > 20:
                rs.append(e[x][0] / p[x][0])
                worst.append((abs(e[x][0] / p[x][0] - 1), label, x, e[x], p[x]))
            if x in e and (abs(e[x][1]) > 20 or abs(p[x][1]) > 20):
                ss.append(e[x][1] - p[x][1])
        print(f"  {label:22} dealt ratio median {statistics.median(rs) if rs else float('nan'):.3f} "
              f"[{min(rs) if rs else 0:.3f}..{max(rs) if rs else 0:.3f}]"
              + (f"  self diff median {statistics.median(ss):+.0f}" if ss else ""))
    print("\nworst:")
    for w in sorted(worst, reverse=True)[:10]:
        print(f"  {w[1]:22} {w[2]:10} engine {w[3][0]:.0f}/{w[3][1]:.0f}  planner2 {w[4][0]:.0f}/{w[4][1]:.0f}")
    if a.write:
        json.dump(fitted, open(BASES, "w"), indent=1)
        print("wrote", BASES)


if __name__ == "__main__":
    main()
