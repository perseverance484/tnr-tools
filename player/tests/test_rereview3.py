"""The review of 442a6311 (docs/reviews/AI_PLAYER_AP1_REREVIEW3_REVIEW.md on chatgpt/review-ai-player-ap1-rereview3
@ 592ba138): a ruling and six findings, the classes K1 to K6, each built on the review's own reproducer (its
blocks C1 to C5). Those tests fail on 442a6311.

K1  the hold on a replaced relay's calls ended by itself (the ruling: no length of time is evidence)
K2  a relay that was replaced before its batch was printed released another relay's calls
K3  a brain started by `brain next` itself kept a failed tick in memory only
K4  an answer to an action that was nothing, false, 0, "" or [] counted as a taken action
K5  an old brain's late answer went to another relay's request, and that request was lost
K6  a fight my profile had left was acted on when it could not be closed
"""
import io
import json
import os
import threading
import time
import unittest
from unittest import mock

from player import brain, calls as K, config as C, relay
from player.tests.support import LINE, Rig, battle_read, res, start_fight, user
from player.tests.test_relay import token_of
from player.tests.test_rereview2 import ask, most_in_a_minute
from player.tests.test_review import NOT_VALID, about, acts, answers


class Client(unittest.TestCase):
    """The real `brain next`, with no resident brain: each request is answered by a brain started for it."""

    def setUp(self):
        self.rig = Rig()
        self.rig.world.absorb([user()._replace(at=self.rig.t)])
        self.rig.world.save()
        env = mock.patch.dict(os.environ, {
            "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(self.rig.dir, "missing.jsonl"),
            "TNR_PLAYER_LIVE": self.rig.dir, "TNR_PLAYER_FIGHTS": os.path.join(self.rig.dir, "fights")})
        env.start()
        self.addCleanup(env.stop)

    def next(self, token=None, sleep=lambda _: None):
        out = io.StringIO()
        brain.next_batch(self.rig.dir, token, out, sleep)
        return out.getvalue().splitlines()

    def new_relay_with_a_batch(self):
        return token_of(self.next(token_of(self.next()[0]))[-1])

    def client(self):
        return relay.read(os.path.join(self.rig.dir, "client.json"))

    def saved(self):
        return relay.read(os.path.join(self.rig.dir, "world.json"))

    def loose(self, token=None):
        """The loose calls of the batch a relay had under this token. (A loose call names that token; at
        442a6311 it named the batch's number only.)"""
        def of(c):
            return token is None or (c[5] == token if len(c) > 5 else c[3] == int(token.split("-")[1]))
        return [c for c in self.saved()["budget"]["calls"] if c[2:3] == ["loose"] and of(c)]

    def calls(self, lines):
        return [json.loads(x)["call"] for x in lines if x.startswith("{") and "call" in json.loads(x)]

    def stopped(self, *tokens):
        out = io.StringIO()
        brain.stopped(self.rig.dir, list(tokens), out)
        return json.loads(out.getvalue())


class K1NoLengthOfTimeIsEvidence(Client):
    """A loose call's hold ended 900 s after its batch was given up. A call the old relay made just before that
    was still in the real minute when the hold was gone: 31 calls, and 21 in the world lane."""

    def traffic(self, lane, batches, old_call_at, start_at):
        """The review's script: one world call out, given up after a second; its relay makes it at old_call_at;
        from start_at on, two-call batches, every wait slept."""
        rig, budget = Rig(), None
        budget, t0 = rig.brain.budget, rig.t
        budget.pace([K.user()], "world")
        rig.t += 1
        budget.settle()
        made, rig.t = [t0 + old_call_at], t0 + start_at
        for _ in range(batches):
            out, _ = budget.pace([K.user(), K.user()], lane)
            for s in out:
                if "wait" in s:
                    rig.t += s["wait"]
                else:
                    made.append(rig.t)
                    rig.t += .01
            rig.t += .01
        return most_in_a_minute(made)

    def test_a_call_made_just_before_the_old_hold_ended(self):
        self.assertLessEqual(self.traffic("recovery", 15, 900, 902), C.CALL_LIMIT)     # was 31
        self.assertLessEqual(self.traffic("world", 10, 900, 902), C.WORLD_CAP)         # was 21

    def test_a_call_made_hours_later(self):
        self.assertLessEqual(self.traffic("recovery", 15, 7200.5, 7201), C.CALL_LIMIT)
        self.assertLessEqual(self.traffic("world", 10, 86400.5, 86401), C.WORLD_CAP)

    def test_a_long_hold_is_raised_once_and_goes_on(self):
        rig = Rig()
        budget, t0 = rig.brain.budget, rig.t
        budget.pace([K.user()] * 3, "world")
        budget.settle(holder="aa11bb-4")
        self.assertIn("python3 -m player.brain stopped", about(rig, "budget")[0]["text"])   # said when it begins
        rig.t = t0 + C.LOOSE_ALERT + 1
        self.assertEqual((budget.used(), budget.used(), len(about(rig, "budget", "stall"))), (3, 3, 1))
        self.assertIn("aa11bb-4", about(rig, "budget", "stall")[0]["text"])
        rig.t = t0 + 50 * C.LOOSE_ALERT
        self.assertEqual((budget.used(), len(about(rig, "budget", "stall"))), (3, 1))

    def test_the_operators_word_ends_a_hold_and_the_calls_count_a_minute_more(self):
        old = self.new_relay_with_a_batch()
        new = self.new_relay_with_a_batch()                                 # replaced: the old relay's batch is loose
        n = len(self.loose(old))
        self.assertGreater(n, 0)
        status = relay.read(os.path.join(self.rig.dir, "status.json"))["budget"]
        self.assertEqual([(h["relay"], h["calls"]) for h in status["held"]], [(old, n)])    # the operator can see it
        self.assertEqual(self.stopped(new)["not_held"], [new])              # the running relay's batch is not held
        self.assertEqual(self.stopped("aa11bb-9")["stopped"], [])           # nor one nobody ever had
        self.assertEqual(len(self.loose(old)), n)
        before = time.time()
        self.assertEqual(self.stopped(old), {"stopped": [old], "all": False, "not_held": [], "still_held": []})
        new = token_of(self.next(new)[-1])                                  # the brain hears of it with the next request
        self.assertEqual(self.loose(), [])
        counted = [c[0] for c in self.saved()["budget"]["calls"] if len(c) == 2]
        self.assertGreaterEqual(len([t for t in counted if before <= t <= time.time()]), n)   # from when it was said
        said = [e for e in self.rig.events("setting_changed") if e.get("about") == "budget"]
        self.assertIn(old, said[0]["text"])
        self.assertEqual(self.stopped(old)["stopped"], [])                  # said once

    def test_all_is_every_replaced_relay_and_never_the_running_one(self):
        first = self.new_relay_with_a_batch()
        second = self.new_relay_with_a_batch()
        third = self.new_relay_with_a_batch()
        self.assertTrue(self.loose(first) and self.loose(second))
        self.assertEqual(sorted(self.stopped("all")["stopped"]), sorted([first, second]))
        out = len([c for c in self.saved()["budget"]["calls"] if c[2:3] == ["out"]])
        self.next(third)
        self.assertEqual(self.loose(), [])
        self.assertGreater(out, 0)                                          # the running relay's batch was not touched

    def test_a_minute_full_of_held_calls_sends_nothing_and_says_so(self):
        rig = Rig()
        budget = rig.brain.budget
        budget.pace([K.act("B", "a", 1, 1, 1)] * C.CALL_LIMIT, "battle")
        budget.settle(holder="aa11bb-4")                                    # thirty calls of a relay that is gone
        rig.t += 500
        for lane, step in (("battle", K.act("B", "a", 1, 1, 2)), ("recovery", K.user()), ("world", K.user())):
            self.assertEqual(budget.pace([step], lane), ([], 0.0), lane)    # not sent, and not after a wait
        self.assertEqual(len(about(rig, "budget", "stall")), 3)
        out = rig.tick(user())
        self.assertEqual((rig.calls(out), out["hold"] >= C.RATE_BACKOFF), ([], True))   # the relay is not spun
        self.assertEqual(budget.ended("*", rig.t), C.CALL_LIMIT)            # the operator's word
        rig.t += 61
        self.assertEqual(len(budget.pace([K.user()], "recovery")[0]), 1)


class K2OnlyTheRelayABatchWasPrintedToCanSayItIsOver(Client):
    """A relay that had asked, and was replaced while it waited for its batch, never got one. Its token still
    carried the number of the batch another relay held, and coming back with it settled that relay's calls."""

    def test_a_relay_replaced_before_its_batch_was_printed(self):
        """The review's script (C2)."""
        a = self.new_relay_with_a_batch()
        b, cs = token_of(self.next()[0]), []                                # B replaces A

        def replaced_meanwhile(wait):
            if wait == C.HUNT_WAIT:
                cs.append(token_of(self.next()[0]))                         # and C replaces B, which is still waiting
        self.assertEqual(self.next(b, replaced_meanwhile), [brain.SUPERSEDED])
        n = len(self.loose(a))
        self.assertGreater(n, 0)
        self.assertEqual(self.next(b), [brain.SUPERSEDED])                  # B comes back: it never had a batch
        self.assertEqual(self.client()["ended"], [])                        # was: batch 1 reported over
        c = token_of(self.next(cs[-1])[-1])
        c = token_of(self.next(c)[-1])
        self.assertEqual(len(self.loose(a)), n)                             # was 0, and A has not come back
        self.assertEqual(self.next(a), [brain.SUPERSEDED])                  # A does
        self.next(c)
        self.assertEqual(self.loose(a), [])

    def test_what_is_held_is_what_was_printed(self):
        a = self.new_relay_with_a_batch()
        self.assertEqual(self.client()["held"]["token"], a)                 # printed to A: A holds it
        b = token_of(self.next()[0])
        state = self.client()
        self.assertEqual((state["held"], [g["token"] for g in state["gone"]]), (None, [a]))
        waiting = []
        self.next(b, lambda wait: waiting.append(self.client()["held"]) if wait == C.HUNT_WAIT else None)
        self.assertEqual(waiting, [None])                                   # asked, not printed yet: holds nothing
        self.assertEqual(self.client()["held"]["id"], self.saved()["budget"]["batch"])   # printed: the brain's batch

    def test_a_batch_that_grew_old_unprinted_is_held_for_nobody(self):
        a = self.new_relay_with_a_batch()

        class Killed(Exception):
            pass

        def dies_in_the_wait(wait):
            if wait == C.HUNT_WAIT:
                raise Killed
        with self.assertRaises(Killed):
            self.next(a, dies_in_the_wait)                                  # its next batch is made, and not printed
        unprinted = [c for c in self.saved()["budget"]["calls"] if c[2:3] == ["out"]]
        self.assertTrue(unprinted)
        state = self.client()
        state["pending"]["ready_at"] = time.time() - C.STALE_OUTBOX - 1
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        self.next(a)                                                        # it asks again; that batch is too old
        self.assertEqual(self.loose(), [])                                  # no relay had it: it is held for none,
        settled = [c for c in self.saved()["budget"]["calls"] if len(c) == 2]
        self.assertGreaterEqual(len(settled), len(unprinted))               # and counted from now all the same

    def test_a_client_file_from_before_is_read_without_trusting_it(self):
        a = self.new_relay_with_a_batch()
        state = self.client()
        state.update(gone=["dead01-1", {"token": "dead02-1"}, 7], held="x", ended=["y", [1]])
        relay.write(os.path.join(self.rig.dir, "client.json"), state)
        self.assertEqual(self.next("dead01-1"), [brain.SUPERSEDED])         # no batch of that shape was ever gone
        self.assertTrue(self.calls(self.next(a)))                           # and the relay that is running goes on
        self.assertEqual((self.client()["ended"], self.client()["gone"]), ([], []))


class K3AFailedTickIsOnDiskBeforeItIsAnswered(Client):
    """With no resident brain, `brain next` starts one for each request. A tick that failed was undone and
    counted in memory only: the next brain knew nothing of it, so every failure was the first."""

    def test_a_new_brain_for_every_request_still_reaches_the_last_resort(self):
        """The review's script (C3, the restart case)."""
        rig = Rig()
        battle, _, out = start_fight(rig)
        T, sent = rig.t, []
        rig.world["battle"]["inbox"] = dict(battle)
        rig.world.save()
        fight = type(rig.brain.reg.activities["battle"])
        with mock.patch.object(fight, "_absorb", side_effect=RuntimeError("persistent tick fault")):
            for seq, t in enumerate((1, 2, 12, 15, 20, 60), 100):
                rig.new_brain()
                sent.append(acts(ask(rig, seq, at=T + t, relay="offline")))
        line = [a["actionId"] for a in LINE]
        self.assertEqual(sent, [[], line, [], [], line, []])                # was: nothing, six times

    def test_what_the_failed_request_brought_and_its_receipt_survive(self):
        rig = Rig()
        rig.tick(user(sector=12))
        rig.world.save()
        with mock.patch.object(brain.Brain, "_decide", side_effect=RuntimeError("persistent tick fault")):
            ask(rig, 9, [user(sector=77)], at=rig.t + 1, relay="offline")
            rig.new_brain()
            self.assertEqual(rig.world.me["sector"], 77)                    # was 12
            self.assertEqual(rig.world["relay"]["answered"]["seq"], 9)      # was: no receipt
            seen, real = [], brain.Brain.handle
            with mock.patch.object(brain.Brain, "handle", lambda *a, **k: seen.append(1) or real(*a, **k)):
                again = ask(rig, 9, [user(sector=77)], at=rig.t + 1, relay="offline")
        self.assertEqual((seen, again["steps"]), ([], []))                  # and it is not run a second time

    def test_the_real_client_with_no_resident_brain(self):
        """The review's script (C3b): an overdue turn, a tick that fails on every read."""
        rig = self.rig
        rig.t = time.time() - 30
        battle, _, out = start_fight(rig)
        rig.world["battle"]["inbox"] = dict(battle)
        rig.world.save()
        with mock.patch.object(type(rig.brain.reg.activities["battle"]), "_absorb",
                               side_effect=RuntimeError("persistent tick fault")):
            token, seen = token_of(self.next()[0]), []
            for _ in range(2):
                rows = self.next(token)
                token = token_of(rows[-1])
                seen.append([json.loads(x)["input"]["actionId"] for x in rows if "performAction" in x])
        self.assertEqual(seen, [[], [a["actionId"] for a in LINE]])         # was: nothing, every time

    def test_a_save_that_fails_is_said_and_the_relay_still_gets_its_answer(self):
        rig = Rig()
        rig.tick(user())
        with mock.patch.object(brain.Brain, "_decide", side_effect=RuntimeError("tick fault")):
            with mock.patch.object(type(rig.world), "save", side_effect=OSError("disk")):
                out = ask(rig, 3, [user(sector=77)], at=rig.t + 1, relay="offline")
        self.assertEqual(out["steps"], [])
        with open(os.path.join(rig.dir, "crash.log")) as f:
            self.assertIn("could not be saved", f.read())


class K4AnAnswerThatIsNoObjectIsNoProof(unittest.TestCase):
    """false, 0, "", [] and nothing were turned into an empty object before they were looked at, and an empty
    object is what a taken action answers. The turn was closed as played, and nothing more was sent."""

    def turn(self, answer):
        """The review's script (C4): both actions of the plan answered with this, and then no read at all."""
        rig = Rig()
        _, _, out = start_fight(rig)
        T, sent = rig.t, []
        said = [res("combat.performAction", answer, inp=s["input"]) for s in out["steps"]
                if s.get("call") == "combat.performAction"]
        for t in (1, 12, 15, 20, 60):
            out = rig.tick(*(said if t == 1 else []), dt=T + t - rig.t)
            sent.append(acts(out))
        return rig, sent

    def test_an_empty_answer_of_any_other_kind(self):
        line = [a["actionId"] for a in LINE]
        for answer in (False, 0, "", [], None, "x", 7, [1], True):
            rig, sent = self.turn(answer)
            self.assertEqual(rig.world["battle"]["turn"]["accepted"], 0, repr(answer))    # was 2
            self.assertEqual(sent, [[], line, [], line, []], repr(answer))  # was: nothing more through T+60
            self.assertEqual(len(about(rig, "selects")), 1, repr(answer))   # and it is said, once a fight

    def test_an_object_is_still_an_answer(self):
        for answer in ({}, {"notification": None}, {"notification": ""}):
            rig, sent = self.turn(answer)
            self.assertEqual((rig.world["battle"]["turn"]["accepted"], sent), (2, [[], [], [], [], []]), answer)
            self.assertEqual(about(rig, "selects"), [])


class K5ARequestAndItsAnswerAreOnePair(Client):
    """Requests and answers were files named by a number alone. A replacement could ask under the number an
    older request was still being answered under: it then printed the older relay's batch, its own request was
    deleted unread, and the evidence it carried was dropped as if the brain had had it."""

    def test_an_old_brains_late_answer_and_the_replacements_own_request(self):
        """The review's script (C5), with threads for its processes: a resident brain is answering a request
        whose `brain next` then dies; a replacement asks under the same number, bringing word that a held batch
        is over; then the resident writes its answer."""
        holder = self.new_relay_with_a_batch()
        a = token_of(self.next()[0])                                        # A replaces the holder
        asked, die, ready, release, new_asked, is_home = (threading.Event() for _ in range(6))
        real_write, printed = relay.write, {}

        class Killed(Exception):
            pass

        def resident():
            lock = brain._lock(self.rig.dir)                                # a brain is home: it answers
            is_home.set()
            asked.wait(5)
            path = relay.pending_requests(self.rig.dir)[0]
            brain.answer(brain.Brain(self.rig.dir), self.rig.dir, path)
            lock.close()

        def write(path, obj):
            if threading.current_thread() is home and os.sep + "outbox" + os.sep in path:
                ready.set()                                                 # the answer is made, and not yet written
                release.wait(5)
            return real_write(path, obj)

        def old_client():
            def sleep(wait):
                if wait == C.BRAIN_WAIT:                                    # it has asked, and waits for the brain
                    asked.set()
                    die.wait(5)
                    raise Killed                                            # the `brain next` that asked dies
            with self.assertRaises(Killed):
                self.next(a, sleep)

        def new_client(token):
            def sleep(wait):
                if wait == C.BRAIN_WAIT:
                    new_asked.set()
                    time.sleep(0.01)
            printed["new"] = self.next(token, sleep)
        home, old = threading.Thread(target=resident), threading.Thread(target=old_client)
        with mock.patch.object(relay, "write", write):
            home.start()
            self.assertTrue(is_home.wait(5))
            old.start()
            self.assertTrue(ready.wait(5))
            die.set()
            old.join(5)
            b = token_of(self.next()[0])                                    # B replaces A
            self.assertEqual(self.next(holder), [brain.SUPERSEDED])         # the holder comes back: its batch is over
            self.assertEqual(len(self.client()["ended"]), 1)
            real_write(os.path.join(self.rig.dir, "control.json"), {"version": 1, "mode": "guard"})
            new = threading.Thread(target=new_client, args=(b,))
            new.start()
            self.assertTrue(new_asked.wait(5))                              # B's request is in, under A's number
            release.set()                                                   # and now the old answer is written
            home.join(5)
            new.join(5)
        self.assertEqual(self.calls(printed["new"]), ["profile.getUser"])   # was: A's batch, a hunt's reads
        self.assertEqual(self.saved()["relay"]["answered"]["relay"], b.split("-")[0])   # was A's
        self.assertEqual(self.client()["ended"], [])                        # handed to the brain,
        self.assertEqual(self.loose(holder), [])                            # which took it in. Was: still loose
        self.assertEqual(relay.pending_requests(self.rig.dir), [])

    def test_a_request_left_by_a_client_that_died_is_not_answered_late(self):
        a = self.new_relay_with_a_batch()
        with mock.patch.object(brain, "_await", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                self.next(a)                                                # dies with its request written
        self.assertEqual(len(relay.pending_requests(self.rig.dir)), 1)
        receipt = self.saved()["relay"]["answered"]
        self.next(token_of(self.next()[0]))                                 # a replacement asks
        self.assertEqual(relay.pending_requests(self.rig.dir), [])          # the dead one's request is gone
        brain.run(self.rig.dir, forever=False)                              # and a brain that comes home later
        self.assertNotEqual(self.saved()["relay"]["answered"], receipt)     # has only the replacement's on record
        self.assertEqual(self.saved()["relay"]["answered"]["relay"], self.client()["relay"])

    def test_word_that_a_batch_is_over_is_taken_from_a_request_answered_from_its_receipt(self):
        """A `brain next` dies with the brain's answer unwritten; before the relay asks again, a replaced relay
        comes back. The second request is answered from the receipt, and still brings that word."""
        held = self.new_relay_with_a_batch()
        runner = self.new_relay_with_a_batch()
        real = relay.write

        class Killed(Exception):
            pass

        def dying(path, obj):
            if path == os.path.join(self.rig.dir, "client.json") and obj.get("pending"):
                raise Killed
            return real(path, obj)
        with mock.patch.object(relay, "write", dying):
            with self.assertRaises(Killed):
                self.next(runner)
        self.assertEqual(self.next(held), [brain.SUPERSEDED])               # meanwhile the replaced relay is back
        seen, handle = [], brain.Brain.handle
        with mock.patch.object(brain.Brain, "handle", lambda *a, **k: seen.append(1) or handle(*a, **k)):
            self.next(runner)                                               # the same request again
        self.assertEqual((seen, self.loose(held), self.client()["ended"]), ([], [], []))

    def test_an_answer_is_read_only_by_the_request_it_names(self):
        self.next()
        asked, real = [], relay.write

        def write(path, obj):
            wrote = real(path, obj)
            if os.sep + "inbox" + os.sep + "req-" in path:
                asked.append(obj)                                           # the request is in. Before the brain
                if len(asked) == 2:                                         # answers the second one, a file turns
                    real(relay.batch_path(self.rig.dir, obj["seq"], obj["id"]), {   # up in its answer's place
                        "seq": obj["seq"], "request": "another", "stop": None, "hold": 0.0,
                        "steps": [{"call": "not.this", "input": {}, "select": []}]})
            return wrote
        with mock.patch.object(relay, "write", write):
            first = self.next(self.client()["token"])
            second = self.next(self.client()["token"])
        self.assertEqual(len({r["id"] for r in asked}), 2)                  # every request has an id of its own
        self.assertEqual(self.saved()["relay"]["answered"]["id"], asked[1]["id"])
        self.assertTrue(self.calls(first))
        self.assertNotIn("not.this", self.calls(second))                    # an answer that names another request
        self.assertTrue(self.calls(second))                                 # is not taken; the brain's own is


class K6NothingIsSentIntoAFightMyProfileHasLeft(unittest.TestCase):
    """A profile said the fight was over, but its archive failed, so it stayed open. The second failure's last
    resort then sent a Defensive Stance into it, from its old read."""

    def test_an_archive_that_fails_does_not_keep_the_fight_open(self):
        """The review's script (C3, the closure case)."""
        rig = Rig()
        _, _, out = start_fight(rig)
        with mock.patch.object(rig.combat, "close_fight", side_effect=RuntimeError("archive unavailable")):
            one = ask(rig, 1, answers(out, NOT_VALID) + [user("AWAKE")], at=rig.t + 1, relay="offline")
            two = ask(rig, 2, at=rig.t + 1, relay="offline")
        self.assertEqual((acts(one), acts(two)), ([], []))                  # was: [], then a stance into B1
        self.assertIsNone(rig.world["battle"])                              # the fight is closed all the same
        with open(os.path.join(rig.dir, "unarchived-B1.json")) as f:
            self.assertEqual(json.loads(f.readline())["bid"], "B1")         # and its state is kept for Duet
        self.assertEqual([e["about"] for e in rig.events("error")], ["crash"])

    def test_a_fight_that_cannot_be_closed_at_all_is_still_not_acted_on(self):
        for profile in (user("AWAKE"), user("HOSPITALIZED"), user("BATTLE", bid="B2")):
            rig = Rig()
            battle, _, out = start_fight(rig)
            fight = type(rig.brain.reg.activities["battle"])
            with mock.patch.object(fight, "_close", side_effect=RuntimeError("cannot close")):
                one = ask(rig, 1, answers(out, NOT_VALID) + [profile, battle_read("B1", battle)], at=rig.t + 1)
                two = ask(rig, 2, at=rig.t + 1)
                three = ask(rig, 3, [battle_read("B1", battle)], at=rig.t + 1)
            status = profile.data["userData.status"]
            self.assertEqual([acts(x) for x in (one, two, three)], [[], [], []], status)
            self.assertEqual([s["call"] for s in two["steps"]], ["profile.getUser"], status)

    def test_a_fight_my_profile_is_still_in_gets_its_last_resort(self):
        rig = Rig()
        battle, _, out = start_fight(rig)
        fight = type(rig.brain.reg.activities["battle"])
        with mock.patch.object(fight, "_absorb", side_effect=RuntimeError("tick fault")):
            ask(rig, 1, answers(out, NOT_VALID) + [user("BATTLE", bid="B1"), battle_read("B1", battle)], at=rig.t + 1)
            two = ask(rig, 2, at=rig.t + 1)
        self.assertEqual(acts(two), ["defensiveStance"])


if __name__ == "__main__":
    unittest.main()
