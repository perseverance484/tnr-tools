# Forge Next — Wireframe Anatomy

**Status:** PRE-WIREFRAME STRUCTURE — NOT FINAL IA OR VISUAL DESIGN  
**Date:** 2026-09-12  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Art Director, Engineering Auditor  
**Depends on:** workflow/component map, safety-state presentation contract, mobile/accessibility audit  
**Purpose:** define the information order and reusable regions that future mobile/desktop wireframes must contain, without locking navigation labels, exact tokens, or source-unverified capabilities

## 1. Rules for all future wireframes

Every consequential wireframe should answer, in visible order:

1. **Where am I / what am I doing?**
2. **Does this touch live data or visibility?**
3. **Is anything blocked, uncertain or waiting for recovery?**
4. **What is the main human content/task summary?**
5. **What is the next safe action?**
6. **What is the current progress/result?**
7. **Where is the technical evidence if I need it?**

A wireframe that looks cleaner by omitting any safety-relevant answer is incomplete, not simplified.

## 2. Global shell anatomy

### Desktop/tablet regions

- **Brand / product identity** — compact; TNR-specific but not dominant during work.
- **Primary navigation rail** — destination set still open.
- **Global system health** — auth/session and blockers visible without consuming large space when healthy.
- **Active work indicator** — resumable/running/recovery work remains reachable from anywhere.
- **Main workspace** — human task/content surface.
- **Optional context/evidence region** — technical details, IDs, diffs, procedure/source evidence where useful.

### Phone regions

- **Compact top identity/context** — page/task title and critical state.
- **Main content column**.
- **Bottom primary navigation** — exact destinations open; no horizontal-scroll tab strip.
- **Optional sticky contextual action** — only where it does not cover warnings/status.
- **More/secondary navigation** — low-frequency destinations and diagnostics.

## 3. Command Center anatomy

### Purpose

Answer “Is Forge ready, what needs my attention, and where do I go next?” without making the operator open multiple technical screens.

### Required regions

#### A. Readiness strip

Compact status for:

- TNR session/auth;
- active blocker or rate limit;
- repository/sync readiness where relevant;
- local persistence problem if one exists.

Healthy state stays compact. Any blocker expands with action.

#### B. Resume / Recovery

Highest priority when present:

- running/resumable package;
- `SENT` reconciliation needed;
- incomplete verification;
- orphan decision.

These must appear above ordinary recent activity.

#### C. Quick Actions

Human task entry such as create/build, capture/research, validate/review, or other final IA-approved actions.

Do not use this region to expose every technical screen.

#### D. Content Lanes

Visual lane cards for common content families. Final taxonomy remains open.

#### E. Recent Activity

Human-readable recent runs/captures/reviews with truthful result labels.

#### F. Admin attention

Where supported: pending-review/publish attention count and entry. Do not fabricate counts/state until a durable queue model exists.

### Mobile priority

Order should normally be:

1. urgent resume/recovery;
2. readiness blocker;
3. quick action;
4. content lanes;
5. recent activity;
6. secondary/admin context depending on role/frequency.

## 4. Work package / manifest discovery anatomy

### Primary region

Search/filter + human package cards/rows showing:

- title;
- content/work type;
- operation consequence classification where known;
- entity/item count;
- status: new / ran / resumable / review-ready where durable;
- workstream/package context where available.

### Secondary metadata

Expandable:

- repository path/number;
- manifest hash;
- commit/source provenance;
- raw manifest view.

### Empty/error states

- no matching package → helpful next action;
- repository list failure → explicit repo failure + retry-safe action;
- auth failure should not be shown here unless the list itself genuinely depends on it.

## 5. Preflight anatomy

### Region 1 — Operation header

Must show:

- operation context;
- human title/subject;
- consequence sentence;
- reads/creates/updates/uploads/captures/visibility counts where available;
- auth/readiness state.

### Region 2 — Blocking issues

Only when present:

- validation blockers;
- missing images/files;
- unavailable protected procedure/auth;
- contract/source mismatch discovered before run.

Blockers appear before advisories and before the main action.

### Region 3 — Human change summary

What content is affected and what the package intends to do, without requiring raw payload interpretation.

### Region 4 — Required inputs

Image/file picks or other operator-provided dependencies.

### Region 5 — Advisories

Warnings that deserve reading but do not block.

### Region 6 — Advanced technical detail

Collapsed by default on phone:

- manifest hash;
- entity/op/target IDs;
- dependency order;
- data keys;
- procedure paths;
- raw JSON.

### Region 7 — Primary action

Action wording reflects consequence:

- Run captures
- Start live write
- Begin validation
- other source-backed operation-specific verbs.

No generic `Run` when the consequence materially differs.

## 6. Read-only capture anatomy

### Header

Clearly `READ ONLY` or final equivalent.

### Target summary

Records/procedures/content being inspected.

### Persistence block

Only if relevant:

- summary-only versus full body;
- repository/local persistence consequence;
- privacy classification once architecture supports tiers.

### Progress

Current read phase and counts.

### Results

Per target:

- read succeeded/failed;
- persistence state if requested;
- human identity + advanced raw detail.

### Final summary

State zero mutations explicitly.

## 7. Live-write run anatomy

### Sticky/compact operation header

Retains:

- live-write context;
- subject/package;
- current phase;
- overall counts;
- auth/rate blocker if it emerges.

### Progress summary

Human wording such as:

- preparing;
- sending item N;
- verifying item N;
- paused;
- reconciling.

Do not replace machine states; translate them.

### Item list

Each item shows:

- human name;
- state label;
- concise phase;
- error/diff indicator if present.

IDs/procedure detail remain expandable.

### Pause control

`Pause after this item` or equivalent clearly separated from navigation/close.

### Evidence region

Verification diffs, IDs, full captures, rate budget and raw detail.

### Completion region

Use `ResultSummary`, not merely “100%”.

## 8. Verification-incomplete anatomy

### Dominant state

`Verification incomplete` / final equivalent.

### Explanation

- writes may have landed;
- proof is missing/drifted;
- do not repeat the write;
- re-read is the safe next action.

### Summary

Counts:

- confirmed;
- verified;
- drifted;
- unread;
- failed/skipped.

### Primary action

`Re-read unverified items` or equivalent.

### Evidence

Human diff summary first, raw before/after detail expandable.

## 9. Ambiguous `SENT` recovery anatomy

### Dominant recovery banner/header

Must say:

- a request may have left;
- outcome is not yet known;
- blind retry is unsafe;
- Forge will reconcile first.

### Reconciliation evidence

What Forge checked / what it found.

### Primary action

`Reconcile & resume` only when allowed.

### Technical detail

Journal phase/timestamps/target/procedure available under disclosure.

### Prohibited element

No ordinary `Retry` button.

## 10. Orphan decision anatomy

### Recovery context

What item/create is unresolved and why a human decision is required.

### Candidate section

One candidate per card/row:

- human record name/type;
- relevant identifying context;
- ID copy/detail;
- `Adopt` action.

No default-selected candidate.

### Manual path

Manual ID adoption only when needed; visually secondary to trustworthy candidates.

### Exceptional resend path

Separate section/action, high-consequence wording, explicit target/phase.

### Skip path

Separate from adopt/resend; must state that any live row remains.

## 11. Result summary anatomy

Never reduce final state to one green/red headline.

Answer separately:

### Execution

Did the job finish, pause, abort or remain open?

### Mutation result

Any failed/skipped/unresolved items?

### Verification

Are writes read-back verified, drifted or unread?

### Capture evidence

Did requested full bodies persist?

### Repository sync/export

Did bundle sync/export succeed?

### Publication lifecycle

If relevant, what is the visibility/publish state? This is separate from execution success.

### Next action

Examples:

- Done / return to dashboard;
- re-read unverified;
- resolve recovery;
- export/sync;
- review/publish when separately authorized.

## 12. System health component anatomy

### Compact healthy row

Icon + text + optional short detail.

### Expanded problem state

- system/dependency name;
- what is wrong;
- what work is affected;
- safe remediation;
- technical detail optional.

### Candidate health domains

Only use where real data exists:

- game session/auth;
- rate budget;
- GitHub bridge;
- journal/storage;
- release/build/pin diagnostics where useful.

Do not invent generic `Operational` statuses with no actual signal behind them.

## 13. Content Admin queue anatomy — capability placeholder

Until Fable source audit is frozen, use capability placeholders rather than fake controls.

### Queue card

May contain:

- content title/type;
- review package/workstream source;
- human change summary;
- hidden/published state if source-backed;
- review coordination state if a durable queue model is approved;
- preview availability indicator only if a real preview exists.

### Detail view

- human content preview/detail;
- diff/change summary;
- mechanics/assets metadata relevant to review;
- review disposition;
- advanced execution/provenance detail collapsed.

### Publish area

Render only after source/permission/product policy proves it exists.

## 14. Publish confirmation anatomy — provisional

This component may be designed structurally before exact UX is ruled.

Required fields:

- `Publish` context label;
- content subject and count;
- current visibility → resulting visibility;
- dependency warning where source evidence supports it;
- account/permission readiness;
- statement that action changes live audience visibility;
- cancel;
- explicit publish verb.

Typed-name / hold / two-person confirmation remains user-owned.

## 15. Advanced evidence panel anatomy

Technical evidence should remain consistently accessible across workflows rather than appearing in unrelated formats.

Candidate sections:

- IDs / target IDs;
- manifest path/hash;
- procedure path;
- raw payload;
- journal state/phase/timestamps;
- before/after capture;
- asserted keys;
- verification diffs;
- repository bundle/export metadata;
- source/contract provenance where useful.

On phone this is normally collapsed or a secondary fullscreen/detail view.

## 16. Notification/toast anatomy

Notifications are for transient acknowledgement, not primary safety state.

Good toast cases:

- copied ID;
- settings saved;
- refresh complete;
- safe retry completed;
- new review item available.

Bad toast-only cases:

- `SENT` ambiguity;
- auth refusal that blocks active work;
- verification incomplete;
- orphan decision required;
- publish failure/uncertain result;
- full-capture persistence failure needed for evidence.

Those require persistent in-workflow surfaces.

## 17. Responsive transformation rules

### Desktop → phone

Do not simply stack every desktop region in source order.

Phone priority order is:

1. operation/safety context;
2. blocker/recovery state;
3. human summary;
4. primary action;
5. progress/result;
6. secondary metadata/evidence.

### Side panel behavior

A desktop evidence/context side panel becomes:

- collapsible inline details;
- a sheet/fullscreen detail view;
- or a secondary route/surface with clear return state.

Do not squeeze it beside the main column at phone width.

## 18. Component states every future style prototype must include

A style prototype is incomplete if it only shows ideal success.

At minimum demonstrate:

- normal/healthy;
- disabled/blocking;
- in progress;
- paused;
- warning/advisory;
- failed;
- ambiguous/recovery;
- confirmed but unverified;
- verified;
- mobile focus/selected state;
- destructive confirmation.

## 19. Wireframes that may be produced before transcript completion

Safe to produce as provisional structure:

- Command Center — desktop + phone;
- preflight — read-only + live-write variants;
- active run — desktop + phone;
- verification incomplete;
- `SENT` recovery;
- orphan decision;
- result summary;
- system health;
- generic Content Admin queue/detail with unverified controls visibly placeholders.

Do not freeze exact nav labels, mode colors or final content-lane names in those wireframes yet.

## 20. Wireframe review checklist

For each future wireframe ask:

- Can the user tell whether this can change live data?
- Is ambiguous state visually distinct from failure and success?
- Can the user tell confirmed from verified?
- Is the next safe action obvious?
- Is technical detail available without dominating?
- Does the phone layout preserve consequence before details?
- Are recovery alternatives sufficiently separated?
- Does any depicted control imply a capability/permission not yet proven?
- Can the same component grammar work across content classes?
- Would removing color still leave state understandable?

## 21. Completion statement

Step 8 of the waiting-period Forge UI workflow is complete.

We now have enough architecture-neutral structure to begin actual provisional wireframes later without waiting for the predecessor transcript, while keeping the chronology-sensitive visual/IA decisions unfrozen.