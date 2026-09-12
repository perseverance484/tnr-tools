# Forge Next — Safety-State Presentation Contract

**Status:** DESIGN CONTRACT — ARCHITECTURE-NEUTRAL / COLOR-AGNOSTIC  
**Date:** 2026-09-12  
**Depends on:** `docs/design/FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`  
**Implementation evidence:** Forge `0.4.0`, `main` at `305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Engineering Auditor  
**Scope:** how Forge Next must communicate safety-relevant machine state to humans  
**Out of scope:** final palette, final operation-mode taxonomy, final navigation, final component styling, backend/state-machine changes

## 1. Purpose

Forge already has a safety-aware execution model. The redesign must not compress that model into a generic `success / warning / error` palette.

This contract defines the **meaning that the UI must preserve** regardless of final colors, icons, layout or component framework.

The central rule is:

> A visual state may summarize machine state, but it may never imply more certainty, safety or completion than the underlying evidence proves.

## 2. Do not treat “state” as one axis

Forge Next must model at least six distinct axes. They may be presented together, but they must not be semantically merged.

### Axis A — operation context

What kind of consequence is the user attempting?

Examples include read-only inspection, mutation-capable work, review, publishing, or recovery. The final taxonomy remains subject to director/transcript reconciliation.

**This axis answers:** “What can this workflow do?”

### Axis B — execution lifecycle

Where is the job/item in the write-ahead process?

Current machine vocabulary includes:

- `PLANNED`
- `SENT`
- `CONFIRMED`
- `VERIFIED`
- `FAILED`
- `ORPHANED`
- `SKIPPED`

and job states:

- `RUNNING`
- `PAUSED`
- `DONE`
- `INCOMPLETE`
- `ABORTED`

**This axis answers:** “How far did execution get?”

### Axis C — evidence / verification outcome

What does read-back or capture evidence prove?

Current semantics include:

- match / verified;
- drift;
- unread / unverified;
- full-capture body persisted;
- full-capture body not persisted;
- capture read succeeded/failed.

**This axis answers:** “What do we actually know happened?”

### Axis D — authentication / authorization availability

Can the logged-in browser session perform the required protected operation?

At minimum distinguish:

- checking/probing;
- ready;
- not confirmed;
- server-proven authentication refusal;
- authorization/role denial when surfaced by the underlying procedure.

**This axis answers:** “May this session attempt the operation?”

### Axis E — system/rate/storage health

Examples:

- rate budget healthy / near limit / tripped;
- GitHub sync configured / unavailable / failed;
- persisted storage available / failed;
- required images present / missing;
- local evidence available / deleted.

**This axis answers:** “Are the supporting systems ready?”

### Axis F — publication/content lifecycle

Publication is a content lifecycle concept, not equivalent to technical job success.

Examples may include hidden/staged, pending review, approved, published, unpublished, or other source-backed states once Content Admin is designed.

**This axis answers:** “Who can see/use this content?”

## 3. Non-negotiable hierarchy of certainty

The UI must preserve the following certainty ordering:

### `PLANNED`

Meaning: intended work has not been recorded as having left the browser.

Presentation requirements:

- neutral/not-started language;
- never imply success;
- safe to distinguish from any request that may have left the device.

### `SENT`

Meaning: the write-ahead journal proves the request left or must be treated as having left, but Forge does not yet have sufficient evidence to say what the server did.

Presentation requirements:

- **highest ambiguity emphasis**;
- explicit language such as `Needs reconciliation` or equivalent;
- never use a success check;
- never expose an ordinary `Retry` action;
- recovery action must lead to reconciliation, not blind resend;
- if technical vocabulary is collapsed, `SENT` must remain available in advanced detail.

### `CONFIRMED`

Meaning: the write is known to have landed or was adopted/reconciled, but the asserted live read-back is not yet proven equal.

Presentation requirements:

- positive progress is allowed;
- **must not look terminal-successful**;
- preferred plain-language framing: `Write confirmed · verification pending` or equivalent;
- if the item is in verify phase, actions must not suggest re-sending the write.

### `VERIFIED`

Meaning: asserted keys read back equal to what Forge intended.

Presentation requirements:

- only this evidence level may receive the strongest successful-write treatment;
- state label/check icon must still be textual/accessible;
- do not conflate with publication.

### `FAILED`

Meaning: the item reached a terminal failure according to execution/server verdict.

Presentation requirements:

- explicit failure label and reason;
- distinguish refusal/validation/transport categories where the next safe action differs;
- do not imply that a failed create can simply be retried unless machine state proves that is safe.

### `ORPHANED`

Meaning: reconciliation could not identify a safe single live result for an ambiguous create/update path and requires an operator decision.

Presentation requirements:

- not a generic error card;
- visually treated as a decision/recovery state;
- show what is known, candidate records when available, and consequence of each operator choice;
- `Adopt`, `Skip`, and any resend path must remain distinct actions;
- do not preselect a destructive or irreversible decision.

### `SKIPPED`

Meaning: the operator deliberately chose not to resolve/apply that item further.

Presentation requirements:

- neutral terminal treatment, not success;
- make explicit when a possible live row remains;
- never count skipped items toward a fully verified outcome.

## 4. Job-state contract

### `RUNNING`

- show current operation context and active phase;
- indicate which action/item is active when known;
- give the operator a safe pause request where supported;
- do not hide authentication or rate health while work is active.

### `PAUSED`

Paused is not failed and not complete.

Presentation must communicate:

- why it paused;
- whether anything may already have been sent;
- when/what permits resume;
- whether resume begins with reconciliation, re-read, or ordinary continuation.

A SESSION pause and a rate-limit pause must not look identical if their recovery instructions differ.

### `INCOMPLETE`

This is one of the most important states in Forge.

Meaning: execution reached the end of its send path, but one or more writes remain unproven by read-back.

Presentation requirements:

- never green/complete;
- plain language must say the writes are **not proven**;
- primary next action should be re-read/verify, not repeat the write;
- distinguish drift from unread where useful;
- preserve the fact that resuming cannot re-send the already-confirmed write.

### `DONE`

`DONE` alone is not enough to choose success styling. The UI must also evaluate the job outcome/evidence.

The current journal intentionally separates job state from outcome. Forge Next must preserve that concept even if labels change.

### `ABORTED`

- terminal interruption/failure treatment;
- reason visible;
- no implication that partial external effects were rolled back unless evidence proves that.

## 5. Outcome contract

The current implementation computes four high-level outcomes:

- `open`
- `success`
- `failed`
- `unverified`

These are useful human summary categories and should remain conceptually available.

### `success`

May be shown only when every relevant mutation item is verified and requested capture-persistence obligations are satisfied.

### `failed`

At least one terminal failure exists, or a capture-only job failed to deliver the read/persistence evidence it requested.

### `unverified`

No terminal item failure is sufficient to explain the result, but the evidence is incomplete or contradictory: drift, unread, skipped/orphaned work, unresolved items, or missing requested full-capture persistence.

**UI rule:** `unverified` must have its own visual grammar. It is neither success-green nor generic failure-red.

### `open`

The final answer is not known yet because execution/recovery is still underway.

## 6. Auth state contract

Authentication state is global context and must not be disguised as a job result.

### Ready

- healthy compressed treatment is acceptable;
- on mutation/publish/recovery screens, readiness should remain visible enough that the operator knows the action can contact protected procedures.

### Probing/checking

- disable actions whose safety depends on the answer;
- communicate that Forge is checking, not failing.

### Not confirmed

- fail closed on protected work;
- explain that Forge cannot prove the browser session is usable;
- distinguish from server-proven sign-out.

### Server-proven refusal

- explicitly state that the server refused authentication;
- invalidate any earlier “session active” presentation;
- explain what was or was not sent before the refusal;
- Resume remains blocked until a successful re-check.

### Authorization / role denial

When underlying procedures expose this distinction, do not collapse it into “sign in again.”

The user may be authenticated but not authorized. The next action and product meaning differ materially.

## 7. Capture persistence contract

A capture has two separate questions:

1. Did the read succeed?
2. If `persist: full` was requested, was the exact body durably stored/exportable?

The UI must never let a successful read stand in for successful evidence persistence.

### Before execution

Full capture must state:

- that it is still a zero-mutation read if applicable;
- that exact record bodies will be persisted;
- where those bodies may be exported/synced when repository sync is enabled;
- the persistence/privacy consequence in human language.

### After execution

Show independently:

- read succeeded / failed;
- body persisted / not persisted.

Missing persistence makes the requested evidence incomplete even when the server read succeeded.

## 8. Rate-limit / budget contract

Rate budget is not merely a diagnostic number. It can change what actions are safely available.

Presentation requirements:

- healthy budget may remain compact;
- approaching or tripped budget must become visible before the next affected action;
- a rate-limit pause should say when work may resume where timing is known;
- the UI must not encourage repeated retries into a limiter;
- background/carrier traffic that is not accounted by Forge should never be visually claimed as part of the Forge budget unless future architecture proves it is.

## 9. Recovery action grammar

Recovery controls require stronger rules than normal buttons.

### Reconcile & resume

Meaning: resolve any `SENT` ambiguity first, then continue safely.

- primary action only when the machine state supports it;
- wording should mention reconciliation, not generic retry.

### Re-read / verify

Meaning: gather evidence for an already-landed/confirmed write.

- must not imply another mutation will occur;
- safe/read semantics should be visible.

### Adopt

Meaning: operator asserts that a particular live record is the result to continue with.

- show candidate identity and human name/context;
- confirmation must state what record will be associated and what continuation follows;
- do not preselect a candidate.

### Re-send phase

This is exceptional and high consequence.

- only surface where the underlying state machine allows it;
- must say which phase will be sent to which entity;
- require an explicit confirmation;
- visually separate it from low-risk `View`/`Re-read` controls.

### Skip

- wording must state that existing server rows are left untouched;
- never use a successful/approved visual treatment;
- final summaries must retain the skipped fact.

### Delete local evidence/cache

Distinguish:

- invalidating disposable read cache;
- deleting immutable full-capture evidence;
- deleting finished journal history;
- forgetting a GitHub credential.

These are not one generic `Danger` action type even if they share destructive styling.

## 10. Required communication stack for consequential states

No consequential state may rely on one cue.

Use at least:

1. **text label** — what state/mode it is;
2. **icon or shape cue** — redundant visual recognition;
3. **color family** — secondary reinforcement;
4. **plain-language consequence** — what this means for live data/user action;
5. **next safe action** — where recovery/action is available.

For high-risk ambiguity (`SENT`, orphan, unverified write), add a sixth cue:

6. **explicit prohibition/warning** — e.g. `Do not retry blindly` where appropriate.

## 11. Color rules before final palette reconciliation

This contract deliberately does not settle exact colors.

Binding rules that survive palette changes:

- operation context colors must remain distinct from semantic outcome colors;
- success/verified styling cannot be reused for `CONFIRMED`, `DONE` without verified outcome, `SKIPPED`, or published state;
- failure/destructive styling must not become the primary identity of a normal mutation mode;
- warning/pause styling must not become the primary identity of live-write mode;
- ambiguity must have a distinct treatment from both failure and success;
- publication must not visually mean “execution succeeded.”

## 12. Component behavior requirements

Whatever final component system is chosen, Forge Next needs equivalents of:

### Operation header

Shows:

- operation context;
- production consequence;
- concise read/write/create/upload/capture/publish counts when available;
- current readiness blockers.

### State chip

Used for compact state only. It must not carry the full consequence explanation for ambiguous/high-risk states.

### Safety callout

Used when operator action is blocked or recovery is required. Contains state, explanation and next safe action.

### Progress treatment

Must distinguish:

- active work;
- paused work;
- ambiguous/reconciliation state;
- confirmation awaiting read-back;
- verified completion.

A single progress bar changing color is not sufficient.

### Recovery decision card

Contains:

- what is uncertain;
- evidence/candidates;
- available choices;
- consequence per choice;
- technical detail under progressive disclosure.

### Final result summary

Must answer separately:

- did execution finish?;
- did any operation fail?;
- are writes verified?;
- did requested capture evidence persist?;
- was anything skipped/unresolved?;
- did repository sync/export succeed, where relevant?;
- publication state, if applicable.

## 13. Mobile requirements for safety state

On phone widths:

- the current operation context must appear before long technical detail;
- active ambiguity/recovery state must remain discoverable without scrolling through completed items;
- primary recovery action must remain thumb-accessible without covering the explanation;
- dangerous alternatives must not be adjacent in a way that encourages accidental taps;
- long IDs/diffs/procedure names collapse behind `Details` rather than shrinking text;
- sticky action bars may be used only if they do not cover warnings/state summaries;
- no hover-dependent explanation.

## 14. Desktop/tablet requirements for safety state

Use width to keep context visible while technical evidence is inspected.

Recommended composition pattern, not a final layout mandate:

- persistent operation/status summary;
- primary work/progress area;
- contextual evidence/details panel;
- recovery decisions kept visually above routine historical rows.

## 15. Accessibility requirements

- state words remain in text even when icons/colors exist;
- focus order must follow consequence hierarchy;
- dynamic changes such as pause/failure/verification should be designed for screen-reader announcement in implementation;
- warning/error text must not depend on all-caps or tiny badges;
- contrast must meet the project's eventual WCAG AA baseline;
- any new motion signaling state must have a reduced-motion equivalent;
- success/failure/ambiguity cannot be color-only.

## 16. Anti-patterns explicitly prohibited by this contract

- `SENT` displayed with a green check because the request left the browser;
- `CONFIRMED` presented as equivalent to verified completion;
- `DONE` mapped mechanically to success without checking outcome/evidence;
- a generic `Retry` button on an ambiguous write;
- auth refusal presented as an ordinary content read failure;
- role denial presented as “please sign in” when the user is already authenticated;
- full-capture read success shown as complete when the requested body was not persisted;
- skipped work disappearing from final summaries;
- publishing using the same visual concept as technical success;
- destructive evidence deletion hidden behind a generic cache-cleanup action;
- mode and outcome communicated by the same color family with no textual distinction.

## 17. Transcript-sensitive items intentionally left open

The predecessor-chat export may settle or supersede presentation choices around:

- final operation-mode names;
- whether `Review` is a first-class mode or a workspace/context;
- exact operation-mode palette;
- exact final button/badge/icon styling;
- final navigation placement of Recovery or Review;
- degree of persistent versus compact state presentation.

Those questions do not change the machine meanings defined here.

## 18. Completion statement

Step 2 of the interim Forge UI workflow is complete.

This contract is intentionally stronger than a color/style guide: it defines the semantic safety floor that any future Forge Next wireframe or implementation must preserve. No production code, Fable branch, live request or live write was touched.