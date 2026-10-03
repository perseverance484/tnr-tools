#!/usr/bin/env python3
"""Cross-bloodline balance matrix for Bloodright proposals.

Usage:
  python3 scripts/bloodright/balance_matrix.py [--check]

Reads every normalized tree under docs/design/bloodright/trees/ (Taiyo Kami
is the reference row), recomputes allocation audits with the shared library and
writes balance_matrix.json and BALANCE_MATRIX.md. Structural and arithmetic
comparison only; no combat simulation.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloodright_lib as L  # noqa: E402

TREES_DIR = L.TREES_DIR
REFERENCE_TREE = L.REFERENCE_TREE
OUT_JSON = os.path.join(L.DESIGN_DIR, "balance_matrix.json")
OUT_MD = os.path.join(L.DESIGN_DIR, "BALANCE_MATRIX.md")


def tree_entry(path: str, snapshot: dict, roster: dict, is_reference: bool) -> dict:
    tree = L.load_json(path)
    idx = L.census_index(snapshot, roster)
    bid = (tree.get("bloodline") or {}).get("id")
    if not bid:
        name = (tree.get("classification") or {}).get("bloodline", "").strip().lower()
        bid = next(k for k, v in idx.items() if v["kit"]["bloodline"]["name"].strip().lower() == name)
    kit = idx[bid]["kit"]
    rec = idx[bid]["record"] or {}
    rows = L.kit_rows(kit, tree.get("evaluation_level", L.DEFAULT_JUTSU_LEVEL))
    sup = [r for r in rows if r.supported]
    errors = L.validate_structure(tree)
    audit = L.audit_tree(tree, rows) if not errors else {}
    nodes = L.parse_nodes(tree)
    by_id = {n.id: n for n in nodes}
    rows_by_tag: dict[str, int] = {}
    for r in sup:
        rows_by_tag[r.tag] = rows_by_tag.get(r.tag, 0) + 1
    examples = []
    for ex in tree.get("examples", []):
        ids = [str(i) for i in ex.get("ids", [])]
        bon = L.bonuses_for(set(ids), by_id)
        examples.append({
            "name": ex.get("name"), "archetype": ex.get("archetype"), "ids": ids,
            "raw_flat_total": sum(bon.values()),
            "row_weighted_total": sum(bon[t] * rows_by_tag.get(t, 0) for t in L.SUPPORTED_TAGS),
            "bonuses": {t: bon[t] for t in L.SUPPORTED_TAGS if bon[t]},
        })
    cls = tree.get("classification", {})
    em = tree.get("emphasis") or {}
    strongest = audit.get("strongest_full_build_by_row_weight") if audit else None
    weakest = audit.get("lowest_value_node_by_row_weight") if audit else None
    jutsu_count = len(kit.get("public_jutsu", [])) + len(kit.get("hidden_jutsu", []))
    return {
        "slug": L.slugify(kit["bloodline"]["name"]),
        "review_id": rec.get("review_id"),
        "name": kit["bloodline"]["name"].strip(),
        "rank": kit["bloodline"].get("rank"),
        "reference": is_reference,
        "jutsu_in_kit": jutsu_count,
        "supported_rows": len(sup),
        "supported_rows_by_tag": rows_by_tag,
        "adverse_supported_rows": sum(1 for r in sup if r.adverse),
        "classification": cls.get("potency_classification"),
        "label_kind": cls.get("label_kind"),
        "classification_status": cls.get("classification_status"),
        "routes": [{"name": r["name"], "primary_tag": r["primary_tag"], "total": r["total"], "on_band": r["total"] in L.ROUTE_BANDS}
                   for r in L.route_totals(by_id)] if not errors else [],
        "director_exceptions": tree.get("director_exceptions") or [],
        "emphasis": {k: em.get(k) for k in ("primary", "secondary", "tertiary")},
        "nodes": len(nodes),
        "tiers": {"F": sum(1 for n in nodes if n.category == "Foundation"),
                  "H": sum(1 for n in nodes if n.category == "Hidden Art"),
                  "A": sum(1 for n in nodes if n.category == "Advanced Art")},
        "structure_errors": errors,
        "full_budget_allocations": audit.get("full_budget_allocations"),
        "non_dominated_full_allocations": audit.get("non_dominated_full_allocations"),
        "maximum_advanced_arts": audit.get("maximum_advanced_arts"),
        "minimum_two_advanced_cost": audit.get("minimum_two_advanced_cost"),
        "maximum_depth": audit.get("maximum_depth"),
        "maximum_tag_bonuses": audit.get("maximum_tag_bonuses"),
        "max_full_build_raw_flat_total": max((b["raw_flat_total"] for b in audit.get("full_builds", [])), default=None),
        "max_full_build_row_weighted_total": strongest["row_weighted_total"] if strongest else None,
        "max_row_weighted_per_supported_row": (round(strongest["row_weighted_total"] / len(sup), 2) if strongest and sup else None),
        "median_full_build_row_weighted_total": (sorted(b["row_weighted_total"] for b in audit["full_builds"])[len(audit["full_builds"]) // 2] if audit.get("full_builds") else None),
        "strongest_full_build": {"ids": strongest["ids"], "names": [by_id[i].name for i in strongest["ids"]],
                                 "bonuses": strongest["bonuses"]} if strongest else None,
        "lowest_value_node": {"name": weakest["name"], "row_weighted_total": weakest["row_weighted_total"]} if weakest else None,
        "nodes_absent_from_non_dominated_builds": audit.get("nodes_absent_from_non_dominated_builds"),
        "examples": examples,
        "narrow_kit_exception": tree.get("narrow_kit_exception"),
        "tags_not_targeted": audit.get("supported_tags_in_kit_not_targeted"),
    }


def build_matrix() -> dict:
    snapshot = L.load_snapshot()
    roster = L.load_roster()
    entries = [tree_entry(REFERENCE_TREE, snapshot, roster, True)]
    for p in sorted(glob.glob(os.path.join(TREES_DIR, "*.json"))):
        if p.endswith(".validation.json") or os.path.abspath(p) == os.path.abspath(REFERENCE_TREE):
            continue
        entries.append(tree_entry(p, snapshot, roster, False))
    approved = set(roster["approved_remaining_ids"])
    idx = L.census_index(snapshot, roster)
    covered = {e["review_id"] for e in entries if not e["reference"]}
    missing = [{"review_id": idx[b]["record"]["review_id"], "name": idx[b]["kit"]["bloodline"]["name"].strip()}
               for b in roster["approved_remaining_ids"] if idx[b]["record"]["review_id"] not in covered]
    ref = entries[0]
    for e in entries:
        e["vs_reference"] = {
            "max_raw_flat_total_delta": (e["max_full_build_raw_flat_total"] or 0) - (ref["max_full_build_raw_flat_total"] or 0),
            "max_row_weighted_delta": (e["max_full_build_row_weighted_total"] or 0) - (ref["max_full_build_row_weighted_total"] or 0),
            "supported_rows_delta": e["supported_rows"] - ref["supported_rows"],
        }
    return {
        "kind": "bloodright_balance_matrix",
        "method": ("Same access budget (4 BP, 1 BP per once-only skill, forks only) for every tree. Raw flat total "
                   "sums every static addition in a legal full allocation; row-weighted total multiplies each addition "
                   "by the number of supported kit rows it reaches. Both are structural/arithmetic measures, not combat "
                   "strength. Inherited kit strength (rank, row count, baseline values) is listed separately from the "
                   "Bloodright additions."),
        "reference": "Taiyo Kami (docs/design/bloodright/trees/taiyo_kami.json; approved values, regenerated)",
        "game_source_pin": L.GAME_SOURCE_PIN,
        "approved_remaining": len(approved),
        "trees_present": len(entries) - 1,
        "approved_without_tree": missing,
        "entries": entries,
        "combat_simulation_performed": False,
    }


def md_matrix(m: dict) -> str:
    out = ["# Bloodright cross-bloodline balance matrix\n", m["method"] + "\n",
           f"Reference: {m['reference']}. Trees present: {m['trees_present']} of {m['approved_remaining']} approved remaining bloodlines" +
           (f"; without a tree: {', '.join(x['name'] for x in m['approved_without_tree'])}" if m["approved_without_tree"] else "") +
           ". No combat simulation was performed.\n"]
    out.append("## Structure and access\n")
    out.append("| Bloodline | Rank | Jutsu | Supp. rows | Adverse | Label (kind) | Nodes F/H/A | Legal 4-BP | Non-dom | Max adv | Min 2-adv cost | Depth | Errors |")
    out.append("|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|")
    for e in m["entries"]:
        tag = " (reference)" if e["reference"] else ""
        out.append(f"| {e['name']}{tag} | {e['rank']} | {e['jutsu_in_kit']} | {e['supported_rows']} | {e['adverse_supported_rows']} | "
                   f"{e['classification']} ({L.short_kind(e['label_kind'])}) | "
                   f"{e['tiers']['F']}/{e['tiers']['H']}/{e['tiers']['A']} | {e['full_budget_allocations']} | {e['non_dominated_full_allocations']} | "
                   f"{e['maximum_advanced_arts']} | {e['minimum_two_advanced_cost']} | {e['maximum_depth']} | {len(e['structure_errors'])} |")
    out.append("\n## Added strength (Bloodright only)\n")
    out.append("| Bloodline | Emphasis (P / S / T) | Max per-tag additions | Max raw total | Δ vs ref | Max row-weighted | Δ vs ref | Per supported row | Median build | Strongest full build | Lowest node |")
    out.append("|---|---|---|---:|---:|---:|---:|---:|---:|---|---|")
    for e in m["entries"]:
        em = e["emphasis"]
        emtxt = " / ".join(str(em.get(k) or "—") for k in ("primary", "secondary", "tertiary"))
        mx = ", ".join(L.mod_text(k, v, abbr=True) for k, v in (e["maximum_tag_bonuses"] or {}).items())
        sb = e["strongest_full_build"]
        sbt = (", ".join(sb["names"]) + " (" + ", ".join(L.mod_text(k, v, abbr=True) for k, v in sb["bonuses"].items() if v) + ")") if sb else "—"
        lw = e["lowest_value_node"]
        lwt = f"{lw['name']} ({lw['row_weighted_total']})" if lw else "—"
        out.append(f"| {e['name']} | {emtxt} | {mx} | {e['max_full_build_raw_flat_total']} | {e['vs_reference']['max_raw_flat_total_delta']:+d} | "
                   f"{e['max_full_build_row_weighted_total']} | {e['vs_reference']['max_row_weighted_delta']:+d} | {e['max_row_weighted_per_supported_row']} | {e['median_full_build_row_weighted_total']} | {sbt} | {lwt} |")
    out.append("\n## Example builds\n")
    out.append("| Bloodline | Build | Purchases | Raw total | Row-weighted | Bonuses |\n|---|---|---|---:|---:|---|")
    for e in m["entries"]:
        for ex in e["examples"]:
            bon = ", ".join(L.mod_text(k, v, abbr=True) for k, v in ex["bonuses"].items())
            out.append(f"| {e['name']} | {ex['name']} ({ex['archetype']}) | {', '.join(ex['ids'])} | {ex['raw_flat_total']} | {ex['row_weighted_total']} | {bon} |")
    out.append("\n## Coverage gaps and exceptions\n")
    for e in m["entries"]:
        bits = []
        if e["tags_not_targeted"]:
            bits.append("untargeted supported tags: " + ", ".join(e["tags_not_targeted"]))
        if e["nodes_absent_from_non_dominated_builds"]:
            bits.append("nodes outside every non-dominated build: " + ", ".join(e["nodes_absent_from_non_dominated_builds"]))
        if e["narrow_kit_exception"]:
            bits.append("narrow-kit exception: " + e["narrow_kit_exception"])
        if e["adverse_supported_rows"]:
            bits.append(f"{e['adverse_supported_rows']} adverse supported row(s) in kit")
        if e["label_kind"] != "element":
            bits.append(f"classification: {e['classification_status']}")
        off = [r for r in e["routes"] if not r["on_band"]]
        if off:
            bits.append("routes off the 5/10/15 bands: " + ", ".join(f"{r['name']} {L.mod_text(r['primary_tag'], r['total'], abbr=True)}" for r in off))
        if e["director_exceptions"]:
            bits.append("director-review exceptions: " + ", ".join(f"{L.TAG_ABBR.get(x.get('tag'), x.get('tag'))} up to +{x.get('max')}%" for x in e["director_exceptions"]))
        if bits:
            out.append(f"- **{e['name']}:** " + "; ".join(bits))
    # outliers by per-row intensity
    vals = [(e["max_row_weighted_per_supported_row"], e["name"]) for e in m["entries"] if e["max_row_weighted_per_supported_row"] is not None]
    if vals:
        ref = next((v for v, n in vals if n == m["entries"][0]["name"]), None)
        hi = [f"{n} ({v})" for v, n in sorted(vals, reverse=True) if ref is not None and v > ref * 1.25]
        lo = [f"{n} ({v})" for v, n in sorted(vals) if ref is not None and v < ref * 0.75]
        out.append(f"\n## Outliers by per-row intensity (reference {ref})\n")
        out.append("- Above 125% of the reference: " + (", ".join(hi) or "none"))
        out.append("- Below 75% of the reference: " + (", ".join(lo) or "none"))
    out.append("\nReading guide: a higher row-weighted total means the same static additions touch more effect rows; it says nothing about delivery, uptime, action cost, duration, caps (percentage tags cap at 100; Afterburn, Reflect and the lifesteal/vamp leech budget cap at 60% of a hit) or the combat multiplication that follows. Mechanical legality and numerical non-dominance do not prove combat balance.\n")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    m = build_matrix()
    jtxt = json.dumps(m, indent=2, ensure_ascii=False) + "\n"
    mtxt = md_matrix(m)
    if args.check:
        stale = [p for p, txt in ((OUT_JSON, jtxt), (OUT_MD, mtxt))
                 if not os.path.exists(p) or open(p, encoding="utf-8").read() != txt]
        if stale:
            print("STALE: " + ", ".join(stale))
            return 2
        print("balance matrix current")
        return 0
    L.write_text(OUT_JSON, jtxt)
    L.write_text(OUT_MD, mtxt)
    print(f"wrote {OUT_MD} ({m['trees_present']} trees + reference)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
