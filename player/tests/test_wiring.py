"""Everything is wired in (director, 2026-11-11: "Every time we add a new system I discover you weren't using it
because it wasnt tied in").

The test fails when a module under player/activities/ is not registered, when a registered activity is never chosen
by the brain in a played-through session, or when a registered model or data feed leaves no trace in that session.
A new activity, model or feed must be added to the session below, or this fails.
"""
import importlib.util
import os
import pkgutil
import unittest

import player.activities
from player import config as C
from player.tests.support import FOE, Rig, battle_read, fixture, log_read, res, scan, user

PREY = (FOE, "AngelSaberTwin", 13, 14, "AWAKE", 100, "y", None, None)


def session():
    """One played-through session that touches everything: start, wake, a trip, a scan, a heal, an attack, a
    fight with the exact state, its end, the result. Returns (rig, the activities chosen, the calls sent)."""
    rig = Rig(mode="guard")
    chosen, calls = [], []

    def tick(*results, **kw):
        out = rig.tick(*results, **kw)
        chosen.append(out["activity"])
        calls.extend(rig.calls(out))
        return out

    tick()                                                             # watch: the first read
    rig.world["control"]["mode"] = "hunt"
    tick(user("ASLEEP"))                                               # session: wake
    tick(user("TRAVEL"))                                               # travel: land the trip
    tick(user(hp=3000))                                                # recovery: Full Potion
    tick(user())                                                       # pvp_hunt: scan, with the harvest riding
    tick(user(), res("profile.getStrongestUsers", {"*.userId": ["user_top"], "*.username": ["Top"]}), dt=10)
    tick(user(), scan([PREY]))                                         # pvp_hunt: his kit, then the attack
    tick(res("jutsu.getPublicUserJutsus", {"*.jutsuId": ["j1"], "*.level": [25], "*.equipped": [True]},
             {"userId": FOE}), user("BATTLE", bid="W1"))               # battle: the opening read
    battle, ents = fixture()
    live = dict(battle, **{"battle.usersEffects": [{"type": "increasedamagegiven", "targetId": C.ME}]})
    tick(battle_read("W1", live), log_read("W1", ents))                # battle: my turn, planned on the live state
    for _ in range(4):
        out = tick(battle_read("W1", {}))                              # the battle is gone: the fight closes
        if "BATTLE OVER" in out["note"]:
            break
    tick(user())                                                       # the result is settled
    return rig, chosen, calls


class Wiring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rig, cls.chosen, cls.calls = session()
        cls.reg = cls.rig.brain.reg

    def test_every_module_under_activities_registers_one_activity(self):
        modules = {m.name for m in pkgutil.iter_modules(player.activities.__path__)}
        self.assertEqual(modules, set(self.reg.activities))
        for name, act in self.reg.activities.items():
            self.assertEqual(type(act).__module__, f"player.activities.{name}")

    def test_every_activity_is_chosen_in_a_session(self):
        riders = {n for n, a in self.reg.activities.items() if a.rides}
        for name in self.reg.activities:
            if name in riders:
                continue
            self.assertIn(name, self.chosen, f"{name} is registered but the brain never chose it")
        self.assertEqual(riders, {"harvest"})
        self.assertIn("profile.getStrongestUsers", self.calls)         # the rider's read went out
        self.assertIn("combat.getBattleHistory", self.calls)           # and its answer set up the next one

    def test_every_model_and_feed_leaves_a_trace(self):
        c, fights = self.rig.combat, self.rig.combat.fights
        spawned = " ".join(" ".join(a) for a in c.spawned)
        evidence = {
            "planner": c.used.get("planner", 0) > 0 and c.plan_args[-1]["live"],
            "dossier": c.saved == [FOE],
            "opponents": "opponents.py build" in spawned,
            "postmortem": "postmortem.py" in spawned,
            "fight_bases": c.used.get("fight_bases", 0) > 0 and "fight_bases.py W1" in spawned,
            "live_state": os.path.exists(os.path.join(fights, "live_states", "W1.json")),
            "fight_log": os.path.exists(os.path.join(fights, "W1_entries.json")),
            "harvest": "players" in self.rig.world.own("harvest").get("stats", ""),
        }
        self.assertEqual(set(evidence), set(self.reg.models) | set(self.reg.feeds),
                         "a model or feed is registered with no check here (or checked and not registered)")
        self.assertEqual([k for k, ok in evidence.items() if not ok], [])

    def test_the_session_played_out(self):
        self.assertEqual(self.rig.events("fight_start")[0]["battle"], "W1")
        self.assertEqual(self.rig.events("fight_end")[0]["result"], "won")
        self.assertEqual(self.calls.count("item.consume"), 2)          # the heal before, and the one at the fight's end
        self.assertEqual(self.rig.world["records"]["turns_missed"], 0)

    def test_every_call_the_code_can_send_is_on_the_approved_list(self):
        spec = importlib.util.spec_from_file_location("pa", os.path.join(C.ROOT, "scripts", "player_allowlist.py"))
        pa = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pa)
        self.assertIn(os.path.join(C.ROOT, "player"), pa.CODE_DIRS)
        errs, _ = pa.check(pa._load(pa.ALLOWLIST), pa._load(pa.SURFACE), [os.path.join(C.ROOT, "player")])
        self.assertEqual(errs, [])
        listed = pa._load(pa.ALLOWLIST)["endpoints"]
        for ep in set(self.calls):
            self.assertIn(ep, listed)


if __name__ == "__main__":
    unittest.main()
