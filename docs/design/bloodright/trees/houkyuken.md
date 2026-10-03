# Houkyuken — The Lodestone Fist

**Bloodline:** Houkyuken (BR-033, rank A, `ALoGrHuBY5Ml9bJG_DILe`) · **Revision:** Draft 4 / Magnet classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Magnet (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Magnet burst (Damage on four casts; self Increase Damage Given on Houkyuken: Magnetic Assignment and Houkyu Dance) · secondary Enemy exposure (Increase Damage Taken on Morning Star and Houkyuken: Magnetic Assignment) · tertiary Self defense (Decrease Damage Taken on Houkyuken: Magnetic Assignment; Reflect on Rising Star).

Ten supported rows sit on five casts and six of them are offensive: four Magnet Taijutsu Damage rows (Magnetic Pulse Strike 50, Houkyu Dance 45, Rising Star 40, Morning Star 40 EP) and two 35% self Increase Damage Given rows (Magnetic Assignment, Taijutsu-filtered with no element; Houkyu Dance, Lightning/Magnet/None/Wind; both realized on the caster at cast time) that sit over a 25% + 0.15/level Increase Damage Given passive. The Control trait reaches potency through two stacking 35% enemy Increase Damage Taken rows (Morning Star, all four stat types; Magnetic Assignment, Lightning/Magnet/None/Wind). Defense is one universal 35% Decrease Damage Taken row and one 40% Reflect row, so root Lodestone carries the offense and exposure routes and root Repulsion the defense and counter routes. Potency reaches matching supported tags on all Magnet jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Magnet jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Lodestone Draw | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Houkyu Dance, Houkyuken: Magnetic Assignment, Morning Star / 4 |
| 02 | Polarized Fist | Hidden Art | Lodestone Draw | +2 Damage (damage) | Houkyu Dance, Magnetic Pulse Strike, Morning Star, Rising Star / 4 |
| 03 | Starfall Hammer | Advanced Art | Polarized Fist | +3 Damage (damage) | Houkyu Dance, Magnetic Pulse Strike, Morning Star, Rising Star / 4 |
| 04 | Reversed Polarity | Hidden Art | Lodestone Draw | +3% Increase Damage Taken (enemy debuff) | Houkyuken: Magnetic Assignment, Morning Star / 2 |
| 05 | Inexorable Pull | Advanced Art | Reversed Polarity | +5% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment, Morning Star / 4 |
| 06 | Repelling Field | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |
| 07 | Magnetized Guard | Hidden Art | Repelling Field | +3% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment / 1 |
| 08 | Absolute Alignment | Advanced Art | Magnetized Guard | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment / 3 |
| 09 | Like Poles Repel | Hidden Art | Repelling Field | +3% Reflect (self buff) | Rising Star / 1 |
| 10 | Violent Repulsion | Advanced Art | Like Poles Repel | +5% Reflect (self buff); +2% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Lodestone Draw** — Iron answers the fist before the blow lands; the enemy is already leaning in. Self Increase Damage Given 35 → 37% (Magnetic Assignment, Houkyu Dance; SELF rows, live after the cast round); exposure 35 → 37% (Morning Star, Magnetic Assignment).
- **Polarized Fist** — Charge the knuckles until every blow lands with twice its weight. Magnetic Pulse Strike 50 → 52, Houkyu Dance 45 → 47, Rising Star and Morning Star 40 → 42 EP; four Magnet hits, 60 AP each, cooldown 7.
- **Starfall Hammer** — A star does not fall by accident. It is pulled down. Same four Damage rows; route total +5 Damage (55 / 50 / 45 / 45 EP). Wound on Pulse Strike and move on Houkyu Dance are unsupported.
- **Reversed Polarity** — Flip the field and the body that fled now hurries toward the hammer. Both exposure rows 40% with Lodestone Draw: Morning Star (any non-pierce source), Magnetic Assignment (Lightning/Magnet/Wind/element-less hits).
- **Inexorable Pull** — Nothing with iron in its blood escapes the draw. Exposure route total +10% (35 → 45%; ×1.45 × 1.45 ≈ ×2.10 on a hit both cover); self damage buffs 39% with Lodestone Draw.
- **Repelling Field** — Turn the pole outward and every blow meets an invisible hand. Magnetic Assignment Decrease Damage Taken 35 → 37% (every non-pierce hit, 40 AP); Rising Star Reflect 40 → 42% (includes pierce hits).
- **Magnetized Guard** — Filings align along the skin; the body becomes its own armour. Magnetic Assignment Decrease Damage Taken only: 40% with Repelling Field; one universal row, 2 rounds per 40 AP cast, cooldown 7.
- **Absolute Alignment** — Every particle set in order; what strikes you finds nothing out of place. Decrease Damage Taken route total +10% (35 → 45%); plus both self damage buffs 35 → 37% (39% with Lodestone Draw).
- **Like Poles Repel** — Bring like to like and the strike is thrown back on the one who threw it. Rising Star Reflect only: 45% with Repelling Field; one self row, 2 rounds per 60 AP single-target cast, under the 60% per-hit cap.
- **Violent Repulsion** — The closer the enemy presses, the harder the field hurls them away. Reflect route total +10% (40 → 50%; 60% per-hit cap untouched); Decrease Damage Taken 39% with Repelling Field (42% with Magnetized Guard).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | REF |
|---|---|---:|---:|---:|---:|---:|
| Starfall Hammer (Burst) | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +5 | +2% | +2% | +2% | +2% |
| Inexorable Pull (Exposure) | Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field | — | +4% | +10% | +2% | +2% |
| Absolute Alignment (Bulwark) | Repelling Field, Magnetized Guard, Absolute Alignment, Lodestone Draw | — | +4% | +2% | +10% | +2% |
| Violent Repulsion (Counterstrike) | Repelling Field, Like Poles Repel, Violent Repulsion, Magnetized Guard | — | — | — | +7% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Starfall Hammer:** +5 Damage on all four Magnet Damage rows (Pulse Strike 55, Houkyu Dance 50, Rising Star and Morning Star 45 EP) with both self damage buffs and both exposure rows at 37% for hits in the two rounds after each buff or debuff cast. Repelling Field is the fourth purchase because it hardens two casts the rotation already uses (Magnetic Assignment 37% Decrease Damage Taken, Rising Star 42% Reflect) without re-buying offense; Reversed Polarity (exposure 40%) is the all-in alternative.
- **Inexorable Pull:** Both enemy Increase Damage Taken rows at the route maximum 45% (+10%; ×1.45 × 1.45 ≈ ×2.10 on a hit both cover when Morning Star and Magnetic Assignment both sit on one target), raising the player's, allies' and weapons' non-pierce hits, with both self damage buffs at 39%. Repelling Field is the fourth purchase so Magnetic Assignment also shields at 37% and Rising Star reflects 42%; Polarized Fist (42 / 42 / 47 / 52 EP) is the burst alternative.
- **Absolute Alignment:** Magnetic Assignment's universal Decrease Damage Taken at the route maximum 45% (+10%) for the two rounds after each 40 AP cast, with both self damage buffs at 39% from the capstone's secondary plus Lodestone Draw, both exposure rows at 37% and Reflect 42%. Lodestone Draw is the fourth purchase because it adds +2% to the same two self damage buffs the capstone raises; Like Poles Repel (Reflect 45%) is the defensive alternative.
- **Violent Repulsion:** Rising Star's Reflect at the route maximum 50% (+10%, under the 60% per-hit cap) with Magnetic Assignment's Decrease Damage Taken at 42% (+7%): a counter-tank that makes every two-round window after Rising Star punish the attacker while the kit's own Magnet hits stay at base. Magnetized Guard is the fourth purchase for the shield depth; Lodestone Draw (buffs and exposure 37%) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Bulwark | Counterstrike |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Magnetic Pulse Strike | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Magnetic Pulse Strike | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Rising Star | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Rising Star | 1 | Reflect | self | 40% | 42% (+2) | 42% (+2) | 42% (+2) | 50% (+10) |
| Morning Star | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Morning Star | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 35% |
| Houkyuken: Magnetic Assignment | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 42% (+7) |
| Houkyuken: Magnetic Assignment | 1 | Increase Damage Given | self | 35% | 37% (+2) | 39% (+4) | 39% (+4) | 35% |
| Houkyuken: Magnetic Assignment | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 35% |
| Houkyu Dance | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Houkyu Dance | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Houkyu Dance | 2 | Increase Damage Given | self | 35% | 37% (+2) | 39% (+4) | 39% (+4) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +4% Increase Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Starfall Hammer: +5 Damage (0 + 2 + 3; on band)
  - Route Inexorable Pull: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Absolute Alignment: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Violent Repulsion: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (DMG 4, DDT 1, IDG 2, IDT 2, REF 1)
- Strongest full build by row-weighted total: Lodestone Draw, Polarized Fist, Reversed Polarity, Inexorable Pull (raw +16, row-weighted 36)
- Lowest row-weighted node: Magnetized Guard (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Lodestone Draw, Polarized Fist, Starfall Hammer, Reversed Polarity | +5 Damage, +2% IDG, +5% IDT |
| 2 | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Lodestone Draw, Polarized Fist, Reversed Polarity, Inexorable Pull | +2 Damage, +4% IDG, +10% IDT |
| 4 | Lodestone Draw, Polarized Fist, Reversed Polarity, Repelling Field | +2 Damage, +2% IDG, +5% IDT, +2% DDT, +2% REF |
| 5 | Lodestone Draw, Polarized Fist, Repelling Field, Magnetized Guard | +2 Damage, +2% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Lodestone Draw, Polarized Fist, Repelling Field, Like Poles Repel | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field | +4% IDG, +10% IDT, +2% DDT, +2% REF |
| 8 | Lodestone Draw, Reversed Polarity, Repelling Field, Magnetized Guard | +2% IDG, +5% IDT, +5% DDT, +2% REF |
| 9 | Lodestone Draw, Reversed Polarity, Repelling Field, Like Poles Repel | +2% IDG, +5% IDT, +2% DDT, +5% REF |
| 10 | Lodestone Draw, Repelling Field, Magnetized Guard, Absolute Alignment | +4% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Lodestone Draw, Repelling Field, Magnetized Guard, Like Poles Repel | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Lodestone Draw, Repelling Field, Like Poles Repel, Violent Repulsion | +2% IDG, +2% IDT, +4% DDT, +10% REF |
| 13 | Repelling Field, Magnetized Guard, Absolute Alignment, Like Poles Repel | +2% IDG, +10% DDT, +5% REF |
| 14 | Repelling Field, Magnetized Guard, Like Poles Repel, Violent Repulsion | +7% DDT, +10% REF |

## Design notes

- Reference reuse: topology and most values follow Taiyo Kami (two roots, four 3-BP routes; Lodestone Draw = Dawnheart, +2/+3 Damage = Crown of Cinders/Solar Cataclysm, Magnetized Guard = Golden Mantle). Departures: exposure (Reversed Polarity +3%, Inexorable Pull +5%) replaces Afterburn and Reflect replaces Decrease Damage Given (the kit has neither); capstone Increase Damage Given secondaries are +2% (two rows).
- Routes (RUL-2026-10-03-005): Burst +5 Damage (Polarized Fist +2, Starfall Hammer +3) on four Magnet rows; Exposure +10% Increase Damage Taken (Lodestone Draw +2%, Reversed Polarity +3%, Inexorable Pull +5%) on two stacking enemy rows; Bulwark +10% Decrease Damage Taken and Counterstrike +10% Reflect (each 2/3/5) on one row each. Increase Damage Given is Foundation-plus-secondaries glue: maximum +4% (39%). Maxima over every legal allocation: Damage +5, IDG +4%, IDT +10%, DDT +10%, Reflect +10%; not jointly attainable.
- Recalibration from Draft 3: Reversed Polarity +2% → +3% and Inexorable Pull's exposure +3% → +5% move the Exposure route from +7% to the +10% band (45% per row; ×1.45 × 1.45 ≈ ×2.10 on a hit both cover). All other values are unchanged.
- Capstone secondaries never out-bid a sibling Hidden Art on its own tag: Inexorable Pull and Absolute Alignment add +2% self buff (no Hidden Art carries IDG); Violent Repulsion adds +2% DDT under Magnetized Guard's +3%; Starfall Hammer is single-tag. Row-weighted full builds run 17–36 (Taiyo Kami 16–31 on nine rows); the top is 01+02+04+05 (exposure +10% on two rows plus +2 Damage), then Burst and Exposure at 32.
- Main tree, passives, pierce: Magnetic Assignment's self IDG row is Taijutsu-filtered with no element, so at the pin (SOURCE_MECHANICS §3) it raises every Taijutsu hit and every element-less hit (basic attacks, non-elemental normal jutsu); Houkyu Dance's row (Lightning/Magnet/None/Wind) raises Lightning, Magnet, Wind and element-less hits. Both live: ×1.35 × 1.35 ≈ ×1.82 on a hit both cover (×1.39² ≈ ×1.93 at +4%), compounding (computeDamagePacket, §3b); the 25% + 0.15/level bloodline passive applies last. IDG/IDT/DDT never touch pierce.
- Delivery and uptime: all casts cooldown 7; percentage rows live the two rounds after their cast round, never in it (§3b); Damage casts 60 AP. Magnetic Assignment (D rank, 40 AP, OTHER_USER, range 4) carries three supported rows and every route touches it; it needs a living non-caster target in range 4, ally or enemy (on an ally its self rows still reach the caster). Houkyu Dance's self buff is a target-SELF row realized on the caster at cast (actions.ts 980-1004), not positional.
- Fourth purchases: Burst takes Repelling Field or Reversed Polarity; Exposure Repelling Field or Polarized Fist; Bulwark Lodestone Draw or Like Poles Repel; Counterstrike Magnetized Guard or Lodestone Draw. All 14 legal full allocations are non-dominated on tag totals and every node appears in one. Four examples: each capstone closes a different role.

## Risks and unproven interactions

- Self-buff reach: Magnetic Assignment's IDG row (Taijutsu, no element) is effectively unfiltered at the pin (any Taijutsu or element-less hit); Houkyu Dance's row (Lightning/Magnet/None/Wind, no stat filter) reaches only Lightning, Magnet, Wind and element-less hits. The +4% maximum raises matching normal jutsu, weapons and basic attacks per window, over the 25% + 0.15/level passive.
- Exposure stacking: Morning Star's Increase Damage Taken (four stat types, no element) and Magnetic Assignment's (Lightning/Magnet/None/Wind) are separate two-round debuffs that compound on one target: ×1.35² ≈ ×1.82 at base, ×1.45² ≈ ×2.10 at the +10% maximum on a hit both cover, for hits from the player, allies and weapons (pierce excluded). Both rows are friendly fire none: either cast aimed at an ally puts its 35–45% exposure on that ally (§3b).
- Damage concentration: +5 Damage lands on four Magnet rows at once (row-weighted 20). All four hits cost 60 AP on cooldown 7, so only one lands per round; the final value is user-owned and no combat simulation was performed.
- Reflect concentration: one row (Rising Star, B rank, 60 AP, range 4, OTHER_USER); the route takes it to 50%, under the 60% per-hit cap; it returns pierce damage and bypasses shield absorption. One cast per seven rounds, live the two rounds after it; aimed at an ally the ENEMIES-only hit is withheld but the SELF Reflect still lands (§3b). It does nothing on rounds nobody attacks the caster.
- Houkyu Dance delivery: its Increase Damage Given row is target SELF on an EMPTY_GROUND AOE_CIRCLE_SPAWN jutsu (range 5), realized on the caster at cast (actions.ts 980-1004; SOURCE_MECHANICS §4b), not through the tiles: its 2 rounds never depend on standing in the circle. Where the unsupported move row leaves the caster is unverified; it touches no potency row. Damage is enemies-only.
- Classification: element-wide Magnet scope (RUL-2026-10-03-005): matching supported tags on all Magnet jutsu, whatever their source; sharing Magnet with other bloodlines (Itojinsei) is expected. Every kit jutsu carries Magnet on a row, but only 6 of the 10 supported rows do; the four element-less rows need the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Magnet coverage is unverified.
- Unsupported rows: wound (Magnetic Pulse Strike) and move (Houkyu Dance) receive nothing, and the 15% Lightning DDT passive is not a jutsu row, so Control is strengthened only through exposure and mobility is untouched. Magnetic Assignment carries three of the ten supported rows and every route touches it: a D-rank 40 AP cast needing a living non-caster target in range 4 is the load-bearing action.
- Context: skill-tree and bloodline effects are suppressed in ranked PvP and ranked sparring; normal-tree potency policy is not approved, so a combined stacking audit is required before implementation. The dominance count treats every tag as a gain and ignores delivery, so 14/14 non-dominated is structural evidence only. No combat simulation was performed; balance values remain user-owned.

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

