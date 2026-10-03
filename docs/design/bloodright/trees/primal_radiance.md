# Primal Radiance — The Burning Hunt

**Bloodline:** Primal Radiance (BR-055, rank C, `ZewrhKT-qBQxT1eNoBWFP`) · **Revision:** Draft 1 / Primal Radiance classification / forked tree · **Classification:** Primal Radiance (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Offense — Fire damage (Fire Style: Beast, Fire Style: Squirrel) and Beast's self Increase Damage Given · secondary Pressure — Afterburn and Increase Damage Taken (Primal Incineration) · tertiary Defense — Decrease Damage Taken (Fire Style: Squirrel circle).

Four of the six supported rows are offensive: the two Fire damage rows (Beast 50, Squirrel 40 at jutsu level 25) and Beast's 35% self Increase Damage Given, plus the bloodline's own Fire Increase Damage Given passive multiplying them, so offense is primary and is given both a raw-power route and a buff-window route. Primal Incineration is the kit's only opener (40 AP, D-rank): its Afterburn 35% and Fire-filtered exposure 35% are single rows whose value lands on every later hit the target takes, so pressure is secondary with one route. Defense is a single 30% Decrease Damage Taken row on Squirrel's ground circle, conditional on standing inside it; it is tertiary and gets one route held to Taiyo Kami's single-row +10 shape. Wound and move are unsupported.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Primal Radiance jutsu (bloodline-keyed classification, proposed extension) under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hunter's Brand | Foundation | None | +2% Increase Damage Taken (enemy debuff); +1 Damage power (damage) | Fire Style: Beast, Fire Style: Squirrel, Primal Incineration / 3 |
| 02 | Fang and Ember | Hidden Art | Hunter's Brand | +2 Damage power (damage) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 03 | Apex Conflagration | Advanced Art | Fang and Ember | +3 Damage power (damage) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 04 | Smoldering Trail | Hidden Art | Hunter's Brand | +3% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 05 | Pyre of the Hunted | Advanced Art | Smoldering Trail | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Primal Incineration / 2 |
| 06 | Hide and Fang | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 07 | Radiant Hide | Hidden Art | Hide and Fang | +3% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 08 | Den of Embers | Advanced Art | Radiant Hide | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 09 | Kindled Fury | Hidden Art | Hide and Fang | +3% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 10 | Primal Rampage | Advanced Art | Kindled Fury | +5% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hunter's Brand** — Every quarry the beast marks is already half-burned. Primal Incineration exposure 35→37% (Fire or element-less hits, 2 rounds); Beast 50→51 and Squirrel 40→41 Fire damage. 3 rows.
- **Fang and Ember** — Teeth of ember, breath of wildfire. Beast and Squirrel Fire damage rows only (51→53 and 41→43 with Hunter's Brand). Both 60 AP, range 4; Squirrel is a ground circle, CD 6.
- **Apex Conflagration** — When the alpha roars, the whole forest catches. The same two damage rows; the route totals +6 power (Beast 50→56, Squirrel 40→46) before the bloodline's Fire damage passive.
- **Smoldering Trail** — Where the hunted beast ran, the ground still smolders. Primal Incineration Afterburn only (one 2-round enemy debuff, 40 AP, CD 7): 35→38%. Value lands on every non-pierce hit the target takes.
- **Pyre of the Hunted** — The hunt ends on a pyre the prey built with its own flight. Incineration Afterburn 38→45% and exposure 37→40% with Hunter's Brand; one 40 AP cast carries both for 2 rounds on one target.
- **Hide and Fang** — Thick pelt, sharp fang, both lit from within. Squirrel circle Decrease Damage Taken 30→32% (while standing in it, from the next round); Beast self Increase Damage Given 35→37%.
- **Radiant Hide** — A hide that drinks the flame it stands in. Squirrel Decrease Damage Taken only (element-less row, all four stat types: every non-pierce hit): 32→35% with Hide and Fang.
- **Den of Embers** — Within the burning den, nothing reaches the beast. Squirrel circle 35→40% Decrease Damage Taken (the +10 route ceiling) and Beast Increase Damage Given 37→39%.
- **Kindled Fury** — Fury stoked until the blood itself glows. Beast Increase Damage Given only (self, 2 rounds after a 60 AP cast, Fire or element-less hits): 37→40% with Hide and Fang.
- **Primal Rampage** — The radiant beast unbound, and nothing left to hold it. Beast Increase Damage Given 40→45% (the +10 route ceiling) and Squirrel circle Decrease Damage Taken 32→34%.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Apex Conflagration (Burst) | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +6 | +2% | +2% | +2% | — |
| Pyre of the Hunted (Burn pressure) | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | +1 | +2% | +5% | +2% | +10% |
| Den of Embers (Fortified) | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | +1 | +4% | +2% | +10% | — |
| Primal Rampage (Buff window) | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +1 | +10% | +2% | +4% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Apex Conflagration:** The +6 power route on both Fire attacks (Beast 50→56, Squirrel 40→46 before the bloodline's Fire Increase Damage Given passive multiplies them) with Hunter's Brand's 37% exposure. Hide and Fang is the fourth purchase so Beast's self buff reaches 37% and the Squirrel circle 32%; Smoldering Trail (Afterburn 38%) is the all-pressure alternative.
- **Pyre of the Hunted:** One 40 AP Primal Incineration cast marks a target with 45% Afterburn and 40% exposure for 2 rounds: every non-pierce hit it then takes (Beast, Squirrel, normal jutsu, weapons, allies) adds 45% Afterburn damage up to the 60% per-hit cap, and Fire or element-less hits are amplified a further 40%. Attacks sit at 51 and 41. Hide and Fang adds Beast 37% and circle 32%; Fang and Ember (attacks 53 / 43) is the sharper alternative.
- **Den of Embers:** The Squirrel circle as a stronghold: 40% Decrease Damage Taken on every non-pierce hit while the caster stands inside it (from the round after the cast), with Beast's self buff at 39%. Hunter's Brand keeps the enemy-facing face alive (exposure 37%, attacks 51 / 41); Kindled Fury (Beast 42%) is the all-self alternative that stays under one root.
- **Primal Rampage:** Beast's self Increase Damage Given at 45% for the 2 rounds after each 60 AP cast, multiplying Squirrel, normal jutsu, weapons and basic attacks that are Fire or element-less, with the circle at 34%. Hunter's Brand gives the setup cast a 37% exposure to stack the window on; Radiant Hide (circle 37%) is the sturdier alternative fourth purchase.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortified | Buff window |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Primal Incineration | 0 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Primal Incineration | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Fire Style: Beast | 0 | Damage | enemy | 50 | 56 (+6) | 51 (+1) | 51 (+1) | 51 (+1) |
| Fire Style: Beast | 1 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 39% (+4) | 45% (+10) |
| Fire Style: Beast | 2 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Fire Style: Squirrel | 0 | Damage | enemy | 40 | 46 (+6) | 41 (+1) | 41 (+1) | 41 (+1) |
| Fire Style: Squirrel | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Fire Style: Squirrel | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 34% (+4) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +6, Increase Damage Given +10%, Increase Damage Taken +5%, Decrease Damage Taken +10%, Afterburn +10% (not jointly attainable)
- Supported rows in kit: 6 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang (raw +20, row-weighted 21)
- Lowest row-weighted node: Smoldering Trail (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hunter's Brand, Fang and Ember, Apex Conflagration, Smoldering Trail | DMG +6, IDT +2, AB +3 |
| 2 | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | DMG +6, IDG +2, IDT +2, DDT +2 |
| 3 | Hunter's Brand, Fang and Ember, Smoldering Trail, Pyre of the Hunted | DMG +3, IDT +5, AB +10 |
| 4 | Hunter's Brand, Fang and Ember, Smoldering Trail, Hide and Fang | DMG +3, IDG +2, IDT +2, DDT +2, AB +3 |
| 5 | Hunter's Brand, Fang and Ember, Hide and Fang, Radiant Hide | DMG +3, IDG +2, IDT +2, DDT +5 |
| 6 | Hunter's Brand, Fang and Ember, Hide and Fang, Kindled Fury | DMG +3, IDG +5, IDT +2, DDT +2 |
| 7 | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | DMG +1, IDG +2, IDT +5, DDT +2, AB +10 |
| 8 | Hunter's Brand, Smoldering Trail, Hide and Fang, Radiant Hide | DMG +1, IDG +2, IDT +2, DDT +5, AB +3 |
| 9 | Hunter's Brand, Smoldering Trail, Hide and Fang, Kindled Fury | DMG +1, IDG +5, IDT +2, DDT +2, AB +3 |
| 10 | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | DMG +1, IDG +4, IDT +2, DDT +10 |
| 11 | Hunter's Brand, Hide and Fang, Radiant Hide, Kindled Fury | DMG +1, IDG +5, IDT +2, DDT +5 |
| 12 | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | DMG +1, IDG +10, IDT +2, DDT +4 |
| 13 | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | IDG +7, DDT +10 |
| 14 | Hide and Fang, Radiant Hide, Kindled Fury, Primal Rampage | IDG +10, DDT +7 |

## Design notes

- Node split: the roots mirror the kit's two faces. Hunter's Brand (enemy-facing: Incineration exposure plus both Fire damage rows) forks into Fang and Ember → Apex Conflagration (raw damage) and Smoldering Trail → Pyre of the Hunted (burn). Hide and Fang (self-facing: Squirrel circle DDT plus Beast IDG) forks into Radiant Hide → Den of Embers (defense) and Kindled Fury → Primal Rampage (buff window). 2 F / 4 H / 4 A; every capstone 3 BP deep; two capstones cost 5 or 6 BP.
- Flats scale by coverage, not rank. Damage reaches 2 rows (Taiyo: 3), so the route totals +6 (1+2+3, the guardrail): Beast 50→56, Squirrel 40→46. Afterburn is 3+7 = +10 (35→45%). Increase Damage Taken is one Fire-filtered row and reaches only +5 (Brand +2, Pyre +3; 35→40%), under Taiyo's +7. DDT and IDG are each one self-buff row and take Taiyo's single-row 2/3/5 shape (+10: circle 30→40%, Beast 35→45%); capstone secondaries are +2, one below the sibling Hidden Art, so no hybrid is dominated.
- Passives and main tree: the Fire IDG passive (15 + 0.15/lvl; bloodline sources multiply) scales the enhanced Fire damage rows. Beast's IDG is jutsu-sourced and, via its Fire element and Highest stat filter, boosts every qualifying hit the caster lands for 2 rounds: Squirrel, normal jutsu, weapons, basic attacks. Incineration's exposure and Afterburn amplify kit, normal, weapon and ally hits on the target. Squirrel's element-less four-stat DDT row covers nearly every non-pierce hit.
- Delivery and uptime: Primal Incineration is 40 AP, CD 7, single target; both debuffs last 2 rounds per 7-round cooldown. Beast is 60 AP, CD 7, single target; its self buff lasts 2 rounds. Squirrel is 60 AP, CD 6, an EMPTY_GROUND circle: its DDT is re-applied each round to whoever stands on the tiles, reaches the caster from the round after the cast (the move row sorts last) and only while they stay inside; spawn duration is not in the dossier. Potency changes percentages and powers only.
- Fourth purchases: Burst (01,02,03) → Hide and Fang (circle 32%, Beast 37%) or Smoldering Trail (Afterburn 38%); Burn (01,04,05) → Hide and Fang or Fang and Ember (attacks 53 / 43); Fortified (06,07,08) → Hunter's Brand (exposure 37%, attacks 51 / 41) or Kindled Fury (Beast 42%); Buff window (06,09,10) → Hunter's Brand or Radiant Hide (circle 37%). Six no-Advanced hybrids: 01,02,04,06; 01,02,06,07; 01,02,06,09; 01,04,06,07; 01,04,06,09; 01,06,07,09. All 14 full allocations are non-dominated.
- Strongest unadvertised allocation by row weight (Σ flat × rows reached): 01,02,04,05 (Damage +3, exposure +5, Afterburn +10) scores 21, level with the advertised Burn build; Burst, Fortified and Buff window score 18 each. Taiyo Kami's full builds span 20–31 on 9 rows, so the scale is proportionate to 6 rows. Lowest row-weighted nodes: Smoldering Trail, Radiant Hide, Kindled Fury (3 each), single-row Hidden Arts whose value is downstream (Afterburn) or window-wide (the self buffs).

## Risks and unproven interactions

- Classification: Fire sits on rows of 29 other census bloodlines, so the label is the bloodline-keyed extension 'Primal Radiance' (proposed whole-kit resolver plus a classification extension). With ['Fire'] today, 4 of 6 rows match directly; the two element-less rows (Afterburn, Squirrel DDT) fall back to None, which also reaches other non-elemental jutsu. Normal-jutsu Fire collisions unverified.
- Afterburn: Pyre of the Hunted puts Incineration's Afterburn at 45% for 2 rounds on one target. Every non-pierce hit it takes (kit, normal jutsu, weapons, allies) adds floor(damage × 45%), cumulative Afterburn per hit capped at 60% of the hit, so it saturates alongside other Afterburn sources. BATTLE_TAG_STACKING is on at the pin. Not a damage instance; downstream instances were not simulated.
- Exposure scope: Incineration's Increase Damage Taken row carries elements ['Fire'] with a Highest stat filter, so it amplifies Fire or element-less hits (and hits sharing the resolved Highest stat; which side's stats resolve 'Highest' for a target-side debuff was not verified). Pierce hits are excluded. Maximum +5 (40%) for 2 rounds per 40 AP cast on CD 7.
- IDG leakage: Beast's self buff (elements Fire, stat Highest) multiplies every qualifying hit the caster lands for 2 rounds, so Primal Rampage's 45% is a window-wide multiplier on Squirrel, normal jutsu, weapons and basic attacks, not kit-only. Jutsu-sourced, additive with other jutsu/skill modifiers; the Fire passive multiplies on top. Pierce excluded; realized only inside the 2-round window.
- DDT delivery: Squirrel's row sits on an EMPTY_GROUND circle spawn with friendly fire ALL (target SELF). The dossier derives the recipient as self, but allies on the tiles may also receive it (beneficial leakage, unverified); it reaches the caster from the round after the cast, only while standing inside; spawn duration was not read. Den of Embers' 40% has conditional uptime tied to a 60 AP cast.
- Value decisions (user-owned): Increase Damage Given and Decrease Damage Taken both reach +10 on single rows (Beast 45%, circle 40%), Damage +6 on 2 rows at the guardrail, Afterburn +10. The brief says to adjust by coverage rather than rank, but this is a C-rank bloodline; lower self-buff ceilings (for example 2/3/4 = +9) remain available if the user prefers. No combat simulation was performed.
- Damage is formula-calculated (sqrt stat scaling) and then multiplied by the Fire Increase Damage Given passive, so +6 raw power is not a linear +6 damage. Squirrel's damage row is an area hit with friendly fire ENEMIES (no ally hazard); Beast's wound 25% and Squirrel's move are unsupported and receive nothing.
- Context not modelled: the bloodline's +10% Increase Damage Taken passive on Water (a standing weakness) is untouched by any node; skill-tree and bloodline effects are suppressed in RANKED_PVP and RANKED_SPARRING at the pin, so no Bloodright node applies there. Main-tree effects, equipment, AP, uptime and modifier delivery are outside this audit.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Primal Radiance jutsu inherit Primal Radiance potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

