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
- Requests and batches are files under live/inbox and live/outbox, written whole and renamed into place.
"""
import datetime as dt
import glob
import json
import os
import re
import time

from . import config as C
from .world import RATE_LIMITED, Result

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


def read_batch(path, token, expected):
    """(results, usage, strays) of the batch a relay hands in with `brain next <token>`.

    Only the calls the relay made between its previous `brain next` and this one are looked at, and each is
    matched once to a call the batch asked for (expected: [(endpoint, input), ...]). So a result is never taken
    from an earlier batch, however late it arrived, nor from a call nobody asked for; strays counts the calls
    that matched nothing. A call with no result is simply absent from the results.

    usage: {"in": prompt tokens the batch cost, "out": output tokens, "context": the size of the relay's last
    prompt}. A request is counted once however many transcript lines it spans."""
    made, answers, cost = _span(path, token)
    out = []
    for ep, inp in expected:
        hit = next((m for m in made if m[1] == ep and m[2] == inp), None)
        if hit is None:
            continue
        made.remove(hit)
        if hit[0] in answers:
            block, t = answers[hit[0]]
            out.append(_result(ep, inp, block, t, path))
    reqs = sorted(cost.values())
    usage = {"in": sum(r[1] for r in reqs), "out": sum(r[2] for r in reqs), "context": reqs[-1][1] if reqs else 0}
    return out, usage, len(made)


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
    size = sum(int(u.get(k) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    requests[row.get("requestId") or f"t{t}"] = (t, size, int(u.get("output_tokens") or 0))


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


def lines(steps, stop=None, token="", echo=False):
    """A batch as the lines `brain next` prints: one JSON object per step, then the next `brain next`; or one
    STOP line when the relay should end. echo: no transcript can be read for this relay, so each call is
    followed by a `put` line that hands its result in (player/RELAY.md says how)."""
    if stop:
        return [f"STOP {stop}"]
    out, n = [], 0
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


def request_path(live, seq):
    return os.path.join(live, "inbox", f"req-{seq:08d}.json")


def batch_path(live, seq):
    return os.path.join(live, "outbox", f"batch-{seq:08d}.json")


def pending_requests(live):
    return sorted(glob.glob(os.path.join(live, "inbox", "req-*.json")))


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
