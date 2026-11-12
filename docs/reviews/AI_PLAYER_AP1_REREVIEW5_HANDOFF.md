# AI player overhaul, phase AP1: correction handoff after the review of efa79808

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`efa79808` ("request changes": two high findings, one medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: efa79808e740811fa562466d332fd01171068cb7
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW4_REVIEW.md on chatgpt/review-ai-player-ap1-rereview4 @ 430a782f
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

All three findings are **confirmed**. Each was reproduced on `efa79808` with the review's own script, and each
script, unchanged, now gives the corrected result.

| # | Finding | The review's script on `efa79808` | Now |
|---|---|---|---|
| 1 | High: `stopped all`, read again, lets go of a relay replaced after the operator spoke (D1) | the active relay's 3 held calls: 3 after the first request, 0 after the retry | 3, and 3 |
| 2 | High: a batch the client's file says nothing of counts as never printed (D2) | A not back, 0 of its 4 calls held; 34 calls in a minute, 24 in the world lane | 4 held; 30 and 20 |
| 3 | Medium: the last resort answers with nothing and no wait when held calls fill the minute (D3) | requests 2 to 5: no call, hold 0.0 | no call, hold 6.0 |

The review's retention controls and its adapted C5 give the same results as before. Every script of the
earlier reviews still shows its case closed.

Finding 2 was also checked the way the review did it, with no file written by hand: the `442a6311` package
itself left a batch out through its own `brain next`, and this head took the same folder over with a
replacement. The old relay's call is held for a relay not on record, stays held when that relay comes back,
shows in the listing as `batch 1`, and goes with `stopped all`.

**The planted defect that passed everything** (a listing that lets go of what is held): the review's script
edits `brain.stopped` by text, and those lines are rewritten here, so it plants nothing on this head. I
planted the same defect in the new function. Two tests fail on it, and so do all 40 walks.

`player/tests/test_rereview4.py` has one class per finding (L1 to L3, 15 tests). On `efa79808`, 10 fail, 4
error and 1 passes (a control). Of the errors, two are a field that did not exist there (`unprinted`), one is
how the old command line wrote its output, and one is real: the old code raised on a held call in an older
shape.

## What each correction is

### 1. The operator's word names the batches it is said of (`brain.py` `stopped`, `_held`; `budget.py` `ended`)

`stopped` now works out, at the moment it is said, which batches are held: those the client's file says went
with a replaced relay, and those the brain's saved ledger holds, whoever has them. The word is written down
as one row per batch, by the batch's id. There is no row that means "everything" any more, and
`Budget.ended` takes nothing but one batch's id. So reading the word again settles nothing more, and a relay
replaced afterwards is not in it.

`all` is every batch held at that moment. It cannot be the running relay's batch: that one is out, not held.
A batch with no relay to its name can be named by its id, which the listing shows.

### 2. Not on record is not never printed (`brain.py` `_ledger`, `_exchange`, `_owed`, `_who`)

The brain now places its last batch only by what the request positively says of it:

| The request says | The batch is |
|---|---|
| the relay asking holds it | handed in: settled |
| it went with a replaced relay | loose, under that relay's token |
| it was never printed | counted from now |
| none of these | loose, with no relay to its name |

"Never printed" is now something the client records, not something inferred from silence. Before
`brain next` asks the brain, it writes the request's id into `client.json` as not printed. If it dies, the
next `brain next` reads that and can say so. A batch that grew old unprinted is recorded the same way. The
list is cleared when the brain has answered.

What `_who` drops from a client file of another shape is no longer taken for its opposite. A held call in an
older ledger shape is kept held and given the fields it has now (`budget.py` `_shape`). Evidence rows in an
older shape are dropped: they were written by the code whose ownership check the last review found wrong.

### 3. No batch with nothing in it goes out without a wait (`brain.py` `_paced`, `_record`)

The rule "no call was admitted, so wait" is now one function that both the ordinary tick and the last resort
go through. Behind it, `_record` gives any batch with no call, no wait and no STOP the same wait, whatever
made it.

## The operator's page

`player/OPERATOR.md` (new) is the brief the review asked for before a live run: what held calls are, what
they look like in `status.json` and the events, the four forms of `brain stopped`, when it is safe to say,
that `all` covers only what is held when it is said, and the sixty seconds that follow.

## The walk, and planted defects

The review listed what the walk's checks did not establish. Three of those are now covered:

- **`stopped all` and the listing.** The operator now lists at random, says `all` when every relay but the
  running one is stopped, and half the time the running relay is then replaced by one whose first request dies
  before the receipt and is asked again: the review's D1 sequence.
- **A lost record.** The client's file loses `held`, or is lost whole.
- **Printed twice to the same relay** is now a problem, like printed to two.

On `efa79808` this walk finds held calls let go without evidence in 35 of 40 walks. On this head,
`python3 -m player.tests.test_walk 200 300` ran 200 walks, 6,957 calls: no problem.

Still not modelled, as the file's header says: fights and the other lanes, results from a transcript, real
processes and locks, and a relay that breaks its contract.

Twenty planted defects, one at a time, in a throwaway worktree:

| Planted defect | Random walk (40 walks) | Tests of the last three reviews |
|---|---|---|
| A replaced relay's batch is taken as run | 40 | 8 fail |
| Any replaced relay's return counts as a held batch being over | 34 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 10 fail |
| A held batch is let go by itself after fifteen minutes | 40 | 4 fail |
| The receipt is not checked | 3 | 7 fail |
| A relay that asked holds the batch before it is printed | 6 | 1 fails |
| A batch nothing is on record of is taken as never printed (finding 2) | 30 | 5 fail |
| A batch known to be unprinted is held as if a relay had it | 5 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read (finding 1) | 3 | 2 fail |
| Asking what is held lets it all go (the review's planted defect) | 40 | 2 fail |
| `stopped all` also names the running relay's batch | 8 | 6 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 1 fails |
| An older ledger's held calls are dropped on loading | not modelled | 2 fail |
| A failed tick is not saved | not modelled | 4 fail |
| The last resort does not wait when nothing can be sent (finding 3) | not modelled | 2 fail |
| An empty answer to an action is a taken action | not modelled | 1 fails |
| The last resort does not look at my profile | not modelled | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 1 fails |

Every one fails at least one committed test. The walk catches twelve of them. The others are outside
what it models, or need a relay to act just before the operator speaks.

## Did a wider assumption change?

Yes, in two places. I recommend the evidence, retry and migration scope the review named.

- **Evidence.** `ended` rows are `[batch id, when, whose, "back" or "stopped"]` and nothing else is read.
  `Budget.ended("*")` is gone. `brain stopped` reads the saved ledger as well as the client's file.
- **Classification.** The request carries `unprinted`. A batch that is not positively placed is held. This
  is the direction that costs room, not safety: a client file that loses its record now leaves calls held
  until the operator speaks, where it used to let them go.

The relay's contract (`player/RELAY.md`) and the names of the request and answer files are unchanged. The
three simulated fights give the same figures as before.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 320 tests`, `OK`, three runs in a row |
| The review's D1, D2, D3, its retention controls and adapted C5, unchanged | the first table |
| A real upgrade from the `442a6311` package | as said above |
| The scripts of the earlier reviews (A, B and C series, with the adaptations of the last handoff) | still closed |
| `test_rereview4.py` on `efa79808` (a throwaway worktree) | of 15: 10 fail, 4 error, 1 passes |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 6,957 calls, no problem |
| The twenty planted defects | every one fails at least one test; the unchanged code passes |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | no crash, no error event, no unsendable action |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

Planted defects were run only in a worktree this time; the real tree was never edited by them.

## Size

Player code 3,895 lines in 19 files (`efa79808`: 3,815); tests 5,422 lines (5,096). `brain.py` is 776 lines,
`battle.py` 685 (AP6 budget 400). Fifteen functions branch more than 12 ways (fifteen). Config constants 49.
Nothing ships switched off.

The split of `brain.py` waits for acceptance, as the review ruled: after correctness, before AP2, as its own
change that moves code and changes no behaviour.

## Known limits

1. "Its relay came back, so its calls have run" rests on the relay doing a batch's lines in order, with
   `brain next` last. No real relay has shown what it does.
2. The operator's word is trusted, for the batches held when it is said. Said of a relay that is still
   running, it lets that relay's calls go uncounted after a minute.
3. `brain stopped` reads the ledger as the brain last saved it. A batch that goes loose in a tick that is
   still running is not in a word said at that instant; say it again.
4. A batch that is not on record is held with no relay to its name. That relay coming back does not release
   it, because nothing ties the two together. Only the operator's word does. This is the price of not
   guessing, and it is paid after a lost or older client file, not in ordinary running: the walk finds no
   such hold without one.
5. A batch is marked as held before it is printed. A `brain next` that dies between the two leaves a batch
   that no relay has, held until the operator's word.
6. When the world model cannot be saved, a tick that worked is treated as failed and sends nothing.
7. A fight whose closing code fails outside its books stays open. Nothing is sent into it.
8. Everything is proven on tests, a random walk and simulations. No real relay has driven any of it.
9. The limits in the earlier handoffs stand where this note does not replace them.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the director: the three token decisions (light polls on his turn; short-lived relays started by a
  script; whether to keep archiving his turn's opening state). Duet's three relay transcripts. Whether
  `player/OPERATOR.md` goes into the next session brief as it is.

Not begun: AP2, and the split of `brain.py`. No live run is proposed on this head until it has been verified.
