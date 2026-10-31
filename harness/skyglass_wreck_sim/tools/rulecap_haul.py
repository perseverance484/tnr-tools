#!/usr/bin/env python3
"""Haul summary for the rule-cap pass: per page, the fitted sensible route (results/fit_haul_summary.json), greedy
clears and the best route as % of sensible, from exact (--paths) results files.

    python3 tools/rulecap_haul.py <label>=<file>[,<file>...] ...
"""
import json, os, sys
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")
fit = json.load(open(os.path.join(R, "fit_haul_summary.json")))["pages"]
PAGES = ["trophy", "bone", "snare", "overgrown", "vault", "bloom"]

def collect(files):
    by = {}
    for f in files:
        d = json.load(open(f))
        for r in d["results"]:
            for p in r["paths"]:
                by.setdefault(r["variant"], {})[p["path"]] = p
    return by

sets = [(a.split("=", 1)[0], collect(a.split("=", 1)[1].split(","))) for a in sys.argv[1:]]
print("| Page | Sensible route | " + " | ".join(f"{lab}: sensible clear % / EV M | {lab}: greedy LLLCC / CLLLC clear % | {lab}: best route vs sensible" for lab, _ in sets) + " |")
print("|---|---|" + "---|---|---|" * len(sets))
for pg in PAGES:
    sr = fit[pg]["sensibleRoute"]
    cells = []
    for lab, by in sets:
        P = by.get(pg, {})
        s = P.get(sr)
        g = "/".join(str(P[x]["clearPct"]) if x in P else "-" for x in ("LLLCC", "CLLLC"))
        if s and s["evM"]:
            best = max(P.values(), key=lambda p: p["evM"])
            cells += [f"{s['clearPct']} / {s['evM']}", g, f"{best['path']} {round(100 * best['evM'] / s['evM'])}%"]
        else:
            cells += ["-", g, "-"]
    print(f"| {pg} | {sr} | " + " | ".join(cells) + " |")
