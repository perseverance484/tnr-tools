#!/usr/bin/env python3
"""Skyglass: three new charts and their Battle Arena runs (director 2026-11-09), all HIDDEN.

    python3 push/skyglass_new_charts.gen.py items                         # write push/536 (the three chart items)
    python3 push/skyglass_new_charts.gen.py runs --items <536 bundle>     # write push/537 (the three runs), AFTER 536 ran
    python3 push/skyglass_new_charts.gen.py runs --stand-in               # TEST ONLY: made-up chart ids, prints, writes nothing

  Chart of the Spoiled Hold   Rare (A). Skyglass Wreck clear. Entry: the chart + 2 Core Rot. Fixed Veteran / Rot-Touched
                              records. A wall of rot before the boss: burn it out (one more fight, 1 Core Rot back) or go
                              around it. Director 2026-11-09: "Burn the rot out only returns 1 and adds an extra combat".
  Chart of the Rotted Galley  Common (C). Faded Wreck and Skyglass Wreck clears. Scaled Common crew copies.
  Chart of the Glass Nursery  Epic (S). Skyglass Wreck clear and Crownhold's ending. Veteran echo records. Foreshadows Sayo
                              (EVENT_MAP gap G1) without naming her.

Design of record: the proposals doc (Claude Doc "Skyglass: new chart drop proposals", 2026-11-09) and the director's
2026-11-09 message. Every enemy is an existing record, by literal id from push/354 and push/355 (`_ai_keys`); no AI is
created. Item ids from push/skyglass_charts.gen.py ITEM, design_data.json and the uber shard bundle. Icons are
PLACEHOLDERS (existing uploaded chart and item icons): new art goes up later in the browser (the MCP host cannot
upload). Drop rows on the Wrecks and Crownhold, and the unhide, are separate go-live manifests on the director's go.
Do not hand-edit the output.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
NUM_ITEMS, NUM_RUNS = 536, 537
PFX = "sg536_"

# ---------------------------------------------------------------------------------------------------------------
# Live ids (verified against the repo's committed manifests and bundles, 2026-11-09)
# ---------------------------------------------------------------------------------------------------------------
ITEM = {
    "Core Rot": "KuqLeFB12BdB-0s5O1udk", "Galley Stores": "D-QTnbjgTyIVc593zzdSB",
    "Skyglass Token": "nzCW7A-_AuYMzBs2wClnM", "Medicine Inro": "ixEKlJ0MmDrX7JoMNJVhi",
    "Skyglass Coffer": "THo7rfzP-S82_43aN8fs3", "Sealed Treasury": "Ma8S90Nmbi0Xvm4u4FzJh",
    "Archive Chart Case": "B48dTRsoLJGKBWIUbeUoG", "Chart of the Buried Cache": "nbLC37UzBamthKXvZsgQB",
    "The Rotted Heading": "U2yJbBM6_N1xBBf0ez96F", "Rotted Reliquary Seal": "2sGi5SZXh2UutHmM-mIMD",
    "Shard of the Tide": "KHGZAfQFosLQJ29AN2ymC",
    "Ledger Page: The Trophy Hold": "JvrytTOdR1voVCoo3fckK", "Ledger Page: The Bone Store": "uu6ETQimuBJ69jwr76IIi",
    "Ledger Page: The Snare Room": "6QgcnW0v6gZeHY474BjR0", "Stores Manifest: The Overgrown Stores": "nLG6TK48xlyZ_t9R28QsY",
    "Stores Manifest: The Ore Vault": "9j4IErGW1gmZ-5FNjZMEQ", "Stores Manifest: The Bloom Cellar": "7Sz2ttMScKH8b10XYS12I",
}
HAUL_PAGES = [n for n in ITEM if n.startswith(("Ledger Page", "Stores Manifest"))]

AI = {  # push/354 and push/355 `_ai_keys`
    "common:deck-warden": "3qlQV9EAnTZldvyhv3YnM", "common:arsenal-keeper": "gd41Je7jTbQXjpHks1x7J",
    "common:oathkeeper": "TjKuLv6msiQ2iMyGYz0ks", "common:first-blade": "jS-toGkHmQBKdVo2fuGwb",
    "veteran:deck-warden": "qCIur1yRxxbqXhVigb-kz", "veteran:seal-charge": "QPWVE_l2ReFPPzf-u6jai",
    "veteran:sealwright-echo": "V1MlOpuen59Qlmscpni3Z", "veteran:first-blade-echo": "j3oNQLeCMEkrU6rH070eF",
    "oneoff:lingering-echo-i": "tAIANvBBijQ-TSUzkVwek", "oneoff:lingering-echo-ii": "kw5VgfWtdfOZkPY5r1eZg",
    "rot:skyglass-sentinel": "KsQdeJQVn_mmxrcv3pOPt", "rot:foundry-warden": "ySwv3MDO5a-fzUF99M3pi",
    "rot:core-horror": "FOsjvngwJvZ8uXJI6q76T",
}

SCENE = {  # push/skyglass_hunts.gen.py SCENE (uploaded boards)
    "hold": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJTdaBvI5IU29dZYJPoOKSh5vmlqatMub3EigH",
    "lower_hull": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ0pHtoKgrYldRWJcD6vE10SjNsXHeA9pVMfQi",
    "reconstruction_chamber": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJRiFRQZ0udmODoNtpa0FMcwI4k2Eq7nJhyvjl",
    "deck_b": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJcoxkatSnxBpQqGNDcTHbLmYz8uXAl3oa54ti",
    "command_observation_gallery": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ8ZwqPukkp45TvAnoIBa0rtCf1lbyXYjVKQ2q",
}
# Placeholder icons until new art is uploaded: Rotted Reliquary Seal, Galley Stores, Reliquary Seal.
ICON = {
    "spoiled": "https://ui0arpl8sm.ufs.sh/f/xigFDKI7-1Qr1qgdrrpcI.webp",
    "galley": "https://ui0arpl8sm.ufs.sh/f/iS35oVeCsybzoJYcfJ2xp.webp",
    "nursery": "https://ui0arpl8sm.ufs.sh/f/GnbyPivtXnCa3YLP97KfO.webp",
}
STEP_EXP = {"II": 2000, "IV": 4000, "VI": 5000}
STEP_N = {"II": 2, "IV": 4, "VI": 6}
FOOTER = ("<i>Spent when the run starts. No refills between fights; once inside, you leave by winning, falling or "
          "abandoning. Claim any waiting reward first.</i>")
CLAIM_LINE = "Claim any reward choice still waiting from an earlier run before you set out."
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the chart's way closes.",
          "fleeDescription": "You break away, and the way back closes behind you."}

# ---------------------------------------------------------------------------------------------------------------
# The three charts
# ---------------------------------------------------------------------------------------------------------------
CHARTS = {
    "spoiled": {
        "item": "Chart of the Spoiled Hold", "quest": "The Spoiled Hold", "rarity": "RARE", "rank": "A",
        "scaled": False, "step": "IV", "pickCount": 1,
        "entry": [("chart", 1), ("Core Rot", 2)],
        "story": "The bottom half of the rotted page, where the brush ran down into the deep hold. Every room it marks "
                 "has gone soft and green.",
        "stars": "★★★☆☆",
        "pick": [("Skyglass Coffer", 1), ("Archive Chart Case", 1), ("Skyglass Token", 1)],
        "ending": [("The Rotted Heading", 10), ("Rotted Reliquary Seal", 10)] + [(p, 1.5) for p in HAUL_PAGES],
        "extra_card": "<b>Entry:</b> this chart and 2 Core Rot.<br>",
        "route_card": "<b>Burn the rot out:</b> one more fight, and 1 Core Rot back.<br>",
        "desc": "The rotted page points down, past the Foundry, to the deep hold where the Core's rot first took. The "
                "crew still stand their posts down there, and the rot stands with them.",
        "success": "You climbed out of the deep hold with the rot's best-kept stores.",
    },
    "galley": {
        "item": "Chart of the Rotted Galley", "quest": "The Rotted Galley", "rarity": "COMMON", "rank": "C",
        "scaled": True, "step": "II", "pickCount": 1,
        "entry": [("chart", 1)],
        "story": "A cook's list of the galley's cold stores, crossed out line by line as the rot got into each one.",
        "stars": "★★☆☆☆",
        "pick": [("Galley Stores", 2), ("Medicine Inro", 1), ("Chart of the Buried Cache", 1)],
        "ending": [("Core Rot", 25)],
        "desc": "The galley's stores list ends in a stain where the rot got into the cold room. The cooks are still at "
                "work, feeding a crew that has not eaten in a generation.",
        "success": "You left the galley with what the rot hadn't reached.",
    },
    "nursery": {
        "item": "Chart of the Glass Nursery", "quest": "The Glass Nursery", "rarity": "EPIC", "rank": "S",
        "scaled": False, "step": "VI", "pickCount": 1,
        "entry": [("chart", 1)],
        "story": "A plan of a room below the reliquary that the ship's builders never drew. Someone pressed a small "
                 "thumbprint into its corner while the ink was still wet.",
        "stars": "★★★☆☆",
        "pick": [("Skyglass Coffer", 2), ("Skyglass Token", 2)],
        "ending": [("Shard of the Tide", 40)],
        "desc": "Below the reliquary there is a room the ship's builders never drew. The plan was made later, by a "
                "careful hand, and the room is still being kept.",
        "success": "You left the nursery with the glass still humming behind you.",
    },
}


def dialog(i, scene, desc, choices, reward_items=None):
    o = {"id": i, "task": "dialog", "description": desc, "sceneBackground": SCENE[scene], "sceneCharacters": [],
         "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}
    if reward_items:
        o["reward_items"] = reward_items
    return o


def opp(keys):
    counts = {}
    for k in keys:
        counts[AI[k]] = counts.get(AI[k], 0) + 1
    return [{"ids": [i], "number": n, "quantity": 1} for i, n in counts.items()]


def battle(i, scene, desc, keys, scaled, nxt):
    return {"id": i, "task": "start_battle", "description": desc, "sceneBackground": SCENE[scene],
            "sceneCharacters": [], "opponentAIs": opp(keys), "completionOutcome": "Win", "scaleGains": 1,
            "keepOriginalPools": False, "opponent_scaled_to_user": scaled, "nextObjectiveId": nxt,
            "failObjectiveId": "f_lost", **SHARED}


def drop(name, chance, quantity=1):
    return {"ids": [ITEM[name]], "number": chance, "quantity": quantity}


def win(i, scene, desc, c, extra=()):
    return {"id": i, "task": "win_quest", "description": desc, "sceneBackground": SCENE[scene], "sceneCharacters": [],
            "reward_exp": STEP_EXP[c["step"]],
            "reward_items": [drop("Sealed Treasury", STEP_N[c["step"]])] + [drop(n, p) for n, p in c["ending"]]
                            + [drop(n, p, q) for n, p, q in extra]}


def fail(scene, desc):
    return {"id": "f_lost", "task": "fail_quest", "description": desc, "sceneBackground": SCENE[scene],
            "sceneCharacters": []}


def spoiled(c):
    s = c["scaled"]
    return [
        dialog("d_bilge", "lower_hull", "The bilge is ankle-deep in green water. A Deck Warden wades through it on his "
               "rounds with a Seal Charge bobbing at his heel, and the boards bend under him like wet bread.",
               [("Break his round", "b1")]),
        battle("b1", "lower_hull", "The Deck Warden and his Seal Charge hold the bilge.",
               ["veteran:deck-warden", "veteran:seal-charge"], s, "d_stores"),
        dialog("d_stores", "hold", "The stores beyond have gone soft. Crates sag into the deck, and a Skyglass Sentinel "
               "stands guard over them, its glass clouded through with rot.", [("Clear the stores", "b2")]),
        battle("b2", "hold", "The Rot-Touched Sentinel steps off its post.",
               ["rot:skyglass-sentinel", "veteran:seal-charge"], s, "d_wall"),
        dialog("d_wall", "hold", "At the bottom of the hold the rot has grown into a wall of wet timber and cloudy "
               "skyglass, knit together. Behind it something large is still being rebuilt. You can burn the rot out and "
               "take what feeds it, or find a way around.",
               [("Burn the rot out", "b_burn"), ("Go around it", "d_around")]),
        battle("b_burn", "hold", "The burning wall stands up and fights back.", ["rot:foundry-warden"], s,
               "d_ash"),
        dialog("d_ash", "hold", "The wall falls into ash, and a lump of Core Rot rolls loose from it, still warm. Beyond "
               "the ash, the Core Horror is pulling itself out of the frame.", [("Face the Core Horror", "b_boss_burn")]),
        battle("b_boss_burn", "hold", "The Rot-Touched Core Horror rises, dripping green.", ["rot:core-horror"], s,
               "w_burn"),
        dialog("d_around", "hold", "You find a crawlway along the keel and come out behind the wall, where the Core "
               "Horror is pulling itself out of the frame.", [("Face the Core Horror", "b_boss")]),
        battle("b_boss", "hold", "The Rot-Touched Core Horror rises, dripping green.", ["rot:core-horror"], s,
               "w_around"),
        win("w_burn", "hold", "The Core Horror sinks back into the rot, and the wall you burned stays burned. You carry "
            "the stores out, and the warm lump of Core Rot with them.", c, extra=[("Core Rot", 100, 1)]),
        win("w_around", "hold", "The Core Horror sinks back into the rot. The deep hold's stores are yours.", c),
        fail("lower_hull", "The rot closes over you, and the hold takes back what you came for."),
    ]


def galley(c):
    s = c["scaled"]
    return [
        dialog("d_galley", "deck_b", "The galley fires are still lit. An Arsenal Keeper counts sacks of rice gone black, "
               "checking them off a list no one will read.", [("Stop the count", "b1")]),
        battle("b1", "deck_b", "The Arsenal Keeper reaches for his charges.", ["common:arsenal-keeper"], s, "d_mess"),
        dialog("d_mess", "deck_b", "In the mess, a Deck Warden and an Oathkeeper sit at a table set for forty, waiting "
               "for a meal that keeps spoiling on the plates.", [("Clear the mess", "b2")]),
        battle("b2", "deck_b", "They stand, as if the bell had rung.", ["common:deck-warden", "common:oathkeeper"], s,
               "d_cold"),
        dialog("d_cold", "hold", "The cold room is the worst of it, green to the ceiling. The First Blade guards the last "
               "good stores, as if someone might still come down for them.", [("Take the cold room", "b3")]),
        battle("b3", "hold", "The First Blade draws.", ["common:first-blade"], s, "w_done"),
        win("w_done", "hold", "The cold room is quiet. You carry out what the rot hadn't reached yet.", c),
        fail("deck_b", "The galley keeps you, and the stores stay where they are."),
    ]


def nursery(c):
    s = c["scaled"]
    return [
        dialog("d_door", "reconstruction_chamber", "The door is skyglass, soft at the edges as if it were poured "
               "yesterday. Small thumbprints are pressed into it in a neat row, one for every frame in the room beyond.",
               [("Go in", "b1")]),
        battle("b1", "reconstruction_chamber", "The Sealwright's echo steps out of the nearest frame to stop you.",
               ["veteran:sealwright-echo", "oneoff:lingering-echo-i"], s, "d_rows"),
        dialog("d_rows", "reconstruction_chamber", "Rows of frames stand in the dark, each holding a face, half set. "
               "Somewhere a woman is humming. Every time you move, the humming stops, and a voice says, kindly, "
               "'Hold still.'", [("Read the labels", "d_labels"), ("Follow the humming", "d_hum")]),
        dialog("d_labels", "command_observation_gallery", "Each frame has a label in the same neat hand: a name, a date "
               "and one word. Nearly all of them carry the same date. The word is always 'kept.'", [("Go on", "b2")]),
        dialog("d_hum", "command_observation_gallery", "The humming leads to an empty chair beside the largest frame. A "
               "folded fan lies on the seat. The glass in the frame is still warm, as if someone had just been leaning "
               "on it.", [("Go on", "b2")]),
        battle("b2", "command_observation_gallery", "The First Blade's echo comes out of the warm frame, and it does "
               "not blink.", ["veteran:first-blade-echo", "oneoff:lingering-echo-ii"], s, "w_done"),
        win("w_done", "command_observation_gallery", "The echoes break, and the frames fill again behind you, one face "
            "at a time. On your way out you notice a new thumbprint in the soft glass of the door. It is yours.", c),
        fail("reconstruction_chamber", "You hold still. The humming starts again."),
    ]


BUILD = {"spoiled": spoiled, "galley": galley, "nursery": nursery}


# ---------------------------------------------------------------------------------------------------------------
# Item cards (the live chart card layout: story, run, difficulty, drops, picks, footer)
# ---------------------------------------------------------------------------------------------------------------
def fmt_pct(p):
    return f"{p:g}%"


def card(key):
    c = CHARTS[key]
    drops = [(n, p) for n, p in c["ending"] if n not in HAUL_PAGES]
    drop_txt = [f"{n} {fmt_pct(p)}" for n, p in drops]
    if any(n in HAUL_PAGES for n, _ in c["ending"]):
        drop_txt.append("each Ledger Page and Stores Manifest 1.5%")
    drop_txt.append(f"Sealed Treasury {STEP_N[c['step']]}%")
    picks = " · ".join(n + (f" ×{q}" if q > 1 else "") for n, q in c["pick"])
    return (f"<i>{c['story']}</i><br><br><b>{c['quest']}</b> · Battle Arena<br>Difficulty: {c['stars']}<br>"
            + c.get("extra_card", "")
            + f"<b>Chance drops:</b> {' · '.join(drop_txt)}<br><b>Choose one:</b> {picks}<br>"
            + c.get("route_card", "") + FOOTER)


ITEM_BASE = {
    "itemType": "OTHER", "slot": "NONE", "cooldown": 0, "weaponType": "NONE", "target": "SELF", "method": "SINGLE",
    "cost": 1, "repsCost": 0, "seichiSilverCost": 0, "stackSize": 999, "destroyOnUse": False, "range": 0,
    "chakraCost": 0, "staminaCost": 0, "healthCost": 0, "staminaCostReducePerLvl": 0, "chakraCostReducePerLvl": 0,
    "healthCostReducePerLvl": 0, "actionCostPerc": 60, "battleDescription": "Treasure chest", "canStack": True,
    "maxImbueNumber": 1, "maxDurability": 100, "inShop": False, "isEventItem": False, "hidden": True, "maxEquips": 1,
    "preventBattleUsage": True, "requiredLevel": 1, "xpToLevel": 1000, "parentItemId": None, "requiredStrength": None,
    "requiredSpeed": None, "requiredIntelligence": None, "requiredWillpower": None, "canBeCrafted": False,
    "canBeImbued": False, "canBeHunted": False, "canBeGathered": False, "canBeTraded": True, "isFarmSeed": False,
    "farmGrowTimeSeconds": 0, "farmYieldItemId": None, "farmMinLevel": 1, "farmPlantExperience": 0,
    "farmHarvestExperience": 0, "farmSellValue": 0, "farmExtractSeedItemId": None, "farmExtractSeedCount": 0,
    "isFarmFertilizer": False, "farmTimeReductionSeconds": 0, "farmFertilizerExperience": 0, "craftingExperience": 0,
    "crystalTargetTypes": None, "bloodlineId": None, "battleUsageType": "BOTH", "effects": [],
}  # push/329's chart create (tradeable, unusable in battle, hidden on create)


def item_entry(key):
    c = CHARTS[key]
    data = dict(ITEM_BASE, name=c["item"], description=card(key), rarity=c["rarity"], image=ICON[key])
    return {"entity": "item", "slot": "create", "srcId": PFX + key, "phase": 1, "name": c["item"], "data": data}


def quest_entry(key, chart_id):
    c = CHARTS[key]
    entry = [{"ids": [chart_id if n == "chart" else ITEM[n]], "number": q} for n, q in c["entry"]]
    objs = BUILD[key](c)
    reward = {"reward_items": [{"ids": [ITEM[n]], "number": 100, "quantity": q} for n, q in c["pick"]]}
    return {"entity": "quest", "slot": "create", "srcId": f"sg537_{key}", "name": c["quest"], "data": {
        "name": c["quest"], "description": c["desc"] + "\n\n" + CLAIM_LINE, "image": ICON[key],
        "questType": "battlepyramid", "questRank": c["rank"], "successDescription": c["success"],
        "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
        "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100, "prerequisiteQuestId": None,
        "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objs, "sceneBackground": "", "sceneCharacters": [], "entryItems": entry,
                    "isolated": True, "rewardMode": "choose", "rewardPickCount": c["pickCount"], "reward": reward}}}


# ---------------------------------------------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------------------------------------------
def check_graph(key, objs):
    ids = {o["id"] for o in objs}
    assert len(ids) == len(objs), key
    seen, todo = set(), [objs[0]["id"]]
    by = {o["id"]: o for o in objs}
    while todo:
        i = todo.pop()
        if i in seen:
            continue
        seen.add(i)
        o = by[i]
        nxt = o.get("nextObjectiveId")
        nxts = [x["nextObjectiveId"] for x in nxt] if isinstance(nxt, list) else ([nxt] if nxt else [])
        if o.get("failObjectiveId"):
            nxts.append(o["failObjectiveId"])
        for n in nxts:
            assert n in ids, (key, i, n)
            todo.append(n)
    assert seen == ids, (key, ids - seen)
    assert any(o["task"] == "win_quest" for o in objs) and any(o["task"] == "fail_quest" for o in objs), key
    for o in objs:
        for t in ("description",):
            assert "—" not in o[t] and "–" not in o[t], (key, o["id"])


def check_ids():
    for d in (ITEM, AI):
        for k, v in d.items():
            assert NANO.match(v), (k, v)


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/skyglass_new_charts.gen.py; do not hand-edit.", "dedupNames": True}
    m.update(extra or {})
    m["items"] = items
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(os.path.relpath(path, ROOT), len(items), "items")


def chart_ids_from_bundle(path):
    b = json.load(open(path))
    out = {}
    for e in b["entries"]:
        src = e.get("srcId") or ""
        if src.startswith(PFX):
            assert e["state"] == "ok" and NANO.match(e["id"]), (src, e.get("state"))
            out[src[len(PFX):]] = e["id"]
    assert set(out) == set(CHARTS), out
    return out


def main():
    check_ids()
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "items":
        write(NUM_ITEMS, "skyglass_new_charts_items",
              "push/536, HIDDEN: three new Skyglass charts (director 2026-11-09): Chart of the Spoiled Hold (Rare), "
              "Chart of the Rotted Galley (Common), Chart of the Glass Nursery (Epic). Tradeable, unusable in battle, "
              "stack 999, the live chart card layout. Icons are PLACEHOLDERS (existing uploads) until new art is "
              "uploaded in the browser. push/537 (the runs) is built from this manifest's results bundle.",
              [item_entry(k) for k in CHARTS])
        return
    if mode == "runs":
        if "--stand-in" in sys.argv:
            ids = {k: f"STANDIN_{k}".ljust(21, "x")[:21] for k in CHARTS}
        else:
            ids = chart_ids_from_bundle(sys.argv[sys.argv.index("--items") + 1])
        items = [quest_entry(k, ids[k]) for k in CHARTS]
        for it in items:
            check_graph(it["name"], it["data"]["content"]["objectives"])
        if "--stand-in" in sys.argv:
            for it in items:
                print(it["name"], len(it["data"]["content"]["objectives"]), "objectives (stand-in, not written)")
            return
        write(NUM_RUNS, "skyglass_new_chart_runs",
              "push/537, HIDDEN: the three new chart runs (isolated Battle Pyramids entered with their chart, spent at "
              "start; a lost fight fails the run; completion pick). The Spoiled Hold also takes 2 Core Rot at entry "
              "and offers 'Burn the rot out' (one more fight, 1 Core Rot back; director 2026-11-09) or 'Go around it'. "
              "Enemies are existing records by literal id (push/354, push/355 `_ai_keys`); no AI is created. Quest "
              "icons are placeholders.", items,
              {"_chart_ids": ids, "_ai_keys": {k: AI[k] for k in AI}})
        return
    print(__doc__)
    sys.exit(2)


if __name__ == "__main__":
    main()
