#!/usr/bin/env python3
"""
push/631_gobblefather_art_rewards.gen.py

Builds push/631_gobblefather_art_rewards.zip, step 3 of The Gobblefather (Thanksgiving 2026), for
browser Forge (the zip carries its own images, so Forge uploads them; the connector cannot).

    asset       11  scene backgrounds (6) and scene characters (5), HIDDEN, folder Gobblefather
    ai edit      7  avatar + avatarLight on the 623 enemies (stay hidden)
    badge        1  Family Business (badges have no hidden state: public on /manual/badge from create)
    item         2  Golden Feathered Ring (ACCESSORY, robprevent 40) and Gobblefather's Cane Token, HIDDEN
    itemVariant  1  Gobblefather's Cane on Night's Testament, token-locked (no hidden state: owners of
                    Night's Testament see "Need Gobblefather's Cane Token" from the run)
    quest edit   1  goJkx-CPJSYvJO71s6CpE: scenes on every node, rewards = rewardPackages
                    "Single Major Event" values + badge + ring + cane token (stays hidden)

Director rulings 2026-11-26 (this thread): ring = rob protection only, power 40 (Ninja Force 1's
value); cane = token reskin of Night's Testament; rewards = the preset "Single Major Event" package.
Source check (TheNinjaRPG@e1953c17, combat.ts ~4466): an equipped ACCESSORY's effects are applied
as passive battle effects; only one ACCESSORY can be equipped (libs/item.ts canEquipAdditional).

Follow-up (connector, before unhide): token edit setting unlockitemvariant.variantId to the new
variant's literal id (pipeline 2.10, 1:1 trophy step 3), so the token cannot unlock other
requiredItemId-less token variants.

Run from the repository root:
    python3 push/631_gobblefather_art_rewards.gen.py
"""
import copy
import importlib.util
import json
import os
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "art", "gobblefather")
OUT_ZIP = os.path.join(ROOT, "push", "631_gobblefather_art_rewards.zip")
OUT_JSON = os.path.join(ROOT, "push", "631_gobblefather_art_rewards.json")  # same manifest, for gates
B623 = os.path.join(ROOT, "harvests", "inbox", "tnr_results_1795631190552.json")

spec = importlib.util.spec_from_file_location("gf622", os.path.join(ROOT, "push", "622_gobblefather_core.gen.py"))
gf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gf)

P = "gf631"
QUEST_ID = "goJkx-CPJSYvJO71s6CpE"
NIGHTS_TESTAMENT = "osJq3k77YPGoFWgof12FQ"
GOAH = "j4tEoLtefH12sZwZY6MF-"  # existing live SCENE_CHARACTER "Goah"
VARIANT_ORDER = 3               # Weeping Testament 1, Nightreaver 2 (live read 2026-11-26)
PACKAGE = {                     # rewardPackages "Single Major Event" (SLBSXuj7n-YrpdbKSPITJ), live read 2026-11-26
    "reward_exp": 10000, "reward_money": 70000, "reward_tokens": 500,
    "reward_prestige": 480, "reward_clanpoints": 500,
}

BG = {k: f"gobblefather_bg_{k}.webp" for k in
      ("trade_road", "tollgate", "golden_silo", "estate", "office", "feast_hall")}
SC = {k: f"gobblefather_sc_{k}.webp" for k in ("hachiro", "tony", "vinny", "don_giblet", "gobblefather")}
AV = {"enforcer": "gobblefather_av_enforcer.webp", "collector": "gobblefather_av_corn_collector.webp",
      "accountant": "gobblefather_av_accountant.webp", "tony": "gobblefather_av_tony.webp",
      "vinny": "gobblefather_av_vinny.webp", "giblet": "gobblefather_av_don_giblet.webp",
      "gobblefather": "gobblefather_av_gobblefather.webp"}
ICON = {"badge": "gobblefather_badge_family_business.webp",
        "ring": "gobblefather_item_golden_feathered_ring.webp",
        "cane": "gobblefather_item_cane_skin.webp"}

BG_NAME = {"trade_road": "Harvest Plains Trade Road", "tollgate": "The Drumstick Tollgate",
           "golden_silo": "Golden Silo Warehouse", "estate": "The Feathered Estate",
           "office": "The Gobblefather's Office", "feast_hall": "The Grand Feast Hall"}
SC_NAME = {"hachiro": "Merchant Hachiro", "tony": "Tony Drumstick", "vinny": "Vinny Drumstick",
           "don_giblet": "Don Giblet", "gobblefather": "The Gobblefather"}

# node -> (background, [characters]); "goah" is the live asset, the rest are this job's creates.
SCENES = {
    "o1": ("trade_road", ["goah"]), "o1a": ("trade_road", ["goah"]), "o2": ("trade_road", []),
    "o3": ("trade_road", ["hachiro"]),
    # law 48: one scene character per node (the client stacks a second on the first)
    "o4": ("tollgate", ["tony"]), "o5": ("tollgate", ["tony"]),
    "o5a": ("tollgate", ["vinny"]), "b6": ("tollgate", []), "r6": ("tollgate", []),
    "o6": ("tollgate", ["vinny"]),
    "o7": ("golden_silo", []), "b8": ("golden_silo", []), "r8": ("golden_silo", []),
    "o9": ("golden_silo", ["don_giblet"]), "o9a": ("golden_silo", ["don_giblet"]),
    "o9b": ("golden_silo", ["don_giblet"]), "b10": ("golden_silo", []), "r10": ("golden_silo", []),
    "o10": ("golden_silo", ["don_giblet"]),
    "o11": ("estate", []),
    "o12": ("office", ["gobblefather"]), "o12a": ("office", ["gobblefather"]),
    "o12b": ("office", ["gobblefather"]), "b13": ("feast_hall", []),
    "o14": ("feast_hall", ["gobblefather"]),
    "o15": ("trade_road", ["goah"]), "o15a": ("trade_road", ["goah"]), "o16": ("trade_road", []),
    "win": ("feast_hall", []), "x": ("office", ["gobblefather"]),
}

DEFAULT_ITEM = {
    "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE", "cost": 1, "repsCost": 0,
    "seichiSilverCost": 0, "range": 0, "chakraCost": 0, "staminaCost": 0, "healthCost": 0,
    "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0, "healthCostReducePerLvl": 0,
    "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": True, "hidden": True,
    "maxEquips": 1, "xpToLevel": 1000, "parentItemId": None, "requiredStrength": None, "requiredSpeed": None,
    "requiredIntelligence": None, "requiredWillpower": None, "canBeCrafted": False, "canBeImbued": False,
    "canBeHunted": False, "canBeGathered": False, "canBeTraded": False, "isFarmSeed": False,
    "farmGrowTimeSeconds": 0, "farmYieldItemId": None, "farmMinLevel": 1, "farmPlantExperience": 0,
    "farmHarvestExperience": 0, "farmSellValue": 0, "farmExtractSeedItemId": None, "farmExtractSeedCount": 0,
    "isFarmFertilizer": False, "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0,
    "craftingExperience": 0, "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH",
    "expireFromStoreAt": None,
}
FX_BLANK = {"appearSfx": "", "disappearSfx": "", "appearAnimation": "", "staticAnimation": "",
            "staticAssetPath": "", "disappearAnimation": "", "powerPerLevel": 0, "direction": "offence"}


def img(name):
    return f"@img:{name}"


def assets():
    out = []
    for k, f in BG.items():
        out.append(("bg_" + k, BG_NAME[k], "SCENE_BACKGROUND", f))
    for k, f in SC.items():
        out.append(("sc_" + k, SC_NAME[k], "SCENE_CHARACTER", f))
    return [{"entity": "asset", "slot": "create", "srcId": f"{P}_{key}", "name": name, "data": {
        "name": name, "type": typ, "image": img(f), "folder": "Gobblefather", "frames": 1, "speed": 1,
        "hidden": True, "onInitialBattleField": False, "licenseDetails": "TNR"}}
        for key, name, typ, f in out]


def ai_edits(idmap):
    names = {"enforcer": "Feathered Enforcer", "collector": "Corn Collector",
             "accountant": "Feathered Accountant", "tony": "Tony Drumstick", "vinny": "Vinny Drumstick",
             "giblet": "Don Giblet", "gobblefather": "The Gobblefather"}
    return [{"entity": "ai", "slot": "edit", "targetId": idmap[f"gf622_ai_{k}"], "name": f"{names[k]}: avatar",
             "data": {"avatar": img(f), "avatarLight": img(f), "hidden": True}} for k, f in AV.items()]


def badge():
    return {"entity": "badge", "slot": "create", "srcId": f"{P}_badge", "name": "Family Business", "data": {
        "name": "Family Business", "image": img(ICON["badge"]), "hidden": True,
        "description": "Brought down the Feathered Family and returned the stolen harvest. Thanksgiving 2026."}}


def ring():
    d = dict(DEFAULT_ITEM)
    d.update({
        "name": "Golden Feathered Ring",
        "description": "<i>The Gobblefather's own signet: a black feather curled around a golden ear of corn.</i>"
                       "<br><br>The Family protects its own. While equipped, it guards your pockets against robbery.",
        "itemType": "ACCESSORY", "rarity": "LEGENDARY", "slot": "ITEM", "stackSize": 1, "canStack": False,
        "destroyOnUse": False, "preventBattleUsage": True, "actionCostPerc": 40, "battleDescription": "Other",
        "requiredLevel": 70, "image": img(ICON["ring"]),
        "effects": [dict(FX_BLANK, type="robprevent", power=40, target="INHERIT", calculation="static",
                         description="Rob protection")],
    })
    return {"entity": "item", "slot": "create", "srcId": f"{P}_ring", "name": d["name"], "data": d}


def cane_token():
    d = dict(DEFAULT_ITEM)
    d.update({
        "name": "Gobblefather's Cane Token",
        "description": "<i>A gold-stamped claim ticket from the Feathered Estate.</i><br><br>Use it to unlock "
                       "<b>Gobblefather's Cane</b>, a new look and name for <b>Night's Testament</b> with the same "
                       "stats. You must own Night's Testament. The token is used up.",
        "itemType": "CONSUMABLE", "rarity": "LEGENDARY", "slot": "NONE", "stackSize": 999, "canStack": True,
        "destroyOnUse": True, "preventBattleUsage": True, "actionCostPerc": 60,
        "battleDescription": "Variant token", "requiredLevel": 1, "image": img(ICON["cane"]),
        "effects": [{"type": "unlockitemvariant", "variantId": None,
                     "description": "Unlocks a token-locked item variant when used on an item", "power": 1,
                     "powerPerLevel": 0, "calculation": "static", "direction": "offence", "staticAssetPath": "",
                     "staticAnimation": "", "appearAnimation": "", "disappearAnimation": "", "appearSfx": "",
                     "disappearSfx": "", "target": "SELF"}],
    })
    return {"entity": "item", "slot": "create", "srcId": f"{P}_cane_token", "name": d["name"], "data": d}


def cane_variant():
    return {"entity": "itemVariant", "slot": "create", "srcId": f"{P}_cane_variant",
            "name": "Gobblefather's Cane", "data": {
                "itemId": NIGHTS_TESTAMENT, "name": "Gobblefather's Cane", "image": img(ICON["cane"]),
                "requiredItemId": f"@item:{P}_cane_token", "costType": "VARIANT_TOKEN", "cost": 1,
                "order": VARIANT_ORDER, "hidden": True,
                "description": "Night's Testament, sheathed in a black lacquered cane under a golden turkey head. "
                               "The Gobblefather never carried a weapon. He never needed to be seen carrying one.",
                "battleDescription": "%user twists the golden turkey head and draws a blade from the cane. "
                                     "One clean stroke, and %target has paid in full."}}


def swap_ai_refs(o, idmap):
    if isinstance(o, dict):
        return {k: swap_ai_refs(v, idmap) for k, v in o.items()}
    if isinstance(o, list):
        return [swap_ai_refs(v, idmap) for v in o]
    if isinstance(o, str) and o.startswith("@ai:"):
        return idmap[o[4:]]
    return o


def quest(idmap):
    f = gf.Factory(ctors=gf.CTORS, entities=gf.ENTS, checks=gf.CHECKS)
    q = gf.build_quest(f, gf.build_objectives(f))
    q = swap_ai_refs(q, idmap)
    q["slot"] = "edit"
    q["targetId"] = QUEST_ID
    q.pop("srcId", None)
    c = q["data"]["content"]

    def scene(k):
        return GOAH if k == "goah" else f"@scene:{P}_sc_{k}"
    for o in c["objectives"]:
        bg, chars = SCENES[o["id"]]
        o["sceneBackground"] = f"@scene:{P}_bg_{bg}"
        o["sceneCharacters"] = [scene(k) for k in chars]
    c["sceneBackground"] = f"@scene:{P}_bg_trade_road"
    c["sceneCharacters"] = []
    r = c["reward"]
    for k in ("reward_exp", "reward_money", "reward_tokens", "reward_prestige", "reward_clanpoints"):
        r[k] = PACKAGE[k]
    r["reward_badges"] = [f"@badge:{P}_badge"]
    r["reward_items"] = [{"ids": [f"@item:{P}_ring"], "number": 100, "quantity": 1},
                         {"ids": [f"@item:{P}_cane_token"], "number": 100, "quantity": 1}]
    q["name"] = "The Gobblefather: scenes and rewards"
    return q


def main():
    idmap = json.load(open(B623))["idmap"]
    missing = [n for n in SCENES if n not in {o[0] for o in gf.GRAPH}]
    assert not missing and len(SCENES) == len(gf.GRAPH), missing
    # build order (law 17, validate.py): badge, assets, items + variant, ai, quest
    items = [badge()] + assets() + [ring(), cane_token(), cane_variant()] + ai_edits(idmap) + [quest(idmap)]
    files = sorted(set(list(BG.values()) + list(SC.values()) + list(AV.values()) + list(ICON.values())))
    sizes = {fn: os.path.getsize(os.path.join(ART, fn)) for fn in files}
    refs = {s[5:] for s in json.dumps(items).replace('"', ' ').split() if s.startswith("@img:")}
    assert refs == set(files), (refs ^ set(files))
    man = {
        "_note": "push/631: The Gobblefather step 3 (art + rewards), browser Forge. HIDDEN except the badge and "
                 "the Night's Testament variant, which have no hidden state. Follow-up over the connector: token "
                 "edit binding unlockitemvariant.variantId to the variant id from this run's bundle. "
                 "Generated by push/631_gobblefather_art_rewards.gen.py; do not hand-edit.",
        "dedupNames": True, "imgSizes": sizes, "items": items,
    }
    with open(OUT_JSON, "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_STORED) as z:
        z.writestr("manifest.json", json.dumps(man, indent=1, ensure_ascii=False) + "\n")
        for fn in files:
            z.write(os.path.join(ART, fn), fn)
    import hashlib
    led = os.path.join(ROOT, "state", "validate_exceptions", "631_gobblefather_art_rewards.json")
    accepted = ([f"ERROR  manifest: build order: {e} appears after a later phase"
                 for e in ["item"] * 2 + ["itemVariant"] + ["ai"] * 7 + ["quest"]])
    with open(led, "w", encoding="utf-8") as fh:
        json.dump({
            "manifest": "push/631_gobblefather_art_rewards.json",
            "ruling": "Accepted by RUL-2026-10-31-085: build-order diagnostics (validator bug).",
            "reason": "validate.py renames every asset entry to 'gameAsset' before its build-order lint, whose table "
                      "is keyed 'asset', so the 11 assets rank 9 and every item/variant/ai/quest after them is flagged. "
                      "The order here is the law-17 order (badge, assets, items + variant, ai, quest); the quest "
                      "references the assets by @scene and the items and badge by @item/@badge, so it must run last. "
                      "check_manifest.mjs: 0 pre-send problems. Validator bug, Lane A, not fixed here.",
            "sha256": hashlib.sha256(open(OUT_JSON, "rb").read()).hexdigest(),
            "accepted": accepted,
        }, fh, indent=1)
        fh.write("\n")
    kinds = {}
    for i in items:
        kinds[i["entity"]] = kinds.get(i["entity"], 0) + 1
    print(OUT_ZIP, os.path.getsize(OUT_ZIP), kinds)


if __name__ == "__main__":
    main()
