"""planner2 fixes from AP run 2's two losses (2026-11-16: fight 6 vs Shisui, fight 8 vs Selaphiel).
Run: python3 tests/test_loss_fixes.py   (python, no live calls)

1. The planner's "pvp1" kit carried Thunder's Judgement after the game's "PvP" loadout had dropped it: every fight
   opened on a line the game refused ("Action not valid anymore"). The director put it back in place of Limit
   Breaker; pvp1 is pinned to the game's list as read back after that swap.
2. planner2 never priced the kunai by the race (only turn.py did), so it always cost "leaning" (350). Now one
   price, turn.kunai_race, serves both planners and the replay review.
3. DESPERATION ranked lines by his HP loss after his own reply (his lifesteal heals counted against me), so a stance
   that cut his hit read as damage; and it ignored how likely each line was to keep me alive.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cd_plan  # noqa: E402
import planner2 as p2  # noqa: E402
import turn  # noqa: E402
import value_model  # noqa: E402

ITEMS_AND_BASICS = {"smoke", "kims", "pill", "panacea", "jewel", "kunai", "nights", "aetherion", "clear", "cleanse",
                    "replace", "defstance", "offstance", "basic"}


def test_pvp1_is_the_games_pvp_loadout():
    jutsu = [n for n in cd_plan.LOADOUTS["pvp1"] if n not in ITEMS_AND_BASICS]
    ids = [turn.ACTION_ID[n] for n in jutsu]
    assert sorted(ids) == sorted(cd_plan.PVP1_JUTSU_IDS), (sorted(set(ids) ^ set(cd_plan.PVP1_JUTSU_IDS)), jutsu)
    assert "thunders" in cd_plan.LOADOUTS["pvp1"] and "limitbreaker" not in cd_plan.LOADOUTS["pvp1"]
    assert len(cd_plan.PVP1_JUTSU_IDS) == 15
    # the older fights are replayed on the kit they were played with
    assert "thunders" in cd_plan.LOADOUTS["pvp1_thunders"] and "thunders" in cd_plan.LOADOUTS["pvp1_parry"]
    assert "parry" in cd_plan.LOADOUTS["pvp1_parry"] and "resist" not in cd_plan.LOADOUTS["pvp1_parry"]
    print("ok: pvp1 is the game's PvP loadout (Thunder's Judgement in, Limit Breaker out); older fights keep their kit")


def test_one_kunai_price_for_both_planners():
    """turn.kunai_race is the only kunai price: planner2 and turn.py set it through turn.kunai_price, the replay
    review reads it through critique.review_race (consolidated 2026-11-16; planner2 had its own copy)."""
    assert not hasattr(p2, "kunai_price")
    # R9, both at 1900: my turn (5050-1900 + 2200) / 10 = 535; his 535: 3.55 rounds each -> close
    cost, why = turn.kunai_race(1900, 1900, 5050, 9, 535.0, False)
    assert cost == value_model.KUNAI_CLOSE and why.startswith("close race"), (cost, why)
    cost, why = turn.kunai_race(1900, 1900, 5050, 9, 535.0, True)
    assert cost == value_model.KUNAI_NEVER and why == "AFK"
    cost, why = turn.kunai_race(600, 1900, 5050, 9, 1200.0, False)
    assert cost == value_model.KUNAI_NEVER and why.startswith("likely loss"), (cost, why)
    cost, _ = turn.kunai_race(1900, 1900, 5050, 9, 900.0, False)      # his observed average counts when larger
    assert cost == value_model.KUNAI_LEAN, cost
    assert turn.kunai_price(1900, 1900, 5050, 9, 535.0, False).startswith("close race")
    assert value_model.KUNAI_COST == value_model.KUNAI_CLOSE
    value_model.KUNAI_COST = value_model.KUNAI_LEAN
    print("ok: one kunai price (turn.kunai_race) for both planners and the review: free in a close race")


class _Desperate:
    """Three lines, every one far below -0.6 DEATH: (bundle, damage to him on my turn, chance I am dead)."""
    LINES = {("stance",): (100.0, 0.50), ("nuke",): (300.0, 0.95), ("hit",): (200.0, 0.55), ("poke",): (50.0, 0.52)}

    def line(self, b):
        dmg, dead = self.LINES[b]
        feats = [0.0] * p2.NF
        feats[7] = -dead
        return feats, -value_model.DEATH, dmg, [], dead

    def extras(self, b, ap):
        return 0.0, 0.0, 0.0, []


def test_desperation_hits_hardest_among_the_lines_that_live_best():
    res = p2.rank(_Desperate(), list(_Desperate.LINES), 100, p2.load_weights())
    order = [r[1] for r in res]
    # within 0.10 of the best survival (0.50): hit (200), poke? no: stance 100, poke 50; nuke (0.95) after
    assert order == [("hit",), ("stance",), ("poke",), ("nuke",)], order
    print("ok: DESPERATION takes the most off him among the lines that keep me alive best")


def test_what_the_lookahead_may_reorder_when_every_line_loses():
    """rank() says how many lines head the list as those that live best (P.desperate). TNR_DESPERATE_LA then says
    what the lookahead may reorder: "all" as it always has, "alive" only those lines, "off" nothing."""
    looked = []

    class P(_Desperate):
        def lookahead(self, b, follows):                 # two exchanges ahead, the nuke looks best and the hit worst
            looked.append(b)
            return {("nuke",): 9000.0, ("poke",): 500.0, ("stance",): 100.0, ("hit",): 0.0}[b], None
    info = {"st": {"used": [], "loadout": []}, "R": 8}
    was, p2.follow_set = (p2.DESPERATE_LA, p2.follow_set), lambda *a: []
    try:
        ranked = p2.rank(P(), list(_Desperate.LINES), 100, p2.load_weights())
        assert [r[1] for r in ranked] == [("hit",), ("stance",), ("poke",), ("nuke",)]
        for mode, order, seen in (
                ("off", [("hit",), ("stance",), ("poke",), ("nuke",)], 0),
                ("alive", [("poke",), ("stance",), ("hit",), ("nuke",)], 3),      # the three that live best only
                ("all", [("nuke",), ("poke",), ("stance",), ("hit",)], 4)):       # as before: the nuke, 95% dead
            p2.DESPERATE_LA, planner = mode, P()
            res = p2.rank(planner, list(_Desperate.LINES), 100, p2.load_weights())
            assert planner.desperate == 3, planner.desperate
            del looked[:]
            got = [r[1] for r in p2.lookahead_rerank(planner, info, res, 3.0)]
            assert got == order and len(looked) == seen, (mode, got, looked)

        class Fine(P):                                   # one line that does not lose: the switch plays no part
            def line(self, b):
                feats, term, dmg, outs, dead = super().line(b)
                return (feats, 0.0, dmg, outs, 0.05) if b == ("poke",) else (feats, term, dmg, outs, dead)
        p2.DESPERATE_LA, fine = "off", Fine()
        res = p2.rank(fine, list(_Desperate.LINES), 100, p2.load_weights())
        del looked[:]
        p2.lookahead_rerank(fine, info, res, 3.0)
        assert fine.desperate == 0 and len(looked) == 4, (fine.desperate, looked)
    finally:
        p2.DESPERATE_LA, p2.follow_set = was
    print("ok: when every line loses the lookahead reorders all, the lines that live best, or nothing, as it is set")


def test_the_worst_case_reply_check_is_a_setting_and_off():
    """RUL-2026-11-17-166, 2. With TNR_WORST_CASE=guard a line that one of his listed replies kills goes behind the
    lines that survive them all, and the lookahead does not bring it back. Off, nothing moves."""
    class P:
        LINES = {("burst",): (0.9, True), ("hit",): (0.6, False), ("heal",): (0.2, False), ("gamble",): (0.8, True)}

        def __init__(self):
            self._wc = {b: dies for b, (_, dies) in self.LINES.items()}

        def line(self, b):
            feats = [0.0] * p2.NF
            feats[0] = 1000.0 * self.LINES[b][0]                 # the swing: burst, gamble, hit, heal
            return feats, 0.0, 100.0, [], 0.3 if self.LINES[b][1] else 0.0

        def extras(self, b, ap):
            return 0.0, 0.0, 0.0, []

        def lookahead(self, b, follows):                         # two exchanges ahead the burst looks best again
            return (5000.0 if b == ("burst",) else 0.0), None
    info = {"st": {"used": [], "loadout": []}, "R": 4}
    was, p2.follow_set = (p2.WORST_CASE, p2.follow_set), lambda *a: []
    try:
        p2.WORST_CASE = "off"
        res = p2.rank(P(), list(P.LINES), 100, p2.load_weights())
        assert [r[1] for r in res] == [("burst",), ("gamble",), ("hit",), ("heal",)], [r[1] for r in res]
        assert [r[1] for r in p2.lookahead_rerank(P(), info, res, 3.0)][0] == ("burst",)
        p2.WORST_CASE, planner = "guard", P()
        res = p2.rank(planner, list(P.LINES), 100, p2.load_weights())
        assert [r[1] for r in res] == [("hit",), ("heal",), ("burst",), ("gamble",)], [r[1] for r in res]
        after = [r[1] for r in p2.lookahead_rerank(planner, info, res, 3.0)]
        assert after[:2] == [("hit",), ("heal",)] and after[2] == ("burst",), after
        planner._wc = {b: True for b in P.LINES}                  # every line dies to something: nothing to prefer
        res = p2.rank(planner, list(P.LINES), 100, p2.load_weights())
        assert [r[1] for r in res][0] == ("burst",)
        desperate = _Desperate()                                  # every line loses: rank()'s own order stands
        desperate._wc = {("hit",): True, ("stance",): False, ("poke",): False, ("nuke",): True}
        res = p2.rank(desperate, list(_Desperate.LINES), 100, p2.load_weights())
        assert [r[1] for r in res][0] == ("hit",) and desperate.desperate == 3
    finally:
        p2.WORST_CASE, p2.follow_set = was
    assert p2.WORST_CASE == "off" or os.environ.get("TNR_WORST_CASE")
    print("ok: the worst-case reply check moves the lines he can kill behind the rest when it is on; it is off")


def test_round_8_against_ddxxd_under_each_setting():
    """AP test fight 2, round 8, rebuilt from its log (tests/ddxxd_r8.txt). With "alive" and with "off" what is
    fired is one of the lines that live best. With "all", today's setting, it is whatever the lookahead likes:
    printed, not judged. His model grows with every logged fight against him; should this stop being a position
    where every line loses, this check says so and the one above still holds."""
    import json
    import re
    import subprocess
    tools = os.path.dirname(HERE)
    for mode in ("alive", "off", "all"):
        out = subprocess.run([sys.executable, os.path.join(tools, "planner2.py"), os.path.join(HERE, "ddxxd_r8.txt"),
                              "--battle=6_UqBB_MXSIqobeRrfmdd", "--enemy=DDXXD", "--loadout=pvp1_thunders", "--top=3"],
                             capture_output=True, text=True, timeout=600, cwd=tools,
                             env=dict(os.environ, TNR_LOOKAHEAD="1", TNR_DESPERATE_LA=mode))
        assert out.returncode == 0, out.stderr[-800:]
        said = re.search(r"^DESPERATION: .*\(die (\d+)%\)", out.stdout, re.M)
        if not said:
            print("note: round 8 against DDXXD is no longer a position where every line loses; not checked")
            return
        first = next(ln for ln in out.stdout.splitlines() if re.match(r"\s*1\.\s+[+-]\d", ln))
        dead = int(re.search(r"dead (\d+)%", first).group(1))
        fire = [a["name"] for a in json.loads(next(ln for ln in out.stdout.splitlines() if ln.startswith("FIRE:"))[5:])]
        assert all(n in first for n in fire), (fire, first)
        if mode != "all":
            assert dead <= int(said.group(1)) + 10, (mode, said.group(0), first)
        print(f"ok: round 8 against DDXXD, lookahead over {mode}: fires {'+'.join(fire)} (dead {dead}%, "
              f"best {said.group(1)}%)")


def test_damage_to_him_is_my_turns_not_after_his_reply():
    """On a real state: line()'s damage is his HP after my turn alone (his reply's heals do not move it)."""
    import exam
    bid, (enemy, loadout) = next(iter(exam.EXAM.items()))
    for r, b, e, his, hp in exam.turns(bid, enemy):
        path = os.path.join(HERE, f"_lf_{bid}_{r}.txt")
        with open(path, "w") as f:
            import json
            f.write(json.dumps(b) + "\n" + json.dumps(e) + "\n")
        try:
            P, info = p2.build(type("A", (), dict(file=path, enemy=enemy, loadout=loadout)))
        finally:
            os.unlink(path)
        if P is None or not info["my_turn"]:
            continue
        bundles = p2.legal_bundles(info["st"], info["R"], info["ap"], info["d0"], info["st"]["loadout"], P.me0, P.en0)
        for bd in bundles[:40]:
            feats, term, dmg, outs, dead = P.line(bd)
            m0, e0 = P.me0.copy(), P.en0.copy()
            if "cleanse" in bd:
                m0.wipe(p2.NEGK)
            P.move_ground(m0, bd)                      # moves: his ground where they land
            p2.run_turn(m0, e0, [P.my_kit[x] for x in bd if x in P.my_kit], 0, *P.caps)
            assert abs(dmg - min(P.en0.hp, P.en0.hp - e0.hp)) < 1e-6, (bd, dmg, P.en0.hp - e0.hp)
            assert 0.0 <= dead <= 1.0, (bd, dead)
        print(f"ok: damage to him is measured after my turn, before his reply ({bid[:6]} R{info['R']}, "
              f"{min(40, len(bundles))} lines)")
        return
    raise AssertionError("no exam state on my turn")


if __name__ == "__main__":
    test_pvp1_is_the_games_pvp_loadout()
    test_one_kunai_price_for_both_planners()
    test_desperation_hits_hardest_among_the_lines_that_live_best()
    test_what_the_lookahead_may_reorder_when_every_line_loses()
    test_the_worst_case_reply_check_is_a_setting_and_off()
    test_round_8_against_ddxxd_under_each_setting()
    test_damage_to_him_is_my_turns_not_after_his_reply()
