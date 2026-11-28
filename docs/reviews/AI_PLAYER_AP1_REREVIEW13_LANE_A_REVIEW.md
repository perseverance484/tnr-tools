# AP1 independent re-review, Lane A — 62e1aab1

Repository: `perseverance484/tnr-tools`. Frozen target: `62e1aab13c61f5e48b70c9a66b4d7bc1824fe1f9`. Code commit: `3fb470222aa0ad0cdb90ec6f36ad06f646608eae`. Base: `ce1be6e98eb39550e79806c5c8f9da87f67fa4eb`. Review date: 2026-11-13.

**Verdict: accept. The concurrent-reader H2 finding is closed. H1 remains closed under protocol 5. No new finding in the requested scope.**

I read the REREVIEW13 handoff first, then Implementation Handoff section 5. I reviewed who closes an unfinished takeover save, its interaction with an active save, and the reader/failure/crash/protocol controls. This is a focused acceptance of the frozen correction; it does not reopen the approved split, settled policy or AP2.

## Unchanged reproducer: closed

I reran the [previous report's embedded reproducer](https://github.com/perseverance484/tnr-tools/blob/39070bc9a6a0b06f5099a7eaf4248587eb7519cf/docs/reviews/AI_PLAYER_AP1_REREVIEW12_LANE_A_REVIEW.md) unchanged, in all four modes.

| Mode | Observed result on this head |
|---|---|
| `window` | The resident holds `brain.lock`. The separate process's `World(live)` does not close its save; `stopped all` queues no takeover word. After restoring the old world bytes/mtime: no calls, 30 held rows, counts 1 then 2. The script stops at its old assertion that the word names the later hold. |
| `failed` | No calls, 30 held rows; counts 2 then 3. The script stops at its old count-1 assertion, as on the preceding head. Its unlocked Brain allows `stopped` to recover the abandoned-looking save, and the later retry counts again. |
| `before` | Passes unchanged. The earlier word cannot release the later restored takeover. |
| `after` | Passes unchanged, with the same safe result. |

I also reran the original `write_window.py` and `save_faults.py` from the review at `219515fe`, unchanged. Their outcomes remain as recorded in the last review: the concurrent and failed-save defect assertions are refuted; before/after and counter-failure controls pass; the world-failure script stops at its obsolete immediate-count assertion. I inspected calls, held rows and identities rather than treating assertion failure alone as closure.

As an additional check, I changed only the acknowledgement child's `World(live)` to `brain.Brain(live)` in a separate copy. That other process also leaves the active save alone. No word is queued, the later takeover retains 30 rows, and no calls are printed.

## Who closes the save

The production call sites now support the intended ownership boundary:

- `World.__init__` is read-only. I compared file bytes and nanosecond mtimes before and after `World`, `seen` and `found` on a folder with `saving=True`; all remained unchanged.
- `Brain.__init__` calls `_left_save` before constructing its World. A process already holding the registered brain lock can recover the previous save. Otherwise it must acquire that lock for recovery, and releases it afterward. If another process holds the lock, it does not count.
- `brain stopped` retains its existing lock-aware recovery path. It cannot close the active resident's save merely because its short wait expired.
- The save's third write rereads the count, so a completed retry does not finish on the stale count captured before its first write.

I checked the lock registry beyond the basic tests: taking the lock through a symlink is recognized through the real path; a failed second acquisition does not disturb the owner; closing the file invalidates ownership; releasing the last reference and collecting it releases ownership and allows reacquisition. The registry uses weak references, so it does not itself keep an otherwise abandoned lock alive.

The tests cover a separate process holding the lock, a reader constructing a whole Brain, a lock already closed, recovery by its owner, and recovery with nobody home. The third-write test exercises a count advanced between writes and verifies that completion advances beyond it.

The accepted boundary remains one active player writer under the brain lock. The handoff explicitly excludes concurrent saves by independently constructed, unlocked script brains. I did not expand that into a guarantee for arbitrary concurrent writers or direct calls to recovery helpers outside their documented lock precondition. Plain World construction—the advertised reader operation in the finding—now has no write side effect.

## Failure and crash controls

I reran my independent crash-boundary script unchanged. It interrupts before any write or immediately after each successful replacement, releases the lock as process death would, and restarts under the lock. It then completes recovery, restores only the original world bytes/mtime, and tests the earlier word against that later takeover.

| Interruption | `(count, saving)` at interruption | At restart | Earlier word releases later takeover rows |
|---|---|---|---:|
| Before write 1 | `(0, false)` | `(0, false)` | 0 |
| After write 1 | `(0, true)` | `(1, false)` | 0 |
| After write 2 | `(0, true)` | `(1, false)` | 0 |
| After write 3 | `(1, false)` | `(1, false)` | 0 |

All four later restored takeovers retain 30 rows. The locked failed-save/same-Brain retry control passes as well: an active Brain's failed save is not mistaken for a dead writer's save by an acknowledgement reader.

The additional probe just before write 3 still safely acknowledges the actual hold already stored in the current ledger. A later restored takeover gets another identity and stays held. The revised comment now describes this distinction accurately: an incomplete foreign-file/count pair cannot supply an acknowledgement identity, while an already-saved hold row can.

The existing same-bytes/same-mtime, stable-before-save, acknowledgement replay, quiet-minute, selective-release, pending delivery and result-idempotence tests remain green. No counter file was deleted or restored in these reproductions. Counter loss/rollback and power-loss durability remain outside these demonstrated guarantees.

## Protocol 5 and ce1be6e9

I reran the earlier H1 harness with only the maker SHA changed to the actual ce1be6e9 package:

| Case | Result |
|---|---|
| Predecessor pending batch | No calls; old defect assertion refuted |
| Predecessor receipt retry | Old caller refused; no calls |
| Predecessor batch after current hold was saved | No calls past the hold |
| Acknowledgement before fresh relay | Two new calls after 60.5 seconds |
| Same pending state made by this frozen head | Four calls after its own eight-second wait; no update hold |
| Same receipt state made by this frozen head | Four calls after eight seconds; no update hold |

The three actual-ce1be6e9 resident tests also pass: the older resident left running, ended during the wait and ended first. Its pending/receipt/ledger test ran without skipping. The current client, waiting batch, request and request name, answer, receipt and ledger checks retain explicit predecessor-number coverage. Current accepted results remain idempotent; an older receipt does not authorize its old batch.

## Regression discrimination

On the base production code, using current test files in an isolated extraction, `test_rereview12.py` gives **10 failures, 4 passes, no errors**, matching the handoff. The missing `_home` name was supplied only in the test process as a false-returning shim; no base production file changed.

This is not ten independent reproductions. Four failures concern the reader and count-completion changes, two concern recovery ownership (the closed-lock test depends on the newly supplied helper), and four treat ce1be6e9 as a predecessor even when running its own production code. The four passing controls are the crash table, acknowledgement before write 3, recovery under an owned lock and recovery with nobody home. The exact previous reader reproducer independently discriminates the defect without that shim.

The full target suite and the focused tests pass without skips. These tests exercise observable publication, identities, held rows, file changes and recovery, rather than relying solely on the new registry's contents.

## Verification

| Command/check at the frozen target | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 436 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_rereview12 player.tests.test_rereview11 player.tests.test_rereview10 player.tests.test_rereview8` | 55 tests, OK, none skipped |
| Current `test_rereview12.py` against ce1be6e9 production code | 10 failures / 4 passes, as qualified above |
| Previous reader and write-window scripts, four modes each; save-fault script | Outcomes above |
| Independent crash, third-write, read-only and lock-alias controls | Safe outcomes above |
| Actual predecessor and current-maker H1 controls | Outcomes above |
| `python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `player_allowlist.py check` and `report --check` | Zero violations; report current |
| `rulings_index.py --check` | 322 rulings; current |
| `check_large_files.py` | Clean |
| `check_no_real_name.py --commits ce1be6e9..62e1aab1` | Zero hits |
| `git diff --check` | Clean |

I did not repeat all 85 author-reported mutations, the 200-walk campaign, fuzzes, simulated fights or unchanged legacy pilot tests for this focused correction. The full suite includes its deterministic walk regression; the real-process tests and independent interleaving are the relevant concurrency evidence. No live behavior or token-use measurement is claimed.

Only this report is published on `chatgpt/review-ai-player-ap1-rereview13-lane-a`. No existing tracked file changed in the review checkout, and no implementation file or `fable/*` branch was modified. Temporary extractions, altered test copies and scratch scripts remained outside the checkout.

**Zero live-game requests, game writes, live credentials or live session material used.**
