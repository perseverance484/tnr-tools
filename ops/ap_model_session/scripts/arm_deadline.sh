#!/bin/bash
# Arm the in-container deadline timer. Run ONCE at launch.
# Usage: arm_deadline.sh <repo_root> <deadline_epoch_seconds>
# Fires: python3 -m player.brain set end_session=true (idempotent) from <repo_root>, real live folder.
REPO="$1"; DEADLINE="$2"; NOTES=${AP_KIT:-$(cd "$(dirname "$0")/.." && pwd)}
[ -d "$REPO/player" ] || { echo "no player/ under $REPO" >&2; exit 2; }
NOW=$(date -u +%s); WAIT=$(( DEADLINE - NOW )); [ $WAIT -gt 0 ] || WAIT=1
setsid nohup bash -c "sleep $WAIT; cd '$REPO' && env -u TNR_PLAYER_LIVE python3 -m player.brain set end_session=true >> '$NOTES/deadline_timer.log' 2>&1; echo \"fired \$(date -u +%FT%TZ)\" >> '$NOTES/deadline_timer.log'" >/dev/null 2>&1 < /dev/null &
echo $! > "$NOTES/deadline_timer.pid"
echo "armed pid=$(cat $NOTES/deadline_timer.pid) wait=${WAIT}s deadline=$(date -u -d @$DEADLINE +%FT%TZ)"
