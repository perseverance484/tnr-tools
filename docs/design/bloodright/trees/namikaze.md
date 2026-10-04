# Namikaze — The Shearing Sky

**Bloodline:** Namikaze (BR-048, rank C, `0Uc2Nfgg08kqGm78QAwZ4`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Wind classification / forked tree · **Classification:** Wind (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Wind offense from Wind at the Back — self Increase Damage Given on Cutting Tempest and the hidden Soaring Fujin, paid off by a controlled +2 Damage on the three Wind hits · secondary Pressure — Afterburn on Tempest Shroud's circle (enemy debuff, ally hazard), landing on every later non-pierce hit the target takes · tertiary Control from Eye of the Storm — self Decrease Damage Taken on Tempest Shroud (Fortress) or enemy Decrease Damage Given on Wind Step's circle (Suppression).

2026-10-04 rebalance under BALANCE_REVIEW_METHOD.md. Wind at the Back answers "How do I turn the wind into killing pressure: cut harder myself, or make every hit on them burn?": Cleaving Cyclone sharpens both self buffs on its Hidden Art (Razor Crosswind) and pays off with +2 Damage (Cutting Tempest 45 → 47, the two circles 40 → 42; no kit row crosses a tier); Fanning the Flames takes Tempest Shroud's Afterburn 35 → 45%. Eye of the Storm answers "How do I win the exchange defensively: weather their blows, or smother them?": Heart of the Tempest takes Shroud's self Decrease Damage Taken 30 → 40% and Dead Calm takes Wind Step's Decrease Damage Given 30 → 40%. Move and pool-cost rows are unsupported. Potency reaches matching supported tags on all Wind jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Wind at the Back | Foundation | How do I turn the wind into killing pressure: cut harder myself, or make every hit on them burn? |
| Eye of the Storm | Foundation | How do I win the exchange defensively: weather their blows, or smother them? |
| Cleaving Cyclone | Advanced Art | burst: self-buff setup, controlled raw-Damage payoff |
| Fanning the Flames | Advanced Art | burn pressure: downstream Afterburn every attacker feeds (ally hazard in the circle) |
| Heart of the Tempest | Advanced Art | fortress: guard the caster |
| Dead Calm | Advanced Art | suppression: blunt every enemy in the zone for the whole party |

- Concern: Heart of the Tempest and Dead Calm are single-effect capstones, lighter than Arashima, whose kit has the same one Decrease Damage Taken row and one Decrease Damage Given row (Unbroken Horizon adds +2% Lifesteal; Silence After Thunder adds +2% Decrease Damage Taken). Namikaze has no sustain tag and Eye of the Storm already gives each path +2% of the sibling defensive tag, so they are kept to one identity each; if the director wants Arashima parity, +2% of the sibling defensive tag fits each capstone (all-defense 4-BP builds +10% / +7% instead of +10% / +5%).
- Concern: Fanning the Flames plus Razor Crosswind (+6% Increase Damage Given, +10% Afterburn) is the strongest offence allocation. Every attacker's non-pierce hits feed the burn, so its edge over Cleaving Cyclone grows with party size, and allies inside the circle are burned too; not simulated.
- Concern: Off-kit Wind Damage rows are unverified: a 50-power Wind jutsu would read 50 → 52 and a 38-power one 38 → 40 under Cleaving Cyclone. The kit's 45/40/40 rows cross no tier.
- Concern: Soaring Fujin's obtainability is unverified; without it Increase Damage Given is one Wind-only row and Razor Crosswind is a thin setup.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Wind jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Wind at the Back | Foundation | None | +3% Increase Damage Given (self buff) | Cutting Tempest, Soaring Fujin / 2 |
| 02 | Razor Crosswind | Hidden Art | Wind at the Back | +3% Increase Damage Given (self buff) | Cutting Tempest, Soaring Fujin / 2 |
| 03 | Cleaving Cyclone | Advanced Art | Razor Crosswind | +2 Damage (damage) | Cutting Tempest, Tempest Shroud, Wind Step / 3 |
| 04 | Searing Squall | Hidden Art | Wind at the Back | +3% Afterburn (enemy debuff) | Tempest Shroud / 1 |
| 05 | Fanning the Flames | Advanced Art | Searing Squall | +7% Afterburn (enemy debuff) | Tempest Shroud / 1 |
| 06 | Eye of the Storm | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Tempest Shroud, Wind Step / 2 |
| 07 | Windward Guard | Hidden Art | Eye of the Storm | +3% Decrease Damage Taken (self buff) | Tempest Shroud / 1 |
| 08 | Heart of the Tempest | Advanced Art | Windward Guard | +5% Decrease Damage Taken (self buff) | Tempest Shroud / 1 |
| 09 | Smothering Headwind | Hidden Art | Eye of the Storm | +3% Decrease Damage Given (enemy debuff) | Wind Step / 1 |
| 10 | Dead Calm | Advanced Art | Smothering Headwind | +5% Decrease Damage Given (enemy debuff) | Wind Step / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Wind at the Back** — Every stride is carried; the gale behind you lends its weight to the blade. Cutting Tempest self buff 35 → 38% (Wind hits only, 2 rounds, CD 6); hidden Soaring Fujin 21.25 → 24.25% (nearly every hit, 2 rounds, CD 6).
- **Razor Crosswind** — Turn the gale edge-on and every cut that rides it bites deeper. Setup: Cutting Tempest buff 38 → 41% and Soaring Fujin 24.25 → 27.25% with Wind at the Back; on a hit inside both windows they compound (×1.41 × 1.2725 ≈ ×1.79).
- **Cleaving Cyclone** — The whole sky leans into one cut. Burst payoff: Cutting Tempest 45 → 47, Tempest Shroud and Wind Step 40 → 42 EP (no kit row crosses a tier; off-kit Wind rows are unverified, see risks). The 41% buff multiplies the circle hits that follow Cutting Tempest.
- **Searing Squall** — Fast air over an open wound burns hotter than any flame. Tempest Shroud Afterburn 35 → 38% for the 2 rounds after the cast on every other user in the circle, allies included; it lands on every non-pierce hit they take.
- **Fanning the Flames** — Feed the fire its favourite thing: more wind. Burn pressure: Tempest Shroud Afterburn 35 → 45% on the full route (+10%): every later non-pierce hit the target takes, from anyone, adds 45% (60% per-hit cap).
- **Eye of the Storm** — At the still centre nothing lands clean, and nothing thrown from inside flies true. Tempest Shroud self Decrease Damage Taken 30 → 32% (non-pierce hits); Wind Step circle Decrease Damage Given 30 → 32% on enemies on its tiles.
- **Windward Guard** — Stand where the gale breaks first and let it take the blow. Tempest Shroud Decrease Damage Taken 32 → 35% with Eye of the Storm; one self row, 2 rounds per 60 AP A-rank cast, CD 7.
- **Heart of the Tempest** — At the tempest's heart the wall of wind takes the blows meant for you. Fortress: Tempest Shroud Decrease Damage Taken 30 → 40% on the full route (+10%), on every non-pierce hit taken in the 2 rounds after the cast.
- **Smothering Headwind** — Every swing thrown into the wind arrives spent. Wind Step Decrease Damage Given 32 → 35% with Eye of the Storm; the 2-round circle re-applies a one-round debuff each round to enemies on it.
- **Dead Calm** — When the air goes dead, so does the arm that swings through it. Suppression: Wind Step Decrease Damage Given 30 → 40% on the full route (+10%) on every enemy standing in the circle, against anyone they hit.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Cleaving Cyclone (Burst) | Wind at the Back, Razor Crosswind, Cleaving Cyclone, Eye of the Storm | +2 | +6% | +2% | +2% | — |
| Fanning the Flames (Burn pressure) | Wind at the Back, Searing Squall, Fanning the Flames, Razor Crosswind | — | +6% | — | — | +10% |
| Heart of the Tempest (Fortress) | Eye of the Storm, Windward Guard, Heart of the Tempest, Smothering Headwind | — | — | +5% | +10% | — |
| Dead Calm (Suppression) | Eye of the Storm, Smothering Headwind, Dead Calm, Wind at the Back | — | +3% | +10% | +2% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Cleaving Cyclone:** Self-buff setup into a controlled Damage payoff: Cutting Tempest buff 35 → 41% and Soaring Fujin 21.25 → 27.25% (×1.41 × 1.2725 ≈ ×1.79 on a hit in both windows, ×1.64 unmodified), then +2 Damage on all three Wind hits (47/42/42 EP; no kit row changes tier). Eye of the Storm is the fourth purchase (Shroud Decrease Damage Taken and Wind Step suppression 32%); Searing Squall (Afterburn 38%) is the all-in alternative.
- **Fanning the Flames:** Tempest Shroud Afterburn 35 → 45% for the 2 rounds after the cast on every other user in the circle (allies included): every non-pierce hit the target takes, from the player, allies or weapons, adds 45% more. Razor Crosswind is the strongest fourth: buffs 41% / 27.25% enlarge the hits that feed the burn, with no flat Damage. Eye of the Storm (32% / 32%) is the safer alternative.
- **Heart of the Tempest:** Tempest Shroud Decrease Damage Taken 30 → 40% for the 2 rounds after each A-rank cast. Smothering Headwind is the fourth purchase: Wind Step suppression 35% on a second CD 7 cast, so staggered casts cover more rounds. Wind at the Back (buffs 38% / 24.25%) is the counter-attack alternative.
- **Dead Calm:** Wind Step Decrease Damage Given 30 → 40% on every enemy standing in the circle, against anyone they hit, with Shroud Decrease Damage Taken 32%. Wind at the Back is the fourth purchase (buffs 38% / 24.25%), so the dead-air zone is also a window to cut; Windward Guard (Shroud 35%) is the all-defense alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Wind Step | 0 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Wind Step | 1 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Wind Step | 2 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 35% (+5) | 40% (+10) |
| Tempest Shroud | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Tempest Shroud | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 40% (+10) | 32% (+2) |
| Tempest Shroud | 2 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Cutting Tempest | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Cutting Tempest | 1 | Increase Damage Given | self | 35% | 41% (+6) | 41% (+6) | 35% | 38% (+3) |
| Soaring Fujin | 0 | Increase Damage Given | self | 21.25% | 27.25% (+6) | 27.25% (+6) | 21.25% | 24.25% (+3) |
| Soaring Fujin | 1 | decreasepoolcost (unsupported) | self | 18.75% | 18.75% | 18.75% | 18.75% | 18.75% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +6% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Cleaving Cyclone: +2 Damage (0 + 0 + 2; off band)
  - Route Fanning the Flames: +10% Afterburn (0 + 3 + 7; on band)
  - Route Heart of the Tempest: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Dead Calm: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 8 (AB 1, DMG 3, DDG 1, DDT 1, IDG 2)
- Strongest full build by row-weighted total: Wind at the Back, Razor Crosswind, Searing Squall, Fanning the Flames (raw +16, row-weighted 22)
- Lowest row-weighted node: Searing Squall (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Tempest Shroud#2

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Wind Step | 1 | 40 (Normal) | 42 (Normal) |
| Tempest Shroud | 0 | 40 (Normal) | 42 (Normal) |
| Cutting Tempest | 0 | 45 (High) | 47 (High) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Cleaving Cyclone | +2 Damage, +6% IDG | Searing Squall | +2 Damage, +6% IDG, +3% AB | 21 |
| Cleaving Cyclone | +2 Damage, +6% IDG | Eye of the Storm *(highest diagnostic)* | +2 Damage, +6% IDG, +2% DDG, +2% DDT | 22 |
| Fanning the Flames | +3% IDG, +10% AB | Razor Crosswind *(highest diagnostic)* | +6% IDG, +10% AB | 22 |
| Fanning the Flames | +3% IDG, +10% AB | Eye of the Storm | +3% IDG, +2% DDG, +2% DDT, +10% AB | 20 |
| Heart of the Tempest | +2% DDG, +10% DDT | Wind at the Back *(highest diagnostic)* | +3% IDG, +2% DDG, +10% DDT | 18 |
| Heart of the Tempest | +2% DDG, +10% DDT | Smothering Headwind | +5% DDG, +10% DDT | 15 |
| Dead Calm | +10% DDG, +2% DDT | Wind at the Back *(highest diagnostic)* | +3% IDG, +10% DDG, +2% DDT | 18 |
| Dead Calm | +10% DDG, +2% DDT | Windward Guard | +10% DDG, +5% DDT | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Wind at the Back, Razor Crosswind, Cleaving Cyclone, Searing Squall | +2 Damage, +6% IDG, +3% AB |
| 2 | Wind at the Back, Razor Crosswind, Cleaving Cyclone, Eye of the Storm | +2 Damage, +6% IDG, +2% DDG, +2% DDT |
| 3 | Wind at the Back, Razor Crosswind, Searing Squall, Fanning the Flames | +6% IDG, +10% AB |
| 4 | Wind at the Back, Razor Crosswind, Searing Squall, Eye of the Storm | +6% IDG, +2% DDG, +2% DDT, +3% AB |
| 5 | Wind at the Back, Razor Crosswind, Eye of the Storm, Windward Guard | +6% IDG, +2% DDG, +5% DDT |
| 6 | Wind at the Back, Razor Crosswind, Eye of the Storm, Smothering Headwind | +6% IDG, +5% DDG, +2% DDT |
| 7 | Wind at the Back, Searing Squall, Fanning the Flames, Eye of the Storm | +3% IDG, +2% DDG, +2% DDT, +10% AB |
| 8 | Wind at the Back, Searing Squall, Eye of the Storm, Windward Guard | +3% IDG, +2% DDG, +5% DDT, +3% AB |
| 9 | Wind at the Back, Searing Squall, Eye of the Storm, Smothering Headwind | +3% IDG, +5% DDG, +2% DDT, +3% AB |
| 10 | Wind at the Back, Eye of the Storm, Windward Guard, Heart of the Tempest | +3% IDG, +2% DDG, +10% DDT |
| 11 | Wind at the Back, Eye of the Storm, Windward Guard, Smothering Headwind | +3% IDG, +5% DDG, +5% DDT |
| 12 | Wind at the Back, Eye of the Storm, Smothering Headwind, Dead Calm | +3% IDG, +10% DDG, +2% DDT |
| 13 | Eye of the Storm, Windward Guard, Heart of the Tempest, Smothering Headwind | +5% DDG, +10% DDT |
| 14 | Eye of the Storm, Windward Guard, Smothering Headwind, Dead Calm | +10% DDG, +5% DDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Kept: graph, names, both Foundations, Burn and both defensive Hidden Arts. Changed: Razor Crosswind +2 Damage → +3% Increase Damage Given; Cleaving Cyclone +3 → +2 Damage; Fanning the Flames and Heart of the Tempest drop their +2% Increase Damage Given; Dead Calm drops its +1 Damage. The old +5 Damage route lifted Wind Step and Tempest Shroud 40 → 45 (Normal → High) and Cutting Tempest 45 → 50 (semi-nuke → Nuke); Damage on the Hidden Art also let Burn buy +2 Damage as its fourth on top of +5% Increase Damage Given and +10% Afterburn. Roster pass (R1–R7): values and structure unchanged. The kit's Damage rows are 45/40/40 with no 50 row, so R1 does not apply; Cleaving Cyclone already follows Arashima's Sundered Sky pattern (percentage setup on the Hidden Art, +2 Damage payoff, R5 default for 45/40 rows). Prose now limits the tier claim to the kit.
- Impact envelope. Damage: three Wind rows (45/40/40), every hit in the kit; +2 moves none of them across a tier. Increase Damage Given: two self rows (Cutting Tempest Wind-only; hidden Soaring Fujin nearly every hit) that compound with each other and with the bloodline's Wind passive, each live 2 rounds after a CD 6 cast. Afterburn: one Shroud row, but it lands on every later non-pierce hit the target takes from anyone, the most downstream leverage in the kit. Decrease Damage Taken and Decrease Damage Given: one element-less 30% row each, 2 rounds per CD 7 cast; each route stops at +10% (30 → 40%) with no rider.
- Maxima over every legal allocation: Damage +2, Increase Damage Given +6%, Afterburn +10%, Decrease Damage Taken +10%, Decrease Damage Given +10%. Only Cleaving Cyclone carries Damage and only Wind at the Back and Razor Crosswind carry Increase Damage Given; no capstone shares a tag with its sibling Hidden Art. The strongest offence allocation, Fanning the Flames plus Razor Crosswind, reaches +6% Increase Damage Given and +10% Afterburn with no flat Damage (the previous tree reached +2 Damage, +5% Increase Damage Given and +10% Afterburn there).
- Matching and timing (§3, §3b): Cutting Tempest's buff lists Wind with no stat or general filter, so it reaches Wind hits only; Soaring Fujin's row reaches nearly every hit; Shroud's Decrease Damage Taken and Afterburn and Wind Step's Decrease Damage Given are element-less with all four stat types, so they cover every non-pierce hit. Each buff or debuff is live in the two rounds after its cast, never in it, so Cutting Tempest's buff never helps its own hit and lifts the circle hits that follow.

## Risks and unproven interactions

- Ally hazard: Shroud's Afterburn row is INHERIT on an OTHER_USER circle with friendly fire absent (= ALL), so every other user in the circle, allies included, receives it (38% with Searing Squall, 45% with Fanning the Flames); the caster never does and no ground effect is created (actions.ts 1029-1060; §4b). Damage is ENEMIES-only and Decrease Damage Taken SELF, so only the burn leaks.
- Afterburn is downstream: at 45% every non-pierce hit a debuffed target takes (kit, normal jutsu, weapons, allies) adds floor(damage × 45%); Afterburn sources stack (process.ts 1109-1117) but cap at 60% of each hit. Its value grows with party size; not simulated.
- Classification: Wind is shared with many other bloodlines (expected under RUL-2026-10-03-005). 5 of 8 kit rows carry Wind; the three element-less rows (Shroud's Decrease Damage Taken and Afterburn, Wind Step's Decrease Damage Given) need the proposed jutsu-classification resolver. Off-kit Wind coverage is unverified, Damage included: an off-kit 50-power Wind Damage row would read 50 → 52 under Cleaving Cyclone (past the Nuke tier) and a 38-power one 38 → 40 (Light → Normal); the kit's own 45/40/40 rows cross no tier. This stays unverified until a public jutsu catalog is captured.
- Soaring Fujin is a hidden NORMAL-type jutsu whose obtainability was not verified; if uncastable, Increase Damage Given reaches only Cutting Tempest's Wind-only row and the Burst setup narrows to one buff.
- Delivery: Tempest Shroud's Decrease Damage Taken is a SELF row realized on the caster at cast time (actions.ts 1060-1075; §4b); the cast needs another living user within range 4. Wind Step's 2-round ground circle re-applies a one-round Decrease Damage Given each round to enemies on its tiles (process.ts 321-340); one who steps off loses it at that round's end.
- Context not modelled: the +10% Fire Increase Damage Taken passive (a standing weakness) is untouched; skill-tree and bloodline effects are suppressed in RANKED_PVP and RANKED_SPARRING; same-tag potency sources sum at the pin, so a combined audit with any normal-tree potency precedes implementation. Value decisions are user-owned; no combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Wind jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

