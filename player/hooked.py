"""The batch of a relay with hooks (player/hook.py), on record: its lines, its closing, what `brain next` hands
in for it, when it is over, and when it is cleared away.

A batch on record (live/hook/), by its token T. No hook removes any of it, whatever batch it is of (review of
184ce648, H1: a hook that had read client.json before its relay was replaced swept away the new relay's
records, and a call went twice). It goes when the brain has the batch's results (consumed).

  T.seen       a hook has run in front of one of the batch's calls
  T.<n>.json   line n, made once, by the tool call that took it ("use", its id). It is refused ("refused"),
               or its call goes to the connector ("call"). {"passed": true}: no tool call took the line in
               time, and none may any more
  T.closed     how each line had ended when the batch was closed: answered, refused, passed, or open
  T.results    what was handed in for the batch
  late/        T.<n>.json: the result of line n's call, when it could not go to the inbox: its batch was
               closed, its relay no longer held it, or the inbox could not be written

The lines of a batch go in order. Line n's call goes when line n-1 has its answer, and not when that line was
refused or passed over: a batch is cut where a call is left out. A line waits GRACE for a tool call to take
the line before it and TURN for that line to end, so a batch whose tool calls Claude Code starts together is
still made in order.

Closing (review of 184ce648, H2: `brain next` took what results were there when it ran; one that came later
was dropped, or was added to a request the brain had answered already). Before `brain next` runs for the batch
its relay holds, every line is waited for until it has ended. Then how each ended is put on record, once
(T.closed). From then on no call of the batch goes, and no result goes to the inbox for it. What the brain is
handed is put together from that record, once (T.results): a `brain next` that is run again hands in the
same, whatever has come since.

A call that is out (re-review of ec231943, R1: a call that had not come back when the batch was closed was
handed in as an error, and the batch as over; a read made while the purchase was still on its way then let
go what was reserved for it). A line is out when its call went to the connector and no result of it is on
record: not in the inbox, not in late/. Closed to new calls is not the same as every call that went being
over. So a batch with a line out is not handed in as over: client.json has it among the batches that are gone
(account), the brain keeps its calls against the minute and what they may cost reserved, and the call itself
is handed in as an error that says it has no answer. When the result is on record, `brain next` brings the
word that the batch is over as of then, and a read made after that pays off what was reserved (player/owed.py).
If it never comes, the operator's word ends it (`brain stopped`). The late result itself is kept and not
handed in: the brain takes no result for a batch but with the batch, from a relay without hooks either.

The same holds for a relay that was replaced and comes back while a call of its is out: its coming back is
no word that its batch is over (back).

A result the hook could not write down (review of 184ce648, H3; re-review of ec231943, R4: the line was put
down as done before the result was anywhere `brain next` could find it). The hook tries the inbox, then
late/. If neither can be written the model is shown the result itself, and the line stays out. `brain next`
looks for the results of lines that are out in the relay's own transcript, for a moment when it hands the
batch in and again every time it comes, and puts what it finds in late/ (recover).

The locks. live/hook/lock is held for a moment by whoever lets a call go, hands a result in, closes a batch,
clears it away, or names a new relay (re-review of ec231943, R2: a new relay was named between a hook's last
look at client.json and its letting the call go). `brain next` takes it while it holds the client's lock
(live/client.lock); a hook takes it alone. Never the other way round, and never across a wait.
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
SPOOL = (8, 0.25)         # looks, and the s between, for a result in the transcript when a batch is handed in
OLD = 3600.0              # s after which what is on record of a batch that is not out any more is removed
LINE = re.compile(r"^(.+)\.(\d+)\.json$")
NO_ANSWER = "no answer: the call went to the connector, and its result was not there when the batch was handed in"
NO_HOOKS = "STOP the relay's hooks are not running: nothing more is sent (player/OPERATOR.md, \"Hooks\")"
BARE = ("STOP this relay's hooks are not running, and the brain does not play through a relay without them "
        "(player/OPERATOR.md, \"Hooks\")")


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
def lock(live, make=True):
    """The hooks' lock. make=False: for one who is no hook; where no hook has ever run there is none to wait for."""
    if make or os.path.isdir(os.path.join(live, "hook")):
        os.makedirs(os.path.join(live, "hook"), exist_ok=True)
        with open(os.path.join(live, "hook", "lock"), "w") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            yield
    else:
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
    """Whether the batch is closed: no call of it goes any more, and no result goes to the inbox for it."""
    return state.get("handed") == token or os.path.exists(on_record(live, token, "closed"))


def _result(live, token, n):
    """Whether a result of line n's call is on record."""
    return os.path.exists(relay.put_path(live, token, n)) or os.path.exists(late(live, token, n))


def how(live, token, n):
    """How line n stands. None: no tool call has taken it. "open": one has, and it waits its turn, or its call
    is with the connector. Or how it ended: "answered", "refused", "passed"."""
    if _result(live, token, n):
        return "answered"
    line = relay.read(on_record(live, token, f"{n}.json"))
    if not isinstance(line, dict):
        return None
    return next((end for end in ("refused", "passed") if line.get(end)), "open")


def out(live, token):
    """The lines of the batch that are out: their call went to the connector, and no result of it is on record.
    -> {n: the line}"""
    found, folder = {}, os.path.join(live, "hook")
    for name in os.listdir(folder) if os.path.isdir(folder) else []:
        at = LINE.match(name)
        line = relay.read(os.path.join(folder, name)) if at and at.group(1) == token else None
        if isinstance(line, dict) and line.get("call") and not _result(live, token, int(at.group(2))):
            found[int(at.group(2))] = line
    return found


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


def bare(live, state, token, hooks):
    """`brain next` of a relay without hooks that would be given a name, or the batch it comes for: what it is
    told in their place; None for any other (RUL-2026-11-14-161).

    Under Claude Code itself a relay that is printed the calls themselves stopped of its own accord in 7
    sessions of 17: it made one call of five and went on, or it read the calls it carried and refused one. A
    relay with hooks did so in none of 58 (docs/reviews/evidence/ai_player_hook_relay/PROOF.md). So such a
    relay plays only where the director has said it may (live/control.json, relay_without_hooks: true), and
    is turned away before it is named: it replaces no relay that is running. hooks: the id that came with
    this `brain next`, or None. A relay that was named with hooks and comes without them is stop's; one that
    was replaced is told so, as before."""
    mine = token is not None and token == state.get("token") and not state.get("hooks")
    if hooks or not (token is None or mine):
        return None
    said = relay.read(os.path.join(live, "control.json"))
    return None if isinstance(said, dict) and said.get("relay_without_hooks") is True else BARE


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


def _look(live, token, path):
    """One look in the transcript for the lines of the batch that are out. What is found goes to late/."""
    left = out(live, token)
    try:
        answers = relay._span(path, "")[1] if left and path else {}
    except OSError:
        answers = {}
    for n, line in left.items():
        hit = answers.get(line.get("use"))
        body = hit[0].get("content") if hit else "ok"
        said = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
        if said.strip() != "ok":                                  # ("ok" stands there for one that was written down)
            relay.write(late(live, token, n), list(relay._result(*line["call"], hit[0], hit[1], path)))


def recover(live, token, path, sleep=None):
    """The lines of the batch that are out may have their results in the relay's transcript: the hook behind
    such a call could not write it down, or did not run, and the model was shown the result itself. What is
    found there goes to late/. path: that relay's transcript, or None. sleep: look again for a moment (SPOOL)
    while a line is still out. -> the lines still out."""
    looks = SPOOL[0] if sleep else 0
    while True:
        _look(live, token, path)
        left = out(live, token)
        if not left or not path or looks <= 0:
            return left
        sleep(SPOOL[1])
        looks -= 1


def handed_in(live, state, path, sleep=None):
    """The results of the batch a relay with hooks hands in, from how the batch was closed: put together once,
    and the same from then on. Nothing is put together for a batch the brain has had (re-review of ec231943,
    R3). A line that is still out is looked for in the relay's transcript first (recover), and is handed in as
    an error if it is not there. path: the relay's transcript, or None. -> [Result]"""
    token = state["token"]
    if state.get("handed") == token:
        return []
    rows = relay.read(on_record(live, token, "results"))
    if not isinstance(rows, list):
        lines = (relay.read(on_record(live, token, "closed")) or {}).get("lines") or {}
        recover(live, token, path, sleep)
        rows = []
        for n in sorted(int(k) for k, end in lines.items() if end in ("answered", "open")):
            with contextlib.suppress(OSError):                    # one that is in late/ goes with its batch after all
                os.replace(late(live, token, n), relay.put_path(live, token, n))
            rows.append(relay.read(relay.put_path(live, token, n)) or relay.read(late(live, token, n))
                        or list(relay.Result(*state["calls"][n - 1], None, NO_ANSWER, time.time())))
        relay.write(on_record(live, token, "results"), rows)
    return relay.unpack(rows)


def account(live, state, path):
    """Before `brain next` asks the brain: which batches are over, by what is on record of their calls.

    The batch being handed in, with a line still out, is not over: it goes from held to gone, as a batch whose
    relay did not hand it in, with the mark that it was closed. A batch that is gone with that mark, or with
    the mark that its replaced relay came back (back), is over when no line of it is out any more: that goes
    among the word for the brain (ended), as of the moment its last result came. Lines that are out are looked
    for in this relay's transcript first. state: client.json, changed here; the caller writes it."""
    held = state.get("held")
    if held and out(live, held["token"]):
        state["gone"], state["held"] = state["gone"] + [dict(held, closed=True)], None
    for was in [g for g in state["gone"] if g.get("closed") or g.get("back")]:
        if not recover(live, was["token"], path):
            state["gone"].remove(was)
            state["ended"] = state["ended"] + [[was["id"], _last(live, was["token"]), was["token"], "answered"]]


def _last(live, token):
    """When the last result on record of the batch came; now, if none is."""
    folder, times = os.path.join(live, "hook", "late"), []
    for name in os.listdir(folder) if os.path.isdir(folder) else []:
        row = relay.read(os.path.join(folder, name)) if name.startswith(token + ".") else None
        if isinstance(row, list) and len(row) == 5 and isinstance(row[4], (int, float)):
            times.append(row[4])
    return max(times, default=time.time())


def back(live, state, was):
    """A relay that was replaced is back with the token of a batch that is gone (`brain next` tells it to
    stop). That is the word that its batch is over, unless a call of it is still out: then it is marked, and is
    over when that call's result is on record (account). state: client.json, changed here."""
    if out(live, was["token"]):
        was["back"] = True
    else:
        state["gone"].remove(was)
        state["ended"] = (state.get("ended") or []) + [[was["id"], time.time(), was["token"], "back"]]


def consumed(live, token):
    """The brain has the batch's results, and client.json says so (`brain next` holds the client's lock). What
    was handed in for the batch goes, with what is on record of it, but for the lines that are out: those stay
    until their result is on record, whatever becomes of the batch. It can be done again and changes nothing
    more (re-review of ec231943, R3: done a second time it took the line of a call that was out, and the
    result that came for it was nowhere). A result in the inbox for another batch is kept (late/). What is
    on record of a batch that is neither held nor gone goes when it is OLD: no hook lives that long."""
    folder, inbox = os.path.join(live, "hook"), os.path.join(live, "inbox")
    if not os.path.isdir(folder):                                 # no relay has had hooks here
        return _puts(inbox, token, None)
    with lock(live):
        state = relay.read(os.path.join(live, "client.json")) or {}
        owed = {g.get("token") for g in [state.get("held")] + (state.get("gone") or []) if isinstance(g, dict)}
        still = {f"{token}.{n}.json" for n in out(live, token)}
        os.utime(os.path.join(folder, "lock"))                    # the time, by the clock that stamps the files
        _cleared(folder, token, still, owed, os.path.getmtime(os.path.join(folder, "lock")))
        _puts(inbox, token, live)                                 # last: a line with its result in the inbox is not out


def _puts(inbox, token, live):
    """The batch's results leave the inbox. Another batch's go to late/, under the name of their line: so a
    line that was answered is not taken for one that is out. live None: no relay has had hooks; they go."""
    for name in [f for f in os.listdir(inbox) if f.startswith("put-")]:
        whose, n = name[4:-5].rsplit("-", 1)
        with contextlib.suppress(OSError, ValueError):
            if whose == token or not live:
                os.unlink(os.path.join(inbox, name))
            else:
                os.makedirs(os.path.dirname(late(live, whose, int(n))), exist_ok=True)
                os.replace(os.path.join(inbox, name), late(live, whose, int(n)))


def _cleared(folder, token, still, owed, now):
    """still: the files of the batch's lines that are out. owed: the tokens of the batches that are held or gone."""
    for root, _, names in os.walk(folder):
        for name in set(names) - {"log.jsonl", "lock"}:
            path, whose = os.path.join(root, name), name.split(".")[0]
            mine = root == folder and whose == token and name not in still
            with contextlib.suppress(OSError):
                if mine or (whose not in owed and now - os.path.getmtime(path) > OLD):
                    os.unlink(path)
