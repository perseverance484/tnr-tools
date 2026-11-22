"""PR 130 third review (2026-11-22, at 3ebdf4ba): one check per finding on the review's repro numbers, plus the
siblings the AP-path sweep found. Run: python3 -m pytest -q tests/test_review_130_r3.py"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE); sys.path.insert(0, TOOLS)
import cd_plan, engine_bridge, planner2 as p2, shotplan, turn  # noqa: E402

ME, HIM = turn.ME, "user_38UxfHXcwBi8IyvtblWpaqkoX7y"


def _fixture(tmp_path, stored, live=(), lines=(), drop=()):
    """tests/mamba_r3.txt (round 3, my turn: his round-2 stun 20 and time compression on me, in the log and on the
    live list): my stored AP, extra live-snapshot effects, his round-2 log lines, live effect types to drop."""
    rows = open(os.path.join(HERE, "mamba_r3.txt")).read().split("\n")
    b, e = json.loads(rows[0]), json.loads(rows[1])
    b["battle.usersState.*.actionPoints"] = [stored, 100]
    b["battle.liveEffects"] = [x for x in b.get("battle.liveEffects") or [] if x.get("type") not in drop] + list(live)
    if lines:
        for k, v in (("*.battleRound", 2), ("*.userId", HIM), ("*.actionId", "x"), ("*.appliedEffects.*.txt", list(lines))):
            e[k].append(v)
    path = tmp_path / "state.txt"
    path.write_text(json.dumps(b) + "\n" + json.dumps(e) + "\n")
    return str(path)


def _eff(t, **kw):
    return dict({"type": t, "targetId": ME, "creatorId": HIM, "rounds": 2, "createdRound": 2, "castThisRound": False,
                 "isNew": False, "fromType": "jutsu", "power": 100, "level": 1}, **kw)


def _turn_main(path):
    out = subprocess.run([sys.executable, os.path.join(TOOLS, "turn.py"), path, "--battle", "x", "--enemy", "Mamba",
                          "--no-engine"], capture_output=True, text=True, timeout=300, cwd=TOOLS)
    return out.stdout + out.stderr


# 1. The live snapshot sets the AP budget, as it sets the combat model: 100 stored, a live 60 stun, none in the log
def test_planner2_budget_from_live_snapshot(tmp_path):
    path = _fixture(tmp_path, 100, live=[_eff("stun", apReduction=60)])
    P, info = p2.build(type("A", (), dict(file=path, enemy="Mamba", loadout="pvp1")))
    assert P.me0.g(p2.STUN, 0) == 60                       # the combat model has it
    assert (info["ap"], info["ap_full"], info["stun"]) == (40, 100, 60)


def test_turn_budget_from_live_snapshot(tmp_path):            # sweep: turn.py never read the live list at all
    out = _turn_main(_fixture(tmp_path, 100, live=[_eff("stun", apReduction=60)]))
    assert "AP 40 (STUNNED -60)" in out, out[-2000:]


def test_live_snapshot_wins_over_the_log(tmp_path):           # a log stun the live list no longer has costs nothing
    path = _fixture(tmp_path, 100, lines=["dauntless is stunned [-40 AP] for the next 2 rounds"],
                    drop=("stun", "timecompression"))
    P, info = p2.build(type("A", (), dict(file=path, enemy="Mamba", loadout="pvp1")))
    assert (info["ap"], info["ap_surcharge"]) == (100, 0)


def test_real_snapshot_mamba_r3(tmp_path):                    # the captured state: a 20 stun and +10, live and logged
    P, info = p2.build(type("A", (), dict(file=_fixture(tmp_path, 100), enemy="Mamba", loadout="pvp1")))
    assert (info["ap"], info["stun"], info["ap_surcharge"]) == (80, 20, 10)


def test_live_ap_state_reads_like_the_engine():
    x = turn.live_ap_state([_eff("stun", apReduction=40), _eff("stun", apReduction=20),
                            _eff("stun", apReduction=60, castThisRound=True),         # cast this round: not yet
                            _eff("timecompression"), _eff("cleanseprevent"),
                            _eff("stun", apReduction=100, targetId=HIM)], ME)
    assert x == {"stun": 40, "surcharge": 10, "kept": 0, "blocked": True}
    x = turn.live_ap_state([_eff("timecompression", fromType="bloodline", rounds=None)], ME)
    assert (x["surcharge"], x["kept"]) == (10, 10)                                  # a bloodline source stays


# 2. Cleanse lifts time compression for what follows: 100 stored, 20 stun, +10, only Cleanse and Overflow ready
def test_cleanse_lifts_the_surcharge_turn():
    st = {"used": [], "loadout": ["cleanse", "overflow"]}
    out = {tuple(sorted(b)) for b in turn.turn_bundles(st, 1, 80, 100, True, False, 2, surch=10, kept=0)}
    assert ("cleanse", "overflow") in out
    out = {tuple(sorted(b)) for b in turn.turn_bundles(st, 1, 100, 100, False, False, 2, surch=10, kept=0)}
    assert ("cleanse", "overflow") in out                  # no stun: 60 + 40 fills the turn too
    out = {tuple(sorted(b)) for b in turn.turn_bundles(st, 1, 100, 100, False, False, 2, surch=10, kept=10)}
    assert ("cleanse", "overflow") not in out              # a bloodline compression survives Cleanse
    out = {tuple(sorted(b)) for b in turn.turn_bundles(st, 1, 80, 100, True, False, 2, surch=10,
                                                       cleanse_blocked=True)}
    assert ("cleanse", "overflow") not in out


def test_cleanse_lifts_the_surcharge_planner2():
    me, en = p2.Side(5050), p2.Side(5050)
    me.add(p2.STUN, 20, 0, 1)
    out = {tuple(sorted(b)) for b in p2.legal_bundles({"used": [], "loadout": ["cleanse", "overflow"]}, 1, 80, 2,
                                                       ["cleanse", "overflow"], me, en, ap_full=100, surcharge=10)}
    assert ("cleanse", "overflow") in out, out
    assert cd_plan.bundle_cost(("cleanse", "overflow"), 10, 0) == 100
    assert cd_plan.bundle_cost(("cleanse", "overflow"), 10) == 110


def test_engine_filter_prices_jutsu_after_cleanse():
    cl, ov = turn.ACTION_ID.get("cleanse", "cleanse"), turn.ACTION_ID.get("overflow", "overflow")
    eng = {"ap": 80, "stun": 20, "available": [{"id": cl, "cost": 60}, {"id": ov, "cost": 50}]}   # engine: +10 live
    ok, _ = turn.engine_filter(eng, 20, lambda b: True, None, 10, 0)
    assert ok(("cleanse", "overflow"))
    ok, _ = turn.engine_filter(eng, 20, lambda b: True, None, 10, None)    # blocked: no lift
    assert not ok(("cleanse", "overflow"))


# 3. A replay budget never exceeds the live one: 90 left, rebirth + kunai + step costs exactly 90
def test_replay_budget_capped_at_live_ap():
    rb, ku = turn.ACTION_ID.get("rebirth", "rebirth"), turn.ACTION_ID.get("kunai", "kunai")
    eng = {"ap": 100, "stun": 0, "available": [{"id": rb, "cost": 60}, {"id": ku, "cost": 20}]}   # replay reset to 100
    ok, ap = turn.engine_filter(eng, 0, lambda b: False, live_ap=90)
    assert ap == 90
    b = ("rebirth", "kunai", "step")
    assert ok(b) and turn.kite_back([b], ap, ap, False) == []


def test_replay_request_carries_live_ap(monkeypatch):
    monkeypatch.setattr(engine_bridge, "_records", lambda: {})
    monkeypatch.setattr(engine_bridge, "_profile", lambda: {"jutsuLevels": {}})
    monkeypatch.setattr(engine_bridge, "_his_kit", lambda *a: [])
    me = {"curHealth": 5000}
    req = engine_bridge._replay_request([], ME, HIM, me, dict(me, userId=HIM), (1, 1), (2, 2), 3, "same", {}, ap=90)
    assert req["me"]["ap"] == 90
    src = open(os.path.join(TOOLS, "..", "..", "..", "..", "harness", "pvp_turn", "engine", "replay_sim.ts")).read()
    assert "setActive(b, req.me.id, req.me.ap)" in src


# sweep: the next-turn lookahead uses the same AP rules
def test_next_turn_follow_ups_get_the_cleanse_refund():
    assert p2.follow_fits(("cleanse", "overflow"), 80)
    assert not p2.follow_fits(("cleanse", "overflow"), 40)       # Cleanse cannot be cast on 40
    m, e = shotplan.Side(5000), shotplan.Side(5000)
    m.tags = [["stun", 20, 2, 3], ["apcost", 10, 2, 3]]
    st = {"used": [], "loadout": ["cleanse", "overflow"]}
    out = {tuple(sorted(b)) for b in turn.next_bundles(st, 2, 80, m, e, set(), 2)}
    assert ("cleanse", "overflow") in out
