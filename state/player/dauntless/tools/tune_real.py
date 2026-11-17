#!/usr/bin/env python3
"""Tune the planner against REAL opponents (director 2026-11-11: "We'll tune the lookahead against real enemies").

For every logged fight (newest first, up to --fights) and every turn of mine, postmortem.review rebuilds the exact
position, asks the planner (with the current settings) for its pick, and fires the pick, the move actually played and
the planner's alternatives in the game's engine, each answered by the turn the opponent ACTUALLY played next. Score:
mean (my HP - his HP) after the exchange for the planner's pick, and how often the pick is the best of the set.
Run it under different TNR_* settings and compare (each run is one line).

--depth N plays each line against N of his actual turns, with my turns in between as I actually played them, and
prints a second line for where things stood after his last one. One exchange gives a buff no credit for the rounds
after it; the deeper figure does, and leans to what was played, whose follow-up it is (postmortem.DEPTH).

Usage: TNR_HEDGE=0.35 tune_real.py [--fights 8] [--depth 3]
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
    ap.add_argument("--depth", type=int, default=1, help="how many of his actual turns each line is played against "
                    "(postmortem.DEPTH): more than one also prints where things stood after his last one")
    a = ap.parse_args()
    postmortem.DEPTH = a.depth
    logs = [(b, p) for b, p, rows, m in OM.load_logs() if "observed" not in p]
    logs.sort(key=lambda x: -os.path.getmtime(x[1]))
    picks, played, best, n = [], [], 0, 0
    deep = []                      # (the pick, what was played, the best of the set) after his last scripted turn
    for bid, _ in logs[:a.fights]:
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                out = postmortem.review(bid[:8], 6)
            except (Exception, SystemExit):  # noqa: BLE001
                continue
        for t in out["turns"]:
            d = t.get("deep") or {}
            if d.get("pick") is not None and d.get("played") is not None and d.get("his_turns", 0) >= a.depth:
                deep.append((d["pick"], d["played"], d["best"]))
            if t.get("swing_pick") is None or t.get("swing_played") is None:
                continue
            n += 1
            picks.append(t["swing_pick"]); played.append(t["swing_played"])
            best += t["swing_pick"] >= t["swing_best"] - 1
    cfg = " ".join(f"{k}={v}" for k, v in sorted(os.environ.items()) if k.startswith("TNR_"))
    if n:
        print(f"[{cfg or 'defaults'}] {n} turns: planner pick {statistics.mean(picks):+.0f} HP/exchange vs played "
              f"{statistics.mean(played):+.0f}; pick is best-of-set {best / n:.0%}")
    if deep:
        print(f"  after {a.depth} of his actual turns, mine in between as played ({len(deep)} turns): pick "
              f"{statistics.mean(d[0] for d in deep):+.0f} vs played {statistics.mean(d[1] for d in deep):+.0f}; "
              f"pick is best-of-set {sum(d[0] >= d[2] - 1 for d in deep) / len(deep):.0%}")


if __name__ == "__main__":
    main()
