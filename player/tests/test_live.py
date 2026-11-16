"""The live session of 2026-11-11 (duet/ai-player-ap1-live @ 112aadbd; the review is the doc "AP1 live session
review"). It ran on 583fe353. One class per defect it showed that the corrected head (39f30ead) still had; each
test fails there. The last class replays the shape of the session's first fight: eleven rounds, a relay that takes
seven to thirteen seconds a batch, reads that come back without the battle, and a battle log with a short column.
"""
import json
import os
import unittest

from player import budget as B, calls as K, config as C
from player.tests.support import FOE, LINE, Rig, battle_read, fixture, gone, log_read, res, start_fight, user
from player.tests.test_review import Game, NOT_VALID, about, acts, answers, turns


def refused(out, text):
    return [res("combat.performAction", {"notification": text}, {"battleId": "B1", "actionId": a}) for a in acts(out)]


class AReadWithoutTheBattle(unittest.TestCase):
    """Live: four reads came back without the battle; each closed a fight that was still on and sent a potion."""

    def test_it_does_not_end_the_fight_and_no_potion_goes(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.usersEffects": []})
        rig.tick(*answers(out), battle_read("B1", his))
        calls = []
        for _ in range(4):
            out = rig.tick(battle_read("B1", {"note": "not the battle"}), user("BATTLE", bid="B1"), dt=out["hold"] + 4)
            calls += rig.calls(out)
        self.assertEqual((len(rig.events("fight_start")), rig.world.in_battle()), (1, True))   # was 2 starts
        self.assertNotIn("item.consume", calls)
        self.assertEqual(rig.events("item") + rig.events("fight_end"), [])
        self.assertIn("not the battle", about(rig, "read")[0]["text"])      # what the read held is on record

    def test_the_fight_keeps_what_it_knew(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.world["battle"]["banned"] = ["kunai_id"]
        n = len(rig.world["battle"]["entries"])
        rig.tick(battle_read("B1", {}), user("BATTLE", bid="B1"))
        state = rig.world["battle"]
        self.assertEqual((state["banned"], len(state["entries"]), state["turn"]["round"]),
                         (["kunai_id"], n, battle["battle.round"]))

    def test_my_profile_leaving_the_battle_ends_it_with_the_potion(self):
        rig = Rig()
        start_fight(rig)
        out = gone(rig)
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])
        rig.tick(res("item.consume", {"success": True}, out["steps"][0]["input"]), user())
        self.assertEqual(rig.events("fight_end")[0]["result"], "won")

    def test_the_profile_is_asked_until_it_answers_even_in_a_full_minute(self):
        rig = Rig()
        start_fight(rig)
        rig.world["budget"]["calls"] = [[rig.t, "battle"]] * (C.CALL_LIMIT - B.TURN_ACTIONS - 3)
        out = rig.tick(battle_read("B1", {}))
        self.assertIn("profile.getUser", rig.calls(out))                    # the watching reads gave way, not this
        out = rig.tick(battle_read("B1", {}))                               # it did not come back: asked again
        self.assertIn("profile.getUser", rig.calls(out))


class TheLogWithAShortColumn(unittest.TestCase):
    """Live: from round 6 on every log read was dropped, because a line with no effect is left out of the text
    column."""

    def ragged(self, n=3):
        ids = [f"x{i}" for i in range(n)]
        return dict(zip(K.ENT, (ids, [3] * n, [FOE] * n, ["a"] * n, [["hit"]] * (n - 1))))

    def test_the_lines_are_kept_and_the_next_reads_ask_for_whole_effects(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.usersEffects": []})
        n = len(rig.world["battle"]["entries"])
        out = rig.tick(*answers(out), battle_read("B1", his), log_read("B1", self.ragged()))
        rows = rig.world["battle"]["entries"][n:]
        self.assertEqual([r[0] for r in rows], ["x2", "x1", "x0"])          # was: none of them
        self.assertEqual({str(r[4]) for r in rows}, {"None"})                # whose text is whose is not known
        select = next(s for s in out["steps"] if s.get("call") == "combat.getBattleEntries")["select"]
        self.assertEqual(select[-1], "*.appliedEffects")
        self.assertEqual(len(about(rig, "selects")), 1)
        whole = dict(zip(K.ENT[:4], (["x0", "x1", "x2"], [3] * 3, [FOE] * 3, ["a"] * 3)))
        whole["*.appliedEffects"] = [[{"txt": "hit", "color": "red"}], [], [{"txt": "burn"}, {"no": "text"}]]
        rig.tick(battle_read("B1", his), log_read("B1", whole))
        texts = {r[0]: r[4] for r in rig.world["battle"]["entries"][n:]}
        self.assertEqual(texts, {"x0": ["hit"], "x1": [], "x2": ["burn"]})   # filled in, each on its own line
        self.assertEqual(len(about(rig, "selects")), 1)                      # said once

    def test_the_tools_get_a_list_where_the_texts_are_not_known(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.tick(*answers(out), battle_read("B1", dict(battle, **{"battle.activeUserId": FOE})),
                 log_read("B1", self.ragged()))
        gone(rig)
        with open(os.path.join(rig.combat.fights, "B1_entries.json"), encoding="utf8") as f:
            saved = json.load(f)
        self.assertEqual(len({len(v) for v in saved.values()}), 1)
        self.assertTrue(all(isinstance(t, list) for t in saved[K.ENT[4]]))

    def test_a_log_whose_plain_columns_do_not_line_up_is_still_dropped(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        n = len(rig.world["battle"]["entries"])
        bad = dict(self.ragged(), **{"*.userId": [FOE]})
        rig.tick(battle_read("B1", battle), log_read("B1", bad))
        self.assertEqual(len(rig.world["battle"]["entries"]), n)


class ATurnsLaterPlans(unittest.TestCase):
    """Live, round 6: two plans landed, the turn was still mine at T+24 s, and the planner was given no time."""

    def test_a_turn_that_has_acted_still_gets_the_planner(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        more = dict(battle, **{"battle.version": battle["battle.version"] + 2})
        out = rig.tick(*answers(out), battle_read("B1", more), dt=C.BEST_LINE_AT + 9)   # T+24, as live
        self.assertGreaterEqual(rig.combat.plan_args[-1]["seconds"], 3.0)   # was below zero: "out of time"
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])          # was Defensive Stance
        self.assertEqual(about(rig, "planner") + about(rig, "turn"), [])     # nor is that a late turn

    def test_the_turns_timing_is_its_first_plans(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        more = dict(battle, **{"battle.version": battle["battle.version"] + 2})
        out = rig.tick(*answers(out), battle_read("B1", more), dt=24)
        his = dict(more, **{"battle.activeUserId": FOE, "battle.version": more["battle.version"] + 2})
        rig.tick(*answers(out), battle_read("B1", his), dt=7)
        row = turns(rig)[-1]
        self.assertEqual((row["fired_after"], row["last_fired_after"], row["plans"], row["outcome"]),
                         (0.0, 24.0, 2, "acted"))                            # was fired_after 31.6 in the session

    def test_a_first_plan_past_twenty_seconds_is_still_a_finding(self):
        rig = Rig()
        rig.world["control"]["director_mode"] = True                        # the one way a first plan is that late
        battle, ents = fixture()
        rig.tick(user("BATTLE", bid="B1"))
        live = dict(battle, **{"battle.usersEffects": []})
        rig.tick(battle_read("B1", live), log_read("B1", ents))
        rig.tick(battle_read("B1", live), dt=C.HANDOFF_WAIT + 1)
        self.assertEqual([e["about"] for e in rig.events("finding")], ["turn"])


class ARefusalInAnyWords(unittest.TestCase):
    """Live: Defensive Stance was refused and sent again four times. The corrected head still did that when the
    refusal was not the one text it knew."""

    def test_an_action_refused_in_words_the_code_does_not_know_is_not_sent_again_this_turn(self):
        rig = Rig()
        rig.combat.line = None
        battle, ents, out = start_fight(rig)
        sent = [acts(out)]
        for _ in range(3):
            out = rig.tick(*refused(out, "Not enough action points"), battle_read("B1", battle), dt=2)
            sent.append(acts(out))
        self.assertEqual(sent, [["defensiveStance"], ["wait"], [], []])     # was the stance four times
        self.assertEqual([e["text"] for e in about(rig, "refusal")],
                         ["the game refused defensiveStance: Not enough action points",
                          "the game refused wait: Not enough action points"][:1])   # each reason once

    def test_it_is_allowed_again_on_my_next_turn(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(*refused(out, "Not enough action points"), battle_read("B1", battle), dt=2)
        self.assertEqual(rig.world["battle"].get("banned", []), [])         # nothing is banned for the fight
        nxt = dict(battle, **{"battle.round": battle["battle.round"] + 1, "battle.version": battle["battle.version"] + 3})
        out = rig.tick(battle_read("B1", nxt), dt=20)
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])

    def test_not_valid_anymore_still_bans_for_the_fight(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.tick(*answers(out, NOT_VALID), battle_read("B1", battle))
        self.assertEqual(rig.world["battle"]["banned"], [a["actionId"] for a in LINE])

    def test_a_stand_in_the_game_took_without_effect_is_not_sent_again(self):
        rig = Rig()
        rig.combat.line = None
        battle, ents, out = start_fight(rig)
        self.assertEqual(acts(out), ["defensiveStance"])
        out = rig.tick(battle_read("B1", battle), dt=3)                     # no answer, and the battle has not moved
        self.assertEqual(acts(out), ["wait"])


class TheEndOfASession(unittest.TestCase):
    """Live: the relay was stopped with the character awake at 648 HP in an enemy sector. A rematch began with
    nothing running, and its first round went unplayed."""

    def test_the_relay_is_stopped_only_once_the_character_is_asleep_at_home(self):
        rig = Rig()
        rig.world["control"]["end_session"] = True
        out = rig.tick(user(hp=648, sector=1490))
        self.assertEqual((out["stop"], out["activity"], rig.calls(out)[0]), (None, "recovery", "item.consume"))
        out = rig.tick(res("item.consume", {"success": True}, {}), user(sector=1490))
        self.assertEqual((out["stop"], out["activity"]), (None, "session"))                 # was: STOP, awake
        self.assertEqual(rig.calls(out), ["travel.startGlobalMove", "travel.finishGlobalMove", "profile.getUser"])
        self.assertEqual(out["steps"][0]["input"], {"sector": C.HOME_SECTOR})
        out = rig.tick(user("TRAVEL", sector=1490))
        self.assertEqual((out["stop"], out["activity"]), (None, "travel"))
        out = rig.tick(user(sector=C.HOME_SECTOR))
        self.assertEqual((out["stop"], rig.calls(out)), (None, ["home.toggleSleep", "profile.getUser"]))
        out = rig.tick(user("ASLEEP", sector=C.HOME_SECTOR))
        self.assertEqual(out["stop"], "session ended by the director: asleep at home")
        self.assertEqual(about(rig, "gate"), [])                            # every call was the session's to make

    def test_an_ending_session_picks_no_new_fight_but_fights_back(self):
        rig = Rig()
        rig.tick(user(sector=1490))
        rig.world["control"]["end_session"] = True
        out = rig.tick(user(sector=1490))
        self.assertNotIn("travel.getSectorData", rig.calls(out))            # no scan, no attack
        out = rig.tick(user("BATTLE", bid="B5", sector=1490))
        self.assertEqual((out["stop"], out["activity"]), (None, "battle"))

    def test_a_sleeper_is_not_woken_by_an_ending_session(self):
        rig = Rig()
        rig.world["control"]["end_session"] = True
        rig.tick()
        out = rig.tick(user("ASLEEP", sector=C.HOME_SECTOR))
        self.assertEqual((out["stop"], rig.calls(out)), ("session ended by the director: asleep at home", []))


class RoundsNobodyPlayed(unittest.TestCase):
    """Live: the brain joined the rematch in round 2 and reported zero missed turns for the fight."""

    def test_rounds_over_before_the_brain_joined_are_counted_and_named(self):
        rig = Rig()
        battle, ents = fixture()                                            # round 3; round 1 has no line of mine
        start_fight(rig, ents=ents)
        self.assertEqual((rig.world["battle"]["joined"], rig.world["battle"]["unseen_rounds"]), (3, [1]))
        self.assertEqual(rig.status()["turns_unseen"], 1)
        gone(rig)
        rig.tick(user())
        end = rig.events("fight_end")[0]
        self.assertEqual((end["joined"], end["unseen_rounds"]), (3, [1]))
        self.assertEqual(rig.world["records"]["turns_missed"], 0)           # not proof of a missed turn: kept apart

    def test_a_wait_of_mine_in_the_log_is_a_timeout_not_an_action(self):
        """The rematch's saved log: round 1, with nothing running, holds one line of mine: wait."""
        rig = Rig()
        battle, ents = fixture()
        R = battle["battle.round"]
        timed_out = {k: [x] + ents[k] for k, x in zip(K.ENT, ("e_wait", 1, C.ME, "wait", []))}
        start_fight(rig, ents=timed_out)
        self.assertEqual(rig.world["battle"]["unseen_rounds"], [1])         # still a round nobody played
        rig = Rig()
        battle, ents, out = start_fight(rig)
        wait = log_read("B1", dict(zip(K.ENT, (["e_w"], [R], [C.ME], ["wait"], [[]]))))
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.round": R + 1})
        rig.tick(*answers(out, NOT_VALID), battle_read("B1", his), wait)
        self.assertEqual(turns(rig)[-1]["outcome"], "missed")               # was acted, on the log's word


class LiveGame(Game):
    """The stand-in game with the session's faults: from `bad_from` on, a read that asks for the ground columns
    comes back without the battle, and so does every `empty_every`-th other read of the fight; the log's text
    column is short from that round on; the relay takes `lags` seconds over its batches, in turn."""

    def __init__(self, rig, bad_from=6, empty_every=5, lags=(9, 8, 10, 13, 7, 11), **kw):
        self.bad_from, self.empty_every, self.lags, self.n, self.potions_in_fight = bad_from, empty_every, lags, 0, 0
        super().__init__(rig, **kw)

    def answer(self, step, now):
        ep, inp = step["call"], step["input"]
        self.lag = self.lags[self.n % len(self.lags)]
        if ep == "item.consume":
            self.potions_in_fight += 1                                      # only reached while the fight is on
        if ep == "combat.getBattle" and self.R >= self.bad_from:
            self.n += 1
            if any(k.startswith("battle.groundEffects") for k in step["select"]) or self.n % self.empty_every == 0:
                return res(ep, {}, inp)
        out = super().answer(step, now)
        if ep == "combat.getBattleEntries" and self.R >= self.bad_from and inp["limit"] <= 8 \
                and "*.appliedEffects" not in step["select"] and out.data["*.id"]:
            out.data[K.ENT[4]] = out.data[K.ENT[4]][1:]                     # one line has no effect: a short column
        return out


class TheSessionsFirstFightAgain(unittest.TestCase):
    def test_eleven_rounds_with_the_sessions_faults(self):
        rig = Rig()
        game = LiveGame(rig, his_turn=25.0)
        game.play(11 * 60)
        played = turns(rig)
        self.assertGreaterEqual(len(played), 11)
        self.assertEqual({t["outcome"] for t in played}, {"acted"})          # every turn played, none in doubt
        self.assertLessEqual(max(t["fired_after"] for t in played), C.FIRE_BY)   # first actions out in time
        self.assertEqual(len(rig.events("fight_start")), 1)                  # the session opened this fight 4 times
        self.assertEqual((game.potions_in_fight, rig.events("item")), (0, []))   # and sent 4 potions into it
        self.assertEqual(rig.world["records"]["turns_missed"] + rig.world["records"]["turns_unresolved"], 0)
        self.assertGreater(len(about(rig, "read")), 0)                       # the empty reads are on record
        self.assertEqual(len(about(rig, "selects")), 1)                      # and the short column, once
        mine = {e[1] for e in rig.world["battle"]["entries"] if e[2] == C.ME}
        self.assertGreaterEqual(len(mine), 11)                               # the log kept every round of mine


if __name__ == "__main__":
    unittest.main()
