#!/usr/bin/env python3
"""The Driftline: Skyglass for levels 30 to 80 (dauntless's go 2026-11-09, "Build it"), all HIDDEN.

    python3 push/driftline.gen.py build      # write push/561 (3 AI records, 2 chart items, 5 quests)
    python3 push/driftline.gen.py check      # build in memory and run the checks; writes nothing

Design of record: /mnt/project-files/tnr/skyglass_band/DRIFTLINE_EVENT.md (approved), its sim SIM_RESULTS.md.
Defaults dauntless can change (coordinator note 2026-11-09): levels 30 to 80, Driftline charts untradeable,
the Tally ends in Shard of the Keel.

Source records: push/560's bundle (profile.getAi + ai.getAiProfile of the Faded Wayfinder, Faded Core Horror and
the Faded Captain's profile), plus state/driftline/faded_captain_getAi_20261109.json: the Faded Captain's
profile.getAi, verbatim from the same session's MCP answer, because 560's runner could not read that 62 KB answer
back from the transcript (MALFORMED_ELEMENT). The three Driftline records copy the live record whole (kit, rules,
stats, sprite, includeDefaultRules) and change only: name, hidden, poolsMultiplier, plus one -50% damage given row.

Changes from the design, forced by the engine:
- One pick list per quest (content.reward), so the Split Hold's two sides share one six-item pick. The side now
  chooses the last fight, not the pick.
- The Buried Cache is rank B (Genin can't start it), so Tally order 2 reads "the Split Hold or the Buried Cache".

Not in this manifest: the Faded Wreck drop rows (the Wreck is live; they go in the Friday go-live batch), the
salvager's tutorial line (the deep review thread owns her rewrite), art (placeholders until painted and uploaded
in the browser). Do not hand-edit the output.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
NUM = 561
PFX = "dl561_"
SRC_BUNDLE = "harvests/inbox/tnr_results_1794240598437.json"  # push/560
CAPTAIN_GETAI = "state/driftline/faded_captain_getAi_20261109.json"

LEVELS = (30, 80)          # dauntless's default; 30 to 79 is the other option
TRADEABLE = False          # dauntless's default: band charts untradeable
TALLY_FINAL = "Shard of the Keel"  # dauntless's default; the other option is a second Skyglass Token

# ---------------------------------------------------------------------------------------------------------------
# Live ids
# ---------------------------------------------------------------------------------------------------------------
ITEM = {
    "Tide Chart": "H1s2IwtZ5JqgPEoJ55IVj", "Watch Roster": "yE8TwzygWZSNoZD5x97rW",
    "Chart of the Buried Cache": "nbLC37UzBamthKXvZsgQB", "Chart of the Captain's Watch": "aHFNuo5RkKpDcaOBLIKiu",
    "Medicine Inro": "ixEKlJ0MmDrX7JoMNJVhi", "Elemental Tool Pouch": "D0gtI5dOgj2dFO4VexsLJ",
    "Galley Stores": "D-QTnbjgTyIVc593zzdSB", "Skyglass Token": "nzCW7A-_AuYMzBs2wClnM",
    "Skyglass Coffer": "THo7rfzP-S82_43aN8fs3", "Sealed Treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
    "Shard of the Keel": "uKnlqlfyE_k1QjLuaVml_",  # push/417 bundle tnr_results_1793716872408.json
    "Chart of the Split Hold": "@item:" + PFX + "split", "Chart of the Broken Stern": "@item:" + PFX + "stern",
}
QUEST = {  # live quest ids, for the Tally's orders
    "Wreck Sighted": "_zp1l7Y9a_77pgonAdsYx", "The Low Tide Run": "pFQBaJxU_8RSvSi4Kir1Z",
    "The Night Watch": "dnzL-bDrAEVXrKB5xariu", "The Rotted Galley": "x7ByC_5ssbpibxTB60Ag1",
    "The Buried Cache": "CgwAVCyZLgNQtEnqgLxxv", "The Drowned Foundry": "UGHSuhi83C3wRtH3FD4Eu",
    "The Captain's Watch": "liljq0yVXWTSna4X6dZE1",
}
AI = {  # existing records by literal id; the three Driftline records by @ref
    "chart:deck-warden": "3qlQV9EAnTZldvyhv3YnM", "chart:seal-charge": "lY1qD7dPuxs1rhCFFDitU",
    "chart:arsenal-keeper": "gd41Je7jTbQXjpHks1x7J", "chart:skyglass-sentinel": "TIHlWmLY6-_bykVShjoM2",
    "chart:oathkeeper": "TjKuLv6msiQ2iMyGYz0ks", "chart:first-blade": "jS-toGkHmQBKdVo2fuGwb",
    "faded:deck-warden": "q3ZuQQ52cIyB6cpTGH8lA", "faded:seal-charge": "RX4f6fhxFxgJBj_irxF18",
    "faded:oathkeeper": "y3z0Y3NTb9VS0VLWSj9Ox",
    "driftline:wayfinder": "@ai:" + PFX + "wayfinder", "driftline:core-horror": "@ai:" + PFX + "core-horror",
    "driftline:captain": "@ai:" + PFX + "captain",
}
SALVAGER = "Xugt7415D3-tepLfxpwM5"   # scene character (push/509)
SHORE = "rX78pJPETsUL2JrsSvGHn"      # the shore scene asset (push/385), dialogs only
SCENE = {  # battle boards (push/skyglass_hunts.gen.py SCENE)
    "keel_walk": "https://ui0arpl8sm.ufs.sh/f/QfsAnXSp9QG0AuwbQywCW.webp",
    "hold": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",
    "lower_hull": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi",
    "deck_b": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJcoxkatSnxBpQqGNDcTHbLmYz8uXAl3oa54ti",
    "chart_room": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJqpbYjW5dkOZgJQ8mGRcdx3SsWvPelyYFTt5V",
    "helm": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJIp0fIvxfOewksxBoS1HQCihpL7c42Ky9uUFv",
}
ICON = {  # PLACEHOLDERS (existing uploads: Galley Stores, Rotted Reliquary Seal) until new art is uploaded
    "split": "https://ui0arpl8sm.ufs.sh/f/iS35oVeCsybzoJYcfJ2xp.webp",
    "stern": "https://ui0arpl8sm.ufs.sh/f/xigFDKI7-1Qr1qgdrrpcI.webp",
    "quest": "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp",
}
STEP_EXP = {"I": 1000, "III": 3000, "IV": 4000}
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the tide takes the way back.",
          "fleeDescription": "You break away, and the tide closes behind you."}
CARD_LINE = "Levels 30 to 80. Enemies match your level. Opens to Genin and up."
RUN_RULES = ("You start every fight at full health, chakra and stamina. Lose a fight and the run ends. Claim any "
             "waiting reward first.")


# ---------------------------------------------------------------------------------------------------------------
# The three Driftline records (copies of the live Faded records)
# ---------------------------------------------------------------------------------------------------------------
COPY_FIELDS = ["level", "rank", "statsMultiplier", "regeneration", "gender", "preferredGeneral1", "preferredGeneral2",
               "primaryElement", "secondaryElement", "isSummon", "avatarFacing", "avatar", "ninjutsuMastery",
               "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery", "sageMastery", "offence",
               "defence", "strength", "intelligence", "willpower", "speed"]
CUT = {"type": "decreasedamagegiven", "power": 50, "rounds": 99, "target": "INHERIT", "direction": "offence",
       "calculation": "percentage", "description": "Decreased damage given", "powerPerLevel": 0, "appearSfx": "",
       "disappearSfx": "", "appearAnimation": "", "staticAnimation": "", "staticAssetPath": "", "disappearAnimation": ""}
RECORDS = {  # key: (new name, source userId, pools)
    "wayfinder": ("Driftline Wayfinder", "g30_Yqj_neO90g9_Dxwap", None),
    "core-horror": ("Driftline Core Horror", "XCDMY6jeLu4XXC71eVxYP", 3),
    "captain": ("Driftline Captain", "nR5okP-MiRsnSpiJQ8CM-", 2),
}
SRC_POOLS = {"wayfinder": 1, "core-horror": 6, "captain": 4}  # live values; checked against the capture


def load_sources():
    b = json.load(open(os.path.join(ROOT, SRC_BUNDLE)))
    prof, rules = {}, {}
    for c in b["captures"]:
        if not c.get("ok"):
            continue
        d = c["data"]
        d = json.loads(d) if isinstance(d, str) else d
        if c["proc"] == "profile.getAi":
            prof[d["userId"]] = d
        elif c["proc"] == "ai.getAiProfile":
            rules[d["userId"]] = d
    cap = json.load(open(os.path.join(ROOT, CAPTAIN_GETAI)))
    assert "nR5okP-MiRsnSpiJQ8CM-" not in prof
    prof[cap["userId"]] = cap
    return prof, rules


def ai_entry(key, prof, rules):
    name, uid, pools = RECORDS[key]
    p, r = prof[uid], rules[uid]
    assert p["poolsMultiplier"] == SRC_POOLS[key], (key, p["poolsMultiplier"])
    assert p["hidden"] if "hidden" in p else True
    jutsus = [j["jutsuId"] for j in p["jutsus"] if j["equipped"]]
    assert len(jutsus) == len(p["jutsus"]), key
    for rule in r["rules"]:
        jid = rule["action"].get("jutsuId")
        assert jid in (None, "basicAttack") or jid in jutsus, (key, jid)
    data = {"username": name, "hidden": True}
    data.update({f: p[f] for f in COPY_FIELDS})
    data["poolsMultiplier"] = pools if pools is not None else p["poolsMultiplier"]
    data.update({"jutsus": jutsus, "items": [], "effects": [dict(e) for e in p["effects"]] + [dict(CUT)],
                 "includeDefaultRules": r["includeDefaultRules"], "rules": r["rules"], "inArena": False})
    return {"entity": "ai", "slot": "create", "srcId": PFX + key, "phase": 1, "name": name, "data": data}


# ---------------------------------------------------------------------------------------------------------------
# The two chart items
# ---------------------------------------------------------------------------------------------------------------
ITEM_BASE = {
    "itemType": "OTHER", "slot": "NONE", "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE",
    "cost": 1, "repsCost": 0, "seichiSilverCost": 0, "stackSize": 999, "destroyOnUse": False, "range": 0,
    "chakraCost": 0, "staminaCost": 0, "healthCost": 0, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
    "healthCostReducePerLvl": 0, "actionCostPerc": 60, "battleDescription": "Treasure chest", "canStack": True,
    "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": False, "hidden": True, "maxEquips": 1,
    "preventBattleUsage": True, "requiredLevel": 1, "xpToLevel": 1000, "parentItemId": None, "requiredStrength": None,
    "requiredSpeed": None, "requiredIntelligence": None, "requiredWillpower": None, "canBeCrafted": False,
    "canBeImbued": False, "canBeHunted": False, "canBeGathered": False, "canBeTraded": TRADEABLE, "isFarmSeed": False,
    "farmGrowTimeSeconds": 0, "farmYieldItemId": None, "farmMinLevel": 1, "farmPlantExperience": 0,
    "farmHarvestExperience": 0, "farmSellValue": 0, "farmExtractSeedItemId": None, "farmExtractSeedCount": 0,
    "isFarmFertilizer": False, "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0, "craftingExperience": 0,
    "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH", "effects": [],
}  # push/536's chart create, with canBeTraded per dauntless's default

SPLIT_PICK = [("Medicine Inro", 1), ("Elemental Tool Pouch", 1), ("Galley Stores", 2),
              ("Chart of the Buried Cache", 1), ("Tide Chart", 2), ("Watch Roster", 2)]
STERN_PICK = [("Skyglass Coffer", 1), ("Skyglass Token", 1), ("Galley Stores", 3), ("Chart of the Split Hold", 2)]
BEACH_PICK = [("Tide Chart", 1), ("Watch Roster", 1), ("Chart of the Split Hold", 1), ("Medicine Inro", 1)]


def picks_txt(p):
    return " · ".join(n + (f" ×{q}" if q > 1 else "") for n, q in p)


CHARTS = {
    "split": {
        "item": "Chart of the Split Hold", "rarity": "COMMON",
        "story": "A rough sketch of the hold where the Wreck broke apart in the shallows, drawn on a plank that washed "
                 "up with the tide. The hull splits two ways at the bottom.",
        "run": "The Split Hold", "stars": "★★☆☆☆",
        "drops": "Chart of the Broken Stern 20% · Sealed Treasury 3%", "pick": SPLIT_PICK,
        "extra": "<b>At the split:</b> go port or starboard for the last fight.<br>",
    },
    "stern": {
        "item": "Chart of the Broken Stern", "rarity": "RARE",
        "story": "The stern's own deck plan, salt-stiff and torn along the keel. Someone aboard marked the helm in red "
                 "and wrote one word under it: still.",
        "run": "The Broken Stern", "stars": "★★★☆☆",
        "drops": "Chart of the Captain's Watch 5% · Sealed Treasury 4%", "pick": STERN_PICK, "extra": "",
    },
}


def item_card(c):
    trade = "" if TRADEABLE else "Can't be traded. "
    return (f"<i>{c['story']}</i><br><br><b>{c['run']}</b> · Battle Arena · The Driftline<br>{CARD_LINE}<br>"
            f"Difficulty: {c['stars']}<br>{c['extra']}<b>Chance drops:</b> {c['drops']}<br>"
            f"<b>Choose one:</b> {picks_txt(c['pick'])}<br><i>Spent when the run starts. {RUN_RULES} {trade}</i>")


def item_entry(key):
    c = CHARTS[key]
    data = dict(ITEM_BASE, name=c["item"], description=item_card(c), rarity=c["rarity"], image=ICON[key])
    return {"entity": "item", "slot": "create", "srcId": PFX + key, "phase": 1, "name": c["item"], "data": data}


# ---------------------------------------------------------------------------------------------------------------
# Objective builders
# ---------------------------------------------------------------------------------------------------------------
def dialog(i, text, choices, scene=SHORE, portrait=False):
    return {"id": i, "task": "dialog", "description": text, "sceneBackground": scene,
            "sceneCharacters": [SALVAGER] if portrait else [],
            "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}


def opp(keys):
    counts = {}
    for k in keys:
        counts[AI[k]] = counts.get(AI[k], 0) + 1
    return [{"ids": [i], "number": n, "quantity": 1} for i, n in counts.items()]


def battle(i, scene, text, keys, nxt):
    return {"id": i, "task": "start_battle", "description": text, "sceneBackground": SCENE[scene],
            "sceneCharacters": [], "opponentAIs": opp(keys), "completionOutcome": "Win", "scaleGains": 1,
            "keepOriginalPools": False, "opponent_scaled_to_user": True, "givePools": 100,
            "nextObjectiveId": nxt, "failObjectiveId": "f_lost", **SHARED}


def drop(name, chance, quantity=1):
    return {"ids": [ITEM[name]], "number": chance, "quantity": quantity}


def win(i, scene, text, exp, drops):
    return {"id": i, "task": "win_quest", "description": text, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "reward_exp": exp, "reward_items": [drop(*d) for d in drops]}


def fail(scene, text):
    return {"id": "f_lost", "task": "fail_quest", "description": text, "sceneBackground": SCENE[scene],
            "sceneCharacters": []}


# ---------------------------------------------------------------------------------------------------------------
# The five quests
# ---------------------------------------------------------------------------------------------------------------
def into():
    return [
        dialog("d_word", "The salvager is up to her knees in the surf, hauling a broken rib of the Wreck onto the sand. "
               "\"You again. Good. Look at this.\" The whole tideline is littered with planks and glass. \"She sheds "
               "when the tide pulls at her. Whole decks break off and drift in, and the crew come with them.\"",
               [("The crew?", "d_crew")], portrait=True),
        dialog("d_crew", "\"Faded ones. They don't know the ship left them behind. They keep their posts on whatever "
               "piece of her they washed in on.\" She points down the beach, where two figures stand watch on a "
               "split hatch. \"The deep decks are for Jonin. The shallows are yours. Clear those two and I'll show "
               "you where the rest of her drifted.\"", [("Clear the hatch", "b1")], portrait=True),
        battle("b1", "keel_walk", "A Deck Warden and his Seal Charge stand their post on a hatch half sunk in sand.",
               ["chart:deck-warden", "chart:seal-charge"], "w_done"),
        win("w_done", "keel_walk", "The two fade into the spray. Under the hatch you find a plank with a hold sketched "
            "on it, and the salvager whistles. \"That's the Split Hold. It came in whole. Go and see what's still "
            "in it.\" From now on she keeps the Driftline's runs for you in the Battle Arena.",
            STEP_EXP["I"], [("Chart of the Split Hold", 100)]),
        fail("keel_walk", "The tide knocks you flat, and the watch goes on without you. The salvager will wait."),
    ]


def beach():
    return [
        dialog("d_tide", "Low tide. The beach below the Wreck is a field of wreckage, and the Faded crew walk it as if "
               "it were still a deck. A Deck Warden and a Seal Charge are working their way along the tideline "
               "toward you.", [("Meet them on the sand", "b1")]),
        battle("b1", "keel_walk", "The Deck Warden calls the watch, and the Seal Charge comes in low.",
               ["chart:deck-warden", "chart:seal-charge"], "w_done"),
        win("w_done", "keel_walk", "The tideline is quiet until the next tide. You pick through what they were "
            "guarding.", STEP_EXP["I"], []),
        fail("keel_walk", "The watch drives you off the sand. The tide will turn again tomorrow."),
    ]


def split():
    return [
        dialog("d_hatch", "The Split Hold lies on its side in the shallows, the sea running in and out of it. A Faded "
               "Deck Warden keeps the hatch with a Seal Charge, both still dripping.", [("Take the hatch", "b1")],
               scene=SCENE["lower_hull"]),
        battle("b1", "lower_hull", "The Deck Warden plants himself in the hatch.",
               ["faded:deck-warden", "chart:seal-charge"], "d_stores"),
        dialog("d_stores", "Below, the stores are knee-deep in seawater. An Arsenal Keeper counts the crates that are "
               "left, and he does not like your face.", [("Go down", "b2")], scene=SCENE["hold"]),
        battle("b2", "hold", "The Arsenal Keeper reaches for his charges.", ["chart:arsenal-keeper"], "d_split"),
        dialog("d_split", "At the bottom the hull has cracked clean in two. To port, a Skyglass Sentinel and the First "
               "Blade hold the armory. To starboard, a Wayfinder bends over a soaked chart while an Oathkeeper stands "
               "over him.", [("Go port", "b3_port"), ("Go starboard", "b3_star")], scene=SCENE["hold"]),
        battle("b3_port", "deck_b", "The Sentinel's glass flares, and the First Blade steps in behind it.",
               ["chart:skyglass-sentinel", "chart:first-blade"], "w_port"),
        battle("b3_star", "chart_room", "The Wayfinder marks you on his chart, and the Oathkeeper raises his blade.",
               ["driftline:wayfinder", "chart:oathkeeper"], "w_star"),
        win("w_port", "deck_b", "The armory is yours, what the sea left of it.", STEP_EXP["III"],
            [("Sealed Treasury", 3), ("Chart of the Broken Stern", 20)]),
        win("w_star", "chart_room", "The Wayfinder's chart is ruined, but the stores behind him are not.",
            STEP_EXP["III"], [("Sealed Treasury", 3), ("Chart of the Broken Stern", 20)]),
        fail("hold", "The sea pours into the hold behind you, and the run is over."),
    ]


def stern():
    return [
        dialog("d_stern", "The Broken Stern has run aground on the bar, upright, as if she were still under way. Two "
               "Faded Deck Wardens and a Seal Charge hold the gangway.", [("Board her", "b1")],
               scene=SCENE["lower_hull"]),
        battle("b1", "lower_hull", "The Deck Wardens close ranks on the gangway.",
               ["faded:deck-warden", "faded:deck-warden", "faded:seal-charge"], "d_chart"),
        dialog("d_chart", "In the chart room a Faded Oathkeeper guards the Wayfinder, who is still plotting a course "
               "for a ship that is not moving.", [("Break the watch", "b2")], scene=SCENE["chart_room"]),
        battle("b2", "chart_room", "The Oathkeeper steps between you and the Wayfinder.",
               ["faded:oathkeeper", "driftline:wayfinder"], "d_hold"),
        dialog("d_hold", "Below, something heavy moves in the flooded hold. The Core Horror has come in with this piece "
               "of her, smaller than the one in the deep, and just as hungry. Watch the floor: red means move.",
               [("Face it", "b3")], scene=SCENE["hold"]),
        battle("b3", "hold", "The Driftline Core Horror rises out of the bilge.", ["driftline:core-horror"], "d_helm"),
        dialog("d_helm", "At the helm the Captain stands with both hands on the wheel, steering a stern that has no "
               "ship in front of it. He turns his head. \"You're not on my roster.\"", [("Take the helm", "b4")],
               scene=SCENE["helm"]),
        battle("b4", "helm", "The Driftline Captain lets go of the wheel.", ["driftline:captain"], "w_done"),
        win("w_done", "helm", "The Captain fades with his hands back on the wheel. The stern is quiet, and the tide "
            "lifts her a little, as if she were finally free to go.", STEP_EXP["IV"],
            [("Sealed Treasury", 4), ("Chart of the Captain's Watch", 5)]),
        fail("helm", "The stern keeps her crew, and you wash back up on the sand."),
    ]


def quest(key, name, objs, *, desc, success, rank="C", qtype="battlepyramid", entry=None, pick=None, prereq,
          retry="none", completes=100, levels=LEVELS, phase=3, extra=None):
    content = {"objectives": objs, "sceneBackground": SHORE, "sceneCharacters": [], "entryItems": entry or [],
               "isolated": qtype == "battlepyramid"}
    if pick:
        content.update({"rewardMode": "choose", "rewardPickCount": 1,
                        "reward": {"reward_items": [{"ids": [ITEM[n]], "number": 100, "quantity": q} for n, q in pick]}})
    else:
        content["reward"] = extra or {}
    data = {"name": name, "description": desc, "image": ICON["quest"], "questType": qtype, "questRank": rank,
            "successDescription": success, "retryDelay": retry, "attemptDelay": "none", "consecutiveObjectives": True,
            "hidden": True, "requiredLevel": levels[0], "maxLevel": levels[1], "maxAttempts": 100,
            "maxCompletes": completes, "prerequisiteQuestId": prereq, "tierLevel": None, "requiredVillage": None,
            "requiredBloodlineId": None, "startsAt": None, "endsAt": None, "content": content}
    if completes == 1 and qtype == "event":
        data["maxAttempts"] = 1
    return {"entity": "quest", "slot": "create", "srcId": PFX + "q_" + key, "phase": phase, "name": name, "data": data}


def tally():
    def order(i, text, ok, reward, quests, n, nxt):
        o = {"id": i, "task": "complete_specific_quest", "description": text, "successDescription": ok,
             "sceneBackground": "", "sceneCharacters": [], "reward_items": [drop(*r) for r in reward],
             "completeQuestIds": [QUEST.get(q) or "@quest:" + PFX + "q_" + q for q in quests], "value": n}
        if nxt:
            o["nextObjectiveId"] = nxt
        return o
    return [
        order("t_tideline", "Bring something up from the tideline.<br><br><b>Win Beachcombing, the Low Tide Run, the "
              "Night Watch or the Rotted Galley, 3 times in total.</b> Reward when you claim it: Galley Stores ×2.",
              "Three hauls off the sand. She chalks them on the hull.", [("Galley Stores", 100, 2)],
              ["beach", "The Low Tide Run", "The Night Watch", "The Rotted Galley"], 3, "t_split"),
        order("t_split", "Go into a broken hold.<br><br><b>Win the Split Hold or the Buried Cache once.</b> Reward when "
              "you claim it: an Elemental Tool Pouch.", "You came back out of the hold, which is more than most do.",
              [("Elemental Tool Pouch", 100)], ["split", "The Buried Cache"], 1, "t_foundry"),
        order("t_foundry", "Learn the ship's lower decks.<br><br><b>Win the Split Hold or the Drowned Foundry, 2 times "
              "in total.</b> Reward when you claim it: a Skyglass Coffer.", "She stops calling you new.",
              [("Skyglass Coffer", 100)], ["split", "The Drowned Foundry"], 2, "t_helm"),
        order("t_helm", "Stand at a helm.<br><br><b>Win the Broken Stern or the Captain's Watch once.</b> Reward when "
              "you claim it: a Sealed Treasury.", "A Captain fell to you. The deep decks will hear of it.",
              [("Sealed Treasury", 100)], ["stern", "The Captain's Watch"], 1, None),
    ]


TALLY_DESC = ("The salvager keeps a tally of who brings what up from the shallows. Four orders, each with a reward to "
              "claim, and a last reward for all four: one Shard of the Keel and a Skyglass Token.<br><br>"
              "<b>Orders</b>, in any order:<br>1. <b>Win Beachcombing, the Low Tide Run, the Night Watch or the Rotted "
              "Galley, 3 times in total.</b><br>2. <b>Win the Split Hold or the Buried Cache once.</b><br>3. <b>Win the "
              "Split Hold or the Drowned Foundry, 2 times in total.</b><br>4. <b>Win the Broken Stern or the Captain's "
              "Watch once.</b><br><br>Every order has a level-80 run beside it, so the tally still counts after you "
              "pass 80. Orders count only once you've taken the tally.")


def build():
    prof, rules = load_sources()
    items = [ai_entry(k, prof, rules) for k in RECORDS] + [item_entry(k) for k in CHARTS]
    intro = ("<br><br><i>" + CARD_LINE + " " + RUN_RULES + "</i>")
    items.append(quest("into", "Into the Driftline", into(), prereq=QUEST["Wreck Sighted"], completes=1, phase=2,
                       desc="The salvager has found something on the beach below the Wreck: pieces of her, broken off "
                            "and drifted ashore, with Faded crew still standing their posts. She wants you to see."
                            + intro,
                       success="The salvager showed you the Driftline. Its runs wait for you in the Battle Arena."))
    ref = "@quest:" + PFX + "q_into"
    items.append(quest("beach", "Beachcombing", beach(), prereq=ref, retry="daily", pick=BEACH_PICK,
                       desc="Every tide leaves more of the Wreck on the sand, and more of her crew walking it. Once a "
                            "day, walk the tideline and take what they guard." + intro,
                       success="You walked the tideline and came back with the tide's leavings."))
    items.append(quest("split", "The Split Hold", split(), prereq=ref, pick=SPLIT_PICK,
                       entry=[{"ids": [ITEM["Chart of the Split Hold"]], "number": 1}],
                       desc="A whole hold broke off the Wreck and drifted into the shallows. Three fights, and at the "
                            "bottom the hull splits: port or starboard." + intro,
                       success="You came up out of the Split Hold with what the sea had left."))
    items.append(quest("stern", "The Broken Stern", stern(), prereq=ref, pick=STERN_PICK,
                       entry=[{"ids": [ITEM["Chart of the Broken Stern"]], "number": 1}],
                       desc="The Wreck's stern ran aground on the bar, upright and crewed, with its Captain still at the "
                            "helm. Four fights: the gangway, the chart room, the hold and the helm." + intro,
                       success="The Broken Stern is quiet, and its Captain has let go of the wheel."))
    final = {"reward_items": [{"ids": [ITEM[TALLY_FINAL]], "number": 100, "quantity": 1},
                              {"ids": [ITEM["Skyglass Token"]], "number": 100, "quantity": 1}]}
    items.append(quest("tally", "The Salvager's Tally", tally(), prereq=ref, qtype="event", rank="D", completes=1,
                       levels=(LEVELS[0], 100), desc=TALLY_DESC, extra=final,
                       success="Tally complete. The salvager presses a shard of the keel into your hand. \"You've earned "
                               "the deep. Don't drown in it.\""))
    return items


# ---------------------------------------------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------------------------------------------
def check_graph(name, objs):
    ids = [o["id"] for o in objs]
    assert len(set(ids)) == len(ids), name
    by = {o["id"]: o for o in objs}
    incoming = set()
    for o in objs:
        nxt = o.get("nextObjectiveId")
        nx = [x["nextObjectiveId"] for x in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])
        if o.get("failObjectiveId"):
            nx.append(o["failObjectiveId"])
        for n in nx:
            assert n in by, (name, o["id"], n)
            incoming.add(n)
    starts = [i for i in ids if i not in incoming]
    assert len(starts) == 1, (name, starts)
    if by[ids[0]]["task"] == "complete_specific_quest":
        return
    # every battle is preceded by a dialog (pack 3.7), never by another battle
    for o in objs:
        nxt = o.get("nextObjectiveId")
        nx = [x["nextObjectiveId"] for x in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])
        if o["task"] == "start_battle":
            assert o["failObjectiveId"] and o["givePools"] == 100 and o["opponent_scaled_to_user"], (name, o["id"])
            for n in nx:
                assert by[n]["task"] != "start_battle", (name, o["id"], n)
    assert any(o["task"] == "win_quest" for o in objs) and any(o["task"] == "fail_quest" for o in objs), name


def check(items):
    for d in (QUEST,):
        for v in d.values():
            assert NANO.match(v), v
    for k, v in ITEM.items():
        assert NANO.match(v) or v.startswith("@item:" + PFX), (k, v)
    for k, v in AI.items():
        assert NANO.match(v) or v.startswith("@ai:" + PFX), (k, v)
    text = json.dumps(items, ensure_ascii=False)
    assert "—" not in text and "–" not in text, "em/en dash"
    for it in items:
        if it["entity"] == "quest":
            check_graph(it["name"], it["data"]["content"]["objectives"])
            assert it["data"]["hidden"] is True
        else:
            assert it["data"]["hidden"] is True, it["name"]
    for it in items:
        if it["entity"] == "ai":
            cut = [e for e in it["data"]["effects"] if e["type"] == "decreasedamagegiven"]
            assert len(cut) == 1 and cut[0]["power"] == 50, it["name"]
    cap = [it for it in items if it["srcId"] == PFX + "captain"][0]
    assert any(e["type"] == "stunprevent" for e in cap["data"]["effects"])


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode not in ("build", "check"):
        print(__doc__)
        sys.exit(2)
    items = build()
    check(items)
    for it in items:
        extra = ""
        if it["entity"] == "ai":
            d = it["data"]
            extra = f"pools {d['poolsMultiplier']}, {len(d['jutsus'])} jutsu, {len(d['rules'])} rules"
        elif it["entity"] == "quest":
            extra = f"{len(it['data']['content']['objectives'])} objectives"
        print(f"  {it['entity']:5} {it['name']}: {extra}")
    if mode == "check":
        return
    m = {"_note": (f"push/{NUM}, HIDDEN: The Driftline, Skyglass for levels 30 to 80 (dauntless's go 2026-11-09, 'Build "
                   "it'). Three AI copies of the live Faded Wayfinder, Core Horror and Captain (kit, rules and sprite "
                   "copied whole from push/560's capture; -50% damage given; Core Horror pools 6 -> 3, Captain 4 -> 2, "
                   "stun immunity kept). Two untradeable chart items (Chart of the Split Hold, Chart of the Broken "
                   "Stern; placeholder icons). Five quests: Into the Driftline (one-time, after Wreck Sighted), "
                   "Beachcombing (daily), The Split Hold, The Broken Stern (chart runs), The Salvager's Tally. Every "
                   "fight scaled to the player with a full refill (givePools 100); a lost fight ends the run. Nothing "
                   "visible to players. Faded Wreck drop rows and the unhide are the Friday go-live batch. Generated "
                   "by push/driftline.gen.py; do not hand-edit."),
         "dedupNames": True, "items": items}
    path = os.path.join(ROOT, "push", f"{NUM}_driftline_build.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items), "items")


if __name__ == "__main__":
    main()
