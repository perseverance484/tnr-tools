# Workflow — Fable Review

Use for independent review of a Fable / Claude Code plan or implementation.

This workflow establishes the **review method**. A task-specific review prompt may add stricter invariants, source pins, scratch-test locations, prohibited paths, report format, or zero-network requirements; those task constraints remain binding.

## 1. Establish the target

Before forming an opinion:

- verify repository `perseverance484/tnr-tools`;
- verify live `main`;
- record the exact Fable branch and frozen handoff SHA;
- verify intended base/merge-base when relevant;
- confirm whether the branch is frozen for review;
- identify any related audit/report branches that are evidence but must not be merged into the target.

Do not review a moving branch. Do not reuse a finding from an older panel/session without reproducing it against the current frozen tree.

## 2. Reconstruct authority

Read in this order unless the task gives a stricter order:

1. current `state/active-context.md` / `state/status.json` as operational orientation;
2. `docs/00_INDEX.md` for precedence and evidence tiers;
3. the task/build brief/plan/design contract;
4. task-specific handoff/notes whose claims are reviewable;
5. relevant `docs/DOCTRINE.md` / `docs/10_LAWS_core.md` / `docs/ENGINE_LAWS.md` sections as routed;
6. generated contracts/verification reports/captures required by the task;
7. exact pinned `studie-tech/TheNinjaRPG` source when the task pins it;
8. target implementation, tests, fixtures, build scripts, and checked-in bundles/artifacts;
9. `CHATGPT.md`, `docs/agents/ENGINEERING_AUDITOR.md`, and this workflow for collaboration method.

If the task supplies its own explicit read order, follow it where it is stricter or more specific.

## 3. Safety envelope

Treat the live game as production.

Default review behaviour:

- no game writes;
- no acquisition/request/synthesis/exposure of session cookies or live credentials;
- no exploratory production requests merely to answer a review question;
- prefer pinned source, local source files, fixtures, committed captures, and in-process/local-file harnesses;
- do not run the game source unless explicitly authorized;
- obey task-specific zero-live-request/network restrictions literally.

If a browser/live session is genuinely required to settle a point and the task does not authorize it, leave the point **unverified**.

## 4. Review by invariant

For each important layer/claim:

1. state the invariant or contract being tested;
2. identify the code paths/exported calls/state transitions that could violate it;
3. construct a reproduction or adversarial case;
4. run/inspect against the exact current tree;
5. try to refute the suspected finding using the implementation, tests, governing source, and expected semantics;
6. report it only if it survives.

Evidence beats intuition.

## 5. Areas to attack when applicable

### State/storage/journals

- illegal backward transitions;
- persistence ordering around irreversible work;
- corruption isolation;
- crash/restart behaviour;
- hand-edited/migrated record safety;
- invalidation/mapping consistency;
- concurrent-tab ownership/leases.

### Transport/protocol

- exact request/response shapes vs fixtures/source;
- decode ambiguity around mutations;
- request-level vs per-item errors;
- origin/path/header allowlists;
- credential separation;
- HTML/gateway/body-read failures.

### Budgets/rate limits

- formula parity with pinned server/source dependency;
- boundary/bucket alignment;
- persistence before send/acquire;
- restart/clock/bucket-edge overspend;
- partial response / 429 semantics;
- path coverage completeness.

### Runner/reconcile

- duplicate sends after crash/retry/resume/reconcile;
- ambiguous SENT handling;
- placeholder/orphan adoption mistakes;
- cross-job adoption;
- deterministic local failures occurring after irreversible creates;
- update-field preservation;
- read-back/reconciliation drift;
- DONE/re-run/idempotence behaviour.

### Validation/contracts

- required fields vs pinned validators/source;
- extractor omissions, spreads, dynamic members;
- stale generated reports;
- unknown/server-owned field handling;
- data-type/enum/bound mismatches;
- disabled/stale check sources accidentally wired into production.

### UI/operator path

- safe DOM construction and repository UI laws;
- route/takeover assumptions vs pinned client source;
- mobile/operator legibility;
- ambiguous write state represented as success;
- session/auth assumptions labeled verified vs inferred.

### Build/bundle fidelity

- regenerate checked-in bundles/artifacts through the documented build;
- diff them against source output;
- investigate drift rather than assuming the bundle is faithful.

## 6. Scratch tests

When a task permits scratch tests:

- place them only in the task-approved gitignored/scratch location;
- do not commit them unless the task explicitly changes that rule;
- keep them targeted to the invariant;
- record the exact command and result in the review;
- do not let scratch infrastructure mutate production/config state.

If the task specifies a scratch path, use exactly that path.

## 7. Source and report discipline

- A generated report is only as trustworthy as its extractor and source pin.
- A verification report explicitly designated as higher authority wins over a conflicting preliminary extraction where the task says so.
- Inspect stale-file claims yourself when feasible.
- Do not infer validator fields from a generated JSON if the task requires checking the validator source directly.
- Do not substitute current upstream source for a pinned source SHA.
- Do not paraphrase/copy prohibited game prose when the task forbids it.

## 8. Classify findings

Useful categories:

- **Confirmed defect**
- **Contract/source mismatch**
- **Stale documentation/report**
- **Needs refinement**
- **User decision required**
- **Unverified risk**
- **Expected behaviour**
- **Operator inconvenience / low severity**
- **Approved / sound**

Severity is by consequence to production data and safe operation.

Examples:

- duplicate create / corrupted live column / unsafe ambiguous resend → high;
- credential leakage / cross-origin auth escape → high;
- inability to recover from a mutation crash → potentially high;
- misleading but recoverable operator friction → lower;
- cosmetic reviewer preference → not a correctness finding.

## 9. Proposed fixes

Review remains review.

- Prefer the smallest robust fix.
- Do not commit fixes to Fable's active branch.
- If the task is review-only and asks for diffs, provide proposed diffs in the report only.
- Do not redesign architecture merely because another design is possible.
- If a finding exposes a user-owned design choice, separate that choice from the engineering fix.

## 10. Durable review

When the review should be durable and the task permits repository records:

- create `chatgpt/review-<task>` without modifying the Fable branch;
- normally anchor it to the exact reviewed handoff when preserving the target relationship is useful;
- add `docs/reviews/<TASK>_REVIEW.md`;
- record exact target/base, verdict, evidence, findings, tests/gates, unverified items, and next workflow step.

When the task explicitly requires a returned-but-uncommitted report, follow that instead.

## 11. Correction loop

Fable applies accepted fixes on its own branch and returns a new frozen SHA.

Re-review only the agreed correction surface when:

- the first review explicitly scoped a narrow re-check;
- the fixes did not alter wider assumptions or architecture;
- the base/target relationship remains valid.

Otherwise repeat the relevant audit scope.

## 12. Integration gate

Recommend integration only when:

- confirmed blockers are closed;
- required user rulings are recorded or safely deferred;
- required tests/gates/builds/fixtures are green;
- source/generated artifact agreement is adequate for the task;
- no merge-blocking contradiction remains;
- the implementation still points at the reviewed SHA;
- unverified browser/live/session items are clearly identified and are not being mistaken for verified safety.

A clean review is a valid outcome. Do not manufacture findings.
