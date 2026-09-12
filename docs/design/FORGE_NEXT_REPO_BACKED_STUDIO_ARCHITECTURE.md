# Forge Next — Repository-Backed Studio Architecture

**Status:** USER-DIRECTED PRODUCT / ARCHITECTURE CONTRACT FOR PLANNING  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Applies to:** Forge Next content authoring, especially Quest Studio and later domain studios  
**Lead lens:** UI/UX Reviewer  
**Supporting lenses:** Engineering Auditor, Content Designer  
**Purpose:** define the product boundary between Forge as the operator-facing translation/orchestration layer and `tnr-tools` as the durable source of facts, contracts, scripts, evidence and generated outputs

---

## 1. Director direction

Forge should be the place where the operator **does the work**.

The repository should remain the place where the system **knows how the work is defined, validated, compiled, evidenced and preserved**.

The target relationship is:

> **Human intent in Forge → structured repository request/source → canonical repository facts and scripts → machine-readable result → human explanation/action in Forge**

The user should not need to leave Forge to design a Mission, Story Quest, Battle Pyramid, Event, Raid/Boss quest or other supported content type merely because the authoritative profile, validator, compiler, generated contract or reference lives in the repository.

Forge therefore acts as a **translation, orchestration and presentation layer**, not a second source of truth.

---

## 2. Product principle

A normal content session should be able to remain inside one Forge workspace from idea through build readiness.

For Quest Studio that means one continuous product can cover:

1. choose a human-facing quest subtype/recipe;
2. capture the brief and player experience;
3. author prose/storyboard;
4. design objective flow and branches;
5. design/reuse encounters;
6. attach scene/art intent;
7. inspect inherited policy and source-backed facts;
8. resolve user-owned decisions;
9. compile through the repository toolchain;
10. review generated outputs and validation;
11. prepare the package;
12. explicitly execute against the live game when the operator chooses;
13. inspect verification/readback/publication state.

The operator should not need separate Mission/Event/Battle-Pyramid forms that each require different manual file workflows. Subtype differences belong in adapters and policy, while the surrounding Studio experience remains coherent.

---

## 3. Authority boundary

### Forge owns the human interaction

Forge should own presentation and interaction such as:

- human-language forms and editors;
- storyboard and semantic graph views;
- route/encounter/asset previews;
- decision cards;
- progress and build status;
- review/readiness summaries;
- repository evidence rendered in context;
- consequence-aware live-operation controls;
- mobile/desktop interaction behavior;
- explanation of repository/compiler results in operator language.

### Repository owns durable knowledge and execution logic

The repository should continue to own, where it owns them today:

- doctrine and engine-law text;
- generated contracts and schemas;
- quest/objective mechanics references;
- mission profiles and subtype policy sources;
- content workstreams and durable project state;
- compiler/factory scripts;
- validators and lints;
- art specifications and production tooling;
- captures/catalogs/evidence;
- generated manifests, build reports and packages;
- implementation tests;
- provenance and exact SHAs.

Forge may cache/project these things for UX. A cache or bundled projection is never the new canonical owner merely because it is easier to render.

---

## 4. Forge does not need all facts embedded in its code

The redesign should deliberately avoid turning Forge into a hand-maintained encyclopedia of TNR rules.

Bad pattern:

> Python/reference says one thing → UI JavaScript independently hard-codes the same thing → one side eventually drifts.

Preferred pattern:

> Repository owns the fact → a generated/read adapter exposes it → Forge renders it with provenance.

Examples:

- quest subtype availability comes from a repository subtype registry or generated projection;
- objective vocabulary/field legality comes from generated source contracts;
- Mission rank policy comes from mission profiles;
- current art target requirements come from the art spec;
- build blockers come from the canonical compiler/validator;
- reusable live/content evidence points to the capture/catalog/source that supports it.

Forge may bundle generated snapshots for fast startup and offline-ish responsiveness, but every such snapshot should identify the repository/source SHA it represents and be refreshable/rebuildable from the canonical source.

---

## 5. Two-speed interaction model

A seamless UI should not make every keystroke wait for GitHub or a remote compiler.

### Fast local interaction

Use browser-side state/generated contracts for:

- editing prose;
- arranging storyboard nodes;
- simple required-field checks;
- obvious dangling-edge/reachability checks when safely shared/generated;
- displaying already-fetched profiles/contracts;
- previewing routes/scenes;
- marking draft changes.

These are **editing aids**, not final authority.

### Canonical repository operations

Use the repository worker/source adapters for:

- resolving subtype policy;
- running canonical Python compilers/factories;
- source-backed validation/lints;
- generating enemies/art requirements/manifests/packages;
- checking values that depend on repository evidence;
- producing durable revision/build outputs;
- recording provenance.

The operator experiences both as one Studio. The implementation boundary should not become a context switch.

---

## 6. Request/response model

Forge needs a small, stable orchestration contract with the repository rather than bespoke GitHub behavior embedded in every screen.

Conceptually, Forge sends requests such as:

- `load project/source`;
- `load subtype registry/policy`;
- `save draft revision`;
- `compile quest source`;
- `validate package`;
- `search/reuse evidence`;
- `generate artifact requirements`;
- `fetch build result`;
- `open generated manifest`.

The repository side returns machine-readable envelopes that include:

- status;
- source revision/SHA;
- compiler/tool revision/SHA;
- requested operation;
- result data;
- blockers;
- warnings/advisories;
- generated artifact pointers/hashes;
- provenance/evidence pointers;
- next legal actions.

Forge translates that into the appropriate human surface.

The exact transport may initially be GitHub Contents + Actions and later become a thinner purpose-built service if that materially improves latency/security. The product contract should depend on the **request/result semantics**, not on a particular transport provider.

---

## 7. Repository execution boundary

The browser should not receive permission to execute arbitrary repository code.

A build request should choose from approved operations/adapters, for example:

- compile Mission;
- compile Event;
- compile generic Story quest;
- validate quest source;
- generate shot list;
- build push package.

The worker executes trusted, reviewed code from a pinned/canonical tool revision against the authored source revision.

This protects the one-stop UX from turning into a remote-shell architecture and keeps security/reproducibility understandable.

---

## 8. Quest Studio consequence

Quest Studio is one UI shell with subtype-driven behavior.

Opening **New Quest** should allow selecting a recipe such as:

- Mission;
- Story Quest;
- Battle Pyramid;
- Event;
- Raid/Boss;
- Daily;
- later audited quest families.

After selection, the same workspace adapts:

- intake questions;
- allowed/recommended structure;
- inherited policy;
- specialized node/encounter controls;
- preview modes;
- compile adapter;
- validation/readiness rules.

The user should not have to know which Python script, profile JSON, validator or manifest format corresponds to that recipe. Forge knows which repository operation to request because the subtype registry declares it.

---

## 9. Example: Battle Pyramid entirely inside Forge

1. User opens Forge → Quest Studio → `Battle Pyramid`.
2. Forge loads the current Battle Pyramid recipe/constraints from the repository-backed subtype contract.
3. User writes the premise and designs floors/encounters/dialog in the shared Studio.
4. Local checks give immediate route/editing feedback.
5. User presses `Compile`.
6. Forge persists the Quest Source revision and requests the approved Battle Pyramid build operation.
7. Repository worker runs the canonical scripts/contracts/validation.
8. Forge receives a structured result and renders any blockers inline.
9. User resolves real design/admin decisions in Forge and recompiles.
10. Forge shows the valid generated manifest/package and review summary.
11. User explicitly starts the live write through the existing Forge runner.
12. Forge displays readback/reconciliation/results without leaving the product.

At no point should the user need to manually open a JSON file, invoke a script, move a manifest between applications, or relay routine compiler output through chat.

---

## 10. Example: source-of-facts lookup

Suppose the user edits a Mission encounter and Forge needs to know the allowed rank profile or whether a particular objective form is legal.

Forge should not depend on a developer having remembered to copy that rule into a component constant.

Instead it should obtain the current generated/profile contract (or a generated snapshot derived from it), display the resulting constraint, and retain its provenance.

For deeper or changing evidence, such as reuse of an existing AI/asset/quest, Forge can request/search the repository's captures/catalogs and show the source freshness/evidence alongside the result.

This makes Forge an **interface to TNR knowledge**, not another competing knowledge store.

---

## 11. Offline/latency and failure behavior

Repository-backed does not mean unusable when a build service is slow or temporarily unavailable.

Forge should distinguish:

- `Draft saved locally`;
- `Repository revision saved`;
- `Build requested`;
- `Building`;
- `Build result received`;
- `Repository unavailable / retry save`;
- `Build failed`;
- `Build blocked by design decision`.

A user must not lose authored work because GitHub/API/worker access fails.

Local durable draft persistence plus explicit repository-sync state is therefore part of the architecture.

Similarly, an old cached contract may remain usable for editing, but Forge must show that canonical compile has not yet run against the current repository source.

---

## 12. What this architecture deliberately avoids

Do not make the redesign depend on:

- duplicating all repository rules in UI source;
- running the full Python/Pillow toolchain inside the mobile browser;
- one Git commit or network request per keystroke;
- exposing raw manifests as the normal authoring model;
- giving the browser an arbitrary remote-shell primitive;
- allowing compiler/build automation to perform live-game writes;
- storing a second canonical content/project database inside Forge;
- forcing the user through separate interfaces merely because different repository scripts implement different content recipes.

---

## 13. Architectural acceptance test

The architecture is succeeding when this statement is true:

> **The operator can remain in Forge for the complete human workflow, while every important machine decision can still be traced to its owning repository source, script, contract, evidence or generated artifact.**

A second test is equally important:

> **Replacing or improving a repository compiler/profile/contract should improve Forge behavior through the adapter/generated-source path rather than requiring a second manual rewrite of the same rule in the UI.**

That is the desired division of responsibility for Forge Next.