# TNR Guide Studio — Product Specification v1.1

**Status:** Direction-locked product/design brief for a standalone player-facing guide authoring site.  
**Hosting:** External to TheNinjaRPG. Cloudflare is the intended deployment platform; deployment/DNS are operator-managed.  
**Implementation owner:** Fable / Claude Code after handoff.  
**Design owner / final acceptance:** project director.  
**Reference guides:** Aerathiel is the series presentation reference; Night Parade demonstrates special-mechanic/summon adaptation.

## 1. Product goal

Let a player create a polished TNR bloodline/build guide without knowing HTML, locating game art, formatting mechanic cards, or touching game tooling.

The target flow is:

**Visit link → select bloodline → enter author name → choose build jutsu → explain how the build works → preview → submit**

The experience must feel like authoring an Aerathiel/Night Parade guide, not filling out a generic survey. The player supplies their build choices and tactical voice while Guide Studio supplies the complete bloodline foundation, official mechanics, official art, structure, and series presentation.

## 2. Core ownership model

### TNR-owned series layer — locked
The player does not edit:
- page shell, typography, spacing, responsive behavior;
- hero dimensions and section rhythm;
- global jutsu-card format;
- combat-effect labels and formatting;
- bloodline introduction / overview;
- the complete bloodline kit and special-mechanic cards;
- official game asset selection.

### Bloodline template layer — locked
Each published bloodline template provides the complete guide foundation:
- bloodline ID and canonical name;
- two concise general-description / introduction paragraphs;
- hero art;
- Bloodline Overview copy and overview art/infographic;
- the **complete core bloodline kit**, not a subset chosen by the player;
- special modules when required, such as Night Parade summons;
- enabled player-authored strategy chapters and chapter prompts;
- optional bloodline-specific chapter names or guidance.

Templates are versioned. A submission records the exact template version used.

**Template completeness rule:** a bloodline template is not publishable in Guide Studio until the introduction, overview, core kit, required special modules, and required official assets are present. The public authoring experience must never expose a bare skeleton and expect the player to supply the bloodline explanation.

### Player layer — editable
The author supplies:
- display name;
- optional one- or two-sentence personal build/playstyle summary;
- recommended build/support jutsu selections;
- ordering of those selections;
- a concise **How I use it** note for each selected build jutsu;
- strategy prose inside guide-like chapter prompts;
- optional combat highlights/screenshots and captions.

**Editorial rule:** mechanics live on locked cards; strategy explains decisions and interactions. Do not ask the player to retype mechanics already shown by the renderer.

## 3. Series structure

The final guide renderer follows the visual/editorial rhythm established by Aerathiel and Night Parade:

1. Two concise, template-owned bloodline introduction paragraphs.
2. 1600×640 hero.
3. **Bloodline Overview** — template-owned overview copy + overview infographic/art.
4. **Bloodline Kit** — the full template-owned core kit, always rendered.
5. Special mechanic module when applicable, such as Night Parade summons.
6. Transition.
7. **My PvP Loadout** or **Recommended PvP Build** — author credit + 1600×480 build banner + the player's selected build package.
8. **How I Use It** notes attached to the selected build jutsu.
9. Transition.
10. **Rotations & Game Plan** — player strategy rendered as polished guide subchapters.
11. **Combat Highlights** — optional.
12. Concise closing paragraph when supplied or template-owned.

The complete bloodline explanation therefore exists before the player-authored build layer begins.

## 4. Core Bloodline Kit versus Player Build Loadout

These are separate concepts and must remain separate in the data model and renderer.

### Core Bloodline Kit — automatic and complete
- Every jutsu belonging to the published bloodline kit is automatically displayed.
- Core-kit presence does not depend on player selection.
- Core-kit mechanics, official images, descriptions, and effect rows come from the pinned catalog/template.
- Special bloodline systems are also automatic; for example, Night Parade's summon module belongs here.
- The player does not remove, reorder, rewrite, or manually recreate core-kit mechanics.

### Player Build Loadout — selected by the author
The loadout identifies the jutsu the author actually recommends around the bloodline. It may include bloodline jutsu and external/support jutsu.

Every selected loadout entry must expose an obvious inline field labeled **HOW I USE IT**. This is an acceptance-critical field, not optional UI polish.

Recommended rendering behavior:
- If a selected jutsu is external/support and is not already shown in the core kit, render its full standard mechanic card followed by `HOW I USE IT`.
- If a selected jutsu already appears in the core kit, prefer a compact build-reference treatment: official thumbnail, name, `Core kit — see above`, and the player's `HOW I USE IT` note. This avoids repeating an entire mechanic card while preserving the author's tactical explanation.
- A simpler MVP may repeat the full card for core-kit selections, but it must still preserve the player's `HOW I USE IT` note and must not cause the complete core kit to disappear.

The loadout screen should state plainly:

**Your full bloodline kit is already included. Choose the jutsu that define your build.**

## 5. Global jutsu-card language

Every mechanic card is rendered by the app, not manually designed by the author.

Standard full-card order:
1. official jutsu image;
2. jutsu name;
3. `ACTION • RANGE • COOLDOWN`;
4. short official/series description;
5. standardized effect rows;
6. divider;
7. `HOW I USE IT`, only when the card represents a player-selected build entry;
8. author's concise tactical note.

Core-kit cards shown only as the locked bloodline reference do not require player notes. Summon cards use the same visual family but show the summon AI portrait.

Effect vocabulary is global and machine-rendered:
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

The renderer chooses labels from structured effect data. Authors never type or rename effect labels.

### Target semantics are mandatory
Effect normalization must preserve who an effect applies to. A reduction to self damage taken must not be flattened into generic damage, and enemy healing reduction must not be flattened into damage or healing.

**Director correction — Kinjutsu: Black Thorn Rose:** this jutsu is not a damage effect. Guide Studio must represent it as:
- self `DAMAGE TAKEN` reduction; and
- enemy `HEALING REDUCTION`.

No `DAMAGE` / damage-dealt row or offensive-damage classification may be emitted for Kinjutsu: Black Thorn Rose unless the canonical game record changes and that change is separately reviewed.

## 6. Primary player flow

### Screen A — Select a bloodline
Show only published, complete Guide Studio templates. Each tile contains:
- bloodline name;
- hero/overview art;
- short identity line;
- `Start guide`.

Aerathiel and Night Parade are the initial exemplars.

### Screen B — About your guide
Required:
- author/display name.

Optional:
- short personal build/playstyle summary.

Show plain copy: “Your name appears as the guide author.”

Autosave begins immediately.

### Screen C — Build your loadout
At the top, show a compact locked preview/status for the selected bloodline:
- bloodline name;
- “Full bloodline kit included automatically”;
- optional link/jump to preview the automatic kit.

Then show the searchable jutsu catalog with:
- official image;
- name;
- type/rank when useful;
- compact mechanic preview;
- `Add to build` control.

Selected jutsu:
- appear in a reorderable list;
- render immediately in the build presentation;
- expose a prominent inline **HOW I USE IT** text area on every selected entry;
- autosave the note as the player types;
- can be removed/reordered without affecting the automatic core bloodline kit.

Players never upload jutsu images and never enter AP/range/cooldown/effects manually.

### Screen D — Explain how your build plays
Do not present this as a bland questionnaire. The player is writing the strategic chapters of a finished guide.

Use template-driven `strategyBlocks`, rendered in the authoring UI and final guide as named guide chapters/subchapters. Recommended default set:

- **Build Philosophy** — What does this setup want the fight to become? What is the win condition or identity?
- **The Core Loop** — What sequence or decision loop do you return to when the fight is stable?
- **Opening Moves** — What are the first priorities and why?
- **Defense & Recovery** — How do you survive, reset, stall, cleanse, absorb, or buy time?
- **Pressure Windows** — What tells you it is time to attack, spend resources, or commit?
- **Key Synergies** — Which jutsu, bloodline tools, or interactions make the build work?
- **Adaptation & Matchups** — What opponent behavior or matchup changes the plan?
- **Mistakes to Avoid** — What common sequencing/resource mistakes get the build punished?

These names are defaults, not mandatory generic labels. A template may rename, reorder, or hide blocks to fit the bloodline. Night Parade, for example, may use bloodline-flavored chapter language such as “Keep the Gate Open” or “Force the Cleanse” where that produces a better guide.

The authoring UI may show a short coaching sentence beneath each chapter title, but the final published guide should read as authored prose, not as answered form questions.

Blank optional strategy blocks do not render. Provide generous text areas, live character count, and autosave. Do not force every block to be filled.

### Screen E — Combat highlights (optional)
Allow a small number of screenshots with captions.
- image upload is only for player-created screenshots/highlights;
- client should resize/compress before submission;
- no official jutsu/bloodline art upload is needed.

### Screen F — Preview
Render the actual guide using the same components as publication. The preview must include the automatic foundation even before the player writes anything:
- general bloodline description;
- hero;
- overview;
- complete bloodline kit;
- special mechanic modules;
- then the player-authored loadout and strategy.

Provide:
- mobile / desktop preview toggle;
- jump links for sections;
- edit buttons that return to the relevant authoring step.

### Screen G — Submit
Before submission show a concise checklist:
- author;
- bloodline/template version;
- automatic core-kit completeness status;
- selected build-jutsu count;
- `How I use it` notes completed;
- strategy chapters completed;
- highlights count.

Button: **Submit guide**

Success state:
- submission ID;
- “Your guide was submitted for review.”
- optional `Edit another copy` / `Start another guide`.

No account is required.

## 7. Autosave and recovery

Use IndexedDB or localStorage for draft data.
- Save after every meaningful edit, including each `How I use it` note.
- Display a quiet `Saved on this device` state.
- Restore the unfinished draft on return.
- Never make autosave dependent on network availability.
- Provide `Clear draft` behind an explicit confirmation.
- Phase 2 may add export/import of a draft file for cross-device recovery.

## 8. Static game catalog

The public Guide Studio must **not** call TNR APIs during ordinary authoring.

The pinned game source already exposes public, read-only:
- `jutsu.getAll` — paginated full jutsu records, up to 1000 per page;
- `bloodline.getAll` — paginated full bloodline records, up to 500 per page.

A separate catalog-refresh job creates versioned static snapshots for Guide Studio.

Recommended snapshot artifacts:
- `catalog/jutsu.vN.json`
- `catalog/bloodlines.vN.json`
- `catalog/catalog-meta.json`
- `templates/<bloodline-slug>.vN.json`

For the current catalog size, a full jutsu refresh is approximately two `getAll` pages plus the bloodline pages. Refresh is operator-controlled or scheduled at a conservative cadence. The deployed client reads only the generated static JSON.

Each catalog record should preserve:
- ID;
- canonical name;
- image URL;
- type/rank;
- action cost;
- range;
- cooldown;
- structured effects including target semantics;
- bloodline ID/name where applicable;
- source snapshot timestamp/version.

The catalog builder normalizes effects into the Guide Studio display model; the browser renderer does not interpret raw game mechanics ad hoc.

## 9. Bloodline template contract

A published template should conceptually contain:

```json
{
  "slug": "night-parade",
  "version": 2,
  "bloodlineId": "...",
  "title": "Night Parade of a Thousand Demons",
  "introduction": ["...", "..."],
  "heroAsset": "...",
  "overview": {"copy": "...", "asset": "..."},
  "coreKitJutsuIds": ["...", "...", "..."],
  "specialModules": ["summons"],
  "strategyBlocks": [
    {"key": "philosophy", "title": "Build Philosophy", "coach": "...", "optional": true},
    {"key": "coreLoop", "title": "The Core Loop", "coach": "...", "optional": true}
  ]
}
```

The exact schema is an implementation choice, but these product-level concepts are required. The template, not the player's loadout, owns which jutsu constitute the complete core bloodline kit.

## 10. Images

### Official game art
MVP:
- serve official image URLs recorded in the static snapshot;
- browser preview displays them directly;
- submission stores IDs, not copied image blobs.

Publication renderer resolves IDs against the pinned catalog/template version.

Phase 2 reliability option:
- mirror/cache official guide assets to Cloudflare R2 during catalog refresh.

### Player screenshots
- accepted formats: common browser-safe images;
- resize/compress client-side;
- enforce count and byte limits;
- store only after explicit submission.

## 11. Submission data contract

Versioned payload, conceptually:

```json
{
  "schema": "tnrguide/v1",
  "template": {"slug": "night-parade", "version": 2},
  "catalogVersion": "2026-09-13",
  "author": "ShisuiUchiha / Eldy",
  "summary": "...",
  "loadout": [
    {"jutsuId": "65Fic...", "howIUseIt": "I use this when..."}
  ],
  "strategy": {
    "philosophy": "...",
    "coreLoop": "...",
    "opening": "...",
    "defenseRecovery": "...",
    "pressureWindows": "...",
    "synergies": "...",
    "adaptation": "...",
    "mistakes": "..."
  },
  "highlights": [
    {"assetKey": "highlight-1", "caption": "..."}
  ]
}
```

The submission does **not** need to duplicate the core bloodline kit; the server/publication renderer resolves the complete kit from the pinned template version. The server adds submission ID and server timestamp. Never trust client-supplied mechanic data.

## 12. Cloudflare deployment architecture

Recommended MVP:
- **Cloudflare Pages** — static app and versioned catalog/templates.
- **Pages Function or Worker** — `/api/submit`.
- **R2** — submitted JSON and optional highlight images.
- **Turnstile** — submission abuse protection.
- **Worker secret** — Discord guide-intake webhook URL.

No TNR login, cookie, token, session, or game credential is requested or stored.

Submission flow:
1. Client sends guide payload + optional compressed highlights.
2. Worker verifies Turnstile.
3. Worker validates payload against current schema/template/catalog.
4. Worker creates random submission ID.
5. Worker stores JSON/highlights in R2.
6. Worker posts a compact intake message to the configured Discord webhook.
7. Worker returns receipt ID.

Discord intake should include:
- author;
- bloodline/template;
- loadout count;
- completed strategy chapters;
- highlight count;
- submission ID;
- staff review/download link.

The Discord webhook is never embedded in browser code.

## 13. Validation and moderation

Client validation is for usability; Worker validation is authoritative.

Reject or normalize:
- unknown or incomplete template/version;
- unknown jutsu ID;
- duplicate selections when template disallows them;
- excessive field lengths;
- unsupported file types;
- oversized images;
- too many highlights;
- empty author;
- malformed schema.

Template/build validation must also ensure:
- every published bloodline has a complete locked foundation;
- every `coreKitJutsuId` resolves against the pinned catalog;
- required official assets resolve;
- selected loadout jutsu do not alter the core-kit membership;
- normalized effect rows preserve target semantics.

All player text is treated as text. Never render it as trusted HTML.

MVP moderation is staff review after submission. No public auto-publishing.

## 14. Staff workflow

1. Submission appears in Discord intake.
2. Staff opens/downloads the structured submission.
3. Staff reviews spelling, readability, guide quality, and duplicate explanation.
4. Minor spelling/formatting cleanup is permitted.
5. Accepted submission is rendered against the same series components/template.
6. Final self-contained HTML is produced for publishing/distribution.

The player's build, strategic priorities, sequencing, and tactical voice remain attributed to them.

## 15. Mobile and accessibility requirements

Mobile-first:
- usable at 360px width;
- no horizontal page scrolling;
- minimum comfortable touch targets;
- sticky `Back / Next` controls on authoring steps;
- search results and selected loadout remain legible one-handed;
- `HOW I USE IT` is directly reachable from each selected entry without a hidden modal-only workflow;
- no hover-only controls;
- text areas must not be obscured by mobile keyboards;
- preview defaults to phone width on mobile.

Accessibility:
- real labels for every input;
- keyboard usable;
- meaningful alt text for bloodline/jutsu images;
- sufficient contrast;
- effect meaning must not depend on color alone;
- reduced-motion friendly.

## 16. Privacy

Collect only what is needed:
- author display name;
- guide content;
- optional screenshots.

Do not request:
- TNR password/session;
- Discord token;
- email;
- IP-derived identity beyond normal infrastructure logs;
- real name.

Display name is public-guide attribution and should be treated as publishable input.

## 17. MVP acceptance criteria

A new player can, on a phone:
1. open the public site with no account;
2. select Aerathiel or Night Parade;
3. immediately see that the chosen guide already contains a general bloodline description, hero/overview material, complete core bloodline kit, and any required special module;
4. enter an author name;
5. search and add a build jutsu without locating/uploading its art;
6. see correct official art and standardized mechanic tags;
7. understand that the full bloodline kit remains included regardless of loadout choices;
8. reorder the selected build loadout;
9. add an obvious inline `HOW I USE IT` note for every selected build jutsu;
10. write strategy using guide-like, template-driven chapters rather than generic survey categories;
11. leave and return without losing the draft;
12. preview an Aerathiel/Night Parade-series guide containing both the automatic foundation and the player's authored build layer;
13. submit;
14. receive a submission receipt;
15. cause a validated intake message to appear in the configured Discord channel.

Mechanic regression requirement:
- Kinjutsu: Black Thorn Rose renders self `DAMAGE TAKEN` reduction and enemy `HEALING REDUCTION`, and does not render a damage-dealt classification.

The deployed app makes **zero game mutations** and ordinary player authoring makes **zero TNR API requests**.

## 18. Testing requirements

At minimum:
- renderer/effect-normalization fixtures;
- schema/template completeness validation;
- full-core-kit-always-rendered test independent of loadout selection;
- core-kit versus selected-loadout separation test;
- inline `How I use it` authoring + autosave/recovery test;
- Kinjutsu: Black Thorn Rose regression fixture proving damage-taken reduction + healing reduction and absence of damage-dealt classification;
- jutsu search/add/remove/reorder;
- unknown/stale IDs rejected on submit;
- blank optional strategy blocks omitted from final renderer;
- text escaping/XSS tests;
- image type/size/count checks;
- responsive/mobile interaction smoke;
- submit Worker unit/integration test with Discord transport mocked;
- no TNR mutation routes/imports;
- no TNR credential/session handling.

## 19. Out of scope for MVP

- player accounts;
- editing previously submitted guides across devices;
- public comments/ratings;
- direct publication;
- game account/session integration;
- TNR-domain hosting;
- live loadout import from a player account;
- arbitrary page-layout design;
- freeform HTML/Markdown;
- automatic AI rewriting of player strategy.

## 20. Phase 2 candidates

- static searchable item/weapon catalog where guide format expands beyond jutsu;
- R2 mirror/cache of official art;
- shareable private draft links;
- staff review dashboard;
- submission revision requests;
- compare template/catalog version changes;
- automatic final self-contained HTML export after staff approval;
- additional bloodline templates.

## 21. Locked product principle

**Guide Studio supplies the complete bloodline guide foundation. Players choose and explain their build.**

That is what keeps every submission recognizably part of the Aerathiel/Night Parade guide series while still preserving the player's tactical authorship.
