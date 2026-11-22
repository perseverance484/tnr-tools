#!/usr/bin/env python3
"""The planner's engine facts come from the combat engine map (docs/combat-engine/, read from the game source):
caps from rules.json, Clear / Cleanse sides from each tag's polarity. Fails when a planner table drifts from the
map. Run: python3 tests/test_combat_map.py"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import combat_map as CM  # noqa: E402


def test_map_loads():
    assert CM.AVAILABLE, f"map missing at {CM.MAP_DIR}"
    assert len(CM.TAGS) >= 90, len(CM.TAGS)
    assert CM.GAME_COMMIT, "map has no pinned game commit"
    print(f"ok: {len(CM.TAGS)} tags, game @ {CM.GAME_COMMIT}")


def test_known_engine_facts():
    # from the game source (constants.ts, combat.ts POSITIVE / NEGATIVE lists)
    assert CM.CAP_ABSORB == CM.CAP_REFLECT == CM.CAP_LEECH == CM.CAP_AFTERBURN == 0.6
    assert CM.DR_CAP == 0.9 and CM.CAP_PARRY == 1.0
    assert CM.removed_by("absorb") == "clear" and CM.removed_by("wound") == "cleanse"
    assert CM.removed_by("clearprevent") is None
    assert "healprevent" in CM.prevented_by("lifesteal")
    # absorb reads the hit and refills pools; it doesn't reduce it (PR #129 review M2)
    assert ("absorb", "feeds") in [(a, k) for a, k, _ in CM.edges("damage", "outgoing")]
    assert ("absorb", "counters") not in [(a, k) for a, k, _ in CM.edges("damage", "incoming")]
    # summonprevent and elementalseal are action gates, not handler prevents (H5, M3)
    assert ("summon", "hides") in [(a, k) for a, k, _ in CM.edges("summonprevent", "outgoing")]
    assert "any age" in CM.tag("clear")["prevent_check"]
    assert CM.tag("vamp")["stage"].startswith("S10")
    print("ok: caps, polarity, prevents and links read as the source has them")


def test_planner_agrees():
    bad = CM.check_planner()
    for b in bad:
        print("  DRIFT " + b)
    assert not bad, bad
    print("ok: planner2 / turn / shotplan tables agree with the map")


if __name__ == "__main__":
    test_map_loads()
    test_known_engine_facts()
    test_planner_agrees()
