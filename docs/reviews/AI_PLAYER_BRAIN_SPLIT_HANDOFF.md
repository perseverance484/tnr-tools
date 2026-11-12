# AI player overhaul: the split of `brain.py`, implementation handoff

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-12.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-brain-split
Base: e4a267cd1ab5ff85c3b2399bab713f2870da6ccb (fable/ai-player-ap1)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Integration target: the AI player line (fable/ai-player-ap1, then AP2). Nothing of it is on main; main was at
        4816b6c9 when this was written.
```

## Why now, and on what

The ruling is that `brain.py` is split after AP1's correctness is accepted, before AP2, as a separate change
that preserves behaviour. AP1's correction was accepted at `7cf7d73c`
(`docs/reviews/AI_PLAYER_AP1_REREVIEW10_REVIEW.md` on `chatgpt/review-ai-player-ap1-rereview10` @ `a1c56c50`).

One thing is still open on AP1, and this handoff does not hide it: the base here is `e4a267cd`, which is
`7cf7d73c` plus the correction of the second review's H2 (a takeover is counted; protocol 3). That correction
has not had its re-check yet. The split does not depend on what that re-check finds. If it leads to a change in
code that moved, I will make the change on `fable/ai-player-ap1`, bring it here, and issue a new SHA. I
recommend reviewing `e4a267cd` first.

## Objective

Turn the one file `player/brain.py` (883 lines; the AP6 budget is 400 a file) into the package `player/brain/`,
by moving code. No behaviour changes, on the command line or inside.

## What moved where

Every block was copied by its line span by a script; nothing was retyped.

| File | Lines | What is in it |
|---|---|---|
| `player/brain/core.py` | 359 | `IDLE_HOLD`, `BLOCK_FOR`, `QUIET`; the class `Brain` with its 19 methods; `_lead`, `_wire`, `_crashed` |
| `player/brain/resident.py` | 123 | `_lock`, `_after_crash`, `_answered`, `REQUEST`, `serve`, `answer`, `run` |
| `player/brain/client.py` | 356 | `_transcript`, `_collect`, `_taken`, `_client`, `SUPERSEDED`, `RETRY_IN`, `_who`, `_a_relay`, `_a_batch`, `_a_waiting_batch`, `_a_word`, `next_batch`, `_greet`, `_exchange`, `_sweep`, `_owed`, `_await`, `stopped`, `_held`, `put` |
| `player/brain/__init__.py` | 96 | the page that was the file's docstring, with four lines added on where things are; `_setting`, `main`; and every name the file had |
| `player/brain/__main__.py` | 6 | `python3 -m player.brain` |

`player/brain.py` is gone. 55 definitions were in it (36 at the top, and the 19 methods). 51 are the same text
in the package. The other four differ in seven lines, and those seven are the whole change inside moved code:

| Where | Was | Is |
|---|---|---|
| `resident.serve` | `return answer(brain, live, path)` | `return B.answer(brain, live, path)` |
| `resident.run` | `lock = _lock(live)` | `lock = B._lock(live)` |
| `resident.run` | `brain = Brain(live)` | `brain = B.Brain(live)` |
| `resident.run` | `serve(brain, live, path)` | `B.serve(brain, live, path)` |
| `client._exchange` | `batch = _await(live, seq, rid, req, sleep)` | `batch = B._await(live, seq, rid, req, sleep)` |
| `client._await` | `lock = _lock(live)` | `lock = B._lock(live)` |
| `client._await` | `serve(Brain(live), live, req)` | `B.serve(B.Brain(live), live, req)` |

`B` is the package itself (`from .. import brain as B`).

### Why those five names go through the package

`Brain`, `serve`, `answer`, `_lock` and `_await` are the places where the tests, and the reviews' scripts,
take the player apart: they put a brain with a clock, a counting lock or a silent `_await` in `player.brain`
and expect the rest to use it. In one file that was a lookup in the module's own names. In a package the same
lookup has to be said. So the code that calls one of the five calls it as `B.name`, and everything else calls
its neighbours directly.

The result: **no test file changed, and no script of any review needs a change.** The other way would have
been to move the patch targets in the tests (fifteen lines) and to leave every published reproducer that puts
a clock on `brain.Brain` broken. I took the way that keeps the evidence of every review so far runnable.

For the same reason `__init__.py` carries every name the file had, the names it imported among them (57 in
all): one review script runs code of its own inside `player.brain`'s namespace.

### What is new, and is not moved code

- The three short pages at the top of `core.py`, `resident.py` and `client.py`, and their imports.
- `__main__.py`, six lines. As a file, `python3 -m player.brain` ran `brain.py` itself; as a package it runs
  this. The command, its arguments and the process's command line are as before (`pgrep -f "player.brain
  run"` on the operator's page still finds the resident: under test).
- `player/tests/test_brain_package.py`, six tests, for what the split itself has to keep: the command line in
  processes of its own (the usage text, `set`, `stopped`, a resident that answers a relay over the files and
  is the only one), every name, and the five lookups. One test that was there already starts the resident in
  a process (the one-brain lock, in `test_relay.py`); it passes as it was.
- `docs/design/AI_PLAYER_OVERHAUL.md`: one line names the package where it named the file.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 409 tests`, `OK`, three runs in a row, none skipped: the 403 that were there, their files byte for byte as at the base, and the six new ones |
| `git diff --stat e4a267cd HEAD -- player/tests` | one file, the new one |
| `python3 docs/reviews/evidence/ai_player_brain_split/moved_check.py e4a267cd player/brain/core.py player/brain/resident.py player/brain/client.py player/brain/__init__.py` | 55 definitions in the old file; 51 the same text; the seven lines above; none missing, none new |
| `PYTHONPATH=. python3 docs/reviews/evidence/ai_player_brain_split/cli_compare.py e4a267cd` | the old file and the package run the same session in processes of their own (no command, a bad one, `status`, `set`, `next` five ways, `put` three ways, `stopped` three ways, `run` twice, SIGTERM): 19 of 19 give the same exit code and the same words, and leave the same files |
| The names of `player.brain` before and after | 57 before; all 57 after, and the three submodules |
| Every script of every review (rounds 4 to 12), unchanged | each ends as on `e4a267cd`, the one that runs code inside `player.brain` among them |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of the base |
| The two fuzzes and the three simulated fights | output identical to the base's |
| Sixty-eight planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests. The table is the base's, row for row: the same walks catch the same defects and the same number of tests fail |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both (the scan of the player's code finds the package) |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |
| `python3 scripts/player_size.py` | below |

The planted defects are the 68 of the last AP1 handoff, each put into the file of the package that now holds
its text, in throwaway worktrees made from a local commit that has the code of the code commit. The six new
tests were added after that commit. The worktrees were clean after the runs and are removed.

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

Player code 4,185 lines in 23 files (base: 4,128 in 19). The 57 more are the pages and imports at the top of
the new files. Tests 7,744 lines (7,595). No file of the brain is over 400 lines: the largest is `core.py`
at 359. Still over: `activities/battle.py` 685 and `budget.py` 408, which the ruling does not cover. Sixteen
functions branch more than 12 ways, the same sixteen. Config constants 49. Nothing ships switched off.

## Source and provenance

No game source, generated contract or capture is touched or read by this change. The comparison base for every
check above is `e4a267cd`, out of the repository's own history.

## Risk and debt

1. **A submodule that refers to its own package.** `resident.py` and `client.py` import `player.brain` as `B`
   for the five names. It is the price of leaving the tests and the scripts alone. If the reviewer would rather
   have the pieces call each other directly and the tests patch the piece, that is a second, separate change;
   I would not mix it into a move.
2. **Names in `__init__.py` that it does not use itself**, marked as such in the file. They are the old
   module's namespace.
3. **The approved brief still says `player/brain.py`** in its AP1 step, and the design's port table says
   `brain.py`. I changed the design's architecture line and left the brief's words as approved.
4. **AP2 is not on this yet.** `fable/ai-player-ap2` does not touch `brain.py`; it is brought onto the split
   after this handoff, by merge.
5. Where I would look hardest: the `B` lookups under a patch (the tests that stand in for `Brain`, `serve`,
   `answer`, `_lock`, `_await`), and the real-process paths: `brain next` starting a resident
   (`subprocess.Popen([... "-m", "player.brain", "run"])`), and the resident's lock.

Nothing was implemented beyond the move. No behaviour, constant, message or file format changed. The protocol's
number stays 3: no record changed its meaning and no rule for admitting calls changed.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material. No live relay and no
browser session were exercised.
