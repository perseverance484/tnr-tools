#!/usr/bin/env python3
"""Generate push/362 (the endgame Skyglass Wreck: floors and clear drops) and push/366 (the easy, level-45 Wreck).

    python3 push/skyglass_wreck.gen.py --currency M,E,T,P              # 362_skyglass_wreck_endgame.json (1 dungeon edit)
    python3 push/skyglass_wreck.gen.py --easy --copies <344 bundle>    # 366_skyglass_wreck_easy.json (1 dungeon create)

362 edits the live, hidden Skyglass Wreck (RHqzYdY4EAQA9HwsBKWDS, push/263; entrance structure gAsRCVBGRplS31wOYckh7,
sector 210 (15, 6), size 5). coop.dungeon.save replaces whole top-level keys and Forge merges shallowly, so asserting
`rewards` replaces the clear currency the director set in game (RUL-2026-10-24-019). --currency is therefore
REQUIRED: the live money, experience, tokens and prestige, read off the dungeon editor (pass 0,0,0,0 only to reset them
and set them again in game). Asserted: description, background, tiers, rewards. Name, entrance, hidden: kept live.

Floors: build_spec.json `endgame.floors` / `lvl50.floors` (state/skyglass_build, provenance in its README) with each
harness id mapped through an AI key (push/skyglass_wave2.py): endgame -> base:<slug> (the live crew records, upgraded
in place by push/361, RUL-2026-10-31-067 item 1); easy -> faded:<slug> (the Faded tier created by the rebuilt push/344,
item 6; ids from its results bundle). Floor kinds are set by position (floors 1-4 `floor`, floor 5 `boss`), as the
engine requires for a single tier (validators/dungeon.ts superRefine; forge/src/dungeon/validate.mjs): the harness's
floor-4 "mini-boss" label is only valid as the last floor of a non-final tier. Every wave's delayRounds is the spec's.

Clear drops (each member rolls each line; SKYGLASS_LOOT_TABLES.md section 2 / 5 / 5b / 5d):
  endgame: Unmarked Cargo 10, Chart of the Buried Cache 20, Drowned Foundry 12, Quarantined Archive 6, Captain's Watch 6,
    Lastlight Lantern 3, Sealed Treasury 3 (as push/263); Tide Chart 15, Watch Roster 10 (RUL-2026-10-28-009); Core Rot 15
    (endgame only, RUL-2026-10-28-020 item 4); each of the six Haul pages 2.4 (RUL-2026-10-30-060 item 5); the Captain's
    and the Core Horror's variant tokens 5, onlyOnce (item 9); The Little Horror's Jar 5, onlyOnce (RUL-2026-10-29-054
    item 4; push/346 id).
  easy: Tide Chart 25, Watch Roster 15, Chart of the Buried Cache 5, Galley Stores 10 (RUL-2026-10-28-010/-013/-019).
Background `dessert` for both (RUL-2026-10-28-027 item 2; push/263 shipped `default`). Description: SKYGLASS_TEXT.md
section 8's corrected Wreck text; the easy version adds its level line (text doc: "The easy version adds: ...").

Easy Wreck placeholders (reversible, director to set; listed in `_placeholders`): its name, its entrance tile (sector
210, one tile east of the endgame entrance), clear currency 0 (set in game, as push/263). Pets fight in the Wreck
(RUL-2026-10-31-072 item 7): dungeon battles are QUEST battles; nothing to build, but the re-simulation should include
the pet.

Do not hand-edit the output.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skyglass_wave2 as W  # noqa: E402
import importlib.util  # noqa: E402

_s = importlib.util.spec_from_file_location("skyglass_text", os.path.join(W.ROOT, "push/skyglass_text.py"))
T = importlib.util.module_from_spec(_s); _s.loader.exec_module(T)

WRECK_ID = "RHqzYdY4EAQA9HwsBKWDS"  # push/263 (tnr_results_1792991569988.json)
STRUCTURE = "gAsRCVBGRplS31wOYckh7"
BUNDLE_329 = os.path.join(W.ROOT, "harvests/inbox/tnr_results_1793424666625.json")
BUNDLE_346 = os.path.join(W.ROOT, "harvests/inbox/tnr_results_1793463543589.json")
DESIGN = os.path.join(W.ROOT, "state/skyglass_design/design_data.json")
BACKGROUND = "dessert"
EASY_NAME = "Faded Skyglass Wreck"  # placeholder name (director)
EASY_TILE = (210, 16, 6)  # placeholder entrance (director)

# (design_data items key | literal, chance, onlyOnce)
ENDGAME = [("unmarked_cargo", 10), ("chart_buried_cache", 20), ("chart_drowned_foundry", 12),
           ("chart_quarantined_archive", 6), ("chart_captains_watch", 6), ("lastlight_lantern", 3),
           ("sealed_treasury", 3), ("chart_tide", 15), ("chart_watch_roster", 10), ("core_rot", 15),
           ("haul_trophy_hold", 2.4), ("haul_bone_store", 2.4), ("haul_snare_room", 2.4),
           ("haul_overgrown_stores", 2.4), ("haul_ore_vault", 2.4), ("haul_bloom_cellar", 2.4),
           ("vt_captain", 5, True), ("vt_core_horror", 5, True), ("little_horror_jar", 5, True)]
EASY = [("chart_tide", 25), ("chart_watch_roster", 15), ("chart_buried_cache", 5), ("galley_stores", 10)]


def item_ids():
    import json
    d = {k: v["id"] for k, v in json.load(open(DESIGN))["items"].items() if v.get("id")}
    im329, im346 = W.idmap(BUNDLE_329), W.idmap(BUNDLE_346)
    d["unmarked_cargo"] = "KzITKJ5BUQRz5QuYWw-0B"  # push/274 (tnr_results_1792984910501.json), as push/263
    d["core_rot"] = im329["sg329_core_rot"]
    d["little_horror_jar"] = im346["sg346_little_horror_jar"]
    assert d["little_horror_jar"] == "oSFTrX15PqtFtjwRXk041"
    assert d["vt_captain"] == im329["sg329_vt_captain"] and d["vt_core_horror"] == im329["sg329_vt_core_horror"]
    return d


def drops(table):
    ids = item_ids()
    out = []
    for row in table:
        key, chance = row[0], row[1]
        d = {"type": "item", "id": ids[key], "chance": chance, "quantity": 1}
        if len(row) > 2 and row[2]:
            d["onlyOnce"] = True
        out.append(d)
    return out


def description(easy):
    row = next(r for r in T.table("## 8. Corrections") if "WRECK_DESCRIPTION" in r[0])
    cell = row[2]
    main = cell[1:cell.index("`", 1)]
    if not easy:
        return main
    tail = cell[cell.index("The easy version adds:"):]
    line = tail[tail.index("`") + 1:tail.rindex("`")]
    return main + "<br><br>" + line


def floors(version, keymap):
    src = W.spec("build_spec.json")[version]["floors"]
    assert len(src) == 5, len(src)
    out = []
    for i, f in enumerate(src):
        waves = []
        for w in f["waves"]:
            ais = []
            for h in w["aiIds"]:
                key = ("faded:" if version == "lvl50" else "base:") + W.slug(h)
                if key not in keymap:
                    raise SystemExit(f"{version} floor {i + 1}: {h} -> {key} has no id")
                ais.append(keymap[key])
            waves.append({"aiIds": ais, "delayRounds": w.get("delayRounds", 0)})
        out.append({"kind": "boss" if i == 4 else "floor", "waves": waves})
    return out


def endgame(currency):
    m, e, t, p = currency
    data = {"description": description(False), "background": BACKGROUND,
            "tiers": [floors("endgame", W.base_key_map())],
            "rewards": {"money": m, "experience": e, "tokens": t, "prestige": p, "drops": drops(ENDGAME)}}
    return {"entity": "dungeon", "slot": "edit", "targetId": WRECK_ID, "name": "Skyglass Wreck", "data": data}


def easy(bundle, notes):
    sector, lon, lat = EASY_TILE
    data = {"name": EASY_NAME, "description": description(True), "structureAssetId": STRUCTURE, "structureScale": 5,
            "sector": sector, "longitude": lon, "latitude": lat, "expiresAt": None, "hidden": True,
            "background": BACKGROUND, "tiers": [floors("lvl50", W.faded_key_map(bundle, notes))],
            "rewards": {"money": 0, "experience": 0, "tokens": 0, "prestige": 0, "drops": drops(EASY)}}
    return {"entity": "dungeon", "slot": "create", "srcId": f"sg{W.NUM['easy']}_easy_wreck", "name": EASY_NAME,
            "data": data}


def main():
    args = sys.argv[1:]
    if "--easy" in args:
        if "--copies" not in args:
            raise SystemExit("--easy needs --copies <rebuilt push/344 results bundle>")
        bundle = args[args.index("--copies") + 1]
        notes = []
        n = W.NUM["easy"]
        m = {"_note": (f"push/{n}: the easy (level-45) Skyglass Wreck, created HIDDEN (RUL-2026-10-31-067 item 6): "
                       f"floors from {W.build_dir_note()}/build_spec.json lvl50 on the Faded tier (ids from "
                       f"{os.path.basename(bundle)}, push/344), clear drops Tide Chart 25 / Watch Roster 15 / Buried "
                       "Cache chart 5 / Galley Stores 10, background dessert. Generated by push/skyglass_wreck.gen.py "
                       "--easy; do not hand-edit."),
             "dedupNames": True,
             "_placeholders": [f"name {EASY_NAME!r} (director)", f"entrance sector {EASY_TILE[0]} ({EASY_TILE[1]}, "
                               f"{EASY_TILE[2]}) (director)", "clear currency 0 (set in game, as push/263)"],
             "_key_notes": notes, "items": [easy(bundle, notes)]}
        return W.write(os.path.join(W.OUT, f"{n}_skyglass_wreck_easy.json"), m)
    if "--currency" not in args:
        raise SystemExit("--currency M,E,T,P is required: the live clear currency (an asserted `rewards` replaces it)")
    cur = [float(x) if "." in x else int(x) for x in args[args.index("--currency") + 1].split(",")]
    if len(cur) != 4 or any(v < 0 for v in cur):
        raise SystemExit("--currency takes four non-negative numbers: money,experience,tokens,prestige")
    n = W.NUM["wreck"]
    m = {"_note": (f"push/{n}: the endgame Skyglass Wreck ({WRECK_ID}, hidden) gets its final floors and clear drops: "
                   f"floors from {W.build_dir_note()}/build_spec.json endgame on the live crew records (push/"
                   f"{W.NUM['crew']} runs FIRST), {len(ENDGAME)} drop lines (Haul pages 2.4% each; the Captain's and "
                   "Core Horror's variant tokens and the Little Horror's Jar 5%, once per player), background dessert, "
                   f"description per SKYGLASS_TEXT.md section 8. Clear currency re-sent as given: {cur}. Generated by "
                   "push/skyglass_wreck.gen.py; do not hand-edit."),
         "items": [endgame(cur)]}
    W.write(os.path.join(W.OUT, f"{n}_skyglass_wreck_endgame.json"), m)


if __name__ == "__main__":
    main()
