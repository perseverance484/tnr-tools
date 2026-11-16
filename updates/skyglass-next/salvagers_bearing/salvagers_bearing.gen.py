#!/usr/bin/env python3
"""Salvager's Bearing: a daily signpost quest that puts a marker on sector 210 for anyone carrying it.

Lane B content, director's spec (2026-11-16 23:31Z). Everything ships HIDDEN; no live write without his go.

    python3 salvagers_bearing.gen.py --weekend 2026-11-21
        -> salvagers_bearing.TEMPLATE.json   (both band EDITs, targetIds placeholders: plan/validate only, not runnable)
    python3 salvagers_bearing.gen.py --weekend 2026-11-21 --id-shallows <clone A> --id-deep <clone B>
        -> salvagers_bearing_manifest.json   (the same EDITs aimed at the real clones, hidden:true)
    python3 salvagers_bearing.gen.py --weekend 2026-11-28 --id-shallows <A> --id-deep <B> --redate [--live]
        -> salvagers_bearing_redate_<date>.json  (next weekend's window, same full records)

TWO BAND COPIES, ONE OBJECTIVE EACH. The spec put both Wrecks side by side at 15/6 and 16/6 (SKYGLASS_EVENT_MAP.md),
but a live read (coop.dungeon.getAll, 2026-11-16 ~23:50Z) puts them apart: Faded Skyglass Wreck j4QEUtjbK_lbOYUPVoidk
at sector 210 7/1 and Skyglass Wreck RHqzYdY4EAQA9HwsBKWDS at sector 210 21/6, matching the live Wreck Sighted text
(push/615) and the map remake (map210 build3.py FADED=(7,1) SKY=(21,6)). One tile cannot be both Wrecks, so each band
gets its own copy pointing at the Wreck it can enter: Shallows (30-80) -> 7/1, the 81+ copy -> 21/6. The map marker is
per sector, so both still light up sector 210; the tile only decides where the order completes.

WHY A CLONE AND NOT A CREATE (TheNinjaRPG@94b585ea server/api/routers/quests.ts 990-1001): a quests.update that turns
a non-event quest into an event bulk-assigns it to every active user of the rank band, hidden or not. Forge's create
slot is quests.create (questType mission) then quests.update, so it would fire exactly that. Same path the Salvager
dailies took (release_nov13/dailies/dailies.gen.py, variant A):
  STEP 0 (run-lock holder, live, director's go): quests.clone {id: jUQYz9zyMdJIRdLbucYjm} twice. Each clone keeps
         questType event and hidden true and assigns nobody. jUQYz9zyMdJIRdLbucYjm is the clone SOURCE ONLY.
  STEP 1: rerun this with --id-shallows/--id-deep and run the edits (full records; questType event throughout).

ENGINE FACTS (read at TheNinjaRPG@94b585ead45826b3dc2f7b6720691d378efe8452, 2026-11-16; read, not run):
  * World-map markers (layout/Map.tsx 73-95): for each active user quest, every objective that has a sector, is not
    hideLocation, is not a dialog and is not done gets a marker on its sector. Hover shows the quest name, the goal
    title ("Travel" for move_to_location, libs/objectives.ts 458) and the objective description (plain text, 2 lines).
    Markers draw only when the player's location is known and the ownership overlay is off (Map.tsx 100-101).
  * Arrival: move_to_location completes when the player stands on sector + longitude/latitude
    (libs/quest.ts 853-860, isObjectiveLocationSatisfied). One objective, consecutive: the quest is complete when
    it is done (libs/objectives.ts 146-164), and the quest reward pays on the Logbook claim.
  * retryDelay "daily" = maxCompletes completions per UTC day (utils/time.ts 410-423 periodStart: 00:00 UTC,
    6 PM Central; libs/quest/availability.ts 237-246, 341-359). So maxCompletes 1 = once a day.
  * maxAttempts is a LIFETIME cap for event quests (availability.ts 228-234, QuestTypesWithMaxAttempts includes
    event). Upstream accepts QUEST_LIMIT_UNLIMITED = -1 (validators/objectives.ts 941), but our 45d contract has
    maxAttempts min 0 and the factory refuses -1, so we send 100 like the dailies: 100 days is longer than the event.
  * Event quests are taken from the Administration Building board (Wake Island) and listed by quests.getEvents
    (routers/quests.ts 365-385); up to 4 active event quests at once (libs/quest/missionHall.ts 185-204).
  * startsAt/endsAt are SQL DATEs: open 00:00 UTC on startsAt, close 00:00 UTC on endsAt
    (push/skyglass_journal.gen.py docstring). Wrecks open Fri 6 PM CT = Sat 00:00 UTC and close Mon 6 PM CT =
    Tue 00:00 UTC, so a weekend window is startsAt Saturday, endsAt Tuesday.

TILES: the live dungeon records above. SKYGLASS_EVENT_MAP.md, push/366 and push/skyglass_wreck.gen.py still carry
the pre-remake 15/6 and 16/6; they are history, not the live map. If the map moves the Wrecks again, change TILES.

OPEN (director's): reward (placeholder below), two band copies vs one quest, weekly window vs whole-event dates, icon.
Do not hand-edit the outputs.
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

CLONE_SOURCE = "jUQYz9zyMdJIRdLbucYjm"  # The Salvager's Trade: A Sealed Chart (event, hidden). Clone source only.
PLACEHOLDERS = {"shallows": "PLACEHOLDERbearingSHAL", "deep": "PLACEHOLDERbearingDEEP"}
# Live dungeon tiles (coop.dungeon.getAll, 2026-11-16): Faded j4QEUtjbK_lbOYUPVoidk, Skyglass RHqzYdY4EAQA9HwsBKWDS
BANDS = {
    "shallows": dict(name="Salvager's Bearing (Shallows)", wreck="Faded Skyglass Wreck", lvl=(30, 80),
                     tile={"sector": 210, "longitude": 7, "latitude": 1}),
    "deep": dict(name="Salvager's Bearing", wreck="Skyglass Wreck", lvl=(81, 100),
                 tile={"sector": 210, "longitude": 21, "latitude": 6}),
}
SHORE = "rX78pJPETsUL2JrsSvGHn"      # the shore scene (Wreck Sighted, the dailies)
SALVAGER = "Xugt7415D3-tepLfxpwM5"   # the salvager scene character
# Placeholder art, reused live uploads (no image job): the Watch Log page icon (QI01). A new icon is an open item.
ICON = "https://ui0arpl8sm.ufs.sh/f/4xb_93fgzp68t83owGoQQ.webp"

OBJECTIVE_TEXT = "The Skyglass Wrecks lie in sector 210. Gather a crew of three and board."  # director's words


def description(wreck):
    return ("The salvager has scratched a bearing on a strip of sailcloth: a line from wherever you stand to the "
            "beach where the Ghost Ship came down. Carry it, and your map will show you the way.<br><br>"
            f"<b>Go to the {wreck} in sector 210.</b> Once a day.")

SUCCESS = "The Wrecks loom over the sand. The bearing has done its job for today."

# --- director's calls; placeholders until he picks --------------------------------------------------------------------
GATE = dict(questRank="D", retryDelay="daily", maxCompletes=1, maxAttempts=100,
            prerequisiteQuestId=None)
REWARD = {"reward_money": 1000}  # PROPOSED, awaiting the director: 1,000 ryo on the daily claim


def weekend(sat):
    d = datetime.date.fromisoformat(sat)
    assert d.weekday() == 5, f"{sat} is not a Saturday (the Wrecks open 00:00 UTC Saturday = Fri 6 PM CT)"
    return d.isoformat(), (d + datetime.timedelta(days=3)).isoformat()  # Tuesday 00:00 UTC = Mon 6 PM CT


def objectives(band):
    o = F.objective("move_to_location", id="m_wrecks", description=OBJECTIVE_TEXT,
                    successDescription=f"You stand in the shadow of the {band['wreck']}.",
                    sectorType="specific", locationType="specific", hideLocation=False, image=ICON, **band["tile"])
    return [o]


def record(band, starts, ends, hidden=True):
    reward = {k: v for k, v in F.objective("dialog", id="x").items() if k.startswith("reward_")}
    reward.update(REWARD)
    return {
        "name": band["name"], "image": ICON, "description": description(band["wreck"]), "successDescription": SUCCESS,
        "questType": "event", "questRank": GATE["questRank"],
        "petTaskMinutes": None, "requiredLevel": band["lvl"][0], "requiredFarmingLevel": 0,
        "prerequisiteQuestId": GATE["prerequisiteQuestId"], "tierLevel": None,
        "hidden": hidden, "consecutiveObjectives": True, "teamEnabled": False, "publicLocations": False,
        "requiredVillage": None, "requiredBloodlineId": None, "requiredSageModeId": None, "requiredSageRank": None,
        "requiredNinjutsuMastery": None, "requiredGenjutsuMastery": None, "requiredTaijutsuMastery": None,
        "requiredBukijutsuMastery": None, "requiredBloodlineMastery": None, "requiredSageMastery": None,
        "maxLevel": band["lvl"][1], "maxAttempts": GATE["maxAttempts"], "maxCompletes": GATE["maxCompletes"],
        "retryDelay": GATE["retryDelay"], "attemptDelay": "none", "startsAt": starts, "endsAt": ends,
        "raidBossMaxHealth": None, "raidBossCurrentHealth": None,
        "content": {"objectives": objectives(band), "sceneBackground": SHORE, "sceneCharacters": [SALVAGER],
                    "entryItems": [], "isolated": False, "rewardMode": "all", "rewardPickCount": 1,
                    "reward": reward},
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--weekend", required=True, help="the Saturday the Wrecks open (00:00 UTC), YYYY-MM-DD")
    ap.add_argument("--id-shallows", help="clone id from STEP 0 for the 30-80 copy")
    ap.add_argument("--id-deep", help="clone id from STEP 0 for the 81+ copy")
    ap.add_argument("--redate", action="store_true", help="a later weekend: same records, new window")
    ap.add_argument("--live", action="store_true", help="with --redate: hidden false (only on the director's go)")
    a = ap.parse_args()
    starts, ends = weekend(a.weekend)
    ids = {"shallows": a.id_shallows, "deep": a.id_deep}
    real = all(ids.values())
    assert real or not any(ids.values()), "give both clone ids or neither"
    hidden = not (a.redate and a.live)
    entries = []
    for key, band in BANDS.items():
        tid = ids[key] or PLACEHOLDERS[key]
        assert tid != CLONE_SOURCE, "never edit the clone source"
        t = band["tile"]
        label = (f"{band['name']} (daily, event, L{band['lvl'][0]}-{band['lvl'][1]}, 210 {t['longitude']}/{t['latitude']}, "
                 f"{'hidden' if hidden else 'LIVE'}, {starts} to {ends})")
        entries.append(F.entry("quest", "edit", targetId=tid, name=label, data=record(band, starts, ends, hidden)))
    note = ("Salvager's Bearing, two band copies, each one move_to_location order with hideLocation false so the world "
            "map marks sector 210 for anyone carrying it: Shallows L30-80 -> Faded Skyglass Wreck 210 7/1; L81-100 -> "
            "Skyglass Wreck 210 21/6 (live dungeon tiles, read 2026-11-16). questType event, retryDelay daily, "
            f"maxCompletes 1, maxAttempts 100, rank D, no prerequisite, window {starts} 00:00 UTC to {ends} 00:00 UTC "
            f"(the Wrecks' weekend). Reward PROPOSED: {REWARD}. EDITS two clones of {CLONE_SOURCE} (STEP 0) so the "
            "non-event->event bulk assignment never fires. Generated by "
            "updates/skyglass-next/salvagers_bearing/salvagers_bearing.gen.py; do not hand-edit.")
    if not real:
        note = "TEMPLATE, NOT RUNNABLE: targetIds are placeholders until STEP 0 (quests.clone x2) runs. " + note
    man = {"_note": note, **F.manifest(entries)}
    out = ("salvagers_bearing.TEMPLATE.json" if not real else
           f"salvagers_bearing_redate_{starts}.json" if a.redate else "salvagers_bearing_manifest.json")
    with open(os.path.join(HERE, out), "w") as f:
        json.dump(man, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote", out)


if __name__ == "__main__":
    main()
