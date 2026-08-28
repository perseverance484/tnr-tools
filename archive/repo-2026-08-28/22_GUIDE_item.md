> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# 22 - GUIDE: Item and Weapon Creation

Owner doc for items, weapons, and loot chests: the design rules, the loot-chest mechanic, the chest chassis to clone, the item contracts, and the catalog. Cross-cutting item doctrine (Legendary default, multiplicative damage, light weapon riders) is in `30_DOCTRINE_balance.md` and summarized here. Shared plumbing is in `10_TECH_pipeline.md`. Effect objects on combat items use the same schema as jutsu (`21_GUIDE_ai_enemy.md` section 7.4). Rarity beyond the default, prices, and drop rates are balance calls reserved by dauntless.

---

## 1. Item tRPC contract

Envelope rules are in `10_TECH_pipeline.md`. Item-specific:

| Op | Method | Shape |
|---|---|---|
| `item.create` | POST | `{json:{type:"<itemType>"}}`. **Not a null body** (this differs from the other creates). Returns a default row of that type, new id in `message`. |
| `item.update` | POST | `{json:{id,data}, meta:{values:{"data.createdAt":["Date"],"data.updatedAt":["Date"]}, v:1}}`. |
| `item.getAll` | GET | same paging pattern as `jutsu.getAll`. |
| `item.getItemWithCraftingRequirements` | GET | full item including effects. |

## 2. Item write gotchas

1. **`item.create` takes `{type}`, not null.** It returns a default row of that type; the follow-up `item.update` fills every field.
2. **`battleDescription` is NOT NULL in the DB.** An empty string is coerced to null and 500s with `Column 'battleDescription' cannot be null`. Always send a non-empty value (for example `"Treasure chest"`), even for items that never see combat.
3. **Include `craftingRequirements: []` and `requiredBloodline: null`** in the update data (the editor sends them and the server tolerates them; the validator's own field is `bloodlineId`). Use `null` for `expireFromStoreAt` and `bloodlineId`.

### 2.1 Complete field schema (source-confirmed)

The full `item.update` write validator (ItemValidator), extracted from the TNR source; machine-readable in `45_DATA_field_schemas.json`. Because `item.create {type}` returns a default row, an update built by editing that row is always complete; a hand-built update must carry every required field below.

**Enums**
- `itemType`: `WEAPON` `CONSUMABLE` `ARMOR` `ACCESSORY` `MATERIAL` `KEYSTONE` `CRYSTAL` `OTHER`
- `rarity`: `COMMON` `RARE` `EPIC` `LEGENDARY`
- `slot`: `HEAD` `CHEST` `LEGS` `FEET` `HAND` `THROWN` `ITEM` `WAIST` `KEYSTONE` `NONE`
- `weaponType`: the same 14-value enum as jutsu `jutsuWeapon` (`NONE` plus 13 weapon types, guide 20 section 2)
- `method` / `target` / `battleUsageType`: the same enums as jutsu (guide 20 section 2)

**Required (no server default):** `name`, `image`, `description`, `battleDescription` (non-empty, gotcha 2), `stackSize` (1-999), `chakraCost` / `healthCost` / `staminaCost` (0-10000), the three `*ReducePerLvl` numbers (0-10000), `actionCostPerc` (1-100; the jutsu floor of 10 does not apply to items), `maxImbueNumber` (1-3), `maxDurability` (1-100), `hidden`, `cooldown` (0-300), `cost` / `repsCost` / `seichiSilverCost` (>= 0), `range` (0-10), `maxEquips` (0-10), `method`, `target`, `itemType`, `weaponType`, `rarity`, `slot`, `expireFromStoreAt` (`YYYY-MM-DD` string or null), `effects`, `crystalTargetTypes` (an ItemTypes value or null), `bloodlineId` (string or null).

**Optional with server defaults:** `destroyOnUse` false, `canStack` false, `inShop` false, `isEventItem` false, `preventBattleUsage` false, `requiredLevel` 1, `canBeImbued` / `canBeCrafted` / `canBeHunted` / `canBeGathered` / `canBeTraded` false, `craftingExperience` 0, `battleUsageType` `BOTH`, `craftingRequirements` `[]` (shape `[{ids: string[], number: 1-100}]`).

## 3. Item and weapon design (doctrine summary)

- **Default to Legendary rarity** for new gear; most active players have outgrown Epic and below. Overridable per request.
- **Damage is multiplicative.** Separate Increased-Damage-Given buckets (stat-scoped versus element-scoped) multiply, so a player stacking several modest sources beats one large source.
- **Weapon riders stay light.** A weapon costs about 40 AP and deals guaranteed damage, so give it at most one modest damage-increase bucket. The multiplicative payoff is meant to come from the player's own stacked sources, not from the weapon stacking buckets itself. The reference anchor is a weapon at roughly damage 30 with a 20% increased-damage-taken rider.
- For combat items and weapons, effects use the verified effect-object schema in `21_GUIDE_ai_enemy.md` section 7.4 (damage is an effect entry; `elements` goes on damage/pierce).

## 4. The loot-chest mechanic

A loot chest is **one item** with a single `noncombatconsumereward` effect (`power: 1`) whose `reward_items` array IS the entire loot table. Each entry is a bundle:
```json
{ "ids": ["<itemId>"], "number": <drop chance %>, "quantity": <amount> }
```
- Each line is one bundle. Multiple lines for the same item create a range: a `100%` line is the floor and additional sub-100% lines add independently-rolled bonus amounts.
- Example, 10 to 50 of an item: `10@100, 20@50, 20@10` (quantity@chance).
- `number` accepts decimals, so ultra-rare lines like `1@0.1` are valid.

Drop chances and quantities are balance decisions.

## 5. Chest chassis (mirror a known-good chest)

When making a new chest, clone these field values and swap the loot table and art:

`itemType: CONSUMABLE`, `slot: ITEM`, `destroyOnUse: true`, `preventBattleUsage: true`, `actionCostPerc: 60`, `stackSize: 999`, `canStack: true`, one effect at `power: 1`, `battleDescription` non-empty (for example `"Treasure chest"`), `inShop: false`, `canBeTraded: false`, `cost: 1`, `seichiSilverCost: 0`, `requiredLevel: 1`. Default rarity for event caches is COMMON unless prestige is wanted (a balance call).

## 6. Catalog and dumper

- **`41_INDEX_item.json`** is the trimmed catalog of the live items for lookup and dedup. Full dump on GitHub.
- **`TNR_item_dumper.user.js`** uses the same engine as the jutsu dumper pointed at `item.getAll` (self-builds `{cursor, limit}`, pages via `nextCursor`, throttles, downloads `item_catalog.json`). Its on-screen list marks battle-usable items so combat consumables are easy to pick.

## 7. QA checklist (before any item push)

- [ ] `item.create` body is `{type}`, not null.
- [ ] `battleDescription` is non-empty.
- [ ] Hand-built updates carry the complete required field set (2.1); enum values from `45_DATA_field_schemas.json`.
- [ ] `craftingRequirements: []` and `requiredBloodline: null` are present; `null` for `expireFromStoreAt` and `bloodlineId`.
- [ ] Weapons carry at most one modest damage bucket (doctrine 6); damage and effects use the verified schema.
- [ ] Rarity defaults to Legendary for gear unless told otherwise; chest caches default to COMMON unless prestige is wanted.
- [ ] Loot-table drop chances, quantities, and rarities confirmed with dauntless (balance).
- [ ] All referenced item ids in a chest's loot table are real, pulled from edit URLs or the catalog.
- [ ] Push read `json.success` / `json.message`, not just HTTP 200.

## Addendum: item rules (live-verified, Tower keystones/scroll)

- `battleDescription` is DB NOT NULL: always non-empty, even on non-combat items.
- **KEYSTONE is a native equip slot** (ItemSlotTypes). Keystone-toggle pattern: bloodline-side jutsu bind to a keystone item via `requiredBloodlineItemId`; swapping the equipped keystone swaps the active side. Live pair: Eclipse Keystone `1VkKByaLQNDjJUEqiNeic`, Aegis Keystone `PPlOpN27RkT0Aw-m9Cfg3`.
- `noncombatconsumereward` spreads the full ObjectiveReward field set, including `reward_bloodlines` (ids-with-number, number = grant chance %): a consumable can grant a specific bloodline.


## Addendum (Jul 10 2026, source extraction)

- **Flipping an item `hidden: true` on edit AUTO-UNEQUIPS it from every player** (`item.update` sets `equipped: NONE` on all userItem rows). Hiding a live item is a server-wide unequip event; plan accordingly.
- **Cost rule (SuperRefineItem):** at least one of `cost` (ryo), `repsCost`, `seichiSilverCost` must be > 0 on every item.
- **`craftingRequirements` write shape CONFIRMED:** `[{ids: string[], number: 1-100}]`; the server expands to one row per id with quantity = number.
- `itemType CONSUMABLE` requires `destroyOnUse: true` (write validator, not just convention).
- Full effect-tag legality and the complete cross-field rule set (noncombatconsumereward / rollbloodline / unlockitemvariant constraints, EMPTY_GROUND rules, wound/vamp pairing): `46_DATA_tag_schemas.json`.

## 9. The item effects union, injectjutsus, and PvE items (2026-07-18, all live-proven)

### 9.1 The item union is narrower than the jutsu union
Confirmed item-legal effect types: damage-class, absorb, increasestat, decreasedamagetaken, increasedamagegiven, heal (with `poolsAffected`), shield, reflect, injectjutsus, noncombatconsumereward. Confirmed EXCLUDED: `clear`, `copy`. `cleanse` and `debuffprevent` were excluded until the 2026-07 source patch added them; current prod accepts direct-effect items with both (the Seven-Beaded Rosary is the live proof: activated item, actionCostPerc 40, cooldown 10, cleanse + debuffprevent). For any effect type not on the confirmed list, default to the injectjutsus wrapper; test direct-effect only against a throwaway record.

### 9.2 injectjutsus is a PERMANENT join
Referencing a jutsu from an item's `injectjutsus` creates a server-side join that makes the jutsu UNEDITABLE FOR LIFE: the guard blocks all updates (not just hiding), and detaching the effect does not clear the join. Additionally the engine requires injected jutsu to be `hidden: false`. Therefore: **the wrapper jutsu must be born final** - correct effects (live-exemplar shapes), correct name, unhidden - BEFORE the item ever points at it. A trapped shell is permanent residue; the only escape is minting a fresh jutsu under a NEW name (the old name is trapped too) and repointing the item's `jutsuIds`.

### 9.3 PvE enforcement and recipes
`battleUsageType: "PVE"` natively enforces PvE-only usage. `craftingRequirements` shape (source-confirmed): `[{ids: [itemId], number: qty}]`. Drop doctrine: every drop is quantity 1 per encounter unless explicitly specified; recipe quantities alone express grind length; a drop quantity and a recipe requirement must never share a common factor. Shared binder materials across multiple recipes (the Silver Thread pattern) keep common drops liquid and every route relevant.

---

## The conversion model (added 2026-07-27, proven on the Ashen Concord)

**One common base per slot drops; everything above it is converted.** The drop table carries exactly one common item per equipment slot. A base plus that slot's themed material converts it to the rare piece, that piece plus more converts to epic, and again to legendary. The consequence worth having: the number of distinct items that must appear in drop tables stays at one per slot no matter how many lines, tiers, or factions the campaign has, and a player always knows what a drop is for.

**Map each slot to one material.** A stable slot-to-material mapping (head takes one faction's material, chest another, and so on) makes a recipe legible without a spreadsheet and gives every faction a reason to be farmed.

**Line identity belongs in the recipe, not the drop.** Three lines sharing one base means the player chooses their build at the forge. Never ship three near-identical commons that differ only by colour: that is a false choice at the drop table and a wider catalog for no gain.

**Name any material sourced outside the campaign.** If a recipe eats an existing game material, say so in the launch post with the total. One hundred units of an externally gathered ore is the single largest trade pressure a campaign can create, and it should be a deliberate design statement rather than a discovery.

## Addendum: harvest Stage 1 facts (2026-08-01)

- **H12.** The item effects union demands the FULL editor key set including cosmetics (`appearSfx`, `disappearAnimation`, `staticAssetPath`), unlike the lean `jutsu.update` path. This qualifies law 3's "lean proven shapes": lean applies per-ENTITY - jutsu lean, item full. (Stage 2 throwaway push will re-confirm the exact minimal item set.)
- **H13.** Exemplar corrections for 40x: `stunprevent` on items uses `calculation: "percentage"` (not static); both `timedilation` and `stunprevent` on items use `target: "INHERIT"` with `friendlyFire: "FRIENDLY"`.
- **Variant subsystem (2026-08-01, 45 v3):** `item.upsertItemVariant { itemId, variant }` is the proper channel for named cosmetic variants (max 7 per item, cost types MONEY/REPUTATION/SEICHI_SILVER/VILLAGE_PRESTIGE/VARIANT_TOKEN). Hemathorn / Weeping Testament-class work rides a manifest now, not the editor.
