"""What one run of the proof shows (proof.py's OUT folder), from what was written down during it.

    python3 docs/reviews/evidence/ai_player_hook_relay/proof_read.py OUT
    python3 docs/reviews/evidence/ai_player_hook_relay/proof_read.py --table OUT [OUT ...]

--table: one line a run. "plan" is the count the estimate uses (estimate.py), in fresh input tokens of the
relay's model: 0.1 x read from the cache + 1.25 x written to it + fresh input + 5 x output, over the whole
session, from the use Claude Code reports at its end.
"""
import json
import os
import re
import sys


def rows(path):
    try:
        with open(path, encoding="utf8") as f:
            return [json.loads(x) for x in f if x.strip().startswith("{")]
    except OSError:
        return []


def main(out):
    live = os.path.join(out, "live")
    stream, game = rows(os.path.join(out, "stream.jsonl")), rows(os.path.join(out, "game.jsonl"))
    hooks, tokens = rows(os.path.join(live, "hook", "log.jsonl")), rows(os.path.join(live, "tokens.jsonl"))
    init = next((e for e in stream if e.get("type") == "system" and e.get("subtype") == "init"), {})
    print("session:", {"model": init.get("model"), "tools": init.get("tools"), "mcp": init.get("mcp_servers"),
                       "permission mode": init.get("permissionMode")})
    # ---- what the model sent, message by message (the stream has one row for each part of a message)
    messages, results, at, use = [], {}, {}, {}
    for e in stream:
        if e.get("type") == "assistant":
            mid = e["message"].get("id")
            if mid not in at:
                at[mid] = len(messages)
                messages.append([])
            use[mid] = e["message"].get("usage") or use.get(mid) or {}
            messages[at[mid]] += [c for c in e["message"].get("content", []) if c.get("type") == "tool_use"]
        elif e.get("type") == "user" and isinstance(e["message"].get("content"), list):
            for c in e["message"]["content"]:
                if c.get("type") == "tool_result":
                    body = c.get("content")
                    text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
                    results[c.get("tool_use_id")] = (bool(c.get("is_error")), text)
    print("requests of the model:", len(messages), "| read from the cache, written to it, at each:",
          [(u.get("cache_read_input_tokens"), u.get("cache_creation_input_tokens")) for u in use.values()])
    messages = [m for m in messages if m]
    shapes = {}
    for uses in messages:
        shape = " + ".join("next" if u["name"] == "Bash" else "call" for u in uses)
        shapes[shape] = shapes.get(shape, 0) + 1
    print("tool calls in one message of the model:", shapes)
    calls = [u for uses in messages for u in uses if u["name"] != "Bash"]
    other = [u["input"] for u in calls if set(u["input"]) != {"endpointName", "input"} or u["input"].get("endpointName") != "player.relay"]
    shown = {}
    for u in calls:
        err, text = results.get(u["id"], (None, "no result in the stream"))
        key = "ok" if text.strip() == "ok" and not err else ("error: " if err else "other: ") + text.strip()[:160]
        shown[key] = shown.get(key, 0) + 1
    print("connector calls the model wrote:", len(calls), "| not a stand-in:", other[:3], "| what it was shown:", shown)
    bash = [u["input"].get("command") for uses in messages for u in uses if u["name"] == "Bash"]
    print("commands the model ran:", len(bash), "| not `brain next`:", [c for c in bash if "player.brain next" not in c][:3])
    # ---- what the hooks did
    by = {}
    for h in hooks:
        key = (h["hook"], "refused: " + h["refused"][:70] if h.get("refused") else "passed")
        by[key] = by.get(key, 0) + 1
    print("hooks:", {f"{a} {b}": n for (a, b), n in sorted(by.items())})
    took = {}
    with open(os.path.join(out, "debug.log"), encoding="utf8", errors="replace") as f:
        for m in re.finditer(r"Hooks: (\w+):(\S+) \[.*\] finished with status (\d+) \((\d+)ms\)", f.read()):
            took.setdefault(f"{m.group(1)} {m.group(2)} exit {m.group(3)}", []).append(int(m.group(4)))
    print("how long Claude Code says each hook ran, ms:", {k: {"n": len(v), "least": min(v), "middle": sorted(v)[len(v) // 2],
                                                               "most": max(v)} for k, v in sorted(took.items())})
    # ---- what reached the stand-in
    came = [g for g in game if g.get("at") == "came"]
    done = [g for g in game if g.get("at") == "answered"]
    print("the stand-in:", {"connected": sum(g.get("at") == "connected" for g in game), "calls": len(came), "answered": len(done),
                            "failed": sum(bool(g.get("failed")) for g in done)})
    kinds = {}
    for g in came:
        kinds[g["endpoint"]] = kinds.get(g["endpoint"], 0) + 1
    print("endpoints:", kinds)
    spans = sorted((g["came"], g["answered"]) for g in done)
    together = sum(1 for a, b in zip(spans, spans[1:]) if b[0] < a[1])
    gaps = [round(b[0] - a[1], 2) for a, b in zip(spans, spans[1:])]
    print("two calls out at once:", together, "times | shortest time from one answer to the next call:", min(gaps) if gaps else None, "s")
    # ---- what the brain got and what it cost
    print("batches in the token log:", len(tokens))
    for t in tokens:
        print("  ", {k: t.get(k) for k in ("seq", "in", "cached", "written", "out", "context", "hooks", "note")})
    events = rows(os.path.join(live, "events.jsonl"))
    kinds = {}
    for e in events:
        kinds[e.get("kind")] = kinds.get(e.get("kind"), 0) + 1
    print("the brain's events:", kinds)
    for e in events:
        if e.get("kind") in ("finding", "error", "stall"):
            print("  ", e.get("kind"), "|", str(e.get("text"))[:200])
    end = next((e for e in stream if e.get("type") == "result"), {})
    print("the session ended:", {k: end.get(k) for k in ("subtype", "is_error", "num_turns", "duration_ms", "total_cost_usd")})
    print("  its last words:", str(end.get("result"))[:300])
    print("  its use, all requests:", {k: (end.get("usage") or {}).get(k) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")})
    kept = sorted(os.path.relpath(os.path.join(r, f), live) for r, _, fs in os.walk(os.path.join(live, "hook")) for f in fs)
    print("left in live/hook:", kept, "| in the inbox:", sorted(os.listdir(os.path.join(live, "inbox"))) if os.path.isdir(os.path.join(live, "inbox")) else None)
    client = (rows(os.path.join(live, "client.json")) or [{}])[0]
    print("client.json:", {k: client.get(k) for k in ("hooks", "token", "held", "gone", "ended", "seen")})


def line(out):
    live = os.path.join(out, "live")
    stream, game = rows(os.path.join(out, "stream.jsonl")), rows(os.path.join(out, "game.jsonl"))
    hooks, tokens = rows(os.path.join(live, "hook", "log.jsonl")), rows(os.path.join(live, "tokens.jsonl"))
    messages, shown = {}, {}
    for e in stream:
        if e.get("type") == "assistant":
            messages.setdefault(e["message"].get("id"), []).extend(
                c for c in e["message"].get("content", []) if c.get("type") in ("tool_use", "thinking", "text"))
        elif e.get("type") == "user" and isinstance(e["message"].get("content"), list):
            for c in e["message"]["content"]:
                if c.get("type") == "tool_result":
                    body = c.get("content")
                    text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
                    shown[c.get("tool_use_id")] = "ok" if text.strip() == "ok" and not c.get("is_error") else "other"
    uses = [[c for c in m if c["type"] == "tool_use"] for m in messages.values()]
    calls = [u for m in uses for u in m if u["name"] != "Bash"]
    end = next((e for e in stream if e.get("type") == "result"), {})
    use = end.get("usage") or {}
    plan = (0.1 * use.get("cache_read_input_tokens", 0) + 1.25 * use.get("cache_creation_input_tokens", 0)
            + use.get("input_tokens", 0) + 5 * use.get("output_tokens", 0)) if use else None
    return {"run": os.path.basename(out), "requests": len(messages),
            "calls and next in one message": sum(1 for m in uses if len({u["name"] for u in m}) == 2),
            "thinking": sum(1 for m in messages.values() for c in m if c["type"] == "thinking"),
            "text": sum(1 for m in messages.values() for c in m if c["type"] == "text"),
            "calls": len(calls), "not a stand-in": sum(1 for u in calls if u["input"].get("endpointName") != "player.relay"),
            "shown ok": sum(1 for u in calls if shown.get(u["id"]) == "ok"),
            "hooks": "/".join(str(sum(1 for h in hooks if h["hook"] == k and not h.get("refused"))) for k in ("bash", "pre", "post", "fail")),
            "refused": sum(1 for h in hooks if h.get("refused")),
            "game": sum(1 for g in game if g.get("at") == "came"), "batches": len(tokens),
            "read": use.get("cache_read_input_tokens"), "written": use.get("cache_creation_input_tokens"),
            "output": use.get("output_tokens"), "plan": round(plan) if plan else None,
            "a batch": round(plan / len(tokens)) if plan and tokens else None,
            "context at the end": tokens[-1].get("context") if tokens else None, "end": str(end.get("result"))[:60]}


if __name__ == "__main__":
    if sys.argv[1] == "--table":
        for out in sys.argv[2:]:
            print(json.dumps(line(os.path.abspath(out))))
    else:
        main(os.path.abspath(sys.argv[1]))
