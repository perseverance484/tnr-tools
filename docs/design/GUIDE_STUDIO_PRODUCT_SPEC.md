# TNR Guide Studio — Product Specification v1

**Status:** Direction-locked product/design brief for a standalone player-facing guide authoring site.  
**Hosting:** External to TheNinjaRPG. Cloudflare is the intended deployment platform; deployment/DNS are operator-managed.  
**Implementation owner:** Fable / Claude Code after handoff.  
**Design owner / final acceptance:** project director.  
**Reference guides:** Aerathiel is the series presentation reference; Night Parade demonstrates special-mechanic/summon adaptation.

## 1. Product goal

Let a player create a polished TNR bloodline/build guide without knowing HTML, locating game art, formatting mechanic cards, or touching game tooling.

The target flow is:

**Visit link → select bloodline → enter author name → choose loadout → write strategy → preview → submit**

The result must look like the same guide series as Aerathiel and Night Parade.

## 2. Core ownership model

### TNR-owned series layer — locked
The player does not edit:
- page shell, typography, spacing, responsive behavior;
- hero dimensions and section rhythm;
- global jutsu-card format;
- combat-effect labels and formatting;
- bloodline introduction / overview;
- bloodline kit and special-mechanic cards;
- official game asset selection.

### Bloodline template layer — locked
Each published bloodline template provides:
- bloodline ID, name, hero art, overview art;
- short TNR-written intro;
- official bloodline kit cards;
- special modules when required (for example summons);
- enabled player sections and prompts.

Templates are versioned. A submission records the exact template version used.

### Player layer — editable
The author supplies:
- display name;
- optional one- or two-sentence playstyle summary;
- recommended loadout / support jutsu selections;
- ordering of those selections;
- concise “How I use it” notes;
- rotations and game-plan prose;
- optional combat highlights/screenshots and captions.

**Editorial rule:** mechanics live on cards; strategy explains decisions and interactions. Do not ask the player to retype mechanics already shown by the renderer.

## 3. Series structure

The final guide renderer follows Aerathiel’s rhythm:

1. Two concise bloodline introduction paragraphs.
2. 1600×640 hero.
3. **Bloodline Overview** — one short paragraph + overview infographic.
4. **Bloodline Kit** — one short paragraph + standardized core cards.
5. Transition.
6. **My PvP Loadout** or **Recommended PvP Build** — author credit + 1600×480 build banner + selected loadout/package.
7. Transition.
8. **Rotations & Game Plan** — player strategy.
9. **Combat Highlights** — optional.
10. Concise closing paragraph when supplied.

Night Parade may include a special summon module inside the locked Bloodline Kit without changing the player-facing authoring model.

## 4. Global jutsu-card language

Every jutsu card is rendered by the app, not manually designed by the author.

Standard order:
1. official jutsu image;
2. jutsu name;
3. `ACTION • RANGE • COOLDOWN`;
4. short official/series description;
5. standardized effect rows;
6. divider;
7. `HOW I USE IT`;
8. author’s concise tactical note, when supplied.

Summon cards use the same visual family but show the summon AI portrait.

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

The renderer chooses the label from structured effect data. Authors never type or rename effect labels.

## 5. Primary player flow

### Screen A — Select a bloodline
Show only published Guide Studio templates. Each tile contains:
- bloodline name;
- hero/overview art;
- short identity line;
- `Start guide`.

Aerathiel and Night Parade are the initial exemplars.

### Screen B — About your guide
Required:
- author/display name.

Optional:
- short playstyle summary.

Show plain copy: “Your name appears as the guide author.”

Autosave begins immediately.

### Screen C — Build your loadout
Searchable jutsu catalog with:
- official image;
- name;
- type/rank when useful;
- compact mechanic preview;
- `Add` control.

Selected jutsu:
- appear in a reorderable list;
- render immediately as series-standard cards;
- expose only one author field: **How I use it**;
- can be removed/reordered.

Players never upload jutsu images and never enter AP/range/cooldown/effects manually.

### Screen D — Write your strategy
Use guided prompts, not an empty document.

Default prompts:
- **Build identity** — what is this setup trying to accomplish?
- **Opening / setup**
- **Sustain / defense**
- **Pressure / offensive transition**
- **Key interactions**
- **What to watch for**
- **General game plan**

Templates may rename/hide prompts. Blank prompts do not render.

Provide generous text boxes with live character count and autosave. Do not force players to fill every prompt.

### Screen E — Combat highlights (optional)
Allow a small number of screenshots with captions.
- image upload is only for player-created screenshots/highlights;
- client should resize/compress before submission;
- no official jutsu/bloodline art upload is needed.

### Screen F — Preview
Render the actual guide using the same components as publication.
Provide:
- mobile / desktop preview toggle;
- jump links for sections;
- edit buttons that return to the relevant authoring step.

### Screen G — Submit
Before submission show a concise checklist:
- author;
- bloodline;
- selected loadout count;
- strategy sections completed;
- highlights count.

Button: **Submit guide**

Success state:
- submission ID;
- “Your guide was submitted for review.”
- optional `Edit another copy` / `Start another guide`.

No account is required.

## 6. Autosave and recovery

Use IndexedDB or localStorage for draft data.
- Save after every meaningful edit.
- Display a quiet `Saved on this device` state.
- Restore the unfinished draft on return.
- Never make autosave dependent on network availability.
- Provide `Clear draft` behind an explicit confirmation.
- Phase 2 may add export/import of a draft file for cross-device recovery.

## 7. Static game catalog

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
- structured effects;
- bloodline ID/name where applicable;
- source snapshot timestamp/version.

The catalog builder normalizes effects into the Guide Studio display model; the browser renderer does not interpret raw game mechanics ad hoc.

## 8. Images

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

## 9. Submission data contract

Versioned payload, conceptually:

```json
{
  "schema": "tnrguide/v1",
  "template": {"slug": "night-parade", "version": 1},
  "catalogVersion": "2026-09-13",
  "author": "ShisuiUchiha / Eldy",
  "summary": "...",
  "loadout": [
    {"jutsuId": "65Fic...", "note": "I use this when..."}
  ],
  "strategy": {
    "buildIdentity": "...",
    "opening": "...",
    "sustain": "...",
    "pressure": "...",
    "interactions": "...",
    "watchFor": "...",
    "gamePlan": "..."
  },
  "highlights": [
    {"assetKey": "highlight-1", "caption": "..."}
  ]
}
```

The server adds submission ID and server timestamp. Never trust client-supplied mechanic data.

## 10. Cloudflare deployment architecture

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
- completed strategy sections;
- highlight count;
- submission ID;
- staff review/download link.

The Discord webhook is never embedded in browser code.

## 11. Validation and moderation

Client validation is for usability; Worker validation is authoritative.

Reject or normalize:
- unknown template or version;
- unknown jutsu ID;
- duplicate selections when template disallows them;
- excessive field lengths;
- unsupported file types;
- oversized images;
- too many highlights;
- empty author;
- malformed schema.

All player text is treated as text. Never render it as trusted HTML.

MVP moderation is staff review after submission. No public auto-publishing.

## 12. Staff workflow

1. Submission appears in Discord intake.
2. Staff opens/downloads the structured submission.
3. Staff reviews spelling, readability, guide quality, and duplicate explanation.
4. Minor spelling/formatting cleanup is permitted.
5. Accepted submission is rendered against the same series components/template.
6. Final self-contained HTML is produced for publishing/distribution.

The player’s build, strategic priorities, sequencing, and tactical voice remain attributed to them.

## 13. Mobile and accessibility requirements

Mobile-first:
- usable at 360px width;
- no horizontal page scrolling;
- minimum comfortable touch targets;
- sticky `Back / Next` controls on authoring steps;
- search results and selected loadout remain legible one-handed;
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

## 14. Privacy

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

## 15. MVP acceptance criteria

A new player can, on a phone:
1. open the public site with no account;
2. select Aerathiel or Night Parade;
3. enter an author name;
4. search and add a jutsu without locating/uploading its art;
5. see correct official art and standardized mechanic tags;
6. reorder the loadout;
7. add a per-jutsu usage note;
8. write strategy using guided prompts;
9. leave and return without losing the draft;
10. preview an Aerathiel-series guide;
11. submit;
12. receive a submission receipt;
13. cause a validated intake message to appear in the configured Discord channel.

The deployed app makes **zero game mutations** and ordinary player authoring makes **zero TNR API requests**.

## 16. Out of scope for MVP

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

## 17. Phase 2 candidates

- static searchable item/weapon catalog where guide format expands beyond jutsu;
- R2 mirror/cache of official art;
- shareable private draft links;
- staff review dashboard;
- submission revision requests;
- compare template/catalog version changes;
- automatic final self-contained HTML export after staff approval;
- additional bloodline templates.

## 18. Locked product principle

**Players choose and explain the build. Guide Studio owns presentation and mechanics formatting.**

That is what keeps every submission recognizably part of the Aerathiel/Night Parade guide series.
