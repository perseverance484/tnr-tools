# Arashima — Reaper's Tempest

**Bloodline:** Arashima (BR-005, rank A, `9F6Ruhuf82gSzpZcsUaPW`) · **Revision:** Director-approved structure (RUL-2026-10-04-003) / Storm classification / forked tree · **Classification:** Storm (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense from Stormsinger's self buff: Storm burst or sustain offense (Tempest Hymn) · secondary Defense: fortress on Stormsinger or suppression on Death's Storm (Stillness in the Squall) · tertiary Lifesteal as the Sustain route's payoff and a light rider on the Fortress.

Director-approved structure (RUL-2026-10-04-003). Tempest Hymn answers "How do I win the storm offensively?": Sundered Sky pushes the Stormsinger buff and adds a narrow +2 Damage to the two 45 EP Storm attacks, while The Storm's Due converts the same buff into +5% Lifesteal sustain. Stillness in the Squall answers "How do I outlast the storm?": Unbroken Horizon protects the singer (+10% Decrease Damage Taken with a small Lifesteal rider) and Silence After Thunder suppresses everyone in Death's Storm (+10% Decrease Damage Given). Potency reaches matching supported tags on all Storm jutsu (RUL-2026-10-03-005).

**Review status:** Director-approved (RUL-2026-10-04-003); protected from the 2026-10-04 batch

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Tempest Hymn | Foundation | How do I win the storm offensively? |
| Stillness in the Squall | Foundation | How do I outlast the storm? |
| Sundered Sky | Advanced Art | burst |
| The Storm's Due | Advanced Art | sustain offense |
| Unbroken Horizon | Advanced Art | fortress |
| Silence After Thunder | Advanced Art | suppression |

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Storm jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempest Hymn | Foundation | None | +3% Increase Damage Given (self buff) | Stormsinger / 1 |
| 02 | Gathering Thunderhead | Hidden Art | Tempest Hymn | +2% Increase Damage Given (self buff) | Stormsinger / 1 |
| 03 | Sundered Sky | Advanced Art | Gathering Thunderhead | +3% Increase Damage Given (self buff); +2 Damage (damage) | Demons Strike, Reapers Storm, Stormsinger / 3 |
| 04 | Crimson Downpour | Hidden Art | Tempest Hymn | +2% Lifesteal (self buff) | Stormsinger / 1 |
| 05 | The Storm's Due | Advanced Art | Crimson Downpour | +3% Lifesteal (self buff); +5% Increase Damage Given (self buff) | Stormsinger / 2 |
| 06 | Stillness in the Squall | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Death’s Storm, Stormsinger / 2 |
| 07 | Stormwarden's Hide | Hidden Art | Stillness in the Squall | +3% Decrease Damage Taken (self buff) | Stormsinger / 1 |
| 08 | Unbroken Horizon | Advanced Art | Stormwarden's Hide | +5% Decrease Damage Taken (self buff); +2% Lifesteal (self buff) | Stormsinger / 2 |
| 09 | Deadwind Dirge | Hidden Art | Stillness in the Squall | +3% Decrease Damage Given (enemy debuff) | Death’s Storm / 1 |
| 10 | Silence After Thunder | Advanced Art | Deadwind Dirge | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff) | Death’s Storm, Stormsinger / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempest Hymn** — The storm sings through Arashima blood; every verse is a wound and a drink. Stormsinger self Increase Damage Given 35 → 38% (2 rounds per 40 AP cast).
- **Gathering Thunderhead** — Clouds mass over the field, heavy with what is about to fall. Stormsinger self buff 38 → 40% with Tempest Hymn.
- **Sundered Sky** — The whole sky comes down at once. Nothing beneath it is spared. Burst: Stormsinger self buff 35 → 43% on the full route; Reapers Storm and Demons Strike Storm Damage 45 → 47 EP (both AoE).
- **Crimson Downpour** — The rain that follows the storm runs red, and it runs toward the singer. Stormsinger Lifesteal 40 → 42%.
- **The Storm's Due** — The storm takes its toll from everything it touches, and pays it back to the singer. Sustain offense: Stormsinger Lifesteal 40 → 45% on the full route (under the 60% leech budget) and self buff 35 → 43% with Tempest Hymn.
- **Stillness in the Squall** — At the heart of the tempest there is a calm that belongs to Arashima alone. Stormsinger Decrease Damage Taken 35 → 37% (self) and Death's Storm Decrease Damage Given 30 → 32% (enemy circle; ally hazard).
- **Stormwarden's Hide** — Years of standing in the gale leave skin the wind no longer bites. Stormsinger Decrease Damage Taken 37 → 40% with Stillness in the Squall.
- **Unbroken Horizon** — The storm has raged all night; at dawn the line still holds. Fortress: Stormsinger Decrease Damage Taken 35 → 45% on the full route; Stormsinger Lifesteal 40 → 42%.
- **Deadwind Dirge** — The wind after Death's Storm carries the strength out of every arm it touches. Death's Storm Decrease Damage Given 32 → 35% with Stillness in the Squall (everyone in the circle; ally hazard).
- **Silence After Thunder** — When the thunder stops, only the Arashima still has the will to strike. Suppression: Death's Storm Decrease Damage Given 30 → 40% on the full route; Stormsinger Decrease Damage Taken 37 → 39% with Stillness in the Squall.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT | LS |
|---|---|---:|---:|---:|---:|---:|
| Sundered Sky (Burst) | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Stillness in the Squall | +2 | +8% | +2% | +2% | — |
| The Storm's Due (Sustain) | Tempest Hymn, Crimson Downpour, The Storm's Due, Stillness in the Squall | — | +8% | +2% | +2% | +5% |
| Unbroken Horizon (Fortress) | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon | — | +3% | +2% | +10% | +2% |
| Silence After Thunder (Suppression) | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder | — | +3% | +10% | +4% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Sundered Sky:** Stormsinger self buff 35 → 43%; Reapers Storm and Demons Strike 45 → 47 EP; Stillness in the Squall is the fourth purchase (+2% DDT/DDG).
- **The Storm's Due:** Stormsinger Lifesteal 40 → 45% and self buff 35 → 43% on the same 2-round cast; Stillness in the Squall is the fourth purchase.
- **Unbroken Horizon:** Stormsinger Decrease Damage Taken 35 → 45%, Lifesteal 42%, self buff 38% with Tempest Hymn as the fourth purchase.
- **Silence After Thunder:** Death's Storm Decrease Damage Given 30 → 40%, Stormsinger Decrease Damage Taken 39%, self buff 38% with Tempest Hymn.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Sustain | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Stormsinger | 0 | Lifesteal | self | 40% | 40% | 45% (+5) | 42% (+2) | 40% |
| Stormsinger | 1 | Increase Damage Given | self | 35% | 43% (+8) | 43% (+8) | 38% (+3) | 38% (+3) |
| Stormsinger | 2 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 39% (+4) |
| Sounds of Tempest | 0 | poison (unsupported) | enemy | 50% | 50% | 50% | 50% | 50% |
| Sounds of Tempest | 1 | increasepoolcost (unsupported) | enemy | 80% | 80% | 80% | 80% | 80% |
| Reapers Storm | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Reapers Storm | 1 | drain (unsupported) | enemy | 250 | 250 | 250 | 250 | 250 |
| Demons Strike | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Demons Strike | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Demons Strike | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Death’s Storm | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Death’s Storm | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Sundered Sky: +8% Increase Damage Given (3 + 2 + 3; off band)
  - Route The Storm's Due: +5% Lifesteal (0 + 2 + 3; on band)
  - Route Unbroken Horizon: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Silence After Thunder: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 6 (DMG 2, DDG 1, DDT 1, IDG 1, LS 1)
- Strongest full build by row-weighted total: Tempest Hymn, Crimson Downpour, The Storm's Due, Stillness in the Squall (raw +17, row-weighted 17)
- Lowest row-weighted node: Gathering Thunderhead (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Death’s Storm#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Reapers Storm | 0 | 45 (High) | 47 (High) |
| Demons Strike | 0 | 45 (High) | 47 (High) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Sundered Sky | +2 Damage, +8% IDG | Crimson Downpour | +2 Damage, +8% IDG, +2% LS | 14 |
| Sundered Sky | +2 Damage, +8% IDG | Stillness in the Squall *(highest diagnostic)* | +2 Damage, +8% IDG, +2% DDG, +2% DDT | 16 |
| The Storm's Due | +8% IDG, +5% LS | Gathering Thunderhead | +10% IDG, +5% LS | 15 |
| The Storm's Due | +8% IDG, +5% LS | Stillness in the Squall *(highest diagnostic)* | +8% IDG, +2% DDG, +2% DDT, +5% LS | 17 |
| Unbroken Horizon | +2% DDG, +10% DDT, +2% LS | Tempest Hymn | +3% IDG, +2% DDG, +10% DDT, +2% LS | 17 |
| Unbroken Horizon | +2% DDG, +10% DDT, +2% LS | Deadwind Dirge *(highest diagnostic)* | +5% DDG, +10% DDT, +2% LS | 17 |
| Silence After Thunder | +10% DDG, +4% DDT | Tempest Hymn | +3% IDG, +10% DDG, +4% DDT | 17 |
| Silence After Thunder | +10% DDG, +4% DDT | Stormwarden's Hide *(highest diagnostic)* | +10% DDG, +7% DDT | 17 |

### Route overlap (diagnostic)

- Sundered Sky / The Storm's Due: similar packages (siblings), path cosine 0.823, shared capstone tags: increasedamagegiven

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Crimson Downpour | +2 Damage, +8% IDG, +2% LS |
| 2 | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Stillness in the Squall | +2 Damage, +8% IDG, +2% DDG, +2% DDT |
| 3 | Tempest Hymn, Gathering Thunderhead, Crimson Downpour, The Storm's Due | +10% IDG, +5% LS |
| 4 | Tempest Hymn, Gathering Thunderhead, Crimson Downpour, Stillness in the Squall | +5% IDG, +2% DDG, +2% DDT, +2% LS |
| 5 | Tempest Hymn, Gathering Thunderhead, Stillness in the Squall, Stormwarden's Hide | +5% IDG, +2% DDG, +5% DDT |
| 6 | Tempest Hymn, Gathering Thunderhead, Stillness in the Squall, Deadwind Dirge | +5% IDG, +5% DDG, +2% DDT |
| 7 | Tempest Hymn, Crimson Downpour, The Storm's Due, Stillness in the Squall | +8% IDG, +2% DDG, +2% DDT, +5% LS |
| 8 | Tempest Hymn, Crimson Downpour, Stillness in the Squall, Stormwarden's Hide | +3% IDG, +2% DDG, +5% DDT, +2% LS |
| 9 | Tempest Hymn, Crimson Downpour, Stillness in the Squall, Deadwind Dirge | +3% IDG, +5% DDG, +2% DDT, +2% LS |
| 10 | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon | +3% IDG, +2% DDG, +10% DDT, +2% LS |
| 11 | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Deadwind Dirge | +3% IDG, +5% DDG, +5% DDT |
| 12 | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder | +3% IDG, +10% DDG, +4% DDT |
| 13 | Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon, Deadwind Dirge | +5% DDG, +10% DDT, +2% LS |
| 14 | Stillness in the Squall, Stormwarden's Hide, Deadwind Dirge, Silence After Thunder | +10% DDG, +7% DDT |

## Design notes

- Director-approved structure (RUL-2026-10-04-003): edges 01→02→03, 01→04→05, 06→07→08, 06→09→10; names Crimson Downpour, The Storm's Due, Stormwarden's Hide and Deadwind Dirge are fixed (not Reaper's Harvest or Torrential Downpour).
- Maxima over every legal allocation: Increase Damage Given +10% (01+04+05+02), Lifesteal +5%, Decrease Damage Taken +10%, Decrease Damage Given +10%, Damage +2 (45 → 47, no tier crossing).
- Delivery: Stormsinger is one 40 AP self cast (Lifesteal 40%, Increase Damage Given 35%, Decrease Damage Taken 35%, 2 rounds, cooldown 7), so three routes share its window. The Storm Damage rows are 60 AP AoE circle spawns; Death's Storm's Decrease Damage Given lands on everyone in its circle (ally hazard).

## Risks and unproven interactions

- Classification: Storm is shared with other bloodlines (expected under RUL-2026-10-03-005). Stormsinger carries no Storm row, so in-kit it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Storm coverage is unverified.
- Lifesteal shares one 60% leech budget with vamp; 45% at the route maximum leaves 15 points of headroom. Lifesteal includes pierce hits and is blocked by healprevent.
- Ally hazard: Death's Storm's Decrease Damage Given (friendly fire none = ALL) also reaches allies in its circle, up to 40% at the Suppression maximum; the caster is never a target.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Storm jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

