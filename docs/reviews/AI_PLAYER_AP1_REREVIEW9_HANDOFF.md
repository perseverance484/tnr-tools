# AI player overhaul, phase AP1: correction handoff after the review of 29797ba0

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`29797ba0` ("request changes": no new finding; it requires what my last handoff left open as known limit 2).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 29797ba0f769152381e71710f812605be9e0bfea
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW8_REVIEW.md on chatgpt/review-ai-player-ap1-rereview8 @ 56dfb24d
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

The requirement is **accepted and built**. The review's script, unchanged, gives on `29797ba0` what the
review reports, and on this head stays inside both limits in all three of its cases.

| The review's case | On `29797ba0` | Now |
|---|---|---|
| No acknowledgement | 4 calls sent at once; 34 in a minute, 24 in the world lane | no call sent; the minute holds relay A's four calls and nothing else |
| Acknowledgement, the old relay's last calls just before it | `stopped all` names nothing; 4 calls at once; 34 and 24 | `stopped all` names the hold; the first calls go a minute after the word; 30 and 20 |
| Acknowledgement, then 60 seconds | 30 and 20 | `stopped all` names the hold; calls go at once, the minute being over; 30 and 20 |

Every script of the earlier reviews still shows its case closed (G, F, E, D, C, B and A series, with the
adaptations already on record). Where one of them looks at an older version's ledger, it now also shows the
30 calls held for the update: F1 prints `old loose calls: 51` where it printed 21, and the adapted G1 counts 4
calls in the minute, relay A's own, where it counted 30 and 20, because nothing of this version is sent
before the operator has spoken.

`player/tests/test_rereview8.py` has the requirement as class Q1, with two more classes: 15 tests. On
`29797ba0`, 9 fail, 4 error and 2 pass. The two that pass are the controls: an ordinary restart, and a first
start. The four errors need a name the old code does not have (the hold, or the ledger's number). To load
there at all the tests need `budget.UPDATE`; it was set in the test process, and no file of the old checkout
was changed.

## What was built

### A ledger says whose it is, and one that is another version's is held for a minute's calls

`brain.py` `Brain._take_over`, `_held`, `stopped`; `budget.py` `Budget.taken_over`, `UPDATE`; `world.py`
`found`, `World.found`, `World.found_at`.

- **Whose ledger.** The brain puts the protocol number on the ledger it keeps (`budget.protocol` in
  `world.json`), with the first thing it saves. A world model on disk whose ledger does not carry this
  version's number, as the integer it is, was kept by another version. So was one that cannot be read.
- **The hold.** A brain that takes such a ledger over holds a whole minute's calls beside whatever the ledger
  itself says: 30 loose calls (`CALL_LIMIT`), in a lane of their own, under one id. With them in the ledger
  no lane has room: no read, no action of a turn, no recovery call is sent. The relay gets its `brain next`
  line and a six-second wait.
- **The id is made from the file that was taken over** (`update-` and a short print of its bytes). So the
  hold has one name whoever looks: `brain stopped` shows it before any brain of this version has started, a
  brain that ends before it has saved leaves the next one to hold the same, and a second update is another
  file and another name.
- **The word.** `brain stopped all`, or `brain stopped update-…`, is the operator's word that every relay from
  before the update is stopped. It goes the way every such word goes: one row naming that one id, taken once
  by the brain, harmless when taken twice. The 30 calls are then counted from the moment the word was said,
  and leave the minute sixty seconds later. So the first call goes a minute after the word; if the word is
  already a minute old when the relay first asks, at once.
- **The word is never counted from before the file was last written.** A row that claims an earlier time is
  taken as said now.
- **What is not touched.** The holds the old ledger does name stay as they were and are let go one by one, as
  before. A batch of this version waiting to be printed, and a receipt, are delivered as before. A ledger
  this version kept is taken as it stands: an ordinary restart has no hold. A first start has no ledger and
  no hold.

`relay.PROTOCOL` stays 1. Every ledger written before this head has no number, `29797ba0`'s included, so
each of them is taken over with the hold.

### The operator's page

`player/OPERATOR.md`, "After the player's code is updated", now says what is built: no call until the word,
a minute after it, the order to follow (end the old brain; end the old relays and see them end; say so; start
a relay), that the word is for this one update, and that it must be true. It also says where there is no
hold: a new live folder, and an ordinary restart.

## Found while correcting

- **The random walk now has this event.** At any moment the ledger turns into one that another version kept:
  its number goes, and with it some of the calls it held for relays that have not come back. Those relays go
  on. The walk's operator says `stopped all` only when every relay but the running one is over, as before.
  200 walks, no problem. Its "ledger is never behind" check is made only on a ledger of this version's, and
  a batch whose calls were let go that way is left out of its "still held" check: nothing stands for those
  calls but the update's minute, which the "cap" check covers.
- **A world model that is not an object** (a list, a string) raised when it was loaded. It is now read as
  one that cannot be read: nothing of it is used, and the hold stands (`world.py` `load`).
- **Ten tests of earlier rounds looked at an older version's ledger and counted every held call.** They now
  count the old ledger's own holds and the update's minute apart. Two of them let the update's minute go, as
  of a minute before, to keep counting what they were written to count: the old relay's four calls against
  this version's batches.

## Did a wider assumption change?

Yes, one, and it is the one the review asked for: **a ledger is trusted only when this version kept it.**
Before, a brain took any ledger at its word. Nothing changes for a brain that restarts on its own ledger.

What the operator has to do after an update changes with it: the player now waits for the word.

I recommend the scope the review named: the admission boundary after a takeover, how it lasts across brains
and retries, the old-package upgrade controls, and this version's own pending and receipt delivery.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 369 tests`, `OK`, three runs in a row, none skipped |
| The review's script, unchanged | the first table |
| The scripts of the earlier reviews | still closed; two print other figures, as said above |
| The state of the review's script, made by the `442a6311` package out of the repository's history | in the suite: `test_the_version_before_itself` (it skips where the history lacks the commit). The same state from recorded files (`fixtures/upgrade_442a6311_forgotten`) is always run |
| `test_rereview8.py` on `29797ba0` (a throwaway worktree) | of 15: 9 fail, 4 error, 2 pass |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,393 calls, no problem (fewer calls than before: the new event holds the player until the operator speaks) |
| Fifty planted defects, in throwaway worktrees | every one fails at least one test; the unchanged code passes the 40 walks and the tests |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | same output as on `29797ba0` |
| The three simulated fights | 14, 9 and 13 turns; 23, 27 and 24 calls in the fullest minute; no action delayed: as on `29797ba0` |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's nine first, then the last review's seven. All were planted in
throwaway worktrees made from a local commit of this work, never in the repository's own tree. That commit
has the code of the code commit; one case was added to a test after it. The worktrees were clean after the
runs and are removed.

| Planted defect | Random walk (40 walks) | Tests of the last seven reviews |
|---|---|---|
| A ledger another version kept is taken at its word (what this review requires) | 16 | 17 fail, 4 errors |
| A ledger this version kept is held all the same, at every start | not caught | 39 fail, 6 errors |
| The hold is twenty calls, not the minute's thirty | not caught | 19 fail |
| The operator's word lets the hold go with no minute after it | 1 | 5 fail |
| The word counts from whenever it claims to have been said | not modelled | 1 fails |
| The hold has a new name each time a brain starts | not caught | 3 fail |
| The listing does not show the hold before a brain has taken the ledger over | not modelled | 3 fail |
| A ledger that cannot be read is a first start | not modelled | 1 fails |
| The brain does not put its number on the ledger | not caught | 41 fail, 6 errors |
| This version's request is published under the name every earlier brain reads | not modelled | 5 fail |
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
| `true`, or 1.0, counts as the number | not modelled | 4 fail |
| The brain keeps its receipt without the number | 19 | 7 fail, 1 errors |
| A replaced relay's batch is taken as run | 39 | 9 fail, 1 errors |
| Any replaced relay's return counts as a held batch being over | 25 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 24 fail |
| A held batch is let go by itself after fifteen minutes | 33 | 6 fail |
| The receipt is not checked | 2 | 11 fail |
| A relay that asked holds the batch before it is printed | 3 | 1 fails |
| A batch nothing is on record of is taken as never printed | 23 | 20 fail |
| A batch known to be unprinted is held as if a relay had it | 4 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 5 | 2 fail |
| Asking what is held lets it all go | 39 | 8 fail |
| An older request's `lost` is read as back | not modelled | 1 fails |
| A number typed is not the number kept | not modelled | 3 fail |
| The brain paces over a batch it has not placed | not modelled | 1 fails |
| A waiting batch in this version's file is not checked for its shape | not modelled | 1 fails, 1 errors |
| `stopped all` also names the running relay's batch | 10 | 7 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 6 fail |
| An older ledger's held calls are dropped on loading | not modelled | 7 fail |
| A failed tick is not saved | not modelled | 4 fail |
| The last resort does not wait when nothing can be sent | not modelled | 2 fail |
| An empty answer to an action is a taken action | not modelled | 1 fails |
| The last resort does not look at my profile | not modelled | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 2 fail |

The walk catches the first of them in 16 of 40 walks: with no hold after a takeover, the relays whose calls
the old ledger let go make them beside this version's.

## Size

Player code 4,083 lines in 19 files (`29797ba0`: 4,017); tests 6,902 lines (6,482), and a third recorded
fixture of three small files. `brain.py` is 882 lines (859), `battle.py` 685, `budget.py` 408 (AP6 budget
400 a file: three files are over it now). Sixteen functions branch more than 12 ways (sixteen). Config
constants 49. Nothing ships switched off. The code change is in `brain.py`, `budget.py` and `world.py`: 74
lines added and 8 removed.

The split of `brain.py` waits for acceptance, as ruled.

## Known limits

1. **The word is taken on trust, and here nothing stands behind it.** For a batch the ledger names, a relay
   that was wrongly said to be stopped still has its calls written down. For the update's minute there is
   nothing written down: if a relay from before the update is running when the operator says it is not, its
   calls are counted by nobody. The page says so.
2. **A new live folder has no hold.** With no ledger on disk there is nothing to take over, so a player
   started on an empty folder sends calls at once. Moving an old folder aside is the operator's act, and so
   is making sure nothing from before is running.
3. **A step back to an older version on the same folder is not covered**, as before. An older brain keeps
   the number it finds on the ledger without keeping this version's rules, so a ledger that went through
   one would be trusted when this version came back to it.
4. **The hold stops a fight too.** A fight that is on at the update gets no action until a minute after the
   word. That is what "no call" means; the cover is not to update with a fight on.
5. The limits in the earlier handoffs stand: the number is kept by hand; a brain of this version does not
   step aside for a later protocol; the ledger lives in `world.json`; the relay doing its lines in order; and
   no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the director: the three token decisions (light polls on his turn; short-lived relays started by a
  script; whether to keep archiving his turn's opening state). Duet's three relay transcripts. Whether
  `player/OPERATOR.md` goes into the next session brief as it is.
- The live test was briefed against `06358ca5`. It should run this head. Its brief starts from a new live
  folder, so the hold does not arise there; limit 2 is the reason its first set-up steps matter.

AP2 was begun on the director's word of 2026-11-12, on its own branch from this head. The split of
`brain.py` is not begun.
