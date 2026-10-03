# Teno Yuki — Court of Heaven's Snow

**Bloodline:** Teno Yuki (BR-077, rank A, `clh4d6qjs000gtb0hr357gjvv`) · **Revision:** Draft 1 / Ice classification / forked tree · **Classification:** Ice (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Control (Increase Damage Taken 35% on Ice Palace's circle; Decrease Damage Given 30% on Ice Coffin) · secondary Burst offense (Damage on three Ice rows at 40/40/45; Increase Damage Given 35% on Frostbound Ascendancy) · tertiary Self preservation (Decrease Damage Taken 35% and Heal 25 on Cryostorm Aegis).

Teno Yuki is an A-rank Genjutsu bloodline with the Control and Defensive traits, and its supported rows split the same way: two enemy debuffs on the 60 AP attack casts (Ice Palace exposure, Ice Coffin suppression), three Ice Damage rows at 45/40/40 (Imperial Freeze, Ice Coffin, Ice Palace) under a 25% + 0.15/level Increase Damage Given passive, a single 35% self damage buff on Frostbound Ascendancy, and the kit's only guard and heal both on the 40 AP Cryostorm Aegis. Control is declared primary because exposure and suppression are the rows that make the Genjutsu kit a pressure tool; Damage is the broadest tag (three rows) and anchors the burst route; the Aegis rows are the tertiary sustain route. Stun, absorb and recoil are unsupported and untouched.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Ice-classified Teno Yuki jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | First Snow of Heaven | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Frostbound Ascendancy, Ice Palace / 2 |
| 02 | Killing Frost | Hidden Art | First Snow of Heaven | +2 Damage power (damage) | Ice Coffin, Ice Palace, Imperial Freeze / 3 |
| 03 | Reign of Absolute Zero | Advanced Art | Killing Frost | +3 Damage power (damage) | Ice Coffin, Ice Palace, Imperial Freeze / 3 |
| 04 | Hairline Fracture | Hidden Art | First Snow of Heaven | +3% Increase Damage Taken (enemy debuff) | Ice Palace / 1 |
| 05 | Court of Splintered Ice | Advanced Art | Hairline Fracture | +5% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Frostbound Ascendancy, Ice Palace / 2 |
| 06 | Vigil of Winter | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Cryostorm Aegis, Ice Coffin / 2 |
| 07 | Permafrost Mantle | Hidden Art | Vigil of Winter | +3% Decrease Damage Taken (self buff) | Cryostorm Aegis / 1 |
| 08 | Still Heart of Winter | Advanced Art | Permafrost Mantle | +5% Decrease Damage Taken (self buff); +3 Heal power (self buff) | Cryostorm Aegis / 2 |
| 09 | Cold Saps the Will | Hidden Art | Vigil of Winter | +3% Decrease Damage Given (enemy debuff) | Ice Coffin / 1 |
| 10 | Silence of Falling Snow | Advanced Art | Cold Saps the Will | +5% Decrease Damage Given (enemy debuff); +2 Heal power (self buff) | Cryostorm Aegis, Ice Coffin / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **First Snow of Heaven** — The first flakes settle without a sound; by morning the court belongs to winter. IDG 35→37% on Frostbound Ascendancy (self, at cast); IDT 35→37% on Ice Palace's circle (enemy, 2 rounds; allies inside also exposed).
- **Killing Frost** — One cold night is enough. Nothing green survives it. Damage 45→47 on Imperial Freeze; 40→42 on Ice Coffin and Ice Palace (Ice, Genjutsu-scaled, 60 AP). Palace's row hits allies in the circle.
- **Reign of Absolute Zero** — At the bottom of the cold nothing moves, nothing resists, nothing is spared. Route total +5: Imperial Freeze 45→50, Ice Coffin and Ice Palace 40→45 on the same three Ice Damage rows.
- **Hairline Fracture** — Every surface the frost touches is already fractured; it only waits for the blow. Ice Palace IDT 37→40% with First Snow of Heaven (one AOE row, 2 rounds, 60 AP, cooldown 7); the kit's only exposure row.
- **Court of Splintered Ice** — The palace shatters around the condemned; every shard carries the sovereign's will. Ice Palace IDT 45% on the full route (Ice, Water, Wind and element-less hits); Frostbound Ascendancy IDG 40% with First Snow of Heaven.
- **Vigil of Winter** — The watch is kept in silence and frost; the gate does not open. DDT 35→37% on Cryostorm Aegis (self, 40 AP, 2 rounds); DDG 30→32% on Ice Coffin (single enemy, 60 AP, 2 rounds).
- **Permafrost Mantle** — Ground that has not thawed in a thousand years does not give way to a blade. Cryostorm Aegis DDT 37→40% with Vigil of Winter (one self row, all four stat types, no element: every non-pierce hit taken).
- **Still Heart of Winter** — Beneath the snow the heart slows, mends, and endures until the thaw that never comes. Cryostorm Aegis DDT 45% on the full route; its Heal 25→28 power (250→280 HP per tick on the two following rounds), both on one 40 AP cast.
- **Cold Saps the Will** — Numb hands, slow thoughts, a blow that lands without conviction. Ice Coffin DDG 32→35% with Vigil of Winter (one single-target row, 2 rounds, 60 AP); the kit's only suppression row.
- **Silence of Falling Snow** — Snow deadens every sound. The enemy's fury arrives as a whisper; you are already healing. Ice Coffin DDG 40% on the full route (one single-target row); Cryostorm Aegis Heal 25→27 power (270 HP per tick, two ticks per cast).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | HEAL |
|---|---|---:|---:|---:|---:|---:|---:|
| Reign of Absolute Zero Burst (Burst) | First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Vigil of Winter | +5 | +2% | +2% | +2% | +2% | — |
| Court of Splintered Ice Exposure (Exposure) | First Snow of Heaven, Hairline Fracture, Court of Splintered Ice, Vigil of Winter | — | +5% | +2% | +10% | +2% | — |
| Still Heart of Winter Bulwark (Bulwark) | Vigil of Winter, Permafrost Mantle, Still Heart of Winter, First Snow of Heaven | — | +2% | +2% | +2% | +10% | +3 |
| Silence of Falling Snow Suppression (Suppression) | Vigil of Winter, Cold Saps the Will, Silence of Falling Snow, First Snow of Heaven | — | +2% | +10% | +2% | +2% | +2 |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Reign of Absolute Zero Burst:** The +5 power route on all three Ice Damage rows (Imperial Freeze 45→50, Ice Coffin and Ice Palace 40→45) with Frostbound Ascendancy's self buff at 37% and Ice Palace's exposure at 37%, so the Palace-then-Freeze sequence lands on an exposed, Genjutsu-scaled target. Vigil of Winter is the fourth purchase for a 37% Aegis guard and 32% Coffin suppression; Hairline Fracture (Palace exposure 40%) is the all-offense alternative.
- **Court of Splintered Ice Exposure:** Ice Palace exposes every enemy in its circle at 45% for two rounds while Frostbound Ascendancy's self buff sits at 40% on top of the bloodline passive, multiplying every Ice, Water, Wind or element-less hit the caster and allies land in the window. Vigil of Winter is the fourth purchase for 37% guard and 32% suppression; Killing Frost (+2 power on three rows) is the offensive alternative.
- **Still Heart of Winter Bulwark:** Cryostorm Aegis becomes a 45% guard against every non-pierce hit for two rounds and heals 280 HP on each of the two following rounds, all from one 40 AP cast. First Snow of Heaven is the fourth purchase so the kit keeps 37% exposure and a 37% self damage buff for the counterattack; Cold Saps the Will (Coffin suppression 35%) is the pure-defense alternative.
- **Silence of Falling Snow Suppression:** Ice Coffin cuts the frozen target's output by 40% of base on every matching hit for two rounds and the Aegis heal rises to 270 HP per tick, the Control trait's own build. First Snow of Heaven is the fourth purchase for 37% exposure and 37% self damage buff; Permafrost Mantle (Aegis guard 40%) is the alternative that stacks suppression with guard in the same window.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Bulwark | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Cryostorm Aegis | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 37% (+2) |
| Cryostorm Aegis | 1 | Heal | self | 25 | 25 | 25 | 28 (+3) | 27 (+2) |
| Imperial Freeze | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Imperial Freeze | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Ice Coffin | 0 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |
| Ice Coffin | 1 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Frostbound Ascendancy | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Frostbound Ascendancy | 1 | absorb (unsupported) | self | 35% | 35% | 35% | 35% | 35% |
| Frostbound Ascendancy | 2 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Ice Palace | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Ice Palace | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Decrease Damage Given +10%, Increase Damage Taken +10%, Decrease Damage Taken +10%, Heal +3 (not jointly attainable)
- Supported rows in kit: 8 (DMG 3, DDG 1, DDT 1, HEAL 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Vigil of Winter (raw +13, row-weighted 23)
- Lowest row-weighted node: Hairline Fracture (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Ice Palace#0, Ice Palace#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Hairline Fracture | DMG +5, IDG +2, IDT +5 |
| 2 | First Snow of Heaven, Killing Frost, Reign of Absolute Zero, Vigil of Winter | DMG +5, IDG +2, DDG +2, IDT +2, DDT +2 |
| 3 | First Snow of Heaven, Killing Frost, Hairline Fracture, Court of Splintered Ice | DMG +2, IDG +5, IDT +10 |
| 4 | First Snow of Heaven, Killing Frost, Hairline Fracture, Vigil of Winter | DMG +2, IDG +2, DDG +2, IDT +5, DDT +2 |
| 5 | First Snow of Heaven, Killing Frost, Vigil of Winter, Permafrost Mantle | DMG +2, IDG +2, DDG +2, IDT +2, DDT +5 |
| 6 | First Snow of Heaven, Killing Frost, Vigil of Winter, Cold Saps the Will | DMG +2, IDG +2, DDG +5, IDT +2, DDT +2 |
| 7 | First Snow of Heaven, Hairline Fracture, Court of Splintered Ice, Vigil of Winter | IDG +5, DDG +2, IDT +10, DDT +2 |
| 8 | First Snow of Heaven, Hairline Fracture, Vigil of Winter, Permafrost Mantle | IDG +2, DDG +2, IDT +5, DDT +5 |
| 9 | First Snow of Heaven, Hairline Fracture, Vigil of Winter, Cold Saps the Will | IDG +2, DDG +5, IDT +5, DDT +2 |
| 10 | First Snow of Heaven, Vigil of Winter, Permafrost Mantle, Still Heart of Winter | IDG +2, DDG +2, IDT +2, DDT +10, HEAL +3 |
| 11 | First Snow of Heaven, Vigil of Winter, Permafrost Mantle, Cold Saps the Will | IDG +2, DDG +5, IDT +2, DDT +5 |
| 12 | First Snow of Heaven, Vigil of Winter, Cold Saps the Will, Silence of Falling Snow | IDG +2, DDG +10, IDT +2, DDT +2, HEAL +2 |
| 13 | Vigil of Winter, Permafrost Mantle, Still Heart of Winter, Cold Saps the Will | DDG +5, DDT +10, HEAL +3 |
| 14 | Vigil of Winter, Permafrost Mantle, Cold Saps the Will, Silence of Falling Snow | DDG +10, DDT +5, HEAL +2 |

## Design notes

- Node split: First Snow of Heaven (IDG + IDT) is the attack root, forking into raw power (Killing Frost → Reign of Absolute Zero, three Ice rows) and exposure (Hairline Fracture → Court of Splintered Ice, the Ice Palace row). Vigil of Winter (DDT + DDG) is the defensive root, forking into guard (Permafrost Mantle → Still Heart of Winter, both Aegis rows) and suppression (Cold Saps the Will → Silence of Falling Snow, the Coffin row). 2F/4H/4A; capstones 3 BP deep; any two cost 5-6 BP.
- Calibration by coverage: Damage +2/+3 (max +5) on three rows matches Taiyo's three-row figure (15 row-weighted). IDT, DDT and DDG are single rows and run +2/+3/+5 to +10 (45/45/40%), Taiyo's single-row DDT/DDG scale; IDT is a full route here because Ice Palace is the only exposure row. IDG is glue (+2 root, +3 capstone secondary; max +5 = 40%) because it stacks on the 28.75% passive at level 25. Heal is a secondary only (+3 / +2, max +3): static ×10 gives 280 HP per tick, a small absolute value.
- Resolver reads: Aegis DDT and Coffin DDG list all four stat types with no element, so the filter is not binding (SOURCE_MECHANICS §3): they act on every non-pierce hit taken or dealt. Frostbound IDG and Ice Palace IDT carry Ice/None/Water/Wind with no stat types, so they match Ice, Water, Wind and element-less hits (basic attacks, normal jutsu, weapons) by caster or allies and skip pierce. The Damage rows are Ice Genjutsu formula rows; the 25% + 0.15/level IDG passive multiplies them downstream.
- Delivery: all five jutsu have cooldown 7; the three attacks cost 60 AP, Cryostorm Aegis and Frostbound Ascendancy 40 AP; percentage rows last 2 rounds. Frostbound's IDG row is target SELF, so it is realized on the caster at cast time regardless of the spiral spawn (actions.ts 980-1004); its absorb and recoil rows are unsupported. Ice Palace is AOE_CIRCLE_SPAWN radius 1 on OTHER_USER: both rows land once on each living non-caster in the circle. Aegis heal ticks on the two following rounds.
- Fourth purchases: Burst takes Vigil of Winter (37% guard, 32% suppression) or Hairline Fracture (40% exposure); Exposure takes Vigil of Winter or Killing Frost (+2 power); Bulwark takes First Snow of Heaven (37% exposure and self buff) or Cold Saps the Will (35% suppression); Suppression takes First Snow of Heaven or Permafrost Mantle (40% guard). Strongest unadvertised allocation by row weight: Reign of Absolute Zero + Hairline Fracture (+5 power, 40% exposure, no guard).
- Relation to the Taiyo reference: Teno Yuki shares five of Taiyo's six supported tags, so the two-root/four-capstone frame recurs; the Teno-specific choices are that no tag crosses roots (attack root = Damage/IDG/IDT, defensive root = DDT/DDG/Heal, so every mixed build is non-dominated), Heal replaces Afterburn as the defensive capstones' secondary, and IDT is a dedicated route. Tag stacking is on at the pin (BATTLE_TAG_STACKING), so repeated casts within a window add; not simulated.

## Risks and unproven interactions

- Classification: Ice is not exclusive. Blue Blade Eyes and Hyouga Yui (INCLUDE), Blue Edge Eyes (EXCLUDE) and four DEFER records carry Ice rows; the normal-jutsu collision is unverified. Today 5 of 8 supported rows match Ice directly and 3 (Aegis DDT and Heal, Coffin DDG) fall back to None, which also reaches non-elemental rows on any jutsu. The tree needs a bloodline-scoped classification.
- Ally hazard: Ice Palace rows 0 (Damage) and 1 (IDT) are AOE_CIRCLE_SPAWN with friendly fire none (= ALL). Killing Frost and Reign of Absolute Zero raise the hit on allies in the circle to 42/45; First Snow of Heaven, Hairline Fracture and Court of Splintered Ice expose allies inside at up to 45% for two rounds. The caster is never a target (OTHER_USER). Positioning, not the node, decides.
- Exposure downstream: a 45% Ice Palace debuff adds 45% of base to every non-pierce Ice, Water, Wind or element-less hit the target takes from the caster or allies for two rounds, so its realized value scales with party damage and enemies in the circle. Flats were held to the Taiyo single-row ceiling (+10); no group-content simulation was performed.
- Guard and suppression overlap: Aegis DDT and Coffin DDG in overlapping rounds subtract both percentages of base from matching hits (100 AP across two casts). The two routes cannot be bought together (6 BP), so one build caps at 45% + 35% (Still Heart of Winter + Cold Saps the Will) or 40% + 40% (Silence of Falling Snow + Permafrost Mantle). Not simulated against the 15% Water-only DDT passive.
- Heal: Cryostorm Aegis heals 250 HP per tick at level 25; the route maxima add 30 (Still Heart of Winter) or 20 (Silence of Falling Snow) per tick on the two following rounds. This is a small absolute value against late-game pools, which is why Heal is only a capstone secondary; healprevent on the caster blocks it. Tag stacking is on at the pin, so two Aegis casts in a window stack.
- Offense stacking: Frostbound Ascendancy's 40% self IDG (Ice/None/Water/Wind, no stat filter) and the 25% + 0.15/level bloodline IDG passive both act on the kit's Damage rows and on normal jutsu, weapons and basic attacks in its two-round window; bloodline-sourced modifiers multiply, jutsu-sourced ones add. Normal-tree potency policy is unapproved, so a combined stacking audit is still required.
- No adverse rows, hidden jutsu, item gates, mode restrictions or injected children exist. Stun (Imperial Freeze), absorb and recoil (Frostbound Ascendancy) are unsupported and unchanged; no pierce, lifesteal, reflect or afterburn rows. Ranked modes suppress skill-tree and bloodline effects. No combat simulation: non-dominance of the 14 allocations is arithmetic over per-row additions only.
- Rank and shape: Teno Yuki is A-rank with a 28.75% Increase Damage Given passive at jutsu level 25 and a 100 regen bonus; the tree equalises marginal opportunity against the Taiyo reference, not final strength, and its six-tag frame is structurally close to Taiyo's because the kits share five tags. Cross-bloodline comparison (including the other Ice kits) is deferred to the roster review.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Teno Yuki jutsu inherit Ice potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

