# AI player overhaul, phase AP1: handoff and findings

Contract: `state/prompt_ai_player_overhaul.md` section 3 (AP1), as updated at 6353a4b4 (AP6, AP7, and the two
engineering rules that apply from AP1 on). Design: `docs/design/AI_PLAYER_OVERHAUL.md`.
Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-11.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Base: 3a8a4c3fa8a66ad60bcf5708b327ab0e37c4bdea (fable/ai-player-base: AP0 with the director's rulings applied)
Merged in: fable/ai-player-overhaul-brief @ 6353a4b4e5719aaa5f8e983452f2f85768a8d61c (docs only)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Integration target: main (it differs from the base in state/run_lock.json only)
Duet's branches: fable/pilot-planner-fixes @ dacdf7e2 and fable/pvp-engine-harness @ f6e8c860, both already in the
                 base; neither was touched
```

## Objective

The brain and its hands: one resident process that makes every decision, a relay contract a small model can
follow, the call budget and the battle turn clock, the gates, and the pilot's PvP hunt, battle and recovery as the
first activities. The code half of the AP1 gate (chaos and wiring tests green) is met. The live half (one
director-started PvP session on a Haiku relay) has not been run.

## What was built, against the brief

| Brief AP1 | Where | State |
|---|---|---|
| 1. Brain: resident process, world model saved after every result, scheduler, arbiter, registry | `player/brain.py`, `world.py`, `registry.py`, `goals.json` | Built. One brain per account, by file lock. `brain next` starts it when it is not running and answers in-process if it has to. |
| 2. Relay prompt under 300 words | `player/RELAY.md` (262 words) | Built. |
| 2. Trimmed responses | `player/calls.py` | Every call has a select; lists are read as columns and every column read checks its lengths; the effect list is read whole. Alignment is **not verified live** (see the live session). |
| 2. Fewer batches | `battle.py`, `pvp_hunt.py`, `travel.py`, `watch.py` | His turn is polled at 3, 4, 5, then 6 s; every leading wait is spent inside `brain next`. |
| 2. Rotation by context size | `relay.py should_rotate` | Built, with one change: see deviation 1. Never in a fight. |
| 2. Watchdog | `brain.py watchdog` | A relay that has not come back 10 s after its batch should be done is a `stall` event, raised once. |
| 2. Token log | `relay.py`, `live/tokens.jsonl` | Per batch from the relay's transcript, tagged with battle and round; summed per fight turn and per hour in `status.json`. |
| 3. Budget lanes and turn deadline | `player/budget.py` | Battle and recovery never delayed; world capped at 20 a minute; T+12, T+15, T+20; 1.2 s between actions; `live/turns.jsonl`. |
| 4. Gates, a test per rule | `player/gates.py`, `tests/test_gates.py` | 26 tests. |
| 5. Core activities ported | `player/activities/` | `battle`, `pvp_hunt`, `recovery`, plus `session` (wake), `travel`, `watch` and `harvest`, which the pilot's loop also did. |
| 6. Wiring test | `tests/test_wiring.py` | Fails when a module is not registered, an activity is never chosen, a model or feed leaves no trace, or the code can send an unlisted endpoint. Each was broken on purpose and the test failed. |
| 7. Chaos tests | `tests/test_chaos.py` | 19 tests. |
| Console data from AP1 on (brief AP7 section 1) | `player/console.py`, `world.py event` | `live/status.json`, `live/events.jsonl`, `live/control.json`. |

Not begun: AP2 and later. No upkeep (training, restock, repair, equipment, bank), no run-lock claim by the brain,
no missions or errands, no daily summary. `pilot.py` and its tools are unchanged and still run Duet's live pilot.

## Verification

Run on the head, from the repository root unless a folder is given.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 137 tests`, `OK` (world 6, gates 26, budget 13, battle 24, activities 18, relay 11, brain 15, wiring 5, chaos 19) |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 39 tests`, `OK` |
| `python3 scripts/player_allowlist.py check` | exit 0; never-list check clean; the code scan now covers `player/` |
| `python3 scripts/player_allowlist.py report --check` | exit 0 |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `python3 scripts/rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commit messages) | exit 0 each |
| `python3 scripts/player_size.py` | the figures under "Size" |

The `-W ignore::ResourceWarning` flag only hides warnings from `harvest.py` in the pilot's tools, which opens files
without closing them.

Checks made by hand, not committed as tests:
- The wiring test was broken four ways (an unregistered module, an activity never chosen, a feed with no trace, an
  unlisted endpoint in `player/calls.py`). It failed each time and passes clean.

**Parity with the pilot.** `tests/test_battle.py` runs the pilot's own `battle_tick` and the brain on the same
logged state and holds the two batches equal, call for call (endpoint, input, select, waits): my turn with the real
planner, his turn, and an AI's turn. The first run of that test found one difference (the brain asked for the
ground list one poll earlier than the pilot), which was removed.

## Size (brief section 4: keep complexity visible)

| Measure | AP1 | AP6 budget |
|---|---|---|
| Player code, without tests | 2,630 lines in 19 files | to be set from the AP5 total |
| Tests | 1,885 lines | - |
| Largest file | `player/activities/battle.py`, 373 lines | 400 |
| Largest function | `player/combat.py:plan_turn`, 38 lines | 60 |
| Most branching function | `battle.py:_absorb`, 17 | 12 |
| Functions over 12 branches | 10: `battle.py` `_absorb` 17, `_tick` 16, `plan` 16, `_my_turn` 13; `combat.py:plan_turn` 16; `calls.py:ground_cols` 15; `gates.py:do_not_attack` 15; `brain.py:_compose` 14; `relay.py` `read_results` 14, `find_transcript` 13 | 0 |
| Third-party dependencies | none | none |

The branching count is strict (every boolean operand and comprehension counts). `scripts/player_size.py` prints all
of this.

**Settings a person can change (9, all in `live/control.json`):** `paused`, `mode`, `director_mode`, `activities`,
`goal_weights`, `spend_caps`, `do_not_attack`, `answers`, `end_session`. `player/goals.json` holds the default goal
weights (4 numbers). One switch file is carried over from the pilot: `fights/live/planner_choice` (`turn` or
`planner2`), which goes when AP4 leaves one planner. `player/config.py` holds 47 constants; none is read from the
environment except the two test folders (`TNR_PLAYER_LIVE`, `TNR_PLAYER_FIGHTS`), `TNR_TRANSCRIPT`,
`TNR_PLAYER_NO_DAEMON`, and Claude Code's own `CLAUDE_CONFIG_DIR` (where transcripts live).

**Switched off:** nothing ships switched off. Two things are refused or empty until their phase: the modes `farm`
and `rest` are refused as settings (AP3, AP2), and `status.json` `battle.his_windows` is null until the planner
states his windows (AP4).

## Deviations and choices for the reviewer to attack

1. **Rotation counts growth, not size.** The brief says relays restart by context size, default 60k tokens. The
   Haiku relays used in AP0 started at about 65k tokens before their first call (the agent's own prompt and tools),
   so an absolute 60k would rotate every relay at once. `should_rotate` fires when the context has grown 60k past
   the relay's first batch, or at 150k whatever it started at. A purpose-built relay with a small prompt behaves
   as the brief intended. The live session measures the real starting size.
2. **"Never paced" has one exception by design.** My turn's batch, the fight's opening read and its closing batch
   are never delayed. How often his turn is polled is scheduled, and keeps 8 calls of the 30 free for my turn.
   Without that a fast relay would hit the limit as my turn starts.
3. **One message, in order.** A batch is several tool calls in one message, run in the order printed (the pilot's
   proven contract; action versions depend on it). The 1.2 s gaps between actions are short sleep lines in the
   batch. Waits in front of a batch are spent in `brain next` and cost the relay nothing.
4. **T+12 s.** A refused read on my turn is not waited for at all (Duet's rule, kept). A read that simply does not
   come back is asked again until T+12 s, then the turn is planned from the last good read.
5. **Four activities beyond the three the brief names:** `session` (only waking), `travel`, `watch` and `harvest`.
   Each is something the pilot's `world()` did; without them the hunt cannot run.
6. **The harvest is on,** as in the pilot, behind the gate `study_only` (never in a fight). AP0 finding 4 (may live
   play use what it learns about a named opponent) is still open; the director can switch the activity off in
   `control.json` meanwhile.
7. **First start takes over from the pilot:** the Full Potion's current user-item id and the two "do not attack
   again yet" lists are read once from the pilot's `fights/live/pilot.json`. Without restock (AP2) the brain has no
   other way to know the potion's id.
8. **Results are matched by time,** as in the pilot: everything in the relay's transcript after the last batch was
   issued. Call ids are not echoed.
9. **A turning point** in the `fight_end` event is the round with the widest gap between HP I lost and HP he lost,
   from the log's own HP count. The engine-based review stays in `postmortem.py` until AP4.
10. **One event kind beyond the AP7 list:** `finding` (a refused call, a late or missed turn, columns that do not
    line up). The console's Decisions tab is to show recent findings.
11. **The goal weights' numbers** (1.0, 0.7, 0.45, 0.45) are mine; the order is the director's (RUL-2026-11-11-149).
    In AP1 only one goal-class activity exists, so no weight changes a live decision yet; a test with two shows the
    weight deciding.
12. **Items I carry none of** are not known to the brain until AP2's restock. The planner may pick one once; the
    game refuses it and it is banned for that fight (the pilot's rule).

## The live session (the second half of the AP1 gate; the director starts it)

Duet stops the pilot first: the brain and the pilot must never both run.

1. `python3 -m player.brain set mode=hunt` (and `director_mode=true` to play the fights by hand).
2. Start a Haiku relay whose whole prompt is `player/RELAY.md`. It runs `python3 -m player.brain next` and loops.
   The run lock is claimed by Duet as `player`, as today: the brain does not claim it until AP2.
3. To end: `python3 -m player.brain set end_session=true`. The relay gets `STOP` once no fight is on.

What the session must record:
- **Missed turns: 0** (`status.json` `turns_missed`; `live/turns.jsonl` has every turn's timing).
- **Tokens:** per batch, per fight turn and per hour (`live/tokens.jsonl`, `status.json` `tokens`), and the relay's
  starting context size. These are the baseline for the targets.
- **Column alignment:** any `finding` event with `about: selects` means a column read did not line up. This is the
  first live check that the selects stay aligned (brief AP1 step 2); AP1 made no game read.
- Any `error` or `stall` event, and `live/crash.log` if it exists.

## Live-game statement

- Live requests made to build or test AP1: none. The four `getEndpointSchema` reads at 20:22 UTC belong to the AP0
  corrections on the base branch.
- Game writes, gameplay actions, credentials: none.
- Not performed: any run of the brain against the game; any relay run with a real model; any browser check.

## Open decisions

- **AP0 finding 4** (the harvest in live play): still open.
- **Rotation** (deviation 1): confirm growth past the first batch, or name another rule.
- Due with their phases, unchanged: equipment-swap scope and spend caps (AP2), PvE auto-combat scope and what
  counts as a rare item (AP3), further modes (AP5), the AP6 size cap, push notifications on by default (AP7).

## Known debt

1. Ten functions branch more than AP6's budget of 12 (the list is under "Size").
2. `player/relay.py` and `scripts/player_allowlist.py` each carry the same 25 lines that read a tool result too
   large for the conversation from its saved file.
3. No daily summary event; the console can build it from `status.json` and `events.jsonl`.
4. No workflow in `.github/workflows` runs the player tests.
5. The reason the hunt gives for passing over a player who is not awake is now one label ("asleep or away"); the
   pilot gave the status itself.
