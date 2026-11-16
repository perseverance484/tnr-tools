# AI player overhaul, phase AP1: correction handoff after the review of c412de4d

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`c412de4d` ("request changes": one high finding, H1).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: c412de4df43baf4f11fbd817efb0f7ae95c08226
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW9_REVIEW.md on chatgpt/review-ai-player-ap1-rereview9 @ e7e4c0f6
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

H1 is **confirmed and corrected**. The mistake was mine and it was a decision, not an oversight: my last note
said "`relay.PROTOCOL` stays 1", on the ground that no record had changed its meaning. The hold was a new rule
for admitting calls, and `relay.py` already said to change the number for that. With the number unchanged,
everything `29797ba0` had made passed for this version's own.

The correction is the one the review calls plausible and narrow: **the number is now 2.** No other line of the
player's code changed. What follows is the verification the review asked for, path by path.

The review's two scripts, unchanged, on `c412de4d` and now:

| The review's case | On `c412de4d` | Now |
|---|---|---|
| Old waiting batch; a new relay asks | 4 calls, no word said | no call. The script stops at its own assertion that calls were printed |
| Old receipt; the relay asks again | 4 calls, no word said | no call: that relay is told to stop |
| Old waiting batch; `stopped all`, then the new relay | 4 calls after 8 s | 2 calls, 60.5 s after the word |
| Old waiting batch; this version's brain has saved its hold first | 4 calls | no call |
| Old waiting batch, 11 s past its time | none | none |
| The same state, made by `c412de4d` | 4 calls, no hold | none: `c412de4d` is now a version before this one. With this head as the maker (the one line of the script that names the maker's commit), 4 calls after 8 s and no hold |
| A resident brain of `29797ba0` still running | 3 calls, no word said | no call: that brain does not see the request, and `brain next` gets no answer while it runs |

Every script of the earlier reviews ends as it did on `c412de4d`, with the adaptations already on record: the
A to G series, and the last review's known-limit script (no acknowledgement: no call, 4 and 4; acknowledgement:
30 and 20; acknowledgement and a minute: 30 and 20).

`player/tests/test_rereview9.py` has the finding as class H1 in five classes, 20 tests. On `c412de4d`, in a
throwaway worktree with the changed test files and the two new fixture folders copied in and nothing else
touched: **17 fail, 3 pass.** The three that pass are the current-version controls. Not all seventeen say
the same thing, so here is what the six that are not plain reproductions say:

- Four set `c412de4d` against itself there (the three process tests with its resident brain, and
  `test_the_version_that_was_reviewed_is_a_version_before_too`). They fail because a version is not a version
  before itself. On this head they are what holds `c412de4d`, the immediate predecessor, to the same rule as
  `29797ba0`.
- `test_nor_once_it_has_grown_too_old_to_send` fails there on what is held, not on a call: `c412de4d` read
  the predecessor's client file and took its word that the batch was never printed. This version reads
  nothing of that file, so the four calls stay held until the operator speaks.
- `test_it_is_ended_first`, with the `29797ba0` resident, likewise: `c412de4d` held the four calls under the
  old relay's name, read from that file. This version holds them for a relay that is not on record.

## What the number does, path by path

`player/relay.py` `PROTOCOL = 2`. Each path the review names, with what a record of `29797ba0` or `c412de4d`
now meets, and the test that holds it with the real `29797ba0` package or its recorded files:

| Record | What this version does with the predecessor's | Test |
|---|---|---|
| `client.json` | read as no file: no relay, no waiting batch, nothing held, gone or ended. Its relay is told to stop | `test_its_waiting_batch_is_not_printed`, `test_its_receipt_is_not_given_again` |
| The waiting batch in it | never printed, in time or stale, with or without the hold saved | the same, `test_nor_once_it_has_grown_too_old_to_send`, `test_nor_when_a_brain_of_this_version_has_the_ledger_already` |
| The receipt in `world.json` | its batch is not given again. A request of this version that names the same relay and number is answered with "come back", and what it brings is not taken in a second time | `test_the_request_it_answered_is_not_run_again_by_this_brain` |
| A request | this version publishes under `p2-req-…`. A brain of `29797ba0` or `c412de4d` reads `req-…` and `p1-req-…`: it does not see it | `H1ThePredecessorsBrainIsStillRunning` and `H1TheReviewedVersionsBrainIsStillRunning`: three tests each against that version's own `brain run` in a process |
| An answer | one that carries 1 is removed and not taken | the stamp cases (below) |
| The ledger | taken over with the hold: no call until the word, and none for a minute after | `test_the_word_and_then_a_minute`, `test_the_predecessor_itself`, `test_the_version_that_was_reviewed_is_a_version_before_too` |
| A `brain next` of `29797ba0` that was in its wait when the code was updated | once a relay of this version has started, it wakes, reads a client file that is not its own, and tells its relay to stop | `test_a_brain_next_of_the_predecessor_that_wakes_after_the_update_prints_nothing` |

What the review asked to be kept:

- **Accepted results are idempotent.** The predecessor's receipt still answers its request; only its batch is
  withheld. Nothing is taken in twice (the test above; `saved world == before`).
- **Outstanding holds are retained.** The four calls of the predecessor's batch stay in the ledger, held for a
  relay not on record, beside the update's minute, in every case above. They leave only on the operator's
  word (`test_the_word_and_then_a_minute` says the word a second time for them).
- **Ordinary delivery for this version's records.** Class `H1WhatThisVersionMadeIsDeliveredAsBefore`: the same
  program run by this version leaves a waiting batch that is printed when its own wait is over, a receipt that
  answers the same request with the same batch and runs nothing twice, and a request that a brain of this
  version at home answers. No hold in any of them.
- **The acknowledgement id, the quiet minute, the hold across brains and retries**: the 15 tests of
  `test_rereview8.py` stand. One of them now also tries the predecessor's number on the ledger.

No ownership evidence is dropped in a way that lets a call go. What the predecessor's client file says of who
holds what is not read; the brain then has no record for those batches and holds them. That is the rule since
the review of `60a28a84`, and the tests above show it for `29797ba0`.

`player/OPERATOR.md`: the claims the review found false (lines 60, 67 and 77 at `c412de4d`) are now what the
code does, and each is under test. One line is added: a batch the last relay from before the update had is
listed only once the new relay has asked, and needs the word again.

## Found while correcting

- **The stamp cases did not name the number that matters.** The tests that put another maker's mark on a
  record used no number, 0, the next number, text, a float, `true` and `null`. At number 1 the 0 happened to
  be the number before; at 2 the list would have left the predecessor's out. "The number before this one" is
  in the list as such now (`STAMPS`, `test_rereview6.py`), and the ledger's own stamp test uses the same list.
  The brain's "not this protocol's to open" test and the sweep test name it too.
- **The random walk could not see a ledger that kept another version's number.** Its "ledger is never behind"
  check is made only on a ledger with this version's number, so a planted defect that left the predecessor's
  number on the ledger passed 200 walks. The walk now also checks that a ledger a brain has saved carries this
  version's number (`whose`), and its "another version" events carry the predecessor's number half the time.
  That defect is now caught in 24 of 40 walks, and "the brain does not put its number on the ledger" in 34.
- **`hold()` in `test_rereview8.py`** now fails with "one minute should be held after the update" when none
  is, as the review suggested, where it raised a `ValueError` from unpacking.
- **Under one planted defect the upgrade tests did not end.** They ask until a time on the test's clock has
  passed; a `brain next` that neither waits nor gives a call never lets it pass. They now fail after fifty
  such asks in a row (`AfterAnUpdate.next`).
- **The older-brain tests take the commit as a parameter** (`the_package_at`, `by_the_version_at`,
  `P1AnOlderBrainIsStillRunning.VERSION`), so the same three process tests run against `442a6311`, `29797ba0`
  and `c412de4d`.
- **My last note's test line count was wrong by two** (6,902; the script says 6,904). The figures below are
  from `scripts/player_size.py`.

## Did a wider assumption change?

Yes: **"the number changes when a record changes its meaning" was too narrow, and I applied it.** A batch is
a promise made under the rules of the brain that made it. A rule that admits fewer calls makes every older
promise one this version would not have made, whatever the record looks like. The text in `relay.py` now says
so in those terms, lists what each number stood for, and ends: when in doubt, change it. A new number costs
the operator one word and a minute; an old one can cost the limit.

Where else did "same number, same rules" carry weight? Everywhere `relay.ours` is asked: the client file, the
waiting batch, the request, the answer, the receipt and the ledger. Each of the six is now tested with the
predecessor's number, and five of them with a predecessor's own package: all but the answer, which a
predecessor's brain no longer gets to write.

What it costs: this update is one the operator must speak to. Every live folder that `c412de4d` or anything
older has run on is taken over with the hold.

I recommend the narrow re-check the review named: the protocol boundary on these six records and the request's
name, against `29797ba0` and `c412de4d`, with the existing migration controls.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 389 tests`, `OK`, three runs in a row, none skipped |
| The review's two scripts, unchanged | the first table |
| The scripts of the earlier reviews | each ends as on `c412de4d` |
| `test_rereview9.py` on `c412de4d` (a throwaway worktree) | of 20: 17 fail, 3 pass (the controls) |
| The predecessor's state made again by the `29797ba0` and `c412de4d` packages out of the repository's history | in the suite: ten tests (they skip where the history lacks the commit; none skipped here). The same state from recorded files of `29797ba0` (`fixtures/upgrade_29797ba0_pending`, `upgrade_29797ba0_receipt`) is always run |
| The three earlier fixture folders | byte for byte as at `c412de4d` |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem |
| Sixty-one planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | same output as on `c412de4d` |
| The three simulated fights | 14, 9 and 13 turns; 23, 27 and 24 calls in the fullest minute; no action delayed: as on `c412de4d` |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's eleven first. All were planted in throwaway worktrees made from
local commits, never in the repository's own tree. The player's code in those commits is the code commit's.
Forty-three rows were run before five tests and the harness guard above were added to the test files, and
the other eighteen after: the tests column of the forty-three can only be short. One defect of my own first
made the walk and the older tests go round without end (this version's waiting batch dropped whenever the
client file is read); the table has in its place one of the same kind that ends. The worktrees were clean
after the runs and are removed.

| Planted defect | Random walk (40 walks) | Tests of the last eight reviews |
|---|---|---|
| The number is the predecessor's again | not caught | 12 fail |
| The number before this one counts as this version's, in every record | 26 | 14 fail |
| A client file with the number before this one is read | not caught | 5 fail |
| A waiting batch with the number before this one is printed | not caught | 1 fails |
| A receipt with the number before this one has its batch given again | not caught | 2 fail |
| An answer with the number before this one is taken | not caught | 1 fails |
| A ledger with the number before this one is taken as it stands | 24 | 1 fails |
| A request with the number before this one is answered | not caught | 1 fails |
| A request is published, and read, under the predecessor's name | not caught | 3 fail |
| This version's own waiting batch is not given to the relay that takes over | 21 | 2 fail |
| This version's own receipt does not give its batch again | 17 | 8 fail |
| A ledger another version kept is taken at its word | 18 | 29 fail, 1 errors |
| A ledger this version kept is held all the same, at every start | not caught | 49 fail, 6 errors |
| The hold is twenty calls, not the minute's thirty | not caught | 26 fail |
| The operator's word lets the hold go with no minute after it | 1 | 7 fail |
| The word counts from whenever it claims to have been said | not caught | 1 fails |
| The hold has a new name each time a brain starts | not caught | 4 fail |
| The listing does not show the hold before a brain has taken the ledger over | not caught | 5 fail |
| A ledger that cannot be read is a first start | not caught | 1 fails |
| The brain does not put its number on the ledger | 34 | 51 fail, 4 errors |
| This version's request is published under the name every earlier brain reads | not caught | 7 fail |
| A request under the old name is answered when it carries the number | not caught | 1 fails |
| The brain does not look at files under the old name, so they are never removed | not caught | 1 fails, 2 errors |
| The brain opens the requests of every protocol | not caught | 1 fails |
| What a dead `brain next` left under another name is not swept | not caught | 1 fails |
| With nothing to answer, `brain next` goes round without waiting | not caught | 1 fails |
| With nothing to answer, a brain is started every round | not caught | 1 fails |
| A batch an older version left waiting is printed | not caught | 22 fail |
| A client file without this version's number is read | not caught | 8 fail |
| A waiting batch without the number, in this version's file, is printed | not caught | 1 fails |
| A request without the number is answered | not caught | 1 fails |
| A request with the number is answered whatever else it lacks | not caught | 1 errors |
| An answer without the number is taken | not caught | 1 fails |
| A receipt without the number has its batch given again | not caught | 3 fail |
| A receipt without the number is no receipt: the results are taken in again | not caught | 3 fail |
| True, or 1.0, counts as the number | not caught | 4 fail |
| The brain keeps its receipt without the number | 17 | 8 fail, 1 errors |
| A replaced relay's batch is taken as run | 39 | 9 fail, 1 errors |
| Any replaced relay's return counts as a held batch being over | 24 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 37 fail |
| A held batch is let go by itself after fifteen minutes | 33 | 6 fail |
| The receipt is not checked | 2 | 13 fail |
| A relay that asked holds the batch before it is printed | 4 | 1 fails |
| A batch nothing is on record of is taken as never printed | 26 | 27 fail |
| A batch known to be unprinted is held as if a relay had it | 4 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 2 fail |
| Asking what is held lets it all go | 40 | 10 fail |
| An older request's `lost` is read as back | not caught | 1 fails |
| A number typed is not the number kept | not caught | 3 fail |
| The brain paces over a batch it has not placed | not caught | 1 fails |
| A batch waiting in an older client file is printed | not caught | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 9 | 8 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 8 fail |
| An older ledger's held calls are dropped on loading | not caught | 7 fail |
| A failed tick is not saved | not caught | 4 fail |
| The last resort does not wait when nothing can be sent | not caught | 2 fail |
| An empty answer to an action is a taken action | not caught | 1 fails |
| The last resort does not look at my profile | not caught | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 2 fail |

## Size

Player code 4,091 lines in 19 files (`c412de4d`: 4,083); tests 7,305 lines (6,904), and two more recorded
fixture folders of three small files each. `relay.py` is 349 lines (341): one line of code changed, the
rest is text. `brain.py` 882, `battle.py` 685 and `budget.py` 408 are unchanged (AP6 budget 400 a file). Sixteen
functions branch more than 12 ways (sixteen). Config constants 49. Nothing ships switched off.

The split of `brain.py` waits for acceptance, as ruled.

## Known limits

1. **The number is still kept by hand, and it failed once.** The rule is now wider and says "when in doubt".
   One test pins that `06358ca5`, `29797ba0` and `c412de4d` do not have this version's number. Nothing
   forces the next change. The alternative, not built and not asked for: let the code be its own number (a
   print of the package's files), so that every update is another version. It would cost the operator the
   word and the minute at every update, which the page already asks for.
2. **A word said before the new relay's first ask does not cover the predecessor's last batch.** That batch
   goes loose with the first ask and is listed from then on. Until the operator says the word again its calls
   stay held: less room, never more. The page says so now.
3. **A `brain next` of the predecessor that was in its wait when the code was updated** still has the old
   code. If it wakes before any `brain next` of this version has run, it prints its batch. The hold is what
   covers that: nothing of this version goes out until the operator has said the old relays are stopped. If
   it wakes after, it tells its relay to stop (under test).
4. **A step back to an older version on the same folder**: `c412de4d` puts 1 on the ledger, so coming back
   from it is a takeover with the hold. A version before `c412de4d` keeps whatever number it finds, as said in
   the last note: coming back from one of those is trusted.
5. The limits in the earlier handoffs stand: the word is taken on trust; a new live folder has no hold; the
   hold stops a fight too; a brain of this version does not step aside for a later protocol; the ledger lives
   in `world.json`; the relay doing its lines in order; and no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the reviewer or the director: limit 1's alternative, if a hand-kept number is not acceptable.
- For the director: the three token decisions; Duet's three relay transcripts; whether `player/OPERATOR.md`
  goes into the next session brief as it is (the review says it should stay in the session instructions).
- A live test should run this head. From a new live folder there is no hold; on a folder an earlier version
  ran on, the first thing the operator does is in "After the player's code is updated".

AP2 goes on, on its own branch. The split of `brain.py` is not begun.
