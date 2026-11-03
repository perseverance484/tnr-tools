#!/usr/bin/env python3
"""Skyglass uber key economy (RUL-2026-11-02-104; RUL-100 item 1, RUL-102): the four Invitation shards, which drop
only, and the Heartglass / The Remainder variant tokens and variants.

    python3 push/skyglass_uber_economy.gen.py
        -> push/417_skyglass_uber_economy.json         (creates, all HIDDEN: 6 items, 2 variants)
    python3 push/skyglass_uber_economy.gen.py --link <417 bundle>
        -> push/418_skyglass_uber_economy_link.json    (2 item edits: each token bound 1:1 to its variant)
    python3 push/skyglass_uber_economy.gen.py --unhide <417 bundle>
        -> push/419_skyglass_uber_economy_unhide.json  (6 item edits, hidden false)
    python3 push/skyglass_uber_economy.gen.py --drops <417 bundle>
        -> push/420_skyglass_uber_shard_drops.json     (11 live quest edits re-sent whole: the shard drops)

Run order: 417 -> (bundle) build 418, 419, 420 -> gates -> run 418 -> 419 -> 420 -> the director's dungeon editor row
(Shard of the Keel on the full Wreck). 418-420 need 417's results for literal ids (L01), so none is committed before
that bundle exists. 420 and the editor row must follow 419: quest rewards do not filter hidden items
(theninjarpg@3314d122: no `hidden` test in the reward path), so a drop may never point at a hidden shard.

Design:
  * RUL-104: Salvage, The Glass Answers and the Stilled Echo are cut. The shards drop only; trading is the pity.
  * RUL-100 item 1: one of each shard is the Mother of Echoes quest's entryItems (the fight build); there is no
    Invitation item. Shards are plain tradeable items with no effect.
  * Rates (RATES): the economy model re-run without Salvage (fable/skyglass-economy-model, recommended.json S1-S4,
    out/rate_search.csv). Proposals: the Crownhold drop is the wall at any legal rate (Lantern-gated), see the README.
  * Tokens: the 1:1 trophy pattern (pipeline 2.10): token create with variantId null (417 phase 1), variant create
    with requiredItemId = the token (417 phase 2), token edit binding variantId (418). Both trade (RUL-102, RUL-105:
    both drop on every uber clear). Variants have no hidden state, so both show on their base weapons as "Need <token>"
    from 417's run (the push/329 precedent).

Do not hand-edit the outputs.
"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("skyglass_items", os.path.join(ROOT, "push/skyglass_items.gen.py"))
IT = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IT)

NUM, LINK, UNHIDE, DROPS = 417, 418, 419, 420
PFX = "sg417_"
PLACEHOLDER = IT.PLACEHOLDER  # engine default image (RUL-2026-10-30-059)
HEARTGLASS_ART = "art/skyglass_variant_skins/exports/icon-variant-heartglass.webp"

UNWRITTEN = "m0RZDUDnwQu_0BtOJgHi9"      # The Unwritten (fan): push/371 variant rows
INK_OF_THE_VOID = "wE1QeldWTjls2Cf43cFjf"  # Ink of the Void (bow): push/371 variant rows (Stargazer)
# Variant orders taken on these bases by push/329 (The Unwritten Order 1, Captain's Gunbai 2; Stargazer 1). Variants
# without a token are not captured on these two items; a taken order refuses the create cleanly (329 Roll-Call).
ORDER = {UNWRITTEN: 3, INK_OF_THE_VOID: 2}

# Integer percent per clear (RUL-2026-10-31-087). Source: the economy model re-run for RUL-104
# (fable/skyglass-economy-model, recommended.json S1-S4). Keel lives on the full Wreck DUNGEON (the editor row);
# the other three are added to the live quests by 420.
RATES = {"keel": 15, "crown": 100, "tide": 75, "ledger": 35}
DROPS_TABLE = {  # shard -> quests whose every win_quest ending gets one drop line
    "crown": ["Crownhold"],
    "tide": ["The Sealed Reliquary", "The Fall", "The Rotted Reliquary", "The Burning Heading"],
    "ledger": ["The Trophy Hold", "The Bone Store", "The Snare Room", "The Overgrown Stores", "The Ore Vault",
               "The Bloom Cellar"],
}
# Latest committed definitions (re-sent whole; no later edit in push/ or harvests), with their verified run bundles.
SOURCES = {
    "push/383_skyglass_publish_chart_runs.json": "harvests/inbox/tnr_results_1793492872251.json",
    "push/384_skyglass_publish_haul.json": "harvests/inbox/tnr_results_1793492888772.json",
    "push/385_skyglass_publish_crownhold_hunts.json": "harvests/inbox/tnr_results_1793492929044.json",
}


# ---------------------------------------------------------------------------------------------------------------
# Text (design voice: story line in italics, then what it does; SKYGLASS_TEXT.md section 4 conventions)
# ---------------------------------------------------------------------------------------------------------------
def rate(key, where):
    return f"{where}: every clear" if RATES[key] == 100 else f"{where} {RATES[key]}%"


INVITE = ("<b>Her invitation:</b> carry all four shards (Keel, Crown, Tide and Ledger) to open the way to "
          "<b>The Mother of Echoes</b>. All four are spent when the fight begins. Shards trade.")
SHARDS = [  # (key, name, story line, drop line)
    ("keel", "Shard of the Keel",
     "A splinter of the Mother Glass, shaken loose from the Core the war-ship was built around.",
     rate("keel", "Skyglass Wreck clear")),
    ("crown", "Shard of the Crown",
     "A splinter of the Mother Glass, fallen from the broken Command Crown.",
     rate("crown", "Crownhold")),
    ("tide", "Shard of the Tide",
     "A splinter of the Mother Glass, washed out of the echoes the Core could not hold.",
     rate("tide", "The Sealed Reliquary, The Fall and both Legendary chart runs")),
    ("ledger", "Shard of the Ledger",
     "A splinter of the Mother Glass, entered in the stores ledger and never claimed.",
     rate("ledger", "every Haul run")),
]
SHARDS_BY_KEY = {k: n for k, n, *_ in SHARDS}


def shard_desc(story, drop):
    return f"<i>{story}</i><br><br><b>Drops:</b> {drop}<br>{INVITE}"


TOKEN_TMPL = ("<i>{story}</i><br><br>Unlocks <b>{v}</b>, a variant of <b>{base}</b> (new look and name, same stats). "
              "You must own {base}: open it, choose <b>Variants</b>, then <b>Use {v}</b>. Once per player.")
TOKENS = [  # (key, variant/token name, base name, base id, token story, variant description, image)
    ("heartglass", "Heartglass", "The Unwritten", UNWRITTEN,
     "Cut from Sayo's own glass. Every pane still holds a face, and every face is listening.",
     "The Unwritten remade in thin panes of cyan glass, a faint face pressed behind each. When it opens, the faces "
     "turn toward your target.", "@img:icon-variant-heartglass.webp"),
    ("remainder", "The Remainder", "Ink of the Void", INK_OF_THE_VOID,
     "What the Silence did not finish drinking. It makes no sound at all.",
     "Ink of the Void gone matte black and still. It drinks the light around it, its string never glints, and dust "
     "hangs unmoving where its arrows pass.", PLACEHOLDER),
]

# RUL-2026-11-02-102 / -105: quest rewards have no once-per-player flag (validators/base.ts:20-28) and both tokens drop
# on every uber clear (25% each, placeholder), so both trade: a duplicate is worth something.
TRADEABLE_TOKENS = {"heartglass", "remainder"}
TRADE_NOTE = "<br>Tradeable: you only ever need one, so sell the rest."


# ---------------------------------------------------------------------------------------------------------------
# 417: creates
# ---------------------------------------------------------------------------------------------------------------
def ref(key):
    return "@item:" + PFX + key


def items():
    out = []
    for key, name, story, drop in SHARDS:
        e = IT.create(PFX + key, name, shard_desc(story, drop), "LEGENDARY", "OTHER", True, battle="Invitation shard")
        e["data"]["destroyOnUse"] = False
        out.append(e)
    for key, v, base, _bid, story, _vdesc, _img in TOKENS:
        trade = key in TRADEABLE_TOKENS
        desc = TOKEN_TMPL.format(story=story, v=v, base=base) + (TRADE_NOTE if trade else "")
        out.append(IT.create(PFX + key, v, desc, "LEGENDARY", "CONSUMABLE", trade, [IT._token_effect()],
                             battle="Variant token"))
    return out


def variants():
    out = []
    for key, v, _base, bid, _story, vdesc, img in TOKENS:
        out.append({"entity": "itemVariant", "slot": "create", "srcId": PFX + "var_" + key, "phase": 2, "name": v,
                    "data": {"itemId": bid, "name": v, "image": img, "requiredItemId": ref(key),
                             "costType": "VARIANT_TOKEN", "cost": 1, "order": ORDER[bid], "description": vdesc,
                             "hidden": True}})
    return out


def image_pack():
    ref_ = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", HEARTGLASS_ART],
                                   text=True).strip()
    if not ref_:
        sys.exit(f"{HEARTGLASS_ART} is not committed")
    disk = open(os.path.join(ROOT, HEARTGLASS_ART), "rb").read()
    if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref_}:{HEARTGLASS_ART}"]) != disk:
        sys.exit(f"{HEARTGLASS_ART}: working copy differs from {ref_}")
    name = os.path.basename(HEARTGLASS_ART)
    return {"ref": ref_, "files": {name: {"path": HEARTGLASS_ART, "sha256": hashlib.sha256(disk).hexdigest(),
                                         "bytes": len(disk)}}}


def placeholders(entries):
    return [f"{e['entity']} {e['srcId']}: {e['data']['name']} (engine default image)"
            for e in entries if e["data"].get("image") == PLACEHOLDER]


def write(num, slug, note, items_, extra=None):
    m = {"_note": note + " Generated by push/skyglass_uber_economy.gen.py; do not hand-edit."}
    if extra:
        m.update(extra)
    m["items"] = items_
    path = os.path.join(ROOT, f"push/{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items_)} items")


def build_create():
    entries = items() + variants()
    pack = image_pack()
    write(NUM, "skyglass_uber_economy", (
        f"push/{NUM}, all HIDDEN (RUL-2026-11-02-104). Phase 1: the four Invitation shards (Legendary, tradeable, no "
        "effect; drop only, at " + ", ".join(f"{SHARDS_BY_KEY[k]} {v}%" for k, v in RATES.items()) + "; the Mother "
        "of Echoes quest takes one of each as entryItems), the Heartglass and The Remainder variant tokens (both "
        f"tradeable, RUL-102/-105) (variantId null until push/{LINK}). Phase 2: the Heartglass variant on The Unwritten "
        "and The Remainder on Ink of the Void (variants have no hidden state: each shows as 'Need <token>' from this "
        "run). Placeholders in _placeholders."),
        entries, {"dedupNames": True, "_placeholders": placeholders(entries),
                  "imgSizes": {k: v["bytes"] for k, v in pack["files"].items()}, "imagePack": pack})


# ---------------------------------------------------------------------------------------------------------------
# 418-420: built from 417's results bundle (literal ids, L01)
# ---------------------------------------------------------------------------------------------------------------
def created(bundle):
    b = json.load(open(bundle))
    got = {}
    for e in b.get("entries") or []:
        if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and (e.get("srcId") or "").startswith(PFX):
            got[e["srcId"]] = e["id"]
    for k, v in (b.get("idmap") or {}).items():
        if k.startswith(PFX):
            got.setdefault(k, v)
    want = {PFX + k for k, *_ in SHARDS} | {PFX + k for k, *_ in TOKENS} | {PFX + "var_" + k for k, *_ in TOKENS}
    missing = sorted(want - set(got))
    if missing:
        raise SystemExit(f"{os.path.basename(bundle)} is not push/{NUM}'s full results; missing {missing}")
    return got


def build_link(bundle):
    ids = created(bundle)
    out = [{"entity": "item", "slot": "edit", "targetId": ids[PFX + key], "name": f"{v} (token): bind its variant",
            "data": {"target": "SELF", "destroyOnUse": True, "preventBattleUsage": True,
                     "effects": [IT._token_effect(ids[PFX + "var_" + key])]}}
           for key, v, *_ in TOKENS]
    write(LINK, "skyglass_uber_economy_link", (
        f"push/{LINK} (after push/{NUM}, from {os.path.basename(bundle)}; literal ids, L01): Heartglass and The Remainder "
        "are bound to their own variants (pipeline 2.10 step 3). Fetch-merge item edits; both stay hidden."), out)


def build_unhide(bundle):
    ids = created(bundle)
    out = [{"entity": "item", "slot": "edit", "targetId": ids[PFX + k], "name": f"{n}: unhide", "data": {"hidden": False}}
           for k, n, *_ in SHARDS]
    out += [{"entity": "item", "slot": "edit", "targetId": ids[PFX + k], "name": f"{v} (token): unhide",
             "data": {"hidden": False}} for k, v, *_ in TOKENS]
    write(UNHIDE, "skyglass_uber_economy_unhide", (
        f"push/{UNHIDE} (after push/{LINK}; from {os.path.basename(bundle)}; literal ids, L01): unhide the four shards "
        f"and the two variant tokens. Run before push/{DROPS} and before the Keel editor row."), out)


def build_drops(bundle):
    ids = created(bundle)
    by_name, packs = {}, {}
    for f, results in SOURCES.items():
        packs[f] = json.load(open(os.path.join(ROOT, f))).get("imagePack")
        r = json.load(open(os.path.join(ROOT, results)))
        verified = {e.get("id") for e in r.get("entries") or [] if e.get("state") == "ok" and e.get("verdict") == "match"}
        for e in json.load(open(os.path.join(ROOT, f)))["items"]:
            if e["entity"] != "quest":
                continue
            assert e["targetId"] in verified, (f, e["name"])
            by_name[e["data"]["name"]] = e
    out, diff = [], {}
    for key, quests in DROPS_TABLE.items():
        line = {"ids": [ids[PFX + key]], "number": RATES[key], "quantity": 1}
        for qn in quests:
            src = by_name[qn]
            data = copy.deepcopy(src["data"])
            assert data["hidden"] is False, qn
            paths = []
            for o in data["content"]["objectives"]:
                if o["task"] == "win_quest":
                    ri = o.setdefault("reward_items", [])
                    assert all(ids[PFX + key] not in x["ids"] for x in ri), (qn, o["id"])
                    ri.append(dict(line))
                    paths.append(f"content.objectives[{o['id']}].reward_items += {SHARDS_BY_KEY[key]} {RATES[key]}%")
            assert paths, qn
            diff[qn] = paths
            out.append({"entity": "quest", "slot": "edit", "targetId": src["targetId"],
                        "name": f"{qn}: {SHARDS_BY_KEY[key]} {RATES[key]}% per clear", "data": data})
    assert len(out) == 11
    used = set(re.findall(r'"@img:([^"]+)"', json.dumps(out)))
    files, refs = {}, set()
    for pk in packs.values():  # the source manifests' own image packs, restricted to the images re-sent here
        for name in used & set((pk or {}).get("files", {})):
            files[name] = pk["files"][name]
            refs.add(pk["ref"])
    assert set(files) == used and len(refs) <= 1, (used - set(files), refs)
    extra = {"dedupNames": True, "_diff": diff}
    if files:
        extra.update({"imgSizes": {k: v["bytes"] for k, v in files.items()},
                      "imagePack": {"ref": refs.pop(), "files": files}})
    write(DROPS, "skyglass_uber_shard_drops", (
        f"push/{DROPS} (after push/{UNHIDE}; shard ids from {os.path.basename(bundle)}, L01). The shard drops "
        "(RUL-2026-11-02-104, rates from the economy model): each quest is re-sent WHOLE from its latest committed "
        "record (push/383, 384, 385, all VERIFIED; no later edit in push/ or harvests) with one drop line added to "
        "every win_quest ending, so each clear rolls once. Nothing else changes (_diff). These are live isolated "
        "Battle Pyramids: an edit makes any open run abandon and restart (libs/questRun.ts hasQuestContentChanged), "
        "so run it when no one is mid-run (outside the Friday-Sunday event)."), out, extra)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--link", help="push/417 results bundle: write 418")
    ap.add_argument("--unhide", help="push/417 results bundle: write 419")
    ap.add_argument("--drops", help="push/417 results bundle: write 420")
    a = ap.parse_args()
    if a.link:
        return build_link(a.link)
    if a.unhide:
        return build_unhide(a.unhide)
    if a.drops:
        return build_drops(a.drops)
    return build_create()


if __name__ == "__main__":
    main()
