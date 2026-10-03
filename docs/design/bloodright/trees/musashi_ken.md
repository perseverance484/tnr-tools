# Musashi Ken — The Drawn Blade

**Bloodline:** Musashi Ken (BR-047, rank D, `EZRt16BYzQRMiGSf_P7is`) · **Revision:** Draft 4 / Musashi Ken classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Musashi Ken (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Bukijutsu tempo — Increase Damage Given (Heiho, Iaido, Iaijutsu; three self rows) · secondary Quick-draw damage — Iaido and Iaijutsu (two formula rows) · tertiary Guard — Decrease Damage Taken (Heiho; one row).

Six supported rows sit on three casts and half are one tag: every jutsu carries a 35% self Increase Damage Given row for 2 rounds (Heiho and Iaijutsu Bukijutsu-filtered with no element, Iaido all four stat types); each lands on the caster at cast time, is live the two rounds after, and same-tag rows compound, so self amplification is the identity and takes the primary route. The two 38-power Bukijutsu / Speed, Strength formula strikes (Iaido single target, Iaijutsu ground circle; 60 AP, cooldown 7 each) are the only direct damage and take the raw-power route. Heiho's single 35% Decrease Damage Taken row (all four stat types, 40 AP, cooldown 5) is the only defensive lever and the kit's only answer to the bloodline's 5% Increase Damage Taken passive, so it carries the guard chain as tertiary; Iaijutsu's move row is unsupported.

> **Narrow-kit exception:** Nine nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on six rows (Increase Damage Given x3, Damage x2, Decrease Damage Taken x1); Iaijutsu's move row is unsupported. Drawn Steel forks into a Damage route (+5 on two strikes) and a tempo route (+5% on three self rows that compound). Decrease Damage Taken is one row, so Reading the Field runs a single guard chain (35 → 45%, +10%) plus one leaf, Answering Cut (Damage +2). A fourth Advanced Art would twin the Damage or tempo capstone on the same rows, or push guard past +10%. The leaf gives the guard side a 4 BP build without Drawn Steel, so no node is in every build. Three distinct complete builds (Burst, Tempo, Guard), each with two fourth-purchase choices.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Musashi Ken-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Drawn Steel | Foundation | None | +2% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 02 | Single Stroke | Hidden Art | Drawn Steel | +2 Damage (damage) | Iaido, Iaijutsu / 2 |
| 03 | Cut of No Return | Advanced Art | Single Stroke | +3 Damage (damage) | Iaido, Iaijutsu / 2 |
| 04 | Second Sword | Hidden Art | Drawn Steel | +1% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 05 | Two Heavens as One | Advanced Art | Second Sword | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Heiho, Iaido, Iaijutsu / 4 |
| 06 | Reading the Field | Foundation | None | +2% Decrease Damage Taken (self buff) | Heiho / 1 |
| 07 | Unbroken Guard | Hidden Art | Reading the Field | +3% Decrease Damage Taken (self buff) | Heiho / 1 |
| 08 | Victory in the Sheath | Advanced Art | Unbroken Guard | +5% Decrease Damage Taken (self buff); +1% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 4 |
| 09 | Answering Cut | Hidden Art | Reading the Field | +2 Damage (damage) | Iaido, Iaijutsu / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Drawn Steel** — Steel leaves the sheath and the whole battle narrows to the length of one blade. All three self buffs 35 → 37%, 2 rounds: Heiho and Iaijutsu (Bukijutsu-filtered or element-less hits), Iaido (every non-pierce hit). 3 rows.
- **Single Stroke** — One stroke, begun and finished before the eye can follow it. Iaido and Iaijutsu Damage 38 → 40 EP; two Bukijutsu / Speed, Strength formula hits, 60 AP, cooldown 7 each. Iaijutsu hits enemies only.
- **Cut of No Return** — The blade does not return to the sheath until the matter is settled. Route total +5 Damage: Iaido and Iaijutsu 38 → 43 EP. 2 rows, no gates or hidden rows.
- **Second Sword** — The off hand was never idle; a second edge waits where the first was parried. All three self buffs 37 → 38% with Drawn Steel; each lands on the caster at cast time and is live the 2 rounds after. 3 rows.
- **Two Heavens as One** — Sword and strategy, long blade and short, drawn as a single will. Route total +5%: three self buffs 35 → 40% (self, 2 rounds each); plus Heiho Decrease Damage Taken 35 → 37% (39% with Reading the Field). 4 rows.
- **Reading the Field** — Before the first cut, the strategist has already chosen the ground. Heiho Decrease Damage Taken 35 → 37% (all four stat types, 2 rounds, cooldown 5). 1 row.
- **Unbroken Guard** — A guard that does not break is a battle that is not lost. Heiho Decrease Damage Taken only: 37 → 40% with Reading the Field; one element-less row for every non-pierce hit, 2 rounds per 40 AP cast.
- **Victory in the Sheath** — The master wins with the sword still sheathed; the draw is only a courtesy. Route total +10%: Heiho guard 35 → 45% for 2 rounds; plus all three self damage buffs +1% (36%, 38% with Drawn Steel). 4 rows.
- **Answering Cut** — Let the enemy commit first; the cut that answers lands before the attack does. Iaido and Iaijutsu Damage 38 → 40 EP: the guard side's strike option (Reading the Field is its prerequisite). 2 rows, no gates.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDT |
|---|---|---:|---:|---:|
| Cut of No Return (Burst) | Drawn Steel, Single Stroke, Cut of No Return, Reading the Field | +5 | +2% | +2% |
| Two Heavens as One (Tempo) | Drawn Steel, Second Sword, Two Heavens as One, Reading the Field | — | +5% | +4% |
| Victory in the Sheath (Guard) | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath | — | +3% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Cut of No Return:** +5 Damage on both Bukijutsu strikes (Iaido and Iaijutsu 38 → 43 EP) with all three self buffs at 37%. The 15% passive and buffs live from an earlier round multiply each strike; neither strike benefits from its own IDG row. Reading the Field is the fourth purchase because it lifts Heiho's guard to 37% without competing for the strike rows; Second Sword (buffs 38%) is the all-offence alternative.
- **Two Heavens as One:** The +5% route on all three Increase Damage Given rows (Heiho, Iaido, Iaijutsu 35 → 40%, each landing on the caster at cast time and live the 2 rounds after): every element-less hit the caster lands in those windows, weapons, basic attacks and normal jutsu included, is multiplied by each live row in turn. Heiho and Iaido cast together (100 AP) multiply the Iaijutsu strike next round by ×1.40 × 1.40 = ×1.96, and all three are live the round after (≈ ×2.74). Heiho's guard reaches 39% from the capstone and Reading the Field; Single Stroke (strikes 40 EP, guard 37%) is the alternative fourth purchase.
- **Victory in the Sheath:** Heiho's Decrease Damage Taken at 45% for the 2 rounds after each cast, one cast per 5-round cooldown, against every non-pierce hit of any stat type, with all three self buffs at 38% (1 from the capstone, 2 from Drawn Steel). Answering Cut (strikes 40 EP, buffs 36%) is the alternative fourth purchase, so Guard does not require the opener.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Tempo | Guard |
|---|---:|---|---|---:|---:|---:|---:|
| Heiho | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 38% (+3) |
| Heiho | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 39% (+4) | 45% (+10) |
| Iaido | 0 | Damage | enemy | 38 | 43 (+5) | 38 | 38 |
| Iaido | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 38% (+3) |
| Iaijutsu | 0 | Damage | enemy | 38 | 43 (+5) | 38 | 38 |
| Iaijutsu | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 38% (+3) |
| Iaijutsu | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 9, 4: 12
- Full-budget allocations: 12; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Cut of No Return: +5 Damage (0 + 2 + 3; on band)
  - Route Two Heavens as One: +5% Increase Damage Given (2 + 1 + 2; on band)
  - Route Victory in the Sheath: +10% Decrease Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 6 (DMG 2, DDT 1, IDG 3)
- Strongest full build by row-weighted total: Drawn Steel, Single Stroke, Second Sword, Two Heavens as One (raw +9, row-weighted 21)
- Lowest row-weighted node: Reading the Field (2)

Validator warnings:

- classification status: requires classification extension (director decision)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Drawn Steel, Single Stroke, Cut of No Return, Second Sword | +5 Damage, +3% IDG |
| 2 | Drawn Steel, Single Stroke, Cut of No Return, Reading the Field | +5 Damage, +2% IDG, +2% DDT |
| 3 | Drawn Steel, Single Stroke, Second Sword, Two Heavens as One | +2 Damage, +5% IDG, +2% DDT |
| 4 | Drawn Steel, Single Stroke, Second Sword, Reading the Field | +2 Damage, +3% IDG, +2% DDT |
| 5 | Drawn Steel, Single Stroke, Reading the Field, Unbroken Guard | +2 Damage, +2% IDG, +5% DDT |
| 6 | Drawn Steel, Single Stroke, Reading the Field, Answering Cut | +4 Damage, +2% IDG, +2% DDT |
| 7 | Drawn Steel, Second Sword, Two Heavens as One, Reading the Field | +5% IDG, +4% DDT |
| 8 | Drawn Steel, Second Sword, Reading the Field, Unbroken Guard | +3% IDG, +5% DDT |
| 9 | Drawn Steel, Second Sword, Reading the Field, Answering Cut | +2 Damage, +3% IDG, +2% DDT |
| 10 | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath | +3% IDG, +10% DDT |
| 11 | Drawn Steel, Reading the Field, Unbroken Guard, Answering Cut | +2 Damage, +2% IDG, +5% DDT |
| 12 | Reading the Field, Unbroken Guard, Victory in the Sheath, Answering Cut | +2 Damage, +1% IDG, +10% DDT |

## Design notes

- Node split: 2 Foundations, 4 Hidden Arts, 3 Advanced Arts. Drawn Steel (IDG +2%) forks into Single Stroke → Cut of No Return (Damage +2/+3) and Second Sword → Two Heavens as One (IDG +1%, then IDG +2% with DDT +2%). Reading the Field (DDT +2%) carries Unbroken Guard → Victory in the Sheath (DDT +3%, then DDT +5% with IDG +1%) and the leaf Answering Cut (Damage +2). Every Advanced Art is 3 BP deep; two cost 5 BP under the shared root or 6 BP across roots.
- Recalibration (RUL-2026-10-03-005): Reading the Field's +1 Damage is removed, so Damage is the default +5 route (Single Stroke +2, Cut of No Return +3; Iaido and Iaijutsu 38 → 43 EP). The tempo route moves from +6% to the +5% band by lowering Second Sword from +2% to +1% (Drawn Steel +2%, Second Sword +1%, Two Heavens as One +2%; three rows 35 → 40%), the lighter default the earlier draft named because the three rows compound. Victory in the Sheath's IDG secondary drops from +2% to +1% so it no longer exceeds Second Sword and Tempo keeps a clear amplification lead (IDG +5% against Guard's +3%). Guard stays the single-row +10% route (2/3/5; 35 → 45%). Maxima over every legal allocation: Damage +5, IDG +5%, DDT +10%.
- Interactions: every supported row is element-less. The Bukijutsu filter on Heiho's and Iaijutsu's IDG is not binding: it matches every element-less hit of any stat type (weapons, basic attacks, non-elemental jutsu) and excludes only elemental Nin/Gen/Tai hits; Iaido's IDG and Heiho's DDT list all four stat types and match every non-pierce hit. Each multiplies a matching hit by 1 + its percentage, in turn; the 15% Bukijutsu IDG passive is bloodline-sourced and applies last. Pierce is untouched.
- Delivery and uptime: Heiho (40 AP self cast, cooldown 5) is live 2 of every 5 rounds; Iaido and Iaijutsu are 60 AP, cooldown 7. Iaijutsu's IDG row is target SELF and lands on the caster at cast time whatever the circle or move row. No row acts in its cast round: Heiho plus Iaido (100 AP) are live the next two rounds, so an Iaijutsu strike in the first of them is multiplied by ×1.35 × 1.35 ≈ ×1.82 (×1.40 × 1.40 = ×1.96 on Tempo) and the round after all three are live (≈ ×2.46, ≈ ×2.74 on Tempo).
- Fourth purchases: Burst (01,02,03) adds Reading the Field (guard 37%) or Second Sword (buffs 38%); Tempo (01,04,05) adds Reading the Field (guard 39%) or Single Stroke (strikes 40 EP); Guard (06,07,08) adds Drawn Steel (buffs 38%) or Answering Cut (strikes 40 EP). 8 of 12 full builds are non-dominated (01,02,04,06 and 01,04,06,09 lose to Tempo with Single Stroke, 01,04,06,07 to Guard, 01,02,06,09 to Burst); every node appears in one. Row-weighted: Tempo with Single Stroke 21 (strongest), Tempo and Guard 19, Burst 18, opener-free Guard 17.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Musashi Ken' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Broad self amplification (user-owned): Two Heavens as One puts each IDG row at 40%. Heiho plus Iaido cast together are live the next two rounds (×1.96 against ×1.82 at base); Iaijutsu cast in the first makes three live the round after (≈ ×2.74 against ≈ ×2.46) on every non-pierce element-less hit. The +10% band on three adding rows was declined as too heavy.
- Iaijutsu delivery: the Damage row is INHERIT on an EMPTY_GROUND circle, friendly fire ENEMIES, so only enemies are hit; the IDG row is target SELF and lands on the caster at cast time (actions.ts 980-1004), not through the tiles, so it is neither positional nor shared with allies or enemies. Only the unsupported move row is positional (sorts last; enemy hazard) and no node touches it.
- Answering Cut twins Single Stroke's tag and flat (Damage +2 on both strikes): 01,04,06,09 and 01,06,07,09 give the same bonuses as 01,02,04,06 and 01,02,06,07. A DDT leaf in its place would breach +10% beside the guard route. Dropping it restores a universal Drawn Steel and a fixed Guard build (user option).
- Guard is one row at 40% uptime: Victory in the Sheath puts Heiho's DDT at 45% for the 2 rounds after each cast (cooldown 5) against every non-pierce hit. Other DDT sources apply in turn (×(1 − p/100) each, floored at 10% of the boosted hit); it runs against the bloodline's 5% IDT passive, which reaches every non-pierce hit except elemental Bukijutsu hits and no node changes.
- Burst is the lighter route by design: Damage is formula-calculated (sqrt stat scaling); the 15% passive and each IDG row live from an earlier round multiply the hit, so the tempo buffs scale the +5 EP too. Both strikes are 60 AP, cooldown 7, one hit per cast. Cut of No Return (+3 on two rows) stays single-tag so Burst does not borrow guard.
- Unsupported rows and modes: Iaijutsu's move receives nothing; the bloodline passives (15% Bukijutsu IDG, 5% IDT, sealprevent) are not jutsu rows. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin. No hidden, item-gated, mode-restricted, adverse or ally-hazard rows exist in this kit.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Musashi Ken-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

