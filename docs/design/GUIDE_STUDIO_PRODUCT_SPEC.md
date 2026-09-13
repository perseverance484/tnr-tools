# TNR Guide Studio — Product Specification v2

**Status:** Direction-locked product/design brief for a premium player-facing guide authoring studio with a content-admin approval/import path.  
**Implementation owner for this task:** Astra, by explicit director assignment.  
**Design owner / final acceptance:** project director.  
**Hosting:** External to TheNinjaRPG; Cloudflare remains the intended deployment platform unless Astra identifies a materially better fit.  
**Reference guides:** Aerathiel is the presentation-quality benchmark; Night Parade is the special-mechanic/summon benchmark.

## 1. Product goal

Build a **premium Guide Studio** that makes it easy for ordinary players to create polished TNR bloodline guides that look and read like the Aerathiel and Night Parade guides, without requiring the player to know HTML, game-data structure, image sourcing, effect formatting, or staff tooling.

The studio is not a generic form builder. It is a guided editorial production environment.

The target player flow is:

**Open studio → choose bloodline → receive complete bloodline foundation → choose/explain build → write strategy → preview the real guide → submit**

The target staff flow is:

**Open submission → review rendered guide → approve → generate/import a game-ready guide package without rebuilding anything by hand**

The product is successful when the player mostly contributes judgment and strategy, while the studio handles presentation, mechanics, assets, consistency, validation, and game-delivery formatting.

## 2. Non-negotiable product model

A player must never begin from a blank skeleton.

Selecting a bloodline immediately gives the guide a complete, polished, locked foundation:

1. **General bloodline description** — two concise TNR-owned introductory paragraphs.
2. **Bloodline hero card / hero art** — series-quality visual presentation.
3. **Bloodline Overview** — short TNR-owned overview copy plus overview art/infographic where available.
4. **Complete Bloodline Kit** — every core bloodline jutsu displayed automatically using official art and normalized mechanics.
5. **Special bloodline systems** — summons, companions, unique forms, or other required mechanic modules when applicable.

Only after that foundation does the **player strategy guide** begin.

The player is not responsible for explaining what the bloodline is or reconstructing its mechanics. The player is responsible for explaining how they use it.

## 3. Ownership layers

### TNR / series-owned layer — locked
The player cannot edit:
- page shell and series visual system;
- hero dimensions and composition rules;
- bloodline introduction and overview copy;
- complete bloodline-kit membership;
- official jutsu/bloodline/AI art selection;
- mechanic values and effect labels;
- special-system cards;
- game-export metadata derived from canonical data.

### Template-owned layer — locked
Each published bloodline template supplies:
- bloodline ID and canonical name;
- intro paragraphs;
- hero art;
- overview copy/art;
- complete core-kit jutsu IDs;
- special modules;
- bloodline-specific strategy chapter titles/coaching prompts;
- default guide metadata used at export.

Templates are versioned. A submission records the exact template and catalog versions used.

A template is not public until the full foundation is complete. Do not expose placeholder templates to players.

### Player-owned layer — editable
The player supplies:
- author/display name;
- optional personal build summary;
- selected build/support jutsu;
- preferred order of those selected jutsu;
- a clear **How I use it** note for every selected build jutsu;
- strategy prose;
- optional combat screenshots/highlights and captions.

Mechanics belong to cards. Strategy belongs to the player.

## 4. Core Bloodline Kit and Player Build are different things

This distinction must exist in the schema, UI, renderer, preview, submission, and export.

### Core Bloodline Kit
- Always rendered.
- Comes from the bloodline template/catalog.
- Never depends on player selection.
- Cannot be removed or altered by the player.
- Uses official art and normalized effect data.
- Includes special mechanic modules when required.

### Player Build / Loadout
The player chooses the jutsu that define their recommended build, including external/support jutsu where relevant.

Every selected entry exposes an inline, autosaved **HOW I USE IT** field.

If the selected jutsu already exists in the core kit, the build section should normally use a compact reference treatment rather than duplicate a giant mechanic card:
- official thumbnail;
- jutsu name;
- `Core kit — see above`;
- player `HOW I USE IT` note.

If the selected jutsu is external/support and is not already shown, render the full standard jutsu card plus the player's `HOW I USE IT` note.

Player-facing copy should make this split obvious:

**Your full bloodline kit is already included. Choose the jutsu that define your build.**

## 5. Guide structure

The final guide should follow the editorial rhythm established by Aerathiel and Night Parade:

1. General bloodline introduction.
2. Wide hero card / hero art.
3. **Bloodline Overview**.
4. **Bloodline Kit** — complete, automatic.
5. Special mechanic module if applicable.
6. Editorial transition into player contribution.
7. **Recommended Build / My PvP Loadout** — author credit, selected jutsu, `How I use it` notes.
8. **Strategy / Rotations & Game Plan** — player-authored guide chapters.
9. **Combat Highlights** — optional.
10. Concise closing treatment.

The finished page should feel authored and intentional, not like a list of answered prompts.

## 6. Premium authoring experience

The studio should feel closer to a modern editorial/design product than a survey wizard.

### Visual direction
- Strong bloodline identity at the top of the workspace.
- Large artwork, restrained panels, deliberate typography, strong section hierarchy.
- Avoid dense admin-dashboard aesthetics for the player-facing flow.
- Avoid generic white-card grids where every section has equal visual weight.
- Use progressive disclosure so the screen feels calm even when the guide is rich.
- Subtle transitions/feedback are welcome; do not rely on motion for meaning.
- Mobile quality is first-class, not a reduced desktop version.

### Recommended workspace pattern
Astra may choose the exact layout, but the preferred experience is:
- compact progress/navigation rail;
- focused authoring canvas;
- persistent or easily reachable live guide preview;
- locked bloodline foundation visibly present as completed/owned by TNR;
- player-authored sections visually distinguished as their contribution.

### Player confidence
At every point the user should understand:
- what the studio already knows for them;
- what they still need to contribute;
- what will appear in the final guide;
- whether their work is saved.

## 7. Player flow

### A. Select a bloodline
Show only complete/published templates.

Each bloodline tile should feel premium and useful, with:
- hero/overview visual;
- canonical name;
- concise identity line;
- completion/readiness state if relevant;
- `Create guide` action.

Aerathiel and Night Parade are initial fixtures and quality tests.

### B. About the guide
Required:
- author/display name.

Optional:
- short build/playstyle summary.

Autosave begins immediately.

### C. See your bloodline foundation
Before asking the player for strategy, show a polished read-only summary of what has already been built for them:
- intro;
- hero;
- overview;
- full bloodline kit;
- special mechanic module.

This can be a compact in-studio preview with a `View full preview` action. The goal is to establish that the guide is already substantial.

### D. Build your loadout
Use a searchable static jutsu catalog with:
- official image;
- name;
- rank/type when useful;
- compact normalized mechanic preview;
- `Add to build`.

Selected entries are reorderable and each exposes `HOW I USE IT` inline without requiring a modal.

The studio should make it easy to move between selecting a jutsu and writing the tactical note while context is fresh.

### E. Write the strategy guide
Do not present bland categories or a questionnaire.

Use template-driven guide chapters. Default chapter family:
- **Build Philosophy**
- **The Core Loop**
- **Opening Moves**
- **Defense & Recovery**
- **Pressure Windows**
- **Key Synergies**
- **Adaptation & Matchups**
- **Mistakes to Avoid**

Templates may rename, reorder, hide, or replace them with bloodline-specific chapter language. For example Night Parade can use headings such as **Keep the Gate Open** or **Force the Cleanse** where appropriate.

Each chapter can show a short coaching sentence in the authoring UI, but that coaching text does not render into the published guide.

Blank optional chapters do not render.

### F. Combat highlights
Optional player screenshots with captions.
- resize/compress client-side;
- enforce limits;
- never require player uploads for official game art.

### G. Live preview
Preview uses the same guide renderer as final publication/export.

It must show:
- locked foundation;
- selected build;
- player notes;
- strategy chapters;
- highlights;
- real section rhythm and final typography.

Provide mobile/desktop preview and direct edit navigation.

### H. Submit
Submission checklist should confirm:
- author;
- bloodline/template/catalog versions;
- foundation completeness;
- selected build count;
- missing `How I use it` notes;
- completed strategy chapters;
- highlights.

Submission is for review, never automatic publication.

## 8. Jutsu/effect rendering contract

Every mechanic card is rendered by the studio from structured data.

Typical full-card order:
1. official image;
2. name;
3. action / range / cooldown;
4. short description;
5. normalized effect rows;
6. optional player `HOW I USE IT` section when this card is part of their build.

Effect normalization must preserve effect type, direction, and target semantics.

Standard vocabulary includes at minimum:
- `POWER`
- `DAMAGE`
- `DAMAGE GIVEN`
- `DAMAGE TAKEN`
- `RECOIL`
- `POOL DRAIN`
- `HEAL`
- `POOL HEAL`
- `SHIELD`
- `LIFESTEAL`
- `BUFF PREVENTION`
- `AP STUN`
- `ABSORB`
- `HEALING REDUCTION`
- `STAMINA & CHAKRA COST`
- `SUMMON`

### Required regression: Kinjutsu: Black Thorn Rose
This is not a damage-dealt jutsu in the Guide Studio representation.

Render it as:
- self `DAMAGE TAKEN` reduction;
- enemy `HEALING REDUCTION`.

A regression test must prove that no offensive `DAMAGE` classification is emitted for it under the pinned source/catalog used by the studio.

## 9. Static game catalog

Ordinary public authoring must make **zero TNR API requests**.

Use a versioned static catalog generated from public read-only game data. The pinned game source already exposes read-only jutsu and bloodline listing/query surfaces suitable for a build-time refresh.

Recommended artifacts:
- `catalog/jutsu.vN.json`
- `catalog/bloodlines.vN.json`
- `catalog/catalog-meta.json`
- `templates/<bloodline-slug>.vN.json`

Each normalized jutsu record should preserve:
- canonical ID/name;
- image URL;
- type/rank;
- action cost;
- range;
- cooldown;
- structured effects with target/direction semantics;
- bloodline relation when applicable;
- source snapshot/version metadata.

The browser renderer consumes normalized catalog data; it should not reinterpret raw combat mechanics ad hoc.

## 10. Submission model

Store structured authorship separately from the rendered guide.

Conceptual player submission:

```json
{
  "schema": "tnrguide/v2",
  "template": {"slug": "night-parade", "version": 3},
  "catalogVersion": "...",
  "author": "PlayerName",
  "summary": "...",
  "loadout": [
    {"jutsuId": "...", "howIUseIt": "..."}
  ],
  "strategy": {
    "philosophy": "...",
    "coreLoop": "..."
  },
  "highlights": []
}
```

Do not duplicate mechanic truth from the browser into the submission. The server/render pipeline resolves mechanics from the pinned catalog/template.

## 11. Staff review experience

The content-admin/staff side is part of the product, not an afterthought.

A reviewer should be able to open a submission and see:
- final rendered guide first;
- author/bloodline/submission metadata;
- catalog/template provenance;
- validation status;
- missing or suspicious sections;
- raw player-authored fields only when needed;
- optional review notes.

Required states:
- Submitted
- In review
- Changes requested
- Approved for import
- Imported
- Rejected/archived

Approval must freeze the exact rendered/export artifact so the thing reviewed is the thing imported.

## 12. Game-ready export contract

The core operational goal is **approve once, rebuild nothing**.

The pinned game source `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756` has a native guide article model and protected staff mutations:
- `guide.create` creates a draft guide article for authorized content staff;
- `guide.update` accepts `{ id, data: GuideArticleValidator }` for authorized content staff;
- `GuideArticleValidator` owns the current editable guide payload shape.

Guide Studio must therefore produce a game-ready artifact that maps directly to that contract rather than inventing a second publication format.

### Required approved export
At approval, generate an immutable package containing at minimum:

- `submission.json` — structured player authorship/provenance;
- `game-guide.json` — exact game-facing guide data;
- `content.html` — rendered guide body used by `game-guide.json`;
- `assets-manifest.json` — all referenced official/generated/highlight assets and provenance;
- `README.txt` or machine-readable metadata with submission/template/catalog versions and content hash.

`game-guide.json` must map directly to the current `GuideArticleValidator` fields:
- `slug`
- `title`
- `subtitle`
- `excerpt`
- `seoTitle`
- `seoDescription`
- `category`
- `content`
- `image`
- `faq`
- `sortOrder`
- `published`
- `relatedBloodlineId`
- `relatedItemId`
- `relatedJutsuId`
- `sourceUrl`
- `reviewNotes`

For bloodline player guides, the expected category is `bloodlines` unless the current canonical game contract or director decision changes it.

### Import safety/defaults
- Approved export should default `published: false`.
- Guide Studio approval is not game publication.
- The operator/content admin retains the explicit live-game import/publish action.
- No public player browser receives or stores a TNR session/cookie/credential.

## 13. Plug-and-play content-admin import

Astra should design the implementation so the approved package can be imported with one explicit content-admin operation, with no manual re-entry of guide prose or metadata.

Preferred architecture:

1. Guide Studio review UI approves and freezes the artifact.
2. Content admin downloads/copies the approved import package or opens a signed/private retrieval link.
3. A narrow authenticated TNR-side importer/Forge helper consumes `game-guide.json`.
4. On an explicit operator click, the importer creates a draft guide and updates it with the exact approved payload.
5. The helper reports the created guide ID and mutation results.
6. Publication remains a separate explicit staff action.

The external public Guide Studio must not directly call protected game mutations or hold game credentials.

If adding the TNR-side importer cannot safely fit the first implementation pass, Astra must still finish the immutable `game-guide.json` contract and provide a thin, well-bounded follow-up integration plan. The final product goal remains one-action import.

## 14. Game compatibility evidence

The implementation must test the exported artifact against a local mirror of the pinned game contract rather than merely checking that JSON exists.

At minimum:
- validate `game-guide.json` against a local equivalent of `GuideArticleValidator`;
- enforce current guide slug rules;
- enforce field length limits;
- enforce valid guide category;
- ensure `content` is non-empty and under the game limit;
- ensure `relatedBloodlineId` matches the template bloodline;
- default `published` false;
- verify the rendered HTML is compatible with the game's guide rendering assumptions;
- record the pinned game-source SHA used for compatibility.

Do not silently assume self-contained external-guide HTML can be pasted into the game unchanged. The game-facing renderer/export may need a constrained HTML profile even if the external preview is richer.

## 15. Cloudflare/service architecture

Recommended production shape:
- **Cloudflare Pages** — player/editor/review frontend and static catalog/templates.
- **Worker or Pages Function** — submission/review/export APIs.
- **R2** — submissions, approved immutable artifacts, optional highlights.
- **Turnstile** — public submission abuse protection.
- **Worker secrets** — Discord/staff intake secrets only.

No game credential is stored in the Guide Studio service.

The staff review surface may use a private token/auth layer appropriate to the deployment, but do not expose staff controls by obscurity alone.

## 16. Autosave and recovery

Player drafts save locally after meaningful edits, including every `How I use it` note and strategy block.

Requirements:
- quiet `Saved on this device` feedback;
- restore unfinished draft on return;
- local save cannot depend on network availability;
- explicit confirmed `Clear draft`;
- schema/version migration or graceful invalidation when template/catalog changes.

Cross-device private drafts may be a later enhancement.

## 17. Accessibility and mobile quality

Minimum requirements:
- excellent at 360px width;
- no horizontal page scrolling;
- comfortable touch targets;
- no hover-only controls;
- text inputs remain usable with mobile keyboard open;
- preview defaults appropriately on phone;
- proper input labels;
- keyboard navigation;
- meaningful image alt text;
- sufficient contrast;
- effect meaning does not depend on color alone;
- reduced-motion friendly.

Premium does not mean visually dense.

## 18. Privacy and abuse boundaries

Collect only what the product needs:
- public guide author/display name;
- guide text;
- optional screenshots.

Do not request or store:
- TNR password;
- TNR session/cookie;
- Discord token;
- email or real name unless a later separately-approved feature requires it.

Player text is untrusted text and must never be rendered as trusted HTML.

## 19. Initial fixtures

Aerathiel and Night Parade are not merely examples. They are acceptance fixtures.

The renderer/schema is insufficient if it cannot represent both convincingly:
- Aerathiel tests the standard polished bloodline-guide rhythm.
- Night Parade tests special mechanics, summons, richer kit presentation, and strategy structure.

Astra should use these two to drive component fidelity before generalizing to additional bloodlines.

## 20. Acceptance criteria

A successful first production-ready release allows a new player on a phone to:

1. choose a complete bloodline template;
2. immediately see a polished bloodline description, hero, overview, and full kit;
3. select build jutsu without locating art or entering mechanics;
4. add a clear `How I use it` note to each build choice;
5. write strategy in guide-like chapters rather than generic form categories;
6. leave and return without losing the draft;
7. preview a guide that visibly belongs to the Aerathiel/Night Parade series;
8. submit it for staff review.

And it allows staff to:

9. review the exact final rendered guide;
10. approve and freeze an immutable artifact;
11. receive a `game-guide.json` that conforms to the pinned TNR guide contract;
12. import the approved guide without retyping/reformatting content;
13. keep the imported guide unpublished until the explicit publication decision;
14. identify submission/template/catalog/source provenance after import.

## 21. Testing expectations

At minimum:
- template completeness validation;
- core kit always renders regardless of player loadout;
- loadout cannot mutate core-kit membership;
- `HOW I USE IT` add/edit/autosave/restore/preview/submission;
- strategy-block rename/reorder/hide behavior;
- blank optional chapters omitted;
- normalized effect target/direction tests;
- Kinjutsu: Black Thorn Rose regression;
- static catalog version/provenance tests;
- XSS/text escaping tests;
- image type/count/size limits;
- responsive/mobile interaction smoke;
- player submission server validation;
- immutable approval/export snapshot test;
- `game-guide.json` compatibility tests against the pinned guide contract;
- export content-hash/determinism test;
- admin importer test with the actual live transport mocked;
- proof that ordinary public authoring performs zero TNR API requests;
- proof that no game credentials/session material are handled by the public studio.

## 22. Implementation authority and handoff

Astra owns implementation architecture for this task within these product constraints. Do not modify the ChatGPT design branch during implementation.

Use a dedicated Astra-owned implementation branch/workspace and return:
- exact base SHA;
- exact frozen head SHA;
- changed files;
- exact tests/builds/gates run and results;
- catalog/template generation provenance;
- game-source pin used for export compatibility;
- Aerathiel/Night Parade fixture status;
- Cloudflare/deployment assumptions;
- importer status;
- known debt/deviations;
- browser/live checks not performed.

No live game write is required to implement or test this product. Any eventual importer must preserve the operator-controlled explicit live action.

## 23. Product principle

**The player should feel like they are writing the interesting part of a premium finished guide, not building the guide itself.**

Guide Studio owns the bloodline foundation, mechanics, art, presentation, validation, and delivery format. The player owns the build choices, tactical explanation, and strategic voice. Staff should be able to approve that finished work and move it into the game without reconstructing it.