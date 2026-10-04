# Oblivion Seal — Rites of Unmaking

**Bloodline:** Oblivion Seal (BR-053, rank A, `wasIGmDuczwD9PB89gML6`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Shadow classification / forked tree · **Classification:** Shadow (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense under Brand of Oblivion: a Cursed Beast Form self-buff setup paid off by a controlled +2 Damage on the three Shadow attacks (Absolute Erasure), or a Shadow Surge Lifesteal drain that also feeds the self buff (Maw of Oblivion) · secondary Control under Umbral Refuge: Shadow Surge's Decrease Damage Taken fortress (Sealed Against Ruin) or Shadowrend's exposure held behind that reduction (Writ of Oblivion) · tertiary Flat Damage only as Absolute Erasure's +2 payoff (Shadow Tether 50 → 52, kept for the Burst trait; director question DQ-A).

The traits are Burst and Sustained DPS, and the kit's three Shadow attacks are 40, 40 and 50 EP (Cursed Beast Form, Curse Empowerment, Shadow Tether at jutsu level 25, each 60 AP, single target). Its two multipliers sit on single rows: Cursed Beast Form's 35% self buff (the caster's Fire, Lightning, Shadow and element-less hits, any target) and Shadowrend's 35% exposure (every non-pierce hit on the target, any source). Alone against one target those two are interchangeable, so they sit on different Foundations (the Blood-Enchanted Eyes graph). Brand of Oblivion answers "How do I press the attack: strike harder through the beast's window, or feed on every blow I land?": Absolute Erasure is the burst, the path's self buff (35 → 40%) as setup and a controlled +2 Damage on the three attacks as payoff (40 → 42, Shadow Tether 50 → 52, the Blood-Enchanted Eyes / Shakunetsu Sakura precedent); Maw of Oblivion is sustain offense, Shadow Surge's Lifesteal 40 → 45% (+5%, the Lifesteal hard ceiling) with the self buff at 40% (the Blood-Enchanted Eyes / Arashima pattern). Umbral Refuge answers "How do I control the exchange: refuse their blows, or brand them to take more while I hold?": Sealed Against Ruin takes Surge's Decrease Damage Taken 35 → 45% (+10%), Writ of Oblivion takes Shadowrend's exposure 35 → 41% (+6%, ×1.044) with Surge's reduction at 39% (+4%). Potency reaches matching supported tags on all Shadow jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Brand of Oblivion | Foundation | How do I press the attack: strike harder through the beast's window, or feed on every blow I land? |
| Umbral Refuge | Foundation | How do I control the exchange: refuse their blows, or brand them to take more while I hold? |
| Absolute Erasure | Advanced Art | burst: Cursed Beast Form self-buff setup, controlled +2 Damage payoff on the three Shadow attacks |
| Maw of Oblivion | Advanced Art | sustain offense: every hit I land in Surge's window heals me, and the beast's self buff grows (the Feast of the Fallen / The Storm's Due pattern) |
| Sealed Against Ruin | Advanced Art | fortress |
| Writ of Oblivion | Advanced Art | combat dominance: the branded foe takes more from every attacker while Surge's reduction holds |

**Director review recommended:** Roster questions: DQ-A (Absolute Erasure +2 Damage after the Umbral Claws self-buff setup, Shadow Tether 50 → 52, kept for the dossier's Burst trait; see above_nuke_rationale).

- Concern: Solo, Absolute Erasure with Umbral Refuge (≈ ×2.01 on the 40 EP attacks, ≈ ×1.99 on Tether, 37% reduction) leads Writ of Oblivion with Brand of Oblivion (×1.96, 39% reduction) by about 2-3% per kit strike (≈ 1.8% on Tether, ≈ 2.8% on the 40 EP attacks); Writ leads whenever allies hit the branded target. Rotation and uptime were not simulated.
- Concern: Absolute Erasure with Hungering Shade (01, 02, 03, 09: +2 Damage, 40% self buff, 42% Lifesteal) and Maw of Oblivion with Umbral Claws (01, 02, 09, 10: 43% self buff, 45% Lifesteal) share three nodes. In Cursed Beast Form's window (the 37% exposure is common to both) Absolute Erasure's 40 EP strikes take ×1.05 × 1.40 = ×1.47 against Maw's ×1.43 (≈ 2.8% more; Tether ×1.04 × 1.40 ≈ ×1.46, ≈ 1.8% more), and outside Cursed Beast Form's window it keeps ×1.05 while Maw's buff rider adds nothing. In Surge's window Maw heals 0.45 × 1.43 ≈ 0.64 of an unbuilt 40 EP hit against 0.42 × 1.47 ≈ 0.62 (≈ 4% more, ≈ 5% on Tether; the +2 Damage also feeds Absolute Erasure's Lifesteal). Maw + Umbral Claws stacks the self buff to 43% (+8%, one row, inside R3's +10%), the Arashima pattern (The Storm's Due + Gathering Thunderhead +10% against Sundered Sky's +8% path).
- Concern: Writ of Oblivion's exposure is single-row: Shadowrend 35 → 41% on its path (+6%, ×1.044) and 43% with Brand of Oblivion (×1.059), below Shakunetsu Sakura's ×1.075 and Blood-Enchanted Eyes' ×1.115 (R10); the route stays under DQ-B's +7% line. Its team-wide reach (allies' hits on the branded target) was not simulated.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Brand of Oblivion | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Cursed Beast Form, Shadowrend / 2 |
| 02 | Umbral Claws | Hidden Art | Brand of Oblivion | +3% Increase Damage Given (self buff) | Cursed Beast Form / 1 |
| 03 | Absolute Erasure | Advanced Art | Umbral Claws | +2 Damage (damage) | Curse Empowerment, Cursed Beast Form, Shadow Tether / 3 |
| 09 | Hungering Shade | Hidden Art | Brand of Oblivion | +2% Lifesteal (self buff) | Shadow Surge / 1 |
| 10 | Maw of Oblivion | Advanced Art | Hungering Shade | +3% Lifesteal (self buff); +3% Increase Damage Given (self buff) | Cursed Beast Form, Shadow Surge / 2 |
| 06 | Umbral Refuge | Foundation | None | +2% Decrease Damage Taken (self buff) | Shadow Surge / 1 |
| 07 | Veil of Nothing | Hidden Art | Umbral Refuge | +3% Decrease Damage Taken (self buff) | Shadow Surge / 1 |
| 08 | Sealed Against Ruin | Advanced Art | Veil of Nothing | +5% Decrease Damage Taken (self buff) | Shadow Surge / 1 |
| 04 | Unraveled Wards | Hidden Art | Umbral Refuge | +2% Increase Damage Taken (enemy debuff) | Shadowrend / 1 |
| 05 | Writ of Oblivion | Advanced Art | Unraveled Wards | +4% Increase Damage Taken (enemy debuff); +2% Decrease Damage Taken (self buff) | Shadow Surge, Shadowrend / 2 |

Connections: 01→02, 02→03, 01→09, 09→10, 06→07, 07→08, 06→04, 04→05. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Brand of Oblivion** — The seal brands both hands: the one that curses and the one that is cursed. Cursed Beast Form self buff 35 → 37% and Shadowrend exposure 35 → 37% (non-pierce hits), each live the 2 rounds after its 60 AP cast.
- **Umbral Claws** — The beast's shadow lengthens, and its claws find more of you. Setup for Absolute Erasure: Cursed Beast Form self buff 37 → 40% with Brand of Oblivion, on the caster's Fire, Lightning, Shadow and element-less hits in the 2 rounds after each 60 AP cast, any target.
- **Absolute Erasure** — What the seal unmakes, the world forgets. Burst payoff: +2 Damage on all three Shadow attacks, Cursed Beast Form and Curse Empowerment 40 → 42 EP (still Normal) and Shadow Tether 50 → 52 EP (past the 50 Nuke tier; pending director review), each a 60 AP single-target cast. Raw power ×1.05 and ×1.04; under the path's 40% self buff ≈ ×1.09 and ≈ ×1.08 against unbuilt.
- **Hungering Shade** — The shade drinks whatever the curse spills. Shadow Surge Lifesteal 40 → 42%: in the 2 rounds after each Surge cast (cooldown 7) a share of every hit the caster lands heals, Shadowrend's pierce included; 60% cap shared with vamp.
- **Maw of Oblivion** — Open the maw: every wound it swallows feeds the beast that deals the next. Sustain offense: Shadow Surge Lifesteal 40 → 45% on the full route (+5%, the Lifesteal hard ceiling) in the 2 rounds after each Surge cast, and Cursed Beast Form self buff 37 → 40% with Brand of Oblivion (43% with Umbral Claws), so the hits it drains are larger.
- **Umbral Refuge** — The shadow you cast shelters you, and it names your enemy. Shadow Surge self Decrease Damage Taken 35 → 37%, on the caster the 2 rounds after each 40 AP cast (cooldown 7); opens the fortress and the brand-and-hold branches.
- **Veil of Nothing** — Blows that reach into the void find less and less to strike. Shadow Surge self Decrease Damage Taken 37 → 40% with Umbral Refuge; non-pierce hits; a 2-round cast-time buff, not positional.
- **Sealed Against Ruin** — Nothing passes the seal that the sealbearer does not permit. Fortress: Shadow Surge Decrease Damage Taken 35 → 45% on the full route (+10%); non-pierce hits taken ×0.55 instead of ×0.65 in the 2 rounds after each cast.
- **Unraveled Wards** — Shadowrend picks the knots of every ward loose. Setup for Writ of Oblivion: Shadowrend exposure 35 → 37% (39% with Brand of Oblivion) on non-pierce hits in the 2 rounds after each 60 AP cast.
- **Writ of Oblivion** — The sentence is written on their skin: every blade reads it, and the seal turns theirs aside. Combat dominance: Shadowrend exposure 35 → 41% on the full route (+6%, ×1.044; 43%, ×1.059 with Brand of Oblivion), on every non-pierce hit the target takes from any source, allies included; Shadow Surge reduction 35 → 39% (+4%) with Umbral Refuge.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | LS |
|---|---|---:|---:|---:|---:|---:|
| Absolute Erasure (Burst) | Brand of Oblivion, Umbral Claws, Absolute Erasure, Umbral Refuge | +2 | +5% | +2% | +2% | — |
| Maw of Oblivion (Sustain offense) | Brand of Oblivion, Umbral Claws, Hungering Shade, Maw of Oblivion | — | +8% | +2% | — | +5% |
| Sealed Against Ruin (Fortress) | Brand of Oblivion, Umbral Refuge, Veil of Nothing, Sealed Against Ruin | — | +2% | +2% | +10% | — |
| Writ of Oblivion (Combat dominance) | Brand of Oblivion, Umbral Refuge, Unraveled Wards, Writ of Oblivion | — | +2% | +8% | +4% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Absolute Erasure:** Cast Cursed Beast Form, then strike: Umbral Claws holds the self buff at 40% and Absolute Erasure adds +2 Damage to all three Shadow attacks (Cursed Beast Form and Curse Empowerment 40 → 42, Shadow Tether 50 → 52 EP), instant on every cast with no window needed. Curse Empowerment under the buff and Brand of Oblivion's 37% exposure takes ×1.05 × 1.40 × 1.37 ≈ ×2.01 (Tether ×1.04 × 1.40 × 1.37 ≈ ×1.99; unbuilt ×1.35 × 1.35 ≈ ×1.82). Umbral Refuge buys 37% Surge reduction; Hungering Shade (01, 02, 03, 09) is the alternative fourth for 42% Lifesteal. Neither fourth touches the Damage rows, the buff or the exposure.
- **Maw of Oblivion:** Shadow Surge's Lifesteal reaches 45% (+5%, the Lifesteal hard ceiling; 15 points under the 60% leech budget), healed from every hit the caster lands in the 2 rounds after the cast, Shadowrend's pierce included. Maw and Umbral Claws make Cursed Beast Form a 43% self buff (exposure 37%), and Surge plus Cursed Beast Form fit one 100 AP round, so both windows open together: a 40 EP strike takes ×1.43 × 1.37 ≈ ×1.96 and heals 45% of it. Against Absolute Erasure with Hungering Shade that is ≈ 3% less damage under the buff (≈ 2% on Tether), no +2 Damage outside it, and ≈ 4% more healing in Surge's window. Umbral Refuge (01, 06, 09, 10) is the alternative fourth: 37% reduction, 40% self buff.
- **Sealed Against Ruin:** Shadow Surge's Decrease Damage Taken reaches 45% (+10%): non-pierce hits taken in the 2 rounds after each 40 AP cast are ×0.55 instead of ×0.65. Brand of Oblivion is the fourth purchase (37% self buff and exposure); Unraveled Wards (06, 07, 08, 04) gives only 37% exposure and is strictly weaker.
- **Writ of Oblivion:** Shadowrend's exposure reaches 43% (+8% with Brand of Oblivion, ×1.059) on every non-pierce hit the target takes from any source in the 2 rounds after the cast, allies included, while Shadow Surge's reduction stands at 39% (+4%); Brand also lifts the self buff to 37%. Alone, a strike under both windows takes ×1.37 × 1.43 ≈ ×1.96 with 39% reduction, against Absolute Erasure's ≈ ×2.01 on its 40 EP attacks (≈ ×1.99 on Tether) with 37%; every ally's hit on the branded target also takes ×1.43. Veil of Nothing (06, 04, 05, 07) is the alternative fourth: 42% reduction, 41% exposure.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Sustain offense | Fortress | Combat dominance |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Shadowrend | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Shadowrend | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 43% (+8) |
| Cursed Beast Form | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Cursed Beast Form | 1 | Increase Damage Given | self | 35% | 40% (+5) | 43% (+8) | 37% (+2) | 37% (+2) |
| Curse Empowerment | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Curse Empowerment | 1 | clearprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Curse Empowerment | 2 | stun (unsupported) | enemy | 110 | 110 | 110 | 110 | 110 |
| Shadow Tether | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Shadow Tether | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Shadow Surge | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 45% (+10) | 39% (+4) |
| Shadow Surge | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Shadow Surge | 2 | Lifesteal | self | 40% | 40% | 45% (+5) | 40% | 40% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +8% Increase Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Absolute Erasure: +2 Damage (0 + 0 + 2; off band)
  - Route Writ of Oblivion: +6% Increase Damage Taken (0 + 2 + 4; off band)
  - Route Sealed Against Ruin: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Maw of Oblivion: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 7 (DMG 3, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Brand of Oblivion, Umbral Claws, Hungering Shade, Maw of Oblivion (raw +15, row-weighted 15)
- Lowest row-weighted node: Hungering Shade (2)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Shadow Tether 50 -> 52

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Cursed Beast Form | 0 | 40 (Normal) | 42 (Normal) |
| Curse Empowerment | 0 | 40 (Normal) | 42 (Normal) |
| Shadow Tether | 0 | 50 (Nuke) | **52 (above Nuke)** |

Above-Nuke rationale: Kit fact (R1′): the Oblivion Seal dossier's Traits line is "Burst, Sustained DPS", and Shadow Tether is the kit's only 50 EP row and heaviest Damage-tag strike (Shadowrend's 58 pierce row is not a supported tag; 60 AP, cooldown 7, single target). Absolute Erasure's controlled +2 Damage lifts it 50 → 52, past the 50 Nuke tier, as the payoff of Umbral Claws' Cursed Beast Form self-buff setup: the pattern the director kept in Blood-Enchanted Eyes (Reaper's Embrace 50 → 52; RUL-2026-10-04-001) and Shakunetsu Sakura (Sakura-ame 50 → 52; RUL-2026-10-04-002). Absolute Erasure is the tree's only Damage node and an Advanced Art, so no allocation without it exceeds 50 and none exceeds +2 (Cursed Beast Form and Curse Empowerment 40 → 42, still Normal); element-wide potency also lifts any other 50 EP Shadow jutsu the owner casts to 52. Fable proposal, flagged for director review (DQ-A).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Absolute Erasure | +2 Damage, +5% IDG, +2% IDT | Umbral Refuge | +2 Damage, +5% IDG, +2% IDT, +2% DDT | 15 |
| Absolute Erasure | +2 Damage, +5% IDG, +2% IDT | Hungering Shade *(highest diagnostic)* | +2 Damage, +5% IDG, +2% IDT, +2% LS | 15 |
| Writ of Oblivion | +6% IDT, +4% DDT | Brand of Oblivion *(highest diagnostic)* | +2% IDG, +8% IDT, +4% DDT | 14 |
| Writ of Oblivion | +6% IDT, +4% DDT | Veil of Nothing | +6% IDT, +7% DDT | 13 |
| Sealed Against Ruin | +10% DDT | Brand of Oblivion *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT | 14 |
| Sealed Against Ruin | +10% DDT | Unraveled Wards | +2% IDT, +10% DDT | 12 |
| Maw of Oblivion | +5% IDG, +2% IDT, +5% LS | Umbral Claws *(highest diagnostic)* | +8% IDG, +2% IDT, +5% LS | 15 |
| Maw of Oblivion | +5% IDG, +2% IDT, +5% LS | Umbral Refuge | +5% IDG, +2% IDT, +2% DDT, +5% LS | 14 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Brand of Oblivion, Umbral Claws, Absolute Erasure, Umbral Refuge | +2 Damage, +5% IDG, +2% IDT, +2% DDT |
| 2 | Brand of Oblivion, Umbral Claws, Absolute Erasure, Hungering Shade | +2 Damage, +5% IDG, +2% IDT, +2% LS |
| 3 | Brand of Oblivion, Umbral Claws, Unraveled Wards, Umbral Refuge | +5% IDG, +4% IDT, +2% DDT |
| 4 | Brand of Oblivion, Umbral Claws, Umbral Refuge, Veil of Nothing | +5% IDG, +2% IDT, +5% DDT |
| 5 | Brand of Oblivion, Umbral Claws, Umbral Refuge, Hungering Shade | +5% IDG, +2% IDT, +2% DDT, +2% LS |
| 6 | Brand of Oblivion, Umbral Claws, Hungering Shade, Maw of Oblivion | +8% IDG, +2% IDT, +5% LS |
| 7 | Brand of Oblivion, Unraveled Wards, Writ of Oblivion, Umbral Refuge | +2% IDG, +8% IDT, +4% DDT |
| 8 | Brand of Oblivion, Unraveled Wards, Umbral Refuge, Veil of Nothing | +2% IDG, +4% IDT, +5% DDT |
| 9 | Brand of Oblivion, Unraveled Wards, Umbral Refuge, Hungering Shade | +2% IDG, +4% IDT, +2% DDT, +2% LS |
| 10 | Brand of Oblivion, Umbral Refuge, Veil of Nothing, Sealed Against Ruin | +2% IDG, +2% IDT, +10% DDT |
| 11 | Brand of Oblivion, Umbral Refuge, Veil of Nothing, Hungering Shade | +2% IDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Brand of Oblivion, Umbral Refuge, Hungering Shade, Maw of Oblivion | +5% IDG, +2% IDT, +2% DDT, +5% LS |
| 13 | Unraveled Wards, Writ of Oblivion, Umbral Refuge, Veil of Nothing | +6% IDT, +7% DDT |
| 14 | Unraveled Wards, Umbral Refuge, Veil of Nothing, Sealed Against Ruin | +2% IDT, +10% DDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Pre-batch, Umbral Claws +2 / Absolute Erasure +3 Damage lifted Cursed Beast Form and Curse Empowerment 40 → 45 (a full tier) and Shadow Tether 50 → 55 (past the Nuke tier), and Umbral Claws alone took Tether to 52 as Writ of Oblivion's fourth purchase. First pass: all flat Damage removed and the route turned into +3% / +5% Increase Damage Given on Cursed Beast Form's one row, still labelled burst. Roster passes (R1′/R2): the dossier Traits line is "Burst, Sustained DPS", so Absolute Erasure returns to a controlled +2 Damage payoff (Tether 50 → 52, the 40 EP attacks 42) after Umbral Claws' unchanged +3% self-buff setup, the Blood-Enchanted Eyes pattern (RUL-2026-10-04-001/002), and drops its +5% Increase Damage Given. Names and graph are kept.
- Review rewire (first pass): with Absolute Erasure and Writ of Oblivion both under Brand of Oblivion, each route's offensive fourth was the other's Hidden Art. The tree uses the Blood-Enchanted Eyes graph: Brand of Oblivion parents Umbral Claws → Absolute Erasure (burst) and Hungering Shade → Maw of Oblivion (sustain offense); Umbral Refuge parents Veil of Nothing → Sealed Against Ruin (fortress) and Unraveled Wards → Writ of Oblivion (brand and hold). No capstone's sibling Hidden Art stacks its primary tag; Umbral Claws stacks only Maw of Oblivion's self-buff rider (43%).
- Burst setup: a self buff, not Blood-Enchanted Eyes' exposure setup. Unraveled Wards → Writ of Oblivion already owns Shadowrend's one exposure row, so the exposure identity stays with Writ; an Increase Damage Taken setup here would not stack with Unraveled Wards (each needs the other Foundation), but it would make Burst a second exposure route. Umbral Claws' 40% buff multiplies the +2 Damage the capstone adds, so the setup enlarges its own payoff.
- Damage tiers (R1′/R8/R9): Absolute Erasure's +2 is the tree's only flat Damage and sits on the Advanced Art. Cursed Beast Form and Curse Empowerment stay Normal (40 → 42); Shadow Tether goes 50 → 52, past the Nuke tier, recorded in above_nuke_rationale and director_review (DQ-A). No allocation crosses 40 → 45 or reaches 55.
- Value changes from the pre-batch tree: Umbral Claws +2 Damage → +3% Increase Damage Given and Absolute Erasure +3 → +2 Damage (Damage maximum +5 → +2); Unraveled Wards +3% → +2% and Writ of Oblivion +5% → +4% Increase Damage Taken, with Writ's +3% Increase Damage Given replaced by +2% Decrease Damage Taken; Sealed Against Ruin drops its +3% Increase Damage Given (a pure +10% fortress); Maw of Oblivion drops its +2% Decrease Damage Taken and keeps +3% Lifesteal / +3% Increase Damage Given (the earlier passes dropped the rider; review restored it). The rider is the anchors' sustain-offense pattern (Feast of the Fallen, The Storm's Due): Maw's path reaches the burst path's 40% self buff, and with Umbral Claws 43%, as The Storm's Due with Gathering Thunderhead (+10%) passes Sundered Sky's +8% path. Without it Maw + Umbral Claws was Absolute Erasure + Hungering Shade minus +2 Damage plus 3% Lifesteal.
- Writ of Oblivion's route carries +6% exposure (×1.044; +8%, ×1.059 with Brand) because exposure reaches every attacker's hits on the target, and it adds Surge reduction (+4%) so the brand-and-hold build is not weakly dominated alone: with the other Foundation as fourth, Absolute Erasure is ×1.40 × 1.37 ≈ ×1.92 on every window hit plus raw power ×1.05 on the 40 EP attacks (≈ ×2.01) and ×1.04 on Tether (≈ ×1.99), with 37% reduction; Writ is ×1.37 × 1.43 ≈ ×1.96 on every window hit, with 39% reduction, and its 43% exposure also multiplies allies' hits.
- Maxima over every legal allocation: Damage +2 (03), Increase Damage Given +8% (01+02+09+10), Increase Damage Taken +8% (01+06+04+05), Decrease Damage Taken +10% (06+07+08), Lifesteal +5% (01+09+10). Top offensive package (R14, Increase Damage Given × Taken, all windows live): ×1.075 (Maw + Umbral Claws, Writ + Brand); Absolute Erasure's ×1.052 with +2 Damage is ≈ ×1.105 on the 40 EP attacks and ≈ ×1.094 on Tether, under Blood-Enchanted Eyes' ×1.234 and its Rite route's ≈ ×1.19.
- Delivery: all five jutsu are cooldown 7; four are 60 AP, single target, range 4. Shadow Surge (40 AP, EMPTY_GROUND circle) realizes its Decrease Damage Taken and Lifesteal on the caster at cast time (actions.ts 980-1004). Rows are live the two rounds after their cast round, never in it (§3b): Surge plus Cursed Beast Form in one 100 AP round, Shadowrend next, then Shadow Tether puts all four windows on that strike. Absolute Erasure's +2 Damage is instant on every cast and needs no window.
- Fourth purchases: Absolute Erasure takes Umbral Refuge (37% reduction) or Hungering Shade (42% Lifesteal), neither touching the Damage rows, the buff or the exposure; Maw of Oblivion takes Umbral Claws (43% self buff; a 40 EP strike under both windows ×1.43 × 1.37 ≈ ×1.96) or Umbral Refuge (37% reduction, 40% buff); Sealed Against Ruin takes Brand of Oblivion (37% buff and exposure) or Unraveled Wards (37% exposure, strictly weaker); Writ of Oblivion takes Brand of Oblivion (43% exposure, 37% buff) or Veil of Nothing (42% reduction). The strongest solo strike in any legal allocation is Absolute Erasure's Curse Empowerment under both windows, ×1.05 × 1.40 × 1.37 ≈ ×2.01 (the first batch draft reached ×2.02 with the all-offense 01, 02, 03, 04).
- Ten nodes, one idea per route (burst: self-buff setup into +2 Damage; drain with a fed buff; fortress; brand and hold). Pierce (Shadowrend 58), wound, stun, clearprevent and move are unsupported.

## Risks and unproven interactions

- Classification: Shadow is shared with other bloodlines (expected under RUL-2026-10-03-005). 4 of 7 kit rows carry Shadow (the three Damage rows and Cursed Beast Form's buff); Shadowrend's exposure row needs the proposed jutsu-classification resolver, and Shadow Surge carries no element on any row, so in-kit it qualifies only through an authored Shadow jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Shadow coverage is unverified.
- Shadow Surge timing (§3b, §4b): its Decrease Damage Taken and Lifesteal are SELF rows realized on the caster at cast time and, like every modifier, skip the cast round: the 60 AP attack sharing Surge's 100 AP round is not lifestolen; hits dealt and taken in the two following rounds are covered.
- Lifesteal budget: the 60%-of-pre-shield-damage leech cap is shared with vamp; 45% leaves 15 points of headroom. Lifesteal includes pierce, so Shadowrend's 58 pierce feeds it inside Surge's window; healprevent on the caster blocks it.
- Exposure reach: Shadowrend's exposure (element-less, all four stat types) amplifies every non-pierce hit the target takes in the 2 rounds after the cast, from allies, weapons and normal jutsu too, so its group value exceeds its row count; it was not simulated. Same-tag effects from different casters all apply: two owners' 43% Shadowrend on one target make ×1.43 × 1.43 ≈ ×2.04 from exposure alone.
- Arithmetic (§3, §3b): the self buff and the exposure are separate stage-2 multipliers, so a strike under both takes ×1.40 × 1.37 ≈ ×1.92 on Absolute Erasure's route and at most ×1.43 × 1.37 ≈ ×1.96 on Maw of Oblivion's with Umbral Claws or Writ of Oblivion's with Brand (base ×1.35 × 1.35 ≈ ×1.82) before the bloodline passive (Increase Damage Given 25% + 0.15/level on Lightning, Fire, Shadow, None) multiplies last. Absolute Erasure's +2 Damage raises raw power first, so all of them scale it.
- Realized value: each window is live only the two rounds after its cast and cooldown 7 forbids recasting inside it; with one 60 AP attack per round a window covers at most two later kit attacks. Per-row numbers overstate per-round value.
- Damage reach: Absolute Erasure's +2 Damage is element-wide, so any other 50 EP Shadow jutsu the owner can cast (NORMAL/SPECIAL/EVENT/FORBIDDEN or injected) also reaches 52; off-kit Shadow coverage is unverified.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Shadow jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

