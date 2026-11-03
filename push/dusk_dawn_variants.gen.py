#!/usr/bin/env python3
"""Nightfall and Dawnbringer: two crafted sidegrade swords that host 12 token-locked skins (push/441, then push/442).

    python3 push/dusk_dawn_variants.gen.py                        # writes push/441_dusk_dawn_variants.json
    python3 push/dusk_dawn_variants.gen.py --binds <results.json> # writes push/442_dusk_dawn_token_binds.json

Design (director, 2026-11-03 chat):
- Night's Testament and Aetherion already carry variants, so their own slots stay free. Two NEW swords host the skins:
  Nightfall (stat clone of Night's Testament) and Dawnbringer (stat clone of Aetherion). Crafted legendary bases, not
  item-shop ones.
- Sidegrade: each new sword is crafted from its base sword + 10 boss shards (Umbral Shard / Aurora Shard). Same stats,
  so no balance change. The boss drop tables are NOT built here: the shards and tokens are created hidden and wired
  into the boss loot by a later manifest.
- No bloodline gate: every skin is open to any owner of the host sword. One tradeable 1:1 token per skin.
- Nightfall: 7 skins (full, MAX_ITEM_VARIANTS = 7). Dawnbringer: 5 skins, 2 slots kept open.

The 1:1 token is three steps (pipeline 2.10): token create with `variantId: null` (here), variant create with
`requiredItemId: @item:<token>` (here, phase 2), then a token edit binding `variantId` (push/442, built from 441's
results because an edit needs a literal targetId). Until 442 lands the tokens are hidden, so no player holds one.

Base records are read from committed `item.get` captures, never typed. Art: art/dusk_dawn_variants (whitekey.py).
"""
import glob
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFX = "dd441_"
PLACEHOLDER = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # engine default (45e)
ART = "art/dusk_dawn_variants/exports/"
SHARDS_PER_SWORD = 10  # director default, 2026-11-03 ("Go" on the stated defaults)

FIELDS = set(json.load(open(os.path.join(ROOT, "skills/building-tnr-content/data/45d_DATA_entity_schemas.json")))
             ["entities"]["item"]["fields"])


def _captured(names):
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "harvests/inbox/tnr_results_*.json"))):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        for c in d.get("captures") or []:
            x = c.get("data")
            if c.get("proc") == "item.get" and isinstance(x, dict) and x.get("name") in names:
                out[x["name"]] = x  # newest capture wins (files sort by timestamp)
    missing = set(names) - set(out)
    assert not missing, f"no item.get capture for {missing}"
    return out


BASES = _captured({"Night's Testament", "Aetherion"})
assert BASES["Night's Testament"]["id"] == "osJq3k77YPGoFWgof12FQ"
assert BASES["Aetherion"]["id"] == "PhP5ZEF5iVa97jcumJ15c"

# sword: (srcId, base, shard name, shard srcId, description, skins)
# skin: (name, art slug, variant description, token story line)
SWORDS = {
    "Nightfall": ("nightfall", "Night's Testament", "Umbral Shard", "umbral_shard",
                  "<i>Night's Testament, reforged around a core of boss-torn shadow.</i><br><br>Fights exactly as Night's "
                  "Testament does. What it gains is a wardrobe: seven Nightfall skins, each unlocked by its own token.<br>"
                  "<b>Crafted from:</b> Night's Testament and 10 Umbral Shards. The Night's Testament is consumed, even if "
                  "it is equipped, and its imbuement goes with it.",
                  [("Duskshroud", "duskshroud", "Nightfall wrapped in living dusk. Faint runes burn violet beneath the smoke.",
                    "Smoke that never quite settles."),
                   ("Thundermourn", "thundermourn", "Nightfall split by violet lightning that never stops crawling along the edge.",
                    "A storm that grieves as it strikes."),
                   ("Cinderfang", "cinderfang", "Nightfall cracked with molten seams, shedding embers with every swing.",
                    "Embers that refuse to cool."),
                   ("Gravewhisper", "gravewhisper", "Nightfall grown with bone and spine, its runes glowing a sickly green.",
                    "Bones that still remember their names."),
                   ("Violet Vespers", "violet-vespers", "Nightfall set in gilded filigree and amethyst, trailing violet flame.",
                    "Evening prayers in a royal court."),
                   ("Rimecleaver", "rimecleaver", "Nightfall sheathed in hoarfrost, icicles hanging from its spine.",
                    "Winter that bites back."),
                   ("Deepcurrent", "deepcurrent", "Nightfall etched with breaking waves and finished with a pearl shell pommel.",
                    "The pull of the deep tide.")]),
    "Dawnbringer": ("dawnbringer", "Aetherion", "Aurora Shard", "aurora_shard",
                    "<i>Aetherion, reforged in the first light after a long night.</i><br><br>Fights exactly as Aetherion "
                    "does. What it gains is a wardrobe: Dawnbringer skins, each unlocked by its own token.<br>"
                    "<b>Crafted from:</b> Aetherion and 10 Aurora Shards. The Aetherion is consumed, even if it is "
                    "equipped, and its imbuement goes with it.",
                    [("Solstice", "solstice", "Dawnbringer forged in white gold, crowned with a blazing sun guard.",
                      "The longest day of the year."),
                     ("Starward", "starward", "Dawnbringer in moonlit silver, its fuller strewn with stars and crescents.",
                      "A path drawn in constellations."),
                     ("Prismheart", "prismheart", "Dawnbringer of faceted crystal that splits the light into every colour.",
                      "Light broken into every colour."),
                     ("Scarab's Oath", "scarabs-oath", "Dawnbringer in desert bronze, a winged scarab spread across its guard.",
                      "An oath sworn under the desert sun."),
                     ("Verdant Vow", "verdant-vow", "Dawnbringer of jade green steel, bound in living vines.",
                      "A promise the forest keeps.")]),
}


def _src(*parts):
    return PFX + "_".join(p.lower().replace("'", "").replace(" ", "_").replace("-", "_") for p in parts)


def _plain(rarity, kind, name, desc, image, traded=True, stack=100):
    """A non-weapon item, full field set (the push/90 material and push/329 consumable creates)."""
    return {"name": name, "description": desc, "effects": [], "itemType": kind, "rarity": rarity, "slot": "NONE",
            "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE", "cost": 1, "repsCost": 0,
            "seichiSilverCost": 0, "stackSize": stack, "image": image, "destroyOnUse": kind == "CONSUMABLE", "range": 0,
            "chakraCost": 0, "staminaCost": 0, "healthCost": 0, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
            "healthCostReducePerLvl": 0, "actionCostPerc": 60, "battleDescription": name, "canStack": True,
            "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": False, "hidden": True,
            "maxEquips": 1, "preventBattleUsage": True, "requiredLevel": 1, "xpToLevel": 1000, "parentItemId": None,
            "requiredStrength": None, "requiredSpeed": None, "requiredIntelligence": None, "requiredWillpower": None,
            "canBeCrafted": False, "canBeImbued": False, "canBeHunted": False, "canBeGathered": False,
            "canBeTraded": traded, "isFarmSeed": False, "farmGrowTimeSeconds": 0, "farmYieldItemId": None,
            "farmMinLevel": 1, "farmPlantExperience": 0, "farmHarvestExperience": 0, "farmSellValue": 0,
            "farmExtractSeedItemId": None, "farmExtractSeedCount": 0, "isFarmFertilizer": False,
            "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0, "craftingExperience": 0,
            "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH", "craftingRequirements": []}


def _token_effect(variant=None):
    return {"type": "unlockitemvariant", "variantId": variant,
            "description": "Unlocks a token-locked item variant when used on an item", "power": 1, "powerPerLevel": 0,
            "calculation": "static", "direction": "offence", "staticAssetPath": "", "staticAnimation": "",
            "appearAnimation": "", "disappearAnimation": "", "appearSfx": "", "disappearSfx": "", "target": "SELF"}


def _clone(base, name, desc, shard_src):
    b = BASES[base]
    d = {k: v for k, v in b.items() if k in FIELDS}
    d.update({"name": name, "description": desc, "hidden": True, "inShop": False, "isEventItem": False,
              "canBeCrafted": True, "parentItemId": None, "expireFromStoreAt": None, "bloodlineId": None,
              "craftingRequirements": [{"ids": [b["id"]], "number": 1},
                                       {"ids": ["@item:" + shard_src], "number": SHARDS_PER_SWORD}]})
    # The clone must fight exactly like its base: every combat field is copied, never retyped.
    for k in ("effects", "cooldown", "actionCostPerc", "chakraCost", "staminaCost", "range", "target", "method",
              "weaponType", "rarity", "requiredLevel", "maxImbueNumber", "canBeImbued", "battleDescription", "image"):
        assert d[k] == b[k], k
    return d


def build():
    items = []
    for sword, (s_src, base, shard, sh_src, desc, skins) in SWORDS.items():
        sh_src = PFX + sh_src
        items.append({"entity": "item", "slot": "create", "srcId": sh_src, "phase": 1, "name": shard,
                      "data": _plain("EPIC", "MATERIAL", shard,
                                     f"A shard torn from the boss's core. {SHARDS_PER_SWORD} of them and a {base} "
                                     f"craft <b>{sword}</b>.", PLACEHOLDER)})
        items.append({"entity": "item", "slot": "create", "srcId": PFX + s_src, "phase": 2, "name": sword,
                      "data": _clone(base, sword, desc, sh_src)})
        assert len(skins) <= 7
        for order, (name, slug, vdesc, story) in enumerate(skins, 1):
            t_src, v_src = _src("tok", slug), _src("var", slug)
            img = f"@img:icon-variant-{slug}.webp"
            tok = _plain("LEGENDARY", "CONSUMABLE", f"{name} Token",
                         f"<i>{story}</i><br><br>Use it on <b>{sword}</b> to unlock the <b>{name}</b> skin. "
                         f"Spent on use.", img)
            tok.update({"effects": [_token_effect()], "battleDescription": "Variant token"})
            items.append({"entity": "item", "slot": "create", "srcId": t_src, "phase": 1, "name": f"{name} Token",
                          "data": tok})
            items.append({"entity": "itemVariant", "slot": "create", "srcId": v_src, "phase": 3, "name": name,
                          "data": {"itemId": "@item:" + PFX + s_src, "name": name, "image": img,
                                   "requiredItemId": "@item:" + t_src, "costType": "VARIANT_TOKEN", "cost": 1,
                                   "order": order, "description": vdesc, "hidden": True}})
    return items


def binds(results):
    idmap = json.load(open(results))["idmap"]
    out = []
    for sword, (_, _, _, _, _, skins) in SWORDS.items():
        for name, slug, _, _ in skins:
            t_src, v_src = _src("tok", slug), _src("var", slug)
            if not idmap.get(t_src) or not idmap.get(v_src):
                raise SystemExit(f"{name}: {t_src} or {v_src} missing from the results idmap")
            out.append({"entity": "item", "slot": "edit", "phase": 1, "targetId": idmap[t_src],
                        "name": f"{name} Token: bind to its variant",
                        "data": {"target": "SELF", "destroyOnUse": True, "preventBattleUsage": True,
                                 "effects": [_token_effect("@variant:" + v_src)]}})
    return out


def pack(items):
    files, used = {}, json.dumps(items)
    for f in sorted(os.listdir(os.path.join(ROOT, ART))):
        if "@img:" + f in used:
            path = ART + f
            b = open(os.path.join(ROOT, path), "rb").read()
            files[f] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return files


def pack_ref(files):
    paths = [f["path"] for f in files.values()]
    ref = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", *paths], text=True).strip()
    assert ref, "commit the exports before generating: the image pack ref is the commit that holds them"
    for f in files.values():
        b = subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{f['path']}"])
        assert hashlib.sha256(b).hexdigest() == f["sha256"], f["path"]
    return ref


def write(num, slug, note, items):
    m = {"_note": note + " Generated by push/dusk_dawn_variants.gen.py; do not hand-edit.", "dedupNames": True}
    files = pack(items)
    if files:
        m["imgSizes"] = {k: v["bytes"] for k, v in files.items()}
        m["imagePack"] = {"ref": pack_ref(files), "files": files}
    m["items"] = items
    path = os.path.join(ROOT, f"push/{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items)} items")


if __name__ == "__main__":
    if "--binds" in sys.argv:
        write(442, "dusk_dawn_token_binds",
              "push/442: binds each of the 12 Nightfall/Dawnbringer tokens to its own variant (pipeline 2.10 step 3), "
              "with literal token ids from push/441's results.", binds(sys.argv[sys.argv.index("--binds") + 1]))
    else:
        write(441, "dusk_dawn_variants",
              "push/441: Nightfall (Night's Testament clone) and Dawnbringer (Aetherion clone), crafted from their base "
              "sword + 10 boss shards; 12 token-locked skins (7 + 5), one tradeable token each. Everything is created "
              "hidden; boss loot wiring and unhide come later. Run push/442 (token binds) from this run's results.",
              build())
