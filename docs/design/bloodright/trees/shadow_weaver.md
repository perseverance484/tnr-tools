# Shadow Weaver — Threads of Night

**Bloodline:** Shadow Weaver (BR-063, rank A, `d0WYPbbsVx7Y_i0fddwxc`) · **Revision:** Draft 2 / Shadow classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Shadow (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (four 40-power Shadow Bukijutsu attacks; +5 Damage route) · secondary Increase Damage Given glue on three stacking self buffs (Domain, Step, Shell; +5% at most) · tertiary Decrease Damage Given (Severance, +10% route) and Decrease Damage Taken (Shell, +10% route).

Shadow Weaver is a rank-A Bukijutsu Sustained DPS kit: four of its nine supported rows are 40-power Shadow attacks (Domain, Severance, Step and Dance, all 60 AP / cooldown 7), so the Damage route is the deepest offensive commitment. Three rows are 35% self Increase Damage Given buffs, the kit's sustained-damage identity; they stack with each other and with the bloodline's own Increase Damage Given passive, so they stay glue at +5% at most. Severance's 30% Decrease Damage Given and Shell's 35% Decrease Damage Taken anchor the Suppression and Fortress routes at +10% each. No Afterburn, Lifesteal, Reflect, Heal or Increase Damage Taken row exists, so none is invented. Potency reaches matching supported tags on all Shadow jutsu (RUL-2026-10-03-005).

> **Narrow-kit exception:** Nine nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on nine rows (Damage x4, Increase Damage Given x3, Decrease Damage Given x1, Decrease Damage Taken x1); Damage, Decrease Damage Given and Decrease Damage Taken each get a route. Increase Damage Given is the only tag left for a fourth route and is deliberately kept as glue at +5% at most: its three 35% self buffs stack with each other and with the bloodline's Increase Damage Given passive, and Domain's and Step's rows also raise Fire, Lightning and element-less hits, so a dedicated route toward +10% would lift three overlapping buffs at once. Any other fourth capstone would restate the Damage, Decrease Damage Given or Decrease Damage Taken capstones under a new name. Umbral Whetstone exists so that the defensive root completes a full build (06, 07, 08, 09) without Loom of Dusk; it is +3% while Seamless Shroud's secondary is +2% so that build is not dominated by 01, 06, 07, 08. Three distinct complete builds exist, one per Advanced Art.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Loom of Dusk | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Given (enemy debuff) | Shadow Domain, Shadow Severance, Shadow Shell, Shadow Step / 4 |
| 02 | Barbed Thread | Hidden Art | Loom of Dusk | +2 Damage (damage) | Shadow Dance, Shadow Domain, Shadow Severance, Shadow Step / 4 |
| 03 | Night Unraveled | Advanced Art | Barbed Thread | +3 Damage (damage) | Shadow Dance, Shadow Domain, Shadow Severance, Shadow Step / 4 |
| 04 | Frayed Resolve | Hidden Art | Loom of Dusk | +3% Decrease Damage Given (enemy debuff) | Shadow Severance / 1 |
| 05 | Strings Cut Short | Advanced Art | Frayed Resolve | +5% Decrease Damage Given (enemy debuff); +3% Increase Damage Given (self buff) | Shadow Domain, Shadow Severance, Shadow Shell, Shadow Step / 4 |
| 06 | Cloak of Woven Night | Foundation | None | +3% Decrease Damage Taken (self buff) | Shadow Shell / 1 |
| 07 | Tightened Weave | Hidden Art | Cloak of Woven Night | +3% Decrease Damage Taken (self buff) | Shadow Shell / 1 |
| 08 | Seamless Shroud | Advanced Art | Tightened Weave | +4% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Shadow Domain, Shadow Shell, Shadow Step / 4 |
| 09 | Umbral Whetstone | Hidden Art | Cloak of Woven Night | +3% Increase Damage Given (self buff) | Shadow Domain, Shadow Shell, Shadow Step / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Loom of Dusk** — Every thread the weaver draws tight is a thread pulled loose from the foe. Domain, Step and Shell self buffs 35 → 37% (2 rounds); Severance's Decrease Damage Given 30 → 32% on every non-pierce hit the target deals.
- **Barbed Thread** — The strand that binds also bites. Domain, Severance, Step and Dance 40 → 42 EP (Shadow, Bukijutsu). Domain's spiral and Step's circle strike enemies only.
- **Night Unraveled** — Pull the last thread and the dark comes apart in their hands. Same four Shadow Damage rows: 40 → 45 EP on the full route (+5 Damage).
- **Frayed Resolve** — Cut enough strands and even the strongest arm swings hollow. Severance's Decrease Damage Given +3% (35% with Loom of Dusk); 2 rounds per cast; pierce excluded.
- **Strings Cut Short** — Their strikes end before they begin; yours never stop. Suppression: Severance 30 → 40% Decrease Damage Given on the full route (+10%); Domain, Step and Shell self buffs +3% (40% with Loom of Dusk).
- **Cloak of Woven Night** — Darkness pulled close enough becomes armor. Shadow Shell's self Decrease Damage Taken 35 → 38% (2 rounds per 40 AP cast); every non-pierce hit taken.
- **Tightened Weave** — No gap between the threads; no gap for a blade. Shadow Shell's Decrease Damage Taken +3% (41% with Cloak of Woven Night).
- **Seamless Shroud** — Wrapped so tight that nothing enters, and nothing dulls the edge inside. Fortress: Shadow Shell 35 → 45% Decrease Damage Taken on the full route (+10%); Domain, Step and Shell self buffs +2% (37%, or 40% with Umbral Whetstone).
- **Umbral Whetstone** — Steel honed on shadow keeps its edge long after the light is gone. Domain, Step and Shell self buffs +3% (38%; 40% with Loom of Dusk or Seamless Shroud); Fire, Lightning, Shadow and element-less hits.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT |
|---|---|---:|---:|---:|---:|
| Night Unraveled (Burst) | Loom of Dusk, Barbed Thread, Night Unraveled, Cloak of Woven Night | +5 | +2% | +2% | +3% |
| Strings Cut Short (Suppression) | Loom of Dusk, Frayed Resolve, Strings Cut Short, Cloak of Woven Night | — | +5% | +10% | +3% |
| Seamless Shroud (Fortress) | Cloak of Woven Night, Tightened Weave, Seamless Shroud, Umbral Whetstone | — | +5% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Night Unraveled:** +5 Damage on all four Shadow attacks (Domain, Severance, Step and Dance 40 → 45 EP), framed by Loom of Dusk's 37% self buffs and 32% sever. Cloak of Woven Night is the fourth purchase for a 38% Shell; Frayed Resolve (01, 02, 03, 04) is the all-offense alternative with a 35% sever and no mitigation.
- **Strings Cut Short:** Severance's Decrease Damage Given rises to 40% (+10%), so for two rounds every non-pierce hit the target deals is cut by two fifths, while the capstone's +3% with Loom of Dusk lifts all three self buffs to 40%. Cloak of Woven Night adds a 38% Shell for a durable duelist; Barbed Thread (01, 02, 04, 05) trades that for +2 Damage on the four attacks.
- **Seamless Shroud:** Shell's Decrease Damage Taken reaches 45% (+10%) on every non-pierce hit taken, and Umbral Whetstone with the capstone's +2% lifts the Domain, Step and Shell buffs to 40% without touching the offensive root. Loom of Dusk (01, 06, 07, 08) is the alternative fourth purchase: 39% buffs plus a 32% sever instead of 40% buffs.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Suppression | Fortress |
|---|---:|---|---|---:|---:|---:|---:|
| Shadow Domain | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) |
| Shadow Domain | 1 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Shadow Domain | 2 | clearprevent (unsupported) | self | 100 | 100 | 100 | 100 |
| Shadow Severance | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Shadow Severance | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 30% |
| Shadow Severance | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 |
| Shadow Step | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Shadow Step | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) |
| Shadow Step | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Shadow Shell | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) |
| Shadow Shell | 1 | Decrease Damage Taken | self | 35% | 38% (+3) | 38% (+3) | 45% (+10) |
| Shadow Shell | 2 | visual (unsupported) **adverse** | self | 1 | 1 | 1 | 1 |
| Shadow Dance | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Shadow Dance | 1 | copy (unsupported) | enemy | 100% | 100% | 100% | 100% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 9, 4: 12
- Full-budget allocations: 12; numerically non-dominated (per-tag totals): 11; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Night Unraveled: +5 Damage (0 + 2 + 3; on band)
  - Route Strings Cut Short: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Seamless Shroud: +10% Decrease Damage Taken (3 + 3 + 4; on band)
- Supported rows in kit: 9 (DMG 4, DDG 1, DDT 1, IDG 3)
- Strongest full build by row-weighted total: Loom of Dusk, Barbed Thread, Frayed Resolve, Strings Cut Short (raw +17, row-weighted 33)
- Lowest row-weighted node: Frayed Resolve (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Loom of Dusk, Barbed Thread, Night Unraveled, Frayed Resolve | +5 Damage, +2% IDG, +5% DDG |
| 2 | Loom of Dusk, Barbed Thread, Night Unraveled, Cloak of Woven Night | +5 Damage, +2% IDG, +2% DDG, +3% DDT |
| 3 | Loom of Dusk, Barbed Thread, Frayed Resolve, Strings Cut Short | +2 Damage, +5% IDG, +10% DDG |
| 4 | Loom of Dusk, Barbed Thread, Frayed Resolve, Cloak of Woven Night | +2 Damage, +2% IDG, +5% DDG, +3% DDT |
| 5 | Loom of Dusk, Barbed Thread, Cloak of Woven Night, Tightened Weave | +2 Damage, +2% IDG, +2% DDG, +6% DDT |
| 6 | Loom of Dusk, Barbed Thread, Cloak of Woven Night, Umbral Whetstone | +2 Damage, +5% IDG, +2% DDG, +3% DDT |
| 7 | Loom of Dusk, Frayed Resolve, Strings Cut Short, Cloak of Woven Night | +5% IDG, +10% DDG, +3% DDT |
| 8 | Loom of Dusk, Frayed Resolve, Cloak of Woven Night, Tightened Weave | +2% IDG, +5% DDG, +6% DDT |
| 9 | Loom of Dusk, Frayed Resolve, Cloak of Woven Night, Umbral Whetstone | +5% IDG, +5% DDG, +3% DDT |
| 10 | Loom of Dusk, Cloak of Woven Night, Tightened Weave, Seamless Shroud | +4% IDG, +2% DDG, +10% DDT |
| 11 | Loom of Dusk, Cloak of Woven Night, Tightened Weave, Umbral Whetstone | +5% IDG, +2% DDG, +6% DDT |
| 12 | Cloak of Woven Night, Tightened Weave, Seamless Shroud, Umbral Whetstone | +5% IDG, +10% DDT |

## Design notes

- Routes: Burst +5 Damage (Barbed Thread +2, Night Unraveled +3); Suppression +10% Decrease Damage Given (Loom of Dusk +2%, Frayed Resolve +3%, Strings Cut Short +5%); Fortress +10% Decrease Damage Taken (Cloak of Woven Night +3%, Tightened Weave +3%, Seamless Shroud +4%). Increase Damage Given glue (Loom of Dusk +2%, Strings Cut Short +3%, Seamless Shroud +2%, Umbral Whetstone +3%) peaks at +5% in any legal allocation. Cloak of Woven Night carries no Damage, so no allocation exceeds +5 Damage.
- Reach: Domain's and Step's buff rows list Fire, Lightning, Shadow and None, so a 40% buff also raises Fire and Lightning jutsu, basic attacks and non-elemental hits; Shell's buff is element-less (its Bukijutsu filter is not binding) and reaches every element-less hit of any stat type. Severance's Decrease Damage Given and Shell's Decrease Damage Taken list all four stat types with no element, so they cover every non-pierce hit the target deals or the caster takes for 2 rounds; both are buff/debuff-prevent gated.
- Delivery: all five jutsu are cooldown 7. Domain (GROUND spiral) and Step (EMPTY_GROUND circle) carry SELF buff rows realized on the caster at cast time; their damage rows are friendly fire ENEMIES, so no supported row is an ally hazard. Whether a cast's own damage row benefits from the buff that same cast applies was not verified.
- Fourth purchases: Burst takes Cloak of Woven Night (Shell 38%) or Frayed Resolve (Severance 35%); Suppression takes Cloak of Woven Night or Barbed Thread (+2 Damage); Fortress takes Umbral Whetstone (buffs 40%) or Loom of Dusk (buffs 39%, Severance 32%). Twelve legal full-budget allocations exist; 01, 04, 06, 09 is the one dominated allocation (Strings Cut Short beats Umbral Whetstone as its fourth purchase).

## Risks and unproven interactions

- Classification: Shadow is the single qualifying element; sharing it with other bloodlines is expected (RUL-2026-10-03-005). 6 of 9 kit rows carry Shadow; the element-less rows need the proposed jutsu-classification resolver, and Shadow Shell carries no Shadow row, so in-kit it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Shadow coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN) is unverified.
- Damage reach: +5 Damage lands on four 40-power rows (45 EP each); every attack costs 60 AP on cooldown 7, so the per-rotation gain depends on how many are cast. Values are raw power before the Bukijutsu formula.
- Increase Damage Given stacking: the three self buffs all match the kit's Shadow Bukijutsu attacks and compound when their windows overlap (×1.35³ ≈ ×2.46 at base, ×1.40³ ≈ ×2.74 at the +5% maximum), with main-tree or gear modifiers in the same pipeline and the bloodline passive multiplying last; Shell's element-less row also raises weapons and basic attacks. Combined final damage was not simulated.
- Uptime: every buff and debuff window is 2 rounds on a cooldown-7 cast, so Shell's 45% and Severance's 40% are live at most two rounds in seven and per-row figures overstate per-round value.
- Shadow Step's move row is unsupported and flagged enemy-hazard (positive ground row, friendly fire none); no node changes it. No supported row is adverse, ally-hazard or enemy-hazard.
- Nine-node tree: Fortress has one Loom-free full build (06, 07, 08, 09); every other full allocation includes Loom of Dusk, so the offensive Foundation is near-universal.
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

