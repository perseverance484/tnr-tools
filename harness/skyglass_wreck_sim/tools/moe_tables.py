#!/usr/bin/env python3
"""Tables for the Mother of Echoes tuning runs (engine/moe.ts --out).

    python3 harness/skyglass_wreck_sim/tools/moe_tables.py results/moe_tune_final_a.json [results/moe_tune_final_b.json ...]

Prints one row per cell (player model : policy) and per act: entered / won, rounds, deaths' causes, set-piece fire
counts (lands per fight, hits, damage per hit), unmarked blasts, boss idle turns, specials.
"""
import json
import sys


def fmt_deaths(d, n=3):
    items = sorted(d.items(), key=lambda kv: -kv[1])[:n]
    return "; ".join(f"{k} {v}" for k, v in items) or "-"


def main(paths):
    cells = {}
    for p in paths:
        doc = json.load(open(p))
        for name, c in doc["cells"].items():
            cells[name] = (c, doc)
    print("| Cell | Runs | Full clear | Act I won/entered (rounds med) | Act II | Act III | Unmarked blasts |")
    print("|---|---|---|---|---|---|---|")
    for name, (c, doc) in cells.items():
        s = c["summary"]
        acts = []
        for a in ("1", "2", "3"):
            pa = s["perAct"].get(a)
            acts.append("-" if not pa or not pa["entered"] else f"{pa['won']}/{pa['entered']} ({pa['roundsAllMedian']})")
        unm = sum(pa["unmarked"] for pa in s["perAct"].values())
        print(f"| {name} | {s['runs']} | {s['fullClears']} ({s['fullClearPct']}%) | {acts[0]} | {acts[1]} | {acts[2]} | {unm} |")
    print()
    print("| Cell | Act | Deaths (top 3) | Stalled | Set pieces: lands per fight / hits / dmg per hit | Idle boss turns | Specials (total) | Max hit med | Kill first |")
    print("|---|---|---|---|---|---|---|---|---|")
    for name, (c, doc) in cells.items():
        for a, pa in sorted(c["summary"]["perAct"].items()):
            if not pa["entered"]:
                continue
            sets = "; ".join(f"{k} {v['landsPerFight']}/{v['hit']}/{v['dmgPerHit']}" for k, v in pa["sets"].items()) or "-"
            idle = ", ".join(f"{k} {v}" for k, v in pa["idleTurns"].items())
            spec = ", ".join(f"{k} {v}" for k, v in sorted(pa["specials"].items()))
            kf = ", ".join(f"{k} {v}" for k, v in pa["killFirst"].items()) or "-"
            print(f"| {name} | {a} | {fmt_deaths(pa['deaths'])} | {pa['stalled']} | {sets} | {idle} | {spec} | {pa['maxHitMedian']} | {kf} |")


if __name__ == "__main__":
    main(sys.argv[1:])
