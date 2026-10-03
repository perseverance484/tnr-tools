# Ancient Tailed Demon — Rites of the Sealed

**Bloodline:** Ancient Tailed Demon (BR-004, rank B, `Au5rBnnukEqUv_lRrk1yO`) · **Revision:** Draft 4 / Ancient Tailed Demon classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Ancient Tailed Demon (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Enemy pressure — Afterburn and Increase Damage Taken on Demonic Embrace · secondary Sustained damage — Increase Damage Given on Demonic Vitae; burst — Damage on Ancient Demon Roar · tertiary Defense — Decrease Damage Taken on Demonic Vitae.

The kit is three casts with one supported row per tag: Demonic Embrace carries the two enemy debuffs (Afterburn 35%, Increase Damage Taken 35%, 2 rounds, 40 AP), Demonic Vitae the two self buffs (Increase Damage Given 35% for 3 rounds, Decrease Damage Taken 25% for 2 rounds, 40 AP) and Ancient Demon Roar the only Damage (45 EP area hit, 60 AP). The Sustained Damage trait and the bloodline's own damage-given passive make pressure and empowerment the natural emphasis; Roar burst is a real but single-cast alternative; mitigation is tertiary because its row is the weakest (25%) and shortest (2 rounds) in the kit.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ancient Tailed Demon-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Demon's Grasp | Foundation | None | +2% Afterburn (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Demonic Embrace / 2 |
| 02 | Rending Bellow | Hidden Art | Demon's Grasp | +2 Damage (damage) | Ancient Demon Roar / 1 |
| 03 | Howl of Annihilation | Advanced Art | Rending Bellow | +3 Damage (damage); +2% Increase Damage Taken (enemy debuff) | Ancient Demon Roar, Demonic Embrace / 2 |
| 04 | Festering Brand | Hidden Art | Demon's Grasp | +3% Afterburn (enemy debuff) | Demonic Embrace / 1 |
| 05 | Consuming Malice | Advanced Art | Festering Brand | +5% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Demonic Embrace / 2 |
| 06 | Demon's Marrow | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Demonic Vitae / 2 |
| 07 | Scarred Hide | Hidden Art | Demon's Marrow | +3% Decrease Damage Taken (self buff) | Demonic Vitae / 1 |
| 08 | Unyielding Husk | Advanced Art | Scarred Hide | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Demonic Vitae / 2 |
| 09 | Boiling Ichor | Hidden Art | Demon's Marrow | +3% Increase Damage Given (self buff) | Demonic Vitae / 1 |
| 10 | Primordial Rampage | Advanced Art | Boiling Ichor | +5% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Demonic Vitae / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Demon's Grasp** — A claw closes around the prey, and what it touches begins to smoulder. Demonic Embrace only: Afterburn 35 → 37% and exposure 35 → 37% on one target for 2 rounds (40 AP, range 4, cooldown 7).
- **Rending Bellow** — The roar that cracked the old mountains has not grown quieter in its cage. Ancient Demon Roar Damage only: 45 → 47 EP at jutsu level 25 (one row, area spawn, 60 AP, range 4, cooldown 7). Its Wound row is unchanged.
- **Howl of Annihilation** — One breath, and the field remembers why the ancients sealed it away. Damage route total +5: Roar 45 → 50 EP. Embrace exposure +2% (39% with Demon's Grasp), so a Roar cast a round later lands harder.
- **Festering Brand** — Flesh the demon marks does not stop burning when the claw lets go. Demonic Embrace Afterburn 40% with Demon's Grasp; adds to every non-pierce hit the target takes for 2 rounds.
- **Consuming Malice** — Hatred older than the villages, poured into a single victim. Afterburn route total +10%: Demonic Embrace Afterburn 35 → 45% and exposure 40% with Demon's Grasp (one target, 2 rounds), below the 60% per-hit cap.
- **Demon's Marrow** — The blood runs black and hot, and the host grows harder to kill. Demonic Vitae only (self, 40 AP, cooldown 7): Increase Damage Given 35 → 37% for 3 rounds, Decrease Damage Taken 25 → 27% for 2; neither touches pierce hits.
- **Scarred Hide** — A thousand years of wounds, and every one of them closed over. Demonic Vitae Decrease Damage Taken 30% with Demon's Marrow, for 2 rounds (non-pierce hits of any stat type).
- **Unyielding Husk** — What the host cannot dodge, the demon simply refuses to feel. Decrease Damage Taken route total +10%: Demonic Vitae 25 → 35%; Increase Damage Given +2% (39% with Demon's Marrow). Pierce still passes through.
- **Boiling Ichor** — Let a little more of it loose, and every strike carries the heat. Demonic Vitae Increase Damage Given 40% with Demon's Marrow, for 3 rounds, on all your non-pierce damage (jutsu, weapons, basics).
- **Primordial Rampage** — The seal holds, barely. Everything within reach learns what that costs. Increase Damage Given route total +10%: Demonic Vitae 35 → 45% for 3 rounds; Decrease Damage Taken +2% (29% with Demon's Marrow).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Howl of Annihilation (Roar burst) | Demon's Grasp, Rending Bellow, Howl of Annihilation, Demon's Marrow | +5 | +2% | +4% | +2% | +2% |
| Consuming Malice (Burn pressure) | Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow | — | +2% | +5% | +2% | +10% |
| Unyielding Husk (Fortified) | Demon's Grasp, Demon's Marrow, Scarred Hide, Unyielding Husk | — | +4% | +2% | +10% | +2% |
| Primordial Rampage (Empowered) | Demon's Grasp, Demon's Marrow, Boiling Ichor, Primordial Rampage | — | +10% | +2% | +4% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Howl of Annihilation:** +5 Damage on Ancient Demon Roar (45 → 50 EP at jutsu level 25) on every enemy in its circle. Cast Demonic Embrace (exposure 39%, Afterburn 37%, one enemy) and Demonic Vitae (Increase Damage Given 37%, Decrease Damage Taken 27% via Demon's Marrow) a round earlier, 80 AP together, so both reach the Roar's hit on that enemy. Festering Brand (Afterburn 40%) in place of Marrow is the all-offence alternative.
- **Consuming Malice:** Demonic Embrace as the signature cast: Afterburn 45% and exposure 40% on one target, so in the 2 rounds after the cast every non-pierce hit it takes from Roar, normal jutsu, weapons and allies gains both (Afterburn route +10%, exposure +5%). Roar stays at 45 EP. Demon's Marrow adds Vitae 37% / 27% as the fourth purchase; Rending Bellow (Roar 47 EP) is the alternative.
- **Unyielding Husk:** Demonic Vitae's Decrease Damage Taken reaches 35% for 2 rounds (the +10% route; the kit's only answer to the bloodline's own 5% damage-taken passive) with its Increase Damage Given at 39%. Demon's Grasp is the fourth purchase (Embrace 37% / 37%); Boiling Ichor instead gives Vitae 42% Increase Damage Given with no Embrace gain. Fortified is never the best burst: Roar stays at 45 EP.
- **Primordial Rampage:** The sustained-damage build: Demonic Vitae's Increase Damage Given reaches 45% for the 3 rounds after each cast (3 of every 7) on all the caster's non-pierce damage (the +10% route), with Decrease Damage Taken at 29%. Demon's Grasp adds Embrace 37% / 37% so the empowered window has an exposed target; Scarred Hide (Vitae Decrease Damage Taken 32%) is the all-Vitae alternative (06,07,09,10).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Roar burst | Burn pressure | Fortified | Empowered |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Demonic Vitae | 0 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 39% (+4) | 45% (+10) |
| Demonic Vitae | 1 | Decrease Damage Taken | self | 25% | 27% (+2) | 27% (+2) | 35% (+10) | 29% (+4) |
| Demonic Embrace | 0 | Afterburn | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 37% (+2) |
| Demonic Embrace | 1 | Increase Damage Taken | enemy | 35% | 39% (+4) | 40% (+5) | 37% (+2) | 37% (+2) |
| Ancient Demon Roar | 0 | wound (unsupported) | enemy | 35% | 35% | 35% | 35% | 35% |
| Ancient Demon Roar | 1 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Howl of Annihilation: +5 Damage (0 + 2 + 3; on band)
  - Route Consuming Malice: +10% Afterburn (2 + 3 + 5; on band)
  - Route Unyielding Husk: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Primordial Rampage: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 5 (AB 1, DMG 1, DDT 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow (raw +19, row-weighted 19)
- Lowest row-weighted node: Rending Bellow (2)

Validator warnings:

- classification status: requires classification extension (director decision)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Demon's Grasp, Rending Bellow, Howl of Annihilation, Festering Brand | +5 Damage, +4% IDT, +5% AB |
| 2 | Demon's Grasp, Rending Bellow, Howl of Annihilation, Demon's Marrow | +5 Damage, +2% IDG, +4% IDT, +2% DDT, +2% AB |
| 3 | Demon's Grasp, Rending Bellow, Festering Brand, Consuming Malice | +2 Damage, +5% IDT, +10% AB |
| 4 | Demon's Grasp, Rending Bellow, Festering Brand, Demon's Marrow | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +5% AB |
| 5 | Demon's Grasp, Rending Bellow, Demon's Marrow, Scarred Hide | +2 Damage, +2% IDG, +2% IDT, +5% DDT, +2% AB |
| 6 | Demon's Grasp, Rending Bellow, Demon's Marrow, Boiling Ichor | +2 Damage, +5% IDG, +2% IDT, +2% DDT, +2% AB |
| 7 | Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow | +2% IDG, +5% IDT, +2% DDT, +10% AB |
| 8 | Demon's Grasp, Festering Brand, Demon's Marrow, Scarred Hide | +2% IDG, +2% IDT, +5% DDT, +5% AB |
| 9 | Demon's Grasp, Festering Brand, Demon's Marrow, Boiling Ichor | +5% IDG, +2% IDT, +2% DDT, +5% AB |
| 10 | Demon's Grasp, Demon's Marrow, Scarred Hide, Unyielding Husk | +4% IDG, +2% IDT, +10% DDT, +2% AB |
| 11 | Demon's Grasp, Demon's Marrow, Scarred Hide, Boiling Ichor | +5% IDG, +2% IDT, +5% DDT, +2% AB |
| 12 | Demon's Grasp, Demon's Marrow, Boiling Ichor, Primordial Rampage | +10% IDG, +2% IDT, +4% DDT, +2% AB |
| 13 | Demon's Marrow, Scarred Hide, Unyielding Husk, Boiling Ichor | +7% IDG, +10% DDT |
| 14 | Demon's Marrow, Scarred Hide, Boiling Ichor, Primordial Rampage | +10% IDG, +7% DDT |

## Design notes

- Node split: the two roots follow the two support casts. Demon's Grasp raises both Demonic Embrace rows and forks into Rending Bellow → Howl of Annihilation (Roar Damage) and Festering Brand → Consuming Malice (Afterburn). Demon's Marrow raises both Demonic Vitae rows and forks into Scarred Hide → Unyielding Husk (Decrease Damage Taken) and Boiling Ichor → Primordial Rampage (Increase Damage Given). 2/4/4; every Advanced Art is 3 BP deep; two cost 5 (shared root) or 6 BP. No node is in every legal 4-BP build.
- Routes: Roar burst +5 Damage (Rending Bellow +2, Howl of Annihilation +3) on one row; Burn pressure +10% Afterburn (Demon's Grasp +2%, Festering Brand +3%, Consuming Malice +5%); Fortified +10% Decrease Damage Taken and Empowered +10% Increase Damage Given (each Demon's Marrow +2%, Hidden Art +3%, Advanced Art +5%). The Vitae Advanced Arts carry a +2% secondary below the sibling Hidden Art's +3%, so hybrids like 01,06,07,09 stay non-dominated. Increase Damage Taken shares Embrace with Afterburn and applies to the same hits, so it has no route: Demon's Grasp +2% plus Howl +2% or Malice +3%, maximum +5%.
- Departures from the Taiyo Kami shape: each Foundation carries one support cast's row pair; Consuming Malice is +5% Afterburn / +3% Increase Damage Taken because Demon's Grasp already adds Afterburn and Embrace has no Increase Damage Given row; the Decrease Damage Given route becomes Increase Damage Given (the kit has no Decrease Damage Given row).
- Interaction with the kit: every row is element-less and lists all four stat types (Vitae Increase Damage Given also Highest), so each already matches every non-pierce hit (SOURCE_MECHANICS §3: stat filters on element-less rows are not binding); the nodes raise percentages, not reach. Each kit row multiplies the hits it matches and the bloodline Increase Damage Given passive (20% + 0.15/lvl) multiplies last (SOURCE_MECHANICS §3b). Its 5% Increase Damage Taken passive is a standing self-weakness the Vitae routes partly offset (Decrease Damage Taken +2% to +10%).
- Delivery and timing: all three jutsu have cooldown 7. Vitae (SELF, 40 AP) gives 3 rounds of Increase Damage Given but only 2 of Decrease Damage Taken; Embrace (one target, range 4, 40 AP) 2 rounds. Rows act only in the rounds after their cast round (§3b), so Vitae and Embrace (80 AP together) go a round before Roar to touch it. Roar (AOE_CIRCLE_SPAWN, range 4, 60 AP) is the only Damage: damage row friendly fire ENEMIES, unsupported Wound row friendly fire none (ally hazard, no node touches it).
- Fourth purchase: normally the other Foundation (the four examples) or a sibling Hidden Art (01,02,03,04 Afterburn 40%; 01,02,04,05 Roar 47 EP; 06,07,08,09 and 06,07,09,10 all-Vitae). All 14 legal full builds are non-dominated (arithmetic only).

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so 'Ancient Tailed Demon' is the placeholder name of a new jutsu classification (requires classification extension), not a bloodline-id selector; which jutsu carry it is a director/engine decision. All three kit jutsu qualify only through that authored jutsu classification (ENGINE_GAP_REGISTER G1); targeting None instead would reach every non-elemental row. Off-kit coverage is unverified.
- Afterburn at 45% on the Burn pressure route: in the 2 rounds after the cast it adds floor(hit × 45%) to every non-pierce hit the target takes from any source; Afterburn sources add, capped at 60% of each hit, so it saturates when another source (main tree, items, allies) is also on the target. Value scales with hits landed in the window, not with the one application row; not simulated.
- Row reach: Demonic Embrace's Increase Damage Taken debuff applies to every non-pierce hit the target takes from the caster and allies, normal jutsu, weapons and basics included; Demonic Vitae's Increase Damage Given self buff raises every non-pierce hit the caster alone lands. Both rows are element-less: potency widens the number, not the reach. Same-tag effects from allies, the main tree or recasts all apply and compound (process.ts 1109–1117; SOURCE_MECHANICS §3b).
- Pierce: Increase Damage Given, Increase Damage Taken and Decrease Damage Taken do not modify pierce hits and Afterburn skips them, so the tree is blind to pierce damage except through Roar's raw EP (Rending Bellow / Howl of Annihilation).
- Weakest route: the Roar burst example (01,02,03,06) is the likely weakest of the four (row weight 15 against 18–19): its +5 Damage lands on one 60 AP cast per 7 rounds while the other routes ride 2–3-round windows over every non-pierce hit. Any lift is a director value call and belongs on Howl's secondary (for example Increase Damage Taken +3%, maximum still +5%), not on Damage.
- Ally hazard: Ancient Demon Roar's Wound row (35%, friendly fire none) lands on allies inside the circle; the caster is never a target of an OTHER_USER area jutsu (§4b). No node touches it, but the Roar route invites more Roar casts. Embrace aimed at an ally (OTHER_USER permits it, §3b) would land both raised debuffs on that ally.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed: hit counts in the Embrace window, the AP economy, main-tree effects and the bloodline's 5% damage-taken passive were not modelled. Percentage caps are not approached (highest value 45%).

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Ancient Tailed Demon-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

