# Fable continuation brief — Forge Next planning after UI-context recovery

**Status:** PLANNING CONTINUATION ADDENDUM — NO IMPLEMENTATION  
**Date:** 2026-09-12  
**Repository:** `perseverance484/tnr-tools`  
**Existing Fable planning branch:** `claude/forge-next-planning-v3frzi`  
**Verified Fable head before this addendum:** `eab1f9bd80694117407700d7caf705dc6c3020cd`  
**Shared baseline still verified:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lane:** A planning/discovery only  
**Implementation:** not authorized by this addendum

## 1. Why this addendum exists

Fable's Forge Next planning pass is already active and has begun producing the planning package under `docs/forge_next/`.

The predecessor ChatGPT UI-design conversation then reached the chat-length limit. While its export is pending, ChatGPT reconstructed the durable visual/design state and completed a set of architecture-neutral UI audits. These are new planning inputs that should inform the remaining Fable planning work without restarting the pass or merging the ChatGPT branch.

Continue the existing planning branch. Do **not** start over, do not implement production Forge UI, and do not modify the ChatGPT branch.

## 2. Read the exact ChatGPT snapshot supplied by the user

The user will give you an exact `chatgpt/forge-next-planning` SHA containing this addendum and the following files. Read them at that exact SHA; do not merge/rebase the branch merely to consume design evidence.

Required new inputs:

- `docs/design/FORGE_NEXT_UI_CONTEXT_HANDOFF.md`
- `docs/design/FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`
- `docs/design/FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`
- `docs/design/FORGE_NEXT_STYLE_BOARD_INVENTORY.md`
- `docs/design/FORGE_NEXT_DESIGN_RECONCILIATION_MATRIX.md`
- `docs/design/FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md`
- `docs/design/FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md`

Continue to treat these earlier sources as governing inputs where they own the decision:

- `state/prompt_forge_next_planning.md`
- `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md`
- `docs/design/FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`
- `docs/design/FORGE_NEXT_COLOR_SEMANTICS.md`

## 3. What is now stable enough to use

The new UI audit/reconciliation work confirms that planning may safely rely on these points without waiting for the predecessor transcript:

- Forge Next remains a professional, dark, atmospheric, TNR-specific operations product.
- Desktop persistent shell + Command Center direction remains approved.
- Mobile must have a deliberate phone navigation treatment rather than a collapsed desktop rail.
- Content lanes remain an approved human-facing entry principle, though final taxonomy remains open.
- Content Admin remains first-class but conceptually distinct from content execution.
- Operation context and semantic outcome must be separate visual/state systems.
- Read-only, mutation, publishing and recovery consequence must be legible before technical detail.
- `SENT`, `CONFIRMED`, `VERIFIED`, `INCOMPLETE`, orphan/recovery, auth refusal and full-capture persistence remain distinct semantic states.
- Recovery is a first-class UX, not a generic error/retry path.
- Current Forge 0.4.0 mobile safety characteristics (44px touch baseline, no hover dependency, scoped overlay) are the minimum floor, not expendable legacy behavior.
- Architecture-neutral component responsibilities are now mapped in `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md` and may be used when refining journeys/wireframes.

## 4. What must remain open pending transcript reconciliation

Do not silently settle these because the latest style board may represent a later chat decision whose chronology is not yet reconstructed:

1. exact operation-mode taxonomy, especially whether `Review` is a first-class mode;
2. exact operation-mode color mapping;
3. exact desktop destination list;
4. exact mobile destination list;
5. exact token/hex values where the style board differs from earlier proposals;
6. exact typography scale where the latest board tightens/changes v0.1;
7. exact content-lane taxonomy;
8. whether semantic `Success` / `Warning` buttons are actual production variants;
9. exact deployment/publish confirmation treatment;
10. any late predecessor-chat Content Admin or publish UX ruling not yet durable.

You may keep/recommend options for these in the planning package, but label them as pending transcript/director confirmation rather than treating the latest image alone as approval.

## 5. Continue the evidence/research track now

The missing transcript does **not** block the technical/product evidence work. Continue and complete, as applicable:

- current architecture map;
- Builder → Forge parity and objective retirement gates;
- real workflow inventory;
- Content Admin source/API/role/publish/preview feasibility;
- current-vs-pinned source drift implications;
- architecture recommendation;
- capture classification/persistence architecture;
- GitHub/repository bridge considerations;
- risk register;
- test/verification strategy;
- migration/Builder retirement plan;
- phased Lane A roadmap.

The new ChatGPT workflow/component map should be used to check that the technical roadmap can support the UI state model without forcing the UI to lie about execution/recovery semantics.

## 6. Reconcile your existing planning package, do not rewrite blindly

At `eab1f9bd...`, the branch already records:

- `docs/forge_next/00_CONTEXT.md`
- `docs/forge_next/A_ARCHITECTURE_MAP.md`
- `docs/forge_next/H_RISK_REGISTER.md`
- `docs/forge_next/K_USER_DECISIONS.md`
- visual reference files

Your own context file also describes additional planned sections/evidence that may exist locally or be forthcoming.

When incorporating these new UI inputs:

- preserve your source-verified architecture/capability evidence;
- update only the design/journey/risk/decision claims affected by the new inputs;
- do not downgrade a source-backed limitation merely because the style board depicts a capability;
- do not duplicate the ChatGPT safety-state contract into multiple planning files; point to it and translate its consequences into the relevant journey/roadmap acceptance gates;
- keep exact design choices visibly user-owned where still open.

## 7. Specific cross-checks requested

Before freezing the planning handoff, explicitly confirm:

### Safety/state model

Your proposed IA/wireframes can represent, without semantic loss:

- `SENT` ambiguity;
- `CONFIRMED` but verification pending;
- `INCOMPLETE` read-back owed;
- orphan candidate/adopt/skip/re-send decisions;
- auth checking/refused/unauthorized distinctions where source permits;
- full-capture read success versus body persistence;
- rate-limit pause;
- game result versus repository sync result;
- publication state distinct from technical success.

### Mobile

Your recommended shell/journeys can satisfy the requirements in `FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md`, especially:

- no horizontal primary-nav dependency;
- persistent/recoverable operation consequence during long flows;
- 44px minimum ordinary targets and appropriate primary-action sizing;
- sticky UI not covering warnings;
- high-risk recovery alternatives separated;
- technical detail progressively disclosed rather than miniaturized.

### Components

Check whether the architecture supports reusable equivalents of the component responsibilities in `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md` without coupling the execution core to a particular screen hierarchy.

## 8. Planning-only boundary remains unchanged

This continuation does not authorize:

- Forge production implementation;
- Builder deprecation/deletion;
- live requests or writes;
- game-source changes;
- release pin movement;
- manifest contract migration;
- credential/session export;
- publishing/live content changes.

## 9. Handoff expectation

When the full planning package is complete:

- push/freeze the exact Fable SHA;
- list every planning artifact actually committed;
- identify any items that remained pending solely because the predecessor transcript was unavailable;
- distinguish source-backed capability decisions from user-owned visual/UX choices;
- provide the normal exact-SHA handoff for independent ChatGPT review under `docs/workflows/FABLE_REVIEW.md`.

Do not request implementation approval as part of the same handoff unless the user separately approves the roadmap after independent review.