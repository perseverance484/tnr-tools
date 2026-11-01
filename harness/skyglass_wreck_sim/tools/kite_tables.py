#!/usr/bin/env python3
"""Tables for the solo kite grid (engine/kite.ts outputs).

    python3 harness/skyglass_wreck_sim/tools/kite_tables.py [results/kite_*.json ...]

Default: every results/kite_<variant>_<rules>_<mode>.json. Prints the per-cell summary table, the Captain's rule
fires per cell (phase-2 rules first), death causes and kite movement counts, as Markdown.
"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
paths = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "results", "kite_*_*_*.json")))
ORDER_V = {"average": 0, "elite": 1}
ORDER_R = {"old": 0, "new": 1}
ORDER_M = {"close": 0, "kite": 1, "poke": 2}
cells = []
for p in paths:
    d = json.load(open(p))
    c = d["cell"]
    cells.append((ORDER_V.get(c["variant"], 9), ORDER_M.get(c["mode"], 9), ORDER_R.get(c["rules"], 9), d))
cells.sort(key=lambda x: x[:3])


def lab(d):
    c = d["cell"]
    return f"{c['variant']} / {c['rules']} / {c['mode']}"


print("| Cell (player / rules / mode) | Won / wiped / stalled at 150 rounds | Boss wave reached % | Wave 2 rounds median (p90) | UC casts per fight median (mean, max) | Max hit on player median (max, by) | Phase 2 reached % | Captain min HP % median | Sealwright killed % | Captain idle turns (player 2+ away) / turns | Captain move turns | Deaths: main cause |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for *_, d in cells:
    a = d["aggregate"]
    mh = a["maxHitMax"]
    dd = {}
    for k0, v0 in a["deaths"].items():
        # Older outputs labelled own-turn HP loss "damage over time / tick on own turn"; it can also be reflected damage.
        unit = "own turn (DoT tick or reflect)" if k0.startswith(("damage over time", "own turn")) else k0.split(" / ")[0]
        act = k0.split(" / ", 1)[1] if " / " in k0 and not k0.startswith(("damage over time", "own turn")) else ""
        u = dd.setdefault(unit, {"n": 0, "acts": {}})
        u["n"] += v0
        if act:
            u["acts"][act] = u["acts"].get(act, 0) + v0
    deaths = sorted(dd.items(), key=lambda kv: -kv[1]["n"])
    dtxt = "; ".join(f"{k} {v['n']}" + (f" (top: {max(v['acts'], key=v['acts'].get)})" if v["acts"] else "") for k, v in deaths) or "-"
    o = a["outcomes"]
    print(f"| {lab(d)} | {o.get('won', 0)} / {o.get('wipe', 0)} / {o.get('stalled', 0)} | {a['wave2ReachedPct']} | {a['wave2RoundsMedian']} ({a['wave2RoundsP90']}) | {a['ucCastsMedian']} ({a['ucCastsMean']}, {a['ucCastsMax']}) | {round(a['maxHitMedian'] or 0):,} ({round(mh['dmg']):,}, {mh['action']}) | {a['reachedPhase2Pct']} | {a['captainMinHpMedian']} | {a['sealwrightKilledPct']} | {a['captainIdleTurns']} ({a['captainIdleTurnsPlayerFar']}) / {a['captainTurns']} | {a['captainMoveTurns']} | {dtxt} |")

print()
print("Captain rule fires (all runs of the cell; phase-2 rules are 0-6). Old and new lists differ after index 12.")
print()
for *_, d in cells:
    fires = [f"{r['index']} {r['note'].split(' (')[0]}: {r['fires']}" for r in d["ruleTable"] if r["fires"]]
    bk = "; ".join(f"{k}: {v}" for k, v in d["backupFires"].items())
    print(f"- **{lab(d)}**: " + "; ".join(fires) + (f"; {bk}" if bk else ""))

print()
print("| Cell | Marks: Binding Ring / Ship's Bell / Rows A / Broadside | Stuns landed on the Captain (player Stunning Jab casts, wave 2) | Kite: retreat / approach steps, cornered turns, pokes, steps inside range / kite steps | Captain decisions: nearest player 5+ away / pet adjacent while player 2+ away / all | Unmarked set pieces (whole floor) |")
print("|---|---|---|---|---|---|")
for *_, d in cells:
    a = d["aggregate"]
    m = a["markVsBlast"]
    k = a.get("kite")
    ktxt = f"{k['retreatSteps']} / {k['approachSteps']}, {k['cornered']}, {k['pokes']}, {k['humanStepsInside']} / {k['humanSteps']}" if k else "-"
    print(f"| {lab(d)} | {m['ring']} / {m['bell']} / {m['rowsA']} / {m['broadside']} | {a['stunOnCaptain']} ({a['jabCastsW2']}) | {ktxt} | {a['captainDecisionsPlayerFar5']} / {a['captainDecisionsPetAdjacentPlayerFar']} / {a['captainDecisions']} | {d['fallbackGuard']['unmarkedCasts']}/{d['fallbackGuard']['setPieceCasts']} |")
