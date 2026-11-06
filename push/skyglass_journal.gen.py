#!/usr/bin/env python3
"""Skyglass event journal, week 1: "The Watch Log: First Page". One event quest create, HIDDEN.

    python3 push/skyglass_journal.gen.py                      -> push/490_skyglass_journal_week1.json
    (--friday YYYY-MM-DD overrides the weekend; default 2026-11-06, the release, RUL-2026-11-05-121 D4)

Design: docs/design/EVENT_JOURNAL.md (the journal pattern and the Skyglass rotation). Zero live requests.

Engine facts this build rests on (theninjarpg@3314d122, read, not run; full citations in EVENT_JOURNAL.md section 2):
  * complete_specific_quest credits once per active -> completed transition of a listed quest, increment 1, so a
    value of 2 means "two wins in total" (libs/quest.ts 677-693, 1584-1595, 1884). Failed runs do not resolve.
  * Trackers exist only for quests the player has active (getNewTrackers iterates getUserQuests, libs/quest.ts
    1038-1074): nothing done before the journal is taken counts.
  * Dungeon battles and the dungeon reward claim emit no tracker task (libs/combat/database.ts 1206;
    server/api/routers/dungeon.ts 466-472), and dungeons_completed is a lifetime count (libs/quest.ts 1403-1406;
    server/utils/achievementObjectives.ts 56-61). Wreck clears stay off the pages until upstream tracks them
    (RUL-2026-11-05-121 D1).
  * Forge L03 refuses a quest create without consecutiveObjectives:true (forge/src/runner/lints.mjs 77). A chain of
    non-dialog objectives is all live from its first node (references/quest.md appendix section 2), so the entries
    still count in any order, and the quest resolves only when every node on the walked path is done
    (libs/objectives.ts 110-140). No ending node: availability walks links and never checks done
    (libs/objectives.ts 151-186; libs/quest.ts 1655-1662), so a final dialog or win_quest would be live from the
    start, not after the entries. The ending is the engine's own: the claim that resolves the page shows
    "Finished: <name>" with successDescription and the completion reward (layout/Logbook.tsx 903-931).
  * Each objective's reward pays once when the player claims it in the Logbook (libs/quest.ts 494-497); the
    quest-level reward pays when every entry is done.
  * Dates are SQL DATEs (drizzle/schema.ts 4333-4334): a page opens 00:00 UTC Friday and closes 00:00 UTC Monday
    (routers/quests.ts 2682-2687; libs/quest.ts 2456-2459; queries/quests.ts 1384-1385).

Rewards approved as drafted (RUL-2026-11-05-121 D3). Still open: the image (placeholder: Wreck Sighted's) and the
Wreck coordinates (sector 210, x 15, y 6: carried assumption that longitude is x). Do not hand-edit the output.
"""
import argparse
import datetime
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = 490
OUT = os.path.join(ROOT, f"push/{NUM}_skyglass_journal_week1.json")

# Live quest ids, from harvested results bundles (harvests/inbox):
Q = {
    "low_tide": "pFQBaJxU_8RSvSi4Kir1Z",        # The Low Tide Run      tnr_results_1793485965044.json
    "night_watch": "dnzL-bDrAEVXrKB5xariu",     # The Night Watch       tnr_results_1793485965044.json
    "buried_cache": "CgwAVCyZLgNQtEnqgLxxv",    # The Buried Cache      design_data picks; tnr_results_1793490827321.json
    "foundry": "UGHSuhi83C3wRtH3FD4Eu",         # The Drowned Foundry   tnr_results_1793490827321.json
    "archive": "-bZ_ZoI6yrUJ_LKT9R5zm",         # The Quarantined Archive tnr_results_1793491138913.json
    "captains_watch": "liljq0yVXWTSna4X6dZE1",  # The Captain's Watch   tnr_results_1793490827321.json
    "reliquary": "yZoR_dPSdg8ksO77gDH_A",       # The Sealed Reliquary  tnr_results_1793485978739.json
    "fall": "H9YInJtnzKCOEMv-sNgzP",            # The Fall              tnr_results_1793485978739.json
    "rotted_reliquary": "FsuXzvaqr_R25p8cEkxoK",  # The Rotted Reliquary tnr_results_1793485978739.json
    "burning_heading": "ozDN-G6nGFXGgKuPZ04Gr",   # The Burning Heading  tnr_results_1793485978739.json
    "crownhold": "fqqpkcp_L4oOsC6yyodlk",       # Crownhold             tnr_results_1793424666625.json
}
# Reward items (state/skyglass_design/design_data.json). Values approved as drafted (RUL-2026-11-05-121 D3).
I = {
    "tide_chart": "H1s2IwtZ5JqgPEoJ55IVj",
    "medicine_inro": "ixEKlJ0MmDrX7JoMNJVhi",
    "archive_chart_case": "B48dTRsoLJGKBWIUbeUoG",
    "skyglass_coffer": "THo7rfzP-S82_43aN8fs3",
    "sealed_treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
    "skyglass_token": "nzCW7A-_AuYMzBs2wClnM",
}
SALVAGER = "Xugt7415D3-tepLfxpwM5"  # scene character, push/374 (tnr_results_1793502324082.json idmap sg374_salvager)
BG = "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJyX6gwPukVH2MI5Lo4ehEfAXvZdcmtWqPg7rp"  # Wreck Sighted's shore scene
IMG = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # PLACEHOLDER (Wreck Sighted's)
WRECK = {"sector": 210, "longitude": 15, "latitude": 6}  # endgame Wreck tile (SKYGLASS_EVENT_MAP.md N2); x/y assumed


def reward(item):
    return [{"ids": [I[item]], "number": 100, "quantity": 1}]


def entry(oid, task, voice, plain, rew, success, **fields):
    o = {"id": oid, "task": task,
         "description": f"{voice}<br><br>{plain} Reward when you claim it: {rew[1]}.",
         "successDescription": success, "sceneBackground": "", "sceneCharacters": [],
         "reward_items": reward(rew[0])}
    o.update(fields)
    return o


def runs(*keys):
    return [Q[k] for k in keys]


def entries():
    out = [
        entry("j_tideline", "move_to_location",
              "Walk the tideline where she lies. The page's first order is only to look at her.",
              "<b>Go to the Skyglass Wreck</b> (sector 210).",
              ("tide_chart", "a Tide Chart"),
              "You stand in her shadow. The crew on deck do not look down.",
              sectorType="specific", locationType="specific", hideLocation=False, **WRECK),
        entry("j_low_watch", "complete_specific_quest",
              "Stand two low watches: the breach the low tide opens, and the night roster with your name on it.",
              "<b>Win the Low Tide Run or the Night Watch, 2 times in total.</b>",
              ("medicine_inro", "a Medicine Inro"),
              "Two watches stood. The roster has a mark beside your name.",
              completeQuestIds=runs("low_tide", "night_watch"), value=2),
        entry("j_crew_chart", "complete_specific_quest",
              "Follow one of the crew's own charts below the waterline: what they buried, the works, the archive "
              "or the helm.",
              "<b>Win one of these runs once:</b> The Buried Cache, The Drowned Foundry, The Quarantined Archive or "
              "The Captain's Watch.",
              ("archive_chart_case", "an Archive Chart Case"),
              "The chart led where it said it would. Not every chart aboard her does.",
              completeQuestIds=runs("buried_cache", "foundry", "archive", "captains_watch"), value=1),
        entry("j_core_hold", "complete_specific_quest",
              "Go down where the Core could not hold them: to the reliquary, or to the night she fell.",
              "<b>Win one of these runs once:</b> The Sealed Reliquary, The Fall, The Rotted Reliquary or The "
              "Burning Heading.",
              ("skyglass_coffer", "a Skyglass Coffer"),
              "You have seen what the Core kept, and what it could not.",
              completeQuestIds=runs("reliquary", "fall", "rotted_reliquary", "burning_heading"), value=1),
        entry("j_last_light", "complete_specific_quest",
              "Carry the last light home. The lantern still points the way to Crownhold.",
              "<b>Win Crownhold once</b> (its way in is a Lastlight Lantern).",
              ("sealed_treasury", "a Sealed Treasury"),
              "Crownhold's signal goes dark behind you. Somewhere below the throne, glass rings once.",
              completeQuestIds=runs("crownhold"), value=1),
    ]
    for a, b in zip(out, out[1:]):  # Forge L03: one chain; non-dialog nodes are all live from the start
        a["nextObjectiveId"] = b["id"]
    return out


def plain_list(objs):
    return "".join(f"<br>{n}. {o['description'].split('<br><br>', 1)[1].split(' Reward when')[0]}"
                   for n, o in enumerate(objs, 1))


def quest(objs, friday):
    starts = ends = None
    if friday:
        d = datetime.date.fromisoformat(friday)
        assert d.weekday() == 4, f"{friday} is not a Friday"
        starts, ends = d.isoformat(), (d + datetime.timedelta(days=3)).isoformat()
    n = len(objs)
    desc = ("The salvager has dried a page of the Ghost Ship's watch log and weighted it under a stone for "
            "you. It is one watch's orders, in the officer's brush. Your name is written in at the top, in the same "
            "ink.<br><br><i>" + "<br>".join(o["description"].split("<br><br>", 1)[0].split(". ")[0].rstrip(".") + "."
                                              for o in objs) + "</i><br><br>"
            f"<b>This weekend's orders</b>, in any order:{plain_list(objs)}<br><br>"
            "Orders count only while you carry this page: nothing you did before taking it counts. Claim each order's "
            f"reward in the Logbook when it is done, and finish all {n} for the page's last reward, a Skyglass Token. The page "
            "is gone "
            "when the weekend ends, so claim before then. Claiming the last order completes the page.")
    return {"entity": "quest", "slot": "create", "srcId": f"sg{NUM}_journal_w1", "phase": 1,
            "name": "The Watch Log: First Page",
            "data": {"name": "The Watch Log: First Page", "description": desc, "image": IMG,
                     "questType": "event", "questRank": "D",
                     "successDescription": ("Page complete. Every order is answered, and the salvager folds the page "
                                            "into her coat with the others. \"The next tide brings the next page.\""),
                     "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
                     "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 1, "maxCompletes": 1,
                     "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None,
                     "requiredBloodlineId": None, "startsAt": starts, "endsAt": ends,
                     "content": {"objectives": objs, "sceneBackground": BG, "sceneCharacters": [SALVAGER],
                                 "entryItems": [],
                                 "reward": {"reward_items": reward("skyglass_token")}}}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--friday", default="2026-11-06", help="weekend start (a Friday); endsAt is the Monday after")
    a = ap.parse_args()
    objs = entries()
    q = quest(objs, a.friday)
    note = (f"push/{NUM}, HIDDEN. The Skyglass event journal, week 1 (docs/design/EVENT_JOURNAL.md; RUL-2026-11-05-120, "
            f"-121): one event quest, {len(objs)} tracker entries in one chain (consecutive for Forge L03; all live at "
            "once, so any order), per-entry rewards on claim and a Skyglass Token on completion (approved, D3). Window "
            f"{q['data']['startsAt']} 00:00 UTC to {q['data']['endsAt']} 00:00 UTC (D4). No Wreck entry (D1). Lands in the "
            "Administration Building and the profile dashboard's Events cards (D2). Placeholder image. Staff test: take it, "
            "reload, win a Low Tide Run; the Logbook should show 1/2. Generated by push/skyglass_journal.gen.py; do not "
            "hand-edit.")
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"_note": note, "items": [q]}, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{os.path.relpath(OUT, ROOT)}: 1 quest create (hidden), {len(objs)} entries")


if __name__ == "__main__":
    main()
