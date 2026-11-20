#!/usr/bin/env python3
"""Stolen Stores: the two Watch Log pages, rebuilt around the new content. HIDDEN until release.

    python3 push/stolen_stores_pages.gen.py create            -> push/641: create both pages, HIDDEN (chained, L03)
    python3 push/stolen_stores_pages.gen.py open --from <641 results bundle>
                                                               -> push/642: every order open at once, still HIDDEN
    python3 push/stolen_stores_pages.gen.py release --from <641 results bundle>
                                                               -> push/643: RELEASE ONLY (Friday), not run here

The director's calls, 2026-11-18 (UTC), relayed in this thread:
  18:35 "Beat the Quartermaster once instead of Isonade. Isonade will probably be too tough for a level 50"
  18:44 "One regular crew win for shallows, one mate win for 81+. Can do short rations if needed. I thought these
         objectives only counted from the moment you took them, not past completions? Why would you need a new trade?"
  18:44 "Any chart counts"  (the chart order counts her existing Deck Charts trade, any pick; the Flooded Stores
         chart is added to that trade as a pick on Friday, push/644; no new trade)
Each order pays its reward plus 3 Wreck Salvage and the whole page pays a Skyglass Token, the live Shallows page
pattern (push/609, push/611).

Engine facts (theninjarpg@3314d122, read, not run):
  * complete_specific_quest credits one per successful resolution of a listed quest while the page is active
    (libs/quest.ts 677-693, 1038-1074); failed runs don't resolve, so a lost Flooded Stores run doesn't count.
  * defeat_opponents credits a win over any listed AI, in any fight, when the page has no entryItems and is not
    isolated (libs/quest.ts 1806-1840). So a Mate or Deckhand beaten in the run, in Short Rations, or on the beach
    counts, and one win closes the order. An order with no location never puts the player in a fight itself
    (the putInCombat call sits under isObjectiveLocationSatisfied, libs/quest.ts 1632-1780).
  * The create needs consecutiveObjectives true (Forge L03); push/642 turns it off so every order is open at once
    (RUL-2026-11-08-139), the same as the live pages.

Friday path (push/643): the live page 3 record (AgGR962c3XNo6Pr0up2qT, published, startsAt 2026-11-21, still the
old pre-split content) takes the tested 81+ data whole; the new Shallows record is unhidden with its window and
level cap. The 81+ staff-test copy stays hidden. For the staff test the Shallows record is open to level 100 and
both test records have no window (a page lists only from its startsAt).

Validator deviation: skills validate.py errors "battle node without failObjectiveId (re-arm loop)" on the three
defeat_opponents orders. That check is for location kill nodes, which re-arm a fight on every visit. These orders
have no location, so nothing re-arms; a lost fight just leaves the order open (libs/quest.ts 1840-1873 only moves
to failObjectiveId when one is set). A failObjectiveId would need a fail node, and on a page with every order open
that node would be live from the start. So the error is expected here; Forge's own plan reports no problems.

Location fix: push/641 ran before it and created the three kill orders with the server default, sector 0 at
(0,0), location shown and unscaled. push/642 sets them to sector 9999 (no such sector), hideLocation true and
opponent_scaled_to_user true, so they never place a fight and show no location.

Flagged for the director (not settled here): hooks and order text are drafts.
Do not hand-edit the output.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")

LIVE_PAGE3 = "AgGR962c3XNo6Pr0up2qT"  # The Watch Log: Stolen Stores (live read 2026-11-18: published, 2026-11-21..24)
RUN = "-_1MdlGp-gxdiWKb6Bf3V"  # The Flooded Stores (push/636, hidden)
SHORT_RATIONS = "Gqbnq2LVtIVBlLYlAnam1"  # push/637 (hidden)
DECK_TRADE = "zYhkIQeVGNUMljwev3-ud"  # The Salvager's Trade: Deck Charts (live)
DAILIES = ["5faJqlDvs8jXTv1zN8B8m", "5ZksRGBaMmzG49EtzugNX", "ejD1-13fEZupXUU8tf8Au", "sbssALiuyJVTApe8ZpLvp"]
DECKHAND, MATE, ISONADE = "MVy7rX2FW9mvGQJNXUKCH", "veKt6fjJqqdDBRJyYiTOT", "K_lwNvMPJLMsn1sUGXqZm"
I = {
    "tide_chart": ("H1s2IwtZ5JqgPEoJ55IVj", "a Tide Chart"),
    "flooded_chart": ("FuQzaFNlpyOUGlO5BtjyX", "a Chart of the Flooded Stores"),  # the director, 2026-11-20 16:19Z
    "medicine_inro": ("ixEKlJ0MmDrX7JoMNJVhi", "a Medicine Inro"),
    "archive_chart_case": ("B48dTRsoLJGKBWIUbeUoG", "an Archive Chart Case"),
    "skyglass_coffer": ("THo7rfzP-S82_43aN8fs3", "a Skyglass Coffer"),
    "sealed_treasury": ("Ma8S90Nmbi0Xvm4u4FzJh", "a Sealed Treasury"),
    "galley_stores": ("D-QTnbjgTyIVc593zzdSB", "Galley Stores"),
}
SALVAGE = "mW6_ZGtGcCSuXGPhn-H4o"
TOKEN = "nzCW7A-_AuYMzBs2wClnM"
SALVAGER = "Xugt7415D3-tepLfxpwM5"
BG = "rX78pJPETsUL2JrsSvGHn"
ICON_LIVE = "https://ui0arpl8sm.ufs.sh/f/4xb_93fgzp68t83owGoQQ.webp"  # the shared placeholder push/641 and 642 sent
# The director's own page icons (2026-11-20 15:58Z), uploaded hidden (state/isonade_upload/uploaded.json). push/675 sets
# the Shallows icon now; the release (643, in 673) carries both, so the 6 PM run does not put the placeholder back.
ICON_RELEASE = {"high": "https://bbenpyo9uu.ufs.sh/f/0tzd8oDeiVIzcskzL6UPdHh7Y96aCTrVbSFG1AXDBn25msqk",
                "low": "https://bbenpyo9uu.ufs.sh/f/0tzd8oDeiVIzDNk0fAljZC3QEWRynJO7qVdTs6zchxtIAL0b"}
FRIDAY_START, FRIDAY_END = "2026-11-21", "2026-11-24"  # 00:00 UTC Saturday (Friday 6 PM Central) to 00:00 UTC Tuesday

WHERE_RUN = "Every player gets its chart from Wreck Sighted, and the Salvager's Deck Charts trade has more."
WHERE_SR = "It's one of the Salvager's dailies in sector 210."


def entry(oid, task, voice, plain, rew, success, **fields):
    item, label = I[rew]
    o = {"id": oid, "task": task,
         "description": f"{voice}<br><br>{plain} Reward when you claim it: {label} and 3 Wreck Salvage.",
         "successDescription": success, "sceneBackground": "", "sceneCharacters": [],
         "reward_items": [{"ids": [item], "number": 100, "quantity": 1},
                          {"ids": [SALVAGE], "number": 100, "quantity": 3}]}
    o.update(fields)
    return o


def beat(ai):
    # The server defaults a defeat_opponents objective to sector 0 at (0,0), shown, which is a real tile where a
    # page holder walking onto it would be put in a fight. Sector 9999 does not exist (ids run 0..1943), so the
    # location never matches and never forces a fight; hideLocation keeps it off the Logbook and map.
    return {"opponentAIs": [{"ids": [ai], "number": 1, "quantity": 1}], "completionOutcome": "Win",
            "sectorType": "specific", "locationType": "specific", "sector": NOWHERE, "latitude": 0, "longitude": 0,
            "hideLocation": True, "opponent_scaled_to_user": True}


NOWHERE = 9999  # MAP_TOTAL_SECTORS = 72 x 27 = 1944; no sector has this id


def done(*qids, value=1):
    return {"completeQuestIds": list(qids), "value": value}


def page_high():
    return [
        entry("s3_mate", "defeat_opponents",
              "Take the list off one of the men still handing out rations.",
              "<b>Beat a Quartermaster's Mate once.</b> They crew The Flooded Stores and Short Rations.",
              "galley_stores", "His list falls open. Every line is the same ration, signed for twice.", **beat(MATE)),
        entry("s3_rations", "complete_specific_quest",
              "Keep her crates on her sand, two tides running.",
              f"<b>Finish Short Rations 2 times.</b> {WHERE_SR}",
              "flooded_chart", "Two tides, and her crates are still on her sand.", **done(SHORT_RATIONS, value=2)),
        entry("s3_trade", "complete_specific_quest",
              "Trade her what the sea gave you for one of the crew's charts.",
              "<b>Trade with her for a deck chart once.</b> Her Deck Charts trade costs 4 Wreck Salvage, and any "
              "chart you pick counts.",
              "skyglass_coffer", "She hands the chart over still damp.", **done(DECK_TRADE)),
        entry("s3_stores", "complete_specific_quest",
              "Go down to the stores twice, and come back up both times.",
              f"<b>Win The Flooded Stores 2 times,</b> either ending. {WHERE_RUN}",
              "archive_chart_case", "Twice down, twice back. The water was higher the second time.", **done(RUN, value=2)),
        entry("s3_isonade", "defeat_opponents",
              "Find what has been eating the stores, and drive it off.",
              "<b>Beat Isonade once.</b> It waits below the stores, in The Flooded Stores' last fight.",
              "sealed_treasury", "It slides back out through the crack in the hull. The ship settles.", **beat(ISONADE)),
    ]


def page_low():
    return [
        entry("s3s_crew", "defeat_opponents",
              "Run off one of the crew dragging her crates back to the hull.",
              "<b>Beat a Looting Deckhand once.</b> They crew The Flooded Stores and Short Rations.",
              "medicine_inro", "He drops the crate and walks back into the sea, still in step.", **beat(DECKHAND)),
        entry("s3s_dailies", "complete_specific_quest",
              "Work the shore the way she does.",
              "<b>Finish any 3 of the Salvager's dailies.</b> Short Rations counts. Find her in sector 210, by the "
              "Wrecks.",
              "galley_stores", "Three tides worked. She stops counting her crates when you're on the beach.",
              **done(*DAILIES, SHORT_RATIONS, value=3)),
        entry("s3s_trade", "complete_specific_quest",
              "Trade her what the sea gave you for one of the crew's charts.",
              "<b>Trade with her for a deck chart once.</b> Her Deck Charts trade costs 4 Wreck Salvage, and any "
              "chart you pick counts.",
              "flooded_chart", "She hands the chart over still damp.", **done(DECK_TRADE)),
        entry("s3s_rations", "complete_specific_quest",
              "Keep her crates on her sand for a tide.",
              f"<b>Finish Short Rations once.</b> {WHERE_SR}",
              "archive_chart_case", "Her crates stay on her sand, for today.", **done(SHORT_RATIONS)),
        entry("s3s_stores", "complete_specific_quest",
              "Go down to the stores the crew keep guarding.",
              f"<b>Win The Flooded Stores once,</b> either ending. {WHERE_RUN}",
              "sealed_treasury", "You came back up with what the sea hadn't taken.", **done(RUN)),
    ]


HIGH = {"key": "high", "srcId": "ss641_page_high", "name": "The Watch Log: Stolen Stores (81+ staff test)",
        "release_name": "The Watch Log: Stolen Stores", "entries": page_high, "level": (81, 100),
        "hook": ("The third page turned up in a galley ration tin. A list of rations, every one signed for twice, "
                 "and a note at the bottom in a shakier hand: the stores are flooding."),
        "levels_line": "For level 81 and up; levels 30 to 80 have their own page.",
        "success": ("Page complete. The salvager counts the stores twice and comes up one short. \"Something down "
                    "there was eating them.\"")}
LOW = {"key": "low", "srcId": "ss641_page_low", "name": "The Watch Log: Stolen Stores (Shallows)",
       "release_name": "The Watch Log: Stolen Stores (Shallows)", "entries": page_low, "level": (30, 80),
       "test_level": (30, 100),
       "hook": ("The bottom of the third page washed up on her beach, wrapped round a ration biscuit. It lists what "
                "the crew are still hauling off the sand."),
       "levels_line": "For levels 30 to 80; level 81 and up has its own page.",
       "success": "Page complete. Her crates are back on her sand. \"They'll be back for them. They always are.\""}
PAGES = [HIGH, LOW]


def challenge_text(page, objs):
    lines = []
    for i, o in enumerate(objs, 1):
        plain, rew = o["description"].split("<br><br>", 1)[1].split(" Reward when you claim it: ")
        lines.append(f"{i}. {plain} <i>Reward: {rew.rstrip('.')}.</i>")
    return (f"<i>{page['hook']}</i><br><br>"
            "<b>This weekend's challenges</b><br>" + "<br>".join(lines) +
            "<br><b>All five:</b> a Skyglass Token.<br><br>"
            f"<b>Rules</b><br>{page['levels_line']} Only wins after you take this page count. Do them in any order, "
            "and claim each reward from its card in the Logbook. The page closes at the end of Monday (00:00 UTC "
            "Tuesday).")


def chained(objs):
    for a, b in zip(objs, objs[1:]):
        a["nextObjectiveId"] = b["id"]
    return objs


def data(page, test=True):
    objs = page["entries"]()
    lo, hi = page.get("test_level", page["level"]) if test else page["level"]
    return {"name": page["name"] if test else page["release_name"], "description": challenge_text(page, objs),
            "image": ICON_LIVE, "questType": "event", "questRank": "D", "successDescription": page["success"],
            "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
            "requiredLevel": lo, "maxLevel": hi, "maxAttempts": 1, "maxCompletes": 1,
            "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
            "startsAt": None, "endsAt": None,
            "content": {"objectives": objs, "sceneBackground": BG, "sceneCharacters": [SALVAGER], "entryItems": [],
                        "isolated": False, "reward": {"reward_items": [{"ids": [TOKEN], "number": 100,
                                                                        "quantity": 1}]}}}


def check(page):
    objs = page["entries"]()
    assert len(objs) == 5 and len({o["id"] for o in objs}) == 5
    for o in objs:
        for s in (o["description"], o["successDescription"]):
            assert "—" not in s and "–" not in s, o["id"]
        if o["task"] == "defeat_opponents":
            assert [a["number"] for a in o["opponentAIs"]] == [1], o["id"]  # law 44: a count
            assert o["sector"] == NOWHERE and o["hideLocation"] is True, o["id"]  # unreachable: never forces a fight
        else:
            assert o["task"] == "complete_specific_quest" and o["value"] >= 1 and o["completeQuestIds"], o["id"]
        ids = [x for r in o["reward_items"] for x in r["ids"]]
        assert ids[-1] == SALVAGE and o["reward_items"][-1]["quantity"] == 3, o["id"]
    for v in [o2 for o in objs for o2 in o.get("completeQuestIds", [])] + [LIVE_PAGE3, TOKEN, SALVAGER, BG]:
        assert NANO.match(v), v


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/stolen_stores_pages.gen.py; do not hand-edit.", "dedupNames": True}
    m.update(extra or {})
    m["items"] = items
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items), "items")


def created(bundle):
    b = json.load(open(bundle if os.path.isabs(bundle) else os.path.join(ROOT, bundle)))
    ids = {}
    for e in b.get("entries", []):
        if e.get("state") == "ok" and e.get("slot") == "create" and e.get("entity") == "quest":
            for p in PAGES:
                if e.get("name") == p["name"]:
                    ids[p["key"]] = e["id"]
    assert set(ids) == {"high", "low"}, ids
    return ids


def main():
    for p in PAGES:
        check(p)
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "create":
        items = []
        for p in PAGES:
            d = data(p)
            d["content"]["objectives"] = chained(d["content"]["objectives"])
            items.append({"entity": "quest", "slot": "create", "srcId": p["srcId"], "phase": 1, "name": p["name"],
                          "data": d})
        write(641, "stolen_stores_pages_create", "push/641, HIDDEN: create the two rebuilt Stolen Stores Watch Log "
              "pages for the staff test (81+ test copy and the Shallows page). Chained for Forge L03; push/642 opens "
              "every order at once, still hidden.", items)
        return
    bundle = sys.argv[sys.argv.index("--from") + 1] if "--from" in sys.argv else ""
    assert bundle, "--from <push/641 results bundle> required"
    ids = created(bundle)
    if mode == "open":
        items = [{"entity": "quest", "slot": "edit", "targetId": ids[p["key"]], "phase": 1,
                  "name": f"{p['name']}: every order open (hidden)",
                  "data": dict(data(p), consecutiveObjectives=False, hidden=True)} for p in PAGES]
        write(642, "stolen_stores_pages_open", "push/642, HIDDEN: both rebuilt pages with consecutiveObjectives "
              "false so every order is open at once (RUL-2026-11-08-139). Still hidden, no window, for the staff "
              "test.", items)
        return
    if mode in ("release", "stage"):
        hi = dict(data(HIGH, test=False), consecutiveObjectives=False, hidden=False, startsAt=FRIDAY_START,
                  endsAt=FRIDAY_END, image=ICON_RELEASE[HIGH["key"]])
        lo = dict(data(LOW, test=False), consecutiveObjectives=False, hidden=False, startsAt=FRIDAY_START,
                  endsAt=FRIDAY_END, image=ICON_RELEASE[LOW["key"]])
        if mode == "stage":
            hi["hidden"] = lo["hidden"] = True
            write(676, "stolen_stores_pages_stage", "push/676, HIDDEN: both Watch Log pages take tonight's release data "
                  "now, hidden (the 81+ record leaves its old Nov 8 content and level 1+ for the rebuilt 81+ page; "
                  "both charts in challenge rewards are the Chart of the Flooded Stores, the director 2026-11-20 "
                  "16:19Z). push/643 (in push/673) sends the same records with hidden false at 6 PM.",
                  [{"entity": "quest", "slot": "edit", "targetId": LIVE_PAGE3, "phase": 1,
                    "name": "The Watch Log: Stolen Stores: rebuilt 81+ page, staged hidden", "data": hi},
                   {"entity": "quest", "slot": "edit", "targetId": ids["low"], "phase": 1,
                    "name": "The Watch Log: Stolen Stores (Shallows): release data, staged hidden", "data": lo}])
            return
        write(643, "stolen_stores_pages_release", "push/643, RELEASE ONLY (Friday Nov 20, with the director's go): "
              "the live page 3 record takes the tested 81+ page whole; the Shallows page is unhidden at levels 30 to "
              "80. Both open 00:00 UTC Saturday and close 00:00 UTC Tuesday. Needs The Flooded Stores, Short Rations "
              "and the Deck Charts pick (push/644) live first. Re-read both records before running.",
              [{"entity": "quest", "slot": "edit", "targetId": LIVE_PAGE3, "phase": 1,
                "name": "The Watch Log: Stolen Stores: rebuilt 81+ page", "data": hi},
               {"entity": "quest", "slot": "edit", "targetId": ids["low"], "phase": 1,
                "name": "The Watch Log: Stolen Stores (Shallows): publish", "data": lo}],
              {"_release_only": True})
        return
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
