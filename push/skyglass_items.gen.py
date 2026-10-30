#!/usr/bin/env python3
"""Skyglass items, caches, profession chests, variant tokens and variants for push/319 (module; imported by
push/skyglass_update.gen.py, which writes the manifest).

    python3 push/skyglass_items.gen.py        # prints the item plan and checks every description against the text doc

Design of record: docs/design/SKYGLASS_LOOT_TABLES.md (sections 1-5d), docs/design/SKYGLASS_TEXT.md (section 4 item text,
section 3.2 Haul pages, section 5 variants), state/skyglass_design/chests.json (profession chest tables, RUL-2026-10-29-036
/ -058), RUL-2026-10-29-040 .. RUL-2026-10-30-061. Art: RUL-2026-10-30-059 (placeholders) and docs/design/SKYGLASS_ART_AUDIT.md
(D2: committed exports that are used now).

Every chest description is RENDERED from the cache tables built here and then compared, byte for byte, with the text doc:
a mismatch stops the generator (loot tables section 0: "descriptions are generated from the same tables the caches are
built from"). Item ids are read from the files that hold them (push/260 manifest, push/323 item captures, answers); none is
typed from memory except where noted with its source.

Not built here, reported instead:
- The Little Horror's Jar: it grants the pet with `reward_pets`, which needs the species id; the species is not built
  (SKYGLASS_PETS.md kit numbers are provisional and the ten rankConcepts are unwritten).
- Crown's Hoard: no id, left pending (skyglass_check WARN).
- The Epic charts' steeping effect (`noncombatquest`): it names the two steeping quests, which are built with the
  chart runs in a later manifest; that manifest adds the effect by edit.
"""
import glob
import hashlib
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("skyglass_text", os.path.join(ROOT, "push/skyglass_text.py"))
T = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(T)

ARCH25 = os.path.join(ROOT, "archive/spent-manifests/push-2026-10-25")
PLACEHOLDER = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # engine default (45e)

# Committed, never uploaded exports for existing records (art audit D2; RUL-2026-10-30-059 item 2). The Buried Cache
# chart's export is held back: the audit asks for its seal to be checked first (drawn when the chart was Common).
IMAGES = {
    "icon-sealed-treasury.webp": "art/skyglass_event_icons/exports/icon-sealed-treasury.webp",
    "icon-archive-chart-case.webp": "art/skyglass_event_icons/exports/icon-archive-chart-case.webp",
    "icon-unmarked-cargo.webp": "art/skyglass_event_icons/exports/icon-unmarked-cargo.webp",
}


# ---------------------------------------------------------------------------------------------------------------
# Ids
# ---------------------------------------------------------------------------------------------------------------
def _captured_items():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "harvests/inbox/tnr_results_*.json"))):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for c in d.get("captures") or []:
            x = c.get("data")
            if c.get("proc") == "item.get" and isinstance(x, dict) and x.get("name"):
                out[x["name"]] = x
    return out


CAP = _captured_items()
M260 = json.load(open(os.path.join(ARCH25, "260_skyglass_items_create.json")))
_260 = {it["srcId"]: it["data"] for it in M260["items"]}


def cid(name):
    """A live id by item name, from the push/323 captures."""
    return CAP[name]["id"]


# Records created by earlier pushes (ids from the files named; design_data.json cites the same sources).
LIVE = {
    "Skyglass Coffer": "THo7rfzP-S82_43aN8fs3",          # push/skyglass_hunts.gen.py ITEM
    "Sealed Treasury": "Ma8S90Nmbi0Xvm4u4FzJh",          # push/skyglass_hunts.gen.py ITEM
    "Archive Chart Case": "B48dTRsoLJGKBWIUbeUoG",       # push/skyglass_hunts.gen.py ITEM
    "Medicine Inro": "ixEKlJ0MmDrX7JoMNJVhi",            # push/skyglass_hunts.gen.py ITEM
    "Sage's Strongbox": "h-d58UCSuHN8EZKbLjT5R",         # push/skyglass_hunts.gen.py ITEM
    "Elemental Tool Pouch": "D0gtI5dOgj2dFO4VexsLJ",     # push/elemental_pouch.gen.py
    "Unmarked Cargo": "KzITKJ5BUQRz5QuYWw-0B",           # push/skyglass_art_swaps.gen.py
    "Lastlight Lantern": "jCJv4N3JSiihuqnK0jJ7t",        # push/crownhold.gen.py ITEM
    "Chart of the Buried Cache": "nbLC37UzBamthKXvZsgQB",          # push/skyglass_update.gen.py
    "Chart of the Drowned Foundry": "pY-0O5Gs2n89pf0kYb5J2",       # push/skyglass_hunts.gen.py ITEM
    "Chart of the Quarantined Archive": "cRZT41zm5vhPTQwwn8vtv",   # push/skyglass_hunts.gen.py ITEM
    "Chart of the Captain's Watch": "aHFNuo5RkKpDcaOBLIKiu",       # push/skyglass_hunts.gen.py ITEM
    "Fragment of the Skyglass Crown": "ayiRmSjWs05lMPyL3G-1d",     # push/crownhold.gen.py
    "Elemental Kunai": "dY00WA51Mr7-uS6zbcS3r",          # push/elemental_pouch.gen.py
}
# The Coffer's own contents, read from its push/260 create.
_coffer_tiers = _260["skyglass_coffer"]["effects"][0]["weightedCache"]["tiers"]
LIVE["Skyglass Filament"] = _coffer_tiers[0]["entries"][0]["items"][0]["itemId"]
LIVE["Skyglass Serum"] = _coffer_tiers[1]["entries"][0]["items"][0]["itemId"]
LIVE["Skyglass Katana"] = _coffer_tiers[3]["entries"][0]["items"][0]["itemId"]
assert LIVE["Skyglass Serum"] == cid("Skyglass Serum")
assert _coffer_tiers[2]["entries"][0]["items"][0]["itemId"] == LIVE["Fragment of the Skyglass Crown"]

PROF = {  # the eight profession chests (answers/names_item.json; design_data.json profession_chests)
    "H:COMMON": "Common Hunter's Chest", "H:RARE": "Rare Hunter's Chest", "H:EPIC": "Epic Hunter's Chest",
    "H:LEGENDARY": "Legendary Hunter's Chest", "G:COMMON": "Common Gatherer's Chest", "G:RARE": "Rare Gatherer's Chest",
    "G:EPIC": "Epic Gatherer's Chest", "G:LEGENDARY": "Legendary Gatherer's Chest",
}

# New records created in this manifest: srcId per name (refs resolve inside the job).
NEW = {
    "Tide Chart": "tide_chart", "Watch Roster": "watch_roster", "Reliquary Seal": "reliquary_seal",
    "The Last Heading": "last_heading", "Rotted Reliquary Seal": "rotted_reliquary_seal",
    "The Rotted Heading": "rotted_heading", "Core Rot": "core_rot", "Galley Stores": "galley_stores",
    "Skyglass Token": "skyglass_token",
    "Ledger Page: The Trophy Hold": "page_trophy", "Ledger Page: The Bone Store": "page_bone",
    "Ledger Page: The Snare Room": "page_snare", "Stores Manifest: The Overgrown Stores": "page_overgrown",
    "Stores Manifest: The Ore Vault": "page_vault", "Stores Manifest: The Bloom Cellar": "page_bloom",
    "Captain's Command Fan": "vt_captain", "Rot-Bloom Reaper": "vt_core_horror", "Warden's Forge-Fists": "vt_warden",
    "Wayfinder's Heading": "vt_wayfinder", "The First Blade": "vt_first_blade", "Sealwright's Seal": "vt_sealwright",
    "Crownbreaker": "vt_crownbreaker",
}


PFX = "sg329_"  # srcIds are unique across every Forge job (the idmap is retained between jobs)
NEW = {k: PFX + v for k, v in NEW.items()}


def ref(name):
    """The id (or same-job @item ref) of an item by name."""
    if name in NEW:
        return "@item:" + NEW[name]
    if name in LIVE:
        return LIVE[name]
    return cid(name)


NAMES = {}  # id/ref -> name, for rendering


def _name_of(i):
    if i in NAMES:
        return NAMES[i]
    for n, v in list(LIVE.items()):
        if v == i:
            return n
    for n, s in NEW.items():
        if "@item:" + s == i:
            return n
    for n, x in CAP.items():
        if x["id"] == i:
            return n
    raise KeyError(i)


# ---------------------------------------------------------------------------------------------------------------
# Effects and descriptions
# ---------------------------------------------------------------------------------------------------------------
_EFF = {k: v for k, v in _260["skyglass_coffer"]["effects"][0].items() if k not in ("rewardMode", "weightedCache")}
COLOUR = {"Common": "#9ca3af", "Rare": "#3b82f6", "Epic": "#a855f7", "Legendary": "#f59e0b", "Forbidden": "#ef4444"}


def fixed(desc, items=(), money=0, pet_exp=0):
    e = dict(_EFF)
    e.update({"description": desc, "reward_items": [{"ids": [ref(n)], "number": 100, "quantity": q} for n, q in items],
              "reward_money": money})
    if pet_exp:
        e["reward_pet_experience"] = pet_exp
    return e


def cache(display, desc, tiers, rolls=((1, 10000),)):
    """tiers: [(name, basis points, [[(item name, qty), ...] per entry])]."""
    e = dict(_EFF)
    e.update({"description": desc, "rewardMode": "weightedCache", "weightedCache": {
        "version": 1, "displayName": display,
        "rolls": [{"count": c, "probability": p} for c, p in rolls],
        "tiers": [{"name": n, "probability": p,
                   "entries": [{"items": [{"itemId": ref(i), "quantity": q} for i, q in ent]} for ent in ents]}
                  for n, p, ents in tiers]}})
    assert sum(p for _, p, _ in tiers) == 10000 and sum(p for _, p in rolls) == 10000, display
    return e


def _qty(n, q):
    return f"{n} ×{q}" if q > 1 else n


def _pct(p):
    return str(int(p / 100 + 0.5)) if (p * 10) % 1000 != 500 else str(int(p // 100) + 1)


def tier_line(name, p, ents):
    parts = [" + ".join(_qty(n, q) for n, q in ent) for ent in ents]
    seen = []
    for x in parts:  # cache order; the text never repeats an entry (round-robin keeps the first three distinct)
        seen.append(x)
    more = len(seen) > 3
    body = " <i>or</i> ".join(seen[:3]) + (", and more" if more else "")
    return f'<span style="color:{COLOUR[name]}"><b>{name} {_pct(p)}%</b></span> · {body}'


def render(story, tiers, rolls=((1, 10000),), always=None, head=None):
    out = [f"<i>{story}</i>", ""]
    if always:
        out.append("<b>Always:</b> " + always)
    counts = sorted({c for c, p in rolls if p})
    if len(counts) > 1:
        out.append(f"<i>{counts[0]}–{counts[-1]} rolls.</i>")
    out.append(head or "<b>Each roll:</b>")
    out += [tier_line(n, p, e) for n, p, e in tiers if p]
    return "<br>".join(out).replace("</i><br><br>", "</i><br><br>", 1)


def story_of(target):
    """The italic story line that opens a text-doc item description."""
    t = T.block(target)
    assert t.startswith("<i>"), target
    return t[3:t.index("</i>")]


def checked(target, rendered):
    want = T.block(target)
    if rendered != want:
        import difflib
        raise SystemExit(f"{target}: rendered description differs from SKYGLASS_TEXT.md\n" + "\n".join(
            difflib.unified_diff(want.split("<br>"), rendered.split("<br>"), "text doc", "rendered", lineterm="")))
    return rendered


# ---------------------------------------------------------------------------------------------------------------
# Cache tables (loot tables sections 2, 3, 3a)
# ---------------------------------------------------------------------------------------------------------------
def one(*names_qty):
    return [[(n, q)] for n, q in names_qty]


COFFER = [("Common", 6900, one(("Skyglass Filament", 2))), ("Rare", 2400, one(("Skyglass Serum", 3))),
          ("Epic", 500, one(("Fragment of the Skyglass Crown", 1))), ("Legendary", 200, one(("Skyglass Katana", 1)))]
TREASURY = [("Common", 4500, one(("Imperial Gold", 5))), ("Rare", 3500, one(("Rare Jewels", 10))),
            ("Epic", 1500, one(("Imperial Gold", 15))), ("Legendary", 500, one(("Unobtanium", 5)))]
TREASURY_ROLLS = ((3, 6000), (4, 3000), (6, 1000))
CHART_CASE = [("Common", 4500, one(("Chart of the Drowned Foundry", 1))),
              ("Rare", 2500, one(("Chart of the Quarantined Archive", 1))),
              ("Epic", 2000, one(("Chart of the Captain's Watch", 1))),
              ("Legendary", 700, one(("Reliquary Seal", 1), ("The Last Heading", 1))),
              ("Forbidden", 300, one(("Lastlight Lantern", 1)))]
INRO = [("Common", 7000, one(("Field Tonic", 10), ("Chakra Pill", 10), ("Stamina Pill", 10))),
        ("Rare", 2200, one(("Small Health Pill", 10), ("Dr. Kim's Miracle Potion", 10), ("Panacea", 10))),
        ("Epic", 700, one(("Chakra Pill II", 10), ("Stamina Pill II", 10))),
        ("Legendary", 100, one(("Pill Pack", 5)))]
STRONGBOX = [("Common", 6500, one(("Dr. Kim Disaster Potion", 20), ("Chakra Disrupting Needles", 20))),
             ("Epic", 2600, one(("Infernum", 10), ("Bashōsen", 10), ("Dr. Kim's Poison Potion", 10))),
             ("Legendary", 800, one(("Solider Pill", 2), ("Enemy Pill", 2), ("Mona's Mermaid Song", 2))),
             ("Forbidden", 100, one(("Forbidden Jutsu Scroll: Nexus", 1), ("Forbidden Jutsu Scroll: Rebirth", 1)))]
POUCH = [("Common", 7000, one(("Elemental Kunai", 10), ("Venom Cask", 10))),
         ("Rare", 2500, one(("Elemental Kunai", 20), ("Elite Smoke Bomb", 10), ("Paper Bombs", 10))),
         ("Epic", 500, one(("Elemental Kunai", 30), ("Senbon Needles", 10), ("Saki", 10)))]
CARGO = [("Common", 4000, one(("Medicine Inro", 1), ("Elemental Tool Pouch", 1))),
         ("Rare", 3500, one(("Sage's Strongbox", 1), ("Galley Stores", 1))),
         ("Epic", 1800, one(("Skyglass Coffer", 1), ("Archive Chart Case", 1))),
         ("Legendary", 700, one(("Sealed Treasury", 1), ("Skyglass Token", 1)))]


def _strongbox_text():
    return render(story_of("item:Sage's Strongbox.description"), STRONGBOX)


# ---------------------------------------------------------------------------------------------------------------
# Records
# ---------------------------------------------------------------------------------------------------------------
_BASE_OTHER = {k: v for k, v in _260["chart_foundry"].items() if k not in ("effects",)}
_BASE_CONS = {k: v for k, v in _260["skyglass_coffer"].items() if k not in ("effects",)}


def create(src, name, desc, rarity, kind, traded, effects=(), battle="Treasure chest", phase=1):
    base = dict(_BASE_CONS if kind == "CONSUMABLE" else _BASE_OTHER)
    base.update({"name": name, "description": desc, "rarity": rarity, "itemType": kind, "image": PLACEHOLDER,
                 "canBeTraded": traded, "effects": list(effects), "battleDescription": battle, "hidden": True,
                 "target": "SELF", "method": "SINGLE", "preventBattleUsage": True,
                 "destroyOnUse": kind == "CONSUMABLE"})
    NAMES["@item:" + src] = name
    return {"entity": "item", "slot": "create", "srcId": src, "phase": phase, "name": name, "data": base}


def edit(name, data, label=None, phase=1):
    return {"entity": "item", "slot": "edit", "targetId": LIVE.get(name) or cid(name), "phase": phase,
            "name": label or name, "data": data}


def _token_effect(variant=None):
    return {"type": "unlockitemvariant", "variantId": variant,
            "description": "Unlocks a token-locked item variant when used on an item", "power": 1, "powerPerLevel": 0,
            "calculation": "static", "direction": "offence", "staticAssetPath": "", "staticAnimation": "",
            "appearAnimation": "", "disappearAnimation": "", "appearSfx": "", "disappearSfx": "", "target": "SELF"}


def chart_items():
    out = []
    for src, name, rar, kind in (("tide_chart", "Tide Chart", "COMMON", "OTHER"),
                                 ("watch_roster", "Watch Roster", "COMMON", "OTHER"),
                                 # The Epic charts are used from the inventory to steep (RUL-2026-10-29-055): consumable
                                 # from the start; the noncombatquest effect is added with the steeping quests.
                                 ("reliquary_seal", "Reliquary Seal", "EPIC", "CONSUMABLE"),
                                 ("last_heading", "The Last Heading", "EPIC", "CONSUMABLE"),
                                 ("rotted_reliquary_seal", "Rotted Reliquary Seal", "LEGENDARY", "OTHER"),
                                 ("rotted_heading", "The Rotted Heading", "LEGENDARY", "OTHER")):
        out.append(create(NEW[name], name, T.block(f"item:{name}.description"), rar, kind, True))
    # Existing charts: the text doc's descriptions; rarity by tier (RUL-2026-10-29-058: the four former hunt charts are Rare).
    for name in ("Chart of the Buried Cache", "Chart of the Drowned Foundry", "Chart of the Quarantined Archive",
                 "Chart of the Captain's Watch"):
        out.append(edit(name, {"description": T.block(f"item:{name}.description"), "rarity": "RARE"},
                        f"{name}: text, Rare"))
    out.append(edit("Lastlight Lantern", {"description": T.block("item:Lastlight Lantern.description"),
                                          "rarity": "LEGENDARY"}, "Lastlight Lantern: text, Legendary"))
    return out


def haul_pages():
    rules = T.block("item:<chart>.description") if False else None  # the rules block has no item heading
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith("**Rules block**"))
    j = next(j for j in range(i, len(L)) if L[j].startswith("```")) + 1
    rules = L[j]
    out = []
    for name, story in T.table("### 3.2 Page items"):
        page = name.split(": ", 1)[1]
        chests = "Hunter's" if name.startswith("Ledger") else "Gatherer's"
        desc = story + rules.replace("<page>", page).replace("<chests>", chests)
        out.append(create(NEW[name], name, desc, "LEGENDARY", "OTHER", True))
    assert len(out) == 6
    return out


def pet_and_rot():
    # Tradeability of Core Rot and Galley Stores is not ruled: placeholder untradeable (reversible), reported.
    return [
        create(NEW["Core Rot"], "Core Rot", T.block("item:Core Rot.description"), "RARE", "OTHER", False),
        create(NEW["Galley Stores"], "Galley Stores", T.block("item:Galley Stores.description"), "RARE", "CONSUMABLE", False,
               [fixed("Galley Stores: 20,000 pet experience to the active pet", pet_exp=20000)]),
    ]


VT = T.table("**Boss variant tokens.**")            # token item, base, story
SKINS = T.table("### 5.1 The 12 Skyglass variants")  # base (type), name, description, art line
BOSS = T.table("### 5.2 The 7 boss variants")         # base (type), name, description, art line
UNTRADEABLE = {"Captain's Command Fan", "Rot-Bloom Reaper", "Crownbreaker"}  # loot tables 5d
VT_TEMPLATE = T.block("**Boss variant tokens.**") if False else None


def tokens():
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith("**Boss variant tokens.**"))
    j = next(j for j in range(i, len(L)) if L[j].startswith("```")) + 1
    tmpl = L[j]
    out = [create(NEW["Skyglass Token"], "Skyglass Token", T.block("item:Skyglass Token.description"), "LEGENDARY",
                  "CONSUMABLE", True, [_token_effect()], battle="Variant token")]
    for name, base, story in VT:
        desc = tmpl.replace("<story line>", story).replace("<Variant>", name).replace("<Base>", base)
        out.append(create(NEW[name], name, desc, "LEGENDARY", "CONSUMABLE", name not in UNTRADEABLE,
                          [_token_effect()], battle="Variant token"))
    assert len(out) == 8
    return out


def caches():
    out = []
    out.append(edit("Skyglass Coffer", {"rarity": "EPIC", "target": "SELF", "effects": [
        cache("Skyglass Coffer", "Skyglass Coffer: one roll of Skyglass salvage", COFFER)],
        "description": checked("item:Skyglass Coffer.description", render(story_of("item:Skyglass Coffer.description"), COFFER))},
        "Skyglass Coffer: text, Epic"))
    out.append(edit("Sealed Treasury", {"rarity": "LEGENDARY", "target": "SELF", "image": "@img:icon-sealed-treasury.webp",
        "effects": [fixed("Sealed Treasury: 150,000 ryo every opening", money=150000),
                    cache("Sealed Treasury", "Sealed Treasury: 3-6 rolls of valuables", TREASURY, TREASURY_ROLLS)],
        "description": checked("item:Sealed Treasury.description",
                               render(story_of("item:Sealed Treasury.description"), TREASURY, TREASURY_ROLLS, "150,000 ryo"))},
        "Sealed Treasury: 150,000 ryo + 3-6 rolls; text; art"))
    out.append(edit("Archive Chart Case", {"rarity": "EPIC", "target": "SELF", "image": "@img:icon-archive-chart-case.webp",
        "effects": [cache("Archive Chart Case", "Archive Chart Case: one chart", CHART_CASE)],
        "description": checked("item:Archive Chart Case.description", render(story_of("item:Archive Chart Case.description"), CHART_CASE))},
        "Archive Chart Case: 45/25/20/7/3 (RUL-2026-10-29-040); text; art"))
    out.append(edit("Medicine Inro", {"rarity": "COMMON", "target": "SELF", "effects": [
        cache("Medicine Inro", "Medicine Inro: two rolls of pills and potions", INRO, ((2, 10000),))],
        "description": checked("item:Medicine Inro.description", render(story_of("item:Medicine Inro.description"), INRO))},
        "Medicine Inro: two rolls (section 3a); text"))
    out.append(edit("Sage's Strongbox", {"rarity": "RARE", "target": "SELF", "effects": [
        cache("Sage's Strongbox", "Sage's Strongbox: one roll of enemy alchemy", STRONGBOX)],
        "description": checked("item:Sage's Strongbox.description", _strongbox_text())},
        "Sage's Strongbox: section 3a table, Forbidden tier; text; Rare"))
    out.append(edit("Elemental Tool Pouch", {"name": "Elemental Tool Pouch", "rarity": "COMMON", "target": "SELF", "effects": [
        fixed("Elemental Kunai x10, every opening", items=[("Elemental Kunai", 10)]),
        cache("Elemental Tool Pouch", "Elemental Tool Pouch: one roll of tools", POUCH)],
        "description": checked("item:Elemental Tool Pouch.description",
                               render(story_of("item:Elemental Tool Pouch.description"), POUCH, always="Elemental Kunai ×10"))},
        "Elemental Tool Pouch"))
    out.append(edit("Unmarked Cargo", {"rarity": "EPIC", "target": "SELF", "canBeTraded": False,
        "image": "@img:icon-unmarked-cargo.webp", "effects": [cache("Unmarked Cargo", "Unmarked Cargo: one roll of the ship's stores", CARGO)],
        "description": checked("item:Unmarked Cargo.description", render(story_of("item:Unmarked Cargo.description"), CARGO))},
        "Unmarked Cargo: 40/35/18/7 (section 2); text; art"))
    return out


def _round_robin(entries):
    """Distinct entries, most frequent first (stable), interleaved so each copy keeps its weight and the first entries
    are distinct (the text lists the first three)."""
    keys, count = [], {}
    for e in entries:
        k = json.dumps(e)
        if k not in count:
            keys.append(k); count[k] = 0
        count[k] += 1
    keys.sort(key=lambda k: -count[k])
    out, left = [], dict(count)
    while any(left.values()):
        for k in keys:
            if left[k]:
                out.append(json.loads(k)); left[k] -= 1
    return out


def profession_chests():
    tables = json.load(open(os.path.join(ROOT, "state/skyglass_design/chests.json")))
    out = []
    for key, name in PROF.items():
        tiers = [(n, p, [[(i, q) for i, q in ent] for ent in _round_robin(ents)]) for n, p, ents in tables[key]]
        rolls = ((3, 6000), (4, 3000), (6, 1000))
        story = story_of(f"item:{name}.description")
        desc = checked(f"item:{name}.description", render(story, tiers, rolls))
        rar = key.split(":")[1]
        out.append({"entity": "item", "slot": "edit", "targetId": cid(name), "phase": 1,
                    "name": f"{name}: tiers Common/Rare/Epic/Legendary (RUL-2026-10-29-058), text",
                    "data": {"rarity": rar, "target": "SELF", "description": desc,
                             "effects": [cache(name, f"{name}: 3-6 rolls of materials", tiers, rolls)]}})
    return out


# ---------------------------------------------------------------------------------------------------------------
# Variants (loot tables 5d; text doc section 5; forge itemVariant)
# ---------------------------------------------------------------------------------------------------------------
# Live VARIANT_TOKEN variants already hold order 1 on these bases (push/326 pass-2 bundle tnr_results_1793364924712.json).
TAKEN_ORDERS = {}
for _f in glob.glob(os.path.join(ROOT, "harvests/inbox/tnr_results_1793364924712.json")):
    for _c in json.load(open(_f)).get("captures") or []:
        if _c.get("proc") == "item.getItemVariants":
            for _v in _c.get("data") or []:
                TAKEN_ORDERS.setdefault(_v["itemId"], set()).add(_v["order"])
BASE_IDS = {"Whispering Dawnblade": "mqCCZGSfXUNL02B4H6C9R"}  # RUL-2026-10-30-060 item 8 (verified against the capture below)


def base_id(label):
    name = label.split(" (")[0]
    i = cid(name)
    assert BASE_IDS.get(name, i) == i, name
    assert CAP[name]["itemType"] == "WEAPON", name
    return i


def variants():
    out, binds, used = [], [], {}

    def order(item):
        taken = TAKEN_ORDERS.get(item, set()) | used.setdefault(item, set())
        o = next(k for k in range(1, 8) if k not in taken)
        used[item].add(o)
        return o

    for base, name, desc, _art in SKINS:
        item = base_id(base)
        src = PFX + "var_" + name.lower().replace("'", "").replace(" ", "_").replace("-", "_")
        out.append({"entity": "itemVariant", "slot": "create", "srcId": src, "phase": 2, "name": name,
                    "data": {"itemId": item, "name": name, "image": PLACEHOLDER, "requiredItemId": "@item:" + NEW["Skyglass Token"],
                             "costType": "VARIANT_TOKEN", "cost": 1, "order": order(item), "description": desc,
                             "hidden": True}})
    tok = {r[0]: r for r in VT}
    for base, name, desc, _art in BOSS:
        item = base_id(base)
        assert tok[name][1] == base.split(" (")[0], name
        src = NEW[name].replace(PFX, PFX + "var_")
        out.append({"entity": "itemVariant", "slot": "create", "srcId": src, "phase": 2, "name": name,
                    "data": {"itemId": item, "name": name, "image": PLACEHOLDER, "requiredItemId": "@item:" + NEW[name],
                             "costType": "VARIANT_TOKEN", "cost": 1, "order": order(item), "description": desc,
                             "hidden": True}})
        # Step 3 of a 1:1 token (pipeline 2.10): bind the token to its variant once the variant exists. The edit needs
        # literal ids (L01), so it is built from this manifest's results bundle (bind_edits).
        binds.append((NEW[name], src, name))
    assert len(out) == 19 and len(binds) == 7
    return out, binds


def bind_edits(idmap):
    """The seven token edits of step 3, with literal ids from the step-2 manifest's results (bundle idmap)."""
    out = []
    for token_src, var_src, name in variants()[1]:
        tid, vid = idmap.get(token_src), idmap.get(var_src)
        if not tid or not vid:
            raise SystemExit(f"{name}: {token_src} or {var_src} missing from the results idmap")
        out.append({"entity": "item", "slot": "edit", "targetId": tid, "name": name,
                    "data": {"target": "SELF", "destroyOnUse": True, "preventBattleUsage": True,
                             "effects": [_token_effect(vid)]}})
    return out


def all_items():
    v, b = variants()
    return {"items": chart_items() + haul_pages() + pet_and_rot() + tokens() + caches() + profession_chests(),
            "variants": v, "binds": b}


def image_pack(items):
    files, used = {}, json.dumps(items)
    for name, path in IMAGES.items():
        if "@img:" + name in used:
            b = open(os.path.join(ROOT, path), "rb").read()
            files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return files


def placeholders(entries):
    """Every record in `entries` that carries the engine-default placeholder image (RUL-2026-10-30-059 item 3)."""
    return [f"{e['entity']} {e.get('srcId') or e.get('targetId')}: {e['data'].get('name', e['name'])}"
            for e in entries if e["data"].get("image") == PLACEHOLDER]


if __name__ == "__main__":
    r = all_items()
    for k, v in r.items():
        print(k, len(v))
        for e in v:
            print("  ", e["entity"], e["slot"], e.get("srcId") or e.get("targetId"), "|", e["name"])
