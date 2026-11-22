#!/usr/bin/env python3
"""The planner's engine facts come from the combat engine map (docs/combat-engine/, read from the game source):
caps from rules.json, Clear / Cleanse sides from each tag's polarity. Fails when a planner table drifts from the
map. Run: python3 tests/test_combat_map.py"""
import json
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
    # a cap clamp must be min(<term>, CM.CAP_<its kind>): a literal in either position or across lines, a local name
    # holding a number, another kind's constant or a mixed min is drift (PR #129 reviews 2, 3 and 4)
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "planner_x.py")
        with open(f, "w") as fh:
            fh.write('a = dmg * min(0.9, g(da, "absorb")[0])\n'
                     'b = dmg * min(1.0, da[PAR * H + o])\n'
                     'c = dmg * min(par, 0.91)\n'
                     'e = dmg * min(\n    g(da, "reflect")[0],\n    0.5,\n)\n'
                     'wrong_cap = 0.91\n'
                     'f = dmg * min(par, wrong_cap)\n'
                     'h = dmg * min(CM.CAP_REFLECT, da[PAR * H + o])\n'
                     'k = dmg * min(CM.CAP_PARRY, par + ab)\n'
                     'm = dmg * min(CM.CAP_PARRY, par, 0.95)\n'
                     'n = dmg * min(CM.CAP_NOPE, par)\n'
                     'ok1 = dmg * min(CM.CAP_ABSORB, g(da, "absorb")[0])\n'
                     'ok2 = min(1.0, tot / 3)\n'
                     'ok3 = max(1e-6, 1 - min(CM.CAP_PARRY, e.g(PAR, o)))\n'
                     'ok4 = min(CM.CAP_LEECH, sa[LS * H + o] + sa[PLS * H + o])\n')
        hits = CM.cap_clamps(f)
    lines = sorted(int(h.split(":")[1].split()[0]) for h in hits)
    assert lines == [1, 2, 3, 4, 9, 10, 11, 12, 13], hits
    assert CM.cap_literals is CM.cap_clamps
    # the shipped planners pass, and every clamp they use names an existing constant
    for mod in ("planner2.py", "turn.py", "shotplan.py"):
        assert CM.cap_clamps(os.path.join(os.path.dirname(HERE), mod)) == [], mod
    print("ok: cap clamps must use their own CM.CAP_* constant; literals, local names and wrong constants are caught")


GAME = os.environ.get("TNR_GAME_SRC") or "/tmp/tnrgit/repo"
_CONSTS = ("app/src/libs/combat/constants.ts", "app/drizzle/constants.ts")
_TOOL = os.path.join(os.path.dirname(HERE), "combat_map.py")
_RULES_PY = os.path.join(os.path.dirname(HERE), "..", "..", "..", "..", "docs", "combat-engine", "_build", "rules.py")


def _git(cwd, *args):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t",
               GIT_COMMITTER_EMAIL="t@t")
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True, env=env)


def _check(game, map_dir):
    env = dict(os.environ, TNR_COMBAT_MAP=map_dir, PYTHONDONTWRITEBYTECODE="1")
    env.pop("TNR_GAME_SRC", None)
    return subprocess.run([sys.executable, _TOOL, "--check", "--game", game], capture_output=True, text=True, env=env)


def _map_copy(d, pin, absorb=None, drop_pin=False):
    """A data-only map directory (the three JSON files) re-pinned to pin."""
    os.makedirs(d)
    for name in ("tags.json", "interactions.json", "rules.json"):
        data = json.load(open(os.path.join(CM.MAP_DIR, name)))
        data["pinned_game_commit"] = pin
        if name == "rules.json":
            if absorb is not None:
                data["caps"]["absorb"]["value"] = absorb
            if drop_pin:
                del data["pinned_game_commit"]
        json.dump(data, open(os.path.join(d, name), "w"))
    return d


def test_rules_match_game_source():
    have = _git(GAME, "rev-parse", "--verify", "HEAD").returncode == 0
    if not have:
        print(f"skip: no game checkout at {GAME} (set TNR_GAME_SRC)")
        return
    pin = CM._RULES["pinned_game_commit"]
    bad, notes = CM.check_source(GAME)
    assert not bad, bad
    with tempfile.TemporaryDirectory() as d:
        # a small repo holding the two pinned constants files as one commit
        repo = os.path.join(d, "game")
        os.makedirs(repo)
        _git(repo, "init", "-q")
        for rel in _CONSTS:
            os.makedirs(os.path.dirname(os.path.join(repo, rel)), exist_ok=True)
            open(os.path.join(repo, rel), "w").write(_git(GAME, "show", f"{pin}:{rel}").stdout)
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", "pinned constants")
        sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
        # 1. clean, with a data-only override (the reader comes from this checkout)
        r = _check(repo, _map_copy(os.path.join(d, "m1"), sha))
        assert r.returncode == 0, r.stdout + r.stderr
        # 2. game file and map both changed to 0.91 at the pinned HEAD: the pinned objects still say 0.6
        path = os.path.join(repo, _CONSTS[0])
        src = open(path).read()
        open(path, "w").write(src.replace("export const ABSORB_CAP_RATIO = 0.6;", "export const ABSORB_CAP_RATIO = 0.91;"))
        r = _check(repo, _map_copy(os.path.join(d, "m2"), sha, absorb=0.91))
        assert r.returncode == 1 and "caps.absorb" in r.stdout and "differs" in r.stdout, r.stdout
        # the same dirty tree with the map left at the pinned 0.6 passes: edits are ignored with a note, not used
        r = _check(repo, _map_copy(os.path.join(d, "m2b"), sha))
        assert r.returncode == 0 and "ignored" in r.stdout, r.stdout + r.stderr
        # rules.py refuses to generate from that dirty tree, since the edit is in a constants file it reads
        r = subprocess.run([sys.executable, _RULES_PY, repo, os.path.join(d, "o.json")], capture_output=True, text=True)
        assert r.returncode != 0 and "differ from HEAD" in r.stderr, r.stderr
        # an edit outside those two files doesn't stop it (extract.py and kb.py are the ones that reject any app/ edit)
        subprocess.run(["git", "-C", repo, "checkout", "-q", "--", _CONSTS[0]], check=True)
        other = os.path.join(repo, "app", "src", "other.ts")
        open(other, "w").write("export const X = 1;\n")
        _git(repo, "add", "-A")
        _git(repo, "commit", "-qm", "other file")
        sha2 = _git(repo, "rev-parse", "HEAD").stdout.strip()
        open(other, "w").write("export const X = 2;\n")
        r = subprocess.run([sys.executable, _RULES_PY, repo, os.path.join(d, "o2.json")], capture_output=True, text=True)
        assert r.returncode == 0 and json.load(open(os.path.join(d, "o2.json")))["pinned_game_commit"] == sha2, r.stderr
        open(path, "w").write(src.replace("export const ABSORB_CAP_RATIO = 0.6;", "export const ABSORB_CAP_RATIO = 0.91;"))
        # back on the dirty constants file for the cases below
        r = subprocess.run([sys.executable, _RULES_PY, repo, os.path.join(d, "o.json")], capture_output=True, text=True)
        assert r.returncode != 0 and "differ from HEAD" in r.stderr, r.stderr
        # 3. a missing pin fails
        r = _check(repo, _map_copy(os.path.join(d, "m3"), sha, drop_pin=True))
        assert r.returncode == 1 and "not a full 40-character commit" in r.stdout, r.stdout
        # 4. a copy without git metadata can't be certified, and rules.py needs a full --revision for it
        copy = os.path.join(d, "copy")
        for rel in _CONSTS:
            os.makedirs(os.path.dirname(os.path.join(copy, rel)), exist_ok=True)
            shutil.copy(os.path.join(GAME, rel), os.path.join(copy, rel))
        r = _check(copy, _map_copy(os.path.join(d, "m4"), pin))
        assert r.returncode == 1 and "not a git checkout" in r.stdout, r.stdout
        for extra in ([], ["--revision", pin[:7]]):
            r = subprocess.run([sys.executable, _RULES_PY, copy, os.path.join(d, "o.json"), *extra],
                               capture_output=True, text=True)
            assert r.returncode != 0 and "--revision" in r.stderr, (extra, r.stderr)
        r = subprocess.run([sys.executable, _RULES_PY, copy, os.path.join(d, "o.json"), "--revision", pin],
                           capture_output=True, text=True)
        assert r.returncode == 0 and json.load(open(os.path.join(d, "o.json")))["pinned_game_commit"] == pin, r.stderr
    print("ok: rules.json is checked against the pinned game objects only (working-tree edits are ignored, so they "
          "can't supply a verified value); a wrong map, a missing pin and an unpinned copy fail")


if __name__ == "__main__":
    test_map_loads()
    test_known_engine_facts()
    test_planner_agrees()
    test_cap_literal_scan()
    test_rules_match_game_source()
