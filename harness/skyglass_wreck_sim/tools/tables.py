#!/usr/bin/env python3
"""Print markdown summary tables from one or more results/*.json files.

Usage: tables.py results/a.json [results/b.json ...] [--waves] [--enemies]
"""
import json
import sys

files = [a for a in sys.argv[1:] if not a.startswith("--")]
show_waves = "--waves" in sys.argv
show_enemies = "--enemies" in sys.argv


def fmt(x):
    return "-" if x is None else (f"{x:g}" if isinstance(x, (int, float)) else str(x))


for f in files:
    d = json.load(open(f))
    title = (d.get("override") or {}).get("name") or "baseline (captured live state)"
    print(f"\n### {title} ({f})\n")
    print("| Tier | Runs | Cleared | Runs with a wipe | Wipes/run (median) | Total rounds median [p10-p90] | Clean-clear rounds | Min @10s | Min @15s | Min @20s | Min @15s + AI 1.5s | Cleared <=60 min @15s |")
    print("|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|")
    for v in d["variants"]:
        t = v["time"]
        print(
            f"| {v['variant']} | {v['runs']} | {v['outcomes']['cleared']} | {fmt(v['runsWithAWipePct'])}% | {fmt(v['wipesPerRunMedian'])} | "
            f"{fmt(v['totalRoundsMedian'])} [{fmt(v['totalRoundsP10'])}-{fmt(v['totalRoundsP90'])}] | {fmt(v['totalRoundsCleanClearMedian'])} | "
            f"{fmt(t['player10s_ai0s']['minutesMedianAllRuns'])} | {fmt(t['player15s_ai0s']['minutesMedianAllRuns'])} | "
            f"{fmt(t['player20s_ai0s']['minutesMedianAllRuns'])} | {fmt(t['player15s_ai1.5s']['minutesMedianAllRuns'])} | "
            f"{fmt(t['player15s_ai0s']['clearedWithinLimitPct'])}% |"
        )
    if show_waves:
        for v in d["variants"]:
            print(f"\n**{v['variant']}** per wave (rounds over all attempts that reached the wave)\n")
            print("| Wave | Enemies | Reached | Cleared | Wiped here | Rounds median [min-max] | Party HP lost % | HP/CP/SP left % | Top threat (share) |")
            print("|---|---|---:|---:|---:|---|---:|---|---|")
            for w in v["waves"]:
                p = w["poolsLeftMedianPct"]
                th = w["threats"][0] if w["threats"] else None
                tht = f"{th['name']} ({fmt(th['sharePct'])}%)" if th else "-"
                print(
                    f"| {w['wave']} | {w['enemies']} | {w['attempts']} | {w['cleared']} | {w['wipedHere']} | "
                    f"{fmt(w['roundsMedian'])} [{fmt(w['roundsMin'])}-{fmt(w['roundsMax'])}] | {fmt(w['partyHpLostPctMedian'])} | "
                    f"{fmt(p['hp'])}/{fmt(p['cp'])}/{fmt(p['sp'])} | {tht} |"
                )
    if show_enemies:
        for v in d["variants"]:
            print(f"\n**{v['variant']}** enemies overall\n")
            print("| Enemy | Appear | Killed % | Dies after rds | Dealt/app | Taken/app | Healed/app | Idle/move % | Rules never fired | Top actions |")
            print("|---|---:|---:|---:|---:|---:|---:|---:|---|---|")
            for e in sorted(v["enemiesOverall"], key=lambda e: -e["dealtPerAppearance"]):
                acts = ", ".join(f"{k} {n}" for k, n in list(e["actions"].items())[:3])
                print(
                    f"| {e['name']} | {e['appearances']} | {fmt(e['killedPct'])} | {fmt(e['diedAfterRoundsMedian'])} | {e['dealtPerAppearance']} | "
                    f"{e['takenPerAppearance']} | {e['healedPerAppearance']} | {fmt(e['idleOrMovePct'])} | {', '.join(e['rulesNeverFired']) or '-'} | {acts} |"
                )
