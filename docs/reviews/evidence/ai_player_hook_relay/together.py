"""The relay's hooks as Claude Code runs them, started together: each one a process of its own, by the command
the agent file names. No request is made of the game: what stands for the connector is this script.

    python3 docs/reviews/evidence/ai_player_hook_relay/together.py [runs]

The review of 184ce648 could not say how Claude Code starts the tool calls of one message, and the hooks had
only been run one after another, in one process. Here a relay holds a batch of four calls. The hooks in front
of all four, and the one in front of `brain next`, are started at the same moment, the last line's first. Each
call that a hook lets go takes a tenth of a second, and then the hook behind it is run with its result.

What must hold, and is checked for every run:
- the four calls go, each once, in the batch's order, each after the one before it was answered;
- the hook in front of `brain next` ends only when all four have their results, and the brain is handed the four;
- nothing is left in the inbox, and nothing on record of the batch.

It runs the suite's stand-in for the game and its rig (player/tests/test_hook_relay.py), so the brain is the
real one, on a folder of its own. It is not a test of the suite: it takes real time, and a machine that is
busy enough to take two seconds over starting a process would fail it (hooked.GRACE).
"""
import io
import json
import os
import re
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, ROOT)

from player import brain, relay  # noqa: E402
from player.tests.test_hook_relay import AGENT, TOOL, Hooks  # noqa: E402

with open(os.path.join(ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
    BASH, PRE, POST, _ = [json.loads(x) for x in re.findall(r'command: ("(?:[^"\\]|\\.)*")', f.read())]
CLOCK = time.time                                                     # (the rig puts its own clock in its place)


def hook(command, inp, live):
    done = subprocess.run(command, shell=True, cwd=ROOT, input=json.dumps(inp), capture_output=True, text=True,
                          env=dict(os.environ, TNR_PLAYER_LIVE=live, CLAUDE_PROJECT_DIR=ROOT), timeout=300)
    assert (done.returncode, done.stderr) == (0, ""), (command, done.stderr)
    return json.loads(done.stdout)["hookSpecificOutput"] if done.stdout.strip() else None


def once():
    h = Hooks()
    h.start()
    try:
        token, lines = h.first_batch()
        h.does(lines)
        token, lines, _ = h.next(token)
        assert len(lines) == 4, lines
        went, back, shown, closed = [], {}, {}, []

        def a_call(n):
            inp = h.inp(TOOL, {"endpointName": lines[n - 1]["call"], "input": lines[n - 1]["input"]}, AGENT,
                        tool_use_id=f"toolu_together_{n}")
            said = hook(PRE, inp, h.r.dir)
            if said["permissionDecision"] != "allow":
                went.append((CLOCK(), n, said["permissionDecisionReason"]))
                return
            real = said["updatedInput"]
            went.append((CLOCK(), n, real["endpointName"]))
            time.sleep(0.1)                                           # the call is with the connector
            done = dict(inp, hook_event_name="PostToolUse", tool_input=real,
                        tool_response=[{"type": "text", "text": json.dumps(h.answer(real))}])
            back[n] = CLOCK()                                         # and comes back
            shown[n] = hook(POST, done, h.r.dir)["updatedToolOutput"]

        def brain_next():
            command = json.loads(relay.next_line(token))["bash"]
            said = hook(BASH, h.inp("Bash", {"command": command}, AGENT), h.r.dir)
            closed.append((CLOCK(), said["permissionDecision"], said.get("updatedInput", {}).get("command")))

        threads = [threading.Thread(target=a_call, args=(n,)) for n in (4, 3, 2, 1)]
        threads.append(threading.Thread(target=brain_next))
        for t in threads:
            t.start()
        for t in threads:
            t.join(400)
        want = [s["call"] for s in h.client()["steps"] if "call" in s]
        assert [(n, what) for _, n, what in sorted(went)] == list(enumerate(want, 1)), went
        assert shown == {n: [{"type": "text", "text": "ok"}] for n in (1, 2, 3, 4)}, shown
        assert all(back[n] <= sorted(went)[n][0] for n in (1, 2, 3)), (went, back)    # each after the one before came back
        assert closed[0][1] == "allow" and closed[0][0] >= back[4], (closed, back)    # and `brain next` after the last
        got = h.handed_to_the_brain()
        brain.next_batch(h.r.dir, token, io.StringIO(), h.sleep, hooks=AGENT)
        assert [x.endpoint for x in got] == want and all(x.error is None for x in got), got
        assert (h.kept(), h.puts()) == ([], []), (h.kept(), h.puts())
        return closed[0][0] - min(t for t, _, _ in went)
    finally:
        h.doCleanups()


if __name__ == "__main__":
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    took = [once() for _ in range(runs)]
    print(f"{runs} runs: four calls and `brain next`, their hooks started together as processes. Every run: the "
          f"calls in order, each after the answer before it; `brain next` after the last answer; four results "
          f"handed to the brain; nothing left over. From the first call let go to the closing: "
          f"{min(took):.2f} to {max(took):.2f} s.")
