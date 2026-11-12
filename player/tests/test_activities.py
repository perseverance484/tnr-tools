"""The world activities ported from the pilot's world(): hunt, recovery, session, travel, watch, harvest."""
import unittest

from player import config as C
from player.tests.support import Rig, limited, res, scan, user

ME_ROW = (C.ME, "dauntless", 10, 10, "AWAKE", 100, "x", None, None)
PREY = ("u_p", "Prey", 13, 14, "AWAKE", 100, "y", None, None)
PASSED_OVER = [("u_s", "Shisui", 11, 10, "AWAKE", 100, "y", None, None),          # on do_not_attack.md
               ("u_f", "Friend", 12, 10, "AWAKE", 100, "y", None, None),          # on do_not_attack.md
               ("u_i", "Immune", 12, 11, "AWAKE", 100, "y", "2099-01-01T00:00:00Z", None),
               ("u_l", "Low", 12, 12, "AWAKE", 50, "y", None, None),
               ("u_a", "Ally", 12, 13, "AWAKE", 100, C.HOME_VILLAGE, None, None),
               ("u_b", "Busy", 12, 14, "AWAKE", 100, "y", None, "B9")]


class Hunt(unittest.TestCase):
    def test_the_nearest_fair_target_is_attacked_with_his_kit_read_first(self):
        rig = Rig()
        out = rig.tick(user(), scan([ME_ROW] + PASSED_OVER + [PREY]))
        self.assertIn("attacking Prey", out["note"])
        self.assertEqual(rig.calls(out), ["travel.moveInSector", "jutsu.getPublicUserJutsus", "combat.attackUser",
                                          "profile.getUser"])
        self.assertEqual(out["steps"][0]["input"]["longitude"], 13)
        self.assertEqual(out["steps"][2]["input"]["userId"], "u_p")
        self.assertEqual(rig.world["map"]["last_scan"], {"dna": 2, "immune": 1, "lowlvl": 1, "ally": 1, "battle": 1})

    def test_a_saved_kit_is_not_read_again_and_a_target_on_my_tile_needs_no_walk(self):
        rig = Rig()
        rig.combat.kits.add("u_p")
        out = rig.tick(user(pos=(13, 14)), scan([ME_ROW, PREY]))
        self.assertEqual(rig.calls(out), ["combat.attackUser", "profile.getUser"])

    def test_nobody_to_fight_moves_on_round_the_circuit(self):
        rig = Rig()
        out = rig.tick(user(), scan([ME_ROW] + PASSED_OVER))
        self.assertIn("next sector 1490", out["note"])
        self.assertEqual(out["steps"][0]["input"], {"sector": 1490})
        self.assertEqual(rig.calls(out)[:4], ["travel.startGlobalMove", "travel.finishGlobalMove", "profile.getUser",
                                              "travel.getSectorData"])
        out = rig.tick(user(sector=99), scan([], sector=99))
        self.assertIn("next sector 1538", out["note"])
        out = rig.tick(user(sector=177))
        self.assertIn("heading to the circuit", out["note"])

    def test_a_scan_waits_in_the_brain_and_senses_every_31_seconds(self):
        rig = Rig()
        out = rig.tick(user())
        self.assertEqual(rig.calls(out)[:3], ["profile.getUser", "travel.getSectorData", "stealth.useSensory"])
        self.assertEqual(out["hold"], C.HUNT_WAIT)
        self.assertNotIn("wait", [k for s in out["steps"] for k in s])     # the pause costs the relay nothing
        out = rig.tick(user(), dt=10)
        self.assertNotIn("stealth.useSensory", rig.calls(out))
        out = rig.tick(user(), dt=25)
        self.assertIn("stealth.useSensory", rig.calls(out))

    def test_a_refused_attack_is_remembered(self):
        rig = Rig()
        rig.tick(user(), scan([ME_ROW, PREY]))
        refusal = res("combat.attackUser", {"success": False, "message": "Target is not in your bracket"},
                      {"userId": "u_p"})
        out = rig.tick(refusal, user(), scan([ME_ROW, PREY]))
        self.assertIn("attack refused (bracket)", out["note"])
        self.assertNotIn("combat.attackUser", rig.calls(out))
        self.assertGreater(rig.world["opponents"]["skip"]["u_p"], rig.t + 5 * 3600)

    def test_a_player_who_beat_me_is_left_alone_for_six_hours(self):
        rig = Rig()
        rig.world["opponents"]["lost_to"]["u_p"] = rig.t + 3600
        out = rig.tick(user(), scan([ME_ROW, PREY]))
        self.assertNotIn("combat.attackUser", rig.calls(out))
        self.assertEqual(rig.world["map"]["last_scan"], {"beat me": 1})

    def test_columns_that_do_not_line_up_give_no_target(self):
        rig = Rig()
        bad = scan([ME_ROW, PREY])
        bad.data["users.*.level"] = [100]                                  # one element lacked the key
        out = rig.tick(user(), bad)
        self.assertNotIn("combat.attackUser", rig.calls(out))
        self.assertEqual([e["about"] for e in rig.events("finding")], ["selects"])

    def test_guard_mode_only_watches(self):
        rig = Rig(mode="guard")
        out = rig.tick(user(), scan([ME_ROW, PREY]))
        self.assertEqual((out["activity"], rig.calls(out), out["hold"]), ("watch", ["profile.getUser"], C.WATCH_WAIT))


class Recovery(unittest.TestCase):
    def test_hospital_potion_and_ramen(self):
        rig = Rig()
        out = rig.tick(user("HOSPITALIZED"))
        self.assertEqual((out["activity"], rig.calls(out)), ("recovery", ["hospital.npcHeal", "profile.getUser"]))
        out = rig.tick(user(hp=3000))
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])
        self.assertEqual(out["steps"][0]["input"], {"userItemId": C.FULL_POTION})
        out = rig.tick(user(curChakra=20))
        self.assertEqual(rig.calls(out), ["village.buyFood", "profile.getUser"])

    def test_a_heal_that_changed_nothing_is_not_tried_again_for_ten_minutes(self):
        rig = Rig()
        rig.tick(user(hp=3000))
        out = rig.tick(user(hp=3000))                                      # the potion changed nothing
        self.assertEqual(out["activity"], "pvp_hunt")
        out = rig.tick(user(hp=3000), dt=C.HEAL_RETRY + 1)
        self.assertEqual(out["activity"], "recovery")

    def test_recovery_comes_before_the_hunt_and_is_never_paced(self):
        rig = Rig()
        rig.world["budget"]["calls"] = [[rig.t, "world"]] * C.WORLD_CAP    # the world lane has used all it may
        out = rig.tick(user(hp=3000), scan([ME_ROW, PREY]))
        self.assertEqual(out["activity"], "recovery")
        self.assertEqual([k for s in out["steps"] for k in s if k == "wait"], [])


class SessionTravelWatch(unittest.TestCase):
    def test_a_hunt_wakes_the_character_and_a_guard_lets_it_sleep(self):
        rig = Rig()
        out = rig.tick(user("ASLEEP"))
        self.assertEqual((out["activity"], rig.calls(out)), ("session", ["home.toggleSleep", "profile.getUser"]))
        rig = Rig(mode="guard")
        out = rig.tick(user("ASLEEP"))
        self.assertEqual((out["stop"], out["steps"]), ("asleep", []))

    def test_a_trip_is_landed_after_its_arrival_time(self):
        rig = Rig()
        arrive = "2027-01-15T08:00:40Z"                                    # 39 s after the rig's clock
        out = rig.tick(res("travel.startGlobalMove", {"success": True, "data.travelFinishAt": arrive}, {"sector": 99}),
                       user("TRAVEL"))
        self.assertEqual((out["activity"], rig.calls(out)), ("travel", ["travel.finishGlobalMove", "profile.getUser"]))
        self.assertEqual(out["hold"], 20.0)                                # waits in the brain, 20 s at most a time
        out = rig.tick(user("TRAVEL"), dt=45)
        self.assertEqual(out["hold"], C.TRAVEL_RETRY + 0.5)                # past the arrival time: short retries

    def test_the_first_tick_reads_the_profile(self):
        rig = Rig(mode="guard")
        out = rig.tick()
        self.assertEqual((out["activity"], rig.calls(out), out["hold"]), ("watch", ["profile.getUser"], 0))


class HarvestFeed(unittest.TestCase):
    def test_it_rides_a_quiet_hunt_batch_and_its_answers_are_kept(self):
        rig = Rig()
        out = rig.tick(user())
        self.assertEqual(rig.calls(out)[-1], "profile.getStrongestUsers")       # the hourly top list first
        top = res("profile.getStrongestUsers", {"*.userId": ["user_top1"], "*.username": ["Top"]})
        out = rig.tick(user(), top, dt=10)
        self.assertEqual(rig.calls(out)[-1], "combat.getBattleHistory")
        self.assertIn("players", rig.world.own("harvest")["stats"])

    def test_it_never_rides_an_attack_or_a_full_minute_or_a_fight(self):
        rig = Rig()
        out = rig.tick(user(), scan([ME_ROW, PREY]))
        self.assertNotIn("profile.getStrongestUsers", rig.calls(out))
        rig = Rig()
        rig.world["budget"]["calls"] = [[rig.t, "world"]] * 17               # 3 left: fewer than 2 reads + 4 spare
        self.assertNotIn("profile.getStrongestUsers", rig.calls(rig.tick(user())))

    def test_the_director_can_switch_it_off(self):
        rig = Rig()
        rig.world["control"]["activities"]["harvest"] = False
        self.assertEqual(rig.calls(rig.tick(user()))[-1], "stealth.useSensory")


class RateLimit(unittest.TestCase):
    def test_a_refused_world_batch_backs_off_and_loses_nothing(self):
        rig = Rig()
        rig.tick(user())
        out = rig.tick(limited("profile.getUser"), limited("travel.getSectorData", {"sector": 1538}))
        self.assertEqual(out["activity"], "pvp_hunt")
        self.assertGreaterEqual(out["hold"], C.RATE_BACKOFF)
        self.assertEqual(rig.calls(out)[:2], ["profile.getUser", "travel.getSectorData"])


if __name__ == "__main__":
    unittest.main()
