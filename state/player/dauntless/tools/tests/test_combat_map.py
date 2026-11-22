#!/usr/bin/env python3
"""The planner's engine facts come from the combat engine map (docs/combat-engine/, read from the game source):
caps from rules.json, Clear / Cleanse sides from each tag's polarity. Fails when a planner table drifts from the
map. Run: python3 tests/test_combat_map.py"""
import os
import shutil
import subprocess
import sys
import tempfile

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


def test_cap_literal_scan():
    # a numeric cap beside a capped term is drift; a CM.CAP_* name is not (PR #129 re-review, finding 4)
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "planner_x.py")
        with open(f, "w") as fh:
            fh.write('a = dmg * min(0.9, g(da, "absorb")[0])\nb = dmg * min(1.0, da[PAR * H + o])\n'
                     'c = dmg * min(CM.CAP_ABSORB, g(da, "absorb")[0])\nd = min(1.0, tot / 3)\n')
        hits = CM.cap_literals(f)
    assert len(hits) == 2 and ":1 " in hits[0] and ":2 " in hits[1], hits
    print("ok: cap literals beside absorb / parry terms are caught")


GAME = os.environ.get("TNR_GAME_SRC") or "/tmp/tnrgit/repo"
_CONSTS = ("app/src/libs/combat/constants.ts", "app/drizzle/constants.ts")


def _have_game():
    return all(os.path.exists(os.path.join(GAME, rel)) for rel in _CONSTS)


def test_rules_match_game_source():
    if not _have_game():
        print(f"skip: no game checkout at {GAME} (set TNR_GAME_SRC)")
        return
    bad, notes = CM.check_source(GAME)
    assert not bad, bad
    # a copy with one cap changed must fail (the reviewer's 0.91 Absorb test)
    with tempfile.TemporaryDirectory() as d:
        for rel in _CONSTS:
            os.makedirs(os.path.dirname(os.path.join(d, rel)), exist_ok=True)
            shutil.copy(os.path.join(GAME, rel), os.path.join(d, rel))
        path = os.path.join(d, _CONSTS[0])
        src = open(path).read()
        assert "export const ABSORB_CAP_RATIO = 0.6;" in src
        open(path, "w").write(src.replace("export const ABSORB_CAP_RATIO = 0.6;", "export const ABSORB_CAP_RATIO = 0.91;"))
        bad, notes = CM.check_source(d)
        assert any("caps.absorb" in b and "0.91" in b for b in bad), bad
        assert any("no git metadata" in n for n in notes), notes
        # rules.py refuses to record an empty commit for a copy without git metadata
        rules = os.path.join(CM.MAP_DIR, "_build", "rules.py")
        r = subprocess.run([sys.executable, rules, d, os.path.join(d, "out.json")], capture_output=True, text=True)
        assert r.returncode != 0 and "--revision" in (r.stderr + r.stdout), (r.returncode, r.stderr)
    print("ok: rules.json matches the game source, and a changed cap is caught")


if __name__ == "__main__":
    test_map_loads()
    test_known_engine_facts()
    test_planner_agrees()
    test_cap_literal_scan()
    test_rules_match_game_source()
