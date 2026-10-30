#!/usr/bin/env python3
"""Markdown tables for REPORT_hunts.md from hunts_main.ts results.

    python3 harness/skyglass_wreck_sim/tools/hunts_tables.py results/hunts_final.json [results/hunts_final_nododge.json]
"""
import json
import sys


def load(p):
    return json.load(open(p))["results"]


def f(x, suffix=""):
    return "-" if x is None else f"{x}{suffix}"


def summary(on, off):
    offm = {r["path"]: r for r in off} if off else {}
    print("| Path | Win (dodge on) | End HP median [p10] | Rounds total | Lost at fight | Win (dodge off) | End HP (off) |")
    print("|---|---:|---|---:|---|---:|---|")
    for r in on:
        o = offm.get(r["path"])
        lost = ", ".join(f"F{k}: {v}" for k, v in r["lossesAt"].items() if v)
        print(f"| {r['path']} | {r['wins']}/{r['runs']} | {f(r['endHpPctMedian'], '%')} [{f(r['endHpPctP10'])}] | {f(r['totalRoundsMedian'])} | {lost or 'none'} | "
              f"{(str(o['wins']) + '/' + str(o['runs'])) if o else '-'} | {f(o['endHpPctMedian'], '%') if o else '-'} |")


def fights(on, off, keys=None):
    offm = {r["path"]: r for r in off} if off else {}
    print("| Path | Fight | Won / reached | Rounds median [p10-p90] | HP start -> end (median, p10 end) | Gross HP lost | Player idle turns | Won / reached (off) | HP end (off) |")
    print("|---|---|---:|---|---|---:|---:|---:|---|")
    for r in on:
        if keys and r["path"] not in keys:
            continue
        o = offm.get(r["path"])
        for i, x in enumerate(r["fights"]):
            y = o["fights"][i] if o else None
            print(f"| {r['path']} | {x['label']}{' **(boss)**' if x['boss'] else ''} | {x['won']}/{x['reached']} | {f(x['roundsMedian'])} [{f(x['roundsP10'])}-{f(x['roundsP90'])}] | "
                  f"{f(x['hpStartPctMedian'])} -> {f(x['hpEndPctMedian'])} ({f(x['hpEndPctP10'])}) | {f(x['hpLostPctMedian'], '%')} | {f(x['playerIdleTurnsPct'], '%')} | "
                  f"{(str(y['won']) + '/' + str(y['reached'])) if y else '-'} | {f(y['hpEndPctMedian']) if y else '-'} |")


def setpieces(on, off):
    offm = {r["path"]: r for r in off} if off else {}
    seen = {}
    for r in on:
        o = offm.get(r["path"])
        for i, x in enumerate(r["fights"]):
            for n, e in x["enemies"].items():
                key = (x["label"].split(" (")[0], n)
                if key in seen:
                    continue
                y = o["fights"][i]["enemies"].get(n) if o and i < len(o["fights"]) else None
                seen[key] = (r["path"], x["label"], n, e, y)
    print("| Fight (first path seen) | Enemy | Appearances | Mark fired % | Marks / blasts per fight | Blast hit % (on / off) | Windows per fight | Signature % | Idle turns after r2 | Dealt per fight (on / off) |")
    print("|---|---|---:|---:|---|---|---:|---:|---:|---|")
    for (path, label, n, e, y) in seen.values():
        print(f"| {label} | {n} | {e['appearances']} | {f(e['markFiredPct'])} | {f(e['marksPerFight'])} / {f(e['blastsPerFight'])} | {f(e['blastHitPct'])} / {f(y['blastHitPct']) if y else '-'} | "
              f"{f(e['windowsPerFight'])} | {f(e['signatureFiredPct'])} | {f(e['idleTurnsAfterR2Pct'], '%')} | {e['dealtPerFight']} / {y['dealtPerFight'] if y else '-'} |")


def dodge(on):
    tot = {}
    for r in on:
        for x in r["fights"]:
            for k, v in x["dodge"].items():
                tot[k] = tot.get(k, 0) + v
    print(f"Dodge totals (all paths, dodge on): {json.dumps(tot)}")


if __name__ == "__main__":
    on = load(sys.argv[1])
    off = load(sys.argv[2]) if len(sys.argv) > 2 else None
    print("### Summary\n")
    summary(on, off)
    print("\n### Per fight\n")
    fights(on, off)
    print("\n### Set pieces and behaviour\n")
    setpieces(on, off)
    print()
    dodge(on)
