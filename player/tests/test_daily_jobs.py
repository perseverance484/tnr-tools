"""The day's jobs: errands paced across the day, the streak and the interest once a day, missions handed to the
model (tnr-autopilot DESIGN.md section 5; director 2026-11-10: "20 missions and 50 errands is the cap")."""
import os
import unittest

from player import config as C
from player.activities import dailies as D
from player.activities import errands as E
from player.tests.support import Rig, res, user

HOME = dict(sector=C.HOME_SECTOR, pos=(10, 10))
START = 1_800_000_000.0     # 2027-01-15 08:00 UTC: an even spread expects 20 of 50 errands by now


def calls(out):
    return [s.get("call") for s in out["steps"]]


def call(out, endpoint):
    return next(s["input"] for s in out["steps"] if s.get("call") == endpoint)


class Pacing(unittest.TestCase):
    def test_behind_is_the_share_of_the_cap_under_an_even_spread_to_20_utc(self):
        self.assertAlmostEqual(E.behind(10, 50, START), 0.2)
        self.assertEqual(E.behind(30, 50, START), 0.0)
        self.assertAlmostEqual(E.behind(45, 50, START + 13 * 3600), 0.1)     # 21:00: the whole cap is expected

    def test_on_schedule_the_hunt_keeps_the_account_and_well_behind_errands_take_it(self):
        hunt = 10.0
        self.assertLess(E.paced_value(0.1, False) * 0.7, hunt)
        self.assertGreater(E.paced_value(0.4, False) * 0.7, hunt)
        self.assertGreater(E.paced_value(0.1, True) * 0.7, hunt)              # a burst runs until caught up


class Errands(unittest.TestCase):
    def rig(self, done):
        r = Rig(daily=True)
        r.world["control"]["activities"]["dailies"] = False
        r.home = dict(HOME, dailyErrands=done)
        return r

    def test_well_behind_one_whole_errand_goes_in_one_batch(self):
        r = self.rig(0)
        out = r.tick(user(**r.home))
        self.assertEqual(out["activity"], "errands")
        self.assertEqual(call(out, "quests.startRandom"), {"type": "errand", "rank": "D", "userLevel": 100,
                                                           "userSector": C.HOME_SECTOR,
                                                           "userVillageId": C.HOME_VILLAGE})
        self.assertEqual(calls(out).count("quests.checkLocationQuest"), 2)
        self.assertEqual(call(out, "quests.checkRewards"), {"questId": E.QUEST_ID})

    def test_on_schedule_the_hunt_goes_on(self):
        r = self.rig(25)
        self.assertNotEqual(r.tick(user(**r.home))["activity"], "errands")

    def test_at_the_cap_no_errand_is_started(self):
        r = self.rig(50)
        r.t += 12 * 3600                                                      # 20:00: far behind if not done
        self.assertNotEqual(r.tick(user(**r.home))["activity"], "errands")

    def test_away_from_home_it_goes_home_first(self):
        r = self.rig(0)
        out = r.tick(user(**dict(r.home, sector=1538)))
        self.assertEqual(out["activity"], "errands")
        self.assertNotIn("quests.startRandom", calls(out))
        self.assertIn("travel.startGlobalMove", calls(out))

    def test_a_refused_start_rests_an_hour_and_a_limit_rests_the_day(self):
        for msg, rest in (("not now", E.RETRY), ("daily limit reached", 86_400)):
            r = self.rig(0)
            out = r.tick(user(**r.home))
            r.tick(res("quests.startRandom", {"success": False, "message": msg}, call(out, "quests.startRandom")),
                   user(**r.home))
            self.assertAlmostEqual(r.world.own("errands")["rest_until"], r.t - 1 + rest, delta=2)
            self.assertTrue(any("refused" in e["text"] for e in r.events("finding")))

    def test_an_errand_it_does_not_know_is_a_finding_for_the_model(self):
        r = self.rig(0)
        out = r.tick(user(**r.home))
        r.tick(res("quests.startRandom", {"success": True, "message": "You started Lost Cat"},
                   call(out, "quests.startRandom")), user(**r.home))
        self.assertEqual([e["about"] for e in r.events("finding")], ["exception"])
        self.assertGreater(r.world.own("errands")["rest_until"], r.t)

    def test_stealth_goes_up_in_the_errand_batch_when_it_is_down(self):
        r = Rig(daily=True, stealth=False)
        r.world["control"]["activities"]["dailies"] = False
        out = r.tick(user(**dict(HOME, dailyErrands=0)))
        self.assertEqual(out["activity"], "errands")
        self.assertIn("stealth.activateStealth", calls(out))


class Dailies(unittest.TestCase):
    STREAKS = {"streaks": [{"configId": "c1", "canClaim": True}, {"configId": "c2", "canClaim": False},
                           {"configId": "c3", "canClaim": True, "claimedToday": True}]}

    def test_claimable_streaks_reads_any_shape_with_config_ids(self):
        self.assertEqual(D.claimable_streaks(self.STREAKS), ["c1"])
        self.assertEqual(D.claimable_streaks({"data": [{"config": {"id": "x"}, "claimable": True}]}), ["x"])
        self.assertIsNone(D.claimable_streaks({"days": [1, 2, 3]}))

    def test_pending_interest(self):
        self.assertEqual(D.pending_interest(1200), 1200.0)
        self.assertEqual(D.pending_interest({"data": {"amount": 5}}), 5.0)
        self.assertIsNone(D.pending_interest({"nothing": True}))

    def test_once_a_day_reads_then_claims_and_never_pays_for_a_catch_up(self):
        r = Rig(daily=True)
        r.world["control"]["activities"]["errands"] = False
        out = r.tick(user(**HOME))
        self.assertEqual((out["activity"], calls(out)),
                         ("dailies", ["activityStreak.getUserStreaks", "bank.getPendingInterest"]))
        out = r.tick(res("activityStreak.getUserStreaks", self.STREAKS), res("bank.getPendingInterest", {"amount": 9}),
                     user(**HOME))
        self.assertEqual(out["activity"], "dailies")
        self.assertEqual(call(out, "activityStreak.claimStreakDay"),
                         {"configId": "c1", "payCatchUp": False, "reset": False})
        self.assertIn("bank.claimInterest", calls(out))
        self.assertTrue(os.path.exists(os.path.join(r.dir, "captures", "activityStreak.getUserStreaks.json")))
        for _ in range(3):
            self.assertNotEqual(r.tick(user(**HOME), dt=400)["activity"], "dailies")
        r.t += 86_400                                                          # the next UTC day
        self.assertEqual(r.tick(user(**HOME))["activity"], "dailies")

    def test_an_unreadable_streak_read_claims_nothing_and_is_a_finding(self):
        r = Rig(daily=True)
        r.world["control"]["activities"]["errands"] = False
        r.tick(user(**HOME))
        out = r.tick(res("activityStreak.getUserStreaks", {"days": [1]}), res("bank.getPendingInterest", 0),
                     user(**HOME))
        self.assertNotIn("activityStreak.claimStreakDay", calls(out))
        self.assertEqual([e["about"] for e in r.events("finding")], ["exception"])


class Missions(unittest.TestCase):
    def rig(self):
        r = Rig(daily=True)
        r.world["control"]["activities"].update(errands=False, dailies=False)
        return r

    def test_off_until_the_director_switches_it_on(self):
        r = self.rig()
        self.assertNotEqual(r.tick(user(**HOME))["activity"], "missions")

    def test_a_run_is_started_held_for_the_model_and_handed_back(self):
        r = self.rig()
        r.world["control"]["activities"]["missions"] = True
        out = r.tick(user(**HOME))
        self.assertEqual(out["activity"], "missions")
        self.assertEqual(call(out, "quests.startRandom")["type"], "medical")
        out = r.tick(res("quests.startRandom", {"success": True, "message": "started"}, call(out, "quests.startRandom")),
                     res("quests.getUserQuests", {"quests": [1]}, {"userId": C.ME}), user(**HOME))
        self.assertEqual([e["about"] for e in r.events("finding")], ["exception"])
        self.assertTrue(os.listdir(os.path.join(r.dir, "exceptions")))
        for _ in range(3):                                                      # the account stays put
            out = r.tick(user(**HOME), dt=130)
            self.assertEqual((out["activity"], calls(out)), ("missions", ["profile.getUser"]))
        r.world["control"]["quest_done"] = True
        out = r.tick(user(**HOME), dt=130)
        self.assertFalse(r.world["control"]["quest_done"])
        self.assertNotEqual(calls(out), ["profile.getUser"])                     # the wait is over: the arbiter's again
        self.assertIsNone(r.brain.reg.activities["missions"].waiting(r.world))
        self.assertEqual(r.world.own("missions")["counts"]["medical"], 1)

    def test_a_limit_rests_that_kind_for_the_day(self):
        r = self.rig()
        r.world["control"]["activities"]["missions"] = True
        out = r.tick(user(**HOME))
        r.tick(res("quests.startRandom", {"success": False, "message": "Daily limit"}, call(out, "quests.startRandom")),
               user(**HOME))
        self.assertGreater(r.world.own("missions")["rest"]["medical"], r.t + 80_000)
        out = r.tick(user(**HOME))
        if out["activity"] == "missions":
            self.assertEqual(call(out, "quests.startRandom")["type"], "mission")


if __name__ == "__main__":
    unittest.main()
