"""The world model: one store, saved after every result, reloaded by a brain that restarts."""
import json
import os
import unittest

from player.world import World
from player.tests.support import Rig, user


class WorldModel(unittest.TestCase):
    def test_a_result_updates_the_model_and_the_file(self):
        rig = Rig()
        rig.tick(user(hp=4000, sector=99))
        self.assertEqual((rig.world.me["curHealth"], rig.world.me["sector"]), (4000, 99))
        with open(os.path.join(rig.dir, "world.json")) as f:
            self.assertEqual(json.load(f)["character"]["curHealth"], 4000)

    def test_a_restart_reloads_everything(self):
        rig = Rig()
        rig.tick(user(hp=4000))
        rig.world["opponents"]["lost_to"]["user_x"] = rig.t + 100
        rig.world.save()
        again = World(rig.dir, clock=lambda: rig.t)
        self.assertEqual(again.me["curHealth"], 4000)
        self.assertIn("user_x", again["opponents"]["lost_to"])
        self.assertEqual(again["control"]["mode"], "hunt")

    def test_only_known_sections_exist(self):
        rig = Rig()
        with self.assertRaises(KeyError):
            rig.world["scratch"] = 1
        with open(os.path.join(rig.dir, "world.json"), "w") as f:
            json.dump({"character": {"status": "AWAKE"}, "made_up": {"x": 1}}, f)
        self.assertNotIn("made_up", World(rig.dir).d)

    def test_spend_is_measured_from_the_profile_not_estimated(self):
        rig = Rig()
        rig.tick(user(money=2_000_000, bank=50_000_000))
        rig.tick(user(money=1_950_000, bank=50_000_000))            # 50,000 spent
        rig.tick(user(money=950_000, bank=51_000_000))              # a deposit: nothing spent
        rig.tick(user(money=1_000_000, bank=51_000_000))            # income: nothing spent
        self.assertEqual(rig.world.spent_today(), 50_000)
        rig.t += 86_400
        self.assertEqual(rig.world.spent_today(), 0)

    def test_a_decision_is_raised_once_and_is_an_event(self):
        rig = Rig()
        self.assertTrue(rig.world.decide("k", "buy the thing?"))
        self.assertFalse(rig.world.decide("k", "buy the thing?"))
        self.assertEqual(len(rig.events("decision_raised")), 1)
        self.assertIsNone(rig.world.answered("k"))

    def test_an_event_has_a_known_kind(self):
        rig = Rig()
        with self.assertRaises(ValueError):
            rig.world.event("gossip", "x")
        rig.world.event("error", "boom")
        self.assertEqual(rig.world["records"]["last_error"]["text"], "boom")


if __name__ == "__main__":
    unittest.main()
