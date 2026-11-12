"""The brain since its split (player/brain/ was the one file player/brain.py until e4a267cd). The split moved
code and changed no behaviour, and every test that was there runs as it was. These are for what the split itself
has to keep: the command line, every name the file had, and the five places where the pieces meet.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

from player import brain, config as C, relay
from player.tests.support import res
from player.tests.test_relay import token_of
from player.tests.test_rereview6 import calls_of

NAMES = """
    BLOCK_FOR Brain Budget C CLASSES Combat Gates IDLE_HOLD QUIET RATE_LIMITED REQUEST RETRY_IN SUPERSEDED
    UPDATE World _a_batch _a_relay _a_waiting_batch _a_word _after_crash _answered _await _client _collect
    _crashed _exchange _greet _held _lead _lock _owed _setting _sweep _taken _transcript _who _wire answer
    console contextlib fcntl found glob json main next_batch os put registry relay run serve stopped subprocess
    sys time traceback
""".split()
"""Every name player/brain.py had at e4a267cd, the names it imported among them: tests and the reviews' scripts
reach for them in `player.brain`, and one script runs code of its own in that namespace."""


class TheCommandLine(unittest.TestCase):
    """`python3 -m player.brain ...`, in processes of their own."""

    def setUp(self):
        self.live = tempfile.mkdtemp(prefix="player-cli-")
        self.env = {**os.environ, "PYTHONPATH": C.ROOT, "TNR_PLAYER_LIVE": self.live, "TNR_PLAYER_NO_DAEMON": "1",
                    "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                    "TNR_PLAYER_FIGHTS": os.path.join(self.live, "fights")}
        self.command = [sys.executable, "-W", "ignore", "-m", "player.brain"]

    def says(self, *args):
        done = subprocess.run(self.command + list(args), cwd=C.ROOT, env=self.env, capture_output=True, text=True,
                              timeout=120)
        return done.returncode, done.stdout, done.stderr

    def test_it_runs_as_a_module_and_says_how_it_is_used(self):
        self.assertEqual(self.says(), (0, "null\n", ""))                    # no command: the status, and none yet
        code, out, usage = self.says("no-such-command")
        self.assertEqual((code, out), (2, ""))
        lines = usage.splitlines()
        self.assertEqual([x.split()[:4] for x in lines],
                         [["python3", "-m", "player.brain", w] for w in ("run", "next", "put", "set", "stopped", "status")])
        code, out, _ = self.says("set", "paused=true")
        self.assertEqual((code, json.loads(out)["paused"]), (0, True))
        self.assertEqual(json.loads(self.says("stopped")[1])["still_held"], [])

    def test_the_resident_process_answers_a_relay_and_is_the_only_one(self):
        home = subprocess.Popen(self.command + ["run"], cwd=C.ROOT, env=self.env, stdout=subprocess.DEVNULL,
                                stderr=subprocess.PIPE, text=True)
        self.addCleanup(home.stderr.close)
        self.addCleanup(lambda: home.poll() is None and (home.kill(), home.wait()))
        until = time.monotonic() + 20
        while time.monotonic() < until and not os.path.exists(os.path.join(self.live, "brain.lock")):
            time.sleep(0.05)
        time.sleep(0.2)
        self.assertIsNone(brain._lock(self.live))                           # it is home: the lock is its own
        with open(f"/proc/{home.pid}/cmdline", encoding="utf8") as f:      # and the operator's page finds it:
            self.assertIn("player.brain\0run", f.read())                    # pgrep -f "player.brain run"
        self.assertEqual(self.says("run")[0], 1)                            # a second one ends at once
        out = io.StringIO()
        with mock.patch.dict(os.environ, self.env), \
                mock.patch.object(brain, "Brain", side_effect=AssertionError("answered here, not by the resident")):
            brain.next_batch(self.live, None, out)
            token = token_of(out.getvalue().splitlines()[0])
            brain.next_batch(self.live, token, out, lambda t: time.sleep(min(t, 0.05)))
        self.assertEqual(calls_of(out.getvalue().splitlines())[:1], ["profile.getUser"])   # its batch, over the files
        self.assertTrue(relay.ours(relay.read(os.path.join(self.live, "world.json"))["budget"]))
        self.assertIsNone(home.poll())
        home.terminate()
        self.assertEqual(home.wait(timeout=20), -15)
        self.assertEqual(home.stderr.read(), "")


class WhatTheFileHadThePackageHas(unittest.TestCase):
    def test_every_name(self):
        self.assertEqual([n for n in NAMES if not hasattr(brain, n)], [])
        self.assertEqual(len(NAMES), 57)
        self.assertEqual({brain.Brain.__module__, brain.serve.__module__, brain.next_batch.__module__},
                         {"player.brain.core", "player.brain.resident", "player.brain.client"})


class ThePiecesMeetInThePackage(unittest.TestCase):
    """Brain, serve, answer, _lock and _await are looked up in player.brain each time they are called, as they
    were when all of it was one file: what a test puts there in their place is what is used."""

    def setUp(self):
        self.live = tempfile.mkdtemp(prefix="player-seams-")
        os.makedirs(os.path.join(self.live, "inbox"))
        env = mock.patch.dict(os.environ, {"TNR_PLAYER_NO_DAEMON": "1", "TNR_PLAYER_LIVE": self.live,
                                           "TNR_TRANSCRIPT": os.path.join(self.live, "none"),
                                           "TNR_PLAYER_FIGHTS": os.path.join(self.live, "fights")})
        env.start()
        self.addCleanup(env.stop)

    def a_request(self):
        path = relay.request_path(self.live, 1, "ab" * 4)
        relay.write(path, {"protocol": relay.PROTOCOL, "seq": 1, "id": "ab" * 4, "relay": "r1", "results": [],
                           "held": None, "gone": [], "ended": [], "unprinted": []})
        return path

    def test_the_resident_loop(self):
        path, seen = self.a_request(), []
        made = mock.Mock(name="a brain")
        with mock.patch.object(brain, "Brain", return_value=made) as starts, \
                mock.patch.object(brain, "serve", side_effect=lambda *a: seen.append(a)):
            self.assertEqual(brain.run(self.live, forever=False), 0)
        self.assertEqual((starts.call_args.args, seen), ((self.live,), [(made, self.live, path)]))
        with mock.patch.object(brain, "_lock", return_value=None), mock.patch.object(brain, "Brain") as starts:
            self.assertEqual(brain.run(self.live, forever=False), 1)        # somebody else is home
        self.assertFalse(starts.called)

    def test_a_request_goes_from_serve_to_answer(self):
        path, made = self.a_request(), mock.Mock(name="a brain")
        with mock.patch.object(brain, "answer", return_value="answered") as answers:
            self.assertEqual(brain.serve(made, self.live, path), "answered")
        self.assertEqual(answers.call_args.args, (made, self.live, path))

    def test_brain_next_asks_through_await_and_await_answers_through_serve(self):
        out = io.StringIO()
        brain.next_batch(self.live, None, out)
        token = token_of(out.getvalue().splitlines()[0])
        with mock.patch.object(brain, "_await", return_value=None) as waits:
            brain.next_batch(self.live, token, out, lambda _: None)
        self.assertEqual(waits.call_args.args[:2], (self.live, 1))
        seen, made, req = [], mock.Mock(name="a brain"), self.a_request()

        def serve(*a):
            seen.append(a)
            os.unlink(a[2])                                                 # (the request is taken, as serve does)
        with mock.patch.object(brain, "Brain", return_value=made), mock.patch.object(brain, "serve", serve):
            self.assertIsNone(brain._await(self.live, 1, "ab" * 4, req, lambda _: None, limit=0.2))
        self.assertEqual(seen, [(made, self.live, req)])                    # nobody home: answered here, once
        with mock.patch.object(brain, "_lock", return_value=None) as locks, mock.patch.object(brain, "Brain") as starts:
            self.assertIsNone(brain._await(self.live, 9, "cd" * 4, "nowhere", lambda _: None, limit=0.2))
        self.assertTrue(locks.called and not starts.called)                 # nobody answers here while one is home


if __name__ == "__main__":
    unittest.main()
