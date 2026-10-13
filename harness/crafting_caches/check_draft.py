#!/usr/bin/env python3
"""Validate the crafting-cache draft against the census and report what each cache yields.

    python3 harness/crafting_caches/check_draft.py [--draft PATH] [--census PATH] [--report PATH]

Offline only. Exit 0 when every hard check passes; 1 otherwise. Hard checks:
  * the census is COMPLETE and its capture sha256 matches the one the draft names;
  * every line names a census item by id, and the name matches;
  * no line references a hidden item, an event item, or a listed exclusion;
  * 0 < chance <= 100, 1 <= quantity <= the item's stackSize;
  * drop doctrine (engine law 22): a line's quantity shares no common factor with any recipe
    quantity of that item across player-craftable recipes;
  * each cache's targets are player-craftable recipes, every target ingredient is carried by the
    cache or is itself a target of that cache (Pill Pack is assembled from pills), and the cache
    carries nothing that none of its targets uses.
The report (markdown) gives expected units per open, the expected opens to fund one craft of each
target (crafted ingredients expanded to their reagents), and the leakage: other player recipes
that use something the cache hands out. Numbers are only as good as the draft's PROPOSED chances
and quantities.
"""
import argparse
import json
import math
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DRAFT = os.path.join(REPO, "docs", "design", "crafting_caches", "caches_draft.json")
CENSUS = os.path.join(REPO, "reports", "crafting_recipe_census", "craftable_recipes.json")
REPORT = os.path.join(REPO, "docs", "design", "crafting_caches", "CACHE_YIELD_REPORT.md")


def load(draft_path, census_path):
    return json.load(open(draft_path, encoding="utf-8")), json.load(open(census_path, encoding="utf-8"))


def index(census):
    """id -> {name, hidden, isEventItem, stackSize, rarity, itemType} over items and ingredients."""
    rows = {}
    for g in census["ingredients"]:
        rows[g["id"]] = {k: g.get(k) for k in ("name", "hidden", "isEventItem", "stackSize", "rarity", "itemType")}
    for i in census["items"]:
        rows[i["id"]] = {k: i.get(k) for k in ("name", "hidden", "isEventItem", "stackSize", "rarity", "itemType")}
    return rows


def recipe_quantities(census):
    q = defaultdict(set)
    for i in census["items"]:
        if i["craftable_by_players_at_pin"]:
            for x in i["ingredients"]:
                q[x["id"]].add(x["quantity"])
    return q


def check(draft, census):
    errors = []
    if census.get("verdict") != "COMPLETE":
        errors.append(f"census verdict {census.get('verdict')}")
    if draft["census"]["capture_sha256"] != census["capture"]["sha256"]:
        errors.append("draft names a different census capture than the one supplied")
    rows = index(census)
    rq = recipe_quantities(census)
    excluded = draft.get("exclusions", {}).get("ids", {})
    for c in draft["caches"]:
        for n, ln in enumerate(c["lines"]):
            tag = f"{c['key']}[{n}] {ln.get('name')}"
            r = rows.get(ln["id"])
            if not r:
                errors.append(f"{tag}: id {ln['id']} not in census")
                continue
            if r["name"] != ln["name"]:
                errors.append(f"{tag}: census name is {r['name']!r}")
            if r["hidden"]:
                errors.append(f"{tag}: item is hidden")
            if r["isEventItem"]:
                errors.append(f"{tag}: item is an event item")
            if ln["id"] in excluded:
                errors.append(f"{tag}: item is on the exclusion list")
            if not (0 < ln["chance"] <= 100):
                errors.append(f"{tag}: chance {ln['chance']}")
            if not (isinstance(ln["quantity"], int) and 1 <= ln["quantity"] <= (r["stackSize"] or 1)):
                errors.append(f"{tag}: quantity {ln['quantity']} vs stackSize {r['stackSize']}")
            shared = sorted(q for q in rq.get(ln["id"], ()) if math.gcd(q, ln["quantity"]) > 1)
            if shared:
                errors.append(f"{tag}: quantity {ln['quantity']} shares a factor with recipe quantities {shared}")
        recipes = {i["id"]: i for i in census["items"]}
        target_ids = {t["id"] for t in c.get("targets", [])}
        carried = {ln["id"] for ln in c["lines"]}
        used = set()
        for t in c.get("targets", []):
            r = recipes.get(t["id"])
            if not r or r["name"] != t["name"] or not r["craftable_by_players_at_pin"]:
                errors.append(f"{c['key']} target {t['name']}: not a player-craftable census recipe")
                continue
            for x in r["ingredients"]:
                used.add(x["id"])
                if x["id"] not in carried and x["id"] not in target_ids:
                    errors.append(f"{c['key']} target {t['name']}: ingredient {x['name']} is not supplied")
        for extra in sorted(carried - used):
            errors.append(f"{c['key']}: carries {rows.get(extra, {}).get('name', extra)}, which no target uses")
    return errors


def raw_demand(recipe_id, recipes, carried, depth=0):
    """Expand one craft into reagent units, crafting any non-carried ingredient from its recipe."""
    need = defaultdict(float)
    for x in recipes[recipe_id]["ingredients"]:
        if x["id"] in carried or depth > 4 or x["id"] not in recipes:
            need[x["id"]] += x["quantity"]
        else:
            for k, v in raw_demand(x["id"], recipes, carried, depth + 1).items():
                need[k] += v * x["quantity"]
    return need


def expected(cache):
    ev = defaultdict(float)
    for ln in cache["lines"]:
        ev[ln["id"]] += ln["quantity"] * ln["chance"] / 100
    return ev


def report(draft, census):
    rows = index(census)
    names = {k: v["name"] for k, v in rows.items()}
    recipes = {i["id"]: i for i in census["items"] if i["craftable_by_players_at_pin"]}
    out = ["# Crafting cache yield report (generated)", "",
           "Generated by `harness/crafting_caches/check_draft.py` from `docs/design/crafting_caches/caches_draft.json`",
           f"and the census capture `{census['capture']['sha256'][:12]}`. Every chance and quantity is a **proposal**.", ""]
    for c in draft["caches"]:
        ev = expected(c)
        lines = c["lines"]
        out += [f"## {c['name']} ({c['key']})", "", c["theme"], "",
                f"- Lines: {len(lines)}; expected lines hit per open: {sum(l['chance'] for l in lines) / 100:.2f}",
                f"- Expected total units per open: {sum(ev.values()):.2f}", "",
                "| Item | Rarity | Lines (qty@%) | Expected units / open |", "| --- | --- | --- | ---: |"]
        by = defaultdict(list)
        for ln in lines:
            by[ln["id"]].append(f"{ln['quantity']}@{ln['chance']:g}")
        for i in sorted(ev, key=lambda k: (-ev[k], names[k])):
            out.append(f"| {names[i]} | {rows[i]['rarity']} | {', '.join(by[i])} | {ev[i]:.2f} |")
        out += ["", "### Targets", "",
                "Expected opens to fund one craft: the bottleneck reagent's demand divided by its expected units per open.", "",
                "| Recipe | Rarity | Reagents per craft | Bottleneck | Expected opens per craft |",
                "| --- | --- | --- | --- | ---: |"]
        for t in c.get("targets", []):
            if t["id"] not in recipes:
                continue
            need = raw_demand(t["id"], recipes, set(ev))
            if not all(k in ev for k in need):
                out.append(f"| {t['name']} | {recipes[t['id']]['rarity']} | - | not fully supplied | - |")
                continue
            opens = {k: v / ev[k] for k, v in need.items()}
            b = max(opens, key=opens.get)
            reag = ", ".join(f"{names[k]} ×{v:g}" for k, v in sorted(need.items(), key=lambda kv: names[kv[0]]))
            out.append(f"| {t['name']} | {recipes[t['id']]['rarity']} | {reag} | {names[b]} | {opens[b]:.1f} |")
        target_ids = {t["id"] for t in c.get("targets", [])}
        leaks = []
        for r in recipes.values():
            if r["id"] in target_ids:
                continue
            hit = sorted({names[x["id"]] for x in r["ingredients"] if x["id"] in ev})
            if hit:
                leaks.append((r["itemType"], r["rarity"], r["name"], hit))
        out += ["", "### Leakage: other recipes that use this cache's contents", ""]
        if leaks:
            out += ["| Recipe | Type | Rarity | Uses from this cache |", "| --- | --- | --- | --- |"]
            out += [f"| {n} | {t} | {r} | {', '.join(h)} |" for t, r, n, h in sorted(leaks)]
        else:
            out.append("None.")
        out.append("")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--draft", default=DRAFT)
    ap.add_argument("--census", default=CENSUS)
    ap.add_argument("--report", default=REPORT)
    ap.add_argument("--check", action="store_true", help="fail if the report on disk is stale")
    a = ap.parse_args(argv)
    draft, census = load(a.draft, a.census)
    errors = check(draft, census)
    for e in errors:
        print(f"ERROR {e}", file=sys.stderr)
    text = report(draft, census) + "\n"
    if a.check:
        cur = open(a.report, encoding="utf-8").read() if os.path.exists(a.report) else None
        if cur != text:
            print(f"{a.report} is stale", file=sys.stderr)
            return 1
    else:
        open(a.report, "w", encoding="utf-8").write(text)
    print(f"{'OK' if not errors else 'FAIL'}: {sum(len(c['lines']) for c in draft['caches'])} lines in "
          f"{len(draft['caches'])} caches; {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
