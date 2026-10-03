# Aerathiel — Litany of Dust

**Bloodline:** Aerathiel (BR-002, rank A, `1C34syOOEKp6k3UKweYT6`) · **Revision:** Draft 3 / Dust classification / forked tree · **Classification:** Dust (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Damage (Dust attacks) · secondary Increase Damage Taken (AOE exposure) · tertiary Reflect and Decrease Damage Given (Atomic Shield / Windshear control).

Three of the nine supported rows are Dust damage (Death's March 40, Decaying Touch 40, Particle Cannon 50 at jutsu level 25), so the kit's declared role is sustained offense. Increase Damage Taken reaches two AOE rows (Windshear Decay and Death's March) that can both sit on one target, so it is the second emphasis but carries smaller flats than a single-row tag. The kit's only self cast, Atomic Shield, carries two Increase Damage Given rows and the single Reflect row; the only suppression row is Windshear Decay's Decrease Damage Given. There are no heal, lifesteal, Decrease Damage Taken or Afterburn rows, so no sustain route is invented.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Dust-classified Aerathiel jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Entropic Grasp | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Atomic Shield, Death's March, Windshear Decay / 4 |
| 02 | Particle Collapse | Hidden Art | Entropic Grasp | +2 Damage power (damage) | Death's March, Decaying Touch, Particle Cannon / 3 |
| 03 | Total Disintegration | Advanced Art | Particle Collapse | +3 Damage power (damage) | Death's March, Decaying Touch, Particle Cannon / 3 |
| 04 | Hollowing Wind | Hidden Art | Entropic Grasp | +3% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 2 |
| 05 | Terminal Decay | Advanced Art | Hollowing Wind | +2% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Atomic Shield, Death's March, Windshear Decay / 4 |
| 06 | Scouring Veil | Foundation | None | +2% Reflect (self buff); +2% Decrease Damage Given (enemy debuff) | Atomic Shield, Windshear Decay / 2 |
| 07 | Particulate Ward | Hidden Art | Scouring Veil | +3% Reflect (self buff) | Atomic Shield / 1 |
| 08 | Atomic Reprisal | Advanced Art | Particulate Ward | +5% Reflect (self buff); +3% Increase Damage Given (self buff) | Atomic Shield / 3 |
| 09 | Withering Gale | Hidden Art | Scouring Veil | +3% Decrease Damage Given (enemy debuff) | Windshear Decay / 1 |
| 10 | Requiem of Dust | Advanced Art | Withering Gale | +5% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Entropic Grasp** — Every touch loosens the bonds that hold a body together. Atomic Shield's two self damage buffs (35→37%) and the Windshear Decay / Death's March exposure debuffs (35→37%). 4 rows, no gates.
- **Particle Collapse** — Matter gives way one particle at a time. Death's March, Decaying Touch and Particle Cannon Dust damage rows (40/40/50 → 42/42/52 power). 3 rows, all 60 AP, cooldown 7.
- **Total Disintegration** — Nothing remains to bury. The same three Dust damage rows; with Particle Collapse the route adds +5 power (Particle Cannon 50→55, the AOE Death's March 40→45).
- **Hollowing Wind** — The gale scours away whatever once turned a blade. Windshear Decay and Death's March Increase Damage Taken (2 AOE rows, 2 rounds): 35→40% with prerequisite Entropic Grasp; 42% at route max.
- **Terminal Decay** — Once decay begins, it does not stop. Both exposure rows (+2) and both Atomic Shield damage buffs (+3); with Entropic Grasp and Hollowing Wind the route totals IDT +7 and IDG +5.
- **Scouring Veil** — A curtain of grit that blunts the blow and bites back. Atomic Shield Reflect (40→42%) and Windshear Decay Decrease Damage Given (35→37%). 2 rows: one 40 AP self cast, one 40 AP AOE debuff.
- **Particulate Ward** — Dust thickens into a shell that remembers every strike. Atomic Shield Reflect only (single row, 2 rounds per 40 AP cast); reflected damage is capped at 60% of each hit taken.
- **Atomic Reprisal** — What strikes the shield returns, and the shield-bearer strikes harder. All three Atomic Shield rows now enhanced: Reflect route total 50% (under the 60% per-hit cap); both damage buffs +3 (38%, 40% with Grasp).
- **Withering Gale** — Arms grow heavy in the dust-laden wind. Windshear Decay Decrease Damage Given only (single AOE row, range 5, 40 AP, 2 rounds); the jutsu's pull row is unsupported and unchanged.
- **Requiem of Dust** — The march ends where the wind lays everything down. Windshear Decay suppression (route total 45%) plus both exposure rows +2; both Windshear Decay debuff rows are raised by one 40 AP AOE cast.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | REF |
|---|---|---:|---:|---:|---:|---:|
| Total Disintegration (Burst) | Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil | +5 | +2% | +2% | +2% | +2% |
| Terminal Decay (Pressure) | Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay | +2 | +5% | — | +7% | — |
| Atomic Reprisal (Fortified) | Entropic Grasp, Scouring Veil, Particulate Ward, Atomic Reprisal | — | +5% | +2% | +2% | +10% |
| Requiem of Dust (Suppression) | Entropic Grasp, Scouring Veil, Withering Gale, Requiem of Dust | — | +2% | +10% | +4% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Total Disintegration:** The +5 power route on all three Dust attacks (Particle Cannon 55, Death's March and Decaying Touch 45) with Entropic Grasp's amplify/expose support. Scouring Veil is the fourth purchase because it opens the control root without competing for the damage rows; Hollowing Wind (exposure +5 total) is the offensive alternative.
- **Terminal Decay:** Exposure first: Windshear Decay and Death's March Increase Damage Taken reach 42% each (84% when both sit on one target; the +7 route maximum matches the reference's Increase Damage Taken reach) while Atomic Shield's two damage buffs reach 40%. Particle Collapse is the fourth purchase because Death's March both damages and exposes; Scouring Veil is the defensive alternative.
- **Atomic Reprisal:** Atomic Shield as the centrepiece: Reflect 50% and both damage buffs 40% from one 40 AP cast, with Windshear and Death's March exposure at 37%. Entropic Grasp is the fourth purchase because it stacks Increase Damage Given to +5; Withering Gale (suppression +5) is the control alternative.
- **Requiem of Dust:** Windshear Decay as an AOE control cast: Decrease Damage Given 45% and Increase Damage Taken 39% on every target standing in the radius-1 circle, which can be placed up to 5 tiles away, with Death's March exposure also 39%. Entropic Grasp is the fourth purchase for exposure +4 and a small amplify; Particulate Ward (Reflect 45%) is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Pressure | Fortified | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Windshear Decay | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 39% (+4) |
| Windshear Decay | 1 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 45% (+10) |
| Windshear Decay | 2 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Death's March | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Death's March | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 39% (+4) |
| Atomic Shield | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Atomic Shield | 1 | Reflect | self | 40% | 42% (+2) | 40% | 50% (+10) | 42% (+2) |
| Atomic Shield | 2 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 37% (+2) |
| Decaying Touch | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Decaying Touch | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Particle Cannon | 0 | Damage | enemy | 50 | 55 (+5) | 52 (+2) | 50 | 50 |
| Particle Cannon | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Decrease Damage Given +10%, Increase Damage Taken +7%, Reflect +10% (not jointly attainable)
- Supported rows in kit: 9 (DMG 3, DDG 1, IDG 2, IDT 2, REF 1)
- Strongest full build by row-weighted total: Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay (raw +14, row-weighted 30)
- Lowest row-weighted node: Particulate Ward (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Death's March#0, Death's March#1, Windshear Decay#0, Windshear Decay#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Entropic Grasp, Particle Collapse, Total Disintegration, Hollowing Wind | DMG +5, IDG +2, IDT +5 |
| 2 | Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil | DMG +5, IDG +2, DDG +2, IDT +2, REF +2 |
| 3 | Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay | DMG +2, IDG +5, IDT +7 |
| 4 | Entropic Grasp, Particle Collapse, Hollowing Wind, Scouring Veil | DMG +2, IDG +2, DDG +2, IDT +5, REF +2 |
| 5 | Entropic Grasp, Particle Collapse, Scouring Veil, Particulate Ward | DMG +2, IDG +2, DDG +2, IDT +2, REF +5 |
| 6 | Entropic Grasp, Particle Collapse, Scouring Veil, Withering Gale | DMG +2, IDG +2, DDG +5, IDT +2, REF +2 |
| 7 | Entropic Grasp, Hollowing Wind, Terminal Decay, Scouring Veil | IDG +5, DDG +2, IDT +7, REF +2 |
| 8 | Entropic Grasp, Hollowing Wind, Scouring Veil, Particulate Ward | IDG +2, DDG +2, IDT +5, REF +5 |
| 9 | Entropic Grasp, Hollowing Wind, Scouring Veil, Withering Gale | IDG +2, DDG +5, IDT +5, REF +2 |
| 10 | Entropic Grasp, Scouring Veil, Particulate Ward, Atomic Reprisal | IDG +5, DDG +2, IDT +2, REF +10 |
| 11 | Entropic Grasp, Scouring Veil, Particulate Ward, Withering Gale | IDG +2, DDG +5, IDT +2, REF +5 |
| 12 | Entropic Grasp, Scouring Veil, Withering Gale, Requiem of Dust | IDG +2, DDG +10, IDT +4, REF +2 |
| 13 | Scouring Veil, Particulate Ward, Atomic Reprisal, Withering Gale | IDG +3, DDG +5, REF +10 |
| 14 | Scouring Veil, Particulate Ward, Withering Gale, Requiem of Dust | DDG +10, IDT +2, REF +5 |

## Design notes

- Node split: the two roots mirror the kit's two support casts. Entropic Grasp (offence) raises Atomic Shield's two Increase Damage Given rows and the two AOE exposure rows; Scouring Veil (control) raises Atomic Shield's Reflect row and Windshear Decay's Decrease Damage Given row. Each root forks into two Hidden Art → Advanced Art routes (Damage and Exposure under Entropic Grasp; Reflect and Suppression under Scouring Veil): 2 Foundations, 4 Hidden Arts, 4 Advanced Arts, every Advanced Art 3 BP deep, any two Advanced Arts 5–6 BP.
- Flats are scaled by coverage, not rank. Damage reaches three rows and mirrors the reference (+2 Hidden, +3 Advanced, max +5). Increase Damage Taken reaches two AOE rows that can both be active on one target (base 35% + 35%), so its route maximum is held to +7 (Entropic Grasp +2, Hollowing Wind +3, Terminal Decay +2: 42% per row, 84% combined), the same reach as the reference's single-row Increase Damage Taken maximum rather than the +10 single-row ladder; Terminal Decay pairs that +2 with +3 Increase Damage Given so the Advanced Art still earns its cost across four rows. Increase Damage Given has two rows on one cast and is held to +5 max (37/40%), as in the reference. Reflect and Decrease Damage Given are single rows and carry the reference +2/+3/+5 ladder (max +10: Reflect 50%, Decrease Damage Given 45%). Requiem of Dust's secondary Increase Damage Taken is +2 rather than the calibration's +3 so that a capstone never outbids the Hidden Art that owns the tag (Hollowing Wind +3).
- Main tree and passives: Atomic Shield row 0 is filtered to the Highest stat and row 2 to Dust/Earth/None/Wind, so the enhanced buffs also multiply normal jutsu and weapon hits passing those filters in the two-round window. Windshear Decay rows 0–1 (four stat types, no element) alter damage from any stat-based or element-less source, allies and weapons included; Death's March row 1 is filtered to Dust/Earth/None/Wind, so the 84% combined exposure applies to the kit's own attacks and element-less hits, while other elemental sources from allies receive only Windshear Decay's 42%. The passive Increase Damage Given (25 + 0.15/level on Wind/Earth/Dust/None) multiplies the enhanced damage rows downstream; the 15% Wind Decrease Damage Taken passive is untouched.
- Delivery and uptime: all five jutsu have cooldown 7. The three damage casts cost 60 AP (Death's March is an AOE circle spawn at range 4; Decaying Touch and Particle Cannon are single-target at range 4). Windshear Decay is a 40 AP AOE circle spawn at range 5 carrying two 2-round debuffs; Atomic Shield is a 40 AP self cast with 2-round buffs. Realised value of every percentage node therefore depends on casting the support jutsu inside its window; no rotation was simulated.
- Fourth purchase choices: Burst takes Scouring Veil (+2 Reflect, +2 DDG) or Hollowing Wind (IDT +5 total); Pressure takes Particle Collapse (+2 Damage) or Scouring Veil; Fortified takes Entropic Grasp (IDG +5, IDT +2) or Withering Gale (DDG +5); Suppression takes Entropic Grasp (IDT +4, IDG +2) or Particulate Ward (Reflect +5). Hybrids with no Advanced Art (for example Entropic Grasp, Particle Collapse, Scouring Veil, Withering Gale) spread smaller gains across four tags. All 14 legal full allocations are numerically non-dominated: Draft 1's one trap purchase (Entropic Grasp, Hollowing Wind, Scouring Veil, Withering Gale, beaten on every axis by the Requiem of Dust build) is removed by giving Hollowing Wind +3 and Requiem of Dust +2 on Increase Damage Taken, so that two-root hybrid reaches IDT +5 against the Requiem build's +4. Every node appears in at least one non-dominated full build.
- Reflect at the route maximum (50%) stays below the engine's 60%-of-hit cap; reflected damage bypasses shield absorption and counts every hit taken, pierce included (pierce bypasses the row's stat filter). No heal, lifesteal, Decrease Damage Taken or Afterburn rows exist in this kit, so there is no sustain or burn route and none is invented.

## Risks and unproven interactions

- Single-cast concentration: Requiem of Dust raises both Windshear Decay debuff rows (Decrease Damage Given 45%, Increase Damage Taken 37–39%) from one 40 AP AOE cast; Atomic Reprisal raises all three Atomic Shield rows (Reflect 50%, two damage buffs 38–40%) from one 40 AP self cast. Per-AP value of those two D/A-rank support casts rises more than the damage route's.
- Increase Damage Taken stacking: Windshear Decay and Death's March each apply a separate 2-round exposure debuff and BATTLE_TAG_STACKING is on at the pin, so one target can carry 70% base exposure and 84% at the route maximum (+7 each; row-weighted +14 against the reference's largest single-tag concentration, Damage +5 × 3 rows = 15). The route maximum was lowered from Draft 1's +8 on review to stay at or below the reference's Increase Damage Taken reach; no combat simulation was run.
- Leakage: Atomic Shield's Increase Damage Given rows multiply normal jutsu and weapon damage that passes their stat (Highest) or element (Dust/Earth/None/Wind) filters while the buff is active; enemy-side exposure and suppression alter damage from allies and weapons as well (Windshear Decay rows 0–1 for any stat-based or element-less hit; Death's March row 1 only for Dust/Earth/Wind or element-less hits). Restricted casting scope does not restrict downstream benefit.
- Friendly fire on the AOE rows (dossier 'Ally hazard', validator warning accepted): Death's March and Windshear Decay target OTHER_USER with AOE_CIRCLE_SPAWN. At the pin the radius-1 spiral around the chosen tile (util.ts 2827–2828) is filtered to tiles holding a living user other than the caster (isValidMove, util.ts 2722–2760), and INHERIT rows are applied directly to that user when checkFriendlyFire passes (actions.ts 1029–1060, 1226–1247; process.ts 173–175), which it does for allies when friendlyFire is null or ALL; no ground effects are created. Death's March row 0 Damage (ALL) and the three debuff rows (null) therefore also land on allies inside the circle, so the Damage, Exposure and Suppression routes raise what allies there receive; the caster is never a target. Positioning, not the tree, decides. recipient_for (scripts/bloodright/bloodright_lib.py) maps OTHER_USER INHERIT rows to enemy regardless of friendlyFire, so the dossier marks the four rows ally-hazard, not adverse; the dossier footnote's 'and the caster' holds only for GROUND/EMPTY_GROUND spawns, which this kit lacks (register correction requested at the cross-roster pass).
- Reflect value is downstream: it depends on how many hits the bearer takes during the two-round window, including pierce hits (which bypass the row's stat filter, tags.ts 3478–3479), and is capped at 60% of each pre-shield hit; at 50% the cap is not reached, but realised value was not simulated.
- Classification: the Dust label collides with Kyuko-sei (INCLUDE) and Nejireru Funjin (DEFER) in the census, and the normal-jutsu Dust collision is unverified, so eligibility must be bloodline-scoped rather than a bare element match. Under the current resolver only 5 of 9 supported rows match Dust directly; the other 4 (Atomic Shield rows 0–1, Windshear Decay rows 0–1) fall back to None and need the proposed whole-kit classification.
- Unsupported rows (Windshear Decay redirection pull, Decaying Touch recoil, Particle Cannon wound) are unchanged by every node; the trait text 'sustained damage over time' is not reflected in any supported DoT row, so no node addresses it.
- Ranked PvP and ranked sparring suppress skill-tree effects at the pin, so the whole tree is inert there. Normal-tree potency policy is not approved; a combined stacking audit is still required before any implementation.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Aerathiel jutsu inherit Dust potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

