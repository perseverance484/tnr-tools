#!/usr/bin/env python3
"""Build craftable_recipes.json from an operator's raw crafting census download. Offline only.

    python3 harness/crafting_recipe_census/build_census.py RAW.json [--out PATH] [--allow-incomplete]
    python3 harness/crafting_recipe_census/build_census.py RAW.json --check [--out PATH]

RAW.json is the file TNRCraftCensus.download() saves (schema tnr.crafting_census.raw.v1). The
builder makes no network request. It proves coverage before it writes:

  * the capture finished (status complete, phase done) under the pinned script/source;
  * each item.getAll pass ran cursor 0..n contiguously, every non-terminal page was full and
    pointed at cursor+1, and the terminal page returned nextCursor null;
  * every list row is canBeCrafted with the pass's hidden value, and no id appears twice;
  * every distinct id has an ok item.getItemWithCraftingRequirements read whose columns equal
    its list row;
  * the confirmation list passes, taken after the detail reads, equal the first passes row for
    row, so the snapshot did not move while it was read;
  * every logged request named an allowed read procedure.

Any failure makes the verdict INCOMPLETE. INCOMPLETE output is refused unless --allow-incomplete,
and exit status is 0 only for COMPLETE. --check rebuilds in memory and fails if --out differs.

Craft-time restrictions are derived from constants and guards read at the pinned source
(SOURCE below); they describe the engine at that pin, not live behaviour after it.
"""
import argparse
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DEFAULT_OUT = os.path.join(REPO, "reports", "crafting_recipe_census", "craftable_recipes.json")

RAW_SCHEMA = "tnr.crafting_census.raw.v1"
OUT_SCHEMA = "tnr.crafting_census.v1"
SCRIPT_VERSION = "1.0.0"
PIN = "641040531176f91a3076fe5f32592ba18197a8c0"
SOURCE_PIN = f"studie-tech/TheNinjaRPG@{PIN}"
ALLOWED_PROCS = ("item.getAll", "item.getItemWithCraftingRequirements")
PASSES = (("hidden=false", False), ("hidden=true", True))
RARITIES = ("COMMON", "RARE", "EPIC", "LEGENDARY")
RANKS = ("NOVICE", "APPRENTICE", "MASTER", "FORGEMASTER")

# Read at the pin; 0 means the rank cannot craft that rarity.
SOURCE = {
    "pin": SOURCE_PIN,
    "refs": {
        "craft_guards": "app/src/server/api/routers/occupation.ts craftItem",
        "queued_start_guard": "app/src/server/utils/userQueue.ts (hidden / canBeCrafted re-checked when a queued craft starts)",
        "rank_times": "app/drizzle/constants.ts CRAFTING_TIMES_MINS",
        "consumable_times": "app/drizzle/constants.ts CONSUMABLE_CRAFTING_TIMES_MINS",
        "rank_exp": "app/drizzle/constants.ts CRAFTING_REQUIRED_EXP",
        "bucket": "app/src/libs/item.ts getInventoryBucket",
        "list": "app/src/server/api/routers/item.ts getAll + itemDatabaseFilter",
        "detail": "app/src/server/api/routers/item.ts fetchItemWithCraftingRequirements",
    },
    "CRAFTING_TIMES_MINS": {
        "NOVICE": {"COMMON": 60, "RARE": 0, "EPIC": 0, "LEGENDARY": 0},
        "APPRENTICE": {"COMMON": 40, "RARE": 65, "EPIC": 0, "LEGENDARY": 0},
        "MASTER": {"COMMON": 30, "RARE": 50, "EPIC": 70, "LEGENDARY": 0},
        "FORGEMASTER": {"COMMON": 15, "RARE": 30, "EPIC": 60, "LEGENDARY": 160},
    },
    "CONSUMABLE_CRAFTING_TIMES_MINS": {"COMMON": 5, "RARE": 10, "EPIC": 15, "LEGENDARY": 20},
    "CRAFTING_REQUIRED_EXP": {"NOVICE": 0, "APPRENTICE": 100000, "MASTER": 300000, "FORGEMASTER": 600000},
    "player_preconditions": [
        "occupation must be CRAFTING",
        "craftingStartBlockMessage(user) must be empty (user-state block)",
        "crafting queue must have room when a craft is already running",
        "quantity per request 1..10; each requirement needs quantity x requested count in inventory",
        "COOKING output must fit the carried cooking bucket",
    ],
    "not_checked_by_craftItem": "requiredLevel, bloodline and other required* fields gate USE, not crafting",
}

# Blocking flags make craftItem refuse the item for every player at the pin.
BLOCKING = {
    "HIDDEN_OUTPUT": "item is hidden; craftItem rejects hidden items",
    "EVOLUTION_ITEM": "parentItemId set; craftItem rejects evolution items",
    "EMPTY_RECIPE": "no craftingRequirements; craftItem rejects it",
    "MISSING_INGREDIENT": "a requirement points at an item id that no longer exists; no player can hold it",
    "NONPOSITIVE_QUANTITY": "a requirement quantity is below 1",
}
ADVISORY = {
    "HIDDEN_INGREDIENT": "an ingredient is hidden; check it has a real acquisition route",
    "DUPLICATE_INGREDIENT": "the same ingredient appears in more than one requirement row; craftItem checks rows independently",
    "SELF_INGREDIENT": "the item is one of its own ingredients",
    "LEGENDARY_FORGEMASTER_ONLY": "LEGENDARY: only FORGEMASTER rank can craft it",
    "INGREDIENT_ACQUISITION_UNKNOWN": "an ingredient is not craftable, hunted, gathered, in shop or traded; "
                                      "the census cannot see quest/AI/chest drops, so confirm its source",
}
SOURCE_FIELDS = ("canBeCrafted", "canBeHunted", "canBeGathered", "inShop", "canBeTraded")

ITEM_KEEP = (
    "itemType", "slot", "rarity", "hidden", "canBeCrafted", "craftingExperience", "stackSize",
    "canStack", "isEventItem", "inShop", "canBeTraded", "canBeHunted", "canBeGathered",
    "canBeImbued", "cost", "repsCost", "seichiSilverCost", "parentItemId", "battleUsageType",
    "preventBattleUsage", "destroyOnUse",
)
USE_RESTRICTIONS = (
    "requiredLevel", "bloodlineId", "requiredBloodlineMastery", "requiredNinjutsuMastery",
    "requiredGenjutsuMastery", "requiredTaijutsuMastery", "requiredBukijutsuMastery",
    "requiredSageMastery", "requiredSkillId", "requiredStrength", "requiredSpeed",
    "requiredIntelligence", "requiredWillpower",
)
INGREDIENT_KEEP = (
    "itemType", "rarity", "hidden", "canBeCrafted", "canBeHunted", "canBeGathered", "inShop",
    "canBeTraded", "isEventItem", "stackSize",
)


def iso(ms):
    if ms is None:
        return None
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat().replace("+00:00", "Z")


def canon(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"))


def verify(raw):
    """Return (coverage, reasons). reasons empty means COMPLETE."""
    reasons = []
    if raw.get("schema") != RAW_SCHEMA:
        reasons.append(f"schema {raw.get('schema')!r} != {RAW_SCHEMA}")
    if raw.get("scriptVersion") != SCRIPT_VERSION:
        reasons.append(f"scriptVersion {raw.get('scriptVersion')!r} != {SCRIPT_VERSION}")
    if raw.get("sourcePin") != SOURCE_PIN:
        reasons.append(f"sourcePin {raw.get('sourcePin')!r} != {SOURCE_PIN}")
    if raw.get("status") != "complete" or raw.get("phase") != "done":
        reasons.append(f"capture status {raw.get('status')}/{raw.get('phase')}, not complete/done")
    limit = (raw.get("config") or {}).get("limit")
    lists = raw.get("lists") or {}

    def check_pass(which, key, hidden):
        p = (lists.get(which) or {}).get(key) or {}
        pages = p.get("pages") or []
        info = {
            "pages": [{"cursor": g.get("cursor"), "rows": len(g.get("rows") or []),
                       "nextCursor": g.get("nextCursor")} for g in pages],
            "rows": sum(len(g.get("rows") or []) for g in pages),
            "terminated_on_null_cursor": bool(pages) and pages[-1].get("nextCursor") is None,
        }
        tag = f"{which} {key}"
        if not p.get("done") or not pages:
            reasons.append(f"{tag}: pass not finished")
        for i, g in enumerate(pages):
            rows = g.get("rows") or []
            inp = g.get("input") or {}
            if g.get("cursor") != i:
                reasons.append(f"{tag}: page {i} has cursor {g.get('cursor')}")
            if inp.get("canBeCrafted") is not True or inp.get("hidden") is not hidden or inp.get("limit") != limit:
                reasons.append(f"{tag}: page {i} input {inp} is not the census filter")
            last = i == len(pages) - 1
            if last:
                if g.get("nextCursor") is not None:
                    reasons.append(f"{tag}: last page nextCursor {g.get('nextCursor')} is not null")
                if len(rows) >= (limit or 0):
                    reasons.append(f"{tag}: terminal page is full ({len(rows)} rows)")
            else:
                if g.get("nextCursor") != i + 1 or len(rows) != limit:
                    reasons.append(f"{tag}: page {i} nextCursor {g.get('nextCursor')} rows {len(rows)}")
            for r in rows:
                if r.get("canBeCrafted") is not True or r.get("hidden") is not hidden:
                    reasons.append(f"{tag}: row {r.get('id')} fails the filter")
        rows = {}
        for g in pages:
            for r in g.get("rows") or []:
                if r.get("id") in rows:
                    reasons.append(f"{tag}: id {r.get('id')} on more than one page (paging shifted)")
                rows[r.get("id")] = r
        return info, rows

    coverage = {"list_filter": None, "passes": {}, "confirm_passes": {}}
    main_rows, confirm_rows = {}, {}
    for key, hidden in PASSES:
        info, rows = check_pass("main", key, hidden)
        coverage["passes"][key] = info
        for i, r in rows.items():
            if i in main_rows:
                reasons.append(f"id {i} listed as both hidden and visible")
            main_rows[i] = (key, r)
        cinfo, crows = check_pass("confirm", key, hidden)
        coverage["confirm_passes"][key] = cinfo
        confirm_rows.update(crows)
        added = sorted(set(crows) - set(rows))
        removed = sorted(set(rows) - set(crows))
        changed = sorted(i for i in set(rows) & set(crows) if canon(rows[i]) != canon(crows[i]))
        cinfo["drift"] = {"added": added, "removed": removed, "changed": changed}
        if added or removed or changed:
            reasons.append(f"snapshot drift in {key}: +{added} -{removed} ~{changed}")
    first = next(iter((lists.get("main") or {}).get("hidden=false", {}).get("pages") or []), None)
    if first:
        coverage["list_filter"] = {k: v for k, v in first["input"].items() if k not in ("cursor", "hidden")}

    details = raw.get("details") or {}
    ids = sorted(main_rows)
    if sorted(raw.get("detailIds") or []) != ids:
        reasons.append("detailIds does not equal the distinct listed ids")
    status = Counter()
    for i in ids:
        d = details.get(i)
        if not d:
            status["missing"] += 1
            reasons.append(f"no detail read for {i}")
            continue
        status[d.get("status")] += 1
        if d.get("status") != "ok":
            reasons.append(f"detail {i}: {d.get('status')} {d.get('message', '')}".strip())
            continue
        data = d.get("data") or {}
        row = main_rows[i][1]
        diff = sorted(k for k in row if canon(row[k]) != canon(data.get(k)))
        if diff:
            reasons.append(f"detail {i} differs from its list row in {diff}")
    extra = sorted(set(details) - set(ids))
    if extra:
        reasons.append(f"detail reads for unlisted ids {extra}")

    log = raw.get("requestLog") or []
    procs = Counter(r.get("proc") for r in log)
    bad = sorted(p for p in procs if p not in ALLOWED_PROCS)
    if bad:
        reasons.append(f"request log names non-census procedures {bad}")
    outcomes = Counter(r.get("outcome") for r in log)
    coverage.update({
        "distinct_ids": len(ids),
        "details": {"requested": len(ids), **dict(sorted(status.items()))},
        "requests": {"total": len(log), "by_procedure": dict(sorted(procs.items())),
                     "by_outcome": dict(sorted(outcomes.items()))},
        "halts": raw.get("halts") or [],
    })
    return coverage, main_rows, reasons


def craft_profile(item):
    rarity = item.get("rarity")
    times = SOURCE["CRAFTING_TIMES_MINS"]
    able = [r for r in RANKS if times[r].get(rarity, 0) > 0]
    consumable = item.get("itemType") == "CONSUMABLE"
    t = item.get("itemType")
    bucket = "cooking" if t == "COOKING" else "materials" if t == "MATERIAL" else "event" if item.get("isEventItem") else "normal"
    return {
        "min_crafting_rank": able[0] if able else None,
        "min_crafting_exp": SOURCE["CRAFTING_REQUIRED_EXP"][able[0]] if able else None,
        "craft_minutes_per_unit": (
            {"static": SOURCE["CONSUMABLE_CRAFTING_TIMES_MINS"].get(rarity)} if consumable
            else {r: times[r][rarity] for r in able}
        ),
        "craft_time_scales_with_rank": not consumable,
        "crafting_experience_per_unit": item.get("craftingExperience", 0),
        "output_bucket": bucket,
        "output_bucket_capacity_checked": bucket == "cooking",
    }


def build(raw, raw_bytes, raw_name):
    coverage, main_rows, reasons = verify(raw)
    details = raw.get("details") or {}
    items, ingredient_use = [], defaultdict(list)
    ingredient_meta = {}
    for iid in sorted(main_rows):
        pass_key, row = main_rows[iid]
        d = details.get(iid) or {}
        data = d.get("data") if d.get("status") == "ok" else None
        src = data or row
        flags = []
        if d.get("status") != "ok":
            flags.append("DETAIL_NOT_READ")
        reqs = (data or {}).get("craftingRequirements") or []
        ingredients = []
        seen = Counter(q.get("requirementItemId") for q in reqs)
        for q in sorted(reqs, key=lambda q: (q.get("requirementItem") or {}).get("name") or "~" + str(q.get("requirementItemId"))):
            rid = q.get("requirementItemId")
            ri = q.get("requirementItem")
            ing = {"id": rid, "name": ri.get("name") if ri else None, "quantity": q.get("quantity"),
                   "missing": ri is None, "requirement_row_id": q.get("id")}
            if ri:
                ing.update({k: ri.get(k) for k in INGREDIENT_KEEP})
                ingredient_meta[rid] = {"name": ri.get("name"), **{k: ri.get(k) for k in INGREDIENT_KEEP}}
            else:
                ingredient_meta.setdefault(rid, {"name": None, "missing": True})
            ingredients.append(ing)
            ingredient_use[rid].append({"id": iid, "name": src.get("name"), "quantity": q.get("quantity"),
                                        "output_hidden": src.get("hidden")})
        if src.get("hidden"):
            flags.append("HIDDEN_OUTPUT")
        if src.get("parentItemId"):
            flags.append("EVOLUTION_ITEM")
        if data is not None and not reqs:
            flags.append("EMPTY_RECIPE")
        if any(i["missing"] for i in ingredients):
            flags.append("MISSING_INGREDIENT")
        if any(not isinstance(i["quantity"], int) or i["quantity"] < 1 for i in ingredients):
            flags.append("NONPOSITIVE_QUANTITY")
        if any(i.get("hidden") for i in ingredients):
            flags.append("HIDDEN_INGREDIENT")
        if any(n > 1 for n in seen.values()):
            flags.append("DUPLICATE_INGREDIENT")
        if iid in seen:
            flags.append("SELF_INGREDIENT")
        if any(not i["missing"] and not any(i.get(k) for k in SOURCE_FIELDS) for i in ingredients):
            flags.append("INGREDIENT_ACQUISITION_UNKNOWN")
        if src.get("rarity") == "LEGENDARY":
            flags.append("LEGENDARY_FORGEMASTER_ONLY")
        bl = (data or {}).get("requiredBloodline")
        use = {k: src.get(k) for k in USE_RESTRICTIONS if src.get(k) is not None}
        if bl:
            use["requiredBloodline"] = {"id": bl.get("id"), "name": bl.get("name")}
        items.append({
            "id": iid,
            "name": src.get("name"),
            "list_pass": pass_key,
            **{k: src.get(k) for k in ITEM_KEEP},
            "ingredients": ingredients,
            "ingredient_count": len(ingredients),
            "total_ingredient_units": sum(i["quantity"] for i in ingredients if isinstance(i["quantity"], int)),
            "craft": craft_profile(src),
            "use_restrictions": use,
            "flags": sorted(flags),
            "blocked": sorted(f for f in flags if f in BLOCKING or f == "DETAIL_NOT_READ"),
            "craftable_by_players_at_pin": not any(f in BLOCKING or f == "DETAIL_NOT_READ" for f in flags),
        })
    items.sort(key=lambda r: ((r["name"] or "").lower(), r["id"]))

    ingredients_index = []
    for rid, uses in ingredient_use.items():
        meta = ingredient_meta.get(rid, {})
        ingredients_index.append({
            "id": rid, **meta, "missing": meta.get("missing", False),
            "recipe_count": len({u["id"] for u in uses}),
            "total_units_across_recipes": sum(u["quantity"] for u in uses if isinstance(u["quantity"], int)),
            "is_also_craftable_output": rid in main_rows,
            "used_by": sorted(uses, key=lambda u: ((u["name"] or "").lower(), u["id"])),
        })
    ingredients_index.sort(key=lambda r: ((r.get("name") or "~").lower(), r["id"]))

    flag_counts = Counter(f for it in items for f in it["flags"])
    totals = {
        "craftable_items": len(items),
        "visible": sum(1 for i in items if not i["hidden"]),
        "hidden": sum(1 for i in items if i["hidden"]),
        "craftable_by_players_at_pin": sum(1 for i in items if i["craftable_by_players_at_pin"]),
        "blocked": sum(1 for i in items if i["blocked"]),
        "with_recipe": sum(1 for i in items if i["ingredients"]),
        "empty_or_unread_recipe": sum(1 for i in items if not i["ingredients"]),
        "distinct_ingredients": len(ingredients_index),
        "requirement_rows": sum(i["ingredient_count"] for i in items),
        "by_rarity": dict(sorted(Counter(i["rarity"] for i in items).items())),
        "by_item_type": dict(sorted(Counter(i["itemType"] for i in items).items())),
        "by_min_crafting_rank": dict(sorted(Counter(str(i["craft"]["min_crafting_rank"]) for i in items).items())),
        "flags": dict(sorted(flag_counts.items())),
    }
    verdict = "COMPLETE" if not reasons else "INCOMPLETE"
    return verdict, {
        "schema": OUT_SCHEMA,
        "verdict": verdict,
        "incomplete_reasons": reasons,
        "producer": "harness/crafting_recipe_census/build_census.py",
        "capture": {
            "file": raw_name,
            "sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "schema": raw.get("schema"),
            "script_version": raw.get("scriptVersion"),
            "origin": raw.get("origin"),
            "started_at": iso(raw.get("createdAt")),
            "finished_at": iso(raw.get("finishedAt")),
            "config": raw.get("config"),
        },
        "source": SOURCE,
        "flag_legend": {"blocking": BLOCKING, "advisory": ADVISORY,
                        "DETAIL_NOT_READ": "the detail read failed or is missing; recipe unknown"},
        "coverage": coverage,
        "totals": totals,
        "items": items,
        "ingredients": ingredients_index,
    }


def render(doc):
    return json.dumps(doc, indent=1, ensure_ascii=False) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("raw")
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--allow-incomplete", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    raw_bytes = open(a.raw, "rb").read()
    raw = json.loads(raw_bytes)
    verdict, doc = build(raw, raw_bytes, os.path.basename(a.raw))
    text = render(doc)
    t = doc["totals"]
    print(f"{verdict}: {t['craftable_items']} craftable ({t['visible']} visible, {t['hidden']} hidden), "
          f"{t['distinct_ingredients']} distinct ingredients, {t['blocked']} blocked")
    for r in doc["incomplete_reasons"]:
        print(f"  INCOMPLETE: {r}", file=sys.stderr)
    if a.check:
        current = open(a.out, encoding="utf-8").read() if os.path.exists(a.out) else None
        if current != text:
            print(f"{a.out} is stale or missing", file=sys.stderr)
            return 1
        print(f"{a.out} current")
        return 0 if verdict == "COMPLETE" else 2
    if verdict != "COMPLETE" and not a.allow_incomplete:
        print("refusing to write an INCOMPLETE census (pass --allow-incomplete to inspect it)", file=sys.stderr)
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"wrote {a.out}")
    return 0 if verdict == "COMPLETE" else 2


if __name__ == "__main__":
    sys.exit(main())
