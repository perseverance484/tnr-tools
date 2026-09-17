# Forge Next — final branch cleanup record

**Status:** APPROVED CLEANUP PLAN — execute after this consolidation branch is integrated to `main`  
**Date:** 2026-09-17  
**Director approval:** K-06, K-17, and the selective repository-consolidation plan approved in chat on 2026-09-17  
**Canonical rationale:** `RUL-2026-09-17-003`

This file turns `docs/reviews/FORGE_NEXT_BRANCH_CONSOLIDATION_AUDIT.md` into an execution list. Branch deletion is ref cleanup, not a merge operation.

## Keep

Keep these branches after the consolidation lands:

- `chatgpt/forge-next-phase1-brief` — until the Phase 1 brief/consolidation commit is integrated and Fable has started from the integrated brief; then this branch may also be deleted.
- `chatgpt/forge-quest-studio-foundation` — retain as the accepted, independently reviewed Phase-S implementation source at `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` until Quest Studio is deliberately reconciled/integrated.

## Delete after consolidation integration

Forge Next planning / Phase 0 refs:

- `chatgpt/forge-next-planning`
- `chatgpt/forge-next-planning-workspace-temp`
- `chatgpt/forge-next-planning-workspace-temp2`
- `chatgpt/forge-next-unified-contract`
- `chatgpt/review-forge-next-phase0`
- `chatgpt/review-forge-next-phase0-final`
- `chatgpt/review-forge-next-phase0-integration`
- `chatgpt/review-forge-next-planning`
- `chatgpt/review-forge-next-planning-r2`
- `claude/forge-next-planning-v3frzi`
- `claude/forge-next-planning-reconciled`
- `fable/forge-next-phase0`

Quest Studio superseded/review refs:

- `chatgpt/forge-quest-studio-final-fix` — redundant accepted-tree alias
- `chatgpt/forge-quest-studio-source-push-temp`
- `chatgpt/forge-quest-studio-source-push-temp2`
- `chatgpt/forge-quest-studio-source-push-work`
- `claude/forge-quest-studio-audit-j4jhcf`
- `claude/quest-studio-source-push-review`
- `claude/quest-studio-final-review`

Do not delete `chatgpt/forge-quest-studio-foundation` in this pass.

## Preconditions before deletion

1. This consolidation branch is integrated to current `main`.
2. `docs/forge_next/README.md`, the selected planning/design records, the reconciled rulings ledger, final Phase 0 clearance and final Quest Studio review are present on `main`.
3. Phase 1's frozen brief is present on `main` at `state/prompt_forge_next_phase1.md`.
4. `chatgpt/forge-quest-studio-foundation` still resolves to accepted SHA `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`.
5. No active review or implementation session is still using one of the refs scheduled for deletion as its mutable workspace.

## Method

Delete branch refs through GitHub's Branches UI or another environment with explicit ref-deletion capability. Do not merge a branch merely to make it deletable. Do not force-update `main`.

Deleting a branch ref does not erase the exact commits cited in the consolidated documents; those SHAs remain historical evidence. If a future audit needs an omitted large planning matrix, retrieve it by the frozen planning SHA rather than restoring the branch as a second active authority.

## After deletion

The expected Forge program branch surface is deliberately small:

- `main` — current operational authority;
- one active `fable/forge-next-phase1` implementation branch once Fable starts;
- one ChatGPT review branch only when Phase 1 review is active;
- `chatgpt/forge-quest-studio-foundation` retained until Phase S integration.

Future phase branches should be created and retired under `docs/DEVELOPMENT_WORKFLOW.md` rather than accumulating indefinitely.