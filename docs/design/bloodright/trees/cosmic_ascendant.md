# Cosmic Ascendant — Weight of the Stars

**Bloodline:** Cosmic Ascendant (BR-018, rank S, `osVXxtyW61gr-bx5v5ys2`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Cosmic Ascendant classification / forked tree · **Classification:** Cosmic Ascendant (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Burst: Collapsing Star charges Cosmic Energy's self Increase Damage Given (+5% on the route), Supernova Unbound opens Increase Damage Taken on Cosmic Intent and Cosmic Chains (+5%) and pays off with a controlled +2 Damage on the 50 EP Cosmic Explosion (50 → 52) · secondary Defense: a Decrease Damage Taken fortress on three casts (+5%), or Lifesteal (+5%) with Decrease Damage Given suppression on Cosmic Aura (+7%) · tertiary Cosmic Intent's Afterburn (+10%) as one-cast, party-wide pressure on the marked enemy.

Cosmic Ascendant is a rank S Burst/Defensive kit with 10 supported rows on five cooldown-7 jutsu. Its only Damage row is Cosmic Explosion at 50 EP, the Nuke tier and the kit's only 60 AP cast, so the Burst trait keeps the director pattern of Blood-Enchanted Eyes and Shakunetsu Sakura: a percentage setup on the Hidden Art and a controlled +2 Damage payoff (Explosion 50 → 52, flagged for director review). With no other Damage row, the payoff has no in-tier Damage effect; it only extends the Nuke row. Celestial Alignment answers "How do I make the enemy I mark fall faster?": Supernova Unbound charges the caster, opens both marks and detonates a stronger Explosion into the window, while Light of Dead Stars makes every hit on Cosmic Intent's target burn. Gravity Well answers "How do I outlast the exchange: harden myself, or drain and blunt them?": Heart of the Singularity raises Decrease Damage Taken on all three guard casts, and Hunger of the Void leeches from Intent while Cosmic Aura blunts its target.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Celestial Alignment | Foundation | How do I make the enemy I mark fall faster? |
| Gravity Well | Foundation | How do I outlast the exchange: harden myself, or drain and blunt them? |
| Supernova Unbound | Advanced Art | burst: self-charge setup, both marks opened, controlled +2 Damage detonation on Cosmic Explosion |
| Light of Dead Stars | Advanced Art | pressure: one Intent cast makes every hit on the mark burn, party-wide |
| Heart of the Singularity | Advanced Art | fortress: all three guard casts |
| Hunger of the Void | Advanced Art | drain and suppression: leech from your hits while Aura blunts theirs |

**Director review recommended:** Roster questions: DQ-A (Cosmic Explosion 50 → 52 under Supernova Unbound; Explosion is the kit's only Damage row, so the route has no in-tier Damage effect and is purely a nuke extension, kept on the dossier's Burst trait; see above_nuke_rationale).

- Concern: Cosmic Explosion 50 → 52 (DQ-A) is the route's only Damage effect: it extends the Nuke row and lifts nothing within a tier. Declining it returns Supernova Unbound to the first-pass +3% Increase Damage Taken / +3% Increase Damage Given (sustained amplification and exposure, not burst).
- Concern: The Fortress is held to R3's +5% on its three compounding guard rows (Event Horizon +1%, Heart of the Singularity +2%) because two guard casts fit one 100 AP round, so the overlap is on demand; the package reads ≈ ×0.79 against base (×0.77 with Gravity Well), lighter than Blood-Enchanted Eyes' Deathless Vitality route (×0.747).
- Concern: The Fortress leads the trade diagnostic moderately (1.36 / 1.08 against 1.28 / 1.06 for Hunger + Event Horizon); that is its identity, and Hunger's Lifesteal is not counted. Not simulated.
- Concern: Gravity Well (+2% Decrease Damage Taken on three rows, +2% Decrease Damage Given) is the strongest fourth for both offensive capstones (Supernova + Gravity Well 1.26 against 1.14 with Searing Starlight); it is a defensive hedge that adds no offense, not a stacked payoff.
- Concern: Burst beats the burn only on Cosmic Explosion (×1.16 against ×1.12 on the path packages); on the caster's other hits the two paths both read ≈ ×1.12, and the burn leads for allies (×1.11 against ×1.08). Supernova is the pick for a detonation, Light of Dead Stars for sustained party pressure.
- Concern: The 'Cosmic Ascendant' classification extension remains a director/engine decision; off-kit coverage is unverified.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Cosmic Ascendant-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Celestial Alignment | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Cosmic Chains, Cosmic Energy, Cosmic Intent / 3 |
| 02 | Collapsing Star | Hidden Art | Celestial Alignment | +3% Increase Damage Given (self buff) | Cosmic Energy / 1 |
| 03 | Supernova Unbound | Advanced Art | Collapsing Star | +3% Increase Damage Taken (enemy debuff); +2 Damage (damage) | Cosmic Chains, Cosmic Explosion, Cosmic Intent / 3 |
| 04 | Searing Starlight | Hidden Art | Celestial Alignment | +3% Afterburn (enemy debuff) | Cosmic Intent / 1 |
| 05 | Light of Dead Stars | Advanced Art | Searing Starlight | +7% Afterburn (enemy debuff) | Cosmic Intent / 1 |
| 06 | Gravity Well | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 4 |
| 07 | Event Horizon | Hidden Art | Gravity Well | +1% Decrease Damage Taken (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 3 |
| 08 | Heart of the Singularity | Advanced Art | Event Horizon | +2% Decrease Damage Taken (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 3 |
| 09 | Stellar Siphon | Hidden Art | Gravity Well | +2% Lifesteal (self buff) | Cosmic Intent / 1 |
| 10 | Hunger of the Void | Advanced Art | Stellar Siphon | +3% Lifesteal (self buff); +5% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Intent / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Celestial Alignment** — When the stars fall into line, the enemy is laid bare and the ascendant burns brighter. Increase Damage Taken 35 → 37% on Cosmic Intent and Cosmic Chains (enemy, 2 rounds); Increase Damage Given 35 → 37% on Cosmic Energy (self, 2 rounds).
- **Collapsing Star** — A star does not go quietly. It folds inward and gathers everything it has for one last light. Cosmic Energy self Increase Damage Given 37 → 40% with Celestial Alignment (2 rounds, realized on the caster at cast time).
- **Supernova Unbound** — What was held inside the star is held no longer. Burst: Cosmic Explosion 50 → 52 EP (the kit's only Damage row, so a nuke extension with no in-tier effect; director review), detonated into exposure 35 → 40% on Intent and Chains (×1.075, Shakunetsu Sakura's Conflagration in Bloom anchor) and Energy's self buff 35 → 40% on the full route: ×1.40 × 1.40 × 1.40 ≈ ×2.74 on 52 EP against ≈ ×2.46 on 50 EP at base, about ×1.16.
- **Searing Starlight** — Starlight is old fire. It keeps burning long after it has arrived. Cosmic Intent Afterburn 35 → 38% (enemy, 2 rounds, range 5); every later non-pierce hit that target takes, from anyone, feeds it.
- **Light of Dead Stars** — The star is gone. Its light still reaches you, and it still burns. Burn: Cosmic Intent Afterburn 35 → 45% on the full route; for two rounds every non-pierce hit on that enemy, from anyone, adds 45% (60% per-hit cap).
- **Gravity Well** — Everything thrown at the ascendant bends, slows, and arrives lighter than it left. Decrease Damage Taken 35 → 37% on Cosmic Chains and Cosmic Energy, 30 → 32% on Cosmic Aura (self, 2 rounds); Decrease Damage Given 30 → 32% on Aura (enemy).
- **Event Horizon** — Past this line, nothing reaches the center whole. Decrease Damage Taken 37 → 38% on Chains and Energy, 32 → 33% on Aura with Gravity Well (cast-time self buffs, 2 rounds).
- **Heart of the Singularity** — At the center of the well there is only stillness. Every blow that falls in is spent before it lands. Fortress: Decrease Damage Taken 35 → 40% on Chains and Energy, 30 → 35% on Aura on the full route; each guard cast alone takes ×0.92 / ×0.93 of base, all three overlapping ×0.60 × 0.60 × 0.65 ≈ ×0.23 (base ≈ ×0.30), ×0.79 against base.
- **Stellar Siphon** — The ascendant drinks the light it tears loose. Cosmic Intent Lifesteal 40 → 42% (self, 2 rounds); shares the 60% leech budget with vamp, and pierce hits count.
- **Hunger of the Void** — The void is not empty. It is hungry, and it is patient. Drain and blunt: Cosmic Intent Lifesteal 40 → 45% (the +5% hard ceiling) and Cosmic Aura Decrease Damage Given 30 → 37% on its target, both on the full route.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Supernova Unbound (Burst) | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +2 | +5% | +2% | +5% | +2% | — | — |
| Light of Dead Stars (Burn pressure) | Celestial Alignment, Searing Starlight, Light of Dead Stars, Collapsing Star | — | +5% | — | +2% | — | +10% | — |
| Heart of the Singularity (Fortress) | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | — | +2% | +2% | +2% | +5% | — | — |
| Hunger of the Void (Drain and suppression) | Gravity Well, Event Horizon, Stellar Siphon, Hunger of the Void | — | — | +7% | — | +3% | — | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Supernova Unbound:** Collapsing Star charges Cosmic Energy's self buff to 40% and Supernova Unbound marks the enemy at 40% Increase Damage Taken on both Intent and Chains, then adds +2 Damage: a Cosmic Explosion cast once all three are live is 52 EP at ×1.40 × 1.40 × 1.40 ≈ ×2.74 (base 50 EP at ≈ ×2.46), about ×1.16 the unbuilt detonation before the bloodline passive; 52 EP is past the 50 Nuke tier (director review). Gravity Well is the fourth purchase (Decrease Damage Taken 37% / 32%, Decrease Damage Given 32%). Searing Starlight instead is the all-offense variant (Afterburn 38%; Explosion ×1.19, the caster's other hits ×1.14).
- **Light of Dead Stars:** One Cosmic Intent cast sets Afterburn to 45% for two rounds, so every non-pierce hit that enemy takes, from the caster or allies, adds 45% inside the 60% per-hit cap; Afterburn reads the hit after Intent's own 37% exposure (×1.37 × 1.45 ≈ ×1.99 per hit, base ≈ ×1.82). Collapsing Star is the offensive fourth: the caster's own hits gain Energy's 40% self buff. Gravity Well instead buys +2% Decrease Damage Taken and Decrease Damage Given.
- **Heart of the Singularity:** Decrease Damage Taken reaches 40% on Chains and Energy and 35% on Aura: three 40 AP casts whose self buffs are live the two rounds after each cast, so staggered casts cover six rounds in seven; each alone takes ×0.92 / ×0.93 of base, and all three overlapping (two casts fit one 100 AP round) take ≈ ×0.23 (base ≈ ×0.30), ×0.77 against base with Gravity Well's Decrease Damage Given. Celestial Alignment is the fourth purchase (exposure and Energy's self buff 37%). Stellar Siphon instead adds Lifesteal 42%.
- **Hunger of the Void:** Cosmic Intent's Lifesteal reaches 45% (fifteen points under the 60% budget shared with vamp) on every hit the caster lands in its two rounds, pierce included, and Cosmic Aura's target deals ×0.63 instead of ×0.70 for two rounds, to the caster and allies alike. Event Horizon is the fourth purchase (Decrease Damage Taken 38% / 33%). Celestial Alignment instead adds +2% exposure and self buff.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Drain and suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Cosmic Intent | 0 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Cosmic Intent | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Cosmic Intent | 2 | Lifesteal | self | 40% | 40% | 40% | 40% | 45% (+5) |
| Cosmic Explosion | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Cosmic Explosion | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Cosmic Chains | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 40% (+5) | 38% (+3) |
| Cosmic Chains | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Cosmic Energy | 0 | Increase Damage Given | self | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 35% |
| Cosmic Energy | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 40% (+5) | 38% (+3) |
| Cosmic Energy | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Cosmic Aura | 0 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 32% (+2) | 37% (+7) |
| Cosmic Aura | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 35% (+5) | 33% (+3) |
| Cosmic Aura | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +7% Decrease Damage Given, +5% Increase Damage Taken, +5% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Supernova Unbound: +5% Increase Damage Taken (2 + 0 + 3; on band)
  - Route Light of Dead Stars: +10% Afterburn (0 + 3 + 7; on band)
  - Route Heart of the Singularity: +5% Decrease Damage Taken (2 + 1 + 2; on band)
  - Route Hunger of the Void: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 10 (AB 1, DMG 1, DDG 1, DDT 3, IDG 1, IDT 2, LS 1)
- Strongest full build by row-weighted total: Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well (raw +16, row-weighted 25)
- Lowest row-weighted node: Stellar Siphon (2)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Cosmic Explosion 50 -> 52
- classification status: requires classification extension (director decision)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Cosmic Explosion | 0 | 50 (Nuke) | **52 (above Nuke)** |

Above-Nuke rationale: Fable proposal following the director precedent of RUL-2026-10-04-001 (Blood-Enchanted Eyes, Reaper's Embrace 50 → 52) and RUL-2026-10-04-002 (Shakunetsu Sakura, Sakura-ame 50 → 52). Kit fact (R1′): the dossier Traits read Burst, Defensive, and Cosmic Explosion is the kit's signature finisher: its only Damage row and its only 60 AP cast (cooldown 7, range 4). Supernova Unbound's +2 Damage is the controlled payoff of Collapsing Star's self Increase Damage Given setup and lifts Explosion 50 → 52, past the 50 Nuke tier. Because Explosion is the kit's only Damage row, the route has no in-tier Damage effect: the +2 is purely a nuke extension. Supernova Unbound is the tree's only Damage node, so no legal allocation adds more than +2 and none without it exceeds 50. Pending director review (DQ-A).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Supernova Unbound | +2 Damage, +5% IDG, +5% IDT | Searing Starlight | +2 Damage, +5% IDG, +5% IDT, +3% AB | 20 |
| Supernova Unbound | +2 Damage, +5% IDG, +5% IDT | Gravity Well *(highest diagnostic)* | +2 Damage, +5% IDG, +2% DDG, +5% IDT, +2% DDT | 25 |
| Light of Dead Stars | +2% IDG, +2% IDT, +10% AB | Collapsing Star | +5% IDG, +2% IDT, +10% AB | 19 |
| Light of Dead Stars | +2% IDG, +2% IDT, +10% AB | Gravity Well *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +10% AB | 24 |
| Heart of the Singularity | +2% DDG, +5% DDT | Celestial Alignment *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +5% DDT | 23 |
| Heart of the Singularity | +2% DDG, +5% DDT | Stellar Siphon | +2% DDG, +5% DDT, +2% LS | 19 |
| Hunger of the Void | +7% DDG, +2% DDT, +5% LS | Celestial Alignment *(highest diagnostic)* | +2% IDG, +7% DDG, +2% IDT, +2% DDT, +5% LS | 24 |
| Hunger of the Void | +7% DDG, +2% DDT, +5% LS | Event Horizon | +7% DDG, +3% DDT, +5% LS | 21 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Celestial Alignment, Collapsing Star, Supernova Unbound, Searing Starlight | +2 Damage, +5% IDG, +5% IDT, +3% AB |
| 2 | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +2 Damage, +5% IDG, +2% DDG, +5% IDT, +2% DDT |
| 3 | Celestial Alignment, Collapsing Star, Searing Starlight, Light of Dead Stars | +5% IDG, +2% IDT, +10% AB |
| 4 | Celestial Alignment, Collapsing Star, Searing Starlight, Gravity Well | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Celestial Alignment, Collapsing Star, Gravity Well, Event Horizon | +5% IDG, +2% DDG, +2% IDT, +3% DDT |
| 6 | Celestial Alignment, Collapsing Star, Gravity Well, Stellar Siphon | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +10% AB |
| 8 | Celestial Alignment, Searing Starlight, Gravity Well, Event Horizon | +2% IDG, +2% DDG, +2% IDT, +3% DDT, +3% AB |
| 9 | Celestial Alignment, Searing Starlight, Gravity Well, Stellar Siphon | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB, +2% LS |
| 10 | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 11 | Celestial Alignment, Gravity Well, Event Horizon, Stellar Siphon | +2% IDG, +2% DDG, +2% IDT, +3% DDT, +2% LS |
| 12 | Celestial Alignment, Gravity Well, Stellar Siphon, Hunger of the Void | +2% IDG, +7% DDG, +2% IDT, +2% DDT, +5% LS |
| 13 | Gravity Well, Event Horizon, Heart of the Singularity, Stellar Siphon | +2% DDG, +5% DDT, +2% LS |
| 14 | Gravity Well, Event Horizon, Stellar Siphon, Hunger of the Void | +7% DDG, +3% DDT, +5% LS |

## Design notes

- 2026-10-04 rebalance, R1′: the dossier Traits include Burst and Cosmic Explosion is the kit's only Damage row and only 60 AP cast, so the Burst route keeps the director pattern: Collapsing Star's +3% self Increase Damage Given is the percentage setup and Supernova Unbound pays off with a controlled +2 Damage (Explosion 50 → 52; above_nuke_rationale), a nuke extension with no in-tier Damage effect. The first pass's capstone was +3% Increase Damage Taken / +3% Increase Damage Given; against it, Explosion ×1.14 → ×1.16 against base, the caster's other hits ×1.14 → ×1.12, allies' hits ×1.08 unchanged.
- The setup is self amplification, not Blood-Enchanted Eyes' +3% Increase Damage Taken: an exposure Hidden Art would be Light of Dead Stars' natural fourth and put 40% exposure under the 45% burn on the same Intent mark. Collapsing Star as Light's fourth adds only the caster's Energy buff.
- Light of Dead Stars dropped its pre-batch +3% Increase Damage Taken: on the same Intent cast as the burn it compounded (×1.40 × 1.45), which made the burn route the strongest offense for the caster and the party. Heart of the Singularity dropped its +3% Increase Damage Given, which overlapped Burst.
- Fortress (R3): Event Horizon +1% and Heart of the Singularity +2% hold the route at +5% Decrease Damage Taken on three compounding guard rows, because two 40 AP guard casts fit one 100 AP round and the three rows overlap whenever the player wants. All three live: ≈ ×0.23 (base ≈ ×0.30), ×0.79 against base (×0.77 with Gravity Well's Decrease Damage Given), lighter than Blood-Enchanted Eyes' Deathless Vitality route (×0.747). The cut sits on Event Horizon rather than the capstone: at Event Horizon +2% / Heart +1%, Hunger of the Void with Event Horizon would take ×0.75 against the Fortress package's ×0.77 with every row live and leech more.
- Hunger of the Void keeps the pre-batch +5% Decrease Damage Given (route 30 → 37% on one Aura row) beside Lifesteal at the +5% hard ceiling: one Aura cast makes its target deal ×0.90 to the caster and allies for two rounds of seven.
- Maxima over every legal allocation: Damage +2 (Cosmic Explosion 50 → 52, only with Supernova Unbound), Increase Damage Taken +5%, Increase Damage Given +5%, Afterburn +10%, Decrease Damage Taken +5%, Decrease Damage Given +7%, Lifesteal +5%.
- Top offensive package (Increase Damage Given × Increase Damage Taken, all windows live): Collapsing Star + Supernova Unbound ×1.115 (exposure ×1.075 × self buff ×1.037), under Blood-Enchanted Eyes' ×1.234. Offense trade (per-row arithmetic, not simulation, against base with Intent, Chains and Energy live): Supernova Unbound ×1.16 on Cosmic Explosion, ×1.12 on the caster's other hits and ×1.08 on allies'; Light of Dead Stars ×1.12 on every caster hit and ×1.11 on allies'. With their offensive fourths (Searing Starlight; Collapsing Star): Explosion ×1.19, other hits ×1.14, allies ×1.10 against ×1.15 / ×1.11. Burst wins the detonation; the burn wins every other hit and the party's.
- Trade diagnostic (offence × 1/incoming against base on the caster's general hits, with all four setup casts live / averaged over single-cast states; per-row arithmetic, Lifesteal and the +2 Damage not counted): Fortress + Celestial Alignment 1.36 / 1.08, Hunger + Event Horizon 1.28 / 1.06, Light of Dead Stars + Gravity Well 1.27 / 1.06, Supernova + Gravity Well 1.26 / 1.06; all-offense Light + Collapsing Star 1.15 / 1.04, Supernova + Searing Starlight 1.14 / 1.03.
- Delivery: every jutsu has cooldown 7 and costs 40 AP except Cosmic Explosion (60 AP, range 4); every buff/debuff row is live the two rounds after its cast. Cosmic Energy's Increase Damage Given and Decrease Damage Taken are SELF rows realized on the caster at cast time, wherever the circle is placed.

## Risks and unproven interactions

- Classification: no kit row carries an element, so 'Cosmic Ascendant' is the placeholder name of a new jutsu classification (requires classification extension), not a bloodline-id selector. All five kit jutsu qualify only through that authored classification (ENGINE_GAP_REGISTER G1); targeting None instead would reach every non-elemental row. Off-kit coverage is unverified.
- Damage: Supernova Unbound lifts Cosmic Explosion to 52 EP, past the 50 Nuke tier (director review). It is one single-target 60 AP cast on a 7-round cooldown; its Wound row is unsupported and unchanged.
- Exposure and Afterburn are party-wide: both Increase Damage Taken rows and the Afterburn row list all four stat types with no element, so they match every non-pierce hit the marked enemy takes from anyone. Afterburn reads the hit after Increase Damage Taken, so the two multiply; its 60% per-hit cap is shared with other Afterburn sources. Not simulated.
- Lifesteal tops out at 45%, fifteen points under the 60% leech budget shared with vamp; it includes pierce, needs both combatants alive and is blocked by healprevent.
- Targeting: Chains, Aura and Intent are OTHER_USER casts; aimed at an ally, their exposure, burn or Decrease Damage Given lands on that ally (§3b). Cosmic Energy's unsupported move row is an INHERIT ground effect (enemy hazard), unchanged.
- Stacking: same-tag rows all apply and compound. All three Decrease Damage Taken rows live at the route maximum give ≈ ×0.23, under the 90% reduction cap. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Cosmic Ascendant-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

