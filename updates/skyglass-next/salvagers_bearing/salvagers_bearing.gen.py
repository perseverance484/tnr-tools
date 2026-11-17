#!/usr/bin/env python3
"""Salvager's Bearing (working name): a daily crew hunt on the sector 210 beach that doubles as the Wrecks' signpost.

Lane B content. Director's idea (2026-11-17 00:06Z): "a daily each day that makes players travel to the wreck and beat
3 of the crew wandering the wreck. That could serve as the sign post and wouldnt need to be on wake island". Delivery
revised to his follow-up (01:23Z): "make it a daily with the prerequisite Wreck Sighted? Then it appears daily for
everyone who has activated the event and it gets hidden on weekend close". Everything ships HIDDEN; no live write
without his go.

    python3 salvagers_bearing.gen.py --weekend 2026-11-21
        -> salvagers_bearing_00_clone_plan.json     STEP 0: clone the original Wreck Sighted twice (hidden event)
        -> salvagers_bearing_build.TEMPLATE.json    STEP 1: edit both clones into the two band copies, hidden
                                                    (also the weekly re-arm: new dates, new Wreck Sighted ids)
        -> salvagers_bearing_release.TEMPLATE.json  STEP 2, Friday 6 PM CT: unhide both
        -> salvagers_bearing_close.TEMPLATE.json    STEP 3, after the Monday close: hide both
    Real ids: --quest-low/--quest-high (STEP 0 clones), --ws-low/--ws-high (that weekend's Wreck Sighted copies),
    --crew <placement id> [--crew <id> --crew <id>] (one, or one per fight).

HOW IT WORKS (TheNinjaRPG@94b585ead45826b3dc2f7b6720691d378efe8452, read 2026-11-17; read, not run)
  * Three defeat_opponents orders, in order, each BOUND to a beach crew placement (overworldPlacementId). Clicking a crew
    member of that placement on the map starts the quest fight (routers/overworldAi.ts 518-600; hostile placements may
    carry defeat bindings, libs/overworldAi.ts 509-517). The server fills opponentAIs from the placement on save
    (deriveOverworldOpponents, libs/overworldAi.ts 642-668): one placement = one opponent per fight. defeat_opponents
    has no kill count, so "beat 3" is three orders. A bound order completes only through its placement, never by
    standing on its stored tile (libs/quest.ts 286-301). opponent_scaled_to_user true scales each fight to the player.
  * Signpost: each order has sector 210 and no hideLocation, so the world map marks sector 210 while any order is open
    (layout/Map.tsx 73-95).
  * Prerequisite: prerequisiteQuestId is ONE quest id, met when the player's history row for it has completed = 1
    (libs/quest/availability.ts 248-277). Wreck Sighted ships as two band copies, so the Bearing ships as two copies
    too, each pointing at its band's Wreck Sighted. Wreck Sighted is re-cloned every week, so each weekly re-arm points
    the copies at that week's ids.
  * Where it shows: as an event quest it is listed on the Administration Building board, filtered by
    isAvailableUserQuests: prerequisite, level, dates, hidden, daily cap (routers/quests.ts allianceBuilding ~370-390).
    retryDelay daily + maxCompletes 1 = once per UTC day (6 PM CT); after the reset it is back on the board for
    everyone who finished their band's Wreck Sighted. It is NOT put in logbooks each day: the player takes it from the
    board. Nothing in the source auto-assigns on a prerequisite (upsertQuestEntries ignores it), and questType "daily"
    is not an option: the midnight daily cron picks one random daily per rank/village/level from all of them and never
    checks a prerequisite (api/daily-quest/route.ts 75-95).
  * Never Forge-create it: a create starts as a hidden mission (queries/quests.ts insertQuestForCreate), and the save
    that turns a non-event into an event hands it to every player active in 7 days, any level, no prerequisite check
    (routers/quests.ts 990-1001). A clone of a hidden event quest stays a hidden event, so nothing is handed out
    (same pattern as push/600 and stolen_stores_pages/00_clone_plan.json).
  * Close: endsAt is the Monday close, and an expired, hidden or prerequisite-failed quest drops off the board and stops
    advancing in any logbook it is open in (getUserQuests runs the same availability check, libs/quest.ts 59-73). The
    STEP 3 hide is tidy-up on top.
  * maxAttempts 100: upstream allows -1 but our 45d contract has min 0. A lost fight goes to fail_quest (validate.py:
    no battle node without failObjectiveId), as in the live Salvager dailies.

DEPENDS ON the beach raiders (Stolen Stores design): the crew placements must exist before STEP 1 saves, because the
server derives each fight's opponent from its placement. And on that weekend's two Wreck Sighted copies.

OPEN (director's): reward (3 Wreck Salvage proposed), name, whether this replaces Short Rations (same job), the go for
each step. Do not hand-edit the outputs.
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

PH_QUEST = {"low": "PLACEHOLDERbearingLOW", "high": "PLACEHOLDERbearingHIGH"}
PH_WS = {"low": "PLACEHOLDERwreckSightedLOW", "high": "PLACEHOLDERwreckSightedHIGH"}
WS_ORIGINAL = "_zp1l7Y9a_77pgonAdsYx"  # the original Wreck Sighted: hidden event, the clone source
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
               "beach bare.<br><br><b>Beat 3 of the crew on the beach in sector 210.</b> Once a day, after Wreck Sighted. "
               "They fight at your level.")
SUCCESS = "Three of the crew lie in the sand. The salvager will hear about it."
LOST = "The crew drive you off the sand. Take it from the board again and go back."
ORDERS = [
    ("The Skyglass Wrecks lie in sector 210, and the crew walk the sand around them. Beat one. (1 of 3)", "One down."),
    ("Beat another of the crew on the beach in sector 210. (2 of 3)", "Two down."),
    ("One more of the crew in sector 210. (3 of 3)", "That's three."),
]

BANDS = {"low": ("Levels 30 to 80", 30, 80), "high": ("Level 81 and up", 81, 100)}
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


def record(band, crew, ws, starts, ends):
    label, lo, hi = BANDS[band]
    reward = {k: v for k, v in F.objective("dialog", id="x").items() if k.startswith("reward_")}
    reward.update(REWARD)
    return {
        "name": f"{NAME} ({label})", "image": ICON, "description": DESCRIPTION, "successDescription": SUCCESS,
        "questType": "event", "questRank": "D",
        "petTaskMinutes": None, "requiredLevel": lo, "requiredFarmingLevel": 0,
        "prerequisiteQuestId": ws, "tierLevel": None,
        "hidden": True, "consecutiveObjectives": True, "teamEnabled": False, "publicLocations": False,
        "requiredVillage": None, "requiredBloodlineId": None, "requiredSageModeId": None, "requiredSageRank": None,
        "requiredNinjutsuMastery": None, "requiredGenjutsuMastery": None, "requiredTaijutsuMastery": None,
        "requiredBukijutsuMastery": None, "requiredBloodlineMastery": None, "requiredSageMastery": None,
        "maxLevel": hi, "maxAttempts": 100, "maxCompletes": 1,
        "retryDelay": "daily", "attemptDelay": "none", "startsAt": starts, "endsAt": ends,
        "raidBossMaxHealth": None, "raidBossCurrentHealth": None,
        "content": {"objectives": objectives(crew), "sceneBackground": SHORE, "sceneCharacters": [SALVAGER],
                    "entryItems": [], "isolated": False, "rewardMode": "all", "rewardPickCount": 1,
                    "reward": reward},
    }


def write(name, note, entries=None, calls=None):
    man = {"_note": note, **(F.manifest(entries) if entries is not None else {"calls": calls})}
    with open(os.path.join(HERE, name), "w") as f:
        json.dump(man, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote", name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weekend", required=True, help="the Saturday the Wrecks open (00:00 UTC), YYYY-MM-DD")
    ap.add_argument("--quest-low", help="STEP 0 clone for Levels 30 to 80")
    ap.add_argument("--quest-high", help="STEP 0 clone for Level 81 and up")
    ap.add_argument("--ws-low", help="that weekend's Wreck Sighted (Levels 30 to 80) id")
    ap.add_argument("--ws-high", help="that weekend's Wreck Sighted (Level 81 and up) id")
    ap.add_argument("--crew", action="append", help="crew placement id: once (all three fights) or three times")
    a = ap.parse_args()
    starts, ends = weekend(a.weekend)
    crew = a.crew or PH_CREW
    if len(crew) == 1:
        crew = crew * 3
    assert len(crew) == 3, "give --crew once or three times"
    qid = {"low": a.quest_low or PH_QUEST["low"], "high": a.quest_high or PH_QUEST["high"]}
    ws = {"low": a.ws_low or PH_WS["low"], "high": a.ws_high or PH_WS["high"]}
    real = all([a.crew, a.quest_low, a.quest_high, a.ws_low, a.ws_high])
    tag = "" if real else ".TEMPLATE"
    head = "" if real else "TEMPLATE, NOT RUNNABLE: quest, Wreck Sighted and placement ids are placeholders. "
    gen = " Generated by updates/skyglass-next/salvagers_bearing/salvagers_bearing.gen.py; do not hand-edit."

    write("salvagers_bearing_00_clone_plan.json",
          f"STEP 0 (director's go; connector, or the Clone button in the quest editor). Clone the ORIGINAL Wreck "
          f"Sighted {WS_ORIGINAL} twice: it is a hidden event quest and a clone keeps both, so nothing is handed out. "
          f"Never Forge-create {NAME}: turning a new quest into an event hands it to every active player. Then "
          "regenerate with --quest-low/--quest-high." + gen,
          calls=[{"endpoint": "quests.clone", "input": {"id": WS_ORIGINAL}, "expect": f"new id -> --quest-{b}"}
                 for b in ("low", "high")])
    write(f"salvagers_bearing_build{tag}.json",
          head + f"STEP 1 (director's go): edit both STEP 0 clones into {NAME}, HIDDEN event, rank D, one per band, "
          f"each needing its band's Wreck Sighted. Three bound crew fights on the sector 210 beach, scaled to the "
          f"player, daily, window {starts}..{ends}. Needs the crew placements to exist first. Also the weekly "
          "re-arm: regenerate with the new --weekend and that week's --ws-low/--ws-high, run it hidden." + gen,
          [F.entry("quest", "edit", targetId=qid[b], name=f"{NAME} ({BANDS[b][0]})",
                   data=record(b, crew, ws[b], starts, ends)) for b in ("low", "high")])
    write(f"salvagers_bearing_release{tag}.json",
          head + f"STEP 2, at the Friday 6 PM CT release, director's go: unhide both copies of {NAME}. From then on "
          "it is on the Administration Building board, once a day, for every player who finished their band's "
          "Wreck Sighted. Run after that weekend's Wreck Sighted copies are live." + gen,
          [F.entry("quest", "edit", targetId=qid[b], name=f"{NAME} ({BANDS[b][0]}): unhide",
                   data={"hidden": False}) for b in ("low", "high")])
    write(f"salvagers_bearing_close{tag}.json",
          head + f"STEP 3, after the Monday 6 PM CT close (endsAt already stops it): hide both copies of {NAME}."
          + gen,
          [F.entry("quest", "edit", targetId=qid[b], name=f"{NAME} ({BANDS[b][0]}): hide",
                   data={"hidden": True}) for b in ("low", "high")])


if __name__ == "__main__":
    main()
