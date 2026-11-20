#!/usr/bin/env python3
"""Job 674, HIDDEN: Stolen Stores story v2 text and Isonade's arms renamed to a hook tail.

    python3 push/stolen_stores_story_v2.gen.py   -> push/674_stolen_stores_story_v2.json

The director approved story v2 and said "Build now" (2026-11-20 15:39Z, relayed into the Isonade thread) for the
drafts in state/flooded_stores_build/stolen_stores_story_v2.md: the four text changes and arms to tail.

What it writes, every record hidden and staying hidden:
  law 18   Grasping Arm Rises comes off Isonade and Arm Lash comes off the Grasping Arm (phase 10), both jutsu are
           edited (20), both kits go back whole (30). Nothing else in either kit changes.
  jutsu    Grasping Arm Rises -> The Hook Tail Rises; Arm Lash -> Tail Lash (names, descriptions, battle text only).
  ai       Grasping Arm -> Hook Tail (username only, in the same edit that puts Tail Lash back on).
  quest    The Flooded Stores: run description, d_below, b4. Both Wreck Sighted copies: n_eat.
Content is sent whole from the live reads in CAP, changed only at those strings.

The release (push/673) is unaffected: it only sends {hidden: false} to these quests and touches none of the AI or jutsu.
Do not hand-edit the output.
"""
import copy
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAP = os.path.join(ROOT, "state/stolen_stores_captures/story_v2_live_2026-11-20")
DROP = {"id", "createdAt", "updatedAt"}

ISONADE = "K_lwNvMPJLMsn1sUGXqZm"
ARM_AI = "lJAnVI4eBn5YjCgghqBji"
RISES = "6w0MWbsSIB2j02MADv1nK"
LASH = "QMXGlGM34xcBfDLWfJYoB"
RUN = "-_1MdlGp-gxdiWKb6Bf3V"
WS = {"VRibCq0gip_otYBbWEX4J": "quest_wreck_sighted_30_80.json", "tYNgqctjx_5KIKbbOyApH": "quest_wreck_sighted_81.json"}
QUEST_TOP = ["name", "description", "successDescription", "image", "questType", "questRank", "requiredLevel",
             "maxLevel", "tierLevel", "prerequisiteQuestId", "requiredVillage", "requiredBloodlineId",
             "consecutiveObjectives", "maxAttempts", "maxCompletes", "retryDelay", "attemptDelay", "startsAt",
             "endsAt", "hidden", "content"]  # the shape push/672 sent and verified

RUN_DESC = ("Below the galley the Quartermaster still hands out rations, and his crew still carry in more. None of it "
            "stays down there long.\n\n3 fights · then take the stores, or go below for a 4th.\n\n"
            "Claim any reward choice still waiting from an earlier run before you set out.")
D_BELOW = ("The storeroom is half sea now. A crack runs the length of the floor, and the crates the crew carried in are "
           "floating out through it, one after another, into black water. Something down there is waiting for them.")
B4 = ("A fin cuts the black water. Then the whole shark comes up through the crack, a barbed hook of a tail lashing "
      "behind it.")
N_EAT = ("She pokes the fire. \"That crew don't eat. Old men on this coast talk about a shark with a hook for a tail. "
         "It takes men off boats. Seems it'll take biscuit too.\"")

RISES_TEXT = {"name": "The Hook Tail Rises",
              "description": "A barbed tail bursts up through the deck and lashes everything around it. Cut it, and "
                             "another grows.",
              "battleDescription": "The deck bursts upward. A barbed black tail hooks up out of it."}
LASH_TEXT = {"name": "Tail Lash", "description": "The barbed tail sweeps every hex around it.",
             "battleDescription": "The barbed tail lashes across the planks."}
ARM_NAME = "Hook Tail"


def cap(name):
    return json.load(open(os.path.join(CAP, name)))


def editable(rec):
    return {k: v for k, v in copy.deepcopy(rec).items() if k not in DROP}


def obj(q, oid):
    hit = [o for o in q["content"]["objectives"] if o["id"] == oid]
    assert len(hit) == 1, oid
    return hit[0]


def quest_edit(q, label):
    data = {k: copy.deepcopy(q[k]) for k in QUEST_TOP}
    assert data["hidden"] is True, q["id"]
    return {"entity": "quest", "slot": "edit", "targetId": q["id"], "phase": 40, "name": f"{q['name']}: {label}",
            "data": data}


def main():
    iso, arm = cap("getAi_isonade.json"), cap("getAi_grasping_arm.json")
    assert iso["userId"] == ISONADE and arm["userId"] == ARM_AI and arm["username"] == "Grasping Arm"
    iso_kit = [j["jutsuId"] for j in iso["jutsus"]]
    arm_kit = [j["jutsuId"] for j in arm["jutsus"]]
    assert len(iso_kit) == 19 and all(j["equipped"] for j in iso["jutsus"]) and RISES in iso_kit, iso_kit
    assert arm_kit == [LASH] and arm["jutsus"][0]["equipped"]
    assert [(i["itemId"], i["equipped"]) for i in iso["items"]] == [("ZBfu0h3K6U1g45Q4gTOG7", "CHEST")]

    rises, lash = cap("jutsu_grasping_arm_rises.json"), cap("jutsu_arm_lash.json")
    assert rises["id"] == RISES and rises["name"] == "Grasping Arm Rises" and rises["hidden"]
    assert lash["id"] == LASH and lash["name"] == "Arm Lash" and lash["hidden"]
    assert [e["aiId"] for e in rises["effects"] if e["type"] == "summon"] == [ARM_AI]
    rd, ld = editable(rises), editable(lash)
    rd.update(RISES_TEXT)
    ld.update(LASH_TEXT)

    run = cap("quest_flooded_stores.json")
    assert run["id"] == RUN and run["hidden"] and run["description"].startswith("Below the galley")
    run["description"] = RUN_DESC
    assert obj(run, "d_below")["description"].startswith("The storeroom is half sea now.")
    obj(run, "d_below")["description"] = D_BELOW
    assert obj(run, "b4")["description"] == "The water heaves, and one pale eye opens in it."
    obj(run, "b4")["description"] = B4

    items = [
        {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 10,
         "name": "Isonade: Grasping Arm Rises off for its rename (law 18)",
         "data": {"jutsus": [j for j in iso_kit if j != RISES]}},
        {"entity": "ai", "slot": "edit", "targetId": ARM_AI, "phase": 10,
         "name": "Grasping Arm: Arm Lash off for its rename (law 18)", "data": {"jutsus": []}},
        {"entity": "jutsu", "slot": "edit", "targetId": RISES, "phase": 20,
         "name": "Grasping Arm Rises -> The Hook Tail Rises (text only)", "data": rd},
        {"entity": "jutsu", "slot": "edit", "targetId": LASH, "phase": 20,
         "name": "Arm Lash -> Tail Lash (text only)", "data": ld},
        {"entity": "ai", "slot": "edit", "targetId": ISONADE, "phase": 30,
         "name": f"Isonade: full kit back ({len(iso_kit)})", "data": {"jutsus": iso_kit}},
        {"entity": "ai", "slot": "edit", "targetId": ARM_AI, "phase": 30,
         "name": "Grasping Arm -> Hook Tail, Tail Lash back on", "data": {"username": ARM_NAME, "jutsus": arm_kit}},
        quest_edit(run, "story v2 text (description, d_below, b4)"),
    ]
    for qid, f in WS.items():
        q = cap(f)
        assert q["id"] == qid
        n = obj(q, "n_eat")
        assert n["description"].startswith("She pokes the fire."), n["description"]
        n["description"] = N_EAT
        items.append(quest_edit(q, "n_eat story v2"))
    for it in items:
        s = json.dumps(it, ensure_ascii=False)
        assert "—" not in s and "–" not in s, it["name"]
    m = {"_note": ("push/674, HIDDEN: Stolen Stores story v2 text (The Flooded Stores description, d_below, b4; "
                   "Wreck Sighted n_eat x2) and Isonade's arms renamed to a hook tail (law 18 on Isonade and the "
                   "Grasping Arm). push/673 unaffected. Generated by push/stolen_stores_story_v2.gen.py; "
                   "do not hand-edit."),
         "items": items}
    out = os.path.join(ROOT, "push", "674_stolen_stores_story_v2.json")
    with open(out, "w") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print("wrote", os.path.relpath(out, ROOT), len(items), "items")


if __name__ == "__main__":
    main()
