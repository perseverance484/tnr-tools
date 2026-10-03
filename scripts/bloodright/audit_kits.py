#!/usr/bin/env python3
"""Produce per-bloodline kit dossiers (JSON + Markdown) for Bloodright planning.

Usage:
  python3 scripts/bloodright/audit_kits.py            # approved + reference
  python3 scripts/bloodright/audit_kits.py --all      # every census record
  python3 scripts/bloodright/audit_kits.py --check    # verify committed dossiers are current

Inputs are the committed snapshot/roster only. No live requests.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloodright_lib as L  # noqa: E402

KITS_DIR = os.path.join(L.DESIGN_DIR, "kits")


def fmt_num(x, calc=None):
    if x is None:
        return "-"
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    s = f"{x:g}" if isinstance(x, float) else str(x)
    return s + ("%" if calc == "percentage" else "")


def dossier_for(bid: str, snapshot: dict, roster: dict, level: int) -> dict:
    idx = L.census_index(snapshot, roster)
    kit = idx[bid]["kit"]
    rec = idx[bid]["record"] or {}
    b = kit["bloodline"]
    rows = L.kit_rows(kit, level)
    sup = [r for r in rows if r.supported]
    by_tag: dict[str, list[L.Row]] = {}
    for r in sup:
        by_tag.setdefault(r.tag, []).append(r)
    summary = []
    for tag in L.SUPPORTED_TAGS:
        rs = by_tag.get(tag, [])
        if not rs:
            continue
        summary.append({
            "tag": tag, "label": L.TAG_LABELS[tag], "rows": len(rs),
            "jutsu": sorted({r.jutsu_name for r in rs}),
            "roles": sorted({r.role for r in rs}),
            "recipients": sorted({r.recipient for r in rs}),
            "bases_at_level": sorted({r.base for r in rs}),
            "adverse_rows": [{"jutsu": r.jutsu_name, "row": r.row, "role": r.role} for r in rs if r.adverse],
            "hidden_rows": sum(1 for r in rs if r.visibility == "hidden"),
            "item_gated_rows": sum(1 for r in rs if r.item_gate),
            "mode_restricted_rows": sum(1 for r in rs if r.usage not in (None, "BOTH")),
            "repeated_on_same_jutsu": sorted({r.jutsu_name for r in rs if sum(1 for q in rs if q.jutsu_name == r.jutsu_name) > 1}),
        })
    jutsu_meta = []
    for vis, key in (("public", "public_jutsu"), ("hidden", "hidden_jutsu")):
        for j in kit.get(key, []):
            jutsu_meta.append({
                "id": j["id"], "name": j["name"], "visibility": vis, "jutsuType": j.get("jutsuType"),
                "jutsuRank": j.get("jutsuRank"), "statClassification": j.get("statClassification"),
                "target": j.get("target"), "range": j.get("range"), "cooldown": j.get("cooldown"),
                "actionCostPerc": j.get("actionCostPerc"), "chakraCost": j.get("chakraCost"),
                "staminaCost": j.get("staminaCost"), "method": j.get("method"),
                "requiredLevel": j.get("requiredLevel"), "jutsuWeapon": j.get("jutsuWeapon"),
                "requiredBloodlineItemId": j.get("requiredBloodlineItemId"),
                "battleUsageType": j.get("battleUsageType"), "injectableInBattle": j.get("injectableInBattle"),
                "hidden": j.get("hidden"), "bloodlineId": j.get("bloodlineId"),
                "effect_count": len(j.get("effects", [])),
                "supported_effect_count": sum(1 for e in j.get("effects", []) if e.get("type") in L.SUPPORTED_TAGS),
            })
    passives = [{
        "type": e.get("type"), "power": e.get("power"), "powerPerLevel": e.get("powerPerLevel"),
        "target": e.get("target"), "elements": e.get("elements"), "statTypes": e.get("statTypes"),
        "generalTypes": e.get("generalTypes"), "calculation": e.get("calculation"),
        "direction": e.get("direction"),
    } for e in b.get("effects", [])]
    cls = L.classification_audit(kit, rows, snapshot, roster)
    ab_rows = [r for r in sup if r.tag == "afterburn"]
    damage_rows = [r for r in sup if r.tag == "damage"]
    return {
        "kind": "bloodright_kit_dossier",
        "review_id": rec.get("review_id"),
        "bloodline_id": bid,
        "name": b["name"],
        "slug": L.slugify(b["name"]),
        "rank": b.get("rank"),
        "hidden": b.get("hidden"),
        "statClassification": b.get("statClassification"),
        "traits": b.get("traits"),
        "regenIncrease": b.get("regenIncrease"),
        "disposition": rec.get("owner_decision"),
        "decision_basis": rec.get("decision_basis"),
        "snapshot": {
            "public_kit_snapshot": rec.get("public_kit_snapshot"),
            "hidden_kit_snapshot": rec.get("hidden_kit_snapshot"),
            "public_retrieved_at": snapshot.get("public_retrieved_at"),
            "hidden_inventory_retrieved_at": snapshot.get("hidden_inventory_retrieved_at"),
            "kind": snapshot.get("kind"),
        },
        "evaluation_level": level,
        "game_source_pin": L.GAME_SOURCE_PIN,
        "passives": passives,
        "jutsu": jutsu_meta,
        "rows": [r.as_dict() for r in rows],
        "supported_row_summary": summary,
        "supported_rows_total": len(sup),
        "unsupported_tags_present": sorted({r.tag for r in rows if not r.supported}),
        "adverse_supported_rows": [{"jutsu": r.jutsu_name, "row": r.row, "tag": r.tag, "role": r.role,
                                     "recipient": r.recipient, "base": r.base} for r in sup if r.adverse],
        "ally_hazard_supported_rows": [{"jutsu": r.jutsu_name, "row": r.row, "tag": r.tag, "method": r.method,
                                        "jutsu_target": r.jutsu_target, "friendly_fire": r.friendly_fire} for r in sup if r.ally_hazard],
        "enemy_hazard_supported_rows": [{"jutsu": r.jutsu_name, "row": r.row, "tag": r.tag, "method": r.method,
                                         "jutsu_target": r.jutsu_target, "friendly_fire": r.friendly_fire} for r in sup if r.enemy_hazard],
        "afterburn": {
            "application_rows": [{"jutsu": r.jutsu_name, "row": r.row, "base": r.base, "rounds": r.rounds} for r in ab_rows],
            "downstream_note": (
                "Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on "
                "following rounds, every instant damage consequence the debuffed target receives "
                "(any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the "
                "cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, "
                "not the duration. Downstream coverage is therefore every non-pierce hit landed on the "
                "target during the debuff, including normal jutsu, weapons and allies; it is not "
                "measured by the application-row count and was not simulated."),
            "kit_instant_damage_rows_that_can_be_enhanced": len(damage_rows),
        },
        "classification_audit": cls,
    }


def md_dossier(d: dict) -> str:
    out = []
    out.append(f"# {d['name']} — Bloodright kit dossier\n")
    out.append(f"**Review id:** {d['review_id']} · **Bloodline id:** `{d['bloodline_id']}` · **Rank:** {d['rank']} · "
               f"**Stat classification:** {d['statClassification']} · **Traits:** {d['traits'] or '—'} · "
               f"**Disposition:** {d['disposition']}\n")
    out.append(f"Evidence: public kit snapshot {d['snapshot']['public_kit_snapshot']}; hidden inventory {d['snapshot']['hidden_kit_snapshot']}. "
               f"Baselines evaluated at **jutsu level {d['evaluation_level']}** (power + powerPerLevel × level). "
               f"Mechanics read at `studie-tech/TheNinjaRPG@{d['game_source_pin']}`. This is a projection of captured records, not a live readback.\n")
    out.append("## Passive bloodline effects (context only; not potency targets)\n")
    out.append("| Type | Power | Per level | Target | Elements | Stat types | Calc |\n|---|---:|---:|---|---|---|---|")
    for p in d["passives"]:
        out.append(f"| {p['type']} | {fmt_num(p['power'])} | {fmt_num(p['powerPerLevel'])} | {p['target']} | {', '.join(p['elements'] or []) or '—'} | {', '.join(p['statTypes'] or []) or '—'} | {p['calculation']} |")
    out.append("\n## Jutsu in kit\n")
    out.append("| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |\n|---|---|---|---|---|---:|---:|---:|---|---|---|---|")
    for j in d["jutsu"]:
        out.append(f"| {j['name']} | {j['visibility']} | {j['jutsuType']} | {j['jutsuRank']} | {j['target']} | {j['range']} | {j['actionCostPerc']} | {j['cooldown']} | {j['method']} | {j['requiredBloodlineItemId'] or '—'} | {j['battleUsageType']} | {j['supported_effect_count']} / {j['effect_count']} |")
    out.append("\n## Effect rows\n")
    out.append("Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.\n")
    out.append("| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |\n|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|")
    for r in d["rows"]:
        filt = ", ".join(r["stat_types"] or []) + (" / " + ", ".join(r["general_types"]) if r["general_types"] else "")
        out.append(f"| {r['jutsu_name']} | {r['row']} | {r['tag']} | {r['calculation']} | {fmt_num(r['base'], r['calculation'])} | {fmt_num(r['power'])} + {fmt_num(r['power_per_level'])}/lvl | {r['rounds'] if r['rounds'] is not None else '—'} | {', '.join(r['elements_effective'])} | {filt or '—'} | {r['friendly_fire'] or 'none (=ALL)'} | {r['recipient']} | {r['role']} | {'✓' if r['supported'] else ''} | {'**yes**' if r['adverse'] else ''} | {'**yes**' if r.get('ally_hazard') else ''} | {'**yes**' if r.get('enemy_hazard') else ''} |")
    out.append("\nStat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.")
    out.append("\n## Supported-row summary by tag\n")
    out.append("| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |\n|---|---:|---|---|---|---|---:|---:|---:|---|")
    for s in d["supported_row_summary"]:
        out.append(f"| {s['label']} | {s['rows']} | {', '.join(s['jutsu'])} | {', '.join(s['roles'])} | {', '.join(fmt_num(b) for b in s['bases_at_level'])} | {', '.join(s['repeated_on_same_jutsu']) or '—'} | {s['hidden_rows']} | {s['item_gated_rows']} | {s['mode_restricted_rows']} | {', '.join(a['jutsu']+'#'+str(a['row']) for a in s['adverse_rows']) or '—'} |")
    out.append(f"\nSupported rows total: **{d['supported_rows_total']}**. Unsupported tags present (no potency): {', '.join(d['unsupported_tags_present']) or 'none'}.\n")
    if d["ally_hazard_supported_rows"]:
        out.append("> **Ally-hazard rows (area delivery, friendly fire none/ALL):** " + "; ".join(f"{a['jutsu']} row {a['row']} ({a['tag']}, {a['method']}, target {a['jutsu_target']})" for a in d["ally_hazard_supported_rows"]) +
                   ". Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.\n")
    if d["enemy_hazard_supported_rows"]:
        out.append("> **Enemy-hazard rows (ground spawn, positive INHERIT row, friendly fire none/ALL):** " + "; ".join(f"{a['jutsu']} row {a['row']} ({a['tag']}, {a['method']}, target {a['jutsu_target']})" for a in d["enemy_hazard_supported_rows"]) +
                   ". The ground effect is re-applied each round to whoever stands on the tiles, enemies included.\n")
    if d["adverse_supported_rows"]:
        out.append("> **Adverse rows:** " + "; ".join(f"{a['jutsu']} row {a['row']} ({a['tag']} on {a['recipient']}, {a['role']})" for a in d["adverse_supported_rows"]) +
                   ". A potency node on that tag also raises these rows; the resolver cannot exclude a row by jutsu.\n")
    c = d["classification_audit"]
    out.append("## Selector / classification audit\n")
    out.append(f"- Signature elements on damage/pierce rows: {', '.join(c['signature_elements']) or 'none'}")
    out.append(f"- Proposed potency classification label: **{c['proposed_label']}** ({c['label_kind']})")
    out.append(f"- {c['note']}")
    for rch in c["current_resolver_reach"]:
        out.append(f"- Current resolver with `affectedElements=['{rch['label']}']`: {rch['rows_matching_label_directly']} of {rch['supported_rows_total']} supported rows match directly; {rch['rows_falling_back_to_None']} fall back to None; {rch['rows_with_other_elements_only']} carry other elements only. Exclusive under current resolver: no.")
    if c["census_collisions_on_signature_elements"]:
        out.append("- Census collisions on signature elements (other bloodlines carrying the element on any row): " +
                   "; ".join(f"{x['name']} [{x['disposition']}] ({x['element']}: {x['rows']} rows, {x['damage_rows']} damage)" for x in c["census_collisions_on_signature_elements"]))
    else:
        out.append("- Census collisions on signature elements: none among the 95 captured bloodline kits.")
    out.append(f"- Normal-jutsu collision: {c['normal_jutsu_collision']}")
    out.append(f"- Item-gated jutsu: {', '.join(c['item_gated_jutsu']) or 'none'}")
    out.append(f"- Mode-restricted jutsu: {', '.join(c['mode_restricted_jutsu']) or 'none'}")
    out.append(f"- Hidden jutsu in kit: {', '.join(c['hidden_jutsu']) or 'none'}")
    out.append(f"- Non-BLOODLINE jutsu types in kit: {', '.join(c['non_bloodline_type_jutsu_in_kit']) or 'none'}")
    if c["injected_children"]:
        out.append("\n### Injected children\n")
        out.append("| Parent | Child | Child id | Child bloodlineId | Child type | Resolved | Child supported rows |\n|---|---|---|---|---|---|---|")
        for ic in c["injected_children"]:
            sup = ", ".join(f"{e['type']}{'('+','.join(e['elements'])+')' if e.get('elements') else ''}" for e in ic["child_effects"] if e["supported"])
            out.append(f"| {ic['parent_jutsu']} | {ic['child_name'] or '?'} | `{ic['child_id']}` | `{ic['child_bloodline_id'] if ic['child_bloodline_id'] is not None else '?'}` | {ic['child_type'] or '?'} | {'yes' if ic['child_resolved'] else 'no'} | {sup or '—'} |")
        out.append("\nInjected children are cast as `jutsu` actions at the inject power as level (actions.ts handleInjectedJutsus), so the resolver would process them; whether they inherit the bloodline classification is an engine decision recorded in the gap register. Children with an empty `bloodlineId` are not bloodline jutsu.\n")
    out.append("\n## Afterburn and downstream notes\n")
    ab = d["afterburn"]
    if ab["application_rows"]:
        out.append("Application rows: " + "; ".join(f"{a['jutsu']} row {a['row']} ({fmt_num(a['base'],'percentage')}, {a['rounds']} rounds)" for a in ab["application_rows"]) + ".")
    else:
        out.append("No Afterburn application rows in this kit.")
    out.append(ab["downstream_note"])
    out.append("\nLifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.\n")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="every census record, not only approved + reference")
    ap.add_argument("--check", action="store_true", help="verify committed dossiers match regenerated output")
    ap.add_argument("--level", type=int, default=L.DEFAULT_JUTSU_LEVEL)
    args = ap.parse_args()
    snapshot = L.load_snapshot()
    roster = L.load_roster()
    ids = list(roster["reference_ids"]) + list(roster["approved_remaining_ids"])
    if args.all:
        ids = [r["bloodline_id"] for r in roster["records"]]
    index_rows = []
    mismatches = []
    for bid in ids:
        d = dossier_for(bid, snapshot, roster, args.level)
        jpath = os.path.join(KITS_DIR, d["slug"] + ".json")
        mpath = os.path.join(KITS_DIR, d["slug"] + ".md")
        md = md_dossier(d)
        import json as _json
        jtxt = _json.dumps(d, indent=2, ensure_ascii=False) + "\n"
        if args.check:
            for p, txt in ((jpath, jtxt), (mpath, md)):
                cur = open(p, encoding="utf-8").read() if os.path.exists(p) else None
                if cur != txt:
                    mismatches.append(p)
        else:
            L.write_text(jpath, jtxt)
            L.write_text(mpath, md)
        c = d["classification_audit"]
        index_rows.append((d["review_id"], d["name"], d["rank"], d["disposition"], d["slug"], d["supported_rows_total"],
                           c["proposed_label"], c["label_kind"], len(c["census_collisions_on_signature_elements"]),
                           len(d["adverse_supported_rows"]), len(c["injected_children"]), len(c["item_gated_jutsu"])))
    idx_md = ["# Bloodright kit dossiers\n",
              f"Generated by `scripts/bloodright/audit_kits.py` from the committed snapshot (public {snapshot.get('public_retrieved_at')}, hidden inventory {snapshot.get('hidden_inventory_retrieved_at')}). Baselines at jutsu level {args.level}. Mechanics pin `{L.GAME_SOURCE_PIN}`.\n",
              "| Review | Bloodline | Rank | Disposition | Dossier | Supported rows | Proposed label | Label kind | Census collisions | Adverse rows | Injected children | Item-gated jutsu |",
              "|---|---|---|---|---|---:|---|---|---:|---:|---:|---:|"]
    for r in sorted(index_rows):
        idx_md.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | [{r[4]}]({r[4]}.md) | {r[5]} | {r[6]} | {r[7]} | {r[8]} | {r[9]} | {r[10]} | {r[11]} |")
    idx_txt = "\n".join(idx_md) + "\n"
    ipath = os.path.join(KITS_DIR, "INDEX.md")
    if args.check:
        cur = open(ipath, encoding="utf-8").read() if os.path.exists(ipath) else None
        if cur != idx_txt:
            mismatches.append(ipath)
        if mismatches:
            print("STALE kit dossiers:\n  " + "\n  ".join(mismatches))
            return 1
        print(f"kit dossiers current ({len(ids)} bloodlines)")
        return 0
    L.write_text(ipath, idx_txt)
    print(f"wrote {len(ids)} dossiers to {KITS_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
