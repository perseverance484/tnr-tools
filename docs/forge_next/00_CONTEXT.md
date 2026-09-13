# 00. Context, evidence base and method

**Status:** PLANNING PACKAGE, no implementation.
**Brief:** `state/prompt_forge_next_planning.md` at `chatgpt/forge-next-planning@70c151616f09c6ec729cb05afb30faa2c6331183`.
**Mid-pass amendment (user-approved visual north star):** `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` at `chatgpt/forge-next-planning@0bb5a54b1025ba49ff6b09aa9606f23102f4dca3`, plus the approved concept mockup supplied as an attachment (a compressed copy is committed as `docs/forge_next/design/forge_next_concept_mockup.jpg` for durability). It was read as a new planning input on the existing branch; the ChatGPT branch was neither merged nor rebased onto. Its section 12 governs what is binding (product character, shell, Command Center, lanes, Content Admin presence, state visualization) and what is illustrative (labels, destinations, lane names, colours, geometry); section D reconciles every mockup element with the capability evidence and section D.7 lists the departures recommended and why.
**Planning branch:** `claude/forge-next-planning-v3frzi` (the branch assigned to this session; `docs/DEVELOPMENT_WORKFLOW.md` §3 names `fable/*` as the normal Fable prefix, so this is a stated deviation, not a new convention).
**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`, verified with `git fetch origin main` at the start of the pass.
**Lane:** A. Planning owner Fable / Claude Code; independent reviewer ChatGPT (Release Auditor with UI/UX Reviewer and Engineering Auditor lenses).

**Second mid-pass amendment (director rulings and consolidated design lane):** `chatgpt/forge-quest-studio-foundation@824c4d58075d0265c717ef25c02485614f3096cf`, consumed read-only (exported into the session scratchpad; neither merged nor rebased, nothing on that branch modified). It carries `RUL-2026-09-12-001` (one shared Quest Studio with subtype adapters; Mission is a subtype, not a parent product) and `RUL-2026-09-12-002` (Forge is the human translation, orchestration and presentation layer over the repository, which stays the durable source of facts, contracts, profiles, scripts, validators, provenance and generated artifacts), their canonical owners `docs/design/FORGE_NEXT_QUEST_STUDIO.md` and `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, the routing index `docs/design/FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md` (authority tiers A to E), the Tier C architecture-neutral UX and safety contracts, the Tier B product proposals (`FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`, `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`, `FORGE_NEXT_MISSION_STUDIO.md` as Mission-subtype detail, `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`), the continuation brief `state/prompt_forge_next_planning_resume_after_ui_recovery.md`, and a ChatGPT-owned Quest Studio foundation implementation under `state/prompt_forge_quest_studio_foundation.md` (Quest Source → request branch → GitHub Actions worker → `quest_compile.py` → build-result → Forge seam, Mission as the first adapter). That implementation is treated here as architecture and roadmap evidence only; it is not a frozen review target and this package does not duplicate or patch it. Its `main` remains `305a28f` (re-verified with `git fetch origin main` when the amendment arrived). Decisions the director still keeps open after these rulings are listed in `K_USER_DECISIONS.md` §K.0.

**Header note (provenance).** The ChatGPT design files and the resume brief still carry the branch name `chatgpt/forge-next-planning` in their headers; the exact snapshot consumed here is `824c4d58` on `chatgpt/forge-quest-studio-foundation`, which contains the older branch's `e0081afa` history. Reviewers should not look for these files on the older branch. The SHA, not the branch name, is the audit target (`CLAUDE.md` §11).

**Transcript status.** At `824c4d58` the predecessor-transcript reconciliation is still pending (`docs/design/FORGE_NEXT_UI_CONTEXT_HANDOFF.md` header: TRANSCRIPT RECONCILIATION PENDING; no filled recovered-state section). Every style-board delta therefore stays a labelled director question (K-20 to K-24, K-30, K-32, K-33 and the wording half of K-12); this package does not read the style board as a later ruling.

**Code cites.** Every `forge/src` line cite in this package is taken at `main@305a28f`. The planning branch changes no file under `forge/`, `skills/`, `state/`, `docs/design/` or `.github/` (verified with `git diff --quiet 305a28f..HEAD` on those paths at each amendment and again before the freeze). Files that exist only on the ChatGPT branch are cited with the prefix `824c4d58:`.

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
2. **Orchestrated deep dive** (`forge-next-deep-dive` workflow): twelve parallel readers over Builder, Forge, the game source at head and both pins, repository consumers (`harvest.py`, `build_answers.py`, `content_workstream.py`, `validate.py`, workflows), the Forge test suite and CI, the current UI, and every committed results bundle and manifest. Two merge agents built the Builder→Forge parity matrix and the Content Admin feasibility matrix. Adversarial verification covers the rows where a wrong cell would change a conclusion the package rests on: every `GAP`, every `INTENTIONAL DIFFERENCE`, every retirement blocker, every row the merge marked low or medium confidence, and every Content Admin row. One verifier per row re-opens every cited location with instructions to default to a correction unless the source says exactly what the row claims. Each verifier returned `CONFIRMED`, `CORRECTED`, `REFUTED` or `UNVERIFIABLE`, and a corrected row replaced the original. Rows outside that set are labelled `not verified` in the matrix and in `B_PARITY_MATRIX.md`, never presented as audited. How far that pass had got at the frozen SHA is stated in `B_PARITY_MATRIX.md` §B.1 and `E_CONTENT_ADMIN_FEASIBILITY.md` §E.1, and those two statements, not this paragraph, are what a reviewer should rely on. The matrices are committed as `evidence/parity-matrix.json` and `evidence/admin-feasibility.json`; `B_PARITY_MATRIX.md` §B.1 and `E_CONTENT_ADMIN_FEASIBILITY.md` §E.1 state the verification status that holds at the frozen SHA, which is the status a reviewer should read before relying on a row.
3. **Design panel** (`forge-next-design-panel` workflow): independent proposals for the information architecture, visual direction and architecture alternatives, scored by independent judges against the brief's criteria and the verified evidence; the recommendation in sections D and F is synthesized from the winner with grafted ideas from runners-up, and the alternatives are kept so the user can choose.
4. **Completeness critic**: a final pass compared the package against brief sections 3 to 17 and the findings were folded in.
5. Baseline gates run in this session, read-only, all from the repository's own scripts: `cd forge && npm test` (293 tests, 292 pass, 1 fail: `release loader: exactly one @x-release-pending marker`, see `A_ARCHITECTURE_MAP.md` §A.10), `skills/building-tnr-content/scripts/doctrinemap.py` (exit 0; 21 assertions, 18 referenced, 16 surfaces, 0 errors, 0 warnings), `render_doctrine.py --check` (exit 0, all projections current), `build_packs.py --check` (exit 0, all packs and TOCs current) and `lawmap.py` (exit 0; 93 laws, 93 matrix rows, 77 citations across 35 files, 0 errors, 5 warnings). No gate was piped in a way that masks its exit code, and this package changes no file those gates own. Studio seam measurements were taken in read-only overlays of `main` plus the exported `824c4d58` files (no branch file modified, zero live requests): `quest_compile.py --selftest` 9/9; `quest_compile_integration_test.py` PASS; Forge overlay suite 305/305 (the branch relaxes the red release-loader assertion); bundle +39,621 B (+10.0%) unminified; committed-bundle equality unverified because the branch bundle was not exported.
6. **UI-contract reading** (`forge-next-consolidated-inputs` workflow): the ten Tier C contracts (`FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`, `FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md`, `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md`, `FORGE_NEXT_WIREFRAME_ANATOMY.md`, `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`, `FORGE_NEXT_INTERACTION_RISK_MATRIX.md`, `FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md`, `FORGE_NEXT_ICON_MOTION_SEMANTICS.md`, `FORGE_NEXT_UX_SCENARIO_MATRIX.md`, `FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md`) plus the Tier A colour-semantics amendment and the visual direction's state rules were read row by row (166 requirement rows, 25 component rows, 35 machine-state rows mapped to `forge/src`, 72 adversarial scenarios), alongside the Tier A/B product documents, the Tier D baseline audit against the code, and the foundation implementation. The resulting reconciliation plan (85 package updates, a corrected decision register, 9 roadmap implications, the resume brief's §7 cross-checks and 24 conflicts) was applied to this package, and the §7 cross-checks are confirmed in the handoff before the SHA is frozen.
7. **Authority handling** follows the routing index (`docs/design/FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md` §2 to §6): Tier A (Quest Studio, repository-backed architecture, colour semantics, visual direction) binding; Tier B (`FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`, `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`, `FORGE_NEXT_MISSION_STUDIO.md` as subtype detail, `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`) proposals reconciled by sections F and G and never inherited as an approved order; Tier C architecture-neutral requirements; Tier D before-state; Tier E scaffolding discarded once recovery lands.

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
docs/forge_next/D_IA_AND_JOURNEYS.md    information architecture, journeys, mockup reconciliation
docs/forge_next/D_VISUAL_SYSTEM.md      the approved visual direction elaborated into tokens, components and state rules
docs/forge_next/E_CONTENT_ADMIN_FEASIBILITY.md  per-class source audit, zero-game-change scope
docs/forge_next/F_ARCHITECTURE_RECOMMENDATION.md  preserve / replace / abstract / migrate
docs/forge_next/G_ROADMAP.md            phased Lane A roadmap with gates
docs/forge_next/H_RISK_REGISTER.md
docs/forge_next/I_TEST_STRATEGY.md
docs/forge_next/J_MIGRATION_AND_RETIREMENT.md
docs/forge_next/K_USER_DECISIONS.md     open user-decision register
docs/forge_next/evidence/*.json         verified matrices, registry gap, drift, harvest evidence
docs/forge_next/wireframes/*.html       sixteen static wireframes (phone and desktop in one page), with src/ (generator) and review/ (rendered captures)
docs/forge_next/design/                 the approved concept mockup and its provenance pointer
docs/handoffs/FORGE_NEXT_PLANNING_HANDOFF.md  section-17 handoff for independent review
```

Files marked (forthcoming) in any section are not committed at the cited SHA. A matrix or evidence file cited by A, H or K but absent from `evidence/` is not evidence until it lands; the handoff lists only committed artifacts and names anything still forthcoming.
