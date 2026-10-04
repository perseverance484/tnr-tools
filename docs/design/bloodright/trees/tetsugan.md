# Tetsugan — Discipline of Iron

**Bloodline:** Tetsugan (BR-083, rank H, `T-MyR4yQ1_aVbaJDLoI07`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Metal classification / forked tree · **Classification:** Metal (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense (Eye of Iron): self-amplification through the Increase Damage Given rows of Middle Guard Stance and Inner Peace, or branding the enemy with Crimson Thrust's Afterburn and exposure · secondary Defense (Tempered Stance): a fortress on the three Decrease Damage Taken rows, or retaliation through Harmonious Slash's Reflect with suppression · tertiary No flat Damage: the seven Metal strikes keep their 40/45/50 tiers.

Eye of Iron answers "How do I win offensively: sharpen my own strikes or brand the enemy?": One Cut Decides takes the stances' Increase Damage Given 35 → 43%, and Branding Iron takes Crimson Thrust's Afterburn 35 → 45% with exposure 40%. Tempered Stance answers "How do I win defensively: endure the blow or send it back?": Hammer and Anvil takes Decrease Damage Taken to 43/43/38%, and Every Blow Returned takes Harmonious Slash's Reflect 40 → 50% with suppression. No node targets Damage: it reaches all seven strikes, and any flat point lifts Phantom Slash past the 50 Nuke tier. Potency reaches matching supported tags on all Metal jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Eye of Iron | Foundation | How do I win offensively: sharpen my own strikes or brand the enemy? |
| Tempered Stance | Foundation | How do I win defensively: endure the blow or send it back? |
| One Cut Decides | Advanced Art | self-amplification: sharpen my own strikes |
| Branding Iron | Advanced Art | attrition: brand the target so every hit burns |
| Hammer and Anvil | Advanced Art | fortress: endure the blow |
| Every Blow Returned | Advanced Art | retaliation: parry and send the blow back |

**Director review recommended:** Two stance-kit magnitudes need the director, because three compounding rows make them the largest gains among the protected references. (1) One Cut Decides: +8% Increase Damage Given gives ×1.19 with both stances (×1.12 in Inner Peace alone), above Blood-Enchanted Eyes' Feast of the Fallen ×1.11, Shakunetsu Sakura ×1.07/×1.10 and Arashima ×1.06/×1.07; +5% (Honed Edge +2%, One Cut Decides +3%) would give ×1.12. (2) Hammer and Anvil, cut to +8% Decrease Damage Taken: both stances ×0.77 against Blood-Enchanted Eyes' Deathless Vitality ×0.75, but all three rows (sword, staff and a third cast) reach ×0.68.

- Concern: One Cut Decides applies no coverage discount: +8% is Arashima's single-row value on three compounding rows (×1.19 against ×1.06–×1.11 for the protected self-amplification routes), offset only by the stances' two-round windows on cooldown 7 and Inner Peace's sword gate. Cutting it would also leave it behind Branding Iron; with the all-offence fourth purchases and every row up the two are level today (×1.27 against ×1.28).
- Concern: Hammer and Anvil's three-row case (×0.68) still exceeds Blood-Enchanted Eyes' two-row fortress; it needs both the sword and the staff, and simultaneous wield was not read at the pin (ENGINE_GAP_REGISTER G7).
- Concern: Every Blow Returned's suppression trims its own Reflect (×1.07 under both suppression rows, ×0.99 with Folded Steel and a stance up): the retaliation route leans defensive rather than returning much more damage.
- Concern: The seven Metal strikes are unamplified: no node targets Damage, because every flat point lifts Phantom Slash past the 50 Nuke tier.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Metal jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempered Stance | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Inner Peace, Middle Guard Stance, Pivoting Fortress, Tranquil Guard Flowing Form, Vacuum Fan / 5 |
| 02 | Folded Steel | Hidden Art | Tempered Stance | +3% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 03 | Hammer and Anvil | Advanced Art | Folded Steel | +3% Decrease Damage Taken (self buff) | Inner Peace, Middle Guard Stance, Pivoting Fortress / 3 |
| 04 | Resonant Parry | Hidden Art | Tempered Stance | +3% Reflect (self buff) | Harmonious Slash / 1 |
| 05 | Every Blow Returned | Advanced Art | Resonant Parry | +7% Reflect (self buff); +3% Decrease Damage Given (enemy debuff) | Harmonious Slash, Tranquil Guard Flowing Form, Vacuum Fan / 3 |
| 06 | Eye of Iron | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 3 |
| 07 | Honed Edge | Hidden Art | Eye of Iron | +3% Increase Damage Given (self buff) | Inner Peace, Middle Guard Stance / 3 |
| 08 | One Cut Decides | Advanced Art | Honed Edge | +5% Increase Damage Given (self buff) | Inner Peace, Middle Guard Stance / 3 |
| 09 | Sparks from the Forge | Hidden Art | Eye of Iron | +3% Afterburn (enemy debuff) | Crimson Thrust / 1 |
| 10 | Branding Iron | Advanced Art | Sparks from the Forge | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Crimson Thrust, Equilibrium Guard Strike, Phantom Slash, Vacuum Fan / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempered Stance** — Breathe. Settle the feet. Let the iron in the blood go still. Decrease Damage Taken 35 → 37% on Middle Guard Stance and Inner Peace, 30 → 32% on Pivoting Fortress (self); Decrease Damage Given 30 → 32% on Tranquil Guard Flowing Form and 35 → 37% on Vacuum Fan (enemy; the fan's spiral also reaches allies).
- **Folded Steel** — Steel folded a thousand times does not break on the first blow. Decrease Damage Taken with Tempered Stance: Middle Guard Stance and Inner Peace 40%, Pivoting Fortress 35% (self, 2 rounds).
- **Hammer and Anvil** — Be the anvil. The hammer tires long before the iron does. Fortress: Decrease Damage Taken 35 → 43% on both stances and 30 → 38% on Pivoting Fortress on the full route (+8%); a hit under both stances lands at ×0.32 instead of ×0.42.
- **Resonant Parry** — A good parry rings. A perfect one sings back. Harmonious Slash Reflect 40 → 43% for the two rounds after each 60 AP sword strike (gated); returned damage caps at 60% of each hit.
- **Every Blow Returned** — What is aimed at the iron eye comes back along the same line. Retaliation: Harmonious Slash Reflect 40 → 50% on the full route; Decrease Damage Given 35% on Tranquil Guard Flowing Form and 40% on Vacuum Fan with Tempered Stance (+5%). Reflect reads the reduced hit, so under both suppression rows the returned share rises only ×1.07.
- **Eye of Iron** — The iron eye sees where the guard is thin and names the opening aloud. Increase Damage Taken 35 → 37% on Phantom Slash (gated), Equilibrium Guard Strike (gated line; ally hazard) and Vacuum Fan (enemy debuffs, 2 rounds).
- **Honed Edge** — The stance is the whetstone: held with patience, it hones every edge drawn from it. Increase Damage Given 35 → 38% on Middle Guard Stance and on both Inner Peace rows (self, 2 rounds).
- **One Cut Decides** — Settle into the stance and the iron eye finds the opening: for two breaths, every cut is the deciding one. Self-amplification: Increase Damage Given 35 → 43% on Middle Guard Stance and both Inner Peace rows on the full route (+8%); Inner Peace's two rows take a hit from ×1.82 to ×2.04, ×2.92 with Middle Guard Stance also up.
- **Sparks from the Forge** — Where the steel bites the ground, the sparks keep burning. Crimson Thrust Afterburn 35 → 38% (dagger-gated ground circle, range 5, enemies only, 2 rounds); fed by every non-pierce hit the target takes.
- **Branding Iron** — The mark of hot iron, pressed into the enemy's guard. Attrition: Crimson Thrust Afterburn 35 → 45% on the full route (60% per-hit cap); Increase Damage Taken 40% with Eye of Iron on Phantom Slash, Equilibrium Guard Strike and Vacuum Fan, so the hits the burn reads are larger too.

## Complete four-purchase examples

| Build | Purchases | IDG | DDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|
| One Cut Decides (Self-amplification) | Eye of Iron, Honed Edge, One Cut Decides, Tempered Stance | +8% | +2% | +2% | +2% | — | — |
| Branding Iron (Attrition) | Eye of Iron, Sparks from the Forge, Branding Iron, Honed Edge | +3% | — | +5% | — | +10% | — |
| Hammer and Anvil (Fortress) | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | — | +2% | +2% | +8% | — | — |
| Every Blow Returned (Retaliation) | Tempered Stance, Resonant Parry, Every Blow Returned, Folded Steel | — | +5% | — | +5% | — | +10% |

Abbreviations: IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **One Cut Decides:** Increase Damage Given 35 → 43% on Middle Guard Stance and both Inner Peace rows: a hit inside Inner Peace's window goes from ×1.82 to ×2.04, ×2.92 with Middle Guard Stance also up; Eye of Iron adds exposure 37%. Tempered Stance is the fourth purchase because the same two stance casts carry Decrease Damage Taken (37%); Sparks from the Forge (Afterburn 38%) is the all-offence alternative. Middle Guard Stance is free; Inner Peace's double row needs the sword-style item.
- **Branding Iron:** Crimson Thrust's Afterburn 35 → 45% and exposure 35 → 40% on Phantom Slash, Equilibrium Guard Strike and Vacuum Fan: a hit on a target under one exposure row and the burn goes from ×1.82 to ×2.03, and allied, weapon and normal-jutsu hits count too. Honed Edge (Increase Damage Given 38%) is the all-offence fourth purchase; Tempered Stance is the defensive alternative. The burn is inert without the dagger-style item.
- **Hammer and Anvil:** Decrease Damage Taken 35 → 43% on both stances and 30 → 38% on Pivoting Fortress: a hit under both stances lands at ×0.32 instead of ×0.42, and at ×0.20 instead of ×0.30 with the staff guard also up; suppression 32/37%. Eye of Iron is the fourth purchase (exposure 37%); Resonant Parry (Reflect 43%) is the all-defence alternative.
- **Every Blow Returned:** Harmonious Slash's Reflect 40 → 50% for the two rounds after each sword strike (60% per-hit cap), with Decrease Damage Given 35% on Tranquil Guard Flowing Form and 40% on Vacuum Fan. Reflect returns a share of the hit after reductions, so the suppression trims it: of a raw enemy hit with no stance up the route returns 50% instead of 40% (×1.25), 30% instead of 26% under Vacuum Fan (×1.15) and 19.5% instead of 18.2% under both suppression rows (×1.07), while the caster takes ×0.86 of the base-kit hit. Folded Steel is the all-defence fourth purchase (stances 40%, Pivoting Fortress 35%): with a stance up under both suppression rows the returned share is flat (×0.99) and the hit taken falls to ×0.79. Eye of Iron is the offensive alternative. Inert without the sword-style item.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Self-amplification | Attrition | Fortress | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Tranquil Guard Flowing Form | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Tranquil Guard Flowing Form | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 32% (+2) | 35% (+5) |
| Tranquil Guard Flowing Form | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Enduring Resonance Ward | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Enduring Resonance Ward | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Pivoting Fortress | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Pivoting Fortress | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 38% (+8) | 35% (+5) |
| Phantom Slash | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Phantom Slash | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Phantom Slash | 2 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Crimson Thrust | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Crimson Thrust | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Crimson Thrust | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Shadow Pierce | 0 | pierce (unsupported) | enemy | 60 | 60 | 60 | 60 | 60 |
| Shadow Pierce | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Middle Guard Stance | 0 | Increase Damage Given | self | 35% | 43% (+8) | 38% (+3) | 35% | 35% |
| Middle Guard Stance | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 43% (+8) | 40% (+5) |
| Middle Guard Stance | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Equilibrium Guard Strike | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Equilibrium Guard Strike | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Harmonious Slash | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Harmonious Slash | 1 | Reflect | self | 40% | 40% | 40% | 40% | 50% (+10) |
| Vacuum Fan | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Vacuum Fan | 1 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Vacuum Fan | 2 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 40% (+5) |
| Inner Peace | 0 | Increase Damage Given | self | 35% | 43% (+8) | 38% (+3) | 35% | 35% |
| Inner Peace | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 43% (+8) | 40% (+5) |
| Inner Peace | 2 | Increase Damage Given | self | 35% | 43% (+8) | 38% (+3) | 35% | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +5% Decrease Damage Given, +5% Increase Damage Taken, +8% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Hammer and Anvil: +8% Decrease Damage Taken (2 + 3 + 3; off band)
  - Route Every Blow Returned: +10% Reflect (0 + 3 + 7; on band)
  - Route One Cut Decides: +8% Increase Damage Given (0 + 3 + 5; off band)
  - Route Branding Iron: +10% Afterburn (0 + 3 + 7; on band)
- Supported rows in kit: 20 (AB 1, DMG 7, DDG 2, DDT 3, IDG 3, IDT 3, REF 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides (raw +14, row-weighted 40)
- Lowest row-weighted node: Resonant Parry (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Equilibrium Guard Strike#1, Vacuum Fan#2
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Tranquil Guard Flowing Form 40 (Normal), Enduring Resonance Ward 40 (Normal), Pivoting Fortress 40 (Normal), Phantom Slash 50 (Nuke), Crimson Thrust 40 (Normal), Equilibrium Guard Strike 45 (High), Harmonious Slash 45 (High)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Hammer and Anvil | +2% DDG, +8% DDT | Resonant Parry | +2% DDG, +8% DDT, +3% REF | 31 |
| Hammer and Anvil | +2% DDG, +8% DDT | Eye of Iron *(highest diagnostic)* | +2% DDG, +2% IDT, +8% DDT | 34 |
| Every Blow Returned | +5% DDG, +2% DDT, +10% REF | Folded Steel *(highest diagnostic)* | +5% DDG, +5% DDT, +10% REF | 35 |
| Every Blow Returned | +5% DDG, +2% DDT, +10% REF | Eye of Iron | +5% DDG, +2% IDT, +2% DDT, +10% REF | 32 |
| One Cut Decides | +8% IDG, +2% IDT | Tempered Stance *(highest diagnostic)* | +8% IDG, +2% DDG, +2% IDT, +2% DDT | 40 |
| One Cut Decides | +8% IDG, +2% IDT | Sparks from the Forge | +8% IDG, +2% IDT, +3% AB | 33 |
| Branding Iron | +5% IDT, +10% AB | Tempered Stance *(highest diagnostic)* | +2% DDG, +5% IDT, +2% DDT, +10% AB | 35 |
| Branding Iron | +5% IDT, +10% AB | Honed Edge | +3% IDG, +5% IDT, +10% AB | 34 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempered Stance, Folded Steel, Hammer and Anvil, Resonant Parry | +2% DDG, +8% DDT, +3% REF |
| 2 | Tempered Stance, Folded Steel, Hammer and Anvil, Eye of Iron | +2% DDG, +2% IDT, +8% DDT |
| 3 | Tempered Stance, Folded Steel, Resonant Parry, Every Blow Returned | +5% DDG, +5% DDT, +10% REF |
| 4 | Tempered Stance, Folded Steel, Resonant Parry, Eye of Iron | +2% DDG, +2% IDT, +5% DDT, +3% REF |
| 5 | Tempered Stance, Folded Steel, Eye of Iron, Honed Edge | +3% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Tempered Stance, Folded Steel, Eye of Iron, Sparks from the Forge | +2% DDG, +2% IDT, +5% DDT, +3% AB |
| 7 | Tempered Stance, Resonant Parry, Every Blow Returned, Eye of Iron | +5% DDG, +2% IDT, +2% DDT, +10% REF |
| 8 | Tempered Stance, Resonant Parry, Eye of Iron, Honed Edge | +3% IDG, +2% DDG, +2% IDT, +2% DDT, +3% REF |
| 9 | Tempered Stance, Resonant Parry, Eye of Iron, Sparks from the Forge | +2% DDG, +2% IDT, +2% DDT, +3% AB, +3% REF |
| 10 | Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides | +8% IDG, +2% DDG, +2% IDT, +2% DDT |
| 11 | Tempered Stance, Eye of Iron, Honed Edge, Sparks from the Forge | +3% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 12 | Tempered Stance, Eye of Iron, Sparks from the Forge, Branding Iron | +2% DDG, +5% IDT, +2% DDT, +10% AB |
| 13 | Eye of Iron, Honed Edge, One Cut Decides, Sparks from the Forge | +8% IDG, +2% IDT, +3% AB |
| 14 | Eye of Iron, Honed Edge, Sparks from the Forge, Branding Iron | +3% IDG, +5% IDT, +10% AB |

## Design notes

- Structure kept (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10); values re-cut in the 2026-10-04 batch. Eye of Iron carries only exposure and leads to self-amplification and attrition; Tempered Stance carries Decrease Damage Taken and Decrease Damage Given and leads to fortress and retaliation. Middle Guard Stance and Inner Peace carry both halves: Eye of Iron's routes sharpen their Increase Damage Given, Tempered Stance's routes harden their Decrease Damage Taken. Maxima over every legal allocation: Increase Damage Given +8%, Increase Damage Taken +5%, Afterburn +10%, Decrease Damage Taken +8%, Decrease Damage Given +5%, Reflect +10%, no Damage.
- No flat Damage. The Damage tag reaches all seven Metal strikes (40/40/40/40/45/45/50), so any flat point lifts Phantom Slash past the 50 Nuke tier; the former +5 route took it to 55, both 45 strikes to 50 and the four 40 strikes to 45. Honed Edge and One Cut Decides now sharpen the stances' Increase Damage Given instead.
- Both stance routes stop at +8% because their rows compound on the same two 40 AP casts (Middle Guard Stance free, Inner Peace sword-gated). Increase Damage Given: a hit inside Inner Peace's window ×1.12, ×1.19 with Middle Guard Stance also up. That is the largest self-amplification gain among the protected references (Blood-Enchanted Eyes' Feast of the Fallen ×1.11 over two rows; Shakunetsu Sakura ×1.07, ×1.10 with the sibling Hidden Art; Arashima ×1.06, ×1.07 with a fourth purchase): +8% is Arashima's single-row value on three compounding rows, so no coverage discount is applied; listed for the director. Decrease Damage Taken: both stances ×0.77, just short of Blood-Enchanted Eyes' Deathless Vitality (×0.75 over two rows, with +5% Decrease Damage Given beside it) and above Arashima's Unbroken Horizon (×0.85 on one row); all three rows reach ×0.68 but need a third 60 AP cast and the staff as well as the sword. Afterburn has one row; Branding Iron stops at +10% and adds exposure beside it. Reflect has one row and sits at its +10% ceiling; Every Blow Returned's suppression comes in addition and trims what Reflect returns (×1.07 under both suppression rows instead of ×1.25 unsuppressed).
- Fourth purchases: the all-offence builds mirror each other (One Cut Decides + Sparks: Increase Damage Given 8%, Increase Damage Taken 2%, Afterburn 3%; Branding Iron + Honed Edge: Afterburn 10%, Increase Damage Taken 5%, Increase Damage Given 3%). Gains over the unbought kit: in a self window with no exposure or burn One Cut Decides gives ×1.19 against ×1.07; on allied hits into a burning target under all three exposure rows Branding Iron gives ×1.20 against ×1.07; with every row up they are within 1% (×1.27, ×1.28). Defence routes add the sibling Hidden Art or Eye of Iron; Every Blow Returned + Folded Steel trades return for survival (returned share ×0.99, hit taken ×0.79 with a stance up under both suppression rows). No fourth stacks a capstone's own primary.
- Filters: Middle Guard Stance row 0 and Inner Peace row 0 are Highest-filtered and element-less, so they match element-less hits and hits of the user's highest stat; Inner Peace row 2 lists Earth/Fire/Metal/None/Water. Equilibrium Guard Strike and Vacuum Fan exposure carry Metal plus four stats (any stat-typed hit). The bloodline passive Increase Damage Given multiplies last.
- Delivery and gates: seven 60 AP strikes (cooldown 7; Crimson Thrust 6, an EMPTY_GROUND circle re-applied each round to enemies in it); Middle Guard Stance and Inner Peace are 40 AP self casts, cooldown 7, two-round buffs; Vacuum Fan is a free 40 AP spiral. Three weapon-style items gate nine of eleven jutsu (staff: Tranquil Guard, Resonance Ward, Pivoting Fortress; dagger: Phantom Slash, Crimson Thrust, Shadow Pierce; sword: Equilibrium Guard Strike, Harmonious Slash, Inner Peace). Equipment gates castability only.

## Risks and unproven interactions

- Item gates: retaliation is inert without the sword-style item (Harmonious Slash) and the burn without the dagger-style item (Crimson Thrust); self-amplification keeps only Middle Guard Stance without the sword, and the fortress's third row needs the staff. Whether two hand weapons can be wielded at once was not read at the pin (ENGINE_GAP_REGISTER G7).
- Stacking: jutsu Increase Damage Given/Taken rows multiply; Decrease Damage Taken/Given apply in sequence with a 10% floor. At the route maxima three Increase Damage Given rows give ×2.92 (from ×2.46) and three Decrease Damage Taken rows ×0.20 (from ×0.30). The stance buffs apply to every hit passing their filters, not only bloodline strikes. Not simulated.
- Afterburn is downstream: one ground-circle application row; every non-pierce hit the burning target takes (allies and weapons included) adds the percentage of the exposed hit, capped at 60% of that hit. No uptime simulation.
- Reflect reads the hit after reductions, so Tempered Stance, Folded Steel and the suppression rider shrink what is returned while they protect the caster: on the full route the returned share of a raw hit rises ×1.25 unsuppressed, ×1.15 under Vacuum Fan and ×1.07 under both suppression rows, and with Folded Steel and a stance up under both it is flat (×0.99). Pierce hits are reflected; cap 60% of each hit. Value depends on hits taken in each two-round window; not simulated.
- Ally hazard (validator warning accepted): Equilibrium Guard Strike row 1 (line exposure) is raised by Eye of Iron and Branding Iron; Vacuum Fan row 2 (spiral suppression) by Tempered Stance and Every Blow Returned. Allies in the area receive the raised values.
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

