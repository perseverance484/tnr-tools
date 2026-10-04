#!/usr/bin/env python3
"""
Build push/61_jellyfish_coast_quest.json.

Candidate hidden content package for "The Crown in the Surf":
- one approved SCENE_BACKGROUND asset
- Jellyfish AI using shared-pool jutsu only
- Royal Jellyfish boss AI using shared-pool jutsu only
- one short event quest with two dialog-gated battles
- no authored reward values

The three @img files are already processed locally; this candidate carries the
mandatory imgSizes ledger for Forge's picker fallback. A repo-backed imagePack
is intentionally deferred until the approved bytes are committed to an
immutable repository ref.

Run from repository root:
    python3 push/61_jellyfish_coast_quest.gen.py
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "building-tnr-content")
sys.path.insert(0, os.path.join(SKILL, "scripts"))

from factory import Factory  # noqa: E402
from enemy import build_ai, load_pool  # noqa: E402

OUT = os.path.join(ROOT, "push", "61_jellyfish_coast_quest.json")
CTORS = os.path.join(ROOT, "45c_DATA_constructors.json")
ENTS = os.path.join(SKILL, "data", "45d_DATA_entity_schemas.json")
CHECKS = os.path.join(ROOT, "45g_DATA_checks.json")
POOL = os.path.join(ROOT, "32b_DATA_pool.json")

QUEST_NAME = "The Crown in the Surf"
QUEST_SRC = "jelly_quest_crown_in_surf"
BG_SRC = "jelly_scene_bg_tidewatch"
BASIC_SRC = "jelly_ai_basic"
ROYAL_SRC = "jelly_ai_royal"

BASIC_AVATAR = "avatar_basic_jellyfish_v1.webp"
ROYAL_AVATAR = "avatar_royal_jellyfish_v1.webp"
BEACH_BG = "scene_bg_tidewatch_beach_v1.webp"

IMG_SIZES = {
    BASIC_AVATAR: 155014,
    ROYAL_AVATAR: 299490,
    BEACH_BG: 202578,
}

BASIC_KIT = ["EW03", "S29", "EW01", "S08", "EW02"]
ROYAL_KIT = ["B20", "B03", "B29", "B16", "EW02", "B02"]

SCENE = "@scene:" + BG_SRC


def dialog(f: Factory, oid: str, description: str, choice: str, nxt: str):
    return f.objective(
        "dialog",
        id=oid,
        description=description,
        nextObjectiveId=[{"text": choice, "nextObjectiveId": nxt}],
        sceneBackground=SCENE,
        sceneCharacters=[],
        attackers=[],
        attackers_scaled_to_user=False,
    )


def build_enemy(
    f: Factory,
    pool: dict,
    *,
    name: str,
    src_id: str,
    role: str,
    rank: str,
    kit: list[str],
    avatar: str,
):
    entry = build_ai(
        {
            "name": name,
            "srcId": src_id,
            "role": role,
            "kit": kit,
            "element": "Water",
            "rank": rank,
            "stat_archetype": "uniform",
            "avatar": "@img:" + avatar,
        },
        100,
        f,
        pool,
    )
    derived = entry.pop("_derived")
    entry["data"]["preferredStat"] = "Ninjutsu"
    entry["data"]["preferredGeneral1"] = "Intelligence"
    entry["data"]["preferredGeneral2"] = "Willpower"

    # The role multipliers are ratified enemy.py defaults, not bespoke beach
    # tuning. The quest scales both opponents to the player at battle time.
    if role == "standard":
        assert entry["data"]["poolsMultiplier"] == 1
        assert entry["data"]["statsMultiplier"] == 1
    elif role == "boss":
        assert entry["data"]["poolsMultiplier"] == 2
        assert entry["data"]["statsMultiplier"] == 3

    assert entry["data"]["regeneration"] == 60
    assert entry["data"]["hidden"] is True
    assert entry["data"]["jutsus"] == [pool[c]["id"] for c in kit]
    assert derived["kit_codes"] == kit
    return entry


def objectives(f: Factory):
    o0 = dialog(
        f,
        "jelly_o0",
        (
            "<i>Morning light flashes across Tidewatch Beach, but the usual fishing "
            "skiffs are pulled high above the tide line. A warning rope cuts across "
            "the path to the water.</i> <br> <br> Overnight, luminous jellyfish drifted "
            "into the shallows and drove everyone off the beach. The assignment on the "
            "weathered patrol board is simple: clear the water and determine why the "
            "swarm came ashore."
        ),
        "Step onto the beach.",
        "jelly_o1",
    )
    o1 = dialog(
        f,
        "jelly_o1",
        (
            "<i>The next wave leaves a cold blue glow behind it. A jellyfish rises from "
            "the foam, its bell pulsing above the surface while thin tendrils drag across "
            "the wet sand.</i> <br> <br> More lights drift farther out, but this one holds "
            "the shallows as if guarding the way seaward."
        ),
        "Clear the shallows.",
        "jelly_b1",
    )
    b1 = f.objective(
        "start_battle",
        id="jelly_b1",
        opponentAIs=[{"ids": ["@ai:" + BASIC_SRC], "number": 1, "quantity": 1}],
        opponent_scaled_to_user=True,
        keepOriginalPools=False,
        completionOutcome="Win",
        nextObjectiveId="jelly_o2",
        failObjectiveId="jelly_f1",
        sceneBackground=SCENE,
        sceneCharacters=[],
    )
    f1 = dialog(
        f,
        "jelly_f1",
        (
            "<i>A numbing sting catches you before you can break away. You retreat above "
            "the tide line as the jellyfish sinks back into the surf.</i> <br> <br> It does "
            "not pursue. The creature simply waits in the shallows, pulsing with cold blue "
            "light."
        ),
        "Regain your footing.",
        "jelly_r1",
    )
    r1 = f.objective(
        "reset_quest",
        id="jelly_r1",
        resetObjectiveId="jelly_o1",
        sceneBackground=SCENE,
        sceneCharacters=[],
    )
    o2 = dialog(
        f,
        "jelly_o2",
        (
            "<i>The jellyfish collapses into the receding foam. At once, the scattered "
            "lights beyond the breakers begin moving together.</i> <br> <br> The water "
            "darkens beneath a broad shadow. A much larger bell rises offshore, edged in "
            "bright points like a crown. The smaller jellyfish were not simply washing "
            "ashore. They were following it."
        ),
        "Follow the retreating swarm.",
        "jelly_o3",
    )
    o3 = dialog(
        f,
        "jelly_o3",
        (
            "<i>The Royal Jellyfish lifts with the swell until its crown clears the water. "
            "Long tendrils comb the surf, and the tide itself seems to pull toward the "
            "creature before spilling back across the sand.</i> <br> <br> The beach will "
            "not clear while the swarm still has something to follow."
        ),
        "Challenge the Royal Jellyfish.",
        "jelly_b2",
    )
    b2 = f.objective(
        "start_battle",
        id="jelly_b2",
        opponentAIs=[{"ids": ["@ai:" + ROYAL_SRC], "number": 1, "quantity": 1}],
        opponent_scaled_to_user=True,
        keepOriginalPools=False,
        completionOutcome="Win",
        nextObjectiveId="jelly_o4",
        failObjectiveId="jelly_f2",
        sceneBackground=SCENE,
        sceneCharacters=[],
    )
    f2 = dialog(
        f,
        "jelly_f2",
        (
            "<i>A crushing surge throws you back toward dry sand. The Royal Jellyfish "
            "settles beyond the breakers while the smaller lights gather around it again.</i> "
            "<br> <br> The swarm has not scattered. Another approach is still possible."
        ),
        "Regroup at the tide line.",
        "jelly_r2",
    )
    r2 = f.objective(
        "reset_quest",
        id="jelly_r2",
        resetObjectiveId="jelly_o3",
        sceneBackground=SCENE,
        sceneCharacters=[],
    )
    o4 = dialog(
        f,
        "jelly_o4",
        (
            "<i>The Royal Jellyfish sinks beneath the final breaker. Its crown is the last "
            "glimmer to vanish.</i> <br> <br> Without it, the remaining jellyfish lose their "
            "pattern. One by one, their blue lights turn away from shore and drift back into "
            "deeper water. The warning rope can finally come down."
        ),
        "Reopen the shore.",
        "jelly_win",
    )
    win = f.objective(
        "InstantWinLoseObjective",
        id="jelly_win",
        task="win_quest",
        successDescription=(
            "The Royal Jellyfish retreats beyond the breakers, and the scattered swarm "
            "drifts back out to sea. Tidewatch Beach is safe again."
        ),
        sceneBackground=SCENE,
        sceneCharacters=[],
    )
    return [o0, o1, b1, f1, r1, o2, o3, b2, f2, r2, o4, win]


def verify(manifest: dict, pool: dict):
    items = manifest["items"]
    assert [(x["entity"], x["slot"]) for x in items] == [
        ("asset", "create"),
        ("ai", "create"),
        ("ai", "create"),
        ("quest", "create"),
    ]
    assert manifest["dedupNames"] is True
    assert manifest["imgSizes"] == IMG_SIZES
    assert not [x for x in items if x["entity"] == "jutsu"]

    asset, basic, royal, quest = items
    assert asset["data"]["type"] == "SCENE_BACKGROUND"
    assert asset["data"]["hidden"] is True
    assert basic["data"]["avatar"] == "@img:" + BASIC_AVATAR
    assert royal["data"]["avatar"] == "@img:" + ROYAL_AVATAR
    assert basic["data"]["jutsus"] == [pool[c]["id"] for c in BASIC_KIT]
    assert royal["data"]["jutsus"] == [pool[c]["id"] for c in ROYAL_KIT]
    assert basic["data"]["statsMultiplier"] == 1
    assert royal["data"]["statsMultiplier"] == 3

    q = quest["data"]
    assert q["questType"] == "event"
    assert q["hidden"] is True
    assert q["content"]["reward"] == {}
    assert q["content"]["sceneCharacters"] == []
    assert q["content"]["sceneBackground"] == SCENE

    objs = q["content"]["objectives"]
    ids = [o["id"] for o in objs]
    assert len(ids) == len(set(ids))

    edges = []
    by_id = {o["id"]: o for o in objs}
    for o in objs:
        nxt = o.get("nextObjectiveId")
        if isinstance(nxt, list):
            edges.extend(c["nextObjectiveId"] for c in nxt)
        elif isinstance(nxt, str):
            edges.append(nxt)
        if o.get("failObjectiveId"):
            edges.append(o["failObjectiveId"])
    assert not set(edges) - set(ids)
    assert [oid for oid in ids if oid not in edges] == ["jelly_o0"]

    # Reset destinations already have normal incoming edges. resetObjectiveId
    # does not count as an incoming edge in engine flow validation.
    assert by_id["jelly_r1"]["resetObjectiveId"] == "jelly_o1"
    assert by_id["jelly_r2"]["resetObjectiveId"] == "jelly_o3"
    assert "jelly_o1" in edges and "jelly_o3" in edges

    for bid in ("jelly_b1", "jelly_b2"):
        b = by_id[bid]
        assert b["task"] == "start_battle"
        assert b["opponent_scaled_to_user"] is True
        assert b["keepOriginalPools"] is False
        assert len(b["opponentAIs"]) == 1
        assert b["opponentAIs"][0]["number"] == 1
        assert by_id[b["failObjectiveId"]]["task"] == "dialog"

    # Every start_battle is directly unlocked by a dialog choice.
    for bid in ("jelly_b1", "jelly_b2"):
        gates = [
            o for o in objs
            if o["task"] == "dialog"
            and any(c["nextObjectiveId"] == bid for c in o["nextObjectiveId"])
        ]
        assert len(gates) == 1

    # The user explicitly requested no rewards and no scene characters.
    blob = json.dumps(manifest, ensure_ascii=False)
    assert '"reward": {}' in blob
    assert "reward_items" not in blob
    assert "reward_money" not in blob
    assert all(o.get("sceneCharacters", []) == [] for o in objs)

    # Player-facing quest copy may not contain em/en dashes.
    for o in objs:
        if o["task"] == "dialog":
            assert "—" not in o["description"] and "–" not in o["description"]
            for c in o["nextObjectiveId"]:
                assert "—" not in c["text"] and "–" not in c["text"]


def main():
    f = Factory(ctors=CTORS, entities=ENTS, checks=CHECKS)
    pool = load_pool(POOL)

    asset = f.entry(
        "asset",
        "create",
        name="Jellyfish Coast - Tidewatch Beach",
        srcId=BG_SRC,
        data={
            "name": "Jellyfish Coast - Tidewatch Beach",
            "type": "SCENE_BACKGROUND",
            "image": "@img:" + BEACH_BG,
            "folder": "JellyfishCoast",
            "frames": 1,
            "speed": 1,
            "hidden": True,
            "onInitialBattleField": False,
            "licenseDetails": "TNR",
        },
    )

    basic = build_enemy(
        f,
        pool,
        name="Jellyfish",
        src_id=BASIC_SRC,
        role="standard",
        rank="JONIN",
        kit=BASIC_KIT,
        avatar=BASIC_AVATAR,
    )
    royal = build_enemy(
        f,
        pool,
        name="Royal Jellyfish",
        src_id=ROYAL_SRC,
        role="boss",
        rank="ELITE JONIN",
        kit=ROYAL_KIT,
        avatar=ROYAL_AVATAR,
    )

    objs = objectives(f)
    quest = f.entry(
        "quest",
        "create",
        name=QUEST_NAME,
        srcId=QUEST_SRC,
        data={
            "name": QUEST_NAME,
            "description": (
                "A quiet stretch of Tidewatch Beach has been closed after luminous "
                "jellyfish began washing into the shallows. Clear the water, then find "
                "what is driving the swarm toward shore."
            ),
            "successDescription": (
                "The Royal Jellyfish retreats beyond the breakers, and the scattered "
                "swarm drifts back out to sea. Tidewatch Beach is safe again."
            ),
            "questType": "event",
            "tierLevel": None,
            "maxAttempts": 1,
            "maxCompletes": 1,
            "retryDelay": "none",
            "attemptDelay": "none",
            "consecutiveObjectives": True,
            "startsAt": None,
            "endsAt": None,
            "content": {
                "objectives": objs,
                "reward": {},
                "sceneBackground": SCENE,
                "sceneCharacters": [],
            },
            "hidden": True,
        },
    )

    manifest = f.manifest([asset, basic, royal, quest])
    manifest = {
        "_note": (
            "Candidate hidden Jellyfish Coast package. Uses only existing shared-pool "
            "jutsu. No rewards. No scene characters. Three @img files use manual-picker "
            "fallback until approved bytes are committed and bound by imagePack."
        ),
        "dedupNames": True,
        "imgSizes": IMG_SIZES,
        "items": manifest["items"],
    }

    verify(manifest, pool)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{OUT}: {len(manifest['items'])} entries, {len(objs)} objectives")


if __name__ == "__main__":
    main()
