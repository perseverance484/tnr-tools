# AI player overhaul, phase AP1: correction handoff after the review of ce1be6e9

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-13, in answer to the review of
`ce1be6e9` ("request changes": the cases of the review before it are corrected, H1 stays closed; one medium
finding).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: ce1be6e98eb39550e79806c5c8f9da87f67fa4eb
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW12_LANE_A_REVIEW.md on
        chatgpt/review-ai-player-ap1-rereview12-lane-a @ 39070bc9 (evidence; not merged)
Base of this correction: ce1be6e98eb39550e79806c5c8f9da87f67fa4eb. Not rebased: this head is two commits on it.
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

The finding is **confirmed and corrected**. The review's reproducer, unchanged, on the reviewed head and now:

| The review's case | On `ce1be6e9` | Now |
|---|---|---|
| `window`: a process of its own makes a `World` and says `stopped all`, between the resident's first write and its second, while the resident has the brain's lock | the `World` closes the resident's save: the count's file says (1, not saving). A word is taken for the name of that moment. The resident finishes on the count it read before, 1. When the old file is back it has that name: 4 calls after 9 s, nothing held | the `World` writes nothing. No word is taken: the listing says a brain is saving the takeover. When the old file is back: no call, all 30 held; counts 1 and 2. The script stops at its check that the word names the later hold |
| `failed` | no call, 30 held; the script stops at its count check (2, not 1) | the same |
| `before`, `after` | pass | pass |

`write_window.py` and `save_faults.py` of the review before, unchanged: each mode ends as it did on `ce1be6e9`.

`player/tests/test_rereview12.py` has the finding as six classes, 14 tests. On `ce1be6e9`, in a throwaway
worktree with the changed test files copied in: **10 fail, 4 pass**.

- Four are the finding and what it rests on: the review's reproduction, the same with a whole `Brain` made in
  the reader's place, a `World` that is made writes nothing, and a save that is counted from outside between its
  writes does not finish on the count it read before.
- Two are about who counts a save that was left: not a brain made while another process has the lock, and not
  on the strength of a lock that was given back.
- Four set `ce1be6e9` against itself as a version before. They are what holds it to the new number here.
- The four that pass are controls that held before and must still hold: the review's own crash table (the
  brain ends before any write and at each of the three, and the next one starts under the lock), a word said
  just before the third write, and a left save counted by a brain that has the lock and by one made with
  nobody home.

To load on `ce1be6e9` the tests need one name of the new code; it was set in the test process, and no file of
that checkout was changed.

## Three things the last handoff said that were wrong, or said too much

1. **Known limit 4** said that anything which makes a `World` on a folder counts a save that was left, and that
   when the brain that began the save is alive "the name moves on; nothing is let go". The second half is the
   finding. It holds for a `World` made after a failed save has returned. It does not hold for one made while
   the save is running.
2. **"Has no name between the first and the third writes."** Once the second write is done the hold is a row of
   the saved ledger, and `brain stopped` speaks of it by that row though "saving" still stands. That is the
   brain's own hold and it is safe; the review shows it and so does a test here
   (`test_word_said_before_the_third_write_names_the_hold_that_is_saved`). What cannot be named between the
   writes is the file that was taken over. The comment in `World.save` says it that way now.
3. **"All 12 fail"** was a count of tests, and the note went on to split it: six about the finding, two about
   helpers the base lacks, four about the number. The review is right that it is not twelve reproductions. The
   split above is put the same way.

## What was built

### Making a `World` writes nothing

`player/world.py` `World.__init__`, `counted`.

A `World` is what anything uses to read a live folder. Its constructor called `counted`, so a reader wrote the
count's file. It no longer does. `counted` is still the one function that closes a save that was left; it now
has three callers, each under the brain's lock.

### A save that was left is counted under the brain's lock, and nowhere else

`player/brain/resident.py` `_left_save`, `_home`, `_lock`, `_HELD`; `player/brain/core.py` `Brain.__init__`.

A brain that starts asks `_left_save` before it makes its `World`:

- **Its own process has the lock** (the resident; a `brain next` that answers for itself). It counts. `_lock`
  now remembers the locks this process has, and a lock is over when its file is closed.
- **Nobody has the lock** (a brain made without one: a test, a review's script). It takes the lock, counts,
  and gives it back. This is the rule `brain stopped` already had.
- **Another process has the lock.** A brain is home. Nothing is counted.

`brain stopped` (`_on_disk`) is as it was: it counts only when it can take the lock.

Every brain a running player makes is made under the lock, in one of two places (`resident.run`,
`client._await`). So in a running player a save can only be closed by the brain that holds the lock, after
the brain that began it is gone.

### A save does not finish on a count that was passed

`player/world.py` `World.save`.

The third write read the count before the first write and added one. It reads it again now. Under the lock
nothing can count in between. A brain made without a lock is not protected by one, and for that brain this is
what keeps the count from going back to a number a word was taken for.

### The number is 5

`player/relay.py`. Who may close a save decides which names a word can be taken for, and so when a hold can be
let go. By the rule the number changes, as the review says. `ce1be6e9` is a version before this one; four
tests hold it to that with its own package.

## Why the review's sequence cannot happen now

The word was taken because a reader made the count's file say "not saving" over a file that was still the old
one. Now the only writers of the count's file are a save (`World.save`) and `counted`, and `counted` runs only
for whoever holds the brain's lock. While the resident saves, it holds the lock: a reader's `World` writes
nothing, a reader's `Brain` cannot take the lock and counts nothing, and `brain stopped` finds "saving", cannot
take the lock, and takes no word.

## Found while correcting

- **Every existing test passed unchanged** once the count moved from `World` to the brain's start: none of
  them made a bare `World` and expected the count to move. That is also why none of them caught the finding.
- **`test_rereview11.py`'s harness is now a class of its own** (`AFolderOfAnotherVersion`), so the new tests
  are made of it. Its tests are unchanged; `dies_at` learned the first write.

## Did a wider assumption change?

Yes: **I had asked what a reader sees between two writes, and not what a reader does.** The same question,
put to everything else that only looks at a live folder:

- `brain stopped` writes its own file (`client.json`, under the client's lock) and, with nobody home, the
  count under the brain's lock;
- `brain status` reads `status.json` and writes nothing;
- `brain set` writes `control.json`, which is its to write;
- a `World` that is made writes nothing now, and neither does `found` or `seen`.

`World.save` and `World.event` write, and both are the brain's. Nothing else that reads a folder writes to it.

I recommend the scope the review names: who closes a save that was left and how that meets a save that is
running, with the reader, failure, crash and protocol controls kept.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 436 tests`, `OK`, three runs in a row, none skipped |
| The review's reproducer, four modes, unchanged | the table above |
| `write_window.py` (four modes) and `save_faults.py` of the review before, unchanged | each ends as on `ce1be6e9` |
| `test_rereview12.py` on `ce1be6e9` (a throwaway worktree) | of 14: 10 fail, 4 pass |
| The state made by the `ce1be6e9`, `e4a267cd`, `7cf7d73c`, `c412de4d` and `29797ba0` packages out of the repository's history | in the suite: twenty-two tests (they skip where the history lacks the commit; none skipped here) |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem |
| Eighty-five planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes and the three simulated fights | output identical to that of the heads before |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's seven first. All were planted in throwaway worktrees made from a
local commit that has the code and the tests of the code commit, never in the repository's own tree. The
worktrees were clean after the runs and are removed. The random walk does not model a second process, so it
catches none of this review's seven; the tests do.

| Planted defect | Random walk (40 walks) | Tests of the last eleven reviews |
|---|---|---|
| A World that is made counts a save that was left | not caught | 5 fail |
| A brain that starts counts a left save whoever has the lock | not caught | 3 fail |
| A brain whose own process has the lock does not count a left save | not caught | 3 fail |
| The lock this process has is not remembered | not caught | 4 fail |
| A lock that was given back still counts as this process's | not caught | 1 fails |
| A brain made with nobody home does not count a left save | not caught | 2 fail |
| The save's third write uses the count read before the first | not caught | 1 fails |
| A name is spoken of while a takeover is being saved | not caught | 9 fail |
| The count is raised before the world model is written, as before | not caught | 12 fail |
| The world model is written before the count's file says saving | not caught | 9 fail |
| The save that a brain left unfinished is not counted by the next brain | not caught | 5 fail |
| `brain stopped` counts a save that a living brain has not finished | not caught | 5 fail |
| `brain stopped` never counts a save that was left, with nobody home | not caught | 1 fails, 3 errors |
| Word is written down for the takeover that is being saved | not caught | 5 fail |
| A save that failed is not done again in full | not caught | 2 fail |
| The third write leaves saving standing | not caught | 14 fail, 1 errors |
| The count and the file are read once, not together | not caught | 1 fails |
| Saving is read from anything that is not nothing | not caught | 1 fails |
| The hold is named by the old file's bytes alone | not caught | 19 fail |
| The count of takeovers is not in the name | not caught | 17 fail |
| The time the file was written is not in the name | not caught | 1 fails |
| A takeover that is saved is not counted | not caught | 15 fail |
| A takeover is counted when a brain looks at it, not when one saves it | 4 | 21 fail, 1 errors |
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
| A ledger another version kept is taken at its word | 18 | 66 fail, 3 errors |
| A ledger this version kept is held all the same, at every start | not caught | 67 fail, 9 errors |
| The hold is twenty calls, not the minute's thirty | not caught | 58 fail |
| The operator's word lets the hold go with no minute after it | 1 | 16 fail |
| The word counts from whenever it claims to have been said | not caught | 1 fails |
| The hold has a new name each time a brain starts | not caught | 11 fail |
| The listing does not show the hold before a brain has taken the ledger over | not caught | 5 fail, 18 errors |
| A ledger that cannot be read is a first start | not caught | 10 fail, 15 errors |
| The brain does not put its number on the ledger | 34 | 68 fail, 4 errors |
| This version's request is published under the name every earlier brain reads | not caught | 15 fail |
| A request under the old name is answered when it carries the number | not caught | 1 fails |
| The brain does not look at files under the old name, so they are never removed | not caught | 1 fails, 2 errors |
| The brain opens the requests of every protocol | not caught | 1 fails |
| What a dead `brain next` left under another name is not swept | not caught | 1 fails |
| With nothing to answer, `brain next` goes round without waiting | not caught | 1 fails |
| With nothing to answer, a brain is started every round | not caught | 1 fails |
| A batch an older version left waiting is printed | not caught | 34 fail |
| A client file without this version's number is read | not caught | 24 fail |
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
| A loose call leaves the ledger after a minute | 40 | 61 fail, 3 errors |
| A held batch is let go by itself after fifteen minutes | 33 | 6 fail |
| The receipt is not checked | 2 | 13 fail |
| A relay that asked holds the batch before it is printed | 4 | 1 fails |
| A batch nothing is on record of is taken as never printed | 26 | 44 fail |
| A batch known to be unprinted is held as if a relay had it | 4 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 14 fail |
| Asking what is held lets it all go | 40 | 11 fail, 16 errors |
| An older request's `lost` is read as back | not caught | 1 fails |
| A number typed is not the number kept | not caught | 3 fail |
| The brain paces over a batch it has not placed | not caught | 1 fails |
| A batch waiting in an older client file is printed | not caught | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 9 | 8 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 16 fail |
| An older ledger's held calls are dropped on loading | not caught | 7 fail |
| A failed tick is not saved | not caught | 4 fail |
| The last resort does not wait when nothing can be sent | not caught | 2 fail |
| An empty answer to an action is a taken action | not caught | 1 fails |
| The last resort does not look at my profile | not caught | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 2 fail |

## Size

Player code 4,330 lines in 23 files (`ce1be6e9`: 4,285); tests 8,265 lines (8,027). `world.py` is
337 lines (329), `brain/resident.py` 152 (123), `brain/core.py` 362 (359), `brain/client.py`
400 (400). No file of the brain is over 400. Over the AP6 budget, as before: `activities/battle.py` 685 and
`budget.py` 408. Sixteen functions branch more than 12 ways, the same sixteen. Config constants 49. Nothing ships switched off.

## Known limits

1. **The exclusion is the brain's lock, and a brain made without one is outside it.** Two brains that a
   script makes on one folder with no lock can still close each other's save; with the count read again for
   the third write the count does not go back, but a script's brain that ends between its second and third
   write, after another has counted for it, leaves a saved takeover that was counted once for two. No running
   player makes a brain without the lock.
2. **A process remembers its locks by the folder's path.** A lock taken through another path to the same
   folder (a link) is found as well, by its real path. A lock file opened by other code than `_lock` is not
   remembered.
3. **A brain made by a script while a brain is home** sees the old file and the count of that moment, and
   would name a hold by them. It is not the folder's brain and saves nothing a player uses; it is not stopped
   from being made.
4. The limits of the earlier handoffs stand: the count is a file; while a brain is home and cannot write the
   world model the takeover cannot be spoken of; `brain stopped` can take two seconds; the number is kept by
   hand; a word said before the new relay's first ask does not cover the predecessor's last batch; the word is
   taken on trust; a new live folder has no hold; the hold stops a fight too; and no real relay has driven any
   of it.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material.

## Open

- AP2's first part is corrected after its own review and issued again on top of this head; its SHA is in the
  correction message.
