"""The hands: how batches reach a relay agent and how results come back (design 4.1, 4.7).

The relay is a small model in a loop: run `brain next`, make the calls it prints, exactly and in order, run
`brain next` again. It holds no state and decides nothing, so any relay can replace any other.

- Every relay gets a name on its first `brain next`, and every batch a token (the relay's name and the batch's
  number). The batch's last line is `brain next <token>`, so the relay hands each batch in under its token.
- Results are read from the relay's own transcript (Claude Code records every call and its exact result there), so
  the relay spends no tokens echoing them. The transcript is the one that holds the Bash call `brain next <token>`,
  and only the calls the relay made since its previous `brain next` are read, each matched to a call the batch
  asked for. A result from an earlier batch, another relay or another session is never taken.
- `brain put` is the fallback when no transcript carries the token: the batch then asks for each result in turn.
- The same transcript gives the relay's token use: per batch, and its context size, which decides rotation.
- Requests and batches are files under live/inbox and live/outbox, written whole and renamed into place. Each
  request has an id of its own in its file's name, and its answer is the file with the same number and id.
"""
import datetime as dt
import glob
import json
import os
import re
import time

from . import config as C
from .world import RATE_LIMITED, Result

PROTOCOL = 10
"""What `brain next` and the brain mean by what they keep for each other, and the rules a batch is made under.
Each of these carries the number of the code that made it: live/client.json and a request (`brain next`), an
answer, the batch waiting to be printed that is made of it, the receipt, and the call ledger (the brain). One
that does not carry this number is never used as if it did: a client file is read as no file, a request is not
answered, an answer is not taken, a waiting batch is not printed, a receipt's batch is not given again, a ledger
is taken over with a minute's calls held (Brain._take_over). Whatever calls it stood for stay in the ledger,
held. A record's shape cannot say this: an older version wrote a waiting batch with every field this one
writes, admitted under a rule this one no longer keeps (review of 60a28a84).

A request is also published under a name that carries the number (request_path). A brain reads the requests
of its own protocol and no other's, so what one version's `brain next` asks is never taken by another
version's brain.

Change the number whenever the meaning of one of these records changes, or the rules by which the brain admits
a batch's calls. When in doubt, change it: a new number costs the operator one word and a minute (OPERATOR.md,
"After the player's code is updated"); an old one can cost the limit. The numbers so far:
  1  06358ca5 to c412de4d: the records carry a number.
  2  no call after a ledger is taken over from another version, until the operator has spoken and a minute
     after. c412de4d brought that rule in and kept the number at 1, so a batch its predecessor had admitted
     without the rule (waiting in client.json, kept in a receipt, or made by a brain still running) was still
     printed as this version's own (review of c412de4d). A change to the rule is a new number: that is what
     makes every record made under the old rule another version's.
  3  the operator's word lets go the hold of the takeover it was said of, and of no later one. Under 2 the
     hold was named by the old file's bytes alone, so word kept through a crash let go the hold of a later
     file of the same bytes (second review of c412de4d). A batch made after such a word is one this version
     would not have made.
  4  no word is taken for a takeover while it is being saved. Under 3 the count was raised before the world
     model was written, and word said between the two was kept under the name of the next takeover of those
     bytes (review of e4a267cd). The same reason as for 3.
  5  a save of a takeover is closed only by the one who has the brain's lock. Under 4 anything that made a
     World closed it, a living brain's too, and word said then was again kept under the name of a later
     takeover (review of ce1be6e9). The same reason as for 3.
  6  a batch carries the cutoff of the run lock's lease it was made under, and is not printed when its last
     call would be made at or after it (player/runlock.py). Under 5 the lease was looked at when a batch
     was planned and never again: one that waited, or was given again from its receipt, was printed after
     the lease had run out (review of 988c56cc, H1). A batch with no cutoff on record is another version's.
  7  what a batch may cost stays reserved, and what it may equip stays unread, until a read that is known to
     follow the batch (player/owed.py); and no trip is started by choice over the pocket's limit, the bank
     switched off or not. Under 6 a replacement's earlier read let a second batch of purchases through, and
     the hunt on (re-review of 87e497a6, H2 to H4): batches this version would not have made.
  8  a relay whose `brain next` comes through its hook (player/hook.py) is printed stand-ins, not calls, and
     its results come from the hooks: client.json says which kind a relay is, which under 7 no file says.
  9  such a relay's batch is closed by its hook before it is handed in, and the brain is handed what is on
     record of the closing (player/hooked.py). Under 8 (184ce648, never run) `brain next` took what was there.
  10 a batch with a call still out is handed in as gone, not held, and a relay is named under the hooks'
     lock. Under 9 (ec231943, never run) such a batch was handed in as over (its re-review, R1 to R4)."""


def ours(record):
    """Whether a record carries this protocol's number, as the number it is: not true, not 1.0, not "1"."""
    return isinstance(record, dict) and type(record.get("protocol")) is int and record["protocol"] == PROTOCOL


NEXT = re.compile(r"player\.brain\s+next(?:\s+([0-9a-f]+-\d+))?(?=\s|$)")
SAVED = re.compile(r"^Error: result \(([\d,]+) characters[^)]*\) exceeds maximum allowed tokens\. "
                   r"Output has been saved to (\S+?\.txt)\.")
PERSISTED = re.compile(r"^<persisted-output>\s*\nOutput too large \([^)]*\)\. Full output saved to: (\S+?\.json)\s*\n")
TAIL = 4_000_000          # bytes of transcript read back: one batch of full battle reads fits many times over
FIND_TAIL = 400_000       # bytes looked through for a batch's token: it is the relay's newest call
RECENT = 120.0            # s: a transcript not written to for this long is not a running relay's


# ---------------------------------------------------------------- the relay's transcript
def _rows(path, tail=TAIL):
    with open(path, "rb") as f:
        f.seek(max(0, os.path.getsize(path) - tail))
        for line in f.read().decode("utf8", "ignore").splitlines():
            try:
                yield json.loads(line)
            except ValueError:
                continue


def _blocks(row):
    content = (row.get("message") or {}).get("content")
    return [c for c in content if isinstance(c, dict)] if isinstance(content, list) else []


def _next_token(block):
    """The token of a Bash `brain next` call ("" on a relay's first one, which has none); None for anything else."""
    if block.get("type") != "tool_use" or block.get("name") != "Bash":
        return None
    m = NEXT.search((block.get("input") or {}).get("command", ""))
    return (m.group(1) or "") if m else None


def find_transcript(token, hint=None):
    """The transcript of the relay that is handing in batch `token`: the one that holds its Bash call
    `brain next <token>`. A transcript that does not carry the token is never taken for it, however new it is:
    None then, and the results come by `brain put`. hint: where this relay's last batch was found.
    TNR_TRANSCRIPT names the one file to look in (tests, or a relay that knows its own)."""
    if os.environ.get("TNR_TRANSCRIPT"):
        files = [os.environ["TNR_TRANSCRIPT"]]
    else:
        home = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
        files = [hint] if hint else []
        for path in glob.glob(os.path.join(home, "projects", "**", "*.jsonl"), recursive=True):
            try:
                if path != hint and time.time() - os.path.getmtime(path) <= RECENT:
                    files.append(path)
            except OSError:
                continue
    for path in files:
        try:
            if any(_next_token(c) == token for row in _rows(path, FIND_TAIL) for c in _blocks(row)):
                return path
        except OSError:
            continue
    return None


def _text(body, transcript):
    """The text of a tool result. One too large for the conversation is replaced by a notice naming the file that
    holds it; that file is read, but only from under the transcript's own folder."""
    text = body if isinstance(body, str) else "".join(
        x.get("text", "") for x in body or [] if isinstance(x, dict) and x.get("type") == "text")
    m = SAVED.match(text) or PERSISTED.match(text)
    if not m:
        return text
    path = os.path.realpath(m.group(m.lastindex))
    if not path.startswith(os.path.realpath(os.path.dirname(transcript)) + os.sep):
        raise ValueError("saved output outside the transcript folder")
    with open(path, encoding="utf8") as f:
        saved = f.read()
    if path.endswith(".json"):
        return "".join(b["text"] for b in json.loads(saved))
    return saved


def _stamp(row):
    try:
        return dt.datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).timestamp()
    except (KeyError, ValueError):
        return 0.0


def read_batch(path, token, expected, hooked=False):
    """(results, usage, strays) of the batch a relay hands in with `brain next <token>`.

    Only the calls the relay made between its previous `brain next` and this one are looked at, and each is
    matched once to a call the batch asked for (expected: [(endpoint, input), ...]). So a result is never taken
    from an earlier batch, however late it arrived, nor from a call nobody asked for; strays counts the calls
    that matched nothing. A call with no result is simply absent from the results.

    usage: {"in": prompt tokens the batch cost, "out": output tokens, "context": the size of the relay's last
    prompt; of "in", "cached": what was read from the prompt cache, and "written": what was written to it;
    "hooks": hooked}. A request is counted once however many transcript lines it spans. The plan's limits do
    not count the three kinds of prompt token alike (RUL-2026-11-13-156), so they are kept apart.

    hooked: the relay's hooks hand its results in (player/hook.py): its transcript is read for the usage only."""
    made, answers, cost = _span(path, token)
    out = []
    for ep, inp in [] if hooked else expected:
        hit = next((m for m in made if m[1] == ep and m[2] == inp), None)
        if hit is None:
            continue
        made.remove(hit)
        if hit[0] in answers:
            block, t = answers[hit[0]]
            out.append(_result(ep, inp, block, t, path))
    return out, _used(sorted(cost.values()), hooked), 0 if hooked else len(made)


def _used(reqs, hooked):
    """A batch's token use, from its requests: (when, prompt tokens, output, read from the cache, written to it)."""
    return {"in": sum(r[1] for r in reqs), "out": sum(r[2] for r in reqs), "context": reqs[-1][1] if reqs else 0,
            "cached": sum(r[3] for r in reqs), "written": sum(r[4] for r in reqs), "hooks": hooked}


def _span(path, token):
    """One batch's stretch of a transcript: (the connector calls made between the `brain next` before it and
    `brain next <token>`, every tool result by the id of its call, the token use of that stretch by request)."""
    made, mine, answers, requests, cost = [], None, {}, {}, {}
    for row in _rows(path):
        t = _stamp(row)
        _usage(row, t, requests)
        for c in _blocks(row):
            tok = _next_token(c)
            if tok is not None:                                   # a `brain next`: one batch ends, the next begins
                if tok == token and mine is None:
                    mine, cost = made, requests
                made, requests = [], {}
            elif c.get("type") == "tool_use" and c.get("name", "").endswith("callEndpoint"):
                inp = c.get("input") or {}
                made.append((c.get("id"), inp.get("endpointName"), inp.get("input") or {}))
            elif c.get("type") == "tool_result":
                answers[c.get("tool_use_id")] = (c, t)
    return list(mine or []), answers, cost


def _usage(row, t, requests):
    """Note one assistant message's token use under its request id."""
    msg = row.get("message") or {}
    u = msg.get("usage")
    if msg.get("role") != "assistant" or not isinstance(u, dict):
        return
    fresh, written, cached = (int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens",
                                                             "cache_read_input_tokens"))
    requests[row.get("requestId") or f"t{t}"] = (t, fresh + written + cached, int(u.get("output_tokens") or 0),
                                                 cached, written)


def _result(ep, inp, block, t, path):
    try:
        text = _text(block.get("content"), path)
    except (OSError, ValueError) as err:
        return Result(ep, inp, None, f"unreadable result: {err}", t)
    return from_text(ep, inp, text, t, block.get("is_error"))


def from_text(ep, inp, text, t, is_error=False):
    """A call's result text -> Result: the selected response, a refusal by the connector, or an error."""
    if "Too Many Requests" in text:
        return Result(ep, inp, None, RATE_LIMITED, t)
    if is_error or re.match(r"^\s*(Error|MCP error)\b", text):
        return Result(ep, inp, None, text.strip()[:300], t)
    try:
        return Result(ep, inp, json.loads(text), None, t)
    except ValueError:
        return Result(ep, inp, None, "unreadable result: not JSON", t)


# ---------------------------------------------------------------- what the relay is handed
def next_line(token=""):
    """The line that brings the relay back: `brain next`, with the token of the batch it will be handing in."""
    return json.dumps({"bash": f"cd {C.ROOT} && python3 -m player.brain next{' ' + token if token else ''}"},
                      separators=(",", ":"))


def lines(steps, stop=None, token="", echo=False, hooked=False):
    """A batch as the lines `brain next` prints: one JSON object per step, then the next `brain next`; or one
    STOP line when the relay should end. echo: no transcript can be read for this relay, so each call is
    followed by a `put` line that hands its result in (player/RELAY.md says how). hooked: the relay's hooks
    put each call in and take each result out (player/hook.py), so it is printed a stand-in for each call,
    which says only which call of which batch it is, and no wait: the hook spends those."""
    if stop:
        return [f"STOP {stop}"]
    out, n = [], 0
    if hooked:
        out = [json.dumps({"call": C.STAND_IN, "input": {"b": token, "n": k + 1}}, separators=(",", ":"))
               for k in range(sum("call" in s for s in steps))]
        steps = []
    for s in steps:
        if "call" in s:
            n += 1
            out.append(json.dumps({"call": s["call"], "input": s["input"], "select": s["select"]},
                                  separators=(",", ":")))
            if echo:
                out.append(json.dumps({"put": f"cd {C.ROOT} && python3 -m player.brain put {token} {n}"},
                                      separators=(",", ":")))
        elif s["wait"] > 0:
            out.append(json.dumps({"bash": f"python3 -c 'import time; time.sleep({s['wait']})'"}, separators=(",", ":")))
    out.append(next_line(token))
    return out


def seconds(steps):
    """How long a relay should take over a batch, for the watchdog."""
    return sum(s.get("wait", 0) for s in steps) + C.CALL_COST * sum(1 for s in steps if "call" in s) + 5.0


# ---------------------------------------------------------------- files between `brain next` and the brain
def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = f"{path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf8") as f:
        json.dump(obj, f, separators=(",", ":"))
    os.replace(tmp, path)


def read(path):
    try:
        with open(path, encoding="utf8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


OLD_REQUESTS = "req-*.json"
"""The name every version before the protocol number gave a request, and the only name a brain of those versions
looks for. This version never writes it."""


def request_path(live, seq, rid=None):
    """A request's file, under a name that only a brain of this protocol reads. A brain from before the update
    that is still running looks for OLD_REQUESTS and does not find it (review of 06358ca5: such a brain took
    this version's request, read it by its own rule as "the last relay is back", and let that relay's calls go;
    refusing its answer afterwards did not undo that). rid: the id `brain next` gives each request it makes, so
    two requests under one number (a relay and its replacement, a request and its retry) are never one file."""
    return os.path.join(live, "inbox", f"p{PROTOCOL}-req-{seq:08d}{'-' + rid if rid else ''}.json")


def is_request(path):
    """Whether a file has this protocol's name for a request."""
    return os.path.basename(path).startswith(f"p{PROTOCOL}-req-")


def batch_path(live, seq, rid=None):
    """The answer to the request with that number and id, and to no other."""
    return os.path.join(live, "outbox", f"batch-{seq:08d}{'-' + rid if rid else ''}.json")


def pending_requests(live):
    """What a brain of this protocol looks through: files under the old name, which are there only to be removed
    (brain.serve), then the requests under its own. A request under another protocol's name is not its to open."""
    inbox = os.path.join(live, "inbox")
    return (sorted(glob.glob(os.path.join(inbox, OLD_REQUESTS)))
            + sorted(glob.glob(os.path.join(inbox, f"p{PROTOCOL}-req-*.json"))))


def put_path(live, token, n):
    """Where the result of call n (from 1) of batch `token` is handed in, by `brain put` or by the relay's hook."""
    return os.path.join(live, "inbox", f"put-{token}-{n:03d}.json")


def put(live, token, n, result):
    write(put_path(live, token, n), list(result))


def pack(results):
    return [list(r) for r in results]


def unpack(rows):
    return [Result(*r) for r in rows or []]


# ---------------------------------------------------------------- tokens
def log_tokens(world, seq, usage, note):
    """One line per batch in live/tokens.jsonl, tagged with the fight turn it served (design 4.7: tokens per batch,
    per fight turn and per hour). Also keeps the relay's context size for rotation."""
    if not usage or not (usage.get("in") or usage.get("out")):
        return
    b = world["battle"] or {}
    relay = world["relay"]
    if relay.get("baseline_tokens") is None:
        relay["baseline_tokens"] = usage.get("context") or 0
    relay["context_tokens"] = usage.get("context") or relay.get("context_tokens", 0)
    world._append("tokens.jsonl", {"at": round(world.now, 1), "seq": seq, "in": usage.get("in", 0),
                                   "out": usage.get("out", 0), "context": usage.get("context", 0),
                                   "cached": usage.get("cached"), "written": usage.get("written"),
                                   "hooks": bool(usage.get("hooks")),             # a relay with hooks carried it
                                   "calls": len(relay.get("last_batch") or []),      # game calls the batch carried
                                   "battle": b.get("bid"), "round": b.get("round"), "note": note[:60]})


def tokens_summary(live, now, window=3600.0):
    """{"last_hour": tokens, "batches": n, "per_fight_turn": average} from live/tokens.jsonl. per_fight_turn is
    the tokens of the batches tagged with a battle and a round, over the number of such rounds; a fight's batches
    with no round yet (its opening read, its closing batch) are in the hour's total only."""
    total, n, turns = 0, 0, {}
    try:
        with open(os.path.join(live, "tokens.jsonl"), encoding="utf8") as f:
            for line in f:
                row = json.loads(line)
                if row["at"] < now - window:
                    continue
                cost = row["in"] + row["out"]
                total, n = total + cost, n + 1
                if row.get("battle") and row.get("round") is not None:
                    key = (row["battle"], row["round"])
                    turns[key] = turns.get(key, 0) + cost
    except (OSError, ValueError, KeyError):
        pass
    return {"last_hour": total, "batches": n,
            "per_fight_turn": round(sum(turns.values()) / len(turns)) if turns else None}


def should_rotate(world):
    """Rotate the relay by size, not by count (design 4.7), and never in a fight."""
    relay = world["relay"]
    ctx, base = relay.get("context_tokens") or 0, relay.get("baseline_tokens") or 0
    return not world.in_battle() and (ctx - base >= C.ROTATE_AFTER_TOKENS or ctx >= C.ROTATE_HARD_CAP)
