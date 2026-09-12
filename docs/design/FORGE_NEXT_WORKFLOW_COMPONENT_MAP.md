# Forge Next — Workflow-to-Component Map

**Status:** ARCHITECTURE-NEUTRAL DESIGN MAP  
**Date:** 2026-09-12  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Engineering Auditor, Art Director  
**Depends on:** current UI baseline audit, safety-state presentation contract, mobile/accessibility audit, style-board reconciliation  
**Scope:** map real operator/admin workflows to reusable UI component responsibilities without selecting the final top-level IA  
**Out of scope:** production implementation, component framework choice, final navigation labels, final palette, source-permission claims not yet audited by Fable

## 1. Purpose

Forge Next should not be designed as a collection of attractive screens first and then forced onto the execution model.

This map starts from real work:

- inspect/research;
- discover/preflight a manifest;
- perform read-only/full captures;
- perform live writes/uploads;
- monitor/verify;
- recover ambiguous/incomplete work;
- export/sync evidence;
- administer review/publish workflows where source permits.

It then identifies the reusable UI pieces needed to support those workflows consistently.

The result can feed any later IA: operation-oriented, content-oriented, two-axis, or another evidence-backed model.

## 2. Component vocabulary used in this map

### `AppShell`

Persistent product frame: brand, navigation, active work/recovery awareness, global system state and responsive structure.

### `CommandCenter`

Home/continuity surface: current readiness, resumable/recovery work, recent activity, quick task entry and pending review/admin signals where supported.

### `SystemHealth`

Compact truthful status for auth/session, GitHub bridge, storage/journal, rate budget and other source-backed dependencies.

### `OperationHeader`

Persistent human-facing context for the current operation: mode/consequence, subject, counts, readiness and uncertainty.

### `ActionCard`

High-level task entry such as create, capture, validate or resume work.

### `ContentLaneCard`

Human-facing content-family entry with visual identity and examples; final taxonomy remains unresolved.

### `WorkPackagePicker`

Manifest/job/workstream discovery surface. Technical filename/repo details remain available, but human title/type/status should lead.

### `PreflightSummary`

Human summary of what the operation will do before execution.

### `OperationCounts`

Compact reads/creates/updates/uploads/captures/publishes/deletes-style counts where source data supports them.

### `ValidationSummary`

Separates blockers from advisories and links each issue to the affected content/input.

### `DependencyInput`

Required operator-supplied input such as image/file selection or other external asset binding.

### `ConsequenceConfirmation`

Structured confirmation for mutation/publish/recovery/destructive maintenance actions.

### `JobProgress`

High-level phase/progress presentation that does not oversimplify ambiguity.

### `ItemProgress`

Per-item state/timeline with human label first and technical phase/detail available on demand.

### `EvidencePanel`

Read-back, diff, capture body, IDs, procedures, hashes and forensic detail under progressive disclosure.

### `SafetyCallout`

Actionable warning/blocker/recovery explanation with next safe step.

### `RecoveryDecision`

Dedicated ambiguous/orphan decision surface with evidence, candidates and consequence per choice.

### `CapturePersistence`

Shows read result separately from full-body persistence/export status.

### `ResultSummary`

Final truthful statement of execution, verification, evidence persistence, skipped/unresolved work and sync state.

### `ActivityRow`

Recent human-readable work/history entry.

### `AdminReviewCard`

Human content/change summary for authorized review workflows. Capability remains source-dependent.

### `DiffView`

Before/after human change presentation with optional raw detail.

### `PublishControl`

Permission-aware publication action with explicit consequence. Exact implementation is deferred until source feasibility is audited.

### `MaintenanceAction`

Explicit local/system maintenance such as cache invalidation, snapshot deletion, journal cleanup or credential forgetting.

## 3. Workflow A — enter Forge / establish readiness

### User goal

Understand immediately whether Forge is ready for the intended work and whether unfinished work needs attention.

### Current 0.4.0 behavior

- Forge opens into Jobs;
- auth banner is global;
- resumable jobs appear first;
- other health data is mostly in Settings/Run.

### Forge Next component sequence

1. `AppShell`
2. `CommandCenter`
3. `SystemHealth`
4. resumable/recovery `ActionCard` or `ActivityRow`

### Required information

- auth ready/checking/refused;
- active/resumable job count;
- ambiguous/recovery work count;
- rate-budget health where meaningful;
- GitHub sync readiness where relevant;
- local persistence/journal problem if present.

### Design rule

Healthy dependencies may compress. Anything that blocks or makes prior work ambiguous must expand into an actionable state.

## 4. Workflow B — discover/select work

### User goal

Find the package/task/content they intend to operate on without needing to think in repository filenames first.

### Current 0.4.0 behavior

Manifest picker lists `push/*.json`, searchable by filename/number/title.

### Forge Next component sequence

1. `WorkPackagePicker`
2. optional `ContentLaneCard` / workstream context
3. `ActivityRow` for recently used packages
4. advanced repository/source detail disclosure

### Required information

Lead with:

- human title;
- content/work type;
- operation classification where known;
- entity/item count;
- prior run/resume/review status;
- workstream/project association where durable evidence exists.

Keep available but secondary:

- manifest number/path;
- hash;
- repository SHA/source metadata.

### Design rule

Repository identity remains evidence; it stops being the primary human interface.

## 5. Workflow C — manifest/job preflight

### User goal

Answer: “What will happen if I run this, what is blocked, and does it touch production?”

### Current 0.4.0 behavior

Selected manifest card contains counts, hash, capture warnings, validation errors, auth blocks, advisories, per-item technical summaries and image picks.

### Forge Next component sequence

1. `OperationHeader`
2. `PreflightSummary`
3. `OperationCounts`
4. `ValidationSummary`
5. `DependencyInput` list
6. human content/item summary
7. advanced `EvidencePanel` for hash/procedures/keys/dependencies
8. `ConsequenceConfirmation` when execution is consequential

### Required decision hierarchy

1. operation consequence;
2. blockers;
3. required user input;
4. what records/content are affected;
5. technical detail.

### Design rule

A user should not have to interpret `keys:` or procedure paths to understand the live consequence.

## 6. Workflow D — ordinary read-only capture/research

### User goal

Read/research live data with zero mutations.

### Component sequence

1. `OperationHeader` — read-only context
2. query/target selector or `WorkPackagePicker`
3. `PreflightSummary`
4. lightweight execution confirmation only where useful
5. `JobProgress`
6. capture/result list
7. `ResultSummary`
8. optional export/sync action

### Design rule

Read-only work should feel materially safer and faster than write work, but still disclose protected/auth requirements and persistence/export consequences.

## 7. Workflow E — full capture with repository-persisted evidence

### User goal

Perform zero-mutation reads while persisting exact record bodies for evidence/review.

### Component sequence

1. read-only `OperationHeader`
2. `CapturePersistence` preflight disclosure
3. `OperationCounts`
4. run action
5. `JobProgress`
6. post-run `CapturePersistence` showing read vs body persistence separately
7. `ResultSummary`
8. repository sync/export state

### Required wording

Before run, communicate both:

- zero mutations;
- exact record bodies may be written into a bundle/repository when sync is enabled.

After run, never let `read succeeded` stand in for `body persisted`.

## 8. Workflow F — live write/update/create

### User goal

Apply an approved mutation package safely and verify it.

### Component sequence

1. live-write `OperationHeader`
2. `PreflightSummary`
3. `OperationCounts`
4. `ValidationSummary`
5. `DependencyInput`
6. `ConsequenceConfirmation`
7. `JobProgress`
8. `ItemProgress`
9. verification `EvidencePanel`
10. `ResultSummary`
11. sync/export state

### Required persistent context

While running, keep visible/recoverable:

- this is live mutation;
- current phase;
- pause capability;
- auth/rate blocker if it appears;
- whether work is confirmed versus verified.

### Design rule

The “happy path” does not end at server acknowledgement. Verified read-back is the strongest success state.

## 9. Workflow G — file/image upload dependency

### User goal

Supply local assets required by a planned operation and know which files are still missing.

### Current 0.4.0 behavior

Each referenced image has a `Pick` control; missing images block execution.

### Component sequence

1. `DependencyInput` group
2. file/asset identity + requirement reason
3. selected/missing state
4. optional thumbnail/metadata where safe/useful
5. blocker integration into `ValidationSummary`

### Design rule

Missing external input is a preflight blocker, not a runtime surprise.

## 10. Workflow H — active execution / pause

### User goal

Monitor work, understand current phase and stop safely when needed.

### Component sequence

1. sticky/compact `OperationHeader`
2. `JobProgress`
3. `SafetyCallout` for auth/rate/session issues
4. `ItemProgress`
5. `Pause after this item` or equivalent safe pause action
6. `EvidencePanel` secondary

### Design rule

Do not overload the progress bar with state meaning. Phase text and explicit state labels remain authoritative.

## 11. Workflow I — verification incomplete / drift

### User goal

Understand that writes may have landed but proof is incomplete, and gather the missing evidence without re-sending them.

### Component sequence

1. `OperationHeader` retaining original write context
2. high-attention `SafetyCallout`: `Verification incomplete`
3. `ResultSummary` showing confirmed/unverified counts
4. `DiffView` / unread evidence
5. primary `Re-read / verify` action
6. technical `EvidencePanel`

### Design rule

The primary action must read like a read/evidence operation, never a retry of the mutation.

## 12. Workflow J — ambiguous `SENT` reconciliation

### User goal

Resolve a request that may have left the device without double-sending.

### Component sequence

1. recovery `OperationHeader`
2. dominant `SafetyCallout`: request state ambiguous
3. `RecoveryDecision`
4. reconciliation evidence/results
5. only then `Reconcile & resume`
6. technical journal/phase detail under `EvidencePanel`

### Design rule

No generic `Retry`. `SENT` ambiguity must be visually and verbally distinct from failure.

## 13. Workflow K — orphan resolution

### User goal

Decide how to proceed when reconciliation cannot confidently identify a single live result.

### Component sequence

1. recovery `OperationHeader`
2. `RecoveryDecision` explanation
3. candidate record cards
4. `Adopt` path
5. exceptional `Re-send phase` path where valid
6. `Skip` path
7. `ConsequenceConfirmation` per high-risk choice
8. `EvidencePanel`

### Design rule

Candidate evidence and consequences lead. Raw IDs remain available but should not be the only differentiator.

## 14. Workflow L — auth/session interruption

### User goal

Recover from a signed-out/refused session without mistaking it for content failure.

### Component sequence

1. global `SystemHealth` changes state
2. operation-local `SafetyCallout`
3. blocked Resume/execution action
4. `Re-check session` action
5. sign-in/reopen instructions
6. continuation/reconciliation after readiness returns

### Design rule

Authentication refusal, authorization denial and content/procedure failure must not collapse into the same error message.

## 15. Workflow M — rate-limit pause

### User goal

Understand why work paused and when it is safe to continue without hammering the limiter.

### Component sequence

1. `SystemHealth` rate status
2. operation-local `SafetyCallout`
3. reset countdown where known
4. disabled/withheld Resume until allowed by the runner/budget state
5. detailed per-path budget in `EvidencePanel`

### Design rule

Do not encourage repeated manual retries while rate-limited.

## 16. Workflow N — result/export/repository sync

### User goal

Know whether the game work is verified and whether the resulting evidence was successfully exported/synced.

### Component sequence

1. `ResultSummary`
2. verification counts/outcome
3. capture persistence state
4. skipped/unresolved disclosure
5. repository sync/export state
6. `ActivityRow` entry/history
7. advanced raw bundle access

### Design rule

Game outcome and repository sync are separate claims. A verified write with failed sync is not the same problem as an unverified write with successful bundle export.

## 17. Workflow O — capture/evidence maintenance

### User goal

Manage local cache/evidence without accidentally deleting the wrong class of data.

### Component sequence

1. maintenance/diagnostics context
2. separate cache and snapshot sections
3. `MaintenanceAction` per class
4. consequence confirmation for evidence deletion
5. storage size/age metadata

### Design rule

`Invalidate cache` and `Delete evidence snapshot` are not interchangeable destructive actions.

## 18. Workflow P — settings/diagnostics

### User goal

Configure repository sync or diagnose system state without wading through ordinary workflow screens.

### Component sequence

1. Settings shell section
2. GitHub bridge configuration
3. system/session diagnostics
4. journal/export tools
5. local maintenance actions

### Design rule

Routine health summaries should surface elsewhere. Settings can carry raw/advanced detail.

## 19. Workflow Q — Content Admin review (source-feasibility pending)

### Intended user goal

Review human-facing content/change packages without understanding runner internals.

### Candidate component sequence

1. admin-aware `AppShell` / queue entry
2. `AdminReviewCard`
3. content detail/preview
4. `DiffView`
5. review disposition controls
6. permission/readiness `SystemHealth`
7. publication control only when source/role permits
8. final result/read-back summary

### Required separation from operations

Admin-facing default view should emphasize:

- what content is being reviewed;
- what changed;
- player-facing/mechanical preview;
- review status;
- publication status.

Manifest procedures, journal phases, hashes and raw payloads remain advanced evidence, not prerequisite knowledge.

### Evidence warning

The exact queue model, edit capability, preview support, permission roles and publish procedures require Fable's pinned game-source audit. This map does not invent them.

## 20. Workflow R — publish/unpublish (capability pending)

### Intended user goal

Make approved content audience-visible through an authorized account.

### Candidate component sequence

1. publish-context `OperationHeader`
2. permission/readiness status
3. human content/change summary
4. `ConsequenceConfirmation`
5. explicit `Publish`/`Unpublish` action
6. progress/result
7. read-back/publication state verification
8. audit/history entry

### Design rule

Publishing is a content lifecycle action and must not be conflated with technical mutation success.

## 21. Cross-workflow component matrix

| Component | Home | Preflight | Read | Full Capture | Write | Run | Recovery | Admin | Settings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AppShell | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| CommandCenter | ✓ |  |  |  |  |  |  |  |  |
| SystemHealth | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| OperationHeader |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | context-dependent |  |
| WorkPackagePicker | quick entry | ✓ | optional | optional | ✓ |  |  | queue/package source |  |
| PreflightSummary |  | ✓ | ✓ | ✓ | ✓ |  |  | edit/publish preflight |  |
| OperationCounts | summary | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | publish/review counts |  |
| ValidationSummary | blockers | ✓ | optional | optional | ✓ |  |  | edit blockers |  |
| DependencyInput |  | ✓ |  |  | ✓ |  |  | maybe |  |
| ConsequenceConfirmation |  | before run | light/optional | persistence-specific | ✓ |  | per decision | ✓ | destructive only |
| JobProgress | activity |  | ✓ | ✓ | ✓ | ✓ | reconciliation progress | action progress |  |
| ItemProgress |  | summary | optional | optional | ✓ | ✓ | ✓ | advanced |  |
| SafetyCallout | blockers | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| RecoveryDecision | recovery alert |  |  |  |  |  | ✓ |  |  |
| CapturePersistence |  | ✓ |  | ✓ | if captures | ✓ | evidence | maybe | maintenance |
| ResultSummary | activity |  | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |  |
| EvidencePanel | optional | advanced | advanced | advanced | advanced | ✓ | ✓ | advanced | diagnostics |
| DiffView |  | optional |  |  | preflight if live diff exists | verification | reconciliation | ✓ |  |
| ActivityRow | ✓ |  |  |  |  |  |  | ✓ |  |
| MaintenanceAction |  |  |  |  |  |  |  |  | ✓ |

## 22. Components that should exist before final IA is settled

The following component contracts are sufficiently cross-cutting that design/prototyping can proceed before Fable settles top-level navigation:

- `SystemHealth`
- `OperationHeader`
- `PreflightSummary`
- `OperationCounts`
- `ValidationSummary`
- `SafetyCallout`
- `ConsequenceConfirmation`
- `JobProgress`
- `ItemProgress`
- `RecoveryDecision`
- `CapturePersistence`
- `ResultSummary`
- `EvidencePanel`
- `DiffView`
- `ActivityRow`

`AppShell`, `CommandCenter`, navigation and exact `ContentLaneCard` taxonomy should remain more loosely specified until IA evidence and transcript chronology are complete.

## 23. Components that must not invent capability

These visual components are especially prone to implying more than source/permissions prove:

### Mode selector

Must not imply that choosing `Publish` or `Write` grants permission or changes manifest capability.

### PublishControl

Must not render as enabled merely because content is ready visually; source procedure + account authorization + product policy must permit it.

### AdminReviewCard

Must not invent an approval state that has no durable backing store.

### Preview

Must not claim fidelity if the game has no source-backed preview/render path for that content class.

### DiffView

Must distinguish repository/package intent from fresh live-state evidence; stale cached data cannot silently masquerade as current live state.

## 24. Phone composition pattern derived from the map

For consequential work, a stable phone anatomy can be designed before final IA:

1. compact shell/navigation;
2. operation context;
3. blocking/uncertain state;
4. human task/content summary;
5. primary action;
6. progress/results;
7. advanced evidence/details.

This order should survive content type changes.

## 25. Desktop composition pattern derived from the map

A useful desktop anatomy is:

- persistent navigation/shell;
- main work column;
- persistent/nearby operation/status context;
- optional secondary evidence/details panel;
- recovery decisions promoted above routine activity.

This is a component-placement principle, not a final screen grid.

## 26. Next design artifacts enabled by this map

Without waiting for the predecessor transcript, we can now safely create architecture-neutral wireframe/component anatomy for:

1. Command Center summary blocks;
2. manifest preflight;
3. read-only/full-capture run;
4. live-write run;
5. verification-incomplete state;
6. ambiguous `SENT` recovery;
7. orphan decision card;
8. generic admin review card with source-dependent controls clearly marked;
9. result summary;
10. system-health treatment.

The final shell destination set and mode colors can be applied after transcript/Fable reconciliation without redesigning these underlying components.

## 27. Completion statement

Step 6 of the interim Forge UI workflow is complete.

The redesign now has a workflow-derived component vocabulary tied back to real Forge safety semantics. This reduces the risk that the final UI becomes a visually polished layer that cannot faithfully represent the runner/journal/recovery model.