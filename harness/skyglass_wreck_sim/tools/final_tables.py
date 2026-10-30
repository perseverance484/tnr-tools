#!/usr/bin/env python3
"""Print the final-pass tables (REPORT_final.md) from results/final_*.json.

    python3 harness/skyglass_wreck_sim/tools/final_tables.py
"""
import json
import os

R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")


def load(n):
    p = os.path.join(R, n)
    return json.load(open(p)) if os.path.exists(p) else None


def pct(a, b):
    return f"{a}/{b} ({round(100 * a / b) if b else 0}%)"


def wreck():
    print("## Wreck")
    print("| Version | Cleared | Runs with a wipe | Min @15 s (AI +1.5 s) | Boss wave wipes/attempts | Unmarked set pieces / cast |")
    print("|---|---|---|---|---|---|")
    for n, lab in (("final_wreck_endgame.json", "Endgame, 60, pets, dodge"), ("final_wreck_lvl50.json", "Level 50, 60, pets, dodge"),
                   ("final_wreck_endgame_nododge.json", "Endgame, 30, pets, no dodge"), ("final_wreck_lvl50_nododge.json", "Level 50, 30, pets, no dodge")):
        d = load(n)
        if not d:
            continue
        v = d["variants"][0]
        t = v["time"]
        boss = [w for w in v["waves"] if w["wave"].startswith("F5W2")]
        b = f"{boss[0]['wipedHere']}/{boss[0]['attempts']}" if boss else "-"
        g = d.get("fallbackGuard", {})
        print(f"| {lab} | {v['outcomes'].get('cleared')}/{v['runs']} | {v['runsWithAWipePct']}% | {t['player15s_ai0s']['minutesMedianAllRuns']} ({t['player15s_ai1.5s']['minutesMedianAllRuns']}) | {b} | {g.get('unmarkedCasts')}/{g.get('setPieceCasts')} |")


def hunts(name="final_hunts_dodge.json", title="Hunts (dodge on)"):
    d = load(name)
    if not d:
        return
    print(f"\n## {title}")
    print("| Path | Win | End HP med [p10] | Rounds | Lost at | Captain phase 1 / phase 2 med (p90) |")
    print("|---|---|---|---|---|---|")
    for r in d["results"]:
        cap = next((f.get("captainPhases") for f in r["fights"] if f.get("captainPhases")), None)
        cs = f"{cap['phase1RoundsMedian']} / {cap['phase2RoundsMedian']} ({cap['phase2RoundsP90']}), reached {cap['reachedPhase2Pct']}%" if cap else ""
        lost = {k: v for k, v in r["lossesAt"].items() if v}
        print(f"| {r['path']} | {pct(r['wins'], r['runs'])} | {r['endHpPctMedian']} [{r['endHpPctP10']}] | {r['totalRoundsMedian']} | {lost or '-'} | {cs} |")
    g = d.get("fallbackGuard", {})
    print(f"\nfallback guard: unmarked {g.get('unmarkedCasts')} of {g.get('setPieceCasts')} set-piece casts")


def charts(name, title):
    d = load(name)
    if not d:
        return
    print(f"\n## {title}")
    print("| Run | Player | Base clear | Press-on won/reached | Base min | Fights (won/reached, rounds, HP start->end) |")
    print("|---|---|---|---|---|---|")
    for r in d["results"]:
        fs = "; ".join(f"F{f['fight']} {f['won']}/{f['reached']} r{f['roundsMedian']} {f['hpStartMedian']}->{f['hpEndMedian']}" for f in r["fights"])
        print(f"| {r['run']} | {r['variant']} | {pct(r['baseClear'], r['runs'])} | {r['pressOnWon']}/{r['pressOnReached']} | {r['baseMinutesMedian']} | {fs} |")
    g = d.get("fallbackGuard", {})
    print(f"\nfallback guard: unmarked {g.get('unmarkedCasts')} of {g.get('setPieceCasts')} set-piece casts")


def haul(name, title):
    d = load(name)
    if not d:
        return
    print(f"\n## {title}")
    print("| Page | Path | Haul M | Clear % | EV M | Min (clear) |")
    print("|---|---|---|---|---|---|")
    for r in d["results"]:
        for p in sorted(r["paths"], key=lambda p: -p["evM"]):
            print(f"| {r['variant']} | {p['path']} | {p['haulM']} | {p['clearPct']} | {p['evM']} | {p.get('minutesClearMedian', p.get('minutesClear'))} |")


def crown():
    d = load("final_crownhold_chain.json")
    if not d:
        return
    print("\n## Crownhold chain (pet, reads 0.85, HP carried; top-up at the Crowned Captain)")
    print("| Route | Chains | Clear | Crowned Captain: reached / entry HP med / win of reached / rounds | Losses at |")
    print("|---|---|---|---|---|")
    for pol, c in d["chain"].items():
        s = c["summary"]
        b = s["bosses"]["D5.BOSS"]
        carried = [f.get("carriedHp") for ch in c["chains"] for f in ch["fights"] if f["fight"] == "D5.BOSS"]
        print(f"| {pol} | {s['chains']} | {s['clearPct']}% | {b['reachedPct']}% / {b['startHpMedian']} (carried {sorted(x for x in carried if x is not None)[len(carried)//2] if carried else '-'}) / {b['winPctOfReached']}% / {b['roundsMedian']} | {s['lossesAt']} |")


if __name__ == "__main__":
    wreck()
    hunts()
    hunts("final_hunts_nododge.json", "Hunts (dodge off)")
    charts("final_charts_dodge_a.json", "Charts: commons, Reliquary runs, steeping (L100, dodge on)")
    charts("final_charts_dodge_b.json", "Charts: The Fall, Burning Heading (L100, dodge on)")
    charts("final_charts_fall_notwist.json", "The Fall without the Keeper's fire (L100, dodge on)")
    charts("final_charts_commons_L50_dodge.json", "Commons, L50 (dodge on)")
    charts("final_charts_commons_L50_nododge.json", "Commons, L50 (dodge off)")
    charts("final_charts_nododge.json", "Charts (dodge off, L100)")
    hunts("final_hunts_presson_probe.json", "Press-on probes: Archive and Watch (dodge on)")
    crown()
    haul("final_haul_exact_dodge.json", "Haul named routes (exact, dodge on)")
