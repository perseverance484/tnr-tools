# Vaporia — Scald and Steam

**Bloodline:** Vaporia (BR-090, rank A, `f7IgtcsLqomqmmBgAYS1O`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Boil classification / forked tree · **Classification:** Boil (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Rush offense from Rising Steam: +2 Damage on the three Boil attacks (Drowning Strike 40, Surfing Strike 45, Scorch Break 40 EP) with Drowning Strike's spiral exposure on the payoff, or Afterburn branded on the Liquid Ember Shell's target · secondary Outlasting the exchange from Vapor Shroud: Lifesteal with an Azure Dragon Palm Heal rider, or Reflect behind Decrease Damage Taken · tertiary Foundation glue: Increase Damage Given and Increase Damage Taken on Rising Steam, Decrease Damage Taken on Vapor Shroud.

The kit's ten supported rows are three Boil Taijutsu formula Damage rows (40/45/40 EP at jutsu level 25) on 60 AP area attacks and seven single-row tags, three of them on one 40 AP Liquid Ember Shell cast (Lifesteal 40% and Increase Damage Given 35% on the caster, Afterburn 35% on the target). Rising Steam answers "How do I make the rush hit harder: scald everyone around me or brand one target?": the Burst route commits +1 Damage on Geyser Fist and Caldera Burst pays off with +1 Damage more (+2 on all three attacks, no tier crossing) and Drowning Strike's spiral exposure at 40%, Boiling Point brands the Shell's target with +10% Afterburn. Vapor Shroud answers "How do I outlast the exchange: heal through my own hits or punish theirs?": Dew of the Dragon reaches the +5% Lifesteal ceiling with a palm Heal rider, Wall of Steam returns 50% of incoming hits behind 35% Decrease Damage Taken. Potency reaches matching supported tags on all Boil jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Rising Steam | Foundation | How do I make the rush hit harder: scald everyone around me or brand one target? |
| Vapor Shroud | Foundation | How do I outlast the exchange: heal through my own hits or punish theirs? |
| Caldera Burst | Advanced Art | area burst: +1 Damage commit, then +1 Damage with the spiral exposure (+2 Damage, 40% exposure) |
| Boiling Point | Advanced Art | branded-target attrition (Afterburn) |
| Dew of the Dragon | Advanced Art | sustain (Lifesteal with a palm Heal rider) |
| Wall of Steam | Advanced Art | retaliation fortress (Reflect behind Decrease Damage Taken) |

- Concern: Caldera Burst raises Drowning Strike's ally-hazard exposure to 40% on everyone standing in the spiral, allies and a caster who steps onto it included; every other build stops at 37%.
- Concern: Caldera Burst depends on sequencing: its 40% exposure reaches only Surfing Strike and Scorch Break cast in the two rounds after Drowning Strike against targets still on the spiral tiles; Drowning Strike's own 42 EP hit never meets it.
- Concern: Geyser Fist carries +1 flat Damage on a Hidden Art, against the roster's flat-Damage-on-Advanced convention (R6), because the Burst's percentage set-up (spiral exposure) multiplied the sibling Afterburn as Boiling Point's obvious fourth (R1). It gives Burn a real fourth choice: +1 EP on its own three attacks or Decrease Damage Taken 32%.
- Concern: Burst + Blistering Mist still pairs Caldera Burst's 40% exposure with a 38% Afterburn, but Blistering Mist adds only +3% (×1.38 / 1.35 ≈ ×1.022). On one target the two offensive builds are level on the kit's attacks (Burn + Geyser Fist 111.6, Burst + Blistering Mist 111.2 EP-equivalent on a 40 EP base); Burn leads on allies' hits (×1.99 against ×1.93), Burst on every other target in the spiral (80.6 against 77.0 per 40 EP follow-up). Not simulated.
- Concern: Burn and Sustain both deepen the one Liquid Ember Shell cast; their realized value depends on sequencing and was not simulated.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Boil jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Rising Steam | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Drowning Strike, Liquid Ember Shell / 2 |
| 02 | Geyser Fist | Hidden Art | Rising Steam | +1 Damage (damage) | Drowning Strike, Scorch Break, Surfing Strike / 3 |
| 03 | Caldera Burst | Advanced Art | Geyser Fist | +1 Damage (damage); +3% Increase Damage Taken (enemy debuff) | Drowning Strike, Scorch Break, Surfing Strike / 4 |
| 04 | Blistering Mist | Hidden Art | Rising Steam | +3% Afterburn (enemy debuff) | Liquid Ember Shell / 1 |
| 05 | Boiling Point | Advanced Art | Blistering Mist | +7% Afterburn (enemy debuff) | Liquid Ember Shell / 1 |
| 06 | Vapor Shroud | Foundation | None | +2% Decrease Damage Taken (self buff) | Surfing Strike / 1 |
| 07 | Siphoned Heat | Hidden Art | Vapor Shroud | +2% Lifesteal (self buff) | Liquid Ember Shell / 1 |
| 08 | Dew of the Dragon | Advanced Art | Siphoned Heat | +3% Lifesteal (self buff); +5% Heal (self buff) | Azure Dragon Palm, Liquid Ember Shell / 2 |
| 09 | Scalding Backlash | Hidden Art | Vapor Shroud | +3% Reflect (self buff) | Scorch Break / 1 |
| 10 | Wall of Steam | Advanced Art | Scalding Backlash | +7% Reflect (self buff); +3% Decrease Damage Taken (self buff) | Scorch Break, Surfing Strike / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Rising Steam** — Heat climbs the blood, and the air around the quarry thickens. Liquid Ember Shell self buff 35 → 37% (2 rounds); Drowning Strike exposure 35 → 37% on its spiral tiles (ally hazard).
- **Geyser Fist** — Steam bursts from the ground beneath the fist and lends every blow its heat. Burst commit: the three Boil attacks +1 Damage on the cast itself (Drowning Strike and Scorch Break 40 → 41, Surfing Strike 45 → 46 EP). A flat commit, not the spiral exposure: exposure here would be Boiling Point's obvious fourth and multiply its Afterburn.
- **Caldera Burst** — The whole basin boils over at once; nothing standing in it is spared. Burst payoff, route total +2 Damage: Drowning Strike and Scorch Break 40 → 42, Surfing Strike 45 → 47 EP (no tier crossing); with Rising Steam, Drowning Strike's spiral exposure 35 → 40% on every tile within 4 of the caster (2 rounds; ally hazard). Surfing Strike and Scorch Break cast in the two rounds after Drowning Strike meet that 40% on targets still on the tiles; Drowning Strike's own hit never does.
- **Blistering Mist** — Steam clings where it lands and keeps on burning long after the blow. Liquid Ember Shell Afterburn 35 → 38% on its target (2 rounds); every matching non-pierce hit it takes adds that share, 60% cap per hit.
- **Boiling Point** — Past this heat there is no simmer left, only the roar. Burn route total +10%: Liquid Ember Shell Afterburn 35 → 45% on its target for 2 rounds; every matching non-pierce hit it takes, allies' included, adds 45% (60% cap per hit).
- **Vapor Shroud** — A veil of steam wraps the body and turns aside part of every blow. Surfing Strike Decrease Damage Taken 30 → 32% (self, 2 rounds after the 60 AP rush).
- **Siphoned Heat** — Every wound dealt gives its warmth back to the one who made it. Liquid Ember Shell Lifesteal 40 → 42% (self, 2 rounds); draws from every matching hit (element-less hits of any stat type, Taijutsu elemental hits, and pierce); shares the 60% leech cap with vamp.
- **Dew of the Dragon** — What rose as steam settles again as cool water on the dragon's scales. Sustain route total +5% Lifesteal (Liquid Ember Shell 40 → 45%; +5% is the hard ceiling); Azure Dragon Palm Heal 25 → 30 (250 → 300 HP per tick).
- **Scalding Backlash** — Strike the kettle and the kettle answers with its contents. Scorch Break Reflect 40 → 43% (self, 2 rounds); returns that share of each hit taken, pierce included, 60% cap per hit.
- **Wall of Steam** — Stand behind the boil and let the enemy learn what it costs to reach through. Retaliation route total +10%: Scorch Break Reflect 40 → 50% (under the 60% cap); with Vapor Shroud, Surfing Strike Decrease Damage Taken 30 → 35% (self, 2 rounds).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | LS | REF | HEAL |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Caldera Burst (Burst) | Rising Steam, Geyser Fist, Caldera Burst, Blistering Mist | +2 | +2% | +5% | — | +3% | — | — | — |
| Boiling Point (Burn) | Rising Steam, Blistering Mist, Boiling Point, Vapor Shroud | — | +2% | +2% | +2% | +10% | — | — | — |
| Dew of the Dragon (Sustain) | Rising Steam, Vapor Shroud, Siphoned Heat, Dew of the Dragon | — | +2% | +2% | +2% | — | +5% | — | +5% |
| Wall of Steam (Retaliation) | Vapor Shroud, Siphoned Heat, Scalding Backlash, Wall of Steam | — | — | — | +5% | — | +2% | +10% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal · REF = Reflect · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Caldera Burst:** A +1 Damage commit into the area payoff: +2 Damage on all three Boil attacks (Drowning Strike and Scorch Break 40 → 42, Surfing Strike 45 → 47 EP; no tier crossing) and Drowning Strike's spiral exposure 35 → 40% (Rising Steam +2%, Caldera Burst +3%; ally hazard); Surfing Strike and Scorch Break in the two rounds after Drowning Strike hit into the 40% exposure, with the Shell buff at 37%. Blistering Mist is the strongest fourth purchase (Afterburn 38%); Vapor Shroud (Decrease Damage Taken 32%) is the defensive alternative.
- **Boiling Point:** Brand one target: Liquid Ember Shell's Afterburn 35 → 45% for 2 rounds, so every matching non-pierce hit it takes, allies' included, adds 45% more (60% cap per hit); Rising Steam puts the Shell buff and Drowning Strike's exposure at 37%. Vapor Shroud is the fourth purchase here (Decrease Damage Taken 32%); Geyser Fist (+1 Damage on the three Boil attacks, exposure stays 37%) is the all-offence alternative.
- **Dew of the Dragon:** Lifesteal 40 → 45% (the +5% hard ceiling) on the Liquid Ember Shell window: for 2 rounds every matching hit the caster lands (element-less hits, Taijutsu elemental hits such as the three Boil attacks, and pierce such as Azure Dragon Palm's 58 EP) returns 45% within the shared 60% leech budget; Azure Dragon Palm's Heal 25 → 30 (300 HP per tick) and Surfing Strike's Decrease Damage Taken 32%. Rising Steam is the fourth purchase so the leech window is also a 37% damage window; Scalding Backlash (Reflect 43%) is the all-defence alternative.
- **Wall of Steam:** Scorch Break's Reflect 40 → 50% (pierce included, under the 60% per-hit cap) and Surfing Strike's Decrease Damage Taken 30 → 35% for their 2-round windows, with the Shell's Lifesteal at 42% from Siphoned Heat as the fourth purchase. No Damage, Afterburn or Increase Damage Given; Rising Steam is the alternative fourth (Shell buff and exposure 37%).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn | Sustain | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Liquid Ember Shell | 0 | Lifesteal | self | 40% | 40% | 40% | 45% (+5) | 42% (+2) |
| Liquid Ember Shell | 1 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |
| Liquid Ember Shell | 2 | Afterburn | enemy | 35% | 38% (+3) | 45% (+10) | 35% | 35% |
| Drowning Strike | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Drowning Strike | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Surfing Strike | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Surfing Strike | 1 | Decrease Damage Taken | self | 30% | 30% | 32% (+2) | 32% (+2) | 35% (+5) |
| Surfing Strike | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Scorch Break | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Scorch Break | 1 | Reflect | self | 40% | 40% | 40% | 40% | 50% (+10) |
| Azure Dragon Palm | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Azure Dragon Palm | 1 | Heal | self | 25 | 25 | 25 | 30 (+5) | 25 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +2% Increase Damage Given, +5% Increase Damage Taken, +5% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal, +10% Reflect, +5% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Caldera Burst: +2 Damage (0 + 1 + 1; off band)
  - Route Boiling Point: +10% Afterburn (0 + 3 + 7; on band)
  - Route Dew of the Dragon: +5% Lifesteal (0 + 2 + 3; on band)
  - Route Wall of Steam: +10% Reflect (0 + 3 + 7; on band)
- Supported rows in kit: 10 (AB 1, DMG 3, DDT 1, HEAL 1, IDG 1, IDT 1, LS 1, REF 1)
- Strongest full build by row-weighted total: Rising Steam, Vapor Shroud, Scalding Backlash, Wall of Steam (raw +19, row-weighted 19)
- Lowest row-weighted node: Vapor Shroud (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Drowning Strike#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +1 Damage | +2 Damage |
|---|---:|---|---|---|
| Drowning Strike | 0 | 40 (Normal) | 41 (Normal) | 42 (Normal) |
| Surfing Strike | 0 | 45 (High) | 46 (High) | 47 (High) |
| Scorch Break | 0 | 40 (Normal) | 41 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Caldera Burst | +2 Damage, +2% IDG, +5% IDT | Blistering Mist *(highest diagnostic)* | +2 Damage, +2% IDG, +5% IDT, +3% AB | 16 |
| Caldera Burst | +2 Damage, +2% IDG, +5% IDT | Vapor Shroud | +2 Damage, +2% IDG, +5% IDT, +2% DDT | 15 |
| Boiling Point | +2% IDG, +2% IDT, +10% AB | Geyser Fist *(highest diagnostic)* | +1 Damage, +2% IDG, +2% IDT, +10% AB | 17 |
| Boiling Point | +2% IDG, +2% IDT, +10% AB | Vapor Shroud | +2% IDG, +2% IDT, +2% DDT, +10% AB | 16 |
| Dew of the Dragon | +2% DDT, +5% LS, +5% HEAL | Rising Steam *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +5% LS, +5% HEAL | 16 |
| Dew of the Dragon | +2% DDT, +5% LS, +5% HEAL | Scalding Backlash | +2% DDT, +5% LS, +3% REF, +5% HEAL | 15 |
| Wall of Steam | +5% DDT, +10% REF | Rising Steam *(highest diagnostic)* | +2% IDG, +2% IDT, +5% DDT, +10% REF | 19 |
| Wall of Steam | +5% DDT, +10% REF | Siphoned Heat | +5% DDT, +2% LS, +10% REF | 17 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Rising Steam, Geyser Fist, Caldera Burst, Blistering Mist | +2 Damage, +2% IDG, +5% IDT, +3% AB |
| 2 | Rising Steam, Geyser Fist, Caldera Burst, Vapor Shroud | +2 Damage, +2% IDG, +5% IDT, +2% DDT |
| 3 | Rising Steam, Geyser Fist, Blistering Mist, Boiling Point | +1 Damage, +2% IDG, +2% IDT, +10% AB |
| 4 | Rising Steam, Geyser Fist, Blistering Mist, Vapor Shroud | +1 Damage, +2% IDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Rising Steam, Geyser Fist, Vapor Shroud, Siphoned Heat | +1 Damage, +2% IDG, +2% IDT, +2% DDT, +2% LS |
| 6 | Rising Steam, Geyser Fist, Vapor Shroud, Scalding Backlash | +1 Damage, +2% IDG, +2% IDT, +2% DDT, +3% REF |
| 7 | Rising Steam, Blistering Mist, Boiling Point, Vapor Shroud | +2% IDG, +2% IDT, +2% DDT, +10% AB |
| 8 | Rising Steam, Blistering Mist, Vapor Shroud, Siphoned Heat | +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% LS |
| 9 | Rising Steam, Blistering Mist, Vapor Shroud, Scalding Backlash | +2% IDG, +2% IDT, +2% DDT, +3% AB, +3% REF |
| 10 | Rising Steam, Vapor Shroud, Siphoned Heat, Dew of the Dragon | +2% IDG, +2% IDT, +2% DDT, +5% LS, +5% HEAL |
| 11 | Rising Steam, Vapor Shroud, Siphoned Heat, Scalding Backlash | +2% IDG, +2% IDT, +2% DDT, +2% LS, +3% REF |
| 12 | Rising Steam, Vapor Shroud, Scalding Backlash, Wall of Steam | +2% IDG, +2% IDT, +5% DDT, +10% REF |
| 13 | Vapor Shroud, Siphoned Heat, Dew of the Dragon, Scalding Backlash | +2% DDT, +5% LS, +3% REF, +5% HEAL |
| 14 | Vapor Shroud, Siphoned Heat, Scalding Backlash, Wall of Steam | +5% DDT, +2% LS, +10% REF |

## Design notes

- Graph unchanged: 01→02→03, 01→04→05, 06→07→08, 06→09→10. 2026-10-04 re-cut under BALANCE_REVIEW_METHOD.md: the pre-batch +5 route (Geyser Fist +2, Caldera Burst +3 Damage) lifted Drowning Strike and Scorch Break 40 → 45 (a full tier) and Surfing Strike 45 → 50 (semi-nuke to Nuke), so it was cut to +2; Boiling Point drops its +3% Increase Damage Taken / +3% Increase Damage Given riders for a single +7% Afterburn, since the riders multiplied the burn and Geyser Fist's +2 Damage made 01,02,04,05 the strongest build; Vapor Shroud drops its +2% Heal glue. Roster pass: no value changes; prose corrected (Lifesteal reads matching hits only, Drowning Strike's own hit never meets its exposure, +5% is the Lifesteal ceiling).
- Final review: the first pass made Geyser Fist a +3% Increase Damage Taken set-up (Caldera Burst +2 Damage), which undid its own Boiling Point fix: Geyser Fist was Boiling Point's obvious fourth, so 01,02,04,05 again laid 40% exposure under the 45% Afterburn, ×1.40 × 1.45 ≈ ×2.03 on every matching hit the brand reads, allies' included (the R1 pattern). Geyser Fist becomes a +1 Damage commit and Caldera Burst carries +1 Damage with the +3% exposure, so Burst's 3-BP package is unchanged (+2 Damage, +2% Increase Damage Given, +5% Increase Damage Taken) and exposure past Rising Steam's 37% is Burst-only. Conventions: no 50 EP row (R1 n/a); Caldera Burst carries the flat-Damage payoff (R2); exposure +5% and Afterburn +10% each reach one row (R3); no twin Hidden Arts (R4); +2 on 40/45 rows, no tier crossing (R5); 10 nodes, 2-4-4, neither Foundation universal (R7). R6 departure: Geyser Fist keeps +1 Damage on a Hidden Art because no percentage set-up passes the fourth-BP audit: exposure and the Shell's Increase Damage Given both multiply the sibling Afterburn, and Decrease Damage Taken, Lifesteal, Reflect and Heal are the defensive branch's tags. A bare +1 capstone would copy the commit and leave Burst + Blistering Mist 2.6% behind Burn + Geyser Fist on the kit's attacks (108.8 against 111.6 EP-equivalent), so Caldera Burst pairs its +1 with the exposure.
- Maxima over every legal allocation: Damage +2 (40 → 42, 45 → 47; builds with Geyser Fist but not Caldera Burst stop at +1, 41 / 46), Increase Damage Given +2%, Increase Damage Taken +5% (Burst only; +2% elsewhere), Decrease Damage Taken +5%, Afterburn +10%, Lifesteal +5%, Reflect +10%, Heal +5%. No capstone shares a tag with its sibling Hidden Art.
- Delivery at the pin: SELF rows land on the caster once per cast (actions.ts 980–1004, 1062–1066), so Surfing Strike's Decrease Damage Taken, Scorch Break's Reflect and the Shell's Lifesteal and Increase Damage Given are plain 2-round self buffs. Drowning Strike's rows are INHERIT rows on a GROUND spiral of radius 4 around the caster (own tile excluded); its 2-round exposure is a ground effect re-applied each round to whoever stands on a tile.
- Interactions: the Shell's three rows and Drowning Strike's exposure are Taijutsu-filtered but element-less, so they match every element-less hit of any stat type plus Taijutsu elemental hits, the three Boil attacks included; Afterburn reads the hit after Increase Damage Given and Increase Damage Taken. Damage modifiers and Afterburn skip pierce; Lifesteal and Reflect include it. The bloodline Increase Damage Given passive multiplies last.
- Uptime: every jutsu has cooldown 7. The Shell is 40 AP, single target, and needs a legal OTHER_USER target for its self rows; the Boil attacks and Azure Dragon Palm cost 60 AP. Buff, exposure and Afterburn windows are the 2 rounds after the cast.
- Fourth purchases: Burst (01,02,03) + Blistering Mist or Vapor Shroud; Burn (01,04,05) + Geyser Fist or Vapor Shroud; Sustain (06,07,08) + Rising Steam or Scalding Backlash; Retaliation (06,09,10) + Siphoned Heat or Rising Steam. The strongest are the offensive siblings. On a Shell-branded target standing in the spiral, during the Shell buff (Shell and Drowning Strike fit one 100 AP round), Burst + Blistering Mist gives ×1.37 × 1.40 × 1.38 ≈ ×2.65 on 42 EP follow-ups (111.2 EP-equivalent on a 40 EP base) and Burn + Geyser Fist ×1.37 × 1.37 × 1.45 ≈ ×2.72 on 41 EP (111.6), against the kit's ×1.35 × 1.35 × 1.35 ≈ ×2.46 (98.4). Allies' hits on that target take ×1.37 × 1.45 ≈ ×1.99 under Burn (×2.03 with the old Geyser Fist) against ×1.40 × 1.38 ≈ ×1.93 under Burst; every other target in the spiral takes 80.6 from a Burst follow-up on a 40 EP base against 77.0 under Burn. Both give up all mitigation. Retaliation + Rising Steam is the highest row-weighted build only because Rising Steam touches two glue rows; it stacks no tag with the capstone.

## Risks and unproven interactions

- Classification: Boil is the single signature element on the three Damage rows and no other captured bloodline has Boil jutsu; ordinary Boil jutsu are in scope by rule and unverified. 3 of 10 supported kit rows carry Boil; the other seven need the proposed jutsu-classification resolver, and Liquid Ember Shell (no Boil row) qualifies in-kit only through an authored Boil jutsu classification (ENGINE_GAP_REGISTER G1).
- Ally hazard (validator warns): Drowning Strike's Increase Damage Taken is an INHERIT ground row with friendly fire none (=ALL); allies on a spiral tile, and the caster if it steps onto one, take the exposure too. Rising Steam (+2%) and Caldera Burst (+3%) raise it to 37% / 40%; the Damage row (friendly fire ENEMIES) is unaffected. Positioning decides.
- Afterburn: Boiling Point makes the Shell's Afterburn 45% on one target for 2 rounds; a second Afterburn source saturates the 60% per-hit cap and wastes part of the +10%. Casting the Shell on an ally for its self rows afterburns that ally. Not simulated.
- Lifesteal: Dew of the Dragon's 45% reads every matching hit the caster lands in the Shell window (element-less hits of any stat type, Taijutsu elemental hits, and pierce; a non-Taijutsu elemental hit returns nothing) within the 60%-of-pre-shield-damage leech budget shared with vamp; +5% is the hard ceiling.
- Reflect: Wall of Steam returns 50% of each hit taken during Scorch Break's window, pierce included and bypassing shields; realized value depends on incoming damage. Not simulated.
- Damage: Burst's +2 (Geyser Fist +1, Caldera Burst +1) is formula power on three area attacks, multiplied by the Shell's buff and the bloodline passive, and on the two follow-up attacks by Caldera Burst's exposure; realized value scales with target count, which was not modelled.
- Heal: Azure Dragon Palm's static 25 is two ticks of 250 HP; Dew's +5% makes them 300 HP, +100 HP per 7-round cycle, a rider rather than a route.
- Unsupported rows and scope: Surfing Strike's move and Azure Dragon Palm's pierce receive nothing; no hidden, item-gated, mode-restricted, injected or adverse rows; the Water Decrease Damage Taken passive is not a potency target. Skill-tree effects are skipped in ranked modes. No combat simulation.

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

