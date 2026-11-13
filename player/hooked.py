"""The batch of a relay with hooks (player/hook.py), on record: its lines, its closing, what `brain next` hands
in for it, and when it is cleared away.

A batch on record (live/hook/), by its token T. No hook removes any of it, whatever batch it is of (review of
184ce648, H1: a hook that had read client.json before its relay was replaced swept away the new relay's
records, and a call went twice). It goes when the brain has the batch's results (consumed).

  T.seen       a hook has run in front of one of the batch's calls
  T.<n>.json   line n, made once, by the tool call that took it ("use", its id). It is refused ("refused"),
               or its call goes to the connector ("call"). {"passed": true}: no tool call took the line in
               time, and none may any more. "shown": its result could not be handed in (below)
  T.closed     how each line had ended when the batch was closed: answered, refused, passed, shown, or open
  T.results    what was handed in for the batch
  late/        results that came for a batch that was closed, or that its relay no longer held

The lines of a batch go in order. Line n's call goes when line n-1 has its answer, and not when that line was
refused or passed over: a batch is cut where a call is left out. A line waits GRACE for a tool call to take
the line before it and TURN for that line to end, so a batch whose tool calls Claude Code starts together is
still made in order.

Closing (review of 184ce648, H2: `brain next` took what results were there when it ran; one that came later
was dropped, or was added to a request the brain had answered already). Before `brain next` runs for the batch
its relay holds, every line is waited for until it has ended. Then how each ended is put on record, once
(T.closed). From then on no call of the batch goes, and no result is handed in for it: one that comes is kept
(late/). What the brain is handed is put together from that record, once (T.results): a `brain next` that
is run again hands in the same, whatever has come since. A call that was still open is handed in as an error
that says so, unless its result has come by then: that one is taken out of late/ and handed in. The brain takes no result for a batch but with the batch,
from a relay without hooks either: a late one stays in that relay's transcript.

A result that cannot be handed in (review of 184ce648, H3: the model was shown "ok" all the same, and the
result was nowhere). The model is shown the result itself then, so the relay's transcript has it, and it is
taken from there.

The lock (live/hook/lock) is held for a moment by whoever lets a call go, hands a result in, closes a batch
or clears it away: so a batch is closed between two of those, never during one.
"""
import contextlib
import fcntl
import os
import re
import time

from . import relay

GRACE = 2.0               # s a line is waited for to be taken by a tool call, before it is passed over
TURN = 120.0              # s a line that a tool call has taken is waited for: by the next line, and at closing
LOOK = 0.05               # s between looks while waiting
OLD = 3600.0              # s after which what is on record of a batch nobody handed in is removed
LINE = re.compile(r"^(.+)\.(\d+)\.json$")
NO_ANSWER = "no answer: the call went to the connector, and its result was not there when the batch was handed in"
NO_HOOKS = "STOP the relay's hooks are not running: nothing more is sent (player/OPERATOR.md, \"Hooks\")"


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


def on_record(live, token, what):
    return os.path.join(live, "hook", f"{token}.{what}")


def late(live, token, n):
    return os.path.join(live, "hook", "late", f"{token}.{n}.json")


@contextlib.contextmanager
def lock(live):
    os.makedirs(os.path.join(live, "hook"), exist_ok=True)
    with open(os.path.join(live, "hook", "lock"), "w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield


def once(path, content):
    """Make a file once, whole. -> whether this call made it."""
    mine = f"{path}.{os.getpid()}"
    relay.write(mine, content)
    try:
        os.link(mine, path)                                       # fails when the file is there already
    except FileExistsError:
        return False
    finally:
        os.unlink(mine)
    return True


# ---------------------------------------------------------------- its lines, and its closing
def shut(live, state, token):
    """Whether the batch is closed: no call of it goes any more, and no result is handed in for it."""
    return state.get("handed") == token or os.path.exists(on_record(live, token, "closed"))


def how(live, token, n):
    """How line n stands. None: no tool call has taken it. "open": one has, and it waits its turn, or its call
    is with the connector. Or how it ended: "answered", "refused", "passed", "shown"."""
    if os.path.exists(relay.put_path(live, token, n)):
        return "answered"
    line = relay.read(on_record(live, token, f"{n}.json"))
    if not isinstance(line, dict):
        return None
    return next((end for end in ("refused", "passed", "shown") if line.get(end)), "open")


def patience():
    """The looks one who waits has: for a line to be taken by a tool call, and for a line that was taken to end."""
    return {"grace": round(GRACE / LOOK), "turn": round(TURN / LOOK)}


def ended(live, token, n, sleep, left):
    """Wait for line n to end. -> how it ended; "open" when it has not in the time there is.
    left: the looks that are left (patience), for one who waits for several lines. A line that no tool call
    takes within the grace is passed over here, for good."""
    while True:
        now = how(live, token, n)
        if now not in (None, "open"):
            return now
        wait = "turn" if now else "grace"
        if left[wait] <= 0:
            if now or once(on_record(live, token, f"{n}.json"), {"passed": True}):
                return now or "passed"
            continue                                              # a tool call took the line this moment
        sleep(LOOK)
        left[wait] -= 1


def close(live, state, sleep=time.sleep):
    """The relay is about to hand in the batch it holds: every line is waited for, then how each ended is put
    on record, once. A line whose call has not gone by then does not go."""
    token, count = state["token"], len(calls(state))
    if os.path.exists(on_record(live, token, "closed")):
        return
    left = patience()
    for n in range(1, count + 1):
        ended(live, token, n, sleep, left)
    with lock(live):
        lines = {}
        for n in range(1, count + 1):
            lines[str(n)] = how(live, token, n)
            if lines[str(n)] == "open" and not (relay.read(on_record(live, token, f"{n}.json")) or {}).get("call"):
                lines[str(n)] = "refused"                         # (hook.release finds the batch closed)
        once(on_record(live, token, "closed"), {"at": round(time.time(), 2), "lines": lines})


# ---------------------------------------------------------------- what `brain next` does with it
def told(args):
    """What follows `brain next` -> (the same without the id, the id the Bash hook put there or None)."""
    if "--hooks" not in args:
        return list(args), None
    at = args.index("--hooks")
    return args[:at] + args[at + 2:], "".join(args[at + 1:at + 2]) or None


def stop(live, state, hooks):
    """`brain next`, of a relay that hands a batch in: what to say when its hooks cannot be relied on. None when
    they can, and for a relay that never had any.

    A relay is with hooks or without from its first `brain next` to its last: the id the hook puts behind the
    command is the one it was named under (client.json, "hooks"). A batch of calls it hands in was closed by
    that hook. And once it has been printed calls, the hook in front of the connector has been seen to run for
    them. If it has not, what the relay was printed went to the connector as it stood, as stand-ins, and no
    result will ever come: it is stopped before it is printed more. hooks: the id that came with this
    `brain next`, or None."""
    if (state.get("hooks") or None) != (hooks or None):
        return NO_HOOKS
    if not hooks or not state.get("calls") or state.get("handed") == state["token"]:
        return None
    if not os.path.exists(on_record(live, state["token"], "closed")):
        return NO_HOOKS
    if not state.get("seen"):
        if not os.path.exists(on_record(live, state["token"], "seen")):
            return NO_HOOKS
        state["seen"] = True
    return None


def _in_transcript(path, use, endpoint, sent):
    """A call's result as the relay's transcript has it, when the model was shown the result itself; None when
    it has "ok" in its place, or nothing."""
    try:
        hit = relay._span(path, "")[1].get(use) if path and use else None
    except OSError:
        hit = None
    body = hit[0].get("content") if hit else "ok"
    text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
    return None if text.strip() == "ok" else list(relay._result(endpoint, sent, hit[0], hit[1], path))


def handed_in(live, state, path):
    """The results of the batch a relay with hooks hands in, from how the batch was closed: put together once,
    and the same from then on. path: the relay's transcript, or None. -> [Result]"""
    token = state["token"]
    rows = relay.read(on_record(live, token, "results"))
    if not isinstance(rows, list):
        lines = (relay.read(on_record(live, token, "closed")) or {}).get("lines") or {}
        rows = []
        for n in sorted(int(k) for k, end in lines.items() if end in ("answered", "open", "shown")):
            endpoint, sent = state["calls"][n - 1]
            use = (relay.read(on_record(live, token, f"{n}.json")) or {}).get("use")
            with contextlib.suppress(OSError):                    # one that came between the closing and now
                os.replace(late(live, token, n), relay.put_path(live, token, n))
            rows.append(relay.read(relay.put_path(live, token, n)) or _in_transcript(path, use, endpoint, sent)
                        or list(relay.Result(endpoint, sent, None, NO_ANSWER, time.time())))
        relay.write(on_record(live, token, "results"), rows)
    return relay.unpack(rows)


def consumed(live, token):
    """The brain has the batch's results, and client.json says so (`brain next` holds the client's lock). What
    was handed in for the batch goes, with what is on record of it: but a line that was open stays, for the
    result that may yet come for it. A result that was handed in for a batch its relay did not live to hand in
    is kept (late/). Whatever is on record of any batch goes when it is OLD: no hook lives that long."""
    folder, inbox = os.path.join(live, "hook"), os.path.join(live, "inbox")
    if not os.path.isdir(folder):                                 # no relay has had hooks here
        return _puts(inbox, token, None)
    with lock(live):
        lines = (relay.read(on_record(live, token, "closed")) or {}).get("lines") or {}
        _puts(inbox, token, os.path.join(folder, "late"))
        os.utime(os.path.join(folder, "lock"))                    # the time, by the clock that stamps the files
        _cleared(folder, token, {n for n, end in lines.items() if end == "open"},
                 os.path.getmtime(os.path.join(folder, "lock")))


def _puts(inbox, token, aside):
    for name in [f for f in os.listdir(inbox) if f.startswith("put-")]:
        with contextlib.suppress(OSError):
            if name.startswith(f"put-{token}-"):
                os.unlink(os.path.join(inbox, name))
            elif aside:
                os.makedirs(aside, exist_ok=True)
                os.replace(os.path.join(inbox, name), os.path.join(aside, name))


def _cleared(folder, token, still_open, now):
    for root, _, names in os.walk(folder):
        for name in set(names) - {"log.jsonl", "lock"}:
            at, path = LINE.match(name), os.path.join(root, name)
            mine = root == folder and name.startswith(token + ".") and not (at and at.group(2) in still_open)
            with contextlib.suppress(OSError):
                if mine or now - os.path.getmtime(path) > OLD:
                    os.unlink(path)
