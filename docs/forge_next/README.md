# Forge Next — consolidated planning index

**Status:** CURRENT ROUTER FOR CONSOLIDATED FORGE NEXT PROGRAM RECORDS  
**Date:** 2026-09-17  
**Consolidation base:** `main@b0bae3bcd6e3d9cf76de48237892ac099fa7a60c`  
**Accepted planning source:** `claude/forge-next-planning-reconciled@ba51a28a99a7748e61de0c2768bd73ab9c65c856`  
**Accepted Quest Studio implementation source:** `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`

This directory preserves the accepted Forge Next planning material needed for future implementation phases without merging the old planning branch's stale operational state, generated snapshots, or implementation tree into current `main`.

Repository precedence remains governed by `docs/00_INDEX.md`. These planning documents do not override doctrine, engine laws, generated contracts, captures, current operational state, later user rulings, or a newer phase implementation brief.

## Current program state

- **Phase 0 — COMPLETE / integrated.** Implementation `3130f9433810cca4f8eca78b80aeb4dc8eb7ddb0`; integration/current release-pin follow-up landed on `main` and canonical Forge CI was green.
- **Phase 1 — READY / FROZEN.** Governing implementation contract: `state/prompt_forge_next_phase1.md`. Director policy is settled by `RUL-2026-09-17-001` and `RUL-2026-09-17-002`.
- **Phase S / Quest Studio — ACCEPTED FUTURE INTEGRATION SOURCE.** Keep `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`; do not infer that its implementation is already on `main`.
- **Phase 2+ — not begun.** Use the roadmap/design records below as planning evidence, then write a fresh phase brief against live `main` before implementation.

## Consolidated planning records

The following files are copied byte-for-byte from the accepted planning/design sources and therefore retain their original historical status language and measured baselines:

- `A_ARCHITECTURE_MAP.md`
- `D_IA_AND_JOURNEYS.md`
- `D_VISUAL_SYSTEM.md`
- `E_CONTENT_ADMIN_FEASIBILITY.md`
- `F_ARCHITECTURE_RECOMMENDATION.md`
- `G_ROADMAP.md`
- `H_RISK_REGISTER.md`
- `I_TEST_STRATEGY.md`
- `J_MIGRATION_AND_RETIREMENT.md`

`history/K_USER_DECISIONS_PLANNING.md` preserves the old decision register as historical planning evidence. It is **not** the current open-decision authority: K-06 and K-17 are now ruled, K-26's credential-scope half was previously settled by `RUL-2026-09-16-002`, and later phase briefs must re-evaluate which remaining entries still block the phase being started.

## Consolidated director/design records

Under `docs/design/` this consolidation preserves:

- `FORGE_NEXT_VISUAL_DIRECTION.md` — approved visual/product north star;
- `FORGE_NEXT_COLOR_SEMANTICS.md` — operation/outcome color-separation principles;
- `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md` — proposal/evidence for later Phase 2, not a final token lock;
- `FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md` — later design-review gate;
- `FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md` — authority-level map for the design set;
- `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` — director-set Forge/repository authority boundary;
- `FORGE_NEXT_QUEST_STUDIO.md` — shared Quest Studio parent product contract.

## Consolidated review evidence

- `docs/reviews/FORGE_NEXT_PHASE0_INTEGRATION_CLEARANCE.md` preserves final Phase 0 clearance.
- `docs/reviews/QUEST_STUDIO_FINAL_CORRECTION_REVIEW.md` preserves the final accepted Quest Studio review and its nonblocking follow-ups.
- `docs/reviews/FORGE_NEXT_BRANCH_CONSOLIDATION_AUDIT.md` records why old Forge branches are not wholesale merge sources.
- `docs/reviews/FORGE_NEXT_BRANCH_CLEANUP_FINAL.md` records the approved keep/delete sequence after this consolidation integrates.

## Historical package not copied wholesale

The accepted planning branch contains large evidence matrices and intermediate workflow inventories that were measured against an older repository baseline. They remain retrievable by exact SHA at `ba51a28a99a7748e61de0c2768bd73ab9c65c856` but are intentionally not copied wholesale into current `main`.

In particular, do not treat historical parity/evidence matrices as current measurements. Re-run the relevant producer against the live implementation when a future phase depends on a number.

This also avoids carrying previously identified stale planning statements forward as current facts. Current briefs/rulings win for phase state, credential scope, evidence-generator behavior, and Quest Studio manifest-digest binding.

## Starting a future phase

1. Verify live `main` and current operational state.
2. Read `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`/`CLAUDE.md`, development workflow, and applicable role/workflow files.
3. Read this index plus the relevant consolidated planning/design records.
4. Re-check any historical measurements or source assumptions the phase depends on.
5. Obtain remaining director decisions for that phase only.
6. Commit a fresh `state/prompt_forge_next_phase<N>.md` implementation contract before Fable starts.

Do not implement directly from the historical planning package merely because it is now locally available on `main`.