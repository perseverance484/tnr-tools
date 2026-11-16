# AI player overhaul, phase AP1: correction handoff after the review of c0006266

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`c0006266` ("request changes": two high findings and one medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: c0006266a128cca68296e4fc77863c8bd62f3096
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW2_REVIEW.md on chatgpt/review-ai-player-ap1-rereview2 @ c9e7a1e6
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

All three findings are **confirmed**. Each was reproduced on `c0006266` with the review's own script, unchanged
(its appendices B1 to B3), and each script now gives the corrected result. The review's scripts for the three
earlier findings (A1 to A3) still show them closed.

| # | Finding | The review's script on `c0006266` | Now |
|---|---|---|---|
| 1 | High: a new log line with an object for an action stalls the fight's tick for good | no action at T+1, +2, +12, +15, +20, +60; six crashes | actions at T+1, T+12 and T+20, as in the script's own control; no crash. (The script's assertion that no action goes now fails) |
| 2a | High: a replaced relay that goes on with its batch | 31 real calls in a minute, the ledger says 30 | 30 |
| 2b | High: answer times that are wrong but can be read | 24 world calls in a minute at a skew of -100 s; 20 with honest times | 20 and 20 |
| 3 | Medium: a client that dies before its receipt is saved | results applied `[1, 1]` | `[1]` |

`player/tests/test_rereview2.py` has one class per finding (H1 to H3, 16 tests) built on those scripts. On
`c0006266`, 13 fail and 3 error. The three errors are tests of names that did not exist there (`LOOSE_FOR`,
`Budget.ended`, `own_clock`); they prove nothing about the old code.

## What each correction is

### 1. A log line is whole before it is kept, and a tick that keeps failing still plays the turn

Two changes, because the finding has two halves.

- **The line** (`calls.py` `log_rows`, `_line`). A line is taken only when its id is text or a number, its
  round a number, its fighter and its action text. Its effect texts are text or the line has none. All 582 lines
  of the 22 saved fight logs are of those kinds; none has an empty action, so no sentinel is kept. A read with
  one line that fails is dropped whole, with a finding, before anything of it reaches the fight's state.
- **The tick** (`brain.py` `_undo`, `_last_resort`; `battle.py` `last_resort`). Whatever makes a fight's tick
  fail, the second failure in a row now sends what the turn is owed: the best line the turn already has, or a
  basic action, from the last good read, with a plain read behind it. It uses only the fields `_usable` has
  checked. A good read that arrived with the failing tick is used, so a later turn is seen too. This is the
  part that does not depend on guessing the next bad value. Every such tick is written to `crash.log` and the
  events.

### 2. The ledger moves a call only on evidence of the brain's own clock (`budget.py`)

A call is now **out** (issued), **settled** (its relay came back with the batch), or **loose** (its relay was
replaced before it came back).

- **2a.** A batch that is given up is no longer taken to have run. Its calls are loose and count in every
  minute. They are settled when the replaced relay comes back: it is told to stop, and the client notes the
  moment for the brain (`brain.py` `_greet`, `Budget.ended`). The client says which case a request is: the relay
  that had the last batch is back, or a new relay is asking while the last batch is still with the old one.
- **2b.** An answer's time from the relay's transcript is not used any more. Every call of a batch is counted
  from the moment its relay came back, by the brain's clock. Only a result handed in with `brain put` carries a
  time of the brain's own clock; it is used when it lies between the call's admission and now.

**One thing here is my judgement and not what the review asked for.** The review asks that unresolved work be
kept "until completion or effective cancellation is established". For a replaced relay that never comes back,
nothing can establish either: no line in a batch can take back a call already printed. I hold such calls for
`LOOSE_FOR` (900 s) and write a finding when the hold ends. Without an end, every relay that dies in the
middle of a batch would cost its calls for the rest of the session. The alternatives are to hold for ever
until the operator says the relay is dead (a new command), or a hook on the relay's connector tool that asks
the brain before each call (true cancellation; a new mechanism I cannot test in this container). It is one
constant; I would like the reviewer's ruling on it.

### 3. A request is answered once (`brain.py` `answer`, `_answered`, `_receipt`)

Every request carries its relay's name and its number. The brain keeps the answer in the world model, written
in the same save as everything the request changed. The same request made again gets that answer, with what is
left of its wait, and nothing is applied. A request older than the last one answered for the same relay is
dropped. A request whose tick crashed is remembered too. The client's own marker (`handed`) stays: it stops a
relay that asks again later from sending the same results under a new number.

## Found while correcting (not from the review)

Four reviews have each found one more gap beside the last. I ran two sweeps before freezing: every field of a
log line never seen before, and every field of a profile read and of an answer to an action, each as every
kind of JSON value. All of these are fixed, with tests in `SweptBesideTheFindings` (7 tests; on `c0006266` 4
fail, 2 error because the old code raises, and one is a control).

| Gap | Fix |
|---|---|
| A profile read with a pocket or bank that was not an amount failed before any other result of its batch was read. On my turn the answers and the fight's read beside it were lost: no action | `world.py` `_profile`, `_unfit`: a profile is checked before it replaces the last one. One that fails is dropped with a finding |
| A battle id of the wrong kind in a profile opened a fight that could not be read | The same check |
| The day of a spend was the result's time. A transcript line with no time on it began the day anew in 1970, and the day's spend with it (the 50M rule counts by that day) | `world.py`: the brain's own clock |
| An answer to an action that was not an object raised, and the fight's read behind it in the batch was not taken | `battle.py` `on_result`, `_acted`: each answer on its own; such an answer counts as unknown |
| An activity that failed while saying whether it can act failed every tick | `brain.py` `rank`: set aside for 60 s like one whose plan failed. The fight is never set aside |
| A status file that could not be written cost the batch | `brain.py` `_record`: an error event, and the batch goes |
| A batch file left under the next number (another life of the folder) was printed as the relay's batch | `brain.py` `_exchange`: removed before the request is made |
| A relay that was replaced before it ever asked came back with a token of the same number as the batch another relay holds | `brain.py` `_greet`: only a relay that had a batch can report one over |

## The review's notes on the tests

- **The log sweep changed lines the fight already had.** Right. `H1` sweeps a line with a new id, through
  `brain.answer`, at the review's six moments, with the effects as texts and whole. The old sweep's docstring now
  says what it does not cover.
- **`assertTrue(watchdog() or True)`.** Replaced: the test sets the relay state as the brain does and asserts
  that the stall was raised once.
- **G3 wrote a made-up batch into `client.json`.** The review's two-thread script (A3) is now a test in G3:
  real expiry, real second request, nothing written by hand. It passes on `c0006266`, as the review found.
- All H tests that need the crash handler go through `brain.answer`.

## Did a wider assumption change?

Yes, in three places. I recommend the full relevant scope for each.

- **The ledger.** Three states in place of two. `settle()` with no batch now means "given up", not "back". No
  transcript time is used. `used()` counts loose calls.
- **The request between `brain next` and the brain.** It now says who asks (`relay`), whether the last batch
  is lost (`lost`), which replaced relays have come back (`ended`), and whose clock the results' times are
  (`clock`). `client.json` keeps `gone` and `ended`. The world model keeps one receipt (`relay.answered`).
  `Brain.handle` takes the request as `ask`. The relay's contract (`player/RELAY.md`) is unchanged.
- **Failure in a fight.** A second failure in a row now acts at once, where it used to wait for the next tick
  that worked. Reads other than the fight's are checked before they are kept.

What this costs, on the three simulated fights of `test_review.py` (uneven call latencies; the game's own
clock):

| Fight | Turns, all acted | Most real calls in a minute | Actions delayed | Longest unread |
|---|---|---|---|---|
| From a hunt at its cap, 4 minutes | 14 (`c0006266`: 13) | 23 (22) | 0 | 16.4 s (13.7) |
| Twenty world calls at once, then the fight | 9 (9) | 27 (27) | 0 | 36.6 s, with a finding (same) |
| Against an AI, 4 minutes | 13 (15) | 24 (24) | 0 | 21.4 s (21.4) |

Counting from the hand-in costs some reads: the AI fight gets two turns fewer in four minutes. No action waits.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 281 tests`, `OK`, three runs in a row |
| The review's B1, B2, B3, unchanged | the first table |
| The review's A1, A2, A3, unchanged | still closed: 29 real calls at most (was 30); stance and the last good tile; the older caller prints no call |
| `test_rereview2.py` on `c0006266` (a throwaway worktree) | of 23 tests: 17 fail, 5 error, 1 passes (a control). Three errors are the missing names above; two are the old code raising |
| The two sweeps (scratch scripts): 1,128 fight-read cases, 380 profile and answer cases | no crash, no error event, no unsendable action. One case gives no action by design: a profile that names another battle opens that battle |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

## Size

Player code 3,602 lines in 19 files (`c0006266`: 3,322); tests 4,341 lines (3,843). `battle.py` is 650 lines
and `brain.py` 601 (AP6 budget 400). Fourteen functions branch more than 12 ways (`c0006266`: twelve); new on
the list are `battle.py` `_acted` (13), `brain.py` `_take_in` (14) and `budget.py` `settle` (13). Config
constants 49 (one new: `LOOSE_FOR`). Nothing ships switched off.

This debt grew again, by 280 lines, and it is the wrong direction for a phase whose bar is a small core. Most
of it is checks at the places values come in, and the two recovery paths. `battle.py` and `brain.py` should be
split before AP2; I did not do it inside a correction.

## Known limits

1. `LOOSE_FOR`, as said above: a replaced relay that never reports and makes a call more than 15 minutes
   after it was given up is outside what the ledger holds.
2. "Its relay came back, so its calls have run" rests on the relay doing a batch's lines in order, with
   `brain next` last. A harness that ran one message's tool calls side by side could come back with a call
   still in flight. No real relay has shown which it does.
3. The seam the review recorded stands: a batch is marked as issued before it is printed. A `brain next` that
   dies between the two leaves a batch nobody has. The brain is asked again and the turn's clock covers it.
4. One receipt is kept, for the last request answered. A crashed tick of a brain started by `brain next`
   itself saves nothing, so its request is run again by the next brain, from the last saved state.
5. A fight whose every tick fails is played with stand-in actions only, and its end is left to my profile.
   If closing the fight is what fails, the player stays in that fight until Duet steps in.
6. The profile check asks for the kinds the fixtures and the pilot's code use. If the game sends another, the
   profile is dropped: the first live run must be checked for `about: selects` findings, as for fight reads.
7. Everything is proven on tests and simulations. No real relay has driven any of it.
8. The limits in the earlier handoffs stand.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the reviewer: the ruling on `LOOSE_FOR`.
- For the director: the three token decisions (light polls on his turn; short-lived relays started by a
  script; whether to keep archiving his turn's opening state). Duet's three relay transcripts.

Not begun: AP2. No live run is proposed on this head until it has been verified.
