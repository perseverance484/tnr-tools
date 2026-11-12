# AP1 re-review, Lane A — c412de4d, verification and replay check

Repository: `perseverance484/tnr-tools`. Frozen target: `c412de4df43baf4f11fbd817efb0f7ae95c08226` on `fable/ai-player-ap1`. Code commit: `fbdf40101695b216e023aad99f444c6300e28c89`. Base: `29797ba0f769152381e71710f812605be9e0bfea`. Reviewed 2026-11-12.

**Verdict: request changes.** The unchanged known-limit script stays inside 30/20 in all three cases. The overall admission requirement remains open: predecessor pending/receipt delivery bypasses the hold (H1, high). A retained acknowledgement can also release a later takeover of identical unreadable bytes (H2, medium; requires the explicit fault sequence below).

I read `AI_PLAYER_AP1_REREVIEW9_HANDOFF.md` first, then `IMPLEMENTATION_HANDOFF.md` section 5. Scope: takeover admission, persistence across brains/retries/restarts, acknowledgement identity, old-package upgrades, current pending/receipt delivery, and the operator instructions. RUL-2026-11-11-149 through -152 remain settled. The brain split remains after acceptance.

The remote already contained `chatgpt/review-ai-player-ap1-rereview9` at `e7e4c0f6`, reporting H1 against this same target. I reproduced H1 with a separately written actual-predecessor harness before reading that report, then reused its acknowledgement/staleness/current-version controls and resident reproducer. This report preserves that branch and publishes on `chatgpt/review-ai-player-ap1-rereview9-lane-a`. H1 is corroboration, not a newly numbered finding. H2 is additional evidence from this run.

## Unchanged known-limit script

Extracted the complete Python program beginning `import io,json,os,time` from the runnable-evidence section of `AI_PLAYER_AP1_REREVIEW8_REVIEW.md` at `56dfb24d`. It is checked in [unchanged](evidence/ap1_rereview9_lane_a/known_limit.py), SHA-256 `e66473838c58fe8551ad0869900d9b25d1c42ebdf6f51370e02d3f43fa5cd3d2`. The real `442a63119d2fa3fe033877bedc86f5df8cd9be00` package was available and ran.

| Case | New calls in the observed batch | Maximum total / world in a minute |
|---|---:|---:|
| No acknowledgement | 0 | 4 / 4 |
| Acknowledgement only | 3, after the brain-side wait | 30 / 20 |
| Acknowledgement plus 60 seconds | 4 | 30 / 20 |

The 4/4 in the first row represents the old relay's calls; no new call is admitted by that test. The acknowledged cases name an `update-…` hold. These results confirm the handoff's bounded claim for this script, not every publication path.

## H1 — High: immediate-predecessor delivery bypasses takeover admission

Locations at the frozen target: `player/relay.py:27` (unchanged protocol 1), `player/brain.py:427` (receipt replay), `:600` (pending acceptance), `:701` (pending reuse), and `:80` (takeover).

The actual `29797ba0` package wrote its own client, world, pending batch and receipt in temporary storage. I injected death at the client pending write, either immediately after it or immediately before it. The predecessor process exited before current code began; no ledger entries or batches were invented. The new code accepts the predecessor's protocol-1 output despite its newly untrusted ledger.

| Local reproduction | Result |
|---|---|
| Old pending; fresh replacement relay; no acknowledgement | Four calls after 8 seconds |
| Same, with the new Brain's takeover saved first | Four calls after 8 seconds, with 30 update rows still saved |
| Old receipt; interrupted caller retried with current code | Four calls after 8 seconds |
| Same receipt retry, with the takeover saved first | Four calls after 8 seconds, with 30 update rows still saved |
| Old pending; `stopped all` immediately before a fresh relay | Four calls after 8 seconds, inside the required minute |
| Old pending advanced to 11 seconds beyond `ready_at` | No calls; hold established |
| Same pending-death/replacement control made entirely by this target | Four calls after 8 seconds; no update hold, as intended |
| Real `29797ba0` resident still running under `brain.lock` | Three calls without acknowledgement; saved ledger remains unmarked |

The four-call batches contain `profile.getUser`, `travel.getSectorData`, `stealth.useSensory`, and `profile.getStrongestUsers`. These are printed instructions observed locally, never executed game calls.

`_exchange` can use `_owed` without consulting a new Brain. Even after a new Brain has saved the hold, that pending delivery is unchanged. The receipt path does construct a Brain, but `_answered` returns the predecessor's batch without pacing it against the hold. Keeping the same request namespace also lets the immediate predecessor resident answer current requests. The resident case intentionally omits the documented stop-old-brain step; the pending/acknowledgement case reproduces with the old process gone and the documented order followed.

**Required correction:** establish the changed admission rules as a compatibility boundary for requests, clients/pending records, answers and receipts, or enforce an equivalent gate at every publication path. `relay.py` already instructs changing the number when admission rules change. Preserve result idempotence and known reservations; retain positive controls for this version's own pending and receipt delivery. A hold only inside fresh pacing is insufficient.

## H2 — Medium: a replayed word settles a later identical-byte takeover

Locations: `player/world.py:68-86` (content-only identity), `player/budget.py:161-162` (hold creation), `:215-217` (matching and timestamp clamp), and `player/brain.py:706-723` (retained evidence until client save).

The hold identifies file contents, not a takeover generation. The handoff explicitly includes unreadable ledgers; the new regression tests include an empty file. Every empty file is named `update-da39a3ee`, regardless of when it was written or whether an earlier takeover was already saved.

Reproduced using current code throughout:

1. Begin with an empty `world.json`; issue `stopped all` once. The client queues the word for `update-da39a3ee`.
2. Run a request, injecting death just before the pending batch is saved to `client.json`. The Brain has already saved a valid, protocol-marked world with the first acknowledgement applied. The client legitimately retains the old evidence for retry.
3. Advance 120 seconds and inject a second file-corruption event: truncate `world.json` again, updating its modification time. This is a separate unreadable-ledger takeover after the first was durably saved. No old program is run and no downgrade is involved.
4. Retry without saying `stopped` again. The second listing again names `update-da39a3ee`. The retained first word matches and settles all 30 new loose rows. A `profile.getUser` call is printed after 61.5 seconds, without a new acknowledgement.

This is **not an early-clock bypass**: the stale timestamp is correctly clamped to the present, preserving a new sixty-second tail. It is an acknowledgement-identity bypass: no fresh word authorizes the second release. If older actors can still execute, the quiet minute alone does not establish that they have ended.

| Replay control | Loose update rows after retry | Calls |
|---|---:|---|
| Repeated empty contents, retained first word | 0 | One after 61.5 seconds |
| Different unreadable contents (`{`), same retained word | 30 | None |
| Repeated empty contents, queued word removed | 30 | None |

This finding requires repeated external corruption plus the crash/retry window. Normal atomic `World.save` was not observed to produce an empty file; this is fault injection against the explicitly supported unreadable-ledger path, not a claim that ordinary restarts corrupt data. It needs neither a hash collision nor arbitrary fabricated acknowledgement rows. The same first word is retained by the real failure path.

**Required correction:** distinguish a new takeover from a retry of the same takeover even when the source bytes repeat. Old evidence must not authorize a later generation. Merely clamping an earlier timestamp delays the release; it does not reject the stale authorization. Keep stable identity before the first successful save and allow the operator to acknowledge before starting a relay. Add the identical-content replay case beside the existing different-content test.

## Controls and operator documentation

The 15 tests in `test_rereview8.py` pass, including the real forgotten-ledger package test. The following behavior is supported on the tested fresh-admission path:

- First start and ordinary restart on a current marked ledger have no update hold.
- An unacknowledged hold persists across new Brain instances, a killed client, retry, and replacement relay. A Brain ending before its first save leaves the next Brain the same identity.
- The 30 update rows block world, recovery and battle pacing; calls stay behind the acknowledgement's sixty-second tail.
- Listing does not release; known old batch holds remain separate and release one by one without releasing the update hold. The numeric legacy-id controls also pass.
- Repeating a word does not widen it to unrelated ids. A different-content later takeover rejects the old word; H2 identifies the omitted identical-content case.
- Current pending/receipt, timeout/death, ownership and result-retention controls pass in the full suite. The 30-test focused run of `test_rereview8` and `test_rereview6` passes, including all real-package tests without skips.

`player/OPERATOR.md`, “After the player's code is updated,” correctly describes the intended order, truthful acknowledgement, selective release, first-start exception and ordinary restart. Three promises exceed the implementation:

| Promise | Counterexample |
|---|---|
| No call until the word and sixty seconds after it; steps 3 and 4 may swap | H1 old pending/receipt output, including a saved hold and the acknowledged 8-second case |
| Old brain gives no answer; an earlier pending batch is unused | Actual protocol-1 predecessor resident and pending batch in H1 |
| The word is of no use for a later update, which has another name | H2's separate identical-byte takeover reuses the name and the word |

The correct response is to enforce the accepted boundary and align the page with verified behavior. This is not a reason to reopen settled rulings or move the brain split before acceptance. The disclosed first-start, dishonest-operator and downgrade limits remain separate from these findings.

## Reproduction and verification

Run from the repository root at the frozen target, with Git history present. Every harness uses temporary local folders, historical package extraction, fixtures and simulated clocks. Assertions in defect harnesses encode the observed defect and should fail when corrected. The `different`, `no-word`, `expired`, and `trusted` modes are controls.

```sh
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/known_limit.py
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/takeover_delivery.py
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/repeated_unreadable.py replay
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/repeated_unreadable.py different
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/repeated_unreadable.py no-word
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/predecessor_controls.py ack
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/predecessor_controls.py expired
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/predecessor_controls.py trusted
PYTHONPATH=. python3 docs/reviews/evidence/ap1_rereview9_lane_a/predecessor_resident.py
```

`known_limit.py` is copied verbatim from the base review. `takeover_delivery.py` and `repeated_unreadable.py` were written for this run. `predecessor_controls.py` and `predecessor_resident.py` are copied verbatim from the earlier report at `e7e4c0f6`; that attribution matters because their original discovery is not this run's work.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 369 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_rereview8 player.tests.test_rereview6` | 30 tests, OK, none skipped |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,393 calls, zero problems |
| `python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `python3 scripts/player_allowlist.py check` and `report --check` | Zero violations; report current |
| `python3 scripts/rulings_index.py --check` | 322 rulings; index current |
| `python3 scripts/check_large_files.py` | Zero unapproved oversized files |
| `python3 scripts/check_no_real_name.py --commits 29797ba0..HEAD` | Zero hits in tracked files and commit messages |
| `git diff --check` | Clean |

The production `player/` tree is identical between the supplied code commit and frozen handoff. I did not repeat the author's 50 mutations, fuzz campaigns, simulated fights, or all earlier standalone review scripts; the unchanged known-limit script, focused adversarial cases and full player suite are the evidence for this run. Passing single-version walks cannot establish predecessor compatibility or coverage of repeated identical-content corruption.

Next correction scope: H1's immediate-predecessor publication paths and H2's takeover identity, with the ordinary-start/restart, selective-release, quiet-minute and current delivery/idempotence controls retained. No full AP1 redesign is requested.

Only this report and local reproduction programs are published. No implementation file or `fable/*` branch was modified. **Zero live-game requests, game writes or live credential/session material used. No live relay or browser session exercised.** GitHub access was solely for repository retrieval and report publication.
