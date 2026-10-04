# Cosmic Ascendant — Weight of the Stars

**Bloodline:** Cosmic Ascendant (BR-018, rank S, `osVXxtyW61gr-bx5v5ys2`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Cosmic Ascendant classification / forked tree · **Classification:** Cosmic Ascendant (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Burst from multipliers, not flat Damage: Increase Damage Taken on Cosmic Intent and Cosmic Chains (+5%) and Increase Damage Given on Cosmic Energy (+8%) build the window a 50 EP Cosmic Explosion lands into · secondary Defense: a Decrease Damage Taken fortress on three casts (+7%), or Lifesteal (+5%) with Decrease Damage Given suppression on Cosmic Aura (+7%) · tertiary Cosmic Intent's Afterburn (+10%) as one-cast, party-wide pressure on the marked enemy.

Cosmic Ascendant is a rank S Burst/Defensive kit with 10 supported rows on five cooldown-7 jutsu. Its only Damage row is Cosmic Explosion at 50 EP, the Nuke tier, so the tree leaves Damage unamplified and builds burst from the kit's compounding multipliers. Celestial Alignment answers "How do I make the enemy I mark fall faster?": Supernova Unbound charges the caster and opens both marks for one detonation window, while Light of Dead Stars makes every hit on Cosmic Intent's target burn. Gravity Well answers "How do I outlast the exchange: harden myself, or drain and blunt them?": Heart of the Singularity raises Decrease Damage Taken on all three guard casts, and Hunger of the Void leeches from Intent while Cosmic Aura blunts its target.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Celestial Alignment | Foundation | How do I make the enemy I mark fall faster? |
| Gravity Well | Foundation | How do I outlast the exchange: harden myself, or drain and blunt them? |
| Supernova Unbound | Advanced Art | burst: charge yourself, open both marks, detonate into the window |
| Light of Dead Stars | Advanced Art | pressure: one Intent cast makes every hit on the mark burn, party-wide |
| Heart of the Singularity | Advanced Art | fortress: all three guard casts |
| Hunger of the Void | Advanced Art | drain and suppression: leech from your hits while Aura blunts theirs |

- Concern: No flat Damage on a Burst-trait kit: Cosmic Explosion (50 EP) is the only Damage row, so any Damage bonus would pass the Nuke tier; Burst is built from multipliers instead. For reference only, the Blood-Enchanted Eyes pattern (+2 Damage) would give Explosion 50 → 52 and need an above_nuke_rationale; it is not proposed.
- Concern: The Fortress still leads the mitigation diagnostic (1.50 / 1.11 against 1.34 / 1.08 for Hunger + Event Horizon); that is its identity, and Hunger's Lifesteal is not counted. Not simulated.
- Concern: Gravity Well (+2% Decrease Damage Taken on three rows) is the strongest fourth for both offensive capstones (Supernova + Gravity Well 1.29 against 1.16 with Searing Starlight); it is a defensive hedge that adds no offense, not a stacked payoff.
- Concern: Burst beats the burn on the caster's own hits only with both marks live; with Intent's mark and Energy's buff but no Chains, the burn is ahead (×1.11 against ×1.10).
- Concern: The 'Cosmic Ascendant' classification extension remains a director/engine decision; off-kit coverage is unverified.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Cosmic Ascendant-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Celestial Alignment | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Cosmic Chains, Cosmic Energy, Cosmic Intent / 3 |
| 02 | Collapsing Star | Hidden Art | Celestial Alignment | +3% Increase Damage Given (self buff) | Cosmic Energy / 1 |
| 03 | Supernova Unbound | Advanced Art | Collapsing Star | +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Cosmic Chains, Cosmic Energy, Cosmic Intent / 3 |
| 04 | Searing Starlight | Hidden Art | Celestial Alignment | +3% Afterburn (enemy debuff) | Cosmic Intent / 1 |
| 05 | Light of Dead Stars | Advanced Art | Searing Starlight | +7% Afterburn (enemy debuff) | Cosmic Intent / 1 |
| 06 | Gravity Well | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 4 |
| 07 | Event Horizon | Hidden Art | Gravity Well | +2% Decrease Damage Taken (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 3 |
| 08 | Heart of the Singularity | Advanced Art | Event Horizon | +3% Decrease Damage Taken (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 3 |
| 09 | Stellar Siphon | Hidden Art | Gravity Well | +2% Lifesteal (self buff) | Cosmic Intent / 1 |
| 10 | Hunger of the Void | Advanced Art | Stellar Siphon | +3% Lifesteal (self buff); +5% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Intent / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Celestial Alignment** — When the stars fall into line, the enemy is laid bare and the ascendant burns brighter. Increase Damage Taken 35 → 37% on Cosmic Intent and Cosmic Chains (enemy, 2 rounds); Increase Damage Given 35 → 37% on Cosmic Energy (self, 2 rounds).
- **Collapsing Star** — A star does not go quietly. It folds inward and gathers everything it has for one last light. Cosmic Energy self Increase Damage Given 37 → 40% with Celestial Alignment (2 rounds, realized on the caster at cast time).
- **Supernova Unbound** — What was held inside the star is held no longer. Burst window: exposure 35 → 40% on Intent and Chains and Energy's self buff 35 → 43% on the full route; Cosmic Explosion stays 50 EP and lands at ×1.40 × 1.40 × 1.43 ≈ ×2.80 into the full setup (base ≈ ×2.46).
- **Searing Starlight** — Starlight is old fire. It keeps burning long after it has arrived. Cosmic Intent Afterburn 35 → 38% (enemy, 2 rounds, range 5); every later non-pierce hit that target takes, from anyone, feeds it.
- **Light of Dead Stars** — The star is gone. Its light still reaches you, and it still burns. Burn: Cosmic Intent Afterburn 35 → 45% on the full route; for two rounds every non-pierce hit on that enemy, from anyone, adds 45% (60% per-hit cap).
- **Gravity Well** — Everything thrown at the ascendant bends, slows, and arrives lighter than it left. Decrease Damage Taken 35 → 37% on Cosmic Chains and Cosmic Energy, 30 → 32% on Cosmic Aura (self, 2 rounds); Decrease Damage Given 30 → 32% on Aura (enemy).
- **Event Horizon** — Past this line, nothing reaches the center whole. Decrease Damage Taken 37 → 39% on Chains and Energy, 32 → 34% on Aura with Gravity Well (cast-time self buffs, 2 rounds).
- **Heart of the Singularity** — At the center of the well there is only stillness. Every blow that falls in is spent before it lands. Fortress: Decrease Damage Taken 35 → 42% on Chains and Energy, 30 → 37% on Aura on the full route; each guard cast alone takes ×0.89 / ×0.90 of base, all three overlapping ×0.58 × 0.58 × 0.63 ≈ ×0.21 (base ≈ ×0.30).
- **Stellar Siphon** — The ascendant drinks the light it tears loose. Cosmic Intent Lifesteal 40 → 42% (self, 2 rounds); shares the 60% leech budget with vamp, and pierce hits count.
- **Hunger of the Void** — The void is not empty. It is hungry, and it is patient. Drain and blunt: Cosmic Intent Lifesteal 40 → 45% (the +5% hard ceiling) and Cosmic Aura Decrease Damage Given 30 → 37% on its target, both on the full route.

## Complete four-purchase examples

| Build | Purchases | IDG | DDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Supernova Unbound (Burst) | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +8% | +2% | +5% | +2% | — | — |
| Light of Dead Stars (Burn pressure) | Celestial Alignment, Searing Starlight, Light of Dead Stars, Collapsing Star | +5% | — | +2% | — | +10% | — |
| Heart of the Singularity (Fortress) | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | +2% | +2% | +2% | +7% | — | — |
| Hunger of the Void (Drain and suppression) | Gravity Well, Event Horizon, Stellar Siphon, Hunger of the Void | — | +7% | — | +4% | — | +5% |

Abbreviations: IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Supernova Unbound:** Intent and Chains each mark the enemy at 40% Increase Damage Taken and Cosmic Energy's self buff reaches 43%, so a Cosmic Explosion cast once all three are live hits at ×1.40 × 1.40 × 1.43 ≈ ×2.80 (base ≈ ×2.46) before the bloodline passive; its 50 EP is unchanged. Gravity Well is the fourth purchase (Decrease Damage Taken 37% / 32%, Decrease Damage Given 32%). Searing Starlight instead is the all-offense variant (Afterburn 38%).
- **Light of Dead Stars:** One Cosmic Intent cast sets Afterburn to 45% for two rounds, so every non-pierce hit that enemy takes, from the caster or allies, adds 45% inside the 60% per-hit cap; Afterburn reads the hit after Intent's own 37% exposure (×1.37 × 1.45 ≈ ×1.99 per hit, base ≈ ×1.82). Collapsing Star is the offensive fourth: the caster's own hits gain Energy's 40% self buff. Gravity Well instead buys +2% Decrease Damage Taken and Decrease Damage Given.
- **Heart of the Singularity:** Decrease Damage Taken reaches 42% on Chains and Energy and 37% on Aura: three 40 AP casts whose self buffs are live the two rounds after each cast, so staggered casts cover six rounds in seven; each alone takes ×0.89 / ×0.90 of base and all three overlapping take ≈ ×0.21 (base ≈ ×0.30). Celestial Alignment is the fourth purchase (exposure and Energy's self buff 37%). Stellar Siphon instead adds Lifesteal 42%.
- **Hunger of the Void:** Cosmic Intent's Lifesteal reaches 45% (fifteen points under the 60% budget shared with vamp) on every hit the caster lands in its two rounds, pierce included, and Cosmic Aura's target deals ×0.63 instead of ×0.70 for two rounds, to the caster and allies alike. Event Horizon is the fourth purchase (Decrease Damage Taken 39% / 34%). Celestial Alignment instead adds +2% exposure and self buff.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Drain and suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Cosmic Intent | 0 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Cosmic Intent | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Cosmic Intent | 2 | Lifesteal | self | 40% | 40% | 40% | 40% | 45% (+5) |
| Cosmic Explosion | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Cosmic Explosion | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Cosmic Chains | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 42% (+7) | 39% (+4) |
| Cosmic Chains | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Cosmic Energy | 0 | Increase Damage Given | self | 35% | 43% (+8) | 40% (+5) | 37% (+2) | 35% |
| Cosmic Energy | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 42% (+7) | 39% (+4) |
| Cosmic Energy | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Cosmic Aura | 0 | Decrease Damage Given | enemy | 30% | 32% (+2) | 30% | 32% (+2) | 37% (+7) |
| Cosmic Aura | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 30% | 37% (+7) | 34% (+4) |
| Cosmic Aura | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +7% Decrease Damage Given, +5% Increase Damage Taken, +7% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Supernova Unbound: +5% Increase Damage Taken (2 + 0 + 3; on band)
  - Route Light of Dead Stars: +10% Afterburn (0 + 3 + 7; on band)
  - Route Heart of the Singularity: +7% Decrease Damage Taken (2 + 2 + 3; off band)
  - Route Hunger of the Void: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 10 (AB 1, DMG 1, DDG 1, DDT 3, IDG 1, IDT 2, LS 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity (raw +13, row-weighted 29)
- Lowest row-weighted node: Stellar Siphon (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Cosmic Explosion 50 (Nuke)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Supernova Unbound | +8% IDG, +5% IDT | Searing Starlight | +8% IDG, +5% IDT, +3% AB | 21 |
| Supernova Unbound | +8% IDG, +5% IDT | Gravity Well *(highest diagnostic)* | +8% IDG, +2% DDG, +5% IDT, +2% DDT | 26 |
| Light of Dead Stars | +2% IDG, +2% IDT, +10% AB | Collapsing Star | +5% IDG, +2% IDT, +10% AB | 19 |
| Light of Dead Stars | +2% IDG, +2% IDT, +10% AB | Gravity Well *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +10% AB | 24 |
| Heart of the Singularity | +2% DDG, +7% DDT | Celestial Alignment *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +7% DDT | 29 |
| Heart of the Singularity | +2% DDG, +7% DDT | Stellar Siphon | +2% DDG, +7% DDT, +2% LS | 25 |
| Hunger of the Void | +7% DDG, +2% DDT, +5% LS | Celestial Alignment *(highest diagnostic)* | +2% IDG, +7% DDG, +2% IDT, +2% DDT, +5% LS | 24 |
| Hunger of the Void | +7% DDG, +2% DDT, +5% LS | Event Horizon | +7% DDG, +4% DDT, +5% LS | 24 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Celestial Alignment, Collapsing Star, Supernova Unbound, Searing Starlight | +8% IDG, +5% IDT, +3% AB |
| 2 | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +8% IDG, +2% DDG, +5% IDT, +2% DDT |
| 3 | Celestial Alignment, Collapsing Star, Searing Starlight, Light of Dead Stars | +5% IDG, +2% IDT, +10% AB |
| 4 | Celestial Alignment, Collapsing Star, Searing Starlight, Gravity Well | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Celestial Alignment, Collapsing Star, Gravity Well, Event Horizon | +5% IDG, +2% DDG, +2% IDT, +4% DDT |
| 6 | Celestial Alignment, Collapsing Star, Gravity Well, Stellar Siphon | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +10% AB |
| 8 | Celestial Alignment, Searing Starlight, Gravity Well, Event Horizon | +2% IDG, +2% DDG, +2% IDT, +4% DDT, +3% AB |
| 9 | Celestial Alignment, Searing Starlight, Gravity Well, Stellar Siphon | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB, +2% LS |
| 10 | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | +2% IDG, +2% DDG, +2% IDT, +7% DDT |
| 11 | Celestial Alignment, Gravity Well, Event Horizon, Stellar Siphon | +2% IDG, +2% DDG, +2% IDT, +4% DDT, +2% LS |
| 12 | Celestial Alignment, Gravity Well, Stellar Siphon, Hunger of the Void | +2% IDG, +7% DDG, +2% IDT, +2% DDT, +5% LS |
| 13 | Gravity Well, Event Horizon, Heart of the Singularity, Stellar Siphon | +2% DDG, +7% DDT, +2% LS |
| 14 | Gravity Well, Event Horizon, Stellar Siphon, Hunger of the Void | +7% DDG, +4% DDT, +5% LS |

## Design notes

- 2026-10-04 rebalance: flat Damage removed. Collapsing Star +2 and Supernova Unbound +3 lifted Cosmic Explosion 50 → 52 / 55, past the Nuke tier. Burst now sets up self-amplification on the Hidden Art (Collapsing Star +3% Increase Damage Given) and pays off with exposure (Supernova Unbound +3% Increase Damage Taken, +3% Increase Damage Given).
- Light of Dead Stars dropped its +3% Increase Damage Taken: on the same Intent cast as the burn it compounded (×1.40 × 1.45), which made the old burn route the strongest offense for the caster and the party. Heart of the Singularity dropped its +3% Increase Damage Given, which overlapped Burst.
- Fortress cut after review: Event Horizon +3% → +2% and Heart of the Singularity +5% → +3% Decrease Damage Taken (route +10% → +7%). At +10% the three compounding guard rows reached ≈ ×0.18 together (×0.61 against base) and the Fortress led every route by a wide margin; at +7% they reach ≈ ×0.21 (×0.72 against base, ×0.70 with Gravity Well's Decrease Damage Given), under Blood-Enchanted Eyes' two-row fortress package (≈ ×0.75 Decrease Damage Taken, ≈ ×0.64 with its Decrease Damage Given).
- Hunger of the Void's Decrease Damage Given is back to +5% (route 30 → 37% on one Aura row): the batch's +8% only kept pace with the old Fortress. One Aura cast makes its target deal ×0.90 to the caster and allies for two rounds of seven, beside Lifesteal at the +5% hard ceiling.
- Maxima over every legal allocation: Increase Damage Taken +5%, Increase Damage Given +8%, Afterburn +10%, Decrease Damage Taken +7%, Decrease Damage Given +7%, Lifesteal +5%; Damage is not targeted.
- Offense trade (per-row arithmetic, not simulation, against base with Intent, Chains and Energy live): Supernova Unbound ×1.14 on the caster's hits and ×1.08 on allies'; Light of Dead Stars ×1.12 and ×1.11. With their offensive fourths (Searing Starlight; Collapsing Star): ×1.16 / ×1.10 against ×1.15 / ×1.11. Burst wins the caster's window, burn wins the party's.
- Trade diagnostic (offence × 1/incoming against base, with all four setup casts live / averaged over single-cast states; per-row arithmetic, Lifesteal not counted): Fortress + Celestial Alignment 1.50 / 1.11, Hunger + Event Horizon 1.34 / 1.08, Supernova + Gravity Well 1.29 / 1.06, Light of Dead Stars + Gravity Well 1.27 / 1.06; all-offense Supernova + Searing Starlight 1.16 / 1.04. Before the cut the Fortress read 1.75 / 1.15.
- Delivery: every jutsu has cooldown 7 and costs 40 AP except Cosmic Explosion (60 AP, range 4); every buff/debuff row is live the two rounds after its cast. Cosmic Energy's Increase Damage Given and Decrease Damage Taken are SELF rows realized on the caster at cast time, wherever the circle is placed.

## Risks and unproven interactions

- Classification: no kit row carries an element, so 'Cosmic Ascendant' is the placeholder name of a new jutsu classification (requires classification extension), not a bloodline-id selector. All five kit jutsu qualify only through that authored classification (ENGINE_GAP_REGISTER G1); targeting None instead would reach every non-elemental row. Off-kit coverage is unverified.
- Exposure and Afterburn are party-wide: both Increase Damage Taken rows and the Afterburn row list all four stat types with no element, so they match every non-pierce hit the marked enemy takes from anyone. Afterburn reads the hit after Increase Damage Taken, so the two multiply; its 60% per-hit cap is shared with other Afterburn sources. Not simulated.
- Lifesteal tops out at 45%, fifteen points under the 60% leech budget shared with vamp; it includes pierce, needs both combatants alive and is blocked by healprevent.
- Targeting: Chains, Aura and Intent are OTHER_USER casts; aimed at an ally, their exposure, burn or Decrease Damage Given lands on that ally (§3b). Cosmic Energy's unsupported move row is an INHERIT ground effect (enemy hazard), unchanged.
- Stacking: same-tag rows all apply and compound. All three Decrease Damage Taken rows live at the route maximum give ≈ ×0.21, under the 90% reduction cap. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

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

