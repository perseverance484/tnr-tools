# AI player overhaul, phase AP1: correction handoff after the review of 0d10b7c6

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`0d10b7c6` ("request changes": two high findings and one medium left open, the fourth closed).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 0d10b7c66fd40fc6c3404e030984f1c5cf7ec059
Review: the director's summary of 2026-11-12. The report and its reproducers are NOT on the remote: a fetch at the
        time of writing shows the same three review branches as before (chatgpt/review-ai-player-ap1 @ e94bf21c,
        -correction @ adeb7807, -live-rulings @ 406f674a). The reproductions below are therefore mine, built from
        the summary, and not the review's scripts.
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

**First thing to verify:** run the review's own reproducers, unchanged, on this head. I could not.

## Disposition

The three open findings are **confirmed** and fixed. The fourth was closed by the review and is untouched.

| # | Finding | My reproduction on `0d10b7c6` | Now |
|---|---|---|---|
| 1 | High, `budget.py`: a status write during a long batch drops ledger entries that are not settled yet | 31 real calls in a minute while the ledger says 30 | 27 |
| 2 | High, `battle.py`: a read whose active id is no fighter passes; a null longitude reaches an action | no action at T+1, T+12, T+15, T+20, T+60, and the last good read overwritten; `wait` sent with `longitude: None` | Defensive Stance at T+1, End Turn at T+12, the last good read kept; the tile sent is the last good read's |
| 3 | Medium, `brain.py`: a batch that expired and its recomputation share a number, so an older waiter can publish the old one | the older call prints the obsolete batch; the fresh one is discarded | the older call prints only the next `brain next` line; the fresh batch goes out |
| 4 | Medium: a proof profile in a new battle | closed by the review | unchanged |

`player/tests/test_rereview.py` has one class per finding (G1 to G3, 7 tests). On `0d10b7c6`, 6 fail or error;
the seventh is a control.

## What each correction is

### 1. A call that is still out stays in the ledger (`budget.py` `_hist`)

Every reader of the ledger dropped entries older than a minute, by their admission time. During a batch longer
than a minute the watchdog's status write did that to calls whose real time was not known yet, so `settle` found
nothing to move. Now an entry marked as out is never dropped for its age. It leaves a minute after the time
`settle` gives it.

### 2. What a usable read is (`battle.py` `_usable`)

A read is usable when the round and the version are numbers; every fighter column is a list with one value per
fighter and none missing; ids and names are text, health and position are numbers; the fighters are distinct; and
the fighter whose turn it is, is one of them. Any other read is not planned on and does not replace the last good
read: the turn's clock and the last good read decide, as when no read came back.

### 3. A batch is known by its own id (`brain.py` `_exchange`, `_owed`, `next_batch`)

Each batch the brain makes gets an id of its own. A call that waited prints its batch only when the batch owed
is still that one. A batch dropped for its age takes its number with it: the recomputed batch gets the next one.

## Found while correcting (not from the review)

Three reviews in a row each found one more gap in the same three places. So I searched them for the next one
before freezing. All of these are fixed, with tests in the two `Swept` classes (9 tests; all fail on `0d10b7c6`).

| Area | Gap | Fix |
|---|---|---|
| Ledger | Calls the relay made that no batch asked for were reported but never counted | `Budget.stray`: they are in the ledger, in a lane of their own, against the 30 |
| Reads | A fighter, log or ground column that came as one value and not a list raised inside the tick | `calls.py` `columns`, `ground_cols`; `battle.py` `_tick`: such a read is one whose columns do not line up |
| Reads | A log line with no id, no fighter or no round was taken into the fight's log as it was | `calls.py` `log_rows`: that log read is dropped, with a finding |
| Reads | An effect list or a whole ground list that was not a list raised; so did an effect whose `timeTracker` was not an object | `battle.py` `_absorb`, `_ground`; `combat.py` `live_effects`: taken as not sent |
| Planner | A planner's line with an action that had no id, no name or no numeric tile was sent as it was | `battle.py` `_sendable`: such a line is no line, and the fallback takes over |
| Brain | One activity that raised on a result stopped every later activity from seeing the batch | `brain.py` `handle`: each activity is caught on its own, with an error event |
| Brain | A world activity whose plan raised stopped the player on every tick after | `brain.py` `_plan`: it is set aside for 60 s and the next activity is asked. A fight's plan still fails the tick, which is undone |
| Client | A second `brain next` for the same batch handed the same results to the brain again | `brain.py` `_exchange`: a batch's results go in once |

The read sweep: every field of a battle read and of a log read, the effect list and the ground, each replaced
by every kind of JSON value, shortened, lengthened, nested, or left out, on my turn and on his. Of 1,128 cases,
120 raised or wrote an error on `0d10b7c6`; none does now. The half on my turn is committed as
`SweptEveryShapeOfARead`: nothing raises, no error is written, an action still goes, and every action sent has a
real tile and version.

## Did a wider assumption change?

Yes. I recommend the full relevant scope again for the budget and the client, and the read intake of `battle.py`.

- **The ledger.** `used()` now counts calls that are out for as long as they are out. During a long batch it
  reads higher than before. A stray call has a lane of its own.
- **`client.json`.** `pending` carries an `id`; `handed` names the batch whose results have gone in. A sequence
  number can now be skipped. The relay's contract (`player/RELAY.md`) is unchanged.
- **Reads.** The rule is stricter than any read the old code refused. A read it turns down costs no action (the
  last good read is planned on at T+12 at the latest) and writes a finding, `about: selects`.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 257 tests`, `OK`, three runs in a row (rereview 33, live 20, review 49) |
| `test_rereview.py` on `0d10b7c6` (a throwaway worktree) | of the 16 new tests, 9 fail and 6 error; one is a control |
| My three reproductions; the earlier reviews' four scripts, unchanged | the first table; 28, 30 and 20 calls, stance then End Turn, the replacement keeps its name, B2 opens with no potion |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

## Size

Player code 3,322 lines in 19 files (`0d10b7c6`: 3,257); tests 3,840 lines (3,567). `battle.py` is 598 lines
and `brain.py` 473 (AP6 budget 400). Twelve functions branch more than 12 ways (`0d10b7c6`: ten): `brain.py`
`handle` (13) and `calls.py` `log_rows` (17) are new on the list, and `calls.py` `ground_cols` went from 15 to
18. Config constants unchanged (48). Nothing ships switched off. This is AP6 debt, and it grew: the checks were
added where the values are read. `battle.py` should be split before AP2.

## Known limits

1. The review's report was not available to me (see the top). A reproducer in it may test something my
   reproduction does not.
2. The kinds `_usable` asks for (text ids and names, numeric health and position) are those of the saved fights
   and fixtures. If the game ever sends one otherwise, every read is turned down and the fight is played from the
   turn's clock: the first live run must be checked for `about: selects` findings.
3. A stray call is written down when its batch came back, which is later than it ran. That is the safe side.
4. A world activity whose plan keeps failing is tried again every minute, with an error event each time. Nothing
   escalates it.
5. Between the brain's answer and the write of `client.json` (a few milliseconds) a killed `brain next` can still
   leave its results to be handed in a second time.
6. The limits in the earlier handoffs stand. Everything is proven on tests and simulations; no real relay has
   driven the token protocol, the lock, or the agent file.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- The three token decisions (light polls on his turn; short-lived relays started by a script; whether to keep
  archiving his turn's opening state).
- Duet's three relay transcripts from the live session.

Not begun: AP2. No live run is proposed on this head until it has been verified.
