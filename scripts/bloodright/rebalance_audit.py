#!/usr/bin/env python3
"""Roster-wide review audit for Bloodright trees (BALANCE_REVIEW_METHOD.md).

  python3 scripts/bloodright/rebalance_audit.py [--check]
  python3 scripts/bloodright/rebalance_audit.py --tree <slug>   # print one tree's audit

Writes docs/design/bloodright/REBALANCE_AUDIT.md and rebalance_audit.json from the
normalized trees and the committed kit snapshot:

- Damage tiers: every supported Damage row, base -> final for every flat Damage total
  a legal allocation reaches, with tier crossings and anything above the 50 Nuke tier;
- Fourth-BP audit: each Advanced Art's three-purchase package and every legal fourth;
- Route overlap: Advanced Arts sharing a primary tag or most of their package;
- Coverage: supported rows, distinct jutsu and base values per tag.

It surfaces evidence for design review. It does not score trees or choose values.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloodright_lib as L  # noqa: E402

OUT_MD = os.path.join(L.DESIGN_DIR, "REBALANCE_AUDIT.md")
OUT_JSON = os.path.join(L.DESIGN_DIR, "rebalance_audit.json")


def tree_paths() -> list[str]:
    return sorted(p for p in glob.glob(os.path.join(L.TREES_DIR, "*.json")) if not p.endswith(".validation.json"))


def coverage(rows: list[L.Row]) -> dict:
    out: dict[str, dict] = {}
    for r in rows:
        if not r.supported:
            continue
        c = out.setdefault(r.tag, {"rows": 0, "jutsu": set(), "bases": [], "recipients": set()})
        c["rows"] += 1
        c["jutsu"].add(r.jutsu_name)
        c["bases"].append(r.base)
        c["recipients"].add(r.recipient)
    return {t: {"rows": v["rows"], "jutsu": sorted(v["jutsu"]), "bases": sorted(v["bases"]),
                "recipients": sorted(v["recipients"])} for t, v in sorted(out.items())}


def entry(path: str, idx: dict) -> dict:
    t = L.load_json(path)
    kit = idx[t["bloodline"]["id"]]["kit"]
    rows = L.kit_rows(kit, t.get("evaluation_level", L.DEFAULT_JUTSU_LEVEL))
    slug = os.path.basename(path)[:-5]
    return {
        "slug": slug,
        "name": t["bloodline"]["name"],
        "revision": t.get("revision"),
        "reference": os.path.abspath(path) == os.path.abspath(L.REFERENCE_TREE),
        "above_nuke_rationale": t.get("above_nuke_rationale"),
        "damage": L.damage_threshold_audit(t, rows),
        "fourth_bp": L.fourth_bp_audit(t, rows),
        "route_overlap": L.route_overlap(t),
        "routes": L.route_totals({n.id: n for n in L.parse_nodes(t)}),
        "coverage": coverage(rows),
    }


def build() -> dict:
    idx = L.census_index(L.load_snapshot(), L.load_roster())
    entries = [entry(p, idx) for p in tree_paths()]
    above = [{"bloodline": e["name"], **x, "rationale": bool(e["above_nuke_rationale"])}
             for e in entries for x in e["damage"]["above_nuke"]]
    high_to_nuke = sorted({(e["name"], r["jutsu"], r["base"], st["added"], st["final"])
                           for e in entries for r in e["damage"]["rows"] for st in r["steps"]
                           if r["base"] < L.NUKE <= st["final"] and r["base"] >= 45})
    return {
        "kind": "bloodright_rebalance_audit",
        "method": "docs/design/bloodright/BALANCE_REVIEW_METHOD.md",
        "game_source_pin": L.GAME_SOURCE_PIN,
        "damage_tiers": {name: floor for floor, name in L.DAMAGE_TIERS},
        "trees": len(entries),
        "summary": {
            "trees_with_damage_nodes": sorted(e["name"] for e in entries if e["damage"]["damage_totals_reachable"]),
            "max_damage_by_tree": {e["name"]: max(e["damage"]["damage_totals_reachable"] or [0]) for e in entries},
            "above_nuke": above,
            "high_to_nuke": [list(x) for x in high_to_nuke],
            "same_primary_overlaps": [{"bloodline": e["name"], **ov} for e in entries for ov in e["route_overlap"] if ov["same_primary_tag"]],
        },
        "entries": entries,
        "combat_simulation_performed": False,
    }


def fmt_pkg(b: dict) -> str:
    return ", ".join(L.mod_text(k, v, abbr=True) for k, v in b.items()) or "—"


def tree_md(e: dict) -> list[str]:
    out = [f"### {e['name']}{' (reference)' if e['reference'] else ''}\n"]
    cov = e["coverage"]
    out.append("Coverage: " + "; ".join(f"{L.TAG_ABBR[t]} {c['rows']} row(s) on {len(c['jutsu'])} jutsu (bases {', '.join(f'{b:g}' for b in c['bases'])})" for t, c in cov.items()) + ".\n")
    d = e["damage"]
    if d["rows"] and d["damage_totals_reachable"]:
        cells = []
        for r in d["rows"]:
            steps = " / ".join(f"{s['final']:g}" + (" (above Nuke)" if s["above_nuke"] else (" ↑" if s["tier_change"] else "")) for s in r["steps"])
            cells.append(f"{r['jutsu']} {r['base']:g} → {steps}")
        out.append(f"Damage (+{', +'.join(str(x) for x in d['damage_totals_reachable'])}): " + "; ".join(cells) + ".")
        if e["above_nuke_rationale"]:
            out.append(f"  Above-Nuke rationale: {e['above_nuke_rationale']}")
        out.append("")
    elif d["rows"]:
        out.append("Damage: no node adds flat Damage (" + ", ".join(f"{r['jutsu']} {r['base']:g}" for r in d["rows"]) + ").\n")
    out.append("| Advanced Art | Route (primary) | Path package | Highest-diagnostic fourth | Full package |\n|---|---|---|---|---|")
    routes = {r["advanced_art"]: r for r in e["routes"]}
    for fb in e["fourth_bp"]:
        r = routes.get(fb["advanced_art"])
        top = next((f for f in fb["fourths"] if f["id"] == fb["highest_diagnostic_fourth"]), None)
        out.append(f"| {fb['name']} | {L.mod_text(r['primary_tag'], r['total']) if r else '—'} | {fmt_pkg(fb['path_bonuses'])} | "
                   f"{top['name'] if top else '—'} | {fmt_pkg(top['bonuses']) if top else '—'} |")
    if e["route_overlap"]:
        out.append("\nOverlap: " + "; ".join(f"{o['a_name']} / {o['b_name']} ({'same primary tag' if o['same_primary_tag'] else 'similar'}, cosine {o['path_cosine']})" for o in e["route_overlap"]) + ".")
    out.append("")
    return out


def md(d: dict) -> str:
    s = d["summary"]
    out = ["# Bloodright rebalance audit\n",
           "Generated by `scripts/bloodright/rebalance_audit.py` for review under `BALANCE_REVIEW_METHOD.md`. "
           "It lists evidence (damage tiers, fourth purchases, overlapping routes, coverage); it does not score trees or choose values. "
           "Player-jutsu damage tiers: 38 Light, 40 Normal, 45 High, 50 Nuke. Per-tree tables with every fourth purchase are in each tree's Markdown.\n",
           "## Roster summary\n",
           f"- Trees audited: {d['trees']} (including the Taiyo Kami reference).",
           f"- Trees with flat Damage nodes: {len(s['trees_with_damage_nodes'])}.",
           "- Maximum flat Damage by tree: " + ", ".join(f"{k} +{v}" for k, v in sorted(s["max_damage_by_tree"].items()) if v) + ".",
           f"- Damage results above the 50 Nuke tier: {len(s['above_nuke'])}" +
           (" — " + "; ".join(f"{x['bloodline']}: {x['jutsu']} {x['base']:g} → {x['final']:g}{'' if x['rationale'] else ' (NO RATIONALE)'}" for x in s["above_nuke"]) if s["above_nuke"] else "") + ".",
           f"- High (45) rows reaching the 50 Nuke tier: {len(s['high_to_nuke'])}" +
           (" — " + "; ".join(f"{b}: {j} {base:g} → {fin:g} (+{add})" for b, j, base, add, fin in s["high_to_nuke"]) if s["high_to_nuke"] else "") + ".",
           f"- Advanced Arts sharing a primary tag: {len(s['same_primary_overlaps'])}" +
           (" — " + "; ".join(f"{o['bloodline']}: {o['a_name']} / {o['b_name']}" for o in s["same_primary_overlaps"]) if s["same_primary_overlaps"] else "") + ".",
           "\n## Trees\n"]
    for e in d["entries"]:
        out += tree_md(e)
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--tree", help="print one tree's audit (slug) and exit")
    args = ap.parse_args()
    if args.tree:
        idx = L.census_index(L.load_snapshot(), L.load_roster())
        e = entry(os.path.join(L.TREES_DIR, args.tree + ".json"), idx)
        print("\n".join(tree_md(e)))
        for fb in e["fourth_bp"]:
            print(f"Fourth-BP {fb['name']} (path {fmt_pkg(fb['path_bonuses'])}):")
            for f in fb["fourths"]:
                print(f"  + {f['name']} [{f['category']}] -> {fmt_pkg(f['bonuses'])} (row-weighted {f['row_weighted']})")
        return 0
    d = build()
    jt = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    mt = md(d)
    if args.check:
        stale = [p for p, t in ((OUT_JSON, jt), (OUT_MD, mt)) if not os.path.exists(p) or open(p, encoding="utf-8").read() != t]
        if stale:
            print("STALE " + ", ".join(stale))
            return 2
        print("rebalance audit current")
        return 0
    L.write_text(OUT_JSON, jt)
    L.write_text(OUT_MD, mt)
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
