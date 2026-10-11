# Skyglass Project — Director reward/visibility decisions

**State:** director-approved values, technical/build freeze pending.  
**Date:** 2026-10-10  
**Baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0`  
**Roadmap:** `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md`

This task-specific design decision record owns approved player-facing intent, not engine mechanics or current live-state evidence. Do not infer undecided values.

## Skyglass Katana — approved

- New Legendary WEAPON; **3% independent Crowned Captain AI drop**; not a quest-completion or Reliquary drop.
- **Damage: 30 EP** (raw Damage effect power under `docs/RULINGS.md` RUL-2026-10-03-005). Fable must validate exact item tag encoding.
- **Consume: 40%** on the same damage-bearing weapon action. Verify actual shield conversion in offline tests.
- Other stats — AP, cooldown, chakra/stamina cost, range, etc. — use a **documented Legendary baseline**. No exact numeric defaults were supplied. Capture/identify a suitable comparable Legendary weapon and present resulting values for director acceptance before build freeze.
- **Supersedes** the earlier “exact copy of Night's Testament except remove imbue slot for shield potency +X” specification. The new Katana has no separate shield-potency affix. Night's Testament `osJq3k77YPGoFWgof12FQ` is now only a possible comparison, not the mandated clone.
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

**Still open:** exact Legendary baseline numbers/technical 30 EP mapping; functional 30% Crystal Consume representation; Crystal rarity/trade; Sealwright tuning, full quest graph, art readiness, and fresh hidden-state readback.
