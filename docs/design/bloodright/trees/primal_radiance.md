# Primal Radiance — The Burning Hunt

**Bloodline:** Primal Radiance (BR-055, rank C, `ZewrhKT-qBQxT1eNoBWFP`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Fire classification / forked tree · **Classification:** Fire (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense, three ways to kill: Primal Incineration's brand, burned (Pyre of the Hunted, Afterburn) or laid open (Apex Conflagration, exposure); Fire Style: Beast's self Increase Damage Given (Primal Rampage) · secondary Defense: Fire Style: Squirrel's self Decrease Damage Taken (Den of Embers) · tertiary Damage unamplified: Fire Style: Beast stays at 50 (Nuke) and Fire Style: Squirrel at 40.

Six supported rows: two Fire Damage rows (Fire Style: Beast 50, Fire Style: Squirrel 40 EP at jutsu level 25) and one row each of Afterburn and Increase Damage Taken (Primal Incineration's brand), Increase Damage Given (Beast's self buff) and Decrease Damage Taken (Squirrel's self buff). Damage is left unamplified: the kit lists no traits, and Beast's own 35% self buff is live only in the 2 rounds after its cast, so Beast opens the window that Squirrel lands in rather than finishing. Hunter's Brand answers "How do I bring down the marked prey: burn it out or lay it open?" with Pyre of the Hunted (Afterburn 45% over 37% exposure) and Apex Conflagration (exposure 45%, ×1.074, after Fang and Ember's 37% self buff). Hide and Fang answers "How do I empower the beast itself: armour it or enrage it?" with Den of Embers (Squirrel 40%) and Primal Rampage (Beast 45%). Potency reaches matching supported tags on all Fire jutsu (RUL-2026-10-03-005); wound and move are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hunter's Brand | Foundation | How do I bring down the marked prey: burn it out or lay it open? |
| Hide and Fang | Foundation | How do I empower the beast itself: armour it or enrage it? |
| Apex Conflagration | Advanced Art | exposure: the brand lays the prey open, so every Fire or highest-stat hit on it lands harder, allies' included; Fang and Ember sharpens the caster's own |
| Pyre of the Hunted | Advanced Art | burn: every non-pierce hit on the branded prey adds Afterburn, allies' included |
| Den of Embers | Advanced Art | fortress |
| Primal Rampage | Advanced Art | sustained amplification: the caster's hits land harder on every target in Beast's window |

**Director review recommended:** Roster questions: DQ-B (Apex Conflagration +10% exposure on one row, Primal Incineration 35 → 45%, ×1.074).

- Concern: Apex Conflagration and Pyre of the Hunted pay off the same Primal Incineration cast through different rows, and split by coverage, not size: with Hide and Fang both reach ×2.68 on a caster Squirrel on the mark in Beast's window; Pyre leads outside that window (×1.99 against ×1.96 on a Fire hit on the mark) and on hits outside the exposure filter (×1.45 against ×1.35); Apex + Smoldering Trail leads Pyre + Fang and Ember on Fire and highest-stat hits on the mark (×2.00 against ×1.99), and exposure also raises residual damage. Not simulated.
- Concern: Apex Conflagration with Smoldering Trail carries exposure 45% under Afterburn 38% (≈ ×2.00 on a Fire or highest-stat hit on the mark, ×1.82 unmodified): the reverse of the stack R12 bounds (≤ +5%); this tree holds exposure at Hunter's Brand's +2% beside Pyre of the Hunted's 45% Afterburn.
- Concern: Fang and Ember (+2%) and Kindled Fury (+3%) amplify Beast's self buff on different roots; neither is a legal fourth for the other's route (not a twin under refined R4), and they meet only in the no-Advanced hybrid 01+02+06+09 (+5%).
- Concern: Two of four routes (Pyre of the Hunted, Den of Embers) amplify element-less rows the current row-element resolver cannot reach; they depend on the proposed jutsu-classification resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Fire jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hunter's Brand | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Primal Incineration / 1 |
| 02 | Fang and Ember | Hidden Art | Hunter's Brand | +2% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 03 | Apex Conflagration | Advanced Art | Fang and Ember | +8% Increase Damage Taken (enemy debuff) | Primal Incineration / 1 |
| 04 | Smoldering Trail | Hidden Art | Hunter's Brand | +3% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 05 | Pyre of the Hunted | Advanced Art | Smoldering Trail | +7% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 06 | Hide and Fang | Foundation | None | +2% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 07 | Radiant Hide | Hidden Art | Hide and Fang | +3% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 08 | Den of Embers | Advanced Art | Radiant Hide | +5% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 09 | Kindled Fury | Hidden Art | Hide and Fang | +3% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 10 | Primal Rampage | Advanced Art | Kindled Fury | +7% Increase Damage Given (self buff) | Fire Style: Beast / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hunter's Brand** — Every quarry the beast marks is already half-burned. Primal Incineration exposure 35 → 37% on one target for 2 rounds (Fire hits and hits on the caster's highest offence stat). Roots the burn (Smoldering Trail) and the exposure (Fang and Ember); Primal Rampage's offensive fourth and Den of Embers' team-only alternative.
- **Fang and Ember** — Teeth of ember, breath of wildfire. Commits the caster's strike (Apex Conflagration's setup): Fire Style: Beast self Increase Damage Given 35 → 37%, live the 2 rounds after each 60 AP cast, so the Squirrel that follows lands harder on the mark. Also Pyre of the Hunted's sharper fourth.
- **Apex Conflagration** — When the alpha roars, the quarry stands open to every fang. Exposure: Primal Incineration exposure 35 → 45% on the full route (+10%, ×1.074; Shakunetsu Sakura's anchor ×1.075) for the 2 rounds after one 40 AP cast: every Fire or highest-stat hit on the target, allies' included, lands ×1.45 (×1.35 unmodified). Fang and Ember's 37% self buff stacks on the caster's own strikes in Beast's window; Afterburn stays at 35%.
- **Smoldering Trail** — Where the hunted beast ran, the ground still smolders. Commits to the brand: Primal Incineration Afterburn 35 → 38% (one 40 AP cast, cooldown 7, live the 2 rounds after it), added to every non-pierce hit the target takes, allies' included.
- **Pyre of the Hunted** — The hunt ends on a pyre the prey built with its own flight. Burn: Primal Incineration Afterburn 35 → 45% on the full route (+10%) over Hunter's Brand's 37% exposure; a Fire or highest-stat hit on the target lands ×1.37, then burns for 45% (×1.37 × 1.45 ≈ ×1.99; ×1.82 unmodified), allies' hits included.
- **Hide and Fang** — The pelt catches first; the fang waits for its spark. Fire Style: Squirrel self Decrease Damage Taken 30 → 32%, live the 2 rounds after each 60 AP cast. Roots the hide (Radiant Hide) and the fury (Kindled Fury); the sturdy fourth for Pyre of the Hunted and Apex Conflagration.
- **Radiant Hide** — A pelt of living flame that swallows every blow. Squirrel self Decrease Damage Taken 32 → 35% with Hide and Fang (no element, all four stat types: every non-pierce hit).
- **Den of Embers** — Within the burning den, nothing reaches the beast. Fortress: Squirrel self Decrease Damage Taken 30 → 40% on the full route (+10%), incoming hits ×0.60 (×0.70 unmodified) for the 2 rounds after each 60 AP cast. One effect; Beast's self buff stays at its base 35%.
- **Kindled Fury** — Fury stoked until the blood itself glows. Commits to the fury: Fire Style: Beast self Increase Damage Given 35 → 38% (Fire hits and hits on the caster's highest offence stat or general, 2 rounds per 60 AP cast).
- **Primal Rampage** — The radiant beast unbound, and nothing left to hold it. Sustained amplification: Beast self Increase Damage Given 35 → 45% on the full route (Kindled Fury +3%, Primal Rampage +7%); every matching caster hit in the 2 rounds after the cast lands ×1.45 (×1.35 unmodified) on any target. One effect; Squirrel's reduction stays at Hide and Fang's 32%.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|
| Apex Conflagration (Exposure) | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +2% | +10% | +2% | — |
| Pyre of the Hunted (Burning brand) | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | — | +2% | +2% | +10% |
| Primal Rampage (Fury window) | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +10% | +2% | +2% | — |
| Den of Embers (Fortress) | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | +3% | — | +10% | — |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Apex Conflagration:** One 40 AP Primal Incineration lays a target open for the 2 rounds after the cast: exposure 45% (Hunter's Brand +2%, Apex Conflagration +8%; ×1.074), so every Fire or highest-stat hit on it, allies' included, lands ×1.45; Fang and Ember adds Beast 37% for the caster's own strikes. Cast Incineration and Beast in one 100 AP turn and the next round's Squirrel lands ×1.37 × 1.45 × 1.35 ≈ ×2.68 on the mark (×2.46 unmodified), level with Pyre of the Hunted and Primal Rampage; Hide and Fang adds Squirrel 32%. Smoldering Trail is the all-in fourth (Afterburn 38%, ≈ ×2.74) without Squirrel's 32%.
- **Pyre of the Hunted:** One 40 AP Primal Incineration marks a target for the 2 rounds after the cast: Afterburn 45% (Smoldering Trail +3%, Pyre of the Hunted +7%) over 37% exposure (Hunter's Brand). Every non-pierce hit on it, allies' included, burns for 45%; Fire and highest-stat hits are first raised ×1.37 (×1.37 × 1.45 ≈ ×1.99). Hide and Fang is the sturdy fourth (Squirrel 32%): cast Incineration and Beast in one 100 AP turn and the next round's Squirrel lands ×1.35 × 1.37 × 1.45 ≈ ×2.68 on the mark (×2.46 unmodified). Fang and Ember is the sharp one (Beast 37%, ≈ ×2.72) without Squirrel's 32%.
- **Primal Rampage:** Beast's self buff reaches 45% (Kindled Fury +3%, Primal Rampage +7%): for the 2 rounds after each 60 AP cast every caster Fire hit, and every hit on the caster's highest offence stat or general, lands ×1.45 on any target (never Beast's own hit, cooldown 7); Hide and Fang adds Squirrel 32%. Hunter's Brand is the offensive fourth (exposure 37%; a Squirrel hit on the mark ×1.45 × 1.37 × 1.35 ≈ ×2.68 with Incineration's unmodified 35% Afterburn); Radiant Hide (Squirrel 35%) is the sturdier one.
- **Den of Embers:** Squirrel's self reduction reaches 40% (Hide and Fang +2%, Radiant Hide +3%, Den of Embers +5%), realized on the caster at cast and live on every non-pierce hit for the 2 rounds after each 60 AP cast (cooldown 6): incoming hits ×0.60. Kindled Fury is the fourth that keeps the beast fighting (Beast 38%); Hunter's Brand (exposure 37%) is the team-only alternative, ahead of Kindled Fury only for allies' Fire or highest-stat hits on the mark (×1.37 against ×1.35).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Exposure | Burning brand | Fury window | Fortress |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Primal Incineration | 0 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Primal Incineration | 1 | Increase Damage Taken | enemy | 35% | 45% (+10) | 37% (+2) | 37% (+2) | 35% |
| Fire Style: Beast | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Fire Style: Beast | 1 | Increase Damage Given | self | 35% | 37% (+2) | 35% | 45% (+10) | 38% (+3) |
| Fire Style: Beast | 2 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Fire Style: Squirrel | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Fire Style: Squirrel | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Fire Style: Squirrel | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 11; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +10% Increase Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Apex Conflagration: +10% Increase Damage Taken (2 + 0 + 8; on band)
  - Route Pyre of the Hunted: +10% Afterburn (0 + 3 + 7; on band)
  - Route Den of Embers: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Primal Rampage: +10% Increase Damage Given (0 + 3 + 7; on band)
- Supported rows in kit: 6 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Hunter's Brand, Fang and Ember, Apex Conflagration, Smoldering Trail (raw +15, row-weighted 15)
- Lowest row-weighted node: Hunter's Brand (2)

Validator warnings:

- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Fire Style: Beast 50 (Nuke), Fire Style: Squirrel 40 (Normal)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Apex Conflagration | +2% IDG, +10% IDT | Smoldering Trail *(highest diagnostic)* | +2% IDG, +10% IDT, +3% AB | 15 |
| Apex Conflagration | +2% IDG, +10% IDT | Hide and Fang | +2% IDG, +10% IDT, +2% DDT | 14 |
| Pyre of the Hunted | +2% IDT, +10% AB | Fang and Ember | +2% IDG, +2% IDT, +10% AB | 14 |
| Pyre of the Hunted | +2% IDT, +10% AB | Hide and Fang *(highest diagnostic)* | +2% IDT, +2% DDT, +10% AB | 14 |
| Den of Embers | +10% DDT | Hunter's Brand | +2% IDT, +10% DDT | 12 |
| Den of Embers | +10% DDT | Kindled Fury *(highest diagnostic)* | +3% IDG, +10% DDT | 13 |
| Primal Rampage | +10% IDG, +2% DDT | Hunter's Brand | +10% IDG, +2% IDT, +2% DDT | 14 |
| Primal Rampage | +10% IDG, +2% DDT | Radiant Hide *(highest diagnostic)* | +10% IDG, +5% DDT | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hunter's Brand, Fang and Ember, Apex Conflagration, Smoldering Trail | +2% IDG, +10% IDT, +3% AB |
| 2 | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +2% IDG, +10% IDT, +2% DDT |
| 3 | Hunter's Brand, Fang and Ember, Smoldering Trail, Pyre of the Hunted | +2% IDG, +2% IDT, +10% AB |
| 4 | Hunter's Brand, Fang and Ember, Smoldering Trail, Hide and Fang | +2% IDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Hunter's Brand, Fang and Ember, Hide and Fang, Radiant Hide | +2% IDG, +2% IDT, +5% DDT |
| 6 | Hunter's Brand, Fang and Ember, Hide and Fang, Kindled Fury | +5% IDG, +2% IDT, +2% DDT |
| 7 | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | +2% IDT, +2% DDT, +10% AB |
| 8 | Hunter's Brand, Smoldering Trail, Hide and Fang, Radiant Hide | +2% IDT, +5% DDT, +3% AB |
| 9 | Hunter's Brand, Smoldering Trail, Hide and Fang, Kindled Fury | +3% IDG, +2% IDT, +2% DDT, +3% AB |
| 10 | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | +2% IDT, +10% DDT |
| 11 | Hunter's Brand, Hide and Fang, Radiant Hide, Kindled Fury | +3% IDG, +2% IDT, +5% DDT |
| 12 | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +10% IDG, +2% IDT, +2% DDT |
| 13 | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | +3% IDG, +10% DDT |
| 14 | Hide and Fang, Radiant Hide, Kindled Fury, Primal Rampage | +10% IDG, +5% DDT |

## Design notes

- 2026-10-04 rebalance, final cleanup (BALANCE_REVIEW_METHOD.md; roster rule R1′). The kit lists no traits and Fire Style: Beast is not its finisher: Beast's row 1 (self Increase Damage Given 35%) is live only in the 2 rounds after its cast, so the D-rank, 60 AP, cooldown 7 Beast opens the window that Fire Style: Squirrel (B rank, cooldown 6) lands in, and Primal Incineration is a pure brand. Damage is therefore unamplified (Beast stays 50, Squirrel 40) and Apex Conflagration changes from +2 Damage to +8% Increase Damage Taken, so the brand's two rows pay off on two routes: Pyre of the Hunted burns the prey out, Apex Conflagration lays it open. Kept: Fang and Ember (+2% self Increase Damage Given, now Apex's setup), the single-effect capstones and every other value.
- Why Fang and Ember stays a self-amplification setup: an Increase Damage Taken setup would be a legal fourth for Pyre of the Hunted and raise exposure under its 45% Afterburn, which the tree chooses to hold at Hunter's Brand's +2% (R12 would allow up to +5%; the setup would also feed Pyre's mark, the fourth-BP pattern the method rejects), and a flat Damage commit is not used on a 50-row kit (R9). Fang and Ember and Kindled Fury share Beast's self-buff row on different roots; neither is a legal fourth for the other's route, so they never stack under a capstone (refined R4: not a twin). Apex's route carries +2% Increase Damage Given against Primal Rampage's +10%; its payoff is exposure, not a second amplification route.
- Maxima over every legal allocation: Increase Damage Given +10%, Increase Damage Taken +10%, Decrease Damage Taken +10%, Afterburn +10%, Damage none. Allocations holding Pyre of the Hunted reach exposure +2% (R12 ≤ +5%); allocations holding Apex Conflagration reach Afterburn +3% (Smoldering Trail). Top offensive package (Increase Damage Given × Taken, all windows live): ×1.090 (Apex Conflagration with Fang and Ember; Primal Rampage with Hunter's Brand), under Blood-Enchanted Eyes' ×1.234.
- Filters (§3): Beast's self buff (Fire; stat and general Highest) multiplies the caster's Fire hits and hits sharing the caster's highest offence stat or general. Incineration's exposure (Fire; stat Highest) covers Fire hits and hits on the debuff caster's highest offence stat (§4b), direct and residual; Afterburn adds to instant hits only. Afterburn and Squirrel's reduction carry no element and list all four stat types: every non-pierce hit. The bloodline's Fire Increase Damage Given passive (15% + 0.15 per level) multiplies last.
- Delivery (§3b, §4b): Incineration is 40 AP, cooldown 7, single target, range 4; Beast 60 AP, cooldown 7, single target; Squirrel 60 AP, cooldown 6, an empty-ground circle whose SELF reduction is realized on the caster at cast (no positioning). Every buff and debuff is live only in the 2 rounds after its cast, so Beast never raises its own hit and a Beast cast in Incineration's round is not exposed.
- Fourth purchases: Apex Conflagration takes Hide and Fang (Squirrel 32%) or Smoldering Trail (Afterburn 38%); Pyre of the Hunted takes Hide and Fang (Squirrel 32%) or Fang and Ember (Beast 37%); Primal Rampage takes Hunter's Brand (exposure 37%) or Radiant Hide (Squirrel 35%); Den of Embers takes Kindled Fury (Beast 38%) or, for allies' hits on the mark, Hunter's Brand. With Incineration and Beast live, a Squirrel hit on the mark lands ×2.74 under Apex + Smoldering Trail, ×2.72 under Pyre + Fang and Ember, ×2.68 under Apex + Hide and Fang, Pyre + Hide and Fang and Rampage + Hunter's Brand, ×2.52 under Den + Kindled Fury (×2.46 unmodified). Pyre leads on hits outside the exposure filter (×1.45 against ×1.35–1.38) and on Fire hits on the mark outside Beast's window (×1.99 against Apex + Hide and Fang's ×1.96); Apex + Smoldering Trail leads on Fire and highest-stat hits on the mark (×2.00 against ×1.99); Rampage leads off the mark in Beast's window (×1.45 against ×1.37). No fourth makes a route automatic.

## Risks and unproven interactions

- Classification: Fire is shared with many other bloodlines (expected under RUL-2026-10-03-005). Incineration's exposure and Beast's self buff carry Fire; Incineration's Afterburn and Squirrel's reduction carry no element and need the proposed jutsu-classification resolver. Off-kit Fire coverage is unverified.
- Exposure: Apex Conflagration puts Incineration's exposure at 45% (×1.074) on one target for the 2 rounds after the cast; every Fire or highest-stat hit it takes, allies' and off-kit Fire jutsu included, lands ×1.45. With Smoldering Trail as the fourth, Afterburn 38% reads the raised hit (≈ ×2.00 on such a hit). Damage rows are untouched: Beast stays at the 50 Nuke tier.
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

