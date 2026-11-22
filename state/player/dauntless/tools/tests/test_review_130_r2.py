"""PR 130 second review (2026-11-22, at 81587565): one check per finding, on the review's own repro numbers.
Run: python3 -m pytest -q tests/test_review_130_r2.py"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); sys.path.insert(0, TOOLS)
import cd_plan, planner2 as p2, shotplan, turn  # noqa: E402

LOADOUT = cd_plan.LOADOUTS["pvp1"]
HIM = "user_38UxfHXcwBi8IyvtblWpaqkoX7y"


def _st():
    return {"used": [], "loadout": list(LOADOUT)}


def _fixture(tmp_path, stored, lines, live=None):
    """tests/mamba_r3.txt (round 3, my turn) with my stored AP set and his round-2 lines on me added. live: extra
    effects on the live snapshot; None drops the snapshot, so the planners read the log (the path these tests
    check; with a snapshot the live list wins, tests/test_review_130_r3.py)."""
    rows = open(os.path.join(HERE, "mamba_r3.txt")).read().split("\n")
    b, e = json.loads(rows[0]), json.loads(rows[1])
    b["battle.usersState.*.actionPoints"] = [stored, 100]
    if live is None:
        b.pop("battle.liveEffects", None)
    else:
        b["battle.liveEffects"] = list(b.get("battle.liveEffects") or []) + live
    for k, v in (("*.battleRound", 2), ("*.userId", HIM), ("*.actionId", "x"), ("*.appliedEffects.*.txt", lines)):
        e[k].append(v)
    path = tmp_path / "state.txt"
    path.write_text(json.dumps(b) + "\n" + json.dumps(e) + "\n")
    return str(path)


# 1. Spendable AP is the stored AP minus the live stun: 80 stored and a 40 stun leave 40, not 60
def test_planner2_build_subtracts_stun_from_stored_ap(tmp_path):
    path = _fixture(tmp_path, 80, ["dauntless is stunned [-40 AP] for the next 2 rounds"])
    P, info = p2.build(type("A", (), dict(file=path, enemy="Mamba", loadout="pvp1")))
    assert (info["ap"], info["ap_full"], info["stun"]) == (40, 80, 40)
    out = p2.legal_bundles(info["st"], info["R"], info["ap"], info["d0"], info["st"]["loadout"], P.me0, P.en0,
                           info["ap_full"])
    assert not [b for b in out if "cleanse" in b]          # a 60-AP Cleanse cannot be cast on 40


def test_turn_subtracts_stun_from_stored_ap(tmp_path):
    assert turn.spendable_ap({"actionPoints": 80}, True, 40) == (80, 40)
    path = _fixture(tmp_path, 80, ["dauntless is stunned [-40 AP] for the next 2 rounds"])
    out = subprocess.run([sys.executable, os.path.join(TOOLS, "turn.py"), path, "--battle", "x", "--enemy", "Mamba",
                          "--no-engine"], capture_output=True, text=True, timeout=300, cwd=TOOLS)
    assert "AP 40 (STUNNED -40)" in out.stdout, out.stdout[-2000:] + out.stderr[-2000:]


# 2. A blocked Cleanse gives no AP back, and the simulator removes nothing with it
def test_blocked_cleanse_gets_no_refund():
    me, en = p2.Side(5050), p2.Side(5050)
    me.add(p2.STUN, 20, 0, 1)
    out = p2.legal_bundles(_st(), 1, 80, 2, LOADOUT, me, en, ap_full=100, cleanse_blocked=True)
    assert out and all(cd_plan.bundle_cost(b) <= 80 for b in out)
    assert ("cleanse", "overflow") not in {tuple(sorted(b)) for b in out}
    out = turn.turn_bundles(_st(), 1, 80, 100, True, False, 2, cleanse_blocked=True)
    assert out and all(cd_plan.bundle_cost(b) <= 80 for b in out)
    assert ("cleanse", "overflow") not in {tuple(sorted(b)) for b in out}
    # not blocked: the refund still applies
    assert ("cleanse", "overflow") in {tuple(sorted(b)) for b in turn.turn_bundles(_st(), 1, 80, 100, True, False, 2)}


def test_planner2_build_reads_cannot_be_cleansed(tmp_path):
    path = _fixture(tmp_path, 100, ["dauntless is stunned [-20 AP] for the next 2 rounds",
                                    "dauntless cannot be cleansed for the next 2 rounds"])
    P, info = p2.build(type("A", (), dict(file=path, enemy="Mamba", loadout="pvp1")))
    assert info["cleanse_blocked"] and not P.cleanse_refund


def test_turn_sim_cleanse_keeps_clear_immunity_and_respects_the_block():
    side = shotplan.Side(5000)
    side.tags = [["clearimmune", 1, 3, 4], ["wound", 100, 3, 4], ["dr", 0.2, 3, 4]]
    turn.cleanse_first(side, 3)
    assert [x[0] for x in side.tags] == ["clearimmune", "dr"]
    side.tags = [["cleanseimmune", 1, 3, 4], ["wound", 100, 3, 4]]
    turn.cleanse_first(side, 3)
    assert [x[0] for x in side.tags] == ["cleanseimmune", "wound"]


# 3. The engine filter keeps a Cleanse bundle that the stun refund pays for: 100 stored, 20 stun, Cleanse + Overflow
def test_engine_filter_keeps_cleanse_bundles():
    cl, ov = turn.ACTION_ID.get("cleanse", "cleanse"), turn.ACTION_ID.get("overflow", "overflow")
    eng = {"ap": 80, "stun": 20, "available": [{"id": cl, "cost": 60}, {"id": ov, "cost": 40}]}
    ok, ap = turn.engine_filter(eng, 20, lambda b: True)
    assert ap == 80 and ok(("cleanse", "overflow"))
    ok, _ = turn.engine_filter(eng, 20, lambda b: False)          # blocked or not ready: no refund
    assert not ok(("cleanse", "overflow"))
    ok, _ = turn.engine_filter({k: v for k, v in eng.items() if k != "stun"}, 20, lambda b: True)   # older engine
    assert ok(("cleanse", "overflow"))
    ok, _ = turn.engine_filter(dict(eng, ap=40, stun=60), 60, lambda b: True)   # Cleanse doesn't fit 40
    assert not ok(("cleanse", "overflow"))


# 4. The kite-back pass prices the bundle with the time-compression surcharge
def test_stepback_uses_surcharged_cost():
    b = ("rebirth", "kunai", "step")
    assert cd_plan.bundle_cost(b, 10) == 100
    assert turn.kite_back([b], 100, 100, False, 10) == []
    assert turn.kite_back([b], 100, 100, False, 0) == [b + ("stepback",)]
