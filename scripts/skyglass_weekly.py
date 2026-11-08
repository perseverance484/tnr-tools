#!/usr/bin/env python3
"""What this week's Skyglass routine should do (reads state/skyglass_schedule.json; no live requests).

    python3 scripts/skyglass_weekly.py release [--date YYYY-MM-DD]   # Friday run, 00:00 UTC Saturday
    python3 scripts/skyglass_weekly.py hide    [--date YYYY-MM-DD]   # Wednesday run, 00:00 UTC Thursday

--date is the America/Chicago date (default: today there; at 00:00 UTC Saturday it is still Friday in Chicago).
Prints one JSON object and exits 0 when there is work, 3 when there is nothing to do (STOP: no write).
"""
import json, os, sys
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stop(msg):
    print(json.dumps({"action": "stop", "reason": msg}))
    sys.exit(3)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("release", "hide"):
        sys.exit(__doc__)
    mode, args = sys.argv[1], sys.argv[2:]
    today = datetime.now(ZoneInfo("America/Chicago")).date()
    if "--date" in args:
        today = date.fromisoformat(args[args.index("--date") + 1])
    weeks = json.load(open(os.path.join(ROOT, "state/skyglass_schedule.json")))["weekends"]
    if mode == "release":
        if today.weekday() != 4:
            stop(f"{today} is not a Friday in Chicago")
        w = next((w for w in weeks if w["friday"] == today.isoformat()), None)
        if not w:
            stop(f"no page is scheduled for Friday {today}")
        if not (w["questId"] and w["published"]):
            stop(f"{w['name']} is scheduled for {today} but is not created and published (needs the director's go)")
        print(json.dumps({"action": "release", "page": w["page"], "name": w["name"], "questId": w["questId"],
                          "expect": {"hidden": False, "startsAt": w["startsAt"], "endsAt": w["endsAt"]},
                          "wreckBuild": f"python3 push/skyglass_wreck_window.gen.py weekend 515 --from {today}",
                          "wreckManifest": "push/515_skyglass_wreck_window.json",
                          "wreckExpiresAt": f"{w['endsAt']}T00:00:00.000Z"}))
    else:
        if today.weekday() != 2:
            stop(f"{today} is not a Wednesday in Chicago")
        friday = (today - timedelta(days=5)).isoformat()
        w = next((w for w in weeks if w["friday"] == friday), None)
        if not w or not w["questId"]:
            stop(f"no live page from the weekend of {friday} to hide")
        print(json.dumps({"action": "hide", "page": w["page"], "name": w["name"], "questId": w["questId"],
                          "build": f"python3 push/skyglass_journal.gen.py hide --page {w['page']} --num {w['hideNum']} --id {w['questId']}",
                          "manifest": f"push/{w['hideNum']}_skyglass_journal_page{w['page']}_hide.json"}))


if __name__ == "__main__":
    main()
