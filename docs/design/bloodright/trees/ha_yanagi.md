# Ha Yanagi — Lament of the Willow

**Bloodline:** Ha Yanagi (BR-030, rank D, `uNZ2UMfA3BuX-J_1g0fHU`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Ha Yanagi classification / forked tree · **Classification:** Ha Yanagi (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Enemy debuff control: Decrease Damage Given (Wailing Bark, Petal Nightmare) and Increase Damage Taken (Blighted Tree) · secondary Self amplification: the Wailing Bark Increase Damage Given row, which multiplies every non-pierce hit the caster lands in its window · tertiary A small Damage option, the Hardened Heartwood leaf: Blighted Tree's formula hit 40 → 42 EP (Normal tier); Petal Nightmare's Damage row is static, a fixed 40 HP, so it gains +2 HP.

Three of the kit's six supported rows are enemy debuffs. Mourning Boughs answers "How do I wither the enemy: blunt their blows or open them to every strike?": Grave Willow's Hush takes both compounding Decrease Damage Given rows to +10% (Wailing Bark 45%, Petal Nightmare 40%), and Hollow at the Heart takes the single Blighted Tree exposure row to +8% (38%); that capstone carries no suppression rider, but its route keeps Mourning Boughs' +2% Decrease Damage Given (+5% with Veil of Falling Petals). Whispering Canopy answers "How do I make my own blows land harder: a heavier Blighted Tree or a stronger Wailing Bark window?": Thousand-Leaf Dream takes the one Wailing Bark self buff to 45%, and the Hardened Heartwood leaf adds +2 Damage (Blighted Tree 40 → 42 EP, still Normal). Damage has no route of its own because it reaches one meaningful row: Petal Nightmare's Damage row is static, a fixed 40 HP. Every percentage row lists all four stat types and no element, so each reaches every non-pierce hit, not Genjutsu only. Potency reaches matching supported tags on all Ha Yanagi-classified jutsu (RUL-2026-10-03-005; requires a classification extension).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Mourning Boughs | Foundation | How do I wither the enemy: blunt their blows or open them to every strike? |
| Whispering Canopy | Foundation | How do I make my own blows land harder: a heavier Blighted Tree or a stronger Wailing Bark window? |
| Grave Willow's Hush | Advanced Art | suppression |
| Hollow at the Heart | Advanced Art | exposure: marks the target for every attacker |
| Thousand-Leaf Dream | Advanced Art | sustained amplification of the Wailing Bark window |

**Director review recommended:** Structural: the Burst capstone Nightmare in Bloom is removed (narrow-kit exception, nine nodes and three Advanced Arts) because flat Damage reaches one meaningful row, Blighted Tree; Petal Nightmare's Damage row is static, a fixed 40 HP. Hardened Heartwood stays as a +2 Damage leaf (Blighted Tree 40 → 42 EP). Confirm the three-route tree, or keep Burst as a recorded niche route (+3 Damage, ×1.075 on one Blighted Tree hit every 7 rounds, near-dominated by Thousand-Leaf Dream).

- Concern: Hardened Heartwood is +2 flat Damage on a Hidden Art leaf. It reaches one meaningful row (Blighted Tree 40 → 42 EP, Normal) and exists so the self root completes a full build and Amplifier has an offensive fourth beside Mourning Boughs' suppression; it is a fourth purchase, not a setup.
- Concern: A Damage-focused player has no capstone. Restoring Nightmare in Bloom would give a near-dominated niche route; raising it to +5 Damage would lift Blighted Tree 40 → 45 (Normal → High).
- Concern: Exposure stops at +8% against Amplifier's +10% (both single rows) because exposure also multiplies allies' hits; Hollow at the Heart +7% (exposure +10%) is the alternative if the director wants parity.
- Concern: Suppression +10% on two compounding rows (×0.33 on a target under both) is the strongest defensive package; it matches the director-approved Blood-Enchanted Eyes suppression on the same 35% / 30% bases.
- Concern: The generated Damage-tier table gives Petal Nightmare's static row an EP tier (40 Normal → 42 Normal); that row is a fixed 40 HP outside the player-jutsu EP ladder, so the label is a renderer limitation.

> **Narrow-kit exception:** Nine nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on six rows, but Damage reaches one meaningful row: Blighted Tree's formula 40 EP hit (60 AP, cooldown 7). Petal Nightmare's Damage row is static, a fixed 40 HP before modifiers, while a 40 EP formula hit scales with level (about 255 HP at user level 50), so each point of Damage there is 1 HP. The former Burst route (Hardened Heartwood → Nightmare in Bloom, +3 Damage) therefore paid ×1.075 on one hit every 7 rounds and was near-dominated by Thousand-Leaf Dream, whose +10% multiplies every non-pierce hit in the Wailing Bark window, Blighted Tree's included when cast there. Nightmare in Bloom is removed rather than re-cut: more Damage would lift Blighted Tree 40 → 45 (Normal → High), and every compatible secondary (Increase Damage Given, Increase Damage Taken, Decrease Damage Given) already owns a route. Hardened Heartwood stays as a +2 Damage leaf, so the self root completes a full build (06, 07, 09, 10), every route keeps two fourth purchases, and no node is in every legal 4-BP build.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ha Yanagi-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Mourning Boughs | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Petal Nightmare, Wailing Bark / 2 |
| 02 | Veil of Falling Petals | Hidden Art | Mourning Boughs | +3% Decrease Damage Given (enemy debuff) | Petal Nightmare, Wailing Bark / 2 |
| 03 | Grave Willow's Hush | Advanced Art | Veil of Falling Petals | +5% Decrease Damage Given (enemy debuff) | Petal Nightmare, Wailing Bark / 2 |
| 04 | Blight Takes Root | Hidden Art | Mourning Boughs | +3% Increase Damage Taken (enemy debuff) | Blighted Tree / 1 |
| 05 | Hollow at the Heart | Advanced Art | Blight Takes Root | +5% Increase Damage Taken (enemy debuff) | Blighted Tree / 1 |
| 06 | Whispering Canopy | Foundation | None | +3% Increase Damage Given (self buff) | Wailing Bark / 1 |
| 07 | Hardened Heartwood | Hidden Art | Whispering Canopy | +2 Damage (damage) | Blighted Tree, Petal Nightmare / 2 |
| 09 | Rising Sap | Hidden Art | Whispering Canopy | +2% Increase Damage Given (self buff) | Wailing Bark / 1 |
| 10 | Thousand-Leaf Dream | Advanced Art | Rising Sap | +5% Increase Damage Given (self buff) | Wailing Bark / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 06→09, 09→10. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Mourning Boughs** — The willow bows under its grief, and every arm raised against it grows heavy. Decrease Damage Given on Wailing Bark 35 → 37% and Petal Nightmare 30 → 32% (enemy, 2 rounds); the two debuffs compound on one target.
- **Veil of Falling Petals** — Petals drift between the foe and its purpose until the blow forgets its aim. Both suppression rows 37 → 40% and 32 → 35% with Mourning Boughs.
- **Grave Willow's Hush** — Beneath the oldest willow nothing strikes true; the grave keeps its quiet. Suppression: Wailing Bark 35 → 45% and Petal Nightmare 30 → 40% on the full route; a target under both deals ×0.55 × 0.60 = ×0.33 on a non-pierce hit (×0.455 at base).
- **Blight Takes Root** — Rot finds the soft heart of a tree, and of a foe, and settles in to stay. Blighted Tree exposure 30 → 33% (enemy, the 2 rounds after the cast, never its own hit); every non-pierce hit the target takes, from any attacker.
- **Hollow at the Heart** — What the blight has hollowed, any passing wind can break. Exposure: Blighted Tree 30 → 38% on the full route, ×1.38 on every non-pierce hit the target takes for 2 rounds, allies' hits included.
- **Whispering Canopy** — The leaves speak in a thousand voices, and all of them say strike. Wailing Bark self Increase Damage Given 35 → 38% (the 2 rounds after each 40 AP cast, cooldown 6); every non-pierce hit you land in that window.
- **Hardened Heartwood** — Seasons of grief turn the willow's soft wood into something that bruises. Blighted Tree's formula Damage 40 → 42 EP (Normal tier), ×1.05 on one 60 AP, cooldown-7 hit; Petal Nightmare's static row is a fixed 40 HP, so +2 there is +2 HP. A leaf: the heavier-strike fourth purchase beside Rising Sap's window.
- **Rising Sap** — Spring climbs the trunk, and the willow remembers how to be fierce. Wailing Bark self buff 38 → 40% with Whispering Canopy.
- **Thousand-Leaf Dream** — Every leaf a dream, every dream a wound; the canopy closes overhead. Sustained amplification: Wailing Bark self buff 35 → 45% on the full route, ×1.45 on every non-pierce hit you land in the 2 rounds after the cast.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT |
|---|---|---:|---:|---:|---:|
| Grave Willow's Hush (Suppression) | Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Whispering Canopy | — | +3% | +10% | — |
| Hollow at the Heart (Exposure) | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Hollow at the Heart | — | — | +5% | +8% |
| Thousand-Leaf Dream (Amplifier) | Whispering Canopy, Rising Sap, Thousand-Leaf Dream, Hardened Heartwood | +2 | +10% | — | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Grave Willow's Hush:** Both Decrease Damage Given rows at +10% (Wailing Bark 45%, Petal Nightmare 40%; ×0.55 × 0.60 = ×0.33 on a non-pierce hit when both sit on one target). Whispering Canopy is the fourth purchase, so the same 40 AP Wailing Bark cast also grants a 38% self buff; Blight Takes Root (exposure 33%) is the alternative.
- **Hollow at the Heart:** Blighted Tree exposure 30 → 38%: ×1.38 on every non-pierce hit the target takes in the 2 rounds after the cast, from you, allies or weapons, never Blighted Tree's own hit. Veil of Falling Petals is the fourth purchase: the route's +2% Decrease Damage Given from Mourning Boughs becomes +5% (suppression 35 → 40% and 30 → 35%), half the Suppression route's +10%. Whispering Canopy (self buff 38%) is the alternative.
- **Thousand-Leaf Dream:** Wailing Bark becomes a 45% self buff for 40 AP on cooldown 6: every non-pierce hit you land in the 2 rounds after the cast, normal jutsu, weapons and basic attacks included, is multiplied by ×1.45 (the bloodline passive applies after it). Hardened Heartwood is the fourth purchase: Blighted Tree 40 → 42 EP, so a Blighted Tree cast inside the window lands ×1.45 × 1.05 ≈ ×1.52 against an unbuffed 40 EP cast. Mourning Boughs (suppression 37% / 32%) is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Suppression | Exposure | Amplifier |
|---|---:|---|---|---:|---:|---:|---:|
| Wailing Bark | 0 | Decrease Damage Given | enemy | 35% | 45% (+10) | 40% (+5) | 35% |
| Wailing Bark | 1 | Increase Damage Given | self | 35% | 38% (+3) | 35% | 45% (+10) |
| Blighted Tree | 0 | Damage | enemy | 40 | 40 | 40 | 42 (+2) |
| Blighted Tree | 1 | Increase Damage Taken | enemy | 30% | 30% | 38% (+8) | 30% |
| Petal Nightmare | 0 | Damage | enemy | 40 | 40 | 40 | 42 (+2) |
| Petal Nightmare | 1 | Decrease Damage Given | enemy | 30% | 40% (+10) | 35% (+5) | 30% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 9, 4: 12
- Full-budget allocations: 12; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Grave Willow's Hush: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Hollow at the Heart: +8% Increase Damage Taken (0 + 3 + 5; off band)
  - Route Thousand-Leaf Dream: +10% Increase Damage Given (3 + 2 + 5; on band)
- Supported rows in kit: 6 (DMG 2, DDG 2, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Blight Takes Root (raw +13, row-weighted 23)
- Lowest row-weighted node: Rising Sap (2)

Validator warnings:

- classification status: requires classification extension (director decision)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Blighted Tree | 0 | 40 (Normal) | 42 (Normal) |
| Petal Nightmare | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Grave Willow's Hush | +10% DDG | Blight Takes Root | +10% DDG, +3% IDT | 23 |
| Grave Willow's Hush | +10% DDG | Whispering Canopy *(highest diagnostic)* | +3% IDG, +10% DDG | 23 |
| Hollow at the Heart | +2% DDG, +8% IDT | Veil of Falling Petals *(highest diagnostic)* | +5% DDG, +8% IDT | 18 |
| Hollow at the Heart | +2% DDG, +8% IDT | Whispering Canopy | +3% IDG, +2% DDG, +8% IDT | 15 |
| Thousand-Leaf Dream | +10% IDG | Mourning Boughs | +10% IDG, +2% DDG | 14 |
| Thousand-Leaf Dream | +10% IDG | Hardened Heartwood *(highest diagnostic)* | +2 Damage, +10% IDG | 14 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Blight Takes Root | +10% DDG, +3% IDT |
| 2 | Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Whispering Canopy | +3% IDG, +10% DDG |
| 3 | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Hollow at the Heart | +5% DDG, +8% IDT |
| 4 | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Whispering Canopy | +3% IDG, +5% DDG, +3% IDT |
| 5 | Mourning Boughs, Veil of Falling Petals, Whispering Canopy, Hardened Heartwood | +2 Damage, +3% IDG, +5% DDG |
| 6 | Mourning Boughs, Veil of Falling Petals, Whispering Canopy, Rising Sap | +5% IDG, +5% DDG |
| 7 | Mourning Boughs, Blight Takes Root, Hollow at the Heart, Whispering Canopy | +3% IDG, +2% DDG, +8% IDT |
| 8 | Mourning Boughs, Blight Takes Root, Whispering Canopy, Hardened Heartwood | +2 Damage, +3% IDG, +2% DDG, +3% IDT |
| 9 | Mourning Boughs, Blight Takes Root, Whispering Canopy, Rising Sap | +5% IDG, +2% DDG, +3% IDT |
| 10 | Mourning Boughs, Whispering Canopy, Hardened Heartwood, Rising Sap | +2 Damage, +5% IDG, +2% DDG |
| 11 | Mourning Boughs, Whispering Canopy, Rising Sap, Thousand-Leaf Dream | +10% IDG, +2% DDG |
| 12 | Whispering Canopy, Hardened Heartwood, Rising Sap, Thousand-Leaf Dream | +2 Damage, +10% IDG |

## Design notes

- Structure: Mourning Boughs (enemy) forks into Veil of Falling Petals → Grave Willow's Hush (suppression) and Blight Takes Root → Hollow at the Heart (exposure); Whispering Canopy (self) forks into Rising Sap → Thousand-Leaf Dream (sustained amplification) and the Hardened Heartwood leaf (+2 Damage). Maxima over every legal allocation: Decrease Damage Given +10%, Increase Damage Given +10%, Increase Damage Taken +8%, Damage +2.
- 2026-10-04 rebalance: the pre-batch Burst route (+5 Damage, both Damage rows 40 → 45) was first cut to +3, then removed: Petal Nightmare's Damage row is static (damageCalc uses raw power for static rows), so the route had one meaningful row, Blighted Tree, and Nightmare in Bloom was near-dominated by Thousand-Leaf Dream. Hardened Heartwood keeps its pre-batch +2 (cut to +1 mid-batch, now restored) and becomes a leaf. Also in this batch: the +2% Decrease Damage Given rider on Hollow at the Heart is removed and Hollow at the Heart +7% → +5% (exposure +10% → +8%); Rising Sap +3% → +2% and Thousand-Leaf Dream +4% → +5%, so Amplifier stays +10% with the payoff on the capstone.
- Fourth purchases: Suppression adds Whispering Canopy (+3% IDG) or Blight Takes Root (+3% IDT); Exposure adds Veil of Falling Petals (+5% DDG in all) or Whispering Canopy; Amplifier adds Hardened Heartwood (+2 Damage) or Mourning Boughs (+2% DDG). No fourth adds to its own route's tag, and none reaches more than half of a sibling route's primary.
- Arithmetic: every percentage row lists all four stat types and no element, so each matches damage of any element (§3). Jutsu-sourced increases multiply the hit in turn and reductions apply in sequence (computeDamagePacket, §3b): Exposure with Whispering Canopy gives ×1.38 × 1.38 ≈ ×1.90 on a hit inside both windows. Formula Damage scales linearly with EP, so +2 Damage is ×1.05 on Blighted Tree at any level. The +15% bloodline Increase Damage Given passive applies last; pierce runs after the modifier pass.
- Delivery: all three casts are OTHER_USER SINGLE. Wailing Bark 40 AP, cooldown 6 (suppression row plus the self buff); Blighted Tree 60 AP, cooldown 7 (formula Damage plus exposure); Petal Nightmare 60 AP, cooldown 6 (static Damage, a fixed 40 HP, plus suppression). Every percentage row is live the two rounds after its cast, never in it, so no cast boosts its own hit. Both suppression debuffs on one target in one round cost 100 AP. Not simulated.

## Risks and unproven interactions

- Classification: no kit row carries an element, so the tree requires a classification extension. 'Ha Yanagi' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. All three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Off-kit coverage is unverified.
- Suppression stacking: Wailing Bark and Petal Nightmare each apply a separate two-round Decrease Damage Given debuff; with BATTLE_TAG_STACKING every active same-tag effect applies (process.ts 1109–1117, §3b) and the reductions compound, so one target's non-pierce hits fall to ×0.65 × 0.70 = ×0.455 at base and ×0.55 × 0.60 = ×0.33 at the +10% route maximum (floor ×0.10). The strongest defensive package in the tree. Not simulated.
- Downstream reach: the Wailing Bark self buff raises normal jutsu, weapons and basic attacks in its window; suppression cuts non-pierce damage from every source the target controls; exposure raises non-pierce hits from allies and weapons, so Hollow at the Heart is worth more in group fights than its single row suggests.
- Single-row routes: Exposure (Blighted Tree, cooldown 7) and Amplifier (Wailing Bark, cooldown 6) each ride one row, live 2 rounds per cast. Exposure stops at +8% because it multiplies every attacker's hits; Hollow at the Heart carries no suppression rider, but the route keeps Mourning Boughs' +2% Decrease Damage Given (+5% with Veil of Falling Petals). Amplifier keeps +10% on the one self row.
- Targeting: all three casts are OTHER_USER and may be aimed at any living non-caster user, allies included (util.ts 2747–2749; actions.ts 1029–1068). Every damage and debuff row has friendly fire none/ALL, so aimed at an ally it damages, suppresses (up to 45%) or exposes (up to 38%) that ally; SINGLE method, so this is player-controlled.
- Pierce and passives: no node touches pierce, and pierce runs after the modifier pass, so suppression and exposure do not change pierce hits. The bloodline's permanent +5% Increase Damage Taken passive (Taijutsu/Bukijutsu, no element) is not a jutsu row; no node raises or removes it.
- Rank and scope: Ha Yanagi is a D-rank bloodline. Blighted Tree's Damage row is formula-calculated, so +2 Damage scales that hit by ×1.05; Petal Nightmare's static row gains a flat +2 HP. Skill-tree effects are skipped in ranked modes; no combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Ha Yanagi-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

