# Forge Next — Mobile Ergonomics & Accessibility Audit

**Status:** DESIGN AUDIT / ACCEPTANCE INPUT  
**Date:** 2026-09-12  
**Current implementation baseline:** Forge `0.4.0`, `main` at `305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Engineering Auditor  
**Depends on:** current UI baseline audit, safety-state presentation contract, style-board inventory and reconciliation matrix  
**Scope:** Android/phone-first ergonomics, responsive behavior, accessibility requirements and testable redesign acceptance criteria  
**Out of scope:** final IA, final token values, production implementation, browser/live smoke

## 1. Context

Forge is operated in a real mobile userscript/browser workflow, not merely inspected on desktop. The current UI is explicitly mobile-first and already has several good mechanical defaults, but Forge Next will add substantially more capability and information density.

The redesign therefore has two simultaneous obligations:

1. preserve current phone safety and touch usability;
2. avoid turning the larger product into a desktop console that merely collapses at narrow widths.

This audit converts those obligations into concrete design/test criteria.

## 2. Current source-backed mobile strengths

Forge 0.4.0 already provides:

- a single-column primary content flow;
- scoped full-screen overlay scrolling;
- standard buttons/inputs at a 44px minimum height;
- native controls for most interactive elements;
- no hover requirement for primary workflow actions;
- wrapping action groups rather than fixed-width button bars;
- long technical IDs that can break/wrap;
- sticky top product bar;
- explicit inline error/status content rather than console-only failures.

These are baseline protections, not redesign debt. Forge Next should not lose them while becoming more polished.

## 3. Current phone friction

### Navigation saturation

The present five-button horizontal navigation works because Forge has only five technical screens. It does not scale cleanly to Dashboard, content creation, capture/research, review/admin, recovery, library/history and settings/diagnostics.

**Risk:** more tabs either create excessive horizontal scrolling or shrink labels/touch targets.

### Long vertical safety flows

Manifest preflight and Run screens can become long stacks of:

- warnings;
- item summaries;
- images;
- progress;
- budget;
- full-capture persistence;
- per-item state;
- drift/error detail.

**Risk:** the highest-consequence context scrolls out of view before the operator reaches the action or failure that depends on it.

### Dense technical metadata

Entity types, operation names, IDs, hashes, dependency lists, data keys, phases and error strings are often visible by default.

**Risk:** ordinary human meaning and the next safe action compete with forensic detail.

### Recovery decisions

Current orphan/reconciliation cards may include IDs, candidates, manual ID entry, re-send and skip actions.

**Risk:** on a narrow screen, multiple high-consequence actions and long identifiers can create tap/interpretation mistakes.

### Toast competition

Fixed bottom toasts are useful, but Forge Next may also use bottom navigation or sticky action bars.

**Risk:** bottom-layer UI elements can overlap or compete, especially with mobile browser chrome/virtual keyboard.

## 4. Mobile shell requirements

### Navigation

The stable design direction is a dedicated phone navigation pattern rather than a shrunk desktop rail.

Requirements:

- highest-frequency destinations fit without horizontal scrolling;
- secondary destinations move under a clear `More`/menu surface;
- current destination remains obvious by text + icon/shape, not color alone;
- recovery/attention state may badge a destination but must not silently redirect the operator;
- navigation must remain reachable with one hand without crowding the primary action region;
- the shell must account for device/browser safe areas and bottom browser chrome.

The exact destination labels remain transcript/Fable-IA dependent.

### Persistent operation context

For mutation/publish/recovery workflows, operation consequence must remain available while scrolling.

Acceptable patterns include:

- compact sticky mode header;
- collapsible sticky summary;
- top summary plus sticky action bar carrying the mode label.

Requirement: the operator should not reach a consequential action after scrolling several screens and have to remember whether the job is read-only, live-write or recovery.

### Sticky action areas

Allowed when useful, with constraints:

- never cover active warnings/errors;
- respect mobile safe area;
- one dominant primary action per decision region;
- secondary/destructive alternatives must not be packed immediately beside the dominant action if a slip would be costly;
- keyboard opening must not hide the control being edited or the confirmation consequence.

## 5. Touch target requirements

### Baseline

- 44x44 CSS px minimum for all normal interactive controls;
- prefer 48px minimum height for primary mobile actions;
- icon-only controls need an equivalent minimum hit target even when the glyph is smaller;
- row-level tap targets must not contain competing nested tap behavior that causes accidental navigation.

### High-consequence controls

For publish, re-send, adopt, skip, delete evidence or other consequential actions:

- do not place two destructive/irreversible targets directly adjacent without meaningful spacing;
- prefer full-width or clearly separated action rows when choice consequence differs materially;
- require descriptive labels, not icon-only danger controls;
- confirmation must repeat the target/action, not merely ask `Are you sure?`.

## 6. Information-density requirements

### Progressive disclosure

On phone, show in this order:

1. what the user is doing;
2. whether it touches live data;
3. what is blocked/uncertain;
4. primary next action;
5. human content summary;
6. secondary metadata;
7. raw technical detail.

Technical detail should collapse behind explicit disclosure such as `Details`, `Technical details`, or a contextual side/fullscreen panel.

### Never solve density by shrinking text

- body operational copy should remain approximately the established 14–15px class or better;
- critical consequence text must not become micro/caption size;
- IDs may wrap or scroll in their own region; they must not force the whole page horizontally.

### Tables

Ordinary workflow tables should transform into stacked rows/cards on phone.

Use horizontal scrolling only for genuinely comparative/technical data where preserving columns is more useful than stacking, and provide clear scroll affordance.

## 7. Form requirements

- labels above controls on phone;
- helper/error text directly below the control it explains;
- validation errors remain visible after keyboard close/open;
- controls that depend on another choice must not silently move offscreen after rerender;
- select/toggle state must include a textual label;
- dirty/changed state must not use danger red merely to indicate unsaved edits;
- file/image pickers must show what file/asset is still missing and why execution is blocked;
- search/filter fields should preserve their value when navigating to detail and back where practical.

## 8. Confirmation requirements on phone

A custom Forge confirmation is preferable to relying permanently on browser-native `confirm()` because Forge Next needs structured consequence information.

Every high-consequence confirmation should contain, in order:

- action title;
- operation mode/context;
- exact human consequence;
- target/content summary;
- counts where helpful;
- uncertainty/read-back caveat if applicable;
- safe cancel;
- explicit action verb.

Examples of acceptable action verbs:

- `Start live write`
- `Publish 3 items`
- `Adopt this record`
- `Re-send update phase`
- `Delete snapshot`

Avoid generic `Submit`, `Continue` or `OK` for production consequences.

## 9. Recovery ergonomics

Recovery is the highest-risk mobile workflow and should get dedicated layout rules.

### Above the fold

Show:

- what is uncertain;
- whether a request may have left;
- what Forge knows from reconciliation;
- whether ordinary retry is unsafe;
- the recommended next safe action, if one exists.

### Candidate selection

For orphan adoption:

- candidate name/context before raw ID where available;
- ID still visible/copyable;
- one candidate per comfortably tappable row/card;
- selection and final adoption confirmation are separate moments unless evidence makes only one candidate possible and the state machine already treats it as safe;
- do not make the first candidate visually selected by default.

### Skip / re-send

Separate these actions visually and spatially from adoption.

`Skip` must repeat that an existing live row is not deleted.

`Re-send` must identify phase and target and should never look like a normal retry.

## 10. Read-only versus live-write ergonomics

The phone UI must make read-only work materially calmer/easier than mutation work without making read-only persistence consequences invisible.

### Read-only

- safe inspection context visible;
- lower confirmation burden for ordinary reads;
- full capture receives additional persistence disclosure because repository/export consequence changes even though mutation count remains zero.

### Live write

- consequence summary before primary action;
- creates/updates/uploads counts where available;
- auth/readiness blockers visible before action;
- confirmation is explicit and mode-labeled;
- active operation context remains visible during run.

## 11. Color and contrast acceptance criteria

Exact tokens remain unresolved, but implementation must verify:

- WCAG AA contrast for body text and interactive labels in normal states;
- status text remains legible on tinted/glowing backgrounds;
- disabled controls remain readable enough to understand what is disabled while clearly non-interactive;
- focus indication is distinct from selected/active/status color;
- operation-mode families remain distinguishable from semantic outcome families in grayscale/color-deficiency contexts through icon/label/shape as well as hue;
- lane imagery/gradients never reduce card-label contrast below the operational baseline.

Do not accept screenshots as contrast proof; final implementation should use measured values/tests.

## 12. Focus and keyboard requirements

Although mobile touch is primary, Forge also has desktop/tablet use and browser accessibility requirements.

- every interactive element gets visible focus;
- DOM/focus order follows reading/consequence order;
- modal focus is trapped appropriately and returns to the invoking control after close;
- opening progressive detail must not unexpectedly reset scroll/focus;
- keyboard navigation can reach advanced/raw views without mouse hover;
- escape/back behavior must not dismiss a high-consequence confirmation by also triggering an underlying action.

## 13. Screen-reader / dynamic status requirements

Future implementation should provide appropriate announcement behavior for:

- validation errors after preflight;
- auth ready/refused changes;
- job paused;
- job failed;
- `SENT` / reconciliation required;
- verification complete;
- capture persistence failure;
- toast notifications where they carry actionable information.

Do not rely on visual progress bars or icon changes alone.

Avoid announcing every minor percentage update; announce meaningful phase/status transitions.

## 14. Motion accessibility

Forge Next may use more motion than 0.4.0.

Requirements:

- respect `prefers-reduced-motion`;
- remove non-essential glow travel/pulse/page-transition motion under reduced motion;
- state changes still remain obvious when animation is removed;
- no animated red danger effects;
- no animation that delays action availability;
- progress can use subtle animation, but phase text remains the authoritative cue.

## 15. Browser/mobile environment hazards to test

Later implementation/browser smoke should explicitly cover:

- Firefox Android viewport with browser chrome expanded/collapsed;
- Android virtual keyboard over forms/search/modal content;
- phone orientation change where supported;
- long IDs/errors without layout overflow;
- bottom navigation + toast + sticky action coexistence;
- scroll lock/release when Forge overlay opens/closes;
- carrier page restoration after close;
- navigation/route changes underneath the overlay;
- tab eviction/reopen/resume state;
- reduced-motion preference;
- text-size/browser zoom increases;
- touch actions with no hover affordance.

This audit does not perform those live/browser checks; it makes them explicit acceptance work.

## 16. Responsive breakpoint behavior principles

Do not design arbitrary breakpoint layouts solely around device names.

### Narrow phone

- one primary column;
- bottom/compact navigation;
- stacked cards;
- technical detail collapsed;
- one primary action region;
- persistent compact operation context.

### Wide phone / small tablet

- maintain touch-first controls;
- optional two-column card grids only where independent;
- avoid turning recovery/preflight into cramped parallel columns.

### Tablet / desktop

- use horizontal space for parallel context/evidence;
- persistent side navigation is appropriate;
- technical detail may live in a secondary panel;
- primary action/consequence still remains near the main work, not stranded in a distant sidebar.

## 17. Style-board mobile reconciliation

The latest board's mobile sample supports:

- bottom navigation;
- large labeled icons;
- atmospheric/brand imagery above the nav;
- a compact five-item primary set.

This is compatible with durable direction.

Still unresolved:

- exact destinations;
- whether `Admin` belongs in the primary phone set for every authorized user;
- badge/attention treatment;
- behavior of `More`;
- whether active work/recovery should temporarily alter the navigation shell.

## 18. Testable acceptance checklist for future implementation

A Forge Next phase that changes the shell or a major workflow should not be considered mobile-complete until it demonstrates:

- no horizontal page overflow at target phone widths;
- all ordinary controls meet 44px target size;
- primary production controls meet preferred 48px height where layout permits;
- operation consequence remains visible/recoverable after scrolling;
- no warning/error is covered by sticky navigation/action surfaces;
- keyboard does not hide the active field/action irrecoverably;
- destructive/recovery alternatives have sufficient separation;
- text remains readable at increased browser text size/zoom;
- focus states are visible;
- state is not color-only;
- reduced-motion mode preserves meaning;
- long IDs/error text do not break layout;
- ambiguous write flow cannot expose a normal retry;
- read-only/full-capture/live-write flows remain distinguishable;
- auth refusal and role denial have distinct recovery wording when source exposes the distinction.

## 19. Priority UX issues for wireframing

The next wireframe/component-anatomy work should prioritize these phone cases rather than designing only the happy path:

1. Command Center with one active resumable job and one system blocker;
2. read-only manifest preflight;
3. full-capture preflight with persistence consequence;
4. live-write preflight with missing/blocked input;
5. active live-write run;
6. `INCOMPLETE` verification owed;
7. `SENT` reconciliation required;
8. orphan candidate adoption;
9. auth refused mid-job;
10. Content Admin publish confirmation once source feasibility is known.

## 20. Completion statement

Step 5 of the interim Forge UI workflow is complete.

This audit does not change the visual north star; it constrains how that visual system must behave on the operator's real phone workflow and establishes concrete accessibility/mobile checks for later Fable implementation and independent review.