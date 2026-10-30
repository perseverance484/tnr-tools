#!/usr/bin/env python3
"""Collect the measured clear rates and run lengths for tools/economy.py from the final-pass result files.

    python3 harness/skyglass_wreck_sim/tools/economy_inputs.py --out harness/skyglass_wreck_sim/results/economy_inputs.json

Sources (results/, dodge on, L100 Kitsune + pet; minutes at 15 s per player turn):
- final_wreck_endgame.json: Wreck minutes (mean over runs, wipes included, AI 0 s).
- final_hunts_dodge.json: Buried Cache (cache_right), Foundry, Archive (clean), Watch (no terms); minutes = total rounds x 15 s.
- final_charts_dodge_a.json / _b.json: commons (L100), Epic and Legendary charts, steeping; base clear, base minutes,
  press-on win of reached.
- final_crownhold_chain.json: Crownhold (clean route).
- final_haul_exact_dodge.json: the Haul (sensible CLC route, mean over the six pages).
"""
import argparse
import json
import os

H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(H, "results")


def load(name):
    p = os.path.join(R, name)
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--press-on", type=float, default=0.5, help="share of clears where the player presses on")
    a = ap.parse_args()
    out = {"_sources": {}}
    w = load("final_wreck_endgame.json")
    if w:
        v = w["variants"][0]
        t = v["time"]["player15s_ai0s"]
        # Mean from median/p90 is not available per run: weight the clean-clear median and the wipe runs' p90.
        wipe = v["runsWithAWipePct"] / 100
        out["wreck"] = {"minutes": round((1 - wipe) * t["minutesMedianAllRuns"] + wipe * t["minutesP90"], 1)}
        out["_sources"]["wreck"] = "final_wreck_endgame.json"
    hu = load("final_hunts_dodge.json")
    if hu:
        by = {r["path"]: r for r in hu["results"]}
        for k, path in (("buried", "cache_right"), ("foundry", "foundry"), ("archive", "archive_clean"), ("watch", "watch_000")):
            if path in by:
                r = by[path]
                out[k] = {"clear": r["wins"] / r["runs"], "minutes": round(r["totalRoundsMedian"] * 15 / 60, 1), "pressOn": 0.0}
                out["_sources"][k] = f"final_hunts_dodge.json {path}"
    ch = [r for n in ("final_charts_dodge_a.json", "final_charts_dodge_b.json") for r in ((load(n) or {}).get("results") or [])]
    if ch:
        for r in ch:
            key = {"lowtide": "tide", "nightwatch": "roster", "reliquary": "reliquary", "fall": "fall", "rotted": "t_rel", "burning": "t_fall"}.get(r["run"])
            if not key or r["variant"] != "L100":
                continue
            out[key] = {"clear": r["baseClear"] / r["runs"], "minutes": r["baseMinutesMedian"], "pressOn": a.press_on,
                        "pressWin": (r["pressOnWon"] / r["pressOnReached"]) if r["pressOnReached"] else 0.0}
            out["_sources"][key] = f"final_charts_dodge_[ab].json {r['run']}"
    st = [x for x in ch if x["run"] == "steeping" and x["variant"] == "L100"]
    if st:
        r = st[0]
        out["steep"] = {"win": r["baseClear"] / r["runs"], "minutes": r["baseMinutesMedian"]}
        out["_sources"]["steep"] = "final_charts_dodge_a.json steeping"
    cr = load("final_crownhold_chain.json")
    if cr and cr.get("chain", {}).get("clean"):
        s = cr["chain"]["clean"]["summary"]
        rounds = [sum(f["rounds"] or 0 for f in c["fights"]) for c in cr["chain"]["clean"]["chains"] if c["outcome"] == "won"]
        mins = round((sorted(rounds)[len(rounds) // 2] if rounds else 90) * 15 / 60, 1)
        out["crown"] = {"clear": s["clearPct"] / 100, "minutes": mins}
        out["_sources"]["crown"] = "final_crownhold_chain.json clean"
    hx = load("final_haul_exact_dodge.json")
    if hx:
        rows = [p for r in hx["results"] for p in r["paths"] if p["path"] == "CLC"]
        if rows:
            out["haul"] = {"clear": sum(p["clearPct"] for p in rows) / len(rows) / 100, "minutes": round(sum(p["minutesClearMedian"] for p in rows) / len(rows), 1)}
            out["_sources"]["haul"] = "final_haul_exact_dodge.json CLC (mean of 6 pages)"
    json.dump(out, open(a.out, "w"), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
