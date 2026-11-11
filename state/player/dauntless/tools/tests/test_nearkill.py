"""Near-kill rules (director 2026-11-11, Korin R11: fired for a kill he survived on 42 HP). Python only.
Run: python3 tests/test_nearkill.py"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import shotplan, turn  # noqa: E402


def test_ground_taken_rebuilt():
    lines = ["10|Korin marked the ground with decreasedamagetaken for the next 2 rounds",
             "10|Korin damage given [all damage] is increased by up to 30% for the next 2 rounds",
             "7|dauntless marked the ground with decreasedamagetaken for the next 2 rounds",
             "7|dauntless damage taken [all damage] is decreased by up to 20% for the next 1 rounds"]
    me, en = shotplan.rebuild(lines, "dauntless", "Korin", 1258, 1188)
    assert [t[:5] for t in en.tags if shotplan.ground(t)] == [["dr", shotplan.GROUND_DR, 10, 12, "ground"]], en.tags
    mine = [t for t in me.tags if t[0] == "dr"]
    assert len(mine) == 1 and abs(mine[0][1] - 0.20) < 1e-9, me.tags      # the landing line is not counted twice
    # his R11 hit on the tile is cut by the ground
    e = shotplan.Side(1188); e.tags = list(en.tags)
    m = shotplan.Side(1258)
    d, _ = shotplan.apply(m, e, (1000, []), 11, True)
    assert abs(d - 1000 * (1 - shotplan.GROUND_DR)) < 1, d
    # a later move of his takes it off
    rows = [(10, "K", "GAyHRgaa1lkYGhE9WxlRL", ["Korin marked the ground with decreasedamagetaken for the next 2 rounds"]),
            (11, "K", "replacementTechnique", [])]
    shotplan.off_ground(en, rows, "K", {"GAyHRgaa1lkYGhE9WxlRL", "replacementTechnique"})
    assert not any(shotplan.ground(t) for t in en.tags), en.tags
    print("ok: Phantom Step's ground -taken is modelled on whoever stands on it")


def test_kill_chance():
    assert turn.kill_chance(1100, 1188, 0.12) == 0.0
    assert turn.kill_chance(1188, 1188, 0.12) == 0.5
    assert turn.kill_chance(1188 / 0.88 + 1, 1188, 0.12) == 1.0
    assert 0.5 < turn.kill_chance(1300, 1188, 0.12) < 1.0
    print("ok: a forecast kill counts as sure only with the margin to spare")


if __name__ == "__main__":
    test_ground_taken_rebuilt()
    test_kill_chance()
