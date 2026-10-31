#!/usr/bin/env python3
"""Crown's Hoard, Wreck Sighted and Crownhold's Hoard pick (push/348, 349). All HIDDEN, engine-default placeholder art
(RUL-2026-10-30-059).

    python3 push/skyglass_hoard.gen.py                           # push/348: Crown's Hoard + Wreck Sighted (creates)
    python3 push/skyglass_hoard.gen.py --crownhold <348 bundle>  # push/349: Crownhold re-sent with the Hoard in its pick

348  Crown's Hoard (loot tables 1, 3, 4a; RUL-2026-10-28-013, RUL-2026-10-29-039 item 2 as amended by -049): one
     consumable with three effects, the way the Sealed Treasury carries two: a fixed 150,000 ryo + Skyglass Token x1, a
     Skyglass Coffer roll (the Coffer's own table, 1 roll) and a Sealed Treasury roll (its table, 3/4/6 rolls). The
     description is rendered from those tables and must equal SKYGLASS_TEXT.md `item:Crown's Hoard.description`.
     Wreck Sighted (RUL-2026-10-28-028 item 2; text doc section 1; scene `cache_site`, RUL-2026-10-30-061 item 7): a
     one-time free intro quest, two dialogs and a win that grants the Tide Chart x1. Both records name only live ids
     (the Skyglass Token and the Tide Chart are push/329 creates, read from 329's results bundle), so 348 depends on no
     unrun manifest.
349  Crownhold's pick gains Crown's Hoard (loot tables 4a). A quest edit is a whole-record send (no fetch-merge), and the
     Hoard is a 348 create, so 349 is built from 348's results bundle (literal ids, L01), never committed before 348 runs.
     The rest of the record is the generator's Crownhold exactly as push/329 created it (skyglass_update.gen.py
     crownhold(), with 329's @item refs resolved from 329's bundle), so the only change is the Hoard card.
Walked Every Deck (loot tables 5c) is NOT built here: see push/README.md (348/349 entry) for why it is stopped and
the options.

Engine (theninjarpg@3314d122): app/src/server/api/routers/item.ts ~2104-2145 opens every weightedCache effect of one
item (one roll set each) and pays the standard effects beside them; server/api/routers/quests.ts ~866-880 (a quest
saved with hidden:false needs scene characters; a hidden one saves without).

Do not hand-edit the outputs.
"""
import copy
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


U = _load("skyglass_update.gen.py")
IT, G, T = U.IT, U.G, U.T
PLACEHOLDER = IT.PLACEHOLDER

NUM, CROWNHOLD_NUM = 348, 349
PFX = "sg348_"  # srcIds are unique across every Forge job
HOARD_SRC = PFX + "crowns_hoard"
WRECK_SIGHTED_SRC = PFX + "wreck_sighted"
BUNDLE_329 = "harvests/inbox/tnr_results_1793424666625.json"  # push/329's results (design_data.json cites it)
DESIGN = os.path.join(ROOT, "state/skyglass_design/design_data.json")


def idmap_329():
    return json.load(open(os.path.join(ROOT, BUNDLE_329))).get("idmap") or {}


def resolve(o, idmap):
    missing = set()
    out = U.resolve_329(o, idmap, missing)
    if missing:
        raise SystemExit("push/329 creates missing from its results idmap: " + ", ".join(sorted(missing)))
    return out


def design():
    return json.load(open(DESIGN))


# ---------------------------------------------------------------------------------------------------------------
# Crown's Hoard
# ---------------------------------------------------------------------------------------------------------------
HOARD_ALWAYS = "150,000 ryo · Skyglass Token"


def hoard_description():
    story = IT.story_of("item:Crown's Hoard.description")
    coffer = IT.render(story, IT.COFFER, always=HOARD_ALWAYS, head="<b>Coffer, 1 roll:</b>")
    treasury = "<br>".join(["<b>Treasury, 3–6 rolls:</b>"] + [IT.tier_line(n, p, e) for n, p, e in IT.TREASURY if p])
    return IT.checked("item:Crown's Hoard.description", coffer + "<br>" + treasury)


def hoard():
    effects = [
        IT.fixed("Crown's Hoard: 150,000 ryo and a Skyglass Token, every opening", items=[("Skyglass Token", 1)],
                 money=150000),
        IT.cache("Skyglass Coffer", "Crown's Hoard: one Skyglass Coffer roll", IT.COFFER),
        IT.cache("Sealed Treasury", "Crown's Hoard: 3-6 Sealed Treasury rolls", IT.TREASURY, IT.TREASURY_ROLLS),
    ]
    # Rarity Legendary (RUL-2026-10-29-058 item 1). Untradeable: the Coffer's own create (push/260) carries
    # canBeTraded false and no ruling sets the Hoard's; reversible placeholder, reported.
    e = IT.create(HOARD_SRC, "Crown's Hoard", hoard_description(), "LEGENDARY", "CONSUMABLE", False, effects)
    return resolve(e, idmap_329())


# ---------------------------------------------------------------------------------------------------------------
# Wreck Sighted
# ---------------------------------------------------------------------------------------------------------------
def wreck_sighted():
    tide = idmap_329()["sg329_tide_chart"]
    assert tide == design()["items"]["chart_tide"]["id"]
    scene = G.SCENE["cache_site"]  # RUL-2026-10-30-061 item 7

    def dialog(i, nxt):
        target = f"obj:Wreck Sighted/{i}.description"
        ch = T.choices(target)
        assert len(ch) == 1, target
        return {"id": i, "task": "dialog", "description": T.block(target), "sceneBackground": scene,
                "sceneCharacters": [], "nextObjectiveId": [{"text": ch[0], "nextObjectiveId": nxt}]}

    win = {"id": "w_done", "task": "win_quest", "description": T.block("obj:Wreck Sighted/w_done.description"),
           "sceneBackground": scene, "sceneCharacters": [],
           "reward_items": [{"ids": [tide], "number": 100, "quantity": 1}]}
    # questType event (listed in the alliance building; maxCompletes enforced, so 1/1 makes it one-time), rank D (every
    # rank can start it), levels 1-100: none of these is ruled; reversible placeholders, reported. No scene character:
    # the salvager portrait is not drawn yet (RUL-2026-10-29-057 item 7) and a hidden quest saves without one; the quest
    # cannot be published until one is set (quests.ts ~866-880).
    return {"entity": "quest", "slot": "create", "srcId": WRECK_SIGHTED_SRC, "phase": 1, "name": "Wreck Sighted",
            "data": {
                "name": T.block("quest:Wreck Sighted.name"), "description": T.block("quest:Wreck Sighted.description"),
                "image": PLACEHOLDER, "questType": "event", "questRank": "D",
                "successDescription": T.block("quest:Wreck Sighted.successDescription"),
                "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
                "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 1, "maxCompletes": 1, "prerequisiteQuestId": None,
                "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
                "content": {"objectives": [dialog("d_word", "d_chart"), dialog("d_chart", "w_done"), win],
                            "sceneBackground": scene, "sceneCharacters": [], "entryItems": [], "reward": {}}}}


# ---------------------------------------------------------------------------------------------------------------
# Crownhold's pick (349)
# ---------------------------------------------------------------------------------------------------------------
def crownhold_edit(bundle):
    idmap = (json.load(open(bundle)).get("idmap") or {})
    hoard_id = idmap.get(HOARD_SRC)
    if not hoard_id:
        raise SystemExit(f"{HOARD_SRC} missing from {os.path.basename(bundle)}'s idmap: is it push/{NUM}'s results?")
    target = design()["picks"]["runs"][-1]
    assert target["run"] == "Crownhold" and target["quest"]["id"] == idmap_329()["sg329_crownhold"]
    q = U.crownhold()
    data = resolve(copy.deepcopy(q["data"]), idmap_329())
    r = data["content"]["reward"]
    if all(hoard_id not in x["ids"] for x in r["reward_items"]):  # U.crownhold() adds it once the design id is set
        r["reward_items"] = [{"ids": [hoard_id], "number": 100, "quantity": 1}] + r["reward_items"]  # section 4a order
    assert r["reward_items"][0]["ids"] == [hoard_id]
    assert data["hidden"] is True  # live truth: created hidden by 329; 349 runs before any publish
    return {"entity": "quest", "slot": "edit", "targetId": target["quest"]["id"],
            "name": "Crownhold: Crown's Hoard joins the pick", "data": data}


# ---------------------------------------------------------------------------------------------------------------
def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/skyglass_hoard.gen.py; do not hand-edit.", "dedupNames": True}
    if extra:
        m.update(extra)
    m["items"] = items
    path = os.path.join(ROOT, f"push/{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items)} items")


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--crownhold":
        bundle = sys.argv[2]
        return write(CROWNHOLD_NUM, "crownhold_hoard_pick", (
            f"push/{CROWNHOLD_NUM} (after push/{NUM}, from its results bundle {os.path.basename(bundle)}; literal ids, "
            "L01). Crownhold (hidden, created by push/329) re-sent whole with Crown's Hoard added to its pick (loot "
            "tables 4a: Crown's Hoard / Skyglass Coffer x3 / Crownbreaker badge / Lastlight / Crown Fragment). Every "
            "other field is push/329's Crownhold. Stays hidden."), [crownhold_edit(bundle)])
    if len(sys.argv) > 1:
        raise SystemExit(__doc__)
    body = [hoard(), wreck_sighted()]
    write(NUM, "skyglass_hoard_and_intro", (
        f"push/{NUM}, HIDDEN, placeholder art (RUL-2026-10-30-059; list in _placeholders). Two creates, no dependency on "
        "an unrun manifest: Crown's Hoard (Legendary consumable: 150,000 ryo + Skyglass Token every opening, one "
        "Skyglass Coffer roll, 3-6 Sealed Treasury rolls; RUL-2026-10-28-013, RUL-2026-10-29-039, -049) and Wreck Sighted (the "
        "one-time intro quest that grants the first Tide Chart; text doc section 1; scene cache_site). Wreck Sighted has "
        "no scene character yet (salvager portrait pending, RUL-2026-10-29-057 item 7), so it cannot be published until "
        f"one is set. After it runs: record Crown's Hoard's id, then build push/{CROWNHOLD_NUM} with --crownhold."),
        body, {"_placeholders": IT.placeholders(body)})


if __name__ == "__main__":
    main()
