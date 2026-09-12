# 00. Context, evidence base and method

**Status:** PLANNING PACKAGE, no implementation.
**Brief:** `state/prompt_forge_next_planning.md` at `chatgpt/forge-next-planning@70c151616f09c6ec729cb05afb30faa2c6331183`.
**Planning branch:** `claude/forge-next-planning-v3frzi` (the branch assigned to this session; `docs/DEVELOPMENT_WORKFLOW.md` §3 names `fable/*` as the normal Fable prefix, so this is a stated deviation, not a new convention).
**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`, verified with `git fetch origin main` at the start of the pass.
**Lane:** A. Planning owner Fable / Claude Code; independent reviewer ChatGPT (Release Auditor with UI/UX Reviewer and Engineering Auditor lenses).

## 00.1 Boot sequence performed

Read from the live checkout, not from memory, in this order: `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `CLAUDE.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/agents/UI_UX_REVIEWER.md`, `docs/agents/ENGINEERING_AUDITOR.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md`, `docs/workflows/FABLE_REVIEW.md`, `docs/workflows/DIRECTOR_DECISIONS.md`, `docs/workflows/CONTENT_WORKSTREAM.md`, `docs/DOCTRINE.md`, `docs/10_LAWS_core.md` (head), `docs/PLAN_2026-09-03_builder_app.md`, `docs/BUILDER_APP_NOTES.md`, `docs/handoffs/BUILDER_APP_READINESS_HANDOFF.md`, `docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md`, `docs/reviews/REPO_SIMPLIFICATION_AUDIT.md`, `docs/DRIFT.md`, `docs/HANDOFF_INVENTORY.md`, `state/prompt_forge_full_capture.md`, `state/prompt_forge_protected_auth.md`, `state/prompt_builder_app_build.md`, `state/one_perfect_crop_content_admin_open.md`, `state/workstreams/INDEX.md` and `one_perfect_crop/roadmap.json`, `skills/building-tnr-content/SKILL.md` and `references/pipeline.md`, `push/README.md` and every manifest under `push/`, `reports/code_audit_2026-09-02.json`, all seven `.github/workflows/*.yml`, `.github/scripts/pin_release.py`, both loaders, every module under `forge/src/`, `forge/build.mjs`, `forge/package.json`, the test file inventory under `forge/test/`, and `builder_bundle.js`.

Current operational state (for orientation only, this pass changes none of it): mission flatten `push/46` shipped and awaiting the user's tap; law-provenance reconciliation not begun; One Perfect Crop workstream active with the content-admin director packet `admin.balance_and_eligibility` READY and `art.intake_accepted_assets` BLOCKED.

## 00.2 Source pins inspected

All game-source reading was done on read-only clones of the public repository `studie-tech/TheNinjaRPG` in the session scratchpad. Nothing was executed from any checkout; no request was made to any game host.

| Role | Commit | Notes |
|---|---|---|
| Current upstream head | `36c5873b7b6ee5fd3af717008d7c51b0f185b756` (2026-09-12 16:03 +0200) | 81 commits after the Forge pin, 170 after the task pin |
| Forge global pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` | every Forge engine fact, `fields.json`, `nested.json`, the procedure registry |
| Protected-auth task pin | `bdec2883748f029a0ecb93505adfdcbae6851fe9` | `state/prompt_forge_protected_auth.md`; auth table proven identical to the global pin (`docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md`) |
| Generated `45c/45d/45e/45f/45g` provenance | `bdec2883` | reconciled by `docs/reviews/REPO_SIMPLIFICATION_AUDIT.md`; older than the Forge pin |
| Sentinel drift signal | `98d0eca5c2e922f3b41e56120f096c072645c1f0` | `docs/DRIFT.md` 2026-09-11: 45d item farm fields and quest `requiredFarmingLevel` now required; guide constants added |
| Last Forge relevance check | game `main@62af1b3405b10183b31f838c9a5f131d790460f1` | 2026-09-09, `docs/BUILDER_APP_NOTES.md` |

Repository release state: `forge_loader_user.js` 0.4.0 and `builder_loader_user.js` 4.32 both `@require` `ce603def204f585d23837121b86cfdd9fd4c308c` via jsDelivr (auto commit `d1dbecc`).

## 00.3 Method

1. **Firsthand reading** of every Forge module and the Builder bundle by the planning owner (section A is written from that reading).
2. **Orchestrated deep dive** (`forge-next-deep-dive` workflow): twelve parallel readers over Builder, Forge, the game source at head and both pins, repository consumers (`harvest.py`, `build_answers.py`, `content_workstream.py`, `validate.py`, workflows), the Forge test suite and CI, the current UI, and every committed results bundle and manifest. Two merge agents built the Builder→Forge parity matrix and the Content Admin feasibility matrix. One adversarial verifier per matrix row re-read every cited location and returned `CONFIRMED`, `CORRECTED`, `REFUTED` or `UNVERIFIABLE`; corrected rows replaced the originals. The verified matrices are committed as `evidence/parity-matrix.json` and `evidence/admin-feasibility.json`; the verdict tallies are recorded in `B_PARITY_MATRIX.md` and `E_CONTENT_ADMIN_FEASIBILITY.md`.
3. **Design panel** (`forge-next-design-panel` workflow): independent proposals for the information architecture, visual direction and architecture alternatives, scored by independent judges against the brief's criteria and the verified evidence; the recommendation in sections D and F is synthesized from the winner with grafted ideas from runners-up, and the alternatives are kept so the user can choose.
4. **Completeness critic**: a final pass compared the package against brief sections 3 to 17 and the findings were folded in.
5. Baseline gates run in this session, read-only: `cd forge && npm test` (293 tests, 292 pass, 1 fail; see `A_ARCHITECTURE_MAP.md` §A.10), `doctrinemap.py` (0 errors), and the doctrine/pack `--check` gates at handoff.

Evidence tiers follow `docs/00_INDEX.md`: Source-verified, Behaviour-proven, Observed, Inferred, Assumed. Every matrix row carries its tier and citations; where a claim could only be settled in a real browser or live session it is marked Inferred or Unverified and listed in the handoff.

## 00.4 Constraints honoured (brief §16)

No Forge production implementation, no Builder deletion or deprecation, no live game requests, no live game writes, no use or request or export of session cookies or credentials, no TheNinjaRPG code changes, no release-pin movement, no manifest contract migration, no doctrine or law change, no publishing or live content change. The throwaway minified bundle measured for §A.9 was written to the session scratchpad only and is not committed.

## 00.5 Package layout

```
docs/PLAN_2026-09-12_forge_next.md      entry point: executive summary, roadmap headline, handoff pointer
docs/forge_next/00_CONTEXT.md           this file
docs/forge_next/A_ARCHITECTURE_MAP.md   current-state architecture (Forge and Builder)
docs/forge_next/B_PARITY_MATRIX.md      Builder → Forge parity and retirement gates
docs/forge_next/C_WORKFLOW_INVENTORY.md real content workflows Forge must support
docs/forge_next/D_IA_AND_JOURNEYS.md    information architecture, journeys, visual directions
docs/forge_next/E_CONTENT_ADMIN_FEASIBILITY.md  per-class source audit, zero-game-change scope
docs/forge_next/F_ARCHITECTURE_RECOMMENDATION.md  preserve / replace / abstract / migrate
docs/forge_next/G_ROADMAP.md            phased Lane A roadmap with gates
docs/forge_next/H_RISK_REGISTER.md
docs/forge_next/I_TEST_STRATEGY.md
docs/forge_next/J_MIGRATION_AND_RETIREMENT.md
docs/forge_next/K_USER_DECISIONS.md     open user-decision register
docs/forge_next/evidence/*.json         verified matrices, registry gap, drift, harvest evidence
docs/forge_next/wireframes/*.html       static wireframes (mobile + desktop) and visual concepts
docs/handoffs/FORGE_NEXT_PLANNING_HANDOFF.md  section-17 handoff for independent review
```
