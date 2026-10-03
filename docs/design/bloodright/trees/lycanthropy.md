# Lycanthropy — Blood Under the Moon

**Bloodline:** Lycanthropy (BR-043, rank B, `_zHoQitqM_tiiqX7Egv-p`) · **Revision:** Draft 4 / Lycanthropy classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Lycanthropy (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Frenzy — Increase Damage Given (Frenzy Assault, Feral Wrath; two self rows) · secondary Taijutsu damage — Moonlit Fury and Feral Wrath (two formula rows) · tertiary Sustain — Heal (Frenzy Assault; one static row).

The kit's five supported rows split 2/2/1: two 35% self Increase Damage Given rows (Frenzy Assault, Taijutsu-filtered; Feral Wrath, all four stat types) that can both be up at once and reach basic attacks, weapons and normal jutsu; two Taijutsu formula damage rows (Moonlit Fury 40, Feral Wrath 50 at jutsu level 25); and one static Heal (40 = 400 HP once per 7 rounds). The frenzy rows are the bloodline's identity (its passive is also Taijutsu Increase Damage Given) and take the broader-reaching route; damage takes the raw-power route; the single Heal row serves the Healing and Sustain trait as a side branch. Wound, cleanseprevent and move are unsupported, and the 10% lifesteal passive is not a jutsu row.

> **Narrow-kit exception:** Seven nodes and two Advanced Arts rather than ten and four: three supported tags on five rows (Damage x2, Increase Damage Given x2, Heal x1). The Beast Within forks into a Damage route (Gnashing Fangs → Jaws of the Alpha, +5) and a frenzy route (Blood on the Wind → Red Moon Rising, +10% on two self rows that compound). Heal is one static row (400 HP once per 7 rounds), so it carries only a side chain (Moonbound Vigor +2% → Lick the Wound +3%; 400 → 450 HP). That chain is accepted low-value trait representation for Healing and Sustain, not evidence that filler was avoided: Moonbound Vigor is a Foundation only because the chain needs a root, covers one row of one jutsu and is not broadly useful support in the brief's section 2 sense; both nodes are the lowest row-weighted purchases at their depth (2 against 4 among Foundations; 3 against 4 and 6 among Hidden Arts). A Heal capstone was declined: each +1% on the static row is 10 HP once per 7 rounds, so even +5% more is 50 HP per cast; a Damage or IDG capstone behind the Heal chain would twin the existing routes on the same two rows. Universal node accepted: The Beast Within is in all 7 legal 4 BP builds. One leaf Hidden Art under Moonbound Vigor would leave that root three nodes deep, so it still has no 4 BP closure without The Beast Within; the leaf could only carry Heal, Damage or IDG on rows Lick the Wound, Gnashing Fangs and Blood on the Wind already cover, so it would be filler. A mirrored layout only moves the universal node to the other root. Three distinct complete builds exist (Burst, Frenzy, Sustain hybrid). Keeping the Heal chain is a user-owned shape decision; the alternatives are in risks.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Lycanthropy-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | The Beast Within | Foundation | None | +2% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 02 | Gnashing Fangs | Hidden Art | The Beast Within | +2 Damage (damage) | Feral Wrath, Moonlit Fury / 2 |
| 03 | Jaws of the Alpha | Advanced Art | Gnashing Fangs | +3 Damage (damage) | Feral Wrath, Moonlit Fury / 2 |
| 04 | Blood on the Wind | Hidden Art | The Beast Within | +3% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 05 | Red Moon Rising | Advanced Art | Blood on the Wind | +5% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 06 | Moonbound Vigor | Foundation | None | +2% Heal (self buff) | Frenzy Assault / 1 |
| 07 | Lick the Wound | Hidden Art | Moonbound Vigor | +3% Heal (self buff) | Frenzy Assault / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07. Advanced Arts: 2; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **The Beast Within** — The change begins in the blood: claws lengthen, and every blow lands heavier. Frenzy Assault and Feral Wrath Increase Damage Given 35 → 37% (self, 2 rounds). 2 rows.
- **Gnashing Fangs** — Teeth made for tearing, not for talking. Moonlit Fury 40 → 42 and Feral Wrath 50 → 52 EP; both Taijutsu formula hits, no gates or hidden rows. 2 rows.
- **Jaws of the Alpha** — The pack leader does not wound. It finishes. Route total +5 Damage: Moonlit Fury 40 → 45, Feral Wrath 50 → 55 EP. Feral Wrath hits every enemy in its circle (friendly fire ENEMIES). 2 rows.
- **Blood on the Wind** — One whiff of an open wound and the frenzy takes hold. Frenzy Assault and Feral Wrath Increase Damage Given 37 → 40% with The Beast Within (self, 2 rounds each). 2 rows, both self buffs.
- **Red Moon Rising** — Under a bloody moon there is no holding back, and nothing left to hold back. Route total +10%: both Increase Damage Given rows 35 → 45% (self, 2 rounds); Feral Wrath's row is realized on the caster at cast, not via tiles.
- **Moonbound Vigor** — Flesh knits under moonlight as readily as it tears. Frenzy Assault Heal 40 → 42 = 420 HP, one tick on the following round (rounds 1, 40 AP, cooldown 7). 1 row, the kit's only sustain.
- **Lick the Wound** — What a beast cannot outfight, it outlasts. Frenzy Assault Heal 42 → 45 with Moonbound Vigor = 450 HP on the following round (+5% Heal in total). 1 row.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | HEAL |
|---|---|---:|---:|---:|
| Jaws of the Alpha (Burst) | The Beast Within, Gnashing Fangs, Jaws of the Alpha, Blood on the Wind | +5 | +5% | — |
| Red Moon Rising (Frenzy) | The Beast Within, Gnashing Fangs, Blood on the Wind, Red Moon Rising | +2 | +10% | — |
| Lick the Wound (Sustain) | The Beast Within, Blood on the Wind, Moonbound Vigor, Lick the Wound | — | +5% | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Jaws of the Alpha:** +5 Damage on both Taijutsu hits (Moonlit Fury 40 → 45, Feral Wrath 50 → 55 EP; the frenzy buffs and the bloodline's Taijutsu IDG passive multiply them), with Blood on the Wind as the fourth purchase so both buff rows sit at 40%. Moonbound Vigor (Frenzy Assault heals 420 HP) is the sustain-leaning alternative fourth purchase.
- **Red Moon Rising:** The +10% route on both Increase Damage Given rows (Frenzy Assault and Feral Wrath 35 → 45%, self): every element-less hit the caster lands in the two rounds after each cast, including basic attacks, weapons and normal jutsu, is amplified, not only the kit attacks. Gnashing Fangs is the fourth purchase (attacks 42/52 EP); Moonbound Vigor (420 HP tick) is the sustain-leaning alternative.
- **Lick the Wound:** A no-Advanced hybrid built around Frenzy Assault: its Heal reaches +5% (450 HP on the following round) and both frenzy rows sit at 40%. It trades a capstone for the kit's only sustain row; Gnashing Fangs in place of Blood on the Wind (attacks 42/52 EP, buffs 37%) is the other sustain hybrid.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Frenzy | Sustain |
|---|---:|---|---|---:|---:|---:|---:|
| Moonlit Fury | 0 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% |
| Moonlit Fury | 1 | cleanseprevent (unsupported) | enemy | 100 | 100 | 100 | 100 |
| Moonlit Fury | 2 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 |
| Frenzy Assault | 0 | Increase Damage Given | self | 35% | 40% (+5) | 45% (+10) | 40% (+5) |
| Frenzy Assault | 1 | Heal | self | 40 | 40 | 40 | 45 (+5) |
| Feral Wrath | 0 | Damage | enemy | 50 | 55 (+5) | 52 (+2) | 50 |
| Feral Wrath | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Feral Wrath | 2 | Increase Damage Given | self | 35% | 40% (+5) | 45% (+10) | 40% (+5) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 6, 4: 7
- Full-budget allocations: 7; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +5% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Jaws of the Alpha: +5 Damage (0 + 2 + 3; on band)
  - Route Red Moon Rising: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 5 (DMG 2, HEAL 1, IDG 2)
- Strongest full build by row-weighted total: The Beast Within, Gnashing Fangs, Blood on the Wind, Red Moon Rising (raw +12, row-weighted 24)
- Lowest row-weighted node: Moonbound Vigor (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (The Beast Within) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | The Beast Within, Gnashing Fangs, Jaws of the Alpha, Blood on the Wind | +5 Damage, +5% IDG |
| 2 | The Beast Within, Gnashing Fangs, Jaws of the Alpha, Moonbound Vigor | +5 Damage, +2% IDG, +2% HEAL |
| 3 | The Beast Within, Gnashing Fangs, Blood on the Wind, Red Moon Rising | +2 Damage, +10% IDG |
| 4 | The Beast Within, Gnashing Fangs, Blood on the Wind, Moonbound Vigor | +2 Damage, +5% IDG, +2% HEAL |
| 5 | The Beast Within, Gnashing Fangs, Moonbound Vigor, Lick the Wound | +2 Damage, +2% IDG, +5% HEAL |
| 6 | The Beast Within, Blood on the Wind, Red Moon Rising, Moonbound Vigor | +10% IDG, +2% HEAL |
| 7 | The Beast Within, Blood on the Wind, Moonbound Vigor, Lick the Wound | +5% IDG, +5% HEAL |

## Design notes

- Node split: 2 Foundations, 3 Hidden Arts, 2 Advanced Arts. The Beast Within (Increase Damage Given +2% on both buff rows) forks into Gnashing Fangs → Jaws of the Alpha (Damage +2/+3) and Blood on the Wind → Red Moon Rising (IDG +3%/+5%). Moonbound Vigor → Lick the Wound (Heal +2%/+3%) is a separate side chain. Both Advanced Arts are 3 BP deep and share the root, so owning both costs 5 BP; a build holds at most one.
- Recalibration (RUL-2026-10-03-005): The Beast Within's +1 Damage is removed, so the Damage route is the default +5 (Gnashing Fangs +2, Jaws of the Alpha +3; Moonlit Fury 40 → 45, Feral Wrath 50 → 55 EP); the frenzy route moves from +7% to +10% (The Beast Within +2%, Blood on the Wind +2% → +3%, Red Moon Rising +3% → +5%; both rows 35 → 45%). Heal stays +5% (400 → 450 HP). Maxima over every legal allocation: Damage +5, IDG +10%, Heal +5%.
- Interactions: both frenzy rows are element-less, so Frenzy Assault's Taijutsu filter is not binding (it excludes only elemental hits of another stat type) and Feral Wrath's four-stat row matches every hit; neither touches pierce. Each multiplies a matching hit by 1 + its percentage and the two compound (×1.35 × 1.35 ≈ ×1.82 at base, ×1.45 × 1.45 ≈ ×2.10 with the frenzy route); the bloodline's Taijutsu IDG passive (20 + 0.15/level) applies last. Extra damage also feeds the 10% lifesteal passive (60% leech budget).
- Delivery: all three jutsu have cooldown 7. Frenzy Assault is a 40 AP self cast (IDG 2 rounds; Heal rounds 1 = one tick next round). Moonlit Fury is a 60 AP single hit at range 4. Feral Wrath is a 60 AP ground circle: damage to enemies in it (friendly fire ENEMIES); its IDG row is SELF, realized on the caster at cast (actions.ts 980-1004), not via the tiles. Each IDG window is the two rounds after its cast round and never helps that round's hits, Feral Wrath's own strike included (§3b).
- Fourth purchases and allocations: Burst → Blood on the Wind (buffs 40%; the example) or Moonbound Vigor (420 HP); Frenzy → Gnashing Fangs (attacks 42/52 EP; the example) or Moonbound Vigor (420 HP); Sustain hybrids 01,04,06,07 (buffs 40%, 450 HP; the example) and 01,02,06,07 (attacks 42/52 EP, buffs 37%, 450 HP); the last no-Advanced hybrid is 01,02,04,06 (42/52 EP, 40%, 420 HP). The validator finds 7 legal full allocations, all non-dominated, every node in at least one; 3 of the 7 hold no Advanced Art. By row weight the Frenzy example is strongest (24) and Burst 20.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Lycanthropy' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Increase Damage Given breadth (user-owned value): Red Moon Rising puts both self buffs at 45%; same-tag effects all apply (process.ts 1109-1117), so with both windows up a matching hit is multiplied by about ×2.10 instead of ×1.82, on basic attacks, weapons and normal jutsu as well as the kit. +10% is this tag's ceiling; the +5% band is the lighter alternative.
- Uptime: each IDG window is the two rounds after its cast, once per 7-round cooldown. Both windows coincide only when Frenzy Assault and Feral Wrath are cast in the same round (100 AP), leaving the next two rounds for Moonlit Fury, basic attacks and weapons; consecutive-round casts share one round. Realized value depends on what lands in those rounds; not simulated.
- Universal opener: every legal 4 BP build contains The Beast Within (validator WARN, acknowledged in the exception). The Moonbound Vigor root has two nodes and one added leaf would leave it at three, so no 4 BP closure avoids the opener; a mirrored layout (Heal + IDG root, damage chain apart) only moves it.
- Heal chain (user-owned shape): +5% Heal is +50 HP once per 7 rounds, so Moonbound Vigor and Lick the Wound are the weakest purchases at their depth. A second modifier on Moonbound Vigor is closed by the ceilings (any IDG there lifts the frenzy maximum above +10%, any Damage the Damage maximum above +5); the alternative is to replace the chain with one Heal +5% Hidden Art under The Beast Within (six nodes).
- Damage is formula-calculated (sqrt stat scaling); the frenzy buffs and the bloodline's Taijutsu IDG passive multiply the result, so +5 EP is not linear +5 damage and realized value depends on stats. Lifesteal (10% passive) grows with it but shares the 60% leech budget with vamp. No combat simulation was performed.
- Unsupported rows: Moonlit Fury's wound 30% and cleanseprevent, and Feral Wrath's move, receive nothing. The bloodline's lifesteal passive is not a jutsu row, so the Healing and Sustain trait is served only through the single Heal row. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Lycanthropy-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

