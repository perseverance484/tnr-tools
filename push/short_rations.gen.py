#!/usr/bin/env python3
"""Stolen Stores: Short Rations, the Salvager's new shore daily, all HIDDEN until release.

    python3 push/short_rations.gen.py test       # write push/637: create Short Rations (mastery, hidden) for the staff test
    python3 push/short_rations.gen.py final --quest <id>   # write push/638: switch it to overworld (still hidden)
    python3 push/short_rations.gen.py release --quest <id> # write push/639: RELEASE ONLY (Friday), not run here

Design of record: Stolen Stores design doc rev 33 (Short Rations: "beat 3 Looting Deckhands and a Quartermaster's
Mate in sector 210 for 3 Wreck Salvage", once a day from level 30). The director, 2026-11-18 18:31 and 18:33 UTC:
"Short Rations goes on the dailies for the Salvager not on the Wake Island board" and "It can go in her daily pool.
Just make it an overworld quest like the others and slot it in at 20%. Subtract 20% from the quest with the highest
rate currently". The others are plain quest fights (start_battle, scaled to the player), so this one is too; it is
modelled on her live Beachcombing daily (read back live 2026-11-18).

Why three stages:
- Overworld quests can only be started from their NPC, and her pool is full (40/30/20/10 = 100). So the hidden staff
  test runs it as a mastery quest first (push/637), then push/638 switches the type to overworld, still hidden.
- Chances are absolute bands: a hidden quest drops out for players but its band does not move to anyone else. Cutting
  Beachcombing 40 to 20 now would make 20% of live players' rolls grant nothing until Friday. So the pool change and
  the unhide are push/639, for the Friday release only.

Flagged for the director (not settled here): reward_exp 1000 matches Beachcombing (not in the doc); icon is a
PLACEHOLDER (Galley Stores) until the Short Rations icon is painted.
Do not hand-edit the output.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")

PLACEMENT = "goagM4WhKWtnVb8oP5euM"  # The Salvager, sector 210 (live read 2026-11-18)
SALVAGER_CHAR = "Xugt7415D3-tepLfxpwM5"  # Beachcombing d_tide sceneCharacters
FIRE_SCENE = "rX78pJPETsUL2JrsSvGHn"
BEACH = "https://ui0arpl8sm.ufs.sh/f/QfsAnXSp9QG0AuwbQywCW.webp"  # Beachcombing battle/win scene
ICON = "https://ui0arpl8sm.ufs.sh/f/iS35oVeCsybzoJYcfJ2xp.webp"  # placeholder: Galley Stores icon
SALVAGE = "mW6_ZGtGcCSuXGPhn-H4o"
DECKHAND, MATE = "MVy7rX2FW9mvGQJNXUKCH", "veKt6fjJqqdDBRJyYiTOT"  # push/633-634 (hidden)
BEACHCOMBING = "5faJqlDvs8jXTv1zN8B8m"
POOL_LIVE = [(BEACHCOMBING, 40), ("5ZksRGBaMmzG49EtzugNX", 20), ("ejD1-13fEZupXUU8tf8Au", 30),
             ("sbssALiuyJVTApe8ZpLvp", 10)]  # live read 2026-11-18
EXP = 1000
NAME = "Short Rations"
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the tide takes the way back.",
          "fleeDescription": "You break away, and the tide closes behind you.", "completionOutcome": "Win",
          "scaleGains": 1, "keepOriginalPools": False, "opponent_scaled_to_user": True, "failObjectiveId": "f_lost",
          "sceneCharacters": []}
DESC = ("The tide keeps leaving the Wreck's crew on the Salvager's beach, and they keep dragging her crates back to the "
        "hull as if it were still their watch. Thin them out: 3 Looting Deckhands and a Quartermaster's Mate, for "
        "3 Wreck Salvage.<br><br><i>Ask the Salvager at her fire on the beach below the Wreck (sector 210). Enemies "
        "match your level. You start each fight at full health, chakra and stamina. Lose one and the job ends.</i>")


def objectives():
    return [
        {"id": "d_ask", "task": "dialog", "sceneBackground": FIRE_SCENE, "sceneCharacters": [SALVAGER_CHAR],
         "overworldPlacementId": PLACEMENT,
         "description": "\"Thin them out and I'll pay you. My crates, my sand.\" Down the beach, two deckhands are "
         "hauling one of her crates toward the hull, in step, without a word.",
         "nextObjectiveId": [{"text": "Cut them off", "nextObjectiveId": "b1"}]},
        {"id": "b1", "task": "start_battle", "sceneBackground": BEACH, "nextObjectiveId": "d_mate",
         "description": "They set the crate down and turn to you, the way they'd turn to an order.",
         "opponentAIs": [{"ids": [DECKHAND], "number": 2, "quantity": 1}], **SHARED},
        {"id": "d_mate", "task": "dialog", "sceneBackground": BEACH, "sceneCharacters": [],
         "description": "Further along the tideline a Quartermaster's Mate is counting crates off a list, and a third "
         "deckhand is stacking them. Neither looks up.",
         "nextObjectiveId": [{"text": "Take the list off him", "nextObjectiveId": "b2"}]},
        {"id": "b2", "task": "start_battle", "sceneBackground": BEACH, "nextObjectiveId": "w_done",
         "description": "The Mate closes his list and calls the stack to order.",
         "opponentAIs": [{"ids": [MATE], "number": 1, "quantity": 1}, {"ids": [DECKHAND], "number": 1, "quantity": 1}],
         **SHARED},
        {"id": "w_done", "task": "win_quest", "sceneBackground": BEACH, "sceneCharacters": [],
         "description": "Her crates stay on her sand, for today. You bring back what they were hauling.",
         "reward_exp": EXP, "reward_items": [{"ids": [SALVAGE], "number": 100, "quantity": 3}]},
        {"id": "f_lost", "task": "fail_quest", "sceneBackground": BEACH, "sceneCharacters": [],
         "description": "The crew carry on past you as if you were never there. The tide will turn again tomorrow."},
    ]


def quest_data(qtype):
    return {
        "name": NAME, "description": DESC, "image": ICON, "questType": qtype, "questRank": "D",
        "successDescription": "You kept her crates on her sand.",
        "retryDelay": "daily", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
        "requiredLevel": 30, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 20,
        "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
        "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives(), "sceneBackground": FIRE_SCENE, "sceneCharacters": [SALVAGER_CHAR],
                    "entryItems": [], "isolated": False, "rewardMode": "all", "rewardPickCount": 1, "reward": {}}}


def check_graph(objs):
    ids = {o["id"] for o in objs}
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
    deck = sum(a["number"] for o in objs for a in o.get("opponentAIs", []) if a["ids"] == [DECKHAND])
    mate = sum(a["number"] for o in objs for a in o.get("opponentAIs", []) if a["ids"] == [MATE])
    assert (deck, mate) == (3, 1), (deck, mate)  # the doc: 3 Deckhands and a Mate


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/short_rations.gen.py; do not hand-edit.", "dedupNames": True}
    m.update(extra or {})
    m["items"] = items
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items), "items")


def main():
    for v in [PLACEMENT, SALVAGER_CHAR, FIRE_SCENE, SALVAGE, DECKHAND, MATE] + [q for q, _ in POOL_LIVE]:
        assert NANO.match(v), v
    assert sum(c for _, c in POOL_LIVE) == 100
    check_graph(objectives())
    assert "—" not in DESC
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "test":
        write(637, "short_rations_create", "push/637, HIDDEN: create Short Rations as a mastery quest so the staff "
              "account can play it (overworld quests only start from their NPC, and her pool is full until Friday).",
              [{"entity": "quest", "slot": "create", "srcId": "sr637_quest", "phase": 1, "name": NAME,
                "data": quest_data("mastery")}])
        return
    qid = sys.argv[sys.argv.index("--quest") + 1] if "--quest" in sys.argv else ""
    assert NANO.match(qid), "--quest <id> required"
    if mode == "final":
        write(638, "short_rations_overworld", "push/638, HIDDEN: switch Short Rations to the overworld type, its "
              "final form. Still hidden and in no pool.",
              [{"entity": "quest", "slot": "edit", "targetId": qid, "phase": 1,
                "name": "Short Rations: questType overworld (hidden)", "data": {"questType": "overworld",
                                                                                "hidden": True}}])
        return
    if mode == "release":
        # Forge has no overworld placement entity (forge/src/runner/manifest.mjs ENTITIES), so the pool change is a
        # direct overworldAi.upsertPlacement call. That endpoint takes the whole placement (every field required,
        # pool as "quests"), so the payload is the 2026-11-18 live read with only the pool changed.
        cap = json.load(open(os.path.join(ROOT, "state", "stolen_stores_captures", "salvager_placement_2026-11-18.json")))
        live = cap["record"]
        assert live["id"] == PLACEMENT and live["updatedAt"] == "2026-11-09T16:53:23.734Z"
        assert [(q["questId"], q["chance"]) for q in live["questPool"]] == POOL_LIVE
        pool = [(q, c - 20 if q == BEACHCOMBING else c) for q, c in POOL_LIVE] + [(qid, 20)]
        assert sum(c for _, c in pool) == 100
        write(639, "short_rations_release", "push/639, RELEASE ONLY (Friday Nov 20, with the director's go): unhide "
              "Short Rations. Then run push/639_salvager_pool_upsert.json (a direct connector call, not Forge).",
              [{"entity": "quest", "slot": "edit", "targetId": qid, "phase": 1, "name": "Short Rations: unhide",
                "data": {"hidden": False}}], {"_release_only": True})
        keep = ["aiTemplateUserId", "interactionType", "sectorType", "locationType", "sector", "longitude", "latitude",
                "sectorList", "isActive", "wanderRadius", "spawnCount", "groupMin", "groupMax", "habitats",
                "wildOnly", "mapScale"]
        data = {k: live[k] for k in keep}
        data["quests"] = [{"questId": q, "chance": c} for q, c in pool]
        call = {"_note": "RELEASE ONLY (Friday Nov 20, with the director's go), after push/639 has unhidden Short "
                         "Rations: overworldAi.upsertPlacement for the Salvager. Pool +Short Rations 20%, Beachcombing "
                         "40% to 20%; every other field is the 2026-11-18 live read. Re-read the placement first "
                         "(overworldAi.getPlacementsForAi) and stop if anything but this pool differs; read it back "
                         "after. Generated by push/short_rations.gen.py; do not hand-edit.",
                "_release_only": True, "endpoint": "overworldAi.upsertPlacement",
                "input": {"id": PLACEMENT, "data": data}}
        path = os.path.join(ROOT, "push", "639_salvager_pool_upsert.json")
        with open(path, "w") as f:
            json.dump(call, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(os.path.relpath(path, ROOT), "connector call")
        return
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
