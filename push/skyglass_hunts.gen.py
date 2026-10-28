#!/usr/bin/env python3
"""Generate push/266 (the Quarantined Archive and the Captain's Watch, filling push/264's placeholders) and push/265 (the Drowned Foundry): hidden, isolated Battle Pyramids.

    python3 push/skyglass_hunts.gen.py

Source text: state/skyglass_hunts/hunts.py (draft content; docs/design/SKYGLASS_HUNTS_CONTENT.md). Rewards:
docs/design/SKYGLASS_LOOT_TABLES.md (RUL-2026-10-25-002/-004). The Foundry's boss is the Foundry Warden created by push/262. Do not hand-edit the output.
"""
import hashlib, importlib.util, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("hunts", os.path.join(ROOT, "state/skyglass_hunts/hunts.py"))
H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)

AI = {"Core Horror": "AQi-bHJ-5tHXtxrnc0P9E", "Skyglass Sentinel": "3V_gdHYaclMB1gTyOPAbV", "Seal Charge": "wTgO-Q32caSSd0is1QIS7",
      "Sealwright": "RBW5KsIXmTGR710D2y2Y7", "Wayfinder": "v7T9_XdGMfP46em0dPuBc", "First Blade": "d6g0mOM7RBSsYI1hrUVT9",
      "The Captain": "QY69h271Nx9uHrBeR6jwW", "Deck Warden": "texZaFi42S3EvJZBwQ8cd", "Core Canister": "frc9LTxqQlM7mncG4VZGK",
      "Arsenal Keeper": "2OXJEXoktxJcjqMkE851g", "Foundry Warden": "81lnIP-q97gItQYWl5vWD"}  # Warden: push/262 result
ITEM = {"treasury": "Ma8S90Nmbi0Xvm4u4FzJh", "chart_archive": "cRZT41zm5vhPTQwwn8vtv", "chart_watch": "aHFNuo5RkKpDcaOBLIKiu",
        "case": "B48dTRsoLJGKBWIUbeUoG", "chart_foundry": "pY-0O5Gs2n89pf0kYb5J2",
        "pouches": ["D0gtI5dOgj2dFO4VexsLJ", "ZZOrFciKSJazAtkW9nt_7", "we2DtPSH2Q5quEvxj7xO2", "hcvHkfcYHP6qBEO_dRFl6", "z9U9wvJKDGtimll6BnTuL"], "strongbox": "h-d58UCSuHN8EZKbLjT5R", "coffer": "THo7rfzP-S82_43aN8fs3", "inro": "ixEKlJ0MmDrX7JoMNJVhi"}
PORTRAIT = {"Sealwright": "b_K8qdNI651fTsRn9tfkk", "Oathkeeper": "6iwMYC8WTCGJTf2QIYfBz", "The Captain": "xm3F2YXkNPeLWHRAUnbmF"}
SCENE = {
    "exterior_keel_walk": "@img:scene_bg_ghost_ship_exterior_keel_walk.webp",
    "hold": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",
    "lower_hull": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi",
    "reconstruction_chamber": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJRiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl",
    "quarantined_archive": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJpo8lFZubKBAOsGCHyl3Sk0mZFrgWPUdjMJ75",
    "cache_site": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJyX6gwPukVH2MI5Lo4ehEfAXvZdcmtWqPg7rp",
    "chart_room": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJqpbYjW5dkOZgJQ8mGRcdx3SsWvPelyYFTt5V",
    "deck_b": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJcoxkatSnxBpQqGNDcTHbLmYz8uXAl3oa54ti",
    "helm": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJIp0fIvxfOewksxBoS1HQCihpL7c42Ky9uUFv",
    "command_observation_gallery": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ8ZwqPukkp45TvAnoIBa0rtCf1lbyXYjVKQ2q",
}
STEP_EXP = {"I": 1000, "II": 2000, "III": 3000, "IV": 4000, "V": 5000, "VI": 5000}
STEP_N = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6}
PACK_REF = "c371a8c1a8302ed23ba7287ed77cb780250dbb24"
IMAGES = {"icon-chart-drowned-foundry.webp": "art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp",
          "icon-chart-quarantined-archive.webp": "art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp",
          "icon-chart-captains-watch.webp": "art/skyglass_event_icons/exports/icon-chart-captains-watch.webp",
          "scene_bg_ghost_ship_exterior_keel_walk.webp": "art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp"}


def effect(t, power, rounds, desc, calc="static"):
    return {"type": t, "power": power, "rounds": rounds, "target": "INHERIT", "direction": "offence", "calculation": calc,
            "powerPerLevel": 0, "description": desc, "appearSfx": "", "disappearSfx": "", "appearAnimation": "",
            "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}


# Every combat tag's BaseAttributes.direction is the literal "offence" (validators/combat.ts): push/264 sent
# "defence" and the server refused both updates (2026-10-25), leaving two hidden placeholders that push/266 fills.
# Proposals (director to tune): the Archive alarm and the Watch terms (RUL-2026-10-24-021).
ALARM = [effect("increasedamagetaken", 20, 3, "The archive's alarm: you take 20% more damage for 3 rounds", "percentage")]
TERM = {1: [effect("elementalseal", 100, 99, "The Oathkeeper's term: your elemental jutsu are sealed")],
        2: [effect("disarm", 100, 99, "The Oathkeeper's term: you fight unarmed")],
        3: [effect("healprevent", 100, 99, "The Oathkeeper's term: no healing at the Captain's helm")]}


def dialog(i, scene, text, choices, portrait=None):
    return {"id": i, "task": "dialog", "description": text, "sceneBackground": SCENE[scene],
            "sceneCharacters": [PORTRAIT[portrait]] if portrait else [],
            "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}


def battle(i, scene, text, foes, nxt, retry=None, debuffs=None):
    # A lost, drawn or fled fight fails the hunt (director 2026-10-25). An isolated pyramid keeps a defeated player in
    # the run at 1 HP with no outside recovery, so a retry could not be won; fail_quest closes the run instead.
    counts = {}
    for f in foes: counts[f] = counts.get(f, 0) + 1
    o = {"id": i, "task": "start_battle", "description": text, "sceneBackground": SCENE[scene], "sceneCharacters": [],
         "opponentAIs": [{"ids": [AI[f]], "number": n, "quantity": 1} for f, n in counts.items()],
         "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False, "opponent_scaled_to_user": False,
         "nextObjectiveId": nxt, "failObjectiveId": FAIL_ID,
         "failDescription": "You are defeated.", "drawDescription": "The fight stalls and the moment is lost.",
         "fleeDescription": "You break away, and the way back closes behind you."}
    if debuffs: o["applyDebuffs"] = debuffs
    return [o]


FAIL_ID = "f_lost"


def failed(scene, text):
    return {"id": FAIL_ID, "task": "fail_quest", "description": text, "sceneBackground": SCENE[scene], "sceneCharacters": []}


def win(i, scene, text, step):
    return {"id": i, "task": "win_quest", "description": text, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "reward_exp": STEP_EXP[step], "reward_items": [{"ids": [ITEM["treasury"]], "number": STEP_N[step], "quantity": 1}]}


def archive():
    objs, prev = [], {}
    nodes = H.ARCHIVE["nodes"]
    for (i, task, scene, src, text, edges, extra) in nodes:
        for _, tgt in edges: prev.setdefault(tgt, i)
    for (i, task, scene, src, text, edges, extra) in nodes:
        portrait = None  # Sealwright scene character pending push/140
        if task == "dialog":
            # A menu may not send two options to one node (validate.py): each wrong answer gets its own short beat
            # that leads on to the shared alarm.
            seen, out = {}, []
            for t, tgt in edges:
                seen[tgt] = seen.get(tgt, 0) + 1
            k = 0
            for t, tgt in edges:
                if seen[tgt] > 1:
                    k += 1
                    beat = f"{i}_wrong{k}"
                    objs.append(dialog(beat, scene, f"You choose: {t}. The seal flares red and the archive's alarm begins to toll.",
                                       [("Brace yourself", tgt)]))
                    out.append((t, beat))
                else:
                    out.append((t, tgt))
            objs.append(dialog(i, scene, text, out, portrait))
        elif task == "start_battle":
            objs += battle(i, scene, text, extra["fight"], edges[0][1], prev[i], ALARM if i.startswith("b_alarm") else None)
        elif task == "win_quest":
            objs.append(win(i, scene, text, extra["step"]))
    objs.append(failed("quarantined_archive", "The archive's seals close over you. You are thrown out of the wreck, and the chart crumbles in your hand."))
    return objs


def foundry():
    objs, prev = [], {}
    for (i, task, scene, src, text, edges, extra) in H.FOUNDRY["nodes"]:
        for _, tgt in edges: prev.setdefault(tgt, i)
    for (i, task, scene, src, text, edges, extra) in H.FOUNDRY["nodes"]:
        if task == "dialog": objs.append(dialog(i, scene, text, edges))
        elif task == "start_battle": objs += battle(i, scene, text, extra["fight"], edges[0][1], prev[i])
        elif task == "win_quest": objs.append(win(i, scene, text, extra["step"]))
    objs.append(failed("lower_hull", "The flood takes you. You wash up on the shore below the wreck, and the chart is gone."))
    return objs


def watch():
    o = []
    land = H.WATCH["nodes"][0]
    o.append(dialog("d_landing", "cache_site", land[4], [("Board the boat", "d_term1")], "Oathkeeper"))
    T1 = H.WATCH["nodes"][1][4]
    T2 = "On deck the First Blade waits in the uniform of a dead era, twin cleavers forming from the gale. 'Finally. Something new.' The Oathkeeper speaks from the rail: 'Meet him with empty hands.'"
    T3 = H.WATCH["nodes"][6][4]
    fights = {1: ("chart_room", "Wayfinder", "The Wayfinder redraws the room around you.", "Your elements go quiet. The Wayfinder waits."),
              2: ("deck_b", "First Blade", "The First Blade steps forward.", "You set your weapons down. The First Blade grins."),
              3: ("helm", "The Captain", "The Captain steps down from the command dais.", "The Oathkeeper seals the helm against healing. The Captain draws.")}
    intro = {1: (T1, "Oathkeeper"), 2: (T2, "Oathkeeper"), 3: (T3, "The Captain")}

    def term_node(n, c):  # the term offer for fight n with c terms accepted so far
        return f"d_term{n}" if n == 1 else f"d_term{n}_{c}"

    def after(n, c):
        if n < 3: return term_node(n + 1, c)
        return "d_gallery_" + ("IV" if c == 0 else "VI" if c == 3 else "V")

    for n in (1, 2, 3):
        scene, foe, fight_text, accept_text = fights[n]
        for c in ([0] if n == 1 else range(n)):
            t = term_node(n, c)
            text, portrait = intro[n]
            o.append(dialog(t, scene, text, [("Accept the term", f"d{n}t_{c}"), ("Refuse and fight", f"d{n}_{c}")], portrait))
            o.append(dialog(f"d{n}_{c}", scene, "You refuse the term. " + fight_text, [("Fight", f"b{n}_{c}")]))
            o.append(dialog(f"d{n}t_{c}", scene, accept_text, [("Fight", f"b{n}t_{c}")]))
            o += battle(f"b{n}_{c}", scene, fight_text, [foe], after(n, c), f"d{n}_{c}")
            o += battle(f"b{n}t_{c}", scene, fight_text + " You fight under the Oathkeeper's term.", [foe], after(n, c + 1), f"d{n}t_{c}", TERM[n])
    gal = H.WATCH["nodes"][8][4]
    for step in ("IV", "V", "VI"):
        o.append(dialog("d_gallery_" + step, "command_observation_gallery", gal, [("Claim the watch's stores", "w_" + step)]))
    for (i, task, scene, src, text, edges, extra) in H.WATCH["nodes"][9:]:
        o.append(win(i, scene, text, extra["step"]))
    o.append(failed("cache_site", "The Oathkeeper lowers his blade. 'The watch is over.' You wake on the boat with the chart burned to ash."))
    return o


# ---- The Buried Cache (RUL-2026-10-25-012): the original Ghost Ship's w_A ending as a short hunt. Riddle and dig prose
# from the 2026-10-13 capture (harvests/inbox/tnr_results_1791903144042.json, d_map..w_A), adapted to the chart.
CACHE_PREMISE = ("Before the Skyglass war-ship vanished into the sky, its crew buried a field cache on this shore. The "
                 "Wayfinder corrected the route to it again and again as the coast changed. This chart carries his last correction. Lose a "
                 "fight and the tide takes the dig, chart and all.")


def cache():
    o = []
    o.append(dialog("d_landing", "cache_site", "The chart's route ends on a quiet stretch of coast, within sight of the "
        "wreck. Among the ship's impossible routes it marks an old field cache, buried before the ship vanished. The ink is decades old. The "
        "Wayfinder's newest corrections are not.", [("Follow the corrected route", "d_riddle"),
        ("Compare the old and new routes", "d_overlay")]))
    o.append(dialog("d_overlay", "cache_site", "Under the first route lies a map of places that did not yet exist when "
        "the ship vanished. The Wayfinder corrected the same journey again and again as villages moved, roads changed, "
        "and generations passed. The cache is real, but the final clue must be read against the newest chart.",
        [("Follow the corrected route", "d_riddle")]))
    o.append(dialog("d_riddle", "cache_site", "A notation along the route sheet reads: 'Where the cliff drinks and the "
        "stone keeps watch, the cache sleeps beneath the watcher's shadow.' Three coves match part of the description.",
        [("The cove beneath the stone shrine", "d_dig"), ("The cove with the split cliff", "d_wrong1"),
         ("The open beach past the reef", "d_wrong2")]))
    o.append(dialog("d_wrong1", "cache_site", "You dig where the split cliff breaks the tide. Beneath the sand you find "
        "old seal fragments, and the fragments wake: a Deck Warden pulls itself out of the sand with a seal charge "
        "still burning in its hook.", [("Fight", "b_ambush1")]))
    o.append(dialog("d_wrong2", "cache_site", "The open beach yields an abandoned anchor brace and reef stone, and "
        "something under it. A Deck Warden rises from the wet sand, dragging a seal charge with it.",
        [("Fight", "b_ambush2")]))
    o += battle("b_ambush1", "cache_site", "The buried Deck Warden and its charge.", ["Deck Warden", "Seal Charge"], "d_tracks")
    o += battle("b_ambush2", "cache_site", "The buried Deck Warden and its charge.", ["Deck Warden", "Seal Charge"], "d_tracks")
    o.append(dialog("d_tracks", "cache_site", "The Warden falls apart into sand and script. Its tracks lead along the "
        "shore to a cove beneath a stone shrine, where the watcher's shadow falls across the sand. The cache was here all "
        "along, and the noise has woken its guardian.", [("Dig beneath the watcher's shadow", "d_guardian_late")]))
    o.append(dialog("d_dig", "cache_site", "You dig beneath the stone watcher's shadow before the tide shifts. Your "
        "shovel strikes metal. Sand bursts outward as the Sentinel unfolds from a buried seal frame, armor plated with "
        "shell and stone around the cache.", [("Fight for the cache", "b_guardian")]))
    o.append(dialog("d_guardian_late", "cache_site", "Your shovel strikes metal. Sand bursts outward as the Sentinel "
        "unfolds from a buried seal frame, armor plated with shell and stone around the cache.",
        [("Fight for the cache", "b_guardian_late")]))
    o += battle("b_guardian", "cache_site", "The Sentinel rises between you and the cache.", ["Skyglass Sentinel"], "d_claim")
    o += battle("b_guardian_late", "cache_site", "The Sentinel rises between you and the cache.", ["Skyglass Sentinel"], "d_claim_late")
    claim = ("The Sentinel breaks apart into sand and fading script. Beneath it sits a sealed field cache stamped with the "
             "Skyglass emblem, the same four-pointed star etched into the wreck's keel.")
    o.append(dialog("d_claim", "cache_site", claim, [("Open the cache", "w_clean")]))
    o.append(dialog("d_claim_late", "cache_site", claim, [("Open the cache", "w_late")]))
    done = ("You recover a field cache buried before the ship vanished. Its supplies are old, kept fresh by a seal that "
            "never broke. Tucked under the lid is a note in a careful hand: 'For when we are relieved.'")
    o.append(win("w_clean", "cache_site", done, "II"))
    o.append(win("w_late", "cache_site", done, "I"))
    o.append(failed("cache_site", "The tide comes in over the dig. When it goes out, the cache is buried again and the chart has washed away."))
    return o


CHART_CACHE = {
    "entity": "item", "slot": "create", "phase": 1, "name": "Chart of the Buried Cache", "srcId": "chart_buried_cache",
    "data": None,  # filled from the Drowned Foundry chart's create (push/260) with its own name, text, rarity, icon
}

INRO_ROLLS = 2  # RUL-2026-10-25-012: the Medicine Inro opens with two rolls (was one)


def quest(src, name, desc, success, chart, image, objectives, reward, rank, target=None):
    head = {"entity": "quest", "slot": "edit", "targetId": target} if target else {"entity": "quest", "slot": "create", "srcId": src}
    return {**head, "name": name, "data": {
        "name": name, "description": desc, "image": image, "questType": "battlepyramid", "questRank": rank,
        "successDescription": success, "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True, "requiredLevel": 1, "maxLevel": 100,
        "maxAttempts": 100, "maxCompletes": 100, "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None,
        "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives, "sceneBackground": "", "sceneCharacters": [],
                    "entryItems": [{"ids": [chart], "number": 1}], "isolated": True,
                    "rewardMode": "choose", "rewardPickCount": 1, "reward": reward}}}


def items_reward(*entries, **scalars):
    r = {"reward_items": [{"ids": [i], "number": 100, "quantity": q} for i, q in entries]}
    r.update(scalars)
    return r


def write(num, slug, note, items):
    files = {}
    used = json.dumps(items)
    for name, path in IMAGES.items():
        if "@img:" + name not in used: continue
        b = open(os.path.join(ROOT, path), "rb").read()
        files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    m = {"_note": note, "dedupNames": True, "imgSizes": {k: v["bytes"] for k, v in files.items()},
         "imagePack": {"ref": PACK_REF, "files": files}, "items": items}
    json.dump(m, open(os.path.join(ROOT, f"push/{num}_{slug}.json"), "w"), indent=1)
    for it in items: print(num, it["name"], len(it["data"].get("content", {}).get("objectives", [])), "objectives")


def main():
    # Earlier outputs (264 failed; 265, 266 ran; 267 superseded; 268 staged) are archived or in push/. Current output:
    # push/270, the Buried Cache and the Medicine Inro's second roll.
    if os.environ.get("REGEN_268"):  # push/268 is staged; set REGEN_268=1 to reproduce it
        write(268, "skyglass_hunts_fail_on_loss", (
            "Skyglass treasure hunts (push/268): the Drowned Foundry, the Quarantined Archive and the Captain's Watch, all HIDDEN, "
            "re-sent as whole-record edits. Change: a lost, drawn or fled fight now fails the hunt (fail_quest closes the "
            "isolated run; the chart was already spent at start). Before this, every loss reset to the fight's dialog, but an "
            "isolated pyramid keeps a defeated player in the run at 1 HP with no outside recovery (libs/combat/database.ts), so "
            "the retry could not be won (director 2026-10-25: 'failing a fight fails the quest'). Wins carry the player's pools "
            "into the next fight (the game default; no givePools). Also: the Captain's Purse pick is 100,000 ryo (was 50,000), "
            "and the Foundry and Watch premises no longer promise retries. Rewards, ladder, debuffs and proposals unchanged "
            "(see push/README 264-266). Generated by push/skyglass_hunts.gen.py; do not hand-edit."), [
            quest("hunt_foundry", "The Drowned Foundry", H.FOUNDRY["premise"],
                  "You carried the last pour out of the keel works.", ITEM["chart_foundry"],
                  "@img:icon-chart-drowned-foundry.webp", foundry(),
                  items_reward(*[(x, 1) for x in ITEM["pouches"]]), "A", "UGHSuhi83C3wRtH3FD4Eu"),
            quest("hunt_archive", "The Quarantined Archive", H.ARCHIVE["premise"],
                  "The archive's last seal is broken and its records are yours.", ITEM["chart_archive"],
                  "@img:icon-chart-quarantined-archive.webp", archive(),
                  items_reward((ITEM["case"], 1), (ITEM["strongbox"], 1), reward_exp=15000), "A", "-bZ_ZoI6yrUJ_LKT9R5zm"),
            quest("hunt_watch", "The Captain's Watch", H.WATCH["premise"],
                  "You kept the Captain's watch and claimed its stores.", ITEM["chart_watch"],
                  "@img:icon-chart-captains-watch.webp", watch(),
                  items_reward((ITEM["coffer"], 1), (ITEM["inro"], 3), reward_money=100000), "A", "liljq0yVXWTSna4X6dZE1"),
        ])
    arch = os.path.join(ROOT, "archive/spent-manifests/push-2026-10-25")
    chart = json.load(open(os.path.join(arch, "260_skyglass_items_create.json")))
    base = next(it for it in chart["items"] if it["srcId"] == "chart_foundry")
    data = dict(base["data"])
    data.update({"name": "Chart of the Buried Cache", "rarity": "COMMON",
                 "description": ("A salt-stained chart from the Skyglass wreck, marking a field cache its crew buried on "
                                 "the shore before the ship vanished. Bring it to the Battle Arena to follow it."),
                 "image": "@img:icon-chart-drowned-foundry.webp"})  # placeholder icon until the cove chart is drawn
    chart_item = {**CHART_CACHE, "data": data}
    inro_src = json.load(open(os.path.join(arch, "253_skyglass_caches_convert.json")))
    inro = next(it for it in inro_src["items"] if it["targetId"] == ITEM["inro"])
    eff = json.loads(json.dumps(inro["data"]["effects"]))
    assert eff[0]["weightedCache"]["rolls"] == [{"count": 1, "probability": 10000}]
    eff[0]["weightedCache"]["rolls"] = [{"count": INRO_ROLLS, "probability": 10000}]
    eff[0]["description"] = "Medicine Inro: two rolls of pills and potions"
    inro_edit = {"entity": "item", "slot": "edit", "targetId": ITEM["inro"], "phase": 1,
                 "name": "Medicine Inro: two rolls", "data": {"effects": eff, "target": "SELF"}}
    q = quest("hunt_buried_cache", "The Buried Cache", CACHE_PREMISE,
              "You dug up the Skyglass crew's field cache.", "@item:chart_buried_cache",
              "@img:icon-chart-drowned-foundry.webp", cache(),
              items_reward((ITEM["inro"], 1), reward_money=50000, reward_exp=5000), "B")
    q["phase"] = 2
    write(270, "buried_cache_and_inro", (
        "push/270 (RUL-2026-10-25-012), all HIDDEN. Phase 1: create the Chart of the Buried Cache (OTHER, COMMON, tradable, "
        "no effect; placeholder icon = the Drowned Foundry chart) and edit the Medicine Inro's weighted cache from one roll "
        "to two (contents unchanged; Inro last written by push/253). Phase 2: create The Buried Cache, an isolated Battle "
        "Pyramid entered with that chart: the original Ghost Ship's buried-cache ending (riddle, dig, Skyglass Sentinel). "
        "Right cove: Sentinel, ladder II (2,000 exp, Sealed Treasury 2%). Wrong cove: a buried Deck Warden + Seal Charge, "
        "then the Sentinel, ladder I (1,000 exp, Treasury 1%); no loop back to the riddle. A lost fight fails the hunt "
        "(RUL-2026-10-25-010). Completion pick 1: 50,000 ryo / 5,000 exp / Medicine Inro x1. questRank B, no level gate: "
        "proposals. The Wreck's 20% drop line for this chart goes into push/263 once this create returns its id. Generated "
        "by push/skyglass_hunts.gen.py; do not hand-edit."), [chart_item, inro_edit, q])


if __name__ == "__main__":
    main()
