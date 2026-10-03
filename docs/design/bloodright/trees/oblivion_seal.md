# Oblivion Seal — Rites of Unmaking

**Bloodline:** Oblivion Seal (BR-053, rank A, `wasIGmDuczwD9PB89gML6`) · **Revision:** Draft 4 / Shadow classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Shadow (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage (three Shadow attacks) · secondary Increase Damage Taken and Increase Damage Given (Shadowrend exposure, Cursed Beast Form empowerment) · tertiary Shadow Surge sustain (Decrease Damage Taken, Lifesteal).

Three of the seven supported rows are Shadow Damage on 60 AP single-target casts (Cursed Beast Form 40, Curse Empowerment 40, Shadow Tether 50 EP at jutsu level 25) and the bloodline's traits are Burst and Sustained DPS, so offense is the declared primary and the Damage route reaches all three attacks. Shadowrend's 35% Increase Damage Taken (element-less, all four stat types listed) and Cursed Beast Form's 35% Increase Damage Given (Fire, Lightning, Shadow and element-less hits) are the two single-row amplifiers that make later strikes land harder (each is live the two rounds after its cast, never its own hit); exposure gets a full +10% route, empowerment is +5% Foundation-plus-capstone glue. Shadow Surge is the kit's only self-cast (40 AP, cooldown 7); its Decrease Damage Taken 35% and Lifesteal 40% are SELF rows realized on the caster at cast time and live the two rounds after it, not circle effects. They are tertiary by kit identity: Decrease Damage Taken takes Taiyo Kami's Sovereign Sun shape (+10%), Lifesteal stops at the +5% hard ceiling. Potency reaches matching supported tags on all Shadow jutsu (RUL-2026-10-03-005). No Afterburn, Reflect, Heal or Decrease Damage Given rows exist, so none is invented.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Brand of Oblivion | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Cursed Beast Form, Shadowrend / 2 |
| 02 | Umbral Claws | Hidden Art | Brand of Oblivion | +2 Damage (damage) | Curse Empowerment, Cursed Beast Form, Shadow Tether / 3 |
| 03 | Absolute Erasure | Advanced Art | Umbral Claws | +3 Damage (damage) | Curse Empowerment, Cursed Beast Form, Shadow Tether / 3 |
| 04 | Unraveled Wards | Hidden Art | Brand of Oblivion | +3% Increase Damage Taken (enemy debuff) | Shadowrend / 1 |
| 05 | Writ of Oblivion | Advanced Art | Unraveled Wards | +5% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Cursed Beast Form, Shadowrend / 2 |
| 06 | Umbral Refuge | Foundation | None | +2% Decrease Damage Taken (self buff) | Shadow Surge / 1 |
| 07 | Veil of Nothing | Hidden Art | Umbral Refuge | +3% Decrease Damage Taken (self buff) | Shadow Surge / 1 |
| 08 | Sealed Against Ruin | Advanced Art | Veil of Nothing | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Cursed Beast Form, Shadow Surge / 2 |
| 09 | Hungering Shade | Hidden Art | Umbral Refuge | +2% Lifesteal (self buff) | Shadow Surge / 1 |
| 10 | Maw of Oblivion | Advanced Art | Hungering Shade | +3% Lifesteal (self buff); +2% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Cursed Beast Form, Shadow Surge / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Brand of Oblivion** — The seal brands both hands: the one that curses and the one that is cursed. Cursed Beast Form self buff 35 → 37% (Fire, Lightning, Shadow, element-less hits); Shadowrend exposure 35 → 37% (non-pierce); next 2 rounds.
- **Umbral Claws** — The beast's shadow lengthens, and its claws find more of you. Cursed Beast Form 40 → 42, Curse Empowerment 40 → 42, Shadow Tether 50 → 52 EP (Shadow, single target, range 4, 60 AP, cooldown 7). Pierce untouched.
- **Absolute Erasure** — What the seal unmakes, the world forgets. Same three Shadow Damage rows; route total +5 Damage (Cursed Beast Form 45, Curse Empowerment 45, Shadow Tether 55 EP at jutsu level 25).
- **Unraveled Wards** — Shadowrend picks the knots of every ward loose. Shadowrend exposure only (+3% more: 40% with Brand of Oblivion); live the 2 rounds after each 60 AP cast; non-pierce hits from any source.
- **Writ of Oblivion** — The sentence is written on their skin and read by every blade. Shadowrend exposure to 45% (route +10%) and Cursed Beast Form self buff to 40% (+5% with Brand of Oblivion); each live 2 rounds after its cast.
- **Umbral Refuge** — The shadow you cast keeps you, and it is always hungry. Shadow Surge self Decrease Damage Taken 35 → 37%, on the caster the 2 rounds after each cast (40 AP, cooldown 7); opens both Surge branches.
- **Veil of Nothing** — Blows that reach into the void find less and less to strike. Shadow Surge self Decrease Damage Taken only (+3% more: 40% with Umbral Refuge); non-pierce hits; a 2-round cast-time buff, not positional.
- **Sealed Against Ruin** — Nothing passes the seal that the sealbearer does not permit. Shadow Surge Decrease Damage Taken to 45% (route +10%); Cursed Beast Form self buff +3% (38%, or 40% with Brand of Oblivion).
- **Hungering Shade** — The shade drinks whatever the curse spills. Shadow Surge Lifesteal only, 40 → 42%; a share of every hit heals, including Shadowrend's pierce; 60% cap shared with vamp.
- **Maw of Oblivion** — Open the maw and let it swallow every wound you deal and every one you take. Shadow Surge Lifesteal to 45% (route +5%, the hard ceiling), Decrease Damage Taken +2% (39% with Umbral Refuge) and Cursed Beast Form self buff +3% (40% with Brand of Oblivion).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | LS |
|---|---|---:|---:|---:|---:|---:|
| Absolute Erasure (Burst) | Brand of Oblivion, Umbral Claws, Absolute Erasure, Umbral Refuge | +5 | +2% | +2% | +2% | — |
| Writ of Oblivion (Exposure) | Brand of Oblivion, Unraveled Wards, Writ of Oblivion, Umbral Refuge | — | +5% | +10% | +2% | — |
| Sealed Against Ruin (Fortress) | Brand of Oblivion, Umbral Refuge, Veil of Nothing, Sealed Against Ruin | — | +5% | +2% | +10% | — |
| Maw of Oblivion (Sustain) | Brand of Oblivion, Umbral Refuge, Hungering Shade, Maw of Oblivion | — | +5% | +2% | +4% | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Absolute Erasure:** The Damage route puts +5 Damage on all three Shadow attacks (45/45/55 EP at jutsu level 25) and Brand of Oblivion adds +2% to both the self buff (37%) and Shadowrend's exposure (37%) that frame the following rounds' strikes. Umbral Refuge is the fourth purchase for a little Surge protection (37% reduction, a 2-round self buff); Unraveled Wards (01, 02, 03, 04) is the all-offense alternative at 40% exposure.
- **Writ of Oblivion:** Shadowrend's exposure rises to 45% (+10%) and Cursed Beast Form's self buff to 40% (+5%). Each opens the round after its cast, so Shadowrend in round 1 and Cursed Beast Form in round 2 put both on a round-3 Shadow Tether (×1.40 × 1.45 ≈ ×2.03), and every other non-pierce hit on the target in rounds 2-3, from normal jutsu, weapons or allies, gains the exposure. Umbral Refuge rounds it out (37% reduction); Umbral Claws (01, 02, 04, 05) trades that for +2 EP on the three attacks.
- **Sealed Against Ruin:** Shadow Surge's self buff cuts non-pierce hits to ×0.55 (45%, +10%) in the 2 rounds after each 40 AP cast, and the capstone's +3% self buff with Brand of Oblivion makes Cursed Beast Form a 40% window, so the fortress still presses the attack. Hungering Shade (06, 07, 08, 09) is the Surge-heavy alternative: 45% reduction, 42% lifesteal and a 38% Cursed Beast Form buff, with no exposure.
- **Maw of Oblivion:** Shadow Surge's Lifesteal reaches 45% (+5%, the hard ceiling; 15 points under the 60% leech cap) for the 2 rounds after each cast (never that round's own attack), returned on every hit the caster lands, Shadowrend's pierce included; Umbral Refuge and the capstone give 39% reduction, and Brand of Oblivion with the capstone's +3% makes Cursed Beast Form a 40% window with Shadowrend's exposure at 37%. Veil of Nothing (06, 07, 09, 10) is the pure Surge turtle: 42% reduction, 45% lifesteal, a 38% buff and no exposure.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Fortress | Sustain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Shadowrend | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Shadowrend | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) | 37% (+2) |
| Cursed Beast Form | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Cursed Beast Form | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 40% (+5) | 40% (+5) |
| Curse Empowerment | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Curse Empowerment | 1 | clearprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Curse Empowerment | 2 | stun (unsupported) | enemy | 110 | 110 | 110 | 110 | 110 |
| Shadow Tether | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Shadow Tether | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Shadow Surge | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 39% (+4) |
| Shadow Surge | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Shadow Surge | 2 | Lifesteal | self | 40% | 40% | 40% | 40% | 45% (+5) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Absolute Erasure: +5 Damage (0 + 2 + 3; on band)
  - Route Writ of Oblivion: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Sealed Against Ruin: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Maw of Oblivion: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 7 (DMG 3, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Brand of Oblivion, Umbral Claws, Absolute Erasure, Unraveled Wards (raw +12, row-weighted 22)
- Lowest row-weighted node: Umbral Refuge (2)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Brand of Oblivion, Umbral Claws, Absolute Erasure, Unraveled Wards | +5 Damage, +2% IDG, +5% IDT |
| 2 | Brand of Oblivion, Umbral Claws, Absolute Erasure, Umbral Refuge | +5 Damage, +2% IDG, +2% IDT, +2% DDT |
| 3 | Brand of Oblivion, Umbral Claws, Unraveled Wards, Writ of Oblivion | +2 Damage, +5% IDG, +10% IDT |
| 4 | Brand of Oblivion, Umbral Claws, Unraveled Wards, Umbral Refuge | +2 Damage, +2% IDG, +5% IDT, +2% DDT |
| 5 | Brand of Oblivion, Umbral Claws, Umbral Refuge, Veil of Nothing | +2 Damage, +2% IDG, +2% IDT, +5% DDT |
| 6 | Brand of Oblivion, Umbral Claws, Umbral Refuge, Hungering Shade | +2 Damage, +2% IDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Brand of Oblivion, Unraveled Wards, Writ of Oblivion, Umbral Refuge | +5% IDG, +10% IDT, +2% DDT |
| 8 | Brand of Oblivion, Unraveled Wards, Umbral Refuge, Veil of Nothing | +2% IDG, +5% IDT, +5% DDT |
| 9 | Brand of Oblivion, Unraveled Wards, Umbral Refuge, Hungering Shade | +2% IDG, +5% IDT, +2% DDT, +2% LS |
| 10 | Brand of Oblivion, Umbral Refuge, Veil of Nothing, Sealed Against Ruin | +5% IDG, +2% IDT, +10% DDT |
| 11 | Brand of Oblivion, Umbral Refuge, Veil of Nothing, Hungering Shade | +2% IDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Brand of Oblivion, Umbral Refuge, Hungering Shade, Maw of Oblivion | +5% IDG, +2% IDT, +4% DDT, +5% LS |
| 13 | Umbral Refuge, Veil of Nothing, Sealed Against Ruin, Hungering Shade | +3% IDG, +10% DDT, +2% LS |
| 14 | Umbral Refuge, Veil of Nothing, Hungering Shade, Maw of Oblivion | +3% IDG, +7% DDT, +5% LS |

## Design notes

- Reference reuse: topology and five nodes follow Taiyo Kami (Brand of Oblivion = Dawnheart; Umbral Claws, Absolute Erasure = Crown of Cinders, Solar Cataclysm; Veil of Nothing, Sealed Against Ruin = Golden Mantle, Sovereign Sun). It fits a near-identical row mix: three Damage rows and one row per modifier tag. Departures: with no Afterburn or Decrease Damage Given rows, the exposure branch is Increase Damage Taken only and the Surge root's second branch takes Lifesteal.
- Recalibration (RUL-2026-10-03-005): Unraveled Wards +2% → +3% and Writ of Oblivion's Increase Damage Taken +3% → +5% put Exposure on +10% (2/3/5; Shadowrend 35 → 45%). Lifesteal is cut to the +5% hard ceiling: Umbral Refuge drops its +2% Lifesteal, Hungering Shade +3% → +2%, Maw of Oblivion +5% → +3% (Surge 40 → 45%); Maw gains +3% Increase Damage Given, the glue the other two non-Damage capstones carry, so the Sustain build keeps an offensive rider. Burst (+5 Damage) and Fortress (+10% Decrease Damage Taken) are unchanged.
- Maxima over every legal allocation: Damage +5, Lifesteal +5%, Increase Damage Taken +10%, Decrease Damage Taken +10%, Increase Damage Given +5% (Brand of Oblivion plus any one capstone).
- Capstone secondaries never out-bid a sibling Hidden Art: Writ of Oblivion, Sealed Against Ruin and Maw of Oblivion take +3% Increase Damage Given (no Hidden Art carries it); Maw's +2% Decrease Damage Taken sits below Veil of Nothing's +3%. Absolute Erasure is Damage-only, like Solar Cataclysm.
- Passives and downstream reach: the bloodline passive (Increase Damage Given 25% + 0.15/level on Lightning, Fire, Shadow, None) is not a potency target, but Cursed Beast Form's buff row has the same element list, so the +5% glue raises the kit's later Shadow attacks, Fire and Lightning jutsu, basic attacks and non-elemental jutsu in the 2 rounds after its cast. Shadowrend's exposure lists all four stat types with no element, so every non-pierce hit from any source on the exposed target qualifies.
- Delivery: all five jutsu are cooldown 7; four are 60 AP, single target, range 4. Shadow Surge is a 40 AP EMPTY_GROUND circle, but its Decrease Damage Taken and Lifesteal are SELF rows realized on the caster at cast time (actions.ts 980-1004); the unsupported move row is the only positional row. Rows are live the two rounds after their cast round, never in it (§3b): Surge plus Cursed Beast Form in one 100 AP round, Shadowrend next, then Shadow Tether puts all four windows on that strike.
- Fourth purchases: Burst takes Umbral Refuge (37% reduction) or Unraveled Wards (40% exposure); Exposure takes Umbral Refuge or Umbral Claws (+2 EP on the three attacks); Fortress takes Brand of Oblivion (40% buff) or Hungering Shade (42% lifesteal, 38% buff, no exposure); Sustain takes Brand of Oblivion or Veil of Nothing (42% reduction, no exposure).
- Ten nodes: five supported tags on seven rows across four distinct roles (burst, exposure, fortress, sustain); no node reskins another. Pierce (Shadowrend 58), wound, stun, clearprevent and move are unsupported and untouched; no other supported tag has a row here, so none is invented.

## Risks and unproven interactions

- Classification: Shadow is shared with other bloodlines (expected under RUL-2026-10-03-005). 4 of 7 kit rows carry Shadow (the three Damage rows and Cursed Beast Form's buff); Shadowrend's exposure row needs the proposed jutsu-classification resolver, and Shadow Surge carries no element on any row, so in-kit it qualifies only through an authored Shadow jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Shadow coverage is unverified.
- Shadow Surge timing (§3b, §4b): its Decrease Damage Taken and Lifesteal are SELF rows realized on the caster at cast time, not tied to the circle, and like every modifier they skip the cast round: the 60 AP attack sharing Surge's 100 AP round is not lifestolen; hits dealt and taken in the two following rounds are covered. The move row is unsupported and irrelevant to potency.
- Lifesteal budget: the 60%-of-pre-shield-damage leech cap is shared with vamp and any other lifesteal. 45% leaves 15 points of headroom, so vamp from equipment or the main tree erodes the capstone's value. Lifesteal does include pierce hits, so Shadowrend's 58 pierce feeds it when cast in Surge's window; healprevent on the caster blocks it entirely.
- Increase Damage Taken reach: Shadowrend's exposure (element-less, all four stat types) amplifies every non-pierce hit the target takes in the 2 rounds after the cast, from any source, including allies, weapons and normal jutsu, so the Exposure build's row weight understates it. Shadowrend's own pierce row gains nothing: damage modifiers skip pierce and never act in their cast round.
- Arithmetic and stacking (§3, §3b): Cursed Beast Form's buff (up to 40%) and Shadowrend's exposure (up to 45%) are separate stage-2 multipliers, so a strike under both takes ×1.40 × 1.45 ≈ ×2.03 before the bloodline passive multiplies last. Same-tag effects from different jutsu or casters all apply, each as its own multiplier: another owner's 45% Shadowrend on the same target makes ×1.45 × 1.45 ≈ ×2.10 from exposure alone. Combined final damage was not simulated.
- Realized value: each window is live only the two rounds after its cast, so Cursed Beast Form's buff never raises its own 40 EP hit; with one 60 AP attack per 100 AP round and cooldown 7 on all five jutsu, a window covers at most two later kit attacks, and cooldown 7 forbids recasting the same jutsu inside its own window. Per-row numbers overstate per-round value.
- Shadowrend's pierce (58 at jutsu level 25) is the kit's largest hit and is unsupported; no node changes it. Only Lifesteal (the Hungering Shade branch) interacts with it. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Shadow jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

