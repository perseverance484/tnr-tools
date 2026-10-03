# Bakuhatsu — Doctrine of Detonation

**Bloodline:** Bakuhatsu (BR-008, rank A, `RNUcHSH2c00IhOLc2C9aJ`) · **Revision:** Draft 4 / Explosion classification / forked tree (RUL-2026-10-03-005 recalibration; Increase Damage Given route added) · **Classification:** Explosion (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (Explosion area attacks) · secondary Afterburn and Increase Damage Taken (Charge 4 Explosion pressure) · tertiary Increase Damage Given and Decrease Damage Taken (charge self buffs / Blast Shield).

Three of the eight supported rows are Explosion Damage on 60 AP area attacks (Kinetic Nova 50, Inferno Cataclysm 40, Howitzer Crash 40 EP at jutsu level 25), so burst is the declared role. Charge 4 Explosion carries three supported rows on one 40 AP single-target cast (self Increase Damage Given 35%, enemy Increase Damage Taken 35%, Afterburn 35%, live the two rounds after the cast), which makes it the pressure hub; Howitzer Crash adds a second Increase Damage Given self buff, realized on the caster at cast time and never raising its own hit. Blast Shield's single Decrease Damage Taken row (35%, a caster-only self buff for two rounds) is the only defensive row. There are no heal, lifesteal, reflect or Decrease Damage Given rows, so no sustain or suppression route is invented.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Explosion jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Primed Fuse | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Charge 4 Explosion, Howitzer Crash / 3 |
| 02 | Shaped Charge | Hidden Art | Primed Fuse | +2 Damage (damage) | Howitzer Crash, Inferno Cataclysm, Kinetic Nova / 3 |
| 03 | Ground Zero | Advanced Art | Shaped Charge | +3 Damage (damage) | Howitzer Crash, Inferno Cataclysm, Kinetic Nova / 3 |
| 04 | Powder Keg | Hidden Art | Primed Fuse | +3% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 10 | Critical Mass | Advanced Art | Powder Keg | +5% Increase Damage Given (self buff) | Charge 4 Explosion, Howitzer Crash / 2 |
| 05 | Smoke and Shrapnel | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Afterburn (enemy debuff) | Blast Shield, Charge 4 Explosion / 2 |
| 06 | Hardened Casing | Hidden Art | Smoke and Shrapnel | +3% Decrease Damage Taken (self buff) | Blast Shield / 1 |
| 07 | Siege Battery | Advanced Art | Hardened Casing | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Blast Shield, Charge 4 Explosion, Howitzer Crash / 3 |
| 08 | Slow Burn | Hidden Art | Smoke and Shrapnel | +3% Afterburn (enemy debuff) | Charge 4 Explosion / 1 |
| 09 | Chain Reaction | Advanced Art | Slow Burn | +5% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Charge 4 Explosion / 2 |

Connections: 01→02, 02→03, 01→04, 04→10, 05→06, 06→07, 05→08, 08→09. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Primed Fuse** — Every detonation begins as a held breath and a lit fuse. Charge 4 Explosion and Howitzer Crash self buffs 35 → 37%; Charge 4 Explosion exposure debuff 35 → 37%. 3 rows, no gates.
- **Shaped Charge** — The blast is not larger; it is aimed. Explosion Damage on Inferno Cataclysm and Howitzer Crash 40 → 42 EP and Kinetic Nova 50 → 52 EP (three area rows, all 60 AP, cooldown 7).
- **Ground Zero** — Where the charge lands, the map is redrawn. Damage route total +5: Kinetic Nova 50 → 55 EP, Inferno Cataclysm and Howitzer Crash 40 → 45 EP.
- **Powder Keg** — The body is a magazine; patience is the match. Both Increase Damage Given self buffs (Charge 4 Explosion, Howitzer Crash) 40% with Primed Fuse, each realized at cast time.
- **Critical Mass** — Pack enough charge into one body and the body becomes the bomb. Increase Damage Given route total +10%: the Charge 4 Explosion and Howitzer Crash self buffs 35 → 45%, live the two rounds after each cast.
- **Smoke and Shrapnel** — The blast is over. Its cloud and its fragments are not. Blast Shield Decrease Damage Taken 35 → 37% (caster-only self buff, 2 rounds) and Charge 4 Explosion Afterburn 35 → 37%. 2 rows, 40 AP each.
- **Hardened Casing** — Debris packs into a wall that holds the second time, too. Blast Shield Decrease Damage Taken 40% with Smoke and Shrapnel (one caster-only row, 2 rounds per 40 AP cast).
- **Siege Battery** — Dug in behind the blast wall, the battery keeps firing. Decrease Damage Taken route total +10% (Blast Shield 35 → 45%); both Increase Damage Given self buffs +2% (39% with Primed Fuse).
- **Slow Burn** — Shrapnel lodges hot and stays hot. Charge 4 Explosion Afterburn 40% with Smoke and Shrapnel (single target, range 4, 40 AP, 2 rounds).
- **Chain Reaction** — One blast primes the next. Nothing lands only once. Afterburn route total +10% (Charge 4 Explosion 35 → 45%) and its exposure +3% (38%, 40% with Primed Fuse); one 40 AP cast raises both debuffs.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Ground Zero (Burst) | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg | +5 | +5% | +2% | — | — |
| Critical Mass (Empowered) | Primed Fuse, Shaped Charge, Powder Keg, Critical Mass | +2 | +10% | +2% | — | — |
| Chain Reaction (Pressure) | Smoke and Shrapnel, Slow Burn, Chain Reaction, Primed Fuse | — | +2% | +5% | +2% | +10% |
| Siege Battery (Fortified) | Smoke and Shrapnel, Hardened Casing, Siege Battery, Primed Fuse | — | +4% | +2% | +10% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Ground Zero:** +5 Damage on all three Explosion area attacks (Kinetic Nova 50 → 55, Inferno Cataclysm and Howitzer Crash 40 → 45 EP) plus Primed Fuse. Powder Keg is the all-in fourth purchase: both Increase Damage Given self buffs reach 40%. Cast Charge 4 Explosion and Howitzer Crash (100 AP) in one round; a Kinetic Nova in either of the next two rounds takes both 40% buffs (×1.40 × 1.40) and the 37% exposure. Smoke and Shrapnel (Blast Shield 37%, Afterburn 37%) is the balanced alternative.
- **Critical Mass:** Both Increase Damage Given self buffs reach 45% (Primed Fuse +2%, Powder Keg +3%, Critical Mass +5%): after Charge 4 Explosion and Howitzer Crash in one 100 AP round, every caster hit in the next two rounds that passes their Highest-stat or element-less filter takes both 45% buffs (×1.45 × 1.45 ≈ ×2.10), normal jutsu and weapons included, and Charge 4 Explosion's exposure sits at 37%. Shaped Charge is the fourth purchase (Explosion strikes 42 / 52 EP); Smoke and Shrapnel (Blast Shield 37%, Afterburn 37%) is the defensive alternative.
- **Chain Reaction:** Charge 4 Explosion becomes the whole plan: Afterburn 45% (Smoke and Shrapnel +2%, Slow Burn +3%, Chain Reaction +5%) and exposure 40% (Primed Fuse +2%, Chain Reaction +3%) on one 40 AP cast; in the two rounds after it, every non-pierce hit the target takes, from the caster, allies or weapons, is burned by Afterburn, and raised by the exposure when the hit is Earth, Explosion, Lightning or element-less. Primed Fuse is the fourth purchase because it adds the self buff (37%) and completes the exposure; Hardened Casing (Blast Shield 40%) is the defensive alternative.
- **Siege Battery:** Blast Shield's reduction rises to 45% on the caster (a self buff live the two rounds after each 40 AP cast; allies do not receive it), and Siege Battery's +2% Increase Damage Given keeps the self buffs at 39% with Primed Fuse, so the shielded caster still amplifies a Nova cast after the charge round. Primed Fuse also brings the 37% exposure; Slow Burn (Afterburn 40%) is the alternative fourth purchase for a bunker that still burns.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Empowered | Pressure | Fortified |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Inferno Cataclysm | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Inferno Cataclysm | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Kinetic Nova | 0 | Damage | enemy | 50 | 55 (+5) | 52 (+2) | 50 | 50 |
| Kinetic Nova | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Blast Shield | 0 | Decrease Damage Taken | self | 35% | 35% | 35% | 37% (+2) | 45% (+10) |
| Blast Shield | 1 | barrier (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Charge 4 Explosion | 0 | Increase Damage Given | self | 35% | 40% (+5) | 45% (+10) | 37% (+2) | 39% (+4) |
| Charge 4 Explosion | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 37% (+2) |
| Charge 4 Explosion | 2 | Afterburn | enemy | 35% | 35% | 35% | 45% (+10) | 37% (+2) |
| Howitzer Crash | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Howitzer Crash | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Howitzer Crash | 2 | Increase Damage Given | self | 35% | 40% (+5) | 45% (+10) | 37% (+2) | 39% (+4) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Ground Zero: +5 Damage (0 + 2 + 3; on band)
  - Route Siege Battery: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Chain Reaction: +10% Afterburn (2 + 3 + 5; on band)
  - Route Critical Mass: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 8 (AB 1, DMG 3, DDT 1, IDG 2, IDT 1)
- Strongest full build by row-weighted total: Primed Fuse, Shaped Charge, Powder Keg, Critical Mass (raw +14, row-weighted 28)
- Lowest row-weighted node: Hardened Casing (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg | +5 Damage, +5% IDG, +2% IDT |
| 2 | Primed Fuse, Shaped Charge, Ground Zero, Smoke and Shrapnel | +5 Damage, +2% IDG, +2% IDT, +2% DDT, +2% AB |
| 3 | Primed Fuse, Shaped Charge, Powder Keg, Smoke and Shrapnel | +2 Damage, +5% IDG, +2% IDT, +2% DDT, +2% AB |
| 4 | Primed Fuse, Shaped Charge, Powder Keg, Critical Mass | +2 Damage, +10% IDG, +2% IDT |
| 5 | Primed Fuse, Shaped Charge, Smoke and Shrapnel, Hardened Casing | +2 Damage, +2% IDG, +2% IDT, +5% DDT, +2% AB |
| 6 | Primed Fuse, Shaped Charge, Smoke and Shrapnel, Slow Burn | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +5% AB |
| 7 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Hardened Casing | +5% IDG, +2% IDT, +5% DDT, +2% AB |
| 8 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Slow Burn | +5% IDG, +2% IDT, +2% DDT, +5% AB |
| 9 | Primed Fuse, Powder Keg, Smoke and Shrapnel, Critical Mass | +10% IDG, +2% IDT, +2% DDT, +2% AB |
| 10 | Primed Fuse, Smoke and Shrapnel, Hardened Casing, Siege Battery | +4% IDG, +2% IDT, +10% DDT, +2% AB |
| 11 | Primed Fuse, Smoke and Shrapnel, Hardened Casing, Slow Burn | +2% IDG, +2% IDT, +5% DDT, +5% AB |
| 12 | Primed Fuse, Smoke and Shrapnel, Slow Burn, Chain Reaction | +2% IDG, +5% IDT, +2% DDT, +10% AB |
| 13 | Smoke and Shrapnel, Hardened Casing, Siege Battery, Slow Burn | +2% IDG, +10% DDT, +5% AB |
| 14 | Smoke and Shrapnel, Hardened Casing, Slow Burn, Chain Reaction | +3% IDT, +5% DDT, +10% AB |

## Design notes

- Node split: the roots mirror the two support casts. Primed Fuse (both Increase Damage Given self buffs, Charge 4 Explosion's exposure) forks into Burst (Shaped Charge → Ground Zero) and Empowered (Powder Keg → Critical Mass). Smoke and Shrapnel (Blast Shield reduction, Charge 4 Explosion Afterburn) forks into Fortified (Hardened Casing → Siege Battery) and Pressure (Slow Burn → Chain Reaction). 2/4/4; any two Advanced Arts cost 5–6 BP. The 'AoE Control' trait lives in unsupported rows (recoil, wound, barrier, move) and area shapes, which no node changes.
- Routes: Burst +5 Damage on three rows (Shaped Charge +2, Ground Zero +3); Empowered +10% Increase Damage Given on two self buffs (Primed Fuse +2%, Powder Keg +3%, Critical Mass +5%); Fortified +10% Decrease Damage Taken (Smoke and Shrapnel +2%, Hardened Casing +3%, Siege Battery +5%); Pressure +10% Afterburn (Smoke and Shrapnel +2%, Slow Burn +3%, Chain Reaction +5%). Increase Damage Taken has no route because it shares Charge 4 Explosion's cast, target and window with Afterburn: Primed Fuse +2% plus Chain Reaction +3%, maximum +5%.
- Structure change: the earlier nine-node narrow-kit exception left Powder Keg as a leaf to hold the two-row Increase Damage Given tag at +5% under the superseded two-row guardrail. RUL-2026-10-03-005 sets that tag's ceiling at +10%, so the kit supports a fourth distinct route and Critical Mass now sits above Powder Keg (+5% only; Siege Battery's +2% secondary cannot combine with it). Powder Keg remains the Burst route's all-in fourth purchase.
- Filters/passives: both Increase Damage Given rows filter the Highest stat, no element, so they raise every element-less hit of any stat type and Highest-stat elemental hits; the exposure row lists Earth/Explosion/Lightning/None; Afterburn and Blast Shield rows take every non-pierce hit. The bloodline Increase Damage Given passive (25% + 0.15/level, Lightning/Earth/Explosion/None) multiplies last, after the jutsu rows (SOURCE_MECHANICS §3b); the Earth-only 15% Decrease Damage Taken passive does not touch Blast Shield's row.
- Delivery and uptime: all five jutsu have cooldown 7. Damage casts cost 60 AP (Inferno Cataclysm spiral of radius 4 around the caster; Kinetic Nova circle spawn on a target, range 4; Howitzer Crash circle spawn on empty ground, range 5, moving the caster). Charge 4 Explosion: 40 AP, single target, range 4. Blast Shield: 40 AP. Every buff and debuff row is live only in the two rounds after its cast; the SELF rows (both IDG, Blast Shield's DDT) land on the caster at cast, not through tiles.
- Fourth purchase choices: Burst takes Powder Keg (Increase Damage Given +5%, all-in) or Smoke and Shrapnel (Decrease Damage Taken and Afterburn +2%); Empowered takes Shaped Charge (+2 Damage) or Smoke and Shrapnel; Pressure takes Primed Fuse (self buffs +2%, exposure +5% total) or Hardened Casing (Decrease Damage Taken +5%); Fortified takes Primed Fuse (self buffs +4%, exposure +2%) or Slow Burn (Afterburn +5%). Hybrids with no Advanced Art spread smaller gains across four tags. All 14 legal full builds are non-dominated and no node is universal.
- Stacking (§3b): same-tag effects from different jutsu or casters all apply and compound. Howitzer Crash plus Charge 4 Explosion in one 100 AP round leaves both Increase Damage Given self buffs live for the next two rounds: ×1.35 × 1.35 ≈ ×1.82 unmodified, ×1.37 × 1.37 ≈ ×1.88 with Primed Fuse, ×1.39 × 1.39 ≈ ×1.93 with Fuse and Siege Battery, ×1.40 × 1.40 = ×1.96 with Fuse and Powder Keg, ×1.45 × 1.45 ≈ ×2.10 on the Empowered route. Cooldown 7 exceeds each two-round window, so one jutsu's windows never overlap. An ally's Increase Damage Taken on the charged target applies alongside the exposure, and an ally's Afterburn adds to it (Afterburn capped at 60% per hit).

## Risks and unproven interactions

- Single-cast concentration: Chain Reaction raises both Charge 4 Explosion debuff rows (Afterburn 45%, exposure 38–40%) and Primed Fuse / Powder Keg / Critical Mass / Siege Battery raise its self buff, so one 40 AP C-rank cast can carry three enhanced rows at once. Per-AP value of that cast rises more than the 60 AP damage route's; no combat simulation was run.
- Row reach: the enhanced Increase Damage Given rows multiply every caster hit (jutsu, weapon, basic attack) passing their Highest-stat or element-less filter (×1.45 each, compounding, at the Empowered maximum); the exposure and Afterburn debuffs raise damage dealt by allies and weapons to the charged target; Blast Shield's enhanced reduction is caster-only. Casting scope does not restrict downstream benefit.
- Afterburn value is downstream: it depends on how many non-pierce hits the charged target takes during the two-round window, and cumulative Afterburn per hit is capped at 60% of that hit, so a 45% debuff leaves only 15 points for any other Afterburn source. Pierce hits are skipped by Afterburn and by the exposure modifier alike.
- Howitzer Crash delivery: its Increase Damage Given row is SELF, realized on the caster at cast and live the two rounds after; not positional, never on allies, so Powder Keg, Critical Mass and Siege Battery values on it need only an empty tile in range 5 (Charge 4 Explosion's need a living non-caster target). Its damage row (ENEMIES) and unsupported move row (Enemy hazard) are tile-delivered INHERIT rows.
- Friendly fire: damage rows are ENEMIES-only, so the Damage route never raises damage to allies; Kinetic Nova's unsupported wound row (ally hazard) is untouched. Charge 4 Explosion may be aimed at an ally (OTHER_USER): its enhanced exposure and Afterburn then land on the ally, the self buff still on the caster. Blast Shield's unsupported barrier row reaches anyone on its tiles, enemies included.
- Classification: Explosion is shared with Bakuhatsu Suru Nendo (expected under RUL-2026-10-03-005). 4 of 8 kit rows carry Explosion (three Damage rows and the exposure row); both self buffs, the Afterburn row and Blast Shield's row need the proposed jutsu-classification resolver, and Blast Shield (no Explosion row) additionally needs an authored Explosion jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Explosion coverage is unverified.
- Both Increase Damage Given rows and Blast Shield's reduction are percentage rows at 35% base; the route maxima (45%) are far from the 100 cap, but each is live only in the two rounds after its cast, so realised uptime, not the flat, decides their value.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Explosion jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

