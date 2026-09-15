# Forge Quest Studio foundation — follow-up review disposition

**Status:** FOLLOW-UP CORRECTIONS GREEN — M1 CREDENTIAL-SCOPE RULING PENDING  
**Date:** 2026-09-15  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `chatgpt/forge-quest-studio-foundation`  
**Implementation owner:** ChatGPT  
**Original Fable-reviewed target:** `cda8ac76100b2fa4b5429bea27c3c8c80353e240`  
**First corrected freeze:** `b536bbe5306f14f606d889d8234e537f0d55b300`  
**Fully verified follow-up implementation parent:** `1e4bfb9d790bed482ce04182521baf61a42687d1`  
**Live-game requests/writes:** none; prohibited throughout this pass  

This handoff responds to the later `REVIEW_REQUEST.md` / `docs/reviews/FORGE_QUEST_STUDIO_FOUNDATION_REVIEW.md` findings that were not fully covered by the first correction round. It supplements, and does not rewrite, the earlier handoffs.

## 1. Required finding dispositions

| Finding | Disposition | Result |
|---|---|---|
| **M1 — Actions: write credential blast radius** | **ACCEPTED — USER DECISION REQUIRED** | Not silently changed. Current `workflow_dispatch` transport still requires repository-wide Actions write. The code-side workflow allowlist remains defence in depth only and does not reduce what a stolen token can call directly. Resolve before final Studio integration/rehearsal. |
| **M2 — generated-artifact path confinement** | **ACCEPTED — CLOSED IN FIRST CORRECTION ROUND** | `%`, `?`, `#`, traversal, empty segments and backslashes are refused; GitHub content paths are segment-encoded. |
| **M3 — generated manifest has no digest binding** | **ACCEPTED — CLOSED THIS ROUND** | `quest_compile.py` now records `generated.manifestSha256` from the exact bytes written. `QuestStudioRepository.generatedManifest()` requires a 64-hex digest, hashes the fetched bytes in-browser with SHA-256, and refuses a mismatch before displaying the artifact. Integration tests bind the envelope digest to `manifest.json`. |
| **M4 — edited draft can reopen with previous build shown current** | **ACCEPTED — CLOSED THIS ROUND** | Every normal authored draft save now invalidates persisted `sourceCommit` and `lastResult`; compile/poll persistence explicitly opts into preserving build identity. A jsdom close/reopen regression proves an edit cannot trigger or display the previous submitted revision as current. |
| **M5 — unresolved S profile looks authorable** | **ACCEPTED — CLOSED IN FIRST CORRECTION ROUND** | `AWAITING_RULING` is sentinel-aware, disabled and rendered as awaiting ruling; compile is blocked locally. |
| **M6 — weakened loader allowlist / wrong PAT scope copy** | **ACCEPTED — CLOSED IN FIRST CORRECTION ROUND** | Exact origin allowlist assertions were restored; Settings and dispatch 403 copy accurately describe the current Contents + Actions write requirement, subject to M1's eventual transport/scope ruling. |

## 2. Minor finding dispositions

| Finding | Disposition | Result / ownership |
|---|---|---|
| **m1 — worker shell guard misses scalar forms / github.event.inputs** | **ACCEPTED — CLOSED THIS ROUND** | Worker contract extraction now covers literal/folded multiline and single-line `run:` scalars and rejects both `${{ inputs.* }}` and `${{ github.event.inputs.* }}` shell interpolation forms. |
| **m2 — blocked/failed classification coupled to English MissionError prose** | **ACCEPTED — NON-BLOCKING DEBT** | Still true. Do not widen this slice into `mission.py` canonical error taxonomy. Replace prose coupling with a typed/code contract before the second adapter or during Phase S canonical-owner cleanup. |
| **m3 — objective_count enforced only in browser** | **ACCEPTED — STUDIO CORRECTNESS CLOSED; OWNER CLEANUP DEFERRED** | The first correction round added canonical Quest Studio adapter enforcement against generated objectives/battle nodes. Browser checks are now advisory projections backed by the repository adapter. Moving the rule into `mission.py` itself remains the K-36 canonical-owner cleanup for unified integration. |
| **m4 — local draft persistence failure is swallowed while UI says saved** | **ACCEPTED — NON-BLOCKING FORGECORE DEBT** | Best-effort local draft persistence remains. The unified durable Project/ForgeCore draft store should expose sync/persistence state rather than growing the temporary overlay's storage model. |
| **m5 — absent result was presented as Build still running** | **ACCEPTED — CLOSED IN FIRST CORRECTION ROUND** | Copy now says no result is available and distinguishes possible early failure from continued execution. Full run identity belongs to ForgeCore. |
| **m6 — buildResult staleness fails open if expected source commit omitted** | **ACCEPTED — CLOSED THIS ROUND** | `buildResult()` now requires an exact 40-hex submitted source commit and refuses before reading otherwise. Staleness comparison therefore fails closed. |
| **m7 — Github.put branch undefined silently falls back to main** | **ACCEPTED — LATENT, NON-BLOCKING DEBT** | Unreachable from current Studio because `questBranch()` always supplies a validated branch. Preserve for Github/Core API cleanup; do not broaden this correction pass into legacy caller semantics. |
| **m8 — meta participates in sourceSha256 though compilation ignores it** | **DISPUTED AS A DEFECT** | `sourceSha256` is intentionally the identity of the complete authored Quest Source envelope, not a semantic-content-only digest. `meta` being ignored by deterministic compilation does not imply it should be excluded from source identity. If a semantic content digest is later useful, add a distinct field rather than weakening provenance identity. |
| **m9 — zero-live guard is not transitive over imported modules** | **ACCEPTED — LIMITATION, NON-BLOCKING** | Correct: the static guard is a tripwire, not a whole-program network proof. Worker separation, reviewed trusted imports and zero-live task discipline remain the stronger boundary. Phase 0 may add broader static dependency analysis if it remains cheap and deterministic. |
| **m10 — Studio CI did not watch mission.py / Mission profile policy** | **ACCEPTED — CLOSED THIS ROUND** | `quest_studio_ci.yml` now triggers on `mission.py` and `48_DATA_mission_profiles.json` changes in push and PR paths. |
| **m11 — Mission integration ignored warnings/art regression** | **ACCEPTED — CLOSED THIS ROUND** | The integration gate now fails if the valid Mission path returns warnings and explicitly proves art requirements remain available. |
| **m12 — unsupported adapter capability gap returned as blocked** | **DISPUTED AS A CURRENT CORRECTNESS DEFECT; TAXONOMY REFINEMENT DEFERRED** | `subtype_not_executable` is an explicit machine blocker and unsupported subtypes are already rendered unavailable. The current `blocked` envelope is broader than only director decisions. Unified result taxonomy may split capability-unavailable from decision-blocked later, but no false executable state or live hazard exists today. |
| **m13 — branch files without trailing newline** | **ACCEPTED IN MATERIAL PART / COSMETIC REMAINDER** | `docs/RULINGS.md`, the append-oriented ledger, was fixed in the first correction round. Remaining newline-only style debt does not justify broad unrelated file churn in this slice. |

## 3. Review acknowledgements

- The review correctly observed that the shared `h()` value-property change repaired the existing results-bundle textarea export while also changing existing-screen behaviour. That effect is acknowledged; the subsequent HTML-sink hardening and full Forge suite cover the shared helper.
- The historical first handoff understated how many temporary bundle-sync workflow cycles were used before its frozen target. The review's correction is accepted as historical evidence; no temporary sync workflow survives in the current tree.

## 4. Process-item dispositions

| Process item | Disposition |
|---|---|
| `docs/00_INDEX.md` does not route `quest_compile.py`, worker contract test, or subtype registry | **ACCEPTED — INTEGRATION STEP.** Add routing when the seam becomes part of the shared operational baseline; do not make a feature branch's unmerged artifacts look like main canon early. |
| `studio/*` is an undeclared branch namespace with no cleanup contract | **ACCEPTED — UNIFIED ARCHITECTURE / K-37.** Declare namespace, retention and cleanup before broad use. |
| `scrub.yml` runs on every Studio source-branch push | **ACCEPTED — DELIBERATE OPERATING-COST DECISION FOR INTEGRATION.** Privacy scanning authored source is defensible, but the cost/noise should be explicit rather than accidental. |

## 5. Follow-up implementation changes

Relative to first corrected freeze `b536bbe5...`, the follow-up implementation changes only:

- `.github/workflows/quest_studio_ci.yml` — watch canonical Mission policy/profile inputs;
- `forge/src/studio/repository.mjs` — manifest digest verification; fail-closed source identity for build reads;
- `forge/src/studio/ui.mjs` — authored edits invalidate submitted-build identity;
- `forge/test/github.studio.test.mjs` — manifest digest mismatch and missing source identity regressions;
- `forge/test/quest.studio.ui.test.mjs` — edit/reopen stale-build regression;
- `forge_bundle.js` — canonical rebuild from corrected source;
- `skills/building-tnr-content/scripts/quest_compile.py` — emit generated manifest SHA-256;
- `skills/building-tnr-content/scripts/quest_compile_integration_test.py` — prove manifest digest and art-warning integrity;
- `skills/building-tnr-content/scripts/quest_worker_contract_test.py` — broaden shell-scalar/input interpolation detection.

No runner, transport, journal, budget, reconcile or live-game execution path was changed.

## 6. Verification

### Gated follow-up harness

Temporary workflow `quest-studio-followup-temp` run **35027535032** completed **success** before product changes were committed. It passed:

- follow-up patch application assertions;
- worker trust-boundary test;
- compiler selftest;
- Mission adapter integration;
- Forge test suite, fixtures and canonical bundle build;
- doctrine map, doctrine projection, pack/TOC and lawmap coherence gates;
- product-only commit after all gates were green.

The temporary workflow and patch script were subsequently removed from the branch.

### Final normal read-only Quest Studio CI

Run **35027762280**, job **104578778182**, against implementation parent `1e4bfb9d790bed482ce04182521baf61a42687d1`: **success**.

Verified in that run:

- zero-live compiler/worker guard: PASS;
- worker trust-boundary test: PASS;
- compiler selftest: **9 passed, 0 failed**;
- Mission integration: PASS, including manifest digest and art-requirements integrity;
- Forge suite: **316 passed, 0 failed**;
- fixtures regenerated with no diff;
- canonical `forge_bundle.js`: **431.2 KB**;
- generated bundle artifact upload: PASS;
- checked bundle parity (`git diff --exit-code -- forge_bundle.js`): PASS.

`npm ci` continues to report the previously disclosed three high-severity dev-dependency advisories. No new runtime path was demonstrated; dependency audit remains separate debt.

No live TNR request, write, capture or publication occurred.

## 7. M1 decision still required before final re-review/integration

The follow-up code is intentionally **not** claiming M1 closed.

The three practical choices remain:

1. **Source-push trigger / no Actions write on the browser token.** Keep the operator PAT at repository Contents write; pushing the exact Quest Source revision triggers the trusted worker. This narrows credential blast radius, but run correlation/cancellation must be redesigned around branch + source SHA and the worker must be re-reviewed.
2. **Keep `workflow_dispatch` and grant Actions write.** Smallest change to the proven seam and clearest explicit request correlation, but a stolen browser token can invoke other dispatchable repository workflows directly. The Forge-side allowlist does not mitigate stolen-token API use.
3. **Keep Actions write but reduce dispatchable-workflow blast radius first.** Retain explicit dispatch while hardening or retiring workflows such as `relay.yml` so the widened token cannot use them to land arbitrary repository changes on `main`. This is a wider repository-security change and needs its own review.

Do not send this branch for its final narrow Fable re-review until the director rules M1 and any resulting transport/security change is applied and gated.
