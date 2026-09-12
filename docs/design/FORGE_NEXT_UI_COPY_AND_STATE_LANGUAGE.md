# Forge Next — UI Copy and State Language

**Status:** DESIGN LANGUAGE CONTRACT — ARCHITECTURE-NEUTRAL  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`, `FORGE_NEXT_INTERACTION_RISK_MATRIX.md`, `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Content Designer  
**Scope:** human-facing words Forge Next should use to describe consequence, progress, evidence, blockers, and recovery  
**Out of scope:** final route names, marketing copy, final operation-mode taxonomy, permission policy, implementation

## 1. Purpose

Forge operates on production content, so wording is part of the safety model.

This guide gives the redesign a consistent vocabulary that maps closely to what Forge can actually prove. It exists to prevent attractive UI copy from overstating certainty or hiding the difference between a read, a write, a confirmation, a verification, and publication.

The central rule is:

> Say what happened, what is known, what remains unknown, and what the user can safely do next.

## 2. Voice

Forge copy should be:

- direct;
- concise;
- operational;
- calm under failure;
- specific about consequences;
- human-readable before technical;
- explicit about uncertainty.

Avoid theatrical danger language for normal production work. Strong visual styling should communicate hierarchy while the words remain precise.

## 3. Message anatomy

For significant status or error copy, prefer this order:

1. **State:** what happened or what state Forge is in.
2. **Consequence:** what that means for live/repository state.
3. **Evidence:** what Forge knows or does not know.
4. **Next action:** the safe thing the user can do.

Example:

> **Verification incomplete.** The write was confirmed, but Forge could not prove the live record matches the intended values. Re-read the record; this will not resend the write.

Not every small message needs all four clauses, but ambiguity and failure usually do.

## 4. Operation consequence language

Final operation-mode names remain transcript-sensitive, but consequence wording should follow these patterns.

### Read-only work

Preferred phrases:

- `Read only`
- `Queries only · zero mutations`
- `This reads live data and does not modify game content.`
- `Run captures`

Avoid:

- `Safe mode` — too broad; reads may still have rate/privacy/persistence consequences.
- `No impact` — a read can consume rate budget or persist evidence.

### Mutation-capable work

Preferred phrases:

- `Live write`
- `This will create or update live game content.`
- `Start live write`
- `3 records · 1 create · 2 updates`

Avoid:

- `Apply changes` without saying they are live.
- `Save` when the action writes production content.

### Publishing

Preferred phrases:

- `Publish`
- `Make visible to players` where source evidence supports that exact consequence.
- `Unpublish` / `Hide from players` where source evidence supports it.
- `Publish content`

Avoid:

- `Save & publish` unless both are truly one approved operation and both consequences are visible.
- `Go live` if it could be confused with ordinary live writes.

### Recovery

Preferred phrases:

- `Recovery`
- `Needs reconciliation`
- `Reconcile before continuing`
- `Resolve ambiguous write`

Avoid:

- `Try again` for ambiguous state.

## 5. Item lifecycle language

### `PLANNED`

Primary label: `Planned`

Supporting copy examples:

- `Not sent yet.`
- `Waiting to run.`

Avoid success/progress language implying the server has seen anything.

### `SENT`

Primary human label: `Needs reconciliation`

Advanced/secondary label may expose `SENT`.

Preferred supporting copy:

- `The request may have reached the game, but Forge cannot yet prove the result.`
- `Do not retry this write. Reconcile it first.`
- `Request left the browser · result uncertain.`

Primary action:

- `Reconcile`
- `Reconcile & resume`

Never use:

- `Retry`
- `Failed` as the only label
- a success check

### `CONFIRMED`

Primary label: `Write confirmed`

Supporting qualifier:

- `Verification pending`
- `The write landed; Forge still needs to read it back.`

Avoid:

- `Complete`
- `Verified`
- `Success`

unless read-back evidence exists.

### `VERIFIED`

Primary label: `Verified`

Supporting copy:

- `Live values match the intended values.`
- `Read-back matched all asserted fields.`

Use the strongest success treatment here.

### `FAILED`

Primary label should name the failure class when known:

- `Validation failed`
- `Write refused`
- `Read failed`
- `Upload failed`
- `Permission denied`
- `Authentication unavailable`
- `Sync failed`

Fallback: `Failed`

Supporting copy should explain whether a request was sent and whether retry is safe.

### `ORPHANED`

Primary label: `Needs operator decision`

Supporting copy:

- `Forge could not identify one safe live record to continue with.`
- `Choose a candidate to adopt, or skip this item.`

Avoid:

- `Error` alone
- `Duplicate` unless evidence proves duplication.

### `SKIPPED`

Primary label: `Skipped`

Supporting copy:

- `No further action will be taken for this item.`
- `A possible live row may remain.` where applicable.

Do not call skipped work successful.

## 6. Job-state language

### `RUNNING`

Primary label: `Running`

Show active phase separately:

- `Reading`
- `Uploading`
- `Sending write`
- `Waiting for response`
- `Verifying`
- `Reconciling`
- `Syncing results`

Avoid using an indeterminate spinner without phase text when the phase is known.

### `PAUSED`

Primary label: `Paused`

Always append reason or recovery instruction where practical:

- `Paused · authentication unavailable`
- `Paused · rate limit`
- `Paused by operator`

Primary action should say what resumes:

- `Resume`
- `Reconcile & resume`
- `Re-read unverified items`

### `INCOMPLETE`

Primary label: `Verification incomplete`

Supporting copy:

- `The send path finished, but one or more writes are not proven.`
- `Re-read unverified items. This will not resend confirmed writes.`

Avoid:

- `Done with warnings`
- `Mostly successful`
- `Completed`

because these blur proof state.

### `DONE`

Do not expose `DONE` as a standalone success message. Pair completion state with evidence outcome.

Preferred final outcomes:

- `Verified`
- `Finished with failures`
- `Finished unverified`

### `ABORTED`

Primary label: `Stopped`

If the distinction matters technically, advanced detail may show `ABORTED`.

Supporting copy must state whether partial external effects may remain.

## 7. Verification language

### Match

- `Verified`
- `Read-back matched`

### Drift

Primary: `Live values differ`

Supporting:

- `The record was read back, but one or more asserted values do not match.`
- `Review the differences before continuing.`

Avoid calling drift a generic read failure; the read succeeded.

### Unread

Primary: `Could not verify`

Supporting:

- `Forge could not read the live record back, so the write is not proven.`

Primary action when safe:

- `Re-read`
- `Verify again`

Avoid:

- `Retry write`

## 8. Capture language

### Summary capture

- `Capture`
- `Read-only capture`
- `Queries only · zero mutations`

### Full capture

Primary label: `Full capture`

Supporting copy:

- `Stores the exact returned record body as evidence for the results bundle.`
- `When repository sync is enabled and the data class is approved for repository persistence, that body is included in the synced bundle.`

Do not imply every arbitrary read is repo-safe.

### Read succeeded, persistence failed

Primary: `Read succeeded · body not persisted`

Supporting:

- `Forge read the record successfully, but the requested full-capture evidence is missing from the bundle.`

Do not show this as capture success.

### Snapshot deletion

Preferred confirmation:

- `Delete capture evidence?`
- `This removes the exact stored record body. An unexported job may no longer be able to produce the requested bundle without reading the game again.`

## 9. Authentication language

### Probing

- `Checking TNR session…`

### Ready

- `TNR session ready`
- `Protected reads and writes are available.`

Avoid `Authenticated` if the UI has only proven the narrower readiness state and that distinction matters.

### Not confirmed

- `TNR session not confirmed`
- `Forge could not confirm a usable signed-in session. Protected work is blocked.`

### Server-proven refusal

- `TNR authentication unavailable`
- `The game refused a protected procedure as unauthenticated.`

### Next action

- `Sign in to The Ninja RPG in this browser, then re-check.`

Do not call an auth problem a read failure.

## 10. Authorization language

When the server/source proves role denial:

Primary:

- `Permission denied`

Supporting:

- `This signed-in account is not authorized to perform this action.`

Avoid telling the user only to sign in again unless the failure is authentication rather than authorization.

## 11. Rate-limit language

Preferred:

- `Paused · rate limit`
- `Forge stopped before sending more work on this path.`
- `Try again after 2:14.` where a trustworthy countdown exists.

Avoid:

- `Something went wrong`
- `Retry now`

Do not create a UI loop that encourages repeated requests before the budget resets.

## 12. Validation language

### Blocker

- `Cannot run`
- `Fix the following before starting.`

### Advisory

- `Check recommended`
- `This does not block execution.`

Do not make advisories look identical to blockers.

Field-level errors should identify the field and the expected correction in ordinary language where possible.

## 13. Missing asset/file language

Preferred:

- `Required image missing`
- `Choose a file for <slot name> before starting.`
- `Picked`

Avoid using semantic failure red to describe a file that simply has not been selected yet unless the user attempted an action that requires it.

## 14. GitHub/repository language

Separate repository actions from live-game actions.

Preferred phrases:

- `Repository connected`
- `Results synced`
- `Results not synced`
- `Repository sync failed`
- `Export bundle`

Never imply `Results synced` means live content was verified.

Credential copy should say where a credential is sent/stored only when that is source-backed and approved by the repository credential model.

## 15. Publish language

### Ready to publish

- `Ready to publish` only when the prerequisites the product claims to check are actually satisfied.

### Confirmation

Pattern:

`Publish <content name>?`

`This changes visibility from <current> to <target>.`

For multi-record scope:

`Publish 4 records?`

Then provide a concise breakdown.

### Pending result

- `Publishing…`

### Mutation confirmed, read-back pending

- `Publish confirmed · verifying visibility`

### Verified published state

- `Published`
- `Visibility verified`

### Failure

- `Publish failed`
- `Publish not verified`

These are distinct. A transport/server refusal is failure; an unread final state is unverified.

## 16. Destructive/evidence-removal language

Use concrete verbs:

- `Delete snapshot`
- `Delete finished jobs`
- `Clear read cache`
- `Forget credential`

Avoid euphemisms:

- `Clean up`
- `Reset`
- `Remove data`

when the exact destructive effect matters.

## 17. Confirmation-copy template

For R4/R5/RX interactions, use this structure when space permits:

**Title:** specific verb + object  
**Consequence:** what will change externally  
**Scope:** counts/record names  
**Uncertainty/warning:** only when material  
**Primary button:** same specific verb  
**Secondary button:** `Cancel` or safe alternate

Example:

**Start live write?**  
`This will create 1 record and update 2 live records. Verification will run after each write.`  
Primary: `Start live write`  
Secondary: `Cancel`

## 18. Error-copy template

Avoid raw exception strings as the only user-facing message.

Preferred layering:

**Human title:** `Could not verify record`  
**Consequence:** `The write is confirmed but not proven.`  
**Next action:** `Re-read the record.`  
**Advanced detail:** procedure/error payload/stack as appropriate.

Raw errors remain valuable, but belong behind a technical-detail disclosure unless they are already clear and safe.

## 19. Empty-state language

Empty states should answer two questions:

1. Why is this empty?
2. What can I do next?

Examples:

- `No active work. Start from a content lane or open a work package.`
- `No captures yet. Run a read-only capture to collect evidence.`
- `No recovery needed. There are no ambiguous or paused jobs.`

Avoid decorative `Nothing here` copy without a next step.

## 20. Terms to reserve

### `Verified`

Reserved for evidence-backed match/read-back.

### `Published`

Reserved for a source-backed content visibility state.

### `Live`

Use carefully. `Live write` means production mutation context; `Published/live to players` means visibility. Prefer explicit wording so the two do not blur.

### `Safe`

Avoid as a general badge. Say what is safe: `Read only`, `zero mutations`, `re-read only`, `will not resend`.

### `Retry`

Use only when repeating the action is proven safe. Never for unresolved `SENT` mutation state.

### `Complete`

Avoid when verification or requested evidence is still missing.

## 21. Terms to avoid as catch-alls

Avoid overusing:

- `Error`
- `Success`
- `Done`
- `Failed`
- `Warning`
- `Retry`

when a more specific state tells the user what happened and what to do.

## 22. Technical vocabulary and progressive disclosure

Plain language should lead, but expert detail must remain available.

Examples:

- primary: `Needs reconciliation`
- advanced: `Journal state: SENT · phase: create`

- primary: `Live values differ`
- advanced: `verify: drift · asserted fields: 6 · mismatched: 2`

- primary: `Permission denied`
- advanced: server/procedure error code and path.

This preserves auditability without making ordinary operation depend on internal terms.

## 23. Microcopy consistency tests

Before accepting a screen, check:

- Does `Verified` mean the same thing everywhere?
- Does `Published` describe content visibility rather than request success?
- Is an ambiguous write ever called `Failed` without explaining uncertainty?
- Does every disabled consequential action have nearby blocker text?
- Does every `Resume` action say what kind of work it resumes when that distinction matters?
- Does any `Retry` risk resending an ambiguous mutation?
- Does the screen say `read only` only when zero mutations are actually possible?
- Are repository sync and live-game verification described separately?

## 24. Transcript-sensitive terminology

Leave these exact labels open pending predecessor-chat reconciliation:

- final operation-mode names;
- whether `Review` is a mode name;
- final top-level route/workspace names;
- exact Command Center title;
- final content-lane taxonomy;
- final publish confirmation wording if the director already ruled it later in the missing chat.

The state/evidence language in this document can be retained even if those labels change.
