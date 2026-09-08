# TNR Tools development workflow

**Status:** binding collaboration workflow for the user, Fable / Claude Code, and ChatGPT.

This document governs **concurrent code/tooling implementation, independent review, design-support, audit, and art collaboration** in `perseverance484/tnr-tools`. It does not replace TNR's established content-production/session loop.

It does not override `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, generated contracts, task-specific plans/briefs, skill references, or pinned source evidence.

## 1. TNR has two Git lanes

Astaron's agent relationship is reused here, but TNR's repository already has an operational content-delivery system. Do not collapse those two concerns.

### Lane A — code/tooling/infrastructure work

Use the collaboration branch/review model in this document for changes such as:

- builder / forge implementation;
- tests and fixtures;
- scripts, extractors, validators, factories, and toolchain code;
- skill implementation or structural reference/tool changes;
- GitHub workflow implementation;
- schema/generator mechanics;
- collaboration/development infrastructure;
- engine-law/doctrine tooling changes;
- other repository changes where a defect could alter future production writes or contracts.

Fable / Claude Code is the normal implementation owner. ChatGPT is the normal independent reviewer/auditor.

### Lane B — established routine content production

Routine content production continues through the repository's existing system unless a separately approved migration changes it.

That includes the established `docs/00_INDEX.md` / mounted-instructions / skill / `state/` / `push/` / harvest/read-back loop in which Fable generates and validates content, pushes Git through the current approved repository ritual, and the user remains the only live-game actor.

This workflow does **not** require every ordinary validated content manifest or routine session-state update to wait for a new Fable→ChatGPT code-review branch cycle.

ChatGPT may collaborate on content design, critique, art, or an explicitly requested content audit. Fable remains the normal manifest/tool implementation agent. Existing validation, hidden/publishing, read-back, and user-push rules remain authoritative.

If a content task also changes code/tooling/contracts, split or clearly identify the Lane A portion and review it independently.

## 2. Current repository topology

### `main` — shared operational baseline

`main` is currently the shared repository baseline used by TNR Tools' established workflows and operator tooling.

- Verify live `main` before substantial work.
- Automated workflows may commit generated artifacts back to `main`; remembered heads can go stale without a human push.
- Do not force-push or rewrite `main`.
- Lane A code/tooling changes should normally arrive through a reviewed task branch rather than ad-hoc direct edits to `main`.
- Lane B routine content/session delivery continues through the existing repository ritual routed by `docs/00_INDEX.md` and current mounted instructions.
- Existing auto-commit workflows remain explicit parts of the operational model.

### No implicit `develop` branch

Astaron uses a shared `develop` baseline, but TNR Tools does **not** adopt that topology merely because the collaboration roles are similar.

A future `develop` migration would need to audit at least:

- builder/root asset fetch refs;
- GitHub Actions trigger/checkout/auto-commit behaviour;
- skillpack/root-config synchronization;
- answers/harvest regeneration;
- release/pin/relay workflows;
- raw/CDN/default-branch assumptions;
- current content/session rituals;
- the user's mobile operating workflow.

Until such a migration is separately planned, reviewed, and approved, `main` remains the shared operational baseline.

## 3. Branch roles for Lane A

### `fable/*` — implementation workspace

Fable / Claude Code is the sole normal writer to `fable/*` branches for code/tooling/infrastructure work.

Examples:

- `fable/forge-hardening`
- `fable/schema-regen-safety`
- `fable/builder-preflight-fix`

Existing pre-bootstrap implementation branches such as `builder-app` are grandfathered. Treat the named implementation owner as sole writer until that workstream closes.

Audit/report branches created for a specific verification purpose keep their own stated ownership and are evidence, not merge sources unless a task explicitly says otherwise.

### `chatgpt/*` — review, audit, design-support, and art workspace

ChatGPT is the sole normal writer to `chatgpt/*` branches.

Use them for:

- independent Fable reviews;
- durable review reports under `docs/reviews/`;
- repository/milestone audits;
- collaboration/workflow infrastructure;
- durable design-support records where appropriate;
- art-direction/production support records and approved visual files when the repository is the correct home.

Examples:

- `chatgpt/review-forge-hardening`
- `chatgpt/repository-audit`
- `chatgpt/art-village-official`

### `coord/*` — narrow shared rulings, if needed

Use only when an approved user decision must reach multiple active Lane A workstreams before either can continue.

A `coord/*` branch should contain the smallest durable change that records the settled ruling in the correct canonical owner. It is not a general feature branch.

## 4. One writer per active Lane A branch

**Do not commit to another agent's active branch.**

- ChatGPT does not add review files or fixes directly to `fable/*` or an active Fable-owned legacy branch.
- Fable does not modify `chatgpt/*`.
- Review findings do not mutate the object being reviewed.
- If a review must become durable repository evidence, ChatGPT uses its own branch, normally based on the exact frozen Fable handoff SHA when preserving that relationship matters.

This keeps the audit target stable and prevents one agent from invalidating the other's working context.

Lane B's established routine content/session loop is not redefined as concurrent agent branch ownership by this section.

## 5. Authority and decision ownership

Repository precedence remains governed by `docs/00_INDEX.md`.

This workflow creates no content or engine canon.

User-owned decisions include the classes already reserved by repository doctrine, including balance, rewards, rarity, publishing, art direction, final acceptance, and live-game actions.

When Fable or ChatGPT encounters a genuine user-owned decision:

1. identify the decision separately from implementation detail;
2. explain the practical consequence and options;
3. prevent dependent permanent work from quietly settling it;
4. obtain the user's ruling;
5. record the ruling in the repository source that already owns that class of decision when a durable record is required;
6. resume dependent work only after the decision is sufficiently resolved or explicitly deferred.

Use `docs/workflows/DIRECTOR_DECISIONS.md`.

## 6. Fable Lane A implementation cycle

### Start

1. Verify live repository and `main` head.
2. Read `state/active-context.md`, `state/status.json`, and `docs/00_INDEX.md`.
3. Read `CLAUDE.md` and the relevant task plan/build brief, skill/reference, implementation, tests, and source contracts.
4. Create or use the explicitly assigned Fable-owned task branch.
5. Record exact base SHA when the base matters.

### Implement

- Keep commits focused and runnable/reviewable.
- Stay inside the assigned task/pass boundary.
- Do not settle user-owned design decisions to make code convenient.
- Use generated contracts and repository tools instead of reconstructing shapes from memory.
- Run relevant tests/gates throughout the work.
- Preserve live-game safety: repository work is not authorization to contact or write the game.

### Handoff freeze

When requesting independent review:

- finish intended commits;
- run required tests/gates/builds/fixtures;
- push the branch;
- provide exact base and head SHAs;
- summarize scope, changed files, tests, generated artifacts, source pins, deviations, known debt, and unverified browser/live behaviour;
- state what explicitly has not begun;
- **freeze the handed-off SHA until the review returns**.

The SHA, not the branch name alone, is the audit target.

Use `docs/workflows/IMPLEMENTATION_HANDOFF.md`.

## 7. ChatGPT review cycle

1. Reconstruct live repository state from `main`, current state files, and `docs/00_INDEX.md`.
2. Verify the exact Fable handoff branch and SHA.
3. Verify intended base/merge-base when it affects the review.
4. Read `CHATGPT.md`, `docs/agents/README.md`, `docs/agents/ENGINEERING_AUDITOR.md`, and `docs/workflows/FABLE_REVIEW.md`.
5. Read the governing brief/plan, contracts, pinned source, implementation, tests, fixtures, reports, and generated artifacts required by the task.
6. Reproduce and then try to refute suspected findings against the frozen target.
7. Report only findings that survive the evidence check.
8. Do not modify the Fable branch.

A review may be returned as a non-committed report when the task requires that. When durable review evidence is useful, use a `chatgpt/review-*` branch and `docs/reviews/` without altering the implementation target.

## 8. Finding discipline

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
- duplicate creates/writes;
- ambiguous mutation state;
- credential/session exposure;
- broken recovery/reconciliation;
- silent schema/contract drift;
- user/operator inability to understand or recover;
- maintainability debt that makes future unsafe writes likely.

Do not inflate severity because code is complex or unfamiliar.

## 9. Correction loop

Fable applies accepted Lane A corrections on its own implementation branch and returns a new exact head SHA.

ChatGPT then:

- performs a narrow re-check only when the first review explicitly bounded the correction surface and no wider assumptions changed;
- otherwise repeats the relevant audit scope;
- verifies that the branch still points at the reviewed SHA before recommending integration.

Do not treat an author summary as evidence that a defect is closed.

## 10. Lane A integration to `main`

A code/tooling implementation is ready for integration when:

- required independent review is complete;
- confirmed blockers are closed;
- required user decisions are recorded or safely deferred;
- required tests/gates/builds are green;
- generated artifacts are reproducible/current where required;
- no merge-blocking source disagreement remains;
- live/browser/session uncertainty is separated from what was actually verified.

Before integration, re-verify live `main` because auto-commit workflows or Lane B work may have advanced it.

Prefer a normal PR/reviewable merge path when feasible. Existing repository automation and routine content delivery remain governed by their own current workflow.

Do not force-update `main` to discard integrated, automated, or content-delivery work.

## 11. Routine content/session synchronization

Lane B remains governed by the current repository instructions, including rebase-first behaviour where applicable.

Because routine content work and automation can advance `main` while Lane A branches are under review:

- do not continuously rebase a frozen review target;
- re-verify `main` before integration;
- synchronize the Fable branch at a meaningful boundary after review if needed;
- resolve semantic conflicts through `docs/00_INDEX.md` rather than choosing newer text automatically.

The goal is to preserve exact-SHA auditability without stopping the repository's ordinary content-production loop.

## 12. Automated workflow writes

TNR Tools has GitHub Actions that may commit generated output back to the repository. Those commits are part of the operational model.

Because automation can race with task branches:

- fetch before integration;
- follow the repository's rebase-first rule where applicable;
- inspect semantic conflicts rather than accepting whichever version Git selects;
- preserve generated-file ownership—edit the source, not the projection, when the toolchain says a file is generated.

If a workflow's branch/write behaviour changes, treat that as Lane A implementation work requiring review.

## 13. Live-game boundary

Git integration and live-game operation are separate systems.

- Fable and ChatGPT may work in GitHub within assigned lanes.
- Neither agent treats GitHub write permission as permission to push the game.
- The user remains the live-game actor under repository doctrine.
- A repo branch can be safe to merge while a manifest remains unsafe/unverified to run.
- Zero-live-request tasks stay entirely on repository/source/fixture/in-process evidence.

## 14. Art workflow ownership

ChatGPT is the primary visual-asset/art-production partner, but the repository's existing art skill remains production authority.

- Art direction/final acceptance belongs to the user.
- Use `skills/producing-tnr-art/SKILL.md` and its current spec/reference files.
- Keep ChatGPT art/review branches separate from active Fable code branches when repository writes are involved.
- If an asset is required by a Fable implementation, communicate the exact filename/contract through a handoff rather than both agents editing one active branch.
- Production QC and filename/versioning rules remain mandatory regardless of who generated the image.

Use `docs/workflows/ART_PRODUCTION.md`.

## 15. Design/content collaboration

ChatGPT may collaborate directly with the user on content/design critique, alternatives, player experience, and art direction.

Fable remains the normal content-manifest/tool implementation agent after decisions are settled.

A design discussion does not become repository canon merely because ChatGPT wrote a compelling draft. Durable changes go into the source that already owns that rule/content class, with user approval where required.

Routine manifest delivery then follows Lane B unless the task also changes Lane A code/tooling.

## 16. Synchronization rules for Lane A

Do not continuously rebase every active code branch merely because `main` moves.

Synchronize at meaningful boundaries:

- before starting a task;
- when a canonical/user ruling the task depends on lands;
- when a generated contract/source update the task depends on lands;
- after review and before integration when `main` drift must be incorporated;
- before final review when the base itself materially affects correctness.

If synchronization creates a semantic conflict in doctrine, engine laws, plans, generated source, or active state, stop and resolve the source-of-truth issue rather than choosing newer text automatically.

## 17. Branch cleanup

After Lane A work is integrated and no audit depends on its exact head:

- delete completed short-lived `fable/*`, `chatgpt/*`, and `coord/*` branches when safe;
- keep their commits through integrated history/PRs;
- retain historical branches only while they provide unique evidence or are explicitly referenced by an unresolved audit.

Do not merge an old branch merely because it exists.

## 18. Handoff minimum

Every substantial Lane A implementation handoff should include:

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
