# Forge Presentation Studio upgrade plan

**Status:** DRAFT FOR DIRECTOR APPROVAL / LANE A PLAN  
**Prepared:** 2026-09-19  
**Repository:** `perseverance484/tnr-tools`  
**Planning base:** `main@eefefd1afd67111a90c332951a8dd9f83cb99cbd`  
**Normal implementation owner:** Fable / Claude Code  
**Independent design/review owner:** ChatGPT  
**Live-game policy for implementation/review:** ZERO LIVE REQUESTS / ZERO LIVE WRITES  
**Relationship to Forge Next:** separate capability track; does not silently supersede `state/prompt_forge_next_phase1.md`. The current Forge size-pass debt is a prerequisite before another substantial bundled feature.

## 1. Why this plan exists

The Godstorm workstream exposed two different classes of failure:

1. **production-operation failures** in Forge itself, where valid content was blocked or mis-reported;
2. **content-delivery failures** after the live content was correct, where the final explanatory poster mixed stale facts, incomplete rosters and generated stand-ins for real game art.

The first class is now largely repaired and verified in Forge 0.5.0. The second class is not a one-off poster problem. It exposes a missing product layer: Forge can safely execute content packages, but it does not yet produce a **source-bound presentation dossier** that downstream staff/player materials can consume without reconstructing the event from chat memory, planning prose and scattered image files.

The goal is therefore not “add an infographic button.” The goal is to make presentation artifacts deterministic, provenance-aware derivatives of the same evidence system that now protects live writes.

## 2. Session incident analysis

### 2.1 Forge execution / operator failures

| Incident | User-visible failure | Root cause | Current status |
| --- | --- | --- | --- |
| `gameAsset.getAllNames` BAD_REQUEST | asset creates failed before mutation | generic list reader sent `undefined` although current asset route requires an object | fixed/reviewed |
| manifest 50/51 journal collision | corrected manifest could not start because old paused job had “same” hash | execution-significant top-level policy was omitted from manifest identity | fixed/reviewed |
| 18 AI profiles reported drift after landing | successful rules writes remained CONFIRMED | verification compared nested rules textually/key-order-sensitively | fixed/reviewed |
| wrong Android image masters selected | five avatar writes failed inside a live run | picker keyed arbitrary physical files under logical manifest names; mobile filenames/locations were operator-hostile | fixed first with pre-start ledger checks, then repo-backed image packs |
| first image-pack review F1 | a same-size replacement could pass Start after verification | provenance described expected bytes but was not bound to the exact verified File object | fixed/re-reviewed |
| first image-pack review F2 | stale in-flight prep could write into a newer manifest selection | fetch/verify mutated runner state before currency check | fixed/re-reviewed |
| bundle budget raised twice | ~96% of new raw/gzip ceilings consumed | substantial safety logic accumulated inside the single Forge bundle | **open debt: size/consolidation pass required** |

### 2.2 Presentation / content-delivery failures

| Incident | User-visible failure | Root cause |
| --- | --- | --- |
| first poster showed only a representative subset of enemies | event looked like it had five enemies instead of the full 18-AI roster | no canonical presentation model declared whether a roster block meant “sample” or “complete”; composition was improvised from local conversational context |
| narrative path was vague | story explanation did not reflect authored quest writing | summary was composed before reading the current dialogue as the direct narrative source |
| later poster inherited wrong/stale narrative beats | e.g. stage language that belonged to an earlier draft rather than final live dialogue | planning/draft prose and current live captures were blended without evidence precedence being enforced mechanically |
| poster showed old floor cash-outs and chest rewards | materially false reward information | historical reward table from the pre-remap plan was used after all intermediate cash-outs and reward items had been removed |
| “locations” became Upper Court / Binding Dais Active / Released | scene-background variants were presented as event locations | no semantic layer distinguishes **event structure** from **scene art assets**; implementation-level asset names leaked into player-facing IA |
| named AI portraits were redrawn/hallucinated | roster no longer showed the actual game characters | whole poster was passed through a generative image model; image generation treats supplied images as references, not immutable raster layers |
| generated poster text contained rendering/name risk | labels can be misspelled or semantically altered by the image model | text and source art were being synthesized inside the same generative surface rather than rendered deterministically |
| source art was scattered across final pack, recovery ZIP, live captures and old asset archive | “use the real art” still required ad-hoc recovery | no single canonical, queryable presentation asset registry maps content entity -> exact approved pixels -> provenance |
| operator had to repeatedly correct basic facts | design iteration spent on fact recovery rather than visual design | no pre-render factual dossier and no artifact lint comparing the presentation against current canonical evidence |

## 3. Product principles

### P1 — facts are derived, not retyped

Structure, objective counts, encounter order, roster membership, reward values, visibility and current image URLs must come from the selected canonical evidence. A presentation author should not manually type “50 battles” or “125,000 ryo” into a layout spec when Forge can derive it.

### P2 — prose has explicit source anchors

Narrative summaries are editorial, so they cannot be mechanically derived with perfect fidelity. They must therefore cite the dialogue/objective IDs or source passages they summarize. “Story overview” is human-authored text over source anchors, not an untraceable paraphrase.

### P3 — named game art is exact-pixel content

For a named AI, asset, item, jutsu, pyramid or other canonical entity, the presentation path must use an exact source image or exact approved repository derivative. A generative image model may never silently redraw a named entity and present it as the game art.

### P4 — presentation semantics are separate from implementation assets

A scene background is not automatically a “location.” A CDN file is not automatically an “approved hero image.” The presentation model needs semantic concepts such as:

- event / quest / pyramid;
- stage / floor / encounter;
- recurring enemy / keeper / boss;
- location / scene / decorative background;
- current reward / historical reward;
- exact source art / generated decoration.

### P5 — evidence freshness is visible

Every presentation build binds to immutable repository evidence and reports what source each fact and image came from. Historical/planning prose may be consulted, but cannot override current capture/live-state evidence for current-state claims.

### P6 — deterministic rendering for factual artifacts

The production poster/brief/guide renderer must compose text and exact images deterministically. Image generation is optional for clearly decorative art only and must be opt-in, isolated and never used for factual roster/location tiles.

### P7 — presentation output is a derivative, never a new canon

The game records and canonical repository owners remain authoritative. A poster spec does not become a second database for rewards, roster or quest structure.

## 4. Proposed architecture

### 4.1 Presentation Dossier

Add a repository/tool contract that normalizes selected evidence into one source-bound read model.

Conceptual output:

```json
{
  "schema": "tnr.presentation.dossier.v1",
  "subject": {
    "type": "event",
    "title": "Godstorm",
    "components": ["Marrow Vaults", "Stormcourt"]
  },
  "sources": {
    "repoCommit": "<immutable commit>",
    "records": [
      {"path": "harvests/inbox/...", "capture": "...", "entityId": "..."}
    ]
  },
  "structure": {},
  "encounters": {},
  "roster": {},
  "rewards": {},
  "dialogue": {},
  "assets": {},
  "warnings": []
}
```

The dossier is generated from explicit evidence inputs. It does not scrape arbitrary planning files for current facts.

Hard-fact fields should record their provenance pointer internally so an audit can answer “where did this number/name/image come from?”

### 4.2 Presentation Spec

A separate small authoring document describes **how to present** the dossier.

It may contain:

- title/subtitle;
- section selection/order;
- semantic grouping;
- short narrative summaries plus source objective/dialog IDs;
- optional labels such as “Lower pyramid”;
- template choice;
- exact asset selection where more than one approved image exists.

It may **not** redundantly own hard numbers, roster names or reward amounts. Those resolve from dossier keys.

Example:

```json
{
  "schema": "tnr.presentation.spec.v1",
  "dossier": "generated/godstorm.presentation.json",
  "template": "event-poster",
  "story": {
    "marrow": {
      "text": "The player enters ...",
      "sourceObjectives": ["d1_1", "d4_1", "d5_victory"]
    }
  },
  "locations": ["quest:2yvE9...", "quest:OSADdX..."],
  "roster": {"coverage": "all"}
}
```

### 4.3 Exact Asset Registry

Build one normalized asset view for presentation use.

For each entity:

- entity id / name / class;
- current source field (`avatar`, `image`, game asset image, etc.);
- exact repository file when available;
- immutable commit/ref;
- SHA-256;
- dimensions / MIME;
- provenance source (live capture, approved art record, repo-backed image pack);
- status: exact-current / approved-derivative / missing / historical-only.

Important: the registry can point to existing `art/godstorm/`, captured source-art archives and current image-pack data; it should not duplicate their binaries.

If a current remote image must be materialized for deterministic rendering, the tool must download it into a content-addressed cache and verify the recorded hash, following the same trust model as repo-backed image packs.

### 4.4 Deterministic Presentation Renderer

Do **not** implement the production poster as an image-generation prompt.

The renderer should produce at least:

1. deterministic HTML/CSS preview;
2. a stable export format suitable for sharing (SVG or PNG; PDF can follow if low-cost).

Required behavior:

- source images are inserted as exact raster layers;
- text is real text, never generated pixels;
- fixed template geometry with responsive preview;
- no model-generated redrawing of AI portraits;
- repeat build from identical dossier/spec/assets gives identical logical content and, where practical, byte-stable output;
- generated output carries a sidecar metadata file with source commit, dossier hash and asset hashes.

Because Forge is already ~96% of its bundle ceilings, the heavy renderer should **not automatically enter `forge_bundle.js`**. Preferred options, in order:

1. repository-side renderer/tool first;
2. optional separately built/lazy presentation module;
3. core Forge bundle only if the size pass proves sustainable headroom.

### 4.5 Presentation Lint

A build must fail or warn before export when:

**Fatal**
- a required dossier source is missing/unverified;
- `coverage:"all"` roster omits an entity;
- a named entity tile has no exact/approved asset;
- a bound asset hash does not match;
- a displayed hard fact differs from the dossier;
- a current-rewards section resolves to historical/non-current reward data;
- a story summary references nonexistent dialogue/objective IDs.

**Warning**
- narrative source anchors cover only a small fraction of a quest;
- evidence sources are from materially different capture dates;
- a presentation uses an approved derivative instead of the current live image;
- optional decorative art is generative;
- a current subject is hidden/unpublished.

## 5. Semantic extraction rules

### 5.1 Structure

For quests/pyramids derive:

- objective count;
- battle count;
- dialog count;
- terminal count;
- encounter sequence;
- reachable reward nodes;
- predecessor/prerequisite relationships when present.

Do not infer a “floor” solely from a scene background. Floor/stage grouping must come from explicit objective grouping rules or a presentation annotation validated against objective IDs.

### 5.2 Encounter roles

A generic event poster needs role annotations. Support an explicit presentation annotation:

- recurring;
- keeper;
- final boss;
- ascendant/variant.

Annotations identify existing AI IDs and are validated against actual battle nodes. They do not create or rename AIs.

For Godstorm, the golden fixture must prove:

- 4 recurring Marrow archetypes;
- 5 Marrow keepers;
- 4 Stormcourt ascendant archetypes;
- 5 Stormcourt keepers;
- 18 distinct AI records total.

### 5.3 Rewards

Derive rewards from **reachable current objective nodes** only.

For the Godstorm golden fixture the correct current result is:

- Marrow Vaults: one full-clear reward node, 125,000 ryo / 25 tokens / 10 prestige / no reward item;
- Stormcourt: one full-clear reward node, 250,000 ryo / 150 tokens / 60 prestige / no reward item;
- zero intermediate cash-out nodes;
- zero chest/item reward entries.

A regression fixture should deliberately feed the old planning reward table and prove it cannot overwrite current dossier rewards.

### 5.4 Narrative

Narrative content is summarized from the actual quest dialogue selected by source IDs.

For Godstorm, the presentation design should reduce each pyramid to 1–2 sentences while retaining the actual arc:

- Marrow: confinement records -> failed silence/light/binding machinery -> divided threshold / stair upward;
- Stormcourt: tribunal and weather suppression -> circling storm and binding instruments -> Sovereign Echo / binding broken.

No phrase from a stale draft becomes eligible merely because it sounds better.

### 5.5 Locations

A presentation-level “location” is a semantic content subject, not an image filename.

For the Godstorm golden fixture the top-level locations are exactly:

- Marrow Vaults;
- Stormcourt.

Upper Court and Binding Dais are scene/background variants and may appear as artwork captions only if the spec explicitly asks for scene detail.

## 6. Forge/operator UX concept

Long-term destination name is open; working name: **Presentation Studio**.

### Core flow

1. Choose subject / evidence package.
2. Forge shows **Source lock**:
   - exact repository commit;
   - records/captures selected;
   - freshness/status.
3. Generate/view dossier.
4. Choose a template.
5. Edit only presentation-owned fields:
   - title/subtitle;
   - short narrative summary;
   - semantic group labels;
   - optional decorative choices.
6. Exact asset coverage shows:
   - 18/18 roster art ready;
   - 2/2 location art ready;
   - no substitutions.
7. Preview.
8. Run presentation lint.
9. Export HTML/SVG/PNG plus provenance sidecar.

### Mobile-first requirements

- no file picker for repo-bound presentation assets;
- no drag-and-drop requirement;
- asset rows identify entity, source and readiness without exposing filesystem complexity;
- one “Resolve assets” action;
- roster completeness as a count;
- errors state exactly which entity/source is missing;
- export usable from Android without requiring desktop dev tools.

## 7. Phased implementation plan

### Phase P0 — Forge size/consolidation prerequisite

**Goal:** recover sustainable bundle headroom before adding another substantial feature.

Fable should audit:

- duplicated explanatory comments that can move to docs without harming safety;
- dead exports / unreachable helpers;
- duplicated UI strings/data structures;
- bundleable modules that are tooling-only and should never be in runtime;
- opportunities to keep Presentation Studio heavy code outside the core bundle.

No behavior change is the default. Any behavior-affecting refactor is independently reviewable.

Acceptance:

- existing 418+ Forge tests green;
- checked bundle reproducible;
- no safety gate weakened;
- report measured raw/gzip before/after;
- establish a new ratchet from the reduced product, not by simply raising the ceiling again.

### Phase P1 — Dossier + lint foundation

**Implementation target for the first Fable handoff.**

Add repository-side modules/tools only unless a tiny Forge action is clearly justified:

- presentation dossier schema/model;
- evidence loader for explicit committed result/capture sources;
- structural/roster/reward extraction;
- narrative source-anchor validation;
- exact-asset registry resolution;
- presentation spec parser;
- presentation lint;
- Godstorm golden fixture.

No renderer UI yet.

Acceptance:

- no game/network request required by tests;
- current Godstorm fixture generates the correct 2-pyramid / 50-battle / 18-AI / 10-keeper / current-reward facts;
- old cash-out/chest reward data cannot contaminate the current dossier;
- `coverage:"all"` catches a missing AI;
- missing real art is fatal when exact art is required;
- scene-background names cannot become top-level locations without explicit presentation semantics;
- story source IDs must exist in selected current quest records.

### Phase P2 — deterministic renderer

Add HTML/CSS and one stable export.

Start with two templates:

- `event-poster`;
- `staff-brief`.

The renderer consumes only dossier + spec + exact assets.

Godstorm acceptance artifact:

- two top-level locations only;
- all 18 exact AI portraits;
- one compact story blurb per pyramid;
- encounter format “4 normal fights -> 1 keeper, repeat for five floors”;
- current full-clear rewards only;
- no historical cash-outs/chests;
- no generative redraws of named art;
- names/text rendered exactly.

### Phase P3 — Forge UX integration

After P1/P2 are independently reviewed:

- subject/evidence selection;
- dossier facts;
- asset readiness;
- spec editing;
- preview/export;
- provenance display.

Do not merge this work into Forge Next Phase 1's research registry unless an explicit shared abstraction is reviewed.

### Phase P4 — broader delivery templates

Only after Godstorm proves the contract:

- quest launch poster;
- AI/enemy roster sheet;
- jutsu/item guide;
- event staff packet;
- player guide.

Avoid building a generic arbitrary page designer. Templates should encode common TNR content-delivery jobs and preserve validation.

## 8. Godstorm golden test contract

The first end-to-end fixture should bind to the verified repository evidence from the completed workstream.

Expected facts:

- event: Godstorm;
- top-level structures: Marrow Vaults, Stormcourt;
- 25 battles each / 50 total;
- 5 keeper fights each / 10 total;
- encounter cadence: 4 recurring/ascendant fights then keeper, repeated five times;
- 18 distinct AI records;
- complete named roster;
- exact approved/current AI art for every roster entry;
- Marrow full clear: 125000 ryo, 25 tokens, 10 prestige, no item;
- Stormcourt full clear: 250000 ryo, 150 tokens, 60 prestige, no item;
- zero intermediate cash-outs;
- story summary anchored to current dialogue;
- current state hidden/unpublished is available as provenance/status, not necessarily poster copy.

Negative fixtures must include:

- old floor cash-out/chest table;
- missing one keeper;
- swapped AI image;
- same-size wrong image;
- scene background mislabeled as event location;
- stale dialogue objective id;
- historical Tower/Dawnless wording.

## 9. Review priorities

ChatGPT independent review should attack:

1. **source precedence:** can stale plan data overwrite current capture facts?
2. **completeness:** can a poster claim “roster” while silently omitting AIs?
3. **asset identity:** can a named entity display pixels not bound to its exact asset?
4. **semantic leakage:** can scene assets become event concepts automatically?
5. **narrative traceability:** can summary text exist with no current-dialog anchor?
6. **renderer determinism:** can generative systems alter names/text/character art?
7. **mobile UX:** can the operator build/export without file-system archaeology?
8. **bundle containment:** did Presentation Studio unnecessarily inflate core Forge?

## 10. Explicit non-goals

- no automatic LLM story writing inside Forge in the first implementation;
- no arbitrary WYSIWYG design canvas;
- no generative replacement for missing canonical art;
- no live-game write path;
- no publish action;
- no new content database;
- no automatic promotion of planning documents to current-state evidence;
- no reimplementation of the game UI for the sake of screenshots.

## 11. User-owned decisions

Before P2/P3 integration, the user should settle:

1. preferred product name: Presentation Studio / Delivery Studio / another label;
2. whether exact player/staff artifacts may include optional generated decorative art at all;
3. whether presentation binaries (PNG/SVG) should be committed to the repo or treated as generated deliverables only;
4. which first two templates are highest priority if not `event-poster` + `staff-brief`;
5. whether this track pauses the already-frozen Forge Next Phase 1, or runs as a narrow parallel capability after the size pass.

None of these decisions blocks P0/P1 foundation work.

## 12. Recommended execution order

1. user accepts/adjusts this plan;
2. new ChatGPT design/review session elaborates the Presentation Studio UX/template contract on a ChatGPT-owned branch;
3. Fable performs P0 + P1 on its own implementation branch;
4. ChatGPT independently reviews frozen P0/P1 SHA;
5. Fable corrects accepted findings;
6. after P1 acceptance, Fable implements P2 renderer against the accepted design contract;
7. ChatGPT reviews the Godstorm golden artifact for factual and exact-art fidelity;
8. only then consider P3 Forge UI integration.

The design session and Fable may work concurrently only where branch/file ownership does not overlap. The design agent must not mutate Fable's implementation branch.

