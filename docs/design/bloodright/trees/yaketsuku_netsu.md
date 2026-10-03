# Yaketsuku Netsu — Scorch and Steel

**Bloodline:** Yaketsuku Netsu (BR-092, rank B, `clh4d6qfn000etb0hydj4cdpl`) · **Revision:** Draft 3 / Yaketsuku Netsu classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Yaketsuku Netsu (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Damage — both attacks (Forgotten Ember Blade, Forbidden Chakra Fury; two formula rows at 40 EP) · secondary Increase Damage Given — Forgotten Ember Blade's self heat (single row, +10% route) · tertiary Increase Damage Taken — Forbidden Chakra Fury's exposure (single enemy row, +10% route).

The kit's four supported rows sit on two C-rank, 60 AP, range-4 single-target attacks: Forgotten Ember Blade (cooldown 6) deals 40 EP formula damage (Bukijutsu / Speed, Strength) and gives the caster 30% Increase Damage Given for the 2 rounds after the cast (Bukijutsu-filtered, element-less); Forbidden Chakra Fury (cooldown 7) deals 40 EP formula damage (Highest) and leaves the target with 30% Increase Damage Taken for the 2 rounds after the cast (four stat types, element-less). Damage is the only two-row tag and is always on, so it is primary; the self heat is the bloodline's identity (its passive is a Bukijutsu Increase Damage Given of 22 + 0.15 per level) and the exposure row amplifies every non-pierce source, allies included; each takes a +10% route. Chakra Shield (absorb 30%, shield 100) is unsupported, so the tree has no defensive route. Potency reaches matching supported tags on all Yaketsuku Netsu-classified jutsu (RUL-2026-10-03-005; requires a classification extension).

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four: the kit has three supported tags on four rows (Damage x2 on Forgotten Ember Blade and Forbidden Chakra Fury; Increase Damage Given x1 on Ember Blade; Increase Damage Taken x1 on Chakra Fury); Chakra Shield's absorb and shield are not potency targets. Universal opener accepted as a design choice, not a four-row impossibility: Heat in the Steel is in all 8 legal full builds because Blistered Guard has one child. A leaf Hidden Art under Blistered Guard would end it but has no fourth role to serve: a Damage or Increase Damage Given leaf twins Searing Edge or Fever Pitch, a mixed +1/+1 leaf is filler, and any Increase Damage Taken flat lifts the exposure maximum above +10%. A +2 Damage leaf remains a user-visible layout option (design notes).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yaketsuku Netsu-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Heat in the Steel | Foundation | None | +2% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 02 | Searing Edge | Hidden Art | Heat in the Steel | +2 Damage (damage) | Forbidden Chakra Fury, Forgotten Ember Blade / 2 |
| 03 | Blade That Never Cools | Advanced Art | Searing Edge | +3 Damage (damage) | Forbidden Chakra Fury, Forgotten Ember Blade / 2 |
| 04 | Fever Pitch | Hidden Art | Heat in the Steel | +3% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 05 | White-Hot Blood | Advanced Art | Fever Pitch | +5% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 06 | Blistered Guard | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 07 | Heat Finds the Seam | Hidden Art | Blistered Guard | +3% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 08 | Nothing Left Forbidden | Advanced Art | Heat Finds the Seam | +5% Increase Damage Taken (enemy debuff); +1 Damage (damage) | Forbidden Chakra Fury, Forgotten Ember Blade / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Heat in the Steel** — The forgotten ember never went out. It waited in the steel for a hand to wake it. Forgotten Ember Blade Increase Damage Given 30 → 32% (self, the 2 rounds after casting). No Damage on the root, so the Damage route stays at +5.
- **Searing Edge** — Where the edge passes, the air itself blisters. Both attacks 40 → 42 EP; formula hits (Bukijutsu / Highest), single-target, range 4; no gates, no hidden rows.
- **Blade That Never Cools** — Quench it in blood, quench it in rain; the heat only climbs. Route total +5 Damage: Ember Blade and Chakra Fury 40 → 45 EP on every cast (60 AP, cooldowns 6 and 7), the kit's only hits.
- **Fever Pitch** — Every swing feeds the heat, and the heat feeds the next swing. Ember Blade Increase Damage Given 35% with Heat in the Steel (self, the 2 rounds after casting); element-less hits of any stat.
- **White-Hot Blood** — Past red, past fear, the blood runs white and nothing it touches survives. Route total +10%: Ember Blade self Increase Damage Given 30 → 40% for the 2 rounds after casting (never its own hit); no pierce.
- **Blistered Guard** — Fury leaves the skin raw, and raw skin remembers every blow that follows. Chakra Fury Increase Damage Taken 30 → 32% (enemy, the 2 rounds after casting); four stat types, element-less: every non-pierce hit.
- **Heat Finds the Seam** — Armor has seams. Heat finds every one of them. Chakra Fury Increase Damage Taken 35% with Blistered Guard (enemy, 2 rounds after cast); allies' and normal-jutsu hits count.
- **Nothing Left Forbidden** — The seal is gone. What was held back is held back no more. Route total +10%: Chakra Fury Increase Damage Taken 30 → 40% (enemy, next 2 rounds); both attacks +1 (41 EP).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT |
|---|---|---:|---:|---:|
| Blade That Never Cools (Burst) | Heat in the Steel, Searing Edge, Blade That Never Cools, Blistered Guard | +5 | +2% | +2% |
| White-Hot Blood (Heat) | Heat in the Steel, Fever Pitch, White-Hot Blood, Blistered Guard | — | +10% | +2% |
| Nothing Left Forbidden (Exposure) | Heat in the Steel, Blistered Guard, Heat Finds the Seam, Nothing Left Forbidden | +1 | +2% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Blade That Never Cools:** +5 Damage on both hits (Forgotten Ember Blade and Forbidden Chakra Fury 40 → 45 EP at jutsu level 25; the bloodline's Bukijutsu IDG passive multiplies the hit, and kit heat and exposure from an earlier round raise it further) with Heat in the Steel's 32% heat. Blistered Guard is the fourth purchase (exposure 32%); Fever Pitch (heat 35%) is the all-self alternative. No uptime dependency: the Damage is on every cast.
- **White-Hot Blood:** +10% on Forgotten Ember Blade's self heat (30 → 40% for the 2 rounds after each cast, 6-round cooldown): it raises every element-less non-pierce hit the caster lands in that window (Chakra Fury, weapon and basic attacks, element-less normal jutsu), never Ember Blade's own hit, beside the multiplicative Bukijutsu IDG passive. Blistered Guard adds the 32% exposure; Searing Edge (attacks 42 EP) is the alternative.
- **Nothing Left Forbidden:** +10% on Forbidden Chakra Fury's exposure (30 → 40% on the target for the 2 rounds after the cast, 7-round cooldown): every non-pierce hit the target takes in that window, from the caster's Ember Blade, weapons, normal jutsu or allies, gains it; Chakra Fury's own hit does not. Both attacks reach 41 EP and Ember Blade's heat 32%. Heat in the Steel is the only fourth purchase (the accepted universal opener, see narrow_kit_exception); the build suits team fights.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Heat | Exposure |
|---|---:|---|---|---:|---:|---:|---:|
| Forgotten Ember Blade | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 41 (+1) |
| Forgotten Ember Blade | 1 | Increase Damage Given | self | 30% | 32% (+2) | 40% (+10) | 32% (+2) |
| Forbidden Chakra Fury | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 41 (+1) |
| Forbidden Chakra Fury | 1 | Increase Damage Taken | enemy | 30% | 32% (+2) | 32% (+2) | 40% (+10) |
| Chakra Shield | 0 | absorb (unsupported) | self | 30% | 30% | 30% | 30% |
| Chakra Shield | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +10% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Blade That Never Cools: +5 Damage (0 + 2 + 3; on band)
  - Route White-Hot Blood: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route Nothing Left Forbidden: +10% Increase Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 4 (DMG 2, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Heat in the Steel, Searing Edge, Blade That Never Cools, Fever Pitch (raw +10, row-weighted 15)
- Lowest row-weighted node: Heat in the Steel (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Heat in the Steel) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Heat in the Steel, Searing Edge, Blade That Never Cools, Fever Pitch | +5 Damage, +5% IDG |
| 2 | Heat in the Steel, Searing Edge, Blade That Never Cools, Blistered Guard | +5 Damage, +2% IDG, +2% IDT |
| 3 | Heat in the Steel, Searing Edge, Fever Pitch, White-Hot Blood | +2 Damage, +10% IDG |
| 4 | Heat in the Steel, Searing Edge, Fever Pitch, Blistered Guard | +2 Damage, +5% IDG, +2% IDT |
| 5 | Heat in the Steel, Searing Edge, Blistered Guard, Heat Finds the Seam | +2 Damage, +2% IDG, +5% IDT |
| 6 | Heat in the Steel, Fever Pitch, White-Hot Blood, Blistered Guard | +10% IDG, +2% IDT |
| 7 | Heat in the Steel, Fever Pitch, Blistered Guard, Heat Finds the Seam | +5% IDG, +5% IDT |
| 8 | Heat in the Steel, Blistered Guard, Heat Finds the Seam, Nothing Left Forbidden | +1 Damage, +2% IDG, +10% IDT |

## Design notes

- Node split: 2 Foundations, 3 Hidden Arts, 3 Advanced Arts, each Advanced Art 3 BP deep, so any two cost 5+. Heat in the Steel (IDG +2%) forks into Searing Edge → Blade That Never Cools (Damage +2/+3) and Fever Pitch → White-Hot Blood (IDG +3%/+5%); Blistered Guard → Heat Finds the Seam → Nothing Left Forbidden (IDT +2%/+3%/+5%, capstone Damage +1) is one chain.
- Routes: Burst +5 Damage (40 → 45 EP; Crown of Cinders/Solar Cataclysm flats); Heat +10% Increase Damage Given and Exposure +10% Increase Damage Taken, both in Taiyo Kami's 2/3/5 shape on one row each. Recalibration: Heat in the Steel's former +1 Damage is removed so no legal allocation exceeds +5 Damage, and the exposure route rises from +8% to +10%. Maxima over all legal allocations: Damage +5, IDG +10%, IDT +10%.
- Both Foundations are single-tag (+2% on one row) because a second tag on either would breach a ceiling: Damage on either root would put the Burst route plus that root above +5; Increase Damage Taken on Heat in the Steel would put 01,06,07,08 at +12%; Increase Damage Given on Blistered Guard would put 01,04,05,06 at +12%. Burst and Heat examples take Blistered Guard fourth; Fever Pitch and Searing Edge are the named alternatives.
- Interactions (§3, §3b): Ember Blade's heat row is Bukijutsu-filtered but element-less, so the filter is not binding: it matches every element-less hit of any stat type plus Bukijutsu elemental hits. Chakra Fury's exposure lists four stat types, no element: every non-pierce hit. Neither touches pierce; the Bukijutsu IDG passive (22 + 0.15/level, fromType bloodline) is applied separately. Same-tag effects all apply (process.ts 1109–1117).
- Timing (§3b, §4b): both attacks are OTHER_USER single-target, range 4, 60 AP, cooldowns 6 and 7. Heat is SELF, realized on the caster at cast; exposure lands on the struck target. Neither acts in its cast round; each is live the 2 rounds after, so the second attack of a back-to-back pair (either order) gets the first one's window. The next round holds both windows, but both attacks are on cooldown, so only weapons, basic attacks, other jutsu and allies use it. The Damage route needs no window.
- Allocations: 8 legal full builds, all non-dominated, 3 with no Advanced Art (01,02,04,06 attacks 42 EP/heat 35%/exposure 32%; 01,02,06,07 42 EP/32%/35%; 01,04,06,07 40 EP/35%/35%). Fourth purchases: Burst → Blistered Guard or Fever Pitch; Heat → Blistered Guard or Searing Edge; Exposure → Heat in the Steel. Open layout option: a +2 Damage leaf under Blistered Guard ends the universal opener (adds 06,07,08,09: Damage +3, IDT +10%; maxima unchanged).

## Risks and unproven interactions

- Classification: no kit row carries an element, so the tree requires a classification extension. 'Yaketsuku Netsu' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Heat breadth: White-Hot Blood puts Ember Blade's self IDG at 40% for the 2 rounds after each cast on every element-less non-pierce hit, beside the multiplicative Bukijutsu IDG passive (22 + 0.15/level) and alongside main-tree or gear IDG. One row carries the whole +10% route.
- Exposure breadth: Nothing Left Forbidden puts Chakra Fury's Increase Damage Taken at 40% for the 2 rounds after the cast; four stat types, no element, so every non-pierce hit from allies, weapons and normal jutsu gains it, and two Yaketsuku Netsu casters' exposures on one target both apply. Value scales with ally output; not simulated.
- Universal opener (accepted, visible to the user): Heat in the Steel is in all 8 legal full builds (6 of 8 also hold Blistered Guard), against brief §1's aim of no mandatory opener. It is a layout choice, not a four-row impossibility: a +2 Damage leaf under Blistered Guard would remove it at the cost of a Searing Edge twin. The enumerated leaf shapes are in narrow_kit_exception.
- Damage is formula-calculated (sqrt stat scaling: Ember Blade on Bukijutsu / Speed, Strength; Chakra Fury on Highest), then multiplied by the Bukijutsu IDG passive and raised by heat or exposure from an earlier round, so +5 EP is not a linear +5 damage; realized value depends on stats. No combat simulation.
- Unsupported rows and modes: Chakra Shield's absorb 30% and shield 100 receive nothing, so the tree cannot serve the kit's defence; the 5% reflect passive and the Ninjutsu-filtered Increase Damage Taken passive on the bearer are not jutsu rows. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin.
- Targeting and uptime: each attack needs a living non-caster user in range 4. Ember Blade aimed at an ally withholds its ENEMIES-only damage row but still realizes the SELF heat on the caster; Chakra Fury on an ally lands its damage and exposure (friendly fire none). Heat and exposure are 2-round windows per 6- and 7-round cooldowns. Realization when the hit misses or is prevented was not verified.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Yaketsuku Netsu-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

