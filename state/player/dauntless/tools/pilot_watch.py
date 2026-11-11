#!/usr/bin/env python3
"""Supervisor view: the status lines a running pilot agent has printed (newest pilot transcript), nothing else.
Usage: pilot_watch.py [N]   (last N lines, default 12)"""
import glob, json, os, sys
files = glob.glob("/root/.claude/projects/**/subagents/*.jsonl", recursive=True)
path = max(files, key=os.path.getmtime)
pending, lines = set(), []
for raw in open(path):
    try:
        d = json.loads(raw)
    except ValueError:
        continue
    for c in (d.get("message") or {}).get("content") or [] if isinstance((d.get("message") or {}).get("content"), list) else []:
        if c.get("type") == "tool_use" and "pilot.py" in (c.get("input") or {}).get("command", ""):
            pending.add(c["id"])
        elif c.get("type") == "tool_result" and c.get("tool_use_id") in pending:
            body = c.get("content")
            text = body if isinstance(body, str) else "".join(x.get("text", "") for x in body or [] if isinstance(x, dict))
            lines.append(d.get("timestamp", "")[11:19] + " " + (text.splitlines() or [""])[0])
print("\n".join(lines[-int(sys.argv[1]) if len(sys.argv) > 1 else -12:]))
