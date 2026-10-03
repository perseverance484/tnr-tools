# Ha Yanagi — Lament of the Willow

**Bloodline:** Ha Yanagi (BR-030, rank D, `uNZ2UMfA3BuX-J_1g0fHU`) · **Revision:** Draft 3 / Ha Yanagi classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Ha Yanagi (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Enemy debuff control: Decrease Damage Given (Wailing Bark, Petal Nightmare) and Increase Damage Taken (Blighted Tree) · secondary Damage on the two damage casts (Blighted Tree formula 40, Petal Nightmare static 40 EP) · tertiary Self amplification: the single Increase Damage Given row on Wailing Bark.

Three of the kit's six supported rows are enemy debuffs: Decrease Damage Given on Wailing Bark (35%) and Petal Nightmare (30%), both two rounds and compounding on one target, and Increase Damage Taken on Blighted Tree (30%), so suppression and exposure are the declared primary (two +10% routes) and hold the heaviest four-purchase builds by row weight (23–24). Damage reaches two rows (40 EP each at jutsu level 25) and is the secondary +5 route. Increase Damage Given is one self row at 35% whose four-stat, element-less filter matches every non-pierce hit the caster lands in the two rounds after the cast; it is tertiary by coverage breadth, not by size (+10% route). Every percentage row in the kit lists all four stat types with no element, so each node's downstream reach is every non-pierce damage effect, not Genjutsu only. Potency reaches matching supported tags on all Ha Yanagi-classified jutsu (RUL-2026-10-03-005; requires a classification extension).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ha Yanagi-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Mourning Boughs | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Petal Nightmare, Wailing Bark / 2 |
| 02 | Veil of Falling Petals | Hidden Art | Mourning Boughs | +3% Decrease Damage Given (enemy debuff) | Petal Nightmare, Wailing Bark / 2 |
| 03 | Grave Willow's Hush | Advanced Art | Veil of Falling Petals | +5% Decrease Damage Given (enemy debuff) | Petal Nightmare, Wailing Bark / 2 |
| 04 | Blight Takes Root | Hidden Art | Mourning Boughs | +3% Increase Damage Taken (enemy debuff) | Blighted Tree / 1 |
| 05 | Hollow at the Heart | Advanced Art | Blight Takes Root | +7% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Blighted Tree, Petal Nightmare, Wailing Bark / 3 |
| 06 | Whispering Canopy | Foundation | None | +3% Increase Damage Given (self buff) | Wailing Bark / 1 |
| 07 | Hardened Heartwood | Hidden Art | Whispering Canopy | +2 Damage (damage) | Blighted Tree, Petal Nightmare / 2 |
| 08 | Nightmare in Bloom | Advanced Art | Hardened Heartwood | +3 Damage (damage); +2% Increase Damage Given (self buff) | Blighted Tree, Petal Nightmare, Wailing Bark / 3 |
| 09 | Rising Sap | Hidden Art | Whispering Canopy | +3% Increase Damage Given (self buff) | Wailing Bark / 1 |
| 10 | Thousand-Leaf Dream | Advanced Art | Rising Sap | +4% Increase Damage Given (self buff) | Wailing Bark / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Mourning Boughs** — The willow bows under its grief, and every arm raised against it grows heavy. Decrease Damage Given on Wailing Bark 35 → 37% and Petal Nightmare 30 → 32%; enemy, 2 rounds, all four stat types; both compound on one target.
- **Veil of Falling Petals** — Petals drift between the foe and its purpose until the blow forgets its aim. Both suppression rows +3% more (40% / 35% with Mourning Boughs); a 40 AP and a 60 AP single-target cast, cooldown 6 each.
- **Grave Willow's Hush** — Beneath the oldest willow nothing strikes true; the grave keeps its quiet. Route total +10%: Wailing Bark 35 → 45%, Petal Nightmare 30 → 40% (×0.55 × 0.60 = ×0.33 on a hit when both debuffs overlap on one target).
- **Blight Takes Root** — Rot finds the soft heart of a tree, and of a foe, and settles in to stay. Blighted Tree exposure only (30 → 33%, cooldown 7), live the 2 rounds after the cast, not on its own hit; every non-pierce hit, any attacker.
- **Hollow at the Heart** — What the blight has hollowed, any passing wind can break. Exposure route total +10% (Blighted Tree 30 → 40%), plus +2% on both suppression rows (39% / 34% with Mourning Boughs). Three enemy rows.
- **Whispering Canopy** — The leaves speak in a thousand voices, and all of them say strike. Wailing Bark self damage buff 35 → 38% (2 rounds after each 40 AP cast, cooldown 6); all four stat types: every non-pierce hit you land.
- **Hardened Heartwood** — Seasons of grief turn the willow's soft wood into something that bruises. Blighted Tree (formula) and Petal Nightmare (static) Damage 40 → 42 EP each; two 60 AP single-target casts at range 4.
- **Nightmare in Bloom** — The dream opens all at once; petals, bark and terror fall together. Route total +5 Damage (45 EP on both rows) and +2% on the Wailing Bark self buff (40% with Whispering Canopy).
- **Rising Sap** — Spring climbs the trunk, and the willow remembers how to be fierce. Wailing Bark self damage buff only (41% with Whispering Canopy); one row, the 2 rounds after the cast, every non-pierce hit you land.
- **Thousand-Leaf Dream** — Every leaf a dream, every dream a wound; the canopy closes overhead. Same self buff; route total +10% (35 → 45%, 2 rounds per 40 AP cast, cooldown 6). No other row touched.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT |
|---|---|---:|---:|---:|---:|
| Grave Willow's Hush (Suppression) | Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Whispering Canopy | — | +3% | +10% | — |
| Hollow at the Heart (Exposure) | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Hollow at the Heart | — | — | +7% | +10% |
| Nightmare in Bloom (Burst) | Whispering Canopy, Hardened Heartwood, Nightmare in Bloom, Rising Sap | +5 | +8% | — | — |
| Thousand-Leaf Dream (Amplifier) | Whispering Canopy, Rising Sap, Thousand-Leaf Dream, Mourning Boughs | — | +10% | +2% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Grave Willow's Hush:** Maximum suppression (+10% on both Decrease Damage Given rows: Wailing Bark 45%, Petal Nightmare 40%, compounding to ×0.55 × 0.60 = ×0.33 on a non-pierce hit when both debuffs sit on one target) with Whispering Canopy, so the same 40 AP Wailing Bark cast also grants a 38% self damage buff for the two rounds after it. The debuffed enemy's non-pierce hits shrink while the caster's later hits grow. Alternative fourth purchase: Blight Takes Root (exposure 33%).
- **Hollow at the Heart:** Pure debuffer: Blighted Tree exposure 30 → 40% (+10%; every non-pierce hit the target takes from you, allies or weapons in the two rounds after the cast, never Blighted Tree's own hit) and +7% on both suppression rows (42% / 37%). All four purchases are enemy-side, so the caster's own numbers are untouched; the heaviest build by row weight (24). Alternative fourth purchase: Whispering Canopy (self buff 38%) in place of Veil of Falling Petals (suppression then 39% / 34%).
- **Nightmare in Bloom:** Raw power: Blighted Tree and Petal Nightmare at 45 EP each (+5 Damage; the static Petal Nightmare row goes 40 → 45 directly, the formula row feeds 45 into its stat scaling), while Wailing Bark's self buff reaches 43% (+3% +2% +3%) and multiplies each damage cast landed in the two rounds after a Wailing Bark cast by ×1.43 (60 AP each, so one per round). Alternative fourth purchase: Mourning Boughs (suppression 37% / 32%, self buff 40%) instead of Rising Sap.
- **Thousand-Leaf Dream:** The willow as a two-sided cast: Wailing Bark becomes a 45% self damage buff (+10%) and a 37% enemy suppression for 40 AP on cooldown 6. Every non-pierce hit the caster lands in the two rounds after the cast, including normal jutsu, weapons and basic attacks, is multiplied by ×1.45 (the bloodline passive applies after it). A thin build by row weight (14), kept as a narrow identity (risk 5). Alternative fourth purchase: Hardened Heartwood (42 EP on both damage casts).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Suppression | Exposure | Burst | Amplifier |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Wailing Bark | 0 | Decrease Damage Given | enemy | 35% | 45% (+10) | 42% (+7) | 35% | 37% (+2) |
| Wailing Bark | 1 | Increase Damage Given | self | 35% | 38% (+3) | 35% | 43% (+8) | 45% (+10) |
| Blighted Tree | 0 | Damage | enemy | 40 | 40 | 40 | 45 (+5) | 40 |
| Blighted Tree | 1 | Increase Damage Taken | enemy | 30% | 30% | 40% (+10) | 30% | 30% |
| Petal Nightmare | 0 | Damage | enemy | 40 | 40 | 40 | 45 (+5) | 40 |
| Petal Nightmare | 1 | Decrease Damage Given | enemy | 30% | 40% (+10) | 37% (+7) | 30% | 32% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +10% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Grave Willow's Hush: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Hollow at the Heart: +10% Increase Damage Taken (0 + 3 + 7; on band)
  - Route Nightmare in Bloom: +5 Damage (0 + 2 + 3; on band)
  - Route Thousand-Leaf Dream: +10% Increase Damage Given (3 + 3 + 4; on band)
- Supported rows in kit: 6 (DMG 2, DDG 2, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Hollow at the Heart (raw +17, row-weighted 24)
- Lowest row-weighted node: Blight Takes Root (3)

Validator warnings:

- classification status: requires classification extension (director decision)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Blight Takes Root | +10% DDG, +3% IDT |
| 2 | Mourning Boughs, Veil of Falling Petals, Grave Willow's Hush, Whispering Canopy | +3% IDG, +10% DDG |
| 3 | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Hollow at the Heart | +7% DDG, +10% IDT |
| 4 | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Whispering Canopy | +3% IDG, +5% DDG, +3% IDT |
| 5 | Mourning Boughs, Veil of Falling Petals, Whispering Canopy, Hardened Heartwood | +2 Damage, +3% IDG, +5% DDG |
| 6 | Mourning Boughs, Veil of Falling Petals, Whispering Canopy, Rising Sap | +6% IDG, +5% DDG |
| 7 | Mourning Boughs, Blight Takes Root, Hollow at the Heart, Whispering Canopy | +3% IDG, +4% DDG, +10% IDT |
| 8 | Mourning Boughs, Blight Takes Root, Whispering Canopy, Hardened Heartwood | +2 Damage, +3% IDG, +2% DDG, +3% IDT |
| 9 | Mourning Boughs, Blight Takes Root, Whispering Canopy, Rising Sap | +6% IDG, +2% DDG, +3% IDT |
| 10 | Mourning Boughs, Whispering Canopy, Hardened Heartwood, Nightmare in Bloom | +5 Damage, +5% IDG, +2% DDG |
| 11 | Mourning Boughs, Whispering Canopy, Hardened Heartwood, Rising Sap | +2 Damage, +6% IDG, +2% DDG |
| 12 | Mourning Boughs, Whispering Canopy, Rising Sap, Thousand-Leaf Dream | +10% IDG, +2% DDG |
| 13 | Whispering Canopy, Hardened Heartwood, Nightmare in Bloom, Rising Sap | +5 Damage, +8% IDG |
| 14 | Whispering Canopy, Hardened Heartwood, Rising Sap, Thousand-Leaf Dream | +2 Damage, +10% IDG |

## Design notes

- Node split: Mourning Boughs (enemy) opens both suppression rows and forks into Veil of Falling Petals → Grave Willow's Hush (suppression) and Blight Takes Root → Hollow at the Heart (exposure). Whispering Canopy (self) opens the Wailing Bark buff and forks into Hardened Heartwood → Nightmare in Bloom (Damage) and Rising Sap → Thousand-Leaf Dream (amplifier). Every Advanced Art is 3 BP deep.
- Routes (RUL-2026-10-03-005): Suppression +10% Decrease Damage Given (Mourning Boughs +2%, Veil of Falling Petals +3%, Grave Willow's Hush +5%); Exposure +10% Increase Damage Taken (Blight Takes Root +3%, Hollow at the Heart +7%); Burst +5 Damage (Hardened Heartwood +2, Nightmare in Bloom +3); Amplifier +10% Increase Damage Given (Whispering Canopy +3%, Rising Sap +3%, Thousand-Leaf Dream +4%). Maxima over every legal allocation: Damage +5, Decrease Damage Given +10%, Increase Damage Taken +10%, Increase Damage Given +10%; not jointly attainable.
- Recalibration from Draft 2: Veil of Falling Petals +2% → +3% and Grave Willow's Hush +4% → +5% (Suppression +8% → +10%); Hollow at the Heart's exposure +5% → +7% (Exposure +8% → +10%; the exposure branch has no Foundation step, so Hidden +3% / Advanced +7% carries the band). Burst and Amplifier were already on band and are unchanged.
- Main tree, passives, pierce: every percentage row lists all four stat types and no element; getEfficiencyRatio returns 1 on any stat overlap, so each matches damage of any element (§3). Jutsu-sourced percentage rows multiply the hit in turn, reductions in sequence (computeDamagePacket, §3b): the Wailing Bark buff raises normal jutsu, weapons and basic attacks in its window, suppression cuts the target's hits, exposure raises allies' hits. The +15% bloodline IDG passive applies last. Pierce runs after the modifier pass.
- Delivery and uptime: all three casts are OTHER_USER SINGLE. Wailing Bark is 40 AP, cooldown 6, range 5 (suppression row plus the SELF buff, so both roots touch it); Blighted Tree 60 AP, cooldown 7, range 4 (formula damage plus exposure); Petal Nightmare 60 AP, cooldown 6, range 4 (static damage plus suppression). Every percentage row is live the two rounds after its cast round, never in it (§3b). Both suppression debuffs on one target in one turn cost 100 AP: ×0.55 × 0.60 = ×0.33 is a ceiling, not a rotation. Not simulated.
- Fourth purchases and dominance: Suppression adds Whispering Canopy (38% buff) or Blight Takes Root (33% exposure); Exposure adds Veil of Falling Petals (42% / 37% suppression) or Whispering Canopy; Burst adds Rising Sap (43% buff) or Mourning Boughs (37% / 32% suppression); Amplifier adds Mourning Boughs or Hardened Heartwood. All 14 full builds are numerically non-dominated and every node appears in one.

## Risks and unproven interactions

- Classification: no kit row carries an element, so the tree requires a classification extension. 'Ha Yanagi' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Off-kit coverage is unverified.
- Suppression stacking: Wailing Bark and Petal Nightmare each apply a separate two-round Decrease Damage Given debuff; with BATTLE_TAG_STACKING on every active same-tag effect applies (process.ts 1109–1117, §3b) and the reductions compound in sequence, so one target's non-pierce hits are cut to ×0.65 × 0.70 = ×0.455 at base and ×0.55 × 0.60 = ×0.33 at the +10% route maximum (floor ×0.10). Not simulated.
- Downstream reach: every percentage row has all four stat types and no element, so the enhanced Wailing Bark self buff raises normal jutsu, weapons and basic attacks in the two rounds after the cast; suppression cuts non-pierce damage from every source the target controls; exposure raises non-pierce hits from allies and weapons.
- Pierce: the kit has no pierce rows and no node touches pierce. At the pin pierce is applied after the damage-modifier pass (process.ts 416-430, 563-577), so the Suppression and Exposure routes do not reduce or amplify enemy pierce hits and the self buff does not raise any pierce the player lands.
- Single-window concentration, accepted as a narrow identity: the Amplifier route's whole value is one 35 → 45% self row live the two rounds after each 40 AP Wailing Bark cast (cooldown 6); its full build is row-weight 14 and Thousand-Leaf Dream (+4%) the lightest Advanced Art. Rising Sap +2% / Thousand-Leaf Dream +5% (still +10%) is a user-owned option (D8). Exposure likewise rides one 30 → 40% Blighted Tree row (cooldown 7).
- Targeting: all three casts are OTHER_USER and may be aimed at any living non-caster user, allies included (util.ts 2747–2749; actions.ts 1029–1068). Every damage and debuff row has friendly fire none/ALL, so aimed at an ally it damages, suppresses (up to 45%) or exposes (up to 40%) that ally, while Wailing Bark's SELF buff still lands on the caster. SINGLE method, so this is player-controlled; the dossier marks no ally-hazard rows.
- Standing self exposure: the bloodline's permanent +5% Increase Damage Taken passive (Taijutsu/Bukijutsu filter, no element, so it also matches every element-less hit) is a passive, not a jutsu row; no node raises or removes it. The dossier marks no adverse supported rows, so no node makes any row worse for the caster.
- Rank and scope: Ha Yanagi is a D-rank bloodline; this tree equalises marginal opportunity, not final strength. Blighted Tree's Damage row is formula-calculated, so +5 Damage lands differently from +5 on Petal Nightmare's static row. Normal-tree potency policy is unapproved; skill-tree effects are skipped in ranked modes; no combat simulation was performed.

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

