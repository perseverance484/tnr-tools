# Kyuko-sei — Ash of Dying Stars

**Bloodline:** Kyuko-sei (BR-040, rank A, `Y10fxyLR39IBJ3ICkAdEp`) · **Revision:** Draft 2 / Dust classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Dust (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (Dust attacks on all four strikes) · secondary Increase Damage Taken (Temporal Erosion / Abysmal End exposure) with Increase Damage Given as glue · tertiary Decrease Damage Taken (Temporal Erosion guard) and Decrease Damage Given (Ethereal Particle Storm suppression).

Four of the ten supported rows are Dust damage (Temporal Erosion, Singularity and Resonance 40, Ethereal Particle Storm 50 at jutsu level 25), all 60 AP on cooldown 7, so the Burst trait is served by the Damage route. Increase Damage Taken reaches two rows that can stack on one target (Temporal Erosion single-target, Abysmal End area) and Increase Damage Given reaches two self buffs whose filters include the kit's own Ninjutsu Dust attacks, so exposure is the pressure route and amplify is the glue. The kit's only guard (Temporal Erosion Decrease Damage Taken 30%) and only suppression (Ethereal Particle Storm Decrease Damage Given 30%) are single rows riding on 60 AP attacks, so they carry the two control routes. There are no Afterburn, Lifesteal, Reflect or Heal rows and Mirror and Move are unsupported, so no sustain or burn route is invented. Potency reaches matching supported tags on all Dust jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dust jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Weight of Eons | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Abysmal End, Singularity, Temporal Erosion / 4 |
| 02 | Shattered Firmament | Hidden Art | Weight of Eons | +2 Damage (damage) | Ethereal Particle Storm, Resonance, Singularity, Temporal Erosion / 4 |
| 03 | Heat Death | Advanced Art | Shattered Firmament | +3 Damage (damage) | Ethereal Particle Storm, Resonance, Singularity, Temporal Erosion / 4 |
| 04 | Aeons Laid Bare | Hidden Art | Weight of Eons | +3% Increase Damage Taken (enemy debuff) | Abysmal End, Temporal Erosion / 2 |
| 05 | Collapse of Ages | Advanced Art | Aeons Laid Bare | +5% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Abysmal End, Singularity, Temporal Erosion / 4 |
| 06 | Hush of the Void | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Ethereal Particle Storm, Temporal Erosion / 2 |
| 07 | Dilated Moment | Hidden Art | Hush of the Void | +3% Decrease Damage Taken (self buff) | Temporal Erosion / 1 |
| 08 | Outlasting Eternity | Advanced Art | Dilated Moment | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Abysmal End, Singularity, Temporal Erosion / 3 |
| 09 | Dimming of Stars | Hidden Art | Hush of the Void | +3% Decrease Damage Given (enemy debuff) | Ethereal Particle Storm / 1 |
| 10 | All Returns to Dust | Advanced Art | Dimming of Stars | +5% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Abysmal End, Ethereal Particle Storm, Temporal Erosion / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Weight of Eons** — What the hollow star touches grows old before it can resist. Abysmal End and Singularity self amplify 35 → 37%; Temporal Erosion and Abysmal End exposure 35 → 37%. 4 rows, 2 rounds each.
- **Shattered Firmament** — The sky cracks, and dust that was once a star pours through. Temporal Erosion, Singularity and Resonance 40 → 42, Ethereal Particle Storm 50 → 52 EP. 4 Dust rows, all 60 AP, cooldown 7.
- **Heat Death** — Every fire goes out. Yours merely goes first. The same four Dust Damage rows; route total +5 Damage (Particle Storm 55, the other three 45 EP).
- **Aeons Laid Bare** — Armor is only time that has not yet passed. Temporal Erosion (single) and Abysmal End (area) exposure, 2 rounds: 35 → 40% with Weight of Eons; both can sit on one target.
- **Collapse of Ages** — Centuries fold into a single falling instant. Route total +10%: both exposure rows 35 → 45% (both apply on one target: ×1.45 × 1.45 ≈ ×2.10); both self amplify rows +3% (40% with Weight of Eons).
- **Hush of the Void** — Where the star once burned there is only quiet, and quiet does not bleed. Temporal Erosion self guard 30 → 32% and Ethereal Particle Storm suppression 30 → 32%. 2 single-target rows, 60 AP, 2 rounds.
- **Dilated Moment** — A heartbeat stretched until the blow arrives too late. Temporal Erosion Decrease Damage Taken only (single self row, 2 rounds per 60 AP cast): 35% with Hush of the Void.
- **Outlasting Eternity** — When the last light fails, you are still standing there. Route total +10%: Temporal Erosion guard 30 → 40%; Abysmal End and Singularity amplify +3% (38%, 40% with Weight of Eons).
- **Dimming of Stars** — One by one the enemy's fires gutter and go dark. Ethereal Particle Storm Decrease Damage Given only (single-target, 60 AP, 2 rounds): 35% with Hush of the Void.
- **All Returns to Dust** — Stars, mountains, names: the dust keeps none of them. Route total +10%: Particle Storm suppression 30 → 40%; Temporal Erosion and Abysmal End exposure +2% (37%, 39% with Weight of Eons).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT |
|---|---|---:|---:|---:|---:|---:|
| Heat Death (Burst) | Weight of Eons, Shattered Firmament, Heat Death, Hush of the Void | +5 | +2% | +2% | +2% | +2% |
| Collapse of Ages (Pressure) | Weight of Eons, Shattered Firmament, Aeons Laid Bare, Collapse of Ages | +2 | +5% | — | +10% | — |
| Outlasting Eternity (Fortress) | Weight of Eons, Hush of the Void, Dilated Moment, Outlasting Eternity | — | +5% | +2% | +2% | +10% |
| All Returns to Dust (Suppression) | Weight of Eons, Hush of the Void, Dimming of Stars, All Returns to Dust | — | +2% | +10% | +4% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Heat Death:** +5 Damage on all four Dust attacks (Ethereal Particle Storm 55; Temporal Erosion, Singularity and Resonance 45 EP) with Weight of Eons' amplify and exposure at 37%. Hush of the Void is the fourth purchase because it opens the control root (guard and suppression 32%) without competing for the damage rows; Aeons Laid Bare (exposure 40% on both rows) is the offensive alternative.
- **Collapse of Ages:** Exposure first: Temporal Erosion and Abysmal End Increase Damage Taken reach 45% each (both apply when they sit on one target, ×1.45 × 1.45 ≈ ×2.10) while both self amplify rows reach 40%. Shattered Firmament is the fourth purchase because the exposed target is then struck by the kit's own +2 attacks (42/42/42/52 EP); Hush of the Void is the defensive alternative.
- **Outlasting Eternity:** Temporal Erosion as the centrepiece: its guard reaches 40% and its exposure 37% from one 60 AP cast, both amplify rows reach 40%, and Particle Storm's suppression sits at 32%. Weight of Eons is the fourth purchase because it stacks Increase Damage Given to +5%; Dimming of Stars (suppression 35%) is the control alternative.
- **All Returns to Dust:** Ethereal Particle Storm as the control cast: a 50 EP Dust hit plus 40% Decrease Damage Given on its target, with both exposure rows at 39%, the guard at 32% and both amplify rows at 37%. Weight of Eons is the fourth purchase for exposure +4% and a small amplify; Dilated Moment (guard 35%) is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Pressure | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Temporal Erosion | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Temporal Erosion | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 39% (+4) |
| Temporal Erosion | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 40% (+10) | 32% (+2) |
| Abysmal End | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 39% (+4) |
| Abysmal End | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Singularity | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Singularity | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Singularity | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Resonance | 0 | mirror (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Resonance | 1 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Ethereal Particle Storm | 0 | Damage | enemy | 50 | 55 (+5) | 52 (+2) | 50 | 50 |
| Ethereal Particle Storm | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 32% (+2) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Heat Death: +5 Damage (0 + 2 + 3; on band)
  - Route Collapse of Ages: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Outlasting Eternity: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route All Returns to Dust: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 10 (DMG 4, DDG 1, DDT 1, IDG 2, IDT 2)
- Strongest full build by row-weighted total: Weight of Eons, Shattered Firmament, Aeons Laid Bare, Collapse of Ages (raw +17, row-weighted 38)
- Lowest row-weighted node: Dilated Moment (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Abysmal End#0

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Weight of Eons, Shattered Firmament, Heat Death, Aeons Laid Bare | +5 Damage, +2% IDG, +5% IDT |
| 2 | Weight of Eons, Shattered Firmament, Heat Death, Hush of the Void | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT |
| 3 | Weight of Eons, Shattered Firmament, Aeons Laid Bare, Collapse of Ages | +2 Damage, +5% IDG, +10% IDT |
| 4 | Weight of Eons, Shattered Firmament, Aeons Laid Bare, Hush of the Void | +2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT |
| 5 | Weight of Eons, Shattered Firmament, Hush of the Void, Dilated Moment | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Weight of Eons, Shattered Firmament, Hush of the Void, Dimming of Stars | +2 Damage, +2% IDG, +5% DDG, +2% IDT, +2% DDT |
| 7 | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Hush of the Void | +5% IDG, +2% DDG, +10% IDT, +2% DDT |
| 8 | Weight of Eons, Aeons Laid Bare, Hush of the Void, Dilated Moment | +2% IDG, +2% DDG, +5% IDT, +5% DDT |
| 9 | Weight of Eons, Aeons Laid Bare, Hush of the Void, Dimming of Stars | +2% IDG, +5% DDG, +5% IDT, +2% DDT |
| 10 | Weight of Eons, Hush of the Void, Dilated Moment, Outlasting Eternity | +5% IDG, +2% DDG, +2% IDT, +10% DDT |
| 11 | Weight of Eons, Hush of the Void, Dilated Moment, Dimming of Stars | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | Weight of Eons, Hush of the Void, Dimming of Stars, All Returns to Dust | +2% IDG, +10% DDG, +4% IDT, +2% DDT |
| 13 | Hush of the Void, Dilated Moment, Outlasting Eternity, Dimming of Stars | +3% IDG, +5% DDG, +10% DDT |
| 14 | Hush of the Void, Dilated Moment, Dimming of Stars, All Returns to Dust | +10% DDG, +2% IDT, +5% DDT |

## Design notes

- Node split: the two roots mirror the kit's two support axes. Weight of Eons (offence) raises both self amplify rows (Abysmal End, Singularity) and both exposure rows (Temporal Erosion, Abysmal End); Hush of the Void (control) raises the single guard row (Temporal Erosion) and single suppression row (Ethereal Particle Storm). Each root forks into two Hidden Art → Advanced Art routes (Damage and Exposure; Guard and Suppression): 2/4/4, every Advanced Art 3 BP deep, any two Advanced Arts 5–6 BP.
- Recalibration (RUL-2026-10-03-005): Collapse of Ages' Increase Damage Taken rises from +2% to +5%, so the Pressure route lands on +10% (+2%/+3%/+5%: 45% per row; both apply when they sit on one target, ×1.45 × 1.45 ≈ ×2.10) instead of +7%; no other value changes. Routes: Burst +5 Damage (Shattered Firmament +2, Heat Death +3); Pressure +10% Increase Damage Taken; Fortress +10% Decrease Damage Taken; Suppression +10% Decrease Damage Given. Increase Damage Given is glue held to +5% (40%). All Returns to Dust's secondary exposure (+2%) never outbids Aeons Laid Bare (+3%). Maxima over every legal allocation: Damage +5, IDG +5%, IDT +10%, DDT +10%, DDG +10%.
- Filters: Abysmal End's amplify and exposure rows are Ninjutsu-filtered and element-less, so they match every element-less hit of any stat type plus any Ninjutsu-general damage (the kit's own Dust attacks); Singularity's amplify lists Dust/Earth/None/Wind; Temporal Erosion's exposure adds Intelligence/Willpower. The guard and suppression rows list every general type and match effectively every non-pierce hit. The passive Increase Damage Given multiplies the enhanced damage rows downstream.
- Delivery: all five jutsu have cooldown 7. Temporal Erosion, Resonance and Particle Storm are 60 AP single-target casts at range 4. Singularity is a 60 AP ground circle at range 5: its damage reaches enemies on the tiles (friendly fire ENEMIES), its self amplify lands on the caster. Abysmal End is a 40 AP circle at range 4: exposure is applied once to each living non-caster user in the circle. Percentage rows last 2 rounds; guard and suppression ride on attacks. No rotation simulated.
- Fourth purchases: Burst takes Hush of the Void (guard and suppression +2%) or Aeons Laid Bare (exposure +5%); Pressure takes Shattered Firmament (+2 Damage) or Hush of the Void; Fortress takes Weight of Eons (amplify +5%, exposure +2%) or Dimming of Stars (suppression +5%); Suppression takes Weight of Eons (exposure +4%, amplify +2%) or Dilated Moment (guard +5%). No-Advanced hybrids spread smaller gains across more tags. All 14 legal full builds are non-dominated; every node appears in one.
- Weaknesses kept: the defensive capstone Outlasting Eternity adds no Damage and no Damage node carries a defensive secondary, so the Fortress build is not also the best burst purchase. The guard lasts 2 rounds per 7-round Temporal Erosion cooldown, so a Fortress build is a timing build rather than a permanent wall, and the control root's Foundation reaches only two rows against the offence root's four.

## Risks and unproven interactions

- Friendly fire on Abysmal End's exposure row (dossier 'Ally hazard'; validator warning accepted): the jutsu targets OTHER_USER with AOE_CIRCLE_SPAWN, so allies in the radius-1 circle also receive the Increase Damage Taken debuff when friendly fire is none/ALL; the caster is never a target. Weight of Eons, Aeons Laid Bare, Collapse of Ages and All Returns to Dust raise what allies there take.
- Exposure stacking: Temporal Erosion and Abysmal End each apply a separate 2-round Increase Damage Taken and BATTLE_TAG_STACKING is on at the pin, so one target can carry both, compounding (×1.35 × 1.35 ≈ ×1.82 at base, ×1.45 × 1.45 ≈ ×2.10 at the +10% route maximum), on every qualifying hit from the caster, allies and weapons. The Pressure build with Shattered Firmament is the strongest full build by row weight (38). No combat simulation was run.
- Damage on four rows: +5 EP reaches all four Dust attacks, Resonance's included although its Mirror identity is unsupported. The hits are formula-calculated and the passive multiplies them, so +5 EP is not +5 damage.
- Reach: the self amplify rows also multiply normal jutsu and weapon hits that pass their filters (Abysmal End: Ninjutsu-general or element-less; Singularity: Dust/Earth/Wind or element-less) while active; exposure and suppression also alter damage from allies and weapons, and Particle Storm's suppression matches effectively every non-pierce source. Pierce ignores all four tags.
- Single-cast concentration: Temporal Erosion carries Damage, the only guard row and one exposure row, so the hybrid Weight of Eons / Shattered Firmament / Hush of the Void / Dilated Moment raises all three rows of one 60 AP cast; Collapse of Ages raises both Abysmal End rows from one 40 AP cast, so that B-rank support cast gains the most per AP. The 40% guard lasts 2 rounds per 7-round cooldown.
- Classification: Dust is shared with Aerathiel and Nejireru Funjin (expected under RUL-2026-10-03-005). 5 of 10 kit rows carry Dust; the other five need the proposed jutsu-classification resolver, and Abysmal End carries no element on any row, so in-kit it qualifies only through an authored Dust jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Dust coverage is unverified.
- Unsupported rows (Resonance Mirror 100%, Singularity Move 1) are unchanged by every node; the dossier's enemy-hazard flag on the Move row concerns that unsupported row only. Ranked PvP and ranked sparring suppress skill-tree effects at the pin, so the whole tree is inert there. Normal-tree potency policy is not approved; a combined stacking audit is still required before any implementation.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Dust jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

