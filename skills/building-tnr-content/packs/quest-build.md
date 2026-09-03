<!-- RENDERED pack 'quest-build' from quest.md@c012b6d + pipeline.md@f49e49f via build_packs.py - edit the sources, never this file -->
# Pack: quest-build

Minimal set for a quest/event create or edit that ends in a push. SKILL doctrine block first, this pack second; mission.py/factory.py construct, 45c/45d own shapes. Depth on demand via references/_toc/quest.json slices: sequencing engine internals, eligibility/prune/surfacing, task vocabulary, data-model prose, design philosophy (dauntless directs). Pipeline relocated laws enforced by validate --parity + harvest verify.

<!-- pack-trace: quest.md @c012b6d '1. The objective graph' -->
## 1. The objective graph

A quest body is a list of **objectives** (nodes). Each node does one thing (talk, choose, collect, fight, reset, win) and points at the next node by id. The set of nodes plus their pointers forms a directed graph the engine walks.

---

<!-- pack-trace: quest.md @c012b6d '1.1 Edges and pointers' -->
### 1.1 Edges and pointers
Each node can carry up to three pointers:
- `nextObjectiveId` - where to go on success. Counts as an incoming edge to its target.
- `failObjectiveId` - where to go on failure (used by battles). Counts as an incoming edge to its target.
- `resetObjectiveId` - where a `reset_quest` node sends the player. **Does NOT count as an incoming edge.**

---

<!-- pack-trace: quest.md @c012b6d '1.2 Flow validation (the rule that rejects quests)' -->
### 1.2 Flow validation (the rule that rejects quests)
The engine requires **exactly one starting objective**: exactly one node with no incoming edge. Incoming edges are counted from `nextObjectiveId` and `failObjectiveId` only. Because `resetObjectiveId` does not count, a node that is reachable *only* through a `reset_quest` pointer looks like a second start and the whole quest is rejected.

Rejection looks like this (note the HTTP status is still 200):
```
{"success": false, "message": "Objective flow invalid: Multiple starting objectives found: <ids>"}
```

**Fix pattern:** never point a `reset_quest` at an otherwise-orphan retry node. Point `resetObjectiveId` at an **in-flow** node that already has a real incoming edge, normally the dialog that precedes the failed battle. That keeps the retry path inside the graph and preserves the single start.

---

---

<!-- pack-trace: quest.md @c012b6d '2. Objective types' -->
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

---

<!-- pack-trace: quest.md @c012b6d '3. Battle objectives' -->
## 3. Battle objectives

This is the most error-prone area. Read the subsection for your quest type: generic quests use `defeat_opponents` (3.2); the `battlepyramid` type uses chained `start_battle` (3.7).

---

<!-- pack-trace: quest.md @c012b6d '3.1 `start_battle`: an instant ACTION, legitimate anywhere when dialog-gated (source-verified)' -->
### 3.1 `start_battle`: an instant ACTION, legitimate anywhere when dialog-gated (source-verified)

The engine classifies `start_battle` as an **InstantTask** alongside `win_quest`/`fail_quest`: it is an action that EXECUTES on every tracker touch while available (and tracker touches happen on virtually every server interaction), not a goal the player works toward. It is not location-gated; coordinates on the node are vestigial.

- **A dialog directly before a start_battle genuinely gates it**: the battle is not *available* until the player picks the choice, and availability is the trigger. This supersedes the older "max one per generic quest / dialogs do not gate" rule, which was the observed behavior of UNGATED chains: non-dialog objectives auto-link forward on first touch (3.4b.2), so an ungated chain of start_battles is entirely available at once, they all fire, and only the first becomes a real battle.
- **Shield doctrine (required):** every `start_battle`, in every quest type, sits DIRECTLY behind a `dialog`. Multiple start_battles are fine when each is dialog-gated and the walked path can only make one available at a time (battlepyramid was never special; it just always followed this shape). A start_battle placed as the FIRST objective fires the moment the quest is accepted; use that only for deliberate ambush openers.
- **Loss handling:** the battle outcome is matched against `completionOutcome` (Win/Lose/Flee/Draw/Any). A non-matching outcome WITH `failObjectiveId` fail-routes the objective (its link is set to the fail target and it completes). A LOST start_battle additionally sets an internal `recentlyDied` flag that blocks auto-refire; the client offers a retry that clears it and re-enters combat. A lost start_battle WITHOUT `failObjectiveId` strands on that retry button, so always set it.
- **Choosing the primitive:** `start_battle` = the fight begins the instant the player commits (a confrontation dialog choice), cinematic, no travel. `defeat_opponents` (3.2) = the fight lives on the map and the player travels to it. Both complete from the same combat feedback (the engine reports the outcome to both task types).

---

<!-- pack-trace: quest.md @c012b6d '3.2 `defeat_opponents` is the primitive for scripted and sequential battles (generic quests)' -->
### 3.2 `defeat_opponents` is the primitive for scripted and sequential battles (generic quests)
- It **is location-gated**: the player travels to a tile and the fight happens there. Multiple `defeat_opponents` nodes sequence correctly when each is reached in turn.
- The node is large (54 keys) and **must include `failObjectiveId`.** A missing `failObjectiveId` is one cause of the battle re-arming in a loop. (`failObjectiveId` is optional in the server schema, so the server never catches its absence; the guard is on us.)
- **Re-arm loop cause:** `sectorType: "enemy_village"` ties the fight to a persistent hostile village that re-engages, and/or a missing `failObjectiveId`. The proven non-looping configuration is `sectorType: "random"` with `failObjectiveId` present.

---

<!-- pack-trace: quest.md @c012b6d '3.3 opponentAIs encoding' -->
### 3.3 opponentAIs encoding
The opponent block is:
```json
{ "ids": ["<ai_id>"], "number": <head_count>, "quantity": 1 }
```
`number` is the headcount for that entry (`number: 2` produces two attackers). `quantity` stays `1`. Multiple entries in the `opponentAIs` array put several **distinct** AIs in one fight: `[{ids:[A],number:1,quantity:1},{ids:[B],number:1,quantity:1}]` is a two-enemy fight of A plus B. (The earlier reading of `number` as a per-wave quantity was wrong.)

The `{ids, number, quantity}` shape is shared with reward bundles, but the semantics differ by context (source-confirmed): in `opponentAIs`, `number` is the headcount; in `reward_items` and loot tables, `number` is the drop chance % (default 100) and `quantity` is the amount granted.

---

<!-- pack-trace: quest.md @c012b6d '3.4 Same-sector activation and dispersal (generic quests)' -->
### 3.4 Same-sector activation and dispersal (generic quests)
When the player enters a sector, the engine **activates every location objective pinned to that sector at once.** Two `defeat_opponents` nodes in the same sector will co-fire, and dialogs between them do NOT disperse them. To make battles happen one at a time, put them in **different sectors.** `sectorType: "random"` lets the engine assign a random sector per node, which naturally spreads them out.

---

<!-- pack-trace: quest.md @c012b6d '3.4b consecutiveObjectives, dates, and the launch fields (2026-07-18, paid for live)' -->
### 3.4b consecutiveObjectives, dates, and the launch fields (2026-07-18, paid for live)

**`consecutiveObjectives: true` is REQUIRED explicitly on EVERY quest create.** The field is schema-required with no default; the DB default is false, which makes every objective simultaneously live: `win_quest` nodes become trivially claimable and the `checkRewards` tracker tick pays their rewards whenever it fires (observed live: a component paid at battle START). The reward-timing rules elsewhere in this guide assume consecutive mode and are only true under it. Every full-record convert must preserve the field.

**`startsAt`/`endsAt` accept plain `YYYY-MM-DD` only** (regex-enforced; ISO datetimes 400 the fill). Launch pattern: one convert setting `hidden: false`, both dates, `maxAttempts`/`maxCompletes` (both cap 100), with the nine player items unhidden in the same manifest.

**Scene rendering split:** the travel-page quest popup renders the TOP-LEVEL `content.sceneBackground` only; per-node scene fields render in the quest view proper. Never leave the top-level scene empty (the client fallback is arbitrary); set a deliberate global scene, typically the entry/exterior.

---

<!-- pack-trace: quest.md @c012b6d '3.4b-2 CYOA branch doctrine (the wings pattern)' -->
### 3.4b-2 CYOA branch doctrine (the wings pattern)

Choices must close doors, or the graph is a menu wearing a maze's clothes. Reference implementation (Crimson Masquerade): the three ENTRANCES open different wings, each reaching only 3-4 of the seven endings, which partitions the reward components and forces evening rotation by construction. Supporting rules: gossip/flavor nodes take a SINGLE forward continuation (never re-offer the full choice menu); knowledge gates drop RATES, never skips fights (no combat-free farm loop may exist once answers hit Discord); exclusive intel picks (one indulgence per run) make information a committed choice paying off in a future run.

---

<!-- pack-trace: quest.md @c012b6d '3.4c Quest gate field caps (server schema, live-verified)' -->
### 3.4c Quest gate field caps (server schema, live-verified)

`maxLevel`, `maxAttempts`, and `maxCompletes` are all capped at **100** by the quest write schema; larger values 400 the whole fill. Additionally, `maxAttempts`/`maxCompletes` are only ENFORCED for questTypes in `QuestTypesWithMaxAttempts = [event, story, battlepyramid, starter, raid]`: `mission`/`errand`/`crime` repeatables ignore both caps entirely (their frequency governance is the engine's daily counters). Consequence: a daily battlepyramid has a hard lifetime ceiling of 100 completions per player; only an upstream code change can raise it.

---

<!-- pack-trace: quest.md @c012b6d '3.4d Quest EDITS reproduce the full record' -->
### 3.4d Quest EDITS reproduce the full record

The quest edit path does not fetch-merge top-level fields: partial edits 400 with undefined name/description/tierLevel/questType. Reproduce the complete quest data object from a live capture with only your changes applied (Howling Hills rule). hidden must be reproduced from live truth to avoid flipping a public quest.

---

<!-- pack-trace: quest.md @c012b6d '3.4e War reward fields' -->
### 3.4e War reward fields

reward_war_damage and reward_war_healing are valid objective-level and quest-level reward fields (summed across objectives). Verified pattern: a war mission pays war damage on its aftermath dialog. defeat_opponents accepts sectorType enemy_village for fights on enemy ground.

---

<!-- pack-trace: quest.md @c012b6d '3.5 Lose-retry pattern' -->
### 3.5 Lose-retry pattern
To let a player retry a lost battle instead of failing the quest:
```
battle (failObjectiveId -> reset node)
  -> reset_quest (resetObjectiveId -> the dialog that precedes the battle)
    -> dialog -> battle
```
The `reset_quest` points back at an in-flow dialog (not at an orphan), which both gives the retry and satisfies flow validation (1.2). This is the same in generic and battlepyramid quests.

---

<!-- pack-trace: quest.md @c012b6d '3.6 reset_quest node shape' -->
### 3.6 reset_quest node shape
A `reset_quest` node is 32 keys: a 25-field reward block (usually zeroed), `resetObjectiveId`, and the scene fields. It has no `nextObjectiveId`. The reward block being present does not mean it grants a reward; leave the values at zero unless a partial-credit reset is intended (a balance decision).

---

<!-- pack-trace: quest.md @c012b6d '3.7 The `battlepyramid` quest type (dialog-gated single battles)' -->
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

---

<!-- pack-trace: quest.md @c012b6d '4.1 Complete top-level create payload (copy this shape)' -->
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

---

<!-- pack-trace: quest.md @c012b6d '5. Quest tRPC contract' -->
## 5. Quest tRPC contract

Envelope rules and the batch format are in `10_TECH_pipeline.md`. Quest-specific shape:

**To build a whole event as one submission** (its jutsu, AI enemies, and the quest together), the quest is one entry in a combined builder manifest: see `10_TECH_pipeline.md` section 1.5. In that form the quest's `opponentAIs` carry `@ai` refs to the AI entries and the quest icon carries an `@img` ref. Scene backgrounds and characters ride the manifest as `entity: "asset"` entries whose art uploads through `@img`; each node's `sceneBackground` and `sceneCharacters` then reference them by `@scene:<srcId>` (or a literal id to reuse an existing one). See 10_TECH 1.5 and 2.7.

| Op | Method | Shape |
|---|---|---|
| `quests.get` | GET | full quest definition. |
| `quests.create` | POST | null-body envelope, returns new id in `message`. |
| `quests.update` | POST | `{json:{id,data}, meta:{values: dates, referentialEqualities: <7 mappings>, v:1}}`. |

---

<!-- pack-trace: quest.md @c012b6d '5.1 The flatten rule (the builder does this automatically)' -->
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

---

<!-- pack-trace: quest.md @c012b6d '5.2 Read json.success, not the HTTP status' -->
### 5.2 Read json.success, not the HTTP status
`quests.update` returns HTTP 200 even when validation fails (flow-invalid, a missing top-level field, missing equalities, and so on). Always read `json.success` and `json.message`. Builder v4.12 does this per entry and shows the server's message on red rows (and its preflight catches flow-invalid graphs before anything is pushed); older builds reported a 200 as "ok" and hid a rejected save, which could leave an empty quest shell that looks created but is not.

---

---

<!-- pack-trace: quest.md @c012b6d '6.2 Writing rules' -->
### 6.2 Writing rules
- Keep dialog short and readable, usually 1 to 3 sentences. Avoid long lore dumps and abstract language with no visible player action.
- **No em dashes in player-facing dialog text** (a dialog node's `description` and a choice's `text`). This is the one place em dashes are banned; the rest of the stack, prose, and code may use them. Use commas, colons, or hyphens in dialog instead.
- **Wrong choices should teach the logic:** route back (reset), explain why the assumption was wrong, and reinforce the theme.
- **Correct choices should advance and clarify** the lesson.
- **Breadcrumbs should be short and memorable.** Do not reveal a faction's full name too early unless this is the finale.
- Always name enemies and quest items in objective text.

---

<!-- pack-trace: quest.md @c012b6d '6.2b Dialog text is HTML, and choices must have consequences (2026-08-26)' -->
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

---

<!-- pack-trace: quest.md @c012b6d '7.1 Reference generic quest (copy for `defeat_opponents` chains)' -->
### 7.1 Reference generic quest (copy for `defeat_opponents` chains)
**Echoes of the Fool - copy**, id `70qYRdS4SJVYpCIr0S1S5`, `questType: event`, 16 objectives. A dialog-wrapped chain of three `defeat_opponents` battles, each `sectorType: "random"` and landing in a different sector (336 / 146 / 21). Each battle is preceded by a dialog offering a fight-or-quit choice; the quit branch routes to a `reset_quest` back to the start dialog. Canonical non-looping, flow-valid sequential multi-battle pattern.

---

<!-- pack-trace: quest.md @c012b6d '7.2 Reference battlepyramid (copy for chained `start_battle`)' -->
### 7.2 Reference battlepyramid (copy for chained `start_battle`)
**Kaeruun's Pyramid**, id `-i3wNG4zgJhtGybbsPU-0`, `questType: battlepyramid`, 12 objectives. Dialogs interleave with `start_battle` floors, each floor's `failObjectiveId` routing to a shared `reset_quest` back to the start dialog, ending at a one-enemy boss `start_battle` into `win_quest`. This is the shape section 3.7 describes. **The Drowned Fleet** (in `44_DATA_id_registry.md`) is the worked build: 24-plus nodes, three ship stages, one dialogue per background, per-stage resets.

---

<!-- pack-trace: quest.md @c012b6d '8. QA checklist (before any quest push)' -->
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

---

<!-- pack-trace: quest.md @c012b6d 'startQuest guards (in order, all live-confirmed contracts)' -->
### startQuest guards (in order, all live-confirmed contracts)
`quests.startQuest {questId, userSector}`: user exists; **rank band**: quest `questRank` must be in `availableQuestLetterRanks(user.rank)`: STUDENT=[D], GENIN=[D,C], CHUNIN=[D,C,B], JONIN/ELITE JONIN/ELDER=[D,C,B,A,S,H]; sector match; not banned; the full eligibility filter; startsAt/endsAt window; retryDelay window vs previous attempt's endAt; not already on the quest. Then per-type: **story requires standing in the Global ANBU HQ structure** (`/globalanbuhq`) and caps at `QUESTS_CONCURRENT_LIMIT = 4` concurrent story quests; hunting requires occupation HUNTER (same limit); **battlepyramid concurrency is 1**; starter has its own path.

---

<!-- pack-trace: quest.md @c012b6d 'Objective schema corrections (validators/objectives.ts)' -->
### Objective schema corrections (validators/objectives.ts)
- `deliver_item.delete_on_complete` defaults **TRUE** (collect_item defaults false).
- Raid objectives require `sector` (no default) and non-empty `opponentAIs` at schema level; `start_battle.opponentAIs` is schema-refined non-empty.
- Dialog `nextObjectiveId` is `[{text, nextObjectiveId?}]`, default `[]`; per-choice nextObjectiveId is optional at schema level.
- Full rewardFields (28 keys) now in 45, including `reward_seichi_silver`, `reward_anbupoints`, `reward_reputation`, `reward_skillpoints`; `reward_village_membership` accepts legacy names and TRANSFORMS them (SHINE->SHIROHANA, GLACIER->HYORIN, SHROUD->AKASUMI, CURRENT->AKIKAZE).

---

# Appendix: source-verified engine semantics (merged from QUEST_ENGINE_ANALYSIS, 2026-07-18)

---

<!-- pack-trace: quest.md @c012b6d '2. Availability: the gating model (the answer to actions vs gates)' -->
## 2. Availability: the gating model (the answer to actions vs gates)

- With `consecutiveObjectives: true`, an objective is available iff reachable from the start by walking `selectedNextObjectiveId` links on the tracker. **`done` is never checked on the path.**
- A **dialog** sets its link ONLY when the player picks (client calls `quests.checkRewards {questId, nextObjectiveId: <choiceId>}`; that endpoint doubles as reward collection).
- **Every non-dialog objective with a string `nextObjectiveId` auto-sets its link on the FIRST tracker touch while available, done or not.** Successors of non-dialog nodes co-activate immediately. A chain of non-dialog nodes is therefore entirely live from its first node onward.
- **Consequence: `dialog` is the only sequencing gate in the engine.** Anything that must wait sits directly behind one.

---

<!-- pack-trace: quest.md @c012b6d '6. reset_quest (exact semantics)' -->
## 6. reset_quest (exact semantics)

Fires every touch while available. With `resetObjectiveId`: removes from the tracker the reset-target's goal AND everything downstream of it along selected links (including, typically, the reset node itself, since the failed battle's fail-route linked to it). Removed goals re-create fresh on the next touch, which means:
- their forward links are gone -> the reset target is the new frontier (a dialog target re-gates everything behind it);
- **their sectors REROLL**: `random` rolls a new sector; `current_sector` re-resolves to wherever the player is standing at that next touch.
Without `resetObjectiveId`: the ENTIRE quest tracker is deleted -> full restart, all sectors reroll.

---

<!-- pack-trace: quest.md @c012b6d '7. The attackers ambush system (semantics differ from opponentAIs!)' -->
## 7. The attackers ambush system (semantics differ from opponentAIs!)

Any ACTIVE objective carrying `attackers` rolls each entry on every consequence pass: **`number` here is a PERCENT ambush chance per touch** (`Math.random()*100 < number`), NOT a headcount; `attackers_max_per_battle` caps the spawn; the battle is a RANDOM_ENCOUNTER type. `win_encounter_at_location` (a) only ambushes while the player is in the objective's sector and (b) **only completes from a RANDOM_ENCOUNTER win in that sector** - quest battles do not complete it. So an encounter hunt is: attackers at a high `number` (e.g. 100 = ambush on next touch), win the ambush in-sector.

---

---

<!-- pack-trace: quest.md @c012b6d 'Relocated engine laws (2026-08-28)' -->
## Relocated engine laws (2026-08-28)

Verbatim law text moved out of project knowledge. Stage 3 splices these into the
owning skill reference. Numbers stay canonical against /docs/ENGINE_LAWS.md.

23. **`consecutiveObjectives: true` MUST be set explicitly on every quest create.** The field is required with no schema default; the DB default is false = every objective simultaneously live = win_quest nodes trivially claimable = rewards pay on the next tracker tick (e.g., at battle START). This single field was the "reward before the kill" bug.

24. **`checkRewards` is a tracker tick, not a victory hook.** With consecutive=true, win-node rewards pay at genuine completion; with false, they pay whenever the tracker looks.

25. **The travel-page quest popup renders top-level `content.sceneBackground` only.** Per-node scenes render in the quest view. Never leave the top-level scene empty; the client fallback is arbitrary. Set a deliberate global scene (typically the entry/exterior).

26. **Reset nodes return the player; battle failObjectiveId overrides optimistic advancement.** Battle->win edges are safe under consecutive=true without gate dialogs.

27. **CYOA doctrine (design law, engine-compatible):** choices must close doors. Entrance wings that partition the fates beat a shared hub menu; gossip/flavor nodes take single forward continuations, never re-offer the full menu; knowledge gates RATES, never skips fights (no combat-free farm loop may exist); exclusive intel picks (one per run) make information a committed choice.

37. **`consecutiveObjectives` lives at DATA level, beside `description` and `maxCompletes`, never inside `content`.** Law 23 established that the field is required; this is where it goes. A copy nested in `content` is silently ignored and restores the reward-before-the-kill bug in full.

38. **`prerequisiteQuestId` is a single `string|null`, not an array.** The unlock graph is therefore a TREE: one parent per quest, any number of children, and every child reveals the moment the parent completes. "Opens after both A and B" cannot be expressed with prerequisites. Second conditions come from orthogonal top-level fields that stack on the prerequisite (`huntingRank`, `gatheringRank`, `requiredLevel`, `requiredRank`, `requiredVillage`, `requiredBloodlineId`) or from a possession check in a `deliver_item` node.

42. **`huntingRank` and `gatheringRank` accept the literal `"NONE"`, which is truthy in code and inert as a gate.** A record carrying `gatheringRank: "NONE"` reads as gated to any naive check and is open to every player in fact. Omit the field entirely rather than writing NONE.

43. **`reward_hunting_experience` and `reward_gathering_experience` are valid objective-level reward fields.** A profession mission that omits them pays materials but feeds nothing back into the profession it is gated on.

44. **`win_encounter_at_location.attackers[].number` is a PERCENTAGE (spawn chance); `defeat_opponents.opponentAIs[].number` is a COUNT.** The two shapes look identical in JSON. A roster row copied from one to the other becomes a fight specifying one hundred enemies; this happened twice, in two separate files, and survived every structural check that did not sum the field.

47. **`reset_quest` and `win_quest` descriptions NEVER display.** Both are silent transitions. Every rewind needs a dialog node immediately before it telling the player they were wrong, and every quest needs a payoff dialog before the win node or the story ends on the previous screen. Source: play testing, confirmed twice.

48. **One scene character per node.** The client renders every entry in `sceneCharacters` at `absolute bottom-0 w-2/5` with no horizontal offset, so multiple characters stack in the same spot. Treat it as a hard one-per-scene constraint.

49. **`sceneCharacters` resolves gameAsset ids ONLY.** An AI's userId renders nothing at all (silent). An AI that appears in dialog needs a SCENE_CHARACTER asset record in ADDITION to its avatar.

51. **A scene character's apparent size is its share of its own canvas.** A small subject (a cat, a child) needs transparent padding above it or the client scales it to human height.

52. **Node-level `image` is the sector map pin.** `libs/threejs/sector.ts drawQuest` returns early when the objective has no image, so NO image means NO pin. The marker behind it is tinted by task (travel yellow, collect and deliver purple, defeat red), so pins must carry meaning through silhouette, not colour. Dialog nodes draw no marker worth guiding to.

53. **The logbook objective badge is static.** `getObjectiveImage` reads `objectiveImageMap[task]` and never consults `objective.image`. The world map (Map.tsx) likewise uses a fixed icon per highlight type. Roughly 1,150 live dialog nodes carry an image value that renders nowhere.

54. **`locationType: "specific"` with longitude/latitude 0 places the objective at tile 0,0.** The engine only randomises when locationType is `random`. Every location node needs real coordinates or the player never walks anywhere and never sees a pin. Sector is 26x26; keep stops two or more tiles off every edge.

    **[AMENDED 2026-08-28]** For `collect_item` this is fatal rather than cosmetic: an Action self-resolves at the timer and requires the player to stand on the tile for the whole duration (`34b`), and tile 0,0 is outside the playable margin, so the Action can never complete. **Battles take real coordinates too**: live `Copies, Not Thefts` places `l2` at 16,12 and `c5` at 12,16, and a fight may share a tile with the Action before it (`c4` and `c5` are both 12,16). Live `Lantern Rounds` places Actions and travel at 5,4 / 4,7 / 8,16 as `specific` + `user_village`. Enforced by `validate.py` since 2026-08-28, scoped by task.

55. **`sectorType: "random"` on a battle node teleports the player to an arbitrary sector.** [CONFIRMED LIVE 2026-08-28: `Night Watch Shadow` still ships this today, so the cloned-template pattern below is in the game right now. Enforced by `validate.py`.] Cloned battle templates carry it. Use `user_village` for anything meant to stay local.

56. **`collect_time_minutes` is a float** (`z.coerce.number().min(0).max(60)`, no integer constraint) and the engine compares `secondsPassed / 60`, so 0.1 is 6 seconds. The notification prints the raw value ("0.5 minutes"), which is ugly but harmless. It is the ONLY timed task in the vocabulary.

57. **Quest `updatedAt` is not maintained on update.** It still read 2024 after multiple successful edits. Never use it as a change indicator for quests (it remains reliable for jutsu).

58. **The in-game quest editor overwrites whatever it holds.** A save from the editor form rewrote every node's `image` with task badge defaults and, on a separate occasion, the quest name, with no trace in any results bundle. Push content BEFORE editor tweaks, or re-harvest after them.

85. **Every dialog objective must carry at least one option.** The flow validator rejects a dialog with an empty or absent `nextObjectiveId`: *"Dialog objective 'e16' must have at least one option."* Confirmed against live `Witness Detail` (`m3` is a dialog with one option) and live `Copies, Not Thefts` (every dialog has options). Enforced by `validate.py`.

86. **A quest terminates on `win_quest`, never on a dialog.** `win_quest` is one of the few tasks permitted to carry no next, and it is what actually marks the quest complete; `fail_quest` and `reset_quest` are the other terminals. Twenty-two endings authored as terminal dialogs were all rejected. Live `Witness Detail` ends at `m4`, live `Copies, Not Thefts` at `d5`. Enforced by `validate.py`.

87. **The objective graph must be acyclic.** The flow validator rejects any back edge: *"Cycle detected in objective chain."* Fail loops, dead-end leads returning to a hub, and battle retries are all cycles when expressed as `nextObjectiveId`. Both live quests inspected are completely acyclic. Enforced by `validate.py`.

88. **Loops are legal only through `reset_quest`, and must never land on a battle node.** `resetObjectiveId` is a separate field, not a graph edge, so it does not close a cycle. Live practice always resets to the node BEFORE the fight: `Copies, Not Thefts` sends `l2` fail to `l4` which resets to `l1` (dialog), and `c5` fail to `c6` which resets to `c4` (collect_item). Resetting onto a `defeat_opponents` node has no live precedent; treat it as illegal. Thirty-seven back edges in one wave collapsed to seventeen shared reset nodes. Enforced by `validate.py`.

89. **`sector` is a column default, not a value. Never write it.** Every live location node reads `sector: 0` across three different `sectorType` values, including `current_sector` and `random`, where 0 cannot describe the real sector. The engine resolves the sector from `sectorType`. Writing it buys nothing and is actively wrong the moment `sectorType` is not `user_village`. Knowledge only: an omission is not mechanically detectable.

- the tRPC surface the builder replays -> `45f_DATA_procedures.json`

**With the caveat that law 83 attaches to all of it:** a generated value is what the code compiles in. For the `DMG_*` family that is a default the live database may already have overridden.

---

<!-- pack-trace: pipeline.md @f49e49f '2.1 Request envelope and conventions' -->
### 2.1 Request envelope and conventions

- TNR uses tRPC batch links. **Every POST body is a batch envelope:** `{"0": { "json": <payload>, "meta": <meta> }}`.
- **Create endpoints take a null-body envelope** (`{"json": null, "meta": {"values": ["undefined"], "v": 1}}`) and **return the new id in the response `message` field** (exception: `item.create`, see 2.3).
- **Update endpoints** take `{"json": {"id": <id>, "data": <data>}, "meta": <meta>}`. The `meta` typically flags `createdAt`/`updatedAt` as Dates.
- **GET list endpoints** (`*.getAll`) are `?batch=1&input=<urlencoded {"0":{"json":{cursor,limit}}}>` and page via `nextCursor`.
- HTTP 200 does not mean success. Read `json.success` and `json.message`.

---

<!-- pack-trace: pipeline.md @f49e49f '2.5 Quest' -->
### 2.5 Quest

| Op | Method | Shape |
|---|---|---|
| `quests.get` | GET | returns the full quest definition. |
| `quests.create` | POST | null body -> new id in `message`. |
| `quests.update` | POST | `{json:{id,data}, meta:{values: dates, referentialEqualities: <7 mappings>, v:1}}`. |

**Flatten rule (the builder does this automatically):** on update, `data` must carry BOTH the nested `content` blob AND a flat top-level copy of every `reward_*` field plus `sceneBackground`/`sceneCharacters`, same values duplicated. The `meta.referentialEqualities` must declare 7 array fields, each top-level array pointing at its `content` twin (`data.sceneCharacters` -> `data.content.sceneCharacters`; `reward_jutsus`/`reward_badges`/`reward_items`/`reward_hunter_items_ids`/`reward_gathering_items_ids`/`reward_bloodlines` -> their `content.reward.*`). Full objective-node schemas and the flow-validation rules live in `23_GUIDE_quest.md`.

---

<!-- pack-trace: pipeline.md @f49e49f '3. Rate limit' -->
## 3. Rate limit

The limiter is a **rolling cumulative request-count budget**, not per-burst. It drains across repeated sessions and refills over time. Use fewer, larger requests with exponential backoff (the builder does this), and let it refill rather than hammering.

---

<!-- pack-trace: pipeline.md @f49e49f '4. id-fetch and capture-first discipline' -->
## 4. id-fetch and capture-first discipline

- Pull live ids from edit URLs (`/manual/ai/edit/[id]`, `/manual/asset/edit/[id]`, the item editor) or from catalog dumps.
- For names to ids, dump the relevant catalog and resolve from the JSON.
- After a builder run, the status rows show `-> <id>` and the idmap holds `srcId -> createdId`; copy those into dependent content (e.g. chest ids into a quest branch reward).
- To verify a new or changed contract, run it once in the editor, capture the call, and confirm `json.success` before building a generator. A 500 with a clear column message (e.g. the `battleDescription` case) still teaches the exact field rule.

---

<!-- pack-trace: pipeline.md @f49e49f '5. Universal gotcha checklist' -->
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

---

<!-- pack-trace: pipeline.md @f49e49f 'Addendum: push-path rules learned in the field (Tower / Howling builds)' -->
## Addendum: push-path rules learned in the field (Tower / Howling builds)

- **AI edits never rely on fetch-merge for `jutsus` or `items`.** The builder passes live rows through raw (jutsu objects, UserItem rows with `dropChancePerc`), which the server rejects. Every AI edit sends `jutsus` as string id refs AND `items` as ids-with-number explicitly, even when only touching other fields. Bundle fix (row normalization in the edit merge) queued for the next builder rev.
- **Quest EDITS do not fetch-merge top-level fields.** A partial quest edit reaches the server with `name`/`description`/`questType`/`tierLevel` undefined and 400s. Reproduce the FULL quest record from a live capture with changes applied. (Whole-array rule, promoted to whole-record for quests.)
- **Items: `battleDescription` is DB NOT NULL.** Empty string is nulled by the write path and 500s at the DB. Always non-empty.
- **AI edits require an explicit `targetId`.** The idmap does not resolve srcIds for `ai` edit entries ("ai needs targetId or slot create"); jutsu converts/edits accept srcId via idmap but carry `targetId` anyway when known. Pull the AI id from the idmap dump or edit URL.
- **The jutsu edit/convert merge-base load trips the API rate limiter** (v4.12): even single-entry, targetId-carrying edit manifests stall on "limited 10s" retries. Workarounds until the builder rev (per-id `jutsu.get` merge base + lazy catalog load): make small scalar/effect changes by hand in the admin UI while the jutsu is unequipped, then push a lean re-equip ai edit; keep any builder-path edit manifests to the minimum entries and let the limiter cool between runs.
- **`stun` AP loss is the `apReduction` field, not `power`.** Power is only the stun CHANCE (RNG roll); an omitted `apReduction` silently takes the server default (-10 AP observed live). Always set `apReduction` explicitly on stun effects. Same power-as-chance pattern applies to the whole prevent/control family (shield creation, flee, seal, prevents).
- **Combat internals are documented in 50_DATA_combat_facts.md** (damage formula and constants, 450k/200k battle-init caps incl. AIs, LVL_CAP 100 clamp, the 10% minimum-damage floor and its boost scaling, pierce pipeline bypass, modifier staging order, ai threshold semantics). Read it before any combat balance work; it is calibrated against live fight captures.
