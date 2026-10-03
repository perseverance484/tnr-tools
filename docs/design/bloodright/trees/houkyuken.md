# Houkyuken — The Lodestone Fist

**Bloodline:** Houkyuken (BR-033, rank A, `ALoGrHuBY5Ml9bJG_DILe`) · **Revision:** Draft 1 / Magnet classification / forked tree · **Classification:** Magnet (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Magnet burst (Damage on four casts; self Increase Damage Given on Houkyuken: Magnetic Assignment and Houkyu Dance) · secondary Enemy exposure (Increase Damage Taken on Morning Star and Houkyuken: Magnetic Assignment) · tertiary Self defense (Decrease Damage Taken on Houkyuken: Magnetic Assignment; Reflect on Rising Star).

Ten supported rows sit on five casts and six of them are offensive: four Magnet Taijutsu Damage rows (Magnetic Pulse Strike 50, Houkyu Dance 45, Rising Star 40, Morning Star 40) and two 35% self Increase Damage Given rows (Magnetic Assignment, Taijutsu-filtered with no element; Houkyu Dance's circle, Lightning/Magnet/None/Wind) that sit over a 25% + 0.15/level Increase Damage Given passive. The Control trait reaches potency through two stacking 35% enemy Increase Damage Taken rows (Morning Star, all four stat types; Magnetic Assignment, Lightning/Magnet/None/Wind). Defense is one universal 35% Decrease Damage Taken row and one 40% Reflect row, so root Lodestone carries the offense and exposure routes and root Repulsion the defense and counter routes; row-weighted full builds run 17–32 against the Taiyo Kami reference's 20–31 on nine rows.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Magnet-classified Houkyuken jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Lodestone Draw | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Houkyu Dance, Houkyuken: Magnetic Assignment, Morning Star / 4 |
| 02 | Polarized Fist | Hidden Art | Lodestone Draw | +2 Damage power (damage) | Houkyu Dance, Magnetic Pulse Strike, Morning Star, Rising Star / 4 |
| 03 | Starfall Hammer | Advanced Art | Polarized Fist | +3 Damage power (damage) | Houkyu Dance, Magnetic Pulse Strike, Morning Star, Rising Star / 4 |
| 04 | Reversed Polarity | Hidden Art | Lodestone Draw | +2% Increase Damage Taken (enemy debuff) | Houkyuken: Magnetic Assignment, Morning Star / 2 |
| 05 | Inexorable Pull | Advanced Art | Reversed Polarity | +3% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment, Morning Star / 4 |
| 06 | Repelling Field | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |
| 07 | Magnetized Guard | Hidden Art | Repelling Field | +3% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment / 1 |
| 08 | Absolute Alignment | Advanced Art | Magnetized Guard | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment / 3 |
| 09 | Like Poles Repel | Hidden Art | Repelling Field | +3% Reflect (self buff) | Rising Star / 1 |
| 10 | Violent Repulsion | Advanced Art | Like Poles Repel | +5% Reflect (self buff); +2% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Lodestone Draw** — Iron answers the fist before the blow lands; the enemy is already leaning in. Self damage buffs 35→37% (Magnetic Assignment, Houkyu Dance circle); enemy exposure 35→37% (Morning Star, Magnetic Assignment).
- **Polarized Fist** — Charge the knuckles until the strike carries its own weight twice over. Magnetic Pulse Strike 50→52, Houkyu Dance 45→47, Rising Star and Morning Star 40→42 power; four Magnet hits, 60 AP each, cooldown 7.
- **Starfall Hammer** — A star does not fall by accident. It is pulled down. Same four Damage rows; route total +5 (55/50/45/45 power). Wound on Pulse Strike and move on Houkyu Dance are unsupported.
- **Reversed Polarity** — Flip the field and the body that fled now hurries toward the hammer. Both exposure rows 37→39% with Lodestone Draw: Morning Star (any non-pierce source), Magnetic Assignment (Lightning/Magnet/Wind/none).
- **Inexorable Pull** — Nothing with iron in its blood escapes the draw. Exposure to route total 42% (+7; 84% when both debuffs sit on one target); self damage buffs 37→39% with Lodestone Draw.
- **Repelling Field** — Turn the pole outward and every blow meets an invisible hand. Magnetic Assignment Decrease Damage Taken 35→37% (every non-pierce hit, 40 AP); Rising Star Reflect 40→42% (includes pierce hits).
- **Magnetized Guard** — Filings align along the skin; the body becomes its own armour. Magnetic Assignment Decrease Damage Taken only: 37→40% with Repelling Field; one universal row, 2 rounds per 40 AP cast, cooldown 7.
- **Absolute Alignment** — Every particle set in order; what strikes you finds nothing out of place. Decrease Damage Taken to route total 45% (+10); plus both self damage buffs 35→37% (39% with Lodestone Draw).
- **Like Poles Repel** — Bring like to like and the strike is thrown back on the one who threw it. Rising Star Reflect only: 42→45% with Repelling Field; one self row, 2 rounds per 60 AP single-target cast, under the 60% per-hit cap.
- **Violent Repulsion** — The closer the enemy presses, the harder the field hurls them away. Reflect to route total 50% (+10; 60% per-hit cap untouched); Decrease Damage Taken 37→39% (42% with Magnetized Guard).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | REF |
|---|---|---:|---:|---:|---:|---:|
| Starfall Hammer (Burst) | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +5 | +2% | +2% | +2% | +2% |
| Inexorable Pull (Exposure) | Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field | — | +4% | +7% | +2% | +2% |
| Absolute Alignment (Bulwark) | Repelling Field, Magnetized Guard, Absolute Alignment, Lodestone Draw | — | +4% | +2% | +10% | +2% |
| Violent Repulsion (Counterstrike) | Repelling Field, Like Poles Repel, Violent Repulsion, Magnetized Guard | — | — | — | +7% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Starfall Hammer:** The +5 power route on all four Magnet Damage rows (Pulse Strike 55, Houkyu Dance 50, Rising Star and Morning Star 45) with both self damage buffs and both exposure rows at 37%. Repelling Field is the fourth purchase because it hardens the two casts the burst rotation already uses (Magnetic Assignment 37% Decrease Damage Taken, Rising Star 42% Reflect) without re-buying offense; Reversed Polarity (exposure 39%) is the all-in alternative.
- **Inexorable Pull:** Both enemy Increase Damage Taken rows at the route maximum 42% (+7; 84% when Morning Star and Magnetic Assignment both land on one target), amplifying the player's, allies' and weapons' non-pierce hits, with both self damage buffs at 39%. Repelling Field is the fourth purchase so Magnetic Assignment also shields at 37% and Rising Star reflects 42%; Polarized Fist (42/42/47/52 power) is the burst alternative.
- **Absolute Alignment:** Magnetic Assignment's universal Decrease Damage Taken at the route maximum 45% (+10) for two rounds per 40 AP cast, with both self damage buffs at 39% from the capstone's secondary plus Lodestone Draw and both exposure rows at 37%. Lodestone Draw is the fourth purchase because it compounds the self-buff secondary on the same cast; Like Poles Repel (Reflect 45%) is the defensive alternative.
- **Violent Repulsion:** Rising Star's Reflect at the route maximum 50% (+10, under the 60% per-hit cap) with Magnetic Assignment's Decrease Damage Taken at 42% (+7): a counter-tank that makes every two-round window after Rising Star punish the attacker while the kit's own Magnet hits stay at base. Magnetized Guard is the fourth purchase for the shield depth; Lodestone Draw (buffs and exposure 37%) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Bulwark | Counterstrike |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Magnetic Pulse Strike | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Magnetic Pulse Strike | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Rising Star | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Rising Star | 1 | Reflect | self | 40% | 42% (+2) | 42% (+2) | 42% (+2) | 50% (+10) |
| Morning Star | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Morning Star | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 35% |
| Houkyuken: Magnetic Assignment | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 42% (+7) |
| Houkyuken: Magnetic Assignment | 1 | Increase Damage Given | self | 35% | 37% (+2) | 39% (+4) | 39% (+4) | 35% |
| Houkyuken: Magnetic Assignment | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 35% |
| Houkyu Dance | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Houkyu Dance | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Houkyu Dance | 2 | Increase Damage Given | self | 35% | 37% (+2) | 39% (+4) | 39% (+4) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +4%, Increase Damage Taken +7%, Decrease Damage Taken +10%, Reflect +10% (not jointly attainable)
- Supported rows in kit: 10 (DMG 4, DDT 1, IDG 2, IDT 2, REF 1)
- Strongest full build by row-weighted total: Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field (raw +13, row-weighted 32)
- Lowest row-weighted node: Magnetized Guard (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Lodestone Draw, Polarized Fist, Starfall Hammer, Reversed Polarity | DMG +5, IDG +2, IDT +4 |
| 2 | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | DMG +5, IDG +2, IDT +2, DDT +2, REF +2 |
| 3 | Lodestone Draw, Polarized Fist, Reversed Polarity, Inexorable Pull | DMG +2, IDG +4, IDT +7 |
| 4 | Lodestone Draw, Polarized Fist, Reversed Polarity, Repelling Field | DMG +2, IDG +2, IDT +4, DDT +2, REF +2 |
| 5 | Lodestone Draw, Polarized Fist, Repelling Field, Magnetized Guard | DMG +2, IDG +2, IDT +2, DDT +5, REF +2 |
| 6 | Lodestone Draw, Polarized Fist, Repelling Field, Like Poles Repel | DMG +2, IDG +2, IDT +2, DDT +2, REF +5 |
| 7 | Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field | IDG +4, IDT +7, DDT +2, REF +2 |
| 8 | Lodestone Draw, Reversed Polarity, Repelling Field, Magnetized Guard | IDG +2, IDT +4, DDT +5, REF +2 |
| 9 | Lodestone Draw, Reversed Polarity, Repelling Field, Like Poles Repel | IDG +2, IDT +4, DDT +2, REF +5 |
| 10 | Lodestone Draw, Repelling Field, Magnetized Guard, Absolute Alignment | IDG +4, IDT +2, DDT +10, REF +2 |
| 11 | Lodestone Draw, Repelling Field, Magnetized Guard, Like Poles Repel | IDG +2, IDT +2, DDT +5, REF +5 |
| 12 | Lodestone Draw, Repelling Field, Like Poles Repel, Violent Repulsion | IDG +2, IDT +2, DDT +4, REF +10 |
| 13 | Repelling Field, Magnetized Guard, Absolute Alignment, Like Poles Repel | IDG +2, DDT +10, REF +5 |
| 14 | Repelling Field, Magnetized Guard, Like Poles Repel, Violent Repulsion | DDT +7, REF +10 |

## Design notes

- Node split: root Lodestone (Lodestone Draw, +2 self Increase Damage Given and +2 exposure, two rows each) forks into a Damage route (Polarized Fist → Starfall Hammer) and an exposure route (Reversed Polarity → Inexorable Pull). Root Repulsion (Repelling Field, +2 Decrease Damage Taken, +2 Reflect) forks into a shield route (Magnetized Guard → Absolute Alignment) and a reflect route (Like Poles Repel → Violent Repulsion). 2/4/4 nodes; every Advanced Art is 3 BP deep; any two cost 5 or 6 BP.
- Flats scaled by coverage. Damage reaches four Magnet rows (40/40/45/50), so it keeps the reference ladder +2/+3 (max +5), not the +6 some four-row siblings use; the route is row-weighted 20 against Taiyo Kami's 15. Increase Damage Taken reaches two stacking enemy rows: +2/+2/+3 (max +7, 42%), the two-row guardrail. Increase Damage Given reaches two stacking self rows and is Foundation-plus-secondaries only: max +4 (39%). Decrease Damage Taken and Reflect are one row each: +2/+3/+5 (max +10).
- Capstone secondaries never out-bid a sibling Hidden Art on its own tag: Inexorable Pull and Absolute Alignment add +2 self buff (no Hidden Art carries IDG); Violent Repulsion adds +2 DDT under Magnetized Guard's +3; Starfall Hammer is single-tag. Row-weighted node values: Foundations 8/4, Hidden Arts 8/4/3/3, Advanced Arts 12/10/9/7; full builds 17–32 (Taiyo Kami 20–31 on nine rows). Maxima over all legal builds: Damage +5, IDG +4, IDT +7, DDT +10, Reflect +10; not jointly attainable.
- Main tree, passives, pierce: Magnetic Assignment's self IDG row is Taijutsu-filtered with no element, so at the pin (SOURCE_MECHANICS §3) it multiplies every Taijutsu hit and every element-less hit of any stat type (basic attacks, non-elemental normal jutsu); Houkyu Dance's row (Lightning/Magnet/None/Wind) multiplies same-element and element-less hits. Both stack on the 25% + 0.15/level IDG passive, which also multiplies the enhanced Magnet Damage rows. Pierce ignores Damage Taken modifiers.
- Delivery and uptime: every cast is cooldown 7; every percentage row lasts 2 rounds. The four Damage casts cost 60 AP; Magnetic Assignment is a D-rank 40 AP OTHER_USER cast (range 4) carrying three supported rows, the load-bearing cast for every route. Houkyu Dance's Damage is a ground circle (range 5, friendly fire ENEMIES, no ally hazard); its self buff is a SELF row on that spawn and reaches the caster from the next round while standing in it. 84% exposure needs two overlapping casts.
- Fourth purchases: Burst takes Repelling Field or Reversed Polarity; Exposure Repelling Field or Polarized Fist; Bulwark Lodestone Draw or Like Poles Repel; Counterstrike Magnetized Guard or Lodestone Draw. All 14 legal full allocations are non-dominated on tag totals and every node appears in one; no-capstone hybrids stay distinct because no capstone secondary repeats a sibling Hidden Art's tag at an equal or higher flat. Four examples: each capstone closes a different role.

## Risks and unproven interactions

- Self-buff leakage: neither Increase Damage Given row has a binding filter at the pin (Magnetic Assignment: Taijutsu, no element; Houkyu Dance: Lightning/Magnet/None/Wind), so the +4 maximum raises matching normal jutsu, weapons and basic attacks in each two-round window, not only bloodline casts, and both rows stack on the caster over the 25% + 0.15/level passive. Uptime not simulated.
- Exposure stacking: Morning Star's Increase Damage Taken (all four stat types, no element) and Magnetic Assignment's (Lightning/Magnet/None/Wind, no stat filter) are separate two-round debuffs that stack on one target to 70% base and 84% at the +7 route maximum, amplifying hits from the player, allies and weapons. Pierce hits are unaffected (modifiers run before pierce).
- Damage concentration: +5 power lands on four Magnet rows at once, so the burst route is row-weighted 20 against the reference's 15 and the strongest full build (Starfall Hammer + Repelling Field) reads 32 against Taiyo Kami's 31 on nine rows. Three of the four hits cost 60 AP on cooldown 7, so only one lands per round; the final value is user-owned and no combat simulation was performed.
- Reflect concentration: Reflect has one row (Rising Star, B rank, 60 AP, range 4, OTHER_USER, 2 rounds) and the route takes it to 50%, under the 60% per-hit cap; Reflect returns pierce damage and bypasses shield absorption. Its whole value rides one single-target cast per seven rounds that needs a legal enemy target in range, and it does nothing on rounds the enemy does not attack the caster.
- Houkyu Dance delivery: its Increase Damage Given row is a SELF row on an EMPTY_GROUND AOE_CIRCLE_SPAWN jutsu (range 5). The dossier marks it a self buff; the batch-1 lesson says it reaches the caster from the following round while standing in the circle (move sorts last). SELF-row handling on ground spawns was not separately source-verified. Its Damage row is friendly-fire ENEMIES; no ally hazard.
- Classification: Magnet is the single signature element on all four Damage rows, but Itojinsei [INCLUDE] carries Magnet on 6 rows (4 damage), so the label works only as a bloodline-scoped whole-kit classification, not a bare element match. Under the current resolver 6 of 10 supported rows match Magnet directly; the four element-less rows fall back to None. Normal-jutsu collision unverified.
- Unsupported rows and passives: wound (Magnetic Pulse Strike) and move (Houkyu Dance) receive nothing, and the 15% Lightning Decrease Damage Taken passive is not a jutsu row, so the Control trait is strengthened only through exposure and mobility is untouched. Magnetic Assignment carries three of the ten supported rows and every route touches it: a D-rank 40 AP cast is the load-bearing action.
- Context: skill-tree and bloodline effects are suppressed in ranked PvP and ranked sparring; normal-tree potency policy is not approved, so a combined stacking audit is required before implementation. The dominance count treats every tag as a gain and ignores delivery, so 14/14 non-dominated is structural evidence only. No combat simulation was performed; balance values remain user-owned.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Houkyuken jutsu inherit Magnet potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

