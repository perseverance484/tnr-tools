# Vaporia — Scald and Steam

**Bloodline:** Vaporia (BR-090, rank A, `f7IgtcsLqomqmmBgAYS1O`) · **Revision:** Draft 2 / Boil classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Boil (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Boil damage — Damage on three Taijutsu formula rows (Drowning Strike 40, Surfing Strike 45, Scorch Break 40 EP) · secondary Liquid Ember Shell window — Afterburn (enemy) with Increase Damage Given and Lifesteal (self) on one 40 AP cast · tertiary Steam body — Decrease Damage Taken (Surfing Strike), Reflect (Scorch Break), Heal (Azure Dragon Palm); Drowning Strike's exposure as glue.

The kit's ten supported rows split 3/7: three Boil Taijutsu formula Damage rows (40, 45, 40 EP at jutsu level 25) on 60 AP area attacks, and seven single-row percentage or static tags. Liquid Ember Shell is the signature 40 AP cast: Lifesteal 40% and Increase Damage Given 35% on the caster plus Afterburn 35% on the target, all for 2 rounds, so the burn and sustain routes both deepen that one window. Surfing Strike's 30% Decrease Damage Taken, Scorch Break's 40% Reflect and Azure Dragon Palm's static Heal 25 (250 HP per tick) give a defensive face that a Taijutsu rusher with 'Consistent Damage' otherwise lacks; Drowning Strike's 35% Increase Damage Taken is a tile-bound exposure with friendly fire, kept small as root and capstone glue. Potency reaches matching supported tags on all Boil jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Boil jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Rising Steam | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Drowning Strike, Liquid Ember Shell / 2 |
| 02 | Geyser Fist | Hidden Art | Rising Steam | +2 Damage (damage) | Drowning Strike, Scorch Break, Surfing Strike / 3 |
| 03 | Caldera Burst | Advanced Art | Geyser Fist | +3 Damage (damage) | Drowning Strike, Scorch Break, Surfing Strike / 3 |
| 04 | Blistering Mist | Hidden Art | Rising Steam | +3% Afterburn (enemy debuff) | Liquid Ember Shell / 1 |
| 05 | Boiling Point | Advanced Art | Blistering Mist | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Drowning Strike, Liquid Ember Shell / 3 |
| 06 | Vapor Shroud | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Heal (self buff) | Azure Dragon Palm, Surfing Strike / 2 |
| 07 | Siphoned Heat | Hidden Art | Vapor Shroud | +2% Lifesteal (self buff) | Liquid Ember Shell / 1 |
| 08 | Dew of the Dragon | Advanced Art | Siphoned Heat | +3% Lifesteal (self buff); +5% Heal (self buff) | Azure Dragon Palm, Liquid Ember Shell / 2 |
| 09 | Scalding Backlash | Hidden Art | Vapor Shroud | +3% Reflect (self buff) | Scorch Break / 1 |
| 10 | Wall of Steam | Advanced Art | Scalding Backlash | +7% Reflect (self buff); +3% Decrease Damage Taken (self buff) | Scorch Break, Surfing Strike / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Rising Steam** — Heat climbs the blood, and the air around the quarry thickens. Liquid Ember Shell self buff 35 → 37% (2 rounds); Drowning Strike exposure 35 → 37% on its spiral tiles (ally hazard).
- **Geyser Fist** — Pressure finds the smallest crack and bursts through it. Drowning Strike 40 → 42, Surfing Strike 45 → 47, Scorch Break 40 → 42 EP; three Boil Taijutsu formula rows, all area deliveries.
- **Caldera Burst** — The whole basin boils over at once; nothing standing in it is spared. Route total +5 Damage: Drowning Strike 40 → 45, Surfing Strike 45 → 50, Scorch Break 40 → 45 EP.
- **Blistering Mist** — Steam clings where it lands and keeps on burning long after the blow. Liquid Ember Shell Afterburn 35 → 38% on its target (2 rounds); every non-pierce hit it takes adds that share, 60% cap per hit.
- **Boiling Point** — Past this heat there is no simmer left, only the roar. Burn route total +10%: Afterburn 35 → 45%; with Rising Steam, Liquid Ember Shell buff 35 → 40% and Drowning Strike exposure 35 → 40% (ally hazard).
- **Vapor Shroud** — A veil of steam wraps the body; what it cannot turn aside, it mends. Surfing Strike Decrease Damage Taken 30 → 32% (self, 2 rounds); Azure Dragon Palm Heal 25 → 27 (270 HP per tick, 2 rounds).
- **Siphoned Heat** — Every wound dealt gives its warmth back to the one who made it. Liquid Ember Shell Lifesteal 40 → 42% (self, 2 rounds); draws from every hit, pierce included; shares the 60% leech cap with vamp.
- **Dew of the Dragon** — What rose as steam settles again as cool water on the dragon's scales. Sustain route total +5% Lifesteal (Shell 40 → 45%, the hard ceiling); with Vapor Shroud, Azure Dragon Palm Heal 25 → 32 (320 HP per tick).
- **Scalding Backlash** — Strike the kettle and the kettle answers with its contents. Scorch Break Reflect 40 → 43% (self, 2 rounds); returns that share of each hit taken, pierce included, 60% cap per hit.
- **Wall of Steam** — Stand behind the boil and let the enemy learn what it costs to reach through. Bulwark route total +10%: Scorch Break Reflect 40 → 50% (under the 60% cap); with Vapor Shroud, Surfing Strike Decrease Damage Taken 30 → 35% (self, 2 rounds, pierce excluded).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | LS | REF | HEAL |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Caldera Burst (Burst) | Rising Steam, Geyser Fist, Caldera Burst, Vapor Shroud | +5 | +2% | +2% | +2% | — | — | — | +2% |
| Boiling Point (Pressure) | Rising Steam, Blistering Mist, Boiling Point, Vapor Shroud | — | +5% | +5% | +2% | +10% | — | — | +2% |
| Dew of the Dragon (Sustain) | Rising Steam, Vapor Shroud, Siphoned Heat, Dew of the Dragon | — | +2% | +2% | +2% | — | +5% | — | +7% |
| Wall of Steam (Bulwark) | Vapor Shroud, Siphoned Heat, Scalding Backlash, Wall of Steam | — | — | — | +5% | — | +2% | +10% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal · REF = Reflect · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Caldera Burst:** +5 Damage on all three Boil attacks (Drowning Strike 40 → 45, Surfing Strike 45 → 50, Scorch Break 40 → 45 EP) before the bloodline's Fire/Water/Boil/None Increase Damage Given passive and Liquid Ember Shell's own buff (37% with Rising Steam) raise them. Rising Steam also puts Drowning Strike's exposure at 37% on its spiral tiles. Vapor Shroud is the fourth purchase for a rounded rusher (32% Decrease Damage Taken after Surfing Strike, 270 HP heal ticks after Azure Dragon Palm); Blistering Mist (Afterburn 38%) is the all-offence alternative.
- **Boiling Point:** The Liquid Ember Shell pressure build: Afterburn 35 → 45% on the target for 2 rounds, so every non-pierce hit it takes from the caster, allies, weapons or normal jutsu adds 45% more (60% cap per hit), while the caster's own buff sits at 40% and Drowning Strike's exposure at 40% on its tiles. Vapor Shroud rounds it with 32% Decrease Damage Taken and 270 HP heal ticks; Geyser Fist (attacks 42/47/42 EP) is the alternative fourth purchase for a build that gives up all mitigation.
- **Dew of the Dragon:** Lifesteal 40 → 45% (the +5% hard ceiling) and Increase Damage Given 35 → 37% on the same Liquid Ember Shell cast: for 2 rounds every hit the caster lands, Azure Dragon Palm's 58 EP pierce included, returns 45% of its damage as health within the shared 60% leech cap, and Azure Dragon Palm's heal ticks reach 320 HP. Rising Steam is the fourth purchase here so the leech window is also the damage window; Scalding Backlash (Reflect 43%) is the pure-sustain alternative. Damage and Afterburn are untouched.
- **Wall of Steam:** The turtle: Scorch Break's Reflect 40 → 50% (pierce included, under the 60% per-hit cap) and Surfing Strike's Decrease Damage Taken 30 → 35% for their 2-round windows, with Liquid Ember Shell's Lifesteal at 42% and 270 HP heal ticks from Vapor Shroud. It carries no Rising Steam, so the build shows the offensive root is not a universal opener; Rising Steam in place of Siphoned Heat (buff 37%, exposure 37%) is the alternative fourth purchase. No Damage, no Afterburn.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Pressure | Sustain | Bulwark |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Liquid Ember Shell | 0 | Lifesteal | self | 40% | 40% | 40% | 45% (+5) | 42% (+2) |
| Liquid Ember Shell | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Liquid Ember Shell | 2 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Drowning Strike | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Drowning Strike | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Surfing Strike | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Surfing Strike | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 35% (+5) |
| Surfing Strike | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Scorch Break | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Scorch Break | 1 | Reflect | self | 40% | 40% | 40% | 40% | 50% (+10) |
| Azure Dragon Palm | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Azure Dragon Palm | 1 | Heal | self | 25 | 27 (+2) | 27 (+2) | 32 (+7) | 27 (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +5% Increase Damage Taken, +5% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal, +10% Reflect, +7% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Caldera Burst: +5 Damage (0 + 2 + 3; on band)
  - Route Boiling Point: +10% Afterburn (0 + 3 + 7; on band)
  - Route Dew of the Dragon: +5% Lifesteal (0 + 2 + 3; on band)
  - Route Wall of Steam: +10% Reflect (0 + 3 + 7; on band)
- Supported rows in kit: 10 (AB 1, DMG 3, DDT 1, HEAL 1, IDG 1, IDT 1, LS 1, REF 1)
- Strongest full build by row-weighted total: Rising Steam, Geyser Fist, Blistering Mist, Boiling Point (raw +22, row-weighted 26)
- Lowest row-weighted node: Siphoned Heat (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Drowning Strike#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Rising Steam, Geyser Fist, Caldera Burst, Blistering Mist | +5 Damage, +2% IDG, +2% IDT, +3% AB |
| 2 | Rising Steam, Geyser Fist, Caldera Burst, Vapor Shroud | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% HEAL |
| 3 | Rising Steam, Geyser Fist, Blistering Mist, Boiling Point | +2 Damage, +5% IDG, +5% IDT, +10% AB |
| 4 | Rising Steam, Geyser Fist, Blistering Mist, Vapor Shroud | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% HEAL |
| 5 | Rising Steam, Geyser Fist, Vapor Shroud, Siphoned Heat | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +2% LS, +2% HEAL |
| 6 | Rising Steam, Geyser Fist, Vapor Shroud, Scalding Backlash | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +3% REF, +2% HEAL |
| 7 | Rising Steam, Blistering Mist, Boiling Point, Vapor Shroud | +5% IDG, +5% IDT, +2% DDT, +10% AB, +2% HEAL |
| 8 | Rising Steam, Blistering Mist, Vapor Shroud, Siphoned Heat | +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% LS, +2% HEAL |
| 9 | Rising Steam, Blistering Mist, Vapor Shroud, Scalding Backlash | +2% IDG, +2% IDT, +2% DDT, +3% AB, +3% REF, +2% HEAL |
| 10 | Rising Steam, Vapor Shroud, Siphoned Heat, Dew of the Dragon | +2% IDG, +2% IDT, +2% DDT, +5% LS, +7% HEAL |
| 11 | Rising Steam, Vapor Shroud, Siphoned Heat, Scalding Backlash | +2% IDG, +2% IDT, +2% DDT, +2% LS, +3% REF, +2% HEAL |
| 12 | Rising Steam, Vapor Shroud, Scalding Backlash, Wall of Steam | +2% IDG, +2% IDT, +5% DDT, +10% REF, +2% HEAL |
| 13 | Vapor Shroud, Siphoned Heat, Dew of the Dragon, Scalding Backlash | +2% DDT, +5% LS, +3% REF, +7% HEAL |
| 14 | Vapor Shroud, Siphoned Heat, Scalding Backlash, Wall of Steam | +5% DDT, +2% LS, +10% REF, +2% HEAL |

## Design notes

- Node split: two roots mirror the kit's faces. Rising Steam (+2% IDG on the Shell, +2% IDT on Drowning Strike) forks into Geyser Fist → Caldera Burst (Damage +2/+3, three Boil rows) and Blistering Mist → Boiling Point (Afterburn +3%/+7%, +3% IDT, +3% IDG). Vapor Shroud (+2% DDT, +2% Heal) forks into Siphoned Heat → Dew of the Dragon (Lifesteal +2%/+3%, Heal +5%) and Scalding Backlash → Wall of Steam (Reflect +3%/+7%, DDT +3%). No capstone secondary shares a tag with a sibling Hidden Art.
- Routes: Burst +5 Damage; Pressure +10% Afterburn (3/7, as Eternal Noon); Sustain +5% Lifesteal (2/3, the hard ceiling; was +8%); Bulwark +10% Reflect (3/7; was +8%). Glue maxima over all legal allocations: IDG, IDT and DDT +5% each (2+3); Heal +7% (Vapor Shroud +2%, Dew of the Dragon +5%; 25 → 32, 250 → 320 HP per tick). Dew's Heal secondary rises from +3% to +5% to offset the Lifesteal cut, as Feast of the Fallen carries a +5% secondary on Blood-Enchanted Eyes' +5% Lifesteal route.
- Delivery at the pin: SELF rows on area jutsu land directly on the caster once per cast (actions.ts 987–1002, 1062–1066), so Surfing Strike's DDT, Scorch Break's Reflect and the Shell's self rows are plain 2-round self buffs from the cast round, not ground effects. Drowning Strike's Damage and IDT are INHERIT rows on a GROUND spiral: ground effects on every tile within 4 of the caster, own tile excluded (util.ts 2893–2894), re-applied each round to whoever stands there (process.ts 296–340).
- Interactions: the Shell's IDG and Lifesteal and Drowning Strike's IDT are Taijutsu-filtered but element-less, so they match every element-less hit of any stat type plus Taijutsu elemental hits, the three Boil attacks included; Surfing Strike's DDT and Scorch Break's Reflect list all four stat types. Damage modifiers and Afterburn skip pierce (Azure Dragon Palm's 58 pierce gets none); Lifesteal and Reflect include it. The bloodline IDG passive multiplies enhanced Damage rows downstream.
- Uptime: every jutsu has cooldown 7. The Shell is 40 AP, range 4, single target, and needs a legal OTHER_USER target for its self rows to land; the Boil attacks and Azure Dragon Palm cost 60 AP (Drowning Strike: spiral radius 4 around the caster; Surfing Strike: radius-1 circle at range 5 plus a move; Scorch Break: radius-1 circle on a target, enemies only). Buff, IDT and Afterburn windows are 2 following rounds; the static Heal is read as two ticks of value ×10 HP.
- Fourth purchases: Burst (01,02,03) adds Vapor Shroud (32% DDT, 270 HP ticks) or Blistering Mist (Afterburn 38%); Pressure (01,04,05) adds Vapor Shroud or Geyser Fist (attacks 42/47/42 EP); Sustain (06,07,08) adds Rising Steam (IDG and IDT 37%) or Scalding Backlash (Reflect 43%); Bulwark (06,09,10) adds Siphoned Heat (Lifesteal 42%) or Rising Steam. 01,02,04,05 (attacks 42/47/42 EP, Afterburn 45%, IDG and IDT 40%) is the strongest unadvertised pressure build, with no mitigation. All 14 legal full builds are non-dominated.

## Risks and unproven interactions

- Classification: Boil is the single signature element on the three Damage rows and no other captured bloodline has Boil jutsu; ordinary Boil jutsu are in scope by rule and unverified. 3 of 10 supported kit rows carry Boil; the other seven need the proposed jutsu-classification resolver, and Liquid Ember Shell (no Boil row) qualifies in-kit only through an authored Boil jutsu classification (ENGINE_GAP_REGISTER G1).
- Ally hazard (validator warns): Drowning Strike row 1 IDT is an INHERIT row on a GROUND spiral with friendly fire none (=ALL): allies within 4 of the caster at the cast, or stepping onto a spiral tile while the ground effect lasts, take the exposure too. Rising Steam (+2%) and Boiling Point (+3%) raise it on them to 37% / 40%; the Damage row (friendly fire ENEMIES) is unaffected. Positioning decides.
- Lifesteal: Dew of the Dragon puts the Shell's Lifesteal at 45% for 2 rounds on every hit the caster lands, basic attacks, weapons, normal jutsu and Azure Dragon Palm's pierce included, sharing the 60%-of-pre-shield-damage leech budget with any vamp. +5% is the hard Lifesteal ceiling (RUL-2026-10-03-005).
- Afterburn: Boiling Point makes the Shell's Afterburn 45% on one target for 2 following rounds; each non-pierce hit it takes adds floor(damage × 0.45) up to a cumulative 60% of that hit, so a second Afterburn source saturates the cap and part of the +10% is lost. Not simulated. Casting the Shell on an ally for its self rows afterburns that ally.
- Reflect: Wall of Steam returns 50% of each hit the caster takes during Scorch Break's 2-round window, pierce included, capped at 60% of pre-shield damage and bypassing shields; the self row needs a legal OTHER_USER target on the cast. The route carries no Damage, Afterburn or IDG, so the turtle is deliberately the weakest burst option. Realized value depends on incoming damage; not simulated.
- Damage is formula-calculated (sqrt stat scaling on Taijutsu / Speed, Strength) and then raised by the bloodline's IDG passive, the Shell's buff and Drowning Strike's exposure, so +5 EP is not a linear +5 damage. All three Damage rows are area deliveries, so the +5 is paid on every enemy hit and realized value scales with target count, which was not modelled.
- Heal timing: Azure Dragon Palm's Heal is static 25 with rounds 2, read as two ticks of value x10 HP on the following rounds (250 → 270 → 320 HP per tick); tick count and pool were not simulated. It rides a 60 AP single-target cast whose 58 EP pierce is unsupported, so +7% Heal is at most +140 HP per 7-round cycle: the lowest-value tag in the tree by HP.
- Unsupported rows and scope: Surfing Strike's move and Azure Dragon Palm's pierce receive nothing; the kit has no hidden, item-gated, mode-restricted, injected or adverse rows, and the Water DDT passive is not a potency target. Skill-tree effects are skipped in ranked modes. Non-dominance of full allocations is arithmetic, not evidence of equal combat strength; no combat simulation.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Boil jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

