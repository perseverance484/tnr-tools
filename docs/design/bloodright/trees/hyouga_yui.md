# Hyouga Yui — Nine Hells Frozen

**Bloodline:** Hyouga Yui (BR-034, rank A, `lPcN4q0dtX2muWT2KlXGg`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Ice classification / forked tree · **Classification:** Ice (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Own Ice strikes landing harder (Permafrost Heart): crack them, then bury them (+3% exposure, then +3 Damage on Nine Hell's Spear 45 → 48, Glacial Shatter: Purgatory 45 → 48, Cerulean Storm: Avalanche 40 → 43 EP), or +10% on both self buffs (Avalanche, Glacier's Will) · secondary Control of the exchange (Cocytus Vigil): +10% exposure on Cocytus's target and Spear's circle, or +10% guard on Cocytus and Glacier's Will's tiles · tertiary A real Burst-or-Amplifier choice: with Cocytus Vigil as the fourth, the R1 Avalanche + Glacier's Will / R2 Spear + Cocytus / R3 Purgatory opener gives Burst 313.6 strike power against 312.2 and +6.7 to 7.5% on any strike outside a window, while the Amplifier takes ×1.104 on every other own hit inside it (×1.057 on a target holding Burst's 40% marks). Every capstone carries one tag.

Permafrost Heart answers "How do I make my Ice strikes land harder: crack them for heavier strikes, or stoke my own window?": Weight of the Avalanche marks Spear's circle and Cocytus's target and Buried in the Avalanche adds raw Damage to every strike on every cast; The Glacier Advances raises both 2-round self buffs. Cocytus Vigil answers "How do I control the exchange: open them to every blow, or shut us off from theirs?": Nine Hells Opened deepens both marks to 45%, Locked in Cocytus guards the caster and the allies on Glacier's Will's tiles. Flat Damage stops at +3 because the strikes sit at 45/45/40 EP and +5 would turn both 45s into 50 Nukes and the 40 into a 45. Wound, shield and move are unsupported. Potency reaches matching supported tags on all Ice jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Permafrost Heart | Foundation | How do I make my Ice strikes land harder: crack them for heavier strikes, or stoke my own window? |
| Cocytus Vigil | Foundation | How do I control the exchange: open them to every blow, or shut us off from theirs? |
| Buried in the Avalanche | Advanced Art | burst: exposure set up, then +3 raw Damage on all three circle strikes on every cast |
| The Glacier Advances | Advanced Art | sustained amplification: both self buffs compound on every own hit in the window |
| Nine Hells Opened | Advanced Art | exposure: a deep mark on Spear's circle and Cocytus's target that lifts allies' hits too |
| Locked in Cocytus | Advanced Art | fortress: pure guard for the caster under Cocytus and the party on Glacier's Will's tiles |

- Concern: Burst and the Amplifier are deliberately close: with Cocytus Vigil, the R1 Avalanche + Glacier's Will / R2 Spear + Cocytus / R3 Purgatory opener gives 313.6 against 312.2 strike power; Burst adds +6.7 to 7.5% on any strike outside a window and ×(1.40 / 1.37)² ≈ ×1.044 on allies' hits on a target holding both marks, the Amplifier ×1.104 on every other own hit in its window (×1.057 on a target holding Burst's marks). Not simulated.
- Concern: Buried in the Avalanche is a single +3 Damage step, one point above the exemplars' +2 payoffs, because +2 leaves Burst behind the Amplifier on the opener's strikes (306.9 against 312.2); it crosses no tier (48 / 48 / 43) and is the tree's only Damage.
- Concern: Two Hidden Arts print +3% Increase Damage Taken (Weight of the Avalanche as Burst's setup, Cracks in the Ice as Exposure's step); 01+02+06+07 reaches +8% without a capstone and is dominated by Exposure + Permafrost Heart.
- Concern: Both percentage pairs compound when cast in one turn (≈ ×2.10 at 45%), and Spear's exposure lifts allies' hits on every enemy in its circle; not simulated.
- Concern: Five of the nine supported rows depend on the proposed jutsu-classification resolver; off-kit Ice coverage is unverified.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ice jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Permafrost Heart | Foundation | None | +3% Increase Damage Given (self buff) | Cerulean Storm: Avalanche, Glacier's Will / 2 |
| 02 | Weight of the Avalanche | Hidden Art | Permafrost Heart | +3% Increase Damage Taken (enemy debuff) | Glacial Descent: Cocytus, Nine Hell's Spear / 2 |
| 03 | Buried in the Avalanche | Advanced Art | Weight of the Avalanche | +3 Damage (damage) | Cerulean Storm: Avalanche, Glacial Shatter: Purgatory, Nine Hell's Spear / 3 |
| 04 | Deepening Frost | Hidden Art | Permafrost Heart | +2% Increase Damage Given (self buff) | Cerulean Storm: Avalanche, Glacier's Will / 2 |
| 05 | The Glacier Advances | Advanced Art | Deepening Frost | +5% Increase Damage Given (self buff) | Cerulean Storm: Avalanche, Glacier's Will / 2 |
| 06 | Cocytus Vigil | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Taken (self buff) | Glacial Descent: Cocytus, Glacier's Will, Nine Hell's Spear / 4 |
| 07 | Cracks in the Ice | Hidden Art | Cocytus Vigil | +3% Increase Damage Taken (enemy debuff) | Glacial Descent: Cocytus, Nine Hell's Spear / 2 |
| 08 | Nine Hells Opened | Advanced Art | Cracks in the Ice | +5% Increase Damage Taken (enemy debuff) | Glacial Descent: Cocytus, Nine Hell's Spear / 2 |
| 09 | Rime Mantle | Hidden Art | Cocytus Vigil | +3% Decrease Damage Taken (self buff) | Glacial Descent: Cocytus, Glacier's Will / 2 |
| 10 | Locked in Cocytus | Advanced Art | Rime Mantle | +5% Decrease Damage Taken (self buff) | Glacial Descent: Cocytus, Glacier's Will / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Permafrost Heart** — The cold settles in the chest first. Everything after it strikes harder. Self damage buffs 35 → 38%: Avalanche's (Ice, Water, Wind and element-less hits) and Glacier's Will's (every non-pierce hit), live for the 2 rounds after each cast.
- **Weight of the Avalanche** — The snowpack settles on them before it falls. Nothing under it can brace. Exposure 35 → 38% (40% with Cocytus Vigil): Spear's circle against every non-pierce hit, Cocytus's target against element-less and highest-stat hits. The setup for Buried in the Avalanche: Spear's mark is live when Purgatory lands the next round.
- **Buried in the Avalanche** — No one digs out of the ninth winter. Damage +3 EP on the three Ice circle strikes: Spear and Purgatory 45 → 48, Avalanche 40 → 43 on every enemy in each circle, on every cast; no tier crossed.
- **Deepening Frost** — Frost does not stop at the skin. It keeps going down. Both self damage buffs 40% with Permafrost Heart; Avalanche's lands with its 60 AP strike, Glacier's Will's with its 40 AP ground cast.
- **The Glacier Advances** — A glacier moves a hand's width a day and nothing in its path survives the year. Amplifier route total +10%: both self buffs 35 → 45%, ×1.45 × 1.45 ≈ ×2.10 on own hits both cover in the two rounds after the casts.
- **Cocytus Vigil** — Keep watch over the frozen lake. What is held in it cannot strike back. Exposure 35 → 37% on Cocytus's target and Nine Hell's Spear's circle; guard 35 → 37% on Cocytus (self) and 30 → 32% on Glacier's Will's tiles.
- **Cracks in the Ice** — Every surface has a seam. The cold finds it and widens it. Exposure 40% with Cocytus Vigil: Spear's circle against every non-pierce hit; Cocytus's target against element-less hits and hits of the caster's highest offence stat.
- **Nine Hells Opened** — The spear does not close the wound it opens. It opens eight more. Exposure route total +10%, 35 → 45% for the two rounds after the cast: Spear's circle on every non-pierce hit from any attacker, allies' included; Cocytus's target on element-less hits and hits of the caster's highest offence stat.
- **Rime Mantle** — Rime thickens on the shoulders until blades skate off it. Guard 40% with Cocytus Vigil on Cocytus (self) and 35% on Glacier's Will's circle (caster and allies on the tiles).
- **Locked in Cocytus** — The lake freezes around both of you. Only one of you was ready for it. Fortress route total +10%: Cocytus 35 → 45% on the caster, Glacier's Will's tiles 30 → 40% for the caster and allies on them; ×0.55 × 0.60 = ×0.33 on non-pierce hits while both are live.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT |
|---|---|---:|---:|---:|---:|
| Buried in the Avalanche (Burst) | Permafrost Heart, Weight of the Avalanche, Buried in the Avalanche, Cocytus Vigil | +3 | +3% | +5% | +2% |
| The Glacier Advances (Amplifier) | Permafrost Heart, Deepening Frost, The Glacier Advances, Cocytus Vigil | — | +10% | +2% | +2% |
| Nine Hells Opened (Exposure) | Cocytus Vigil, Cracks in the Ice, Nine Hells Opened, Permafrost Heart | — | +3% | +10% | +2% |
| Locked in Cocytus (Fortress) | Cocytus Vigil, Rime Mantle, Locked in Cocytus, Cracks in the Ice | — | — | +5% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Buried in the Avalanche:** Weight of the Avalanche marks Spear's circle and Cocytus's target (40% with Cocytus Vigil), then +3 Damage lands on all three Ice circle strikes on every cast (Spear and Purgatory 45 → 48, Avalanche 40 → 43 EP). In the R1 Avalanche + Glacier's Will / R2 Spear + Cocytus / R3 Purgatory opener the strikes total 43 + 91.4 + 179.2 = 313.6, and any strike outside a window is +6.7 to 7.5% over the Amplifier. Cocytus Vigil is the fourth purchase (exposure 40%, guard 37% / 32%); Deepening Frost (self buffs 40%, 316.2 in the same opener) is the solo all-in.
- **The Glacier Advances:** Both self buffs 35 → 45%: cast together (Avalanche 60 AP + Glacier's Will 40 AP) they compound ×1.45 × 1.45 ≈ ×2.10 on own hits both cover for the next two rounds, strikes, weapons and normal jutsu alike; Avalanche's own hit takes neither. In the same opener the strikes total 40 + 94.6 + 177.6 = 312.2, and every other own hit in the window takes ×(1.45 / 1.38)² ≈ ×1.104 over Burst (×1.057 on a target holding Burst's 40% marks). Cocytus Vigil is the fourth purchase (exposure 37%, guard 37% / 32%); Weight of the Avalanche (exposure 38%, 314.8) is the alternative.
- **Nine Hells Opened:** Both exposures 35 → 45% for the two rounds after the cast: Spear marks every enemy in its circle against every non-pierce hit, Cocytus marks one target against element-less and highest-stat hits; on a target holding both, hits from the caster and allies compound ×1.45 × 1.45 ≈ ×2.10 (×(1.45 / 1.40)² ≈ ×1.073 over Burst's marks). Permafrost Heart is the fourth purchase (self buffs 38%); Rime Mantle (guard 40% / 35%) is the defensive alternative.
- **Locked in Cocytus:** Guard at the route maximum: Cocytus 45% on the caster, Glacier's Will's tiles 40% for the caster and allies on them, ×0.55 × 0.60 = ×0.33 on non-pierce hits while both are live. Cracks in the Ice is the fourth purchase: +5% IDT (both exposures 40%) beside that guard, the mirror of Exposure + Rime Mantle; Permafrost Heart (self buffs 38%, exposure 37%) is the alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Amplifier | Exposure | Fortress |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Glacial Descent: Cocytus | 0 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 45% (+10) | 40% (+5) |
| Glacial Descent: Cocytus | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 45% (+10) |
| Nine Hell's Spear | 0 | Damage | enemy | 45 | 48 (+3) | 45 | 45 | 45 |
| Nine Hell's Spear | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 45% (+10) | 40% (+5) |
| Nine Hell's Spear | 2 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Cerulean Storm: Avalanche | 0 | Damage | enemy | 40 | 43 (+3) | 40 | 40 | 40 |
| Cerulean Storm: Avalanche | 1 | Increase Damage Given | self | 35% | 38% (+3) | 45% (+10) | 38% (+3) | 35% |
| Glacial Shatter: Purgatory | 0 | Damage | enemy | 45 | 48 (+3) | 45 | 45 | 45 |
| Glacial Shatter: Purgatory | 1 | shield (unsupported) | self | 110 | 110 | 110 | 110 | 110 |
| Glacier's Will | 0 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |
| Glacier's Will | 1 | Increase Damage Given | self | 35% | 38% (+3) | 45% (+10) | 38% (+3) | 35% |
| Glacier's Will | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 13; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +3 Damage, +10% Increase Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Buried in the Avalanche: +3 Damage (0 + 0 + 3; off band)
  - Route The Glacier Advances: +10% Increase Damage Given (3 + 2 + 5; on band)
  - Route Nine Hells Opened: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Locked in Cocytus: +10% Decrease Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 3, DDT 2, IDG 2, IDT 2)
- Strongest full build by row-weighted total: Permafrost Heart, Cocytus Vigil, Cracks in the Ice, Nine Hells Opened (raw +15, row-weighted 30)
- Lowest row-weighted node: Deepening Frost (4)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +3 Damage |
|---|---:|---|---|
| Nine Hell's Spear | 0 | 45 (High) | 48 (High) |
| Cerulean Storm: Avalanche | 0 | 40 (Normal) | 43 (Normal) |
| Glacial Shatter: Purgatory | 0 | 45 (High) | 48 (High) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Buried in the Avalanche | +3 Damage, +3% IDG, +3% IDT | Deepening Frost | +3 Damage, +5% IDG, +3% IDT | 25 |
| Buried in the Avalanche | +3 Damage, +3% IDG, +3% IDT | Cocytus Vigil *(highest diagnostic)* | +3 Damage, +3% IDG, +5% IDT, +2% DDT | 29 |
| The Glacier Advances | +10% IDG | Weight of the Avalanche | +10% IDG, +3% IDT | 26 |
| The Glacier Advances | +10% IDG | Cocytus Vigil *(highest diagnostic)* | +10% IDG, +2% IDT, +2% DDT | 28 |
| Nine Hells Opened | +10% IDT, +2% DDT | Permafrost Heart | +3% IDG, +10% IDT, +2% DDT | 30 |
| Nine Hells Opened | +10% IDT, +2% DDT | Rime Mantle *(highest diagnostic)* | +10% IDT, +5% DDT | 30 |
| Locked in Cocytus | +2% IDT, +10% DDT | Permafrost Heart | +3% IDG, +2% IDT, +10% DDT | 30 |
| Locked in Cocytus | +2% IDT, +10% DDT | Cracks in the Ice *(highest diagnostic)* | +5% IDT, +10% DDT | 30 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Permafrost Heart, Weight of the Avalanche, Buried in the Avalanche, Deepening Frost | +3 Damage, +5% IDG, +3% IDT |
| 2 | Permafrost Heart, Weight of the Avalanche, Buried in the Avalanche, Cocytus Vigil | +3 Damage, +3% IDG, +5% IDT, +2% DDT |
| 3 | Permafrost Heart, Weight of the Avalanche, Deepening Frost, The Glacier Advances | +10% IDG, +3% IDT |
| 4 | Permafrost Heart, Weight of the Avalanche, Deepening Frost, Cocytus Vigil | +5% IDG, +5% IDT, +2% DDT |
| 5 | Permafrost Heart, Weight of the Avalanche, Cocytus Vigil, Cracks in the Ice | +3% IDG, +8% IDT, +2% DDT |
| 6 | Permafrost Heart, Weight of the Avalanche, Cocytus Vigil, Rime Mantle | +3% IDG, +5% IDT, +5% DDT |
| 7 | Permafrost Heart, Deepening Frost, The Glacier Advances, Cocytus Vigil | +10% IDG, +2% IDT, +2% DDT |
| 8 | Permafrost Heart, Deepening Frost, Cocytus Vigil, Cracks in the Ice | +5% IDG, +5% IDT, +2% DDT |
| 9 | Permafrost Heart, Deepening Frost, Cocytus Vigil, Rime Mantle | +5% IDG, +2% IDT, +5% DDT |
| 10 | Permafrost Heart, Cocytus Vigil, Cracks in the Ice, Nine Hells Opened | +3% IDG, +10% IDT, +2% DDT |
| 11 | Permafrost Heart, Cocytus Vigil, Cracks in the Ice, Rime Mantle | +3% IDG, +5% IDT, +5% DDT |
| 12 | Permafrost Heart, Cocytus Vigil, Rime Mantle, Locked in Cocytus | +3% IDG, +2% IDT, +10% DDT |
| 13 | Cocytus Vigil, Cracks in the Ice, Nine Hells Opened, Rime Mantle | +10% IDT, +5% DDT |
| 14 | Cocytus Vigil, Cracks in the Ice, Rime Mantle, Locked in Cocytus | +5% IDT, +10% DDT |

## Design notes

- Structure kept (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10). Routes: Burst sets up then pays off (Weight of the Avalanche +3% Increase Damage Taken, Buried in the Avalanche +3 Damage); Amplifier +10% Increase Damage Given (3 + 2 + 5); Exposure +10% Increase Damage Taken (2 + 3 + 5); Fortress +10% Decrease Damage Taken (2 + 3 + 5). Every capstone carries one tag. Maxima over every legal allocation: Damage +3, IDG +10%, IDT +10%, DDT +10%.
- Damage tiers: the strikes are 45 / 45 / 40 EP and all three are radius-1 area casts. +5 would make them 50 / 50 / 45 (two semi-nukes into Nukes, one Normal into High); +3 gives 48 / 48 / 43 and crosses nothing. Only Buried in the Avalanche carries Damage, so no other build borrows any.
- Why the Burst payoff is +3 in one step: the Amplifier's two self buffs compound, so its 45% against Permafrost Heart's 38% is worth ×(1.45 / 1.38)² ≈ ×1.104 on Spear and Purgatory inside the window. In the R1 Avalanche + Glacier's Will / R2 Spear + Cocytus / R3 Purgatory opener, both with Cocytus Vigil, a +2 payoff (47 / 47 / 42) totals 306.9 strike power against the Amplifier's 312.2, so Burst would trail on the opener's strikes as well as on every other own hit in the window; +3 totals 43 + 91.4 + 179.2 = 313.6 against 40 + 94.6 + 177.6 = 312.2.
- Weight of the Avalanche follows the Blood-Enchanted Eyes Burst pattern (exposure setup, raw-Damage payoff): Spear's mark is live when Purgatory lands. The most another route borrows from it is +3% IDT (Amplifier + Weight: exposure 38%).
- Fourth purchases: Burst takes Cocytus Vigil (exposure 40%, guard 37% / 32%) or Deepening Frost (self buffs 40%, 316.2 in the opener); Amplifier, Cocytus Vigil or Weight of the Avalanche (314.8); Exposure, Permafrost Heart or Rime Mantle; Fortress, Cracks in the Ice or Permafrost Heart. Fortress + Cracks in the Ice (+5% IDT, +10% DDT) mirrors Exposure + Rime Mantle (+10% IDT, +5% DDT). No fourth adds a second step on the capstone's own tag. The no-capstone 01+02+06+07 reaches +8% IDT and is dominated by Exposure + Permafrost Heart.
- Delivery (SOURCE_MECHANICS §3b, §4b): all cooldown 7. Strikes: 60 AP, range 4, radius-1 circle, friendly fire ENEMIES. Cocytus: 40 AP single target, exposure on the target and guard on the caster. Glacier's Will: 40 AP EMPTY_GROUND; self buff SELF, guard an INHERIT FRIENDLY ground circle re-applied each round to the caster and allies on the tiles. Buff and debuff rows are live in the two rounds after the cast round, never in it.

## Risks and unproven interactions

- Classification: element-wide Ice scope (RUL-2026-10-03-005); sharing Ice with other bloodlines is expected. 4 of the 9 supported rows carry Ice; Glacial Descent: Cocytus and Glacier's Will carry no Ice row and qualify in-kit only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Ice coverage is unverified.
- Self-buff stacking: Avalanche and Glacier's Will fit one 100 AP turn, so at 45% both compound to ×1.45 × 1.45 ≈ ×2.10 (×1.82 unbuffed) on hits both cover, before the 25% + 0.15/level passive applies last. Glacier's Will's row also reaches basic attacks, weapons and normal jutsu.
- Exposure reach: Spear's exposure (no element) raises every non-pierce hit on every enemy in its circle, from any attacker; Cocytus's raises element-less hits and hits of the caster's highest offence stat. Spear and Cocytus fit one turn, so one target can carry ×1.45 × 1.45 ≈ ×2.10 for two rounds.
- Guard scale: Cocytus 45% and Glacier's Will 40% apply in sequence, ×0.55 × 0.60 = ×0.33 (×0.46 unbuffed) on non-pierce hits while both are live. The ground guard is positional and also covers allies on the tiles.
- Ally hazard: none on supported rows (strikes and Spear's exposure are friendly fire ENEMIES; Glacier's Will's supported rows are SELF or FRIENDLY). Spear's wound and Glacier's Will's move are the kit's only hazard rows; both are unsupported.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed; balance values remain director-owned.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Ice jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

