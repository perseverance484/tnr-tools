# Bakuhatsu — Doctrine of Detonation

**Bloodline:** Bakuhatsu (BR-008, rank A, `RNUcHSH2c00IhOLc2C9aJ`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Explosion classification / forked tree · **Classification:** Explosion (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Increase Damage Given and Increase Damage Taken (charge and aim: the Charge 4 Explosion and Howitzer Crash self buffs, which compound, and Charge 4 Explosion's exposure on its target) · secondary Afterburn (the mark Charge 4 Explosion leaves on its target) · tertiary Decrease Damage Taken (Blast Shield); Damage is not amplified.

Three of the eight supported rows are Explosion Damage (Kinetic Nova 50, Inferno Cataclysm and Howitzer Crash 40 EP), but the kit's trait is AoE Control, not Burst, and Kinetic Nova shares rank A, 60 AP and cooldown 7 with Inferno Cataclysm, so Damage stays unamplified and Nova stays at 50. Primed Fuse answers "How do I make my detonations land harder: charge myself or aim the charge?" with Critical Mass (both compounding self buffs 43%) and Ground Zero (Charge 4 Explosion exposure 45%). Smoke and Shrapnel answers "How do I win what the blast leaves behind: shelter in the smoke or leave the shrapnel burning?" with Siege Battery (Blast Shield 45%) and Chain Reaction (Afterburn 45%). The kit has no heal, lifesteal, reflect or Decrease Damage Given rows, so no sustain or suppression route is invented.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Primed Fuse | Foundation | How do I make my detonations land harder: charge myself or aim the charge? |
| Smoke and Shrapnel | Foundation | How do I win what the blast leaves behind: shelter in the smoke or leave the shrapnel burning? |
| Ground Zero | Advanced Art | exposure: the charged target takes more from every matching hit, the party's included |
| Critical Mass | Advanced Art | sustained amplification: both self buffs charged, every hit in the window lands harder |
| Chain Reaction | Advanced Art | mark: Afterburn on one target, paid out by every hit from the party |
| Siege Battery | Advanced Art | fortress: Blast Shield's reduction on the caster |

**Director review recommended:** Roster questions: DQ-B (Ground Zero +10% exposure on one row, Charge 4 Explosion 35 → 45%, ×1.074).

- Concern: Ground Zero and Chain Reaction both mark the Charge 4 Explosion target. Exposure multiplies only Earth, Explosion, Lightning and element-less hits; Afterburn adds to every non-pierce hit, capped at 60% per hit. No allocation holds both capstones, and with the other branch's Foundation as fourth each reaches ×1.45 × 1.37 ≈ ×1.99 on an ally's matching hit (×1.82 unmodified).
- Concern: Critical Mass with Shaped Charge is the top offensive package (×1.164, under Blood-Enchanted Eyes' ×1.234); Ground Zero with Powder Keg is ×1.060 × 1.074 ≈ ×1.139 and ahead on allies' hits on the target.
- Concern: Damage is left unamplified on kit evidence (AoE Control, no Burst; Kinetic Nova's AP and cooldown match Inferno Cataclysm's); a controlled +2 Damage Ground Zero would return only if the director reads Nova as the kit's signature finisher.
- Concern: Every amplified row except the exposure depends on the proposed jutsu-classification resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Explosion jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Primed Fuse | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Charge 4 Explosion, Howitzer Crash / 3 |
| 02 | Shaped Charge | Hidden Art | Primed Fuse | +3% Increase Damage Taken (enemy debuff) | Charge 4 Explosion / 1 |
| 03 | Ground Zero | Advanced Art | Shaped Charge | +5% Increase Damage Taken (enemy debuff) | Charge 4 Explosion / 1 |
| 04 | Powder Keg | Hidden Art | Primed Fuse | +2% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 10 | Critical Mass | Advanced Art | Powder Keg | +4% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 05 | Smoke and Shrapnel | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Afterburn (enemy debuff) | Blast Shield, Charge 4 Explosion / 2 |
| 06 | Hardened Casing | Hidden Art | Smoke and Shrapnel | +3% Decrease Damage Taken (self buff) | Blast Shield / 1 |
| 07 | Siege Battery | Advanced Art | Hardened Casing | +5% Decrease Damage Taken (self buff) | Blast Shield / 1 |
| 08 | Slow Burn | Hidden Art | Smoke and Shrapnel | +3% Afterburn (enemy debuff) | Charge 4 Explosion / 1 |
| 09 | Chain Reaction | Advanced Art | Slow Burn | +5% Afterburn (enemy debuff) | Charge 4 Explosion / 1 |

Connections: 01→02, 02→03, 01→04, 04→10, 05→06, 06→07, 05→08, 08→09. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Primed Fuse** — Every detonation begins as a held breath and a lit fuse. Charge 4 Explosion and Howitzer Crash self buffs 35 → 37%; Charge 4 Explosion exposure 35 → 37% (3 rows).
- **Shaped Charge** — The blast is not larger; it is aimed. Aims the charge (Ground Zero's setup): Charge 4 Explosion exposure 37 → 40% with Primed Fuse (single target, range 4, 40 AP, live the two rounds after the cast); Earth, Explosion, Lightning and element-less hits on it land ×1.40.
- **Ground Zero** — Where the charge lands, the map is redrawn. Exposure payoff: Charge 4 Explosion exposure 35 → 45% on the full route (+10%) from one 40 AP cast; for the two rounds after it, every Earth, Explosion, Lightning or element-less hit on the target, allies' included, lands ×1.45 (×1.35 unmodified, ×1.074).
- **Powder Keg** — The body is a magazine; patience is the match. Commits to the charge: both self buffs 37 → 39% with Primed Fuse, each live the two rounds after its cast (×1.39 × 1.39 ≈ ×1.93 with both up).
- **Critical Mass** — Pack enough charge into one body and the body becomes the bomb. Sustained amplification: both self buffs 35 → 43% on the full route (+8%); with both live, every caster hit that is element-less or uses the highest offence stat lands ×1.43 × 1.43 ≈ ×2.04 (×1.82 unmodified).
- **Smoke and Shrapnel** — The blast is over. Its cloud and its fragments are not. Blast Shield Decrease Damage Taken 35 → 37% (caster-only self buff, 2 rounds per 40 AP cast); Charge 4 Explosion Afterburn 35 → 37% (2 rows).
- **Hardened Casing** — Debris packs into a wall that holds the second time, too. Blast Shield Decrease Damage Taken 37 → 40% with Smoke and Shrapnel (one caster-only row).
- **Siege Battery** — Dug in behind the blast wall, the battery outlasts the barrage. Fortress: Blast Shield 35 → 45% on the full route (+10%), incoming hits ×0.55 (×0.65 unmodified, ×0.846); caster-only, two rounds per 40 AP cast.
- **Slow Burn** — Shrapnel lodges hot and stays hot. Marks the target: Charge 4 Explosion Afterburn 37 → 40% with Smoke and Shrapnel (single target, range 4, 40 AP, live the two rounds after the cast).
- **Chain Reaction** — One blast primes the next. Nothing lands only once. Mark: Charge 4 Explosion Afterburn 35 → 45% on the full route (+10%) from one 40 AP cast; for the two rounds after it, every non-pierce hit on the target, allies' included, adds 45% Afterburn.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|
| Ground Zero (Exposure) | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg | +4% | +10% | — | — |
| Critical Mass (Sustained amplification) | Primed Fuse, Powder Keg, Critical Mass, Shaped Charge | +8% | +5% | — | — |
| Chain Reaction (Mark) | Smoke and Shrapnel, Slow Burn, Chain Reaction, Primed Fuse | +2% | +2% | +2% | +10% |
| Siege Battery (Fortress) | Smoke and Shrapnel, Hardened Casing, Siege Battery, Primed Fuse | +2% | +2% | +10% | +2% |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Ground Zero:** One 40 AP Charge 4 Explosion leaves its target at exposure 45% for two rounds (Primed Fuse +2%, Shaped Charge +3%, Ground Zero +5%): every Earth, Explosion, Lightning or element-less hit on it, allies' included, lands ×1.45 (×1.35 unmodified). Powder Keg is the offensive fourth: after Charge 4 Explosion and Howitzer Crash in one 100 AP round both self buffs are 39%, so the caster's Kinetic Nova on the target lands ×1.39 × 1.39 × 1.45 ≈ ×2.80 before the bloodline passive (×2.46 unmodified). Smoke and Shrapnel (Blast Shield 37%, Afterburn 37%) is the safer fourth.
- **Critical Mass:** Both self buffs reach 43% (Primed Fuse +2%, Powder Keg +2%, Critical Mass +4%). Cast Charge 4 Explosion and Howitzer Crash in one 100 AP round; in the next two rounds every Kinetic Nova, Inferno Cataclysm or other caster hit that is element-less or uses the highest offence stat lands ×1.43 × 1.43 ≈ ×2.04 on everything it hits, weapons and off-kit jutsu included, and the bloodline passive multiplies last. Shaped Charge is the offensive fourth (exposure 40%: ×2.04 × 1.40 ≈ ×2.86 on the charged target); Smoke and Shrapnel (Blast Shield 37%, Afterburn 37%) is the safe one.
- **Chain Reaction:** One 40 AP Charge 4 Explosion marks its target for two rounds: Afterburn 45% (Smoke and Shrapnel +2%, Slow Burn +3%, Chain Reaction +5%), so every non-pierce hit on the mark, from the caster or allies, adds 45% Afterburn. Primed Fuse is the offensive fourth: the same cast's exposure reaches 37% and both self buffs 37%, so an ally's Earth, Explosion, Lightning or element-less hit on the mark comes to ×1.37 × 1.45 ≈ ×1.99. Hardened Casing (Blast Shield 40%) is the defensive one.
- **Siege Battery:** Blast Shield's reduction reaches 45% on the caster for the two rounds after each 40 AP cast (incoming hits ×0.55 against ×0.65, ×0.846; allies do not receive it). Primed Fuse is the fourth that keeps the battery firing: both self buffs 37% and the exposure 37% (×1.37 × 1.37 ≈ ×1.88 with both buffs up). Slow Burn (Afterburn 40%) is the alternative fourth for a bunker that still burns.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Exposure | Sustained amplification | Mark | Fortress |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Inferno Cataclysm | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Inferno Cataclysm | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Kinetic Nova | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Kinetic Nova | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Blast Shield | 0 | Decrease Damage Taken | self | 35% | 35% | 35% | 37% (+2) | 45% (+10) |
| Blast Shield | 1 | barrier (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Charge 4 Explosion | 0 | Increase Damage Given | self | 35% | 39% (+4) | 43% (+8) | 37% (+2) | 37% (+2) |
| Charge 4 Explosion | 1 | Increase Damage Taken | enemy | 35% | 45% (+10) | 40% (+5) | 37% (+2) | 37% (+2) |
| Charge 4 Explosion | 2 | Afterburn | enemy | 35% | 35% | 35% | 45% (+10) | 37% (+2) |
| Howitzer Crash | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Howitzer Crash | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Howitzer Crash | 2 | Increase Damage Given | self | 35% | 39% (+4) | 43% (+8) | 37% (+2) | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Ground Zero: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Siege Battery: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Chain Reaction: +10% Afterburn (2 + 3 + 5; on band)
  - Route Critical Mass: +8% Increase Damage Given (2 + 2 + 4; off band)
- Supported rows in kit: 8 (AB 1, DMG 3, DDT 1, IDG 2, IDT 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Primed Fuse, Powder Keg, Smoke and Shrapnel, Critical Mass (raw +14, row-weighted 22)
- Lowest row-weighted node: Shaped Charge (3)

Validator warnings:

- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Inferno Cataclysm 40 (Normal), Kinetic Nova 50 (Nuke), Howitzer Crash 40 (Normal)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Ground Zero | +2% IDG, +10% IDT | Powder Keg | +4% IDG, +10% IDT | 18 |
| Ground Zero | +2% IDG, +10% IDT | Smoke and Shrapnel *(highest diagnostic)* | +2% IDG, +10% IDT, +2% DDT, +2% AB | 18 |
| Siege Battery | +10% DDT, +2% AB | Primed Fuse *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT, +2% AB | 18 |
| Siege Battery | +10% DDT, +2% AB | Slow Burn | +10% DDT, +5% AB | 15 |
| Chain Reaction | +2% DDT, +10% AB | Primed Fuse *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% AB | 18 |
| Chain Reaction | +2% DDT, +10% AB | Hardened Casing | +5% DDT, +10% AB | 15 |
| Critical Mass | +8% IDG, +2% IDT | Shaped Charge | +8% IDG, +5% IDT | 21 |
| Critical Mass | +8% IDG, +2% IDT | Smoke and Shrapnel *(highest diagnostic)* | +8% IDG, +2% IDT, +2% DDT, +2% AB | 22 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg | +4% IDG, +10% IDT |
| 2 | Primed Fuse, Shaped Charge, Ground Zero, Smoke and Shrapnel | +2% IDG, +10% IDT, +2% DDT, +2% AB |
| 3 | Primed Fuse, Shaped Charge, Powder Keg, Smoke and Shrapnel | +4% IDG, +5% IDT, +2% DDT, +2% AB |
| 4 | Primed Fuse, Shaped Charge, Powder Keg, Critical Mass | +8% IDG, +5% IDT |
| 5 | Primed Fuse, Shaped Charge, Smoke and Shrapnel, Hardened Casing | +2% IDG, +5% IDT, +5% DDT, +2% AB |
| 6 | Primed Fuse, Shaped Charge, Smoke and Shrapnel, Slow Burn | +2% IDG, +5% IDT, +2% DDT, +5% AB |
| 7 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Hardened Casing | +4% IDG, +2% IDT, +5% DDT, +2% AB |
| 8 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Slow Burn | +4% IDG, +2% IDT, +2% DDT, +5% AB |
| 9 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Critical Mass | +8% IDG, +2% IDT, +2% DDT, +2% AB |
| 10 | Primed Fuse, Smoke and Shrapnel, Hardened Casing, Siege Battery | +2% IDG, +2% IDT, +10% DDT, +2% AB |
| 11 | Primed Fuse, Smoke and Shrapnel, Hardened Casing, Slow Burn | +2% IDG, +2% IDT, +5% DDT, +5% AB |
| 12 | Primed Fuse, Smoke and Shrapnel, Slow Burn, Chain Reaction | +2% IDG, +2% IDT, +2% DDT, +10% AB |
| 13 | Smoke and Shrapnel, Hardened Casing, Siege Battery, Slow Burn | +10% DDT, +5% AB |
| 14 | Smoke and Shrapnel, Hardened Casing, Slow Burn, Chain Reaction | +5% DDT, +10% AB |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md; roster cleanup pass). Damage is left unamplified: the dossier trait is AoE Control, not Burst, and Kinetic Nova, the only 50 row, shares rank A, 60 AP and cooldown 7 with Inferno Cataclysm (every kit jutsu has cooldown 7), so no dossier fact makes it a signature finisher. Against the pre-batch tree: Shaped Charge +2 Damage → +3% Increase Damage Taken, Ground Zero +3 Damage → +5% Increase Damage Taken (pre-batch Kinetic Nova reached 55), Powder Keg +3% → +2% and Critical Mass +5% → +4% Increase Damage Given, Siege Battery drops its +2% Increase Damage Given rider (no offensive rider on a fortress), and Chain Reaction drops its +3% Increase Damage Taken (it raised the exposure on the same cast as its burn). Unchanged: Primed Fuse, Smoke and Shrapnel, Hardened Casing, Slow Burn.
- Increase Damage Given is held at +8%, not +10%: its two self buffs compound when both are live, so +8% takes the double-buff window from ×1.82 to ×2.04 (×1.122); +10% would reach ×2.10. Exposure is one row: Ground Zero's route takes it 35 → 45% (×1.45/1.35 ≈ ×1.074, the anchor table's single-row figure, level with Shakunetsu Sakura's ×1.075). Top offensive package: Critical Mass with Shaped Charge, ×1.122 × 1.037 ≈ ×1.164, under Blood-Enchanted Eyes' ×1.234. Maxima over every legal allocation: Increase Damage Given +8%, Increase Damage Taken +10%, Afterburn +10%, Decrease Damage Taken +10%, no Damage.
- Filters (§3): both Increase Damage Given rows list the Highest stat and no element, so they match every element-less hit of any stat type and the caster's highest-stat elemental hits, all three Explosion attacks included. The exposure lists Earth, Explosion, Lightning and None; Afterburn and Blast Shield's row list all four stat types and no element. The bloodline Increase Damage Given passive (25% + 0.15 per level; Lightning, Earth, Explosion, None) multiplies last; the Earth-only 15% Decrease Damage Taken passive is separate from Blast Shield's row.
- Delivery (§3b, §4b): every jutsu has cooldown 7. The three Damage casts cost 60 AP (Inferno Cataclysm spiral around the caster, Kinetic Nova circle on a target, Howitzer Crash circle on empty ground that moves the caster) and are ENEMIES-only. Charge 4 Explosion (40 AP, single target, range 4) carries the self buff, the exposure and the Afterburn; Howitzer Crash carries the second self buff; Blast Shield (40 AP) the reduction. SELF rows land on the caster at cast. Every buff and debuff is live only in the two rounds after its cast, so neither self buff raises its own jutsu's hit.
- Fourth purchases: Ground Zero takes Powder Keg (self buffs 39%) or Smoke and Shrapnel (Blast Shield 37%, Afterburn 37%); Critical Mass takes Shaped Charge (exposure 40%) or Smoke and Shrapnel; Chain Reaction takes Primed Fuse (self buffs 37%, exposure 37%: an ally's hit on the mark ×1.37 × 1.45 ≈ ×1.99) or Hardened Casing; Siege Battery takes Primed Fuse (self buffs 37%, exposure 37%) or Slow Burn (Afterburn 40%). Neither Shaped Charge nor Ground Zero can join Chain Reaction (5 BP), so exposure beside the Afterburn capstone stays at +2%. The two all-offense Primed Fuse builds share three nodes and differ in the capstone: in the double-buff window the caster's hit on the charged target lands ×1.43 × 1.43 × 1.40 ≈ ×2.86 with Critical Mass and ×1.39 × 1.39 × 1.45 ≈ ×2.80 with Ground Zero, so Critical Mass wins on the caster's own hits on every target and Ground Zero on allies' hits on the target (×1.45 against ×1.40) and whenever the self-buff round is not paid. No fourth makes a route automatic.

## Risks and unproven interactions

- Damage tier: no node raises Damage, so Kinetic Nova stays 50 (Nuke) and Inferno Cataclysm and Howitzer Crash 40 (Normal) in every allocation.
- Classification: Explosion is shared with Bakuhatsu Suru Nendo (expected under RUL-2026-10-03-005). The exposure row carries Explosion; both self buffs, the Afterburn row and Blast Shield's row need the proposed jutsu-classification resolver, and Blast Shield (no Explosion row) also needs an authored classification (ENGINE_GAP_REGISTER G1). Off-kit Explosion coverage is unverified.
- Reach: the self buffs multiply every matching caster hit in their window, on every target an area attack catches, plus weapons, basic attacks and off-kit jutsu; the exposure and Afterburn raise allies' hits on the mark. Blast Shield's reduction is caster-only.
- Charge 4 Explosion concentration: one 40 AP cast can carry up to three enhanced rows (Ground Zero with Powder Keg: self buff 39%, exposure 45%; Critical Mass with Shaped Charge: self buff 43%, exposure 40%; Chain Reaction with Primed Fuse: self buff 37%, exposure 37%, Afterburn 45%). Afterburn per hit is capped at 60% of the hit, so 45% leaves 15 points for other Afterburn sources.
- Friendly fire: Charge 4 Explosion may be aimed at an ally (OTHER_USER); its enhanced exposure and Afterburn then land on the ally while the self buff stays on the caster. Kinetic Nova's wound (ally hazard) and Blast Shield's barrier (enemy hazard) are unsupported and untouched.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Explosion jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

