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

And since the review of 184ce648 (player/hooked.py):
- no hook removes what is on record of a batch, so no call goes twice when a relay is replaced (H1);
- a batch is closed before it is handed in: every call that went is waited for, nothing of it goes after, and
  the brain is handed the same however often `brain next` is run (H2);
- a result is taken out of the model's sight only when it is written down for the brain (H3);
- calls whose hooks start together still go in order.

The hooks are run here the way Claude Code runs them: each gets the hook's input as a dict and gives its answer.
What that input holds is taken from a probe of Claude Code 2.1.323 (docs/reviews/evidence/ai_player_hook_relay).
"""
import contextlib
import io
import json
import os
import re
import subprocess
import threading
import unittest
from unittest import mock

from player import brain, calls as K, config as C, hook, hooked, relay
from player.brain import client
from player.brain.core import Brain
from player.tests.support import FOE, Rig, fixture, user
from player.tests.test_ap2_rereview1 import PRICES, READS, SHORT
from player.tests.test_relay import token_of, transcript
from player.tests.test_rereview9 import WhatAVersionBeforeLeft
from player.tests.test_upkeep import stock
from player.world import utc_day

BEFORE = "661f3f63f9bd51887c402ce00f76e8e9735cb2ea"
"""The head this was built on (AP2's first part, approved): protocol 7."""

REVIEWED = "184ce648a0268c8e4b280f280392938b6ee371ac"
"""The first head with hooks, as it was reviewed (request changes; never run): protocol 8."""
REREVIEWED = "ec231943e4c07d4f0d6e1c1ef0e20e7e75ec4844"
"""Its correction, as it was re-reviewed (request changes; never run): protocol 9."""

TOOL = "mcp__Tnr__callEndpoint"
AGENT = "a1b2c3d4e5f60718"
OK = [{"type": "text", "text": "ok"}]


class Hooks(unittest.TestCase):
    """A live folder, `brain next` as a relay runs it, the hooks as Claude Code runs them, and a stand-in for
    the game that answers whatever a hook lets through."""

    def start(self, mode="hunt", rig=None):
        self.r = r = rig or Rig(mode)
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

    def bash(self, command, agent=AGENT, meanwhile=None, **more):
        """The Bash hook's answer to a command: (the command that is run, None) or (None, why it is refused).
        meanwhile: what happens while the hook waits (it is told each wait)."""
        said = hook.run("bash", self.inp("Bash", {"command": command, "description": "x"}, agent, **more), self.r.dir,
                        meanwhile or self.sleep)
        said = said["hookSpecificOutput"]
        if said["permissionDecision"] == "allow":
            self.assertEqual(said["updatedInput"]["description"], "x")      # (the rest of the input is kept)
            return said["updatedInput"]["command"], None
        return None, said["permissionDecisionReason"]
    def next(self, token=None, agent=AGENT, hooked=True, meanwhile=None):
        """The relay runs its `brain next` line. -> (the token to come back with, the batch's lines but the
        last, every line). self.waited: how long the hook in front of it waited."""
        command = "python3 -m player.brain next" if token is None else json.loads(relay.next_line(token))["bash"]
        hooks = None
        if hooked:
            before = len(self.slept)
            command, why = self.bash(command, agent, meanwhile)
            self.assertIsNone(why)
            command, hooks = command.split(" --hooks ")
            self.waited = round(sum(self.slept[before:]), 6)
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
        """The hook behind a call that was answered. -> what the model is shown in the result's place, or None
        when it is shown the result itself."""
        done = dict(inp, hook_event_name="PostToolUse", tool_input=real, tool_response=response, duration_ms=400)
        said = hook.run("post", done, self.r.dir)
        return said and said["hookSpecificOutput"]["updatedToolOutput"]

    def sent(self, line, agent=AGENT, **more):
        """The model's tool call for a line, as far as the hook in front of it. -> (the hook's input, the real
        call, which is with the connector from now; or None when the hook refused it)."""
        inp = self.inp(TOOL, {"endpointName": line["call"], "input": line["input"]}, agent, **more)
        real = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"].get("updatedInput")
        if real:
            self.game.append(real)
        return inp, real

    def comes(self, inp, real):
        """The connector's answer to a call that went. -> what the model is shown for it."""
        return self.after(inp, real, [{"type": "text", "text": json.dumps(self.answer(real))}])

    def refused(self, line, **kw):
        n = len(self.game)
        why = self.call(line, **kw)
        self.assertEqual(len(self.game), n, why)                            # the game did not see it
        self.assertIsInstance(why, str)
        return why

    def kept(self):
        """What is on record of the relay's batches (live/hook), but the lock and the log."""
        folder = os.path.join(self.r.dir, "hook")
        return sorted(os.path.relpath(os.path.join(root, f), folder) for root, _, names in os.walk(folder)
                      for f in names if f not in ("lock", "log.jsonl"))

    def puts(self):
        """The results that are handed in and wait for the brain."""
        return sorted(f for f in os.listdir(os.path.join(self.r.dir, "inbox")) if f.startswith("put-"))

    def loose(self):
        """The batches whose calls the brain's saved ledger holds against every minute: {id: how many calls}."""
        held = {}
        for c in relay.read(os.path.join(self.r.dir, "world.json"))["budget"]["calls"]:
            if c[2:3] == ["loose"]:
                held[c[3]] = held.get(c[3], 0) + 1
        return held

    def late(self, token, n):
        """A result that is kept beside the late ones."""
        return relay.unpack([relay.read(hooked.late(self.r.dir, token, n))])[0]
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
        self.assertEqual(self.next(token, hooked=False)[2], [hooked.NO_HOOKS])    # its hook did not run this time
        self.assertEqual(self.next(token, agent="b" * 16)[2], [hooked.NO_HOOKS])  # or it is not that relay at all
        self.assertEqual(self.client(), before)                              # nothing was taken from either
        self.assertEqual(len(self.next(token)[1]), 4)                        # the relay itself carries on

    def test_a_relay_that_began_without_hooks_does_not_get_them_later(self):
        token, lines = self.first_batch(hooked=False)
        self.assertEqual(self.next(token)[2], [hooked.NO_HOOKS])


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
        self.slept = []
        self.assertIn("call 1 of the batch was not made", self.refused(lines[1]))           # the second, first
        self.assertAlmostEqual(sum(self.slept), hooked.GRACE, places=6)      # (the first was waited for, so long)
        self.assertIn("its turn has passed", self.refused(lines[0]))         # and is passed over for good
        self.assertIn("made already", self.refused(lines[1]))                # as the second is used up
        self.slept = []
        self.assertIn("call 2 of the batch was not made", self.refused(lines[2]))
        self.assertIn("call 3 of the batch was not made", self.refused(lines[3]))
        self.assertEqual(self.slept, [])                                     # (that is known at once)
        self.assertEqual(len(self.game), 1)                                  # nothing of the batch went
        self.next(token)
        self.assertEqual(self.waited, 0)                                     # and every line of it has ended

    def test_calls_that_are_started_together_go_in_order_whichever_hook_runs_first(self):
        """Claude Code may start the tool calls of one message together (review of 184ce648, check 4: a line
        whose hook ran before the line in front of it was taken was refused, and the batch was cut there).
        Here the hook of the last line runs first, and each hook starts while the one behind it waits."""
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        shown, begun = {}, set()

        def while_it_waits(n):
            def sleep(seconds):
                self.sleep(seconds)
                if n > 1 and n - 1 not in begun:                             # the hook of the line in front starts
                    begun.add(n - 1)
                    shown[n - 1] = self.call(lines[n - 2], sleep=while_it_waits(n - 1))
            return sleep
        shown[4] = self.call(lines[3], sleep=while_it_waits(4))
        self.assertEqual(shown, {n: OK for n in (1, 2, 3, 4)})
        self.assertEqual([g["endpointName"] for g in self.game[1:]],
                         [s["call"] for s in self.client()["steps"] if "call" in s])
    def test_a_call_waits_for_the_one_before_it_to_be_answered(self):
        """The second is held until the first has its answer, and is refused if that does not come."""
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        first, real = self.sent(lines[0])
        looks = []

        def then_it_answers(seconds):                                       # the first call's answer comes meanwhile
            looks.append(seconds)
            if len(looks) == 3:
                self.comes(first, real)
        self.assertEqual(self.call(lines[1], sleep=then_it_answers), OK)
        self.assertEqual(looks, [hooked.LOOK] * 3)
        self.sent(lines[2])                                                  # the third goes, and is never answered
        self.slept = []
        self.assertIn("call 3 of the batch has not been answered", self.refused(lines[3]))
        self.assertAlmostEqual(sum(self.slept), hooked.TURN, places=6)
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
        """From the moment the relay comes to hand a batch in, nothing more of that batch goes: not while the
        brain is asked, and not while the relay sits in `brain next` until the next batch is printed. A call of
        it that comes then (started together with `brain next`, say) is not made."""
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.call(lines[0])
        late = []

        def meanwhile(seconds):                                             # the brain-side wait
            self.sleep(seconds)
            late.append(self.refused(lines[2]))
        self.bash(json.loads(relay.next_line(token))["bash"])                # the hook in front of `brain next`
        self.assertIn("handed in", self.refused(lines[1]))
        with mock.patch.object(brain, "_await", lambda *a, **k: dict(self.a_batch(), hold=2.0)):
            brain.next_batch(self.r.dir, token, io.StringIO(), meanwhile, hooks=AGENT)
        self.assertEqual(len(late), 1)
        self.assertIn("handed in", late[0])
        self.assertEqual(len(self.game), 2)
    def a_batch(self, until=None):
        return {"protocol": relay.PROTOCOL, "id": "feedfeed", "steps": [K.user()], "stop": None, "until": until}

    def test_a_brain_next_that_died_when_the_brain_had_the_results_is_given_the_batch_when_run_again(self):
        token, lines = self.first_batch()
        self.does(lines)

        class Killed(Exception):
            pass

        def dies(seconds):                                                  # in the brain-side wait
            raise Killed
        self.bash(json.loads(relay.next_line(token))["bash"])
        with mock.patch.object(brain, "_await", lambda *a, **k: dict(self.a_batch(), hold=2.0)), \
                self.assertRaises(Killed):
            brain.next_batch(self.r.dir, token, io.StringIO(), dies, hooks=AGENT)
        self.assertEqual(self.kept(), [])                                    # (the brain has them: all is cleared)
        new, lines, printed = self.next(token)
        self.assertEqual((self.waited, len(lines)), (0, 1))                  # the batch that was waiting, at once
        self.assertEqual(self.call(lines[0]), OK)

    def test_the_cutoff_a_batch_was_made_under_is_kept_for_the_hook(self):
        token, lines = self.first_batch()
        self.does(lines)
        with mock.patch.object(brain, "_await", lambda *a, **k: dict(self.a_batch(self.r.t + 50), hold=0.0)):
            token, lines, _ = self.next(token)
        self.assertEqual(self.client()["until"], self.r.t + 50)
        self.r.t += 50
        self.assertIn("lease", self.refused(lines[0]))

    def test_a_batch_the_brain_did_not_take_stays_closed(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.call(lines[0])
        with mock.patch.object(brain, "_await", lambda *a, **k: None):       # the brain gives no answer for now
            self.assertEqual(self.next(token)[2], [relay.next_line(token)])
        self.assertIn("handed in", self.refused(lines[1]))                   # the relay came to hand it in
        self.assertNotEqual(self.next(token)[0], token)                      # and when the brain answers, goes on
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
        self.assertIn("call 2 of the batch was not made", self.refused(lines[2]))            # so nothing behind it
        for bad in ("soon", True, -5.0, 0.0):                                # (at the cutoff is past it)
            self.start()
            token, lines = self.first_batch()
            until = self.r.t + bad if isinstance(bad, float) else bad
            relay.write(os.path.join(self.r.dir, "client.json"), dict(self.client(), until=until))
            self.assertIn("lease", self.refused(lines[0]), bad)

    def test_a_relay_that_is_replaced_while_its_call_waits(self):
        token, lines = self.into_a_fight()
        self.call(lines[0])

        def replaced_meanwhile(seconds):                                    # the wait in front of the second action
            self.sleep(seconds)
            self.first_batch(agent="c" * 16)
        self.assertIn("another relay's", self.refused(lines[1], sleep=replaced_meanwhile))

    def test_a_tool_call_with_no_id_is_not_made(self):
        token, lines = self.first_batch()
        for bad in (None, "", 7):                                            # (its result could not be known by it)
            inp = self.inp(TOOL, {"endpointName": C.STAND_IN, "input": lines[0]["input"]}, tool_use_id=bad)
            said = hook.run("pre", inp, self.r.dir, self.sleep)["hookSpecificOutput"]
            self.assertEqual(said["permissionDecision"], "deny", bad)
        self.assertEqual(self.call(lines[0]), OK)

    def test_a_hook_that_fails_with_a_line_in_its_hand_gives_the_line_up(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        with mock.patch.object(hook, "_turn", side_effect=RuntimeError("boom")):
            self.assertIn("the relay's hook failed", self.refused(lines[0]))
        self.slept = []
        self.assertIn("call 1 of the batch was not made", self.refused(lines[1]))
        self.assertEqual(self.slept, [])                                     # (nobody waits for it)
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
        """Nothing is written down for it, so nothing is put in its place: "ok" stands for a result that is kept
        (re-review of ec231943, R3: it stood there for whatever the hook did not know)."""
        token, lines = self.first_batch()
        stray = self.inp(TOOL, {"endpointName": "profile.getUser", "input": {}})
        self.assertIsNone(self.after(stray, stray["tool_input"], [{"type": "text", "text": "{}"}]))
        self.assertIsNone(hook.run("fail", dict(stray, error="x"), self.r.dir))
        self.assertEqual((self.puts(), self.kept()), ([], []))
        self.does(lines)
        self.next(token)
        self.assertEqual(len(self.got), 1)
    def test_what_comes_for_a_call_the_hook_refused_is_no_result(self):
        """Nothing should: a refused call is not made. If Claude Code ran the hooks behind one all the same,
        what they are given is not a result of the batch."""
        token, lines = self.first_batch()
        relay.write(os.path.join(self.r.dir, "client.json"), dict(self.client(), until=self.r.t - 1))
        inp, real = self.sent(lines[0])                                      # past the lease: refused, on record
        self.assertIsNone(real)
        self.assertIsNone(self.after(inp, inp["tool_input"], [{"type": "text", "text": "{}"}]))
        self.assertIsNone(hook.run("fail", dict(inp, error="x"), self.r.dir))
        with open(os.path.join(self.r.dir, "hook", "log.jsonl"), encoding="utf8") as f:
            self.assertEqual([json.loads(x)["refused"] for x in f][-2:], ["not a call of a batch"] * 2)
        self.assertEqual((self.puts(), self.kept()), ([], [f"{token}.1.json", f"{token}.seen"]))

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
        self.assertEqual(self.next(token)[2], [hooked.NO_HOOKS])
        self.assertEqual(self.game, [])
        self.assertEqual(self.next(token)[2], [hooked.NO_HOOKS])               # and however often it asks

    def test_a_relay_whose_hooks_have_run_is_not_stopped_for_a_batch_it_left_out(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertTrue(self.client()["seen"])
        token, lines, printed = self.next(token)                             # it made none of the four calls
        self.assertNotIn(hooked.NO_HOOKS, printed)
        self.assertTrue(lines)

    def test_a_refused_call_is_a_hook_that_ran(self):
        token, lines = self.first_batch()
        self.call({"call": C.STAND_IN, "input": {"b": token, "n": 5}})       # refused: but the hook was there
        self.assertNotIn(hooked.NO_HOOKS, self.next(token)[2])

    def test_a_batch_its_hook_did_not_close_is_not_handed_in(self):
        """`brain next` with the relay's id behind it, and no hook in front of it: run by hand, say. What
        the relay holds was not closed, so a call of it may still be on its way: nothing is taken."""
        token, lines = self.first_batch()
        self.does(lines)
        out = io.StringIO()
        brain.next_batch(self.r.dir, token, out, self.sleep, hooks=AGENT)
        self.assertEqual(out.getvalue().splitlines(), [hooked.NO_HOOKS])
        self.assertEqual(self.puts(), [f"put-{token}-001.json"])
        self.assertEqual(len(self.next(token)[1]), 4)                        # through its hook, the relay carries on
    def test_a_line_is_one_tool_calls_however_many_ask_for_it_at_once(self):
        path = os.path.join(self.r.dir, "hook", "ab12cd-1.1.json")
        self.assertTrue(hooked.once(path, {"use": "toolu_a"}))
        with mock.patch.object(hooked.os, "getpid", return_value=os.getpid() + 1):   # (another hook's process)
            self.assertFalse(hooked.once(path, {"use": "toolu_b"}))
        self.assertEqual(relay.read(path), {"use": "toolu_a"})
        self.assertEqual(self.kept(), ["ab12cd-1.1.json"])                   # (and nothing is left lying beside it)

class AHookThatIsBehindTheTimes(Hooks):
    """Review of 184ce648, H1. A hook reads who holds which batch, and may be held up before it goes on: by then
    its relay may have been replaced. That hook then swept away what was on record of the new relay's batch
    (the line its call had taken, the sign that its hooks run), and the new relay's call went a second time."""

    def setUp(self):
        self.start()
        self.got = self.handed_to_the_brain()

    def test_it_takes_nothing_of_the_new_relays_and_no_call_goes_twice(self):
        old, old_lines = self.first_batch()
        read, new = hooked.holding, {}

        def read_and_be_held_up(live):
            state = read(live)                                              # the old relay's hook reads the file;
            if not new:
                new["agent"] = "c" * 16
                with mock.patch.object(hook, "holding", read):
                    new["token"], new["lines"] = self.first_batch(agent=new["agent"])    # a new relay takes over
                    self.assertEqual(self.call(new["lines"][0], agent=new["agent"]), OK)   # and makes its call;
            return state
        with mock.patch.object(hook, "holding", read_and_be_held_up):
            self.assertIn("another relay's", self.call(old_lines[0]))        # and then the old hook goes on
        self.assertEqual(len(self.game), 1)                                  # (its own call did not go)
        token, line = new["token"], new["lines"][0]
        self.assertEqual(self.kept(), sorted([f"{old}.1.json", f"{old}.seen", f"{token}.1.json", f"{token}.seen"]))
        self.assertEqual(self.puts(), [f"put-{token}-001.json"])
        self.assertIn("made already", self.refused(line, agent=new["agent"]))                # the same call again
        self.assertEqual(len(self.game), 1)
        self.next(token, agent=new["agent"])
        self.assertEqual([(x.endpoint, x.error) for x in self.got], [(self.game[0]["endpointName"], None)])

    def test_a_new_relay_is_not_named_between_a_hooks_last_look_and_its_letting_the_call_go(self):
        """Re-review of ec231943, R2. The hook's last look at client.json and its letting the call go were
        under the hooks' lock. Naming a new relay was not, and fell between the two: the old relay's call was
        let go, and put on record as let go, after the new relay was named. Now the naming waits for the hook:
        the call went before it, and is a call that is out, of a batch that is gone."""
        old, old_lines = self.first_batch()
        read, looks, new = hooked.holding, [], {}

        def at_its_last_look(live):
            state = read(live)
            looks.append(state and state["hooks"])
            if len(looks) == 2:                                             # the hook has the lock, and has read
                new["relay"] = threading.Thread(target=lambda: new.update(token=self.next(agent="c" * 16)[0]))
                new["relay"].start()
                new["relay"].join(0.3)
                new["waits"] = new["relay"].is_alive() and self.client()["hooks"] == AGENT
            return state
        with mock.patch.object(hook, "holding", at_its_last_look):
            inp, real = self.sent(old_lines[0])
        new["relay"].join(60)
        self.assertTrue(new["waits"])                                        # no relay was named meanwhile
        self.assertEqual((looks[:2], real["endpointName"]), ([AGENT, AGENT], "profile.getUser"))   # so the call went,
        self.assertEqual((self.client()["hooks"], [g["token"] for g in self.client()["gone"]]), ("c" * 16, [old]))
        self.assertEqual(list(hooked.out(self.r.dir, old)), [1])             # and is out, of a batch that is gone
        self.assertEqual(self.comes(inp, real), OK)
        self.assertEqual((self.late(old, 1).data, hooked.out(self.r.dir, old)), (self.me.data, {}))

    def test_the_hooks_of_a_relay_that_was_replaced_leave_the_new_relays_batch_alone(self):
        """Every hook of the old relay, run after the new one has taken over and made its first call."""
        old, old_lines = self.first_batch()
        self.does(old_lines)
        old, old_lines, _ = self.next(old)
        self.call(old_lines[0])
        inp, real = self.sent(old_lines[1])                                  # one of its calls is with the connector
        new, lines = self.first_batch(agent="c" * 16)
        self.assertEqual(self.call(lines[0], agent="c" * 16), OK)
        mine = [f"{new}.1.json", f"{new}.seen"]
        before = {name: relay.read(os.path.join(self.r.dir, "hook", name)) for name in mine}
        self.assertEqual(self.comes(inp, real), OK)                          # its result comes
        self.assertIn("another relay's", self.refused(old_lines[2]))         # it makes another call
        self.assertEqual(self.next(old)[2], [brain.SUPERSEDED])              # and comes to hand its batch in
        self.assertEqual({name: relay.read(os.path.join(self.r.dir, "hook", name)) for name in mine}, before)
        self.assertNotIn(f"{old}.closed", self.kept())                       # (it is not the old relay's to close)
        self.assertIn(f"put-{new}-001.json", self.puts())
        self.assertIn("made already", self.refused(lines[0], agent="c" * 16))


class ABatchIsClosedBeforeItIsHandedIn(Hooks):
    """Review of 184ce648, H2. `brain next` took what results were there when it ran. One that came later was
    refused (the batch had moved on), or was added to a request the brain had answered already and then
    removed as taken."""

    def setUp(self):
        self.start()
        self.got = self.handed_to_the_brain()

    def four(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertEqual(len(lines), 4)
        del self.got[:]
        return token, lines

    def test_brain_next_waits_for_a_call_that_is_with_the_connector(self):
        """The first schedule: Claude Code starts `brain next` while a call of the batch is still out."""
        token, lines = self.first_batch()
        inp, real = self.sent(lines[0])
        looks = []

        def then_it_answers(seconds):
            self.sleep(seconds)
            looks.append(seconds)
            if len(looks) == 4:
                self.assertEqual(self.comes(inp, real), OK)
        self.next(token, meanwhile=then_it_answers)
        self.assertEqual(looks, [hooked.LOOK] * 4)                           # no longer than it took
        self.assertEqual([(x.endpoint, x.data) for x in self.got], [("profile.getUser", self.me.data)])

    def test_a_call_that_does_not_come_back_is_handed_in_as_unanswered_and_its_batch_as_not_over(self):
        token, lines = self.four()
        self.call(lines[0])
        inp, real = self.sent(lines[1])                                      # the second goes, and stays out
        batch = self.client()["held"]
        new, new_lines, _ = self.next(token)
        self.assertEqual(self.waited, hooked.TURN + hooked.GRACE)            # it was waited for; then the two not begun
        self.assertEqual([(x.endpoint, x.error) for x in self.got],
                         [(self.game[-2]["endpointName"], None), (real["endpointName"], hooked.NO_ANSWER)])
        self.assertEqual((self.asks[-1]["held"], self.asks[-1]["gone"]), (None, [dict(batch, closed=True)]))
        self.assertEqual(self.loose(), {batch["id"]: 4})                     # the brain holds the batch's calls
        self.assertEqual(self.kept(), [f"{token}.2.json"])                   # and the line that is out stays
        self.r.t += 3
        self.assertEqual(self.comes(inp, real), OK)                          # its result comes after all: not shown,
        self.assertEqual(self.puts(), [])                                    # not handed in with another batch,
        self.assertEqual(self.kept(), [f"{token}.2.json", f"late/{token}.2.json"])           # and not lost
        came = self.late(token, 2)
        self.assertEqual((came.endpoint, came.input, came.data, came.at), (real["endpointName"], real["input"], self.answer(real), self.r.t))
        del self.got[:]
        self.r.t += 5
        self.does(new_lines)
        self.next(new)
        self.assertEqual(self.asks[-1]["gone"], [])                          # the word that the batch is over, as of
        self.assertEqual(self.asks[-1]["ended"], [[batch["id"], came.at, token, "answered"]])   # when the result came
        self.assertEqual(self.loose(), {})
        self.assertEqual([x.endpoint for x in self.got], [g["endpointName"] for g in self.game[-len(new_lines):]])
        self.assertEqual(self.kept(), [f"{token}.2.json", f"late/{token}.2.json"])           # (for an hour more)
    def test_a_result_that_is_there_when_the_batch_is_handed_in_is_handed_in_though_it_came_late(self):
        """It came between the closing and `brain next`: kept aside, and the brain is handed it with the batch."""
        token, lines = self.four()
        self.call(lines[0])
        inp, real = self.sent(lines[1])
        self.bash(json.loads(relay.next_line(token))["bash"])                # closed: the second is still out
        self.assertEqual(self.comes(inp, real), OK)
        self.assertEqual(self.puts(), [f"put-{token}-001.json"])
        self.assertEqual(self.kept()[-1], f"late/{token}.2.json")
        batch = self.client()["held"]
        brain.next_batch(self.r.dir, token, io.StringIO(), self.sleep, hooks=AGENT)
        self.assertEqual([(x.endpoint, x.error) for x in self.got], [(g["endpointName"], None) for g in self.game[-2:]])
        self.assertEqual((self.kept(), self.puts()), ([], []))               # (late/ holds what was not handed in)
        self.assertEqual((self.asks[-1]["held"], self.asks[-1]["gone"], self.loose()), (batch, [], {}))   # and it is over

    def test_a_brain_next_that_died_hands_in_the_same_when_it_is_run_again(self):
        """The second schedule: the brain answers the request, and `brain next` dies before it has the answer.
        The relay runs its line again. Whatever has come meanwhile, the brain is handed what it was handed."""
        token, lines = self.four()
        self.call(lines[0])
        inp, real = self.sent(lines[1])
        batch, answer = self.client()["held"], brain._await

        class Killed(Exception):
            pass

        def answered_and_then_it_dies(*a, **k):
            answer(*a, **k)
            raise Killed
        with mock.patch.object(brain, "_await", answered_and_then_it_dies), self.assertRaises(Killed):
            self.next(token)
        first = self.asks[-1]
        self.assertEqual((len(first["results"]), first["held"], first["gone"]), (2, None, [dict(batch, closed=True)]))
        self.assertEqual(self.comes(inp, real), OK)                          # the second call's result comes now
        new, new_lines, _ = self.next(token)
        self.assertEqual(self.waited, 0)                                     # (closed once: nothing is waited for again)
        self.assertEqual(self.asks[-1]["results"], first["results"])
        self.assertEqual(len(self.got), 4)                                   # (twice the same two)
        self.assertEqual([row[0::3] for row in self.asks[-1]["ended"]], [[batch["id"], "answered"]])   # and it is over
        self.assertEqual((self.kept(), self.puts(), self.loose()), ([f"late/{token}.2.json"], [], {}))
        self.assertTrue(new_lines)                                           # (its line went with its batch: it had its result)
    def test_the_second_schedule_as_the_review_ran_it(self):
        """The request with the first result is written, `brain next` dies before the brain answers, a brain
        at home answers the request, and then the relay makes the second call. That call went then; its
        result was added to the request that was made again, and removed unread. Now it does not go."""
        token, lines = self.four()
        self.call(lines[0])

        class Killed(Exception):
            pass

        def dies(*a, **k):
            raise Killed
        with mock.patch.object(brain, "_await", dies), self.assertRaises(Killed):
            self.next(token)
        (request,) = relay.pending_requests(self.r.dir)
        brain.serve(brain.Brain(self.r.dir), self.r.dir, request)            # a brain at home answers it
        self.assertIn("handed in", self.refused(lines[1]))
        self.assertNotEqual(self.next(token)[0], token)                      # the relay runs its line again
        first, again = [a["results"] for a in self.asks[-2:]]
        self.assertEqual((len(first), again), (1, first))
        self.assertEqual((self.puts(), self.kept()), ([], []))

    def test_a_batch_is_closed_once_however_often_its_relay_comes(self):
        token, lines = self.four()
        self.call(lines[0])
        self.sent(lines[1])                                                  # the second goes, and stays out
        closed = os.path.join(self.r.dir, "hook", f"{token}.closed")
        with mock.patch.object(brain, "_await", lambda *a, **k: None):       # the brain gives no answer for now
            self.next(token)
            first = relay.read(closed)
            self.assertEqual((self.waited, first["lines"]["2"]), (hooked.TURN + hooked.GRACE, "open"))
            self.next(token)
        self.assertEqual((self.waited, relay.read(closed)), (0, first))      # the call is not waited for again

    def test_a_batch_is_closed_by_the_relay_that_holds_it_and_no_other(self):
        token, lines = self.four()
        self.call(lines[0])
        self.assertEqual(self.next(token, agent="b" * 16)[2], [hooked.NO_HOOKS])   # another agent runs the line
        self.assertEqual((self.waited, self.kept()), (0, [f"{token}.1.json", f"{token}.seen"]))
        self.assertEqual(self.call(lines[1]), OK)                            # the relay's batch stands as it was

    def test_a_line_that_has_not_gone_when_the_batch_is_closed_does_not_go(self):
        """Its hook is waiting (for its turn, or the wait in front of it) when the relay comes to hand in."""
        token, lines = self.into_a_fight()
        self.call(lines[0])
        del self.got[:]
        made = []

        def closed_meanwhile(seconds):                                      # the wait in front of the second action
            self.sleep(seconds)
            self.bash(json.loads(relay.next_line(token))["bash"])
            made.append(relay.read(os.path.join(self.r.dir, "hook", f"{token}.closed"))["lines"]["2"])
        self.assertIn("handed in", self.refused(lines[1], sleep=closed_meanwhile))
        self.assertEqual(made, ["refused"])
        brain.next_batch(self.r.dir, token, io.StringIO(), self.sleep, hooks=AGENT)
        self.assertEqual([x.endpoint for x in self.got], [self.game[-1]["endpointName"]])     # the first, and no more

    def test_the_brain_takes_no_result_of_a_relay_that_was_replaced_and_none_is_lost(self):
        token, lines = self.four()
        self.call(lines[0])                                                  # handed in for the batch, which
        inp, real = self.sent(lines[1])                                      # the relay does not live to hand in
        batch = self.client()["held"]
        new, new_lines = self.first_batch(agent="c" * 16)
        self.assertEqual(self.comes(inp, real), OK)                          # the old relay's call comes back
        self.assertEqual(self.puts(), [])                                    # (neither is the new relay's to hand in)
        self.call(new_lines[0], agent="c" * 16)
        self.next(new, agent="c" * 16)
        self.assertEqual([x.endpoint for x in self.got], [self.game[-1]["endpointName"]])     # the new relay's own
        self.assertEqual(self.puts(), [])
        self.assertEqual(self.kept(), sorted([f"{token}.1.json", f"{token}.2.json", f"{token}.seen",
                                              f"late/{token}.1.json", f"late/{token}.2.json"]))
        self.assertEqual(self.client()["gone"], [batch])                     # held, until its relay is back or stopped

    def test_a_replaced_relay_that_is_back_while_its_call_is_out_has_not_ended_its_batch(self):
        """Its `brain next` may have been started together with its calls. That it is back says that nothing
        more of its batch will go, not that what went is over (re-review of ec231943, R1 and R2)."""
        token, lines = self.four()
        self.call(lines[0])
        inp, real = self.sent(lines[1])                                      # with the connector
        batch = self.client()["held"]
        new, new_lines = self.first_batch(agent="c" * 16)
        self.assertEqual(self.next(token)[2], [brain.SUPERSEDED])            # the old relay is back, and is stopped
        self.assertEqual((self.client()["gone"], self.client()["ended"]), ([dict(batch, back=True)], []))
        self.call(new_lines[0], agent="c" * 16)
        new, new_lines, _ = self.next(new, agent="c" * 16)
        self.assertEqual((self.asks[-1]["ended"], self.loose()), ([], {batch["id"]: 4}))     # still held
        self.r.t += 2
        self.assertEqual(self.comes(inp, real), OK)                          # the call comes back
        self.next(new, agent="c" * 16)
        self.assertEqual(self.asks[-1]["ended"], [[batch["id"], self.late(token, 2).at, token, "answered"]])
        self.assertEqual((self.client()["gone"], self.loose()), ([], {}))

    def test_a_replaced_relay_that_is_back_with_nothing_out_has_ended_its_batch(self):
        token, lines = self.four()
        self.does(lines[:2])
        batch = self.client()["held"]
        self.first_batch(agent="c" * 16)
        self.assertEqual(self.next(token)[2], [brain.SUPERSEDED])
        self.assertEqual((self.client()["gone"], [row[0::3] for row in self.client()["ended"]]), ([], [[batch["id"], "back"]]))

class ACallThatIsOutHoldsWhatItMayCost(Hooks):
    """Re-review of ec231943, R1, as it ran it, on the spending fixture of AP2's re-review: 180,000 ryo of the
    day's allowance left, 400,000 in the pocket. A purchase goes to the connector and does not come back
    within the two minutes. It was handed in as an error and its batch as over; the next read, made while the
    purchase was still on its way, showed nothing spent, what was reserved went, and 180,000 more were
    admitted: 345,000 against 180,000."""

    def setUp(self):
        self.start(rig=Rig(upkeep=True))
        r = self.r
        r.world["control"]["activities"].update(training=False, equipment=False)
        self.me, self.items = user(money=400_000, bank=900_000_000), stock(**SHORT)
        r.world.absorb([self.me._replace(at=r.t)])
        r.world["records"]["spend"] = {"day": utc_day(r.t), "ryo": C.DAILY_CAP - 180_000}
        r.world.save()
        self.got = self.handed_to_the_brain()

    def answer(self, real):
        """The game: my items and my profile as they are now."""
        return {"item.getUserItems": self.items.data, "profile.getUser": self.me.data}.get(real["endpointName"], {"success": True})

    def planned(self):
        """(the calls of the batch the relay holds, what its purchases cost)."""
        steps = [s for s in self.client()["steps"] if "call" in s]
        return [s["call"] for s in steps], sum(s["input"]["stack"] * PRICES[s["input"]["itemId"]] for s in steps if s["call"] == "item.buy")

    def spend(self):
        return relay.read(os.path.join(self.r.dir, "world.json"))["records"]["spend"]

    def test_it(self):
        token, lines = self.first_batch()
        self.assertEqual(self.planned()[0][:2], READS)
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertEqual(self.planned()[1], 180_000)                         # the brain buys for what the day has left
        batch, calls = self.client()["held"], len(self.planned()[0])
        inp, real = self.sent(lines[0])                                      # the first purchase goes: 165,000 ryo
        self.assertEqual((real["endpointName"], real["input"]["stack"] * PRICES[real["input"]["itemId"]]), ("item.buy", 165_000))
        token, lines, _ = self.next(token)                                   # and is still out two minutes on
        self.assertEqual(self.waited, hooked.TURN + hooked.GRACE)
        self.assertEqual(self.loose(), {batch["id"]: calls})                 # its batch is held
        self.assertEqual(self.spend()["out"], [[batch["id"], 180_000.0]])    # and what it may cost stays reserved
        for _ in range(3):                                                   # the reads that follow show nothing spent
            self.does(lines)
            token, lines, _ = self.next(token)
            self.assertEqual(self.planned()[1], 0)                           # was: 180,000 more
            self.assertEqual((self.spend()["ryo"], self.spend()["out"]), (C.DAILY_CAP - 180_000, [[batch["id"], 180_000.0]]))
        self.r.t += 1
        self.me = user(money=235_000, bank=900_000_000)                      # the purchase is made after all,
        self.assertEqual(self.comes(inp, real), OK)                          # and its result comes
        self.assertEqual(self.late(batch["token"], 1).data, {"success": True})
        self.does(lines)
        token, lines, _ = self.next(token)                                   # the word that the batch is over
        self.assertEqual(self.asks[-1]["ended"], [[batch["id"], self.late(batch["token"], 1).at, batch["token"], "answered"]])
        self.assertEqual((self.loose(), self.planned()[1]), ({}, 0))
        self.assertEqual(self.spend()["out"], [[batch["id"], 180_000.0, True]])   # a read after that word pays it off
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertEqual((self.spend()["ryo"], self.spend()["out"]), (C.DAILY_CAP - 15_000, []))
        self.assertLessEqual(self.planned()[1], 15_000)                      # and the day has 15,000 left

    def test_the_operators_word_ends_it_when_the_result_never_comes(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        batch, calls = self.client()["held"], len(self.planned()[0])
        self.sent(lines[0])
        token, lines, _ = self.next(token)
        self.assertEqual(self.loose(), {batch["id"]: calls})
        out = io.StringIO()
        brain.stopped(self.r.dir, [batch["token"]], out)
        self.assertEqual(json.loads(out.getvalue())["stopped"], [batch["token"]])
        self.does(lines)
        token, lines, _ = self.next(token)
        self.assertEqual(([row[0::3] for row in self.asks[-1]["ended"]], self.loose()), ([[batch["id"], "stopped"]], {}))
        self.assertEqual(self.spend()["out"], [[batch["id"], 180_000.0, True]])


class AResultTheHookCannotWriteDown(Hooks):
    """Review of 184ce648, H3: the hook could not write the result down, showed the model "ok" in its place all
    the same, and the result was nowhere. Re-review of ec231943, R4: the model was left with it, but its line
    was put down as done at once, and `brain next` looked for it once in a transcript that did not have it yet."""

    def setUp(self):
        self.start()
        self.got = self.handed_to_the_brain()
        self.token, lines = self.first_batch()
        self.asked, self.real = self.sent(lines[0])
        self.line, self.batch = lines[0], self.client()["held"]
        self.text = json.dumps(self.me.data)

    def transcript(self, *handed_in, result=None, is_error=False):
        """The relay's own transcript: its call, the `brain next` lines it has run since, and the call's result
        if the host has written that down."""
        path, t, use = os.path.join(self.r.dir, "relay.jsonl"), self.r.t, self.asked["tool_use_id"]
        rows = [("bash", "b0", "python3 -m player.brain next", t - 9), ("use", use, C.STAND_IN, self.line["input"], t)]
        rows += [("bash", f"b{k}", json.loads(relay.next_line(token))["bash"], t) for k, token in enumerate(handed_in, 1)]
        transcript(path, rows + ([("res", use, result, t, is_error)] if result is not None else []))
        return mock.patch.dict(os.environ, {"TNR_TRANSCRIPT": path})

    def hooks_log(self):
        with open(os.path.join(self.r.dir, "hook", "log.jsonl"), encoding="utf8") as f:
            return f.read()

    # ---- the inbox cannot be written: it is kept beside the late ones, and handed in from there
    def test_when_the_inbox_cannot_be_written_it_is_kept_in_the_hooks_folder_and_handed_in_from_there(self):
        with mock.patch.object(relay, "put", side_effect=OSError("no space left on device")):
            self.assertEqual(self.after(self.asked, self.real, [{"type": "text", "text": self.text}]), OK)
        self.assertEqual((self.puts(), self.kept()[-1]), ([], f"late/{self.token}.1.json"))
        with self.transcript(self.token):                                    # (the host has not written the result yet)
            self.next(self.token)
        self.assertEqual(self.waited, 0)
        self.assertEqual([(x.endpoint, x.data, x.error) for x in self.got], [("profile.getUser", self.me.data, None)])
        self.assertEqual((self.asks[-1]["held"], self.kept(), self.puts()), (self.batch, [], []))

    def test_a_failed_call_keeps_what_it_failed_with(self):
        failed = dict(self.asked, hook_event_name="PostToolUseFailure", tool_input=self.real,
                      error="MCP error -32000: Too Many Requests")
        with mock.patch.object(relay, "put", side_effect=OSError("no space left on device")):
            self.assertIsNone(hook.run("fail", failed, self.r.dir))
        with self.transcript(self.token):
            self.next(self.token)
        self.assertEqual([(x.endpoint, x.data, x.error) for x in self.got], [("profile.getUser", None, brain.RATE_LIMITED)])

    # ---- nothing can be written: the model is left with it, and the line stays out
    def nothing_can_be_written(self, error=None):
        with mock.patch.object(relay, "write", side_effect=OSError("read-only file system")):
            if error is None:
                self.assertIsNone(self.after(self.asked, self.real, [{"type": "text", "text": self.text}]))   # no "ok"
            else:
                failed = dict(self.asked, hook_event_name="PostToolUseFailure", tool_input=self.real, error=error)
                self.assertIsNone(hook.run("fail", failed, self.r.dir))
        self.assertIn("could not be written down", self.hooks_log())
        self.assertEqual((self.puts(), self.kept()), ([], [f"{self.token}.1.json", f"{self.token}.seen"]))

    def test_the_model_is_left_with_it_and_brain_next_takes_it_from_the_relays_transcript(self):
        self.nothing_can_be_written()
        with self.transcript(self.token, result=self.text):
            self.next(self.token)
        self.assertEqual(self.waited, hooked.TURN)                           # (its line says the call is out)
        self.assertEqual([(x.endpoint, x.data, x.error) for x in self.got], [("profile.getUser", self.me.data, None)])
        self.assertEqual((self.asks[-1]["held"], self.asks[-1]["gone"], self.kept()), (self.batch, [], []))

    def test_a_result_the_host_has_not_written_down_yet_is_not_given_up(self):
        """The re-review's schedule: the transcript has the call and the `brain next`, and the result only
        after `brain next` has run. The brain is told the call has no answer; the batch is not over; the line
        stays; and when the transcript has the result, it is taken from there and the batch is over."""
        self.nothing_can_be_written()
        with self.transcript(self.token):
            new, lines, _ = self.next(self.token)
        self.assertEqual([(x.data, x.error) for x in self.got], [(None, hooked.NO_ANSWER)])
        self.assertEqual((self.asks[-1]["held"], self.asks[-1]["gone"]), (None, [dict(self.batch, closed=True)]))
        self.assertEqual((self.kept(), self.loose()), ([f"{self.token}.1.json"], {self.batch["id"]: 1}))
        self.r.t += 4
        with self.transcript(self.token, new, result=self.text):             # the host writes the result down
            self.next(new)
        came = self.late(self.token, 1)
        self.assertEqual((came.endpoint, came.data, came.error), ("profile.getUser", self.me.data, None))
        self.assertEqual(self.asks[-1]["ended"], [[self.batch["id"], came.at, self.token, "answered"]])
        self.assertEqual((self.asks[-1]["gone"], self.loose()), ([], {}))
        self.assertEqual(self.kept(), [f"{self.token}.1.json", f"late/{self.token}.1.json"])

    def test_a_failure_the_host_has_not_written_down_yet_keeps_what_it_failed_with(self):
        self.nothing_can_be_written("MCP error -32000: Too Many Requests")
        with self.transcript(self.token):
            new, lines, _ = self.next(self.token)
        self.assertEqual([x.error for x in self.got], [hooked.NO_ANSWER])
        with self.transcript(self.token, new, result="MCP error -32000: Too Many Requests", is_error=True):
            self.next(new)
        self.assertEqual((self.late(self.token, 1).error, self.loose()), (brain.RATE_LIMITED, {}))

    def test_it_is_looked_for_for_a_moment_when_the_batch_is_handed_in(self):
        self.nothing_can_be_written()
        self.bash(json.loads(relay.next_line(self.token))["bash"])
        looks = []

        def the_host_writes_it_meanwhile(seconds):
            self.sleep(seconds)
            looks.append(seconds)
            if len(looks) == 3:
                self.transcript(self.token, result=self.text)
        with self.transcript(self.token):
            brain.next_batch(self.r.dir, self.token, io.StringIO(), the_host_writes_it_meanwhile, hooks=AGENT)
        self.assertEqual(looks[:3], [hooked.SPOOL[1]] * 3)
        self.assertEqual([(x.data, x.error) for x in self.got], [(self.me.data, None)])
        self.assertEqual((self.asks[-1]["held"], self.asks[-1]["gone"]), (self.batch, []))

    def test_no_longer_than_that_and_with_no_transcript_not_at_all(self):
        self.nothing_can_be_written()
        self.bash(json.loads(relay.next_line(self.token))["bash"])
        self.slept = []
        with self.transcript(self.token):
            brain.next_batch(self.r.dir, self.token, io.StringIO(), self.sleep, hooks=AGENT)
        self.assertEqual(self.slept[:hooked.SPOOL[0] + 1].count(hooked.SPOOL[1]), hooked.SPOOL[0])
        self.assertEqual([x.error for x in self.got], [hooked.NO_ANSWER])
        self.start()
        self.got = self.handed_to_the_brain()
        token, lines = self.first_batch()
        self.asked, self.real = self.sent(lines[0])
        self.token = token
        self.nothing_can_be_written()
        self.bash(json.loads(relay.next_line(token))["bash"])
        self.slept = []
        brain.next_batch(self.r.dir, token, io.StringIO(), self.sleep, hooks=AGENT)
        self.assertNotIn(hooked.SPOOL[1], self.slept)
        self.assertEqual([x.error for x in self.got], [hooked.NO_ANSWER])

    def test_a_result_the_model_was_shown_ok_for_is_never_taken_from_the_transcript(self):
        """What stands in a transcript for a result that was written down is "ok": that is no result."""
        self.assertEqual(self.comes(self.asked, self.real), OK)
        os.unlink(os.path.join(self.r.dir, "inbox", self.puts()[0]))         # (and it is lost on the way, say)
        with self.transcript(self.token, result="ok"):
            self.next(self.token)
        self.assertEqual([(x.data, x.error) for x in self.got], [(None, hooked.NO_ANSWER)])
        self.assertEqual(self.kept(), [f"{self.token}.1.json"])


class WhatIsKeptOfABatch(Hooks):
    def setUp(self):
        self.start()

    def test_it_goes_when_the_brain_has_the_batchs_results_and_not_before(self):
        token, lines = self.first_batch()
        self.does(lines)
        self.assertEqual(self.kept(), [f"{token}.1.json", f"{token}.seen"])
        with mock.patch.object(brain, "_await", lambda *a, **k: None):       # the brain gives no answer for now
            self.next(token)
        self.assertEqual(self.kept(), [f"{token}.1.json", f"{token}.closed", f"{token}.results", f"{token}.seen"])
        self.assertEqual(self.puts(), [f"put-{token}-001.json"])
        new, lines, _ = self.next(token)
        self.assertEqual((self.kept(), self.puts()), ([], []))
        self.does(lines)
        self.assertEqual(self.kept(), [f"{new}.{k}.json" for k in (1, 2, 3, 4)] + [f"{new}.seen"])
        line = relay.read(os.path.join(self.r.dir, "hook", f"{new}.2.json"))
        self.assertEqual((sorted(line), line["call"]), (["call", "use"], [self.game[2]["endpointName"], self.game[2]["input"]]))

    def test_what_nobody_handed_in_stays_while_its_batch_is_held_and_goes_an_hour_after(self):
        token, lines = self.first_batch()
        self.does(lines)                                                     # a relay makes its call, and is replaced
        new, new_lines = self.first_batch(agent="c" * 16)
        self.call(new_lines[0], agent="c" * 16)
        new, _, _ = self.next(new, agent="c" * 16)
        left = sorted([f"{token}.1.json", f"{token}.seen", f"late/{token}.1.json"])
        self.assertEqual(self.kept(), left)                                  # what it left is kept
        folder = os.path.join(self.r.dir, "hook")

        def an_hour_passes():
            long_ago = os.path.getmtime(os.path.join(folder, "lock")) - hooked.OLD - 60
            for name in left + ["log.jsonl"]:
                os.utime(os.path.join(folder, name), (long_ago, long_ago))
            return long_ago
        an_hour_passes()
        new, _, _ = self.next(new, agent="c" * 16)                           # (the next batch the brain has)
        self.assertEqual(self.kept(), left)                                  # its batch is held still: all of it stays
        brain.stopped(self.r.dir, [token], io.StringIO())                    # the operator says that relay is stopped
        long_ago = an_hour_passes()
        self.first_batch(hooked=False)                                       # a relay without hooks takes over, and
        self.assertEqual(self.kept(), [])                                    # the brain has its first batch
        self.assertTrue(os.path.exists(os.path.join(folder, "log.jsonl")))   # (the log is the operator's: no hook
        self.assertLess(os.path.getmtime(os.path.join(folder, "log.jsonl")), long_ago + 1)   # has written to it since)

    def test_clearing_a_batch_away_again_keeps_the_line_of_a_call_that_is_out(self):
        """Re-review of ec231943, R3, as it ran it: the brain has the batch, `brain next` clears it away and
        dies before it prints the next; run again it cleared the batch away once more, and took the line of
        the call that was out. The result that came for it was shown as "ok" and was nowhere."""
        token, lines = self.first_batch()
        inp, real = self.sent(lines[0])
        batch, clear = self.client()["held"], client._taken

        class Died(Exception):
            pass

        def cleared_and_then_it_dies(*args):
            clear(*args)
            raise Died
        with mock.patch.object(client, "_taken", cleared_and_then_it_dies), self.assertRaises(Died):
            self.next(token)
        self.assertEqual(self.kept(), [f"{token}.1.json"])
        with mock.patch.object(client, "_taken", side_effect=Died), self.assertRaises(Died):
            self.next(token)                                                 # run again, it dies before it clears:
        self.assertEqual(self.kept(), [f"{token}.1.json"])                   # nothing was put together anew
        new, _, _ = self.next(token)
        self.assertEqual(self.kept(), [f"{token}.1.json"])                   # was: gone
        hooked.consumed(self.r.dir, token)                                   # (and however often it is done)
        self.assertEqual(self.kept(), [f"{token}.1.json"])
        self.assertEqual(self.comes(inp, real), OK)
        self.assertEqual((self.late(token, 1).data, self.kept()), (self.me.data, [f"{token}.1.json", f"late/{token}.1.json"]))
        self.next(new)
        self.assertEqual((self.loose(), self.client()["gone"]), ({}, []))    # and its batch is over
        self.assertEqual(self.kept(), [f"{token}.1.json", f"late/{token}.1.json"])

    def test_a_brain_next_that_dies_before_it_clears_the_batch_away_clears_it_when_run_again(self):
        """The other side of the same crash: the brain has the batch, and nothing is cleared yet. The call that
        is out fails in the end."""
        token, lines = self.first_batch()
        inp, real = self.sent(lines[0])

        class Died(Exception):
            pass

        def dies(*args):
            raise Died
        with mock.patch.object(client, "_taken", dies), self.assertRaises(Died):
            self.next(token)
        self.assertEqual(self.kept(), [f"{token}.1.json", f"{token}.closed", f"{token}.results", f"{token}.seen"])
        new, _, _ = self.next(token)
        self.assertEqual(self.kept(), [f"{token}.1.json"])
        failed = dict(inp, hook_event_name="PostToolUseFailure", tool_input=real, error="connection reset by peer")
        self.assertIsNone(hook.run("fail", failed, self.r.dir))
        self.assertEqual(self.late(token, 1).error, "connection reset by peer")
        self.next(new)
        self.assertEqual((self.kept(), self.loose()), ([f"{token}.1.json", f"late/{token}.1.json"], {}))

    def test_results_in_the_inbox_for_a_batch_nobody_handed_in_are_kept_whoever_takes_over(self):
        """Also a relay without hooks: it took what was in the inbox for another batch away (the first note's
        limit; the re-review, on reading 1)."""
        got = self.handed_to_the_brain()
        token, lines = self.first_batch()
        self.does(lines)
        new, new_lines = self.first_batch(hooked=False)
        self.assertEqual(self.late(token, 1).data, self.me.data)
        self.assertEqual((self.puts(), got), ([], []))                       # (and are not the new relay's to hand in)
    def test_a_relay_without_hooks_keeps_nothing_there(self):
        token, lines = self.first_batch(hooked=False)
        self.assertEqual(brain.put(self.r.dir, token, 1, json.dumps(self.me.data)), 0)
        self.next(token, hooked=False)
        self.assertEqual(self.puts(), [])
        self.assertFalse(os.path.exists(os.path.join(self.r.dir, "hook")))


class OneAtATime(Hooks):
    """Whoever lets a call go, hands a result in, closes a batch or clears it away holds the lock for that
    moment (live/hook/lock), and so does `brain next` when it names a new relay: a batch is closed, and a
    relay replaced, between two of those and never during one."""

    def setUp(self):
        self.start()

    def waits_for_the_lock(self, does):
        done = []
        with hooked.lock(self.r.dir):
            thread = threading.Thread(target=lambda: done.append(does()))
            thread.start()
            thread.join(0.3)
            waited = thread.is_alive() and not done
        thread.join(60)
        self.assertEqual(len(done), 1)
        return waited

    def test_each_of_them_waits_while_another_has_it(self):
        token, lines = self.first_batch()
        self.does(lines)
        token, lines, _ = self.next(token)
        went = []
        self.assertTrue(self.waits_for_the_lock(lambda: went.append(self.sent(lines[0]))))   # a call is let go
        self.assertTrue(went[0][1])
        self.assertTrue(self.waits_for_the_lock(lambda: self.comes(*went[0])))               # a result handed in
        self.assertTrue(self.waits_for_the_lock(lambda: self.bash(json.loads(relay.next_line(token))["bash"])))
        self.assertTrue(self.waits_for_the_lock(lambda: hooked.consumed(self.r.dir, token)))
        self.assertEqual((self.kept(), self.puts()), ([], []))
        self.assertTrue(self.waits_for_the_lock(lambda: self.next(agent="c" * 16)))          # a new relay is named
        self.assertEqual(self.client()["hooks"], "c" * 16)


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


class TheHeadsBeforeThisOne(WhatAVersionBeforeLeft):
    def test_what_the_head_before_the_hooks_left_is_another_versions(self):
        """661f3f63 knows no hooks: a relay it named would be printed calls, and a batch it made carries no
        steps for a hook. Its number is 7, so nothing it left is taken for this version's."""
        self.nothing_it_made_is_delivered(BEFORE)

    def test_what_the_first_head_with_hooks_left_is_another_versions(self):
        """184ce648 handed a batch in without closing it, and its hooks kept less on record of one: a batch
        held under it has no closing to go by. Its number is 8."""
        self.nothing_it_made_is_delivered(REVIEWED)

    def test_what_its_correction_left_is_another_versions(self):
        """ec231943 handed a batch in as over while a call of it was out, and named a new relay outside the
        hooks' lock. Its number is 9."""
        self.nothing_it_made_is_delivered(REREVIEWED)


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

    def test_the_hooks_that_wait_are_given_the_time_to(self):
        """The hook in front of `brain next` waits for a batch's lines to end, the one in front of a call for
        the line before it and then the wait in front of its own: Claude Code must not end either first."""
        with open(os.path.join(C.ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
            text = f.read()
        time = {what: int(n) for what, n in re.findall(r'player\.hook (\w+)"\n +timeout: (\d+)', text)}
        self.assertEqual(set(time), {"bash", "pre", "post", "fail"})
        self.assertGreaterEqual(time["bash"], hooked.GRACE + hooked.TURN + 30)
        minute = 60                                  # the longest pause the pacing puts in front of a call (budget.pace)
        self.assertGreaterEqual(time["pre"], hooked.GRACE + hooked.TURN + minute + 30)

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
        self.assertIsNone(run(post, dict(call, tool_response=[{"type": "text", "text": "{}"}])))   # (no call's result)
        self.assertIsNone(run(fail, dict(call, error="x")))
        with open(os.path.join(live, "hook", "log.jsonl"), encoding="utf8") as f:
            self.assertEqual([json.loads(x)["hook"] for x in f], ["bash", "pre", "post", "fail"])


if __name__ == "__main__":
    unittest.main()
