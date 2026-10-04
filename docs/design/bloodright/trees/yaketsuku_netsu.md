# Yaketsuku Netsu — Scorch and Steel

**Bloodline:** Yaketsuku Netsu (BR-092, rank B, `clh4d6qfn000etb0hydj4cdpl`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Yaketsuku Netsu classification / forked tree · **Classification:** Yaketsuku Netsu (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Increase Damage Given — Forgotten Ember Blade's self heat window (the Sustained DPS identity; the bloodline passive is also a Bukijutsu Increase Damage Given) · secondary Increase Damage Taken — Forbidden Chakra Fury's exposure, which every attacker's non-pierce hits use · tertiary Damage — a controlled +3 on both attacks (40 → 43 EP, still Normal): a +1 commit on Searing Edge and a +2 payoff on Blade That Never Cools.

The kit's four supported rows sit on two 60 AP, range-4 single-target attacks. Forgotten Ember Blade (cooldown 6) deals 40 EP and gives the caster 30% Increase Damage Given for the 2 rounds after the cast; Forbidden Chakra Fury (cooldown 7) deals 40 EP and leaves the target with 30% Increase Damage Taken for the 2 rounds after the cast. Each attack's window feeds the other attack and every other hit landed in it. Heat in the Steel answers how the caster's own strikes land harder: Blade That Never Cools strikes harder on every cast (route +3 Damage, no window to wait for), White-Hot Blood runs the heat to 40%. Blistered Guard opens the target for every attacker: Nothing Left Forbidden takes the exposure to 40%. Flat Damage stops at +3 (40 → 43): both Damage rows are the kit's only hits and +5 would lift both from Normal (40) to High (45), while the capstone's +2 has to outweigh the +1 commit that White-Hot Blood can also buy as its fourth. Chakra Shield's absorb and shield are unsupported, so there is no defensive route. Potency reaches matching supported tags on all Yaketsuku Netsu-classified jutsu (RUL-2026-10-03-005; requires a classification extension).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Heat in the Steel | Foundation | How do I make my own strikes land harder: strike harder on every cast, or run my blade hotter? |
| Blistered Guard | Foundation | How do I open the target for everyone who hits it? |
| Blade That Never Cools | Advanced Art | burst: raw Damage on both attacks on every cast, either order, no window |
| White-Hot Blood | Advanced Art | sustained self amplification: the heat window lifts every hit I land on any target |
| Nothing Left Forbidden | Advanced Art | team exposure: the opened target takes more from every attacker |

**Director review recommended:** Nothing Left Forbidden keeps single-row team exposure at +10% (Chakra Fury 30 → 40%, every attacker's non-pierce hits), above the director templates' ~+5% exposure and on the same 2/3/5 ladder as White-Hot Blood's self heat. Kept deliberately: solo the two mirror on the Fury's target, but heat reaches every target and recurs every 6 rounds against exposure's 7, while exposure adds ×1.40 to every ally hit. It is the party route and moves with the roster-wide single-row exposure question; Nothing Left Forbidden +3% (route +8%, 38%) is the lever if the director wants it priced.

- Concern: Heat in the Steel stays in every legal full build (narrow-kit exception): every second leaf under Blistered Guard would twin an existing node on the same row.
- Concern: Searing Edge carries +1 flat Damage on a Hidden Art, against the roster's flat-Damage-on-Advanced convention (R6): the kit has three supported tags, so a heat or exposure setup twins Fever Pitch or Seams Laid Bare (the first pass's +3% exposure setup did). It also gives White-Hot Blood a real fourth choice (+1 EP or 32% exposure).
- Concern: Blade That Never Cools carries +2 (route +3, 40 → 43 on the kit's only two hits, no tier crossing), one over the roster's +2 default for Normal rows (R5). At +1 it copied Searing Edge, which White-Hot Blood also buys as its fourth: Burst + Fever Pitch (98.7 / 96.6 on a back-to-back pair, Blade first / Fury first) led Heat + Searing Edge (98.4 / 94.3) by 0.3% when the Blade led and the capstone was worth about one Hidden Art (the capstone-less 01, 02, 04, 06 totals 96.4 / 95.1). At +2 Burst gives ≈ 101.1 / 98.9 while Heat keeps ×1.40 against ×1.35 on every other own hit in the heat window. A director who prefers the default would set Blade That Never Cools to +1 (40 → 42). Not simulated.
- Concern: White-Hot Blood and Nothing Left Forbidden are bare single-row +10% capstones with no rider: the kit has no rider tag that is not a sibling route's primary.
- Concern: Every amplified row depends on the proposed Yaketsuku Netsu classification extension and the jutsu-classification resolver (G1); none carries an element today.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four: the kit has three supported tags on four rows (Damage on both attacks, one self Increase Damage Given row on Forgotten Ember Blade, one enemy Increase Damage Taken row on Forbidden Chakra Fury); Chakra Shield's absorb and shield are not potency targets, so no sustain or defensive identity exists for a fourth route. Universal opener accepted: Heat in the Steel is in all 8 legal full builds because Blistered Guard has one child. Every second leaf under Blistered Guard would twin an existing node on the same row: an Increase Damage Given leaf twins Heat in the Steel (and only replaces it as the Exposure route's fourth), a Damage leaf twins Searing Edge, and an Increase Damage Taken leaf twins Seams Laid Bare and lifts the exposure maximum above +10%.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yaketsuku Netsu-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Heat in the Steel | Foundation | None | +2% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 02 | Searing Edge | Hidden Art | Heat in the Steel | +1 Damage (damage) | Forbidden Chakra Fury, Forgotten Ember Blade / 2 |
| 03 | Blade That Never Cools | Advanced Art | Searing Edge | +2 Damage (damage) | Forbidden Chakra Fury, Forgotten Ember Blade / 2 |
| 04 | Fever Pitch | Hidden Art | Heat in the Steel | +3% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 05 | White-Hot Blood | Advanced Art | Fever Pitch | +5% Increase Damage Given (self buff) | Forgotten Ember Blade / 1 |
| 06 | Blistered Guard | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 07 | Seams Laid Bare | Hidden Art | Blistered Guard | +3% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |
| 08 | Nothing Left Forbidden | Advanced Art | Seams Laid Bare | +5% Increase Damage Taken (enemy debuff) | Forbidden Chakra Fury / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Heat in the Steel** — The forgotten ember never went out. It waited in the steel for a hand to wake it. Forgotten Ember Blade self heat 30 → 32% Increase Damage Given for the 2 rounds after the cast, on every element-less non-pierce hit the caster lands.
- **Searing Edge** — Where the edge passes, the air itself blisters. Commit: both attacks 40 → 41 EP (×1.025 per hit) on every cast. A heat or exposure setup here would twin Fever Pitch or Seams Laid Bare on the same single row.
- **Blade That Never Cools** — Quench it in blood, quench it in rain; the heat only climbs. Payoff: +2 here, route total +3 Damage, both attacks 40 → 43 EP (×1.075 per hit, still Normal tier) on every cast, in either order, with no window to wait for.
- **Fever Pitch** — Every swing feeds the heat, and the heat feeds the next swing. Ember Blade heat 32 → 35% with Heat in the Steel (self, the 2 rounds after casting); element-less hits of any stat.
- **White-Hot Blood** — Past red, past fear, the blood runs white and nothing it touches survives. Route total +10%: Ember Blade heat 30 → 40% for the 2 rounds after each cast, on every element-less non-pierce hit the caster lands (never the Blade's own hit).
- **Blistered Guard** — Fury leaves the skin raw, and raw skin remembers every blow that follows. Chakra Fury exposure 30 → 32% Increase Damage Taken (enemy, the 2 rounds after the cast); four stat types, element-less: every non-pierce hit from any attacker.
- **Seams Laid Bare** — Armor has seams. The Fury finds every one of them. Exposure 32 → 35% with Blistered Guard; allies', weapon and normal-jutsu hits all count.
- **Nothing Left Forbidden** — The seal is gone. What was held back is held back no more. Route total +10%: Chakra Fury exposure 30 → 40% on the target for the 2 rounds after the cast, on every attacker's non-pierce hits (never the Fury's own hit).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT |
|---|---|---:|---:|---:|
| Blade That Never Cools (Burst) | Heat in the Steel, Searing Edge, Blade That Never Cools, Fever Pitch | +3 | +5% | — |
| White-Hot Blood (Heat) | Heat in the Steel, Searing Edge, Fever Pitch, White-Hot Blood | +1 | +10% | — |
| Nothing Left Forbidden (Exposure) | Heat in the Steel, Blistered Guard, Seams Laid Bare, Nothing Left Forbidden | — | +2% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Blade That Never Cools:** Raw Damage on every cast: both attacks 40 → 43 EP (×1.075) whatever the order, with Fever Pitch fourth for 35% heat. Blade then Fury lands the Fury at 43 × 1.35 ≈ 58.1; Fury then Blade lands the Blade at 43 × 1.30 = 55.9; the opening strike of each pair stays at 43. Blistered Guard is the order-free alternative fourth (heat and exposure 32%: 43 × 1.32 ≈ 56.8 either way).
- **White-Hot Blood:** Sustained self amplification: Ember Blade heat 30 → 40% for the 2 rounds after each cast on every element-less non-pierce hit the caster lands on any target (Chakra Fury, weapons, basic attacks, element-less normal jutsu), beside the Bukijutsu Increase Damage Given passive. Searing Edge fourth adds +1 EP to both attacks (Fury after Blade 41 × 1.40 = 57.4); Blistered Guard instead gives 32% exposure (×1.40 × 1.32 ≈ ×1.85 on a hit in both windows). The route itself adds no Damage.
- **Nothing Left Forbidden:** Team exposure: Chakra Fury exposure 30 → 40% on the target for the 2 rounds after the cast; every non-pierce hit it takes from any attacker gains ×1.40 (Blade after Fury 40 × 1.40 = 56.0), and the caster's own hit in both windows ×1.32 × 1.40 ≈ ×1.85. Heat in the Steel is the only fourth purchase (heat 32%). No flat Damage; the route's value grows with the party.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Heat | Exposure |
|---|---:|---|---|---:|---:|---:|---:|
| Forgotten Ember Blade | 0 | Damage | enemy | 40 | 43 (+3) | 41 (+1) | 40 |
| Forgotten Ember Blade | 1 | Increase Damage Given | self | 30% | 35% (+5) | 40% (+10) | 32% (+2) |
| Forbidden Chakra Fury | 0 | Damage | enemy | 40 | 43 (+3) | 41 (+1) | 40 |
| Forbidden Chakra Fury | 1 | Increase Damage Taken | enemy | 30% | 30% | 30% | 40% (+10) |
| Chakra Shield | 0 | absorb (unsupported) | self | 30% | 30% | 30% | 30% |
| Chakra Shield | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +3 Damage, +10% Increase Damage Given, +10% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Blade That Never Cools: +3 Damage (0 + 1 + 2; off band)
  - Route White-Hot Blood: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route Nothing Left Forbidden: +10% Increase Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 4 (DMG 2, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Heat in the Steel, Fever Pitch, White-Hot Blood, Blistered Guard (raw +12, row-weighted 12)
- Lowest row-weighted node: Heat in the Steel (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Heat in the Steel) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +1 Damage | +3 Damage |
|---|---:|---|---|---|
| Forgotten Ember Blade | 0 | 40 (Normal) | 41 (Normal) | 43 (Normal) |
| Forbidden Chakra Fury | 0 | 40 (Normal) | 41 (Normal) | 43 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Blade That Never Cools | +3 Damage, +2% IDG | Fever Pitch *(highest diagnostic)* | +3 Damage, +5% IDG | 11 |
| Blade That Never Cools | +3 Damage, +2% IDG | Blistered Guard | +3 Damage, +2% IDG, +2% IDT | 10 |
| White-Hot Blood | +10% IDG | Searing Edge | +1 Damage, +10% IDG | 12 |
| White-Hot Blood | +10% IDG | Blistered Guard *(highest diagnostic)* | +10% IDG, +2% IDT | 12 |
| Nothing Left Forbidden | +10% IDT | Heat in the Steel *(highest diagnostic)* | +2% IDG, +10% IDT | 12 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Heat in the Steel, Searing Edge, Blade That Never Cools, Fever Pitch | +3 Damage, +5% IDG |
| 2 | Heat in the Steel, Searing Edge, Blade That Never Cools, Blistered Guard | +3 Damage, +2% IDG, +2% IDT |
| 3 | Heat in the Steel, Searing Edge, Fever Pitch, White-Hot Blood | +1 Damage, +10% IDG |
| 4 | Heat in the Steel, Searing Edge, Fever Pitch, Blistered Guard | +1 Damage, +5% IDG, +2% IDT |
| 5 | Heat in the Steel, Searing Edge, Blistered Guard, Seams Laid Bare | +1 Damage, +2% IDG, +5% IDT |
| 6 | Heat in the Steel, Fever Pitch, White-Hot Blood, Blistered Guard | +10% IDG, +2% IDT |
| 7 | Heat in the Steel, Fever Pitch, Blistered Guard, Seams Laid Bare | +5% IDG, +5% IDT |
| 8 | Heat in the Steel, Blistered Guard, Seams Laid Bare, Nothing Left Forbidden | +2% IDG, +10% IDT |

## Design notes

- Structure kept: Heat in the Steel (+2% IDG) forks into Searing Edge → Blade That Never Cools (Damage +1/+2) and Fever Pitch → White-Hot Blood (IDG +3%/+5%); Blistered Guard → Seams Laid Bare → Nothing Left Forbidden (IDT +2%/+3%/+5%) is one chain. Each Advanced Art is 3 BP deep, so any two cost 5+. Maxima over all legal allocations: Damage +3, IDG +10%, IDT +10%.
- Rebalance (2026-10-04): the pre-batch +5 Damage Burst route (Searing Edge +2, Blade That Never Cools +3) lifted both attacks 40 → 45, a full tier on the kit's only two hits; Nothing Left Forbidden's +1 Damage rider is dropped so Damage belongs to one route. The first pass made Searing Edge a +3% exposure setup (the Blood-Enchanted Eyes pattern), which twinned Seams Laid Bare on Chakra Fury's single exposure row under the other Foundation. The roster pass makes Searing Edge a +1 Damage commit (with three supported tags, any heat or exposure setup twins Fever Pitch or Seams Laid Bare). The final review raised Blade That Never Cools from +1 to +2 (route +3, 40 → 43, still Normal; the Tenohira Musei and Hyouga Yui +1/+2 shape): at +1 the capstone copied Searing Edge, White-Hot Blood's natural fourth, so Burst led Heat only on a Blade-first pair (98.7 against 98.4).
- Damage and kit hits: formula damage is linear in EP (tags.ts powerEffect: baseline × power / 40 × stat advantage), so +1 EP is ×1.025 and +3 EP ×1.075 on each 40 EP hit whatever the stats. A kit attack never lands in its own window (a row never acts in its cast round; the 6 and 7 cooldowns outlast the 2-round windows), so each gets at most the other's window. Fury after Blade: Burst with Fever Pitch 43 × 1.35 ≈ 58.1, Heat with Searing Edge 41 × 1.40 = 57.4 (40 × 1.40 = 56.0 with Blistered Guard), Exposure 40 × 1.32 = 52.8. Blade after Fury: Burst 43 × 1.30 = 55.9, Heat 41 × 1.30 = 53.3 (40 × 1.32 = 52.8), Exposure 40 × 1.40 = 56.0. With the unwindowed opening strike, a back-to-back pair totals Burst ≈ 101.1 / 98.9 (Blade first / Fury first; ≈ 99.8 either way with Blistered Guard), Heat 98.4 / 94.3 (96.0 / 92.8 with Blistered Guard), Exposure 92.8 / 96.0.
- Other hits in the windows (weapons, basic attacks, element-less normal jutsu): heat-window hits on any target take Heat ×1.40, Burst ×1.35 or ×1.32, Exposure ×1.32; a hit in both windows takes Heat ×1.40 × 1.32 ≈ ×1.85 (×1.82 with Searing Edge), Exposure ×1.32 × 1.40 ≈ ×1.85, Burst ×1.35 × 1.30 ≈ ×1.76 (×1.74 with Blistered Guard); unmodified kit ×1.69. Ally hits on the Fury's target take ×1.40 under Exposure, ×1.30–×1.32 otherwise. So Burst leads a back-to-back pair of the kit's attacks in either order (by about 2.7% / 4.9% over Heat, 3.0% over Exposure when the Fury leads), Heat leads every other own hit on every target by about 3.7% (×1.40 against ×1.35; its 6-round cooldown also beats exposure's 7), Exposure the party's hits.
- Fourth purchases: Burst → Fever Pitch (heat 35%) or Blistered Guard (heat and exposure 32%); Heat → Searing Edge (+1 EP on both attacks) or Blistered Guard (exposure 32%), a real choice between strike and party value; Exposure → Heat in the Steel only. No fourth stacks a route's own primary tag; Searing Edge for Heat is the only fourth that adds Damage (+1).
- Timing (§3b, §4b): both attacks are OTHER_USER single-target, range 4, 60 AP, cooldowns 6 and 7. Heat is realized on the caster at cast; exposure lands on the struck target. Neither acts in its cast round; each is live the 2 rounds after, so the second attack of a back-to-back pair gets the first one's window, and the round after holds both windows for the caster's weapons, basic attacks and other jutsu. Allies get only the exposure window.
- Interactions (§3): Ember Blade's heat row is Bukijutsu-filtered but element-less, so the filter is not binding: it matches every element-less hit of any stat type plus Bukijutsu elemental hits. Chakra Fury's exposure lists four stat types and no element: every non-pierce hit. Neither touches pierce; the Bukijutsu IDG passive (22 + 0.15/level, fromType bloodline) multiplies last.

## Risks and unproven interactions

- Classification: no kit row carries an element, so the tree requires a classification extension. 'Yaketsuku Netsu' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Exposure leverage: Nothing Left Forbidden's 40% applies to every non-pierce hit the target takes for 2 rounds from any attacker, so its value scales with party size; two Yaketsuku Netsu casters' exposures on one target both apply. Not simulated.
- Heat breadth: White-Hot Blood's 40% applies to every element-less non-pierce hit the caster lands in the window, beside the Bukijutsu IDG passive and any main-tree or gear IDG. One row carries the whole +10% route; the kit has no rider tag that is not a sibling route's primary.
- Damage: +3 EP is exactly ×1.075 on each kit hit (formula damage is linear in EP); the stat-advantage term and the bloodline passive scale the absolute value, not that ratio. The kit-hit figures in the design notes are EP × window only. No combat simulation.
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

