#!/usr/bin/env python3
"""Rule-cap pass tables (REPORT.md "Rule cap and law-40 gates"): final pass vs gates only vs gates + trims.

    python3 harness/skyglass_wreck_sim/tools/rulecap_tables.py [results_dir]

Reads results/final_*.json (final pass, d5957e79) and results/rulecap_{G,T,B,P}_*.json (this pass):
G = law-40 gates, pre-trim rules (--allow-over-cap); T = gates + trimmed rules; B = old gates + old rules at the
RUL-060 params (only where RUL-060 changed a fight's params); P = RUL-2026-10-31-067 feasibility probes.
"""
import json
import os
import sys

R = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")


def load(n):
    p = os.path.join(R, n)
    return json.load(open(p)) if os.path.exists(p) else None


def cell(x):
    return "-" if x is None else str(x)


def wreck(d):
    if not d:
        return None
    v = d["variants"][0]
    boss = [w for w in v["waves"] if w["wave"].startswith("F5W2")]
    horror = [e for e in v["enemiesOverall"] if e["name"] == "Core Horror"]
    return {
        "wipe": v["runsWithAWipePct"], "min": v["time"]["player15s_ai0s"]["minutesMedianAllRuns"],
        "boss": f"{boss[0]['wipedHere']}/{boss[0]['attempts']}" if boss else "-",
        "horrorSig": horror[0].get("signatureFiredPct") if horror else None,
        "unmarked": f"{d.get('fallbackGuard', {}).get('unmarkedCasts')}/{d.get('fallbackGuard', {}).get('setPieceCasts')}",
    }


def hunts(d):
    if not d:
        return {}
    out = {}
    for r in d["results"]:
        o = {"win": r["winPct"]}
        for f in r["fights"]:
            if f.get("captainPhases"):
                cp = f["captainPhases"]
                o["p2"] = f"{cp['phase2RoundsMedian']} (p90 {cp['phase2RoundsP90']})"
        out[r["path"]] = o
    return out


def charts(*ds):
    out = {}
    for d in ds:
        if not d:
            continue
        for r in d["results"]:
            n = r["runs"]
            out[(r["run"], r["variant"])] = {"clear": round(100 * r["baseClear"] / n, 1), "press": f"{r.get('pressOnWon')}/{r.get('pressOnReached')}"}
    return out


def crown(d):
    if not d:
        return {}
    return {k: v["summary"]["clearPct"] for k, v in d["chain"].items()}


def cc(d):
    if not d:
        return {}
    return {m: v["summary"]["winPct"] for m, v in d["modes"].items()}


def row(label, target, *vals):
    print(f"| {label} | {target} | " + " | ".join(cell(v) for v in vals) + " |")


def main():
    print("| Fight | Target | Final pass | Gates only | Gates + trims |")
    print("|---|---|---|---|---|")
    F, G, T = load("final_wreck_endgame.json"), load("rulecap_G_wreck_endgame.json"), load("rulecap_T_wreck_endgame.json")
    f, g, t = wreck(F), wreck(G), wreck(T)
    # 120-run check (seeds 61-120 added): runs with a wipe over both halves
    for x, n in ((g, "rulecap_G_wreck_endgame_s61.json"), (t, "rulecap_T_wreck_endgame_s61.json")):
        e = wreck(load(n))
        if x and e:
            x["wipe"] = f"{x['wipe']} (120 runs: {round((x['wipe'] + e['wipe']) / 2, 1)})"
    for k, lab, tg in (("min", "Endgame Wreck, minutes @15 s", "~22"), ("wipe", "Endgame Wreck, runs with a wipe %", "~17"),
                       ("boss", "Endgame boss wave wipes / attempts", "-"), ("horrorSig", "Endgame Core Horror signature %", "-"), ("unmarked", "Endgame unmarked set pieces", "0")):
        row(lab, tg, *(x and x.get(k) for x in (f, g, t)))
    f, g, t = (wreck(load(n)) for n in ("final_wreck_lvl50.json", "rulecap_G_wreck_lvl50.json", "rulecap_T_wreck_lvl50.json"))
    for k, lab, tg in (("min", "Level-50 Wreck, minutes @15 s", "-"), ("wipe", "Level-50 Wreck, runs with a wipe %", "~10"), ("unmarked", "Level-50 unmarked set pieces", "0")):
        row(lab, tg, *(x and x.get(k) for x in (f, g, t)))
    hf, hg, ht = hunts(load("final_hunts_dodge.json")), hunts(load("rulecap_G_hunts.json")), hunts(load("rulecap_T_hunts.json"))
    hb = hunts(load("rulecap_B_watch.json"))
    tg = {"foundry": "~80", "archive_clean": "> alarm", "archive_alarm1": "-", "archive_alarm3": "-", "watch_000": "~80 (pools 3)", "cache_right": "boss ~20% HP"}
    for p in ("foundry", "archive_clean", "archive_alarm1", "archive_alarm3", "watch_000", "cache_right"):
        extra = f" (old gates, pools 3: {hb[p]['win']})" if p in hb else ""
        row(f"Hunt {p}, clear %{extra}", tg[p], *(x.get(p, {}).get("win") for x in (hf, hg, ht)))
    row("Watch Captain phase 2 rounds", ">= 6-7", *(x.get("watch_000", {}).get("p2") for x in (hf, hg, ht)))
    cf = charts(load("final_charts_dodge_a.json"), load("final_charts_dodge_b.json"), load("final_charts_burning.json"))
    cg, ct, cb = charts(load("rulecap_G_charts.json")), charts(load("rulecap_T_charts.json")), charts(load("rulecap_B_reliquary.json"))
    tg = {"lowtide": "cut room", "nightwatch": "-", "reliquary": "~80 (2 rows)", "rotted": "~55", "steeping": "~75", "fall": "~80", "burning": "~55"}
    for run in ("lowtide", "nightwatch", "reliquary", "rotted", "steeping", "fall", "burning"):
        k = (run, "L100")
        extra = f" (old gates, 2 rows: {cb[k]['clear']})" if k in cb else ""
        row(f"Chart {run}, clear %{extra}", tg[run], *(x.get(k, {}).get("clear") for x in (cf, cg, ct)))
        row(f"Chart {run}, press-on won/reached", "-", *(x.get(k, {}).get("press") for x in (cf, cg, ct)))
    kt = {}
    for pol in ("clean", "alert", "war", "healing"):
        kt.update(crown(load(f"rulecap_T_crown_{pol}.json")))
    kf, kg, kb = crown(load("final_crownhold_chain.json")), crown(load("rulecap_G_crown.json")), crown(load("rulecap_B_crown_war.json"))
    for pol in ("healing", "clean", "alert", "war"):
        extra = f" (old gates, top-up: {kb[pol]})" if pol in kb else ""
        row(f"Crownhold {pol} route, clear %{extra}", "all routes clear", *(x.get(pol) for x in (kf, kg, kt)))
    sg, st = cc(load("rulecap_G_cc_solo.json")), cc(load("rulecap_T_cc_solo.json"))
    for m in ("dodge_on", "dodge_off"):
        row(f"Crowned Captain solo ({m}), win %", "-", None, sg.get(m), st.get(m))


if __name__ == "__main__":
    main()
