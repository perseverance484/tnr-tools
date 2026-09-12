# Forge 0.4.0 — Current UI/UX Baseline Audit

**Status:** EVIDENCE-BASED CURRENT-STATE AUDIT  
**Date:** 2026-09-12  
**Implementation audited:** `main` at `305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Forge package version:** `0.4.0`  
**Audit branch:** `chatgpt/forge-next-planning`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Engineering Auditor  
**Scope:** current Forge shell, screens, operator flows, state presentation, mobile ergonomics, recovery affordances, and redesign constraints  
**Out of scope:** production implementation, final Forge Next IA, final visual direction, game-source changes, live requests/writes

## 1. Purpose

This document establishes the before-state for Forge Next. It answers **what the operator can actually see and do in Forge 0.4.0 today** so redesign work can preserve safety-critical behavior instead of replacing it from memory.

This is a source audit, not a browser/live smoke. Claims are limited to the implementation at the pinned `main` SHA and repository-held evidence. No live game request or write was performed.

Primary implementation sources inspected:

- `forge/package.json`
- `forge/src/ui/app.mjs`
- `forge/src/ui/screens.mjs`
- `forge/src/ui/styles.mjs`
- `forge/src/ui/takeover.mjs`
- `state/prompt_forge_next_planning.md`

## 2. Current product shape

Forge 0.4.0 is a **five-screen technical operations utility**, not yet the Command Center/content-operations product described by Forge Next.

The shell routes directly between:

1. **Jobs**
2. **Manifests**
3. **Run**
4. **Captures**
5. **Settings**

The app begins on Jobs and returns there automatically when resumable work exists. The shell itself consists of a sticky title/version bar, a horizontally arranged navigation strip, a standing authentication banner, a single main content column, and fixed-position toast feedback.

The implementation is intentionally small and operational. That is a strength for safety and a constraint for the redesign: Forge Next should preserve the execution meanings while replacing the current information hierarchy.

## 3. Host / takeover model visible to UX

Forge is entered through `/forge`, but protected work does not actually run on the providerless `/forge` document. The entry arms the tab and moves Forge onto a real application route where the game's provider/auth runtime remains mounted underneath a fixed, opaque Forge overlay.

Operator-facing consequences:

- Forge behaves like a full-screen application even though the authenticated TNR page stays alive underneath it.
- `Close` returns the carrier page rather than destroying the underlying app state.
- Forge refuses to close while a job is actively running and instructs the operator to pause first.
- the old Builder overlay is suppressed only while Forge is mounted and is allowed to return after Forge closes.
- activation is per-tab through `sessionStorage`; opening Forge in one tab does not intentionally drag another tab into Forge.

**Redesign constraint:** the new shell can look completely different, but must remain compatible with an overlay whose host page and auth providers stay alive underneath it. Global CSS/reset assumptions are unsafe.

## 4. Shell and navigation baseline

### Current shell

`App.mount()` builds:

- sticky top bar: `TNR forge`, version, optional `Close`;
- horizontally scrolling/flexible nav buttons for the five screens;
- auth status region;
- main workspace;
- toast region.

The stylesheet is mobile-first and scoped to `.f-host` / `.f-app`. The main workspace is constrained to `max-width: 760px`, centered, with bottom padding for phone use.

### Current strengths

- extremely low navigation complexity;
- no hover dependency for the core flow;
- button/input minimum height is 44px;
- state/error feedback is kept inside the Forge overlay rather than only in console output;
- all CSS is scoped to avoid contaminating the underlying TNR page;
- the standing auth state is visible on every screen.

### Current UX debt

- the five destinations are technical system surfaces, not the operator's goals;
- the nav has no visual hierarchy between routine work and dangerous/recovery work;
- horizontal top navigation scales poorly as Forge adds Content Admin, content lanes, research/build/review, and diagnostics;
- desktop width is largely unused because the main column stays narrow;
- there is no dashboard/home summary;
- there is no persistent human-facing operation context such as `READ ONLY`, `LIVE WRITE`, or equivalent;
- the current shell has little TNR-specific visual identity beyond dark styling and the product title;
- the shell does not surface recent work, system readiness, pending review, or primary task entry points in one place.

## 5. Standing authentication UX

Authentication is deliberately separated from job outcome.

The banner can represent:

- session ready;
- probing/checking;
- server-proven signed-out/refused;
- authentication not yet confirmed.

When authentication is unavailable, Forge explains that protected work is blocked, that this is not merely a read failure, and gives a recovery path: close Forge, sign in to TNR in the same browser, reopen Forge, and re-check.

A SESSION-paused job cannot offer a functional Resume until the auth probe succeeds again.

### What should survive the redesign

- auth/session readiness must remain globally visible when it affects current work;
- `not authenticated` must remain distinct from ordinary transport/read failure;
- a server refusal must invalidate the optimistic ready state;
- a blocked Resume must explain why it is blocked and what action restores it;
- public/read-only work may remain available where the underlying procedure permits it.

### UX opportunity

The current standing banner is safe but visually expensive. Forge Next can compress healthy auth into a system-health treatment while expanding it automatically when action is required. Do not hide it entirely on production-write screens.

## 6. Jobs screen

### What the screen does

Jobs is simultaneously:

- recovery landing page;
- resumable-work list;
- orphan-resolution workspace;
- recent-run history.

Open jobs appear first as warning banners. The primary recovery button changes wording based on state:

- `Reconcile & resume` when any item is `SENT`;
- `Re-read unverified items` for `INCOMPLETE` jobs;
- otherwise `Resume`.

Recent runs summarize item-state counts and age.

Orphan cards can:

- show server candidates;
- adopt a candidate ID;
- accept a manually pasted ID;
- re-send a known phase for an existing entity only after a confirmation;
- skip while explicitly leaving any server row in place.

### Strengths

- recovery is explicit rather than hidden behind retry;
- ambiguous `SENT` work gets distinct reconciliation wording;
- `INCOMPLETE` communicates that writes may have landed but read-back is still owed;
- orphan handling exposes candidate identities instead of guessing;
- skip wording states that nothing is deleted.

### UX debt / redesign implications

- Jobs mixes ordinary history with high-risk recovery decisions;
- open/resumable work is presented as banners rather than a dedicated continuity model;
- recovery decisions are technically accurate but dense;
- the operator must understand terms such as `SENT`, `ORPHANED`, phases and entity IDs before acting;
- the same screen carries both everyday history and exceptional reconciliation, which makes the highest-risk states compete with routine rows.

**Forge Next implication:** active/resumable work should be visible from the Command Center, while ambiguous/orphan recovery deserves a dedicated recovery treatment with plain-language consequence summaries and advanced technical detail beneath it.

## 7. Manifests screen

### Discovery

The current picker lists JSON files from `push/`, sorted primarily by manifest number. Search matches filename, number or manifest title. A manifest path with prior journal history gets a `ran` pill.

### Selection / preflight

Selecting a manifest:

- parses it;
- resolves plan order;
- runs validator checks for applicable entities;
- resolves image references;
- calculates protected paths that current auth cannot use.

The selected card shows:

- filename;
- item count;
- capture count;
- manifest hash;
- read-only status where applicable;
- full-capture persistence consequence;
- blocking validation problems;
- authentication block;
- pool-resolution notice;
- advisories;
- each planned item with entity/op/target/dependencies/data-key summary;
- required image picks;
- one execution action.

### Read-only distinction

A manifest with zero planned mutation items receives explicit wording that it is a read-only capture job and sends zero mutations. Its primary action becomes `Run captures`.

### Full-capture distinction

Full capture is not rendered as an ordinary capture. Before execution the UI says that exact record bodies will be written into the results bundle and may be committed to the repository when GitHub sync is enabled.

### Write distinction

A mutation-capable manifest receives a browser confirmation that states the number of items/creates and says explicitly that the action writes to the game.

### Strengths

- read-only and mutation-capable jobs are not silently conflated;
- full-capture persistence is disclosed before execution;
- blocking errors disable the primary execution button;
- missing image inputs disable execution;
- auth is re-checked at the moment of execution rather than trusting stale selection state;
- technical detail is sufficient for an expert operator to understand what the manifest intends.

### UX debt / redesign implications

- manifest discovery is repository-file-first rather than job/workstream/task-first;
- filenames, hashes, keys and procedure-level detail dominate the ordinary preflight surface;
- the technical item list does not give a human content summary or before/after meaning;
- browser-native `confirm()` is the final consequence surface rather than a structured Forge confirmation component;
- safe read, full capture persistence, mutation, upload and publish consequences do not yet share a consistent operation-summary grammar;
- no progressive disclosure separates everyday operator information from forensic detail.

## 8. Run screen

The Run screen is the current product's most safety-critical surface.

It exposes:

- manifest/job identity and job state;
- progress bar;
- read-only capture completion/failure summary;
- full-capture persistence success/failure separately from read success;
- verified write completion;
- failed/unverified write summaries;
- SESSION pause handling;
- other pause causes including rate-limit state;
- active running status;
- Resume / Reconcile & resume / Re-read unverified items;
- `Pause after this item`;
- bundle export;
- per-path budget consumption;
- full-capture snapshot persistence;
- per-item state, phase, IDs, errors, drift details and reconciliation notes.

### Safety behaviors that must remain visible

- a successful server write is not represented as verified until the asserted fields read back correctly;
- drift and unread read-back are not green success;
- an `INCOMPLETE` write job explains that the writes are not proven;
- re-reading an incomplete job cannot re-send the write;
- SESSION refusal is explained separately from ambiguous transport state;
- the UI states whether nothing was sent, nothing further was sent, or a server answer proved refusal;
- rate-budget state is inspectable during/after work;
- full-capture read success and body-persistence success are separate facts.

### UX debt / redesign implications

- nearly all execution, safety and diagnostics information is in one long vertical page;
- technical state is accurate but has weak visual hierarchy;
- progress is based on terminal item states rather than communicating richer phase/context to a non-expert;
- per-item rows expose engine vocabulary by default;
- budget detail, capture persistence, item verification and recovery controls all compete at one hierarchy level;
- `Pause after this item` is important but visually similar to ordinary secondary actions;
- the page lacks a persistent top-level consequence summary such as reads/writes/uploads/captures/current mode.

**Forge Next implication:** redesign the surface around a persistent operation header + human progress summary + collapsible technical phases. Do not simplify away the underlying states.

## 9. Captures screen

The screen deliberately distinguishes two different stores:

### Read cache

- lists cached reads and byte usage;
- permits per-entry invalidation;
- permits clearing the entire read cache;
- warns that future reads will spend budget again.

### Immutable full-capture snapshots

- lists durable per-occurrence record-body snapshots;
- explains that writes do not invalidate them;
- permits individual deletion;
- permits deleting all snapshots;
- warns that deleting a snapshot can destroy evidence needed by an unexported job and require another game read.

### Strengths

The distinction between disposable cache and evidentiary snapshot is unusually important and correctly represented in the UI.

### UX debt / redesign implications

- `Captures` currently mixes an operator research concept with low-level cache/storage administration;
- destructive evidence deletion sits inside what sounds like a normal capture library;
- raw cache keys and storage mechanics dominate the surface;
- there is no human-facing capture library organized by content subject, job, workstream or persistence/privacy class.

Forge Next should likely separate **Research/Capture work** from **local storage/evidence management**, even if both use the same underlying stores.

## 10. Settings screen

Settings currently contains three materially different responsibilities:

### GitHub bridge

- PAT input;
- auto-commit results toggle;
- save;
- forget PAT;
- explicit statement that the PAT goes only to GitHub and is stored in the browser under the Builder-compatible key.

### Session diagnostics

- game session description;
- auth description;
- budget values;
- persisted storage state.

### Journal administration

- export journal as text;
- delete finished jobs;
- deletion wording preserves open jobs and ties full-capture snapshots to deleted jobs.

### UX debt / redesign implications

- credentials/configuration, runtime health and destructive maintenance share one undifferentiated settings destination;
- raw JSON-ish diagnostic output is appropriate for expert troubleshooting but not ordinary product status;
- system readiness should be summarized elsewhere, especially on Command Center and operation preflight;
- destructive maintenance actions need stronger separation from ordinary preferences.

## 11. Current state vocabulary visible to the operator

The UI currently exposes or styles at least these journal/job/item states:

- `PLANNED`
- `SENT`
- `CONFIRMED`
- `VERIFIED`
- `DONE`
- `FAILED`
- `ABORTED`
- `ORPHANED`
- `PAUSED`
- `INCOMPLETE`
- `SKIPPED`

It also presents adjacent operational states that are not the same vocabulary:

- auth `READY` / probing / unavailable;
- read-only capture complete / incomplete / failed;
- full-capture body persisted / not persisted;
- read-back `match` / `drift` / `unread` semantics;
- rate-budget tripped/available;
- running and operator-requested pause;
- GitHub sync/configuration state.

**Design consequence:** Forge Next needs a state model, not merely a palette. Operation context, lifecycle state, result verdict, auth state, persistence state and publication state are different axes and must not be flattened into one set of colored badges.

## 12. Current visual system

The implementation uses a small dark token set:

- canvas near-black;
- one panel surface;
- one border color;
- primary/muted text;
- green success;
- amber warning;
- red failure;
- blue accent/info;
- violet `SENT`/ambiguity.

Components are mostly generic:

- cards;
- rows;
- pills;
- banners;
- buttons;
- fields;
- simple progress bars;
- key/value blocks;
- details disclosures;
- toasts.

The visual system is functional and low-risk, but it has almost no hierarchy for brand, operation mode, content family, review/admin context or desktop composition.

## 13. Mobile ergonomics baseline

### Already good

- mobile-first CSS;
- 44px minimum standard interactive height;
- no hover-only core controls;
- vertical primary content flow;
- scoped overlay can independently scroll;
- technical long values can wrap/break;
- action groups wrap rather than forcing a single horizontal row.

### Current friction

- horizontal navigation grows with destination count;
- long preflight/run screens require substantial vertical scanning;
- critical mode/consequence context can scroll away;
- dense error/reconciliation copy competes with action controls;
- rows often combine long metadata plus actions in one flex layout;
- complex technical states have no dedicated mobile disclosure hierarchy;
- fixed toasts plus long pages can compete for lower-screen attention;
- the shell has no phone-specific bottom navigation or persistent contextual action area.

## 14. Desktop/tablet baseline

The desktop experience is effectively a centered mobile utility widened to `760px`. It does not use horizontal space for simultaneous context, side panels, activity, system health or technical drill-in.

Forge Next therefore has substantial safe room to improve desktop productivity without changing the execution core: a shell/sidebar, main working column, and optional contextual/technical side panel can create hierarchy where the current implementation simply stacks everything.

## 15. Accessibility baseline from source

Positive source-level evidence:

- native buttons, inputs, labels and details are heavily used;
- minimum interactive height is 44px for normal buttons/inputs;
- state is usually written as text, not color alone;
- current page is marked with `aria-current="page"`;
- forms and actions generally remain keyboard-native because the UI uses standard elements.

Open / not proven by this source audit:

- actual contrast ratios across all state combinations;
- focus visibility quality;
- screen-reader announcement behavior for toasts/progress/state updates;
- landmark/heading quality across dynamic rerenders;
- reduced-motion behavior (current UI has little motion, but Forge Next intends more);
- actual viewport behavior on the operator's Android browser.

These should become explicit redesign acceptance checks rather than assumptions.

## 16. High-consequence confusion risks in the current UI

These are not claims that Forge is unsafe; they are UX risks created by density/terminology.

1. **Job state versus item state versus verification verdict.** Several vocabularies appear together and require expert interpretation.
2. **`CONFIRMED` versus `VERIFIED`.** The implementation distinguishes them correctly, but the hierarchy is too subtle for a future broader admin/operator audience.
3. **Capture versus full-capture persistence.** The current copy is accurate, but the product needs a reusable privacy/persistence presentation rather than one-off warning prose.
4. **Recovery actions.** `Adopt`, `Re-send`, `Reconcile & resume`, and `Skip` are correct but need stronger consequence framing and progressive disclosure.
5. **System state versus work result.** Auth, rate budget, GitHub sync, job state and result verdict coexist without a unified status model.
6. **Destructive maintenance.** Evidence deletion, PAT forgetting and journal cleanup are standard danger buttons inside ordinary utility screens, with limited spatial separation.

## 17. What Forge Next should preserve unchanged in meaning

The redesign may change labels/layout after review, but it must preserve these semantic guarantees unless a separately reviewed implementation contract changes the underlying behavior:

- read-only work is visibly distinguished from mutation-capable work;
- full-capture persistence is disclosed separately from read success;
- blocking preflight/auth/image failures disable execution;
- auth is re-evaluated at consequential actions;
- ambiguous `SENT` work is reconciled, not presented as retry-safe;
- `CONFIRMED` is not treated as equivalent to read-back `VERIFIED`;
- incomplete verification remains visibly unverified;
- recovery decisions are explicit and operator-controlled;
- no automatic deletion is introduced;
- evidence/cache deletion explains consequence;
- rate-limit state remains inspectable;
- technical detail remains available even when ordinary surfaces become more human-facing;
- closing/visual restyling must not destroy or contaminate the underlying TNR carrier page.

## 18. Highest-value redesign opportunities established by this audit

These are architecture-neutral opportunities, not final IA decisions:

### A. Introduce a Command Center

Replace the Jobs-first technical landing with a home surface that can show:

- system readiness;
- active/resumable/recovery work;
- recent activity;
- quick safe task entry;
- pending review/admin work where supported.

### B. Separate operation consequence from outcome state

Every consequential workflow needs a persistent human-facing operation context above journal/result details.

### C. Turn manifest preflight into a human job summary

Lead with what will be read/changed/created/uploaded/persisted. Move hash, procedure and raw-key detail behind disclosure.

### D. Promote Recovery to a first-class experience

Do not bury ambiguous writes/orphans among routine history. Provide guided choices with explicit consequence and advanced evidence.

### E. Split research/capture from storage maintenance

Research is an operator task. Cache/snapshot deletion is system/evidence administration.

### F. Use desktop width meaningfully

Permit parallel context — operation summary + work detail + technical/evidence panel — without sacrificing the phone-first flow.

### G. Build a reusable state grammar

The current implementation already proves that one `success/warn/error` scale is insufficient. Forge Next needs orthogonal treatment for mode, lifecycle, outcome, auth, publication and persistence.

## 19. Items deliberately not settled by this audit

The following remain director/planning decisions or transcript-reconciliation questions:

- final navigation model and destination names;
- final content-lane taxonomy;
- exact Command Center composition/order;
- exact operation-mode taxonomy, including the latest board's `Review` mode;
- exact operation-mode palette;
- exact final visual style/degree of flashiness;
- Content Admin permission/action scope;
- final publish UX and confirmation level;
- whether any game-source changes are acceptable;
- Builder deprecation timing.

## 20. Completion statement

Step 1 of the interim Forge UI workflow is complete as a **source-backed current-state baseline**.

No production Forge code was modified. No Fable branch was touched. No browser/live request was made. The next workflow step can now define the architecture-neutral **safety-state presentation contract** against this baseline.