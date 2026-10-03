# Namikaze — The Shearing Sky

**Bloodline:** Namikaze (BR-048, rank C, `0Uc2Nfgg08kqGm78QAwZ4`) · **Revision:** Draft 3 / Namikaze classification / forked tree · **Classification:** Namikaze (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Wind offense — Damage on Cutting Tempest, Tempest Shroud and Wind Step; self Increase Damage Given on Cutting Tempest (and the hidden Soaring Fujin) · secondary Pressure — Afterburn on Tempest Shroud's circle (enemy debuff, ally hazard) · tertiary Control — self Decrease Damage Taken on Tempest Shroud; enemy Decrease Damage Given on Wind Step's circle.

Five of the eight supported rows are offensive: three Wind Damage rows (Cutting Tempest 45, Tempest Shroud 40, Wind Step 40 at jutsu level 25) and two self Increase Damage Given rows (Cutting Tempest 35%, Wind-only; hidden Soaring Fujin 21.25%), over a 15% + 0.15/level Wind Increase Damage Given passive, so offense is primary with a raw-power route and a buff-weighted Foundation. Tempest Shroud carries three rows on one A-rank cast; its 35% Afterburn is one debuff row whose value lands on every later non-pierce hit a debuffed target takes, so pressure is secondary with one route. Control is two element-less 30% rows, self Decrease Damage Taken on Tempest Shroud and enemy Decrease Damage Given on Wind Step's ground circle, each held to the single-row +10 shape; move and pool-cost rows are unsupported.

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
- **Eye of the Storm** — At the still centre nothing lands clean, and nothing thrown from inside flies true. Tempest Shroud self Decrease Damage Taken 30→32% (non-pierce hits); Wind Step circle Decrease Damage Given 30→32% on enemies on its tiles.
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

- **Cleaving Cyclone:** The +5 power route on all three Wind Damage rows (Cutting Tempest 50, Tempest Shroud 45, Wind Step 45), multiplied by the Wind passive; Cutting Tempest's 38% buff adds to the Shroud and Wind Step hits in the two rounds after its cast, never to its own hit. Eye of the Storm is the fourth purchase because it hardens the two casts the rotation already uses (Shroud 32% Decrease Damage Taken, Wind Step 32% suppression) without re-buying offense; Searing Squall (Afterburn 38%) is the all-in alternative.
- **Fanning the Flames:** Tempest Shroud's Afterburn at the route maximum 45% (+10) for the two rounds after the cast on every other user in the circle (allies included), so every non-pierce hit a debuffed target takes from the player, allies or weapons adds 45% more (60% per-hit cap); both self buffs at +5 (Cutting Tempest 40%, Soaring Fujin 26.25%) enlarge later hits that feed the burn. Eye of the Storm is the fourth purchase for 32% self shield and 32% suppression; Razor Crosswind (47/42/42 power) is the offensive alternative.
- **Heart of the Tempest:** Tempest Shroud's element-less Decrease Damage Taken at the route maximum 40% (+10) for the two rounds after each A-rank cast, with Cutting Tempest's Wind buff at 40% (capstone secondary plus Wind at the Back) and Wind Step suppression at 32%. Wind at the Back is the fourth purchase because it compounds the self-buff secondary; Smothering Headwind (suppression 35%) is the defensive alternative.
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

- Reference reuse: topology and most flats copy Taiyo Kami nearly verbatim (Eye of the Storm = Sunward Oath +2/+2; Damage +2/+3; Afterburn +3/+7; DDT +3/+5; DDG Hidden Art +3). Departures: no Increase Damage Taken row exists, so Wind at the Back is a single-tag +3 IDG root, the burn and shield capstones carry +2 IDG (not +3 IDT/IDG) and Dead Calm's secondary is +1 Damage, not +5 IDT. The shape fits: the kit has the same four roles (Wind hits, downstream burn, self shield, enemy suppression).
- Flats scale by coverage. Damage reaches three Wind rows (45/40/40) on the +2/+3 ladder (max +5, not the +6 of two-row kits). Afterburn is one downstream row: 3+7 = +10 (35→45%). Decrease Damage Taken and Decrease Damage Given are one element-less row each on the single-row 2/3/5 shape (30→40%). Increase Damage Given reaches two rows, one hidden: +3 Foundation plus +2 capstone secondaries, max +5. Option (user-owned): a 2/3/4 control ladder (+9) for this C-rank bloodline.
- Capstone secondaries never out-bid a Hidden Art on the same tag: Fanning the Flames and Heart of the Tempest add +2 Increase Damage Given (no Hidden Art carries it); Dead Calm adds +1 Damage under Razor Crosswind's +2. Row-weighted node values (Σ flat × rows): Foundations 6/4, Hidden Arts 6/3/3/3, Advanced Arts 9/11/9/8; full builds span 16–26 (raw 11–19) against Taiyo Kami's 16–31 (raw 12–24) on nine rows. Maxima: Damage +5, IDG +5, Afterburn +10, DDT +10, DDG +10; not jointly attainable.
- Matching (tags.ts getEfficiencyRatio): Cutting Tempest's buff row lists Wind with no stat or general filter, so it reaches Wind hits only (kit Damage rows, Wind normal jutsu), not element-less hits. Soaring Fujin's row (Wind, Highest stat, four general types) reaches nearly every hit. Shroud's DDT and Afterburn rows and Wind Step's DDG row are element-less with all four stat types, so they cover every non-pierce hit. Kit buffs add power/100 × staged base (§3b); only the Wind passive multiplies.
- Timing (§3b): each percentage row is live in the two rounds after its cast round, never in it, so Cutting Tempest's buff never helps its own hit or a same-round action and CD 6 keeps it off its own recasts; it lifts the Shroud and Wind Step hits that follow. Tempest Shroud (A, 60 AP, CD 7, OTHER_USER circle, range 4) carries Damage, shield and Afterburn. Wind Step (D, 60 AP, CD 7, EMPTY_GROUND circle, range 5) hits once; its suppression rides the 2-round ground circle.
- Fourth purchases: Burst (01,02,03) → Eye of the Storm or Searing Squall; Burn (01,04,05) → Eye of the Storm or Razor Crosswind; Fortress (06,07,08) → Wind at the Back or Smothering Headwind; Suppression (06,09,10) → Windward Guard or Wind at the Back. Six no-capstone hybrids stay distinct. Strongest unadvertised allocation: 01,02,04,05 (Damage +2, IDG +5, Afterburn +10) at 26 row-weighted, one above Burst. Four examples because each capstone closes a different role.

## Risks and unproven interactions

- Ally hazard: Shroud's Afterburn row is INHERIT on an OTHER_USER circle, friendly fire absent (= ALL): every other user in the circle, allies included, receives it; the caster never does and no ground effect is created (actions.ts 1029-1060; §4b). Searing Squall and Fanning the Flames raise it to 38/45%. Damage is ENEMIES-only and the shield SELF, so only the burn leaks; aim and positioning decide.
- Afterburn: Fanning the Flames puts the Shroud debuff at 45% for the two rounds after the cast. Every non-pierce hit a debuffed target takes (kit, normal jutsu, weapons, allies) adds floor(damage × 45%); Afterburn sources all stack (process.ts 1109-1117) but cumulative Afterburn per hit caps at 60% of the hit, so it saturates. Not a damage instance; downstream value was not simulated.
- Classification: Wind sits on rows of 28 other census bloodlines (Aerathiel, Shiroi Youso and others), so the label is the bloodline-keyed extension 'Namikaze' (whole-kit resolver plus classification extension). With ['Wind'] 5 of 8 supported rows match; the three element-less rows fall back to None, which also reaches other non-elemental jutsu. Normal-jutsu Wind collisions are unverified.
- Increase Damage Given scope: Cutting Tempest's row (Wind, no stat or general filter) adds to Wind hits only; element-less basic attacks and weapons are not matched. Soaring Fujin's row adds to nearly every hit, but it is a hidden NORMAL-type jutsu whose obtainability was not verified; if uncastable, IDG is one row and Wind at the Back is the weakest Foundation.
- Delivery: Tempest Shroud's Decrease Damage Taken is a SELF row realized on the caster at cast time (actions.ts 1060-1075; §4b), not positionally; the cast needs any other living user, ally or enemy, within range 4. Wind Step's 2-round ground circle re-applies a one-round Decrease Damage Given each round to enemies on its tiles (process.ts 321-340); one who steps off loses it at that round's end.
- Value decisions are user-owned: single-row Decrease Damage Taken and Decrease Damage Given each reach +10 (30→40%), Afterburn +10, Damage +5 on three rows and Increase Damage Given +5, set by coverage rather than rank on a C-rank bloodline (lower ladder in design notes). No combat simulation was performed.
- Damage rows are formula-calculated (sqrt stat scaling) and multiplied by the Wind passive (bloodline-sourced); Cutting Tempest's buff adds 35-40% of the staged base only in the two rounds after its cast, so +5 raw power is not +5 damage. Both circle Damage rows are ENEMIES-only. Wind Step's move and Soaring Fujin's pool-cost rows are unsupported; mobility is untouched.
- Context not modelled: the +10% Fire Increase Damage Taken passive (a standing weakness) is untouched; skill-tree and bloodline effects are suppressed in RANKED_PVP and RANKED_SPARRING; normal-tree potency policy is not approved and same-tag potency sources sum at the pin, so a combined audit precedes implementation. The 14/14 non-dominance count ignores delivery; it is structural only.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Namikaze jutsu inherit Namikaze potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

