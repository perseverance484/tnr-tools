"""The gate of the check for the operator's machine (preflight.py). A hook, given to each of the check's
sessions on its command line (--settings), in front of every tool call of the session and of its subagents.

    python3 preflight_gate.py start     at SessionStart: writes down that the command line's hooks run here
    python3 preflight_gate.py tool      at PreToolUse, every tool: refuses, or says nothing

It is not one of the relay's hooks and does not rest on them: whether those are run is what the check asks.
It never allows a call. It refuses one, or says nothing and leaves the call to whatever else decides. It is
declared with onFailure: block, so a gate that fails refuses.

What it refuses (review of 65974c02, B1 and B3: the brain's guard mode is not a ceiling on what a relay may
be asked to carry, and a watcher that looks at a session after it has started is not in front of its calls):

- everything, until preflight.py has looked at this session's first event and written the session's id into
  OUT/admitted. It waits ten seconds for that, then refuses;
- a command that is not `python3 -m player.brain next`, with a batch's token or none;
- a subagent, unless the check is of the subagent form, it is the relay's agent, and it is the first;
- a connector call that is not a read of my own profile: `profile.getUser` with nothing in its input. For a
  stand-in line it looks up what the line stands for in the batch the relay holds (live/client.json), as the
  relay's own hook does. What it cannot look up it refuses;
- a connector call after the check's three;
- any other tool.

Every decision is a row in OUT/gate.jsonl. preflight.py reads what was let through from there, not from the
relay's hooks.
"""
import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
sys.path.insert(0, ROOT)

from player import config as C, hooked  # noqa: E402

TOOL = "mcp__Tnr__callEndpoint"
PROBE = ("profile.getUser", {})
NEXT = re.compile(r"(?:cd " + re.escape(ROOT) + r" && )?python3 -m player\.brain next(?: [0-9a-f]+-\d+)?")
WAIT = 10.0


def stands_for(inp, live):
    """(endpoint, input) of the call this tool call would make of the connector; None when it cannot be told."""
    asked = inp.get("tool_input")
    if not isinstance(asked, dict) or not isinstance(asked.get("endpointName"), str):
        return None
    if asked["endpointName"] != C.STAND_IN:                       # (a relay without hooks is printed the call itself)
        return asked["endpointName"], asked.get("input") if asked.get("input") is not None else {}
    line, state = asked.get("input"), hooked.holding(live)
    if not (state and isinstance(line, dict) and line.get("b") == state["token"] and type(line.get("n")) is int):
        return None
    steps = hooked.calls(state)
    if not 1 <= line["n"] <= len(steps):
        return None
    step = steps[line["n"] - 1][0]
    return step["call"], step.get("input") if step.get("input") is not None else {}


def decide(inp, run, admitted, before, live):
    """-> (the kind of row this call is, why it is refused or None).
    run: OUT/run.json. admitted: the session id in OUT/admitted, or None. before: OUT/gate.jsonl so far."""
    tool, asked = inp.get("tool_name"), inp.get("tool_input") if isinstance(inp.get("tool_input"), dict) else {}
    if not admitted or admitted != inp.get("session_id"):
        return "early", "the check has not looked at this session yet"
    if tool == "Bash":
        ok = isinstance(asked.get("command"), str) and NEXT.fullmatch(asked["command"])
        return "bash", None if ok else "not `brain next`"
    if tool in ("Agent", "Task"):
        if run.get("form") != "subagent" or inp.get("agent_id"):
            return "agent", "no subagent is started in this form of the check"
        if asked.get("subagent_type") != run.get("agent"):
            return "agent", "not the relay's agent"
        if any(r.get("kind") == "agent" and not r.get("refused") for r in before):
            return "agent", "the relay has been started"
        return "agent", None
    if tool == TOOL:
        if sum(1 for r in before if r.get("kind") == "call" and not r.get("refused")) >= run.get("bound", 0):
            return "call", "the check's calls have been made"
        if stands_for(inp, live) != PROBE:
            return "call", "not a read of my own profile"
        return "call", None
    return "other", "not a tool of the relay"


def rows(path):
    try:
        with open(path, encoding="utf8") as f:
            return [json.loads(x) for x in f if x.strip()]
    except FileNotFoundError:
        return []


def locked(out):
    """One decision at a time: the count of calls let through is read and added to as one step."""
    path = os.path.join(out, "gate.lock")
    for _ in range(2000):
        try:
            os.close(os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
            return path
        except FileExistsError:
            time.sleep(0.005)
    raise RuntimeError("the gate's lock is held")


def note(out, row):
    with open(os.path.join(out, "gate.jsonl"), "a", encoding="utf8") as f:
        f.write(json.dumps(dict(row, at=round(time.time(), 3))) + "\n")


def admitted(out, session, wait=WAIT, sleep=time.sleep):
    for _ in range(int(wait / 0.05) + 1):
        try:
            with open(os.path.join(out, "admitted"), encoding="utf8") as f:
                one = f.read().strip()
            if one:
                return one
        except FileNotFoundError:
            pass
        sleep(0.05)
    return None


def main(argv=None, stdin=None, stdout=None):
    what, out = (argv or sys.argv[1:])[0], os.environ["TNR_PREFLIGHT_OUT"]
    inp = json.loads((stdin or sys.stdin).read())
    if what == "start":
        note(out, {"kind": "start", "session": inp.get("session_id")})
        return 0
    with open(os.path.join(out, "run.json"), encoding="utf8") as f:
        run = json.load(f)
    whose = admitted(out, inp.get("session_id"))
    lock = locked(out)
    try:
        kind, why = decide(inp, run, whose, rows(os.path.join(out, "gate.jsonl")),
                           os.environ.get("TNR_PLAYER_LIVE") or os.path.join(out, "live"))
        note(out, {"kind": kind, "tool": inp.get("tool_name"), "use": inp.get("tool_use_id"),
                   "by": inp.get("agent_id") or inp.get("session_id"), "session": inp.get("session_id"), "refused": why})
    finally:
        os.unlink(lock)
    if why:
        (stdout or sys.stdout).write(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": "the check's gate: " + why}}) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
