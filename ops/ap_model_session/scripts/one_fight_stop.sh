#!/bin/bash
# Short test run: after the FIRST fight_end event in live/events.jsonl that is newer than START_EPOCH,
# run `python3 -m player.brain set end_session=true` once (orderly shutdown: home, sleep, lock released by the brain).
# Usage (background, from the repo root): one_fight_stop.sh <repo_root> <start_epoch>
REPO="$1"; START="$2"; EV="$REPO/state/player/dauntless/live/events.jsonl"; NOTES=${AP_KIT:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$REPO" || exit 2
while true; do
  if [ -f "$EV" ] && python3 - "$EV" "$START" <<'PY'
import json, sys
from datetime import datetime
def ts(v):
    if isinstance(v, (int, float)): return float(v)
    try: return datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
    except ValueError: return 0.0
ev, start = sys.argv[1], float(sys.argv[2])
for line in open(ev, encoding="utf8"):
    try: e = json.loads(line)
    except ValueError: continue
    if e.get("kind") == "fight_end":
        if ts(e.get("at")) >= start:
            print(json.dumps(e)); sys.exit(0)
sys.exit(1)
PY
  then
    env -u TNR_PLAYER_LIVE python3 -m player.brain set end_session=true >> "$NOTES/one_fight_stop.log" 2>&1
    echo "end_session set after first fight $(date -u +%FT%TZ)" >> "$NOTES/one_fight_stop.log"; exit 0
  fi
  sleep 5
done
