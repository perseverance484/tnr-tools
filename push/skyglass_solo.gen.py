#!/usr/bin/env python3
"""Skyglass solo chart grind: two Battle Pyramids that mirror the Wreck for players without a party (RUL-2026-10-31-088).

    python3 push/skyglass_solo.gen.py --copies <344 bundle> [--copies <bundle> ...] [--name FULL --faded-name FADED]
        -> push/393_skyglass_solo_pyramids.json   (2 battlepyramid quest creates, HIDDEN: everything ships hidden, L13)
    python3 push/skyglass_solo.gen.py --unhide <393 bundle>
        -> push/394_skyglass_solo_unhide.json     (2 quest edits, hidden false; literal ids from 393's results, L01)

Design (director, 2026-10-31: "a way for them to grind charts like the wreck, a real source. Maybe a battle pyramid";
"Leave it unlimited ... the concept is approved"):
  * Battle Arena > Battle Pyramid. Solo, isolated, free to enter (no entryItems). maxAttempts / maxCompletes 100, the
    write schema's ceiling; battlepyramid is in QuestTypesWithMaxAttempts, so 100 runs per player lifetime is the engine
    limit (theninjarpg@3314d122 libs/quest.ts ~2504-2516). retryDelay none (unlimited inside that cap).
  * Five dialog-gated fights mirroring the Wreck's floors: crew, crew, crew, the Core as a stage boss, an officer pair.
    Every enemy is a Common-chart copy (common:<crew>) or the Steeping Horror, all `opponent_scaled_to_user`, so one
    roster serves both tiers. Health and chakra carry (isolated battlepyramid). Not simulated: win rate unmeasured.
  * The ending rolls the Wreck's chart table, lower so the party Wreck stays the faster farm. Wreck-only: variants,
    the Little Horror jar, Haul pages, the Lantern, the Treasury.
  * Names are placeholders until the director picks (`--name`, `--faded-name`).

Do not hand-edit the output.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
import skyglass_aikeys as K  # noqa: E402

NUM, PFX = 393, "sg393_"
DESIGN = os.path.join(ROOT, "state/skyglass_design/design_data.json")
BUNDLE_329 = os.path.join(ROOT, "harvests/inbox/tnr_results_1793424666625.json")
BLANK = "1YXbXYW2wz3GETVMb6DT6"  # blank scene character (push/383-385)
ICON = "https://ui0arpl8sm.ufs.sh/f/c4jsXOv_HYS6MfbL01kbb.webp"  # placeholder: the Low Tide Run's icon until art lands
S = {"lower_hull": "dFwyPzyhUZQjDBXpJRUDJ", "deck_b": "U2pjcM1_N-HdVf928Sn5z", "hold": "yufttCkG-KsefHKuz9Q2a",
     "reconstruction_chamber": "81DATu13hATfbkPuLT54E", "helm": "-eB0frmTJss6Uco6ZoM07",
     "cache_site": "rX78pJPETsUL2JrsSvGHn"}  # push/339 SCENE_ASSET

# (dialog id, scene, dialog text, choice, battle text, AI keys)
FIGHTS = [
    ("d_breach", "lower_hull",
     "The hull has split along the keel, and the gap is wide enough to climb through. Inside, the Core holds the deck the "
     "way it was: dry, lamplit, ready for sea. The watch has not been relieved in decades. It is not about to be relieved by you.",
     "Climb in through the keel", "A Deck Warden calls the alarm. A seal charge is already rolling.",
     ["common:deck-warden", "common:seal-charge"]),
    ("d_deck", "deck_b",
     "The gun deck is quiet. The Sentinel at the stair has not moved in years, and the skyglass has grown over its feet. "
     "The First Blade sits on a powder keg beside it, waiting for anything new.",
     "Take the stair", "The skyglass cracks as the Sentinel steps free. The First Blade stands.",
     ["common:skyglass-sentinel", "common:first-blade"]),
    ("d_hold", "hold",
     "The hold smells of tar and rot. An Oathkeeper stands guard over the stores, reciting the ship's articles to a Deck "
     "Warden who long ago stopped listening.",
     "Cross the hold", "The Oathkeeper stops mid-article. \"Boarders,\" he says, as if he has been hoping.",
     ["common:oathkeeper", "common:deck-warden"]),
    ("d_core", "reconstruction_chamber",
     "The Core chamber hums. Something has steeped in the cracked crystal so long that it has grown a shape, and the shape "
     "has noticed you.",
     "Go to the Core", "The Core spits out what it has been growing.",
     ["oneoff:steeping-horror"]),
    ("d_helm", "helm",
     "The last stair opens onto the helm. The Arsenal Keeper has loaded every gun aft, and a Deck Warden holds the wheel "
     "on a heading nobody has changed in decades.",
     "Take the helm", "The Arsenal Keeper turns the guns inboard.",
     ["common:arsenal-keeper", "common:deck-warden"]),
]
SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the Core pushes you out.",
          "fleeDescription": "You break away, and the hull closes behind you."}

# design_data key (or literal key), chance per clear
FULL_DROPS = [("chart_buried_cache", 15), ("chart_tide", 15), ("chart_drowned_foundry", 8), ("chart_watch_roster", 10),
              ("chart_quarantined_archive", 4), ("chart_captains_watch", 4), ("core_rot", 10)]
FADED_DROPS = [("chart_tide", 28), ("chart_watch_roster", 20), ("galley_stores", 16), ("chart_buried_cache", 12)]  # ~80% of the live Faded Wreck (RUL-089)

TIERS = {
    "full": {"level": 80, "exp": 1000, "ryo": 25000, "drops": FULL_DROPS,
             "blurb": "For level 80 and up. Drops the Skyglass Wreck's charts and Core Rot."},
    "faded": {"level": 30, "exp": 500, "ryo": 25000, "drops": FADED_DROPS,
              "blurb": "For level 30 and up. Drops the Faded Wreck's charts and Galley Stores."},
}
LORE = ("The Ghost Ship lies broken on the shore, and its crew still stand their watch. You go in alone, through the "
        "split keel, and climb the decks to the helm.")
RULES = ("Five fights in a row. Health and chakra carry from fight to fight, and a lost fight ends the run. Free to "
         "enter; each clear rolls the Wreck's chart drops.")


def item_ids():
    d = {k: v["id"] for k, v in json.load(open(DESIGN))["items"].items() if v.get("id")}
    for e in json.load(open(BUNDLE_329))["entries"]:
        if e.get("srcId") == "sg329_core_rot" and e.get("state") == "ok":
            d["core_rot"] = e["id"]
    assert "core_rot" in d
    return d


def quest(slug, name, tier, R, ids):
    T = TIERS[tier]
    sc = lambda k: {"sceneBackground": S[k], "sceneCharacters": []}  # noqa: E731
    objs = []
    for i, (did, scene, text, choice, btext, keys) in enumerate(FIGHTS):
        bid = f"b{i + 1}"
        nxt = FIGHTS[i + 1][0] if i + 1 < len(FIGHTS) else "w_done"
        objs.append({"id": did, "task": "dialog", "description": text, **sc(scene),
                     "nextObjectiveId": [{"text": choice, "nextObjectiveId": bid}]})
        objs.append({"id": bid, "task": "start_battle", "description": btext, **sc(scene),
                     "opponentAIs": [{"ids": [R(k)], "number": 1, "quantity": 1} for k in keys],
                     "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False,
                     "opponent_scaled_to_user": True, "nextObjectiveId": nxt, "failObjectiveId": "f_lost", **SHARED})
    objs.append({"id": "w_done", "task": "win_quest", **sc("helm"),
                 "description": "The wheel spins free. For a moment the whole ship seems to breathe out. Then the Core "
                                "pulls the deck back the way it was, and the watch begins again.<br><br>You climb down "
                                "through the keel with what you took.",
                 "reward_exp": T["exp"], "reward_money": T["ryo"],
                 "reward_items": [{"ids": [ids[k]], "number": c, "quantity": 1} for k, c in T["drops"]]})
    objs.append({"id": "f_lost", "task": "fail_quest", **sc("cache_site"),
                 "description": "You wake on the sand below the wreck with nothing to show for it. Above you, the watch goes on."})
    return {"entity": "quest", "slot": "create", "srcId": PFX + slug, "phase": 1, "name": name, "data": {
        "name": name, "description": f"{RULES}\n\n{LORE}\n\n{T['blurb']}",
        "successDescription": "You cleared the decks. The Core will have them back by morning.",
        "image": ICON, "questType": "battlepyramid", "questRank": "D", "hidden": True,
        "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True,
        "requiredLevel": T["level"], "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
        "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
        "startsAt": None, "endsAt": None,
        "content": {"objectives": objs, "sceneBackground": S["lower_hull"], "sceneCharacters": [BLANK],
                    "isolated": True, "reward": {}}}}


def unhide(bundle):
    got = {e["srcId"]: (e["id"], e["name"]) for e in json.load(open(bundle))["entries"]
           if e.get("entity") == "quest" and e.get("slot") == "create" and e.get("state") == "ok" and e.get("id")
           and (e.get("srcId") or "").startswith(PFX)}
    if set(got) != {PFX + "full", PFX + "faded"}:
        raise SystemExit(f"{os.path.basename(bundle)} is not push/{NUM}'s results: {sorted(got)}")
    items = [{"entity": "quest", "slot": "edit", "name": f"{n}: unhide", "targetId": i, "data": {"hidden": False}}
             for i, n in (got[PFX + "full"], got[PFX + "faded"])]
    m = {"_note": f"push/{NUM + 1}: unhide the two solo pyramids (from {os.path.basename(bundle)}; literal ids, L01). "
                  "Generated by push/skyglass_solo.gen.py --unhide; do not hand-edit.", "items": items}
    path = os.path.join(ROOT, f"push/{NUM + 1}_skyglass_solo_unhide.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{NUM + 1}_skyglass_solo_unhide.json: {len(items)} items")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--copies", action="append", default=[], help="push/344 results bundle(s)")
    ap.add_argument("--unhide", help="push/393 results bundle: write the unhide edits")
    ap.add_argument("--name", default="Ghostwatch")
    ap.add_argument("--faded-name", default="Faded Ghostwatch")
    a = ap.parse_args()
    if a.unhide:
        return unhide(a.unhide)
    if not a.copies:
        ap.error("--copies <344 bundle> is required")
    R, ids = K.Resolver(a.copies), item_ids()
    items = [quest("full", a.name, "full", R, ids), quest("faded", a.faded_name, "faded", R, ids)]
    m = {"_note": (f"push/{NUM}: the solo chart grind (RUL-2026-10-31-088), two HIDDEN Battle Pyramids (push/394 unhides), {a.name} "
                   f"(level 80) and {a.faded_name} (level 30). Free entry, isolated, 100 attempts (engine cap), 5 "
                   "scaled fights, the Wreck's chart table lowered. Icon is the Low Tide Run's (placeholder). Win rate "
                   "unmeasured. Generated by push/skyglass_solo.gen.py; do not hand-edit."),
         "dedupNames": True, "_aiKeys": R.used, "items": items}
    path = os.path.join(ROOT, f"push/{NUM}_skyglass_solo_pyramids.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{NUM}_skyglass_solo_pyramids.json: {len(items)} items")


if __name__ == "__main__":
    main()
