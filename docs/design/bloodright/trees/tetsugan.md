# Tetsugan — Discipline of Iron

**Bloodline:** Tetsugan (BR-083, rank H, `T-MyR4yQ1_aVbaJDLoI07`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Metal classification / forked tree · **Classification:** Metal (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense (Eye of Iron): burst that hones the stances' Increase Damage Given and pays off with +2 Damage on the seven Metal strikes, or branding the enemy with Crimson Thrust's Afterburn and exposure · secondary Defense (Tempered Stance): a fortress on the three Decrease Damage Taken rows, or retaliation through Harmonious Slash's Reflect · tertiary Flat Damage only as One Cut Decides' controlled +2 payoff (40 → 42, 45 → 47, Phantom Slash 50 → 52).

Eye of Iron answers "How do I win offensively: sharpen my own strikes or brand the enemy?": Honed Edge sets up the stances' Increase Damage Given (35 → 38%) and One Cut Decides pays off with +2 Damage on every Metal strike, while Branding Iron takes Crimson Thrust's Afterburn 35 → 45% with exposure 39%. Tempered Stance answers "How do I win defensively: endure the blow or send it back?": Hammer and Anvil takes Decrease Damage Taken to 43/43/38%, and Every Blow Returned takes Harmonious Slash's Reflect 40 → 50% as a bare payoff. The +2 lifts Phantom Slash 50 → 52, the controlled payoff the director kept on Blood-Enchanted Eyes and Shakunetsu Sakura (RUL-2026-10-04-001/002). Potency reaches matching supported tags on all Metal jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Eye of Iron | Foundation | How do I win offensively: sharpen my own strikes or brand the enemy? |
| Tempered Stance | Foundation | How do I win defensively: endure the blow or send it back? |
| One Cut Decides | Advanced Art | burst: hone the stances, then a controlled +2 Damage cut |
| Branding Iron | Advanced Art | attrition: brand the target so every hit burns |
| Hammer and Anvil | Advanced Art | fortress: endure the blow |
| Every Blow Returned | Advanced Art | retaliation: parry and send the blow back |

**Director review recommended:** Confirm two consequences. (1) One Cut Decides' +2 lifts Phantom Slash 50 → 52 (above the Nuke tier), following Blood-Enchanted Eyes and Shakunetsu Sakura (RUL-2026-10-04-001/002); the first-pass +8% Increase Damage Given route is withdrawn. (2) Hammer and Anvil keeps +8% Decrease Damage Taken on three rows, above the roster's three-row +5% convention, because the third row needs a second weapon-style item: both stances ×0.77 against Deathless Vitality ×0.75, all three rows ×0.68.

- Concern: Branding Iron + Honed Edge is the strongest all-offence allocation with every row up (×1.25, against One Cut Decides + Sparks from the Forge ×1.19 and Blood-Enchanted Eyes' Feast of the Fallen + Opened Veins ×1.23 on the same model), but it needs the dagger and the sword at once (ENGINE_GAP_REGISTER G7) and six casts live together; with the dagger alone it is ×1.16.
- Concern: One Cut Decides' +2 reaches all seven Metal strikes, wider than the director patterns (Blood-Enchanted Eyes four rows, Shakunetsu Sakura and Arashima two); the weapon gates hold one item to two or three strikes, and Equilibrium Guard Strike's line carries 47 to allies in it.
- Concern: Hammer and Anvil's three-row case (×0.68) still exceeds Blood-Enchanted Eyes' two-row fortress; it needs both the sword and the staff, and simultaneous wield was not read at the pin (ENGINE_GAP_REGISTER G7).
- Concern: Every Blow Returned is a bare single-row payoff (Reflect 40 → 50% on sword-gated Harmonious Slash, the one-row +10% band); its earlier +3% Decrease Damage Given rider was dropped because it shrank the hit Reflect reads. Tempered Stance's +2% still trims the return slightly (×1.18 instead of ×1.25 under both suppression rows), and Folded Steel as the fourth is a deliberate return-for-survival trade (×1.09 returned, ×0.87 taken with a stance up under both suppression rows).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Metal jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempered Stance | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Inner Peace, Middle Guard Stance, Pivoting Fortress, Tranquil Guard Flowing Form, Vacuum Fan / 5 |
| 02 | Folded Steel | Hidden Art | Tempered Stance | +3% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 03 | Hammer and Anvil | Advanced Art | Folded Steel | +3% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 04 | Resonant Parry | Hidden Art | Tempered Stance | +3% Reflect (self buff) | Harmonious Slash / 1 |
| 05 | Every Blow Returned | Advanced Art | Resonant Parry | +7% Reflect (self buff) | Harmonious Slash / 1 |
| 06 | Eye of Iron | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 3 |
| 07 | Honed Edge | Hidden Art | Eye of Iron | +3% Increase Damage Given (self buff) | Inner Peace, Middle Guard Stance / 3 |
| 08 | One Cut Decides | Advanced Art | Honed Edge | +2 Damage (damage) | Crimson Thrust, Enduring Resonance Ward, Equilibrium Guard Strike, Harmonious Slash, Phantom Slash, Pivoting Fortress, Tranquil Guard Flowing Form / 7 |
| 09 | Sparks from the Forge | Hidden Art | Eye of Iron | +3% Afterburn (enemy debuff) | Crimson Thrust / 1 |
| 10 | Branding Iron | Advanced Art | Sparks from the Forge | +7% Afterburn (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Crimson Thrust, Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempered Stance** — Breathe. Settle the feet. Let the iron in the blood go still. Decrease Damage Taken 35 → 37% on Middle Guard Stance and Inner Peace, 30 → 32% on Pivoting Fortress (self); Decrease Damage Given 30 → 32% on Tranquil Guard Flowing Form and 35 → 37% on Vacuum Fan (enemy; the fan's spiral also reaches allies).
- **Folded Steel** — Steel folded a thousand times does not break on the first blow. Decrease Damage Taken with Tempered Stance: Middle Guard Stance and Inner Peace 40%, Pivoting Fortress 35% (self, 2 rounds).
- **Hammer and Anvil** — Be the anvil. The hammer tires long before the iron does. Fortress: Decrease Damage Taken 35 → 43% on both stances and 30 → 38% on Pivoting Fortress on the full route (+8%); a hit under both stances lands at ×0.32 instead of ×0.42.
- **Resonant Parry** — A good parry rings. A perfect one sings back. Harmonious Slash Reflect 40 → 43% for the two rounds after each 60 AP sword strike (gated); returned damage caps at 60% of each hit.
- **Every Blow Returned** — What is aimed at the iron eye comes back along the same line. Retaliation: Harmonious Slash Reflect 40 → 50% on the full route for the two rounds after each sword strike (60% per-hit cap). The capstone adds nothing that shrinks the hit Reflect reads: a raw hit returns ×1.25, ×1.18 under both suppression rows.
- **Eye of Iron** — The iron eye sees where the guard is thin and names the opening aloud. Increase Damage Taken 35 → 37% on Phantom Slash (gated), Equilibrium Guard Strike (gated line; ally hazard) and Vacuum Fan (enemy debuffs, 2 rounds).
- **Honed Edge** — The stance is the whetstone: held with patience, it hones every edge drawn from it. Burst setup: Increase Damage Given 35 → 38% on Middle Guard Stance and both Inner Peace rows (self, 2 rounds), ×1.07 on a hit inside both stance windows.
- **One Cut Decides** — From the settled stance the school teaches one cut. It has never needed a second. Burst payoff: +2 Damage on all seven Metal strikes: Tranquil Guard Flowing Form, Enduring Resonance Ward, Pivoting Fortress and Crimson Thrust 40 → 42, Equilibrium Guard Strike and Harmonious Slash 45 → 47, Phantom Slash 50 → 52 EP (above the 50 Nuke tier; director-review precedent). With Honed Edge a sword strike inside both stances gains ×1.12.
- **Sparks from the Forge** — Where the steel bites the ground, the sparks keep burning. Crimson Thrust Afterburn 35 → 38% (dagger-gated ground circle, range 5, enemies only, 2 rounds); fed by every non-pierce hit the target takes.
- **Branding Iron** — The mark of hot iron, pressed into the enemy's guard. Attrition: Crimson Thrust Afterburn 35 → 45% on the full route (60% per-hit cap); Increase Damage Taken 39% with Eye of Iron on Phantom Slash, Equilibrium Guard Strike and Vacuum Fan, so the hits the burn reads are larger too.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| One Cut Decides (Burst) | Eye of Iron, Honed Edge, One Cut Decides, Tempered Stance | +2 | +3% | +2% | +2% | +2% | — | — |
| Branding Iron (Attrition) | Eye of Iron, Sparks from the Forge, Branding Iron, Honed Edge | — | +3% | — | +4% | — | +10% | — |
| Hammer and Anvil (Fortress) | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | — | — | +2% | +2% | +8% | — | — |
| Every Blow Returned (Retaliation) | Tempered Stance, Resonant Parry, Every Blow Returned, Folded Steel | — | — | +2% | — | +5% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **One Cut Decides:** Honed Edge sets up Increase Damage Given 35 → 38% on Middle Guard Stance and both Inner Peace rows, and One Cut Decides adds +2 Damage to every Metal strike (40 → 42, 45 → 47, Phantom Slash 50 → 52). A sword strike (45 → 47) inside both stances on a target under Equilibrium Guard Strike's and Vacuum Fan's exposure (37%) gains ×1.15. Tempered Stance is the fourth purchase because the same two stance casts carry Decrease Damage Taken (37%); Sparks from the Forge (Afterburn 38%) is the all-offence alternative but needs the dagger. Middle Guard Stance is free; Inner Peace's double row needs the sword-style item.
- **Branding Iron:** Crimson Thrust's Afterburn 35 → 45% and exposure 35 → 39% on Phantom Slash, Equilibrium Guard Strike and Vacuum Fan: a hit on a target under one exposure row and the burn goes from ×1.82 to ×2.02, and allied, weapon and normal-jutsu hits count too. Honed Edge (Increase Damage Given 38%) is the all-offence fourth purchase, but with the dagger in hand it reaches only Middle Guard Stance (×1.16 in all); Tempered Stance is the defensive alternative. The burn is inert without the dagger-style item.
- **Hammer and Anvil:** Decrease Damage Taken 35 → 43% on both stances and 30 → 38% on Pivoting Fortress: a hit under both stances lands at ×0.32 instead of ×0.42, and at ×0.20 instead of ×0.30 with the staff guard also up; suppression 32/37%. Eye of Iron is the fourth purchase (exposure 37%); Resonant Parry (Reflect 43%) is the all-defence alternative.
- **Every Blow Returned:** Harmonious Slash's Reflect 40 → 50% for the two rounds after each sword strike (60% per-hit cap); the capstone carries nothing else. Reflect returns a share of the hit after reductions, so only Tempered Stance's +2% trims it: of a raw enemy hit with no stance up the route returns 50% instead of 40% (×1.25), 31.5% instead of 26% under Vacuum Fan (×1.21) and 21.4% instead of 18.2% under both suppression rows (×1.18), while the caster takes ×0.94 of the base-kit hit. Folded Steel is the all-defence fourth purchase (stances 40%, Pivoting Fortress 35%): with a stance up under both suppression rows the returned share is ×1.09 instead of ×1.14 and the hit taken falls to ×0.87. Eye of Iron is the offensive alternative. Inert without the sword-style item.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Attrition | Fortress | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Tranquil Guard Flowing Form | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Tranquil Guard Flowing Form | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 32% (+2) | 32% (+2) |
| Tranquil Guard Flowing Form | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Enduring Resonance Ward | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Enduring Resonance Ward | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Pivoting Fortress | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Pivoting Fortress | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 38% (+8) | 35% (+5) |
| Phantom Slash | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Phantom Slash | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 39% (+4) | 37% (+2) | 35% |
| Phantom Slash | 2 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Crimson Thrust | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Crimson Thrust | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Crimson Thrust | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Shadow Pierce | 0 | pierce (unsupported) | enemy | 60 | 60 | 60 | 60 | 60 |
| Shadow Pierce | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Middle Guard Stance | 0 | Increase Damage Given | self | 35% | 38% (+3) | 38% (+3) | 35% | 35% |
| Middle Guard Stance | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 43% (+8) | 40% (+5) |
| Middle Guard Stance | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Equilibrium Guard Strike | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Equilibrium Guard Strike | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 39% (+4) | 37% (+2) | 35% |
| Harmonious Slash | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Harmonious Slash | 1 | Reflect | self | 40% | 40% | 40% | 40% | 50% (+10) |
| Vacuum Fan | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 39% (+4) | 37% (+2) | 35% |
| Vacuum Fan | 1 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Vacuum Fan | 2 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 37% (+2) |
| Inner Peace | 0 | Increase Damage Given | self | 35% | 38% (+3) | 38% (+3) | 35% | 35% |
| Inner Peace | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 43% (+8) | 40% (+5) |
| Inner Peace | 2 | Increase Damage Given | self | 35% | 38% (+3) | 38% (+3) | 35% | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +3% Increase Damage Given, +2% Decrease Damage Given, +4% Increase Damage Taken, +8% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Hammer and Anvil: +8% Decrease Damage Taken (2 + 3 + 3; off band)
  - Route Every Blow Returned: +10% Reflect (0 + 3 + 7; on band)
  - Route One Cut Decides: +2 Damage (0 + 0 + 2; off band)
  - Route Branding Iron: +10% Afterburn (0 + 3 + 7; on band)
- Supported rows in kit: 20 (AB 1, DMG 7, DDG 2, DDT 3, IDG 3, IDT 3, REF 1)
- Strongest full build by row-weighted total: Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides (raw +11, row-weighted 39)
- Lowest row-weighted node: Resonant Parry (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Phantom Slash 50 -> 52
- ally-hazard area rows amplified (friendly fire none/ALL): Equilibrium Guard Strike#0, Equilibrium Guard Strike#1, Vacuum Fan#2

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Tranquil Guard Flowing Form | 0 | 40 (Normal) | 42 (Normal) |
| Enduring Resonance Ward | 0 | 40 (Normal) | 42 (Normal) |
| Pivoting Fortress | 0 | 40 (Normal) | 42 (Normal) |
| Phantom Slash | 0 | 50 (Nuke) | **52 (above Nuke)** |
| Crimson Thrust | 0 | 40 (Normal) | 42 (Normal) |
| Equilibrium Guard Strike | 0 | 45 (High) | 47 (High) |
| Harmonious Slash | 0 | 45 (High) | 47 (High) |

Above-Nuke rationale: One Cut Decides' controlled +2 Damage lifts Phantom Slash 50 → 52, past the 50 Nuke tier. It is the payoff of a deliberate burst route (Honed Edge's +3% Increase Damage Given setup on the stances), the pattern the director kept on Blood-Enchanted Eyes (RUL-2026-10-04-001, Reaper's Embrace 50 → 52) and Shakunetsu Sakura (RUL-2026-10-04-002, Sakura-ame 50 → 52). No row passes 52; the 45 strikes stop at 47 and the 40 strikes at 42. Flagged for director confirmation.

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Hammer and Anvil | +2% DDG, +8% DDT | Resonant Parry | +2% DDG, +8% DDT, +3% REF | 31 |
| Hammer and Anvil | +2% DDG, +8% DDT | Eye of Iron *(highest diagnostic)* | +2% DDG, +2% IDT, +8% DDT | 34 |
| Every Blow Returned | +2% DDG, +2% DDT, +10% REF | Folded Steel *(highest diagnostic)* | +2% DDG, +5% DDT, +10% REF | 29 |
| Every Blow Returned | +2% DDG, +2% DDT, +10% REF | Eye of Iron | +2% DDG, +2% IDT, +2% DDT, +10% REF | 26 |
| One Cut Decides | +2 Damage, +3% IDG, +2% IDT | Tempered Stance *(highest diagnostic)* | +2 Damage, +3% IDG, +2% DDG, +2% IDT, +2% DDT | 39 |
| One Cut Decides | +2 Damage, +3% IDG, +2% IDT | Sparks from the Forge | +2 Damage, +3% IDG, +2% IDT, +3% AB | 32 |
| Branding Iron | +4% IDT, +10% AB | Tempered Stance *(highest diagnostic)* | +2% DDG, +4% IDT, +2% DDT, +10% AB | 32 |
| Branding Iron | +4% IDT, +10% AB | Honed Edge | +3% IDG, +4% IDT, +10% AB | 31 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempered Stance, Folded Steel, Hammer and Anvil, Resonant Parry | +2% DDG, +8% DDT, +3% REF |
| 2 | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | +2% DDG, +2% IDT, +8% DDT |
| 3 | Tempered Stance, Folded Steel, Resonant Parry, Every Blow Returned | +2% DDG, +5% DDT, +10% REF |
| 4 | Tempered Stance, Folded Steel, Resonant Parry, Eye of Iron | +2% DDG, +2% IDT, +5% DDT, +3% REF |
| 5 | Tempered Stance, Folded Steel, Eye of Iron, Honed Edge | +3% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Tempered Stance, Folded Steel, Eye of Iron, Sparks from the Forge | +2% DDG, +2% IDT, +5% DDT, +3% AB |
| 7 | Tempered Stance, Resonant Parry, Every Blow Returned, Eye of Iron | +2% DDG, +2% IDT, +2% DDT, +10% REF |
| 8 | Tempered Stance, Resonant Parry, Eye of Iron, Honed Edge | +3% IDG, +2% DDG, +2% IDT, +2% DDT, +3% REF |
| 9 | Tempered Stance, Resonant Parry, Eye of Iron, Sparks from the Forge | +2% DDG, +2% IDT, +2% DDT, +3% AB, +3% REF |
| 10 | Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides | +2 Damage, +3% IDG, +2% DDG, +2% IDT, +2% DDT |
| 11 | Tempered Stance, Eye of Iron, Honed Edge, Sparks from the Forge | +3% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 12 | Tempered Stance, Eye of Iron, Sparks from the Forge, Branding Iron | +2% DDG, +4% IDT, +2% DDT, +10% AB |
| 13 | Eye of Iron, Honed Edge, One Cut Decides, Sparks from the Forge | +2 Damage, +3% IDG, +2% IDT, +3% AB |
| 14 | Eye of Iron, Honed Edge, Sparks from the Forge, Branding Iron | +3% IDG, +4% IDT, +10% AB |

## Design notes

- Structure kept (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10); values re-cut in the 2026-10-04 batch and its roster pass. Eye of Iron carries only exposure and leads to burst and attrition; Tempered Stance carries Decrease Damage Taken and Decrease Damage Given and leads to fortress and retaliation. Middle Guard Stance and Inner Peace carry both halves: Honed Edge (under Eye of Iron) sharpens their Increase Damage Given as the burst setup, and Tempered Stance's routes harden their Decrease Damage Taken. Maxima over every legal allocation: Damage +2, Increase Damage Given +3%, Increase Damage Taken +4%, Afterburn +10%, Decrease Damage Taken +8%, Decrease Damage Given +2%, Reflect +10%.
- Burst uses the director pattern: a percentage setup on the Hidden Art (Honed Edge, +3% Increase Damage Given on the stances, a self-buff setup like Arashima's Gathering Thunderhead) and a controlled +2 Damage payoff on the Advanced Art (as Blood-Enchanted Eyes' Rite of Exsanguination). The Damage tag reaches all seven Metal strikes (40/40/40/40/45/45/50): four 40 → 42 and two 45 → 47 stay in their tiers, and Phantom Slash 50 → 52 passes the Nuke tier as in Blood-Enchanted Eyes and Shakunetsu Sakura (above_nuke_rationale). The pre-batch +5 route (50 → 55, 45 → 50, 40 → 45) is not restored. Weapon gates split the strikes (staff 40/40/40, dagger 50/40, sword 45/45), so one item reaches two or three of them.
- Magnitudes (multipliers are every-row-live upper bounds: Increase rows multiply, Afterburn as 1 + p, flat Damage as final/base; Lifesteal not counted). Increase Damage Given has three compounding rows on two 40 AP casts, so it stays a +3% setup (×1.07 inside both stance windows); the first-pass +8% route (×1.19) is withdrawn. One Cut Decides' 3-BP package is ×1.15 on a sword strike inside both stances on a target under two exposure rows, ×1.17 with every row up, below Blood-Enchanted Eyes' Rite of Exsanguination (×1.20). Branding Iron's exposure rider is +2% (route +4% on three rows): ×1.14 with the dagger, ×1.17 with every row up, level with One Cut Decides. Decrease Damage Taken: both stances ×0.77, just short of Blood-Enchanted Eyes' Deathless Vitality (×0.75 over two rows); the third row (×0.68) needs the staff as well as the sword and a third 60 AP cast, so with one weapon-style item the +8% fortress compounds on two rows. Afterburn has one row; Branding Iron stops at +10%. Reflect has one row and sits at its +10% ceiling (the one-row band); Every Blow Returned carries no rider, so the capstone never shrinks the hit Reflect reads (×1.25 on a raw hit, ×1.18 under both suppression rows, where only Tempered Stance's +2% trims it).
- Fourth purchases: One Cut Decides takes Tempered Stance (the same stance casts carry Decrease Damage Taken; the natural sword build) or Sparks from the Forge (Afterburn 38%, dagger only; ×1.19 with every row up). Branding Iron takes Honed Edge (×1.16 with the dagger, where it reaches only Middle Guard Stance; ×1.25 with every row up, which needs the sword as well) or Tempered Stance. Defence routes add the sibling Hidden Art or Eye of Iron; with a stance up under both suppression rows, Every Blow Returned + Folded Steel returns ×1.09 and takes ×0.87 of the base-kit hit, Hammer and Anvil + Resonant Parry returns ×0.89 and takes ×0.83. No fourth stacks a capstone's own primary.
- Filters: Middle Guard Stance row 0 and Inner Peace row 0 are Highest-filtered and element-less, so they match element-less hits and hits of the user's highest stat; Inner Peace row 2 lists Earth/Fire/Metal/None/Water. Equilibrium Guard Strike and Vacuum Fan exposure carry Metal plus four stats (any stat-typed hit). The bloodline passive Increase Damage Given multiplies last.
- Delivery and gates: seven 60 AP strikes (cooldown 7; Crimson Thrust 6, an EMPTY_GROUND circle re-applied each round to enemies in it); Middle Guard Stance and Inner Peace are 40 AP self casts, cooldown 7, two-round buffs; Vacuum Fan is a free 40 AP spiral. Three weapon-style items gate nine of eleven jutsu (staff: Tranquil Guard, Resonance Ward, Pivoting Fortress; dagger: Phantom Slash, Crimson Thrust, Shadow Pierce; sword: Equilibrium Guard Strike, Harmonious Slash, Inner Peace). Equipment gates castability only.

## Risks and unproven interactions

- Item gates: retaliation is inert without the sword-style item (Harmonious Slash) and the burn without the dagger-style item (Crimson Thrust); the burst setup keeps only Middle Guard Stance without the sword, One Cut Decides reaches only the strikes of the weapon in hand, and the fortress's third row needs the staff. Whether two hand weapons can be wielded at once was not read at the pin (ENGINE_GAP_REGISTER G7).
- Stacking: jutsu Increase Damage Given/Taken rows multiply; Decrease Damage Taken/Given apply in sequence with a 10% floor. At the route maxima three Increase Damage Given rows give ×2.63 (from ×2.46) and three Decrease Damage Taken rows ×0.20 (from ×0.30). The stance buffs apply to every hit passing their filters, not only bloodline strikes, and they multiply One Cut Decides' raised strikes. Not simulated.
- Afterburn is downstream: one ground-circle application row; every non-pierce hit the burning target takes (allies and weapons included) adds the percentage of the exposed hit, capped at 60% of that hit. No uptime simulation.
- Reflect reads the hit after reductions, so Tempered Stance and Folded Steel shrink what is returned while they protect the caster: on the full route the returned share of a raw hit rises ×1.25 unsuppressed, ×1.21 under Vacuum Fan, ×1.18 under both suppression rows and ×1.14 with a stance up as well (×1.09 with Folded Steel). Pierce hits are reflected; cap 60% of each hit. Value depends on hits taken in each two-round window; not simulated.
- Ally hazard (validator warning accepted): Equilibrium Guard Strike's line carries its Damage (45 → 47 under One Cut Decides) and its exposure (raised by Eye of Iron and Branding Iron) to allies in it; Vacuum Fan row 2 (spiral suppression) is raised by Tempered Stance. Allies in the area receive the raised values.
- Classification: no other captured bloodline has Metal jutsu; ordinary Metal jutsu, including their Damage rows, are in scope by rule and unverified. Ten of the twenty targeted kit rows carry Metal (the seven strikes, Inner Peace row 2, Equilibrium Guard Strike and Vacuum Fan exposure); the rest need the proposed jutsu-classification resolver, and Middle Guard Stance qualifies only through an authored Metal classification (ENGINE_GAP_REGISTER G1).
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed. A combined potency budget with the main tree is not reviewed.

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

