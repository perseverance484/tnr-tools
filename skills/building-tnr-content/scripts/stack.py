#!/usr/bin/env python3
"""Check the source stack itself. Run it at the start of every session.

The stack is 40-odd files that reference each other, cite laws by number,
carry ids that may no longer exist, and accumulate duplicates. None of that is
visible by reading, and all of it costs turns: a dead routing entry in the
index is a retrieval that returns nothing, an unverifiable id is a question
back to dauntless, a law cited by a number that moved is a wrong answer.

Usage
  python3 tnr_stack.py /path/to/stack            # full report
  python3 tnr_stack.py /path/to/stack --quiet    # errors only
  python3 tnr_stack.py /path/to/stack --ids      # id reconciliation detail
"""
import json, os, re, sys
from collections import Counter, defaultdict

ID_RE = re.compile(r"`([A-Za-z0-9_\-]{21})`")
FILE_RE = re.compile(r"`?(\d{2}[a-z]?_[A-Za-z0-9_]+\.(?:md|json|py|js))`?")
LAW_RE = re.compile(r"laws? (\d+)", re.I)
RETIRED = {
    "40_DATA_jutsu_catalog.json": "replaced by its 4x_INDEX twin; full catalogs live in the tnr-tools repo",
    "41_DATA_item_catalog.json": "replaced by its 4x_INDEX twin; full catalogs live in the tnr-tools repo",
    "42_DATA_ai_catalog.json": "replaced by its 4x_INDEX twin; full catalogs live in the tnr-tools repo",
    "43_DATA_asset_catalog.json": "replaced by its 4x_INDEX twin; full catalogs live in the tnr-tools repo",
    "47_DATA_quest_catalog.json": "replaced by its 4x_INDEX twin; full catalogs live in the tnr-tools repo",
    "45b_DATA_write_shapes.json": "superseded by 45c constructors; archived in the tnr-tools repo",
    "48_DATA_mutation_census.json": "analysis artifact, findings absorbed into doctrine; archived in the repo",
    "49_DATA_full_exemplars.json": "full exemplar dump archived in the repo; 40x is the curated working set",
    # Phase 5 (2026-08-28): storage vs intent. Live catalogs and session state are volatile,
    # so they moved to the session bundle. A stale copy here looks authoritative and is not:
    # 47_INDEX listed four quests that no longer existed and all four got picked for a capture.
    "40_INDEX_jutsu.json": "bundled to state/catalogs/; stamped per row and synced by catalog_sync.py",
    "41_INDEX_item.json": "bundled to state/catalogs/; stamped per row and synced by catalog_sync.py",
    "42_INDEX_ai.json": "bundled to state/catalogs/; stamped per row and synced by catalog_sync.py",
    "43_INDEX_asset.json": "bundled to state/catalogs/; stamped per row and synced by catalog_sync.py",
    "47_INDEX_quest.json": "bundled to state/catalogs/; stamped per row and synced by catalog_sync.py",
    "44c_DATA_ids.json": "bundled to state/catalogs/",
    "44_DATA_id_registry.md": "frozen and bundled; catalogs now record creation from push entries",
    "44b_DATA_registry_2026-08-25.md": "frozen and bundled",
    "90_STATE_board.md": "intent, not storage; bundled to state/active-context.md + status.json",
    "94_ART_disposition.md": "intent, not storage; bundled to state/",
    "25x_DATA_art_spec.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "26x_EVENT_sheet_schema.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "40x_EXEMPLARS_effects.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "45d_DATA_entity_schemas.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "45f_DATA_procedures.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "45g_DATA_checks.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "46b_DATA_tag_runtime.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "48_DATA_mission_profiles.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "art_index_2026-08-26.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "capture_example.json": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "refresh_catalogs.py": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "sim_damage.py": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "sim_turns.py": "bundled to the session bundle 2026-08-28; project knowledge is prose only, and JSON is provably retrievable so it counted toward the RAG threshold",
    "91_PLAN_stack_overhaul.md": "intent, not storage; bundled to state/",
    "92_MAP_file50_retirement.md": "archived in the tnr-tools repo",
    "README_APPLY.md": "archived in the tnr-tools repo",
    "MANIFEST.sha256": "archived in the tnr-tools repo",
    "builder_bundle.js": "GitHub is the deploy truth and a project copy drifts; upload only for editing sessions",
    "builder_loader_user.js": "lives in ViolentMonkey and the repo, not project knowledge",
    "90_SESSION_DELTA_2026-08-01.md": "absorbed into owning docs and the state board",
    "90_SESSION_DELTA_2026-08-25.md": "absorbed into owning docs and the state board",
    # Phase 3 (2026-08-26): prose migrated into the two skills. The skills are
    # loaded on demand instead of retrieved whole, so these are not rot.
    "10_TECH_pipeline.md": "migrated to building-tnr-content/references/pipeline.md",
    "20_GUIDE_jutsu.md": "migrated to building-tnr-content/references/jutsu.md",
    "21_GUIDE_ai_enemy.md": "migrated to building-tnr-content/references/ai.md (part 1)",
    "22_GUIDE_item.md": "migrated to building-tnr-content/references/item.md",
    "23_GUIDE_quest.md": "migrated to building-tnr-content/references/quest.md",
    "24_GUIDE_ai_behavior.md": "migrated to building-tnr-content/references/ai.md (part 2)",
    "25_GUIDE_assets.md": "migrated to producing-tnr-art/references/{prompts,processing}.md",
    "26_TEMPLATE_event_design.md": "migrated to building-tnr-content/references/event.md",
    "30_DOCTRINE_balance.md": "migrated to building-tnr-content/references/balance.md",
    "33_DOCTRINE_quest_tiers.md": "migrated to building-tnr-content/references/balance.md",
    "45_DATA_field_schemas.json": "hand-authored; superseded by generated 45d. Archived in the repo",
    "50_DATA_combat_facts.md": "numbers generated into 45e; formula shape pending merge into 46b",
    "70_TOOL_validate.py": "bundled at building-tnr-content/scripts/validate.py",
    "70_TOOL_calc.py": "bundled at building-tnr-content/scripts/calc.py",
    "70_TOOL_harvest.py": "bundled at building-tnr-content/scripts/harvest.py",
    "70_TOOL_stack.py": "bundled at building-tnr-content/scripts/stack.py",
    "schema_extract.py": "bundled at building-tnr-content/scripts/schema_extract.py",
}

# Archived to the tnr-tools repo rather than migrated. Consulted rarely and
# never during a mechanical build, so a citation to one is not rot - but it
# does mean the file must be re-uploaded for a session that writes into it.
ARCHIVED = {
    "27_LORE_world.md": "lore, archived to the repo (Phase 3)",
    "28_ARC_the_unwritten_war.md": "arc, archived to the repo (Phase 3)",
    "28b_ARC_storyboard.md": "arc, archived to the repo (Phase 3)",
    "29_PLAN_unwritten_build.md": "arc build plan, archived to the repo (Phase 3)",
    "31_ARC_ashen_concord.md": "arc, archived to the repo (Phase 3). 208 entries unpushed",
    "31b_ARC_salt_crown.md": "arc, archived to the repo (Phase 3)",
}

CATALOGS = ("40_INDEX_jutsu.json", "41_INDEX_item.json", "42_INDEX_ai.json",
            "43_INDEX_asset.json", "47_INDEX_quest.json")
OLD_CATALOGS = ("40_DATA_jutsu_catalog.json", "41_DATA_item_catalog.json",
                "42_DATA_ai_catalog.json", "43_DATA_asset_catalog.json",
                "47_DATA_quest_catalog.json")


def _numkey(v):
    """Compare 450000 and 450,000 and 450_000 as one value."""
    return round(float(v), 4)


def read(p):
    try:
        return open(p, errors="ignore").read()
    except Exception:
        return ""


def rows_of(path):
    try:
        d = json.load(open(path))
    except Exception:
        return []
    rows = d.get("rows") or d.get("payload", {}).get("rows") or []
    cols = d.get("cols")
    if cols and rows and isinstance(rows[0], list):
        rows = [dict(zip(cols, r)) for r in rows]
    return rows


def check(stack, quiet=False, ids_detail=False, bundle=None):
    files = set(os.listdir(stack))
    # Since 2026-08-28 project knowledge is prose only and everything a script reads lives in
    # the session bundle. A citation that resolves there is not rot, so the bundle is part of
    # the resolvable set. Without this every session opens on three false errors and learns to
    # ignore this tool, which is exactly how law 14 reached a push.
    bundled = set()
    if bundle and os.path.isdir(bundle):
        for base, _d, fs in os.walk(bundle):
            bundled |= set(fs)
    md = sorted(f for f in files if f.endswith(".md"))
    errs, warns, notes = [], [], []

    # 1. dangling file references -------------------------------------------
    refs = defaultdict(set)
    for f in md:
        for m in FILE_RE.findall(read(os.path.join(stack, f))):
            refs[m].add(f)
    missing = {k: v for k, v in refs.items()
               if k not in files and k not in RETIRED and k not in ARCHIVED
               and k not in bundled}
    for k, v in sorted(missing.items()):
        who = ", ".join(sorted(v))
        (errs if "00_INDEX.md" in v else warns).append(
            f"dangling file reference '{k}' cited by {who}")

    # 2. numbering collisions ------------------------------------------------
    FAMILIES = {"70", "90"}     # tool family and session/state family share a prefix by design
    prefix = Counter(f.split("_")[0] for f in files if re.match(r"^\d", f))
    for p, n in prefix.items():
        if n > 1 and p not in FAMILIES:
            same = sorted(f for f in files if f.split("_")[0] == p)
            if len({f.rsplit(".", 1)[-1] for f in same}) == 1:
                warns.append(f"numbering collision on '{p}': {', '.join(same)}")

    # 3. law citation integrity ---------------------------------------------
    lawfile = os.path.join(stack, "12_TECH_engine_laws.md")
    if os.path.exists(lawfile):
        defined = {int(x) for x in re.findall(r"^(\d+)[a-d]?\.", read(lawfile), re.M)}
        for f in md:
            if f == "12_TECH_engine_laws.md":
                continue
            for n in LAW_RE.findall(read(os.path.join(stack, f))):
                if int(n) not in defined:
                    errs.append(f"{f} cites 'law {n}' which is not defined in 12_TECH")
        notes.append(f"laws defined: {len(defined)} (highest {max(defined) if defined else 0})")

    # 4. id reconciliation ---------------------------------------------------
    live = set()
    cat_present = []
    for c in CATALOGS:
        p = os.path.join(stack, c)
        if not os.path.exists(p):
            hit = None
            if bundle:
                hit = next((os.path.join(b, c) for b, _d, fs in os.walk(bundle) if c in fs), None)
            if hit:
                cat_present.append(c)
                for r in rows_of(hit):
                    for k in ("id", "userId"):
                        if isinstance(r, dict) and r.get(k):
                            live.add(r[k])
                continue
            warns.append(f"catalog missing: {c}"
                         + (" (expected: catalogs live in the bundle)" if bundle else ""))
            continue
        cat_present.append(c)
        for r in rows_of(p):
            for k in ("id", "userId"):
                if isinstance(r, dict) and r.get(k):
                    live.add(r[k])
    reg_ids = defaultdict(set)
    for f in md:
        for i in ID_RE.findall(read(os.path.join(stack, f))):
            reg_ids[i].add(f)
    unverified = {i: v for i, v in reg_ids.items() if i not in live}
    if reg_ids:
        pct = 100 * len(unverified) / len(reg_ids)
        (errs if pct > 60 else warns).append(
            f"{len(unverified)} of {len(reg_ids)} ids cited in prose ({pct:.0f}%) appear in no catalog. "
            "Hidden content and post-harvest records are expected here; anything else is rot")
    if ids_detail and unverified:
        by = defaultdict(list)
        for i, v in unverified.items():
            for f in v:
                by[f].append(i)
        notes.append("unverified ids by file:")
        for f, v in sorted(by.items(), key=lambda x: -len(x[1])):
            notes.append(f"    {f:<44} {len(v)}")

    # 4b. retired files still present ----------------------------------------
    for c, why in ARCHIVED.items():
        if c in files:
            notes.append(f"{c} is archived to the repo ({why.split('(')[0].strip()}); "
                         "present here, which is fine for a session that writes into it")
    for c, why in RETIRED.items():
        if c in files:
            errs.append(f"{c} is retired from project knowledge: {why}. Delete it here")

    # 5. freshness -----------------------------------------------------------
    for c in cat_present:
        p = os.path.join(stack, c)
        if not os.path.exists(p) and bundle:
            p = next((os.path.join(b, c) for b, _d, fs in os.walk(bundle) if c in fs), p)
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        if "_freshness" not in d:
            errs.append(f"{c} has no _freshness stamp: staleness is invisible and stale data "
                        "has already produced wrong conclusions twice (run tnr_harvest.py stamp)")

    # 5b. laws that restate a generated constant (Phase 4) -------------------
    # A law carrying a figure that a generated file also carries is a second
    # copy of a fact, and the two drift silently. Two precisions, because a
    # bare value match across 400+ numeric constants collides by coincidence:
    #   ERROR - the law NAMES a constant and also spells a value it holds.
    #           That is unambiguous duplication.
    #   WARN  - a large number in law prose matches some generated value. Could
    #           be coincidence, so it is reported with every candidate name.
    consts_p = os.path.join(stack, "45e_DATA_constants.json")
    if os.path.exists(lawfile) and os.path.exists(consts_p):
        C = json.load(open(consts_p)).get("constants", {})
        by_val = defaultdict(list)
        for k, v in C.items():
            val = v.get("value")
            if isinstance(val, (int, float)) and not isinstance(val, bool) and abs(val) >= 100:
                by_val[_numkey(val)].append(k)
            elif isinstance(val, dict):
                for sub in val.values():
                    if isinstance(sub, (int, float)):
                        by_val[_numkey(sub)].append(k)
        for para in read(lawfile).split("\n"):
            if not re.match(r"^\d+[a-d]?\.", para.strip()):
                continue
            law_no = re.match(r"^(\d+[a-d]?)\.", para.strip()).group(1)
            named = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_]{3,})`", para))
            prose = re.sub(r"`[^`]*`", " ", para)
            nums = set()
            for m in re.finditer(r"\b(\d[\d,_]*(?:k\b)?)\b", prose):
                raw = m.group(1)
                mult = 1000 if raw.endswith("k") else 1
                try:
                    nums.add((raw, int(raw.rstrip("k").replace(",", "").replace("_", "")) * mult))
                except ValueError:
                    pass
            for raw, val in sorted(nums):
                cands = by_val.get(_numkey(val))
                if not cands:
                    continue
                overlap = named & set(cands)
                if overlap:
                    errs.append(f"law {law_no} names `{sorted(overlap)[0]}` AND spells its value "
                                f"({raw}). Cite the constant; a number written twice drifts")
                elif val >= 1000:
                    warns.append(f"law {law_no} spells {raw}, which 45e also generates "
                                 f"({', '.join(sorted(cands)[:3])}). Coincidence, or a restatement?")

    # 5c. generated files older than the newest source drop (Phase 4) --------
    stamps = {}
    for f in sorted(x for x in files if x.endswith(".json")):
        try:
            d = json.load(open(os.path.join(stack, f)))
        except Exception:
            continue
        prov = d.get("_provenance") if isinstance(d, dict) else None
        if isinstance(prov, dict) and prov.get("extracted"):
            stamps[f] = (prov["extracted"], prov.get("source_drop", "?"))
    if stamps:
        newest = max(v[0] for v in stamps.values())
        for f, (when, drop) in sorted(stamps.items()):
            if when < newest:
                errs.append(f"{f} was generated {when} from '{drop}' but a sibling generated file "
                            f"is stamped {newest}. Regenerate ALL of them from one drop or the "
                            "set disagrees with itself")
        notes.append(f"generated files: {len(stamps)}, all stamped {newest}"
                     if len({v[0] for v in stamps.values()}) == 1
                     else f"generated files: {len(stamps)}, MIXED stamps")

    # 6. generated files that duplicate a hand-maintained one ---------------
    gen = os.path.join(stack, "45c_DATA_constructors.json")
    hand = os.path.join(stack, "46_DATA_tag_schemas.json")
    if os.path.exists(gen) and os.path.exists(hand):
        g = json.load(open(gen))["unions"].get("AllTags", {})
        h = json.load(open(hand)).get("tags")
        if h:
            drift = set(g) - set(h)
            errs.append(f"46 still carries a hand `tags` block ({len(h)} entries) duplicating the "
                        f"generated 45c ({len(g)}). Drift already: {sorted(drift) or 'none yet'}")
        else:
            notes.append(f"45c is sole shape authority ({len(g)} tags); 46 holds judgment layers only")

    # 7. machine-readability of registries ----------------------------------
    for reg, twin in (("32_REGISTRY_shared_ai_pool.md", "32b_DATA_pool.json"),
                      ("34_REGISTRY_map_pins.md", "34b_DATA_pins.json"),
                      ("44_DATA_id_registry.md", "44c_DATA_ids.json")):
        p = os.path.join(stack, reg)
        if not os.path.exists(p):
            continue
        table_rows = len(re.findall(r"^\|", read(p), re.M))
        if table_rows > 8 and not os.path.exists(os.path.join(stack, twin)):
            warns.append(f"{reg} holds {table_rows} table rows but has no machine-readable twin "
                         f"({twin}); tools cannot consume it")

    # 8. session deltas that should have been absorbed ----------------------
    deltas = [f for f in files if f.startswith("90_SESSION_DELTA")]
    if len(deltas) > 1:
        warns.append(f"{len(deltas)} session delta files present ({', '.join(sorted(deltas))}); "
                     "absorb into the owning docs and the state board, then delete")

    # 9. size hogs -----------------------------------------------------------
    sizes = {f: os.path.getsize(os.path.join(stack, f)) for f in files}
    total = sum(sizes.values())
    for f, s in sorted(sizes.items(), key=lambda x: -x[1])[:3]:
        share = 100 * s / total
        if share > 20:
            warns.append(f"{f} is {share:.0f}% of the stack ({s//1024}KB). "
                         "If it is a staged output rather than reference, move it out")
    notes.append(f"stack total: {total//1024}KB across {len(files)} files")

    # ------------------------------------------------------------------ out
    for e in errs:
        print("ERROR  " + e)
    if not quiet:
        for w in warns:
            print("warn   " + w)
        for n in notes:
            print("note   " + n)
    print(f"\n{len(errs)} errors, {len(warns)} warnings")
    return 1 if errs else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    bundle = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--bundle=")), None)
    sys.exit(check(args[0] if args else ".",
                   "--quiet" in sys.argv, "--ids" in sys.argv, bundle))
