# Planning handoff: Forge Next unified content operations and Content Admin

Per `docs/workflows/IMPLEMENTATION_HANDOFF.md` and `CLAUDE.md` sections 8, 11 and 12, in the ten
fields the planning brief's section 17 requires. This is a **planning** handoff: it freezes a
document package for independent review, not an implementation.

Planning contract: `state/prompt_forge_next_planning.md` at
`chatgpt/forge-next-planning@70c151616f09c6ec729cb05afb30faa2c6331183`.
Mid-pass amendments consumed read-only: the approved visual north star
(`docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` at `chatgpt/forge-next-planning@0bb5a54b1025ba49ff6b09aa9606f23102f4dca3`)
and the consolidated design lane and director rulings
(`chatgpt/forge-quest-studio-foundation@824c4d58075d0265c717ef25c02485614f3096cf`).
Continuation brief: `state/prompt_forge_next_planning_resume_after_ui_recovery.md` at `824c4d58`.

Expect a **full** independent audit of the package, not a narrow re-check. The brief's own words for
what ChatGPT is asked to decide are in field 10.

---

## 1. What this is, and the branch pushed

**Revision.** This is the second frozen handoff for this package. The first froze at `201a1e2ea57011440e164f84a0ed30298fa4b243`, was independently reviewed, and came back `APPROVE_WITH_REQUIRED_CORRECTIONS` with four findings. Section 1.1 below states exactly what changed in response and what did not. Everything else in this document describes the package at this SHA, and every count in it was re-measured for this freeze rather than carried forward.

**One note on how the first draft was produced, kept because a reviewer of the diff will see its traces.** It was written from the package, then the package changed under it: an adversarial critic had produced 85 findings across six lenses, a re-check confirmed 56 already fixed, and the remaining 29 were closed after that handoff was first written. The specific late changes were: the image-supply capability became the eighth hard retirement blocker and gained its gate; the gameAsset verdict moved from partial to yes for record work; the rate-limiter claim, the confidentiality claim and the parse-baseline requirement were each scoped to what the source supports; and three decisions were registered that had been assumptions (K-59, K-60, K-61). Independent review then found that three summary strings still described the pre-correction state; those are fixed at this SHA and field 8.4 records what was actually stale.

**Objective in one sentence.** Produce a durable, evidence-backed plan for a unified Forge that
absorbs the Builder's remaining real work and adds a Content Admin surface, so that the director can
decide what to build, in what order, and what is still theirs to rule.

**What was produced.** Thirteen planning sections (`00_CONTEXT` and A to K) under
`docs/forge_next/`, eleven committed evidence files, seventeen static wireframes with their generator
and seven rendered captures, and the approved concept mockup with its provenance note. No code, no
test, no manifest and no doctrine was written or changed.

| | |
|---|---|
| repository | `perseverance484/tnr-tools` |
| planning branch (pushed) | `claude/forge-next-planning-v3frzi` |
| lane | A (planning only) |
| planning owner | Fable / Claude Code |
| independent reviewer | ChatGPT, Release Auditor lens with UI/UX Reviewer and Engineering Auditor |
| integration target | none yet. This package is reviewed first; implementation is a separate, later, director-approved brief |

**Branch-prefix deviation, stated plainly.** `docs/DEVELOPMENT_WORKFLOW.md` section 3 names
`fable/*` as the normal Fable prefix. This session was assigned `claude/forge-next-planning-v3frzi`
and worked only there. That is a stated deviation for this one branch, not a new convention, and
`00_CONTEXT.md` records it in the same words.

**What explicitly has not begun.** No Forge implementation phase. No phase-0 brief has been
written. No screen, token, component, test or registry row exists anywhere as code. The roadmap in
section G names phase 0 as the only phase that can be briefed first, and it has not been.

---

## 1.1 Correction round 1: what independent review required, and what changed

The first freeze, `201a1e2ea57011440e164f84a0ed30298fa4b243`, was audited by ChatGPT
(`docs/reviews/FORGE_NEXT_PLANNING_REVIEW.md` at
`chatgpt/review-forge-next-planning@a991abc2e6af0dfe25ae06e032541a0b73409e8d`, a branch whose single
commit adds that file on top of the frozen SHA, so the audit target itself is untouched). Disposition:
**architecture approved; package approved with required corrections before integration.** Four
findings. All four are accepted; none required changing a conclusion, a recommendation or the
architecture.

| # | Finding | Accepted | Where the correction landed |
|---|---|---|---|
| F1 | high — the register escalated ordinary engineering mechanisms as director rulings, against `docs/workflows/DIRECTOR_DECISIONS.md` §1 | yes, in full | `K_USER_DECISIONS.md` §K.1 (new) plus a **Class** field on all 59 entries and three index tables; fifteen entries reclassified as engineering and given Fable's position; five split with only their director half waiting; K-60 and K-61 rewritten. Downstream: `G_ROADMAP.md` §§G.0, G.1, G.2.0, G.3, G.4, G.5, G.6; `I_TEST_STRATEGY.md`; `J_MIGRATION_AND_RETIREMENT.md`; `D_VISUAL_SYSTEM.md`; `PLAN_2026-09-12_forge_next.md` §5; §7 of this handoff |
| F2 | high — phase 0 was blocked by K-13, K-14 and K-60, two of which say "Can defer: yes", and the K-60 entry misread the one-writer rule | yes, in full | `G_ROADMAP.md` §G.2.0 now lists four objective prerequisites and **no** director decision; the phase table gained a legend separating director rulings from engineering positions; the one-writer reading is corrected in K-60, G §G.2.0 and §G.4, J §J.1 and §J.3, and I §I.1 in the first round, and in F §F.3, §F.16 and §F.18, H R-22 and the wireframe specs in the follow-up round after a critique found the first pass had reached only the files in its own diff |
| F3 | medium — the package studied `824c4d58`; the implementation froze later at `cda8ac76` | yes, with its scope stated | `00_CONTEXT.md` §00.6 measures the difference rather than assuming it: of the fourteen paths this package cites on that branch, eleven are byte-identical at `cda8ac76` and three changed; every reading survives, and of the twelve line cites into the three changed files four still resolve and eight shift. A phase-S precondition (d) now requires re-resolving every cite at the accepted SHA, which is `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`. The branch's evidence claims have since been independently reviewed and accepted at that SHA |
| F4 | medium — audit-summary metadata was stale relative to the package's own final rows | yes, in full | Both evidence matrices' summary strings are now **generated** from their rows by `evidence/gen_evidence_summary.py`; `verification.method` in both was corrected from "per capability row" to the decisive set; field 8.4 of this handoff now states what was actually stale and which two "defects" the final sections had already fixed |

**A second pass, and why it was needed.** Before this handoff was sent, the round was itself put
through an adversarial critique, which found that the F1 and F2 corrections had reached only the
files in their own diff. Three surfaces still carried the corrected-away reading: `F_ARCHITECTURE_RECOMMENDATION.md`
§F.3 and §F.16 still called the release-loader marker fix "a conflict for the director to assign",
§F.18 still listed every entry as blocking including the engineering ones, `H_RISK_REGISTER.md` R-22
still said two branches touching one test file "breaks the one-writer rule", and four wireframes
listed engineering-class entries under a heading reading "Open director decisions this screen depends
on". All are corrected at this SHA; the wireframes were corrected at their generator source
(`wireframes/src/specs.json` and `src/gen.py`) and regenerated rather than hand-edited (`CLAUDE.md`
§7). Two other defects the critique found are also fixed: `evidence/gen_evidence_summary.py`
hard-coded absolute paths and could only run in one checkout, and the F3 row of the table above
under-counted the shifted line cites. The lesson is worth stating because it will recur: a
correction is not applied until it is applied everywhere the claim appears, and a diff is not a
search.

**What did not change, and why.** The review's section 3 lists ten strengths to preserve; none of
them was touched. The architecture recommendation (headless `ForgeCore` first, then incremental shell
replacement), the retirement gate model, the compile/live separation, the operation-first IA with
content lanes as a second axis, and the safety-state semantics are unchanged at this SHA. The review's
section 4 raises two shell choices — exact destinations, and whether Quest Studio and Content Admin
deserve a primary phone slot rather than `More` — as legitimately open for the phase-2 design freeze.
They already are: K-20 and K-02 hold them, and `D_IA_AND_JOURNEYS.md` §D.1 keeps the alternatives in
full rather than presenting the current proposal as settled. No change was made there, because making
one would settle a director decision by editing a plan.

**What this round did not do, and is not authorised to do.** Step 5 of the review's own correction
sequence asks for an independent review of the Quest Studio foundation. **That review has since been
performed**, across two rounds, and closed at
`chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`
(`claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d`, APPROVE_WITH_NONBLOCKING_FOLLOWUP); it was not performed by this planning round. The
unified implementation contract the review proposes in its step 9 has likewise not been drafted. The
second amendment's constraint still stands and was honoured here: no second implementation stream was
begun from this planning branch.

---

## 2. Exact base and head SHAs

| | |
|---|---|
| base | `main@305a28f992e33194fbba279a3f32e698dfb2b67f` (short `305a28f`), verified with `git fetch origin main` at the start of the pass and again at each amendment |
| previous freeze (superseded) | `201a1e2ea57011440e164f84a0ed30298fa4b243` — the review target of `docs/reviews/FORGE_NEXT_PLANNING_REVIEW.md`. It is left intact in history; this round adds commits on top of it and rewrites nothing |
| head (FROZEN) | the commit that adds this handoff revision. The planning owner reports the exact hash in the message that accompanies the push, read back from `origin/claude/forge-next-planning-v3frzi`, not assumed from an authored commit |
| merge-base with `main` | `305a28f`. The branch has not been rebased and `main` has not been merged into it |

**The SHA, not the branch name, is the audit target** (`CLAUDE.md` section 11). The branch may
receive a correction round after review; every round returns a new exact head SHA under
`docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Until review returns, the frozen head does not
move.

A reviewer can reproduce the whole diff with:

```
git diff 305a28f992e33194fbba279a3f32e698dfb2b67f..<head> --stat
```

and should expect every path to be under `docs/forge_next/`, `docs/handoffs/` or `docs/PLAN_2026-09-12_forge_next.md`. Nothing under `forge/`, `skills/`, `state/`, `docs/design/`, `push/`, `harvests/`, `archive/` or `.github/` is touched, which `git diff --quiet 305a28f..<head> -- <those paths>` confirms.

---

## 3. Every planning artifact created

Taken from `ls` and from the files themselves at the frozen head. Sizes are bytes; the count column
is lines for prose and structured rows for evidence.

### 3.1 Planning sections

| Path | What it is, in one line | Size | Count |
|---|---|---:|---|
| `docs/forge_next/00_CONTEXT.md` | Provenance, pins, boot sequence, method, constraints honoured, package layout | 23,310 | 115 lines |
| `docs/forge_next/A_ARCHITECTURE_MAP.md` | Current state of Forge 0.4.0 and Builder v4.32: module map, data flow, state machines, storage, contracts, safety invariants, bundle facts, the Quest Studio seam read as evidence | 53,593 | 261 lines |
| `docs/forge_next/B_PARITY_MATRIX.md` | Builder to Forge parity: 61 capability rows, 8 hard and 9 conditional retirement blockers, 10 retirement gates with measurable acceptance | 270,547 | 359 lines |
| `docs/forge_next/C_WORKFLOW_INVENTORY.md` | The 25 content workflows that actually run here (W-01 to W-25), each with evidence of real use, today's tooling, and Forge's support | 48,719 | 230 lines |
| `docs/forge_next/D_IA_AND_JOURNEYS.md` | Recommended information architecture for phone and desktop, 32 screens, 7 journeys, mockup element reconciliation, departures | 68,154 | 458 lines |
| `docs/forge_next/D_VISUAL_SYSTEM.md` | The approved visual direction elaborated into tokens, a 25-component inventory, state and motion rules, 17 departures, a 5-slice shell sequence | 126,072 | 776 lines |
| `docs/forge_next/E_CONTENT_ADMIN_FEASIBILITY.md` | Per-class source audit of what a content admin can do with zero game-source change, the role model, the denial-signal audit, publication axes, queue options | 71,331 | 357 lines |
| `docs/forge_next/F_ARCHITECTURE_RECOMMENDATION.md` | Preserve, refactor, replace, abstract or migrate per module; the headless core boundary; brief section 12 answered question by question | 100,170 | 451 lines |
| `docs/forge_next/G_ROADMAP.md` | Nine reviewable Lane A phases (0, 1, 2, 3, S, 4, 5, W, 6) with objective, surfaces, prerequisites, gates, decisions, rollback and retirement impact | 58,274 | 416 lines |
| `docs/forge_next/H_RISK_REGISTER.md` | 31 risks (R-01 to R-31) with evidence, how each would bite, and the phase gate that bounds it | 40,463 | 49 lines |
| `docs/forge_next/I_TEST_STRATEGY.md` | Today's measured suite, the test architecture a larger UI needs, static gates, per-phase gate map, and the nine user-owned browser and live smokes | 48,193 | 251 lines |
| `docs/forge_next/J_MIGRATION_AND_RETIREMENT.md` | Retirement gates G-01 to G-13, the six-stage transition ladder, storage and contract migration rules, how the operator is told | 55,918 | 223 lines |
| `docs/forge_next/K_USER_DECISIONS.md` | The decision register: three rulings recorded as context and one advisory reading the director must still confirm, then 59 entries K-01 to K-61 (K-18 and K-19 unused) split by ownership class — 39 director decisions, 5 split, 15 Fable engineering decisions carrying Fable's position — each with options, consequence, a recommendation or a position, and the phase it blocks | 133,853 | 746 lines |

### 3.2 Evidence

| Path | What it is, in one line | Size | Rows |
|---|---|---:|---|
| `docs/forge_next/evidence/parity-matrix.json` | The parity matrix as data: 61 capability rows plus 10 gate rows, each with citations, tier, blocker verdict and verification state | 566,037 | 71 |
| `docs/forge_next/evidence/admin-feasibility.json` | The Content Admin audit as data: 25 content-class rows (CA-01 to CA-25) and 10 cross-cutting rows (CC-01 to CC-10) | 651,369 | 35 |
| `docs/forge_next/evidence/forge-tests-ci.json` | Test and CI inventory: per-test rows, gap rows, harness rows, totals and the CI workflow shape | 175,959 | 334 |
| `docs/forge_next/evidence/visual-synthesis.json` | The synthesised token set, component inventory, departures, grafted ideas and the alternatives kept | 114,793 | 2 alternatives, 20 grafts, 11 decisions, 22 evidence rows |
| `docs/forge_next/evidence/drift.json` | Game-source drift between the Forge pin and the read head, per surface | 110,143 | 197 |
| `docs/forge_next/evidence/harvest-evidence.json` | The committed record: 42 results bundles, 41 manifests, 23 generator scripts, read row by row | 94,523 | 105 |
| `docs/forge_next/evidence/repo-consumers.json` | Which repository scripts and workflows consume Forge and Builder output, and on which paths | 92,516 | 92 |
| `docs/forge_next/evidence/ux-audit-current.json` | The current Forge UI audited surface by surface against the code | 69,883 | 95 |
| `docs/forge_next/evidence/registry-gap.json` | Procedure registry coverage against the pinned source | 40,864 | 145 |
| `docs/forge_next/evidence/contrast.py` | The one contrast computation every ratio in `D_VISUAL_SYSTEM.md` comes from, so a reviewer can recompute rather than trust | 1,460 | 41 lines |
| `docs/forge_next/evidence/gen_evidence_summary.py` | Regenerates the audit-summary strings in both matrices from their own rows, so a prose tally can never drift from the data again (added in correction round 1, review finding F4) | 5,006 | 76 lines |

### 3.3 Wireframes and design reference

| Path | What it is, in one line | Size or count |
|---|---|---|
| `docs/forge_next/wireframes/index.html` | Index of every screen plus the theme token tiles | 31,922 B |
| `docs/forge_next/wireframes/README.md` | What the set is, what is open, how to regenerate, and that nothing contacts a host | 1,307 B |
| `docs/forge_next/wireframes/wf01_command_center.html` to `wf17_degraded_states.html` | Seventeen screens, each showing phone 390 and desktop 1280 in one self-contained page with inline CSS and no external resource | 17 files, 21,887 to 26,732 B each |
| `docs/forge_next/wireframes/src/{build_specs.py, gen.py, specs.json, themes.json}` | The generator: `build_specs.py` rebuilds `specs.json`, `gen.py` renders it with `themes.json` | 4 files, 214,471 B total |
| `docs/forge_next/wireframes/review/*.jpg` | Rendered captures of 7 of the 17 screens (wf01, wf04, wf06, wf11, wf13, wf14, wf17) at 1400 px, for reviewers without a browser | 7 files |
| `docs/forge_next/design/forge_next_concept_mockup.jpg` | A compressed copy of the director-approved concept mockup, committed so the reference does not depend on a chat attachment | 248,720 B |
| `docs/forge_next/design/README.md` | Provenance of the mockup and the rule that nothing in it may be inferred to exist | 880 B |

### 3.4 Cross-referenced but not on disk at this SHA (forthcoming or external)

A reviewer should not look for these in the tree. Each is named because a section cites it.

| Cited artifact | Cited by | Status |
|---|---|---|
| `scratchpad/design/*.json` panel inputs | D.0, F.0, F.1 and D2.11 name the options the recommendations were weighed from | **Committed since.** The seven options and the three superseded visual explorations are at `docs/forge_next/evidence/design-options/`, with a README saying what each argues and what is absent. The judge files for the visual family and the scratchpad working files are not committed |
| `scratchpad/design/synth-arch.json`, `synth-data.json` | F.0 names them as absent | **Do not exist.** F says so in its own words: panel synthesis unavailable, recommendation derived by the planning owner |
| `evidence/admin-verdicts.json` | E.1 names it as absent when E was written | **Not committed.** The per-row adversarial verdicts were folded into `evidence/admin-feasibility.json` instead; E.1's tally is the statement of record |
| `docs/design/FORGE_NEXT_*.md` (the Tier A to E design lane, about 20 files) | Every section, by the abbreviations SSC, MOB, WCM, WFA, SCR, IRM, CPY, ICN, SCN, ACC, COL, VD, QS, RB, AUD, HND, IDX, MS, SBI, RCM, DS, EXP, WSP | **External by design.** They live on `chatgpt/forge-quest-studio-foundation@824c4d58` and are cited by SHA. They are not on this branch and must not be looked for on the older `chatgpt/forge-next-planning` branch either |
| `state/prompt_forge_next_planning.md` | The planning contract | **External by design.** `chatgpt/forge-next-planning@70c1516`. Absent from this branch's disk |

---

## 4. The recommended architecture and information architecture, in plain language

This is the one page a reviewer should be able to read without looking anything up. The detail is
`F_ARCHITECTURE_RECOMMENDATION.md` and `D_IA_AND_JOURNEYS.md`.

### 4.1 The architecture

**The part of Forge that does the dangerous work is the part that should not change.** Everything
below `forge/src/ui/` (journal, transport, rate budget, runner, reconciler) is already independent of
the screen and carries 277 of the 293 existing tests. The thin part on top carries 16 tests and
holds work that does not belong to a screen: it builds the results bundle, decides which paths auth
blocks, materialises capture bodies, and caches repository listings in the game read cache.

**So the recommendation is: move that work down first, with the screens unchanged, and only then
change the screens, one at a time.** Concretely:

1. **Extract a headless core.** Create `forge/src/core/` inside the existing composition root, so all
   293 tests protect it from the first commit. Move the ten leaked pieces down. The acceptance test
   is mechanical: a serialised copy of today's five screens, committed before the move, must come
   back byte identical afterwards.
2. **Then replace the shell against that core, screen by screen**, keeping the CSS class names the
   existing tests select on, so each slice is separately reviewable and separately revertible.
3. **Touch the execution core exactly once**, to add an advisory progress event beside the logging
   callback the runner already has. It may not write the journal and may not advance an item state,
   and an adversarial test asserts that a subscriber which throws leaves the journal bytes, the write
   order and the state transitions identical.
4. **Keep storage rollback safe.** Repository text moves out of the game capture database into a
   separate database rather than raising the existing database's version, because rolling a release
   back is re-pinning the loader, and an older bundle cannot open a newer database.
5. **Close one latent hole**: the element helper assigns any non-string value to a matching element
   property, which for the key `innerHTML` is an HTML sink that neither the build gate nor the source
   grep can see. It is unreachable today and becomes reachable the moment fields are rendered from a
   generated contract, so the helper gains a deny list.

Sixteen modules are preserved unchanged or changed only additively. Four are replaced or split, and
all four are under `forge/src/ui/`.

Two alternatives were weighed and kept rather than deleted: evolving the current UI in place (cheapest,
but leaves the boundary a convention rather than a checked rule), and replacing the UI layer in one
bet (strictest diff, but rewrites the thinnest-tested layer wholesale and roughly doubles the bundle
the phone parses on every matched game page).

**The boundary rule that sits over all of it**, from the director's ruling: the repository keeps the
facts, contracts, profiles, scripts, validators and provenance; Forge translates, orchestrates and
presents. Forge may call approved repository operations and may show repository state. It may never
become a second copy of it.

### 4.2 The information architecture

**The first thing the operator chooses is the consequence, not the content type.** The top level is
what this action will do to production; content type is a filter and an entry point underneath it.

The reason is measurable rather than aesthetic. Forge already computes read-only versus mutating from
the parsed plan, so an axis built on it cannot drift from the truth. A content-type axis cannot be
computed for a package that carries two entity types, and the committed record is full of packages
that mix reads and writes. The most frequent real work is reading, and it carries no risk; the rarest
work is publishing, and it carries the most. Operation-first gives the frequent thing the shortest
path and gives publishing its own place, its own colour and its own confirmation.

Eight desktop destinations in four groups: Command Center, Capture and Research, Build and Update,
Quest Studio, Content Admin, Jobs and Recovery, Projects, Settings. Every one of them is fed by state
Forge already holds, so opening a destination costs nothing against the game's rate limit.

On the phone, five bottom items plus a More sheet: Home, Work, Capture, Jobs, More. No horizontal
scrolling navigation. A destination may carry a badge; a badge never moves the operator.

Thirty-two screens are inventoried. Seven journeys are written end to end, each naming the scenarios
it covers and marking a step HOLD where the capability does not exist yet rather than writing it as a
deliverable.

Four structural choices are worth naming because they change what the director saw in the mockup:
the recovery decision renders on the job that produced it rather than in a separate place; there is
no operator destination for "create content" or "validate", because authoring is the Studio and
validation is a step of a package; preview is scoped per content class, because a player-facing
renderer honestly exists for some classes and not others; and on a phone the Command Center puts
attention above the hero.

Nothing in the IA freezes a label, a lane name or a colour. Those are the director's, and they are
listed in field 7.

---

## 5. Builder parity headline, and the remaining retirement blockers

Source: `B_PARITY_MATRIX.md`. Sixty-one capability rows cover every meaningful behaviour of
`builder_bundle.js` v4.32 and `forge/src` 0.4.0 at `main@305a28f`.

### 5.1 The tallies

| Parity status | Rows |
|---|---:|
| FORGE BETTER | 24 |
| PARITY | 8 |
| INTENTIONAL DIFFERENCE | 6 |
| GAP | 23 |
| total | 61 |

| Retirement blocker | Rows |
|---|---:|
| yes (hard) | 8 |
| conditional | 9 |
| no | 43 |

| Verification at this SHA | Rows |
|---|---:|
| CORRECTED by an adversarial verifier | 29 |
| not verified (outside the decisive set) | 32 |

**In plain language.** Forge is the safer tool on 24 capabilities and matches the Builder on 8 more,
so the direction is not in question. But 23 capabilities have no Forge path at all, and 8 of those
are load-bearing parts of how content is actually made or repaired today. The pattern is not exotic:
it is how a package and its images arrive, how research is read, and what happens when a run goes
wrong. Forge was built to make writes safe; the Builder is still the only tool that can read broadly
and repair.

**Read `CORRECTED` carefully.** Verifiers were told to return `CONFIRMED` only when every cited
location says exactly what the row claims, and a row carries roughly fifteen cells. One tightened
count moves a whole row to `CORRECTED`. The distribution is a property of the bar, not a defect rate.
Rows marked `not verified` are the merge agent's finding and must not be read as audited.

### 5.2 The eight hard blockers

| Id | Capability | Why it blocks, in one line | Gate |
|---|---|---|---|
| P-06 | Zip push packs (manifest plus image members loaded as one unit) | Every asset create in the committed record rode a pack; repository doctrine mandates the pack; the remaining art lanes each plan one | G-01 |
| P-07 | The `imgSizes` byte ledger: pack integrity and size-based file matching | A safety function guarding an irreversible side effect, used on every image-bearing package | G-01 |
| P-08 | Image supply for `@img` references (pack lane plus the multi-file picker) | Forge offers a per-reference picker only | none |
| P-10 | Read procedures Forge cannot issue, inside and outside the audited registry | Proven current research use with no Forge path; two already-audited list reads are refused by Forge's reader as well | G-02 |
| P-11 | Paged and filtered list captures with an input | A proven work shape with no Forge path, whose current failure discards the run's bundle; no census can be reproduced | G-03 |
| P-12 | Capture bodies in the results bundle for every read | The census-to-generator loop depends on bodies Forge cannot export, and the two committed research manifests are unrunnable on Forge at all | G-03 |
| P-21 | `srcId` idempotency across runs | Re-running a finished create-bearing manifest duplicates live records in Forge, irreversibly and near-silently | G-06 |
| P-45 | Retry or re-send of a failed step | `FAILED` is terminal in the journal and the run loop; the only remedy today is a hand-authored edit manifest committed to `push/` | G-06 |

### 5.3 The nine conditional blockers

Each blocks only under a stated condition, and the condition is part of the row rather than a caveat:
**P-02** manifest input from the device, **P-13** field projection and scope annotation, **P-23**
quest fetch-merge and partial-edit shapes, **P-33** enum, bounds and flow-graph preflight, **P-36**
the preflight escape hatch, **P-40** whole-record pushed-versus-live diff, **P-50** bundle download
without a credential, **P-55** id-map import and reset, **P-58** capture evidence honesty for
null-returning reads.

### 5.4 The gates

Thirteen. G-01 to G-10 are owned by `B_PARITY_MATRIX.md` section B.4. G-11, G-12 and G-13 are added
by `J_MIGRATION_AND_RETIREMENT.md` section J.1, because a capability row cannot carry a persistence
tier, the ingress surface as a whole, or a repository guard that breaks on Forge output.

| Gate | What must be true | Phase that measures it | Stage it opens |
|---|---|---|---|
| G-01 | Zip push packs run in Forge with byte-ledger verification | 3 | 2 |
| G-02 | The audited registry covers the procedures real research uses | 1 | 2 |
| G-03 | Paged and filtered list captures with persisted bodies | 1 | 2 |
| G-04 | Partial quest edits without an escape hatch | 3 | 2 |
| G-05 | Enum and task-vocabulary preflight derived from the pin | 3 | 2 |
| G-06 | In-tool recovery: retry, safe re-run, id-map import and reset | 3 | 2 |
| G-07 | Evidence preservation and honesty | 1 | 2 |
| G-08 | One live write proven through Forge, committed as a bundle | operator tap after phase 0, verified in 6 | 1 |
| G-09 | Gates green on `main` | 0 | 1 |
| G-10 | The retirement ruling and loader decommission | 6 | 5 |
| G-11 | Research-read tier: (a) export refuses above tier, (b) the tier ships | 1 | 2 and 3 |
| G-12 | Ingress parity: every legitimate arrival path is reachable or has a written disposition | 3, Studio half in S | 3 |
| G-13 | A Forge results bundle no longer breaks the repository's own session guard | 0 | 1 |

Six gates cannot close without a user decision: G-02 and G-11 need K-17 and K-06; G-04 needs K-59;
G-06 needs K-16; G-12's Studio half needs K-39; G-10 needs K-11. The rest are measurable by Fable or
closed by one user-controlled live tap.

**Retirement timing is the director's (K-11) and is not proposed here.** The transition ladder in
section J has six stages and keeps the Builder installed and pinned until stage 5, because the
failure mode is asymmetric: another month of the Builder costs nothing measurable, one gate too early
strands real work.

---

## 6. Content Admin feasibility headline

Source: `E_CONTENT_ADMIN_FEASIBILITY.md`, built on seven independent readers over the game source at
two read-only checkouts, committed as `evidence/admin-feasibility.json`.

**The headline.** For every class Forge touches today, plus guide and badge, the whole loop of draft,
review, edit, publish and delete is composed **entirely of procedures that already exist**. There is
no publish toggle anywhere in the content routers: publishing is a whole-record update with the
lifecycle field set. **Twenty-two of the 25 content-class rows are `YES` for zero game-source change,
three are `PARTIAL`, and none is `NO`.**

### 6.1 Zero-game-change verdict per class

| Id | Class | Lifecycle field | Verdict | The reason, in one line |
|---|---|---|---|---|
| CA-01 | jutsu | `hidden`, default false | **YES** for the whole loop | Every read is public, every mutation exists; the placeholder is born visible and shielded only by its type |
| CA-02 | item | `hidden`, create inserts true | **YES** | Reads public, clone present; the recipe uses the plain read, so crafting requirements are not round-tripped |
| CA-03 | bloodline | `hidden`, create inserts true | **YES** | Hidden excludes from the roll pool but not from purchase by id, which is a server gap, not a Forge one |
| CA-04 | gameAsset | `hidden`, default **true** | **PARTIAL** | Record CRUD yes; **no publish step may be built**, because engine law 16c rules that the flag affects listing only and that no unhide step should exist. Bytes are partial: Forge speaks only the 512 KB upload slug |
| CA-05 | quest | `hidden`, create forces true | **YES** for list, read, edit, publish, clone and delete | No native audit read and no server preview, so Forge must own both |
| CA-06 | AI | **none**; containment flags only | **YES** | CRUD and containment flips are existing procedures and per-record history is readable; there is no draft state at all |
| CA-07 | AiProfile | none; activation is a pointer | **YES** | Read, edit and toggle all exist, and Forge reads before toggling so it never flips an active pointer |
| CA-08 | guide article | `published`, default false | **YES at the game head, impossible at the Forge pin** | The entire class is post-pin: no router, validator, table or constant exists at `345d18ac` |
| CA-09 | badge | none | **YES**, the simplest class | Three keys and the same placeholder-then-update shape as the six existing recipes |

The other sixteen staff-managed classes the readers found (CA-10 to CA-25) are compressed in section
E.2f. Two further `PARTIAL` verdicts sit there: **CA-12** sector maps (the only first-class lifecycle
enum in scope, with a dedicated publish procedure) and **CA-21** jutsu reskin moderation (owner-scoped
at the server, so a cross-user queue is impossible). **CA-23** content backups is `PARTIAL` because
triggering a snapshot is limited to four backup-control roles, and it is not a restore mechanism at
all. Two rows are feasible but do not belong in a Content Admin surface on ownership grounds rather
than capability grounds: **CA-25** balance knobs and **CA-17** ranked-season rewards are user-owned.

### 6.2 The role-denial finding

This is the finding the director asked for, and it is the one place where the honest answer is "less
than was hoped".

- **There is no role middleware anywhere.** Every content role check runs inside the resolver against
  a twelve-role permission list. Role lives in a database column, not in a session claim. The
  practical consequence is that a Forge surface can only ever **narrow** what the game allows, and it
  cannot know the role without asking.
- **A denial is per procedure, not per session.** The same signed-in account is authorised for some
  paths and not others. **So a fifth session-level "not authorised" lamp has no source behind it**,
  and none is proposed.
- Content mutations answer a role miss with HTTP 200 and a message string. **There is no error code on
  that path.** A per-action denial label is supportable for exactly thirteen paths, and only by
  matching the message text, which is the same prose-coupling failure mode the register carries as a
  risk: a wording change upstream silently downgrades the label.
- For four further paths the same message is also returned for a missing record, and for three more
  the message conflates a role miss with not being the owner. **On those seven the label would be
  wrong some of the time and must not be rendered.**
- **There is a real hazard in the two families that do carry a machine-readable code.** Forge maps the
  code `UNAUTHORIZED` to its session class and moves the whole session to signed-out. Those are
  exactly the paths a naive adoption would mis-report as a lost session, so a role pre-check is
  required before any of them is adopted.
- **The robust mechanism is a pre-check, not a classification.** Read the role once per session
  through one same-origin profile read, hold it in memory only, never persist it, and use it to
  disable the actions the role cannot perform. That makes the state renderable pre-emptively ("this
  account cannot publish") instead of explaining a failure after the fact.

Whether any authorisation label is rendered at all stays **K-34**.

### 6.3 What would need a game change

None of these is planned as a deliverable. Each is recorded with the zero-change fallback that is
used instead: a partial publish toggle; optimistic concurrency on update (no procedure checks a
version, so two admins silently overwrite each other); audit rows on create and clone; three classes
added to the loggable set; role-gated draft reads; a role endpoint; **a native approval field, which
does not exist on any class**; a draft flag on AI records; a server-side quest preview; per-record
restore; privileged columns removed from the AI validator; and owner scoping fixed on reskin
moderation.

Three cross-cutting facts the product must not misstate. **Hidden does not mean secret**: for six of
the seven Forge classes any account can read an unreleased record by id and list unreleased records
by asking for them, and the confidentiality is page-level only. **An upload is not final when the PUT
returns**: the slug Forge uses runs moderation after completion and a flagged image is deleted,
leaving a record pointing at nothing. **There is no approval state anywhere in the game**, so approval
metadata has to live in the repository and must never be read as the record's live state.

---

## 7. User decisions required before implementation

Source: `K_USER_DECISIONS.md`. Fifty-nine entries are registered, and §K.1 there classes each one.
**Forty-four hold something the director owns** — thirty-nine director decisions and the director halves
of five split entries — and those are the list below. **Fifteen are Fable's own engineering decisions**
and carry Fable's position rather than a question; they are named per phase so a brief cannot forget
them, and they block no freeze. That split was made in response to review finding F1 and changed no id.
Nothing in this package settles a director decision, and every recommendation that depends on one says
so by id.

### 7.1 Ruled during the pass, carried as context

| Ruling | What it settles | Canonical owner | What stays open under it |
|---|---|---|---|
| Visual north star, 2026-09-12 | A TNR-specific dark operations console, crimson, gold and cool blue over deep navy, strong Forge branding, Command Center home, content lanes, a first-class Content Admin, controlled motion, explicit operation contexts | `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` section 12 at `chatgpt/forge-next-planning@0bb5a54b` | exact labels, destinations, lane taxonomy, tokens, type scale, geometry |
| `RUL-2026-09-12-001` | One shared Quest Studio with subtype adapters; Mission is a subtype, not a parent product; routine compile needs no chat or file relay; live execution stays an explicit user action | `docs/design/FORGE_NEXT_QUEST_STUDIO.md` at `824c4d58` | K-25, K-26, K-27 |
| `RUL-2026-09-12-002` | Forge is the translation, orchestration and presentation layer; the repository owns facts, contracts, profiles, scripts, validators, provenance and generated artifacts; local projections are never a second canon | `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` at `824c4d58` | K-28, K-29 |
| `RUL-2026-09-12-002` applied to the expansion study | Forge is the primary human content-development workspace; project and authoring workflows are product scope, not helper utilities around the runner | same, section 1 | K-28, K-29, K-24 |

**A process point the reviewer should weigh.** None of these three is recorded in `docs/RULINGS.md`
on `main@305a28f`, which ends at `RUL-2026-09-08-007`. Two are recorded on a branch that has not
merged; one is documented only in a design file on another unmerged branch. Recording them in the
repository's own ruling history is an outstanding step, and it belongs to whoever integrates that
branch, not to this package.

### 7.2 Open decisions, grouped by what they block

| Blocks | Decisions |
|---|---|
| **Phase 0** (foundations, the only phase that can be briefed first) | **none.** K-13 (pin refresh), K-14 (minified bundle) and K-60 (the release-loader baseline fix) are engineering positions the phase-0 brief fixes and review checks. What phase 0 waits on is objective: a green or explicitly isolated `main`, a re-run drift check, a named owner and branch, and a written bundle and release approach |
| **Phase 1** (research and capture) | K-06 what classes of captured data may persist to a public repository, K-17 which non-content procedures Forge may read at all. Both are split entries: the tier mechanism and the per-row audit under them are engineering |
| **Phase 2** (shell and design system) | K-02 navigation model, **K-20** destinations and labels, **K-21** operation-mode taxonomy, **K-22** mode colours and tokens, **K-23** typography scale, **K-24** lane taxonomy, K-31 background art, **K-32** semantic button variants, **K-33** mode derived or selectable, K-56 wordmark, K-57 whether a light theme exists, K-58 which actions keep the browser's own confirmation. K-01 is ruled; token acceptance at the phase-2 freeze is what remains under it |
| **Phase 3** (manifest experience and recovery) | **K-12** publishing UX and confirmation level (wording half), K-15 whether the admin's device holds a credential at all and its scope (the sync mechanism under it is engineering), K-16 deletion policy for placeholders and orphans, K-59 the operator remedy for server-owned columns |
| **Phase S** (Quest Studio) | K-26 the credential scope on the operator's device (the trigger model under it is engineering), K-27 adapter rollout order, K-46 graph editing depth, K-49 policy override workflow, and K-15 jointly with K-26. Engineering positions this phase's brief fixes: K-25 source schema, K-36 canonical profile-shape enforcement, K-37 branch namespace and retention, K-38 worker refusal observability, K-39 promotion gate, K-40 how project state references a build, K-50 adapter boundary |
| **Phase 4** (Content Admin read and review) | K-03 permission scope, K-04 arbitrary writes or editorial only, K-05 which classes get first-class forms, K-08 direct edits or a staged package, K-09 where approval state lives, K-10 whether any game-source change is acceptable, K-16, K-34 whether the product carries authorisation vocabulary at all, K-53 whether balance-bearing classes appear at all. Engineering positions the phase-4 brief fixes: K-47 review annotations, K-52 which role lookup the surface uses |
| **Phase 5** (publish) | K-07 which operations are eligible for few-tap publish, K-12, **K-30** late admin and publish visual details, K-54 whether the product says plainly that hidden is not secret, **K-55** whether a delegated admin performs the publish act at all |
| **Phase W** (project workspace) | K-28 how much project state Forge may edit, K-43 project creation scope, K-44 lifecycle vocabulary |
| **Phase 6** (retirement) | K-10, K-11 timing of deprecation and removal |
| **Ordering rather than a phase** | K-42 confirm the flagship end-to-end workflow |
| **Not scheduled by this roadmap** | K-29 Guide Studio and the infographic lane, K-41 how art files enter packaging, K-45 when feedback becomes a task, K-51 an AI assistance layer. K-35 (`ABORTED`) and K-48 (reuse search) are engineering positions with no phase |

**Two decisions bind more than one phase.** K-55 is a doctrine question about whether a delegated
Content Admin performs the publish act at all, so no phase may assume its answer and phase 5 is
written to be buildable either way. K-15 and K-26 decide one credential on one device across phases 3
and S together, so ruling them separately would leave one phase planning around a scope it does not
have.

### 7.3 The decisions pending the predecessor transcript

Eight entries, plus one half of a ninth, are open **solely because the predecessor-transcript
reconciliation had not landed at `824c4d58`** (the UI context handoff on that branch still reads
TRANSCRIPT RECONCILIATION PENDING with no filled recovered-state section). This package therefore
does not read the later style board as a ruling, and every style-board delta stays a labelled
question rather than a settled value:

**K-20** destination lists and labels, **K-21** operation-mode taxonomy including whether Review is a
mode, **K-22** mode colours, tokens and hex values including the board's Critical tier, **K-23**
typography scale, **K-24** content-lane taxonomy, **K-30** late Content Admin and publish visual
details, **K-32** semantic Success and Warning button variants, **K-33** mode selectable or derived,
and **the wording half of K-12**.

All nine block the phase-2 freeze or the phase-5 copy. They are the answer to the continuation
brief's request to identify what remained pending only because the transcript was unavailable.

---

## 8. Evidence and source pins inspected

### 8.1 Source pins

All game-source reading was done on read-only clones of the public repository
`studie-tech/TheNinjaRPG` in the session scratchpad. Nothing was executed from any checkout, and no
request was made to any game host.

| Role | Commit | What it governs |
|---|---|---|
| Current upstream head (read for drift) | `36c5873b7b6ee5fd3af717008d7c51b0f185b756` (2026-09-12) | 81 commits after the Forge pin, 170 after the task pin |
| Forge global pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` | every Forge engine fact, the derived field sets, the 43-row procedure registry |
| Protected-auth task pin | `bdec2883748f029a0ecb93505adfdcbae6851fe9` | the auth table, proven identical to the global pin |
| Generated `45c/45d/45e/45f/45g` provenance | `bdec2883` | older than the Forge pin |
| Sentinel drift signal | `98d0eca5c2e922f3b41e56120f096c072645c1f0` | item farm fields and a quest field now required; guide constants added |
| Last Forge relevance check on record | game `main@62af1b3405b10183b31f838c9a5f131d790460f1` (2026-09-09) | the byte-identical regeneration of the derived contracts |

Repository release state at the base: both loaders pin the same immutable bundle commit
`ce603def204f585d23837121b86cfdd9fd4c308c` through jsDelivr, set by the automatic pin commit
`d1dbecc`.

### 8.2 The two ChatGPT SHAs consumed read-only

| SHA | Branch | What was taken from it | How it was handled |
|---|---|---|---|
| `0bb5a54b1025ba49ff6b09aa9606f23102f4dca3` | `chatgpt/forge-next-planning` | The approved visual direction (the mid-pass north star) and the concept mockup | Exported into the session scratchpad and read as a new planning input. **Not merged, not rebased onto, nothing on it modified** |
| `824c4d58075d0265c717ef25c02485614f3096cf` | `chatgpt/forge-quest-studio-foundation` | The two director rulings, the routing index with its authority tiers, the ten architecture-neutral UX and safety contracts, the Tier B product proposals, the continuation brief, and the Quest Studio foundation implementation | Same. Read as **architecture and roadmap evidence only**. It is not a review target of this package, and this package neither duplicates nor patches it |
| `cda8ac76100b2fa4b5429bea27c3c8c80353e240` | `chatgpt/forge-quest-studio-foundation` | Correction round 1 only, and only to answer one question: which of the paths this package cites changed after the `824c4d58` snapshot. Fetched and diffed locally against `824c4d58`; the result is `00_CONTEXT.md` §00.6 | Read-only, nothing merged, nothing modified. Superseded: the implementation line was corrected past this SHA and accepted at `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` (`claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d`), so its evidence is reviewed rather than pending |
| `a991abc2e6af0dfe25ae06e032541a0b73409e8d` | `chatgpt/review-forge-next-planning` | The independent review of the first freeze. Its only commit sits on top of `201a1e2e`, so it adds a file and changes nothing it audits | Read-only. Findings applied on this branch, per `CLAUDE.md` §12; the review branch itself is untouched |

The design files and the continuation brief still carry the older branch name in their own headers.
The exact snapshot consumed is `824c4d58`, which contains the older branch's history. **A reviewer
must not look for these files on the older branch.**

**One-writer discipline was kept.** The ChatGPT branches have one writer each; this planning branch
has one writer. Neither merged nor rebased onto the other, and the package cites the ChatGPT work by
SHA only.

### 8.3 Deep-dive readers and matrices

- **Firsthand reading** by the planning owner of every module under `forge/src/` and of the whole
  Builder bundle at `main@305a28f`. Section A is written from that reading.
- **Twelve parallel readers** over the Builder, Forge, the game source at head and both pins,
  repository consumers, the Forge test suite and CI, the current UI, and every committed results
  bundle and manifest.
- **Two merge agents** built the Builder-to-Forge parity matrix and the Content Admin feasibility
  matrix, re-opening the cited source wherever the readers disagreed.
- **A design panel** produced independent IA, architecture, capture, queue and visual proposals, with
  independent judges on the visual family.
- **A UI-contract reading** of the ten architecture-neutral contracts row by row: 166 requirement
  rows, 25 component rows, 35 machine-state rows mapped to `forge/src`, 72 adversarial scenarios.
- **A completeness critic** compared the package against brief sections 3 to 17.
- Population read for the workflow inventory: **42 results bundles, 41 manifests, 23 generator
  scripts, 7 live manifests under `push/`, 15 workstream tasks**.

### 8.4 Verification scope, and what was not verified

**Parity matrix.** A row was adversarially verified when a wrong cell would change a conclusion the
package rests on: every GAP, every intentional difference, every retirement blocker, and every row
the merge marked low or medium confidence. **29 rows verified and corrected; 32 rows are marked `not
verified` and are the merge agent's finding, not an audited one.** Those 32 are all high-confidence
PARITY or FORGE BETTER rows that block nothing.

**Content Admin matrix.** Adversarial verification **covered 33 of the 35 rows and corrected every one
it touched**, almost always in detail rather than verdict. **CA-23 is the single row whose
zero-game-change answer changed.** The two rows not reached, **CC-08 and CC-10**, are labelled not
verified in the evidence file; CC-08's substance is independently established in the risk register
and was verified against the pin.

**Panel synthesis was unavailable at this SHA.** There is no judged architecture synthesis, no judged
IA synthesis and no test-strategy proposal file. Sections D, F and I say so in their own words and
label the recommendation as the planning owner's, derived by comparing the independent proposals
against the evidence. Section F.12 does use the queue-model option file, which exists.

**Nothing in section E is browser-proven.** Every claim about how a procedure behaves in the admin's
session is inferred from source.

**Studio seam measurements** behind the Studio risks were taken in read-only overlays of `main` plus
the exported branch files, not on that branch's committed bundle. The brief's "a fresh build equals
the checked-in bundle" property is therefore **unverified here** and is review focus for the seam's
own owner.

**The three internal inconsistencies the first handoff reported, and what is true now.** Independent
review checked all three against the final files and found that the first handoff had described
defects the sections had already fixed, while misnaming the one that was real. Corrected here:

1. **Real, and now fixed.** The stale numbers were in `evidence/parity-matrix.json`'s **prose
   `summary`** (GAP 22, PARITY 10, INTENTIONAL DIFFERENCE 5, blocker yes 7 / no 45), not in its
   machine `status_tally`, which already read GAP 23, PARITY 8, INTENTIONAL DIFFERENCE 6 and blocker
   yes 8 / conditional 9 / no 43 / split 1 in agreement with section B. The first handoff pointed at
   the wrong field. Both files' summary strings are now **generated** from the rows by
   `evidence/gen_evidence_summary.py`, so the two cannot diverge again, and the same script corrected
   a second overstatement in both files: `verification.method` claimed a verifier per capability row,
   where the real scope is the decisive set B.1 defines.
2. **Not a defect.** Section B.2's blocker table carries the explicit `split (part no, part gated) 1`
   row, so it sums to all 61. P-34 is that row.
3. **Not a defect.** `D_IA_AND_JOURNEYS.md` §D.3.1 says "Seventeen pages are committed", which agrees
   with `00_CONTEXT.md` §00.5 and the wireframes README.

---

## 9. Live-game statement, constraints, gates, and what was not checked

### 9.1 The explicit statement

- **No implementation was performed.** No production code, no test, no fixture, no manifest and no
  generated artifact was written or changed. Every file added by this branch is documentation,
  evidence or a static wireframe.
- **Live requests to `theninja-rpg.com`: none.**
- **Live game writes: none.**
- **Session cookies or credentials obtained, requested, synthesised, exported or exposed: none.**
- **TheNinjaRPG source changes: none.** The game source was read from read-only local clones at three
  commits and **never executed**.
- Network access in this pass touched the **public game repository** and `github.com` only, for
  fetches and clones. It never touched the game.

### 9.2 The brief's section 16 constraints, one by one

| Constraint | Held? | Evidence |
|---|---|---|
| No Forge production implementation | **yes** | `git diff 305a28f..HEAD -- forge/` is empty |
| No Builder deletion or deprecation | **yes** | `builder_bundle.js` and `builder_loader_user.js` untouched; J.2 keeps the Builder installed and pinned through stage 4 |
| No live game requests | **yes** | see 9.1 |
| No live game writes | **yes** | see 9.1 |
| No use, request or export of session cookies or credentials | **yes** | see 9.1 |
| No TheNinjaRPG code changes | **yes** | all three checkouts are read-only clones in the session scratchpad |
| No release-pin movement | **yes** | `git diff 305a28f..HEAD -- .github/` is empty; both loaders still pin `ce603def` |
| No manifest contract migration | **yes** | `push/`, `archive/`, the runner and the validator are untouched; J.4 plans compatibility, it does not change it |
| No changing repository doctrine or laws to fit a proposed UI | **yes** | `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md` and `docs/RULINGS.md` are untouched. Where a law constrains the product (engine law 16c forbids a gameAsset unhide step) the package **records the law and drops the capability**, in CA-04 |
| No publishing or live content changes | **yes** | no publish action exists in Forge today and none was built |
| A capability that genuinely needs a game change is recorded as a dependency, not implemented | **yes** | section E.11 is that list, each row with the zero-change fallback used instead |

Two further self-imposed boundaries were kept. **No active `chatgpt/*` branch was modified**
(`CLAUDE.md` section 4), and **no user-owned decision was settled**: `K_USER_DECISIONS.md` holds 58
open entries and every dependent recommendation names the id it waits on.

The one byte-producing side activity, a minified bundle built to measure the size question, was
written to the session scratchpad only and **is not committed**.

### 9.3 Gates run, with exact commands and results

Read-only, and **re-run for this freeze** rather than carried forward from the first one. None was
piped in a way that masks its exit code. **This package changes no file any of these gates owns**, so
they are a statement about the baseline, not about the package. One number moved between freezes and
is corrected here: `doctrinemap.py` reports 17 surfaces scanned, not 16, because it scans every
top-level `docs/*.md` and this branch adds `docs/PLAN_2026-09-12_forge_next.md` to that directory.
The first handoff quoted a pre-package measurement.

| Command | Result | Exit |
|---|---|---|
| `skills/building-tnr-content/scripts/doctrinemap.py` | 21 assertions, 18 referenced, 17 surfaces scanned; 0 errors, 0 warnings | **0** |
| `skills/building-tnr-content/scripts/render_doctrine.py --check` | all projections current | **0** |
| `skills/building-tnr-content/scripts/build_packs.py --check` | all packs and table-of-contents files current | **0** |
| `skills/building-tnr-content/scripts/lawmap.py` | 93 laws, 93 matrix rows, 77 citations across 35 files; 0 errors, **5 warnings** | **0** |
| `cd forge && npm test` | **293 tests, 292 pass, 1 fail**, Node v22.22.2, 12.2 s | **1** |
| `git diff --quiet 305a28f992e33194fbba279a3f32e698dfb2b67f..HEAD -- forge/ skills/ state/ docs/design/ .github/` | no output: none of those paths changed | **0** |

**The five lawmap warnings are pre-existing on `main`** and are unrelated to this package: laws 16d,
37 and 69 are classed `validate` with no citation in the validating scripts, and laws 18 and 61 are
classed `knowledge` but cited by `validate.py`.

**The one failing test is the known red baseline, not a regression.** `forge/test/release_loader.test.mjs`
requires exactly one release-pending marker, and the release-pin workflow removes that marker on
`main`, so the suite is red on `main` after every release. Forge CI last ran at the merge commit and
did not run on the automatic pin commit, so CI never observes this state. It is carried as risk R-11,
closed by gate G-09, and the fix currently lives on the ChatGPT branch together with unrelated
assertion changes, which is why **K-60** exists.

Studio-seam measurements taken in read-only overlays and reported as such, not re-run for this freeze:
the compiler selftest 9 of 9, the mission integration test pass, the overlaid Forge suite 305 of 305
(the branch relaxes the red assertion), and an unminified bundle delta of +39,621 bytes, +10.0 per
cent. **The branch's committed bundle was not exported, so its equality to a fresh build is
unverified here.**

### 9.4 What was NOT checked, and who must check it

**No browser was opened. No device was used. No live session was exercised.** Every claim below is
Inferred or Assumed and must not be treated as verified by anyone reading this package.

| Not checked | Who must check it |
|---|---|
| Firefox Android and ViolentMonkey timing, the entry hop against the real 404, overlay mount and release on a real build | **the operator (dauntless)**, smoke SM-1, after a phase-0 release |
| That any Forge write works live at all: no Forge write has ever run against the game, and all seven committed Forge bundles are capture-only | **the operator**, smoke SM-2. This is gate G-08 and it is the single mutating smoke in the plan |
| Responsive behaviour, touch targets at real widths, safe-area insets, and whether a sticky bar covers a warning | **the operator**, smoke SM-3, after phase 2 |
| Whether operating-system reduced-motion and contrast preferences reach a userscript overlay | **the operator**, smoke SM-4 |
| Glyph coverage for the chosen Unicode blocks on the device | **the operator**, smoke SM-5 |
| That the Builder panel does not reappear over the Forge surface with both loaders installed | **the operator**, smoke SM-6 |
| Recovery after a real tab eviction | **the operator**, smoke SM-7 |
| Whether `navigator.storage.persist()` is granted, and what the prompt does | **the operator**, smoke SM-8 |
| The Studio compile seam end to end from a real device | **the operator**, smoke SM-9, only after that seam merges |
| That the carrier overlay can reach the admin procedures with the admin's own cookie; what a role miss looks like over the wire; what the upload completion result actually is; whether a paged draft listing stays inside the shared rate window | **the operator**, and only after the reviewer accepts the phase that would build them |
| Real rate-limit clock skew, Clerk session refresh during a long job, carrier-page traffic outside the budget's view | **the operator** |
| Whether the ChatGPT seam's committed bundle equals a fresh build | **the seam's own owner**, in its own independent review |

**No smoke is scheduled as Fable work and none appears as a phase deliverable.** Repository access is
not live-game authorisation (`CLAUDE.md` section 6); a smoke is an operator action that a phase
enables.

---

## 10. What is frozen, and what the reviewer is asked to audit

### 10.1 Frozen

Everything under `docs/forge_next/` and this file, at the head SHA reported with the push. The head
does not move until review returns. If a blocking correction proves unavoidable before review starts,
a **new handoff with a new exact SHA** is issued rather than an edit in place. That is what happened
here: the first freeze `201a1e2e` stayed still through its review, and this freeze is a new SHA
carrying the accepted corrections rather than a rewrite of it (`CLAUDE.md` §12).

### 10.2 What ChatGPT is asked to audit

The brief's own five criteria, with what each means against this package:

| Criterion | What to attack |
|---|---|
| **Completeness** | Does the package answer brief sections 13-A to 13-K and the eighteen section-12 questions? Is anything cited that does not exist (field 3.4 lists what is known to be missing, starting with the absent entry-point plan)? Are the 59 registered decisions the right set, is anything settled in prose that should have been a decision, and — the F1 question in reverse — is any entry now classed **engineering** that carries a consequence the director actually owns? |
| **Safety** | Does any proposed surface, component or phase create a path to re-send an ambiguous write, hide a pause, make a failure look like success, or render a state with no machine source behind it? The standing gates in G.0 and G.1.2 claim to prevent exactly that; test the claim. Is the single execution-core change (the advisory event hook) genuinely advisory? |
| **Source agreement** | Spot-check the rows the package rests on. Every citation is a file and line at `main@305a28f`, in the Builder bundle, or in a named game checkout. Attack the 32 parity rows marked `not verified` and the two admin rows marked not verified, and re-run `evidence/gen_evidence_summary.py` to confirm the generated summaries still match the rows |
| **UX coherence** | Do the IA, the visual system and the wireframes describe one product with one vocabulary? Does any element promise a capability the evidence does not have? The reconciliation of the approved mockup lists 17 visual and 8 structural departures with the smallest correction for each; judge whether each departure is justified by evidence or by taste |
| **Whether the phases are reviewable** | Can phase 0 be briefed and reviewed on its own SHA, with an empty execution-core diff and a byte-identical screen fixture as its acceptance? Is each later phase a vertical slice that leaves Forge usable? Are the dependencies real or convenient? |

The reviewer should attack hardest at: **the panel-synthesis gap** (sections D, F and I recommend
without a judged synthesis and say so), **the parity rows that were not verified**, **the
role-denial audit in E.3**, whose conclusion removes a proposed UI state, and **the retirement
gates**, because the whole "Builder can be retired" claim is only as good as they are.

**For this round specifically**, the narrower question is whether the four findings are actually
closed. The checks that answer it: (1) read `K_USER_DECISIONS.md` §K.1 and each of the fifteen
engineering entries, and challenge any reclassification that buries a director-owned consequence —
section 1.1 of this handoff lists where every correction landed; (2) confirm `G_ROADMAP.md` §G.2.0
now states objective prerequisites and that no phase table, dependency node or §G.6 line still calls
K-13, K-14 or K-60 a director blocker; (3) re-derive `00_CONTEXT.md` §00.6's file-level Studio
reconciliation with `git diff --name-only 824c4d58 cda8ac76`, and check that no claim from that
branch's own handoff has been adopted as verified; (4) run `python3
docs/forge_next/evidence/gen_evidence_summary.py` and confirm it rewrites nothing.

### 10.3 The continuation brief's section 7 cross-checks, confirmed before the freeze

The cross-check rows were recorded before sections D, F and G were finished, so their original
"not on disk" statuses are stale. The table below is the status **at the frozen SHA**.

| Id | Requirement | Status at this SHA | Where it is satisfied |
|---|---|---|---|
| CC-S1 | `SENT` ambiguity representable without semantic loss | **satisfied** | D2.3 StatePill and SegmentedProgress, `SENT` as a hatched construction with its own glyph and no retry affordance; D.3 BU-3; wireframe `wf06_halt_sent`; the standing gate R-01 in G.1.2; the code invariant in A.4 |
| CC-S2 | `CONFIRMED` positive but not terminal; no re-send in the verify phase | **satisfied** | D2.3 StatePill state table; D.4.2 journey; A.4 phase semantics (the phase written on `CONFIRMED` is the next step, so a resume can only read) |
| CC-S3 | `INCOMPLETE` means a read-back is owed; never green; primary action is re-read | **satisfied** | D.3 BU-3 and JR-2; `wf08_results_sync`; D2.3 outcome lamp split from the state pill; A.4.1 item 6 records today's one visible breach |
| CC-S4 | Orphan candidate, adopt, skip and re-send as a decision surface | **satisfied** | D2.3.2 RecoveryDecision construction (no preselect, name before id, re-send visually separated); `wf07_orphan_decision`; A.7 records the current defect that this corrects |
| CC-S5 | Auth checking, refused and unauthorized distinguished **where source permits** | **NOT satisfied as a session state, and deliberately so** | E.3 is the audit the requirement asks for. It finds denial is per action, prose-coupled and unusable on seven paths, so **no fifth session lamp is proposed**. D2.2 makes the lamp conditional on this audit; risk R-26; the ruling stays **K-34** |
| CC-S6 | Full-capture read success versus body persistence | **satisfied** | D2.3 CaptureRow renders two separate verdicts; `wf09_capture_preflight` and `wf10_captures_library`; the honesty defect is parity row P-58 and gate G-07 |
| CC-S7 | Rate-limit pause visible before the next action, with no retry encouragement | **satisfied** | D2.3 BudgetMeter and the TRIPPED rule in D2.3.4; D.3 BU-3 halt card; risk R-03 carried into phases 1 and 4 |
| CC-S8 | Game result and repository sync result as separate claims | **satisfied as a plan, not as a capability** | D2.3.1 ResultSummary carries a separate sync lamp and JR-2 makes export a state of the screen; F.8 adds a journaled `job.sync` as the one additive journal migration; G phase 3 carries it under R-07. **There is no machine source for it today** (A.4.1 item 4), which is why it is a phase-3 deliverable |
| CC-S9 | Publication state distinct from technical success | **satisfied as a proposal, gated** | D.3 AD-5 is HOLD; E.4 shows three different publication axes so one generic Publish would be a lie on the third; gated on K-07, K-12 and K-55 |
| CC-M1 | No horizontal primary-nav dependency; at most five destinations; a More surface | **satisfied** | D.1.3 five bottom items plus More; D2.3 BottomNav and MoreSurface; the phone column of every wireframe. Exact destinations stay K-20 |
| CC-M2 | Persistent and recoverable operation consequence during long flows | **satisfied** | D2.3 ModeBand, sticky under the top bar on phone; D.6; the top-bar underline that persists during a run |
| CC-M3 | 44 px ordinary targets, appropriate primary sizing | **satisfied, with today's exceptions recorded rather than hidden** | D2.3 AppShell raises Close from 32 px and NavRail rows to 44 px; A.10 records that today's nav is 40 px and Close 32 px and that the docs said otherwise (the code wins under the precedence table) |
| CC-M4 | Sticky UI never covers warnings | **satisfied** | D2.3.3 is the phone chrome stack rule that did not exist when the cross-check was written |
| CC-M5 | High-risk recovery alternatives separated, with descriptive labels | **satisfied** | D2.3.2 separated action regions and one primary with a distant Cancel; `wf07_orphan_decision` |
| CC-M6 | Technical detail progressively disclosed, never miniaturised | **satisfied** | D2.3.1 EvidencePanel row (full-screen sheet on phone, inspector on desktop); D.9. The exact type floor stays K-23 |
| CC-C1 | Reusable equivalents of the component responsibilities without coupling the execution core to a screen hierarchy | **satisfied** | A.12 maps all 25 component responsibilities to a Forge data source today and names what must move below the seam; D2.3 plus D2.3.1 cover all 25 under this package's names with an explicit mapping column; F.4 defines the headless boundary and the import-direction gate that makes it machine-checked |
| CC-C2 | The technical roadmap supports the UI state model without forcing the UI to lie | **satisfied** | F.10 is the seam state table; every phase carries a gate that no class, pill, lamp or label is rendered without a machine source. **Three states have no source today and are named rather than invented**: repository sync, authorisation denial, and a structured waiting-for-response event |

Two rows therefore remain open on purpose: **CC-S5**, which the evidence closed in the negative, and
**CC-S8**, which is a phase-3 deliverable rather than a present capability. Every other row is
satisfied at this SHA.

### 10.4 Director questions the package surfaces

These are the conflicts the pass could not resolve by repository authority, and which are the
director's to settle. The nine below are routed to the director explicitly; each is registered in
`K_USER_DECISIONS.md` at the id shown.

| Id | The question | Register entry |
|---|---|---|
| CF-04 | A fifth authorisation state was proposed with no source signal behind it. Authorise the pinned-source audit conclusion in E.3 and decide whether a per-action denial label is rendered at all | **K-34** |
| CF-06 | The approved direction, the colour-semantics amendment, design system v0.1 and the style board give four different mode palettes and disagree on whether Review is a mode. Rule the taxonomy and palette now, or confirm the wait for the transcript export. This blocks the phase-2 freeze and the Studio shell absorption | **K-21**, **K-22**, **K-33** |
| CF-16 | The Studio seam implements a workflow-dispatch trigger model that its own design document did not recommend first, widening the phone credential to include Actions write. Ratify the model with its scope, or require reversion before a second adapter | **K-26**, with **K-15** |
| CF-17 | The manual-art-submission boundary is cited as a standing ruling, but no ruling id exists; the operative text is the art workflow and doctrine. Record it as a ruling entry? | **K-41** |
| CF-18 | The canonical compiler does not enforce the mission profile shape that doctrine says the profile owns, while the Studio browser does. Should the compiler enforce it canonically, or is the shape advisory? | **K-36** |
| CF-19 | The change that makes `main` green rides on the ChatGPT feature branch together with unrelated assertion drops. Which branch owns the baseline fix, and may the marker-only change be separated? | **K-60** |
| CF-20 | The seam introduces a branch namespace and a bot committer that the development workflow does not declare and the index does not route. Authorise declaring and routing them as part of that seam's integration? | **K-37** |
| CF-21 | The expansion study proposes its own channel priorities and phase order, which section G reconciled rather than inherited. Confirm the flagship workflow so the first vertical slice is settled | **K-42** |
| CF-22 | The Studio ships a second shell with its own palette and its own confirmation, mounted outside the composition root. After the seam integrates, who owns those files for the design-system absorption? | tracked against **K-26** and the phase-S owner list |

**Two questions have no register entry yet** and are surfaced here for the director to decide whether
they need one, exactly as section F.18 states:

1. **The two-release storage rule.** May a release write a storage version that the previously pinned
   release cannot read? The recommendation is no, because rollback is re-pinning the loader and the
   journal refuses a newer record. It is a policy worth confirming rather than a detail.
2. **Whether a real-browser test layer may ever exist.** Without one, responsive behaviour, touch
   targets at real widths and visual regression stay unverifiable by any agent, and every
   device-facing claim in this package stays Inferred. Tests are socket-free by repository rule, so
   admitting such a layer is a ruling, not a Fable decision.

Two more were surfaced by the workflow inventory and routed to the register's owner rather than
registered: whether `push/` supersession and archiving becomes a Forge action or stays a repository
ritual, and whether the census-to-generator loop becomes a Forge workflow with persisted list bodies
or remains a repository-session pattern.

### 10.5 Which parts of this package are judgement, not measurement

Stated plainly so that no later phase treats an opinion as a fact.

**Measured, and checkable from the tree.** Every file and line citation into `forge/src`,
`forge/test`, `builder_bundle.js`, `scripts/`, `skills/` and `.github/` at `main@305a28f`. Every
citation into the three game checkouts. The bundle byte counts and their attribution by section. The
test counts and timings. The counts drawn from the committed record: 42 bundles, 41 manifests, 23
generator scripts, 148 write items, 178 reference uses, 28 persisted bodies. The gate results in field
9.3. The contrast ratios, which are reproducible from `evidence/contrast.py`. The parity and admin
matrix rows that carry a verification verdict.

**The planning owner's judgement.** These are arguments from evidence, not measurements, and a
reviewer is entitled to reach a different conclusion:

- **The architecture recommendation itself** (core first, then shell). There was no judged panel
  synthesis; F.0 says so. The three options were weighed by the planning owner against axes the
  planning owner chose.
- **The information architecture recommendation** (operation-first with content lanes second). Two
  independent proposals existed and no judge ranked them; D.0 says so. Both weakness lists are
  reproduced rather than summarised away.
- **The test strategy** in section I. No panel proposal existed for it at all.
- **The capture classification model** in F.11, derived by the planning owner from the named evidence.
- **The roadmap's phase boundaries and ordering.** The dependencies are argued from capability
  existence, parity gates and admin feasibility, but the choice of nine phases, their names and their
  cut points are the planning owner's.
- **Every likelihood and impact estimate in the risk register.** They are marked as estimates in the
  register's own legend, and the later rows carry an explicit estimate marker.
- **Every `proposed_disposition` in the parity matrix** and every phase placement of a gate. The gates
  themselves are derived from evidence; when to close them is not.
- **The visual token values, component constructions and the 17 mockup departures.** Each names a
  smallest correction and an evidence line, but the set is a proposal for the phase-2 design freeze,
  and the director accepts or adjusts it.
- **The transition ladder's stage order**, drawn for one still-open option of K-11 and saying so.
- **Every recommendation inside a K entry.** They are advisory by construction.
- **Anything about a phone, a browser, the operating system, or the live game.** Marked Inferred or
  Assumed wherever it appears, and listed in field 9.4.

**Nothing in this package is a decision.** Where the evidence points somewhere, the package says so
and names the id that must rule.
