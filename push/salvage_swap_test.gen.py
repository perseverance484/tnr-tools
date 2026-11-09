#!/usr/bin/env python3
"""Salvager's Trade swap test (push/539). All HIDDEN; nothing here goes live.

    python3 push/salvage_swap_test.gen.py   -> push/539_salvage_swap_test.json

Director 2026-11-09 09:06 ("Build the swap test"), after the Salvager's Trade proposal (Claude Doc YNEcUm9oBvYijwTRYWYUAc).
Proves on the live engine, on the test account only, the three things the Trade rests on:
  1. entryItems on an EVENT quest take the salvage (proven so far only on special/battlepyramid/MoE quests);
  2. the win_quest pays the chart;
  3. a one-round foe stays harmless (end_turn only, level 1, 100 HP, not scaled to the player).

Records:
  * Wreck Salvage (item, hidden, untradeable per the director's Nov 2 ruling). Reusable by the real Trade; the image is a
    placeholder until his icon.
  * Wreck Test Husk (AI, hidden): includeDefaultRules false, one unconditional end_turn rule (a final unconditional
    rule is required, or the AI suicides).
  * Salvage Swap Test: Grant (event quest, hidden): one dialog, then win pays 6 Wreck Salvage.
  * Salvage Swap Test: Tide Chart (event quest, hidden): entry 4 Wreck Salvage. d_trade (the shield dialog directly
    before the fight) -> b_husk -> w_trade pays 1 Tide Chart. "Back out" -> w_back refunds the 4 salvage. A loss pays the
    salvage back on a dialog (F03: fail_quest rewards are never paid), then fails.
The Tide Chart is the live push/329 item. Do not hand-edit the output.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = 539
PFX = "sg539_"
TIDE_CHART = "@item:sg329_tide_chart"  # replaced below with the literal 329 id
SCENE_BG = "rX78pJPETsUL2JrsSvGHn"        # the Fire scene (push/509)
SALVAGER = "Xugt7415D3-tepLfxpwM5"        # the salvager scene character (push/509)
QUEST_IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # Fire quest image
ITEM_IMG = "https://ui0arpl8sm.ufs.sh/f/xigFDKI7-1Qr1qgdrrpcI.webp"  # placeholder (a chart icon) until his salvage icon
AVATAR = "https://ui0arpl8sm.ufs.sh/f/ai-sprite-20261018-wTgO-Q32caSSd0is1QIS7-main-067335f147b0.webp"
BUNDLE_329 = os.path.join(ROOT, "harvests/inbox/tnr_results_1793424666625.json")


def tide_chart():
    for e in json.load(open(BUNDLE_329))["entries"]:
        if e.get("srcId") == "sg329_tide_chart" and e.get("state") == "ok":
            assert e["name"] == "Tide Chart", e["name"]
            return e["id"]
    raise SystemExit("Tide Chart missing from the 329 bundle")


def item_data():
    base = json.load(open(os.path.join(ROOT, "push/536_skyglass_new_charts_items.json")))["items"][0]["data"]
    d = dict(base)
    d.update({
        "name": "Wreck Salvage", "rarity": "COMMON", "image": ITEM_IMG, "canBeTraded": False, "hidden": True,
        "effects": [], "destroyOnUse": False, "preventBattleUsage": True, "itemType": "OTHER", "stackSize": 999,
        "canStack": True, "battleDescription": "Salvage",
        "description": "<i>Brass fittings, glass shards and rope pulled out of the Skyglass Wreck.</i><br><br>"
                       "The salvager at the Fire trades charts for it.",
    })
    return d


def ai_data():
    return {
        "username": "Wreck Test Husk", "hidden": True, "level": 1, "rank": "GENIN", "poolsMultiplier": 1,
        "statsMultiplier": 1, "regeneration": 0, "gender": "Unknown", "preferredGeneral1": "Strength",
        "preferredGeneral2": "Speed", 
        "primaryElement": None, "secondaryElement": None, "isSummon": False,
        "avatarFacing": "left",
        **{m: 10 for m in ("ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery")},
        "bloodlineMastery": 10, "sageMastery": 10,
        **{s: 10 for s in ("offence", "defence", "strength", "intelligence", "willpower", "speed")},
        "avatar": AVATAR, "jutsus": [], "items": [], "effects": [],
        "includeDefaultRules": False,
        "rules": [{"conditions": [], "action": {"type": "end_turn", "description": "stands still (swap test)"}}],
    }


SALVAGE = "@item:" + PFX + "salvage"
HUSK = "@ai:" + PFX + "husk"
scene = {"sceneBackground": SCENE_BG, "sceneCharacters": []}


def pay(i, n):
    return {"ids": [i], "number": 100, "quantity": n}


def quest_base(name, desc, success, objectives, entry):
    return {
        "name": name, "description": desc, "image": QUEST_IMG, "questType": "event", "questRank": "D",
        "successDescription": success, "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True,
        "hidden": True, "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
        "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
        "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives, "sceneBackground": SCENE_BG, "sceneCharacters": [],
                    "entryItems": entry, "isolated": False, "reward": {}},
    }


def main():
    tide = tide_chart()
    grant = quest_base(
        "Salvage Swap Test: Grant", "Test only. The salvager hands over six pieces of salvage.", "Six salvage, as promised.",
        [{"id": "d_grant", "task": "dialog", **scene,
          "description": "\"Test haul. Take it.\"",
          "nextObjectiveId": [{"text": "Take the salvage", "nextObjectiveId": "w_grant"}]},
         {"id": "w_grant", "task": "win_quest", **scene, "description": "Six pieces of salvage.",
          "reward_items": [pay(SALVAGE, 6)]}], [])
    trade = quest_base(
        "Salvage Swap Test: Tide Chart", "Test only. Four salvage for a Tide Chart.", "A Tide Chart, fairly traded.",
        [{"id": "d_trade", "task": "dialog", **scene,
          "description": "\"Four pieces for a Tide Chart. Clear the husk off my nets and it's yours.\"",
          "nextObjectiveId": [{"text": "Trade", "nextObjectiveId": "b_husk"},
                              {"text": "Back out", "nextObjectiveId": "w_back"}]},
         {"id": "b_husk", "task": "start_battle", **scene, "description": "A husk drifts in from the wreck.",
          "opponentAIs": [{"ids": [HUSK], "number": 1, "quantity": 1}], "completionOutcome": "Win", "scaleGains": 1,
          "keepOriginalPools": False, "opponent_scaled_to_user": False,
          "nextObjectiveId": "w_trade", "failObjectiveId": "f_back",
          "failDescription": "You are defeated.", "drawDescription": "The husk drifts off.",
          "fleeDescription": "You step back from the nets."},
         {"id": "w_trade", "task": "win_quest", **scene, "description": "She hands over a Tide Chart.",
          "reward_items": [pay(tide, 1)]},
         {"id": "f_back", "task": "dialog", **scene, "description": "\"Keep your salvage. Try again when you're up.\"",
          "reward_items": [pay(SALVAGE, 4)],
          "nextObjectiveId": [{"text": "Leave", "nextObjectiveId": "f_lost"}]},
         {"id": "f_lost", "task": "fail_quest", **scene, "description": "The trade falls through."},
         {"id": "w_back", "task": "win_quest", **scene, "description": "She hands the salvage back.",
          "reward_items": [pay(SALVAGE, 4)]}],
        [{"ids": [SALVAGE], "number": 4}])
    items = [
        {"entity": "item", "slot": "create", "srcId": PFX + "salvage", "phase": 1, "name": "Wreck Salvage",
         "data": item_data()},
        {"entity": "ai", "slot": "create", "srcId": PFX + "husk", "phase": 1, "name": "Wreck Test Husk", "data": ai_data()},
        {"entity": "quest", "slot": "create", "srcId": PFX + "grant", "phase": 2, "name": grant["name"], "data": grant},
        {"entity": "quest", "slot": "create", "srcId": PFX + "trade", "phase": 2, "name": trade["name"], "data": trade},
    ]
    m = {"_note": f"push/{NUM}, HIDDEN. Salvager's Trade swap test (director 2026-11-09 09:06): Wreck Salvage item "
                  "(untradeable), a harmless end_turn AI, a grant quest (6 salvage) and an event trade quest (entry 4 "
                  "salvage, one-round fight, pays a Tide Chart). Test account only. Generated by "
                  "push/salvage_swap_test.gen.py; do not hand-edit.",
         "dedupNames": True, "items": items}
    path = os.path.join(ROOT, f"push/{NUM}_salvage_swap_test.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(path, len(items))


if __name__ == "__main__":
    main()
