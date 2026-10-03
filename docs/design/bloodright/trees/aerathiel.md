# Aerathiel — Litany of Dust

**Bloodline:** Aerathiel (BR-002, rank A, `1C34syOOEKp6k3UKweYT6`) · **Revision:** Draft 4 / Dust classification / forked tree · **Classification:** Dust (element) · **Engine status:** proposal_requires_resolver_adjustment

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

- **Total Disintegration:** The +5 power route on all three Dust attacks (Particle Cannon 55, Death's March and Decaying Touch 45) with Entropic Grasp's amplify/expose support from earlier casts. Scouring Veil is the fourth purchase because it opens the control root without competing for the damage rows; Hollowing Wind (exposure +5 total) is the offensive alternative.
- **Terminal Decay:** Exposure first: Windshear Decay and Death's March Increase Damage Taken reach 42% each (adding 84% of the staged base when both sit on one target) while Atomic Shield's two damage buffs reach 40%. Particle Collapse is the fourth purchase because the exposed target's next hits are the kit's own Dust strikes (Particle Cannon, Decaying Touch); Scouring Veil is the defensive alternative.
- **Atomic Reprisal:** Atomic Shield as the centrepiece: Reflect 50% and both damage buffs 40% for the two rounds after one 40 AP cast, with Windshear and Death's March exposure at 37%. Entropic Grasp is the fourth purchase because it stacks Increase Damage Given to +5; Withering Gale (suppression +5) is the control alternative.
- **Requiem of Dust:** Windshear Decay as an AOE control cast: Decrease Damage Given 45% and Increase Damage Taken 39% on every non-caster user in the radius-1 circle (placed up to 5 tiles away; allies there too), with Death's March exposure also 39%. Entropic Grasp is the fourth purchase for exposure +4 and a small amplify; Particulate Ward (Reflect 45%) is the defensive alternative.

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

- Node split: the roots mirror the kit's two support casts. Entropic Grasp (offence) raises Atomic Shield's two Increase Damage Given rows and the two AOE exposure rows; Scouring Veil (control) raises Atomic Shield's Reflect row and Windshear Decay's Decrease Damage Given row. Each root forks into two Hidden Art → Advanced Art routes (Damage and Exposure; Reflect and Suppression): every Advanced Art is 3 BP deep and any two cost 5–6 BP.
- Reference reuse: flats copy Taiyo Kami nearly verbatim (Entropic Grasp = Dawnheart; the Damage route = Crown of Cinders/Solar Cataclysm; Withering Gale = Ashen Verdict; the Reflect route reuses the DDT ladder +2/+3/+5 with +3 IDG), because the kit has the same shape: three Dust damage rows, two IDG rows, single-row DDG. Departures: no Afterburn or DDT rows, so Hollowing Wind is IDT +3 and Terminal Decay IDT +2/IDG +3; Requiem's IDT is +2, not +5, so a capstone never outbids Hollowing Wind.
- Filters (§3, register G15): Atomic Shield row 0 (Highest stat, no element) matches the caster's highest-offence-stat hits and every element-less hit; row 2 matches Dust/Earth/Wind and element-less hits, so the kit's Dust strikes and element-less weapon or basic hits take both buffs (+70% of staged base, 80% at IDG +5). Windshear Decay rows 0–1 match any stat-based or element-less hit; Death's March row 1 only Dust/Earth/Wind or element-less hits. The passive IDG multiplies downstream.
- Delivery and timing (§3b): all five jutsu have cooldown 7. The damage casts cost 60 AP (Death's March a range-4 circle spawn; Decaying Touch and Particle Cannon single-target, range 4); Windshear Decay is a 40 AP range-5 circle spawn, Atomic Shield a 40 AP self cast. Each buff/debuff row is live in the two rounds after its cast round, never in it: Death's March's exposure never boosts its own hit, and Shield's buffs help only later strikes. No rotation was simulated.
- Fourth purchase: Burst takes Scouring Veil (Reflect/DDG +2) or Hollowing Wind (IDT +5); Pressure takes Particle Collapse (+2 Damage) or Scouring Veil; Fortified takes Entropic Grasp (IDG +5, IDT +2) or Withering Gale (DDG +5); Suppression takes Entropic Grasp (IDT +4, IDG +2) or Particulate Ward (Reflect +5). Hybrids without an Advanced Art spread smaller gains over four tags. All 14 legal full builds are non-dominated, every node is in one, and neither Foundation is universal (12 of 14 each).
- Value option (user-owned, not applied): Requiem's IDT secondary could rise to +3 only with Hollowing Wind at +4, or the Entropic Grasp + Hollowing Wind + Scouring Veil + Withering Gale hybrid becomes dominated by the Requiem build; that lifts the IDT route maximum to +8, above the two-row ceiling. No heal, lifesteal, Decrease Damage Taken or Afterburn rows exist in this kit, so no sustain or burn route is invented.

## Risks and unproven interactions

- Single-cast concentration: Requiem of Dust raises both Windshear Decay debuff rows (Decrease Damage Given 45%, Increase Damage Taken 37–39%) from one 40 AP AOE cast; Atomic Reprisal raises all three Atomic Shield rows (Reflect 50%, two damage buffs 38–40%) from one 40 AP self cast. Per-AP value of those two D/A-rank support casts rises more than the damage route's.
- Exposure stacking (§3b, process.ts 1109–1117): Windshear Decay and Death's March apply separate 2-round IDT debuffs that both apply and add, so one target takes +70% of the staged base (84% at the +7 route max; row-weighted 14 against the reference's largest single-tag concentration, Damage +5 × 3 rows = 15). The two windows overlap for at most two rounds per cooldown-7 cycle; not simulated.
- Leakage: in the two rounds after Atomic Shield both enhanced IDG rows add to the caster's normal jutsu and weapon hits (Highest-stat or element-less for row 0; Dust/Earth/Wind or element-less for row 2). Windshear Decay's exposure (row 0) raises what the target takes from allies and weapons too; its suppression (row 1) lowers the target's own jutsu and weapon damage against the caster's side.
- Friendly fire (validator WARN accepted): Death's March and Windshear Decay are OTHER_USER AOE_CIRCLE_SPAWN casts whose INHERIT rows land once on each living non-caster user in the radius-1 circle when friendlyFire is none/ALL (§4b, G16), so the Damage, Exposure and Suppression routes also raise what allies there receive; the caster is never a target. Positioning, not the tree, decides.
- Reflect value is downstream: it depends on how many hits the bearer takes during the two-round window, including pierce hits (which bypass the row's stat filter, tags.ts 3478–3479), and is capped at 60% of each pre-shield hit; at 50% the cap is not reached, but realised value was not simulated.
- Classification: the Dust label collides with Kyuko-sei (INCLUDE) and Nejireru Funjin (DEFER), and the normal-jutsu Dust collision is unverified, so eligibility must be bloodline-scoped. Under the current resolver 5 of 9 supported rows match Dust; the other 4 (Atomic Shield rows 0–1, Windshear Decay rows 0–1) fall back to None and need the proposed whole-kit classification.
- Unsupported rows (Windshear Decay redirection pull, Decaying Touch recoil, Particle Cannon wound) are unchanged by every node; the trait text 'sustained damage over time' is not reflected in any supported DoT row, so no node addresses it.
- Ranked PvP and ranked sparring suppress skill-tree effects at the pin, so the whole tree is inert there. Normal-tree potency policy is not approved; a combined main-tree plus Bloodright potency audit is still required before any implementation.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Aerathiel jutsu inherit Dust potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

