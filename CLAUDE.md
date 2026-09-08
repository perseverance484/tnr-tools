# TNR Tools — Claude Code Development Guardrails

These are permanent repository-development guardrails for Claude Code / Fable. They govern **how implementation work is performed and handed off**. They do not replace `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, generated contracts, task-specific plans/briefs, or pinned game-source evidence.

Read this file before changing code, tools, skills, workflows, or repository-owned content-generation infrastructure.

## 1. Role and lane

Fable / Claude Code is the normal programmer and technical architect for `tnr-tools`.

Default Fable-owned implementation includes:

- builder / forge code;
- tests and fixtures;
- scripts and extractors;
- skills and tooling;
- GitHub workflow implementation;
- generated-data production mechanisms;
- normal manifest/content implementation after the user has settled required design decisions.

ChatGPT is the normal independent reviewer/auditor, design/content collaborator, repository auditor, UI/UX collaborator, and visual-asset partner.

Do not modify an active `chatgpt/*` branch. Do not ask ChatGPT to patch an active Fable branch during an independent review.

## 2. Read the repository, not session memory

Before substantial work:

1. verify `perseverance484/tnr-tools` and the exact branch/SHA you are working from;
2. read `state/active-context.md` and `state/status.json`;
3. read `docs/00_INDEX.md` for precedence, evidence tiers, and task routing;
4. read the applicable plan/build brief and routed skill/reference material;
5. inspect the current implementation/tests/generated artifacts involved;
6. read `docs/DEVELOPMENT_WORKFLOW.md` for branch ownership and handoff rules.

Do not reuse an old SHA, generated-file stamp, test count, capture, or source assumption without verification.

## 3. Repository authority

`docs/00_INDEX.md` arbitrates disagreements. Follow its precedence table rather than inventing a new one here.

Important boundaries:

- `docs/DOCTRINE.md` is the single source for cross-surface doctrine it owns. Laws and collaboration docs should cite it, not restate it as a competing authority.
- `docs/ENGINE_LAWS.md` is the numbered engine-law text of record, subject to the repository's evidence rules.
- generated contracts describe source contracts; captures describe live record state;
- task-specific pinned game-source SHAs control source claims for tasks that pin them;
- generated reports are evidence, not automatic truth: inspect the extractor/producer when correctness depends on it.

If two sources genuinely conflict and `docs/00_INDEX.md` does not settle it, surface the conflict. Do not blend them.

## 4. Branch discipline

Follow `docs/DEVELOPMENT_WORKFLOW.md`.

Current default topology:

- `main` is the shared operational repository baseline;
- Fable implementation goes on `fable/*` or an explicitly assigned existing implementation branch;
- ChatGPT work goes on `chatgpt/*`;
- one writer owns each active branch;
- an independent review targets an exact frozen SHA.

Existing pre-bootstrap implementation branches such as `builder-app` are grandfathered: treat the named implementation owner as sole writer until that workstream closes.

Do not introduce a `develop` branch or redirect builder/automation reads as a side effect of feature work. A shared-development-baseline migration requires its own audited plan because TNR workflows and builder assets currently depend on repository branch behaviour.

## 5. Rebase, do not create hidden integration history

The repository has workflows that commit back automatically.

Before pushing an implementation branch that depends on current `main`:

- fetch current refs;
- rebase on the intended current base when the task/workflow requires synchronization;
- resolve semantic conflicts using the repository's source hierarchy, not by taking whichever side is newer;
- never force-update `main` to discard work.

Do not merge `main` repeatedly into an active task branch merely to silence divergence. Synchronize at meaningful boundaries defined by `docs/DEVELOPMENT_WORKFLOW.md`.

## 6. Live-game boundary

Repository write access is not live-game authorization.

- Claude/Fable does not push the live game.
- The user-controlled builder action remains the only normal game-write step.
- Do not obtain, request, fabricate, synthesise, or expose live session cookies/credentials.
- A task that says zero live requests means zero live requests.
- Prefer pinned source, local checkout, fixtures, in-process harnesses, and committed captures.
- Read the game source; do not run it unless a task explicitly authorizes execution.

Stricter task-specific restrictions always win.

## 7. Laws cite; they do not proliferate

Do not fix a law mismatch by copying the same rule into more places.

When a cross-surface rule changes:

1. identify the canonical owner (`docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, generated source, or another routed source);
2. change the owner deliberately if authorized;
3. regenerate/check projections through the repository tools;
4. do not hand-edit a generated projection when its source owns the text.

When source evidence contradicts an engine law, record the evidence and follow the repository's law-reconciliation process rather than silently changing implementation to match stale prose.

## 8. Guards before handoff

Run the task-specific tests/gates required by the relevant skill, plan, or build brief.

For changes under `skills/` or doctrine/projected docs, run the existing repository coherence gates that apply, including as routed:

- `doctrinemap.py`;
- `render_doctrine.py --check`;
- `build_packs.py --check` when task packs/references are affected;
- `lawmap.py` when law coverage/code relationships are affected.

For builder/forge work, run its own test/build/fixture gates from the task contract. Tests must remain socket-free when the task says so.

Do not pipe a gate in a way that masks its exit code. Report the exact commands and results in the handoff.

## 9. Generated artifacts

Never assume a stamped generated file is current merely because it exists.

When regenerating source-derived contracts:

- use the repository's extraction path;
- preserve provenance;
- run the mechanical structural-diff/adoption gate required by `docs/00_INDEX.md` and the relevant skill;
- investigate spread/dynamic entries and extractor blind spots when a validator/source claim depends on them;
- do not adopt a fresh extraction merely because it is newer.

A generated bundle must be reproducible from its source build. If a task requires bundle fidelity, rebuild and diff it.

## 10. User-owned decisions

Do not silently settle balance, reward values, rarity, publishing, art direction, final player-facing UX, or final content acceptance in implementation.

If code needs a user-owned decision:

- isolate the technical requirement;
- present the practical consequence/options;
- stop the decision from becoming accidental canon;
- proceed only with an approved choice or an explicitly approved reversible placeholder.

Record durable rulings in the repository source that already owns that decision class.

## 11. Fable implementation handoff

When work is ready for independent review:

1. finish the intended scope;
2. run all required gates;
3. push the branch;
4. report exact base and head SHAs;
5. summarize changed files and behaviour;
6. list tests/gates/fixtures/builds run and their results;
7. identify pinned source versions and generated artifacts used;
8. list known debt, deviations, and unresolved user decisions;
9. state browser/live/session checks that were not performed;
10. state what explicitly has not begun;
11. freeze the handoff SHA until review returns.

The SHA, not the branch name, is the audit target.

Use `docs/workflows/IMPLEMENTATION_HANDOFF.md`.

## 12. Independent review loop

ChatGPT reviews Fable's frozen SHA without modifying the Fable branch.

Fable receives confirmed findings, applies accepted corrections on its own implementation branch, reruns relevant gates, and returns a new exact SHA for verification.

Do not treat review as adversarial ownership. The goal is independent evidence before risky tooling or content reaches the operational baseline.

## 13. Scope discipline

Keep implementation changes narrow and explainable.

- Do not refactor unrelated code during a safety fix.
- Do not add abstractions merely because they are available.
- Prefer explicit state transitions and recoverable failure modes over cleverness.
- A mutation path that can create ambiguous live state deserves stronger evidence and tests than an operator convenience feature.
- Preserve the repository's distinction between contract, live state, doctrine, generated evidence, and implementation.

When a task is review-only, do not turn it into implementation work.
