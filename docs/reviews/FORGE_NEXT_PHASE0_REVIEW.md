# Forge Next Phase 0 — independent implementation review

**Status:** FROZEN INDEPENDENT REVIEW  
**Date:** 2026-09-17  
**Repository:** `perseverance484/tnr-tools`  
**Reviewer:** ChatGPT — Engineering Auditor, supporting Release Auditor lens  
**Implementation owner:** Fable / Claude Code  
**Target branch:** `fable/forge-next-phase0`  
**Target SHA:** `8be4c5bb6a89832e705be1281f90b2395cfd11d4`  
**Base / merge-base:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`  
**Governing contract:** `state/prompt_forge_next_phase0.md@f7c77a6a160347abd824402c77537ccf5864d4dd`  
**Runner-event commit:** `413835e32f85d562390c4ac94d861b080eb662cb`  
**Live-game requests/writes by reviewer:** none

## Verdict

**CORRECTIONS_REQUIRED**

The Phase-0 architecture itself is sound and the extraction preserved the important execution invariants. The review found one blocking core-boundary contract gap and one smaller but load-bearing mechanical-gate gap. A third item is an integration prerequisite: the intended canonical CI workflow exists only in `state/staged_workflows/forge.yml` and is not yet the installed `.github/workflows/forge.yml`.

The correction surface is narrow. No redesign of ForgeCore, runner, transport, journal, reconciliation, UI visuals or storage architecture is requested.

## Evidence and verification

### Exact target / base

- remote `fable/forge-next-phase0` resolves to `8be4c5bb6a89832e705be1281f90b2395cfd11d4`;
- compare against `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` is 11 commits ahead / 0 behind with that SHA as the merge-base;
- `6306f5ce956304ba147ed4a714f343a4e980b8ff..8be4c5bb6a89832e705be1281f90b2395cfd11d4` changes only `docs/handoffs/FORGE_NEXT_PHASE0_HANDOFF.md`, so the final product/test tree is the tree exercised by the Forge run on `6306f5c`.

### Repository-side Forge CI independently inspected

GitHub Actions run `35232269682`, job `105239150889`, at product commit `6306f5ce956304ba147ed4a714f343a4e980b8ff`:

- Node `24.20.0`, npm `11.19.0`;
- `npm ci` PASS;
- `npm audit --omit=dev --audit-level=high` → `found 0 vulnerabilities`;
- `npm test` → **332 tests / 332 pass / 0 fail / 0 cancelled / 0 skipped**;
- screen/core/storage/import/boundary/budget/runner-event cases all appear by name in the passing log;
- fixtures regenerated successfully;
- checked `forge_bundle.js` rebuilt without diff.

The reviewer environment could not perform a fresh local clone because its container had no external DNS/network route to GitHub. That limitation is not treated as a pass. Independent review therefore used exact-SHA repository reads, commit diffs, and the full GitHub Actions job log rather than repeating Fable's handoff count.

### Upstream/source orientation

`studie-tech/TheNinjaRPG` `main` still resolves to `1fd355ab92cec78148130e02c8d38834836c3181`, matching the Phase-0 recorded drift observation. No game source was run and no live host was contacted.

## Findings

### F1 — BLOCKING / contract mismatch: the headless core exists, but its public state/API boundary is not frozen and the view can still widen/mutate core state directly

The Phase-0 contract explicitly requires an **“explicit core API/snapshot golden so the UI boundary cannot silently widen.”** That acceptance evidence is absent.

`forge/test/core.headless.test.mjs` proves important properties — no DOM dependency, a complete non-DOM lifecycle, sync/no-sync export, hostile notification isolation and concurrent-job refusal — but it does not pin the core's public action surface or a serializable machine-state snapshot. `ForgeCore` exposes the whole dependency bag through `Object.assign(this, d)` and exposes its mutable `state` object directly; there is no `snapshot()` (or equivalent public state contract) to freeze.

The missing golden is already producing exactly the boundary drift it was meant to catch:

- `App` aliases the object directly: `this.state = this.core.state`;
- `ManifestsScreen` writes view-only `pickerQuery` into that state;
- `ManifestsScreen` stores `_renderPicker`, a **DOM-render callback function**, on that same core state object;
- the Clear button directly assigns `app.state.selected = null` instead of invoking a core action;
- `App._persist()` writes browser/UI storage-persistence status onto `this.state.persisted`;
- `ForgeCore.loadPicker()` still permits `this.repoCache ?? this.cache`, so a consumer that omits the new dependency silently violates the Phase-0 storage-isolation invariant and places repository text back in the capture cache.

The current production composition supplies `repoCache`, so this is not a current production data-corruption bug. The current screens also remain byte-identical. The failure is architectural and evidentiary: the core seam can be widened or contaminated by a second shell while every present Phase-0 acceptance test remains green. That is the central failure mode Phase 0 was created to prevent.

**Smallest robust correction:**

1. define an explicit ForgeCore dependency contract rather than accepting/retaining arbitrary dependency-bag properties; `repoCache` should be required (or fail closed), not fall back to the capture cache;
2. expose a serializable machine-state `snapshot()` (or equivalent immutable/view-model getter) and a deliberate action surface;
3. move `pickerQuery`, `_renderPicker` and browser persistence-display state to App/view-owned state, never core machine state;
4. replace direct screen mutation of `selected` with a core action such as `clearSelection()`;
5. add the contract-required golden test that pins public action names plus snapshot keys/shape, proves the snapshot is JSON-serializable and contains no function/DOM/presentation objects, and proves UI rendering cannot add keys/functions to core machine state.

This can be corrected without changing any rendered screen byte.

### F2 — REQUIRED / mechanical-gate defect: the new architecture/safety gates have trivial syntax bypasses

The Phase-0 contract requires import direction and no-live/network confinement to **stay mechanically enforced in CI**, not merely be true at this SHA.

Two scanners do not yet cover ordinary JavaScript forms:

1. `forge/tools/check_imports.mjs` recognizes `import/export ... from` and literal dynamic `import(...)`, but not side-effect imports such as:

   `import "../ui/dom.mjs";`

   Therefore `runner/_leak.mjs` or `core/_leak.mjs` can import a view for side effects and the gate returns zero violations. Its red test injects only named `import { h } from ...`, so the blind spot is untested.

2. `forge/tools/check_boundaries.mjs` uses `/(?<![.\w])fetch\s*\(/`, which deliberately does not match qualified calls such as `globalThis.fetch(...)` or `window.fetch(...)`. It also allowlists `main.mjs` even though the stated architecture says composition should inject networking, not issue requests there. A future direct relative game request from a forbidden layer can therefore evade the static gate without hardcoding the hostname.

No such prohibited edge/request was found in the current Phase-0 tree. This is a gate-quality defect, not evidence that current code is making hidden requests. It matters because these are standing architecture/safety ratchets for every later Forge phase.

**Smallest robust correction:**

- extend import scanning to side-effect imports and add a red case that injects one into both `runner/` and `core/`;
- make the fetch detector catch qualified `.fetch(` as well as bare `fetch(` without matching `fetchImpl(`;
- remove `main.mjs` from the request-issuing allowlist unless there is an actual direct request that the architecture intentionally permits there;
- add red tests for `globalThis.fetch('/api/...')` / equivalent forbidden-layer syntax so the gate is observed failing on the bypass form.

No runtime behavior needs to change.

### F3 — INTEGRATION PREREQUISITE / process: the canonical Phase-0 CI workflow is staged, not installed

The implementation contract says Phase 0 leaves Forge with one canonical Node gate set. The intended file is correctly authored at `state/staged_workflows/forge.yml`, but `.github/workflows/forge.yml` at the frozen target remains byte-identical to `main` and therefore directly runs only the older gate sequence.

This is accurately disclosed in the Fable handoff and is caused by the repository PAT intentionally lacking Workflows permission. It is not a reason to widen that credential.

The old installed workflow still gives useful evidence because `npm test` now contains the new import, boundary, bundle-budget and screen-identity tests; run `35232269682` is therefore meaningful. But Phase 0 is not integration-ready until the canonical workflow itself is installed and exercised.

**Required integration step:** use the repository's approved user/web-UI workflow-install path to place the reviewed `state/staged_workflows/forge.yml` content at `.github/workflows/forge.yml`, then run that exact canonical workflow against the corrected Phase-0 tree. Preserve least privilege; do not grant the implementation/browser credential Workflows scope just to bypass this process.

If installing the workflow changes the Phase-0 branch SHA, return that new exact frozen SHA for the narrow re-review. If repository policy requires installing it only at integration time, treat the workflow installation as a separately reviewable integration commit and do not call Phase 0 integrated until its run is green.

## Verified strengths / findings refuted

- **Base discipline holds.** The branch is a direct descendant of the declared current-main base; no hidden merge/rebase was found.
- **Baseline defect isolation is sound.** `3b586b358ae7d2b4ee2f53bb5cfea32b58597a74` only corrects the release-pending marker test to match the actual staged/promoted lifecycle and the existing checker.
- **Runner event hook holds.** `413835e32f85d562390c4ac94d861b080eb662cb` is a focused runner/test/bundle change. The hook is synchronous, unawaited, subscriber exceptions are swallowed, and the dedicated test compares request order, journal bytes, persisted storage and final summary across no/passive/hostile subscribers.
- **Execution-core preservation holds.** No journal transition model, transport, budget or reconciliation redesign was introduced by the Phase-0 extraction.
- **Headless execution is real.** The core test drives select → start → run → capture resolution → bundle export with no DOM global and validates the produced bundle semantics.
- **Operator-visible UI parity is strong.** Twelve deterministic fixtures cover all five released screens and the final CI log passes the byte-identity tests. No visual redesign landed.
- **DOM sink hardening is correct.** `h()` rejects the required HTML sinks before either property or attribute assignment, including non-string values.
- **Storage split is correctly implemented in production composition.** `tnr_forge_repo` is a separate IndexedDB v1; capture DB stays at its prior version and rollback behavior has targeted tests.
- **Bundle/build evidence holds.** CI rebuilt the checked bundle without diff; final recorded bundle growth is modest relative to Phase-0 scope.
- **Runtime dependency audit is clean.** Production dependency audit reports zero vulnerabilities; disclosed high findings are dev-only.
- **Quest Studio scope discipline holds.** The accepted Studio branch was not merged/cherry-picked into Phase 0.
- **Zero-live boundary holds for this review.** No game request/write or game credential/session material was used.

## Unverified / nonblocking

- No real Firefox/ViolentMonkey/mobile smoke has been performed. Carrier hydration, real CSSOM behavior and real IndexedDB persistence/rollback remain browser evidence, not Node evidence.
- The game-source drift discovered by Phase 0 remains deliberately unadopted; this review does not convert it into a contract-pin move.
- Twelve screen scenarios do not cover every paused/orphan/rate-limit render branch; that is acceptable for an extraction provided later edits add fixtures for paths they touch.
- Dev-only package advisories remain separate debt.

## Correction/re-review scope

A **narrow re-review is safe** if the correction round is limited to:

1. ForgeCore dependency/API/snapshot boundary and removal of view-only mutation from core state;
2. import/network static-gate coverage plus targeted red tests;
3. installation/execution evidence for the staged canonical Forge workflow;
4. regenerated checked bundle only as mechanically required by those source changes.

Do not use this correction round to begin Phase 1, Studio integration, shell redesign, Content Admin, Builder retirement, release movement, source-pin adoption, or any live-game activity.
