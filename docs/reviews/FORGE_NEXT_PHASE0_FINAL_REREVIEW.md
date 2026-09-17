# Forge Next Phase 0 — final narrow re-review

**Status:** APPROVE_WITH_INTEGRATION_PREREQUISITE
**Date:** 2026-09-17
**Repository:** `perseverance484/tnr-tools`
**Lead:** ChatGPT / Engineering Auditor
**Target:** `fable/forge-next-phase0@9af54dd4f6621b91b028aacfaacc175ef038644f`
**Base / merge-base:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`
**Previous reviewed head:** `12a9d4db881b552c1aa93ae6fddd57f5d81772c9`
**Prior review:** `chatgpt/review-forge-next-phase0@a8c01ecce498820e41334f32e65c4cd250affeea`
**Live-game requests/writes:** none

## Verdict

The residual F1 correction is accepted. No further Fable code correction is required for Phase 0 before the CI-install prerequisite is satisfied.

Phase 0 is **not yet integration-ready** because the canonical Forge workflow remains staged rather than installed. Install `state/staged_workflows/forge.yml` through the approved operator/web-UI path, then run that installed workflow green against the final corrected tree. If installing the workflow moves the implementation branch SHA, return the new exact SHA for one final pointer/workflow-only confirmation before integration.

## F1 — CLOSED

The previous review required four things: constrain `ForgeCore.go(screen, patch)`, stop exposing top-level mutable machine state to the view, route mount-time state mutation through a core action, and add a red unknown-patch-key test.

At the accepted target:

- `SCREENS` and `GO_PATCH_KEYS` explicitly constrain the `go()` routing surface;
- `go()` rejects unknown screens, non-object patches and unknown state keys before changing state;
- `App.state` wraps the core state in a write-refusing Proxy for top-level writes/adds/deletes/definitions;
- `App.mount()` calls `core.go("jobs")` instead of assigning `state.screen`;
- the screen-scenario harness routes job selection through `go("run", {jobId})` rather than direct assignment;
- `core.contract.test.mjs` includes red cases for unknown keys, mixed valid/invalid patches, unknown screens, non-object patches and direct view state writes;
- the 12 committed screen fixtures are reported byte-identical.

This closes the specific silent-widening seam reported in the prior review.

### Nonblocking hardening note

The view-state Proxy is shallow: nested objects such as `state.selected` and entries under `state.picker` are still ordinary references. Current screen code was inspected and no nested machine-state mutation was found in the reviewed path. This is therefore not a Phase-0 blocker, but a future shell should continue to mutate machine state only through core actions. If later UI work starts editing nested state directly, make the view read model deeply read-only or render from a snapshot rather than allowing that pattern to become a new convention.

## F2 — remains CLOSED

The F1-only delta from `12a9d4d` does not touch the import/network gates. The previously accepted side-effect-import and qualified-fetch protections remain unchanged.

## F3 — integration prerequisite remains OPEN

`state/staged_workflows/forge.yml` contains the required canonical gate sequence, including import direction, static boundaries, screen-fixture reproducibility and bundle budget.

`.github/workflows/forge.yml` at the reviewed target is still the older installed workflow. It runs `npm ci`, runtime dependency audit, `npm test`, envelope fixtures and bundle reproducibility, but does not separately run the complete staged Phase-0 gate sequence.

Do not widen the repository PAT to solve this. The operator should install the staged workflow through the existing approved GitHub web-UI path and obtain a green canonical run before integration.

## Verification and evidence

Repository state verified:

- current `main`: `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`;
- target branch tip: `9af54dd4f6621b91b028aacfaacc175ef038644f`;
- target remains a direct descendant of the base; merge-base is unchanged;
- delta from `12a9d4d` is confined to the F1 correction, its tests/scenarios, regenerated bundle and handoff.

Author handoff reports:

- `npm test`: 343 / 343 pass / 0 fail / 0 cancelled / 0 skipped;
- 12 screen fixtures byte-identical;
- bundle raw 417,370 B / 430,000 B budget (97.1%);
- bundle gzip 79,294 B / 81,000 B budget (97.9%);
- import-direction: 37 modules / 62 cross-layer imports / 0 violations;
- boundary gate: 0 violations, pin `345d18ac`.

The correction test count was not independently rerun in a local checkout in this review environment. GitHub shows only the repository `scrub` workflow on the final stamp SHA; the canonical Forge workflow is precisely the still-open F3 installation prerequisite. The code/test assertions above were therefore verified by direct inspection at the exact frozen SHA, with the reported local command results treated as author evidence until the canonical workflow is installed and run.

## Remaining release/browser evidence

No real-browser or live-session verification was performed. That remains separate from Phase-0 code acceptance and must not be represented as verified. Real-device/browser smoke remains required before release, not before merging this architecture slice unless the release workflow says otherwise.

## Review-process correction

During creation of this review branch, the reviewer accidentally created a placeholder review file on the Fable branch, temporarily advancing the branch by one commit. The branch ref was immediately restored to the exact frozen target `9af54dd4f6621b91b028aacfaacc175ef038644f`, and the restored branch tip was re-read from GitHub before this review was frozen. No implementation file on the reviewed tree was changed; the stray commit is not on the Fable branch history reachable from its current tip.

## Next step

1. Operator installs `state/staged_workflows/forge.yml` as `.github/workflows/forge.yml` through GitHub web UI without widening the PAT.
2. Run the installed canonical Forge workflow green against the corrected Phase-0 tree.
3. If the install changes the branch SHA, return that exact SHA for a final workflow/pointer-only confirmation.
4. After that confirmation, Phase 0 may integrate to fresh `main` under `docs/DEVELOPMENT_WORKFLOW.md`.
5. Do not begin Phase 1 until Phase 0 integration is complete.
