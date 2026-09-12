# Forge Next — Adversarial UX Scenario Matrix

**Status:** DESIGN/REVIEW TEST INPUT — ARCHITECTURE-NEUTRAL  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** current Forge 0.4.0 behavior, safety-state presentation contract, screen requirements, interaction-risk matrix, UI copy/state language  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Engineering Auditor, Release Auditor  
**Scope:** states that wireframes, prototypes, and eventual UI tests must be able to represent honestly  
**Out of scope:** backend test implementation, procedure coverage, final routing, final tokens

## 1. Purpose

Happy-path mockups are insufficient for Forge.

The product's most important UX behavior often appears when execution is incomplete, ambiguous, permission-blocked, rate-limited, or split between successful live work and failed repository sync.

This matrix defines representative scenarios that future designs should render before the visual system is considered complete.

The goal is not to prescribe exact screenshots. The goal is to prove that the information architecture and component system can express every safety-relevant state without collapsing them into generic success/error screens.

## 2. Review method

For each scenario, a wireframe/prototype should answer:

- What does the user see first?
- What is the operation consequence?
- What does Forge know?
- What remains uncertain?
- What is the primary safe next action?
- What action must **not** be offered?
- What advanced evidence can the operator inspect?

If a design cannot answer those questions without raw JSON, it is not ready.

## 3. Entry and readiness scenarios

### S-01 — Fresh open, session ready

**Setup:** Forge opens on a valid carrier route; TNR session probe succeeds; no open jobs.

**Must show:**

- healthy session/readiness state;
- no false urgency;
- clear starting paths for work;
- no technical carrier-route detail in primary UX.

**Must not show:** generic success banner dominating the dashboard forever.

### S-02 — Fresh open, authentication not confirmed

**Setup:** page auth runtime/session readiness cannot be confirmed.

**Must show:**

- protected work blocked;
- public/read-only capability only if actually allowed;
- `Re-check`/sign-in guidance;
- auth problem distinct from read failure.

**Must not offer:** enabled protected write actions.

### S-03 — Server-proven unauthenticated refusal

**Setup:** a protected procedure is refused as unauthenticated.

**Must show:**

- stronger `authentication unavailable` state than mere probing/not-confirmed;
- protected work blocked;
- server refusal described without exposing auth material;
- safe sign-in/re-check path.

### S-04 — Authenticated but unauthorized

**Setup:** signed-in account receives source/server-supported role/permission denial.

**Must show:** `Permission denied` rather than `Sign in again`.

**Must not:** conflate authorization with authentication.

## 4. Work discovery and preflight scenarios

### S-05 — Repository list loads normally

**Must show:** human title/summary before raw path; search/filter; run-history indication where evidence exists.

### S-06 — Repository list refresh fails after prior data loaded

**Must show:** refresh failure while retaining prior usable list when feasible.

**Must not:** blank the whole workspace if existing cached/listed context is still valid.

### S-07 — Read-only summary capture preflight

**Must show:**

- `Read only` / zero mutations;
- capture/read count;
- authentication requirements if any read is protected;
- no live-write styling.

**Primary action:** `Run captures` or equivalent.

### S-08 — Read-only full capture preflight

**Must show:**

- zero mutations;
- full-capture count;
- exact-body persistence consequence;
- repository persistence consequence when sync/data class makes that true;
- allowlist/data-classification status once architecture is finalized.

**Must not:** make full capture visually indistinguishable from summary capture.

### S-09 — Live write preflight, all ready

**Must show:**

- live mutation consequence;
- create/update counts;
- captures/uploads when applicable;
- validation status;
- auth readiness;
- required files ready;
- explicit start verb.

### S-10 — Preflight blocked by validation

**Must show:** `Cannot run`, affected item/field, actionable correction.

**Must not:** allow primary live-write action.

### S-11 — Preflight blocked by missing image/file

**Must show:** exact missing slot and a pick-file path.

**Must not:** treat the unpicked file as a server/live failure.

### S-12 — Preflight has advisory but no blocker

**Must show:** advisory severity distinct from blocker and explain that execution is still allowed.

## 5. Running scenarios

### S-13 — Normal live write progressing

**Must show:**

- operation consequence;
- active item/phase when known;
- item lifecycle states;
- progress without implying early success;
- safe pause behavior.

### S-14 — Operator requests pause mid-item

**Must show:** `Pause after this item` semantics if that is the implementation contract.

**Must not:** imply an in-flight request was cancelled/rolled back.

### S-15 — Session expires before next protected send

**Must show:** paused/auth-blocked state and that nothing further was sent.

**Primary next action:** sign in/re-check then resume.

### S-16 — Rate budget trips

**Must show:**

- paused · rate limit;
- affected path;
- trustworthy wait/reset time if known;
- no eager retry action.

### S-17 — Close attempted while job running

**Must show:** why close is blocked or what pause is required first.

**Must not:** silently close and imply cancellation if work remains active.

## 6. Ambiguous write and reconciliation scenarios

### S-18 — Mutation recorded `SENT`, response/evidence ambiguous

**This is a mandatory design state.**

**Must show first:** `Needs reconciliation`.

**Must say:** request left/may have reached the game; result not proven.

**Primary action:** `Reconcile` / `Reconcile & resume`.

**Must not offer:** `Retry` or ordinary `Run again`.

### S-19 — `SENT` create reconciles to one clear record

**Must show:** reconciliation result, adopted/confirmed identity, then verification phase.

**Must not:** jump directly from ambiguity to green verified state unless read-back also completes.

### S-20 — `SENT` create yields multiple candidates

**Must show:** operator-decision state with candidate names/IDs/details.

**Must not:** preselect a candidate.

### S-21 — Reconciliation yields no safe candidate

**Must show:** why Forge cannot continue automatically and available operator choices.

If resend is not proven safe, it must not be offered.

## 7. Orphan scenarios

### S-22 — Orphan with candidate list

**Must show:**

- affected content/item;
- candidate list;
- Adopt actions;
- Skip action separated from adoption;
- consequence of adoption.

### S-23 — Orphan with manual ID adoption

**Must show:** ID input with confirmation and enough context to avoid pasting an unrelated record blindly.

### S-24 — Orphan skip

**Confirmation must say:** no deletion occurs and a possible live row may remain.

**Final outcome:** skipped/unverified, not success.

### S-25 — Safe later-phase resend path

**Setup:** machine state/source contract proves a later phase may be resent after operator inspection.

**Must show:** exact phase and why this is not repeating the ambiguous create.

## 8. Verification scenarios

### S-26 — Every write verifies

**Must show:** strongest verified treatment; concise summary; optional item details.

**Must not:** automatically imply published/visible.

### S-27 — Write confirmed, read-back unread

**Must show:** `Could not verify` / `Verification incomplete` and explicitly say write is confirmed but unproven.

**Primary action:** `Re-read` / `Verify again`.

**Must not:** resend the write.

### S-28 — Read-back drift

**Must show:** read succeeded but live values differ; changed/mismatched fields available.

**Must not:** call this a read failure.

### S-29 — Mixed result: some verified, one failed

**Must show:** aggregate `Finished with failures`, per-item distinctions, no full-page green success.

### S-30 — Mixed result: no failures but one skipped/unverified

**Must show:** aggregate `Finished unverified` rather than success.

## 9. Capture/evidence scenarios

### S-31 — Summary capture succeeds

**Must show:** read count succeeded and zero mutations sent.

### S-32 — Capture read fails

**Must show:** affected path/record and zero-mutation context.

### S-33 — Full capture read succeeds and body persists

**Must show:** both claims: read succeeded + body persisted.

### S-34 — Full capture read succeeds but body persistence fails

**Mandatory partial-success state.**

**Must show:** `Read succeeded · body not persisted` and that requested evidence is missing.

**Must not:** label the overall capture successful merely because the query worked.

### S-35 — Ordinary cache invalidation

**Must show:** local cache consequence and future rate-budget cost.

### S-36 — Delete one full-capture snapshot

**Must show before action:** exact evidence deletion consequence.

### S-37 — Delete all full-capture snapshots

**Must show:** scope/count/bytes where practical and impact on unexported jobs.

## 10. Repository/export scenarios

### S-38 — Live work verified, repository sync succeeds

**Must show separately:** live verification and result sync.

### S-39 — Live work verified, repository sync fails

**Mandatory split-success state.**

**Must show:** live content remains verified; repository record is not synced.

**Must not:** turn verified live work into a generic overall `failed` state without explaining the split.

### S-40 — Live work fails, repository export still available

**Must allow:** evidence export/inspection where safe even though the live outcome failed.

### S-41 — PAT/repository credential absent

Behavior depends on approved credential architecture, but the UI must not imply live operation is unavailable merely because repository sync is disabled unless the workflow truly depends on it.

## 11. Settings/diagnostics scenarios

### S-42 — Storage persistence healthy

Show as background diagnostic, not celebratory status.

### S-43 — Journal/storage write failure

**Critical:** must be durable/obvious because write-ahead safety depends on persistence.

**Must block unsafe mutation continuation** according to implementation contract.

### S-44 — Corrupt/unreadable journal record

Must provide export/diagnostic path without allowing one broken record to hide other good jobs if current architecture can retain that behavior.

### S-45 — Build/source drift gate present

Once Fable defines a user-visible drift model, the UI must explain what is stale and which operations are blocked rather than just showing `Update required`.

## 12. Content Admin scenarios — provisional

Apply after Fable completes source/permission feasibility and director decisions.

### S-46 — Review queue empty

Show clear `No content waiting for review` state and appropriate next path.

### S-47 — Queue has hidden/staged content awaiting review

Show human content identity, lifecycle, concise changes, review state/provenance.

### S-48 — Admin opens content detail with no edit permission

Show read-only detail/preview and explicit permission boundary.

### S-49 — Admin edits permitted fields on hidden live record

Show dirty state, changed fields, validation, live-edit consequence according to approved adapter architecture.

### S-50 — Edit verifies but remains hidden

Must show `Saved/verified` separately from `Published`.

### S-51 — Publish preflight, single record

Show current→target visibility, record identity, readiness warnings, explicit Publish action.

### S-52 — Publish mutation confirms, visibility read-back unread

**Mandatory:** `Publish not verified`, not `Published`.

### S-53 — Publish verifies

Show `Published` / verified visibility.

### S-54 — Publish refused by permission

Show `Permission denied`, not auth/sign-in guidance unless auth is also invalid.

### S-55 — Package/multi-record publish partial success

If package publish is ever approved, show per-record outcomes and avoid presenting the package as wholly published when only some records verify.

## 13. Mobile stress scenarios

### S-56 — Narrow phone with long manifest/content title

Title must wrap/truncate without pushing primary action/state off-screen.

### S-57 — Long record ID/procedure/error

Technical text must wrap/copy without horizontal page overflow.

### S-58 — Software keyboard open during ID adoption/edit

Active field and primary/cancel actions remain reachable.

### S-59 — Sticky bottom action + warning-heavy preflight

Sticky controls must not cover warnings or make the user confirm before reading consequence.

### S-60 — Reduced-motion preference

All state changes remain understandable with nonessential animation removed.

## 14. Desktop/tablet stress scenarios

### S-61 — Wide desktop dashboard

Uses parallel context meaningfully; does not stretch one phone column to extreme width.

### S-62 — Recovery detail with technical side panel

Primary decision remains clear while IDs/logs/diffs can coexist in a secondary region.

### S-63 — Dense item list with one ambiguous item

Attention should be drawn to the unresolved item without making all completed items visually noisy.

## 15. Visual-semantic collision scenarios

### S-64 — Live-write mode contains warning

Operation identity and warning state remain visually distinguishable.

### S-65 — Publish mode contains publish failure

Publish context remains identifiable while the failure callout uses semantic error treatment.

### S-66 — Decorative crimson Combat lane contains verified status

Lane identity must not override green/verified semantic cue.

### S-67 — Recovery context resolves successfully

Recovery operation identity must not prevent the final evidence state from becoming Verified when proof actually exists.

## 16. Copy consistency scenarios

### S-68 — Same `VERIFIED` item shown on dashboard, job detail, activity history

All three should use compatible wording and not redefine Verified.

### S-69 — `Resume` shown for three different paused jobs

Where behavior differs, labels/helper text must distinguish ordinary continuation, reconciliation, and re-read-only continuation.

### S-70 — Generic exception string exists

Human-facing title/consequence/next step should appear before raw exception detail.

## 17. Required scenario set for first wireframe review

At minimum, the first serious Forge Next wireframe set should demonstrate:

- S-01 healthy command center;
- S-02 auth blocked;
- S-08 full capture preflight;
- S-09 live-write preflight;
- S-13 running work;
- S-18 ambiguous SENT recovery;
- S-22 orphan resolution;
- S-27 verification unread;
- S-28 verification drift;
- S-34 read succeeded/body not persisted;
- S-39 live verified/repo sync failed;
- S-51 publish confirmation (provisional if admin architecture is not settled);
- S-52 publish not verified (provisional);
- S-59 mobile warning + sticky action.

This set intentionally over-samples unhappy/uncertain states because those are where a polished redesign is most likely to accidentally weaken Forge's existing safety model.

## 18. Acceptance criterion

A component system passes this scenario matrix when the scenarios can be represented using a coherent reusable vocabulary **without** inventing special one-off visual meanings or hiding machine distinctions.

A scenario may remain `HOLD` when the source/permission/architecture decision is genuinely unresolved. A HOLD is preferable to designing a fictional capability.
