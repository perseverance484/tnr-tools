#!/usr/bin/env python3
"""Plan the opening turn of a hunting fight (odd-q hex grid, 12x10 hunting map).

Usage: hunt_plan.py ME_COL ME_ROW EN_COL EN_ROW [--buff]
(--buff: always Invigoration first; needed for 5,000+ HP targets, D-rank 2,940 HP dies to a bare Jab)
Prints the exact performAction calls to make, e.g.
  JAB 8 3                      (enemy already within Jab range: one call)
  INVIG 7 3 | JAB 8 3          (Chakra Invigoration to (7,3), then Jab)

--ab: prints the whole A/B (10,650 HP) fight with fixed battle versions; fire every line in ONE batch of
parallel tool calls (they execute in order), then ramen + the next hunting.start. Buy large ramen before every
A/B hunt: chakra carries between hunts. Basic attack is once per turn. Per-creature scripts (2026-11-10):
  Enrai No Oni   INVIG v1, JAB v2, EMBER v6, OVERFLOW v7, FURY v10, BASIC v11 (dead).
  Tsukihana      same, then DEF STANCE v12, ETHEREAL REBIRTH (K0t6Z-Q4lau1jFt8Tkpot) v15 (dead).
  Kugatsunagi    stuns on R1. INVIG v1, JAB v2; read version v; EMBER v, BASIC v+1, DEF v+2, FURY v+5.
  If the landing isn't adjacent the enemy walks in: play R1, read version v, shift every later version by v-6.
Connector cap is 30 calls/min: one hunt is about 11 calls, so at most two hunts a minute.

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


def plan(me, en, jab_range=4, leap=5, cols=12, rows=10, buff=False):
    if dist(me, en) <= jab_range and not buff:
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


IDS = {
    "INVIG": "AJNmwnlzhqiHzdE84_m9k", "JAB": "VT7oxj_fObWuQa3Rq_BbI", "EMBER": "Wy7EBGd7gpP96hyumb0Lz",
    "OVERFLOW": "e2eC-x4UXc5m6QexNbx8w", "FURY": "Lg_thN-MB8FRAr_Agf9tn", "BASIC": "basicAttack",
}


def ab_script(me, en):
    """A/B (10,650 HP) one-batch script. Valid only when the Invigoration landing is adjacent to the
    enemy: the AI then stands still and versions are fixed (verified 2026-11-10, Enrai No Oni x3:
    R1 v1-2, R2 v6-7, R3 v10-11; enemy HP 10650 -> 7973 -> 4330 -> dead). Returns None otherwise."""
    steps = plan(me, en, buff=True)
    land = steps[0][1]
    if len(steps) < 2 or dist(land, en) != 1:
        return None
    seq = [("INVIG", land, 1), ("JAB", en, 2), ("EMBER", en, 6), ("OVERFLOW", land, 7),
           ("FURY", en, 10), ("BASIC", en, 11)]
    return [(n, IDS[n], h, v) for n, h, v in seq]


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:5]]
    me, en = (a[0], a[1]), (a[2], a[3])
    if "--ab" in sys.argv:
        s = ab_script(me, en)
        if s is None:
            print("NOT-ADJACENT: play R1 then re-read the battle")
        else:
            for n, aid, h, v in s:
                print(f"{n} {aid} {h[0]} {h[1]} v{v}")
        sys.exit(0)
    # --buff: always open with Invigoration (+30% given) - use for 5,000+ HP targets (C rank and up)
    steps = plan(me, en, buff="--buff" in sys.argv)
    print(" | ".join(f"{name} {h[0]} {h[1]}" for name, h in steps))
