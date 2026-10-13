#!/usr/bin/env python3
"""Compare the crafting-cache draft with existing chests' loot tables. Offline only.

    python3 harness/crafting_caches/compare_chests.py RESULTS.json [RESULTS.json ...] [--out PATH]

RESULTS are Forge/builder results bundles (`captures[]`), normally from the read-only
push/95_chest_loot_baseline_capture.json run. Any captured item row whose effects include a
`noncombatconsumereward` with `reward_items` is treated as a chest; when an id appears in several
bundles the row with the newest updatedAt wins. A row whose id/name disagrees with the push/95
expectation is reported and skipped. Item rarities come from the crafting census and the seed
index (`harvests/seed/41_INDEX_item.json`).

Line semantics (item reference §4): every reward_items line rolls independently with
`number`% chance and pays `quantity` of its id (one id per line in practice; a multi-id line is
counted once per id).
"""
import argparse
import json
import os
import sys
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DRAFT = os.path.join(REPO, "docs", "design", "crafting_caches", "caches_draft.json")
CENSUS = os.path.join(REPO, "reports", "crafting_recipe_census", "craftable_recipes.json")
SEED = os.path.join(REPO, "harvests", "seed", "41_INDEX_item.json")
MANIFEST = os.path.join(REPO, "push", "95_chest_loot_baseline_capture.json")
OUT = os.path.join(REPO, "docs", "design", "crafting_caches", "CHEST_COMPARISON.md")
RARITIES = ("COMMON", "RARE", "EPIC", "LEGENDARY")
MONEY_KEYS = ("reward_money", "reward_tokens", "reward_prestige", "reward_reputation", "reward_seichi_silver")


def catalog():
    meta = {}
    seed = json.load(open(SEED, encoding="utf-8"))
    for r in seed["rows"]:
        row = dict(zip(seed["cols"], r))
        meta[row["id"]] = {"name": row["n"], "rarity": row["rar"], "type": row["type"]}
    census = json.load(open(CENSUS, encoding="utf-8"))
    for g in census["ingredients"]:
        meta[g["id"]] = {"name": g.get("name"), "rarity": g.get("rarity"), "type": g.get("itemType")}
    for i in census["items"]:
        meta[i["id"]] = {"name": i["name"], "rarity": i["rarity"], "type": i["itemType"]}
    return meta


def chests_from_bundles(paths):
    expected = {}
    if os.path.exists(MANIFEST):
        seed = {r[0]: r[1] for r in json.load(open(SEED, encoding="utf-8"))["rows"]}
        for rd in json.load(open(MANIFEST, encoding="utf-8"))["capture"]["before"]:
            expected[rd["input"]["id"]] = seed.get(rd["input"]["id"])
    found, problems, read_ok = {}, [], set()
    for p in paths:
        bundle = json.load(open(p, encoding="utf-8"))
        for c in bundle.get("captures") or []:
            row = c.get("data")
            if isinstance(row, dict) and "data" in row and isinstance(row["data"], dict):
                row = row["data"]
            if not (isinstance(row, dict) and c.get("ok", True) and row.get("id")):
                if (c.get("input") or {}).get("id") in expected:
                    problems.append(f"{os.path.basename(p)}: read of {c['input']['id']} failed: {c.get('error')}")
                continue
            want = (c.get("input") or {}).get("id")
            read_ok.add(row["id"])
            if want and row["id"] != want:
                problems.append(f"{os.path.basename(p)}: asked {want}, got {row['id']}")
                continue
            if row["id"] in expected and expected[row["id"]] and row.get("name") != expected[row["id"]]:
                problems.append(f"{row['id']}: name {row.get('name')!r}, seed index says {expected[row['id']]!r}")
            eff = next((e for e in row.get("effects") or [] if e.get("type") == "noncombatconsumereward"
                        and e.get("reward_items")), None)
            if not eff:
                continue
            prev = found.get(row["id"])
            if not prev or str(row.get("updatedAt")) > str(prev["row"].get("updatedAt")):
                found[row["id"]] = {"row": row, "effect": eff, "src": os.path.basename(p)}
    missing = sorted(i for i in expected if i not in found and i not in read_ok)
    not_chests = sorted(i for i in expected if i not in found and i in read_ok)
    return found, problems, missing, not_chests


def metrics(lines, meta, extra=None):
    """lines: [{ids:[...], number, quantity}]"""
    ev_units = 0.0
    hit = 0.0
    by_rar = Counter()
    by_item = defaultdict(float)
    guaranteed = 0
    qty = Counter()
    for ln in lines:
        ids = ln.get("ids") or [ln.get("id")]
        p = float(ln.get("number", ln.get("chance", 0))) / 100
        q = ln.get("quantity", 1)
        hit += p
        guaranteed += p >= 1
        qty[q] += 1
        for i in ids:
            ev_units += p * q
            by_item[i] += p * q
            by_rar[(meta.get(i) or {}).get("rarity") or "?"] += p * q
    chances = sorted(float(ln.get("number", ln.get("chance", 0))) for ln in lines)
    return {
        "lines": len(lines), "distinct_items": len(by_item), "guaranteed_lines": guaranteed,
        "expected_lines_hit": hit, "expected_units": ev_units,
        "by_rarity": {r: by_rar.get(r, 0.0) for r in RARITIES + ("?",) if by_rar.get(r)},
        "chance_min": chances[0] if chances else None, "chance_max": chances[-1] if chances else None,
        "quantities": dict(sorted(qty.items())), "extra": extra or {}, "by_item": by_item,
    }


def fmt_rar(d):
    return ", ".join(f"{k[0]}{v:.1f}" for k, v in d.items()) or "-"


def render(existing, draft_rows, meta, problems, missing, sources, not_chests=()):
    out = ["# Chest loot comparison (generated)", "",
           "Generated by `harness/crafting_caches/compare_chests.py`. Existing chests come from captured live",
           f"rows ({', '.join(sorted(sources)) or 'no bundles'}); the three crafting caches come from",
           "`caches_draft.json` and are **proposals**.", "",
           "Columns: lines; lines at 100%; expected lines hit per open; expected item units per open;",
           "expected units by reward rarity (C/R/E/L); chance range %; quantities used (qty×lines); other rewards.", ""]
    if missing:
        out += [f"**Coverage:** {len(missing)} of the push/95 chests are not in the supplied bundles yet: "
                + ", ".join(f"`{m}`" for m in missing) + ". The comparison is partial until push/95 runs.", ""]
    if not_chests:
        out += ["**Read but not loot chests** (no `noncombatconsumereward.reward_items`): "
                + ", ".join(f"{(meta.get(i) or {}).get('name', i)} `{i}`" for i in not_chests) + ".", ""]
    unknown = sorted({(ch["row"]["name"], i) for ch in existing.values()
                      for ln in ch["effect"]["reward_items"] for i in ln.get("ids") or [] if i not in meta})
    if unknown:
        out += ["**Reward ids not in the census or seed index.** A malformed id never resolves; a valid one may "
                "be newer than the index:", ""]
        out += [f"- {n}: `{i}`" + (" — malformed placeholder; it matches no item id"
                                    if not i.replace("-", "").replace("_", "").isalnum() else "")
                for n, i in unknown] + [""]
    if problems:
        out += ["**Problems:**", ""] + [f"- {p}" for p in problems] + [""]
    head = ["| Chest | Rarity | Lines | 100% | Hit/open | Units/open | By rarity | Chance % | Quantities | Other |",
            "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |"]

    def row(name, rar, m):
        other = ", ".join(f"{k.replace('reward_', '')} {v:,}" for k, v in m["extra"].items()) or "-"
        q = ", ".join(f"{k}×{v}" for k, v in m["quantities"].items())
        return (f"| {name} | {rar} | {m['lines']} | {m['guaranteed_lines']} | {m['expected_lines_hit']:.2f} | "
                f"{m['expected_units']:.2f} | {fmt_rar(m['by_rarity'])} | {m['chance_min']:g}–{m['chance_max']:g} | {q} | {other} |")

    out += ["## Existing chests", ""] + head
    for cid, ch in sorted(existing.items(), key=lambda kv: kv[1]["row"]["name"]):
        e = ch["effect"]
        extra = {k: e[k] for k in MONEY_KEYS if isinstance(e.get(k), (int, float)) and e.get(k)}
        out.append(row(ch["row"]["name"], ch["row"].get("rarity"), metrics(e["reward_items"], meta, extra)))
    out += ["", "## Crafting caches (draft)", ""] + head
    for name, lines in draft_rows:
        out.append(row(name, "COMMON (proposed)", metrics(lines, meta)))
    out += ["", "## Same reagent, existing chests vs draft", "",
            "Expected units per open of each draft reagent in every existing chest that also pays it out.", "",
            "| Draft cache | Reagent | Draft / open | Existing chests / open |", "| --- | --- | ---: | --- |"]
    ex_items = {cid: metrics(ch["effect"]["reward_items"], meta)["by_item"] for cid, ch in existing.items()}
    for name, lines in draft_rows:
        mine = metrics(lines, meta)["by_item"]
        for rid in sorted(mine, key=lambda k: (meta.get(k) or {}).get("name") or k):
            others = sorted(((existing[c]["row"]["name"], v[rid]) for c, v in ex_items.items() if rid in v),
                            key=lambda t: -t[1])
            o = "; ".join(f"{n} {u:.1f}" for n, u in others) or "none"
            out.append(f"| {name} | {(meta.get(rid) or {}).get('name', rid)} | {mine[rid]:.2f} | {o} |")
    out += ["", "## What each existing chest pays out", ""]
    for cid, ch in sorted(existing.items(), key=lambda kv: kv[1]["row"]["name"]):
        out.append(f"- **{ch['row']['name']}**: " + "; ".join(
            f"{(meta.get(i) or {}).get('name', i)} {ln.get('quantity', 1)}@{ln.get('number')}%"
            for ln in ch["effect"]["reward_items"] for i in ln.get("ids") or []))
    out.append("")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bundles", nargs="+")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args(argv)
    meta = catalog()
    existing, problems, missing, not_chests = chests_from_bundles(a.bundles)
    draft = json.load(open(DRAFT, encoding="utf-8"))
    draft_rows = [(c["name"], c["lines"]) for c in draft["caches"]]
    srcs = {v["src"] for v in existing.values()}
    text = render(existing, draft_rows, meta, problems, missing, srcs, not_chests) + "\n"
    open(a.out, "w", encoding="utf-8").write(text)
    print(f"{len(existing)} existing chests, {len(missing)} push/95 chests missing, {len(problems)} problems -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
