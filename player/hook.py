"""The relay's hooks (director 2026-11-13, RUL-2026-11-13-157): what Claude Code runs before and after every tool
call of a relay, so that the model in the relay carries neither a call nor its result.

    python3 -m player.hook bash     before a Bash command            (PreToolUse)
    python3 -m player.hook pre      before a call of the connector   (PreToolUse)
    python3 -m player.hook post     after one that was answered      (PostToolUse)
    python3 -m player.hook fail     after one that failed            (PostToolUseFailure)

Each reads the hook's input, JSON, on standard input and writes its answer, JSON, to standard output. The
relay's agent file (.claude/agents/tnr-relay.md) names them. Nothing here decides what is played.

Why. A batch is one model request, and a request carries the relay's whole conversation. Without hooks the
model writes every call out in full, and every result lands in its conversation: a full read of a fight is
some 15,000 tokens, read again with every batch after it. What that costs is in RUL-2026-11-13-156.

How it goes, for a relay whose `brain next` came through the first hook:

  bash   The relay's one command is `brain next`. That line is let through with the relay's own id added
         (--hooks ID): so `brain next` knows hooks run for this relay, and to whom it prints. Every other
         command is refused.
  batch  `brain next` prints no call to such a relay. In place of call n it prints a stand-in: the connector's
         tool with endpointName STAND_IN and input {"b": the batch's token, "n": n}. The waits of the batch are
         not printed: they are spent here.
  pre    The real call is put in the stand-in's place: endpoint, input and select, as `brain next` kept the
         batch in live/client.json. Everything else is refused, in this order: a tool that is not the
         connector's call; a call that is not a stand-in, to the letter; a batch that is not the one this relay
         holds, or that it has handed in; a call the batch has not got; a lease of the run lock that has run
         out; a call whose turn it is not (the one before it has not been made, or not answered); a call that
         was made already. A refused call is not made: the game never sees it.
  post   The result goes to the brain as `brain put` hands one in (live/inbox/put-<token>-<n>.json), and the
         model is shown "ok" in its place.
  fail   The same for a call that failed. The model sees the error, which is short.

What a hook that does not run can cost: nothing in the game. A stand-in that reaches the connector names no
endpoint of the game. A relay whose `brain next` comes without the id is a relay without hooks, and is given
its batches as before (player/relay.py, lines). A relay with hooks whose first calls came back with no sign
of this file having run is told to stop (stop).

What it was tried on: Claude Code 2.1.323, 2026-11-13, one read of my own profile's status through the
connector (docs/reviews/evidence/ai_player_hook_relay/). A hook's input carries the agent's id, the tool's
name and input and the id of the tool call; PostToolUse also the result, as a list of text blocks.
"""
import json
import os
import re
import sys
import time

from . import config as C
from . import relay

OK = [{"type": "text", "text": "ok"}]
"""What the model is shown in place of a result."""

TURN = 30.0               # s a call waits for the one before it to be answered, before it is refused
LOOK = 0.05               # s between looks while it waits
BASH = re.compile(r"^(?:cd " + re.escape(C.ROOT) + r" && )?python3 -m player\.brain next(?: [0-9a-f]+-\d+)?$")
ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")


def who(inp):
    """The id of whoever made the tool call: the subagent's, or the session's when the relay is its main agent."""
    one = inp.get("agent_id") or inp.get("session_id")
    return one if isinstance(one, str) and ID.match(one) else None


def holding(live):
    """live/client.json, when it is this version's and names a relay with hooks and the batch it holds."""
    state = relay.read(os.path.join(live, "client.json"))
    good = (relay.ours(state) and isinstance(state.get("hooks"), str) and isinstance(state.get("token"), str)
            and isinstance(state.get("steps"), list))
    return state if good else None


def calls(state):
    """The batch's calls in order, each with the seconds to wait in front of it: [(step, wait)]."""
    out, wait = [], 0.0
    for step in state["steps"]:
        if "call" in step:
            out.append((step, wait))
            wait = 0.0
        else:
            wait += step.get("wait", 0)
    return out


# ---------------------------------------------------------------- what is on record of a batch's calls
def _claim(live, token, n):
    return os.path.join(live, "hook", f"{token}.{n}.json")


def _first(live, token):
    """The hooks run in front of this batch's calls. Said once a batch: what is on record of any other batch
    is of no use any more, and goes."""
    mark = os.path.join(live, "hook", f"{token}.seen")
    if os.path.exists(mark):
        return
    os.makedirs(os.path.dirname(mark), exist_ok=True)
    for name in os.listdir(os.path.dirname(mark)):
        if not name.startswith(token + ".") and name != "log.jsonl":
            try:
                os.unlink(os.path.join(os.path.dirname(mark), name))
            except OSError:
                pass
    relay.write(mark, True)


def told(args):
    """What follows `brain next` -> (the same without the id, the id the Bash hook put there or None)."""
    if "--hooks" not in args:
        return list(args), None
    at = args.index("--hooks")
    return args[:at] + args[at + 2:], "".join(args[at + 1:at + 2]) or None


NO_HOOKS = "STOP the relay's hooks are not running: nothing more is sent (player/OPERATOR.md, \"Hooks\")"


def stop(live, state, hooks):
    """`brain next`, of a relay that hands a batch in: what to say when its hooks cannot be relied on. None when
    they can, and for a relay that never had any.

    A relay is with hooks or without from its first `brain next` to its last: the id the hook puts behind the
    command is the one it was named under (client.json, "hooks"). And once it has been printed calls, the hook
    in front of the connector has been seen to run for them. If it has not, what the relay was printed went to
    the connector as it stood, as stand-ins, and no result will ever come: it is stopped before it is printed
    more. hooks: the id that came with this `brain next`, or None."""
    if (state.get("hooks") or None) != (hooks or None):
        return NO_HOOKS
    if not hooks:
        return None
    if not state.get("seen") and state.get("calls"):
        if not os.path.exists(os.path.join(live, "hook", f"{state['token']}.seen")):
            return NO_HOOKS
        state["seen"] = True
    return None


def _note(live, what, inp, why=None):
    """One line in live/hook/log.jsonl: for the operator, who cannot see why a call was refused otherwise."""
    try:
        os.makedirs(os.path.join(live, "hook"), exist_ok=True)
        with open(os.path.join(live, "hook", "log.jsonl"), "a", encoding="utf8") as f:
            f.write(json.dumps({"at": round(time.time(), 2), "hook": what, "by": who(inp),
                                "tool": inp.get("tool_name"), "use": inp.get("tool_use_id"), "refused": why}) + "\n")
    except OSError:
        pass


# ---------------------------------------------------------------- before a Bash command
def stamped(inp):
    """-> (the command with this relay's id behind it, None), or (None, why it is refused)."""
    asked = inp.get("tool_input") if isinstance(inp.get("tool_input"), dict) else {}
    command = str(asked.get("command", "")).strip()
    if not BASH.match(command):
        return None, "a relay runs `brain next`, exactly as it is printed, and no other command"
    if not who(inp):
        return None, "this relay has no id that the hooks can pass on"
    return dict(asked, command=f"{command} --hooks {who(inp)}"), None


# ---------------------------------------------------------------- before a call of the connector
def _stand_in(inp):
    """(the batch's token, n) when the tool call is a stand-in, to the letter; else None."""
    asked = inp.get("tool_input")
    if not (str(inp.get("tool_name", "")).endswith("callEndpoint") and isinstance(asked, dict)
            and set(asked) == {"endpointName", "input"} and asked["endpointName"] == C.STAND_IN):
        return None
    line = asked["input"]
    if not (isinstance(line, dict) and set(line) == {"b", "n"} and isinstance(line["b"], str)
            and type(line["n"]) is int):
        return None
    return line["b"], line["n"]


def _may(state, inp, token, n, now):
    """Why call n of batch `token` may not be made now, by what client.json says; None when it may."""
    if state is None:
        return "no relay with hooks holds a batch"
    if who(inp) != state["hooks"]:
        return "that batch is another relay's"
    if token != state["token"]:
        return "that batch is not the one this relay holds"
    if state.get("handed") == token:
        return "that batch has been handed in"
    if not 1 <= n <= len(calls(state)):
        return "the batch has no such call"
    until = state.get("until")
    if until is not None and (not isinstance(until, (int, float)) or isinstance(until, bool) or now >= until):
        return "the run lock's lease does not reach this call"
    return None


def _turn(live, token, n, sleep):
    """Why it is not call n's turn; None when it is. The call before it has been made, and is answered (it is
    waited for: a relay's calls may be started together)."""
    if n == 1:
        return None
    if not os.path.exists(_claim(live, token, n - 1)):
        return f"call {n - 1} of the batch comes first"
    waited = 0.0
    while not os.path.exists(relay.put_path(live, token, n - 1)):
        if waited >= TURN:
            return f"call {n - 1} of the batch has not been answered"
        sleep(LOOK)
        waited += LOOK
    return None


def _mine(live, token, n, use):
    """Call n is this tool call's, and no other's: its file is made once, whole. -> whether it is."""
    path = _claim(live, token, n)
    mine = f"{path}.{os.getpid()}"
    relay.write(mine, {"use": use, "at": round(time.time(), 2)})
    try:
        os.link(mine, path)                                       # fails when the call is someone's already
    except FileExistsError:
        return False
    finally:
        os.unlink(mine)
    return True


def release(live, inp, sleep=time.sleep):
    """-> (the real call's input for the connector's tool, None), or (None, why the call is refused)."""
    line = _stand_in(inp)
    if line is None:
        return None, "not a line of the batch: a call is made as it is printed, and only so"
    token, n = line
    state = holding(live)
    if state is not None and token == state["token"]:
        _first(live, token)
    why = _may(state, inp, token, n, time.time()) or _turn(live, token, n, sleep)
    if why:
        return None, why
    if not _mine(live, token, n, inp.get("tool_use_id")):
        return None, "that call was made already"
    step, wait = calls(state)[n - 1]
    if wait > 0:
        sleep(wait)
    why = _may(holding(live), inp, token, n, time.time())             # the wait is over: is it still so?
    if why:                                                       # (whatever it is, it holds for the calls behind)
        return None, why
    return {"endpointName": step["call"], "input": step["input"], "select": step["select"]}, None


# ---------------------------------------------------------------- after a call of the connector
def answered(live, inp, error=None):
    """The call's result, handed in as `brain put` hands one in. error: the text of a call that failed.
    -> whether a result was taken."""
    state, use = holding(live), inp.get("tool_use_id")
    if state is None or not use:
        return False
    token = state["token"]
    n = next((k for k in range(1, len(calls(state)) + 1)
              if (relay.read(_claim(live, token, k)) or {}).get("use") == use), None)
    if n is None:
        return False                                              # not a call this file let through
    step, now = calls(state)[n - 1][0], time.time()
    if error is None:
        body = inp.get("tool_response")
        body = body.get("content") if isinstance(body, dict) else body
        try:
            result = relay.from_text(step["call"], step["input"],
                                     relay._text(body, inp.get("transcript_path") or "").strip(), now)
        except (OSError, ValueError) as err:
            result = relay.Result(step["call"], step["input"], None, f"unreadable result: {err}", now)
    else:
        result = relay.from_text(step["call"], step["input"], str(error).strip() or "Error: no text", now, True)
    relay.put(live, token, n, result)
    return True


# ---------------------------------------------------------------- the commands
def _answer(event, decision, why, updated=None):
    out = {"hookEventName": event, "permissionDecision": decision, "permissionDecisionReason": why}
    if updated is not None:
        out["updatedInput"] = updated
    return {"hookSpecificOutput": out}


def run(what, inp, live=None, sleep=time.sleep):
    """One hook, on its input. -> its answer (a dict), or None for no answer."""
    live = live or C.live_dir()
    if what in ("bash", "pre"):
        try:
            updated, why = stamped(inp) if what == "bash" else release(live, inp, sleep)
        except Exception as err:  # noqa: BLE001  (whatever goes wrong here, the call is not made)
            updated, why = None, f"the relay's hook failed: {err!r}"[:200]
        _note(live, what, inp, why)
        if why:
            return _answer("PreToolUse", "deny", why)
        return _answer("PreToolUse", "allow", "the relay's batch", updated)
    try:
        taken = answered(live, inp, None if what == "post" else str(inp.get("error") or ""))
    except Exception as err:  # noqa: BLE001  (the result is lost; the model is still not shown it)
        taken = False
        _note(live, what, inp, f"the result was not taken: {err!r}"[:200])
    else:
        _note(live, what, inp, None if taken else "not a call of the batch")
    if what == "post":
        return {"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": OK}}
    return None


def main(argv=None, stdin=None, stdout=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 1 or argv[0] not in ("bash", "pre", "post", "fail"):
        sys.stderr.write(__doc__.split("\n\n")[1] + "\n")
        return 2
    try:
        inp = json.loads((stdin or sys.stdin).read())
    except ValueError:
        inp = None
    if not isinstance(inp, dict):
        inp = {}                                                   # nothing can be told of it: it is refused
    out = run(argv[0], inp)
    if out is not None:
        (stdout or sys.stdout).write(json.dumps(out) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
