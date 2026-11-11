"""The arbiter, the director's settings (live/control.json), the status file and the watchdog."""
import os
import unittest

from player import config as C
from player import console
from player.registry import Activity, plan
from player.tests.support import Rig, scan, user

PREY = ("u_p", "Prey", 13, 14, "AWAKE", 100, "y", None, None)


class Fake(Activity):
    def __init__(self, name, priority, value, goal=None):
        self.name, self.priority, self._value, self.goal = name, priority, value, goal

    def available(self, world):
        return True

    def value(self, world):
        return self._value

    def plan(self, world):
        return plan([], "world", self.name, hold=1.0)


class Arbiter(unittest.TestCase):
    def test_a_higher_class_always_wins(self):
        rig = Rig()
        self.assertEqual(rig.tick(user("HOSPITALIZED"))["activity"], "recovery")       # safety over goals
        self.assertEqual(rig.tick(user("BATTLE", bid="B1"))["activity"], "battle")     # a fight over everything
        self.assertEqual(rig.tick(user("TRAVEL"))["activity"], "battle")               # even over a trip's status
        order = [a.name for a in rig.brain.rank()]
        self.assertEqual(order[0], "battle")

    def test_within_a_class_value_times_the_goals_weight_decides(self):
        rig = Rig()
        rig.tick(user())
        acts = rig.brain.reg.activities
        acts["a_missions"], acts["a_farm"] = Fake("a_missions", "goals", 30, "daily_caps"), Fake("a_farm", "goals", 30, "ryo")
        try:
            names = [a.name for a in rig.brain.rank()]
            self.assertLess(names.index("a_missions"), names.index("a_farm"))          # 0.7 beats 0.45 at equal value
            self.assertLess(names.index("a_missions"), names.index("pvp_hunt"))        # 30 x 0.7 beats 10 x 1.0
            rig.world["control"]["goal_weights"] = {"ryo": 0.9}                        # the director re-weights
            names = [a.name for a in rig.brain.rank()]
            self.assertLess(names.index("a_farm"), names.index("a_missions"))
        finally:
            del acts["a_missions"], acts["a_farm"]

    def test_the_gates_block_an_activity_and_the_brain_does_something_else(self):
        """The hunt's own filter is the first lock and the gate the second. Here the hunt is given an empty list,
        so only the gate stands between it and a player on do_not_attack.md."""
        friend = ("u_f", "Friend", 13, 14, "AWAKE", 100, "y", None, None)
        rig = Rig()
        hunt = rig.brain.reg.activities["pvp_hunt"]
        hunt.gates = type("NoList", (), {"dna_path": os.devnull})()
        try:
            out = rig.tick(user(), scan([friend]))
            self.assertEqual(out["activity"], "watch")                                 # the attack was refused
            self.assertNotIn("combat.attackUser", rig.calls(out))
            self.assertEqual([e["rule"] for e in rig.events("finding")], ["do_not_attack"])
            self.assertEqual(rig.tick(user(), scan([friend]))["activity"], "watch")    # and it is not tried round
            self.assertEqual(len(rig.events("finding")), 1)
        finally:
            hunt.gates = rig.brain.gates
        self.assertEqual(rig.tick(user(), dt=61)["activity"], "pvp_hunt")

    def test_nothing_to_do_holds_in_the_brain(self):
        rig = Rig()
        rig.tick(user())
        rig.world["control"]["paused"] = True
        out = rig.tick(user())
        self.assertEqual((out["steps"], out["hold"], out["note"]), ([], 30.0, "paused"))


class Settings(unittest.TestCase):
    def test_a_new_version_is_applied_and_every_change_is_an_event(self):
        rig = Rig(mode="guard")
        rig.tick(user())
        console.set_control(rig.dir, mode="hunt", director_mode=True, spend_caps={"daily": 1_000_000})
        out = rig.tick(user())
        self.assertEqual(out["activity"], "pvp_hunt")
        self.assertEqual({e["setting"] for e in rig.events("setting_changed")}, {"mode", "director_mode", "spend_caps"})
        self.assertEqual(rig.status()["control_version"], 1)
        rig.tick(user())
        self.assertEqual(len(rig.events("setting_changed")), 3)                        # the same version is not re-applied

    def test_a_setting_cannot_widen_what_the_gates_allow(self):
        rig = Rig()
        rig.tick(user())
        rig.world["control"]["do_not_attack"] = ["Luka"]
        console.set_control(rig.dir, mode="farm", activities={"battle": False, "raids": True}, do_not_attack=[],
                            allowlist=["stripe.createCheckout"], goal_weights={"pvp": -1}, paused="yes")
        rig.tick(user())
        errors = " | ".join(e["text"] for e in rig.events("error"))
        for why in ("mode", "activities", "do_not_attack", "allowlist: not a setting", "goal_weights", "paused"):
            self.assertIn(why, errors)
        ctl = rig.world["control"]
        self.assertEqual((ctl["mode"], ctl["do_not_attack"], ctl["activities"], ctl["paused"]),
                         ("hunt", ["Luka"], {}, False))
        self.assertEqual(rig.events("setting_changed"), [])

    def test_pause_stops_the_world_but_never_a_fight(self):
        rig = Rig()
        rig.tick(user())
        console.set_control(rig.dir, paused=True)
        self.assertEqual(rig.tick(user(), scan([PREY]))["activity"], None)
        rig.world["battle"] = {"bid": "B1", "entries": []}
        self.assertEqual(rig.tick()["activity"], "battle")
        rig.world["battle"] = None
        console.set_control(rig.dir, paused=False)
        self.assertEqual(rig.tick(user())["activity"], "pvp_hunt")

    def test_the_director_answers_a_pending_decision(self):
        rig = Rig()
        rig.tick(user())
        rig.world.decide("k1", "buy the skill?")
        did = rig.world["decisions"][0]["id"]
        console.set_control(rig.dir, answers={did: "yes"})
        rig.tick(user())
        self.assertEqual(rig.world.answered("k1"), "yes")
        self.assertEqual([e["answer"] for e in rig.events("decision_answered")], ["yes"])
        self.assertEqual(rig.status()["decisions_pending"], [])

    def test_end_the_session_now_waits_for_the_fight_to_finish(self):
        rig = Rig()
        rig.tick(user())
        console.set_control(rig.dir, end_session=True)
        rig.world["battle"] = {"bid": "B1", "entries": []}
        self.assertIsNone(rig.tick()["stop"])
        rig.world["battle"] = None
        self.assertEqual(rig.tick(user())["stop"], "session ended by the director")


class Handover(unittest.TestCase):
    def test_the_first_start_carries_on_from_the_pilots_state(self):
        import json
        from player.tests.support import StubCombat
        rig = Rig()
        fights = os.path.join(rig.dir, "fights2")
        os.makedirs(os.path.join(fights, "live"))
        with open(os.path.join(fights, "live", "pilot.json"), "w") as f:
            json.dump({"full_potion_uid": "uid_now", "lost_to": {"u_p": rig.t + 3600}, "mode": "hunt"}, f)
        os.unlink(os.path.join(rig.dir, "world.json")) if os.path.exists(os.path.join(rig.dir, "world.json")) else None
        rig.combat = StubCombat(fights)
        rig.new_brain()
        rig.world["control"]["mode"] = "hunt"
        out = rig.tick(user(hp=3000))
        self.assertEqual(out["steps"][0]["input"], {"userItemId": "uid_now"})
        self.assertNotIn("combat.attackUser", rig.calls(rig.tick(user(), scan([PREY]))))   # he beat me an hour ago
        rig.world["inventory"]["full_potion_uid"] = "uid_later"
        rig.world.save()
        self.assertEqual(rig.new_brain().world["inventory"]["full_potion_uid"], "uid_later")   # taken over once only

    def test_a_setting_from_the_command_line(self):
        from player import brain
        self.assertEqual(brain._setting("mode=hunt"), ("mode", "hunt"))
        self.assertEqual(brain._setting("paused=true"), ("paused", True))
        self.assertEqual(brain._setting('activities={"harvest": false}'), ("activities", {"harvest": False}))


class Status(unittest.TestCase):
    def test_the_status_file_says_what_the_player_is_doing_and_why(self):
        rig = Rig()
        rig.tick(user(hp=4000, sector=1490))
        s = rig.status()
        self.assertEqual(s["schema"], 1)
        self.assertEqual((s["mode"], s["activity"]["name"]), ("hunt", "recovery"))
        self.assertIn("Full Potion", s["activity"]["why"])
        self.assertEqual([q["name"] for q in s["queue"]][:1], ["pvp_hunt"])
        self.assertLessEqual(len(s["queue"]), 5)
        self.assertEqual((s["character"]["hp"], s["character"]["sector"]), (4000, 1490))
        for key in ("battle", "relay", "budget", "tokens", "decisions_pending", "turns_missed", "last_error"):
            self.assertIn(key, s)
        self.assertEqual(s["budget"]["limit"], C.CALL_LIMIT)
        self.assertTrue(s["relay"]["healthy"])

    def test_an_activity_that_ends_is_an_event(self):
        rig = Rig()
        rig.tick(user("HOSPITALIZED"))
        rig.tick(user())
        self.assertEqual([e["activity"] for e in rig.events("activity_done")], ["recovery"])


class Watchdog(unittest.TestCase):
    def test_a_relay_that_does_not_come_back_is_a_stall_raised_once(self):
        rig = Rig()
        out = rig.tick(user())                                             # a scan: held 8 s, then two calls
        self.assertFalse(rig.brain.watchdog())
        rig.t += out["hold"] + 15                                          # inside the batch's own time + 10 s
        self.assertFalse(rig.brain.watchdog())
        rig.t += 10
        self.assertTrue(rig.brain.watchdog())
        self.assertFalse(rig.brain.watchdog())                             # once
        self.assertEqual([e["about"] for e in rig.events("stall")], ["relay"])
        self.assertFalse(rig.status()["relay"]["healthy"])
        rig.tick(user())                                                   # the relay is back
        self.assertTrue(rig.status()["relay"]["healthy"])

    def test_a_relay_told_to_stop_is_not_a_stall(self):
        rig = Rig(mode="guard")
        rig.tick(user("ASLEEP"))
        rig.t += 600
        self.assertFalse(rig.brain.watchdog())


if __name__ == "__main__":
    unittest.main()
