# Skyglass Project — director reward and hidden-release decisions

**State:** DIRECTOR-APPROVED ITEM TYPE AND EFFECT VALUES / ENGINE + REMAINING BASELINE STILL TO FREEZE.  
**Latest decision date:** 2026-10-10 (director's revised Katana and Crystal specification).  
**Design baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verify again before any implementation).  
**Historical rulings:** `RUL-2026-10-10-007` supersedes earlier Katana/Crystal effect values in `RUL-2026-10-10-002`.  
**Roadmap:** `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md`.

This file owns operative, director-approved Ghost Ship reward **design intent**. It is not a live record, tested game contract, execution manifest, or authorization to change production. Unresolved technical fields and choices stay explicitly open.

## Skyglass Katana — current approved specification

- **Name:** Skyglass Katana.
- **Rarity:** LEGENDARY (unchanged).
- **Type:** `itemType:"WEAPON"`, `weaponType:"SWORD"` (confirmed enum identifiers in the generated TNR item contract).
- **Cannot be imbued:** `canBeImbued:false`; do **not** set `maxImbueNumber:0` to represent this, because the item schema enforces minimum 1 on that numeric field. The `canBeImbued` flag is the eligibility gate. No Skyglass Crystal or other imbuement should function on this weapon.
- **Precisely THREE combat effects:**
  1. **50 EP Pierce**, as one `pierce` tag with `power:50`, normal offensive target/weapon calculation; this **replaces** generic Damage 30 EP and is not a fourth independent Damage effect.
  2. **Buff Prevent Immunity (self, 2 rounds)**, one `immunity` tag with `blocks:"buffprevent"`, `target:"SELF"`, `rounds:2`. Prevents new Buff Prevent applications; does not itself clear existing Buff Prevent.
  3. **Consume 40%**, one `consume` tag with `power:40`, `target:"SELF"`, `calculation:"percentage"`, instant tag (`rounds:0`); generated shield duration is not user-specified and engine currently defaults `shieldRounds:3`. Do not add a separate authored flat shield.
- **Source:** Crowned Captain's **independent 3% AI equipment drop**, not a quest-end prize or Reliquary roll. Crowned Captain independently has **20% Fragment of the Skyglass Crown** AI drop. Five fragments craft The Skyglass Crown; no direct Crown drop.
- **Other Legendary weapon values:** cooldown, AP/action cost, chakra/stamina/health costs, range/target/method, slot, durability, equip/trade restrictions and related required fields need a source-verified Legendary Sword baseline and director sign-off. Do not substitute arbitrary default numbers.

**Superseded Katana stats:** (a) exact Night's Testament clone with shield-potency swap; (b) 30 Damage EP + 40% Consume; (c) 30 Damage EP + 300 HP Shield / 2 rounds + Buff Prevent Immunity / 2 rounds. Only the current **Pierce 50 EP + Buff Prevent Immunity SELF/2 rounds + Consume 40%** set is operative. Earlier values remain in historical rulings for traceability, not for implementation.

**Source-backed feasibility:** Current TNR source at `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` shows `SuperRefineEffects` accepts a Consume tag if the **same effects array** includes Pierce or Damage. `damageUser` writes a `damage` consequence for a cast-round `pierce` effect; the subsequent `forEachOutgoingDamage` for Consume reads this consequence for same-caster outgoing positive damage. This supports the intended Pierce-to-Consume shield conversion **at source level**, but precise schema validation and offline combat playback still remain to be performed. Normal `consume` shield generation is tied to outgoing damage, not a guaranteed fixed 300 HP shield.

## Skyglass Crystal — current approved specification

- **Name:** Skyglass Crystal.
- **Type:** `itemType:"CRYSTAL"` (weapon imbuement), with `crystalTargetTypes:"WEAPON"` (source-confirmed `ItemTypes` target equality).
- **Precisely ONE effect:** **Consume 20%**, one `consume` tag with `power:20`; **supersedes Consume 30%**. Intended to add Consume to the eligible weapon's damaging action; no separately authored Damage/Pierce tag is approved. Engine-default generated shield duration currently 3 rounds, subject to actual feasibility test.
- **Explicit exclusion:** Skyglass Katana is `canBeImbued:false`, so this weapon-only crystal **cannot** be imbued onto Skyglass Katana despite Katana itself having Consume 40%. Weapon-only describes the item category, not universal eligibility.
- **Source:** Skyglass Reliquary **independent 3% direct Crystal chance** on opening; separate **12 Skyglass Filaments craft one Crystal** loop remains. The secret sixth ending awards **one Reliquary guaranteed** (both Gathering and Hunting).
- **Reliquary table otherwise unchanged:** 1 Skyglass Filament + 3 Rare Jewels guaranteed; independent 25% bonus Filament, 30% Skyglass Serum, 15% Ornate Chest, and 3% Skyglass Crystal. No Katana/Crown fragment in chest.
- **Open:** Crystal rarity, Crystal/Filament trading, Crafting-rank/occupation economics and actual item-contract compatibility; do not invent player privileges or rates.

**CRYSTAL ENGINE BLOCKER REMAINS:** `app/src/validators/combat.ts` `SuperRefineEffects` validates **each item's own effects array** and rejects a Consume-only crystal without a `damage` or `pierce` effect on that same **crystal**. The weapon-plus-imbue concatenation during battle is a later phase and does not automatically fix item creation. Source-backed, test-covered targeted validation support for *weapon-targeted Consume-only crystals* may be needed before the 20% crystal can be built. Must not sneak in `damage:0`, `pierce:1` or any unapproved tag to bypass the validation; must not modify the game source without separate explicit authorization. Verify that on a successful weapon imbue the effect actually activates in combat.

## Quest hidden-state evidence conflict

- Director reports both Ghost Ship profession quests are **currently HIDDEN**.
- Historic `harvests/inbox/tnr_results_1790826101573.json` from 2026-10-01 captured both `hidden:false`. That is a historic state, not authoritative current visibility.
- Before any in-place edit, obtain an **operator-run fresh read-only** `quests.get` capture of `6Ri-W5TtUrEMWpyYlnf_F` and `HckXVOf-qk6ESU9t5rxLh`. Preserve verified `hidden:true`, no agent-run publication/unhide.
- No live-game requests or writes occurred while updating these decisions.

## Build acceptance gates still open

1. Source-verified full Legendary **Sword** item baseline (cooldown, AP, costs, method, target, slot, durability etc.) and director acceptance of actual numbers.
2. TNR source-aware validator + offline runtime tests for Katana `pierce:50`, `immunity:buffprevent SELF/2r`, `consume:40%`, and `canBeImbued:false`; test shield conversion off **Pierce** specifically.
3. Source-backed engine solution and tests for `CRYSTAL`, `crystalTargetTypes:WEAPON`, Consume 20% **only**, without additive damage/pierce.
4. Crystal rarity/trading/crafting economy; Sealwright effective Captain parity, new art QA, final quest prose, fresh operator-run hidden readback.
