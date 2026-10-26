# Skyglass Wreck offline simulation: first report (2026-10-26)

Offline, engine-native fights (game source at origin/main, exported copy, in-memory battles; zero live requests). Written
from the simulation agent's report; numbers are in `results/*.json`. Targets: RUL-2026-10-26-006 / -007.

## Headline

- The live 16-wave definition (push/263) does not fit the hour: the strongest party modelled needs about 98 minutes for one
  clean pass at 15 s per player turn.
- **Calibration is the open question.** With the code's default damage settings, a level-100 Jonin party without gear
  wipes on wave 1 in 120/120 attempts (crew carry +350-450% built-in damage given; one Tide Bolt hits ~5,450 against a
  5,050-HP player). Gear, bloodlines and live damage settings are not modelled, so the "average party" must be anchored
  to real play before tuning numbers mean anything.

## Baseline (16 waves), 30 seeded runs per party

| Party (stand-in for gear) | HP | Damage taken | Damage dealt | Full clears | Where it fails |
|---|---|---|---|---|---|
| geared | x2.5 | -40% | +100% | 0/30 | floor 1 wave 2 |
| strong | x4 | -60% | +250% | 0/30 | floor 1 wave 3, then floor 2 wave 3 |
| elite | x6 | -75% | +400% | 6/30 | floor 5 |

Elite rounds per wave: about 9 for every 3-enemy wave on floors 1-4; floor 5 10 / 15 (Sealwright) / 13 / 11.5. The party
reaches the boss wave on ~8% HP (pools refill only between floors). Clean pass ~147-157 rounds: ~66 min at 10 s per turn,
~98 at 15 s, ~130 at 20 s. AI turns are effectively instant server-side; floor transitions assumed 30 s each.

## Where the time goes

- A 3-enemy wave takes ~9 rounds whatever the party's strength: 1-2 rounds walking (far-side spawns), and most rounds
  are basic attacks because player attacks sit on 7-round cooldowns.
- Floor 5 is about a third of a clean run and causes almost every wipe; the Sealwright (25,250 HP) and Crowned Captain
  (60,600 HP) waves run 12-15 rounds.

## Candidates (overrides/), minutes at 15 s per turn

| Candidate | Geared | Strong | Elite |
|---|---|---|---|
| candidate_2waves (10 waves) | not run | 3/30 | 30/30, 43% wipe once, ~83 min |
| candidate_1wave (each floor's elite/boss wave only) | not run | 28/30, ~47 min | 30/30, ~43 min |
| candidate_compact (7 waves of 2-3, boss HP halved) | 0/30 | 30/30, ~36 min | 30/30, ~36 min |
| **candidate_target20** | **30/30, 1/30 wiped once, ~26 rounds, ~20 min** | 30/30, ~19.5 min | 30/30, ~19.5 min |
| candidate_target20_soft (crew damage given +150%) | 30/30, no wipes, ~19.8 min | 30/30 | not run |

candidate_target20: one wave of two per floor (F1 Deck Warden + Core Horror; F2 Oathkeeper + Arsenal Keeper; F3 Sentinel +
First Blade; F4 The Captain + Wayfinder; F5 Crowned Captain + 2 Core Canisters), crew pools x1.5, Crowned Captain pools x4.
Easier than "1 run in 5 wipes once"; the boss wave is ~10 of ~25 rounds, so it is the lever for both time and risk.

## Behaviour findings (fix in the redesign)

- "round lower than 2" opener rules read the battle round, which keeps counting across waves: units in wave 2+ never fire
  them (Sentinel's Springguard, First Blade's Battle Trance).
- Unreachable rules (an earlier rule already covers them): Deck Warden rule 2, Core Horror rule 3, Oathkeeper rule 4.
- Crew spend 30-54% of actions moving or waiting; The Captain is the most passive.
- Core Canisters swing by layout: 37% of damage in the original boss wave, idle 99% in target20 (their range gate rarely
  holds against range-4 players).

## Easier version (level 40-60)

The player model takes a level (`lvl40`, `lvl50`, `lvl60`); overrides can set enemy levels. Sample: level-50 crew still wipe
a level-50 party in 2-3 rounds, because the crew keep stats x5, pools x2.5 and +350% damage given. The easy copies need those
lowered, not just the level.

## What is engine-faithful

Battle setup per floor, wave spawning, turn order, every action/effect/damage number, every enemy decision from captured
rules, push/250-252 edits replayed through the server's save path, dungeon rules (one battle per floor, pools refill after a
won floor, a wipe returns the party to floor 1). Approximations: players are AI-driven; damage settings are code defaults
(live values come from a settings table); gear is a stand-in; seeded spawn draws; one record-only hook to log rule hits
(verified outcome-neutral and deterministic).
