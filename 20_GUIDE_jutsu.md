# 20 - GUIDE: Jutsu Creation

Owner doc for player-facing jutsu: the field schema, the create/update/getAll contracts, the design rules, and mass-edit (sweep) patterns. The effect-object schema and the full tag vocabulary are shared with AI jutsu and live in `21_GUIDE_ai_enemy.md` (sections 7.4 and 4); this guide points there rather than duplicating them. Cross-cutting balance rules are in `30_DOCTRINE_balance.md`. Shared plumbing is in `10_TECH_pipeline.md`.

AI-enemy jutsu are a special case (hidden, `jutsuType: "AI"`, kit-equipped) and are covered end to end in guide 21. This guide is for normal player jutsu, but section 2 (the full field set) and the create-vs-convert rule apply to AI jutsu too.

---

## 1. Jutsu tRPC contract

Envelope rules are in `10_TECH_pipeline.md`. Jutsu-specific:

| Op | Method | Shape |
|---|---|---|
| `jutsu.create` | POST | null-body envelope, returns new id in `message`. |
| `jutsu.update` | POST | `{json:{id,data}, meta:{values:{"data.createdAt":["Date"],"data.updatedAt":["Date"]}, v:1}}`. |
| `jutsu.getAll` | GET | requires a `limit` (number) in the input or it 400s; page via `nextCursor`. |

The builder pattern is create-then-fill: POST a blank `jutsu.create`, read the id from `message`, then `jutsu.update` with your fields.

**Create-fill merges as of builder v4.12.** After `jutsu.create`, the builder GETs the fresh record (`jutsu.get {id}`, source-confirmed) and merges your `data` over its defaults, the same fetch-merge `convert` uses. A partial `create` no longer NaN-fails on a missing required field. Complete payloads (2.1) remain best practice, since server defaults are placeholders (blank name, default image), not content. On v4.11 and older, `create` sent `data` as-is with no merge, and a missing required number coerced to `NaN` and failed with `expected number, received NaN`; that era is why the complete-payload discipline exists.

---

## 2. Jutsu field schema (complete)

The complete set of fields written on `jutsu.update`, captured from a live AI jutsu record and now verified against the server's own write validator (JutsuValidator, extracted from the TNR source). The machine-readable schema with every type, range, default, and enum is `45_DATA_field_schemas.json`. Defaults shown are safe values for an AI-kit jutsu; player jutsu differ where noted (not hidden, real rank, real pool costs, a player `jutsuType`). Do not omit a required field on a `create`.

**Required strings and enums**

| Field | Values | Notes |
|---|---|---|
| `name` | string | Display name. **Must be UNIQUE across all live jutsu.** A duplicate name returns HTTP 200 with `success:false` and leaves a blank `New Jutsu - <id>` shell. See 2.2. |
| `description` | non-empty string | Menu blurb. Empty or missing 400s. |
| `battleDescription` | non-empty string | Combat-log line. Placeholders `%user`, `%target`, `%jutsu`. Empty or missing 400s. |
| `jutsuType` | `"AI"` for enemy kits; a player category otherwise | AI-kit jutsu use `"AI"`. |
| `jutsuRank` | full ladder `D` / `C` / `B` / `A` / `S` / `H` (there is no E rank) | Cosmetic for hidden AI jutsu; prefer `"D"`. |
| `jutsuWeapon` | `NONE`, or one of: `STAFF` `AXE` `FIST_WEAPON` `SHURIKEN` `SICKLE` `DAGGER` `SWORD` `POLEARM` `FLAIL` `CHAIN` `FAN` `BOW` `HAMMER` | This is the JUTSU weapon field; the same 14-value enum as the item `weaponType`. |
| `statClassification` | `Highest` / `Ninjutsu` / `Genjutsu` / `Taijutsu` / `Bukijutsu` | Scaling school. Prefer `"Highest"` for elementals. |
| `battleUsageType` | `PVE` / `PVP` / `BOTH` | Server default `BOTH` when omitted. |
| `target` | `SELF` / `OTHER_USER` / `OPPONENT` / `ALLY` / `CHARACTER` / `GROUND` / `EMPTY_GROUND` | |
| `method` | `SINGLE` / `ALL` / `AOE_CIRCLE_SPAWN` / `AOE_LINE_SHOOT` / `AOE_WALL_SHOOT` / `AOE_LARGE_WALL_SHOOT` / `AOE_CIRCLE_SHOOT` / `AOE_SPIRAL_SHOOT` | `ALL` is all-targets; the `AOE_*` methods are shaped ground patterns. |
| `requiredRank` | `"STUDENT"` for AI | Gating rank to learn or use. |

**Required numbers** (a missing one coerces to `NaN` and 400s)

| Field | Notes |
|---|---|
| `range` | int 0 to 5 (0 self). The validator caps range at 5. |
| `requiredLevel` | int 1 to 100, `1` for AI. |
| `actionCostPerc` | integer `40` or `60` only (doctrine). The validator accepts 10 to 100. |
| `cooldown` | int rounds, 0 to 300. |
| `chakraCost` / `staminaCost` / `healthCost` / `extraBaseCost` | real pool costs (pools 0 to 10000; extraBaseCost 0 to 65535). AI kit jutsu use `0`; the `0.05` value is a placeholder that leaked onto some player jutsu (sweep in 6). |
| `staminaCostReducePerLvl` / `chakraCostReducePerLvl` / `healthCostReducePerLvl` | **required, default `0`.** These three were the recurring NaN culprit; they are easy to forget and non-optional. |

**Required but emptyable (use `""`, not null)**

| Field | Notes |
|---|---|
| `bloodlineId` | `""` when none. The validator accepts string or null; the live record uses empty string. |
| `villageId` | `""` when none. The validator accepts string or null; live uses empty string. |
| `image` | uploaded asset url (or an `@img:<file>` ref the builder resolves). |
| `hidden` | bool. `true` for AI-kit jutsu, `false` for player jutsu. Optional server-side; always send it explicitly. |

**Nullable (default `null`)**

| Field | Notes |
|---|---|
| `requiredBloodlineItemId` | null when none. |
| `parentJutsuId` | null. |
| `injectableInBattle` | bool, default `false`. |
| `requiredStrength` / `requiredSpeed` / `requiredIntelligence` / `requiredWillpower` | stat gates, null when ungated. |
| `requiredNinjutsuOffence` / `requiredNinjutsuDefence` | null when ungated. |
| `requiredGenjutsuOffence` / `requiredGenjutsuDefence` | null when ungated. |
| `requiredTaijutsuOffence` / `requiredTaijutsuDefence` | null when ungated. |
| `requiredBukijutsuOffence` / `requiredBukijutsuDefence` | null when ungated. |

**Array**

| Field | Notes |
|---|---|
| `effects` | array of effect objects (section 3). Damage is itself an effect entry. |

**Builder-managed (do not hand-set)**

`id`, `createdAt`, `updatedAt`. The builder assigns the id, preserves `createdAt` on convert, stamps `updatedAt`, and attaches the Date meta. Display tags are derived from the effects and are not sent.

### 2.1 Complete create payload (copy this shape for a `create`)

An AI-kit jutsu with a single damage effect. Every required field is present; drop nothing when using `slot: "create"`.

```json
{
  "name": "Drowned Water Lash",
  "description": "A whip of water lashes the target.",
  "battleDescription": "%user lashes %target with a whip of water",
  "jutsuType": "AI",
  "jutsuRank": "D",
  "jutsuWeapon": "NONE",
  "statClassification": "Highest",
  "battleUsageType": "BOTH",
  "target": "OTHER_USER",
  "method": "SINGLE",
  "range": 5,
  "requiredRank": "STUDENT",
  "requiredLevel": 1,
  "actionCostPerc": 60,
  "cooldown": 3,
  "chakraCost": 0,
  "staminaCost": 0,
  "healthCost": 0,
  "extraBaseCost": 0,
  "staminaCostReducePerLvl": 0,
  "chakraCostReducePerLvl": 0,
  "healthCostReducePerLvl": 0,
  "bloodlineId": "",
  "villageId": "",
  "requiredBloodlineItemId": null,
  "parentJutsuId": null,
  "injectableInBattle": false,
  "requiredStrength": null,
  "requiredSpeed": null,
  "requiredIntelligence": null,
  "requiredWillpower": null,
  "requiredNinjutsuOffence": null,
  "requiredNinjutsuDefence": null,
  "requiredGenjutsuOffence": null,
  "requiredGenjutsuDefence": null,
  "requiredTaijutsuOffence": null,
  "requiredTaijutsuDefence": null,
  "requiredBukijutsuOffence": null,
  "requiredBukijutsuDefence": null,
  "hidden": true,
  "image": "@img:jutsu_icon.jpg",
  "effects": [
    { "type": "damage", "power": 40, "powerPerLevel": 0, "rounds": 0, "calculation": "formula", "direction": "offence", "target": "INHERIT", "statTypes": ["Highest"], "generalTypes": ["Highest"], "elements": ["Water"] }
  ]
}
```

### 2.1b Formula effects: statTypes AND generalTypes are load-bearing (2026-07-18)

Every formula-calculation effect (`damage`, `pierce`, `wound`) MUST carry BOTH `statTypes` and `generalTypes` (default `["Highest"]` for each, exactly as the 2.1 payload shows). An absent or empty `generalTypes` does not error at create: it detonates the damage formula at runtime into astronomical values (trillions, observed live). This is the single most expensive omission in the stack's history. Generation helpers must be seeded from the 2.1 template verbatim (12_TECH law 31), never freehanded.

### 2.1c Strict unions and live-exemplar composition

The create path is lenient; the update path validates every effect object against its EXACT per-tag schema. Any extra field fails the whole union, including fields legal on other tags: `calculation` on clear/cleanse, `direction: "defence"` on reflect (`direction` is the fixed literal `"offence"` even on defensive tags). Consequence: a record that pushed fine at create can be un-editable as stored. Rule: compose every effect from a LIVE exemplar (catalog 40b or a working capture) and change only values. Canonical lean shapes: `clear`/`cleanse`/`debuffprevent` = `{type, power, rounds}` and nothing else. Full law set: 12_TECH_engine_laws.md section 1.

### 2.1d Converts require explicit targetId

`slot: "convert"` entries MUST carry an explicit `targetId`. srcId + idmap does NOT self-resolve for jutsu converts; without targetId the fetch-merge base is empty and the fill fails on phantom missing fields (`name: undefined` means your targetId is wrong or missing).

### 2.2 Name uniqueness (silent-shell failure)

Catalog-based dedup is ADVISORY ONLY: the trimmed catalogs miss live and hidden records, which collide invisibly (two pool records collided with unlisted live names in 2026-07). Prefer distinctive names over generic ones. Jutsu names are unique in the live database. Creating a jutsu whose name already exists returns HTTP 200 with `success:false` (a "name taken" style message). Builder v4.12 reads `json.success` per entry, so the row now shows red with the server's message; the created record still stays a blank `New Jutsu - <id>` shell that needs cleanup or reuse (the idmap keeps its id, so fixing the name and re-running fills the same shell). Before creating, **dedup the name** against `40_INDEX_jutsu.json` and, for names that may exist outside the trimmed catalog, against a live `getAllNames` capture. When a themed set collides, prefix the whole set with a unique tag (the Drowned Fleet set uses a `Drowned ` prefix). Renaming does not affect equipped-jutsu links, which are by id.

### 2.3 Create vs convert (which payload to send)

- **`create`** (new jutsu): prefer the COMPLETE payload (2.1). As of v4.12 the builder fetch-merges your data over the fresh record's defaults, so a partial create saves; anything you omit stays a server placeholder.
- **`convert`** (edit existing jutsu by id): send ONLY the fields you change. The builder fetch-merges over the live record (section 6). When changing an array field like `effects`, reproduce the whole array from the live record with just your change applied, since the array is replaced, not deep-merged.

---

## 3. Effects and tags (shared schema)

The `effects[]` object schema is identical to the AI jutsu schema. Use the **verified effect-object schema in `21_GUIDE_ai_enemy.md` section 7.4** (keys: `type`, `power`, `powerPerLevel`, `rounds`, `calculation`, `direction`, `target`, `statTypes`, `generalTypes`, optional `elements` on damage/pierce, cosmetic keys optional). The complete lowercase `type` enum and the per-type direction and calculation rules are in that same section.

The **tag vocabulary in guide 21 section 4** also applies, with one difference: the **AI restrictions do not apply to player jutsu.** Players may use `lifesteal`, `vamp`, and self `move` (movement) jutsu, which AI enemies may not. Everything else (the stacking set, poison and increased-cost global cooldowns, stun being minus 40 AP, the distinction between Vamp / Absorb / Lifesteal) is the same.

---

## 4. Player jutsu design rules

- **40 AP is setup or utility with no damage; 60 AP is where damage lives** (doctrine 4).
- **Damage tiers (player scope): Light 38, Normal 40, High 45, Nuke 50.** Do not confuse these with the AI enemy attack-weight curve (doctrine 2).
- **Three tags are an identity, not a target.** Prefer two. Damage counts as a tag.
- **Movement targets ground or self,** not direct enemy debuffs.
- Timing follows doctrine 3: damage resolves immediately, buffs and debuffs queue to the start of the next round, cleanse is instant.

---

## 5. Keystone jutsu

Keystones follow the keystone philosophy in `30_DOCTRINE_balance.md` section 5: a keystone enables an **alternate playstyle, not a raw power upgrade.** The B-rank shape is a base kit plus a cornerstone plus two alternate keystone jutsu, and any weakness-swap must introduce a new weakness.

---

## 6. Mass-edit, sweep, and re-equip patterns

The builder's `convert` slot (entity `jutsu`) is the bulk-edit path. As of builder v4.6 it **fetch-merges**: on the first convert of a run it loads the full live jutsu catalog once (`jutsu.getAll`, two passes so **hidden AI jutsu are included**, mapped by id), then for each entry it merges your `data` over the live record, strips the read-only `bloodline` join, preserves the original `createdAt`, and sends `jutsu.update`. It throttles about 2 seconds apart with backoff and is idempotent.

Because it merges over the live record, **a convert entry only needs the fields you are changing.** A description fix is just `{entity:"jutsu", slot:"convert", targetId:"<id>", data:{description:"..."}}`; the builder pulls the rest of the record itself. Full-record `data` still works. The trimmed catalog (`40_INDEX_jutsu.json`) is for finding the target ids, not as convert input. Confirm each save read `json.success`.

**Re-equip after editing a jutsu that is on an AI (stale-equip).** If you modify a jutsu after it has been equipped to an AI, the AI will not use it in combat until it is re-equipped; the equip link is captured at equip time and goes stale on edit. The fix lives in `21_GUIDE_ai_enemy.md`: unequip (`profile.updateAi` with `jutsus: []`), save, then re-equip (`jutsus: [ids]`), save. Any jutsu edit that touches enemy-kit jutsu should be followed by a re-equip pass for the affected AIs.

Two known candidate sweeps over the live catalog (run with the bloodline-ownership caution from doctrine 7, since bloodline jutsu may be user-owned):
- **Placeholder descriptions:** about 267 jutsu carry placeholder description text. A sweep replaces them with real descriptions, in batches, candidate status until accepted, each entry carrying only the new `description`.
- **Placeholder pool costs:** about 24 player-facing jutsu still carry the `0.05` placeholder pool cost (the AI default leaked onto player content). A sweep sets real `chakraCost` / `staminaCost`. Cost values are a balance call.

---

## 7. Catalog and dumper

- **`40_INDEX_jutsu.json`** is the trimmed catalog of all 780 live jutsu (name, id, element, type, AP, damage, key effects, rank) for lookup, dedup, and pattern reference. The full-fidelity dump lives on GitHub.
- **`TNR_jutsu_dumper.user.js`** pages `jutsu.getAll` (self-builds `{cursor, limit}`, follows `nextCursor`, throttles, downloads the full catalog). Re-run it to refresh the catalog after large changes.

---

## 8. QA checklist (before any jutsu push)

- [ ] `create` payloads preferably carry the COMPLETE field set (section 2), including the three `*ReducePerLvl` numbers and `bloodlineId`/`villageId` as `""` (v4.12 merges defaults under partial creates, but placeholders are not content); `convert` payloads carry only the change (2.3).
- [ ] `name` is unique against the catalog / `getAllNames`; a themed set that collides is prefixed (2.2).
- [ ] `description` and `battleDescription` are both non-empty.
- [ ] `actionCostPerc` is 40 or 60; damage only on 60 (doctrine 1, 4).
- [ ] At most 3 tags (damage counts), 2 preferred.
- [ ] Damage numbers use the player tier scope (38 / 40 / 45 / 50), not the AI curve.
- [ ] Effects use the verified schema (guide 21 section 7.4); every field enum is source-confirmed in `45_DATA_field_schemas.json` (rank ladder D/C/B/A/S/H, 14 weapon values, 5 stat schools, 8 methods, 7 targets).
- [ ] Player pool costs are real, not the `0.05` AI placeholder.
- [ ] Bloodline-linked jutsu are not edited without confirming ownership (doctrine 7).
- [ ] Any edit to an equipped enemy-kit jutsu is followed by a re-equip pass (section 6, guide 21).
- [ ] Push read `json.success` / `json.message`, not just HTTP 200; then confirm the live record is not a blank shell.

## Addendum: harvest Stage 1 + batch 6 (2026-08-01)

- **Level-cap doctrine (H17):** `JUTSU_TRAIN_LEVEL_CAP = 25`. House rule: `powerPerLevel: 0` with the intended MAXIMUM values written directly on the record - what you write is what a maxed jutsu does. No growth curves.
- **Cosmetics requirement (H05, lint L30):** every jutsu must carry at least one effect with BOTH `appearSfx` and `appearAnimation` non-empty, or the cast renders wrong client-side. The complete-payload templates satisfy this; freehand effect arrays are where it gets dropped.
- **Static heal x10 (46b R-law):** `calculation: "static"` heal multiplies power x10 at runtime (power 250 heals 2500); static damage and drain have NO x10. To hit a flat heal target, write power = target/10.
