# Primal Radiance — The Burning Hunt

**Bloodline:** Primal Radiance (BR-055, rank C, `ZewrhKT-qBQxT1eNoBWFP`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Fire classification / forked tree · **Classification:** Fire (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense from the kit's two windows: Fire Style: Beast's self Increase Damage Given (Primal Rampage) and Primal Incineration's brand, Afterburn over exposure (Pyre of the Hunted) · secondary Defense: Fire Style: Squirrel's self Decrease Damage Taken (Den of Embers) · tertiary Flat Damage stays unamplified: Fire Style: Beast is already a 50 EP Nuke.

The two Fire Damage rows (Fire Style: Beast 50, Fire Style: Squirrel 40 EP at jutsu level 25) stay unamplified: Beast is already a Nuke, so any flat Damage lifts it past 50. The offense is carried by the kit's two 2-round windows instead. Hunter's Brand answers "How do I make the branded prey pay for every hit?" with one chain, Pyre of the Hunted (Primal Incineration's Afterburn 45% over 37% exposure on one target). Hide and Fang answers "How do I empower the beast itself: hit harder or refuse to fall?" with Primal Rampage (Beast's self buff 45%) and Den of Embers (Squirrel's self reduction 40%). Potency reaches matching supported tags on all Fire jutsu (RUL-2026-10-03-005); wound and move are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hunter's Brand | Foundation | How do I make the branded prey pay for every hit? |
| Hide and Fang | Foundation | How do I empower the beast itself: hit harder or refuse to fall? |
| Pyre of the Hunted | Advanced Art | attrition: one brand makes every hit on the prey burn, allies' included |
| Den of Embers | Advanced Art | fortress |
| Primal Rampage | Advanced Art | sustained amplification: the caster's hits land harder on every target |

**Director review recommended:** Structural: flat Damage is removed rather than re-cut (any flat Damage lifts Fire Style: Beast past 50), leaving three Advanced Arts with Hide and Fang in every build. Confirm the narrow-kit exception, or choose the Blood-Enchanted Eyes pattern as a fourth route (Fang and Ember +3% Increase Damage Taken → Apex Conflagration +2 Damage: Beast 50 → 52, Squirrel 40 → 42).

- Concern: Pyre of the Hunted and Primal Rampage are close in solo (a Squirrel hit on the mark ×2.72 against ×2.68 with their best fourths); Pyre leads in team play because Afterburn adds to allies' hits of any element, Rampage on every other target. Not simulated.
- Concern: Hide and Fang is universal, so Pyre of the Hunted's fourth purchase is forced; Hunter's Brand roots one chain because Afterburn and exposure share one cast.
- Concern: Increase Damage Taken reaches only +2% (Hunter's Brand): exposure is kept near base so the brand's setup does not compound its own Afterburn payoff.
- Concern: Two of three routes (Pyre of the Hunted, Den of Embers) amplify element-less rows the current row-element resolver cannot reach; they depend on the proposed jutsu-classification resolver.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. Supported rows: two Fire Damage rows (Fire Style: Beast 50, Fire Style: Squirrel 40 EP) and one row each of Afterburn and Increase Damage Taken (both on Primal Incineration's target), Increase Damage Given (Beast's self buff) and Decrease Damage Taken (Squirrel's self buff). Flat Damage is declined because Beast is a 50 EP Nuke and any flat Damage lifts it past 50, so the old Burst branch (Fang and Ember → Apex Conflagration) is removed rather than re-cut. Afterburn and Increase Damage Taken share one cast, target and window, so Hunter's Brand roots one brand chain; a second brand capstone would read as the same choice. Hide and Fang is a universal node (in all 8 legal 4 BP builds) because Hunter's Brand roots a single chain.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Fire jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hunter's Brand | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Primal Incineration / 1 |
| 04 | Smoldering Trail | Hidden Art | Hunter's Brand | +3% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 05 | Pyre of the Hunted | Advanced Art | Smoldering Trail | +7% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 06 | Hide and Fang | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 07 | Radiant Hide | Hidden Art | Hide and Fang | +3% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 08 | Den of Embers | Advanced Art | Radiant Hide | +5% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 09 | Kindled Fury | Hidden Art | Hide and Fang | +3% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 10 | Primal Rampage | Advanced Art | Kindled Fury | +5% Increase Damage Given (self buff) | Fire Style: Beast / 1 |

Connections: 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hunter's Brand** — Every quarry the beast marks is already half-burned. Primal Incineration exposure 35 → 37% on one target for 2 rounds (Fire hits and hits on the caster's highest offence stat). Roots the brand chain; the beast's routes buy it as their offensive fourth.
- **Smoldering Trail** — Where the hunted beast ran, the ground still smolders. Commits to the brand: Primal Incineration Afterburn 35 → 38% (one 40 AP cast, cooldown 7, live the 2 rounds after it), added to every non-pierce hit the target takes, allies' included.
- **Pyre of the Hunted** — The hunt ends on a pyre the prey built with its own flight. Attrition: Primal Incineration Afterburn 35 → 45% on the full route (+10%) over Hunter's Brand's 37% exposure; a Fire or highest-stat hit on the target lands ×1.37, then burns for 45% (×1.37 × 1.45 ≈ ×1.99; ×1.82 unmodified).
- **Hide and Fang** — Thick pelt, sharp fang, both lit from within. Fire Style: Squirrel self Decrease Damage Taken 30 → 32% and Fire Style: Beast self Increase Damage Given 35 → 37%, each live the 2 rounds after its 60 AP cast. In every legal build, because Hunter's Brand roots a single chain.
- **Radiant Hide** — A pelt of living flame that swallows every blow. Squirrel self Decrease Damage Taken 32 → 35% with Hide and Fang (no element, all four stat types: every non-pierce hit).
- **Den of Embers** — Within the burning den, nothing reaches the beast. Fortress: Squirrel self Decrease Damage Taken 30 → 40% on the full route (+10%), incoming hits ×0.60 (×0.70 unmodified) for the 2 rounds after each 60 AP cast. One effect; Beast's self buff stays at Hide and Fang's 37%.
- **Kindled Fury** — Fury stoked until the blood itself glows. Beast self Increase Damage Given 37 → 40% with Hide and Fang (Fire hits and hits on the caster's highest offence stat or general, 2 rounds per 60 AP cast).
- **Primal Rampage** — The radiant beast unbound, and nothing left to hold it. Sustained amplification: Beast self Increase Damage Given 35 → 45% on the full route (+10%); every matching caster hit in the 2 rounds after the cast lands ×1.45 (×1.35 unmodified) on any target. One effect; Squirrel's reduction stays at 32%.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|
| Pyre of the Hunted (Brand) | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | +2% | +2% | +2% | +10% |
| Primal Rampage (Fury window) | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +10% | +2% | +2% | — |
| Den of Embers (Fortress) | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | +5% | — | +10% | — |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Pyre of the Hunted:** One 40 AP Primal Incineration marks a target for the 2 rounds after the cast: Afterburn 45% (Smoldering Trail +3%, Pyre of the Hunted +7%) over 37% exposure (Hunter's Brand). Every non-pierce hit on it, allies' included, burns for 45%; Fire and highest-stat hits are first raised ×1.37 (×1.37 × 1.45 ≈ ×1.99). Hide and Fang is the only fourth (Beast 37%, Squirrel 32%): cast Incineration and Beast in one 100 AP turn and the next round's Squirrel lands ×1.37 × 1.37 × 1.45 ≈ ×2.72 on the mark (×2.46 unmodified).
- **Primal Rampage:** Beast's self buff reaches 45% (Hide and Fang +2%, Kindled Fury +3%, Primal Rampage +5%): for the 2 rounds after each 60 AP cast every caster Fire hit, and every hit on the caster's highest offence stat or general, lands ×1.45 on any target (never Beast's own hit, cooldown 7). Hunter's Brand is the offensive fourth (exposure 37%; a Squirrel hit on the mark ×1.37 × 1.45 × 1.35 ≈ ×2.68 with Incineration's unmodified 35% Afterburn); Radiant Hide (Squirrel 35%) is the sturdier one.
- **Den of Embers:** Squirrel's self reduction reaches 40% (Hide and Fang +2%, Radiant Hide +3%, Den of Embers +5%), realized on the caster at cast and live on every non-pierce hit for the 2 rounds after each 60 AP cast (cooldown 6): incoming hits ×0.60. Kindled Fury is the fourth that keeps the beast fighting (Beast 40%); Hunter's Brand (exposure 37%) is the alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Brand | Fury window | Fortress |
|---|---:|---|---|---:|---:|---:|---:|
| Primal Incineration | 0 | Afterburn | enemy | 35% | 45% (+10) | 35% | 35% |
| Primal Incineration | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 35% |
| Fire Style: Beast | 0 | Damage | enemy | 50 | 50 | 50 | 50 |
| Fire Style: Beast | 1 | Increase Damage Given | self | 35% | 37% (+2) | 45% (+10) | 40% (+5) |
| Fire Style: Beast | 2 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% |
| Fire Style: Squirrel | 0 | Damage | enemy | 40 | 40 | 40 | 40 |
| Fire Style: Squirrel | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Fire Style: Squirrel | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +10% Increase Damage Given, +2% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Pyre of the Hunted: +10% Afterburn (0 + 3 + 7; on band)
  - Route Den of Embers: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Primal Rampage: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 6 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang (raw +16, row-weighted 16)
- Lowest row-weighted node: Hunter's Brand (2)

Validator warnings:

- universal node: 06 (Hide and Fang) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Fire Style: Beast 50 (Nuke), Fire Style: Squirrel 40 (Normal)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Pyre of the Hunted | +2% IDT, +10% AB | Hide and Fang *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% AB | 16 |
| Den of Embers | +2% IDG, +10% DDT | Hunter's Brand | +2% IDG, +2% IDT, +10% DDT | 14 |
| Den of Embers | +2% IDG, +10% DDT | Kindled Fury *(highest diagnostic)* | +5% IDG, +10% DDT | 15 |
| Primal Rampage | +10% IDG, +2% DDT | Hunter's Brand | +10% IDG, +2% IDT, +2% DDT | 14 |
| Primal Rampage | +10% IDG, +2% DDT | Radiant Hide *(highest diagnostic)* | +10% IDG, +5% DDT | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | +2% IDG, +2% IDT, +2% DDT, +10% AB |
| 2 | Hunter's Brand, Smoldering Trail, Hide and Fang, Radiant Hide | +2% IDG, +2% IDT, +5% DDT, +3% AB |
| 3 | Hunter's Brand, Smoldering Trail, Hide and Fang, Kindled Fury | +5% IDG, +2% IDT, +2% DDT, +3% AB |
| 4 | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | +2% IDG, +2% IDT, +10% DDT |
| 5 | Hunter's Brand, Hide and Fang, Radiant Hide, Kindled Fury | +5% IDG, +2% IDT, +5% DDT |
| 6 | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +10% IDG, +2% IDT, +2% DDT |
| 7 | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | +5% IDG, +10% DDT |
| 8 | Hide and Fang, Radiant Hide, Kindled Fury, Primal Rampage | +10% IDG, +5% DDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Removed: Fang and Ember (+2 Damage) and Apex Conflagration (+3 Damage); the +5 route lifted Fire Style: Beast 50 → 55 and Fire Style: Squirrel 40 → 45, and even +1 lifts Beast past 50. Removed riders: Pyre of the Hunted's +3% exposure, Den of Embers' +2% Increase Damage Given and Primal Rampage's +2% Decrease Damage Taken, so each capstone carries one effect. Kept: every other value and the edges 01→04→05, 06→07→08, 06→09→10.
- Maxima over every legal allocation: Afterburn +10%, Increase Damage Given +10%, Decrease Damage Taken +10%, Increase Damage Taken +2%, no flat Damage. Exposure stays at the Foundation: Afterburn reads the already-raised hit, so exposure under the burn enlarges its own payoff, and the old +3% exposure rider took Pyre's combo past Primal Rampage's (×2.78 against ×2.68).
- Filters (§3): Beast's self buff (Fire; stat and general Highest) multiplies the caster's Fire hits and hits sharing the caster's highest offence stat or general. Incineration's exposure (Fire; stat Highest) covers Fire hits and hits on the debuff caster's highest offence stat (§4b). Afterburn and Squirrel's reduction carry no element and list all four stat types: every non-pierce hit. The bloodline's Fire Increase Damage Given passive (15% + 0.15 per level) multiplies last.
- Delivery (§3b, §4b): Incineration is 40 AP, cooldown 7, single target, range 4; Beast 60 AP, cooldown 7, single target; Squirrel 60 AP, cooldown 6, an empty-ground circle whose SELF reduction is realized on the caster at cast (no positioning). Every buff and debuff is live only in the 2 rounds after its cast, so Beast never raises its own hit.
- Fourth purchases: Pyre of the Hunted takes Hide and Fang (forced); Primal Rampage takes Hunter's Brand (exposure 37%) or Radiant Hide (Squirrel 35%); Den of Embers takes Kindled Fury (Beast 40%) or Hunter's Brand. With Incineration and Beast live, a Squirrel hit on the mark lands ×2.72 under Pyre with Hide and Fang and ×2.68 under Rampage with Hunter's Brand (×2.46 unmodified); Rampage wins on every other target, Pyre for allies hitting the mark (any non-pierce hit ×1.45 against ×1.35). No fourth makes a route automatic.

## Risks and unproven interactions

- Classification: Fire is shared with many other bloodlines (expected under RUL-2026-10-03-005). With flat Damage gone, the exposure and Beast's self buff are the only amplified rows that carry Fire; Incineration's Afterburn and Squirrel's reduction carry no element and need the proposed jutsu-classification resolver. Off-kit Fire coverage is unverified.
- Afterburn: Pyre of the Hunted puts Incineration's Afterburn at 45% on one target for the 2 rounds after the cast. Every non-pierce hit it takes (kit, normal jutsu, weapons, basic attacks, allies) adds floor(damage × 45%); other Afterburn sources add under the 60%-of-hit cumulative cap, so 15 points remain. Not a damage instance; downstream hits were not simulated.
- Reach: Beast's 45% self buff multiplies matching caster hits on every target in its window (Squirrel's circle, basic attacks, off-kit Fire jutsu), and the bloodline Fire passive multiplies last. Squirrel's reduction is caster-only.
- Friendly fire: Incineration may be aimed at an ally (OTHER_USER); its Afterburn (friendly fire none = ALL) then lands on the ally, while the exposure (ENEMIES) is withheld. Beast's wound and Squirrel's move are unsupported and untouched.
- Context: the bloodline's 10% Water Increase Damage Taken passive (a standing weakness) is untouched; skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Fire jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

