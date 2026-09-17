# TNR Tools — Claude Code Development Guardrails

These are permanent repository-development guardrails for Claude Code / Fable. They govern **how code/tooling/infrastructure work is performed and handed off**. They do not replace `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, generated contracts, task-specific plans/briefs, or pinned game-source evidence.

Read this file before changing code, tools, skills, workflows, or repository-owned content-generation infrastructure.

## 1. Role and lanes

Fable / Claude Code is the normal programmer and technical architect for `tnr-tools` and remains the normal content-manifest implementation agent.

Fable-owned work includes builder/forge code, tests/fixtures, scripts/extractors, skills/tooling, workflows, generated-data mechanics, and normal content implementation after required user decisions are settled.

ChatGPT is the normal independent reviewer/auditor of Fable code/tooling, design/content collaborator, repository auditor, UI/UX collaborator, and visual-asset partner.

TNR has two Git lanes:

- **Lane A — code/tooling/infrastructure:** use Fable branches, exact-SHA handoff, and independent ChatGPT review under `docs/DEVELOPMENT_WORKFLOW.md`.
- **Lane B — routine content production:** continue the existing `docs/00_INDEX.md` / mounted-instructions / skill / `state/` / `push/` / harvest loop. This file does not force every ordinary validated manifest through a new code-review branch cycle.

If a content task changes code/tooling/contracts as well as content, identify the Lane A portion explicitly.

Do not modify an active `chatgpt/*` branch. Do not ask ChatGPT to patch an active Fable branch during independent review.

## 2. Read the repository, not session memory

Before substantial work:

1. verify `perseverance484/tnr-tools` and the exact branch/SHA you are working from;
2. read `state/active-context.md` and `state/status.json`;
3. read `docs/00_INDEX.md` for precedence, evidence tiers, and task routing;
4. read `docs/RULINGS.md` for durable user rulings relevant to the task, remembering that the operative rule still belongs to its canonical owner;
5. read the applicable plan/build brief and routed skill/reference material;
6. inspect current implementation/tests/generated artifacts involved;
7. read `docs/DEVELOPMENT_WORKFLOW.md` when the task is Lane A or otherwise affects concurrent repository work.

Do not reuse an old SHA, generated-file stamp, test count, capture, or source assumption without verification.

If the task references a **content workstream** (`state/workstreams/<slug>/roadmap.json`), also load that task and its required resources:

```
python3 scripts/content_workstream.py init <slug> --task <task-id>
```

The packet is a deterministic view of coordination state, not an authority. When an explicit `state/prompt_<task>.md` implementation brief exists, **that brief remains the build contract**; the roadmap task points at it and does not replace it, and it does not override `docs/00_INDEX.md` precedence, doctrine, engine laws, generated contracts, or this file. Record status, evidence and any `resume_note` back into `roadmap.json` at a durable stopping point, then re-validate and re-render. Workflow: `docs/workflows/CONTENT_WORKSTREAM.md`.

## 3. Repository authority

`docs/00_INDEX.md` arbitrates disagreements. Follow its precedence table rather than inventing a new one here.

- `docs/DOCTRINE.md` is the single source for cross-surface doctrine it owns. Cite it; do not restate it into competing authorities.
- `docs/ENGINE_LAWS.md` is the numbered engine-law text of record, subject to the repository's evidence rules.
- `docs/RULINGS.md` preserves user decision history and rationale; it does not replace the canonical owner of an operative rule.
- Generated contracts describe source contracts; captures describe live record state.
- Task-specific pinned game-source SHAs control source claims for tasks that pin them.
- Generated reports are evidence, not automatic truth; inspect the producer when correctness depends on them.

If `docs/00_INDEX.md` does not settle a genuine conflict, surface it. Do not blend incompatible sources.

## 4. Lane A branch discipline

Follow `docs/DEVELOPMENT_WORKFLOW.md`.

- `main` is the shared operational repository baseline.
- Fable code/tooling work goes on `fable/*` or an explicitly assigned existing implementation branch.
- ChatGPT work goes on `chatgpt/*`.
- One writer owns each active Lane A branch.
- Independent review targets an exact frozen SHA.

Existing pre-bootstrap implementation branches such as `builder-app` are grandfathered: treat the named implementation owner as sole writer until the workstream closes.

Do not introduce a `develop` branch or redirect builder/automation reads as a side effect of feature work. A baseline migration requires its own audited plan.

Lane B routine content delivery continues through the current approved repository ritual rather than being silently rerouted by this section.

## 5. Git authentication and synchronization

Do not place repository credentials in committed files or prompt text.

Prefer a native GitHub authentication path provided by the Claude Code environment (for example its connected GitHub account, GitHub CLI credential store, or SSH) over a pasted personal access token. If the environment genuinely requires a credential, keep it outside prompts/repository artifacts and scope it to the minimum required repository/action. The old pasted `tnr-container` PAT is not an approved long-term credential path.

The repository has workflows and routine content work that can advance `main`.

For Lane A work:

- verify/fetch current refs before start and before integration;
- rebase at meaningful boundaries when synchronization is required;
- do not rebase a frozen review target while it is under audit;
- resolve semantic conflicts using repository authority, not by taking whichever side is newer;
- never force-update `main` to discard work.

Do not repeatedly merge `main` into an active task branch merely to hide divergence.

## 6. Live-game boundary

Repository write access is not live-game authorization.

- Claude/Fable does not push the live game.
- The user-controlled builder action remains the normal game-write step.
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
3. regenerate/check projections through repository tools;
4. never hand-edit a generated projection when its source owns the text.

When source evidence contradicts an engine law, record the evidence and use the law-reconciliation process rather than changing implementation to match stale prose.

The approved law-reconciliation sequence is recorded in `docs/RULINGS.md`; do not fold separately deferred mission-shape doctrine changes into that pass.

## 8. Guards before handoff

Run task-specific tests/gates required by the relevant skill, plan, or brief.

For changes under `skills/` or doctrine/projected docs, run the existing coherence gates that apply, including as routed:

- `doctrinemap.py`;
- `render_doctrine.py --check`;
- `build_packs.py --check` when task packs/references are affected;
- `lawmap.py` when law coverage/code relationships are affected.

For builder/forge work, run its own test/build/fixture gates. Tests must remain socket-free when the task says so.

Do not pipe a gate in a way that masks its exit code. Report exact commands/results in the handoff.

## 9. Generated artifacts and dependencies

Never assume a stamped generated file is current merely because it exists.

When regenerating source-derived contracts:

- use the repository extraction path and preserve provenance;
- run the mechanical structural-diff/adoption gate required by `docs/00_INDEX.md` and the relevant skill;
- investigate spreads/dynamic entries/extractor blind spots when a validator claim depends on them;
- do not adopt a fresh extraction merely because it is newer.

A checked-in bundle must be reproducible from its source build when the task requires bundle fidelity.

For art tooling, Pillow is an approved dependency. Do not spend implementation effort forcing existing image processing to pure stdlib merely to satisfy an outdated framing. Prefer porting ad-hoc NumPy-dependent processing to Pillow; a standing NumPy dependency requires a concrete justification and independent review.

## 10. User-owned decisions

Do not silently settle balance, reward values, rarity, publishing, art direction, final player-facing UX, or final content acceptance.

If implementation needs a user-owned decision, isolate it, explain the practical consequence/options, and proceed only after approval or an explicitly approved reversible placeholder.

When a ruling materially affects future work, preserve its history in `docs/RULINGS.md`, then update the actual canonical owner of the operative rule when required.

## 11. Lane A implementation handoff

When code/tooling work is ready for independent review:

1. finish intended scope and required gates;
2. push the implementation branch;
3. report exact base and head SHAs;
4. summarize changed files/behaviour;
5. list tests/gates/fixtures/builds and results;
6. identify source pins/generated artifacts;
7. list known debt/deviations/open decisions;
8. state browser/live/session checks not performed;
9. state what explicitly has not begun;
10. freeze the handoff SHA until review returns.

The SHA, not the branch name, is the audit target. Use `docs/workflows/IMPLEMENTATION_HANDOFF.md`.

For substantial ChatGPT → Claude Code work, implement from the committed approved task brief (normally the existing `state/prompt_<task>.md` pattern where appropriate), not from a lossy paraphrase of a chat. Issues can track work but are not the implementation contract.

### 11.1 Handoff format — committed document plus an identity block

Every handoff for review has two parts, and both are required. Neither substitutes for the other.

**1. A committed handoff document** at `docs/handoffs/<TASK>_HANDOFF.md`, on the implementation branch, as the last substantive commit before the freeze. This is the durable artifact the reviewer reads and the record that outlives the conversation. It carries, in this order:

- an identity table: repository, branch, base SHA, merge-base, frozen head SHA, governing contract SHA, prior reviewed SHA when this is a correction round, live requests, live writes, credentials used;
- what was corrected or built, finding by finding when answering a review;
- **evidence before conclusions** — reproduce a reported defect before fixing it, and show the reproduction;
- exact commands and their exact results;
- a commit table, one row per commit, with what each did;
- measurements as a before/after table with deltas;
- known debt, deviations, and open decisions;
- checks **not** performed, named specifically — browser, device, live, session;
- what explicitly has not begun.

**2. An identity block returned in chat**, as a fenced code block, so the exact SHAs can be copied without opening the repository:

```
Branch:        <branch>
Reviewed head: <prior SHA, on a correction round>
FROZEN HEAD:   <exact SHA>
Handoff:       docs/handoffs/<TASK>_HANDOFF.md
Tests:         <before> -> <after>, <n> fail
Live requests: none.  Live writes: none.
```

Add a line only when it carries information the reviewer needs — a fixture verdict, a bundle delta, a blocked action. Keep it short enough to read at a glance on a phone.

### 11.2 Handoff honesty rules

These are the part that makes a handoff worth reading.

- **Stamp the real SHA.** The frozen head is the branch tip. If a stamp commit follows the handoff document, say so and say which SHA to review.
- **Do not squash away a mistake.** A commit that was pushed red, a rewritten history, a stale artifact a gate caught — record it in the handoff, with the commit SHA, and say what it cost. A reviewer who finds an error that the handoff already owns can trust the rest of it.
- **Never claim a check that was not run.** "Browser checks not performed" is a required section, not a formality, and it names the specific surfaces left unverified.
- **State the blocked action.** When a gate, a credential or a permission prevents completion — a workflow the PAT cannot install, a rehearsal that needs the live game — the handoff says what is pending, who has to do it, and what is unenforced until they do.
- **A measurement, not an absence.** "Zero violations" means nothing without the population scanned. Report both.
- **Do not widen a credential to make a handoff cleaner.** The blocked action goes in the handoff.

## 12. Independent review loop

ChatGPT reviews Fable's frozen Lane A SHA without modifying the Fable branch.

Fable applies accepted corrections on its own branch, reruns relevant gates, and returns a new exact SHA for verification.

Routine Lane B content is independently audited when the user/task requests it; it is not automatically blocked on a code-review ritual this file invented.

## 13. Scope discipline

Keep implementation changes narrow and explainable.

- Do not refactor unrelated code during a safety fix.
- Do not add abstractions merely because they are available.
- Prefer explicit state transitions and recoverable failure modes over cleverness.
- Mutation paths that can create ambiguous live state deserve stronger evidence/tests than operator-convenience features.
- Preserve the distinction between contract, live state, doctrine, generated evidence, and implementation.
- When a task is review-only, do not turn it into implementation work.
