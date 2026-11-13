"""The relay with hooks (director 2026-11-13, RUL-2026-11-13-157; player/hook.py).

Without hooks the model in the relay writes every call out in full and gets every result into its conversation,
and each batch is a model request that carries the whole conversation. With them the relay is printed a
stand-in for each call; a hook puts the real call in its place, and another takes the result out and hands it
to the brain. The model carries the batch's token and a number.

What must hold:
- the game gets the calls the brain made, in order, with their waits, and nothing else: whatever the model
  sends that is not the next line of the batch it holds is refused, and is not made;
- the brain gets every result, as it does from a relay without hooks;
- a relay whose hooks do not run sends nothing into the game, and is stopped;
- a relay without hooks is given its batches as before.

The hooks are run here the way Claude Code runs them: each gets the hook's input as a dict and gives its answer.
What that input holds is taken from a probe of Claude Code 2.1.323 (docs/reviews/evidence/ai_player_hook_relay).
"""
import contextlib
import io
import json
import os
import re
import subprocess
import unittest
from unittest import mock

from player import brain, calls as K, config as C, hook, relay
from player.brain.core import Brain
from player.tests.support import FOE, Rig, fixture, user
from player.tests.test_relay import token_of, transcript
from player.tests.test_rereview9 import WhatAVersionBeforeLeft

BEFORE = "661f3f63f9bd51887c402ce00f76e8e9735cb2ea"
"""The head this was built on (AP2's first part, approved): protocol 7."""

TOOL = "mcp__Tnr__callEndpoint"
AGENT = "a1b2c3d4e5f60718"
OK = [{"type": "text", "text": "ok"}]


class Hooks(unittest.TestCase):
    """A live folder, `brain next` as a relay runs it, the hooks as Claude Code runs them, and a stand-in for
    the game that answers whatever a hook lets through."""

    def start(self, mode="hunt"):
        self.r = r = Rig(mode)
        r.world.save()
        self.me, self.fails, self.game, self.shown, self.slept, self.uses = user(), {}, [], [], [], 0
        self.battle, self.log = fixture()
        with contextlib.ExitStack() as stack:
            stack.enter_context(mock.patch.object(
                brain, "Brain", lambda live: Brain(live, clock=lambda: r.t, combat=r.combat, gates=r.brain.gates)))
            stack.enter_context(mock.patch.object(brain.time, "time", lambda: r.t))
            stack.enter_context(mock.patch.dict(os.environ, {
                "TNR_PLAYER_NO_DAEMON": "1", "TNR_TRANSCRIPT": os.path.join(r.dir, "absent"),
                "TNR_PLAYER_FIGHTS": os.path.join(r.dir, "fights")}))
            self.addCleanup(stack.pop_all().close)

    def sleep(self, seconds):
        self.slept.append(round(seconds, 2))
        self.r.t += seconds

    def inp(self, tool, asked, agent=AGENT, **more):
        """A hook's input, as Claude Code gives it for a tool call of a subagent."""
        self.uses += 1
        row = {"session_id": "0f0f0f0f-aaaa-4bbb-8ccc-121212121212", "cwd": C.ROOT, "permission_mode": "auto",
               "transcript_path": os.path.join(self.r.dir, "projects", "main.jsonl"),
               "agent_id": agent, "agent_type": "tnr-relay", "hook_event_name": "PreToolUse", "tool_name": tool,
               "tool_input": asked, "tool_use_id": f"toolu_{self.uses:04d}"}
        if agent is None:
            del row["agent_id"], row["agent_type"]                          # the relay is the session's main agent
        row.update(more)
        return row

    def bash(self, command, agent=AGENT, **more):
        """The Bash hook's answer to a command: (the command that is run, None) or (None, why it is refused)."""
        said = hook.run("bash", self.inp("Bash", {"command": command, "description": "x"}, agent, **more), self.r.dir)
        said = said["hookSpecificOutput"]
        if said["permissionDecision"] == "allow":
            self.assertEqual(said["updatedInput"]["description"], "x")      # (the rest of the input is kept)
            return said["updatedInput"]["command"], None
        return None, said["permissionDecisionReason"]

    def next(self, token=None, agent=AGENT, hooked=True):
        """The relay runs its `brain next` line. -> (the token to come back with, the batch's lines but the
        last, every line)."""
        command = "python3 -m player.brain next" if token is None else json.loads(relay.next_line(token))["bash"]
        hooks = None
        if hooked:
            command, why = self.bash(command, agent)
            self.assertIsNone(why)
            command, hooks = command.split(" --hooks ")
        out = io.StringIO()
        brain.next_batch(self.r.dir, token, out, self.sleep, hooks=hooks)
        lines = out.getvalue().splitlines()
        stop = lines[-1].startswith("STOP")
        return (None if stop else token_of(lines[-1])), [json.loads(x) for x in lines[:None if stop else -1] if x[:1] == "{"], lines

    def call(self, line, agent=AGENT, tool=TOOL, sleep=None):
        """The model makes one tool call for a line it was printed. -> what it is shown for it."""
        asked = {"endpointName": line["call"], "input": line["input"]}
        asked.update({k: line[k] for k in ("select",) if k in line})
        inp = self.inp(tool, asked, agent)
        said = hook.run("pre", inp, self.r.dir, sleep or self.sleep)["hookSpecificOutput"]
        if said["permissionDecision"] != "allow":
            self.shown.append(said["permissionDecisionReason"])
            return self.shown[-1]
        real = said["updatedInput"]
        self.game.append(real)
        self.r.t += 0.4                                                     # the call takes a moment
        if real["endpointName"] in self.fails:
            failed = dict(inp, hook_event_name="PostToolUseFailure", tool_input=real,
                          error=self.fails[real["endpointName"]])
            self.assertIsNone(hook.run("fail", failed, self.r.dir))
            self.shown.append(self.fails[real["endpointName"]])
        else:
            self.shown.append(self.after(inp, real, [{"type": "text", "text": json.dumps(self.answer(real))}]))
        return self.shown[-1]

    def after(self, inp, real, response):
        done = dict(inp, hook_event_name="PostToolUse", tool_input=real, tool_response=response, duration_ms=400)
        return hook.run("post", done, self.r.dir)["hookSpecificOutput"]["updatedToolOutput"]

    def answer(self, real):
        """The game."""
        ep = real["endpointName"]
        if ep == "profile.getUser":
            return self.me.data
        if ep == "combat.getBattle":
            return dict(self.battle, **({"battle.usersEffects": []} if "battle.usersEffects" in real["select"] else {}))
        if ep == "combat.getBattleEntries":
            return self.log
        return {"success": True}

    def does(self, lines):
        self.r.t += 1
        return [self.call(x) for x in lines]

    def first_batch(self, **kw):
        """A new relay asks twice: once for its name, once for a batch. -> (token, lines)."""
        token, _, _ = self.next(**kw)
        token, lines, _ = self.next(token, **kw)
        return token, lines

    def client(self):
        return relay.read(os.path.join(self.r.dir, "client.json"))

    def into_a_fight(self):
        """The relay finds the character in a fight, reads it, and is printed my turn. -> (token, lines)."""
        self.me = user("BATTLE", bid="B1")
        self.r.combat.kits.add(FOE)
        token, lines = self.first_batch()
        for _ in range(3):
            if len(self.game) >= 3:
                break
            self.does(lines)
            token, lines, _ = self.next(token)
        return token, lines

    def handed_to_the_brain(self):
        """Every result the brain has been handed, as its requests carried them."""
        got, real, self.asks = [], brain.serve, []

        def serve(b, live, req):
            self.asks.append(relay.read(req) or {})
            got.extend(relay.unpack(self.asks[-1].get("results")))
            return real(b, live, req)
        patch = mock.patch.object(brain, "serve", serve)
        patch.start()
        self.addCleanup(patch.stop)
        return got


class TheOneCommand(Hooks):
    def setUp(self):
        self.start()

    def test_brain_next_is_let_through_with_the_relays_id_behind_it(self):
        line = json.loads(relay.next_line("ab12cd-7"))["bash"]
        for command in ("python3 -m player.brain next", f"cd {C.ROOT} && python3 -m player.brain next", line):
            self.assertEqual(self.bash(command), (f"{command} --hooks {AGENT}", None))
        self.assertEqual(self.bash(f"  {line}\n")[0], f"{line} --hooks {AGENT}")      # (space around it is nothing)

    def test_a_relay_that_is_the_sessions_main_agent_is_known_by_the_session(self):
        self.assertEqual(self.bash("python3 -m player.brain next", agent=None)[0],
                         "python3 -m player.brain next --hooks 0f0f0f0f-aaaa-4bbb-8ccc-121212121212")

    def test_no_other_command_is_run(self):
        line = json.loads(relay.next_line("ab12cd-7"))["bash"]
        for command in ("ls /", "python3 -c 'import time; time.sleep(1.2)'", line + " && rm -rf x", line + "; ls",
                        line + " --hooks someone", "cd /elsewhere && python3 -m player.brain next ab12cd-7",
                        "python3 -m player.brain stopped all", "python3 -m player.brain set paused=false",
                        "python3 -m player.brain put ab12cd-7 1", "python3 -m player.brain next ab12cd-7 extra",
                        "python3 -m player.brain next $(id)", "", "python3 -m player.brain run"):
            self.assertEqual(self.bash(command)[0], None, command)
        self.assertIn("no other command", self.bash("ls /")[1])

    def test_an_id_that_cannot_be_passed_on_safely_is_not(self):
        for bad in ("a b", "a;ls", "$(id)", "", "x" * 81, 7):
            self.assertEqual(self.bash("python3 -m player.brain next", agent=None, session_id=bad)[0], None, bad)

    def test_the_command_line_takes_the_id(self):
        seen = []
        with mock.patch.object(brain, "next_batch", lambda live, token=None, **kw: seen.append((token, kw)) or 0), \
                mock.patch.dict(os.environ, {"TNR_PLAYER_LIVE": self.r.dir}):
            for argv in (["next"], ["next", "ab12cd-7"], ["next", "--hooks", AGENT], ["next", "ab12cd-7", "--hooks", AGENT],
                         ["next", "ab12cd-7", "--hooks"]):
                self.assertEqual(brain.main(argv), 0)
        self.assertEqual(seen, [(None, {"hooks": None}), ("ab12cd-7", {"hooks": None}), (None, {"hooks": AGENT}),
                                ("ab12cd-7", {"hooks": AGENT}), ("ab12cd-7", {"hooks": None})])


class WhatSuchARelayIsPrinted(Hooks):
    def setUp(self):
        self.start()

    def test_a_stand_in_for_each_call_and_the_next_line(self):
        token, lines = self.first_batch()
        self.assertEqual(lines, [{"call": C.STAND_IN, "input": {"b": token, "n": 1}}])
        self.does(lines)
        token, lines, printed = self.next(token)
        self.assertEqual(lines, [{"call": C.STAND_IN, "input": {"b": token, "n": k}} for k in (1, 2, 3, 4)])
        self.assertEqual(printed[-1], relay.next_line(token))
        self.assertEqual(self.client()["hooks"], AGENT)
        kept = [s for s in self.client()["steps"] if "call" in s]           # the batch itself, for the hook
        self.assertEqual([s["call"] for s in kept], ["profile.getUser", "travel.getSectorData", "stealth.useSensory",
                                                     "profile.getStrongestUsers"])
        self.assertTrue(all(s["select"] for s in kept))

    def test_no_wait_and_no_put_line_though_no_transcript_can_be_read(self):
        token, lines = self.into_a_fight()                                  # my turn: two actions, 1.2 s apart
        steps = self.client()["steps"]
        self.assertIn({"wait": C.ACTION_GAP}, steps)
        self.assertEqual([set(x) for x in lines], [{"call", "input"}] * sum("call" in s for s in steps))

    def test_a_relay_without_hooks_is_printed_its_calls_as_before(self):
        token, lines = self.first_batch(hooked=False)
        self.assertEqual(lines[0], {"call": "profile.getUser", "input": {}, "select": K.user()["select"]})
        self.assertIn("put", lines[1])                                      # (no transcript: it hands results in)
        self.assertIsNone(self.client()["hooks"])
        self.assertEqual(brain.put(self.r.dir, token, 1, json.dumps(self.me.data)), 0)
        token, lines, _ = self.next(token, hooked=False)
        self.assertEqual([x["call"] for x in lines if "call" in x][:2], ["profile.getUser", "travel.getSectorData"])

    def test_a_relay_is_with_hooks_or_without_from_its_first_ask_to_its_last(self):
        token, lines = self.first_batch()
        self.does(lines)
        before = self.client()
        self.assertEqual(self.next(token, hooked=False)[2], [hook.NO_HOOKS])    # its hook did not run this time
        self.assertEqual(self.next(token, agent="b" * 16)[2], [hook.NO_HOOKS])  # or it is not that relay at all
        self.assertEqual(self.client(), before)                              # nothing was taken from either
        self.assertEqual(len(self.next(token)[1]), 4)                        # the relay itself carries on

    def test_a_relay_that_began_without_hooks_does_not_get_them_later(self):
        token, lines = self.first_batch(hooked=False)
        self.assertEqual(self.next(token)[2], [hook.NO_HOOKS])


class WhatTheHookLetsThrough(Hooks):
    def setUp(self):
        self.start()

    def test_the_calls_the_brain_made_in_order_and_the_model_is_shown_ok(self):
        token, lines = self.first_batch()
        self.assertEqual(self.does(lines), [OK])
        token, lines, _ = self.next(token)
        self.assertEqual(self.does(lines), [OK] * 4)
        want = [{"endpointName": s["call"], "input": s["input"], "select": s["select"]}
                for s in [K.user(), K.user(), K.sector(1538)]]
        self.assertEqual(self.game[:3], want)
        self.assertEqual([g["endpointName"] for g in self.game[3:]], ["stealth.useSensory", "profile.getStrongestUsers"])

    def test_the_waits_of_a_batch_are_spent_by_the_hook(self):
        token, lines = self.into_a_fight()
        self.slept, at = [], []
        for line in lines:
            self.call(line)
            at.append(self.r.t)
        acts = [g["input"]["actionId"] for g in self.game if g["endpointName"] == "combat.performAction"]
        self.assertEqual(len(acts), 2)
        self.assertEqual(self.slept, [C.ACTION_GAP])                        # in front of the second action, once
        self.assertAlmostEqual(at[1] - at[0], C.ACTION_GAP + 0.4, places=3)

    def refused(self, line, **kw):
        n = len(self.game)
        why = self.call(line, **kw)
        self.assertEqual(len(self.game), n, why)                            # the game did not see it
        self.assertIsInstance(why, str)
        return why

    def test_anything_that_is_not_a_line_of_the_batch_is_refused(self):
        token, lines = self.first_batch()
        one = lines[0]
        for line in ({"call": "profile.getUser", "input": {}},                              # a real call, by hand
                     {"call": "item.buy", "input": {"itemId": "x", "stack": 1}},
                     dict(one, select=["userData.status"]),                                 # a stand-in and more
                     {"call": C.STAND_IN, "input": dict(one["input"], x=1)},
                     {"call": C.STAND_IN, "input": {"b": token}},
                     {"call": C.STAND_IN, "input": {"b": token, "n": "1"}},
                     {"call": C.STAND_IN, "input": {"b": token, "n": True}},
                     {"call": C.STAND_IN, "input": {"b": token, "n": 1.0}},
                     {"call": C.STAND_IN, "input": [token, 1]},
                     {"call": "text relay", "input": one["input"]}):                        # (the probe's model did)
            self.assertIn("not a line of the batch", self.refused(line), line)
        self.assertIn("not a line", self.refused(one, tool="mcp__other__tool"))             # another tool
        self.assertEqual(self.call(one), OK)                                 # and the line itself goes

    def test_a_call_the_batch_has_not_got(self):
        token, lines = self.first_batch()
        for n in (0, 2, -1, 99):
            self.assertIn("no such call", self.refused({"call": C.STAND_IN, "input": {"b": token, "n": n}}))

    def test_a_call_is_made_once(self):
        token, lines = self.first_batch()
        self.assertEqual(self.call(lines[0]), OK)
        self.assertIn("made already", self.refused(lines[0]))
        self.assertEqual(len(self.game), 1)

    def test_a_batch_is_made_in_order_and_is_cut_where_a_call_is_left_out(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertIn("call 1 of the batch comes first", self.refused(lines[1]))
        self.assertEqual(self.call(lines[0]), OK)
        self.assertIn("call 2 of the batch comes first", self.refused(lines[2]))            # 2 was left out
        self.assertIn("call 3 of the batch comes first", self.refused(lines[3]))
        self.assertEqual(self.call(lines[1]), OK)                            # (refused before its turn: not used up)
        self.assertEqual(len(self.game), 3)

    def test_a_call_waits_for_the_one_before_it_to_be_answered(self):
        """Claude Code may start the tool calls of one message together. The second is held until the first has
        its answer, and is refused if that does not come."""
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        first = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]})
        real = hook.run("pre", first, self.r.dir, self.sleep)["hookSpecificOutput"]["updatedInput"]
        looks = []

        def then_it_answers(seconds):                                       # the first call's answer comes meanwhile
            looks.append(seconds)
            if len(looks) == 3:
                self.after(first, real, [{"type": "text", "text": json.dumps(self.me.data)}])
        self.assertEqual(self.call(lines[1], sleep=then_it_answers), OK)
        self.assertEqual(looks, [hook.LOOK] * 3)
        third = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[2]["input"]})
        hook.run("pre", third, self.r.dir, self.sleep)                       # the third is made, and never answered
        self.slept = []
        self.assertIn("call 3 of the batch has not been answered", self.refused(lines[3]))
        self.assertAlmostEqual(sum(self.slept), hook.TURN, places=2)

    def test_a_batch_that_is_not_the_one_the_relay_holds(self):
        token, lines = self.first_batch()
        self.does(lines)
        old = lines[0]
        token, lines, _ = self.next(token)
        self.assertIn("not the one this relay holds", self.refused(old))                    # the batch before
        self.assertIn("not the one this relay holds",
                      self.refused({"call": C.STAND_IN, "input": {"b": "ffffff-9", "n": 1}}))
        self.assertEqual(self.call(lines[0]), OK)

    def test_a_batch_that_has_been_handed_in(self):
        """From the moment the brain has a batch's results until the next batch is printed, the relay sits in
        `brain next`. A call of the old batch that comes then (started together with it, say) is not made."""
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.call(lines[0])
        late = []

        def meanwhile(seconds):                                             # the brain-side wait
            self.sleep(seconds)
            late.append(self.refused(lines[1]))
        with mock.patch.object(brain, "_await", lambda *a, **k: dict(self.a_batch(), hold=2.0)):
            brain.next_batch(self.r.dir, token, io.StringIO(), meanwhile, hooks=AGENT)
        self.assertEqual(len(late), 1)
        self.assertIn("handed in", late[0])

    def a_batch(self, until=None):
        return {"protocol": relay.PROTOCOL, "id": "feedfeed", "steps": [K.user()], "stop": None, "until": until}

    def test_the_cutoff_a_batch_was_made_under_is_kept_for_the_hook(self):
        token, lines = self.first_batch()
        self.does(lines)
        with mock.patch.object(brain, "_await", lambda *a, **k: dict(self.a_batch(self.r.t + 50), hold=0.0)):
            token, lines, _ = self.next(token)
        self.assertEqual(self.client()["until"], self.r.t + 50)
        self.r.t += 50
        self.assertIn("lease", self.refused(lines[0]))

    def test_a_batch_the_brain_has_not_taken_yet_can_still_be_finished(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.call(lines[0])
        with mock.patch.object(brain, "_await", lambda *a, **k: None):       # the brain gives no answer for now
            self.assertEqual(self.next(token)[2], [relay.next_line(token)])
        self.assertEqual(self.call(lines[1]), OK)                            # nothing was taken: the batch stands

    def test_another_agents_call_for_this_relays_batch(self):
        token, lines = self.first_batch()
        self.assertIn("another relay's", self.refused(lines[0], agent="b" * 16))
        self.assertIn("another relay's", self.refused(lines[0], agent=None))                 # the main session
        self.assertEqual(self.call(lines[0]), OK)

    def test_a_relay_that_was_replaced_makes_no_more_calls(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.call(lines[0])
        new, new_lines = self.first_batch(agent="c" * 16)                    # a new relay takes over
        self.assertIn("another relay's", self.refused(lines[1]))             # the old one goes on with its batch
        self.assertEqual(self.next(token)[2], [brain.SUPERSEDED])
        self.assertEqual(self.call(new_lines[0], agent="c" * 16), OK)

    def test_a_call_due_at_or_after_the_run_locks_cutoff(self):
        token, lines = self.into_a_fight()
        state = self.client()
        self.assertIsNone(state["until"])                                    # a rehearsal has no lease
        state["until"] = self.r.t + 1.0                                      # a lease that ends between the actions
        relay.write(os.path.join(self.r.dir, "client.json"), state)
        self.assertEqual(self.call(lines[0]), OK)
        self.assertIn("lease", self.refused(lines[1]))                       # 1.2 s on: past it, after its wait
        self.assertIn("lease", self.refused(lines[2]))                       # and everything behind it
        for bad in ("soon", True, self.r.t - 5, self.r.t):                   # (at the cutoff is past it)
            state.update(until=bad, token=state["token"])
            relay.write(os.path.join(self.r.dir, "client.json"), state)
            self.assertIn("lease", self.refused(lines[2]), bad)

    def test_with_no_relay_on_record_or_another_versions_file_nothing_goes(self):
        token, lines = self.first_batch()
        state = self.client()
        for other in (dict(state, protocol=relay.PROTOCOL - 1), dict(state, hooks=None), dict(state, steps=None),
                      "not json at all"):
            relay.write(os.path.join(self.r.dir, "client.json"), other)
            self.assertIn("no relay with hooks", self.refused(lines[0]), other)
        os.unlink(os.path.join(self.r.dir, "client.json"))
        self.assertIn("no relay with hooks", self.refused(lines[0]))

    def test_a_hook_that_fails_refuses(self):
        token, lines = self.first_batch()
        with mock.patch.object(hook, "calls", side_effect=RuntimeError("boom")):
            self.assertIn("the relay's hook failed", self.refused(lines[0]))
        out = io.StringIO()
        self.assertEqual(hook.main(["pre"], io.StringIO("not json"), out), 0)      # an input that cannot be read
        self.assertEqual(json.loads(out.getvalue())["hookSpecificOutput"]["permissionDecision"], "deny")
        with contextlib.redirect_stderr(io.StringIO()) as said:
            self.assertEqual(hook.main(["what"], io.StringIO("{}"), io.StringIO()), 2)
        self.assertIn("python3 -m player.hook pre", said.getvalue())

    def test_the_log_says_what_was_refused_and_why(self):
        token, lines = self.first_batch()
        self.refused({"call": "item.buy", "input": {}})
        self.call(lines[0])
        with open(os.path.join(self.r.dir, "hook", "log.jsonl"), encoding="utf8") as f:
            rows = [json.loads(x) for x in f]
        self.assertEqual([(x["hook"], x["refused"] is None) for x in rows[-3:]],
                         [("pre", False), ("pre", True), ("post", True)])
        self.assertTrue(all(x["by"] == AGENT for x in rows))


class WhatTheBrainGets(Hooks):
    def setUp(self):
        self.start()
        self.got = self.handed_to_the_brain()

    def test_every_result_as_from_a_relay_without_hooks(self):
        self.me = user(sector=1490, hp=4321)
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertEqual([(x.endpoint, x.input, x.error) for x in self.got], [("profile.getUser", {}, None)])
        self.assertEqual(self.got[0].data, self.me.data)
        self.assertEqual(relay.read(os.path.join(self.r.dir, "world.json"))["character"]["sector"], 1490)
        self.assertEqual([f for f in os.listdir(os.path.join(self.r.dir, "inbox")) if f.startswith("put-")], [])
        self.does(lines)
        self.next(token)
        self.assertEqual([x.endpoint for x in self.got[1:]], [s["endpointName"] for s in self.game[1:]])
        self.assertEqual([e for e in self.r.events("finding") if e["about"] == "relay"], [])   # no call is a stray

    def test_a_call_that_failed(self):
        token, lines = self.first_batch()
        self.fails = {"profile.getUser": "MCP error -32000: Too Many Requests"}
        self.assertEqual(self.does(lines), [self.fails["profile.getUser"]])  # (the model sees the error itself)
        self.next(token)
        self.assertEqual([(x.endpoint, x.data, x.error) for x in self.got], [("profile.getUser", None, brain.RATE_LIMITED)])

    def test_a_call_the_connector_refused_in_its_own_words(self):
        token, lines = self.first_batch()
        self.fails = {"profile.getUser": "connection reset by peer"}
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertEqual([(x.data, x.error) for x in self.got], [(None, "connection reset by peer")])
        self.fails = {"profile.getUser": ""}                                 # a failure with nothing said of it
        self.does(lines[:1])
        token, lines, _ = self.next(token)
        self.assertEqual((self.got[-1].data, self.got[-1].error), (None, "Error: no text"))
        self.fails = {}
        inp = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]})
        real = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"]["updatedInput"]
        self.assertEqual(self.after(inp, real, [{"type": "text", "text": "Error: endpoint not available"}]), OK)
        self.next(token)
        self.assertEqual((self.got[-1].data, self.got[-1].error), (None, "Error: endpoint not available"))

    def test_a_result_in_any_shape_claude_code_gives_one(self):
        shapes = (lambda t: [{"type": "text", "text": t}], lambda t: t, lambda t: {"content": [{"type": "text", "text": t}]},
                  lambda t: [{"type": "text", "text": t[:9]}, {"type": "text", "text": t[9:]}])
        token, lines = self.first_batch()
        for shape in shapes:
            inp = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]})
            real = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"]["updatedInput"]
            self.assertEqual(self.after(inp, real, shape(json.dumps(self.me.data))), OK)
            token, lines, _ = self.next(token)
            self.assertEqual((self.got[-1].endpoint, self.got[-1].data), (real["endpointName"], self.me.data))

    def test_a_result_too_large_for_the_conversation_is_read_from_where_it_was_saved(self):
        token, lines = self.first_batch()
        inp = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]})
        real = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"]["updatedInput"]
        saved = os.path.join(os.path.dirname(inp["transcript_path"]), "main", "tool-results", "toolu_x.txt")
        os.makedirs(os.path.dirname(saved))
        with open(saved, "w", encoding="utf8") as f:
            f.write(json.dumps(self.me.data))
        notice = f"Error: result (99,999 characters) exceeds maximum allowed tokens. Output has been saved to {saved}."
        self.assertEqual(self.after(inp, real, [{"type": "text", "text": notice}]), OK)
        token, lines, _ = self.next(token)
        self.assertEqual(self.got[-1].data, self.me.data)
        inp = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]})
        real = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"]["updatedInput"]
        outside = notice.replace(saved, "/etc/hostname.txt")                 # a notice that names a file elsewhere
        self.assertEqual(self.after(inp, real, [{"type": "text", "text": outside}]), OK)
        self.next(token)
        self.assertIn("unreadable result", self.got[-1].error)

    def test_a_tool_call_that_no_hook_let_through_gives_no_result(self):
        token, lines = self.first_batch()
        stray = self.inp(TOOL, {"endpointName": "profile.getUser", "input": {}})
        self.assertEqual(self.after(stray, stray["tool_input"], [{"type": "text", "text": "{}"}]), OK)   # still not shown
        self.assertIsNone(hook.run("fail", dict(stray, error="x"), self.r.dir))
        self.assertEqual(os.listdir(os.path.join(self.r.dir, "inbox")), [])
        self.does(lines)
        self.next(token)
        self.assertEqual(len(self.got), 1)

    def test_a_result_that_cannot_be_taken_is_still_not_shown_to_the_model(self):
        token, lines = self.first_batch()
        inp = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]})
        real = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"]["updatedInput"]
        with mock.patch.object(relay, "put", side_effect=OSError("disk")):
            self.assertEqual(self.after(inp, real, [{"type": "text", "text": json.dumps(self.me.data)}]), OK)
        self.next(token)
        self.assertEqual(self.got, [])                                       # the brain is told nothing came

    def test_its_transcript_is_read_for_the_tokens_and_nothing_else(self):
        """A relay with hooks has a transcript too: its stand-ins, "ok" for each result, and what each request
        cost. None of those calls is a result, and none is a call the batch did not ask for."""
        path = os.path.join(self.r.dir, "relay.jsonl")
        token, lines = self.first_batch()
        self.does(lines)
        t, rows = self.r.t, [("bash", "b0", "python3 -m player.brain next", self.r.t - 9)]
        rows += [("usage", "req1", 3, 5400, 120, t), ("use", "u1", C.STAND_IN, lines[0]["input"], t),
                 ("res", "u1", "ok", t), ("bash", "b1", json.loads(relay.next_line(token))["bash"], t)]
        transcript(path, rows)
        with mock.patch.dict(os.environ, {"TNR_TRANSCRIPT": path}):
            token, lines, _ = self.next(token)
        self.assertEqual([x.endpoint for x in self.got], ["profile.getUser"])                 # from the hook, once
        self.assertEqual(self.got[0].data, self.me.data)
        with open(os.path.join(self.r.dir, "tokens.jsonl"), encoding="utf8") as f:
            row = json.loads(f.read().splitlines()[-1])
        self.assertEqual((row["in"], row["out"], row["context"]), (5403, 120, 5403))
        self.assertEqual((row["cached"], row["written"], row["hooks"]), (5400, 0, True))   # what the plan counts by
        self.assertEqual(self.asks[-1]["clock"], "ours")                     # the results' times are the hook's
        self.assertEqual([e for e in self.r.events("finding") if e["about"] == "relay"], [])


class ARelayWhoseHooksDoNotRun(Hooks):
    def setUp(self):
        self.start()

    def test_it_is_stopped_before_it_is_printed_a_second_batch_of_calls(self):
        """Its `brain next` came through the Bash hook, so it was printed stand-ins. The hook in front of the
        connector did not run (the tool has another name on this machine, say): they went to the connector as
        they stood, which knows no such endpoint. Nothing reached the game, and no result will ever come."""
        token, lines = self.first_batch()
        self.r.t += 2                                                       # (the model made the call: no hook ran)
        self.assertEqual(self.next(token)[2], [hook.NO_HOOKS])
        self.assertEqual(self.game, [])
        self.assertEqual(self.next(token)[2], [hook.NO_HOOKS])               # and however often it asks

    def test_a_relay_whose_hooks_have_run_is_not_stopped_for_a_batch_it_left_out(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertTrue(self.client()["seen"])
        token, lines, printed = self.next(token)                             # it made none of the four calls
        self.assertNotIn(hook.NO_HOOKS, printed)
        self.assertTrue(lines)

    def test_a_refused_call_is_a_hook_that_ran(self):
        token, lines = self.first_batch()
        self.call({"call": C.STAND_IN, "input": {"b": token, "n": 5}})       # refused: but the hook was there
        self.assertNotIn(hook.NO_HOOKS, self.next(token)[2])

    def test_what_is_on_record_of_a_batch_goes_with_the_next(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.does(lines)
        folder = os.path.join(self.r.dir, "hook")
        self.assertEqual(sorted(os.listdir(folder)),
                         [f"{token}.{k}.json" for k in (1, 2, 3, 4)] + [f"{token}.seen", "log.jsonl"])

    def test_a_call_is_one_tool_calls_however_many_ask_for_it_at_once(self):
        token, lines = self.first_batch()
        self.assertTrue(hook._mine(self.r.dir, token, 1, "toolu_a"))
        with mock.patch.object(hook.os, "getpid", return_value=os.getpid() + 1):   # (another hook's process)
            self.assertFalse(hook._mine(self.r.dir, token, 1, "toolu_b"))
        self.assertEqual(relay.read(os.path.join(self.r.dir, "hook", f"{token}.1.json"))["use"], "toolu_a")
        self.assertEqual([f for f in os.listdir(os.path.join(self.r.dir, "hook")) if f.count(".") > 2], [])


class TheSameGameEitherWay(Hooks):
    """One session, played twice against the same stand-in for the game: by a relay without hooks, which is
    printed the calls and hands the results in with `brain put`; and by a relay with hooks. The game sees the
    same calls at the same moments, and the brain ends in the same place."""

    def play(self, hooked, batches=9):
        self.start()
        self.r.combat.kits.add(FOE)
        seen, at = [], []
        token, _, _ = self.next(hooked=hooked)
        for i in range(batches):
            token, lines, _ = self.next(token, hooked=hooked)
            self.me = user("BATTLE", bid="B1") if i >= 2 else user()        # a fight finds the character
            self.r.t += 1
            n = 0
            for line in lines:
                if "bash" in line:                                           # (a wait, as a relay without hooks runs it)
                    self.r.t += float(line["bash"].split("sleep(")[1].split(")")[0])
                elif hooked:
                    self.call(line)
                    at.append(round(self.r.t, 2))
                elif "call" in line:
                    n += 1
                    real = {"endpointName": line["call"], "input": line["input"], "select": line["select"]}
                    self.game.append(real)
                    self.r.t += 0.4
                    at.append(round(self.r.t, 2))
                    self.assertEqual(brain.put(self.r.dir, token, n, json.dumps(self.answer(real))), 0)
            seen.append(len(self.game))
        world = relay.read(os.path.join(self.r.dir, "world.json"))
        return self.game, at, seen, {k: world[k] for k in ("character", "battle", "map", "records")}

    def test_it(self):
        plain = self.play(False)
        hooked = self.play(True)
        self.assertGreater(len(plain[0]), 20)
        self.assertIn("combat.performAction", [g["endpointName"] for g in plain[0]])
        self.assertEqual(hooked[0], plain[0])                                # the same calls, in the same order
        self.assertEqual(hooked[1], plain[1])                                # at the same moments
        self.assertEqual(hooked[2], plain[2])                                # batch for batch
        self.assertEqual(hooked[3], plain[3])                                # and the brain knows the same


class TheHeadBeforeTheHooks(WhatAVersionBeforeLeft):
    def test_what_it_left_is_another_versions(self):
        """661f3f63 knows no hooks: a relay it named would be printed calls, and a batch it made carries no
        steps for a hook. The number is 8, so nothing it left is taken for this version's."""
        self.nothing_it_made_is_delivered(BEFORE)


class TheAgentFile(unittest.TestCase):
    def test_the_relays_agent_runs_the_four_hooks_and_a_failing_one_blocks(self):
        with open(os.path.join(C.ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
            _, head, _ = f.read().split("---\n", 2)
        block = head[head.index("hooks:"):]
        for event, matcher, what in (("PreToolUse", "Bash", "bash"), ("PreToolUse", "mcp__.*", "pre"),
                                     ("PostToolUse", "mcp__.*", "post"), ("PostToolUseFailure", "mcp__.*", "fail")):
            part = block[block.index(f"  {event}:"):]
            self.assertIn(f'matcher: "{matcher}"', part)
            self.assertIn(f'python3 -m player.hook {what}"', part)
        self.assertEqual(block.count("onFailure: block"), 2)                 # the two that stand in front of a call
        before = block[:block.index("  PostToolUse:")]
        self.assertEqual(before.count("onFailure: block"), 2)

    def test_its_commands_run_as_they_are_written(self):
        """Each command of the agent file, run by a shell as Claude Code runs it: from the session's folder,
        the hook's input on standard input, its answer on standard output, exit 0."""
        with open(os.path.join(C.ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
            commands = [json.loads(x) for x in re.findall(r'command: ("(?:[^"\\]|\\.)*")', f.read())]
        self.assertEqual(len(commands), 4)
        live = Rig().dir
        env = dict(os.environ, TNR_PLAYER_LIVE=live, CLAUDE_PROJECT_DIR=C.ROOT)

        def run(command, inp, cwd=C.ROOT, **more):
            done = subprocess.run(command, shell=True, cwd=cwd, env=dict(env, **more), input=json.dumps(inp),
                                  capture_output=True, text=True, timeout=60)
            self.assertEqual((done.returncode, done.stderr), (0, ""), command)
            return json.loads(done.stdout) if done.stdout.strip() else None
        bash, pre, post, fail = commands
        said = run(bash, {"tool_name": "Bash", "tool_input": {"command": "python3 -m player.brain next"},
                          "agent_id": AGENT})["hookSpecificOutput"]
        self.assertEqual((said["permissionDecision"], said["updatedInput"]["command"]),
                         ("allow", f"python3 -m player.brain next --hooks {AGENT}"))
        call = {"tool_name": TOOL, "tool_input": {"endpointName": C.STAND_IN, "input": {"b": "ab12cd-1", "n": 1}},
                "tool_use_id": "toolu_1", "agent_id": AGENT}
        said = run(pre, call, cwd=os.path.join(C.ROOT, "player"))["hookSpecificOutput"]   # (wherever the session is)
        self.assertEqual((said["permissionDecision"], said["permissionDecisionReason"]),
                         ("deny", "no relay with hooks holds a batch"))
        self.assertEqual(run(post, dict(call, tool_response=[{"type": "text", "text": "{}"}]))["hookSpecificOutput"],
                         {"hookEventName": "PostToolUse", "updatedToolOutput": OK})
        self.assertIsNone(run(fail, dict(call, error="x")))
        with open(os.path.join(live, "hook", "log.jsonl"), encoding="utf8") as f:
            self.assertEqual([json.loads(x)["hook"] for x in f], ["bash", "pre", "post", "fail"])


if __name__ == "__main__":
    unittest.main()
