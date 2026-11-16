#!/usr/bin/env python3
"""Tune the planner against REAL opponents (director 2026-11-11: "We'll tune the lookahead against real enemies").

For every logged fight (newest first, up to --fights) and every turn of mine, postmortem.review rebuilds the exact
position, asks the planner (with the current settings) for its pick, and fires the pick, the move actually played and
the planner's alternatives in the game's engine, each answered by the turn the opponent ACTUALLY played next. Score:
mean (my HP - his HP) after the exchange for the planner's pick, and how often the pick is the best of the set.
Run it under different TNR_* settings and compare (each run is one line).

Usage: TNR_HEDGE=0.35 tune_real.py [--fights 8]
"""
import argparse
import os
import statistics
import sys
import contextlib
import io

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import opponents as OM  # noqa: E402
import postmortem  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fights", type=int, default=8)
    a = ap.parse_args()
    logs = [(b, p) for b, p, rows, m in OM.load_logs() if "observed" not in p]
    logs.sort(key=lambda x: -os.path.getmtime(x[1]))
    picks, played, best, n = [], [], 0, 0
    for bid, _ in logs[:a.fights]:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                out = postmortem.review(bid[:8], 6)
            except (Exception, SystemExit):  # noqa: BLE001
                continue
        for t in out["turns"]:
            if t.get("swing_pick") is None or t.get("swing_played") is None:
                continue
            n += 1
            picks.append(t["swing_pick"]); played.append(t["swing_played"])
            best += t["swing_pick"] >= t["swing_best"] - 1
    cfg = " ".join(f"{k}={v}" for k, v in sorted(os.environ.items()) if k.startswith("TNR_"))
    if n:
        print(f"[{cfg or 'defaults'}] {n} turns: planner pick {statistics.mean(picks):+.0f} HP/exchange vs played "
              f"{statistics.mean(played):+.0f}; pick is best-of-set {best / n:.0%}")


if __name__ == "__main__":
    main()
