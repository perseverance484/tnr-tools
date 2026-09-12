# Forge Next — Content Studio Expansion Study

**Status:** PRODUCT / WORKFLOW STUDY — PROPOSAL, NOT IMPLEMENTATION CONTRACT  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**TNR Tools baseline inspected:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Game-source head inspected:** `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`  
**Lead lens:** Content Designer  
**Supporting lenses:** UI/UX Reviewer, Art Director, Engineering Auditor  
**Purpose:** identify product channels that can make Forge a seamless one-stop content-development environment without duplicating canon, weakening production safety, or pre-empting Fable's architecture work

---

## 1. Product thesis

Forge should evolve from a **manifest execution console** into a **content-development control plane**.

A seamless Forge experience should let a user remain in one product from the first idea through post-launch verification:

> **Brief → Research → Design → Narrative/Mechanics → Assets/Visual Communication → Preview → Review/Decisions → Build → Preflight → Execute → Verify → Publish → Feedback/Revision**

The important qualifier is that Forge should **orchestrate existing authorities rather than become a second content database**.

The repository already has strong domain-specific owners:

- content workstreams coordinate multi-session work;
- mission profiles + `mission.py` own deterministic mission construction;
- `storyboard.py` owns the human-readable mission editing surface contract;
- quest/event references own engine-aware design rules;
- generated contracts and validators own payload legality;
- the art spec, reference pack and QC tools own production assets;
- captures own fresh live-state evidence;
- the live game owns live records;
- the user owns balance, rewards, publishing, art direction and final acceptance.

Forge should make those systems feel like one product **without replacing their authority**.

### One interface, many owners

The design goal is therefore:

- **one project workspace** for the human;
- **one visible lifecycle** from idea to verified delivery;
- **one evidence trail** showing where each fact came from;
- **one decision surface** for unresolved director/admin choices;
- **many underlying canonical owners**, explicitly preserved.

This is a stronger model than trying to make every piece of content originate as a Forge-native database row.

---

## 2. What the current workflow already proves

### 2.1 Mission production is already a compiler pipeline hidden behind files

`skills/building-tnr-content/scripts/mission.py` already separates the mission into the right conceptual layers:

1. a **creative design sheet** containing name, prose and objective graph;
2. a **rank profile** containing what is correct for that mission class, including reward/profile policy;
3. **source-derived contracts** containing what the engine legally accepts;
4. generated enemy records and battle wiring;
5. a generated art shot list derived from the graph;
6. a combined manifest output.

The script deliberately refuses unresolved `AWAITING_RULING` values instead of silently turning a missing balance decision into a default. This is exactly the behavior a high-quality visual authoring surface should preserve.

The opportunity is not to rewrite mission construction in the UI. It is to create a **Mission Studio** that presents the creative/design layer directly and delegates deterministic construction to an adapter over the existing compiler/tooling contract.

### 2.2 Storyboard is already the correct authoring philosophy

`storyboard.py` says the storyboard is the editing surface while the design sheet remains the source of truth. Prose can be edited freely; node ids and edges remain explicit wiring.

That principle should become first-class Forge UX:

- humans edit a readable story/flow representation;
- graph wiring remains inspectable;
- generated payloads are outputs rather than the editing surface;
- changing wiring is an explicit structural action rather than an accidental text edit.

### 2.3 Quest rules justify a semantic graph editor, not a generic node canvas

The quest reference distinguishes semantic classes such as dialog gates, instant actions, location goals and counters. Availability and auto-link behavior make apparently small graph changes mechanically significant.

A Forge quest editor therefore has more value if it knows what a node **means**:

- `dialog` visually reads as a gate;
- `start_battle` reads as an instant consequence and warns when not gated as intended;
- location goals expose map/travel consequences;
- reset/failure routes show retry behavior;
- unreachable/multiple-start/unsafe sequencing states appear while designing, not after manifest generation.

The quality gain comes from moving engine-aware feedback earlier in the creative loop.

### 2.4 Event intake already demonstrates the desired staff-facing abstraction

`EVENT_SHEET.md` and `references/event.md` deliberately split the workflow into:

- a thin **plain-language staff canvas**;
- a deeper **internal build contract**.

Blank / `AI` / `NONE` have distinct meanings, balance fields remain proposals, attachments are accepted as references, contradictions are surfaced, and the event remains hidden until approved.

This is already a product design for a **Brief Intake Studio**. Forge can turn it into a guided form without exposing engine fields to the submitter.

### 2.5 Content workstreams already describe the project-management model Forge needs

`state/workstreams/<slug>/roadmap.json` already models:

- task groups;
- dependencies;
- READY / BLOCKED / REVIEW / COMPLETE state;
- durable required resources;
- evidence;
- blockers;
- resume notes;
- user-owned decisions.

One Perfect Crop demonstrates a real project crossing design, prose, read-only research, combat specification, several art classes, content-admin decisions, implementation, review, execution and readback.

That is effectively a **content project model** already. Forge should project it rather than inventing a second project tracker.

### 2.6 Art is a separate production discipline with one shared content contract

The art pipeline intentionally differs from manifest construction. It uses the target-specific art spec, approved visual references, one-asset-at-a-time direction, raw QC, processing, dark-composite QC, preflight, user acceptance and exact filename contracts.

Its shared boundary with content is primarily the final asset identity / `@img` filename.

Forge should unify the **experience** while preserving the different pipeline:

- derive required shots from content;
- display target constraints and reference selections;
- track direction → generation → QC → acceptance;
- preview assets in actual target context;
- carry exact filenames into the package automatically;
- show missing/blocked art in project readiness.

It should not flatten art into "just another form field."

A standing project ruling keeps art submission manual. This study therefore does **not** propose automatic live-art submission/upload as a default. A future change to that boundary would require an explicit new director ruling.

### 2.7 Guides are now a first-class game content type and deserve their own studio

Current game source at `36c5873...` includes `guide` in `ContentTypes` and a dedicated guide content model.

`GuideArticleValidator` supports:

- slug;
- title / subtitle / excerpt;
- SEO title / description;
- category;
- rich HTML content;
- cover image;
- FAQ;
- ordering;
- native `published` state;
- related bloodline / item / jutsu links;
- source URL;
- review notes.

The guide router supports draft-aware reads plus role-gated create/update/delete. New guides begin unpublished, updates are moderated and action-logged, and the existing game editor already demonstrates edit/preview tabs, FAQ editing, image upload and rendered preview.

This makes a **Guide Studio** a highly credible Forge expansion, not a speculative feature.

However, the current Forge-generated contract surface is pinned before this guide support and the current `45c_DATA_constructors.json` does not include guide validators. Direct Forge guide operations therefore require a deliberate game-source pin/contract/procedure-registry expansion before implementation. UI design must not pretend the current Forge runner can already do it.

### 2.8 Infographics are a genuine missing production lane

No existing `tnr-tools` workflow owns infographics as a production class.

That matters because the current TNR art pipeline is deliberately hostile to text/UI-like output: production game art rejects labels, text, panels, borders and grids. An infographic intentionally needs many of those things.

Therefore **infographics must not be squeezed into the game-art pipeline**. They need a distinct Visual Communication workflow with their own:

- source/evidence provenance;
- layout templates;
- typography/readability rules;
- export targets;
- accessibility expectations;
- revision semantics;
- integration contract with guides or external staff/community delivery.

Current guide HTML explicitly permits image elements, making guide-embedded infographics a plausible downstream use, but the exact hosting/upload adapter must be source-audited before implementation.

---

## 3. Proposed Forge development channels

These are **capability channels**, not a final navigation menu. Several could share one workspace or route once Fable settles the information architecture.

### Channel A — Project / Workstream Workspace

**Goal:** make the entire content project legible in one place.

Forge should be able to project the existing content-workstream state into a human workspace showing:

- objective and content type;
- lifecycle stage;
- task dependency graph;
- READY / BLOCKED / REVIEW / COMPLETE state;
- blockers and resume notes;
- required resources;
- evidence anchors;
- open director/admin decisions;
- asset readiness;
- generated packages;
- review handoffs;
- execution/readback state;
- publication state.

**Quality gain:** users stop manually reconstructing "where are we?" across chats, files and push manifests.

**Authority rule:** `roadmap.json` remains coordination source. Forge is a projection/editor subject to the same validation rules, not a new project database.

**Priority:** P0. This is the connective tissue for the one-stop-shop experience.

---

### Channel B — Brief Intake Studio

**Goal:** turn an idea/submission into an executable, durable content brief without exposing engine internals.

Candidate intake templates:

- Event;
- Mission / mission arc;
- Story quest;
- Combat encounter;
- Item / jutsu concept;
- Guide article;
- Infographic / explainer;
- Art-only request.

Event intake should directly preserve the semantics already proven by `EVENT_SHEET.md`:

- blank / AI / NONE distinction;
- [BALANCE] values flagged as proposals;
- attachments and reference intent;
- contradictions surfaced rather than merged silently;
- player fantasy/outcome captured before mechanics;
- explicit off-limits material;
- intended publication window and audience.

Forge can then create or update the appropriate durable source/workstream pointers rather than asking the user to manually copy a markdown template.

**Quality gain:** upstream ambiguity is caught before it infects prose, combat, art and implementation.

**Priority:** P0/P1.

---

### Channel C — Mission / Quest Studio

**Goal:** make mission design feel like narrative design rather than JSON authoring.

Recommended capabilities:

#### Storyboard view

- premise;
- success/failure outcome;
- node-by-node prose;
- actor/background context;
- choice text;
- battle summaries;
- inline comments/review notes.

#### Semantic graph view

- nodes grouped by engine behavior: gate / action / goal / counter;
- success/failure/reset edges;
- start node and endings;
- branch/wings visualization;
- reachability;
- retry loops;
- dialog-gating visibility;
- travel/map consequence badges;
- scene completeness.

#### Mission profile / policy view

- chosen rank/profile;
- fields fixed by the profile;
- creative fields editable by the author;
- balance-owned fields shown as `Awaiting ruling` rather than editable defaults;
- deterministic values explained as inherited, not mysterious hidden state.

#### Preview view

- mobile dialog/script preview;
- sequence playback through a selected route;
- success/failure route walkthrough;
- enemy/asset placeholders;
- estimated node/fight/travel counts;
- clear label that this is a structural/player-experience preview, not a live engine simulation.

#### Compile / preflight view

- run the equivalent mission compiler/factory/validator chain;
- show generated enemy/art requirements;
- show hard blockers separately from advisories;
- expose generated manifest only under progressive disclosure.

**Quality gain:** mechanical errors and pacing/design flaws become visible while authoring rather than after package construction.

**Implementation constraint:** reuse/port/share the deterministic mission/compiler rules rather than re-encoding them independently in UI code.

**Priority:** P0/P1. This is the strongest existing workflow-to-product conversion opportunity.

---

### Channel D — Encounter / AI Studio

**Goal:** make enemy design, kit selection and behavior understandable alongside the quest that uses it.

Potential capabilities:

- new enemy vs existing-live reuse decision;
- catalog search and fresh-capture provenance;
- role/archetype and intended player experience;
- approved level/stat/pool contract;
- jutsu pool browser;
- explicit new-vs-reused jutsu distinction;
- ordered behavior-rule editor;
- range/target/condition visualization;
- headcount and encounter composition;
- rule linting against source-derived condition/action vocabulary;
- avatar requirement/status;
- human-readable "what this AI will try to do" summary.

The studio should deliberately distinguish:

- source-contract validity;
- design intent;
- balance values;
- live reuse evidence.

**Quality gain:** the quest author can judge the encounter as an experience, not a pile of ids and rules.

**Priority:** P1.

---

### Channel E — Balance / Rewards / Eligibility Decision Workbench

**Goal:** remove unresolved director/admin decisions from prose and manifests and give them a dedicated decision surface.

Instead of scattering placeholders across files, Forge can aggregate every unresolved value surfaced by compilers/workstreams:

- reward values and drop rates;
- repeatability;
- min/max eligibility;
- ranks;
- enemy counts/difficulty parameters;
- rarity;
- event windows;
- publish timing;
- other user-owned knobs.

The workbench should show:

- decision requested;
- why it matters to player experience;
- verified comparison/reference data;
- proposed options;
- downstream tasks blocked by the decision;
- current owner;
- ruling status;
- canonical destination after approval.

It should never auto-select a plausible default merely to make a build green.

**Quality gain:** fewer accidental design decisions are made by implementation order.

**Priority:** P0/P1.

---

### Channel F — Research / Capture / Reuse Library

**Goal:** make repository evidence reusable during content creation instead of requiring separate investigative sessions for every question.

Candidate capabilities:

- search live-name catalogs;
- browse committed captures;
- freshness/provenance badges;
- compare catalog value vs newer capture;
- inspect existing quest/AI/item/jutsu/asset records;
- save project-scoped reuse candidates;
- record accept/reject reasoning;
- request/generate a read-only capture manifest where current Forge supports the procedure;
- show whether a proposed reuse would mutate a shared live entity;
- link captured visual assets into art-reference selection.

A useful distinction in the UI is:

- **known from source contract**;
- **known from fresh capture**;
- **known from catalog**;
- **inferred / needs capture**.

**Quality gain:** content designers make reuse and compatibility decisions from evidence instead of memory.

**Priority:** P1.

---

### Channel G — Art Direction / Asset Studio

**Goal:** keep visual production inside the same project experience without collapsing the art pipeline into manifest fields.

Capabilities should include:

- automatically generated shot list from the quest graph;
- required target/type and exact filename;
- current art-spec constraints;
- approved reference selection/provenance;
- direction brief;
- generation status;
- raw-QC status;
- processed output;
- dark-composite preview;
- art-preflight result;
- version lineage (`_b`, `_c`, etc.);
- user acceptance state;
- wiring status into the eventual content package;
- missing-art readiness blockers.

Forge could also provide a context preview showing scene characters over backgrounds or icons at approximate in-game display size, while clearly distinguishing that from the game's real renderer.

**Boundary:** retain manual live art submission/upload under the standing ruling unless the director explicitly revisits it.

**Quality gain:** content and art stop drifting apart; filenames, scene requirements and acceptance status remain tied to the originating project.

**Priority:** P1.

---

### Channel H — Guide Studio

**Goal:** provide a first-class long-form player-information workflow rather than treating guides as raw HTML edits.

Recommended authoring experience:

#### Article structure

- title / subtitle / excerpt;
- category;
- slug;
- cover image;
- section outline / headings;
- rich body content;
- FAQ editor;
- related item/jutsu/bloodline links;
- source/provenance notes;
- review notes;
- SEO fields;
- ordering;
- draft/published state.

#### Structured blocks

Forge should consider authoring helpers for common TNR guide patterns:

- callout / warning;
- step sequence;
- comparison table;
- item/jutsu/entity reference card;
- glossary definition;
- FAQ;
- image/infographic block;
- source-note block visible to staff but not necessarily players.

These helpers should compile to the game's accepted HTML rather than inventing a new player-facing format.

#### Preview

- use the same or source-faithful HTML preparation rules as the game;
- desktop/mobile reading preview;
- heading/TOC preview;
- image/infographic preview;
- link checking where feasible;
- publish-state consequence shown explicitly.

#### Review / publication

Because guides have a native `published` field, Forge can eventually present an unusually clean draft → review → publish lifecycle after source/registry support lands.

**Current blocker:** current Forge generated contracts/procedure coverage predate guide support. Expand source pin/contracts/registry first; do not bolt guide writes onto stale contracts.

**Quality gain:** higher-quality guides with consistent structure, preview, SEO/FAQ hygiene and auditable publication.

**Priority:** P1/P2 after contract/pin work.

---

### Channel I — Infographic / Visual Communication Studio

**Goal:** create clear, evidence-backed visual explanations for guides, announcements, staff review and player education.

This should be a **new production lane**, separate from TNR scene/icon art.

#### Why separate

Game-art rules intentionally reject text, panels and grid-like UI elements. Infographics often require exactly those things. Reusing the game-art QC contract would reject valid infographic output or encourage the wrong visual language.

#### Candidate infographic families

- combat effect/tag relationship maps;
- loadout-building explainers;
- progression/rank ladders;
- farming loops;
- event flow summaries;
- mission/quest branch diagrams;
- item/jutsu comparison cards;
- economy/process explainers;
- release/event calendars;
- boss-mechanic quick references;
- guide hero diagrams;
- staff-facing balancing/comparison sheets.

#### Data-binding principle

An infographic should be able to bind every factual datum to a source:

- generated contract;
- source constant;
- committed capture;
- approved design/ruling;
- project decision.

The editor should distinguish manually written explanatory copy from data-backed values and show "last verified" provenance where useful.

#### Authoring model

Prefer reusable components/templates over image-generation for text-heavy information:

- title / subtitle;
- sections;
- stat/value cards;
- icon+label rows;
- comparison columns;
- arrows/flows;
- timelines;
- diagrams;
- callouts;
- footnotes/source marks.

The exact rendering technology is an architecture choice for Fable. The product requirement is **reproducible, editable, data-grounded output**, not a flattened one-off image as the only source.

#### Outputs

Potential outputs include:

- responsive HTML block for Guide Studio;
- PNG/WebP export for embedding or external distribution;
- compact mobile version;
- staff-review version carrying provenance annotations.

The delivery adapter for hosted images must be designed/source-audited rather than assumed.

**Quality gain:** documentation becomes visually teachable while remaining correct and maintainable.

**Priority:** P1/P2. High content-quality upside; currently no repository-native owner exists.

---

### Channel J — Player Experience Preview Lab

**Goal:** let creators judge what content feels like before live execution.

Potential previews:

- quest/story route playback;
- dialog scene composition;
- battle/encounter summary cards;
- asset compositing;
- quest listing/icon treatment;
- guide player render;
- infographic mobile render;
- content-admin human diff;
- publication/visibility consequences.

This should explicitly distinguish three evidence levels:

1. **source-faithful preview** — renderer logic is reused/ported from source;
2. **contract preview** — correct shape/content, approximate styling;
3. **concept preview** — visual design aid only.

Never present a static preview as proof that the live game will execute the mechanic correctly.

**Quality gain:** review becomes experiential rather than purely structural.

**Priority:** P1.

---

### Channel K — Content Admin Review Queue

**Goal:** give a reviewer a human content package instead of a manifest.

A review package should aggregate:

- what the content is trying to achieve;
- player-facing preview;
- mechanics summary;
- balance/reward decisions;
- entities created/changed/reused;
- art and acceptance state;
- validation status;
- unresolved blockers;
- source/live-state evidence;
- diff against live where applicable;
- approval / request-changes / reject disposition;
- publication readiness.

Review should progressively disclose execution internals rather than force the admin to understand manifests.

**Quality gain:** content quality review becomes a real product flow rather than a relay through the operator.

**Priority:** P1/P2; exact permissions/approval-state model remains a director/Fable decision.

---

### Channel L — Package / Delivery Composer

**Goal:** turn approved source artifacts into one deterministic delivery package.

The user should not need to manually correlate:

- a design sheet;
- generated AI;
- art filenames;
- a quest object;
- capture requirements;
- validation output;
- a manifest;
- a push zip;
- result/readback expectations.

Forge should show a package as a human object:

> **One Perfect Crop — Build Package**  
> 1 quest · 2 AI · 2 AI profiles · 5 scene assets · 3 icons · 4 captures · 0 unresolved decisions

Then provide:

- generated content list;
- dependency order;
- asset completeness;
- preflight results;
- validation blockers/advisories;
- mutation consequence summary;
- capture/readback plan;
- generated manifest/package under expert disclosure.

The combined-manifest model already proves that the underlying execution can be one package; the UI should make the package the primary human concept rather than the JSON file.

**Quality gain:** dramatically fewer wiring/filename/id/hand-off mistakes.

**Priority:** P0/P1.

---

### Channel M — Publish / Release Center

**Goal:** separate "build succeeded" from "content is approved and visible."

The center should aggregate:

- verified build/readback status;
- hidden/draft state;
- dependency readiness;
- admin approval/disposition;
- publication action(s);
- exact visibility consequence;
- post-publish readback;
- audit/history;
- rollback/recovery options where genuinely supported.

High-consequence publication must remain deliberate and permission-aware. The user retains publishing authority under current doctrine; any delegated admin capability is limited to actual game permissions and future director decisions.

Avoid bulk convenience until dependency/publish behavior is fully proven.

**Quality gain:** removes the common conceptual error that a green write means content is ready/live.

**Priority:** P2 after content/admin models are settled.

---

### Channel N — Post-Launch Feedback / Revision Loop

**Goal:** make content development a lifecycle rather than ending at the push.

A project can retain:

- expected player experience;
- live verification evidence;
- player/admin feedback;
- observed defects;
- balance observations;
- art/prose revision requests;
- new capture evidence;
- revision package history.

A feedback item should be convertible into a new project/workstream task rather than disappearing into chat.

This is especially important for experiments where doctrine/law updates are deliberately deferred pending player feedback.

**Quality gain:** lessons and revisions feed back into the source rather than becoming ephemeral operator memory.

**Priority:** P2.

---

### Channel O — Template / Pattern Library

**Goal:** make proven content structures easy to start without turning old live content into doctrine.

Templates should be explicit, versioned patterns with provenance, for example:

- four-node flavor mission;
- dialog-gated single battle;
- battlepyramid climb;
- committed-choice event wings;
- short repeatable event loop;
- boss raid;
- common guide article structures;
- infographic families;
- review-package templates.

Each template should state whether it is:

- doctrine/policy-backed;
- engine/source-derived;
- approved design pattern;
- example only.

**Quality gain:** consistency without cargo-culting arbitrary live records.

**Priority:** P2.

---

### Channel P — Quality Intelligence / Content Linting

**Goal:** catch quality defects earlier than schema validation.

Schema validity is necessary but not sufficient. Forge can add clearly separated **design/editorial advisories** such as:

#### Quest/mission

- graph complexity vs intended mission class;
- missing scene assets on dialog nodes;
- battle without clear setup/consequence;
- excessive travel or node count relative to selected pattern;
- repeated actors/backgrounds that may be unintended;
- unhandled failure route;
- objective text that fails to name the thing the player must act on;
- structural divergence between storyboard and sheet.

#### Narrative

- unresolved character motive questions;
- inconsistent names/pronouns;
- excessive node length;
- repeated lines/phrases;
- branch choices whose destinations do not meaningfully differ;
- missing completion consequence.

#### Art

- required shot missing;
- accepted asset superseded by unaccepted revision;
- filename/wiring mismatch;
- target/type mismatch;
- QC/preflight missing.

#### Guides

- missing excerpt/SEO fields;
- broken heading hierarchy;
- FAQ incompleteness;
- related-content links stale/missing;
- unsupported HTML after sanitization;
- infographic/data provenance stale.

#### Delivery

- unresolved decision placeholders;
- stale capture relied upon despite fresher evidence;
- package claims complete while evidence is missing;
- publication requested before verification/approval.

Hard contract errors and design advisories must have different visual/behavioral treatment. An advisory should never pretend to be a source-law violation.

**Quality gain:** Forge actively improves content quality rather than only preventing malformed writes.

**Priority:** P1, introduced incrementally.

---

## 4. The ideal end-to-end content project experience

A creator should be able to do the following without leaving the conceptual Forge workspace:

### 1. Start

Choose `New Content Project` and select a goal such as Mission, Event, Guide, Infographic, Item/Jutsu, or another supported content class.

### 2. Brief

Fill a human-facing brief. Forge identifies balance/admin decisions, missing context and attachments.

### 3. Research

Search existing entities/captures/assets, save reuse candidates, request needed read-only evidence, and record why a candidate was accepted/rejected.

### 4. Design

Use the content-specific studio:

- quest graph/storyboard;
- encounter editor;
- guide outline/editor;
- infographic canvas;
- etc.

### 5. Decide

Resolve user/admin-owned values in the Decision Workbench. Block dependent compilation rather than guessing.

### 6. Produce visuals

Generate/track the graph-derived shot list and any visual-communication assets. Run appropriate QC for each production class.

### 7. Preview

Review the content from the player/admin perspective at phone and desktop sizes.

### 8. Review

Content Admin receives one human review package with evidence and decisions, not a manifest.

### 9. Compile

Forge creates the deterministic delivery package and runs every appropriate validator/preflight.

### 10. Execute

Operator sees exact read/write consequence and runs only the approved package through the existing safe execution model.

### 11. Verify

Fresh readback proves what landed. Ambiguity/recovery remains first-class.

### 12. Publish

Approval and verified state are visible before a deliberate publish action.

### 13. Learn

Feedback/readback/revisions attach to the project and can create the next work item.

The seamlessness comes from **continuous project context and evidence**, not from hiding safety boundaries.

---

## 5. A recommended conceptual object: the Content Project view

Forge needs a stable human object around which these studios compose.

The safest approach is a **view/projection**, not a new canonical datastore.

A Content Project view can aggregate pointers to:

- project identity/type/objective;
- existing workstream roadmap;
- design sheet/prose source;
- open decisions;
- captures/research evidence;
- entity reuse decisions;
- art/infographic artifacts;
- generated package(s);
- review disposition;
- run/readback evidence;
- publication state;
- revision/feedback history.

Where a content project does not yet need a formal multi-session workstream, Forge can present an equivalent ephemeral workspace until the work becomes durable. Once durable, repository-backed sources should own reconstructable state.

**Do not create a Forge-only truth that a future repository session cannot reconstruct.**

---

## 6. Cross-cutting capabilities with outsized quality value

### 6.1 Provenance everywhere

Every important value should be able to answer one of:

- source contract;
- fresh capture;
- catalog;
- user ruling;
- design proposal;
- generated output.

This matters especially in infographics and guides, where a visually polished stale number is worse than an obviously incomplete draft.

### 6.2 Human-readable diffs

Show changes in the language of the content class:

- quest node/prose/edge differences;
- enemy kit/rule differences;
- guide section/metadata changes;
- art version changes;
- reward/eligibility changes.

Raw object diffs remain expert detail.

### 6.3 Reuse intelligence

Forge can surface likely reusable content without silently choosing it:

- matching entities by name/type/tags;
- shared asset candidates;
- existing jutsu pool matches;
- similar quests/patterns;
- guide related-content links.

Reuse recommendations must show freshness/provenance and whether editing the candidate would affect shared live content.

### 6.4 Decision gating as a first-class feature

`AWAITING_RULING` behavior is a quality feature, not friction. Forge should make blocked decisions pleasant to resolve instead of making it easy to bypass them.

### 6.5 Generated requirements from source artifacts

Where one artifact deterministically implies another, Forge should derive it:

- quest graph → shot list;
- quest encounters → enemy/avatar requirements;
- guide structure → TOC/heading checks;
- content package → capture/readback plan;
- changed assets → exact filename/wiring ledger.

Manual synchronization should become the exception.

### 6.6 Source-faithful preview adapters

The closer Forge preview gets to actual client rendering, the more review quality improves. Reuse/port source render logic where feasible rather than maintaining a visually similar but semantically drifting clone.

### 6.7 Mobile continuity

The real workflow is mobile-first. Every major project step should support:

- resume after tab eviction;
- large tap targets;
- compact project status;
- drafts without accidental mutation;
- sticky consequence/action context;
- no hover dependency;
- progressive disclosure of technical detail.

---

## 7. Implementation-risk tiers

To avoid turning this product expansion into one giant rewrite, separate capability classes.

### Tier 1 — orchestration/presentation over existing repository evidence

Generally safest to pursue first:

- project/workstream view;
- decision workbench;
- content brief forms;
- mission storyboard/graph presentation;
- shot-list/art readiness projection;
- capture/evidence library;
- previews from repository artifacts;
- quality/advisory checks;
- package readiness view;
- review package composition.

These can deliver large UX value without broadening live write authority.

### Tier 2 — new Forge content adapters / source-procedure support

Requires source-pin/contracts/registry and runner work:

- direct guide reads/writes;
- broader research/capture procedures;
- additional content-class forms/editors;
- source-faithful live-diff adapters;
- direct admin editorial updates for supported classes.

These are Lane A implementation changes and must go through Fable + exact-SHA review.

### Tier 3 — policy or game-source-dependent capability

Do not assume these:

- new native approval-state fields in the game;
- automatic art submission if it conflicts with the standing manual-art ruling;
- unrestricted admin manifest execution;
- new upstream game APIs solely for Forge;
- broad bulk publishing;
- background/automated live writes.

These require explicit director decisions and possibly separate game-source workstreams.

---

## 8. Recommended development sequence

This sequence is a product recommendation; Fable should reconcile it against its architecture/roadmap package rather than treating it as an implementation order already approved.

### Phase A — Make Forge project-aware

1. Workstream/project workspace.
2. Open decisions and blockers.
3. Evidence/resource browser.
4. Human package/readiness summary.

**Why first:** all later studios benefit from continuous project context.

### Phase B — Make missions/events genuinely authorable

1. Brief Intake Studio.
2. Mission/Quest storyboard + semantic graph.
3. Decision gating/profile view.
4. Encounter/AI sub-workspace.
5. graph-derived shot/art requirements.
6. player-experience preview.
7. compile/preflight adapter.

**Why second:** the repository already has mature deterministic tools, so UX can add large value without inventing the domain rules.

### Phase C — Complete the delivery loop

1. Review package.
2. Package composer.
3. verification/readback presentation.
4. content-admin disposition.
5. publication readiness.

**Why:** content creation should not fall back into raw manifests at the final mile.

### Phase D — Add Guide Studio

1. deliberate game-source pin/contract/registry expansion;
2. draft/list/get adapter;
3. structured authoring + source-faithful preview;
4. images/FAQ/related content;
5. review notes and publication.

### Phase E — Add Visual Communication / Infographics

1. define a separate infographic spec/workflow;
2. evidence-bound template model;
3. editable responsive canvas/blocks;
4. export + Guide Studio embed handoff;
5. accessibility/mobile QC.

### Phase F — Deep quality intelligence

Add domain-specific advisory checks, pattern library and post-launch feedback/revision loops after the primary authoring surfaces are stable.

---

## 9. Highest-value channels by content-delivery quality

| Rank | Channel | Primary quality gain | Current foundation | Main dependency |
|---|---|---|---|---|
| 1 | Mission / Quest Studio | earlier structural + narrative quality feedback | very strong | UI/compiler adapter |
| 2 | Project / Workstream Workspace | continuity, fewer dropped requirements/decisions | very strong | repository projection |
| 3 | Package / Delivery Composer | fewer wiring/handoff mistakes | strong | adapter over existing build/validate flow |
| 4 | Decision Workbench | prevents accidental balance/content canon | strong conceptual precedent | UI + durable ruling links |
| 5 | Research / Reuse Library | evidence-driven reuse and consistency | strong | indexing/search/capture adapters |
| 6 | Art Direction / Asset Studio | visual coherence + no asset drift | very strong | orchestration only first |
| 7 | Guide Studio | higher-quality structured documentation | strong current game support | Forge source pin/registry expansion |
| 8 | Quality Intelligence | catches valid-but-bad content | partial rules scattered across workflow | domain lint design |
| 9 | Infographic Studio | improves player comprehension/guide quality | missing lane | new visual-communication spec |
| 10 | Preview Lab | experiential review before live use | partial current renderers | source-faithful preview adapters |
| 11 | Content Admin Queue | makes review/publish human-first | planning/source support | permission/approval decisions |
| 12 | Feedback / Revision Loop | turns releases into learning | workstream model | operational adoption |

---

## 10. Concrete UX principle: generated artifacts should recede

Today many workflows are mentally organized around files:

- sheet JSON;
- storyboard Markdown;
- manifest JSON;
- push ZIP;
- capture JSON;
- art files;
- result bundle.

Those files should remain durable and inspectable, but Forge should organize the normal experience around **human concepts**:

- project;
- quest;
- encounter;
- scene;
- asset;
- guide;
- infographic;
- decision;
- review package;
- release.

The generated file should appear when the user asks "show me the implementation artifact," not because it is the only way to navigate the workflow.

---

## 11. Important non-goals / boundaries

A one-stop shop must **not** mean:

- Forge becomes the canonical owner of doctrine or engine rules;
- Forge copies all repository references into an internal database;
- Forge silently decides missing balance/reward values;
- Forge treats a static preview as live-engine proof;
- Forge hides mutation ambiguity in pursuit of a smooth workflow;
- Forge turns every staff/content-admin user into a manifest operator;
- Forge auto-publishes because the build is green;
- Forge treats existing live content as the desired design merely because it can fetch it;
- Forge merges the text-heavy infographic workflow into a game-art pipeline that deliberately rejects text;
- Forge broadens current live/art authority without an explicit ruling.

The right product is seamless **because context, evidence and handoffs are integrated**, not because authority boundaries disappear.

---

## 12. New user decisions surfaced by this study

These do not need to be answered immediately, but they should eventually become explicit product decisions rather than accidental implementation outcomes.

### D1 — Is Forge officially intended to become the primary content-development workspace?

**Consequence:** determines whether project/authoring workflows are first-class product scope or merely helper utilities around the runner.

**Recommendation:** yes. Preserve repository/source owners underneath it.

### D2 — Should non-game visual communication (infographics/explainers) become an official TNR Tools production lane?

**Consequence:** requires a new spec/workflow because current game-art rules intentionally reject text/UI compositions.

**Recommendation:** yes, if guides/player education are intended to be part of Forge's content mission.

### D3 — Should Guide Studio be a Forge-owned operator/admin surface rather than leaving guide authoring solely in the native game editor?

**Consequence:** requires source-pin/registry/adapters but creates a unified review/provenance flow.

**Recommendation:** yes for authoring/review integration, while reusing source-faithful rendering and game permission enforcement.

### D4 — How much project state may Forge edit in GitHub?

**Consequence:** determines whether Forge only reads workstreams or can update roadmap/design sources through controlled repository writes.

**Recommendation:** allow narrow, schema-validated coordination/source edits through explicit user actions; do not create opaque Forge-only state.

### D5 — What should be the first end-to-end flagship workflow?

Candidates:

- mission from brief to verified hidden build;
- event from staff sheet to review package;
- guide from outline to published article;
- One Perfect Crop-like multi-domain project.

**Recommendation:** use a mission/event vertical slice first because the repository already has the strongest deterministic compiler, storyboard and art requirement pipeline there.

---

## 13. Fable handoff implications

When Fable resumes its Forge Next planning work, this document should be consumed as **product/workflow input**, not as an instruction to rewrite its architecture package.

Fable should specifically reconcile:

1. whether its proposed IA has a stable Content Project/workstream concept;
2. where content-specific authoring studios plug into the execution core;
3. how repository-backed compilers/validators are adapted without duplicating domain logic;
4. whether the architecture can support source-faithful preview adapters;
5. how guide support enters after the source pin/registry moves;
6. what a new infographic/visual-communication pipeline would require outside existing game-art rules;
7. how project evidence/decisions/art/build/readback remain linked end-to-end;
8. which phases can ship as orchestration-only improvements before adding new live procedure support.

No Fable-owned branch should be modified from this ChatGPT design lane. Fable can cite this document at an exact ChatGPT branch SHA as an input.

---

## 14. Bottom line

The highest-quality version of Forge is not merely a safer Builder replacement.

It is a **TNR Content Studio** where:

- a creator begins with intent instead of JSON;
- research and reuse are evidence-backed;
- missions are authored as stories and semantic graphs;
- enemies are designed as encounters rather than id arrays;
- unresolved balance stays visibly unresolved;
- art requirements are generated from the content and tracked through acceptance;
- guides have structured authoring and source-faithful preview;
- infographics become reproducible, data-grounded visual explanations;
- reviewers see player-facing content instead of manifests;
- delivery packages compile deterministically;
- execution retains Forge's strong safety/recovery model;
- fresh readback proves what landed;
- publication remains a separate deliberate act;
- feedback creates the next revision rather than vanishing into chat.

That is a realistic one-stop-shop direction because most of the hard domain knowledge already exists in the repository. The main product challenge is to **surface and connect it without duplicating it**.