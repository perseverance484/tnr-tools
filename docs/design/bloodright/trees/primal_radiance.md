# Primal Radiance — The Burning Hunt

**Bloodline:** Primal Radiance (BR-055, rank C, `ZewrhKT-qBQxT1eNoBWFP`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Fire classification / forked tree · **Classification:** Fire (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense, three ways to kill: Primal Incineration's brand, Afterburn over exposure (Pyre of the Hunted); a controlled +2 Damage on both Fire strikes (Apex Conflagration); Fire Style: Beast's self Increase Damage Given (Primal Rampage) · secondary Defense: Fire Style: Squirrel's self Decrease Damage Taken (Den of Embers) · tertiary Exposure held at +2% (Hunter's Brand) so the brand does not enlarge its own Afterburn.

Six supported rows: two Fire Damage rows (Fire Style: Beast 50, Fire Style: Squirrel 40 EP at jutsu level 25) and one row each of Afterburn and Increase Damage Taken (Primal Incineration's brand), Increase Damage Given (Beast's self buff) and Decrease Damage Taken (Squirrel's self buff). Hunter's Brand answers "How do I bring down the marked prey: burn it out or strike it down?" with Pyre of the Hunted (Afterburn 45% over 37% exposure) and Apex Conflagration (Beast 50 → 52, Squirrel 40 → 42 EP after Fang and Ember's 37% self buff; the Shakunetsu Sakura 50 → 52 precedent). Hide and Fang answers "How do I empower the beast itself: armour it or enrage it?" with Den of Embers (Squirrel 40%) and Primal Rampage (Beast 45%). Potency reaches matching supported tags on all Fire jutsu (RUL-2026-10-03-005); wound and move are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hunter's Brand | Foundation | How do I bring down the marked prey: burn it out or strike it down? |
| Hide and Fang | Foundation | How do I empower the beast itself: armour it or enrage it? |
| Apex Conflagration | Advanced Art | burst: self-amplification setup, controlled +2 Damage payoff on both Fire strikes, Beast's own hit included |
| Pyre of the Hunted | Advanced Art | exposure: the branded prey takes more from every hit (Afterburn), allies' included |
| Den of Embers | Advanced Art | fortress |
| Primal Rampage | Advanced Art | sustained amplification: the caster's hits land harder on every target in the window |

**Director review recommended:** Fire Style: Beast 50 → 52 (Squirrel 40 → 42) under Apex Conflagration, above the 50 Nuke tier; restored as a controlled burst payoff on the RUL-2026-10-04-002 precedent (Shakunetsu Sakura: the same 40/50 Damage tier pair, Scorch: Sakuragari 40 → 42, Sakura-ame 50 → 52, approved at +2) and RUL-2026-10-04-001, with an above_nuke_rationale. Fire is far more widely shared than Scorch, so the +2 also lifts any off-kit 50 EP Fire row to 52 (count unverified). The setup is +2% self Increase Damage Given, not the anchors' exposure setups (Shakunetsu's Burning Petal Carpet +2% Increase Damage Taken, Blood-Enchanted Eyes' Opened Veins +3%): here either would be a legal fourth for Pyre of the Hunted and stack exposure under its 45% Afterburn (a Squirrel hit on the mark ≈ ×2.74 at +3%, ≈ ×2.72 at +2%). Confirm the 50 → 52 with its wider Fire reach, Fang and Ember sharing Beast's self-buff row with Kindled Fury, and that Primal Rampage's niche (concerns) is enough beside Apex Conflagration.

- Concern: Fang and Ember (+2%) and Kindled Fury (+3%) amplify the same row, Beast's self buff, on different roots (a departure from roster rule R4). Afterburn and Decrease Damage Taken already own Hidden Arts; an Increase Damage Taken setup would feed Pyre of the Hunted's mark, which R1 forbids (Blood-Enchanted Eyes' +3% gives ≈ ×2.74); a flat commit would put Beast at 51 in four builds without the capstone. Precedent for a shared row: Arashima's self Increase Damage Given setup into +2 Damage (RUL-2026-10-04-003) and Shakunetsu Sakura's two +3% Increase Damage Given Hidden Arts. They never stack under one capstone (at most +7% in the no-Advanced hybrid 01+02+06+09).
- Concern: Apex Conflagration with Hide and Fang is at least equal to Primal Rampage with Hunter's Brand on the kit's two Fire strikes, in and out of Beast's window: inside it, Squirrel on the mark ×2.70 against ×2.68 and off it ×1.46 against ×1.45; outside it the +2 still applies (Squirrel ×1.05, Beast ×1.04, against ×1.00), while Rampage's +10% is live only in the 2 rounds after each Beast cast (cooldown 7). Exposure (37%) and Squirrel's reduction (32%) are identical. Rampage's niche is in-window hits the +2 cannot reach: basic attacks and non-Fire hits on the caster's highest stat (×1.45 against ×1.39), plus the sturdier Radiant Hide fourth. A loadout-dependent niche, not a dominance; director to confirm it is enough. Not simulated.
- Concern: Pyre of the Hunted with Hide and Fang and Apex Conflagration with Smoldering Trail both reach ×2.72 on a Squirrel hit on the mark; Pyre leads for allies' hits (×1.45 Afterburn on any non-pierce hit), Apex off the mark. Not simulated.
- Concern: Increase Damage Taken reaches only +2% (Hunter's Brand): exposure is kept near base so the brand's setup does not compound its own Afterburn payoff.
- Concern: Two of four routes (Pyre of the Hunted, Den of Embers) amplify element-less rows the current row-element resolver cannot reach; they depend on the proposed jutsu-classification resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Fire jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hunter's Brand | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Primal Incineration / 1 |
| 02 | Fang and Ember | Hidden Art | Hunter's Brand | +2% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 03 | Apex Conflagration | Advanced Art | Fang and Ember | +2 Damage (damage) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 04 | Smoldering Trail | Hidden Art | Hunter's Brand | +3% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 05 | Pyre of the Hunted | Advanced Art | Smoldering Trail | +7% Afterburn (enemy debuff) | Primal Incineration / 1 |
| 06 | Hide and Fang | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Fire Style: Beast, Fire Style: Squirrel / 2 |
| 07 | Radiant Hide | Hidden Art | Hide and Fang | +3% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 08 | Den of Embers | Advanced Art | Radiant Hide | +5% Decrease Damage Taken (self buff) | Fire Style: Squirrel / 1 |
| 09 | Kindled Fury | Hidden Art | Hide and Fang | +3% Increase Damage Given (self buff) | Fire Style: Beast / 1 |
| 10 | Primal Rampage | Advanced Art | Kindled Fury | +5% Increase Damage Given (self buff) | Fire Style: Beast / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hunter's Brand** — Every quarry the beast marks is already half-burned. Primal Incineration exposure 35 → 37% on one target for 2 rounds (Fire hits and hits on the caster's highest offence stat). Roots the brand (Smoldering Trail) and the strike (Fang and Ember); Primal Rampage's offensive fourth and Den of Embers' team-only alternative.
- **Fang and Ember** — Teeth of ember, breath of wildfire. Commits to the kill: Fire Style: Beast self Increase Damage Given 35 → 37% (39% with Hide and Fang), live the 2 rounds after each 60 AP cast, so the Squirrel that follows lands harder.
- **Apex Conflagration** — When the alpha roars, the whole forest catches. Burst: Fire Style: Beast 50 → 52 and Fire Style: Squirrel 40 → 42 EP (+2 Damage; Beast above the 50 Nuke tier, see above_nuke_rationale). Raw power needs no window, so it reaches Beast's own strike (×1.04), which its self buff never does; Squirrel ×1.05 × 1.37 ≈ ×1.44 after Fang and Ember.
- **Smoldering Trail** — Where the hunted beast ran, the ground still smolders. Commits to the brand: Primal Incineration Afterburn 35 → 38% (one 40 AP cast, cooldown 7, live the 2 rounds after it), added to every non-pierce hit the target takes, allies' included.
- **Pyre of the Hunted** — The hunt ends on a pyre the prey built with its own flight. Exposure: Primal Incineration Afterburn 35 → 45% on the full route (+10%) over Hunter's Brand's 37% exposure; a Fire or highest-stat hit on the target lands ×1.37, then burns for 45% (×1.37 × 1.45 ≈ ×1.99; ×1.82 unmodified), allies' hits included.
- **Hide and Fang** — Thick pelt, sharp fang, both lit from within. Fire Style: Squirrel self Decrease Damage Taken 30 → 32% and Fire Style: Beast self Increase Damage Given 35 → 37%, each live the 2 rounds after its 60 AP cast. The usual fourth for Pyre of the Hunted and Apex Conflagration.
- **Radiant Hide** — A pelt of living flame that swallows every blow. Squirrel self Decrease Damage Taken 32 → 35% with Hide and Fang (no element, all four stat types: every non-pierce hit).
- **Den of Embers** — Within the burning den, nothing reaches the beast. Fortress: Squirrel self Decrease Damage Taken 30 → 40% on the full route (+10%), incoming hits ×0.60 (×0.70 unmodified) for the 2 rounds after each 60 AP cast. One effect; Beast's self buff stays at Hide and Fang's 37%.
- **Kindled Fury** — Fury stoked until the blood itself glows. Beast self Increase Damage Given 37 → 40% with Hide and Fang (Fire hits and hits on the caster's highest offence stat or general, 2 rounds per 60 AP cast).
- **Primal Rampage** — The radiant beast unbound, and nothing left to hold it. Sustained amplification: Beast self Increase Damage Given 35 → 45% on the full route (+10%); every matching caster hit in the 2 rounds after the cast lands ×1.45 (×1.35 unmodified) on any target. One effect; Squirrel's reduction stays at 32%.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Apex Conflagration (Burst) | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +2 | +4% | +2% | +2% | — |
| Pyre of the Hunted (Exposure brand) | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | — | +2% | +2% | +2% | +10% |
| Primal Rampage (Fury window) | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | — | +10% | +2% | +2% | — |
| Den of Embers (Fortress) | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | — | +5% | — | +10% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Apex Conflagration:** Fire Style: Beast 50 → 52 and Fire Style: Squirrel 40 → 42 EP (Apex Conflagration +2 Damage) over Hunter's Brand's 37% exposure, with Beast's self buff at 39% (Fang and Ember +2%, Hide and Fang +2%). Cast Incineration and Beast in one 100 AP turn and the next round's Squirrel lands ×1.05 × 1.37 × 1.39 × 1.35 ≈ ×2.70 on the mark (×2.46 unmodified); a Beast cast on a mark laid the round before lands ×1.04 × 1.37 × 1.35 ≈ ×1.92 (×1.82). Hide and Fang adds Squirrel 32%; Smoldering Trail (Afterburn 38%) is the all-in fourth (Squirrel ≈ ×2.72 on the mark, Beast ≈ ×1.97).
- **Pyre of the Hunted:** One 40 AP Primal Incineration marks a target for the 2 rounds after the cast: Afterburn 45% (Smoldering Trail +3%, Pyre of the Hunted +7%) over 37% exposure (Hunter's Brand). Every non-pierce hit on it, allies' included, burns for 45%; Fire and highest-stat hits are first raised ×1.37 (×1.37 × 1.45 ≈ ×1.99). Hide and Fang is the fourth (Beast 37%, Squirrel 32%): cast Incineration and Beast in one 100 AP turn and the next round's Squirrel lands ×1.37 × 1.37 × 1.45 ≈ ×2.72 on the mark (×2.46 unmodified). Fang and Ember gives the same 37% without Squirrel's 32%, so it never beats Hide and Fang.
- **Primal Rampage:** Beast's self buff reaches 45% (Hide and Fang +2%, Kindled Fury +3%, Primal Rampage +5%): for the 2 rounds after each 60 AP cast every caster Fire hit, and every hit on the caster's highest offence stat or general, lands ×1.45 on any target (never Beast's own hit, cooldown 7). Hunter's Brand is the offensive fourth (exposure 37%; a Squirrel hit on the mark ×1.37 × 1.45 × 1.35 ≈ ×2.68 with Incineration's unmodified 35% Afterburn); Radiant Hide (Squirrel 35%) is the sturdier one.
- **Den of Embers:** Squirrel's self reduction reaches 40% (Hide and Fang +2%, Radiant Hide +3%, Den of Embers +5%), realized on the caster at cast and live on every non-pierce hit for the 2 rounds after each 60 AP cast (cooldown 6): incoming hits ×0.60. Kindled Fury is the fourth that keeps the beast fighting (Beast 40%); Hunter's Brand (exposure 37%) is the team-only alternative, ahead of Kindled Fury only for allies' Fire or highest-stat hits on the mark (×1.37 against ×1.35).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure brand | Fury window | Fortress |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Primal Incineration | 0 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Primal Incineration | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |
| Fire Style: Beast | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Fire Style: Beast | 1 | Increase Damage Given | self | 35% | 39% (+4) | 37% (+2) | 45% (+10) | 40% (+5) |
| Fire Style: Beast | 2 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Fire Style: Squirrel | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Fire Style: Squirrel | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Fire Style: Squirrel | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 10; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Increase Damage Given, +2% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Apex Conflagration: +2 Damage (0 + 0 + 2; off band)
  - Route Pyre of the Hunted: +10% Afterburn (0 + 3 + 7; on band)
  - Route Den of Embers: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Primal Rampage: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 6 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang (raw +16, row-weighted 16)
- Lowest row-weighted node: Hunter's Brand (2)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Fire Style: Beast 50 -> 52

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Fire Style: Beast | 0 | 50 (Nuke) | **52 (above Nuke)** |
| Fire Style: Squirrel | 0 | 40 (Normal) | 42 (Normal) |

Above-Nuke rationale: Apex Conflagration's +2 Damage lifts Fire Style: Beast 50 → 52 (Fire Style: Squirrel 40 → 42), past the 50 Nuke tier, as the payoff of a deliberate burst route (Hunter's Brand exposure → Fang and Ember self buff → Apex Conflagration). Precedent: RUL-2026-10-04-002, Shakunetsu Sakura, with the same 40/50 Damage tier pair (Scorch: Sakuragari 40 → 42, Sakura-ame 50 → 52 under Conflagration in Bloom's +2), and RUL-2026-10-04-001 (Blood-Enchanted Eyes, Reaper's Embrace 50 → 52). The reach differs: Fire is a far more widely shared element than Scorch (29 other bloodlines against Scorch's one), so Apex's +2 also lifts any off-kit 50 EP Fire row the owner casts to 52 (count unverified). Only builds holding Apex Conflagration exceed 50, by at most +2. Fable proposal; flagged for director review.

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Apex Conflagration | +2 Damage, +2% IDG, +2% IDT | Smoldering Trail | +2 Damage, +2% IDG, +2% IDT, +3% AB | 11 |
| Apex Conflagration | +2 Damage, +2% IDG, +2% IDT | Hide and Fang *(highest diagnostic)* | +2 Damage, +4% IDG, +2% IDT, +2% DDT | 12 |
| Pyre of the Hunted | +2% IDT, +10% AB | Fang and Ember | +2% IDG, +2% IDT, +10% AB | 14 |
| Pyre of the Hunted | +2% IDT, +10% AB | Hide and Fang *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% AB | 16 |
| Den of Embers | +2% IDG, +10% DDT | Hunter's Brand | +2% IDG, +2% IDT, +10% DDT | 14 |
| Den of Embers | +2% IDG, +10% DDT | Kindled Fury *(highest diagnostic)* | +5% IDG, +10% DDT | 15 |
| Primal Rampage | +10% IDG, +2% DDT | Hunter's Brand | +10% IDG, +2% IDT, +2% DDT | 14 |
| Primal Rampage | +10% IDG, +2% DDT | Radiant Hide *(highest diagnostic)* | +10% IDG, +5% DDT | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hunter's Brand, Fang and Ember, Apex Conflagration, Smoldering Trail | +2 Damage, +2% IDG, +2% IDT, +3% AB |
| 2 | Hunter's Brand, Fang and Ember, Apex Conflagration, Hide and Fang | +2 Damage, +4% IDG, +2% IDT, +2% DDT |
| 3 | Hunter's Brand, Fang and Ember, Smoldering Trail, Pyre of the Hunted | +2% IDG, +2% IDT, +10% AB |
| 4 | Hunter's Brand, Fang and Ember, Smoldering Trail, Hide and Fang | +4% IDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Hunter's Brand, Fang and Ember, Hide and Fang, Radiant Hide | +4% IDG, +2% IDT, +5% DDT |
| 6 | Hunter's Brand, Fang and Ember, Hide and Fang, Kindled Fury | +7% IDG, +2% IDT, +2% DDT |
| 7 | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang | +2% IDG, +2% IDT, +2% DDT, +10% AB |
| 8 | Hunter's Brand, Smoldering Trail, Hide and Fang, Radiant Hide | +2% IDG, +2% IDT, +5% DDT, +3% AB |
| 9 | Hunter's Brand, Smoldering Trail, Hide and Fang, Kindled Fury | +5% IDG, +2% IDT, +2% DDT, +3% AB |
| 10 | Hunter's Brand, Hide and Fang, Radiant Hide, Den of Embers | +2% IDG, +2% IDT, +10% DDT |
| 11 | Hunter's Brand, Hide and Fang, Radiant Hide, Kindled Fury | +5% IDG, +2% IDT, +5% DDT |
| 12 | Hunter's Brand, Hide and Fang, Kindled Fury, Primal Rampage | +10% IDG, +2% IDT, +2% DDT |
| 13 | Hide and Fang, Radiant Hide, Den of Embers, Kindled Fury | +5% IDG, +10% DDT |
| 14 | Hide and Fang, Radiant Hide, Kindled Fury, Primal Rampage | +10% IDG, +5% DDT |

## Design notes

- 2026-10-04 rebalance, roster pass (BALANCE_REVIEW_METHOD.md; roster rule R1). The first pass deleted the burst branch because any flat Damage lifts Fire Style: Beast past 50, which shrank the tree to 8 nodes and made Hide and Fang universal. Restored on the director pattern: Fang and Ember is now a +2% Increase Damage Given setup (was +2 Damage) and Apex Conflagration a +2 Damage payoff (was +3): Beast 50 → 52, Squirrel 40 → 42 EP, never 55 or 45. Kept from the first pass: single-effect capstones (Pyre of the Hunted without its +3% exposure rider, Den of Embers without +2% Increase Damage Given, Primal Rampage without +2% Decrease Damage Taken) and every other value.
- Why a self-amplification setup (a departure from roster rule R4): Afterburn and Decrease Damage Taken already own Hidden Arts (Smoldering Trail, Radiant Hide). An Increase Damage Taken setup would sit under Hunter's Brand and feed Pyre of the Hunted's mark, which roster rule R1 forbids: as Pyre's fourth, Blood-Enchanted Eyes' +3% (Opened Veins) puts exposure at 40% under 45% Afterburn (a Squirrel hit on the mark ×1.40 × 1.35 × 1.45 ≈ ×2.74), and Shakunetsu Sakura's +2% (Burning Petal Carpet) ties Pyre + Hide and Fang at ≈ ×2.72. A +1 Damage commit would lift Beast to 51 in four 4 BP builds without the capstone, Pyre's among them. Fang and Ember therefore shares Kindled Fury's row (Beast's self buff) on the other root at a lower value, as Arashima's Gathering Thunderhead (+2% Increase Damage Given into Sundered Sky's +2 Damage, RUL-2026-10-04-003) shares its sibling route's Increase Damage Given row and Shakunetsu Sakura carries two +3% Increase Damage Given Hidden Arts (Kindled Boughs, Blossom Dominion). It raises the Squirrel that carries the +2 and is never Pyre's better fourth.
- Maxima over every legal allocation: Afterburn +10%, Increase Damage Given +10%, Decrease Damage Taken +10%, Increase Damage Taken +2%, Damage +2 (above 50 only with Apex Conflagration). Exposure stays at the Foundation: Afterburn reads the already-raised hit, so exposure under the burn enlarges its own payoff.
- Filters (§3): Beast's self buff (Fire; stat and general Highest) multiplies the caster's Fire hits and hits sharing the caster's highest offence stat or general. Incineration's exposure (Fire; stat Highest) covers Fire hits and hits on the debuff caster's highest offence stat (§4b). Afterburn and Squirrel's reduction carry no element and list all four stat types: every non-pierce hit. Damage is linear in power (powerEffect, tags.ts 1436-1462), so +2 is ×1.04 on Beast and ×1.05 on Squirrel. The bloodline's Fire Increase Damage Given passive (15% + 0.15 per level) multiplies last.
- Delivery (§3b, §4b): Incineration is 40 AP, cooldown 7, single target, range 4; Beast 60 AP, cooldown 7, single target; Squirrel 60 AP, cooldown 6, an empty-ground circle whose SELF reduction is realized on the caster at cast (no positioning). Every buff and debuff is live only in the 2 rounds after its cast, so Beast never raises its own hit and a Beast cast in Incineration's round is not exposed.
- Fourth purchases: Apex Conflagration takes Hide and Fang (Beast 39%, Squirrel 32%) or Smoldering Trail (Afterburn 38%); Pyre of the Hunted takes Hide and Fang (Fang and Ember is dominated); Primal Rampage takes Hunter's Brand (exposure 37%) or Radiant Hide (Squirrel 35%); Den of Embers takes Kindled Fury (Beast 40%) or, for allies' hits on the mark, Hunter's Brand. With Incineration and Beast live, a Squirrel hit on the mark lands ×2.72 under Pyre + Hide and Fang and under Apex + Smoldering Trail, ×2.70 under Apex + Hide and Fang, ×2.68 under Rampage + Hunter's Brand, ×2.55 under Den + Kindled Fury (×2.46 unmodified). Pyre leads for allies on the mark (any non-pierce hit ×1.45), Rampage on basic attacks and non-Fire highest-stat hits (×1.45 against Apex's ×1.39), Apex on the kit's strikes off the mark (Beast ×1.04, Squirrel ×1.46 against Rampage's ×1.00 and ×1.45) and outside Beast's window, where the +2 still applies (Squirrel ×1.05, Beast ×1.04, against ×1.00). No fourth makes a route automatic.

## Risks and unproven interactions

- Classification: Fire is shared with many other bloodlines (expected under RUL-2026-10-03-005). The two Damage rows, the exposure and Beast's self buff carry Fire; Incineration's Afterburn and Squirrel's reduction carry no element and need the proposed jutsu-classification resolver. Off-kit Fire coverage is unverified.
- Damage reach: Apex Conflagration's +2 reaches every Fire Damage row the owner casts, off-kit Fire jutsu included (another 50 EP Fire jutsu also becomes 52). Only the capstone exceeds 50; see above_nuke_rationale.
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

