#!/bin/bash
# Prints the timer process, or DEAD.
P=$(cat ${AP_KIT:-$(cd "$(dirname "$0")/.." && pwd)}/deadline_timer.pid 2>/dev/null)
if [ -n "$P" ] && kill -0 "$P" 2>/dev/null; then ps -o pid,etime,args -p "$P" --no-headers; else echo DEAD; fi
