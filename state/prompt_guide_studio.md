# Astra implementation contract — TNR Guide Studio

## Assignment

You are the implementation owner for this task by explicit project-director assignment.

Build a **premium TNR Guide Studio** for players to create polished bloodline/build guides and submit them for staff review. The finished workflow must let a content admin approve a submission and move it into TheNinjaRPG without manually rebuilding prose, mechanics, metadata, or presentation.

This is not an MVP questionnaire and not a generic CMS form. The quality target is: **a player with no HTML or game-data knowledge can produce a guide that feels like the Aerathiel/Night Parade guide series.**

The governing product spec is:

`docs/design/GUIDE_STUDIO_PRODUCT_SPEC.md` on the exact `chatgpt/guide-studio-spec` handoff SHA supplied by the director.

Treat that spec as the product contract. Raise conflicts instead of silently simplifying it.

## Repository/start ritual

Repository: `perseverance484/tnr-tools`.

Before implementation:
1. verify current live `main` and record the exact base SHA;
2. read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CLAUDE.md` if present, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, and `docs/workflows/IMPLEMENTATION_HANDOFF.md`;
3. read the full Guide Studio product spec from the exact ChatGPT handoff SHA;
4. inspect the relevant pinned game source rather than relying on this prompt's summary;
5. work on a dedicated Astra-owned implementation branch/workspace; do not modify `chatgpt/guide-studio-spec`.

This is Lane A application/tooling work. Return an exact frozen SHA for independent review.

## Product outcome

### Player side
The player flow should feel like a guided editorial studio:

**Choose bloodline → receive finished bloodline foundation → choose/explain build → write strategy → preview real guide → submit**

Selecting a bloodline must automatically provide, before the player writes strategy:
- two concise default/general bloodline-description paragraphs;
- premium bloodline hero card/art;
- Bloodline Overview copy/art where configured;
- the **complete bloodline kit**, always rendered regardless of build selections;
- special mechanic modules where required, e.g. Night Parade summons.

Only after that foundation does the player-authored strategy/build guide commence.

The player should never be asked to recreate core mechanics or source official art.

### Staff side
The staff flow should be:

**Submission → rendered review → approve/freeze → game-ready package → explicit one-action import → separate publication decision**

Approval must freeze exactly what was reviewed. The approved artifact should require no manual rewriting before import.

## UX bar

The player-facing experience must feel premium and intentional, not like filling in database fields.

Required UX characteristics:
- mobile-first and excellent at 360px;
- strong bloodline identity and artwork;
- calm progressive disclosure;
- clear distinction between locked TNR-owned foundation and player-authored strategy;
- live or one-tap guide preview using the real renderer;
- local autosave/recovery;
- no hover-only essential controls;
- no generic form-dashboard aesthetic as the primary experience.

Use Aerathiel and Night Parade as renderer/UX acceptance fixtures, not just inspiration.

If your component/schema cannot represent both convincingly, do not generalize further yet.

## Required player authoring model

### Core Bloodline Kit
Separate this completely from the player loadout.

The complete core kit:
- comes from the template/catalog;
- always renders;
- cannot be removed/reordered/rewritten by the player;
- uses official art and normalized mechanics;
- survives an empty or unrelated player loadout.

### Player Build / Loadout
The player chooses jutsu that define their build, including support/external jutsu.

Every selected jutsu gets a prominent inline, autosaved **HOW I USE IT** field.

Do not hide this behind a generic strategy modal.

If a selected jutsu is already part of the core kit, prefer a compact build-reference card with thumbnail/name/`Core kit — see above` plus `HOW I USE IT` rather than duplicating a large mechanics card. External/support jutsu should get the full card.

Player-facing copy should communicate:

**Your full bloodline kit is already included. Choose the jutsu that define your build.**

## Strategy authoring

Do not implement a bland questionnaire.

Use template-driven guide chapters. Default family:
- Build Philosophy
- The Core Loop
- Opening Moves
- Defense & Recovery
- Pressure Windows
- Key Synergies
- Adaptation & Matchups
- Mistakes to Avoid

Templates may rename/reorder/hide/replace these. Night Parade should support bloodline-flavored headings such as `Keep the Gate Open` or `Force the Cleanse`.

A short coaching prompt can appear in the editor but should not render as published prose.

Blank optional chapters do not render.

## Mechanics/data rules

All mechanics come from normalized catalog/template data. Never trust player-entered mechanic values.

Preserve effect target and direction semantics. Do not flatten effects based only on names.

Mandatory regression:

**Kinjutsu: Black Thorn Rose is not an offensive damage effect.**

Guide Studio representation must include:
- self `DAMAGE TAKEN` reduction;
- enemy `HEALING REDUCTION`;
- no offensive `DAMAGE` classification.

Add a fixture/test for this specifically and structure normalization so the same class of target/direction bug is hard to repeat.

## Catalog architecture

Ordinary public authoring must make **zero TNR API requests**.

Generate versioned static catalog snapshots through a separate read-only refresh/build step. The public browser consumes static normalized data only.

At minimum preserve for jutsu:
- ID/name;
- official image URL;
- type/rank;
- action cost;
- range;
- cooldown;
- structured effects including target/direction semantics;
- bloodline relation;
- source version/provenance.

Pin catalog/template versions in every submission.

## Pinned game-source integration facts to verify

Use `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756` as the current design-time compatibility source unless the task is deliberately repinned and the change is reported.

At that source:
- `app/src/server/api/routers/guide.ts` exposes public guide reads and protected content-staff `guide.create` / `guide.update` mutations;
- `guide.create` creates a draft placeholder and returns its ID;
- `guide.update` accepts `{ id, data: GuideArticleValidator }` for an authorized content staff user;
- `app/src/validators/guide.ts` defines the editable guide payload contract;
- `GuideCategories` includes `bloodlines`;
- guide content is HTML-backed and the game has its own rendering/preparation path.

Re-open and verify these source files yourself before implementing export/import compatibility.

## Game-ready export

Approved submissions must generate an immutable export package containing at least:

- `submission.json` — structured player-authored data/provenance;
- `game-guide.json` — exact game-facing payload;
- `content.html` — rendered game-facing guide body;
- `assets-manifest.json` — asset/provenance map;
- metadata containing submission/template/catalog versions and a content hash.

`game-guide.json` must map directly to the current `GuideArticleValidator` shape:
- slug
- title
- subtitle
- excerpt
- seoTitle
- seoDescription
- category
- content
- image
- faq
- sortOrder
- published
- relatedBloodlineId
- relatedItemId
- relatedJutsuId
- sourceUrl
- reviewNotes

For bloodline guides, use `category: "bloodlines"` unless canonical source/director direction changes.

Default approved export to `published: false`. Approval/import is not publication.

The exported guide must be validated against a local mirror/equivalent of the pinned game contract, including slug rules, field lengths, category, content length, and relatedBloodlineId.

Do not assume the richer external preview HTML can be pasted into the game unchanged. Produce a game-compatible HTML profile and prove it against the pinned rendering/validator assumptions.

## Plug-and-play import target

Final product goal: the content admin approves once and does not reconstruct the guide.

Preferred flow:
1. staff approves and freezes artifact in Guide Studio;
2. approved package is retrievable by content staff;
3. a narrow authenticated TNR-side importer/Forge helper consumes `game-guide.json`;
4. one explicit operator click performs the required create/update sequence in the authorized game context;
5. importer reports resulting guide ID and each mutation result clearly;
6. guide remains unpublished until a separate explicit publish action.

The public Guide Studio must never hold a TNR session/cookie/password or call protected game mutations.

Preserve project doctrine: repository/tool access is not authorization to operate the live game. Implement and test the importer with transport mocked/local harnesses. Do not make a live write during implementation.

If the actual TNR-side importer is too risky or architecturally separate for the first pass, still complete the immutable game-ready contract/export and return a precise follow-up integration plan. Do not downgrade the end-state goal.

## Suggested service architecture

Cloudflare remains the intended deployment target:
- Pages for the studio frontend/static catalogs/templates;
- Worker/Pages Functions for submissions/review/export;
- R2 for submissions, immutable approved artifacts, and optional screenshots;
- Turnstile for public submission abuse protection;
- secrets only for staff/Discord integration, never TNR credentials.

You may improve this architecture if you can explain the operational benefit and keep the product/security boundaries intact.

## Required surfaces

At minimum implement/design:
1. premium bloodline/template selector;
2. author/about step;
3. visible locked bloodline foundation;
4. searchable build-jutsu picker;
5. inline per-jutsu `HOW I USE IT` authoring;
6. template-driven strategy chapter editor;
7. optional highlights;
8. real final-guide preview;
9. submit/receipt;
10. staff review queue/detail view;
11. approve/freeze action;
12. game-ready export/download;
13. importer integration or the fully specified thin bridge needed to consume the approved payload.

## Initial templates/fixtures

Implement Aerathiel and Night Parade first.

Neither should be exposed publicly until its template has:
- complete intro;
- hero;
- overview;
- complete bloodline kit;
- required special modules;
- required official assets.

Do not fake missing template content with player-editable placeholders.

## Testing gates

At minimum cover:
- template completeness validation;
- full core kit always renders independent of selected loadout;
- loadout cannot mutate core-kit membership;
- `HOW I USE IT` edit/autosave/restore/preview/submission;
- template-driven strategy chapter rename/reorder/hide behavior;
- blank optional chapters omitted;
- effect target/direction normalization;
- Kinjutsu regression;
- static catalog/version/provenance behavior;
- XSS/text escaping;
- image type/count/size limits;
- 360px mobile smoke;
- player submission server validation;
- approval freeze/immutability;
- deterministic export/content hash;
- `game-guide.json` compatibility against pinned guide contract;
- game-facing HTML compatibility tests;
- admin importer create/update flow with transport mocked;
- proof public authoring makes zero TNR requests;
- proof public service never handles TNR credentials/session data.

## Quality bar / completion definition

Do not declare this complete because the form works.

A release candidate is ready for review when:
- the authoring flow feels like a polished studio;
- Aerathiel and Night Parade both render convincingly;
- a player can produce a high-quality guide easily on mobile;
- core mechanics/art require no player manual entry;
- staff can review the actual final representation;
- approval freezes an immutable artifact;
- the export is contract-valid and import-ready;
- no manual copy-edit/reassembly is required to move approved content into the game;
- live publication remains explicitly operator-controlled.

## Handoff back for independent review

Return:

```text
Repository: perseverance484/tnr-tools
Branch: <Astra-owned branch>
Base: <exact sha>
Head: <exact frozen sha>
Integration target: main @ <verified sha>

Objective:
Changed files/directories:
Out of scope / not begun:

Verification:
- <exact command> — <exact result>

Game-source compatibility:
- studie-tech/TheNinjaRPG @ <sha>
- validator/router/render files checked:
- catalog source/provenance:

Fixture status:
- Aerathiel:
- Night Parade:

Cloudflare/deployment assumptions:
Importer status:
Known debt/deviations:
Unverified browser/live/session items:
Live requests/writes/credentials used: none
```

Freeze the handed-off SHA until independent review returns.