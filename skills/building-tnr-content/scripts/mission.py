#!/usr/bin/env python3
"""
mission.py - build a mission from its profile instead of deciding it again.

A mission has always had four halves and only one of them was deterministic. The manifest
shape was covered by factory.py and validate.py; the parameters, the rewards and the art were
decided by hand each time, which is a different kind of failure from an invalid payload: the
record pushes cleanly and is simply wrong, and nothing catches it.

So this reads three inputs and emits a complete record:

  48_DATA_mission_profiles.json   what a mission of rank R sets for every quest field, plus
                                  its reward block. The layer 45d cannot supply, because 45d
                                  describes legality and this describes correctness.
  45d / 45c (through factory.py)  the shapes, bounds and defaults.
  a design sheet                  the creative half only: the name, the prose, the node list.

Everything else is filled. The design sheet cannot set `maxAttempts`, because that is not a
creative decision and a sheet that can set it is a sheet that will.

    python3 mission.py sheet.json --profiles 48_DATA_mission_profiles.json
                                  [--spec 25x_DATA_art_spec.json]
                                  [--out manifest.json] [--selftest]

REFUSAL IS THE POINT. Any profile value still reading AWAITING_RULING for the rank being
built stops the run and names the field. A placeholder that silently becomes 0 or 1 is worse
than no pipeline at all: rewards are supplied by dauntless, and a mission that ships paying zero
looks exactly like a mission that ships paying correctly.

The art half is not guessed either. Once the objective graph exists, shotlist.py reads it and
emits the required assets with their dimensions, filenames, @img refs and rendered generator
prompts. This module calls it rather than reimplementing it.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

AWAITING = "AWAITING_RULING"
# The two objective tasks that spawn a fight. Both carry opponentAIs; nothing else does.
BATTLE_TASKS = ("start_battle", "defeat_opponents")
AUTHOR = "AUTHOR"
SEARCH = [os.getcwd(), os.path.dirname(os.path.abspath(__file__)), "/mnt/project"]

# mission.py sits beside factory.py in the content skill, but shotlist.py lives in the art
# skill, so the two halves of a mission are imported from two different installs. Both script
# directories go on the path. Without this the art half fails as an ImportError and degrades
# to "not generated", which is a silent half-build rather than an error.
SCRIPT_DIRS = [
    os.path.dirname(os.path.abspath(__file__)),
    "/mnt/skills/user/building-tnr-content/scripts",
    "/mnt/skills/user/producing-tnr-art/scripts",
]


def _path_setup() -> None:
    for d in SCRIPT_DIRS:
        if os.path.isdir(d) and d not in sys.path:
            sys.path.insert(0, d)


class MissionError(ValueError):
    """A mission that would have been wrong rather than invalid."""


def _find(name: str) -> str:
    for d in SEARCH:
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise MissionError(f"cannot find {name} (looked in {', '.join(SEARCH)})")


def load(name: str) -> dict:
    with open(_find(name)) as fh:
        return json.load(fh)


# --------------------------------------------------------------------------- profile

def resolve_profile(profiles: dict, rank: str) -> dict:
    ranks = profiles.get("ranks", {})
    if rank not in ranks:
        raise MissionError(f"rank {rank!r} has no profile (have: {', '.join(sorted(ranks))})")
    return ranks[rank]


def unresolved(node, path="") -> list:
    """Every AWAITING_RULING slot still in the profile, named by its full path.

    Reported all at once. Fixing one blocker per run is how a ten-field gap becomes ten
    round trips.
    """
    out = []
    if isinstance(node, dict):
        for k, v in node.items():
            out += unresolved(v, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            out += unresolved(v, f"{path}[{i}]")
    elif node == AWAITING:
        out.append(path)
    return out


# --------------------------------------------------------------------------- build

def resolve_enemy_level(shape: dict, roster_entry: dict) -> int:
    """Pick the level for one enemy, or refuse.

    `enemy_level_band` is a band, not a level. Taking its floor, its ceiling or its midpoint
    would each be a balance decision made silently by a tool, so a band demands an explicit
    per-enemy level and only a single-value band fills on its own.
    """
    if roster_entry.get("level") is not None:
        lvl = int(roster_entry["level"])
        band = shape.get("enemy_level_band")
        if isinstance(band, (list, tuple)) and len(band) == 2 and not band[0] <= lvl <= band[1]:
            raise MissionError(
                f"{roster_entry.get('name')}: level {lvl} is outside the rank's band {band}"
            )
        return lvl
    band = shape.get("enemy_level_band")
    if isinstance(band, int):
        return band
    if isinstance(band, (list, tuple)) and len(band) == 2:
        raise MissionError(
            f"{roster_entry.get('name')}: the rank's enemy_level_band is {band}, a range. "
            f"Give the roster entry an explicit `level`; picking a point in the band is a "
            f"balance call and not one this tool makes."
        )
    raise MissionError(f"{roster_entry.get('name')}: no level and no usable enemy_level_band")


def wire_battles(objectives: list, ai_entries: list, headcount) -> list:
    """Attach opponentAIs to every battle node.

    `number` inside opponentAIs is the HEADCOUNT of that AI in the fight, not a drop chance -
    the same idsWithNumber shape means drop-chance percent in a reward array and a body count
    here. Getting it backwards produces a battle against 100 copies of one enemy.
    """
    if not ai_entries:
        return objectives
    ids = ["@ai:" + e["srcId"] for e in ai_entries]
    out = []
    for obj in objectives:
        if obj.get("task") in BATTLE_TASKS and not obj.get("opponentAIs"):
            obj = dict(obj)
            obj["opponentAIs"] = [{"ids": ids, "number": int(headcount), "quantity": 1}]
        out.append(obj)
    return out


def check_headcount(objectives: list, profile: dict, rank: str) -> None:
    """Refuse a battle node whose total headcount exceeds the rank's ceiling.

    Route-varying encounters are the point of the design: the roof is one Fleetfoot, the front
    door is two Ironfoots. That variation lives in the SHEET, per node, because a single
    profile scalar cannot express it. So the profile stops being the value and becomes the
    CEILING, and this is what makes the ceiling real rather than a convention in a document.

    Summed per node, not per group: a node may carry several opponentAIs groups and the fight
    is all of them at once. `Blacksteel Contract: Perimeter Breach` is live proof, with groups
    of 2 and 1 on one node for a fight against three.
    """
    cap = profile["shape"].get("max_enemies_per_battle")
    if cap in (None, AWAITING):
        return
    for obj in objectives:
        if obj.get("task") not in BATTLE_TASKS:
            continue
        total = sum(int(g.get("number") or 0) for g in (obj.get("opponentAIs") or []))
        if total > int(cap):
            raise MissionError(
                f"objective {obj.get('id')!r}: {total} enemies in one fight, but rank {rank} "
                f"caps a battle at {cap}. Ratified 2026-08-27: C 2, B 3, A 4."
            )


def build_record(sheet: dict, profiles: dict) -> dict:
    rank = sheet.get("rank")
    if not rank:
        raise MissionError("sheet has no rank; the profile is selected by rank")
    profile = resolve_profile(profiles, rank)

    blocked = unresolved({"quest": profile["quest"], "shape": profile["shape"]}, rank)
    blocked += unresolved(profile["reward"], f"{rank}.reward")
    if blocked:
        raise MissionError(
            "profile incomplete for rank " + rank + "; these are rulings, not defaults:\n  "
            + "\n  ".join(blocked)
        )

    for required in ("name", "description", "successDescription", "objectives"):
        if not sheet.get(required):
            raise MissionError(f"sheet is missing {required!r} ({AUTHOR} field, no default exists)")

    fixed = profiles["_field_routing"]["fixed"]
    nulls = profiles["_field_routing"]["null_by_design"]

    record = {
        "name": sheet["name"],
        "description": sheet["description"],
        "successDescription": sheet["successDescription"],
        **fixed,
        **{k: v for k, v in profile["quest"].items()},
        **{k: None for k in nulls},
        "content": {
            "objectives": sheet["objectives"],
            "reward": dict(profile["reward"]),
            "sceneBackground": sheet.get("sceneBackground", ""),
            "sceneCharacters": sheet.get("sceneCharacters", []),
        },
    }
    if sheet.get("image"):
        record["image"] = sheet["image"]
    return record


def build_entry(record: dict, src_id: str) -> dict:
    return {"name": record["name"], "entity": "quest", "slot": "create",
            "srcId": src_id, "data": record}


def build_enemies(sheet: dict, profile: dict) -> list:
    roster = sheet.get("roster") or []
    if not roster:
        return []
    _path_setup()
    import enemy as enemy_mod
    from factory import Factory

    fac = Factory()
    pool = enemy_mod.load_pool()
    out = []
    for entry in roster:
        level = resolve_enemy_level(profile["shape"], entry)
        try:
            out.append(enemy_mod.build_ai(entry, level, fac, pool))
        except enemy_mod.EnemyError as err:
            raise MissionError(str(err))
    return out


def avatar_shots(ai_entries: list, spec: dict, slug: str, folder: str) -> list:
    """An AI_AVATAR shot per enemy, with its prompt rendered from the same scaffolds.

    shotlist.py reads a quest graph, and an enemy is not in the graph - the graph holds only
    the ai id. So the roster raises these, using the same spec block, so avatars cannot drift
    into a different register from the scene art beside them.
    """
    _path_setup()
    import shotlist

    t = spec["targets"]["AI_AVATAR"]
    aspect = t["aspect"]
    accepted = aspect.get("accepted") or ([aspect["value"]] if aspect.get("value") else [])
    shots = []
    for i, e in enumerate(ai_entries, start=1):
        filename = f"{slug}_ai{i:02d}_avatar.{t['format']}"
        shots.append({
            "target": "AI_AVATAR",
            "for": e["name"],
            "srcId": e["srcId"],
            "filename": filename,
            "img_ref": f"@img:{filename}",
            "folder": folder,
            "aspect_accepted": accepted,
            "min_width_px": t.get("min_width_px", {}).get("value"),
            "delivered_width_px": t.get("delivered_width_px"),
            "format": t["format"],
            "format_mode": t.get("format_mode"),
            "chroma_key": t.get("chroma_key"),
            "note": (f"{e['_derived']['role']} enemy, kit "
                     f"{', '.join(e['_derived']['kit_codes'])}, {e['_derived']['rank_reason']}"),
            "prompt": shotlist.render_prompt(spec, "AI_AVATAR",
                                             subject=e.get("subject") or None),
        })
    return shots


def build(sheet: dict, profiles: dict, spec: dict | None = None) -> dict:
    record = build_record(sheet, profiles)
    profile = resolve_profile(profiles, sheet["rank"])
    ai_entries = build_enemies(sheet, profile)
    if ai_entries:
        record["content"]["objectives"] = wire_battles(
            record["content"]["objectives"], ai_entries,
            profile["shape"]["enemies_per_battle"])
    check_headcount(record["content"]["objectives"], profile, sheet["rank"])
    src_id = sheet.get("srcId") or "mission_" + str(record["questRank"]).lower()
    # Build order matters: ai entries precede the quest so @ai refs resolve from the idmap.
    out = {"manifest": {"items": ai_entries + [build_entry(record, src_id)]},
           "rank": record["questRank"], "srcId": src_id,
           "enemies": [e["name"] for e in ai_entries]}

    if spec is not None:
        try:
            _path_setup()
            import shotlist  # noqa: E402
            art = shotlist.build(record, spec, sheet.get("slug", ""),
                                 sheet.get("folder", ""))
            if ai_entries:
                art["shots"] = art["shots"] + avatar_shots(
                    ai_entries, spec, art["slug"], art["folder"])
            out["art"] = art
        except ImportError:
            out["art"] = {"error": "shotlist.py not importable; art half not generated"}
    return out


# --------------------------------------------------------------------------- selftest

SHEET = {
    "rank": "D", "srcId": "mission_test", "name": "Test Mission",
    "description": "A courier run.", "successDescription": "Delivered.",
    "objectives": [
        {"id": "n1", "task": "move_to_location", "description": "Reach the drop",
         "nextObjectiveId": "n2"},
        {"id": "n2", "task": "deliver_item", "description": "Hand it over"},
    ],
}


def selftest() -> int:
    checks, failures = [], []

    def want(cond, label):
        checks.append(label)
        if not cond:
            failures.append(label)

    profiles = load("48_DATA_mission_profiles.json")

    # 1. A profile with AWAITING slots must refuse, and must name every one of them.
    try:
        build_record(SHEET, profiles)
        want(False, "an unratified profile refuses to build")
    except MissionError as err:
        want("rulings, not defaults" in str(err), "an unratified profile refuses to build")
        want(str(err).count("\n") >= 3, "refusal names every blocked field, not just the first")

    # 2. With the rank ratified, it fills.
    import copy
    ready = copy.deepcopy(profiles)
    d = ready["ranks"]["D"]
    d["quest"].update({"requiredLevel": 1, "maxLevel": 10, "maxAttempts": 3,
                       "maxCompletes": 1, "retryDelay": "daily", "attemptDelay": "none"})
    d["shape"].update({"objective_count": 2, "battle_nodes": 0,
                       "enemies_per_battle": 2, "enemy_level_band": [1, 10]})
    d["reward"]["reward_money"] = 250

    rec = build_record(SHEET, ready)
    want(rec["questType"] == "mission", "questType fixed by the profile, not the sheet")
    want(rec["hidden"] is True, "hidden ships true and is not a sheet field")
    want(rec["consecutiveObjectives"] is True, "consecutiveObjectives fixed true")
    want(rec["maxAttempts"] == 3, "profile value filled without the sheet mentioning it")
    want(rec["content"]["reward"]["reward_money"] == 250, "reward block comes from the profile")
    want(len(rec["content"]["reward"]) == 27, "all 27 reward fields present, none dropped")
    want(rec["medicalRank"] is None, "null_by_design fields filled as explicit nulls")
    want(rec["questRank"] == "D", "rank carried onto the record")

    # 3. The sheet cannot reach a profile field.
    sneaky = dict(SHEET, maxAttempts=99)
    want(build_record(sneaky, ready)["maxAttempts"] == 3,
         "a sheet field cannot override a profile field")

    # 4. Creative fields have no defaults.
    try:
        build_record({k: v for k, v in SHEET.items() if k != "description"}, ready)
        want(False, "a missing AUTHOR field refuses rather than defaulting")
    except MissionError:
        want(True, "a missing AUTHOR field refuses rather than defaulting")

    # 5. Reward mutation isolation: two builds must not share a reward dict.
    a = build_record(SHEET, ready)
    a["content"]["reward"]["reward_money"] = 1
    b = build_record(SHEET, ready)
    want(b["content"]["reward"]["reward_money"] == 250,
         "each build gets its own reward copy, not a shared reference")

    # --- enemy half -------------------------------------------------------------
    battle_sheet = dict(SHEET)
    battle_sheet["objectives"] = [
        {"id": "n1", "task": "dialog", "description": "Approach", "nextObjectiveId": "n2"},
        {"id": "n2", "task": "defeat_opponents", "description": "Fight", "failObjectiveId": "n1"},
    ]
    battle_sheet["roster"] = [
        {"name": "Selftest Thug", "role": "standard", "kit": ["S01", "S02"], "level": 8},
    ]
    spec = load("25x_DATA_art_spec.json")
    built = build(battle_sheet, ready, spec)
    items = built["manifest"]["items"]
    want(items[0]["entity"] == "ai" and items[-1]["entity"] == "quest",
         "ai entries precede the quest so @ai refs resolve")
    quest_nodes = items[-1]["data"]["content"]["objectives"]
    battle = next(o for o in quest_nodes if o["task"] == "defeat_opponents")
    want(battle["opponentAIs"][0]["ids"] == ["@ai:ai_selftest_thug"],
         "battle node wired to the roster by @ai ref")
    want(battle["opponentAIs"][0]["number"] == 2,
         "opponentAIs number is the headcount from the profile, not a drop chance")
    want("opponentAIs" not in quest_nodes[0], "non-battle nodes left alone")

    avatars = [s for s in built["art"]["shots"] if s["target"] == "AI_AVATAR"]
    want(len(avatars) == 1, "one avatar shot per roster enemy")
    want(avatars[0]["img_ref"] == "@img:" + avatars[0]["filename"], "avatar @img ref matches")
    want(avatars[0]["prompt"] and "[STYLE]" not in avatars[0]["prompt"]["positive"],
         "avatar prompt rendered from the same scaffolds as the scene art")
    want(avatars[0]["prompt"].get("costume_grammar"), "avatar prompt carries costume grammar")

    # A banded level with no explicit per-enemy level must refuse, not pick a point.
    banded = copy.deepcopy(ready)
    banded["ranks"]["D"]["shape"]["enemy_level_band"] = [5, 15]
    vague = dict(battle_sheet)
    vague["roster"] = [{"name": "Vague", "role": "standard", "kit": ["S01"]}]
    try:
        build(vague, banded, None)
        want(False, "a band with no explicit level refuses rather than picking a point")
    except MissionError as err:
        want("balance call" in str(err),
             "a band with no explicit level refuses rather than picking a point")

    for label in failures:
        print(f"  FAIL  {label}")
    print(f"\n{len(checks) - len(failures)} passed, {len(failures)} failed")
    return len(failures)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet", nargs="?")
    ap.add_argument("--profiles", default="48_DATA_mission_profiles.json")
    ap.add_argument("--spec", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.sheet:
        ap.error("a design sheet is required")

    with open(args.sheet) as fh:
        sheet = json.load(fh)
    profiles = load(args.profiles)
    spec = load(args.spec) if args.spec else None

    try:
        result = build(sheet, profiles, spec)
    except MissionError as err:
        print("REFUSED: " + str(err))
        return 1

    text = json.dumps(result["manifest"], indent=1)
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(text)
        print(f"wrote {args.out}")
    else:
        print(text)

    art = result.get("art")
    if art and "shots" in art:
        print(f"\nart: {len(art['shots'])} shots, {len(art.get('satisfied', []))} already wired")
        for s in art["shots"]:
            print(f"  {s['filename']}  {s['target']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
