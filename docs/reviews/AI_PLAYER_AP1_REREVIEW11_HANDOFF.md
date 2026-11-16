# AI player overhaul, phase AP1: correction handoff after the second review of c412de4d

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to a second
review of `c412de4d` ("request changes": H1 high, H2 medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: c412de4df43baf4f11fbd817efb0f7ae95c08226
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW9_LANE_A_REVIEW.md on
        chatgpt/review-ai-player-ap1-rereview9-lane-a @ f586a6b2 (evidence; not merged)
Supersedes: 7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e, the handoff after the first review of c412de4d
        (docs/reviews/AI_PLAYER_AP1_REREVIEW10_HANDOFF.md). Not rebased: this head is two commits on top of it.
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Where this stands

`c412de4d` has been reviewed twice. The first review found H1, and I corrected it at `7cf7d73c`. This second
review reached me after that handoff. It finds H1 again, by a harness of its own, and one more, H2.

- **H1 was closed at `7cf7d73c`** and is closed here. This review's scripts say so: the table below.
- **H2 is confirmed.** It was still there at `7cf7d73c`. It is corrected here.

`7cf7d73c` was frozen for re-review and is untouched: it is this head's grandparent. A review of it that is
under way loses nothing by moving here. The code that differs is `player/world.py` (the count, and the name),
one line of `player/brain.py`, and the number in `player/relay.py`.

## Disposition

This review's five scripts. Three are scripts I had already run for the last handoff, under other names
(`known_limit.py`, `predecessor_controls.py`, `predecessor_resident.py`). Two are new.

| Script | On `c412de4d` (the review) | On `7cf7d73c` | Now |
|---|---|---|---|
| `known_limit.py`, unchanged | no call, 4 and 4; 30 and 20; 30 and 20 | the same | the same |
| `takeover_delivery.py`, unchanged (H1) | 4 calls after 8 s in each of its four cases | no call; it stops at its first check that calls were printed | the same. With its three checks taken out, all four cases print: no call in any |
| `predecessor_controls.py`, unchanged (H1) | pending, receipt, installed: 4 calls; ack: 4 calls after 8 s | no call; ack: 2 calls, 60.5 s after the word | the same |
| the same, `trusted` | 4 calls, no hold | none: `c412de4d` is a version before | none. Made by this head (the one line that names the maker): 4 calls after 8 s, no hold |
| `predecessor_resident.py`, unchanged (H1) | 3 calls | no call | no call |
| `repeated_unreadable.py replay` (H2) | the second hold has the first one's name; the kept word lets it go; a call 61.5 s later | the same, once the script's own check of the ledger's number reads this version's (it expects 1) | another name; all 30 calls still held; no call |
| the same, `different` and `no-word` | 30 held, no call | the same | the same |

Run unchanged, `repeated_unreadable.py` stops in every mode at its check that the ledger carries the number
1. The ledger carried 2 at `7cf7d73c` and carries 3 now. The figures above are from a copy in which that one
line reads `relay.PROTOCOL`.

`player/tests/test_rereview10.py` has H2 as four classes, 13 tests, and `test_rereview8.py` has one more
beside its different-contents test, as the review asked. On `7cf7d73c`, in a throwaway worktree with the
changed test files copied in: of the 13, **11 fail, 1 errors, 1 passes**, and the one in `test_rereview8.py`
fails. They do not all say the same thing:

- Three are the finding: the review's replay, the same with the later file written at the very same time,
  and the one in `test_rereview8.py` (a readable ledger, restored byte for byte with its time).
- Six are about the count and the time in the name, which `7cf7d73c` does not have: the four of
  `H2TheCount`, the brain that ends between the count and the save (it errors there: nothing to end between),
  and the "keeps its name" control, which passes there up to its last line, where it looks for the count.
- Four set `7cf7d73c` against itself: the three process tests with its resident brain, and "nothing it made
  is delivered". They fail because a version is not a version before itself. Here they are what holds
  `7cf7d73c` to the new number.
- The one that passes is the control: the same crash with no second takeover.

To load on `7cf7d73c` the tests need the name `player.world.takeovers`. It was set in the test process, and
no file of that checkout was changed.

## What was built

### A takeover has a number, and the hold's name carries it

`player/world.py` `takeovers`, `found`, `World.save`, `World.taken_over`; `player/brain.py`
`Brain._take_over` (one line).

- **The count.** `live/takeovers.json` says how many ledgers of another version the brains of this folder
  have taken over and saved as their own. It is not in `world.json`, because `world.json` is the file that
  is lost or written over when there is a takeover.
- **The name.** The hold is `update-` and a print of three things: the bytes of the file that is taken
  over, the time it was last written, and the count. Before, it was the bytes alone.
- **When it is counted.** With the first save of a brain that took a ledger over, and before that save. So:
  - from the moment the file is there until a brain has saved it, everyone who looks gives the hold the same
    name: `brain stopped`, every brain that starts and ends without saving, the brain that saves. The
    operator can speak before any relay is started, as before;
  - once it is saved, the next file that turns up is another takeover under another name, whatever its
    bytes and whatever its time. Word of the first names nothing in it.
- **Why the count is written first.** A brain that ends between the two writes leaves the file as it was
  under a new name, and the operator is asked again. The other order would leave a saved takeover that was
  never counted, and its name free for the next file of the same bytes.
- **Why the time is in the name as well.** For a file that is written again before any brain has saved it:
  whatever wrote it was still about after the operator spoke, so it is not the file the operator spoke of.

What stays as it was: the word is one row naming one id, taken once, harmless when taken twice (the control
in the tests: the same crash, no second takeover, calls a minute after the one word). A word that claims a
time before the file was last written is still taken as said now. With the name as it is that can only be a
row made by hand, and the minute then starts now.

### The number is 3

`player/relay.py`. This changes when a hold is let go, which is a rule for admitting calls. `7cf7d73c` could
have let a hold go on word that was not said of it, and a batch made after that is one this version would not
have made. By the rule I wrote into `relay.py` last time (change the number when such a rule changes; when in
doubt, change it), `7cf7d73c` is a version before this one. Four tests hold it to that with its own package.
A live folder that `7cf7d73c` has run on is taken over with the hold, and the operator says the word once. I
know of none.

### The operator's page

`player/OPERATOR.md`: the line the review found false ("the word is of no use for a later update, which is
listed under another name") now says it holds also when the file that is taken over is the same byte for
byte. That is what the code does.

## Found while correcting

- **Was any other name made from what a file says?** No. A relay's name, a request's id and with it a
  batch's id, and the id given to a held batch that has none are all drawn at random. The update hold was the
  one name made from content.
- **`Brain._save` goes on in memory when a save fails.** That is from before and I have not changed it, but
  it meets the count: if the count is written and `world.json` then cannot be, the brain holds the minute
  under the old name while `brain stopped` shows the new one, until a save succeeds. No call goes meanwhile,
  and the brain says that it could not save.
- **A test of the last round took "the number before this one" to be `c412de4d`'s.** With a third number
  that is `7cf7d73c`'s. The harness for "what a version before left" now takes the commit
  (`WhatAVersionBeforeLeft.nothing_it_made_is_delivered`) and asks only that the old ledger's number is a
  number and not this version's.
- **The random walk does not model this finding.** Its foreign ledgers never repeat byte for byte, because
  each keeps the rows of the batch that is out. I have not bent it to; the cases are unit tests.

## Did a wider assumption change?

Yes: **"what a file says tells which takeover it is" was wrong**, and the first version of the hold was
built on it. Two takeovers are two events, and an event is counted, not read off the bytes. The review asks
for exactly that ("a takeover generation").

Nothing else in the ledger rests on it (the first point above). The cost: one more small file in the live
folder, which the brain writes once per takeover.

I recommend the scope the review names: H2's takeover identity, with the controls for an ordinary start and
restart, selective release, the quiet minute, and this version's own delivery and idempotence; and for H1 a
confirmation with the review's own scripts, since its correction was made one head earlier.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 403 tests`, `OK`, three runs in a row, none skipped |
| This review's five scripts | the first table |
| The scripts of every earlier review | each ends as on `7cf7d73c` |
| `test_rereview10.py` and the one new test of `test_rereview8.py`, on `7cf7d73c` (a throwaway worktree) | of 14: 12 fail, 1 errors, 1 passes |
| The state made by the `7cf7d73c`, `c412de4d` and `29797ba0` packages out of the repository's history | in the suite: fourteen tests (they skip where the history lacks the commit; none skipped here) |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem |
| Sixty-eight planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | same output as on `7cf7d73c` |
| The three simulated fights | 14, 9 and 13 turns; 23, 27 and 24 calls in the fullest minute; no action delayed: as on `7cf7d73c` |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's seven first, then the number, then those of the earlier rounds. All
were planted in throwaway worktrees made from a local commit that has the code and the tests of the code
commit, never in the repository's own tree. The worktrees were clean after the runs and are removed.

| Planted defect | Random walk (40 walks) | Tests of the last nine reviews |
|---|---|---|
| The hold is named by the old file's bytes alone | not caught | 6 fail |
| The count of takeovers is not in the name | not caught | 4 fail |
| The time the file was written is not in the name | not caught | 1 fails |
| A takeover that is saved is not counted | not caught | 6 fail |
| The count is written after the save, not before it | not caught | 1 fails |
| A takeover is counted when a brain looks at it, not when one saves it | 4 | 4 fail |
| Every save of a brain that took a ledger over is counted | not caught | 1 fails |
| The number is the head before's again | not caught | 5 fail |
| The number before this one counts as this version's, in every record | 26 | 8 fail |
| A client file with the number before this one is read | not caught | 4 fail |
| A waiting batch with the number before this one is printed | not caught | 1 fails |
| A receipt with the number before this one has its batch given again | not caught | 1 fails |
| An answer with the number before this one is taken | not caught | 1 fails |
| A ledger with the number before this one is taken as it stands | 24 | 5 fail |
| A request with the number before this one is answered | not caught | 1 fails |
| A request is published, and read, under the predecessor's name | not caught | 4 fail |
| This version's own waiting batch is not given to the relay that takes over | 21 | 2 fail |
| This version's own receipt does not give its batch again | 17 | 8 fail |
| A ledger another version kept is taken at its word | 18 | 46 fail, 1 errors |
| A ledger this version kept is held all the same, at every start | not caught | 55 fail, 7 errors |
| The hold is twenty calls, not the minute's thirty | not caught | 39 fail |
| The operator's word lets the hold go with no minute after it | 1 | 13 fail |
| The word counts from whenever it claims to have been said | not caught | 1 fails |
| The hold has a new name each time a brain starts | not caught | 9 fail |
| The listing does not show the hold before a brain has taken the ledger over | not caught | 5 fail, 5 errors |
| A ledger that cannot be read is a first start | not caught | 2 fail, 6 errors |
| The brain does not put its number on the ledger | 34 | 56 fail, 4 errors |
| This version's request is published under the name every earlier brain reads | not caught | 11 fail |
| A request under the old name is answered when it carries the number | not caught | 1 fails |
| The brain does not look at files under the old name, so they are never removed | not caught | 1 fails, 2 errors |
| The brain opens the requests of every protocol | not caught | 1 fails |
| What a dead `brain next` left under another name is not swept | not caught | 1 fails |
| With nothing to answer, `brain next` goes round without waiting | not caught | 1 fails |
| With nothing to answer, a brain is started every round | not caught | 1 fails |
| A batch an older version left waiting is printed | not caught | 26 fail |
| A client file without this version's number is read | not caught | 16 fail |
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
| A loose call leaves the ledger after a minute | 40 | 44 fail |
| A held batch is let go by itself after fifteen minutes | 33 | 6 fail |
| The receipt is not checked | 2 | 13 fail |
| A relay that asked holds the batch before it is printed | 4 | 1 fails |
| A batch nothing is on record of is taken as never printed | 26 | 36 fail |
| A batch known to be unprinted is held as if a relay had it | 4 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 5 fail |
| Asking what is held lets it all go | 40 | 10 fail, 4 errors |
| An older request's `lost` is read as back | not caught | 1 fails |
| A number typed is not the number kept | not caught | 3 fail |
| The brain paces over a batch it has not placed | not caught | 1 fails |
| A batch waiting in an older client file is printed | not caught | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 9 | 8 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 13 fail |
| An older ledger's held calls are dropped on loading | not caught | 7 fail |
| A failed tick is not saved | not caught | 4 fail |
| The last resort does not wait when nothing can be sent | not caught | 2 fail |
| An empty answer to an action is a taken action | not caught | 1 fails |
| The last resort does not look at my profile | not caught | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 2 fail |

## Size

Player code 4,128 lines in 19 files (`7cf7d73c`: 4,091); tests 7,595 lines (7,305). `world.py` is 278
lines (246), `brain.py` 883 (882), `relay.py` 353 (349). `battle.py` 685 and `budget.py` 408 are
unchanged (AP6 budget 400 a file). Sixteen functions branch more than 12 ways (sixteen). Config constants 49.
Nothing ships switched off.

The split of `brain.py` waits for acceptance, as ruled.

## Known limits

1. **The count is a file, and can be lost.** If `takeovers.json` is lost, a word is still queued from an
   earlier takeover, and the same bytes turn up again written at the same time, the old word counts. A live
   folder that is put back whole from a copy, word included, is the same takeover to this code: nothing on
   disk says otherwise.
2. **A brain that ends between the count and the save** leaves the takeover under a new name. Word already
   said of it names nothing, and the operator is asked again (under test).
3. **A file written again before any brain has saved it** is a new name too, by the time in it. A tool that
   only touches the file has the same effect: the operator is asked again.
4. The limits of the last handoff stand: the number is kept by hand; a word said before the new relay's
   first ask does not cover the predecessor's last batch; a `brain next` of an older version that wakes
   before this version has run prints its batch, and the hold covers it; a step back to a version from
   before `c412de4d`; the word is taken on trust; a new live folder has no hold; the hold stops a fight too;
   and no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the reviewer or the director, from the last handoff: whether a hand-kept number is acceptable, or the
  code should be its own number.
- For the director: the three token decisions; Duet's three relay transcripts; whether `player/OPERATOR.md`
  goes into the next session brief as it is.
- A live test should run this head, not `7cf7d73c`.

AP2 goes on, on its own branch. The split of `brain.py` is not begun.
