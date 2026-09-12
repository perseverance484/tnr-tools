# Forge Next — UI Design Input Index

**Status:** WORKING INDEX — CHATGPT DESIGN/REVIEW LANE  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Purpose:** let Fable/reviewers consume the growing UI-design evidence without confusing authority levels

## 1. Read this first

This branch contains a mix of user-approved visual direction, user-directed corrections, product/workflow proposals, architecture-neutral UX/safety contracts, current-implementation audits, style-board analysis and transcript-recovery scaffolding. They are not equally authoritative.

Repository precedence remains governed by `docs/00_INDEX.md`. These files do not override doctrine, engine laws, source-derived contracts, the planning brief, or user-owned decisions.

## 2. Tier A — user-approved / user-directed inputs

### `FORGE_NEXT_VISUAL_DIRECTION.md`

**Use as:** approved visual/product north star.

Owns the broad character: professional TNR operations application, dark/atmospheric/premium, first-party-feeling, mobile-first, Command Center direction, content lanes, Content Admin presence, strong state visualization and controlled motion. Exact labels/layouts remain illustrative where the document says so.

### `FORGE_NEXT_COLOR_SEMANTICS.md`

**Use as:** binding principle that operation context and semantic outcome remain visually distinct.

The exact earlier reference palette may be superseded by a later transcript ruling; the meaning-separation rule remains durable.

### `FORGE_NEXT_QUEST_STUDIO.md`

**Use as:** director-set parent product contract for quest authoring.

Quest authoring is one **Quest Studio** with subtype/recipe adapters (Mission, Event, Story, Raid/Boss, Battle Pyramid, Daily and later audited types), not separate top-level Mission/Event mini-apps. It defines the browser-authoring + repository-worker + existing-Forge-runner architecture needed to eliminate routine chat/file relay while keeping repository scripts canonical and live execution user-controlled.

`RUL-2026-09-12-001` records this direction historically.

### `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`

**Use as:** director-set authority/boundary contract for Forge as a whole.

Forge is the human-facing translation/orchestration/presentation layer; `tnr-tools` remains the durable source of facts, contracts, profiles, evidence, scripts, validators and generated build artifacts. Forge may cache/generated-project repository knowledge for responsive editing, but it must not become a second canonical rules database. Canonical build/validation runs through approved typed repository operations, while live-game execution and publishing remain separate explicit user actions.

`RUL-2026-09-12-002` records this direction historically.

## 3. Tier B — planning/design/product proposals, not final implementation architecture

### `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`

**Use as:** proposed foundation/token/component language. Do not treat exact hex values, geometry, route model or operation taxonomy as final locks.

### `FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`

**Use as:** product/workflow expansion study for evolving Forge from a manifest runner into a one-stop TNR Content Studio/control plane.

It analyzes actual mission/quest, event, workstream, art and delivery workflows plus current game-source guide support, and proposes Project Workspace, Brief Intake, Quest/Encounter/Decision/Research/Art/Guide/Visual-Communication studios, Preview Lab, review/package/release flows, feedback and quality intelligence.

### `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`

**Use as:** architecture-neutral product contract for the human project/workstream control surface.

It specifies how Forge can project `roadmap.json` and durable sources into one project workspace covering attention/blockers, dependency-aware tasks, director decisions, content/assets, evidence, review packages, delivery artifacts, execution/readback and publication without creating a second canonical project database.

### `FORGE_NEXT_MISSION_STUDIO.md`

**Use as:** **Mission subtype detail contract**, subordinate to `FORGE_NEXT_QUEST_STUDIO.md` for parent product scope.

Its mission-profile/storyboard/encounter/scene/policy/decision/preview details remain useful. Its former open question about mission-specific vs shared Quest Studio is resolved: shared Quest Studio core with subtype adapters.

It also preserves the guardrail that the current four-node Forsworn flatten experiment must not become universal mission doctrine while that decision remains deferred pending player feedback.

### `FORGE_NEXT_STYLE_BOARD_INVENTORY.md`

**Use as:** objective inventory of the newest supplied visual board. Records what is visibly present, not what is approved.

### `FORGE_NEXT_DESIGN_RECONCILIATION_MATRIX.md`

**Use as:** delta map between repository design sources and the newest style board. Transcript-sensitive rows remain open until reconciled or re-ruled.

## 4. Tier C — architecture-neutral UX/safety contracts

These should survive changes in navigation, framework and exact styling.

- `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md` — required human meaning for machine state, especially SENT ambiguity, CONFIRMED vs VERIFIED, incomplete verification, auth/read failures, capture persistence and publication.
- `FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md` — phone/mobile/accessibility requirements and current-surface findings.
- `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md` — real workflows mapped to reusable UI responsibilities without choosing routes.
- `FORGE_NEXT_WIREFRAME_ANATOMY.md` — required content hierarchy for key flow states; not final layouts.
- `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md` — what major surfaces must help the user understand/do regardless of sitemap.
- `FORGE_NEXT_INTERACTION_RISK_MATRIX.md` — confirmation/friction/evidence requirements based on consequence and ambiguity.
- `FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md` — consistent human-facing terminology for lifecycle, verification, captures, auth, rate limits, recovery, sync and publication.
- `FORGE_NEXT_ICON_MOTION_SEMANTICS.md` — library/color-agnostic rules separating operation context, state/outcome, content identity and motion.
- `FORGE_NEXT_UX_SCENARIO_MATRIX.md` — adversarial unhappy/ambiguous/partial-success coverage for wireframes/tests.
- `FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md` — wireframe/visual/implementation review gate, not a capability source.

## 5. Tier D — current implementation evidence

### `FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`

**Use as:** before-state audit of Forge 0.4.0 at `main@305a28f992e33194fbba279a3f32e698dfb2b67f`.

## 6. Tier E — transcript recovery scaffolding

### `FORGE_NEXT_UI_CONTEXT_HANDOFF.md`

**Use as:** bridge between the predecessor max-length chat and replacement conversation. Do not treat it as independent canonical design once recovery is complete.

## 7. Recommended Fable reading order when token budget returns

1. planning brief / existing Fable package context;
2. `FORGE_NEXT_VISUAL_DIRECTION.md`;
3. `FORGE_NEXT_COLOR_SEMANTICS.md`;
4. this index;
5. `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` — authority/translation-layer boundary;
6. `FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`;
7. `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`;
8. `FORGE_NEXT_QUEST_STUDIO.md` — parent authoring/product + build-worker architecture;
9. `FORGE_NEXT_MISSION_STUDIO.md` only for Mission-subtype detail;
10. current UI baseline and safety-state contract;
11. screen/risk/copy/mobile contracts;
12. workflow/component + wireframe anatomy;
13. adversarial scenario and icon/motion contracts;
14. style-board inventory/reconciliation for visual-delta questions;
15. acceptance checklist during review.

Fable does not need to copy these documents into its branch. It may cite exact ChatGPT branch SHAs under the one-writer workflow.

## 8. Decisions these files deliberately do not make

The ChatGPT design lane has not settled:

- final top-level information architecture and destination names/order;
- final content-lane taxonomy;
- final operation-mode taxonomy, including whether `Review` is a mode or workflow category;
- final exact palette/tokens;
- final Content Admin permission/edit/review-state/publish-confirmation model;
- whether infographic/visual-communication becomes an official production lane;
- whether Guide Studio is a first-class Forge authoring surface;
- how much repository-backed project state Forge may edit directly;
- exact Quest Source schema/versioning;
- exact repository-worker trigger/auth/branch architecture;
- subtype rollout order beyond the director-set shared Quest Studio model;
- game-source changes;
- Builder retirement timing.

## 9. Conflict handling

If a Fable source finding conflicts with a ChatGPT proposal, source/contract evidence wins on what the system can truthfully do. Surface the UX consequence, preserve approved product character where possible, ask the director when multiple valid experiences remain, and never invent backend capability to satisfy a mockup.

If the predecessor transcript contains a later explicit director ruling that conflicts with an older proposal, make the later ruling durable in the appropriate owning design source and record historical supersession where required.

## 10. Current branch snapshot

The Quest Studio direction and repository-backed translation-layer architecture supersede the earlier Mission-Studio-as-parent framing. Use the branch head reported in the current handoff/chat when consuming these inputs; do not assume this index update remains the final planning SHA.