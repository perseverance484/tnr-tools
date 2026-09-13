# E. Content Admin feasibility and source audit

**Status:** planning evidence, no implementation, no live request, no credential material read. Part of the Forge Next planning package (context and pins in `00_CONTEXT.md`).
**Base:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`; repository line anchors are from that tree. Game anchors are from two read-only checkouts: the Forge pin `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` (written `(pin)`) and TNR head `36c5873b7b6ee5fd3af717008d7c51b0f185b756` (written `(head)`).
**Rulings honoured:** `RUL-2026-09-12-001` (one Quest Studio with subtype adapters) and `RUL-2026-09-12-002` (Forge translates, orchestrates and presents; the repository owns facts and contracts). Nothing here settles a user-owned decision; open items route to `K_USER_DECISIONS.md` in E.12 by id.

Abbreviations, each `docs/design/<file>` at `chatgpt/forge-quest-studio-foundation@824c4d58`, cited as `ABBR:line`: SSC = FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md, CPY = FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md, IDX = FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md, EXP = FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md, WSP = FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md, QS = FORGE_NEXT_QUEST_STUDIO.md, RB = FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md. `CA-nn` and `CC-nn` are the rows of `evidence/admin-feasibility.json`. `W-nn` are rows of `C_WORKFLOW_INVENTORY.md`, `R-nn` of `H_RISK_REGISTER.md`, `P-nn` of the parity matrix (section B), `K-nn` of `K_USER_DECISIONS.md`.

## E.0 Scope

This section answers one question per content class: what can an authorized content administrator do from a same-origin Forge surface, using the admin's own browser session, with **zero change to TheNinjaRPG source**. For each class it records the lifecycle field and its default, what visibility actually gates, how a hidden draft is read, how it is edited, what exact mutation publishes it, what deletes it, whether a preview path exists, what audit the game keeps, which roles are required, the verdict, and what Forge's registry covers today. It also records the cross-cutting facts an admin queue depends on: role discovery, rate limits, audit composition, draft confidentiality, image moderation and concurrency.

What it is not. It is not a permission design (K-03, K-04 stay open), not a queue decision (E.8 is evidence plus options, verdict pending), not an approval-state ruling (K-09), and not authorization for any game-source change (K-10 default is no change). Where the game does not offer something, it is recorded as a dependency or a needs-game-change item in E.11, never as a phase deliverable (IDX §9).

## E.1 Method, checkouts and evidence tiers

1. **Source of the rows.** The per-class rows are the merged output of seven independent readers over the game source, committed as `evidence/admin-feasibility.json` (35 rows: 25 content classes CA-01 to CA-25, 10 cross-cutting CC-01 to CC-10). **The rows are merged and their adversarial per-row verification is still in flight.** No `admin-verdicts.json` existed when this section was written. If a CA row changes under verification, **section E is corrected first** and every other section that cites a CA id second.
2. **Which checkout each fact comes from.** The merged rows were built at head. Every fact this section makes load-bearing for a Forge Next decision (authorization gates, refusal shapes, unhide gates, hidden list filters, permission sets, rate-limit construction, upload middleware, `LOG_TYPES`) was **re-opened at the Forge pin `345d18ac`** for this section and is cited `(pin)`. Facts not re-read at the pin (column shapes in `app/drizzle/schema.ts`, client renderers, routers outside the seven Forge classes) keep the merged reader's head cite and are marked `(head)`.
3. **Evidence tiers** per `docs/00_INDEX.md`: Source-verified (SV), Behaviour-proven (BP), Observed (OBS), Inferred (INF), Assumed. Tiers are never upgraded. Every "Forge could do X" statement in this section is INF about Forge Next and SV only about the procedure it would call. Nothing in this section is browser-proven: no live request was made.
4. **CA row verdict tally as merged** (25 content-class rows, counted from `evidence/admin-feasibility.json`): zero-game-change `YES` on 23 rows and `PARTIAL` on 2 (CA-04 gameAsset bytes, CA-12 sectorMap). Two of the 23 are feasible but do not belong in a Content Admin surface on ownership grounds rather than capability grounds: CA-25 balance knobs and CA-17 ranked-season rewards, both user-owned (`CLAUDE.md` section 10; see K-53). One further step is feasible in the procedures and forbidden by repository law: the gameAsset unhide, which engine law 16c rules must not be built (`docs/ENGINE_LAWS.md:46`). Confidence as merged: high on 10 rows, medium-high on 1, medium on 12, low-medium on 2.
5. **Headline.** For all seven classes Forge touches today plus guide and badge, the full draft to review to edit to publish to delete loop is composed **entirely of procedures that already exist**. There is no publish toggle anywhere in the content routers: publishing is a whole-record `<class>.update` with the lifecycle field set. The only dedicated toggles in the game are `worldMap.publishSectorMap` and `activityStreak.toggleConfigActive`, neither of which belongs to a Forge class.

### E.1.1 What this section did not verify

Stated plainly so that no later phase treats an untested claim as proven. No browser was driven and no live request was made, so every claim about how a procedure behaves **in the admin's session** is Inferred from source. Specifically unverified: that the carrier overlay can reach these procedures with the admin's cookie in a real browser; that a role miss looks the way the resolver says it does over the wire; that the upload completion result is what the client receives; that a paged draft listing stays within the shared rate window in practice; that any preview re-implementation matches the game's own render. Each of these becomes a browser or live smoke item in section I, requiring the user's own action, and none of them is a planning-pass deliverable.

## E.2 Per-class feasibility

Tables E.2a to E.2e cover the nine classes the brief names (CA-01 to CA-09) with one row each; table E.2f compresses the other sixteen staff-managed classes the readers found. Rows share ids across all tables.

### E.2a Lifecycle field, default, and what visibility means

| CA | Class | Lifecycle field and default | What visibility gates: listing or play |
|---|---|---|---|
| CA-01 | jutsu | `hidden` boolean default false notNull (`app/drizzle/schema.ts:1666`, head); `jutsu.create` sets no `hidden`, so the placeholder is born **visible** and is shielded only by `jutsuType 'AI'` (`app/src/server/api/routers/jutsu.ts:391-416`, pin) | both. Listing: `getAll` applies `eq(hidden,false)` only when the client omits `hidden` (`jutsu.ts:2115-2116`, pin). Play: hidden cannot be trained, equipped or evolved into without the staff bypass (head). Hiding force-unequips every owner (`jutsu.ts:816`, pin) |
| CA-02 | item | `hidden` default false notNull (`schema.ts:1428`, head); `item.create` and `item.clone` insert `hidden:true` (head) | both. Listing filter is client-controlled (`item.ts:3420-3421`, pin). Play: cannot be bought, crafted or evolved into; owned copies vanish from inventory reads. Hiding sets `userItem.equipped='NONE'` (`item.ts:599`, pin) |
| CA-03 | bloodline | `hidden` default false notNull (`schema.ts:505`, head); `bloodline.create` inserts `hidden:true` (head) | listing plus roll-pool and registration exclusion. Filter is client-controlled (`bloodline.ts:1313-1314`, pin). **Not** enforced on purchase or swap: a hidden bloodline is still purchasable by id (head). Hiding has no effect on current holders |
| CA-04 | gameAsset | `hidden` default **true** notNull (`schema.ts:81`, head); `gameAsset.create` sets no `hidden`, so a new asset is hidden by DB default (head) | listing only, and only in consumers: battle essentials, `misc.fetchGameAssets`, the client asset picker. `asset.ts` reads never filter and take no `hidden` input at all (grep of `input.hidden` in `asset.ts` returns nothing, pin). A hidden asset referenced by a visible quest still resolves (INF from the absent filter) |
| CA-05 | quest | `hidden` default false notNull (`schema.ts:3622`, head); `quests.create` forces `hidden:true` (head) | play, not reads. Play gate is `!hidden \|\| canPlayHiddenQuests(role)` (head); achievement catalogue and battle essentials require `hidden:false` for everyone. Reads are public with a client-controlled filter (`quests.ts:187`, pin). BP: `harvests/inbox/tnr_results_1788104822853.json` captures 0-6 are `quests.get` bodies with `hidden:true` |
| CA-06 | AI (`userData.isAi`) | **none**. No `hidden` or `published` column. Containment flags only: `isAi`, `isSummon`, `isEvent`, `inShrines`, `inArena` default false (`schema.ts:2393-2397`, head) | containment, not hiding. Reachability is `inArena`, `inShrines`, a quest objective reference, or an active overworld placement. Every AI is listed to everyone through `profile.getAllAiNames` (`profile.ts:444`, pin) |
| CA-07 | AiProfile | none. Activation is `userData.aiProfileId` pointing at the row; id `Default` is the global fallback (head) | n/a. Rules take effect only through the pointer |
| CA-08 | guide article | `published` boolean default false notNull (`schema.ts:5865`, head); `guide.create` inserts `published:false` (head). **Entire class is post-pin** (E.9) | listing and page visibility only, with no gameplay dependency. `/guide/[slug]` returns notFound for an unpublished row **even for staff** (head) |
| CA-09 | badge | none | n/a. A badge is in pickers as soon as it exists; awarding to players is a separate staff action under a different permission (head) |

### E.2b Review read path for hidden rows, and full-record read

| CA | Review read for drafts (role needed?) | Full-record read | Queue feasibility today |
|---|---|---|---|
| CA-01 | **no role**: `jutsu.get`, `jutsu.getAllNames`, `jutsu.getAll {hidden:true, limit<=1000, cursor}` are all public with no role check on the filter (`jutsu.ts:2115-2116`, pin). Only `jutsu.getEvolutions` role-gates hidden children | `jutsu.get {id}` returns the full row and throws NOT_FOUND when absent | paged public list exists; Forge's reader refuses it (E.10) |
| CA-02 | **no role**: `item.get` (returns null, does not throw), `getItemWithCraftingRequirements`, `getAllNames`, `getAll {hidden:true, limit<=500}` (`item.ts:3420-3421`, pin) | prefer `getItemWithCraftingRequirements` when crafting matters; the game's own editor does | same |
| CA-03 | **no role**: `bloodline.get`, `getAllNames`, `getAll {hidden:true, limit<=500}` with **no orderBy** (`bloodline.ts:1313-1314`, pin) | `bloodline.get {id}`, throws NOT_FOUND | paging order is undefined across edits (INF) |
| CA-04 | **no role**, and no way to ask for drafts: `gameAsset.getAll` has no `hidden` input, so a drafts queue must page the whole library and filter client-side | `gameAsset.get {id}`, throws NOT_FOUND | 500 per page against a 60/60s budget |
| CA-05 | **no role**: `quests.getAll {hidden:true, limit<=500}` and `quests.get` are public (`quests.ts:187`, pin). NPC-only quest types are dropped for non-staff; `hideLocation` objectives are rewritten for non-staff | `quests.get {id}` returns the row or **null**, never throws | same |
| CA-06 | **no role beyond sign-in**: `profile.getAllAiNames` is public (`profile.ts:444`, pin); `profile.getAi {userId}` is protected with **no role gate** (`profile.ts:1121`, pin) | `profile.getAi` returns the row plus jutsus and items, or null; protected, so **unlimited** | listing is complete and unfiltered |
| CA-07 | `ai.getAiProfile {id}` is protected and gated: `canChangeContent` or own profile, else it **throws** UNAUTHORIZED (`ai.ts:34-37`, pin). No list procedure exists | same call; ids are discovered through `profile.getAi().aiProfileId` | discovery is per-AI only |
| CA-08 | **staff only**: `guide.getAll {includeDrafts:true}` returns drafts only to a `canChangeContent` viewer; `guide.get` on an unpublished row is NOT_FOUND for everyone else, indistinguishable from missing (head). This is the only in-scope class whose drafts are genuinely confidential | `guide.get {id}`; `getAll` is unpaged and returns full bodies | not at the pin (E.9) |
| CA-09 | **no role**: `badge.get`, `getAll {limit<=500}`, `getAllNames` are public (head) | `badge.get {id}`, throws NOT_FOUND | trivial |

### E.2c Edit, publish and delete

| CA | Edit path and key hazards | Publish path: the exact mutation that flips the flag | Delete path |
|---|---|---|---|
| CA-01 | `jutsu.update {id, data: JutsuValidator}`, protected, **whole record** `.set(input.data)`. Validator is non-strict, so a typo is dropped silently. Role gate at `jutsu.ts:730` (pin) | no toggle. `jutsu.update` with the full record and `hidden:false`. **Unhide gate**: at least one effect needs both `appearAnimation` and `appearSfx`, else a refusal (`jutsu.ts:760-770`, pin). `hidden` is optional in the validator, so omitting it leaves the column unchanged (INF) | `jutsu.delete {id}`, refused when injected by other content, owned by AI users, rewarded by quests, or holding child evolutions (head). No clone procedure |
| CA-02 | `item.update {id, data: ItemValidator}`, whole record. `hidden` is **required** in the validator, so every update must state it. `craftingRequirements` are replaced wholesale. `reward_reputation` is preserved server-side unless `canAwardReputation`, so sent is not stored. Role gate at `item.ts:438-439` (pin) | `item.update` with `hidden:false`. **Unhide gate**: a WEAPON, or a CONSUMABLE that is battle-usable, needs an effect with both `appearAnimation` and `appearSfx` (`item.ts:459-473`, pin) | `item.delete {id}` refused only for child evolutions; it then deletes variants, player copies and imbuements leaf-first and non-transactionally (head). `item.clone` exists, inserts `hidden:true`, writes no audit row |
| CA-03 | `bloodline.update`, whole record. The server **deletes** `rounds` and `friendlyFire` from every effect before diffing and writing (head), so the stored shape differs from the authored shape. Role gate at `bloodline.ts:647` with the refusal at `:687` (pin) | `bloodline.update` with `hidden:false`. **No animation gate** in this router | `bloodline.delete {id}`, refused while non-AI users hold it; no guard for jutsu or item `bloodlineId` references (`bloodline.ts:604-605`, pin) |
| CA-04 | `gameAsset.update {id, data: gameAssetValidator}`, partial for optional keys but effectively whole-record because name, image, frames, speed, type, licence and `onInitialBattleField` are required. The diff reports omitted optional keys as `Deleted` even when the column is untouched (head) | `gameAsset.update` with `hidden:false` plus all required fields. Omitting `hidden` leaves the asset **hidden**, because the column default is true. No gate | `gameAsset.delete {id}`; hard delete of the row only, leaving tag rows and quest scene references dangling (`asset.ts:217-232`, pin) |
| CA-05 | `quests.update {id, data: QuestValidator}`, whole record, plus a `questHistory.questType` sync. Server rewrites: reputation rewards preserved, `opponentAIs` rebound for placement-bound objectives, retyping to `event` bulk-assigns. `hidden` and `consecutiveObjectives` are required booleans. Role gate at `quests.ts:741` with the refusal at `:863` (pin) | `quests.update` with the full record and `hidden:false`. **Unhide gate**: refused unless `content.sceneCharacters` is non-empty **or** every objective has scene characters (`quests.ts:757-770`, pin) | `quests.delete {id}`, cascade over quest history, raid participation, raid thresholds, buffs, placements and attempts; does not scrub player quest trackers (`quests.ts:1003-1036`, pin). `quests.clone` copies `hidden` **as-is**, so a clone of a visible quest is immediately live |
| CA-06 | `profile.updateAi {id, data: insertAiSchema}`, whole merged row plus server stat scaling. Jutsus and items are a **set difference**: anything absent from the payload is deleted, and an undefined list strips the kit. `insertAiSchema` does not omit `role`, `isBanned`, `staffAccount` or `money`, so a content editor can write privileged columns on an AI row (head). Role gate at `profile.ts:1515` (pin) | **no flag to flip.** The closest publish is `profile.updateAi` with `inArena:true` or `inShrines:true`, or referencing the AI id from a quest objective or an overworld placement | `profile.delete {id}` runs the account cascade, writes **no audit row**, and does not scrub quest `opponentAIs` references (`profile.ts:1248-1252`, pin). `profile.cloneAi` copies `inArena` and `inShrines` verbatim |
| CA-07 | `ai.updateAiProfile {id, rules, includeDefaultRules}`, full replace of the rules array, max 20 rules. Editing the `Default` profile needs `canChangeDefaultAiProfile` (`permissions.ts:165`, pin). `ai.createAiProfile` does not link the pointer (`ai.ts:53`, pin) | `ai.toggleAiProfile {aiId}` is the only activate path and it is a **non-idempotent flip**: a second send deactivates (`ai.ts:134-135`, pin) | no delete procedure; the row goes only with the user cascade. No clone: `cloneAi` copies the pointer, not the row |
| CA-08 | `guide.update {id, data: GuideArticleValidator}`, whole record. The server sanitises the HTML and can **reject** the save on a profanity match, and the sanitiser strips classes and most inline styles, so read-back differs from what was sent (head) | `guide.update` with the full payload and `published` true or false. `published` is required, so omission fails validation. No further gate | `guide.delete {id}`, hard delete, no reference checks (head) |
| CA-09 | `badge.update {id, data: BadgeValidator}`, whole record. The validator allows a 512-character description against a 500-character column. Role gate at `badge.ts:78` with the refusal at `:103` (pin) | n/a, no lifecycle. Creation is live in pickers immediately | `badge.delete {id}` cascades player-held badges with no guard (`badge.ts:127-143`, pin) |

### E.2d Preview, audit and roles

| CA | Preview: client renderer, route, or re-implement | Native audit | Roles required |
|---|---|---|---|
| CA-01 | **re-implement.** `/manual/jutsu/[id]` returns notFound for hidden rows (head). The staff editor deep link `/manual/jutsu/edit/<id>` works and is client-gated. A Forge render needs `ItemWithEffects` plus the tag defaults, the HTML sanitiser, the spritesheet convention and rarity frames; it is user-context free except staff icons (head) | `actionLog` on update and delete with a server-computed diff, plus a Discord fan-out; **not** on create. Readable: `logs.getContentChanges {logtype:'jutsu'}` | `canChangeContent` = 12 roles (`permissions.ts:22-36`, pin), excluding USER and the three moderator roles |
| CA-02 | **re-implement**, same family; variant images need `item.getItemVariants` | `actionLog` on update and delete; not on create, clone or variant writes. Readable as `logtype:'item'` | `canChangeContent`; reputation rewards additionally `canAwardReputation` (`permissions.ts:507`, pin) |
| CA-03 | **re-implement**, `ItemWithEffects` bloodline branch | `actionLog` on update and delete; not on create. Readable as `logtype:'bloodline'` | `canChangeContent` |
| CA-04 | **trivial.** Image URL plus a spritesheet canvas for STATIC and ANIMATION, `<audio controls>` for SFX and MUSIC. No public per-asset route exists | `actionLog` on update and delete; not on create. **Not readable**: `gameAsset` is absent from `LOG_TYPES` (pin `app/drizzle/constants.ts:189-202`) | `canChangeContent`; uploads split by slug (E.10) |
| CA-05 | **re-implement, large.** No player-facing renderer is usable: the objective component needs a live tracker and user context, and the picker is server-filtered per user (head). The staff editor has a flow graph, not a player render. A Forge preview means objective cards, a reward block, scene assets through `gameAsset.getSceneAssets`, and a flow graph from `nextObjectiveId` edges | `actionLog` on update and delete; not on create or clone. **Not readable**: `quest` is absent from `LOG_TYPES` (pin) | `canChangeContent`; play-testing hidden quests needs `canPlayHiddenQuests` (`permissions.ts:80`, pin), which **excludes MODERATOR-ADMIN**, a role that can nevertheless save hidden quests; starter quests need `canEditStarterQuests` (`permissions.ts:855`, pin) |
| CA-06 | **partial.** `/username/<name>` renders an AI like a player, and the staff editor shows a status bar and the rule editor. A Forge preview means avatar, level-scaled stats (scaling is server-side), the kit from `profile.getAi` and the rules from `ai.getAiProfile` | `actionLog` on `updateAi` only; **not** on create, clone or delete. Readable as `logtype:'ai'` | `canChangeContent` for write; `profile.getAi` needs only a signed-in session |
| CA-07 | render the rule list; no battle simulation is available client-side | **none.** No `ai.ts` mutation writes an audit row or calls Discord | `canChangeContent` or profile owner; `Default` needs `canChangeDefaultAiProfile` |
| CA-08 | **closest thing to a native preview.** The staff editor has a Preview tab that renders the **unsaved** form content client-side; a Forge preview re-implements the same two functions over the draft (head) | `actionLog` on update and delete, no Discord; not on create. Readable at head (`logtype:'guide'`), **not at the pin**: `LOG_TYPES` gains `guide` only after the pin (pin `constants.ts:189-202` vs head `constants.ts:255-269`) | `canChangeContent` for draft read, create, update, publish and delete |
| CA-09 | trivial: image, name, description | `actionLog` on update and delete; not on create. Readable as `logtype:'badge'` | `canChangeContent` for CRUD; awarding uses a wider permission |

### E.2e Verdict, dependencies, Forge coverage today, drift

| CA | Zero-game-change verdict | Would need a game change (nice to have) | Forge registry and recipe coverage today | Drift pin to head | Conf. |
|---|---|---|---|---|---|
| CA-01 | **YES** for the whole loop | partial hidden toggle; version check on update; audit on create; role-gated hidden reads | covered: create, get, getAll, getAllNames, update, delete in `forge/src/transport/procedures.mjs:24-67`; recipe at `forge/src/runner/recipes.mjs:12-16`. Missing: a delete caller, a paged list (E.10), `logs.getContentChanges`, relations and evolutions reads, a role pre-check | none behavioural: id-schema alias only | high |
| CA-02 | **YES** | as CA-01 plus a delete guard for player-owned copies | covered incl. `clone`; recipe uses `item.get`, not the crafting-aware read, so crafting requirements are not round-tripped (INF) | none: validator byte-identical | high |
| CA-03 | **YES** | none for the loop; the purchasable-while-hidden gap is a server gap | covered; recipe at `recipes.mjs:22-26`. No committed manifest has ever created or edited a bloodline through either tool | none | high |
| CA-04 | **PARTIAL**, and narrower than the procedures allow: record CRUD yes, but **no publish step may be built**. Engine law 16c (`docs/ENGINE_LAWS.md:46`) rules that `gameAsset.hidden` affects listing only, never rendering, that live public quests already render hidden assets, and that "no unhide step is needed at publish and none should be built". The procedure would accept `hidden:false`; the law says the product must not offer it. Bytes are also partial, **bytes** partial, because Forge speaks only the 512 KB `imageUploader` slug (`forge/src/transport/upload.mjs:22`) and never selects the 8 MB background or the audio slugs, which exist server-side | a `hidden` filter on the list input; `gameAsset` in `LOG_TYPES`; a delete guard for referenced assets | covered for CRUD; recipe at `recipes.mjs:27-31` with an anonymous `Placeholder`, so orphans are distinguishable only by snapshot diff. Missing: scene-asset, folder and name-tag reads; other upload slugs; zip packs | none | high |
| CA-05 | **YES** for list, read, edit, publish, clone and delete. No native audit read and no server preview: Forge must own both | `quest` in `LOG_TYPES` or a quest history procedure; a server-side preview endpoint if a true play preview is ever wanted; a partial toggle | covered incl. `clone`; recipe at `recipes.mjs:32-36`. Forge refuses quest edits that re-assert drizzle-only columns pre-send, and five archived quest manifests relied on Builder's `skipPreflight` (section B, W-03) | none: quest validators and libs are zero-diff | high |
| CA-06 | **YES**: CRUD and containment flips are existing procedures, and per-record history is readable | audit on create, clone and delete; omit privileged columns from the AI validator; a draft flag if drafts must be invisible | covered incl. `cloneAi` and the four `ai.*` procedures; recipes at `recipes.mjs:37-49`. Missing: clone and delete callers, `ai.getAiRelations` for a where-used check, `profile.getPublicUsers` | none: 157 validator keys identical | high |
| CA-07 | **YES**: read, edit and toggle all exist; Forge already reads before toggling so it never flips an active pointer | audit rows; an idempotent set-active procedure; NOT_FOUND instead of a 500 on an unknown id | fully covered procedurally; no rule preview UI | none: validator zero-diff | high |
| CA-08 | **YES** at head; **impossible at the pin** (E.9) | none | **zero**: no guide procedure in `procedures.mjs` (grep count 0), no recipe, no field set (`forge/src/runner/validate.mjs:5-6` names six entities) | entirely new after the pin | high |
| CA-09 | **YES**, the simplest class | validator and column length parity; a duplicate guard on awarding | **zero**: no badge procedure, recipe or field set. Adoption is mechanical: three keys and the same placeholder-then-update shape as the six existing recipes | none | high |

### E.2f Other staff-managed classes the readers found

Compressed. None is covered by Forge today; all are candidates only, and several are explicitly user-owned balance surfaces.

| CA | Class | Lifecycle | Publish mechanism | Native audit | Zero-change verdict and note | Conf. |
|---|---|---|---|---|---|---|
| CA-10 | sageMode | `hidden`, create inserts true | `sageMode.update` with `hidden:false`; refusal at `sageMode.ts:268` (pin) | written, **not readable** (absent from `LOG_TYPES`) | YES; drafts are list-hidden from non-staff, the only class besides guide where that holds | med-high |
| CA-11 | skillTree and folders | `hidden`, skill create inserts true | `skillTree.update` with `hidden:false` | **none** | YES for CRUD, but a role miss **throws** UNAUTHORIZED (`skillTree.ts:197,242-243,295-296`, pin), which Forge would misread as a lost session (E.3) | med |
| CA-12 | sectorMap | `status` DRAFT/PUBLISHED/ARCHIVED plus version: the only first-class lifecycle enum in scope | **dedicated** `worldMap.publishSectorMap {id}`; unpublish is `archiveSectorMap` | none | PARTIAL: procedures exist and are cleanly role-gated, but the payload is a Tiled JSON document and there is no edit-in-place; this is a map tool, not a record editor. At the pin the two staff reads throw a plain `Error` (`worldMap.ts:90,191`) | med |
| CA-13 | mapAsset | none | n/a | on update and delete, not readable | YES; trivial preview | med |
| CA-14 | mapTerrain | `protected` flag is a guard, not a lifecycle | n/a | on update and delete, not readable | YES; terrain costs are world balance (user-owned) | med |
| CA-15 | overworldAiPlacement | `isActive` default true | upsert with `isActive` flipped; no toggle | **none** | YES for CRUD; tightly ordered with maps and quests (publish map, place AI, bind quest); pool sync is delete-all then insert without a transaction | med |
| CA-16 | towerDefense character/upgrade | none | n/a | **none** | YES, but every save is immediately live and unlogged: not a safe admin target without Forge-side staging | med |
| CA-17 | rankedSeason | `ended`/`paused`; active is date-derived | n/a | **none** | YES technically; season rewards are balance (user-owned). Input is flat, not the `{id,data}` convention, and carries real Date values | med |
| CA-18 | activityStreakConfig | `isActive`; one active recurring config | **dedicated** `toggleConfigActive {id}` | **none** | YES; `deleteConfig` also destroys player streak progress with no confirmation | med |
| CA-19 | raidDamageThreshold | none | follows the parent raid quest's `hidden` | **none** | YES; belongs inside the quest edit flow, which Forge cannot manage today | med |
| CA-20 | itemVariant | none | follows the parent item (INF) | **none** | YES; delete destroys player unlocks with no guard | med |
| CA-21 | jutsuReskin / bloodlineReskin | none | n/a | on update, reject and delete; readable | PARTIAL: bloodline reskin admin yes; jutsu reskin moderation is owner-scoped at the server, so a cross-user moderation queue is not possible. External moderation sits in the write path | med |
| CA-22 | cannedResponse | none | n/a | none | YES; support tooling, out of content scope | low-med |
| CA-23 | contentBackup | none | n/a | none | YES to **trigger** a snapshot before a risky push; **NO** as a restore mechanism (E.6) | high |
| CA-24 | historical avatar / sound effect | status flag on the generation row | the URL is copied into a content record | none | YES for uploads; generation endpoints are outside Forge's current policy | med |
| CA-25 | gameSetting / damage config / global tavern | n/a | n/a | not read | YES technically; these are direct balance knobs and are **user-owned** (`CLAUDE.md` §10). Recommend excluding them from a Content Admin surface | low-med |

### E.2g The zero-game-change loop as an explicit call sequence

The brief asks what an admin can do without touching TheNinjaRPG code. The answer per class is a sequence of procedures that all exist today. Listing it explicitly makes the claim testable rather than rhetorical, and it is also the shopping list for the registry expansion in E.10. Every step is Source-verified as a procedure; that Forge Next can chain them is Inferred, because no live request has been made.

| CA | Find drafts | Open one | Edit | Publish | Verify | Steps missing from Forge's registry today |
|---|---|---|---|---|---|---|
| CA-01 jutsu | `jutsu.getAll {hidden:true}` | `jutsu.get` | `jutsu.update` (fetch-merge) | same call, `hidden:false`, after the animation gate is satisfied | `jutsu.get` read-back plus `logs.getContentChanges {logtype:'jutsu', relatedId}` | paged list support; the history read; relations and evolutions |
| CA-02 item | `item.getAll {hidden:true}` | `item.getItemWithCraftingRequirements` | `item.update` | same call, `hidden:false`, after the weapon and consumable gate | read-back plus history | paged list; the crafting-aware read; variants; history |
| CA-03 bloodline | `bloodline.getAll {hidden:true}` | `bloodline.get` | `bloodline.update` | same call, `hidden:false`, no gate | read-back plus history; expect the server to have stripped two effect keys | paged list; history |
| CA-04 gameAsset | `gameAsset.getAll` then filter client-side | `gameAsset.get` | `gameAsset.update` with every required key | same call, `hidden:false` | read-back only: there is no readable history for this class | paged list; scene, folder and tag reads; the larger upload slugs |
| CA-05 quest | `quests.getAll {hidden:true}` | `quests.get` | `quests.update` (fetch-merge) | same call, `hidden:false`, after the scene-character gate | read-back only; Forge captures are the history | paged list; scene assets and placement names for pickers |
| CA-06 AI | `profile.getAllAiNames` (no draft filter exists) | `profile.getAi` (protected, unlimited) | `profile.updateAi` with the **whole kit re-sent** | `profile.updateAi` with `inArena` or `inShrines`, or a quest or placement reference | read-back plus `logs.getContentChanges {logtype:'ai'}` | where-used relations; the history read |
| CA-07 AiProfile | `profile.getAllAiNames` exposes the pointer column | `ai.getAiProfile` | `ai.updateAiProfile` (full rule replace) | `ai.toggleAiProfile` only when the pointer is null | read-back; **no history exists at all** | nothing procedural |
| CA-08 guide | `guide.getAll {includeDrafts:true}` (staff only) | `guide.get` | `guide.update` | same call, `published:true` | read-back plus history at head; expect sanitiser differences | the entire class (E.9) |
| CA-09 badge | `badge.getAll` | `badge.get` | `badge.update` | n/a | read-back plus history | the entire class, mechanically |

Two observations the sequence makes visible. First, **publish and edit are the same call** on every class with a lifecycle flag, so a publish is exactly as risky as an edit and inherits every whole-record hazard in E.2c; the separation between them is a Forge-side idea, not a server one. Second, the only step that is missing across **every** class is paged list support in the cached reader, which is why a draft queue is the first capability gap rather than a UI decision.

## E.3 Role model and the authorization-denial signal audit

**Role model.** There is no role middleware anywhere. `publicProcedure` is rate-limit plus Sentry (`app/src/server/api/trpc.ts:211-213`, pin); `protectedProcedure` is authentication plus Sentry and carries **no limiter** (`trpc.ts:230-232`, pin). Every content role check therefore runs **inside the resolver**, against `canChangeContent(user.role)`, a 12-role list (`app/src/utils/permissions.ts:22-36`, pin). Role lives only in `userData.role`; it is not in a Clerk claim (CC-01). The practical consequence for Forge Next: the surface can only ever **narrow** what the game allows, never widen it, and it cannot know the role without asking (E.10).

| Permission (pin) | Roles | What it unlocks in scope |
|---|---|---|
| `canChangeContent` (`permissions.ts:22-36`) | CONTENT, BALANCE, HEAD_CONTENT, HEAD_BALANCE, EVENT, HEAD_EVENT, EVENT-ADMIN, OWNER, CODING-ADMIN, MODERATOR-ADMIN, CONTENT-ADMIN, CODER | create, edit, publish, clone and delete on every class in E.2, plus the staff-only draft reads on guide, sage mode, evolutions and sector maps, plus the admin upload slugs. Excludes USER, HEAD_MODERATOR, MODERATOR, JR_MODERATOR |
| `canPlayHiddenQuests` (`permissions.ts:80`) | the same list **minus MODERATOR-ADMIN** | play-testing a hidden quest. The asymmetry matters: a MODERATOR-ADMIN can save and publish a hidden quest but cannot play it, so the admin surface should say so rather than offering a test link that fails |
| `canEditStarterQuests` (`permissions.ts:855`) | OWNER, CONTENT-ADMIN | editing starter and tutorial quests; a narrower gate inside `quests.update` that refuses with its own message |
| `canAwardReputation` (`permissions.ts:507`) | MODERATOR-ADMIN, OWNER, CODING-ADMIN, CONTENT-ADMIN, EVENT-ADMIN | writing reputation rewards on items and quests. Without it the server **silently preserves** the stored value, so the sent payload and the stored record differ and the UI must show the post-save read |
| `canChangeDefaultAiProfile` (`permissions.ts:165`) | OWNER, CODING-ADMIN, CONTENT-ADMIN, EVENT-ADMIN | editing the global `Default` AI rules, which is a game-wide balance change and therefore user-owned |
| `canControlBackups` (`permissions.ts:66`) | OWNER, CODING-ADMIN, CONTENT-ADMIN, EVENT-ADMIN | creating a content backup snapshot and reading the backup list |

The practical shape of a role pre-check is therefore not a single boolean. An admin surface wants `canChangeContent` to decide whether to render actions at all, and the four narrower permissions to decide whether specific fields and affordances are offered.

**The denial-signal audit that K-34 and `U-E-01` asked for.** Per admin-relevant procedure at the pin, what does a role miss return? The content mutations all answer with `baseServerResponse {success, message}` at HTTP 200 (`trpc.ts:244-247`, pin), built by `errorResponse` (`trpc.ts:250-252`, pin). There is no error code on that path, so the only candidate signal is the **message string**. The audit below asks the stricter question: can that message be produced by anything other than a role miss on the same path?

| Procedure (pin) | Role check | Refusal shape and message | Role-only? |
|---|---|---|---|
| `jutsu.update` | `jutsu.ts:730` | 200 `success:false`, `"Not allowed"` | **yes**: banned, not-found, name and tutorial guards all precede it (`jutsu.ts:723-729`) |
| `jutsu.delete` | `jutsu.ts:442` | 200, `"Not allowed"` | **yes** (`jutsu.ts:437-441`) |
| `item.update` | `item.ts:438` | 200, `"Not allowed to edit item"` (`item.ts:439`) | **yes** (`item.ts:433-436`) |
| `item.delete` | `item.ts:340` | 200, `"Not allowed to delete item"` (`item.ts:341`) | **yes** (`item.ts:335-338`) |
| `item.clone` | `item.ts:275` | 200, `"Not allowed"` | **yes** (`item.ts:272-274`) |
| `bloodline.update` | `bloodline.ts:647` | 200, `"Not allowed to edit bloodline"` (`bloodline.ts:687`) | **yes** (`bloodline.ts:642-646`) |
| `bloodline.delete` | `bloodline.ts:604` | 200, `"Not allowed to delete bloodline"` (`bloodline.ts:605`) | **yes** (`bloodline.ts:600-603`) |
| `quests.update` | `quests.ts:741` | 200, `"Not allowed to edit quest"` (`quests.ts:863`) | **yes**: `"Quest not found"` is returned earlier (`quests.ts:719-721`) |
| `quests.delete` | `quests.ts:1007` | 200, `"Not allowed to delete quest"` (`quests.ts:1036`) | **yes** (`quests.ts:1001-1006`) |
| `quests.clone` | `quests.ts:946` | 200, `"Not allowed to clone quest"` (`quests.ts:947`) | **yes** (`quests.ts:941-945`) |
| `profile.updateAi` | `profile.ts:1515` | 200, `"Not allowed"` | **yes** (`profile.ts:1511-1514`) |
| `profile.cloneAi` | `profile.ts:1197` | 200, `"Not allowed"` | **yes** (`profile.ts:1195-1196`) |
| `badge.update` | `badge.ts:78` | 200, `"Not allowed to edit badge"` (`badge.ts:103`) | **yes** (`badge.ts:74-77`) |
| `gameAsset.update` | `asset.ts:163` | 200, `"Not allowed to edit gameAsset"` (`asset.ts:191`) | **no**: the guard is `if (entry && canChangeContent(...))` with no prior not-found check, so a missing asset returns the same message |
| `gameAsset.delete` | `asset.ts:217` | 200, `"Not allowed to delete gameAsset"` (`asset.ts:232`) | **no**, same construction |
| `badge.delete` | `badge.ts:127` | 200, `"Not allowed to delete badge"` (`badge.ts:143`) | **no**, same construction |
| `profile.delete` (AI) | `profile.ts:1248` | 200, `"Not allowed to delete AI"` (`profile.ts:1252`) | **no**: missing user, non-AI target and role miss share the message |
| `ai.createAiProfile` | `ai.ts:53` | 200, `"Unauthorized"` | denial, but conflates role miss with not-owner |
| `ai.updateAiProfile` | `ai.ts:78-79` | 200, `"Unauthorized"` | same |
| `ai.toggleAiProfile` | `ai.ts:134-135` | 200, `"Unauthorized"` | same |
| `ai.getAiProfile` | `ai.ts:34-37` | **throws** `TRPCError UNAUTHORIZED` | distinguishable by code, but see the hazard below |
| `skillTree.create/update/delete` | `skillTree.ts:197,242-243,295-296` | **throws** `serverError("UNAUTHORIZED", ...)` | same hazard |
| `worldMap.listSectorMaps` / `getSectorMapById` | `worldMap.ts:90,191` | **throws a plain `Error`** at the pin, surfacing as INTERNAL_SERVER_ERROR; at head these become a FORBIDDEN server error | not usable as a signal at the pin |
| `guide.*` | n/a at the pin | class does not exist at the pin (E.9); at head the shape matches the `errorResponse` family | n/a |

**Hazard.** Forge maps the tRPC code `UNAUTHORIZED` to the class `SESSION` (`forge/src/transport/outcome.mjs:62`) and `AuthState.refuse()` moves the whole session to SIGNED_OUT (`forge/src/transport/auth.mjs:199-201`). So the two families that **do** carry a machine-readable code are exactly the ones Forge would mis-report as a lost session. A role pre-check is required before `ai.getAiProfile` or any `skillTree.*` path is ever adopted (CC-01, R-26).

**Conclusion for K-34 and the NOT AUTHORIZED lamp (evidence, not a ruling).**
1. A role denial is **per procedure, not per session**. The same signed-in account is authorized for some paths and not others, and the game answers each call independently. A **fifth session-lamp state** therefore has no source behind it: nothing in the transport can put the session into a "not authorized" condition, and D2.2 makes the lamp conditional on exactly this audit (`D_VISUAL_SYSTEM.md` §D2.2 `session_lamp`).
2. A **per-action** denial label is supported for the thirteen paths marked role-only above, and only through a **string match**, because the code field is absent. That is the same prose-coupling failure mode as R-21: a message reworded upstream silently downgrades the label. It is defensible only if the mapping is a generated table anchored to the pin and re-checked by the existing drift tools at every phase gate.
3. For the four conflated paths and the three `"Unauthorized"` paths, the label would be wrong some of the time and must not be rendered.
4. The robust mechanism is the **role pre-check** (E.10, CC-01): read the role once per session, disable the actions the role cannot perform, and re-check on send. That satisfies the intent of SSC:291-295 without inventing a signal, and it makes CPY:384-396 renderable as a **pre-emptive** state ("this account cannot publish") rather than a post-hoc classification.
5. Consequence if the director rules the lamp out: the `NOT AUTHORIZED` lamp, its banner construction and the `classifyError` FORBIDDEN class leave the proposal, and the four-state lamp of `forge/src/transport/auth.mjs:54` stands unchanged. **The decision stays with K-34.**

## E.4 Publication axis per class

Three axes exist, and they are not interchangeable. A single generic "Publish" action across classes would be a lie on the third.

| Axis | Classes | What publishing is | What a dependency read before the flip can check |
|---|---|---|---|
| `hidden` boolean | jutsu, item, bloodline, quest (CA-01, CA-02, CA-03, CA-05), plus sageMode and skillTree. **gameAsset is excluded by engine law 16c** (`docs/ENGINE_LAWS.md:46`): its `hidden` is listing only, hidden assets already render in live quests, and no unhide step may be built | a whole-record `update` with `hidden:false`. Two of the five carry an **unhide gate** that refuses after the whole record has been sent: jutsu and item need an effect with `appearAnimation` and `appearSfx`; quest needs scene characters | feasible and cheap: the gate inputs are inside the record Forge has already read, so the gate can be checked **before** the send and shown as a blocker rather than a refusal |
| `published` boolean | guide (CA-08) only | a whole-record `update` with `published:true`. `published` is required in the validator, so it can never be omitted by accident. **"Published" here means page visibility only**: there is no gameplay consequence, and the article becomes reachable at `/guide/<slug>`. Unpublishing hides it from staff too, because the public route refuses drafts for every role | slug uniqueness and the profanity gate are both server-side and can reject the save; a slug change breaks old URLs with no redirect |
| none | AI (CA-06), AiProfile (CA-07), badge (CA-09), and most of E.2f | **containment by references.** An AI is reachable only through `inArena`, `inShrines`, a quest objective that names its id, or an active overworld placement. "Publish" is whichever of those the package intends; "unpublish" is the reverse plus a where-used check | `ai.getAiRelations` answers where-used for quests, and `overworldAi.getPlacementsForAi` for placements. Neither is in Forge's registry today, so the check is a registry expansion, not a game change |

Two consequences for the admin surface. First, the publish control must be **per class**, named by what it actually does ("Make visible", "Publish article", "Add to arena"), because K-07 asks which operations are eligible for a few-tap publish and the answer differs by axis. Second, a package publish (K-07 option b) is only meaningful on the first axis: a quest plus its assets is a set of `hidden` flips, while an AI joins the package as a reference edit.

## E.5 Preview strategy per class (brief section 12, question 9)

The game has **one** usable preview affordance for drafts, and it belongs to guides. Every other class 404s its public detail page for a hidden row, and the staff editors are React pages that cannot be embedded. So Forge's preview is a re-implementation in every case, and the honest strategy is tiered by cost.

| Tier | Classes | Strategy | Cost and risk |
|---|---|---|---|
| Trivial | gameAsset, badge, mapAsset, mapTerrain | render the asset directly: image plus a spritesheet canvas from `frames` and `speed`, or an audio element for SFX and MUSIC | low. The only risk is CDN reachability, and the game's own CSP already allows the hosts |
| Moderate | jutsu, item, bloodline, sageMode | re-implement the shared effects card from the full record read. It is user-context free except staff-only icons, so a faithful render is possible without a session-dependent path | medium. The tag-default logic and the HTML sanitiser must be mirrored, and drift in either makes the preview lie |
| Moderate | AiProfile | render the rules as condition to action rows | low, but no battle simulation is possible client-side |
| High | AI | avatar, kit and rules are direct reads; **stats are scaled server-side**, so a preview must either re-implement the scaling or show the post-save row | medium. Showing the post-save row is the safer default and matches the whole-record read-back Forge already does |
| High | quest | full re-implementation: objective cards, reward block, scene background and characters through a scene-asset read, and a flow graph from the objective edges. The player components are unusable (live tracker plus user context) | **highest**. This is the class the active workstream publishes, which is why it is also the class where a preview earns the most |
| Native-adjacent | guide | the game's own editor previews unsaved content client-side with two pure functions. Forge can mirror the same two functions over the draft | low once the class exists at all (E.9) |
| Not attempted | sectorMap, overworld placements, towerDefense | a Tiled renderer or a world-map render is out of proportion to the value | n/a |

A preview must carry its provenance. `D_VISUAL_SYSTEM.md` §D2.3 already specifies **PreviewFrame** with a line stating that the preview reflects the live hidden record read at a stated time; that is the correct guard against a preview being mistaken for the live page.

## E.6 Audit and history composition

Four different histories exist. Each answers a different question, and none of them answers all three of "what changed", "who did it" and "can it be undone".

| Source | Answers | Covers | Gaps that matter |
|---|---|---|---|
| Game `actionLog` through `logs.getContentChanges` | what changed and who did it, per record, as server-computed diff strings | at the pin: ai, badge, bloodline, item, jutsu (`app/drizzle/constants.ts:189-202`, pin). At head, also guide | **quest, gameAsset and sageMode rows are written but unreadable**, because those table names are absent from the enum the read procedure accepts. Nothing is logged on **create** or **clone** anywhere, so placeholder minting is invisible to the game |
| Game `content_backups` | a whole-table SQL snapshot | bloodline, jutsu, item, ai only | **not a restore path.** Restore targets dev and AI databases only, after a destructive delete; there is no production restore and no per-record restore. Legitimate use is a snapshot before a risky bulk push (CA-23) |
| Forge journal and captures | what this device intended, what was sent, what the server said, and what the record looked like before and after | every mutation Forge runs, plus the seven allow-listed full-capture point reads (`forge/src/storage/captures.mjs:58-66`) | the journal is per device. Full persistence is capped at 512 KiB per body (`captures.mjs:82`) and allow-listed, which is the deliberate privacy boundary (K-06) |
| Committed results bundles and git | the durable, reviewable record: which manifest, which SHA, what came back | 42 committed bundles today (section C) | the bundle is the **only** history for quest and gameAsset, because the game's own log is unreadable for those classes |

Per class, the History panel composes from these sources. "Game log" means readable through the content-changes read; "bundle" means the committed results bundle carrying the before and after capture.

| CA | Game log at the pin | Forge journal | Committed bundle | Net answer to "what changed and who did it" |
|---|---|---|---|---|
| CA-01 jutsu | yes (update, delete) | yes | yes | complete except creates |
| CA-02 item | yes (update, delete) | yes | yes | complete except creates, clones and variant writes |
| CA-03 bloodline | yes (update, delete) | yes | yes | complete except creates |
| CA-04 gameAsset | **no** | yes | yes | **bundle only**; the game keeps the row but will not serve it |
| CA-05 quest | **no** | yes | yes | **bundle only**; same reason, on the class the workstream publishes |
| CA-06 AI | yes (update only) | yes | yes | no record of create, clone or delete anywhere in the game |
| CA-07 AiProfile | **none written at all** | yes | yes | Forge is the only history |
| CA-08 guide | not at the pin, yes at head | not yet | not yet | depends entirely on K-13 |
| CA-09 badge | yes (update, delete) | not yet | not yet | complete once the class is adopted |

Composition rule for the admin surface: a record's History panel is the union of the game log (where the class is readable), the Forge journal entry for any mutation this device made, and the committed bundle that carries the before and after capture. The panel must label each source, because they have different authority: the game log is what the server did, the journal is what this device believes, and the bundle is what the repository can prove. A Content Admin flow should capture the pre-state **automatically** before every update and delete, rather than relying on a manifest asking for it.

## E.7 Rate limits and multi-tab consequences for an admin queue (brief section 10)

The limiter is a 60-request sliding window per 60 seconds, keyed per procedure path per user (`app/src/server/api/trpc.ts:123`, pin), and it applies to `publicProcedure` only (`trpc.ts:211-213`, pin). A trip is a **penalty, not a retry signal**: `movedTooFastCount` increments and both money and bank are multiplied by 0.99 before the request is rejected (`trpc.ts:166-168,179`, pin).

The consequence for an admin queue is uncomfortable and must shape the design:

- **Every read a draft queue would poll is public and therefore limited.** The `getAll` list reads for jutsu, item, bloodline, quest, gameAsset and badge, the point `get` reads, the history read and the AI name list are all `publicProcedure`. The queue is the most read-heavy screen in the product and it spends the scarcest budget.
- **The protected reads are unlimited.** `profile.getAi`, `ai.getAiProfile` and the staff reads on maps, streak configs and raid thresholds carry no limiter at all. Where a protected equivalent exists, the admin surface should prefer it.
- **The window is shared with the carrier page.** Forge mounts over a live game route, and that page issues its own tRPC calls on the same paths under the same user key; the game refetches the profile every five minutes by itself. Forge cannot see that traffic, which is exactly why its local mirror reserves half the window: allowance is `floor(60 * 0.5) = 30` per path per minute (`forge/src/budget/bucket.mjs:32`).
- **Multiple tabs compete.** Two Forge tabs, or Forge plus the game in another tab, share one server window and two independent local mirrors. The write-ahead send log in `localStorage` is shared across tabs of the same origin, which bounds the damage, but the carrier traffic remains invisible.
- **Paging sizes.** 1000 per call for jutsu, 500 for item, bloodline, quest, gameAsset and badge, 100 for public user lists and for the history read. A full draft census of one class is one or two calls; a poll of six classes every thirty seconds is a trip.

| Read an admin queue needs | Auth class | Limited? | Page size | Queue consequence |
|---|---|---|---|---|
| `<class>.getAll {hidden:true}` for jutsu, item, bloodline, quest | public | yes | 1000 / 500 / 500 / 500 | one or two calls per class per refresh; four classes is already a quarter of the reserved allowance if refreshed every minute |
| `gameAsset.getAll` | public | yes | 500 | worse than the others, because there is no draft filter and the whole library must be paged |
| `<class>.get` point reads | public | yes | n/a | cache and reuse; these are also the seven paths whose bodies may be fully persisted |
| `badge.getAll`, `<class>.getAllNames` | public | yes | 500 | cheap, and a name list is the right cache key for a queue index |
| `logs.getContentChanges` | public | yes | 100 | per record, on demand only. Never prefetch history for a list |
| `profile.getAllAiNames` | public | yes | n/a | the only AI listing that exists |
| `profile.getAi` | protected | **no** | n/a | prefer it for AI review; it is free |
| `ai.getAiProfile` | protected | **no** | n/a | free, but a role miss throws (E.3) |
| `profile.getPublicUser` (role probe) | public | yes | n/a | one unit per session |
| `profile.getUser` (role probe) | protected | **no** | n/a | free but heavy in payload |

Design rules this implies for the queue, all of them things Forge already knows how to do: pull on demand with a visible "refreshed at" stamp rather than polling; refresh name lists and reuse cached point reads; never auto-refresh a background tab; surface the per-path budget meter on the queue screen, not only in diagnostics; and treat a rate-limit error as a halt with a countdown, never a retry (R-03).

## E.8 Review-queue truth source and approval-state storage (brief section 9)

**Design-panel verdict pending.** No `synth-data.json` and no `queue-model.json` existed when this section was written, so the options below are evaluated from the CA and CC rows and from the repository's own write contracts. The F author reconciles this subsection against the panel's data recommendation when it lands; if the panel disagrees, F wins on the recommendation and E keeps the source facts.

The question the brief asks is what durable thing can truthfully mean "ready for admin review". Four options, with what the evidence says about each.

| Option | What it would be | Evidence for | Evidence against |
|---|---|---|---|
| (a) repository-backed package | a file per package under `state/review/<slug>.json`, written through the same contents API Forge already uses, and rendered beside the workstream roadmap | `state/**` fires only the scrub workflow, so nothing regenerates or overwrites it; the paths owned by automation are `answers/*`, `dist/*`, the two loaders, the sentinel and `docs/DRIFT.md`, all disjoint. Builder already ships a user-driven "commit files to a repo directory" path defaulting to `state`, so this is precedent, not a new capability. It is diffable, reviewable and honest about being coordination state | it is a second representation that can drift from the live record; it needs a link to the live id to stay meaningful; the write is a single sha-aware PUT with no retry (R-07) |
| (b) live hidden records | the queue is a listing of `hidden:true` records discovered through authorized reads | needs no new storage and cannot drift, because it **is** the live state. Feasible for six of seven classes with no role at all (E.2b) | `hidden` carries no author, no intent, no reviewer and no date. It cannot distinguish "drafted yesterday" from "abandoned in March", and AI records have no flag to list by at all (CA-06). It answers "what is unpublished", not "what is ready" |
| (c) workstream `roadmap.json` | reuse the existing coordination file and its task statuses | the schema is validated by a real tool, statuses are an enum, and evidence anchors must exist in the tree; the workflow already carries `lead_role` and open decisions | the projections are regenerated manually and no CI runs the validator, so an app write leaves a stale `ROADMAP.md` for the next session to fix. The file is per workstream, not per record, and it is the content agent's coordination surface, not the admin's |
| (d) local only | per device state in IndexedDB | zero repository risk | the admin and the operator are different people on different devices; a queue only one of them can see does not remove the relay the brief wants gone |

**Evidence-based reading, for the F author to confirm or replace.** (b) is the only source that cannot lie about live state and should be the **listing**; it is what "unpublished" means and it is free. It cannot carry approval, so approval metadata has to live somewhere else, and (a) is the only candidate whose write path is already proven, whose directory nothing overwrites, and which is honest that it is coordination rather than canon. The natural shape is therefore a **hybrid**: the queue lists live hidden records, and a repository package file annotates the subset that a human has actually submitted, each entry naming the live ids it covers so the two can be reconciled by reading the game. That is also what `RUL-2026-09-12-002` implies: Forge presents and orchestrates, the repository holds the durable statement, and the game stays the only truth about what is live.

Three constraints any choice inherits. First, **no second canon**: the approval file must never be read as the record's state, and the UI must show live `hidden` beside it. Second, the game has **no approval field on any class**, so nothing here can be pushed into the game without a source change (K-10). Third, whatever file is chosen must not sit under a path an automation workflow regenerates. **K-09 stays open**; this subsection is its evidence, not its answer.

### E.8.1 How work moves between Content Operations and Content Admin

The brief keeps the two conceptually distinct even inside one application, and the source evidence says the seam is narrow. Operations produces a live hidden record: a manifest run mints the placeholder, edits it, reads it back, and the results bundle lands in the repository. Admin consumes exactly two things from that: the **live record id** and the **evidence** that the record is what the package intended. Nothing else has to cross.

That gives three handoff facts worth carrying into the architecture. First, the id is enough, because every class's full record is readable without a role for six of seven classes (E.2b), so the admin surface never needs the operator's journal to show the record. Second, the evidence the admin wants is already committed: the read-back capture in the bundle is the before and after the History panel composes (E.6). Third, the direction back is a publish, which is the same `update` call the operator would make, journaled the same way, so an admin publish is an ordinary mutation in the same execution core rather than a second write path. The practical consequence for section F is that Content Admin is a **presentation and policy layer over the existing runner**, not a parallel engine, which is also what `RUL-2026-09-12-002` requires.

## E.9 Guides: the one class that is post-pin

Guides are a first-class content type at the game head with a native `published` flag, staff-only draft reads, a role-gated create, update and delete, a client preview and readable history. They are also **entirely absent from the Forge pin**: there is no guide router, validator, table or constant at `345d18ac`.

The repository's own state confirms the gap. `forge/src/transport/procedures.mjs` is anchored to `345d18ac` (line 4) and contains **zero** guide entries; `skills/building-tnr-content/data/45c_DATA_constructors.json` and `45f_DATA_procedures.json` contain **zero** guide mentions; and `docs/DRIFT.md` lists the guide constants as upstream drift that has not been adopted (`docs/DRIFT.md:56` for `ContentTypes` and `:81` for `LOG_TYPES`, under the file's own rule that nothing below is adopted until the structural diff gate passes, `docs/DRIFT.md:5`). At the pin, `LOG_TYPES` has twelve entries with no `guide` (`app/drizzle/constants.ts:189-202`, pin) against thirteen at head (`constants.ts:255-269`, head).

So a Guide surface in Forge has a hard prerequisite chain, and none of it is a game change: **move the pin (K-13), regenerate the derived contracts through the repository's adoption gate, add five registry rows and a guide recipe, derive the validator field set**, and only then design the lane. The drift evidence says the pin move itself is contract-neutral for the existing 43 paths, which is why K-13 records it as cheap; the 45x re-extraction is the pass that needs care. Whether a Guide Studio becomes an official lane at all is **K-29**, and a lane shown before its capability exists is a placeholder (K-24).

## E.10 Cross-cutting findings

**CC-01 Role discovery without credential material.** The role is a column, not a claim, so Forge must ask. Two same-origin options never touch a cookie or token, because the browser attaches the session itself: `profile.getPublicUser {userId}` with the account's own id (public, costs **one** budget unit, `profile.ts:1950`, pin) or `profile.getUser` (protected, unlimited, but pulls the whole profile, `profile.ts:547`, pin). Forge today gates only on whether a path is protected (`forge/src/transport/auth.mjs:206-211`), so a role miss arrives as a refused write after the send. Recommendation: read the role once per session, hold it in memory only, never persist it, and use it to disable actions rather than to explain failures. The cost trade-off between the two calls is a design choice, not a decision.

**CC-05 Hidden-AI containment.** There is no draft state for an AI. A placeholder is contained (arena flag defaults false) but fully listed. A clone copies the containment flags verbatim, so cloning an arena AI puts the copy straight into the pool. Delete writes no log and leaves quest references dangling. An admin AI row should therefore show a containment panel and require a where-used read before a delete or a containment flip.

**CC-06 Image moderation.** The 512 KB `imageUploader` slug that Forge uses runs NSFW classification **after** the upload completes, and a flagged image or a classifier failure deletes the file and returns an empty URL with an error (`app/src/app/api/uploadthing/core.ts:42-60,89-94`, pin, byte-identical at head). So the upload is not final when the PUT returns, and Forge's current path keys off the PUT body rather than the completion result: a moderated-out image would leave a content record pointing at a deleted file. The 8 MB `backgroundImageUploader` requires `canChangeContent` and has **no** moderation call (`core.ts:190-199`, pin); its refusal message discloses the caller's role (`core.ts:79-83`, pin). Audio slugs are admin-gated and unmoderated.

**CC-08 Draft confidentiality.** For six of the seven Forge classes, hidden rows are readable by any account: the point reads are public and the list filter is client-controlled with no role check (`jutsu.ts:2115-2116`, `item.ts:3420-3421`, `bloodline.ts:1313-1314`, `quests.ts:187`, all pin; `gameAsset` takes no filter at all). This is Behaviour-proven for quests by committed captures. Only guide, sageMode lists, evolution reads and sector maps gate drafts on role. Public **pages** do 404 hidden rows, so the confidentiality is page-level only. The product must never promise that hidden means secret; spoiler-sensitive content is discoverable by id from any account.

**CC-09 Concurrency and session expiry mid-workflow.** Every content update is a whole-record write and **no procedure checks a version or timestamp**. Two admins editing the same record silently overwrite each other, and the game's own editor guards staleness client-side only. Forge's fetch-merge-send recipe is the right base; Forge Next should add its own optimistic check by re-reading immediately before the send and refusing on change. Session expiry mid-workflow is already handled by the four-state auth model plus the gate that blocks a protected send **before** it is journaled, so a refusal can never leave an item marked sent; what the admin surface must add is that the pause is durable, not a toast (R-25).

**CC-10 Registry coverage.** Forge's registry is 43 paths over seven routers (`forge/src/transport/procedures.mjs:24-67`), and anything outside it throws (`procedures.mjs:70-72`). For the seven classes the CRUD and publish procedures are all present, but six delete paths and three clone paths have **no caller**, and the cached reader refuses any list that is not a name list (`forge/src/budget/reader.mjs:74-76`), so a paged draft queue cannot be built at all today. The minimum registry expansion for a zero-game-change admin surface over the seven classes is: the history read, three relations reads, two evolutions reads, the crafting-aware item read, the scene-asset read, one role read, paged list support in the reader, and callers for the existing delete and clone paths. Every addition except the profile read is a public procedure and therefore budget-relevant (E.7).

**Cross-cutting row coverage.** For traceability against `evidence/admin-feasibility.json`: CC-01 is in this subsection; CC-02 is E.7; CC-03 and CC-04 are E.6; CC-05, CC-06, CC-08 and CC-09 are in this subsection; CC-07 is E.9; CC-10 is the closing paragraph above. No cross-cutting row is unowned.

## E.11 What would need a game change

None of these is a phase deliverable. Each is a dependency with a zero-change fallback, recorded so that the roadmap never plans around a capability the game does not offer (IDX §9, K-10 default is no change).

| Want | Why it is wanted | Zero-change fallback Forge Next uses instead |
|---|---|---|
| a partial publish toggle per class | publishing sends the whole record, so a publish can fail on an unrelated validator field | fetch, merge, send the whole record, and show the post-save read-back. Pre-check the unhide gates from the record already in hand |
| optimistic concurrency on update | two admins overwrite each other silently | re-read immediately before the send and refuse on change (CC-09) |
| `actionLog` on create and clone | placeholder minting and clones are invisible to the game's own history | the Forge journal and the committed bundle are the only record; make the pre-state capture automatic |
| `quest`, `gameAsset`, `sageMode` in `LOG_TYPES` | their history is written to the table but unreachable through the API | Forge captures, already committed for quests and assets, become the sole history for those two classes |
| role-gated hidden reads | drafts are not confidential (CC-08) | say so in the product. Do not promise secrecy |
| a role endpoint or a role claim | the role must be probed | one public or one protected profile read per session (CC-01) |
| a native approval field | there is no approval state on any class | repository-backed approval metadata that never claims to be live state (E.8, K-09) |
| a draft flag on AI records | a half-built AI is listed to everyone | containment flags plus a where-used check, and a Forge-side "not yet referenced" marker |
| a server-side quest preview | a true play preview is impossible client-side | re-implement the objective view and label it a preview of the stored record |
| production or per-record restore | `content_backups` cannot restore production | pre-write captures plus the committed bundle; no automatic deletion anywhere |
| privileged columns removed from the AI validator | a content editor can write role, ban, staff and money columns on an AI row | Forge's field allowlist per class refuses them pre-send (K-04) |
| owner scoping fixed on jutsu reskin moderation | a cross-user reskin moderation queue is impossible | out of scope for v1 |

## E.12 Open decisions routed to K

By id only. Each line states the consequence for this section, not the answer.

- **K-03** Content Admin permission scope: E.2 says what the roles allow; how much of it the surface exposes is the director's.
- **K-04** editorial-only versus arbitrary writes: every edit is a whole-record send, so a field allowlist is Forge policy, not a server capability.
- **K-05** which classes get first-class forms and previews in v1: E.2e and E.5 give the cost order; guides cannot be first because of K-13.
- **K-06** capture data classification: the automatic pre-write capture E.6 recommends is bounded by this decision.
- **K-07** operations eligible for a few-tap publish: E.4 shows the three publication axes, so eligibility cannot be uniform.
- **K-08** direct edits to hidden live records versus a staged package: E.8's hybrid reading assumes a direct edit with a repository annotation; the alternative keeps the operator relay.
- **K-09** where approval state lives: E.8 is its evidence and remains verdict-pending until the design panel's data recommendation lands.
- **K-10** whether any game-source change is acceptable: E.11 is the list that would become live if this ever moved from the default.
- **K-13** pin refresh: prerequisite for guides (E.9) and for citing head line numbers as contract.
- **K-29** Guide Studio as an official lane: depends on K-13 and has no capability behind it at the pin.
- **K-34** distinguishing authorization denial: E.3 is the audit it asked for. The finding is partial, per path and prose-coupled, and a fifth session state has no source behind it; the ruling stays with the director.
