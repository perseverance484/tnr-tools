#!/usr/bin/env python3
"""Salvager's Bearing (working name): a daily crew hunt on the sector 210 beach that doubles as the Wrecks' signpost.

Lane B content. Director's idea (2026-11-17 00:06Z): "a daily each day that makes players travel to the wreck and beat
3 of the crew wandering the wreck. That could serve as the sign post and wouldnt need to be on wake island". It replaces
the first draft (one move_to_location order taken from the board). Everything ships HIDDEN; no live write without his go.

    python3 salvagers_bearing.gen.py --weekend 2026-11-21
        -> salvagers_bearing_build.TEMPLATE.json    STEP 1: create the quest hidden, as a MISSION (assigns nobody)
        -> salvagers_bearing_release.TEMPLATE.json  STEP 2, Friday 6 PM CT: edit A flips it to EVENT, unhidden
                                                    (this hands it to every active player), edit B sets rank D
        -> salvagers_bearing_rearm.TEMPLATE.json    STEP 3, before each later Friday: back to MISSION, hidden
    Real ids: --quest <id from STEP 1> and --crew <placement id> [--crew <id> --crew <id>] (one, or one per fight).

HOW IT WORKS (TheNinjaRPG@94b585ead45826b3dc2f7b6720691d378efe8452, read 2026-11-17; read, not run)
  * Three defeat_opponents orders, in order, each BOUND to a beach crew placement (overworldPlacementId). Clicking a crew
    member of that placement on the map starts the quest fight (routers/overworldAi.ts 518-600; hostile placements may
    carry defeat bindings, libs/overworldAi.ts 509-517). The server fills opponentAIs from the placement on save
    (deriveOverworldOpponents, libs/overworldAi.ts 642-668): one placement = one opponent per fight. defeat_opponents
    has no kill count, so "beat 3" is three orders. A bound order completes only through its placement, never by
    standing on its stored tile (libs/quest.ts 286-301).
  * opponent_scaled_to_user true: the bound fight scales the crew member to the player (scaleTarget, overworldAi.ts
    ~570). So ONE quest serves both bands, 30 to 100, and the band's Wreck tiles don't matter.
  * Signpost: each order has sector 210 and no hideLocation, so the world map marks sector 210 while any order is open
    (layout/Map.tsx 73-95; hover shows the quest name, "Defeat" and the order text). Unlike the first draft, the marker
    stays up until the third fight, not just until arrival.
  * Delivery without the board: flipping a quest from non-event to event assigns it to every user active in the last
    7 days whose rank is in availableRanks(questRank) (routers/quests.ts 990-1001; libs/rank.ts 56-78). It ignores level.
    questRank S covers all six ranks, so edit A uses S. Board visibility runs the other way
    (availableQuestLetterRanks: S is Jonin and up only), so edit B, a plain re-save with questType still event, sets
    rank D so everyone can re-take it. A re-save does not assign again. The flip also reopens rows of players who did
    it before (server/utils/questAssignment.ts upsertQuestEntries), which is what makes the weekly re-arm work.
  * Daily: retryDelay daily, maxCompletes 1 = once per UTC day (6 PM CT). After day one, a player re-takes it from the
    Administration Building board. No source path auto-assigns an event quest every day: event quests can't come from
    an NPC (OVERWORLD_ASSIGNABLE_QUEST_TYPES, overworldAi.ts 862-867), and questType "daily" is one random pick a day
    from every visible daily (api/daily-quest/route.ts 75-95; 7 exist today, only one for 81+), so it isn't reliable.
  * maxAttempts 100: upstream allows -1 but our 45d contract has min 0.
  * A lost fight goes to fail_quest (validate.py: no battle node without failObjectiveId), the same ending the live
    Salvager dailies use. Flee and draw count as a loss (completionOutcome Win).

DEPENDS ON the beach raiders (Stolen Stores design): the crew placements must exist before STEP 1 saves, because the
server derives each fight's opponent from its placement. Placement ids are placeholders until then.

OPEN (director's): reward (3 Wreck Salvage proposed), name, whether this replaces Short Rations (same job), that the
flip also reaches players under 30, the go for each step. Do not hand-edit the outputs.
"""
import argparse
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SKILL = os.environ.get("TNR_SKILL_SCRIPTS") or os.path.join(ROOT, "skills", "building-tnr-content", "scripts")
sys.path.insert(0, SKILL)
from factory import Factory  # noqa: E402

F = Factory(ctors=os.path.join(ROOT, "45c_DATA_constructors.json"),
            entities=os.path.join(ROOT, "skills", "building-tnr-content", "data", "45d_DATA_entity_schemas.json"),
            checks=os.path.join(ROOT, "45g_DATA_checks.json"))

PH_QUEST = "PLACEHOLDERbearingQUEST"
PH_CREW = ["PLACEHOLDERcrewPLACE01", "PLACEHOLDERcrewPLACE02", "PLACEHOLDERcrewPLACE03"]
PH_CREW_AI = "PLACEHOLDERcrewAI0001"  # replaced by the server from the placement on save
SALVAGE = "mW6_ZGtGcCSuXGPhn-H4o"     # Wreck Salvage
SHORE = "rX78pJPETsUL2JrsSvGHn"       # the shore scene
SALVAGER = "Xugt7415D3-tepLfxpwM5"    # the salvager scene character
ICON = "https://ui0arpl8sm.ufs.sh/f/4xb_93fgzp68t83owGoQQ.webp"  # placeholder: the Watch Log page icon
# Stored tile on each order: the Salvager's fire (live read 210 14/7). Bound orders never use it to complete; it only
# keeps the location fields real (law 54).
TILE = {"sector": 210, "longitude": 14, "latitude": 7}

NAME = "Salvager's Bearing"
DESCRIPTION = ("The Quartermaster's crew have come ashore in sector 210. They walk the sand around the Skyglass Wrecks "
               "as if they were still on watch, and the salvager wants three of them put down before they strip the "
               "beach bare.<br><br><b>Beat 3 of the crew on the beach in sector 210.</b> Once a day. They fight at "
               "your level.")
SUCCESS = "Three of the crew lie in the sand. The salvager will hear about it."
LOST = "The crew drive you off the sand. Try again tomorrow, or take it from the board again today."
ORDERS = [
    ("The Skyglass Wrecks lie in sector 210, and the crew walk the sand around them. Beat one. (1 of 3)", "One down."),
    ("Beat another of the crew on the beach in sector 210. (2 of 3)", "Two down."),
    ("One more of the crew in sector 210. (3 of 3)", "That's three."),
]

LEVELS = (30, 100)
REWARD = {"reward_items": [{"ids": [SALVAGE], "number": 100, "quantity": 3}]}  # PROPOSED: 3 Wreck Salvage a day


def weekend(sat):
    d = datetime.date.fromisoformat(sat)
    assert d.weekday() == 5, f"{sat} is not a Saturday (the Wrecks open 00:00 UTC Saturday = Fri 6 PM CT)"
    return d.isoformat(), (d + datetime.timedelta(days=3)).isoformat()


def objectives(crew):
    out = []
    for i, (text, done) in enumerate(ORDERS):
        out.append(F.objective("defeat_opponents", id=f"d{i + 1}", description=text, successDescription=done,
                               overworldPlacementId=crew[i], opponentAIs=[{"ids": [PH_CREW_AI], "number": 1}],
                               opponent_scaled_to_user=True, completionOutcome="Win",
                               nextObjectiveId=f"d{i + 2}" if i < 2 else "w_done", failObjectiveId="f_lost",
                               **TILE))
    # Same ending pair as the live Salvager dailies (push/600): a win pays, a loss ends today's try.
    for task, oid, text, chars in (("win_quest", "w_done", SUCCESS, [SALVAGER]), ("fail_quest", "f_lost", LOST, [])):
        out.append(F._build("AllObjectives", "InstantWinLoseObjective",
                            dict(task=task, id=oid, description=text, sceneBackground=SHORE,
                                 sceneCharacters=chars), disc="task"))
    return out


def record(crew, starts, ends, quest_type, rank, hidden):
    reward = {k: v for k, v in F.objective("dialog", id="x").items() if k.startswith("reward_")}
    reward.update(REWARD)
    return {
        "name": NAME, "image": ICON, "description": DESCRIPTION, "successDescription": SUCCESS,
        "questType": quest_type, "questRank": rank,
        "petTaskMinutes": None, "requiredLevel": LEVELS[0], "requiredFarmingLevel": 0,
        "prerequisiteQuestId": None, "tierLevel": None,
        "hidden": hidden, "consecutiveObjectives": True, "teamEnabled": False, "publicLocations": False,
        "requiredVillage": None, "requiredBloodlineId": None, "requiredSageModeId": None, "requiredSageRank": None,
        "requiredNinjutsuMastery": None, "requiredGenjutsuMastery": None, "requiredTaijutsuMastery": None,
        "requiredBukijutsuMastery": None, "requiredBloodlineMastery": None, "requiredSageMastery": None,
        "maxLevel": LEVELS[1], "maxAttempts": 100, "maxCompletes": 1,
        "retryDelay": "daily", "attemptDelay": "none", "startsAt": starts, "endsAt": ends,
        "raidBossMaxHealth": None, "raidBossCurrentHealth": None,
        "content": {"objectives": objectives(crew), "sceneBackground": SHORE, "sceneCharacters": [SALVAGER],
                    "entryItems": [], "isolated": False, "rewardMode": "all", "rewardPickCount": 1,
                    "reward": reward},
    }


def write(name, note, entries):
    man = {"_note": note, **F.manifest(entries)}
    with open(os.path.join(HERE, name), "w") as f:
        json.dump(man, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote", name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weekend", required=True, help="the Saturday the Wrecks open (00:00 UTC), YYYY-MM-DD")
    ap.add_argument("--quest", help="the quest id STEP 1 created")
    ap.add_argument("--crew", action="append", help="crew placement id: once (all three fights) or three times")
    a = ap.parse_args()
    starts, ends = weekend(a.weekend)
    crew = a.crew or PH_CREW
    if len(crew) == 1:
        crew = crew * 3
    assert len(crew) == 3, "give --crew once or three times"
    real_crew = bool(a.crew)
    qid = a.quest or PH_QUEST
    tag = "" if (real_crew and a.quest) else ".TEMPLATE"
    head = "" if tag == "" else "TEMPLATE, NOT RUNNABLE: placement/quest ids are placeholders. "
    gen = " Generated by updates/skyglass-next/salvagers_bearing/salvagers_bearing.gen.py; do not hand-edit."

    write(f"salvagers_bearing_build{tag}.json",
          head + f"STEP 1 (director's go): create {NAME} HIDDEN as a MISSION, so saving it assigns nobody. Three bound "
          f"crew fights on the sector 210 beach, scaled to the player, L{LEVELS[0]}-{LEVELS[1]}, daily, window "
          f"{starts}..{ends}. Needs the crew placements to exist first." + gen,
          [F.entry("quest", "create", name=NAME,
                   data=record(crew, starts, ends, "mission", "D", True))])
    write(f"salvagers_bearing_release{tag}.json",
          head + f"STEP 2, at the Friday 6 PM CT release, director's go: edit A flips {NAME} to EVENT, rank S, "
          "UNHIDDEN. That save ASSIGNS IT TO EVERY PLAYER ACTIVE IN THE LAST 7 DAYS, all ranks, any level "
          "(routers/quests.ts 990-1001): the signpost. Edit B re-saves rank D (no second assignment) so every rank "
          "can re-take it from the board on later days." + gen,
          [F.entry("quest", "edit", targetId=qid, name=f"{NAME} A: flip to event, rank S, live (assigns everyone)",
                   data=record(crew, starts, ends, "event", "S", False)),
           F.entry("quest", "edit", targetId=qid, name=f"{NAME} B: rank D for the board, live",
                   data=record(crew, starts, ends, "event", "D", False))])
    write(f"salvagers_bearing_rearm{tag}.json",
          head + f"STEP 3, any time before a later Friday: {NAME} back to MISSION, hidden, with that weekend's "
          f"dates ({starts}..{ends}). Then STEP 2 again with the same --weekend: the flip reopens and reassigns it."
          + gen,
          [F.entry("quest", "edit", targetId=qid, name=f"{NAME}: re-arm as mission, hidden",
                   data=record(crew, starts, ends, "mission", "D", True))])


if __name__ == "__main__":
    main()
