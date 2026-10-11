# Skyglass Project — director reward and hidden-release decisions

**State:** DIRECTOR-APPROVED ITEM TYPES, BASELINE, EFFECT VALUES, 2/2 CONSUME TIMING AND CRYSTAL ECONOMY / FINAL-RECORD REVALIDATION PENDING.
**Latest decision date:** 2026-10-11 (RUL-2026-10-11-006: Consume 2/2 on both items; Crystal Legendary, tradable, not craftable. Rates remain Katana15 / Crystal10 under RUL005; Katana baseline remains RUL004).
**Design baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verify again before any implementation).  
**Historical rulings:** `RUL-2026-10-11-005` supersedes 40%/20% and instant-only Consume. `RUL-2026-10-11-006` settles both timers and Crystal economy, removing the 12-Filament recipe. Other accepted effect, baseline and reward fields remain operative.
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
  3. **Consume 15%**, one `consume` tag with `power:15`, `target:"SELF"`, `calculation:"percentage"`, **`rounds:2`, `shieldRounds:2`**. Grants an active Consume buff: qualifying damage while it is active generates shields, rather than conversion being limited to the granting action. Each generated shield has its own lifetime. Do not carry forward instant `rounds:0` or add a separate authored flat shield.
- **Source:** Crowned Captain's **independent 3% AI equipment drop**, not a quest-end prize or Reliquary roll. Crowned Captain independently has **20% Fragment of the Skyglass Crown** AI drop. Five fragments craft The Skyglass Crown; no direct Crown drop.
- **Pierce element:** **Crystal** (RUL-2026-10-11-004).
- **Other Legendary weapon values (RUL-2026-10-11-004, Night's Testament baseline):**
  - action: AP 40, cooldown 6, range 4, OTHER_USER / SINGLE;
  - costs: chakra 40, stamina 40, health 0, no per-level reducers;
  - equipment: slot HAND, maxEquips 1, durability 100, required level 1, no stat or mastery requirements, battle usage BOTH;
  - economy: cost 1 ryo, not in shop, **tradable**, **drop-only (not craftable)**, stack 1, xpToLevel 1000;
  - created hidden.
  The frozen r4 field-level record `state/ghost_ship_skyglass_katana_record.json`, derived from push/85, remains historical test evidence with Consume40/rounds0. It is not the current Consume specification. Apply `state/ghost_ship_skyglass_final_item_contract.json` when preparing the next version; Fable owns the derived-record and harness update. Description, battle description, image and effect animation/SFX remain presentation/art items pending acceptance.

**Superseded Katana stats:** earlier shield-potency, generic Damage and fixed-Shield variants remain superseded. The r4 Pierce50 + immunity2r + Consume40/rounds0 record is now historical too. Only **Pierce 50 EP + Buff Prevent Immunity SELF/2 rounds + active Consume 15%** is operative for new construction. Earlier values remain in historical rulings and frozen fixtures for traceability.

**Source and validation boundary:** The r4 Stage 2 item evidence at engine `cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` covers the former 40%/20% contracts. It does not validate the revised items. Reviewed upstream source `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` implements active Consume. Weapon effects activate through weapon actions; this is not a permanent buff granted merely by equipping a weapon. Completed3/3 evidence is linked below; the current brief is `state/prompt_ghost_ship_skyglass_final_item_revalidation.md` for the approved2/2 values and selected Crystal economy.

**Timing accepted (RUL006):** both items use active `rounds:2` and generated `shieldRounds:2`. The earlier 3/3 carriers and their passing evidence remain historical; Fable must produce and test the final 2/2 records. Assert exact engine activation/expiry timelines rather than interpreting “two rounds” as a manually implemented timer.

## Skyglass Crystal — current approved specification

- **Name:** Skyglass Crystal.
- **Economy (RUL006):** `rarity:"LEGENDARY"`, `canBeTraded:true`, `canBeCrafted:false`. Drop-only through the existing Reliquary roll; no 12-Filament recipe. Trading does not waive native imbuement occupation/rank requirements.
- **Type:** `itemType:"CRYSTAL"` (weapon imbuement), with `crystalTargetTypes:"WEAPON"` (source-confirmed `ItemTypes` target equality).
- **Precisely ONE effect:** **Consume 10%**, one `consume` tag with `power:10`, `target:"SELF"`, `calculation:"percentage"`, **`rounds:2`, `shieldRounds:2`**; supersedes 20% and older 30%. The imbued weapon action grants active Consume for qualifying damage while the buff lasts. No separately authored Damage/Pierce tag is approved. Final 2/2 runtime validation remains required.
- **Explicit exclusion:** Skyglass Katana is `canBeImbued:false`, so this weapon-only crystal **cannot** be imbued onto Skyglass Katana despite Katana itself having Consume 15%. Weapon-only describes the item category, not universal eligibility.
- **Source:** Skyglass Reliquary **independent 3% direct Crystal chance** on opening. The former **12 Skyglass Filaments craft one Crystal** route is superseded by RUL006's not-craftable decision. The secret sixth ending awards **one Reliquary guaranteed** (both Gathering and Hunting).
- **Reliquary table otherwise unchanged:** 1 Skyglass Filament + 3 Rare Jewels guaranteed; independent 25% bonus Filament, 30% Skyglass Serum, 15% Ornate Chest, and 3% Skyglass Crystal. No Katana/Crown fragment in chest.
- **Open:** final complete-record compatibility, presentation and Filament trading/use. Filament rewards remain approved, but no replacement use is invented after removal of their Crystal recipe. Native Legendary imbuement access must be verified, not bypassed.
- **Consume overlap:** explicitly deferred by the director; not a blocking design decision for this pass. Preserve observed native behavior and existing evidence. No stacking correction, deduplication change or new compatibility restriction is requested.

**Old Crystal blocker is historical:** at the newly reviewed source, `SuperRefineEffects` requires same-array Damage/Pierce for Consume only when `rounds === 0`. Positive-duration Consume-only Crystal is source-admissible; the previous validator-exemption proposal is not automatically needed. Exact full-item validation and imbued-weapon runtime tests pass for the explicit3/3 carrier; final2/2/economy records still require validation. Do not add fake Damage/Pierce or modify upstream engine code. Preserve overlap evidence without imposing a new policy gate.

## Quest hidden-state evidence conflict

- Director reports both Ghost Ship profession quests are **currently HIDDEN**.
- Historic `harvests/inbox/tnr_results_1790826101573.json` from 2026-10-01 captured both `hidden:false`. That is a historic state, not authoritative current visibility.
- Before any in-place edit, obtain an **operator-run fresh read-only** `quests.get` capture of `6Ri-W5TtUrEMWpyYlnf_F` and `HckXVOf-qk6ESU9t5rxLh`. Preserve verified `hidden:true`, no agent-run publication/unhide.
- No live-game requests or writes occurred while updating these decisions.

**Updated candidate evidence:** `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_OFFLINE_RESULTS.md` and `harness/ghost_ship_consume/results/` validate Katana15 / Crystal10 at engine `585534d7eb21d6f0dd678d5c3eb92662f611d39b`, using explicit **3/3 test timing only**. Full carriers are in `state/ghost_ship_skyglass_active_consume_carriers.json`. Positive-duration Crystal validates without a companion effect; active runtime/guard probes pass. These are not final 2/2/economy results. See `state/prompt_ghost_ship_skyglass_final_item_revalidation.md`; presentation and independent frozen-SHA acceptance remain open. Both historical harnesses and their records remain unchanged in this design pass.

## Build acceptance gates

Settled or historical:

- Legendary Sword baseline and economy: accepted by RUL-2026-10-11-004 (Night's Testament, push/85).
- R4 Stage 2 offline results remain evidence for their old source pin and former item values. Preserve the frozen record, generator and harness for reproducibility; their PASS does not close the new Consume gates.
- Current rates and active-buff direction: Katana15 / Crystal10 accepted by RUL-2026-10-11-005.
- Both Consume timers 2/2 and Crystal Legendary/tradable/not craftable: accepted by RUL-2026-10-11-006. Consume overlap is deferred, not a current approval gate.

Still open:

1. Fable validates final 2/2 records and the approved Crystal economy under `state/prompt_ghost_ship_skyglass_final_item_revalidation.md`, preserving the 3/3 evidence. Independent review remains open.
2. Sealwright effective Captain parity and final AI decisions; new art QA, final quest prose, Filament disposition and fresh operator-run hidden readback.
3. Katana presentation: description, battle description, image, effect animation/SFX.
