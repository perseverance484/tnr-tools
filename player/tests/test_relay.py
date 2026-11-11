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


def nxt(token=""):
    """The Bash command a relay runs to hand a batch in."""
    return f"cd /repo && python3 -m player.brain next {token}".strip()


def token_of(line):
    """The token on a batch's last line."""
    return json.loads(line)["bash"].split()[-1]


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
        for must in ("brain next", "callEndpoint", "in order", "ONE message", "STOP", "no decisions", "put",
                     "one line at a time", "exactly as printed"):
            self.assertIn(must, text)

    def test_the_relay_agent_is_that_prompt_with_two_tools_and_nothing_else(self):
        """Live, 2026-11-11: a general-purpose relay was born with 118,190 tokens of context, and every request
        re-sent them. The relay's own agent definition carries the prompt, Bash and the connector's one call."""
        with open(os.path.join(C.ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
            _, head, body = f.read().split("---\n", 2)
        with open(os.path.join(C.ROOT, "player", "RELAY.md"), encoding="utf8") as f:
            self.assertEqual(body, f.read())                               # one prompt, not two
        fields = dict(line.split(": ", 1) for line in head.strip().splitlines())
        self.assertEqual((fields["model"], fields["omitClaudeMd"]), ("haiku", "true"))
        self.assertEqual([t.strip() for t in fields["tools"].split(",")], ["Bash", "mcp__Tnr__callEndpoint"])

    def test_a_batch_is_calls_waits_and_the_next_tick_and_nothing_else(self):
        rig = Rig()
        out = rig.tick(user())
        lines = [json.loads(x) for x in relay.lines(out["steps"] + [{"wait": 1.2}], token="ab12cd-7")]
        for row in lines[:-1]:
            self.assertTrue(set(row) == {"call", "input", "select"} or
                            re.fullmatch(r"python3 -c 'import time; time\.sleep\([\d.]+\)'", row.get("bash", "")), row)
        self.assertTrue(lines[-1]["bash"].endswith("python3 -m player.brain next ab12cd-7"))   # the batch's token
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
            ("use", "a", "profile.getUser", {}, 90), ("bash", "n1", nxt("ab12cd-1"), 90),                  # an older batch
            ("res", "a", '{"userData.status":"AWAKE"}', 90),
            ("use", "b", "profile.getUser", {}, 101), ("use", "c", "combat.getBattle", {"battleId": "B"}, 102),
            ("use", "d", "combat.performAction", {"battleId": "B"}, 103), ("use", "e", "item.consume", {}, 104),
            ("bash", "n2", nxt("ab12cd-2"), 104),
            ("res", "b", '{"userData.status":"BATTLE"}', 101),
            ("res", "c", "Error POSTing to endpoint: Too Many Requests", 102),
            ("res", "d", "Error calling combat.performAction: Not your turn", 103),
            ("res", "e", "not json", 104),
            ("usage", "r1", 10, 60_000, 50, 101), ("usage", "r1", 10, 60_000, 50, 102), ("usage", "r2", 5, 61_000, 40, 104)])
        asked = [("profile.getUser", {}), ("combat.getBattle", {"battleId": "B"}),
                 ("combat.performAction", {"battleId": "B"}), ("item.consume", {})]
        results, usage, strays = relay.read_batch(p, "ab12cd-2", asked)
        self.assertEqual([r.endpoint for r in results], [a[0] for a in asked])
        self.assertEqual(results[0].data, {"userData.status": "BATTLE"})
        self.assertEqual(results[1].error, "rate_limited")
        self.assertIn("Not your turn", results[2].error)
        self.assertIn("unreadable", results[3].error)
        self.assertEqual(strays, 0)

    def test_a_request_is_counted_once_and_only_for_its_own_batch(self):
        rig = Rig()
        p = os.path.join(rig.dir, "t.jsonl")
        transcript(p, [
            ("usage", "r0", 9, 50_000, 30, 90), ("bash", "n1", nxt("ab12cd-1"), 90),
            ("usage", "r1", 10, 60_000, 50, 101), ("usage", "r1", 10, 60_000, 50, 102),
            ("usage", "r2", 5, 61_000, 40, 104), ("bash", "n2", nxt("ab12cd-2"), 104)])
        self.assertEqual(relay.read_batch(p, "ab12cd-2", [])[1], {"in": 60_010 + 61_005, "out": 90, "context": 61_005})
        self.assertEqual(relay.read_batch(p, "ab12cd-1", [])[1], {"in": 50_009, "out": 30, "context": 50_009})

    def test_a_result_too_large_for_the_conversation_is_read_from_its_file(self):
        rig = Rig()
        p = os.path.join(rig.dir, "t.jsonl")
        saved = os.path.join(rig.dir, "big.json")
        with open(saved, "w") as f:
            json.dump([{"type": "text", "text": '{"battle.version": 7}'}], f)
        notice = f"<persisted-output>\nOutput too large (55.7KB). Full output saved to: {saved}\n\nPreview..."
        asked = [("combat.getBattle", {"battleId": "B"})]
        rows = [("use", "a", "combat.getBattle", {"battleId": "B"}, 101), ("bash", "n", nxt("ab12cd-3"), 101)]
        transcript(p, rows + [("res", "a", notice, 101)])
        self.assertEqual(relay.read_batch(p, "ab12cd-3", asked)[0][0].data, {"battle.version": 7})
        transcript(p, rows + [("res", "a", notice.replace(saved, "/etc/hostname.json"), 101)])
        self.assertIn("unreadable", relay.read_batch(p, "ab12cd-3", asked)[0][0].error)

    def test_the_relays_transcript_is_the_one_that_carries_the_batchs_token(self):
        rig = Rig()
        home = os.path.join(rig.dir, "claude")
        os.makedirs(os.path.join(home, "projects", "x", "subagents"))
        sup = os.path.join(home, "projects", "x", "main.jsonl")
        rel = os.path.join(home, "projects", "x", "subagents", "agent-1.jsonl")
        transcript(rel, [("bash", "n", nxt("ab12cd-4"), time.time())])
        transcript(sup, [("bash", "s", "git status", time.time())])           # written later: the newest file
        os.environ["CLAUDE_CONFIG_DIR"] = home
        try:
            self.assertEqual(relay.find_transcript("ab12cd-4"), rel)
            self.assertIsNone(relay.find_transcript("ab12cd-5"))              # nobody's token: nobody's transcript
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
        with open(os.path.join(rig.dir, "tokens.jsonl")) as f:
            self.assertEqual([json.loads(line)["calls"] for line in f], [4, 3, 3])   # the calls each batch carried

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

    def next(self, token=None):
        out, slept = io.StringIO(), []
        brain.next_batch(self.rig.dir, token, out, slept.append)
        return out.getvalue().splitlines(), slept

    def hello(self):
        """A new relay's first `brain next`: it gets a name and one line. Returns its first token."""
        lines, _ = self.next()
        self.assertEqual(len(lines), 1)
        return token_of(lines[0])

    def test_next_answers_without_a_resident_brain_and_spends_the_wait_itself(self):
        now = time.time()
        t0 = self.hello()
        transcript(self.t, [("bash", "n0", nxt(t0), now)])
        lines, slept = self.next(t0)
        self.assertEqual([json.loads(x).get("call") for x in lines[:-1]], ["profile.getUser"])
        t1 = token_of(lines[-1])
        transcript(self.t, [("bash", "n0", nxt(t0), now), ("use", "a", "profile.getUser", {}, now),
                            ("bash", "n1", nxt(t1), now), ("res", "a", json.dumps(user().data), now)])
        lines, slept = self.next(t1)                                          # the hunt scan, held 8 s in the brain
        self.assertEqual([json.loads(x).get("call") for x in lines[:2]], ["profile.getUser", "travel.getSectorData"])
        self.assertIn(C.HUNT_WAIT, slept)
        self.assertEqual(os.listdir(os.path.join(self.rig.dir, "inbox")), [])  # the request was answered and removed
        self.assertEqual(brain.Brain(self.rig.dir).world.me["sector"], 1538)

    def test_a_relay_with_no_readable_transcript_hands_results_in_with_put(self):
        os.environ["TNR_TRANSCRIPT"] = os.path.join(self.rig.dir, "missing.jsonl")
        lines, _ = self.next(self.hello())
        self.assertEqual([sorted(json.loads(x))[0] for x in lines], ["call", "put", "bash"])
        t1 = token_of(lines[-1])
        self.assertTrue(json.loads(lines[1])["put"].endswith(f"python3 -m player.brain put {t1} 1"))
        self.assertEqual(brain.put(self.rig.dir, t1, "1", json.dumps(user(sector=99).data)), 0)
        self.next(t1)
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
            lines, _ = self.next(self.hello())
            self.assertEqual(json.loads(lines[0])["call"], "profile.getUser")
        finally:
            proc.kill()
            proc.wait()
        lines, _ = self.next(token_of(lines[-1]))                            # the brain died: next still answers
        self.assertRegex(lines[-1], r'player\.brain next [0-9a-f]{6}-\d+"}$')


if __name__ == "__main__":
    unittest.main()
