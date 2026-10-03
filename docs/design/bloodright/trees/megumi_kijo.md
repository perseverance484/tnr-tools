# Megumi Kijo — Hearth of the Hag

**Bloodline:** Megumi Kijo (BR-045, rank B, `tBhjGw6fPVKhAgdVElIzW`) · **Revision:** Draft 2 / Megumi Kijo classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Megumi Kijo (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Genjutsu damage — Damage on Phantom Realm Oblivion and Onibaba's Laughter (2 rows) · secondary Control — Decrease Damage Given on Phantom Realm Oblivion (1 row) · tertiary Sustain — Heal on Onibaba's Laughter and Increase Heal on Kijo's Benevolence (1 row each).

Two of the five supported rows are Genjutsu damage (Phantom Realm Oblivion 40 single target, Onibaba's Laughter 45 per enemy in a radius-1 circle, both 60 AP, cooldown 7), and the bloodline's own Genjutsu Increase Damage Given passive multiplies them, so damage is primary. The Control trait lives in one row: Phantom Realm Oblivion's 30% Decrease Damage Given on one enemy for 2 rounds, which is also the kit's only mitigation lever because it carries no Decrease Damage Taken and the bloodline has a standing 10% Increase Damage Taken passive. Sustain is real but thin: Laughter's Heal is one 400 HP tick on the following round and Kijo's Benevolence's 30% Increase Heal is a 2-round ground field the caster steps into. Absorb and move on Benevolence are unsupported; no Afterburn, Lifesteal, Reflect, IDG or IDT row exists, and none is invented.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on five rows (Damage x2, Decrease Damage Given x1, Increase Heal x1, Heal x1). The enemy-facing root (Hagmother's Welcome) forks into a damage route and a suppression route; the self-facing root (Mountain Hag's Mercy) is a single Foundation → Hidden → Advanced chain. A fourth route would have to split Heal from Increase Heal into two capstones on one row each: Heal is one static row that ticks once per 7 rounds (10 HP per +1%), and an Increase Heal-led second route would duplicate Nursed by Demon Hands, so the kit's thin sustain stays one shared route. A Damage or Decrease Damage Given Hidden Art under Mercy is structurally legal (any two Advanced Arts would still cost 5 BP or more) but would duplicate the Welcome routes on the same rows, so it is declined by choice. Three distinct complete builds exist (Burst, Suppression, Sustain); Burst and Suppression each have two fourth-purchase choices, and Sustain's fourth purchase is always Hagmother's Welcome (01,06,07,08 is legal and non-dominated), so Hagmother's Welcome is a universal node (in all 8 legal 4-BP builds) because Mercy roots a single 3-node chain.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Megumi Kijo-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hagmother's Welcome | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Phantom Realm Oblivion / 1 |
| 02 | Teeth Behind the Smile | Hidden Art | Hagmother's Welcome | +2 Damage (damage) | Onibaba's Laughter, Phantom Realm Oblivion / 2 |
| 03 | Appetite of Oblivion | Advanced Art | Teeth Behind the Smile | +3 Damage (damage) | Onibaba's Laughter, Phantom Realm Oblivion / 2 |
| 04 | Numbing Lullaby | Hidden Art | Hagmother's Welcome | +3% Decrease Damage Given (enemy debuff) | Phantom Realm Oblivion / 1 |
| 05 | Cradle of the Kijo | Advanced Art | Numbing Lullaby | +5% Decrease Damage Given (enemy debuff); +2% Heal (self buff) | Onibaba's Laughter, Phantom Realm Oblivion / 2 |
| 06 | Mountain Hag's Mercy | Foundation | None | +2% Heal (self buff); +2% Increase Heal (self buff) | Kijo's Benevolence, Onibaba's Laughter / 2 |
| 07 | Nursed by Demon Hands | Hidden Art | Mountain Hag's Mercy | +3% Increase Heal (self buff) | Kijo's Benevolence / 1 |
| 08 | Laughter That Mends | Advanced Art | Nursed by Demon Hands | +3% Heal (self buff); +3% Increase Heal (self buff) | Kijo's Benevolence, Onibaba's Laughter / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hagmother's Welcome** — Come in, traveller. The mountain is cold, and the hag's hearth is always lit. Phantom Realm Oblivion suppression 30 → 32% (one target, 2 rounds, every non-pierce hit that enemy deals). 1 row.
- **Teeth Behind the Smile** — Guests who look too long at the smile see the teeth behind it. Both Genjutsu Damage rows: Phantom Realm Oblivion 40 → 42, Onibaba's Laughter 45 → 47 EP per enemy in its circle. 60 AP, CD 7.
- **Appetite of Oblivion** — What the phantom realm swallows, it does not give back. Same two rows; route total +5 Damage (Phantom Realm 40 → 45, Laughter 45 → 50 EP), then the Genjutsu damage passive multiplies them.
- **Numbing Lullaby** — A song older than the mountain, and the arm that lifts the blade grows heavy. Phantom Realm Oblivion Decrease Damage Given only (single target, 2 rounds, 60 AP, CD 7): 32 → 35% with Hagmother's Welcome.
- **Cradle of the Kijo** — Sleep, little one. She will decide in the morning whether you were a guest or a meal. Route total +10%: Phantom Realm suppression 30 → 40%; Onibaba's Laughter Heal 40 → 42 (420 HP; 440 with Mercy).
- **Mountain Hag's Mercy** — The same hands that cook the traveller also raise the orphan. Onibaba's Laughter Heal 40 → 42 (400 → 420 HP next round, self); Kijo's Benevolence Increase Heal 30 → 32% for you and allies in its field. CD 7.
- **Nursed by Demon Hands** — Clawed fingers, surprisingly gentle, pressing the wound closed. Kijo's Benevolence Increase Heal only (ground field, 2 rounds, reaches you from the round after you step in): 32 → 35% with Mercy.
- **Laughter That Mends** — Her laughter shakes the valley, and every cut on her closes as she cackles. Route total +5% Heal: Onibaba's Laughter 40 → 45 with Mercy (450 HP per tick); Kijo's Benevolence Increase Heal 35 → 38% for you and allies in the field.

## Complete four-purchase examples

| Build | Purchases | DMG | DDG | IH | HEAL |
|---|---|---:|---:|---:|---:|
| Appetite of Oblivion (Burst) | Hagmother's Welcome, Teeth Behind the Smile, Appetite of Oblivion, Mountain Hag's Mercy | +5 | +2% | +2% | +2% |
| Cradle of the Kijo (Suppression) | Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy | — | +10% | +2% | +4% |
| Laughter That Mends (Sustain) | Hagmother's Welcome, Mountain Hag's Mercy, Nursed by Demon Hands, Laughter That Mends | — | +2% | +8% | +5% |

Abbreviations: DMG = Damage · DDG = Decrease Damage Given · IH = Increase Heal · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Appetite of Oblivion:** +5 Damage on both Genjutsu attacks (Phantom Realm Oblivion 40 → 45, Onibaba's Laughter 45 → 50 EP per enemy in its circle), before the bloodline's Genjutsu damage passive multiplies them, with Hagmother's Welcome's 32% suppression riding the Phantom Realm hit. Mountain Hag's Mercy is the fourth purchase so Laughter's tick heals 420 HP and Benevolence's field gives 32% Increase Heal; Numbing Lullaby (suppression 35%) is the all-offence alternative.
- **Cradle of the Kijo:** The control build: Phantom Realm Oblivion's Decrease Damage Given reaches 40% for 2 rounds on one enemy (30 → 40%), cutting every non-pierce hit that enemy deals to the caster or allies, and the capstone's +2% Heal with Mercy makes Laughter's tick 440 HP so the caster outlasts the exchange. Teeth Behind the Smile (attacks 42/47 EP, Laughter 420 HP, no field bonus) is the sharper alternative fourth purchase.
- **Laughter That Mends:** Sustain as the centrepiece: Onibaba's Laughter heals 450 HP on the following round (+5% Heal) and Kijo's Benevolence's field gives 38% Increase Heal for 2 rounds to the caster and allies standing in it, which also lifts Benevolence's own 35% absorb and any main-tree or item healing in the window. Hagmother's Welcome is the only legal fourth purchase (suppression 32%); the Mercy chain has no side branch.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Suppression | Sustain |
|---|---:|---|---|---:|---:|---:|---:|
| Phantom Realm Oblivion | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Phantom Realm Oblivion | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 32% (+2) |
| Onibaba's Laughter | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 |
| Onibaba's Laughter | 1 | Heal | self | 40 | 42 (+2) | 44 (+4) | 45 (+5) |
| Kijo's Benevolence | 0 | absorb (unsupported) | self | 35% | 35% | 35% | 35% |
| Kijo's Benevolence | 1 | Increase Heal | self | 30% | 32% (+2) | 32% (+2) | 38% (+8) |
| Kijo's Benevolence | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Decrease Damage Given, +8% Increase Heal, +5% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Appetite of Oblivion: +5 Damage (0 + 2 + 3; on band)
  - Route Cradle of the Kijo: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Laughter That Mends: +5% Heal (2 + 0 + 3; on band)
- Supported rows in kit: 5 (DMG 2, DDG 1, HEAL 1, IH 1)
- Strongest full build by row-weighted total: Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy (raw +16, row-weighted 16)
- Lowest row-weighted node: Hagmother's Welcome (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Hagmother's Welcome) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hagmother's Welcome, Teeth Behind the Smile, Appetite of Oblivion, Numbing Lullaby | +5 Damage, +5% DDG |
| 2 | Hagmother's Welcome, Teeth Behind the Smile, Appetite of Oblivion, Mountain Hag's Mercy | +5 Damage, +2% DDG, +2% IH, +2% HEAL |
| 3 | Hagmother's Welcome, Teeth Behind the Smile, Numbing Lullaby, Cradle of the Kijo | +2 Damage, +10% DDG, +2% HEAL |
| 4 | Hagmother's Welcome, Teeth Behind the Smile, Numbing Lullaby, Mountain Hag's Mercy | +2 Damage, +5% DDG, +2% IH, +2% HEAL |
| 5 | Hagmother's Welcome, Teeth Behind the Smile, Mountain Hag's Mercy, Nursed by Demon Hands | +2 Damage, +2% DDG, +5% IH, +2% HEAL |
| 6 | Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy | +10% DDG, +2% IH, +4% HEAL |
| 7 | Hagmother's Welcome, Numbing Lullaby, Mountain Hag's Mercy, Nursed by Demon Hands | +5% DDG, +5% IH, +2% HEAL |
| 8 | Hagmother's Welcome, Mountain Hag's Mercy, Nursed by Demon Hands, Laughter That Mends | +2% DDG, +8% IH, +5% HEAL |

## Design notes

- Node split: the two roots are the hag's two faces. Hagmother's Welcome (enemy side) raises Phantom Realm Oblivion's suppression, then forks into Teeth Behind the Smile → Appetite of Oblivion (damage) and Numbing Lullaby → Cradle of the Kijo (suppression). Mountain Hag's Mercy (self side) raises Laughter's Heal and Benevolence's Increase Heal in one chain through Nursed by Demon Hands → Laughter That Mends. 2/3/3; capstones are 3 BP deep; any two cost 5 or 6 BP.
- Recalibration (RUL-2026-10-03-005): Hagmother's Welcome's +1 Damage is removed, so the Damage route is the default +5 (Teeth Behind the Smile +2, Appetite of Oblivion +3; Phantom Realm 40 → 45, Laughter 45 → 50 EP); no other value changes. Suppression is the single-row +10% route (2/3/5; 30 → 40%). Sustain is a +5% Heal route (Mercy +2%, Laughter That Mends +3%; 400 → 450 HP) with Increase Heal glue at 2/3/3 (+8%, 38%). Cradle's secondary is +2% Heal rather than +3% Increase Heal so that 01,04,06,07 is not dominated by 01,04,05,06. Maxima over every legal allocation: Damage +5, DDG +10%, Increase Heal +8%, Heal +5%.
- Passives and main tree: the bloodline's Increase Damage Given passive (20% + 0.15/level, Genjutsu filter, no element) is bloodline-sourced and multiplicative, and its stat filter does not bind on element-less hits (SOURCE_MECHANICS §3), so it multiplies the enhanced Phantom Realm and Laughter rows. Its 10% Increase Damage Taken passive is a standing self-weakness; the kit has no Decrease Damage Taken, so the Lullaby route (one enemy's non-pierce hits ×0.60 for 2 rounds) is the only mitigation lever.
- Delivery and uptime: all cooldown 7. Phantom Realm Oblivion (single target, 60 AP) delivers hit and 2-round suppression at once. Onibaba's Laughter (radius-1 circle, 60 AP) hits each enemy inside; its SELF Heal (rounds 1) ticks once next round. Kijo's Benevolence (40 AP, empty-ground spiral) lays Increase Heal and absorb ground effects on every tile within 4 of the caster, then its move row moves the caster to the clicked tile, so it reaches them from the next round while they stand in it.
- Fourth purchases: Burst → Mountain Hag's Mercy (Laughter 420 HP, field 32%) or Numbing Lullaby (suppression 35%); Suppression → Mercy (field 32%, Laughter 440 HP) or Teeth Behind the Smile (attacks 42/47 EP); Sustain → Hagmother's Welcome only (suppression 32%). No-Advanced hybrids: 01,02,04,06 (Damage +2, DDG +5%), 01,02,06,07 (Damage +2, IH +5%), 01,04,06,07 (DDG +5%, IH +5%). All eight full allocations are non-dominated and every node appears in at least one; by row weight Burst and Suppression tie at 16 and Sustain is 15.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Megumi Kijo' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Suppression at 40%: Phantom Realm Oblivion's DDG row has no element and lists all four stat types, so for 2 rounds it reduces every non-pierce hit the debuffed enemy deals to anyone (caster, allies, summons), broader than one row suggests. It is one target per 7-round cooldown, debuff-prevent gated, and compounds with other DDG sources, each applied in turn as ×(1 − p/100) (BATTLE_TAG_STACKING on at the pin).
- Pierce: Decrease Damage Given does not touch pierce hits, so the Suppression build is blind to pierce damage; the Damage route (raw EP) and the Heal values are unaffected. Percentage caps are not approached (highest value 40%).
- Increase Heal delivery: Benevolence's Increase Heal is a ground effect on every tile within 4 of the caster, re-applied each round to whoever stands there; the caster gets it only from the round after the cast (the move row relocates them last) and only while in the field. Allies in the field get it too (the dossier says self), so the Mercy chain lifts allied heals, lifesteal, vamp and absorb.
- Increase Heal reach: adjustHealGiven adds the percentage to heal_hp, lifesteal_hp, vampRatio and absorb_hp for the holder, so +8% also raises Benevolence's own unsupported 35% absorb and other healing in the window (max 38%). It ignores new or cast-this-round buffs; whether a ground-applied Increase Heal adjusts a same-round Laughter tick was not verified (621 vs 450 HP; baselines 520 / 400).
- Heal timing: Onibaba's Laughter's Heal is target SELF with rounds 1, so it is one tick on the following round (static ×10 HP per point), deduplicated by stack key however many enemies the circle hits, and blocked by healprevent on the caster. +5% Heal is +50 HP per cast, once per 7-round cooldown; it is the kit's whole raw sustain.
- Damage is formula-calculated and scaled by the Genjutsu damage-given passive, so +5 EP is not a linear +5; Laughter's +5 applies per enemy in its radius-1 circle (friendly fire ENEMIES, no ally hazard). The 10% damage-taken passive stays, and single-target suppression leaves it open against a second enemy. Skill-tree and bloodline effects are skipped in ranked modes. No combat simulation.
- Value decisions (user-owned): Decrease Damage Given +10% is the single-row 2/3/5 route; Heal +5% and Increase Heal +8% keep the self chain modest. Absorb and move on Kijo's Benevolence are unsupported and get no direct potency; only the Increase Heal interaction touches absorb indirectly.

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

