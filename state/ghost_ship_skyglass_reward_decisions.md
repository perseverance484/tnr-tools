# Skyglass Project — director reward and hidden-release decisions

**State:** DIRECTOR-APPROVED ITEM TYPES, BASELINE AND EFFECT VALUES / ACTIVE CONSUME TIMING + REVALIDATION PENDING.
**Latest decision date:** 2026-10-11 (active Consume: Katana 15%, Crystal 10%, RUL-2026-10-11-005; accepted Katana baseline remains RUL-2026-10-11-004).
**Design baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verify again before any implementation).  
**Historical rulings:** `RUL-2026-10-11-005` supersedes the 40%/20% Consume rates and instant-only interpretation in earlier specifications. All other accepted effect, baseline and reward fields remain operative.
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
  3. **Consume 15%**, one `consume` tag with `power:15`, `target:"SELF"`, `calculation:"percentage"`. Grants an active Consume buff: qualifying damage while it is active generates shields, rather than conversion being limited to the granting action. Buff duration and generated-shield duration remain separate open fields; do not carry forward the old instant `rounds:0`. Do not add a separate authored flat shield.
- **Source:** Crowned Captain's **independent 3% AI equipment drop**, not a quest-end prize or Reliquary roll. Crowned Captain independently has **20% Fragment of the Skyglass Crown** AI drop. Five fragments craft The Skyglass Crown; no direct Crown drop.
- **Pierce element:** **Crystal** (RUL-2026-10-11-004).
- **Other Legendary weapon values (RUL-2026-10-11-004, Night's Testament baseline):**
  - action: AP 40, cooldown 6, range 4, OTHER_USER / SINGLE;
  - costs: chakra 40, stamina 40, health 0, no per-level reducers;
  - equipment: slot HAND, maxEquips 1, durability 100, required level 1, no stat or mastery requirements, battle usage BOTH;
  - economy: cost 1 ryo, not in shop, **tradable**, **drop-only (not craftable)**, stack 1, xpToLevel 1000;
  - created hidden.
  The frozen r4 field-level record `state/ghost_ship_skyglass_katana_record.json`, derived from push/85, remains historical test evidence with Consume40/rounds0. It is not the current Consume specification. Apply `state/ghost_ship_skyglass_consume_revision.json` when preparing the next version; Fable owns the derived-record and harness update. Description, battle description, image and effect animation/SFX remain presentation/art items pending acceptance.

**Superseded Katana stats:** earlier shield-potency, generic Damage and fixed-Shield variants remain superseded. The r4 Pierce50 + immunity2r + Consume40/rounds0 record is now historical too. Only **Pierce 50 EP + Buff Prevent Immunity SELF/2 rounds + active Consume 15%** is operative for new construction. Earlier values remain in historical rulings and frozen fixtures for traceability.

**Source and validation boundary:** The r4 Stage 2 item evidence at engine `cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` covers the former 40%/20% contracts. It does not validate the revised items. Reviewed upstream source `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` implements active Consume. Weapon effects activate through weapon actions; this is not a permanent buff granted merely by equipping a weapon. Runtime revalidation is assigned in `state/prompt_ghost_ship_skyglass_consume_revalidation.md`.

**Timing remains open:** that source defaults active `rounds` to 3 and generated `shieldRounds` separately to 3. The director approved the active-buff behavior and rates, not these durations. Defaults may be labelled offline test carriers, not silently frozen balance. Explicitly select both lifetimes before a final item record or manifest.

## Skyglass Crystal — current approved specification

- **Name:** Skyglass Crystal.
- **Type:** `itemType:"CRYSTAL"` (weapon imbuement), with `crystalTargetTypes:"WEAPON"` (source-confirmed `ItemTypes` target equality).
- **Precisely ONE effect:** **Consume 10%**, one `consume` tag with `power:10`, `target:"SELF"`, `calculation:"percentage"`; supersedes 20% and older 30%. The imbued weapon action grants active Consume for qualifying damage while the buff lasts. No separately authored Damage/Pierce tag is approved. Buff duration and generated-shield lifetime require separate acceptance and testing.
- **Explicit exclusion:** Skyglass Katana is `canBeImbued:false`, so this weapon-only crystal **cannot** be imbued onto Skyglass Katana despite Katana itself having Consume 15%. Weapon-only describes the item category, not universal eligibility.
- **Source:** Skyglass Reliquary **independent 3% direct Crystal chance** on opening; separate **12 Skyglass Filaments craft one Crystal** loop remains. The secret sixth ending awards **one Reliquary guaranteed** (both Gathering and Hunting).
- **Reliquary table otherwise unchanged:** 1 Skyglass Filament + 3 Rare Jewels guaranteed; independent 25% bonus Filament, 30% Skyglass Serum, 15% Ornate Chest, and 3% Skyglass Crystal. No Katana/Crown fragment in chest.
- **Open:** Crystal rarity, Crystal/Filament trading, Crafting-rank/occupation economics and actual item-contract compatibility; do not invent player privileges or rates.

**Old Crystal blocker is historical:** at the newly reviewed source, `SuperRefineEffects` requires same-array Damage/Pierce for Consume only when `rounds === 0`. Positive-duration Consume-only Crystal is source-admissible; the previous validator-exemption proposal is not automatically needed. Exact full-item validation and actual imbued-weapon runtime tests for Consume10 remain pending. Do not add fake Damage/Pierce or modify upstream engine code to bypass validation. Recheck activation, repeated casts and overlap with existing Consume under the changed engine.

## Quest hidden-state evidence conflict

- Director reports both Ghost Ship profession quests are **currently HIDDEN**.
- Historic `harvests/inbox/tnr_results_1790826101573.json` from 2026-10-01 captured both `hidden:false`. That is a historic state, not authoritative current visibility.
- Before any in-place edit, obtain an **operator-run fresh read-only** `quests.get` capture of `6Ri-W5TtUrEMWpyYlnf_F` and `HckXVOf-qk6ESU9t5rxLh`. Preserve verified `hidden:true`, no agent-run publication/unhide.
- No live-game requests or writes occurred while updating these decisions.

## Build acceptance gates

Settled or historical:

- Legendary Sword baseline and economy: accepted by RUL-2026-10-11-004 (Night's Testament, push/85).
- R4 Stage 2 offline results remain evidence for their old source pin and former item values. Preserve the frozen record, generator and harness for reproducibility; their PASS does not close the new Consume gates.
- Current rates and active-buff direction: Katana15 / Crystal10 accepted by RUL-2026-10-11-005.

Still open:

1. Separate Consume buff and generated-shield durations; exact 15%/10% full-item validation and runtime revalidation at a pinned updated engine, including stacking, expiry, attribution and existing eligibility guards. Fable owns the next derived records and tests under `state/prompt_ghost_ship_skyglass_consume_revalidation.md`.
2. Crystal rarity/trading/crafting economy; Sealwright effective Captain parity and final AI decisions; new art QA, final quest prose and fresh operator-run hidden readback.
3. Katana presentation: description, battle description, image, effect animation/SFX.
