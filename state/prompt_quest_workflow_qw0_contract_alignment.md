# Fable brief — QW-0A: source-contract and validator alignment

**Status:** DIRECTOR-APPROVED IMPLEMENTATION-PLANNING PASS (2026-10-12; RUL-2026-10-12-016). Ready for Fable to start a bounded Lane A investigation/correction branch; *no auto-adoption* of source drift.  
**Repository:** perseverance484/tnr-tools  
**Design source:** `docs/design/QUEST_CREATION_WORKFLOW_IMPROVEMENT_PLAN_2026-10-12.md`, QW-0; approved design branch `chatgpt/quest-workflow-skyglass-retrospective-20261012` (freeze the exact source SHA at handoff).  
**Baseline at planning:** main@4de2668bb947368113683b5cb97e197abc87df27; reverify fresh `main` and all pins before implementation.  
**Implementation owner:** Fable / Claude Code, one new `fable/*` branch. **Independent reviewer:** ChatGPT at the frozen SHA.  
**Live game:** ZERO requests / ZERO writes. No credentials, no publication, no operator-side execution.

## Outcome

Make the repository's canonical content validation and Forge preflight agree with an *explicitly audited* pinned game-source contract for post-0056 items, effects, AI creates and rewards, without changing gameplay rules or generalizing the release-specific Ghost Ship exception. Keep existing legacy manifest and source-contract compatibility observable.

This brief is **the first, narrower slice of QW-0**. Version-label correction, new crafting-relation capture, spent-manifest archival and the Ghost Ship historical after-capture audit are **separate follow-ups**. Do not mix them into this change.

## Required reconstruction and evidence

1. Verify live refs. Read `CLAUDE.md`, `CHATGPT.md`, `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md` as routed, `docs/DEVELOPMENT_WORKFLOW.md`, this brief, the approved workflow plan and `docs/RULINGS.md` RUL-2026-10-12-013 through -016.
2. Read `state/active-context.md` and `state/status.json` but do **not** rewrite their September Forge checkpoint. The Ghost Ship release outcome is `docs/handoffs/GHOST_SHIP_SKYGLASS_RELEASE_MANIFEST_HANDOFF.md` `8.
3. Inspect repository owners and consumers:
   - `skills/building-tnr-content/data/45c_DATA_constructors.json`, `45d_DATA_entity_schemas.json`, `45e_DATA_constants.json`, `45f_DATA_procedures.json`, `45g_DATA_checks.json` and `45h_DATA_lints.json`;
   - `skills/building-tnr-content/scripts/schema_extract.py`, `schema_diff.py`, `validate.py`, `factory.py` and related selftests;
   - `forge/src/runner/{validate,lints}.mjs`, `forge/src/runner/fields.json`, `forge/test/post0056.test.mjs`, `forge/tools/check_manifest.mjs` and bundle/fixture tests;
   - `state/ghost_ship_skyglass_release_validate_exception.json` and the release's three SHA-scoped exception gates.
4. Pin and compare source evidence: release-tested `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`; latest *signal-only* sentinel at `6e4429d65f466b0df9fca3f9917b6dd427df7573` recorded by `state/schema_sentinel.json` / `docs/DRIFT.md`. Verify actual current upstream HEAD separately. **No assumption that any of these equals deployed production.** State which pin is suitable for the intended bounded correction, which remains unverified and why.

## Implementation boundary

**QW-0A can implement narrowly proven validator / contract fixes when the existing mechanical adoption gates allow them**; it may also return a stop/report if adopting the source would violate those gates. It must not silently expand into a general latest-upstream migration.

- Reproduce the legacy validator output against historical `push/90_ghost_ship_skyglass_release.json` and its SHA-specific approved exception. Classify each historical error by genuine source mismatch, intended director waiver, stale catalog or deliberate compatibility rule. **Historical exception ledgers remain byte-for-byte preserved.**
- Run `schema_extract.py <source> --ctors` **first** in scratch; then `schema_diff.py --invariants NEW_45c --constants 45e` and `schema_diff.py diff OLD NEW` per generated file. Record field, enum, type and nullability changes, provenance and the exact gate result.
- **Fail closed** on enum/field removals, type drift or a source conflict not deliberately resolved through the repository's existing adoption process. Do not lower or bypass `schema_diff.py` barriers, hand-edit generated output, or copy source-only metadata into a new authoritative file.
- If gates permit adoption of the bounded pin: regenerate owning generated contracts; update only proven validator/factory/Forge parity semantics as needed, then add regression fixtures for post-0056 item required columns, AI `preferredStat` removal and full-create fields, effect/tag normalization, current reward/consumable fields and nullability. Preserve the older storable shapes that must remain valid for staged legacy work unless a separately reviewed compatibility change is justified.
- If gates fail: produce a source/contract mismatch report with reproducible commands, exact diff classes and the smallest viable follow-up; **do not** claim the canonical validator is fixed or delete the current exception gates.
- Do not broaden `skipPreflight`, invent a general release exception, change the game engine or choose gameplay/balance/reward values. Any unexpected shared law/doctrine change is reported for separate ruling/reconciliation.

## Tests and acceptance evidence

- Existing source extraction and adoption checks, showing positive and negative cases; no suppressing a nonzero exit.
- Canonical `validate.py` for newly supported fixture payloads from the chosen pin; matching Forge `check_manifest.mjs` result and checks/lint parity. For historical `push/90` / `push/93` / `push/94`, verify that approved immutable exception validation continues to hold at the historical source/manifest hashes. If a new validator intentionally changes diagnostic output, **do not rewrite a historical exception**; report that its original gate no longer applies to the new validator and provide a separate compatibility disposition.
- Task-specific factory selftests, `forge/test/post0056.test.mjs`, relevant Forge suite and reproducible bundle/build, budget/release-pin checks if Forge implementation changes; `build_packs.py --check` and `lawmap.py` / `doctrinemap.py` as their code/document owners require.
- Negative tests: old fields rejected when source proves removal; unsupported effect/enum rejected; schema diff fails on intentional deletions; no silent partial acceptance; no invalid historical manifest treated as runnable just because it has an exception.
- Evidence must distinguish source-verified, test-proven, inferred and deployment-unverified claims. All tests/fixtures socket-free; no live-game or CDN contact.

## Deliverables and handoff

- One Fable-owned frozen branch/commit with narrowly scoped changes and a concise report under `docs/reviews/` or `docs/handoffs/`, including the source-selection and adoption ledger.
- Exact base, merge-base, head SHA, affected files, pinned source revisions, generated-file hash/provenance, commands/exit codes, changed behavior, compatibility debt, residual blockers and a clear verdict: `ALIGNED` or `BLOCKED_BY_SOURCE_ADOPTION`.
- ChatGPT independent exact-SHA review before integration. Reverify `main` immediately before merge. No next QW pass begins automatically.

**Explicitly not begun:** QW-0B Forge version fix, crafting-relation capture, spent-manifest archive/audit, QW-1 project starter, QW-2/3/4/5, Quest Studio integration, game changes, live reads/writes or publication.
