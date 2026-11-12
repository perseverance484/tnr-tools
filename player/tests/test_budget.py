"""The call budget's three lanes and the turn clock (design 4.6)."""
import json
import os
import unittest

from player import budget as B
from player import calls as K
from player import config as C
from player.tests.support import Rig, user


class Lanes(unittest.TestCase):
    def setUp(self):
        self.rig = Rig()
        self.rig.tick(user())
        self.rig.world["budget"]["calls"] = []
        self.b = self.rig.brain.budget

    def test_the_world_lane_is_paced_to_its_cap(self):
        steps, waited = self.b.pace([K.user()] * C.WORLD_CAP, "world")
        self.assertEqual((len(steps), waited), (C.WORLD_CAP, 0))
        steps, waited = self.b.pace([K.user(), K.user()], "world")
        self.assertIn("wait", steps[0])                                # the 21st call in the minute waits
        self.assertGreater(waited, 40)
        self.assertEqual(self.b.used(self.rig.t + 200), 0)             # and the window empties with time

    def test_actions_and_recovery_wait_for_nothing_but_the_accounts_limit(self):
        self.b.pace([K.user()] * C.WORLD_CAP, "world")
        steps, waited = self.b.pace([K.act("B", "a", 1, 1, 3)] * 6, "battle")
        self.assertEqual((len(steps), waited), (6, 0))
        steps, waited = self.b.pace([K.potion("p"), K.user(), K.hospital(), K.user()], "recovery")
        self.assertEqual((len(steps), waited), (4, 0))
        self.assertEqual(self.b.used(), C.CALL_LIMIT)                  # the minute is full, and nothing has waited
        steps, waited = self.b.pace([K.act("B", "a", 1, 1, 3)], "battle")
        self.assertIn("wait", steps[0])                                # the 31st call waits: it would be refused
        self.assertEqual(self.rig.events("finding")[-1]["about"], "budget")   # and the wait is on record

    def test_no_read_takes_the_room_of_a_turns_actions(self):
        steps, waited = self.b.pace([K.battle("B")] * (C.CALL_LIMIT - B.TURN_ACTIONS + 1), "battle")
        self.assertIn("wait", steps[-2])                               # the read past that mark waits
        self.rig.world["budget"]["calls"].pop()
        steps, waited = self.b.pace([K.act("B", "a", 1, 1, 3)] * B.TURN_ACTIONS, "battle")
        self.assertEqual(waited, 0)                                    # and a turn's actions still go at once

    def test_the_world_lane_leaves_the_shared_limit_alone(self):
        self.b.pace([K.act("B", "a", 1, 1, 3)] * C.CALL_LIMIT, "battle")
        steps, waited = self.b.pace([K.user()], "world")
        self.assertGreater(waited, 0)

    def test_no_world_call_has_room_while_a_fight_is_on(self):
        self.assertEqual(self.b.headroom(), C.WORLD_CAP)
        self.rig.world["battle"] = {"bid": "B1", "entries": []}
        self.assertEqual(self.b.headroom(), 0)

    def test_his_turn_is_polled_with_room_left_for_my_turn(self):
        self.assertEqual(self.b.poll_hold(2, 3.0), 3.0)
        self.b.pace([K.battle("B")] * (C.CALL_LIMIT - B.TURN_RESERVE), "battle")
        self.assertEqual(self.b.poll_hold(2, 3.0), B.BLIND_MAX)        # the reserve holds a poll back, but not for long
        self.assertEqual(self.rig.events("finding"), [])
        self.b.pace([K.act("B", "a", 1, 1, 3)] * 3, "battle")          # only a turn's actions are left in the minute
        self.assertGreater(self.b.poll_hold(2, 3.0), 50)               # no poll takes those
        self.assertEqual(self.rig.events("finding")[-1]["about"], "budget")   # the long blind wait is on record

    def test_waits_inside_a_batch_count(self):
        steps, _ = self.b.pace([K.user(), K.wait(30), K.user()], "world")
        times = sorted(c[0] for c in self.rig.world["budget"]["calls"])
        self.assertGreaterEqual(times[1] - times[0], 30)

    def test_a_batch_the_brain_holds_is_counted_from_when_the_relay_gets_it(self):
        self.b.pace([K.user()], "world", start=self.rig.t + 8)
        self.assertGreaterEqual(self.rig.world["budget"]["calls"][0][0], self.rig.t + 8)

    def test_a_restart_remembers_the_last_minute(self):
        self.b.pace([K.user()] * 7, "world")
        self.rig.world.save()
        self.assertEqual(self.rig.new_brain().budget.used(), 7)


class TurnClock(unittest.TestCase):
    def setUp(self):
        self.rig = Rig()
        self.rig.tick(user())
        self.w = self.rig.world

    def test_the_clock_starts_once_per_turn(self):
        state = {}
        turn = B.turn_open(state, 3, 100.0, unseen=4.5)
        self.assertIs(B.turn_open(state, 3, 105.0), turn)
        self.assertEqual((turn["T"], turn["unseen"]), (100.0, 4.5))
        self.assertEqual(B.turn_open(state, 4, 130.0)["T"], 130.0)

    def test_the_planner_is_cut_off_at_t_plus_15_and_a_read_is_not_awaited_past_t_plus_12(self):
        turn = B.turn_open({}, 3, 100.0)
        self.assertEqual(B.planner_seconds(turn, 104.0), C.BEST_LINE_AT - 4.0)
        self.assertFalse(B.read_is_overdue(turn, 111.9))
        self.assertTrue(B.read_is_overdue(turn, 112.0))

    def test_every_turn_is_logged_and_a_slow_fire_is_a_finding(self):
        turn = B.turn_open({}, 3, self.rig.t)
        self.rig.t += 25                                               # past the 20 s rule
        B.turn_fired(self.w, "B1", turn, "1.0s stub", 2)
        B.turn_closed(self.w, "B1", turn, "acted")
        B.turn_closed(self.w, "B1", turn, "acted")                     # logged once
        with open(os.path.join(self.rig.dir, "turns.jsonl")) as f:
            rows = [json.loads(line) for line in f]
        self.assertEqual([(r["round"], r["fired_after"], r["outcome"]) for r in rows], [(3, 25.0, "acted")])
        self.assertEqual([e["about"] for e in self.rig.events("finding")], ["turn"])

    def test_a_turn_fired_close_to_the_limit_is_a_finding(self):
        turn = B.turn_open({}, 5, self.rig.t)
        self.rig.t += C.LATE_TURN + 1
        B.turn_fired(self.w, "B1", turn, "slow", 1)
        B.turn_closed(self.w, "B1", turn, "acted")
        self.assertEqual(len(self.rig.events("finding")), 2)           # over the 20 s rule, and near the limit

    def test_a_missed_turn_is_counted_and_raised(self):
        turn = B.turn_open({}, 2, self.rig.t)
        B.turn_closed(self.w, "B1", turn, "missed")
        self.assertEqual(self.w["records"]["turns_missed"], 1)
        self.assertEqual([e["about"] for e in self.rig.events("stall")], ["missed_turn"])

    def test_a_turn_ends_as_the_evidence_says(self):
        turn = B.turn_open({}, 2, 100.0)
        self.assertEqual(B.turn_outcome(turn, logged=False), "missed")           # nothing sent, nothing in the log
        self.assertEqual(B.turn_outcome(turn, logged=True), "acted")             # the log shows my action
        self.assertEqual(B.turn_outcome(turn, logged=False, ended=True), "unresolved")
        turn.update(sent=2, answered=0)
        self.assertEqual(B.turn_outcome(turn, logged=False), "unresolved")       # sent, and no answer came back
        turn.update(answered=2)
        self.assertEqual(B.turn_outcome(turn, logged=False), "missed")           # every answer was a refusal
        turn.update(unknown=1)
        self.assertEqual(B.turn_outcome(turn, logged=False), "unresolved")       # an answer was an error
        turn.update(accepted=1)
        self.assertEqual(B.turn_outcome(turn, logged=False), "acted")            # the game took one

    def test_an_unresolved_turn_is_counted_apart_and_is_a_finding(self):
        turn = B.turn_open({}, 2, self.rig.t, unseen=C.FIRE_BY + 5)
        B.turn_closed(self.w, "B1", turn, "unresolved")
        self.assertEqual((self.w["records"]["turns_missed"], self.w["records"]["turns_unresolved"]), (0, 1))
        self.assertEqual(len(self.rig.events("finding")), 2)           # no proof of an action; and seen late
        with open(os.path.join(self.rig.dir, "turns.jsonl")) as f:
            self.assertEqual(json.loads(f.readline())["unseen"], C.FIRE_BY + 5)

    def test_when_a_plan_is_owed_with_no_read_in_hand(self):
        turn = B.turn_open({}, 2, 100.0)
        self.assertFalse(B.turn_owed(turn, False, 105.0))              # nothing sent yet: the read is waited for
        self.assertTrue(B.turn_owed(turn, True, 105.0))                # unless the connector refused it
        self.assertTrue(B.turn_owed(turn, False, 100.0 + C.LAST_GOOD_READ_AT))
        turn.update(sent=2, answered=2)
        self.assertTrue(B.turn_owed(turn, False, 105.0))               # every action came back refused: at once
        turn.update(answered=0)
        self.assertFalse(B.turn_owed(turn, False, 113.0))              # answers still out: one read first
        turn.update(looked=True)
        self.assertTrue(B.turn_owed(turn, False, 113.0))
        turn.update(accepted=1)
        self.assertFalse(B.turn_owed(turn, True, 113.0))               # the game took an action: nothing is owed


if __name__ == "__main__":
    unittest.main()
