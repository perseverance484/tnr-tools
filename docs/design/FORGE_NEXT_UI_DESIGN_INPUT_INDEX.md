# Forge Next — UI Design Input Index

**Status:** WORKING INDEX — CHATGPT DESIGN/REVIEW LANE  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Purpose:** let Fable/reviewers consume the growing UI-design evidence without confusing authority levels

## 1. Read this first

This branch contains a mix of:

- user-approved visual direction;
- user-directed corrections;
- product/workflow expansion proposals;
- architecture-neutral design contracts;
- audits of the current implementation;
- analysis of the latest supplied style board;
- transcript-recovery scaffolding.

They are not all equally authoritative.

Repository precedence remains governed by `docs/00_INDEX.md`. These files do not override doctrine, engine laws, source-derived contracts, the planning brief, or user-owned decisions.

## 2. Tier A — user-approved / user-directed design inputs

### `FORGE_NEXT_VISUAL_DIRECTION.md`

**Use as:** approved visual/product north star.

Owns the broad character: professional TNR operations application, dark/atmospheric/premium, first-party-feeling, mobile-first, Command Center direction, content lanes, Content Admin presence, strong state visualization, controlled motion.

It explicitly distinguishes binding direction from illustrative mockup details.

### `FORGE_NEXT_COLOR_SEMANTICS.md`

**Use as:** binding principle that operation context and semantic outcome must remain visually distinct.

The exact earlier reference palette may be superseded by a later transcript ruling; the meaning-separation rule remains durable.

## 3. Tier B — planning/design/product proposals, not final architecture

### `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`

**Use as:** proposed foundation/token/component language.

Do not treat exact hex values, geometry, route model, or operation taxonomy as final implementation locks.

### `FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`

**Use as:** product/workflow expansion study for evolving Forge from a manifest runner into a one-stop TNR Content Studio/control plane.

It analyzes the repository's actual mission/quest, event, workstream, art and delivery workflows plus current game-source guide support, and proposes capability channels such as project/workstream workspace, Brief Intake, Mission/Quest Studio, Encounter/AI Studio, Decision Workbench, evidence/reuse library, Art Studio, Guide Studio, a distinct infographic/visual-communication lane, Preview Lab, review/package/release flows, post-launch feedback and quality intelligence.

It deliberately does **not** choose the final sitemap or implementation architecture. Fable should reconcile it against its source/audit package and phase plan.

### `FORGE_NEXT_STYLE_BOARD_INVENTORY.md`

**Use as:** objective inventory of the newest supplied visual board.

This file records what is visibly present, not what is approved. It is especially useful for identifying the board's Read/Write/Review/Publish/Recovery treatment and visual component vocabulary.

### `FORGE_NEXT_DESIGN_RECONCILIATION_MATRIX.md`

**Use as:** delta map between repository design sources and the newest style board.

Rows marked chronology/transcript-sensitive remain open until the predecessor-chat export is reconciled or the director rules them again.

## 4. Tier C — architecture-neutral UX/safety contracts

These are intended to survive changes in navigation, component framework, and exact styling.

### `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`

**Use as:** required human meaning for machine state.

Preserves distinctions such as SENT ambiguity, CONFIRMED vs VERIFIED, INCOMPLETE verification, auth vs read failure, capture persistence, and publication vs technical success.

### `FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md`

**Use as:** mobile/accessibility requirements and current-surface findings.

### `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md`

**Use as:** mapping from real workflows to reusable UI responsibilities without choosing final routes.

### `FORGE_NEXT_WIREFRAME_ANATOMY.md`

**Use as:** required content hierarchy for key flow states; not final layouts.

### `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`

**Use as:** what each major capability surface must help the user understand/do, regardless of final sitemap.

### `FORGE_NEXT_INTERACTION_RISK_MATRIX.md`

**Use as:** confirmation/friction/evidence requirements based on consequence and ambiguity.

### `FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md`

**Use as:** consistent human-facing terminology for consequence, lifecycle, verification, captures, auth, rate limits, recovery, repository sync, and publication.

### `FORGE_NEXT_ICON_MOTION_SEMANTICS.md`

**Use as:** library- and color-agnostic rules for keeping operation icons, outcome/state icons, content identity, and motion semantically distinct.

### `FORGE_NEXT_UX_SCENARIO_MATRIX.md`

**Use as:** adversarial design-state coverage. It enumerates the unhappy/ambiguous/partial-success scenarios that wireframes and later UI tests must be able to represent honestly.

### `FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md`

**Use as:** wireframe/visual/implementation review gate. It should not be used to invent capabilities.

## 5. Tier D — current implementation evidence

### `FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`

**Use as:** before-state audit of Forge 0.4.0 at `main@305a28f992e33194fbba279a3f32e698dfb2b67f`.

This file describes what the current UI actually exposes and where the redesign must preserve safety behavior while improving usability.

## 6. Tier E — transcript recovery scaffolding

### `FORGE_NEXT_UI_CONTEXT_HANDOFF.md`

**Use as:** bridge between the predecessor max-length chat and the replacement conversation.

It defines the transcript reconciliation buckets and records what is currently known versus chronology-sensitive.

Do not treat it as an independent canonical design spec once the recovery is complete; its purpose is to point to owning sources.

## 7. Recommended Fable reading order when token budget returns

1. planning brief / existing Fable package context;
2. `FORGE_NEXT_VISUAL_DIRECTION.md`;
3. `FORGE_NEXT_COLOR_SEMANTICS.md`;
4. this index;
5. `FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md` when reconciling product scope, authoring workflows and phase opportunities;
6. `FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`;
7. `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`;
8. `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`;
9. `FORGE_NEXT_INTERACTION_RISK_MATRIX.md`;
10. `FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md`;
11. `FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md`;
12. workflow/component + wireframe anatomy as needed;
13. `FORGE_NEXT_UX_SCENARIO_MATRIX.md` when checking state coverage;
14. `FORGE_NEXT_ICON_MOTION_SEMANTICS.md` when translating structure into visual behavior;
15. style-board inventory/reconciliation only for visual-delta questions;
16. acceptance checklist during review rather than as a source of architecture.

Fable does not need to copy these documents into its branch. It may cite exact ChatGPT branch SHAs as planning inputs under the one-writer workflow.

## 8. Decisions these files deliberately do not make

The ChatGPT design lane has not settled:

- final top-level information architecture;
- final destination names/order;
- final content-lane taxonomy;
- final operation-mode taxonomy;
- whether `Review` is a mode or workflow category;
- final exact palette/tokens;
- final Content Admin permission scope;
- final admin edit staging model;
- final approval-state storage;
- final publish confirmation level;
- whether infographic/visual-communication becomes an official production lane;
- whether Guide Studio is a first-class Forge authoring surface;
- how much repository-backed project state Forge may edit directly;
- game-source changes;
- Builder retirement timing.

These remain with the planning/source deep dive and/or director.

## 9. Conflict handling

If a Fable source finding conflicts with a ChatGPT design proposal:

- source/contract evidence wins on what the system can truthfully do;
- surface the practical UX consequence;
- preserve the approved visual/product character where possible;
- ask the director when multiple valid product experiences remain;
- do not silently invent backend capability to satisfy a mockup.

If the predecessor transcript contains a later explicit director ruling that conflicts with an older design proposal, make the later ruling durable in the appropriate owning design source and record historical supersession where required.

## 10. Current branch snapshot

This index now includes the Content Studio expansion study in addition to the waiting-period design, adversarial UX-scenario and icon/motion-semantics artifacts. Use the branch head reported in the handoff/chat when consuming these inputs; do not assume this file's update commit remains the final planning SHA.