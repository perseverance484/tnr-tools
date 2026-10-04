# Yaketsuku Netsu — Scorch and Steel

**Bloodline:** Yaketsuku Netsu (BR-092, rank B, `clh4d6qfn000etb0hydj4cdpl`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Yaketsuku Netsu classification / forked tree · **Classification:** Yaketsuku Netsu (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Increase Damage Given — Forgotten Ember Blade's self heat window (the Sustained DPS identity; the bloodline passive is also a Bukijutsu Increase Damage Given) · secondary Increase Damage Taken — Forbidden Chakra Fury's exposure, which every attacker's non-pierce hits use · tertiary Damage — a controlled +2 payoff on both attacks (40 → 42 EP), set up by exposure.

The kit's four supported rows sit on two 60 AP, range-4 single-target attacks. Forgotten Ember Blade (cooldown 6) deals 40 EP and gives the caster 30% Increase Damage Given for the 2 rounds after the cast; Forbidden Chakra Fury (cooldown 7) deals 40 EP and leaves the target with 30% Increase Damage Taken for the 2 rounds after the cast. Each attack's window feeds the other attack and every other hit landed in it, so the tree is built on the two windows. Heat in the Steel answers how the caster's own strikes land harder: White-Hot Blood runs the heat to 40%, and Blade That Never Cools sets up 33% exposure and pays off with +2 Damage. Blistered Guard opens the target for every attacker: Nothing Left Forbidden takes the exposure to 40%. Flat Damage stays at +2 because both Damage rows are the kit's only hits and +5 would lift both from Normal (40) to High (45). Chakra Shield's absorb and shield are unsupported, so there is no defensive route. Potency reaches matching supported tags on all Yaketsuku Netsu-classified jutsu (RUL-2026-10-03-005; requires a classification extension).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Heat in the Steel | Foundation | How do I make my own strikes land harder: open the target for my blade, or run my blade hotter? |
| Blistered Guard | Foundation | How do I open the target for everyone who hits it? |
| Blade That Never Cools | Advanced Art | burst: exposure set up, controlled raw-Damage payoff on both attacks |
| White-Hot Blood | Advanced Art | sustained self amplification: the heat window lifts every hit I land |
| Nothing Left Forbidden | Advanced Art | team exposure: the opened target takes more from every attacker |

- Concern: Heat in the Steel stays in every legal full build (narrow-kit exception carried forward): the kit has no fourth tag for a leaf under Blistered Guard that would not blur or twin a route.
- Concern: Exposure leverage: on a hit landed in both windows the three full packages sit within ×1.80–×1.86, but Nothing Left Forbidden also lifts every ally hit on the target by ×1.40, so it is the strongest route in a party. Party value was not simulated.
- Concern: The Heat route's best fourth is its sibling Searing Edge (exposure 33%), one point over Blistered Guard (32%), so Heat + Blistered Guard is numerically dominated. Accepted to keep the 2/3/5 exposure chain unchanged.
- Concern: Every amplified row depends on the proposed Yaketsuku Netsu classification extension and the jutsu-classification resolver (G1); none carries an element today.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four: the kit has three supported tags on four rows (Damage on both attacks, one self Increase Damage Given row on Forgotten Ember Blade, one enemy Increase Damage Taken row on Forbidden Chakra Fury); Chakra Shield's absorb and shield are not potency targets, so no sustain or defensive identity exists for a fourth route. Universal opener accepted: Heat in the Steel is in all 8 legal full builds because Blistered Guard has one child. A leaf Hidden Art under Blistered Guard would only blur or twin a route: an Increase Damage Taken leaf lifts the exposure maximum above +10%, a Damage leaf hands the Exposure route the Burst payoff, and an Increase Damage Given leaf merely replaces Heat in the Steel as the Exposure route's fourth.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yaketsuku Netsu-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Heat in the Steel | Foundation | None | +2% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 02 | Searing Edge | Hidden Art | Heat in the Steel | +3% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 03 | Blade That Never Cools | Advanced Art | Searing Edge | +2 Damage (damage) | Forbidden Chakra Fury, Forgotten Ember Blade / 2 |
| 04 | Fever Pitch | Hidden Art | Heat in the Steel | +3% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 05 | White-Hot Blood | Advanced Art | Fever Pitch | +5% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 06 | Blistered Guard | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 07 | Heat Finds the Seam | Hidden Art | Blistered Guard | +3% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 08 | Nothing Left Forbidden | Advanced Art | Heat Finds the Seam | +5% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Heat in the Steel** — The forgotten ember never went out. It waited in the steel for a hand to wake it. Forgotten Ember Blade self heat 30 → 32% Increase Damage Given for the 2 rounds after the cast, on every element-less non-pierce hit the caster lands.
- **Searing Edge** — The Fury sears the guard away; the edge only has to follow. Setup: Forbidden Chakra Fury exposure 30 → 33% Increase Damage Taken (enemy, the 2 rounds after the cast), so an Ember Blade that follows lands into it.
- **Blade That Never Cools** — Quench it in blood, quench it in rain; the heat only climbs. Payoff: both attacks 40 → 42 EP on every cast (still Normal tier, the kit's only hits); with Searing Edge, the Blade that follows a Fury lands into 33% exposure.
- **Fever Pitch** — Every swing feeds the heat, and the heat feeds the next swing. Ember Blade heat 32 → 35% with Heat in the Steel (self, the 2 rounds after casting); element-less hits of any stat.
- **White-Hot Blood** — Past red, past fear, the blood runs white and nothing it touches survives. Route total +10%: Ember Blade heat 30 → 40% for the 2 rounds after each cast, on every element-less non-pierce hit the caster lands (never the Blade's own hit).
- **Blistered Guard** — Fury leaves the skin raw, and raw skin remembers every blow that follows. Chakra Fury exposure 30 → 32% Increase Damage Taken (enemy, the 2 rounds after the cast); four stat types, element-less: every non-pierce hit from any attacker.
- **Heat Finds the Seam** — Armor has seams. Heat finds every one of them. Exposure 32 → 35% with Blistered Guard; allies', weapon and normal-jutsu hits all count.
- **Nothing Left Forbidden** — The seal is gone. What was held back is held back no more. Route total +10%: Chakra Fury exposure 30 → 40% on the target for the 2 rounds after the cast, on every attacker's non-pierce hits (never the Fury's own hit).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT |
|---|---|---:|---:|---:|
| Blade That Never Cools (Burst) | Heat in the Steel, Searing Edge, Blade That Never Cools, Fever Pitch | +2 | +5% | +3% |
| White-Hot Blood (Heat) | Heat in the Steel, Searing Edge, Fever Pitch, White-Hot Blood | — | +10% | +3% |
| Nothing Left Forbidden (Exposure) | Heat in the Steel, Blistered Guard, Heat Finds the Seam, Nothing Left Forbidden | — | +2% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Blade That Never Cools:** Exposure into a narrow burst: both attacks 40 → 42 EP, Chakra Fury exposure 33% and, with Fever Pitch fourth, Ember Blade heat 35%. Fury then Blade lands the Blade into ×1.33; Blade then Fury lands the Fury into ×1.35; a hit in both windows takes ×1.35 × 1.33 ≈ ×1.80. Blistered Guard is the alternative fourth (exposure 35%, heat 32%).
- **White-Hot Blood:** Sustained self amplification: Ember Blade heat 30 → 40% for the 2 rounds after each cast on every element-less non-pierce hit the caster lands (Chakra Fury, weapons, basic attacks, element-less normal jutsu), beside the Bukijutsu Increase Damage Given passive. Searing Edge is the fourth purchase (exposure 33%; ×1.40 × 1.33 ≈ ×1.86 on a hit in both windows); Blistered Guard gives 32%. No flat Damage.
- **Nothing Left Forbidden:** Team exposure: Chakra Fury exposure 30 → 40% on the target for the 2 rounds after the cast; every non-pierce hit it takes from any attacker gains ×1.40, and the caster's own hit in both windows ×1.32 × 1.40 ≈ ×1.85. Heat in the Steel is the only fourth purchase (heat 32%). No flat Damage; the route's value grows with the party.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Heat | Exposure |
|---|---:|---|---|---:|---:|---:|---:|
| Forgotten Ember Blade | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Forgotten Ember Blade | 1 | Increase Damage Given | self | 30% | 35% (+5) | 40% (+10) | 32% (+2) |
| Forbidden Chakra Fury | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Forbidden Chakra Fury | 1 | Increase Damage Taken | enemy | 30% | 33% (+3) | 33% (+3) | 40% (+10) |
| Chakra Shield | 0 | absorb (unsupported) | self | 30% | 30% | 30% | 30% |
| Chakra Shield | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 6; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Increase Damage Given, +10% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Blade That Never Cools: +2 Damage (0 + 0 + 2; off band)
  - Route White-Hot Blood: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route Nothing Left Forbidden: +10% Increase Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 4 (DMG 2, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Heat in the Steel, Searing Edge, Fever Pitch, White-Hot Blood (raw +13, row-weighted 13)
- Lowest row-weighted node: Heat in the Steel (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Heat in the Steel) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Forgotten Ember Blade | 0 | 40 (Normal) | 42 (Normal) |
| Forbidden Chakra Fury | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Blade That Never Cools | +2 Damage, +2% IDG, +3% IDT | Fever Pitch *(highest diagnostic)* | +2 Damage, +5% IDG, +3% IDT | 12 |
| Blade That Never Cools | +2 Damage, +2% IDG, +3% IDT | Blistered Guard | +2 Damage, +2% IDG, +5% IDT | 11 |
| White-Hot Blood | +10% IDG | Searing Edge *(highest diagnostic)* | +10% IDG, +3% IDT | 13 |
| White-Hot Blood | +10% IDG | Blistered Guard | +10% IDG, +2% IDT | 12 |
| Nothing Left Forbidden | +10% IDT | Heat in the Steel *(highest diagnostic)* | +2% IDG, +10% IDT | 12 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Heat in the Steel, Searing Edge, Blade That Never Cools, Fever Pitch | +2 Damage, +5% IDG, +3% IDT |
| 2 | Heat in the Steel, Searing Edge, Blade That Never Cools, Blistered Guard | +2 Damage, +2% IDG, +5% IDT |
| 3 | Heat in the Steel, Searing Edge, Fever Pitch, White-Hot Blood | +10% IDG, +3% IDT |
| 4 | Heat in the Steel, Searing Edge, Fever Pitch, Blistered Guard | +5% IDG, +5% IDT |
| 5 | Heat in the Steel, Searing Edge, Blistered Guard, Heat Finds the Seam | +2% IDG, +8% IDT |
| 6 | Heat in the Steel, Fever Pitch, White-Hot Blood, Blistered Guard | +10% IDG, +2% IDT |
| 7 | Heat in the Steel, Fever Pitch, Blistered Guard, Heat Finds the Seam | +5% IDG, +5% IDT |
| 8 | Heat in the Steel, Blistered Guard, Heat Finds the Seam, Nothing Left Forbidden | +2% IDG, +10% IDT |

## Design notes

- Structure kept: Heat in the Steel (+2% IDG) forks into Searing Edge → Blade That Never Cools (+3% IDT setup, +2 Damage payoff) and Fever Pitch → White-Hot Blood (IDG +3%/+5%); Blistered Guard → Heat Finds the Seam → Nothing Left Forbidden (IDT +2%/+3%/+5%) is one chain. Each Advanced Art is 3 BP deep, so any two cost 5+.
- Rebalance (2026-10-04): the +5 Damage Burst route (Searing Edge +2, Blade That Never Cools +3) lifted both attacks 40 → 45, a full tier on the kit's only two hits. It is re-cut on the Blood-Enchanted Eyes pattern (RUL-2026-10-04-001): Searing Edge sets up +3% exposure and Blade That Never Cools pays off with +2 Damage (40 → 42). Nothing Left Forbidden's +1 Damage rider is dropped so Damage belongs to one route. Maxima over all legal allocations: Damage +2, IDG +10%, IDT +10%.
- Compounding (§3b): heat and exposure multiply on any hit landed in both windows. Full packages on such a hit: Burst ×1.35 × 1.33 ≈ ×1.80 with 42 EP attacks; Heat ×1.40 × 1.33 ≈ ×1.86; Exposure ×1.32 × 1.40 ≈ ×1.85, plus ×1.40 on every ally hit; unmodified kit ×1.30 × 1.30 = ×1.69.
- Fourth purchases: Burst → Fever Pitch (heat 35%) or Blistered Guard (exposure 35%); Heat → Searing Edge (exposure 33%, one point over Blistered Guard's 32%); Exposure → Heat in the Steel only. No fourth adds flat Damage or stacks a route's own primary tag.
- Timing (§3b, §4b): both attacks are OTHER_USER single-target, range 4, 60 AP, cooldowns 6 and 7. Heat is realized on the caster at cast; exposure lands on the struck target. Neither acts in its cast round; each is live the 2 rounds after, so the second attack of a back-to-back pair gets the first one's window, and the round after holds both windows for weapons, basic attacks, other jutsu and allies.
- Interactions (§3): Ember Blade's heat row is Bukijutsu-filtered but element-less, so the filter is not binding: it matches every element-less hit of any stat type plus Bukijutsu elemental hits. Chakra Fury's exposure lists four stat types and no element: every non-pierce hit. Neither touches pierce; the Bukijutsu IDG passive (22 + 0.15/level, fromType bloodline) multiplies last.

## Risks and unproven interactions

- Classification: no kit row carries an element, so the tree requires a classification extension. 'Yaketsuku Netsu' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Exposure leverage: Nothing Left Forbidden's 40% applies to every non-pierce hit the target takes for 2 rounds from any attacker, so its value scales with party size; two Yaketsuku Netsu casters' exposures on one target both apply. Not simulated.
- Heat breadth: White-Hot Blood's 40% applies to every element-less non-pierce hit the caster lands in the window, beside the Bukijutsu IDG passive and any main-tree or gear IDG. One row carries the whole +10% route; the kit has no rider tag that is not a sibling route's primary.
- Damage is formula-calculated (sqrt stat scaling: Ember Blade on Bukijutsu / Speed, Strength; Chakra Fury on Highest), so +2 EP is not a linear +2 damage; realized value depends on stats. No combat simulation.
- Unsupported rows and modes: Chakra Shield's absorb 30% and shield 100 receive nothing, so the tree cannot serve the kit's defence. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin.
- Targeting and uptime: each attack needs a living non-caster user in range 4. Ember Blade aimed at an ally withholds its ENEMIES-only damage row but still realizes the heat on the caster; Chakra Fury on an ally lands its damage and exposure (friendly fire none). Heat and exposure are 2-round windows per 6- and 7-round cooldowns. Realization when the hit misses or is prevented was not verified.

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

