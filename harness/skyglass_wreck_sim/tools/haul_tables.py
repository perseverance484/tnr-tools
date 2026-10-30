#!/usr/bin/env python3
"""The Haul: policy / variant / modifier tables from haul_main.ts results (--exhaustive or --paths).

  python3 haul_tables.py results/haul_x.json [more.json ...] [--scale PCT] [--old 7.5] [--exact exact.json ...]

--exact: exact per-seed results (--paths) whose clear rates and EVs replace the state-merged ones for the same paths
(same dodge setting); those cells are the best estimate, the rest are state-merged.

--scale rescales every EV by PCT/100 (a chest drop chance applied after the run, e.g. to read a 100% run at 55%).
Policies (per variant, over the evaluated paths):
  timid    C and CC (leave after 1-2 crates)
  sensible the best 3-step, 1-locker, no-cut path (the design's "about 3 steps, 1 locker")
  greedy   the best 5-step path with 3+ lockers (fixed reference CLLLC if present)
  cut      the best path with 2+ cuts
  best / worst: the highest / lowest EV over all paths of 2+ steps
"""
import json
import sys

args = sys.argv[1:]
scale = 1.0
old = 7.5
files = []
exact_files = []
i = 0
while i < len(args):
    if args[i] == "--exact":
        exact_files.append(args[i + 1])
        i += 2
        continue
    if args[i] == "--scale":
        scale = float(args[i + 1]) / 100
        i += 2
    elif args[i] == "--old":
        old = float(args[i + 1])
        i += 2
    else:
        files.append(args[i])
        i += 1

EX = {}
for f in exact_files:
    d = json.load(open(f))
    for r in d["results"]:
        EX[(r["variant"], d["settings"]["dodge"])] = {p["path"]: p for p in r["paths"]}

rows = []
for f in files:
    d = json.load(open(f))
    dodge = d["settings"]["dodge"]
    for r in d["results"]:
        ex = EX.get((r["variant"], dodge), {})
        r["paths"] = [dict(p, clearPct=ex[p["path"]]["clearPct"], evM=ex[p["path"]]["evM"], exact=True) if p["path"] in ex else p for p in r["paths"]]
        rows.append((r, dodge))


def ev(p):
    return p["evM"] * scale


def mins(p):
    return p.get("minutesClear", p.get("minutesClearMedian"))


def pick(paths, pred, key=ev):
    c = [p for p in paths if pred(p)]
    return max(c, key=key) if c else None


def fmt(p, sens=None):
    if not p:
        return "-"
    rel = f" ({100 * ev(p) / ev(sens):.0f}%)" if sens and ev(sens) else ""
    return f"{p['path']}{'*' if p.get('exact') else ''} {p['clearPct']}% / {ev(p):.1f}M{rel} / {mins(p)} min"


print(f"EV scale {scale * 100:.0f}% of the haul; old S-rank quest ~{old}M per run\n")
print("| Variant | Dodge | Timid C / CC | Sensible | Greedy (best 5-step, 3+ L) | CLLLC | Cut-heavy | Best | Worst (2+ steps) |")
print("|---|---|---|---|---|---|---|---|---|")
summary = {}
for r, dodge in rows:
    P = r["paths"]
    for p in P:
        p.setdefault("lockers", p["path"].count("L"))
        p.setdefault("cuts", p["path"].count("X"))
    by = {p["path"]: p for p in P}
    sens = pick(P, lambda p: len(p["path"]) == 3 and p["lockers"] == 1 and p["cuts"] == 0)
    greedy = pick(P, lambda p: len(p["path"]) == 5 and p["lockers"] >= 3)
    cut = pick(P, lambda p: p["cuts"] >= 2)
    best = pick(P, lambda p: len(p["path"]) >= 2)
    worst = pick(P, lambda p: len(p["path"]) >= 2, key=lambda p: -ev(p))
    t1, t2 = by.get("C"), by.get("CC")
    summary[(r["variant"], dodge)] = {"sensible": sens, "best": best}
    tim = f"{ev(t1):.1f} / {ev(t2):.1f}M ({t2['clearPct']}%)" if t1 and t2 else "-"
    print(f"| {r['variant']} | {'on' if dodge else 'off'} | {tim} | {fmt(sens)} | {fmt(greedy, sens)} | {fmt(by.get('CLLLC'), sens)} | {fmt(cut, sens)} | {fmt(best, sens)} | {fmt(worst, sens)} |")

# Steeping: the Rot-Sealed Page roll vs the base page (best-path EV; the player picks the best route for the page).
weights = None
for f in files:
    d = json.load(open(f))
    weights = {k: m["weight"] for k, m in d["settings"]["params"]["modifiers"].items()}
if weights and any("+" in v for v, _ in summary):
    print("\nSteeping (best-path EV, dodge on): roll = weighted modifiers / base page")
    print("| Layout | Base | " + " | ".join(f"{k} (w {w})" for k, w in weights.items()) + " | Roll EV | Roll / base |")
    print("|---|---|" + "---|" * len(weights) + "---|---|")
    for (v, dodge), s in summary.items():
        if "+" in v or not dodge:
            continue
        cells = []
        tot = 0.0
        wsum = 0.0
        for k, w in weights.items():
            m = summary.get((f"{v}+{k}", True))
            if not m or not m["best"]:
                cells.append("-")
                continue
            e = ev(m["best"])
            cells.append(f"{m['best']['path']} {e:.1f}M")
            tot += w * e
            wsum += w
        base = ev(s["best"]) if s["best"] else 0
        roll = tot / wsum if wsum else 0
        print(f"| {v} | {s['best']['path']} {base:.1f}M | " + " | ".join(cells) + f" | {roll:.1f}M | {roll / base:.2f}x |" if base else "")
