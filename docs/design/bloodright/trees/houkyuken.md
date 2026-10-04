# Houkyuken — The Lodestone Fist

**Bloodline:** Houkyuken (BR-033, rank A, `ALoGrHuBY5Ml9bJG_DILe`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Magnet classification / forked tree · **Classification:** Magnet (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense from Lodestone Draw: Burst on the two self damage buffs (Increase Damage Given on Houkyuken: Magnetic Assignment and Houkyu Dance) or Exposure on the two enemy debuffs (Increase Damage Taken on Morning Star and Houkyuken: Magnetic Assignment) · secondary Defense from Repelling Field: Fortress (Decrease Damage Taken on Houkyuken: Magnetic Assignment) or Retaliation (Reflect on Rising Star) · tertiary No flat Damage: Magnetic Pulse Strike is a 50 EP Nuke, so any Damage bonus would pass the Nuke tier.

Ten supported rows sit on five casts. The four Magnet Taijutsu Damage rows (Magnetic Pulse Strike 50, Houkyu Dance 45, Rising Star and Morning Star 40 EP) are left at base because even +1 Damage lifts Pulse Strike past the 50 Nuke tier; Burst is carried instead by the two 35% self Increase Damage Given rows, which compound on a hit both cover. Lodestone Draw answers "How do I make each blow land harder: strengthen my own fist, or drag the target onto it?" with Burst (own hits on every target) and Exposure (every attacker's hits on the marked target). Repelling Field answers "How do I answer the blows aimed at me: blunt them, or throw them back?" with Fortress on the one universal Decrease Damage Taken row and Retaliation on the one Reflect row. Potency reaches matching supported tags on all Magnet jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Lodestone Draw | Foundation | How do I make each blow land harder: strengthen my own fist, or drag the target onto it? |
| Repelling Field | Foundation | How do I answer the blows aimed at me: blunt them, or throw them back? |
| Starfall Hammer | Advanced Art | burst: a self-amplified strike window (own hits on every target) |
| Inexorable Pull | Advanced Art | exposure: mark one target for every attacker |
| Absolute Alignment | Advanced Art | fortress: the Magnetic Assignment window as armour that still swings |
| Violent Repulsion | Advanced Art | retaliation: every blow in the window costs the attacker |

- Concern: No flat Damage on a Burst-trait kit: Magnetic Pulse Strike is 50 EP, so any Damage bonus passes the Nuke tier. If the director prefers the Blood-Enchanted Eyes pattern (+2 Damage payoff; Pulse Strike 50 → 52, Houkyu Dance 45 → 47), Starfall Hammer is where it would go in place of its +4% Increase Damage Given.
- Concern: Burst and Exposure converge at 4 BP: a capstone plus the sibling Hidden Art gives the same ×3.95 on a fully set-up solo strike. They differ only in reach (own hits on every target, Houkyu Dance's area included, against every attacker's hits on the marked target); party-size effects were not simulated.
- Concern: Retaliation keeps Reflect at +10% (50%) on one row; its value scales with the number of attackers in the window and was not simulated.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Magnet jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Lodestone Draw | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Houkyu Dance, Houkyuken: Magnetic Assignment, Morning Star / 4 |
| 02 | Polarized Fist | Hidden Art | Lodestone Draw | +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment / 2 |
| 03 | Starfall Hammer | Advanced Art | Polarized Fist | +4% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment / 2 |
| 04 | Reversed Polarity | Hidden Art | Lodestone Draw | +2% Increase Damage Taken (enemy debuff) | Houkyuken: Magnetic Assignment, Morning Star / 2 |
| 05 | Inexorable Pull | Advanced Art | Reversed Polarity | +4% Increase Damage Taken (enemy debuff) | Houkyuken: Magnetic Assignment, Morning Star / 2 |
| 06 | Repelling Field | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |
| 07 | Magnetized Guard | Hidden Art | Repelling Field | +3% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment / 1 |
| 08 | Absolute Alignment | Advanced Art | Magnetized Guard | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Houkyu Dance, Houkyuken: Magnetic Assignment / 3 |
| 09 | Like Poles Repel | Hidden Art | Repelling Field | +3% Reflect (self buff) | Rising Star / 1 |
| 10 | Violent Repulsion | Advanced Art | Like Poles Repel | +5% Reflect (self buff); +2% Decrease Damage Taken (self buff) | Houkyuken: Magnetic Assignment, Rising Star / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Lodestone Draw** — Iron answers the fist before the blow lands; the enemy is already leaning in. Self Increase Damage Given 35 → 37% (Magnetic Assignment, Houkyu Dance) and enemy exposure 35 → 37% (Morning Star, Magnetic Assignment); each row is live the two rounds after its cast.
- **Polarized Fist** — Charge the knuckles with the field, and every blow that follows lands heavier. Both self damage buffs 37 → 39% with Lodestone Draw (Magnetic Assignment, Houkyu Dance); they compound on a hit both cover.
- **Starfall Hammer** — A star does not fall by accident. It is pulled down. Burst: both self damage buffs 35 → 43% on the full route (×1.43² ≈ ×2.04 on a hit both cover, ×1.82 at base). No Damage row moves; Magnetic Pulse Strike stays 50 EP.
- **Reversed Polarity** — Flip the field and the body that fled now hurries toward the hammer. Both exposure rows 37 → 39% with Lodestone Draw: Morning Star (any stat type) and Magnetic Assignment (Lightning, Magnet, Wind and element-less hits).
- **Inexorable Pull** — Nothing with iron in its blood escapes the draw. Exposure: both enemy rows 35 → 43% on the full route (×1.43² ≈ ×2.04 on a hit both cover) for every non-pierce hit the target takes, the party's included.
- **Repelling Field** — Turn the pole outward and every blow meets an invisible hand. Magnetic Assignment Decrease Damage Taken 35 → 37% (every non-pierce hit, 40 AP); Rising Star Reflect 40 → 42% (includes pierce hits).
- **Magnetized Guard** — Filings align along the skin; the body becomes its own armour. Magnetic Assignment Decrease Damage Taken only: 40% with Repelling Field; one universal row, 2 rounds per 40 AP cast, cooldown 7.
- **Absolute Alignment** — Every particle set in order; what strikes you finds nothing out of place. Fortress: Magnetic Assignment Decrease Damage Taken 35 → 45% on the full route (incoming ×0.55, ×0.65 at base); both self damage buffs 35 → 37% (39% with Lodestone Draw).
- **Like Poles Repel** — Bring like to like and the strike is thrown back on the one who threw it. Rising Star Reflect only: 45% with Repelling Field; one self row, 2 rounds per 60 AP single-target cast, under the 60% per-hit cap.
- **Violent Repulsion** — The closer the enemy presses, the harder the field hurls them away. Retaliation: Rising Star Reflect 40 → 50% on the full route (under the 60% per-hit cap); Magnetic Assignment Decrease Damage Taken 39% with Repelling Field (42% with Magnetized Guard).

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | REF |
|---|---|---:|---:|---:|---:|
| Starfall Hammer (Burst) | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +8% | +2% | +2% | +2% |
| Inexorable Pull (Exposure) | Lodestone Draw, Reversed Polarity, Inexorable Pull, Polarized Fist | +4% | +8% | — | — |
| Absolute Alignment (Fortress) | Repelling Field, Magnetized Guard, Absolute Alignment, Lodestone Draw | +4% | +2% | +10% | +2% |
| Violent Repulsion (Retaliation) | Repelling Field, Like Poles Repel, Violent Repulsion, Magnetized Guard | — | — | +7% | +10% |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Starfall Hammer:** Both self damage buffs 35 → 43% (Magnetic Assignment, Houkyu Dance; ×1.43² ≈ ×2.04 on a hit both cover) with exposure 37% on Morning Star and Magnetic Assignment. Repelling Field is the fourth purchase (Magnetic Assignment Decrease Damage Taken 37%, Rising Star Reflect 42%); Reversed Polarity (exposure 39%) is the all-in alternative. No Damage row moves: Pulse Strike stays 50 EP.
- **Inexorable Pull:** Both exposure rows 35 → 43% with both self buffs 39% from Polarized Fist as the fourth purchase: ×1.43² × 1.39² ≈ ×3.95 on a kit strike under all four rows (×3.32 at base), and the exposure half also raises allies' non-pierce hits on the target. This is the strongest offense allocation; Starfall Hammer with Reversed Polarity mirrors it for own hits on every target. Repelling Field is the defensive alternative.
- **Absolute Alignment:** Magnetic Assignment's universal Decrease Damage Taken 35 → 45% for the two rounds after each 40 AP cast (incoming ×0.55, ×0.65 at base), with both self damage buffs 39% from the capstone rider and Lodestone Draw as the fourth purchase, exposure 37% and Reflect 42%. Like Poles Repel (Reflect 45%) is the all-defense alternative.
- **Violent Repulsion:** Rising Star Reflect 40 → 50% (60% per-hit cap untouched) with Magnetic Assignment Decrease Damage Taken 42% (+7%): every blow in the window costs the attacker half of what lands while the kit's strikes stay at base. Magnetized Guard is the fourth purchase; Lodestone Draw (buffs and exposure 37%) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Fortress | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Magnetic Pulse Strike | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Magnetic Pulse Strike | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Rising Star | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Rising Star | 1 | Reflect | self | 40% | 42% (+2) | 40% | 42% (+2) | 50% (+10) |
| Morning Star | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Morning Star | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 35% |
| Houkyuken: Magnetic Assignment | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 45% (+10) | 42% (+7) |
| Houkyuken: Magnetic Assignment | 1 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 39% (+4) | 35% |
| Houkyuken: Magnetic Assignment | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 35% |
| Houkyu Dance | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Houkyu Dance | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Houkyu Dance | 2 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 39% (+4) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 13; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Starfall Hammer: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Inexorable Pull: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Absolute Alignment: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Violent Repulsion: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (DMG 4, DDT 1, IDG 2, IDT 2, REF 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Lodestone Draw, Repelling Field, Magnetized Guard, Absolute Alignment (raw +18, row-weighted 24)
- Lowest row-weighted node: Magnetized Guard (3)

Validator warnings:

- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Magnetic Pulse Strike 50 (Nuke), Rising Star 40 (Normal), Morning Star 40 (Normal), Houkyu Dance 45 (High)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Starfall Hammer | +8% IDG, +2% IDT | Reversed Polarity | +8% IDG, +4% IDT | 24 |
| Starfall Hammer | +8% IDG, +2% IDT | Repelling Field *(highest diagnostic)* | +8% IDG, +2% IDT, +2% DDT, +2% REF | 24 |
| Inexorable Pull | +2% IDG, +8% IDT | Polarized Fist | +4% IDG, +8% IDT | 24 |
| Inexorable Pull | +2% IDG, +8% IDT | Repelling Field *(highest diagnostic)* | +2% IDG, +8% IDT, +2% DDT, +2% REF | 24 |
| Absolute Alignment | +2% IDG, +10% DDT, +2% REF | Lodestone Draw *(highest diagnostic)* | +4% IDG, +2% IDT, +10% DDT, +2% REF | 24 |
| Absolute Alignment | +2% IDG, +10% DDT, +2% REF | Like Poles Repel | +2% IDG, +10% DDT, +5% REF | 19 |
| Violent Repulsion | +4% DDT, +10% REF | Lodestone Draw *(highest diagnostic)* | +2% IDG, +2% IDT, +4% DDT, +10% REF | 22 |
| Violent Repulsion | +4% DDT, +10% REF | Magnetized Guard | +7% DDT, +10% REF | 17 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Lodestone Draw, Polarized Fist, Starfall Hammer, Reversed Polarity | +8% IDG, +4% IDT |
| 2 | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field | +8% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Lodestone Draw, Polarized Fist, Reversed Polarity, Inexorable Pull | +4% IDG, +8% IDT |
| 4 | Lodestone Draw, Polarized Fist, Reversed Polarity, Repelling Field | +4% IDG, +4% IDT, +2% DDT, +2% REF |
| 5 | Lodestone Draw, Polarized Fist, Repelling Field, Magnetized Guard | +4% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Lodestone Draw, Polarized Fist, Repelling Field, Like Poles Repel | +4% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Lodestone Draw, Reversed Polarity, Inexorable Pull, Repelling Field | +2% IDG, +8% IDT, +2% DDT, +2% REF |
| 8 | Lodestone Draw, Reversed Polarity, Repelling Field, Magnetized Guard | +2% IDG, +4% IDT, +5% DDT, +2% REF |
| 9 | Lodestone Draw, Reversed Polarity, Repelling Field, Like Poles Repel | +2% IDG, +4% IDT, +2% DDT, +5% REF |
| 10 | Lodestone Draw, Repelling Field, Magnetized Guard, Absolute Alignment | +4% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Lodestone Draw, Repelling Field, Magnetized Guard, Like Poles Repel | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Lodestone Draw, Repelling Field, Like Poles Repel, Violent Repulsion | +2% IDG, +2% IDT, +4% DDT, +10% REF |
| 13 | Repelling Field, Magnetized Guard, Absolute Alignment, Like Poles Repel | +2% IDG, +10% DDT, +5% REF |
| 14 | Repelling Field, Magnetized Guard, Like Poles Repel, Violent Repulsion | +7% DDT, +10% REF |

## Design notes

- Structure unchanged (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10). Maxima over every legal allocation: Increase Damage Given +8% (01+02+03), Increase Damage Taken +8% (01+04+05), Decrease Damage Taken +10%, Reflect +10%; no Damage. Not jointly attainable.
- 2026-10-04 rebalance: the +5 Damage Burst route (Polarized Fist +2, Starfall Hammer +3) is removed. It lifted Rising Star and Morning Star 40 → 45, Houkyu Dance 45 → 50 and Magnetic Pulse Strike 50 → 55, and even +1 passes the Nuke tier on Pulse Strike. Burst now pays off on the two compounding self buffs (2/2/4). Exposure comes down from +10% (Draft 4 raised it to reach the band) to +8% and Inexorable Pull drops its Increase Damage Given rider, so each offense capstone owns one tag.
- Offense is sized by multiplier, not printed total: +8% on two compounding rows is ×1.43² ≈ ×2.04 against ×1.82 at base (+12%). The strongest offense allocation, a capstone plus the sibling Hidden Art, is ×1.43² × 1.39² ≈ ×3.95 on a kit strike under all four rows against ×3.32 at base (+19%). The offense Hidden Arts are +2% (not +3%) so that this obvious fourth adds only +2% of the other tag.
- Defense keeps the single-row pattern: +10% on the one Decrease Damage Taken row and the one Reflect row, each with a +2% rider. Absolute Alignment's rider is Increase Damage Given (Magnetic Assignment carries the shield and the self buff on one cast), which keeps Fortress distinct from Retaliation at 4 BP instead of mirroring it.
- Fourth purchases: Burst takes Reversed Polarity (all-in) or Repelling Field; Exposure Polarized Fist (all-in) or Repelling Field; Fortress Lodestone Draw or Like Poles Repel; Retaliation Magnetized Guard or Lodestone Draw. 13 of 14 full allocations are non-dominated on tag totals: 01+02+06+07 is dominated by the Fortress build with Lodestone Draw because Absolute Alignment's rider equals Polarized Fist; every node still appears in a non-dominated build.
- Filters and order: Magnetic Assignment's self Increase Damage Given row is Taijutsu-filtered with no element, so at the pin (SOURCE_MECHANICS §3) it raises every Taijutsu or element-less hit; Houkyu Dance's row (Lightning/Magnet/None/Wind) raises Lightning, Magnet, Wind and element-less hits. Both compound (computeDamagePacket, §3b) and the 25% + 0.15/level bloodline passive applies last. Increase Damage Given, Increase Damage Taken and Decrease Damage Taken never touch pierce.
- Delivery: every cast has cooldown 7 and every percentage row is live the two rounds after its cast round, never in it (§3b). Magnetic Assignment (D rank, 40 AP, OTHER_USER, range 4) carries three supported rows and every route touches it; a fully covered strike needs Magnetic Assignment plus Houkyu Dance (Burst) or Morning Star (Exposure) in the two rounds before it.

## Risks and unproven interactions

- Self-buff reach: Magnetic Assignment's Increase Damage Given row is effectively unfiltered at the pin (any Taijutsu or element-less hit), so the +8% maximum (43% per row) also raises matching normal jutsu, weapons and basic attacks in each window, over the 25% + 0.15/level passive.
- Exposure stacking: Morning Star's Increase Damage Taken (all four stat types, no element) and Magnetic Assignment's (Lightning/Magnet/None/Wind) are separate two-round debuffs that compound on one target: ×1.35² ≈ ×1.82 at base, ×1.43² ≈ ×2.04 at the +8% maximum, for hits from the player, allies and weapons (pierce excluded). Both rows are friendly fire none: either cast aimed at an ally puts its exposure on that ally (§3b).
- Reflect concentration: one row (Rising Star, 60 AP, range 4); the route takes it to 50%, under the 60% per-hit cap. It returns pierce damage, bypasses shield absorption and answers every attacker in the two-round window, so its value grows with the number of attackers; aimed at an ally the ENEMIES-only hit is withheld but the SELF Reflect still lands (§3b).
- Houkyu Dance delivery: its Increase Damage Given row is target SELF on an EMPTY_GROUND AOE_CIRCLE_SPAWN jutsu, realized on the caster at cast (actions.ts 980-1004; SOURCE_MECHANICS §4b), so the buff never depends on standing in the circle. The unsupported move row touches no potency row.
- Classification: element-wide Magnet scope (RUL-2026-10-03-005); sharing Magnet with Itojinsei is expected. Only 6 of the 10 supported rows carry Magnet; the four element-less rows need the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Magnet coverage is unverified.
- Unamplified: Damage (all four rows), wound (Magnetic Pulse Strike), move (Houkyu Dance) and the 15% Lightning Decrease Damage Taken passive receive nothing, so the Burst trait is served by percentage rows only.
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

