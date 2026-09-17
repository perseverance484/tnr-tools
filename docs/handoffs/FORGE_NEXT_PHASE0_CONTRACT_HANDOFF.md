# Forge Next Phase 0 — implementation-contract handoff

**Status:** FROZEN CONTRACT HANDOFF — READY FOR FABLE IMPLEMENTATION
**Date:** 2026-09-16
**Repository:** `perseverance484/tnr-tools`
**Contract author:** ChatGPT
**Implementation owner:** Fable / Claude Code
**Independent reviewer after implementation:** ChatGPT
**Contract branch:** `chatgpt/forge-next-unified-contract`
**Contract commit:** `f7c77a6a160347abd824402c77537ccf5864d4dd`
**Contract file:** `state/prompt_forge_next_phase0.md`
**Input-verification commit:** `90a76f90c93d2f01d449a7a10a471a08829c221f`
**Input-verification file:** `docs/reviews/FORGE_NEXT_FINAL_INPUT_VERIFICATION.md`
**Operational main observed when authored:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`
**Live-game requests/writes:** none

## Frozen upstream inputs

- reconciled planning: `claude/forge-next-planning-reconciled@ba51a28a99a7748e61de0c2768bd73ab9c65c856`
- accepted Quest Studio: `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`
- Quest Studio final review: `claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d`
- Quest Studio verdict: `APPROVE_WITH_NONBLOCKING_FOLLOWUP`

## Contract interpretation

Phase 0 starts from **fresh operational `main`**, not from this ChatGPT branch and not by merging either frozen input branch.

The contract preserves Fable's reviewed ForgeCore architecture and limits this implementation slice to the headless-core/measured-baseline work. Quest Studio remains a reviewed downstream integration input and is not merged in Phase 0.

`docs/reviews/FORGE_NEXT_FINAL_INPUT_VERIFICATION.md` records three stale statements in the frozen planning package that must not be inherited literally:

1. K-26's director credential-scope half is settled by `RUL-2026-09-16-002`: Contents write only, no Actions write, no Workflows write; source-push accepted.
2. `gen_evidence_summary.py` regenerates the parity prose summary, while the admin matrix receives verification metadata updates rather than a regenerated prose summary.
3. the accepted Quest Studio result includes and verifies `generated.manifestSha256`.

These are explicit evidence corrections, not a reopening of the approved architecture.

## Immediate next action

Fable should:

1. read `state/prompt_forge_next_phase0.md` at contract commit `f7c77a6a160347abd824402c77537ccf5864d4dd`;
2. verify fresh `main` and create a Fable-owned Phase-0 branch from it;
3. perform the baseline/drift measurements before implementation;
4. implement only Phase 0;
5. freeze an exact SHA with the required handoff;
6. return it for independent ChatGPT review.

No Phase 1, shell redesign, Quest Studio integration, Content Admin, Builder retirement, release movement or live-game action is authorized by this brief.
