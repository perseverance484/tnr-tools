# Isonade v5: Strict windows, base DR, marks 90 / 100

Ask (the director, 2026-11-19): strict fight, base DR on Isonade so big lifesteal hits can't
skip mechanics, tested with Eclipse Drain on dauntless, with clear windows for Clear, Cleanse,
Smoke, pierce (the Deep) and movement (crates).

Picked marks (the director, 22:32Z): Silt Cloud fires when the player's damage given reaches 90;
Scour fires at 100. Both are `target_has_effect` on `increasedamagegiven`.

## What the AI reads (source, pin 3314d122 and main 7fc8789d agree)

- `target_has_effect` sums the stored `power` of the effect type on the target (ai_v2.ts
  reachesEffectPower). No active or cast-this-round filter. Thresholds are 0-100.
- Unscoped percentage damage given from armor, accessory and keystone is folded out at battle
  start (damagePipeline.ts consolidatePreBattleDamageModifiers). The AI never sees gear IDG.
- What it sees: bloodline, pet species passives, element-scoped and trained-element bonuses,
  raid/meal buffs, cast buffs. Skill trees are excluded (not live).
- dauntless at battle start: 40 (bloodline 20 + pet 20). Best A/S player: 45, or 60 with a
  capped trained element.
- Cast buffs: Eclipse Drain 30, Chakra Overflow 50, Inner Peace 50, Parry 30.
- With 90 / 100: dauntless trips Silt with one Overflow and Scour with Eclipse Drain plus a
  second buff; the best player trips Silt with Eclipse Drain alone and Scour with one Overflow.

## Sim (12 seeds, harness isonade_v5.ts, engine pin 3314d122)

C1 = dauntless baseline (sim player carries no passives, so a live mark M is simulated as
M - 40). C2 = best A/S player (M - 60). Base DR on Isonade: decreasedamagetaken 70, 99 rounds.

| Run | C1 dauntless | C2 best player |
|---|---|---|
| reads every tell | 66.7% win, 42.7% HP left, 15.5 rds | 83.3% win, 48.7% HP |
| ignores tells | 0% | 0% |
| skips the Deep (pierce) | 0% | 0% |
| skips Cleanse | 33% at 12.7% HP | 83% at 10.2% HP |
| skips Smoke | 58% at 15.4% HP | 83% at 29.5% HP |
| skips Clear the Tide | 83% at 13.5% HP | 83% at 44.3% HP |
| skips the crate | 67% at 35.1% HP | 67% at 44.7% HP |

Read: ignoring tells and skipping the Deep lose outright. Skipping Cleanse, Smoke or Clear costs
roughly 25-35 points of HP left. Skipping the crate costs the least (about 4-8 points); Black
Water I at 900 is survivable at full HP.

Raw outputs: `v5_sim/C*_*.out.json`. Params: `isonade_v5_params_C1.json`, `_C2.json`. Spec:
`isonade_v5_spec.json` (C1 params).

## Build

- `push/655_isonade_v5_windows.gen.py` writes 655 (4 hidden jutsu creates) and 656 (unequip,
  full-record jutsu edits, kit re-equip, Isonade effects, AI rules with the marks overridden).
- Unchanged live: It Rises, Black Water omen, Scour, Silt Cloud, Grasping Arm Rises.
- Dropped from the kit: Shed, Drowned Anchor.

## Not covered by the sim

Player skills, titles, raid buffs, cooking, clan, sage mode. The live hidden test on dauntless
checks the marks against the real battle-start state.

## Live hidden test (2026-11-19, battle JVuqkJ6fO8Zd6S3CvEH-A)

dauntless, PvE kit (Eclipse Drain, Chakra Overflow, Thunderbolt Fury and the rest), pet Little Horror,
full HP, solo. Log: `/mnt/project-files/tnr/battle-logs/2026-11-19_isonade_v5_test_JVuqkJ6fO8Zd6S3CvEH-A.json`.

Result: won in 14 rounds with 1,292 / 5,050 HP left (26%). Sim C1 with every tell read: 66.7% win,
43% HP left, 15.5 rounds. The live run skipped the smoke window (kit has no smoke bomb) and never saw
the Deep, so it sits between "reads every tell" and "skips Smoke".

| Check | What happened |
|---|---|
| Base DR vs big hits | Single jutsu landed 637 to 1,842 through DR 70. Eclipse Drain lifesteal returned 35% of a hit: 423 on 1,210, 400 on 1,144, 149 on a hit the shield ate. Lifesteal alone could not outheal the fight. |
| Absorb, not lifesteal, was the big sustain | Chakra Shield, Stormguard Aura and Ethereal Rebirth turned Isonade's hits into 293 to 1,234 HP each (1,234 off Tidal Bore). |
| Scour at 100 | Fired round 2 at stored 108 (bloodline 20, pet 20, Eclipse 30, Thunderbolt 38) and stripped Eclipse's lifesteal and damage buffs. It did not fire on rounds 5, 10, 11 and 12 with 125 to 158 stored. Correction (v6): the cause was Scour's 10-round cooldown, not AP; Scour and Silt already sat ahead of the rotation (rules 6 and 7). |
| Silt Cloud at 90 | Fired round 3 (bloodline 20 + Overflow 70 after the pet died) and round 13 (alongside Tidal Bore). |
| Chakra Overflow | At level 25 it gives two 35s (70), not 50. With the pet alive Overflow alone puts dauntless at 110, so Scour, not Silt. |
| Clear (Tide Draws Back) | Tide shows "+100% damage given for 1 round". Clear removed it and Silt's 40% DR; base DR 70 and stunprevent survived the Clear. |
| Cleanse (Brine Brand) | Brine put heal-block 3 rounds and +100% damage taken 1 round on dauntless; Cleanse removed both before the Undertow (962 + 800 shield). |
| Crate (Black Water) | Omen round 8, Floods round 9: no damage while standing on the crate at (6,1). One full turn of warning. |
| Tidal Bore (Smoke) | Swell Builds round 11, Swell Rises 12, Bore 13: two turns of warning. Unbraced, no smoke: 3,024 + 500 shield. The largest hit of the fight. |
| Harpoon | 884 pierce, broke the shield as designed. |
| The Deep (pierce) | Never fired. Isonade crossed 35% in round 11 while the Swell chain held the rotation, then died in round 14. A burst player can skip the Deep entirely. |
| Grasping Arm | Arm Lash one-shot the pet in round 1 (4,545), then hit nothing for 13 rounds: the Arm does not move and dauntless stayed out of its reach. |

Not tested: Smoke and the Deep pierce window (no smoke bomb or pierce jutsu in the PvE kit).

Open for the director: Scour's 10-round cooldown keeping it quiet (first written here as losing to the rotation; corrected in v6), the Deep being
skippable when 35% falls inside the Swell chain, and whether the Arm should reach.
