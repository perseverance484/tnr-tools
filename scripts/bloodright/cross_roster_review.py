#!/usr/bin/env python3
"""Phase 3 cross-roster review for Bloodright proposals.

  python3 scripts/bloodright/cross_roster_review.py [--check]

Recomputes, from every normalized tree (Taiyo Kami as the reference row) and the
committed kit snapshot, the roster-wide checks the planning brief asks for:
strongest found combinations, worst-value purchases, stacked exposure and
self-amplification, sustain/reflect/afterburn ceilings against engine caps,
percentage caps, RUL-2026-10-03-005 ceilings and route bands, delivery and item
constraints, injection, universal nodes, element-wide classification status, and
inherited versus added strength. Writes
CROSS_ROSTER_REVIEW.md and cross_roster_review.json. Arithmetic only; no
combat simulation.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloodright_lib as L  # noqa: E402

TREES = L.TREES_DIR
REF = L.REFERENCE_TREE
OUT_MD = os.path.join(L.DESIGN_DIR, "CROSS_ROSTER_REVIEW.md")
OUT_JSON = os.path.join(L.DESIGN_DIR, "cross_roster_review.json")
REVIEW_LOG = os.path.join(L.DESIGN_DIR, "review_log.json")


def _prod(vals):
    out = 1.0
    for v in vals:
        out *= v
    return out


def load_entries():
    snap = L.load_snapshot()
    roster = L.load_roster()
    idx = L.census_index(snap, roster)
    paths = [REF] + sorted(p for p in glob.glob(os.path.join(TREES, "*.json"))
                           if not p.endswith(".validation.json") and os.path.abspath(p) != os.path.abspath(REF))
    out = []
    for p in paths:
        t = L.load_json(p)
        bid = t["bloodline"]["id"]
        kit = idx[bid]["kit"]
        rec = idx[bid]["record"]
        rows = L.kit_rows(kit, t.get("evaluation_level", L.DEFAULT_JUTSU_LEVEL))
        nodes = L.parse_nodes(t)
        by_id = {n.id: n for n in nodes}
        audit = L.audit_tree(t, rows)
        out.append({"path": p, "tree": t, "kit": kit, "rec": rec, "rows": rows, "by_id": by_id, "audit": audit,
                    "name": kit["bloodline"]["name"].strip(), "reference": p == REF})
    return out, snap


def finals_max(entry, tag):
    """Max final value over legal full builds for every row of `tag`, plus the summed stack."""
    rows = [r for r in entry["rows"] if r.supported and r.tag == tag]
    if not rows:
        return None
    best = None
    for b in entry["audit"]["full_builds"]:
        add = b["bonuses"].get(tag, 0)
        finals = [min(100.0, r.base + add) if r.calculation == "percentage" else r.base + add for r in rows]
        tot = sum(finals)
        if best is None or tot > best[0]:
            best = (tot, add, finals, b["ids"])
    base_tot = sum(r.base for r in rows)
    return {"rows": len(rows), "base_sum": round(base_tot, 2), "max_sum": round(best[0], 2), "addition": best[1],
            "max_single": round(max(best[2]), 2), "build": best[3],
            "recipients": sorted({r.recipient for r in rows})}


def build():
    entries, snap = load_entries()
    review = L.load_json(REVIEW_LOG) if os.path.exists(REVIEW_LOG) else {}
    data = {"kind": "bloodright_cross_roster_review", "game_source_pin": L.GAME_SOURCE_PIN,
            "trees": len(entries) - 1, "combat_simulation_performed": False}
    # 1. strongest combinations
    builds = []
    nodes_all = []
    for e in entries:
        sup = [r for r in e["rows"] if r.supported]
        for b in e["audit"]["full_builds"]:
            builds.append({"bloodline": e["name"], "reference": e["reference"], "ids": b["ids"],
                           "names": [e["by_id"][i].name for i in b["ids"]], "raw": b["raw_flat_total"],
                           "row_weighted": b["row_weighted_total"],
                           "per_row": round(b["row_weighted_total"] / max(1, len(sup)), 2),
                           "bonuses": b["bonuses"], "non_dominated": b["non_dominated"]})
        for nv in e["audit"]["node_values"]:
            nodes_all.append({"bloodline": e["name"], "reference": e["reference"], **{k: nv[k] for k in ("id", "name", "category", "depth", "raw_flat_total", "row_weighted_total", "covered_rows")}})
    data["strongest_by_row_weight"] = sorted(builds, key=lambda b: (-b["row_weighted"], -b["raw"]))[:12]
    data["strongest_by_raw"] = sorted(builds, key=lambda b: (-b["raw"], -b["row_weighted"]))[:12]
    data["strongest_by_per_row"] = sorted(builds, key=lambda b: (-b["per_row"], -b["raw"]))[:12]
    data["dominated_builds"] = [b for b in builds if not b["non_dominated"]]
    adv = [n for n in nodes_all if n["category"] == "Advanced Art"]
    data["weakest_advanced_arts"] = sorted(adv, key=lambda n: (n["row_weighted_total"], n["raw_flat_total"]))[:12]
    data["weakest_purchases"] = sorted(nodes_all, key=lambda n: (n["row_weighted_total"], n["raw_flat_total"]))[:12]
    # 2. tag ceilings vs caps
    tagrep = {}
    for tag in L.SUPPORTED_TAGS:
        lst = []
        for e in entries:
            fm = finals_max(e, tag)
            if fm and fm["addition"]:
                lst.append({"bloodline": e["name"], **fm})
        tagrep[tag] = sorted(lst, key=lambda x: -x["max_single"])
    data["tag_ceilings"] = tagrep
    # stacked exposure / self amplification
    def stack(tag, recipient):
        out = []
        for e in entries:
            rows = [r for r in e["rows"] if r.supported and r.tag == tag and r.recipient == recipient]
            if len(rows) < 2:
                continue
            add = e["audit"]["maximum_tag_bonuses"].get(tag, 0)
            # computeDamagePacket (process.ts 1692-1825): stage-2 increases multiply in turn,
            # percentage reductions apply sequentially as (1 - p); the 90% DR floor is ignored here.
            if tag in ("increasedamagegiven", "increasedamagetaken"):
                comb = lambda vals: _prod(1 + v / 100 for v in vals)
            else:
                comb = lambda vals: _prod(1 - v / 100 for v in vals)
            out.append({"bloodline": e["name"], "rows": len(rows),
                        "base_multiplier": round(comb([r.base for r in rows]), 3),
                        "max_multiplier": round(comb([min(100.0, r.base + add) for r in rows]), 3), "addition": add,
                        "jutsu": sorted({r.jutsu_name for r in rows})})
        rev = tag in ("increasedamagegiven", "increasedamagetaken")
        return sorted(out, key=lambda x: -x["max_multiplier"] if rev else x["max_multiplier"])
    data["stacked_enemy_exposure"] = stack("increasedamagetaken", "enemy")
    data["stacked_self_idg"] = stack("increasedamagegiven", "self")
    data["stacked_self_ddt"] = stack("decreasedamagetaken", "self")
    data["stacked_enemy_ddg"] = stack("decreasedamagegiven", "enemy")
    # 3. caps
    caps = []
    for e in entries:
        for b in e["audit"]["full_builds"]:
            for r in e["rows"]:
                if r.supported and r.calculation == "percentage" and r.base + b["bonuses"].get(r.tag, 0) > 100:
                    caps.append({"bloodline": e["name"], "jutsu": r.jutsu_name, "row": r.row, "tag": r.tag})
    data["percentage_rows_over_100"] = caps
    # 3b. RUL-2026-10-03-005 ceilings and route bands over every legal allocation
    ceil = []
    for e in entries:
        errs, warns, rep = L.ceiling_findings(e["tree"])
        ceil.append({"bloodline": e["name"], "reference": e["reference"],
                     "maximum": rep["maximum_over_all_legal_allocations"],
                     "over_ceiling": [t for t, v in rep["maximum_over_all_legal_allocations"].items() if v > L.ceiling_for(t)],
                     "routes": [{"name": r["name"], "primary_tag": r["primary_tag"], "total": r["total"],
                                 "steps": r["steps"], "on_band": r["on_band"], "band_rationale": r.get("band_rationale")}
                                for r in rep["routes"]],
                     "director_exceptions": rep["director_exceptions"], "errors": errs})
    data["ceilings"] = ceil
    # 4. delivery / gates / injection / universal / adverse / hazards / classification
    deliv = []
    for e in entries:
        sup = [r for r in e["rows"] if r.supported]
        gated_tags = sorted({r.tag for r in sup} - {r.tag for r in sup if not r.item_gate}) if any(r.item_gate for r in sup) else []
        hidden_tags = sorted({r.tag for r in sup if r.visibility == "hidden"})
        mode = sorted({f"{r.jutsu_name} ({r.usage})" for r in sup if r.usage not in (None, "BOTH")})
        inj = L.injected_children(e["kit"], snap)
        universal = [n for n in e["by_id"] if e["audit"]["full_builds"] and all(n in b["ids"] for b in e["audit"]["full_builds"])]
        cls = e["tree"].get("classification", {})
        qual = cls.get("qualifying_elements") or []
        deliv.append({"bloodline": e["name"], "rank": e["kit"]["bloodline"].get("rank"),
                      "label": cls.get("potency_classification"), "label_kind": cls.get("label_kind"),
                      "classification_status": cls.get("classification_status"),
                      "shared_element_bloodlines": len(cls.get("shared_element_bloodlines") or []),
                      "authored_classification_jutsu": cls.get("kit_jutsu_by_authored_classification") or [],
                      "rows_matching_label_directly": sum(1 for r in sup if any(q in r.elements_effective for q in qual)),
                      "rows_none_fallback": sum(1 for r in sup if r.elements_effective == ["None"]),
                      "supported_rows": len(sup),
                      "tags_only_on_gated_rows": gated_tags, "tags_with_hidden_rows": hidden_tags,
                      "mode_restricted": mode, "injected_children": [f"{c['child_name']} (bloodlineId {'match' if c['child_bloodline_id'] == e['kit']['bloodline']['id'] else (c['child_bloodline_id'] or 'none')})" for c in inj],
                      "universal_nodes": [e["by_id"][n].name for n in universal],
                      "adverse_rows": [f"{r.jutsu_name}#{r.row} {r.tag}" for r in sup if r.adverse],
                      "ally_hazard_rows": [f"{r.jutsu_name}#{r.row} {r.tag}" for r in sup if r.ally_hazard],
                      "enemy_hazard_rows": [f"{r.jutsu_name}#{r.row} {r.tag}" for r in sup if r.enemy_hazard],
                      "repeated_rows_on_one_jutsu": sorted({f"{r.jutsu_name} {r.tag}" for r in sup if sum(1 for q in sup if q.jutsu_name == r.jutsu_name and q.tag == r.tag) > 1})})
    data["delivery_and_scope"] = deliv
    # 5. inherited vs added
    inh = []
    for e in entries:
        sup = [r for r in e["rows"] if r.supported]
        dmg = [r.base for r in sup if r.tag == "damage"]
        pct = [r.base for r in sup if r.calculation == "percentage"]
        strongest = max((b["row_weighted_total"] for b in e["audit"]["full_builds"]), default=0)
        inh.append({"bloodline": e["name"], "rank": e["kit"]["bloodline"].get("rank"),
                    "jutsu": len(e["kit"].get("public_jutsu", [])) + len(e["kit"].get("hidden_jutsu", [])),
                    "supported_rows": len(sup), "damage_rows": len(dmg), "damage_base_sum": round(sum(dmg), 1),
                    "percentage_rows": len(pct), "percentage_base_sum": round(sum(pct), 1),
                    "added_max_row_weighted": strongest,
                    "added_share_of_inherited_pct": round(100 * strongest / max(1, sum(dmg) + sum(pct)), 1)})
    data["inherited_vs_added"] = sorted(inh, key=lambda x: x["bloodline"])
    data["review_log"] = review
    return data


def md(d):
    out = ["# Bloodright cross-roster review\n",
           f"Generated by `scripts/bloodright/cross_roster_review.py` over {d['trees']} drafted trees plus the Taiyo Kami reference, using the committed kit snapshot and mechanics read at `studie-tech/TheNinjaRPG@{d['game_source_pin']}`. "
           "Every number is a static per-row addition from the legal-allocation enumeration; no combat simulation was performed, so nothing here certifies equal combat strength, an ideal build or win rates.\n"]
    def tbl(rows, cols, heads):
        o = ["| " + " | ".join(heads) + " |", "|" + "|".join("---" for _ in heads) + "|"]
        for r in rows:
            o.append("| " + " | ".join(str(c(r)) for c in cols) + " |")
        return o
    bon = lambda b: ", ".join(L.mod_text(k, v, abbr=True) for k, v in b["bonuses"].items())
    out.append("## 1. Strongest found combinations\n")
    out.append("Row-weighted total = Σ (addition × supported rows of that tag). It favours kits with many rows; per-row intensity divides by the kit's supported rows.\n")
    out.append("**By row-weighted total**\n")
    out += tbl(d["strongest_by_row_weight"], [lambda b: b["bloodline"], lambda b: ", ".join(b["names"]), lambda b: b["row_weighted"], lambda b: b["raw"], lambda b: b["per_row"], bon],
               ["Bloodline", "Build", "Row-weighted", "Raw", "Per row", "Additions"])
    out.append("\n**By per-row intensity**\n")
    out += tbl(d["strongest_by_per_row"], [lambda b: b["bloodline"], lambda b: ", ".join(b["names"]), lambda b: b["per_row"], lambda b: b["row_weighted"], bon],
               ["Bloodline", "Build", "Per row", "Row-weighted", "Additions"])
    out.append("\n**By raw flat total**\n")
    out += tbl(d["strongest_by_raw"], [lambda b: b["bloodline"], lambda b: ", ".join(b["names"]), lambda b: b["raw"], lambda b: b["row_weighted"], bon],
               ["Bloodline", "Build", "Raw", "Row-weighted", "Additions"])
    out.append(f"\nDominated legal full builds across the roster: {len(d['dominated_builds'])}" +
               ("" if not d["dominated_builds"] else " — " + "; ".join(f"{b['bloodline']}: {', '.join(b['names'])}" for b in d["dominated_builds"])) + ". A dominated build is legal but worse on every tag than another legal build of the same tree.\n")
    out.append("## 2. Worst-value purchases\n")
    out += tbl(d["weakest_advanced_arts"], [lambda n: n["bloodline"], lambda n: n["name"], lambda n: n["row_weighted_total"], lambda n: n["raw_flat_total"], lambda n: n["covered_rows"]],
               ["Bloodline", "Weakest Advanced Arts", "Row-weighted", "Raw", "Rows reached"])
    out.append("")
    out += tbl(d["weakest_purchases"], [lambda n: n["bloodline"], lambda n: n["name"], lambda n: n["category"], lambda n: n["row_weighted_total"], lambda n: n["raw_flat_total"]],
               ["Bloodline", "Weakest purchases (any tier)", "Tier", "Row-weighted", "Raw"])
    out.append("\n## 3. Tag ceilings against engine caps\n")
    out.append("Per tag: the highest single-row final and the summed finals at the best legal build. Engine caps (SOURCE_MECHANICS): percentage rows cap at 100; Afterburn damage per hit caps at 60% of that hit; Reflect returns at most 60% of a hit; Lifesteal plus vamp share one 60%-of-hit budget; static Heal is ×10 HP per tick.\n")
    for tag in ("afterburn", "lifesteal", "reflect", "heal", "increaseheal", "damage"):
        lst = d["tag_ceilings"].get(tag) or []
        if not lst:
            continue
        out.append(f"**{L.TAG_LABELS[tag]}** — top {min(6, len(lst))} of {len(lst)} trees\n")
        out += tbl(lst[:6], [lambda x: x["bloodline"], lambda x: x["rows"], lambda x: x["addition"], lambda x: x["max_single"], lambda x: x["max_sum"], lambda x: ", ".join(x["recipients"])],
                   ["Bloodline", "Rows", "Max addition", "Max single-row final", "Summed finals", "Recipient"])
        out.append("")
    out.append("## 4. Stacking (same-tag rows on one recipient all apply — process.ts 1109–1117)\n")
    out.append("Jutsu-sourced percentage increases compound and reductions apply sequentially (`computeDamagePacket`, process.ts 1692–1825; SOURCE_MECHANICS §3b), so the table gives the combined damage multiplier: ×Π(1 + p) for Increase Damage Given/Taken and ×Π(1 − p) for Decrease Damage Taken/Given, before the 90% reduction floor.\n")
    for key, title in (("stacked_enemy_exposure", "Enemy Increase Damage Taken"), ("stacked_self_idg", "Self Increase Damage Given"),
                       ("stacked_self_ddt", "Self Decrease Damage Taken"), ("stacked_enemy_ddg", "Enemy Decrease Damage Given")):
        lst = d[key]
        out.append(f"**{title}** — kits with two or more rows on that recipient ({len(lst)})\n")
        if lst:
            out += tbl(lst[:10], [lambda x: x["bloodline"], lambda x: x["rows"], lambda x: f"×{x['base_multiplier']}", lambda x: f"+{x['addition']}%", lambda x: f"×{x['max_multiplier']}", lambda x: ", ".join(x["jutsu"])],
                       ["Bloodline", "Rows", "Base combined multiplier", "Tree max addition per row", "Combined multiplier at max", "Jutsu"])
        out.append("\nStack figures assume every row is active together; cooldowns, AP and the cast-round rule (no buff or debuff acts in its own cast round) usually prevent that.\n")
    out.append(f"Percentage rows pushed past the 100 cap by any legal build: {len(d['percentage_rows_over_100'])}.\n")
    out.append("## 3b. Ceilings and route bands (RUL-2026-10-03-005)\n")
    out.append("Maximum per tag over every legal prerequisite-closed allocation. Hard ceilings: Damage +5, Lifesteal +5%, Afterburn +15%; every other tag +10% unless a director-review exception is recorded. Routes are scored by each Advanced Art's first modifier tag summed along its path; preferred totals are +5/+10/+15.\n")
    out += tbl(d["ceilings"], [lambda x: x["bloodline"] + (" (reference)" if x["reference"] else ""),
                               lambda x: ", ".join(L.mod_text(k, v, abbr=True) for k, v in x["maximum"].items()),
                               lambda x: ", ".join(x["over_ceiling"]) or "—",
                               lambda x: "; ".join(f"{r['name']} {L.mod_text(r['primary_tag'], r['total'], abbr=True)}" + ("" if r["on_band"] else " (off band)") for r in x["routes"]),
                               lambda x: ", ".join(f"{L.TAG_ABBR.get(z.get('tag'), z.get('tag'))} ≤ +{z.get('max')}%" for z in x["director_exceptions"]) or "—"],
               ["Bloodline", "Maximum over legal allocations", "Over ceiling", "Routes", "Director-review exceptions"])
    out.append("")
    out.append("## 5. Delivery, scope and classification\n")
    out += tbl(d["delivery_and_scope"], [lambda x: x["bloodline"], lambda x: x["rank"], lambda x: f"{x['label']} ({L.short_kind(x['label_kind'])})",
                                         lambda x: x["shared_element_bloodlines"], lambda x: ", ".join(x["authored_classification_jutsu"]) or "—",
                                         lambda x: f"{x['rows_matching_label_directly']}/{x['supported_rows']} ({x['rows_none_fallback']} None)",
                                         lambda x: ", ".join(x["tags_only_on_gated_rows"]) or "—", lambda x: ", ".join(x["mode_restricted"]) or "—",
                                         lambda x: "; ".join(x["injected_children"]) or "—", lambda x: ", ".join(x["universal_nodes"]) or "—",
                                         lambda x: len(x["ally_hazard_rows"]), lambda x: len(x["enemy_hazard_rows"]), lambda x: ", ".join(x["adverse_rows"]) or "—",
                                         lambda x: ", ".join(x["repeated_rows_on_one_jutsu"]) or "—"],
               ["Bloodline", "Rank", "Classification", "Bloodlines sharing the element", "Kit jutsu needing authored classification", "Kit rows matching the element now", "Tags only on gated rows", "Mode-restricted", "Injected children", "Universal node", "Ally-hazard rows", "Enemy-hazard rows", "Adverse rows", "Repeated rows"])
    out.append("\nPotency is element-wide (RUL-2026-10-03-005): every jutsu of the qualifying element qualifies, so sharing an element with other bloodlines is expected, not a collision. `Kit rows matching the element now` shows how much of each kit the current row-element resolver would reach; the rest needs the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1–G2), and kit jutsu whose own rows carry no qualifying element additionally need an authored jutsu classification. Off-kit coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element) is unverified. Item gates decide castability only.\n")
    out.append("## 6. Inherited strength versus Bloodright additions\n")
    out.append("Inherited strength is the kit as captured (rank, rows, baseline values at jutsu level 25). The added column is the strongest legal build's row-weighted addition; the share compares it with the kit's summed baselines. Ranks and native kits were not equal beforehand; Bloodright equalises marginal opportunity, not final strength.\n")
    out += tbl(d["inherited_vs_added"], [lambda x: x["bloodline"], lambda x: x["rank"], lambda x: x["jutsu"], lambda x: x["supported_rows"], lambda x: f"{x['damage_rows']} / {x['damage_base_sum']}",
                                         lambda x: f"{x['percentage_rows']} / {x['percentage_base_sum']}", lambda x: x["added_max_row_weighted"], lambda x: f"{x['added_share_of_inherited_pct']}%"],
               ["Bloodline", "Rank", "Jutsu", "Supported rows", "Damage rows / base sum", "% rows / base sum", "Added (max row-weighted)", "Added share"])
    out.append("\n## 7. Interactions outside the tree\n")
    out.append("- **Main tree:** skill-tree potency effects stack with Bloodright under `BATTLE_TAG_STACKING`; broad normal-tree potency is not approved (OPEN_DECISIONS D7). Main-tree IDG/IDT/DDT effects are stage-1 multipliers in the same pipeline as the kit's rows (SOURCE_MECHANICS §3b); their combined budget is unaudited.")
    out.append("- **Bloodline passives:** the passive IDG (fromType bloodline) multiplies the running damage last, after the jutsu-sourced multipliers, so a flat Damage addition is worth more on kits whose passive covers that element. Passives are not potency targets.")
    out.append("- **Cast-round rule:** no buff or debuff acts in its own cast round (tags.ts handler gates; process.ts 1520–1523 for the damage-modifier pipeline), so a jutsu's own IDG/IDT/Afterburn row never boosts its own hit; realized value depends on sequencing across rounds.")
    out.append("- **Ranked modes:** skill-tree and bloodline effects are skipped in RANKED_PVP and RANKED_SPARRING, so Bloodright is inert there (OPEN_DECISIONS D6).")
    out.append("- **Equipment:** item-gated jutsu need their item to be cast; the item is never a potency selector. Keystones are exclusive per battle, weapons may not be (ENGINE_GAP_REGISTER G7).")
    rl = d.get("review_log") or {}
    if rl:
        out.append("\n## 8. Review state\n")
        out.append("| Bloodline | Revision | Final review | Open blocker/major findings |\n|---|---|---|---|")
        for slug, v in sorted(rl.items()):
            out.append(f"| {v.get('name', slug)} | {v.get('revision', '')} | {v.get('final_review', '')} | {'; '.join(v.get('open_major', [])) or '—'} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    d = build()
    jt = json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    mt = md(d)
    if a.check:
        stale = [p for p, t in ((OUT_JSON, jt), (OUT_MD, mt)) if not os.path.exists(p) or open(p, encoding="utf-8").read() != t]
        if stale:
            print("STALE " + ", ".join(stale))
            return 2
        print("cross-roster review current")
        return 0
    L.write_text(OUT_JSON, jt)
    L.write_text(OUT_MD, mt)
    print(f"wrote {OUT_MD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
