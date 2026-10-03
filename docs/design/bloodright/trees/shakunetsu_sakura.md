# Shakunetsu Sakura — Dragon of Falling Petals

**Bloodline:** Shakunetsu Sakura (BR-064, rank A, `aa1lZukkHpz6ihmcxLaei`) · **Revision:** Draft 2 / Scorch classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Scorch (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Scorch area damage on the Hiru-Sakura circles (Sakuragari, Sakura-ame) · secondary Increase Damage Taken exposure (Sakuragari circle, Sakura Dragon Tree) and the Sakura Dragon Tree self Increase Damage Given · tertiary Decrease Damage Given suppression (Sakura-ame) and Heal (Sakura Dragon Pearl).

Seven supported rows on four of the five casts. The two A-rank Hiru-Sakura circles carry the only Damage rows (Sakuragari 40 and Sakura-ame 50 EP at jutsu level 25, one hit on every user inside the radius-1 area) and are the declared primary; the kit's Damage Over Time trait lives on Dancing Embers' unsupported wound. Increase Damage Taken is the broadest tag by reach (two 35% rows on the Sakuragari circle and the Sakura Dragon Tree, all four stat types and no element, so every non-pierce hit on the exposed target is amplified), and the D-rank 40 AP Sakura Dragon Tree also carries the kit's single 35% self Increase Damage Given (Fire, None, Scorch, Wind) on top of the bloodline's same-element passive, so those two share the secondary. Decrease Damage Given (Sakura-ame 30%, enemies only) and the Sakura Dragon Pearl's static 25 Heal (250 HP per tick) are single rows. Potency reaches matching supported tags on all Scorch jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Scorch jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Ember Dragon's Roots | Foundation | None | +2% Increase Damage Given (self buff); +2% Heal (self buff) | Asazakura – Sakura Dragon Tree, Yozakura: Sakura Dragon Pearl / 2 |
| 02 | Kindled Boughs | Hidden Art | Ember Dragon's Roots | +3% Increase Damage Given (self buff) | Asazakura – Sakura Dragon Tree / 1 |
| 03 | Dragon in Full Blossom | Advanced Art | Kindled Boughs | +5% Increase Damage Given (self buff); +3% Heal (self buff) | Asazakura – Sakura Dragon Tree, Yozakura: Sakura Dragon Pearl / 2 |
| 04 | Branded by Petals | Hidden Art | Ember Dragon's Roots | +2% Increase Damage Taken (enemy debuff) | Asazakura – Sakura Dragon Tree, Hiru-Sakura: Sakuragari / 2 |
| 05 | Scorching Hanami | Advanced Art | Branded by Petals | +3% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Asazakura – Sakura Dragon Tree, Hiru-Sakura: Sakuragari / 3 |
| 06 | Falling Ember Petals | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Hiru-Sakura: Sakura-ame / 1 |
| 07 | Burning Petal Carpet | Hidden Art | Falling Ember Petals | +2 Damage (damage) | Hiru-Sakura: Sakura-ame, Hiru-Sakura: Sakuragari / 2 |
| 08 | Conflagration in Bloom | Advanced Art | Burning Petal Carpet | +3 Damage (damage) | Hiru-Sakura: Sakura-ame, Hiru-Sakura: Sakuragari / 2 |
| 09 | Smothering Petal Rain | Hidden Art | Falling Ember Petals | +3% Decrease Damage Given (enemy debuff) | Hiru-Sakura: Sakura-ame / 1 |
| 10 | Deluge of Burning Petals | Advanced Art | Smothering Petal Rain | +5% Decrease Damage Given (enemy debuff); +1 Damage (damage) | Hiru-Sakura: Sakura-ame, Hiru-Sakura: Sakuragari / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Ember Dragon's Roots** — Night pearl and morning bough: the dragon stirs before the blossoms burn. Sakura Dragon Tree self damage buff 35 → 37% (2 rounds per 40 AP cast); Sakura Dragon Pearl Heal 25 → 27 (270 HP per tick).
- **Kindled Boughs** — Every branch of the dragon tree catches, and the heat carries into each strike. Sakura Dragon Tree self buff only: 37 → 40% with Ember Dragon's Roots; Scorch, Fire, Wind and element-less hits.
- **Dragon in Full Blossom** — At the height of its bloom the dragon burns brightest and does not tire. Amplifier: Sakura Dragon Tree self buff 35 → 45% on the full route (+10%); Sakura Dragon Pearl Heal 25 → 30 with Ember Dragon's Roots (300 HP per tick).
- **Branded by Petals** — Where a scorched petal lands, the mark stays and every blow finds it. Exposure on the Sakuragari circle (ally hazard) and the Sakura Dragon Tree, 35 → 37% for 2 rounds; amplifies every non-pierce hit on the target.
- **Scorching Hanami** — The blossom-viewing turns to a hunt, and the dragon watches it burn. Both exposure rows 35 → 40% on the full route (+5%; Sakuragari circle is an ally hazard); Sakura Dragon Tree self buff 37 → 39% with Ember Dragon's Roots.
- **Falling Ember Petals** — Petals drift down already alight, and whatever they settle on burns. Sakura-ame Decrease Damage Given 30 → 32% (enemies only, 2 rounds). No Damage here, so the Damage route stays at +5.
- **Burning Petal Carpet** — The ground beneath the blossoms is a carpet of embers. Sakuragari and Sakura-ame Scorch area damage 40 → 42 / 50 → 52 EP (60 AP, range 4, cooldown 7). Ally hazard.
- **Conflagration in Bloom** — The whole orchard goes up at once. Burst: Sakuragari 40 → 45 and Sakura-ame 50 → 55 EP on the full route (+5 Damage), before the Scorch Increase Damage Given passive applies.
- **Smothering Petal Rain** — Blossom rain thick enough to choke the breath from a strike. Sakura-ame Decrease Damage Given only (2 rounds, enemies inside the circle): 32 → 35% with Falling Ember Petals.
- **Deluge of Burning Petals** — Under the burning rain nothing they throw lands whole, and the petals keep scalding. Suppression: Sakura-ame 30 → 40% Decrease Damage Given on the full route (+10%); Sakuragari and Sakura-ame area damage +1 (41 / 51 EP, or 43 / 53 with Burning Petal Carpet). Ally hazard.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | HEAL |
|---|---|---:|---:|---:|---:|---:|
| Conflagration in Bloom (Burst) | Ember Dragon's Roots, Falling Ember Petals, Burning Petal Carpet, Conflagration in Bloom | +5 | +2% | +2% | — | +2% |
| Scorching Hanami (Exposure) | Ember Dragon's Roots, Branded by Petals, Scorching Hanami, Falling Ember Petals | — | +4% | +2% | +5% | +2% |
| Dragon in Full Blossom (Amplifier) | Ember Dragon's Roots, Kindled Boughs, Dragon in Full Blossom, Branded by Petals | — | +10% | — | +2% | +5% |
| Deluge of Burning Petals (Suppression) | Falling Ember Petals, Burning Petal Carpet, Smothering Petal Rain, Deluge of Burning Petals | +3 | — | +10% | — | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Conflagration in Bloom:** +5 Damage on both Scorch circles (Sakuragari 40 → 45, Sakura-ame 50 → 55 EP at jutsu level 25, one hit on every user inside the radius-1 area, before the bloodline's Scorch damage passive multiplies) with Sakura-ame's suppression at 32%. Ember Dragon's Roots is the fourth purchase so the Sakura Dragon Tree buff sits at 37% and the Pearl ticks 270 HP; Smothering Petal Rain (suppression 35%) is the all-control alternative.
- **Scorching Hanami:** Both Increase Damage Taken rows reach 40% for 2 rounds (Sakuragari circle on everyone inside it, Sakura Dragon Tree on one target; compounding to ×1.96 on a target caught by both), amplifying every non-pierce hit the exposed target takes from the kit, normal jutsu, weapons and allies; the Sakura Dragon Tree self buff is 39% and the Pearl ticks 270 HP. Falling Ember Petals is the fourth purchase (suppression 32%); Kindled Boughs (self buff 42%) is the all-dragon alternative.
- **Dragon in Full Blossom:** Sakura Dragon Tree as a two-round amplifier: its self Increase Damage Given reaches 45% and multiplies every Scorch, Fire, Wind or element-less hit landed in the window, including the circles, normal jutsu and basic attacks, with the Pearl at 300 HP per tick. Branded by Petals is the fourth purchase so both exposure rows sit at 37%; Falling Ember Petals (suppression 32%) is the alternative.
- **Deluge of Burning Petals:** Sakura-ame's Decrease Damage Given at the +10% route maximum (30 → 40% on every enemy inside the circle, 2 rounds) with +3 Damage on both circles (43 / 53 EP). Burning Petal Carpet is the fourth purchase; Ember Dragon's Roots (circles 41 / 51 EP, self buff 37%, Pearl 270 HP) is the alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Amplifier | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Yozakura: Sakura Dragon Pearl | 0 | Heal | self | 25 | 27 (+2) | 27 (+2) | 30 (+5) | 25 |
| Yozakura: Sakura Dragon Pearl | 1 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Yozakura: Dancing Embers | 0 | pierce (unsupported) | enemy | 60 | 60 | 60 | 60 | 60 |
| Yozakura: Dancing Embers | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Yozakura: Dancing Embers | 2 | visual (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Hiru-Sakura: Sakuragari | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 43 (+3) |
| Hiru-Sakura: Sakuragari | 1 | Increase Damage Taken | enemy | 35% | 35% | 40% (+5) | 37% (+2) | 35% |
| Hiru-Sakura: Sakuragari | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Hiru-Sakura: Sakura-ame | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 53 (+3) |
| Hiru-Sakura: Sakura-ame | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 30% | 40% (+10) |
| Hiru-Sakura: Sakura-ame | 2 | visual (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Asazakura – Sakura Dragon Tree | 0 | Increase Damage Given | self | 35% | 37% (+2) | 39% (+4) | 45% (+10) | 35% |
| Asazakura – Sakura Dragon Tree | 1 | Increase Damage Taken | enemy | 35% | 35% | 40% (+5) | 37% (+2) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +5% Increase Damage Taken, +5% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Dragon in Full Blossom: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route Scorching Hanami: +5% Increase Damage Taken (0 + 2 + 3; on band)
  - Route Conflagration in Bloom: +5 Damage (0 + 2 + 3; on band)
  - Route Deluge of Burning Petals: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 7 (DMG 2, DDG 1, HEAL 1, IDG 1, IDT 2)
- Strongest full build by row-weighted total: Ember Dragon's Roots, Kindled Boughs, Dragon in Full Blossom, Branded by Petals (raw +17, row-weighted 19)
- Lowest row-weighted node: Falling Ember Petals (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Hiru-Sakura: Sakura-ame#0, Hiru-Sakura: Sakuragari#0, Hiru-Sakura: Sakuragari#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Ember Dragon's Roots, Kindled Boughs, Dragon in Full Blossom, Branded by Petals | +10% IDG, +2% IDT, +5% HEAL |
| 2 | Ember Dragon's Roots, Kindled Boughs, Dragon in Full Blossom, Falling Ember Petals | +10% IDG, +2% DDG, +5% HEAL |
| 3 | Ember Dragon's Roots, Kindled Boughs, Branded by Petals, Scorching Hanami | +7% IDG, +5% IDT, +2% HEAL |
| 4 | Ember Dragon's Roots, Kindled Boughs, Branded by Petals, Falling Ember Petals | +5% IDG, +2% DDG, +2% IDT, +2% HEAL |
| 5 | Ember Dragon's Roots, Kindled Boughs, Falling Ember Petals, Burning Petal Carpet | +2 Damage, +5% IDG, +2% DDG, +2% HEAL |
| 6 | Ember Dragon's Roots, Kindled Boughs, Falling Ember Petals, Smothering Petal Rain | +5% IDG, +5% DDG, +2% HEAL |
| 7 | Ember Dragon's Roots, Branded by Petals, Scorching Hanami, Falling Ember Petals | +4% IDG, +2% DDG, +5% IDT, +2% HEAL |
| 8 | Ember Dragon's Roots, Branded by Petals, Falling Ember Petals, Burning Petal Carpet | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% HEAL |
| 9 | Ember Dragon's Roots, Branded by Petals, Falling Ember Petals, Smothering Petal Rain | +2% IDG, +5% DDG, +2% IDT, +2% HEAL |
| 10 | Ember Dragon's Roots, Falling Ember Petals, Burning Petal Carpet, Conflagration in Bloom | +5 Damage, +2% IDG, +2% DDG, +2% HEAL |
| 11 | Ember Dragon's Roots, Falling Ember Petals, Burning Petal Carpet, Smothering Petal Rain | +2 Damage, +2% IDG, +5% DDG, +2% HEAL |
| 12 | Ember Dragon's Roots, Falling Ember Petals, Smothering Petal Rain, Deluge of Burning Petals | +1 Damage, +2% IDG, +10% DDG, +2% HEAL |
| 13 | Falling Ember Petals, Burning Petal Carpet, Conflagration in Bloom, Smothering Petal Rain | +5 Damage, +5% DDG |
| 14 | Falling Ember Petals, Burning Petal Carpet, Smothering Petal Rain, Deluge of Burning Petals | +3 Damage, +10% DDG |

## Design notes

- Node split: two roots mirror the kit's two faces. Ember Dragon's Roots (Pearl, Dragon Tree) forks into Kindled Boughs → Dragon in Full Blossom (Increase Damage Given) and Branded by Petals → Scorching Hanami (Increase Damage Taken). Falling Ember Petals (the two Hiru-Sakura circles) forks into Burning Petal Carpet → Conflagration in Bloom (Damage) and Smothering Petal Rain → Deluge of Burning Petals (Decrease Damage Given). 2F/4H/4A; every Advanced Art is 3 BP deep; any two cost 5 or 6 BP.
- Routes: Amplifier +10% Increase Damage Given (Ember Dragon's Roots +2%, Kindled Boughs +3%, Dragon in Full Blossom +5%; 35 → 45%); Burst +5 Damage (Burning Petal Carpet +2, Conflagration in Bloom +3); Suppression +10% Decrease Damage Given (Falling Ember Petals +2%, Smothering Petal Rain +3%, Deluge of Burning Petals +5%; 30 → 40%); Exposure +5% Increase Damage Taken (Branded by Petals +2%, Scorching Hanami +3%), held to the 5 band because its two rows stack on one target (35 → 40% each; on a target caught by both they compound, ×1.40 × 1.40 ≈ ×1.96). Falling Ember Petals carries no Damage, so no allocation exceeds +5 Damage; Heal peaks at +5% (Roots +2%, Dragon in Full Blossom +3%; Pearl 25 → 30, 300 HP a tick). Capstone secondaries under-bid the Hidden Art on their tag (Increase Damage Given +2% < Kindled Boughs +3%; Damage +1 < Burning Petal Carpet +2).
- Interactions: the Dragon Tree buff row (Fire, None, Scorch, Wind) multiplies the Scorch circles, element-less hits (basic attacks, weapons) and Fire/Wind jutsu in its 2-round window; the bloodline's same-element Increase Damage Given passive (25 + 0.15/level) multiplies last. Both Increase Damage Taken rows list all four stat types and no element, so every hit on the exposed target, from the player, allies or weapons, is amplified. Pierce runs after the modifier pass and is neither raised nor amplified.
- Delivery: every cast has cooldown 7. Sakuragari and Sakura-ame are 60 AP OTHER_USER AOE_CIRCLE_SPAWN casts at range 4; per the batch-1 Aerathiel read, their INHERIT rows land once on every other living user in the radius-1 circle, with no ground effect: one Scorch hit and 2-round debuffs per user. The Dragon Tree is a 40 AP single-target cast at range 5 (legal target needed; self buff and enemy exposure together). The Pearl is a 40 AP self cast; its Heal ticks on following rounds.
- Fourth purchases: Burst → Ember Dragon's Roots (buff 37%, Pearl 270 HP) or Smothering Petal Rain (suppression 35%); Exposure → Falling Ember Petals (suppression 32%) or Kindled Boughs (buff 42%); Amplifier → Branded by Petals (exposure 37%) or Falling Ember Petals (suppression 32%); Suppression → Burning Petal Carpet (circles 43 / 53 EP) or Ember Dragon's Roots (circles 41 / 51 EP). No-capstone hybrids: 01, 02, 04, 06 (buff 40%, exposure 37%) and 01, 06, 07, 09 (circles 42 / 52 EP, suppression 35%).

## Risks and unproven interactions

- Classification: Scorch is the single qualifying element; sharing it with Taiyo Kami is expected (RUL-2026-10-03-005). 3 of 7 kit rows carry Scorch; the 4 element-less rows need the proposed jutsu-classification resolver, and Sakura Dragon Pearl carries no Scorch row, so in-kit it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Scorch coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN) is unverified.
- Ally hazard: Sakuragari rows 0 (Damage) and 1 (exposure) and Sakura-ame row 0 (Damage) are AOE_CIRCLE_SPAWN rows with no friendlyFire value (=ALL), so allies inside the radius-1 circle take the enhanced Scorch hit and exposure too; the caster is never a target (batch-1 read). Nodes 07, 08 and 10 (Damage) and 04 and 05 (Increase Damage Taken) raise that; positioning decides. Sakura-ame's suppression row is ENEMIES only.
- Exposure stacking: the Sakuragari circle and the Dragon Tree each apply a separate 2-round Increase Damage Taken debuff and BATTLE_TAG_STACKING is on at the pin, so on a target caught by both the two rows compound: every non-pierce hit from the player, allies and weapons is multiplied by ×1.35 × 1.35 ≈ ×1.82 at base and ×1.40 × 1.40 ≈ ×1.96 at the +5% route maximum. The route is held to +5% and both exposure nodes sit on one branch for this reason; not simulated.
- Increase Damage Given reach: the Sakura Dragon Tree self buff (Fire, None, Scorch, Wind) multiplies normal jutsu, weapons and basic attacks in its window, not only kit casts, and the bloodline's same-element passive (about 29% at level 25) multiplies after it; 45% is far below the 100 cap.
- Area delivery: the dossier footnote calls AOE_CIRCLE_SPAWN rows re-applied ground effects reaching the caster; the batch-1 Aerathiel read found OTHER_USER circles apply INHERIT rows once, directly to users in the radius-1 area, with no ground effect and the caster excluded. This tree follows that read, unverified here; if the circles persist, the Damage route is worth more than stated.
- Unsupported rows: Dancing Embers (pierce 60, wound 30%), the Pearl's debuffprevent, Sakuragari's self shield and the visual rows receive no bonus. Because pierce bypasses the damage-modifier pass, the Amplifier and Exposure routes do not raise the pierce hit and the Suppression route does not reduce enemy pierce; the kit's B-rank attack is outside every node.
- Heal: the Pearl's Heal row is static (×10 HP per tick) and applies on following rounds, so +5% Heal at the maximum is 300 HP per tick against 250; tick count per cast and healprevent were not simulated. Heal appears only on the dragon root (Foundation +2%, Dragon in Full Blossom +3%).
- Damage rows are formula-calculated (sqrt stat scaling) and then multiplied by the Scorch Increase Damage Given passive, so +5 Damage is not a linear +5. Skill-tree and bloodline effects are suppressed in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Scorch jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

