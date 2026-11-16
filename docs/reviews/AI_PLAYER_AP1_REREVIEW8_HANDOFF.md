# AI player overhaul, phase AP1: correction handoff after the review of 06358ca5

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`06358ca5` ("request changes": one high finding, about a brain from before the update that is still running).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 06358ca539372cae12d41b086a465719f403aba7
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW7_REVIEW.md on chatgpt/review-ai-player-ap1-rereview7 @ 718a9512
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

The finding is **confirmed**, and it refutes a claim of my last handoff. That note said an older brain still
running leaves this version's relay without a batch, "a stall, not a breach". The test behind it had the same
relay hand its batch in, where the older brain's reading ("the relay is back") happens to be true. With a
replacement asking, it is false, as the review shows.

Reproduced on `06358ca5` with the review's own script, unchanged: 34 calls in a minute, 24 in the world lane.

| # | Finding | The review's script on `06358ca5` | Now |
|---|---|---|---|
| 1 | High: a brain from before the update that is still running takes this version's request and lets the outstanding calls go before its answer is refused (G1) | the request is taken; the four calls are settled; `recovery 34`, `world 24` | the script stops at its own assertion that the request has been taken: after its five seconds the request is still in the inbox |

To see the rest of that script on this head I ran a copy with these changes and no other: its two assertions
of the defect removed (that the request is taken, that the four rows are settled), its wait for the old brain
made once instead of at every poll, and two prints added (whether the request still waits, and the ledger once
the old brain is gone). It prints: the request still waiting after 5 s; the four rows still `out` while the
old brain holds the lock; after that brain is ended, this version's brain answers and the four rows are
`loose` with no relay to their name; `recovery 30`, `world 20`.

Every script of the earlier reviews still shows its case closed (F, E, D, C, B and A series, with the
adaptations already on record).

`player/tests/test_rereview7.py` has the finding as class P1, with a second class that needs no history: 8
tests. On `06358ca5`, 6 fail and 2 pass. The two that pass are the control the review asked to keep (the old
brain is ended first) and a rule the old code keeps by accident (it never looked at another name).

## What the correction is

### A request is published where only a brain of this protocol looks

`relay.py` `request_path`, `is_request`, `pending_requests`, `OLD_REQUESTS`; `brain.py` `serve`, `_sweep`.

The last correction put a number on every record, and checked it when a record was read. The review's point
is that a check on reading comes too late for a request: the damage is done by the brain that reads it, and an
older brain checks nothing.

- This version's `brain next` publishes its request as `inbox/p1-req-<number>-<id>.json`: the name carries the
  protocol number. Every brain before this version looks for `inbox/req-*.json` and for nothing else there. I
  checked that in each of the 27 commits that contain the player, from its first (`3b3b4170`) to `06358ca5`;
  that includes `583fe353`, which ran the live session of 2026-11-11. In all of them the brain also takes the
  same lock, `brain.lock`, so there is one brain on the ledger at a time.
- So an older brain that is still running does not find the request, takes nothing of this version's, and
  writes nothing because of it. The ledger stays as that brain last saved it.
- This version's `brain next` then waits its minute and a half, gives no call, and says to ask again. The
  moment the older brain is ended, the lock is free: a `brain next` that is waiting answers its own request
  with this version's brain. That brain finds the older batch out, with no record of who has it, and holds it.
- A brain of this version answers a request only under its own protocol's name (and, as before, with its
  number and with every field). A file under the old name is removed unanswered whatever it says, as before.
  A request under another protocol's name is not opened and not removed: it is not this brain's.
- `brain next`, before it asks, still clears away what a dead `brain next` left: now under any of these names.

`relay.PROTOCOL` stays 1. No record changed its meaning and the brain's rules for letting calls in are as
they were; what changed is where a request is put.

## Found while correcting (not from the review)

- **`brain next` could go round without a pause, starting a brain every round.** When nobody held the lock,
  the request was gone and no answer had come, the wait loop did not sleep. I met it because this round's test
  never ended on the old checkout: there the old brain takes the request, and once it is ended nothing is left
  to answer. Measured on `06358ca5` with the process start counted instead of made: 14,300 starts in 0.3 s.
  On this head it is not reached from the review's case, since the request is not taken; it is reached when a
  brain drops a request as older than its receipt. The loop now waits like any other wait and starts a brain
  once (`brain.py` `_await`).
- **A real-package test of the last round tested something that can no longer happen.**
  `test_a_receipt_of_the_version_before_itself` had the `442a6311` brain answer this version's request and
  checked that its receipt was not given again. That brain cannot find the request now. The test keeps its
  name and now holds that this brain takes nothing and changes nothing, and that the relay's request is then
  answered once by this version. The rule that an older brain's receipt is never given again is still held
  by `test_a_receipt`, on a receipt without the number.
- **The real-process tests cannot hang.** Their clock moves only when `brain next` waits, so a `brain next`
  that goes round without waiting is stopped after 2,000 rounds and fails the test.

## Did a wider assumption change?

Two things changed, both narrow.

1. **Where a request is.** Its file name carries the protocol number. A request's content, the answer's
   name, the lock and every other file are as at `06358ca5`.
2. **The wait with nothing to answer.** It sleeps, and starts one brain, where it span.

`player/OPERATOR.md` changed with it: the section on updates is now an order to follow (end the old brain,
start a new relay, say what has been stopped), and it no longer says that an older brain left running is only
a stall. It says what this version does (hands it nothing) and what it cannot do (undo what that brain does
to its own ledger meanwhile).

I recommend the scope the review named: no request of this version taken by an older brain, the reservations
before and after that brain is ended, and this version's own pending and receipt delivery, with the queued
and pending upgrade fixtures and the selective release as controls.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 354 tests`, `OK`, three runs in a row, none skipped |
| The review's G1, unchanged, and the copy described above | the first table and the paragraph under it |
| The scripts of the earlier reviews | still closed |
| The `442a6311` brain as a process of its own, holding the lock, with relay A's four calls out | in the suite: `P1AnOlderBrainIsStillRunning`, three tests (a replacement asks while it is home; it is ended while this version waits; it is ended first). They skip where the history lacks the commit |
| The same without the old package | `P1ARequestIsPublishedWhereOnlyThisProtocolLooks`, five tests: the name, the old name, another protocol's name, the sweep, the wait |
| `test_rereview7.py` on `06358ca5` (a throwaway worktree) | of 8: 6 fail, 2 pass |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 6,948 calls, no problem |
| Forty-one planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | same output as on `06358ca5` |
| The three simulated fights | 14, 9 and 13 turns; 23, 27 and 24 calls in the fullest minute; no action delayed: as on `06358ca5` |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's seven first, then the last review's ten. All were planted in
throwaway worktrees made from a local commit of this work, never in the repository's own tree. That commit
differs from the code commit by one sentence in a docstring. The worktrees were clean after the runs and are
removed.

| Planted defect | Random walk (40 walks) | Tests of the last six reviews |
|---|---|---|
| This version's request is published under the name every earlier brain reads (this review's finding) | not modelled | 5 fail |
| A request under the old name is answered when it carries the number | not modelled | 1 fails |
| The brain does not look at files under the old name, so they are never removed | not modelled | 1 fails, 2 errors |
| The brain opens the requests of every protocol | not modelled | 1 fails |
| What a dead `brain next` left under another name is not swept | not modelled | 1 fails |
| With nothing to answer, `brain next` goes round without waiting | not modelled | 1 fails |
| With nothing to answer, a brain is started every round | not modelled | 1 fails |
| A batch an older version left waiting is printed | not caught | 8 fail |
| A client file without this version's number is read | not caught | 3 fail |
| A waiting batch without the number, in this version's file, is printed | not modelled | 1 fails |
| A request without the number is answered | not modelled | 1 fails |
| A request with the number is answered whatever else it lacks | not modelled | 1 errors |
| An answer without the number is taken | not modelled | 1 fails |
| A receipt without the number has its batch given again | not modelled | 2 fail |
| A receipt without the number is no receipt: its results are taken in again | not modelled | 2 fail |
| `true`, or 1.0, counts as the number | not modelled | 3 fail |
| The brain keeps its receipt without the number | 19 | 7 fail, 1 errors |
| A replaced relay's batch is taken as run | 40 | 8 fail, 1 errors |
| Any replaced relay's return counts as a held batch being over | 34 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 17 fail |
| A held batch is let go by itself after fifteen minutes | 40 | 5 fail |
| The receipt is not checked | 3 | 11 fail |
| A relay that asked holds the batch before it is printed | 6 | 1 fails |
| A batch nothing is on record of is taken as never printed | 30 | 20 fail |
| A batch known to be unprinted is held as if a relay had it | 5 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 2 fail |
| Asking what is held lets it all go | 40 | 5 fail |
| An older request's `lost` is read as back | not modelled | 1 fails |
| A number typed is not the number kept | not modelled | 3 fail |
| The brain paces over a batch it has not placed | not modelled | 1 fails |
| A waiting batch in this version's file is not checked for its shape | not modelled | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 8 | 6 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 2 fail |
| An older ledger's held calls are dropped on loading | not modelled | 7 fail |
| A failed tick is not saved | not modelled | 4 fail |
| The last resort does not wait when nothing can be sent | not modelled | 2 fail |
| An empty answer to an action is a taken action | not modelled | 1 fails |
| The last resort does not look at my profile | not modelled | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 2 fail |

The walk catches none of this review's seven, and cannot: it runs one version's brain and `brain next`.

Two counts are lower than in the last handoff, for a reason. "A receipt without the number has its batch
given again" and "is no receipt" failed three tests each; now two. The third was the real-package receipt
test, which no longer reaches a receipt (see above).

## Size

Player code 4,017 lines in 19 files (`06358ca5`: 3,986); tests 6,482 lines (6,205). `brain.py` is 859 lines
(849), `battle.py` 685 (AP6 budget 400). Sixteen functions branch more than 12 ways (sixteen). Config
constants 49. Nothing ships switched off. The code change is in `relay.py` and `brain.py`: 52 lines added and 21
removed, a good part of it the text that says what each rule is for.

The split of `brain.py` waits for acceptance, as ruled: after correctness, before AP2, as its own change.

## Known limits

1. **What an older brain does to its own ledger while it runs is by its own rules, and this version cannot
   undo it.** `442a6311` lets a held call go fifteen minutes after its relay was replaced, the next time it
   counts: at a request of its own version, or at the one status write of its watchdog. This version no
   longer gives it a reason to count, but it does not stop it either. The same holds for a hold that an older
   version had already let go before the update: it is not in the file this version takes over. The cover is
   the operator's order: end the old brain first, and say `stopped all` only when no relay from before can be
   running.
2. **A possible stricter rule, not done here.** After an update the player could make no call at all until
   the operator has spoken. That would cover limit 1 without trusting the older ledger. It changes what the
   operator must do at every update, so it is a decision for the director and the review, not a correction.
3. **A brain of this version does not step aside for a later protocol either.** It will not open that
   protocol's requests, and that relay will wait until this brain is ended. Safe, and the same operator rule.
4. **The name rule rests on what the earlier brains read.** That is a fact of the history, checked commit by
   commit as said above. A branch of the player outside that history would have to be checked the same way.
5. The limits in the earlier handoffs stand: the number is kept by hand; a step back to an older version on
   the same folder is not covered; the ledger lives in `world.json`; the relay doing its lines in order; the
   operator's word being trusted; and no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the director: limit 2 above. The three token decisions (light polls on his turn; short-lived relays
  started by a script; whether to keep archiving his turn's opening state). Duet's three relay transcripts.
  Whether `player/OPERATOR.md` goes into the next session brief as it is.
- The live test the director asked for was briefed against `06358ca5`. If it has not run, it should run this
  head instead. The brief's first set-up step (end any brain from before, and check none is left) is the
  order this finding calls for.

Not begun: AP2, and the split of `brain.py`.
