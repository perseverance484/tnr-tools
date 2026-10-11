# Skyglass Project — Director reward/visibility decisions

**State:** director-approved values, technical/build freeze pending.  
**Date:** 2026-10-10  
**Baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0`  
**Roadmap:** `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md`

This task-specific design decision record owns approved player-facing intent, not engine mechanics or current live-state evidence. Do not infer undecided values.

## Skyglass Katana — approved

- New Legendary WEAPON; **3% independent Crowned Captain AI drop**; not a quest-completion or Reliquary drop.
- **Damage: 30 EP** (raw Damage effect power under `docs/RULINGS.md` RUL-2026-10-03-005).
- **Shield: 300 HP for 2 rounds** on the wielder when the Katana is used. Source-backed candidate tag: `shield` with `health:300`, `rounds:2`, `target:SELF`, and `power:100` (the shield tag's creation chance, for a guaranteed shield). The `power` parameter is a chance, **not** another shield-HP magnitude.
- **Buff Prevent immunity: 2 rounds** on the wielder. Exact source-backed candidate tag: `immunity` with `blocks:buffprevent`, `rounds:2`, `target:SELF`. This protects against **new applications** of the Buff Prevent effect; it does not itself apply Buff Prevent, grant generic debuff immunity, or cleanse an already-active Buff Prevent.
- **Consume: REMOVED from the Katana**; previous Katana 40% Consume is superseded. Skyglass Crystal's separate weapon-only 30% Consume is unchanged.
- Other stats — AP, cooldown, chakra/stamina cost, range, etc. — use a **documented Legendary baseline**. No exact numeric defaults were supplied. Capture/identify a suitable comparable Legendary weapon and present resulting values for director acceptance before build freeze.
- **Three-tag identity:** Damage + Shield + Immunity (three effects, matching TNR's three-tag maximum). The shield and immunity are temporary self-effects granted by using the weapon; they are not permanent passive stat increases. The original Night's Testament exact-copy / imbue-slot → shield-potency +X concept and the later Consume 40% Katana are both **SUPERSEDED**. Night's Testament `osJq3k77YPGoFWgof12FQ` is optional comparison only, not a mandated clone.
- Existing Crowned Captain fragment rule remains **20% AI drop**, independently rolled. Five fragments craft the Skyglass Crown, never a direct boss drop.

## Skyglass Crystal — approved

- New equipment imbuement item `itemType:CRYSTAL`; weapon-only target (`crystalTargetTypes:WEAPON` candidate field; verify against the live item contract).
- **Consume: 30%**, not +X. Three-round shield duration follows the current Consume design, subject to source-backed validation.
- **Skyglass Reliquary:** independent 3% direct Crystal chance per opening; one Reliquary awarded for completing the mutually exclusive secret route.
- The approved hybrid reward structure also includes guaranteed 1 Skyglass Filament + 3 Rare Jewels; independent 25% extra Filament, 30% Skyglass Serum, 15% Ornate Chest. **12 Filaments craft 1 Crystal**.
- Crystal rarity, trading, and exact operational crafting eligibility remain to be locked.

**ENGINE BLOCKER:** The current `SuperRefineEffects` demands `consume` coexist with `damage` or `pierce` on the SAME item's effect array. A standalone Consume-only crystal fails validation, and a crystal imbuement must actually affect weapon actions, not merely validate. Require a proven source-backed solution and, if necessary, separate reviewed upstream engine work. No silent bonus-damage effect, substitute tag, or weakened Consume is authorized.

## Hidden quest state

- Director reports both Ghost Ship profession quests **currently HIDDEN**.
- Historical capture `harvests/inbox/tnr_results_1790826101573.json` showed `hidden:false` on 2026-10-01. It is outdated on visibility; user report is not a fresh read-back.
- Before changing either existing quest ID (`6Ri-W5TtUrEMWpyYlnf_F`, `HckXVOf-qk6ESU9t5rxLh`), obtain a new operator-run read-only `quests.get` capture.
- If confirmed hidden, preserve `hidden:true` throughout the entire implementation and read-back phase. Never unhide or publish without separate operator authorization. No live-game requests or writes were performed while recording these decisions.

**Source-backed implementation checks:** Pinned source `studie-tech/TheNinjaRPG@4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6` confirms `ShieldTag` (`health`, `rounds`, proc `power`) and `ImmunityTag` (`blocks:buffprevent`, `rounds`) and weapon action routing honors self-targeted tags. No live-game tests were made; Fable must still run offline schema/behavior tests proving all three tags land correctly in sequence, and verify shield application, Immunity behavior and stacking/cooldown interactions.

**Still open:** exact Legendary weapon baseline values and final technical 30 EP tag encoding; offline runtime tests of 300 HP shield/2 rounds and 2-round Buff Prevent immunity; functional 30% Crystal Consume representation; Crystal rarity/trade; Sealwright tuning, full quest graph, art readiness, and fresh hidden-state readback.
