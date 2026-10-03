# Dai Kenja — Doctrine of Overflow

**Bloodline:** Dai Kenja (BR-021, rank D, `Dqqw3zcIGDserD-qEE9QW`) · **Revision:** Draft 5 / Dai Kenja classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Dai Kenja (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Overloaded Impact offense (Damage and Increase Damage Given) · secondary Decrease Damage Given (Chakra Overload / Chakra Cannon suppression) · tertiary Increase Damage Taken (Chakra Overload exposure; adverse on Overloaded Impact).

Six supported rows on three casts, none carrying an element. Overloaded Impact holds the only Damage row (40 EP at jutsu level 25) and the only Increase Damage Given row (30% self; Ninjutsu filter with no element, so it also admits every non-elemental hit, and it is live only in the two rounds after the cast), so offense through that cast is primary in two forms: +5 Damage on the hit (Burst) or a +10% amplifier for the hits that follow (Amplifier). Decrease Damage Given is the broadest tag (25% on Chakra Overload, 30% on the AOE Chakra Cannon, all stat types) and is the secondary +10% Suppression route. Increase Damage Taken reaches Chakra Overload's 35% enemy exposure but also the adverse 25% self exposure on Overloaded Impact, so it is a small, explicitly accepted +5% Exposure route. Chakra Cannon's pierce and Chakra Overload's pool-cost row are unsupported. Potency reaches matching supported tags on all Dai Kenja-classified jutsu (RUL-2026-10-03-005; requires a classification extension).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dai Kenja-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Brimming Cup | Foundation | None | +2% Increase Damage Given (self buff) | Overloaded Impact / 1 |
| 02 | Chakra Surcharge | Hidden Art | Brimming Cup | +2 Damage (damage) | Overloaded Impact / 1 |
| 03 | Breaking Point | Advanced Art | Chakra Surcharge | +3 Damage (damage); +2% Increase Damage Given (self buff) | Overloaded Impact / 2 |
| 04 | Flooded Meridians | Hidden Art | Brimming Cup | +3% Increase Damage Given (self buff) | Overloaded Impact / 1 |
| 05 | Boundless Reservoir | Advanced Art | Flooded Meridians | +5% Increase Damage Given (self buff) | Overloaded Impact / 1 |
| 06 | Sage's Rebuke | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Chakra Cannon, Chakra Overload / 2 |
| 07 | Smothered Current | Hidden Art | Sage's Rebuke | +3% Decrease Damage Given (enemy debuff) | Chakra Cannon, Chakra Overload / 2 |
| 08 | Edict of Silence | Advanced Art | Smothered Current | +5% Decrease Damage Given (enemy debuff) | Chakra Cannon, Chakra Overload / 2 |
| 09 | Cracked Vessel | Hidden Art | Sage's Rebuke | +2% Increase Damage Taken (enemy debuff) | Chakra Overload, Overloaded Impact / 2 · **adverse:** Overloaded Impact#2 |
| 10 | Shattered Vessel | Advanced Art | Cracked Vessel | +3% Increase Damage Taken (enemy debuff); +3% Decrease Damage Given (enemy debuff) | Chakra Cannon, Chakra Overload, Overloaded Impact / 4 · **adverse:** Overloaded Impact#2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Brimming Cup** — A sage's chakra fills the cup past its rim and keeps pouring. Overloaded Impact self damage buff 30 → 32%; multiplies Ninjutsu or non-elemental hits in the 2 rounds after each cast, never its own hit.
- **Chakra Surcharge** — Every impact carries more than the body was meant to hold. Overloaded Impact Damage only (40 → 42 EP); one 60 AP single-target cast at range 4, cooldown 6. Chakra Cannon's pierce is unsupported.
- **Breaking Point** — Push the overload one breath further than wisdom allows. Route total +5 Damage: Overloaded Impact 40 → 45 EP; its self buff +2% (34% with Brimming Cup), live after the cast round, never on this hit.
- **Flooded Meridians** — Open every channel; let the current run where it will. Overloaded Impact self damage buff only (35% with Brimming Cup); Ninjutsu or non-elemental hits in the 2 rounds after each cast.
- **Boundless Reservoir** — There is no bottom to the well the Great Sage draws from. Same self buff; route total +10% (30 → 40%) for the 2 rounds after each 60 AP cast, cooldown 6. No other row.
- **Sage's Rebuke** — A word from the sage, and the enemy's chakra falters. Decrease Damage Given on Chakra Overload 25 → 27% (enemies) and Chakra Cannon 30 → 32% (any non-caster in its circle); all stat types, 2 rounds.
- **Smothered Current** — Their flow is pinched to a trickle under the sage's hand. Both Decrease Damage Given rows +3% more (30% / 35% with Sage's Rebuke); the two debuffs compound on one target when both casts land.
- **Edict of Silence** — The sage speaks once; the enemy's power answers in a whisper. Route total +10%: Chakra Overload 25 → 35%, Chakra Cannon 30 → 40% (×0.65 × 0.60 = ×0.39 on a hit when both sit on one target). Cannon also reaches allies in its circle.
- **Cracked Vessel** — Overload leaves fissures in the vessel, yours and theirs. Chakra Overload enemy exposure 35 → 37% (Ninjutsu or non-elemental hits) and the adverse Overloaded Impact self exposure 25 → 27% (all damage).
- **Shattered Vessel** — What is overfilled must break; the sage chooses when. Exposure route total +5%: Chakra Overload 40%, adverse self exposure 30%; both Decrease Damage Given rows +3% (30% / 35% with Sage's Rebuke).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT |
|---|---|---:|---:|---:|---:|
| Breaking Point (Burst) | Brimming Cup, Chakra Surcharge, Breaking Point, Sage's Rebuke | +5 | +4% | +2% | — |
| Boundless Reservoir (Amplifier) | Brimming Cup, Flooded Meridians, Boundless Reservoir, Sage's Rebuke | — | +10% | +2% | — |
| Edict of Silence (Suppression) | Brimming Cup, Sage's Rebuke, Smothered Current, Edict of Silence | — | +2% | +10% | — |
| Shattered Vessel (Exposure) | Sage's Rebuke, Smothered Current, Cracked Vessel, Shattered Vessel | — | — | +8% | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Breaking Point:** +5 Damage on the kit's only Damage row (Overloaded Impact 40 → 45 EP) and its self buff at 34% for the two rounds after the cast, never on the cast's own hit. Sage's Rebuke is the fourth purchase because it opens the control root (Decrease Damage Given 27% / 32%) without touching Overloaded Impact again; Flooded Meridians (buff 37%) is the all-in alternative.
- **Boundless Reservoir:** Overloaded Impact as a two-round amplifier: its self Increase Damage Given reaches 40% (+10%) and multiplies every Ninjutsu or non-elemental hit (normal jutsu, basic attacks, weapons) landed in the two rounds after the cast by ×1.40, never the cast's own hit. Sage's Rebuke is the fourth purchase for a small suppression floor (27% / 32%); Chakra Surcharge (42 EP) is the offensive alternative.
- **Edict of Silence:** Both Decrease Damage Given rows at the route maximum (+10%: Chakra Overload 35% on enemies, Chakra Cannon 40% on any non-caster in its circle), compounding to ×0.65 × 0.60 = ×0.39 on a non-pierce hit from a target carrying both debuffs (casts in the same or consecutive rounds). Brimming Cup is the fourth purchase because it raises the self buff to 32% at no exposure cost; Cracked Vessel (exposure 37%, adverse self 27%) is the aggressive alternative.
- **Shattered Vessel:** The overload gamble: Chakra Overload's enemy exposure (Ninjutsu or non-elemental damage, from every attacker) reaches 40% (+5%) while Overloaded Impact's own self exposure (all damage) rises to 30%, and both suppression rows sit at +8% (33% / 38%). Smothered Current is the fourth purchase because it compounds the control casts; Brimming Cup (buff 32%) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Amplifier | Suppression | Exposure |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Overloaded Impact | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Overloaded Impact | 1 | Increase Damage Given | self | 30% | 34% (+4) | 40% (+10) | 32% (+2) | 30% |
| Overloaded Impact | 2 | Increase Damage Taken **adverse** | self | 25% | 25% | 25% | 25% | 30% (+5) |
| Chakra Overload | 0 | Decrease Damage Given | enemy | 25% | 27% (+2) | 27% (+2) | 35% (+10) | 33% (+8) |
| Chakra Overload | 1 | Increase Damage Taken | enemy | 35% | 35% | 35% | 35% | 40% (+5) |
| Chakra Overload | 2 | increasepoolcost (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Chakra Cannon | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Chakra Cannon | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 38% (+8) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 13; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +5% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Breaking Point: +5 Damage (0 + 2 + 3; on band)
  - Route Boundless Reservoir: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route Edict of Silence: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Shattered Vessel: +5% Increase Damage Taken (0 + 2 + 3; on band)
- Supported rows in kit: 6 (DMG 1, DDG 2, IDG 1, IDT 2)
- Strongest full build by row-weighted total: Sage's Rebuke, Smothered Current, Cracked Vessel, Shattered Vessel (raw +13, row-weighted 26)
- Lowest row-weighted node: Brimming Cup (2)

Validator warnings:

- node 09 (Cracked Vessel) also amplifies adverse rows: Overloaded Impact#2
- node 10 (Shattered Vessel) also amplifies adverse rows: Overloaded Impact#2
- classification status: requires classification extension (director decision)
- ally-hazard area rows amplified (friendly fire none/ALL): Chakra Cannon#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Brimming Cup, Chakra Surcharge, Breaking Point, Flooded Meridians | +5 Damage, +7% IDG |
| 2 | Brimming Cup, Chakra Surcharge, Breaking Point, Sage's Rebuke | +5 Damage, +4% IDG, +2% DDG |
| 3 | Brimming Cup, Chakra Surcharge, Flooded Meridians, Boundless Reservoir | +2 Damage, +10% IDG |
| 4 | Brimming Cup, Chakra Surcharge, Flooded Meridians, Sage's Rebuke | +2 Damage, +5% IDG, +2% DDG |
| 5 | Brimming Cup, Chakra Surcharge, Sage's Rebuke, Smothered Current | +2 Damage, +2% IDG, +5% DDG |
| 6 | Brimming Cup, Chakra Surcharge, Sage's Rebuke, Cracked Vessel | +2 Damage, +2% IDG, +2% DDG, +2% IDT |
| 7 | Brimming Cup, Flooded Meridians, Boundless Reservoir, Sage's Rebuke | +10% IDG, +2% DDG |
| 8 | Brimming Cup, Flooded Meridians, Sage's Rebuke, Smothered Current | +5% IDG, +5% DDG |
| 9 | Brimming Cup, Flooded Meridians, Sage's Rebuke, Cracked Vessel | +5% IDG, +2% DDG, +2% IDT |
| 10 | Brimming Cup, Sage's Rebuke, Smothered Current, Edict of Silence | +2% IDG, +10% DDG |
| 11 | Brimming Cup, Sage's Rebuke, Smothered Current, Cracked Vessel | +2% IDG, +5% DDG, +2% IDT |
| 12 | Brimming Cup, Sage's Rebuke, Cracked Vessel, Shattered Vessel | +2% IDG, +5% DDG, +5% IDT |
| 13 | Sage's Rebuke, Smothered Current, Edict of Silence, Cracked Vessel | +10% DDG, +2% IDT |
| 14 | Sage's Rebuke, Smothered Current, Cracked Vessel, Shattered Vessel | +8% DDG, +5% IDT |

## Design notes

- Node split mirrors the kit's two sides. Brimming Cup (self) opens Overloaded Impact and forks into raw power (Chakra Surcharge → Breaking Point) and self buff (Flooded Meridians → Boundless Reservoir); Sage's Rebuke (enemy) opens Chakra Overload / Chakra Cannon and forks into suppression (Smothered Current → Edict of Silence) and exposure (Cracked Vessel → Shattered Vessel). Every Advanced Art is 3 BP deep.
- Routes (RUL-2026-10-03-005): Burst +5 Damage (Chakra Surcharge +2, Breaking Point +3); Amplifier +10% Increase Damage Given (Brimming Cup +2%, Flooded Meridians +3%, Boundless Reservoir +5%); Suppression +10% Decrease Damage Given (Sage's Rebuke +2%, Smothered Current +3%, Edict of Silence +5%); Exposure +5% Increase Damage Taken (Cracked Vessel +2%, Shattered Vessel +3%). Maxima over every legal allocation: Damage +5, Increase Damage Given +10%, Decrease Damage Given +10%, Increase Damage Taken +5%; not jointly attainable.
- Recalibration from Draft 4: Chakra Surcharge +3 → +2 Damage (hard +5 ceiling; was +6), Brimming Cup +3% → +2% and Boundless Reservoir +4% → +5% (Amplifier stays +10%), Smothered Current +2% → +3% and Edict of Silence +4% → +5% (Suppression +8% → +10%, on band). Exposure stays +5%: the adverse self row keeps it small.
- Timing (SOURCE_MECHANICS §3b): Overloaded Impact's self buff is inert in its cast round (tags.ts 925; util.ts 2567–2577), so it never touches its own hit, and cooldown 6 outlives it. In the two rounds after the cast the enhanced 32–40% multiplies every Ninjutsu or non-elemental hit (×1.32 to ×1.40; getEfficiencyRatio, tags.ts 3477–3510; computeDamagePacket, process.ts 1692–1825); the 15% bloodline passive applies last.
- Delivery and uptime: Overloaded Impact is 60 AP, cooldown 6, one single-target hit at range 4; its buff and self exposure live two rounds in every six. Chakra Overload is 40 AP single target, cooldown 6; Chakra Cannon a 60 AP AOE circle, cooldown 7. Both suppression debuffs sit on one target only when the casts land in the same or consecutive rounds (100 AP in all), so ×0.65 × 0.60 = ×0.39 is a ceiling. Nothing was simulated.
- Fourth purchases: Burst takes Sage's Rebuke (27% / 32%) or Flooded Meridians (buff 37%); Amplifier, Sage's Rebuke or Chakra Surcharge (42 EP); Suppression, Brimming Cup (buff 32%) or Cracked Vessel (exposure 37%, self 27%); Exposure, Smothered Current or Brimming Cup. Counting Increase Damage Taken as a gain, 13 of 14 full builds are non-dominated; IDT-neutral, 8 are and neither Vessel node appears, so Cracked Vessel earns its place as the Shattered Vessel gate. Adverse-aware dominance is tooling debt.

## Risks and unproven interactions

- Adverse row accepted (OPEN_DECISIONS D11, ENGINE_GAP_REGISTER G14): Increase Damage Taken nodes also raise Overloaded Impact's self exposure (all damage; 27% with Cracked Vessel, 30% with Shattered Vessel) in the two rounds after each cast, atop the 5% IDT passive. Only the Exposure route carries the tag; the enemy row (Chakra Overload, Ninjutsu or non-elemental, 35 → 40%) needs its own 40 AP cast.
- Ally hazard (Chakra Cannon#1): Cannon is an OTHER_USER AOE circle with friendly fire ALL, so an ally in the circle (never the caster) receives its two-round suppression at the enhanced 32–40% (actions.ts 1029–1060; process.ts 154–183); every Decrease Damage Given node raises it, and positioning decides. Chakra Overload's suppression is ENEMIES-only; its ALL exposure row lands on an ally only if aimed at one.
- Single-cast concentration: all five root-A nodes modify Overloaded Impact only (one 60 AP single-target cast, cooldown 6). The Burst route adds +5 Damage to one hit per cycle; the Amplifier route pays only on Ninjutsu or non-elemental hits landed in the two rounds after that cast.
- Suppression stacking: Chakra Overload and Chakra Cannon apply separate two-round Decrease Damage Given debuffs; with BATTLE_TAG_STACKING on, every same-tag effect applies and the reductions compound in sequence (process.ts 1109–1117, 1692–1825), so one target's non-pierce hits are cut to ×0.75 × 0.70 = ×0.525 at baseline and ×0.65 × 0.60 = ×0.39 at the +10% route maximum (floor ×0.10), lower still with an allied Dai Kenja. Not simulated.
- Downstream reach: the self buff multiplies every Ninjutsu or non-elemental hit the caster lands in its window (normal jutsu, basic attacks, weapons); enemy-side suppression and exposure alter damage from allies and weapons too. Stat filters on element-less rows are not binding (SOURCE_MECHANICS §3, getEfficiencyRatio).
- Classification: no kit row carries an element, so the tree requires a classification extension. 'Dai Kenja' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Off-kit coverage is unverified.
- Unsupported rows: Chakra Cannon's pierce (58 at level 25) and Chakra Overload's increasepoolcost (100%) receive no bonus; pierce is processed after the damage-modifier pass, so the Amplifier and Exposure routes do not raise the pierce hit and the Suppression route does not reduce enemy pierce.
- Rank context: Dai Kenja is a D-rank bloodline with B/C/A-rank jutsu; the tree equalises marginal opportunity, not final strength. Normal-tree potency policy is not approved, so a combined stacking audit precedes implementation. Skill-tree effects are skipped in ranked PvP and ranked sparring. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Dai Kenja-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

