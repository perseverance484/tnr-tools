# Forge Next — Latest Style Board Inventory

**Status:** OBSERVED ARTIFACT INVENTORY — NOT AN APPROVAL RECORD  
**Date:** 2026-09-12  
**Source artifact:** user-supplied `Forge Design System v0.1` board in the replacement ChatGPT conversation  
**Depends on:** `docs/design/FORGE_NEXT_UI_CONTEXT_HANDOFF.md`  
**Lead lens:** Art Director  
**Supporting lens:** UI/UX Reviewer  
**Purpose:** record what is visibly present in the latest board so transcript reconciliation can focus on approval chronology rather than re-analysis

## 1. Evidence boundary

This file records **what the board visibly proposes**.

It does **not** establish that every board detail was approved. The predecessor chat export is still pending, so any conflict with repository design sources remains unresolved until chronology is reconstructed.

Do not use this file as the canonical implementation palette or final IA.

## 2. Overall product character visible in the board

The board presents Forge as a dark, premium TNR operations application rather than a generic admin panel.

Visible characteristics:

- a wide branded masthead with `TNR FORGE` identity;
- moonlit fortress/village landscape with cool blue night lighting and red foliage accents;
- deep navy/black operational surfaces;
- bright crimson and warm gold brand/action accents;
- cyan/blue system accents;
- ivory/parchment text/highlight color;
- strong outlined panels with subtle glow/elevation;
- squared-to-moderately-rounded controls rather than soft SaaS pills everywhere;
- high-contrast iconography;
- controlled glow used around active/status/action examples;
- dense but organized component-showcase composition.

The board strongly aligns with the repository's previously approved “professional TNR content-operations application” character, but exact components/colors remain subject to reconciliation.

## 3. Core palette shown

### Brand family

The board labels four primary brand colors:

| Board label | Visible value | Intended board role |
| --- | --- | --- |
| Crimson | `#B91C1C` | primary TNR red / action / brand |
| Gold | `#F59E0B` | warm branded emphasis |
| Ninja Ink | `#0EA5E9` | bright cool system/accent blue |
| Ivory | `#F4EBD9` | warm light text/accent |

### Neutral family

The board shows a stepped slate/near-black scale:

| Board label | Visible value |
| --- | --- |
| Deep Black | `#05080F` |
| Slate 900 | `#0F172A` |
| Slate 800 | `#1E293B` |
| Slate 700 | `#334155` |
| Slate 600 | `#475569` |
| Slate 400 | `#94A3B8` |
| Slate 300 | `#CBD5E1` |
| Slate 200 | `#E2E8F0` |

These values are recorded as board content only. They are not elevated here above `FORGE_NEXT_COLOR_SEMANTICS.md` or later transcript decisions.

## 4. Semantic outcome colors shown

The board explicitly separates a **Semantic Colors** panel from operation-mode colors.

Visible semantic mappings:

| Semantic label | Board value | Board wording |
| --- | --- | --- |
| Success | `#16A34A` | Completed / Healthy |
| Info | `#0EA5E9` | Information / Neutral |
| Warning | `#F59E0B` | Check Required |
| Error | `#EF4444` | Action Failed |
| Critical | `#7F1D1D` | System / Safety Critical |
| Muted | `#64748B` | Disabled / Inactive |

Important observed principle: the board treats semantic result/status color as a separate system rather than using every accent color interchangeably.

## 5. Operation-mode system shown

The board contains both an **Operation Mode Colors** panel and a **Mode Selector (Example)**.

The visible mode taxonomy is:

1. `Read Only`
2. `Write`
3. `Review`
4. `Publish`
5. `Recovery`

Visible board associations:

| Mode | Visible family | Board consequence wording |
| --- | --- | --- |
| Read Only | indigo/periwinkle | Safe Inspection |
| Write | cyan | Live Changes |
| Review | violet/purple | Staging / Approval |
| Publish | orange | Live Deployment |
| Recovery | teal | Resolve / Repair |

The legible board hex labels include:

- Read Only: `#6366F1`
- Write: `#06B6D4`
- Review: `#8B5CF6`
- Publish: `#F97316`

The Recovery family is visibly teal; this inventory does not promote an uncertain small-text hex reading to a durable value.

### Major chronology flag

This taxonomy does **not** exactly match the earlier repository color amendment. In particular, `Review` appears as a first-class board mode and the Publish/Recovery mapping differs from the earlier proposal.

Treat this as a transcript-reconciliation question, not an automatic supersession.

## 6. Typography system shown

The board demonstrates a clearly separated display/operational hierarchy.

Visible examples:

| Role | Board sample | Board spec text |
| --- | --- | --- |
| H1 | `Forge Title` | Bold / 40px / 120% |
| H2 | `Section Header` | Semibold / 28px / 130% |
| H3 | `Panel Header` | Semibold / 20px / 130% |
| H4 | `Subsection` | Semibold / 16px / 140% |
| Body | operational body copy | Regular / 15px / 150% |
| Small | secondary/hints | Regular / 13px / 150% |
| Caption | labels/metadata | Regular / 12px / 150% |

The H1 sample uses a stylized serif/display treatment, while H2–body examples appear substantially more conventional/readable.

Observed design intent: brand/display typography may carry personality, but functional copy remains clean.

## 7. Desktop navigation proposal shown

The board's desktop navigation example is a persistent left rail.

Visible destinations, in order:

1. Dashboard
2. Create Content
3. Capture
4. Edit & Write
5. Validate
6. Manifest & Deploy
7. Content Admin
8. Library
9. Reports
10. Settings

The active Dashboard row receives strong crimson focus styling.

This is an **illustrated navigation proposal**, not yet canonical IA. The existing planning brief explicitly keeps final top-level navigation user-owned and evidence-dependent.

## 8. Mobile navigation proposal shown

The board separately demonstrates a mobile bottom navigation pattern rather than simply shrinking the desktop rail.

Visible primary items:

- Home
- Create
- Capture
- Admin
- More

This supports the previously approved principle that mobile should get its own navigation adaptation.

The relationship between desktop destinations and the `More` grouping remains unspecified in the board.

## 9. Content-lane cards shown

Six large visual content-lane cards are shown:

### Combat

Descriptor examples: skills, enemies, AI, encounters. Visual treatment is crimson/red with a combat silhouette.

### Items

Descriptor examples: gear, consumables, materials. Visual treatment is bright blue with a potion/flask subject.

### Quests & Events

Descriptor examples: stories, triggers, world content. Visual treatment is warm amber/gold with scroll/mission imagery.

### Locations

Descriptor examples: zones, maps, travel, discovery. Visual treatment is teal/cyan with a pagoda/environment subject.

### Characters

Descriptor examples: NPCs, factions, dialogues. Visual treatment is violet/purple with a character silhouette.

### Systems

Descriptor examples: mechanics, configuration. Visual treatment is steel/neutral with crate/tooling imagery.

Observed pattern:

- full-card atmospheric image;
- dark gradient/readability layer;
- lane name in strong uppercase type;
- concise descriptor list;
- colored border/accent family;
- forward-chevron affordance.

These labels remain illustrative until taxonomy/IA is resolved.

## 10. Button hierarchy shown

The board demonstrates six button treatments:

- Primary Button
- Secondary Button
- Ghost Button
- Success Button
- Warning Button
- Danger Button

Observed traits:

- primary has strong crimson fill/glow and forward chevron;
- secondary is dark with outlined geometry;
- ghost is low-fill/outlined;
- success/warning/danger use semantic families and meaningful icons;
- controls are moderately squared rather than capsule-shaped.

Potential reconciliation question: whether semantic Success/Warning buttons are meant as reusable action variants or only illustrative status-action examples. The board alone cannot settle that.

## 11. System status indicators shown

A compact status indicator set includes:

- Online
- Operational
- Degraded
- Outage
- Offline
- Maintenance
- Rate Limited
- Unknown

Each combines text, color and a small icon/dot cue.

This status set appears oriented toward **system/service health**, not journal item lifecycle, which supports keeping those domains separate in the safety-state contract.

## 12. Operation mode indicator shown

A prominent operation-context component displays:

- icon;
- large `LIVE WRITE` label;
- supporting consequence text (`Changes will modify game data.`);
- a `Change` control/dropdown.

Observed intent: operation mode is persistent context with plain-language production consequence, not merely a small badge.

The exact mode naming remains transcript-sensitive.

## 13. Mode selector shown

The board also shows a compact five-choice mode selector using large icon tiles:

- Read
- Write
- Review
- Publish
- Recovery

Each has a distinct hue/icon identity.

Potential UX issue to evaluate later: a mode selector can be useful if mode is genuinely user-selectable, but must not imply that choosing a color/mode grants a capability or authority the current workflow/account does not possess.

## 14. Form system shown

The form example includes:

- labeled text input;
- select/dropdown;
- checkbox with red selected treatment;
- toggle/switch;
- search input with icon.

The overall form language is compact, outlined and dark-surface oriented.

The board claims “Clean and accessible,” but this visual inventory does not verify contrast, keyboard, screen-reader or focus behavior.

## 15. Confirmation/modal example shown

The dialog example is a centered high-consequence confirmation titled `Confirm Deployment`.

Visible content pattern:

- prominent warning icon;
- clear action title;
- plain-language consequence copy stating that items will be published live;
- explicit `Cancel` and `Deploy` actions;
- destructive/high-consequence action receives orange emphasis rather than ordinary primary styling.

Observed principle worth preserving regardless of final wording: consequential operations should state the production effect, not use a generic `Continue` confirmation.

## 16. Notification examples shown

Five notification types are demonstrated:

- successful validation;
- new capture available for review;
- rate limit approaching;
- manifest validation failed;
- ready for review.

They use distinct semantic/context families with icons, label text and close controls.

Potential design implication: `Ready for review` is visually treated as a review/workflow notification, not success or warning.

## 17. Progress states shown

The board demonstrates multiple operation-progress rows with icon, label, bar and percentage:

- Processing manifest — 60%
- Capturing game data — 30%
- Validating content — 75%
- Deploying to repository — 15%

Different contextual accent colors are used across rows.

This is visually richer than the current single progress bar, but any implementation must obey the safety-state contract: contextual color cannot imply success before verification.

## 18. Panel/container treatments shown

Three panel variants are demonstrated:

- Default Panel — standard contained surface;
- Elevated Panel — raised content with stronger shadow/light border;
- Accent Panel — highlighted/focused content with crimson edge/glow.

This provides a clear hierarchy vocabulary without requiring every surface to glow.

## 19. Empty state shown

The board's empty state uses:

- large neutral cube/box icon;
- `No Content Yet` heading;
- short guidance copy;
- prominent `Create Content` action.

The surface is visually calm and leaves room for brand personality.

## 20. Error state shown

The error state uses:

- large red warning triangle;
- `Something Went Wrong` heading;
- concise explanation;
- primary `Try Again` action;
- secondary `View Logs` action.

Important future constraint: generic `Try Again` is appropriate only for genuinely retry-safe errors. The safety-state contract prohibits using that generic pattern for ambiguous writes.

## 21. Icon system shown

The icon sample uses simple outlined pictograms including home, weapon/tool, flask, scroll/document, location, users, settings and cube/package shapes.

The board explicitly lists the intended icon properties:

- consistent stroke weight;
- simple, recognizable shapes;
- optimized for dark UI;
- meaningful and game-appropriate;
- support for filled and outline variants.

The overall direction is operational/iconographic rather than decorative fantasy glyphs.

## 22. Reusable component inventory derived from the board

Architecture-neutral component concepts visibly supported by the board:

- branded application masthead;
- desktop navigation rail;
- mobile bottom navigation;
- content-lane card;
- operation-context header;
- mode selector;
- system-health chip;
- status/semantic notification;
- primary/secondary/ghost/action-semantic buttons;
- field wrapper/input/select/checkbox/toggle/search;
- consequence confirmation modal;
- operation-progress row;
- default/elevated/accent panel;
- empty state;
- error state;
- icon family.

This inventory can be mapped against real Forge workflows before any implementation framework is chosen.

## 23. Visible strengths of the board

- operation context is separated visually from semantic outcome status;
- desktop and mobile navigation are treated differently;
- content work gets human-facing visual lanes rather than procedure names;
- TNR-specific atmosphere is concentrated in brand/lane areas rather than form-heavy panels;
- component hierarchy is much richer than current Forge while remaining readable;
- state communication generally combines icons, labels and color;
- elevated/accent surfaces provide hierarchy without forcing every component into one style;
- modal/notification/progress examples speak in operational terms.

## 24. Visible risks / questions to test later

These are design-review questions, not rejections:

- several bright glows may become visually noisy in real data-dense screens;
- lane colors sometimes sit near semantic hues, so the semantic-vs-decorative rule must remain explicit;
- mode colors include several adjacent blue/violet/teal families whose distinctness needs accessibility/real-device testing;
- the desktop nav contains ten destinations before secondary grouping is considered;
- `Manifest & Deploy` combines a technical object and a consequence in one destination name;
- `Edit & Write`, `Validate`, `Manifest & Deploy`, and `Review` may overlap conceptually depending on Fable's eventual workflow model;
- the board's generic `Try Again` error pattern must not be reused for ambiguous writes;
- the mode selector must not make operation authority look like a user preference;
- stylized H1 branding should remain out of warnings, forms, diffs and dense operational text.

## 25. Items requiring transcript reconciliation

Highest-priority chronology questions raised by the board:

1. Was the five-mode `Read / Write / Review / Publish / Recovery` taxonomy explicitly approved?
2. Did the board supersede the earlier operation-mode color amendment, or was it another proposal?
3. Was the desktop navigation destination set approved or illustrative?
4. Was the mobile `Home / Create / Capture / Admin / More` set approved?
5. Were the six content-lane names accepted as the working taxonomy?
6. Were the board's exact palette/typography values accepted, or only the visual character?
7. Were semantic action buttons (`Success`, `Warning`) intended as real component variants?
8. Was the displayed `Confirm Deployment` pattern accepted as the publishing/deployment direction?

## 26. Completion statement

Step 3 of the interim Forge UI workflow is complete as an observed artifact inventory.

The board has now been converted from an image that future sessions would need to reinterpret into a searchable repository record of its visible proposals, while deliberately preserving the distinction between **observed** and **approved**.