"""PR 130 review (2026-11-22): one focused check per finding. Run: python3 -m pytest -q tests/test_review_130.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..")))
import cd_plan, planner2 as p2, policy, shotplan, turn  # noqa: E402

LOADOUT = cd_plan.LOADOUTS["pvp1"]


def _st():
    return {"used": [], "loadout": list(LOADOUT)}


def _stunned(amount):
    me, en = p2.Side(5050), p2.Side(5050)
    me.add(p2.STUN, amount, 0, 1)
    return me, en


# 1. Cleanse is only given the stun's AP back when it can be cast on the stunned AP
def test_planner2_no_cleanse_it_cannot_afford():
    me, en = _stunned(60)
    out = p2.legal_bundles(_st(), 1, 40, 2, LOADOUT, me, en, ap_full=100)
    assert out and not [b for b in out if "cleanse" in b], [b for b in out if "cleanse" in b][:3]
    me, en = _stunned(20)                               # 80 AP: Cleanse (60) fits, and gives the 20 back
    out = p2.legal_bundles(_st(), 1, 80, 2, LOADOUT, me, en, ap_full=100)
    assert any("cleanse" in b and cd_plan.bundle_cost(b) == 100 for b in out)


def test_turn_no_cleanse_it_cannot_afford():
    out = turn.turn_bundles(_st(), 1, 40, 100, True, False, 2)
    assert out and not [b for b in out if "cleanse" in b]
    out = turn.turn_bundles(_st(), 1, 80, 100, True, False, 2)
    assert any("cleanse" in b and cd_plan.bundle_cost(b) == 100 for b in out)


# 2. Time compression is counted while the bundles are built
def test_surcharge_keeps_the_pair_that_fills_the_turn():
    out = {tuple(sorted(b)) for b in turn.turn_bundles(_st(), 1, 100, 100, False, False, 2, surch=10)}
    assert tuple(sorted(("thunders", "overflow"))) in out
    assert tuple(sorted(("thunders", "overflow", "basic"))) not in out
    assert all(cd_plan.bundle_cost(b, 10, 0) <= 100 for b in out)   # a Cleanse lifts it (review 3)
    me, en = p2.Side(5050), p2.Side(5050)
    out2 = {tuple(sorted(b)) for b in p2.legal_bundles(_st(), 1, 100, 2, LOADOUT, me, en, surcharge=10)}
    assert tuple(sorted(("thunders", "overflow"))) in out2
    assert all(cd_plan.bundle_cost(b, 10, 0) <= 100 for b in out2)


# 3. The live capture keeps the stun's size
def test_live_capture_keeps_ap_reduction():
    import pilot
    from player import combat
    e = {"type": "stun", "targetId": "x", "creatorId": "y", "rounds": 2, "createdRound": 3, "apReduction": 60}
    assert pilot.live_effects([e])[0]["apReduction"] == 60
    assert combat.live_effects([e])[0]["apReduction"] == 60


# 4. Cleanse keeps neutral Clear immunity, in the simulator and in the log rebuild
def test_cleanse_keeps_clear_immunity():
    side = shotplan.Side(5000)
    side.tags = [["clearimmune", 1, 3, 4], ["wound", 100, 3, 4], ["dr", 0.2, 3, 4]]
    kept = [x for x in side.tags if not shotplan.negative(x)]
    assert [x[0] for x in kept] == ["clearimmune", "dr"]
    lines = ["3|Mamba cannot be cleared for the next 2 rounds", "3|Mamba was cleared of all negative effects"]
    me, en = shotplan.rebuild(lines, "dauntless", "Mamba", 5000, 5000)
    assert en.live("clearimmune", 4), en.tags


# 5. A hit fired before a move goes through the barrier between my starting tile and him, not the landing's
def test_barrier_from_the_tile_the_hit_is_fired_from():
    class Probe(p2.Planner):
        def __init__(self, board, kit, land):
            self.board, self.my_kit, self._land = board, kit, land

        def landing(self, b):
            return self._land

    seen = []
    real = p2.apply

    def spy(src, dst, act, o, scale=1.0):
        seen.append((act, None if p2.MY_BARRIER is None else list(p2.MY_BARRIER[:2])))
        return 0.0, 0.0
    old_bar, old_ml = turn.BARRIERS, turn.moves_last
    try:
        p2.apply = spy
        turn.moves_last = lambda b, d0: True                  # the attack is in range: the move fires last
        me_pos, en_pos, land = (0, 0), (3, 0), (0, 3)
        turn.BARRIERS = [(1, 0, 900, 0.5, "him")]            # on the line from where I stand, not from the landing
        P = Probe((me_pos, en_pos, set(), 3), {"stormblade": "HIT", "phantom": "MOVE"}, land)
        P.my_turn(p2.Side(5050), p2.Side(5050), ("phantom", "stormblade"), None, 5050, 5050)
        assert seen[0][0] == "HIT" and seen[0][1] == [900, 0.5], seen
    finally:
        p2.apply, turn.BARRIERS, turn.moves_last = real, old_bar, old_ml
