# Forge Quest Studio foundation — correction-round handoff

**Status:** FROZEN CORRECTION HANDOFF — NARROW INDEPENDENT RE-REVIEW REQUIRED  
**Date:** 2026-09-13  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `chatgpt/forge-quest-studio-foundation`  
**Implementation owner:** ChatGPT  
**Original reviewed target:** `cda8ac76100b2fa4b5429bea27c3c8c80353e240`  
**Independent review:** `claude/forge-quest-studio-audit-j4jhcf@43b8ef1c4b6f80042a52c5a73fd64a1314dd030a`  
**Current shared baseline observed at correction start:** `main@6848a7805d912378f7f8eb27f52c9625dd10ac54`  
**Fully verified corrected implementation parent:** `44c3178451541f38e913ff00f0e5d07eb797ebbd`  
**Live-game requests/writes:** none; prohibited throughout this correction round  

This document supplements the original `FORGE_QUEST_STUDIO_FOUNDATION_HANDOFF.md`; it does not rewrite the historical first-review record. The SHA containing this handoff is the frozen re-review target.

## 1. Correction-round disposition

The correction round accepted Fable findings F1–F11 and F14 where they described a current implementation defect or low-cost hardening opportunity. It deliberately did **not** change the transport family from `workflow_dispatch` to `repository_dispatch`; that remains an integration-architecture choice for the unified ForgeCore contract. F12 (Studio branch/build retention), F13 (multi-draft/cross-tab lifecycle) and F15 (unrelated dev-dependency advisories) remain later integration/debt items.

### F1 — loader safety assertion weakening — corrected

- Restored the exact two-origin `@match` allowlist assertion and the explicit no-`/forge`-only assertion.
- Restored the inherited activation/entry assertions.
- Kept only the legitimate release-marker correction, now expressed as the actual state contract: a released loader whose `@version` equals the package has zero pending markers; a staged newer package has exactly one marker naming that package.

### F2 — unresolved Mission profile rendered as settled — corrected

- Mission profile reads are sentinel-aware.
- A profile containing `AWAITING_RULING` is disabled and rendered as `awaiting ruling`, never `NaN`, `? nodes` or `no combat`.
- Draft readiness blocks the unresolved profile before compile.
- Regression coverage loads the real `48_DATA_mission_profiles.json`, including the S profile.

### F3 — PAT instruction did not match `workflow_dispatch` permission — corrected for current transport

- Settings now states that the fine-grained PAT needs `Contents: write + Actions: write` on `tnr-tools` for the current dispatch model.
- A dispatch HTTP 403 reports the missing Actions permission explicitly.
- The future `repository_dispatch` alternative remains deferred to the unified architecture contract rather than being silently substituted in a correction pass.

### F4 — failed source envelope could lose request identity — corrected

- `quest_compile.py` accepts a validated worker `--request-id` and binds authored source identity to it.
- Failure envelopes preserve that validated request id even when authored source is malformed or names an unknown subtype.
- Request-id mismatch between worker identity and Quest Source is refused.
- Forge can therefore render the structured `failed` result rather than rejecting `requestId:null` and wedging the draft.

### F5 — Mission profile shape only advisory in browser — corrected in the Quest Studio adapter

- `compile_mission` now checks the generated quest against ratified numeric Mission-profile `objective_count` and `battle_nodes` after `mission.py` builds it.
- The check reads the actual generated manifest at `data.content.objectives` and counts battle primitives.
- A mismatch returns structured blocker `profile_shape_unmet`.
- General `mission.py` policy was **not** rewritten; the additional conformance rule is scoped to the Quest Studio adapter.

### F6 — boundary failures / ambiguous no-result state — corrected within the current worker model

- Dispatch identity is validated before the authored checkout.
- Authored content is checked out by exact `source_sha`, not branch tip, removing the branch-advance race.
- Post-checkout content/symlink boundary failures are persisted as request-scoped `status: failed` envelopes with the validated request id before the job exits non-zero.
- The Studio no-result copy no longer asserts that a build is definitely still running; it states that no result is available and may reflect an early worker failure.
- Full workflow-run-id/status tracking is not introduced in this slice; that belongs naturally in the later ForgeCore build-state machine.

### F7 — generated manifest inspection hidden behind Studio overlay — corrected

- Generated-manifest inspection now renders inside the visible Studio result surface as a read-only field.
- Direct promotion/preflight handoff into the existing live runner is still intentionally withheld pending the reviewed promotion contract; inspection is not presented as execution readiness.

### F8 — encoded traversal / query injection in artifact paths — corrected

- Result-supplied generated-artifact tails reject `%`, `?` and `#` in addition to traversal, empty segments and backslashes.
- GitHub Contents GET/PUT paths encode each repository path segment instead of interpolating path text into the URL.
- Regression coverage includes percent-encoded traversal and `?ref=main` injection attempts.

### F9 — general workflow dispatch primitive — corrected for current implementation

- Browser dispatch is allowlisted to `quest_studio.yml`; other workflow names refuse before fetch.
- Switching to `repository_dispatch` remains a later architecture decision because it changes the transport/auth model rather than correcting the existing seam in place.

### F10 — worker-order contract hardening — corrected

- Main/request/path/SHA identity validation precedes authored checkout.
- Authored checkout is exact-SHA pinned.
- Content/symlink validation precedes compile.
- The worker contract test now asserts this ordering and recognizes multiline `run` block forms rather than relying on one literal indentation shape.
- Untrusted workflow inputs remain excluded from shell interpolation and request content remains data-only.

### F11 — latent generic DOM HTML-string sink — hardened

- `h()` rejects the prohibited HTML property family before generic property assignment.
- The denylist is expressed without embedding the forbidden sink literals in `forge/src`, preserving the existing repository source-grep law.
- A direct behavioral regression proves object coercion cannot reach the sink.

### F14 — rulings ledger newline — corrected

`docs/RULINGS.md` now ends with a newline so the append-oriented ledger remains safe for the next entry.

## 2. Verification evidence

Two layers of evidence were used.

### Gated correction harness

The correction harness repeatedly applied the full candidate patch to an ephemeral checkout and refused to commit product changes until gates passed. Earlier candidate mistakes were caught before product commit: stale contract-test expectations, an incorrect generated-manifest objective path, and a source-grep interaction in the HTML-sink hardening.

The final substantive harness pass (`quest-studio-correction-round` run `34765930271`) passed:

- zero-live worker/compiler static guard;
- strengthened worker trust-boundary contract;
- compiler selftest: **9 passed, 0 failed**;
- Mission integration including profile-shape refusal and failure-envelope identity;
- Forge Node suite: **314 passed, 0 failed**;
- fixture regeneration/diff;
- canonical bundle build;
- skillpack regeneration;
- doctrinemap: 0 errors / 0 warnings;
- doctrine projection check;
- packs/TOCs check;
- catalog-sync selftest;
- lawmap: 93 laws / 93 matrix rows / 77 citations / 0 errors / 5 pre-existing warnings.

That run's final push failed only because the Actions token cannot modify workflow files. The already-tested source/generated changes were subsequently committed separately and the tested workflow delta was applied through the repository-scoped connector.

### Final normal read-only CI on the combined tree

`quest-studio-ci` run **`34766148917`**, job **`103747351141`**, against corrected implementation parent **`44c3178451541f38e913ff00f0e5d07eb797ebbd`** completed **success**:

- zero-live network guard: PASS;
- worker trust-boundary test: PASS;
- compiler selftest: PASS;
- Mission adapter integration: PASS;
- Forge tests + fixtures: PASS;
- canonical bundle build: PASS;
- generated bundle upload: PASS;
- checked `forge_bundle.js` parity: PASS.

The correction pass generated a checked Forge bundle of approximately **430.0 KB**. No live TNR request, read, write, capture or publication occurred.

## 3. Deliberately deferred to unified Forge integration

These are not correction-round regressions and should not be smuggled into this slice:

1. **Transport redesign:** whether to replace `workflow_dispatch` with `repository_dispatch` or another service boundary, and the final least-privilege credential model.
2. **Studio branch/build lifecycle:** retention, cleanup, promotion and immutable adoption policy for `studio/quest/*` work.
3. **Multi-draft/project persistence:** replace the single foundation draft slot with the Project Workspace / ForgeCore draft store and cross-tab ownership model.
4. **Full build-state machine:** workflow run identity/cancellation/progress should move into ForgeCore rather than growing the temporary overlay's polling logic.
5. **Studio → runner promotion:** generated output remains inspection-only until a reviewed promotion contract feeds existing Forge preflight/journal/reconciliation safely.
6. **Temporary Studio shell:** `.qs-*` styling, launcher injection and full-screen overlay remain scaffolding to be absorbed by the approved unified Forge Next shell/design system.
7. **Dependency advisories:** the existing three high-severity npm advisories are dev-dependency debt with no demonstrated Quest Studio runtime path; track separately.

## 4. Re-review request

Fable should review the correction delta from original target `cda8ac76100b2fa4b5429bea27c3c8c80353e240` to the SHA containing this handoff.

Primary closure scope is F1–F11 and F14, plus reproduction of the worker/compiler/Forge/bundle gates. Because F10 changes worker ordering, the trust boundary should be inspected again rather than assumed unchanged. The product architecture itself is not reopened unless a correction introduced a new contradiction.

If that narrow re-review is clean, this Quest Studio slice is ready to enter the **unified Forge implementation-contract/integration step**, alongside the separately corrected Fable planning package. It should not be merged blindly as a competing product shell; the proven repository/compiler seam should be absorbed into the reviewed ForgeCore and approved Forge Next UX architecture.
