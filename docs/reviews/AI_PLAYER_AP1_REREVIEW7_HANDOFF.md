# AI player overhaul, phase AP1: correction handoff after the review of 60a28a84

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`60a28a84` ("request changes": one medium finding, about a batch an older version left waiting to be printed).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 60a28a84fb9b47910827c234b2e64e760ddcaa81
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW6_REVIEW.md on chatgpt/review-ai-player-ap1-rereview6 @ edd8b469
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

The finding is **confirmed**. It was reproduced on `60a28a84` with the review's own script, unchanged. That
script ends by asserting the defect, so on this head it stops at that assertion; what it prints before it is
the corrected result.

| # | Finding | The review's script on `60a28a84` | Now |
|---|---|---|---|
| 1 | Medium: a batch the version before had stored and not printed is printed by this version, and the brain is not asked (F1) | `legacy pending accepted: True`; both old calls printed; `served requests: 0`; 22 calls in the minute | `legacy pending accepted: False`; nothing printed; `served requests: 1`; 20 calls in the minute; the script stops at its assertion that there are more than 20 |

Every script of the earlier reviews still shows its case closed (E, D, C, B and A series, with the adaptations
already on record).

`player/tests/test_rereview6.py` has the finding as class N1, with two more classes: 15 tests. On `60a28a84`,
8 fail, 4 error and 3 pass. The three that pass are the controls: a waiting batch and a receipt of this
version are delivered as before. The four errors read the new number where the old code writes none. To run
there at all, the tests need the name `relay.PROTOCOL`; it was set in the test process, and no file of the old
checkout was changed.

## What the correction is

### A record is this version's own by the number it carries, not by its shape

`relay.PROTOCOL`, `relay.ours`; in `brain.py`: `_who`, `_a_waiting_batch`, `serve`, `_await`, `_answered`,
`_receipt`, `answer`.

The review's point is that the fields of a waiting batch cannot say which version's brain let its calls in.
So each record the brain and `brain next` keep for each other now carries a protocol number, written by the
code that made it. A record without this version's number is not used.

| Record | Written by | Without this version's number |
|---|---|---|
| `live/client.json` | `brain next` | read as no file: no relay, no waiting batch, nothing held, gone, ended or unprinted |
| a waiting batch (`pending`) | `brain next`, from the brain's answer | not printed |
| a request | `brain next` | removed unanswered (as since the last review, now by number as well as by its fields) |
| an answer | the brain | not taken |
| the receipt | the brain | its batch is not given again; the request it matches is told to come back in a moment, and its results are not taken in a second time |

The number must be the integer itself. `true`, `1.0` and `"1"` do not count.

Nothing that is put aside is taken for its opposite. The calls of such a batch stay in the ledger. The first
request of this version finds no record of who has them, and they are held, with no relay to their name. The
operator's word lets them go.

This is the first version with a number, so every earlier version's records are without it. That includes
`60a28a84`'s own, which have this version's shape. That is the intent: by its fields, a `60a28a84` batch
cannot be told from a `442a6311` one.

### The state of the review, on this head

The eighth relay's file is the old version's, so it is read as no file. A new relay starts and the brain is
asked. The brain holds the 21 calls the old ledger held and the two that waited: 23 in a lane of 20. It prints
no call and makes the relay wait six seconds between asks, for as long as it takes. In the test that is twenty
minutes: no length of time lets them go. After `stopped all` the first calls come a minute later.

The two calls that waited are held, and not counted as "never printed", for a reason. The `brain next` that
stored them may be alive and still waiting. One test has the old package's own process do that: this version
begins meanwhile; the old process then wakes, finds that the file names another relay, and prints no call.

## Found while correcting (not from the review)

I went through every way a batch made by an older version could still reach a relay.

| Way | On `60a28a84` | Now |
|---|---|---|
| The relay whose `brain next` was killed runs its line again (what a relay does) | the old batch was printed to it | it is told to stop; the file and the ledger are untouched |
| An older brain is still running when this version's `brain next` asks. It answers its own way and keeps a receipt. Then it is ended, and the relay asks again | the older brain's batch came back out of the receipt and was printed. With the `442a6311` brain itself: two calls | the relay is told to come back; the results are not taken in twice; that batch's calls are held |
| An older brain answers under the file name this version reads | taken | not taken; `brain next` goes on waiting, and then says to ask again |
| An older `brain next` runs on this version's file and stores a batch (a step back to the older code, then forward again) | printed | not printed, from the file or from the receipt |

Also:

- **The random walk** has a new step: at any moment the client's file is left without the number. Its model
  now reads such a file as saying nothing. Before that change it reported two walks; both were the model
  reading word that this version no longer reads.
- **`player/OPERATOR.md`** has a section "After the player's code is updated": a relay from before is told to
  stop; what was out or waiting is held until `stopped all`; a brain from before must be ended.
- **Last round's shape test** (`M1AClientFileOfAnyShapeDoesNotStopBrainNext`) now runs each of its files twice:
  as the older version left it, and with this version's number on it. Without the second, the checks of what
  is inside a file of this version would no longer have been reached.
- **An older test had gone blind, and a planted defect showed it.**
  `test_an_answer_is_read_only_by_the_request_it_names` plants an answer that names another request. That
  answer had no number, so the new check turned it away, and the test passed whatever the check of the
  request's name did. The planted answer now carries the number.
- **A request is still checked for its fields.** The review removed each field of a real request in turn; that
  is now in the suite, on a request that carries the number.

## Did a wider assumption change?

Yes, two. Both follow from the correction, and both are worth a look.

1. **What an older client file is good for.** On `60a28a84` the parts of it that had a usable shape were used:
   the relay's name and number, so a relay from before an update could carry on. Now none of it is used. A
   relay from before is told to stop, and what it would have handed in is not taken in. The world model
   catches up from the next relay's reads.
2. **The brain's own records are checked too.** An answer and a receipt count only with the number. So an
   older brain that is still running leaves this version's relay without a batch until that brain is ended.
   That is a stall, not a breach. `player/OPERATOR.md` says what to do.

Unchanged: the ledger's states, the evidence rows, the pacing, the file names, and a request's fields apart
from the number. The three simulated fights give the same figures as on `60a28a84`.

I recommend the scope the review named (legacy queued and pending upgrades, preserved holds, selective
release, this version's pending and receipt delivery), and with it the two brain-side checks above.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 346 tests`, `OK`, three runs in a row, none skipped |
| The review's F1, unchanged | the first table |
| The scripts of the earlier reviews | still closed |
| The upgrade from the `442a6311` package with a batch waiting, made by that package out of the repository's history | in the suite: `test_the_version_before_itself`, `test_the_old_brain_next_was_not_killed_and_wakes`, `test_a_receipt_of_the_version_before_itself` (they skip where the history lacks the commit). The same state from recorded files is always run |
| The recorded files against a fresh run of the old package | same keys in both files, same fields and types in the waiting batch, same calls, same ledger rows (length, lane, state) |
| `test_rereview6.py` on `60a28a84` (a throwaway worktree) | of 15: 8 fail, 4 error, 3 pass |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 6,948 calls, no problem |
| Thirty-four planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | same output as on `60a28a84`: no crash, no error event, no unsendable action |
| The three simulated fights | 14, 9 and 13 turns; 23, 27 and 24 calls in the fullest minute; no action delayed: as on `60a28a84` |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's ten first. All of them were planted in throwaway worktrees made
from local commits of this work, never in the repository's own tree. Those worktrees were clean after the
runs and are removed.

| Planted defect | Random walk (40 walks) | Tests of the last five reviews |
|---|---|---|
| A batch an older version left waiting is printed (this review's finding) | not caught | 8 fail |
| A client file without this version's number is read | not caught | 3 fail |
| A waiting batch without the number, in this version's file, is printed | not modelled | 1 fails |
| A request without the number is answered | not modelled | 1 fails |
| A request with the number is answered whatever else it lacks | not modelled | 1 errors |
| An answer without the number is taken | not modelled | 1 fails |
| A receipt without the number has its batch given again | not modelled | 3 fail |
| A receipt without the number is no receipt: its results are taken in again | not modelled | 3 fail |
| `true`, or 1.0, counts as the number | not modelled | 3 fail |
| The brain keeps its receipt without the number | 19 | 7 fail, 1 errors |
| A replaced relay's batch is taken as run | 40 | 8 fail, 1 errors |
| Any replaced relay's return counts as a held batch being over | 34 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 14 fail |
| A held batch is let go by itself after fifteen minutes | 40 | 5 fail |
| The receipt is not checked | 3 | 12 fail |
| A relay that asked holds the batch before it is printed | 6 | 1 fails |
| A batch nothing is on record of is taken as never printed | 30 | 17 fail |
| A batch known to be unprinted is held as if a relay had it | 5 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 2 fail |
| Asking what is held lets it all go | 40 | 4 fail |
| An older request's `lost` is read as back | not modelled | 1 fails |
| A number typed is not the number kept | not modelled | 2 fail |
| The brain paces over a batch it has not placed | not modelled | 1 fails |
| A waiting batch in this version's file is not checked for its shape | not modelled | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 8 | 6 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 2 fail |
| An older ledger's held calls are dropped on loading | not modelled | 6 fail |
| A failed tick is not saved | not modelled | 4 fail |
| The last resort does not wait when nothing can be sent | not modelled | 2 fail |
| An empty answer to an action is a taken action | not modelled | 1 fails |
| The last resort does not look at my profile | not modelled | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 1 fails |

The walk catches one of this review's ten. It cannot catch the first two: every record in a walk is made by
this version, so a file without the number is, to a planted defect that reads it anyway, a good file.

The counts of the earlier reviews' rows were taken before one test and one case were added to this round's
file; they can only have grown.

## Size

Player code 3,986 lines in 19 files (`60a28a84`: 3,951); tests 6,205 lines (5,721), and a second recorded
fixture of three files. `brain.py` is 849 lines (832), `battle.py` 685 (AP6 budget 400). Sixteen functions
branch more than 12 ways (sixteen). Config constants 49. Nothing ships switched off. The code change itself is
in `brain.py` and `relay.py`: 64 lines added and 29 removed, a good part of it the text that says what each
check is for.

The split of `brain.py` waits for acceptance, as ruled: after correctness, before AP2, as its own change.

## Known limits

1. **The number is kept by hand.** A later change to what a record means, or to the rule by which the brain
   lets a batch's calls in, is safe across an update only if `relay.PROTOCOL` is changed with it. Nothing
   checks that.
2. **An older brain that is still running is not ended by anything here.** Until the operator ends it, every
   `brain next` waits a minute and a half, gives no call and says to ask again.
3. **A step back to an older version on the same live folder is not covered.** That code does not know the
   number and reads this version's files as its own. What this version finds afterwards is covered (the last
   row of the table above); what the older code does meanwhile is not.
4. **After an update, everything that was out or waiting is held until the operator speaks**, also a batch
   that was certainly never printed. That is the price of not reading the older file.
5. **The recorded upgrades are from `442a6311` only**, two states of it now. Every other older version is
   handled by the rule: no number, not used.
6. **The ledger lives in `world.json`.** If that file is lost while relays have batches, their calls are not
   counted. This is not new and not part of this correction; the walk loses the client's file, never the
   brain's.
7. The limits in the earlier handoffs stand: the relay doing its lines in order, the operator's word being
   trusted, a batch marked as held before it is printed, a world model that cannot be saved, a fight that
   cannot be closed, and that no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the director: the three token decisions (light polls on his turn; short-lived relays started by a
  script; whether to keep archiving his turn's opening state). Duet's three relay transcripts. Whether
  `player/OPERATOR.md` goes into the next session brief as it is; it now has the section on updates.

Not begun: AP2, and the split of `brain.py`. No live run is proposed on this head until it has been verified.
