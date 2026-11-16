"""The relay's hooks (director 2026-11-13, RUL-2026-11-13-157): what Claude Code runs before and after every tool
call of a relay, so that the model in the relay carries neither a call nor its result.

    python3 -m player.hook bash     before a Bash command            (PreToolUse)
    python3 -m player.hook pre      before a call of the connector   (PreToolUse)
    python3 -m player.hook post     after one that was answered      (PostToolUse)
    python3 -m player.hook fail     after one that failed            (PostToolUseFailure)

Each reads the hook's input, JSON, on standard input and writes its answer, JSON, to standard output. The
relay's agent file (.claude/agents/tnr-relay.md) names them. Nothing here decides what is played. What is kept
of a batch, how it is closed and what `brain next` makes of it is in player/hooked.py.

Why. A batch is one model request, and a request carries the relay's whole conversation. Without hooks the
model writes every call out in full, and every result lands in its conversation: a full read of a fight is
some 15,000 tokens, read again with every batch after it. What that costs is in RUL-2026-11-13-156.

How it goes, for a relay whose `brain next` came through the first hook:

  batch  `brain next` prints no call to such a relay. In place of call n it prints a stand-in: the connector's
         tool with endpointName STAND_IN and input {"b": the batch's token, "n": n}. The waits of the batch are
         not printed: they are spent here.
  pre    The real call is put in the stand-in's place: endpoint, input and select, as `brain next` kept the
         batch in live/client.json. Everything else is refused, and a refused call is not made. A line of the
         batch is one tool call's, once, and goes when the line before it has its answer.
  post   The result goes to the brain as `brain put` hands one in (live/inbox/put-<token>-<n>.json), and only
         when it is written down is the model shown "ok" in its place. One that comes when its batch is
         closed is kept aside.
  fail   The same for a call that failed. The model sees the error, which is short.
  bash   The relay's one command is `brain next`. Every other is refused. `brain next` is let through with the
         relay's own id behind it (--hooks ID): so `brain next` knows hooks run for this relay. The batch the
         relay hands in with it is closed first: every call of it that went is waited for.

No hook removes anything that is on record of a batch, whatever batch it is of (review of 184ce648, H1).

What a hook that does not run can cost: nothing in the game. A stand-in that reaches the connector names no
endpoint of the game. A relay whose `brain next` comes without the id is a relay without hooks, and is given
its batches as before (player/relay.py, lines). A relay with hooks whose batch was not closed here, or whose
first calls came back with no sign of this file having run, is told to stop (hooked.stop). A result this file
cannot write down is left in front of the model: the relay's transcript has it then, and `brain next` looks
for it there (review of 184ce648, H3; hooked.recover).

What it was tried on: Claude Code 2.1.323, 2026-11-13, one read of my own profile's status through the
connector (docs/reviews/evidence/ai_player_hook_relay/). A hook's input carries the agent's id, the tool's
name and input and the id of the tool call; PostToolUse also the result, as a list of text blocks.
"""
import contextlib
import json
import os
import re
import sys
import time

from . import config as C
from . import relay
from .hooked import LINE, calls, close, ended, holding, late, lock, on_record, once, patience, shut

OK = [{"type": "text", "text": "ok"}]
"""What the model is shown in place of a result that has been taken from it."""

BASH = re.compile(r"^(?:cd " + re.escape(C.ROOT) + r" && )?python3 -m player\.brain next(?: ([0-9a-f]+-\d+))?$")
ID = re.compile(r"^[A-Za-z0-9_-]{1,80}$")


def who(inp):
    """The id of whoever made the tool call: the subagent's, or the session's when the relay is its main agent."""
    one = inp.get("agent_id") or inp.get("session_id")
    return one if isinstance(one, str) and ID.match(one) else None


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
def stamped(live, inp, sleep=time.sleep):
    """-> (the command with this relay's id behind it, None), or (None, why it is refused). When the relay is
    handing in the batch it holds, that batch is closed first (hooked.close)."""
    asked = inp.get("tool_input") if isinstance(inp.get("tool_input"), dict) else {}
    command = str(asked.get("command", "")).strip()
    line = BASH.match(command)
    if not line:
        return None, "a relay runs `brain next`, exactly as it is printed, and no other command"
    if not who(inp):
        return None, "this relay has no id that the hooks can pass on"
    state = holding(live)
    if (state and line.group(1) == state["token"] and who(inp) == state["hooks"]
            and state.get("handed") != state["token"]):
        close(live, state, sleep)
    return dict(asked, command=f"{command} --hooks {who(inp)}"), None


# ---------------------------------------------------------------- before a call of the connector
def _stand_in(inp):
    """(the batch's token, n) when the tool call is a stand-in, to the letter, and has an id; else None."""
    asked = inp.get("tool_input")
    if not (str(inp.get("tool_name", "")).endswith("callEndpoint") and isinstance(asked, dict)
            and set(asked) == {"endpointName", "input"} and asked["endpointName"] == C.STAND_IN
            and isinstance(inp.get("tool_use_id"), str) and inp["tool_use_id"]):
        return None
    line = asked["input"]
    if not (isinstance(line, dict) and set(line) == {"b", "n"} and isinstance(line["b"], str)
            and type(line["n"]) is int):
        return None
    return line["b"], line["n"]


def _whose(state, inp, token):
    """Why batch `token` is not this tool call's to make a call of, by what client.json says; None when it is."""
    if state is None:
        return "no relay with hooks holds a batch"
    if who(inp) != state["hooks"]:
        return "that batch is another relay's"
    if token != state["token"]:
        return "that batch is not the one this relay holds"
    return None


def _take(live, state, token, n, use):
    """Line n of the batch this relay holds becomes one tool call's. -> why it does not, or None.
    From here on the hook has been seen to run for the batch, whatever comes of the line."""
    if not os.path.exists(on_record(live, token, "seen")):
        relay.write(on_record(live, token, "seen"), True)
    if not 1 <= n <= len(calls(state)):
        return "the batch has no such call"
    if shut(live, state, token):
        return "that batch has been handed in"
    if not once(on_record(live, token, f"{n}.json"), {"use": use}):
        return "that call was made already, or its turn has passed"
    return None


def _over(live, state, token):
    """Why no call of the batch goes any more; None while they do."""
    if shut(live, state, token):
        return "that batch has been handed in"
    until = state.get("until")
    if until is not None and (not isinstance(until, (int, float)) or isinstance(until, bool)
                              or time.time() >= until):
        return "the run lock's lease does not reach this call"
    return None


def _turn(live, token, n, sleep):
    """Why it is not line n's turn; None when it is: the line before it has its answer."""
    if n == 1:
        return None
    end = ended(live, token, n - 1, sleep, patience())
    if end == "answered":
        return None
    return f"call {n - 1} of the batch " + ("has not been answered" if end == "open" else "was not made")


def release(live, inp, sleep=time.sleep):
    """-> (the real call's input for the connector's tool, None), or (None, why the call is refused)."""
    line = _stand_in(inp)
    if line is None:
        return None, "not a line of the batch: a call is made as it is printed, and only so"
    (token, n), use, state = line, inp["tool_use_id"], holding(live)
    why = _whose(state, inp, token) or _take(live, state, token, n, use)
    if why:
        return None, why                                          # (the line is not this tool call's)
    step, wait = calls(state)[n - 1]
    why = _turn(live, token, n, sleep) or _over(live, state, token)
    if not why and wait > 0:
        sleep(wait)
    with lock(live):                                              # the waits are over: is it all still so?
        state = holding(live)
        why = why or _whose(state, inp, token) or _over(live, state, token)
        relay.write(on_record(live, token, f"{n}.json"),
                    {"use": use, "refused": why} if why else {"use": use, "call": [step["call"], step["input"]]})
    if why:
        return None, why
    return {"endpointName": step["call"], "input": step["input"], "select": step["select"]}, None


# ---------------------------------------------------------------- after a call of the connector
def _made(live, use):
    """The line whose call this tool call was, whatever batch it is of: (token, n, [endpoint, input]); or None."""
    folder = os.path.join(live, "hook")
    for name in sorted(os.listdir(folder)) if use and os.path.isdir(folder) else []:
        at = LINE.match(name)
        line = relay.read(os.path.join(folder, name)) if at else None
        if isinstance(line, dict) and line.get("use") == use and line.get("call"):
            return at.group(1), int(at.group(2)), line["call"]
    return None


def answered(live, inp, error=None):
    """A call's result, written down. It goes to the inbox, as `brain put` hands one in, while its batch is the
    one held and is not closed; to live/hook/late/ after that, and when the inbox cannot be written. If it
    cannot be written there either, that is raised. error: the text of a call that failed.
    -> "handed in", "kept", or None for a tool call that was no call of a batch: nothing is written for that."""
    made = _made(live, inp.get("tool_use_id"))
    if made is None:
        return None
    token, n, (endpoint, sent) = made
    now = time.time()
    if error is None:
        body = inp.get("tool_response")
        body = body.get("content") if isinstance(body, dict) else body
        try:
            result = relay.from_text(endpoint, sent, relay._text(body, inp.get("transcript_path") or "").strip(), now)
        except (OSError, ValueError) as err:
            result = relay.Result(endpoint, sent, None, f"unreadable result: {err}", now)
    else:
        result = relay.from_text(endpoint, sent, str(error).strip() or "Error: no text", now, True)
    with lock(live):
        state = holding(live)
        if state is not None and token == state["token"] and not shut(live, state, token):
            with contextlib.suppress(OSError):
                relay.put(live, token, n, result)
                return "handed in"
        relay.write(late(live, token, n), list(result))
    return "kept"


def _dropped(live, inp, why):
    """A hook failed with a line in its hand, before the line's call went. The line says so, if that can be
    written: nobody waits for it then."""
    with contextlib.suppress(Exception):
        (token, n), use = _stand_in(inp), inp["tool_use_id"]
        with lock(live):
            if relay.read(on_record(live, token, f"{n}.json")) == {"use": use}:
                relay.write(on_record(live, token, f"{n}.json"), {"use": use, "refused": why})


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
            updated, why = stamped(live, inp, sleep) if what == "bash" else release(live, inp, sleep)
        except Exception as err:  # noqa: BLE001  (whatever goes wrong here, the call is not made)
            updated, why = None, f"the relay's hook failed: {err!r}"[:200]
            _dropped(live, inp, why)
        _note(live, what, inp, why)
        if why:
            return _answer("PreToolUse", "deny", why)
        return _answer("PreToolUse", "allow", "the relay's batch", updated)
    try:
        end = answered(live, inp, None if what == "post" else str(inp.get("error") or ""))
    except Exception as err:  # noqa: BLE001  (it is nowhere but in front of the model: it is left there)
        end = None
        _note(live, what, inp, f"the result could not be written down: {err!r}"[:200])
    else:
        _note(live, what, inp, {"handed in": None, "kept": "the result is kept beside the late ones"}.get(
            end, "not a call of a batch"))
    if what == "post" and end:                                    # written down: the model need not carry it
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
