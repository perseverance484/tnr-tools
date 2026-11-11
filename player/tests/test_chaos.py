"""Chaos (brief AP1 step 7; design section 6): refusals, "Too Many Requests", a relay that restarts mid-battle, a
battle that starts in the middle of something else, a brain that restarts, a planner that runs out of time, the
Full Potion at the fight's end, and the deadline fallback. In every one of them a turn of mine still gets an
action."""
import json
import os
import tempfile
import time
import unittest

from player import budget as B
from player import config as C
from player.combat import Combat
from player.tests.support import (FOE, Ledger, Rig, battle_read, fixture, limited, log_read, res, scan, start_fight,
                                  user)

PREY = ("u_p", "Prey", 13, 14, "AWAKE", 100, "y", None, None)


def acts(out):
    return [s["input"]["actionId"] for s in out["steps"] if s.get("call") == "combat.performAction"]


class Refusals(unittest.TestCase):
    def test_every_action_refused_one_by_one_still_ends_in_an_action(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        for aid in ("stormblade_id", "kunai_id"):
            bad = res("combat.performAction", {"notification": "Action not valid anymore"},
                      {"battleId": "B1", "actionId": aid})
            out = rig.tick(bad, battle_read("B1", battle))
            self.assertTrue(acts(out), "a turn of mine with no action")
        self.assertEqual(acts(out), ["defensiveStance"])                   # everything banned: the stance, not nothing

    def test_a_call_that_errors_is_an_event_and_the_loop_goes_on(self):
        rig = Rig()
        rig.tick(user())
        out = rig.tick(res("travel.getSectorData", None, {"sector": 1538}, error="Error calling travel.getSectorData: boom"),
                       user())
        self.assertEqual(out["activity"], "pvp_hunt")
        self.assertEqual([e["about"] for e in rig.events("error")], ["call"])


class TooManyRequests(unittest.TestCase):
    def test_on_my_turn_the_plan_comes_from_the_last_good_read_at_once(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(limited("combat.performAction", {"battleId": "B1", "actionId": "stormblade_id"}),
                       limited("combat.performAction", {"battleId": "B1", "actionId": "kunai_id"}),
                       limited("combat.getBattle", {"battleId": "B1"}))
        self.assertEqual(acts(out), ["stormblade_id", "kunai_id"])
        self.assertEqual(out["hold"], 0)
        self.assertEqual(out["steps"][0]["call"], "combat.performAction")
        self.assertEqual([k for s in out["steps"][:1] for k in s if k == "wait"], [])

    def test_on_his_turn_the_poll_backs_off_and_the_fight_is_not_called_over(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.tick(battle_read("B1", dict(battle, **{"battle.activeUserId": FOE})))
        out = rig.tick(limited("combat.getBattle", {"battleId": "B1"}))
        self.assertTrue(rig.world.in_battle())
        self.assertEqual(rig.calls(out), ["combat.getBattle", "combat.getBattleEntries"])
        self.assertEqual(out["hold"], C.RATE_BACKOFF)

    def test_the_opening_read_refused_is_asked_again_in_full(self):
        rig = Rig()
        rig.tick(user("BATTLE", bid="B1"))
        out = rig.tick(limited("combat.getBattle", {"battleId": "B1"}))
        self.assertEqual([s["input"] for s in out["steps"]], [{"battleId": "B1"}, {"battleId": "B1", "limit": 200}])
        self.assertIn("battle.usersEffects", out["steps"][0]["select"])
        self.assertEqual(out["hold"], C.RATE_BACKOFF)

    def test_the_whole_fight_stays_under_the_limit(self):
        rig = Rig()
        ledger = Ledger(rig)
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE})
        for _ in range(40):                                                # a long turn of his, a relay with no lag
            out = rig.tick(battle_read("B1", his), dt=out["hold"] + 0.5)
            self.assertLessEqual(out["hold"], B.BLIND_MAX)                 # his turn is never left unread for long
        self.assertLessEqual(ledger.worst(), C.CALL_LIMIT - B.TURN_ACTIONS)   # and room is kept for my turn


class RelayRestart(unittest.TestCase):
    def test_a_new_relay_mid_battle_picks_the_fight_up(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)                               # my turn's batch went to a relay that died
        self.assertTrue(rig.brain.watchdog() is False)
        rig.t += 60
        self.assertTrue(rig.brain.watchdog())                              # the stall is raised, and says so
        self.assertIn("in a fight", rig.events("stall")[-1]["text"])
        out = rig.tick()                                                   # a fresh relay: no results to hand in
        self.assertIsNone(out["stop"])
        self.assertEqual((out["activity"], rig.calls(out), out["hold"]),
                         ("battle", ["combat.getBattle", "combat.getBattleEntries"], 0))
        moved = dict(battle, **{"battle.version": battle["battle.version"] + 2, "battle.activeUserId": FOE})
        self.assertIn("his turn", rig.tick(battle_read("B1", moved))["note"])

    def test_a_relay_is_never_rotated_in_a_fight(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.world["relay"].update(baseline_tokens=10_000, context_tokens=10_000 + C.ROTATE_AFTER_TOKENS * 2)
        self.assertIsNone(rig.tick(battle_read("B1", battle))["stop"])


class BattleInTheMiddleOfSomethingElse(unittest.TestCase):
    def test_an_attack_lands_while_the_hunt_is_scanning(self):
        rig = Rig()
        rig.tick(user())
        out = rig.tick(user("BATTLE", bid="B7"), scan([PREY]))             # the scan's own read shows the fight
        self.assertEqual(out["activity"], "battle")
        self.assertEqual(out["hold"], 0)
        self.assertNotIn("combat.attackUser", rig.calls(out))
        self.assertNotIn("profile.getStrongestUsers", rig.calls(out))      # nothing rides a fight's batch

    def test_an_attack_lands_during_a_trip_or_a_heal(self):
        for status in ("TRAVEL", "HOSPITALIZED"):
            rig = Rig()
            rig.tick(user(status))
            out = rig.tick(user("BATTLE", bid="B8", hp=2000))
            self.assertEqual((out["activity"], out["hold"]), ("battle", 0), status)

    def test_world_calls_issued_just_before_do_not_slow_the_fight(self):
        rig = Rig()
        rig.world["budget"]["calls"] = [[rig.t, "world"]] * C.WORLD_CAP    # the world lane has used all it may
        out = rig.tick(user("BATTLE", bid="B9"))
        self.assertEqual([k for s in out["steps"] for k in s if k == "wait"], [])
        battle, ents = fixture()
        out = rig.tick(battle_read("B9", dict(battle, **{"battle.usersEffects": []})), log_read("B9", ents))
        self.assertEqual(out["steps"][0]["call"], "combat.performAction")
        self.assertEqual(out["hold"], 0)


class BrainRestart(unittest.TestCase):
    def test_a_brain_restarted_mid_battle_gives_the_same_batch(self):
        battle, ents = fixture()
        his = dict(battle, **{"battle.activeUserId": FOE})
        outs = []
        for restart in (False, True):
            rig = Rig()
            start_fight(rig)
            rig.tick(battle_read("B1", his))
            if restart:
                rig.new_brain()                                            # everything it knows is in world.json
            out = rig.tick(battle_read("B1", dict(battle, **{"battle.version": battle["battle.version"] + 3})))
            outs.append((out["note"], json.dumps(out["steps"], sort_keys=True), out["hold"]))
        self.assertEqual(outs[0], outs[1])
        self.assertIn("MY TURN", outs[0][0])

    def test_a_brain_restarted_between_the_plan_and_its_results_does_not_fire_twice(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        rig.new_brain()
        ok = res("combat.performAction", {}, {"battleId": "B1", "actionId": "stormblade_id"})
        after = dict(battle, **{"battle.version": battle["battle.version"] + 2, "battle.activeUserId": FOE})
        out = rig.tick(ok, battle_read("B1", after))
        self.assertEqual(acts(out), [])
        self.assertEqual(rig.world["records"]["turns_missed"], 0)

    def test_a_restart_keeps_settings_decisions_and_cooldowns(self):
        rig = Rig()
        rig.tick(user())
        rig.world["opponents"]["lost_to"]["u_p"] = rig.t + 3600
        rig.world.decide("k", "buy?")
        rig.world.save()
        rig.new_brain()
        out = rig.tick(user(), scan([PREY]))
        self.assertNotIn("combat.attackUser", rig.calls(out))
        self.assertEqual(len(rig.status()["decisions_pending"]), 1)
        self.assertEqual(rig.status()["mode"], "hunt")


class BrainCrash(unittest.TestCase):
    def test_a_tick_that_crashes_still_answers_the_relay_and_is_written_down(self):
        from player import brain, relay
        rig = Rig()
        rig.brain.handle = lambda results, usage=None, strays=0: 1 / 0
        req = relay.request_path(rig.dir, 5)
        relay.write(req, {"seq": 5, "results": [], "usage": {}})
        brain.answer(rig.brain, rig.dir, req)
        batch = relay.read(relay.batch_path(rig.dir, 5))
        self.assertEqual((batch["steps"], batch["stop"]), ([], None))       # come back; never a dead end
        self.assertTrue(relay.lines(batch["steps"], batch["stop"], "ab12cd-5")[0].endswith('brain next ab12cd-5"}'))
        self.assertFalse(os.path.exists(req))
        with open(os.path.join(rig.dir, "crash.log")) as f:
            self.assertIn("ZeroDivisionError", f.read())
        self.assertEqual([e["about"] for e in rig.events("error")], ["crash"])


class PlannerOutOfTime(unittest.TestCase):
    def test_a_tick_that_arrives_late_in_the_turn_fires_the_stance(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(battle_read("B1", dict(battle, **{"battle.usersEffects": []})), dt=C.BEST_LINE_AT)
        self.assertEqual(acts(out), ["defensiveStance"])                   # T+15 s: no time to plan, never nothing
        self.assertLess(rig.combat.plan_args[-1]["seconds"], 0.5)

    def test_the_real_planner_is_cut_off_and_returns(self):
        battle, ents = fixture()
        rows = [list(x) for x in zip(*(ents[k] for k in ("*.id", "*.battleRound", "*.userId", "*.actionId",
                                                         "*.appliedEffects.*.txt")))][::-1]
        combat = Combat(tempfile.mkdtemp(), spawn=False)
        t0 = time.time()
        line, how = combat.plan_turn("CUT", dict(battle), rows, "AngelSaber", seconds=0.6)
        self.assertIsNone(line)
        self.assertIn("planner failed", how)
        self.assertLess(time.time() - t0, 3.0)
        self.assertEqual(combat.plan_turn("CUT", dict(battle), rows, "AngelSaber", seconds=0.2),
                         (None, "planner failed: out of time"))


class FullPotionAtTheEnd(unittest.TestCase):
    def test_the_potion_and_the_last_read_are_one_batch_even_in_a_minute_the_fight_has_filled(self):
        rig = Rig()
        start_fight(rig)
        rig.world["budget"]["calls"] = [[rig.t, "battle"]] * (C.CALL_LIMIT - B.TURN_ACTIONS - 4)   # a busy fight
        for _ in range(4):
            out = rig.tick(battle_read("B1", {}))
            if "BATTLE OVER" in out["note"]:
                break
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])
        self.assertEqual(([k for s in out["steps"] for k in s if k == "wait"], out["hold"]), ([], 0))


class DeadlineFallback(unittest.TestCase):
    def test_a_read_that_never_comes_back_is_not_waited_for_past_t_plus_12(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        boom = res("combat.getBattle", None, {"battleId": "B1"}, error="Error calling combat.getBattle: boom")
        out = rig.tick(boom, dt=5)
        self.assertEqual(acts(out), [])                                    # T+5 s: read again
        self.assertEqual(rig.calls(out), ["combat.getBattle", "combat.getBattleEntries"])
        out = rig.tick(boom, dt=C.LAST_GOOD_READ_AT - 5)
        self.assertEqual(acts(out), ["stormblade_id", "kunai_id"])         # T+12 s: the last good read, and act
        self.assertIn("last good read", out["note"])
        self.assertLessEqual(rig.combat.plan_args[-1]["seconds"], C.BEST_LINE_AT - C.LAST_GOOD_READ_AT)
        with open(os.path.join(rig.dir, "turns.jsonl")) if os.path.exists(os.path.join(rig.dir, "turns.jsonl")) \
                else open(os.devnull) as f:
            self.assertEqual(f.read(), "")                                 # the turn is logged when it closes, not before


if __name__ == "__main__":
    unittest.main()
