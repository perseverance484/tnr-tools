# Isonade: why each retest finds a new mismatch (review, 2026-11-18)

Asked by the director after the v3 retest: "take an in depth look at the rules set and the desired result and figure
out why we're struggling to achieve parity". Nothing was changed in the game and no fight was run for this review.

Evidence: the design (doc rev 33, Isonade section), `isonade_spec_v3.json` (20 rules, 17 jutsu), the v3 simulator
results (`isonade_results_v3.json`, 30 seeds), the live retest log (battle MUH-bMM1A, 12 rounds, every log line read),
the game source at the simulator's pin 3314d122 (2026-10-29) and on `main` today (`libs/combat/ai_v2.ts`,
`actions.ts`, `util.ts`, `process.ts`).

## The one root cause

The design is a timeline: telegraphed Slams every other turn, three Black Waters with a feed window after each, a bite
at half health that speeds things up. The engine has no timeline. Its AI re-reads a priority list before every action
and takes the first rule whose conditions hold and whose jutsu is usable right now (`performAIaction`: rules in order,
`availActions` filtered by cooldown, shared lock, pools and AP; an unusable pick silently falls to the next rule).
Conditions can only see HP thresholds, round numbers, distance, a live summon and effects on itself; there is no "last
action", no counter and no NOT.

So the timeline is emulated by five separate mechanisms whose interaction produces it:

1. HP thresholds start Black Water, Bite and the bitten chain, and stay true once crossed.
2. One-round self effects used as flags (increasecooldown, decreasecooldown, increaserange, robprevent, disarm,
   fleeprevent, elementalseal, increaseheal) carry "what comes next" from one round to the next.
3. Cooldowns stop repeats (Black Water marks 99, arm 5, Undertow 3).
4. AP costs decide how many actions fit in a round (mark 46, land 70, Black Water mark 50) and keep a mark from firing
   in the same round as the land that set its flag (70 + 46 > 100).
5. Rule order decides who wins when two beats are due in the same round.

None of these is checked against the timeline, and when one of them blocks a beat nothing errors: the AI quietly does
the next rule down. Every retest so far exposed a different one of the five.

## Every conflict found

| # | Conflict | Mechanism | Seen | Status |
|---|---|---|---|---|
| 1 | Slam II never landed: drain on every land shares a 4-round lock | live shared-cooldown table (runtime data, not code) | live retest 1-2 | fixed in 648 (damage pools) |
| 2 | Slam III never warned: Black Water at <75% (rule 11) outranks the Slam III mark (rule 17) | rule order | live retest 3 | open |
| 3 | Round 1 lost its Slam: It Rises 10 + Grasping Arm 40 + Undertow 40 = 90 AP, the Slam mark (46) no longer fits, so the chain started a round late | AP budget, adds above beats | live retest 3 (r1) | open |
| 4 | Which beats a player sees depends on their damage. Thresholds come every 25% of HP; a full Slam I-III chain is 6 rounds. dauntless dealt ~8.7% a round, so thresholds came every ~3 rounds and half the fight (6 of 12 rounds) was Black Water marks and lands; the bitten slams never appeared | HP-triggered beats + fixed-length chain | live retest 3 | design-level |
| 5 | The feed window (triple damage after each Black Water) speeds the next threshold, compressing the fight further for strong players | design feedback loop | live retest 3 | design-level |
| 6 | Simulator runs the 2026-10-29 pin; live runs `main`. `actions.ts` ~1,000, `tags.ts` ~2,000, `util.ts` ~2,900, `process.ts` ~2,500 changed lines between them. The AI rule loop itself is unchanged in behaviour; cooldown/lock handling, effect processing and AP are not | stale engine | 1 surfaced; others unknown | open |
| 7 | Shared-cooldown table and damage settings are staff-editable data (`battle.extraState.sharedCooldowns`, `dmgConfig`), so even current code cannot show them; the harness carries a 2026-11-18 copy of the table and a 2026-10-28 copy of the damage config | runtime data | 1 | open |
| 8 | Sim player is far weaker than the real one: sim median win 21 rounds at 44% HP; dauntless won in 12 rounds at 82%. In the sim the 75% mark fell at r6-7 with Slam I marked at r1, so Slam III always fit; live it started at r2 (see 3), so it didn't. The "near 40% HP" target was tuned against that weaker player | player model | live retest 2-3 | open |
| 9 | Pool text says it hits "with every action" (the design said the same, after the Arsenal Keeper's embers); the engine ticks a ground effect once per round per target (`shouldApply` timeTracker, same on pin and main), plus a free round when stepping in | design assumption vs engine | live retest 3 | open, text only |
| 10 | Flags borrow real tags. Today they are inert on Isonade (increasecooldown, decreasecooldown and increaserange only touch basic actions it never uses), but they are inert by accident: a staff table edit or engine change to any of them silently breaks the chain the way drain did | borrowed tags | not yet | risk |

## Recommendation: a fight the engine can't get wrong

Build the boss as a state machine whose invariants hold by construction, and check them before any live test.

1. **One beat per round, chained by flags at the top of the list.** Every telegraphed step (mark or land) casts the
   flag for the next step, and the rule for "next step" sits above everything else. Beats cost 60 AP, It Rises 10,
   extras (arm, Undertow) 30: one beat always fits, two never do (60 + 60 > 100), and at most one extra rides along.
   Adds can slip a round; a beat never can.
2. **Black Water as a slot in the cycle, not an HP interrupt.** Cycle: Slam I, Slam II, Slam III, Black Water, each
   a mark round then a land round (8 rounds), then repeat. Every player sees the whole pattern in the same order,
   which is what "players can learn the room" asks for. HP gates only the one-time Bite, which switches to the
   bitten cycle (combined land-and-mark beats, so slams come a turn sooner). About 16 of the 20 rules with the bitten chain.
   Alternative that keeps the 75/50/25 trigger: move every chain-continuation rule above the threshold rules so a
   Black Water waits for the current chain to finish. That fixes conflict 2 but not 4 or 5: a fast player still sees
   fewer beats.
3. **Flags with no gameplay meaning on the boss, checked live.** Keep tags that do nothing on a boss with no basic
   actions, and add a pre-release check that reads the live shared-cooldown table and fails if any kit tag is in it.
4. **Parity tooling before tuning.** Re-pin the simulator to current `main`; load the live shared-cooldown table and
   damage config at run time; add a replay check that feeds a live battle log's player actions through the
   simulator and requires the same Isonade action on every round. Calibrate the sim player to two real anchors
   (dauntless's 12-round kill, and a median 81+ player) instead of one modelled player.
5. **Say what the engine does.** Pool text: "Brine pool: hits anyone standing in it once each round".

Decisions that are the director's: the fixed cycle versus HP-triggered Black Waters (2), and which player the
"near 40% HP" target is for (4). Nothing above has been built or run.
