"""The autopilot's switches and the director's rules built into the brain (tnr-autopilot DESIGN.md sections 6 and 9;
"Build all of it", 2026-11-23).

- a brain starts in the dry run, and out of fights against people
- kill stops at once, in a fight too, and at the hook; run off stops; shadow sends nothing; read_only sends reads
- stop is the graceful end: the session's end, after any fight
- in a fight against a person nothing is sent but reads, and the director is pinged once; pvp_turns on plays it
- targets: level 100, or 85-99 rated 60% or better from a public record; hidden or unrated, skipped
- no attack short of full HP, chakra or stamina: the hunt holds and the gate refuses
- stealth is cast when it is off and off cooldown, and is broken by an attack
- after every fight: a repair, and a step off the tile (not at home)
- the circuit: the director's when he names it; never 210
"""
import json
import os
import unittest

from player import config as C, console, gates, hook, world as W
from player.tests import LIVE_DEFAULTS
from player.tests.support import FOE, Rig, battle_read, fixture, log_read, res, scan, user

PREY = ("user_prey", "Prey", 13, 14, "AWAKE", 100, "y", None, None)


def calls(out):
    return [s["call"] for s in out["steps"] if "call" in s]


def fight(rig, ai=False, bid="B1"):
    """A fight opened, and its first read in: my turn, round 3, against AngelSaber (or an AI in his seat)."""
    rig.tick(user("BATTLE", bid=bid))
    battle, ents = fixture()
    if ai:
        battle["battle.usersState.*.isAi"] = [u == FOE for u in battle["battle.usersState.*.userId"]]
    return rig.tick(battle_read(bid, battle), log_read(bid, ents))


class Defaults(unittest.TestCase):
    def test_a_brain_starts_in_the_dry_run_and_out_of_fights_against_people(self):
        self.assertEqual(W.RUN_DEFAULT, "shadow")
        self.assertEqual(LIVE_DEFAULTS, {"run": "shadow", "pvp_turns": False})

    def test_the_level_rule_and_the_circuit(self):
        self.assertEqual((C.MIN_LEVEL, C.RATED_LEVELS, C.RATED_MIN), (100, (85, 99), 0.60))
        self.assertNotIn(210, C.CIRCUIT)
        self.assertEqual(C.CIRCUIT[:3], [1538, 1490, 724])             # the enemy villages first


class Switches(unittest.TestCase):
    def test_kill_stops_at_once_even_in_a_fight(self):
        rig = Rig()
        fight(rig)
        rig.world["control"]["kill"] = True
        out = rig.tick()
        self.assertEqual((out["stop"], out["steps"]), ("killed by the director", []))

    def test_kill_refuses_every_line_at_the_hook(self):
        rig = Rig()
        self.assertIsNone(hook.killed(rig.dir))
        console.set_control(rig.dir, kill=True)
        self.assertIn("killed", hook.killed(rig.dir))

    def test_run_off_stops(self):
        rig = Rig(run="off")
        self.assertEqual(rig.tick(user())["stop"], "run is off")

    def test_shadow_sends_nothing_and_writes_what_it_would_have(self):
        rig = Rig(run="shadow")
        out = rig.tick(user(), scan([PREY]))
        self.assertEqual(calls(out), [])
        with open(os.path.join(rig.dir, "shadow.jsonl"), encoding="utf8") as f:
            rows = [json.loads(x) for x in f]
        self.assertEqual(rows[-1]["activity"], "pvp_hunt")
        self.assertIn("combat.attackUser", [h["call"] for h in rows[-1]["held"]])

    def test_read_only_sends_the_reads_and_holds_the_attack(self):
        rig = Rig(run="read_only")
        out = rig.tick(user(), scan([PREY]))
        self.assertNotIn("combat.attackUser", calls(out))
        self.assertIn("profile.getUser", calls(out))
        with open(os.path.join(rig.dir, "shadow.jsonl"), encoding="utf8") as f:
            held = [h["call"] for x in f for h in json.loads(x)["held"]]
        self.assertIn("combat.attackUser", held)

    def test_stop_is_the_sessions_end(self):
        rig = Rig()
        console.set_control(rig.dir, stop=True)
        rig.tick(user())
        self.assertTrue(rig.world["control"]["end_session"])

    def test_the_settings_are_checked(self):
        rig = Rig()
        console.set_control(rig.dir, run="fast", circuit=[1538, 210], pvp_turns="yes")
        rig.tick(user())
        refused = " ".join(e["text"] for e in rig.events("error"))
        for key in ("run", "circuit", "pvp_turns"):
            self.assertIn(f"setting refused: {key}", refused)
        self.assertEqual(rig.world["control"]["run"], "live")


class HandsOff(unittest.TestCase):
    def test_a_fight_against_a_person_is_only_watched_and_he_is_pinged_once(self):
        rig = Rig(pvp_turns=False)
        out = fight(rig)
        self.assertNotIn("combat.performAction", calls(out))
        self.assertIn("combat.getBattle", calls(out))
        self.assertIn("hands off", out["note"])
        battle, ents = fixture()
        out = rig.tick(battle_read("B1", battle), log_read("B1", ents), dt=5)
        self.assertNotIn("combat.performAction", calls(out))
        self.assertEqual(len(rig.events("ping")), 1)
        self.assertEqual(rig.world["records"]["turns_missed"], 0)       # his turns are not mine to miss

    def test_a_fight_against_ai_only_is_played(self):
        rig = Rig(pvp_turns=False)
        out = fight(rig, ai=True)
        self.assertIn("combat.performAction", calls(out))
        self.assertEqual(rig.events("ping"), [])

    def test_with_pvp_turns_on_his_fight_is_played(self):
        rig = Rig(pvp_turns=True)
        self.assertIn("combat.performAction", calls(fight(rig)))

    def test_the_last_resort_does_not_act_in_his_fight(self):
        rig = Rig(pvp_turns=False)
        fight(rig)
        act = rig.brain.reg.activities["battle"]
        p = act.last_resort(rig.world)
        self.assertNotIn("combat.performAction", [s.get("call") for s in p.steps])


class Targets(unittest.TestCase):
    def rated(self, rig, ratings):
        with open(os.path.join(rig.dir, "rater.json"), "w", encoding="utf8") as f:
            json.dump(ratings, f)

    def test_level_100_only_unless_rated_60_or_better(self):
        rig = Rig()
        low = ("user_low", "Low", 13, 14, "AWAKE", 95, "y", None, None)
        out = rig.tick(user(), scan([low]))
        self.assertNotIn("combat.attackUser", calls(out))
        self.assertEqual(rig.world["map"]["last_scan"].get("lowlvl"), 1)
        self.rated(rig, {"user_low": 0.55})
        self.assertNotIn("combat.attackUser", calls(rig.tick(user(), scan([low]), dt=10)))
        self.rated(rig, {"user_low": 0.61})
        self.assertIn("combat.attackUser", calls(rig.tick(user(), scan([low]), dt=10)))

    def test_under_85_is_never_a_target_whatever_the_rating(self):
        rig = Rig()
        self.rated(rig, {"user_low": 0.99})
        self.assertFalse(gates.level_ok(84, "user_low", rig.world))
        self.assertTrue(gates.level_ok(85, "user_low", rig.world))
        self.assertTrue(gates.level_ok(100, "user_unrated", rig.world))

    def test_the_gate_refuses_a_low_level_target(self):
        rig = Rig()
        rig.tick(user())
        step = {"call": "combat.attackUser", "input": {"userId": "user_low"},
                "meta": {"target": {"userId": "user_low", "username": "Low", "level": 90}}}
        v = rig.brain.gates.check(step, rig.world, "pvp_hunt")
        self.assertEqual((v.ok, v.rule), (False, "fair_target"))

    def test_holds_on_aurora_dusk_and_momochi_end_on_their_own(self):
        import datetime as dt
        before = dt.datetime(2026, 11, 25, tzinfo=dt.timezone.utc).timestamp()
        after = dt.datetime(2026, 11, 26, 21, 0, tzinfo=dt.timezone.utc).timestamp()
        never, _ = gates.do_not_attack(C.DO_NOT_ATTACK, before)
        self.assertTrue({"aurora_dusk", "momochi", "keoshi", "jazu", "indrauchiha", "angelsaber"} <= never)
        never, _ = gates.do_not_attack(C.DO_NOT_ATTACK, after)
        self.assertFalse({"aurora_dusk", "momochi"} & never)
        self.assertTrue({"keoshi", "jazu", "indrauchiha", "angelsaber"} <= never)


class FullBeforeAFight(unittest.TestCase):
    def test_the_hunt_holds_the_attack_until_hp_is_full(self):
        rig = Rig()
        out = rig.tick(user(hp=4900), scan([PREY]))                     # 97%: over the potion's line, not full
        self.assertNotIn("combat.attackUser", calls(out))
        self.assertIn("holding the attack on Prey", out["note"])
        out = rig.tick(user(), scan([PREY]), dt=10)
        self.assertIn("combat.attackUser", calls(out))

    def test_short_chakra_gets_the_ramen_first(self):
        rig = Rig()
        rig.tick(user(curChakra=80), scan([PREY]))
        out = rig.tick(user(curChakra=80), dt=2)
        self.assertEqual(calls(out), ["village.buyFood", "profile.getUser"])

    def test_the_gate_refuses_an_attack_short_of_full(self):
        rig = Rig()
        rig.tick(user(hp=4000))
        step = {"call": "combat.attackUser", "input": {"userId": "user_prey"},
                "meta": {"target": {"userId": "user_prey", "username": "Prey", "level": 100}}}
        v = rig.brain.gates.check(step, rig.world, "pvp_hunt")
        self.assertEqual((v.ok, v.rule), (False, "full_pools"))


class Stealth(unittest.TestCase):
    def test_cast_when_off_once_per_cooldown_and_kept_while_up(self):
        rig = Rig(stealth=False)
        out = rig.tick(user())
        self.assertIn("stealth.activateStealth", calls(out))
        out = rig.tick(user(), scan([]), dt=8)
        self.assertNotIn("stealth.activateStealth", calls(out))         # asked, not answered: not asked twice
        rig.tick(res("stealth.activateStealth", {"success": True}), user(), scan([]), dt=8)
        self.assertTrue(rig.world["map"]["stealth"]["on"])
        out = rig.tick(user(), scan([]), dt=C.STEALTH_COOLDOWN)
        self.assertNotIn("stealth.activateStealth", calls(out))

    def test_an_attack_breaks_it_and_a_trip_too(self):
        rig = Rig()
        rig.tick(res("combat.attackUser", {"success": True, "battleId": "B9"}, {"userId": "user_prey"}))
        st = rig.world["map"]["stealth"]
        self.assertFalse(st["on"])
        self.assertGreater(st["ready_at"], rig.t)

    def test_it_expires_after_twenty_minutes(self):
        rig = Rig(stealth=False)
        rig.tick(res("stealth.activateStealth", {"success": True}), user())
        out = rig.tick(user(), dt=C.STEALTH_FOR + 1)                     # the next scan casts it again
        self.assertIn("stealth.activateStealth", calls(out))


class Threat(unittest.TestCase):
    """The snipe after a loss: someone who beat me is in the sector, awake, and my stealth is down."""
    WINNER = ("user_winner", "Winner", 11, 11, "AWAKE", 100, "y", None, None)

    def rig(self, stealth):
        rig = Rig(stealth=stealth)
        rig.world["opponents"]["lost_to"]["user_winner"] = 1e12
        rig.tick(user())
        return rig

    def test_with_stealth_down_the_hunt_leaves_his_sector(self):
        rig = self.rig(False)
        out = rig.tick(user(), scan([self.WINNER, PREY]))
        self.assertIn("travel.startGlobalMove", calls(out))
        self.assertNotIn("combat.attackUser", calls(out))
        self.assertIn("Winner beat me", out["note"])
        self.assertEqual([e["about"] for e in rig.events("finding")], ["threat"])

    def test_with_stealth_up_it_stays_and_hunts(self):
        rig = self.rig(True)
        out = rig.tick(user(), scan([self.WINNER, PREY]))
        self.assertNotIn("travel.startGlobalMove", calls(out))

    def test_asleep_or_in_a_fight_he_is_no_threat(self):
        rig = self.rig(False)
        rig.tick(user(), scan([self.WINNER[:4] + ("BATTLE",) + self.WINNER[5:]]))
        self.assertFalse(rig.events("finding"))


class AfterEveryFight(unittest.TestCase):
    def end(self, rig, sector=1538):
        rig.tick(user(sector=sector))
        rig.world["records"]["fight_end"] = {"bid": "B1", "result": "won", "hp": 5050, "max": 5050, "at": rig.t}
        return rig.brain.reg.activities["recovery"].after_fight(rig.world)

    def test_a_step_off_the_tile_then_a_repair(self):
        rig = Rig(upkeep=True)
        self.end(rig)
        out = rig.tick(user(), dt=1)
        self.assertEqual(calls(out), ["travel.moveInSector", "profile.getUser"])
        self.assertEqual(out["steps"][0]["input"]["longitude"], 12)     # two tiles off (10, 10)
        self.assertTrue(rig.world.own("repair").get("after_fight"))

    def test_no_step_at_home(self):
        rig = Rig()
        self.end(rig, sector=C.HOME_SECTOR)
        out = rig.tick(user(sector=C.HOME_SECTOR))
        self.assertNotIn("travel.moveInSector", calls(out))

    def test_the_repair_goes_out_whatever_the_last_items_read_says(self):
        rig = Rig()
        rig.world["control"]["activities"]["repair"] = True
        repair = rig.brain.reg.activities["repair"]
        rig.tick(user())
        self.assertFalse(repair.available(rig.world))                    # nothing close to broken
        rig.world.own("repair")["after_fight"] = True
        self.assertTrue(repair.available(rig.world))
        p = repair.plan(rig.world)
        self.assertEqual([s["call"] for s in p.steps], ["item.useRepairAll", "item.getUserItems"])
        self.assertIn("after the fight", p.note)
        self.assertFalse(rig.world.own("repair").get("after_fight"))


class Circuit(unittest.TestCase):
    def test_the_directors_circuit_and_never_210(self):
        rig = Rig()
        console.set_control(rig.dir, circuit=[1490, 724])
        out = rig.tick(user(sector=55))
        self.assertIn("heading to the circuit (1490)", out["note"])
        from player.activities.pvp_hunt import circuit_of
        rig.world["control"]["circuit"] = [210]
        self.assertNotIn(210, circuit_of(rig.world))


if __name__ == "__main__":
    unittest.main()
