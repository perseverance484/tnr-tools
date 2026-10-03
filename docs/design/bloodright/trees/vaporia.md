# Vaporia — Scald and Steam

**Bloodline:** Vaporia (BR-090, rank A, `f7IgtcsLqomqmmBgAYS1O`) · **Revision:** Draft 1 / Boil classification / forked tree · **Classification:** Boil (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Boil damage — Damage on three Taijutsu formula rows (Drowning Strike 40, Surfing Strike 45, Scorch Break 40) · secondary Liquid Ember Shell window — Afterburn (enemy) with Increase Damage Given and Lifesteal (self) on one 40 AP cast · tertiary Steam body — Decrease Damage Taken (Surfing Strike), Reflect (Scorch Break), Heal (Azure Dragon Palm); Drowning Strike's exposure as glue.

The kit's ten supported rows split 3/7: three Boil Taijutsu formula Damage rows (40, 45, 40 at jutsu level 25) on 60 AP area attacks, and seven single-row percentage or static tags. Liquid Ember Shell is the signature 40 AP cast: Lifesteal 40% and Increase Damage Given 35% on the caster plus Afterburn 35% on the target, all for 2 rounds, so the burn and sustain routes both deepen that one window. Surfing Strike's 30% Decrease Damage Taken, Scorch Break's 40% Reflect and Azure Dragon Palm's static Heal 25 (250 HP per tick) give a defensive face that a Taijutsu rusher with 'Consistent Damage' otherwise lacks; Drowning Strike's 35% Increase Damage Taken is a tile-bound exposure with friendly fire, kept small as root and capstone glue.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Boil-classified Vaporia jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Rising Steam | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Drowning Strike, Liquid Ember Shell / 2 |
| 02 | Geyser Fist | Hidden Art | Rising Steam | +2 Damage power (damage) | Drowning Strike, Scorch Break, Surfing Strike / 3 |
| 03 | Caldera Burst | Advanced Art | Geyser Fist | +3 Damage power (damage) | Drowning Strike, Scorch Break, Surfing Strike / 3 |
| 04 | Blistering Mist | Hidden Art | Rising Steam | +3% Afterburn (enemy debuff) | Liquid Ember Shell / 1 |
| 05 | Boiling Point | Advanced Art | Blistering Mist | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Drowning Strike, Liquid Ember Shell / 3 |
| 06 | Vapor Shroud | Foundation | None | +2% Decrease Damage Taken (self buff); +2 Heal power (self buff) | Azure Dragon Palm, Surfing Strike / 2 |
| 07 | Siphoned Heat | Hidden Art | Vapor Shroud | +3% Lifesteal (self buff) | Liquid Ember Shell / 1 |
| 08 | Dew of the Dragon | Advanced Art | Siphoned Heat | +5% Lifesteal (self buff); +3 Heal power (self buff) | Azure Dragon Palm, Liquid Ember Shell / 2 |
| 09 | Scalding Backlash | Hidden Art | Vapor Shroud | +3% Reflect (self buff) | Scorch Break / 1 |
| 10 | Wall of Steam | Advanced Art | Scalding Backlash | +5% Reflect (self buff); +3% Decrease Damage Taken (self buff) | Scorch Break, Surfing Strike / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Rising Steam** — Heat climbs the blood, and the air around the quarry thickens. Liquid Ember Shell self buff 35→37% (2 rounds); Drowning Strike exposure 35→37% on its spiral tiles (ally hazard). 2 rows.
- **Geyser Fist** — Pressure finds the smallest crack and bursts through it. Drowning Strike 40→42, Surfing Strike 45→47, Scorch Break 40→42 power; three Boil Taijutsu formula rows, all area deliveries.
- **Caldera Burst** — The whole basin boils over at once; nothing standing in it is spared. Route total +5: Drowning Strike 40→45, Surfing Strike 45→50, Scorch Break 40→45 power (Taiyo Kami's three-row figure). 3 rows.
- **Blistering Mist** — Steam clings where it lands and keeps on burning long after the blow. Liquid Ember Shell Afterburn 35→38% on its target (2 rounds); every non-pierce hit it takes adds that share, 60% cap per hit. 1 row.
- **Boiling Point** — Past this heat there is no simmer left, only the roar. Afterburn 35→45% on the route; with Rising Steam, Liquid Ember Shell buff 35→40%, Drowning Strike exposure 35→40% (ally hazard). 3 rows.
- **Vapor Shroud** — A veil of steam wraps the body; what it cannot turn aside, it mends. Surfing Strike Decrease Damage Taken 30→32% (self, 2 rounds); Azure Dragon Palm Heal 25→27 power = 270 HP per tick, 2 rounds. 2 rows.
- **Siphoned Heat** — Every wound dealt gives its warmth back to the one who made it. Liquid Ember Shell Lifesteal 40→43% (self, 2 rounds); draws from every hit, pierce included; shares the 60% leech cap with vamp. 1 row.
- **Dew of the Dragon** — What rose as steam settles again as cool water on the dragon's scales. Lifesteal 40→48% on the route; with Vapor Shroud, Azure Dragon Palm Heal 25→30 power = 300 HP per tick (the +5 guardrail). 2 rows.
- **Scalding Backlash** — Strike the kettle and the kettle answers with its contents. Scorch Break Reflect 40→43% (self, 2 rounds); returns that share of each hit taken, pierce included, 60% cap per hit. 1 row.
- **Wall of Steam** — Stand behind the boil and let the enemy learn what it costs to reach through. Reflect 40→48% on the route; with Vapor Shroud, Surfing Strike Decrease Damage Taken 30→35% (self, 2 rounds, pierce excluded). 2 rows.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | LS | REF | HEAL |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Caldera Burst (Burst) | Rising Steam, Geyser Fist, Caldera Burst, Vapor Shroud | +5 | +2% | +2% | +2% | — | — | — | +2 |
| Boiling Point (Pressure) | Rising Steam, Blistering Mist, Boiling Point, Vapor Shroud | — | +5% | +5% | +2% | +10% | — | — | +2 |
| Dew of the Dragon (Sustain) | Rising Steam, Vapor Shroud, Siphoned Heat, Dew of the Dragon | — | +2% | +2% | +2% | — | +8% | — | +5 |
| Wall of Steam (Bulwark) | Vapor Shroud, Siphoned Heat, Scalding Backlash, Wall of Steam | — | — | — | +5% | — | +3% | +8% | +2 |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal · REF = Reflect · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Caldera Burst:** The +5 power route on all three Boil attacks (Drowning Strike 40→45, Surfing Strike 45→50, Scorch Break 40→45) before the bloodline's Fire/Water/Boil/None Increase Damage Given passive and Liquid Ember Shell's own buff (37% with Rising Steam) multiply them. Rising Steam also puts Drowning Strike's exposure at 37% on its spiral tiles. Vapor Shroud is the fourth purchase for a rounded rusher (32% Decrease Damage Taken after Surfing Strike, 270 HP heal ticks after Azure Dragon Palm); Blistering Mist (Afterburn 38%) is the all-offence alternative.
- **Boiling Point:** The Liquid Ember Shell pressure build: Afterburn 35→45% on the target for 2 rounds, so every non-pierce hit it takes from the caster, allies, weapons or normal jutsu adds 45% more (60% cap per hit), while the caster's own buff sits at 40% and Drowning Strike's exposure at 40% on its tiles. Vapor Shroud rounds it with 32% Decrease Damage Taken and 270 HP heal ticks; Geyser Fist (attacks 42/47/42) is the alternative fourth purchase for a build that gives up all mitigation.
- **Dew of the Dragon:** Lifesteal 40→48% and Increase Damage Given 35→37% on the same Liquid Ember Shell cast: for 2 rounds every hit the caster lands, Azure Dragon Palm's 58-power pierce included, returns nearly half its damage as health, and Azure Dragon Palm's heal ticks reach 300 HP (the +5 guardrail). Rising Steam is the fourth purchase here so the leech window is also the damage window; Scalding Backlash (Reflect 43%) is the pure-sustain alternative. Damage power and Afterburn are untouched.
- **Wall of Steam:** The turtle: Scorch Break's Reflect 40→48% (up to 60% of each hit returned, pierce included) and Surfing Strike's Decrease Damage Taken 30→35% for their 2-round windows, with Liquid Ember Shell's Lifesteal at 43% and 270 HP heal ticks from Vapor Shroud. It carries no Rising Steam, so the build shows the offensive root is not a universal opener; Rising Steam in place of Siphoned Heat (buff 37%, exposure 37%) is the alternative fourth purchase. No Damage power, no Afterburn.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Pressure | Sustain | Bulwark |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Liquid Ember Shell | 0 | Lifesteal | self | 40% | 40% | 40% | 48% (+8) | 43% (+3) |
| Liquid Ember Shell | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Liquid Ember Shell | 2 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Drowning Strike | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Drowning Strike | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Surfing Strike | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Surfing Strike | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 35% (+5) |
| Surfing Strike | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Scorch Break | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Scorch Break | 1 | Reflect | self | 40% | 40% | 40% | 40% | 48% (+8) |
| Azure Dragon Palm | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Azure Dragon Palm | 1 | Heal | self | 25 | 27 (+2) | 27 (+2) | 30 (+5) | 27 (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Increase Damage Taken +5%, Decrease Damage Taken +5%, Afterburn +10%, Lifesteal +8%, Reflect +8%, Heal +5 (not jointly attainable)
- Supported rows in kit: 10 (AB 1, DMG 3, DDT 1, HEAL 1, IDG 1, IDT 1, LS 1, REF 1)
- Strongest full build by row-weighted total: Rising Steam, Geyser Fist, Blistering Mist, Boiling Point (raw +22, row-weighted 26)
- Lowest row-weighted node: Blistering Mist (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Drowning Strike#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Rising Steam, Geyser Fist, Caldera Burst, Blistering Mist | DMG +5, IDG +2, IDT +2, AB +3 |
| 2 | Rising Steam, Geyser Fist, Caldera Burst, Vapor Shroud | DMG +5, IDG +2, IDT +2, DDT +2, HEAL +2 |
| 3 | Rising Steam, Geyser Fist, Blistering Mist, Boiling Point | DMG +2, IDG +5, IDT +5, AB +10 |
| 4 | Rising Steam, Geyser Fist, Blistering Mist, Vapor Shroud | DMG +2, IDG +2, IDT +2, DDT +2, AB +3, HEAL +2 |
| 5 | Rising Steam, Geyser Fist, Vapor Shroud, Siphoned Heat | DMG +2, IDG +2, IDT +2, DDT +2, LS +3, HEAL +2 |
| 6 | Rising Steam, Geyser Fist, Vapor Shroud, Scalding Backlash | DMG +2, IDG +2, IDT +2, DDT +2, REF +3, HEAL +2 |
| 7 | Rising Steam, Blistering Mist, Boiling Point, Vapor Shroud | IDG +5, IDT +5, DDT +2, AB +10, HEAL +2 |
| 8 | Rising Steam, Blistering Mist, Vapor Shroud, Siphoned Heat | IDG +2, IDT +2, DDT +2, AB +3, LS +3, HEAL +2 |
| 9 | Rising Steam, Blistering Mist, Vapor Shroud, Scalding Backlash | IDG +2, IDT +2, DDT +2, AB +3, REF +3, HEAL +2 |
| 10 | Rising Steam, Vapor Shroud, Siphoned Heat, Dew of the Dragon | IDG +2, IDT +2, DDT +2, LS +8, HEAL +5 |
| 11 | Rising Steam, Vapor Shroud, Siphoned Heat, Scalding Backlash | IDG +2, IDT +2, DDT +2, LS +3, REF +3, HEAL +2 |
| 12 | Rising Steam, Vapor Shroud, Scalding Backlash, Wall of Steam | IDG +2, IDT +2, DDT +5, REF +8, HEAL +2 |
| 13 | Vapor Shroud, Siphoned Heat, Dew of the Dragon, Scalding Backlash | DDT +2, LS +8, REF +3, HEAL +5 |
| 14 | Vapor Shroud, Siphoned Heat, Scalding Backlash, Wall of Steam | DDT +5, LS +3, REF +8, HEAL +2 |

## Design notes

- Node split: two roots mirror the kit's faces. Rising Steam (+2 IDG on the Shell, +2 IDT on Drowning Strike) forks into Geyser Fist → Caldera Burst (Damage +2/+3, three Boil rows) and Blistering Mist → Boiling Point (Afterburn +3/+7, +3 IDT, +3 IDG). Vapor Shroud (+2 DDT, +2 Heal) forks into Siphoned Heat → Dew of the Dragon (Lifesteal +3/+5, Heal +3) and Scalding Backlash → Wall of Steam (Reflect +3/+5, DDT +3). No capstone secondary shares a tag with a sibling Hidden Art.
- Flats by coverage: Damage reaches three rows, so the route stops at +5 (Taiyo Kami's three-row figure), not the +6 of one- or two-row kits. Single-row tags: Afterburn 3+7 = +10 (the ceiling, as Eternal Noon); Lifesteal and Reflect 3+5 = +8, below Arashima's +10 lifesteal because both include pierce hits; IDG, IDT and DDT 2+3 = +5 each; Heal 2+3 = +5 (the guardrail; 250 → 300 HP per tick).
- Delivery at the pin: SELF rows on area jutsu land directly on the caster once per cast (actions.ts 987–1002, 1062–1066), so Surfing Strike's DDT, Scorch Break's Reflect and the Shell's self rows are plain 2-round self buffs from the cast round, not ground effects. Drowning Strike's Damage and IDT are INHERIT rows on a GROUND spiral: ground effects on every tile within 4 of the caster, own tile excluded (util.ts 2893–2894), re-applied each round to whoever stands there (process.ts 296–340).
- Interactions: the Shell's IDG and Lifesteal and Drowning Strike's IDT are Taijutsu-filtered but element-less, so they match every element-less hit of any stat type plus Taijutsu elemental hits, the three Boil attacks included; Surfing Strike's DDT and Scorch Break's Reflect list all four stat types. Damage modifiers and Afterburn skip pierce (Azure Dragon Palm's 58 pierce gets none); Lifesteal and Reflect include it. The bloodline IDG passive multiplies enhanced Damage rows downstream.
- Uptime: every jutsu has cooldown 7. The Shell is 40 AP, range 4, single target, and needs a legal OTHER_USER target for its self rows to land; the Boil attacks and Azure Dragon Palm cost 60 AP (Drowning Strike: spiral radius 4 around the caster; Surfing Strike: radius-1 circle at range 5 plus a move; Scorch Break: radius-1 circle on a target, enemies only). Buff, IDT and Afterburn windows are 2 following rounds; the static Heal is read as two ticks of power ×10 HP.
- Fourth purchases: Burst (01,02,03) adds Vapor Shroud (32% DDT, 270 HP ticks) or Blistering Mist (Afterburn 38%); Pressure (01,04,05) adds Vapor Shroud or Geyser Fist (attacks 42/47/42); Sustain (06,07,08) adds Rising Steam (IDG and IDT 37%) or Scalding Backlash (Reflect 43%); Bulwark (06,09,10) adds Siphoned Heat (Lifesteal 43%) or Rising Steam. 01,02,04,05 (attacks 42/47/42, Afterburn 45%, IDG and IDT 40%) is the strongest unadvertised pressure build, with no mitigation.

## Risks and unproven interactions

- Classification: Boil is the single signature element on the three Damage rows (census-exclusive), but 7 of 10 supported rows are element-less and fall back to None: unreachable with affectedElements=['Boil'], reachable with None only along with every non-elemental row on any jutsu the player casts. Assumes the proposed bloodline-scoped label; normal-jutsu Boil use unverified.
- Ally hazard (validator warns): Drowning Strike row 1 IDT is an INHERIT row on a GROUND spiral with friendly fire none (=ALL): allies within 4 of the caster at the cast, or stepping onto a spiral tile while the ground effect lasts, take the exposure too. Rising Steam (+2) and Boiling Point (+3) raise it on them to 37% / 40%; the Damage row (friendly fire ENEMIES) is unaffected. Positioning decides.
- Lifesteal (user-owned value): Dew of the Dragon puts the Shell's Lifesteal at 48% for 2 rounds on every hit the caster lands, basic attacks, weapons, normal jutsu and Azure Dragon Palm's pierce included, sharing the 60%-of-pre-shield-damage leech budget with any vamp. +8 rather than Arashima's +10 keeps the sustain capstone below the burn capstone; +10 (+3/+7) would still fit the cap.
- Afterburn: Boiling Point makes the Shell's Afterburn 45% on one target for 2 following rounds; each non-pierce hit it takes adds floor(damage × 0.45) up to a cumulative 60% of that hit, so a second Afterburn source saturates the cap and part of the +10 is lost. Not simulated. Casting the Shell on an ally for its self rows afterburns that ally.
- Reflect: Wall of Steam returns 48% of each hit the caster takes during Scorch Break's 2-round window, pierce included, capped at 60% of pre-shield damage and bypassing shields; the self row needs a legal OTHER_USER target on the cast. The route carries no Damage, Afterburn or IDG, so the turtle is deliberately the weakest burst option. Realized value depends on incoming damage; not simulated.
- Damage is formula-calculated (sqrt stat scaling on Taijutsu / Speed, Strength) and then multiplied by the bloodline's IDG passive, the Shell's buff and Drowning Strike's exposure, so +5 raw power is not a linear +5 damage. All three Damage rows are area deliveries, so the +5 is paid on every enemy hit and realized value scales with target count, which was not modelled.
- Heal timing: Azure Dragon Palm's Heal is static power 25 with rounds 2, read as two ticks of power ×10 HP on the following rounds (250 → 270 → 300 HP per tick); tick count and pool were not simulated. It rides a 60 AP single-target cast whose 58-power pierce is unsupported, so +5 Heal is at most +100 HP per 7-round cycle: the lowest-value flat in the tree by HP.
- Unsupported rows and scope: Surfing Strike's move and Azure Dragon Palm's pierce receive nothing; the kit has no hidden, item-gated, mode-restricted, injected or adverse rows, and the Water DDT passive is not a potency target. Skill-tree effects are skipped in ranked modes. Non-dominance of full allocations is arithmetic, not evidence of equal combat strength; no combat simulation.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Vaporia jutsu inherit Boil potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

