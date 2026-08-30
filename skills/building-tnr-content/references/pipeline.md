# Pipeline: contracts, envelopes, manifest format

<!-- builder-version:begin -->Current live builder: **v4.28** (generated from builder_bundle.js - do not hand-edit)<!-- builder-version:end -->

> Migrated from `10_TECH_pipeline.md` (Phase 3, 2026-08-26). This is the shared plumbing every push uses, whatever the entity.

## Contents

  - [1. Tooling](#1-tooling)
  - [2. Verified tRPC contracts](#2-verified-trpc-contracts)
  - [3. Rate limit](#3-rate-limit)
  - [4. id-fetch and capture-first discipline](#4-id-fetch-and-capture-first-discipline)
  - [5. Universal gotcha checklist](#5-universal-gotcha-checklist)
  - [Addendum: push-path rules learned in the field (Tower / Howling builds)](#addendum-push-path-rules-learned-in-the-field-tower--howling-builds)
  - [Addendum (Jul 6 2026): AI equip + profile facts](#addendum-jul-6-2026-ai-equip--profile-facts)
  - [Addendum (Jul 10 2026): builder v4.13 + contract discoveries](#addendum-jul-10-2026-builder-v413--contract-discoveries)
  - [Addendum (Jul 10 2026, Phase 6): the native TNR MCP server (source-documented)](#addendum-jul-10-2026-phase-6-the-native-tnr-mcp-server-source-documented)
  - [Builder backlog (consolidated 2026-07-18; supersedes 61_UPGRADE)](#builder-backlog-consolidated-2026-07-18-supersedes-61upgrade)



Shared infrastructure for every content type. Read the relevant domain guide for WHAT to build; read this for HOW to push it and the verified API contracts. All contracts below were confirmed by 200-OK saves.

## 1. Tooling

### 1.1 The builder (universal manifest runner)

`builder.bundle.js` runs a manifest of content operations against TNR's tRPC API.

Manifest shape:
```json
{ "items": [
  { "name": "<label>", "entity": "jutsu|quest|asset|item",
    "slot": "create|convert", "srcId": "<optional>", "targetId": "<REQUIRED on every convert/edit - srcId+idmap does NOT self-resolve>",
    "data": { ... } }
] }
```
- `items` is the generic entry array; per-entry `entity` selects the type.
- `slot: "create"` makes a new record; `slot: "convert"` edits an existing one (`targetId` is the live id), and `slot: "edit"` updates an existing record by `targetId` for entities that fetch-merge (AI). **As of v4.12, `create` also fetch-merges:** after the create call, the builder GETs the fresh record (`jutsu.get` / `item.get` / `quests.get`, all `{id}`, source-confirmed) and merges your `data` over its defaults, the way `convert` and the asset path always did. A partial `create` payload no longer NaN-fails on a missing required field; complete payloads (the tables in `20_GUIDE_jutsu.md` and `23_GUIDE_quest.md`) remain best practice because server defaults are placeholders, not content. **`convert`/`edit` fetch-merge over the live record**, so they may carry only the fields you change (reproduce whole arrays like `effects` from the live record with just the change applied). On v4.11 and older, `create` sent `data` as-is with NO merge and required a complete payload.
- Build order is jutsu creates, then jutsu converts, then assets, then items, then quests, throttled about 2 seconds apart with exponential backoff for rate limits.
- **targetId law (2026-07-18):** every convert/edit entry carries an explicit literal targetId. Jutsu converts and AI edits do NOT resolve srcIds through the idmap; a missing targetId yields an empty fetch-merge base and phantom missing-field errors (`name: undefined`).
- **Ref-stripping law:** unresolvable `@` refs in AI equip arrays are silently STRIPPED server-side (entry ok, AI naked); quest fields pass them through as literal garbage. Manifests must be fully ref-substituted with literal ids, or run in the same session as their creates. Never hand over a ref-bearing repair manifest for a standalone run.
- **ID provenance law:** ids entering any manifest are EXTRACTED programmatically from bundle files and existence-checked at generation time - never transcribed from printed output (a truncated printout put invented ids into live reward tables).
- **Image re-upload law:** every corrected image gets a FRESH filename (_b, _c suffixes); never reuse a filename for changed content.
- **Idempotency:** a localStorage idmap (`srcId -> createdId`) means re-running a manifest fills the SAME record instead of duplicating. Bump `srcId` to force a fresh create.
- The builder auto-handles quest specifics (the flatten rule and referentialEqualities, see 2.5). It preserves original `createdAt` on edits.
- It surfaces per-entry status rows and the resulting ids. **Fixed in v4.12:** every mutation response is parsed and `json.success` / `json.message` is read per entry, so a rejected save (HTTP 200 with `success:false`, e.g. a name collision or flow-invalid quest) now shows RED with the server's message. On v4.11 and older this showed green while the record stayed a blank shell; if ever running an old bundle, confirm live records changed and dedup names first (section 5).

### 1.1a Builder capabilities

**Version authority (H04): the ONE authoritative builder-version line lives in `44_DATA_id_registry.md`; this file no longer states which build is current.** Version numbers below are historical capability markers (which behavior shipped in which build), not a claim about the deployed bundle.

The current builder (v4.12) handles entities `jutsu`, `item`, `asset`, `quest`, `ai`, and `aiProfile`; slots `create`, `convert`, and `edit`. It resolves cross-references (`@jutsu:<srcId>`, `@ai:<srcId>`, `@scene:<srcId>` -> the produced id from the idmap) and image refs (`@img:<file>` -> a URL it uploads, see 1.4). AI `create` includes the `toggleAiProfile` step so behavior rules attach on a fresh AI (guide 24). The panel title shows the loaded version.

Shipped in v4.12 (the whole prior roadmap plus preflight):
- **`json.success`/`json.message` read per entry.** A rejected save (name collision, flow-invalid) shows red with the server's message instead of green.
- **Error text widened** from about 300 to 1200 characters, so multi-field quest validation errors show at once.
- **Fetch-merge on `create`** for jutsu, item, and quest: the builder GETs the fresh record (`jutsu.get` / `item.get` / `quests.get`, all `{id}`, confirmed from the TNR source, no capture needed) and merges your fields over its defaults. Item `edit` (slot other than create) also fetch-merges over the live record.
- **Preflight validation.** Before any push, every manifest entry is checked against the source-confirmed write schema (`45_DATA_field_schemas.json` embedded in compact form): enum values (ranks, weapons, methods, targets, item/quest/asset enums, elements), numeric bounds, effect tag literals, AI rule condition/action/target literals, quest task vocabulary, and the quest flow graph (exactly one start node, every edge resolves to a real objective id, `start_battle`/`defeat_opponents` carry `failObjectiveId`, battle and raid nodes have non-empty `opponentAIs`, daily quests have 3-7 objectives, raid quests have exactly 1 plus boss health fields). Failing rows go red with the named fields and the build aborts before anything is pushed. `@`-refs are treated as valid placeholders. Escape hatch: a top-level `"skipPreflight": true` in the manifest bypasses the check.

### 1.2 The capture tool

`tnr_capture.bundle.js` hooks `fetch` and `XHR` and logs every matching request: method, tRPC procedure, full URL, request body, status, full response body. It persists across page reloads (localStorage) and downloads the whole log as one JSON file. Default filter is `/api/` (all tRPC traffic, no asset noise); clear the filter to capture everything.

Use it to reverse-engineer any unconfirmed contract: run the action in the UI, hit Download, hand the JSON to Claude. This is the source of truth for new endpoints.

**Combat resets the capture tool; use the sniffer for combat and quest runs.** Entering combat triggers a full page navigation, which clears the capture tool's in-memory log before it is persisted, so a captured quest run comes back with only the post-combat calls (`quests.checkRewards`, `profile.getUser`). The upload sniffer (`tnr-upload-sniff`) survives the navigation and logs the whole run: `quests.startQuest`, every `combat.performAction`, `combat.getBattle` / `getBattleEntries`, `gameAsset.getSceneAssets`, and `checkRewards`. For anything that passes through a battle (battlepyramid diagnosis, combat contracts, scene-asset loads), capture with the sniffer, not the capture tool. Sniffer entries are shaped `{t, via, method, url, req, status, resp}` with the body under `resp.text` (a JSON string).

### 1.3 The hosted-loader update loop

Bundles are loaded into VM via a tiny `@require` loader so the mobile editor never truncates them:
```js
// @match  *://www.theninja-rpg.com/*
// @match  *://theninja-rpg.com/*
// @grant  none
// @run-at document-start            // capture tool; builder can use document-idle
// @require https://raw.githubusercontent.com/perseverance484/tnr-tools/main/<bundle>.js?v=N
```
To update a bundle: regenerate it, dauntless re-uploads it to the repo and commits, then bump `?v=N` in the loader and reload. `@grant none` is required so the script runs in page context and can hook the page's `fetch`.

**Verify the commit before trusting a `?v` bump.** `raw.githubusercontent.com` caches the file for about 5 minutes after a push (and generic web fetches cache it too), so a fresh `?v` can still pull the old bytes, and a browser fetch of the raw URL is not a reliable check. Confirm the new version landed via the GitHub **blob** view (`github.com/<user>/<repo>/blob/main/<bundle>.js`), which reflects the commit immediately and is not CDN-cached. A common miss is the mobile GitHub editor committing to a new branch instead of `main`; the blob view on `main` catches that. After the blob view shows the new version, bump `?v`, save, and reload. The panel title shows the loaded version (e.g. `Content builder v4.12`), so confirm the right bundle loaded before running a manifest; never run a new manifest against a stale bundle.

### 1.4 Image upload (the builder resolves `@img` refs)

A manifest field value `@img:<filename>` is uploaded by the builder and replaced with the stored URL, so image assets never have to be uploaded by hand. Upload flow (uploadthing, captured):

1. Presign: POST `/api/uploadthing?actionType=upload&slug=imageUploader`, credentials same-origin, body `{files:[{name,size,type,lastModified}]}` -> `[{url:<signed ingest URL>, key}]`.
2. HEAD then PUT the file (FormData field `file`) to the signed url.
3. Stored URL = `https://<app-id>.ufs.sh/f/<key>` (app id `ui0arpl8sm`). No finalize or poll; the URL is live immediately. The builder caches it in the idmap under the filename and reuses it on re-run.

**Picker gotcha (Android).** The Gallery / Photos picker hands the file input MediaStore-numbered names (e.g. `1000007643.jpg`) and re-encodes PNGs to JPG, which destroys sprite transparency. Load images through the **Files / Documents** picker, which preserves the real filename and the raw bytes. The builder's file input carries no `accept` filter specifically to steer Firefox to the document picker. As a safety net the manifest may carry an `imgSizes` map (`{filename: bytes}`); the builder then matches a file by byte size even when the picker renamed it, but this only works on the raw original (document picker), not a re-encoded copy.

### 1.4b The `capture` block (read-only manifests, v4.21+)

A manifest can READ. This section exists because the rest of this file documents v4.12, where it
could not, and that stale line has already caused a session to build a bespoke capture userscript
for a job the builder does natively.

```json
{ "capture": { "before": [ { "proc": "quests.getAll",
                             "input": { "questType": "mission", "limit": 500, "cursor": 0 } } ] },
  "items": [] }
```

- `before` runs ahead of the mutations, `after` behind them. Each entry is `{proc, input}`; `proc`
  is required and `input` must be an object. `validate.py` shape-checks both.
- **A capture-only manifest is legal**: `items: []` with a non-empty capture block validates and
  runs. That was the v4.22 fix; on v4.21 `no items` fired first and blocked every read-only run.
- `capture.after` is the read-back. A push echo is not evidence; only a fresh read says what is in
  the database. Prefer `after` over trusting a green row for anything that matters.
- Reads come back in the results bundle, so a capture and the mutations it verifies are one
  artifact rather than two files to correlate by hand.
- Known history worth not rediscovering: `capture.before` was nested inside `if(dedupNames)` until
  v4.22 and had never once run, failing silently inside a bare catch.

### 1.5 The combined manifest (one form builds a whole event)

A single manifest can build an entire event, all its jutsu, AI enemies, and the quest, in one pass, the way the Drowned Fleet shipped. This is the "one completed form" format: emit one JSON object and the builder creates everything and wires the pieces together by reference, so no id is ever pasted by hand. A quest that reuses existing content is the same shape with fewer entries (put literal catalog ids in `opponentAIs` instead of `@ai` refs, and only `@img` refs for any new art).

Envelope:
```json
{ "imgSizes": { "jt-lash.jpg": 51234, "ai-treader.png": 80912 },
  "items": [ ...entries... ] }
```

Entry shape (same for every entity):
```json
{ "name": "<label>", "entity": "jutsu|ai|quest|item|asset",
  "slot": "create|convert|edit", "srcId": "<local handle>",
  "targetId": "<live id, edit/convert only>", "data": { ...entity payload... } }
```
- `srcId` is a local handle (any string) the builder maps to the created id in its idmap; other entries reference it by that handle.
- Build order is fixed: jutsu, then AI, then scene assets, then quest, so a reference always resolves before it is used. List entries in any order.

Four reference types, resolved anywhere in an entry's `data` (including nested `content.objectives` and AI `rules`) before each call:
- `@img:<filename>` uploaded via the image pipeline (1.4) and replaced with the stored URL. Use it for any per-record image (jutsu icon, AI avatar, quest icon) and for the art inside a scene-`asset` entry's `data.image`.
- `@jutsu:<srcId>` replaced with the created jutsu's id. Use it in an AI's `jutsus` equip array and in a rule's `jutsuId`/`comboIds`.
- `@ai:<srcId>` replaced with the created AI's id. Use it in a quest's `opponentAIs`.
- `@scene:<srcId>` replaced with the created scene asset's gameAsset id. Use it in a quest node's `sceneBackground` (point at a `SCENE_BACKGROUND` `srcId`) and in `sceneCharacters` (a `SCENE_CHARACTER` `srcId`).

Per-entity `data`:
- **jutsu** (create): the complete jutsu payload (guide 20 section 2.1), with `image: "@img:<icon>"`.
- **ai** (create): the AI record (guide 21 section 7.2), with `avatar: "@img:<sprite>"`, `jutsus: ["@jutsu:<srcId>", ...]`, and, for behavior, `rules: [...]` plus `includeDefaultRules: true`. The builder runs `toggleAiProfile` automatically so rules attach on the fresh AI (guide 24).
- **asset** (create): a scene background or character. `data` = `{name, type: "SCENE_BACKGROUND" | "SCENE_CHARACTER", image: "@img:<file>", folder, frames: 1, speed: 1, hidden: true, onInitialBattleField: false, licenseDetails: "TNR"}`. The builder runs `gameAsset.create` (null body, id in `message`), uploads the `@img` art, `gameAsset.update`s the record, and registers `srcId -> id` for `@scene` refs. See the creation contract in 2.7.
- **quest** (create): the complete top-level quest payload (guide 23 section 4.1), with the quest `image: "@img:<icon>"`, `content.objectives` where each `start_battle` node's `opponentAIs` uses `@ai` refs, and each dialog node's `sceneBackground: "@scene:<srcId>"` (plus `sceneCharacters: ["@scene:<srcId>"]` on a boss dialog). The builder applies the flatten rule and referentialEqualities (2.5) itself.

**Scene backgrounds and characters ride the manifest as `asset` entries** and no longer need a manual editor step. Each is an `entity: "asset"` entry that uploads its art through `@img` and is referenced by the quest through `@scene`, so the whole pyramid, art included, uploads in one run. They are still shared, reusable gameAsset rows (grouped by `folder`); to reuse an existing scene, put its literal id straight in `sceneBackground` rather than creating a duplicate. A node's `sceneBackground` accepts a `SCENE_BACKGROUND` id, an `@scene` ref, or a raw `ufs.sh` URL; `sceneCharacters` is an array of `SCENE_CHARACTER` ids or `@scene` refs. Verified from a live scene-asset creation capture and a populated quest save.

Worked skeleton (one of each entity; the Drowned Fleet manifest is the full reference):
```json
{
  "imgSizes": { "jt-lash.jpg": 51234, "ai-treader.png": 80912, "quest-icon.jpg": 33110, "bg-coast.jpg": 44000 },
  "items": [
    { "name": "Water Lash", "entity": "jutsu", "slot": "create", "srcId": "water_lash",
      "data": { "name": "Drowned Water Lash", "image": "@img:jt-lash.jpg",
                "effects": [ { "type": "damage", "power": 40 } ] } },

    { "name": "Tide Treader", "entity": "ai", "slot": "create", "srcId": "tide_treader",
      "data": { "username": "Tide Treader", "avatar": "@img:ai-treader.png",
                "jutsus": ["@jutsu:water_lash"], "includeDefaultRules": true,
                "rules": [ { "conditions": [ { "type": "distance_lower_than", "value": 5, "target": "RANDOM_OPPONENT" } ],
                            "action": { "type": "use_specific_jutsu", "target": "RANDOM_OPPONENT", "jutsuId": "@jutsu:water_lash" } } ] } },

    { "name": "Coast Background", "entity": "asset", "slot": "create", "srcId": "coast_bg",
      "data": { "name": "DrownedFleetCoast", "type": "SCENE_BACKGROUND", "image": "@img:bg-coast.jpg",
                "folder": "DrownedFleet", "frames": 1, "speed": 1, "hidden": true, "onInitialBattleField": false, "licenseDetails": "TNR" } },

    { "name": "The Drowned Fleet", "entity": "quest", "slot": "create", "srcId": "quest_main",
      "data": { "name": "The Drowned Fleet", "questType": "battlepyramid", "image": "@img:quest-icon.jpg",
                "content": { "reward": {}, "sceneBackground": "", "sceneCharacters": [],
                  "objectives": [
                    { "id": "d_intro", "task": "dialog", "sceneBackground": "@scene:coast_bg", "image": "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp",
                      "nextObjectiveId": [ { "text": "Begin", "nextObjectiveId": "f1_1" } ] },
                    { "id": "f1_1", "task": "start_battle", "sceneBackground": "@scene:coast_bg",
                      "opponentAIs": [ { "ids": ["@ai:tide_treader"], "number": 1, "quantity": 1 } ],
                      "completionOutcome": "Win", "nextObjectiveId": "win", "failObjectiveId": "reset1" }
                  ] } } }
  ]
}
```
The payloads above are abbreviated; every `create` still needs its complete field set (guides 20, 21, 23) and the objective graph must pass flow validation (23 section 1.2). After the run, confirm `json.success` per row and that the live records are real, not blank shells.

## 2. Verified tRPC contracts

### 2.1 Request envelope and conventions

- TNR uses tRPC batch links. **Every POST body is a batch envelope:** `{"0": { "json": <payload>, "meta": <meta> }}`.
- **Create endpoints take a null-body envelope** (`{"json": null, "meta": {"values": ["undefined"], "v": 1}}`) and **return the new id in the response `message` field** (exception: `item.create`, see 2.3).
- **Update endpoints** take `{"json": {"id": <id>, "data": <data>}, "meta": <meta>}`. The `meta` typically flags `createdAt`/`updatedAt` as Dates.
- **GET list endpoints** (`*.getAll`) are `?batch=1&input=<urlencoded {"0":{"json":{cursor,limit}}}>` and page via `nextCursor`.
- HTTP 200 does not mean success. Read `json.success` and `json.message`.

### 2.2 Jutsu

| Op | Method | Shape |
|---|---|---|
| `jutsu.create` | POST | null-body envelope -> new id in `message`. |
| `jutsu.update` | POST | `{json:{id,data}, meta:{values:{"data.createdAt":["Date"],"data.updatedAt":["Date"]}, v:1}}`. |
| `jutsu.getAll` | GET | requires a `limit` (number) in input or it 400s; follow `nextCursor`. |

### 2.3 Item

| Op | Method | Shape |
|---|---|---|
| `item.create` | POST | `{json:{type:"<itemType>"}}` (NOT null body, differs from the others). Creates a default row of that type; new id in `message`. |
| `item.update` | POST | `{json:{id,data}, meta: dates}`. `data` includes `craftingRequirements: []` and `requiredBloodline: null`. |
| `item.getAll` | GET | same paging pattern as `jutsu.getAll`. |
| `item.getItemWithCraftingRequirements` | GET | returns the full item. |

**Gotcha:** `battleDescription` is NOT NULL. An empty string coerces to null and 500s. Always send a non-empty value (e.g. `"Treasure chest"`).

### 2.4 AI enemy (profile)

| Op | Method | Shape |
|---|---|---|
| `profile.create` | POST | null body -> new AI id in `message`. |
| `profile.updateAi` | POST | `{json:{id,data}}` with **NO meta wrapper and NO date fields** (differs from jutsu/item). |

Edit URL for the in-console editor: `/manual/ai/edit/[id]`. Armor is set in the editor, not in the payload. See `21_GUIDE_ai_enemy.md` for the data schema. AI behavior rules live on a separate AiProfile row with its own contract (`ai.toggleAiProfile`, `ai.getAiProfile`, `ai.updateAiProfile`); a fresh AI is `aiProfileId: null` and needs the toggle before rules attach. See `24_GUIDE_ai_behavior.md`.

### 2.5 Quest

| Op | Method | Shape |
|---|---|---|
| `quests.get` | GET | returns the full quest definition. |
| `quests.create` | POST | null body -> new id in `message`. |
| `quests.update` | POST | `{json:{id,data}, meta:{values: dates, referentialEqualities: <7 mappings>, v:1}}`. |

**Flatten rule (the builder does this automatically):** on update, `data` must carry BOTH the nested `content` blob AND a flat top-level copy of every `reward_*` field plus `sceneBackground`/`sceneCharacters`, same values duplicated. The `meta.referentialEqualities` must declare 7 array fields, each top-level array pointing at its `content` twin (`data.sceneCharacters` -> `data.content.sceneCharacters`; `reward_jutsus`/`reward_badges`/`reward_items`/`reward_hunter_items_ids`/`reward_gathering_items_ids`/`reward_bloodlines` -> their `content.reward.*`). Full objective-node schemas and the flow-validation rules live in `23_GUIDE_quest.md`.

### 2.6 Asset

| Op | Method | Shape |
|---|---|---|
| `gameAsset.create` | POST | null body -> new id, creates a default STATIC row. |
| `gameAsset.update` | POST | `{json:{id,data}, meta: dates}`. |

Asset types: `STATIC`, `SCENE_BACKGROUND`, `SCENE_CHARACTER`, `MUSIC`, `SFX`. Edit URL: `/manual/asset/edit/[id]`.

**Creating a scene asset (verified, and what the builder automates):** three steps, the same create-upload-update shape as jutsu and AI. (1) `gameAsset.create` (null body) returns a new id in `message` and makes a default `STATIC` row. (2) Upload the art through the image pipeline (1.4), taking the `ufs.sh` URL. (3) `gameAsset.update` with `data = {name, type: "SCENE_BACKGROUND"|"SCENE_CHARACTER", image: <the ufs.sh URL>, url: <the create's default webp>, folder, frames:1, speed:1, hidden:true, onInitialBattleField:false, licenseDetails:"TNR"}` (the asset path fetch-merges, so only these fields are needed; `id`/`createdAt`/`updatedAt`/`createdByUserId` come from the create). In the combined manifest this is an `entity: "asset"` entry (1.5): `data.image` is an `@img` ref and the quest references the created id through `@scene:<srcId>`.

### 2.7 Read / list endpoints

- **Jutsu / item lists:** `jutsu.getAll` and `item.getAll`, GET, input `{cursor, limit}`, page via `nextCursor`. Dumped by `TNR_jutsu_dumper.user.js` / `TNR_item_dumper.user.js`.
- **AI list (confirmed):** `profile.getPublicUsers`, GET, input `{limit, orderBy:"Weakest", isAi:true, cursor:<int starts at 1>, direction:"forward"}`, returns `{data:[...], nextCursor}`; the list projection carries `userId`, `username`, `level`, `rank`, `isSummon`. Dumped by `TNR_ai_dumper.user.js`. For one AI's full record (12 stats, `primaryElement`/`secondaryElement`, multipliers, equipped `jutsus` join array) call `profile.getAi`, GET, input `{userId}`.
- **Asset list (confirmed):** `gameAsset.getAll`, GET, input `{limit, direction:"forward", folder?}` (omit `folder` for all, or pass a folder name to scope), returns `{data:[...], nextCursor}`; records carry `id`, `name`, `type`, `folder`, `image`, `url`. The folder index is `gameAsset.getAllFolders`, GET, null body, returning `{folder, count}[]`. Both dumped by `TNR_asset_dumper.user.js`.
- **Scene assets (confirmed, sniffer):** `gameAsset.getSceneAssets`, GET, null body, returns the quest-usable scene records (`SCENE_BACKGROUND` and `SCENE_CHARACTER`). A record is `{id, name, type, image, url, frames, speed, hidden, folder, onInitialBattleField, licenseDetails, createdByUserId, createdAt, updatedAt}` where **`image` is the art URL** (the `ufs.sh` upload) and `url` is a webp fallback. So scene backgrounds and characters are real `gameAsset` rows created in the editor (grouped in a `folder`), separate from the combined manifest. Verified from a populated quest save, a node references these by id or URL: `sceneBackground` accepts either a `SCENE_BACKGROUND` asset id (dialogs use this) or a direct `ufs.sh` URL (battles use this), and `sceneCharacters` is an array of `SCENE_CHARACTER` asset id strings (a boss dialog carried the Kaisei portrait id). The node `image` field is separate from the backdrop and stays a placeholder on dialogs.

## 3. Rate limit

The limiter is a **rolling cumulative request-count budget**, not per-burst. It drains across repeated sessions and refills over time. Use fewer, larger requests with exponential backoff (the builder does this), and let it refill rather than hammering.

## 4. id-fetch and capture-first discipline

- Pull live ids from edit URLs (`/manual/ai/edit/[id]`, `/manual/asset/edit/[id]`, the item editor) or from catalog dumps.
- For names to ids, dump the relevant catalog and resolve from the JSON.
- After a builder run, the status rows show `-> <id>` and the idmap holds `srcId -> createdId`; copy those into dependent content (e.g. chest ids into a quest branch reward).
- To verify a new or changed contract, run it once in the editor, capture the call, and confirm `json.success` before building a generator. A 500 with a clear column message (e.g. the `battleDescription` case) still teaches the exact field rule.

## 5. Universal gotcha checklist

Run before any push:

1. No em dashes in quest player-facing dialog text (a dialog node's `description`, a choice's `text`). Em dashes are fine elsewhere, in payloads, prose, and code.
2. All ids (AI, item, asset, jutsu) are real, pulled from edit URLs or catalog dumps, never invented.
3. Read `json.success` / `json.message`; HTTP 200 alone does not mean the save applied.
4. `item` pushes: `battleDescription` is non-empty; `item.create` body is `{type}`, not null.
5. `profile.updateAi` carries no meta and no dates; `jutsu.update` and `item.update` do carry date meta.
6. Quest pushes: the flatten rule and 7 referentialEqualities are present (builder handles), and the objective graph passes flow validation (see `23_GUIDE_quest.md`).
7. Rate limit is cumulative and cross-session; batch with backoff and let it refill.
8. Userscripts match both `www` and non-`www`, use `createElement`/CSSOM not `innerHTML`, and are hosted via `@require` if large.
9. `create` payloads carry the COMPLETE field set for the type (guides 20/23), including easy-to-miss required numbers (jutsu `*ReducePerLvl`, quest `consecutiveObjectives`/`maxAttempts`/`maxCompletes`); `convert`/`edit` payloads carry only the change and reproduce whole arrays.
10. Names are unique: dedup a new jutsu / AI / item / quest name against the catalog or a `getAllNames` capture before creating. A duplicate returns 200 with `success:false` and leaves a blank `New ...` shell.
11. Images load through the Files / Documents picker, not Gallery, so filenames and PNG transparency survive (1.4).
12. After a build, spot-check the live records. v4.12 reads `json.success` per entry so a rejected save shows red; on older bundles a 200 with `success:false` showed "ok" and left blank shells.

## Addendum: push-path rules learned in the field (Tower / Howling builds)

- **AI edits never rely on fetch-merge for `jutsus` or `items`.** The builder passes live rows through raw (jutsu objects, UserItem rows with `dropChancePerc`), which the server rejects. Every AI edit sends `jutsus` as string id refs AND `items` as ids-with-number explicitly, even when only touching other fields. Bundle fix (row normalization in the edit merge) queued for the next builder rev.
- **Quest EDITS do not fetch-merge top-level fields.** A partial quest edit reaches the server with `name`/`description`/`questType`/`tierLevel` undefined and 400s. Reproduce the FULL quest record from a live capture with changes applied. (Whole-array rule, promoted to whole-record for quests.)
- **Items: `battleDescription` is DB NOT NULL.** Empty string is nulled by the write path and 500s at the DB. Always non-empty.
- **AI edits require an explicit `targetId`.** The idmap does not resolve srcIds for `ai` edit entries ("ai needs targetId or slot create"); jutsu converts/edits accept srcId via idmap but carry `targetId` anyway when known. Pull the AI id from the idmap dump or edit URL.
- **The jutsu edit/convert merge-base load trips the API rate limiter** (v4.12): even single-entry, targetId-carrying edit manifests stall on "limited 10s" retries. Workarounds until the builder rev (per-id `jutsu.get` merge base + lazy catalog load): make small scalar/effect changes by hand in the admin UI while the jutsu is unequipped, then push a lean re-equip ai edit; keep any builder-path edit manifests to the minimum entries and let the limiter cool between runs.
- **`stun` AP loss is the `apReduction` field, not `power`.** Power is only the stun CHANCE (RNG roll); an omitted `apReduction` silently takes the server default (-10 AP observed live). Always set `apReduction` explicitly on stun effects. Same power-as-chance pattern applies to the whole prevent/control family (shield creation, flee, seal, prevents).
- **Combat internals are documented in 50_DATA_combat_facts.md** (damage formula and constants, 450k/200k battle-init caps incl. AIs, LVL_CAP 100 clamp, the 10% minimum-damage floor and its boost scaling, pierce pipeline bypass, modifier staging order, ai threshold semantics). Read it before any combat balance work; it is calibrated against live fight captures.

## Addendum (Jul 6 2026): AI equip + profile facts
- ai-edit `jutsus` ADDITIONS create userjutsu links `equipped: false`; combat's availActions includes
  only equipped:true, and rules referencing unequipped jutsu skip silently. Fix: unequip -> re-equip
  cycle (edit `jutsus: []`, then edit `jutsus: [all ids]`) - fresh links equip true (Testament precedent).
- AiProfile rule cap: 20. use_combo_action compresses rotations (walks comboIds in order) but its
  range semantics beyond the proven Law+Unravel are unverified; prefer use_specific_jutsu at range.
- Rule EXECUTABILITY law and A* distance semantics (inclusive comparators, no-path reads 0): see
  50_DATA_combat_facts.md - both are load-bearing for any AiProfile work.
- Chat attachment quirk: "Pasted content" attachments can arrive empty; upload outputs as files via
  the + picker, or paste short excerpts inline.


## Addendum (Jul 10 2026): builder v4.13 + contract discoveries

**Builder v4.13 (supersedes the 1.1a v4.12 description; version + `?v` authoritative in 44):**
- **Quest edit fetch-merge**: quest `slot: convert`/`edit` now GETs `quests.get {id}` and merges partial data over the live record. The Howling full-record rule (23 sec 3.4d) is automated for builder-mediated edits; it still applies to hand-pushed `quests.update`. Content is one merge key: supply the whole `content` object when touching objectives/reward/scene.
- **`@quest:` / `@item:` cross-refs**: the resolver is prefix-generic; preflight now validates every `@jutsu/@ai/@scene/@item/@quest` ref (must resolve to an earlier-phase srcId, an earlier same-phase quest, or an existing idmap key) and a runtime guard blocks entries with unresolved refs. Quest->quest forward refs work in one run (manifest order). Live-proven: prereq + newQuestIds wiring in a single push.
- **Results bundle**: every build auto-downloads `tnr_results_<ts>.json` (per-entry name/srcId/entity/slot/state/detail/id + the exact merged payload pushed + full idmap). Standing rule: the bundle comes back for verification; it feeds 44 and the session delta.
- **Live name dedup (opt-in)**: manifest top-level `"dedupNames": true` checks creates against live names (jutsu/item/asset/ai) before pushing.
- **Manifest file picker** ("Load" button): kills the 100k paste cap. **Idmap export/import** ("Map" buttons): idempotency survives device/browser loss.
- Field sanitizers (empty-string `image` stripped; reward type checks), AI write-shape sanitizer (raw jutsus/items join rows -> string refs / ids-with-number), equip-reminder on jutsu converts.
- Known defect carried to v4.14: jutsu convert still loads the full catalog as merge base and trips the limiter on small edit manifests (per-id `jutsu.get` fix scoped in 60_PROCESS C1).

**`gameAsset.getAllNames` takes `{type, folderPrefix}` (2026-08-26, capture-verified).** It returns ONE asset
type per call, so a full asset sweep needs SCENE_BACKGROUND, SCENE_CHARACTER, STATIC, SFX and MUSIC separately.
With `folderPrefix: true` the `name` comes back as `folder/Name`. A capture filtered to scene types cannot see
map pins (type STATIC) and must not be read as evidence they do not exist.

**Bundle editing workflow (2026-08-26):** `builder_bundle.js` lives in the tnr-tools repo only; project
knowledge does not carry a copy (it drifted before: project held v4.17 while the registry said v4.18 was
current). To edit the builder, upload the current bundle from the repo at the start of the session; the
session ends with the changed file handed back for commit.

**Generated shape source (2026-08-26):** `schema_extract.py` now emits `45c_DATA_constructors.json` alongside
`45b`. `45c` carries every tagged-union member (73 effect tags, 20 quest objectives, 10 AI actions, 9 AI
conditions) with its discriminant, all fields, `prefault` defaults and resolved enums. **Build payload objects
from it; never hand-author a tagged shape.** Run `python3 schema_extract.py <repo> --report` after any repo
drop and eyeball the member counts: a union returning zero members means the regex parser missed it, not that
the union is empty.

**getAllNames contract family (live-captured, staff manual):** `quests.getAllNames`, `jutsu.getAllNames`, `item.getAllNames`, `gameAsset.getAllNames`, `village.getAllNames`, `profile.getAllAiNames`, `badge.getAll`. Single-call id+name(+image) lists; the cheap dedup/index source. `quests.getAll` also pages full quest records (quest dumper unblocked).

**Quest run contracts (live-captured):** `quests.startQuest` POST `{questId, userSector}`. `quests.checkRewards {questId}` (no nextObjectiveId) is the collect/resolve call; `{questId, nextObjectiveId}` is the dialog-choice call. Both return `{success, notifications[], rewards{...}, userQuest, resolved}`.

**Capture tooling note:** three overlapping tools are in circulation (capture bundle, upload-sniff, monitor); consolidation scoped in 60_PROCESS. Until then: monitor/sniffer for anything crossing combat or quest runs.


## Addendum (Jul 10 2026, Phase 6): the native TNR MCP server (source-documented)

Sources: `app/src/libs/mcp/*`, `app/src/app/api/mcp/[[...transport]]/route.ts`, `app/src/app/api/monthly-mcp-reset/route.ts`, root `CLAUDE.md`, `.env.example`.

**What it is.** A Model Context Protocol server over the whole tRPC API: **408 endpoints across ~40 routers are `mcp: enabled`**, including the full content-editor surface (quests create/update/clone/delete, jutsu, item, bloodline, AI profile, checkRewards, startQuest...). Exposed as **4 meta-tools** (listGameRouters -> listRouterEndpoints -> getEndpointSchema -> callEndpoint) rather than 408 individual tools.

**Where it runs (the critical fact).** The MCP server is env-gated (`NEXT_PUBLIC_MCP_ENABLED`, `false` in .env.example) and its monthly reset explicitly runs only on **`www.theninja-rpg.ai`**, the SEPARATE AI deployment that CLAUDE.md maps to its own database (`theninja-ai`, PlanetScale branch `main`), not production (`tnr`/`main-1`). Working hypothesis pending live confirmation: **MCP writes land in the AI-instance database, not the production game.** The monthly reset wipes/resets that instance's state.

**Auth.** Bearer token on `/api/mcp`: either a Clerk JWT (verified directly) or an opaque OAuth access token (`oat_` prefix, verified via Clerk's `/oauth/userinfo`). Scopes are parsed from token claims. Mutation gating (`checkEndpointAuthorization`): blocked only when the caller is BOTH unauthenticated AND lacks a write scope (`profile:write` or `write`); an authenticated user passes the gate, with per-procedure permission checks (e.g. `canChangeContent`) still enforced inside tRPC.

**Limits.** 30 requests / 60s per IP AND 30/60s per authenticated user (Redis sliding window), stricter than general tRPC.

**Implication for the pipeline.** Two possible verdicts, decided by the live test below:
1. If MCP is only the `.ai` sandbox instance: it is NOT a production push channel; the builder remains primary. Its value becomes a schema-true validation sandbox (server-validated dry runs of manifests before production pushes) and possibly the future Foundry substrate.
2. If a production-pointed MCP exists or is enabled for staff: it becomes the primary push channel candidate (server-side zod validation, no userscript, no manifest replay), builder demotes to fallback.

**Live test procedure (dauntless):**
1. Confirm whether `www.theninja-rpg.ai` responds and whether your Clerk session/token works there (same Clerk instance or separate?).
2. Read-only probe: MCP client (or curl) -> `POST https://www.theninja-rpg.ai/api/mcp` with your bearer token: `listGameRouters`, then `listRouterEndpoints {routerName: "quests"}`, then `callEndpoint {endpointName: "quests.getAllNames"}`.
3. Identity check: `callEndpoint profile.getUser` -> is the returned user YOUR account (shared DB?) or a separate AI-instance account (separate DB confirmed)?
4. If shared-DB or a prod MCP surface exists: one hidden-record write test (e.g. quests.update on a salt-test throwaway) before any verdict.
Deliverable back: the raw responses; the verdict re-ranks 61.

## Builder backlog (consolidated 2026-07-18; supersedes 61_UPGRADE)
v4.15 preflight (from the Masquerade failure classes): hard-block unresolved @refs; require targetId on every convert/edit; per-tag effect validation against 46 (catch direction/calculation poisons); require consecutiveObjectives on quest creates, rank/regeneration/preferred on AI creates, generalTypes on formula effects; warn on >4 same-type percentage rows (multiplicative guard).
Still-open from the old roadmap: results-bundle auto-download; live-name dedup in preflight (getAllNames pass); @item cross-manifest resolution for two-phase pushes.



## Data tiers (moved from project 11_TECH_source_map, 2026-08-28)

Three tiers of data, with a hard rule about which one you may write from.

## Tier 1: the trimmed catalogs (40, 41, 42, 43, 47)

**LOOKUP ONLY. Never compose a write payload from these.**

They answer: does this name already exist, what id is it, what level is that AI, which quests use this enemy, what does this jutsu roughly do, is this asset real art or a placeholder.

Every one carries a `_coverage` block naming exactly how many fields the full record has, how many are kept, and what was dropped. Read it before assuming a field is absent from the game rather than absent from the file. The most dangerous omissions:

- **Jutsu and item effects are display strings, not payload objects.** A real effect row has 16 fields including `appearAnimation`, `appearSfx`, `calculation`, `direction`, `generalTypes`, `statTypes`, `powerPerLevel`. The catalog shows `"damage 45"`. Composing from that produces a record the server rejects, or worse, accepts with silent cosmetic loss.
- **The quest catalog contains NO objective graph.** `nodes` and `tasks` are counts. Node ids, descriptions, dialog choices, edges, scenes and per-node rewards are all absent.
- **The AI catalog carries 3 of 12 stat fields**, offence only.

## Tier 2: the full exemplars (49)

One complete untrimmed record per entity: jutsu, item, asset, quest, AI. Every field, real values, straight from a live harvest.

**This is the shape reference.** When you need to know what a payload looks like, read this, not a guide's field table and not a trimmed catalog. The AI exemplar alone has 160 fields.

The quest exemplar keeps one objective per task type so it stays readable, but every field on each objective is complete.

## Tier 3: the harvest dumps

Full fidelity, every record, ~25 MB per set. Not stored in this stack. dauntless runs `TNR_harvester.js` and uploads them; they live in the working folder for the session.

**Pull from a harvest when:** you are editing a specific record and need its exact current state, you are reproducing an effects array, you are reading or rewriting a quest graph, or the catalogs are older than the last push.

## Regeneration

```
python3 refresh_catalogs.py <folder of harvests> <output folder>
```

Picks the newest dump of each kind and rewrites catalogs 40, 41, 42, 43 and 47 with fresh contents and a fresh `_coverage` block. Shapes never change, only contents, so a refresh is a drop-in replacement.

Run it after any session with pushes. The catalogs are snapshots and say so; an id looked up in a stale catalog is the same class of error as an invented field.

## The rule in one line

Catalogs to find it, exemplars to shape it, harvests to write it.


## Relocated engine laws (2026-08-28)

Verbatim law text moved out of project knowledge. Stage 3 splices these into the
owning skill reference. Numbers stay canonical against /docs/ENGINE_LAWS.md.

1. **Create paths are lenient; update paths are strict.** A create can store payloads the update validator will later reject. Corollary: a record that "pushed fine" at create may be un-editable as stored. Always compose to update-strict standards.

2. **Per-tag strict unions.** Effect objects validate against their exact tag schema; ANY extra field fails the whole union, even fields legal on other tags (`calculation` on clear/cleanse, `direction: "defence"` on reflect). `direction` is a fixed literal, `"offence"`, even on defensive tags.

3. **Compose effects from live exemplars only.** Never assemble effect objects from schema-doc field lists. Pull the shape from catalog 40b or a live capture of a working record and change only values. Lean proven shapes: `clear/cleanse/debuffprevent {type, power, rounds}`. QUALIFIER (H12, 2026-08-01): lean applies PER ENTITY - the jutsu.update path accepts lean shapes, but the ITEM effects union demands the full editor key set including cosmetics (appearSfx, disappearAnimation, staticAssetPath). Jutsu lean, item full.

4. **Formula effects require BOTH `statTypes` AND `generalTypes`** (damage, pierce, wound). An absent/empty generals list detonates the damage formula into astronomical values (trillions). `["Highest"]` is the default for both.

5. **Explicit `targetId` on every convert and edit, all entities.** srcId + idmap does NOT self-resolve on jutsu converts or AI edits. Missing targetId on a convert makes the fetch-merge base empty and fails on phantom missing fields (`name: undefined` = your targetId is wrong).

6. **[SHARPENED 2026-08-26] Effect `power` caps at 100 per row, `apReduction` on stun caps at 100, and the `threshold` on `has_effect`/`target_has_effect` caps at 100.** Rows may repeat to stack (see stacking laws). CAVEAT: a condition's `value` field has NO upper bound (`z.coerce.number().int().positive()`), so `health_below: 150` validates and is simply never false. Do not assume the 100 ceiling generalises across the condition schemas; it does not. Bounds per field: `45c`.

7. **Quest `startsAt`/`endsAt` accept plain `YYYY-MM-DD` only** (regex-enforced; ISO datetimes 400).

8. **`maxLevel`/`maxAttempts`/`maxCompletes` cap at 100.**

16b. **[NEW 2026-08-26] `hidden: true` goes on every create, every entity, no exceptions.** Where the table has the column it hides the record; where it does not (`userData`, i.e. AI records) the key is stripped silently, because `insertAiSchema` is `createInsertSchema(...)` without `.strict()`. Either way lint L13 is satisfied and nothing ships visible by accident. For AI records the real containment is `inArena: false` plus not being referenced by a quest. Publishing is always a separate manifest.

16c. **[NEW 2026-08-26] gameAsset `hidden` affects LISTING ONLY, never rendering.** The column defaults to `true`. Live public quests render hidden assets today (Copies, Not Thefts displays three; every `dmissionicons` quest icon is hidden and visible). 165 of 407 live assets are hidden. No unhide step is needed at publish and none should be built.

17. **Unresolvable `@` refs in AI equip arrays are silently STRIPPED server-side** - entry reports ok, AI stands naked. Quest refs pass through as literal garbage strings instead. Every manifest must be fully ref-substituted, or run in the same builder session as its creates.

28. **HTTP 200 never means success; per-entry `json.success` does.** Bundles are read programmatically.

29. **IDs are EXTRACTED from bundle files by script, never transcribed from printed output.** A truncated printout put invented ids into live reward tables. Any id entering a manifest is existence-checked against its source bundle in the generation script.

30. **Name-collision fills leave equipped blank shells**, and the trimmed catalogs (40/42) are stale for collision checks - live records (including hidden ones) collide invisibly. Treat catalog dedup as advisory; distinctive names beat generic ones.

31. **Generation starts from the owning guide's complete payload template.** Both catastrophic failures this cycle (stat-less AIs, generals-less damage) were documented in the guides and skipped by freehand generator helpers. Helpers must be seeded from the guide templates, not from memory.

32. **Fresh filenames on every re-upload of a corrected image** (`_b`, `_c` suffixes) - never reuse a filename for changed content.

36. **`data.name` must be set on every create and must equal the entry name.** The builder sends the data payload; the entry-level `name` is manifest metadata the server never sees. Thirty-one records in one campaign, most of the AI roster, were composed with the name at entry level only and would have landed carrying server defaults.

45. **Doubled reference prefixes (`@ai:@ai:name`) survive a naive ref sweep** because the usual pattern matches the inner copy and finds a legitimate srcId. At push time the whole string resolves to nothing and the node spawns an empty fight. Lint for the doubled prefix explicitly.

46. **An `image` field sent as an empty string is nulled at the write path and 500s at the DB** (H16). On repair edits, OMIT the field entirely so fetch-merge preserves the editor-uploaded value; never send `image: ""`.

72. **[CORRECTED 2026-08-26] Optional means ABSENT; nullable means null is FINE. They are different chains and the difference is now generated.** `z.string().optional()` rejects an explicit null, so a payload cloned from a harvest (which serialises missing keys as null) must have those keys stripped. But `.nullable()` and `.nullish()` fields ACCEPT an explicit null, and stripping those makes a field impossible to clear. 54 fields across the four content entities are nullable, `requiredVillage` and `prerequisiteQuestId` among them; the authoritative split is the `nullable` flag in `45d_DATA_entity_schemas.json` and no count belongs in this file. A blanket null-strip is a bug, not a safety measure: it is why a pushed `requiredVillage: null` left the old village lock in place.

73. **Booleans are not numbers.** In Python `isinstance(False, int)` is True, so any numeric normalisation pass silently flattens `reward_hunter_items` and `reward_gathering_items` to 0 and the write is rejected. 12 fields are boolean.

74. **Read records are not write shapes.** The three classes above (null optionals, coerced booleans, enum strings sent as 0) account for every authoring failure in this cycle. `schema_extract.py` derives the guard lists from `validators/objectives.ts` and `validators/rewards.ts`; builder v4.18 applies them to every outgoing mutation body.
