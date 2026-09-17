# Forge Next — unified implementation contract, Phase 0

**Status:** APPROVED LANE-A IMPLEMENTATION CONTRACT — PHASE 0 ONLY
**Date:** 2026-09-16
**Repository:** `perseverance484/tnr-tools`
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Suggested implementation branch:** `fable/forge-next-phase0`
**Integration target:** fresh operational `main`, after independent review
**Live-game policy:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

This is the first implementation slice after the Forge Next planning and Quest Studio review lines converged. It is deliberately narrow. Phase 0 changes architecture and testability while keeping the operator-visible Forge byte-identical.

## 1. Authoritative inputs

Read all of these before implementation.

### Repository/current-state authority

- fresh `main` at task start — do not reuse the SHA below if it has moved;
- `state/active-context.md`;
- `state/status.json`;
- `docs/00_INDEX.md`;
- `docs/RULINGS.md`;
- `CLAUDE.md`;
- `CHATGPT.md`;
- `docs/DEVELOPMENT_WORKFLOW.md`;
- `docs/agents/README.md`;
- `docs/workflows/IMPLEMENTATION_HANDOFF.md`.

Operational `main` observed when this contract was frozen:

`b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`

Do **not** base the implementation branch on the ChatGPT contract branch. Read this contract by exact SHA, then create the implementation branch from fresh `main`.

### Reviewed Forge Next planning

Planning input:

`claude/forge-next-planning-reconciled@ba51a28a99a7748e61de0c2768bd73ab9c65c856`

Primary Phase-0 owners inside that package:

- `docs/forge_next/F_ARCHITECTURE_RECOMMENDATION.md`
- `docs/forge_next/G_ROADMAP.md`, especially `G.2.0`
- `docs/forge_next/I_TEST_STRATEGY.md`
- `docs/forge_next/H_RISK_REGISTER.md`
- `docs/forge_next/K_USER_DECISIONS.md`

The architecture remains:

> extract a headless `ForgeCore` first, preserve the reviewed execution core, and replace/expand the shell only in later phases.

### Accepted Quest Studio input

Accepted implementation:

`chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`

Final independent review:

`claude/quest-studio-final-review@82bb686370f3f8cbbe57068fe42b887c90fdf48d`

Verdict:

`APPROVE_WITH_NONBLOCKING_FOLLOWUP`

Quest Studio is a **downstream integration constraint**, not Phase-0 code to merge. Its reviewed source-push/security/provenance semantics must be preserved when Studio integration happens later.

### Final input verification

Read:

`docs/reviews/FORGE_NEXT_FINAL_INPUT_VERIFICATION.md`

It records three stale planning statements that this contract supersedes:

1. K-26's director credential-scope half is already settled: **Contents: write only; no Actions write; no Workflows write; source-push accepted** under `RUL-2026-09-16-002`. Do not ask the director to rule it again.
2. `gen_evidence_summary.py` regenerates the parity summary, but for the admin matrix it updates verification metadata rather than a prose summary string.
3. the accepted Quest Studio **does** carry `generated.manifestSha256` and verifies the fetched manifest against it. Preserve that binding later.

## 2. Phase-0 objective

Make current Forge green, measured and structurally ready for the larger product without changing what the operator sees.

At the end of Phase 0:

- domain/orchestration logic currently embedded in `forge/src/ui/app.mjs` lives behind a headless core boundary;
- a non-DOM host can exercise a complete Forge lifecycle through that core;
- the existing userscript host consumes the same core through `compose()`;
- existing screens, copy and visual output remain byte-identical under deterministic fixtures;
- the execution core remains unchanged except for one separately reviewable additive progress-event hook in `runner.mjs`;
- import direction, bundle size, contract drift and no-live-network boundaries are mechanically gated;
- Forge's Node CI has one canonical gate set rather than parallel copies;
- no Quest Studio shell, Content Admin surface, navigation redesign or other visible Forge Next feature is introduced.

This phase is successful precisely because the director should notice no product change.

## 3. Branch and writer rules

Fable is the only writer to the implementation branch.

Recommended branch:

`fable/forge-next-phase0`

Before writing:

1. fetch/verify fresh `main`;
2. record exact base SHA;
3. verify the branch is based on that SHA;
4. do not merge or rebase either frozen planning branch or the accepted Quest Studio branch into the implementation branch;
5. keep the final handoff SHA frozen until ChatGPT review returns.

The planning and Quest Studio SHAs are source/evidence inputs. They are not merge sources for this phase.

## 4. Mandatory preflight and measured baseline

Before refactoring, record the current state on the fresh implementation base.

### 4.1 Forge baseline

Run from `forge/`:

```bash
npm ci
npm test
npm run fixtures
git diff --exit-code -- test/fixtures/envelope
npm run build
```

Also record:

- exact Node/npm versions;
- total/pass/fail/cancelled test counts;
- raw `forge_bundle.js` bytes;
- gzip bytes using a deterministic command/tool recorded in the handoff;
- `npm audit --omit=dev --audit-level=high` result;
- full `npm audit` headline separately so dev-only debt is not confused with shipped-runtime risk.

If the baseline is red, isolate the defect before the extraction. Do not bury a baseline fix inside a large refactor.

The planning package observed a stale release-loader marker assertion on its older base. If that exact defect still exists on fresh `main`, fix only the false assertion needed to match the real release contract and prove it independently. Do not import unrelated release-loader changes from the Quest Studio branch.

### 4.2 Repository gates

Run and record:

```bash
python3 skills/building-tnr-content/scripts/doctrinemap.py
python3 skills/building-tnr-content/scripts/render_doctrine.py --check
python3 skills/building-tnr-content/scripts/build_packs.py --check
python3 skills/building-tnr-content/scripts/lawmap.py .
```

Phase 0 is not a doctrine/law rewrite. Existing warnings are evidence to record, not permission to alter canon.

### 4.3 Game-source drift measurement

Public `studie-tech/TheNinjaRPG` `main` was observed at contract-authoring time at:

`1fd355ab92cec78148130e02c8d38834836c3181`

Re-verify upstream `main` at task start and rerun the Forge-relevance drift check required by the planning package. Inspect the source assumptions Forge depends on, including host/takeover/session/auth/tRPC/procedure/contract surfaces relevant to current Forge.

Phase 0 **measures and records drift**. It does not silently:

- move Forge's generated-contract pin;
- regenerate/adopt source contracts;
- change auth semantics;
- change procedure shapes;
- change game source.

Any material contract adoption discovered by the drift pass becomes a separately scoped Lane-A task unless it is strictly necessary to make the current baseline truthful.

## 5. Architecture contract

### 5.1 Extract a headless ForgeCore

Create an explicit core layer under `forge/src/core/`.

Move orchestration/domain responsibilities out of the view layer. The exact module split is Fable's engineering decision, but the boundary must absorb the responsibilities currently living in `ui/app.mjs` such as:

- manifest/work-package selection and lifecycle orchestration;
- start/resume/halt/reconcile decisions that are not presentation;
- blocked-path and resume-blocked reasoning;
- capture materialization/result shaping;
- export/result preparation;
- repository-sync orchestration/state;
- confirmation/decision-gate facts, while leaving final confirmation presentation in the UI;
- any other stateful workflow logic a second shell would otherwise have to duplicate.

The core owns machine state and actions. The UI renders core state and invokes core actions.

No module under `core/` may depend on DOM globals, `window`, userscript takeover mechanics or presentation CSS/classes.

### 5.2 Composition root

`forge/src/main.mjs` `compose()` becomes the explicit dependency/composition root for the core and the userscript host.

The current userscript behavior must remain available through the same public entry behavior. A headless test host must be able to construct/use the core without a DOM.

### 5.3 Host isolation

Move userscript/browser takeover responsibilities toward `forge/src/hosts/userscript/` as planned, while preserving behavior exactly.

This phase does not redesign host routing, authentication or overlay presentation.

In particular:

- `/forge` handoff behavior stays the same;
- carrier/provider runtime behavior stays the same;
- unarmed game pages stay untouched;
- current auth/session protections stay intact;
- release-loader behavior stays intact except a proven baseline-test correction if required.

### 5.4 Import-direction boundary

Add a mechanical import-direction gate.

Target architecture:

- execution/storage/transport/budget/reconcile may not import UI or host code;
- core may depend on the lower execution layers;
- UI/hosts may depend on core interfaces;
- core may not import UI/hosts;
- cross-seam leaks are driven to zero and stay zero in CI.

Record the starting leak count on fresh `main`; do not copy the old planning count as current evidence.

### 5.5 DOM helper hardening

Add the accepted deny-list behavior to `forge/src/ui/dom.mjs` if fresh `main` does not already contain equivalent protection.

The helper must reject computed/property assignment to HTML-string sinks including at least:

- `innerHTML`
- `outerHTML`
- `srcdoc`
- `insertAdjacentHTML`

for every value type, not only string literals.

This hardening must produce no visible UI change.

### 5.6 Repository/manifest text storage

Repository text/manifest caching that does not belong in the game capture cache must move to a **separate IndexedDB database**, not a version bump of the existing `tnr_forge` database.

Do not raise the current capture-cache database version in Phase 0 merely to store repository text. Rollback to the previous released bundle must remain able to open the existing capture/journal data it already understands.

Retained Builder compatibility keys stay untouched in shape.

## 6. Execution-core preservation rule

The following are preservation surfaces for Phase 0:

- `forge/src/storage/journal.mjs`
- `forge/src/storage/compat.mjs`
- `forge/src/transport/**`
- `forge/src/budget/**`
- `forge/src/reconcile/**`
- `forge/src/runner/**`, except the single additive event hook below.

No state-machine redesign, transport redesign, rate-budget change, reconciliation change, journal migration or procedure-contract change is allowed in this phase.

### 6.1 The one permitted runner change

Add one structured progress/event emitter adjacent to the existing injected log/progress seam in the runner.

Contract:

- advisory only;
- may not write the journal;
- may not advance or rewrite item/job state;
- may not change request ordering;
- may not alter retry/reconcile semantics;
- a throwing/broken subscriber must not affect journal bytes, send order, transition sequence or job result.

Put this execution-core edit in its own focused commit and identify that commit SHA in the handoff. `PH-0.seam` should otherwise be empty.

## 7. UI identity gate

Before moving domain logic, commit deterministic fixtures/serialization for the current five released Forge screens.

After extraction, those fixtures must be byte-identical.

Do not use this phase to improve copy, classes, navigation, layout, colour, typography, spacing, button hierarchy or interaction design.

Existing UI regression tests must not be weakened or deleted to make the extraction pass. Test relocation/adapter changes are allowed only where they preserve the same assertion.

Any visible UX improvement belongs to the later shell/design phase.

## 8. Required Phase-0 tests

Add/retain evidence for all of the following.

### Core/host

- full lifecycle driven through ForgeCore with no DOM global;
- explicit core API/snapshot golden so the UI boundary cannot silently widen;
- userscript host still produces the existing screen fixtures byte-for-byte;
- import-direction gate reaches zero prohibited imports;
- host release/takeover semantics preserved.

### State and execution safety

- the full existing journal transition/recovery suite remains green;
- SENT can never be resent by the refactor;
- auth refusal/recovery behavior remains green;
- reconciliation behavior remains green;
- budget behavior remains green;
- runner event subscriber exception has zero state/send-order effect;
- no new path bypasses existing preflight/runner/reconcile composition.

### UI/DOM

- all existing screen tests remain green;
- deterministic five-screen serialization is identical before/after;
- HTML-sink deny-list rejects computed non-string and string assignments;
- stylesheet/output unchanged in this phase.

### Storage

- new repository-text storage is isolated from the existing `tnr_forge` capture database;
- reopening/rollback assumptions are tested without increasing the existing DB version;
- Builder compatibility keys stay intact.

### Contracts/build

- `fields.json` / `nested.json` provenance/drift gate is rerun against their owning generated source and current declared pin;
- fixtures regenerate with no unintended diff;
- `forge_bundle.js` rebuild is reproducible;
- raw and gzip bundle budgets compare against the recorded fresh-main baseline;
- no new production dependency is introduced without explicit justification.

### Static live-safety gate

Maintain/extend a static check that implementation/build/compiler/worker code in scope contains no live-game network path outside Forge's existing reviewed transport boundary.

This Phase-0 task itself makes **zero** request to any TNR game host.

## 9. CI contract

Phase 0 leaves Forge with one canonical Node gate set.

Required behavior:

- one `npm ci` / test / fixtures / build path for Forge;
- `npm audit` policy retained rather than silently dropped;
- import-direction check included;
- bundle raw/gzip budget included;
- checked-bundle reproducibility included;
- contract/projection drift checks included where appropriate;
- no-live static gate included.

The accepted Quest Studio branch currently carries its own CI because it is not integrated. **Do not import Quest Studio or `quest_studio_ci.yml` into Phase 0 simply to consolidate it.**

When the reviewed Studio seam is integrated in its later dedicated integration slice, its Python worker/compiler/Mission gates must fold into the canonical Forge/repository gate structure rather than creating a second permanent full Node test job.

## 10. Quest Studio constraints carried forward, but not implemented here

Phase 0 must leave room for the accepted Studio seam but must not merge it.

The later Studio integration must preserve:

- source-push build request model;
- browser repository credential: **Contents write only**;
- **no Actions write**;
- **no Workflows write**;
- Workflows-write prohibition as a security invariant;
- trusted-main compiler / authored-data branch separation;
- exact source-revision correlation;
- stale-result refusal;
- `generated.manifestSha256` binding and fetched-manifest re-hash;
- request-scoped generated persistence;
- zero-live compiler boundary.

Do not re-ask K-26's credential-scope decision.

The final Studio review's nonblocking follow-ups remain future obligations:

- **N1:** pin the worker-definition equality check's execution order in the worker contract test;
- **N2:** make stale-worker/request-branch fail-closed behavior legible/recoverable instead of only becoming a poll timeout;
- **N3:** improve the cosmetic failure message if the authored-request checkout is absent when `always()` persistence evaluates;
- **N4:** reconcile base drift and preserve both 2026-09-16 rulings.

These do not belong in Phase 0 unless Fable can prove a change is necessary to preserve the Phase-0 boundary. Default: leave them for the dedicated Studio integration/Phase-S brief.

## 11. Explicitly out of scope

Do not implement or merge any of the following in Phase 0:

- Quest Studio implementation or its standalone shell;
- Quest Studio worker/compiler files;
- Quest Studio subtype expansion;
- Content Admin;
- Project Workspace;
- new navigation / Command Center;
- visual-design token rollout;
- mode/lane taxonomy;
- manifest UX redesign;
- new capture capabilities;
- paged/filtered capture work;
- journal schema/version migration;
- Builder retirement/deprecation;
- release pin/version movement;
- live-game smoke write;
- game-source changes;
- generated-contract pin movement/adoption;
- doctrine or engine-law rewrites;
- any user-owned balance/reward/publishing/art decision.

Do not merge `claude/forge-next-planning-reconciled` or `chatgpt/forge-quest-studio-foundation` wholesale into the Phase-0 branch.

## 12. Director decisions

**None are required to begin or finish Phase 0.**

K-13, K-14 and K-60 are engineering decisions/positions and must be resolved in the implementation/handoff by Fable, then independently reviewed.

K-26's director half is already settled by `RUL-2026-09-16-002` and the director's source-push choice. It is not an open Phase-0 or Studio credential-scope question.

If implementation uncovers a genuinely new product/UX/publishing/security consequence that belongs to the director, stop only the dependent part and surface it separately. Do not turn ordinary module boundaries, commit structure or test mechanics into director decisions.

## 13. Phase-0 acceptance gates

### PH-0.state

Every state rendered by the existing Forge UI must still come from a machine state owned by the execution/auth/budget/capture/reconcile/core layers. The refactor may not create view-local pseudo-state that changes the meaning of an existing machine state.

### PH-0.seam

Final changed-file inventory under:

- `forge/src/runner/`
- `forge/src/storage/`
- `forge/src/transport/`
- `forge/src/budget/`
- `forge/src/reconcile/`

must be empty except for the one reviewed additive runner progress-emitter file/change. New repository-text storage should live outside the existing execution/capture database seam and must not require a journal/capture DB version rise.

### Visual identity

The five existing released screens and their user-facing copy/structure are fixture-identical to the fresh-main baseline.

### Headless core

A whole lifecycle is testable with no DOM global and with the public core API/snapshot contract pinned.

### Baseline and gates

Tests, fixtures, bundle reproduction, import direction, source/contract drift checks, bundle budgets and repository coherence gates are green or any pre-existing exception is named with exact evidence.

## 14. Commit/review shape

Keep the branch reviewable. Recommended commit boundaries:

1. **baseline evidence / deterministic UI fixtures** — no behavior change;
2. **ForgeCore + composition/host extraction** — execution core untouched;
3. **single additive runner event emitter** — isolated execution-core commit;
4. **repository-text storage separation + DOM helper hardening**, if not already naturally contained in #2;
5. **CI/static/import/bundle gates and generated bundle**.

Do not squash away the isolated runner change before independent review.

The final review target is one frozen exact SHA. ChatGPT will independently inspect all commits and may narrow-review individual corrections later if the first review supports that.

## 15. Required implementation handoff

Return a durable handoff following `docs/workflows/IMPLEMENTATION_HANDOFF.md` with at least:

- repository;
- implementation branch;
- exact fresh-main base SHA;
- exact frozen head SHA;
- merge-base;
- commit list and the isolated runner-emitter commit SHA;
- changed-file list grouped by core / host / UI / execution seam / tests / CI / generated bundle;
- baseline test counts and final test counts;
- Node/npm/Python versions;
- raw + gzip bundle baseline and final sizes;
- fixture result;
- bundle reproducibility result;
- `npm audit --omit=dev` and full-audit headline;
- import-direction gate result;
- current upstream game-source SHA used for the drift measurement;
- what the drift check found and whether anything was deliberately **not** adopted;
- doctrine/projection/pack/law gate results;
- exact list of any files changed in runner/storage/transport/budget/reconcile;
- known debt/deviations;
- unverified browser/device behavior;
- explicit statement that no live request/write/credential material was used;
- explicit statement that Quest Studio, Content Admin, shell redesign and Builder retirement have not begun.

Freeze the SHA after handoff.

## 16. What follows Phase 0

Do not begin the next implementation phase from this brief.

After Phase 0 is independently reviewed and integrated, the next work must be briefed from the reviewed new `main`.

The accepted programme order remains:

1. Phase 0 — headless core and measured baseline;
2. Phase 1 — research/capture tiers and registry policy;
3. Phase 2 — visual shell/design system;
4. Phase 3 — manifest/recovery experience;
5. dedicated Quest Studio fresh-main integration, then Phase S product absorption under the shared shell;
6. Content Admin / publish / Project Workspace according to their own gates and director decisions;
7. Builder retirement only after its retirement gates are actually closed.

Before the accepted Quest Studio seam is integrated, reconcile its old base deliberately with then-current `main`, preserve both `RUL-2026-09-16-001` and `RUL-2026-09-16-002`, close/assign N1-N4, and run the required repository-only `studio/quest/*` end-to-end rehearsal after the seam exists on `main`. That rehearsal has **zero live-game contact**.
