# Lycanthropy — Blood Under the Moon

**Bloodline:** Lycanthropy (BR-043, rank B, `_zHoQitqM_tiiqX7Egv-p`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Lycanthropy classification / forked tree · **Classification:** Lycanthropy (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Frenzy — Increase Damage Given on Frenzy Assault and Feral Wrath (two self rows that compound) · secondary Regeneration — Heal on Frenzy Assault (one static row) with a frenzy rider · tertiary Damage left unamplified: Feral Wrath is a 50 EP Nuke-tier hit.

Five supported rows: two 35% self Increase Damage Given rows (Frenzy Assault, Feral Wrath) that each amplify every element-less hit the caster lands in the two rounds after the cast and compound when both are up; two Taijutsu formula Damage rows (Moonlit Fury 40, Feral Wrath 50 at jutsu level 25); one static Heal row (Frenzy Assault 40 = 400 HP once per 7 rounds). Each Foundation owns one identity: The Beast Within feeds the frenzy (Red Moon Rising, +8% on both buff rows) and Moonbound Vigor heals through the fight (Undying Hunger, Heal +10% with a +3% frenzy rider). Flat Damage is left out: any +N lifts Feral Wrath past the 50 Nuke tier, and the frenzy rows already multiply both attacks. Wound, cleanseprevent and move are unsupported; the 10% lifesteal passive is not a jutsu row.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| The Beast Within | Foundation | How do I make the frenzy hit harder? |
| Moonbound Vigor | Foundation | How do I outlast the fight? |
| Red Moon Rising | Advanced Art | sustained amplification: the full frenzy |
| Undying Hunger | Advanced Art | regeneration: a bigger heal that keeps a frenzy |

- Concern: Regeneration is the weaker route in raw value: static Heal is 10 HP per point, so its +10% Heal is 100 HP per Frenzy Assault cast; the +3% frenzy rider keeps it a choice rather than a trap.
- Concern: Both Foundations are in every legal full build (two 3-node chains); the choice is which chain to finish.
- Concern: Damage is left unamplified; a +2 Damage payoff would lift Feral Wrath 50 → 52, above the Nuke tier.

> **Narrow-kit exception:** Six nodes and two Advanced Arts rather than ten and four: the kit has three supported tags on five rows, and this revision targets two of them (Increase Damage Given x2, Heal x1). The two identities are two 3-node chains: The Beast Within → Blood on the Wind → Red Moon Rising (frenzy) and Moonbound Vigor → Lick the Wound → Undying Hunger (regeneration). Universal nodes accepted: with two 3-node chains every 4 BP build holds both Foundations, so the real choice is which chain to finish; the only other full build is the no-capstone hybrid (both Hidden Arts). A third route was declined: the only remaining tag is Damage, and any flat Damage lifts Feral Wrath 50 past the Nuke tier; a second Hidden Art under either Foundation could only repeat Increase Damage Given or Heal on the same rows (filler, and an Increase Damage Given sibling would stack with Red Moon Rising).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Lycanthropy-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | The Beast Within | Foundation | None | +2% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 04 | Blood on the Wind | Hidden Art | The Beast Within | +2% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 05 | Red Moon Rising | Advanced Art | Blood on the Wind | +4% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 2 |
| 06 | Moonbound Vigor | Foundation | None | +2% Heal (self buff) | Frenzy Assault / 1 |
| 07 | Lick the Wound | Hidden Art | Moonbound Vigor | +3% Heal (self buff) | Frenzy Assault / 1 |
| 08 | Undying Hunger | Advanced Art | Lick the Wound | +5% Heal (self buff); +3% Increase Damage Given (self buff) | Feral Wrath, Frenzy Assault / 3 |

Connections: 01→04, 04→05, 06→07, 07→08. Advanced Arts: 2; any two cost at least 6 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **The Beast Within** — The change begins in the blood: claws lengthen, and every blow lands heavier. Frenzy Assault and Feral Wrath Increase Damage Given 35 → 37% (self, 2 rounds each). 2 rows.
- **Blood on the Wind** — One whiff of an open wound and the frenzy takes hold. Both frenzy rows 37 → 39% with The Beast Within (self, 2 rounds each). 2 rows.
- **Red Moon Rising** — Under a bloody moon there is no holding back, and nothing left to hold back. Sustained amplification: both frenzy rows 35 → 43% on the full route (+8%); with both windows up a matching hit is multiplied by ×1.43 × 1.43 ≈ ×2.04 instead of ×1.82.
- **Moonbound Vigor** — Flesh knits under moonlight as readily as it tears. Frenzy Assault Heal 40 → 42 = 420 HP, one tick on the following round (40 AP, cooldown 7). 1 row, the kit's only Heal.
- **Lick the Wound** — What a beast cannot outfight, it outlasts. Frenzy Assault Heal 42 → 45 with Moonbound Vigor = 450 HP on the following round. 1 row.
- **Undying Hunger** — The wound closes, and the hunger only sharpens. Regeneration: Frenzy Assault Heal 40 → 50 on the full route (+10%, 500 HP on the following round); both frenzy rows 35 → 38%, 40% with The Beast Within.

## Complete four-purchase examples

| Build | Purchases | IDG | HEAL |
|---|---|---:|---:|
| Red Moon Rising (Frenzy) | The Beast Within, Blood on the Wind, Red Moon Rising, Moonbound Vigor | +8% | +2% |
| Undying Hunger (Regeneration) | Moonbound Vigor, Lick the Wound, Undying Hunger, The Beast Within | +5% | +10% |

Abbreviations: IDG = Increase Damage Given · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Red Moon Rising:** Both frenzy rows 35 → 43% (+8%): every element-less hit the caster lands in the two rounds after each cast, basic attacks and weapons included, is amplified, and with both windows up the rows compound to about ×2.04 (×1.82 at base). Moonbound Vigor is the only legal fourth purchase (Frenzy Assault heals 420 HP).
- **Undying Hunger:** Frenzy Assault's Heal 40 → 50 (+10%, 500 HP on the following round) with both frenzy rows at 40% (Undying Hunger +3%, The Beast Within +2%), so each cast mends and still leaves a frenzy. The Beast Within is the only legal fourth purchase; against the Frenzy build it trades 3% Increase Damage Given for 80 HP per cast.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Frenzy | Regeneration |
|---|---:|---|---|---:|---:|---:|
| Moonlit Fury | 0 | wound (unsupported) | enemy | 30% | 30% | 30% |
| Moonlit Fury | 1 | cleanseprevent (unsupported) | enemy | 100 | 100 | 100 |
| Moonlit Fury | 2 | Damage | enemy | 40 | 40 | 40 |
| Frenzy Assault | 0 | Increase Damage Given | self | 35% | 43% (+8) | 40% (+5) |
| Frenzy Assault | 1 | Heal | self | 40 | 42 (+2) | 50 (+10) |
| Feral Wrath | 0 | Damage | enemy | 50 | 50 | 50 |
| Feral Wrath | 1 | move (unsupported) | self | 1 | 1 | 1 |
| Feral Wrath | 2 | Increase Damage Given | self | 35% | 43% (+8) | 40% (+5) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 3, 3: 4, 4: 3
- Full-budget allocations: 3; numerically non-dominated (per-tag totals): 2; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +10% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Red Moon Rising: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Undying Hunger: +10% Heal (2 + 3 + 5; on band)
- Supported rows in kit: 5 (DMG 2, HEAL 1, IDG 2)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: The Beast Within, Moonbound Vigor, Lick the Wound, Undying Hunger (raw +15, row-weighted 20)
- Lowest row-weighted node: Moonbound Vigor (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (The Beast Within), 06 (Moonbound Vigor) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Moonlit Fury 40 (Normal), Feral Wrath 50 (Nuke)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Red Moon Rising | +8% IDG | Moonbound Vigor *(highest diagnostic)* | +8% IDG, +2% HEAL | 18 |
| Undying Hunger | +3% IDG, +10% HEAL | The Beast Within *(highest diagnostic)* | +5% IDG, +10% HEAL | 20 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | The Beast Within, Blood on the Wind, Red Moon Rising, Moonbound Vigor | +8% IDG, +2% HEAL |
| 2 | The Beast Within, Blood on the Wind, Moonbound Vigor, Lick the Wound | +4% IDG, +5% HEAL |
| 3 | The Beast Within, Moonbound Vigor, Lick the Wound, Undying Hunger | +5% IDG, +10% HEAL |

## Design notes

- Structure: two 3-node chains, The Beast Within → Blood on the Wind → Red Moon Rising (Increase Damage Given +2/+2/+4%) and Moonbound Vigor → Lick the Wound → Undying Hunger (Heal +2/+3/+5%, with +3% Increase Damage Given on the capstone). Owning both Advanced Arts costs 6 BP, so a build holds one. Draft 4's Damage route (Gnashing Fangs → Jaws of the Alpha) is removed.
- Damage: Draft 4's +5 route lifted Moonlit Fury 40 → 45 (a full tier) and Feral Wrath 50 → 55 (past the Nuke tier), and Gnashing Fangs alone put Feral Wrath at 52 as Red Moon Rising's fourth purchase. With no flat Damage both attacks stay at 40 and 50; the frenzy rows and the bloodline's Taijutsu Increase Damage Given passive still multiply them.
- Frenzy magnitude: each 35% row multiplies every element-less hit for the two rounds after its cast (Frenzy Assault's Taijutsu filter is not binding on an element-less row), and the two compound when both are up. Red Moon Rising's route is held at +8% rather than the +10% guardrail: ×1.43 × 1.43 ≈ ×2.04 against ×1.82 at base (+12% in a shared window, +6% in a single one); +10% would give ×2.10.
- Delivery: all three jutsu have cooldown 7. Frenzy Assault is a 40 AP self cast (Increase Damage Given 2 rounds; static Heal rounds 1 = one tick on the following round at 10 HP per heal power). Feral Wrath is a 60 AP ground circle whose Increase Damage Given row is SELF, realized on the caster at cast. Neither buff helps the round it is cast, Feral Wrath's own strike included (§3b); both windows coincide only when the two are cast in the same round (100 AP).
- Allocations: three legal full builds, each holding both Foundations: Frenzy (01, 04, 05, 06: +8% Increase Damage Given, +2% Heal), Regeneration (01, 06, 07, 08: +5% Increase Damage Given, +10% Heal) and the no-capstone hybrid (01, 04, 06, 07: +4%, +5%), which Regeneration dominates. Row weight ranks Regeneration first (20 against 18), but a Heal point here is 10 HP once per 7 rounds, so Frenzy is the stronger build in play. Maxima over every legal allocation: Increase Damage Given +8%, Heal +10%, no Damage.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Lycanthropy' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision, and all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Regeneration value: static Heal is 10 HP per point, so Undying Hunger's route adds 100 HP once per 7 rounds (400 → 500) and the Regeneration build gives up 3% Increase Damage Given against Frenzy for 80 HP more per cast. The +3% frenzy rider is what keeps it a choice; a larger rider would blur it into a second frenzy route.
- Frenzy breadth: both rows reach basic attacks, weapons and element-less normal jutsu as well as the kit, and the bloodline's Taijutsu Increase Damage Given passive multiplies last; extra damage also feeds the 10% lifesteal passive (shared 60% leech budget). Realized value depends on what lands in the windows; not simulated.
- Damage is a supported tag the tree leaves unamplified. A raw-strike route on the Blood-Enchanted Eyes / Shakunetsu Sakura pattern (+2 Damage payoff) would lift Moonlit Fury 40 → 42 and Feral Wrath 50 → 52, above the Nuke tier, and would need a third chain and an above-nuke rationale.
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

