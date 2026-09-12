# Forge Quest Studio — repository-backed foundation implementation brief

**Status:** APPROVED IMPLEMENTATION CONTRACT — CHATGPT-OWNED LANE A SLICE  
**Date:** 2026-09-12  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `chatgpt/forge-quest-studio-foundation`  
**Base:** `88680fb52e208747bb353ce1e37e7d33e3f41231` (approved Forge Next design branch head)  
**Shared operational baseline inspected:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Implementation owner for this slice:** ChatGPT  
**Independent review required before integration:** Fable / another independent reviewer  
**Live-game requests/writes:** prohibited

## 1. Objective

Implement the first end-to-end technical seam for the approved repository-backed Quest Studio architecture:

> Forge-authored Quest Source → approved repository operation → canonical repository compiler → machine-readable build result → Forge-readable result.

This slice proves the boundary without attempting the full Forge Next visual redesign or every quest subtype.

## 2. In scope

1. A versioned, human-authoring `Quest Source` contract suitable for Forge drafts.
2. A repository-owned subtype registry that can be rendered by Forge and consumed by the compiler.
3. A canonical `quest_compile.py` orchestration entry point.
4. A real `mission` adapter that delegates to existing `mission.py` / mission profiles rather than reimplementing mission policy.
5. A standard build-result envelope that reports `valid`, `blocked`, or `failed`, provenance, decisions/blockers, warnings, generated artifacts, and resolved engine type.
6. A GitHub Actions repository worker that accepts only approved Quest Studio request locations/branches, runs trusted repository tooling, and commits generated build output back to the request branch.
7. Forge GitHub-client primitives for safe Studio branch creation, explicit branch-scoped file writes, workflow dispatch, and result reads.
8. Unit/selftests covering the new contracts and browser-side repository client behavior.

## 3. Explicitly out of scope

- full Mission/Story/Event/Battle Pyramid visual authoring UI;
- final Forge Next shell/navigation redesign;
- Event compiler implementation;
- Story/Raid/Battle Pyramid production adapters beyond registry declarations/maturity metadata;
- AI-assisted prose/content generation;
- Content Admin publishing changes;
- live-game requests, mutations, or browser-session smoke tests;
- automatic publication;
- rewriting existing mission/quest policy into JavaScript.

## 4. Architecture constraints

- Forge is the human translation/orchestration layer; the repository remains the durable authority for facts, scripts, contracts, profiles, provenance and generated outputs.
- Browser-side checks are advisory/editing aids. Canonical compile/validation runs in repository tooling.
- The worker executes an allowlisted operation, not arbitrary shell supplied by Forge.
- Authored content and compiler code are separated: the worker runs reviewed tooling from its trusted checkout and reads only the requested source artifact from the request checkout.
- `Compile` must never imply or initiate a live-game write.
- Existing Forge mutation/reconciliation/readback behavior is not weakened or bypassed.
- Generated artifacts record the exact source revision and compiler revision used.
- Mission policy remains owned by `48_DATA_mission_profiles.json` + `mission.py`; unresolved `AWAITING_RULING` remains a structured blocker rather than a guessed default.

## 5. Initial Quest Source shape

Minimum required top-level fields:

- `schemaVersion` — starts at `1`;
- `kind` — `quest`;
- `subtype` — stable authoring recipe id;
- `requestId` — safe identifier used for build/result paths;
- `project` — optional project/workstream identity;
- `content` — subtype-specific authoring source;
- `meta` — optional UI/revision metadata ignored by deterministic compilation.

For `subtype: mission`, `content` is the existing mission design-sheet shape expected by `mission.py` rather than a second independently maintained mission schema.

## 6. Initial repository paths

The implementation may refine exact names, but preserve this separation:

- authored request source: `studio/requests/<requestId>.quest.json` on a `studio/quest/<requestId>` branch;
- generated result: `studio/results/<requestId>.build.json` on the same request branch;
- generated artifacts: `studio/builds/<requestId>/...` on the same request branch;
- subtype registry: repository-owned static/generated contract under the content skill data tree.

No normal Quest Studio compile request is written to `main`.

## 7. Worker safety contract

The repository worker must:

- accept only request branches beginning `studio/quest/`;
- accept only source paths under `studio/requests/` ending `.quest.json`;
- validate `requestId` before using it in paths;
- use workflow inputs through environment variables, never interpolate untrusted values directly into shell syntax;
- check out trusted tool code independently from the request source checkout;
- execute only the canonical Quest Studio compiler entry point;
- write only result/build paths owned by the request id;
- never contact the live game;
- expose provenance in the build result.

## 8. Browser-side GitHub contract

Existing Forge `Github` behavior used by manifests/results must remain backward compatible.

Add narrow primitives rather than changing default `main` semantics silently:

- branch/ref lookup;
- create request branch from a known base;
- explicit branch-scoped `put`;
- workflow dispatch with explicit workflow/ref/inputs;
- branch-scoped result reads.

All GitHub bearer traffic remains GitHub-only and separate from the TNR game session.

## 9. Verification gates for this slice

Required before handoff:

- Python compiler selftest/unit tests for source validation, Mission delegation, structured blockers, and result provenance;
- Forge Node tests for branch-scoped GitHub URLs/writes/dispatch and legacy compatibility;
- existing Forge `npm test`;
- existing Forge fixture regeneration gate;
- Forge bundle fresh build equals checked bundle if Forge source changes;
- static verification that the worker has no live-game URL/use;
- workflow syntax/review checks as feasible without running live production operations.

If the checked bundle must change because Forge source changes, regenerate it by the repository build and include it in the handoff; do not hand-edit it.

## 10. Review focus

Independent review should attack especially hard:

- branch/path injection in the repository worker;
- whether untrusted request-branch code can execute;
- whether Forge can accidentally write Quest Studio drafts to `main`;
- whether browser-side rules duplicate canonical Python policy;
- whether structured `blocked` versus `failed` results preserve the difference between missing user decisions and tool defects;
- whether provenance is sufficient to reproduce a build;
- whether any new path weakens current live-operation/auth/reconciliation safety.