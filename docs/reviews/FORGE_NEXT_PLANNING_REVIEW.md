# Forge Next planning — independent review

**Status:** INDEPENDENT REVIEW — REQUIRED CORRECTIONS BEFORE INTEGRATION  
**Date:** 2026-09-13  
**Reviewer:** ChatGPT — Engineering Auditor lead, UI/UX Reviewer supporting lens  
**Reviewed branch:** `claude/forge-next-planning-v3frzi`  
**Reviewed exact SHA:** `201a1e2ea57011440e164f84a0ed30298fa4b243`  
**Declared planning base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Live main at review start:** `6848a7805d912378f7f8eb27f52c9625dd10ac54`  
**Concurrent ChatGPT implementation reviewed as reconciliation evidence only:** `chatgpt/forge-quest-studio-foundation@cda8ac76100b2fa4b5429bea27c3c8c80353e240`  
**Live-game requests/writes:** none

## 1. Verdict

**Architecture: approve. Planning package: approve with required corrections before integration.**

The package's central engineering recommendation is sound and compatible with the director-approved product direction: extract a headless `ForgeCore`, preserve the reviewed runner/storage/transport/reconcile safety core, move leaked domain behavior below the UI seam, then replace the shell incrementally. The operation-first IA with content lanes as a second axis is also compatible with the approved visual/product direction because the package keeps Quest Studio, Content Admin and content lanes first-class while leaving exact navigation labels/placement as director decisions.

The package is unusually strong on evidence, parity, retirement gates, source-vs-live distinctions, failure semantics, and explicit uncertainty. It should become the engineering architecture backbone of the unified Forge product.

It is **not ready to integrate unchanged** for four reasons:

1. the user-decision register escalates ordinary engineering choices that repository workflow explicitly says not to escalate;
2. the roadmap then turns some of those technical choices into false phase blockers and contradicts its own `Can defer` statements;
3. the package necessarily studied an intermediate Quest Studio implementation SHA and must be reconciled to the final frozen implementation/review evidence before the two lines are unified;
4. several audit-grade summary strings/handoff statements are stale relative to the package's own final files.

None of these findings requires abandoning the architecture or visual direction.

---

## 2. Findings

### F1 — HIGH — The decision register over-escalates engineering details into director decisions

`docs/workflows/DIRECTOR_DECISIONS.md` says to use the director-decision path for balance, publishing, final content/UX/art direction, risky production-workflow changes and other explicitly reserved classes, and states: **"Do not escalate ordinary engineering details that are already settled by source/contracts/tests."**

`K_USER_DECISIONS.md` correctly contains many genuine director decisions, but it also makes normal architecture/implementation ownership into user rulings. Examples include:

- K-13 game-source pin refresh mechanics;
- K-14 whether the build is minified;
- K-25 Quest Source schema/version evolution;
- the implementation-mechanism half of K-26 (dispatch vs source-push, branch mechanics);
- K-36 where profile-shape enforcement lives;
- K-37 Studio branch namespace/retention/conflict handling;
- K-38 worker refusal/cancellation observability;
- K-39 artifact-promotion/journal contract mechanics;
- K-40 workstream-to-build reference mechanics;
- K-50 adapter boundary between shared compiler and subtype logic;
- K-52 which source-backed role lookup is used;
- K-60 who applies a release-loader test correction;
- K-61 who owns Studio files after the explicitly assigned ChatGPT foundation slice ends.

Several may contain a smaller director-owned consequence (credential exposure, production safety, visible UX), but the technical mechanism itself belongs to Fable as architecture/implementation owner and to independent review as a verification concern.

**Practical consequence:** implementation can stall waiting for the director to choose internal mechanisms that the engineering owner should decide and defend. It also weakens the distinction between user-owned product canon and engineering design.

**Required correction:** split section K into at least two classes:

- **Director decisions** — only choices whose operator/player/authority consequence is genuinely user-owned;
- **Engineering decisions / implementation gates** — Fable-owned choices constrained by source, contracts, tests and the director-approved product boundary.

Where one row contains both, split it. For example, credential possession/scope may remain a director/security policy choice, while whether the worker uses `workflow_dispatch` or a source-push trigger is an engineering choice once least privilege and UX requirements are satisfied.

This correction should reduce the number of decisions presented to the director, not merely rename the same list.

### F2 — HIGH — Phase 0 is falsely blocked by choices the package itself says can defer

`G_ROADMAP.md` says Phase 0 requires K-13, K-14 and K-60 before implementation. But the owning decision entries say:

- K-13 **Can defer: yes**, provided drift is rechecked;
- K-14 **Can defer: yes**;
- K-60 is a branch/work assignment rather than a product ruling.

K-60 also misreads the one-writer rule. The rule is **one writer per branch**, not a global prohibition on two independently owned branches ever touching the same file. Cross-branch overlap is an integration/review concern; it does not require a director ruling merely because both branches contain changes to `release_loader.test.mjs`.

The project role model also makes Fable the normal implementation owner unless the director explicitly assigns ChatGPT. The ChatGPT Quest Studio implementation was an explicit slice assignment, not a permanent transfer of Forge ownership. Therefore K-61 is normally resolved by the existing role split after the frozen slice is reviewed/integrated unless the director explicitly assigns otherwise.

**Practical consequence:** the proposed first implementation phase can be prevented from starting for no product or safety reason.

**Required correction:** Phase 0 should begin from objective prerequisites, not director assignments for routine engineering. At minimum:

- current `main` green or known-baseline defects explicitly isolated;
- current game-source drift rechecked;
- exact implementation owner/branch named in the implementation brief;
- chosen bundle-size/release approach documented by Fable and reviewable;
- known release-loader test correction included in the integration plan.

Do not require K-13/K-14 as director rulings if their own entries say they can defer.

### F3 — MEDIUM — The planning package must be reconciled to the final Quest Studio foundation, not the intermediate `824c4d58` snapshot

The planning package behaved correctly under concurrent-work rules: it treated `chatgpt/forge-quest-studio-foundation@824c4d58` as read-only evidence and did not patch it. However, the ChatGPT implementation line later froze at:

`cda8ac76100b2fa4b5429bea27c3c8c80353e240`

with fully verified implementation parent:

`bcb3a47e7c516b20f5a51c5aa195364d32eb6b73`.

The final implementation evidence materially advances the snapshot Fable studied:

- zero-live-network static guard;
- worker trust-boundary contract test;
- `quest_compile.py` 9/9 selftests;
- real Mission adapter integration through `mission.py + validate.py`;
- Forge suite 308/308;
- multiline-draft regression;
- generated-artifact path-traversal fix and regression;
- canonical bundle rebuild and checked-bundle parity;
- explicit final handoff and known-debt list.

The final branch still has the architectural debt Fable correctly identified: the first Studio UI is a second shell with local hard-coded styling, and its eventual absorption into the shared shell/core is real work. But the plan should not continue to describe final evidence as unverified merely because the earlier snapshot was.

**Practical consequence:** integrating the planning docs unchanged would canonize obsolete test counts, stale security status and stale uncertainty around the Studio seam.

**Required correction after the independent implementation review:** update Studio citations/readings from `824c4d58` to the final accepted Quest Studio SHA, preserve any still-valid architectural criticisms, and retire/refine decisions that the final implementation already settled mechanically. Do not reimplement the seam from scratch. Phase S should absorb the reviewed implementation into `ForgeCore`/the new shell.

### F4 — MEDIUM — Audit-summary metadata is stale inside the frozen package

The detailed sections are stronger than several top-level summary strings.

Verified examples at the frozen SHA:

- `evidence/parity-matrix.json` has a stale prose `summary` claiming `PARITY 10 / INTENTIONAL DIFFERENCE 5 / GAP 22 / blocker yes 7 / no 45`, while the same file's machine `status_tally` and `B_PARITY_MATRIX.md` correctly report `PARITY 8 / INTENTIONAL DIFFERENCE 6 / GAP 23`, with blocker rows `yes 8 / conditional 9 / no 43 / split 1`.
- The final freeze commit message says **nine evidence files**, while the top-level evidence directory contains ten evidence files (`admin-feasibility.json`, `contrast.py`, `drift.json`, `forge-tests-ci.json`, `harvest-evidence.json`, `parity-matrix.json`, `registry-gap.json`, `repo-consumers.json`, `ux-audit-current.json`, `visual-synthesis.json`) plus the `design-options/` directory.
- The handoff reports a blocker-count inconsistency and a 16-vs-17 wireframe inconsistency, but the final `B_PARITY_MATRIX.md` already has the explicit `split` blocker row and final `D_IA_AND_JOURNEYS.md` already says seventeen wireframes. The handoff therefore describes defects that no longer exist while omitting that only the evidence summary string remains stale.

**Practical consequence:** reviewers cannot tell whether a number is authoritative without opening the underlying section, which is contrary to the purpose of an audit handoff.

**Required correction:** regenerate/reconcile the summary metadata from the final rows and make the final handoff describe the actual frozen state. The detailed row data remains the authority; do not alter conclusions merely to match stale prose.

---

## 3. Verified strengths

The following should be preserved during corrections and integration:

1. **Headless-core-first architecture.** `ForgeCore` as an explicit, machine-checked seam is the right long-term foundation. It preserves the deeply tested safety core while allowing the UI/product surface to grow.
2. **Incremental shell replacement.** Screen-by-screen replacement after seam extraction is materially safer than a wholesale UI rewrite.
3. **Repository-backed Studio model.** Fable accepts the director-set rule that Forge is the operator interface and `tnr-tools` owns durable facts/scripts/contracts/build artifacts. This aligns with the Quest Studio implementation rather than competing with it.
4. **One Quest Studio.** Mission remains a subtype, not a separate product. Unsupported types stay honest rather than appearing executable.
5. **Compile/live separation.** The plan consistently keeps repository compilation separate from live-game mutation and preserves explicit operator action for production work.
6. **Builder retirement discipline.** Retirement is gate-driven, not schedule-driven. Proven Builder-only research, image-pack and recovery capabilities remain explicit blockers.
7. **Content Admin evidence.** The source audit distinguishes technical feasibility from authority and keeps unverified browser/session behavior marked as unverified.
8. **Visual reconciliation.** The package genuinely consumes the approved dark TNR operations-tool direction and separates binding product character from illustrative tokens/labels.
9. **Safety-state semantics.** SENT ambiguity, recovery, auth, budget and readback remain separate machine states rather than being cosmetically collapsed.
10. **Testing strategy.** The layered unit/contract/UI/scenario/adversarial/static/browser strategy is appropriate; real browser/live proof remains user-owned.

---

## 4. UI/UX reconciliation notes — not architecture blockers

The operation-first IA is a defensible recommendation, not a conflict with the approved content-lane direction. Keep content lanes as a prominent second axis and Command Center entry mechanism.

Two director-facing shell choices remain legitimately open:

- exact desktop/mobile destinations;
- whether Quest Studio and/or Content Admin deserve a primary phone-nav slot rather than living under `More`.

Because Forge's approved product goal is a one-stop content workspace and Content Admin is intended to be first-class, the phase-2 design freeze should evaluate role/context-aware promotion of those destinations rather than treating the current `Home / Work / Capture / Jobs / More` proposal as settled.

The current Quest Studio foundation's standalone palette must not survive final absorption. In particular its orange `Compile` control must be remapped into the unified operation/semantic token system so compilation cannot visually resemble LIVE WRITE or PUBLISH. This is expected integration work, not a defect in Fable's plan.

---

## 5. Baseline drift observed during review

This does not invalidate the frozen audit target, but integration must not reuse old heads silently.

At review start:

- live `tnr-tools/main` = `6848a7805d912378f7f8eb27f52c9625dd10ac54`, advanced from the planning base `305a28f...`;
- live `studie-tech/TheNinjaRPG/main` = `1e01028cdd68459b731001dc98d78bf1970cd7f1`, 29 commits ahead of the source head `36c5873b...` used by the planning pass.

Fable's proposed Phase-0 drift gates are exactly the right response. Before an implementation brief is frozen, re-run the source relevance/contract drift checks and compare current `main` against both reviewed branches. Do not assume the frozen planning evidence is a current source pin.

---

## 6. Required correction and cross-review sequence

1. **Fable keeps the frozen review target intact** and applies accepted findings only after the review is released, on its own branch.
2. Fable reduces/splits K so director decisions contain only actual director-owned choices; engineering mechanisms move into architecture/phase gates.
3. Fable removes the false Phase-0 director blockers and corrects the one-writer interpretation.
4. Fable reconciles stale evidence/handoff summaries.
5. **Fable independently reviews** `chatgpt/forge-quest-studio-foundation@cda8ac76100b2fa4b5429bea27c3c8c80353e240` using its handoff/adversarial checklist. ChatGPT does not self-approve that implementation.
6. ChatGPT applies accepted Quest Studio findings on the ChatGPT-owned implementation branch and freezes a new SHA if corrections are required.
7. Fable then refreshes its Studio evidence/citations against the final accepted implementation SHA rather than `824c4d58`.
8. Reverify current `main` and current TNR source head.
9. Freeze a concise **unified implementation contract**: Fable's `ForgeCore`/roadmap architecture + the director-approved Forge visual/product direction + the reviewed Quest Studio seam.
10. Implementation ownership returns to Fable by default for the unified Forge work unless the director explicitly assigns another ChatGPT slice.

Do **not** blind-merge the two frozen branches. The desired result is one product: preserve the working Quest Studio protocol/compiler seam, absorb its UI into the headless-core/shared-shell architecture, and make Fable's corrected plan reference the final accepted implementation evidence.

---

## 7. Final review disposition

**No rejection of the architecture. No live-game safety blocker found in the planning package.**

The package is suitable to become the Forge Next engineering plan after F1-F4 are corrected and the concurrent Quest Studio implementation has completed its independent review/reconciliation.

**Disposition:** `APPROVE_WITH_REQUIRED_CORRECTIONS` — integration to `main` should wait for those corrections and the cross-review loop.