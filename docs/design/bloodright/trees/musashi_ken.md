# Musashi Ken — The Drawn Blade

**Bloodline:** Musashi Ken (BR-047, rank D, `EZRt16BYzQRMiGSf_P7is`) · **Revision:** Draft 1 / Musashi Ken classification / forked tree · **Classification:** Musashi Ken (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Bukijutsu tempo — Increase Damage Given (Heiho, Iaido, Iaijutsu; three self rows) · secondary Quick-draw damage — Iaido and Iaijutsu (two formula rows) · tertiary Guard — Decrease Damage Taken (Heiho; one row).

Six supported rows sit on three casts and half of them are the same tag: every jutsu carries a 35% self Increase Damage Given row for 2 rounds (Heiho and Iaijutsu Bukijutsu-filtered with no element, Iaido all four stat types), they stack under BATTLE_TAG_STACKING and sit over a 15% Bukijutsu Increase Damage Given passive, so self amplification is the bloodline's identity and takes the primary route. The two 38-power Bukijutsu / Speed, Strength formula strikes (Iaido single target, Iaijutsu ground circle; 60 AP, cooldown 7 each) are the kit's only direct damage and take the raw-power route. Heiho's single 35% Decrease Damage Taken row (all four stat types, 40 AP, cooldown 5) is the only defensive lever and the only answer to the bloodline's own 5% Increase Damage Taken passive, so it carries one chain as tertiary. Iaijutsu's move row is unsupported.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on six rows (Increase Damage Given x3, Damage x2, Decrease Damage Taken x1); Iaijutsu's move row is unsupported. Drawn Steel forks into a damage route (Single Stroke → Cut of No Return, +6 with Reading the Field, the two-row Damage guardrail) and a tempo route (Second Sword → Two Heavens as One, +6 on three self rows that can stack). Decrease Damage Taken is one row, so Reading the Field runs a single chain (Unbroken Guard → Victory in the Sheath, 35→45%, the Taiyo Kami +10 shape); a fourth Advanced Art would need a second branch under Reading the Field that twins Single Stroke or Second Sword on the same rows, or a guard capstone past +10, and Draft 1 declines both so that each route is the only way to its tag maximum. Because the guard side has three nodes, every legal 4 BP build contains Drawn Steel; a mirrored layout only moves the universal node to the other root. Three distinct complete builds exist (Burst, Tempo, Guard); Burst and Tempo each have two fourth-purchase choices, Guard's fourth purchase is always Drawn Steel. 8 legal full allocations, 7 non-dominated, every node in at least one.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Musashi Ken jutsu (bloodline-keyed classification, proposed extension) under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Drawn Steel | Foundation | None | +2% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 02 | Single Stroke | Hidden Art | Drawn Steel | +2 Damage power (damage) | Iaido, Iaijutsu / 2 |
| 03 | Cut of No Return | Advanced Art | Single Stroke | +3 Damage power (damage) | Iaido, Iaijutsu / 2 |
| 04 | Second Sword | Hidden Art | Drawn Steel | +2% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 05 | Two Heavens as One | Advanced Art | Second Sword | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Heiho, Iaido, Iaijutsu / 4 |
| 06 | Reading the Field | Foundation | None | +2% Decrease Damage Taken (self buff); +1 Damage power (damage) | Heiho, Iaido, Iaijutsu / 3 |
| 07 | Unbroken Guard | Hidden Art | Reading the Field | +3% Decrease Damage Taken (self buff) | Heiho / 1 |
| 08 | Victory in the Sheath | Advanced Art | Unbroken Guard | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Drawn Steel** — Steel leaves the sheath and the whole battle narrows to the length of one blade. All three self damage buffs 35→37%, 2 rounds each: Heiho (40 AP), Iaido and Iaijutsu (Bukijutsu-filtered or element-less hits). 3 rows.
- **Single Stroke** — One stroke, begun and finished before the eye can follow it. Iaido and Iaijutsu Damage 38→40 power; two Bukijutsu / Speed, Strength formula hits, 60 AP, cooldown 7 each. Iaijutsu hits its circle.
- **Cut of No Return** — The blade does not return to the sheath until the matter is settled. Route total +5: Iaido and Iaijutsu 38→43 power (44 with Reading the Field, the two-row Damage guardrail). 2 rows, no gates or hidden rows.
- **Second Sword** — The off hand was never idle; a second edge waits where the first was parried. All three self buffs 35→39% with Drawn Steel; Heiho and Iaido can be up together, Iaijutsu's rides its circle from the next round. 3 rows.
- **Two Heavens as One** — Sword and strategy, long blade and short, drawn as a single will. Route total +6: three self buffs 35→41% (self, 2 rounds each); plus Heiho Decrease Damage Taken 35→37% (39% with Reading the Field). 4 rows.
- **Reading the Field** — Before the first cut, the strategist has already chosen the ground. Heiho Decrease Damage Taken 35→37% (all four stat types, 2 rounds, cooldown 5); Iaido and Iaijutsu Damage 38→39 power. 3 rows.
- **Unbroken Guard** — A guard that does not break is a battle that is not lost. Heiho Decrease Damage Taken only: 37→40% with Reading the Field; one element-less row for every non-pierce hit, 2 rounds per 40 AP cast.
- **Victory in the Sheath** — The master wins with the sword still sheathed; the draw is only a courtesy. Route total +10: Heiho guard 35→45% for 2 rounds; plus all three self damage buffs 35→37% (39% with Drawn Steel). 4 rows.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDT |
|---|---|---:|---:|---:|
| Cut of No Return (Burst) | Drawn Steel, Single Stroke, Cut of No Return, Reading the Field | +6 | +2% | +2% |
| Two Heavens as One (Tempo) | Drawn Steel, Second Sword, Two Heavens as One, Reading the Field | +1 | +6% | +4% |
| Victory in the Sheath (Guard) | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath | +1 | +4% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Cut of No Return:** The +6 power route on both Bukijutsu strikes (Iaido and Iaijutsu 38→44, before the 15% Bukijutsu Increase Damage Given passive and the kit's own buffs multiply them) with all three self buffs at 37%. Reading the Field is the fourth purchase because it supplies the last point of power and lifts Heiho's guard to 37%; Second Sword (buffs 39%, strikes 43) is the all-offence alternative.
- **Two Heavens as One:** The +6 route on all three Increase Damage Given rows (Heiho, Iaido, Iaijutsu 35→41%, self, 2 rounds each): every element-less hit the caster lands inside those windows, including weapon and basic attacks and normal jutsu, is amplified, not only the two kit strikes (39 power from Reading the Field). Heiho's guard reaches 39% from the capstone and the root; Single Stroke (strikes 40, guard 37%) is the alternative fourth purchase.
- **Victory in the Sheath:** Heiho's Decrease Damage Taken at 45% for its 2 rounds every 5-round cooldown, against every non-pierce hit of any stat type, with all three self buffs at 39% (2 from the capstone, 2 from Drawn Steel) and the strikes at 39 power. Drawn Steel is the only possible fourth purchase; the build has no second route.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Tempo | Guard |
|---|---:|---|---|---:|---:|---:|---:|
| Heiho | 0 | Increase Damage Given | self | 35% | 37% (+2) | 41% (+6) | 39% (+4) |
| Heiho | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 39% (+4) | 45% (+10) |
| Iaido | 0 | Damage | enemy | 38 | 44 (+6) | 39 (+1) | 39 (+1) |
| Iaido | 1 | Increase Damage Given | self | 35% | 37% (+2) | 41% (+6) | 39% (+4) |
| Iaijutsu | 0 | Damage | enemy | 38 | 44 (+6) | 39 (+1) | 39 (+1) |
| Iaijutsu | 1 | Increase Damage Given | self | 35% | 37% (+2) | 41% (+6) | 39% (+4) |
| Iaijutsu | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +6, Increase Damage Given +6%, Decrease Damage Taken +10% (not jointly attainable)
- Supported rows in kit: 6 (DMG 2, DDT 1, IDG 3)
- Strongest full build by row-weighted total: Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath (raw +15, row-weighted 24)
- Lowest row-weighted node: Unbroken Guard (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Drawn Steel, Single Stroke, Cut of No Return, Second Sword | DMG +5, IDG +4 |
| 2 | Drawn Steel, Single Stroke, Cut of No Return, Reading the Field | DMG +6, IDG +2, DDT +2 |
| 3 | Drawn Steel, Single Stroke, Second Sword, Two Heavens as One | DMG +2, IDG +6, DDT +2 |
| 4 | Drawn Steel, Single Stroke, Second Sword, Reading the Field | DMG +3, IDG +4, DDT +2 |
| 5 | Drawn Steel, Single Stroke, Reading the Field, Unbroken Guard | DMG +3, IDG +2, DDT +5 |
| 6 | Drawn Steel, Second Sword, Two Heavens as One, Reading the Field | DMG +1, IDG +6, DDT +4 |
| 7 | Drawn Steel, Second Sword, Reading the Field, Unbroken Guard | DMG +1, IDG +4, DDT +5 |
| 8 | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath | DMG +1, IDG +4, DDT +10 |

## Design notes

- Node split: 2 Foundations, 3 Hidden Arts, 3 Advanced Arts. Drawn Steel (IDG +2 on all three self rows) forks into Single Stroke → Cut of No Return (Damage +2/+3) and Second Sword → Two Heavens as One (IDG +2, then IDG +2 with DDT +2). Reading the Field (DDT +2 on Heiho, Damage +1 on both strikes) runs one chain through Unbroken Guard → Victory in the Sheath (DDT +3, then DDT +5 with IDG +2). Every Advanced Art is 3 BP deep; two cost 5 BP under the shared root or 6 BP across roots.
- Flats by coverage: Damage reaches two 38-power rows, so the route totals +6 (1+2+3; 38→44), the two-row guardrail Lycanthropy and Loup-Garou use; the +1 sits on the guard root so Burst's fourth purchase weighs power plus guard against tempo. IDG reaches three self rows that stack, so it is held to +6 (2+2+2; 35→41% per row), between Taiyo Kami's two-row +5 and the two-row +7 of Lycanthropy and Tenohira Musei. DDT is one row and takes 2+3+5 = +10 (35→45%), the Golden Mantle / Sovereign Sun shape.
- Interactions: every supported row is element-less. The Bukijutsu filter on Heiho's and Iaijutsu's IDG is not binding: it matches every element-less hit of any stat type (weapons, basic attacks, non-elemental jutsu) and excludes only elemental Nin/Gen/Tai hits; Iaido's IDG and Heiho's DDT list all four stat types and match every non-pierce hit. Each adds power/100 × the staged base per hit; the 15% Bukijutsu IDG passive is bloodline-sourced and multiplies in its own stage. Pierce is untouched.
- Delivery and uptime: Heiho is a 40 AP self cast, cooldown 5, so its 2-round IDG and DDT windows cover at most 2 of 5 rounds. Iaido (single target, range 4) and Iaijutsu (ground circle, range 5) cost 60 AP, cooldown 7. Iaijutsu's damage hits enemies on the tiles; its move row sorts last and carries the caster in, so its IDG arrives from the next round and only while standing there. Heiho plus Iaido cost 100 AP; cast together, two IDG rows overlap for 2 rounds (70% base, 82% on the tempo route).
- Fourth purchases: Burst (01,02,03) takes Reading the Field (strikes 44, guard 37%) or Second Sword (strikes 43, buffs 39%); Tempo (01,04,05) takes Reading the Field (guard 39%, strikes 39) or Single Stroke (strikes 40, guard 37%); Guard (06,07,08) can only add Drawn Steel (buffs 39%). Hybrids 01,02,04,06 (strikes 41, buffs 39%, guard 37%) and 01,02,06,07 (strikes 41, guard 40%) are non-dominated; 01,04,06,07 is dominated by the Guard build. 8 full allocations, 7 non-dominated, every node in one.
- Row-weighted value: the Tempo builds (01,02,04,05 and 01,04,05,06) and the Guard build (01,06,07,08) are the strongest full allocations at 24; Burst runs 20–22 and the weakest hybrid 17. Dai Kenja peaks at 24 on six rows, Lycanthropy at 20 on five, Taiyo Kami at 31 on nine. Lowest-value purchases are Unbroken Guard (+3 on one row) and Reading the Field (+2 on one row, +1 on two); both are the price of the kit's only defensive lever and neither gates anything that out-bids a sibling.

## Risks and unproven interactions

- Classification: no row carries an element, so the tree needs the proposed bloodline-keyed label (Musashi Ken); under the current resolver all 6 supported rows fall back to None, which also reaches every non-elemental row on any jutsu the player casts. Whether NORMAL/SPECIAL/EVENT jutsu collide is unverified (no non-bloodline catalog with effect rows in the repository).
- Broad self amplification (user-owned value): Two Heavens as One puts all three IDG rows at 41% for 2 rounds; Heiho and Iaido cast in one round overlap for +12 points on every element-less or Bukijutsu non-pierce hit (weapons, basic attacks, normal jutsu), Iaijutsu's row is a conditional third, and the 15% passive stacks on top. +5 (Second Sword +1) or +7 (capstone IDG +3, no DDT) are the options.
- Iaijutsu buff timing: the IDG row rides a ground circle (EMPTY_GROUND, friendly fire ALL); the move row sorts last and carries the caster in, so the buff lands from the following round and only while the caster stays on the tiles. Realized uptime can fall below the nominal 2 rounds, and whether allies in the circle also receive the buff was not verified (the dossier derives the recipient as self).
- Universal opener: every legal full build contains Drawn Steel because the guard side has three nodes. Moving the tempo chain under Reading the Field only makes that root universal instead; on six rows and three tags the brief's preference for no mandatory opener cannot be met without a twinned Hidden Art.
- Guard is one row at 40% uptime: Victory in the Sheath puts Heiho's DDT at 45% for 2 rounds per 5-round cooldown against every non-pierce hit of any stat type (pierce is applied after the modifiers). It stacks with other DDT sources and runs against the bloodline's own 5% IDT passive on Nin/Gen/Tai hits, which no node changes. +8 (capstone +3) is the lighter alternative to Taiyo Kami's +10.
- Damage is formula-calculated (sqrt stat scaling on Bukijutsu / Speed, Strength) and then multiplied by the Bukijutsu IDG passive and any active buff, so +6 raw power is not a linear +6 damage. Both strikes cost 60 AP with cooldown 7, so each Damage row fires at most once per 7 rounds, and Cut of No Return is the lowest-weight capstone (+3 on two rows). No combat simulation was performed.
- Unsupported rows and modes: Iaijutsu's move receives nothing; the bloodline passives (15% Bukijutsu IDG, 5% IDT, sealprevent) are not jutsu rows. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin. No hidden, item-gated, mode-restricted, adverse or ally-hazard rows exist in this kit.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Musashi Ken jutsu inherit Musashi Ken potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

