# Isonade v6: The Deep at 35%, Scour and Silt back sooner (HIDDEN)

Job 658 (`push/658_isonade_v6_reactions.gen.py --cd=5`), live and hidden since 2026-11-19, 5/5 verified.

- The Deep's omen moved from rule 15 to rule 6, right after the set-piece lands, at 70 AP.
- Scour and Silt Cloud cooldown 10 -> 5. **Reversible placeholder**; the value is the director's call.

Rollback captures: `state/stolen_stores_captures/isonade_v6_live_2026-11-19/`.

## Correction to the v5 write-up

v5 said Scour did not refire because the rotation spent Isonade's AP first. That was wrong. Scour and Silt
already sat ahead of the rotation (rules 6 and 7). Their 10-round cooldown kept them quiet.

## Sim (harness `isonade_v5.ts`, deepFirst, 12 seeds, params `isonade_v6_params_cd*.json`)

| Variant | Reads every tell | Skips smoke | Reads nothing |
|---|---|---|---|
| cooldown 10 | 66.7% win, 45% HP left, 16 rds; Deep 7/12, always pierced | 58.3% | 0% |
| cooldown 5 | 66.7% win, 39% HP left, 16 rds; Deep 10/12, always pierced | | 0% |
| cooldown 3 | same as 5 | 75% | 0% |

Cooldown 5 and 3 come out the same: the IDG mark, not the cooldown, gates Scour and Silt. With the omen after the
set-piece lands, the Deep's crash never fires the same turn, so the pierce window is always there.
The sim player has 6,250 HP; live dauntless has 5,050.

## Live hidden retest (2026-11-19 23:33Z, battle DRHKoZODjY9eTmTR6QkfY)

dauntless, solo, pet Little Horror. Kit: Eclipse Drain, Chakra Overflow, attacks, Elite Smoke Bomb and
Night's Testament (pierce). Started at full HP.

**Test flaw:** the item loadout was the PvP set (Kaeruun's, B-bCCtg-_fvcJSrvR1ts0), not the PvE set used in v5.
That set carries the smoke bomb and the pierce item. dauntless's first turn was also lost to the turn timer.

Log: `/mnt/project-files/tnr/battle-logs/2026-11-19_isonade_v6_test_DRHKoZODjY9eTmTR6QkfY.json`.

**Result:** lost in round 7, with Isonade at about 91% (11,505 / 12,625). dauntless took 6,807 damage and dealt
about 1,120. The quest closed at 1 HP with no hospital stay. The 75%, 55% and 35% marks were never reached, so
the crate, the smoke and the Deep pierce windows went untested.

| Check | What happened | v5 for comparison |
|---|---|---|
| Grasping Arm | Arm Lash one-shot the pet in round 1 (4,545) | Same |
| Silt Cloud (90) | Fired round 2 (Invigoration 30 + Eclipse 30 + standing 40) | Round 3 |
| Clear (round 3) | Removed the Tide's +100% damage, Silt's 40% DR, and the Barnacle shield and DR | Same |
| Scour (100) | Fired round 3 after Chakra Overflow and stripped every buff, Invigoration's DR 25 included. Did not refire in the 4 rounds left (cooldown 5) | Fired round 2 |
| Breaker (round 4) | **3,818** to dauntless with no DR up. Tide had been cleared. Wound 229 for 2 rounds | 1,410 |
| Harpoon (round 5) | 884 pierce | 884 |
| Brine Brand (round 6) | Heal block 3 rounds and +100% damage taken. Also put a move-lock on Isonade | Same |
| Cleanse, then Undertow (round 7) | Cleanse removed the +100%, but the Undertow still fired: 1,647 + 500 shield. It killed dauntless | 962 + 800 shield |

What this shows:

- **The Undertow's trigger is Isonade's own move-lock from the Brand (rule 8), not the Brand on the player.**
  Cleanse cannot stop it. It only takes away the +100% damage taken. That works as designed, but the window is
  "Cleanse to halve it", not "Cleanse to skip it".
- **The Breaker is the swing hit.** It did 3,818 with nothing braced. In the sim, with Defensive Stance, it
  does about 1,015. Its only tell is the Tide two turns earlier. Clearing the Tide removes the +100% but not the
  Breaker.
- **Scour does its job.** It stripped the DR buffs right before the Breaker, which is why that hit was so large.
  A player who stacks to 100 IDG on the turn before the Breaker pays twice.

## Not yet answered

- The smoke and Deep pierce windows need another run, in PvE armour with the smoke bomb and the pierce item.
  The armour is the open question: either build an item loadout with all three, or add the two items to the PvE set.
- Scour and Silt cooldown 5 is a placeholder until the director picks the value.
