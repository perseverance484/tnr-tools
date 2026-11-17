# AI player, AP4, first part: the two measures and the move atlas. Handoff for review

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-17.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap4
Stands on: fable/ai-player-run2-followup @ e051d0622d9861032b583276b8b95cd96d1d6287, handed off 2026-11-17;
           its review has not returned. The diff to review here is e051d062..HEAD.
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Authority: RUL-2026-11-17-166 (the director: "1-3 approved. 4, yes. 5, acceptable", and on 4: "Actually no, just
           check after every fight. Repair when its below 25%")
Engine: studie-tech/theninjarpg @ df864509f8b33f4c9cf8332fd416ab511d2f0478, the harness's pin, offline
```

AP4 comes before AP3 now, and it starts with the move atlas. The director also approved two things that judge
every change to how the planner chooses: `tune_real` looking further than one exchange, and the worst-case reply
check as a setting. All three are here. Nothing was played, and no fight is played differently: both settings
are off, and nothing reads the atlas yet.

## 1. `tune_real --depth`: a line played against several of his actual turns

`tune_real` fires each line in the engine and answers it with the turn he actually played next. One exchange
gives a buff no credit for the rounds after it, so it could not say whether setup rounds are worth too little
or too much. With `--depth N` the turns that followed in the log are played on, his and mine in turn, and each
of my turns also keeps where things stood after his N-th.

- `harness/pvp_turn/engine/replay_sim.ts`, eval mode: `script`. `scriptedReply` is untouched.
- `postmortem.py`: `turns_after`, `deep_swings`; `DEPTH` is 1 unless set, and then nothing changes.
- My turns in the script are the ones I played after what was played. So the deeper figure leans to what was
  played: it is "with the same follow-up", not each line's best.

In the engine, on run 2's loss to Selaphiel, the one-exchange figures are the same on all ten turns at depth 1
and at depth 3. What it shows that one exchange cannot, from the same fight: in round 7 the planner's pick is
382 HP ahead of what was played after one exchange and 665 behind after three.

Twelve logged fights, today's planner, every one of my 66 turns (with my whole kit in the engine, section 4,
none is left that the engine cannot fire; before, 12 were):

| | Turns | The planner's pick | What was played | The pick is the best of its set |
|---|---|---|---|---|
| After his next turn | 66 | +559 | +593 | 29% |
| After three of his turns | 42 | +845 | +823 | 26% |

After one exchange the pick is 34 HP behind what was played; three turns deep it is 22 ahead. Both gaps are small
beside how far a turn's figure moves from one turn to the next, so this settles nothing about setup rounds yet.
It shows that one exchange understates the planner's picks. Whether setup is weighted right is found by moving
the weights and reading this line, which is what it is for.

## 2. The worst-case reply check: a setting, measured, off

`TNR_WORST_CASE=guard`: a line that one of his listed replies kills (his likely lines, and the hardest one he has
ready) goes behind every line that survives them all. The order holds through the lookahead. Not when every
line loses, and not when every line dies to something.

| | Off | `guard` |
|---|---|---|
| Simulator, the whole matrix, 196 fights | 190 won; 2,565 HP left on average | 190 won; 2,561 |
| `tune_real`, 12 fights, 66 turns: the pick after his next turn | +559 | +559 |
| the pick after three of his turns (42 turns) | +845 | +845 |
| Turns where it changed the pick | | 0 of 66 |

**It changes nothing, so it stays off.** A line that one of his listed replies kills already carries the death
term in its score and is at the bottom before the check looks at it. By the brief's AP6 (keep only what is
needed) it is a candidate to go.

## 3. The move atlas

`player/atlas.json`, made by `player/atlas.py` from the catalog and the engine; never by hand.

| | |
|---|---|
| Cards | 1,165: every jutsu that is not an AI's or a pet's, every item used from a hand, item or thrown slot that has an effect, the 8 basics |
| Fired by the engine | 894: 747 jutsu, 139 items, the 8 basics |
| Effect types on them | 53 |
| Not fired, and saying why | 109 for PvE only; 133 the engine does not list as an action in a fight; 29 it refused |
| Of my own kit | 39 actions measured a second time, fired by me as I am |
| Build | 45 seconds; three builds in a row are the same bytes |

**A card** is what the game's own combat code did when the action was fired alone on a fresh board: both at full
health, next to each other, round 1; the caster with capped stats and the endgame gear the director assumes,
the jutsu at level 25, against my own profile and gear. It holds what the engine asks for it, what it took off
each side at once, every effect and ground effect it left (power, per level, level, rounds, on whom, by whom,
and whether it only counts from the next round), where both stand, and one idle round on. The record's own
fields (cost, cooldown, range, target, method, bloodline, weapon, effect types) are beside it.

**The caster is built again for every card**, with that card for his whole kit and what the engine asks for
before it lists it: its bloodline, the elements it is of, a weapon of the kind it is cast with, the item its
bloodline requires. Without those the engine did not list 48 jutsu that it lists now, Thunder's Judgement among them.

**`python3 -m player.atlas check`** says which cards a changed catalog has made stale: each card carries a mark of
the record it was made of, so harvests that touch no card do not. With the engine it also makes the atlas again
and compares. **`coverage`**: every action of a player in every logged fight has a card the engine fired, but
three summons (Jade, Hell Hound, Momo); the harness strips summons.

My kit, fresh board, against the standard opponent. The first column is what the planners use where there is
no engine (`shotplan.MINE`):

| | Hand-written | Fired by me in the engine |
|---|---|---|
| Stormblade Arc | 707 | 707 |
| Night's Testament | 631 | 631 |
| Forbidden Chakra Fury | 620 | 615 |
| Rebirth, Shrapnel Clone Barrage | 600 | 615 |
| Forgotten Ember Blade | 560 | 546 |
| Lotus Dance | 560 | 615 |
| Danse Macabre | 420 | 451 |
| basic attack | 150 | 205 |

**What the atlas is not yet.**

- **Nothing reads it.** The planners still use the hand-written kit (`shotplan.MINE`, `clock.compile_record`).
  Replacing them is the next step, and by RUL-2026-11-17-166 it is a setting first.
- **What Clear, Cleanse, a seal and the prevents do to each effect** is not on a card.
- **Heals** do not show: the board is at full health. The record's effect types are on the card (`tags`).
- **The brief's 1% gate** (a card applied alone matches the engine) is about the planner applying a card. The
  card itself is the engine's answer.
- 27 jutsu the engine still does not list for the standard caster (18 are reskins of another jutsu, 6 ask for a
  bloodline item in a way the caster is not given), and the summons.
- The catalog here has 1,859 records. The brief speaks of 2,985: this checkout's catalog is built from the
  harvests on `main`.

## 4. Two faults found on the way

- **Engine runs side by side could read half a file.** `harness/pvp_turn/run.sh` copied its TypeScript files into
  the engine's folder on every run. Two of the first five builds of the atlas came out wrong: a batch with no
  answer, and a batch answered "I.act is not a function". Files are now put in place only when they differ, by a
  rename. This was there before the atlas: anything that ran
  two engine processes at once could lose answers.
- **The engine never had my whole kit.** It is given my kit from a list kept by hand, which lacked Chakra
  Resistance (in today's PvP 1), Limit Breaker and PvP 2's five. The engine refused every line of mine with one
  in it, so the reviews had no figure for them (run 2: Phantom Step + Chakra Resistance). The list is now
  extended by whatever my loadouts hold. The 31 actions measured before have the same figures.

## 5. Repair

Asked as a choice of two, answered "yes", then corrected. Gear is checked after every fight and repaired under a
quarter of its durability, which is what the brain does. No code is changed. The ledger has both answers.

## Changed

| Commit | What |
|---|---|
| `1c082726` | RUL-2026-11-17-166; the brief's order, AP4 before AP3 |
| `d3e6622f` | `tune_real --depth`: `replay_sim.ts` `script`, `postmortem.py`, `tune_real.py` |
| `c3b61030` | planner2: `TNR_WORST_CASE`, off |
| `41099f66` | `harness/pvp_turn/run.sh`: files renamed in, only when they differ |
| `dad5105d` | `engine_bridge.my_kit_ids()` |
| `b8becfc5`, `945a8159` | `replay_sim.ts` `cards` mode; `player/atlas.py`, `player/atlas.json`, `player/tests/test_atlas.py` |
| `9597576c` | `player/combat.py`: the planner's calibration module is claimed in the registry |
| this one | this note |

The protocol number stays 10. No default of the planner is changed.

## Verification

On the head before this note (`9597576c`), with the note in the tree:

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 692 tests`, `OK` (e051d062: 681) |
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 44 tests`, `OK` |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `tools/tests/test_{critique,integration,loss_fixes,nearkill,pilot,planner2,review_tools}.py`, engine present | exit 0 each; planner2 parity 4000/4000 |
| `test_{critique,loss_fixes,review_tools}.py` with `TNR_ENGINE_APP` pointed at nothing | exit 0 each |
| the nine `scripts/test_*.py` | `OK` each |
| `python3 -m player.atlas check`, engine present | "the atlas is current (made again: 1165 cards)", exit 0 |
| `python3 -m player.atlas check`, no engine | "the atlas is current (no engine app here: not made again)", exit 0 |
| `python3 -m player.atlas coverage` | exit 1, as it must while any is missing: the three summons |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits origin/main..HEAD`), `git diff --check origin/main HEAD` | exit 0 each; 338 rulings |
| `player_allowlist.py check`, `report --check`, `player_size.py` | exit 0 each |
| `doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`, `lawmap.py` | exit 0 each |

One test failed on the way and is why `9597576c` exists: the inventory test asks that every pilot tool the
player's code imports has an owner in the registry, and the atlas's generator imports the planner's calibration.

Measured, not gated (figures above): `tune_real --fights 12 --depth 3` with the worst-case check off and on; the
simulator's whole matrix, 196 fights, off and on; the Selaphiel loss reviewed at depth 1 and 3; the atlas made
three times.

## What is not shown

- **Nothing live.** No relay, no connector call, no run lock.
- **No engine in the tests.** The suite runs without it. What needs it was run by hand and is in this note: the
  one-exchange figures at depth 1 and 3, the atlas made three times, `atlas check`.
- **The simulator is kind**, as before: it is a screen for a change that loses fights, not a measure of how
  many are won.
- **`tune_real` at depth** has my follow-up turns as played, as said above.

## Live-game statement

Zero live requests. The engine ran offline at the harness's pin with socket calls denied.

## Not begun

The planner reading cards. What Clear, Cleanse, seals and prevents do to an effect. AP4's steps 1 to 5. AP3.
Keeping the enemy on our ground.
