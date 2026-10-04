# Kyuko-sei — Ash of Dying Stars

**Bloodline:** Kyuko-sei (BR-040, rank A, `Y10fxyLR39IBJ3ICkAdEp`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Dust classification / forked tree · **Classification:** Dust (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst and exposure: Shattered Firmament's self amplify setup (35 → 40% on two rows) into Heat Death's +2 Damage on all four Dust strikes (40 → 42, Particle Storm 50 → 52); Collapse of Ages' exposure +8% on two compounding rows (35 → 43%, ≈ ×1.122) · secondary Defense: Temporal Erosion guard (Outlasting Eternity) and Ethereal Particle Storm suppression (All Returns to Dust), +10% on one row each · tertiary Recipient split at the root: self buffs (Hush of the Void) against enemy debuffs (Weight of Eons), so the burst setup and the exposure capstone never share a 4-BP build.

The Foundations split self from enemy. Hush of the Void answers "How do I make myself the dying star: strike harder or take less?" with Heat Death (amplify setup into raw Damage) or Outlasting Eternity (the Temporal Erosion guard). Weight of Eons answers "How do I wear the enemy down: make them take more or deal less?" with Collapse of Ages (both exposure rows) or All Returns to Dust (the Particle Storm suppression). The Burst trait keeps a raw-Damage route on the Blood-Enchanted Eyes pattern: a percentage setup on the Hidden Art and a controlled +2 Damage payoff on the Advanced Art, which lifts Particle Storm 50 → 52 as the director precedent does. Potency reaches matching supported tags on all Dust jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hush of the Void | Foundation | How do I make myself the dying star: strike harder or take less? |
| Weight of Eons | Foundation | How do I wear the enemy down: make them take more or deal less? |
| Heat Death | Advanced Art | burst: self amplify setup into a controlled +2 Damage payoff on all four strikes |
| Outlasting Eternity | Advanced Art | fortress: a timed guard on Temporal Erosion |
| Collapse of Ages | Advanced Art | exposure: the marked target takes more from every source, allies included |
| All Returns to Dust | Advanced Art | suppression: the struck enemy deals less to everyone |

**Director review recommended:** Roster questions: DQ-A (Heat Death +2 Damage after the Shattered Firmament setup, Ethereal Particle Storm 50 → 52, kept for the dossier's Burst trait; see above_nuke_rationale); DQ-B (Collapse of Ages +8% Increase Damage Taken on two compounding rows, Temporal Erosion and Abysmal End 35 → 43%, ≈ ×1.122, against Blood-Enchanted Eyes' ×1.115 and Shakunetsu Sakura's ×1.075); DQ-H (self/enemy root axis: Hush of the Void owns the self buffs and Weight of Eons the enemy debuffs, in place of the anchors' offence/defence roots, so the Shattered Firmament setup is never Collapse of Ages' fourth purchase).

- Concern: Root axis: the self/enemy split departs from the offence/defence roots of Blood-Enchanted Eyes, Shakunetsu Sakura and Arashima, and a duel barely sees it (each Foundation gives +2% to one multiplier pair and one defensive row). It is kept so that the burst setup cannot be Collapse of Ages' fourth purchase. Under the offence/defence wiring, Collapse of Ages + Shattered Firmament would reach exposure 43% and amplify 40% together.
- Concern: In a duel the defensive capstones mirror: Outlasting Eternity (+10% guard, +2% amplify) and All Returns to Dust (+10% suppression, +2% exposure) cut the caster's damage taken by the same factor. They separate only in group play (several attackers against the guard, or the suppressed enemy hitting allies). This is accepted as in Blood-Enchanted Eyes' fortress/suppression pair. Both are single-tag, lighter than the anchors' riders.
- Concern: Shattered Firmament and Collapse of Ages each count Abysmal End as one of their two rows, and Abysmal End is Dust only by authored jutsu classification. Without that classification Collapse of Ages reaches only Temporal Erosion and the amplify setup only Singularity, so the +8% two-row exposure value and the +5% amplify should be revisited. Heat Death's +2 Damage reaches four natively Dust rows and does not depend on it.
- Concern: The defensive routes rest on one row each, live 2 rounds per 7-round cooldown.
- Concern: Five of the six buff/debuff rows depend on the proposed jutsu-classification resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dust jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 06 | Hush of the Void | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Abysmal End, Singularity, Temporal Erosion / 3 |
| 02 | Shattered Firmament | Hidden Art | Hush of the Void | +3% Increase Damage Given (self buff) | Abysmal End, Singularity / 2 |
| 03 | Heat Death | Advanced Art | Shattered Firmament | +2 Damage (damage) | Ethereal Particle Storm, Resonance, Singularity, Temporal Erosion / 4 |
| 07 | Dilated Moment | Hidden Art | Hush of the Void | +3% Decrease Damage Taken (self buff) | Temporal Erosion / 1 |
| 08 | Outlasting Eternity | Advanced Art | Dilated Moment | +5% Decrease Damage Taken (self buff) | Temporal Erosion / 1 |
| 01 | Weight of Eons | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Abysmal End, Ethereal Particle Storm, Temporal Erosion / 3 |
| 04 | Aeons Laid Bare | Hidden Art | Weight of Eons | +2% Increase Damage Taken (enemy debuff) | Abysmal End, Temporal Erosion / 2 |
| 05 | Collapse of Ages | Advanced Art | Aeons Laid Bare | +4% Increase Damage Taken (enemy debuff) | Abysmal End, Temporal Erosion / 2 |
| 09 | Dimming of Stars | Hidden Art | Weight of Eons | +3% Decrease Damage Given (enemy debuff) | Ethereal Particle Storm / 1 |
| 10 | All Returns to Dust | Advanced Art | Dimming of Stars | +5% Decrease Damage Given (enemy debuff) | Ethereal Particle Storm / 1 |

Connections: 06→02, 02→03, 06→07, 07→08, 01→04, 04→05, 01→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hush of the Void** — In the hush before a star collapses, it draws in all its light and all its weight. Self rows: Abysmal End and Singularity amplify 35 → 37%; Temporal Erosion guard 30 → 32%. 2 rounds each.
- **Shattered Firmament** — The sky cracks, and the light of a dying star pours through you. Setup: Abysmal End and Singularity self amplify 37 → 40% with Hush of the Void (2 rounds each).
- **Heat Death** — Every fire goes out. Yours merely goes first. Burst payoff: +2 Damage on all four Dust strikes, Temporal Erosion, Singularity and Resonance 40 → 42 and Ethereal Particle Storm 50 → 52 EP (above the 50 Nuke tier; director review). The route's two self amplify rows sit at 40%.
- **Dilated Moment** — A heartbeat stretched until the blow arrives too late. Temporal Erosion guard 32 → 35% with Hush of the Void (one self row, 2 rounds per 60 AP cast).
- **Outlasting Eternity** — When the last light fails, you are still standing there. Fortress: Temporal Erosion guard 30 → 40% on the full route; for two rounds hits taken deal ×0.60 instead of ×0.70.
- **Weight of Eons** — What the hollow star touches grows old before it can resist. Enemy rows: Temporal Erosion and Abysmal End exposure 35 → 37%; Ethereal Particle Storm suppression 30 → 32%. 2 rounds each.
- **Aeons Laid Bare** — Armor is only time that has not yet passed. Temporal Erosion (single) and Abysmal End (area, ally hazard) exposure 37 → 39% with Weight of Eons.
- **Collapse of Ages** — Centuries fold into a single falling instant. Exposure: both rows 35 → 43% on the full route; a target carrying both takes ×1.43 × 1.43 ≈ ×2.04 instead of ×1.82 (≈ ×1.122, against Blood-Enchanted Eyes' ×1.115 exposure maximum) from every matching hit, allies' included.
- **Dimming of Stars** — One by one the enemy's fires gutter and go dark. Ethereal Particle Storm suppression 32 → 35% with Weight of Eons (single target, 2 rounds per 60 AP cast).
- **All Returns to Dust** — Stars, mountains, names: the dust keeps none of them. Suppression: Ethereal Particle Storm 30 → 40% on the full route; for two rounds the struck enemy's matching hits on anyone deal ×0.60 instead of ×0.70.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT |
|---|---|---:|---:|---:|---:|---:|
| Heat Death (Burst) | Hush of the Void, Shattered Firmament, Heat Death, Weight of Eons | +2 | +5% | +2% | +2% | +2% |
| Outlasting Eternity (Fortress) | Hush of the Void, Dilated Moment, Outlasting Eternity, Shattered Firmament | — | +5% | — | — | +10% |
| Collapse of Ages (Exposure) | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Dimming of Stars | — | — | +5% | +8% | — |
| All Returns to Dust (Suppression) | Weight of Eons, Dimming of Stars, All Returns to Dust, Hush of the Void | — | +2% | +10% | +2% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Heat Death:** Self amplify setup into raw Damage: Abysmal End and Singularity amplify 35 → 40% (≈ ×1.075 with both up), then +2 Damage on all four Dust strikes (Temporal Erosion, Singularity and Resonance 40 → 42; Particle Storm 50 → 52 EP). Weight of Eons is the fourth purchase (exposure 37%, suppression 32%); the whole package is ≈ ×1.108 with every window live; Temporal Erosion guard 32%.
- **Outlasting Eternity:** Temporal Erosion guard 30 → 40%; Shattered Firmament is the fourth purchase, so both self amplify rows reach 40% on every target the guarded window strikes. In a duel Weight of Eons (exposure 37%, suppression 32%) is the stronger defensive fourth.
- **Collapse of Ages:** Temporal Erosion and Abysmal End exposure 35 → 43% (×2.04 instead of ×1.82 on a target carrying both, ≈ ×1.122); Dimming of Stars is the fourth purchase, so Particle Storm's struck target also deals 35% less.
- **All Returns to Dust:** Particle Storm suppression 30 → 40%; Hush of the Void is the fourth purchase (Temporal Erosion guard 32%, self amplify 37%); exposure 37%. Aeons Laid Bare (exposure 39%) is the group-play alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Fortress | Exposure | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Temporal Erosion | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Temporal Erosion | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 37% (+2) |
| Temporal Erosion | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 40% (+10) | 30% | 32% (+2) |
| Abysmal End | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 37% (+2) |
| Abysmal End | 1 | Increase Damage Given | self | 35% | 40% (+5) | 40% (+5) | 35% | 37% (+2) |
| Singularity | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Singularity | 1 | Increase Damage Given | self | 35% | 40% (+5) | 40% (+5) | 35% | 37% (+2) |
| Singularity | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Resonance | 0 | mirror (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Resonance | 1 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Ethereal Particle Storm | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Ethereal Particle Storm | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 35% (+5) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Heat Death: +2 Damage (0 + 0 + 2; off band)
  - Route Collapse of Ages: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Outlasting Eternity: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route All Returns to Dust: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 10 (DMG 4, DDG 1, DDT 1, IDG 2, IDT 2)
- Strongest full build by row-weighted total: Weight of Eons, Shattered Firmament, Heat Death, Hush of the Void (raw +13, row-weighted 26)
- Lowest row-weighted node: Dilated Moment (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Ethereal Particle Storm 50 -> 52
- ally-hazard area rows amplified (friendly fire none/ALL): Abysmal End#0

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Temporal Erosion | 0 | 40 (Normal) | 42 (Normal) |
| Singularity | 0 | 40 (Normal) | 42 (Normal) |
| Resonance | 1 | 40 (Normal) | 42 (Normal) |
| Ethereal Particle Storm | 0 | 50 (Nuke) | **52 (above Nuke)** |

Above-Nuke rationale: Kit fact: the Kyuko-sei dossier's Traits line is "Burst, Control"; Ethereal Particle Storm (50 EP, 60 AP, cooldown 7, single target) is the highest of its four Dust strikes. Heat Death's +2 Damage lifts it 50 → 52, past the 50 Nuke tier, as the controlled payoff of the burst route (Shattered Firmament's +3% Increase Damage Given setup, then +2 Damage): the pattern the director kept in Blood-Enchanted Eyes (Rite of Exsanguination, Reaper's Embrace 50 → 52; RUL-2026-10-04-001) and Shakunetsu Sakura (Conflagration in Bloom, Sakura-ame 50 → 52; RUL-2026-10-04-002). Flat Damage sits only on Heat Death, so no allocation without it exceeds 50; no legal allocation exceeds +2 Damage; the three 40 EP strikes stay in the Normal tier (40 → 42). Fable proposal, flagged for director review (DQ-A).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Heat Death | +2 Damage, +5% IDG, +2% DDT | Weight of Eons *(highest diagnostic)* | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT | 26 |
| Heat Death | +2 Damage, +5% IDG, +2% DDT | Dilated Moment | +2 Damage, +5% IDG, +5% DDT | 23 |
| Collapse of Ages | +2% DDG, +8% IDT | Hush of the Void *(highest diagnostic)* | +2% IDG, +2% DDG, +8% IDT, +2% DDT | 24 |
| Collapse of Ages | +2% DDG, +8% IDT | Dimming of Stars | +5% DDG, +8% IDT | 21 |
| Outlasting Eternity | +2% IDG, +10% DDT | Weight of Eons *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% DDT | 20 |
| Outlasting Eternity | +2% IDG, +10% DDT | Shattered Firmament | +5% IDG, +10% DDT | 20 |
| All Returns to Dust | +10% DDG, +2% IDT | Aeons Laid Bare | +10% DDG, +4% IDT | 18 |
| All Returns to Dust | +10% DDG, +2% IDT | Hush of the Void *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +2% DDT | 20 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Weight of Eons, Shattered Firmament, Heat Death, Hush of the Void | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT |
| 2 | Weight of Eons, Shattered Firmament, Aeons Laid Bare, Hush of the Void | +5% IDG, +2% DDG, +4% IDT, +2% DDT |
| 3 | Weight of Eons, Shattered Firmament, Hush of the Void, Dilated Moment | +5% IDG, +2% DDG, +2% IDT, +5% DDT |
| 4 | Weight of Eons, Shattered Firmament, Hush of the Void, Dimming of Stars | +5% IDG, +5% DDG, +2% IDT, +2% DDT |
| 5 | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Hush of the Void | +2% IDG, +2% DDG, +8% IDT, +2% DDT |
| 6 | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Dimming of Stars | +5% DDG, +8% IDT |
| 7 | Weight of Eons, Aeons Laid Bare, Hush of the Void, Dilated Moment | +2% IDG, +2% DDG, +4% IDT, +5% DDT |
| 8 | Weight of Eons, Aeons Laid Bare, Hush of the Void, Dimming of Stars | +2% IDG, +5% DDG, +4% IDT, +2% DDT |
| 9 | Weight of Eons, Aeons Laid Bare, Dimming of Stars, All Returns to Dust | +10% DDG, +4% IDT |
| 10 | Weight of Eons, Hush of the Void, Dilated Moment, Outlasting Eternity | +2% IDG, +2% DDG, +2% IDT, +10% DDT |
| 11 | Weight of Eons, Hush of the Void, Dilated Moment, Dimming of Stars | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | Weight of Eons, Hush of the Void, Dimming of Stars, All Returns to Dust | +2% IDG, +10% DDG, +2% IDT, +2% DDT |
| 13 | Shattered Firmament, Heat Death, Hush of the Void, Dilated Moment | +2 Damage, +5% IDG, +5% DDT |
| 14 | Shattered Firmament, Hush of the Void, Dilated Moment, Outlasting Eternity | +5% IDG, +10% DDT |

## Design notes

- Root axis: the Foundations split self buffs (Hush of the Void: amplify and guard) from enemy debuffs (Weight of Eons: exposure and suppression), unlike the offence/defence roots of the director anchors. This keeps Shattered Firmament (the burst setup) and Collapse of Ages (the exposure capstone) in different roots. No 4-BP build stacks the +5% amplify on the +8% exposure route, and each multiplier route's other multiplier stays at the other Foundation's +2%. Under the pre-batch offence/defence wiring, Collapse of Ages' obvious fourth would be Shattered Firmament: exposure 43% and amplify 40% together. The cost is that a duel barely separates the two Foundations.
- Damage (kit fact): the dossier Traits are Burst, Control, and Ethereal Particle Storm (50 EP, 60 AP, cooldown 7, single target) is the highest of the four Dust strikes, so the burst route stays. The pre-batch route put flat Damage on the Hidden Art and reached 40 → 45 and 50 → 55; now Shattered Firmament sets up with +3% Increase Damage Given and only Heat Death carries flat Damage, +2: 40 → 42 on three strikes and Particle Storm 50 → 52, never 55 (Blood-Enchanted Eyes / Shakunetsu Sakura pattern, RUL-2026-10-04-001/002). The setup is self amplification rather than exposure because Aeons Laid Bare already owns the exposure rows.
- Values: Heat Death's route is +5% amplify (Abysmal End and Singularity 35 → 40%; ≈ ×1.075 with both up) plus +2 Damage. Collapse of Ages stops at +8% (2/2/4) because its two exposure rows compound on one target (≈ ×1.122, against the Blood-Enchanted Eyes ×1.115 and Shakunetsu Sakura ×1.075 exposure anchors). Outlasting Eternity and All Returns to Dust reach +10% (2/3/5) on one row each (×0.60 instead of ×0.70, ≈ ×0.857). Each capstone carries one effect. Maxima over every legal allocation: Damage +2, Increase Damage Given +5%, Increase Damage Taken +8%, Decrease Damage Taken +10%, Decrease Damage Given +10%. Top offensive packages, all windows live: Collapse of Ages + Hush of the Void ≈ ×1.156; Heat Death + Weight of Eons ≈ ×1.108, ≈ ×1.16 on a 40 → 42 strike; both under Blood-Enchanted Eyes' ×1.234.
- Fourth purchases: Heat Death takes Weight of Eons (exposure 37%, suppression 32%) or Dilated Moment (guard 35%). Outlasting Eternity takes Shattered Firmament (amplify 40%: slightly more damage, on every target hit) or Weight of Eons (exposure 37%, suppression 32%: the stronger duel defence). Collapse of Ages takes Hush of the Void (amplify 37%, guard 32%) or Dimming of Stars (suppression 35%). All Returns to Dust takes Hush of the Void, the better duel choice, or Aeons Laid Bare (exposure 39%), which pays only in group play, where allies' hits and Abysmal End's circle use it.
- Delivery: every jutsu has cooldown 7 and its percentage rows last the 2 rounds after the cast. Abysmal End (40 AP, no damage) carries one amplify and one exposure row; the amplify's other row is on Singularity, the exposure's on Temporal Erosion. Heat Death's +2 Damage reaches all four Dust strikes (60 AP each), so the payoff lands on hits the amplify window multiplies. The guard rides on Temporal Erosion and the suppression on Particle Storm, both 60 AP attacks. No rotation simulated.

## Risks and unproven interactions

- Ally hazard: Abysmal End's exposure lands on every living non-caster user in its radius-1 circle (friendly fire none = ALL), allies included; Weight of Eons, Aeons Laid Bare and Collapse of Ages raise it to 43% at most.
- Exposure stacking: Temporal Erosion and Abysmal End each apply their own 2-round Increase Damage Taken and both apply to one target (BATTLE_TAG_STACKING), on every matching hit from the caster, allies and weapons: ×1.82 at base, ×2.04 at the Collapse of Ages maximum (≈ ×1.122). The two self amplify rows compound the same way on the caster's own hits (×1.96 at Shattered Firmament's 40%, ≈ ×1.075).
- Damage tier: every build with Heat Death lifts Ethereal Particle Storm 50 → 52 EP, past the Nuke tier (above_nuke_rationale; director review). The three 40 EP strikes reach 42 and stay in the Normal tier.
- Reach: Abysmal End's amplify and exposure rows are Ninjutsu-filtered and element-less, so they match the kit's Ninjutsu Dust attacks and every element-less hit; Singularity's amplify lists Dust/Earth/None/Wind; the guard and suppression rows list every stat type and match effectively every non-pierce hit. Pierce ignores all four tags.
- Classification: Dust is shared with Aerathiel and Nejireru Funjin (expected under RUL-2026-10-03-005). Only Singularity's amplify among the buff/debuff rows carries Dust; the other five need the proposed jutsu-classification resolver, and Abysmal End qualifies only by authored classification (ENGINE_GAP_REGISTER G1). Off-kit Dust coverage is unverified.
- Unsupported rows (Resonance Mirror, Singularity Move) are unchanged. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

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

