#!/usr/bin/env python3
"""Refresh the record catalog from the public game catalog (director, 2026-11-11: "Update the catalogs jutsu records
from the live source"; the public read surface already serves these to any visitor).

Unauthenticated, read-only tRPC GETs on https://www.theninja-rpg.com (no cookies, no credentials, no mutations):
  jutsu.getAll, item.getAll and bloodline.getAll, each visible + hidden (AI and pet jutsu included), every page.
Writes one capture to harvests/inbox/tnr_results_<ms>.json (same shape as the 2026-10-23 public-read capture), then
rebuilds kit/catalog.json and kit/bloodlines.json with build_catalog.py. Run between fights, never during one.
Usage: fetch_catalog.py [--dry-run]
"""
import datetime
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
BASE = "https://www.theninja-rpg.com/api/trpc/"
UA = {"User-Agent": "tnr-tools catalog refresh (read-only)", "Accept": "application/json"}


def get(proc, inp):
    url = BASE + proc + "?batch=1&input=" + urllib.parse.quote(json.dumps({"0": {"json": inp}}))
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90) as r:
                return json.loads(r.read())[0]["result"]["data"]["json"]
        except Exception as err:  # noqa: BLE001
            if attempt == 2:
                raise
            print(f"  retry {proc} after {err!r}"[:160], file=sys.stderr)
            time.sleep(3)


def pages(proc, base, limit):
    rows, cursor, out = [], 0, []
    while True:
        t = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        d = get(proc, {**base, "limit": limit, "cursor": cursor})
        data = d.get("data", [])
        rows += data
        out.append({"phase": "before", "proc": proc, "input": {**base, "limit": limit, "cursor": cursor}, "at": t,
                    "ok": True, "rows": len(data), "error": None, "data": d})
        print(f"  {proc} cursor {cursor}: {len(data)}")
        cursor = d.get("nextCursor")
        if cursor is None or not data:
            return rows, out
        time.sleep(0.5)


def main():
    caps, counts = [], {}
    for name, proc, base, limit in [
        ("jutsu (visible)", "jutsu.getAll", {"hidden": False}, 1000),
        ("jutsu (hidden)", "jutsu.getAll", {"hidden": True}, 1000),
        ("items (visible)", "item.getAll", {"minCost": 0, "minRepsCost": 0, "minSeichiSilverCost": 0}, 500),
        ("items (hidden)", "item.getAll", {"minCost": 0, "minRepsCost": 0, "minSeichiSilverCost": 0, "hidden": True}, 500),
        ("bloodlines (visible)", "bloodline.getAll", {}, 500),
        ("bloodlines (hidden)", "bloodline.getAll", {"hidden": True}, 500),
    ]:
        try:
            rows, out = pages(proc, base, limit)
        except Exception as err:  # noqa: BLE001
            print(f"{name}: FAILED {err!r}"[:200])
            continue
        counts[name] = len(rows)
        caps += out
    now = datetime.datetime.now(datetime.timezone.utc)
    doc = {"builder": "public-read (Claude Code; director-approved catalog refresh 2026-11-11)",
           "at": now.isoformat(timespec="milliseconds").replace("+00:00", "Z"), "cfg": "public-read", "state": "DONE",
           "outcome": "success" if counts else "failed",
           "_note": "Unauthenticated public reads of jutsu.getAll (visible and hidden), item.getAll and bloodline.getAll "
                    "for the offline PvP harness catalog. No credentials, zero mutations. Counts: " + json.dumps(counts),
           "captures": caps}
    print("counts:", counts)
    if "--dry-run" in sys.argv or not counts:
        return
    path = os.path.join(REPO, "harvests/inbox", f"tnr_results_{int(now.timestamp() * 1000)}.json")
    json.dump(doc, open(path, "w"), separators=(",", ":"))
    print("wrote", os.path.relpath(path, REPO), f"{os.path.getsize(path) // 1024} KB")
    subprocess.run([sys.executable, os.path.join(REPO, "harness/pvp_turn/tools/build_catalog.py")], check=True)


if __name__ == "__main__":
    main()
