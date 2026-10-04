# Terra Nova — Tectonic Creed

**Bloodline:** Terra Nova (BR-081, rank C, `AohWgMy9uYF14ivDlE-xq`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Earth classification / forked tree · **Classification:** Earth (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Earth strikes (Fault Line): raw Damage on Earthen Fortitude and Terra Spire, or Earthen Fortitude's suppression · secondary Earth Wall's window (Bedrock Stance): Decrease Damage Taken or Earth-only Increase Damage Given · tertiary No riders: each capstone carries one effect. The kit has no Afterburn, Heal, Lifesteal or Reflect rows.

Fault Line answers "How do I make my Earth strikes decide the exchange?": Continental Rift adds raw Damage to both 38 EP Earth attacks (+2, 38 → 40, the only route to the 40 Normal line) and Pressure of Ages takes Earthen Fortitude's suppression to 40%. Bedrock Stance answers "How do I use Earth Wall's two rounds?": Unmoved Mountain holds (Decrease Damage Taken 45%) and Landslide Momentum strikes (Earth-only Increase Damage Given 45%). Raw Damage and the Earth Wall amplify multiply each other, so they sit under different Foundations and Bedrock Stance carries only the wall's guard: the +2 Damage builds carry no Increase Damage Given, the +10% Increase Damage Given builds carry no Damage, and the only mix is +1 Damage with +3%. Continental Rift, a steady edge, owns every cast (40 against 38 EP); Landslide Momentum owns the wall's window (38 × 1.45 = 55.1 against 40 × 1.35 = 54.0). Potency reaches matching supported tags on all Earth jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Fault Line | Foundation | How do I make my Earth strikes decide the exchange: hit harder, or leave the struck enemy weaker? |
| Bedrock Stance | Foundation | How do I use Earth Wall's two rounds: hold behind it, or strike from it? |
| Continental Rift | Advanced Art | steady edge: +2 Damage on every Earth strike (38 → 40) from a +1 commit and a +1 payoff, no setup window |
| Pressure of Ages | Advanced Art | suppression: the struck enemy hits softer for the whole party |
| Unmoved Mountain | Advanced Art | fortress: take less from nearly every hit in the wall's window |
| Landslide Momentum | Advanced Art | sustained amplification: Earth hits timed into the wall's window land hardest |

**Director review recommended:** Roster questions: DQ-D (Rending Strata +1 Damage, the commit of a 1/1 steady-edge route, 38 → 39 → 40).

- Concern: Off-kit flat Damage is unverified: Continental Rift's +2 reaches every Earth Damage row, so an off-kit Earth row at 45 or 50 would read 47 or 52; the validator checks kit rows only.
- Concern: Landslide Momentum's in-window lead over Continental Rift is about 2% on the kit's 38 EP attacks (55.1 against 54.0 EP-equivalent) and widens with base (72.5 against 70.2 on a 50 row); Continental Rift leads 40 to 38 (about 5%) outside the window and on any Earth cast not timed into it. Bedrock Stance no longer lends Continental Rift the amplify, so Landslide plus Fault Line (team suppression) and Landslide plus Rampart Discipline (Decrease Damage Taken 40%) are both real fourths. Not simulated.
- Concern: Hidden-Art flat Damage (DQ-D): Rending Strata's +1 (×1.026) is a small commit rather than a percentage setup, because each of the kit's three percentage tags already has its own route and a setup would copy that route's Hidden Art (design notes). Continental Rift is a steady edge, not burst; its value is uptime, not size: +2 EP (×1.053) on every Earth cast, Light 38 into Normal 40.
- Concern: Defense reads lighter than the anchors: Pressure of Ages and Unmoved Mountain carry no rider, unlike Blood-Enchanted Eyes and Arashima. Kept because the two defensive tags sit on different jutsu under different Foundations, so riders would be cross-family and converge the two defensive builds (0.366 against 0.363). Landslide Momentum's route is likewise a bare single-row +10%, which it needs to own Earth Wall's window; with no Increase Damage Given on Bedrock Stance its capstone carries +7, above the anchors' usual +5.
- Concern: Two of four routes (Pressure of Ages, Unmoved Mountain) amplify element-less rows that the current row-element resolver cannot reach; they depend on the proposed jutsu-classification resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Earth jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Fault Line | Foundation | None | +2% Decrease Damage Given (enemy debuff) | Earthen Fortitude / 1 |
| 02 | Rending Strata | Hidden Art | Fault Line | +1 Damage (damage) | Earthen Fortitude, Terra Spire / 2 |
| 03 | Continental Rift | Advanced Art | Rending Strata | +1 Damage (damage) | Earthen Fortitude, Terra Spire / 2 |
| 04 | Burden of Stone | Hidden Art | Fault Line | +3% Decrease Damage Given (enemy debuff) | Earthen Fortitude / 1 |
| 05 | Pressure of Ages | Advanced Art | Burden of Stone | +5% Decrease Damage Given (enemy debuff) | Earthen Fortitude / 1 |
| 06 | Bedrock Stance | Foundation | None | +2% Decrease Damage Taken (self buff) | Earth Wall / 1 |
| 07 | Rampart Discipline | Hidden Art | Bedrock Stance | +3% Decrease Damage Taken (self buff) | Earth Wall / 1 |
| 08 | Unmoved Mountain | Advanced Art | Rampart Discipline | +5% Decrease Damage Taken (self buff) | Earth Wall / 1 |
| 09 | Weight Behind the Blow | Hidden Art | Bedrock Stance | +3% Increase Damage Given (self buff) | Earth Wall / 1 |
| 10 | Landslide Momentum | Advanced Art | Weight Behind the Blow | +7% Increase Damage Given (self buff) | Earth Wall / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Fault Line** — The ground splits where you choose, and your enemy stands on the wrong side. In the kit, only Earthen Fortitude carries a Decrease Damage Given row: 30 → 32% for the 2 rounds after its hit, on one enemy. The strike family's root carries no Damage, so raw Damage stays on Continental Rift's route.
- **Rending Strata** — Layer by layer, the earth is torn open. Kit examples: Earthen Fortitude (single target) and Terra Spire (spiral around the caster) Damage 38 → 39 EP, still Light. The +1 commit of a steady-edge route: each of the kit's three percentage tags already has its own route, so a percentage setup here would copy another route's Hidden Art.
- **Continental Rift** — When the plates move, nothing built upon them survives. Steady edge: the kit's two Earth Damage rows 38 → 40 EP on the full route (Rending Strata +1, then +1 here), Light into Normal on every cast; no other allocation passes 39. The Earth damage passive multiplies the result.
- **Burden of Stone** — Every swing drags the weight of a quarry behind it. In the kit, only Earthen Fortitude carries this row (one enemy, 2 rounds, 60 AP, cooldown 7): Decrease Damage Given 35% with Fault Line. Terra Spire's recoil is untouched.
- **Pressure of Ages** — What the mountain presses down stays pressed down. Suppression: Earthen Fortitude Decrease Damage Given 30 → 40% on the full route, live the 2 rounds after its hit. One effect, no rider.
- **Bedrock Stance** — Plant your feet where the stone runs deepest. In the kit, only Earth Wall carries a Decrease Damage Taken row (40 AP self cast, range 0, cooldown 7, 2 rounds): 35 → 37%. The wall's Earth amplify sits wholly on the strike branch, so a build that buys Bedrock Stance as its fourth gains guard, not amplify.
- **Rampart Discipline** — A wall is only as patient as the one who raised it. In the kit, only Earth Wall carries a Decrease Damage Taken row (self, 2 rounds): 40% with Bedrock Stance. No element, four stat types: most non-pierce hits.
- **Unmoved Mountain** — Storms wear themselves out against it, and the mountain does not notice. Fortress: Earth Wall Decrease Damage Taken 35 → 45% on the full route, for the 2 rounds after its cast. One effect; Earth Wall's Earth amplify stays at its 35% base.
- **Weight Behind the Blow** — The strike carries the whole hillside with it. In the kit, only Earth Wall carries an Increase Damage Given row (self, 2 rounds): 35 → 38%, on Earth-element hits only; no stat filter. Bedrock Stance adds none, so the whole amplify is on this branch.
- **Landslide Momentum** — Once the slope begins to move, it does not stop for anyone. Sustained amplification: Earth Wall Increase Damage Given 35 → 45% on Earth hits on the full route (+3, then +7 here), for the 2 rounds after its cast (×1.45 / 1.35 ≈ ×1.074 over the unbought wall). In the window a 38 EP attack lands at 55.1 EP-equivalent, ahead of Continental Rift's 40 × 1.35 = 54.0 with any fourth.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT |
|---|---|---:|---:|---:|---:|
| Continental Rift (Steady edge) | Fault Line, Rending Strata, Continental Rift, Bedrock Stance | +2 | — | +2% | +2% |
| Pressure of Ages (Suppression) | Fault Line, Burden of Stone, Pressure of Ages, Bedrock Stance | — | — | +10% | +2% |
| Unmoved Mountain (Fortress) | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain | — | — | +2% | +10% |
| Landslide Momentum (Amplify) | Bedrock Stance, Rampart Discipline, Weight Behind the Blow, Landslide Momentum | — | +10% | — | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Continental Rift:** Both Earth attacks 38 → 40 EP on every cast with no setup window (Terra Spire on each enemy in its spiral), before the Earth damage passive multiplies them; Fault Line leaves Earthen Fortitude's suppression at 32%. Bedrock Stance, the fourth shown, adds Earth Wall Decrease Damage Taken 37%, guard rather than amplify, so a 40 EP strike in the wall's window lands at 40 × 1.35 = 54.0 against Landslide Momentum's 55.1; outside the window Continental Rift leads 40 to 38. Burden of Stone (suppression 35%) is the equally realistic strike-only fourth.
- **Pressure of Ages:** Earthen Fortitude as a control cast: the target's damage is cut by 40% (30% base) on the two rounds after the hit, against the caster and allies alike for any stat-based or element-less hit, pierce excluded. Bedrock Stance is the fourth purchase: Earth Wall Decrease Damage Taken 37%. Against the struck enemy that is 0.60 × 0.63 = 0.378 of its damage, slightly more than Unmoved Mountain plus Fault Line's 0.374; the case is the party, whose damage taken from that enemy the debuff also cuts. Rending Strata (attacks 39 EP) is the alternative.
- **Unmoved Mountain:** Earth Wall Decrease Damage Taken 45% (35% base) on the two rounds after its cast, against every non-pierce hit whose stat resolves to one of the four stat types or that carries no element, Lightning included despite the bloodline's +10% Lightning weakness; the Earth amplify stays at its 35% base. Fault Line is the fourth purchase (suppression 32%; 0.68 × 0.55 = 0.374 of the struck enemy's damage, 0.55 of anyone else's); Weight Behind the Blow (Earth amplify 38%) is the offensive alternative.
- **Landslide Momentum:** Earth Wall Increase Damage Given 45% (35% base) on the two rounds after its cast, on Earth-element damage only: both kit attacks and any Earth normal jutsu, not basic attacks or non-Earth jutsu. All three kit jutsu share cooldown 7, so timing both attacks into the window is the route's skill test: there a 38 EP attack lands at 38 × 1.45 = 55.1, ahead of Continental Rift with any fourth (40 × 1.35 = 54.0); outside the window Continental Rift leads 40 to 38. Rampart Discipline is the fourth purchase (Decrease Damage Taken 40% on the same cast); Fault Line (suppression 32%, which also protects the party) is the team alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Steady edge | Suppression | Fortress | Amplify |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Earthen Fortitude | 0 | Damage | enemy | 38 | 40 (+2) | 38 | 38 | 38 |
| Earthen Fortitude | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 32% (+2) | 30% |
| Terra Spire | 0 | Damage | enemy | 38 | 40 (+2) | 38 | 38 | 38 |
| Terra Spire | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Terra Spire | 2 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Earth Wall | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 40% (+5) |
| Earth Wall | 1 | Increase Damage Given | self | 35% | 35% | 35% | 35% | 45% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Continental Rift: +2 Damage (0 + 1 + 1; off band)
  - Route Pressure of Ages: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Unmoved Mountain: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Landslide Momentum: +10% Increase Damage Given (0 + 3 + 7; on band)
- Supported rows in kit: 5 (DMG 2, DDG 1, DDT 1, IDG 1)
- Strongest full build by row-weighted total: Bedrock Stance, Rampart Discipline, Weight Behind the Blow, Landslide Momentum (raw +15, row-weighted 15)
- Lowest row-weighted node: Fault Line (2)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +1 Damage | +2 Damage |
|---|---:|---|---|---|
| Earthen Fortitude | 0 | 38 (Light) | 39 (Light) | 40 (Normal) ↑ |
| Terra Spire | 0 | 38 (Light) | 39 (Light) | 40 (Normal) ↑ |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Continental Rift | +2 Damage, +2% DDG | Burden of Stone *(highest diagnostic)* | +2 Damage, +5% DDG | 9 |
| Continental Rift | +2 Damage, +2% DDG | Bedrock Stance | +2 Damage, +2% DDG, +2% DDT | 8 |
| Pressure of Ages | +10% DDG | Rending Strata | +1 Damage, +10% DDG | 12 |
| Pressure of Ages | +10% DDG | Bedrock Stance *(highest diagnostic)* | +10% DDG, +2% DDT | 12 |
| Unmoved Mountain | +10% DDT | Fault Line | +2% DDG, +10% DDT | 12 |
| Unmoved Mountain | +10% DDT | Weight Behind the Blow *(highest diagnostic)* | +3% IDG, +10% DDT | 13 |
| Landslide Momentum | +10% IDG, +2% DDT | Fault Line | +10% IDG, +2% DDG, +2% DDT | 14 |
| Landslide Momentum | +10% IDG, +2% DDT | Rampart Discipline *(highest diagnostic)* | +10% IDG, +5% DDT | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Fault Line, Rending Strata, Continental Rift, Burden of Stone | +2 Damage, +5% DDG |
| 2 | Fault Line, Rending Strata, Continental Rift, Bedrock Stance | +2 Damage, +2% DDG, +2% DDT |
| 3 | Fault Line, Rending Strata, Burden of Stone, Pressure of Ages | +1 Damage, +10% DDG |
| 4 | Fault Line, Rending Strata, Burden of Stone, Bedrock Stance | +1 Damage, +5% DDG, +2% DDT |
| 5 | Fault Line, Rending Strata, Bedrock Stance, Rampart Discipline | +1 Damage, +2% DDG, +5% DDT |
| 6 | Fault Line, Rending Strata, Bedrock Stance, Weight Behind the Blow | +1 Damage, +3% IDG, +2% DDG, +2% DDT |
| 7 | Fault Line, Burden of Stone, Pressure of Ages, Bedrock Stance | +10% DDG, +2% DDT |
| 8 | Fault Line, Burden of Stone, Bedrock Stance, Rampart Discipline | +5% DDG, +5% DDT |
| 9 | Fault Line, Burden of Stone, Bedrock Stance, Weight Behind the Blow | +3% IDG, +5% DDG, +2% DDT |
| 10 | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain | +2% DDG, +10% DDT |
| 11 | Fault Line, Bedrock Stance, Rampart Discipline, Weight Behind the Blow | +3% IDG, +2% DDG, +5% DDT |
| 12 | Fault Line, Bedrock Stance, Weight Behind the Blow, Landslide Momentum | +10% IDG, +2% DDG, +2% DDT |
| 13 | Bedrock Stance, Rampart Discipline, Unmoved Mountain, Weight Behind the Blow | +3% IDG, +10% DDT |
| 14 | Bedrock Stance, Rampart Discipline, Weight Behind the Blow, Landslide Momentum | +10% IDG, +5% DDT |

## Design notes

- Structure kept: Fault Line (Earthen Fortitude's suppression) forks into Rending Strata → Continental Rift (steady edge) and Burden of Stone → Pressure of Ages (suppression); Bedrock Stance (Earth Wall's guard) forks into Rampart Discipline → Unmoved Mountain (fortress) and Weight Behind the Blow → Landslide Momentum (amplification). 2 F / 4 H / 4 A; every capstone 3 BP deep; any two capstones cost 5–6 BP. An offense/defense split (Damage with Increase Damage Given, Decrease Damage Taken with Decrease Damage Given) was considered and rejected: raw Damage and the Earth Wall amplify multiply each other, so one Foundation would let a capstone plus its sibling Hidden Art stack both.
- 2026-10-04 rebalance: the pre-batch Burst route is cut from +5 Damage (Rending Strata +2, Continental Rift +3; 38 → 43 on both attacks, one an area spiral) to +2 (Rending Strata +1, Continental Rift +1; 38 → 39 → 40), so the Hidden Art no longer crosses the 40 Normal line and Landslide Momentum owns the wall's window (calibration below). Pressure of Ages' +1 Damage rider is removed, so no build outside Continental Rift passes 39 EP; an interim +2% Decrease Damage Taken rider was also dropped, because with Bedrock Stance it let suppression beat the fortress at its own job (0.60 × 0.61 = 0.366 of the struck enemy's damage against Unmoved Mountain plus Fault Line's 0.374). Unmoved Mountain's +2% Increase Damage Given and Landslide Momentum's +2% Decrease Damage Taken riders are removed: each fed its sibling Hidden Art's tag on the same Earth Wall cast, so both capstones' best fourth purchase converged on the same all-Earth-Wall package (45%/42% against 42%/45%). Final review: Bedrock Stance's +2% Increase Damage Given moved to Landslide Momentum (+5 → +7), so the route still totals +10% but Continental Rift's realistic fourth no longer borrows the wall amplify. In the window Continental Rift plus Bedrock Stance drops from 40 × 1.37 = 54.8 to 40 × 1.35 = 54.0 against Landslide's 55.1 (a 2% edge, not 0.5%), so Landslide plus Fault Line is a real fourth rather than near-dominated by it. Unmoved Mountain plus Weight Behind the Blow now borrows +3% (amplify 38%, guard 45%) rather than +5%, against Landslide plus Rampart Discipline's amplify 45%, guard 40%. The capstone, not Weight Behind the Blow, takes the moved +2%, so both Hidden Arts stay at +3.
- Calibration (uptime-aware): Continental Rift's +2 EP is ×40 / 38 ≈ ×1.053 on every Earth cast, in or out of the window. Landslide Momentum's +10% is ×1.45 / 1.35 ≈ ×1.074 on Earth hits in Earth Wall's two-round window only. Bedrock Stance lends no amplify, so inside the window Continental Rift with any fourth gives (B + 2) × 1.35 against Landslide Momentum's 1.45B; break-even is B = 27 EP, so Landslide Momentum leads on every player-tier row (38: 54.0 against 55.1, about 2%; 50: 70.2 against 72.5, about 3%) and Continental Rift leads everywhere else (40 against 38, about 5%). With Bedrock Stance's former +2% the gap was 54.8 against 55.1 (0.5%); with an earlier +3 Damage as well, the route out-hit Landslide Momentum inside its own window up to B ≈ 51.4 EP. Defense: Unmoved Mountain's 45% is ×0.55 / 0.65 ≈ ×0.85 damage taken in the window; Pressure of Ages' 40% is ×0.60 / 0.70 ≈ ×0.86 on one enemy's hits for two rounds. With both windows aligned (Earth Wall 40 AP plus Earthen Fortitude 60 AP fit in one round), Unmoved plus Fault Line takes 0.68 × 0.55 = 0.374 of the struck enemy's damage against Pressure plus Bedrock Stance's 0.60 × 0.63 = 0.378, and 0.55 against 0.63 from anyone else.
- Rending Strata keeps a +1 Damage commit (38 → 39, Light), splitting the Light-row +2 as +1 / +1 (a steady edge, not burst) instead of the director pattern's percentage setup, because every percentage setup here would copy another route's Hidden Art: Increase Damage Given repeats Weight Behind the Blow on Earth Wall's row and re-merges the multiplying pair this tree keeps apart (+2% would restore the 40 × 1.37 = 54.8 near-tie in Landslide Momentum's window, +3% passes its 55.1 at 55.2); Decrease Damage Given repeats its sibling Burden of Stone, pushes Pressure of Ages plus Rending Strata past +10% and becomes Pressure's best fourth; Decrease Damage Taken repeats Rampart Discipline and fits neither half of Fault Line's sentence. The kit has no fifth supported tag.
- Matching (tags.ts getEfficiencyRatio 3477–3510): the Decrease Damage Taken and Decrease Damage Given rows list four stat types and no element, so they alter every non-pierce hit whose stat resolves to one of the four or that is element-less (basic attacks and weapons included). Earth Wall's Increase Damage Given row has elements ['Earth'] and no stat type: it amplifies Earth-element damage only.
- Delivery: all three jutsu have cooldown 7. Earth Wall (40 AP, SELF) buffs are live on the two rounds after its cast (§3b), never in it: 2-in-7 uptime for both wall routes, though both kit attacks share cooldown 7 and can be timed into the window each cycle. Earthen Fortitude (60 AP, range 4, single target) hits in its cast round and suppresses on the two rounds after. Terra Spire (60 AP) hits enemies on a radius-4 spiral around the caster. The Earth damage passive (15% + 0.15/level, fromType bloodline) multiplies last; the +10% Lightning Increase Damage Taken passive is the kit's weakness. Both passives are suppressed in ranked modes (§5).
- One effect per capstone. The anchors give their defensive capstones riders, but there both defensive tags sit under one Foundation; here Decrease Damage Given (Earthen Fortitude, Fault Line) and Decrease Damage Taken (Earth Wall, Bedrock Stance) sit under different ones, so mirrored riders would be cross-family and pull the two defensive 4-BP builds together (Pressure plus Bedrock Stance 0.60 × 0.61 = 0.366, Unmoved plus Fault Line 0.66 × 0.55 = 0.363). Landslide Momentum's route stays a bare +10% (Weight Behind the Blow +3, Landslide Momentum +7): at +8% (38 × 1.43 = 54.3) its in-window lead over Continental Rift (54.0) would shrink to about 0.6%, and each possible rider fails: Damage re-merges the multiplying pair, Decrease Damage Taken feeds Rampart Discipline on the same cast, and Decrease Damage Given is Fault Line's cross-family tag.
- Fourth purchases: Steady edge → Bedrock Stance (Decrease Damage Taken 37%, no amplify; 54.0 in the window) or Burden of Stone (suppression 35%); Suppression → Bedrock Stance (Decrease Damage Taken 37%) or Rending Strata (39 EP); Fortress → Fault Line (suppression 32%) or Weight Behind the Blow (amplify 38%); Amplification → Rampart Discipline (Decrease Damage Taken 40%) or Fault Line (suppression 32%).

## Risks and unproven interactions

- Classification: Earth is shared with other bloodlines (expected under RUL-2026-10-03-005). 3 of 5 supported kit rows carry Earth; Earthen Fortitude's Decrease Damage Given and Earth Wall's Decrease Damage Taken rows carry no element and need the proposed jutsu-classification resolver, so two of the four routes depend on it. Off-kit Earth coverage is unverified.
- Off-kit flat Damage: Continental Rift's +2 reaches every Earth Damage row, not only the kit's two 38 EP rows. An off-kit Earth row at 45 or 50 would read 47 or 52; the validator enumerates kit rows only.
- Earth-only amplify: Earth Wall's Increase Damage Given row matches Earth damage alone (its element list lacks None), so Landslide Momentum's 45% skips basic attacks and non-Earth jutsu, and its value depends on landing Earth hits in the two-round window.
- Broad fortification: Unmoved Mountain puts Earth Wall's Decrease Damage Taken at 45% for 2 rounds, matching every non-pierce hit whose stat is one of the four or that is element-less, Lightning included. Same-tag effects all apply (process.ts 1109–1117), so it compounds with any other Decrease Damage Taken on the caster. Cooldown 7 exceeds the 2 rounds, so own casts never overlap.
- Suppression reach: Pressure of Ages puts Earthen Fortitude's Decrease Damage Given at 40% for 2 rounds on one target; the debuff also reduces that enemy's damage to the caster's allies, so the route is worth more in team battles than one row suggests. It is a single-target 60 AP cast on cooldown 7; the kit has no area suppression.
- Single-cast concentration: each capstone depends on one jutsu (Earth Wall for the wall routes, Earthen Fortitude for suppression, both attacks for the steady edge), so a prevented or sealed cast removes the route's value for that cooldown cycle.
- Terra Spire's recoil and wound rows are unsupported. The wound row lacks friendlyFire (= ALL), so allies inside the caster-centred spiral receive the wound and the caster never does (actions.ts 1029–1060). No node touches it, but Continental Rift's route invites casting Spire near allies.
- Highest-stat resolution (§4b): both damage rows list statTypes 'Highest', resolved from the caster's highestOffence, so enemy Decrease Damage Taken buffs and Decrease Damage Given debuffs with four-stat filters match and blunt the boosted hits.
- Formula damage scales linearly with EP (tags.ts powerEffect 1436–1462), so +2 EP is ×1.053 on a 38 EP row before Earth Wall's amplify and the Earth passive multiply it. No combat simulation was performed; main-tree effects, equipment, AP, uptime and modifier delivery are outside this audit.

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

