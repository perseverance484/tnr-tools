# Forge Next — Content Project Workspace

**Status:** PRODUCT / UX DESIGN CONTRACT — PROPOSAL, NOT FINAL IA OR IMPLEMENTATION CONTRACT  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**TNR Tools baseline inspected:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Content Designer  
**Depends on:** `FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`, `FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md`, `FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md`, `FORGE_NEXT_VISUAL_DIRECTION.md`, `docs/workflows/CONTENT_WORKSTREAM.md`  
**Purpose:** define the architecture-neutral human workspace that can make Forge feel like one continuous content-development product while preserving the repository's current authority, evidence and production-safety model

---

## 1. Product decision this document proposes

Forge should treat a **content project** as the primary human unit of substantial content development.

A project is not a new database row that competes with TNR Tools. It is the human-facing projection of an existing repository workstream and the durable resources that workstream points to.

For an event, quest, mission arc, guide package or similarly substantial deliverable, the operator should be able to open one workspace and answer:

- What are we making and why?
- What has already been decided?
- What work is ready now?
- What is blocked, and by whom?
- Which content entities and assets belong to this project?
- What evidence supports reuse or mechanical decisions?
- What still requires Content Admin / director approval?
- Is the project mechanically valid?
- Is the content actually ready for review?
- What package will be delivered?
- Has anything touched production?
- Has that production result been read back and verified?
- Is the content still hidden/draft, or has it been published?

Today those answers are distributed across `roadmap.json`, plans, prose files, captures, art ledgers, manifests, result bundles and conversation handoffs. The repository structure is correct for authority and reproducibility, but the operator experience is fragmented.

The Content Project Workspace is the **control surface over those sources**, not their replacement.

---

## 2. Authority model

### 2.1 The project workspace is a projection

The workspace must preserve these owners:

- `state/workstreams/<slug>/roadmap.json` — coordination state: tasks, dependencies, blockers, evidence, open decisions, resume notes;
- doctrine / engine laws / generated contracts — rules and legal shapes they already own;
- task-specific plans / briefs / prose files — design intent and approved wording where they are the durable source;
- captures — fresh live-record evidence;
- answer/catalog files — cached searchable state, subordinate to fresher captures;
- art spec / production ledgers — asset constraints and production status;
- manifests / push packs — generated delivery artifacts;
- result bundles / harvests — execution and read-back evidence;
- live game — live records;
- user / Content Admin — reserved decisions, publishing and all live-game actions.

Forge may aggregate and edit a canonical source through a validated adapter, but it must not silently copy the same fact into a Forge-only state store and then treat the copy as authoritative.

### 2.2 One visible lifecycle does not mean one canonical status

The UI may show an understandable project journey such as:

> **Brief → Design → Research → Build Inputs → Review → Package → Execute → Verify → Publish**

That journey is a **derived presentation**. It does not replace the workstream task statuses:

- `PLANNED`
- `READY`
- `IN_PROGRESS`
- `BLOCKED`
- `REVIEW`
- `COMPLETE`
- `SKIPPED`
- `SUPERSEDED`

The lifecycle indicator should summarize where work concentrates and where gates remain; it must not create a second authoritative task state machine.

### 2.3 No project-wide green light from one signal

A project can be:

- mechanically valid but missing art;
- visually complete but awaiting a balance ruling;
- fully approved but not yet packaged;
- packaged but never executed;
- executed but incompletely verified;
- verified but still hidden;
- technically published but awaiting post-launch feedback.

Therefore Forge should expose **readiness dimensions**, not one generic `Ready` badge.

Recommended dimensions:

| Dimension | Example states |
| --- | --- |
| Design | incomplete / review / approved |
| Decisions | 3 open / resolved |
| Evidence | stale / sufficient / fresh |
| Assets | 2 missing / QC pending / accepted |
| Build | not compiled / blocked / valid |
| Review | not requested / in review / approved |
| Production | untouched / planned / sent / confirmed / verified |
| Publication | hidden/draft / publish-ready / published |

These are derived summaries. The underlying evidence remains inspectable.

---

## 3. Workspace anatomy

This section defines content obligations, not final route names or exact component geometry.

### 3.1 Project header

The header should establish, at a glance:

- project title;
- content type / project class;
- concise objective / player experience;
- overall workstream state;
- current attention state (`2 blocked`, `1 decision needed`, `verification incomplete`, etc.);
- last durable activity;
- project provenance / repository identity under advanced disclosure.

The project title, goal and current blocker should lead. The slug, branch, hashes and paths remain available but secondary.

### 3.2 Persistent readiness strip

Below or adjacent to the header, show the highest-value readiness dimensions:

- design;
- decisions;
- assets;
- build;
- review;
- production / verification;
- publication.

On mobile, this should collapse to the current stage plus the next blocking state, with the rest available in a horizontally swipeable or expandable detail that does not hide blockers.

### 3.3 `Needs attention`

This is the most important project-level block when non-empty.

It should aggregate actionable blockers without flattening unlike problems together.

Examples:

- **Director decision** — choose repeatability.
- **Missing durable input** — accepted icon bytes are not in the repository.
- **Evidence needed** — reuse candidate has only stale catalog data; fresh capture required.
- **Asset gate** — Road Bandit portrait awaiting acceptance.
- **Review gate** — Fable handoff awaiting independent SHA review.
- **Production ambiguity** — write confirmed but read-back incomplete.
- **Publication gate** — content verified but still hidden awaiting approval.

Each row should state:

1. what is blocked;
2. why;
3. who owns the next decision/action;
4. what downstream work is waiting;
5. the safest next action.

The workspace must not use a single notification count as the only representation of these states.

### 3.4 Work plan / task dependency surface

The roadmap already contains the right project model. Forge should visualize it in two complementary views.

#### Execution list

The default mobile-friendly view:

- task title;
- area (design, research, art, implementation, review, execution, etc.);
- status;
- owner;
- dependency/blocker summary;
- evidence count / completion anchor;
- `Open` / `Resume` action.

Recommended grouping:

- **Ready now**
- **In progress**
- **Blocked / decision needed**
- **Review**
- **Complete**

This grouping helps the operator act without mentally resolving the whole dependency graph.

#### Dependency map

A secondary desktop/tablet or full-screen mobile view showing:

- task dependencies;
- fan-out from decisions;
- implementation/review boundaries;
- execution/readback gates;
- blocked paths.

The graph is explanatory, not the only way to navigate. Mobile must never require precision drag/pan merely to open a task.

### 3.5 Open decisions workbench

User-owned and Content-Admin-owned decisions deserve a first-class project section.

For each open decision, show:

- decision question;
- owner;
- why it matters;
- verified evidence / comparisons available;
- options or proposal where one exists;
- downstream tasks blocked;
- whether the decision is reversible;
- canonical destination after approval.

If a compiler or task encounters `AWAITING_RULING`, Forge should route it here rather than presenting a default-looking editable field.

Resolved decisions should remain discoverable as history/provenance but stop competing with current work.

### 3.6 Content inventory

A project should show the human-facing content objects it will produce or reuse.

Possible categories:

- quest / mission / event;
- enemies / AI profiles;
- jutsu / items;
- scene assets;
- icons / avatars / backgrounds;
- guides;
- infographic / visual communication assets;
- existing live entities reused without mutation.

Each object should show a small set of meaningful states:

- new vs reused;
- design status;
- source/evidence provenance;
- asset requirement where applicable;
- build/wiring status;
- review state;
- live identity only once one legitimately exists.

Do not imply that every project entity is a live game record. A design-only concept, generated file and live record are different states.

### 3.7 Asset readiness

The project workspace should aggregate asset requirements generated by content design.

For each required asset:

- intended use / scene / entity;
- target class;
- exact filename contract if fixed;
- reuse vs new production;
- reference-selection status;
- generation status;
- raw QC;
- processing / composite QC;
- preflight;
- user acceptance;
- repository durability;
- wiring status.

The project workspace summarizes these states; the Art Studio owns the detailed production workflow.

A visually accepted image whose exact bytes are not durable must remain incomplete.

### 3.8 Evidence and reuse section

Evidence should be project-scoped without being copied out of its canonical source.

A useful card should communicate:

- claim / decision supported;
- evidence type (`source contract`, `fresh capture`, `catalog`, `approved ruling`, `generated validator result`);
- source path / capture / SHA;
- freshness where relevant;
- accepted/rejected reuse conclusion;
- what would invalidate the conclusion.

The interface should make evidence tier legible without forcing users to understand repository precedence from memory.

### 3.9 Review package

When a project reaches review, Forge should compose a human review surface from project sources.

It should answer:

- what player-facing content is being proposed;
- what changed since the previous approved state;
- what new records/assets are involved;
- what existing content is reused;
- what balance/admin decisions are already resolved;
- what remains explicitly unresolved;
- what validation/QC has run;
- what is being asked of the reviewer now.

Raw manifests should be available under advanced evidence, not be the primary review object.

### 3.10 Build / delivery package

A project may eventually produce one or more delivery artifacts. The workspace should show:

- package name;
- generated-from sources;
- included entities/assets;
- validation status;
- unresolved references;
- exact package hash / repository path under advanced detail;
- execution history;
- supersession state.

The UI should clearly mark an older artifact `SUPERSEDED` when a later package replaces it. A previously valid package must not continue to look like the recommended action after the project changes.

### 3.11 Production and verification timeline

Production is a separate project section because repository completeness is not proof of live state.

Show a chronological evidence trail:

- package prepared;
- user initiated live action;
- request sent / confirmed;
- read-back performed;
- verification result;
- result bundle persisted;
- any incomplete or ambiguous work;
- publication action and verification when applicable.

The timeline must preserve the distinction between:

- no live action;
- mutation request sent;
- server acknowledgement;
- read-back verified;
- repository result persisted;
- published.

A successful GitHub sync is not a successful game write, and a successful game write is not proof of publication.

---

## 4. Primary project actions

The workspace should not become a wall of buttons. Primary actions derive from state.

Examples:

| Current condition | Primary action |
| --- | --- |
| New project with incomplete brief | `Continue brief` |
| Ready design task exists | `Start next task` |
| Director decision blocks work | `Resolve decision` |
| Asset work is the next gate | `Open asset production` |
| Design complete, package absent | `Compile / prepare package` |
| Review requested | `Open review package` |
| Package approved, never run | `Open production preflight` |
| Write confirmed but unverified | `Verify again` |
| Ambiguous sent state | `Reconcile` |
| Verified and hidden awaiting approval | `Review publication readiness` |

There should rarely be more than one dominant next action at project level.

`Start live write` or `Publish` must never appear merely because the project is generally complete; those actions require their own consequence-aware preflight and user authorization.

---

## 5. Creating a project

### 5.1 Intake choices

A `New content` action may begin with a project class such as:

- mission / mission arc;
- event / story quest;
- combat encounter;
- guide;
- visual communication / infographic;
- asset-only work;
- another source-backed content family.

The final taxonomy remains a Fable/director decision.

### 5.2 Create from brief, not from blank technical state

The initial experience should ask human questions appropriate to the class and produce durable source files / roadmap tasks through validated adapters.

For event-like work, preserve the already-proven `blank / AI / NONE / [BALANCE]` semantics.

For mission work, select the applicable mission profile only when that choice is actually known. Do not invent a rank or profile simply to advance the wizard.

### 5.3 Project bootstrap result

After intake, the user should land in a workspace containing:

- objective;
- initial durable brief/source;
- initial task plan;
- explicit blockers/open decisions;
- expected content/asset classes;
- first executable task.

A project is not `READY` merely because the UI has enough data to render a page. Existing workstream validation rules still govern whether a task is executable from durable repository evidence.

---

## 6. Editing roadmap state from Forge

This is an implementation/architecture choice for Fable, but the UX contract is clear.

If Forge gains roadmap editing, it should behave as a structured editor over the canonical `roadmap.json` contract:

- validate task IDs and dependencies;
- reject nonexistent required resources;
- preserve `COMPLETE` evidence-anchor requirements;
- require a resume note for partial in-progress work where the workflow requires one;
- regenerate/check projections rather than hand-editing generated Markdown;
- show the repository change before committing/syncing when the edit materially changes the plan.

A Forge-only copy of the roadmap that later “syncs” opportunistically is a weaker model because it creates split-brain coordination state.

A lower-risk first release may therefore begin as a **read-only projection plus task launchers**, then add controlled roadmap writes once Fable proves the repository adapter and conflict model.

---

## 7. Desktop and mobile structure

### 7.1 Desktop / tablet

A strong candidate composition is:

- left application rail from the approved Forge shell;
- project identity + readiness header;
- main column for `Needs attention`, active task and project work;
- secondary column for decisions/readiness/evidence summaries;
- task plan and inventory below or in workspace tabs;
- contextual action area that remains visible without covering evidence.

Use width to keep independent context visible. Do not create a single infinitely tall phone column stretched across desktop.

### 7.2 Phone

Recommended reading order:

1. project title / state;
2. highest-priority attention item;
3. primary next action;
4. readiness summary;
5. ready/in-progress tasks;
6. decisions;
7. assets / content inventory;
8. review/build/production history;
9. advanced provenance.

The operator should not need a dependency graph to know what to do next.

Sticky UI should retain only the task identity/consequence and primary safe action. Avoid persistent multi-row chrome that consumes the small viewport.

---

## 8. Example: One Perfect Crop as a workspace

This is illustrative only; the existing roadmap remains authoritative.

The workspace could summarize:

### Header

`One Perfect Crop`  
Event · ACTIVE  
Goal: finish the frozen route/prose through art, implementation, review and verified Forge delivery.

### Needs attention

- Accepted Ittetsu / Waystation Keeper / quest-icon bytes are not durable in the repository.
- Road Bandit scene-character production is ready.
- Combat avatar production is ready.
- Content-admin decisions remain grouped in the existing decision packet.

### Work plan

- Structure — COMPLETE
- Prose — COMPLETE
- Asset probes — COMPLETE
- Road Bandit research — COMPLETE
- Combat AI/profile spec — COMPLETE
- Accepted art intake — BLOCKED
- Scene characters — READY
- Combat avatars — READY
- …later implementation/review/execution tasks remain dependency-gated

### Evidence

Fresh captures and durable resolution docs appear alongside the decisions they support rather than as an undifferentiated file list.

### Result

A new conversation/operator can understand the project without reading the predecessor transcript, which is exactly the existing workstream workflow's goal.

---

## 9. Quality-of-life capabilities that materially improve delivery

These are appropriate project-level enhancements because they reduce real failure modes rather than merely decorate the workspace.

### `Why is this blocked?`

Every blocked state should expand into a dependency chain in human language.

Example:

> Final package is blocked because `art.intake_accepted_assets` lacks durable bytes. Fable implementation does not need to start until those files are available because the final package filename contract depends on them.

### `What changed since review?`

When review must be repeated, show which durable project sources changed after the reviewed snapshot/SHA.

### `Show only my decisions`

Content Admin/director view filtering project state to unresolved user-owned decisions.

### `Show readiness gaps`

A concise checklist of everything preventing the next major gate (review, compile, execution, publication).

### `Open evidence`

One tap from a decision or reuse verdict to the capture/source that supports it.

### `Resume here`

For `IN_PROGRESS` tasks, surface the durable `resume_note` prominently so the next session starts at the actual boundary rather than reconstructing the conversation.

---

## 10. Safety constraints

The project workspace must preserve existing Forge/TNR production boundaries.

- Repository access is not live-game authorization.
- User remains the live-game actor.
- Everything built for game content follows hidden-first doctrine unless a separately source-backed content type has its own approved lifecycle.
- A push echo/server acknowledgement is not read-back verification.
- Publication is separate from technical write success.
- Ambiguous `SENT` work routes to reconciliation, never generic retry.
- Full-capture persistence and ordinary reads remain distinct.
- Balance/reward/art-direction/final-content decisions remain visibly user-owned.
- Workstream `COMPLETE` continues to require verifiable evidence anchors.

The one-stop-shop goal is fewer context switches, **not fewer safety distinctions**.

---

## 11. Proposed implementation slices for Fable to evaluate

This is sequencing guidance, not an implementation assignment.

### Slice 1 — Project reader

- discover repository workstreams;
- render objective/status/tasks/dependencies/blockers/open decisions/evidence;
- derive readiness dimensions;
- deep-link to existing Forge packages/captures where association is known;
- no roadmap writes.

This is low-risk and immediately useful.

### Slice 2 — Task launchers and durable source navigation

- launch the correct authoring/research/art/review surface from a task;
- show `required_resources` and upstream evidence in context;
- preserve resume notes;
- add project-scoped activity.

### Slice 3 — Controlled roadmap editing

- validated task/status/blocker/evidence updates;
- conflict/rebase strategy;
- generated projection checks;
- explicit repository change preview.

### Slice 4 — Integrated decision / asset / build readiness

- decision aggregation;
- generated shot/asset readiness;
- compile/validation results;
- review-package composition.

### Slice 5 — Production/readback/publication linkage

- associate execution jobs/result bundles with the project;
- show verification/publication timeline;
- keep live actions inside the existing consequence-aware Forge runner.

---

## 12. Acceptance scenarios

A final implementation should be able to demonstrate these without raw JSON as the normal path.

### Scenario A — resume a multi-session project

A user opens Forge after several days and can identify the next READY task, the blocker preventing the next downstream task, and the relevant resume note in under one minute.

### Scenario B — unresolved balance decision

A compiler/task exposes an unresolved user-owned value. The project shows a decision card and blocked dependents; the UI does not substitute a default.

### Scenario C — accepted but missing art bytes

An asset may be visually approved but not durable. The project remains blocked and explains exactly what is missing.

### Scenario D — package superseded

A previously validated package exists, but a later design/art change produced a replacement. The old package is visibly superseded and is not presented as the primary production action.

### Scenario E — verified live result, failed repo sync

The project shows game verification as successful while repository persistence/export remains failed/pending. These outcomes are not conflated.

### Scenario F — write acknowledgement without readback

The project shows `verification incomplete` and offers a read/reverify action rather than a resend.

### Scenario G — phone workflow

On a phone, the operator can see the top blocker and primary safe next action without opening a graph, scrolling through raw file lists or using hover interactions.

---

## 13. Explicit non-goals

This proposal does **not** authorize or require:

- a Forge-owned replacement for `roadmap.json`;
- storing canonical prose, balance rules or captures in a new Forge database;
- automatically converting the current Forsworn mission flatten into universal mission doctrine;
- automatic live-game execution;
- automatic publication;
- a final top-level navigation taxonomy;
- a final review-state persistence model;
- implementation on ChatGPT's branch.

Fable remains the normal implementation owner after the director approves a concrete roadmap/brief.

---

## 14. Open product decisions for later planning

These should remain visible rather than being silently settled by implementation order.

1. **Project creation scope:** which content classes receive full workstreams versus lightweight single-task packages?
2. **Roadmap mutation model:** read-only projection first, or repository-backed editing in the first project release?
3. **Review-state canonical owner:** existing roadmap/task state, a new repository contract, or source-backed game state where appropriate?
4. **Admin filtering:** whether Content Admin receives a dedicated project view or a role-filtered version of the same workspace.
5. **Project lifecycle vocabulary:** final human stage names and whether they appear as navigation, summary only, or both.
6. **Post-launch feedback:** when feedback becomes a formal workstream task versus an external note/reference.

None of these block using this document as the UX contract for the workspace's information obligations.
