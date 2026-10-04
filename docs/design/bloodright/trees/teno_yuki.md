# Teno Yuki — Court of Heaven's Snow

**Bloodline:** Teno Yuki (BR-077, rank A, `clh4d6qjs000gtb0hr357gjvv`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Ice classification / forked tree · **Classification:** Ice (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Control by identity: exposure on Ice Palace's circle (Increase Damage Taken 35%) and suppression on Ice Coffin (Decrease Damage Given 30%) · secondary Ice offense: the Frostbound Ascendancy self buff (Increase Damage Given 35%) set up for a controlled +2 Damage on the three Ice attacks (45/40/40) · tertiary Self preservation on Cryostorm Aegis (Decrease Damage Taken 35%, Heal 25).

Teno Yuki is an A-rank Genjutsu bloodline with the Control and Defensive traits. Every non-Damage tag has a single row on a single jutsu, so each route is built on one cast: Frostbound Ascendancy's self buff and the three Ice Damage rows (Burst), Ice Palace's area exposure (Exposure), both Cryostorm Aegis rows (Fortress) and Ice Coffin's suppression with a small Aegis guard rider (Suppression). First Snow of Heaven answers "How do I win offensively: sharpen my own strikes or expose them to everyone's?"; Vigil of Winter answers "How do I win defensively: protect myself or suppress them?". Burst is a percentage setup on the Hidden Art with a +2 Damage payoff (Imperial Freeze 45 → 47, Ice Coffin and Ice Palace 40 → 42) instead of +5 Damage, which made the stunning Imperial Freeze a 50 Nuke and lifted both 40 attacks a full tier. Stun, absorb and recoil are unsupported and untouched. Potency reaches matching supported tags on all Ice jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| First Snow of Heaven | Foundation | How do I win offensively: sharpen my own strikes or expose them to everyone's? |
| Vigil of Winter | Foundation | How do I win defensively: protect myself or suppress them? |
| Reign of Absolute Zero | Advanced Art | burst: self-buff setup on the Hidden Art, controlled +2 Damage payoff on the three Ice attacks |
| Court of Splintered Ice | Advanced Art | exposure: party-wide area amplification on Ice Palace's circle |
| Still Heart of Winter | Advanced Art | fortress: guard and mend against every attacker on one cast |
| Silence of Falling Snow | Advanced Art | suppression: blunt one enemy's blows for the whole party, with a small guard rider |

**Director review recommended:** Roster questions: DQ-B (Court of Splintered Ice +10% Increase Damage Taken on one area row, Ice Palace 35 → 45% on everyone in the radius-1 circle, allies included, ×1.074: the same as Shakunetsu Sakura's two-row +5% at ×1.075, below Blood-Enchanted Eyes' ×1.115; at +3% the route would be +8%, Palace 43%, ×1.059).

- Concern: Court of Splintered Ice is the tree's highest-leverage route in group play. Solo it is level with Reign: Court + Killing Frost gives the caster ×1.40 × 1.45 ≈ ×2.03 on 45/40 EP (×1.037 × 1.074 ≈ ×1.114 over the unmodified kit, the tree's top offensive package, below Blood-Enchanted Eyes' ×1.234), Reign + Hairline Fracture ×1.40 × 1.40 = ×1.96 on 47/42 EP with the +2 Damage also live outside the window. Trimmed to +3% (Palace 43%), Court would be only a +3% top-up on allies over Reign + Hairline Fracture (40%), so the magnitude is kept for the director.
- Concern: Reign of Absolute Zero lifts Imperial Freeze, a 2-round stun, 45 → 47 (Arashima's 45 → 47 precedent, no tier change); no Damage row exceeds 50.
- Concern: Fortress and Suppression split on attackers and party: against one Coffined enemy Suppression is slightly ahead (×0.366 against ×0.374 at 3 BP, ×0.35 against ×0.36 at 4 BP) and shields allies; Fortress guards 45% against every attacker and heals 60 HP more per Aegis cast. Each rests on one row, so both read lighter than the multi-row anchors' defensive packages.
- Concern: Aegis's two rows and Coffin's Decrease Damage Given are element-less, so the defensive half depends on the proposed jutsu-classification resolver, and Cryostorm Aegis on an authored jutsu classification (ENGINE_GAP_REGISTER G1).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ice jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | First Snow of Heaven | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Frostbound Ascendancy, Ice Palace / 2 |
| 02 | Killing Frost | Hidden Art | First Snow of Heaven | +3% Increase Damage Given (self buff) | Frostbound Ascendancy / 1 |
| 03 | Reign of Absolute Zero | Advanced Art | Killing Frost | +2 Damage (damage) | Ice Coffin, Ice Palace, Imperial Freeze / 3 |
| 04 | Hairline Fracture | Hidden Art | First Snow of Heaven | +3% Increase Damage Taken (enemy debuff) | Ice Palace / 1 |
| 05 | Court of Splintered Ice | Advanced Art | Hairline Fracture | +5% Increase Damage Taken (enemy debuff) | Ice Palace / 1 |
| 06 | Vigil of Winter | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Cryostorm Aegis, Ice Coffin / 2 |
| 07 | Permafrost Mantle | Hidden Art | Vigil of Winter | +3% Decrease Damage Taken (self buff) | Cryostorm Aegis / 1 |
| 08 | Still Heart of Winter | Advanced Art | Permafrost Mantle | +5% Decrease Damage Taken (self buff); +3% Heal (self buff) | Cryostorm Aegis / 2 |
| 09 | Cold Saps the Will | Hidden Art | Vigil of Winter | +3% Decrease Damage Given (enemy debuff) | Ice Coffin / 1 |
| 10 | Silence of Falling Snow | Advanced Art | Cold Saps the Will | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff) | Cryostorm Aegis, Ice Coffin / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **First Snow of Heaven** — The first flakes settle without a sound; by morning the court belongs to winter. Frostbound Ascendancy Increase Damage Given 35 → 37% (self); Ice Palace exposure 35 → 37% (enemies and allies inside the circle). Both live 2 rounds after cast.
- **Killing Frost** — The cold gathers in the sovereign's own hands. One night of it is enough; nothing green survives. Setup: Frostbound Ascendancy self buff 37 → 40% with First Snow of Heaven (the caster's Ice, Water, Wind and element-less hits, live the 2 rounds after the 40 AP cast).
- **Reign of Absolute Zero** — At the bottom of the cold nothing moves, nothing resists, nothing is spared. Burst payoff: Imperial Freeze 45 → 47, Ice Coffin and Ice Palace 40 → 42 EP (no tier change); the 40% Frostbound buff multiplies these hits in its window.
- **Hairline Fracture** — Every surface the frost touches is already fractured; it only waits for the blow. Ice Palace exposure 37 → 40% with First Snow of Heaven (one area row, 2 rounds, 60 AP, cooldown 7); the kit's only exposure row.
- **Court of Splintered Ice** — The palace shatters around the condemned; every shard carries the sovereign's will. Exposure: Ice Palace 35 → 45% on the full route (+10% on one area row, ×1.45/1.35 ≈ ×1.074) on everyone in the circle, allies included, for the 2 rounds after the cast; raises the whole party's Ice, Water, Wind and element-less hits on them.
- **Vigil of Winter** — The watch is kept in silence and frost; the gate does not open. Cryostorm Aegis Decrease Damage Taken 35 → 37% (self, 40 AP, 2 rounds); Ice Coffin Decrease Damage Given 30 → 32% (single enemy, 60 AP, 2 rounds).
- **Permafrost Mantle** — Ground that has not thawed in a thousand years does not give way to a blade. Cryostorm Aegis Decrease Damage Taken 37 → 40% with Vigil of Winter (one self row, all four stat types, no element: every non-pierce hit taken).
- **Still Heart of Winter** — Beneath the snow the heart slows, mends, and endures until the thaw that never comes. Fortress: Cryostorm Aegis Decrease Damage Taken 35 → 45% on the full route (+10%) and Heal 25 → 28 (250 → 280 HP per tick), both on one 40 AP cast.
- **Cold Saps the Will** — Numb hands, slow thoughts, a blow that lands without conviction. Ice Coffin Decrease Damage Given 32 → 35% with Vigil of Winter (one single-target row, 2 rounds, 60 AP); the kit's only suppression row.
- **Silence of Falling Snow** — Snow deadens every sound. The enemy's fury arrives as a whisper. Suppression: Ice Coffin Decrease Damage Given 30 → 40% on the full route (+10%), on the target's non-pierce hits against anyone for the 2 rounds after the cast, while Coffin still lands its 40 EP Ice hit; rider: Cryostorm Aegis Decrease Damage Taken 37 → 39% with Vigil of Winter.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | HEAL |
|---|---|---:|---:|---:|---:|---:|---:|
| Reign of Absolute Zero Burst (Burst) | First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Hairline Fracture | +2 | +5% | — | +5% | — | — |
| Court of Splintered Ice Exposure (Exposure) | First Snow of Heaven, Hairline Fracture, Court of Splintered Ice, Vigil of Winter | — | +2% | +2% | +10% | +2% | — |
| Still Heart of Winter Fortress (Fortress) | Vigil of Winter, Permafrost Mantle, Still Heart of Winter, Cold Saps the Will | — | — | +5% | — | +10% | +3% |
| Silence of Falling Snow Suppression (Suppression) | Vigil of Winter, Cold Saps the Will, Silence of Falling Snow, First Snow of Heaven | — | +2% | +10% | +2% | +4% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Reign of Absolute Zero Burst:** Frostbound Ascendancy 35 → 40%, Ice Palace exposure 40% and +2 Damage (Imperial Freeze 47, Ice Coffin and Ice Palace 42 EP). Open with Palace and Frostbound (100 AP); Freeze and Coffin in the two following rounds land at ×1.40 × 1.40 = ×1.96 on the larger base, and the passive multiplies last. Hairline Fracture is the all-offense fourth; Vigil of Winter (Aegis 37%, Coffin 32%) is the safe one.
- **Court of Splintered Ice Exposure:** Ice Palace exposes everyone in its circle at 45% for the two rounds after the cast, so every Ice, Water, Wind or element-less hit from the caster or allies lands ×1.45; with Frostbound at 37% the caster's own hits reach ×1.37 × 1.45 ≈ ×1.99. Vigil of Winter is the fourth for a support caster who also guards (Aegis 37%, Coffin 32%); Killing Frost (Frostbound 40%, ×1.40 × 1.45 = ×2.03) is the all-offense fourth.
- **Still Heart of Winter Fortress:** Cryostorm Aegis becomes a 45% guard against non-pierce hits and heals 280 HP per tick, both live the two rounds after one 40 AP cast. Cold Saps the Will is the pure-defense fourth: Coffin at 35% in the same window takes a Coffined enemy's hits on the caster to ×0.55 × 0.65 ≈ ×0.36. First Snow of Heaven is the counterattack fourth (Frostbound and Palace 37%).
- **Silence of Falling Snow Suppression:** Ice Coffin cuts its target's hits on anyone to ×0.60 for two rounds while dealing its 40 EP hit, and Aegis guards at 39%: against the Coffined enemy the caster takes ×0.61 × 0.60 ≈ ×0.366 (Fortress at 3 BP: ×0.55 × 0.68 ≈ ×0.374), and allies share the cut. First Snow of Heaven is the Control fourth (Palace exposure and Frostbound 37%); Permafrost Mantle (Aegis 42%, ×0.58 × 0.60 ≈ ×0.35 against the Coffined enemy) is the pure-defense fourth.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Cryostorm Aegis | 0 | Decrease Damage Taken | self | 35% | 35% | 37% (+2) | 45% (+10) | 39% (+4) |
| Cryostorm Aegis | 1 | Heal | self | 25 | 25 | 25 | 28 (+3) | 25 |
| Imperial Freeze | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Imperial Freeze | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Ice Coffin | 0 | Decrease Damage Given | enemy | 30% | 30% | 32% (+2) | 35% (+5) | 40% (+10) |
| Ice Coffin | 1 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Frostbound Ascendancy | 0 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 35% | 37% (+2) |
| Frostbound Ascendancy | 1 | absorb (unsupported) | self | 35% | 35% | 35% | 35% | 35% |
| Frostbound Ascendancy | 2 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Ice Palace | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Ice Palace | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 45% (+10) | 35% | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken, +3% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Reign of Absolute Zero: +2 Damage (0 + 0 + 2; off band)
  - Route Court of Splintered Ice: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Still Heart of Winter: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Silence of Falling Snow: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 8 (DMG 3, DDG 1, DDT 1, HEAL 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: First Snow of Heaven, Vigil of Winter, Permafrost Mantle, Still Heart of Winter (raw +19, row-weighted 19)
- Lowest row-weighted node: Killing Frost (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Ice Palace#0, Ice Palace#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Imperial Freeze | 0 | 45 (High) | 47 (High) |
| Ice Coffin | 1 | 40 (Normal) | 42 (Normal) |
| Ice Palace | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Reign of Absolute Zero | +2 Damage, +5% IDG, +2% IDT | Hairline Fracture | +2 Damage, +5% IDG, +5% IDT | 16 |
| Reign of Absolute Zero | +2 Damage, +5% IDG, +2% IDT | Vigil of Winter *(highest diagnostic)* | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT | 17 |
| Court of Splintered Ice | +2% IDG, +10% IDT | Killing Frost | +5% IDG, +10% IDT | 15 |
| Court of Splintered Ice | +2% IDG, +10% IDT | Vigil of Winter *(highest diagnostic)* | +2% IDG, +2% DDG, +10% IDT, +2% DDT | 16 |
| Still Heart of Winter | +2% DDG, +10% DDT, +3% HEAL | First Snow of Heaven *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% DDT, +3% HEAL | 19 |
| Still Heart of Winter | +2% DDG, +10% DDT, +3% HEAL | Cold Saps the Will | +5% DDG, +10% DDT, +3% HEAL | 18 |
| Silence of Falling Snow | +10% DDG, +4% DDT | First Snow of Heaven *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +4% DDT | 18 |
| Silence of Falling Snow | +10% DDG, +4% DDT | Permafrost Mantle | +10% DDG, +7% DDT | 17 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Hairline Fracture | +2 Damage, +5% IDG, +5% IDT |
| 2 | First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Vigil of Winter | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT |
| 3 | First Snow of Heaven, Killing Frost, Hairline Fracture, Court of Splintered Ice | +5% IDG, +10% IDT |
| 4 | First Snow of Heaven, Killing Frost, Hairline Fracture, Vigil of Winter | +5% IDG, +2% DDG, +5% IDT, +2% DDT |
| 5 | First Snow of Heaven, Killing Frost, Vigil of Winter, Permafrost Mantle | +5% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | First Snow of Heaven, Killing Frost, Vigil of Winter, Cold Saps the Will | +5% IDG, +5% DDG, +2% IDT, +2% DDT |
| 7 | First Snow of Heaven, Hairline Fracture, Court of Splintered Ice, Vigil of Winter | +2% IDG, +2% DDG, +10% IDT, +2% DDT |
| 8 | First Snow of Heaven, Hairline Fracture, Vigil of Winter, Permafrost Mantle | +2% IDG, +2% DDG, +5% IDT, +5% DDT |
| 9 | First Snow of Heaven, Hairline Fracture, Vigil of Winter, Cold Saps the Will | +2% IDG, +5% DDG, +5% IDT, +2% DDT |
| 10 | First Snow of Heaven, Vigil of Winter, Permafrost Mantle, Still Heart of Winter | +2% IDG, +2% DDG, +2% IDT, +10% DDT, +3% HEAL |
| 11 | First Snow of Heaven, Vigil of Winter, Permafrost Mantle, Cold Saps the Will | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | First Snow of Heaven, Vigil of Winter, Cold Saps the Will, Silence of Falling Snow | +2% IDG, +10% DDG, +2% IDT, +4% DDT |
| 13 | Vigil of Winter, Permafrost Mantle, Still Heart of Winter, Cold Saps the Will | +5% DDG, +10% DDT, +3% HEAL |
| 14 | Vigil of Winter, Permafrost Mantle, Cold Saps the Will, Silence of Falling Snow | +10% DDG, +7% DDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Kept: graph, names, Foundations, Exposure, Fortress and the defensive Hidden Arts. First pass: Killing Frost +2 Damage → +3% Increase Damage Given; Reign of Absolute Zero +3 → +2 Damage; Court of Splintered Ice drops its +3% Increase Damage Given; Silence of Falling Snow drops its +2% Heal. The old +5 Damage route made Imperial Freeze (a 2-round stun) 45 → 50 and lifted Coffin and Palace 40 → 45; Damage on the Hidden Art also let Exposure buy +2 Damage as its fourth. Roster pass: Silence of Falling Snow gains +2% Decrease Damage Taken (Arashima's Silence After Thunder pattern, RUL-2026-10-04-003); Court's +10% exposure (one row, ×1.074) is kept as roster question DQ-B.
- Route ownership: Burst holds the Frostbound buff and the Damage rows, Exposure Ice Palace's Increase Damage Taken, Fortress both Aegis rows, Suppression Ice Coffin's Decrease Damage Given plus a +2% share of the Aegis guard. Heal stays only on Still Heart of Winter, where it is the guard cast's own second row; a Heal rider on Silence was glue. Maxima over every legal allocation: Damage +2, Increase Damage Given +5%, Increase Damage Taken +10%, Decrease Damage Taken +10%, Decrease Damage Given +10%, Heal +3%.
- Resolver reads (§3): Aegis Decrease Damage Taken and Coffin Decrease Damage Given list all four stat types and no element, so the filter is not binding: every non-pierce hit the caster takes or the Coffined enemy deals. Ice Palace Increase Damage Taken and Frostbound Increase Damage Given list Ice/None/Water/Wind: they match Ice, Water, Wind and element-less hits, never pierce.
- Delivery: all five jutsu have cooldown 7; the attacks cost 60 AP, Aegis and Frostbound 40 AP. Buff and debuff rows and Aegis heal ticks are live the two rounds after the cast (§3b), so Palace's exposure never raises its own hit and Frostbound only raises later-round attacks. Frostbound's buff row is SELF, realized on the caster at cast (actions.ts 980-1004). Ice Palace lands both rows once on each living non-caster in its radius-1 circle.
- Fourth purchases: Burst takes Hairline Fracture (Palace 40%) or Vigil of Winter; Exposure takes Killing Frost (Frostbound 40%) or Vigil of Winter; Fortress takes Cold Saps the Will (Coffin 35%) or First Snow of Heaven; Suppression takes Permafrost Mantle (Aegis 42%) or First Snow of Heaven. The two all-offense builds differ only in Reign's +2 Damage against Court's +5% exposure. Against a Coffined enemy the all-defense builds reach ×0.55 × 0.65 ≈ ×0.36 (Fortress) and ×0.58 × 0.60 ≈ ×0.35 (Suppression); Fortress keeps the higher guard against every other attacker and 60 HP more healing per Aegis cast, while Suppression's 40% also shields allies, so no fourth makes one route automatic.

## Risks and unproven interactions

- Classification: Ice is the single qualifying element; sharing it with other bloodlines (Blue Blade Eyes, Hyouga Yui and others) is expected (RUL-2026-10-03-005). Aegis Decrease Damage Taken and Heal and Coffin Decrease Damage Given are element-less, and Cryostorm Aegis carries no Ice row, so it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Ice coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN) is unverified; Reign's +2 Damage reaches any such Ice Damage row.
- Ally hazard: Ice Palace rows 0 (Damage) and 1 (Increase Damage Taken) are AOE_CIRCLE_SPAWN with friendly fire none (= ALL): Reign raises the hit on allies in the circle to 42, and the exposure nodes expose them at up to 45%. The caster is never a target. Ice Coffin reaches an ally only if aimed at one; Imperial Freeze's Damage row is ENEMIES-only.
- Exposure downstream: one 45% Palace multiplies every matching non-pierce hit on everyone in the circle by ×1.45 from caster and allies for two rounds, so its value grows with party size and enemies caught. Same-tag debuffs from different casters all apply (process.ts 1109-1117): two Palaces compound to ×1.45 × 1.45 ≈ ×2.10.
- Guard and suppression: Aegis and Coffin together cost 100 AP and apply in sequence to the Coffined enemy's hits on the caster; the 4-BP maxima are ×0.55 × 0.65 ≈ ×0.36 (Fortress + Cold Saps the Will) and ×0.58 × 0.60 ≈ ×0.35 (Suppression + Permafrost Mantle), well above the 10% floor; the Water-only 15% Decrease Damage Taken passive applies last.
- Heal: Aegis heals 250 HP per tick on the two rounds after the cast; Still Heart of Winter adds 30 HP per tick. healprevent on the caster blocks it.
- Rank and passive: the Increase Damage Given passive (25% + 0.15 per user level: 28.75% at user level 25, 40% at 100; Water, Wind, Ice, None) multiplies last on every Burst and Exposure hit. Skill-tree and bloodline effects are skipped in ranked modes. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Ice jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

