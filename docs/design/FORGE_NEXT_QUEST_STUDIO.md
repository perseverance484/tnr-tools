# Forge Next — Unified Quest Studio

**Status:** USER-DIRECTED PRODUCT CONTRACT — PROPOSAL FOR ARCHITECTURE / IMPLEMENTATION PLANNING  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**TNR Tools baseline inspected:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Game-source head inspected:** `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Content Designer, Engineering Auditor  
**Supersedes product scope of:** `FORGE_NEXT_MISSION_STUDIO.md` (mission-specific details remain useful as the Mission subtype contract)  
**Purpose:** define a single Forge Quest Studio that authors all supported quest families through subtype-specific policy/build adapters and can invoke the repository's canonical scripts without requiring a chat/agent relay between authoring and build

---

## 1. Director decision

Forge should not expose a standalone Mission Studio as the top-level quest-authoring product.

The product surface is **Quest Studio**. The operator begins a quest and selects a human-facing subtype / recipe such as Mission, Event, Story, Raid/Boss, Battle Pyramid, Daily, or another supported quest family. Mission authoring becomes one policy adapter inside this larger Studio.

The long-term target is that any quest class intentionally supported by TNR content operations can be designed, compiled, validated, packaged and handed directly to Forge's existing execution/reconciliation system from this one interface.

The desired experience is:

> **New Quest → choose subtype → author in human language → design flow/encounters/scenes → resolve required decisions → Compile → canonical repo toolchain runs → results return to Forge → review/package → explicit live execution when the user chooses**

Routine deterministic transformations should require **no ChatGPT/Fable relay and no manual copy/paste between files**.

This does not remove real human decisions. Balance, rewards, rarity, final content direction, art direction/acceptance, publishing and live-game action remain user-owned. Where the repository currently refuses to guess, Quest Studio should surface a decision card instead of inventing a default.

---

## 2. Feasibility conclusion

This design is **highly plausible**.

The game already uses one shared quest record/objective engine across story missions, repeatable missions, timed events and battlepyramid content. Current source exposes 19 quest-type enum values, while the repository quest reference already treats the objective graph as the shared mechanical substrate.

The hard part is not building a common editor. The hard part is giving that browser editor a trustworthy way to run the repository's Python compilers/validators without duplicating those rules in JavaScript.

Current Forge is an ES-module browser/userscript application bundled for Firefox. It can read/write repository files through the GitHub API and execute manifests against TNR, but it is not a Python host. Therefore the recommended architecture is:

> **browser Quest Studio + repository-backed canonical build worker + existing Forge runner**

Do not make a JavaScript rewrite of every Python content tool the authoritative compiler.

---

## 3. Quest Studio must separate authoring subtype from engine `questType`

The operator-facing subtype and the game's stored `questType` are related but should not be assumed to be one-to-one.

Current game source supports:

`starter`, `tier`, `daily`, `mission`, `errand`, `crime`, `exam`, `event`, `story`, `anbu`, `medical`, `hunting`, `gathering`, `battlepyramid`, `pvp`, `achievement`, `war`, `raid`, `overworld`.

However, the existing event build contract proves that an **Event** in human terms can map to several engine shapes:

- chain of fights climbing to boss → `battlepyramid`;
- story event → generic/story-style quest structure;
- short repeatable reward loop → `questType: event`;
- one boss encounter → `questType: raid`.

Therefore Quest Studio should model two related concepts:

### Authoring recipe / product subtype

What the creator thinks they are making: Mission, Event, Story, Raid/Boss, Daily, etc.

This chooses the intake questions, policy source, allowed design patterns, previews and compiler adapter.

### Resolved engine type

The actual `questType` and objective structure emitted by the compiler.

Forge should show the resolved engine type in policy/technical detail, but the content creator should not need to choose raw enum values merely to start designing.

---

## 4. The shared Quest Studio core

Every subtype should inherit a common editor shell.

### Overview / brief

Human-facing intent:

- title and one-line player experience;
- premise;
- success/failure meaning;
- audience/eligibility intent;
- tone/cast;
- reuse requirements;
- off-limits material;
- project/workstream association.

### Storyboard

Readable node-by-node authoring rather than raw objective JSON.

### Semantic flow

Shared directed graph with explicit start, success/failure/reset edges, choices, endings, reachability and engine-aware node meaning.

### Encounter layer

Reuse/new enemy decisions, composition, behavior intent and references to Encounter/AI Studio.

### Scene/assets layer

Background/character/pin requirements derived from the graph and linked to the art workflow.

### Policy/eligibility/rewards

Subtype-specific inherited values, fixed doctrine values, user-owned decisions and unresolved rulings.

### Research/reuse

Source/capture/catalog evidence for existing quest/AI/jutsu/item/asset reuse.

### Preview

Route playback, scene/dialog preview, structural metrics and human-readable revision diff.

### Compile / build

Canonical repository execution and machine-readable results.

### Review / package

Human review packet leading into the existing consequence-aware Forge execution runner.

The subtype should change the **policy and recipe**, not force the user into an unrelated application.

---

## 5. Subtype adapter registry

Quest Studio needs a declarative subtype registry rather than subtype behavior scattered through UI components.

A registry entry should identify at least:

- stable subtype id and display label;
- supported engine quest type(s);
- intake/source schema;
- policy/profile source;
- compiler adapter;
- required repository resources;
- subtype-specific structural rules;
- allowed/recommended objective intents;
- decision classes that may block compilation;
- art/scene requirements;
- preview capabilities;
- validation/build commands;
- support maturity (`supported`, `experimental`, `read-only/system-managed`, `needs recipe` or equivalent).

The UI reads the registry to configure itself. The compiler reads the same registry or a generated sibling contract. Do not maintain one subtype matrix in the browser and another independently in Python.

### Initial adapter examples

**Mission** — wraps the existing `mission.py`, `48_DATA_mission_profiles.json`, storyboard philosophy, enemy generation and generated shot-list behavior.

**Event** — turns the current `EVENT_SHEET.md` / `26x_EVENT_sheet_schema.json` / `references/event.md` procedure into an executable compiler adapter. This is new tooling: today the event contract describes a build sequence, but there is no single event compiler equivalent to `mission.py`.

**Story** — shared quest-graph compiler plus story-specific eligibility/attempt/pacing policy and preview defaults.

**Raid/Boss** — raid-specific one-objective rules, boss-health requirements and raid objective vocabulary.

**Battle Pyramid** — battlepyramid-specific battle semantics and floor/reset sequencing.

**Daily** — shared graph compiler with the source-verified 3–7 objective constraint and daily policy.

Additional engine types can join as their source semantics and content recipes are audited. “Any quest type” is the intended architecture, not permission to expose a type before its adapter is truthful.

---

## 6. Introduce a canonical authored Quest Source

The Studio needs a structured source artifact above the generated manifest.

Call it `Quest Source` here; final filename/schema naming is Fable's architecture decision.

It should contain **authoring intent**, not a second copy of the final server record. Candidate sections:

- schema/version;
- subtype / recipe;
- project identity;
- brief and prose;
- semantic objectives/edges;
- encounters and reuse intent;
- scene/art intent;
- policy/profile selection;
- decision slots / approved overrides;
- references/evidence pointers;
- build metadata.

Subtype adapters compile that source into whatever intermediate inputs existing tools expect.

For Mission, the adapter can emit/consume the existing mission design-sheet contract rather than rewriting `mission.py`.

For Event, the adapter can emit the machine-parseable event-sheet representation and then run a new deterministic event compiler/orchestrator.

### Authority rule

Quest Source is the editable creative source. Generated manifest/push pack is a build artifact. Live record is live state. Captures are evidence. Do not make any one of those pretend to be all four.

---

## 7. Why Forge cannot simply run the Python scripts in its current browser process

Current Forge is bundled by esbuild as a browser IIFE and targets Firefox. Its runtime graph uses browser `window`, `localStorage`, IndexedDB and `fetch`; its npm runtime dependency is only `superjson`.

The canonical TNR content tools are Python programs with filesystem/import/subprocess assumptions. `mission.py` imports other repository tools and the art skill; `pushpack.py` shells out to `validate.py`; factories load generated data from the repository filesystem.

Trying to execute all of that through Pyodide/WASM in the userscript is technically possible in principle but is the wrong first architecture:

- large mobile/browser payload;
- virtual-filesystem hydration of repository data;
- Python import/path assumptions;
- subprocess incompatibility/refactors;
- Pillow/art-pipeline complications;
- Android memory/performance cost;
- another environment to debug;
- temptation to maintain browser-only forks of the content tools.

A desktop/local helper is also a poor primary solution because the actual operator workflow is mobile/browser-first.

---

## 8. Recommended canonical build architecture: repository worker

Forge should treat the repository as a **build service boundary**.

### 8.1 Local authoring

Quest Studio keeps the current draft responsive in browser storage and performs fast client-side checks that can be safely derived from bundled/source-generated contracts.

These checks improve editing UX but are not the canonical compile result.

### 8.2 Save build input to a project branch/path

On `Compile`, Forge serializes the Quest Source and commits it to a dedicated repository work branch or another deliberately designed non-production source location.

Do not commit every keystroke to `main`.

The content project should have a stable branch/source identity so revisions are inspectable and resumable.

### 8.3 Trigger a trusted repository build

Preferred V1 approach: a GitHub Actions worker triggered by the Quest Source change or explicitly dispatched by Forge.

The worker must run **trusted compiler code from a pinned/main repository revision**, not arbitrary scripts from the authored content branch. A safe worker can check out canonical tooling separately and ingest only the Quest Source/data file from the project branch.

This prevents a content draft from changing the workflow/compiler code that executes with repository write permissions.

### 8.4 General quest orchestrator

Add one canonical entry point, conceptually:

`quest_compile.py <quest-source> --out <build-dir>`

It should be an orchestrator, not a rewrite of all domain logic.

It resolves the subtype adapter and delegates to existing tools:

- `mission.py` for mission policy/build;
- `factory.py` for generated legal structures;
- `enemy.py` / other content factories as required;
- art `shotlist.py` for graph-derived requirements;
- `validate.py` as the mandatory manifest gate;
- `pushpack.py` when all required production files are present;
- future subtype-specific adapters for event/story/raid/etc.

### 8.5 Standard machine-readable build report

Every adapter should return the same result envelope, for example conceptually:

- `status`: `valid | blocked | failed`;
- subtype and resolved engine `questType`;
- canonical source SHA/version;
- decisions required;
- hard errors;
- warnings/advisories;
- generated entities;
- generated manifest path/hash;
- art/asset requirements and missing files;
- validation result;
- package readiness;
- compiler/tool SHAs/versions.

Forge polls/reads that result and renders it natively.

### 8.6 Build outputs return to Quest Studio

The operator sees:

- mechanically valid / blocked;
- exactly what is missing;
- generated encounter/assets/entities;
- preview changes;
- manifest/package readiness;
- technical detail only when wanted.

There is no “download this JSON, send it to chat, copy the answer back” step.

### 8.7 Handoff directly to existing Forge runner

When the build is valid, Quest Studio can load the generated manifest directly into the existing Forge planning/runner path.

The user then receives the normal live consequence preflight and explicitly starts the live operation.

The build service must **never** turn `Compile` into a live-game write.

---

## 9. Trigger strategy

There are two reasonable GitHub-worker trigger models.

### A. Source-push trigger — recommended first

Forge writes `quest-source` on a dedicated branch/path. A workflow listening only to that source path starts automatically.

Advantages:

- uses repository-content write capability rather than requiring a second workflow-dispatch permission in the browser;
- compilation feels automatic after Save/Compile;
- generated-output commits can be excluded from the trigger path to avoid loops.

The workflow can write `build-report.json` and generated text artifacts back to the project branch or another known output branch/path that Forge polls through the Contents API.

### B. `workflow_dispatch`

Forge writes the source and then calls a workflow with branch/path identifiers.

Advantages: explicit build request and simpler job correlation. Cost: Forge's GitHub credential needs the appropriate Actions permission and the GitHub client needs workflow/run APIs.

The repository already has a `workflow_dispatch` relay pattern, so this is operationally familiar, but the source-push trigger is the smaller initial browser-permission expansion.

Fable should choose after auditing the current GitHub credential model and branch/write policy.

---

## 10. “No back and forth” contract

Quest Studio should eliminate **mechanical relay**, not human judgment.

A normal build should need no external conversation when:

- every required creative input is present;
- existing policy/profile resolves deterministic values;
- reuse choices are settled;
- required balance/admin/art decisions are already approved;
- required asset bytes are available when packaging requires them.

If something cannot be determined lawfully, the worker returns a structured blocker and Quest Studio places it in the appropriate editing/decision surface.

Example:

> `Enemy level requires director decision: allowed profile band 60–70; no approved exact level.`

The user resolves it in Forge; Compile runs again automatically. There is still no chat/file relay.

A future AI-assistance layer could propose prose, structure, enemies or choices inside the Studio, but it must remain subordinate to the same decision/compile gates. AI integration is not required to achieve the one-stop deterministic workflow.

---

## 11. Quest-type support should expand by adapter maturity

Do not block Quest Studio until all 19 engine types have bespoke authoring recipes.

Recommended sequencing:

### Foundation

Shared Quest Source, storyboard, semantic graph, local structural checks, subtype registry, repository build worker and result envelope.

### First production adapters

Mission first because a real compiler/profile pipeline already exists; Event next because the staff intake + build contract already describe the necessary transformation but need to be made executable; then Story/Raid/Battle Pyramid where the shared quest reference has strong mechanics.

### Generic/simple adapters

Daily and other types whose differences can be expressed mostly through shared quest compilation plus policy constraints.

### Specialized/system-linked adapters

Tier, profession, PvP, War, Overworld, Exam, Achievement, ANBU and other types only after their creation/edit semantics, permissions, player-facing role and required supporting systems are source-audited.

Quest Studio can still show unsupported engine types in an expert capability matrix without pretending they are ready to author.

---

## 12. Mobile interaction model

The repository worker is especially compatible with the Android-first workflow because the phone does not do heavy compilation itself.

On phone, Quest Studio should primarily use:

- Brief;
- Storyboard;
- focused node editor;
- Choices/Route controls;
- Encounter cards;
- Decisions;
- Assets;
- Preview;
- Compile status.

The full graph may open as a focused pan/zoom view, but precise drag wiring cannot be the only way to edit routes.

Compilation can continue remotely while the UI displays `Building…`; when the build report lands, Forge refreshes the current Studio state.

---

## 13. Safety and provenance requirements

The integrated workflow must preserve:

- exact repository/compiler SHA in every build result;
- Quest Source revision/hash used to compile;
- generated manifest hash;
- validation result;
- distinction between advisory client lints and canonical repository validation;
- hidden-first content policy;
- user-owned live execution;
- user-owned publishing;
- existing Forge journal / `SENT` reconciliation / readback semantics;
- source/capture/catalog provenance on reuse decisions;
- no automatic substitution for unresolved balance/reward/art/final-content decisions.

A one-click content studio that hides these distinctions would be less safe than today's file workflow even if it were more convenient.

---

## 14. Relationship to the earlier Mission Studio document

`FORGE_NEXT_MISSION_STUDIO.md` remains useful for detailed Mission-subtype UX: mission profiles, storyboard behavior, inherited policy, Forsworn-experiment guardrails and mission acceptance scenarios.

Its open question “mission-specific Studio first, or shared quest core?” is now resolved by director decision:

> **Shared Quest Studio core with subtype policy/compiler adapters.**

Future wireframes and implementation planning should use Quest Studio as the parent product and treat Mission as one subtype.

---

## 15. Minimum architecture proof before full UI investment

Fable should prove the end-to-end seam with one narrow vertical slice before building a large editor:

1. Forge creates a minimal Mission Quest Source without raw JSON.
2. Source is committed to a project branch/path.
3. Repository worker runs trusted canonical tooling.
4. `mission.py` / validators produce a manifest and machine-readable build report.
5. Forge observes the result without manual refresh/download/upload steps.
6. A changed prose field produces a new traceable build.
7. An `AWAITING_RULING`/missing decision returns a structured blocker instead of a guessed value.
8. A valid output can be opened directly in existing Forge preflight.
9. Nothing contacts the live game until the operator explicitly starts the existing Forge run.

If that seam works cleanly on Android, scaling the same architecture to Event/Story/Raid is principally adapter work rather than another product rewrite.

---

## 16. Architecture risks to resolve in Fable planning

- project-branch/source lifecycle and cleanup;
- GitHub authentication/least-privilege model for browser-originated source writes and build observation;
- build-trigger choice (push vs dispatch);
- canonical Quest Source schema/versioning;
- how workflow outputs are persisted without making generated files canonical creative sources;
- conflict handling when repository main/compiler advances while a quest draft is open;
- exact adapter boundary between shared quest compiler and subtype logic;
- how art files enter packaging while the standing manual-art-submission ruling remains in force;
- whether build artifacts stay in work branches until review or are promoted to normal `push/` only at an explicit package gate;
- how project/workstream state references a Quest Studio draft/build without duplicating it.

These are engineering decisions for Fable's planning package. They do not undermine the product concept; they are the implementation work needed to make it safe and reproducible.