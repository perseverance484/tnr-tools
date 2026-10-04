# Musashi Ken — The Drawn Blade

**Bloodline:** Musashi Ken (BR-047, rank D, `EZRt16BYzQRMiGSf_P7is`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Musashi Ken classification / forked tree · **Classification:** Musashi Ken (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Bukijutsu tempo — Increase Damage Given (Heiho, Iaido, Iaijutsu; three self rows that compound) · secondary The draw — Damage on Iaido and Iaijutsu (two 38 EP Light-tier strikes) · tertiary Guard — Decrease Damage Taken (Heiho; one row).

Six supported rows on three casts. Every jutsu carries a 35% self Increase Damage Given row for 2 rounds; each lands on the caster at cast time, acts only in the two rounds after, and compounds with the others on every element-less hit, so self amplification is the kit's highest-leverage lever and the Tempo route's job. The two 38 EP Bukijutsu / Speed, Strength strikes (Iaido single target, Iaijutsu ground circle; 60 AP, cooldown 7) are the only Damage rows and sit in the Light tier, so the steady edge stops at the batch's +2 flat-Damage limit (38 → 40, Light → Normal) and the Normal-tier step comes from the capstone. Heiho's single 35% Decrease Damage Taken row is the only defensive lever; it carries the Fortress chain and the steady edge's small guard rider. Iaijutsu's move row is unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Drawn Steel | Foundation | How do I win with the drawn blade: make the draw itself land harder, or keep a chain of buffs multiplying every cut? |
| Reading the Field | Foundation | How do I hold Heiho's guard? |
| Cut of No Return | Advanced Art | steady edge: a +1 commit, then +1 raw Damage on both draws (38 → 40, Light → Normal), every cast, no setup window, with a small guard rider |
| Two Heavens as One | Advanced Art | sustained amplification: three compounding self buffs |
| Victory in the Sheath | Advanced Art | fortress: Heiho's guard |

**Director review recommended:** Roster questions: DQ-D (Single Stroke +1 Damage, the commit of a 1/1 steady-edge route, 38 → 39 → 40: an Increase Damage Given setup there twins Second Sword and lifts Tempo's Single Stroke fourth to +6% on three compounding rows, and a Decrease Damage Taken one sets up no strike); DQ-H (9 → 8 nodes: the pre-batch Answering Cut leaf is removed and Drawn Steel is universal, see narrow_kit_exception).

- Concern: The steady edge trails Tempo on sustained throughput at the +2 flat-Damage limit (rough model: 0.7–1.4% behind Tempo with Single Stroke, within 1% of Tempo with Reading the Field at equal 37% guard), and the limit leaves no Damage lever to close the gap. Its case is the draw at 40 EP on every cast with at most one buff live, plus Cut of No Return's +2% guard.
- Concern: Single Stroke keeps +1 flat Damage on a Hidden Art (38 → 39, still Light) because no percentage setup works there: Increase Damage Given twins Second Sword and lifts Tempo's fourth to +6% on three compounding rows; Decrease Damage Taken sets up no strike.
- Concern: Cut of No Return's +2% Decrease Damage Taken rider departs from the anchors' offensive burst riders (Arashima +3% Increase Damage Given, Shakunetsu Sakura +3% Increase Damage Taken): the kit's only offensive percentage tag is Tempo's, so an offensive rider would make the steady edge a near-copy of Tempo.
- Concern: Drawn Steel is universal (acknowledged in the narrow-kit exception); the Fortress build is fixed (01, 06, 07, 08) and is pure guard.
- Concern: The 'Musashi Ken' classification extension and off-kit coverage remain director/engine decisions; an off-kit Damage row given the classification would also take +2 (a 50 EP row would read 52), unverified.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on six rows (Increase Damage Given ×3, Damage ×2, Decrease Damage Taken ×1); a fourth Advanced Art would twin a capstone on the same rows or push the single Decrease Damage Taken row past +10%. Reading the Field therefore runs one guard chain and Drawn Steel is universal: it is in every legal 4-BP build, so the Fortress build is fixed and every build carries +2% Increase Damage Given. Every leaf that could avoid this is filler or illegal: a Damage leaf would be kept only so Drawn Steel is not universal (the pre-batch Answering Cut, removed as filler under R4), an Increase Damage Given leaf only re-sells Drawn Steel as Fortress's fourth, and a Decrease Damage Taken leaf lifts the guard chain past +10%.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Musashi Ken-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Drawn Steel | Foundation | None | +2% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 02 | Single Stroke | Hidden Art | Drawn Steel | +1 Damage (damage) | Iaido, Iaijutsu / 2 |
| 03 | Cut of No Return | Advanced Art | Single Stroke | +1 Damage (damage); +2% Decrease Damage Taken (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 04 | Second Sword | Hidden Art | Drawn Steel | +1% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 05 | Two Heavens as One | Advanced Art | Second Sword | +2% Increase Damage Given (self buff) | Heiho, Iaido, Iaijutsu / 3 |
| 06 | Reading the Field | Foundation | None | +2% Decrease Damage Taken (self buff) | Heiho / 1 |
| 07 | Unbroken Guard | Hidden Art | Reading the Field | +3% Decrease Damage Taken (self buff) | Heiho / 1 |
| 08 | Victory in the Sheath | Advanced Art | Unbroken Guard | +5% Decrease Damage Taken (self buff) | Heiho / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Drawn Steel** — Steel leaves the sheath and the whole battle narrows to the length of one blade. All three self buffs 35 → 37% for 2 rounds: Heiho and Iaijutsu (Bukijutsu-filtered, element-less), Iaido (all four stat types). 3 rows.
- **Single Stroke** — One stroke, begun and finished before the eye can follow it. Commitment: Iaido and Iaijutsu Damage 38 → 39 EP, still Light tier; the Normal-tier step belongs to Cut of No Return. 2 rows.
- **Cut of No Return** — The blade does not return to the sheath until the matter is settled. Steady edge: Iaido and Iaijutsu 38 → 40 EP on the full route (Light → Normal), landing on the strike's own cast, which no buff does. Rider: Heiho's guard 35 → 37% (39% with Reading the Field). 3 rows.
- **Second Sword** — The off hand was never idle; a second edge waits where the first was parried. All three self buffs 37 → 38% with Drawn Steel; each lands on the caster at cast time and is live the 2 rounds after. 3 rows.
- **Two Heavens as One** — Sword and strategy, long blade and short, drawn as a single will. Sustained amplification: all three self buffs 35 → 40% on the full route, compounding to ×1.96 with two live and ≈ ×2.74 with three. 3 rows.
- **Reading the Field** — Before the first cut, the strategist has already chosen the ground. Heiho Decrease Damage Taken 35 → 37% (all four stat types, 2 rounds, cooldown 5). 1 row.
- **Unbroken Guard** — A guard that does not break is a battle that is not lost. Heiho Decrease Damage Taken 37 → 40% with Reading the Field; one row against every non-pierce hit, 2 rounds per 40 AP cast.
- **Victory in the Sheath** — The master wins with the sword still sheathed; the draw is only a courtesy. Fortress: Heiho Decrease Damage Taken 35 → 45% on the full route, so a non-pierce hit lands at ×0.55 instead of ×0.65 for the 2 rounds after each cast. 1 row.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDT |
|---|---|---:|---:|---:|
| Cut of No Return (Steady edge) | Drawn Steel, Single Stroke, Cut of No Return, Second Sword | +2 | +3% | +2% |
| Two Heavens as One (Tempo) | Drawn Steel, Second Sword, Two Heavens as One, Reading the Field | — | +5% | +2% |
| Victory in the Sheath (Fortress) | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath | — | +2% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Cut of No Return:** Iaido and Iaijutsu 38 → 40 EP (Light → Normal) on each strike's own cast with no setup round, all three self buffs at 38% (Drawn Steel +2%, Second Sword +1%) multiplying any strike that follows an earlier cast, and Heiho's guard at 37% from Cut of No Return's rider. Second Sword is the offensive fourth purchase; Reading the Field (buffs 37%, guard 39%) is the guarded alternative.
- **Two Heavens as One:** All three self buffs 35 → 40%. Heiho and Iaido cast together (100 AP) multiply every element-less hit next round by ×1.40 × 1.40 = ×1.96 (×1.82 at base); with Iaijutsu cast in that round all three are live the round after, ≈ ×2.74 (≈ ×2.46). Reading the Field (guard 37%) is the safer fourth purchase; Single Stroke (strikes 39 EP, still Light) is the offensive one.
- **Victory in the Sheath:** Heiho's Decrease Damage Taken at 45% (×0.55 of each non-pierce hit, against ×0.65 at base) for the 2 rounds after each cast (cooldown 5), with all three self buffs at 37% from Drawn Steel, the only legal fourth purchase.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Steady edge | Tempo | Fortress |
|---|---:|---|---|---:|---:|---:|---:|
| Heiho | 0 | Increase Damage Given | self | 35% | 38% (+3) | 40% (+5) | 37% (+2) |
| Heiho | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) |
| Iaido | 0 | Damage | enemy | 38 | 40 (+2) | 38 | 38 |
| Iaido | 1 | Increase Damage Given | self | 35% | 38% (+3) | 40% (+5) | 37% (+2) |
| Iaijutsu | 0 | Damage | enemy | 38 | 40 (+2) | 38 | 38 |
| Iaijutsu | 1 | Increase Damage Given | self | 35% | 38% (+3) | 40% (+5) | 37% (+2) |
| Iaijutsu | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Cut of No Return: +2 Damage (0 + 1 + 1; off band)
  - Route Two Heavens as One: +5% Increase Damage Given (2 + 1 + 2; on band)
  - Route Victory in the Sheath: +10% Decrease Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 6 (DMG 2, DDT 1, IDG 3)
- Strongest full build by row-weighted total: Drawn Steel, Second Sword, Two Heavens as One, Reading the Field (raw +7, row-weighted 17)
- Lowest row-weighted node: Single Stroke (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Drawn Steel) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +1 Damage | +2 Damage |
|---|---:|---|---|---|
| Iaido | 0 | 38 (Light) | 39 (Light) | 40 (Normal) ↑ |
| Iaijutsu | 0 | 38 (Light) | 39 (Light) | 40 (Normal) ↑ |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Cut of No Return | +2 Damage, +2% IDG, +2% DDT | Second Sword *(highest diagnostic)* | +2 Damage, +3% IDG, +2% DDT | 15 |
| Cut of No Return | +2 Damage, +2% IDG, +2% DDT | Reading the Field | +2 Damage, +2% IDG, +4% DDT | 14 |
| Two Heavens as One | +5% IDG | Single Stroke | +1 Damage, +5% IDG | 17 |
| Two Heavens as One | +5% IDG | Reading the Field *(highest diagnostic)* | +5% IDG, +2% DDT | 17 |
| Victory in the Sheath | +10% DDT | Drawn Steel *(highest diagnostic)* | +2% IDG, +10% DDT | 16 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Drawn Steel, Single Stroke, Cut of No Return, Second Sword | +2 Damage, +3% IDG, +2% DDT |
| 2 | Drawn Steel, Single Stroke, Cut of No Return, Reading the Field | +2 Damage, +2% IDG, +4% DDT |
| 3 | Drawn Steel, Single Stroke, Second Sword, Two Heavens as One | +1 Damage, +5% IDG |
| 4 | Drawn Steel, Single Stroke, Second Sword, Reading the Field | +1 Damage, +3% IDG, +2% DDT |
| 5 | Drawn Steel, Single Stroke, Reading the Field, Unbroken Guard | +1 Damage, +2% IDG, +5% DDT |
| 6 | Drawn Steel, Second Sword, Two Heavens as One, Reading the Field | +5% IDG, +2% DDT |
| 7 | Drawn Steel, Second Sword, Reading the Field, Unbroken Guard | +3% IDG, +5% DDT |
| 8 | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath | +2% IDG, +10% DDT |

## Design notes

- Node split: 2 Foundations, 3 Hidden Arts, 3 Advanced Arts. Drawn Steel (+2% IDG) forks into Single Stroke → Cut of No Return (+1 Damage, then +1 Damage with +2% DDT) and Second Sword → Two Heavens as One (+1%, then +2% IDG). Reading the Field (+2% DDT) carries Unbroken Guard → Victory in the Sheath (+3%, then +5% DDT). Any two Advanced Arts cost 5 BP under Drawn Steel or 6 BP across roots. Maxima over every legal allocation: Damage +2 (38 → 40), Increase Damage Given +5%, Decrease Damage Taken +10%. Tempo's +5% on three compounding rows is ×1.115 over the unmodified kit with all three live, the tree's top offensive package, under Blood-Enchanted Eyes' ×1.234. Second Sword's +1% step is kept: three compounding rows cap the route at +5%, which leaves no room for a larger setup, and the capstone's +2% still exceeds it.
- Roster pass: the Damage route goes from +4 (Single Stroke +1, Cut of No Return +3; 38 → 42) to +2 (+1, then +1; 38 → 40). +4 was the largest non-protected flat-Damage gain in the roster (×1.105 per strike, 2 EP past the Normal line); the batch caps flat Damage at +2 over every legal allocation, since potency reaches every Musashi Ken-classified jutsu. With no percentage setup the route is a steady edge, not burst. Single Stroke keeps a +1 commit (39, still Light) because no percentage setup works there: Increase Damage Given twins Second Sword under the same Foundation and lifts Tempo's Single Stroke fourth to +6% on three compounding rows; a Decrease Damage Taken setup feeds no strike and only re-sells Reading the Field as Tempo's guarded fourth. The Light → Normal step is the capstone's.
- Guard rider (Edge below means the steady-edge route, Cut of No Return): at +2 EP, Edge with Second Sword (40 EP, buffs 38%) would trail Tempo with Single Stroke (39 EP, 40%) on almost every hit: Tempo's ×1.029 with two buffs live beats Edge's ×1.026 on two strikes, and only a draw with at most one buff live favours Edge. Cut of No Return therefore adds +2% Decrease Damage Taken on Heiho rather than more EP: the draw is made from guard and the blade stays up until the matter is settled. An Increase Damage Given rider was rejected because Edge with Second Sword (40 EP, 39%) would then be Tempo with Single Stroke (39 EP, 40%) with one point moved. With the rider, Edge with Second Sword and Tempo with Reading the Field hold the same 37% guard and trade +2 EP on two strikes against +2% on three buffs.
- First-pass riders stay removed: Two Heavens as One's +2% Decrease Damage Taken gave Tempo guard with no reason in its identity (Tempo already leads on throughput), and Victory in the Sheath's +1% Increase Damage Given was filler that only matched printed totals. Tempo is pure amplification and Fortress pure guard (buffs 37% from the mandatory Drawn Steel); the kit has no sustain or second defensive tag to give Fortress an identity-compatible secondary, so its one row carries the 2/3/5 chain alone.
- Fourth purchases: Edge (01,02,03) adds Second Sword (40 EP, buffs 38%, guard 37%) or Reading the Field (40 EP, buffs 37%, guard 39%); Tempo (01,04,05) adds Single Stroke (39 EP, buffs 40%) or Reading the Field (38 EP, buffs 40%, guard 37%); Fortress (06,07,08) adds only Drawn Steel (buffs 37%, guard 45%). Tempo's Single Stroke takes 1 of Edge's 2 EP but not the Normal-tier step; Edge's Second Sword takes 1 of Tempo's 5%.
- Interactions: every supported row is element-less. The Bukijutsu filter on Heiho's and Iaijutsu's IDG is not binding: it matches every element-less hit of any stat type (weapons, basic attacks, non-elemental jutsu) and excludes only elemental Nin/Gen/Tai hits; Iaido's IDG and Heiho's DDT list all four stat types and match every non-pierce hit. Live IDG rows multiply a hit one after another (×1.40 × 1.40 = ×1.96), DDT applies as ×(1 − p/100), and the 15% Bukijutsu IDG passive applies last. Formula Damage is linear in EP.
- Delivery: Heiho (40 AP self cast, cooldown 5) is live 2 of every 5 rounds; Iaido and Iaijutsu are 60 AP, cooldown 7. No buff acts in its cast round, so Tempo pays off only in later rounds, while the steady edge's flat Damage lands on the strike itself, including an opening or finishing draw with nothing live.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Musashi Ken' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. All three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Edge and Tempo trade throughput, marginal to marginal. Edge with Second Sword (40 EP, buffs 38%, guard 37%) against Tempo with Single Stroke (39 EP, 40%, guard 35%): Tempo gains ×1.40/1.38 per live buff (×1.029 with two live, ×1.044 with three) on every element-less hit; Edge gains ×1.026 (40/39) on its two cooldown-7 strikes, on their own cast with nothing live, and takes ×0.63 against ×0.65 while Heiho is live. Against Tempo with Reading the Field (38 EP, guard 37%) Edge's strikes gain ×1.053 at equal guard. A rough rotation model (indicative only: 100 AP per round, element-less filler, buffs live the 2 rounds after each cast, strikes carrying 18–41% of damage) puts Edge with Second Sword at ×1.038–1.049 over a no-tree build, Tempo with Single Stroke at ×1.052–1.056 and Tempo with Reading the Field at ×1.045–1.047: Edge trails the all-offence Tempo by 0.7–1.4% and is within 1% either way of the equal-guard Tempo. Not simulated in the engine.
- Iaijutsu delivery: the Damage row is INHERIT on an EMPTY_GROUND circle with friendly fire ENEMIES, so only enemies are hit; its IDG row is target SELF and lands on the caster at cast time (actions.ts 980-1004), not through the tiles. Only the unsupported move row is positional (enemy hazard), and no node touches it.
- Guard is one row at 40% uptime: Victory in the Sheath puts Heiho's DDT at 45% (×0.55 against ×0.65 at base) for the 2 rounds after each cast against every non-pierce hit; it runs against the bloodline's 5% Increase Damage Taken passive, which no node changes. Fortress gives up about 3% throughput to Tempo with Reading the Field (buffs 37% against 40%) for ×0.55 against ×0.63 while Heiho is live; Edge with Reading the Field sits between them (guard 39%, ×0.61).
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

