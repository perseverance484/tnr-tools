# AI player overhaul, phase AP1: correction handoff after the review of e4a267cd

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-13, in answer to the review of
`e4a267cd` ("request changes": H1 closed; of H2 one medium finding left).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: e4a267cd1ab5ff85c3b2399bab713f2870da6ccb
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW11_LANE_A_REVIEW.md on
        chatgpt/review-ai-player-ap1-rereview11-lane-a @ 219515fe (evidence; not merged)
Base of this correction: 25308e2a4f2ee905f1bf3412c3f7f85c1811c62f. That is e4a267cd with brain.py split into a
        package, approved on chatgpt/review-ai-player-brain-split @ 11a0d5df. The branch was moved forward onto
        it; nothing was rebased.
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Where this stands, and a mistake of mine in the order of things

The review of `e4a267cd` was published on 2026-11-12. It did not reach me, and I did not look for it: I found
it on the remote the next day. In between I wrote, in two handoffs, that `e4a267cd` "has not had its re-check".
That was untrue when I wrote it. What I built on that belief:

- the split of `brain.py`, on `e4a267cd`. It is approved, and its review says in so many words that it leaves
  AP1's verdict at the base as it is;
- AP2's first part, on the split, handed off at `c720743a`.

So this correction is made where the code now is: in the package. The diff to review is `git diff 25308e2a
HEAD`. In the old file's terms it touches `world.py` and two functions the split moved without a change,
`stopped` and `_held`, now in `player/brain/client.py`. AP2 takes this correction in and its handoff is issued
again at a new SHA.

H1 is closed in the review against `29797ba0`, `c412de4d` and `7cf7d73c`. Nothing of it changes here but the
protocol's number.

## Disposition

The finding is **confirmed and corrected**. The review's script, unchanged, on the base and now:

| The review's case | On the base (`25308e2a`, the code of `e4a267cd`) | Now |
|---|---|---|
| `window`: `stopped all` by a process of its own, between the two writes, while the resident has the brain's lock | the word is kept under a name the brain's hold does not have; when the old file is back, that takeover has the name: 4 calls after 9 s, nothing held | no word is taken: the listing says a brain is saving the takeover. When the old file is back: no call, all 30 held. Counts 1 and 2. The script stops at its check that the word and the later listing name the same hold |
| `failed`: the world model cannot be written; `stopped all`; the same brain saves later | the same: 4 calls after 9 s, nothing held | no call, all 30 held; the word that was taken and the later hold have different names. The script stops at its check that the count is 1: it is 2, for the reason below |
| `before`: the word said before the save | no call, 30 held | the same |
| `after`: the word said after the save | no call, 30 held | the same |

**The `failed` case and the brain's lock.** The script makes its brain in its own process and takes no lock
for it. A brain that runs holds the brain's lock, and `brain stopped` tells a brain that is home from one that
is gone by that lock. So in the script `stopped` finds nobody home, counts the save that was left, and takes
the word for the file's new name; the brain that did not die counts again when it does save. Hence 2 and 3
where the script expects 1 and 2. Nothing is let go either way. With the lock held, as it is held in
production, no word is taken at all and the counts are 1 and 2:
`test_word_said_after_a_save_that_failed_is_not_written_down_while_that_brain_is_home`. The script's own shape
is `test_with_nobody_home_the_save_that_was_left_is_counted_and_the_file_has_a_new_name`.

The review's `save_faults.py`: its `counter` case passes unchanged. Its `world` case stops at its check that
the count is 1 after the failed write: it is 0 now, with "saving" standing. With that check and the last one
taken out it prints what it goes on to look at: the restart does not reuse the name, the old word lets go 0
rows, and the count is 2 once the first brain has saved as well.

Every script of the earlier reviews ends as it did on the base.

`player/tests/test_rereview11.py` has the finding as four classes, 12 tests. On the base, in a throwaway
worktree with the changed test files copied in: **all 12 fail**. Six are the finding and its neighbours (the
two reproductions fail on a name being written down). Two are about `generation` and `seen`, which the base
does not have. Four set `e4a267cd` against itself as a version before, and are what holds it to the new number
here. To load on the base the tests need four names of the new code; they were set in the test process, and no
file of that checkout was changed.

## What was built

### A takeover is saved in three writes, and has no name between the first and the third

`player/world.py` `World.save`, `generation`, `seen`, `counted`, `print_of`; `World.__init__`.

Before, two writes: the count raised, then `world.json`. Between them the old file and the raised count read
as the name of a takeover that did not exist yet. Now:

1. `takeovers.json` says `"saving": true`. The count is not raised.
2. `world.json`.
3. The count is raised and `"saving"` is over.

- **While "saving" stands, the count and the file make no name.** `brain stopped` reads the two together
  (`seen`: the count before and after the file, again if it moved) and takes no word for a takeover then.
- **A save that was left is counted by whoever comes next, before any name is made.** A brain that starts
  finds "saving" and raises the count first (`counted`). `brain stopped`, when it finds "saving" still standing
  after a moment and can take the brain's lock, so that nobody is home, does the same.
- **A save that failed is done again in full** by the same brain: all three writes.

### `brain stopped`

`player/brain/client.py` `_on_disk`, `_held`, `stopped`, `_named`, `SAVING`, `LOOKS`.

When a takeover is being saved, `stopped` looks again for up to two seconds, which is far longer than a save
takes. If a brain finishes meanwhile, the hold is in the saved ledger under its own name and the word is taken
for that. If "saving" still stands and a brain is home, nothing is written down for the takeover and the
listing says `the relays from before the update (a brain is saving the takeover: say it again in a moment)`.
Other holds are spoken of as before.

### Why no word can now be kept for a later takeover

A word is written down only under a name made of a file and a count that were read together with "saving" not
standing. For that name to be a later takeover's, the same file and the same count would have to stand again,
with "saving" not standing, after a world model was written in between. After any write of the world model
the count is raised: by the third write, or, if that brain ended first, by the next brain's start or by
`stopped` with nobody home, and each of those comes before a name is made again. What is left is the limit
already on record: the count's own file lost or put back.

The count-first behaviour at a crash is as the review asks: a brain that ends after the first write leaves the
old file, and it is taken over under a new name, with word of the old name letting nothing go
(`test_a_brain_that_ends_between_the_count_and_the_save_leaves_the_file_under_a_new_name`, adjusted to the
three writes). The operator can still speak before a relay is started, also after such a crash.

### The number is 4

`player/relay.py`. This changes when a hold can be let go, so by the rule the number changes, as the review
says. `e4a267cd` is a version before this one; four tests hold it to that with its own package. An older
`takeovers.json`, which has a count and no "saving", reads as it should.

### The operator's page

`player/OPERATOR.md`: what the new line in the listing means and what to do (say it again).

## Found while correcting

- **The package did not carry what came after the split.** One review script runs the source of `stopped`
  again inside `player.brain`'s namespace. This correction gave `stopped` two new names, and the script failed
  on the first. The package now has them, and itself under the name its files use (`B`), and a test holds it
  to the rule: every global a function of the three files uses is a name of the package
  (`test_what_a_function_of_the_package_uses_the_package_has`; it fails on the base, for `B`).
- **A helper I first called `_ledger`** shares its name with a method of `Brain`. It is `_ledger_in`.

## Did a wider assumption change?

Yes: **I had asked what a crash between two writes leaves, and not what somebody reading between them
sees.** The same question, put to the other places where one process writes two files and another reads them:

- the brain saves the world model, then writes the answer: the client reads only the answer, and the receipt
  is in the world model already;
- `brain next` writes `client.json`, then the request: the brain reads only the request;
- `brain stopped` reads the saved ledger's rows and `client.json`: each is one file, replaced whole.

The pair of the count and the world model was the one place where a reader makes a name out of two files.

I recommend the scope the review names: the takeover's identity for a reader during the save and after a save
that failed, the crash behaviour, and the controls it lists; and a confirmation that `e4a267cd` is another
version's.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 422 tests`, `OK`, three runs in a row, none skipped |
| The review's `write_window.py`, four modes, and `save_faults.py`, unchanged | the table and the paragraphs above |
| The scripts of every earlier review | each ends as on the base |
| `test_rereview11.py` on the base (a throwaway worktree) | of 12: 12 fail |
| The state made by the `e4a267cd`, `7cf7d73c`, `c412de4d` and `29797ba0` packages out of the repository's history | in the suite: eighteen tests (they skip where the history lacks the commit; none skipped here) |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem |
| Seventy-eight planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes and the three simulated fights | output identical to the base's |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's eleven first. All were planted in throwaway worktrees made from a
local commit that has the tests of the code commit and its code, never in the repository's own tree. The code
commit differs from it in the wording of two comments in `client.py`, shortened to keep the file at 400
lines. The worktrees were clean after the runs and are removed.

| Planted defect | Random walk (40 walks) | Tests of the last ten reviews |
|---|---|---|
| A name is spoken of while a takeover is being saved | not caught | 6 fail |
| The count is raised before the world model is written, as before | not caught | 5 fail |
| The world model is written before the count's file says saving | not caught | 4 fail |
| The save that a brain left unfinished is not counted by the next brain | not caught | 1 fails |
| `brain stopped` counts a save that a living brain has not finished | not caught | 3 fail |
| `brain stopped` never counts a save that was left, with nobody home | not caught | 1 fails, 2 errors |
| Word is written down for the takeover that is being saved | not caught | 3 fail |
| A save that failed is not done again in full | not caught | 2 fail |
| The third write leaves saving standing | not caught | 7 fail |
| The count and the file are read once, not together | not caught | 1 fails |
| Saving is read from anything that is not nothing | not caught | 1 fails |
| The hold is named by the old file's bytes alone | not caught | 11 fail |
| The count of takeovers is not in the name | not caught | 9 fail |
| The time the file was written is not in the name | not caught | 1 fails |
| A takeover that is saved is not counted | not caught | 8 fail |
| A takeover is counted when a brain looks at it, not when one saves it | 4 | 10 fail |
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
| A ledger another version kept is taken at its word | 18 | 55 fail, 1 errors |
| A ledger this version kept is held all the same, at every start | not caught | 59 fail, 8 errors |
| The hold is twenty calls, not the minute's thirty | not caught | 47 fail |
| The operator's word lets the hold go with no minute after it | 1 | 15 fail |
| The word counts from whenever it claims to have been said | not caught | 1 fails |
| The hold has a new name each time a brain starts | not caught | 10 fail |
| The listing does not show the hold before a brain has taken the ledger over | not caught | 5 fail, 10 errors |
| A ledger that cannot be read is a first start | not caught | 7 fail, 8 errors |
| The brain does not put its number on the ledger | 34 | 60 fail, 4 errors |
| This version's request is published under the name every earlier brain reads | not caught | 13 fail |
| A request under the old name is answered when it carries the number | not caught | 1 fails |
| The brain does not look at files under the old name, so they are never removed | not caught | 1 fails, 2 errors |
| The brain opens the requests of every protocol | not caught | 1 fails |
| What a dead `brain next` left under another name is not swept | not caught | 1 fails |
| With nothing to answer, `brain next` goes round without waiting | not caught | 1 fails |
| With nothing to answer, a brain is started every round | not caught | 1 fails |
| A batch an older version left waiting is printed | not caught | 30 fail |
| A client file without this version's number is read | not caught | 20 fail |
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
| A loose call leaves the ledger after a minute | 40 | 51 fail, 1 errors |
| A held batch is let go by itself after fifteen minutes | 33 | 6 fail |
| The receipt is not checked | 2 | 13 fail |
| A relay that asked holds the batch before it is printed | 4 | 1 fails |
| A batch nothing is on record of is taken as never printed | 26 | 40 fail |
| A batch known to be unprinted is held as if a relay had it | 4 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 8 fail |
| Asking what is held lets it all go | 40 | 11 fail, 8 errors |
| An older request's `lost` is read as back | not caught | 1 fails |
| A number typed is not the number kept | not caught | 3 fail |
| The brain paces over a batch it has not placed | not caught | 1 fails |
| A batch waiting in an older client file is printed | not caught | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 9 | 8 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 15 fail |
| An older ledger's held calls are dropped on loading | not caught | 7 fail |
| A failed tick is not saved | not caught | 4 fail |
| The last resort does not wait when nothing can be sent | not caught | 2 fail |
| An empty answer to an action is a taken action | not caught | 1 fails |
| The last resort does not look at my profile | not caught | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 2 fail |

## Size

Player code 4,285 lines in 23 files (base: 4,185); tests 8,027 lines (7,744). `world.py` is 329
lines (278) and `brain/client.py` 400 (356). No file of the brain is over 400. Over the AP6 budget, as
before: `activities/battle.py` 685 and `budget.py` 408. Sixteen functions branch more than 12 ways, the same sixteen; `stopped` is one of them, at 14 where it was 15. Config constants 49. Nothing ships switched
off.

## Known limits

1. **The count is a file**, as said before: lost or put back with a word still kept, it can repeat a name.
2. **While a brain is home and cannot write the world model, the takeover cannot be spoken of.** The listing
   says to say it again. If the disk does not come back, the brain has to be ended; `stopped` then counts the
   save it left and the file has a name.
3. **`brain stopped` can take up to two seconds** when it finds a takeover being saved, and takes the brain's
   lock for a moment when it counts a save that was left. A `brain next` at that instant looks again.
4. **Anything that makes a `World` on a folder counts a save that was left there**, a script included. If
   the brain that began the save is alive, it counts again when it saves. The name moves on; nothing is let
   go.
5. The limits of the earlier handoffs stand: the number is kept by hand; a word said before the new relay's
   first ask does not cover the predecessor's last batch; the word is taken on trust; a new live folder has no
   hold; the hold stops a fight too; and no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material.

## Open

- For the director: this review reached me a day late. Reviews are published on `chatgpt/review-*` branches; I
  now look there before I say that something is unreviewed.
- AP2's first part is issued again on top of this head; its SHA is in the correction message.
