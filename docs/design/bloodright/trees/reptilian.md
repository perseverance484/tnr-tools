# Reptilian — Cold Blood and Scale

**Bloodline:** Reptilian (BR-057, rank B, `z78aHAPRQfctiw7_qNXMx`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Reptilian classification / forked tree · **Classification:** Reptilian (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Increase Damage Given — two 35% rows that compound on a caster carrying both buffs (Reptile Chimera self, Cool-Blooded Empowerment circle) · secondary Decrease Damage Taken — Reptile Chimera hide (single row, +10% Fortress route) · tertiary Lifesteal — Cool-Blooded Empowerment circle (single row, +5% hard ceiling) with an Increase Damage Given rider.

Four supported rows sit on two 40 AP, cooldown-7 buffs, each live for the 2 rounds after its cast: Reptile Chimera (SELF) carries 35% Increase Damage Given and 35% Decrease Damage Taken; Cool-Blooded Empowerment (ALLY, radius-1 circle, caster included) carries 35% Increase Damage Given and 35% Lifesteal. Each tag has one route that maximizes it: Jaws of the Chimera takes both IDG rows to 42% (a caster carrying both buffs goes from ×1.82 to ×2.02); Basilisk Carapace takes the hide to 45% (hits ×0.65 → ×0.55); Feast of Scales takes the circle's Lifesteal to the 40% ceiling with a +2% IDG rider on both IDG rows. No row deals damage, so no node carries flat Damage. Potency reaches matching supported tags on all jutsu of the proposed Reptilian classification (RUL-2026-10-03-005). Summoning: Reptile Zoo (summon, injectjutsus, visual; PVP only) and its injected Reptile King are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Chimeric Blood | Foundation | How do I win the exchange: bite harder or harden the hide? |
| Blood of the Brood | Foundation | How do I keep the brood fed? |
| Jaws of the Chimera | Advanced Art | sustained self-amplification: both Increase Damage Given buffs stacked on the caster in one window (the circle row also lifts allies) |
| Basilisk Carapace | Advanced Art | fortress: the one hide row to +10% |
| Feast of Scales | Advanced Art | pack sustain offense: circle Lifesteal at the ceiling, with an IDG rider so recipients leech from larger hits |

**Director review recommended:** Roster questions: none. Tree-specific: Jaws of the Chimera's +7% Increase Damage Given (Draft 4: +5%) sits on two rows that compound on the caster (×1.82 → ×2.02 with both buffs, ×1.106), and one of them, Cool-Blooded Empowerment's circle, also lifts every same-village ally in radius 1 (×1.35 → ×1.42). The nearest precedent, Blood-Enchanted Eyes' Feast of the Fallen (+7% on two self rows), has no ally reach. Confirm +7% or return the route to +5%.

- Concern: Jaws of the Chimera rises from Draft 4's +5% to +7% Increase Damage Given, within the two-compounding-row convention (≤ +8%). Feast of the Fallen (35 → 42%) is only a partial precedent: both its rows are SELF and its +7% is a secondary on a Lifesteal route, whereas one Reptilian row is the Cool-Blooded Empowerment circle, so Jaws also gives allies in the circle 42%. The two rows compound only on the caster (×1.82 → ×2.02, +10.6%); allies get one row (×1.35 → ×1.42, +5.2%). Kept at +7% for director attention, not as a settled match.
- Concern: Basilisk Carapace takes one narrow row to the +10% Decrease Damage Taken ceiling with no secondary: Reptile Chimera's hide 35 → 45%, self only, live 2 of every 7 rounds. Arashima's Unbroken Horizon (Stormsinger's single hide row 35 → 45%) is the precedent, but it carries a +2% Lifesteal rider; this tree declines the rider so Lifesteal is raised by one route only. A lower value with a rider is the alternative if defensive capstones should read like the anchors.
- Concern: Feast of Scales' +2% IDG rider reaches both IDG rows, so Pack sustain carries +4% IDG with the forced Chimeric Blood: as much as Fortress with Apex Instinct, below Jaws' +7%. It is a small share of the amplification route's tag, as the old +2% DDT rider was of the Fortress's.
- Concern: Pack sustain is team-dependent: solo the circle reaches only the caster, so it is likely the weakest 1v1 route (not simulated).
- Concern: Chimeric Blood stays universal (all 8 legal builds), as in Draft 4.
- Concern: Row-weighted intensity: the strongest build (Jaws + Hardened Scales, row-weighted 19 on four rows; Draft 4's best was 18) is 4.75 per supported row, the highest per-row figure in the first-pass balance matrix. Four BP on four rows makes that largely structural; row weight is diagnostic only.
- Concern: The Reptilian classification extension and off-kit coverage remain director/engine decisions.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on four rows (Increase Damage Given on Reptile Chimera and Cool-Blooded Empowerment; Decrease Damage Taken on Reptile Chimera; Lifesteal on Cool-Blooded Empowerment), and each tag gets one route that maximizes it: sustained self-amplification (IDG), fortress (DDT), pack sustain (Lifesteal); a fourth Advanced Art would repeat one of them. Chimeric Blood is a universal node (in all 8 legal 4 BP builds) because Blood of the Brood's subtree is one 3-node chain. A 1 BP leaf under Blood of the Brood would need to beat Chimeric Blood (+2% IDG, +2% DDT) as Pack sustain's fourth: Lifesteal is already at the +5% ceiling, Decrease Damage Taken +3% twins Hardened Scales, and Increase Damage Given +3% lets 06, leaf, 01, 02 reach +7% IDG, the Jaws route without its capstone. A mirrored layout only moves the universal node to the other root.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Reptilian-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Chimeric Blood | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Cool-Blooded Empowerment, Reptile Chimera / 3 |
| 02 | Apex Instinct | Hidden Art | Chimeric Blood | +2% Increase Damage Given (self buff) | Cool-Blooded Empowerment, Reptile Chimera / 2 |
| 03 | Jaws of the Chimera | Advanced Art | Apex Instinct | +3% Increase Damage Given (self buff) | Cool-Blooded Empowerment, Reptile Chimera / 2 |
| 04 | Hardened Scales | Hidden Art | Chimeric Blood | +3% Decrease Damage Taken (self buff) | Reptile Chimera / 1 |
| 05 | Basilisk Carapace | Advanced Art | Hardened Scales | +5% Decrease Damage Taken (self buff) | Reptile Chimera / 1 |
| 06 | Blood of the Brood | Foundation | None | +1% Lifesteal (self buff) | Cool-Blooded Empowerment / 1 |
| 07 | Serpent's Thirst | Hidden Art | Blood of the Brood | +2% Lifesteal (self buff) | Cool-Blooded Empowerment / 1 |
| 08 | Feast of Scales | Advanced Art | Serpent's Thirst | +2% Lifesteal (self buff); +2% Increase Damage Given (self buff) | Cool-Blooded Empowerment, Reptile Chimera / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Chimeric Blood** — The blood remembers every beast it has been and lends their strength to its bearer. Reptile Chimera Increase Damage Given and Decrease Damage Taken 35 → 37%; Cool-Blooded Empowerment Increase Damage Given 35 → 37% (circle: same-village allies, caster); 2 rounds per 40 AP cast.
- **Apex Instinct** — Nothing in the swamp hunts the hunter. It learns to strike first. Both Increase Damage Given rows 37 → 39% with Chimeric Blood; element-less non-pierce hits, plus elemental hits of Ninjutsu (Chimera) or the caster's highest stat (Empowerment).
- **Jaws of the Chimera** — Three sets of jaws close at once, and nothing caught between them is let go. Amplification: both Increase Damage Given rows 35 → 42% on the full route (+7%); a caster carrying both buffs hits at ×1.42 × 1.42 ≈ ×2.02 (×1.82 unenhanced) for the 2 rounds after the 80% AP double cast; allies in the circle ×1.42.
- **Hardened Scales** — Each shed skin leaves the next one thicker. Reptile Chimera Decrease Damage Taken only, 37 → 40% with Chimeric Blood; every stat-typed non-pierce hit; 2 rounds per cast.
- **Basilisk Carapace** — Blades skate off the carapace and find nothing beneath worth cutting. Fortress: Reptile Chimera Decrease Damage Taken 35 → 45% on the full route (+10%), so hits in its 2-round window land at ×0.55 instead of ×0.65. Pierce bypasses it.
- **Blood of the Brood** — The brood shares one cold blood, and what one drinks warms them all. Cool-Blooded Empowerment Lifesteal 35 → 36% for same-village allies in the radius-1 circle (caster included); 2 rounds; 60% leech budget.
- **Serpent's Thirst** — A serpent does not stop at the first mouthful. Same Lifesteal row 36 → 38% with Blood of the Brood; includes pierce hits the recipient lands; needs both combatants alive.
- **Feast of Scales** — The brood feeds together, and every mouthful sharpens the next bite. Pack sustain: Cool-Blooded Empowerment Lifesteal 35 → 40% on the full route (+5%, the hard ceiling); both Increase Damage Given rows +2% (37%, or 39% with Chimeric Blood), the circle row and Reptile Chimera's self row alike, so recipients leech from larger hits.

## Complete four-purchase examples

| Build | Purchases | IDG | DDT | LS |
|---|---|---:|---:|---:|
| Jaws of the Chimera (Predation) | Chimeric Blood, Apex Instinct, Jaws of the Chimera, Hardened Scales | +7% | +5% | — |
| Basilisk Carapace (Fortress) | Chimeric Blood, Apex Instinct, Hardened Scales, Basilisk Carapace | +4% | +10% | — |
| Feast of Scales (Pack sustain) | Chimeric Blood, Blood of the Brood, Serpent's Thirst, Feast of Scales | +4% | +2% | +5% |

Abbreviations: IDG = Increase Damage Given · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Jaws of the Chimera:** Sustained self-amplification with a hide: both Increase Damage Given rows reach 42% (+7%), so the double cast puts ×1.42 × 1.42 ≈ ×2.02 on the caster for two rounds and ×1.42 on allies in the circle; Hardened Scales, the strongest fourth, makes the same Chimera window a 40% hide. Blood of the Brood is the alternative fourth (circle Lifesteal 36%).
- **Basilisk Carapace:** Survival: Reptile Chimera's Decrease Damage Taken, the kit's one hide row, reaches 45% (+10%) for its 2-round window every 7 rounds; Apex Instinct, the strongest fourth, keeps a bite with both Increase Damage Given rows at 39%. Blood of the Brood is the alternative fourth (circle Lifesteal 36%, IDG 37%).
- **Feast of Scales:** Team sustain: Cool-Blooded Empowerment's Lifesteal reaches 40% (+5%, the hard ceiling) for every same-village ally in the circle, and both Increase Damage Given rows reach 39% with the forced Chimeric Blood, so each recipient leeches 40% of a larger hit; a caster in the circle adds the 10% Ninjutsu Lifesteal passive (50% of the 60% leech budget). Chimeric Blood is the only legal fourth (hide 37%).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Predation | Fortress | Pack sustain |
|---|---:|---|---|---:|---:|---:|---:|
| Summoning: Reptile Zoo | 0 | summon (unsupported) | self | 60% | 60% | 60% | 60% |
| Summoning: Reptile Zoo | 1 | injectjutsus (unsupported) | self | 100 | 100 | 100 | 100 |
| Summoning: Reptile Zoo | 2 | visual (unsupported) **adverse** | self | 1 | 1 | 1 | 1 |
| Cool-Blooded Empowerment | 0 | Increase Damage Given | ally | 35% | 42% (+7) | 39% (+4) | 39% (+4) |
| Cool-Blooded Empowerment | 1 | Lifesteal | ally | 35% | 35% | 35% | 40% (+5) |
| Cool-Blooded Empowerment | 2 | visual (unsupported) **adverse** | ally | 1 | 1 | 1 | 1 |
| Reptile Chimera | 0 | Increase Damage Given | self | 35% | 42% (+7) | 39% (+4) | 39% (+4) |
| Reptile Chimera | 1 | Decrease Damage Taken | self | 35% | 40% (+5) | 45% (+10) | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +7% Increase Damage Given, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Jaws of the Chimera: +7% Increase Damage Given (2 + 2 + 3; off band)
  - Route Basilisk Carapace: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Feast of Scales: +5% Lifesteal (1 + 2 + 2; on band)
- Supported rows in kit: 4 (DDT 1, IDG 2, LS 1)
- Strongest full build by row-weighted total: Chimeric Blood, Apex Instinct, Jaws of the Chimera, Hardened Scales (raw +12, row-weighted 19)
- Lowest row-weighted node: Blood of the Brood (1)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Chimeric Blood) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Jaws of the Chimera | +7% IDG, +2% DDT | Hardened Scales *(highest diagnostic)* | +7% IDG, +5% DDT | 19 |
| Jaws of the Chimera | +7% IDG, +2% DDT | Blood of the Brood | +7% IDG, +2% DDT, +1% LS | 17 |
| Basilisk Carapace | +2% IDG, +10% DDT | Apex Instinct *(highest diagnostic)* | +4% IDG, +10% DDT | 18 |
| Basilisk Carapace | +2% IDG, +10% DDT | Blood of the Brood | +2% IDG, +10% DDT, +1% LS | 15 |
| Feast of Scales | +2% IDG, +5% LS | Chimeric Blood *(highest diagnostic)* | +4% IDG, +2% DDT, +5% LS | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Chimeric Blood, Apex Instinct, Jaws of the Chimera, Hardened Scales | +7% IDG, +5% DDT |
| 2 | Chimeric Blood, Apex Instinct, Jaws of the Chimera, Blood of the Brood | +7% IDG, +2% DDT, +1% LS |
| 3 | Chimeric Blood, Apex Instinct, Hardened Scales, Basilisk Carapace | +4% IDG, +10% DDT |
| 4 | Chimeric Blood, Apex Instinct, Hardened Scales, Blood of the Brood | +4% IDG, +5% DDT, +1% LS |
| 5 | Chimeric Blood, Apex Instinct, Blood of the Brood, Serpent's Thirst | +4% IDG, +2% DDT, +3% LS |
| 6 | Chimeric Blood, Hardened Scales, Basilisk Carapace, Blood of the Brood | +2% IDG, +10% DDT, +1% LS |
| 7 | Chimeric Blood, Hardened Scales, Blood of the Brood, Serpent's Thirst | +2% IDG, +5% DDT, +3% LS |
| 8 | Chimeric Blood, Blood of the Brood, Serpent's Thirst, Feast of Scales | +4% IDG, +2% DDT, +5% LS |

## Design notes

- Layout: Chimeric Blood (+2% IDG, +2% DDT; both Reptile Chimera rows plus the circle's IDG row) forks into Apex Instinct → Jaws of the Chimera (IDG 2/2/3 = +7%) and Hardened Scales → Basilisk Carapace (DDT 2/3/5 = +10%). Blood of the Brood runs one chain, Serpent's Thirst → Feast of Scales (Lifesteal 1/2/2 = +5%, plus +2% IDG on the capstone). Every Advanced Art is 3 BP deep; any two cost 5 or 6 BP.
- Changes from Draft 4: Lifesteal no longer rides on Jaws of the Chimera or Basilisk Carapace (it was a +2% rider on all three capstones), so Pack sustain is the one route that raises it. Jaws becomes a pure IDG capstone and Apex Instinct a real commitment (+1% → +2%, Jaws +2% → +3%; route +5% → +7%). Feast of Scales trades its +2% DDT rider for +2% IDG. The modifier reaches every IDG row, so it lifts both the circle row and Reptile Chimera's self row (Pack sustain +4% IDG with Chimeric Blood); it stays because larger hits mean more leech, the Lifesteal-plus-IDG pairing of the director-approved Feast of the Fallen and The Storm's Due. Basilisk Carapace keeps +5% DDT: one self row, live 2 of 7 rounds, reaches the +10% single-row ceiling, as Stormsinger's hide does under Arashima's Unbroken Horizon (which adds a +2% Lifesteal rider this tree declines). Maxima over every legal allocation: IDG +7%, DDT +10%, Lifesteal +5%.
- Impact: both IDG rows are jutsu-sourced, element-less and multiply in sequence (§3b), so the double cast (80% AP) gives ×1.42 × 1.42 ≈ ×2.02 on the full route against ×1.82 unenhanced (+10.6%), each buff alone ×1.42 against ×1.35 (+5.2%). Feast of the Fallen's 35 → 42% on two self IDG rows is the nearest director precedent; it has no ally reach, while Jaws also lifts allies in the circle. The Fortress cuts hits in its window from ×0.65 to ×0.55 (−15.4%). Pack sustain: 40% Lifesteal on 39% IDG hits gives a recipient 0.40 × 1.39 ≈ 0.56 HP per point of unbuffed damage against 0.35 × 1.35 ≈ 0.47. The Ninjutsu IDG passive multiplies last; the 10% Genjutsu Increase Damage Taken passive is blunted only inside the Chimera window.
- Fourth purchases: Jaws (01,02,03) adds Hardened Scales (hide 40%, strongest) or Blood of the Brood (Lifesteal 36%); Fortress (01,04,05) adds Apex Instinct (IDG 39%, strongest) or Blood of the Brood; Pack sustain (06,07,08) only Chimeric Blood. No fourth adds the route's own primary tag: the sibling Hidden Arts carry different tags and Blood of the Brood carries no IDG or DDT.
- Delivery: both carriers cost 40 AP with cooldown 7; at most 2 of 7 rounds carry each buff, and neither acts in its cast round. Reptile Chimera is SELF. Cool-Blooded Empowerment is ALLY, AOE_CIRCLE_SPAWN: the clicked tile must hold a living same-side user (the caster's own tile qualifies: util.ts 2750–2752) and its rows apply once at cast to every same-village user within radius 1 (actions.ts 1239–1240; friendlyFire FRIENDLY). Not a ground effect.

## Risks and unproven interactions

- Classification (director decision): no row carries a non-None element, so no existing element identifies this kit. The proposal needs a classification extension: a new jutsu classification (placeholder 'Reptilian') assigned to jutsu records. It is not a bloodline-id selector; which jutsu carry it is a director/engine decision, and targeting None would reach every non-elemental row in the game. All three kit jutsu qualify only through that authored classification (ENGINE_GAP_REGISTER G1). Off-kit coverage is unverified.
- IDG stacking: the caster is a legal ALLY target, so Reptile Chimera and Cool-Blooded Empowerment can both sit on the caster; same-tag effects from different jutsu each apply as their own multiplier (§3b; process.ts 1692–1825), giving ×2.02 on the Jaws route before the Ninjutsu passive. The window costs 80% AP in the cast round, which itself gets no bonus. Combined final damage was not simulated.
- Lifesteal budget: lifesteal and vamp share one 60%-of-damage leech budget per hit. Pack sustain reaches 40%; a caster inside the circle adds the 10% Ninjutsu passive (50%), so vamp or lifesteal from the main tree or items fills the last 10 points. The recipient heals from their own hits (pierce included); both combatants must be alive; healprevent on the recipient blocks it.
- Highest resolution: Cool-Blooded Empowerment's rows carry statTypes [Highest], resolved from the caster's highestOffence (G16), so on an ally the ratio tests the caster's highest stat. Element-less rows still match every element-less hit of any stat type and exclude only elemental hits of another stat (§3, §4b).
- Team dependence: the circle reaches same-village users only (getTargetUser compares villageId); in a 1v1 it reaches only the caster, so Pack sustain is likely the weakest solo route and gains most in team fights. Jaws, and Feast's rider, also lift allies' Empowerment IDG.
- Summoning: Reptile Zoo (PVP only) and its injected Reptile King (SPECIAL, empty bloodlineId, summon row only) have no supported rows; no node changes them. The unsupported visual rows (adverse) are untouched. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. Uptime against real opponents was not simulated.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Reptilian-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

