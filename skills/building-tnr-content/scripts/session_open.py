#!/usr/bin/env python3
"""session_open.py - collapse the start ritual into one command.

Reads state/digest.json (the single session-state source), prints the state
line, in-progress item, rulings_open and next; re-runs the guard trio
(lawmap; validate on the in-progress file when set; --parity vs the newest
inbox bundle) so nothing in the handoff is trusted unverified; seeds the
token ledger with the bytes this ritual itself read. Output stays under
~500 tokens by design - the digest is the entry point, not the activity log.

Usage
  python3 session_open.py            # ritual
  python3 session_open.py --read P   # log an additional heavy read into the
                                     # ledger mid-session (repeatable)
Stdlib only. Run after clone + git identity; exits 1 if any guard is red.
"""
import glob
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
DIGEST = os.path.join(ROOT, "state", "digest.json")
sys.path.insert(0, HERE)
from session_close import run_guards  # noqa: E402


def ledger_add(d, path):
    full = os.path.join(ROOT, path)
    if os.path.exists(full):
        d.setdefault("token_ledger", []).append(
            {"path": path, "bytes": os.path.getsize(full),
             "at": time.strftime("%H:%MZ", time.gmtime())})


def main():
    if not os.path.exists(DIGEST):
        print("no digest at state/digest.json - no clone means no state; "
              "clone first, or this repo predates WO-05")
        return 1
    d = json.load(open(DIGEST, encoding="utf-8"))

    if "--read" in sys.argv:
        p = sys.argv[sys.argv.index("--read") + 1]
        ledger_add(d, p)
        json.dump(d, open(DIGEST, "w", encoding="utf-8"), indent=2,
                  ensure_ascii=False)
        print("ledger + %s" % p)
        return 0

    print("STATE  " + str(d.get("state_line", "?")))
    ip = d.get("in_progress") or {}
    if ip:
        print("WORK   " + "; ".join("%s: %s" % kv for kv in ip.items()))
    for r in (d.get("rulings_open") or [])[:8]:
        print("RULING " + str(r))
    print("NEXT   " + str(d.get("next", "?")))

    bad = run_guards(ROOT, d)
    for line in d.get("verified_at_close") or []:
        print("GUARD  " + line)

    d["token_ledger"] = []                      # fresh ledger per session
    for p in ("state/digest.json", "state/active-context.md",
              "state/status.json", "docs/00_INDEX.md"):
        ledger_add(d, p)
    bundles = sorted(glob.glob(os.path.join(ROOT, "harvests", "inbox", "*.json")))
    if bundles:
        ledger_add(d, os.path.relpath(bundles[-1], ROOT))
        print("INBOX  newest bundle: %s (harvest.py verify it if unread)"
              % os.path.basename(bundles[-1]))
    json.dump(d, open(DIGEST, "w", encoding="utf-8"), indent=2,
              ensure_ascii=False)

    if bad:
        print("GUARDS RED (%s) - fix before trusting anything" % ", ".join(bad))
        return 1
    print("guards green; ledger seeded (%d reads)" % len(d["token_ledger"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
