# Ethereal Monarch — Mandate of Heaven

**Bloodline:** Ethereal Monarch (BR-023, rank S, `IxhIoLEmznqdcnc_6MCN9`) · **Revision:** Draft 2 / Yin-Yang classification / forked tree (director correction + RUL-2026-10-03-005 recalibration) · **Classification:** Yin-Yang (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (Tamashī no Sakeme 50, Celestial Sealing 40) and Increase Damage Given (three 35% self buffs: Starlight Veil, Celestial Sealing, Stardust) · secondary Decrease Damage Taken (Starlight Veil 35%, Founder's Wrath 30%) and Reflect (Heavenly Constructs 40%) · tertiary Stardust's enemy debuffs: Increase Damage Taken 35% and Afterburn 30% (reached through Heavenly Constructs' inject window).

Ten supported kit rows on six casts: two Yin-Yang Damage rows, three element-less 35% Increase Damage Given self buffs, two Decrease Damage Taken self rows, one Reflect row and Stardust's two enemy debuffs. The offensive root (Sovereign's Decree) forks into a Damage route and a Stardust burn route; the defensive root (Veil of the Monarch) forks into a Decrease Damage Taken route and a Reflect route. Potency reaches matching supported tags on all Yin-Yang jutsu (RUL-2026-10-03-005). Starlight Veil, Heavenly Constructs and Stardust carry no Yin-Yang row, so in-kit they qualify only through an authored jutsu classification (ENGINE_GAP_REGISTER G1); injection provenance is not a selector.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yin-Yang jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Sovereign's Decree | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Celestial Sealing, Stardust, Starlight Veil / 4 |
| 02 | Tear in the Soul | Hidden Art | Sovereign's Decree | +2 Damage (damage) | Celestial Sealing, Tamashī no Sakeme / 2 |
| 03 | Ethereal Coronation | Advanced Art | Tear in the Soul | +3 Damage (damage) | Celestial Sealing, Tamashī no Sakeme / 2 |
| 04 | Stardust Afterglow | Hidden Art | Sovereign's Decree | +3% Afterburn (enemy debuff) | Stardust / 1 |
| 05 | Rain of Fallen Stars | Advanced Art | Stardust Afterglow | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Celestial Sealing, Stardust, Starlight Veil / 5 |
| 06 | Veil of the Monarch | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Founder’s Wrath, Heavenly Constructs, Starlight Veil / 3 |
| 07 | Woven Starlight | Hidden Art | Veil of the Monarch | +3% Decrease Damage Taken (self buff) | Founder’s Wrath, Starlight Veil / 2 |
| 08 | Immovable Throne | Advanced Art | Woven Starlight | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Celestial Sealing, Founder’s Wrath, Stardust, Starlight Veil / 5 |
| 09 | Mirrored Construct | Hidden Art | Veil of the Monarch | +3% Reflect (self buff) | Heavenly Constructs / 1 |
| 10 | Monarch's Retribution | Advanced Art | Mirrored Construct | +5% Reflect (self buff); +3% Increase Damage Taken (enemy debuff); +2% Decrease Damage Taken (self buff) | Founder’s Wrath, Heavenly Constructs, Stardust, Starlight Veil / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Sovereign's Decree** — The Monarch's word carries weight in every court, and the heavens enforce it. Self damage buffs on Starlight Veil, Celestial Sealing and Stardust 35 → 37%; Stardust exposure 35 → 37%.
- **Tear in the Soul** — What the Monarch rends does not knit back together. Tamashī no Sakeme 50 → 52 and Celestial Sealing 40 → 42 EP (Yin-Yang Damage rows); Founder's Wrath pierce is not a Damage row.
- **Ethereal Coronation** — Crowned beyond the veil, the Monarch strikes with the authority of the sky. Route total +5 Damage: Tamashī no Sakeme 50 → 55 and Celestial Sealing 40 → 45 EP. Damage only (director correction).
- **Stardust Afterglow** — Stardust does not settle; it smolders on whatever it touches. Stardust Afterburn 30 → 33% for 2 rounds; raises the percent per non-pierce hit, not the duration.
- **Rain of Fallen Stars** — When the Monarch is angered, the firmament itself comes down. Stardust Afterburn route total +10% (30 → 40%); Stardust exposure 35 → 40% with Sovereign's Decree; self damage buffs on Starlight Veil, Celestial Sealing and Stardust 35 → 40% with Decree.
- **Veil of the Monarch** — Starlight gathers around the throne, and nothing reaches it unanswered. Self Decrease Damage Taken on Starlight Veil 35 → 37% and Founder's Wrath 30 → 32%; Heavenly Constructs Reflect 40 → 42%.
- **Woven Starlight** — Thread by thread the veil thickens until blades lose their way inside it. Both self DDT rows +3% more: Starlight Veil 40%, Founder's Wrath 35% with Veil of the Monarch.
- **Immovable Throne** — Seated beyond the reach of blades, the Monarch's every decree lands harder. DDT route total +10%: Starlight Veil 35 → 45%, Founder's Wrath 30 → 40%; self damage buffs on Veil, Sealing and Stardust +3% (40% with Sovereign's Decree).
- **Mirrored Construct** — The constructs of heaven are polished to a sheen that returns every blow. Heavenly Constructs Reflect 45% with Veil of the Monarch; includes pierce hits; 60%-of-hit cap.
- **Monarch's Retribution** — Strike the throne and the throne strikes back, then marks you for what follows. Reflect route total +10% (40 → 50%, under the 60% cap); Stardust exposure 40% with Decree; both self DDT rows +2% (39% / 34% with Veil).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|
| Ethereal Coronation (Burst) | Sovereign's Decree, Tear in the Soul, Ethereal Coronation, Veil of the Monarch | +5 | +2% | +2% | +2% | — | +2% |
| Rain of Fallen Stars (Burn pressure) | Sovereign's Decree, Stardust Afterglow, Rain of Fallen Stars, Veil of the Monarch | — | +5% | +5% | +2% | +10% | +2% |
| Immovable Throne (Fortified) | Sovereign's Decree, Veil of the Monarch, Woven Starlight, Immovable Throne | — | +5% | +2% | +10% | — | +2% |
| Monarch's Retribution (Mirror) | Sovereign's Decree, Veil of the Monarch, Mirrored Construct, Monarch's Retribution | — | +2% | +5% | +4% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Ethereal Coronation:** +5 Damage on both Yin-Yang Damage rows (Tamashī no Sakeme 55, Celestial Sealing 45 EP); Sovereign's Decree adds +2% to the three self damage buffs (37%) and Stardust's exposure (37%). Veil of the Monarch is the fourth purchase (Starlight Veil 37%, Founder's Wrath 32% DDT; Reflect 42%).
- **Rain of Fallen Stars:** Afterburn at the route maximum on Stardust (30 → 40%), so every non-pierce hit the marked target takes for two rounds adds extra damage; Stardust's exposure and the three self damage buffs reach 40% with Sovereign's Decree. Founder's Wrath pierce takes no Afterburn. Veil of the Monarch is the fourth purchase.
- **Immovable Throne:** Both self Decrease Damage Taken rows at +10% (Starlight Veil 45%, Founder's Wrath 40%) and the three self damage buffs at 40% (Decree +2%, Throne +3%), with Stardust's exposure at 37% and Reflect 42%. Sovereign's Decree is the fourth purchase.
- **Monarch's Retribution:** Reflect at the route maximum (Heavenly Constructs 50%, ten points under the 60%-of-hit cap), returned on every hit taken, pierce included, for two rounds per cast, with Stardust's exposure at 40% (Decree +2%, Retribution +3%); the self DDT rows sit at 39% / 34%. Sovereign's Decree is the fourth purchase.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortified | Mirror |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Stardust | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Stardust | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 40% (+5) |
| Stardust | 2 | Afterburn | enemy | 30% | 30% | 40% (+10) | 30% | 30% |
| Tamashī no Sakeme | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Tamashī no Sakeme | 1 | consume (unsupported) **adverse** | enemy | 60% | 60% | 60% | 60% | 60% |
| Founder’s Wrath | 0 | pierce (unsupported) | enemy | 66 | 66 | 66 | 66 | 66 |
| Founder’s Wrath | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 34% (+4) |
| Celestial Sealing | 0 | seal (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Celestial Sealing | 1 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Celestial Sealing | 2 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Heavenly Constructs | 0 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Heavenly Constructs | 1 | Reflect | self | 40% | 42% (+2) | 42% (+2) | 42% (+2) | 50% (+10) |
| Heavenly Constructs | 2 | injectjutsus (unsupported) | self | 110 | 110 | 110 | 110 | 110 |
| Starlight Veil | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 39% (+4) |
| Starlight Veil | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Starlight Veil | 2 | visual (unsupported) **adverse** | self | 1 | 1 | 1 | 1 | 1 |
| Starlight Veil | 3 | clearprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Ethereal Coronation: +5 Damage (0 + 2 + 3; on band)
  - Route Rain of Fallen Stars: +10% Afterburn (0 + 3 + 7; on band)
  - Route Immovable Throne: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Monarch's Retribution: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (AB 1, DMG 2, DDT 2, IDG 3, IDT 1, REF 1)
- Strongest full build by row-weighted total: Sovereign's Decree, Veil of the Monarch, Woven Starlight, Immovable Throne (raw +19, row-weighted 39)
- Lowest row-weighted node: Stardust Afterglow (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Tamashī no Sakeme 50 -> 52, Tamashī no Sakeme 50 -> 55

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage | +5 Damage |
|---|---:|---|---|---|
| Tamashī no Sakeme | 0 | 50 (Nuke) | **52 (above Nuke)** | **55 (above Nuke)** |
| Celestial Sealing | 1 | 40 (Normal) | 42 (Normal) | 45 (High) ↑ |

Above-Nuke rationale: Director-corrected tree (2026-10-03; protected from the 2026-10-04 batch): the Burst route's +5 Damage (Tear in the Soul +2, Ethereal Coronation +3) lifts Tamashī no Sakeme 50 → 55 (52 with Tear in the Soul alone), past the 50 Nuke tier. Not retuned here; flagged for director review under BALANCE_REVIEW_METHOD.md.

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Ethereal Coronation | +5 Damage, +2% IDG, +2% IDT | Stardust Afterglow | +5 Damage, +2% IDG, +2% IDT, +3% AB | 21 |
| Ethereal Coronation | +5 Damage, +2% IDG, +2% IDT | Veil of the Monarch *(highest diagnostic)* | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% REF | 24 |
| Rain of Fallen Stars | +5% IDG, +5% IDT, +10% AB | Tear in the Soul | +2 Damage, +5% IDG, +5% IDT, +10% AB | 34 |
| Rain of Fallen Stars | +5% IDG, +5% IDT, +10% AB | Veil of the Monarch *(highest diagnostic)* | +5% IDG, +5% IDT, +2% DDT, +10% AB, +2% REF | 36 |
| Immovable Throne | +3% IDG, +10% DDT, +2% REF | Sovereign's Decree *(highest diagnostic)* | +5% IDG, +2% IDT, +10% DDT, +2% REF | 39 |
| Immovable Throne | +3% IDG, +10% DDT, +2% REF | Mirrored Construct | +3% IDG, +10% DDT, +5% REF | 34 |
| Monarch's Retribution | +3% IDT, +4% DDT, +10% REF | Sovereign's Decree *(highest diagnostic)* | +2% IDG, +5% IDT, +4% DDT, +10% REF | 29 |
| Monarch's Retribution | +3% IDT, +4% DDT, +10% REF | Woven Starlight | +3% IDT, +7% DDT, +10% REF | 27 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Sovereign's Decree, Tear in the Soul, Ethereal Coronation, Stardust Afterglow | +5 Damage, +2% IDG, +2% IDT, +3% AB |
| 2 | Sovereign's Decree, Tear in the Soul, Ethereal Coronation, Veil of the Monarch | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Sovereign's Decree, Tear in the Soul, Stardust Afterglow, Rain of Fallen Stars | +2 Damage, +5% IDG, +5% IDT, +10% AB |
| 4 | Sovereign's Decree, Tear in the Soul, Stardust Afterglow, Veil of the Monarch | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% REF |
| 5 | Sovereign's Decree, Tear in the Soul, Veil of the Monarch, Woven Starlight | +2 Damage, +2% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Sovereign's Decree, Tear in the Soul, Veil of the Monarch, Mirrored Construct | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Sovereign's Decree, Stardust Afterglow, Rain of Fallen Stars, Veil of the Monarch | +5% IDG, +5% IDT, +2% DDT, +10% AB, +2% REF |
| 8 | Sovereign's Decree, Stardust Afterglow, Veil of the Monarch, Woven Starlight | +2% IDG, +2% IDT, +5% DDT, +3% AB, +2% REF |
| 9 | Sovereign's Decree, Stardust Afterglow, Veil of the Monarch, Mirrored Construct | +2% IDG, +2% IDT, +2% DDT, +3% AB, +5% REF |
| 10 | Sovereign's Decree, Veil of the Monarch, Woven Starlight, Immovable Throne | +5% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Sovereign's Decree, Veil of the Monarch, Woven Starlight, Mirrored Construct | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Sovereign's Decree, Veil of the Monarch, Mirrored Construct, Monarch's Retribution | +2% IDG, +5% IDT, +4% DDT, +10% REF |
| 13 | Veil of the Monarch, Woven Starlight, Immovable Throne, Mirrored Construct | +3% IDG, +10% DDT, +5% REF |
| 14 | Veil of the Monarch, Woven Starlight, Mirrored Construct, Monarch's Retribution | +3% IDT, +7% DDT, +10% REF |

## Design notes

- Director correction (2026-10-03): Ethereal Coronation is +3 Damage only (its +2% Increase Damage Given was removed) and Rain of Fallen Stars is +7% Afterburn, +3% Increase Damage Taken, +3% Increase Damage Given. Recalibration under RUL-2026-10-03-005: Immovable Throne's Decrease Damage Taken rises from +2% to +5% so the Fortified route lands on +10% (was +7%), the same Hidden +3% / Advanced +5% shape as Taiyo Kami's Sovereign Sun.
- Routes: Burst +5 Damage (Tear in the Soul +2, Ethereal Coronation +3); Burn pressure +10% Afterburn (Stardust Afterglow +3%, Rain of Fallen Stars +7%); Fortified +10% Decrease Damage Taken (Veil +2%, Woven Starlight +3%, Immovable Throne +5%); Mirror +10% Reflect (Veil +2%, Mirrored Construct +3%, Monarch's Retribution +5%). Glue maxima over every legal allocation: Increase Damage Given +5%, Increase Damage Taken +5%.
- Every IDG, exposure and DDT row lists all four stat types with no element, so each matches every non-pierce hit of any stat type (SOURCE_MECHANICS §3). Pierce (Founder's Wrath) ignores damage modifiers and takes no Afterburn; Reflect returns pierce hits.
- Delivery: all six casts are cooldown 7 with 2-round windows. Starlight Veil, Heavenly Constructs and Founder's Wrath's DDT row are target SELF and realize on the caster at cast time. Stardust is cast through Heavenly Constructs' 2-round inject (level 110; its rows have no per-level scaling).

## Risks and unproven interactions

- Classification: Yin-Yang is shared with other bloodlines (expected under RUL-2026-10-03-005). 2 of 10 kit rows carry Yin-Yang; the rest need the proposed jutsu-classification resolver, and Starlight Veil, Heavenly Constructs and Stardust additionally need an authored Yin-Yang jutsu classification. Off-kit Yin-Yang coverage is unverified.
- Stacking: the element-less all-stat IDG rows raise basic attacks, weapons and normal jutsu inside their windows and stack when Starlight Veil, Celestial Sealing and Stardust overlap (three rows at 40%). The all-stat Stardust exposure also raises allies' hits. Not simulated.
- Afterburn: one application row (Stardust 40% at the route maximum), 20 points under the 60% per-hit cap; its value depends on non-pierce hits landing in the two rounds after the inject.
- Reflect: 50% at the route maximum, capped at 60% of pre-shield damage per hit; it does not reduce damage taken.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Yin-Yang jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

