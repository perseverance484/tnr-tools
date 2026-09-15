# Forge Next planning — correction re-review

**Status:** INDEPENDENT RE-REVIEW — ARCHITECTURE APPROVED; FINAL RECONCILIATION REQUIRED BEFORE INTEGRATION  
**Date:** 2026-09-15  
**Reviewer:** ChatGPT — Engineering Auditor lead, UI/UX Reviewer supporting lens  
**Reviewed branch:** `claude/forge-next-planning-v3frzi`  
**Reviewed exact SHA:** `22f1fc43f8e316d0ec8412d5595a7cd0936f98d0`  
**Original reviewed SHA:** `201a1e2ea57011440e164f84a0ed30298fa4b243`  
**Declared planning base / merge-base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Live `tnr-tools/main` at re-review:** `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`  
**Live `studie-tech/TheNinjaRPG/main` observed:** `ebb914cbd5307782a659db09b55225d3f4bbd179`  
**Live-game requests/writes:** none

## 1. Verdict

**The original high-severity planning findings are closed. The architecture remains approved.**

Fable materially corrected the package rather than renaming the old problems:

- director, split and engineering decisions are now separated;
- fifteen implementation choices are explicitly Fable-owned engineering positions rather than director questions;
- Phase 0 has no director blocker and now begins from objective, reviewable prerequisites;
- the one-writer rule is correctly treated as one writer per active branch, not one file per branch;
- stale parity counts were regenerated from the final rows and the handoff now describes the second correction pass explicitly;
- the headless `ForgeCore` first / incremental shell replacement architecture remains compatible with the approved Forge product direction and the Quest Studio seam.

Two residual issues remain before the planning package itself should be integrated. Neither changes the recommended architecture or the implementation roadmap. The first is the cross-review dependency already identified by the original review; the second is a small audit-metadata overclaim.

**Disposition:** `APPROVE_WITH_FINAL_RECONCILIATION`. No further broad planning pass is required. After Fable narrowly re-reviews the corrected Quest Studio SHA, update the Studio provenance/preconditions and the small evidence-generator wording, then the package is suitable for the unified implementation-contract step.

## 2. Original findings re-checked

### F1 — CLOSED — decision ownership

`K_USER_DECISIONS.md` now defines director, split and engineering classes. Fifteen entries carry Fable's engineering position and explicitly block no director freeze; five mixed rows isolate only the director-owned consequence. The downstream roadmap and generated wireframes were also corrected so engineering rows are no longer presented as director blockers.

The package additionally discloses four conservative ownership extensions instead of pretending the repository already reserved them. That is acceptable for planning: operator-facing UX, credential blast radius and public persistence have material operator/security consequences, while the document explicitly says the director can collapse those extensions back to engineering ownership. No implementation is blocked by hiding an engineering choice inside a ruling.

### F2 — CLOSED — false Phase-0 blockers / one-writer interpretation

Phase 0 now states **User decisions: None**. Its prerequisites are objective conditions: re-measure the baseline, re-run source drift, name one implementation owner/branch, and record Fable's bundle/release approach for review. K-13, K-14 and K-60 are engineering positions, not director rulings.

K-60, section F, section G, the risk register and affected wireframes now correctly treat the one-writer rule as branch ownership. Cross-branch overlap is an integration concern, not a director assignment question.

### F3 — PARTIALLY CLOSED / SEQUENCING CONDITION — Quest Studio provenance

The package did the right first half: `00_CONTEXT.md` §00.6 measures the difference between the original `824c4d58` evidence snapshot and `cda8ac76` instead of silently upgrading evidence, and it adds a requirement to re-resolve Studio citations at the accepted implementation SHA.

However, the corrected planning tree now also contains `docs/reviews/FORGE_QUEST_STUDIO_FOUNDATION_REVIEW.md`, which proves that Fable **did** review `cda8ac76`. Several reconciliation passages still say that review "has not been performed" or that the accepted SHA cannot be known until that review occurs. Those statements are now stale.

More importantly, ChatGPT has since applied the accepted implementation corrections and frozen the corrected Quest Studio at `chatgpt/forge-quest-studio-foundation@b536bbe5306f14f606d889d8234e537f0d55b300`. Fable has not yet narrowly re-reviewed that corrected SHA. Therefore the planning package cannot honestly replace its `824c4d58`/`cda8ac76` references with a final accepted Studio SHA yet.

This is a workflow dependency, not a planning-architecture defect. Once the narrow Studio re-review closes, Fable should update the planning package exactly once to the accepted SHA and re-resolve the affected citations/claims.

### F4 — MOSTLY CLOSED — stale audit metadata

The parity matrix's headline counts now agree with its row-derived machine tally, and the handoff's evidence/wireframe counts were refreshed. `evidence/gen_evidence_summary.py` uses checkout-relative paths, so the portability defect is fixed.

One small statement remains inaccurate: `00_CONTEXT.md` and the handoff say the generator rebuilds **both matrices' summary strings**. The script assigns `d['summary']` only for `parity-matrix.json`; for `admin-feasibility.json` it updates `verification.method` and `verification.scope_note`, not `a['summary']`.

The admin summary appears internally coherent and this does not affect any conclusion. Fix either the prose (recommended) or make the generator actually own that second summary. Do not leave an audit handoff claiming a producer owns data it does not produce.

## 3. Residual finding R1 — MEDIUM — Studio review state and Phase-S preconditions are internally stale

**Invariant:** a planning package that gates implementation on exact-SHA review must describe the actual review state and must not make a superseded SHA look like the future integration target.

**Evidence:**

- the corrected tree commits `docs/reviews/FORGE_QUEST_STUDIO_FOUNDATION_REVIEW.md`, reviewing `cda8ac76`;
- `docs/handoffs/FORGE_NEXT_PLANNING_HANDOFF.md` §1.1 still says that review "has not been performed";
- `00_CONTEXT.md` §00.6 similarly treats review of `cda8ac76` as future work;
- `G_ROADMAP.md` G.0 still names `cda8ac76` as the frozen implementation review target;
- G.0 enumerates four Studio preconditions (a,b,c,d), but the Phase-S detail says "All three preconditions in G.0" and omits the citation re-resolution condition;
- the implementation owner has since frozen corrected Quest Studio at `b536bbe5...`, which has not yet received Fable's narrow correction review.

**Practical consequence:** if merged now, the plan would preserve a false review-state narrative and could send a future implementer toward the superseded Studio review target rather than the corrected accepted seam.

**Smallest robust correction:** after Fable reviews `b536bbe5...`, make one reconciliation commit on the planning branch that:

1. names the final accepted Quest Studio SHA;
2. records the earlier `cda8ac76` review as completed historical evidence;
3. resolves every `824c4d58:` cite required by G.0 against the accepted SHA;
4. updates G.0 / Phase S so the precondition count and wording agree;
5. preserves any findings/debt that still survive at the accepted SHA rather than assuming corrections removed them.

Do not reopen the architecture or reimplement the Studio seam.

## 4. Residual finding R2 — LOW — evidence generator ownership is overstated

**Invariant:** generated/audit metadata should identify its actual producer accurately.

**Evidence:** `docs/forge_next/evidence/gen_evidence_summary.py` generates the parity matrix `summary`; for the admin matrix it updates only verification metadata. The package/handoff says it regenerates both summary strings.

**Consequence:** low operational impact, but it undermines the exact producer/provenance discipline the package correctly demands elsewhere.

**Correction:** change the prose to say the generator regenerates the parity summary and both matrices' verification metadata, or extend the generator to produce the admin summary as well.

## 5. Verified strengths preserved

The re-review found no reason to change the original architectural approval:

- headless `ForgeCore` first;
- deeply tested runner/storage/transport/budget/reconcile core preserved;
- UI/domain leakage moved below the seam before shell expansion;
- incremental screen replacement rather than a wholesale rewrite;
- one shared Quest Studio with repository-backed typed operations;
- repository remains authority for contracts/scripts/provenance rather than browser duplication;
- compile/build stays separate from live execution;
- Builder retirement remains gate-driven;
- Content Admin capability is separated from authority/publishing decisions;
- safety states remain machine-sourced and ambiguity is not rendered as success.

## 6. Baseline drift

The planning package deliberately remains evidence pinned to its original base; it should not be rewritten continuously as Lane B advances `main`.

For the next implementation brief, however, the baseline must be refreshed. At this re-review:

- `tnr-tools/main` = `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`;
- `studie-tech/TheNinjaRPG/main` = `ebb914cbd5307782a659db09b55225d3f4bbd179`.

The current upstream TNR head includes further browser/session work, so Phase 0's host/auth/source-drift checks are not optional. This is exactly the purpose of the roadmap's standing drift gate and is **not** a defect in the frozen planning evidence.

## 7. Gates/evidence checked in this re-review

This was a narrow documentation correction audit, not a rerun of Fable's original deep-dive workflows.

Checked directly against the frozen SHA:

- exact branch/head and ancestry of the four correction commits;
- changed-file inventory from `201a1e2...` to `22f1fc43...`;
- corrected K ownership tables and representative engineering/split entries;
- Phase-0 prerequisite/user-decision table;
- Phase-S prerequisite wording;
- updated handoff correction ledger;
- parity matrix row-derived headline/tally;
- evidence summary generator source;
- committed Quest Studio independent review now present in the corrected package;
- current `main` and current upstream game head.

GitHub reports no commit-status checks attached to `22f1fc43...`. Fable's correction commits themselves report doctrine/render/pack/law gates green; because this re-review is documentation-only and the two residual findings are visible from committed source, no live/browser/game test was required or performed.

## 8. Next permitted workflow step

1. Keep `claude/forge-next-planning-v3frzi@22f1fc43...` frozen except for the eventual reconciliation correction described above.
2. Fable performs the already-planned **narrow correction re-review** of `chatgpt/forge-quest-studio-foundation@b536bbe5306f14f606d889d8234e537f0d55b300`.
3. If that review is clean, Fable makes the small planning reconciliation commit for R1/R2 and returns one final planning SHA.
4. ChatGPT performs a very narrow readback of that reconciliation only; no third broad planning audit is warranted unless the architecture changes.
5. Re-verify current `main` and current TNR source.
6. Freeze the single unified Forge implementation contract: Fable's ForgeCore/roadmap architecture + the approved Forge UX/product direction + the accepted Quest Studio seam.
7. Fable resumes normal implementation ownership starting with Phase 0.

**Do not blind-merge either historical branch.** The desired integration is one reconciled product against fresh `main`, not the union of two stale branch trees.
