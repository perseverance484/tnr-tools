# Sands of Time — Dominion of Hours

**Bloodline:** Sands of Time (BR-059, rank H, `yzbSbZ5rqRVIjiwN-farx`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Sand classification / forked tree · **Classification:** Sand (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Control — Increase Damage Taken (Timeshift, Momentum Shift; two enemy rows) and Decrease Damage Given (Timelapse circle) · secondary Tank — Decrease Damage Taken (Timelapse self row) and Heal (Cellular Regeneration) · tertiary Self-amplification — Momentum Shift's self Increase Damage Given (one row) on the caster's own hits against every target in its window; Sand Damage (Timeshift 40, Timelapse 40, Eternity Flux 50) is left unamplified.

Sands of Time is a rank H Tank / Control kit built from paired rows: Momentum Shift marks the target (35% Increase Damage Taken) and buffs the caster (35% Increase Damage Given); Timelapse weakens every enemy in its circle (30% Decrease Damage Given) and shields the caster (30% Decrease Damage Taken). Timeshift adds a second, broad 35% exposure row and Cellular Regeneration a static Heal 25 (250 HP per tick). The tree follows those pairs: an offensive Foundation on Momentum Shift (strike harder myself or age the target) and a defensive Foundation on Timelapse (shelter myself or weaken them). Routes: Sustained amplification +10% Increase Damage Given on Momentum Shift's self row, Exposure +8% Increase Damage Taken, Fortress +10% Decrease Damage Taken with +5% Heal, Suppression +10% Decrease Damage Given. Damage stays unamplified: the Traits are Tank and Control, and the 50 row is Eternity Flux's, a C-rank stun cast (60 AP, cooldown 7), not a signature finisher. Stun, timecompression and barrier are unsupported and receive nothing.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Borrowed Hours | Foundation | How do I turn time into damage: quicken my own hand or age my target? |
| Suspended Moment | Foundation | How do I hold back the hour: shelter myself or slow the hands raised against us? |
| Sovereign of the Hour | Advanced Art | sustained amplification: the caster's own hits on every target in Momentum Shift's window (pure Increase Damage Given, not burst) |
| The Inevitable Hour | Advanced Art | exposure: one marked target takes more from everyone |
| Timeless Bastion | Advanced Art | fortress: endure and recover |
| Stilled Hourglass | Advanced Art | suppression: blunt every enemy in the circle |

**Director review recommended:** Roster questions: DQ-B (The Inevitable Hour +8% Increase Damage Taken on two rows, ×1.122).

- Concern: Damage is unamplified (Traits Tank, Control; Eternity Flux's 50 row is a C-rank, 60 AP stun cast, not a signature finisher), so Sovereign of the Hour is a bare +10% on one self row (2/3/5, ×1.074). Shakunetsu Sakura's single-row +10% routes also carry a +5% Heal or +3% Decrease Damage Given rider; a rider here would borrow a defensive route's tag (Heal, Decrease Damage Taken or Given).
- Concern: The Inevitable Hour's +8% Increase Damage Taken on two compounding, team-wide rows is ×1.122, just above Blood-Enchanted Eyes' exposure maximum (×1.115) and above Shakunetsu Sakura's ×1.075. It is the kit's primary Control identity and should be ruled with the roster's other two-row exposure routes (Aerathiel, Crystal Essence, Kyuko-sei, Houkyuken, Hyouga Yui and Sea-King's Blessing at +8%, Tenohira Musei at +7%), not alone.
- Concern: At 3 BP Exposure out-values Sovereign of the Hour wherever both exposure rows reach a hit (an ally's hit on the mark ×2.04 vs ×1.88; the caster's hit with all three rows live ×2.80 vs ×2.72) and on a hit that meets one exposure row without the self buff (×1.43 vs ×1.37). Sovereign leads wherever its self buff meets only one exposure row (×1.99 vs ×1.96: the Momentum Shift window alone, a Timeshift-marked target that Momentum Shift did not mark, or a highest-stat hit outside Earth/None/Sand/Wind on a target with all three rows live) and on unmarked targets such as Timelapse's circle (×1.45 vs ×1.37). Party size, target count and window uptime were not simulated.
- Concern: Every percentage row except Momentum Shift's exposure carries no Sand and needs the proposed jutsu-classification resolver; Sovereign of the Hour's whole route depends on it.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Sand jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Borrowed Hours | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Momentum Shift, Timeshift / 3 |
| 02 | Quickened Sands | Hidden Art | Borrowed Hours | +3% Increase Damage Given (self buff) | Momentum Shift / 1 |
| 03 | Sovereign of the Hour | Advanced Art | Quickened Sands | +5% Increase Damage Given (self buff) | Momentum Shift / 1 |
| 04 | Brittle with Age | Hidden Art | Borrowed Hours | +2% Increase Damage Taken (enemy debuff) | Momentum Shift, Timeshift / 2 |
| 05 | The Inevitable Hour | Advanced Art | Brittle with Age | +4% Increase Damage Taken (enemy debuff) | Momentum Shift, Timeshift / 2 |
| 06 | Suspended Moment | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Timelapse / 2 |
| 07 | Held in Stasis | Hidden Art | Suspended Moment | +3% Decrease Damage Taken (self buff) | Timelapse / 1 |
| 08 | Timeless Bastion | Advanced Art | Held in Stasis | +5% Decrease Damage Taken (self buff); +5% Heal (self buff) | Cellular Regeneration, Timelapse / 2 |
| 09 | Leaden Seconds | Hidden Art | Suspended Moment | +3% Decrease Damage Given (enemy debuff) | Timelapse / 1 |
| 10 | Stilled Hourglass | Advanced Art | Leaden Seconds | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff) | Timelapse / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Borrowed Hours** — Every second stolen from them is a second lent to you. Increase Damage Taken 35 → 37% on Timeshift (four stat types, no element) and Momentum Shift (Earth/None/Sand/Wind hits); Momentum Shift self Increase Damage Given 35 → 37%. 2 rounds after each cast.
- **Quickened Sands** — For you the grains run fast; for everyone else they barely fall. Setup: Momentum Shift self Increase Damage Given 37 → 40% with Borrowed Hours (2 rounds after the 40 AP cast).
- **Sovereign of the Hour** — The hour answers to one hand, and that hand strikes with every second of it. Sustained amplification: Momentum Shift self Increase Damage Given 35 → 45% on the full route (+10% on one row, ×1.074), on the caster's highest-stat and element-less hits against every target for the 2 rounds after the cast.
- **Brittle with Age** — Centuries pass in a heartbeat, and bone remembers every one of them. Setup for The Inevitable Hour: Timeshift and Momentum Shift Increase Damage Taken 37 → 39% with Borrowed Hours (enemy, 2 rounds after the cast).
- **The Inevitable Hour** — Nothing outruns the hour that was always coming. Exposure: both rows 35 → 43% on the full route (+8%); a hit under both takes ×1.43 × 1.43 ≈ ×2.04 (×1.82 at base), ×1.122 compounded against Blood-Enchanted Eyes' ×1.115 and Shakunetsu Sakura's ×1.075. Pierce excluded.
- **Suspended Moment** — Between one grain and the next, the world forgets to hurt you. Timelapse self Decrease Damage Taken 30 → 32% and Decrease Damage Given 30 → 32% on every enemy in the circle (2 rounds).
- **Held in Stasis** — The blow arrives; the moment it should land never does. Timelapse self Decrease Damage Taken 32 → 35% with Suspended Moment; self-targeted, so it lands on the caster wherever the circle is placed.
- **Timeless Bastion** — Stand still long enough and time learns to flow around you. Fortress: Timelapse self Decrease Damage Taken 30 → 40% on the full route (+10%); Cellular Regeneration Heal 25 → 30 (250 → 300 HP per tick, 600 per cast).
- **Leaden Seconds** — Their arms grow heavy with every second they cannot spend. Timelapse Decrease Damage Given 32 → 35% with Suspended Moment (enemies in the circle only).
- **Stilled Hourglass** — When the sand stops falling, so does everything inside the glass. Suppression: Timelapse Decrease Damage Given 30 → 40% on every enemy in the circle (+10%); self Decrease Damage Taken 32 → 34% with Suspended Moment.

## Complete four-purchase examples

| Build | Purchases | IDG | DDG | IDT | DDT | HEAL |
|---|---|---:|---:|---:|---:|---:|
| Sovereign of the Hour (Sustained amplification) | Borrowed Hours, Quickened Sands, Sovereign of the Hour, Brittle with Age | +10% | — | +4% | — | — |
| The Inevitable Hour (Exposure) | Borrowed Hours, Brittle with Age, The Inevitable Hour, Suspended Moment | +2% | +2% | +8% | +2% | — |
| Timeless Bastion (Fortress) | Suspended Moment, Held in Stasis, Timeless Bastion, Leaden Seconds | — | +5% | — | +10% | +5% |
| Stilled Hourglass (Suppression) | Borrowed Hours, Suspended Moment, Leaden Seconds, Stilled Hourglass | +2% | +10% | +2% | +4% | — |

Abbreviations: IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Sovereign of the Hour:** Self-amplification: Momentum Shift's self buff at 45% lifts the caster's own hits on every target for the two rounds after the cast, Timelapse's whole circle included; Brittle with Age puts both exposure rows at 39%. A hit under all three rows takes ×1.45 × 1.39 × 1.39 ≈ ×2.80 (×2.46 at base). Suspended Moment is the defensive alternative fourth.
- **The Inevitable Hour:** Team focus: Timeshift and Momentum Shift mark one target at 43% each, so nearly every non-pierce hit from the caster or an ally gains (Momentum Shift's row only Earth/None/Sand/Wind hits); a hit under both rows and the 37% self buff takes ×1.37 × 1.43 × 1.43 ≈ ×2.80. Suspended Moment adds Timelapse's 32% / 32% defence. Quickened Sands is the strongest offensive fourth (self buff 40%, ≈ ×2.86).
- **Timeless Bastion:** Outlast: Timelapse's self Decrease Damage Taken at 40% and Decrease Damage Given 35% on the circled enemy cut its hits on the caster to ×0.60 × 0.65 = ×0.39 (×0.49 at base), and Cellular Regeneration heals 300 HP per tick. Borrowed Hours is the alternative fourth for some exposure (37%).
- **Stilled Hourglass:** Team control: Decrease Damage Given 40% on every enemy in the Timelapse circle protects the whole side, self Decrease Damage Taken 34%, and Borrowed Hours adds 37% exposure and self buff. Held in Stasis instead of Borrowed Hours is the duel build: Decrease Damage Taken 37%, an enemy in the circle hits the caster at ×0.60 × 0.63 ≈ ×0.38.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustained amplification | Exposure | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Timelapse | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Timelapse | 1 | Decrease Damage Given | enemy | 30% | 30% | 32% (+2) | 35% (+5) | 40% (+10) |
| Timelapse | 2 | Decrease Damage Taken | self | 30% | 30% | 32% (+2) | 40% (+10) | 34% (+4) |
| Timeshift | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Timeshift | 1 | Increase Damage Taken | enemy | 35% | 39% (+4) | 43% (+8) | 35% | 37% (+2) |
| Timeshift | 2 | timecompression (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Eternity Flux | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Eternity Flux | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Cellular Regeneration | 0 | barrier (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Cellular Regeneration | 1 | Heal | self | 25 | 25 | 25 | 30 (+5) | 25 |
| Momentum Shift | 0 | Increase Damage Taken | enemy | 35% | 39% (+4) | 43% (+8) | 35% | 37% (+2) |
| Momentum Shift | 1 | Increase Damage Given | self | 35% | 45% (+10) | 37% (+2) | 35% | 37% (+2) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +10% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken, +5% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Sovereign of the Hour: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route The Inevitable Hour: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Timeless Bastion: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Stilled Hourglass: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 3, DDG 1, DDT 1, HEAL 1, IDG 1, IDT 2)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Borrowed Hours, Suspended Moment, Held in Stasis, Timeless Bastion (raw +21, row-weighted 23)
- Lowest row-weighted node: Quickened Sands (3)

Validator warnings:

- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Timelapse 40 (Normal), Timeshift 40 (Normal), Eternity Flux 50 (Nuke)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Sovereign of the Hour | +10% IDG, +2% IDT | Brittle with Age | +10% IDG, +4% IDT | 18 |
| Sovereign of the Hour | +10% IDG, +2% IDT | Suspended Moment *(highest diagnostic)* | +10% IDG, +2% DDG, +2% IDT, +2% DDT | 18 |
| The Inevitable Hour | +2% IDG, +8% IDT | Quickened Sands | +5% IDG, +8% IDT | 21 |
| The Inevitable Hour | +2% IDG, +8% IDT | Suspended Moment *(highest diagnostic)* | +2% IDG, +2% DDG, +8% IDT, +2% DDT | 22 |
| Timeless Bastion | +2% DDG, +10% DDT, +5% HEAL | Borrowed Hours *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% DDT, +5% HEAL | 23 |
| Timeless Bastion | +2% DDG, +10% DDT, +5% HEAL | Leaden Seconds | +5% DDG, +10% DDT, +5% HEAL | 20 |
| Stilled Hourglass | +10% DDG, +4% DDT | Borrowed Hours *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +4% DDT | 20 |
| Stilled Hourglass | +10% DDG, +4% DDT | Held in Stasis | +10% DDG, +7% DDT | 17 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Borrowed Hours, Quickened Sands, Sovereign of the Hour, Brittle with Age | +10% IDG, +4% IDT |
| 2 | Borrowed Hours, Quickened Sands, Sovereign of the Hour, Suspended Moment | +10% IDG, +2% DDG, +2% IDT, +2% DDT |
| 3 | Borrowed Hours, Quickened Sands, Brittle with Age, The Inevitable Hour | +5% IDG, +8% IDT |
| 4 | Borrowed Hours, Quickened Sands, Brittle with Age, Suspended Moment | +5% IDG, +2% DDG, +4% IDT, +2% DDT |
| 5 | Borrowed Hours, Quickened Sands, Suspended Moment, Held in Stasis | +5% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Borrowed Hours, Quickened Sands, Suspended Moment, Leaden Seconds | +5% IDG, +5% DDG, +2% IDT, +2% DDT |
| 7 | Borrowed Hours, Brittle with Age, The Inevitable Hour, Suspended Moment | +2% IDG, +2% DDG, +8% IDT, +2% DDT |
| 8 | Borrowed Hours, Brittle with Age, Suspended Moment, Held in Stasis | +2% IDG, +2% DDG, +4% IDT, +5% DDT |
| 9 | Borrowed Hours, Brittle with Age, Suspended Moment, Leaden Seconds | +2% IDG, +5% DDG, +4% IDT, +2% DDT |
| 10 | Borrowed Hours, Suspended Moment, Held in Stasis, Timeless Bastion | +2% IDG, +2% DDG, +2% IDT, +10% DDT, +5% HEAL |
| 11 | Borrowed Hours, Suspended Moment, Held in Stasis, Leaden Seconds | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | Borrowed Hours, Suspended Moment, Leaden Seconds, Stilled Hourglass | +2% IDG, +10% DDG, +2% IDT, +4% DDT |
| 13 | Suspended Moment, Held in Stasis, Timeless Bastion, Leaden Seconds | +5% DDG, +10% DDT, +5% HEAL |
| 14 | Suspended Moment, Held in Stasis, Leaden Seconds, Stilled Hourglass | +10% DDG, +7% DDT |

## Design notes

- Structure unchanged (01→02→03, 01→04→05, 06→07→08, 06→09→10); the Foundations follow the kit's paired jutsu. Changes from Draft 4: the +5 Damage route (Grinding Sands / Erosion of Eternity; the 40s to 45, Eternity Flux 50 → 55) becomes self-amplification, Quickened Sands +3% / Sovereign of the Hour +5% Increase Damage Given (2/3/5 = +10% on Momentum Shift's one self row); The Inevitable Hour drops its Increase Damage Given rider and is pure exposure (2/2/4 = +8%); Suspended Moment trades Heal +2% for Decrease Damage Given +2%; Timeless Bastion carries the whole +5% Heal; Stilled Hourglass is +5% Decrease Damage Given (route still +10%) with +2% Decrease Damage Taken. The roster pass's +2 Damage on Sovereign is withdrawn: with Tank / Control Traits and a 50 row on a C-rank stun cast there is no kit reason to lift Eternity Flux past the Nuke tier, so Damage is unamplified (Timeshift and Timelapse 40, Eternity Flux 50 EP in every allocation).
- Sovereign vs Exposure at 3 BP, with the offensive fourth (Brittle with Age / Quickened Sands) in brackets; base kit ×2.46 with all three Momentum Shift / Timeshift rows live. With all three live a caster's hit takes ×2.72 [×2.80] under Sovereign and ×2.80 [×2.86] under Exposure; Timeshift window alone ×1.37 [×1.39] vs ×1.43; Momentum Shift window alone ×1.99 [×2.02] vs ×1.96 [×2.00]; an ally's hit on the mark ×1.88 [×1.93] vs ×2.04. Exposure is the single-target team route; Sovereign leads on the caster's hits where its self buff meets only one exposure row, and on unmarked targets (Timelapse's circle ×1.45 vs ×1.37 [×1.40]). Exposure stays at the batch's two-row +8%, ×1.122 compounded (director question).
- Defence: both routes use one Timelapse cast. An enemy in the circle hits the caster at ×0.408 (Fortress) or ×0.396 (Suppression) at 3 BP, ×0.39 or ×0.378 with the sibling Hidden Art (base ×0.49); the Fortress keeps its Heal, the Suppression covers every enemy in the circle and the caster's allies. Maxima over every legal allocation: Increase Damage Given +10%, Increase Damage Taken +8%, Decrease Damage Taken +10%, Decrease Damage Given +10%, Heal +5%; no flat Damage.
- Matching and delivery (tags.ts 3477–3510; §3b): Timeshift's exposure and Timelapse's rows list four stat types and no element, so they match nearly every non-pierce hit; Momentum Shift's exposure matches only Earth/None/Sand/Wind hits; its self buff ('Highest', no element) matches the caster's highest-stat and element-less hits. Every cast has cooldown 7 and buff/debuff rows act the two rounds after the cast round only.

## Risks and unproven interactions

- Classification: Sand is the single signature element and no other captured kit carries it. 4 of 9 kit rows carry Sand; the other five need the proposed jutsu-classification resolver, and Cellular Regeneration carries no element on any row, so in-kit it qualifies only through an authored Sand jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Sand coverage is unverified.
- Ally hazard: Timelapse's Sand damage hits every other user inside the circle, allies included (friendly fire none = ALL; the caster never; actions.ts 1029-1060); the tree adds no Damage to it (40 EP). Only enemies get its Decrease Damage Given row, and the Decrease Damage Taken row is self-targeted.
- Exposure reach: The Inevitable Hour's 43% rows amplify allies' hits as well as the caster's, and any other Increase Damage Taken source multiplies again (stacking on, process.ts 1109-1117). Team value is larger than the duel arithmetic above.
- Area suppression reach: Stilled Hourglass's 40% Decrease Damage Given lands on every enemy in the Timelapse circle and cuts their damage to the caster's allies too; worth more in team battles than one row suggests.
- Heal: static heal is ×10 HP per tick, so +5% Heal adds 50 HP per tick (600 per cast vs 500). The SELF row on the EMPTY_GROUND spiral lands on the caster at cast time, not through the tiles (actions.ts 980-1004), and ticks on the two following rounds only. Healprevent blocks it.
- Highest-stat resolution (G16): Momentum Shift's self buff lists 'Highest', resolved from the caster's highestOffence (a required BattleUserState field, types.ts 156). If undefined, it would still match element-less hits and the kit's own Sand rows, not other elemental jutsu.
- No combat simulation: stun, timecompression, the barrier, circle target counts, AP and uptime were not modelled. A sealed or prevented Timelapse cast removes both defensive routes' value for that cycle. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Sand jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

