# Forge Quest Studio — final correction handoff

**Status:** FROZEN FINAL CORRECTION — NARROW FABLE RE-REVIEW REQUIRED
**Date:** 2026-09-16
**Repository:** `perseverance484/tnr-tools`
**Implementation owner:** ChatGPT
**Prior review target:** `1f6a1097e33108d595ca27067a7240cf14b98ded`
**Fable review:** `claude/quest-studio-source-push-review@10658b817b51a77efcc18470ef8ef9b9e89e1dbe`
**Correction work branch:** `chatgpt/forge-quest-studio-final-fix`
**Tested permanent tree:** `4197e45878a2a5f5588013c849a8fa249a500b0f`
**Clean pre-handoff descendant:** `ba9ddb73ff93e31ee1291da1f206dbc1318786b0`
**Live-game requests/writes:** none

This pass addresses Fable's final source-push re-review findings without reopening the approved Forge/Quest Studio architecture.

## Findings addressed

### F1 — closed

The two accidentally nested Node tests were moved to top-level declarations:

- `QuestStudioRepository refuses build reads without an exact submitted source identity`
- `editing a submitted Mission invalidates persisted build identity before reopen`

Normal Quest Studio CI on Node 24 now reports **315 tests / 315 pass / 0 fail / 0 cancelled**. Both formerly swallowed protections are visibly executed as independent passing tests.

### F2 — closed as requested hardening

The source-push credential assumption is now explicit in both durable governance and architecture:

- `RUL-2026-09-16-002` states that the browser credential must never hold GitHub Workflows write permission, because push-triggered workflow definitions are resolved from the pushed request ref.
- `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` names the same credential invariant and explains why it is load-bearing.

The worker adds defence in depth before any authored source checkout or compile:

1. trusted `main` is checked out under `tools/` with `persist-credentials:false`;
2. the exact pushed ref is checked out separately under `request-definition/` with `persist-credentials:false`;
3. `.github/workflows/quest_studio.yml` from the pushed ref is byte-compared with trusted `main`;
4. any mismatch fails closed before request identity validation, authored request checkout, or compile.

`quest_worker_contract_test.py` now pins that comparison.

This does not replace the credential invariant. Workflows write on the browser credential remains forbidden because an attacker able to replace the pushed-ref workflow definition could also remove the comparison itself.

### F5 — closed

`Persist build result to request branch` now runs with an `always()` condition once request identity was established. If the compile step exits without producing its structured result file, persistence synthesizes a request-scoped failed envelope with error code `compiler_no_result`, preserving source/compiler provenance and `liveGameTouched:false` before surfacing the failure.

The final failure-surfacing step also runs under the same condition and defaults a missing compiler rc to 4.

The worker contract test pins both structured fallback persistence and the new fail-closed worker-definition check.

## Findings deliberately not widened

- F3 remains integration debt: this feature line is behind operational `main`, and the rulings ledger must be reconciled/rebased deliberately before integration so `RUL-2026-09-16-001` (One Perfect Crop) and `RUL-2026-09-16-002` both survive.
- F4 remains accepted: stale-result TOCTOU is closed by concurrency cancellation, explicit remote-head equality and non-fast-forward push refusal. Do not add `--force`.
- The repository-only end-to-end `studio/quest/*` rehearsal remains an integration requirement after the reviewed compiler/worker seam lands on `main`. It must not contact the live game.

## Verification evidence

### Gated correction harness

Temporary correction workflow applied the candidate test/docs/worker changes and ran:

- source-push worker contract test — pass;
- compiler selftest — **9 passed / 0 failed**;
- Mission adapter integration — pass;
- Forge Node tests under Node 24 — pass;
- fixtures — current;
- bundle build — pass;
- skillpack regeneration — pass;
- doctrinemap / doctrine projections / packs / lawmap — pass with only the pre-existing 5 lawmap warnings.

It committed only the tested non-workflow files. The permanent workflow file was then applied separately through the repository connector because GitHub Actions tokens cannot update workflow definitions.

### Normal read-only Quest Studio CI

Run **`35165418773`**, job **`105025300496`**, against permanent tree `4197e45878a2a5f5588013c849a8fa249a500b0f`: **success**.

Every step passed:

- zero-live worker/compiler guard;
- worker trust-boundary test;
- compiler selftest;
- Mission adapter integration;
- Forge tests and fixtures;
- bundle build;
- artifact upload;
- checked bundle parity.

Forge test result from that run:

- tests: **315**
- pass: **315**
- fail: **0**
- cancelled: **0**
- skipped: **0**

The two temporary correction files were removed afterward; no product logic changed after the green permanent tree.

## Diff from the rejected review target

Relative to `1f6a1097e33108d595ca27067a7240cf14b98ded`, the clean corrected tree changes only:

- `.github/workflows/quest_studio.yml`
- `skills/building-tnr-content/scripts/quest_worker_contract_test.py`
- `forge/test/github.studio.test.mjs`
- `forge/test/quest.studio.ui.test.mjs`
- `docs/RULINGS.md`
- `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`
- regenerated `dist/building-tnr-content.zip`

No Forge runner, transport, budget, storage, reconciliation, or live-game code changed.

## Requested re-review

Fable should perform one final narrow verification against the final frozen SHA:

1. confirm F1 is closed and the two tests execute independently;
2. confirm F2's credential invariant is correctly stated and the worker-definition equality check occurs before authored source checkout/compile;
3. confirm F5 now leaves structured evidence for a missing compiler result;
4. rerun normal worker/compiler/Mission/Forge/bundle gates;
5. confirm no previously closed Quest Studio finding regressed.

If clean, return `APPROVE` or `APPROVE_WITH_NONBLOCKING_FOLLOWUP` and then perform the already-specified tiny reconciliation on `claude/forge-next-planning-v3frzi@22f1fc43f8e316d0ec8412d5595a7cd0936f98d0` against the final accepted Quest Studio SHA. Do not begin unified Forge implementation until both exact SHAs are frozen and returned to the director/ChatGPT.
