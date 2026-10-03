# Eyes of the Forsaken King — Court in Exile

**Bloodline:** Eyes of the Forsaken King (BR-027, rank S, `r3nBY_Th4_ZAIUfhx1jdy`) · **Revision:** Draft 3 / Light classification / forked tree (RUL-2026-10-03-005 reconciliation; values unchanged) · **Classification:** Light (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst and exposure (Damage, Increase Damage Taken) · secondary Afterburn pressure through Imperial Swords · tertiary Self buffs on illuminance and Lux (Increase Damage Given, Decrease Damage Taken, Reflect).

Ten supported rows across five casts. Three Light Damage rows (Shattered Reflection 40, Lux 50 on an AOE line, Imperial Swords 40 EP at jutsu level 25; each 60 AP, cooldown 7) and three 35% Increase Damage Taken rows (two on Chrono Stasis, which land together on one target, one on Imperial Swords) are the kit's identity under its Burst trait, so burst and exposure are the declared primary. Imperial Swords also carries the only Afterburn row (25%, 2 rounds), the secondary pressure route. illuminance's 35% Increase Damage Given (Fire/Light/Lightning/Wind/None, no stat filter) and 30% Decrease Damage Taken, and Lux's 40% Reflect, are single-row two-round self buffs realized on the caster at cast time; they form the defensive root. Mirror, move and timedilation are unsupported. Potency reaches matching supported tags on all Light jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Light jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Gaze of the Deposed | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Chrono Stasis, Imperial Swords, illuminance / 4 |
| 02 | Edge of the Regalia | Hidden Art | Gaze of the Deposed | +2 Damage (damage) | Imperial Swords, Lux, Shattered Reflection / 3 |
| 03 | Throne of Broken Light | Advanced Art | Edge of the Regalia | +3 Damage (damage) | Imperial Swords, Lux, Shattered Reflection / 3 |
| 04 | Searing Afterimage | Hidden Art | Gaze of the Deposed | +3% Afterburn (enemy debuff) | Imperial Swords / 1 |
| 05 | Judgment of the Forsaken | Advanced Art | Searing Afterimage | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Chrono Stasis, Imperial Swords / 4 |
| 06 | Mantle of Exile | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Lux, illuminance / 2 |
| 07 | Halo of the Unbowed | Hidden Art | Mantle of Exile | +3% Decrease Damage Taken (self buff) | illuminance / 1 |
| 08 | Kingdom of One | Advanced Art | Halo of the Unbowed | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | illuminance / 2 |
| 09 | Mirrored Crown | Hidden Art | Mantle of Exile | +3% Reflect (self buff) | Lux / 1 |
| 10 | Usurper's Reckoning | Advanced Art | Mirrored Crown | +5% Reflect (self buff); +2% Increase Damage Taken (enemy debuff) | Chrono Stasis, Imperial Swords, Lux / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Gaze of the Deposed** — What the fallen king looks upon, he still judges. illuminance self damage buff 35 → 37% (self at cast, 2 rounds); Chrono Stasis ×2 and Imperial Swords enemy exposure 35 → 37% each (2 rounds).
- **Edge of the Regalia** — The crown jewels were always blades. All three Damage rows: Lux 50 → 52 EP (AOE line; allies in it are hit), Shattered Reflection and Imperial Swords 40 → 42 EP; all 60 AP casts.
- **Throne of Broken Light** — He rules nothing now but the moment the light breaks. Same three Damage rows; route total +5 Damage (Lux 55, Shattered Reflection 45, Imperial Swords 45 EP). Lux's line still reaches allies in it.
- **Searing Afterimage** — Look away; the image stays, and it burns. Imperial Swords Afterburn only (25 → 28%, the 2 rounds after each 60 AP cast); its value is every later non-pierce hit the target takes.
- **Judgment of the Forsaken** — No court will hear the appeal; the sentence is light. Imperial Swords Afterburn route total +10% (25 → 35%); exposure +3% on Chrono Stasis ×2 and Imperial Swords (40% each with Gaze; 120% stacked).
- **Mantle of Exile** — Stripped of the crown, he kept the light it cast. illuminance self damage reduction 30 → 32% (all non-pierce damage, 2 rounds); Lux self Reflect 40 → 42% of each hit, pierce included (2 rounds).
- **Halo of the Unbowed** — A king without a kingdom still refuses to kneel. illuminance self damage reduction only (35% with Mantle of Exile); one row, all non-pierce damage, 2 rounds per 40 AP cast.
- **Kingdom of One** — One subject, one sovereign, one light that answers to him. illuminance damage reduction route total +10% (30 → 40%) and self damage buff +3% (38%; 40% with Gaze of the Deposed); one 40 AP cast, 2 rounds.
- **Mirrored Crown** — Strike the crown and meet your own blow in its facets. Lux self Reflect only (45% with Mantle of Exile); one row, every hit incl. pierce, 60% per-hit cap, 2 rounds per 60 AP cast, cooldown 7.
- **Usurper's Reckoning** — Every hand raised against the king is counted, and repaid. Lux Reflect route total +10% (40 → 50%, under the 60% per-hit cap); exposure +2% on Chrono Stasis ×2 and Imperial Swords (37%; 39% with Gaze).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|
| Throne of Broken Light (Burst) | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Mantle of Exile | +5 | +2% | +2% | +2% | — | +2% |
| Judgment of the Forsaken (Burn pressure) | Gaze of the Deposed, Searing Afterimage, Judgment of the Forsaken, Mantle of Exile | — | +2% | +5% | +2% | +10% | +2% |
| Kingdom of One (Fortress) | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Kingdom of One | — | +5% | +2% | +10% | — | +2% |
| Usurper's Reckoning (Counter) | Mantle of Exile, Halo of the Unbowed, Mirrored Crown, Usurper's Reckoning | — | — | +2% | +5% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Throne of Broken Light:** +5 Damage on all three Light Damage rows (Lux 55 EP on the line, Shattered Reflection 45, Imperial Swords 45) with illuminance's damage buff at 37% and every exposure row at 37%. Mantle of Exile is the fourth purchase because it opens the defensive root (reduction 32%, Reflect 42%) without touching the Damage rows again; Searing Afterimage (Afterburn 28%) is the all-in alternative.
- **Judgment of the Forsaken:** Imperial Swords as the pressure cast: its Afterburn reaches 35% (+10%) and all three exposure rows reach 40% (Chrono Stasis lands two at once, Imperial Swords the third), so every non-pierce hit on the marked target in the two rounds after the casts is amplified and burns (Imperial Swords' own hit is not). Mantle of Exile is the fourth purchase for a small defensive floor; Edge of the Regalia (+2 Damage) is the offensive alternative.
- **Kingdom of One:** illuminance as a two-round fortress buff: damage reduction 40% (+10%) and damage buff 40% for the two rounds after one 40 AP cast, with exposure at 37% and Reflect at 42%. Gaze of the Deposed is the fourth purchase because it lifts illuminance's buff and the exposure rows; Mirrored Crown (Reflect 45%) is the defensive alternative.
- **Usurper's Reckoning:** The counter-punch build: Lux's Reflect reaches 50% (+10%) of every hit taken for two rounds after each cast, illuminance's reduction sits at 35%, and the three exposure rows carry 37% from the capstone alone. Halo of the Unbowed is the fourth purchase because it compounds the survival window; Gaze of the Deposed (exposure 39%, buff 37%) is the aggressive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Counter |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Shattered Reflection | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Shattered Reflection | 1 | mirror (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Lux | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Lux | 1 | Reflect | self | 40% | 42% (+2) | 42% (+2) | 42% (+2) | 50% (+10) |
| illuminance | 0 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 35% |
| illuminance | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 35% (+5) |
| illuminance | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Chrono Stasis | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Chrono Stasis | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Chrono Stasis | 2 | timedilation (unsupported) | self | 100% | 100% | 100% | 100% | 100% |
| Imperial Swords | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Imperial Swords | 1 | Afterburn | enemy | 25% | 25% | 35% (+10) | 25% | 25% |
| Imperial Swords | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Throne of Broken Light: +5 Damage (0 + 2 + 3; on band)
  - Route Judgment of the Forsaken: +10% Afterburn (0 + 3 + 7; on band)
  - Route Kingdom of One: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Usurper's Reckoning: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (AB 1, DMG 3, DDT 1, IDG 1, IDT 3, REF 1)
- Strongest full build by row-weighted total: Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Judgment of the Forsaken (raw +19, row-weighted 33)
- Lowest row-weighted node: Searing Afterimage (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Lux#0

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Searing Afterimage | +5 Damage, +2% IDG, +2% IDT, +3% AB |
| 2 | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Mantle of Exile | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Judgment of the Forsaken | +2 Damage, +2% IDG, +5% IDT, +10% AB |
| 4 | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Mantle of Exile | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% REF |
| 5 | Gaze of the Deposed, Edge of the Regalia, Mantle of Exile, Halo of the Unbowed | +2 Damage, +2% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Gaze of the Deposed, Edge of the Regalia, Mantle of Exile, Mirrored Crown | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Gaze of the Deposed, Searing Afterimage, Judgment of the Forsaken, Mantle of Exile | +2% IDG, +5% IDT, +2% DDT, +10% AB, +2% REF |
| 8 | Gaze of the Deposed, Searing Afterimage, Mantle of Exile, Halo of the Unbowed | +2% IDG, +2% IDT, +5% DDT, +3% AB, +2% REF |
| 9 | Gaze of the Deposed, Searing Afterimage, Mantle of Exile, Mirrored Crown | +2% IDG, +2% IDT, +2% DDT, +3% AB, +5% REF |
| 10 | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Kingdom of One | +5% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Mirrored Crown | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Gaze of the Deposed, Mantle of Exile, Mirrored Crown, Usurper's Reckoning | +2% IDG, +4% IDT, +2% DDT, +10% REF |
| 13 | Mantle of Exile, Halo of the Unbowed, Kingdom of One, Mirrored Crown | +3% IDG, +10% DDT, +5% REF |
| 14 | Mantle of Exile, Halo of the Unbowed, Mirrored Crown, Usurper's Reckoning | +2% IDT, +5% DDT, +10% REF |

## Design notes

- Node split: Gaze of the Deposed (damage buff + exposure) forks into a Damage route (Edge of the Regalia → Throne of Broken Light) and an Afterburn route (Searing Afterimage → Judgment of the Forsaken). Mantle of Exile (reduction + Reflect) forks into a reduction route (Halo of the Unbowed → Kingdom of One) and a Reflect route (Mirrored Crown → Usurper's Reckoning). 2 Foundations, 4 Hidden Arts, 4 Advanced Arts; every capstone is 3 BP deep; any two capstones cost 5 or 6 BP (budget 4).
- Routes (RUL-2026-10-03-005): Burst +5 Damage (Edge of the Regalia +2, Throne of Broken Light +3; Lux 55, the others 45 EP); Burn pressure +10% Afterburn (Searing Afterimage +3%, Judgment +7%; 35%); Fortress +10% Decrease Damage Taken (Mantle +2%, Halo +3%, Kingdom +5%; 40%); Counter +10% Reflect (Mantle +2%, Mirrored Crown +3%, Usurper +5%; 50%). Glue maxima over every legal allocation: Increase Damage Given +5% (40%), Increase Damage Taken +5% (40% per row). Values are unchanged from Draft 2: every route already sat on a band and under every ceiling.
- Shape: the Taiyo Kami fork with kit substitutions. Reflect replaces Decrease Damage Given (the kit has no DDG row); Judgment drops Eternal Noon's +3% Increase Damage Given; exposure reaches three stacking rows, so it stays glue at +5% (Gaze +2%, Judgment +3%; Usurper +2%) rather than a route.
- Interactions: illuminance's damage buff (no stat filter) adds 35% (40% at the maximum) of the staged base to the caster's Light, Fire, Lightning, Wind and element-less hits in the 2 rounds after its cast; the bloodline passive (25% + 0.15/level, same elements) is bloodline-sourced and multiplies on top. Chrono Stasis row 0 and Imperial Swords row 2 (four stat types, no element) add to every non-pierce hit on the target; Chrono Stasis row 1 skips Water, Earth and other unlisted elements.
- Delivery and uptime: the three damage casts cost 60 AP on cooldown 7 at range 4 (Lux is an AOE line). illuminance is a 40 AP EMPTY_GROUND circle at range 5; its buff rows are SELF, realized on the caster at cast (actions.ts 980-1004), not through the tiles. Chrono Stasis is a 40 AP single-target cast at range 5 carrying both exposure rows. Lux's Reflect row is SELF too (live the 2 rounds after cast). Stacked exposure figures are ceilings (100 AP for both casts); nothing was simulated.
- Fourth purchases: Burst takes Mantle of Exile (reduction 32%, Reflect 42%) or Searing Afterimage (Afterburn 28%); Burn pressure takes Mantle of Exile or Edge of the Regalia (+2 Damage); Fortress takes Gaze of the Deposed (buff 40%, exposure 37%) or Mirrored Crown (Reflect 45%); Counter takes Halo of the Unbowed (reduction 35%) or Gaze of the Deposed (exposure 39%, buff 37%). All 14 legal full-budget allocations are numerically non-dominated and every node appears in at least one.
- Capstone secondaries: Judgment of the Forsaken carries exposure +3% because Imperial Swords holds both the Afterburn row and an exposure row (burn and mark on one cast). Kingdom of One carries damage buff +3% so both of illuminance's self rows reach 40% on one cast. Usurper's Reckoning carries exposure +2%, below the pressure capstone's +3%, so the defensive capstone is not the best offensive purchase and the three-row exposure maximum stays at +5%. No secondary out-bids a sibling Hidden Art (+3%).

## Risks and unproven interactions

- Ally hazard (Lux#0): Lux's AOE line Damage row has no friendlyFire value (ALL at the pin), so allies in the line take 50 EP (52 with Edge of the Regalia, 55 with Throne); positioning decides. Shattered Reflection, Chrono Stasis and Imperial Swords (Damage ENEMIES-only) are single-target; illuminance's supported rows are SELF, so its ground circle carries no amplified hazard.
- Exposure stacking (SOURCE_MECHANICS §3b): Chrono Stasis's two Increase Damage Taken rows (70%) and Imperial Swords' row (35%) all apply to one target and add to 105% of the staged base, 120% at the +5% maximum, in the two rounds after their casts (not on Imperial Swords' own hit); Afterburn 35% is taken from the amplified hits. Exposure is held to +5% glue for this reason; not simulated.
- Reflect near cap: Lux's Reflect reaches 50% at the route maximum against the engine's 60% per-hit cap (process.ts), so a main-tree or equipment Reflect source stacking on it saturates quickly; the buff lasts 2 rounds per 60 AP Lux cast on cooldown 7, so the Counter build's value depends on being hit inside that window. Lux must be aimed at a living non-caster user to realize it.
- Downstream reach and pierce: illuminance's damage buff also adds to the caster's non-bloodline Fire/Lightning/Wind and element-less hits in its window; enemy-side exposure and Afterburn amplify allies' and weapons' damage against the marked target. Stat filters on element-less rows are not binding (SOURCE_MECHANICS §3). Damage modifiers never touch pierce hits; Reflect includes pierce; Afterburn skips it.
- Classification: element-wide Light scope (RUL-2026-10-03-005): matching supported tags on all Light jutsu, whatever their source; sharing Light with other bloodlines is expected. All five kit jutsu carry Light on a row, but only 5 of the 10 supported rows do, so the rest need the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Light coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu) is unverified.
- Afterburn: one application row (Imperial Swords, 25% for 2 rounds per 60 AP cast; 35% at the route maximum); its value is downstream, depends on hits landed in the window, skips pierce, and the 60% per-hit cap means stacked Afterburn sources saturate. No proc or uptime simulation was performed.
- Rank context: an S-rank bloodline whose native kit (three 60 AP Damage casts, triple exposure, a 25%+ damage-buff passive) is strong before any node; the tree equalises marginal opportunity, not final strength. Ranked modes suppress skill-tree effects; normal-tree potency policy is unapproved, so a stacking audit precedes implementation.
- Unsupported rows untouched: Shattered Reflection's mirror (100%), illuminance's move (1) and Chrono Stasis's timedilation (100%) receive no bonus. No adverse rows exist in this kit; no row is hidden, item-gated or mode-restricted.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Light jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

