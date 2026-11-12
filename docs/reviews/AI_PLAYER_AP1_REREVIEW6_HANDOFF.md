# AI player overhaul, phase AP1: correction handoff after the review of 426a9fba

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-12, in answer to the review of
`426a9fba` ("request changes": one high finding, one medium, both about what an older version leaves behind).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1
Reviewed: 426a9fbabc5d25247f53d808d297412840a85e26
Review: docs/reviews/AI_PLAYER_AP1_REREVIEW5_REVIEW.md on chatgpt/review-ai-player-ap1-rereview5 @ 8dc89799
        (evidence; not merged)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## Disposition

Both findings are **confirmed**. Each was reproduced on `426a9fba` with the review's own script, unchanged.
Both scripts end by asserting the defect, as the review says of them, so on this head each stops at that
assertion; what they print before it is the corrected result.

| # | Finding | The review's script on `426a9fba` | Now |
|---|---|---|---|
| 1 | High: a brain that comes home answers a request an older version left, and takes its silence about the last batch for "its relay is back" (E1) | the old relay's four calls settled; 34 calls in a minute, 24 in the world lane | the request is removed unanswered; the four calls stay out; the script stops at its assertion that they are settled |
| 2 | Medium: `stopped 1` does not name the batch listed as `batch 1` (E2) | `stopped: []`, `not_held: ["1"]` | `stopped: ["batch 1"]`, `not_held: []`, the other relay's batch still held; the script stops at its assertion of the old answer |

Every script of the earlier reviews still shows its case closed (D, C, B and A series, with the adaptations
already on record).

`player/tests/test_rereview5.py` has the two findings as classes M1 and M2 (11 tests). On `426a9fba`, 6 fail,
3 error and 2 pass (controls). Of the errors, one is a name that did not exist there (`brain.REQUEST`) and
two are real: the old code raised on a request file, and on a client file, that was a list.

## What each correction is

### 1. A running player answers only its own client's requests (`brain.py` `serve`, `run`, `_await`, `_ledger`)

The brain let a request say nothing of who holds what, and read that as "the relay is back". That was meant
for a test that drives the brain itself. It was also true of every request an older version wrote.

- `serve` is now the way a running player's requests reach the brain: the resident brain looking through the
  inbox, and `brain next` answering for itself. It answers a request only when the request carries everything
  this version's `brain next` writes (`REQUEST`: its number, id and relay, and `held`, `gone`, `ended`,
  `unprinted`). Anything else is removed unanswered, with a finding. Its `brain next` is long gone.
- The batch that request was about is untouched: still out. The next request of this version places it, and
  with no record of who has it, it is held.
- `answer` still takes any request, for tests. But `lost`, the older version's own word that the batch was not
  handed in, is never read as "back", whoever passes it.
- Behind that, the brain no longer leans on the budget's rule that pacing a batch means the last one is
  back. Before it paces, a batch still out is held (`_paced`). In ordinary running none is: the ledger has
  placed it. This is for the day the ledger's step fails.

### 2. A batch is named as it is listed (`brain.py` `stopped`)

A name on the command line is text; an older version's batch id is a number. A name now matches a batch when
it is the batch's id as the listing prints it. `not_held` uses the same rule. The word still goes down as one
row for that one batch, with the id as the ledger keeps it, so it settles that batch and no other.

## Found while correcting (not from the review)

The review found one file an older version leaves. I went through the others a new brain or client reads.

| File | State |
|---|---|
| `inbox/req-*.json` | finding 1 |
| `client.json` | `_who` already dropped older records of who holds what. It now also drops a waiting batch that is not in this version's shape (it was printed as it stood, or raised when it grew old), a relay with no usable name, token or number (a new relay starts afresh), and a file that is not an object (it raised). Test: `M1AClientFileOfAnyShapeDoesNotStopBrainNext` |
| `outbox/batch-*.json`, `inbox/put-*.json` | never read unless they carry this request's id, or this batch's token; removed by the next `brain next` |
| `world.json` | sections are merged by name; a held call in an older shape stays held (last handoff); an older receipt has the fields `_answered` reads |

`player/OPERATOR.md` has the sentence the review suggested: if a batch you expect is not listed yet, let the
relay ask once more and list again.

## Did a wider assumption change?

One, and it is narrow. I recommend the scope the review named: request migration through resident startup,
the ordinary upgrade, the selective release by a legacy id, and their receipt and evidence controls.

- **What reaches the brain as a request.** A running player's requests now pass `serve`. `answer` is
  unchanged for a direct caller, apart from `lost`.

The client protocol, the ledger's states, the evidence rows and the file names are as at `426a9fba`. The three
simulated fights give the same figures.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 331 tests`, `OK`, three runs in a row |
| The review's E1 and E2, unchanged | the first table |
| The upgrade from the `442a6311` package, made by that package out of the repository's history | in the suite (`test_the_version_before_itself`; it skips where the history lacks the commit); the same state from recorded files is always run |
| The scripts of the earlier reviews | still closed |
| `test_rereview5.py` on `426a9fba` (a throwaway worktree) | of 11: 6 fail, 3 error, 2 pass |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 6,957 calls, no problem |
| Twenty-five planted defects, in a throwaway worktree | every one fails at least one test; the unchanged code passes |
| The two fuzzes (1,128 fight-read cases, 380 profile and answer cases) | no crash, no error event, no unsendable action |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects, with this review's five first. Under the first of them a test of mine wrote a file into
the worktree's own tree; the tests now keep every brain they start in a folder of its own, and the worktree
stays clean under all twenty-five.

| Planted defect | Random walk (40 walks) | Tests of the last four reviews |
|---|---|---|
| A brain that comes home answers whatever request it finds (this review's finding 1) | not modelled | 5 fail |
| An older request's `lost` is read as back | not modelled | 1 fails |
| A number typed is not the number kept (this review's finding 2) | not modelled | 2 fail |
| The brain paces over a batch it has not placed | not modelled | 1 fails |
| A batch waiting in an older client file is printed | not modelled | 1 fails |
| A replaced relay's batch is taken as run | 40 | 8 fail |
| Any replaced relay's return counts as a held batch being over | 34 | 3 fail |
| A loose call leaves the ledger after a minute | 40 | 13 fail |
| A held batch is let go by itself after fifteen minutes | 40 | 4 fail |
| The receipt is not checked | 3 | 8 fail |
| A relay that asked holds the batch before it is printed | 6 | 1 fails |
| A batch nothing is on record of is taken as never printed | 30 | 9 fail |
| A batch known to be unprinted is held as if a relay had it | 5 | 3 fail |
| `stopped all` is kept as a word for whatever is held when it is read | 3 | 2 fail |
| Asking what is held lets it all go | 40 | 3 fail |
| `stopped all` also names the running relay's batch | 8 | 6 fail |
| Word that a batch is over is dropped by a request answered from its receipt | 1 | 1 fails |
| The operator's word counts the calls from a minute before | not caught | 1 fails |
| An older ledger's held calls are dropped on loading | not modelled | 2 fail |
| A failed tick is not saved | not modelled | 4 fail |
| The last resort does not wait when nothing can be sent | not modelled | 2 fail |
| An empty answer to an action is a taken action | not modelled | 1 fails |
| The last resort does not look at my profile | not modelled | 1 fails |
| An answer is taken whatever request it names | not caught | 1 fails |
| A request left by a `brain next` that died is answered late | not caught | 1 fails |

## Size

Player code 3,951 lines in 19 files (`426a9fba`: 3,895); tests 5,721 lines (5,422), and a recorded fixture of
four small files. `brain.py` is 832 lines, `battle.py` 685 (AP6 budget 400). Sixteen functions branch more
than 12 ways (fifteen). Config constants 49. Nothing ships switched off.

The split of `brain.py` waits for acceptance, as ruled: after correctness, before AP2, as its own change.

## Known limits

1. The walk does not model an upgrade. What an older version leaves is covered by the tests of this review
   and the last, on recorded files and on the old package itself, not by search.
2. Files of versions older than `442a6311` are handled by shape, not by a recorded upgrade from each. Any
   request they left is removed; any record of who holds what is dropped; what was out is held.
3. A batch held with no relay to its name is released only by the operator's word. After an upgrade with a
   batch out, the operator has to say `stopped 1` (or `all`) once the old relay is known to be stopped.
4. The limits in the earlier handoffs stand: the relay doing its lines in order, the operator's word being
   trusted, a batch marked as held before it is printed, a world model that cannot be saved, a fight that
   cannot be closed, and that no real relay has driven any of it.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential.

## Open

- For the director: the three token decisions (light polls on his turn; short-lived relays started by a
  script; whether to keep archiving his turn's opening state). Duet's three relay transcripts. Whether
  `player/OPERATOR.md` goes into the next session brief as it is.

Not begun: AP2, and the split of `brain.py`. No live run is proposed on this head until it has been verified.
