#!/usr/bin/env python3
"""Print current session state, rerun guards, and seed the read ledger."""

import argparse
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


def ledger_add(digest, path):
    full_path = os.path.join(ROOT, path)
    if os.path.exists(full_path):
        digest.setdefault("token_ledger", []).append(
            {
                "path": path,
                "bytes": os.path.getsize(full_path),
                "at": time.strftime("%H:%MZ", time.gmtime()),
            }
        )


def save(digest):
    with open(DIGEST, "w", encoding="utf-8") as handle:
        json.dump(digest, handle, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--read", metavar="PATH")
    args = parser.parse_args()

    if not os.path.exists(DIGEST):
        print("no digest at state/digest.json - clone first, or this repo predates WO-05")
        return 1

    with open(DIGEST, encoding="utf-8") as handle:
        digest = json.load(handle)

    if args.read:
        ledger_add(digest, args.read)
        save(digest)
        print("ledger + " + args.read)
        return 0

    print("STATE  " + str(digest.get("state_line", "?")))
    in_progress = digest.get("in_progress") or {}
    if in_progress:
        print("WORK   " + "; ".join("%s: %s" % item for item in in_progress.items()))
    for ruling in (digest.get("rulings_open") or [])[:8]:
        print("RULING " + str(ruling))
    print("NEXT   " + str(digest.get("next", "?")))

    failures = run_guards(ROOT, digest)
    for line in digest.get("verified_at_close") or []:
        print("GUARD  " + line)

    digest["token_ledger"] = []
    for path in (
        "state/digest.json",
        "state/active-context.md",
        "state/status.json",
        "docs/00_INDEX.md",
    ):
        ledger_add(digest, path)

    bundles = sorted(glob.glob(os.path.join(ROOT, "harvests", "inbox", "*.json")))
    if bundles:
        latest = bundles[-1]
        ledger_add(digest, os.path.relpath(latest, ROOT))
        print("INBOX  newest bundle: %s (harvest.py verify it if unread)" % os.path.basename(latest))

    save(digest)
    if failures:
        print("GUARDS RED (%s) - fix before trusting anything" % ", ".join(failures))
        return 1
    print("guards green; ledger seeded (%d reads)" % len(digest["token_ledger"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
