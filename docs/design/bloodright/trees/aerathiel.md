# Aerathiel — Litany of Dust

**Bloodline:** Aerathiel (BR-002, rank A, `1C34syOOEKp6k3UKweYT6`) · **Revision:** Draft 5 / Dust classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Dust (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (Dust attacks) · secondary Increase Damage Taken (AOE exposure) · tertiary Reflect and Decrease Damage Given (Atomic Shield / Windshear control).

Three of the nine supported rows are Dust Damage (Death's March 40, Decaying Touch 40, Particle Cannon 50 EP at jutsu level 25), so the kit's declared role is sustained offense. Increase Damage Taken reaches two AOE rows (Windshear Decay and Death's March) that can both sit on one target, so exposure is the second emphasis. The kit's only self cast, Atomic Shield, carries two Increase Damage Given rows and the single Reflect row; the only suppression row is Windshear Decay's Decrease Damage Given. There are no heal, lifesteal, Decrease Damage Taken or Afterburn rows, so no sustain or burn route is invented.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dust jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Entropic Grasp | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Atomic Shield, Death's March, Windshear Decay / 4 |
| 02 | Particle Collapse | Hidden Art | Entropic Grasp | +2 Damage (damage) | Death's March, Decaying Touch, Particle Cannon / 3 |
| 03 | Total Disintegration | Advanced Art | Particle Collapse | +3 Damage (damage) | Death's March, Decaying Touch, Particle Cannon / 3 |
| 04 | Hollowing Wind | Hidden Art | Entropic Grasp | +3% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 2 |
| 05 | Terminal Decay | Advanced Art | Hollowing Wind | +5% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Atomic Shield, Death's March, Windshear Decay / 4 |
| 06 | Scouring Veil | Foundation | None | +2% Reflect (self buff); +2% Decrease Damage Given (enemy debuff) | Atomic Shield, Windshear Decay / 2 |
| 07 | Particulate Ward | Hidden Art | Scouring Veil | +3% Reflect (self buff) | Atomic Shield / 1 |
| 08 | Atomic Reprisal | Advanced Art | Particulate Ward | +5% Reflect (self buff); +3% Increase Damage Given (self buff) | Atomic Shield / 3 |
| 09 | Withering Gale | Hidden Art | Scouring Veil | +3% Decrease Damage Given (enemy debuff) | Windshear Decay / 1 |
| 10 | Requiem of Dust | Advanced Art | Withering Gale | +5% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Entropic Grasp** — Every touch loosens the bonds that hold a body together. Atomic Shield's two self damage buffs 35 → 37% and the Windshear Decay / Death's March exposure debuffs 35 → 37%.
- **Particle Collapse** — Matter gives way one particle at a time. Dust Damage on Death's March and Decaying Touch 40 → 42 EP and Particle Cannon 50 → 52 EP (all 60 AP, cooldown 7).
- **Total Disintegration** — Nothing remains to bury. Damage route total +5: Particle Cannon 50 → 55 EP, Death's March and Decaying Touch 40 → 45 EP.
- **Hollowing Wind** — The gale scours away whatever once turned a blade. Windshear Decay and Death's March Increase Damage Taken (two AOE rows, 2 rounds) 35 → 40% with Entropic Grasp.
- **Terminal Decay** — Once decay begins, it does not stop. Pressure route total +10% Increase Damage Taken: Windshear Decay and Death's March 35 → 45%; Atomic Shield's two damage buffs +3% (40% with Entropic Grasp).
- **Scouring Veil** — A curtain of grit that blunts the blow and bites back. Atomic Shield Reflect 40 → 42% (40 AP self cast) and Windshear Decay Decrease Damage Given 35 → 37% (40 AP AOE debuff).
- **Particulate Ward** — Dust thickens into a shell that remembers every strike. Atomic Shield Reflect 45% with Scouring Veil (one row, 2 rounds per cast); reflected damage is capped at 60% of each hit taken.
- **Atomic Reprisal** — What strikes the shield returns, and the shield-bearer strikes harder. Reflect route total +10% (Atomic Shield 40 → 50%, under the 60% per-hit cap); both Atomic Shield damage buffs +3% (40% with Entropic Grasp).
- **Withering Gale** — Arms grow heavy in the dust-laden wind. Windshear Decay Decrease Damage Given 40% with Scouring Veil (one AOE row, range 5, 40 AP, 2 rounds); its redirection row is unsupported.
- **Requiem of Dust** — The march ends where the wind lays everything down. Suppression route total +10% (Windshear Decay 35 → 45%) plus both exposure rows +2% (39% with Entropic Grasp).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | REF |
|---|---|---:|---:|---:|---:|---:|
| Total Disintegration (Burst) | Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil | +5 | +2% | +2% | +2% | +2% |
| Terminal Decay (Pressure) | Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay | +2 | +5% | — | +10% | — |
| Atomic Reprisal (Fortified) | Entropic Grasp, Scouring Veil, Particulate Ward, Atomic Reprisal | — | +5% | +2% | +2% | +10% |
| Requiem of Dust (Suppression) | Entropic Grasp, Scouring Veil, Withering Gale, Requiem of Dust | — | +2% | +10% | +4% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Total Disintegration:** +5 Damage on all three Dust attacks (Particle Cannon 50 → 55, Death's March and Decaying Touch 40 → 45 EP), with Entropic Grasp's 37% amplify and exposure from earlier casts. Scouring Veil is the fourth purchase (Reflect 42%, Decrease Damage Given 37%); Hollowing Wind (exposure 40%) is the offensive alternative.
- **Terminal Decay:** Exposure first: Windshear Decay and Death's March Increase Damage Taken reach 45% each (×1.45 × 1.45 on a matching hit when both sit on one target) while Atomic Shield's two damage buffs reach 40%. Particle Collapse is the fourth purchase (Dust strikes 42 / 52 EP) because the exposed target's next hits are the kit's own Dust strikes; Scouring Veil is the defensive alternative.
- **Atomic Reprisal:** Atomic Shield as the centrepiece: Reflect 50% and both damage buffs 40% for the two rounds after one 40 AP cast, with Windshear Decay and Death's March exposure at 37%. Entropic Grasp is the fourth purchase because it lifts Increase Damage Given to +5%; Withering Gale (Decrease Damage Given 40%) is the control alternative.
- **Requiem of Dust:** Windshear Decay as an AOE control cast: Decrease Damage Given 45% and Increase Damage Taken 39% on every non-caster user in the radius-1 circle (placed up to 5 tiles away; allies there too), with Death's March exposure also 39%. Entropic Grasp is the fourth purchase for exposure +4% and a small amplify; Particulate Ward (Reflect 45%) is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Pressure | Fortified | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Windshear Decay | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 39% (+4) |
| Windshear Decay | 1 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 45% (+10) |
| Windshear Decay | 2 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Death's March | 0 | Damage | enemy | 40 | 45 (+5) | 42 (+2) | 40 | 40 |
| Death's March | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 39% (+4) |
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
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +10% Increase Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Total Disintegration: +5 Damage (0 + 2 + 3; on band)
  - Route Terminal Decay: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Atomic Reprisal: +10% Reflect (2 + 3 + 5; on band)
  - Route Requiem of Dust: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 3, DDG 1, IDG 2, IDT 2, REF 1)
- Strongest full build by row-weighted total: Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay (raw +17, row-weighted 36)
- Lowest row-weighted node: Particulate Ward (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Death's March#0, Death's March#1, Windshear Decay#0, Windshear Decay#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Entropic Grasp, Particle Collapse, Total Disintegration, Hollowing Wind | +5 Damage, +2% IDG, +5% IDT |
| 2 | Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% REF |
| 3 | Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay | +2 Damage, +5% IDG, +10% IDT |
| 4 | Entropic Grasp, Particle Collapse, Hollowing Wind, Scouring Veil | +2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% REF |
| 5 | Entropic Grasp, Particle Collapse, Scouring Veil, Particulate Ward | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% REF |
| 6 | Entropic Grasp, Particle Collapse, Scouring Veil, Withering Gale | +2 Damage, +2% IDG, +5% DDG, +2% IDT, +2% REF |
| 7 | Entropic Grasp, Hollowing Wind, Terminal Decay, Scouring Veil | +5% IDG, +2% DDG, +10% IDT, +2% REF |
| 8 | Entropic Grasp, Hollowing Wind, Scouring Veil, Particulate Ward | +2% IDG, +2% DDG, +5% IDT, +5% REF |
| 9 | Entropic Grasp, Hollowing Wind, Scouring Veil, Withering Gale | +2% IDG, +5% DDG, +5% IDT, +2% REF |
| 10 | Entropic Grasp, Scouring Veil, Particulate Ward, Atomic Reprisal | +5% IDG, +2% DDG, +2% IDT, +10% REF |
| 11 | Entropic Grasp, Scouring Veil, Particulate Ward, Withering Gale | +2% IDG, +5% DDG, +2% IDT, +5% REF |
| 12 | Entropic Grasp, Scouring Veil, Withering Gale, Requiem of Dust | +2% IDG, +10% DDG, +4% IDT, +2% REF |
| 13 | Scouring Veil, Particulate Ward, Atomic Reprisal, Withering Gale | +3% IDG, +5% DDG, +10% REF |
| 14 | Scouring Veil, Particulate Ward, Withering Gale, Requiem of Dust | +10% DDG, +2% IDT, +5% REF |

## Design notes

- Node split: the roots mirror the kit's two support casts. Entropic Grasp (offence) raises Atomic Shield's two Increase Damage Given rows and the two AOE exposure rows; Scouring Veil (control) raises Atomic Shield's Reflect row and Windshear Decay's Decrease Damage Given row. Each root forks into two Hidden Art → Advanced Art routes (Burst and Pressure; Fortified and Suppression): every Advanced Art is 3 BP deep and any two cost 5–6 BP.
- Routes: Burst +5 Damage (Particle Collapse +2, Total Disintegration +3); Pressure +10% Increase Damage Taken (Entropic Grasp +2%, Hollowing Wind +3%, Terminal Decay +5%); Fortified +10% Reflect (Scouring Veil +2%, Particulate Ward +3%, Atomic Reprisal +5%); Suppression +10% Decrease Damage Given (Scouring Veil +2%, Withering Gale +3%, Requiem of Dust +5%). Glue maxima over every legal allocation: Increase Damage Given +5% (Entropic Grasp plus Terminal Decay's or Atomic Reprisal's +3%); Requiem's +2% Increase Damage Taken secondary keeps Pressure the only +10% exposure route.
- Filters (§3, register G15): Atomic Shield row 0 (Highest stat, no element) matches the caster's highest-offence-stat hits and every element-less hit; row 2 matches Dust/Earth/Wind and element-less hits, so the kit's Dust strikes and element-less weapon or basic hits take both buffs, which compound (×1.35 × 1.35 unmodified, ×1.40 × 1.40 at Increase Damage Given +5%; SOURCE_MECHANICS §3b). Windshear Decay rows 0–1 match any stat-based or element-less hit; Death's March row 1 only Dust/Earth/Wind or element-less hits. The passive Increase Damage Given multiplies downstream.
- Delivery and timing (§3b): all five jutsu have cooldown 7. The damage casts cost 60 AP (Death's March a range-4 circle spawn; Decaying Touch and Particle Cannon single-target, range 4); Windshear Decay is a 40 AP range-5 circle spawn, Atomic Shield a 40 AP self cast. Each buff/debuff row is live in the two rounds after its cast round, never in it: Death's March's exposure never boosts its own hit, and Shield's buffs help only later strikes. No rotation was simulated.
- Fourth purchase: Burst takes Scouring Veil (Reflect and Decrease Damage Given +2%) or Hollowing Wind (exposure +5%); Pressure takes Particle Collapse (+2 Damage) or Scouring Veil; Fortified takes Entropic Grasp (Increase Damage Given +5%, exposure +2%) or Withering Gale (Decrease Damage Given +5%); Suppression takes Entropic Grasp (exposure +4%, Increase Damage Given +2%) or Particulate Ward (Reflect +5%). All 14 legal full builds are non-dominated, every node is in one, and neither Foundation is universal (12 of 14 each).

## Risks and unproven interactions

- Single-cast concentration: Requiem of Dust raises both Windshear Decay debuff rows (Decrease Damage Given 45%, Increase Damage Taken 37–39%) from one 40 AP AOE cast; Atomic Reprisal raises all three Atomic Shield rows (Reflect 50%, two damage buffs 38–40%) from one 40 AP self cast.
- Exposure stacking (§3b, process.ts 1109–1117): Windshear Decay and Death's March apply separate 2-round Increase Damage Taken debuffs that both apply and compound (SOURCE_MECHANICS §3b), so a matching hit on a target under both takes ×1.35 × 1.35 ≈ ×1.82 unmodified and ×1.45 × 1.45 ≈ ×2.10 at the +10% Pressure route maximum. The two windows overlap for at most two rounds per cooldown-7 cycle; not simulated.
- Row reach: in the two rounds after Atomic Shield both enhanced Increase Damage Given rows apply to the caster's normal jutsu and weapon hits (Highest-stat or element-less for row 0; Dust/Earth/Wind or element-less for row 2). Windshear Decay's exposure (row 0) raises what the target takes from allies and weapons too; its suppression (row 1) lowers the target's own jutsu and weapon damage against the caster's side.
- Friendly fire (validator WARN accepted): Death's March and Windshear Decay are OTHER_USER AOE_CIRCLE_SPAWN casts whose INHERIT rows land once on each living non-caster user in the radius-1 circle when friendlyFire is none/ALL (§4b, G16), so the Burst, Pressure and Suppression routes also raise what allies there receive; the caster is never a target. Positioning, not the tree, decides.
- Reflect value is downstream: it depends on how many hits the bearer takes during the two-round window, including pierce hits (which bypass the row's stat filter, tags.ts 3478–3479), and is capped at 60% of each pre-shield hit; at 50% the cap is not reached, but realised value was not simulated.
- Classification: Dust is shared with Kyuko-sei and Nejireru Funjin (expected under RUL-2026-10-03-005). 5 of 9 kit rows carry Dust; Atomic Shield rows 0–1 and Windshear Decay rows 0–1 need the proposed jutsu-classification resolver, and Windshear Decay (no Dust row) additionally needs an authored Dust jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Dust coverage is unverified.
- Unsupported rows (Windshear Decay redirection, Decaying Touch recoil, Particle Cannon wound) are unchanged by every node; the trait text 'sustained damage over time' is not reflected in any supported damage-over-time row, so no node addresses it.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Dust jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

