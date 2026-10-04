# Ancient Tailed Demon — Rites of the Sealed

**Bloodline:** Ancient Tailed Demon (BR-004, rank B, `Au5rBnnukEqUv_lRrk1yO`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Ancient Tailed Demon classification / forked tree · **Classification:** Ancient Tailed Demon (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary The host (Demon's Marrow): a sustained rampage or a fortress, both on Demonic Vitae · secondary The marked prey (Demon's Grasp): Demonic Embrace's exposure and Afterburn, cashed in as a Roar burst or a burn · tertiary Ancient Demon Roar Damage as Howl of Annihilation's controlled +2 payoff (45 → 47, High tier kept) after an exposure setup.

Three casts, one supported row per tag. Demonic Embrace's Afterburn (35%) and Increase Damage Taken (35%) share one target and one 2-round window; Demon's Grasp raises both, then one route deepens the exposure and cashes it in through Ancient Demon Roar's single 45 EP row (+2 on every enemy in the circle, High tier kept) and the other deepens the burn. Demonic Vitae carries the two self buffs (Increase Damage Given 35% for 3 rounds, Decrease Damage Taken 25% for 2), which split into a sustained rampage and a fortress.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Demon's Grasp | Foundation | How do I make the demon's mark pay: open the prey for the Roar, or burn it down? |
| Demon's Marrow | Foundation | How do I strengthen the host: hit everything harder or refuse to fall? |
| Howl of Annihilation | Advanced Art | burst: exposure set up on the mark, controlled +2 Damage payoff on Roar's whole circle |
| Consuming Malice | Advanced Art | burn on the marked prey: one target takes 45% Afterburn on every instant hit, allies' included |
| Unyielding Husk | Advanced Art | fortress |
| Primordial Rampage | Advanced Art | sustained amplification: every own hit on any target harder for 3 rounds |

**Director review recommended:** Roster questions: DQ-B (Howl of Annihilation +7% Increase Damage Taken on one row, Demonic Embrace 35 → 42%, ×1.052).

- Concern: Rending Grip (+2% exposure) and Festering Brand (+3% Afterburn) both raise what Embrace's target takes, so at the Hidden tier they read alike; they differ in mechanics (exposure also multiplies residual ticks and the hit Afterburn reads; Afterburn skips pierce and shares a 60% per-hit cap) and in the payoff each leads to.
- Concern: Howl of Annihilation is the narrowest route in 1v1: its +2 lands on one 60 AP cast per 7 rounds and it trails Consuming Malice by ≈ 2.1% on every hit the mark takes. It leads Malice when several enemies stand in Roar's circle (+4.4% on each other enemy) and leads Primordial Rampage on allies' hits on the mark (≈ ×1.95 against ×1.88). Not simulated.
- Concern: Cross-route stack: Rending Grip is a legal fourth for Consuming Malice and Festering Brand for Howl, so one 40 AP Embrace cast reaches exposure 39% / Afterburn 45% (≈ ×2.02 on the mark, party-wide) or 42% / 40% (≈ ×1.99); with Malice held exposure stays at +4% (×1.030), inside the roster's ≤ +5% beside an Afterburn capstone. No non-twin setup exists: the kit has one supported row per tag, the other three percentage tags each own a Hidden Art, and flat Damage belongs on the payoff. An Afterburn setup would twin Festering Brand and push Malice past +10%; a self Increase Damage Given setup would twin Boiling Ichor, put a host buff under the mark's Foundation and pull Howl toward Primordial Rampage's Vitae amplification; Decrease Damage Taken would twin Scarred Hide and sets up no burst. Neither stack is dominant: on the caster's hits Malice + Demon's Marrow ties Malice + Rending Grip (≈ ×1.37 × 1.37 × 1.45 ≈ ×2.72 against ×1.35 × 1.39 × 1.45 ≈ ×2.72), so Grip leads only on allies' hits (≈ ×2.02 against ×1.99) and gives up Vitae's +2% / +2%; Howl + Festering Brand likewise trades them for allies' hits on the mark (≈ ×1.99 against ×1.95).
- Concern: Classification extension ('Ancient Tailed Demon' jutsu classification) remains a director/engine decision.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ancient Tailed Demon-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Demon's Grasp | Foundation | None | +2% Afterburn (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Demonic Embrace / 2 |
| 02 | Rending Grip | Hidden Art | Demon's Grasp | +2% Increase Damage Taken (enemy debuff) | Demonic Embrace / 1 |
| 03 | Howl of Annihilation | Advanced Art | Rending Grip | +3% Increase Damage Taken (enemy debuff); +2 Damage (damage) | Ancient Demon Roar, Demonic Embrace / 2 |
| 04 | Festering Brand | Hidden Art | Demon's Grasp | +3% Afterburn (enemy debuff) | Demonic Embrace / 1 |
| 05 | Consuming Malice | Advanced Art | Festering Brand | +5% Afterburn (enemy debuff) | Demonic Embrace / 1 |
| 06 | Demon's Marrow | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Demonic Vitae / 2 |
| 07 | Scarred Hide | Hidden Art | Demon's Marrow | +3% Decrease Damage Taken (self buff) | Demonic Vitae / 1 |
| 08 | Unyielding Husk | Advanced Art | Scarred Hide | +5% Decrease Damage Taken (self buff) | Demonic Vitae / 1 |
| 09 | Boiling Ichor | Hidden Art | Demon's Marrow | +2% Increase Damage Given (self buff) | Demonic Vitae / 1 |
| 10 | Primordial Rampage | Advanced Art | Boiling Ichor | +4% Increase Damage Given (self buff) | Demonic Vitae / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Demon's Grasp** — A claw closes around the prey, and what it touches begins to smoulder. Demonic Embrace only: Afterburn 35 → 37% and exposure 35 → 37% on one target for 2 rounds (40 AP, range 4, cooldown 7).
- **Rending Grip** — The claw does not merely hold the prey; it tears it open for what comes next. Demonic Embrace exposure 39% with Demon's Grasp (one target, 2 rounds): the setup for an Ancient Demon Roar cast the round after.
- **Howl of Annihilation** — One breath, and the field remembers why the ancients sealed it away. Exposure into burst: on the full route Demonic Embrace exposure 35 → 42% (+7% on one row, ×1.052 on the mark, under Shakunetsu Sakura's ×1.075) and Ancient Demon Roar 45 → 47 EP on every enemy in its circle (High tier kept).
- **Festering Brand** — Flesh the demon marks does not stop burning when the claw lets go. Demonic Embrace Afterburn 40% with Demon's Grasp: for 2 rounds the marked target takes 40% extra from each instant non-pierce hit, allies' included.
- **Consuming Malice** — Hatred older than the villages, poured into a single victim. Burn: on the full route Demonic Embrace Afterburn 35 → 45% (+10%, below the 60% per-hit cap) with exposure 37%, so each instant non-pierce hit on the target is worth ≈ ×1.37 × 1.45 ≈ ×1.99 (×1.82 unmodified), allies' included, for 2 rounds.
- **Demon's Marrow** — The blood runs black and hot, and the host grows harder to kill. Demonic Vitae only (self, 40 AP, cooldown 7): Increase Damage Given 35 → 37% for 3 rounds, Decrease Damage Taken 25 → 27% for 2; neither touches pierce hits.
- **Scarred Hide** — A thousand years of wounds, and every one of them closed over. Demonic Vitae Decrease Damage Taken 30% with Demon's Marrow, for 2 rounds (non-pierce hits of any stat type).
- **Unyielding Husk** — What the host cannot dodge, the demon simply refuses to feel. Fortress: Decrease Damage Taken route total +10%, Demonic Vitae 25 → 35% for 2 rounds (damage taken ×0.75 → ×0.65). Pierce still passes through.
- **Boiling Ichor** — Let a little more of it loose, and every strike carries the heat. Demonic Vitae Increase Damage Given 39% with Demon's Marrow, for 3 rounds, on all your non-pierce damage (jutsu, weapons, basics).
- **Primordial Rampage** — The seal holds, barely. Everything within reach learns what that costs. Sustained amplification: Demonic Vitae Increase Damage Given 35 → 43% (route +8%) for 3 rounds on every non-pierce hit you land on any target (Roar 45 EP ≈ ×1.43 on its whole circle).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Howl of Annihilation (Exposure into burst) | Demon's Grasp, Rending Grip, Howl of Annihilation, Demon's Marrow | +2 | +2% | +7% | +2% | +2% |
| Consuming Malice (Burn) | Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow | — | +2% | +2% | +2% | +10% |
| Unyielding Husk (Fortress) | Demon's Grasp, Demon's Marrow, Scarred Hide, Unyielding Husk | — | +2% | +2% | +10% | +2% |
| Primordial Rampage (Sustained amplification) | Demon's Grasp, Demon's Marrow, Boiling Ichor, Primordial Rampage | — | +8% | +2% | +2% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Howl of Annihilation:** Embrace one enemy and cast Vitae (80 AP), then Roar the round after: Roar lands at 47 EP on every enemy in its circle (≈ 47 × 1.37 ≈ 64 with Vitae 37%), and on the marked one exposure 42% with Afterburn 37% makes each instant non-pierce hit ≈ ×1.42 × 1.37 ≈ ×1.95 from anyone (Roar ≈ 47 × 1.37 × 1.95 ≈ 125). Festering Brand instead of Demon's Marrow is the all-Grasp fourth (Afterburn 40%, ≈ ×1.99 on the mark, no Vitae gain).
- **Consuming Malice:** Embrace one enemy and cast Vitae in the same round (80 AP), then fight it for 2 rounds: Afterburn 45% with exposure 37% makes each instant non-pierce hit it takes worth ≈ ×1.37 × 1.45 ≈ ×1.99 from anyone, and the caster's own hits carry Vitae 37% on top (≈ ×2.72). Roar stays at 45 EP. Rending Grip instead of Demon's Marrow lifts exposure to 39% (≈ ×2.02 on the mark) with no Vitae gain.
- **Unyielding Husk:** Demonic Vitae's Decrease Damage Taken reaches 35% for 2 rounds (the +10% route; damage taken ×0.75 → ×0.65) with Increase Damage Given 37%. Demon's Grasp is the fourth purchase (Embrace 37% / 37%); Boiling Ichor instead gives Vitae Increase Damage Given 39%. Roar stays at 45 EP.
- **Primordial Rampage:** Demonic Vitae's Increase Damage Given reaches 43% for the 3 rounds after each cast on every non-pierce hit the caster lands on any target: Roar at 45 EP becomes ≈ 45 × 1.43 ≈ 64 on every enemy in its circle (level with Howl's 47 × 1.37), and the Embrace target takes ≈ ×1.43 × 1.37 × 1.37 ≈ ×2.68 from the caster. Demon's Grasp adds Embrace 37% / 37%; Scarred Hide (Vitae Decrease Damage Taken 30%) is the all-Vitae alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Exposure into burst | Burn | Fortress | Sustained amplification |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Demonic Vitae | 0 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 43% (+8) |
| Demonic Vitae | 1 | Decrease Damage Taken | self | 25% | 27% (+2) | 27% (+2) | 35% (+10) | 27% (+2) |
| Demonic Embrace | 0 | Afterburn | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 37% (+2) |
| Demonic Embrace | 1 | Increase Damage Taken | enemy | 35% | 42% (+7) | 37% (+2) | 37% (+2) | 37% (+2) |
| Ancient Demon Roar | 0 | wound (unsupported) | enemy | 35% | 35% | 35% | 35% | 35% |
| Ancient Demon Roar | 1 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +8% Increase Damage Given, +7% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Howl of Annihilation: +7% Increase Damage Taken (2 + 2 + 3; off band)
  - Route Consuming Malice: +10% Afterburn (2 + 3 + 5; on band)
  - Route Unyielding Husk: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Primordial Rampage: +8% Increase Damage Given (2 + 2 + 4; off band)
- Supported rows in kit: 5 (AB 1, DMG 1, DDT 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow (raw +16, row-weighted 16)
- Lowest row-weighted node: Rending Grip (2)

Validator warnings:

- classification status: requires classification extension (director decision)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Ancient Demon Roar | 1 | 45 (High) | 47 (High) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Howl of Annihilation | +2 Damage, +7% IDT, +2% AB | Festering Brand | +2 Damage, +7% IDT, +5% AB | 14 |
| Howl of Annihilation | +2 Damage, +7% IDT, +2% AB | Demon's Marrow *(highest diagnostic)* | +2 Damage, +2% IDG, +7% IDT, +2% DDT, +2% AB | 15 |
| Consuming Malice | +2% IDT, +10% AB | Rending Grip | +4% IDT, +10% AB | 14 |
| Consuming Malice | +2% IDT, +10% AB | Demon's Marrow *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% AB | 16 |
| Unyielding Husk | +2% IDG, +10% DDT | Demon's Grasp *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT, +2% AB | 16 |
| Unyielding Husk | +2% IDG, +10% DDT | Boiling Ichor | +4% IDG, +10% DDT | 14 |
| Primordial Rampage | +8% IDG, +2% DDT | Demon's Grasp *(highest diagnostic)* | +8% IDG, +2% IDT, +2% DDT, +2% AB | 14 |
| Primordial Rampage | +8% IDG, +2% DDT | Scarred Hide | +8% IDG, +5% DDT | 13 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Demon's Grasp, Rending Grip, Howl of Annihilation, Festering Brand | +2 Damage, +7% IDT, +5% AB |
| 2 | Demon's Grasp, Rending Grip, Howl of Annihilation, Demon's Marrow | +2 Damage, +2% IDG, +7% IDT, +2% DDT, +2% AB |
| 3 | Demon's Grasp, Rending Grip, Festering Brand, Consuming Malice | +4% IDT, +10% AB |
| 4 | Demon's Grasp, Rending Grip, Festering Brand, Demon's Marrow | +2% IDG, +4% IDT, +2% DDT, +5% AB |
| 5 | Demon's Grasp, Rending Grip, Demon's Marrow, Scarred Hide | +2% IDG, +4% IDT, +5% DDT, +2% AB |
| 6 | Demon's Grasp, Rending Grip, Demon's Marrow, Boiling Ichor | +4% IDG, +4% IDT, +2% DDT, +2% AB |
| 7 | Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow | +2% IDG, +2% IDT, +2% DDT, +10% AB |
| 8 | Demon's Grasp, Festering Brand, Demon's Marrow, Scarred Hide | +2% IDG, +2% IDT, +5% DDT, +5% AB |
| 9 | Demon's Grasp, Festering Brand, Demon's Marrow, Boiling Ichor | +4% IDG, +2% IDT, +2% DDT, +5% AB |
| 10 | Demon's Grasp, Demon's Marrow, Scarred Hide, Unyielding Husk | +2% IDG, +2% IDT, +10% DDT, +2% AB |
| 11 | Demon's Grasp, Demon's Marrow, Scarred Hide, Boiling Ichor | +4% IDG, +2% IDT, +5% DDT, +2% AB |
| 12 | Demon's Grasp, Demon's Marrow, Boiling Ichor, Primordial Rampage | +8% IDG, +2% IDT, +2% DDT, +2% AB |
| 13 | Demon's Marrow, Scarred Hide, Unyielding Husk, Boiling Ichor | +4% IDG, +10% DDT |
| 14 | Demon's Marrow, Scarred Hide, Boiling Ichor, Primordial Rampage | +8% IDG, +5% DDT |

## Design notes

- Structure (2/4/4, the pre-batch shape): Demon's Grasp raises both Demonic Embrace debuffs and forks into exposure into burst (Rending Grip → Howl of Annihilation) or a burn (Festering Brand → Consuming Malice); Demon's Marrow raises both Demonic Vitae buffs and forks into fortress (Scarred Hide → Unyielding Husk) or sustained amplification (Boiling Ichor → Primordial Rampage). Each Hidden Art leans on a different tag, and no node is in every legal 4-BP build.
- Roster pass: the first pass cut Draft 4's Roar route (Rending Bellow +2 Damage → Howl of Annihilation +3 Damage, +2% exposure) and hung Roar's +2 on Primordial Rampage. That route was a Roar burst, not a marked-prey twin, and a +2 payoff on a 45 row does not reach the Nuke tier (Arashima's Sundered Sky carries +2 on 45 rows). It is restored with the director pattern: a percentage setup at the Hidden Art (Rending Grip, exposure) and the only flat Damage on the Advanced Art (+2, 45 → 47). Primordial Rampage is back to Increase Damage Given alone.
- Damage: Draft 4 lifted Ancient Demon Roar 45 → 50 (semi-nuke to nuke). Now the only flat Damage is Howl of Annihilation's +2 (45 → 47, High tier kept), the roster default for a High row; no Hidden Art carries flat Damage.
- Embrace split: exposure belongs to Howl's route (+7%, 35 → 42%) and Afterburn to Malice's (+10%, 35 → 45%), and neither capstone carries the other's tag. A capstone plus the sibling Hidden Art reaches at most exposure 39% / Afterburn 45% (≈ ×1.39 × 1.45 ≈ ×2.02 on the mark) or exposure 42% / Afterburn 40% (≈ ×1.42 × 1.40 ≈ ×1.99), both below the first pass's Malice package (40% / 45%, ≈ ×2.03); with Malice held, exposure stays at +4% (×1.030), inside the roster's ≤ +5% beside an Afterburn capstone (concerns). Afterburn reads each hit after the damage modifiers, so the two compound; it is not damage over time and caps at 60% of a hit.
- Narrow coverage: Roar's +2 is one row on one 60 AP cast per 7 rounds (+4.4% on that cast), so Howl carries an identity-compatible secondary (exposure on the target the Roar is aimed at) rather than more Damage. Exposure +7% on one row is ≈ ×1.05 on the mark, below the anchors' compounded exposure (Shakunetsu +5% on two rows ≈ ×1.075, Blood-Enchanted Eyes +5% on three ≈ ×1.115).
- Pricing by reach: Vitae's Increase Damage Given multiplies every hit the caster lands on every target for 3 rounds, so Primordial Rampage stays at +8% (43%, ×1.059), not +10%. Its steps are 2/2/4, so the capstone's +4% outweighs Boiling Ichor's +2%.
- Fourth-BP comparisons (arithmetic only): Howl + Marrow against Rampage + Grasp puts Roar level on the rest of the circle (47 × 1.37 ≈ 64.4 against 45 × 1.43 ≈ 64.4); Howl leads on allies' hits on the mark (≈ ×1.95 against ×1.88) and on Roar on the mark (≈ 125 against 121), Rampage on the caster's hits against everyone else (+4.4%), slightly on its non-Roar hits on the mark (+0.7%) and in Vitae's third round. Malice + Marrow against Howl + Marrow: Malice +2.1% on every hit the mark takes; Howl's Roar +4.4% on every other enemy in its circle and ≈ +2.3% on the marked one.
- No cross-riders: each Vitae capstone carries only its own route's tag. Capstone plus sibling Hidden Art: 06,07,08,09 gives Increase Damage Given 39% / Decrease Damage Taken 35%; 06,07,09,10 gives 43% / 30%.
- Maxima over every legal allocation: Damage +2, Increase Damage Given +8%, Increase Damage Taken +7%, Decrease Damage Taken +10%, Afterburn +10%. Top offensive package: Primordial Rampage with Demon's Grasp, ×1.059 × 1.015 ≈ ×1.075, under Blood-Enchanted Eyes' ×1.234.
- Delivery: all three jutsu have cooldown 7 and no row acts in its own cast round (§3b). Embrace (one target, 40 AP) and Vitae (self, 40 AP) go a round before Roar (60 AP AoE circle) to touch it; Vitae's Increase Damage Given (3 rounds) raises Roar on every enemy in the circle, Embrace's debuffs only on the marked one.

## Risks and unproven interactions

- Classification: no kit row carries an element, so 'Ancient Tailed Demon' is the placeholder name of a new jutsu classification (requires classification extension), not a bloodline-id selector; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row. Off-kit coverage is unverified.
- Embrace leverage: its exposure (up to 42%) and Afterburn (up to 45%) apply to every non-pierce hit the marked target takes from the caster and allies for 2 rounds, so team play is worth more than the solo numbers. Afterburn sources add and cap at 60% of each hit, so a second Afterburn source saturates it.
- Route balance between Howl of Annihilation, Consuming Malice and Primordial Rampage is arithmetic only (per-hit multipliers, Roar damage assumed proportional to EP); no combat simulation.
- Pierce: the four percentage tags do not touch pierce hits (pierce resolves after the damage modifiers and Afterburn skips it), and the kit has no pierce row, so pierce damage stays outside the tree.
- Ally hazard: Ancient Demon Roar's unsupported Wound row (35%, friendly fire none) lands on allies inside the circle; the caster is never a target (§4b). Howl's route invites more Roar casts. Embrace aimed at an ally (OTHER_USER permits it) would land both raised debuffs on that ally.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. The bloodline's 5% self Increase Damage Taken passive and AP economy were not modelled.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Ancient Tailed Demon-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

