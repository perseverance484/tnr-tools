# Primal Radiance — The Burning Hunt

**Bloodline:** Primal Radiance (BR-055, rank C, `ZewrhKT-qBQxT1eNoBWFP`) · **Revision:** Draft 4 / Fire classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Fire (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense — Fire damage (Fire Style: Beast, Fire Style: Squirrel) and Beast's self Increase Damage Given · secondary Pressure — Afterburn and Increase Damage Taken (Primal Incineration) · tertiary Defense — Decrease Damage Taken (Fire Style: Squirrel self buff).

Three of the six supported rows are directly offensive: the two Fire Damage rows (Beast 50, Squirrel 40 EP at jutsu level 25) and Beast's 35% self Increase Damage Given, with the bloodline's own Fire Increase Damage Given passive multiplying Fire hits, so offense is primary and gets both a Damage route and a buff-window route. Primal Incineration is the kit's only opener (40 AP, D-rank): its Afterburn 35% and Fire-filtered exposure 35% are single rows live for the two rounds after the cast round and paid out on later hits the target takes, so pressure is secondary with one route. Defense is a single 30% Decrease Damage Taken self buff on Fire Style: Squirrel, realized on the caster at cast time regardless of position and live for the two rounds after the cast round (60 AP, CD 6); as the kit's only defensive row it is tertiary with one route in Taiyo Kami's single-row +10% shape. Potency reaches matching supported tags on all Fire jutsu (RUL-2026-10-03-005). Wound and move are unsupported.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Fire jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hunter's Brand | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Primal Incineration / 1 |
| 02 | Fang and Ember | Hidden Art | Hunter's Brand | +2 Damage (damage) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 03 | Apex Conflagration | Advanced Art | Fang and Ember | +3 Damage (damage) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 04 | Smoldering Trail | Hidden Art | Hunter's Brand | +3% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 05 | Pyre of the Hunted | Advanced Art | Smoldering Trail | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Primal Incineration / 2 |
| 06 | Hide and Fang | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 07 | Radiant Hide | Hidden Art | Hide and Fang | +3% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 08 | Den of Embers | Advanced Art | Radiant Hide | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 09 | Kindled Fury | Hidden Art | Hide and Fang | +3% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 10 | Primal Rampage | Advanced Art | Kindled Fury | +5% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hunter's Brand** — Every quarry the beast marks is already half-burned. Primal Incineration exposure 35 → 37% (Fire hits, or hits on the caster's highest offence stat; 2 rounds). 1 row.
- **Fang and Ember** — Teeth of ember, breath of wildfire. Beast and Squirrel Fire Damage rows only (50 → 52 and 40 → 42 EP). Both 60 AP, range 4; Squirrel is a ground circle, CD 6.
- **Apex Conflagration** — When the alpha roars, the whole forest catches. The same two Damage rows; route total +5 Damage (Beast 50 → 55, Squirrel 40 → 45 EP) before the bloodline's Fire damage passive.
- **Smoldering Trail** — Where the hunted beast ran, the ground still smolders. Primal Incineration Afterburn only (one 2-round enemy debuff, 40 AP, CD 7): 35 → 38%. Value lands on every non-pierce hit the target takes.
- **Pyre of the Hunted** — The hunt ends on a pyre the prey built with its own flight. Incineration Afterburn 38 → 45% (route +10%) and exposure 37 → 40% with Hunter's Brand; one 40 AP cast carries both for 2 rounds on one target.
- **Hide and Fang** — Thick pelt, sharp fang, both lit from within. Squirrel self Decrease Damage Taken 30 → 32% (realized on the caster at cast, live the next 2 rounds, any position); Beast self Increase Damage Given 35 → 37%.
- **Radiant Hide** — A pelt of living flame that swallows every blow. Squirrel Decrease Damage Taken only (element-less row, all four stat types: every non-pierce hit): 32 → 35% with Hide and Fang.
- **Den of Embers** — Within the burning den, nothing reaches the beast. Squirrel self Decrease Damage Taken 35 → 40% (route +10%; 2 rounds per 60 AP cast) and Beast Increase Damage Given 37 → 39%.
- **Kindled Fury** — Fury stoked until the blood itself glows. Beast self Increase Damage Given only (live 2 rounds after each 60 AP cast; Fire hits or hits on the caster's highest offence stat or general): 37 → 40%.
- **Primal Rampage** — The radiant beast unbound, and nothing left to hold it. Beast Increase Damage Given 40 → 45% (route +10%) and Squirrel self Decrease Damage Taken 32 → 34%.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Apex Conflagration (Burst) | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +5 | +2% | +2% | +2% | — |
| Pyre of the Hunted (Burn pressure) | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | — | +2% | +5% | +2% | +10% |
| Den of Embers (Fortified) | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | — | +4% | +2% | +10% | — |
| Primal Rampage (Buff window) | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | — | +10% | +2% | +4% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Apex Conflagration:** The +5 Damage route on both Fire attacks (Beast 50 → 55, Squirrel 40 → 45 EP before the bloodline's Fire Increase Damage Given passive multiplies them) with Hunter's Brand's 37% exposure. Hide and Fang is the fourth purchase so Beast's self buff reaches 37% and Squirrel's self DDT 32%; Smoldering Trail (Afterburn 38%) is the all-pressure alternative.
- **Pyre of the Hunted:** One 40 AP Primal Incineration cast marks a target with 45% Afterburn (+10%) and 40% exposure for the 2 rounds after the cast round: every non-pierce hit it takes then (Beast, Squirrel, normal jutsu, weapons, allies) adds 45% Afterburn damage up to the 60% per-hit cap, and Fire hits, plus hits whose resolved stat type equals the caster's highest offence stat (e.g. the caster's basic attacks), are further multiplied by 1.40. Hide and Fang adds Beast 37% and Squirrel DDT 32%; Fang and Ember (attacks 52 / 42 EP) is the sharper alternative.
- **Den of Embers:** The beast as its own stronghold: each 60 AP Squirrel cast (CD 6) realizes 40% Decrease Damage Taken (+10%) on the caster at cast time, live on every non-pierce hit for the 2 rounds after the cast round wherever anyone stands; Beast's self buff sits at 39%. Hunter's Brand keeps the enemy-facing face alive (exposure 37%); Kindled Fury (Beast 42%) is the all-self alternative that stays under one root.
- **Primal Rampage:** Beast's self Increase Damage Given at 45% (+10%) for the 2 rounds after each 60 AP cast (never Beast's own hit, CD 7) multiplies Squirrel and other Fire hits by 1.45, and hits on the caster's highest offence stat or general (basic attacks always); non-Fire hits sharing neither are excluded. Squirrel's self DDT sits at 34%. An Incineration cast timed with Beast lays Hunter's Brand's 37% exposure under the window; Radiant Hide (DDT 37%) is the sturdier alternative fourth purchase.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortified | Buff window |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Primal Incineration | 0 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Primal Incineration | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Fire Style: Beast | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Fire Style: Beast | 1 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 39% (+4) | 45% (+10) |
| Fire Style: Beast | 2 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Fire Style: Squirrel | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Fire Style: Squirrel | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Fire Style: Squirrel | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 34% (+4) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Apex Conflagration: +5 Damage (0 + 2 + 3; on band)
  - Route Pyre of the Hunted: +10% Afterburn (0 + 3 + 7; on band)
  - Route Den of Embers: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Primal Rampage: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 6 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang (raw +19, row-weighted 19)
- Lowest row-weighted node: Hunter's Brand (2)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hunter's Brand, Fang and Ember, Apex Conflagration, Smoldering Trail | +5 Damage, +2% IDT, +3% AB |
| 2 | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +5 Damage, +2% IDG, +2% IDT, +2% DDT |
| 3 | Hunter's Brand, Fang and Ember, Smoldering Trail, Pyre of the Hunted | +2 Damage, +5% IDT, +10% AB |
| 4 | Hunter's Brand, Fang and Ember, Smoldering Trail, Hide and Fang | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Hunter's Brand, Fang and Ember, Hide and Fang, Radiant Hide | +2 Damage, +2% IDG, +2% IDT, +5% DDT |
| 6 | Hunter's Brand, Fang and Ember, Hide and Fang, Kindled Fury | +2 Damage, +5% IDG, +2% IDT, +2% DDT |
| 7 | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | +2% IDG, +5% IDT, +2% DDT, +10% AB |
| 8 | Hunter's Brand, Smoldering Trail, Hide and Fang, Radiant Hide | +2% IDG, +2% IDT, +5% DDT, +3% AB |
| 9 | Hunter's Brand, Smoldering Trail, Hide and Fang, Kindled Fury | +5% IDG, +2% IDT, +2% DDT, +3% AB |
| 10 | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | +4% IDG, +2% IDT, +10% DDT |
| 11 | Hunter's Brand, Hide and Fang, Radiant Hide, Kindled Fury | +5% IDG, +2% IDT, +5% DDT |
| 12 | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +10% IDG, +2% IDT, +4% DDT |
| 13 | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | +7% IDG, +10% DDT |
| 14 | Hide and Fang, Radiant Hide, Kindled Fury, Primal Rampage | +10% IDG, +7% DDT |

## Design notes

- Node split: the roots mirror the kit's two faces. Hunter's Brand (enemy-facing: Incineration exposure) forks into Fang and Ember → Apex Conflagration (Damage) and Smoldering Trail → Pyre of the Hunted (burn). Hide and Fang (self-facing: Squirrel self DDT plus Beast IDG) forks into Radiant Hide → Den of Embers (defense) and Kindled Fury → Primal Rampage (buff window). 2 F / 4 H / 4 A; every capstone 3 BP deep; two capstones cost 5 or 6 BP.
- Reference reuse: flats follow Taiyo Kami nearly verbatim (Damage 2/3, Afterburn 3/7 with IDT +3%, DDT 2/3/5). Departures: Hunter's Brand carries only +2% IDT (this kit's IDG is a self buff on the other root); Hide and Fang pairs DDT with IDG (no DDG row); Pyre drops Eternal Noon's IDG +3%; the fourth route is IDG 2/3/5 instead of DDG. On the self routes each capstone's +2% secondary sits one below the sibling Hidden Art's +3%.
- Recalibration (RUL-2026-10-03-005): Hunter's Brand drops its +1 Damage, so Burst is the default +5 Damage (Fang and Ember +2, Apex Conflagration +3); every other value is unchanged. Routes: Burst +5 Damage, Burn pressure +10% Afterburn, Fortified +10% Decrease Damage Taken, Buff window +10% Increase Damage Given. Maxima over every legal allocation: Damage +5, Afterburn +10%, Increase Damage Given +10%, Decrease Damage Taken +10%, Increase Damage Taken +5%.
- Passives: the Fire IDG passive (15 + 0.15/lvl, Fire only; bloodline-sourced, it multiplies) scales the Fire Damage rows. Beast's IDG row (Fire, stat and general Highest) multiplies the caster's Fire hits and hits sharing the caster's highest offence stat or general (§3; tags.ts 3407-3416). Incineration's exposure (Fire, stat Highest) covers Fire hits and hits on the debuff caster's highest offence stat (§4b). Afterburn and Squirrel's DDT (no element, all four stats) cover every non-pierce hit.
- Delivery and uptime: Incineration is 40 AP, CD 7, single target; Beast 60 AP, CD 7, single target; Squirrel 60 AP, CD 6, an EMPTY_GROUND circle. Each buff/debuff row is live in the 2 rounds after its cast round, never in it (§3b): no strike benefits from its own row, and Beast's CD 7 keeps its hit outside its IDG. Squirrel's DDT row has target SELF: realized on the caster at cast time (§4b, actions.ts 980-1004), no positioning, no leak. Only its damage and unsupported move rows are positional.
- Fourth purchases: Burst (01,02,03) → Hide and Fang (Squirrel DDT 32%, Beast 37%) or Smoldering Trail (Afterburn 38%); Burn (01,04,05) → Hide and Fang or Fang and Ember (attacks 52 / 42 EP); Fortified (06,07,08) → Hunter's Brand (exposure 37%) or Kindled Fury (Beast 42%); Buff window (06,09,10) → Hunter's Brand or Radiant Hide (DDT 37%). Six no-Advanced hybrids: 01,02,04,06; 01,02,06,07; 01,02,06,09; 01,04,06,07; 01,04,06,09; 01,06,07,09.

## Risks and unproven interactions

- Classification: Fire is shared with many other bloodlines (expected under RUL-2026-10-03-005). 4 of 6 kit rows carry Fire; the two element-less rows (Incineration's Afterburn, Squirrel's DDT) sit on Fire jutsu and need the proposed jutsu-classification resolver. Off-kit Fire coverage is unverified.
- Afterburn: Pyre of the Hunted puts Incineration's Afterburn at 45% on one target for the 2 rounds after the cast round. Every non-pierce hit it then takes (kit, normal jutsu, weapons, allies) adds floor(damage × 45%); other Afterburn sources add (§3b) under the 60%-of-hit cumulative cap, so they saturate quickly. Not a damage instance; downstream instances were not simulated.
- Exposure: Incineration's IDT row has elements ['Fire'], stat Highest; a non-empty element list pushes no 'None' (SOURCE_MECHANICS.md §3), so it amplifies Fire hits plus hits resolving to the debuff caster's highest offence stat (realizeTag copies the caster's highestOffence, §4b): the caster's basic attacks match, an ally's non-Fire hit only on that stat. Pierce excluded. Maximum +5% (40%), 2 rounds.
- IDG scope: Beast's self buff (Fire, stat and general Highest) multiplies by 1.45 (Primal Rampage), for the 2 rounds after the cast, the caster's Fire hits and hits sharing the caster's highest offence stat or general (basic attacks always): window-wide, not kit-only. Jutsu-sourced: other jutsu or skill IDG applies as its own multiplier, and the Fire passive multiplies last (§3b). Pierce excluded.
- DDT delivery: Squirrel's DDT row has target SELF on an EMPTY_GROUND spawn. Per §4b a SELF row on a ground action is realized on the caster at cast time, not through the tiles (no positioning, no leak), and per §3b it is live for the 2 rounds after the cast round. Den of Embers' 40% thus has plain per-cast uptime (60 AP, CD 6), like Beast's IDG.
- Self-buff strength: Increase Damage Given and Decrease Damage Taken both reach the +10% default ceiling on single unconditional 2-round self buffs (Beast 45%, Squirrel 40%) on a C-rank bloodline; the brief adjusts by coverage, not rank. No combat simulation.
- Damage is formula-calculated (sqrt stat scaling) and then multiplied by the Fire Increase Damage Given passive, so +5 raw EP is not a linear +5 damage. Squirrel's damage row is an area hit with friendly fire ENEMIES (no ally hazard); Beast's wound 25% and Squirrel's move are unsupported and receive nothing.
- Context not modelled: the bloodline's +10% Increase Damage Taken passive on Water (a standing weakness) is untouched by any node; skill-tree and bloodline effects are suppressed in RANKED_PVP and RANKED_SPARRING at the pin, so no Bloodright node applies there. Main-tree effects, equipment, AP, uptime and modifier delivery are outside this audit.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Fire jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

