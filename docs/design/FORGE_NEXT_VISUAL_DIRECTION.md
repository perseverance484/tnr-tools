# Forge Next — approved visual direction

**Status:** USER-APPROVED VISUAL NORTH STAR FOR PLANNING  
**Date:** 2026-09-12  
**Applies to:** `state/prompt_forge_next_planning.md`  
**Decision owner:** project director/operator  
**Implementation owner:** Fable / Claude Code UltraCode after roadmap approval  
**Independent review:** ChatGPT, UI/UX Reviewer + Engineering Auditor

## 1. Purpose

This document records the visual/product direction approved by the project director during the Forge Next planning phase.

A concept mockup was reviewed in chat and explicitly approved as the desired direction. The image itself should be supplied to Fable alongside the planning brief as a **visual reference**. This document makes the important parts durable in the repository so the direction does not depend on chat memory.

The mockup is a **north star, not a pixel-perfect implementation contract**. Fable must still complete the evidence-backed information-architecture and capability analysis required by the planning brief. Exact labels, card counts, navigation placement, and content grouping may change when the deep dive proves a better structure. Material departures from the visual character described here should be surfaced for user approval rather than silently replacing the direction.

## 2. Approved product character

Forge Next should feel like a **professional TNR content-operations application**: polished enough to feel first-party and game-specific, but clearer and more operational than an in-game screen.

The target character is:

- professional and trustworthy;
- immediately understandable to a content operator or admin;
- distinctly TNR rather than generic SaaS/admin software;
- dark, atmospheric and premium;
- a little flashy through depth, lighting, motion and strong state feedback;
- restrained enough that production state, warnings and recovery remain obvious;
- responsive/mobile-first rather than a desktop dashboard squeezed onto a phone.

The aesthetic should support the work rather than compete with it.

## 3. Visual language

Use the current TNR client as inspiration, not as a requirement to duplicate its page chrome.

### Foundation

- deep navy / charcoal / near-black surfaces;
- layered panels with subtle separation rather than flat gray boxes;
- warm ivory/parchment for selective high-attention surfaces and text accents;
- burnt crimson / dark red as a signature TNR action/accent family;
- warm gold/amber for premium emphasis, review/admin cues, and branded highlights;
- cool chakra-like blue as a secondary/system/active accent;
- semantic green, amber and red remain reserved for success, caution and danger where clarity matters.

Decorative lane colors may include blue, crimson, gold, teal or violet, but they must not override semantic status colors.

### TNR-inspired details

Borrow selectively from the game's current hard-edged ink language:

- confident borders and silhouette;
- occasional squared/hard-edged controls rather than ubiquitous soft SaaS pills;
- restrained offset shadows inspired by TNR's ink buttons;
- strong typography and compact labels;
- subtle atmospheric ninja-world imagery or texture in non-critical hero/empty-state areas;
- light glow or energy accents for focus/current activity;
- tasteful transitions and active-state motion.

Do **not** introduce prohibited franchise material, copied proprietary visual identity, decorative text that harms readability, or heavy fantasy ornament around safety-critical actions.

## 4. Shell / navigation direction

The approved mockup strongly favors a persistent application shell rather than the current horizontally scrolling five-tab utility UI.

### Desktop / tablet

Preferred direction:

- compact left navigation rail;
- branded Forge identity at the top;
- main workspace using the full available width;
- current session/operator/system state visible without dominating the page;
- active work/recovery state remains accessible across destinations.

### Phone

Do not merely shrink the desktop sidebar.

Preferred direction:

- bottom navigation for the highest-frequency destinations;
- secondary destinations grouped under a clear More/menu surface;
- sticky contextual action area where appropriate;
- large touch targets;
- one primary decision/action per viewport region;
- dense technical details collapse progressively rather than disappearing.

Fable must validate the exact destination set against actual workflow frequency and risk during planning.

## 5. Dashboard / Command Center direction

The approved concept establishes a strong **Command Center** home rather than opening directly into a raw manifest list.

It should answer at a glance:

- can Forge safely operate right now?;
- what work is active or resumable?;
- what needs attention/review?;
- what did I recently do?;
- what is the fastest path to the task I came here to perform?

Candidate blocks from the approved concept:

- **Quick Actions** — e.g. create content, capture from live, validate, create/open manifest;
- **Content Lanes** — large visual entry points into major content families;
- **Recent Activity** — manifests, captures, writes, review actions;
- **System Status** — session/auth, repository connectivity, validation readiness, rate-budget health;
- **Content Admin** — visible pending-review count and direct entry to review/preview/publish work.

These blocks are directionally approved. Their final data sources and exact actions must be evidence-backed in Fable's plan.

## 6. Content lanes

The approved mockup uses visually distinct content-lane cards so users choose the kind of work they are doing rather than starting from a technical procedure.

Illustrative lane concepts shown in the mockup include:

- Combat;
- Items;
- Quests & Events;
- Locations;
- Characters;
- Systems.

These labels are **not yet canonical taxonomy**. Fable must map them against Forge/Builder/game capabilities and recommend the final grouping. The important approved principle is that common content work should have recognizable, human-facing lanes rather than a single undifferentiated manifest console.

Each lane may have its own accent/image treatment, but the underlying interaction system should remain consistent.

## 7. Content Admin direction

Content Admin should look and feel intentionally simpler than Content Operations while remaining part of the same product.

The approved concept makes Content Admin a first-class destination with obvious actions such as:

- Review pending content;
- Edit content;
- Preview content;
- Publish / Unpublish where authorized;
- Browse the content library/history.

The admin should see human-facing content and change summaries first. Manifest internals, procedure names, payload JSON and reconciliation details should be available only when useful/authorized, not required for ordinary review.

Publishing must remain visually deliberate and permission-aware. A polished interface must not turn publish/unhide into an accidental tap.

## 8. Operation mode header — required UX exploration

Fable should explicitly explore a persistent operation-context treatment for actionable flows.

Before execution, the interface should make the production consequence legible in plain language, for example:

- `READ ONLY`;
- `LIVE WRITE`;
- `PUBLISH`;
- `RECOVERY`.

Pair this with useful counts such as:

- records read;
- records changed;
- creates;
- uploads;
- captures;
- publishes/unpublishes;
- deletes, if a future authorized workflow ever supports them.

The goal is that a user can understand whether the action touches production before reading technical detail.

This does not replace the journal/reconciliation lifecycle. It is the human-facing summary above it.

## 9. State visualization

Flashiness must reinforce state rather than blur it.

Recommended principles:

- active/running work may use restrained animated energy/progress treatments;
- completed verified work should feel decisively finished;
- paused/incomplete/recovery work should be visually distinct from both success and failure;
- ambiguous `SENT` state must never look retry-safe;
- authentication unavailable, authorization denied and transport/read failure should remain separate states;
- read-only capture jobs should look materially safer than live-write jobs;
- full capture persistence should remain explicitly visible because it changes repository persistence consequences;
- publishing should get its own unmistakable visual treatment.

Do not use color alone to communicate these states.

## 10. Motion and polish

Approved level of motion/polish:

- short card/selection transitions;
- subtle glow/edge response on active content lanes;
- progress animation during long operations;
- responsive status changes;
- smooth expansion of advanced details;
- tasteful page/section transitions when they improve orientation.

Avoid:

- constant ambient animation in data-heavy views;
- motion behind critical confirmation dialogs;
- long cinematic transitions;
- effects that make the interface feel like a game battle screen rather than a professional operations tool.

Respect reduced-motion preferences where practical.

## 11. Typography and density

Use strong, legible interface typography for operational text. A stylized/display face may be used sparingly for the Forge brand or major section identity, but field labels, tables, warnings, diffs and controls should use a highly readable UI face.

The desktop layout may be information-rich. Mobile should progressively disclose secondary metadata rather than producing tiny text or horizontal overflow.

Monospace remains appropriate for IDs, procedure paths, hashes and raw payload/debug views only.

## 12. What from the concept is binding vs illustrative

### Approved / preserve in subsequent planning

- TNR-specific dark atmospheric visual character;
- professional operations-tool clarity;
- crimson/gold/cool-blue accent family over deep navy/charcoal;
- stronger branded Forge identity;
- modern layered dashboard rather than a generic flat utility screen;
- clear Quick Actions;
- visual content lanes;
- first-class Content Admin presence;
- obvious system/session readiness;
- recent activity/work continuity;
- strong mobile and desktop adaptations;
- polish through controlled motion, depth and state visualization.

### Illustrative / Fable may change with rationale

- exact `FORGE` logo treatment;
- background illustration;
- exact wording such as `Dashboard` vs `Command Center`;
- exact sidebar destinations;
- exact content-lane names/grouping;
- the number/order of Quick Actions;
- exact colors/hex values;
- exact icon set;
- exact card geometry;
- exact desktop column layout.

### Must not be inferred from the concept

- that every displayed action already exists;
- that a content type can be edited/published without source-verified procedures/permissions;
- that Forge may bypass TNR auth/roles;
- that visual simplification permits weaker confirmation/recovery semantics;
- that Builder may be retired before objective parity gates pass.

## 13. Planning deliverables added by this direction

Fable's planning package should include:

1. a screen map showing how the recommended IA relates to this approved direction;
2. desktop and phone wireframes for Command Center, a content lane, manifest preflight/run, Content Admin queue/detail/preview/publish, and recovery;
3. a compact design-token proposal covering surfaces, text, borders, signature accents and semantic states;
4. a component inventory showing reusable shell/navigation/card/status/action patterns;
5. a statement of any recommended departure from this document and why the real workflow/source evidence requires it;
6. a proposed implementation sequence that allows the visual shell/design system to evolve without destabilizing the existing execution/recovery core.

Do not implement production UI during the planning pass.

## 14. Reference handling for Fable kickoff

When starting the Fable planning session, provide both:

- the exact planning-contract SHA containing `state/prompt_forge_next_planning.md` and this file; and
- the approved concept mockup image as a chat attachment.

Tell Fable explicitly:

> Treat the attached Forge mockup as the user-approved visual north star. Read `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` for what is binding versus illustrative. Reconcile the design with your capability/IA/source deep dive rather than cloning it blindly. Any material departure from the approved character should be called out in the roadmap for user review.
