#!/usr/bin/env python3
"""Stolen Stores: the Chart of the Flooded Stores and its Battle Arena run, all HIDDEN (hidden end-to-end test).

    python3 push/flooded_stores_run.gen.py item                         # write push/635 (the chart item)
    python3 push/flooded_stores_run.gen.py run --item <635 bundle>      # write push/636 (the run + test grant edit)
    python3 push/flooded_stores_run.gen.py run --stand-in               # TEST ONLY: made-up chart id, writes nothing

Design of record: the Stolen Stores design doc, rev 33 (The Flooded Stores section, approved 2026-11-18); the director's
"Yes, create and test" (2026-11-18 18:00 UTC) for the hidden test. Enemies are the hidden records created by push/632-634
(flooded_stores_build), by literal id. Every fight is scaled to the player (doc: "enemies scaled to the player").

Known gaps, stand-ins, flagged for the director (not settled here):
- REWARD PICK COUNT: the engine takes one reward choice per quest (content.rewardMode "choose" + one rewardPickCount).
  The doc's "choose two from a different list" for beating Isonade cannot be expressed. This build gives both endings
  the take-the-stores choose-one; the Isonade ending adds its 3 Wreck Salvage and the 2% Shard of the Ledger as fixed
  rolls on its win node.
- reward_exp is not in the design: 4000 on both endings, the rare-tier step used by the other rare chart.
- Icons are placeholders (the Galley Stores icon) until the chart icon is painted and uploaded.
- push/636 also repoints the hidden test-only quest "Salvage Swap Test: Grant" (x5-kg5W6sHoyXM8yJk-M4, mastery) to pay
  1 chart, so the staff account can enter the run without an item grant endpoint.
Do not hand-edit the output.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
NUM_ITEM, NUM_RUN, NUM_FIX = 635, 636, 640
RUN_ID = "-_1MdlGp-gxdiWKb6Bf3V"  # push/636 results bundle (hidden)
PFX = "fs635_"

ITEM = {  # push/skyglass_new_charts.gen.py ITEM, design_data.json
    "Core Rot": "KuqLeFB12BdB-0s5O1udk", "Galley Stores": "D-QTnbjgTyIVc593zzdSB",
    "Skyglass Token": "nzCW7A-_AuYMzBs2wClnM", "Medicine Inro": "ixEKlJ0MmDrX7JoMNJVhi",
    "Skyglass Coffer": "THo7rfzP-S82_43aN8fs3", "Sealed Treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
    "Wreck Salvage": "mW6_ZGtGcCSuXGPhn-H4o", "Shard of the Ledger": "cGrmhfe88ACBvFk2XqvSu",
}
AI = {  # push/633 + push/634 results bundles (hidden)
    "isonade": "K_lwNvMPJLMsn1sUGXqZm", "deckhand": "MVy7rX2FW9mvGQJNXUKCH", "mate": "veKt6fjJqqdDBRJyYiTOT",
    "quartermaster": "rg-poMY3IBOl3xFrumEaq", "sentinel": "eIAwMQw7RPLVLUKW41FGX", "blade": "RCyyhNmDmJq3xZAAItnG7",
}
SCENE = {  # push/skyglass_hunts.gen.py SCENE (uploaded boards)
    "hold": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",
    "lower_hull": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi",
    "deck_b": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJcoxkatSnxBpQqGNDcTHbLmYz8uXAl3oa54ti",
}
ICON = "https://ui0arpl8sm.ufs.sh/f/iS35oVeCsybzoJYcfJ2xp.webp"  # placeholder: Galley Stores icon
GRANT_QUEST = "x5-kg5W6sHoyXM8yJk-M4"
EXP = 4000
FOOTER = ("<i>Spent when the run starts. No refills between fights; once inside, you leave by winning, falling or "
          "abandoning. Claim any waiting reward first.</i>")
CLAIM_LINE = "Claim any reward choice still waiting from an earlier run before you set out."
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the way back closes.",
          "fleeDescription": "You break away, and the way back closes behind you."}
PICK = [("Galley Stores", 3), ("Medicine Inro", 1), ("Skyglass Token", 1)]
CHANCE = [("Core Rot", 25), ("Sealed Treasury", 3)]

CARD = ("<i>A quartermaster's issue sheet, every ration signed for twice. The last column is in another hand, and it "
        "only ever says \"taken\".</i><br><br><b>The Flooded Stores</b> · Battle Arena · Level 30+<br>"
        "Difficulty: ★★★☆☆<br><b>Chance drops:</b> Core Rot 25% · Sealed Treasury 3% · Wreck Salvage ×1<br>"
        "<b>Choose one</b> (two from the Stores Below): Galley Stores ×3 · Medicine Inro · Skyglass Token<br>" + FOOTER)
RUN_DESC = ("Below the galley the Quartermaster still hands out rations, and his crew still line up for them.\n\n"
            "3 fights · then take the stores, or go below for a 4th.")


def dialog(i, scene, desc, choices):
    return {"id": i, "task": "dialog", "description": desc, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}


def battle(i, scene, desc, keys, nxt, scaled=True):
    counts = {}
    for k in keys:
        counts[AI[k]] = counts.get(AI[k], 0) + 1
    return {"id": i, "task": "start_battle", "description": desc, "sceneBackground": SCENE[scene],
            "sceneCharacters": [], "opponentAIs": [{"ids": [a], "number": n, "quantity": 1} for a, n in counts.items()],
            "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False, "opponent_scaled_to_user": scaled,
            "nextObjectiveId": nxt, "failObjectiveId": "f_lost", **SHARED}


def drop(name, chance, quantity=1):
    return {"ids": [ITEM[name]], "number": chance, "quantity": quantity}


def win(i, scene, desc, extra):
    return {"id": i, "task": "win_quest", "description": desc, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "reward_exp": EXP, "reward_items": [drop(n, p) for n, p in CHANCE] + [drop(*e) for e in extra]}


def objectives():
    return [
        dialog("d_galley", "deck_b", "The galley is as it always was: fires lit, cooks at work, nobody eating. But a "
               "cold draft is coming up through the floor, and it smells of the sea. Down the steps, a Quartermaster's "
               "Mate is handing out biscuits to a line of deckhands.", [("Break up the line", "b1")]),
        battle("b1", "deck_b", "The Mate looks up from his list, and the line turns around.",
               ["mate", "deckhand", "deckhand"], "d_crates"),
        dialog("d_crates", "hold", "The stores door is blocked by crates, and a Sentinel is still stacking more of them "
               "in front of the Mate behind it.", [("Go through the wall", "b2")]),
        battle("b2", "hold", "The Sentinel sets another crate down and turns to you.", ["sentinel", "mate"], "d_qm"),
        dialog("d_qm", "hold", "In the storeroom the Quartermaster stands at his ledger, a Looting Blade on either side, "
               "and signs for every ration twice.", [("Close the ledger", "b3")]),
        battle("b3", "hold", "The Quartermaster opens the stores to his crew.", ["quartermaster", "blade", "blade"],
               "d_choice"),
        dialog("d_choice", "hold", "The stores are yours: crates, tins, a cask that sloshes. Under your feet the deck "
               "shifts, slowly, the way a ship moves when something heavy leans on it.",
               [("Take the stores", "w_take"), ("Go below", "d_below")]),
        dialog("d_below", "lower_hull", "The storeroom is half sea now. What's left of the stores floats in black water, "
               "and something in the water is eating them.", [("Wade in", "b4")]),
        # The director, 2026-11-18 18:37 UTC: the crew scale to the player, Isonade does not. Scaling is per fight
        # (routers/combat.ts scaleTarget), and Isonade fights alone, so b4 is the one unscaled fight: its stored
        # level-100 record, capped at JONIN, which is exactly the row the harness tuned (cclib aiRow + sim capUserStats).
        battle("b4", "lower_hull", "The water heaves, and one pale eye opens in it.", ["isonade"], "w_below",
               scaled=False),
        win("w_take", "hold", "You carry the stores up past a crew that never looks at you.",
            [("Wreck Salvage", 100, 1)]),
        win("w_below", "lower_hull", "It lets go and slides back out through the crack in the hull. The ship settles. "
            "Above you, the crew carry on as if nothing happened.",
            [("Wreck Salvage", 100, 3), ("Shard of the Ledger", 2, 1)]),
        {"id": "f_lost", "task": "fail_quest", "description": "The stores close over you, and you wake on the sand "
         "with nothing.", "sceneBackground": SCENE["lower_hull"], "sceneCharacters": []},
    ]


ITEM_BASE = {  # push/skyglass_new_charts.gen.py ITEM_BASE (push/329's chart create)
    "itemType": "OTHER", "slot": "NONE", "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE",
    "cost": 1, "repsCost": 0, "seichiSilverCost": 0, "stackSize": 999, "destroyOnUse": False, "range": 0,
    "chakraCost": 0, "staminaCost": 0, "healthCost": 0, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
    "healthCostReducePerLvl": 0, "actionCostPerc": 60, "battleDescription": "Treasure chest", "canStack": True,
    "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": False, "hidden": True, "maxEquips": 1,
    "preventBattleUsage": True, "requiredLevel": 1, "xpToLevel": 1000, "parentItemId": None, "requiredStrength": None,
    "requiredSpeed": None, "requiredIntelligence": None, "requiredWillpower": None, "canBeCrafted": False,
    "canBeImbued": False, "canBeHunted": False, "canBeGathered": False, "canBeTraded": True, "isFarmSeed": False,
    "farmGrowTimeSeconds": 0, "farmYieldItemId": None, "farmMinLevel": 1, "farmPlantExperience": 0,
    "farmHarvestExperience": 0, "farmSellValue": 0, "farmExtractSeedItemId": None, "farmExtractSeedCount": 0,
    "isFarmFertilizer": False, "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0, "craftingExperience": 0,
    "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH", "effects": [],
}


def item_entry():
    data = dict(ITEM_BASE, name="Chart of the Flooded Stores", description=CARD, rarity="RARE", image=ICON)
    return {"entity": "item", "slot": "create", "srcId": PFX + "chart", "phase": 1,
            "name": "Chart of the Flooded Stores", "data": data}


def run_entry(chart_id):
    objs = objectives()
    reward = {"reward_items": [{"ids": [ITEM[n]], "number": 100, "quantity": q} for n, q in PICK]}
    return {"entity": "quest", "slot": "create", "srcId": "fs636_run", "phase": 1, "name": "The Flooded Stores",
            "data": {
                "name": "The Flooded Stores", "description": RUN_DESC + "\n\n" + CLAIM_LINE, "image": ICON,
                "questType": "battlepyramid", "questRank": "A",
                "successDescription": "You came back up from the flooded stores with what the sea hadn't taken.",
                "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
                "requiredLevel": 30, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
                "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
                "startsAt": None, "endsAt": None,
                "content": {"objectives": objs, "sceneBackground": "", "sceneCharacters": [],
                            "entryItems": [{"ids": [chart_id], "number": 1}], "isolated": True,
                            "rewardMode": "choose", "rewardPickCount": 1, "reward": reward}}}


def grant_entry(chart_id):
    # Read back live 2026-11-18 18:35 UTC (mastery, hidden, rewardMode all, two objectives); only the texts and the
    # w_grant reward change. Forge fetch-merges top-level fields; content is sent whole.
    scene = "rX78pJPETsUL2JrsSvGHn"
    return {"entity": "quest", "slot": "edit", "targetId": GRANT_QUEST, "phase": 2,
            "name": "Salvage Swap Test: Grant: pays 1 Chart of the Flooded Stores (test only)",
            "data": {
                "description": "Test only. The salvager hands over one Chart of the Flooded Stores.",
                "successDescription": "One chart, as promised.", "hidden": True,
                "content": {"objectives": [
                    {"id": "d_grant", "task": "dialog", "sceneBackground": scene, "sceneCharacters": [],
                     "description": "\"Test haul. Take it.\"",
                     "nextObjectiveId": [{"text": "Take the chart", "nextObjectiveId": "w_grant"}]},
                    {"id": "w_grant", "task": "win_quest", "sceneBackground": scene, "sceneCharacters": [],
                     "description": "One Chart of the Flooded Stores.",
                     "reward_items": [{"ids": [chart_id], "number": 100, "quantity": 1}]}],
                    "sceneBackground": scene, "sceneCharacters": [], "entryItems": [], "isolated": False,
                    "rewardMode": "all", "rewardPickCount": 1, "reward": {}}}}


def check_graph(objs):
    ids = {o["id"] for o in objs}
    assert len(ids) == len(objs)
    by, seen, todo = {o["id"]: o for o in objs}, set(), [objs[0]["id"]]
    while todo:
        i = todo.pop()
        if i in seen:
            continue
        seen.add(i)
        o = by[i]
        nxt = o.get("nextObjectiveId")
        nx = [x["nextObjectiveId"] for x in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])
        if o.get("failObjectiveId"):
            nx.append(o["failObjectiveId"])
        for n in nx:
            assert n in ids, (i, n)
            todo.append(n)
    assert seen == ids, ids - seen
    for o in objs:
        assert "—" not in o["description"] and "–" not in o["description"], o["id"]


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/flooded_stores_run.gen.py; do not hand-edit.", "dedupNames": True}
    m.update(extra or {})
    m["items"] = items
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items), "items")


def chart_id_from_bundle(path):
    for e in json.load(open(path))["entries"]:
        if (e.get("srcId") or "") == PFX + "chart":
            assert e["state"] == "ok" and NANO.match(e["id"]), e
            return e["id"]
    raise SystemExit("chart not in bundle")


def main():
    for v in list(ITEM.values()) + list(AI.values()) + [GRANT_QUEST]:
        assert NANO.match(v), v
    assert "—" not in CARD + RUN_DESC
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "item":
        write(NUM_ITEM, "flooded_stores_chart", "push/635, HIDDEN: Chart of the Flooded Stores (Rare, tradeable, "
              "unusable in battle, stack 999), the live chart card layout. Icon is a PLACEHOLDER (Galley Stores).",
              [item_entry()])
        return
    if mode == "run":
        stand_in = "--stand-in" in sys.argv
        cid = "STANDIN_chart_xxxxxxx" if stand_in else chart_id_from_bundle(sys.argv[sys.argv.index("--item") + 1])
        items = [run_entry(cid), grant_entry(cid)]
        check_graph(items[0]["data"]["content"]["objectives"])
        if stand_in:
            print("run", len(items[0]["data"]["content"]["objectives"]), "objectives (stand-in, not written)")
            return
        write(NUM_RUN, "flooded_stores_run", "push/636, HIDDEN: The Flooded Stores run (isolated Battle Pyramid "
              "entered with the chart, 3 scaled crew fights, then take the stores or go below to Isonade; a lost "
              "fight fails the run) and the test-only grant quest repointed to pay 1 chart. Reward pick count "
              "gap: both endings share one choose-one (engine allows one per quest).", items,
              {"_chart_id": cid, "_ai_keys": AI})
        return
    if mode == "isonade-fixed":
        cid = sys.argv[sys.argv.index("--chart") + 1]
        assert NANO.match(cid) and NANO.match(RUN_ID)
        content = run_entry(cid)["data"]["content"]
        check_graph(content["objectives"])
        fixed = [o["id"] for o in content["objectives"] if o.get("task") == "start_battle"
                 and not o["opponent_scaled_to_user"]]
        assert fixed == ["b4"], fixed
        write(NUM_FIX, "flooded_stores_isonade_fixed", "push/640, HIDDEN: The Flooded Stores, b4 (Isonade) no longer "
              "scales to the player, so Isonade fights at its stored level 100 while fights 1 to 3 still scale. "
              "Content is sent whole; only b4's opponent_scaled_to_user changes.",
              [{"entity": "quest", "slot": "edit", "targetId": RUN_ID, "phase": 1,
                "name": "The Flooded Stores: Isonade fixed at level 100", "data": {"hidden": True, "content": content}}],
              {"_chart_id": cid})
        return
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
