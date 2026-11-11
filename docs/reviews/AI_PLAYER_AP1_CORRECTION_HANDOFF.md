# AI player overhaul, phase AP1: correction handoff

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-11, in answer to the independent
review of `583fe353` ("request changes": four high findings, seven medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 583fe35390e4701eea50f331ae2bc10013f150c9
Review: docs/reviews/AI_PLAYER_AP1_REVIEW.md on chatgpt/review-ai-player-ap1 @ e94bf21c (evidence; not merged)
Base: 40788e78d4159777a47e0b317fe13d83fa1819b3 (fable/ai-player-base, unchanged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Commits since the reviewed SHA:
  3dcbcdfa  RUL-2026-11-11-151 (was the head of fable/ai-player-rulings; the review read it as evidence)
  4b7079e5  cherry-pick of Duet's b37a287e: the director's 24 h hold in do_not_attack.md (one line)
  3a154d4b  the corrections and their tests
  the head  this note
Integration target: main (not integrated; main has moved on with run-lock and player-session commits only)
Duet's branches: fable/pilot-planner-fixes is now at e14317c5 (session logs and kits; pilot.py unchanged since
                 dacdf7e2). Not merged here, apart from the one line above. fable/pvp-engine-harness @ f6e8c860.
```

## Disposition

All eleven findings are **confirmed**. Each was reproduced on `583fe353` before anything was changed, with the
review's own numbers where it gave them. None is refuted and none needs clarification.

| # | Finding | Reproduced on `583fe353` | Corrected in |
|---|---|---|---|
| 1 | High: the shared budget can pass 30 | 27 calls after turn one, 32 after turn two, a 41.7 s hold | `budget.py`, `battle.py`, `brain.py` |
| 2 | High: refused or undelivered plans stop the deadline fallback | reads only at T+1, T+12, T+15, T+20, T+60; `fired_at` set after a crash in `_compose` | `budget.py`, `battle.py`, `brain.py` |
| 3 | High: the fallback repeats a refused action | `defensiveStance` sent again while banned | `battle.py` |
| 4 | High: results not bound to relay and batch | a call made before the cutoff taken; an unrelated transcript taken | `relay.py`, `brain.py` |
| 5 | Medium: an unknown price counts as zero | ramen bought at exactly the daily cap, no decision raised | `gates.py`, `calls.py`, `recovery.py` |
| 6 | Medium: a hold past midnight ends early | nobody held at 23:55 inside 23:50-00:20 | `gates.py` |
| 7 | Medium: missed turns can hide | `acted: true` with no answer and no log line; no row on a round jump | `budget.py`, `battle.py`, `console.py` |
| 8 | Medium: wiring passes with production adapters unplugged | 5 of 5 pass with `plan_turn` and `save_kit` patched out | `tests/test_wiring.py`, `registry.py`, `combat.py` |
| 9 | Medium: purchase events before approval or success | "ramen bought" with no `village.buyFood` sent | `recovery.py` |
| 10 | Medium: the opening archive loses information | first row `seat: null`; ground in the planner's short form | `battle.py` |
| 11 | Medium: `put` breaks on a quote | `No closing quotation` | `RELAY.md`, `relay.py`, `brain.py` |

`player/tests/test_review.py` has one class per finding (49 tests). Run on `583fe353`, 47 of them fail or error;
the two that pass there are controls (a same-day hold, the potion inside the limit). The rebuilt wiring suite
cannot start on `583fe353`, and its six "unplugged" tests fail there.

## What each correction is

### 1. The shared limit

`Budget.pace` now applies the account's limit to every lane. Who gives way first is the rule:

- A turn's actions and recovery calls may use the whole minute (30).
- No read takes the room of a turn's actions (25).
- Reads that only watch a fight (his turn's polls, the poll behind my actions) and the world lane leave room
  for a turn and its read (22). For that reserve alone a fight is not left unread for more than 12 s.
- When a call still has to wait: a wait in front of an action or a recovery call, or a blind wait over 12 s, is a
  `finding` event (`about: budget`). The limit is never passed silently.
- A watching read that would have to wait more than 3 s behind other calls is left out of the batch, so the relay
  never sits on action answers. A wait in front of a batch's first call is spent in the brain.
- His kit read rides a poll only when the minute has room for it.

Every turn now logs `unseen`: how long the fight had gone unread when the turn was first seen. That is the
detection delay, kept apart from `fired_after` (planning and firing).

The tests play whole fights against a stand-in game that answers only the calls each batch makes
(`test_review.py`, `Game`), and check every rolling minute of the full call ledger:

| Fight (simulated) | Turns | Most calls in a minute | Actions delayed | Longest unread | Budget findings |
|---|---|---|---|---|---|
| Starts from a hunt at its cap (20 world calls spread over the last minute), 4 minutes | 13, all acted | 24 | 0 | 13.0 s | 0 |
| The review's start: 20 world calls at once, then the fight, 3 minutes | 12, all acted | 27 | 0 | 31.5 s | 1 |
| Against an AI, as fast as the relay goes, 4 minutes | 17, all acted | 26 | 0 | 32.1 s | 2 |

What this does not do, stated plainly:

- **The review's burst still ends in one long blind stretch** (31.5 s in the simulation; 37.3 s in the review's
  exact sequence, where it was 41.7 s, now with 26 calls in the worst minute instead of 32). Twenty world calls
  at once and two quick turns leave almost nothing for the rest of the minute.
  The limit holds, no action waits, no turn is lost, and the wait is a finding. I did not add a guard against the
  burst itself: no activity sends more than 5 world calls in a batch, and a per-20-seconds cap tight enough to
  matter also delays the hunt's attack batch.
- **Against an AI the reads saturate** (32 s unread at worst). PvE is AP3; the nudge needs pacing there.

### 2. Plans the game refused or never got

- Each turn keeps what happened to its actions: `sent`, `answered`, `accepted`, `unknown` (an error answer).
- `turn_owed` decides, with no read in hand, whether a plan must go now from the last good read: yes when the
  connector refused the read or an action, when every action sent came back refused, or at T+12 s. It replaces
  the old test on `fired_at`, which a refused or undelivered plan left set.
- A plan whose answers never came back may have landed, so one read is asked for before it is sent again. The
  resend carries the version last seen, so the game's own version check keeps it from landing twice.
- `Brain.handle` keeps a copy of the world model after the results are folded in. If the tick fails after that,
  the copy is restored: what was learned stays, what was decided does not. A plan that never reached the relay
  is no longer remembered as sent, and the calls it would have made are not charged to the budget.
- After a crashed tick in a fight the relay is told to come back in 1 s, not 3.
- A planner that raises is treated as a planner with no line.

### 3. The fallback

With no line from the planner, in order: the best line this turn already had (when the battle has not moved and
none of it was refused), Defensive Stance, End Turn (`wait`). An action the game has refused is never sent again.
When all are refused, the batch is reads only and a finding says so; the turn then closes as missed.

"Best line so far" means the last line the planner returned in this turn. The planner tools print one line when
they finish, so there is no partial line to take from a run that is cut off. That is AP4's to change.

### 4. Relay and batch

- A relay's first `brain next` (no token) names it and returns one line: `brain next <relay>-<n>`. Nothing is
  taken from it yet. This costs one extra round trip per relay start.
- Every batch ends with `brain next <token>`. The brain reads only the transcript that holds that Bash call,
  only the connector calls made since the relay's previous `brain next`, and matches each once to a call the
  batch asked for (same endpoint, same input). A late result from an earlier batch, a result from another
  session, and a call the batch did not ask for are never answers. Unasked calls are counted and reported.
- No transcript carries the token: the next batch asks for each result with a `put` line (finding 11).
- A token from a relay that was replaced gets `STOP superseded`. The current relay's own stale token (a
  `brain next` run twice) gets the current line again, and no second tick.

### 5 to 11

- **5.** A spend-capped call with no price is taken to cost all the money in pocket. A large ramen's price is
  measured from the pocket before and after, and used from then on. With no profile read yet, the gate asks.
- **6.** A hold whose end is at or before its start is on the next day. A hold with its own end date
  (`... UTC to 2026-11-12 17:10 UTC: ...`, the form the live file now uses) is read, user ids included. A line
  that cannot be read, or that ends before it starts, holds.
- **7.** A turn closes as `acted` (the game's answer, or my line in the battle log), `missed` (nothing taken and
  nothing outstanding) or `unresolved` (an answer never came back or was an error, or the fight ended, and the
  log does not settle it). A turn of an earlier round that no read closed is closed when the next one opens.
  `status.json` has `turns_unresolved` beside `turns_missed`.
- **8.** See "Wiring" below.
- **9.** "Full Potion used" and "ramen bought" are written from the game's answer. A refusal by the game is a
  finding; a gate refusal and a transport error produce no item event.
- **10.** The seat is told from the first read, on either side's turn, before the first row is archived. The
  archive keeps the ground as the read carried it, with `ground_read`: `whole`, `columns`, `none on the field`,
  `not asked` or `misaligned`.
- **11.** `python3 -m player.brain put TOKEN N` reads the result from standard input. `RELAY.md` tells the relay
  to run the printed line with a quoted heredoc, one line at a time, each after the one before has returned.
  The test runs that command through `bash` with apostrophes, quotes, `$( )`, backslashes and several lines.

### Wiring (finding 8)

- The session now runs on the production `Combat` adapter. The five tool scripts it starts are stand-ins in a
  temporary folder: they record what they were given and answer in the real tools' format. The tools it imports
  (`opponent_kit`, `exam`, `harvest`, `opponents`) are the real ones, pointed at temporary folders.
- Evidence is what came out: the planner's line is the line sent; the saved kit stops the second kit read; each
  background job ran and could read the file written for it; the fight's result and turning point come from the
  real log count.
- `Unplugged` repeats the session with one production method disconnected at a time (`plan_turn`, `save_kit`,
  `_popen`, `close_fight`, `archive_state`, `turning_point`, `log_says_lost`, the harvest) and requires the
  check for exactly that model or feed to fail.
- `Inventory` takes ownership from outside the registry: the tools the player's code runs or imports, read from
  its syntax tree, must equal the tools the registry claims; every tool the design's file map keeps for AP1 must
  be owned; the three feeds the file map found running by hand (`meal_factor.py`, `validate.py`,
  `engine_fit.py`) must be listed as deferred, each with a phase and an owner.
- The inventory found one unowned tool at once: `exam.py`. It is now the model `fight_result`.

## Found while correcting (not in the review)

1. A planner line with an action the gates refuse (Flee) made the brain set the whole battle activity aside for
   60 s. The line is now planned again without that action.
2. The director's 24 h hold of 2026-11-11 was only on Duet's branch, in a form the old reader could not parse.
   It is cherry-picked (`4b7079e5`) and the form is read and tested against the repository's own file.
3. After a full poll was lost, the plain re-read was treated as if it had asked for the ground, which could
   empty the ground list. The flags now describe the read that was sent.
4. `live/tokens.jsonl` rows carry `calls`, the number of game calls in the batch, so calls per rolling minute
   can be measured from a live session.

## Did a wider assumption change?

Yes. I recommend the full relevant scope for `budget.py`, the turn handling in `battle.py`, `relay.py` and the
client half of `brain.py`; a narrow check is likely enough for `gates.py`, `recovery.py` and the archive. The
reviewer decides.

- **The budget rule.** The brief's AP1 step 3 says the battle and recovery lanes are "never paced". They are now
  delayed by one thing only: the account's own limit. Reads give way before actions. The design (section 4.6) is
  brought into line; the brief's sentence is left as written, for the director to change or keep.
- **The relay protocol.** The handshake, the tokens, and `put` over standard input. `live/client.json` and the
  batch files changed shape (`steps` instead of printed lines).
- **Files the console reads.** `turns.jsonl`: `outcome` replaces `acted`, and `unseen` and `accepted` are new.
  `status.json`: `turns_unresolved`. `tokens.jsonl`: `calls`. Item events come one batch later than before.
- **The registry.** `model` and `feed` take the tools they stand on; `defer` is new. `Combat` takes `scripts`.

## Verification on `3a154d4b`

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 202 tests`, `OK`, three runs in a row (world 6, gates 26, budget 17, battle 25, activities 18, relay 12, brain 15, wiring 15, chaos 19, review 49) |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check` | exit 0; never-list clean; 93 endpoints |
| `python3 scripts/player_allowlist.py report --check` | exit 0 |
| `python3 tests/test_planner2.py`, `test_pilot.py`, `test_integration.py`, `test_nearkill.py` (in `state/player/dauntless/tools`) | exit 0 each; `parity: 4000/4000 lines match` |
| `python3 scripts/rulings_index.py --check` | exit 0 |
| `python3 scripts/check_large_files.py` | exit 0 |
| `python3 scripts/check_no_real_name.py`, and `--commits 583fe353..HEAD` | exit 0, both |
| `python3 scripts/player_size.py` | the figures below |
| The new tests on `583fe353` (a throwaway worktree) | `test_review.py`: 47 of 49 fail or error. `test_wiring.py`: `Unplugged` 6 of 6 fail; `Wiring` and `Inventory` cannot start |
| The review's wiring reproduction (`plan_turn` and `save_kit` patched out) on the head | 7 of 15 fail |

The pilot tests write `pilot_good.py` and `fights/observed/` into the tree; both were removed after the run.

## Size (brief section 4)

| Measure | At `583fe353` | Now | AP6 budget |
|---|---|---|---|
| Player code, without tests | 2,657 lines in 19 files | 3,030 lines in 19 files | to be set from the AP5 total |
| Tests | 1,914 lines | 2,957 lines | - |
| Largest file | `battle.py`, 389 | `battle.py`, **484** | 400 |
| Largest function | `combat.py:plan_turn`, 38 lines | `battle.py:_tick`, 40 lines | 60 |
| Functions over 12 branches | 10 | 9: `battle.py` `_tick` 17, `_my_turn` 15, `_no_read` 14, `_absorb` 13; `combat.py:plan_turn` 16; `calls.py:ground_cols` 15; `gates.py:do_not_attack` 15; `brain.py:_compose` 14; `relay.py:find_transcript` 13 | 12 |
| Config constants (`config.py`) | 47 | 47 | 15 knobs |
| Control settings | 9, and the planner-choice switch | the same | - |
| Constants added elsewhere | - | `budget.py`: `TURN_ACTIONS` 5, `BLIND_MAX` (twice the longest poll gap). `relay.py`: `FIND_TAIL`, `RECENT`. `battle.py`: `EMERGENCY` | - |
| Shipped switched off | nothing | nothing | - |

`battle.py` is now over AP6's file budget. I did not split it in this pass: the review asked that the correction
not become a consolidation. It is AP6 debt, with the nine functions above.

## Known limits

1. A tick that crashes every time (not once) still leaves the turn without an action; the crash is logged and
   the relay comes back each second. Only the planner call has a guard of its own.
2. A refused resend is banned for the rest of the fight like any refusal (the pilot's rule). If a plan had
   landed and its answers were lost, the resend's first action is banned though nothing was wrong with it. The
   one read asked for before a resend makes this rare; it is not removed.
3. The spend bound assumes the game pays a purchase from the pocket, not the bank. No game source is in this
   checkout to confirm it.
4. `wait` as End Turn on my own turn is taken from the battle logs (players' `wait` lines) and the pilot's use of
   it to nudge an AI. It has not been sent on a turn of mine.
5. The ground is read as ten columns, so the archive's ground has those columns only.
6. After a crashed tick the same read can be archived twice.
7. In `put` mode no token use is logged, so `tokens.jsonl` has no rows for those batches.
8. A confirmed action is "no error and no refusal text". The game also returns the new battle version with each
   action (`battleUpdate.version`, per the pilot's notes). Reading it would make the proof exact; it changes a
   select the pilot-parity test compares, so it is left as a proposal.

## The live session (unchanged in purpose; the steps changed)

The review asks that the live gate wait for these corrections to be verified. It remains the director's to start.

1. Duet stops the pilot. The brain and the pilot never both run.
2. `python3 -m player.brain set mode=hunt paused=false end_session=false director_mode=false`
3. A Haiku relay whose whole prompt is `player/RELAY.md` runs `python3 -m player.brain next`. Its first answer is
   one line (the handshake); the batches follow.
4. A replaced relay ends itself on `STOP superseded`. A relay that ends on `STOP rotate` is replaced at once.
5. To end: `python3 -m player.brain set end_session=true`.

What the session must record, and where:

| The review asks for | Where it is |
|---|---|
| Actual calls per rolling minute | `live/tokens.jsonl`: `at` and `calls` per batch. `status.json` `budget` |
| Observation-to-action latency | `live/turns.jsonl`: `unseen` (detection) and `fired_after` (planning and firing) |
| Unresolved deliveries | `turns.jsonl` `outcome: unresolved`; `status.json` `turns_unresolved`; findings `about: relay` |
| Confirmed missed turns | `status.json` `turns_missed`; `stall` events `about: missed_turn` |
| Relay tokens per batch, turn and hour | `live/tokens.jsonl`; `status.json` `tokens`; the first row's `context` is the starting size |
| Column alignment (from the first handoff) | findings `about: selects` |
| Budget pressure | findings `about: budget` |

The gate is 0 missed turns. An unresolved turn is not a played turn: each one is to be explained from the log.

## Live-game statement

Zero live requests in this correction: no connector call, no read, no write, no gameplay, no credential. Every
test is socket-free. The relay protocol and the `put` path have never been driven by a real relay.

## Open decisions

For the director:
1. The brief's "never paced" for the battle and recovery lanes: keep the sentence, or change it to the rule above.
2. End Turn (`wait`) as the last resort when Defensive Stance is refused: allowed, or should the turn rather
   close with reads only.
3. Still open from before, needed for AP2: spend caps, the scope of equipment changes beyond PvP 2, and the day
   boundary of the daily level transfer.

Not begun: AP2 and everything after it.
