"""The review of c0006266 (docs/reviews/AI_PLAYER_AP1_REREVIEW2_REVIEW.md on chatgpt/review-ai-player-ap1-rereview2
@ c9e7a1e6): three findings, the classes H1 to H3, each built on the review's own reproducer (its appendices B1
to B3). Those tests fail on c0006266.

H1  a log line the tick could not read was kept in the fight's state, and every tick after it failed
H2  the call ledger took a time it had no proof of: a relay that was replaced and went on, an answer's time
    from another clock
H3  a `brain next` that died before it had the answer down handed the same results in twice
"""
import io
import json
import os
import time
import unittest
from unittest import mock

from player import brain, budget as B, calls as K, config as C, relay
from player.tests.support import FOE, Rig, battle_read, fixture, log_read, res, start_fight, user
from player.tests.test_relay import nxt, token_of, transcript
from player.tests.test_review import NOT_VALID, about, acts, answers, turns
from player.world import Result


def most_in_a_minute(times):
    return max((sum(1 for u in times if t - 60 < u <= t) for t in times), default=0)


def ask(rig, seq, results=(), at=None, **said):
    """One request through brain.answer, as the resident brain takes it, crash handler and all; the batch."""
    if at is not None:
        rig.t = at
    path = relay.request_path(rig.dir, seq)
    relay.write(path, dict({"seq": seq, "results": relay.pack(results)}, **said))
    brain.answer(rig.brain, rig.dir, path)
    return relay.read(relay.batch_path(rig.dir, seq))


def well_formed(row):
    def number(v):
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    return ((isinstance(row[0], str) or number(row[0])) and number(row[1]) and isinstance(row[2], str)
            and isinstance(row[3], str)
            and (row[4] is None or isinstance(row[4], list) and all(isinstance(x, str) for x in row[4])))


class H1ALogLineTheTickCannotRead(unittest.TestCase):
    """A new line whose action was an object was kept in the fight's entries before the tick ran. The tick
    raised on it, the undo put it back, and every tick after raised again: six crashes, no action to T+60."""

    MOMENTS = (1, 2, 12, 15, 20, 60)

    def fight(self, log):
        """The review's script: my turn, the first plan refused, and one log read; then nothing but the clock."""
        rig = Rig()
        battle, _, out = start_fight(rig)
        T, seen = rig.t, []
        for seq, t in enumerate(self.MOMENTS, 90):
            results = answers(out, NOT_VALID) + [battle_read("B1", battle), log_read("B1", log)] if t == 1 else []
            out = ask(rig, seq, results, at=T + t)
            seen.append(acts(out))
        return rig, battle, seen

    def new_line(self, battle, **change):
        row = {"*.id": "new-row", "*.battleRound": battle["battle.round"], "*.userId": FOE,
               "*.actionId": "valid-action", K.ENT[4]: []}
        row.update(change)
        return {k: [v] for k, v in row.items()}

    def test_an_action_that_is_an_object(self):
        battle = fixture()[0]
        good = self.fight(self.new_line(battle))[2]
        self.assertTrue(good[0] and good[2])                                # the control: actions at T+1 and T+12
        for action in ({}, [], {"a": 1}, ["x"], None, 7, True):
            rig, _, seen = self.fight(self.new_line(battle, **{"*.actionId": action}))
            self.assertEqual(seen, good, action)                            # was: nothing, at all six moments
            self.assertEqual(rig.events("error"), [], action)               # was: six crashes
            self.assertNotIn("new-row", [e[0] for e in rig.world["battle"]["entries"]], action)
            self.assertEqual(len(about(rig, "selects")), 1, action)         # the read is dropped, and that is said

    def test_no_new_line_of_any_shape_is_kept_unless_it_is_whole(self):
        """Every field of a line never seen before, as every kind of JSON value; with the effects as texts and
        whole. (The sweep at c0006266 changed lines the fight already had, which are never taken in again.)"""
        battle = fixture()[0]
        good = self.fight(self.new_line(battle))[2]
        shapes = (None, 7, 1.5, True, "x", {}, [], {"a": 1}, [1], ["x"], [[]], [{"txt": {}}], [{"txt": "hit"}])
        fields = ["*.id", "*.battleRound", "*.userId", "*.actionId", K.ENT[4], "*.appliedEffects"]
        for field in fields:
            for shape in shapes:
                log = self.new_line(battle, **{field: shape})
                if field == "*.appliedEffects":
                    log.pop(K.ENT[4])
                for bare in (False, True):                                  # the field's column: a list, or the value
                    if bare:
                        log[field] = shape
                    rig, _, seen = self.fight(log)
                    what = (field, shape, bare)
                    self.assertEqual(rig.events("error"), [], what)
                    self.assertEqual(seen, good, what)
                    self.assertTrue(all(well_formed(e) for e in rig.world["battle"]["entries"]), what)

    def test_a_tick_that_keeps_failing_still_plays_every_turn(self):
        """Whatever breaks the tick, and for however long: here it fails on every read of the fight."""
        rig = Rig()
        battle, _, out = start_fight(rig)
        R, v = battle["battle.round"], battle["battle.version"]
        fight = rig.brain.reg.activities["battle"]
        with mock.patch.object(type(fight), "_absorb", side_effect=RuntimeError("this fight breaks the tick")):
            first = ask(rig, 1, answers(out, NOT_VALID) + [battle_read("B1", battle)], at=rig.t + 1)
            second = ask(rig, 2, at=rig.t + 1)
            self.assertEqual((acts(first), acts(second)), ([], ["defensiveStance"]))   # was: nothing, both times
            self.assertEqual(second["steps"][0]["input"]["version"], v)
            took = ask(rig, 3, answers(second), at=rig.t + 2)               # the game takes the stance
            self.assertEqual(acts(took), [])                                # nothing more of this turn is owed
            his = dict(battle, **{"battle.version": v + 2, "battle.activeUserId": FOE})
            self.assertEqual(acts(ask(rig, 4, [battle_read("B1", his)], at=rig.t + 3)), [])
            mine = dict(battle, **{"battle.round": R + 1, "battle.version": v + 4})
            again = ask(rig, 5, [battle_read("B1", mine)], at=rig.t + 9)    # my next turn, seen by a failing tick
            self.assertEqual(acts(again), ["defensiveStance"])
            self.assertEqual(again["steps"][0]["input"]["version"], v + 4)  # from the read that came with it
        self.assertEqual([(t["round"], t["outcome"]) for t in turns(rig)], [(R, "acted")])
        self.assertEqual({e["about"] for e in rig.events("error")}, {"crash"})    # every failure is written down
        self.assertTrue(os.path.exists(os.path.join(rig.dir, "crash.log")))

    def test_a_last_resort_never_acts_on_a_fight_that_is_over(self):
        rig = Rig()
        battle, _, out = start_fight(rig)
        fight = rig.brain.reg.activities["battle"]
        down = dict(battle, **{"battle.usersState.*.curHealth": [0 if u != C.ME else 900
                                                                  for u in battle["battle.usersState.*.userId"]]})
        with mock.patch.object(type(fight), "_absorb", side_effect=RuntimeError("this fight breaks the tick")):
            ask(rig, 1, answers(out) + [battle_read("B1", down)], at=rig.t + 1)
            last = ask(rig, 2, [battle_read("B1", down)], at=rig.t + 1)
        self.assertEqual(acts(last), [])
        self.assertIn("profile.getUser", rig.calls(last))                   # my profile says whether it is over


class H2TheLedgerTakesNoTimeItCannotProve(unittest.TestCase):
    """A batch that was given up was taken to have run at that moment: its relay went on and made a 31st call in
    a minute. An answer's time from the relay's transcript was taken as it stood: one that read early let the
    world lane make 24 calls in a minute."""

    def test_a_relay_that_was_replaced_and_goes_on_with_its_batch(self):
        """The review's script: one call out, given up after a second; its relay makes it a minute later, while
        the replacement's batches use the budget."""
        rig, made = Rig(), []
        origin, budget = rig.t, rig.brain.budget
        budget.pace([K.user()], "world")
        rig.t += 1
        budget.settle()                                                     # given up: its relay was replaced
        rig.t = origin + 62
        made.append(rig.t)                                                  # and the old relay makes the call
        for _ in range(15):
            out, _ = budget.pace([K.user(), K.user()], "recovery")
            for s in out:
                if "wait" in s:
                    rig.t += s["wait"]
                else:
                    made.append(rig.t)
                    rig.t += .01
            rig.t += .01
        self.assertLessEqual(most_in_a_minute(made), C.CALL_LIMIT)          # was 31

    def test_a_loose_call_counts_in_every_minute_until_there_is_evidence(self):
        """(At 442a6311 the hold ended by itself after LOOSE_FOR. The review of that commit ruled that out: see
        test_rereview3.)"""
        rig = Rig()
        budget, t0 = rig.brain.budget, rig.t
        budget.pace([K.user()] * 3, "world")
        budget.settle()
        for later in (0, 61, 600, 10 * C.LOOSE_ALERT):
            self.assertEqual(budget.used(t0 + later), 3, later)
            rig.t = t0 + later
            self.assertEqual(budget.used(), 3, later)

    def test_the_replaced_relay_coming_back_settles_its_calls(self):
        rig = Rig()
        budget, t0 = rig.brain.budget, rig.t
        rig.world["budget"]["batch"] = 6
        budget.pace([K.user()] * 3, "world")
        budget.settle()
        rig.t = t0 + 80
        budget.ended(5, t0 + 40)                                            # some other batch: nothing changes
        self.assertEqual(budget.used(t0 + 500), 3)
        budget.ended(6, t0 + 40)                                            # its relay was back at t0+40
        self.assertEqual((budget.used(), budget.used(t0 + 99), budget.used(t0 + 101)), (3, 3, 0))

    def test_an_answers_time_from_the_transcript_is_not_used(self):
        """The review's script: five world calls a batch, the first batch slow, the answers' times off."""
        for skew in (0, -100, -3, -0.5, 30):
            rig, made = Rig(), []
            for lag in [8] + [.4] * 7:
                steps = [K.user()] * 5
                out, _ = rig.brain.budget.pace(steps, "world")
                results = []
                for s in out:
                    if "wait" in s:
                        rig.t += s["wait"]
                    else:
                        made.append(rig.t)
                        rig.t += lag
                        results.append(Result(s["call"], s["input"], {}, None, rig.t + skew))
                rig.brain.budget.settle(results, [s for s in out if "call" in s])
                rig.t += .5
            self.assertLessEqual(most_in_a_minute(made), C.WORLD_CAP, skew)    # was 24 at -100

    def test_a_time_of_the_brains_own_clock_is_used_when_it_can_be_true(self):
        rig = Rig()
        budget, t0 = rig.brain.budget, rig.t
        out, _ = budget.pace([K.user()] * 4, "world")
        asked = [s for s in out if "call" in s]
        rig.t = t0 + 30
        put = [Result(s["call"], s["input"], {}, None, at) for s, at in zip(asked, (t0 + 9, t0 - 50, t0 + 31))]
        budget.settle(put, asked, own_clock=True)
        times = [c[0] for c in rig.world["budget"]["calls"]]
        # answered at t0+9: then. A time before the call could run, a time after now, no answer: now.
        self.assertEqual(times, [t0 + 9, t0 + 30, t0 + 30, t0 + 30])
        budget.pace([K.user()] * 4, "world")                                # the same answers, said to be the transcript's
        rig.t = t0 + 60
        budget.settle([r._replace(at=t0 + 39) for r in put[:1]], asked)
        self.assertEqual([c[0] for c in rig.world["budget"]["calls"]][4:], [t0 + 60] * 4)

    # ---- through the real client: who says a batch is given up, and who says its relay is back
    def client(self):
        self.rig = Rig()
        self.rig.world.save()
        env = mock.patch.dict(os.environ, {
            "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(self.rig.dir, "missing.jsonl"),
            "TNR_PLAYER_LIVE": self.rig.dir, "TNR_PLAYER_FIGHTS": os.path.join(self.rig.dir, "fights")})
        env.start()
        self.addCleanup(env.stop)

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.rig.dir, token, out, lambda _: None)
        return out.getvalue().splitlines()

    def ledger(self):
        return relay.read(os.path.join(self.rig.dir, "world.json"))["budget"]["calls"]

    def loose(self, token):
        """The loose calls of the batch a relay had under this token."""
        return [c for c in self.ledger() if c[2:3] == ["loose"] and c[5] == token]

    def test_a_replacement_leaves_the_old_relays_batch_loose_until_that_relay_comes_back(self):
        self.client()
        old = token_of(self.next(token_of(self.next()[0]))[-1])             # a relay, with its first batch
        n = len([c for c in self.ledger() if c[2:3] == ["out"]])
        self.assertGreater(n, 0)
        new = token_of(self.next(token_of(self.next()[0]))[-1])             # replaced: the new one gets a batch
        self.assertEqual(len(self.loose(old)), n)                           # was: settled, as if they had all run
        self.assertEqual(self.next("abcdef-1"), [brain.SUPERSEDED])         # some other old relay: proves nothing
        new = token_of(self.next(new)[-1])
        self.assertEqual(len(self.loose(old)), n)
        self.assertEqual(self.next(old), [brain.SUPERSEDED])                # the replaced relay is back
        new = token_of(self.next(new)[-1])
        self.assertEqual(self.loose(old), [])                               # its calls had run by then
        self.assertGreaterEqual(len([c for c in self.ledger() if len(c) == 2]), n)  # and leave a minute after that

    def test_a_relay_that_never_had_a_batch_cannot_speak_for_one(self):
        """A relay's first token repeats the number of the batch another relay holds. One that is replaced
        before it ever asked comes back with that token: it says nothing about that batch."""
        self.client()
        holder = token_of(self.next(token_of(self.next()[0]))[-1])          # a relay, with a batch
        never, new = token_of(self.next()[0]), token_of(self.next()[0])     # two replacements; the first never asks
        self.assertEqual(never.split("-")[1], holder.split("-")[1])         # the same number, another relay
        self.assertEqual(self.next(never), [brain.SUPERSEDED])
        new = token_of(self.next(new)[-1])
        self.assertTrue(self.loose(holder))                                 # still held
        self.next(new)
        self.assertTrue(self.loose(holder))


class H3ARequestIsAnsweredOnce(unittest.TestCase):
    """A `brain next` that died after the brain had answered, before it wrote that down, came again with the
    same results: they were applied a second time."""

    def setUp(self):
        self.rig = Rig()
        self.rig.world.save()
        self.path = os.path.join(self.rig.dir, "t.jsonl")
        env = mock.patch.dict(os.environ, {
            "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": self.path,
            "TNR_PLAYER_LIVE": self.rig.dir, "TNR_PLAYER_FIGHTS": os.path.join(self.rig.dir, "fights")})
        env.start()
        self.addCleanup(env.stop)
        self.seen, real = [], brain.Brain.handle

        def spy(self_, results, *a, **k):
            self.seen.append(len(results))
            return real(self_, results, *a, **k)
        spying = mock.patch.object(brain.Brain, "handle", spy)
        spying.start()
        self.addCleanup(spying.stop)

    def next(self, token=None):
        out = io.StringIO()
        brain.next_batch(self.rig.dir, token, out, lambda _: None)
        return out.getvalue().splitlines()

    def test_a_client_that_dies_before_it_has_the_answer_down(self):
        """The review's script: a real transcript, the client killed at its write of the batch it is owed."""
        t0 = token_of(self.next()[0])
        transcript(self.path, [("bash", "n0", nxt(t0), time.time())])
        t1 = token_of(self.next(t0)[-1])
        transcript(self.path, [("bash", "n0", nxt(t0), time.time()), ("use", "u", "profile.getUser", {}, time.time()),
                               ("res", "u", json.dumps(user(sector=77).data), time.time()),
                               ("bash", "n1", nxt(t1), time.time())])
        del self.seen[:]
        real_write = relay.write

        class Killed(Exception):
            pass

        def dying(path, obj):
            if path == os.path.join(self.rig.dir, "client.json") and obj.get("pending"):
                raise Killed
            return real_write(path, obj)
        with mock.patch.object(relay, "write", dying):
            with self.assertRaises(Killed):
                self.next(t1)
        events = len(self.rig.events())
        again = self.next(t1)                                               # the relay runs the same line again
        self.assertEqual(self.seen, [1])                                    # was [1, 1]
        self.assertTrue(any('"call"' in line for line in again))            # and it has its batch all the same
        self.assertEqual(len(self.rig.events()), events)                    # nothing happened twice
        self.next(token_of(again[-1]))
        self.assertEqual(self.seen, [1, 0])                                 # the next request is a new one

    def request(self, relay_name, seq, results=()):
        path = relay.request_path(self.rig.dir, seq)
        relay.write(path, {"seq": seq, "relay": relay_name, "results": relay.pack(results)})
        brain.answer(self.rig.brain, self.rig.dir, path)
        batch = relay.read(relay.batch_path(self.rig.dir, seq))
        if batch is not None:
            os.unlink(relay.batch_path(self.rig.dir, seq))
        return batch

    def test_the_same_request_gets_the_same_answer_and_an_older_one_none(self):
        first = self.request("aa11", 5, [user(sector=77)])
        self.assertEqual(self.request("aa11", 5, [user(sector=77)])["steps"], first["steps"])
        self.assertEqual(self.seen, [1])
        self.assertIsNone(self.request("aa11", 4, [user(sector=12)]))       # older than the last one answered
        self.assertEqual((self.seen, len(about(self.rig, "relay"))), ([1], 1))
        self.assertEqual(self.rig.world.me["sector"], 77)                   # and nothing of it was taken in
        self.assertIsNotNone(self.request("bb22", 5))                       # another relay's request is its own
        self.assertIsNotNone(self.request("aa11", 6))
        self.assertEqual(self.seen, [1, 0, 0])

    def test_the_answer_is_saved_with_what_the_request_changed(self):
        first = self.request("aa11", 5, [user(sector=77)])
        self.rig.new_brain()                                                # the brain restarts from its file
        self.assertEqual(self.request("aa11", 5, [user(sector=77)])["steps"], first["steps"])
        self.assertEqual(self.seen, [1])

    def test_a_request_whose_tick_crashed_is_not_run_again_either(self):
        with mock.patch.object(brain.Brain, "_decide", side_effect=RuntimeError("this tick breaks")):
            first = self.request("aa11", 5, [user(sector=77)])
            again = self.request("aa11", 5, [user(sector=77)])
        self.assertEqual((first["steps"], again["steps"], self.seen), ([], [], [1]))
        self.assertEqual(len(self.rig.events("error")), 1)

    def test_what_is_left_of_the_wait_is_what_the_second_answer_asks_for(self):
        self.rig.world["control"]["paused"] = True                          # nothing to do: a long hold
        first = self.request("aa11", 5)
        self.rig.t += 12
        again = self.request("aa11", 5)
        self.assertEqual((first["hold"], again["hold"]), (brain.IDLE_HOLD, brain.IDLE_HOLD - 12))


class SweptBesideTheFindings(unittest.TestCase):
    """Not from the review: the other things a batch brings back, and the other ways a tick can fail, searched
    for the same three faults (a value taken in unchecked, a time not the brain's own, a batch from nowhere)."""

    def test_a_profile_that_cannot_be_used_costs_nothing_else_in_its_batch(self):
        for field, value in (("money", "x"), ("bank", [1]), ("battleId", 7), ("curHealth", None), ("status", 5),
                             ("maxHealth", "x"), ("longitude", {}), ("sector", True)):
            rig = Rig()
            battle, _, out = start_fight(rig)
            before = dict(rig.world.me)
            profile = dict(user("BATTLE", bid="B1").data, **{f"userData.{field}": value})
            got = ask(rig, 1, answers(out, NOT_VALID) + [res("profile.getUser", profile), battle_read("B1", battle)],
                      at=rig.t + 1)
            self.assertEqual(acts(got), ["defensiveStance"], field)         # was: no action (money, bank)
            self.assertEqual(rig.events("error"), [], field)                # was: a crashed tick
            self.assertEqual((rig.world.me, len(about(rig, "selects"))), (before, 1), field)

    def test_a_good_profile_is_still_a_good_profile(self):
        rig = Rig()
        for profile in (user(), user("BATTLE", bid="B1"), user(money="1500000.5", bank=0), user(curEnergy=None),
                        user(hp=4040.5, pos=(3, 4))):
            rig.tick(profile)
            self.assertEqual(rig.world.me["status"], profile.data["userData.status"])
        self.assertEqual((rig.world.me["curHealth"], about(rig, "selects")), (4040.5, []))

    def test_the_day_of_a_spend_is_the_brains_own_clocks(self):
        rig = Rig()
        rig.tick(user(money=2_000_000))
        rig.tick(user(money=1_500_000)._replace(at=0.0))                    # a transcript line with no time on it
        self.assertEqual(rig.world.spent_today(), 500_000)                  # was 0: the day began anew in 1970
        rig.tick(user(money=1_400_000)._replace(at=rig.t - 3 * 86400))
        self.assertEqual(rig.world.spent_today(), 600_000)

    def test_an_answer_to_an_action_that_is_no_answer_is_not_known_to_have_landed(self):
        for answer in ("x", 7, [1], True):
            rig = Rig()
            battle, _, out = start_fight(rig)
            his = dict(battle, **{"battle.version": battle["battle.version"] + 2, "battle.activeUserId": FOE})
            said = [Result("combat.performAction", {"battleId": "B1", "actionId": a}, answer, None, None)
                    for a in acts(out)]
            ask(rig, 1, said + [battle_read("B1", his)], at=rig.t + 1)
            self.assertEqual(rig.events("error"), [], answer)               # was: the read beside it was lost
            self.assertEqual(rig.world["battle"]["battle"]["battle.activeUserId"], FOE, answer)
            self.assertEqual([t["outcome"] for t in turns(rig)], ["unresolved"], answer)

    def test_an_activity_that_cannot_say_whether_it_can_act_is_set_aside(self):
        rig = Rig()
        rig.tick(user())
        hunt = type(rig.brain.reg.activities["pvp_hunt"])
        with mock.patch.object(hunt, "available", side_effect=ValueError("bad state")):
            out = rig.tick(user())                                          # was: the tick failed, every time
            self.assertNotEqual(out["activity"], "pvp_hunt")
            self.assertIn("pvp_hunt", rig.world.own("brain")["blocked"])
            self.assertEqual(rig.tick(user("BATTLE", bid="B7"))["activity"], "battle")
        self.assertEqual({e["about"] for e in rig.events("error")}, {"crash"})

    def test_a_status_file_that_cannot_be_written_does_not_cost_the_batch(self):
        rig = Rig()
        battle, _, out = start_fight(rig)
        with mock.patch("player.console.write_status", side_effect=OSError("disk")):
            out = rig.tick(*answers(out, NOT_VALID), battle_read("B1", battle))
        self.assertEqual(acts(out), ["defensiveStance"])                    # was: the tick failed, no action
        self.assertEqual([e["about"] for e in rig.events("error")], ["crash"])

    def test_a_batch_file_left_under_the_next_number_is_never_printed(self):
        rig = Rig()
        rig.world.save()
        env = mock.patch.dict(os.environ, {
            "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(rig.dir, "missing.jsonl"),
            "TNR_PLAYER_LIVE": rig.dir, "TNR_PLAYER_FIGHTS": os.path.join(rig.dir, "fights")})
        env.start()
        self.addCleanup(env.stop)

        def run(token=None):
            out = io.StringIO()
            brain.next_batch(rig.dir, token, out, lambda _: None)
            return out.getvalue()
        stale = {"seq": 1, "stop": None, "hold": 0.0,
                 "steps": [{"call": "combat.performAction", "input": {"battleId": "OLD"}, "select": []}]}
        relay.write(relay.batch_path(rig.dir, 1), stale)                    # from another life of this folder
        printed = run(token_of(run().splitlines()[0]))
        self.assertNotIn("OLD", printed)                                    # was: printed, as this relay's batch
        self.assertIn("profile.getUser", printed)


if __name__ == "__main__":
    unittest.main()
