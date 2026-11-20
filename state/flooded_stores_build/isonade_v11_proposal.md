# Isonade v11: one proposal from the QA pass (sim only, nothing live)

2026-11-20. The director asked (after the v10 QA pass, `isonade_v10_qa.md`): solo chart fight, over by round 18 and
never past 19, never idle, never a free kill, sim both Barnacle and Harpoon fixes, and solve every open issue. This is
the one proposal. Nothing has been built or changed live; a build waits on the director's yes.

Sim: `isonade_v11_sim/isonade_v11.ts` on engine pin `3314d122`, 16 seeds per read, zero live requests. Player is
dauntless solo with the PvE kit and pet. "Read" is how often the player answers a telegraph correctly
(1 = always, 0.85, 0.7). Params: `isonade_v11_sim/v11_proposal.json` (same as `params_d8.json`).

## Result: v10 as live today vs the proposal

| | v10 live | Proposal |
|---|---|---|
| Win, perfect read | 63% | 81% |
| Win, 85% read | 56% | 63% |
| Win, 70% read | 50% | 56% |
| Rounds to win (median / p90) | 16 / 19 | 13 / 17 |
| Longest fight (any outcome) | 24 | 19 |
| Isonade idle rounds per fight | 0.3-0.4 | 0.1 (one seed, round 10) |
| Scour per fight | 1.9-2.1 | 1.3 |
| Barnacle Hide per fight | 1.7-2.1 | 1.4 |
| Harpoon per fight | 2.0-2.6 | 1.1-1.2 |

Perfect-read losses (3 of 16) are seeds where the player's damage rolls run low and the Bore lands late; the flood
ends them by round 17-18 instead of a 24-round grind.

## The changes (20 rules, at the cap)

1. **Barnacle Hide cooldown 3 -> 6.** Clearing it now buys real time. (Once per phase would need a marker rule; the
   cap is full.)
2. **Harpoon cooldown 2 -> 4 (spacing, not a warning).** A warned Harpoon needs an omen rule and a marker; there is
   no rule slot. Spacing halves the hits. Absorb still counters it.
3. **Payoffs first.** The Undertow and Breaker rules move above the Scour/Silt reactions, so a Scour can no longer
   push the Undertow a round late (the fight 2 R7/R8 case).
4. **Scour/Silt reaction cooldown 5 -> 8.** About one Scour a fight instead of two or three.
5. **The churn rule goes.** "Black water churns" no longer posts every round, so the warnings are not buried. The sim
   showed no stray Undertows or marker misfires without it.
6. **New: The Hold Floods (replaces the churn's slot).** From round 11, last in its list at 30 AP, so it only fires
   with the AP left after the round's real move. Each use: a small pierce on the player (about 380 at first), and a
   stacking +12% damage taken on the player **and** +20% damage taken on Isonade. The fight speeds up for both sides,
   so it can't stall and a player near the kill gets there. It is also the filler that stops idle turns from round 11.
7. **Isonade HP: pools 2.5 -> 2.1** (12,625 -> 10,605). The director's call.
8. **Arm Lash power 45 -> 20.** It hit the pet for 4,545 live in round 1. By the same scaling the new hit is about
   2,000. Not verified: the sim pet doesn't rush the boss as the live pet did, so the sim can't reproduce the
   one-shot. Worth one live look.
9. **Black Water omen visual lasts 2 rounds** (was 1), so the safe crate still shows on the player's move turn.

Text only:
- **Brine Brand:** say the Undertow comes either way and a Cleanse halves it. Cleansing removes the doubled damage, not
  the Undertow (the QA "Undertow after Cleanse" case is working as built; the wording promised more).

## Kept as is (the director's ruling)

Clear on the Bore or on the Deep stays a valid answer to either; using it on the Deep means a harder Bore.

## Not covered

- Harpoon warning (no rule slot).
- Party play (chart is solo).
- Live check of the Arm Lash on a pet, and of the 2-round crate visual on the board.
