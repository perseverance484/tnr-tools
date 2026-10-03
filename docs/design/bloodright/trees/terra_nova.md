# Terra Nova — Tectonic Creed

**Bloodline:** Terra Nova (BR-081, rank C, `AohWgMy9uYF14ivDlE-xq`) · **Revision:** Draft 4 / Earth classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Earth (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (Earth attacks: Earthen Fortitude, Terra Spire) · secondary Decrease Damage Taken (Earth Wall fortification) · tertiary Decrease Damage Given (Earthen Fortitude suppression) and Increase Damage Given (Earth Wall, Earth hits only).

Two of the five supported rows are Earth damage at 38 EP (Earthen Fortitude single target, Terra Spire AOE spiral), so the kit's declared role is an Earth bruiser and Damage is primary. Earth Wall (40 AP self cast) carries the only two self buffs: its Decrease Damage Taken row lists all four stat types and no element, so it blunts nearly every non-pierce hit, while its Increase Damage Given row is Earth-only and amplifies Earth damage alone, so fortification outranks amplification in breadth, not in flats. Earthen Fortitude's 30% Decrease Damage Given rides on the single-target hit and is the kit's only supported enemy debuff (Terra Spire's recoil and wound are enemy debuffs outside potency). The three single-row percentage routes all land on +10%; no Afterburn, heal, lifesteal or reflect route is invented. Potency reaches matching supported tags on all Earth jutsu (RUL-2026-10-03-005).

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Earth jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Fault Line | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Earthen Fortitude / 1 |
| 02 | Rending Strata | Hidden Art | Fault Line | +2 Damage (damage) | Earthen Fortitude, Terra Spire / 2 |
| 03 | Continental Rift | Advanced Art | Rending Strata | +3 Damage (damage) | Earthen Fortitude, Terra Spire / 2 |
| 04 | Burden of Stone | Hidden Art | Fault Line | +3% Decrease Damage Given (enemy debuff) | Earthen Fortitude / 1 |
| 05 | Pressure of Ages | Advanced Art | Burden of Stone | +5% Decrease Damage Given (enemy debuff); +1 Damage (damage) | Earthen Fortitude, Terra Spire / 3 |
| 06 | Bedrock Stance | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Earth Wall / 2 |
| 07 | Rampart Discipline | Hidden Art | Bedrock Stance | +3% Decrease Damage Taken (self buff) | Earth Wall / 1 |
| 08 | Unmoved Mountain | Advanced Art | Rampart Discipline | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Earth Wall / 2 |
| 09 | Weight Behind the Blow | Hidden Art | Bedrock Stance | +3% Increase Damage Given (self buff) | Earth Wall / 1 |
| 10 | Landslide Momentum | Advanced Art | Weight Behind the Blow | +5% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Earth Wall / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Fault Line** — The ground splits where you choose, and your enemy stands on the wrong side. Earthen Fortitude's Decrease Damage Given 30 → 32% for the 2 rounds after its hit, on one enemy. No Damage on the root, so the Damage route stays at +5.
- **Rending Strata** — Layer by layer, the earth is torn open. Both Earth Damage rows (Earthen Fortitude single target, Terra Spire AOE spiral) 38 → 40 EP. Range 4, 60 AP, cooldown 7.
- **Continental Rift** — When the plates move, nothing built upon them survives. The same two Earth Damage rows: 38 → 43 EP on the full route (+5 Damage), then the Earth damage passive multiplies the result.
- **Burden of Stone** — Every swing drags the weight of a quarry behind it. Earthen Fortitude Decrease Damage Given only (one enemy row, 2 rounds, 60 AP, cooldown 7): 35% with Fault Line. Spire's recoil untouched.
- **Pressure of Ages** — What the mountain presses down stays pressed down. Suppression route total +10%: Fortitude 30 → 40%, live the 2 rounds after its hit; both Earth Damage rows +1 (39 EP).
- **Bedrock Stance** — Plant your feet where the stone runs deepest. Earth Wall only (40 AP self cast, range 0, cooldown 7, 2 rounds): Decrease Damage Taken 35 → 37%; Increase Damage Given 35 → 37% on Earth hits only.
- **Rampart Discipline** — A wall is only as patient as the one who raised it. Earth Wall Decrease Damage Taken (one self row, 2 rounds): 40% with Bedrock Stance. No element, four stat types: most non-pierce hits.
- **Unmoved Mountain** — Storms wear themselves out against it, and the mountain does not notice. Fortified route total +10%: Earth Wall Decrease Damage Taken 35 → 45%; Increase Damage Given +2% (39% with Bedrock Stance, Earth hits only).
- **Weight Behind the Blow** — The strike carries the whole hillside with it. Earth Wall Increase Damage Given only (one self row, 2 rounds): 40% with Bedrock Stance. Earth-element hits only; no stat filter.
- **Landslide Momentum** — Once the slope begins to move, it does not stop for anyone. Amplify route total +10%: Earth Wall Increase Damage Given 35 → 45% on Earth hits; Decrease Damage Taken +2% (39% with Bedrock Stance). 40 AP cast.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT |
|---|---|---:|---:|---:|---:|
| Continental Rift (Burst) | Fault Line, Rending Strata, Continental Rift, Bedrock Stance | +5 | +2% | +2% | +2% |
| Pressure of Ages (Suppression) | Fault Line, Burden of Stone, Pressure of Ages, Bedrock Stance | +1 | +2% | +10% | +2% |
| Unmoved Mountain (Fortified) | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain | — | +4% | +2% | +10% |
| Landslide Momentum (Amplify) | Fault Line, Bedrock Stance, Weight Behind the Blow, Landslide Momentum | — | +10% | +2% | +4% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Continental Rift:** +5 Damage on both Earth attacks (Earthen Fortitude and Terra Spire 38 → 43 EP, applied per target inside the spiral, before the bloodline's Earth damage passive multiplies them) with Fault Line's 32% suppression. Bedrock Stance is the fourth purchase so Earth Wall gives 37% Decrease Damage Taken and 37% Earth amplify on the two rounds after its cast; Burden of Stone (suppression 35%) is the attack-root-only alternative (no Earth Wall purchase).
- **Pressure of Ages:** Earthen Fortitude as a control cast: one 60 AP hit at 39 EP, then the target's damage is cut by 40% (30% base) on the two rounds after the hit, against the caster and allies alike for any stat-based or element-less hit, pierce excluded. Terra Spire sits at 39 EP. Bedrock Stance is the fourth purchase for Earth Wall at 37%/37%; Rending Strata (attacks 41 EP) is the sharper alternative.
- **Unmoved Mountain:** Earth Wall as the centrepiece: Decrease Damage Taken 45% (35% base) on the two rounds after its cast, against every non-pierce hit whose stat resolves to one of the four stat types or that carries no element, Lightning included despite the bloodline's +10% Lightning weakness, with the Earth amplify at 39%. Fault Line is the fourth purchase (suppression 32%); Weight Behind the Blow (Earth amplify 42%) is the offensive alternative.
- **Landslide Momentum:** Earth Wall as a springboard: Increase Damage Given 45% (35% base) on the two rounds after its cast, on Earth-element damage only, which covers both bloodline attacks and any Earth normal jutsu but not basic attacks or non-Earth jutsu, with Decrease Damage Taken at 39%. Fault Line is the fourth purchase (suppression 32%); Rampart Discipline (Decrease Damage Taken 42%) is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Suppression | Fortified | Amplify |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Earthen Fortitude | 0 | Damage | enemy | 38 | 43 (+5) | 39 (+1) | 38 | 38 |
| Earthen Fortitude | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 32% (+2) | 32% (+2) |
| Terra Spire | 0 | Damage | enemy | 38 | 43 (+5) | 39 (+1) | 38 | 38 |
| Terra Spire | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Terra Spire | 2 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Earth Wall | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 39% (+4) |
| Earth Wall | 1 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 39% (+4) | 45% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Continental Rift: +5 Damage (0 + 2 + 3; on band)
  - Route Pressure of Ages: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Unmoved Mountain: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Landslide Momentum: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 5 (DMG 2, DDG 1, DDT 1, IDG 1)
- Strongest full build by row-weighted total: Bedrock Stance, Rampart Discipline, Unmoved Mountain, Weight Behind the Blow (raw +17, row-weighted 17)
- Lowest row-weighted node: Fault Line (2)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Fault Line, Rending Strata, Continental Rift, Burden of Stone | +5 Damage, +5% DDG |
| 2 | Fault Line, Rending Strata, Continental Rift, Bedrock Stance | +5 Damage, +2% IDG, +2% DDG, +2% DDT |
| 3 | Fault Line, Rending Strata, Burden of Stone, Pressure of Ages | +3 Damage, +10% DDG |
| 4 | Fault Line, Rending Strata, Burden of Stone, Bedrock Stance | +2 Damage, +2% IDG, +5% DDG, +2% DDT |
| 5 | Fault Line, Rending Strata, Bedrock Stance, Rampart Discipline | +2 Damage, +2% IDG, +2% DDG, +5% DDT |
| 6 | Fault Line, Rending Strata, Bedrock Stance, Weight Behind the Blow | +2 Damage, +5% IDG, +2% DDG, +2% DDT |
| 7 | Fault Line, Burden of Stone, Pressure of Ages, Bedrock Stance | +1 Damage, +2% IDG, +10% DDG, +2% DDT |
| 8 | Fault Line, Burden of Stone, Bedrock Stance, Rampart Discipline | +2% IDG, +5% DDG, +5% DDT |
| 9 | Fault Line, Burden of Stone, Bedrock Stance, Weight Behind the Blow | +5% IDG, +5% DDG, +2% DDT |
| 10 | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain | +4% IDG, +2% DDG, +10% DDT |
| 11 | Fault Line, Bedrock Stance, Rampart Discipline, Weight Behind the Blow | +5% IDG, +2% DDG, +5% DDT |
| 12 | Fault Line, Bedrock Stance, Weight Behind the Blow, Landslide Momentum | +10% IDG, +2% DDG, +4% DDT |
| 13 | Bedrock Stance, Rampart Discipline, Unmoved Mountain, Weight Behind the Blow | +7% IDG, +10% DDT |
| 14 | Bedrock Stance, Rampart Discipline, Weight Behind the Blow, Landslide Momentum | +10% IDG, +7% DDT |

## Design notes

- Node split: Fault Line raises Earthen Fortitude's suppression and forks into Rending Strata → Continental Rift (Damage) and Burden of Stone → Pressure of Ages (suppression). Bedrock Stance raises both Earth Wall rows, forking into Rampart Discipline → Unmoved Mountain (fortify) and Weight Behind the Blow → Landslide Momentum (amplify). 2 F / 4 H / 4 A; every capstone 3 BP deep; any two capstones 5–6 BP. Ten nodes because the four tags are four distinct roles.
- Routes: Burst +5 Damage (Rending Strata +2, Continental Rift +3; 38 → 43 EP); Suppression +10% Decrease Damage Given (Fault Line +2%, Burden of Stone +3%, Pressure of Ages +5%; 30 → 40%); Fortified +10% Decrease Damage Taken and Amplify +10% Increase Damage Given (Bedrock Stance +2%, Hidden Art +3%, capstone +5%; 35 → 45%), all in Taiyo Kami's shapes. Recalibration: Fault Line's former +1 Damage is removed so no legal allocation exceeds +5 Damage; it stays single-tag because Earth Wall's two tags already reach +10% on their own routes. Capstone secondaries (+1 Damage, +2% IDG, +2% DDT) stay below each sibling Hidden Art.
- Matching (tags.ts getEfficiencyRatio, 3477–3510): the DDT and DDG rows list four stat types and no element, so their tag list includes None and they alter every non-pierce hit whose stat resolves to one of the four or that is element-less (basic attacks and weapons included). Earth Wall's IDG row has no stat types and elements ['Earth'] only, so its tag list is exactly ['Earth']: it amplifies Earth-element damage alone, never basic attacks or non-elemental jutsu.
- Passives: the bloodline's Earth Increase Damage Given passive (15% + 0.15/level, fromType bloodline) multiplies every enhanced Earth damage row, so +5 EP is worth more than +5 after it. The +10% Lightning Increase Damage Taken passive is the kit's weakness; Earth Wall's DDT row (element-less, four stat types) also reduces Lightning hits on the two rounds after its cast, softening that weakness for 2 of every 7 rounds. Both passives are suppressed in ranked modes (§5).
- Delivery and uptime: all three jutsu have cooldown 7. Earth Wall's (40 AP, SELF target) buffs are live on the two rounds after its cast round (§3b), never in it: 2-in-7 uptime for both self routes. Earthen Fortitude (60 AP, range 4, single target) lands its hit in the cast round and its suppression on the two rounds after. Terra Spire (60 AP) hits enemies on a radius-4 spiral around the caster with Earth damage and unsupported recoil; its wound also reaches allies. Potency changes values only.
- Fourth purchases: Burst → Bedrock Stance (Wall 37%/37%) or Burden of Stone (suppression 35%; attack-root only, no Earth Wall); Suppression → Bedrock Stance or Rending Strata (attacks 41 EP); Fortified → Fault Line (suppression 32%) or Weight Behind the Blow (amplify 42%); Amplify → Fault Line or Rampart Discipline (DDT 42%). All 14 legal full builds are non-dominated and every node is in one. Lowest-value nodes: Fault Line and the three +3% single-row Hidden Arts.

## Risks and unproven interactions

- Classification: Earth is shared with other bloodlines (expected under RUL-2026-10-03-005). 3 of 5 supported kit rows carry Earth; Earthen Fortitude's Decrease Damage Given and Earth Wall's Decrease Damage Taken rows carry no element and need the proposed jutsu-classification resolver. Off-kit Earth coverage is unverified.
- Earth-only amplify: Earth Wall's IDG row matches Earth damage alone (its element list lacks None), so Landslide Momentum's 45% skips basic attacks and non-Earth jutsu; the Amplify route is narrower than its +10% suggests.
- Broad fortification: Unmoved Mountain puts Earth Wall's DDT at 45% for 2 rounds, matching every non-pierce hit whose stat is one of the four or that is element-less, Lightning included. Same-tag effects all apply (process.ts 1109–1117), so it stacks with any other DDT on the caster. Cooldown 7 exceeds the 2 rounds, so own casts never overlap.
- Suppression reach: Pressure of Ages puts Earthen Fortitude's Decrease Damage Given at 40% for 2 rounds on one target; the debuff reduces that enemy's damage to the caster's allies as well (any stat-based or element-less hit, pierce excluded), so the route is worth more in team battles than one row suggests. It is a single-target 60 AP cast on cooldown 7; the kit has no area suppression.
- Single-cast concentration: both Earth Wall routes raise rows of one 40 AP D-rank SELF-target cast (only the caster receives them), and both attack-root routes share Earthen Fortitude; Earth Wall's per-AP value rises more than the damage route's. All four capstones depend on one jutsu each, so a prevented or sealed cast removes the route's value for that cooldown cycle.
- Terra Spire's recoil and wound rows are unsupported. The spiral is centred on the caster (radius 4, own tile removed; §3b); the wound row lacks friendlyFire (= ALL), so allies within it receive the wound and the caster never does (OTHER_USER area rows reach only living non-caster users: actions.ts 1029–1060, 1226–1248). No node touches it, but the Damage route invites casting Spire near allies.
- Highest-stat resolution (§4b, G16): both damage rows list statTypes 'Highest', resolved from the caster's highestOffence, a required BattleUserState field (types.ts 156), so enemy DDT buffs and DDG debuffs with four-stat filters match and blunt the boosted hits. Their Earth element is what matches Earth Wall's amplify; only an elemental hit with no stat type escapes the four-stat DDT/DDG rows.
- Damage is formula-calculated with sqrt stat scaling, then the Earth passive multiplies it and Earth Wall's amplify (live from an earlier cast) raises it further, so +5 EP is not a linear +5 damage. No combat simulation was performed; main-tree effects, equipment, AP, uptime and modifier delivery are outside this audit.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Earth jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

