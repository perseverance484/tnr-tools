# TNR Tools development workflow

**Status:** binding collaboration workflow for the user, Fable / Claude Code, and ChatGPT.

This document governs **how concurrent implementation, review, design-support, audit, and art work reaches `perseverance484/tnr-tools`**. It does not override `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, generated contracts, task-specific plans/briefs, skill references, or pinned source evidence.

## 1. Current repository topology

### `main` — shared operational baseline

`main` is currently the shared repository baseline used by TNR Tools' established workflows and operator tooling.

- Verify live `main` before beginning substantial work.
- Automated workflows may commit generated artifacts back to `main`; a remembered head can become stale without a human push.
- Do not force-push or rewrite `main`.
- Human/agent implementation should normally arrive through a reviewed task branch rather than direct ad-hoc edits to `main`.
- Existing auto-commit workflows are explicit exceptions; preserve their documented behaviour unless a separate migration changes it.

### No implicit `develop` branch

Astaron uses a shared `develop` baseline, but TNR Tools does **not** adopt that topology merely because the collaboration model is similar.

A future `develop` migration would need to audit at least:

- builder/root asset fetch refs;
- GitHub Actions trigger/checkout/auto-commit behaviour;
- skillpack/root-config synchronization;
- answers/harvest regeneration;
- release/pin/relay workflows;
- any raw/CDN/default-branch assumptions;
- the user’s mobile operating ritual.

Until such a migration is separately planned, reviewed, and approved, `main` remains the shared operational baseline.

## 2. Branch roles

### `fable/*` — implementation workspace

Fable / Claude Code is the sole normal writer to `fable/*` branches.

Use them for:

- builder / forge implementation;
- tests and fixtures;
- scripts, extractors, validators, and toolchain work;
- skill implementation;
- GitHub workflow implementation;
- generated-data mechanics;
- technical implementation plans;
- content-manifest implementation after required user decisions are settled.

Examples:

- `fable/forge-hardening`
- `fable/schema-regen-safety`
- `fable/mission-builder-fix`

Existing task branches created before this workflow—such as `builder-app` and the client-contract audit/verification branches—are grandfathered. Treat their named implementation/audit owner as sole writer until the workstream closes.

### `chatgpt/*` — review, audit, design-support, and art workspace

ChatGPT is the sole normal writer to `chatgpt/*` branches.

Use them for:

- independent Fable reviews;
- durable review reports under `docs/reviews/`;
- repository/milestone audits;
- collaboration/workflow infrastructure;
- design-support documents where a durable repo record is appropriate;
- art-direction/production support records and approved visual assets when the repository is the correct home;
- integration/status documentation that does not belong to the generated session-state pipeline.

Examples:

- `chatgpt/review-forge-hardening`
- `chatgpt/repository-audit`
- `chatgpt/art-village-official`

### `coord/*` — narrow shared rulings, if needed

Use only when an approved user decision must reach multiple active workstreams before either can continue.

A `coord/*` branch should contain the smallest durable change that records the settled ruling in the correct canonical owner. It is not a general feature branch.

## 3. One writer per active branch

**Do not commit to another agent's active branch.**

- ChatGPT does not add review files or fixes directly to `fable/*` or an active Fable-owned legacy branch.
- Fable does not modify `chatgpt/*`.
- Review findings do not mutate the object being reviewed.
- If a review must become durable repository evidence, ChatGPT uses its own branch, normally based on the exact frozen Fable handoff SHA when preserving that relationship matters.

This keeps the audit target stable and prevents one agent from invalidating the other's working context.

## 4. Authority and decision ownership

Repository precedence remains governed by `docs/00_INDEX.md`.

This workflow does not create content or engine canon.

User-owned decisions include the classes already reserved by repository doctrine, including balance, rewards, rarity, publishing, art direction, final acceptance, and live-game actions.

When Fable or ChatGPT encounters a genuine user-owned decision:

1. identify the decision separately from implementation detail;
2. explain the practical consequence and options;
3. prevent the dependent implementation from quietly settling it;
4. obtain the user's ruling;
5. record the ruling in the repository source that already owns that class of decision when a durable record is required;
6. resume dependent work only after the decision is sufficiently resolved or explicitly deferred.

Use `docs/workflows/DIRECTOR_DECISIONS.md`.

## 5. Fable implementation cycle

### Start

1. Verify the live repository and `main` head.
2. Read `state/active-context.md`, `state/status.json`, and `docs/00_INDEX.md`.
3. Read `CLAUDE.md` and the relevant task plan/build brief, skill/reference, implementation, tests, and source contracts.
4. Create or use the explicitly assigned Fable-owned task branch.
5. Record exact base SHA in the working plan/handoff when the base matters.

### Implement

- Keep commits focused and runnable/reviewable.
- Stay inside the assigned task/pass boundary.
- Do not settle user-owned design decisions to make code convenient.
- Use generated contracts and repository tools instead of reconstructing shapes from memory.
- Run relevant tests/gates throughout the work.
- Preserve live-game safety: repository work is not authorization to contact or write the game.

### Handoff freeze

When requesting independent review:

- finish all intended commits;
- run required tests/gates/builds/fixtures;
- push the branch;
- provide exact base and head SHAs;
- summarize scope, changed files, tests, generated artifacts, source pins, deviations, known debt, and unverified browser/live behaviour;
- state what explicitly has not begun;
- **freeze the handed-off SHA until the review returns**.

The SHA, not the branch name alone, is the audit target.

Use `docs/workflows/IMPLEMENTATION_HANDOFF.md`.

## 6. ChatGPT review cycle

1. Reconstruct live repository state from `main`, current state files, and `docs/00_INDEX.md`.
2. Verify the exact Fable handoff branch and SHA.
3. Verify intended base/merge-base when it affects the review.
4. Read `CHATGPT.md`, `docs/agents/README.md`, `docs/agents/ENGINEERING_AUDITOR.md`, and `docs/workflows/FABLE_REVIEW.md`.
5. Read the governing task brief/plan, contracts, pinned game source, implementation, tests, fixtures, reports, and generated artifacts required by the task.
6. Try to reproduce and then refute suspected findings against the frozen target.
7. Report only findings that survive the evidence check.
8. Do not modify the Fable branch.

A review may be returned as a non-committed report when the task requires that. When durable review evidence is useful, use a `chatgpt/review-*` branch and `docs/reviews/` without altering the implementation target.

## 7. Finding discipline

When useful, classify review results as:

- **Approved / sound**
- **Confirmed defect**
- **Contract/source mismatch**
- **Stale documentation/report**
- **Needs refinement**
- **User decision required**
- **Unverified risk**
- **Expected behaviour**
- **Operator inconvenience / low severity**

Severity is based on realistic consequence:

- corrupt or lost game data;
- double creates/writes;
- ambiguous mutation state;
- credential/session exposure;
- broken recovery or reconciliation;
- silent schema/contract drift;
- user/operator inability to understand or recover;
- maintainability debt that makes future unsafe writes likely.

Do not inflate severity because code is complex or unfamiliar.

## 8. Correction loop

Fable applies accepted corrections on its own implementation branch and returns a new exact head SHA.

ChatGPT then:

- performs a narrow re-check only when the first review explicitly bounded the correction surface and no wider assumptions changed;
- otherwise repeats the relevant audit scope;
- verifies that the branch still points to the reviewed SHA before recommending integration.

Do not treat an author summary of the fix as evidence that the defect is closed.

## 9. Integration to `main`

An implementation is ready for integration when:

- required independent review is complete;
- confirmed blockers are closed;
- required user decisions are recorded or explicitly deferred in a way that makes the implementation safe;
- required tests/gates/builds are green;
- generated artifacts are reproducible/current where required;
- no merge-blocking source disagreement remains;
- live/browser/session uncertainty is clearly separated from what was actually verified.

Before integration, re-verify live `main` because auto-commit workflows or other workstreams may have advanced it.

Prefer a normal PR/reviewable merge path when feasible. Existing repository automation that legitimately writes generated artifacts back remains governed by its own workflow.

Do not force-update `main` to discard integrated or automated work.

## 10. Automated workflow writes

TNR Tools has GitHub Actions that may commit generated output back to the repository. Those commits are part of the repository's operational model, not evidence that direct human/agent writes to `main` are preferred.

Because automation can race with task branches:

- fetch before integration;
- follow the repository's rebase-first rule where applicable;
- inspect semantic conflicts rather than accepting whichever version Git selects;
- preserve generated-file ownership—edit the source, not the projection, when the toolchain says a file is generated.

If a workflow's branch behaviour changes, treat that as implementation work requiring review.

## 11. Live-game boundary

Git integration and live-game operation are separate systems.

- Fable and ChatGPT may work in GitHub within their assigned lanes.
- Neither agent treats GitHub write permission as permission to push the game.
- The user remains the live-game actor under repository doctrine.
- A repo branch can be safe to merge and still not be safe to run against production; reviews should say which conclusion they support.
- Zero-live-request tasks stay entirely on repository/source/fixture/in-process evidence.

## 12. Art workflow ownership

ChatGPT is the primary visual-asset/art-production partner, but the repository's existing art skill remains the production authority.

- Art direction/final acceptance belongs to the user.
- Use `skills/producing-tnr-art/SKILL.md` and its current spec/reference files.
- Keep image-production branches separate from active Fable implementation branches.
- If an asset is required by a Fable implementation, communicate the filename/contract through a durable handoff rather than having both agents edit one branch.
- Production QC and filename/versioning rules remain mandatory regardless of who generated the image.

Use `docs/workflows/ART_PRODUCTION.md`.

## 13. Design/content collaboration

ChatGPT may collaborate directly with the user on content/design decisions, critique, alternatives, player experience, and art direction.

Fable remains the normal implementation owner for manifests/tooling after decisions are settled.

A design discussion does not become repository canon merely because ChatGPT wrote a compelling draft. Durable changes go into the source that already owns that rule/content class, with user approval where required.

## 14. Synchronization rules

Do not continuously rebase every active branch merely because `main` moves.

Synchronize at meaningful boundaries:

- before starting a task;
- when a canonical/user ruling the task depends on lands;
- when a generated contract/source update the task depends on lands;
- before integration;
- before final review when base drift affects correctness.

If synchronization creates a semantic conflict in doctrine, engine laws, plans, generated source, or active state, stop and resolve the source-of-truth issue rather than choosing newer text automatically.

## 15. Branch cleanup

After work is integrated and no audit depends on the exact branch head:

- delete completed short-lived `fable/*`, `chatgpt/*`, and `coord/*` branches when safe;
- keep their commits through integrated history/PRs;
- retain historical branches only while they provide unique evidence or are explicitly referenced by an unresolved audit.

Do not merge an old branch merely because it exists.

## 16. Handoff minimum

Every substantial implementation handoff should include:

- repository;
- branch;
- exact base SHA;
- exact head SHA;
- changed-file scope;
- behavioural summary;
- tests/gates/builds/fixtures run;
- generated artifacts/provenance;
- external/pinned source SHA when relevant;
- known debt/deviations;
- open user decisions;
- browser/live/session checks not performed;
- what has not begun.

The independent reviewer should be able to reconstruct the task from repository evidence even if the implementation chat disappears.
