# AI player relay refusal: first correction review

**Verdict: approved for this correction surface. R1 and R2 are closed.** No new blocking finding was found. The bounded lock wait is acceptable, and protocol 10 can stay.

Reviewed 2026-11-15 in `perseverance484/tnr-tools`:

- Frozen target: `fable/ai-player-relay-refusal` @ `aa73867c53b1f7ab7a8577d0402e7195d43f0824`.
- Previous target and verified merge base: `9c2955bae4a1c681f7bf14de8f7ad57675cbf1d8`.
- Scope: `git diff 9c2955ba aa73867c`, the correction handoff, and the client/accounting/test paths on which the corrections depend. Three commits: `6f8fa44d`, `fcb0929c`, and `aa73867c`.
- Prior findings: `docs/reviews/AI_PLAYER_RELAY_REFUSAL_REVIEW_20261114.md` on `chatgpt/review-ai-player-relay-refusal-20261114` @ `64f7d87aaef5e2abac89d04be6b1d6d760aab35c`.
- Authority: RUL-2026-11-14-161. Review method: `docs/workflows/FABLE_REVIEW.md`, Engineering Auditor.
- Remote target still matched the frozen SHA before publication. `main` was `e6ccece9995c038548b6d41b927701346119be25`; `fable/ai-player-hook-proof` remained `071ba1b1dcf6f28f7fadcf25b05af62d102daedd`.
- Report branch: `chatgpt/review-ai-player-relay-refusal-rereview1-20261115`, anchored to the frozen target. Only this report is added; no implementation or Fable branch is changed.

**This is not the separate re-review of 071ba1b1.** This approval does not approve that preflight correction or authorize its use on a machine connected to the game. Zero live-game requests or writes; no credentials used, real connector started, Claude session launched, or preflight/proof program run.

## R1: final refusal and accounting — closed

`player/brain/client.py:155` now checks `hooked.bare` under the client lock after the answer/pacing wait, before any transition from pending to held and before the only batch-printing call to `relay.lines`. The early check remains before `_greet`, preserving the refusal of a newcomer without renaming or replacing a running relay.

The final condition checks changed ownership first. A relay superseded during the wait still gets `SUPERSEDED`, even when its permission was also revoked. A still-current hookless relay gets exactly `hooked.BARE`; this branch neither writes client state nor claims, discards, or prints its pending batch. A relay previously named with hooks still follows the existing hook-loss response at entry. The new check does not change what counts as a hook stamp.

I traced the other output paths. No-answer, changed-pending, expired-lease, and stale-token paths print a retry command, not game calls; foreign tokens retain the superseded path. A saved pending batch must pass both the entry and final policy checks. I found no remaining path that publishes a game-call batch to an unstamped relay when the final policy check sees anything other than literal JSON `true`.

The six withdrawal schedules in the added test cover false, absent, and malformed control files, during both the brain-answer wait and the pacing wait. They assert the exact STOP output, unchanged token, no held batch or calls, retained pending work, and an unchanged client on the following refused invocation. Positive controls retain permitted bare delivery and hooked delivery. The superseded test checks the exact prior response.

Pending ownership and accounting remain sound:

- Naming a hooked replacement preserves the pending record. Its next call retrieves that same batch through `_owed`, then prints stand-ins and holds the original batch ID. The committed test exercises the hooks through a fixture answer for `profile.getUser`.
- An independent scratch check confirmed that a fresh pending batch transfers without making another request to the brain, is not put in `unprinted`, and does not remain loose after the hooked result is handed back.
- An independent stale-batch check advanced the fixture clock beyond `STALE_OUTBOX`. The replacement requested fresh work, reported the old ID in `unprinted` exactly once, held a different ID, and left neither the old pending record nor an old loose charge behind. This is the existing expiry behavior, not a promise to deliver expired work.

The refusal itself must not report a retained pending batch as unprinted: it may still be delivered to the replacement. The correction preserves that distinction.

## R2: operator recovery — closed

`player/OPERATOR.md`, **When that word is taken back**, now provides the required order:

1. Confirm the refused relay has ended.
2. Start a relay with hooks, which takes over and makes the old held batch listable.
3. Say `stopped TOKEN` for the old relay's token.
4. Let the new relay's next `brain next` convey that acknowledgment to the brain.

This is complete for the reviewed recovery case. Refusal alone leaves the relay current, so its previously printed batch stays held; a STOP line is not evidence that outstanding calls have ended. The text now distinguishes a refused newcomer, which gets no name, from an already admitted relay, which keeps its name. The previously reviewed subagent-start instructions remain unchanged.

`test_its_batch_is_let_go_by_the_operators_word_once_a_relay_with_hooks_has_taken_over` executes the sequence through the actual client and brain. Before replacement it tries listing, token, batch ID, and `all`, confirms none acknowledges the current batch, and checks that `held` survives. After naming the hooked replacement it checks `gone`, listing, acceptance of the old token, the request's `ended` record with reason `stopped`, and an empty loose ledger. `stopped` itself is unchanged. This closes the documentation defect without weakening its safeguard.

## Lock wait in fcb0929c — acceptable

The final assertion in `TheCommandLine.test_a_relays_brain_next_starts_the_resident_by_itself` previously treated absence from its `/proc` command-line/environment scan as proof that all process resources were already released. Those are separate observations during process exit. Waiting for the actual lock is an appropriate synchronization step.

The new loop uses a monotonic deadline, polls every 50 ms for at most approximately five seconds, retains `assertIsNotNone(lock)`, and closes the acquired handle. It does not swallow a failed assertion or restart the resident. The prior assertions still require one resident, refusal of a second resident, continuing service, and disappearance of the resident after termination. Production shutdown and locking code are unchanged.

I extracted the actual final assertion block through the Python AST and ran it with a controlled clock/lock: delayed release succeeds and closes the handle; a permanently unavailable lock still raises the assertion after the deadline. The real subprocess test also passed within the full suite. The change deliberately allows bounded teardown latency; it cannot establish instantaneous release, nor was the prior process-list check a reliable measurement of that property. It does not hide a persistent lock leak.

The handoff's 3/40 failures on each tree and 0/80 after the fix are author-reported evidence. I did not repeat those statistical runs or independently measure the kernel exit interval. My prior review did observe the original intermittent assertion failure; the current bounded check and its failure behavior are independently verified here.

## Protocol and test scope

Keeping protocol **10** is appropriate. No request, receipt, pending, held, or ledger format or accounting meaning changes. This is a delivery-policy check applied to existing pending work, including work saved before the correction. A new protocol number would not repair the old in-flight omission; the added final check does. Existing upgrade requirements to end old processes still apply: an already executing old binary does not acquire this correction.

The new hook-relay tests add assertions rather than replacing existing ones. The earlier fixture helpers and `test_rereview9.OLD_ASLEEP` are unchanged in this delta. The only existing test assertion whose timing changes is the lock-release assertion discussed above. The production change remains narrowly scoped to the final refusal check; the six added lines in `hooked.py` explain when it runs and why pending work remains.

## Independent verification

All commands below ran against the frozen target in an isolated review worktree. Fixture tests used temporary live directories and synthetic answers; none dispatched a game request.

| Check | Result |
| --- | --- |
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | **651 tests, OK**, 60.288 s; no skips. Includes the six new relay tests, operator-recovery sequence, and real resident-process test. |
| `PYTHONPATH=. python3 -W ignore::ResourceWarning /workspace/scratch/refusal_rereview_checks.py` | **4 tests, OK**: fresh transfer without a second brain request; expired pending work reported unprinted; actual lock-test tail accepts delayed release and closes; actual tail rejects permanent non-release. |
| `git diff --check 9c2955ba aa73867c` | Passed. |
| Publication checks: staged diff whitespace, `check_no_real_name.py --commits 9c2955ba..HEAD`, `check_large_files.py`, `rulings_index.py --check` | Passed; 0 name hits, 0 disallowed large files, 331 rulings with current index. File scans cover the sparse checkout, including this report, not absent files. |

Scratch source is outside the repository and is not published. SHA-256: `cd594c0cce3fb70b50f67c3e0f7f977919dbb7aa55ac0adc0b15b7e617c28cd6`. Its pending-batch checks use the production client/brain through the existing hook fixture, and its lock checks compile the unchanged test's final AST statements with injected time and lock acquisition.

No real Claude Code scheduling or connected-machine preflight was tested. The review establishes the code paths and offline regression behavior for this correction, not the separately pending preflight safety claim. No remaining correction is requested here. The next step is the separate review of `071ba1b1` before treating the combined work as cleared for integration or connected-machine use.
