# 00. Context, evidence base and method

**Status:** PLANNING PACKAGE, no implementation.
**Brief:** `state/prompt_forge_next_planning.md` at `chatgpt/forge-next-planning@70c151616f09c6ec729cb05afb30faa2c6331183`.
**Mid-pass amendment (user-approved visual north star):** `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` at `chatgpt/forge-next-planning@0bb5a54b1025ba49ff6b09aa9606f23102f4dca3`, plus the approved concept mockup supplied as an attachment (a compressed copy is committed as `docs/forge_next/design/forge_next_concept_mockup.jpg` for durability). It was read as a new planning input on the existing branch; the ChatGPT branch was neither merged nor rebased onto. Its section 12 governs what is binding (product character, shell, Command Center, lanes, Content Admin presence, state visualization) and what is illustrative (labels, destinations, lane names, colours, geometry); section D reconciles every mockup element with the capability evidence and section D.7 lists the departures recommended and why.
**Planning branch:** `claude/forge-next-planning-v3frzi` (the branch assigned to this session; `docs/DEVELOPMENT_WORKFLOW.md` §3 names `fable/*` as the normal Fable prefix, so this is a stated deviation, not a new convention).
**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`, verified with `git fetch origin main` at the start of the pass.
**Lane:** A. Planning owner Fable / Claude Code; independent reviewer ChatGPT (Release Auditor with UI/UX Reviewer and Engineering Auditor lenses).

**Second mid-pass amendment (director rulings and consolidated design lane):** `chatgpt/forge-quest-studio-foundation@824c4d58075d0265c717ef25c02485614f3096cf`, consumed read-only (exported into the session scratchpad; neither merged nor rebased, nothing on that branch modified). It carries `RUL-2026-09-12-001` (one shared Quest Studio with subtype adapters; Mission is a subtype, not a parent product) and `RUL-2026-09-12-002` (Forge is the human translation, orchestration and presentation layer over the repository, which stays the durable source of facts, contracts, profiles, scripts, validators, provenance and generated artifacts), their canonical owners `docs/design/FORGE_NEXT_QUEST_STUDIO.md` and `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, the routing index `docs/design/FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md` (authority tiers A to E), the Tier C architecture-neutral UX and safety contracts, the Tier B product proposals (`FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`, `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`, `FORGE_NEXT_MISSION_STUDIO.md` as Mission-subtype detail, `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`), the continuation brief `state/prompt_forge_next_planning_resume_after_ui_recovery.md`, and a ChatGPT-owned Quest Studio foundation implementation under `state/prompt_forge_quest_studio_foundation.md` (Quest Source → request branch → GitHub Actions worker → `quest_compile.py` → build-result → Forge seam, Mission as the first adapter). That implementation is treated here as architecture and roadmap evidence only; it is not a frozen review target and this package does not duplicate or patch it. Its `main` remains `305a28f` (re-verified with `git fetch origin main` when the amendment arrived). Decisions the director still keeps open after these rulings are listed in `K_USER_DECISIONS.md` §K.0.

**Header note (provenance).** The ChatGPT design files and the resume brief still carry the branch name `chatgpt/forge-next-planning` in their headers; the exact snapshot consumed here is `824c4d58` on `chatgpt/forge-quest-studio-foundation`, which contains the older branch's `e0081afa` history. Reviewers should not look for these files on the older branch. The SHA, not the branch name, is the audit target (`CLAUDE.md` §11).

**Transcript status.** At `824c4d58` the predecessor-transcript reconciliation is still pending (`docs/design/FORGE_NEXT_UI_CONTEXT_HANDOFF.md` header: TRANSCRIPT RECONCILIATION PENDING; no filled recovered-state section). Every style-board delta therefore stays a labelled director question (K-20 to K-24, K-30, K-32, K-33 and the wording half of K-12); this package does not read the style board as a later ruling.

**Code cites.** Every `forge/src` line cite in this package is taken at `main@305a28f`. The planning branch changes no file under `forge/`, `skills/`, `state/`, `docs/design/` or `.github/` (verified with `git diff --quiet 305a28f..HEAD` on those paths at each amendment and again before the freeze). Files that exist only on the ChatGPT branch are cited with the prefix `824c4d58:`.

## 00.1 Boot sequence performed

Read from the live checkout, not from memory, in this order: `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `CLAUDE.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/agents/UI_UX_REVIEWER.md`, `docs/agents/ENGINEERING_AUDITOR.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md`, `docs/workflows/FABLE_REVIEW.md`, `docs/workflows/DIRECTOR_DECISIONS.md`, `docs/workflows/CONTENT_WORKSTREAM.md`, `docs/DOCTRINE.md`, `docs/10_LAWS_core.md` (head), `docs/PLAN_2026-09-03_builder_app.md`, `docs/BUILDER_APP_NOTES.md`, `docs/handoffs/BUILDER_APP_READINESS_HANDOFF.md`, `docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md`, `docs/reviews/REPO_SIMPLIFICATION_AUDIT.md`, `docs/DRIFT.md`, `docs/HANDOFF_INVENTORY.md`, `state/prompt_forge_full_capture.md`, `state/prompt_forge_protected_auth.md`, `state/prompt_builder_app_build.md`, `state/one_perfect_crop_content_admin_open.md`, `state/workstreams/INDEX.md` and `one_perfect_crop/roadmap.json`, `skills/building-tnr-content/SKILL.md` and `references/pipeline.md`, `push/README.md` and every manifest under `push/`, `reports/code_audit_2026-09-02.json`, all seven `.github/workflows/*.yml`, `.github/scripts/pin_release.py`, both loaders, every module under `forge/src/`, `forge/build.mjs`, `forge/package.json`, the test file inventory under `forge/test/`, and `builder_bundle.js`.

Current operational state (for orientation only, this pass changes none of it): mission flatten `push/46` shipped and awaiting the user's tap; law-provenance reconciliation not begun; One Perfect Crop workstream active with the content-admin director packet `admin.balance_and_eligibility` READY and `art.intake_accepted_assets` BLOCKED.

## 00.2 Source pins inspected

All game-source reading was done on read-only clones of the public repository `studie-tech/TheNinjaRPG` in the session scratchpad. Nothing was executed from any checkout; no request was made to any game host.

| Role | Commit | Notes |
|---|---|---|
| Current upstream head | `36c5873b7b6ee5fd3af717008d7c51b0f185b756` (2026-09-12 16:03 +0200) | 81 commits after the Forge pin, 170 after the task pin |
| Forge global pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` | every Forge engine fact, `fields.json`, `nested.json`, the procedure registry |
| Protected-auth task pin | `bdec2883748f029a0ecb93505adfdcbae6851fe9` | `state/prompt_forge_protected_auth.md`; auth table proven identical to the global pin (`docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md`) |
| Generated `45c/45d/45e/45f/45g` provenance | `bdec2883` | reconciled by `docs/reviews/REPO_SIMPLIFICATION_AUDIT.md`; older than the Forge pin |
| Sentinel drift signal | `98d0eca5c2e922f3b41e56120f096c072645c1f0` | `docs/DRIFT.md` 2026-09-11: 45d item farm fields and quest `requiredFarmingLevel` now required; guide constants added |
| Last Forge relevance check | game `main@62af1b3405b10183b31f838c9a5f131d790460f1` | 2026-09-09, `docs/BUILDER_APP_NOTES.md` |

Repository release state: `forge_loader_user.js` 0.4.0 and `builder_loader_user.js` 4.32 both `@require` `ce603def204f585d23837121b86cfdd9fd4c308c` via jsDelivr (auto commit `d1dbecc`).

## 00.3 Method

1. **Firsthand reading** of every Forge module and the Builder bundle by the planning owner (section A is written from that reading).
2. **Orchestrated deep dive** (`forge-next-deep-dive` workflow): twelve parallel readers over Builder, Forge, the game source at head and both pins, repository consumers (`harvest.py`, `build_answers.py`, `content_workstream.py`, `validate.py`, workflows), the Forge test suite and CI, the current UI, and every committed results bundle and manifest. Two merge agents built the Builder→Forge parity matrix and the Content Admin feasibility matrix. Adversarial verification covers the rows where a wrong cell would change a conclusion the package rests on: every `GAP`, every `INTENTIONAL DIFFERENCE`, every retirement blocker, every row the merge marked low or medium confidence, and every Content Admin row. One verifier per row re-opens every cited location with instructions to default to a correction unless the source says exactly what the row claims. Each verifier returned `CONFIRMED`, `CORRECTED`, `REFUTED` or `UNVERIFIABLE`, and a corrected row replaced the original. Rows outside that set are labelled `not verified` in the matrix and in `B_PARITY_MATRIX.md`, never presented as audited. How far that pass had got at the frozen SHA is stated in `B_PARITY_MATRIX.md` §B.1 and `E_CONTENT_ADMIN_FEASIBILITY.md` §E.1, and those two statements, not this paragraph, are what a reviewer should rely on. The matrices are committed as `evidence/parity-matrix.json` and `evidence/admin-feasibility.json`; `B_PARITY_MATRIX.md` §B.1 and `E_CONTENT_ADMIN_FEASIBILITY.md` §E.1 state the verification status that holds at the frozen SHA, which is the status a reviewer should read before relying on a row.
3. **Design panel** (`forge-next-design-panel` workflow): independent proposals for the information architecture, visual direction and architecture alternatives, scored by independent judges against the brief's criteria and the verified evidence; the recommendation in sections D and F is synthesized from the winner with grafted ideas from runners-up, and the alternatives are kept so the user can choose.
4. **Completeness critic**: a final pass compared the package against brief sections 3 to 17 and the findings were folded in.
5. Baseline gates run in this session, read-only, all from the repository's own scripts: `cd forge && npm test` (293 tests, 292 pass, 1 fail: `release loader: exactly one @x-release-pending marker`, see `A_ARCHITECTURE_MAP.md` §A.10), `skills/building-tnr-content/scripts/doctrinemap.py` (exit 0; 21 assertions, 18 referenced, 16 surfaces, 0 errors, 0 warnings), `render_doctrine.py --check` (exit 0, all projections current), `build_packs.py --check` (exit 0, all packs and TOCs current) and `lawmap.py` (exit 0; 93 laws, 93 matrix rows, 77 citations across 35 files, 0 errors, 5 warnings). No gate was piped in a way that masks its exit code, and this package changes no file those gates own. Studio seam measurements were taken in read-only overlays of `main` plus the exported `824c4d58` files (no branch file modified, zero live requests): `quest_compile.py --selftest` 9/9; `quest_compile_integration_test.py` PASS; Forge overlay suite 305/305 (the branch relaxes the red release-loader assertion); bundle +39,621 B (+10.0%) unminified; committed-bundle equality unverified because the branch bundle was not exported.
6. **UI-contract reading** (`forge-next-consolidated-inputs` workflow): the ten Tier C contracts (`FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`, `FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md`, `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md`, `FORGE_NEXT_WIREFRAME_ANATOMY.md`, `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`, `FORGE_NEXT_INTERACTION_RISK_MATRIX.md`, `FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md`, `FORGE_NEXT_ICON_MOTION_SEMANTICS.md`, `FORGE_NEXT_UX_SCENARIO_MATRIX.md`, `FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md`) plus the Tier A colour-semantics amendment and the visual direction's state rules were read row by row (166 requirement rows, 25 component rows, 35 machine-state rows mapped to `forge/src`, 72 adversarial scenarios), alongside the Tier A/B product documents, the Tier D baseline audit against the code, and the foundation implementation. The resulting reconciliation plan (85 package updates, a corrected decision register, 9 roadmap implications, the resume brief's §7 cross-checks and 24 conflicts) was applied to this package, and the §7 cross-checks are confirmed in the handoff before the SHA is frozen.
7. **Authority handling** follows the routing index (`docs/design/FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md` §2 to §6): Tier A (Quest Studio, repository-backed architecture, colour semantics, visual direction) binding; Tier B (`FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`, `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`, `FORGE_NEXT_MISSION_STUDIO.md` as subtype detail, `FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`) proposals reconciled by sections F and G and never inherited as an approved order; Tier C architecture-neutral requirements; Tier D before-state; Tier E scaffolding discarded once recovery lands.

Evidence tiers follow `docs/00_INDEX.md`: Source-verified, Behaviour-proven, Observed, Inferred, Assumed. Every matrix row carries its tier and citations; where a claim could only be settled in a real browser or live session it is marked Inferred or Unverified and listed in the handoff.

## 00.4 Constraints honoured (brief §16)

No Forge production implementation, no Builder deletion or deprecation, no live game requests, no live game writes, no use or request or export of session cookies or credentials, no TheNinjaRPG code changes, no release-pin movement, no manifest contract migration, no doctrine or law change, no publishing or live content change. The throwaway minified bundle measured for §A.9 was written to the session scratchpad only and is not committed.

## 00.5 Package layout

```
docs/PLAN_2026-09-12_forge_next.md      entry point: executive summary, roadmap headline, handoff pointer
docs/forge_next/00_CONTEXT.md           this file
docs/forge_next/A_ARCHITECTURE_MAP.md   current-state architecture (Forge and Builder)
docs/forge_next/B_PARITY_MATRIX.md      Builder → Forge parity and retirement gates
docs/forge_next/C_WORKFLOW_INVENTORY.md real content workflows Forge must support
docs/forge_next/D_IA_AND_JOURNEYS.md    information architecture, journeys, mockup reconciliation
docs/forge_next/D_VISUAL_SYSTEM.md      the approved visual direction elaborated into tokens, components and state rules
docs/forge_next/E_CONTENT_ADMIN_FEASIBILITY.md  per-class source audit, zero-game-change scope
docs/forge_next/F_ARCHITECTURE_RECOMMENDATION.md  preserve / replace / abstract / migrate
docs/forge_next/G_ROADMAP.md            phased Lane A roadmap with gates
docs/forge_next/H_RISK_REGISTER.md
docs/forge_next/I_TEST_STRATEGY.md
docs/forge_next/J_MIGRATION_AND_RETIREMENT.md
docs/forge_next/K_USER_DECISIONS.md     the decision register, split by ownership class
docs/forge_next/evidence/*.json         the two matrices with their verification state, registry gap, drift, harvest evidence, repository consumers, test and CI inventory, current-UX audit and the visual synthesis
docs/forge_next/evidence/*.py           the contrast checker behind every ratio in D, and the generator that rebuilds both matrices' summary strings from their rows
docs/forge_next/wireframes/*.html       seventeen static wireframes (phone and desktop in one page), with src/ (generator) and review/ (rendered captures)
docs/forge_next/design/                 the approved concept mockup and its provenance pointer
docs/handoffs/FORGE_NEXT_PLANNING_HANDOFF.md  section-17 handoff for independent review
```

Files marked (forthcoming) in any section are not committed at the cited SHA. A matrix or evidence file cited by A, H or K but absent from `evidence/` is not evidence until it lands; the handoff lists only committed artifacts and names anything still forthcoming.

## 00.6 Post-review reconciliation (2026-09-13)

The package was frozen at `claude/forge-next-planning-v3frzi@201a1e2ea57011440e164f84a0ed30298fa4b243` and independently reviewed. The review is `docs/reviews/FORGE_NEXT_PLANNING_REVIEW.md` at `chatgpt/review-forge-next-planning@a991abc2e6af0dfe25ae06e032541a0b73409e8d`, a branch whose only commit adds that file on top of the frozen SHA, so the audit target is untouched by it. Its disposition is `APPROVE_WITH_REQUIRED_CORRECTIONS`: the architecture is approved, and four findings had to be corrected before integration. This section records what changed; nothing here was read from or written to any ChatGPT-owned branch except as read-only evidence.

| Finding | What it said | What was done |
|---|---|---|
| F1 (high) | The register escalated ordinary engineering mechanisms as director rulings, against `docs/workflows/DIRECTOR_DECISIONS.md` §1 | Accepted. `K_USER_DECISIONS.md` now carries an ownership class per entry and three index tables (§K.1). Fifteen entries moved to **engineering**, five are **split** with only the director half waiting, and each engineering entry states Fable's position instead of a question. No id changed |
| F2 (high) | Phase 0 was blocked by K-13, K-14 and K-60, two of which say "Can defer: yes", and K-60 misread the one-writer rule | Accepted. Phase 0 now has four objective prerequisites and no director decision. The one-writer reading is corrected in K-60, in `G_ROADMAP.md` §G.2.0 and §G.4, in `J_MIGRATION_AND_RETIREMENT.md` and in `I_TEST_STRATEGY.md`: the rule reserves a branch to one writer, not a file to one branch. K-61 is answered by the default role model rather than held open |
| F3 (medium) | The package studied `824c4d58`; the implementation froze later at `cda8ac76`, and was finally accepted at `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` | Accepted with the scope stated below. Provenance is restamped and measured. The branch's evidence is no longer unreviewed: the independent review at `claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d` verified it and returned APPROVE_WITH_NONBLOCKING_FOLLOWUP. Cite re-resolution now happens against the accepted SHA |
| F4 (medium) | Audit-summary metadata was stale relative to the package's own final rows | Accepted. The evidence summary strings are regenerated from the rows by `evidence/gen_evidence_summary.py`, which any checkout can run, and the handoff now describes the actual frozen state |

**A second pass.** An adversarial critique of this round found that the F1 and F2 edits had reached only the files in their own diff. `F_ARCHITECTURE_RECOMMENDATION.md` §F.3, §F.16 and §F.18, `H_RISK_REGISTER.md` R-22, and four wireframes still carried the corrected-away reading; the wireframes were corrected at their generator source and regenerated rather than hand-edited (`CLAUDE.md` §7). `docs/handoffs/FORGE_NEXT_PLANNING_HANDOFF.md` §1.1 records the full list.

### Quest Studio provenance, measured rather than assumed

This package's Studio readings were taken at `chatgpt/forge-quest-studio-foundation@824c4d58075d0265c717ef25c02485614f3096cf`, the branch tip when the second amendment arrived. The implementation line later froze for review at `cda8ac76100b2fa4b5429bea27c3c8c80353e240`, whose handoff names `bcb3a47e7c516b20f5a51c5aa195364d32eb6b73` as its fully verified parent.

What that means for the cites in this package was measured here, read-only, by diffing the two commits in this checkout. The package cites fourteen distinct paths with the `824c4d58:` prefix. Eleven are byte-identical at `cda8ac76`, so every cite into them resolves unchanged: `.github/workflows/quest_studio.yml`, `docs/RULINGS.md`, `forge/src/github.mjs`, `forge/src/main.mjs`, `forge/src/studio/ui.mjs`, `forge/src/ui/dom.mjs`, `forge/test/release_loader.test.mjs`, `skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json`, `skills/building-tnr-content/scripts/quest_compile.py`, `skills/building-tnr-content/scripts/quest_compile_integration_test.py`, and the `forge/src/studio/` directory reference. Three changed:

| Path | Change between the two SHAs | Effect on this package |
|---|---|---|
| `forge/src/studio/repository.mjs` | A `generatedArtifactPath()` helper is added and `generatedManifest()` delegates to it; the path check now also rejects backslashes and empty, `.` or `..` segments | The confinement claim in §A.11 and the `null`-on-404 reading behind K-38 both still hold; they are stricter than the package describes, not weaker. Line cites `:10-20`, `:31-39` and `:41-49` still resolve; `:52`, `:57-66`, `:73-90`, `:73-121`, `:95` and `:115-117` shift by the fourteen inserted lines |
| `.github/workflows/quest_studio_ci.yml` | Two trigger paths added, a static "no live-game network path" guard over the worker and compiler, and a worker trust-boundary test step. Both line cites into this file, `:3-28` and `:47-74`, shift | The package's phase-0 proposal for a static no-live check now has an existing implementation on that branch to adopt and extend rather than to invent. The CI-duplication finding is unaffected: a second `npm ci` and `npm test` still run there and `npm audit` is still absent at `cda8ac76` (verified here) |
| `forge/test/quest.studio.ui.test.mjs` | Regression cases added | The one cite, `:22-41`, still resolves |

**What is deliberately not adopted.** The final handoff on that branch claims a larger evidence set: a 9/9 compiler selftest, a 308/308 Forge suite, a real Mission adapter integration, a multiline-draft regression, a path-traversal regression and a checked-bundle parity rebuild. Those were the implementing branch's own claims when this package was written. They have since been independently reviewed: the final target `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` was verified at `claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d`, which independently reproduced the compiler selftest (9/9), the full Forge suite (315/315 on a Node version different from CI's), the Mission adapter integration, bundle reproducibility and the worker trust-boundary contract. Those specific claims are therefore reviewed rather than pending. Claims not re-verified there stay at their original tier. The architectural criticisms the package makes of the seam — a second full-screen shell with its own palette, a mount outside the composition root, a missing promotion contract, no manifest hash in the envelope, invisible worker refusals — were checked against the final SHA above and none of them is retired by it.

**The reconciliation step, and where it belongs.** Before a phase-S brief is frozen, every `824c4d58:` cite in this package is re-resolved at the accepted Studio SHA and the three changed paths above are re-read in full. That is a prerequisite of the phase, listed in `G_ROADMAP.md` §G.0. **The accepted SHA is now known: `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`.** The re-resolution itself remains phase-S work rather than a correction made here, because it requires re-reading each cited path in full; what this reconciliation fixes is the pointer it re-resolves against.

### Baseline drift since the planning base

The package's base is `main@305a28f992e33194fbba279a3f32e698dfb2b67f` and that remains the SHA every unprefixed cite resolves at. `main` has since advanced to `6848a7805d912378f7f8eb27f52c9625dd10ac54` (verified here with `git fetch origin main`). The content of the move, measured in this checkout:

- **Forge 0.4.1** (`ef15445`): the takeover now mounts only once the carrier owns `<body>`, so hydration cannot clear the overlay. It changes `forge/src/main.mjs` (+106 lines) and `forge/src/ui/takeover.mjs` (+196), adds `forge/test/carrier.mjs`, `carrier.test.mjs` and `carrier.react.test.mjs`, and adds `react` and `react-dom` 19.2.8 as dev dependencies. Phase 0 relocates `takeover.mjs` into a userscript host, so its file list and its byte-identical-render fixtures must be re-measured against 0.4.1 rather than 0.4.0, and the committed test count in §G.2.0 and `evidence/forge-tests-ci.json` is a 0.4.0 measurement.
- The release pin moved to `25388cc7e19e9b7be8bd6a115bd3ece70775a23a`, and two content captures and two results bundles landed.
- The upstream game head has also moved past `36c5873b`, which the review reports at `1e01028cdd68459b731001dc98d78bf1970cd7f1`; that has not been re-measured here and no source claim in this package rests on it, because every source claim is pinned to `345d18ac` or to `36c5873b` by name.

None of this invalidates the frozen evidence, and none of it is silently absorbed. It is what the package's own standing gates exist for: R-05 re-runs the source-drift check per phase rather than once, and phase 0's first prerequisite is a re-measured baseline. The correct response is to re-run them when the phase-0 brief is written, not to restate 0.4.1 numbers here from a diff.

### 00.7 Quest Studio: accepted SHA and what it fixes in this package

**Accepted Quest Studio SHA:** `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`
**Independent review:** `claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d` — **APPROVE_WITH_NONBLOCKING_FOLLOWUP**
**Governing ruling:** `RUL-2026-09-16-002`

This package was written against `824c4d58` and restamped against `cda8ac76`. Neither is the
accepted target. Two rounds of independent review moved the implementation past both, and the
corrections changed things this package asserts:

| This package says | Accepted SHA |
|---|---|
| the worker is dispatch-triggered | **source-push**: Compile writes a fresh Quest Source revision to `studio/quest/*`, and that write is the build request. No browser `workflow_dispatch` path exists; `Github.dispatch()` was deleted |
| browser credential scope is an open engineering question under K-26 | **Contents: write only. No Actions write. No Workflows write.** Fixed by `RUL-2026-09-16-002` |
| the branch's evidence is unreviewed | reviewed and independently reproduced at the accepted SHA |

**Security invariant carried forward into every downstream brief.** The browser GitHub credential
must never hold **Workflows write**. Push-triggered workflow definitions are resolved from the
pushed request ref, so a credential able to write `.github/workflows/` on a request branch could
replace the worker definition and collapse the trusted-`main` compiler boundary. The worker also
byte-compares its pushed-ref definition against trusted `main` and fails closed on drift, but that
is defence in depth against accidental drift — it is **not** a substitute for the credential
invariant, because an attacker who can replace the workflow can also remove the comparison.

**K-26 note, not a ruling.** `RUL-2026-09-16-002` fixes the operator-device credential scope, which
is the substance of K-26's director half. Whether that closes K-26 as recorded in
`K_USER_DECISIONS.md` is the director's call; this reconciliation records the overlap and settles
nothing. `G_ROADMAP.md` §G.0 precondition (b) is left as written.

**Integration gate that survives acceptance.** The accepted SHA is behind operational `main`.
Before integration: reconcile the drift deliberately rather than by blind merge; ensure both
`RUL-2026-09-16-001` (One Perfect Crop) and `RUL-2026-09-16-002` survive it; then run one
repository-only end-to-end `studio/quest/*` rehearsal once the seam exists on `main`, verifying
trigger, worker-definition equality, compiler SHA provenance, request-scoped artifacts, a
superseding second source push, and stale-build refusal. **Zero live-game contact.**

**Non-blocking follow-ups inherited from the review**, to be folded into the unified
implementation contract rather than actioned here: the worker contract test pins that the
definition-equality check exists but not that it runs first; and a request branch carrying a stale
worker definition fails closed with no evidence written to the branch, which Forge currently
surfaces only as a poll timeout.

Nothing else in this package changes. The ForgeCore architecture, the just-in-time
director-decision model, and every settled director decision stand as written.
