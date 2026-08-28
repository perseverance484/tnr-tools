> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# 23 - GUIDE: Quest, Mission, and Event Creation

Owner doc for quest objective-graph mechanics, the quest data model, the verified quest tRPC contracts, mission and event design patterns, and the working reference quest. Shared plumbing (the builder, capture tool, rate limit) is in `10_TECH_pipeline.md`. Reward values, drop rates, and difficulty tuning are balance decisions reserved by dauntless; this guide fills structure and mechanics.

A "quest" is the engine object behind story missions, repeatable missions, timed events, and the battlepyramid gauntlet. They share one data model and one objective engine. The mechanics below were verified in live play, not inferred. `start_battle` behaves differently in generic quests versus the `battlepyramid` type; both are documented in section 3.

---

## 1. The objective graph

A quest body is a list of **objectives** (nodes). Each node does one thing (talk, choose, collect, fight, reset, win) and points at the next node by id. The set of nodes plus their pointers forms a directed graph the engine walks.

### 1.1 Edges and pointers
Each node can carry up to three pointers:
- `nextObjectiveId` - where to go on success. Counts as an incoming edge to its target.
- `failObjectiveId` - where to go on failure (used by battles). Counts as an incoming edge to its target.
- `resetObjectiveId` - where a `reset_quest` node sends the player. **Does NOT count as an incoming edge.**

### 1.2 Flow validation (the rule that rejects quests)
The engine requires **exactly one starting objective**: exactly one node with no incoming edge. Incoming edges are counted from `nextObjectiveId` and `failObjectiveId` only. Because `resetObjectiveId` does not count, a node that is reachable *only* through a `reset_quest` pointer looks like a second start and the whole quest is rejected.

Rejection looks like this (note the HTTP status is still 200):
```
{"success": false, "message": "Objective flow invalid: Multiple starting objectives found: <ids>"}
```

**Fix pattern:** never point a `reset_quest` at an otherwise-orphan retry node. Point `resetObjectiveId` at an **in-flow** node that already has a real incoming edge, normally the dialog that precedes the failed battle. That keeps the retry path inside the graph and preserves the single start.

---

## 2. Objective types

| `task` | Purpose | Notes |
|---|---|---|
| `dialog` | Story setup, NPC explanation, scene transitions, reveals, consequences. | Carries scene fields. `nextObjectiveId` on EVERY dialog node in EVERY quest type is a **choices array** `[{text, nextObjectiveId}]`, single-entry for straight continuations; non-dialog nodes take a plain string (H02 settled 2026-08-01; lint L29). |
| `dialog` with a choices array ("dialog_choice") | Investigation, deduction checks, moral or procedural decisions, branch selection. | Not a distinct task in the engine: a choice gate is a `dialog` node whose `nextObjectiveId` is a multi-entry choices array. **Every choice must route somewhere.** |
| `collect_item` | Evidence, markers, tags, ledgers, scraps, maps, chests, seals. | Always name the item. |
| `defeat_opponents` | The primitive for scripted and sequential battles in generic quests. | Location-gated, 54-key node, **requires `failObjectiveId`.** See 3.2. |
| `start_battle` | A single opener battle in generic quests; the **chained floor primitive in battlepyramid**. | Behavior depends on quest type. See 3.1 and 3.7. |
| `reset_quest` | Send the player back on a wrong assumption, destroyed evidence, premature accusation, or a lost battle. | 32-key node, has `resetObjectiveId`, no `nextObjectiveId`. Reset text should explain the mistake. |
| `win_quest` | Mission completion and reward delivery. | Completion text should state what changed. |
| `fail_quest` | Hard fail (e.g. a wrong deduction in a gated mission, or a boss loss). | Ends the quest as a loss. |

### 2.1 Full task vocabulary (source-confirmed)

The engine's objective union accepts 42 task literals (complete list and per-task field schemas in `45_DATA_field_schemas.json`). Beyond the table above, all available and source-confirmed:

- **Location tasks:** `move_to_location`, `win_encounter_at_location`, `collect_item`, `deliver_item`. These carry a location block: `sectorType` (`specific` / `random` / `from_list` / `user_village` / `current_sector` / `enemy_village`), `locationType` (`specific` / `random`), `sector` / `longitude` / `latitude`, `sectorList`, `hideLocation`. `collect_item` and `deliver_item` add `item_name` (min 3 chars), `collectItemIds` / `deliverItemIds`, `delete_on_complete`, and collect adds `collect_time_minutes` (0-60).
- **`new_quest`:** grants quests on reach via `newQuestIds: []`.
- **Raid tasks:** `open_raid` / `exclusive_raid`. Raid quests must consist of exactly one of these as the only objective, with a required `sector`, non-empty `opponentAIs`, and `raidBossMaxHealth` (> 0) plus `raidBossCurrentHealth` set at quest level.
- **29 simple counter tasks** (each takes a `value` threshold, default 3): `pvp_kills`, `arena_kills` (**PvE counter, not PvP** - the only PvP primitives are `pvp_kills` and `spars_won`; H18), `spars_won`, `random_encounter_wins`, `minutes_passed`, `minutes_training`, `stats_trained`, `user_level`, `reputation_points`, `jutsus_mastered`, `days_in_village`, `days_as_kage`, `errands_total`, `a/b/c/d_missions_total`, `a/b/c/d_crimes_total`, and the profession counters `medical_experience`, `medical_experience_gained`, `crafting_experience`, `crafting_experience_gained`, `hunting_experience`, `hunting_experience_gained`, `gathering_experience`, `gathering_experience_gained`.

Two cross-field rules run server-side: **daily quests need 3 to 7 objectives; raid quests exactly 1.**

---

## 3. Battle objectives

This is the most error-prone area. Read the subsection for your quest type: generic quests use `defeat_opponents` (3.2); the `battlepyramid` type uses chained `start_battle` (3.7).

### 3.1 `start_battle`: an instant ACTION, legitimate anywhere when dialog-gated (source-verified)

The engine classifies `start_battle` as an **InstantTask** alongside `win_quest`/`fail_quest`: it is an action that EXECUTES on every tracker touch while available (and tracker touches happen on virtually every server interaction), not a goal the player works toward. It is not location-gated; coordinates on the node are vestigial.

- **A dialog directly before a start_battle genuinely gates it**: the battle is not *available* until the player picks the choice, and availability is the trigger. This supersedes the older "max one per generic quest / dialogs do not gate" rule, which was the observed behavior of UNGATED chains: non-dialog objectives auto-link forward on first touch (3.4b.2), so an ungated chain of start_battles is entirely available at once, they all fire, and only the first becomes a real battle.
- **Shield doctrine (required):** every `start_battle`, in every quest type, sits DIRECTLY behind a `dialog`. Multiple start_battles are fine when each is dialog-gated and the walked path can only make one available at a time (battlepyramid was never special; it just always followed this shape). A start_battle placed as the FIRST objective fires the moment the quest is accepted; use that only for deliberate ambush openers.
- **Loss handling:** the battle outcome is matched against `completionOutcome` (Win/Lose/Flee/Draw/Any). A non-matching outcome WITH `failObjectiveId` fail-routes the objective (its link is set to the fail target and it completes). A LOST start_battle additionally sets an internal `recentlyDied` flag that blocks auto-refire; the client offers a retry that clears it and re-enters combat. A lost start_battle WITHOUT `failObjectiveId` strands on that retry button, so always set it.
- **Choosing the primitive:** `start_battle` = the fight begins the instant the player commits (a confrontation dialog choice), cinematic, no travel. `defeat_opponents` (3.2) = the fight lives on the map and the player travels to it. Both complete from the same combat feedback (the engine reports the outcome to both task types).

### 3.2 `defeat_opponents` is the primitive for scripted and sequential battles (generic quests)
- It **is location-gated**: the player travels to a tile and the fight happens there. Multiple `defeat_opponents` nodes sequence correctly when each is reached in turn.
- The node is large (54 keys) and **must include `failObjectiveId`.** A missing `failObjectiveId` is one cause of the battle re-arming in a loop. (`failObjectiveId` is optional in the server schema, so the server never catches its absence; the guard is on us.)
- **Re-arm loop cause:** `sectorType: "enemy_village"` ties the fight to a persistent hostile village that re-engages, and/or a missing `failObjectiveId`. The proven non-looping configuration is `sectorType: "random"` with `failObjectiveId` present.

### 3.3 opponentAIs encoding
The opponent block is:
```json
{ "ids": ["<ai_id>"], "number": <head_count>, "quantity": 1 }
```
`number` is the headcount for that entry (`number: 2` produces two attackers). `quantity` stays `1`. Multiple entries in the `opponentAIs` array put several **distinct** AIs in one fight: `[{ids:[A],number:1,quantity:1},{ids:[B],number:1,quantity:1}]` is a two-enemy fight of A plus B. (The earlier reading of `number` as a per-wave quantity was wrong.)

The `{ids, number, quantity}` shape is shared with reward bundles, but the semantics differ by context (source-confirmed): in `opponentAIs`, `number` is the headcount; in `reward_items` and loot tables, `number` is the drop chance % (default 100) and `quantity` is the amount granted.

### 3.4 Same-sector activation and dispersal (generic quests)
When the player enters a sector, the engine **activates every location objective pinned to that sector at once.** Two `defeat_opponents` nodes in the same sector will co-fire, and dialogs between them do NOT disperse them. To make battles happen one at a time, put them in **different sectors.** `sectorType: "random"` lets the engine assign a random sector per node, which naturally spreads them out.

### 3.4b The sequencing engine (source-verified, `quest.ts` / `objectives.ts` / `sector.ts` / `quests.ts`)

Extracted from the engine, not inferred. The full working paper is `QUEST_ENGINE_ANALYSIS.md`; these are the rules that govern design.

**Task classes (the engine's own taxonomy):**
- **GATE: `dialog`, and nothing else.** A dialog sets its forward link only when the player picks a choice (the client sends it via `quests.checkRewards {questId, nextObjectiveId}`).
- **ACTIONS (instant): `win_quest`, `fail_quest`, `new_quest`, `reset_quest`, `start_battle`.** They execute on EVERY tracker touch while available. Tracker touches run inside nearly every server call (user fetch, tile poll, combat end, training), so "available" means "happening now."
- **GOALS (location): `move_to_location`, `collect_item`, `deliver_item`, `defeat_opponents`, `win_encounter_at_location`.** Map-pinned, completed by player behavior at a location.
- **COUNTERS (simple tasks):** value accumulators.

**Sequencing rules:**
1. **Availability = link traversal, not completion.** An objective is available iff reachable from the start by walking `selectedNextObjectiveId` links; `done` is never checked on the path.
2. **Non-dialog objectives auto-link forward on their first touch while available, done or not.** Successors of non-dialog nodes co-activate immediately; a chain of non-dialog nodes is entirely live from its first node. **To make anything wait, put a `dialog` directly before it.**
3. **All sectors resolve on the first tracker touch after accepting**, before availability filtering: `random` rolls then; **`current_sector` = the sector where the quest was accepted** (there is no "previous objective's sector" mechanism; co-locate same-scene hooks by giving them all `current_sector`).
4. **A location objective with an empty `image` renders NO map marker** (the renderer returns before drawing). Every collect/deliver/move/defeat node the player must find requires a non-empty `image` URL. `hideLocation` hides log coordinates, not the marker.
5. **`reset_quest` semantics:** it fires every touch while available. With `resetObjectiveId`, it deletes the reset-target's goal and everything downstream along selected links (usually including the reset node itself), so those objectives re-create fresh: the reset target is re-gated, and **their sectors REROLL** (`random` re-rolls; `current_sector` re-resolves to wherever the player stands at the next touch). Without `resetObjectiveId` the whole tracker wipes and the quest restarts.
6. **`attackers` is an ambush system and its `number` is a PERCENT chance per touch** (`attackers_max_per_battle` caps the spawn; battles are RANDOM_ENCOUNTER type), unlike `opponentAIs.number` which is a headcount. `win_encounter_at_location` only ambushes while the player is in the objective's sector and **only completes from a RANDOM_ENCOUNTER win there**; quest battles never complete it. An encounter hunt therefore wants `number` high (100 = ambush on next touch).
7. **Reward timing:** objective-level rewards pay ONCE on the first `checkRewards` after the objective is done (a `collected` flag prevents re-pay); the quest-level `content.reward` pays when the walked path resolves. **`reward_items` entries carry a drop chance: `{ids: [itemId], number: percent}` with number defaulting to 100 (guaranteed); each entry rolls independently, fractional percents work.** The same ids-with-number chance applies to an AI inventory's drop items. Mission/crime/medical/errand types receive village/shrine/clan boosts; `story`/`event` pay raw.
8. **`collect_item`:** timer starts on the tile (`collect_time_minutes`, non-integers fine, 0.2 = 12s) and CANCELS with a notification if the player leaves early; completion grants `collectItemIds` (empty array completes and grants nothing, correct for flavor trail items); `delete_on_complete` cleans up.
9. **Server-side flow validation on save:** exactly one start (unreferenced) objective, no self or unknown references, no duplicate ids, dialogs need at least one choice, DFS cycle detection over string-next + dialog choices + `failObjectiveId` (`resetObjectiveId` is NOT an edge, so retry loops must route through `reset_quest`), and every objective reachable.

### 3.4b consecutiveObjectives, dates, and the launch fields (2026-07-18, paid for live)

**`consecutiveObjectives: true` is REQUIRED explicitly on EVERY quest create.** The field is schema-required with no default; the DB default is false, which makes every objective simultaneously live: `win_quest` nodes become trivially claimable and the `checkRewards` tracker tick pays their rewards whenever it fires (observed live: a component paid at battle START). The reward-timing rules elsewhere in this guide assume consecutive mode and are only true under it. Every full-record convert must preserve the field.

**`startsAt`/`endsAt` accept plain `YYYY-MM-DD` only** (regex-enforced; ISO datetimes 400 the fill). Launch pattern: one convert setting `hidden: false`, both dates, `maxAttempts`/`maxCompletes` (both cap 100), with the nine player items unhidden in the same manifest.

**Scene rendering split:** the travel-page quest popup renders the TOP-LEVEL `content.sceneBackground` only; per-node scene fields render in the quest view proper. Never leave the top-level scene empty (the client fallback is arbitrary); set a deliberate global scene, typically the entry/exterior.

### 3.4b-2 CYOA branch doctrine (the wings pattern)

Choices must close doors, or the graph is a menu wearing a maze's clothes. Reference implementation (Crimson Masquerade): the three ENTRANCES open different wings, each reaching only 3-4 of the seven endings, which partitions the reward components and forces evening rotation by construction. Supporting rules: gossip/flavor nodes take a SINGLE forward continuation (never re-offer the full choice menu); knowledge gates drop RATES, never skips fights (no combat-free farm loop may exist once answers hit Discord); exclusive intel picks (one indulgence per run) make information a committed choice paying off in a future run.

### 3.4c Quest gate field caps (server schema, live-verified)

`maxLevel`, `maxAttempts`, and `maxCompletes` are all capped at **100** by the quest write schema; larger values 400 the whole fill. Additionally, `maxAttempts`/`maxCompletes` are only ENFORCED for questTypes in `QuestTypesWithMaxAttempts = [event, story, battlepyramid, starter, raid]`: `mission`/`errand`/`crime` repeatables ignore both caps entirely (their frequency governance is the engine's daily counters). Consequence: a daily battlepyramid has a hard lifetime ceiling of 100 completions per player; only an upstream code change can raise it.

### 3.4d Quest EDITS reproduce the full record

The quest edit path does not fetch-merge top-level fields: partial edits 400 with undefined name/description/tierLevel/questType. Reproduce the complete quest data object from a live capture with only your changes applied (Howling Hills rule). hidden must be reproduced from live truth to avoid flipping a public quest.

### 3.4e War reward fields

reward_war_damage and reward_war_healing are valid objective-level and quest-level reward fields (summed across objectives). Verified pattern: a war mission pays war damage on its aftermath dialog. defeat_opponents accepts sectorType enemy_village for fights on enemy ground.

### 3.5 Lose-retry pattern
To let a player retry a lost battle instead of failing the quest:
```
battle (failObjectiveId -> reset node)
  -> reset_quest (resetObjectiveId -> the dialog that precedes the battle)
    -> dialog -> battle
```
The `reset_quest` points back at an in-flow dialog (not at an orphan), which both gives the retry and satisfies flow validation (1.2). This is the same in generic and battlepyramid quests.

### 3.6 reset_quest node shape
A `reset_quest` node is 32 keys: a 25-field reward block (usually zeroed), `resetObjectiveId`, and the scene fields. It has no `nextObjectiveId`. The reward block being present does not mean it grants a reward; leave the values at zero unless a partial-credit reset is intended (a balance decision).

### 3.7 The `battlepyramid` quest type (dialog-gated single battles)

`questType: "battlepyramid"` uses `start_battle` as its fight primitive, but it does NOT chain consecutive battles. A `start_battle` behaves as in 3.1: any `start_battle` nodes connected with no non-battle node between them are activated together at the start of the action phase, and all but one auto-resolve as done with no fight. Confirmed on a live run: the Drowned Fleet, built with consecutive `start_battle` floors, resolved to `win_quest` and paid full rewards while most of its battles were skipped. (This corrects an earlier claim that the battlepyramid engine chains battles one at a time; it does not.)

**The rule: put a non-battle node between every battle.** A `dialog` node between two `start_battle` nodes gates the second one: it does not activate until the player passes the dialog. Give every fight its own preceding dialog and the battles fire one at a time.

- **Each `start_battle` is one fight, and must be preceded by a dialog.** Clearing it follows `nextObjectiveId`; losing follows `failObjectiveId` (normally to a `reset_quest`). There is no location gating and no sectors, but there is no auto-sequencing either: without a non-battle node before it, a battle is pre-activated with the previous one and skipped.
- **Nodes used:** `dialog`, `start_battle`, `reset_quest`, `win_quest`, `fail_quest`. No `defeat_opponents`.
- **Verified node shapes:**
  - `dialog` (37 keys): a 25-field reward block plus `image`, `attackers` (`[]`), `description`, `nextObjectiveId` as a **choices array** `[{ "text": "...", "nextObjectiveId": "<id>" }]`, `sceneBackground`, `sceneCharacters` (`[]`), `successDescription`, `attackers_scale_gains`, `attackers_max_per_battle`, `attackers_scaled_to_user`.
  - `start_battle` (41 keys): the reward block plus `opponentAIs` (3.3), `failObjectiveId`, `nextObjectiveId` as a **single id string** (not a choices array), `completionOutcome: "Win"`, `scaleGains`, `keepOriginalPools: false`, `opponent_scaled_to_user: false`, `drawDescription`, `failDescription`, `fleeDescription`, `sceneBackground`, `sceneCharacters`.
  - `reset_quest` (32 keys): reward block plus `resetObjectiveId`, scene fields, no `nextObjectiveId`.
  - `win_quest` / `fail_quest`: reward block plus scene fields, terminal (no `nextObjectiveId`).
- **Canonical flow (a dialog before every battle):**
  ```
  d_intro (dialog) -> b1 (start_battle) -> d1 (dialog) -> b2 -> d2 -> b3 -> ... -> d_boss (dialog) -> boss (start_battle) -> win_quest
  ```
  The buffer dialogs can be one short line each (the next guardian steps forward) and reuse their stage's background. Each `start_battle`'s `failObjectiveId` points to a `reset_quest` whose `resetObjectiveId` returns to that battle's preceding dialog (the lose-retry loop, 3.5), so a loss restarts that fight, not the whole run. The boss loss can route to a `fail_quest` for a hard fail.
- **Flow validation (1.2) still applies:** exactly one start node (no incoming `next`/`fail` edge; `resetObjectiveId` does not count), and every `start_battle` needs `failObjectiveId`.
- **Scene convention and scene fields.** Give each background at least one `dialog`; the per-battle buffer dialogs within a stage reuse that stage's `sceneBackground`, and each `reset_quest` points at the battle's preceding dialog. The backdrop is the node's **`sceneBackground`**, which accepts a `SCENE_BACKGROUND` gameAsset id (what dialogs use) or a direct `ufs.sh` URL (what battles use). **`sceneCharacters`** is an array of `SCENE_CHARACTER` gameAsset id strings, used to place a portrait in a dialog (a boss intro sets one). Scene assets are shared `gameAsset` rows listed by `gameAsset.getSceneAssets` (10_TECH 2.7); they can be **created in the same combined manifest** as `entity: "asset"` entries and referenced by `@scene:<srcId>` (10_TECH 1.5, 2.7), or reused by putting a literal id here. The node `image` field is separate from the backdrop and can stay a placeholder on dialogs.

---

## 4. Quest-level data model (complete)

Top-level fields on the quest, set once outside the objective list, captured from a live quest record and verified against the server write validator (QuestValidator); the machine-readable schema is `45_DATA_field_schemas.json`. As of builder v4.12, a quest `create` fetch-merges: the builder GETs the fresh quest (`quests.get {id}`) and merges your data over its defaults, so a partial create no longer fails on a missing field. **Complete payloads below remain best practice** (server defaults are placeholders), and a `quests.update` by hand still needs the flatten rule (5.1) with the full reward block. The required-field failures called out below are what bit us on v4.11 and older.

**Required strings and enums**

| Field | Values | Notes |
|---|---|---|
| `name` | string | Display name. |
| `description` | string | Listing blurb. |
| `image` | url | Listing art. |
| `questType` | 18 values: `starter` `tier` `daily` `mission` `errand` `crime` `exam` `event` `story` `anbu` `medical` `hunting` `gathering` `battlepyramid` `pvp` `achievement` `war` `raid` | `event` has no daily limit and is convenient for testing. `daily` requires 3 to 7 objectives; `raid` has special rules (2.1). |
| `questRank` | `D` / `C` / `B` / `A` / `S` / `H` | |
| `successDescription` | **non-empty string** | **Must be >=1 character.** An empty string returns `too_small: expected string to have >=1 characters`. |
| `retryDelay` | `none` / `daily` / `weekly` / `monthly` | Source-confirmed enum. |
| `medicalRank` / `huntingRank` / `gatheringRank` | `"NONE"` when unused | Required in practice. Enums: medical `NONE` / `NOVICE` / `APPRENTICE` / `MASTER` / `LEGENDARY`; hunting and gathering `NONE` / `D RANK` / `C RANK` / `B RANK` / `A RANK` / `S RANK`. |
| `consecutiveObjectives` | bool, **required** | `true` for a floor-by-floor gauntlet (battlepyramid). A missing value returns `expected nonoptional, received undefined`. |
| `hidden` | bool | `true` keeps it off the public list while testing; flip to `false` to publish. |

**Required numbers (gating; values are dauntless's call, but the fields are required)**

| Field | Notes |
|---|---|
| `requiredLevel` | minimum level. |
| `maxLevel` | maximum level. |
| `maxAttempts` | attempts allowed. |
| `maxCompletes` | completions allowed. |

**Nullable (default `null`)**

| Field | Notes |
|---|---|
| `prerequisiteQuestId` | null when none. |
| `tierLevel` | null unless a difficulty tier is used. |
| `requiredVillage` | null when ungated. |
| `requiredBloodlineId` | null when ungated. |
| `startsAt` / `endsAt` | null for an always-on quest (timed events set these). |
| `raidBossCurrentHealth` / `raidBossMaxHealth` | null unless a raid boss. |
| `raidCaptureDeadline` / `raidEndsAt` / `raidGracePeriodEnd` | null unless a raid. |

**Object**

| Field | Notes |
|---|---|
| `content` | the body: `{ objectives: [...], sceneBackground, sceneCharacters, reward: { ... } }`. |

The `content.reward` block holds `reward_money`, `reward_tokens`, `reward_clans` (clan/prestige points), `reward_exp`, `reward_prestige`, `reward_rank`, and the array rewards `reward_jutsus`, `reward_badges`, `reward_items`, `reward_bloodlines`, `reward_hunter_items_ids`, `reward_gathering_items_ids`. War quests also carry `reward_war_damage`. The full 25-field reward block appears on each objective node too (usually zeroed). All reward values are dauntless's call.

**Builder-managed:** `id`, `createdAt`, `updatedAt` (Date meta). Do not hand-set.

### 4.1 Complete top-level create payload (copy this shape)

The wrapper the builder fills; objectives and reward omitted for length. Drop nothing on a `create`.

```json
{
  "name": "The Drowned Fleet",
  "description": "...",
  "image": "@img:quest_icon.jpg",
  "questType": "battlepyramid",
  "questRank": "B",
  "successDescription": "The Drowned Fleet lies broken beneath the waves.",
  "retryDelay": "none",
  "medicalRank": "NONE",
  "huntingRank": "NONE",
  "gatheringRank": "NONE",
  "consecutiveObjectives": true,
  "hidden": true,
  "requiredLevel": 40,
  "maxLevel": 100,
  "maxAttempts": 1,
  "maxCompletes": 1,
  "prerequisiteQuestId": null,
  "tierLevel": null,
  "requiredVillage": null,
  "requiredBloodlineId": null,
  "startsAt": null,
  "endsAt": null,
  "raidBossCurrentHealth": null,
  "raidBossMaxHealth": null,
  "raidCaptureDeadline": null,
  "raidEndsAt": null,
  "raidGracePeriodEnd": null,
  "content": { "objectives": [], "sceneBackground": "", "sceneCharacters": [], "reward": {} }
}
```

---

## 5. Quest tRPC contract

Envelope rules and the batch format are in `10_TECH_pipeline.md`. Quest-specific shape:

**To build a whole event as one submission** (its jutsu, AI enemies, and the quest together), the quest is one entry in a combined builder manifest: see `10_TECH_pipeline.md` section 1.5. In that form the quest's `opponentAIs` carry `@ai` refs to the AI entries and the quest icon carries an `@img` ref. Scene backgrounds and characters ride the manifest as `entity: "asset"` entries whose art uploads through `@img`; each node's `sceneBackground` and `sceneCharacters` then reference them by `@scene:<srcId>` (or a literal id to reuse an existing one). See 10_TECH 1.5 and 2.7.

| Op | Method | Shape |
|---|---|---|
| `quests.get` | GET | full quest definition. |
| `quests.create` | POST | null-body envelope, returns new id in `message`. |
| `quests.update` | POST | `{json:{id,data}, meta:{values: dates, referentialEqualities: <7 mappings>, v:1}}`. |

### 5.1 The flatten rule (the builder does this automatically)
On update, `data` must carry **both** the nested `content` blob **and a flat top-level copy** of every `reward_*` field plus `sceneBackground` and `sceneCharacters`, with the same values duplicated in both places. The `meta.referentialEqualities` must declare 7 array fields, each flat top-level array pointing at its `content` twin:
- `data.sceneCharacters` -> `data.content.sceneCharacters`
- `reward_jutsus` -> `content.reward.reward_jutsus`
- `reward_badges` -> `content.reward.reward_badges`
- `reward_items` -> `content.reward.reward_items`
- `reward_hunter_items_ids` -> `content.reward.reward_hunter_items_ids`
- `reward_gathering_items_ids` -> `content.reward.reward_gathering_items_ids`
- `reward_bloodlines` -> `content.reward.reward_bloodlines`

The builder's quest path (`qupdate`) assembles all of this from a single objective list plus a reward block, so hand-authoring rarely needs to touch it. If you do push by hand, missing any of the seven equalities or the flat copy fails the save.

### 5.2 Read json.success, not the HTTP status
`quests.update` returns HTTP 200 even when validation fails (flow-invalid, a missing top-level field, missing equalities, and so on). Always read `json.success` and `json.message`. Builder v4.12 does this per entry and shows the server's message on red rows (and its preflight catches flow-invalid graphs before anything is pushed); older builds reported a 200 as "ok" and hid a rejected save, which could leave an empty quest shell that looks created but is not.

---

## 6. Design

### 6.1 The patterns
- **Story mission.** Title, level/rank gates, availability, prerequisite, unlocks, reward package, campaign function, a player summary, the objective flow, and reusable assets. Deduction missions add gated `dialog_choice` checks where a wrong choice routes to a `reset_quest` (or `fail_quest` for hard gates) that explains the mistake.
- **Repeatable mission.** Unlocked by story progress; it should reinforce the mechanic or theme of the story mission that unlocked it.
- **Event.** Direct, repeatable, reward-driven, with a clear fantasy and a simple loop. Events want clear eligibility, an obvious reward ladder, chest tiers, and short readable instructions. Use `questType: event`.
- **Battlepyramid gauntlet.** A dialog-wrapped chain of `start_battle` floors climbing to a boss (3.7). One dialogue per background; each stage's loss resets to that stage.

### 6.2 Writing rules
- Keep dialog short and readable, usually 1 to 3 sentences. Avoid long lore dumps and abstract language with no visible player action.
- **No em dashes in player-facing dialog text** (a dialog node's `description` and a choice's `text`). This is the one place em dashes are banned; the rest of the stack, prose, and code may use them. Use commas, colons, or hyphens in dialog instead.
- **Wrong choices should teach the logic:** route back (reset), explain why the assumption was wrong, and reinforce the theme.
- **Correct choices should advance and clarify** the lesson.
- **Breadcrumbs should be short and memorable.** Do not reveal a faction's full name too early unless this is the finale.
- Always name enemies and quest items in objective text.

### 6.3 Reward philosophy (values are dauntless's call)

**Ruled individual-mission reward structure (canonical, set by the Content Admin).** Any `questType: "mission"` quest uses its rank's line as the quest-level `content.reward`; these are final values, not placeholders. Mission-type payouts additionally receive shrine/village/clan boost multipliers engine-side (3.4b.7), so these are the pre-boost base.

| Rank | Exp | Ryo | Prestige | Tokens | Clan Points |
|---|---:|---:|---:|---:|---:|
| S | 547 | 3,500 | 45 | 100 | 500 |
| A | 410 | 2,625 | 34 | 100 | 300 |
| B | 308 | 1,970 | 25 | 100 | 200 |
| C | 231 | 1,475 | 19 | 100 | 100 |
| D | 173 | 1,100 | 14 | 100 | 100 |
Use known reward structures when provided rather than inventing them. Reference points from existing story acts: an Act I standard mission ran 15,000 ryo / 100 tokens / 100 clan points / 450 exp / 100 prestige; an Act I finale ran 20,000 / 125 / 125 / 560 / 125; Act II standard 18,000 / 110 / 110 / 500 / 110; Act II finale 25,000 / 150 / 150 / 670 / 150. Outcome variants, where a mission uses them, are reduced success -20%, standard at base, bonus success +20%. For events, separate the chest tier from its possible contents, separate Hunter and Gatherer pools if relevant, classify contents by rarity, and **do not invent exact drop percentages.**

### 6.4 Asset planning
When moving toward implementation or an infographic, list the assets. Story missions: backgrounds, NPC portraits, enemy portraits or sprites, quest-item icons, objective icons, reward icons, an act or mission emblem. Battlepyramid: one background per stage, a boss sprite, a scene character for the boss dialog, the quest icon. Unknown assets are written `NOT RECORDED`; do not fabricate them unless asked for new creative assets.

---

## 7. Reference quests and worked examples

### 7.1 Reference generic quest (copy for `defeat_opponents` chains)
**Echoes of the Fool - copy**, id `70qYRdS4SJVYpCIr0S1S5`, `questType: event`, 16 objectives. A dialog-wrapped chain of three `defeat_opponents` battles, each `sectorType: "random"` and landing in a different sector (336 / 146 / 21). Each battle is preceded by a dialog offering a fight-or-quit choice; the quit branch routes to a `reset_quest` back to the start dialog. Canonical non-looping, flow-valid sequential multi-battle pattern.

### 7.2 Reference battlepyramid (copy for chained `start_battle`)
**Kaeruun's Pyramid**, id `-i3wNG4zgJhtGybbsPU-0`, `questType: battlepyramid`, 12 objectives. Dialogs interleave with `start_battle` floors, each floor's `failObjectiveId` routing to a shared `reset_quest` back to the start dialog, ending at a one-enemy boss `start_battle` into `win_quest`. This is the shape section 3.7 describes. **The Drowned Fleet** (in `44_DATA_id_registry.md`) is the worked build: 24-plus nodes, three ship stages, one dialogue per background, per-stage resets.

### 7.3 Warpath (event, war cache) - id `ZpCHLfGJJcR9L7ovcHx6J`
A daily war event on the generic pattern: two `defeat_opponents` battles, then a choose-your-cache dialog branching to five confirm dialogs, then `win_quest`. `questType: event` for testing (toggle to `war` when shipping), `requiredLevel 80`, `maxLevel 100`.

### 7.4 Ashen Lung (story, medical) - id `b6DKJZB3_6v54RDcBXYWi`
A Rank D medical deduction mission with four `dialog_choice` gates where a wrong choice routes to `fail_quest`. Demonstrates the gated-deduction story pattern and the writing rules in 6.2.

---

## 8. QA checklist (before any quest push)

- [ ] `create` preferably carries the COMPLETE top-level field set (section 4), including `consecutiveObjectives`, `retryDelay`, the four gating numbers, and the nullable raid/timing fields (v4.12 merges defaults under partial creates); `successDescription` is non-empty (4.1).
- [ ] Exactly one starting objective; every `reset_quest.resetObjectiveId` points at an in-flow node, not an orphan (1.2).
- [ ] Every `dialog_choice` routes somewhere on every branch.
- [ ] Correct primitive for the fight: `start_battle` (dialog-gated, instant on commit) or `defeat_opponents` (travel to the fight on the map); EVERY `start_battle` sits directly behind a `dialog` and carries `failObjectiveId` (3.1).
- [ ] Every battle node has `failObjectiveId`; independent `defeat_opponents` battles use `sectorType: "random"` to disperse (3.2/3.4); same-scene chained hooks all use `current_sector` (3.4b.3).
- [ ] Every location objective (`collect_item`, `deliver_item`, `move_to_location`, `defeat_opponents`) carries a non-empty `image`, or its map marker will not render (3.4b.4).
- [ ] A `dialog` directly precedes every `start_battle` and every location objective that must not co-activate with its predecessor (3.4b.2).
- [ ] `opponentAIs` uses `{ids, number: <headcount>, quantity: 1}`; multiple entries for multi-enemy fights (3.3).
- [ ] Battlepyramid: a `dialog` (buffer) precedes EVERY `start_battle`, so no two battles are consecutive; each `reset_quest` points at the battle's preceding dialog (3.7).
- [ ] Lost-battle paths route through a `reset_quest` back to the pre-battle dialog if a retry is intended (3.5).
- [ ] Reward values, drop rates, and gates confirmed with dauntless; exact drop percentages not invented (6.3).
- [ ] Push read `json.success` / `json.message`, not just HTTP 200; then confirm the quest is real, not an empty shell (5.2).
- [ ] `hidden: true` while testing; flipped to `false` only when shipping.
- [ ] All enemy and item ids are real, pulled from edit URLs or catalog dumps.
- [ ] Task literals come from the confirmed vocabulary (2.1 / file 45); a choice gate is a `dialog` with a choices array, not a `dialog_choice` task.


## Addendum (Jul 10 2026): new_quest mechanics, exclusivity findings, two write-validator rules

**Two write-validator rules (live 400s, now also expanded in 45):**
1. `reward_village_membership` is a VILLAGE ENUM, not a free string: `"NONE" | "SHIROHANA" | "TSUKIMORI" | "HYORIN" | "AKASUMI" | "AKIKAZE"` (legacy union: `"SHINE" | "GLACIER" | "SHROUD" | "CURRENT"`). Empty string 400s the whole fill. Applies at quest level and objective level.
2. **Public quests require scene characters**: a `hidden: false` quest must have main `content.sceneCharacters` non-empty OR every objective carrying `sceneCharacters`. Hidden quests are exempt. Error text: "Quest must have either main sceneCharacters set or all objectives must have sceneCharacters defined". Consequence: every quest gets scene characters before its publish flip.

**new_quest grant mechanics (live-verified end to end, Jul 10):**
- The grant fires inside the granting quest's `checkRewards`, announces via notification, and STARTS the target quest (tracker created immediately; the player does not pick it up).
- **The tracker is pruned on the next eligibility pass if the target's prerequisite is unmet.** `new_quest` does NOT bypass prerequisite gating in effect. (The notification still shows; the quest never persists.)
- **Hidden quests granted with no prerequisite DO persist** (hidden is a listing filter, not an eligibility filter). Hidden quests are also staff-startable directly via `quests.startQuest`.
- **Quest resolution requires a client `checkRewards {questId}` call**, which only player-visible quest-log UI fires. A hidden quest can complete its objectives (instant tasks execute on tracker touches) but sits unresolved forever for players; prerequisite checks read RESOLVED completion.

**Branch-exclusivity verdict (tested Jul 10):** there is no grant-only door into a public quest in the current engine. Phantom prerequisites prune the granted tracker; hidden buffer quests persist but cannot self-resolve; questType-based hiding either surfaces somewhere or risks engine auto-assignment (mission/errand/crime generators, daily/tier/exam/starter systems). **Working pattern for one-playthrough branching: a single quest record with branch subgraphs and multiple terminals; per-ending payouts on objective-level rewards on the terminal nodes.** Multi-record branching requires an upstream engine change (e.g. auto-resolving quests with no player-facing objectives).


## Addendum (Jul 10 2026, source extraction): the quest engine from the repo (AUTHORITATIVE)

Extracted from the full TNR repo drop. Sources: `app/src/libs/quest.ts`, `app/src/server/api/routers/quests.ts`, `app/src/validators/objectives.ts`, `app/src/libs/train.ts`, `app/src/utils/permissions.ts`. This section supersedes any conflicting earlier claim. (Doc is at the three-addenda fold trigger per 60_PROCESS A2: fold on next quest-free session.)

### The eligibility filter (`isAvailableUserQuests`) - one filter rules everything
ALL of the following must pass, and the SAME filter governs public listing, startQuest, AND the active-quest prune (`getUserQuests` runs it on every user fetch with `ignorePreviousAttempts=true`):
1. **hidden**: `!hidden || canPlayHiddenQuests(role)`. Staff roles that can play hidden quests: CONTENT, BALANCE, HEAD_CONTENT, HEAD_BALANCE, EVENT, HEAD_EVENT, CODER, OWNER, CODING-ADMIN, CONTENT-ADMIN, EVENT-ADMIN. For everyone else a hidden quest fails eligibility EVERYWHERE, including as an already-granted active quest.
2. **endsAt** in the future (or null). `startsAt` is checked at startQuest only.
3. **maxCompletes / maxAttempts**: enforced only for `QuestTypesWithMaxAttempts = [event, story, battlepyramid, starter, raid]` (confirms 3.4c). Attempts ignored for the active-quest prune.
4. **requiredVillage**: null, or equals user's villageId, or (requiredVillage == VILLAGE_SYNDICATE_ID `ryBk0qD4EgvPPyav2K4OC` and user is outlaw).
5. **requiredBloodlineId**: null or matches.
6. **medical/hunting/gathering rank**: user's derived profession rank >= quest's.
7. **level window**: requiredLevel <= level <= maxLevel (uses originalLevel for combat-scaled users).
8. **prerequisiteQuestId**: null, or user's completedQuests contains it with `completed === 1` (RESOLVED completion, not merely started).
Failure messages are per-check and human-readable; the 400/pruned reason is always one of these.

### The prune, precisely
`getUserQuests` filters the user's ACTIVE quests through the eligibility filter on effectively every server interaction. Consequence (source-confirms the Jul 10 live finding): a granted quest whose prerequisite is unmet, or a hidden quest on a non-staff account, is silently dropped from the active set on the next touch. There is no grant-only door into a public quest without an engine change.

### startQuest guards (in order, all live-confirmed contracts)
`quests.startQuest {questId, userSector}`: user exists; **rank band**: quest `questRank` must be in `availableQuestLetterRanks(user.rank)`: STUDENT=[D], GENIN=[D,C], CHUNIN=[D,C,B], JONIN/ELITE JONIN/ELDER=[D,C,B,A,S,H]; sector match; not banned; the full eligibility filter; startsAt/endsAt window; retryDelay window vs previous attempt's endAt; not already on the quest. Then per-type: **story requires standing in the Global ANBU HQ structure** (`/globalanbuhq`) and caps at `QUESTS_CONCURRENT_LIMIT = 4` concurrent story quests; hunting requires occupation HUNTER (same limit); **battlepyramid concurrency is 1**; starter has its own path.

### Where each questType lists (the surfacing map)
- **story** -> QuestPicker at `/globalanbuhq` ("can only be started here"), via the by-type listing query, results filtered through the eligibility filter (prereq-met + non-hidden-or-staff only).
- **event** -> `quests.allianceBuilding` (village-filtered, level-window).
- **mission, errand, crime, medical, pvp, war** -> `quests.missionHall` (village-filtered, level-window).
- Level windows in listings use `requiredLevel <= level <= maxLevel` at the SQL layer; a maxLevel of 0 delists for everyone.

### Objective schema corrections (validators/objectives.ts)
- `deliver_item.delete_on_complete` defaults **TRUE** (collect_item defaults false).
- Raid objectives require `sector` (no default) and non-empty `opponentAIs` at schema level; `start_battle.opponentAIs` is schema-refined non-empty.
- Dialog `nextObjectiveId` is `[{text, nextObjectiveId?}]`, default `[]`; per-choice nextObjectiveId is optional at schema level.
- Full rewardFields (28 keys) now in 45, including `reward_seichi_silver`, `reward_anbupoints`, `reward_reputation`, `reward_skillpoints`; `reward_village_membership` accepts legacy names and TRANSFORMS them (SHINE->SHIROHANA, GLACIER->HYORIN, SHROUD->AKASUMI, CURRENT->AKIKAZE).

---

# Appendix: source-verified engine semantics (merged from QUEST_ENGINE_ANALYSIS, 2026-07-18)

## 2. Availability: the gating model (the answer to actions vs gates)

- With `consecutiveObjectives: true`, an objective is available iff reachable from the start by walking `selectedNextObjectiveId` links on the tracker. **`done` is never checked on the path.**
- A **dialog** sets its link ONLY when the player picks (client calls `quests.checkRewards {questId, nextObjectiveId: <choiceId>}`; that endpoint doubles as reward collection).
- **Every non-dialog objective with a string `nextObjectiveId` auto-sets its link on the FIRST tracker touch while available, done or not.** Successors of non-dialog nodes co-activate immediately. A chain of non-dialog nodes is therefore entirely live from its first node onward.
- **Consequence: `dialog` is the only sequencing gate in the engine.** Anything that must wait sits directly behind one.


## 6. reset_quest (exact semantics)

Fires every touch while available. With `resetObjectiveId`: removes from the tracker the reset-target's goal AND everything downstream of it along selected links (including, typically, the reset node itself, since the failed battle's fail-route linked to it). Removed goals re-create fresh on the next touch, which means:
- their forward links are gone -> the reset target is the new frontier (a dialog target re-gates everything behind it);
- **their sectors REROLL**: `random` rolls a new sector; `current_sector` re-resolves to wherever the player is standing at that next touch.
Without `resetObjectiveId`: the ENTIRE quest tracker is deleted -> full restart, all sectors reroll.


## 7. The attackers ambush system (semantics differ from opponentAIs!)

Any ACTIVE objective carrying `attackers` rolls each entry on every consequence pass: **`number` here is a PERCENT ambush chance per touch** (`Math.random()*100 < number`), NOT a headcount; `attackers_max_per_battle` caps the spawn; the battle is a RANDOM_ENCOUNTER type. `win_encounter_at_location` (a) only ambushes while the player is in the objective's sector and (b) **only completes from a RANDOM_ENCOUNTER win in that sector** - quest battles do not complete it. So an encounter hunt is: attackers at a high `number` (e.g. 100 = ambush on next touch), win the ambush in-sector.

---

## Unlock graph, reveal pacing, and profession quests (added 2026-07-27)

**One prerequisite, and it makes a tree.** `prerequisiteQuestId` is a single `string|null` (law 38). One parent per quest, any number of children, and all children reveal at once when the parent completes. There is no way to express "opens after both A and B" with prerequisites. Where a second condition is genuinely needed: serialize (hang the record off the later beat and let a linear spine carry the rest transitively), use an orthogonal gate field (`huntingRank`, `gatheringRank`, `requiredLevel`, `requiredRank`, `requiredVillage`, `requiredBloodlineId`), or check possession in a `deliver_item` node.

**Reveal at most two open records per beat.** The next story step, and at most one area. Profession-gated records do not count. A single beat revealing nine records is quest overload, and the fix is to chain the extras behind each other rather than hanging them all off the same parent.

**`consecutiveObjectives` goes at data level** (law 37), beside `maxCompletes`, never inside `content`.

**`deliver_item` shows without consuming**, even with `delete_on_complete: true` (live-confirmed). Design gates as possession checks and say so in the node text, or players will hoard against a consumption that never comes.

**Profession quests.** Gate with a real rank; the literal `"NONE"` is inert (law 42). Pay `reward_hunting_experience` or `reward_gathering_experience` on the win node (law 43), or the mission feeds nothing back into the profession. A profession lane wants two shapes: an uncapped standing mission paying a small amount per run, and a capped daily paying more with the chase drop attached.

**Count versus percentage in battle rows** (law 44): `opponentAIs[].number` is a COUNT and caps at 3 combatants; `attackers[].number` in `win_encounter_at_location` is a spawn PERCENTAGE. Never copy a roster row between the two shapes.

## Addendum: harvest Stage 1 facts (2026-08-01, from 52_HARVEST sweep)

- **H19.** `defeat_opponents` accepts `sectorType` of `random` or `enemy_village` ONLY, never `specific`. The full sectorType enum in section 2.1 applies to the other location tasks.
- **H20. Reward-field type discipline:** `reward_village_membership` and `reward_rank` must be STRINGS; `reward_gathering_items` and `reward_hunter_items` must be BOOLEANS. Zeroing every reward field to literal 0 breaks the objective union outright - omit or use the correct-typed neutral value.
- **H21.** `move_to_location` canonical write shape: `sectorType: "specific"`, `locationType: "specific"`, `sector` number, `longitude`/`latitude` tiles, `hideLocation` flag.
- **H22.** `win_quest` / `fail_quest` nodes do NOT conflict with `questType: battlepyramid` - verified against live server behavior. The Quest Helper UI raises warnings here; the UI is WRONG. Ignore it.
- **H23.** `deliver_item` checks keys without consuming them. Hidden items are invisible in inventory even on staff accounts, so a hidden key silently fails its own deliver gate during testing - unhide the key or use a staff-visible copy when testing.
- **Dialog choices-array law is universal** (section 2 table updated): the old battlepyramid-only scoping was wrong; the shape broke three separate builds before being settled. Now lint L29.


### 6.2b Dialog text is HTML, and choices must have consequences (2026-08-26)

**Node `description` renders as HTML, not plain text.** Newlines do nothing. The live house format, confirmed
from the Copies, Not Thefts record:

```
<i> Stage direction, present tense, sets the room and puts one thing in motion. </i> <br> <br>
"Speech, in quotes, from whoever is in the scene." <br>
A second line if the beat needs one.
```

Block one is narration in `<i>`, then `<br> <br>`, then a voice. A dialog node with no voice in it is a
caption, not a scene. Choice text is a line a person would say, never a menu label: "A cat hunt. You owe me
tea for this." does characterisation work that "Accept" cannot.

**Every multi-choice dialog must fork to DISTINCT targets.** A menu whose options all lead to the same node
teaches the player their input is decorative, which is worse than not offering the choice. If the player asks
why, the next scene answers why; if they make a sharp remark, the NPC answers the remark. Two answers may
reconverge afterwards, but each needs its own beat first. This is mechanically checkable and should be linted
and then coded: reject at expand time.

**Single-choice nodes still need acknowledgement.** If the player says "stay at my left shoulder", the next
scene has her at their left shoulder. Cheap, and it is what makes the choice feel heard.

**Player-facing text carries no mechanics.** No "all three routes end in a fight", no node or reward language.
State the danger in the fiction: eyes you cannot see yet, people standing very still in the cold.
