# Bakuhatsu — Doctrine of Detonation

**Bloodline:** Bakuhatsu (BR-008, rank A, `RNUcHSH2c00IhOLc2C9aJ`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Explosion classification / forked tree · **Classification:** Explosion (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Increase Damage Given (the charge: Charge 4 Explosion and Howitzer Crash self buffs, which compound) · secondary Afterburn and Increase Damage Taken (the mark Charge 4 Explosion leaves on its target) · tertiary Decrease Damage Taken (Blast Shield).

The three Explosion Damage rows (Kinetic Nova 50, Inferno Cataclysm and Howitzer Crash 40 EP) stay unamplified: Kinetic Nova is already a Nuke, so any flat Damage lifts it past 50. The burst is carried by the charge instead: the two 35% Increase Damage Given self buffs multiply every matching caster hit, area attacks included, in the two rounds after their casts. Primed Fuse answers "How do I make the detonation land harder: charge myself or mark the target?" with Critical Mass (both self buffs 43%) and Chain Reaction (Charge 4 Explosion's Afterburn 45% and exposure 40%). Eye of the Blast answers "How do I survive at the centre of my own blasts?" with one fortress, Siege Battery (Blast Shield 45%). The kit has no heal, lifesteal, reflect or Decrease Damage Given rows, so no sustain or suppression route is invented.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Primed Fuse | Foundation | How do I make the detonation land harder: charge myself or mark the target? |
| Eye of the Blast | Foundation | How do I survive at the centre of my own blasts? |
| Critical Mass | Advanced Art | area burst: both self buffs charged, every blast in the window lands harder on all it hits |
| Chain Reaction | Advanced Art | mark: exposure and Afterburn on one target, paid out by every hit from the party |
| Siege Battery | Advanced Art | fortress that keeps firing |

**Director review recommended:** Structural: flat Damage is removed rather than re-cut (any flat Damage lifts Kinetic Nova past 50), leaving three Advanced Arts with Primed Fuse in every build. Confirm the narrow-kit exception, or choose the Blood-Enchanted Eyes pattern as a fourth route (Shaped Charge +3% Increase Damage Taken → Ground Zero +2 Damage, Kinetic Nova 50 → 52).

- Concern: Critical Mass is held at +8% Increase Damage Given because the two self buffs compound; it remains the strongest solo route against targets other than the mark.
- Concern: Primed Fuse is universal, so the fortress's fourth purchase is forced; the kit has no second defensive tag for a leaf under Eye of the Blast.
- Concern: Every amplified row except the exposure depends on the proposed jutsu-classification resolver.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. Supported rows: three Explosion Damage rows, two Increase Damage Given self buffs, and one row each of Increase Damage Taken and Afterburn (both on Charge 4 Explosion's target) and Decrease Damage Taken (Blast Shield). Flat Damage is declined because Kinetic Nova is a 50 EP Nuke and any flat Damage lifts it past 50, so the old Burst branch (Shaped Charge → Ground Zero) is removed rather than re-cut. Increase Damage Taken and Afterburn share one cast, target and window, so they form one mark route, not two; Decrease Damage Taken is one row, so Eye of the Blast roots a single fortress chain. A fourth Advanced Art would repeat one of the three. Primed Fuse is a universal node (in all 8 legal 4 BP builds) because the defensive root has no second defensive tag for a leaf.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Explosion jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Primed Fuse | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Charge 4 Explosion, Howitzer Crash / 3 |
| 04 | Powder Keg | Hidden Art | Primed Fuse | +2% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 10 | Critical Mass | Advanced Art | Powder Keg | +4% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 08 | Slow Burn | Hidden Art | Primed Fuse | +5% Afterburn (enemy debuff) | Charge 4 Explosion / 1 |
| 09 | Chain Reaction | Advanced Art | Slow Burn | +5% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Charge 4 Explosion / 2 |
| 05 | Eye of the Blast | Foundation | None | +2% Decrease Damage Taken (self buff) | Blast Shield / 1 |
| 06 | Hardened Casing | Hidden Art | Eye of the Blast | +3% Decrease Damage Taken (self buff) | Blast Shield / 1 |
| 07 | Siege Battery | Advanced Art | Hardened Casing | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Blast Shield, Charge 4 Explosion, Howitzer Crash / 3 |

Connections: 01→04, 04→10, 01→08, 08→09, 05→06, 06→07. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Primed Fuse** — Every detonation begins as a held breath and a lit fuse. Charge 4 Explosion and Howitzer Crash self buffs 35 → 37%; Charge 4 Explosion exposure 35 → 37%. In every legal build, because Eye of the Blast roots a single chain.
- **Powder Keg** — The body is a magazine; patience is the match. Commits to the charge: both self buffs 37 → 39% with Primed Fuse, each live the two rounds after its cast (×1.39 × 1.39 ≈ ×1.93 with both up).
- **Critical Mass** — Pack enough charge into one body and the body becomes the bomb. Area burst: both self buffs 35 → 43% on the full route (+8%); with both live, every caster hit that is element-less or uses the highest offence stat lands ×1.43 × 1.43 ≈ ×2.04 (×1.82 unmodified).
- **Slow Burn** — Shrapnel lodges hot and stays hot. Marks the target: Charge 4 Explosion Afterburn 35 → 40% (single target, range 4, 40 AP, live the two rounds after the cast).
- **Chain Reaction** — One blast primes the next. Nothing lands only once. Mark: Charge 4 Explosion Afterburn 35 → 45% (+10%) and exposure 35 → 40% with Primed Fuse, from one 40 AP cast; every non-pierce hit on the target, allies' included, burns for 45%.
- **Eye of the Blast** — Every detonation has a still centre. Stand in it. Blast Shield Decrease Damage Taken 35 → 37% (caster-only self buff, 2 rounds per 40 AP cast).
- **Hardened Casing** — Debris packs into a wall that holds the second time, too. Blast Shield Decrease Damage Taken 37 → 40% with Eye of the Blast (one caster-only row).
- **Siege Battery** — Dug in behind the blast wall, the battery keeps firing. Fortress: Blast Shield 35 → 45% on the full route (+10%), incoming hits ×0.55 (×0.65 unmodified); both self buffs +2%, 39% with Primed Fuse, the route's only fourth purchase.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|
| Critical Mass (Area burst) | Primed Fuse, Powder Keg, Critical Mass, Slow Burn | +8% | +2% | — | +5% |
| Chain Reaction (Mark) | Primed Fuse, Slow Burn, Chain Reaction, Powder Keg | +4% | +5% | — | +10% |
| Siege Battery (Fortress) | Eye of the Blast, Hardened Casing, Siege Battery, Primed Fuse | +4% | +2% | +10% | — |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Critical Mass:** Both self buffs reach 43% (Primed Fuse +2%, Powder Keg +2%, Critical Mass +4%). Cast Charge 4 Explosion and Howitzer Crash in one 100 AP round; in the next two rounds every Kinetic Nova, Inferno Cataclysm or other caster hit that is element-less or uses the highest offence stat lands ×1.43 × 1.43 ≈ ×2.04 on everything it hits, and the bloodline passive multiplies last. Slow Burn is the offensive fourth (Afterburn 40% and exposure 37% on the charged target); Eye of the Blast (Blast Shield 37%) is the safe one.
- **Chain Reaction:** One 40 AP Charge 4 Explosion marks its target for two rounds: Afterburn 45% (Slow Burn +5%, Chain Reaction +5%) and exposure 40% (Primed Fuse +2%, Chain Reaction +3%). Every non-pierce hit on the mark, from the caster or allies, adds 45% Afterburn, and Earth, Explosion, Lightning or element-less hits are first raised ×1.40. Powder Keg is the offensive fourth: with both self buffs at 39% a caster hit on the mark lands ×1.39 × 1.39 × 1.40 ≈ ×2.70, then burns for 45% of that. Eye of the Blast (Blast Shield 37%) is the defensive fourth.
- **Siege Battery:** Blast Shield's reduction reaches 45% on the caster for the two rounds after each 40 AP cast (incoming hits ×0.55; allies do not receive it). Primed Fuse is the only fourth purchase, because Eye of the Blast roots a single chain: with Siege Battery's +2% both self buffs reach 39% and the exposure 37%, so the shielded caster still fires a charged Nova (×1.39 × 1.39 ≈ ×1.93 with both buffs up).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Area burst | Mark | Fortress |
|---|---:|---|---|---:|---:|---:|---:|
| Inferno Cataclysm | 0 | Damage | enemy | 40 | 40 | 40 | 40 |
| Inferno Cataclysm | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% |
| Kinetic Nova | 0 | Damage | enemy | 50 | 50 | 50 | 50 |
| Kinetic Nova | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% |
| Blast Shield | 0 | Decrease Damage Taken | self | 35% | 35% | 35% | 45% (+10) |
| Blast Shield | 1 | barrier (unsupported) | self | 100 | 100 | 100 | 100 |
| Charge 4 Explosion | 0 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 39% (+4) |
| Charge 4 Explosion | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) |
| Charge 4 Explosion | 2 | Afterburn | enemy | 35% | 40% (+5) | 45% (+10) | 35% |
| Howitzer Crash | 0 | Damage | enemy | 40 | 40 | 40 | 40 |
| Howitzer Crash | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Howitzer Crash | 2 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 39% (+4) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Siege Battery: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Chain Reaction: +10% Afterburn (0 + 5 + 5; on band)
  - Route Critical Mass: +8% Increase Damage Given (2 + 2 + 4; off band)
- Supported rows in kit: 8 (AB 1, DMG 3, DDT 1, IDG 2, IDT 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Primed Fuse, Powder Keg, Slow Burn, Chain Reaction (raw +19, row-weighted 23)
- Lowest row-weighted node: Eye of the Blast (2)

Validator warnings:

- universal node: 01 (Primed Fuse) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Inferno Cataclysm 40 (Normal), Kinetic Nova 50 (Nuke), Howitzer Crash 40 (Normal)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Siege Battery | +2% IDG, +10% DDT | Primed Fuse *(highest diagnostic)* | +4% IDG, +2% IDT, +10% DDT | 20 |
| Chain Reaction | +2% IDG, +5% IDT, +10% AB | Powder Keg *(highest diagnostic)* | +4% IDG, +5% IDT, +10% AB | 23 |
| Chain Reaction | +2% IDG, +5% IDT, +10% AB | Eye of the Blast | +2% IDG, +5% IDT, +2% DDT, +10% AB | 21 |
| Critical Mass | +8% IDG, +2% IDT | Eye of the Blast | +8% IDG, +2% IDT, +2% DDT | 20 |
| Critical Mass | +8% IDG, +2% IDT | Slow Burn *(highest diagnostic)* | +8% IDG, +2% IDT, +5% AB | 23 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Primed Fuse, Powder Keg, Eye of the Blast, Hardened Casing | +4% IDG, +2% IDT, +5% DDT |
| 2 | Primed Fuse, Powder Keg, Eye of the Blast, Slow Burn | +4% IDG, +2% IDT, +2% DDT, +5% AB |
| 3 | Primed Fuse, Powder Keg, Eye of the Blast, Critical Mass | +8% IDG, +2% IDT, +2% DDT |
| 4 | Primed Fuse, Powder Keg, Slow Burn, Chain Reaction | +4% IDG, +5% IDT, +10% AB |
| 5 | Primed Fuse, Powder Keg, Slow Burn, Critical Mass | +8% IDG, +2% IDT, +5% AB |
| 6 | Primed Fuse, Eye of the Blast, Hardened Casing, Siege Battery | +4% IDG, +2% IDT, +10% DDT |
| 7 | Primed Fuse, Eye of the Blast, Hardened Casing, Slow Burn | +2% IDG, +2% IDT, +5% DDT, +5% AB |
| 8 | Primed Fuse, Eye of the Blast, Slow Burn, Chain Reaction | +2% IDG, +5% IDT, +2% DDT, +10% AB |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Removed: Shaped Charge (+2 Damage) and Ground Zero (+3 Damage); the +5 route lifted Kinetic Nova 50 → 55 and Inferno Cataclysm and Howitzer Crash 40 → 45, and even +2 lifts Nova past 50. Rewired: Slow Burn moves from Smoke and Shrapnel to Primed Fuse (Afterburn +3% → +5%), so the mark sits beside the charge on the offensive root; Smoke and Shrapnel becomes Eye of the Blast (+2% Decrease Damage Taken; its +2% Afterburn moved into Slow Burn). Changed: Powder Keg +3% → +2% and Critical Mass +5% → +4% Increase Damage Given. Kept: Primed Fuse, Hardened Casing, Siege Battery and Chain Reaction values; the Chain Reaction build with Eye of the Blast as its fourth has the old Pressure build's totals.
- Increase Damage Given is held at +8%, not +10%: its two self buffs compound when both are live, so +8% takes the double-buff window from ×1.82 to ×2.04 (+12%, about what a +16% step does on one row); +10% would reach ×2.10. Maxima over every legal allocation: Increase Damage Given +8%, Afterburn +10%, Increase Damage Taken +5%, Decrease Damage Taken +10%, no flat Damage.
- Filters (§3): both Increase Damage Given rows list the Highest stat and no element, so they match every element-less hit of any stat type and the caster's highest-stat elemental hits, all three Explosion attacks included. The exposure lists Earth, Explosion, Lightning and None; Afterburn and Blast Shield's row list all four stat types and no element. The bloodline Increase Damage Given passive (25% + 0.15 per level; Lightning, Earth, Explosion, None) multiplies last; the Earth-only 15% Decrease Damage Taken passive is separate from Blast Shield's row.
- Delivery (§3b, §4b): every jutsu has cooldown 7. Charge 4 Explosion (40 AP, single target, range 4) carries the self buff, the exposure and the Afterburn; Howitzer Crash (60 AP, empty-ground circle, range 5, moves the caster) carries the second self buff; Blast Shield (40 AP) the reduction. SELF rows land on the caster at cast. Every buff and debuff is live only in the two rounds after its cast, so neither self buff raises its own jutsu's hit.
- Fourth purchases: Critical Mass takes Slow Burn (Afterburn 40%) or Eye of the Blast; Chain Reaction takes Powder Keg (self buffs 39%) or Eye of the Blast; Siege Battery takes Primed Fuse. The two all-offense builds share Primed Fuse, Powder Keg and Slow Burn and differ only in the capstone; a caster hit on the mark with both buffs up comes to the same total (×1.43² × 1.37 × 1.40 ≈ ×1.39² × 1.40 × 1.45 ≈ ×3.92), so Critical Mass wins on every other target its area reaches and Chain Reaction wins for allies hitting the mark (×1.40 × 1.45 ≈ ×2.03 against ×1.37 × 1.40 ≈ ×1.92). No fourth makes a route automatic.

## Risks and unproven interactions

- Classification: Explosion is shared with Bakuhatsu Suru Nendo (expected under RUL-2026-10-03-005). With flat Damage gone, the exposure row is the only amplified row that carries Explosion; both self buffs, the Afterburn row and Blast Shield's row need the proposed jutsu-classification resolver, and Blast Shield (no Explosion row) also needs an authored classification (ENGINE_GAP_REGISTER G1). Off-kit Explosion coverage is unverified.
- Reach: the self buffs multiply every matching caster hit in their window, on every target an area attack catches, plus weapons, basic attacks and off-kit jutsu; the exposure and Afterburn raise allies' hits on the mark. Blast Shield's reduction is caster-only.
- Charge 4 Explosion concentration: in the Chain Reaction build with Powder Keg one 40 AP cast carries three enhanced rows (self buff 39%, exposure 40%, Afterburn 45%). Afterburn per hit is capped at 60% of the hit, so 45% leaves 15 points for other Afterburn sources.
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

