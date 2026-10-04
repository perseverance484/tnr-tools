# Houkyuken — The Lodestone Fist

**Bloodline:** Houkyuken (BR-033, rank A, `ALoGrHuBY5Ml9bJG_DILe`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Magnet classification / forked tree · **Classification:** Magnet (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense from Lodestone Draw: Burst (Polarized Fist's self Increase Damage Given setup on Houkyuken: Magnetic Assignment and Houkyu Dance, paid off by Starfall Hammer's +2 Damage on all four Magnet strikes) or Exposure (Increase Damage Taken on Morning Star and Houkyuken: Magnetic Assignment) · secondary Defense from Repelling Field: Fortress (Decrease Damage Taken on Houkyuken: Magnetic Assignment) or Retaliation (Reflect on Rising Star) · tertiary Flat Damage only as Starfall Hammer's controlled +2 payoff, kept for the dossier's Burst trait: Magnetic Pulse Strike 50 → 52 (above the Nuke tier; director review), Houkyu Dance 45 → 47, Rising Star and Morning Star 40 → 42 EP.

Ten supported rows sit on five casts. The four Magnet Taijutsu Damage rows (Magnetic Pulse Strike 50, Houkyu Dance 45, Rising Star and Morning Star 40 EP) take only a controlled +2 at the end of the Burst route (the dossier Traits include Burst), after a percentage setup on the two 35% self Increase Damage Given rows: the Blood-Enchanted Eyes and Shakunetsu Sakura pattern (RUL-2026-10-04-001/002). Lodestone Draw answers "How do I make each blow land harder: strengthen my own fist, or drag the target onto it?" with Burst (+2 Damage on every own strike, window or not) and Exposure (every attacker's hits on the marked target). Repelling Field answers "How do I answer the blows aimed at me: blunt them, or throw them back?" with Fortress on the one universal Decrease Damage Taken row and Retaliation on the one Reflect row. Potency reaches matching supported tags on all Magnet jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Lodestone Draw | Foundation | How do I make each blow land harder: strengthen my own fist, or drag the target onto it? |
| Repelling Field | Foundation | How do I answer the blows aimed at me: blunt them, or throw them back? |
| Starfall Hammer | Advanced Art | burst: self-amplification setup, controlled +2 Damage payoff on every strike |
| Inexorable Pull | Advanced Art | exposure: mark one target for every attacker |
| Absolute Alignment | Advanced Art | fortress: the Magnetic Assignment window as armour |
| Violent Repulsion | Advanced Art | retaliation: every blow in the window costs the attacker |

**Director review recommended:** Roster questions: DQ-A (Starfall Hammer +2 Damage after the Polarized Fist setup, Magnetic Pulse Strike 50 → 52, kept for the dossier's Burst trait; see above_nuke_rationale); DQ-B (Inexorable Pull +8% Increase Damage Taken on two rows, 35 → 43%, ≈ ×1.122). Tree-specific: with Absolute Alignment's Increase Damage Given rider removed, Fortress + Lodestone Draw is still the strongest 1v1 allocation, outgoing/incoming ≈ 1.25 (from ≈ 1.29) against 1.17 to 1.19 for every offense-capstone build, a 5 to 7% lead (concerns).

- Concern: Inside a fully set-up single-target window Exposure + Polarized Fist (≈ ×3.95) still leads Burst + Reversed Polarity (×3.88 to ×3.92), and non-Magnet or allied hits favour Exposure further. Burst's niche is +2 Damage on every own strike regardless of window, across Houkyu Dance's area and through a debuff cleanse. Party size and window uptime were not simulated.
- Concern: Fortress + Lodestone Draw is still the strongest 1v1 allocation: ×1.06 own damage with ×0.846 incoming in each Magnetic Assignment window (outgoing/incoming ≈ 1.25 against 1.17 to 1.19 for the offense builds), a 5 to 7% lead, about the 6% Arashima's approved fortress holds on the same lens. Dropping Absolute Alignment's Increase Damage Given rider took it from ≈ 1.29. Stepping Decrease Damage Taken 2/3/3 (≈ 1.21) was not taken: Absolute Alignment would add no more than Magnetized Guard, and Fortress's 8% would sit next to Retaliation + Magnetized Guard's 7% plus +10% Reflect. It remains the director's lever if the lead should close further; the (1 − p) leverage, not a rider, now drives the gap.
- Concern: Exposure is +8% on two compounding team-wide rows, 35 → 43% (≈ ×1.122), just above Blood-Enchanted Eyes' ×1.115 exposure maximum and above Shakunetsu Sakura's ×1.075 (DQ-B). If the director wants exposure at or below the anchors, Houkyuken should move with the other two-row +8% exposure trees, not alone (+7%, 35 → 42%, is ≈ ×1.106).
- Concern: Retaliation keeps Reflect at +10% (50%) on one row; its value scales with the number of attackers in the window and was not simulated, and its Decrease Damage Taken rider trims what Reflect returns (design notes).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Magnet jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Lodestone Draw | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Houkyu Dance, Houkyuken: Magnetic Assignment, Morning Star / 4 |
| 02 | Polarized Fist | Hidden Art | Lodestone Draw | +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment / 2 |
| 03 | Starfall Hammer | Advanced Art | Polarized Fist | +2 Damage (damage) | Houkyu Dance, Magnetic Pulse Strike, Morning Star, Rising Star / 4 |
| 04 | Reversed Polarity | Hidden Art | Lodestone Draw | +2% Increase Damage Taken (enemy debuff) | Houkyuken: Magnetic Assignment, Morning Star / 2 |
| 05 | Inexorable Pull | Advanced Art | Reversed Polarity | +4% Increase Damage Taken (enemy debuff) | Houkyuken: Magnetic Assignment, Morning Star / 2 |
| 06 | Repelling Field | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |
| 07 | Magnetized Guard | Hidden Art | Repelling Field | +3% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment / 1 |
| 08 | Absolute Alignment | Advanced Art | Magnetized Guard | +5% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment / 1 |
| 09 | Like Poles Repel | Hidden Art | Repelling Field | +3% Reflect (self buff) | Rising Star / 1 |
| 10 | Violent Repulsion | Advanced Art | Like Poles Repel | +5% Reflect (self buff); +2% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Lodestone Draw** — Iron answers the fist before the blow lands; the enemy is already leaning in. Self Increase Damage Given 35 → 37% (Magnetic Assignment, Houkyu Dance) and enemy exposure 35 → 37% (Morning Star, Magnetic Assignment); each row is live the two rounds after its cast.
- **Polarized Fist** — Charge the knuckles with the field, and every blow that follows lands heavier. Setup: both self damage buffs 37 → 39% with Lodestone Draw (Magnetic Assignment, Houkyu Dance; ×1.39² ≈ ×1.93 on a hit both cover); Starfall Hammer pays it off.
- **Starfall Hammer** — A star does not fall by accident. It is pulled down. Burst payoff: +2 Damage on all four Magnet strikes, live on every cast: Magnetic Pulse Strike 50 → 52 (above the 50 Nuke tier; director review), Houkyu Dance 45 → 47, Rising Star and Morning Star 40 → 42 EP.
- **Reversed Polarity** — Flip the field and the body that fled now hurries toward the hammer. Both exposure rows 37 → 39% with Lodestone Draw: Morning Star (any stat type) and Magnetic Assignment (Lightning, Magnet, Wind and element-less hits).
- **Inexorable Pull** — Nothing with iron in its blood escapes the draw. Exposure: both enemy rows 35 → 43% on the full route (≈ ×1.122 over base where both apply, ×1.059 on one; Blood-Enchanted Eyes' exposure maximum is ×1.115), raising non-pierce hits on the target from every attacker, the party's included. Morning Star covers every such hit; Magnetic Assignment covers Lightning, Magnet, Wind and element-less hits.
- **Repelling Field** — Turn the pole outward and every blow meets an invisible hand. Magnetic Assignment Decrease Damage Taken 35 → 37% (every non-pierce hit, 40 AP); Rising Star Reflect 40 → 42% (includes pierce hits).
- **Magnetized Guard** — Filings align along the skin; the body becomes its own armour. Magnetic Assignment Decrease Damage Taken only: 40% with Repelling Field; one universal row, 2 rounds per 40 AP cast, cooldown 7.
- **Absolute Alignment** — Every particle set in order; what strikes you finds nothing out of place. Fortress: Magnetic Assignment Decrease Damage Taken 35 → 45% on the full route, so incoming is ×0.55 against ×0.65 at base (≈ ×0.846) for the two rounds after each 40 AP cast.
- **Like Poles Repel** — Bring like to like and the strike is thrown back on the one who threw it. Rising Star Reflect only: 45% with Repelling Field; one self row, 2 rounds per 60 AP single-target cast, under the 60% per-hit cap.
- **Violent Repulsion** — The closer the enemy presses, the harder the field hurls them away. Retaliation: Rising Star Reflect 40 → 50% on the full route (under the 60% per-hit cap); Magnetic Assignment Decrease Damage Taken 39% with Repelling Field (42% with Magnetized Guard), which also trims the post-mitigation damage Reflect returns.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | REF |
|---|---|---:|---:|---:|---:|---:|
| Starfall Hammer (Burst) | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +2 | +4% | +2% | +2% | +2% |
| Inexorable Pull (Exposure) | Lodestone Draw, Reversed Polarity, Inexorable Pull, Polarized Fist | — | +4% | +8% | — | — |
| Absolute Alignment (Fortress) | Repelling Field, Magnetized Guard, Absolute Alignment, Lodestone Draw | — | +2% | +2% | +10% | +2% |
| Violent Repulsion (Retaliation) | Repelling Field, Like Poles Repel, Violent Repulsion, Magnetized Guard | — | — | — | +7% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Starfall Hammer:** +2 Damage on all four Magnet strikes (Pulse Strike 52, Houkyu Dance 47, Rising Star and Morning Star 42 EP) on every cast, over both self damage buffs at 39% (×1.39² ≈ ×1.93 on a hit both cover, ×1.82 at base) and exposure 37% for the two rounds after their casts. Repelling Field is the fourth purchase (Magnetic Assignment Decrease Damage Taken 37%, Rising Star Reflect 42%); Reversed Polarity (exposure 39%) is the all-in alternative.
- **Inexorable Pull:** Both exposure rows 35 → 43% with both self buffs 39% from Polarized Fist as the fourth purchase: ×1.43² × 1.39² ≈ ×3.95 on a kit strike under all four rows (×3.32 at base: ×1.19, under Blood-Enchanted Eyes' ×1.234 top package), and the exposure half also raises allies' non-pierce hits on the target. This is the strongest in-window offense; Starfall Hammer with Reversed Polarity reaches ×1.39⁴ ≈ ×3.73 before its +2 Damage (×3.88 on Pulse Strike, ×3.92 on a 40 EP strike) but keeps the +2 outside the windows. Repelling Field is the defensive alternative.
- **Absolute Alignment:** Magnetic Assignment's universal Decrease Damage Taken 35 → 45% for the two rounds after each 40 AP cast (incoming ×0.55 against ×0.65 at base, ≈ ×0.846). Lodestone Draw is the fourth purchase: both self damage buffs and both exposure rows 37% (≈ ×1.06 own damage on a fully covered strike) and Reflect 42%. On the 1v1 race lens (outgoing / incoming ≈ 1.25 against 1.17 to 1.19 for the offense builds) it is still the tree's strongest allocation. Like Poles Repel (Reflect 45%) is the all-defense alternative.
- **Violent Repulsion:** Rising Star Reflect 40 → 50% (60% per-hit cap untouched) with Magnetic Assignment Decrease Damage Taken 42% (+7%): every blow in the window costs the attacker half of what lands while the kit's strikes stay at base. Per 100 incoming before mitigation it takes 58 and returns 29, against 65 and 26 at base. Magnetized Guard is the fourth purchase; Lodestone Draw (buffs and exposure 37%) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Fortress | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Magnetic Pulse Strike | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Magnetic Pulse Strike | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Rising Star | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Rising Star | 1 | Reflect | self | 40% | 42% (+2) | 40% | 42% (+2) | 50% (+10) |
| Morning Star | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Morning Star | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 35% |
| Houkyuken: Magnetic Assignment | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 45% (+10) | 42% (+7) |
| Houkyuken: Magnetic Assignment | 1 | Increase Damage Given | self | 35% | 39% (+4) | 39% (+4) | 37% (+2) | 35% |
| Houkyuken: Magnetic Assignment | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 35% |
| Houkyu Dance | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Houkyu Dance | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Houkyu Dance | 2 | Increase Damage Given | self | 35% | 39% (+4) | 39% (+4) | 37% (+2) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +4% Increase Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Starfall Hammer: +2 Damage (0 + 0 + 2; off band)
  - Route Inexorable Pull: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Absolute Alignment: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Violent Repulsion: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (DMG 4, DDT 1, IDG 2, IDT 2, REF 1)
- Strongest full build by row-weighted total: Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field (raw +14, row-weighted 24)
- Lowest row-weighted node: Magnetized Guard (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Magnetic Pulse Strike 50 -> 52

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Magnetic Pulse Strike | 0 | 50 (Nuke) | **52 (above Nuke)** |
| Rising Star | 0 | 40 (Normal) | 42 (Normal) |
| Morning Star | 0 | 40 (Normal) | 42 (Normal) |
| Houkyu Dance | 0 | 45 (High) | 47 (High) |

Above-Nuke rationale: Kit fact: the Houkyuken dossier's Traits line is "Burst, Control"; Magnetic Pulse Strike (50 EP) is the highest of its four Magnet Taijutsu strikes. Starfall Hammer's +2 Damage lifts it 50 → 52, past the 50 Nuke tier, as the controlled payoff of the burst route (Polarized Fist's +2% Increase Damage Given setup, then +2 Damage): the pattern the director kept in Blood-Enchanted Eyes (Rite of Exsanguination, Reaper's Embrace 50 → 52; RUL-2026-10-04-001) and Shakunetsu Sakura (Conflagration in Bloom, Sakura-ame 50 → 52; RUL-2026-10-04-002). Flat Damage sits only on Starfall Hammer, so no allocation without it exceeds 50; no legal allocation exceeds +2 Damage; the other rows stay in tier (45 → 47, 40 → 42). Fable proposal, flagged for director review (DQ-A).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Starfall Hammer | +2 Damage, +4% IDG, +2% IDT | Reversed Polarity | +2 Damage, +4% IDG, +4% IDT | 24 |
| Starfall Hammer | +2 Damage, +4% IDG, +2% IDT | Repelling Field *(highest diagnostic)* | +2 Damage, +4% IDG, +2% IDT, +2% DDT, +2% REF | 24 |
| Inexorable Pull | +2% IDG, +8% IDT | Polarized Fist | +4% IDG, +8% IDT | 24 |
| Inexorable Pull | +2% IDG, +8% IDT | Repelling Field *(highest diagnostic)* | +2% IDG, +8% IDT, +2% DDT, +2% REF | 24 |
| Absolute Alignment | +10% DDT, +2% REF | Lodestone Draw *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT, +2% REF | 20 |
| Absolute Alignment | +10% DDT, +2% REF | Like Poles Repel | +10% DDT, +5% REF | 15 |
| Violent Repulsion | +4% DDT, +10% REF | Lodestone Draw *(highest diagnostic)* | +2% IDG, +2% IDT, +4% DDT, +10% REF | 22 |
| Violent Repulsion | +4% DDT, +10% REF | Magnetized Guard | +7% DDT, +10% REF | 17 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Lodestone Draw, Polarized Fist, Starfall Hammer, Reversed Polarity | +2 Damage, +4% IDG, +4% IDT |
| 2 | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +2 Damage, +4% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Lodestone Draw, Polarized Fist, Reversed Polarity, Inexorable Pull | +4% IDG, +8% IDT |
| 4 | Lodestone Draw, Polarized Fist, Reversed Polarity, Repelling Field | +4% IDG, +4% IDT, +2% DDT, +2% REF |
| 5 | Lodestone Draw, Polarized Fist, Repelling Field, Magnetized Guard | +4% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Lodestone Draw, Polarized Fist, Repelling Field, Like Poles Repel | +4% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field | +2% IDG, +8% IDT, +2% DDT, +2% REF |
| 8 | Lodestone Draw, Reversed Polarity, Repelling Field, Magnetized Guard | +2% IDG, +4% IDT, +5% DDT, +2% REF |
| 9 | Lodestone Draw, Reversed Polarity, Repelling Field, Like Poles Repel | +2% IDG, +4% IDT, +2% DDT, +5% REF |
| 10 | Lodestone Draw, Repelling Field, Magnetized Guard, Absolute Alignment | +2% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Lodestone Draw, Repelling Field, Magnetized Guard, Like Poles Repel | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Lodestone Draw, Repelling Field, Like Poles Repel, Violent Repulsion | +2% IDG, +2% IDT, +4% DDT, +10% REF |
| 13 | Repelling Field, Magnetized Guard, Absolute Alignment, Like Poles Repel | +10% DDT, +5% REF |
| 14 | Repelling Field, Magnetized Guard, Like Poles Repel, Violent Repulsion | +7% DDT, +10% REF |

## Design notes

- Structure unchanged (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10). Maxima over every legal allocation: Damage +2 (Starfall Hammer only), Increase Damage Given +4% (01+02), Increase Damage Taken +8% (01+04+05), Decrease Damage Taken +10%, Reflect +10%. Not jointly attainable.
- 2026-10-04 rebalance. First pass: the pre-batch +5 Damage Burst route (Polarized Fist +2, Starfall Hammer +3) lifted Rising Star and Morning Star 40 → 45, Houkyu Dance 45 → 50 and Magnetic Pulse Strike 50 → 55 and was cut; Exposure came down from +10% to +8% and Inexorable Pull lost its Increase Damage Given rider. Roster pass: the pure +4% Increase Damage Given Starfall Hammer that replaced Burst mirrored Exposure (both ×3.95 at 4 BP), so Burst returns in the director pattern: Polarized Fist's +2% Increase Damage Given setup, then Starfall Hammer's controlled +2 Damage (RUL-2026-10-04-001/002; above_nuke_rationale). Final review: Absolute Alignment's +2% Increase Damage Given rider equalled Polarized Fist, so Fortress + Lodestone Draw held Starfall Hammer's whole self-buff package plus +10% Decrease Damage Taken (outgoing / incoming ≈ 1.29); the rider is dropped. Final cleanup: the 50 → 52 result stays because the dossier Traits include Burst, not because the pre-batch tree had a burst route.
- Damage tiers: the +2 reaches all four Magnet strikes in one step: Magnetic Pulse Strike 50 → 52 (past the Nuke tier; director review), Houkyu Dance 45 → 47, Rising Star and Morning Star 40 → 42. No lower tier is crossed. +2 is the batch's flat-Damage limit (every director anchor uses +2), and only Starfall Hammer carries it, so no allocation without the capstone exceeds 50.
- Offense is sized by compounded factor over base: +8% exposure on two compounding rows is ×1.43² / 1.35² ≈ ×1.122, against Blood-Enchanted Eyes' ×1.115 exposure maximum and Shakunetsu Sakura's ×1.075. The top 4-BP offensive package is Exposure + Polarized Fist, ×1.122 × 1.060 ≈ ×1.19 (×3.95 on a fully covered own strike against ×3.32 at base), under Blood-Enchanted Eyes' ×1.234. Burst + Reversed Polarity is ×1.124 before its +2 Damage and ×1.17 to ×1.18 after (×3.88 to ×3.92), below Blood-Enchanted Eyes' Rite of Exsanguination package (×1.149, ≈ ×1.19 on Reaper's Embrace). Burst gives up a little in-window peak for +2 Damage on every strike, window or not, across Houkyu Dance's whole area and through a debuff cleanse. Both Hidden Arts stay +2% so each offense route's obvious fourth adds no more than Lodestone Draw already does.
- Defense keeps the single-row pattern: +10% on the one Decrease Damage Taken row (Arashima's Unbroken Horizon, RUL-2026-10-04-003, is the same +10% on one 35% row) and +10% on the one Reflect row. Decrease Damage Taken works on (1 − p): 35 → 45% makes incoming ×0.55/0.65 ≈ ×0.846 (about +18% effective HP) per window, more than either offense route adds at 3 BP (×1.14 to ×1.16 on a fully covered strike). Absolute Alignment is pure Decrease Damage Taken: the kit's only other defensive tag is Reflect, and a Reflect rider would make Fortress a mirror of Violent Repulsion. Fortress + Lodestone Draw (01+06+07+08) pairs ×0.846 incoming with ×1.37⁴ / 1.35⁴ ≈ ×1.06 own damage, an outgoing/incoming ratio of about 1.25 against 1.17 to 1.19 for every offense build with either fourth: still the strongest 1v1 allocation, by 5 to 7%, about the 6% lead Arashima's approved fortress holds on the same lens (Unbroken Horizon + Tempest Hymn against Sundered Sky + Stillness in the Squall).
- Reflect reads post-mitigation damage (the post-damage family runs after the damage modifiers; SOURCE_MECHANICS §3, process.ts 415-612), so Decrease Damage Taken trims what Reflect returns while Magnetic Assignment's window is live. Per 100 incoming before mitigation: base takes 65 and returns 26; the Retaliation route (Decrease Damage Taken 39%, Reflect 50%) takes 61 and returns 30.5 (+17%, not the +25% the Reflect print suggests); with Magnetized Guard 58 and 29 (+12%); Fortress + Like Poles Repel 55 and 24.75, below base. Violent Repulsion keeps its rider because a counter-tank has to survive the window it punishes.
- Fourth purchases: Burst takes Reversed Polarity (all-in) or Repelling Field; Exposure Polarized Fist (all-in) or Repelling Field; Fortress Lodestone Draw or Like Poles Repel; Retaliation Magnetized Guard or Lodestone Draw. All 14 full allocations are non-dominated on tag totals, so every node appears in a non-dominated build.
- Filters and order: Magnetic Assignment's self Increase Damage Given row is Taijutsu-filtered with no element, so at the pin (SOURCE_MECHANICS §3) it raises every Taijutsu or element-less hit; Houkyu Dance's row (Lightning/Magnet/None/Wind) raises Lightning, Magnet, Wind and element-less hits. Both compound (computeDamagePacket, §3b) and the 25% + 0.15/level bloodline passive applies last. Increase Damage Given, Increase Damage Taken and Decrease Damage Taken never touch pierce.
- Delivery: every cast has cooldown 7 and every percentage row is live the two rounds after its cast round, never in it (§3b); flat Damage needs no window. Magnetic Assignment (D rank, 40 AP, OTHER_USER, range 4) carries three supported rows; a fully covered strike needs Magnetic Assignment plus Houkyu Dance (Burst) or Morning Star (Exposure) in the two rounds before it.

## Risks and unproven interactions

- Self-buff reach: Magnetic Assignment's Increase Damage Given row is effectively unfiltered at the pin (any Taijutsu or element-less hit), so the +4% maximum (39% per row) also raises matching normal jutsu, weapons and basic attacks in each window, over the 25% + 0.15/level passive.
- Exposure stacking: Morning Star's Increase Damage Taken (all four stat types, no element) and Magnetic Assignment's (Lightning/Magnet/None/Wind) are separate two-round debuffs that compound on one target: ×1.35² ≈ ×1.82 at base, ×1.43² ≈ ×2.04 at the +8% maximum (≈ ×1.122 over base), for hits from the player, allies and weapons (pierce excluded). Both rows are friendly fire none: either cast aimed at an ally puts its exposure on that ally (§3b).
- Damage concentration: +2 Damage lands on four Magnet strikes at once; each costs 60 AP on cooldown 7, so at most one lands per round. Magnetic Pulse Strike at 52 sits above the 50 Nuke tier (director review). Off-kit Magnet Damage rows gain +2 too; their count is unverified.
- Reflect concentration: one row (Rising Star, 60 AP, range 4); the route takes it to 50%, under the 60% per-hit cap. It returns pierce damage, bypasses shield absorption and answers every attacker in the two-round window, so its value grows with the number of attackers; aimed at an ally the ENEMIES-only hit is withheld but the SELF Reflect still lands (§3b).
- Houkyu Dance delivery: its Increase Damage Given row is target SELF on an EMPTY_GROUND AOE_CIRCLE_SPAWN jutsu, realized on the caster at cast (actions.ts 980-1004; SOURCE_MECHANICS §4b), so the buff never depends on standing in the circle. The unsupported move row touches no potency row.
- Classification: element-wide Magnet scope (RUL-2026-10-03-005); sharing Magnet with Itojinsei is expected. The tree targets all 10 supported rows. Six carry Magnet (the four Damage rows, Houkyu Dance's Increase Damage Given and Magnetic Assignment's Increase Damage Taken); the four element-less rows need the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Under the current resolver Starfall Hammer's +2 Damage works in full, Burst's and Exposure's percentage steps each reach one of their two rows, and both defense primaries (Magnetic Assignment Decrease Damage Taken, Rising Star Reflect) do nothing. Off-kit Magnet coverage is unverified.
- Unamplified: wound (Magnetic Pulse Strike), move (Houkyu Dance) and the 15% Lightning Decrease Damage Taken passive receive nothing, so the Control trait is served only through exposure.
- Skill-tree and bloodline effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed; balance values remain user-owned.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Magnet jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

