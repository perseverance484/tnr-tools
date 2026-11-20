# Isonade v10: no seals for rounds 1-5, Omen: Black Water from round 6 (HIDDEN, job 670)

The director (2026-11-20 01:07Z, relayed): "I want both to be true, below 75% and after round 5. My plan is to give
Isonade Seal immunity for the first 5 rounds until Black Water is used for the first time. Seal Immunity drops and
they Seal themselves for the damage amp next round. Just to slow players down a bit so they arent speed running
through it".

## What changed (engine pin 3314d122)

- **Record:** sealprevent 100 (static), 5 rounds, added beside stunprevent 100 and the 70% hull.
  - Record effects start the battle with their own rounds (combat.ts 4117-4136) and lose one round each time the
    round advances (util.ts 3042-3049). So the guard is up in rounds 1-5 and gone from round 6.
  - A player's seal checks sealprevent first (tags.ts seal(), preventCheck) and is cancelled.
  - The guard is fromType bloodline, so Clear and Cleanse can't strip it (persistentEffectSourceTypes).
- **Rule 15:** Omen: Black Water now needs `health_below 75` **and** `round_greater_than 5` (ai_v2.ts: round > 5).
  Its own self seal lands as before, because the guard has already run out.
- **Validator note:** sealprevent only accepts `calculation: "static"`. A copy of the stunprevent shape with
  "percentage" is refused.
- **Unchanged:** stun guard (record and worn Isonade's Old Hull, CHEST, drop 0), hull 70, the 18 jutsu and the other
  19 rules.

## Why a timer, not "until the first Black Water"

The only seal guards a player cannot Clear are on the AI record or on worn gear, and nothing Isonade casts can remove
either. A jutsu-laid guard could be dropped by the omen, but a player's Clear would strip it too, and players Clear
Isonade's Tide buff routinely. With the round-6 gate, the guard ends on the first round Black Water can come.

**Consequence:** a slower player who hasn't got Isonade under 75% by round 6 can seal it from round 6, before Black
Water. For a fast player the two coincide.

## Sim (isonade_v10.ts, 12 seeds each)

Players:
- **read 1:** answers every tell.
- **read 0:** ignores tells and casts lifesteal greedily.
- **seal:** seals Isonade whenever the seal is off cooldown (every 4 rounds).

| Player | Live (669) | v10 |
|---|---|---|
| Perfect, seals | won 100%, 12.5 rounds (p10 10), 42% HP left; first player seal R1-2; omen R8 (min R5) | won 100%, 16 rounds (p10 11), 34% HP left; first player seal R6; omen R11 (min R7) |
| Ignores tells + lifesteal, seals | won 83%, 7 rounds, 54% HP left | won 0% (Isonade at 61% when they died) |
| Perfect, no seal | won 83%, 16 rounds, 29% HP left; omen R9 (min R8) | won 75%, 16 rounds, 30% HP left; omen R9 (min R8) |
| Ignores tells, no seal | won 0% | won 0% |

- In every v10 run, no player seal landed before round 6, the omen never came before round 6, and Isonade's own
  seal landed (3 sealed rounds per fight).
- No stray Undertow or Floods fired.
- Files: `isonade_v10_sim/`.

The perfect no-seal pair differs by one seed of 12, which is noise. Without seals the omen already came at round 8
or later, so the gate changes nothing there.

## Build

- **Job 670-mwoaabsv:** DONE, 2/2 verified. Bundle `harvests/inbox/tnr_results_1795137158269.json`.
- **Read-back:** `state/stolen_stores_captures/isonade_v8_live_2026-11-20/post670_getAi_isonade.json`.
  - Effects: stunprevent 100/99, hull 70/99, sealprevent 100/5.
  - 18/18 jutsu equipped; Old Hull CHEST, drop 0.
  - Rule 15 reads health_below 75 + round_greater_than 5.
- **Not tested live:** dauntless has no seal source, and the test needs full HP plus the director's go.
