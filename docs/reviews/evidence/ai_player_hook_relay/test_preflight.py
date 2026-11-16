"""The check for the operator's machine, off line: its gate, what it reads, and when it says yes.

    python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py

No session is started and nothing is sent: the brain's batches are made by the suite's rig, the logs are
written by hand, and the one process is a stand-in for Claude Code that prints what a test tells it to.
Review of 65974c02 (chatgpt/review-ai-player-relay-preflight-20261114 @ 5d46d7ef), B1 to B4.
"""
import contextlib
import io
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE)))))

import preflight as P  # noqa: E402
import preflight_gate as G  # noqa: E402
from player import config as C, relay  # noqa: E402
from player.tests.support import Rig, user  # noqa: E402

S, A = "11111111-2222-3333-4444-555555555555", "a0123456789abcdef"      # a session's id, a subagent's
RUN = {"form": "main", "agent": "tnr-relay", "bound": 3}


def held(live, steps, token="ab12cd-3"):
    """live/client.json as a relay with hooks holds a batch."""
    os.makedirs(live, exist_ok=True)
    relay.write(os.path.join(live, "client.json"), {"protocol": relay.PROTOCOL, "hooks": S, "token": token, "steps": steps})
    return token


def line(token, n, use="toolu_1", **more):
    return dict({"tool_name": G.TOOL, "tool_use_id": use, "session_id": S,
                 "tool_input": {"endpointName": C.STAND_IN, "input": {"b": token, "n": n}}}, **more)


def bash(command, **more):
    return dict({"tool_name": "Bash", "tool_use_id": "toolu_b", "session_id": S, "tool_input": {"command": command}}, **more)


class TheGate(unittest.TestCase):
    def setUp(self):
        self.live = os.path.join(tempfile.mkdtemp(prefix="gate-test-"), "live")

    def decide(self, inp, run=RUN, admitted=S, before=()):
        return G.decide(inp, run, admitted, list(before), self.live)[1]

    def test_what_the_brain_asks_for_in_guard_mode_is_no_ceiling_and_the_gate_is(self):
        """B1. Guard mode with the upkeep activities off still heals, ends a trip and reads a fight, as it
        should. Of every batch it makes, the gate lets through the reads of my own profile and nothing else."""
        seen = {}
        for status, bid in (("AWAKE", None), ("HOSPITALIZED", None), ("TRAVEL", None), ("BATTLE", "offline-battle")):
            rig = Rig(mode="guard")
            rig.tick()
            out = rig.tick(user(status=status, bid=bid))
            token = held(self.live, out["steps"])
            calls = [s for s in out["steps"] if "call" in s]
            for n, step in enumerate(calls, 1):
                why = self.decide(line(token, n))
                seen.setdefault(status, []).append((step["call"], why is None))
                self.assertEqual(why is None, step["call"] == "profile.getUser" and not step["input"], (status, step))
        self.assertEqual(seen["AWAKE"], [("profile.getUser", True)])
        self.assertIn(("hospital.npcHeal", False), seen["HOSPITALIZED"])
        self.assertIn(("travel.finishGlobalMove", False), seen["TRAVEL"])
        self.assertEqual({c for c, _ in seen["BATTLE"]}, {"combat.getBattle", "combat.getBattleEntries"})
        self.assertFalse(any(ok for _, ok in seen["BATTLE"]))

    def test_a_call_is_a_read_of_my_own_profile_or_it_is_refused(self):
        token = held(self.live, [{"call": "profile.getUser", "input": {}, "select": ["userData.status"]},
                                 {"wait": 1.0}, {"call": "profile.getUser", "input": {"userId": "another"}, "select": []},
                                 {"call": "profile.getPublicUser", "input": {}, "select": []}])
        self.assertIsNone(self.decide(line(token, 1)))
        for n in (2, 3, 4, 0):                                   # another's profile, another endpoint, no such line
            self.assertEqual(self.decide(line(token, n)), "not a read of my own profile")
        self.assertEqual(self.decide(line("ffffff-9", 1)), "not a read of my own profile")     # another batch's line
        real = {"tool_name": G.TOOL, "tool_use_id": "toolu_2", "session_id": S}
        self.assertIsNone(self.decide(dict(real, tool_input={"endpointName": "profile.getUser", "input": {}, "select": []})))
        self.assertIsNone(self.decide(dict(real, tool_input={"endpointName": "profile.getUser"})))
        for asked in ({"endpointName": "travel.startGlobalMove", "input": {"sector": 7}},
                      {"endpointName": "profile.getUser", "input": {"userId": "x"}}, {"input": {}}, None, "profile.getUser"):
            self.assertEqual(self.decide(dict(real, tool_input=asked)), "not a read of my own profile")

    def test_a_stand_in_with_no_batch_behind_it_is_refused(self):
        self.assertEqual(self.decide(line("ab12cd-3", 1)), "not a read of my own profile")     # (no client.json)
        relay.write(os.path.join(self.live, "client.json"), {"protocol": relay.PROTOCOL - 1, "hooks": S,
                                                             "token": "ab12cd-3", "steps": [{"call": "profile.getUser", "input": {}}]})
        self.assertEqual(self.decide(line("ab12cd-3", 1)), "not a read of my own profile")     # (another version's file)

    def test_the_fourth_call_is_refused(self):
        token = held(self.live, [{"call": "profile.getUser", "input": {}, "select": []}])
        three = [{"kind": "call", "refused": None}] * 3
        self.assertIsNone(self.decide(line(token, 1), before=three[:2] + [{"kind": "call", "refused": "not a read of my own profile"}]))
        self.assertEqual(self.decide(line(token, 1), before=three), "the check's calls have been made")
        self.assertEqual(self.decide(line(token, 1), run=dict(RUN, bound=0)), "the check's calls have been made")

    def test_nothing_is_let_through_before_the_check_has_looked_at_the_session(self):
        """B3. The gate is in front of the calls; what looks at the session's first event is behind them."""
        token = held(self.live, [{"call": "profile.getUser", "input": {}, "select": []}])
        for inp in (line(token, 1), bash("python3 -m player.brain next")):
            self.assertIsNone(self.decide(inp))
            for admitted in (None, "", "another-session"):
                self.assertEqual(self.decide(inp, admitted=admitted), "the check has not looked at this session yet")

    def test_the_one_command_is_brain_next(self):
        for ok in ("python3 -m player.brain next", "python3 -m player.brain next ab12cd-3",
                   f"cd {G.ROOT} && python3 -m player.brain next ab12cd-3"):
            self.assertIsNone(self.decide(bash(ok)), ok)
        for no in ("python3 -m player.brain set mode=hunt", "python3 -m player.brain next; rm -rf x", "ls",
                   "python3 -m player.brain next ab12cd-3 --hooks x", "cd /elsewhere && python3 -m player.brain next",
                   "python3 -m player.brain next\npython3 -m player.brain stopped all", " python3 -m player.brain next",
                   "python3 -m player.brain next\n", "python3 -m player.brain next ab12cd-3 "):
            self.assertEqual(self.decide(bash(no)), "not `brain next`", no)
        self.assertEqual(self.decide(dict(bash("x"), tool_input=None)), "not `brain next`")

    def test_a_subagent_is_the_relay_once_and_only_in_that_form(self):
        start = {"tool_name": "Agent", "tool_use_id": "toolu_a", "session_id": S, "tool_input": {"subagent_type": "tnr-relay"}}
        sub = dict(RUN, form="subagent")
        self.assertEqual(self.decide(start), "no subagent is started in this form of the check")
        self.assertIsNone(self.decide(start, run=sub))
        self.assertIsNone(self.decide(dict(start, tool_name="Task"), run=sub))
        self.assertEqual(self.decide(start, run=sub, before=[{"kind": "agent", "refused": None}]), "the relay has been started")
        self.assertIsNone(self.decide(start, run=sub, before=[{"kind": "agent", "refused": "not the relay's agent"}]))
        self.assertEqual(self.decide(dict(start, tool_input={"subagent_type": "general-purpose"}), run=sub), "not the relay's agent")
        self.assertEqual(self.decide(dict(start, agent_id=A), run=sub), "no subagent is started in this form of the check")

    def test_any_other_tool_is_refused(self):
        for tool in ("Read", "Write", "Edit", "WebFetch", "mcp__Tnr__standIn_0a1b2c", "mcp__Tnr__getEndpointSchema",
                     "mcp__Other__callEndpoint", "", None):
            self.assertEqual(self.decide({"tool_name": tool, "session_id": S, "tool_input": {}}), "not a tool of the relay")

    def test_the_hook_as_claude_code_runs_it(self):
        """Its answer and its row, by what is on its standard input; and that a gate that cannot tell fails."""
        out = os.path.dirname(self.live)
        token = held(self.live, [{"call": "profile.getUser", "input": {}, "select": []},
                                 {"call": "hospital.npcHeal", "input": {}, "select": []}])
        old, G.WAIT = (os.environ.get("TNR_PREFLIGHT_OUT"), os.environ.get("TNR_PLAYER_LIVE"), G.WAIT), 0.1
        os.environ.update(TNR_PREFLIGHT_OUT=out, TNR_PLAYER_LIVE=self.live)

        def run(what, inp):
            said = io.StringIO()
            self.assertEqual(G.main([what], io.StringIO(json.dumps(inp)), said), 0)
            return json.loads(said.getvalue()) if said.getvalue() else None
        try:
            with self.assertRaises(OSError):                     # (no run.json: it exits with an error, which blocks)
                run("tool", line(token, 1))
            with open(os.path.join(out, "run.json"), "w", encoding="utf8") as f:
                json.dump(RUN, f)
            self.assertIsNone(run("start", {"session_id": S}))
            early = run("tool", line(token, 1))["hookSpecificOutput"]
            self.assertEqual((early["permissionDecision"], early["permissionDecisionReason"]),
                             ("deny", "the check's gate: the check has not looked at this session yet"))
            with open(os.path.join(out, "admitted"), "w", encoding="utf8") as f:
                f.write(S)
            self.assertIsNone(run("tool", line(token, 1, use="toolu_1")))
            self.assertEqual(run("tool", line(token, 2, use="toolu_2", agent_id=A))["hookSpecificOutput"]["permissionDecision"], "deny")
            kept = P.rows(os.path.join(out, "gate.jsonl"))
            self.assertEqual([(r["kind"], r.get("use"), r.get("by"), r.get("refused")) for r in kept], [
                ("start", None, None, None), ("early", "toolu_1", S, "the check has not looked at this session yet"),
                ("call", "toolu_1", S, None), ("call", "toolu_2", A, "not a read of my own profile")])
            self.assertFalse(os.path.exists(os.path.join(out, "gate.lock")))
        finally:
            G.WAIT = old[2]
            for k, v in (("TNR_PREFLIGHT_OUT", old[0]), ("TNR_PLAYER_LIVE", old[1])):
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)


def init(servers=None, tools=(P.TOOL,), session=S):
    return {"type": "system", "subtype": "init", "session_id": session, "tools": ["Bash"] + list(tools),
            "mcp_servers": [{"name": "Tnr", "status": "connected"}] if servers is None else servers}


class WhatTheCheckReads(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="preflight-test-")

    def put(self, name, text):
        with open(os.path.join(self.dir, name), "w", encoding="utf8") as f:
            f.write(text)
        return os.path.join(self.dir, name)

    def test_a_log_that_is_not_there_has_no_rows_and_one_that_cannot_be_read_fails(self):
        """B2. A log that could not be opened was read as one with nothing in it."""
        self.assertEqual(P.rows(os.path.join(self.dir, "none.jsonl")), [])
        os.mkdir(os.path.join(self.dir, "a_folder.jsonl"))
        with self.assertRaises(P.Failed):
            P.rows(os.path.join(self.dir, "a_folder.jsonl"))
        self.assertEqual(P.rows(self.put("a.jsonl", '{"a": 1}\n{"b": 2}\n{"c": ')), [{"a": 1}, {"b": 2}])   # (the last is being written)
        for bad in ('{"a": 1}\nnot a row\n', '[1]\n', '{"a": \n{"b": 2}\n'):
            with self.assertRaises(P.Failed):
                P.rows(self.put("b.jsonl", bad))

    def test_the_first_event_is_told_by_its_fields_however_it_is_written(self):
        """B3. It was looked for by the bytes a line began with: the same event with a space in it was not seen."""
        one = init()
        for text in (json.dumps(one, separators=(",", ":")), json.dumps(one), json.dumps(dict(reversed(list(one.items())))),
                     "  " + json.dumps(one, indent=None)):
            path = self.put("s.jsonl", "Warning: no stdin data received\n" + json.dumps({"type": "system", "subtype": "hook"})
                            + "\n" + text + "\n")
            self.assertEqual(P.first_event(P.events(path)), one)
        self.assertIsNone(P.first_event(P.events(self.put("s.jsonl", '{"type":"assistant"}\n'))))
        self.assertIsNone(P.first_event(P.events(os.path.join(self.dir, "none"))))
        with self.assertRaises(P.Failed):
            P.events(self.put("s.jsonl", '{"type":"system","subtype":"init", \n'))
        self.assertEqual(P.events(self.put("s.jsonl", '{"type":"system","subtype":"in')), [])   # (not finished yet)

    def test_a_session_with_anything_but_the_stand_in_is_told(self):
        both = [P.TOOL, "mcp__Tnr__standIn_0a1b2c"]
        self.assertIsNone(P.inventory(init(), [P.TOOL]))
        self.assertIsNone(P.inventory(init(tools=both), both))
        for wrong in (init(servers=[]), init(servers=[{"name": "Tnr", "status": "connected"}, {"name": "claude.ai Tnr", "status": "connected"}]),
                      init(servers=[{"name": "Other", "status": "connected"}]), init(servers=[{"name": "Tnr", "status": "failed"}]),
                      init(servers=[{"name": "Tnr"}]), init(servers="Tnr"), init(servers=["Tnr"]),
                      {"type": "system", "subtype": "init", "session_id": S, "tools": [P.TOOL]}):
            self.assertIn("not the stand-in alone", P.inventory(wrong, [P.TOOL]))
        connector = (P.TOOL, "mcp__Tnr__getEndpointSchema", "mcp__Tnr__listGameRouters", "mcp__Tnr__listRouterEndpoints")
        for tools, must in ((connector, [P.TOOL]), ((P.TOOL,), both), ((), [P.TOOL]), (both, [P.TOOL]),
                            ((P.TOOL, "mcp__Other__x"), [P.TOOL]), (connector, both)):
            self.assertIn("its MCP tools are", P.inventory(init(tools=tools), must))
        self.assertEqual(P.inventory(dict(init(), tools=None), [P.TOOL]), "it does not list its tools")

    def test_a_session_is_let_through_when_all_of_it_is_there(self):
        game, gate = [{"at": "connected", "nonce": "n1", "pid": 7}], [{"kind": "start", "session": S}]
        self.assertEqual(P.admission(init(), game, gate, "n1", [P.TOOL]), (None, False))
        for not_yet in (P.admission(init(), [], gate, "n1", [P.TOOL]),                             # (it may still come)
                        P.admission(init(), [{"at": "came", "endpoint": P.PROBE}], gate, "n1", [P.TOOL]),
                        P.admission(init(), game, [], "n1", [P.TOOL]),
                        P.admission(init(), game, [{"kind": "start", "session": "another"}], "n1", [P.TOOL])):
            self.assertTrue(not_yet[0] and not not_yet[1], not_yet)
        for final in (P.admission(init(), [{"at": "connected", "nonce": "old"}], gate, "n1", [P.TOOL]),
                      P.admission(init(), game * 2, gate, "n1", [P.TOOL]),
                      P.admission(init(servers=[]), game, gate, "n1", [P.TOOL]),
                      P.admission(init(session=None), game, gate, "n1", [P.TOOL])):
            self.assertTrue(final[0] and final[1], final)

    def test_a_call_that_went_and_is_not_in_the_stand_ins_log(self):
        """B2. With no log of the stand-in's, a call that had gone was not missed. It is, by what the session
        shows for it: an answer that is no error, and no row of the stand-in's."""
        through = [{"kind": "call", "use": "u1", "refused": None, "at": 100.0}]
        came = [{"at": "came", "endpoint": P.PROBE, "input": {}, "use": "u1"}]
        self.assertIsNone(P.astray(through, came, {"u1": False}, [], 500.0))
        self.assertIsNone(P.astray(through, [], {}, [], 100.0 + P.LATE))                     # (no result yet, and in time)
        self.assertEqual(P.astray(through, [], {"u1": False}, [], 100.1), "a call was answered, and not by the stand-in")
        refused = [{"hook": "pre", "use": "u1", "refused": "call 1 of the batch was not made"}]
        self.assertIsNone(P.astray(through, [], {"u1": True}, refused, 900.0))          # the relay's hook refused it,
        self.assertIsNone(P.astray(through, [], {}, refused, 900.0))                    # on record: it never went
        for hooks in ([], [{"hook": "pre", "use": "u1", "refused": None}], [{"hook": "post", "use": "u1", "refused": "x"}],
                      [{"hook": "pre", "use": "u2", "refused": "x"}]):
            self.assertIn("whether it went cannot be told", P.astray(through, [], {"u1": True}, hooks, 100.1), hooks)
        self.assertIn("has no result after", P.astray(through, [], {}, [], 100.1 + P.LATE))
        self.assertIn("did not let through", P.astray([], came, {}, [], 100.0))
        self.assertIn("did not let through", P.astray([dict(through[0], refused="x")], came, {}, [], 100.0))
        self.assertIn("not a read of my own profile", P.astray(through, [dict(came[0], endpoint="hospital.npcHeal")], {}, [], 100.0))
        self.assertIn("not a read of my own profile", P.astray(through, [dict(came[0], input={"userId": "x"})], {}, [], 100.0))
        self.assertIn("do not name their tool calls", P.astray(through, [dict(came[0], use=None)], {}, [], 100.0))
        self.assertIn("do not name their tool calls", P.astray(through * 2, came * 2, {}, [], 100.0))
        shown = P.results([{"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "u1", "is_error": True},
                                                                    {"type": "tool_result", "tool_use_id": "u2"}]}},
                           {"type": "assistant", "message": {"content": [{"type": "tool_result", "tool_use_id": "u3"}]}},
                           {"type": "user", "message": {"content": "text"}}, {"type": "user"}])
        self.assertEqual(shown, {"u1": True, "u2": False})

    def test_an_error_for_a_call_does_not_say_that_it_never_went(self):
        """Review of 071ba1b1, C3, as it was run: the stand-in itself is told to answer a call with an error
        and to write nothing down. It was given the call. What the session shows for it is an error, which
        was read as "refused before it went" and passed over, for as long as the session lasted."""
        log, control = os.path.join(self.dir, "game.jsonl"), self.put("control.json", "{}")
        server = subprocess.Popen([sys.executable, os.path.join(HERE, "fake_connector.py")], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True,
                                  env=dict(os.environ, TNR_FAKE_LOG=log, TNR_FAKE_CONTROL=control, TNR_FAKE_NONCE="n1"))

        def ask(rid, method, params=None):
            server.stdin.write(json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}) + "\n")
            server.stdin.flush()
            return json.loads(server.stdout.readline())

        def call(rid, use):
            return ask(rid, "tools/call", {"name": "callEndpoint", "arguments": {"endpointName": P.PROBE, "input": {}},
                                           "_meta": {"claudecode/toolUseId": use}})["result"]
        try:
            ask(1, "initialize", {})
            self.assertFalse(call(2, "u1")["isError"])
            self.put("control.json", json.dumps({"unseen": True, "fail": [P.PROBE]}))
            self.assertTrue(call(3, "u2")["isError"])                               # it was given the call,
        finally:
            server.kill()
            server.wait()
            server.stdin.close()
            server.stdout.close()
        game = P.rows(log)
        self.assertEqual([g.get("use") for g in game if g.get("at") == "came"], ["u1"])   # and wrote the first down
        gate = [{"kind": "call", "use": u, "refused": None, "at": 100.0} for u in ("u1", "u2")]
        said = P.astray(gate, game, {"u1": False, "u2": True}, [], 100.1)
        self.assertIn("came back as an error and is not in the stand-in's log", said)   # (was: None, at any time)
        self.assertIsNone(P.astray(gate[:1], game, {"u1": False}, [], 900.0))

    def test_a_shell_that_sets_the_live_folder_itself_stops_the_check(self):
        """`brain next` is run by the session's shell: with another TNR_PLAYER_LIVE it would play in the
        player's real folder."""
        old, asked = P.subprocess.run, []

        class Said:
            def __init__(self, out):
                self.stdout = out
        try:
            for out, ok in ((os.path.join(self.dir, "live"), True), ("motd\n" + os.path.join(self.dir, "live"), True),
                            ("/home/me/tnr-tools/state/player/x/live", False), ("", False)):
                P.subprocess.run = lambda cmd, **k: (asked.append((cmd, k["env"]["TNR_PLAYER_LIVE"])), Said(out))[1]
                self.assertEqual(P.shell_keeps(self.dir) is None, ok, out)
            self.assertEqual(asked[0][1], os.path.join(self.dir, "live"))
            self.assertEqual(asked[0][0][1:], ["-lc", 'printf "%s" "$TNR_PLAYER_LIVE"'])

            def gone(cmd, **k):
                raise FileNotFoundError("no shell")
            P.subprocess.run = gone
            self.assertIn("could not be asked", P.shell_keeps(self.dir))
        finally:
            P.subprocess.run = old

    def test_a_folder_that_was_used_before_is_not_used_again(self):
        """B4. A folder used again kept the logs of the run before, and they were read as this run's."""
        self.put("game.jsonl", "{}\n")
        with self.assertRaises(P.Failed):
            P.fresh(self.dir)
        with self.assertRaises(P.Failed):
            P.fresh(os.path.join(self.dir, "game.jsonl"))
        new = os.path.join(self.dir, "new", "main")
        self.assertEqual(P.fresh(new), new)
        self.assertEqual(P.fresh(new), new)                                              # (made, and still empty)


def good(form="main"):
    """What a session that passed leaves: (gate rows, the relay's hook rows, the stand-in's rows)."""
    by = S if form == "main" else A
    uses = ["u1", "u2", "u3"]
    gate = [{"kind": "start", "session": S}] + ([{"kind": "agent", "by": S, "session": S, "refused": None}] if form != "main" else [])
    hooks, game = [{"hook": "bash", "by": by, "use": "b0", "refused": None}], [{"at": "connected", "nonce": "n1", "pid": 1}]
    for u in uses:
        gate += [{"kind": "bash", "by": by, "session": S, "refused": None}, {"kind": "call", "use": u, "by": by, "session": S, "refused": None}]
        hooks += [{"hook": "bash", "by": by, "use": "b" + u, "refused": None}, {"hook": "pre", "by": by, "use": u, "refused": None},
                  {"hook": "post", "by": by, "use": u, "refused": None}]
        game += [{"at": "came", "endpoint": P.PROBE, "use": u}, {"at": "answered", "endpoint": P.PROBE, "use": u, "failed": False}]
    return gate, hooks, game


class WhenItSaysYes(unittest.TestCase):
    def verdict(self, form="main", how=P.STOPPED, session=S, reaped=True, gate=None, hooks=None, game=None,
                running=True, code=143):
        g, h, s = good(form)
        return P.verdict(form, P.Ended(how, session, reaped, running, code), g if gate is None else gate,
                         h if hooks is None else hooks, s if game is None else game)

    def test_a_relay_whose_hooks_ran_for_each_of_the_three_calls(self):
        self.assertIsNone(self.verdict())
        self.assertIsNone(self.verdict("subagent"))

    def test_one_hook_behind_a_call_for_three_calls_is_not_every_call(self):
        """B4, as the review ran it: three calls, three hooks before, one behind; and the session's exit."""
        gate, hooks, game = good()
        some = [h for h in hooks if h["hook"] != "post" or h["use"] == "u1"]
        self.assertEqual(self.verdict(hooks=some), "the hook behind a call did not run once for each call")
        self.assertIn("before a call", self.verdict(hooks=[h for h in hooks if h["hook"] != "pre" or h["use"] != "u2"]))
        self.assertIn("did not run once", self.verdict(hooks=hooks + [dict(hooks[-1])]))             # (twice for one call)
        self.assertIn("every batch", self.verdict(hooks=[h for h in hooks if h["hook"] != "bash"][:] + hooks[:1]))
        self.assertIn("did not let through", self.verdict(hooks=hooks + [{"hook": "pre", "by": S, "use": "u9", "refused": None}]))

    def test_a_session_that_was_not_stopped_after_its_calls_does_not_pass(self):
        for how in ("ended: the clock ran out", P.BY_ITSELF, "ended: a call was answered, and not by the stand-in",
                    "ended: the session did not show what it has in time", None, ""):
            self.assertIn("was not stopped after its calls", self.verdict(how=how))
        self.assertIn("could not be seen to end", self.verdict(reaped=False))
        self.assertIn("was not stopped after its calls", self.verdict(running=False))   # (C2: said to be stopped,
        self.assertIn("ended by itself (with 1)", self.verdict(how=P.BY_ITSELF, code=1))  # and was not running)

    def test_what_another_session_left_behind_does_not_pass(self):
        """B4: logs of an earlier run in the same folder, and two sessions that then failed to start."""
        self.assertEqual(self.verdict(session="99999999-0000-0000-0000-000000000000"), "the gate's rows are not all this session's")
        self.assertIn("not all this session's", self.verdict(session=None))
        gate, hooks, game = good()
        self.assertIn("another than the relay", self.verdict(hooks=hooks + [{"hook": "bash", "by": "older", "refused": None}]))
        self.assertIn("not the ones the gate let through", self.verdict(game=[dict(g, use="old-" + g["use"]) if g.get("use") else g for g in game]))

    def test_the_count_is_three_of_each(self):
        gate, hooks, game = good()
        self.assertIn("let 2 calls through", self.verdict(gate=gate[:-1]))
        self.assertIn("let 4 calls through", self.verdict(gate=gate + [dict(gate[-1], use="u4")]))
        self.assertIn("let 3 calls through", self.verdict(gate=gate[:-1] + [dict(gate[-1], use="u1")]))   # (one id twice)
        self.assertIn("given 3 calls and answered 2", self.verdict(game=game[:-1]))
        self.assertIn("given 3 calls and answered 3", self.verdict(game=game[:-1] + [dict(game[-1], failed=True)]))
        self.assertIn("given 4 calls", self.verdict(game=game + [{"at": "came", "endpoint": P.PROBE, "use": "u4"}]))

    def test_the_relay_is_one_and_of_the_form_that_was_asked_for(self):
        gate, hooks, game = good("subagent")
        self.assertIn("one relay of this form", self.verdict("main", gate=gate, hooks=hooks, game=game))
        self.assertIn("one relay of this form", self.verdict("subagent"[:0] + "subagent", gate=good()[0], hooks=good()[1]))
        mixed = [dict(g, by="another") if g.get("use") == "u2" else g for g in good()[0]]
        self.assertIn("one relay of this form", self.verdict(gate=mixed))

    def test_a_hook_that_refused_does_not_pass_but_for_the_call_past_the_third(self):
        gate, hooks, game = good()
        self.assertIn("a hook refused", self.verdict(hooks=hooks + [{"hook": "pre", "by": S, "use": "u3", "refused": "call 2 was not made"}]))
        over = gate + [{"kind": "call", "use": "u4", "by": S, "session": S, "refused": "the check's calls have been made"}]
        self.assertIsNone(self.verdict(gate=over, hooks=hooks + [{"hook": "pre", "by": S, "use": "u4", "refused": None}]))
        self.assertIsNone(self.verdict(gate=over, hooks=hooks + [{"hook": "pre", "by": S, "use": "u4", "refused": "no relay holds it"}]))


REAL = (P.time, subprocess.Popen, P.end, subprocess.run)


class Clock:
    def __init__(self):
        self.t = 1000.0

    def time(self):
        return self.t

    def sleep(self, s):
        self.t += s


class Stub:
    """In place of Claude Code: a process that is running until a test ends it, or that ends by itself with
    `code` once it has been looked at `after` times."""
    pid, code, after = 4242, None, 0

    def poll(self):
        self.after -= 1
        return self.code if self.after < 0 else None

    def wait(self, timeout=None):
        return self.code


class TheSessionIsWatched(unittest.TestCase):
    """The loop itself, with a clock the test moves and no process: what a session printed is written by hand."""

    def setUp(self):
        self.out = tempfile.mkdtemp(prefix="preflight-loop-")
        self.nonce = P.prepare(self.out, "main", "tnr-relay")
        self.clock, self.stub, self.ended = Clock(), Stub(), []
        P.time = self.clock
        P.subprocess.Popen = lambda *a, **k: (self.started(), self.stub)[1]
        P.end = lambda p, game: (self.ended.append(self.clock.t), (True, p.poll() is None))[1]
        self.says = None

    def tearDown(self):
        P.time, P.subprocess.Popen, P.end, P.subprocess.run = REAL           # (whatever a test put in their place,
                                                                             # and however often it began again)

    def started(self):
        if self.says is not None:
            with open(os.path.join(self.out, "stream.jsonl"), "a", encoding="utf8") as f:
                f.write(self.says)

    def log(self, name, *rows):
        os.makedirs(os.path.dirname(os.path.join(self.out, name)), exist_ok=True)
        with open(os.path.join(self.out, name), "a", encoding="utf8") as f:
            f.write("".join(json.dumps(r) + "\n" for r in rows))

    def run_it(self, done=lambda gate, hooks, game: False):
        self.last = P.session(self.out, "main", ["--agent", "tnr-relay", "Begin."], [P.TOOL], done)
        return self.last.how, self.last.session, self.last.gone

    def admitted(self):
        try:
            with open(os.path.join(self.out, "admitted"), encoding="utf8") as f:
                return f.read()
        except FileNotFoundError:
            return None

    def test_a_session_that_never_shows_what_it_has_is_ended_and_never_let_through(self):
        """B3: no first event was passed over until the clock of the whole run."""
        how, whose, reaped = self.run_it()
        self.assertEqual((how, whose, self.admitted()), ("ended: the session did not show what it has in time", None, None))
        self.assertLess(self.ended[0] - 1000.0, P.STARTUP + 1)

    def test_a_first_event_with_another_server_is_ended_however_it_is_written(self):
        """B3: the same event as json.dumps writes it was not seen at all."""
        for dumps in (lambda o: json.dumps(o, separators=(",", ":")), json.dumps):
            self.setUp()
            self.says = dumps(init(servers=[{"name": "Tnr", "status": "connected"}, {"name": "Game", "status": "connected"}])) + "\n"
            self.log("gate.jsonl", {"kind": "start", "session": S})
            self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
            how, whose, _ = self.run_it()
            self.assertIn("not the stand-in alone", how)
            self.assertEqual((whose, self.admitted()), (None, None))
            self.assertLess(self.ended[0] - 1000.0, 1.0)
            self.tearDown()

    def test_a_line_of_its_output_that_cannot_be_read_ends_it(self):
        self.says = '{"type":"system","subtype":"init", broken\n'
        how, whose, _ = self.run_it()
        self.assertEqual((how, whose, self.admitted()), ("ended: the session printed a line that cannot be read", None, None))

    def test_a_session_with_the_stand_in_alone_is_let_through_when_the_stand_in_and_the_gate_are_there(self):
        self.says = json.dumps(init()) + "\n"                    # (with spaces, as the check did not know it)
        how, whose, _ = self.run_it()                             # the stand-in and the gate's mark never come
        self.assertEqual((how, whose, self.admitted()), ("ended: the session did not show what it has in time", None, None))
        for there in ("gate.jsonl", "game.jsonl"):                # one of the two, and not the other
            self.setUp()
            self.says = json.dumps(init()) + "\n"
            self.log(there, {"kind": "start", "session": S} if there == "gate.jsonl" else
                     {"at": "connected", "nonce": self.nonce, "pid": 1})
            how, whose, _ = self.run_it()
            self.assertEqual((how, whose, self.admitted()), ("ended: the session did not show what it has in time", None, None))
        self.setUp()
        self.says = json.dumps(init()) + "\n"
        self.log("gate.jsonl", {"kind": "start", "session": S})
        self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
        how, whose, _ = self.run_it(done=lambda gate, hooks, game: self.admitted() == S)
        self.assertEqual((how, whose, self.admitted()), (P.STOPPED, S, S))
        self.assertEqual((self.last.running, self.last.gone), (True, True))

    def test_a_call_that_is_answered_and_not_by_the_stand_in_ends_the_session(self):
        """B2, with no log of the stand-in's calls at all."""
        self.says = json.dumps(init()) + "\n" + json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "tool_use_id": "u1", "content": "ok"}]}}) + "\n"
        self.log("gate.jsonl", {"kind": "start", "session": S},
                 {"kind": "call", "use": "u1", "by": S, "session": S, "refused": None, "at": 1000.0})
        self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
        how, _, _ = self.run_it()
        self.assertEqual(how, "ended: a call was answered, and not by the stand-in")
        self.assertLess(self.ended[0] - 1000.0, 1.0)

    def everything_a_session_that_passed_leaves(self, out, nonce):
        """Written when the session is started: its first event, and three calls from the gate to the stand-in
        and back, each with its hooks."""
        gate, hooks, game = good()
        t = self.clock.t
        with open(os.path.join(out, "stream.jsonl"), "a", encoding="utf8") as f:
            f.write(json.dumps(init()) + "\n")
        os.makedirs(os.path.join(out, "live", "hook"), exist_ok=True)
        for name, rows in (("gate.jsonl", [dict(g, at=t) for g in gate]), (os.path.join("live", "hook", "log.jsonl"), hooks),
                           ("game.jsonl", [dict(g, nonce=nonce, answered=t) if g["at"] != "came" else g for g in game])):
            with open(os.path.join(out, name), "a", encoding="utf8") as f:
                f.write("".join(json.dumps(r) + "\n" for r in rows))

    def a_form(self, code, after=0):
        """preflight.form on a session that leaves everything a passing one leaves, and whose process ends by
        itself with `code` (None: it is running until the check ends it)."""
        out = os.path.join(tempfile.mkdtemp(prefix="preflight-form-"), "main")
        self.stub.code, self.stub.after = code, after

        def started(*a, **k):
            with open(os.path.join(out, "run.json"), encoding="utf8") as f:
                self.everything_a_session_that_passed_leaves(out, json.load(f)["nonce"])
            return self.stub
        P.subprocess.Popen = started
        P.subprocess.run = lambda *a, **k: None                              # (`brain set`, in the check's own folder)
        return P.form(out, "main", "tnr-relay", [])

    def test_a_session_that_ended_by_itself_is_not_one_the_check_stopped_whatever_it_left(self):
        """Review of 071ba1b1, C2, as it was run: every row of a passing session, written for this run, and a
        process that had ended with 1. What it had left was looked at first, and the session was put down as
        stopped after its calls: the form passed."""
        for code, after in ((1, 0), (0, 0), (1, 3), (0, 5)):                 # at once, and while the check waits a
            self.setUp()                                                     # moment before it ends the session
            ran, said = self.a_form(code, after)
            self.assertEqual((ran, said["the relay's hooks ran for every call"]), (False, False), (code, after))
            self.assertEqual((said["how the session ended"], said["it ended with"]), (P.BY_ITSELF, code))
            self.assertEqual(said["why not"], f"the session was not stopped after its calls: {P.BY_ITSELF} (with {code})")
            self.assertEqual(said["calls the gate let through"], 3)          # (the rows are all there)
        self.setUp()
        ran, said = self.a_form(None)                                        # the same rows, and a session that
        self.assertEqual((ran, said["how the session ended"], said["why not"]), (True, P.STOPPED, None))   # is running

    def test_the_loop_looks_at_the_process_before_it_looks_at_what_was_done(self):
        self.says = json.dumps(init()) + "\n"
        self.log("gate.jsonl", {"kind": "start", "session": S})
        self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
        self.stub.code = 1
        self.assertEqual(self.run_it(done=lambda gate, hooks, game: True)[0], P.BY_ITSELF)
        self.assertEqual((self.last.running, self.last.code, self.admitted()), (False, 1, S))

    def a_look(self, code, rows=()):
        """preflight.look on a session that lists the stand-in alone, has the gate's mark, and ends by itself
        with `code` (None: it does not end)."""
        out = os.path.join(tempfile.mkdtemp(prefix="preflight-look-"), "look")
        self.stub.code, self.stub.after = code, 2

        def started(*a, **k):
            with open(os.path.join(out, "run.json"), encoding="utf8") as f:
                nonce = json.load(f)["nonce"]
            for name, lines in (("stream.jsonl", [init(tools=(P.TOOL, f"mcp__Tnr__standIn_{nonce}"))]),
                                ("gate.jsonl", [{"kind": "start", "session": S}] + list(rows)),
                                ("game.jsonl", [{"at": "connected", "nonce": nonce, "pid": 1}])):
                with open(os.path.join(out, name), "a", encoding="utf8") as f:
                    f.write("".join(json.dumps(r) + "\n" for r in lines))
            return self.stub
        P.subprocess.Popen = started
        return P.look(out)

    def test_the_session_that_may_call_nothing_ends_by_itself_and_well_or_nothing_is_started(self):
        self.assertIsNone(self.a_look(0))
        self.setUp()
        self.assertIn("could not be looked at: the session ended by itself (with 1)", self.a_look(1))
        self.setUp()
        self.assertIn("could not be looked at: ended: the clock ran out", self.a_look(None))
        self.setUp()
        self.assertIsNone(self.a_look(0, [{"kind": "bash", "session": S, "refused": "the check has not looked at this session yet"}]))
        self.setUp()
        self.assertEqual(self.a_look(0, [{"kind": "bash", "session": S, "refused": None}]),
                         "the session that may call nothing made a call")

    def test_on_a_system_it_was_not_written_for_nothing_is_started(self):
        """How it ends a session's processes and sees them gone was written for Windows too, and never run
        there (review of 071ba1b1, C1). It says so and starts nothing."""
        started, said = [], io.StringIO()
        P.subprocess.Popen = P.subprocess.run = lambda *a, **k: started.append(a)
        with mock.patch.object(P.os, "name", "nt"), mock.patch.object(sys, "argv", ["preflight.py"]), \
                contextlib.redirect_stdout(said):
            self.assertEqual(P.main(), 2)
        self.assertEqual(started, [])
        self.assertEqual(json.loads(said.getvalue())["started"], False)
        self.assertIn("POSIX", json.loads(said.getvalue())["why"])

    def test_a_log_that_cannot_be_read_ends_it(self):
        self.says = json.dumps(init()) + "\n"
        os.mkdir(os.path.join(self.out, "game.jsonl"))
        how, _, _ = self.run_it()
        self.assertIn("game.jsonl cannot be read", how)

    def test_a_session_that_ends_by_itself_or_runs_out_the_clock_is_said_to(self):
        self.says = json.dumps(init()) + "\n"
        self.log("gate.jsonl", {"kind": "start", "session": S})
        self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
        how, _, _ = self.run_it()
        self.assertEqual(how, "ended: the clock ran out")
        self.setUp()
        self.says, self.stub.code = json.dumps(init()) + "\n", 1
        self.stub.after = 0
        self.log("gate.jsonl", {"kind": "start", "session": S})
        self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
        self.assertEqual(self.run_it()[0], P.BY_ITSELF)
        self.assertEqual((self.last.running, self.last.code), (False, 1))


CHILD = "import signal, time; signal.signal(signal.SIGTERM, signal.SIG_IGN); print('deaf', flush=True); time.sleep(600)"
PARENT = """
import subprocess, sys, time
child = subprocess.Popen([sys.executable, "-c", sys.argv[1]], start_new_session="leaves" in sys.argv)
print(child.pid, flush=True)
if "dies" not in sys.argv:
    time.sleep(600)
"""


LATE = """
import os, signal, subprocess, sys, time
def asked(*a):
    child = subprocess.Popen([sys.executable, "-c", sys.argv[3]], start_new_session=True, stdout=subprocess.PIPE)
    child.stdout.readline()
    with open(sys.argv[2] + ".tmp", "w") as f:
        f.write(str(child.pid))
    os.replace(sys.argv[2] + ".tmp", sys.argv[2])
    while not os.path.exists(sys.argv[1]):
        time.sleep(0.01)
    os._exit(0)
signal.signal(signal.SIGTERM, asked)
print("ready", flush=True)
time.sleep(600)
"""
WAITS = "import os, sys, time\nwhile not os.path.exists(sys.argv[1]):\n    time.sleep(0.01)\nsys.exit(1)\n"


class TheSessionIsEnded(unittest.TestCase):
    """Review of 071ba1b1, C1, with processes of this machine that do nothing: a leader of a process group of its
    own, as the check starts a session, and a child of it that does not end when it is asked to."""

    def setUp(self):
        self.patience, P.PATIENCE = P.PATIENCE, 1.0
        self.addCleanup(setattr, P, "PATIENCE", self.patience)
        self.started = []

    def tearDown(self):
        for pid in self.started:
            for kill in (os.killpg, os.kill):
                try:
                    kill(pid, signal.SIGKILL)
                except (ProcessLookupError, PermissionError):
                    pass

    def start(self, *how):
        """-> (the leader, its child's pid). The child has said that it does not hear a request to end."""
        leader = subprocess.Popen([sys.executable, "-c", PARENT, CHILD, *how], stdout=subprocess.PIPE, text=True,
                                  start_new_session=True)
        self.addCleanup(leader.stdout.close)
        child = int(leader.stdout.readline())
        self.assertEqual(leader.stdout.readline().strip(), "deaf")
        self.started += [leader.pid, child]
        return leader, child

    def running(self, pid):
        listed = P.processes()
        return pid in listed and not listed[pid][2].startswith("Z")

    def test_a_child_that_does_not_end_when_asked_is_ended_and_seen_gone(self):
        """Was: true, with the child running. The group was asked to end, the leader did, and that was all."""
        leader, child = self.start()
        self.assertTrue(self.running(child) and leader.poll() is None)
        self.assertEqual(P.end(leader, []), (True, True))
        self.assertFalse(self.running(child))
        self.assertIsNotNone(leader.poll())

    def test_and_so_it_is_when_the_leader_had_ended_before(self):
        """Was: true, with the child running, and no signal sent at all."""
        leader, child = self.start("dies")
        self.assertEqual(leader.wait(timeout=20), 0)
        self.assertTrue(self.running(child))
        self.assertEqual(P.end(leader, []), (True, False))                   # (gone, and not stopped by this)
        self.assertFalse(self.running(child))

    def test_a_child_that_left_the_group_is_ended_while_it_can_be_found(self):
        leader, child = self.start("leaves")                                 # a session of its own: the leader's
        self.assertEqual(P.end(leader, []), (True, True))                    # child still, and found by that
        self.assertFalse(self.running(child))
        leader, child = self.start("leaves", "dies")                         # no group and no parent to find it by,
        leader.wait(timeout=20)                                              # but it is the stand-in, by its log:
        self.assertEqual(P.end(leader, [{"at": "connected", "pid": child, "nonce": "n1"}, {"at": "came", "pid": 1}]),
                         (True, False))
        self.assertFalse(self.running(child))

    def a_child_that_appears_in_the_wait(self, child_code):
        """Review of c2efaaa2, C1, as it was run. The leader has no child. Asked to end, it starts one in a
        session of the child's own, and ends when it is let. The system is asked what runs while the child is
        still the leader's; by the next look the leader has gone and the child has no parent to be found by.
        -> (what `end` said, the child is running after it, how long `end` took from that look on)."""
        folder = tempfile.mkdtemp(prefix="preflight-late-")
        let, born = os.path.join(folder, "let"), os.path.join(folder, "born")
        leader = subprocess.Popen([sys.executable, "-c", LATE, let, born, child_code], stdout=subprocess.PIPE, text=True,
                                  start_new_session=True)
        self.addCleanup(leader.stdout.close)
        self.assertEqual(leader.stdout.readline().strip(), "ready")
        self.started.append(leader.pid)
        real, looks, seen = P.processes, [], []

        def looked():
            looks.append(1)
            if len(looks) != 2:                                              # the first look in the wait:
                return real()
            for _ in range(400):                                             # the child is there, and the leader's
                listed = real()
                if os.path.exists(born):
                    with open(born, encoding="utf8") as f:
                        child = int(f.read())
                    if listed.get(child, (None,))[0] == leader.pid:
                        break
                time.sleep(0.02)
            self.started.append(child)
            seen.append((child, listed[child][1] != leader.pid, child in P.family(listed, leader.pid, set())))
            with open(let, "w", encoding="utf8"):                            # the leader is let go, and has ended
                pass                                                         # before this look is handed back
            leader.wait(timeout=20)
            looked.since = time.time()
            return listed
        with mock.patch.object(P, "processes", looked):
            said = P.end(leader, [])
            took = time.time() - looked.since
        (child, apart, family), = seen
        self.assertEqual((apart, family), (True, True))                      # (in a group of its own, and seen)
        return said, self.running(child), took

    def test_a_child_that_is_seen_in_the_wait_is_not_forgotten_when_its_parent_has_gone(self):
        """Only the look before each signal was kept, so the child was looked for no more once its parent had
        gone: gone, it was said, with the child running. It does not end when it is asked to, so that being
        asked at once does not stand in for being kept: it is found again by its own id, and ended."""
        said, running, took = self.a_child_that_appears_in_the_wait(CHILD)
        self.assertEqual((said, running), ((True, True), False))             # was: true, and the child running
        self.assertGreaterEqual(took, P.PATIENCE * 0.5)                      # (by the round that ends by force)

    def test_and_one_that_ends_when_asked_is_asked_as_soon_as_it_is_seen(self):
        said, running, took = self.a_child_that_appears_in_the_wait("print('up', flush=True); import time; time.sleep(600)")
        self.assertEqual((said, running), ((True, True), False))
        self.assertLess(took, P.PATIENCE)                                    # not left for the round that ends

    def test_what_cannot_be_ended_or_cannot_be_seen_is_not_called_gone(self):
        leader, child = self.start()
        with mock.patch.object(P.os, "killpg", lambda *a: None), mock.patch.object(P.os, "kill", lambda *a: None):
            self.assertEqual(P.end(leader, []), (False, True))               # (nothing ends: the signals go nowhere)
        self.assertTrue(self.running(child))
        with mock.patch.object(P, "processes", lambda: None):                # the system cannot be asked what runs
            self.assertEqual(P.end(leader, []), (False, False))
        real, asked = P.processes, []
        with mock.patch.object(P, "processes", lambda: None if asked else (asked.append(1), real())[1]), \
                mock.patch.object(P.os, "killpg", lambda *a: None), mock.patch.object(P.os, "kill", lambda *a: None):
            self.assertEqual(P.end(leader, []), (False, True))               # or can be asked once, and not again
        self.assertTrue(self.running(child))
        self.assertEqual(P.end(leader, []), (True, True))                    # (and now it is ended)
        self.assertFalse(self.running(child))

    def test_a_process_that_ends_when_asked(self):
        one = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"], start_new_session=True)
        self.started.append(one.pid)
        began = time.time()
        self.assertEqual(P.end(one, []), (True, True))
        self.assertEqual(one.poll(), -signal.SIGTERM)                        # asked, not ended by force,
        self.assertLess(time.time() - began, P.PATIENCE)                     # and not waited out

    def test_what_the_system_lists(self):
        listed = P.processes()
        mine = listed[os.getpid()]
        self.assertEqual((mine[0], mine[1]), (os.getppid(), os.getpgid(0)))
        some = {10: (1, 10, "S"), 11: (10, 10, "S"), 12: (11, 12, "S"), 13: (1, 10, "Z"), 14: (1, 14, "S"),
                15: (14, 14, "R"), 16: (1, 16, "S")}
        self.assertEqual(P.family(some, 10, {14, 99}), {10, 11, 12, 14, 15})
        # never this program, what it descends from, or the first process, whatever a log names: they would be
        # asked to end, and everything that descends from them with them
        me, parent = os.getpid(), os.getppid()
        tree = {**some, 1: (0, 1, "S"), parent: (1, parent, "S"), me: (parent, me, "S"), 20: (me, 20, "S")}
        for named in ({1}, {me}, {parent}, {0}, {1, me, parent}):
            self.assertEqual(P.family(tree, 10, named), {10, 11, 12}, named)
        self.assertEqual(P.family(tree, 10, {20}), {10, 11, 12, 20})         # (a child of this program can be named)
        self.assertEqual(P.family({**tree, me: (parent, 10, "S"), 21: (me, 10, "S")}, 10, set()), {10, 11, 12, 21})
        self.assertEqual(P.family({**tree, 1: (0, 10, "S")}, 10, set()), {10, 11, 12})   # (nor by the group's number)
        self.assertEqual(P.family(listed, 1, {1, me}), set())

    def a_form_of_a_process(self, let_go_in_the_first_look):
        """preflight.form, with everything a session that passes leaves, written for this run; and in place of
        Claude Code a process of this machine that ends with 1 when it is let, and is otherwise running until
        it is ended. The check's own ending is used, and the system is asked what runs."""
        out = os.path.join(tempfile.mkdtemp(prefix="preflight-real-"), "main")
        let, popen, run, processes, looks, made = out + ".let", subprocess.Popen, subprocess.run, P.processes, [], []

        def started(cmd, **k):
            if os.path.basename(cmd[0]) != "claude":
                return popen(cmd, **k)                                       # (`ps`, which the system is asked by)
            child = popen([sys.executable, "-c", WAITS, let], stdout=k["stdout"], stderr=k["stderr"],
                          stdin=k["stdin"], start_new_session=True)
            self.started.append(child.pid)
            made.append(child)
            with open(os.path.join(out, "run.json"), encoding="utf8") as f:
                nonce = json.load(f)["nonce"]
            gate, hooks, game, now = *good(), time.time()
            os.makedirs(os.path.join(out, "live", "hook"))
            for name, rows in (("stream.jsonl", [init()]), ("gate.jsonl", [dict(g, at=now) for g in gate]),
                               (os.path.join("live", "hook", "log.jsonl"), hooks),
                               ("game.jsonl", [{"at": "connected", "nonce": nonce}] + [dict(g, answered=now) for g in game[1:]])):
                with open(os.path.join(out, name), "a", encoding="utf8") as f:
                    f.write("".join(json.dumps(r) + "\n" for r in rows))
            return child

        def looked():
            looks.append(1)
            if let_go_in_the_first_look and len(looks) == 1:                 # while the system is being asked, and
                with open(let, "w", encoding="utf8"):                        # before any signal: it ends by itself
                    pass
                made[0].wait(timeout=20)
            return processes()
        with mock.patch.object(P.subprocess, "Popen", started), mock.patch.object(P, "processes", looked), \
                mock.patch.object(P.subprocess, "run", lambda cmd, **k: run(cmd, **k) if cmd[0] == "ps" else None):
            return P.form(out, "main", "tnr-relay", [])

    def test_a_session_that_ends_by_itself_while_the_system_is_asked_what_runs_was_not_stopped(self):
        """Review of c2efaaa2, C2, as it was run, through the form, the loop, the ending and the verdict. The
        session was running when the loop chose to stop it and when it was looked at once more. Then the
        system was asked what runs, which takes its time, and in that time the session ended with 1. No signal
        ever reached it: its group was gone. It was put down as stopped after its calls, and the form passed."""
        ran, said = self.a_form_of_a_process(let_go_in_the_first_look=True)
        self.assertEqual((ran, said["how the session ended"], said["it ended with"]), (False, P.BY_ITSELF, 1))
        self.assertEqual(said["why not"], f"the session was not stopped after its calls: {P.BY_ITSELF} (with 1)")
        self.assertEqual(said["calls the gate let through"], 3)              # (the rows are all there)
        ran, said = self.a_form_of_a_process(let_go_in_the_first_look=False)   # the same, and it runs until it is
        self.assertEqual((ran, said["how the session ended"], said["it ended with"], said["why not"]),
                         (True, P.STOPPED, -signal.SIGTERM, None))           # ended: stopped by the check


if __name__ == "__main__":
    unittest.main()
