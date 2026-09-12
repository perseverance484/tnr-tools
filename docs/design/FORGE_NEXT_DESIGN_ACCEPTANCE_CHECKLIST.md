# Forge Next — Design Acceptance Checklist

**Status:** REVIEW CHECKLIST — ARCHITECTURE-NEUTRAL  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** Forge Next visual direction, safety-state presentation contract, mobile/accessibility audit, screen content requirements, interaction-risk matrix, UI copy/state language  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Engineering Auditor, Release Auditor  
**Purpose:** provide a repeatable acceptance gate for wireframes, prototypes, and eventual implementation

## 1. How to use this checklist

This checklist does not decide the final information architecture or component framework.

Use it at three points:

- **wireframe review:** does the flow contain the right information and decisions?
- **visual review:** does styling preserve hierarchy, state separation, readability, and TNR character?
- **implementation review:** does the actual interactive behavior still satisfy the safety and accessibility contract?

A design can be visually polished and still fail this checklist.

## 2. Product character

- [ ] The interface reads as a professional TNR content-operations product rather than generic SaaS.
- [ ] Atmospheric/game-specific styling does not compete with operational content.
- [ ] Branded art/texture is concentrated in shell, lane, hero, or empty-state areas rather than recovery/diff/warning regions.
- [ ] The product feels deliberate and premium without imitating a battle screen.
- [ ] High-consequence controls are visually crisp and legible rather than ornament-heavy.
- [ ] Flash/motion reinforces state or orientation instead of creating ambient distraction.

## 3. Information hierarchy

- [ ] Every screen has one obvious page/task identity.
- [ ] Consequence is visible before the user reaches a high-consequence primary action.
- [ ] Blocking issues appear before non-blocking advisories.
- [ ] Primary action is visually distinguishable from secondary inspection actions.
- [ ] Advanced IDs/procedures/hashes do not dominate ordinary workflows.
- [ ] Important evidence remains available through progressive disclosure.
- [ ] Counts are used where they help scope decisions rather than as decorative metrics.

## 4. Operation consequence

- [ ] Read-only work is explicitly labeled as read-only/zero-mutation when that claim is true.
- [ ] Live mutation work says that it changes production/live content.
- [ ] Publish/visibility actions have a distinct consequence treatment.
- [ ] Recovery has a distinct context from ordinary execution.
- [ ] Operation context and semantic outcome are not communicated with the same visual grammar alone.
- [ ] Operation context never replaces the underlying machine state.
- [ ] Color is not the sole operation cue.

## 5. Lifecycle-state fidelity

- [ ] `PLANNED` does not look sent or successful.
- [ ] `SENT` is visibly ambiguous and requires reconciliation.
- [ ] `SENT` never exposes an ordinary Retry path.
- [ ] `CONFIRMED` does not look fully successful while verification is pending.
- [ ] `VERIFIED` is reserved for evidence-backed match/read-back.
- [ ] `FAILED` explains what failed and, when relevant, whether anything may have been sent.
- [ ] `ORPHANED` is presented as a decision/recovery problem rather than a generic error.
- [ ] `SKIPPED` is terminal but not successful.
- [ ] `INCOMPLETE` explicitly says the writes are not proven.
- [ ] `DONE`/completion state is not used by itself as proof of success.

## 6. Outcome/evidence fidelity

- [ ] Verified, failed, unverified, and open outcomes are visually and verbally distinct.
- [ ] Drift is distinguished from unread verification.
- [ ] Read success and full-capture persistence success are separate claims.
- [ ] Live-game verification and repository sync are separate claims.
- [ ] Publication state is not inferred from mutation transport success.
- [ ] A progress bar reaching 100% cannot be mistaken for verified completion.

## 7. Authentication and authorization

- [ ] Session probing has a visible non-error state.
- [ ] Authentication unavailable is distinct from ordinary read failure.
- [ ] Authorization/permission denial is distinct from authentication failure.
- [ ] Protected actions are disabled/blocked with an explanatory reason when the session is not ready.
- [ ] The safe next action for authentication failure is visible.
- [ ] No credential/session material is displayed as ordinary diagnostics.

## 8. Preflight

- [ ] Preflight clearly states whether the job is read-only or mutation-capable.
- [ ] Preflight provides meaningful operation counts.
- [ ] Validation blockers and advisories are separate.
- [ ] Missing required files/assets are visible before execution.
- [ ] Full-capture persistence consequences are visible before execution.
- [ ] Authentication/authorization blockers are visible before execution.
- [ ] The primary action uses a specific consequence-oriented verb.
- [ ] Raw JSON is not required to understand the normal operation.

## 9. Running work

- [ ] Active phase is visible when known.
- [ ] Current operation consequence remains available.
- [ ] Item-level state can be inspected without opening raw logs.
- [ ] Pause wording reflects actual behavior (`after this item` if that is the contract).
- [ ] Rate-budget state remains available when relevant.
- [ ] Session/auth state remains available during protected work.
- [ ] Navigation away/close behavior does not imply cancellation or rollback unless true.

## 10. Recovery

- [ ] Recovery is discoverable without scanning ordinary recent history.
- [ ] Different recovery classes are not collapsed into one generic Resume action.
- [ ] `SENT` recovery explains what is known and unknown.
- [ ] Orphan candidates are not preselected.
- [ ] Candidate IDs/details are available.
- [ ] Adopt and Skip have clearly different consequence language.
- [ ] Skip explains when a possible live row remains.
- [ ] Re-read-only recovery explicitly says it will not resend the write.
- [ ] Rate-limit recovery does not encourage early retry.

## 11. Capture/evidence management

- [ ] Ordinary read cache and immutable full-capture snapshots are conceptually distinct.
- [ ] Clearing read cache explains rate-budget consequence but does not look like live deletion.
- [ ] Deleting full-capture evidence requires deliberate confirmation.
- [ ] Evidence deletion explains what cannot be recovered locally.
- [ ] Data-classification/persistence tier is visible once Fable finalizes that architecture.
- [ ] No UI implies arbitrary captured data is repository-safe by default.

## 12. Content Admin — provisional gate

Apply only after Fable's source/permission model is accepted.

- [ ] Queue rows lead with human content identity, not manifest path.
- [ ] Current visibility/lifecycle is visible.
- [ ] Change summary is understandable without raw payloads.
- [ ] Editable and read-only fields are distinguishable.
- [ ] Dirty/changed fields do not use error styling.
- [ ] Edit/save and publish are distinct concepts.
- [ ] Publish is permission-aware.
- [ ] Preview is source-backed rather than a fabricated approximation presented as canonical.
- [ ] Approval/review state is labeled as coordination state if it is not live-game canon.
- [ ] Final action state is based on read-back/verification where required.

## 13. Publish/visibility

- [ ] Publish action names the content/record being affected.
- [ ] Current and target visibility are both visible before confirmation.
- [ ] Multi-record publish shows record count and relevant breakdown.
- [ ] Publish control is separated from ordinary Save/Edit actions.
- [ ] Publish operation identity does not reuse error/destructive red as its normal mode color.
- [ ] `Published` is not shown until the visibility result is evidenced.
- [ ] Publish failure and publish-unverified are distinguishable.
- [ ] Dependency/readiness warnings appear before confirmation when source-backed.

## 14. Confirmation quality

- [ ] High-consequence confirmation is not the first place consequence becomes visible.
- [ ] Confirmation uses a specific verb rather than `OK`/`Continue`.
- [ ] Confirmation names scope/count.
- [ ] Irreversible consequence is stated in text.
- [ ] Low-risk reads do not suffer confirmation fatigue.
- [ ] Package-level confirmation is preferred over repetitive per-item modals when the package is one coherent reviewed operation.
- [ ] Ambiguity introduces recovery explanation rather than a normal confirmation.

## 15. Buttons and action hierarchy

- [ ] One primary action per decision region.
- [ ] Disabled consequential actions have a nearby reason.
- [ ] Destructive styling is reserved for genuinely destructive actions/evidence deletion, not every live write.
- [ ] Recovery actions are not styled/labeled like ordinary retries.
- [ ] Publish action has deliberate identity without masquerading as success state.
- [ ] Primary and destructive actions are not dangerously adjacent on mobile.

## 16. Copy quality

- [ ] Messages say what happened instead of relying on generic `Error`/`Warning` labels.
- [ ] `Verified` has one meaning across the product.
- [ ] `Published` has one meaning across the product.
- [ ] `Safe` is not used as a vague all-purpose badge.
- [ ] `Retry` appears only when repeating the action is proven safe.
- [ ] `Complete` is not used while evidence is missing.
- [ ] Authentication and permission messages give the correct next action.
- [ ] Repository sync messages do not imply live verification.
- [ ] Empty states explain what the user can do next.

## 17. Mobile ergonomics

- [ ] Primary task can be completed at phone width without horizontal page scrolling.
- [ ] Interactive targets meet the agreed minimum target size.
- [ ] Important consequence/warning copy appears before long detail.
- [ ] Bottom/sticky actions do not cover state or warning content.
- [ ] Dense tables transform into readable stacked representations where necessary.
- [ ] IDs/hashes wrap or truncate safely and are copyable.
- [ ] No hover-only critical affordance exists.
- [ ] Primary navigation does not require tiny horizontally scrolling text tabs as the only usable model.
- [ ] Keyboard opening does not hide the active field or confirmation controls.
- [ ] Safe-area insets are respected where a fixed bottom action/navigation surface is used.

## 18. Desktop/tablet ergonomics

- [ ] Horizontal space provides parallel context rather than stretched single-column cards.
- [ ] Long prose/detail retains readable line length.
- [ ] Side context does not push the primary workflow below the fold unnecessarily.
- [ ] Core operation/recovery state remains visible while technical detail can occupy secondary regions.
- [ ] Desktop interactions do not depend on hover for core meaning.

## 19. Accessibility

- [ ] Text and controls target WCAG AA contrast.
- [ ] Color is never the sole state cue.
- [ ] Focus is visible on every interactive control.
- [ ] Focus order follows the visual/task order.
- [ ] Dialog focus is trapped/restored appropriately.
- [ ] Escape/cancel never triggers the consequence.
- [ ] Form errors are programmatically associated with their field.
- [ ] Status icons supplement text rather than replace it.
- [ ] Reduced-motion preference removes nonessential animation.
- [ ] Essential information is not encoded in tiny all-caps text.
- [ ] Decorative imagery does not degrade contrast/readability.

## 20. Motion

- [ ] Motion explains state/orientation or provides immediate feedback.
- [ ] Critical dialog backgrounds are not distractingly animated.
- [ ] Red/error state does not pulse/bounce for attention.
- [ ] Page transitions do not delay action.
- [ ] Progress animation does not imply completion/evidence it cannot prove.
- [ ] Reduced motion preserves all information.

## 21. Visual semantics

- [ ] Operation colors and semantic outcome colors remain distinguishable.
- [ ] Decorative content-lane colors do not imply operational state.
- [ ] Error/destructive red remains available for actual error/destruction.
- [ ] Warning/caution remains distinguishable from live-write identity.
- [ ] Publish identity remains distinguishable from failure/destructive state.
- [ ] Ambiguity/reconciliation treatment is distinct from verified success.

## 22. Resilience and errors

- [ ] Screen-render failure has a readable fallback.
- [ ] Network/repository failures do not erase already useful context unnecessarily.
- [ ] Persistent unresolved state survives transient toasts.
- [ ] Recovery after navigation/tab eviction is represented honestly.
- [ ] Partial failure does not turn an entire mixed result green.
- [ ] No UI implies rollback occurred unless the system actually performed/proved rollback.

## 23. Progressive disclosure

- [ ] Human summary comes before raw procedure/JSON detail.
- [ ] Expert users can still inspect IDs, hashes, paths, phases, and diffs.
- [ ] Advanced detail can be copied/exported when operationally useful.
- [ ] Collapsing technical detail never removes a safety-critical fact.

## 24. Performance perception

- [ ] Initial shell gives timely feedback even if repository lists load later.
- [ ] Long lists do not make the whole interface appear frozen.
- [ ] Progress states identify meaningful work rather than showing indefinite spinners everywhere.
- [ ] Visual effects do not materially compromise mobile responsiveness.
- [ ] Large imagery is not required to understand operational state.

## 25. Source and authority honesty

- [ ] Every displayed capability has a real source-backed path or is clearly a prototype placeholder.
- [ ] Mockup-implied actions are not silently implemented without capability evidence.
- [ ] Review/approval state does not pretend to be canonical live state when stored elsewhere.
- [ ] Final user-owned UX/publish/permission decisions remain visible rather than being settled by implementation convenience.
- [ ] No screen creates a new competing source of canon.

## 26. Transcript-reconciliation gate

Before final visual freeze, confirm the predecessor transcript has resolved or explicitly left open:

- [ ] final operation-mode taxonomy;
- [ ] operation-mode palette changes;
- [ ] whether `Review` is a mode;
- [ ] final navigation/destination language if ruled;
- [ ] final content-lane taxonomy if ruled;
- [ ] final publish-confirmation direction if ruled;
- [ ] any style-board acceptance/rejection not yet represented durably.

If the export is still unavailable, these rows remain a visible hold rather than being silently guessed.

## 27. Acceptance outcome

A reviewed design should receive one of:

- **ACCEPT** — meets all applicable critical requirements; remaining issues are polish only.
- **ACCEPT WITH FOLLOW-UPS** — no safety/authority/accessibility blocker, but named non-critical issues remain.
- **HOLD** — missing evidence/user decision prevents an honest final design choice.
- **REJECT** — design obscures safety state, authority, consequence, recovery, accessibility, or source truth.

Any HOLD/REJECT should identify the smallest concrete change or decision needed to move forward.
