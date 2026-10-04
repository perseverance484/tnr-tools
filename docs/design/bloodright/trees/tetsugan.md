# Tetsugan — Discipline of Iron

**Bloodline:** Tetsugan (BR-083, rank H, `T-MyR4yQ1_aVbaJDLoI07`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Metal classification / forked tree · **Classification:** Metal (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense (Eye of Iron): sustained amplification that hones the stances' Increase Damage Given to 40%, or branding the enemy with Crimson Thrust's Afterburn and exposure · secondary Defense (Tempered Stance): a fortress on the three Decrease Damage Taken rows, or retaliation through Harmonious Slash's Reflect · tertiary None: Damage is left unamplified. The kit lists no traits and Phantom Slash (50 EP) is not a signature finisher, so no strike leaves its tier.

Eye of Iron answers "How do I win offensively: sharpen my own strikes or brand the enemy?": Honed Edge and One Cut Decides take the stances' Increase Damage Given 35 → 40% (×1.115 on three compounding rows), while Branding Iron takes Crimson Thrust's Afterburn 35 → 45% with exposure 39%. Tempered Stance answers "How do I win defensively: endure the blow or send it back?": Hammer and Anvil takes Decrease Damage Taken to 40/40/35% (×0.79), and Every Blow Returned takes Harmonious Slash's Reflect 40 → 50% as a bare payoff. Damage is unamplified: Phantom Slash shares the 60 AP and 7-round cooldown of five other Damage strikes. Potency reaches matching supported tags on all Metal jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Eye of Iron | Foundation | How do I win offensively: sharpen my own strikes or brand the enemy? |
| Tempered Stance | Foundation | How do I win defensively: endure the blow or send it back? |
| One Cut Decides | Advanced Art | sustained amplification: hone the stances so every cut inside them lands harder |
| Branding Iron | Advanced Art | attrition: brand the target so every hit burns |
| Hammer and Anvil | Advanced Art | fortress: endure the blow |
| Every Blow Returned | Advanced Art | retaliation: parry and send the blow back |

- Concern: One Cut Decides is the strongest offensive package (×1.166 with every row up; Tempered Stance or Sparks from the Forge as the fourth leaves it there), below Blood-Enchanted Eyes' Feast of the Fallen + Crimson Thirst + Opened Veins (×1.234). Branding Iron + Honed Edge is ×1.141 with Afterburn 45% but needs the dagger and the sword at once (ENGINE_GAP_REGISTER G7); with the dagger alone it is ×1.076.
- Concern: Damage is left unamplified: no traits, and Phantom Slash shares the 60 AP and 7-round cooldown of five other Damage strikes, so it is not a signature finisher. One Cut Decides is sustained amplification rather than a flat-Damage cut above the Nuke tier.
- Concern: Hammer and Anvil now stops at +5% on three rows (×0.85 on the two stances, ×0.79 with the staff guard), milder than Deathless Vitality's ×0.747; Folded Steel is a +1% commit because the three-row cap leaves no room.
- Concern: Every Blow Returned is a bare single-row payoff (Reflect 40 → 50% on sword-gated Harmonious Slash, the one-row +10% band). Tempered Stance's +2% still trims the return slightly (×1.18 instead of ×1.25 under both suppression rows), and Folded Steel as the fourth is a small return-for-survival trade (×1.12 returned, ×0.90 taken with a stance up under both suppression rows).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Metal jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempered Stance | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Inner Peace, Middle Guard Stance, Pivoting Fortress, Tranquil Guard Flowing Form, Vacuum Fan / 5 |
| 02 | Folded Steel | Hidden Art | Tempered Stance | +1% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 03 | Hammer and Anvil | Advanced Art | Folded Steel | +2% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 04 | Resonant Parry | Hidden Art | Tempered Stance | +3% Reflect (self buff) | Harmonious Slash / 1 |
| 05 | Every Blow Returned | Advanced Art | Resonant Parry | +7% Reflect (self buff) | Harmonious Slash / 1 |
| 06 | Eye of Iron | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 3 |
| 07 | Honed Edge | Hidden Art | Eye of Iron | +2% Increase Damage Given (self buff) | Inner Peace, Middle Guard Stance / 3 |
| 08 | One Cut Decides | Advanced Art | Honed Edge | +3% Increase Damage Given (self buff) | Inner Peace, Middle Guard Stance / 3 |
| 09 | Sparks from the Forge | Hidden Art | Eye of Iron | +3% Afterburn (enemy debuff) | Crimson Thrust / 1 |
| 10 | Branding Iron | Advanced Art | Sparks from the Forge | +7% Afterburn (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Crimson Thrust, Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempered Stance** — Breathe. Settle the feet. Let the iron in the blood go still. Decrease Damage Taken 35 → 37% on Middle Guard Stance and Inner Peace, 30 → 32% on Pivoting Fortress (self); Decrease Damage Given 30 → 32% on Tranquil Guard Flowing Form and 35 → 37% on Vacuum Fan (enemy; the fan's spiral also reaches allies).
- **Folded Steel** — Steel folded a thousand times does not break on the first blow. Decrease Damage Taken with Tempered Stance: Middle Guard Stance and Inner Peace 38%, Pivoting Fortress 33% (self, 2 rounds); a +1% commit, as the three-row +5% route leaves no room.
- **Hammer and Anvil** — Be the anvil. The hammer tires long before the iron does. Fortress: Decrease Damage Taken 35 → 40% on both stances and 30 → 35% on Pivoting Fortress on the full route (+5% on three compounding rows): a hit under both stances lands at ×0.36 instead of ×0.42 (×0.85), ×0.79 with the staff guard also up.
- **Resonant Parry** — A good parry rings. A perfect one sings back. Harmonious Slash Reflect 40 → 43% for the two rounds after each 60 AP sword strike (gated); returned damage caps at 60% of each hit.
- **Every Blow Returned** — What is aimed at the iron eye comes back along the same line. Retaliation: Harmonious Slash Reflect 40 → 50% on the full route for the two rounds after each sword strike (60% per-hit cap). The capstone adds nothing that shrinks the hit Reflect reads: a raw hit returns ×1.25, ×1.18 under both suppression rows.
- **Eye of Iron** — The iron eye sees where the guard is thin and names the opening aloud. Increase Damage Taken 35 → 37% on Phantom Slash (gated), Equilibrium Guard Strike (gated line; ally hazard) and Vacuum Fan (enemy debuffs, 2 rounds).
- **Honed Edge** — The stance is the whetstone: held with patience, it hones every edge drawn from it. Amplification commit: Increase Damage Given 35 → 37% on Middle Guard Stance and both Inner Peace rows (self, 2 rounds), ×1.045 on a hit inside both stance windows.
- **One Cut Decides** — Hold the settled stance, and every cut drawn from it is the one that decides. Sustained amplification: Increase Damage Given 35 → 40% on Middle Guard Stance and both Inner Peace rows on the full route (+5% on three compounding rows): ×1.115 on a hit inside both stance windows, ×1.037 with Middle Guard Stance alone (no sword). No strike changes tier.
- **Sparks from the Forge** — Where the steel bites the ground, the sparks keep burning. Crimson Thrust Afterburn 35 → 38% (dagger-gated ground circle, range 5, enemies only, 2 rounds); fed by every non-pierce hit the target takes.
- **Branding Iron** — The mark of hot iron, pressed into the enemy's guard. Attrition: Crimson Thrust Afterburn 35 → 45% on the full route (60% per-hit cap); the +2% rider takes exposure to 39% with Eye of Iron on Phantom Slash, Equilibrium Guard Strike and Vacuum Fan (×1.092 on three rows), so the hits the burn reads are larger too.

## Complete four-purchase examples

| Build | Purchases | IDG | DDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|
| One Cut Decides (Sustained amplification) | Eye of Iron, Honed Edge, One Cut Decides, Tempered Stance | +5% | +2% | +2% | +2% | — | — |
| Branding Iron (Attrition) | Eye of Iron, Sparks from the Forge, Branding Iron, Honed Edge | +2% | — | +4% | — | +10% | — |
| Hammer and Anvil (Fortress) | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | — | +2% | +2% | +5% | — | — |
| Every Blow Returned (Retaliation) | Tempered Stance, Resonant Parry, Every Blow Returned, Folded Steel | — | +2% | — | +3% | — | +10% |

Abbreviations: IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **One Cut Decides:** Honed Edge and One Cut Decides take Increase Damage Given 35 → 40% on Middle Guard Stance and both Inner Peace rows (×1.115 inside both stance windows), and Eye of Iron's exposure (37% on three rows, ×1.045) brings the package to ×1.166 with every row up; no strike changes tier. Tempered Stance is the fourth purchase because the same two stance casts carry Decrease Damage Taken (37%); Sparks from the Forge (Afterburn 38%) is the all-offence alternative but needs the dagger. Middle Guard Stance is free; Inner Peace's double row needs the sword-style item.
- **Branding Iron:** Crimson Thrust's Afterburn 35 → 45% and exposure 35 → 39% on Phantom Slash, Equilibrium Guard Strike and Vacuum Fan (×1.092 on three rows): a hit on a target under one exposure row and the burn goes from ×1.82 to ×2.02, and allied, weapon and normal-jutsu hits count too. Honed Edge (Increase Damage Given 37%) is the all-offence fourth purchase (×1.141 with every row up), but with the dagger in hand it reaches only Middle Guard Stance (×1.076); Tempered Stance is the defensive alternative. The burn is inert without the dagger-style item.
- **Hammer and Anvil:** Decrease Damage Taken 35 → 40% on both stances and 30 → 35% on Pivoting Fortress: a hit under both stances lands at ×0.36 instead of ×0.42 (×0.85), and at ×0.23 instead of ×0.30 with the staff guard also up (×0.79, against Deathless Vitality's ×0.747); suppression 32/37%. Eye of Iron is the fourth purchase (exposure 37%); Resonant Parry (Reflect 43%) is the all-defence alternative.
- **Every Blow Returned:** Harmonious Slash's Reflect 40 → 50% for the two rounds after each sword strike (60% per-hit cap); the capstone carries nothing else. Reflect returns a share of the hit after reductions, so only Tempered Stance's +2% trims it: of a raw enemy hit with no stance up the route returns 50% instead of 40% (×1.25), 31.5% instead of 26% under Vacuum Fan (×1.21) and 21.4% instead of 18.2% under both suppression rows (×1.18), while the caster takes ×0.94 of the base-kit hit. Folded Steel is the all-defence fourth purchase (stances 38%, Pivoting Fortress 33%): with a stance up under both suppression rows the returned share is ×1.12 instead of ×1.14 and the hit taken falls to ×0.90. Eye of Iron is the offensive alternative. Inert without the sword-style item.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustained amplification | Attrition | Fortress | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Tranquil Guard Flowing Form | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Tranquil Guard Flowing Form | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 32% (+2) | 32% (+2) |
| Tranquil Guard Flowing Form | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Enduring Resonance Ward | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Enduring Resonance Ward | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Pivoting Fortress | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Pivoting Fortress | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 35% (+5) | 33% (+3) |
| Phantom Slash | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Phantom Slash | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 39% (+4) | 37% (+2) | 35% |
| Phantom Slash | 2 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Crimson Thrust | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Crimson Thrust | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Crimson Thrust | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Shadow Pierce | 0 | pierce (unsupported) | enemy | 60 | 60 | 60 | 60 | 60 |
| Shadow Pierce | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Middle Guard Stance | 0 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 35% | 35% |
| Middle Guard Stance | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 40% (+5) | 38% (+3) |
| Middle Guard Stance | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Equilibrium Guard Strike | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Equilibrium Guard Strike | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 39% (+4) | 37% (+2) | 35% |
| Harmonious Slash | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Harmonious Slash | 1 | Reflect | self | 40% | 40% | 40% | 40% | 50% (+10) |
| Vacuum Fan | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 39% (+4) | 37% (+2) | 35% |
| Vacuum Fan | 1 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Vacuum Fan | 2 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 37% (+2) |
| Inner Peace | 0 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 35% | 35% |
| Inner Peace | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 40% (+5) | 38% (+3) |
| Inner Peace | 2 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 35% | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5% Increase Damage Given, +2% Decrease Damage Given, +4% Increase Damage Taken, +5% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Hammer and Anvil: +5% Decrease Damage Taken (2 + 1 + 2; on band)
  - Route Every Blow Returned: +10% Reflect (0 + 3 + 7; on band)
  - Route One Cut Decides: +5% Increase Damage Given (0 + 2 + 3; on band)
  - Route Branding Iron: +10% Afterburn (0 + 3 + 7; on band)
- Supported rows in kit: 20 (AB 1, DMG 7, DDG 2, DDT 3, IDG 3, IDT 3, REF 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Tempered Stance, Eye of Iron, Sparks from the Forge, Branding Iron (raw +18, row-weighted 32)
- Lowest row-weighted node: Folded Steel (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Equilibrium Guard Strike#1, Vacuum Fan#2
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Tranquil Guard Flowing Form 40 (Normal), Enduring Resonance Ward 40 (Normal), Pivoting Fortress 40 (Normal), Phantom Slash 50 (Nuke), Crimson Thrust 40 (Normal), Equilibrium Guard Strike 45 (High), Harmonious Slash 45 (High)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Hammer and Anvil | +2% DDG, +5% DDT | Resonant Parry | +2% DDG, +5% DDT, +3% REF | 22 |
| Hammer and Anvil | +2% DDG, +5% DDT | Eye of Iron *(highest diagnostic)* | +2% DDG, +2% IDT, +5% DDT | 25 |
| Every Blow Returned | +2% DDG, +2% DDT, +10% REF | Folded Steel | +2% DDG, +3% DDT, +10% REF | 23 |
| Every Blow Returned | +2% DDG, +2% DDT, +10% REF | Eye of Iron *(highest diagnostic)* | +2% DDG, +2% IDT, +2% DDT, +10% REF | 26 |
| One Cut Decides | +5% IDG, +2% IDT | Tempered Stance *(highest diagnostic)* | +5% IDG, +2% DDG, +2% IDT, +2% DDT | 31 |
| One Cut Decides | +5% IDG, +2% IDT | Sparks from the Forge | +5% IDG, +2% IDT, +3% AB | 24 |
| Branding Iron | +4% IDT, +10% AB | Tempered Stance *(highest diagnostic)* | +2% DDG, +4% IDT, +2% DDT, +10% AB | 32 |
| Branding Iron | +4% IDT, +10% AB | Honed Edge | +2% IDG, +4% IDT, +10% AB | 28 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempered Stance, Folded Steel, Hammer and Anvil, Resonant Parry | +2% DDG, +5% DDT, +3% REF |
| 2 | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | +2% DDG, +2% IDT, +5% DDT |
| 3 | Tempered Stance, Folded Steel, Resonant Parry, Every Blow Returned | +2% DDG, +3% DDT, +10% REF |
| 4 | Tempered Stance, Folded Steel, Resonant Parry, Eye of Iron | +2% DDG, +2% IDT, +3% DDT, +3% REF |
| 5 | Tempered Stance, Folded Steel, Eye of Iron, Honed Edge | +2% IDG, +2% DDG, +2% IDT, +3% DDT |
| 6 | Tempered Stance, Folded Steel, Eye of Iron, Sparks from the Forge | +2% DDG, +2% IDT, +3% DDT, +3% AB |
| 7 | Tempered Stance, Resonant Parry, Every Blow Returned, Eye of Iron | +2% DDG, +2% IDT, +2% DDT, +10% REF |
| 8 | Tempered Stance, Resonant Parry, Eye of Iron, Honed Edge | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% REF |
| 9 | Tempered Stance, Resonant Parry, Eye of Iron, Sparks from the Forge | +2% DDG, +2% IDT, +2% DDT, +3% AB, +3% REF |
| 10 | Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides | +5% IDG, +2% DDG, +2% IDT, +2% DDT |
| 11 | Tempered Stance, Eye of Iron, Honed Edge, Sparks from the Forge | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 12 | Tempered Stance, Eye of Iron, Sparks from the Forge, Branding Iron | +2% DDG, +4% IDT, +2% DDT, +10% AB |
| 13 | Eye of Iron, Honed Edge, One Cut Decides, Sparks from the Forge | +5% IDG, +2% IDT, +3% AB |
| 14 | Eye of Iron, Honed Edge, Sparks from the Forge, Branding Iron | +2% IDG, +4% IDT, +10% AB |

## Design notes

- Structure kept (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10); values re-cut in the 2026-10-04 batch and its roster passes. Eye of Iron carries only exposure and leads to sustained amplification and attrition; Tempered Stance carries Decrease Damage Taken and Decrease Damage Given and leads to fortress and retaliation. Middle Guard Stance and Inner Peace carry both halves: Honed Edge and One Cut Decides (under Eye of Iron) raise their Increase Damage Given, and Tempered Stance's routes harden their Decrease Damage Taken. Maxima over every legal allocation: Damage unamplified, Increase Damage Given +5%, Increase Damage Taken +4%, Afterburn +10%, Decrease Damage Taken +5%, Decrease Damage Given +2%, Reflect +10%.
- Damage is unamplified. The dossier lists no traits, and Phantom Slash (50 EP) is not a signature finisher: it costs the same 60 AP on the same 7-round cooldown as five other Damage strikes, and the dagger's Shadow Pierce carries the kit's largest hit (60 pierce). The kit is stance-and-guard led (two self stances; three strikes carry a self guard row), so a flat-Damage cut lifting Phantom Slash above the Nuke tier has no kit reason; One Cut Decides instead completes the stances' Increase Damage Given. The 40 and 45 strikes keep their tiers.
- Magnitudes (every row live: Increase rows ×(1+p) per row, Decrease rows ×(1−p) per row; Afterburn stated separately). Increase Damage Given has three compounding rows on two 40 AP self casts, so the route stops at +5% (Honed Edge +2%, One Cut Decides +3%): ×1.115 inside both stance windows. One Cut Decides' 3-BP package with Eye of Iron's exposure is ×1.166, below Blood-Enchanted Eyes' Feast of the Fallen + Crimson Thirst + Opened Veins (×1.234) and Rite of Exsanguination + Opened Veins + Iron in the Blood (≈ ×1.19 with the 50-row Damage). Branding Iron's exposure rider is +2% (route +4% on three rows, ×1.092, below Blood-Enchanted Eyes' ×1.115 exposure maximum). Decrease Damage Taken also has three compounding rows, so Hammer and Anvil stops at +5% (2/1/2): both stances ×0.85, all three ×0.79, milder than Deathless Vitality's ×0.747. Afterburn has one row; Branding Iron stops at +10%. Reflect has one row and sits at +10% (the one-row band); Every Blow Returned carries no rider, so the capstone never shrinks the hit Reflect reads (×1.25 on a raw hit, ×1.18 under both suppression rows, where only Tempered Stance's +2% trims it).
- Fourth purchases: One Cut Decides takes Tempered Stance (the same stance casts carry Decrease Damage Taken 37%; the natural sword build) or Sparks from the Forge (Afterburn 38%, dagger only); neither changes its ×1.166. Branding Iron takes Honed Edge (×1.141 with every row up, which needs the sword as well as the dagger; ×1.076 with the dagger alone, where it reaches only Middle Guard Stance) or Tempered Stance. Defence routes add the sibling Hidden Art or Eye of Iron; with a stance up under both suppression rows, Every Blow Returned + Folded Steel returns ×1.12 and takes ×0.90 of the base-kit hit, Hammer and Anvil + Resonant Parry returns ×0.93 and takes ×0.87. No fourth stacks a capstone's own primary.
- Filters: Middle Guard Stance row 0 and Inner Peace row 0 are Highest-filtered and element-less, so they match element-less hits and hits of the user's highest stat; Inner Peace row 2 lists Earth/Fire/Metal/None/Water. Equilibrium Guard Strike and Vacuum Fan exposure carry Metal plus four stats (any stat-typed hit). The bloodline passive Increase Damage Given multiplies last.
- Delivery and gates: seven 60 AP strikes (cooldown 7; Crimson Thrust 6, an EMPTY_GROUND circle re-applied each round to enemies in it); Middle Guard Stance and Inner Peace are 40 AP self casts, cooldown 7, two-round buffs; Vacuum Fan is a free 40 AP spiral. Three weapon-style items gate nine of eleven jutsu (staff: Tranquil Guard, Resonance Ward, Pivoting Fortress; dagger: Phantom Slash, Crimson Thrust, Shadow Pierce; sword: Equilibrium Guard Strike, Harmonious Slash, Inner Peace). Equipment gates castability only.

## Risks and unproven interactions

- Item gates: retaliation is inert without the sword-style item (Harmonious Slash) and the burn without the dagger-style item (Crimson Thrust); the amplification route keeps only Middle Guard Stance without the sword (×1.037 instead of ×1.115), and the fortress's third row needs the staff. Whether two hand weapons can be wielded at once was not read at the pin (ENGINE_GAP_REGISTER G7).
- Stacking: jutsu Increase Damage Given/Taken rows multiply; Decrease Damage Taken/Given apply in sequence with a 10% floor. At the route maxima three Increase Damage Given rows give ×2.74 (from ×2.46) and three Decrease Damage Taken rows ×0.23 (from ×0.30). The stance buffs apply to every hit passing their filters, not only bloodline strikes. Not simulated.
- Afterburn is downstream: one ground-circle application row; every non-pierce hit the burning target takes (allies and weapons included) adds the percentage of the exposed hit, capped at 60% of that hit. No uptime simulation.
- Reflect reads the hit after reductions, so Tempered Stance and Folded Steel shrink what is returned while they protect the caster: on the full route the returned share of a raw hit rises ×1.25 unsuppressed, ×1.21 under Vacuum Fan, ×1.18 under both suppression rows and ×1.14 with a stance up as well (×1.12 with Folded Steel). Pierce hits are reflected; cap 60% of each hit. Value depends on hits taken in each two-round window; not simulated.
- Ally hazard (validator warning accepted): Equilibrium Guard Strike's line carries its exposure (raised by Eye of Iron and Branding Iron) to allies in it; Vacuum Fan row 2 (spiral suppression) is raised by Tempered Stance. Allies in the area receive the raised values.
- Classification: no other captured bloodline has Metal jutsu; ordinary Metal jutsu are in scope by rule and unverified. Three of the thirteen targeted kit rows carry Metal (Inner Peace row 2, Equilibrium Guard Strike and Vacuum Fan exposure); the rest need the proposed jutsu-classification resolver, and Middle Guard Stance qualifies only through an authored Metal classification (ENGINE_GAP_REGISTER G1).
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

