# Forge Next — Mission Studio

**Status:** PRODUCT / UX DESIGN CONTRACT — PROPOSAL, NOT ENGINE LAW OR IMPLEMENTATION CONTRACT  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**TNR Tools baseline inspected:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Content Designer  
**Depends on:** `FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md`, `FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md`, `skills/building-tnr-content/scripts/mission.py`, `skills/building-tnr-content/scripts/storyboard.py`, `skills/building-tnr-content/data/48_DATA_mission_profiles.json`, `skills/building-tnr-content/references/quest.md`  
**Purpose:** define a human-first mission authoring surface that preserves the existing mission compiler/profile/storyboard contracts, moves mechanical feedback earlier in the creative loop, and makes generated manifests an output rather than the primary editing surface

---

## 1. Product thesis

Mission Studio should make creating a TNR mission feel like designing a **short player experience**, not filling a quest payload.

The current repository already contains the core compiler architecture:

- the **design sheet** owns creative mission input;
- the **mission profile** owns rank/policy values that should not be re-decided during every build;
- generated/source contracts own legal payload shapes;
- `mission.py` combines those inputs and refuses unresolved policy/balance decisions;
- `storyboard.py` renders the design sheet into the human-readable editing/review surface;
- art requirements are generated from the objective graph rather than guessed separately;
- validators/preflight own final mechanical legality.

Mission Studio should expose those distinctions directly.

The central interaction principle is:

> **Edit the mission. Inspect the mechanics. Compile the payload.**

Not:

> Edit a payload and hope it reads like a good mission.

---

## 2. Critical current-state constraint: do not canonize the Forsworn flatten experiment

Current repository state says the ten Forsworn missions have a staged four-node no-travel rewrite and that doctrine/law changes are explicitly **deferred until player feedback**.

Therefore Mission Studio must not:

- make `dialog → start_battle → dialog → win_quest` the universal mission template merely because it is the newest operational experiment;
- rewrite mission-profile shape policy to match that experiment without the later ruling;
- label longer mission shapes invalid simply because the Forsworn wave is being tested in a flatter form;
- treat `start_battle` as the mandatory mission combat primitive.

The Studio should instead be driven by:

1. the selected canonical mission profile / approved project brief;
2. current quest mechanics/contracts;
3. any task-specific approved design source;
4. later durable rulings if the player-feedback experiment becomes doctrine.

This distinction is essential. Forge should make design evolution easier without turning the latest live experiment into accidental global policy.

---

## 3. Source-of-truth model

### 3.1 Design sheet remains the creative source

Mission Studio should save/edit the structured creative source that `mission.py` can consume or a versioned successor with the same authority split.

Creative fields include the mission's human experience:

- name;
- premise / description;
- success description;
- objective nodes;
- objective prose;
- choices;
- scene intent;
- encounter intent / roster inputs where the compiler contract supports them;
- route-specific authored differences.

The Studio should not make the generated manifest the editable source.

### 3.2 Mission profile owns deterministic mission policy

`48_DATA_mission_profiles.json` explicitly distinguishes:

- author-owned fields;
- profile-owned fields;
- fixed values;
- generated values;
- values deliberately null by design;
- unresolved `AWAITING_RULING` values.

Mission Studio should visualize this ownership rather than flattening all fields into one form.

Recommended field treatment:

| Ownership | UI treatment |
| --- | --- |
| Author | ordinary editable control |
| Profile | read-only inherited value, with source/profile label |
| Fixed | read-only policy value; hidden from normal prose authoring unless relevant |
| Generated | status/preview only; regenerated from source |
| Null by design | normally suppressed; inspectable under policy detail |
| `AWAITING_RULING` | blocking decision card, never a plausible default |

### 3.3 Generated manifest is a build artifact

The manifest should be accessible for expert inspection, diff and handoff evidence, but ordinary mission editing should not require the author to understand:

- full quest field lists;
- nested payload envelopes;
- `@ai` / `@img` wiring syntax;
- default-filled technical fields;
- procedure-specific request shapes.

A raw JSON editor, if retained at all, belongs behind an advanced/debug affordance and must not silently become the canonical creative source.

---

## 4. Mission Studio workspace anatomy

This document does not settle final route/tab names. It defines the conceptual surfaces the Studio must provide.

### 4.1 Mission header

Always keep available:

- mission title;
- rank/profile;
- project/workstream association;
- design status;
- unresolved decisions count;
- structural summary: nodes / battles / choices / endings / travel goals;
- compile/validation state;
- next meaningful action.

Do not use a generic `Valid` badge to imply content quality, art readiness or approval.

### 4.2 Overview / brief

The author should begin from player experience, not node mechanics.

Recommended fields:

- mission name;
- rank/profile selection when known;
- one-line player experience;
- premise;
- success outcome / what changed;
- antagonist/obstacle;
- expected tone;
- cast;
- important reuse requirements;
- off-limits themes/mechanics;
- task-specific design notes.

The Studio may derive structural guidance from the selected profile/brief, but should clearly mark whether guidance is:

- required by profile;
- required by engine contract;
- recommended design practice;
- merely an existing example.

### 4.3 Storyboard view — primary authoring surface

This should embody the existing `storyboard.py` philosophy.

Each node card should lead with human content:

- scene / beat label;
- speaker/cast;
- background/setting intent;
- player-facing text;
- choice labels;
- encounter summary;
- success/failure text;
- route destination in readable terms.

Technical node id and engine task remain visible but secondary.

#### Prose editing

Prose changes should feel like ordinary script editing.

Structural changes should be more explicit:

- change node type;
- add/remove choice;
- change edge;
- split scene;
- add encounter;
- add retry/failure route;
- change ending.

This preserves the current rule that text edits are cheap but wiring edits are meaningful.

### 4.4 Semantic flow view

The graph should visualize **engine meaning**, not just boxes and arrows.

Recommended semantic classes:

- **Gate** — dialog / player commitment;
- **Instant action** — e.g. `start_battle`, `win_quest`, `fail_quest`, `reset_quest`, `new_quest` where applicable;
- **Location goal** — travel/collect/deliver/defeat-at-location style objectives;
- **Counter / progression goal** — threshold tasks;
- **Ending** — success/failure terminal outcome.

The exact vocabulary should be sourced from the current quest contract/reference rather than hard-coded from this proposal.

#### Graph visual responsibilities

Show:

- start node;
- success edges;
- failure edges;
- reset edges;
- branch choices;
- endings;
- unreachable nodes;
- ambiguous/multiple starts;
- auto-activation risk where current mechanics make it relevant;
- dialog gating before instant actions;
- travel/map consequences;
- route-specific battle counts.

#### Mobile behavior

The flow graph must not be the only editor.

On phone:

- storyboard/list remains primary;
- `Route` action opens a focused full-screen flow view;
- tapping a node opens its detail;
- reordering/rewiring must have accessible controls beyond freehand drag;
- zoom/pan is for orientation, not required precision input.

### 4.5 Encounter view

A mission author should understand fights in player terms without opening raw `opponentAIs` structures.

For each battle node, show:

- encounter label;
- combat primitive / consequence (`immediate confrontation`, `map/location fight`, etc.);
- enemy composition;
- new vs reused AI;
- headcount;
- level/profile intent;
- avatar readiness;
- AI behavior summary when available;
- loss behavior / route;
- retry behavior;
- relevant balance/admin decision state.

Mission Studio may embed a compact encounter editor or deep-link into a future Encounter/AI Studio.

It should never encourage a user to choose a fight primitive only because one takes fewer fields. Tooling convenience must not become design policy.

### 4.6 Scene / art view

The objective graph should drive scene requirements.

For each dialog/scene-bearing beat:

- background intent;
- scene character(s);
- new vs reused asset;
- placeholder vs accepted production asset;
- exact filename/ref when generated;
- art-production state;
- scene completeness warnings.

After the graph stabilizes, the Studio should display the generated shot list from the canonical art tooling rather than maintaining a separately hand-authored asset checklist.

A user should be able to answer:

> If I add this character/scene, what new art work did I just create?

before the project reaches manifest time.

### 4.7 Policy / profile view

This is where inherited mission correctness becomes visible without cluttering authoring.

Show grouped read-only policy such as:

- quest type;
- rank;
- level/eligibility fields;
- attempt/completion policy;
- prerequisite/village policy;
- consecutive-objective behavior;
- hidden-first state;
- reward package;
- shape guidance / ceilings encoded by the profile;
- generated/null-by-design fields.

For each value, make the source understandable:

- `From C-rank mission profile`;
- `Fixed by hidden-first doctrine`;
- `Generated from art shot list`;
- `Awaiting director ruling`.

The goal is trust: an author can see why a value exists without being invited to casually override it.

### 4.8 Decision surface

Any unresolved user-owned value should be promoted out of ordinary technical forms.

Examples:

- exact enemy level where a profile supplies only an allowed band;
- unresolved reward/profile value;
- encounter count/difficulty where not already approved;
- new-vs-reuse decision;
- art direction/final acceptance.

A blocking decision card should contain:

- question;
- why the compiler cannot decide;
- allowed/known range if source-backed;
- evidence/comparisons;
- project tasks blocked;
- owner;
- approval recording target.

`mission.py` currently treats refusal as a feature. Mission Studio should preserve that product philosophy.

---

## 5. Authoring actions should speak the language of missions

The primary add actions should be conceptual rather than raw engine task names.

Candidate actions:

- `Add dialog beat`
- `Add choice`
- `Add confrontation`
- `Add travel objective`
- `Add collection/delivery objective`
- `Add retry route`
- `Add success ending`
- `Add failure ending`

After the user chooses an intent, Forge can ask the minimum additional questions required to map it to a legal engine primitive.

Advanced users may inspect or change the underlying objective type, but `task: start_battle` should not be the first language a content author sees.

### Example: Add confrontation

Forge could ask:

1. **Where does the fight happen?** `Right now` vs `Player travels to it`.
2. **Who is fought?** reuse existing AI / create new encounter.
3. **What happens on loss?** retry / route elsewhere / hard fail, constrained by current engine semantics.
4. **What should the player read before committing?** dialog beat / use existing gate.

Forge then proposes the appropriate engine structure and shows the resulting route before committing the structural edit.

This moves schema knowledge into a safe translation layer while leaving the generated structure inspectable.

---

## 6. Inline mechanical intelligence

Mission Studio should catch high-value structural problems during design, not only during final manifest validation.

### Hard blockers

Examples, subject to the current canonical validator/reference:

- unresolved edge target;
- invalid/multiple start nodes;
- missing required failure route for a battle primitive under current house/validator rules;
- impossible objective type/field combination;
- unresolved references required for compilation;
- profile-required value still `AWAITING_RULING`;
- battle headcount beyond an approved profile ceiling;
- build-required source missing.

### Mechanical warnings / advisories

Examples:

- instant battle action not directly gated by dialog when the intended experience requires player commitment;
- location objectives likely to introduce travel when the approved brief says zero travel;
- multiple location goals sharing activation conditions in a way that may co-fire;
- reset route points somewhere surprising;
- scene-bearing dialog lacks explicit scene intent;
- branch ends without a clear player-facing consequence;
- route materially exceeds approved node/fight pacing guidance.

### Editorial/design advisories

These must look different from engine errors.

Examples:

- long node prose;
- choice labels that do not communicate consequence;
- repeated scene with no meaningful state change;
- antagonist motive absent from the brief;
- branch that changes text but not outcome;
- failure route teaches nothing / creates pointless repetition.

Forge should never imply an editorial advisory is a server rejection.

---

## 7. Preview Lab inside Mission Studio

Preview is one of the biggest quality multipliers because missions combine prose, flow, encounters and visual assets.

The Studio should provide several explicit preview modes.

### 7.1 Route playback

Choose a route and step through it in player order.

Show:

- dialog text;
- choice selection;
- encounter card;
- success/failure transitions;
- ending.

Display route metrics:

- nodes traversed;
- fights;
- travel goals;
- decisions/choices;
- ending reached.

### 7.2 Dialog / scene preview

Approximate the TNR scene composition using the accepted/reused background and characters.

Clearly label this as a **Forge preview**, not proof of exact live-client rendering unless Fable later builds a source-faithful shared renderer and proves parity.

### 7.3 Structural comparison

Compare two mission revisions or routes by player-visible consequences:

- nodes added/removed;
- prose changes;
- choices changed;
- fights changed;
- travel changed;
- endings changed;
- assets newly required.

This is more useful to a reviewer than a raw JSON diff.

### 7.4 No fake combat simulation

Unless a real, source-backed deterministic simulator is later introduced and independently verified, Mission Studio should summarize encounter design rather than pretend to predict exact combat outcome.

---

## 8. Compile / preflight experience

`Compile` should mean:

> Rebuild the technical outputs from the current canonical creative/profile sources and report what is still unresolved.

Recommended phases:

1. validate design-sheet structure;
2. resolve mission profile;
3. surface all `AWAITING_RULING` values at once;
4. construct enemies where the sheet requires them;
5. wire battle refs;
6. enforce approved headcount/profile constraints;
7. build quest record / combined manifest;
8. generate art shot list;
9. run canonical manifest validation/preflight;
10. summarize blockers, advisories and generated outputs.

The implementation should reuse/share the existing deterministic logic rather than translating it into an independent UI-only rule set that can drift.

### Compile result hierarchy

Show first:

- `Build blocked` / `Build valid`;
- decisions still needed;
- structural errors;
- missing assets/references;
- generated entity/art summary;
- validator result.

Then allow access to:

- generated manifest;
- exact source files;
- hashes;
- raw validation output.

### Compile does not mean approved

A valid manifest can still have poor prose, weak pacing, unaccepted art or unresolved content-review concerns. Keep `Mechanically valid`, `Content approved`, `Art accepted`, and `Ready for production` distinct.

---

## 9. Review experience

Mission review should be based on the human mission, not the manifest.

Recommended review packet:

- mission premise and intended player experience;
- selected profile/rank;
- storyboard;
- route map;
- route metrics;
- encounter summaries;
- scene/art preview/status;
- inherited reward/policy summary;
- open/settled decisions;
- validation/QC result;
- change summary since last reviewed revision.

Review comments should ideally be anchorable to:

- overview field;
- node/beat;
- edge/choice;
- encounter;
- asset;
- policy/decision.

The final canonical review-comment storage model remains a Fable/director architecture decision.

---

## 10. Relationship to Content Project Workspace

Mission Studio is a **task workspace inside a project**, not a second project tracker.

The parent project owns:

- task sequencing;
- blockers/dependencies;
- cross-discipline decisions;
- overall asset/build/review/production readiness;
- final delivery/readback history.

Mission Studio owns the mission's authoring experience:

- creative source;
- mission structure;
- mission-specific decisions;
- derived encounters/assets;
- preview;
- compile result.

When the mission reaches a durable stopping point, the project should receive:

- current task state;
- durable source paths;
- compile/validator evidence;
- newly created blockers/decisions;
- generated asset requirements;
- concise resume note if incomplete.

This mirrors the existing content-workstream contract instead of inventing a Studio-only progress system.

---

## 11. Desktop and phone behavior

### 11.1 Desktop / tablet

Candidate composition:

- left project/app navigation;
- center storyboard or flow canvas;
- right contextual inspector for node/scene/encounter/policy detail;
- persistent compile/readiness summary;
- preview can open side-by-side for prose/scene work.

Do not show every technical field simply because width exists.

### 11.2 Phone

Recommended default:

- compact mission header;
- current blocker/decision;
- storyboard list;
- floating/sticky contextual `Add beat` or current primary action;
- full-screen editor for one beat;
- full-screen route map when requested;
- bottom sheet / secondary page for inherited policy and raw detail;
- compile result as a clear summary before raw output.

Avoid:

- tiny draggable graph nodes as the only structural editor;
- multi-column forms;
- horizontal field tables;
- long fixed headers that hide prose;
- hover-only edge controls.

---

## 12. Revision and provenance

The Studio should make it difficult for the human-reviewed mission and generated payload to diverge.

### Required principle

Every compiled delivery artifact should be traceable to:

- exact mission creative source revision;
- exact mission profile revision;
- relevant contract/spec revision;
- generated art requirement revision;
- validator/build result.

If the source changes after compilation, the package becomes stale/superseded and the UI should say so.

### Human review snapshots

When a mission is submitted for review, Forge should be able to identify the exact durable revision under review. If the author edits it afterward, reviewers should see that the review target changed rather than unknowingly approving moving content.

This does not necessarily require Git branches per mission; Fable should choose the lightest repository model that preserves exact revision identity.

---

## 13. Mission-quality intelligence opportunities

These are future advisory capabilities, not engine laws.

### Route quality

- dead/meaningless choices;
- one branch substantially longer than the others without an intentional reason;
- repeated failure loops;
- route with no player-visible consequence;
- unintended travel introduced by one objective.

### Narrative quality

- speaker appears without prior introduction where that matters;
- inconsistent character naming/pronouns against project references;
- duplicated or near-duplicated beats;
- success text does not resolve the premise;
- encounter occurs without setup/consequence.

### Production quality

- scene art required but absent;
- new character introduced with no portrait decision;
- placeholder/reused art still wired after bespoke art acceptance;
- mission icon missing;
- accepted asset bytes not durable;
- filename mismatch between art and generated package.

These advisories should link directly to the beat/asset they concern and always distinguish automated suggestion from canonical rule.

---

## 14. Candidate first-release scope

A useful first Mission Studio does **not** need to solve every quest type.

### V1 — mission sheet editor + compiler visibility

- open/create mission design source;
- overview fields;
- storyboard node editing;
- readable route links;
- profile/policy viewer;
- unresolved decision surfacing;
- compile using current mission toolchain;
- validator summary;
- generated art-shot requirements;
- project/workstream linkage.

### V1.5 — semantic flow and preview

- full semantic graph;
- route playback;
- scene preview;
- structural change summary;
- stronger inline lints.

### V2 — integrated encounter/art/research workflows

- existing AI/asset search with evidence provenance;
- compact encounter editing / handoff to Encounter Studio;
- asset production linkage;
- review comments / revision snapshots;
- package readiness.

This sequence lets Forge improve content quality early without first rebuilding every downstream tool.

---

## 15. Acceptance scenarios

### Scenario A — author a simple mission without JSON

An operator creates a mission, chooses an approved profile, writes the premise/storyboard, adds a legal route and compiles a valid hidden mission without editing a manifest.

### Scenario B — unresolved profile decision

The chosen profile contains an `AWAITING_RULING` value. The Studio blocks compile, shows every unresolved ruling at once and routes them to the decision surface. It does not silently substitute `0`, `1` or a remembered value.

### Scenario C — structural wiring edit

The author changes a choice destination. The Studio visibly treats this as a route change, updates the graph/route preview and re-runs structural checks.

### Scenario D — prose-only edit

The author changes dialog wording. The Studio does not force them through raw edge/task controls, but the later compile produces a new traceable artifact.

### Scenario E — zero-travel brief violated

A location objective is added to a mission whose approved task brief says zero travel. The Studio warns about the player-facing consequence before package time.

### Scenario F — new encounter adds art

The author adds a new enemy. The Studio shows the new AI/avatar requirement and project readiness changes immediately.

### Scenario G — compiler-valid but not review-ready

Validation passes, but one portrait is unaccepted and a content decision remains open. Forge reports `Mechanically valid` while keeping `Ready for review/production` false.

### Scenario H — Forsworn experiment does not become default

Opening a new mission after the current Forsworn flatten work does not automatically seed the four-node experimental shape unless an approved profile/brief/ruling actually calls for it.

### Scenario I — phone editing

On Android/phone, the operator can edit prose, inspect route destination, add a choice and compile without manipulating tiny graph nodes or horizontally scrolling a schema table.

---

## 16. Explicit non-goals

Mission Studio does **not**:

- replace `mission.py`/profiles/contracts with UI-owned copies;
- make existing live missions the design standard merely because they exist;
- convert a temporary workstream experiment into doctrine;
- settle balance, rewards, rarity, encounter difficulty or art direction without user approval;
- simulate combat without a separately verified simulation contract;
- make a successful compile equivalent to final content acceptance;
- perform live-game writes on its own;
- make publishing part of ordinary save/compile behavior;
- require a final Forge information architecture to be chosen before the Studio concept can be used.

---

## 17. Open product decisions for Fable/director planning

1. **Creative source format:** preserve the current sheet schema as-is, evolve it versionedly, or introduce a more general authored-quest source that compiles down to mission sheets?
2. **Graph editing depth in V1:** storyboard plus edge controls first, or full semantic graph immediately?
3. **Mission vs generic Quest Studio:** mission-specific Studio first, or shared quest core with mission/event policy adapters?
4. **Review annotations:** repository-backed comments, project task notes, or another durable review artifact?
5. **Reuse search:** embed live/catalog search directly in Mission Studio or always hand off to a shared Research Library?
6. **Policy override workflow:** whether exceptional approved deviations create a new profile variant, a task-specific brief override, or another explicit canonical mechanism.

The Studio should not answer these by hidden implementation convenience. Each affects maintainability, authority or future content consistency and deserves an explicit architecture/product decision.
