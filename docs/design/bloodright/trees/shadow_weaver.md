# Shadow Weaver — Threads of Night

**Bloodline:** Shadow Weaver (BR-063, rank A, `d0WYPbbsVx7Y_i0fddwxc`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Shadow classification / forked tree · **Classification:** Shadow (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst from Loom of Dusk: Increase Damage Given setup on three stacking self buffs, paid off with a controlled +2 Damage on four 40 EP Shadow attacks · secondary Fortress on Shadow Shell's Decrease Damage Taken (+10%) and Suppression on Shadow Severance's Decrease Damage Given (+10%) · tertiary Increase Damage Given outside Burst: a +2% rider on the Fortress and the Umbral Whetstone lean.

Shadow Weaver is a rank-A Bukijutsu Sustained DPS kit: four 40 EP Shadow attacks (Domain, Severance, Step, Dance; 60 AP, cooldown 7) and three 35% self Increase Damage Given buffs (Domain, Step, Shell) that compound when their windows overlap. The old +5 Damage route lifted all four attacks 40 → 45, a full tier each; Burst now sharpens the buffs on the Hidden Art and pays off with +2 Damage (40 → 42) on the capstone. Loom of Dusk answers "How do I win the exchange: strike harder or blunt their strikes?" (Burst or Suppression on Severance); Cloak of Woven Night answers "How do I fight from inside my own weave: thicken it or sharpen it?" (Fortress on Shell or the Umbral Whetstone buff lean). No Afterburn, Lifesteal, Reflect, Heal or Increase Damage Taken row exists, so none is invented. Potency reaches matching supported tags on all Shadow jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Loom of Dusk | Foundation | How do I win the exchange: strike harder or blunt their strikes? |
| Cloak of Woven Night | Foundation | How do I fight from inside my own weave: thicken it or sharpen it? |
| Night Unraveled | Advanced Art | burst: sharpened self buffs into a controlled raw-Damage payoff |
| Strings Cut Short | Advanced Art | suppression: sever one enemy's offense |
| Seamless Shroud | Advanced Art | fortress: armour inside Shadow Shell |

- Concern: Increase Damage Given rises from a +5% maximum to +7% (Loom of Dusk, Barbed Thread, Cloak of Woven Night, Umbral Whetstone) and +6% on the Burst route; it is the tree's highest-leverage tag because the three self buffs compound (×1.42³ ≈ ×2.86 against ×2.46 when all three windows overlap).
- Concern: Burst trades raw Damage for buff leverage: over one assumed rotation (Shell with Domain, then Step, Severance, Dance) it is estimated at about +14% against about +16% for the old +5 Damage route, with no tier jump (not simulated). If the director wants Burst to read as raw burst, +3 Damage on Night Unraveled (40 → 43, still Normal) instead of its +2% Increase Damage Given is the alternative.
- Concern: Suppression and Fortress each rest on one element-less row that the current resolver cannot reach (G1).

> **Narrow-kit exception:** Nine nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on nine rows (Damage x4, Increase Damage Given x3, Decrease Damage Given x1, Decrease Damage Taken x1). Burst takes Damage with Increase Damage Given as its setup, Suppression takes Decrease Damage Given and Fortress takes Decrease Damage Taken. A fourth capstone could only be a second Increase Damage Given route, which would read as Burst without the Damage and would let a capstone plus a sibling Hidden Art stack three compounding self buffs. Umbral Whetstone is a leaf so that the defensive root completes a full build (06, 07, 08, 09) without Loom of Dusk; it is +3% while Barbed Thread is +2% because Barbed Thread's value is the route behind it.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Loom of Dusk | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Given (enemy debuff) | Shadow Domain, Shadow Severance, Shadow Shell, Shadow Step / 4 |
| 02 | Barbed Thread | Hidden Art | Loom of Dusk | +2% Increase Damage Given (self buff) | Shadow Domain, Shadow Shell, Shadow Step / 3 |
| 03 | Night Unraveled | Advanced Art | Barbed Thread | +2 Damage (damage); +2% Increase Damage Given (self buff) | Shadow Dance, Shadow Domain, Shadow Severance, Shadow Shell, Shadow Step / 7 |
| 04 | Frayed Resolve | Hidden Art | Loom of Dusk | +3% Decrease Damage Given (enemy debuff) | Shadow Severance / 1 |
| 05 | Strings Cut Short | Advanced Art | Frayed Resolve | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff) | Shadow Severance, Shadow Shell / 2 |
| 06 | Cloak of Woven Night | Foundation | None | +3% Decrease Damage Taken (self buff) | Shadow Shell / 1 |
| 07 | Tightened Weave | Hidden Art | Cloak of Woven Night | +3% Decrease Damage Taken (self buff) | Shadow Shell / 1 |
| 08 | Seamless Shroud | Advanced Art | Tightened Weave | +4% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Shadow Domain, Shadow Shell, Shadow Step / 4 |
| 09 | Umbral Whetstone | Hidden Art | Cloak of Woven Night | +3% Increase Damage Given (self buff) | Shadow Domain, Shadow Shell, Shadow Step / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Loom of Dusk** — Every thread the weaver draws tight is a thread pulled loose from the foe. Domain, Step and Shell self buffs 35 → 37% (2 rounds); Severance's Decrease Damage Given 30 → 32% on every non-pierce hit the target deals.
- **Barbed Thread** — Every strand the weaver wears grows a barb. Setup: Domain, Step and Shell self buffs 37 → 39% with Loom of Dusk, live the 2 rounds after each cast. All three raise the kit's Shadow Bukijutsu attacks and element-less hits; Domain's and Step's also raise Fire, Lightning and other Shadow hits.
- **Night Unraveled** — Pull the last thread and the dark comes apart in their hands. Burst payoff: Domain, Severance, Step and Dance 40 → 42 EP (no tier change); self buffs 35 → 41% on the full route, so a strike under all three windows lands at ×1.41³ ≈ ×2.80 instead of ×2.46.
- **Frayed Resolve** — Cut enough strands and even the strongest arm swings hollow. Severance's Decrease Damage Given +3% (35% with Loom of Dusk); 2 rounds per cast; pierce excluded.
- **Strings Cut Short** — Cut the strings and the blow dies before it lands. Suppression: Severance 30 → 40% Decrease Damage Given on the full route (+10%), on every non-pierce hit the target deals for 2 rounds; Shadow Shell's Decrease Damage Taken 35 → 37%.
- **Cloak of Woven Night** — Darkness pulled close enough becomes armor. Shadow Shell's self Decrease Damage Taken 35 → 38% (2 rounds per 40 AP cast); every non-pierce hit taken.
- **Tightened Weave** — No gap between the threads; no gap for a blade. Shadow Shell's Decrease Damage Taken +3% (41% with Cloak of Woven Night).
- **Seamless Shroud** — Wrapped so tight that nothing enters, and nothing dulls the edge inside. Fortress: Shadow Shell 35 → 45% Decrease Damage Taken on the full route (+10%); Domain, Step and Shell self buffs +2% (37%, or 40% with Umbral Whetstone).
- **Umbral Whetstone** — Steel honed on shadow keeps its edge long after the light is gone. Domain, Step and Shell self buffs +3% (38%; 40% with Loom of Dusk or Seamless Shroud, 42% with Loom of Dusk and Barbed Thread, the tree's maximum); no capstone follows.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT |
|---|---|---:|---:|---:|---:|
| Night Unraveled (Burst) | Loom of Dusk, Barbed Thread, Night Unraveled, Cloak of Woven Night | +2 | +6% | +2% | +3% |
| Strings Cut Short (Suppression) | Loom of Dusk, Frayed Resolve, Strings Cut Short, Cloak of Woven Night | — | +2% | +10% | +5% |
| Seamless Shroud (Fortress) | Cloak of Woven Night, Tightened Weave, Seamless Shroud, Umbral Whetstone | — | +5% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Night Unraveled:** Self buffs 35 → 41% (Loom 2, Barbed 2, Night 2) and all four Shadow attacks 40 → 42 EP; under all three windows a strike lands at about ×1.20 of its unenhanced value (×1.14 from the buffs, ×1.05 from the Damage). Cloak of Woven Night is the fourth purchase for a 38% Shell; Frayed Resolve (01, 02, 03, 04) is the all-offense alternative with a 35% sever.
- **Strings Cut Short:** Severance's Decrease Damage Given 30 → 40%, so for two rounds the target's non-pierce hits land at ×0.60 instead of ×0.70; Cloak of Woven Night with the capstone's +2% puts Shell at 40%. Barbed Thread (01, 02, 04, 05) is the offensive fourth: self buffs 39% instead of the Cloak.
- **Seamless Shroud:** Shadow Shell's Decrease Damage Taken 35 → 45%, so hits in its window land at ×0.55 instead of ×0.65; Umbral Whetstone with the capstone's +2% lifts the three self buffs to 40% without the offensive root. Loom of Dusk (01, 06, 07, 08) is the alternative fourth: 39% buffs plus a 32% sever.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Suppression | Fortress |
|---|---:|---|---|---:|---:|---:|---:|
| Shadow Domain | 0 | Increase Damage Given | self | 35% | 41% (+6) | 37% (+2) | 40% (+5) |
| Shadow Domain | 1 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Shadow Domain | 2 | clearprevent (unsupported) | self | 100 | 100 | 100 | 100 |
| Shadow Severance | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Shadow Severance | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 30% |
| Shadow Severance | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 |
| Shadow Step | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Shadow Step | 1 | Increase Damage Given | self | 35% | 41% (+6) | 37% (+2) | 40% (+5) |
| Shadow Step | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Shadow Shell | 0 | Increase Damage Given | self | 35% | 41% (+6) | 37% (+2) | 40% (+5) |
| Shadow Shell | 1 | Decrease Damage Taken | self | 35% | 38% (+3) | 40% (+5) | 45% (+10) |
| Shadow Shell | 2 | visual (unsupported) **adverse** | self | 1 | 1 | 1 | 1 |
| Shadow Dance | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Shadow Dance | 1 | copy (unsupported) | enemy | 100% | 100% | 100% | 100% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 9, 4: 12
- Full-budget allocations: 12; numerically non-dominated (per-tag totals): 10; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +7% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Night Unraveled: +2 Damage (0 + 0 + 2; off band)
  - Route Strings Cut Short: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Seamless Shroud: +10% Decrease Damage Taken (3 + 3 + 4; on band)
- Supported rows in kit: 9 (DMG 4, DDG 1, DDT 1, IDG 3)
- Strongest full build by row-weighted total: Loom of Dusk, Barbed Thread, Night Unraveled, Frayed Resolve (raw +13, row-weighted 31)
- Lowest row-weighted node: Frayed Resolve (3)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Shadow Domain | 1 | 40 (Normal) | 42 (Normal) |
| Shadow Severance | 0 | 40 (Normal) | 42 (Normal) |
| Shadow Step | 0 | 40 (Normal) | 42 (Normal) |
| Shadow Dance | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Night Unraveled | +2 Damage, +6% IDG, +2% DDG | Frayed Resolve | +2 Damage, +6% IDG, +5% DDG | 31 |
| Night Unraveled | +2 Damage, +6% IDG, +2% DDG | Cloak of Woven Night *(highest diagnostic)* | +2 Damage, +6% IDG, +2% DDG, +3% DDT | 31 |
| Strings Cut Short | +2% IDG, +10% DDG, +2% DDT | Barbed Thread *(highest diagnostic)* | +4% IDG, +10% DDG, +2% DDT | 24 |
| Strings Cut Short | +2% IDG, +10% DDG, +2% DDT | Cloak of Woven Night | +2% IDG, +10% DDG, +5% DDT | 21 |
| Seamless Shroud | +2% IDG, +10% DDT | Loom of Dusk | +4% IDG, +2% DDG, +10% DDT | 24 |
| Seamless Shroud | +2% IDG, +10% DDT | Umbral Whetstone *(highest diagnostic)* | +5% IDG, +10% DDT | 25 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Loom of Dusk, Barbed Thread, Night Unraveled, Frayed Resolve | +2 Damage, +6% IDG, +5% DDG |
| 2 | Loom of Dusk, Barbed Thread, Night Unraveled, Cloak of Woven Night | +2 Damage, +6% IDG, +2% DDG, +3% DDT |
| 3 | Loom of Dusk, Barbed Thread, Frayed Resolve, Strings Cut Short | +4% IDG, +10% DDG, +2% DDT |
| 4 | Loom of Dusk, Barbed Thread, Frayed Resolve, Cloak of Woven Night | +4% IDG, +5% DDG, +3% DDT |
| 5 | Loom of Dusk, Barbed Thread, Cloak of Woven Night, Tightened Weave | +4% IDG, +2% DDG, +6% DDT |
| 6 | Loom of Dusk, Barbed Thread, Cloak of Woven Night, Umbral Whetstone | +7% IDG, +2% DDG, +3% DDT |
| 7 | Loom of Dusk, Frayed Resolve, Strings Cut Short, Cloak of Woven Night | +2% IDG, +10% DDG, +5% DDT |
| 8 | Loom of Dusk, Frayed Resolve, Cloak of Woven Night, Tightened Weave | +2% IDG, +5% DDG, +6% DDT |
| 9 | Loom of Dusk, Frayed Resolve, Cloak of Woven Night, Umbral Whetstone | +5% IDG, +5% DDG, +3% DDT |
| 10 | Loom of Dusk, Cloak of Woven Night, Tightened Weave, Seamless Shroud | +4% IDG, +2% DDG, +10% DDT |
| 11 | Loom of Dusk, Cloak of Woven Night, Tightened Weave, Umbral Whetstone | +5% IDG, +2% DDG, +6% DDT |
| 12 | Cloak of Woven Night, Tightened Weave, Seamless Shroud, Umbral Whetstone | +5% IDG, +10% DDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Kept: graph, names, both Foundations, Frayed Resolve, the Fortress line and Umbral Whetstone. Changed: Barbed Thread +2 Damage → +2% Increase Damage Given; Night Unraveled +3 Damage → +2 Damage, +2% Increase Damage Given; Strings Cut Short's +3% Increase Damage Given rider → +2% Decrease Damage Taken. The old +5 Damage route lifted Domain, Severance, Step and Dance 40 → 45 (four Normal → High tier jumps), and Damage on the Hidden Art made +2 Damage the obvious fourth purchase for Suppression.
- Maxima over every legal allocation: Damage +2 (40 → 42, no tier change), Increase Damage Given +7% (Loom of Dusk, Barbed Thread, Cloak of Woven Night, Umbral Whetstone: no capstone), Decrease Damage Given +10%, Decrease Damage Taken +10%.
- Impact: the three self buffs are jutsu-sourced and multiply in sequence (§3b): ×1.35³ ≈ ×2.46 unenhanced, ×1.41³ ≈ ×2.80 on the Burst route (+14%), ×1.42³ ≈ ×2.86 at the +7% maximum (+16%); a single window gains only +4 to +5%. Burst's +2 Damage multiplies under the same windows, about ×1.20 with all three live. Fortress cuts hits in Shell's window from ×0.65 to ×0.55 (−15%); Suppression cuts the Severed target's hits from ×0.70 to ×0.60 (−14%). The bloodline passive (Increase Damage Given on Fire, Lightning, Shadow and element-less hits) multiplies last.
- Reach: Domain's and Step's buff rows list Fire, Lightning, Shadow and None, so they also raise Fire and Lightning jutsu, basic attacks and other element-less hits; Shell's buff is element-less (its Bukijutsu filter is not binding). Severance's Decrease Damage Given and Shell's Decrease Damage Taken list all four stat types and no element, so each covers every non-pierce hit the target deals or the caster takes in its window.
- Delivery: all five jutsu are cooldown 7; buffs and debuffs are live the two rounds after the cast and never in the cast round (§3b), so Domain's and Step's buffs never raise their own hit. Domain (GROUND spiral) and Step (EMPTY_GROUND circle) carry SELF buff rows realized on the caster at cast; their damage rows are friendly fire ENEMIES, so no supported row is an ally hazard.
- Fourth purchases: Burst takes Cloak of Woven Night (Shell 38%) or Frayed Resolve (Severance 35%); Suppression takes Barbed Thread (buffs 39%) or Cloak of Woven Night (Shell 40%); Fortress takes Umbral Whetstone (buffs 40%) or Loom of Dusk (buffs 39%, Severance 32%). No fourth adds Damage, and none adds the route's own primary tag. Two full allocations are dominated (Barbed Thread without Night Unraveled loses to Umbral Whetstone in the same slot).

## Risks and unproven interactions

- Classification: Shadow is the single qualifying element; sharing it with other bloodlines is expected (RUL-2026-10-03-005). 6 of 9 kit rows carry Shadow; Severance's Decrease Damage Given and both Shell rows carry no element, so Suppression and Fortress depend wholly on the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Shadow coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN) is unverified.
- Off-kit Damage: +2 Damage reaches every Shadow Damage row the caster can use; an off-kit Shadow jutsu at 50 would become 52. No off-kit catalog exists to check.
- Increase Damage Given is the high-leverage tag: one +1% lifts three compounding windows, and Domain's and Step's rows also raise Fire, Lightning and element-less hits. The +7% maximum needs no capstone; combined final damage was not simulated.
- Uptime: every buff and debuff window is 2 rounds on a cooldown-7 cast, so Shell's 45% and Severance's 40% are live at most two rounds in seven.
- Shadow Step's move row is unsupported and flagged enemy-hazard (positive ground row, friendly fire none); no node changes it. No supported row is adverse, ally-hazard or enemy-hazard.
- Loom of Dusk is in 11 of 12 legal full allocations; only the Fortress build with Umbral Whetstone skips it.
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

