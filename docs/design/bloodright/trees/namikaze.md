# Namikaze — The Shearing Sky

**Bloodline:** Namikaze (BR-048, rank C, `0Uc2Nfgg08kqGm78QAwZ4`) · **Revision:** Draft 2 / Namikaze classification / forked tree · **Classification:** Namikaze (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Wind offense — Damage on Cutting Tempest, Tempest Shroud and Wind Step; self Increase Damage Given on Cutting Tempest (and the hidden Soaring Fujin) · secondary Pressure — Afterburn on Tempest Shroud's circle (enemy debuff, ally hazard) · tertiary Control — self Decrease Damage Taken on Tempest Shroud; enemy Decrease Damage Given on Wind Step's circle.

Five of the eight supported rows are offensive: three Wind Damage rows (Cutting Tempest 45, Tempest Shroud 40, Wind Step 40 at jutsu level 25) and two self Increase Damage Given rows (Cutting Tempest 35%, Wind-only; Soaring Fujin 21.25%, a hidden NORMAL-type cast), all sitting over a 15% + 0.15/level Wind Increase Damage Given passive, so offense is primary and gets a raw-power route plus a buff-weighted Foundation. Tempest Shroud carries three of the eight rows on one A-rank cast: its 35% Afterburn is a single enemy debuff whose value lands on every later non-pierce hit, so pressure is secondary with one route. Control is two universal 30% rows, self Decrease Damage Taken on Tempest Shroud and enemy Decrease Damage Given on Wind Step's ground circle, each held to the single-row +10 shape. Move and pool-cost rows are unsupported.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Namikaze jutsu (bloodline-keyed classification, proposed extension) under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Wind at the Back | Foundation | None | +3% Increase Damage Given (self buff) | Cutting Tempest, Soaring Fujin / 2 |
| 02 | Razor Crosswind | Hidden Art | Wind at the Back | +2 Damage power (damage) | Cutting Tempest, Tempest Shroud, Wind Step / 3 |
| 03 | Cleaving Cyclone | Advanced Art | Razor Crosswind | +3 Damage power (damage) | Cutting Tempest, Tempest Shroud, Wind Step / 3 |
| 04 | Searing Squall | Hidden Art | Wind at the Back | +3% Afterburn (enemy debuff) | Tempest Shroud / 1 |
| 05 | Fanning the Flames | Advanced Art | Searing Squall | +7% Afterburn (enemy debuff); +2% Increase Damage Given (self buff) | Cutting Tempest, Soaring Fujin, Tempest Shroud / 3 |
| 06 | Eye of the Storm | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Tempest Shroud, Wind Step / 2 |
| 07 | Windward Guard | Hidden Art | Eye of the Storm | +3% Decrease Damage Taken (self buff) | Tempest Shroud / 1 |
| 08 | Heart of the Tempest | Advanced Art | Windward Guard | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Cutting Tempest, Soaring Fujin, Tempest Shroud / 3 |
| 09 | Smothering Headwind | Hidden Art | Eye of the Storm | +3% Decrease Damage Given (enemy debuff) | Wind Step / 1 |
| 10 | Dead Calm | Advanced Art | Smothering Headwind | +5% Decrease Damage Given (enemy debuff); +1 Damage power (damage) | Cutting Tempest, Tempest Shroud, Wind Step / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Wind at the Back** — Every stride is carried; the gale behind you lends its weight to the blade. Cutting Tempest self buff 35→38% (Wind hits, 2 rounds, CD 6); Soaring Fujin 21.25→24.25% (hidden NORMAL-type cast, broad stat filter).
- **Razor Crosswind** — Turn the breeze edge-on and it opens skin before it is felt. Cutting Tempest 45→47, Tempest Shroud 40→42, Wind Step 40→42 Wind power; three hits at 60 AP (CD 6/7/7), two of them circles.
- **Cleaving Cyclone** — The whole sky leans into one cut. Same three Wind Damage rows; route total +5 (Cutting Tempest 50, Tempest Shroud 45, Wind Step 45). Move and pool-cost rows unsupported.
- **Searing Squall** — Fast air over an open wound burns hotter than any flame. Tempest Shroud Afterburn only: 35→38% for 2 rounds on every other user in the circle, allies included; value lands on every non-pierce hit.
- **Fanning the Flames** — Feed the fire its favourite thing: more wind. Shroud Afterburn 38→45% (route +10); Cutting Tempest buff 38→40% and Soaring Fujin 24.25→26.25% with Wind at the Back.
- **Eye of the Storm** — At the still centre nothing lands clean, and nothing thrown from inside flies true. Tempest Shroud self Decrease Damage Taken 30→32% (every non-pierce hit); Wind Step circle Decrease Damage Given 30→32% on enemies on its tiles.
- **Windward Guard** — Stand where the gale breaks first and let it take the blow. Tempest Shroud Decrease Damage Taken only: 32→35% with Eye of the Storm; one self row, 2 rounds per 60 AP A-rank cast, CD 7.
- **Heart of the Tempest** — Inside the wall of wind you are untouched, and everything you throw leaves faster. Decrease Damage Taken to route total 40% (+10); Cutting Tempest buff 35→37% (40% with Wind at the Back), Soaring Fujin 23.25%.
- **Smothering Headwind** — Every swing thrown into the wind arrives spent. Wind Step Decrease Damage Given only: 32→35% with Eye of the Storm; 2-round circle re-applies a one-round debuff per round to enemies on it.
- **Dead Calm** — When the air goes dead, so does the arm that swings through it. Wind Step suppression to route total 40% (+10); all three Wind Damage rows +1 (Cutting Tempest 46, Tempest Shroud 41, Wind Step 41).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT | AB |
|---|---|---:|---:|---:|---:|---:|
| Cleaving Cyclone (Burst) | Wind at the Back, Razor Crosswind, Cleaving Cyclone, Eye of the Storm | +5 | +3% | +2% | +2% | — |
| Fanning the Flames (Burn pressure) | Wind at the Back, Searing Squall, Fanning the Flames, Eye of the Storm | — | +5% | +2% | +2% | +10% |
| Heart of the Tempest (Fortress) | Eye of the Storm, Windward Guard, Heart of the Tempest, Wind at the Back | — | +5% | +2% | +10% | — |
| Dead Calm (Suppression) | Eye of the Storm, Smothering Headwind, Dead Calm, Windward Guard | +1 | — | +10% | +5% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken · AB = Afterburn. Values are per-matching-row static additions, not final combat percentages.

- **Cleaving Cyclone:** The +5 power route on all three Wind Damage rows (Cutting Tempest 50, Tempest Shroud 45, Wind Step 45), multiplied downstream by the Wind passive and by Cutting Tempest's own buff at 38%. Eye of the Storm is the fourth purchase because it hardens the two casts the rotation already uses (Shroud 32% Decrease Damage Taken, Wind Step 32% suppression) without re-buying offense; Searing Squall (Afterburn 38%) is the all-in alternative.
- **Fanning the Flames:** Tempest Shroud's Afterburn at the route maximum 45% (+10) for 2 rounds on every other user in the circle (allies included), so every non-pierce hit a debuffed target takes from the player, allies or weapons adds up to 45% more, with both self buffs at +5 (Cutting Tempest 40%, Soaring Fujin 26.25%) feeding larger hits into the burn. Eye of the Storm is the fourth purchase for 32% self shield and 32% suppression; Razor Crosswind (47/42/42 power) is the offensive alternative.
- **Heart of the Tempest:** Tempest Shroud's universal Decrease Damage Taken at the route maximum 40% (+10) for two rounds per A-rank cast, with Cutting Tempest's Wind buff at 40% from the capstone's secondary plus Wind at the Back, and Wind Step suppression at 32%. Wind at the Back is the fourth purchase because it compounds the self-buff secondary; Smothering Headwind (suppression 35%) is the defensive alternative.
- **Dead Calm:** Wind Step's circle Decrease Damage Given at the route maximum 40% (+10) on every enemy standing in it, with Tempest Shroud's Decrease Damage Taken at 35% (+5) and all three Wind hits +1 power: a control build that blunts what the enemy deals and shrugs off what gets through while the kit's offense stays near base. Windward Guard is the fourth purchase for shield depth; Wind at the Back (buffs 38% / 24.25%) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Wind Step | 0 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Wind Step | 1 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 41 (+1) |
| Wind Step | 2 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |
| Tempest Shroud | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 41 (+1) |
| Tempest Shroud | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 35% (+5) |
| Tempest Shroud | 2 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Cutting Tempest | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 46 (+1) |
| Cutting Tempest | 1 | Increase Damage Given | self | 35% | 38% (+3) | 40% (+5) | 40% (+5) | 35% |
| Soaring Fujin | 0 | Increase Damage Given | self | 21.25% | 24.25% (+3) | 26.25% (+5) | 26.25% (+5) | 21.25% |
| Soaring Fujin | 1 | decreasepoolcost (unsupported) | self | 18.75% | 18.75% | 18.75% | 18.75% | 18.75% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Decrease Damage Given +10%, Decrease Damage Taken +10%, Afterburn +10% (not jointly attainable)
- Supported rows in kit: 8 (AB 1, DMG 3, DDG 1, DDT 1, IDG 2)
- Strongest full build by row-weighted total: Wind at the Back, Razor Crosswind, Searing Squall, Fanning the Flames (raw +17, row-weighted 26)
- Lowest row-weighted node: Searing Squall (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Tempest Shroud#2

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Wind at the Back, Razor Crosswind, Cleaving Cyclone, Searing Squall | DMG +5, IDG +3, AB +3 |
| 2 | Wind at the Back, Razor Crosswind, Cleaving Cyclone, Eye of the Storm | DMG +5, IDG +3, DDG +2, DDT +2 |
| 3 | Wind at the Back, Razor Crosswind, Searing Squall, Fanning the Flames | DMG +2, IDG +5, AB +10 |
| 4 | Wind at the Back, Razor Crosswind, Searing Squall, Eye of the Storm | DMG +2, IDG +3, DDG +2, DDT +2, AB +3 |
| 5 | Wind at the Back, Razor Crosswind, Eye of the Storm, Windward Guard | DMG +2, IDG +3, DDG +2, DDT +5 |
| 6 | Wind at the Back, Razor Crosswind, Eye of the Storm, Smothering Headwind | DMG +2, IDG +3, DDG +5, DDT +2 |
| 7 | Wind at the Back, Searing Squall, Fanning the Flames, Eye of the Storm | IDG +5, DDG +2, DDT +2, AB +10 |
| 8 | Wind at the Back, Searing Squall, Eye of the Storm, Windward Guard | IDG +3, DDG +2, DDT +5, AB +3 |
| 9 | Wind at the Back, Searing Squall, Eye of the Storm, Smothering Headwind | IDG +3, DDG +5, DDT +2, AB +3 |
| 10 | Wind at the Back, Eye of the Storm, Windward Guard, Heart of the Tempest | IDG +5, DDG +2, DDT +10 |
| 11 | Wind at the Back, Eye of the Storm, Windward Guard, Smothering Headwind | IDG +3, DDG +5, DDT +5 |
| 12 | Wind at the Back, Eye of the Storm, Smothering Headwind, Dead Calm | DMG +1, IDG +3, DDG +10, DDT +2 |
| 13 | Eye of the Storm, Windward Guard, Heart of the Tempest, Smothering Headwind | IDG +2, DDG +5, DDT +10 |
| 14 | Eye of the Storm, Windward Guard, Smothering Headwind, Dead Calm | DMG +1, DDG +10, DDT +5 |

## Design notes

- Node split: root Wind at the Back (self-facing, +3 Increase Damage Given on both buff rows) forks into a Damage route (Razor Crosswind → Cleaving Cyclone) and a burn route (Searing Squall → Fanning the Flames). Root Eye of the Storm (control-facing, +2 Decrease Damage Taken on Tempest Shroud, +2 Decrease Damage Given on Wind Step's circle) forks into a shield route (Windward Guard → Heart of the Tempest) and a suppression route (Smothering Headwind → Dead Calm). 2 F / 4 H / 4 A; every capstone 3 BP deep; two capstones cost 5 or 6 BP.
- Flats scale by coverage. Damage reaches three Wind rows (45/40/40) and keeps the reference ladder +2/+3 (max +5, not the +6 two-row kits use; Dead Calm's +1 lifts a suppression build to +1 only). Afterburn is one downstream row: 3+7 = +10 (35→45%). Decrease Damage Taken and Decrease Damage Given are one universal row each and take the single-row 2/3/5 shape (30→40%). Increase Damage Given reaches two rows, one hidden, so it is a +3 Foundation plus +2 capstone secondaries: max +5 (Cutting Tempest 40%, Soaring Fujin 26.25%).
- Capstone secondaries never out-bid a Hidden Art on the same tag: Fanning the Flames and Heart of the Tempest add +2 self buff (no Hidden Art carries Increase Damage Given); Dead Calm adds +1 Damage under Razor Crosswind's +2. Row-weighted node values (Σ flat × rows reached): Foundations 6/4, Hidden Arts 6/3/3/3, Advanced Arts 9/11/9/8; full builds span 16–26 (raw flat 11–19) against Taiyo Kami's 16–31 (raw 12–24) on nine rows. Maxima over legal builds: Damage +5, IDG +5, Afterburn +10, DDT +10, DDG +10; not jointly attainable.
- Matching at the pin (tags.ts getEfficiencyRatio): Cutting Tempest's buff row lists Wind with no stat or general filter, so it multiplies Wind hits only, including Wind normal jutsu, not element-less hits. Soaring Fujin's row lists Wind plus the Highest stat and all four general types, so it multiplies nearly every hit the caster lands. The three enemy/self percentage rows (Shroud DDT and Afterburn, Wind Step DDG) list all four stat types with no element, so they cover every non-pierce hit. Pierce ignores all of them; the Wind IDG passive multiplies the enhanced Damage rows.
- Delivery and uptime: Tempest Shroud (A rank, 60 AP, CD 7, OTHER_USER circle, range 4) carries Damage, the self shield and the Afterburn, so every route touches it; its percentage rows last 2 rounds. Wind Step (D rank, 60 AP, CD 7) is an EMPTY_GROUND circle (range 5): its Damage hits enemies once and its 2-round ground circle re-applies the suppression each round, as a one-round debuff, to enemies standing on the tiles. Cutting Tempest (C rank, 60 AP, CD 6, single target) is the fastest cast and its 2-round buff windows the follow-up Wind hits. Soaring Fujin is a hidden SELF cast (60 AP, CD 6).
- Fourth purchases: Burst (01,02,03) → Eye of the Storm or Searing Squall; Burn (01,04,05) → Eye of the Storm or Razor Crosswind; Fortress (06,07,08) → Wind at the Back or Smothering Headwind; Suppression (06,09,10) → Windward Guard or Wind at the Back. Six no-capstone hybrids (01,02,04,06; 01,02,06,07; 01,02,06,09; 01,04,06,07; 01,04,06,09; 01,06,07,09) stay distinct. Strongest unadvertised allocation by row weight: 01,02,04,05 (Damage +2, IDG +5, Afterburn +10) at 26, one above the advertised Burst build. Four examples: each capstone closes a different role.

## Risks and unproven interactions

- Ally hazard: Tempest Shroud's Afterburn row is INHERIT-target on an AOE_CIRCLE_SPAWN with no friendly-fire value (treated as ALL), so allies standing in the circle also receive the debuff and take extra Afterburn damage from hits they suffer; the caster is never a target of an OTHER_USER area cast and no ground effect is created (actions.ts 1029-1060). Searing Squall and Fanning the Flames raise that to 38% and 45%. The Damage row is friendly-fire ENEMIES and the shield row targets SELF, so only the burn is hazardous; positioning decides.
- Afterburn: Fanning the Flames puts the Shroud debuff at 45% for 2 rounds on every other user in the circle (allies included, never the caster). Every non-pierce hit a debuffed target takes (kit, normal jutsu, weapons, allies) adds floor(damage × 45%), cumulative Afterburn per hit capped at 60% of the hit, so it saturates alongside other Afterburn sources. BATTLE_TAG_STACKING is on at the pin. Not a damage instance; downstream instances were not simulated.
- Classification: Wind sits on rows of 28 other census bloodlines (Aerathiel, Houkyuken, Shiroi Youso and others), so the label is the bloodline-keyed extension 'Namikaze' (proposed whole-kit resolver plus a classification extension). With ['Wind'] today 5 of 8 supported rows match directly; the three element-less rows fall back to None, which also reaches other non-elemental jutsu. Normal-jutsu Wind collisions are unverified.
- Increase Damage Given scope: Cutting Tempest's row carries elements ['Wind'] with no stat or general filter, so at the pin it multiplies Wind hits only (kit Damage rows, Wind normal jutsu); element-less basic attacks and weapons are not matched. Soaring Fujin's row (Wind, Highest stat, four general types) multiplies nearly every hit for 2 rounds, but it is a hidden NORMAL-type jutsu whose obtainability was not verified; if uncastable, IDG is one row and Wind at the Back is the weakest Foundation.
- Shield and suppression delivery: Tempest Shroud's Decrease Damage Taken is a SELF row on an OTHER_USER circle, realized on the caster at cast time (actions.ts 1060-1075; SOURCE_MECHANICS.md §4b), not positionally; the cast needs any other living user, ally or enemy, within range 4. Wind Step's suppression is a 2-round ground circle that re-applies a one-round debuff each round to enemies on its tiles (process.ts 321-340); one who steps off loses it at the end of that round. Both ride 60 AP casts on CD 7.
- Value decisions (user-owned): Decrease Damage Taken and Decrease Damage Given each reach +10 on a single universal row (30→40%), Afterburn +10, Damage +5 on three rows, Increase Damage Given +5. The brief says to adjust by coverage rather than rank, but this is a C-rank bloodline; lower control ladders (for example 2/3/4 = +9) remain available if the user prefers. No combat simulation was performed.
- Damage is formula-calculated (sqrt stat scaling) and then multiplied by the Wind Increase Damage Given passive and Cutting Tempest's buff, so +5 raw power is not a linear +5 damage. Two of the three Damage rows are circle hits with friendly fire ENEMIES (no ally hazard). Wind Step's move and Soaring Fujin's pool-cost rows are unsupported and receive nothing; mobility is untouched.
- Context not modelled: the bloodline's +10% Increase Damage Taken passive on Fire (a standing weakness) is untouched by any node; skill-tree and bloodline effects are suppressed in RANKED_PVP and RANKED_SPARRING at the pin, so no node applies there; normal-tree potency policy is not approved, so a combined stacking audit precedes implementation. The 14/14 non-dominance count treats every tag as a gain and ignores delivery; it is structural evidence only.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Namikaze jutsu inherit Namikaze potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

