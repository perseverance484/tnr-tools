#!/usr/bin/env python3
"""Plan the opening turn of a hunting fight (odd-q hex grid, 12x10 hunting map).

Usage: hunt_plan.py ME_COL ME_ROW EN_COL EN_ROW [--jab-range 4] [--leap 5]
Prints the exact performAction calls to make, e.g.
  JAB 8 3                      (enemy already within Jab range: one call)
  INVIG 7 3 | JAB 8 3          (Chakra Invigoration to (7,3), then Jab)

Rules (verified 2026-11-10): Stunning Jab range 4; Chakra Invigoration leaps up to 5.
Picks the landing hex within leap range that is closest to the enemy (ties: closest to
me), never the enemy's own hex. Deterministic, stdlib only.
"""
import sys


def cube(col, row):
    x = col
    z = row - (col - (col & 1)) // 2
    return x, -x - z, z


def dist(a, b):
    ax, ay, az = cube(*a)
    bx, by, bz = cube(*b)
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


def plan(me, en, jab_range=4, leap=5, cols=12, rows=10):
    if dist(me, en) <= jab_range:
        return [("JAB", en)]
    best = None
    for c in range(cols):
        for r in range(rows):
            h = (c, r)
            if h == en or dist(me, h) > leap:
                continue
            key = (dist(h, en), dist(me, h))
            if best is None or key < best[0]:
                best = (key, h)
    land = best[1]
    if dist(land, en) > jab_range:
        return [("INVIG", land)]  # still out of range: leap, Jab next turn
    return [("INVIG", land), ("JAB", en)]


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:5]]
    steps = plan((a[0], a[1]), (a[2], a[3]))
    print(" | ".join(f"{name} {h[0]} {h[1]}" for name, h in steps))
