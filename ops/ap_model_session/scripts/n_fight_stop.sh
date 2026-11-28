#!/bin/bash
# After the Nth fight_end event (default 10) in live/events.jsonl that is newer than START_EPOCH,
# run `python3 -m player.brain set end_session=true` once (orderly shutdown: home, sleep, lock released by the brain).
# Usage (background, from the repo root): n_fight_stop.sh <repo_root> <start_epoch> [n=10]
REPO="$1"; START="$2"; N="${3:-10}"; EV="$REPO/state/player/dauntless/live/events.jsonl"; NOTES=${AP_KIT:-$(cd "$(dirname "$0")/.." && pwd)}
cd "$REPO" || exit 2
while true; do
  if [ -f "$EV" ] && python3 - "$EV" "$START" "$N" <<'PY'
import json, sys
from datetime import datetime
def ts(v):
    if isinstance(v, (int, float)): return float(v)
    try: return datetime.fromisoformat(str(v).replace("Z", "+00:00")).timestamp()
    except ValueError: return 0.0
ev, start, n = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]); seen = 0
for line in open(ev, encoding="utf8"):
    try: e = json.loads(line)
    except ValueError: continue
    if e.get("kind") == "fight_end":
        if ts(e.get("at")) >= start:
            seen += 1
            if seen >= n: print(json.dumps(e)); sys.exit(0)
sys.exit(1)
PY
  then
    env -u TNR_PLAYER_LIVE python3 -m player.brain set end_session=true >> "$NOTES/n_fight_stop.log" 2>&1
    echo "end_session set after fight $N $(date -u +%FT%TZ)" >> "$NOTES/n_fight_stop.log"; exit 0
  fi
  sleep 5
done
