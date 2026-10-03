# Suragu — Blood of the Caldera

**Bloodline:** Suragu (BR-074, rank A, `Ksb6ogNqc5mp4l_hRgPuW`) · **Revision:** Draft 4 / Lava classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Lava (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Infernal Stream sustain and burst (Lifesteal +5% route, Damage +5 on two Lava rows; the burst capstone also deepens leech) · secondary Decrease Damage Taken on Lava Wave (+10% route) and Afterburn pressure on Eruption Strike (+10% route) · tertiary Increase Damage Given (Lava Wave) and Increase Damage Taken (Blow of Devastation) as glue, +5% each at most.

Suragu is a rank A Sustained DPS kit whose signature cast, Infernal Stream (60 AP, A rank), carries both of the tree's offensive anchors: Damage 40 and a SELF Lifesteal 40% that is live the two rounds after the cast and never on its own hit, so the burst and sustain routes both refine it while Magma Slayer (Damage 45) adds a second Damage row in PVP only. Lava Wave (40 AP ground circle) holds Increase Damage Given 35% (SELF, on the caster at cast) and Decrease Damage Taken 30% (ground row for the caster and allies on the circle) and anchors the tank route; Eruption Strike's Afterburn 35% (circle on the enemy, ally hazard) is the opt-in pressure route, and Blow of Devastation's Increase Damage Taken 35% is the cheap D-rank exposure that glues the offense Foundation together. Every percentage tag is a single row: Decrease Damage Taken and Afterburn take Taiyo Kami's single-row +10% routes, Increase Damage Given and Increase Damage Taken stay at +5% as glue, and Lifesteal and Damage sit at their +5 hard ceilings. Potency reaches matching supported tags on all Lava jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Lava jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Magma Vein | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Blow of Devastation, Lava Wave / 2 |
| 02 | Scalding Tide | Hidden Art | Magma Vein | +2 Damage (damage) | Infernal Stream, Magma Slayer / 2 |
| 03 | Pyroclastic Surge | Advanced Art | Scalding Tide | +3 Damage (damage); +1% Lifesteal (self buff) | Infernal Stream, Magma Slayer / 3 |
| 04 | Clinging Slag | Hidden Art | Magma Vein | +3% Afterburn (enemy debuff) | Eruption Strike / 1 |
| 05 | The Mountain Wakes | Advanced Art | Clinging Slag | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Blow of Devastation, Eruption Strike, Lava Wave / 3 |
| 06 | Cooling Crust | Foundation | None | +2% Decrease Damage Taken (self buff) | Lava Wave / 1 |
| 07 | Igneous Shell | Hidden Art | Cooling Crust | +3% Decrease Damage Taken (self buff) | Lava Wave / 1 |
| 08 | Heart of the Caldera | Advanced Art | Igneous Shell | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Lava Wave / 2 |
| 09 | Molten Draught | Hidden Art | Cooling Crust | +2% Lifesteal (self buff) | Infernal Stream / 1 |
| 10 | Unquenchable Furnace | Advanced Art | Molten Draught | +3% Lifesteal (self buff); +2% Decrease Damage Taken (self buff) | Infernal Stream, Lava Wave / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Magma Vein** — The mountain's blood runs in Suragu veins, and it does not cool. Lava Wave Increase Damage Given 35 → 37% (SELF at cast, live 2 rounds after, not positional); Blow of Devastation exposure 35 → 37% (enemy, 2 rounds).
- **Scalding Tide** — What the tide touches, it takes; what it leaves behind still smokes. Infernal Stream 40 → 42 and Magma Slayer 45 → 47 EP (PVP only); both 60 AP Lava hits. Eruption Strike's pierce is unsupported.
- **Pyroclastic Surge** — The slope gives way and the whole burning hillside comes down at once. Burst: Infernal Stream 40 → 45 and Magma Slayer 45 → 50 EP on the full route (+5 Damage); Infernal Stream Lifesteal 40 → 41%. Magma Slayer is PVP only.
- **Clinging Slag** — Lava does not splash and vanish. It clings, and it keeps burning. Eruption Strike Afterburn 35 → 38% (enemy, 2 rounds after cast; ally hazard in the circle, never the caster); non-pierce hits feed it.
- **The Mountain Wakes** — The ground remembers every eruption. It has been patient long enough. Burn pressure: Eruption Strike Afterburn 35 → 45% on the full route (+10%; 60% per-hit cap); Blow exposure and Lava Wave buff 35 → 40% with Magma Vein.
- **Cooling Crust** — Black stone over a red heart: the crust shields, the heat beneath sustains. Lava Wave Decrease Damage Taken 30 → 32% (ground row: self and allies on the circle, from the round after it lands).
- **Igneous Shell** — Stone born of fire turns the blade, the fist and the flame alike. Lava Wave Decrease Damage Taken +3% (35% with Cooling Crust); ground row: self and allies on the circle; move row unchanged.
- **Heart of the Caldera** — Stand where the earth itself is molten, and nothing reaches you unburned. Fortified: Lava Wave Decrease Damage Taken 30 → 40% on the full route (+10%; self and allies on the circle); Lava Wave buff +3% (40% with Magma Vein), self at cast.
- **Molten Draught** — The flow swallows what it touches, and the Suragu grow stronger for it. Infernal Stream Lifesteal 40 → 42% (SELF, 2 rounds after cast, never its own hit); 60% cap shared with vamp; pierce counts.
- **Unquenchable Furnace** — Every wound stoked, every blow fed back into a furnace that never cools. Sustain: Infernal Stream Lifesteal 40 → 45% on the full route (+5%); Lava Wave Decrease Damage Taken +2% (34% with Cooling Crust, 37% with Igneous Shell).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Pyroclastic Surge (Burst) | Magma Vein, Scalding Tide, Pyroclastic Surge, Cooling Crust | +5 | +2% | +2% | +2% | — | +1% |
| The Mountain Wakes (Burn pressure) | Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust | — | +5% | +5% | +2% | +10% | — |
| Heart of the Caldera (Fortified off.) | Magma Vein, Cooling Crust, Igneous Shell, Heart of the Caldera | — | +5% | +2% | +10% | — | — |
| Unquenchable Furnace (Sustain) | Magma Vein, Cooling Crust, Molten Draught, Unquenchable Furnace | — | +2% | +2% | +4% | — | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Pyroclastic Surge:** +5 Damage takes Infernal Stream from 40 to 45 and Magma Slayer from 45 to 50 EP (PVP only; in PVE only Infernal Stream gains), and the bloodline's own Increase Damage Given passive (25% + 0.15/level on Lava, Earth, Fire and None) multiplies that downstream. The capstone's +1% Lifesteal takes Infernal Stream's SELF leech to 41% for the two rounds after the cast (never its own hit). Magma Vein is the required ancestor (Lava Wave buff 37% on the caster for the two rounds after its cast; exposure 37%); Cooling Crust is the fourth purchase for Decrease Damage Taken 32%. It gives up the deep leech, the tank route and the burn entirely.
- **The Mountain Wakes:** Eruption Strike's Afterburn goes from 35% to 45% for the two rounds after its cast, so every non-pierce hit the burning enemy takes then (Infernal Stream, Magma Slayer in PVP, weapons, normal jutsu, allies) carries up to 45% extra inside the 60% per-hit cap; Eruption Strike's own pierce never feeds it. The capstone's +3% Increase Damage Taken and +3% Increase Damage Given with Magma Vein take Blow of Devastation's exposure and Lava Wave's damage buff to 40% each (they compound: ×1.40 × 1.40 ≈ ×1.96 on a hit both cover), and Cooling Crust adds Decrease Damage Taken 32%. Damage is untouched, and the burn circle is an ally hazard: allies standing in it also receive the enhanced debuff; the caster never does.
- **Heart of the Caldera:** The Fortified route takes Lava Wave's ground row from 30% to 40% mitigation for the caster and any ally standing in the circle, from the round after it lands and only while on it, so one 40 AP cast becomes a team fortress tile. The capstone's +3% with Magma Vein lifts the same cast's SELF buff to 40%: that buff is realized on the caster at cast and live the two rounds after, wherever they stand, so the offensive half is unconditional. Exposure stays at 37%, Lifesteal at 40% and Afterburn at 35%, so it is neither the sustain nor the burn build; only the mitigation half depends on holding the tile.
- **Unquenchable Furnace:** The Lifesteal route takes Infernal Stream's leech from 40% to 45% (the +5% ceiling), fifteen points under the 60% cap shared with vamp, and draws from every hit the caster lands in the two rounds after the cast (never Infernal Stream's own hit), including Eruption Strike's unsupported 58-power pierce and Magma Slayer in PVP. The capstone's +2% Decrease Damage Taken with Cooling Crust leaves Lava Wave at 34% mitigation, and Magma Vein adds a 37% buff and 37% exposure. Damage is untouched. The alternative fourth purchase, Igneous Shell instead of Magma Vein, is the tank-sustain variant (Decrease Damage Taken 37%, no buff or exposure).

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
| Infernal Stream | 1 | Lifesteal | self | 40% | 41% (+1) | 40% | 40% | 45% (+5) |
| Infernal Stream | 2 | poison (unsupported) | enemy | 50% | 50% | 50% | 50% | 50% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Pyroclastic Surge: +5 Damage (0 + 2 + 3; on band)
  - Route The Mountain Wakes: +10% Afterburn (0 + 3 + 7; on band)
  - Route Heart of the Caldera: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Unquenchable Furnace: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 7 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Magma Vein, Scalding Tide, Clinging Slag, The Mountain Wakes (raw +22, row-weighted 24)
- Lowest row-weighted node: Cooling Crust (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Eruption Strike#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Magma Vein, Scalding Tide, Pyroclastic Surge, Clinging Slag | +5 Damage, +2% IDG, +2% IDT, +3% AB, +1% LS |
| 2 | Magma Vein, Scalding Tide, Pyroclastic Surge, Cooling Crust | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +1% LS |
| 3 | Magma Vein, Scalding Tide, Clinging Slag, The Mountain Wakes | +2 Damage, +5% IDG, +5% IDT, +10% AB |
| 4 | Magma Vein, Scalding Tide, Clinging Slag, Cooling Crust | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Magma Vein, Scalding Tide, Cooling Crust, Igneous Shell | +2 Damage, +2% IDG, +2% IDT, +5% DDT |
| 6 | Magma Vein, Scalding Tide, Cooling Crust, Molten Draught | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust | +5% IDG, +5% IDT, +2% DDT, +10% AB |
| 8 | Magma Vein, Clinging Slag, Cooling Crust, Igneous Shell | +2% IDG, +2% IDT, +5% DDT, +3% AB |
| 9 | Magma Vein, Clinging Slag, Cooling Crust, Molten Draught | +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% LS |
| 10 | Magma Vein, Cooling Crust, Igneous Shell, Heart of the Caldera | +5% IDG, +2% IDT, +10% DDT |
| 11 | Magma Vein, Cooling Crust, Igneous Shell, Molten Draught | +2% IDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Magma Vein, Cooling Crust, Molten Draught, Unquenchable Furnace | +2% IDG, +2% IDT, +4% DDT, +5% LS |
| 13 | Cooling Crust, Igneous Shell, Heart of the Caldera, Molten Draught | +3% IDG, +10% DDT, +2% LS |
| 14 | Cooling Crust, Igneous Shell, Molten Draught, Unquenchable Furnace | +7% DDT, +5% LS |

## Design notes

- Node split: two Foundations each fork into two Hidden -> Advanced routes, one per non-glue tag and role: Damage (burst), Afterburn (pressure), Decrease Damage Taken (tank), Lifesteal (sustain). Increase Damage Given and Increase Damage Taken sit only on Magma Vein and as capstone secondaries, never on a Hidden Art, and each capstone secondary stays below the Hidden Art flat on its tag (Pyroclastic Surge +1% Lifesteal under Molten Draught +2%; Unquenchable Furnace +2% Decrease Damage Taken under Igneous Shell +3%): all 14 full builds non-dominated, every node used.
- Calibration and Taiyo reuse: nodes 01, 02, 04, 05, 07, 08 copy Taiyo Kami's tags and flats; the shape fits as Suragu has the same four roles (burst, burn, tank, sustain). Departures: with no Decrease Damage Given row, a Lifesteal route replaces Taiyo's Suppression route (Molten Draught +2%, Unquenchable Furnace +3% plus +2% Decrease Damage Taken) and Cooling Crust carries Decrease Damage Taken only. Under RUL-2026-10-03-005 Lifesteal is held to its +5% hard ceiling: Cooling Crust's former +2% Lifesteal was removed and the route cut from +10% to +5%, and Pyroclastic Surge's Lifesteal secondary went from +2% to +1%, which it adds because PVE Damage reaches one row.
- Passives and arithmetic: the bloodline Increase Damage Given passive (25% + 0.15/level on Lava, Earth, Fire, None) multiplies enhanced Damage hits; kit Increase Damage Given and Increase Damage Taken rows each multiply a matching hit by 1 + power/100 and compound, so Lava Wave's buff at 40% and Blow's exposure at 40% give ×1.40 × 1.40 ≈ ×1.96 on a hit both cover; the Decrease Damage Taken row multiplies matching incoming hits by 1 − power/100. The passive multiplies last. Lava Wave's buff lists Earth, Fire, Lava, None, so it also raises element-less basic attacks, weapons and jutsu. Its Decrease Damage Taken row and Blow's exposure are element-less with all four stat types: they match every non-pierce hit. Lifesteal counts pierce; the rest skip it.
- Delivery and timing: all cooldowns are 7; nothing is item-gated or hidden. Buff/debuff rows act only in the two rounds after their cast round, so no cast benefits from its own row (Infernal Stream never leeches its own hit). Lava Wave (40 AP, range 5): its buff is SELF, on the caster at cast wherever they stand; only the Decrease Damage Taken row is a ground effect (INHERIT, FRIENDLY), re-applied each round to the caster and allies on the circle. Others cost 60 AP, Blow 40. Ranked PVP and ranked sparring skip the tree.
- Fourth-purchase choices: after any 3-BP route the natural fourth is the other Foundation. Unadvertised legal builds include 01+02+04+05 (the strongest burn: +2 Damage, +10% Afterburn, +5% Increase Damage Taken, +5% Increase Damage Given, no mitigation or leech), 01+02+03+04 (burst with 3% Afterburn), 06+07+08+09 (pure fortress: +10% Decrease Damage Taken, +2% Lifesteal, +3% Increase Damage Given) and 06+07+09+10 (tank-sustain: +5% Lifesteal, +7% Decrease Damage Taken). No-capstone hybrids such as 01+02+06+09 (+2 Damage, +2% Lifesteal, +2% each of Increase Damage Given, Increase Damage Taken and Decrease Damage Taken) are legal and non-dominated.
- Four examples because each capstone answers a different role with its own Advanced Art; the pressure route's value is downstream. The burst route is the lowest-value capstone in PVE: +5 Damage on one 40-power, 60 AP, cooldown-7 row (+12.5%) plus +1% Lifesteal, while sibling capstones reach +10% (Afterburn, Decrease Damage Taken) or the +5% Lifesteal ceiling; Damage cannot exceed its +5 hard ceiling.

## Risks and unproven interactions

- Classification: Lava is the single qualifying element (Magma Slayer and Infernal Stream Damage, Eruption Strike pierce); sharing it with Amaterasu is expected (RUL-2026-10-03-005). 3 of 7 kit rows carry Lava; the 4 element-less rows (Decrease Damage Taken, Increase Damage Taken, Afterburn, Lifesteal) need the proposed jutsu-classification resolver (matching None instead would reach every element-less row on any jutsu). Blow of Devastation carries no Lava row, so in-kit it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Lava coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN) is unverified.
- Ally hazard (validator warns): Eruption Strike row 1 Afterburn (AOE_CIRCLE_SPAWN on the enemy, friendly fire none) is raised by Clinging Slag and The Mountain Wakes; allies standing in that circle also receive the enhanced burn, so positioning decides; the caster is never a target of an OTHER_USER circle. The route is opt-in: no Foundation touches Afterburn; the other three builds never raise it.
- Mode restriction: Magma Slayer (Damage 45, wound) is PVP-only, so in PVE the Damage route reaches only Infernal Stream and +5 Damage is +12.5% on a single 40-power row, the lowest-value capstone at depth 3 in that mode; Pyroclastic Surge's +1% Lifesteal is its only other gain.
- Lifesteal: the route tops out at 45% (+5%, the hard ceiling), fifteen points under the 60%-of-pre-shield-damage leech budget shared with vamp; vamp from the normal tree or items can still saturate the cap. It needs both combatants alive and is blocked by healprevent on the caster. It is a SELF buff live the two rounds after a 60 AP cast, never on Infernal Stream's own hit, so with a 7-round cooldown it feeds on follow-up hits.
- Afterburn: the +10% route is one application row on a 60 AP cast whose own damage is pierce (58) and never feeds the burn; the kit holds only two instant Damage rows (one PVP-only) that can, so the route's value rests on weapons, normal jutsu and allies hitting the one burning enemy in the two rounds after the cast, capped at 60% of each hit. Not simulated.
- Stacking: BATTLE_TAG_STACKING is true at the pin, so these potency effects stack with other potency sources, and same-tag combat effects from other jutsu, recasts or allies all apply (process.ts 1109-1117), and percentage damage modifiers compound. Lava Wave's 40% buff multiplies a later matching hit by ×1.40; the bloodline passive multiplies last.
- No combat simulation: non-dominance of the 14 allocations and the row-weighted totals are arithmetic over per-row additions, not evidence of equal combat strength. Lava Wave's tile uptime, Blow of Devastation's recoil, Magma Slayer's wound, Infernal Stream's poison, Eruption Strike's pierce and AP economy were not modelled. No adverse, hidden, item-gated or injected rows exist in this kit.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Lava jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

