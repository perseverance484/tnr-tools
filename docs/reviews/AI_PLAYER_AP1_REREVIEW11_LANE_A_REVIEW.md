# AP1 independent re-review, Lane A — e4a267cd

Repository: `perseverance484/tnr-tools`. Frozen target: `e4a267cd1ab5ff85c3b2399bab713f2870da6ccb`, branch `fable/ai-player-ap1`. Code commit: `046e94513c0746d89ee8c7d10ccfd76861b3b339`. Superseded handoff: `7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e`. Review date: 2026-11-12.

**Verdict: request changes. H1 is closed for the three requested predecessors. The original H2 reproducer is refuted, but H2's identity requirement remains open at the counter/world publication boundary: one medium finding below.**

I read `AI_PLAYER_AP1_REREVIEW11_HANDOFF.md`, then `AI_PLAYER_AP1_REREVIEW10_HANDOFF.md`, then Implementation Handoff section 5. Scope is the takeover count, name and write order, with ordinary start/restart, selective release, quiet-minute and current delivery/idempotence controls; H1 is a confirmation using both reports' own scripts. This is not a general AP1 restart. Settled rulings remain settled and the brain split remains after acceptance.

The ancestry is as stated: `7cf7d73c -> 046e9451 -> e4a267cd`, without a rebase. The code commit and frozen handoff have identical `player/` trees. Protocols are 1 for `29797ba0` and `c412de4d`, 2 for `7cf7d73c`, and **3 for the reviewed head**.

## H2 — Medium: a word recorded while the counter is ahead can authorize a later takeover

Relevant locations at the frozen head:

- `player/world.py:97`: `found` hashes source bytes, modification time and the current counter.
- `player/world.py:134-136`: the counter is replaced first; `taken_over` is cleared; the world file is replaced second.
- `player/brain.py:801-807` and `:825-834`: `stopped` holds the client lock, reads the two files and queues the derived id, without synchronizing with their publication.
- `player/brain.py:363-374`: the resident watchdog can perform the first takeover save without a client holding the client lock.
- `player/brain.py:196-203`: a failed save can leave the same Brain alive to save its in-memory state later.

Writing the counter first is conservative when a process dies between the writes, as the handoff says. It is not sufficient when an operator observes that intermediate state and the same Brain subsequently finishes saving.

Let `A = hash(old bytes, old mtime, count 0)` and `B = hash(old bytes, old mtime, count 1)`:

1. The new Brain takes over a genuine `7cf7d73c` ledger, installing hold **A** in memory.
2. Its first save writes count **1**, while `world.json` still contains the old ledger.
3. `brain stopped all` runs now. It reads the old ledger with count 1 and queues a word for **B**, not the Brain's actual hold A.
4. The world save succeeds. It contains hold **A**; the queued word for B remains in `client.json`. The counter remains 1.
5. Later, the old world snapshot returns with the same bytes and modification time. **Only `world.json` is restored. `takeovers.json` is neither lost, changed nor rolled back.** This is a later takeover, whose computed hold is B.
6. A new relay's request carries the retained word for B. It settles the new hold without a new acknowledgement. Four calls are printed after **9 seconds**, and no loose update rows remain. The second save advances the intact counter to 2.

The word is over a minute old at step 6; therefore this is an authorization-identity failure, not arithmetic that shortens a valid acknowledgement's sixty-second tail. A word about the first takeover must not authorize the later one at all.

### Two independently exercised ways to reach the intermediate state

**Concurrent operator:** the harness runs the actual `brain.run(live, forever=False)` path. Its watchdog performs the first save. At the boundary before the world write, the harness schedules a **separate Python process** calling `brain.stopped(..., ['all'])`. That process succeeds while the resident demonstrably holds `brain.lock`; the real client lock remains enabled. The harness then permits the world write to finish. This is deterministic scheduling of an allowed interleaving, not a fabricated acknowledgement row or a disabled lock. The old package has already exited.

**Failed world write, same-Brain recovery:** let the counter write succeed, inject `OSError` for the world write, and let `Brain._save` catch it. Issue `stopped all` after that method returns. Then allow the same Brain's next save to succeed. It writes its original hold A without counting again. The queued word is B, and the later restored world consumes it exactly as above. This case needs no concurrent timing and exercises the save-failure behavior explicitly disclosed in the handoff.

| When the operator speaks | Later restored takeover | Calls printed | Loose update rows |
|---|---|---:|---:|
| Before the counter write | Different from the acknowledged id | 0 | 30 |
| Between counter and world writes, separate process | Same as the prematurely exposed id | 4 after 9 s | 0 |
| After the world save completes | Different from the acknowledged id | 0 | 30 |
| After world-save failure, before same-Brain recovery | Same as the prematurely exposed id | 4 after 9 s | 0 |

Each case starts with a fresh live folder made by the actual protocol-2 package. In every case the counter is 1 after the first takeover is saved and 2 after the later request. The restoration of identical bytes and mtime is deliberate fault injection, matching the correction's stated requirement and its new readable-snapshot test. This does not assert that normal saves restore old snapshots. No hash collision or whole-folder restore is involved.

**Required correction:** prevent the operator from recording an identity derived from a partially published counter/world pair that can subsequently become a later takeover's identity. Preserve the conservative counter-first crash behavior. The solution must cover both concurrent observation and a failed world save followed by same-Brain recovery; synchronizing only the successful two-write interval would leave the second case. Ensure that the id being acknowledged belongs to the actual current takeover and cannot be left queued for a future generation.

The handoff's disclosed counter-loss limit does not cover this reproduction: the counter survives and increases correctly. Nor does the statement that no call goes out during a failed save close it: publication occurs later, after recovery and another takeover. `OPERATOR.md`'s claim that an old word cannot release a later identical-byte takeover is still too broad for this implementation.

### Runnable evidence

[write_window.py](evidence/ap1_rereview11_lane_a/write_window.py) contains the two reproductions and their before/after controls. Run from the reviewed repository root, with its Git history available:

```sh
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview11_lane_a/write_window.py window
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview11_lane_a/write_window.py failed
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview11_lane_a/write_window.py before
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview11_lane_a/write_window.py after
```

The first two modes assert the observed defect; a correction should refute those assertions. The last two assert safe controls. The file generates its source ledger using `7cf7d73c` and uses temporary folders, fake clocks and simulated output only. The printed calls are instructions observed locally, never game requests.

## Original H2 and counter controls

I ran `repeated_unreadable.py` from the second report unchanged. All three modes stop at its obsolete literal `protocol == 1` assertion; that is not behavioral evidence about this head. With only that assertion changed to `protocol == relay.PROTOCOL`:

- On `7cf7d73c`, `replay` reproduces the defect: `update-da39a3ee` twice, no loose update rows, one call after 61.5 seconds.
- On `e4a267cd`, `replay` prints different identities, 30 held rows and no call, then fails its old assertion that the identities match. The original sequence is closed.
- The `different` and `no-word` controls pass: 30 held rows and no call.

All 13 tests in `test_rereview10.py` pass, as does the additional same-bytes/same-mtime readable-ledger test in `test_rereview8.py`. They establish stable identity before first save, a changed identity after a saved takeover, the mtime distinction before any save, and harmless replay without a later takeover. They do not exercise operator observation during the two-write transition or after a failed world write followed by same-Brain recovery.

I separately injected failures at each write with [save_faults.py](evidence/ap1_rereview11_lane_a/save_faults.py):

| Failure point | Counter after failure | Restart's identity | Effect of prior word |
|---|---:|---|---|
| Before counter replacement | 0; world untouched | Same takeover | Names its 30 rows, as expected |
| Counter succeeds, world write fails | 1; world untouched | New identity | Releases 0 rows |

In both cases the original Brain can recover and save twice with final count 1: no double increment. These component checks support the write-order rationale but do not invalidate the intermediate-observer finding above.

First start and ordinary restart do not create an update hold or counter file. The tests also retain selective release of known batches without releasing the update hold, the sixty-second quiet period, hold persistence across brains and retries, current pending delivery and receipt/result idempotence. The focused 49-test run covers `test_rereview8`, `test_rereview9` and `test_rereview10`; none skipped.

## H1 — Closed against all three requested predecessors

Sources: the first report's two Python blocks at `e7e4c0f6` (`predecessor_controls` and `predecessor_resident`), and the second report's `takeover_delivery.py` at `f586a6b2`. The latter report's predecessor-control/resident files are identical copies of the first report's scripts, not separate harnesses.

I ran the original scripts unchanged against their original `29797ba0` maker, then made narrowly adapted copies to complete the matrix. Adaptations were only the predecessor SHA and removal of obsolete assertions that require the defect to occur. In the second report's harness, the three trailing defect checks were removed so all four pending/receipt cases could print. The resident's full wait was retained; it was not replaced with a shortened fake timeout.

| Current receiver: e4a267cd, protocol 3 | 29797ba0 / p1 | c412de4d / p1 | 7cf7d73c / p2 |
|---|---|---|---|
| First report: pending | No calls | No calls | No calls |
| First report: receipt retry | No calls; old caller stops | Same | Same |
| First report: hold already saved | No calls | No calls | No calls |
| First report: pending stale | No calls | No calls | No calls |
| First report: acknowledgement before fresh relay | 2 calls after 60.5 s | 2 after 60.5 s | 2 after 60.5 s |
| First report: actual predecessor resident still running | No calls; no answer while resident holds lock | Same | Same |
| Second report: pending, with/without saved takeover | No calls in either case | Same | Same |
| Second report: receipt, with/without saved takeover | No calls in either case | Same | Same |

Pending cases save 30 update rows. A rejected old-token receipt retry need not start a Brain, so without the explicit pre-save it leaves the predecessor ledger as it was; this is not a missing-hold failure. The fresh-relay receipt controls in the suite then establish the hold and retain the predecessor's four reservations.

The first report's unchanged `trusted` mode still makes its state with `c412de4d`: it now correctly emits no calls, failing its old expectation. Changing only that maker to the reviewed target produces the intended current-version control: four calls after 8 seconds, no update hold, ledger protocol 3. Current receipt replay and exactly-once result handling also pass in the suite; a foreign receipt suppresses reapplication without authorizing the old batch.

Unchanged H1 scripts stop at their old defect assertions when no call is emitted. `ack` and `expired` pass as written. These assertion failures are expected refutations, not test errors being counted as successes. Every adapted matrix run exits 0, and I inspected its printed calls, timing and ledger state.

[run_report_scripts.py](evidence/ap1_rereview11_lane_a/run_report_scripts.py) extracts the exact source programs from the two report commits and recreates these original/adapted runs in temporary storage. It records each script's output and exit code; expected obsolete-assertion failures are retained. Run it from the repository root. Its `--prepare-only` option extracts the five originals without executing them. Git history must include both report commits and all predecessor packages.

The earlier `known_limit.py` was also rerun **unchanged**: no acknowledgement gives no new calls and peaks 4/4; acknowledgement gives 30/20; acknowledgement plus 60 seconds gives 30/20. Its SHA-256 remains `e66473838c58fe8551ad0869900d9b25d1c42ebdf6f51370e02d3f43fa5cd3d2`.

## Verification and remaining boundary

| Command/check at the frozen target | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 403 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_rereview10 player.tests.test_rereview9 player.tests.test_rereview8` | 49 tests, OK, none skipped |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, zero problems |
| `python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `python3 scripts/player_allowlist.py check` and `report --check` | Zero violations; report current |
| `python3 scripts/rulings_index.py --check` | 322 rulings; index current |
| `python3 scripts/check_large_files.py` | Zero unapproved oversized files |
| `python3 scripts/check_no_real_name.py --commits 7cf7d73c..HEAD` | Zero hits |
| `git diff --check` | Clean |

I did not independently repeat all 68 author-reported mutations, fuzz campaigns or simulated fights. The new interleaving/failure reproduction survives the passing suite. The walk does not model repeated source snapshots or operator observation between the two writes; its passing result does not refute H2.

For this scope, the explicit protocol transition and actual-predecessor tests close H1; I do not require an automatic code fingerprint as a new acceptance condition. The manual protocol maintenance risk remains documented. Counter loss/corruption and whole-folder rollback remain the handoff's separate limits; this finding does not depend on either. No broader durability claim about power loss is made.

The next correction should keep the counter-first crash property while making takeover identity consistent for acknowledgement readers during publication and save recovery. Retain the original H2 replay, same-content/same-mtime, before-first-save acknowledgement, quiet-minute, selective-release and current delivery controls. Because this changes release/admission behavior, apply the project's protocol-change rule again and retain an actual `e4a267cd` predecessor control. H1 itself does not need a redesign, and the brain split need not move ahead of acceptance.

Published additions are this report and three local reproduction programs on `chatgpt/review-ai-player-ap1-rereview11-lane-a`. No implementation file or `fable/*` branch was modified. **Zero live-game requests, game writes, live credentials or live session material used. No live relay/browser session exercised.** GitHub access was only repository retrieval and report publication.
