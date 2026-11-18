# Isonade v3: damage pools (2026-11-18)

Why: the live shared-cooldown table (misc.getSharedCooldowns, read 2026-11-18) locks drain for 4 rounds and the live
engine locks every other action sharing a tag whatever the cast's cooldown. All six slam lands carried the brine
drain, so landing Slam I locked Slam II. The director: "Let's just do a different effect for the pools? Like damage".
Damage is not in the table.

Simulator: harness/isonade.ts with `poolKind: "damage"`, run against an engine export whose applyActionCooldowns is
patched to the live per-tag lock (harness/livelock/livelock_patch.py; TNR_ENGINE_WORK=/root/isowork/engwork_live).
30 seeds, good level 100 player, full pools, reads 1 and 0.85.

| Build | Read | Win % | HP left (wins, median) | Slam marks / lands per fight | Lapsed warnings | Pool damage taken (median) |
|---|---|---|---|---|---|---|
| v2 brine, pin engine (old harness) | 1 | 83 | 46% | 9.2 / 8.3 | 0 | 1515 |
| v2 brine, live lock | 1 | 93 | 50% | 10.2 / 5.7 | 113 (every Slam II) | - |
| v3 damage pools 200 | 1 | 80 | 44% | 9.1 / 8.3 | 0 | 1448 |
| v3 damage pools 200 | 0.85 | 63 | 44% | 7.7 / 7.2 | 0 | 1695 |
| v3 damage pools 240 | 1 | 80 | 37% | 8.9 / 8.1 | 0 | 1738 |
| v3 damage pools 280 | 1 | 80 | 33% | 8.8 / 8.0 | 0 | 2029 |

The live-lock model reproduces the live test: with brine, Slam II and III never land. With damage pools every Slam
II and III lands on its warning (the only unmatched warnings are ones whose fight ended the next round).

Pick: pool power 200 (formula, 3 rounds), the closest match to the old 12% brine. The land's own hit is 360 so a land
still totals 560 on anyone caught in the rows (the pool tag also hits on the landing action). Shipped hidden as
push/648.
