#!/usr/bin/env python3
"""Markdown tables for REPORT_charts.md from the charts_main.ts result files.

    python3 harness/skyglass_wreck_sim/tools/charts_tables.py harness/skyglass_wreck_sim/results
"""
import json
import sys
from pathlib import Path

R = Path(sys.argv[1] if len(sys.argv) > 1 else "harness/skyglass_wreck_sim/results")


def load(name):
    p = R / name
    if not p.exists():
        return {}
    return {(x["run"], x["variant"]): x for x in json.loads(p.read_text())["results"]}


def pct(a, b):
    return "-" if not b else f"{round(100 * a / b)}%"


def clear(x):
    return "-" if not x else f"{x['baseClear']}/{x['runs']} ({pct(x['baseClear'], x['runs'])})"


def press(x):
    if not x:
        return "-"
    return f"{x['pressOnWon']}/{x['pressOnReached']} ({pct(x['pressOnWon'], x['pressOnReached'])})"


def fights(x):
    if not x:
        return "-"
    out = []
    for f in x["fights"]:
        tag = "P" if f["pressOn"] else "F"
        hp = "-" if f["hpEndMedian"] is None else f"{f['hpStartMedian']}->{f['hpEndMedian']}"
        out.append(f"{tag}{f['fight']} {f['won']}/{f['reached']} r{f['roundsMedian']} {hp}")
    return "; ".join(out)


on, off = load("charts_commons_dodge.json"), load("charts_commons_nododge.json")
print("### Common charts (opponent_scaled_to_user), 40 seeds per cell\n")
print("| Run | Player | Base clear (dodge on / off) | Press-on won of reached (on / off) | Base minutes (on) |")
print("|---|---|---|---|---:|")
for run in ["lowtide", "nightwatch"]:
    for v in ["L50", "L50kit", "L100", "L100noarmor"]:
        a, b = on.get((run, v)), off.get((run, v))
        if not a and not b:
            continue
        print(f"| {run} | {v} | {clear(a)} / {clear(b)} | {press(a)} / {press(b)} | {a['baseMinutesMedian'] if a else '-'} |")
print("\nPer fight (dodge on): won/reached, median rounds, median HP start->end (% of base max HP)\n")
print("| Run | Player | Fights |")
print("|---|---|---|")
for run in ["lowtide", "nightwatch"]:
    for v in ["L50", "L50kit", "L100", "L100noarmor"]:
        a = on.get((run, v))
        if a:
            print(f"| {run} | {v} | {fights(a)} |")

ron, roff = load("charts_rares_dodge.json"), load("charts_rares_nododge.json")
non, noff = load("charts_rares_notwist_dodge.json"), load("charts_rares_notwist_nododge.json")
print("\n### Rare and tainted charts (L100, endgame), 40 seeds per cell\n")
print("| Run | Player | Base clear, twist on (dodge on / off) | Base clear, twist OFF (on / off) | Press-on won of reached (on / off) | Base minutes (on) |")
print("|---|---|---|---|---|---:|")
for run in ["reliquary", "fall", "rotted", "burning"]:
    for v in ["L100", "L100noarmor"]:
        a, b = ron.get((run, v)), roff.get((run, v))
        c, d = non.get((run, v)), noff.get((run, v))
        if not a and not b:
            continue
        print(f"| {run} | {v} | {clear(a)} / {clear(b)} | {clear(c)} / {clear(d)} | {press(a)} / {press(b)} | {a['baseMinutesMedian'] if a else '-'} |")
print("\nPer fight (twist on, dodge on): won/reached, median rounds, median HP start->end (% of base max HP)\n")
print("| Run | Player | Fights |")
print("|---|---|---|")
for run in ["reliquary", "fall", "rotted", "burning"]:
    for v in ["L100", "L100noarmor"]:
        a = ron.get((run, v))
        if a:
            print(f"| {run} | {v} | {fights(a)} |")

son, soff = load("charts_steeping_dodge.json"), load("charts_steeping_nododge.json")
print("\n### Steeping (Steeping Horror scaled to the player), 40 seeds\n")
print("| Player | Win (dodge on / off) | Rounds (on) | HP start->end median (on) |")
print("|---|---|---|---|")
for v in ["L100", "L100noarmor"]:
    a, b = son.get(("steeping", v)), soff.get(("steeping", v))
    if a or b:
        f = a["fights"][0] if a else None
        print(f"| {v} | {clear(a)} / {clear(b)} | {f['roundsMedian'] if f else '-'} | {f['hpStartMedian'] if f else '-'}->{f['hpEndMedian'] if f else '-'} |")

print("\n### Twist hazards (twist on, dodge on / off, L100)\n")
print("| Run | Fight | Hazard marks / blasts per fight | Blast hit % (on / off) | Hazard died median round (on) |")
print("|---|---|---|---|---|")
for run in ["reliquary", "rotted", "fall", "burning"]:
    a, b = ron.get((run, "L100")), roff.get((run, "L100"))
    if not a:
        continue
    for i, f in enumerate(a["fights"]):
        for n, e in f["enemies"].items():
            if n not in ("Lingering Echo", "Burning Deck"):
                continue
            eb = b["fights"][i]["enemies"].get(n, {}) if b and i < len(b["fights"]) else {}
            print(f"| {run} | {f['label'][:48]} | {e['marksPerFight']} / {e['blastsPerFight']} | {e['blastHitPct']} / {eb.get('blastHitPct', '-')} | {e['diedMedianRound']} |")
