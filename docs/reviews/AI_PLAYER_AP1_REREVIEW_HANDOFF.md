# AI player overhaul, phase AP1: correction handoff after the re-reviews

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the re-review of
`c225ed36` ("request changes": two high findings, two medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1 (fast-forwarded to the reviewed commit, then the corrections; one AP1 branch again)
Reviewed: c225ed36f8ca4f1631d97d5f267546a9eb46f10d (it was the head of fable/ai-player-rulings)
Reviews: docs/reviews/AI_PLAYER_AP1_LIVE_RULINGS_REVIEW.md on chatgpt/review-ai-player-ap1-live-rulings @ 406f674a
         docs/reviews/AI_PLAYER_AP1_CORRECTION_REVIEW.md on chatgpt/review-ai-player-ap1-correction @ adeb7807
         (evidence; not merged). The second reached me only with the first: its three findings are findings 1 to 3.
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
fable/ai-player-ap1-live @ a9cec9d8 and fable/ai-player-rulings @ c225ed36 are ancestors of this head and are
not moved.
```

## Disposition

All four findings are **confirmed**. Each was reproduced on `c225ed36` with the review's own script, unchanged,
and each script now gives the corrected result.

| # | Finding | The review's script on `c225ed36` | Now |
|---|---|---|---|
| 1 | High: the limits are not held by the clock the calls really ran on | 31 real calls in a minute; 24 in the world lane | 28 and 20 (30 with an even 0.4 s latency) |
| 2 | High: an unusable read bypasses the T+12 fallback | no action at T+1, T+12, T+15, T+20, T+60 | Defensive Stance at T+1, End Turn at T+12 (both planned actions were refused in that script) |
| 3 | Medium: a waiting client overwrites its replacement | the old relay's name stored again; it prints 4 calls; the replacement is stopped | the replacement keeps its name and gets the batch; the old one prints `STOP superseded` and no call |
| 4 | Medium: a proof profile in a new battle sends the old fight's potion | `item.consume`, `profile.getUser`; no battle state | the new fight's opening read; battle state is B2; no potion |

`player/tests/test_rereview.py` holds one class per finding (17 tests). On `c225ed36`, 14 of them fail or error;
the other three are controls.

## What each correction is

### 1. The call ledger is kept on the safe side of real time (`budget.py` `settle`, `pace`; `brain.py` `handle`)

The ledger wrote each call down at a predicted time and released it sixty seconds after that prediction. Now:

- **Admission.** A call is admitted at the earliest moment it could run: the batch's start and the waits in front
  of it. No time is allowed for the calls themselves, so a relay faster than any guess cannot get ahead of it.
- **Release.** When the batch is back, each of its calls is moved to when it did run: the time of its answer,
  or the moment the batch came back when it has no answer. It leaves the minute sixty seconds after that.
- `pace` settles whatever is still out before it schedules anything, so the rule holds even when the budget is
  driven alone, as in the review's probe.

A call's ledger time is therefore never earlier than its real time, and a new call is never admitted later than
it can run. The price is some capacity: a call with no answer is held until a minute after its batch returned.

The simulated fights now carry their own clock of when each call ran, with uneven latencies, and are held to the
limit on that clock as well as on the ledger:

| Fight (simulated, uneven call latencies) | Turns | Most real calls in a minute | Actions delayed | Longest unread |
|---|---|---|---|---|
| From a hunt at its cap, 4 minutes | 13, all acted | 22, the hunt's calls counted | 0 | 13.7 s |
| The burst of twenty world calls, then the fight | 9, all acted | 27, the burst counted | 0 | 36.6 s, with a finding |
| Against an AI | 15, all acted | 24 | 0 | 21.4 s |

### 2. A read that cannot be used is no read (`battle.py` `_usable`, `_tick`)

A read is usable when it has the round, the version, whose turn it is, and one value per fighter in every fighter
column. One that is not is neither planned on nor answered with another read on its own: it goes down the same
path as a tick with no read at all, where the turn's clock and the last good read decide. The last good read is
left as it was. The finding is written once, then every tenth time.

Found on the way: a read missing the version or the round raised inside the tick. The brain's undo then put the
same read back, and the tick failed on it again, for ever. A read whose tick has failed twice is now dropped
(`brain.py` `handle`); after one failure it is kept, so a one-off crash still costs nothing.

### 3. Relay ownership is serialised (`brain.py` `_client`, `next_batch`, `_greet`, `_exchange`, `_owed`)

- `live/client.json` is read, used and written under a lock (`live/client.lock`), one `brain next` at a time. A
  handshake waits for an exchange with the brain that is under way.
- A batch the brain has made is written into `client.json` before the brain-side wait. The wait is spent with the
  lock released. When it is over, the lock is taken again and the owner is read again: the batch goes to whoever
  owns the relay then. A relay that was replaced during the wait prints `STOP superseded` and no call. The
  replacement's first hand-in is given that batch, with no second tick.
- A batch that has waited more than 10 s for a relay is not handed on; the brain is asked afresh.

### 4. Straight from one fight into another (`battle.py` `_left`, `_open`)

When my profile is out of the battle the brain was fighting and already in another one, the old fight is closed
and kept, its result is the log's own HP count, the potion that would have gone with its closing batch is
dropped, and the new fight is opened in the same tick with its opening read. Out of combat, nothing changes: the
closing batch carries the potion.

## The review's notes on the token figures: accepted

- "About 1,001k per fight turn" and the console's 937,607 used different denominators. The console divided by
  14 groups, two of them a fight's batches with no round. `relay.py` `tokens_summary` now counts only batches
  tagged with a round; on the session's log it gives 1,001,117 over 12 rounds.
- "Every batch is one model request" was an approximation: five of the 69 batches had more than one.
- The 5k birth context, the light-poll saving and the per-round restart saving are scenarios computed from the
  old run's log. Nothing about the corrected player's token use has been measured.

## Did a wider assumption change?

Yes, in two places; I recommend the full relevant scope for both.

- **The ledger.** Entries carry a third field while their batch is out. Times mean "no earlier than real" from
  here on. Every budget test and all three simulations were rerun on it.
- **`client.json`.** It has a `pending` batch, and a lock beside it. `next_batch` is now three functions.

The battle changes (findings 2 and 4) are local to `_tick`, `_profile` and the new `_left`.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 241 tests`, `OK`, three runs in a row (rereview 17, live 20, review 49) |
| The review's four scripts, unchanged | the figures in the first table |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits) | exit 0 each |
| `test_rereview.py` on `c225ed36` (a throwaway worktree) | 14 of 17 fail or error |

## Size

Player code 3,257 lines in 19 files (`c225ed36`: 3,142); tests 3,567 lines. `battle.py` is 574 lines and
`brain.py` 447 (AP6 budget 400). Ten functions branch more than 12 ways, the same ten as at `c225ed36`; the most
is 18 (`battle.py` `_tick` and `_my_turn`). Config constants unchanged (48). Nothing ships switched off. This is
AP6 debt; `battle.py` should be split before AP2.

## Known limits

1. A batch that was given up on is settled at the moment the next one is scheduled. A relay that had been
   replaced and was still running that batch could make its last calls after that moment.
2. A second read that fails a tick twice is dropped silently apart from `crash.log` and the error events.
3. The lock is a file lock on one machine. The brain and its relays run on one machine by design.
4. Everything is proven on tests and simulations. No real relay has driven the token protocol or the lock.
5. The limits listed in the correction and live handoffs stand.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- The three token decisions (light polls on his turn; short-lived relays started by a script; whether to keep
  archiving his turn's opening state). The review asks that finding 2 be fixed before light polls and finding 3
  before scripted relays; both are fixed here. Rotation inside a fight would also need a change to
  RUL-2026-11-11-151 ("never in a fight").
- Duet's three relay transcripts from the live session.

Not begun: AP2. No live run is proposed on this head until it has been verified.
