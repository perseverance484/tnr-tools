#!/usr/bin/env python3
"""Generate push/274: the Armory Requisition (token + Special quest) and the Wreck's chest of chests (RUL-2026-10-25-014).

    python3 push/skyglass_mystery.gen.py

Phase 1: "Armory Requisition", a one-node Special quest whose completion is a pick of 1 of the five Tool Pouches.
Phase 2: the Armory Requisition token (consuming it starts that quest: noncombatquest, routers/item.ts requires SELF,
SINGLE and preventBattleUsage). Phase 3: the chest, a weighted cache with one roll. All HIDDEN. Do not hand-edit.
"""
import hashlib, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCH = os.path.join(ROOT, "archive/spent-manifests/push-2026-10-25")

CHEST_NAME = "Unmarked Cargo"  # director 2026-10-25
ITEM = {"inro": "ixEKlJ0MmDrX7JoMNJVhi", "strongbox": "h-d58UCSuHN8EZKbLjT5R", "coffer": "THo7rfzP-S82_43aN8fs3",
        "case": "B48dTRsoLJGKBWIUbeUoG", "treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
        "pouches": ["D0gtI5dOgj2dFO4VexsLJ", "ZZOrFciKSJazAtkW9nt_7", "we2DtPSH2Q5quEvxj7xO2", "hcvHkfcYHP6qBEO_dRFl6",
                    "z9U9wvJKDGtimll6BnTuL"]}
PACK_REF = "c371a8c1a8302ed23ba7287ed77cb780250dbb24"
IMAGES = {"icon-armory-requisition.webp": "art/skyglass_event_icons/exports/icon-armory-requisition.webp",
          "icon-skyglass-coffer.webp": "art/skyglass_event_icons/exports/icon-skyglass-coffer.webp"}

# The chest (director 2026-10-25): one roll; each tier gives one of its entries.
TIERS = [("Common", 5000, ["inro"]), ("Rare", 3000, ["strongbox", "@item:armory_requisition"]),
         ("Epic", 1500, ["coffer", "case"]), ("Legendary", 500, ["treasury"])]


def base_item():
    m = json.load(open(os.path.join(ARCH, "260_skyglass_items_create.json")))
    return next(it for it in m["items"] if it["srcId"] == "skyglass_coffer")


def reward_effect(display, cache):
    eff = json.loads(json.dumps(base_item()["data"]["effects"][0]))
    eff["description"] = display
    eff["weightedCache"] = cache
    return eff


def item_id(k):
    return k if k.startswith("@") else ITEM[k]


def main():
    coffer = base_item()["data"]
    special = {"entity": "quest", "slot": "create", "phase": 1, "name": "Armory Requisition", "srcId": "armory_requisition_quest",
               "data": {
                   "name": "Armory Requisition", "questType": "special", "questRank": "D", "hidden": True,
                   "description": ("The Skyglass armory still honours a valid requisition. Present it and choose the "
                                   "tool pouch you were issued."),
                   "successDescription": "The quartermaster's seal accepts your requisition. Choose your pouch.",
                   "image": "@img:icon-armory-requisition.webp", "retryDelay": "none", "attemptDelay": "none",
                   "consecutiveObjectives": True, "requiredLevel": 1, "maxLevel": 100, "prerequisiteQuestId": None,
                   "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
                   "content": {"objectives": [{"id": "w_issue", "task": "win_quest", "sceneBackground": "", "sceneCharacters": [],
                                               "description": "The requisition is stamped and the armory's stores open."}],
                               "sceneBackground": "", "sceneCharacters": [], "rewardMode": "choose", "rewardPickCount": 1,
                               "reward": {"reward_items": [{"ids": [p], "number": 100, "quantity": 1} for p in ITEM["pouches"]]}}}}
    token = dict(coffer)
    token.update({"name": "Armory Requisition", "rarity": "RARE", "canBeTraded": False,
                  "description": ("A sealed requisition slip from the Skyglass armory. Use it to choose one of the five "
                                  "elemental tool pouches."),
                  "image": "@img:icon-armory-requisition.webp",
                  "effects": [{"type": "noncombatquest", "questId": "@quest:armory_requisition_quest", "power": 1,
                               "target": "INHERIT", "direction": "offence", "calculation": "static", "powerPerLevel": 0,
                               "description": "Starts the Armory Requisition", "appearSfx": "", "disappearSfx": "",
                               "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}]})
    chest = dict(coffer)
    chest.update({"name": CHEST_NAME, "rarity": "EPIC", "canBeTraded": False,
                  "description": ("Unmarked cargo hauled out of the Skyglass wreck. Something from the ship's stores is "
                                  "sealed inside; no one knows what until it is opened."),
                  "image": "@img:icon-skyglass-coffer.webp",  # placeholder icon until the chest is drawn
                  "effects": [reward_effect(f"{CHEST_NAME}: one of the ship's containers", {
                      "version": 1, "displayName": CHEST_NAME, "rolls": [{"count": 1, "probability": 10000}],
                      "tiers": [{"name": n, "probability": p, "entries": [{"items": [{"itemId": item_id(k), "quantity": 1}]} for k in ks]}
                                for n, p, ks in TIERS]})]})
    assert sum(p for _, p, _ in TIERS) == 10000
    # Listed items first for validate.py's build-order lint; Forge runs by the explicit phases (quest 1, token 2, chest 3).
    items = [{"entity": "item", "slot": "create", "phase": 2, "name": "Armory Requisition", "srcId": "armory_requisition", "data": token},
             {"entity": "item", "slot": "create", "phase": 3, "name": CHEST_NAME, "srcId": "wreck_chest", "data": chest},
             special]
    files = {}
    used = json.dumps(items)
    for name, path in IMAGES.items():
        if "@img:" + name in used:
            b = open(os.path.join(ROOT, path), "rb").read()
            files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    m = {"_note": (
            f"push/274 (RUL-2026-10-25-014), all HIDDEN. Phase 1: the Armory Requisition Special quest (one node; pick 1 of "
            f"the five Tool Pouches; Special quests take no completion caps). Phase 2: the Armory Requisition token "
            f"(RARE, untradeable; using it starts that quest). Phase 3: {CHEST_NAME} (EPIC, untradeable; one roll: Common 50 "
            f"Medicine Inro / Rare 30 Sage's Strongbox or Armory Requisition / Epic 15 Skyglass Coffer or Archive Chart "
            f"Case / Legendary 5 Sealed Treasury). Placeholder chest icon = the Coffer's. The chest's 10% Wreck line goes "
            f"into push/263 once this create returns its id. Generated by push/skyglass_mystery.gen.py; do not hand-edit."),
         "dedupNames": True, "imgSizes": {k: v["bytes"] for k, v in files.items()},
         "imagePack": {"ref": PACK_REF, "files": files}, "items": items}
    json.dump(m, open(os.path.join(ROOT, "push/274_wreck_chest_and_requisition.json"), "w"), indent=1)
    print(len(items), "items")


if __name__ == "__main__":
    main()
