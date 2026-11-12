# AI player overhaul, phase AP1: correction handoff after the review of 442a6311

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`442a6311` ("request changes": a ruling on `LOOSE_FOR`, four high findings, two medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 442a63119d2fa3fe033877bedc86f5df8cd9be00
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW3_REVIEW.md on chatgpt/review-ai-player-ap1-rereview3 @ 592ba138
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

The ruling is accepted and done. All six findings are **confirmed**: each was reproduced on `442a6311` with
the review's own script, unchanged.

On this head three of those scripts run unchanged (C3, C3b, C4). The others cannot, because the corrections
the review asked for remove what they read: the constant, the file named by a number alone, the batch number
in a loose call. The changes each needs are listed under the table, in full.

| # | Finding | The review's script on `442a6311` | Now |
|---|---|---|---|
| 1 | High: a loose call's hold ends by itself (C1) | 31 calls in a minute; 21 in the world lane | 30 and 20, with `LOOSE_ALERT` for `LOOSE_FOR` |
| 2 | High: a relay that never got its batch releases another relay's calls (C2) | `ended queued: [[1, t]]`; A's 4 loose calls settled, A not back | `ended queued: []`, unchanged; A's 4 calls still loose, with the script's `loose()` reading the token |
| 3 | High: a brain started by `brain next` loses a failed tick (C3, C3b) | no action at six moments, the count 1 each time; sector 12 and no receipt after a restart; the real client: six empty batches | the line at the second failure (T+2 and T+20), as with one brain; 77 and the receipt; the real client: the line at its second request. Unchanged |
| 4 | High: an empty answer of another kind is a taken action (C4) | `accepted: 2`, no action through T+60, for false, 0, "", [] and nothing | `accepted: 0`, the line sent again at T+12 and T+20, as for "x". Unchanged |
| 5 | Medium: an old brain's late answer goes to another relay's request (C5) | the replacement prints the older relay's batch; the receipt names that relay; its own request deleted unread; `ended` cleared; the holder's 4 calls still loose | it prints its own batch (the profile only); the receipt names it; its request is answered; `ended` handed in; none loose. With three lines changed |
| 6 | Medium: a fight my profile has left is acted on (C3) | second request: Defensive Stance into B1, profile AWAKE | no action; the fight is closed at the first request. Unchanged |

The review's controls give the same three results (30; the profile only and a new receipt; no action and no
battle), with `LOOSE_ALERT` for `LOOSE_FOR`.

The changes, and why:

- **C1, Controls:** `C.LOOSE_FOR` becomes `C.LOOSE_ALERT`. The constant no longer ends anything, so it has
  another name. Unchanged, both stop at `AttributeError`.
- **C2:** in `loose()`, `c[3]==int(token.split('-')[1])` becomes `c[5]==token`. A loose call now names the
  token its relay had, not the batch's number. Unchanged, it prints 0 for A's loose calls before and after.
- **C5:** a request is found by its number and any id (`glob` of `relay.request_path(r.dir,2)[:-5]+'*.json'`,
  twice), the answer being written likewise (`path_.startswith(relay.batch_path(r.dir,2)[:-5])`), and the last
  line drops `c[3]==1`. Unchanged, it stops at `TimeoutError: test rendezvous`.

`player/tests/test_rereview3.py` has one class per finding (K1 to K6, 23 tests), built on those scripts. On
`442a6311`, 13 fail, 6 error and 4 pass. All six errors are names or fields that did not exist there
(`holder`, `brain.stopped`, `held`, a request's `id`): they prove nothing about the old code. Two of the four
that pass are controls. The other two guard against mistakes the new design could make and the old one did
not: a batch that was never printed held for ever, and a dead client's request answered late.

## The ruling: no length of time is evidence

Done as ruled (`player/budget.py`).

- A loose call is held until there is evidence that its batch is over, however long that takes. Evidence is
  the replaced relay coming back with that batch's token, or the operator's word. From that moment the calls
  are counted for sixty seconds more.
- `LOOSE_ALERT` (900 s) only raises a held batch as a stall, once, naming the relay and the command.
- The operator's word is `python3 -m player.brain stopped TOKEN ...`, or `stopped all` for every replaced
  relay (never the one that is running). It is written into `live/client.json` under the client's lock and
  handed to the brain with the next request. With no token the command lists what is held.
- What is held shows in `status.json` (`budget.held`: relay, calls, since), in a finding when a batch goes
  loose, and in the stall.
- When held calls leave no room under the limit, a call is not sent at all, whatever its lane, and that is a
  stall too. The relay is then given a wait, not an empty batch at once.

## What each correction is

### 1, 2. Who holds a batch is what was printed, to whom (`brain.py` `next_batch`, `_greet`, `_exchange`)

A batch is now known by the id of the request that made it. `client.json` keeps `held`: the batch printed to
the relay that is running, set at the moment it is printed and cleared when the brain has its results. A new
relay moves `held` to `gone`. Only a relay that comes back with the exact token of a batch in `gone` is
evidence, and the report names the batch's id. A relay that asked and was replaced before its batch was
printed held nothing, so it is in neither.

The brain no longer takes a flag for "the last batch is lost". Each request says what the asker holds and
what is gone, and the brain places its own last batch: handed in by the relay it was printed to; printed to a
relay since replaced, so loose under that relay's token; or never printed to anyone, so counted from now.

### 3. A failed tick is on disk before it is answered (`brain.py` `_undo`, `_save`)

After a failed tick the brain saves what the request brought, the count of failures and the receipt, and only
then answers. So a brain started for the next request finds them, counts to two, and reaches the last resort.

### 4. Only an object is an answer (`battle.py` `_acted`)

An answer to an action counts as taken only when it is an object with no refusal in it. Anything else is
unknown: the turn goes on from reads and the log. The first such answer in a fight is a finding. The pilot's
own code read `(data or {})`, so nothing in the repository says what the game sends for a taken action beyond
"an object"; the first live run will show it.

### 5. A request and its answer are one pair (`relay.py` paths; `brain.py` `answer`, `_await`, `_sweep`)

Every request has an id in its file's name, and its answer is the file with the same number and id, which
also names the request inside. A brain deletes only the request file it read. Before `brain next` writes a
request it removes every request and batch file left by a `brain next` that died: with the client's lock held,
no live one is waiting. Word that a held batch is over is cleared from `client.json` only when the brain has
answered, and the brain takes it from every request, also one it answers from its receipt.

### 6. Nothing is sent into a fight my profile has left (`battle.py` `last_resort`, `_close`, `_books`)

The last resort first looks at my profile: out of this fight, or in another, it reads my profile and sends
nothing. And a fight's books (its last turn, its result, its archive) no longer keep it open: when they
fail, the fight's state is written to `live/unarchived-<battle>.json`, an error is logged, and the fight
closes.

## Found while correcting (not from the review)

| Gap | Fix |
|---|---|
| Results handed in with `brain put` were deleted when they were read. A `brain next` that died before the brain answered left the next one nothing to hand in | `brain.py` `_collect`, `_taken`: they stay until the brain has answered and the receipt is saved |
| When the brain gave no answer in time, the client made up an empty batch, marked the results as handed in and dropped its evidence | `brain.py` `_exchange`: nothing moves; the relay is told to ask the same thing again |
| A `client.json` of another shape (an older version, an edit) could make a batch look held or gone | `brain.py` `_who`: only what this code writes is read |

## A random walk, and planted defects

Five reviews each found an interleaving I had not tried. So this time I built the search:
`player/tests/test_walk.py`. It drives the real `brain next` with relays that are replaced at any moment (also
while they wait for a batch), go on after being replaced, come back, ask again after being told to stop, or
die; with `brain next` processes killed at three points; with long pauses; and with an operator who says
"stopped" only of relays that are. The hunt runs at its fastest, so the world lane is at its cap and an
uncounted call shows as one too many. After every step it checks seven things; the file's header lists them.

- The suite runs 6 walks of 200 steps (1.5 s). `python3 -m player.tests.test_walk 200 300` ran 200 walks,
  11,212 calls: no problem.
- It does not cover fights, results read from a transcript, or a relay that breaks its contract.

To see whether the walk and the tests can find anything, I planted fourteen defects one at a time, in a
throwaway worktree:

| Planted defect | Random walk (40 walks) | Tests of the last two reviews |
|---|---|---|
| A replaced relay's batch is taken as run | 40 | 5 fail |
| Any replaced relay's return counts as a held batch being over | 40 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 7 fail |
| A held batch is let go by itself after fifteen minutes | 40 | 4 fail |
| The receipt is not checked | 7 | 7 fail |
| A relay that asked holds the batch before it is printed | 15 | 1 fails |
| A batch that was never printed is held as if a relay had it | 12 | 1 fails |
| Word that a batch is over is dropped by a request answered from its receipt | 2 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 1 fails |
| A failed tick is not saved | not modelled | 4 fail |
| An empty answer to an action is a taken action | not modelled | 1 fails |
| The last resort does not look at my profile | not modelled | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 1 fails |

The first version of the walk caught three of the first seven. The table is what it catches now. One test
in it was added, and one rewritten, because a planted defect got past the tests as they were.

**One incident.** The first planted-defect runs changed the files of the real working tree and restored them
afterwards. The container was restarted during one, and one planted line stayed in `player/brain.py` (the
first row of the table). I found it by checking every planted line before going on, restored it, and moved
the runs to a worktree. That row is caught by five tests, so the suite cannot pass with it in.

## The review's notes on the tests

- **One brain kept across requests** (H1, H3): K3 runs the same cases with a new brain for every request,
  and through the real client with no resident brain.
- **Empty answers left out**: K4.
- **The ownership test stopped before the exchange**: K2 is the review's C2. The walk replaces relays during
  the wait.
- **The leftover-file test had no late writer**: K5 is the review's C5 with threads for its processes. It
  fails on `442a6311` on what it prints, not on a missing name.
- **The HP-zero test's failure on the old head was a missing read, not an action**: right. K6 has the action
  itself, and fails on `442a6311` on it.

## Did a wider assumption change?

Yes. I recommend the full relevant scope again for all of it.

- **`client.json`**: `held` and `gone` are new and carry tokens with batch ids; `ended` rows are
  `[batch id, time, token, how]`; `handed` stays.
- **Request and answer files** carry the request's id in their names. The request says `held`, `gone`,
  `ended`; `lost` is gone. The answer carries the batch's id and names its request.
- **The ledger**: a loose call is `[time, lane, "loose", batch id, since, token]` and has no end.
  `Budget.ended` takes a batch id, or `"*"`. `settle` takes `holder`. A call can now be refused outright.
- **`config.py`**: `LOOSE_FOR` is gone; `LOOSE_ALERT` is new. One new command, `brain stopped`.
- **A brain that gives no answer** no longer costs the relay its results.

The three simulated fights give the same figures as at `442a6311` (14, 9 and 13 turns, all acted; 23, 27 and
24 calls at most in a minute; no action delayed).

## The operator's part

The ledger now takes one statement on trust: that a replaced relay has been stopped. Duet has to make it:
after stopping a relay, or finding one dead, `python3 -m player.brain stopped TOKEN` (the token is in
`status.json` and in the event), or `stopped all` at the start of a session when no old relay can be
running. Without it the player slows down as held calls add up, and says why. **This is not in any session
brief yet**; it must be in the one for the next live run.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 305 tests`, `OK`, three runs in a row |
| The review's C3, C3b, C4 unchanged; C1, C2, C5 and the controls with the changes above | the first table |
| The scripts of the earlier reviews (A1 to A3, B1 to B3, and the two before), unchanged | still closed |
| `test_rereview3.py` on `442a6311` (a throwaway worktree) | of 23: 13 fail, 6 error, 4 pass, as said above |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 11,212 calls, no problem |
| The fourteen planted defects | every one fails at least one test; the unchanged code passes |
| The two fuzzes of the last handoff (1,128 fight-read cases, 380 profile and answer cases) | no crash, no error event, no unsendable action |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

## Size

Player code 3,815 lines in 19 files (`442a6311`: 3,602); tests 5,096 lines (4,341). `brain.py` is 724 lines,
`battle.py` 685 (AP6 budget 400). Fifteen functions branch more than 12 ways (fourteen). Config constants 49.
Nothing ships switched off.

`brain.py` is now nearly twice its budget. About 260 of its lines are the relay's client (`next_batch` and
what it calls), which is a unit of its own. Moving it to its own file is a pure move and would bring
`brain.py` to about 460; I have not done it inside a correction, for the third time, and I think it should be
the next step after this head is accepted, before AP2.

## Known limits

1. "Its relay came back, so its calls have run" still rests on the relay doing a batch's lines in order, with
   `brain next` last. A relay that ran `brain next` before its calls would put the ledger ahead. No real relay
   has shown what it does.
2. The operator's word is trusted. Said of a relay that is still running, it lets that relay's calls go
   uncounted after a minute.
3. A batch is marked as held before it is printed. A `brain next` that dies between the two leaves a batch
   that no relay has, held until the operator's word. This is the safe side of the seam the review recorded.
4. A request left by a `brain next` that died is removed, not answered. What it carried is lost unless its
   relay asks again; the next reads and the turn's clock make up for it.
5. When the world model cannot be saved, a tick that worked is treated as failed and sends nothing: with a
   brain started per request, calls sent without a saved ledger would not be counted. A disk that cannot be
   written stops the player, and `crash.log` says so.
6. A fight whose closing code fails outside its books stays open. Nothing is sent into it; only my profile
   is read, with an error on every tick, until Duet steps in.
7. Everything is proven on tests, a random walk and simulations. No real relay has driven any of it.
8. The limits in the earlier handoffs stand where this note does not replace them.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the director: the three token decisions (light polls on his turn; short-lived relays started by a
  script; whether to keep archiving his turn's opening state). Duet's three relay transcripts. The operator's
  command in the next session brief.
- For the reviewer: whether the split of `brain.py` should come before the next review or after acceptance.

Not begun: AP2. No live run is proposed on this head until it has been verified.
