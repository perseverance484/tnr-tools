# Taiyo Kami — Covenant of the Sun

**Bloodline:** Taiyo Kami (BR-075, rank A, `6C2t3jK35hvPoVocLiHEl`) · **Revision:** approved reference (handoff v4 values) regenerated under RUL-2026-10-03-005 · **Classification:** Scorch (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Review status:** Approved worked reference; protected from the 2026-10-04 batch (values unchanged)

**Director review recommended:** Incandescent Nova 50 → 55 under the Burst route is flagged under BALANCE_REVIEW_METHOD.md; not retuned.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Scorch jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Dawnheart | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Celestial Ignition, Stellar Inferno / 3 |
| 02 | Crown of Cinders | Hidden Art | Dawnheart | +2 Damage (damage) | Incandescent Nova, Solar Reverb, Stellar Inferno / 3 |
| 03 | Solar Cataclysm | Advanced Art | Crown of Cinders | +3 Damage (damage) | Incandescent Nova, Solar Reverb, Stellar Inferno / 3 |
| 04 | Emberwake | Hidden Art | Dawnheart | +3% Afterburn (enemy debuff) | Solar Reverb / 1 |
| 05 | Eternal Noon | Advanced Art | Emberwake | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Celestial Ignition, Solar Reverb, Stellar Inferno / 4 |
| 06 | Sunward Oath | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Celestial Ignition, Radiant Embers / 2 |
| 07 | Golden Mantle | Hidden Art | Sunward Oath | +3% Decrease Damage Taken (self buff) | Celestial Ignition / 1 |
| 08 | Sovereign Sun | Advanced Art | Golden Mantle | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Celestial Ignition / 3 |
| 09 | Ashen Verdict | Hidden Art | Sunward Oath | +3% Decrease Damage Given (enemy debuff) | Radiant Embers / 1 |
| 10 | Dying Light | Advanced Art | Ashen Verdict | +5% Decrease Damage Given (enemy debuff); +5% Increase Damage Taken (enemy debuff) | Radiant Embers, Stellar Inferno / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.


## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|---:|
| Solar Cataclysm (Burst) | Dawnheart, Crown of Cinders, Solar Cataclysm, Sunward Oath | +5 | +2% | +2% | +2% | +2% | — |
| Eternal Noon (Burn pressure) | Dawnheart, Emberwake, Eternal Noon, Sunward Oath | — | +5% | +2% | +5% | +2% | +10% |
| Sovereign Sun (Fortified offense) | Dawnheart, Sunward Oath, Golden Mantle, Sovereign Sun | — | +5% | +2% | +2% | +10% | — |
| Dying Light (Suppression) | Sunward Oath, Golden Mantle, Ashen Verdict, Dying Light | — | — | +10% | +5% | +5% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.


## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortified offense | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Solar Reverb | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Solar Reverb | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Incandescent Nova | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Incandescent Nova | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Celestial Ignition | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 35% |
| Celestial Ignition | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 35% |
| Celestial Ignition | 2 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 40% (+5) |
| Radiant Embers | 0 | Decrease Damage Given | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 45% (+10) |
| Radiant Embers | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Stellar Inferno | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Stellar Inferno | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 40% (+5) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +7% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Solar Cataclysm: +5 Damage (0 + 2 + 3; on band)
  - Route Eternal Noon: +10% Afterburn (0 + 3 + 7; on band)
  - Route Sovereign Sun: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Dying Light: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 9 (AB 1, DMG 3, DDG 1, DDT 1, IDG 2, IDT 1)
- Strongest full build by row-weighted total: Dawnheart, Crown of Cinders, Emberwake, Eternal Noon (raw +22, row-weighted 31)
- Lowest row-weighted node: Emberwake (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Incandescent Nova 50 -> 52, Incandescent Nova 50 -> 55
- ally-hazard area rows amplified (friendly fire none/ALL): Solar Reverb#0, Stellar Inferno#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage | +5 Damage |
|---|---:|---|---|---|
| Solar Reverb | 0 | 40 (Normal) | 42 (Normal) | 45 (High) ↑ |
| Incandescent Nova | 0 | 50 (Nuke) | **52 (above Nuke)** | **55 (above Nuke)** |
| Stellar Inferno | 0 | 40 (Normal) | 42 (Normal) | 45 (High) ↑ |

Above-Nuke rationale: Approved worked reference (handoff v4; protected from the 2026-10-04 batch): the Burst route's +5 Damage lifts Incandescent Nova 50 → 55 (52 with Crown of Cinders alone), past the 50 Nuke tier. Not retuned here; flagged for director review under BALANCE_REVIEW_METHOD.md.

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Solar Cataclysm | +5 Damage, +2% IDG, +2% IDT | Emberwake | +5 Damage, +2% IDG, +2% IDT, +3% AB | 24 |
| Solar Cataclysm | +5 Damage, +2% IDG, +2% IDT | Sunward Oath *(highest diagnostic)* | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT | 25 |
| Eternal Noon | +5% IDG, +5% IDT, +10% AB | Crown of Cinders *(highest diagnostic)* | +2 Damage, +5% IDG, +5% IDT, +10% AB | 31 |
| Eternal Noon | +5% IDG, +5% IDT, +10% AB | Sunward Oath | +5% IDG, +2% DDG, +5% IDT, +2% DDT, +10% AB | 29 |
| Sovereign Sun | +3% IDG, +2% DDG, +10% DDT | Dawnheart *(highest diagnostic)* | +5% IDG, +2% DDG, +2% IDT, +10% DDT | 24 |
| Sovereign Sun | +3% IDG, +2% DDG, +10% DDT | Ashen Verdict | +3% IDG, +5% DDG, +10% DDT | 21 |
| Dying Light | +10% DDG, +5% IDT, +2% DDT | Dawnheart *(highest diagnostic)* | +2% IDG, +10% DDG, +7% IDT, +2% DDT | 23 |
| Dying Light | +10% DDG, +5% IDT, +2% DDT | Golden Mantle | +10% DDG, +5% IDT, +5% DDT | 20 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Dawnheart, Crown of Cinders, Solar Cataclysm, Emberwake | +5 Damage, +2% IDG, +2% IDT, +3% AB |
| 2 | Dawnheart, Crown of Cinders, Solar Cataclysm, Sunward Oath | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT |
| 3 | Dawnheart, Crown of Cinders, Emberwake, Eternal Noon | +2 Damage, +5% IDG, +5% IDT, +10% AB |
| 4 | Dawnheart, Crown of Cinders, Emberwake, Sunward Oath | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Dawnheart, Crown of Cinders, Sunward Oath, Golden Mantle | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Dawnheart, Crown of Cinders, Sunward Oath, Ashen Verdict | +2 Damage, +2% IDG, +5% DDG, +2% IDT, +2% DDT |
| 7 | Dawnheart, Emberwake, Eternal Noon, Sunward Oath | +5% IDG, +2% DDG, +5% IDT, +2% DDT, +10% AB |
| 8 | Dawnheart, Emberwake, Sunward Oath, Golden Mantle | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +3% AB |
| 9 | Dawnheart, Emberwake, Sunward Oath, Ashen Verdict | +2% IDG, +5% DDG, +2% IDT, +2% DDT, +3% AB |
| 10 | Dawnheart, Sunward Oath, Golden Mantle, Sovereign Sun | +5% IDG, +2% DDG, +2% IDT, +10% DDT |
| 11 | Dawnheart, Sunward Oath, Golden Mantle, Ashen Verdict | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | Dawnheart, Sunward Oath, Ashen Verdict, Dying Light | +2% IDG, +10% DDG, +7% IDT, +2% DDT |
| 13 | Sunward Oath, Golden Mantle, Sovereign Sun, Ashen Verdict | +3% IDG, +5% DDG, +10% DDT |
| 14 | Sunward Oath, Golden Mantle, Ashen Verdict, Dying Light | +10% DDG, +5% IDT, +5% DDT |

## Design notes

- Calibration reference, not a template. Node names, tiers, prerequisites and every modifier value are copied unchanged from the approved handoff (examples/taiyo_kami.json); only the scope, display units and generated metadata follow RUL-2026-10-03-005.
- Route identities: Burst +5 Damage (Crown of Cinders +2, Solar Cataclysm +3); Burn pressure +10% Afterburn (Emberwake +3%, Eternal Noon +7%); Fortified offense +10% Decrease Damage Taken; Suppression +10% Decrease Damage Given.
- The original handoff files under examples/ are historical evidence: they keep the earlier per-bloodline scope wording and the old raw-power Damage label, and are not regenerated.

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

