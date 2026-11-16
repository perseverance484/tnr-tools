#!/usr/bin/env python3
"""Skyglass weekend 3 (Stolen Stores, opens Fri Nov 20 6 PM CT = 2026-11-21 00:00 UTC): band setup, same as Nov 13.

Nothing here runs or writes to the game. It writes manifests into this folder for the director's review.

    python3 stolen_stores_band.gen.py --repo <tnr-tools checkout> \
        --page-id <clone> --ws-low-id <clone> --ws-high-id <clone> [--dated]

Bases (repo perseverance484/tnr-tools, main c647a54):
  * push/609_master_A_nov13.json   whole records of this week's two Wreck Sighted copies and the 30-80 page
  * push/615_wreck_sighted_text_final_nov14b.json   the text pass the director okayed 00:42Z Nov 14, as a whole content
    block. Ran in his tab 15:40Z Nov 14, 3/3 verified (614, objectives only, was refused for missing content.reward).
    The new copies take 609's top-level fields with 615's whole content block, so they match the live copies.
  * push/518_skyglass_journal_page3_publish.json   Stolen Stores as live (published Nov 8, levels 1-100, no prereq)
  * push/611_salvage_and_flips_nov13.json   3 Wreck Salvage per Watch Log order (RUL-2026-11-13-148)

Clone source: the original Wreck Sighted _zp1l7Y9a_77pgonAdsYx (event, hidden since Nov 14 00:01Z). Last week's
source, The Watch Log: First Page, was deleted Nov 14 00:31Z. A Forge create of an event quest bulk-assigns it to
every active player, so every new event record must start as a clone of a hidden event record.
"""
import argparse, copy, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
CLONE_SOURCE = "_zp1l7Y9a_77pgonAdsYx"
OLD = {"ws_low": "IZgCt17ReC_0vtUG-GNRl", "ws_high": "-UjsbiBbaSyPtZ4zAH10A",
       "page_low": "73ivWjFFk0dwSEG7bNhMj", "page_high": "V-i3ZcAqPu0hB3G9IEzGo"}
STOLEN = "AgGR962c3XNo6Pr0up2qT"           # The Watch Log: Stolen Stores (81+ page from this build on)
FADED_WRECK, SKYGLASS_WRECK = "j4QEUtjbK_lbOYUPVoidk", "RHqzYdY4EAQA9HwsBKWDS"
STARTS, ENDS = "2026-11-21", "2026-11-24"   # 00:00 UTC Sat (Fri 6 PM CT) to 00:00 UTC Tue (Mon 6 PM CT)
SALVAGE = "mW6_ZGtGcCSuXGPhn-H4o"; SALVAGE_N = 3
SALVAGER, SHORE = "Xugt7415D3-tepLfxpwM5", "rX78pJPETsUL2JrsSvGHn"
ICON_PAGE = "https://ui0arpl8sm.ufs.sh/f/4xb_93fgzp68t83owGoQQ.webp"   # stand-in until the painted icon is uploaded
Q = {  # ids exactly as in this week's live 30-80 page (609) and the Driftline go-live (611)
    "low_tide": "pFQBaJxU_8RSvSi4Kir1Z", "night_watch": "dnzL-bDrAEVXrKB5xariu",
    "galley": "x7ByC_5ssbpibxTB60Ag1", "split": "ktVUByCZUfREmWYsvPtzQ", "stern": "BDUY4nScGzYiZoHGkmkxP",
    "t_deck": "zYhkIQeVGNUMljwev3-ud", "t_hold": "OCrpmCXlh1v9CnQPzDRpj",
    "t_sealed": "oMBY3r0XiSZ_2HaJN0L39", "t_lantern": "26MTz1wdUuKbfm1nPQNGU",
    "beach": "5faJqlDvs8jXTv1zN8B8m", "d_glass": "ejD1-13fEZupXUU8tf8Au",
    "d_echoes": "5ZksRGBaMmzG49EtzugNX", "d_count": "sbssALiuyJVTApe8ZpLvp",
}
I = {
    "tide_chart": ("H1s2IwtZ5JqgPEoJ55IVj", "a Tide Chart"),
    "medicine_inro": ("ixEKlJ0MmDrX7JoMNJVhi", "a Medicine Inro"),
    "galley_stores": ("D-QTnbjgTyIVc593zzdSB", "Galley Stores"),
    "sealed_treasury": ("Ma8S90Nmbi0Xvm4u4FzJh", "a Sealed Treasury"),
    "skyglass_token": ("nzCW7A-_AuYMzBs2wClnM", "a Skyglass Token"),
    "chart_case": ("B48dTRsoLJGKBWIUbeUoG", "an Archive Chart Case"),
}
REWARD_ZERO = {"reward_exp": 0, "reward_rank": "NONE", "reward_money": 0, "reward_badges": [], "reward_jutsus": [],
               "reward_titles": [], "reward_tokens": 0, "reward_prestige": 0, "reward_anbupoints": 0,
               "reward_bloodlines": [], "reward_clanpoints": 0, "reward_reputation": 0, "reward_sage_modes": [],
               "reward_war_damage": 0, "reward_skillpoints": 0, "reward_war_healing": 0,
               "reward_hunter_items": False, "reward_seichi_silver": 0, "reward_gathering_items": False,
               "reward_hunter_items_ids": [], "reward_hunting_experience": 0, "reward_medical_experience": 0,
               "reward_village_membership": "NONE", "reward_crafting_experience": 0,
               "reward_gathering_items_ids": [], "reward_gathering_experience": 0,
               "reward_sage_mastery_experience": 0}
PAGE_LOW_NAME = "The Watch Log: Stolen Stores (Shallows)"


def row(item, qty=1):
    return {"ids": [item], "number": 100, "quantity": qty}


def order(oid, voice, plain, rew, success, quests, value):
    return {"id": oid, "task": "complete_specific_quest",
            "description": f"{voice}<br><br>{plain} Reward when you claim it: {I[rew][1]} and {SALVAGE_N} Wreck Salvage.",
            "successDescription": success, "sceneBackground": "", "sceneCharacters": [],
            "completeQuestIds": [Q[k] for k in quests], "value": value,
            "reward_items": [row(I[rew][0]), row(SALVAGE, SALVAGE_N)]}


def low_orders():
    o = [
        order("j3s_galley", "Start where the stores were kept, and where the rot got in first.",
              "<b>Win The Rotted Galley 2 times in total.</b> Its chart drops in both Wrecks.", "galley_stores",
              "Two counts of the cold room. Both come up short.", ["galley"], 2),
        order("j3s_watch", "Stand the watches the ration list was drawn up for.",
              "<b>Win the Low Tide Run or the Night Watch, 2 times in total.</b>", "medicine_inro",
              "Two watches stood. Nobody on the roster ate their share.", ["low_tide", "night_watch"], 2),
        order("j3s_driftline", "Follow the stores that went over the side when she broke.",
              "<b>Win The Split Hold or The Broken Stern once.</b> Their charts drop in the Faded Wreck.",
              "tide_chart", "The crates the sea took were empty before they hit the water.", ["split", "stern"], 1),
        order("j3s_trade", "Bring the salvager what you pulled up, and see what she can spare.",
              "<b>Win any of the Salvager's trades once.</b> Her Deck Charts trade costs 4 Wreck Salvage.",
              "chart_case", "She weighs your salvage twice and hands you a chart case from her own stores.",
              ["t_deck", "t_hold", "t_sealed", "t_lantern"], 1),
        order("j3s_daily", "Work the shore for what washed out of the stores.",
              "<b>Win any of the Salvager's dailies 5 times in total.</b> Find her in sector 210, by the Wrecks.",
              "sealed_treasury", "Five tides worked. The shore gives back tins, never food.",
              ["beach", "d_glass", "d_echoes", "d_count"], 5),
    ]
    for a, b in zip(o, o[1:]):
        a["nextObjectiveId"] = b["id"]
    return o


HOOK_LOW = ("A strip torn from the bottom of the third page washed into the shallows with the ration tin. It lists "
            "the small rooms the deckhands kept, and every one of them comes up short.")
RULES = {
    "low": ("For levels 30 to 80; level 81 and up has its own page. Only wins after you take this page count. Wreck "
            "clears don't count, but the charts the Wrecks drop open these runs. Do them in any order, and claim "
            "each reward from its card in the Logbook. The page closes at the end of Monday (00:00 UTC Tuesday)."),
    "high": ("For level 81 and up; levels 30 to 80 have their own page. Only wins after you take this page count. "
             "Do them in any order, and claim each reward from its card in the Logbook. The page closes at the end "
             "of Monday (00:00 UTC Tuesday)."),
}


def description(hook, objs, band):
    lines = []
    for n, o in enumerate(objs, 1):
        plain, rew = o["description"].split("<br><br>", 1)[1].split(" Reward when you claim it: ")
        lines.append(f"{n}. {plain} <i>Reward: {rew.rstrip('.')}.</i>")
    return (f"<i>{hook}</i><br><br><b>This weekend's challenges</b><br>" + "<br>".join(lines) +
            f"<br><b>All five:</b> a Skyglass Token.<br><br><b>Rules</b><br>{RULES[band]}")


def check_text(s, where):
    assert "—" not in s and "–" not in s, f"dash in {where}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/home/claude/perseverance484/tnr-tools")
    ap.add_argument("--page-id", default="PLACEHOLDERclonePAGE00")
    ap.add_argument("--ws-low-id", default="PLACEHOLDERcloneWSLOW0")
    ap.add_argument("--ws-high-id", default="PLACEHOLDERcloneWSHIGH")
    ap.add_argument("--undated", action="store_true",
                    help="leave the copies' startsAt/endsAt empty, as on Nov 13 (then they must stay hidden until Friday)")
    a = ap.parse_args()
    P = lambda f: json.load(open(os.path.join(a.repo, "push", f)))
    m609, m615, m518, m611 = P("609_master_A_nov13.json"), P("615_wreck_sighted_text_final_nov14b.json"), \
        P("518_skyglass_journal_page3_publish.json"), P("611_salvage_and_flips_nov13.json")
    rec609 = {it["targetId"]: it["data"] for it in m609["items"] if it["slot"] == "edit"}
    con615 = {it["targetId"]: it["data"]["content"] for it in m615["items"]}
    rh611 = next(it for it in m611["items"] if it["targetId"] == OLD["page_high"])["data"]["content"]

    # ---- 1. the two Wreck Sighted copies -------------------------------------------------------------------------
    ws_items = []
    for band, old_ws, old_page, new_ws, new_page in (
            ("low", OLD["ws_low"], OLD["page_low"], a.ws_low_id, a.page_id),
            ("high", OLD["ws_high"], OLD["page_high"], a.ws_high_id, STOLEN)):
        d = copy.deepcopy(rec609[old_ws])
        content = copy.deepcopy(con615[old_ws])
        objs = content["objectives"]
        grants = [o for o in objs if o["task"] == "new_quest"]
        assert len(grants) == 1 and grants[0]["newQuestIds"] == [old_page], grants
        grants[0]["newQuestIds"] = [new_page]
        d["content"] = content
        assert d["questType"] == "event" and d["maxCompletes"] == 1 and d["retryDelay"] == "none"
        d.update({"hidden": True, "prerequisiteQuestId": None})
        if not a.undated:
            d.update({"startsAt": STARTS, "endsAt": ENDS})
        check_text(json.dumps(d, ensure_ascii=False), d["name"])
        ws_items.append({"entity": "quest", "slot": "edit", "targetId": new_ws, "phase": 2,
                         "name": f"{d['name']}: Stolen Stores weekend copy (grants {'the new 30-80 page' if band == 'low' else 'Stolen Stores'})",
                         "data": d})

    # ---- 2. the new 30-80 page ------------------------------------------------------------------------------------
    lo = low_orders()
    page = copy.deepcopy(rec609[OLD["page_low"]])
    page.update({"name": PAGE_LOW_NAME, "description": description(HOOK_LOW, lo, "low"), "image": ICON_PAGE,
                 "successDescription": ("Page complete. The salvager lays the strip under the ration tin's list and "
                                        "runs a finger down both. \"Same rooms. Same shortfall. Someone was counting.\""),
                 "hidden": True, "prerequisiteQuestId": a.ws_low_id, "startsAt": STARTS, "endsAt": ENDS,
                 "requiredLevel": 30, "maxLevel": 80, "consecutiveObjectives": False})
    page["content"]["objectives"] = lo
    page["content"]["reward"] = {**REWARD_ZERO, "reward_items": [row(I["skyglass_token"][0])]}
    check_text(json.dumps(page, ensure_ascii=False), PAGE_LOW_NAME)
    page_item = {"entity": "quest", "slot": "edit", "targetId": a.page_id, "phase": 1,
                 "name": f"{PAGE_LOW_NAME}: build on the hidden clone", "data": page}

    # ---- 3. Stolen Stores becomes the 81+ page --------------------------------------------------------------------
    ss = m518["items"][0]["data"]
    assert ss["name"] == "The Watch Log: Stolen Stores"
    sc = copy.deepcopy(ss["content"])
    for o in sc["objectives"]:
        assert all(r["ids"] != [SALVAGE] for r in o["reward_items"])
        o["reward_items"].append(row(SALVAGE, SALVAGE_N))
        head, tail = o["description"].rsplit(" Reward when you claim it: ", 1)
        o["description"] = f"{head} Reward when you claim it: {tail.rstrip('.')} and {SALVAGE_N} Wreck Salvage."
    sc["reward"] = {**rh611["reward"], "reward_items": [row(I["skyglass_token"][0])]}
    for k in ("isolated", "rewardMode", "rewardPickCount"):
        sc.setdefault(k, rh611[k])
    hook_high = re.match(r"<i>(.*?)</i>", ss["description"]).group(1)
    ss_data = {"requiredLevel": 81, "maxLevel": 100, "prerequisiteQuestId": a.ws_high_id,
               "description": description(hook_high, sc["objectives"], "high"), "content": sc}
    check_text(json.dumps(ss_data, ensure_ascii=False), "Stolen Stores")
    ss_item = {"entity": "quest", "slot": "edit", "targetId": STOLEN, "phase": 3,
               "name": "The Watch Log: Stolen Stores: level 81+, needs the new 81+ Wreck Sighted, 3 salvage per order",
               "data": ss_data}

    build = {"_note": ("Wednesday build for the Stolen Stores weekend (opens Fri Nov 20 6 PM CT). Run in the director's Forge "
                       "tab AFTER the three clones in 00_clone_plan.json and a regenerate with their ids. Phase 1: the "
                       "new 30-80 page onto its clone (hidden). Phase 2: both Wreck Sighted copies onto their clones "
                       "(hidden; 609 top-level fields + 615's whole content block, as live since 15:40Z Nov 14; each grants its band's page). Phase 3: Stolen "
                       "Stores (already published, startsAt 2026-11-21) becomes the 81+ page: level 81-100, needs the "
                       "new 81+ copy, 3 Wreck Salvage per order, rewards and rules lines updated. Generated by "
                       "stolen_stores_band.gen.py; do not hand-edit."),
             "items": [page_item] + ws_items + [ss_item]}

    release = {"_note": ("Release flips. LIVE. Default: Friday Nov 20 at 6 PM CT with the Wrecks. Because the new "
                         "copies and page carry startsAt 2026-11-21 (the engine refuses a start before it), this can "
                         "also run Wednesday after the build: nothing becomes playable early. Old copies are hidden so "
                         "a new player can't take last week's key."),
               "items": [
                   {"entity": "quest", "slot": "edit", "targetId": a.page_id, "phase": 1,
                    "name": f"{PAGE_LOW_NAME}: publish", "data": {"hidden": False}},
                   {"entity": "quest", "slot": "edit", "targetId": a.ws_low_id, "phase": 1,
                    "name": "Wreck Sighted (Levels 30 to 80), Stolen Stores copy: unhide", "data": {"hidden": False}},
                   {"entity": "quest", "slot": "edit", "targetId": a.ws_high_id, "phase": 1,
                    "name": "Wreck Sighted (Level 81 and up), Stolen Stores copy: unhide", "data": {"hidden": False}},
                   {"entity": "quest", "slot": "edit", "targetId": OLD["ws_low"], "phase": 2,
                    "name": "Wreck Sighted (Levels 30 to 80), Rotted Heading copy: hide", "data": {"hidden": True}},
                   {"entity": "quest", "slot": "edit", "targetId": OLD["ws_high"], "phase": 2,
                    "name": "Wreck Sighted (Level 81 and up), Rotted Heading copy: hide", "data": {"hidden": True}},
               ]}

    req = {"retryDelay": "daily", "maxAttempts": None, "attemptDelay": "none", "maxCompletes": 100,
           "requiredItemId": None, "requiredItemQuantity": 1}
    gates = {"_note": ("Wreck gates re-pointed to the new copies. NOT a Forge file: Forge refuses dungeon edits (its "
                       "pinned dungeon contract lacks maxPlayers). Send as coop.dungeon.save {id, content} built from a "
                       "fresh coop.dungeon.getAll with tnr/release_nov13/direct/dsplit.py, or set the two fields in the "
                       "dungeon editor. Run any time after the Wrecks close (Mon Nov 16 6 PM CT) and the new copies "
                       "exist, before the Friday reopen. requirements = live object read 2026-11-13 23:45Z with only "
                       "prerequisiteQuestId changed."),
             "items": [
                 {"entity": "dungeon", "slot": "edit", "targetId": FADED_WRECK, "phase": 1,
                  "name": "Faded Skyglass Wreck: needs the Stolen Stores 30-80 Wreck Sighted",
                  "data": {"requirements": {**req, "requiredLevel": 30, "prerequisiteQuestId": a.ws_low_id}}},
                 {"entity": "dungeon", "slot": "edit", "targetId": SKYGLASS_WRECK, "phase": 1,
                  "name": "Skyglass Wreck: needs the Stolen Stores 81+ Wreck Sighted",
                  "data": {"requirements": {**req, "requiredLevel": 81, "prerequisiteQuestId": a.ws_high_id}}},
             ]}

    clone = {"_note": ("Step 0 (connector, or the Clone button in the quest editor). Clone the ORIGINAL Wreck Sighted "
                       f"{CLONE_SOURCE} three times: it is an event quest and hidden, and a clone keeps both. Never "
                       "clone a visible record and never Forge-create an event quest (bulk-assigns it to every active "
                       "player). Then: python3 stolen_stores_band.gen.py --page-id A --ws-low-id B --ws-high-id C"),
             "calls": [{"endpoint": "quests.clone", "input": {"id": CLONE_SOURCE}, "expect": f"new id -> {k}"}
                       for k in ("--page-id", "--ws-low-id", "--ws-high-id")]}

    for name, obj in (("00_clone_plan.json", clone), ("01_stolen_stores_band_build.json", build),
                      ("02_release_flips.json", release), ("03_wreck_gates_direct_save.json", gates)):
        with open(os.path.join(HERE, name), "w") as f:
            json.dump(obj, f, indent=1, ensure_ascii=False); f.write("\n")
        print(name)


if __name__ == "__main__":
    main()
