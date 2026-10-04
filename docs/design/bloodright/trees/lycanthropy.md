# Lycanthropy — Blood Under the Moon

**Bloodline:** Lycanthropy (BR-043, rank B, `_zHoQitqM_tiiqX7Egv-p`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Lycanthropy classification / forked tree · **Classification:** Lycanthropy (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Frenzy — Increase Damage Given on Frenzy Assault and Feral Wrath (two self rows that compound) · secondary Regeneration — Heal on Frenzy Assault (one static row) · tertiary Raw strike — a +2 Damage rider on Undying Hunger, the regeneration capstone, with no setup (Moonlit Fury 40 → 42, Feral Wrath 50 → 52, above the Nuke tier; director choice).

Five supported rows: two 35% self Increase Damage Given rows (Frenzy Assault, Feral Wrath) that each amplify every element-less hit the caster lands in the two rounds after the cast and compound when both are up; two Taijutsu formula Damage rows (Moonlit Fury 40, Feral Wrath 50 at jutsu level 25); one static Heal row (Frenzy Assault 40 = 400 HP once per 7 rounds). Each Foundation owns one identity: The Beast Within feeds the frenzy (Red Moon Rising, +8% on both buff rows) and Moonbound Vigor outlasts the fight and finishes it (Undying Hunger, Heal +8% with a +2 Damage rider on both strikes, the tree's only flat Damage). Wound, cleanseprevent and move are unsupported; the 10% lifesteal passive is not a jutsu row.

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| The Beast Within | Foundation | How do I make the frenzy hit harder? |
| Moonbound Vigor | Foundation | How do I outlast the fight and still finish it? |
| Red Moon Rising | Advanced Art | sustained amplification: the full frenzy, every hit in the windows |
| Undying Hunger | Advanced Art | sustain offense: regeneration whose capstone adds a +2 raw-strike rider on the kit's two strikes (no setup) |

**Director review recommended:** Choose one for Undying Hunger. (a) As proposed: Heal +3% with a +2 Damage rider, lifting Feral Wrath 50 → 52 (above the Nuke tier) and Moonlit Fury 40 → 42. It is a rider on a sustain chain that restores at +2 the strike weight of the burst route the first pass deleted (Draft 4's Gnashing Fangs → Jaws of the Alpha); it has no setup and is not the RUL-2026-10-04-001/002 setup → payoff pattern, which this kit cannot host without a twin of Blood on the Wind (narrow_kit_exception). (b) Keep Damage unamplified and return Undying Hunger to the first pass's Heal +5% / Increase Damage Given +3% (route Heal +10%; a lighter second frenzy beside Red Moon Rising's +8%).

- Concern: Draft 4 declined a Heal capstone (+5% is 50 HP per cast); the first pass accepted one whose +3% Increase Damage Given rider was about as large as Red Moon Rising's own +4% step. This revision keeps the capstone but swaps that rider for the tree's only flat Damage, so the route's reason to exist is strike weight rather than a second, lighter frenzy. The Heal chain does not set the Damage up; it is trait representation and stops at +8% (+80 HP per cast) rather than the +10% guardrail.
- Concern: Undying Hunger against Frenzy: about even on the kit's two strikes inside one frenzy window and 4–5% ahead outside one, behind on every other hit in the windows (×1.37 against ×1.43; ×1.88 against ×2.04 with both up), plus 60 HP per cast. Frenzy stays the stronger build for a player who weaves basic attacks, weapons and other element-less jutsu into the windows. Not simulated.
- Concern: Six nodes against Draft 4's seven, and both Foundations are in every legal full build: no third Hidden Art exists that would not repeat Blood on the Wind or Lick the Wound or carry flat Damage before the capstone.
- Concern: Red Moon Rising's only fourth purchase, Moonbound Vigor, adds 20 HP per cast; accepted so that no second Increase Damage Given source sits beside the +8% route.

> **Narrow-kit exception:** Six nodes and two Advanced Arts rather than ten and four: the kit has three supported tags on five rows (Increase Damage Given x2, Damage x2, Heal x1), and only two Hidden Arts can differ in tag: Increase Damage Given (Blood on the Wind) and Heal (Lick the Wound); Damage is kept for an Advanced Art. The two identities are two 3-node chains: The Beast Within → Blood on the Wind → Red Moon Rising (frenzy) and Moonbound Vigor → Lick the Wound → Undying Hunger (regeneration whose capstone carries the tree's only flat Damage, a +2 rider with no setup). Draft 4's seventh node, Gnashing Fangs, was a flat-Damage Hidden Art that put Feral Wrath at 52 as Red Moon Rising's fourth purchase; a third route would need a Hidden Art that repeats Increase Damage Given (a twin of Blood on the Wind, and under The Beast Within a fourth purchase that lifts Red Moon Rising past +8%), repeats Heal on the one Heal row, or carries flat Damage before the capstone, so none is added. Universal nodes accepted: with two 3-node chains every 4 BP build holds both Foundations, so the real choice is which chain to finish; the only other full build is the no-capstone hybrid (both Hidden Arts).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Lycanthropy-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | The Beast Within | Foundation | None | +2% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 04 | Blood on the Wind | Hidden Art | The Beast Within | +2% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 05 | Red Moon Rising | Advanced Art | Blood on the Wind | +4% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 06 | Moonbound Vigor | Foundation | None | +2% Heal (self buff) | Frenzy Assault / 1 |
| 07 | Lick the Wound | Hidden Art | Moonbound Vigor | +3% Heal (self buff) | Frenzy Assault / 1 |
| 08 | Undying Hunger | Advanced Art | Lick the Wound | +3% Heal (self buff); +2 Damage (damage) | Feral Wrath, Frenzy Assault, Moonlit Fury / 3 |

Connections: 01→04, 04→05, 06→07, 07→08. Advanced Arts: 2; any two cost at least 6 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **The Beast Within** — The change begins in the blood: claws lengthen, and every blow lands heavier. Frenzy Assault and Feral Wrath Increase Damage Given 35 → 37% (self, 2 rounds each). 2 rows.
- **Blood on the Wind** — One whiff of an open wound and the frenzy takes hold. Both frenzy rows 37 → 39% with The Beast Within (self, 2 rounds each). 2 rows.
- **Red Moon Rising** — Under a bloody moon there is no holding back, and nothing left to hold back. Sustained amplification: both frenzy rows 35 → 43% on the full route (+8%); with both windows up a matching hit is multiplied by ×1.43 × 1.43 ≈ ×2.04 instead of ×1.82.
- **Moonbound Vigor** — Flesh knits under moonlight as readily as it tears. Frenzy Assault Heal 40 → 42 = 420 HP, one tick on the following round (40 AP, cooldown 7). 1 row, the kit's only Heal.
- **Lick the Wound** — What a beast cannot outfight, it outlasts. Frenzy Assault Heal 42 → 45 with Moonbound Vigor = 450 HP on the following round. 1 row.
- **Undying Hunger** — The wound closes, and the hunger only sharpens. Regeneration with a raw-strike rider: Frenzy Assault Heal 40 → 48 on the full route (+8%, 480 HP on the following round); Moonlit Fury 40 → 42 and Feral Wrath 50 → 52 EP (above the 50 Nuke tier; director choice).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | HEAL |
|---|---|---:|---:|---:|
| Red Moon Rising (Frenzy) | The Beast Within, Blood on the Wind, Red Moon Rising, Moonbound Vigor | — | +8% | +2% |
| Undying Hunger (Sustain offense) | Moonbound Vigor, Lick the Wound, Undying Hunger, The Beast Within | +2 | +2% | +8% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Red Moon Rising:** Both frenzy rows 35 → 43% (+8%): every element-less hit the caster lands in the two rounds after each cast, basic attacks and weapons included, is amplified, and with both windows up the rows compound to about ×2.04 (×1.82 at base). Moonbound Vigor is the only legal fourth purchase (+20 HP per Frenzy Assault cast, 400 → 420): a near-token point, accepted so that no second Increase Damage Given source sits beside Red Moon Rising.
- **Undying Hunger:** Frenzy Assault's Heal 40 → 48 (+8%, 480 HP on the following round) and a +2 Damage rider on both kit strikes (Moonlit Fury 40 → 42, Feral Wrath 50 → 52, above the Nuke tier). The Beast Within is the only legal fourth purchase (both frenzy rows 37%). Against the Frenzy build it gives up 6% Increase Damage Given for 60 HP more per cast and the heavier strikes: inside one frenzy window the strikes come out about even (Feral Wrath 52 × 1.37 ≈ 71.2 against 50 × 1.43 = 71.5; Moonlit Fury 42 × 1.37 ≈ 57.5 against 57.2) and outside one they are 4–5% ahead, while every other hit in the windows is lighter (×1.37 against ×1.43; ×1.88 against ×2.04 with both up).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Frenzy | Sustain offense |
|---|---:|---|---|---:|---:|---:|
| Moonlit Fury | 0 | wound (unsupported) | enemy | 30% | 30% | 30% |
| Moonlit Fury | 1 | cleanseprevent (unsupported) | enemy | 100 | 100 | 100 |
| Moonlit Fury | 2 | Damage | enemy | 40 | 40 | 42 (+2) |
| Frenzy Assault | 0 | Increase Damage Given | self | 35% | 43% (+8) | 37% (+2) |
| Frenzy Assault | 1 | Heal | self | 40 | 42 (+2) | 48 (+8) |
| Feral Wrath | 0 | Damage | enemy | 50 | 50 | 52 (+2) |
| Feral Wrath | 1 | move (unsupported) | self | 1 | 1 | 1 |
| Feral Wrath | 2 | Increase Damage Given | self | 35% | 43% (+8) | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 3, 3: 4, 4: 3
- Full-budget allocations: 3; numerically non-dominated (per-tag totals): 3; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +8% Increase Damage Given, +8% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Red Moon Rising: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Undying Hunger: +8% Heal (2 + 3 + 3; off band)
- Supported rows in kit: 5 (DMG 2, HEAL 1, IDG 2)
- Strongest full build by row-weighted total: The Beast Within, Blood on the Wind, Red Moon Rising, Moonbound Vigor (raw +10, row-weighted 18)
- Lowest row-weighted node: Moonbound Vigor (2)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Feral Wrath 50 -> 52
- classification status: requires classification extension (director decision)
- universal node: 01 (The Beast Within), 06 (Moonbound Vigor) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Moonlit Fury | 2 | 40 (Normal) | 42 (Normal) |
| Feral Wrath | 0 | 50 (Nuke) | **52 (above Nuke)** |

Above-Nuke rationale: Undying Hunger's +2 Damage lifts Feral Wrath 50 → 52, past the 50 Nuke tier (Moonlit Fury 40 → 42 stays Normal). It is not the Blood-Enchanted Eyes / Shakunetsu Sakura setup → payoff pattern (RUL-2026-10-04-001/002): it is a +2 rider on the regeneration chain's capstone with no setup, since Moonbound Vigor and Lick the Wound raise only Frenzy Assault's Heal and neither prime nor multiply the strikes. It is kept to restore, at +2, the strike weight of the burst route the first pass deleted (Draft 4's Gnashing Fangs → Jaws of the Alpha, +5, Feral Wrath 50 → 55). Only the magnitude follows those rulings: +2 on a 40/50 pair (Shakunetsu Sakura's pair), the tree's only flat Damage, never alongside Red Moon Rising's +8% frenzy (6 BP). No legal allocation adds more than +2. Fable proposal; the director chooses between this and keeping Damage unamplified (design_review.director_review).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Red Moon Rising | +8% IDG | Moonbound Vigor *(highest diagnostic)* | +8% IDG, +2% HEAL | 18 |
| Undying Hunger | +2 Damage, +8% HEAL | The Beast Within *(highest diagnostic)* | +2 Damage, +2% IDG, +8% HEAL | 16 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | The Beast Within, Blood on the Wind, Red Moon Rising, Moonbound Vigor | +8% IDG, +2% HEAL |
| 2 | The Beast Within, Blood on the Wind, Moonbound Vigor, Lick the Wound | +4% IDG, +5% HEAL |
| 3 | The Beast Within, Moonbound Vigor, Lick the Wound, Undying Hunger | +2 Damage, +2% IDG, +8% HEAL |

## Design notes

- Structure: two 3-node chains, The Beast Within → Blood on the Wind → Red Moon Rising (Increase Damage Given +2/+2/+4%) and Moonbound Vigor → Lick the Wound → Undying Hunger (Heal +2/+3/+3%, with +2 Damage on the capstone). Owning both Advanced Arts costs 6 BP, so a build holds one. Draft 4's Damage chain (Gnashing Fangs → Jaws of the Alpha, +2/+3), which the first pass deleted, is not restored as a chain; a +2 rider on the Heal chain's capstone carries its strike weight in place of the first pass's +3% Increase Damage Given rider. The Heal nodes are not a setup (they neither prime nor multiply the strikes), and the chain stops at +8% Heal, below the +10% single-row guardrail, because its Heal is trait representation rather than the route's lever.
- Damage: Draft 4's +5 route lifted Moonlit Fury 40 → 45 (a full tier) and Feral Wrath 50 → 55 (past the Nuke tier), and Gnashing Fangs alone put Feral Wrath at 52 as Red Moon Rising's fourth purchase. Undying Hunger's +2 (Moonlit Fury 40 → 42, Feral Wrath 50 → 52) is the only flat Damage and needs the whole Moonbound Vigor chain, so Red Moon Rising's 43% frenzy never multiplies a 52 strike (6 BP). Formula damage is linear in EP (tags.ts powerEffect): +2 is ×1.05 on Moonlit Fury and ×1.04 on Feral Wrath.
- Frenzy magnitude: each 35% row multiplies every element-less hit for the two rounds after its cast (Frenzy Assault's Taijutsu filter is not binding on an element-less row), and the two compound when both are up. Red Moon Rising's route is held at +8% rather than the +10% guardrail: ×1.43 × 1.43 ≈ ×2.04 against ×1.82 at base (+12% in a shared window, +6% in a single one); +10% would give ×2.10.
- Delivery: all three jutsu have cooldown 7. Frenzy Assault is a 40 AP self cast (Increase Damage Given 2 rounds; static Heal rounds 1 = one tick on the following round at 10 HP per heal power). Feral Wrath is a 60 AP ground circle whose Increase Damage Given row is SELF, realized on the caster at cast. Neither buff helps the round it is cast, Feral Wrath's own strike included (§3b). Both windows coincide fully only when the two are cast in the same round (100 AP); cast one round apart, Frenzy Assault first, they share one round and Feral Wrath's strike lands under Frenzy Assault's buff. Feral Wrath's strike is therefore under at most one kit window; Moonlit Fury and off-kit hits can be under both.
- Allocations: three legal full builds, each holding both Foundations and none dominated: Frenzy (01, 04, 05, 06: +8% Increase Damage Given, +2% Heal), Undying Hunger (01, 06, 07, 08: +2% Increase Damage Given, +8% Heal, +2 Damage) and the no-capstone hybrid (01, 04, 06, 07: +4% Increase Damage Given, +5% Heal). Frenzy amplifies everything in the windows; Undying Hunger puts its weight on the kit's own strikes and the heal. Maxima over every legal allocation: Increase Damage Given +8%, Heal +8%, Damage +2.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Lycanthropy' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision, and all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Regeneration value: static Heal is 10 HP per point, so Undying Hunger's route adds 80 HP once per 7 rounds (400 → 480), about 1.6% of a 5,050 HP level-100 pool (calcHP = 100 + 50 × (level − 1)). The capstone's Heal step stays at Lick the Wound's +3 rather than +5: two more points (20 HP per cast) would only reach the +10% guardrail. The route's pull is its +2 Damage; the Heal is the trait's only row.
- Frenzy breadth: both rows reach basic attacks, weapons and element-less normal jutsu as well as the kit, and the bloodline's Taijutsu Increase Damage Given passive multiplies last; extra damage also feeds the 10% lifesteal passive (shared 60% leech budget). Realized value depends on what lands in the windows; not simulated.
- Above the Nuke tier: Undying Hunger lifts Feral Wrath 50 → 52 (Moonlit Fury 40 → 42 stays Normal) with no setup. Unlike the exposure setups of Blood-Enchanted Eyes and Shakunetsu Sakura, the Heal commitment does not multiply the payoff; only the kit's own frenzy rows (37% with the forced fourth purchase, The Beast Within) and the bloodline passive do.
- Unsupported rows: Moonlit Fury's wound 30% and cleanseprevent, and Feral Wrath's move, receive nothing. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Lycanthropy-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

