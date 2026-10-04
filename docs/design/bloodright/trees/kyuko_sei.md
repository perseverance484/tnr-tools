# Kyuko-sei — Ash of Dying Stars

**Bloodline:** Kyuko-sei (BR-040, rank A, `Y10fxyLR39IBJ3ICkAdEp`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Dust classification / forked tree · **Classification:** Dust (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense multipliers: self amplification (Hush of the Void → Heat Death) and exposure (Weight of Eons → Collapse of Ages), each +8% on two compounding rows · secondary Defense: Temporal Erosion guard (Outlasting Eternity) and Ethereal Particle Storm suppression (All Returns to Dust), +10% on one row each · tertiary Damage left unamplified: Ethereal Particle Storm is 50 EP, so any flat Damage passes the Nuke tier.

The Foundations split self from enemy. Hush of the Void answers "How do I make myself the dying star: strike harder or take less?" with Heat Death (both self amplify rows) or Outlasting Eternity (the Temporal Erosion guard). Weight of Eons answers "How do I wear the enemy down: make them take more or deal less?" with Collapse of Ages (both exposure rows) or All Returns to Dust (the Particle Storm suppression). The Burst trait is carried by the amplify and exposure multipliers rather than flat Damage, because every flat Damage point also reaches Particle Storm's 50 EP row. Potency reaches matching supported tags on all Dust jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hush of the Void | Foundation | How do I make myself the dying star: strike harder or take less? |
| Weight of Eons | Foundation | How do I wear the enemy down: make them take more or deal less? |
| Heat Death | Advanced Art | burst: a self-amplified strike window (two compounding self buffs on the caster's hits) |
| Outlasting Eternity | Advanced Art | fortress: a timed guard on Temporal Erosion |
| Collapse of Ages | Advanced Art | exposure: the marked target takes more from every source, allies included |
| All Returns to Dust | Advanced Art | suppression: the struck enemy deals less to everyone |

- Concern: No flat Damage node on a kit with four Damage rows and the Burst trait: Ethereal Particle Storm is 50 EP, so any flat Damage passes the Nuke tier. If the director prefers the Blood-Enchanted Eyes pattern, Heat Death is where +2 Damage would go (40 → 42 on three rows, Particle Storm 50 → 52).
- Concern: In a duel Heat Death and Collapse of Ages both multiply the caster's hits on the target; they separate in group play (a self buff on any target and Singularity's area versus a debuff that also multiplies allies' hits) and by Foundation. Rotation and uptime were not simulated.
- Concern: The defensive routes rest on one row each, live 2 rounds per 7-round cooldown.
- Concern: Five of the six buff/debuff rows depend on the proposed jutsu-classification resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dust jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 06 | Hush of the Void | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Abysmal End, Singularity, Temporal Erosion / 3 |
| 02 | Shattered Firmament | Hidden Art | Hush of the Void | +2% Increase Damage Given (self buff) | Abysmal End, Singularity / 2 |
| 03 | Heat Death | Advanced Art | Shattered Firmament | +4% Increase Damage Given (self buff) | Abysmal End, Singularity / 2 |
| 07 | Dilated Moment | Hidden Art | Hush of the Void | +3% Decrease Damage Taken (self buff) | Temporal Erosion / 1 |
| 08 | Outlasting Eternity | Advanced Art | Dilated Moment | +5% Decrease Damage Taken (self buff) | Temporal Erosion / 1 |
| 01 | Weight of Eons | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Abysmal End, Ethereal Particle Storm, Temporal Erosion / 3 |
| 04 | Aeons Laid Bare | Hidden Art | Weight of Eons | +2% Increase Damage Taken (enemy debuff) | Abysmal End, Temporal Erosion / 2 |
| 05 | Collapse of Ages | Advanced Art | Aeons Laid Bare | +4% Increase Damage Taken (enemy debuff) | Abysmal End, Temporal Erosion / 2 |
| 09 | Dimming of Stars | Hidden Art | Weight of Eons | +3% Decrease Damage Given (enemy debuff) | Ethereal Particle Storm / 1 |
| 10 | All Returns to Dust | Advanced Art | Dimming of Stars | +5% Decrease Damage Given (enemy debuff) | Ethereal Particle Storm / 1 |

Connections: 06→02, 02→03, 06→07, 07→08, 01→04, 04→05, 01→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hush of the Void** — In the hush before a star collapses, it draws in all its light and all its weight. Self rows: Abysmal End and Singularity amplify 35 → 37%; Temporal Erosion guard 30 → 32%. 2 rounds each.
- **Shattered Firmament** — The sky cracks, and the light of a dying star pours through you. Abysmal End and Singularity self amplify 37 → 39% with Hush of the Void.
- **Heat Death** — Every fire goes out. Yours merely goes first. Burst: both self amplify rows 35 → 43% on the full route; with both up, the caster's matching hits are multiplied ×1.43 × 1.43 ≈ ×2.04 (×1.82 at base).
- **Dilated Moment** — A heartbeat stretched until the blow arrives too late. Temporal Erosion guard 32 → 35% with Hush of the Void (one self row, 2 rounds per 60 AP cast).
- **Outlasting Eternity** — When the last light fails, you are still standing there. Fortress: Temporal Erosion guard 30 → 40% on the full route; for two rounds hits taken deal ×0.60 instead of ×0.70.
- **Weight of Eons** — What the hollow star touches grows old before it can resist. Enemy rows: Temporal Erosion and Abysmal End exposure 35 → 37%; Ethereal Particle Storm suppression 30 → 32%. 2 rounds each.
- **Aeons Laid Bare** — Armor is only time that has not yet passed. Temporal Erosion (single) and Abysmal End (area, ally hazard) exposure 37 → 39% with Weight of Eons.
- **Collapse of Ages** — Centuries fold into a single falling instant. Exposure: both rows 35 → 43% on the full route; a target carrying both takes ×1.43 × 1.43 ≈ ×2.04 (×1.82 at base) from every matching hit, allies' included.
- **Dimming of Stars** — One by one the enemy's fires gutter and go dark. Ethereal Particle Storm suppression 32 → 35% with Weight of Eons (single target, 2 rounds per 60 AP cast).
- **All Returns to Dust** — Stars, mountains, names: the dust keeps none of them. Suppression: Ethereal Particle Storm 30 → 40% on the full route; for two rounds the struck enemy's matching hits on anyone deal ×0.60 instead of ×0.70.

## Complete four-purchase examples

| Build | Purchases | IDG | DDG | IDT | DDT |
|---|---|---:|---:|---:|---:|
| Heat Death (Burst) | Hush of the Void, Shattered Firmament, Heat Death, Weight of Eons | +8% | +2% | +2% | +2% |
| Outlasting Eternity (Fortress) | Hush of the Void, Dilated Moment, Outlasting Eternity, Shattered Firmament | +4% | — | — | +10% |
| Collapse of Ages (Exposure) | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Dimming of Stars | — | +5% | +8% | — |
| All Returns to Dust (Suppression) | Weight of Eons, Dimming of Stars, All Returns to Dust, Hush of the Void | +2% | +10% | +2% | +2% |

Abbreviations: IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Heat Death:** Abysmal End and Singularity self amplify 35 → 43% (both up: ×1.43 × 1.43 ≈ ×2.04); Weight of Eons is the fourth purchase (exposure 37%, Particle Storm suppression 32%). Temporal Erosion guard 32%.
- **Outlasting Eternity:** Temporal Erosion guard 30 → 40%; Shattered Firmament is the fourth purchase, so both self amplify rows reach 39% and the guarded window still strikes back.
- **Collapse of Ages:** Temporal Erosion and Abysmal End exposure 35 → 43% (×2.04 on a target carrying both); Dimming of Stars is the fourth purchase, so Particle Storm's struck target also deals 35% less.
- **All Returns to Dust:** Particle Storm suppression 30 → 40%; Hush of the Void is the fourth purchase (Temporal Erosion guard 32%, self amplify 37%); exposure 37%.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Fortress | Exposure | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Temporal Erosion | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Temporal Erosion | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 37% (+2) |
| Temporal Erosion | 2 | Decrease Damage Taken | self | 30% | 32% (+2) | 40% (+10) | 30% | 32% (+2) |
| Abysmal End | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 37% (+2) |
| Abysmal End | 1 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 35% | 37% (+2) |
| Singularity | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Singularity | 1 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 35% | 37% (+2) |
| Singularity | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Resonance | 0 | mirror (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Resonance | 1 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Ethereal Particle Storm | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Ethereal Particle Storm | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 35% (+5) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Heat Death: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Collapse of Ages: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Outlasting Eternity: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route All Returns to Dust: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 10 (DMG 4, DDG 1, DDT 1, IDG 2, IDT 2)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Weight of Eons, Shattered Firmament, Heat Death, Hush of the Void (raw +14, row-weighted 24)
- Lowest row-weighted node: Dilated Moment (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Abysmal End#0
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Temporal Erosion 40 (Normal), Singularity 40 (Normal), Resonance 40 (Normal), Ethereal Particle Storm 50 (Nuke)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Heat Death | +8% IDG, +2% DDT | Weight of Eons *(highest diagnostic)* | +8% IDG, +2% DDG, +2% IDT, +2% DDT | 24 |
| Heat Death | +8% IDG, +2% DDT | Dilated Moment | +8% IDG, +5% DDT | 21 |
| Collapse of Ages | +2% DDG, +8% IDT | Hush of the Void *(highest diagnostic)* | +2% IDG, +2% DDG, +8% IDT, +2% DDT | 24 |
| Collapse of Ages | +2% DDG, +8% IDT | Dimming of Stars | +5% DDG, +8% IDT | 21 |
| Outlasting Eternity | +2% IDG, +10% DDT | Weight of Eons *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% DDT | 20 |
| Outlasting Eternity | +2% IDG, +10% DDT | Shattered Firmament | +4% IDG, +10% DDT | 18 |
| All Returns to Dust | +10% DDG, +2% IDT | Aeons Laid Bare | +10% DDG, +4% IDT | 18 |
| All Returns to Dust | +10% DDG, +2% IDT | Hush of the Void *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +2% DDT | 20 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Weight of Eons, Shattered Firmament, Heat Death, Hush of the Void | +8% IDG, +2% DDG, +2% IDT, +2% DDT |
| 2 | Weight of Eons, Shattered Firmament, Aeons Laid Bare, Hush of the Void | +4% IDG, +2% DDG, +4% IDT, +2% DDT |
| 3 | Weight of Eons, Shattered Firmament, Hush of the Void, Dilated Moment | +4% IDG, +2% DDG, +2% IDT, +5% DDT |
| 4 | Weight of Eons, Shattered Firmament, Hush of the Void, Dimming of Stars | +4% IDG, +5% DDG, +2% IDT, +2% DDT |
| 5 | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Hush of the Void | +2% IDG, +2% DDG, +8% IDT, +2% DDT |
| 6 | Weight of Eons, Aeons Laid Bare, Collapse of Ages, Dimming of Stars | +5% DDG, +8% IDT |
| 7 | Weight of Eons, Aeons Laid Bare, Hush of the Void, Dilated Moment | +2% IDG, +2% DDG, +4% IDT, +5% DDT |
| 8 | Weight of Eons, Aeons Laid Bare, Hush of the Void, Dimming of Stars | +2% IDG, +5% DDG, +4% IDT, +2% DDT |
| 9 | Weight of Eons, Aeons Laid Bare, Dimming of Stars, All Returns to Dust | +10% DDG, +4% IDT |
| 10 | Weight of Eons, Hush of the Void, Dilated Moment, Outlasting Eternity | +2% IDG, +2% DDG, +2% IDT, +10% DDT |
| 11 | Weight of Eons, Hush of the Void, Dilated Moment, Dimming of Stars | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | Weight of Eons, Hush of the Void, Dimming of Stars, All Returns to Dust | +2% IDG, +10% DDG, +2% IDT, +2% DDT |
| 13 | Shattered Firmament, Heat Death, Hush of the Void, Dilated Moment | +8% IDG, +5% DDT |
| 14 | Shattered Firmament, Hush of the Void, Dilated Moment, Outlasting Eternity | +4% IDG, +10% DDT |

## Design notes

- Rewire (2026-10-04 batch): the old offence/defence Foundations became self/enemy Foundations; Shattered Firmament moved under Hush of the Void and Dimming of Stars under Weight of Eons. With flat Damage gone, an offence Foundation would have held two multiplier routes (amplify, exposure) whose obvious fourth purchase was each other's Hidden Art, ending in the same build. Split by recipient, each multiplier route's sibling is a defensive one.
- Damage removed: the old +2/+3 route lifted Temporal Erosion, Singularity and Resonance 40 → 45 and Ethereal Particle Storm 50 → 52 at the Hidden Art and 55 at the capstone. Potency cannot leave Particle Storm out, so the Burst trait rides on the multipliers instead.
- Values: Heat Death and Collapse of Ages stop at +8% (2/2/4) because each tag's two rows compound on one target (×1.43 × 1.43 ≈ ×2.04, ×1.82 at base). Outlasting Eternity and All Returns to Dust reach +10% (2/3/5) on one row each (×0.60 instead of ×0.70). Each capstone carries one effect; the old riders (Increase Damage Given on Collapse of Ages and Outlasting Eternity, Increase Damage Taken on All Returns to Dust) are gone. Maxima over every legal allocation: Increase Damage Given +8%, Increase Damage Taken +8%, Decrease Damage Taken +10%, Decrease Damage Given +10%, no Damage.
- Fourth purchases: Heat Death takes Weight of Eons (exposure 37%, suppression 32%) or Dilated Moment (guard 35%); Outlasting Eternity takes Shattered Firmament (amplify 39%) or Weight of Eons; Collapse of Ages takes Dimming of Stars (suppression 35%) or Hush of the Void; All Returns to Dust takes Aeons Laid Bare (exposure 39%) or Hush of the Void. The strongest offensive build is one multiplier route plus the other Foundation: +8% on one multiplier and +2% on the other.
- Delivery: every jutsu has cooldown 7 and its percentage rows last the 2 rounds after the cast. Abysmal End (40 AP, no damage) carries one amplify and one exposure row, so both multiplier routes use it; Heat Death's other row is on Singularity, Collapse of Ages' on Temporal Erosion. The guard rides on Temporal Erosion and the suppression on Particle Storm, both 60 AP attacks. No rotation simulated.

## Risks and unproven interactions

- Ally hazard: Abysmal End's exposure lands on every living non-caster user in its radius-1 circle (friendly fire none = ALL), allies included; Weight of Eons, Aeons Laid Bare and Collapse of Ages raise it to 43% at most.
- Exposure stacking: Temporal Erosion and Abysmal End each apply their own 2-round Increase Damage Taken and both apply to one target (BATTLE_TAG_STACKING), on every matching hit from the caster, allies and weapons: ×1.82 at base, ×2.04 at the Collapse of Ages maximum. Heat Death's two self buffs compound the same way on the caster's own hits.
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

