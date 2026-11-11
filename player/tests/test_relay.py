"""The hands: the relay contract, results from the relay's transcript, tokens and rotation, the next/put client."""
import io
import json
import os
import re
import subprocess
import sys
import time
import unittest

from player import brain, config as C, relay
from player.tests.support import Rig, user


def transcript(path, rows):
    """rows: ("use", id, endpoint, input, t) | ("res", id, text, t[, is_error]) | ("bash", id, command, t) |
    ("usage", request id, in, cache_read, out, t)."""
    out = []
    for r in rows:
        ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(r[-1] if r[0] != "res" or len(r) == 4 else r[3])) + "Z"
        if r[0] == "use":
            out.append({"timestamp": ts, "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": r[1], "name": "mcp__Tnr__callEndpoint",
                 "input": {"endpointName": r[2], "input": r[3], "select": []}}]}})
        elif r[0] == "bash":
            out.append({"timestamp": ts, "message": {"role": "assistant", "content": [
                {"type": "tool_use", "id": r[1], "name": "Bash", "input": {"command": r[2]}}]}})
        elif r[0] == "res":
            out.append({"timestamp": ts, "message": {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": r[1], "is_error": len(r) > 4 and r[4],
                 "content": [{"type": "text", "text": r[2]}]}]}})
        else:
            out.append({"timestamp": ts, "requestId": r[1], "message": {"role": "assistant", "content": [], "usage": {
                "input_tokens": r[2], "cache_read_input_tokens": r[3], "cache_creation_input_tokens": 0,
                "output_tokens": r[4]}}})
    with open(path, "w", encoding="utf8") as f:
        f.write("\n".join(json.dumps(x) for x in out) + "\n")


class Contract(unittest.TestCase):
    def test_the_relay_prompt_is_short_and_says_the_loop(self):
        with open(os.path.join(C.ROOT, "player", "RELAY.md"), encoding="utf8") as f:
            text = f.read()
        self.assertLess(len(text.split()), 300)
        for must in ("brain next", "callEndpoint", "in order", "ONE message", "STOP", "no decisions"):
            self.assertIn(must, text)

    def test_a_batch_is_calls_waits_and_the_next_tick_and_nothing_else(self):
        rig = Rig()
        out = rig.tick(user())
        lines = [json.loads(x) for x in relay.lines(out["steps"] + [{"wait": 1.2}])]
        for row in lines[:-1]:
            self.assertTrue(set(row) == {"call", "input", "select"} or
                            re.fullmatch(r"python3 -c 'import time; time\.sleep\([\d.]+\)'", row.get("bash", "")), row)
        self.assertTrue(lines[-1]["bash"].endswith("python3 -m player.brain next"))
        self.assertNotIn("meta", json.dumps(lines))                        # what the gates read stays in the brain
        self.assertEqual(relay.lines([], "asleep"), ["STOP asleep"])

    def test_every_call_has_a_select(self):
        rig = Rig()
        for out in (rig.tick(user()), rig.tick(user("BATTLE", bid="B1")), rig.tick(user("HOSPITALIZED"))):
            for s in out["steps"]:
                if "call" in s:
                    self.assertTrue(s["select"], s["call"])


class Transcript(unittest.TestCase):
    def test_results_come_back_in_order_with_refusals_and_errors_marked(self):
        rig = Rig()
        p = os.path.join(rig.dir, "t.jsonl")
        transcript(p, [
            ("use", "a", "profile.getUser", {}, 90), ("res", "a", '{"userData.status":"AWAKE"}', 90),      # an older batch
            ("use", "b", "profile.getUser", {}, 101), ("res", "b", '{"userData.status":"BATTLE"}', 101),
            ("use", "c", "combat.getBattle", {"battleId": "B"}, 102),
            ("res", "c", "Error POSTing to endpoint: Too Many Requests", 102),
            ("use", "d", "combat.performAction", {"battleId": "B"}, 103),
            ("res", "d", "Error calling combat.performAction: Not your turn", 103),
            ("use", "e", "item.consume", {}, 104), ("res", "e", "not json", 104),
            ("usage", "r1", 10, 60_000, 50, 101), ("usage", "r1", 10, 60_000, 50, 102), ("usage", "r2", 5, 61_000, 40, 104)])
        results, usage = relay.read_results(p, 100)
        self.assertEqual([r.endpoint for r in results],
                         ["profile.getUser", "combat.getBattle", "combat.performAction", "item.consume"])
        self.assertEqual(results[0].data, {"userData.status": "BATTLE"})
        self.assertEqual(results[1].error, "rate_limited")
        self.assertIn("Not your turn", results[2].error)
        self.assertIn("unreadable", results[3].error)
        self.assertEqual(usage, {"in": 60_010 + 61_005, "out": 90, "context": 61_005})   # a request counted once

    def test_a_result_too_large_for_the_conversation_is_read_from_its_file(self):
        rig = Rig()
        p = os.path.join(rig.dir, "t.jsonl")
        saved = os.path.join(rig.dir, "big.json")
        with open(saved, "w") as f:
            json.dump([{"type": "text", "text": '{"battle.version": 7}'}], f)
        notice = f"<persisted-output>\nOutput too large (55.7KB). Full output saved to: {saved}\n\nPreview..."
        transcript(p, [("use", "a", "combat.getBattle", {"battleId": "B"}, 101), ("res", "a", notice, 101)])
        results, _ = relay.read_results(p, 100)
        self.assertEqual(results[0].data, {"battle.version": 7})
        outside = notice.replace(saved, "/etc/hostname.json")
        transcript(p, [("use", "a", "combat.getBattle", {"battleId": "B"}, 101), ("res", "a", outside, 101)])
        self.assertIn("unreadable", relay.read_results(p, 100)[0][0].error)

    def test_the_relay_is_the_transcript_whose_last_call_is_brain_next(self):
        rig = Rig()
        home = os.path.join(rig.dir, "claude")
        os.makedirs(os.path.join(home, "projects", "x", "subagents"))
        sup = os.path.join(home, "projects", "x", "main.jsonl")
        rel = os.path.join(home, "projects", "x", "subagents", "agent-1.jsonl")
        transcript(rel, [("bash", "n", "cd /repo && python3 -m player.brain next", time.time())])
        transcript(sup, [("bash", "s", "git status", time.time())])           # written later: newest file
        os.environ["CLAUDE_CONFIG_DIR"] = home
        try:
            self.assertEqual(relay.find_transcript(), rel)
        finally:
            del os.environ["CLAUDE_CONFIG_DIR"]


class Tokens(unittest.TestCase):
    def test_tokens_are_logged_per_batch_and_summed_per_fight_turn_and_hour(self):
        rig = Rig()
        rig.tick(user())
        rig.brain.handle([], {"in": 1000, "out": 50, "context": 62_000})
        rig.world["battle"] = {"bid": "B1", "round": 3, "entries": []}
        relay.log_tokens(rig.world, 7, {"in": 2000, "out": 100, "context": 64_000}, "MY TURN")
        relay.log_tokens(rig.world, 8, {"in": 500, "out": 20, "context": 64_500}, "his turn")
        s = relay.tokens_summary(rig.dir, rig.t)
        self.assertEqual((s["last_hour"], s["batches"], s["per_fight_turn"]), (3670, 3, 2620))
        self.assertEqual(relay.tokens_summary(rig.dir, rig.t + 7200)["last_hour"], 0)
        self.assertEqual(rig.world["relay"]["baseline_tokens"], 62_000)

    def test_the_relay_is_rotated_by_size_and_never_in_a_fight(self):
        rig = Rig()
        rig.tick(user())
        rig.brain.handle([], {"in": 1, "out": 1, "context": 65_000})          # a relay that starts large is not rotated
        self.assertIsNone(rig.tick(user())["stop"])
        rig.world["battle"] = {"bid": "B1", "entries": [], "battle": {}}
        relay.log_tokens(rig.world, 9, {"in": 1, "out": 1, "context": 65_000 + C.ROTATE_AFTER_TOKENS}, "")
        self.assertFalse(relay.should_rotate(rig.world))                      # mid-fight: never
        rig.world["battle"] = None
        out = rig.tick(user())
        self.assertTrue(out["stop"].startswith("rotate"))
        self.assertEqual(rig.world["relay"]["rotations"], 1)
        self.assertIsNone(rig.tick(user())["stop"])                           # the fresh relay starts a new count


class Client(unittest.TestCase):
    def setUp(self):
        self.rig = Rig()
        self.rig.world.save()
        self.t = os.path.join(self.rig.dir, "relay.jsonl")
        os.environ.update(TNR_TRANSCRIPT=self.t, TNR_PLAYER_NO_DAEMON="1", TNR_PLAYER_LIVE=self.rig.dir,
                          TNR_PLAYER_FIGHTS=os.path.join(self.rig.dir, "fights"))

    def tearDown(self):
        for k in ("TNR_TRANSCRIPT", "TNR_PLAYER_NO_DAEMON", "TNR_PLAYER_LIVE", "TNR_PLAYER_FIGHTS"):
            os.environ.pop(k, None)

    def next(self):
        out, slept = io.StringIO(), []
        brain.next_batch(self.rig.dir, out, slept.append)
        return out.getvalue().splitlines(), slept

    def test_next_answers_without_a_resident_brain_and_spends_the_wait_itself(self):
        transcript(self.t, [])
        lines, slept = self.next()
        self.assertEqual([json.loads(x).get("call") for x in lines[:-1]], ["profile.getUser"])
        now = time.time() + 1                                                 # the fake transcript keeps whole seconds
        transcript(self.t, [("use", "a", "profile.getUser", {}, now),
                            ("res", "a", json.dumps(user().data), now)])
        lines, slept = self.next()                                            # the hunt scan, held 8 s in the brain
        self.assertEqual([json.loads(x).get("call") for x in lines[:2]], ["profile.getUser", "travel.getSectorData"])
        self.assertIn(C.HUNT_WAIT, slept)
        self.assertEqual(os.listdir(os.path.join(self.rig.dir, "inbox")), [])  # the request was answered and removed
        self.assertEqual(brain.Brain(self.rig.dir).world.me["sector"], 1538)

    def test_a_relay_with_no_readable_transcript_hands_results_in_with_put(self):
        os.environ["TNR_TRANSCRIPT"] = os.path.join(self.rig.dir, "missing.jsonl")
        lines, _ = self.next()
        self.assertEqual(lines[0], "ECHO")
        brain.put(self.rig.dir, 1, json.dumps(user(sector=99).data))
        self.next()
        self.assertEqual(brain.Brain(self.rig.dir).world.me["sector"], 99)

    def test_the_resident_process_answers_and_only_one_brain_runs(self):
        transcript(self.t, [])
        env = dict(os.environ, PYTHONPATH=C.ROOT)
        proc = subprocess.Popen([sys.executable, "-m", "player.brain", "run"], cwd=C.ROOT, env=env)
        try:
            deadline = time.time() + 10
            while time.time() < deadline and brain._lock(self.rig.dir) is not None:
                time.sleep(0.05)                                             # until the resident brain holds the lock
            self.assertEqual(subprocess.run([sys.executable, "-m", "player.brain", "run"], cwd=C.ROOT, env=env,
                                            timeout=20).returncode, 1)       # a second brain refuses to start
            lines, _ = self.next()
            self.assertEqual(json.loads(lines[0])["call"], "profile.getUser")
        finally:
            proc.kill()
            proc.wait()
        lines, _ = self.next()                                               # the brain died: next still answers
        self.assertTrue(lines[-1].endswith('player.brain next"}'))


if __name__ == "__main__":
    unittest.main()
