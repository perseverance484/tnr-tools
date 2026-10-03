# Terra Nova — Tectonic Creed

**Bloodline:** Terra Nova (BR-081, rank C, `AohWgMy9uYF14ivDlE-xq`) · **Revision:** Draft 2 / Terra Nova classification / forked tree · **Classification:** Terra Nova (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Damage (Earth attacks: Earthen Fortitude, Terra Spire) · secondary Decrease Damage Taken (Earth Wall fortification) · tertiary Decrease Damage Given (Earthen Fortitude suppression) and Increase Damage Given (Earth Wall, Earth hits only).

Two of the five supported rows are Earth damage at 38 power (Earthen Fortitude single target, Terra Spire AOE spiral), so the kit's declared role is an Earth bruiser and Damage is primary. Earth Wall (40 AP self cast) carries the only two self buffs: its Decrease Damage Taken row lists all four stat types and no element, so it blunts nearly every non-pierce hit, while its Increase Damage Given row is Earth-only and amplifies Earth damage alone, so fortification outranks amplification in coverage breadth, not in flats. Earthen Fortitude's 30% Decrease Damage Given rides on the single-target hit and is the kit's only supported enemy debuff (Terra Spire's recoil and wound are enemy debuffs outside potency). The three single-row percentage tags are deliberately symmetric at the +10 guardrail, so the secondary/tertiary ordering is presentational, and whether the Earth-only IDG route should stop at +8 instead is the user decision named in risks; no Afterburn, heal, lifesteal or reflect route is invented.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Terra Nova jutsu (bloodline-keyed classification, proposed extension) under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Fault Line | Foundation | None | +1 Damage power (damage); +2% Decrease Damage Given (enemy debuff) | Earthen Fortitude, Terra Spire / 3 |
| 02 | Rending Strata | Hidden Art | Fault Line | +2 Damage power (damage) | Earthen Fortitude, Terra Spire / 2 |
| 03 | Continental Rift | Advanced Art | Rending Strata | +3 Damage power (damage) | Earthen Fortitude, Terra Spire / 2 |
| 04 | Burden of Stone | Hidden Art | Fault Line | +3% Decrease Damage Given (enemy debuff) | Earthen Fortitude / 1 |
| 05 | Pressure of Ages | Advanced Art | Burden of Stone | +5% Decrease Damage Given (enemy debuff); +1 Damage power (damage) | Earthen Fortitude, Terra Spire / 3 |
| 06 | Bedrock Stance | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Earth Wall / 2 |
| 07 | Rampart Discipline | Hidden Art | Bedrock Stance | +3% Decrease Damage Taken (self buff) | Earth Wall / 1 |
| 08 | Unmoved Mountain | Advanced Art | Rampart Discipline | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Earth Wall / 2 |
| 09 | Weight Behind the Blow | Hidden Art | Bedrock Stance | +3% Increase Damage Given (self buff) | Earth Wall / 1 |
| 10 | Landslide Momentum | Advanced Art | Weight Behind the Blow | +5% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Earth Wall / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Fault Line** — The ground splits where you choose, and your enemy stands on the wrong side. Fortitude and Terra Spire Earth damage 38→39 (2 rows, 60 AP, CD 7); Fortitude's Decrease Damage Given 30→32% for 2 rounds on one enemy.
- **Rending Strata** — Layer by layer, the earth is torn open. Both Earth damage rows (Earthen Fortitude single target, Terra Spire AOE spiral): 39→41 power with Fault Line. Range 4, 60 AP, CD 7.
- **Continental Rift** — When the plates move, nothing built upon them survives. The same two Earth damage rows; the route totals +6 power (38→44 on both attacks), then the Earth damage passive multiplies the result.
- **Burden of Stone** — Every swing drags the weight of a quarry behind it. Earthen Fortitude Decrease Damage Given only (single enemy row, 2 rounds, 60 AP, CD 7): 32→35% with Fault Line. Spire's recoil untouched.
- **Pressure of Ages** — What the mountain presses down stays pressed down. Fortitude suppression reaches 40% on the route (30% base); both Earth damage rows +1 (route total +2, 38→40). One 60 AP cast carries both.
- **Bedrock Stance** — Plant your feet where the stone runs deepest. Earth Wall only (40 AP self cast, range 0, CD 7, 2 rounds): Decrease Damage Taken 35→37%; Increase Damage Given 35→37% on Earth hits only.
- **Rampart Discipline** — A wall is only as patient as the one who raised it. Earth Wall Decrease Damage Taken only (one self row, 2 rounds): 37→40% with Bedrock Stance. No element, four stat types: nearly all hits.
- **Unmoved Mountain** — Storms wear themselves out against it, and the mountain does not notice. Earth Wall: Decrease Damage Taken route total 45% (base 35%); Increase Damage Given +2 (39% with Bedrock Stance, Earth hits only).
- **Weight Behind the Blow** — The strike carries the whole hillside with it. Earth Wall Increase Damage Given only (one self row, 2 rounds): 37→40% with Bedrock Stance. Earth-element hits only; no stat filter.
- **Landslide Momentum** — Once the slope begins to move, it does not stop for anyone. Earth Wall: Increase Damage Given route total 45% on Earth hits (base 35%); Decrease Damage Taken +2 (39% with Bedrock Stance). 40 AP cast.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT |
|---|---|---:|---:|---:|---:|
| Continental Rift (Burst) | Fault Line, Rending Strata, Continental Rift, Bedrock Stance | +6 | +2% | +2% | +2% |
| Pressure of Ages (Suppression) | Fault Line, Burden of Stone, Pressure of Ages, Bedrock Stance | +2 | +2% | +10% | +2% |
| Unmoved Mountain (Fortified) | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain | +1 | +4% | +2% | +10% |
| Landslide Momentum (Amplify) | Fault Line, Bedrock Stance, Weight Behind the Blow, Landslide Momentum | +1 | +10% | +2% | +4% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Continental Rift:** The +6 power route on both Earth attacks (Earthen Fortitude and Terra Spire 38→44, applied per target inside the spiral, before the bloodline's Earth damage passive multiplies them) with Fault Line's 32% suppression. Bedrock Stance is the fourth purchase so Earth Wall gives 37% Decrease Damage Taken and 37% Earth amplify; Burden of Stone (suppression 35%) is the attack-root-only alternative (both routes on Earthen Fortitude/Terra Spire; no Earth Wall purchase).
- **Pressure of Ages:** Earthen Fortitude as a control cast: one 60 AP hit at 40 power that leaves the target dealing 40% less damage for 2 rounds (30% base), to the caster and allies alike for any stat-based or element-less hit, pierce excluded. Terra Spire sits at 40. Bedrock Stance is the fourth purchase for Earth Wall at 37%/37%; Rending Strata (attacks 42) is the sharper alternative.
- **Unmoved Mountain:** Earth Wall as the centrepiece: Decrease Damage Taken 45% for 2 rounds (35% base) against every non-pierce hit whose stat resolves to one of the four stat types or that carries no element, Lightning included despite the bloodline's +10% Lightning weakness, with the Earth amplify at 39%. Fault Line is the fourth purchase (attacks 39, suppression 32%); Weight Behind the Blow (Earth amplify 42%) is the offensive alternative.
- **Landslide Momentum:** Earth Wall as a springboard: Increase Damage Given 45% for 2 rounds (35% base) on Earth-element damage only, which covers both bloodline attacks and any Earth normal jutsu but not basic attacks or non-Earth jutsu, with Decrease Damage Taken at 39%. Fault Line is the fourth purchase so the amplified attacks start at 39 power; Rampart Discipline (Decrease Damage Taken 42%) is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Suppression | Fortified | Amplify |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Earthen Fortitude | 0 | Damage | enemy | 38 | 44 (+6) | 40 (+2) | 39 (+1) | 39 (+1) |
| Earthen Fortitude | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 32% (+2) | 32% (+2) |
| Terra Spire | 0 | Damage | enemy | 38 | 44 (+6) | 40 (+2) | 39 (+1) | 39 (+1) |
| Terra Spire | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Terra Spire | 2 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Earth Wall | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 39% (+4) |
| Earth Wall | 1 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 39% (+4) | 45% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +6, Increase Damage Given +10%, Decrease Damage Given +10%, Decrease Damage Taken +10% (not jointly attainable)
- Supported rows in kit: 5 (DMG 2, DDG 1, DDT 1, IDG 1)
- Strongest full build by row-weighted total: Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain (raw +17, row-weighted 18)
- Lowest row-weighted node: Burden of Stone (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Fault Line, Rending Strata, Continental Rift, Burden of Stone | DMG +6, DDG +5 |
| 2 | Fault Line, Rending Strata, Continental Rift, Bedrock Stance | DMG +6, IDG +2, DDG +2, DDT +2 |
| 3 | Fault Line, Rending Strata, Burden of Stone, Pressure of Ages | DMG +4, DDG +10 |
| 4 | Fault Line, Rending Strata, Burden of Stone, Bedrock Stance | DMG +3, IDG +2, DDG +5, DDT +2 |
| 5 | Fault Line, Rending Strata, Bedrock Stance, Rampart Discipline | DMG +3, IDG +2, DDG +2, DDT +5 |
| 6 | Fault Line, Rending Strata, Bedrock Stance, Weight Behind the Blow | DMG +3, IDG +5, DDG +2, DDT +2 |
| 7 | Fault Line, Burden of Stone, Pressure of Ages, Bedrock Stance | DMG +2, IDG +2, DDG +10, DDT +2 |
| 8 | Fault Line, Burden of Stone, Bedrock Stance, Rampart Discipline | DMG +1, IDG +2, DDG +5, DDT +5 |
| 9 | Fault Line, Burden of Stone, Bedrock Stance, Weight Behind the Blow | DMG +1, IDG +5, DDG +5, DDT +2 |
| 10 | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain | DMG +1, IDG +4, DDG +2, DDT +10 |
| 11 | Fault Line, Bedrock Stance, Rampart Discipline, Weight Behind the Blow | DMG +1, IDG +5, DDG +2, DDT +5 |
| 12 | Fault Line, Bedrock Stance, Weight Behind the Blow, Landslide Momentum | DMG +1, IDG +10, DDG +2, DDT +4 |
| 13 | Bedrock Stance, Rampart Discipline, Unmoved Mountain, Weight Behind the Blow | IDG +7, DDT +10 |
| 14 | Bedrock Stance, Rampart Discipline, Weight Behind the Blow, Landslide Momentum | IDG +10, DDT +7 |

## Design notes

- Node split: Fault Line raises both Earth damage rows and Fortitude's suppression, forking into Rending Strata → Continental Rift (damage) and Burden of Stone → Pressure of Ages (suppression). Bedrock Stance raises both Earth Wall rows, forking into Rampart Discipline → Unmoved Mountain (fortify) and Weight Behind the Blow → Landslide Momentum (amplify). 2 F / 4 H / 4 A; every capstone 3 BP deep; any two capstones 5–6 BP. Ten nodes because the four tags are four distinct roles.
- Flats scale by coverage. Damage reaches 2 rows (Taiyo Kami: 3), so the route is 1+2+3 = +6 power at the guardrail (38→44 on both attacks). The three single-row percentage tags follow Taiyo's 2+3+5 = +10 shape (DDG 30→40%, DDT 35→45%, IDG 35→45%). Capstone secondaries (+1 Damage, +2 IDG, +2 DDT) stay below the sibling Hidden Art on the same tag. Each example build row-weights 18 (Nature's Blessing 16–18 on five rows; Taiyo Kami examples 20–29, all builds 16–31, on nine).
- Matching (tags.ts getEfficiencyRatio, 3477–3510): the DDT and DDG rows list four stat types and no element, so their tag list includes None and they alter every non-pierce hit whose stat resolves to one of the four or that is element-less (basic attacks and weapons included). Earth Wall's IDG row has no stat types and elements ['Earth'] only, so its tag list is exactly ['Earth']: it amplifies Earth-element damage alone, never basic attacks or non-elemental jutsu.
- Passives: the bloodline's Earth Increase Damage Given passive (15% + 0.15/level, bloodline-sourced, multiplicative) scales every enhanced Earth damage row, so +6 power is worth more than +6 after it. The +10% Lightning Increase Damage Taken passive is the kit's weakness; Earth Wall's DDT row (element-less, four stat types) does reduce Lightning hits while active, so the fortify route softens that weakness for 2 of every 7 rounds without removing it.
- Delivery and uptime: all three jutsu have cooldown 7. Earth Wall is a 40 AP SELF cast (range 0) whose two buffs last 2 rounds from the following round, so both self routes have 2-in-7 uptime per cast. Earthen Fortitude (60 AP, range 4, single target) delivers the hit and the 2-round suppression together; Terra Spire (60 AP, range 4, AOE spiral) delivers Earth damage per target plus unsupported recoil and wound. Potency changes powers and percentages only.
- Fourth purchases: Burst → Bedrock Stance (Wall 37%/37%) or Burden of Stone (suppression 35%; attack-root only, no Earth Wall); Suppression → Bedrock Stance or Rending Strata (attacks 42); Fortified → Fault Line (attacks 39, suppression 32%) or Weight Behind the Blow (amplify 42%); Amplify → Fault Line or Rampart Discipline (DDT 42%). Strongest unadvertised build by row weight: 01,02,04,05 (DDG +10, Damage +4) ties the examples at 18. Lowest-value nodes: the three +3 single-row Hidden Arts.

## Risks and unproven interactions

- Classification: Earth is a basic element carried by 23 other census bloodlines and, unverified, by ordinary jutsu, so the label is the bloodline-keyed extension 'Terra Nova' (resolver change and extension). Under the current resolver an Earth modifier reaches the 3 Earth rows directly and the 2 element-less rows only via None, which also reaches every non-elemental row the player casts.
- Earth-only amplify (open user decision): Earth Wall's IDG row matches Earth damage alone (element list lacks None), so Landslide Momentum's 45% skips basic attacks and non-Earth jutsu. The draft keeps +5 (route +10, symmetric with DDT/DDG) because the scope is narrow; the alternative is +3 (route 2+3+3 = +8), leaving DDT as the only +10 self route and making the declared ordering real.
- Broad self fortification: Unmoved Mountain puts Earth Wall's DDT at 45% for 2 rounds; the row matches every non-pierce hit whose stat resolves to one of the four stat types or that is element-less, so it also blunts Lightning hits against the kit's +10% Lightning weakness. BATTLE_TAG_STACKING is on at the pin, so it stacks with other DDT sources; one cast per 7 rounds limits self-stacking.
- Suppression leakage: Pressure of Ages puts Earthen Fortitude's Decrease Damage Given at 40% for 2 rounds on one target; the debuff reduces that enemy's damage to the caster's allies as well (any stat-based or element-less hit, pierce excluded), so the route is worth more in team battles than one row suggests. It is a single-target 60 AP cast on cooldown 7; the kit has no area suppression.
- Single-cast concentration: both Earth Wall routes raise rows of one 40 AP D-rank self cast (range 0, so no ally receives it), and both attack-root routes share Earthen Fortitude; the per-AP value of Earth Wall rises more than the damage route's. All four capstones depend on one jutsu each, so a prevented or sealed cast removes the whole route's value for that cooldown cycle.
- Terra Spire's recoil and wound rows are unsupported and unchanged. The wound row lacks friendlyFire (treated as ALL), so allies in the spiral already receive it; the caster never does (OTHER_USER area rows reach only living non-caster users: actions.ts 1029-1060, 1226-1248). No node touches it, but the Damage route invites casting Spire into mixed groups. The damage row is friendly fire ENEMIES.
- Highest-stat resolution: both damage rows use statTypes/generalTypes 'Highest', resolved through the caster's highestOffence (gap G16, not verified always defined). Their Earth element matches Earth Wall's amplify regardless, and the element-less DDT/DDG rows match element-less hits through None regardless, but an elemental enemy hit whose 'Highest' fails to resolve would not be blunted.
- Damage is formula-calculated with sqrt stat scaling and is then multiplied by the Earth Increase Damage Given passive and by Earth Wall's amplify when active, so +6 raw power is not linear +6 damage. No combat simulation was performed; main-tree effects, equipment, AP, uptime and modifier delivery are outside this audit.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Terra Nova jutsu inherit Terra Nova potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

