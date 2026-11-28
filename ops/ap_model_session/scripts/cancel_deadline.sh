#!/bin/bash
# Cancel the timer after an early clean finish (kills its process group).
P=$(cat ${AP_KIT:-$(cd "$(dirname "$0")/.." && pwd)}/deadline_timer.pid 2>/dev/null)
[ -n "$P" ] && { kill -- -"$P" 2>/dev/null || kill "$P" 2>/dev/null; }; echo cancelled
