#!/usr/bin/env python3
"""Skyglass event journal: one Watch Log page per weekend. Each page is two jobs:

    python3 push/skyglass_journal.gen.py --page N             -> the page's create, HIDDEN (PAGES[N]["num"])
    python3 push/skyglass_journal.gen.py publish --page N --from <create results bundle>
                                                              -> the publish edit (PAGES[N]["publish_num"])
    (page 1 is the default and reproduces push/490 exactly; --friday overrides a page's weekend. endsAt is the
     Tuesday after, so a page closes 00:00 UTC Tuesday = Monday evening US, RUL-2026-11-05-122 item 2)

EVERY ORDER OPEN AT ONCE (RUL-2026-11-08-139). The create must carry consecutiveObjectives:true (Forge L03, law 23),
but a chained page shows players only its first order: the engine walks a consecutive chain one link per tracker
pass and skips every order off the walked path, so they neither show nor count (TheNinjaRPG libs/objectives.ts
isQuestObjectiveAvailable; libs/quest.ts, the availability skip before any task matching). Week 1 went live that way
and the director set it to false in the editor on 2026-11-07. So the publish edit sends consecutiveObjectives:false
with hidden:false. That is safe here because a page has no win_quest, dialog or battle node (law 23's danger): only
tracker and location orders, and a non-consecutive quest completes when every order is done (isQuestComplete).

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
  * Forge L03 refuses a quest create without consecutiveObjectives:true (forge/src/runner/lints.mjs 77). The create
    keeps the entries in one chain for that; the publish edit turns the chain off (see above). No ending node: with
    every order live, a final dialog or win_quest would be live from the start, not after the entries. The ending is
    the engine's own: the claim that resolves the page shows "Finished: <name>" with successDescription and the
    completion reward (layout/Logbook.tsx 903-931).
  * Each objective's reward pays once when the player claims it in the Logbook (libs/quest.ts 494-497); the
    quest-level reward pays when every entry is done.
  * Dates are SQL DATEs (drizzle/schema.ts 4333-4334): a page opens 00:00 UTC on its startsAt and closes 00:00 UTC on its endsAt
    (routers/quests.ts 2682-2687; libs/quest.ts 2456-2459; queries/quests.ts 1384-1385).

Page 1 rewards approved as drafted (RUL-2026-11-05-121 D3); each later page's rewards are the director's, listed in
its PAGES entry with their status. Image: page 1 packs the QI01 icon; later pages reuse its live upload, so they run
over the connector with no image job. Do not hand-edit the output.
"""
import argparse
import datetime
import hashlib
import json
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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
# Item ids for use_specific_item_combat orders (live reads):
USE = {
    "skyglass_serum": "XhilCv1Hq4eNt-Wddok-m",  # Skyglass Serum: CONSUMABLE, heal, SELF (item.get 2026-11-08)
}
# Reward items (state/skyglass_design/design_data.json). Values approved as drafted (RUL-2026-11-05-121 D3).
I = {
    "tide_chart": "H1s2IwtZ5JqgPEoJ55IVj",
    "medicine_inro": "ixEKlJ0MmDrX7JoMNJVhi",
    "archive_chart_case": "B48dTRsoLJGKBWIUbeUoG",
    "skyglass_coffer": "THo7rfzP-S82_43aN8fs3",
    "sealed_treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
    "skyglass_token": "nzCW7A-_AuYMzBs2wClnM",
    "galley_stores": "D-QTnbjgTyIVc593zzdSB",
}
SALVAGER = "Xugt7415D3-tepLfxpwM5"  # scene character, push/374 (tnr_results_1793502324082.json idmap sg374_salvager)
BG = "rX78pJPETsUL2JrsSvGHn"  # Wreck Sighted's shore scene, as the asset id push/385 sends (live record)
ICON = "art/skyglass_journal/exports/icon-quest-watch-log.webp"  # QI01, the director's generation (2026-11-06), preflight 0/0
IMG = "@img:" + os.path.basename(ICON)
ICON_LIVE = "https://ui0arpl8sm.ufs.sh/f/4xb_93fgzp68t83owGoQQ.webp"  # QI01 as uploaded by push/490 (live read 2026-11-07)
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


def entries_page1():
    return [
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


def entries_page2():
    """The Rotted Heading: the rot, from the helm to the burning heading (EVENT_JOURNAL.md section 5)."""
    return [
        entry("j2_helm", "complete_specific_quest",
              "Stand the captain's own watch on the helm deck. She still keeps it.",
              "<b>Win The Captain's Watch once.</b>",
              ("archive_chart_case", "an Archive Chart Case"),
              "The helm is quiet. Whatever she saw from it, she did not tell you.",
              completeQuestIds=runs("captains_watch"), value=1),
        entry("j2_serum", "use_specific_item_combat",
              "Drink what the night watch drank, and keep standing.",
              "<b>Drink a Skyglass Serum in battle once.</b> Any chart run counts; fights inside the Wreck dungeons "
              "do not.",
              ("medicine_inro", "a Medicine Inro"),
              "Seal-light closes the cut. It tastes of salt and old lamp oil.",
              useItemIds=[USE["skyglass_serum"]], value=1),
        entry("j2_fall", "complete_specific_quest",
              "Live through the night she fell, and climb back out.",
              "<b>Win The Fall once.</b>",
              ("galley_stores", "Galley Stores"),
              "You came back up. The crew who rode her down did not.",
              completeQuestIds=runs("fall"), value=1),
        entry("j2_rot_seal", "complete_specific_quest",
              "Open the reliquary after the rot got in.",
              "<b>Win The Rotted Reliquary once.</b> Its seal comes from steeping a Reliquary Seal with 3 Core Rot.",
              ("skyglass_coffer", "a Skyglass Coffer"),
              "The reliquary is open. What grew inside it is not.",
              completeQuestIds=runs("rotted_reliquary"), value=1),
        entry("j2_burning", "complete_specific_quest",
              "Follow the rotted heading the wrong way, through the fire.",
              "<b>Win The Burning Heading once.</b> The Rotted Heading comes from steeping The Last Heading with 3 "
              "Core Rot.",
              ("sealed_treasury", "a Sealed Treasury"),
              "The heading burns out in your hand. Somewhere below, the glass rings again.",
              completeQuestIds=runs("burning_heading"), value=1),
    ]


def chained(objs):
    for a, b in zip(objs, objs[1:]):  # Forge L03 on the create; the publish edit sets consecutiveObjectives false
        a["nextObjectiveId"] = b["id"]
    return objs


PAGE1_INTRO = ("The salvager has dried a page of the Ghost Ship's watch log and weighted it under a stone for you. It "
               "is one watch's orders, in the officer's brush. Your name is written in at the top, in the same ink.")
PAGE2_INTRO = ("The second page came up from the deep hold, and the rot has been at it. Half the officer's brush is "
               "eaten through, and what is left points down, to the rooms the Core spoiled. Your name is at the top "
               "again, in the same ink.")

PAGES = {
    1: {"num": 490, "out": "push/490_skyglass_journal_week1.json", "srcId": "sg490_journal_w1",
        "name": "The Watch Log: First Page", "friday": "2026-11-06", "entries": entries_page1, "intro": PAGE1_INTRO,
        "success": ("Page complete. Every order is answered, and the salvager folds the page into her coat with the "
                    "others. \"The next tide brings the next page.\""),
        "image": "pack", "publish_num": 507},
    2: {"num": 512, "out": "push/512_skyglass_journal_page2.json", "srcId": "sg512_journal_p2",
        "publish_num": 513, "publish_out": "push/513_skyglass_journal_page2_publish.json",
        "name": "The Watch Log: Second Page", "friday": "2026-11-13", "entries": entries_page2, "intro": PAGE2_INTRO,
        "success": ("Page complete. The rot stops at your name. The salvager reads it twice before she folds it away. "
                    "\"That one came up from further down than the last.\""),
        "image": "live", "rewards": "DRAFT, awaiting the director (RUL-2026-11-05-121 D3 covered page 1 only)"},
}


def plain_list(objs):
    return "".join(f"<br>{n}. {o['description'].split('<br><br>', 1)[1].split(' Reward when')[0]}"
                   for n, o in enumerate(objs, 1))


NUMWORD = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}


def quest(page, objs, friday):
    starts = ends = None
    if friday:
        d = datetime.date.fromisoformat(friday)
        assert d.weekday() == 4, f"{friday} is not a Friday"
        starts, ends = d.isoformat(), (d + datetime.timedelta(days=4)).isoformat()
    n = len(objs)
    desc = (f"This weekend's orders: {n} to claim, a Skyglass Token for all {NUMWORD[n]}.<br><br>"
            + page["intro"] + "<br><br><i>" + "<br>".join(o["description"].split("<br><br>", 1)[0].split(". ")[0].rstrip(".") + "."
                                              for o in objs) + "</i><br><br>"
            f"<b>This weekend's orders</b>, in any order:{plain_list(objs)}<br><br>"
            "Orders count only while you carry this page: nothing you did before taking it counts. Claim each order's "
            f"reward in the Logbook when it is done, and finish all {n} for the page's last reward, a Skyglass Token. The page "
            "closes at the end of Monday (00:00 UTC Tuesday), so claim before then. Claiming the last order completes "
            "the page.")
    return {"entity": "quest", "slot": "create", "srcId": page["srcId"], "phase": 1,
            "name": page["name"],
            "data": {"name": page["name"], "description": desc, "image": IMG if page["image"] == "pack" else ICON_LIVE,
                     "questType": "event", "questRank": "D",
                     "successDescription": page["success"],
                     "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
                     "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 1, "maxCompletes": 1,
                     "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None,
                     "requiredBloodlineId": None, "startsAt": starts, "endsAt": ends,
                     "content": {"objectives": objs, "sceneBackground": BG, "sceneCharacters": [SALVAGER],
                                 "entryItems": [],
                                 "reward": {"reward_items": reward("skyglass_token")}}}}


def pack(path):
    """imagePack pinned to the newest commit touching the icon; the working copy must equal that commit."""
    ref = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", path], text=True).strip()
    disk = open(os.path.join(ROOT, path), "rb").read()
    assert ref and subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{path}"]) == disk, f"{path}: commit it first"
    name = os.path.basename(path)
    return {"imgSizes": {name: len(disk)},
            "imagePack": {"ref": ref, "files": {name: {"path": path, "sha256": hashlib.sha256(disk).hexdigest(),
                                                       "bytes": len(disk)}}}}


def note_for(n, page, q, objs):
    if n == 1:  # the record as it ran (push/490); kept byte-for-byte
        return (f"push/{page['num']}, HIDDEN. The Skyglass event journal, week 1 (docs/design/EVENT_JOURNAL.md; RUL-2026-11-05-120, "
                f"-121): one event quest, {len(objs)} tracker entries in one chain (consecutive for Forge L03; all live at "
                "once, so any order), per-entry rewards on claim and a Skyglass Token on completion (approved, D3). Window "
                f"{q['data']['startsAt']} 00:00 UTC to {q['data']['endsAt']} 00:00 UTC (D4; RUL-2026-11-05-122 item 2). No Wreck entry (D1). Lands in the "
                "Administration Building and the profile dashboard's Events cards (D2). The QI01 page icon is packed (imagePack). Staff test: take it, "
                "reload, win a Low Tide Run; the Logbook should show 1/2. Generated by push/skyglass_journal.gen.py; do not "
                "hand-edit.")
    return (f"push/{page['num']}, HIDDEN. {page['name']} (docs/design/EVENT_JOURNAL.md section 5): one event quest, "
            f"{len(objs)} orders, per-order rewards on claim and a Skyglass Token on completion. Rewards: "
            f"{page['rewards']}. Window {q['data']['startsAt']} 00:00 UTC to {q['data']['endsAt']} 00:00 UTC. The create "
            "carries consecutiveObjectives true for Forge L03; push/" + str(page["publish_num"]) + " (built from this "
            "job's results bundle) publishes it with every order open at once (RUL-2026-11-08-139). Icon: the live QI01 "
            "upload, so no image job. Runs over the connector. Generated by push/skyglass_journal.gen.py --page "
            f"{n}; do not hand-edit.")


def build_create(n, friday):
    page = PAGES[n]
    objs = chained(page["entries"]())
    q = quest(page, objs, friday or page["friday"])
    out = {"_note": note_for(n, page, q, objs)}
    if page["image"] == "pack":
        out.update(pack(ICON))
    out["items"] = [q]
    path = os.path.join(ROOT, page["out"])
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{page['out']}: 1 quest create (hidden), {len(objs)} entries")


def build_publish(n, bundle):
    """The publish edit: the committed create data, whole, with hidden false and every order open at once."""
    page = PAGES[n]
    if "publish_out" not in page:
        raise SystemExit(f"page {n} was published by push/{page['publish_num']}; nothing to build")
    m = json.load(open(os.path.join(ROOT, page["out"])))
    b = json.load(open(bundle if os.path.isabs(bundle) else os.path.join(ROOT, bundle)))
    (it,) = m["items"]
    ok = [e for e in b.get("entries", []) if e.get("state") == "ok" and e.get("slot") == "create"
          and e.get("entity") == "quest" and e.get("name") == it["name"]]
    if len(ok) != 1:
        raise SystemExit(f"{bundle}: expected one ok create of {it['name']!r}")
    data = dict(it["data"], hidden=False, consecutiveObjectives=False)
    out = {"_note": (f"push/{page['publish_num']}: publish {page['name']} ({ok[0]['id']}, created by push/{page['num']}). "
                     "Re-sends the committed create data whole with hidden false and consecutiveObjectives false, so "
                     "every order is open at once (RUL-2026-11-08-139); the page still lists only from its startsAt. "
                     f"Built from {os.path.basename(bundle)} by push/skyglass_journal.gen.py publish; do not hand-edit."),
           "items": [{"entity": "quest", "slot": "edit", "targetId": ok[0]["id"], "phase": 10,
                      "name": f"{it['name']}: publish", "data": data}]}
    path = os.path.join(ROOT, page["publish_out"])
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{page['publish_out']}: publish {it['name']} -> {ok[0]['id']}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", nargs="?", default="create", choices=["create", "publish"])
    ap.add_argument("--page", type=int, default=1, choices=sorted(PAGES))
    ap.add_argument("--friday", help="override the page's weekend start (a Friday); endsAt is the Tuesday after")
    ap.add_argument("--from", dest="bundle", help="publish: the create job's results bundle")
    a = ap.parse_args()
    if a.mode == "publish":
        if not a.bundle:
            ap.error("publish needs --from <results bundle>")
        build_publish(a.page, a.bundle)
    else:
        build_create(a.page, a.friday)


if __name__ == "__main__":
    main()
