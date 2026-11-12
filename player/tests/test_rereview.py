"""The re-reviews of the corrected player.

Of 39f30ead (docs/reviews/AI_PLAYER_AP1_CORRECTION_REVIEW.md on chatgpt/review-ai-player-ap1-correction @
adeb7807) and of c225ed36 (docs/reviews/AI_PLAYER_AP1_LIVE_RULINGS_REVIEW.md on
chatgpt/review-ai-player-ap1-live-rulings @ 406f674a): four findings, the classes F1 to F4, built on the reviews'
own reproducers. Those tests fail on c225ed36.

Of 0d10b7c6 (the director's summary of 2026-11-12; three findings left open, the fourth closed): the classes G1
to G3, built from that summary. Those tests fail on 0d10b7c6.

The two Swept classes are not from a review: the same three areas searched once more for the next gap of the
same kind. They fail on 0d10b7c6 as well.
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
from player.tests.support import FOE, LINE, Rig, battle_read, fixture, log_read, res, scan, start_fight, user
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

    def test_a_call_is_counted_from_when_its_batch_came_back(self):
        """(At c225ed36 an answered call was counted from the time its answer carried. The review of c0006266
        showed that time cannot be relied on when it is the transcript's: see test_rereview2.)"""
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = []
        out = rig.tick(user())                                              # the hunt's scan: three or four calls
        t0, n = rig.t, len(rig.calls(out))
        self.assertEqual({len(c) for c in rig.world["budget"]["calls"]}, {3})   # written down, marked as still out
        first = out["steps"][0]
        rig.tick(res(first["call"], user().data, first["input"])._replace(at=t0 + 9.0), dt=30)   # back at t0+30
        times = sorted(c[0] for c in rig.world["budget"]["calls"])[:n]
        self.assertEqual(set(times), {t0 + 30})                             # every call: when the batch came back
        #                                                                     so at t0+68 all are still in the minute

    def test_calls_still_out_survive_a_restart(self):
        rig = Rig()
        rig.tick(user())
        out = rig.tick(user())
        rig.world.save()
        rig.new_brain()
        self.assertTrue(any(len(c) == 3 for c in rig.world["budget"]["calls"]))
        rig.t += 45
        rig.brain.budget.settle(asked=())                                   # the relay is back
        self.assertEqual(rig.brain.budget.used(rig.t + 59), len(rig.calls(out)))   # and they count from now


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
            sent = []
            for seq, results in ((1, answers(out, NOT_VALID) + [battle_read("B1", battle)]), (2, [])):
                rig.t += 1
                req = relay.request_path(rig.dir, seq)
                relay.write(req, {"seq": seq, "results": relay.pack([r._replace(at=rig.t) for r in results])})
                brain.answer(rig.brain, rig.dir, req)
                sent.append(acts(relay.read(relay.batch_path(rig.dir, seq))))
            self.assertNotIn("inbox", rig.world["battle"])                  # it failed twice: not a third time
        # and the turn is not stuck behind it. (At c225ed36 the stance went on the next tick that worked; since
        # the review of c0006266 it goes with the second failure itself: see test_rereview2.)
        self.assertEqual(sent, [[], ["defensiveStance"]])


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


class G1ACallThatIsStillOutStaysInTheLedger(unittest.TestCase):
    """During a batch longer than a minute, the watchdog's status write dropped the calls that were still out;
    they were never settled, and 31 real calls went in a minute while the ledger said 30."""

    def fight_batch(self):
        return ([K.act("B", "a", 0, 0, 1), K.wait(1.2), K.act("B", "b", 0, 0, 2)]
                + watching([K.battle("B"), K.entries("B", 8)]))

    def test_a_status_write_during_a_long_batch_drops_nothing(self):
        rig, made, stalls = Rig(), [], []
        for n, lag in enumerate([20.0] + [0.3] * 14):                       # the first batch lasts eighty seconds
            out, _ = rig.brain.budget.pace(self.fight_batch(), "battle")
            if n == 0:                                                      # as the brain notes a batch it issues
                rig.world["relay"].update(issued_at=rig.t, expect=relay.seconds(out), stalled=False)
            for s in out:
                if "wait" in s:
                    rig.t += s["wait"]
                else:
                    made.append(rig.t)
                    rig.t += lag
                if n == 0 and rig.t - made[0] > 61 and not stalls:
                    stalls.append(rig.brain.watchdog())                     # the stall is raised, the status written
            if n == 0:
                rig.brain.budget.settle(asked=[x for x in out if "call" in x])   # that relay is back, at last
            rig.t += 0.5
        self.assertEqual(stalls, [True])
        self.assertLessEqual(most_in_a_minute(made), C.CALL_LIMIT)          # was 31

    def test_calls_out_for_over_a_minute_are_still_counted_and_then_settled(self):
        rig = Rig()
        rig.tick(user())
        rig.world["budget"]["calls"] = []
        out = rig.tick(user())
        n = len(rig.calls(out))
        rig.t += 90                                                         # the relay has had the batch for 90 s
        self.assertTrue(rig.brain.watchdog())
        self.assertEqual(rig.status()["budget"]["last_minute"], n)          # was 0: dropped by this very read
        self.assertEqual(len(rig.world["budget"]["calls"]), n)
        rig.brain.budget.settle(asked=())                                   # the relay is back
        self.assertEqual({c[0] for c in rig.world["budget"]["calls"]}, {rig.t})   # counted from when it came back
        self.assertEqual(rig.brain.budget.used(rig.t + 59), n)


class G2WhatAUsableReadIs(unittest.TestCase):
    """A read whose active id was none of its fighters passed for his turn: it replaced the last good read and no
    action went through T+60. A read with a null position reached an action."""

    def owed(self, change):
        """My turn, both planned actions refused, and then only this broken read, at the review's five moments."""
        rig = Rig()
        battle, ents, out = start_fight(rig)
        T, seen = rig.t, []
        bad = dict(battle, **change)
        for t in (1, 12, 15, 20, 60):
            out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", bad), dt=T + t - rig.t)
            seen.append(out)
        return rig, battle, seen

    def test_an_active_id_that_is_no_fighter(self):
        rig, battle, seen = self.owed({"battle.activeUserId": "user_nobody"})
        self.assertEqual([acts(o) for o in seen[:2]], [["defensiveStance"], ["wait"]])   # was nothing, five times
        self.assertEqual(rig.world["battle"]["battle"]["battle.activeUserId"], C.ME)     # the last good read stands
        self.assertEqual(turns(rig), [])                                    # and my turn was not closed as his

    def test_no_value_from_a_broken_read_reaches_an_action(self):
        for change in ({"battle.usersState.*.longitude": [None, None]}, {"battle.usersState.*.latitude": [None, 4]},
                       {"battle.usersState.*.curHealth": ["2756", 4943]}, {"battle.usersState.*.curHealth": [True, 1]},
                       {"battle.usersState.*.userId": [C.ME, C.ME]}, {"battle.usersState.*.username": [None, "x"]},
                       {"battle.version": "11"}, {"battle.round": None}, {"battle.activeUserId": None}):
            rig, battle, seen = self.owed(change)
            sent = [s["input"] for o in seen for s in o["steps"] if s.get("call") == "combat.performAction"]
            self.assertTrue(sent, change)                                   # the turn still gets its actions
            me = battle["battle.usersState.*.userId"].index(C.ME)
            where = (battle["battle.usersState.*.longitude"][me], battle["battle.usersState.*.latitude"][me])
            for inp in sent:                                                # from the last good read, whole
                self.assertEqual(((inp["longitude"], inp["latitude"]), inp["version"]),
                                 (where, battle["battle.version"]), change)
            self.assertEqual(rig.world["battle"]["battle"]["battle.usersState.*.curHealth"],
                             battle["battle.usersState.*.curHealth"], change)
            self.assertEqual(rig.events("error"), [], change)

    def test_a_good_read_is_still_a_good_read(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        his = dict(battle, **{"battle.activeUserId": FOE, "battle.version": battle["battle.version"] + 2})
        self.assertIn("his turn", rig.tick(*answers(out), battle_read("B1", his))["note"])
        self.assertEqual(about(rig, "selects"), [])


class G3ABatchIsKnownByItsOwnId(unittest.TestCase):
    """A batch that grew too old was recomputed under the same number. A call still waiting on the old one could
    then publish it in the new one's place, and the fresh decision was thrown away."""

    setUp = F3ARelayReplacedWhileItsOldCallWaits.setUp
    next = F3ARelayReplacedWhileItsOldCallWaits.next
    client = F3ARelayReplacedWhileItsOldCallWaits.client
    calls = F3ARelayReplacedWhileItsOldCallWaits.calls
    started = F3ARelayReplacedWhileItsOldCallWaits.started

    def test_an_older_waiter_does_not_publish_its_batch_over_a_fresher_one(self):
        t1 = self.started()
        path = os.path.join(self.rig.dir, "client.json")

        def recomputed_meanwhile(delay):
            if delay == C.HUNT_WAIT:                                        # while this call waits, its batch grows
                state = self.client()                                       # old and another call has the brain
                fresh = dict(state["pending"], id="f" * 8, ready_at=time.time() + 5,   # asked again: same number,
                             steps=[{"call": "profile.getUser", "input": {}, "select": ["fresh"]}])   # as before
                relay.write(path, dict(state, pending=fresh))
        old = self.next(t1, recomputed_meanwhile)
        self.assertEqual(old, [relay.next_line(t1)])                        # was: its own obsolete batch
        self.assertEqual(self.client()["pending"]["id"], "f" * 8)           # was: None, the fresh one thrown away
        got = self.next(t1)                                                 # it comes back, and gets the fresh one
        self.assertEqual(json.loads(got[0])["select"], ["fresh"])

    def test_a_number_is_not_used_twice(self):
        t1, new = self.started(), []
        self.next(t1, lambda d: new.append(token_of(self.next()[0])) if d == C.HUNT_WAIT else None)
        state = self.client()
        old_seq, old_id = state["pending"]["seq"], state["pending"]["id"]
        state["pending"]["ready_at"] = time.time() - C.STALE_OUTBOX - 1      # the replacement took its time
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        seen = []
        got = self.next(new[0], lambda d: seen.append(self.client()["pending"]))
        self.assertEqual((seen[-1]["seq"], seen[-1]["id"] != old_id), (old_seq + 1, True))   # was the same number
        self.assertTrue(token_of(got[-1]).endswith(f"-{old_seq + 1}"))

    def test_two_calls_of_one_relay_and_a_batch_that_expires_between_them(self):
        """The review's own script (its appendix A3): nothing is written into client.json by hand. One call waits
        on a batch; the batch grows too old; a second call of the same relay has the brain asked afresh, after
        the director changed a setting; then both wake."""
        clock, printed = [100.0], {}
        ready, release = [threading.Event(), threading.Event()], [threading.Event(), threading.Event()]
        t1 = self.started()

        def run(i):
            def sleep(_):
                ready[i].set()
                release[i].wait(5)
            printed[i] = self.next(t1, sleep)
        with mock.patch.object(brain.time, "time", side_effect=lambda: clock[0]):
            first = threading.Thread(target=run, args=(0,))
            first.start()
            self.assertTrue(ready[0].wait(3))
            old = self.client()["pending"]
            clock[0] = old["ready_at"] + C.STALE_OUTBOX + 1
            relay.write(os.path.join(self.rig.dir, "control.json"), {"version": 1, "mode": "guard"})
            second = threading.Thread(target=run, args=(1,))
            second.start()
            self.assertTrue(ready[1].wait(3))
            fresh = self.client()["pending"]
            release[0].set()
            first.join(3)
            release[1].set()
            second.join(3)
        self.assertEqual(fresh["seq"], old["seq"] + 1)                      # was the same number
        self.assertEqual(self.calls(printed[0]), [])                        # was: the old batch's calls
        self.assertEqual(self.calls(printed[1]), [x["call"] for x in fresh["steps"] if "call" in x])
        self.assertNotEqual(self.calls(printed[1]), [x["call"] for x in old["steps"] if "call" in x])


class SweptAfterThreeReviews(unittest.TestCase):
    """Not from a review: the same three areas, searched for the next gap of the same kind after three rounds had
    each found one (the ledger missing a call, an unchecked input reaching the tick, a delivery made twice)."""

    def test_calls_the_relay_made_unasked_are_in_the_ledger(self):
        rig = Rig()
        rig.tick(user())
        rig.brain.handle([], None, strays=3)
        self.assertEqual(rig.brain.budget.used(lane="stray"), 3)            # was 0: made, and not counted
        full = [[rig.world.now, "battle"] for _ in range(C.CALL_LIMIT - 3)]
        rig.world["budget"]["calls"] += full                                # with them, the minute is full:
        steps, waited = rig.brain.budget.pace([K.act("B1", "a", 1, 1, 1)], "battle")
        self.assertGreater(waited, 0)                                       # so even an action has to wait

    def test_a_log_line_with_no_round_is_not_taken_and_breaks_nothing(self):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        n = len(rig.world["battle"]["entries"])
        odd = dict(zip(K.ENT, (["z1", "z2"], [None, 3], [FOE, FOE], ["a", "b"], [["x"], ["y"]])))
        out = rig.tick(*answers(out), battle_read("B1", dict(battle, **{"battle.activeUserId": FOE})), log_read("B1", odd))
        self.assertEqual((len(rig.world["battle"]["entries"]), "his turn" in out["note"]), (n, True))
        self.assertEqual(rig.events("error"), [])

    def test_a_planners_line_that_cannot_be_sent_is_no_line(self):
        for broken in ({"actionId": "a", "longitude": None, "latitude": 4, "name": "A"},
                       {"actionId": None, "longitude": 6, "latitude": 4, "name": "A"},
                       {"actionId": "a", "longitude": 6, "latitude": 4}, "strike"):
            rig = Rig()
            rig.combat.line = [broken]
            rig.combat.plan_turn = lambda *a, **k: ([broken], "0.1s stub")
            battle, ents, out = start_fight(rig)
            self.assertEqual(acts(out), ["defensiveStance"], broken)        # used to raise, or send a null tile
            self.assertEqual(rig.events("error"), [], broken)

    def test_a_scan_that_breaks_the_hunt_sets_the_hunt_aside_not_the_player(self):
        rig = Rig()
        rig.tick(user())
        bad_row = ("u_p", "Prey", None, 14, "AWAKE", 100, "y", None, None)   # no longitude
        out = rig.tick(user(), scan([bad_row]))
        self.assertNotEqual(out["activity"], "pvp_hunt")                    # used to raise, on every tick after
        self.assertTrue(rig.calls(out))
        self.assertEqual([e["about"] for e in rig.events("error")], ["crash"])
        self.assertIn("pvp_hunt", rig.world.own("brain")["blocked"])
        out = rig.tick(user("BATTLE", bid="B3"))                            # and a fight is still fought
        self.assertEqual(out["activity"], "battle")

    def test_one_activitys_bad_result_does_not_cost_the_others_theirs(self):
        rig = Rig()
        rig.tick(user())
        with mock.patch.object(type(rig.brain.reg.activities["pvp_hunt"]), "on_result", side_effect=ValueError("bad")):
            out = rig.tick(scan([]), user("BATTLE", bid="B4"))
        self.assertEqual((out["activity"], rig.world["battle"]["bid"]), ("battle", "B4"))
        self.assertIn("pvp_hunt could not take a result in", rig.events("error")[0]["text"])

    def test_a_batchs_results_are_handed_to_the_brain_once(self):
        case = F3ARelayReplacedWhileItsOldCallWaits("test_replaced_during_the_brain_side_hold")
        case.setUp()
        self.addCleanup(case.env.stop)
        t1, seen, real = case.started(), [], brain.Brain.handle

        def spy(self_, results, *a, **k):
            seen.append(len(results))
            return real(self_, results, *a, **k)

        class Killed(Exception):
            pass

        def killed(delay):
            if delay == C.HUNT_WAIT:
                raise Killed                                                # the call dies before it prints its batch
        with mock.patch.object(brain.Brain, "handle", spy):
            with self.assertRaises(Killed):
                case.next(t1, killed)
            brain.put(case.rig.dir, t1, 1, json.dumps(user(sector=77).data))   # the relay tries again, same batch
            state = case.client()
            state["pending"]["ready_at"] = time.time() - C.STALE_OUTBOX - 1  # and by then the batch is too old
            relay.write(os.path.join(case.rig.dir, "client.json"), state)
            case.next(t1)
        self.assertEqual(seen, [1, 0])                                      # was [1, 1]: the same results twice


class SweptEveryShapeOfARead(unittest.TestCase):
    """Every field of a battle read and of a log read, broken in every way a JSON value can be, on my turn with
    both planned actions refused. Nothing raises, no error is written, an action still goes, and every action
    that goes has a real tile and version. (The same sweep over both turns, 1,128 cases: 120 failed on 0d10b7c6.)

    Its log half changes lines the fight already has, and those are never taken in again (the review of c0006266
    saw that): the lines never seen before are swept in test_rereview2.py, class H1."""

    EFFECTS = {"battle.usersEffects": [{"type": "damage", "targetId": FOE, "creatorId": C.ME, "power": 30, "rounds": 2,
                                        "createdRound": 1, "timeTracker": {"originalDamage": 55}},
                                       {"type": "buff", "targetId": C.ME, "creatorId": C.ME, "power": 5}]}
    GROUND = dict({f"battle.groundEffects.*.{k}": v for k, v in zip(
        K.GROUND_COLS, (["barrier", "damage"], [FOE, FOE], [5, 6], [4, 4], [1, 2], [2, 2], [1, 1]))},
        **{f"battle.groundEffects.*.{k}": [100] for k in K.BARRIER_COLS})
    WHOLE = {"battle.groundEffects": [{"type": "barrier", "longitude": 5, "latitude": 4, "curHealth": 9}]}
    MISSING = object()

    def shapes(self, v):
        yield from (None, "x", 7, True, [], {}, self.MISSING)
        if isinstance(v, list):
            yield from (v[:-1], v + v[-1:], [None] * len(v), ["x"] * len(v), [[x] for x in v], [{} for _ in v],
                        [True] * len(v), [{"type": {"a": 1}, "timeTracker": "x", "rounds": "x", "power": []}] + v[1:])

    def play(self, key, val, in_log=False, extra=None):
        rig = Rig()
        battle, ents, out = start_fight(rig)
        T, sent = rig.t, []
        read, log = dict(battle, **(extra or {})), dict(ents)
        target = log if in_log else read
        if val is self.MISSING:
            target.pop(key, None)
        else:
            target[key] = val
        for t in (1, 12):
            reads = [battle_read("B1", dict(read))] + ([log_read("B1", dict(log))] if in_log else [])
            out = rig.tick(*answers(out, NOT_VALID), *reads, dt=T + t - rig.t)
            sent += [s["input"] for s in out["steps"] if s.get("call") == "combat.performAction"]
        return rig, sent

    def check(self, source, in_log=False, extra=None, acts_owed=True):
        for key, v in source.items():
            for val in self.shapes(v):
                what = (key, "missing" if val is self.MISSING else val)
                rig, sent = self.play(key, val, in_log, extra)              # must not raise
                self.assertEqual(rig.events("error"), [], what)
                self.assertTrue(sent or not acts_owed, what)
                for inp in sent:
                    self.assertTrue(isinstance(inp["actionId"], str) and all(
                        isinstance(inp[k], (int, float)) and not isinstance(inp[k], bool)
                        for k in ("longitude", "latitude", "version")), (what, inp))

    def test_the_fighters_and_the_turn(self):
        self.check(fixture()[0])

    def test_the_log(self):
        self.check(fixture()[1], in_log=True)

    def test_the_effect_list_and_the_ground(self):
        for extra in (self.EFFECTS, self.GROUND, self.WHOLE):
            self.check(extra, extra=extra)


if __name__ == "__main__":
    unittest.main()
