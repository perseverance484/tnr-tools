"""The hands: how batches reach a relay agent and how results come back (design 4.1, 4.7).

The relay is a small model in a loop: run `brain next`, make the calls it prints, exactly and in order, run
`brain next` again. It holds no state and decides nothing, so any relay can replace any other.

- Results are read from the relay's own transcript (Claude Code records every call and its exact result there), so
  the relay spends no tokens echoing them. `brain put` is the fallback when a transcript cannot be read.
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

NEXT = re.compile(r"player\.brain\s+next|player/brain\.py\s+next")
SAVED = re.compile(r"^Error: result \(([\d,]+) characters[^)]*\) exceeds maximum allowed tokens\. "
                   r"Output has been saved to (\S+?\.txt)\.")
PERSISTED = re.compile(r"^<persisted-output>\s*\nOutput too large \([^)]*\)\. Full output saved to: (\S+?\.json)\s*\n")
TAIL = 4_000_000          # bytes of transcript read back: one batch of full battle reads fits many times over


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


def find_transcript():
    """The transcript of the relay running this `brain next`: among recently written transcripts, the one whose
    newest call is a Bash `brain next`. TNR_TRANSCRIPT names it outright (tests, or a relay that knows its own)."""
    if os.environ.get("TNR_TRANSCRIPT"):
        return os.environ["TNR_TRANSCRIPT"]
    home = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    files = sorted(glob.glob(os.path.join(home, "projects", "**", "*.jsonl"), recursive=True),
                   key=os.path.getmtime, reverse=True)
    now = time.time()
    for path in files[:8]:
        if now - os.path.getmtime(path) > 120:
            break
        last = None
        for row in _rows(path, 60_000):
            for c in _blocks(row):
                if c.get("type") == "tool_use":
                    last = c
        if last and last.get("name") == "Bash" and NEXT.search((last.get("input") or {}).get("command", "")):
            return path
    return files[0] if files else None


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


def read_results(path, since):
    """([Result, ...] in the order they came back, usage) for everything the relay did after `since` (epoch s).

    usage: {"in": prompt tokens the batch cost, "out": output tokens, "context": the size of the relay's last
    prompt}. A request is counted once however many transcript lines it spans."""
    asked, out, requests = {}, [], {}
    for row in _rows(path):
        t = _stamp(row)
        if t > since:
            _usage(row, t, requests)
        for c in _blocks(row):
            if c.get("type") == "tool_use" and c.get("name", "").endswith("callEndpoint"):
                inp = c.get("input") or {}
                asked[c["id"]] = (inp.get("endpointName"), inp.get("input") or {})
            elif c.get("type") == "tool_result" and c.get("tool_use_id") in asked and t > since:
                out.append(_result(*asked[c["tool_use_id"]], c, t, path))
    reqs = sorted(requests.values())
    return out, {"in": sum(r[1] for r in reqs), "out": sum(r[2] for r in reqs), "context": reqs[-1][1] if reqs else 0}


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
    if "Too Many Requests" in text:
        return Result(ep, inp, None, RATE_LIMITED, t)
    if block.get("is_error") or re.match(r"^\s*(Error|MCP error)\b", text):
        return Result(ep, inp, None, text.strip()[:300], t)
    try:
        return Result(ep, inp, json.loads(text), None, t)
    except ValueError:
        return Result(ep, inp, None, "unreadable result: not JSON", t)


# ---------------------------------------------------------------- what the relay is handed
def lines(steps, stop=None):
    """A batch as the lines `brain next` prints: one JSON object per step, then the next `brain next`; or one
    STOP line when the relay should end."""
    if stop:
        return [f"STOP {stop}"]
    out = []
    for s in steps:
        if "call" in s:
            out.append(json.dumps({"call": s["call"], "input": s["input"], "select": s["select"]},
                                  separators=(",", ":")))
        elif s["wait"] > 0:
            out.append(json.dumps({"bash": f"python3 -c 'import time; time.sleep({s['wait']})'"}, separators=(",", ":")))
    out.append(json.dumps({"bash": f"cd {C.ROOT} && python3 -m player.brain next"}, separators=(",", ":")))
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
                                   "battle": b.get("bid"), "round": b.get("round"), "note": note[:60]})


def tokens_summary(live, now, window=3600.0):
    """{"last_hour": tokens, "batches": n, "per_fight_turn": average} from live/tokens.jsonl."""
    total, n, turns = 0, 0, {}
    try:
        with open(os.path.join(live, "tokens.jsonl"), encoding="utf8") as f:
            for line in f:
                row = json.loads(line)
                if row["at"] < now - window:
                    continue
                cost = row["in"] + row["out"]
                total, n = total + cost, n + 1
                if row.get("battle"):
                    key = (row["battle"], row.get("round"))
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
