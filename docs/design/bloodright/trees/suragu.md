# Suragu — Blood of the Caldera

**Bloodline:** Suragu (BR-074, rank A, `Ksb6ogNqc5mp4l_hRgPuW`) · **Revision:** Draft 3 / Lava classification / forked tree · **Classification:** Lava (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Infernal Stream sustain and burst (Lifesteal +10 ceiling, Damage +5 on two Lava rows; the burst capstone also deepens leech) · secondary Decrease Damage Taken on Lava Wave (+10 ceiling) and Afterburn pressure on Eruption Strike (+10 ceiling) · tertiary Increase Damage Given (Lava Wave) and Increase Damage Taken (Blow of Devastation) as glue, +5 each.

Suragu is a rank A Sustained DPS kit whose signature cast, Infernal Stream (60 AP, A rank), carries both of the tree's offensive anchors: Damage 40 and a SELF Lifesteal 40% that is live the two rounds after the cast and never on its own hit, so the burst and sustain routes both refine it while Magma Slayer (Damage 45) adds a second Damage row in PVP only. Lava Wave (40 AP ground circle) holds IDG 35% (SELF, on the caster at cast) and DDT 30% (ground row for the caster and allies on the circle) and anchors the tank route; Eruption Strike's Afterburn 35% (circle on the enemy, ally hazard) is the opt-in pressure route, and Blow of Devastation's IDT 35% is the cheap D-rank exposure that glues the offense Foundation together. Every percentage tag is a single row: DDT and Afterburn take Taiyo Kami's single-row +10, IDG and IDT stay at +5 as glue, Lifesteal +10 is set by the 60% leech budget; Damage reaches two rows, one mode-restricted, so it stays at +5 (user decision, design note 6).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Lava-classified Suragu jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Magma Vein | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Blow of Devastation, Lava Wave / 2 |
| 02 | Scalding Tide | Hidden Art | Magma Vein | +2 Damage power (damage) | Infernal Stream, Magma Slayer / 2 |
| 03 | Pyroclastic Surge | Advanced Art | Scalding Tide | +3 Damage power (damage); +2% Lifesteal (self buff) | Infernal Stream, Magma Slayer / 3 |
| 04 | Clinging Slag | Hidden Art | Magma Vein | +3% Afterburn (enemy debuff) | Eruption Strike / 1 |
| 05 | The Mountain Wakes | Advanced Art | Clinging Slag | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Blow of Devastation, Eruption Strike, Lava Wave / 3 |
| 06 | Cooling Crust | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Lifesteal (self buff) | Infernal Stream, Lava Wave / 2 |
| 07 | Igneous Shell | Hidden Art | Cooling Crust | +3% Decrease Damage Taken (self buff) | Lava Wave / 1 |
| 08 | Heart of the Caldera | Advanced Art | Igneous Shell | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Lava Wave / 2 |
| 09 | Molten Draught | Hidden Art | Cooling Crust | +3% Lifesteal (self buff) | Infernal Stream / 1 |
| 10 | Unquenchable Furnace | Advanced Art | Molten Draught | +5% Lifesteal (self buff); +2% Decrease Damage Taken (self buff) | Infernal Stream, Lava Wave / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Magma Vein** — The mountain's blood runs in Suragu veins, and it does not cool. IDG 35% on Lava Wave (SELF at cast, live 2 rounds after, not positional) -> 37%; IDT 35% on Blow of Devastation (enemy, 2 rounds) -> 37%.
- **Scalding Tide** — What the tide touches, it takes; what it leaves behind still smokes. Damage on Infernal Stream 40 -> 42 and Magma Slayer 45 -> 47 (PVP only); both 60 AP Lava hits. Eruption Strike's pierce is unsupported.
- **Pyroclastic Surge** — The slope gives way and the whole burning hillside comes down at once. Damage 40/45 -> 45/50 on the route; Infernal Stream Lifesteal 40% -> 42% (44% with Cooling Crust). Magma Slayer is PVP only.
- **Clinging Slag** — Lava does not splash and vanish. It clings, and it keeps burning. Eruption Strike Afterburn 35% -> 38% (enemy, 2 rounds after cast; ally hazard in the circle, never the caster); non-pierce hits feed it.
- **The Mountain Wakes** — The ground remembers every eruption. It has been patient long enough. Afterburn 35% -> 45% on the route (60% per-hit cap); IDT on Blow 35% -> 40% and IDG on Lava Wave 35% -> 40% with Magma Vein.
- **Cooling Crust** — Black stone over a red heart: the crust shields, the heat beneath sustains. DDT 30% on Lava Wave (ground row: self and allies on the circle, from the round after it lands) -> 32%; Infernal Stream LS 40% -> 42%.
- **Igneous Shell** — Stone born of fire turns the blade, the fist and the flame alike. Lava Wave DDT 30% -> 35% with Cooling Crust; ground row: self and allies on the circle, from the round after it lands; move row unchanged.
- **Heart of the Caldera** — Stand where the earth itself is molten, and nothing reaches you unburned. Lava Wave DDT 30% -> 40% on the route (ground row: self and allies on the circle); IDG 35% -> 38% (40% with Magma Vein), self at cast.
- **Molten Draught** — The flow swallows what it touches, and the Suragu grow stronger for it. Infernal Stream Lifesteal 40% -> 45% with Cooling Crust (SELF, 2 rounds after cast, never its own hit); 60% cap with vamp; pierce counts.
- **Unquenchable Furnace** — Every wound stoked, every blow fed back into a furnace that never cools. Infernal Stream Lifesteal 40% -> 50% on the route; Lava Wave DDT 30% -> 34% with Cooling Crust (37% with Igneous Shell).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Pyroclastic Surge (Burst) | Magma Vein, Scalding Tide, Pyroclastic Surge, Cooling Crust | +5 | +2% | +2% | +2% | — | +4% |
| The Mountain Wakes (Burn pressure) | Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust | — | +5% | +5% | +2% | +10% | +2% |
| Heart of the Caldera (Fortified off.) | Magma Vein, Cooling Crust, Igneous Shell, Heart of the Caldera | — | +5% | +2% | +10% | — | +2% |
| Unquenchable Furnace (Sustain) | Magma Vein, Cooling Crust, Molten Draught, Unquenchable Furnace | — | +2% | +2% | +4% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Pyroclastic Surge:** Damage +5 takes Infernal Stream from 40 to 45 and Magma Slayer from 45 to 50 (PVP only; in PVE only Infernal Stream gains), and the bloodline's own IDG passive (25% + 0.15/level on Lava, Earth, Fire and None) multiplies that raw power downstream. The capstone's +2 Lifesteal with Cooling Crust takes Infernal Stream's SELF leech to 44% for the two rounds after the cast (never its own hit), so follow-ups such as Eruption Strike's pierce or the bigger Magma Slayer in PVP heal more and the capstone deepens sustain as well as burst. Magma Vein is the required ancestor (IDG 37% on the caster for the two rounds after Lava Wave's cast; exposure 37%); Cooling Crust is the fourth purchase for DDT 32%. It gives up the deep leech, the tank route and the burn entirely.
- **The Mountain Wakes:** Eruption Strike's Afterburn goes from 35% to 45% for the two rounds after its cast, so every non-pierce hit the burning enemy takes then (Infernal Stream, Magma Slayer in PVP, weapons, normal jutsu, allies) carries up to 45% extra inside the 60% per-hit cap; Eruption Strike's own pierce never feeds it. The capstone's +3 IDT and +3 IDG with Magma Vein take Blow of Devastation's exposure and Lava Wave's damage buff to 40% each (they add: 80% of the staged base on a hit both cover), and Cooling Crust adds DDT 32% and Lifesteal 42%. Raw Damage power is untouched, and the burn circle is an ally hazard: allies standing in it also receive the enhanced debuff; the caster never does.
- **Heart of the Caldera:** The DDT route takes Lava Wave's ground row from 30% to 40% mitigation for the caster and any ally standing in the circle, from the round after it lands and only while on it, so one 40 AP cast becomes a team fortress tile. The capstone's +3 IDG with Magma Vein lifts the same cast's SELF row to 40%: that buff is realized on the caster at cast and live the two rounds after, wherever they stand, so the offensive half is unconditional. Exposure stays at 37% and Lifesteal at 42% from Cooling Crust, Afterburn at 35%, so it is neither the sustain nor the burn build; only the DDT half depends on holding the tile.
- **Unquenchable Furnace:** The lifesteal route takes Infernal Stream's leech from 40% to 50%, ten points under the 60% cap shared with vamp, and draws from every hit the caster lands in the two rounds after the cast (never Infernal Stream's own hit), including Eruption Strike's unsupported 58-power pierce and Magma Slayer in PVP. The capstone's +2 DDT with Cooling Crust leaves Lava Wave at 34% mitigation, and Magma Vein adds IDG 37% and exposure 37%. Raw Damage is untouched. The alternative fourth purchase, Igneous Shell instead of Magma Vein, is the tank-sustain variant (DDT 37%, no IDG or exposure).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortified off. | Sustain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Lava Wave | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Lava Wave | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 34% (+4) |
| Lava Wave | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Blow of Devastation | 0 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Blow of Devastation | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Eruption Strike | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Eruption Strike | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Magma Slayer | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Magma Slayer | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Infernal Stream | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Infernal Stream | 1 | Lifesteal | self | 40% | 44% (+4) | 42% (+2) | 42% (+2) | 50% (+10) |
| Infernal Stream | 2 | poison (unsupported) | enemy | 50% | 50% | 50% | 50% | 50% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Increase Damage Taken +5%, Decrease Damage Taken +10%, Afterburn +10%, Lifesteal +10% (not jointly attainable)
- Supported rows in kit: 7 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust (raw +24, row-weighted 24)
- Lowest row-weighted node: Clinging Slag (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Eruption Strike#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Magma Vein, Scalding Tide, Pyroclastic Surge, Clinging Slag | DMG +5, IDG +2, IDT +2, AB +3, LS +2 |
| 2 | Magma Vein, Scalding Tide, Pyroclastic Surge, Cooling Crust | DMG +5, IDG +2, IDT +2, DDT +2, LS +4 |
| 3 | Magma Vein, Scalding Tide, Clinging Slag, The Mountain Wakes | DMG +2, IDG +5, IDT +5, AB +10 |
| 4 | Magma Vein, Scalding Tide, Clinging Slag, Cooling Crust | DMG +2, IDG +2, IDT +2, DDT +2, AB +3, LS +2 |
| 5 | Magma Vein, Scalding Tide, Cooling Crust, Igneous Shell | DMG +2, IDG +2, IDT +2, DDT +5, LS +2 |
| 6 | Magma Vein, Scalding Tide, Cooling Crust, Molten Draught | DMG +2, IDG +2, IDT +2, DDT +2, LS +5 |
| 7 | Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust | IDG +5, IDT +5, DDT +2, AB +10, LS +2 |
| 8 | Magma Vein, Clinging Slag, Cooling Crust, Igneous Shell | IDG +2, IDT +2, DDT +5, AB +3, LS +2 |
| 9 | Magma Vein, Clinging Slag, Cooling Crust, Molten Draught | IDG +2, IDT +2, DDT +2, AB +3, LS +5 |
| 10 | Magma Vein, Cooling Crust, Igneous Shell, Heart of the Caldera | IDG +5, IDT +2, DDT +10, LS +2 |
| 11 | Magma Vein, Cooling Crust, Igneous Shell, Molten Draught | IDG +2, IDT +2, DDT +5, LS +5 |
| 12 | Magma Vein, Cooling Crust, Molten Draught, Unquenchable Furnace | IDG +2, IDT +2, DDT +4, LS +10 |
| 13 | Cooling Crust, Igneous Shell, Heart of the Caldera, Molten Draught | IDG +3, DDT +10, LS +5 |
| 14 | Cooling Crust, Igneous Shell, Molten Draught, Unquenchable Furnace | DDT +7, LS +10 |

## Design notes

- Node split: two Foundations each fork into two Hidden -> Advanced routes, one per non-glue tag and role: Damage (burst), Afterburn (pressure), DDT (tank), Lifesteal (sustain). IDG and IDT sit only on Magma Vein and as capstone secondaries, never on a Hidden Art, and each capstone secondary stays below the Hidden Art flat on its tag (Pyroclastic Surge +2 LS under Molten Draught +3; Unquenchable Furnace +2 DDT under Igneous Shell +3): all 14 full builds non-dominated, every node used.
- Calibration and Taiyo reuse: nodes 01, 02, 04, 05, 07, 08 copy Taiyo Kami's tags and flats; the shape fits as Suragu has the same four roles (burst, burn, tank, sustain). Departures: with no DDG row, Lifesteal (set by the 60% leech cap) replaces DDG on 06 (+2), 09 (+3) and 10 (+5, plus DDT +2 under Igneous Shell's +3, not IDT +5); 03 adds LS +2 as PVE Damage reaches one row. DDT/AB +10 equal Taiyo; IDT +5 is under its +7; IDG +5 reaches one row (Taiyo two). Top build 24 on 7 rows vs 31 on 9.
- Passives and arithmetic: the bloodline IDG passive (25% + 0.15/level on Lava, Earth, Fire, None) multiplies enhanced Damage hits; kit IDG/IDT/DDT add power/100 x staged base, so Lava Wave IDG 40% and Blow IDT 40% add 80% to a hit both cover. Lava Wave's IDG lists Earth, Fire, Lava, None, so it also raises element-less basic attacks, weapons and jutsu. Its DDT and Blow's IDT are element-less with all four stat types: they match every non-pierce hit. Lifesteal counts pierce; the rest skip it.
- Delivery and timing: all cooldowns are 7; nothing is item-gated or hidden. Buff/debuff rows act only in the two rounds after their cast round, so no cast benefits from its own row (Infernal Stream never leeches its own hit). Lava Wave (40 AP, range 5): IDG is SELF, on the caster at cast wherever they stand; only DDT is a ground effect (INHERIT, FRIENDLY), re-applied each round to the caster and allies on the circle. Others cost 60 AP, Blow 40. Ranked PVP and ranked sparring skip the tree.
- Fourth-purchase choices: after any 3-BP route the natural fourth is the other Foundation. Unadvertised legal builds include 01+02+04+05 (the strongest burn: +2 Damage, +10 Afterburn, +5 IDT, +5 IDG, no mitigation or leech), 01+02+03+04 (burst with 3% Afterburn), 06+07+08+09 (pure fortress: +10 DDT, +5 Lifesteal, +3 IDG) and 06+07+09+10 (tank-sustain: +10 Lifesteal, +7 DDT). No-capstone hybrids such as 01+02+06+09 (+2 Damage, +5 Lifesteal, +2 IDG/IDT/DDT) are legal and non-dominated.
- Four examples because each capstone answers a different role with its own Advanced Art; the pressure route's value is downstream. USER DECISION: Damage ceiling +5 (Pyroclastic Surge +3) or +6 (+4). As drafted the burst route is the lowest-value capstone at depth 3: in PVE it is +5 on one 40-power, 60 AP, 7-cooldown row (+12.5%) plus LS +2, while sibling capstones add +10 to their rows; +6 (guardrail max) gives PVE +15%. The +2 LS stays either way. Also open: +3 IDG on Mountain Wakes; LS cap 50%.

## Risks and unproven interactions

- Classification: Lava is the kit's single signature element (Magma Slayer and Infernal Stream Damage, Eruption Strike pierce) but is not exclusive in the census: Amaterasu [DEFER] carries Lava on 3 rows (2 damage). The label therefore has to be bloodline-scoped under the proposed whole-kit classification, not a bare element match. Whether any non-bloodline jutsu carries Lava is unverified.
- Resolver: 4 of 7 supported rows (DDT, IDT, Afterburn, Lifesteal) carry no element and fall back to None under the current resolver; affectedElements=['Lava'] matches only Lava Wave IDG and the two Damage rows directly. Reaching the rest today needs None, which also reaches every non-elemental row on any jutsu the player casts. The tree assumes the proposed whole-kit classification.
- Ally hazard (validator warns): Eruption Strike row 1 Afterburn (AOE_CIRCLE_SPAWN on the enemy, friendly fire none) is raised by Clinging Slag and The Mountain Wakes; allies standing in that circle also receive the enhanced burn, so positioning decides; the caster is never a target of an OTHER_USER circle. The route is opt-in: no Foundation touches Afterburn; the other three builds never raise it.
- Mode restriction: Magma Slayer (Damage 45, wound) is PVP-only, so in PVE the Damage route reaches only Infernal Stream and the +5 ceiling is +12.5% on a single 40-power row, the lowest-value capstone at depth 3 in that mode. The route was weighted accordingly (+5 rather than +6, Lifesteal secondary on the capstone); the +5 vs +6 ceiling is the user decision recorded in design note 6.
- Lifesteal: the route tops out at 50%, ten points under the 60%-of-pre-shield-damage leech budget shared with vamp; vamp from the normal tree or items can saturate the cap. It needs both combatants alive and is blocked by healprevent on the caster. It is a SELF buff live the two rounds after a 60 AP cast, never on Infernal Stream's own hit, so with a 7-round cooldown it feeds on follow-up hits.
- Afterburn: the +10 route is one application row on a 60 AP cast whose own damage is pierce (58) and never feeds the burn; the kit holds only two instant Damage rows (one PVP-only) that can, so the route's value rests on weapons, normal jutsu and allies hitting the one burning enemy in the two rounds after the cast, capped at 60% of each hit. Not simulated.
- Stacking: BATTLE_TAG_STACKING is true at the pin, so these potency effects stack with other potency sources, and same-tag combat effects from other jutsu, recasts or allies all apply and add (process.ts 1109-1117); the budget with a future normal-tree potency policy is unaudited. The bloodline IDG passive multiplies enhanced Damage hits; Lava Wave's 40% IDG adds 40% of staged base to a later hit.
- No combat simulation: non-dominance of the 14 allocations and the row-weighted totals are arithmetic over per-row additions, not evidence of equal combat strength. Lava Wave's DDT tile uptime, Blow of Devastation's recoil, Magma Slayer's wound, Infernal Stream's poison, Eruption Strike's pierce and AP economy were not modelled. No adverse, hidden, item-gated or injected rows exist in this kit.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Suragu jutsu inherit Lava potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

