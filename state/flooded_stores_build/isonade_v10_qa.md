# Isonade v10: full QA pass (live, hidden)

2026-11-20, 05:58-06:30Z. The director asked for a full QA pass: try to break the fight, test interactions and other
jutsu, budget 50m ryo, 2 hours. dauntless solo with the PvE kit (pet Little Horror in fight 2). Hidden content only.

| Fight | Battle | Result | Logs |
|---|---|---|---|
| 1 | `2mk-FLft-TZrp5O58Wr7h` | lost R26, Isonade about 30% | `/mnt/project-files/tnr/battle-logs/2026-11-20_isonade_v10_qa_fight1_2mk-FLft-TZrp5O58Wr7h.json` |
| 2 | `_m4bFrw0V0hFNJDZGbPy-` | lost R33, Isonade 673 / 12,625 | `/mnt/project-files/tnr/battle-logs/2026-11-20_isonade_v10_qa_fight2__m4bFrw0V0hFNJDZGbPy-.json` |

The earlier v10 test (`x6uPpWW1Hx5EOYSAkevQF`) was a win at R15. Both QA fights were played to probe, not to win.

## Breaks (the director's call whether to keep)

1. **Clear cancels the Tidal Bore.** Swell Rises puts robprevent on Isonade; the Bore rule needs it. One Clear
   (60 AP, worked from range 4) strips it and the Bore never fires (fight 1, R18). Smoke is not needed for the Bore.
2. **Clear cancels The Deep.** The crash needs Isonade's own shield; Clear removes shield and the 80% DR (positive
   effects, source `isPositiveUserEffect`). Fight 2 R15: no crash, Isonade Surfaced into its weakness window at
   once. The intended answer (pierce through the shield) is skipped entirely.
3. **The Undertow fires a round after a Cleanse.** Cleansing the Brand at R7 removed only its +100% damage taken.
   The Undertow keys on Isonade's own marker, so it still fired at R8 for 1,226. A player who cleanses feels safe
   and is hit a round later.

## Behaviour notes

- **Late fight is a Barnacle/Harpoon loop.** After the scripted chain, Barnacle Hide (1,500 shield, 25% DR) is
  recast every 3 rounds and Harpoon (884 pierce, ignores DR and smoke) every 2-4 rounds. Clearing Barnacle at R26
  brought it back the same round. A solo player who misses the R15 window loses to attrition: the only in-battle
  heal is Basic Heal (600, cooldown 5). Harpoon rounds: fight 1 R4, 8, 12, 15, 19, 23, 26; fight 2 R5, 10, 16, 21,
  24, 28, 30, 33.
- **Scour** fired 2-3 times a fight (fight 1 R10, R21; fight 2 R2, R7, R27) and strips every buff. Buff builds
  lose their setup.
- **Grasping Arm** one-shot the pet in R1 (4,545). It re-summons the round it dies, so killing it is wasted. From
  the far crate (E6) it could not reach dauntless and idled for 20 rounds.
- **Black Water:** at the move turn no ground mark shows which crate is safe (the omen's visuals are range 0 and
  last one round). Standing on a crate still took 0. Needs the director's look on the board art.
- **Smoke** (whole field, lands next round, also cuts your own damage 70%): smoked Bore 681 with 25% DR. It does
  nothing against Harpoon.
- **Absorb counters Harpoon:** Ethereal Rebirth 35% absorb turned 310 of 884 back into HP.
- **Stun immunity held** through the Black Water self-seal (Stun Jab, R12). Seal guard held.
- **Dead turns:** Isonade ended its turn doing nothing on most rounds after 75%.
- **Not testable:** player seal on Isonade (dauntless owns no seal jutsu); party play.

## Spend

About 102k ryo (Full Potions 100k, food). Used: 6 Full Potions, 7 Repair Kits, 2 large ramen, 2 smoke bombs,
2 Miracle Potions, 4 Chakra Pills.
