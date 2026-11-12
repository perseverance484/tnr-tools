"""The run lock in the brain (director 2026-11-12, RUL-2026-11-12-154: "Give it to the brain then").

The lock is one writer on the account at a time (docs/workflows/FORGE_MCP_RUNNER.md). The brain claims it as
`player` before a session's first call, sends no call without it, renews it, and gives it back when the session
is over. A brain that is not on the account's own live folder is a rehearsal and claims nothing: every other test
in this package is one.

The first classes script the lock tool. The last runs the real forge/tools/run_lock.mjs against a repository made
for the test in a temporary folder: no network, and never the real `main`.
"""
import datetime as dt
import json
import os
import shutil
import subprocess
import tempfile
import types
import unittest
from unittest import mock

from player import calls as K, config as C, relay, runlock
from player.tests.support import Rig, user


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


class ScriptedTool:
    """forge/tools/run_lock.mjs as a test wants it: what it says, and everything it was asked."""

    def __init__(self, rig):
        self.rig, self.asked, self.other, self.token, self.broken, self.n = rig, [], None, None, None, 0

    def claim(self, instance):
        self.asked.append(("claim", instance))
        if self.broken:
            return {"type": "error", "text": self.broken}
        if self.other:
            return {"type": "refused", "waitMs": 425_000,
                    "text": f"the run lock is held by {self.other} (push/502) for up to {7 + len(self.asked)} more minute(s)"}
        self.n += 1
        self.token = f"token-{self.n}"
        return {"type": "claimed", "holder": "player", "job": "play session", "token": self.token,
                "expiresAt": iso(self.rig.t + 3600)}

    def heartbeat(self, token):
        self.asked.append(("heartbeat", token))
        if self.broken:
            return {"type": "error", "text": self.broken}
        if token != self.token:
            return {"type": "refused", "text": f"this claim no longer holds the run lock ({self.other} does)"}
        return {"type": "heartbeat", "holder": "player", "expiresAt": iso(self.rig.t + 3600)}

    def release(self, token):
        self.asked.append(("release", token))
        mine, self.token = token == self.token, None if token == self.token else self.token
        return {"type": "released", "already": not mine, "commit": "0" * 40}


def on_the_accounts_folder(rig, tool=None):
    """The rig's brain, holding the lock the way the brain of the account's own live folder does."""
    tool = tool or ScriptedTool(rig)
    rig.brain.lock = runlock.RunLock(rig.world, tool=tool, rehearsal=False)
    return tool


class WhoHoldsTheLock(unittest.TestCase):
    def test_only_the_brain_of_the_accounts_own_live_folder(self):
        own = os.path.join(C.ACCOUNT_DIR, "live")
        self.assertTrue(runlock.own_folder(own))
        self.assertIs(runlock.RunLock(types.SimpleNamespace(live=own)).rehearsal, False)
        rig = Rig()
        self.assertFalse(runlock.own_folder(rig.dir))
        self.assertIs(rig.brain.lock.rehearsal, True)                       # as every brain in these tests is

    def test_a_rehearsal_plays_as_before_and_never_runs_the_tool(self):
        rig = Rig()
        with mock.patch.object(runlock.subprocess, "run", side_effect=AssertionError("the lock tool was run")):
            out = rig.tick(user())
            self.assertTrue(rig.calls(out))
            rig.world["control"]["paused"] = True
            rig.tick(user())
        self.assertIn("rehearsal", rig.status()["run_lock"]["state"])
        self.assertNotIn("run_lock", rig.world["records"])


class TheBrainHoldsTheRunLock(unittest.TestCase):
    def test_no_call_goes_until_the_lock_is_the_brains(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        tool.other = "duet"                                                 # a content job is running
        out = rig.tick(user())
        self.assertEqual(rig.calls(out), [])                                # not even a read of my profile
        self.assertTrue(1.0 <= out["hold"] <= 30.0)
        self.assertIn("held by duet (push/502)", out["note"])
        self.assertEqual(tool.asked, [("claim", os.path.realpath(rig.dir))])   # as this brain's own instance
        for _ in range(5):
            self.assertEqual(rig.calls(rig.tick(user(), dt=5)), [])
        self.assertEqual(len(tool.asked), 1)                                # the tool is not asked at every tick,
        rig.t += runlock.ASK_AGAIN[1]
        self.assertEqual(rig.calls(rig.tick(user())), [])
        self.assertEqual(len(tool.asked), 2)                                # a minute on it is,
        said = [e["text"] for e in rig.events("stall") if "run lock" in e["text"]]
        self.assertEqual(len(said), 1)                                      # and the wait is said once
        self.assertIn("No call is sent", said[0])
        self.assertEqual(rig.status()["run_lock"]["state"], "not held")
        tool.other = None                                                   # the job is done
        rig.t += runlock.ASK_AGAIN[1]
        out = rig.tick(user())
        self.assertTrue(rig.calls(out))
        self.assertIn("session: the run lock is claimed as player", [e["text"] for e in rig.events("activity_done")])

    def test_the_token_is_kept_in_the_world_model_and_never_in_the_status(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        rig.world.save()
        self.assertEqual(rig.world["records"]["run_lock"]["token"], tool.token)
        with open(os.path.join(rig.dir, "status.json"), encoding="utf8") as f:
            status = f.read()
        self.assertNotIn(tool.token, status)
        self.assertEqual(json.loads(status)["run_lock"]["state"], "held")
        rig.new_brain()                                                     # a restart goes on with the claim
        on_the_accounts_folder(rig, tool)
        self.assertTrue(rig.calls(rig.tick(user())))
        self.assertEqual([a[0] for a in tool.asked], ["claim"])

    def test_the_claim_is_renewed_and_a_fight_puts_that_off_until_the_lease_is_short(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        rig.t += runlock.RENEW_EVERY - 5
        rig.tick(user())
        self.assertEqual([a[0] for a in tool.asked], ["claim"])
        rig.t += 10
        self.assertTrue(rig.calls(rig.tick(user())))
        self.assertEqual(tool.asked[-1], ("heartbeat", tool.token))
        self.assertGreater(rig.world["records"]["run_lock"]["expires"], rig.t + 3500)
        lock, n = rig.brain.lock, len(tool.asked)
        rig.t += runlock.RENEW_EVERY + 1                                    # due again, with 45 minutes of lease left:
        self.assertIsNone(lock.hold(in_battle=True))
        self.assertEqual(len(tool.asked), n)                                # not in the middle of a fight
        rig.t = rig.world["records"]["run_lock"]["expires"] - runlock.RENEW_NOW + 1
        self.assertIsNone(lock.hold(in_battle=True))
        self.assertEqual(len(tool.asked), n + 1)                            # under ten minutes left: now

    def test_a_lock_that_was_taken_stops_every_call_at_once(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        tool.token, tool.other = "somebody-elses", "duet"                   # the lease was lost, and claimed
        rig.t += runlock.RENEW_EVERY + 1
        out = rig.tick(user())
        self.assertEqual(rig.calls(out), [])
        self.assertEqual([a[0] for a in tool.asked], ["claim", "heartbeat", "claim"])
        self.assertTrue(any("the run lock is lost" in e["text"] for e in rig.events("stall")))
        self.assertNotIn("token", rig.world["records"]["run_lock"])

    def test_a_renewal_that_fails_plays_on_until_a_minute_before_the_lease_ends(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        ends = rig.world["records"]["run_lock"]["expires"]
        tool.broken = "could not push the lock after 4 attempts"
        rig.t += runlock.RENEW_EVERY + 1
        self.assertTrue(rig.calls(rig.tick(user())))                        # the lease is still good
        self.assertTrue(any("could not be renewed" in e["text"] for e in rig.events("error")))
        tries = len(tool.asked)
        self.assertTrue(rig.calls(rig.tick(user(), dt=20)))
        self.assertEqual(len(tool.asked), tries)                            # tried again a minute later, not at once
        rig.t = ends - runlock.STOP_MARGIN - 30
        self.assertTrue(rig.calls(rig.tick(user())))
        rig.t = ends - runlock.STOP_MARGIN + 1
        self.assertEqual(rig.calls(rig.tick(user())), [])                   # the last confirmed expiry is the limit
        self.assertEqual(rig.world["records"]["run_lock"]["expires"], ends)

    def test_no_path_sends_a_call_without_it(self):
        """Every batch is paced in one place (Brain._paced), the last resort's too: that place asks as well."""
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        tool.other = "duet"
        steps, hold, _ = rig.brain._paced([K.user(), K.wait(2), K.user()], "battle", 0.0)
        self.assertEqual(([s for s in steps if "call" in s], hold >= C.RATE_BACKOFF), ([], True))
        self.assertEqual(rig.world["budget"]["calls"], [])                  # and nothing is counted as sent

    def test_the_lock_goes_back_when_the_session_is_over_or_paused_and_not_for_a_new_relay(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        with mock.patch.object(relay, "should_rotate", return_value=True):
            self.assertTrue(rig.tick(user())["stop"].startswith("rotate"))  # a fresh relay: the session goes on
        self.assertEqual([a[0] for a in tool.asked], ["claim"])
        rig.world["control"]["end_session"] = True
        out = rig.tick(user("ASLEEP", sector=C.HOME_SECTOR))
        self.assertIn("asleep at home", out["stop"])
        self.assertEqual(tool.asked[-1], ("release", "token-1"))
        rig.tick(user("ASLEEP", sector=C.HOME_SECTOR))
        self.assertEqual([a[0] for a in tool.asked], ["claim", "release"])  # once
        self.assertIn("session: the run lock is released", [e["text"] for e in rig.events("activity_done")])
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        rig.world["control"]["paused"] = True                               # the director pauses the player
        self.assertEqual(rig.calls(rig.tick(user())), [])
        self.assertEqual([a[0] for a in tool.asked], ["claim", "release"])
        rig.world["control"]["paused"] = False
        self.assertTrue(rig.calls(rig.tick(user())))                        # and it claims again to go on
        self.assertEqual([a[0] for a in tool.asked], ["claim", "release", "claim"])


@unittest.skipUnless(shutil.which("node") and shutil.which("git"), "the lock tool needs node and git")
class TheRealTool(unittest.TestCase):
    """forge/tools/run_lock.mjs itself, pushing to a repository that exists only for this test."""

    def setUp(self):
        self.top = tempfile.mkdtemp(prefix="player-runlock-")
        self.origin, self.work = os.path.join(self.top, "origin.git"), os.path.join(self.top, "work")
        who = {"GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@example.invalid",
               "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@example.invalid"}
        self.env = {**who, "RUN_LOCK_REPO": self.work}

        def git(*args, cwd=self.work):
            return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True,
                                  env={**os.environ, **who}).stdout
        self.git = git
        git("init", "-q", "--bare", "-b", "main", self.origin, cwd=self.top)
        git("clone", "-q", self.origin, self.work, cwd=self.top)
        os.makedirs(os.path.join(self.work, "state"))
        with open(os.path.join(self.work, "state", "run_lock.json"), "w", encoding="utf8") as f:
            json.dump({"holder": None, "token": None, "job": None}, f)
        git("add", "-A")
        git("commit", "-q", "-m", "a lock that is free")
        git("push", "-q", "origin", "HEAD:main")

    def log(self):
        return self.git("log", "--format=%s", "main", cwd=self.origin).strip().split("\n")

    def test_claim_renew_release_and_what_a_second_runner_is_told(self):
        mine, other = runlock.Tool(env=self.env), runlock.Tool(env=self.env)
        said = mine.claim("the-brains-live-folder")
        self.assertEqual((said["type"], said["holder"], said["job"]), ("claimed", "player", "play session"))
        self.assertGreater(runlock._epoch(said["expiresAt"]), dt.datetime.now(dt.timezone.utc).timestamp() + 3000)
        refused = other.claim("another-runner")
        self.assertEqual(refused["type"], "refused")
        self.assertIn("held by player (play session)", refused["text"])
        self.assertGreater(refused["waitMs"], 0)
        self.assertEqual(mine.heartbeat(said["token"])["type"], "heartbeat")
        self.assertEqual(other.heartbeat("not-the-token")["type"], "refused")
        self.assertEqual(mine.release(said["token"]), {"type": "released", "already": False,
                                                       "commit": self.git("rev-parse", "main", cwd=self.origin).strip()})
        quiet = other.claim("another-runner")                               # the rolling minute is still the brain's
        self.assertEqual(quiet["type"], "refused")
        self.assertIn("less than a minute ago", quiet["text"])
        again = mine.claim("the-brains-live-folder")                        # the same instance need not wait
        self.assertEqual(again["type"], "claimed")
        mine.release(again["token"])
        self.assertEqual(self.log()[:5][::-1], ["run-lock: claim by player (play session)", "run-lock: heartbeat by player",
                                                "run-lock: release by player", "run-lock: claim by player (play session)",
                                                "run-lock: release by player"])

    def test_a_tool_that_cannot_reach_the_repository_says_so_and_claims_nothing(self):
        said = runlock.Tool(env={**self.env, "RUN_LOCK_REPO": os.path.join(self.top, "nowhere")}).claim("x")
        self.assertEqual(said["type"], "error")
        self.assertEqual(self.log(), ["a lock that is free"])

    def test_a_session_of_the_brain_from_its_first_call_to_asleep(self):
        rig = Rig()
        on_the_accounts_folder(rig, runlock.Tool(env=self.env))
        real = dt.datetime.now(dt.timezone.utc).timestamp()
        rig.t = real                                                        # the lease is on the tool's clock
        self.assertTrue(rig.calls(rig.tick(user())))
        held = json.loads(self.git("show", "main:state/run_lock.json", cwd=self.origin))
        self.assertEqual((held["holder"], held["job"], held["instance"]), ("player", "play session", os.path.realpath(rig.dir)))
        self.assertEqual(held["token"], rig.world["records"]["run_lock"]["token"])
        rig.world["control"]["end_session"] = True
        self.assertIn("asleep at home", rig.tick(user("ASLEEP", sector=C.HOME_SECTOR))["stop"])
        free = json.loads(self.git("show", "main:state/run_lock.json", cwd=self.origin))
        self.assertEqual((free["holder"], free["token"], free["releasedBy"]), (None, None, "player"))
        self.assertEqual(self.log()[:2], ["run-lock: release by player", "run-lock: claim by player (play session)"])


if __name__ == "__main__":
    unittest.main()
