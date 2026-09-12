# Forge Next — Screen Content Requirements

**Status:** DESIGN REQUIREMENTS — ARCHITECTURE-NEUTRAL / NAVIGATION-AGNOSTIC  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** `FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`, `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`, `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md`, `FORGE_NEXT_WIREFRAME_ANATOMY.md`  
**Implementation evidence baseline:** Forge `0.4.0`, `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Engineering Auditor, Content Designer  
**Scope:** what each major Forge Next surface must help the user understand and do  
**Out of scope:** final route names, final nav destinations, final token palette, final operation-mode taxonomy, backend architecture, Content Admin permission decisions

## 1. Purpose

This document specifies **screen content obligations**, not a final sitemap.

Fable may ultimately group, rename, split, or combine these surfaces. Whatever information architecture is chosen, the resulting product must still provide the user-facing capabilities and information below.

The central rule is:

> A screen is complete only when the user can understand consequence, current evidence, blockers, and the next safe action without opening raw JSON or guessing from color.

## 2. Global shell obligations

Every consequential Forge surface must have access to the following context even if some of it is collapsed:

- current Forge/build identity;
- authentication/session readiness;
- current operation consequence when an actionable workflow is active;
- active/resumable/recovery work indicator;
- clear path back to a safe overview;
- visible indication when something requires operator attention;
- access to technical detail without forcing it into the primary reading path.

### Mobile priority

At phone width, persistent space is scarce. Preserve in this order:

1. page/task identity;
2. current consequence/state;
3. blocking issue or ambiguity;
4. primary safe next action;
5. supporting counts/metadata;
6. raw/technical detail behind disclosure.

### Desktop/tablet priority

Use horizontal space to keep independent context visible at the same time. Do not simply stretch phone cards to full width.

## 3. Command Center / home surface

### Questions it must answer

- Can Forge safely operate right now?
- Is anything active, paused, incomplete, ambiguous, or awaiting recovery?
- What work needs attention?
- What did I recently do?
- What is the shortest path to common work?

### Required content blocks

#### Readiness summary

Must distinguish at least:

- TNR session/auth readiness;
- repository/GitHub readiness where relevant;
- rate-budget condition;
- storage/journal health;
- any source/contract drift blocker Fable ultimately exposes.

Readiness must not collapse all failures into one generic red status.

#### Active and resumable work

Show open jobs before ordinary recent history when any exist.

For each active/resumable job, expose:

- human-readable job/manifest identity;
- operation consequence;
- current job state;
- ambiguity/recovery requirement when applicable;
- what Resume actually does (`continue`, `reconcile`, or `re-read`);
- age/last activity.

#### Attention queue

May include, once source-backed:

- `SENT` items requiring reconciliation;
- orphans requiring a decision;
- incomplete verification;
- missing required files/assets;
- failed sync/export;
- pending review/admin work.

Do not merge all of these into a generic notification count if their safe next actions differ.

#### Quick actions

Quick actions are allowed only for capabilities that exist and are safe to expose. Each action should state its goal in human language, not procedure terminology.

Examples of directionally valid labels include research/capture, open work package, create/build, review/recovery, and content administration. Exact destinations remain an IA decision.

#### Recent activity

Recent activity should summarize what happened in operator language:

- subject;
- action;
- time;
- evidence/outcome;
- publication state where relevant.

A row that merely says `job DONE` is insufficient.

### Empty state

A first-use dashboard may use branded/atmospheric art. It must still provide a concrete first action and explain what Forge is for.

## 4. Work discovery / package selection surface

This obligation currently corresponds partly to `Manifests`, but Forge Next should treat the selected object as a work package/job rather than exposing repository mechanics first.

### Questions it must answer

- What package am I looking at?
- Where did it come from?
- Has it already run?
- What kind of work does it contain?
- Is it safe/ready to inspect further?

### Required capabilities

- search/filter by human title and repository identity;
- distinguish recent/unrun/already-run where evidence supports it;
- show item/read/capture/write counts without opening the package;
- expose provenance/path/hash in advanced detail;
- show loading/listing failures without losing already loaded work;
- permit refresh without implying live-game mutation.

### Mobile behavior

Search and highest-value filters must remain immediately usable. Dense repository metadata should not force horizontal scrolling.

## 5. Preflight surface

Preflight is the most important prevention surface in Forge Next.

### Questions it must answer before the action button

- Is this read-only, mutation-capable, publish-capable, or recovery work?
- What exactly will be read, changed, created, uploaded, persisted, or published?
- What blockers exist?
- What warnings/advisories exist?
- Are required files present?
- Is authentication/authorization sufficient?
- Does full capture create repository-persisted evidence?
- What will the primary action do?

### Required information hierarchy

1. operation consequence label and one-sentence consequence;
2. blocking errors;
3. compact counts (`reads`, `writes`, `creates`, `captures`, `uploads`, `publishes` as applicable);
4. warnings/advisories;
5. required asset/file readiness;
6. item-by-item summary;
7. technical details/procedure paths/hash behind disclosure;
8. explicit primary action.

### Action wording

Avoid generic `Run`, `Continue`, or `Submit` for high-consequence paths when a more specific verb fits.

Examples:

- `Run captures`
- `Start live write`
- `Verify again`
- `Reconcile before continuing`
- `Publish content`

### Prohibited simplifications

- a single green `Ready` badge that hides warnings;
- equating zero validation errors with permission/auth readiness;
- making a full capture look identical to a summary capture;
- allowing a live-write action before the consequence summary is visible.

## 6. Running / execution surface

### Questions it must answer

- What is running?
- What phase is active?
- What has definitely happened?
- What is still uncertain?
- Can I safely leave/pause?
- What happens next?

### Required content

#### Persistent operation context

The consequence mode stays visible during execution.

#### Progress

Progress must separate terminally resolved items from unresolved items. A progress bar reaching 100% must not automatically imply verification success.

#### Active phase

When known, show human language for the active phase: preparing, reading, uploading, sending, waiting for response, verifying, reconciling, exporting/syncing.

#### Item list

Each item should expose:

- name/type;
- lifecycle state;
- phase when relevant;
- evidence status;
- safe drill-down for IDs/diffs/errors.

#### Pause

If pause is supported only between items, the button and helper text should say so (`Pause after this item`).

#### Rate/system context

Rate-budget health and authentication state must remain available while work runs because either can change the next safe action.

## 7. Completion / result surface

### Questions it must answer

- Did every intended action happen?
- Is the result verified, failed, or unverified?
- Did requested evidence persist successfully?
- What remains to do?
- Was the result synced/exported?

### Required summary categories

Preserve the current conceptual distinction between:

- success/verified;
- failed;
- unverified/incomplete;
- open.

### Verified completion

A strong success treatment is permitted only when the relevant asserted writes read back correctly and requested evidence obligations are satisfied.

### Unverified completion

Must state explicitly that the writes are **not proven** and make the next safe action a read/reverification path rather than resend.

### Capture-only completion

Must separately report:

- reads succeeded/failed;
- requested full bodies persisted/not persisted;
- zero mutations sent.

### Export/sync

Repository sync success is a separate claim from live-game verification. The UI must not collapse the two.

## 8. Recovery overview surface

Recovery is a first-class workspace obligation even if Fable ultimately nests it under Jobs.

### Questions it must answer

- What is uncertain or interrupted?
- Why is it here?
- What is known to have left the device?
- What must happen before ordinary execution may resume?
- What decisions require the operator?

### Required grouping

Separate at least:

- ambiguous `SENT` work needing reconciliation;
- orphan decisions;
- paused jobs with recoverable causes;
- incomplete verification that only needs reads;
- authentication-blocked work;
- rate-limited work.

Their actions are different and should not be flattened into one `Resume all` model.

## 9. `SENT` reconciliation detail

### Required message structure

1. **What we know:** the request must be treated as having left the browser.
2. **What we do not know:** whether the intended live effect occurred.
3. **What Forge will do next:** reconcile/read before any resend.
4. **What the user must not do:** do not blindly retry.

### Required action

Primary action wording should make reconciliation explicit, e.g. `Reconcile` or `Reconcile & resume`.

Never present an ordinary `Retry` button for `SENT`.

## 10. Orphan-resolution detail

### Questions it must answer

- Which item is ambiguous?
- What phase created the ambiguity?
- Which candidate records exist, if any?
- What does adopting each candidate mean?
- What does Skip leave behind?
- Is any resend path being offered, and why is it safe?

### Interaction requirements

- no preselected candidate;
- IDs available without dominating the card;
- candidate names/metadata shown when present;
- `Adopt`, `Skip`, and any resend action visually and verbally distinct;
- confirmation describes the concrete consequence;
- Skip must say that a possible live row may remain.

## 11. Capture / evidence library

Current Forge mixes read cache and immutable full-capture snapshots in one `Captures` screen. Forge Next may reorganize this, but must preserve the distinction.

### Read-cache obligations

Explain that deleting/invalidation:

- discards cached reads;
- may cost rate budget on the next read;
- does not by itself delete live content.

### Full-capture snapshot obligations

Explain that deleting a snapshot:

- destroys exact evidence used for bundle export;
- may make an unexported bundle incomplete;
- cannot be undone locally;
- may require another game read to reconstruct.

The destructive action must therefore be more deliberate than ordinary cache invalidation.

### Privacy/persistence note

Once Fable finalizes capture-classification architecture, this surface must clearly identify whether data is repo-safe, local-only, projected, or another approved category. Do not implement that taxonomy from this document alone.

## 12. Content Admin queue — provisional obligation

**Maturity:** product requirement exists; exact source model and permissions remain Fable/user decisions.

### Questions it should answer

- What is awaiting human review?
- What changed?
- What content type/status is it?
- Who/what initiated the change if evidence exists?
- What is the next admin decision?

### Required row/card content

- human-facing content title;
- content class;
- lifecycle/visibility state;
- review state once a canonical coordination model is chosen;
- concise change summary;
- relevant age/provenance;
- clear entry to review detail.

Do not show raw manifest path as the primary title.

## 13. Content Admin detail / edit — provisional obligation

### Required hierarchy

1. content identity and current visibility/lifecycle;
2. human-facing preview/summary;
3. what changed;
4. editable permitted fields;
5. validation and dirty state;
6. history/provenance;
7. publish/approval actions separated from ordinary edits;
8. raw/technical data behind advanced disclosure.

### Editing rules

- editable and read-only fields must be visually distinguishable;
- dirty/changed state must not use semantic error red;
- whole-record write implications must not be hidden if relevant to the final adapter architecture;
- permission refusal and authentication failure need separate messages;
- save/edit success is not equivalent to published.

## 14. Publish / visibility change — provisional obligation

Publishing is a separate high-consequence surface or deliberate action state even if invoked from content detail.

### Before confirmation, show

- record/content name;
- current visibility state;
- target visibility state;
- dependency/readiness warnings supported by evidence;
- exact number of records affected;
- who will be able to see/use the content after the change in plain language where source evidence supports that claim.

### After action, show

- server/action result;
- read-back/verification result;
- final visibility state;
- any repository/audit sync status separately.

Never show `Published` merely because the mutation request was sent.

## 15. Settings / diagnostics

### Ordinary settings

Human-facing controls should include only things an operator may reasonably need to change.

### Diagnostics

Technical information belongs in a distinct section:

- build/version;
- session/auth detail;
- rate-budget configuration/status;
- storage persistence status;
- source/pin/contract information where useful;
- GitHub sync/configuration;
- exportable diagnostic/journal data.

### Credential handling

Any future credential UX must follow repository rulings and Fable's architecture decision. This document does not authorize new credential storage.

## 16. Notification and global-attention obligations

A transient toast is appropriate for low-consequence acknowledgement such as `Copied`.

A toast is **not enough** for:

- failed live write;
- ambiguous write;
- authentication blocking an active job;
- verification drift;
- failed full-capture persistence;
- failed publish/read-back;
- lost/deleted required evidence.

Those states must remain visible on the relevant durable surface until resolved or explicitly dismissed where safe.

## 17. Raw/advanced detail obligations

Progressive disclosure is required, not technical erasure.

Advanced detail should make available as appropriate:

- record IDs;
- manifest path/hash;
- procedure paths;
- lifecycle phase;
- raw validation/error detail;
- before/after or asserted/live diffs;
- journal information;
- capture snapshot keys;
- source/pin/build metadata.

Ordinary users should not need these to decide the normal next action.

## 18. Cross-surface consistency rules

- The same lifecycle state uses the same core label everywhere.
- The same operation consequence uses the same human wording everywhere.
- `Verified` means evidence-backed verification, never merely `request succeeded`.
- `Published` describes content visibility/lifecycle, never transport success.
- `Retry` is never used for an ambiguous `SENT` mutation.
- `Resume` must explain when it means reconcile or re-read rather than ordinary continuation.
- Destructive evidence deletion must never visually resemble cache refresh/invalidation.
- Authentication failure and authorization denial remain distinct.

## 19. Transcript-sensitive items deliberately left open

The predecessor-chat export may still change:

- final navigation labels/destination count;
- final operation-mode taxonomy, including whether `Review` is a mode or a workflow category;
- exact visual hierarchy/tokens;
- final content-lane labels;
- exact Content Admin action scope and publish confirmation model.

Nothing in this document settles those items.

## 20. Use by Fable

Fable may cite this file as a **UI content-requirements input**, not as an architecture decision.

If Fable's source deep dive proves that a required block has no truthful data source or that a different grouping is safer, surface the disagreement explicitly. Do not fabricate data merely to satisfy the mockup.
