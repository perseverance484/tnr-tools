"""The re-reviews of the corrected player: of 39f30ead (docs/reviews/AI_PLAYER_AP1_CORRECTION_REVIEW.md on
chatgpt/review-ai-player-ap1-correction @ adeb7807) and of c225ed36
(docs/reviews/AI_PLAYER_AP1_LIVE_RULINGS_REVIEW.md on chatgpt/review-ai-player-ap1-live-rulings @ 406f674a).
Four findings; one class each, built on the reviews' own reproducers. Every test here fails on c225ed36.
"""
import io
import json
import os
import threading
import time
import unittest
from unittest import mock

from player import brain, budget as B, calls as K, config as C, relay
from player.activities.battle import watching
from player.tests.support import FOE, LINE, Rig, battle_read, log_read, res, start_fight, user
from player.tests.test_relay import token_of
from player.tests.test_review import NOT_VALID, about, acts, answers, turns


def most_in_a_minute(times):
    return max(sum(1 for u in times if t - 60 < u <= t) for t in times)


class F1TheLimitsByTheClockTheCallsReallyRanOn(unittest.TestCase):
    """The ledger used the times it predicted. A slow batch followed by fast ones then made 31 real calls in a
    minute, and 24 in the world lane, while the ledger said 30 and 20."""

    def run_batches(self, lane, lags):
        """The review's probe: every wait the budget returns is slept, every call runs when its turn comes and
        takes that batch's latency; the times are kept apart from the ledger."""
        rig, made = Rig(), []
        for lag in lags:
            steps = ([K.user()] * 5 if lane == "world" else
                     [K.act("B", "a", 0, 0, 1), K.wait(1.2), K.act("B", "b", 0, 0, 2)]
                     + watching([K.battle("B"), K.entries("B", 8)]))
            out, _ = rig.brain.budget.pace(steps, lane)
            for s in out:
                if "wait" in s:
                    rig.t += s["wait"]
                else:
                    made.append(rig.t)
                    rig.t += lag
            rig.t += 0.5
        return most_in_a_minute(made)

    def test_a_slow_batch_then_fast_ones_stay_under_thirty(self):
        self.assertLessEqual(self.run_batches("battle", [8, 3, .4, 1, .2, .2, .4, 3, .4, 1, 3]), C.CALL_LIMIT)   # was 31
        self.assertLessEqual(self.run_batches("battle", [.4] * 11), C.CALL_LIMIT)
        self.assertLessEqual(self.run_batches("battle", [.05] * 30), C.CALL_LIMIT)       # faster than any guess
        self.assertLessEqual(self.run_batches("battle", [20, .1, .1, .1, .1, 15, .1, .1, .1, .1, .1, .1]), C.CALL_LIMIT)

    def test_the_world_lane_stays_under_its_twenty(self):
        self.assertLessEqual(self.run_batches("world", [8] + [.4] * 7), C.WORLD_CAP)     # was 24
        self.assertLessEqual(self.run_batches("world", [.05] * 12), C.WORLD_CAP)

    def test_a_call_is_counted_from_when_its_answer_came_back(self):
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = []
        out = rig.tick(user())                                              # the hunt's scan: three or four calls
        t0, n = rig.t, len(rig.calls(out))
        self.assertEqual({len(c) for c in rig.world["budget"]["calls"]}, {3})   # written down, marked as still out
        first, second = out["steps"][0], [s for s in out["steps"] if "call" in s][1]
        back = [res(first["call"], user().data, first["input"])._replace(at=t0 + 9.0),
                res(second["call"], {"users.*.userId": []}, second["input"])._replace(at=t0 + 14.0)]
        rig.tick(*back, dt=30)                                              # the relay was slow: it is back at t0+30
        times = sorted(c[0] for c in rig.world["budget"]["calls"])[:n]
        self.assertEqual(times[:2], [t0 + 9.0, t0 + 14.0])                  # the two that were answered: then
        self.assertEqual(set(times[2:]), {t0 + 30})                         # the rest: when the batch came back
        self.assertGreater(min(times), t0 + 8)                              # so at t0+68 all are still in the minute

    def test_calls_still_out_survive_a_restart(self):
        rig = Rig()
        rig.tick(user())
        out = rig.tick(user())
        rig.world.save()
        rig.new_brain()
        self.assertTrue(any(len(c) == 3 for c in rig.world["budget"]["calls"]))
        rig.t += 45
        rig.brain.budget.settle()
        self.assertEqual(rig.brain.budget.used(rig.t + 59), len(rig.world["budget"]["calls"]))


class F2AReadThatCannotBeUsed(unittest.TestCase):
    """A read with both fighters but one health value asked for another read for ever, past T+12, T+15, T+20 and
    the end of the turn."""

    def bad(self, battle):
        return dict(battle, **{"battle.usersState.*.curHealth": [123]})

    def test_the_reviews_sequence_now_ends_in_actions(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        T, seen = rig.t, []
        for t in (1, 12, 15, 20, 60):
            out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", self.bad(battle)), dt=T + t - rig.t)
            seen.append(acts(out))
        self.assertEqual(seen[:2], [["defensiveStance"], ["wait"]])        # was no action at any of the five
        self.assertEqual(rig.world["battle"]["battle"]["battle.usersState.*.curHealth"],
                         battle["battle.usersState.*.curHealth"])            # the last good read is untouched
        self.assertEqual(len(about(rig, "selects")), 1)                      # said once, not five times

    def test_a_plan_with_no_answer_goes_again_at_t_plus_12(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(battle_read("B1", self.bad(battle)), dt=5)
        self.assertEqual(acts(out), [])                                     # T+5: one more read first
        out = rig.tick(battle_read("B1", self.bad(battle)), dt=C.LAST_GOOD_READ_AT - 5)
        self.assertEqual(acts(out), [a["actionId"] for a in LINE])          # T+12: from the last good read
        self.assertIn("last good read", out["note"])

    def test_a_read_without_the_round_or_the_version_is_no_read_either(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        for missing in ("battle.version", "battle.round", "battle.activeUserId"):
            broken = {k: v for k, v in battle.items() if k != missing}
            out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", broken), dt=1)   # used to crash the tick
            self.assertTrue(rig.world.in_battle())
        self.assertEqual(rig.events("error"), [])

    def test_the_first_read_of_a_fight_coming_back_unusable_is_read_again(self):
        rig = Rig()
        battle, ents = start_fight(Rig())[:2]
        rig.tick(user("BATTLE", bid="B1"))
        out = rig.tick(battle_read("B1", self.bad(battle)), log_read("B1", ents))
        self.assertEqual((acts(out), rig.calls(out)[0]), ([], "combat.getBattle"))

    def test_a_read_whose_tick_crashes_twice_is_dropped_and_the_clock_decides(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        fight = rig.brain.reg.activities["battle"]
        with mock.patch.object(type(fight), "_absorb", side_effect=RuntimeError("this read breaks the tick")):
            for seq, results in ((1, answers(out, NOT_VALID) + [battle_read("B1", battle)]), (2, [])):
                rig.t += 1
                req = relay.request_path(rig.dir, seq)
                relay.write(req, {"seq": seq, "results": relay.pack([r._replace(at=rig.t) for r in results])})
                brain.answer(rig.brain, rig.dir, req)
                self.assertEqual(relay.read(relay.batch_path(rig.dir, seq))["steps"], [])
            self.assertNotIn("inbox", rig.world["battle"])                  # it failed twice: not a third time
        out = rig.tick(dt=1)                                                # and the turn is not stuck behind it
        self.assertEqual(acts(out), ["defensiveStance"])


class F3ARelayReplacedWhileItsOldCallWaits(unittest.TestCase):
    """An old `brain next` that was waiting wrote its own name back over its replacement's and printed its batch;
    the replacement was told to stop."""

    def setUp(self):
        self.rig = Rig()
        self.rig.world.save()
        self.env = mock.patch.dict(os.environ, {
            "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(self.rig.dir, "missing.jsonl"),
            "TNR_PLAYER_LIVE": self.rig.dir, "TNR_PLAYER_FIGHTS": os.path.join(self.rig.dir, "fights")})
        self.env.start()
        self.addCleanup(self.env.stop)

    def next(self, token=None, sleep=lambda _: None):
        out = io.StringIO()
        brain.next_batch(self.rig.dir, token, out, sleep)
        return out.getvalue().splitlines()

    def client(self):
        return relay.read(os.path.join(self.rig.dir, "client.json"))

    def calls(self, lines):
        return [json.loads(x)["call"] for x in lines if x.startswith("{") and "call" in json.loads(x)]

    def started(self):
        """A relay with its first batch answered; returns the token it will hand in next."""
        t1 = token_of(self.next(token_of(self.next()[0]))[-1])
        brain.put(self.rig.dir, t1, 1, json.dumps(user().data))
        return t1

    def test_replaced_during_the_brain_side_hold(self):
        t1, new = self.started(), []

        def replaced_meanwhile(delay):
            if delay == C.HUNT_WAIT:
                new.append(token_of(self.next()[0]))                        # a replacement shakes hands
        old = self.next(t1, replaced_meanwhile)
        self.assertEqual(old, [brain.SUPERSEDED])                           # was: its batch, four calls
        self.assertEqual(self.client()["relay"], new[0].split("-")[0])      # was: the old relay's name again
        got = self.next(new[0])
        self.assertEqual(self.calls(got)[:2], ["profile.getUser", "travel.getSectorData"])   # was: STOP superseded
        self.assertTrue(token_of(got[-1]).startswith(new[0].split("-")[0]))
        self.assertEqual(self.rig.brain.__class__(self.rig.dir).world["relay"]["seq"], 2)    # one tick made it, once

    def test_the_handshake_waits_for_an_exchange_that_is_under_way(self):
        done = []
        with brain._client(self.rig.dir):                                   # an old call is talking to the brain
            taker = threading.Thread(target=lambda: done.append(self.next()))
            taker.start()
            time.sleep(0.3)
            self.assertEqual(done, [])                                      # the replacement does not cut in
        taker.join(5)
        self.assertEqual(len(done), 1)

    def test_a_batch_left_too_long_is_not_handed_on(self):
        t1, new = self.started(), []
        self.next(t1, lambda d: new.append(token_of(self.next()[0])) if d == C.HUNT_WAIT else None)
        state = self.client()
        state["pending"]["ready_at"] = time.time() - C.STALE_OUTBOX - 1      # the replacement took its time
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        self.next(new[0])
        self.assertEqual(self.rig.brain.__class__(self.rig.dir).world["relay"]["seq"], 3)    # the brain was asked afresh

    def test_the_same_relay_calling_twice_gets_its_batch_once(self):
        t1, inner = self.started(), []
        outer = self.next(t1, lambda d: inner.append(self.next(t1)) if d == C.HUNT_WAIT else None)
        self.assertEqual(len(self.calls(inner[0])), 4)                      # one of the two has the batch
        self.assertEqual(outer, [relay.next_line(self.client()["token"])])  # the other is only told to come back


class F4StraightIntoAnotherFight(unittest.TestCase):
    """The proof profile said BATTLE, in another battle. The old fight's potion went out into the new fight, and
    the new fight was not opened."""

    def left_for(self, status, bid):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        out = rig.tick(*answers(out), battle_read("B1", {}))
        self.assertIn("profile.getUser", rig.calls(out))
        return rig, rig.tick(user(status, bid=bid, hp=1000))

    def test_a_rematch_opens_at_once_and_gets_no_potion(self):
        rig, out = self.left_for("BATTLE", "B2")
        self.assertEqual(rig.calls(out), ["combat.getBattle", "combat.getBattleEntries"])   # was item.consume, profile
        self.assertEqual(out["steps"][0]["input"], {"battleId": "B2"})
        self.assertEqual(rig.world["battle"]["bid"], "B2")                  # was no battle at all
        self.assertEqual([e["battle"] for e in rig.events("fight_start")], ["B1", "B2"])

    def test_the_old_fight_is_closed_and_kept(self):
        rig, out = self.left_for("BATTLE", "B2")
        end = rig.events("fight_end")
        self.assertEqual([(e["battle"], e["result"]) for e in end], [("B1", "won")])   # the log's own count
        self.assertTrue(os.path.exists(os.path.join(rig.combat.fights, "B1_entries.json")))
        self.assertIsNone(rig.world["records"]["pending_result"])
        rig.combat.lost_by_log = True
        rig2, _ = self.left_for("BATTLE", "B2")
        rig2.combat.lost_by_log = True
        rig3 = Rig()
        rig3.combat.lost_by_log = True
        battle, ents, out = start_fight(rig3)
        rig3.tick(*answers(out), battle_read("B1", {}))
        rig3.tick(user("BATTLE", bid="B2"))
        self.assertEqual(rig3.events("fight_end")[0]["result"], "lost")
        self.assertIn(FOE, rig3.world["opponents"]["lost_to"])

    def test_the_two_controls(self):
        rig, out = self.left_for("BATTLE", "B1")                            # the same battle: it goes on
        self.assertEqual((rig.world["battle"]["bid"], "item.consume" in rig.calls(out)), ("B1", False))
        rig, out = self.left_for("AWAKE", None)                             # out of combat: the potion is right
        self.assertEqual(rig.calls(out), ["item.consume", "profile.getUser"])

    def test_no_recovery_call_goes_out_while_the_new_fight_is_on(self):
        rig, out = self.left_for("BATTLE", "B2")
        battle, ents = start_fight(Rig())[:2]
        for _ in range(3):
            out = rig.tick(battle_read("B2", dict(battle, **{"battle.activeUserId": FOE, "battle.usersEffects": []})),
                           log_read("B2", ents), dt=out["hold"] + 3)
            self.assertNotIn("item.consume", rig.calls(out))


if __name__ == "__main__":
    unittest.main()
