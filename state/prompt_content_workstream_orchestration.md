# Implementation brief — repository-backed content workstreams

**Repository:** `perseverance484/tnr-tools`  
**Lane:** A — collaboration/workflow infrastructure  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Evidence baseline:** `main@70188b64d8b58053626d07e03bae6bfc4effa85d`  
**Implementation base:** branch from the live `main` head that contains this brief; verify it before starting.  
**Suggested branch:** `fable/content-workstreams`  
**Integration target:** `main` after independent review  
**Live-game policy:** zero live-game requests and zero game writes.

## Objective

Create a repository-backed **content workstream** system for TNR quests/events/mission-style content so one top-level planning conversation can establish the full project roadmap and durable resources, then later specialized sessions can initialize directly from the repository and work on a bounded task without depending on predecessor-chat memory.

The intended operator flow is:

1. dauntless starts a top-level content conversation (for example a new event or quest);
2. ChatGPT reconstructs the repository, develops the content/design roadmap with dauntless, and commits the roadmap plus durable supporting resources;
3. the roadmap groups related work into **session-sized tasks**, not one microtask per artifact;
4. a fresh future conversation can begin with a short request such as:  
   `Initialize session from repo. Workstream: One Perfect Crop. Task: scene characters.`
5. that session loads the roadmap, validates task readiness, reads only the task's routed resources plus required global authorities, and proceeds with aligned context;
6. when the task finishes or blocks, the session records evidence/status back into the workstream so downstream sessions see the current state;
7. Fable implementation/review/live-run tasks remain governed by their existing Lane A/Lane B and production-safety workflows.

This system must make the **repository the bridge between conversations**. It must not create a second source of content canon or a parallel replacement for `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, doctrine, engine laws, generated contracts, captures, art specs, Fable briefs, or live readback evidence.

## Design principles

### 1. Roadmap = coordination, not authority duplication

The workstream roadmap owns:

- task decomposition;
- task status;
- dependencies;
- task/session grouping;
- pointers to required resources;
- deliverables;
- completion gates;
- completion evidence;
- unresolved blockers/open user decisions;
- current safe next tasks.

It does **not** restate canonical quest mechanics, art contracts, doctrine, engine laws, generated schemas, or large prose/design documents. Those remain in their existing owners and the roadmap links to them.

### 2. A task is a session-sized packet

Do not model every individual image, node, or small artifact as a separate roadmap task.

Tasks should group work that benefits from one loaded context and one production mode. Examples:

- `design.structure` — route/quest architecture and branch logic;
- `prose.full_pass` — full player-facing prose and normalization;
- `research.live_probes` — a coherent set of read-only compatibility captures;
- `art.scene_characters` — all scene-character generation/QC for the workstream;
- `art.backgrounds` — all scene backgrounds;
- `art.combat_avatars` — enemy/AI avatars;
- `art.icons` — quest/item icons that share the same production mode;
- `admin.balance_and_rewards` — user-owned balance/reward/eligibility decisions;
- `build.final_freeze` — final implementation contract;
- `build.manifest` — Fable manifest implementation;
- `review.manifest` — exact-SHA independent review;
- `production.run_and_readback` — dauntless-only Forge execution plus readback verification.

Within an art task, still obey the art workflow's one-asset-at-a-time generation/QC rhythm. "One task" means one conversation/context, not batch generation.

### 3. New chats must be able to bootstrap from repo only

A task marked ready must not rely on hidden predecessor-chat context.

Required task resources must therefore be:

- committed repository paths; or
- explicitly labeled unresolved/external inputs that prevent the task from being marked READY.

A task may point to committed captures/results, generated contracts, task briefs, approved prose files, art indexes/reference packs, or other durable records. A previous chat attachment or sandbox-only file is **not** a durable resource.

### 4. User-owned decisions stay visible

Balance, rewards, rarity, publishing, final content/art direction, and live actions remain dauntless-owned. A task blocked on one of these must say so explicitly rather than inventing a value to make the roadmap green.

### 5. Existing Lane A/Lane B workflow remains intact

The workstream is an orchestration layer only.

- Routine content/design/art work may continue through the established Lane B/content workflow.
- Code/tooling changes and substantial Fable implementation still use Lane A branch ownership, exact-SHA handoff, independent review, and integration rules.
- `state/prompt_<task>.md` remains the normal substantial ChatGPT→Fable implementation contract where applicable; a roadmap task points to that brief after it exists.
- The user remains the only live-game actor.

## Repository layout

Add:

```text
state/workstreams/
  INDEX.md                         # generated human projection of all active workstreams
  <slug>/
    roadmap.json                   # canonical coordination source
    ROADMAP.md                     # generated human projection
```

Do not move existing canonical task/design files merely to satisfy the new layout. The pilot should reference existing One Perfect Crop files in place. Future workstreams may keep task-specific durable design/resources inside their workstream directory when that is clearer, but the roadmap remains pointers rather than a duplicate content database.

Add canonical workflow documentation:

```text
docs/workflows/CONTENT_WORKSTREAM.md
```

Add a small, stdlib-only orchestration tool:

```text
scripts/content_workstream.py
```

If a separate schema file materially improves validation, use:

```text
docs/workflows/CONTENT_WORKSTREAM.schema.json
```

Do not place this orchestration tool under an art/content skill merely to gain packaging. It is cross-surface repository workflow infrastructure and should not trigger skill ZIP rebuilds by itself.

## `roadmap.json` v1 contract

Use a small explicit versioned format. At minimum the workstream level must include:

- `version`;
- stable `slug`;
- human `title`;
- `content_type` (event / quest / mission / other supported descriptive value; this is coordination metadata, not an engine enum);
- overall `status`;
- concise `objective`;
- top-level `resources` (repository pointers that apply across many tasks);
- `tasks` array.

Each task must include at minimum:

- stable task `id`;
- `title`;
- `area`/kind (design, prose, research, art, admin, build, review, production, etc.);
- `status`;
- `owner` (dauntless / ChatGPT / Fable / shared as descriptive coordination metadata);
- `lead_role` when relevant (for example Content Designer, Image Production, Engineering Auditor);
- `depends_on` task IDs;
- concise `objective`;
- `scope` — what is included in this session-sized packet;
- `required_resources` — repository-relative paths with a short reason/authority label;
- `deliverables` — expected repository artifacts/results;
- `completion_gates`;
- `evidence` — empty until work is actually completed/verified;
- `blockers` / `open_decisions` when applicable;
- concise `resume_note` for incomplete/in-progress work when useful.

Recommended statuses:

- `PLANNED`
- `READY`
- `IN_PROGRESS`
- `BLOCKED`
- `REVIEW`
- `COMPLETE`
- `SKIPPED`
- `SUPERSEDED`

The validator may reject impossible combinations, for example:

- READY while a dependency is not COMPLETE/SKIPPED as allowed;
- COMPLETE with no completion evidence;
- BLOCKED with no blocker/open decision;
- duplicate task IDs;
- missing dependencies;
- dependency cycles;
- required repository resource paths missing for READY/IN_PROGRESS tasks;
- absolute filesystem paths or sandbox paths in durable resources.

Do not encode ephemeral branch heads as permanent authority. If an active implementation/review task needs a branch/SHA, record it as task evidence/state and update it as the workflow advances.

## `ROADMAP.md` and `INDEX.md`

`roadmap.json` is the editable coordination source. Markdown files are generated projections and must say so at the top.

`ROADMAP.md` should show, compactly:

- workstream title/objective/status;
- progress counts;
- task table in execution order with status, owner, dependencies, and one-line scope;
- open blockers/user decisions;
- READY tasks;
- recommended next task(s);
- completed evidence links where present.

`state/workstreams/INDEX.md` should scan every workstream and show:

- title/slug;
- overall status;
- progress;
- current READY/IN_PROGRESS task(s);
- blockers;
- link/path to its roadmap.

This is a content-workstream projection under existing `state/`, not a replacement for the global board/digest.

## CLI requirements

`scripts/content_workstream.py` should support deterministic, socket-free operations.

### `validate`

Examples:

```bash
python3 scripts/content_workstream.py validate state/workstreams/one_perfect_crop/roadmap.json
python3 scripts/content_workstream.py validate --all
```

Validate the v1 contract and cross-task/resource invariants described above.

### `render`

Examples:

```bash
python3 scripts/content_workstream.py render state/workstreams/one_perfect_crop/roadmap.json
python3 scripts/content_workstream.py render --all
```

Regenerate the per-workstream `ROADMAP.md` and global `INDEX.md` deterministically.

### `list` / `next`

Examples:

```bash
python3 scripts/content_workstream.py list
python3 scripts/content_workstream.py next one_perfect_crop
```

Show active workstreams and currently executable/blocked tasks.

### `init`

Primary operator/session feature:

```bash
python3 scripts/content_workstream.py init one_perfect_crop --task art.scene_characters
```

It should produce a concise **session initialization packet** on stdout containing:

- workstream and selected task;
- task status and dependency readiness;
- task objective/scope;
- owner/lead role;
- exact required repo resources to read, grouped in useful authority order;
- relevant completed upstream outputs/evidence;
- deliverables and completion gates;
- open blockers/user decisions;
- explicit reminder to verify live repository head/global authority files before substantive work;
- a stop/fail message if the task is not ready.

The packet is not a new committed authority; it is a deterministic view of the roadmap.

Support matching a workstream/task by stable slug/id. Friendly title matching may be added only if unambiguous and deterministic.

### `--selftest`

Add socket-free tests covering at least:

- valid roadmap;
- duplicate IDs;
- missing dependency;
- cycle detection;
- READY task with unfinished dependency;
- READY task with missing required repo resource;
- BLOCKED task without blocker;
- COMPLETE task without evidence;
- deterministic render;
- deterministic `init` output;
- all-path validation rejects sandbox/absolute paths.

Do not add a workflow that contacts ChatGPT, GitHub, or TNR automatically.

## Session initialization convention

Add the convention to `docs/workflows/CONTENT_WORKSTREAM.md` and route it from `CHATGPT.md` / `docs/00_INDEX.md` without bloating the project bootstrap.

When the user says something equivalent to:

> Initialize session from repo. Workstream: `<name>`. Task: `<task>`.

ChatGPT should:

1. verify live repository and `main` SHA;
2. read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, and relevant collaboration workflow/role files as normal;
3. read the selected workstream roadmap;
4. validate that the task is READY/IN_PROGRESS and its dependencies/resources are available;
5. read the task's `required_resources` and relevant completed upstream outputs/evidence;
6. state the task objective, completion gate, and any user-owned decisions still open;
7. work only that task unless new evidence requires a roadmap change;
8. at a durable stopping point, update the task status/evidence/resume note and regenerate roadmap projections.

A fresh session should not need the predecessor chat transcript if the workstream is healthy.

Fable should get the analogous rule in `CLAUDE.md`: when a handed-off implementation task references a workstream, load that task plus its required resources, while still treating an explicit `state/prompt_<task>.md` implementation brief as the build contract when one exists.

## Top-level planning-chat responsibilities

Document that the initial/top-level content conversation should, once enough requirements are known:

1. establish a concise durable content/design source (or point at existing committed source material);
2. enumerate the full expected workstream from design through readback;
3. group work into session-sized tasks by context/tooling affinity;
4. mark dependencies and user-owned decision gates;
5. commit all available durable resources/pointers;
6. mark tasks READY only when a future session can execute them from repo evidence alone;
7. render the roadmap;
8. keep the workstream updated when scope or sequencing changes.

This planning chat remains useful as a coordinator, but it is not a required memory source after the roadmap exists.

## Task granularity guidance

Make this explicit in the workflow because it is central to operator experience.

Prefer one task when all of the following are true:

- same production mode/tools;
- same reference set or nearby context;
- work can be completed coherently in one conversation;
- there is value in keeping visual/narrative consistency across outputs.

Split tasks when:

- a user decision gates the second half;
- different authority/source stacks are needed;
- a Lane A implementation/review boundary begins;
- mixing asset classes risks image-generation context contamination;
- the session would become too large to reconstruct/verify cleanly.

Examples:

- **Good:** all scene characters in one art session, generated/QC'd one at a time.
- **Good:** all AI avatars in a separate art session.
- **Bad:** one roadmap task per individual character portrait.
- **Bad:** icons and scene characters in one generation task when their visual/reference modes differ.

## Pilot migration — One Perfect Crop

Implement the generic system and migrate **One Perfect Crop** as the first workstream without changing its approved content.

Create:

```text
state/workstreams/one_perfect_crop/roadmap.json
state/workstreams/one_perfect_crop/ROADMAP.md
```

The pilot must point to existing durable files rather than copying their text, including where relevant:

- `state/plan_one_perfect_crop_finish.md`
- `state/one_perfect_crop_prose_graph.md`
- `state/one_perfect_crop_bandit_resolution.md`
- `state/one_perfect_crop_content_admin_open.md`
- the successful committed Forge 0.4.0 bandit probe result/capture evidence;
- `skills/building-tnr-content/references/event.md`
- `skills/building-tnr-content/references/quest.md`
- `skills/building-tnr-content/references/ai.md`
- `skills/producing-tnr-art/SKILL.md`
- the TNR art reference-pack files **if that separate task has been integrated by implementation time**.

Do not invent that a prior chat attachment is a durable resource. If Ittetsu/Waystation Keeper/other accepted art bytes are not actually committed, the roadmap must say so and either:

- include their repository-materialization inside the relevant scene-character task; or
- mark the task/blocker accurately until those bytes are supplied.

### Pilot task shape

Use roughly this session grouping, adjusting IDs/names only for a cleaner implementation without changing intent:

| Task | Initial status intent | Scope |
| --- | --- | --- |
| `design.structure` | COMPLETE | approved route/cast/encounter architecture |
| `prose.final` | COMPLETE | normalized approved player-facing prose/graph |
| `research.bandit_ai` | COMPLETE | Forge protected-read repair outcome + Road Bandit reuse rejection/new-AI decision |
| `art.scene_characters` | READY or BLOCKED only if required durable inputs are missing | Ittetsu + Waystation Keeper production intake/ledger, Market Clerk reuse verification, new Road Bandit SCENE_CHARACTER; one conversation, one asset at a time |
| `art.backgrounds` | READY | final reuse/new decisions and any required production backgrounds |
| `art.combat_avatars` | READY | Road Bandit AI avatar + Harvest Boar avatar |
| `art.icons` | READY | approved quest icon production/QC plus Cabbage Seed item icon |
| `admin.balance_and_eligibility` | BLOCKED / user-owned | rewards, seed rarity/economics/type, repeatability, eligibility substitute/removal |
| `build.final_freeze` | PLANNED | freeze `state/prompt_one_perfect_crop.md`; depends on art/admin/combat inputs |
| `build.manifest` | PLANNED | Fable implementation from frozen brief |
| `review.manifest` | PLANNED | ChatGPT exact-SHA audit |
| `production.run_and_readback` | PLANNED | dauntless Forge execution + fresh readback; publishing remains separate |

The pilot roadmap must reflect the already-resolved Road Bandit decision: create a **new** Road Bandit AI/profile; do not edit shared live AI.

The pilot is a migration/coordination exercise only. Do not alter One Perfect Crop's frozen route/prose/combat rulings as part of this tooling task.

## Interaction with the TNR art reference-pack task

A separate brief exists at `state/prompt_tnr_art_reference_pack.md`.

This workstream task should not reimplement that system. If the reference-pack work has integrated first, One Perfect Crop art tasks should point to its selector/index as a required resource. If it has not integrated yet, record it as an external tooling dependency/blocker rather than copying its planned contract.

Prefer implementing this workstream task **after** the reference-pack task is integrated, because the pilot's first intended fresh session is `art.scene_characters` and should benefit from the new durable visual refs.

## Workflow/documentation changes

At minimum update/reroute:

- `docs/workflows/CONTENT_WORKSTREAM.md` — new canonical workflow;
- `docs/00_INDEX.md` — route content-workstream initialization and tooling;
- `CHATGPT.md` — recognize workstream/task initialization and repository-backed cross-chat continuation;
- `CLAUDE.md` — workstream-aware implementation bootstrap while preserving explicit Fable brief authority;
- `docs/agents/PROJECT_INSTRUCTIONS.md` only if a minimal pointer is genuinely needed; keep the project bootstrap short;
- `docs/workflows/ART_PRODUCTION.md` should **not** need substantive changes for this task; art tasks simply route to it. Avoid conflicting with the separate reference-pack task.

Do not alter doctrine/engine laws for this orchestration feature.

## Ruling history

After the implementation shape is accepted by dauntless, append a durable ruling to `docs/RULINGS.md` recording that substantial TNR content work uses repository-backed workstreams/top-level planning + session-sized task continuation. The operative workflow belongs to `docs/workflows/CONTENT_WORKSTREAM.md`; the ruling ledger preserves the decision history only.

Do not write the ruling as if the tooling existed before this implementation is reviewed/integrated.

## Completion semantics

A task is COMPLETE only when its declared completion gates are satisfied and evidence is recorded. Conversation claims alone are not evidence.

Useful evidence can include:

- user approval recorded in a committed decision/design file;
- committed art ledger/preflight outputs;
- committed capture/result file;
- exact implementation/review SHA;
- validator result recorded in handoff;
- readback capture path.

`COMPLETE` should mean downstream sessions can safely rely on the task outcome from repository evidence.

If a conversation stops partway through a task, set it to `IN_PROGRESS` or `BLOCKED` with `resume_note` and current durable outputs. Do not mark partial work COMPLETE merely to advance the roadmap.

## Explicit non-goals

Do not in this task:

- build a web project-management UI;
- create an external database/service;
- require ChatGPT conversation IDs or transcripts;
- automatically call ChatGPT/Fable/image generation;
- automatically make game requests;
- replace the global `state/digest.json` / active-context/status system;
- replace `state/prompt_<task>.md` Fable implementation briefs;
- duplicate full quest/prose/art/source documents into roadmap JSON;
- move every historical content file into the new layout;
- rewrite One Perfect Crop content decisions;
- turn every asset into a separate roadmap task;
- introduce a `develop` branch or alter repository topology.

## Acceptance criteria

The implementation is acceptable when:

1. A validated v1 workstream format exists and clearly separates coordination state from canonical content/source authority.
2. `content_workstream.py --selftest` passes with the required graph/status/resource failure fixtures.
3. `validate --all` exits 0 on checked-in workstreams.
4. `render --all` is deterministic and produces a useful One Perfect Crop ROADMAP plus global INDEX.
5. `init one_perfect_crop --task art.scene_characters` prints a bounded session packet with correct dependencies/resources/completion gates and does not require predecessor-chat context.
6. A non-ready task fails/halts initialization with an actionable explanation.
7. One Perfect Crop's existing completed design/prose/bandit work is represented as COMPLETE with repository evidence, not duplicated prose.
8. Remaining One Perfect Crop work is grouped into smooth session-sized tasks as described above.
9. Missing non-repository resources are surfaced honestly rather than assumed durable.
10. The workflow docs instruct ChatGPT to update task status/evidence at durable stopping points.
11. Fable implementation tasks still defer to explicit `state/prompt_<task>.md` build contracts and exact-SHA review.
12. No live-game request/write occurs.
13. No doctrine/engine-law/generated-contract authority is displaced.
14. Existing repository/session coherence gates remain green.

## Required verification before Fable handoff

Run and report exact results for at least:

```bash
python3 scripts/content_workstream.py --selftest
python3 scripts/content_workstream.py validate --all
python3 scripts/content_workstream.py render --all
python3 scripts/content_workstream.py next one_perfect_crop
python3 scripts/content_workstream.py init one_perfect_crop --task art.scene_characters
python3 scripts/content_workstream.py init one_perfect_crop --task build.manifest
python3 skills/building-tnr-content/scripts/doctrinemap.py
python3 skills/building-tnr-content/scripts/render_doctrine.py --check
python3 skills/building-tnr-content/scripts/build_packs.py --check
git diff --check
```

The `build.manifest` init call should demonstrate that a not-yet-ready downstream task is refused or clearly reported as blocked by dependencies.

If the reference-pack task was integrated before this implementation begins, also verify the One Perfect Crop scene-character task points to the integrated reference selector/index rather than a stale planning brief.

## Handoff

Use `docs/workflows/IMPLEMENTATION_HANDOFF.md` and return:

- repository;
- branch;
- exact base SHA;
- exact frozen head SHA;
- changed files;
- CLI/test/gate results;
- One Perfect Crop pilot roadmap summary;
- any migration deviations;
- whether the art reference-pack dependency was integrated or still external;
- open user decisions;
- live requests/writes/credentials used: expected `none`;
- what explicitly has not begun.

Freeze the exact head for independent ChatGPT review.