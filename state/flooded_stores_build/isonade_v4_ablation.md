# Isonade revision 4 (live, push 653): what each missed answer costs

Asked 2026-11-19 19:22Z by the director: "If you read every set piece and clear, cleanse and smoke properly its
winnable? What does failing to do each cost you?" and 19:23Z: "Then we can set what each costs you if played properly
or improperly and determine what a win or loss takes".

Sim only, zero live requests. Params `/v4_retune/params_R25.json` (the live revision). 20 seeds per row, read 1 with one
answer forced off (`isonade_v4.ts --skip <answer>`), plus read 0. Sim player: 81+ stand-in, 6,250 max HP; it has no Smoke,
so Defensive Stance (the damage cut ahead of the Breaker) stands in that slot. dauntless took about 1.6x the sim's
damage live, so read these as optimistic.

| Run | Win % | HP left on a win (median) | Extra damage vs perfect | Where it lands |
|---|---|---|---|---|
| Perfect | 85 | 47% | - | losses end with Isonade at 1% |
| No Clear on Tide | 70 | 47% | +590 (9%) | Breaker 1,523, or 2,882 with a Brand on |
| No Cleanse on Brand | 70 | 50% | +240 (4%) | Breaker with Tide and Brand 2,984 |
| No Stance (Smoke slot) | 70 | 46% | +320 (5%) | Breaker 1,346 instead of 1,144 |
| No crate in Black Water I | 100 | 23% | +1,560 (25%) | Black Water I lands 1,707 (27%) |
| Deep shield not broken | 85 | 47% | 0 | the Deep came in 3 of 20 fights; basic attacks broke the shell anyway |
| Ignores everything | 40 | 5% | +2,800 (45%) | one Breaker 3,029 (48%) |

Perfect-read damage per fight: Breaker 1,797, Anchor 776, Arm 656, Harpoon 520, wounds 264 (4,013, 64% of max HP).

Findings:
- A single missed core answer (Clear, Cleanse, Stance) costs only 4-9% HP, but drops wins 85 to 70: the perfect run
  already finishes close, so any loss is a long fight that runs dry with Isonade under 20%.
- The crate is the biggest single cost (a quarter of the HP bar) and still never loses: staying put deals more damage.
- The Deep almost never matters: fights end by round 11-12, and its 1,500 shell breaks under ordinary attacks.
