# Forge Next Phase 0 — correction re-review

**Status:** CORRECTIONS REQUIRED — ONE NARROW RESIDUAL BLOCKER
**Date:** 2026-09-17
**Repository:** `perseverance484/tnr-tools`
**Target:** `fable/forge-next-phase0@12a9d4db881b552c1aa93ae6fddd57f5d81772c9`
**Previous target:** `8be4c5bb6a89832e705be1281f90b2395cfd11d4`
**Previous review:** `chatgpt/review-forge-next-phase0@6df00b836d1af3b7b06f3689ca00648e03af51bd`
**Base / merge-base:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`
**Live requests/writes:** none

## Verdict

`CORRECTIONS_REQUIRED` for one residual F1 boundary defect. F2 is closed. F3 remains an integration prerequisite, not an implementation defect.

## F1 — residual blocker: the state golden can still be bypassed through the public API

The correction materially improves the boundary: dependencies are explicitly allowlisted; `repoCache` is required; a serializable `snapshot()` exists; view-only `pickerQuery`, picker callback and persistence state moved onto `App.view`; `clearSelection()` moved into the core; and `core.contract.test.mjs` pins public method names and initial state keys.

One path still defeats the stated invariant that the UI boundary cannot silently widen:

```js
go(screen, patch = {}) { Object.assign(this.state, patch, { screen }); this.changed(); }
```

`patch` is unconstrained. A current or future shell can call `go("jobs", { pickerQuery: "x" })` (or any other new field), which creates a new key on `core.state`. The current golden does not reject this API behavior because `snapshot()` copies only the fixed `STATE_KEYS`, and the render test exercises only today's known calls.

There is a second manifestation of the same boundary: `App.state` returns the mutable `core.state` object directly, and `App.mount()` itself writes `this.state.screen = "jobs"`. The handoff says the getter is read-through and the view no longer writes core state, but that statement is not literally true at the frozen SHA.

### Smallest robust correction

Keep the architecture. Close only the mutation seam:

1. make `go()` accept only an explicit, validated patch key set (today effectively `jobId`, with `screen` validated separately), or replace it with named state-transition methods;
2. stop returning a mutable machine-state object as the UI's general `state` surface. Prefer rendering from `core.snapshot()` / a read-only view-model and invoking actions for changes; at minimum ensure every core-state write is through a validated core action;
3. remove `App.mount()`'s direct `state.screen` write (use a core action);
4. add red tests proving an unknown `go()` patch key is refused and that rendering/mounting cannot introduce a new state key.

This is narrow and does not require a wider architecture review.

## F2 — closed

The exact static-gate bypasses from the first review are closed:

- `check_imports.mjs` now recognizes side-effect imports in addition to named/export-from and dynamic imports;
- the red test injects side-effect UI imports into both `runner/` and `core/` and requires nonzero exit;
- `check_boundaries.mjs` now catches bare and qualified `.fetch(...)` calls outside the allowed network layers;
- `main.mjs` is removed from the network allowlist;
- red tests cover bare, `globalThis.fetch` and `window.fetch`, while preserving the injected `fetchImpl` and `.fetch.bind(...)` composition seam.

No current forbidden import or direct network path was found in the corrected tree.

The scanner is intentionally lexical rather than a full JavaScript parser; that is future hardening, not a correction blocker for this bounded finding.

## F3 — integration prerequisite still open

The canonical workflow remains staged at `state/staged_workflows/forge.yml`; installed `.github/workflows/forge.yml` still has the older sequence. The implementation branch correctly did not widen the repository credential to gain Workflows write.

Before integration, the director/operator must install the staged workflow through the approved GitHub web-UI path, then the corrected exact tree must receive a green run of that installed canonical workflow (import direction, static boundaries, full tests, both fixture sets, checked bundle, bundle budget, release pin). If the install commit moves the branch head, return that exact head for final narrow verification.

## Evidence / verification

Repository state verified:

- branch head exactly `12a9d4db881b552c1aa93ae6fddd57f5d81772c9`;
- current `main` remains `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`;
- correction is five commits directly on top of reviewed `8be4c5b`;
- changed surface is limited to correction handoff, core/UI boundary, the two static gates/tests and rebuilt bundle.

The correction handoff reports 340/340 tests and byte-identical screen fixtures. The repository connector in this review environment could not execute a clean local checkout, so this re-review does not claim an independent local rerun. Source inspection independently verified the corrected F2 mechanics and the residual F1 path above.

No live-game request or write was made.

## Next step

Fable should make one narrow F1 correction on its own branch, rerun the full 340+ suite/fixtures/build/gates, and freeze a new SHA. The director should install the staged canonical `forge.yml` before integration; the installed workflow must then run green on the final corrected tree.

A further re-review can remain narrow to the state-mutation correction, test/bundle fallout, exact branch head, and installed-workflow evidence.