# Tetsugan — Discipline of Iron

**Bloodline:** Tetsugan (BR-083, rank H, `T-MyR4yQ1_aVbaJDLoI07`) · **Revision:** Draft 4 / Metal classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Metal (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (seven Metal weapon strikes, +5 route) · secondary Decrease Damage Taken and Increase Damage Given (the Middle Guard Stance / Inner Peace / Pivoting Fortress stance buffs) · tertiary Increase Damage Taken and Afterburn exposure (Phantom Slash, Equilibrium Guard Strike, Vacuum Fan, Crimson Thrust); Reflect and Decrease Damage Given counter-play (Harmonious Slash, Tranquil Guard, Vacuum Fan).

Seven of the twenty supported rows are Metal damage (Phantom Slash 50 EP; Equilibrium Guard Strike and Harmonious Slash 45; Tranquil Guard Flowing Form, Enduring Resonance Ward, Pivoting Fortress and Crimson Thrust 40 at jutsu level 25, all 60 AP), split across the kit's staff, dagger and sword styles, so a weapon-school offense is the primary emphasis. The two 40 AP self stances carry three Increase Damage Given rows (Inner Peace twice) and, with Pivoting Fortress, three Decrease Damage Taken rows, which makes a stance-fortification route the natural second emphasis. Exposure (three Increase Damage Taken rows plus Crimson Thrust's single Afterburn row) and counter-play (Harmonious Slash's single Reflect row plus two Decrease Damage Given rows) are the tertiary routes. No heal, lifesteal or increase-heal row exists, so no sustain route is invented. Potency reaches matching supported tags on all Metal jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Metal jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempered Stance | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 6 |
| 02 | Folded Steel | Hidden Art | Tempered Stance | +3% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 03 | Hammer and Anvil | Advanced Art | Folded Steel | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 6 |
| 04 | Resonant Parry | Hidden Art | Tempered Stance | +3% Reflect (self buff) | Harmonious Slash / 1 |
| 05 | Every Blow Returned | Advanced Art | Resonant Parry | +7% Reflect (self buff); +3% Decrease Damage Given (enemy debuff) | Harmonious Slash, Tranquil Guard Flowing Form, Vacuum Fan / 3 |
| 06 | Eye of Iron | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Equilibrium Guard Strike, Phantom Slash, Tranquil Guard Flowing Form, Vacuum Fan / 5 |
| 07 | Honed Edge | Hidden Art | Eye of Iron | +2 Damage (damage) | Crimson Thrust, Enduring Resonance Ward, Equilibrium Guard Strike, Harmonious Slash, Phantom Slash, Pivoting Fortress, Tranquil Guard Flowing Form / 7 |
| 08 | One Cut Decides | Advanced Art | Honed Edge | +3 Damage (damage) | Crimson Thrust, Enduring Resonance Ward, Equilibrium Guard Strike, Harmonious Slash, Phantom Slash, Pivoting Fortress, Tranquil Guard Flowing Form / 7 |
| 09 | Sparks from the Forge | Hidden Art | Eye of Iron | +3% Afterburn (enemy debuff) | Crimson Thrust / 1 |
| 10 | Branding Iron | Advanced Art | Sparks from the Forge | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Crimson Thrust, Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempered Stance** — Breathe. Settle the feet. Let the iron in the blood go still. Middle Guard Stance and Inner Peace buffs 35 → 37% (Increase Damage Given 3 rows, Decrease Damage Taken 2 rows); Pivoting Fortress guard 30 → 32%. Inner Peace and Pivoting Fortress are item-gated.
- **Folded Steel** — Steel folded a thousand times does not break on the first blow. Decrease Damage Taken only: Middle Guard Stance and Inner Peace 40% with Tempered Stance, Pivoting Fortress 35%. 3 self rows.
- **Hammer and Anvil** — Take the blow on the anvil; answer it with the hammer. Fortified route total +10% Decrease Damage Taken (Middle Guard Stance and Inner Peace 35 → 45%, Pivoting Fortress 30 → 40%); Increase Damage Given +3% (Stance and both Inner Peace rows 40% with Tempered Stance).
- **Resonant Parry** — A good parry rings. A perfect one sings back. Harmonious Slash Reflect only (one self row, 40 → 43%, 2 rounds per 60 AP sword strike; gated). Returned damage caps at 60% of each hit.
- **Every Blow Returned** — What is aimed at the iron eye comes back along the same line. Counter route total +10%: Harmonious Slash Reflect 40 → 50%; Decrease Damage Given +3% on Tranquil Guard Flowing Form (gated) and Vacuum Fan (ally hazard).
- **Eye of Iron** — The iron eye sees where the guard is thin and names the opening aloud. Exposure 35 → 37%: Phantom Slash (gated), Equilibrium Strike (gated; ally hazard), Vacuum Fan. Suppression +2%: Tranquil Guard (gated), Fan.
- **Honed Edge** — An edge is only as sharp as the patience that honed it. All seven Metal Damage rows 40/45/50 → 42/47/52 EP: Tranquil Guard, Resonance Ward, Fortress, Phantom, Crimson, Equilibrium, Harmonious.
- **One Cut Decides** — The school teaches one cut. It has never needed a second. Same seven Metal rows; route total +5 Damage (Phantom Slash 50 → 55 EP, Equilibrium Strike and Harmonious Slash 45 → 50, the other four 40 → 45). All gated.
- **Sparks from the Forge** — Where the steel bites the ground, the sparks keep burning. Crimson Thrust Afterburn only (dagger-gated ground circle, range 5, cooldown 6, enemies only, 2 rounds): 35 → 38%; fed by every non-pierce hit.
- **Branding Iron** — The mark of hot iron, pressed into the enemy's guard. Burn route total +10%: Crimson Thrust (dagger-gated) Afterburn 35 → 45%, 60% hit cap; exposure 40% with Eye of Iron: Phantom (gated), Equilibrium (gated; ally hazard), Fan.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| One Cut Decides (Burst) | Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides | +5 | +2% | +2% | +2% | +2% | — | — |
| Hammer and Anvil (Fortified) | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | — | +5% | +2% | +2% | +10% | — | — |
| Branding Iron (Burn pressure) | Tempered Stance, Eye of Iron, Sparks from the Forge, Branding Iron | — | +2% | +2% | +5% | +2% | +10% | — |
| Every Blow Returned (Counter) | Tempered Stance, Resonant Parry, Every Blow Returned, Eye of Iron | — | +2% | +5% | +2% | +2% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **One Cut Decides:** +5 Damage on every one of the seven Metal weapon strikes (Phantom Slash 55 EP; Equilibrium Guard Strike and Harmonious Slash 50; Tranquil Guard, Resonance Ward, Pivoting Fortress and Crimson Thrust 45), multiplied downstream by the bloodline's own Increase Damage Given passive. Eye of Iron is the required root (exposure and suppression +2%); Tempered Stance is the fourth purchase for +2% on both stance buffs. Sparks from the Forge (Afterburn 38%) is the all-offence alternative fourth purchase. It gives up the fortified stances, the reflect and the burn.
- **Hammer and Anvil:** The stance route: Decrease Damage Taken reaches 45% on Middle Guard Stance and Inner Peace and 40% on Pivoting Fortress, while Increase Damage Given reaches 40% on Middle Guard Stance and on both Inner Peace rows, all from 40 AP self casts (Pivoting Fortress rides a 60 AP strike). Eye of Iron is the fourth purchase for +2% exposure and suppression; Resonant Parry (Reflect 43%) is the all-defence alternative. Damage is untouched, so it is not the burst build.
- **Branding Iron:** Crimson Thrust's Afterburn goes from 35% to 45% for its two rounds on any enemy standing in the circle, so every non-pierce hit those targets take (the seven Metal strikes, weapons, normal jutsu, allies) carries up to 45% extra within the 60% per-hit cap; the capstone's +3% exposure with Eye of Iron takes Phantom Slash, Equilibrium Guard Strike and Vacuum Fan to 40%. Tempered Stance is the fourth purchase; Honed Edge (Damage +2) is the all-offence alternative. Single application row, dagger-gated, Damage untouched.
- **Every Blow Returned:** Harmonious Slash's Reflect rises from 40% to 50% for two rounds after each 60 AP sword strike, ten points under the 60% per-hit cap, and the capstone's +3% suppression with Eye of Iron takes Tranquil Guard Flowing Form to 35% and Vacuum Fan to 40% Decrease Damage Given. Tempered Stance adds +2% to the stance buffs as the fourth purchase; Folded Steel (Decrease Damage Taken +5%) is the all-defence alternative. The whole route is inert without the sword-style item that gates Harmonious Slash.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Fortified | Burn pressure | Counter |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Tranquil Guard Flowing Form | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Tranquil Guard Flowing Form | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 35% (+5) |
| Tranquil Guard Flowing Form | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Enduring Resonance Ward | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Enduring Resonance Ward | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Pivoting Fortress | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Pivoting Fortress | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 40% (+10) | 32% (+2) | 32% (+2) |
| Phantom Slash | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Phantom Slash | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 37% (+2) |
| Phantom Slash | 2 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Crimson Thrust | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Crimson Thrust | 1 | Afterburn | enemy | 35% | 35% | 35% | 45% (+10) | 35% |
| Crimson Thrust | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Shadow Pierce | 0 | pierce (unsupported) | enemy | 60 | 60 | 60 | 60 | 60 |
| Shadow Pierce | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Middle Guard Stance | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Middle Guard Stance | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 37% (+2) |
| Middle Guard Stance | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Equilibrium Guard Strike | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Equilibrium Guard Strike | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 37% (+2) |
| Harmonious Slash | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Harmonious Slash | 1 | Reflect | self | 40% | 40% | 40% | 40% | 50% (+10) |
| Vacuum Fan | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 37% (+2) |
| Vacuum Fan | 1 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Vacuum Fan | 2 | Decrease Damage Given | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 40% (+5) |
| Inner Peace | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |
| Inner Peace | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 37% (+2) |
| Inner Peace | 2 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +5% Decrease Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Hammer and Anvil: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Every Blow Returned: +10% Reflect (0 + 3 + 7; on band)
  - Route One Cut Decides: +5 Damage (0 + 2 + 3; on band)
  - Route Branding Iron: +10% Afterburn (0 + 3 + 7; on band)
- Supported rows in kit: 20 (AB 1, DMG 7, DDG 2, DDT 3, IDG 3, IDT 3, REF 1)
- Strongest full build by row-weighted total: Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides (raw +13, row-weighted 57)
- Lowest row-weighted node: Resonant Parry (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Equilibrium Guard Strike#0, Equilibrium Guard Strike#1, Vacuum Fan#2

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempered Stance, Folded Steel, Hammer and Anvil, Resonant Parry | +5% IDG, +10% DDT, +3% REF |
| 2 | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | +5% IDG, +2% DDG, +2% IDT, +10% DDT |
| 3 | Tempered Stance, Folded Steel, Resonant Parry, Every Blow Returned | +2% IDG, +3% DDG, +5% DDT, +10% REF |
| 4 | Tempered Stance, Folded Steel, Resonant Parry, Eye of Iron | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +3% REF |
| 5 | Tempered Stance, Folded Steel, Eye of Iron, Honed Edge | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Tempered Stance, Folded Steel, Eye of Iron, Sparks from the Forge | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +3% AB |
| 7 | Tempered Stance, Resonant Parry, Every Blow Returned, Eye of Iron | +2% IDG, +5% DDG, +2% IDT, +2% DDT, +10% REF |
| 8 | Tempered Stance, Resonant Parry, Eye of Iron, Honed Edge | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% REF |
| 9 | Tempered Stance, Resonant Parry, Eye of Iron, Sparks from the Forge | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB, +3% REF |
| 10 | Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT |
| 11 | Tempered Stance, Eye of Iron, Honed Edge, Sparks from the Forge | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 12 | Tempered Stance, Eye of Iron, Sparks from the Forge, Branding Iron | +2% IDG, +2% DDG, +5% IDT, +2% DDT, +10% AB |
| 13 | Eye of Iron, Honed Edge, One Cut Decides, Sparks from the Forge | +5 Damage, +2% DDG, +2% IDT, +3% AB |
| 14 | Eye of Iron, Honed Edge, Sparks from the Forge, Branding Iron | +2 Damage, +2% DDG, +5% IDT, +10% AB |

## Design notes

- Node split: Tempered Stance (self IDG/DDT) forks into Guard (DDT) and Counter (Reflect); Eye of Iron (enemy IDT/DDG) into Blade (Damage) and Burn (Afterburn); 14 full builds, none dominated. Blade 2/3, Burn 3/7 + IDT 3 and Guard 2/3/5 reuse Taiyo Kami's Crown of Cinders/Solar Cataclysm, Emberwake/Eternal Noon and Sunward Oath/Golden Mantle/Sovereign Sun flats. Departures: Branding Iron drops Eternal Noon's IDG +3% (a second path to the IDG maximum), and the Reflect route is new (3/7, mirroring Branding Iron).
- Routes: Burst +5 Damage (Honed Edge +2, One Cut Decides +3; seven rows, all item-gated); Fortified +10% Decrease Damage Taken (Tempered Stance +2%, Folded Steel +3%, Hammer and Anvil +5%; three self rows); Burn +10% Afterburn (Sparks from the Forge +3%, Branding Iron +7%; 35 → 45%); Counter +10% Reflect (Resonant Parry +3%, Every Blow Returned +7%; 40 → 50%). Glue tags IDG, IDT and DDG stop at +5% (Foundation +2%, capstone +3%) on no Hidden Art, so no capstone outbids a sibling. Recalibration: Fortified rises from +6% (2/2/2) and Counter from +8% to the +10% band; stacking on three DDT rows is in risks.
- Filters (getEfficiencyRatio returns 1 on any shared stat/general/element tag): Middle Guard Stance row 0 and Inner Peace row 0 are Highest-filtered and element-less, so they apply to element-less hits and to hits of the user's highest stat; Inner Peace row 2 lists Earth/Fire/Metal/None/Water. The DDT rows, Phantom Slash exposure and both suppression rows are element-less with stat filters. Equilibrium Strike and Vacuum Fan exposure carry Metal plus four stats: any stat-typed hit.
- Passives and delivery: the passive IDG (25 + 0.15/level on Earth/Fire/Metal/None/Water) multiplies the enhanced damage rows downstream; nothing touches Shadow Pierce's pierce row. The seven damage casts are 60 AP, cooldown 7 (Crimson Thrust 6: an EMPTY_GROUND circle at range 5, re-applied each round to enemies standing in it). Middle Guard Stance and Inner Peace are 40 AP self casts, cooldown 7, two-round buffs. Vacuum Fan: 40 AP spiral, range 5. No rotation simulated.
- Fourth purchase choices: Burst takes Tempered Stance (stance buffs +2%) or Sparks from the Forge (Afterburn +3%); Fortified takes Eye of Iron or Resonant Parry (Reflect +3%); Burn takes Tempered Stance or Honed Edge (all-offence 06/07/09/10: Damage +2, Afterburn +10%, exposure +5%); Counter takes Eye of Iron or Folded Steel (all-defence 01/02/04/05: DDT +5%, Reflect +10%, suppression +3%). No-capstone hybrids spread small flats across five or six tags. Four examples: each capstone anchors a role.
- Gates: three bloodline items gate nine of eleven jutsu and align with the records' jutsuWeapon values (staff: Tranquil Guard, Resonance Ward, Pivoting Fortress; dagger: Phantom Slash, Crimson Thrust, Shadow Pierce; sword: Equilibrium Guard Strike, Harmonious Slash, Inner Peace). Every damage row, the Afterburn row, the Reflect row and two of three IDG/DDT rows sit behind a gate; only Middle Guard Stance and Vacuum Fan are free. Equipment gates castability only; no node is limited by an item.

## Risks and unproven interactions

- Item gates: the Counter route is inert without the sword-style item (Harmonious Slash holds the only Reflect row); the Burn route's Afterburn is inert without the dagger-style item (Crimson Thrust); the Blade route needs all three items for full coverage. Whether equipping the matching weapon type is also required was not read at the pin; this projection evaluates effect rows only.
- Ally hazard (validator warning accepted): Equilibrium Guard Strike rows 0–1 (damage, exposure; line, friendly fire none) and Vacuum Fan row 2 (suppression; spiral, friendly fire none). Honed Edge and One Cut Decides raise the line's damage to allies in it; Eye of Iron and Branding Iron raise their exposure; Eye of Iron and Every Blow Returned raise suppression on allies in the spiral.
- Stance stacking (process.ts 468–476, 1692–1770; constants.ts 3096): in the damage pipeline jutsu IDG rows multiply and percentage DDT rows apply as sequential reductions, floored at 10% of post-system-DR damage (DMG_REDUCTION_CAP 0.9). Both stances at base leave x0.4225 of a hit and three IDG rows give x2.46; at the Fortified maximum (DDT 45%, IDG 40%) x0.3025 and x2.74, and Pivoting Fortress at 40% can add a third reduction. The IDG rise applies to every damage source, not only bloodline strikes. Not simulated.
- Seven-row damage: +5 Damage is the reference per-cast gain (Hidden +2 / Advanced +3), but Tetsugan lands a bloodline strike every round (seven 60 AP casts, cooldown 6–7) where Taiyo Kami lands three per seven, so realised per-battle uplift is about 2.3x the reference. Not simulated.
- Afterburn is downstream: one ground-circle application row (Crimson Thrust, 2 rounds, enemies only, re-applied to any enemy standing in the circle); its value comes from every non-pierce hit the burning target takes, allies and weapons included, capped at 60% of each hit; other Afterburn sources saturate at that cap. Shadow Pierce's pierce row does not feed it. No proc or uptime simulation.
- Downstream reach: the stance buffs raise or blunt normal jutsu, weapon and basic hits passing their stat filters in the two-round window (Inner Peace row 2 only for Earth/Fire/Metal/Water or element-less hits); enemy-side exposure and suppression alter allied and weapon damage too, and the Metal-plus-four-stat exposure rows match any stat-typed hit. Casting scope does not limit downstream benefit.
- Classification: no other captured bloodline has Metal jutsu; ordinary Metal jutsu are in scope by rule and unverified. 10 of 20 supported kit rows carry Metal (seven damage rows, Inner Peace row 2, the two Metal-tagged exposure rows); the other 10 need the proposed jutsu-classification resolver, and Middle Guard Stance (no Metal row) qualifies in-kit only through an authored Metal jutsu classification (ENGINE_GAP_REGISTER G1).
- Ranked PvP and ranked sparring suppress skill-tree effects at the pin, so the tree is inert there. Reflect value depends on hits taken (pierce included) inside each two-round window and was not simulated. Normal-tree potency policy is not approved; a combined potency budget with the main tree still needs review before any implementation.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Metal jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

