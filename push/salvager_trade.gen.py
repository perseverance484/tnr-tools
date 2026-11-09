#!/usr/bin/env python3
"""The Salvager's Trade (push/542, push/543). All HIDDEN; nothing here goes live before the Nov 13 release.

    python3 push/salvager_trade.gen.py           -> push/542_salvager_trade.json        (test shape)
    python3 push/salvager_trade.gen.py --final   -> push/543_salvager_trade_final.json  (overworld + prerequisite)

Director 2026-11-09 15:53 ("Just use the daily NPC rolls!") and 15:58 (one overworld salvager NPC; trades need Wreck
Sighted done). Prices from the Salvager's Trade write-up (Claude Doc YNEcUm9oBvYijwTRYWYUAc): deck charts 4 (rank C,
Genin up), hold charts 10 (rank A, Jonin), sealed charts 20 once a week (Jonin), the Lantern 30 once a week (level 80).

One quest per price tier, because a quest has one entry price. Graph (Law 47: a dialog before every win):
  d_offer --"Clear the nets"--> b_husk --win--> d_pick --chart--> w_<chart> (pays that chart x1)
          --"Keep my salvage"--> d_back (pays the salvage back) --> f_back (fail_quest)
  b_husk fail/draw/flee --> d_back.
Entry items are charged at quest START (swap test 541), and fail_quest rewards never pay (F03), so the refund sits
on the dialog before the fail. A back-out ends in a fail, so it does not use up a weekly completion.
Weekly tiers: retryDelay weekly + maxCompletes 1 (periodCapReached caps completions per period; lifetime cap ignored).
Deck and hold: retryDelay none, so maxCompletes 100 is the lifetime cap. maxAttempts 100 is lifetime for overworld.

542 builds them as questType mastery with no prerequisite so dauntless can start them from the quest log (overworld
quests start only from an NPC roll, and the placement stays inactive until release). It also tops the swap-test grant
up to 70 salvage for the test and drops "at the Fire" from Wreck Salvage. 543 sets questType overworld and
prerequisiteQuestId Wreck Sighted on all four. Do not hand-edit the outputs.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE_BG = "rX78pJPETsUL2JrsSvGHn"          # the Fire scene (push/509)
SALVAGER = "Xugt7415D3-tepLfxpwM5"          # the salvager scene character (push/509)
QUEST_IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"
SALVAGE = "mW6_ZGtGcCSuXGPhn-H4o"           # Wreck Salvage (push/539, hidden, untradeable)
HUSK = "Yk1LNNncF2dt7jY_TVSXc"              # the harmless end_turn husk (push/539)
WRECK_SIGHTED = "_zp1l7Y9a_77pgonAdsYx"     # push/507
GRANT_QID = "x5-kg5W6sHoyXM8yJk-M4"         # Salvage Swap Test: Grant (hidden, test only)
IDS = {}  # tier key -> live quest id, filled from push/542_ids.json once 542 has run
if os.path.exists(os.path.join(ROOT, "push/542_ids.json")):
    IDS = json.load(open(os.path.join(ROOT, "push/542_ids.json")))

CH = {
    "tide": ("H1s2IwtZ5JqgPEoJ55IVj", "Tide Chart"),
    "roster": ("yE8TwzygWZSNoZD5x97rW", "Watch Roster"),
    "cache": ("nbLC37UzBamthKXvZsgQB", "Chart of the Buried Cache"),
    "galley": ("rztQVUjxTLRpyEPb3yrr6", "Chart of the Rotted Galley"),
    "foundry": ("pY-0O5Gs2n89pf0kYb5J2", "Chart of the Drowned Foundry"),
    "archive": ("cRZT41zm5vhPTQwwn8vtv", "Chart of the Quarantined Archive"),
    "watch": ("aHFNuo5RkKpDcaOBLIKiu", "Chart of the Captain's Watch"),
    "nursery": ("VuTcs22ieSdQY0cEu8Fyt", "Chart of the Glass Nursery"),
    "spoiled": ("7tC2tkIuOJpMZ_YkMYDKv", "Chart of the Spoiled Hold"),
    "seal": ("sVqDdYUJIxxRYbmKbbxo0", "Reliquary Seal"),
    "heading": ("s1mYHuKqw2YuzIzxVwU-_", "The Last Heading"),
    "lantern": ("jCJv4N3JSiihuqnK0jJ7t", "Lastlight Lantern"),
}

TIERS = [
    dict(key="deck", name="The Salvager's Trade: Deck Charts", price=4, rank="C", level=30, weekly=False,
         charts=["tide", "roster", "cache", "galley"],
         desc="The salvager trades deck charts for Wreck Salvage: 4 salvage for one chart of your choice.",
         offer="She weighs your salvage in one hand. \"Four pieces buys a deck chart. Before that, a husk has "
               "tangled itself in my nets. Clear it off and you can pick.\"",
         pick="She spreads four charts on a flat stone, still damp. \"Deck charts. Pick one.\""),
    dict(key="hold", name="The Salvager's Trade: Hold Charts", price=10, rank="A", level=30, weekly=False,
         charts=["foundry", "archive", "watch", "nursery", "spoiled"],
         desc="The salvager trades hold charts for Wreck Salvage: 10 salvage for one chart of your choice.",
         offer="\"Ten pieces buys a chart from below the waterline. The hold shifts more than the deck, so "
               "don't sit on it.\" She nods at her nets. \"Husk first.\"",
         pick="She unrolls five charts and pins the corners with stones. \"The hold. Pick one.\""),
    dict(key="sealed", name="The Salvager's Trade: A Sealed Chart", price=20, rank="A", level=30, weekly=True,
         charts=["seal", "heading"],
         desc="Once a week, the salvager trades a sealed chart for 20 Wreck Salvage: a Reliquary Seal or The "
              "Last Heading.",
         offer="\"Twenty pieces, and only once a week. I don't find many of these.\" She jerks her chin at the "
               "nets. \"Husk first.\"",
         pick="She takes two charts out of an oilcloth wrap, both sealed in wax. \"One. The other waits for "
              "next week.\""),
    dict(key="lantern", name="The Salvager's Trade: The Lantern", price=30, rank="A", level=80, weekly=True,
         charts=["lantern"],
         desc="Once a week, the salvager trades a Lastlight Lantern for 30 Wreck Salvage.",
         offer="\"Thirty pieces for a Lantern. One a week, no more. Crownhold doesn't open for anyone who "
               "asks.\" She looks at the nets. \"Husk first.\"",
         pick="She lifts a Lantern out of the sand by the fire. It is cold to the touch. \"Carry it home.\""),
]


def the(n):
    return n if n.startswith("The ") else "the " + n


def pay(i, n):
    return {"ids": [i], "number": 100, "quantity": n}


def scene(extra=None):
    return {"sceneBackground": SCENE_BG, "sceneCharacters": [SALVAGER]}


def objectives(t):
    p = t["price"]
    obs = [
        {"id": "d_offer", "task": "dialog", **scene(), "description": t["offer"],
         "nextObjectiveId": [{"text": "Clear the nets", "nextObjectiveId": "b_husk"},
                             {"text": "Keep my salvage", "nextObjectiveId": "d_back"}]},
        {"id": "b_husk", "task": "start_battle", **scene(), "description": "A husk drifts out of the nets.",
         "opponentAIs": [{"ids": [HUSK], "number": 1, "quantity": 1}], "completionOutcome": "Win",
         "scaleGains": 1, "keepOriginalPools": False, "opponent_scaled_to_user": False,
         "nextObjectiveId": "d_pick", "failObjectiveId": "d_back",
         "failDescription": "The husk drags you into the surf.", "drawDescription": "The husk drifts off.",
         "fleeDescription": "You step back from the nets."},
        {"id": "d_pick", "task": "dialog", **scene(), "description": t["pick"],
         "nextObjectiveId": [{"text": CH[c][1], "nextObjectiveId": "w_" + c} for c in t["charts"]]},
    ]
    for c in t["charts"]:
        obs.append({"id": "w_" + c, "task": "win_quest", **scene(), "description": f"She hands over {the(CH[c][1])}.",
                    "reward_items": [pay(CH[c][0], 1)]})
    obs += [
        {"id": "d_back", "task": "dialog", **scene(),
         "description": f"She counts {p} pieces back into your hands. \"Come back when you want to trade.\"",
         "reward_items": [pay(SALVAGE, p)],
         "nextObjectiveId": [{"text": "Leave", "nextObjectiveId": "f_back"}]},
        {"id": "f_back", "task": "fail_quest", **scene(), "description": "No trade today."},
    ]
    return obs


def quest(t, final):
    return {
        "name": t["name"], "description": t["desc"], "image": QUEST_IMG,
        "questType": "overworld" if final else "mastery", "questRank": t["rank"],
        "successDescription": "A fair trade.",
        "retryDelay": "weekly" if t["weekly"] else "none", "attemptDelay": "none", "consecutiveObjectives": True,
        "hidden": True, "requiredLevel": t["level"], "maxLevel": 100, "maxAttempts": 100,
        "maxCompletes": 1 if t["weekly"] else 100,
        "prerequisiteQuestId": WRECK_SIGHTED if final else None, "tierLevel": None, "requiredVillage": None,
        "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives(t), "sceneBackground": SCENE_BG, "sceneCharacters": [SALVAGER],
                    "entryItems": [{"ids": [SALVAGE], "number": t["price"]}], "isolated": False, "reward": {}},
    }


def grant_70():
    s = {"sceneBackground": SCENE_BG, "sceneCharacters": []}
    return {"content": {
        "objectives": [
            {"id": "d_grant", "task": "dialog", **s, "description": "\"Test haul. Take it.\"",
             "nextObjectiveId": [{"text": "Take the salvage", "nextObjectiveId": "w_grant"}]},
            {"id": "w_grant", "task": "win_quest", **s, "description": "Seventy pieces of salvage.",
             "reward_items": [pay(SALVAGE, 70)]}],
        "sceneBackground": SCENE_BG, "sceneCharacters": [], "entryItems": [], "isolated": False, "reward": {}},
        "description": "Test only. The salvager hands over seventy pieces of salvage.",
        "successDescription": "Seventy salvage, as promised."}


def write(path, m):
    with open(os.path.join(ROOT, path), "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(path, len(m["items"]))


def build():
    items = [{"entity": "item", "slot": "edit", "targetId": SALVAGE, "phase": 1,
                  "name": "Wreck Salvage: description (one salvager NPC)",
                  "data": {"description": "<i>Brass fittings, glass shards and rope pulled out of the Skyglass "
                                          "Wreck.</i><br><br>The salvager trades charts for it."}}]
    items += [{"entity": "quest", "slot": "create", "srcId": "sg542_" + t["key"], "phase": 2, "name": t["name"],
               "data": quest(t, False)} for t in TIERS]
    items.append({"entity": "quest", "slot": "edit", "targetId": GRANT_QID, "phase": 2,
                  "name": "Salvage Swap Test: Grant pays 70 (test only)", "data": grant_70()})
    write("push/542_salvager_trade.json", {
        "_note": "push/542, HIDDEN. The Salvager's Trade: four trade quests (deck 4, hold 10, sealed 20 weekly, "
                 "Lantern 30 weekly L80), built as mastery with no prerequisite for the hidden test on dauntless; "
                 "543 makes them overworld with Wreck Sighted as prerequisite. Also Wreck Salvage description and "
                 "the test grant topped up to 70. Generated by push/salvager_trade.gen.py; do not hand-edit.",
        "dedupNames": True, "items": items})


def final(ids):
    items = [{"entity": "quest", "slot": "edit", "targetId": ids[t["key"]], "phase": 1,
              "name": f"{t['name']}: overworld, needs Wreck Sighted",
              "data": quest(t, True)} for t in TIERS]
    write("push/543_salvager_trade_final.json", {
        "_note": "push/543, HIDDEN. The four Salvager's Trade quests from 542 become questType overworld (handed out "
                 "by the salvager NPC on daily rolls) with prerequisiteQuestId Wreck Sighted, sent as the full record so the sealed trade's 'the The Last Heading' line is fixed too. Still hidden until the "
                 "Nov 13 release. Generated by push/salvager_trade.gen.py --final; do not hand-edit.",
        "items": items})


if __name__ == "__main__":
    if "--final" in sys.argv:
        final(json.load(open(os.path.join(ROOT, "push/542_ids.json"))))
    else:
        build()
