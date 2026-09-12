# Forge Next — Interaction Risk Matrix

**Status:** DESIGN-SAFETY CONTRACT — ARCHITECTURE-NEUTRAL  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`, `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`, repository doctrine/workflows  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Engineering Auditor  
**Scope:** confirmation, friction, action wording, and evidence requirements by consequence class  
**Out of scope:** granting permissions, adding procedures, final Content Admin scope, deleting live content, final publish workflow

## 1. Purpose

Forge Next should reduce operator friction without flattening all actions into the same interaction pattern.

This matrix provides a UX classification for **how deliberate an action must feel** and **what evidence the UI must present** before and after it.

It does not replace backend authorization, manifest validation, journaling, reconciliation, or user-owned publishing authority.

## 2. Principle: friction follows consequence and ambiguity

Confirmation should not be proportional to how technically complicated an operation is. It should be proportional to:

- external side effects;
- reversibility;
- possibility of duplicate effects;
- visibility/publication consequence;
- destruction of evidence;
- ambiguity in whether an earlier action landed;
- scope (one record vs many);
- whether the UI can prove the current state.

A low-risk read should be fast. A high-risk write should be explicit. A recovery action may need more explanation than either because the system is uncertain.

## 3. Interaction classes

These are UX classes, not permission classes.

### R0 — passive/local navigation

Examples:

- open a detail view;
- expand technical details;
- filter/search local data;
- switch tabs/workspaces;
- copy an ID.

**Default:** no confirmation.

**Feedback:** immediate state change; lightweight toast allowed for copy acknowledgements.

### R1 — reversible local/UI state

Examples:

- change sort/filter preferences;
- dismiss a non-critical panel;
- select/deselect a local file before execution;
- invalidate an ordinary read-cache entry when the consequence is clearly local.

**Default:** no blocking confirmation unless the action discards meaningful unsaved work.

**Feedback:** inline acknowledgement; undo preferred when practical.

### R2 — external read / inspection

Examples:

- refresh a repository listing;
- send an ordinary game read/capture query;
- re-read an unverified item;
- probe authentication readiness.

**Default:** usually no modal confirmation.

**Pre-action requirement:** operation context must make clear that the action is read-only when that claim is true.

**Post-action requirement:** show read success/failure without suggesting mutation occurred.

**Exception:** a read with special persistence/privacy consequences may move to R3.

### R3 — evidence/persistence consequence

Examples:

- run a full capture whose exact body will be persisted into a results bundle;
- delete immutable full-capture evidence;
- enable/trigger repository result sync;
- export protected/local-only evidence if a future approved architecture permits it.

**Default:** consequence summary before action. Confirmation required when evidence is destroyed or persistence expands beyond the local cache.

**Required wording:** name where the data will live or what evidence will be lost.

### R4 — live mutation

Examples:

- create a live content record;
- update an existing live content record;
- upload/associate an asset when the operation has live effects;
- resume a job that is about to send a not-yet-sent mutation.

**Default:** one clear confirmation surface after preflight, provided the machine state is not ambiguous.

**Pre-action requirements:**

- explicit `live`/production consequence;
- record/item count;
- creates vs updates where useful;
- blockers resolved;
- authentication/authorization readiness;
- no unresolved `SENT` state bypassed.

**Post-action requirements:** distinguish sent, confirmed, and verified.

### R5 — audience visibility / publication

Examples:

- hidden → visible/published;
- published → hidden/unpublished;
- package-level publication if later authorized.

**Default:** deliberate confirmation that names the content and visibility change. Multi-record publication requires stronger scope presentation than single-record publication.

**Pre-action requirements:**

- current visibility;
- target visibility;
- records affected;
- dependency/readiness warnings supported by evidence;
- explicit publish/unpublish verb.

**Post-action requirements:** mutation result plus read-back/final visibility. `Published` may only be shown as a final state once evidence supports it.

### R6 — destructive live action

Examples only if later source-verified and explicitly authorized:

- delete a live record;
- bulk destructive operation.

**Default:** strongest confirmation class. No implementation is authorized by this document.

**Requirements if ever designed:** explicit record identity, irreversible consequence, scope count, permission check, and source-backed recovery story (or explicit statement that none exists).

### RX — ambiguity/recovery decision

Examples:

- reconcile a `SENT` mutation;
- adopt an orphan candidate;
- skip an unresolved orphan;
- resend a later phase only where the state machine proves it is safe.

RX is orthogonal to R0–R6. It exists because the risk comes from **uncertainty**, not merely from the action's normal side effect.

**Default:** dedicated recovery presentation, not a generic confirmation modal.

**Requirements:**

- what is known;
- what is uncertain;
- what will be read/sent next;
- why the offered action is safe;
- what remains if the user skips.

## 4. Current action matrix

| Action | UX class | Default confirmation | Required pre-action language | Required post-action evidence |
| --- | --- | --- | --- | --- |
| Open screen/detail | R0 | none | none | immediate navigation |
| Copy ID/hash | R0 | none | none | `Copied` acknowledgement |
| Search/filter | R0 | none | none | visible filtered state |
| Select local image | R1 | none | required filename/slot | picked/missing state |
| Invalidate ordinary read cache | R1 | usually none; confirm for bulk clear | `Next read will use rate budget again` | cache state updated |
| Clear entire read cache | R1/R3 boundary | confirm | cache-only consequence; no live deletion | count/cache cleared |
| Probe/re-check auth | R2 | none | `Checks session readiness` | ready/not confirmed/refused |
| Refresh repo manifest list | R2 | none | repo read context | loaded/error with previous usable state retained where practical |
| Run summary capture | R2 | concise preflight action | `Read only · zero mutations` | read success/failure |
| Run full capture | R3 | consequence confirmation in preflight | exact body persists to bundle/repo when sync applies | read verdict + persistence verdict separately |
| Delete one full-capture snapshot | R3 | confirm | exact evidence will be lost | snapshot deleted; affected job/export consequence visible |
| Delete all snapshots | R3 high | strong confirm | scope count/bytes if available; unexported evidence risk | deletion result |
| Export bundle | R3 | usually no confirmation when export is local/read-only; architecture may raise class | destination/data class visible | export generated/failed |
| Auto-commit results to repo | R3 | setting enable/credential flow deliberate; each known-safe sync need not modal-confirm | public-repo/persistence consequence | commit/sync result distinct from live verification |
| Start live create/update job | R4 | yes | `Live write`, item/create/update counts, blockers | sent/confirmed/verified lifecycle |
| Upload asset as part of live work | R4 | covered by package confirmation if scope clearly includes uploads | upload count/destination role | upload result + associated record verification where applicable |
| Pause after current item | R1 operational | none | `Pause after this item` | paused reason/state |
| Resume ordinary paused job | R2 or R4 depending next phase | no second modal if consequence already clear and state proves next step; primary label must be specific | what Resume will do next | state progression |
| Re-read incomplete verification | R2 | none | `Re-read only · will not resend write` | match/drift/unread |
| Reconcile `SENT` | RX | dedicated recovery action | `Request may have landed; reconcile before resend` | reconciled outcome/candidates |
| Adopt orphan candidate | RX/R4 | confirm | candidate ID/name and continuation consequence | adopted state then subsequent verification |
| Skip orphan | RX | confirm | possible live row remains; nothing deleted | skipped state, unverified overall outcome |
| Safe later-phase resend after explicit recovery proof | RX/R4 | confirm | exact phase and why resend is safe | sent/confirmed/verified lifecycle |
| Save ordinary local form draft | R1 | none | local-only if true | dirty/saved-local state |
| Save Content Admin edit to hidden live record (if authorized) | R4 | confirmation level depends approved adapter policy | record + changed fields + live consequence | read-back verified/unverified |
| Publish/unhide one record | R5 | yes | record name, current→target visibility | read-back final visibility |
| Publish package/multiple records | R5 high | stronger scope confirmation | package name, count, per-class/dependency warnings | per-record result + aggregate state |
| Delete live record | R6 | not currently authorized | future explicit destructive contract | source-backed read-back/audit if ever allowed |

## 5. Confirmation design rules

### 5.1 Confirmation is not a substitute for preflight

A confirmation should summarize an already understandable action. It should not be the first place the user learns that the action writes to production.

### 5.2 Confirmation must name the verb

Prefer:

- `Start live write`
- `Delete snapshot`
- `Adopt record`
- `Skip unresolved item`
- `Publish content`

Avoid generic labels such as:

- `OK`
- `Yes`
- `Continue`
- `Submit`

for high-consequence actions.

### 5.3 Confirmation must name scope

When more than one object is affected, state the count. When the count is heterogeneous, include the most decision-relevant breakdown.

Example pattern:

`3 records · 1 create · 2 updates · 2 full captures`

### 5.4 Confirmation must describe the irreversible part

Examples:

- live records will be created/updated;
- content will become visible to players;
- exact capture evidence will be deleted;
- a possible unresolved live row will be left in place.

### 5.5 Confirmation fatigue is a safety defect

Do not require repetitive modals for low-risk reads or each item of a package that the user has already reviewed as one coherent live-write operation. Excess confirmations train users to dismiss them.

Use one meaningful package-level confirmation where state and scope permit it, then reserve new confirmations for newly introduced consequences or ambiguity.

## 6. Button hierarchy rules

### Primary

One primary action per decision region. It should represent the safest expected forward action.

### Secondary

Use for inspection, cancel/back, or alternate safe paths.

### Destructive

Destructive styling is reserved for actual destructive/local-evidence removal/refusal actions, not every live write.

### Recovery

Recovery actions need their own contextual treatment. Do not style `Reconcile` as if it were ordinary `Run again`.

### Publish

Publish may have a dedicated operation-mode treatment but must remain distinct from semantic success and destructive error colors.

## 7. Disabled-action rules

A disabled button must have an understandable blocker nearby.

Do not make the user infer why `Start`, `Resume`, or `Publish` is disabled.

Common blocker classes include:

- validation error;
- required image/file missing;
- authentication unavailable;
- authorization denied;
- unresolved ambiguity;
- rate-limit wait;
- source/contract drift gate;
- unresolved user decision/permission policy for future admin features.

If the blocker can be fixed on the same screen, provide the next action there.

## 8. Authentication vs authorization

These are different interaction states.

### Authentication unavailable

Message should say the session is not available/accepted and protected work is blocked.

### Authorization denied

Message should say the signed-in account does not have permission for the operation when the source/server verdict supports that conclusion.

Do not tell an unauthorized user merely to `sign in again` unless authentication is actually the problem.

## 9. Rate-limit interactions

A rate-limited job should not offer an impatient retry loop.

Show:

- what path hit the limit;
- when another attempt is allowed where known;
- that Forge is paused rather than failed when appropriate;
- whether any mutation ambiguity exists separately.

Do not animate or pulse the resume action while the limit is still active.

## 10. Recovery-specific anti-patterns

Never:

- offer `Retry` for an unresolved `SENT` mutation;
- treat orphan adoption as a benign selection without consequence text;
- hide candidate IDs entirely;
- preselect an orphan candidate;
- imply Skip cleans up a possible live record;
- mark a recovered job green before verification;
- let a generic `Resume all` bypass different recovery classes.

## 11. Publish-specific anti-patterns

Never:

- use `Save` as a euphemism for publish;
- place publish immediately beside ordinary save with identical styling;
- infer publish success from transport/HTTP success alone;
- automatically publish after an edit unless a future explicitly approved workflow says so;
- batch-publish by default from a broad list selection;
- use the same red family as error/destructive state for normal publish identity.

## 12. Mobile confirmation rules

On phone widths:

- consequence statement comes before long technical detail;
- action buttons remain reachable without covering warning content;
- confirmation surfaces must not require horizontal scroll;
- primary and destructive actions must not be tightly adjacent;
- long IDs are copyable and wrap/truncate safely without displacing the main decision;
- if a bottom sheet is used, it must support keyboard/focus and sufficient vertical scrolling;
- the safest cancel/back path remains obvious.

## 13. Accessibility rules

- focus moves into a modal/dialog when one is used and returns to the invoker on close;
- Escape/cancel behavior must not trigger the consequence;
- button labels describe the action without relying on icon/color;
- warning/consequence text is associated with the action context;
- irreversible/destructive consequence is conveyed in text;
- no timed confirmation is required for ordinary use;
- motion is not used as the sole signal of urgency.

## 14. Transcript-sensitive items left open

The predecessor transcript may still settle:

- exact publish confirmation level;
- exact operation-mode names;
- whether `Review` is an operation mode or a workflow category;
- final navigation placement of recovery/admin actions;
- exact visual form of confirmation surfaces.

The consequence classes and ambiguity rules remain useful regardless of those choices.

## 15. Implementation-review use

When Forge Next implementation begins, every consequential control should be reviewable against this matrix by answering:

1. What external/local consequence does it have?
2. What risk class applies?
3. What must the user know before activating it?
4. What evidence must be shown afterward?
5. What happens if the network/session changes mid-action?
6. Does ambiguity change the action into RX?

A control that cannot answer these questions is not ready for production UX review.
