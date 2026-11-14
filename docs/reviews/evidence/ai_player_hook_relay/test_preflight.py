"""The check for the operator's machine, off line: its gate, what it reads, and when it says yes.

    python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py

No session is started and nothing is sent: the brain's batches are made by the suite's rig, the logs are
written by hand, and the one process is a stand-in for Claude Code that prints what a test tells it to.
Review of 65974c02 (chatgpt/review-ai-player-relay-preflight-20261114 @ 5d46d7ef), B1 to B4.
"""
import io
import json
import os
import sys
import tempfile
import unittest

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
        self.assertIsNone(P.astray(through, came, {"u1": False}, 500.0))
        self.assertIsNone(P.astray(through, [], {}, 100.0 + P.LATE))                     # (no result yet, and in time)
        self.assertEqual(P.astray(through, [], {"u1": False}, 100.1), "a call was answered, and not by the stand-in")
        self.assertIsNone(P.astray(through, [], {"u1": True}, 900.0))                    # (refused after the gate: it never went)
        self.assertIn("has no result after", P.astray(through, [], {}, 100.1 + P.LATE))
        self.assertIn("did not let through", P.astray([], came, {}, 100.0))
        self.assertIn("did not let through", P.astray([dict(through[0], refused="x")], came, {}, 100.0))
        self.assertIn("not a read of my own profile", P.astray(through, [dict(came[0], endpoint="hospital.npcHeal")], {}, 100.0))
        self.assertIn("not a read of my own profile", P.astray(through, [dict(came[0], input={"userId": "x"})], {}, 100.0))
        self.assertIn("do not name their tool calls", P.astray(through, [dict(came[0], use=None)], {}, 100.0))
        self.assertIn("do not name their tool calls", P.astray(through * 2, came * 2, {}, 100.0))
        shown = P.results([{"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "u1", "is_error": True},
                                                                    {"type": "tool_result", "tool_use_id": "u2"}]}},
                           {"type": "assistant", "message": {"content": [{"type": "tool_result", "tool_use_id": "u3"}]}},
                           {"type": "user", "message": {"content": "text"}}, {"type": "user"}])
        self.assertEqual(shown, {"u1": True, "u2": False})

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
    def verdict(self, form="main", how=P.STOPPED, session=S, reaped=True, gate=None, hooks=None, game=None):
        g, h, s = good(form)
        return P.verdict(form, how, session, g if gate is None else gate, h if hooks is None else hooks,
                         s if game is None else game, reaped)

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
        for how in ("ended: the clock ran out", "the session ended by itself", "ended: a call was answered, and not by the stand-in",
                    "ended: the session did not show what it has in time", None, ""):
            self.assertIn("was not stopped after its calls", self.verdict(how=how))
        self.assertIn("could not be seen to end", self.verdict(reaped=False))

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


class Clock:
    def __init__(self):
        self.t = 1000.0

    def time(self):
        return self.t

    def sleep(self, s):
        self.t += s


class Stub:
    """In place of Claude Code: a process that is running until a test ends it."""
    pid, code = 4242, None

    def poll(self):
        return self.code

    def wait(self, timeout=None):
        return self.code


class TheSessionIsWatched(unittest.TestCase):
    """The loop itself, with a clock the test moves and no process: what a session printed is written by hand."""

    def setUp(self):
        self.out = tempfile.mkdtemp(prefix="preflight-loop-")
        self.nonce = P.prepare(self.out, "main", "tnr-relay")
        self.clock, self.stub, self.ended = Clock(), Stub(), []
        self.old = (P.time, P.subprocess.Popen, P.end)
        P.time = self.clock
        P.subprocess.Popen = lambda *a, **k: (self.started(), self.stub)[1]
        P.end = lambda p, game: (self.ended.append(self.clock.t), True)[1]
        self.says = None

    def tearDown(self):
        P.time, P.subprocess.Popen, P.end = self.old

    def started(self):
        if self.says is not None:
            with open(os.path.join(self.out, "stream.jsonl"), "a", encoding="utf8") as f:
                f.write(self.says)

    def log(self, name, *rows):
        os.makedirs(os.path.dirname(os.path.join(self.out, name)), exist_ok=True)
        with open(os.path.join(self.out, name), "a", encoding="utf8") as f:
            f.write("".join(json.dumps(r) + "\n" for r in rows))

    def run_it(self, done=lambda gate, hooks, game: False):
        return P.session(self.out, "main", ["--agent", "tnr-relay", "Begin."], [P.TOOL], done)

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
        self.log("gate.jsonl", {"kind": "start", "session": S})
        self.log("game.jsonl", {"at": "connected", "nonce": self.nonce, "pid": 1})
        self.assertEqual(self.run_it()[0], "the session ended by itself")


if __name__ == "__main__":
    unittest.main()
