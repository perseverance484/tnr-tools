# Megumi Kijo — Hearth of the Hag

**Bloodline:** Megumi Kijo (BR-045, rank B, `tBhjGw6fPVKhAgdVElIzW`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Megumi Kijo classification / forked tree · **Classification:** Megumi Kijo (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Sustain from Mountain Hag's Mercy — Heal on Onibaba's Laughter (400 → 420 HP) and Increase Heal on Kijo's Benevolence (1 row each); its single chain raises Benevolence's healing field to 40% · secondary Control — Decrease Damage Given on Phantom Realm Oblivion (1 row), 30 → 40% on the Suppression route · tertiary Damage — +2 on the two Genjutsu attacks (Phantom Realm Oblivion 40 → 42, Onibaba's Laughter 45 → 47) on the steady-edge route only, +1 at Teeth Behind the Smile and +1 at Appetite of Oblivion.

Five supported rows on three cooldown-7 jutsu. Hagmother's Welcome answers "How do I deal with my guest: lull it harmless, or eat it?": Numbing Lullaby and Cradle of the Kijo take Phantom Realm Oblivion's single Decrease Damage Given row 30 → 40% (Suppression), the kit's only supported damage-reduction row against its standing 10% Increase Damage Taken passive, and Teeth Behind the Smile and Appetite of Oblivion add +1 Damage each to both Genjutsu attacks (steady edge, no tier crossed). Mountain Hag's Mercy answers "How do I mend the hag and everyone at her hearth?": Nursed by Demon Hands and The Ever-Lit Hearth raise Benevolence's Increase Heal field to 40% for the caster and allies standing in it. Benevolence's 35% absorb also mitigates but is unsupported, as is its move row. No IDG, IDT, Lifesteal, Reflect or Afterburn row exists, and none is invented.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hagmother's Welcome | Foundation | How do I deal with my guest: lull it harmless, or eat it? |
| Mountain Hag's Mercy | Foundation | How do I mend the hag and everyone at her hearth? |
| Appetite of Oblivion | Advanced Art | steady edge: +1 Damage commit then +1 on both Genjutsu attacks, every cast (40 → 42, 45 → 47; no tier crossed) |
| Cradle of the Kijo | Advanced Art | suppression |
| The Ever-Lit Hearth | Advanced Art | healing field for the caster and allies |

**Director review recommended:** Roster questions: DQ-D (Teeth Behind the Smile carries +1 Damage as the commit before Appetite of Oblivion's +1; route +2, Phantom Realm Oblivion 40 → 42, Onibaba's Laughter 45 → 47).

- Concern: Appetite of Oblivion is the leanest payoff (+2 EP on two cooldown-7 attacks). +2 is the roster default for 40/45 EP rows (Arashima 45 → 47) and the batch ceiling for flat Damage, so nothing larger is proposed.
- Concern: Teeth Behind the Smile is a +1 Damage commit, not a setup (DQ-D): no percentage setup exists that neither twins Numbing Lullaby nor is Heal glue. As a result Appetite + Numbing Lullaby (01,02,03,04) and Cradle + Teeth (01,02,04,05) share three nodes and differ only in the capstone: +1 Damage (Oblivion 41 → 42, Laughter 46 → 47) against +5% Decrease Damage Given (35 → 40%).
- Concern: Cradle of the Kijo is single-tag (+5% Decrease Damage Given) where the director anchors' suppression capstones carry a rider; the kit's candidates are Heal (glue on a once-per-7-rounds tick), Increase Heal (the Hearth's identity) and Damage (an offensive rider), so none is added.
- Concern: The Ever-Lit Hearth's 40% Increase Heal reaches allies in the field and Benevolence's own absorb, and lifts a Laughter tick taken in the field to 588 HP; it is positional and absent in the field's cast round (risks).
- Concern: The 'Megumi Kijo' classification extension is a director/engine decision; off-kit coverage is unverified.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on five rows (Damage x2, Decrease Damage Given x1, Heal x1, Increase Heal x1). The enemy-facing Hagmother's Welcome forks into Suppression and the steady-edge Damage chain; the self-facing Mountain Hag's Mercy is a single chain onto Benevolence's field. A fourth capstone would be filler: Heal is one static tick (+10 HP per +1% once per 7 rounds), and a second Decrease Damage Given or Increase Heal route would repeat Suppression or the Hearth on the same row. Hagmother's Welcome is a universal node (in all 8 legal 4-BP builds) because Mercy roots a single 3-node chain.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Megumi Kijo-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hagmother's Welcome | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Phantom Realm Oblivion / 1 |
| 02 | Teeth Behind the Smile | Hidden Art | Hagmother's Welcome | +1 Damage (damage) | Onibaba's Laughter, Phantom Realm Oblivion / 2 |
| 03 | Appetite of Oblivion | Advanced Art | Teeth Behind the Smile | +1 Damage (damage) | Onibaba's Laughter, Phantom Realm Oblivion / 2 |
| 04 | Numbing Lullaby | Hidden Art | Hagmother's Welcome | +3% Decrease Damage Given (enemy debuff) | Phantom Realm Oblivion / 1 |
| 05 | Cradle of the Kijo | Advanced Art | Numbing Lullaby | +5% Decrease Damage Given (enemy debuff) | Phantom Realm Oblivion / 1 |
| 06 | Mountain Hag's Mercy | Foundation | None | +2% Heal (self buff); +2% Increase Heal (self buff) | Kijo's Benevolence, Onibaba's Laughter / 2 |
| 07 | Nursed by Demon Hands | Hidden Art | Mountain Hag's Mercy | +3% Increase Heal (self buff) | Kijo's Benevolence / 1 |
| 08 | The Ever-Lit Hearth | Advanced Art | Nursed by Demon Hands | +5% Increase Heal (self buff) | Kijo's Benevolence / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hagmother's Welcome** — Come in, traveller. The mountain is cold, and the hag's hearth is always lit. Phantom Realm Oblivion suppression 30 → 32% (one enemy, 2 rounds, every non-pierce hit it deals).
- **Teeth Behind the Smile** — Guests who look too long at the smile see the teeth behind it. Steady-edge commit: Phantom Realm Oblivion 40 → 41 and Onibaba's Laughter 45 → 46 EP per enemy in its circle, every cast.
- **Appetite of Oblivion** — What the phantom realm swallows, it does not give back. Steady edge: Phantom Realm Oblivion 40 → 42 and Onibaba's Laughter 45 → 47 EP per enemy in its circle on the full route, every cast (no tier crossed).
- **Numbing Lullaby** — A song older than the mountain, and the arm that lifts the blade grows heavy. Phantom Realm Oblivion suppression 32 → 35% with Hagmother's Welcome.
- **Cradle of the Kijo** — Sleep, little one. She will decide in the morning whether you were a guest or a meal. Suppression: Phantom Realm Oblivion Decrease Damage Given 30 → 40% on the full route, so that enemy's non-pierce hits are ×0.60 for 2 rounds.
- **Mountain Hag's Mercy** — The same hands that cook the traveller also raise the orphan. Onibaba's Laughter Heal 40 → 42 (420 HP the round after the cast, self); Kijo's Benevolence Increase Heal 30 → 32% for you and allies in its field.
- **Nursed by Demon Hands** — Clawed fingers, surprisingly gentle, pressing the wound closed. Kijo's Benevolence Increase Heal 32 → 35% with Mountain Hag's Mercy (ground field, 2 rounds, reaches you from the round after the cast).
- **The Ever-Lit Hearth** — Sit closer to the fire, little ones. Whatever she means for you tomorrow, tonight every wound closes. Healing field: Kijo's Benevolence Increase Heal 30 → 40% on the full route for you and allies standing in it, lifting their heals, lifesteal, vamp and Benevolence's own 35% absorb.

## Complete four-purchase examples

| Build | Purchases | DMG | DDG | IH | HEAL |
|---|---|---:|---:|---:|---:|
| Appetite of Oblivion (Steady edge) | Hagmother's Welcome, Teeth Behind the Smile, Appetite of Oblivion, Numbing Lullaby | +2 | +5% | — | — |
| Cradle of the Kijo (Suppression) | Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy | — | +10% | +2% | +2% |
| The Ever-Lit Hearth (Healing field) | Mountain Hag's Mercy, Nursed by Demon Hands, The Ever-Lit Hearth, Hagmother's Welcome | — | +2% | +10% | +2% |

Abbreviations: DMG = Damage · DDG = Decrease Damage Given · IH = Increase Heal · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Appetite of Oblivion:** Phantom Realm Oblivion 40 → 42 and Onibaba's Laughter 45 → 47 EP per enemy, every cast, with Numbing Lullaby as the fourth purchase so the same Oblivion cast suppresses at 35%. Mountain Hag's Mercy (Laughter 420 HP, field 32%) is the alternative fourth.
- **Cradle of the Kijo:** Phantom Realm Oblivion's Decrease Damage Given 30 → 40% on one enemy for 2 rounds, cutting every non-pierce hit it deals. Mountain Hag's Mercy is the fourth purchase (Laughter 420 HP, field 32%); Teeth Behind the Smile (+1 Damage: Oblivion 41, Laughter 46) is the alternative.
- **The Ever-Lit Hearth:** Kijo's Benevolence Increase Heal 30 → 40% for the caster and allies in the field, with Laughter's tick at 420 HP (588 HP when it lands in a live field). Hagmother's Welcome (suppression 32%) is the only legal fourth purchase.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Steady edge | Suppression | Healing field |
|---|---:|---|---|---:|---:|---:|---:|
| Phantom Realm Oblivion | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 |
| Phantom Realm Oblivion | 1 | Decrease Damage Given | enemy | 30% | 35% (+5) | 40% (+10) | 32% (+2) |
| Onibaba's Laughter | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 |
| Onibaba's Laughter | 1 | Heal | self | 40 | 40 | 42 (+2) | 42 (+2) |
| Kijo's Benevolence | 0 | absorb (unsupported) | self | 35% | 35% | 35% | 35% |
| Kijo's Benevolence | 1 | Increase Heal | self | 30% | 30% | 32% (+2) | 40% (+10) |
| Kijo's Benevolence | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Decrease Damage Given, +10% Increase Heal, +2% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Appetite of Oblivion: +2 Damage (0 + 1 + 1; off band)
  - Route Cradle of the Kijo: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route The Ever-Lit Hearth: +10% Increase Heal (2 + 3 + 5; on band)
- Supported rows in kit: 5 (DMG 2, DDG 1, HEAL 1, IH 1)
- Strongest full build by row-weighted total: Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy (raw +14, row-weighted 14)
- Lowest row-weighted node: Hagmother's Welcome (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Hagmother's Welcome) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +1 Damage | +2 Damage |
|---|---:|---|---|---|
| Phantom Realm Oblivion | 0 | 40 (Normal) | 41 (Normal) | 42 (Normal) |
| Onibaba's Laughter | 0 | 45 (High) | 46 (High) | 47 (High) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Appetite of Oblivion | +2 Damage, +2% DDG | Numbing Lullaby | +2 Damage, +5% DDG | 9 |
| Appetite of Oblivion | +2 Damage, +2% DDG | Mountain Hag's Mercy *(highest diagnostic)* | +2 Damage, +2% DDG, +2% IH, +2% HEAL | 10 |
| Cradle of the Kijo | +10% DDG | Teeth Behind the Smile | +1 Damage, +10% DDG | 12 |
| Cradle of the Kijo | +10% DDG | Mountain Hag's Mercy *(highest diagnostic)* | +10% DDG, +2% IH, +2% HEAL | 14 |
| The Ever-Lit Hearth | +10% IH, +2% HEAL | Hagmother's Welcome *(highest diagnostic)* | +2% DDG, +10% IH, +2% HEAL | 14 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hagmother's Welcome, Teeth Behind the Smile, Appetite of Oblivion, Numbing Lullaby | +2 Damage, +5% DDG |
| 2 | Hagmother's Welcome, Teeth Behind the Smile, Appetite of Oblivion, Mountain Hag's Mercy | +2 Damage, +2% DDG, +2% IH, +2% HEAL |
| 3 | Hagmother's Welcome, Teeth Behind the Smile, Numbing Lullaby, Cradle of the Kijo | +1 Damage, +10% DDG |
| 4 | Hagmother's Welcome, Teeth Behind the Smile, Numbing Lullaby, Mountain Hag's Mercy | +1 Damage, +5% DDG, +2% IH, +2% HEAL |
| 5 | Hagmother's Welcome, Teeth Behind the Smile, Mountain Hag's Mercy, Nursed by Demon Hands | +1 Damage, +2% DDG, +5% IH, +2% HEAL |
| 6 | Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy | +10% DDG, +2% IH, +2% HEAL |
| 7 | Hagmother's Welcome, Numbing Lullaby, Mountain Hag's Mercy, Nursed by Demon Hands | +5% DDG, +5% IH, +2% HEAL |
| 8 | Hagmother's Welcome, Mountain Hag's Mercy, Nursed by Demon Hands, The Ever-Lit Hearth | +2% DDG, +10% IH, +2% HEAL |

## Design notes

- Rewire (2026-10-04 batch, final pass): Teeth Behind the Smile returns under Hagmother's Welcome, as in the pre-batch tree, as a +1 Damage commit, and Appetite of Oblivion drops to +1 (route +2: Phantom Realm Oblivion 40 → 42, Onibaba's Laughter 45 → 47; the pre-batch +2/+3 lifted them 40 → 45 and 45 → 50). The earlier pass hung the chain under Mountain Hag's Mercy behind a +3% Heal step (+30 HP once per 7-round cast) that gated the Damage without setting it up, and Mercy's sustain sentence did not cover a Damage child. Under Welcome both children act on the guest (lull it or eat it), the dossier's two traits, Control and Sustained Damage.
- Why a +1 Damage commit (steady edge, not burst): the kit has no Increase Damage Given or Taken row to set Damage up, a Decrease Damage Given step would twin Numbing Lullaby (a legal fourth for this route), and Heal or Increase Heal would be glue. No row is above 45, so no Damage result reaches the Nuke tier.
- Values: Suppression stays 2/3/5 (30 → 40%) without the pre-batch Cradle +2% Heal rider. The Ever-Lit Hearth is +5% Increase Heal (route 30 → 40%), so each capstone carries one effect and Heal is Mountain Hag's Mercy's +2% alone. Maxima over every legal allocation: Damage +2, Decrease Damage Given +10%, Increase Heal +10%, Heal +2%.
- Delivery: all cooldown 7. Phantom Realm Oblivion (single target, 60 AP) lands its hit and 2-round suppression together. Onibaba's Laughter (radius-1 circle, 60 AP) hits each enemy inside; its self Heal ticks once the next round. Kijo's Benevolence (40 AP) lays a FRIENDLY Increase Heal field within 4 tiles, then moves the caster, who gets it from the next round while standing in it. The bloodline's Genjutsu Increase Damage Given passive multiplies both attacks last.
- Fourth purchases: Appetite → Numbing Lullaby (suppression 35%) or Mountain Hag's Mercy (Laughter 420 HP, field 32%); Cradle → Mercy or Teeth Behind the Smile (+1 Damage: 41 / 46); Hearth → Hagmother's Welcome only (suppression 32%). Only Appetite's route reaches +2 Damage.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Megumi Kijo' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Suppression at 40%: Phantom Realm Oblivion's Decrease Damage Given row has no element and lists all four stat types, so for 2 rounds it reduces every non-pierce hit the debuffed enemy deals to anyone. It is one target per 7-round cooldown, debuff-prevent gated, and compounds with other reductions as ×(1 − p/100) in turn. It does not touch pierce.
- Increase Heal: Benevolence's field is a FRIENDLY ground effect re-applied each round to whoever stands in it, allies included and never enemies (actions.ts 1006–1016, process.ts 321–340; the dossier says self), and adjustHealGiven raises heal_hp, lifesteal_hp, vampRatio and absorb_hp for its holder (tags.ts 1110–1195), so 40% also lifts Benevolence's own 35% absorb and any healing in the window. A Laughter tick landing while the caster stands in a live field is raised too: the ground-derived buff copies the field's cleared isNew/castThisRound (process.ts 301, 333–339) and heal adjusters run after heals (process.ts 440, 600), so the tick is 420 × 1.40 = 588 HP on a Hearth build, and nothing in the field's cast round. Lifesteal and vamp raised there still share the 60% leech budget, which is applied to the adjusted values when consequences resolve (process.ts 733–766, 905–917).
- Heal timing: Laughter's Heal is one static tick on the following round (×10 HP per point), deduplicated however many enemies the circle hits and blocked by healprevent, so Mountain Hag's Mercy's +2% Heal is +20 HP per cast once per 7 rounds.
- Damage is formula-calculated and multiplied by the Genjutsu damage passive, so +2 EP is not a linear +2; Laughter's +2 applies per enemy in its circle (friendly fire ENEMIES, no ally hazard). The 10% damage-taken passive stays. Skill-tree and bloodline effects are skipped in ranked modes. No combat simulation.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Megumi Kijo-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

