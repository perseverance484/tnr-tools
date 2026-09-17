# Forge Next Phase 1 — implementation handoff

**Status:** READY FOR FABLE / CLAUDE CODE IMPLEMENTATION  
**Date:** 2026-09-17  
**Repository:** `perseverance484/tnr-tools`  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Implementation brief:** `state/prompt_forge_next_phase1.md`  
**Program router:** `docs/forge_next/README.md`  
**Live-game policy:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## Start point

Create a fresh Fable-owned branch from the then-current `main`; suggested name:

`fable/forge-next-phase1`

Do not implement from a historical planning or Quest Studio branch. The accepted planning/design records needed for future work are now selectively consolidated onto `main` and the governing Phase 1 contract is the frozen `state/prompt_forge_next_phase1.md`.

At handoff freeze, current `main` is expected to include the consolidation and handoff commit. Reverify it immediately before branching and record the exact base/merge-base in your completion handoff.

## Director-set Phase 1 policy

- `RUL-2026-09-17-001`: capture persistence tiers are `repo-safe`, `local-only`, and `projected`; new non-content research reads default `local-only`; projected exports fail closed.
- `RUL-2026-09-17-002`: non-content research admission is demand-driven, read-only, source-audited, and fail-closed before transport.
- `RUL-2026-09-17-003`: do not merge old planning/review/temp branches as cleanup or implementation inputs.

## Required implementation outcome

Implement only the Phase 1 research/evidence capability defined by the frozen brief:

- explicit capture-tier semantics and leak-proof export behavior;
- demand-driven audited research-read registry;
- exact-input-aware filtered/paged caching and provenance;
- bounded paging and honest partial/error evidence;
- minimal ForgeCore/UI plumbing without the Phase 2 visual redesign;
- preserve all Phase 0 execution/recovery/auth/reconcile/budget/import/live-safety invariants;
- keep Quest Studio implementation deferred to Phase S.

## Source discipline

Forge generated-contract pin at freeze: `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`.

Public `studie-tech/TheNinjaRPG` main was reverified at handoff time as:

`1fd355ab92cec78148130e02c8d38834836c3181`

Reverify both relevant repository state and upstream head at implementation start. Do not silently adopt game-source drift or move the generated-contract pin inside Phase 1. Split any required adoption into a separately reviewed task.

## Baseline / gates

Start from the integrated Phase 0 baseline and rerun the canonical Forge gates before substantive implementation. Phase 0 closed with 343/343 tests and byte-identical 12-screen fixtures; treat current `main` as authority if counts have since changed.

Do not weaken the raw/gzip bundle gates. Phase 0 ended near the current ceilings, so if Phase 1 requires a budget raise, measure the feature delta first, isolate the ratchet change in a focused commit, and justify the new tight ceiling in the handoff.

Keep the task zero-live: use pinned/public source, committed captures, fixtures, fake/in-process transport, local storage substitutes, and static gates only.

## Completion handoff

Return an exact frozen SHA with at least:

- repository, branch, base, merge-base, frozen head;
- changed surfaces;
- source/game pin inspected and upstream head inspected;
- exact research registry additions and source evidence;
- capture-tier behavior implemented;
- pagination/cache identity behavior implemented;
- total/pass/fail test counts and key commands;
- fixture and checked-bundle reproducibility;
- raw/gzip before/after and any budget-ratchet commit;
- canonical Forge CI run/job;
- known debt / deliberately unsupported shapes;
- browser checks not performed;
- live requests: none;
- live writes: none;
- what has explicitly not begun.

Freeze the SHA until ChatGPT independent review returns. Do not begin Phase 2 automatically after implementation or review.