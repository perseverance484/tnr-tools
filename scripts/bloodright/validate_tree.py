#!/usr/bin/env python3
"""Validate and normalize a Bloodright tree JSON against its bloodline kit.

Usage:
  python3 scripts/bloodright/validate_tree.py docs/design/bloodright/trees/<slug>.json [--write] [--check]

Without --write it only reports. With --write it fills the computed fields
(coverage, display roles, minimum path cost, example bonuses/finals, audit,
legal full-budget builds) in place and writes <slug>.validation.json. With
--check it fails if a rewrite would change the committed files.

Exit codes: 0 valid, 1 structural/semantic errors, 2 stale (--check).
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloodright_lib as L  # noqa: E402

TREES_DIR = os.path.join(L.DESIGN_DIR, "trees")

PROGRESSION = {
    "currency": "Bloodright Point",
    "abbreviation": "BP",
    "acquired_with": "silver",
    "acquisition_cap": L.BP_CAP,
    "node_cost": L.NODE_COST,
    "silver_price": None,
    "ownership_gate": "current bloodline",
    "separate_from_normal_skill_points": True,
}


def find_kit(tree: dict, snapshot: dict, roster: dict) -> tuple[dict, dict]:
    idx = L.census_index(snapshot, roster)
    bl = tree.get("bloodline") or {}
    bid = bl.get("id")
    if bid and bid in idx:
        return idx[bid]["kit"], idx[bid]["record"]
    name = (bl.get("name") or tree.get("classification", {}).get("bloodline") or "").strip().lower()
    for bid2, ent in idx.items():
        if ent["kit"]["bloodline"]["name"].strip().lower() == name:
            return ent["kit"], ent["record"]
    raise SystemExit(f"bloodline not found in snapshot: {bl}")


def other_tree_names(exclude_path: str, bloodline_id: str | None = None, bloodline_name: str | None = None) -> dict[str, str]:
    """Node names used by every other tree (another file for a different bloodline)."""
    names: dict[str, str] = {}
    paths = sorted(glob.glob(os.path.join(TREES_DIR, "*.json")))
    for p in paths:
        if os.path.abspath(p) == os.path.abspath(exclude_path) or p.endswith(".validation.json"):
            continue
        try:
            t = L.load_json(p)
        except Exception:
            continue
        tid = (t.get("bloodline") or {}).get("id")
        tname = ((t.get("bloodline") or {}).get("name") or (t.get("classification") or {}).get("bloodline") or "").strip().lower()
        if bloodline_id and tid == bloodline_id:
            continue
        if bloodline_name and tname == bloodline_name.strip().lower():
            continue
        for n in t.get("nodes", []):
            names[str(n.get("name", "")).strip().lower()] = os.path.basename(p)
    return names


def role_for_modifier(tag: str, rows: list[L.Row]) -> tuple[str, list[str]]:
    roles = sorted({r.role for r in rows if r.supported and r.tag == tag})
    if not roles:
        return "UNCOVERED", roles
    if roles == ["DAMAGE"]:
        return "DAMAGE", roles
    non_adverse = [x for x in roles if x in ("SELF BUFF", "ALLY BUFF", "ENEMY DEBUFF", "DAMAGE")]
    if set(non_adverse) <= {"SELF BUFF", "ALLY BUFF"} and non_adverse:
        return "SELF BUFF", roles
    if non_adverse == ["ENEMY DEBUFF"]:
        return "ENEMY DEBUFF", roles
    if non_adverse:
        return non_adverse[0], roles
    return roles[0], roles


def normalize(tree: dict, kit: dict, record: dict, rows: list[L.Row], level: int) -> tuple[dict, dict, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    b = kit["bloodline"]
    bname = b["name"].strip()
    sup_rows = [r for r in rows if r.supported]
    rows_by_tag: dict[str, list[L.Row]] = {}
    for r in sup_rows:
        rows_by_tag.setdefault(r.tag, []).append(r)

    errors.extend(L.validate_structure(tree))
    errors.extend(f"stale pre-RUL-2026-10-03-005 wording in {h}" for h in L.stale_language(tree))
    nodes = L.parse_nodes(tree)
    by_id = {n.id: n for n in nodes}

    # semantic checks on modifiers
    for n in nodes:
        for m in n.modifiers:
            tag = m.get("tag")
            if tag in L.SUPPORTED_TAGS and not rows_by_tag.get(tag):
                errors.append(f"node {n.id} ({n.name}) targets {tag} but the kit has no supported {tag} row")
    audit_cls = L.classification_audit(kit, rows, L.load_snapshot(), L.load_roster())
    prior = tree.get("classification") or {}
    cls = {
        "potency_classification": audit_cls["proposed_label"],
        "label_kind": audit_cls["label_kind"],
        "classification_status": audit_cls["classification_status"],
        "qualifying_elements": audit_cls["qualifying_elements"],
        "display_element": audit_cls.get("display_element"),
        "selector": "jutsu classification: the qualifying element(s), whatever the jutsu's source",
        "applies_to": "",
        "not_selectors": audit_cls["not_selectors"],
        "kit_jutsu_by_authored_classification": audit_cls["kit_jutsu_by_authored_classification"],
        "shared_element_bloodlines": sorted({c["name"].strip() for c in audit_cls["shared_element_bloodlines"]}),
        "off_kit_coverage": "unverified (no non-bloodline jutsu catalog with effect rows in the repository)",
        "changes_combat_elements": False,
        "preserves_row_filters": True,
        "engine_status": audit_cls["engine_status"],
    }
    cls["applies_to"] = f"matching supported tags on all {L.scope_label(cls)} jutsu"
    if prior.get("director_note"):
        cls["director_note"] = prior["director_note"]
    tree["classification"] = cls
    membership = {m["jutsu"]: m["membership"] for m in audit_cls["kit_membership"]}

    tree["bloodline"] = {
        "id": b["id"], "review_id": (record or {}).get("review_id"), "name": bname, "rank": b.get("rank"),
        "statClassification": b.get("statClassification"), "traits": b.get("traits"),
    }
    tree["progression"] = PROGRESSION
    tree.setdefault("title", f"{bname} — Bloodright")
    tree.setdefault("revision", "draft proposal")
    tree["evaluation_level"] = level
    tree["game_source_pin"] = L.GAME_SOURCE_PIN
    tree["snapshot"] = {"public_kit_snapshot": (record or {}).get("public_kit_snapshot"),
                        "hidden_kit_snapshot": (record or {}).get("hidden_kit_snapshot")}

    label = cls["potency_classification"]
    for n in tree.get("nodes", []):
        nid = str(n["id"])
        n["id"] = nid
        n["parents"] = [str(p) for p in (n.get("parents") or [])]
        n["parent_rule"] = "ALL"
        n["cost"] = L.NODE_COST
        n["potency_classification"] = label
        n["scope"] = f"all {L.scope_label(cls)} jutsu"
        if not errors:
            n["minimum_path_bp"] = L.depth(nid, by_id)
        cov_jutsu: set[str] = set()
        cov_rows = 0
        adverse_rows = []
        hidden_rows = 0
        gated_rows = 0
        hazard_rows = []
        enemy_rows = []
        authored_rows = 0
        for m in n.get("modifiers", []):
            m["flat"] = int(m["flat"])
            role, roles = role_for_modifier(m["tag"], rows)
            m["display_role"] = role
            if len(roles) > 1:
                m["row_roles"] = roles
            for r in rows_by_tag.get(m["tag"], []):
                cov_jutsu.add(r.jutsu_name)
                cov_rows += 1
                if r.adverse:
                    adverse_rows.append(f"{r.jutsu_name}#{r.row}")
                if r.visibility == "hidden":
                    hidden_rows += 1
                if r.item_gate:
                    gated_rows += 1
                if r.ally_hazard:
                    hazard_rows.append(f"{r.jutsu_name}#{r.row}")
                if r.enemy_hazard:
                    enemy_rows.append(f"{r.jutsu_name}#{r.row}")
                if membership.get(r.jutsu_name) == "authored":
                    authored_rows += 1
        n["coverage"] = {"jutsu": sorted(cov_jutsu), "effect_rows": cov_rows}
        if hazard_rows:
            n["coverage"]["ally_hazard_rows"] = sorted(set(hazard_rows))
        if enemy_rows:
            n["coverage"]["enemy_hazard_rows"] = sorted(set(enemy_rows))
        if adverse_rows:
            n["coverage"]["adverse_rows"] = sorted(set(adverse_rows))
            warnings.append(f"node {nid} ({n['name']}) also amplifies adverse rows: {', '.join(sorted(set(adverse_rows)))}")
        if hidden_rows:
            n["coverage"]["hidden_rows"] = hidden_rows
        if gated_rows:
            n["coverage"]["item_gated_rows"] = gated_rows
        if authored_rows:
            n["coverage"]["rows_via_authored_classification"] = authored_rows

    # examples
    examples = tree.get("examples") or []
    if len(examples) < 2 and not tree.get("narrow_kit_exception"):
        errors.append("fewer than 2 complete build examples and no narrow_kit_exception recorded")
    if len(examples) > 4:
        warnings.append("more than 4 example builds; keep 2-3 representative builds")
    seen_sets = []
    adv_used = []
    if not errors:
        for ex in examples:
            ids = [str(i) for i in ex.get("ids", [])]
            ex["ids"] = ids
            s = set(ids)
            if len(s) != len(ids):
                errors.append(f"example {ex.get('name')} repeats a node")
            if any(i not in by_id for i in ids):
                errors.append(f"example {ex.get('name')} references unknown node ids {ids}")
                continue
            cost = sum(by_id[i].cost for i in ids)
            ex["cost"] = cost
            if cost != L.BP_CAP:
                errors.append(f"example {ex.get('name')} spends {cost} BP; complete examples spend exactly {L.BP_CAP}")
            if not L.is_closed(s, by_id):
                errors.append(f"example {ex.get('name')} is not prerequisite-closed: {ids}")
            if s in seen_sets:
                errors.append(f"example {ex.get('name')} duplicates another example's allocation")
            seen_sets.append(s)
            advs = [i for i in ids if by_id[i].category == "Advanced Art"]
            if advs and advs in adv_used:
                warnings.append(f"example {ex.get('name')} shares its Advanced Art {advs} with another example; builds should be distinct")
            adv_used.append(advs)
            bon = L.bonuses_for(s, by_id)
            ex["bonuses"] = {t: bon[t] for t in L.SUPPORTED_TAGS if bon[t]}
            ex["finals"] = L.finals_for(ids, tree, rows)
            ex["advanced_arts"] = [by_id[i].name for i in advs]
    if errors:
        return tree, {}, errors, warnings

    audit = L.audit_tree(tree, rows)
    tree["audit"] = {k: v for k, v in audit.items() if k not in ("full_builds", "legal_allocations", "node_values",
                                                                    "strongest_full_build_by_row_weight",
                                                                    "lowest_value_node_by_row_weight")}
    tree["audit"]["revision"] = tree.get("revision")
    tree["audit"]["source_snapshot"] = tree["snapshot"]["public_kit_snapshot"]
    tree["audit"]["limits"] = [
        "Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).",
        f"{L.scope_sentence(cls)} Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.",
        "Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.",
        "Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.",
        "Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.",
        "Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.",
        "Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.",
        "No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.",
        "Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.",
    ]
    tree["legal_full_budget_builds"] = [{"ids": bld["ids"], "bonuses": bld["bonuses"]} for bld in audit["full_builds"]]

    # warnings on design quality
    if audit["available_skills"] < 6 and not tree.get("narrow_kit_exception"):
        warnings.append(f"only {audit['available_skills']} nodes without a narrow_kit_exception")
    if audit["advanced_art_count"] < 2 and not tree.get("narrow_kit_exception"):
        warnings.append("fewer than 2 Advanced Arts without a narrow_kit_exception")
    if audit["nodes_absent_from_non_dominated_builds"]:
        warnings.append("nodes absent from every non-dominated full build: " + ", ".join(audit["nodes_absent_from_non_dominated_builds"]))
    c_err, c_warn, c_report = L.ceiling_findings(tree)
    errors.extend(c_err)
    warnings.extend(c_warn)
    tree["audit"]["ceilings"] = c_report
    # Review audits (BALANCE_REVIEW_METHOD.md): damage tiers, fourth purchases, route overlap.
    dta = L.damage_threshold_audit(tree, rows)
    if dta["above_nuke"]:
        worst = max(dta["above_nuke"], key=lambda x: (x["final"], x["jutsu"]))
        lst = ", ".join(sorted({f"{x['jutsu']} {x['base']:g} -> {x['final']:g}" for x in dta["above_nuke"]}))
        why = str(tree.get("above_nuke_rationale") or "").strip()
        if why:
            warnings.append(f"Damage above the 50 Nuke tier in a legal allocation (director review): {lst}")
        else:
            errors.append(f"Damage above the 50 Nuke tier in a legal allocation without an above_nuke_rationale: {lst} (worst {worst['final']:g})")
    for ov in L.route_overlap(tree):
        if ov["same_primary_tag"]:
            warnings.append(f"route overlap (diagnostic): {ov['a_name']} and {ov['b_name']} share their primary tag"
                            f"{' as siblings' if ov['siblings'] else ''} (path cosine {ov['path_cosine']})")
    if cls["label_kind"] != "element":
        warnings.append(f"classification status: {cls['classification_status']} (director decision)")
    universal = [nid for nid in by_id if audit["full_builds"] and all(nid in b["ids"] for b in audit["full_builds"])]
    if universal:
        names = ", ".join(f"{nid} ({by_id[nid].name})" for nid in sorted(universal))
        msg = f"universal node: {names} appears in every legal full-budget allocation"
        if tree.get("narrow_kit_exception") and "universal" in str(tree.get("narrow_kit_exception")).lower():
            msg += " (acknowledged in narrow_kit_exception)"
        warnings.append(msg)
    for nv in audit["node_values"]:
        if nv["tags_without_rows"]:
            errors.append(f"node {nv['id']} targets tags with no rows: {nv['tags_without_rows']}")
    hazard_all = sorted({h for n in tree.get("nodes", []) for h in n.get("coverage", {}).get("ally_hazard_rows", [])})
    if hazard_all:
        warnings.append("ally-hazard area rows amplified (friendly fire none/ALL): " + ", ".join(hazard_all))
    enemy_all = sorted({h for n in tree.get("nodes", []) for h in n.get("coverage", {}).get("enemy_hazard_rows", [])})
    if enemy_all:
        warnings.append("enemy-hazard ground rows amplified (positive row, friendly fire none/ALL): " + ", ".join(enemy_all))
    untargeted = audit["supported_tags_in_kit_not_targeted"]
    if untargeted:
        warnings.append("supported tags present in kit but not targeted by any node: " + ", ".join(untargeted))

    validation = {
        "kind": "bloodright_tree_validation",
        "slug": L.slugify(bname),
        "bloodline": tree["bloodline"],
        "revision": tree.get("revision"),
        "structure_errors": errors,
        "warnings": warnings,
        "classification": cls,
        "examples": [{"name": e.get("name"), "archetype": e.get("archetype"), "ids": e["ids"], "cost": e["cost"],
                      "bonuses": e["bonuses"], "advanced_arts": e["advanced_arts"]} for e in examples],
        "audit": audit,
        "damage_thresholds": L.damage_threshold_audit(tree, rows),
        "fourth_bp": L.fourth_bp_audit(tree, rows),
        "route_overlap": L.route_overlap(tree),
        "evaluation_level": level,
        "game_source_pin": L.GAME_SOURCE_PIN,
        "combat_simulation_performed": False,
        "live_mutations": 0,
    }
    return tree, validation, errors, warnings


def process(path: str, write: bool, check: bool, level: int) -> int:
    tree = L.load_json(path)
    snapshot = L.load_snapshot()
    roster = L.load_roster()
    kit, record = find_kit(tree, snapshot, roster)
    rows = L.kit_rows(kit, level)
    tree, validation, errors, warnings = normalize(tree, kit, record, rows, level)
    # cross-tree name uniqueness (SkillTree.name is a unique index in the game schema)
    others = other_tree_names(path, kit["bloodline"]["id"], kit["bloodline"]["name"])
    for n in tree.get("nodes", []):
        key = str(n.get("name", "")).strip().lower()
        if key in others:
            errors.append(f"node name {n.get('name')!r} already used in {others[key]} (SkillTree.name is unique)")
    if validation:
        validation["structure_errors"] = errors
    slug = L.slugify(kit["bloodline"]["name"])
    vpath = os.path.join(os.path.dirname(path), slug + ".validation.json")
    tag = f"[{slug}]"
    for w in warnings:
        print(f"{tag} WARN {w}")
    if errors:
        for e in errors:
            print(f"{tag} ERROR {e}")
        print(f"{tag} INVALID ({len(errors)} errors)")
        return 1
    ttxt = json.dumps(tree, indent=2, ensure_ascii=False) + "\n"
    vtxt = json.dumps(validation, indent=2, ensure_ascii=False) + "\n"
    if check:
        stale = []
        if open(path, encoding="utf-8").read() != ttxt:
            stale.append(path)
        if not os.path.exists(vpath) or open(vpath, encoding="utf-8").read() != vtxt:
            stale.append(vpath)
        if stale:
            print(f"{tag} STALE: " + ", ".join(stale))
            return 2
        print(f"{tag} current")
        return 0
    if write:
        L.write_text(path, ttxt)
        L.write_text(vpath, vtxt)
    a = validation["audit"]
    print(f"{tag} VALID nodes={a['available_skills']} F/H/A={a['foundation_count']}/{a['hidden_art_count']}/{a['advanced_art_count']} "
          f"full_allocs={a['full_budget_allocations']} non_dom={a['non_dominated_full_allocations']} "
          f"min_two_adv={a['minimum_two_advanced_cost']} max_adv={a['maximum_advanced_arts']} "
          f"max={a['maximum_tag_bonuses']}{' (written)' if write else ''}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--level", type=int, default=L.DEFAULT_JUTSU_LEVEL)
    args = ap.parse_args()
    rc = 0
    for p in args.paths:
        if p.endswith(".validation.json"):
            continue
        rc = max(rc, process(p, args.write, args.check, args.level))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
