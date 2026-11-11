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

    def test_battle_and_recovery_are_never_delayed(self):
        self.b.pace([K.user()] * C.WORLD_CAP, "world")
        for lane in ("battle", "recovery"):
            steps, waited = self.b.pace([K.act("B", "a", 1, 1, 3)] * 6, lane)
            self.assertEqual((len(steps), waited), (6, 0), lane)
        self.assertEqual(self.b.used(), C.WORLD_CAP + 12)

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
        self.assertGreater(self.b.poll_hold(2, 3.0), 50)               # the minute is full but for my turn's share

    def test_waits_inside_a_batch_count(self):
        steps, _ = self.b.pace([K.user(), K.wait(30), K.user()], "world")
        times = sorted(t for t, _ in self.rig.world["budget"]["calls"])
        self.assertGreater(times[1] - times[0], 30)

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
        turn = B.turn_open(state, 3, 100.0)
        self.assertIs(B.turn_open(state, 3, 105.0), turn)
        self.assertEqual(turn["T"], 100.0)
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
        B.turn_closed(self.w, "B1", turn, acted=True)
        B.turn_closed(self.w, "B1", turn, acted=True)                  # logged once
        with open(os.path.join(self.rig.dir, "turns.jsonl")) as f:
            rows = [json.loads(line) for line in f]
        self.assertEqual([(r["round"], r["fired_after"], r["acted"]) for r in rows], [(3, 25.0, True)])
        self.assertEqual([e["about"] for e in self.rig.events("finding")], ["turn"])

    def test_a_turn_fired_close_to_the_limit_is_a_finding(self):
        turn = B.turn_open({}, 5, self.rig.t)
        self.rig.t += C.LATE_TURN + 1
        B.turn_fired(self.w, "B1", turn, "slow", 1)
        B.turn_closed(self.w, "B1", turn, acted=True)
        self.assertEqual(len(self.rig.events("finding")), 2)           # over the 20 s rule, and near the limit

    def test_a_missed_turn_is_counted_and_raised(self):
        turn = B.turn_open({}, 2, self.rig.t)
        B.turn_closed(self.w, "B1", turn, acted=False)
        self.assertEqual(self.w["records"]["turns_missed"], 1)
        self.assertEqual([e["about"] for e in self.rig.events("stall")], ["missed_turn"])


if __name__ == "__main__":
    unittest.main()
