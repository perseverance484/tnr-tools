# Blue Blade Eyes — Edge of Sapphire

**Bloodline:** Blue Blade Eyes (BR-015, rank S, `clh4d6qo4000itb0hrx8t06wq`) · **Revision:** Draft 4 / Ice classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Ice (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst offense (Damage on five Ice rows; Increase Damage Given on four self rows) · secondary Control (Increase Damage Taken on three enemy rows; Decrease Damage Given on Icebound Might) · tertiary Self preservation and sustain (Decrease Damage Taken on the two ungated casts; Lifesteal on Arctic Frost).

Damage is the kit's broadest tag: five Ice rows at 40/45 EP (Icebound Might, Glacial Volley, Ice Shackles, Blade Resonance, Blue Crimson), and Increase Damage Given reaches four self rows at 35% (Glacial Volley, Blue Crimson, Arctic Frost, Quintessential Flake) under a 25% + 0.15/level bloodline passive of the same tag, so burst is the declared primary and the Burst trait's home. Increase Damage Taken (35% on Sapphire Command, Blade Resonance, Arctic Frost) and the single Decrease Damage Given row (30% on Icebound Might's AOE circle) are the Control trait's rows and the secondary. Decrease Damage Taken sits only on Quintessential Flake and Sapphire Command (35% each, 40 AP) and Lifesteal only on Arctic Frost (40%), so guard and drain are the tertiary routes. Shield, stun, buffprevent, wound, move and redirection are unsupported and untouched.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Ice jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Sapphire Edge | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Given (enemy debuff) | Arctic Frost, Blue Crimson, Glacial Volley, Icebound Might, Quintessential Flake / 5 |
| 02 | Honed Crescent | Hidden Art | Sapphire Edge | +2 Damage (damage) | Blade Resonance, Blue Crimson, Glacial Volley, Ice Shackles, Icebound Might / 5 |
| 03 | Stroke That Splits Stone | Advanced Art | Honed Crescent | +3 Damage (damage) | Blade Resonance, Blue Crimson, Glacial Volley, Ice Shackles, Icebound Might / 5 |
| 04 | Frostbitten Grip | Hidden Art | Sapphire Edge | +3% Decrease Damage Given (enemy debuff) | Icebound Might / 1 |
| 05 | Numb to the Marrow | Advanced Art | Frostbitten Grip | +5% Decrease Damage Given (enemy debuff); +3% Increase Damage Given (self buff) | Arctic Frost, Blue Crimson, Glacial Volley, Icebound Might, Quintessential Flake / 5 |
| 06 | Unblinking Sapphire | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Taken (self buff) | Arctic Frost, Blade Resonance, Quintessential Flake, Sapphire Command / 5 |
| 07 | Hoarfrost Bulwark | Hidden Art | Unblinking Sapphire | +3% Decrease Damage Taken (self buff) | Quintessential Flake, Sapphire Command / 2 |
| 08 | Glacier Does Not Yield | Advanced Art | Hoarfrost Bulwark | +5% Decrease Damage Taken (self buff); +3% Increase Damage Taken (enemy debuff) | Arctic Frost, Blade Resonance, Quintessential Flake, Sapphire Command / 5 |
| 09 | Thirst of the Frost | Hidden Art | Unblinking Sapphire | +2% Lifesteal (self buff) | Arctic Frost / 1 |
| 10 | Winter Takes Its Due | Advanced Art | Thirst of the Frost | +3% Lifesteal (self buff); +5% Increase Damage Taken (enemy debuff) | Arctic Frost, Blade Resonance, Sapphire Command / 4 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Sapphire Edge** — Blue chakra runs down the edge; what it touches keeps no edge of its own. Increase Damage Given 35 → 37% on Glacial Volley, Blue Crimson, Arctic Frost and Quintessential Flake; Decrease Damage Given 30 → 32% on Icebound Might's circle.
- **Honed Crescent** — The crescent is honed until the air itself parts before it. Ice Damage 40 → 42 EP on Icebound Might, Glacial Volley and Blue Crimson; 45 → 47 EP on Ice Shackles and Blade Resonance.
- **Stroke That Splits Stone** — One stroke splits the boulder. Nothing you face is harder than granite. Damage route total +5: 40 → 45 and 45 → 50 EP on the same five Ice Damage rows.
- **Frostbitten Grip** — Hands numbed by frost strike without conviction. Icebound Might Decrease Damage Given 35% with Sapphire Edge (every enemy in the circle, 2 rounds, 60 AP); the kit's only suppression row.
- **Numb to the Marrow** — Their blows lose all force in the cold; yours lose none. Decrease Damage Given route total +10% (Icebound Might 30 → 40%); Increase Damage Given 40% with Sapphire Edge on all four self damage buffs.
- **Unblinking Sapphire** — Sapphire eyes that never close see the opening and the blow alike. Increase Damage Taken 35 → 37% on Sapphire Command, Blade Resonance and Arctic Frost; Decrease Damage Taken 35 → 37% on Quintessential Flake and Sapphire Command.
- **Hoarfrost Bulwark** — Hoarfrost thickens on the skin until steel slides off it. Decrease Damage Taken 40% with Unblinking Sapphire on Sapphire Command and Quintessential Flake (self rows, live 2 rounds after cast).
- **Glacier Does Not Yield** — Stand in the cold long enough and nothing moves you; everything else cracks. Decrease Damage Taken route total +10% (35 → 45%) on both self rows; Increase Damage Taken 40% with Unblinking Sapphire on Sapphire Command, Blade Resonance and Arctic Frost.
- **Thirst of the Frost** — Frost does not merely bite. It drinks. Arctic Frost Lifesteal 40 → 42% (self, 2 rounds, 40 AP); leeches from every hit landed in the window, pierce included.
- **Winter Takes Its Due** — Winter asks nothing twice; what it takes from the enemy it keeps. Lifesteal route total +5% (Arctic Frost 40 → 45%, the hard ceiling); Increase Damage Taken 42% with Unblinking Sapphire on all three exposure rows.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Stroke That Splits Stone Burst (Burst) | Sapphire Edge, Honed Crescent, Stroke That Splits Stone, Unblinking Sapphire | +5 | +2% | +2% | +2% | +2% | — |
| Numb to the Marrow Suppression (Suppression) | Sapphire Edge, Frostbitten Grip, Numb to the Marrow, Unblinking Sapphire | — | +5% | +10% | +2% | +2% | — |
| Glacier Does Not Yield Bulwark (Bulwark) | Sapphire Edge, Unblinking Sapphire, Hoarfrost Bulwark, Glacier Does Not Yield | — | +2% | +2% | +5% | +10% | — |
| Winter Takes Its Due Drain (Drain) | Unblinking Sapphire, Hoarfrost Bulwark, Thirst of the Frost, Winter Takes Its Due | — | — | — | +7% | +5% | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Stroke That Splits Stone Burst:** +5 Damage on all five Ice Damage rows (40 → 45, 45 → 50 EP) with the self damage buffs at 37% and Icebound Might's suppression at 32%. Unblinking Sapphire is the fourth purchase because it raises the two casts that need no weapon (exposure 37%, guard 37%); Frostbitten Grip (suppression 35%) is the alternative.
- **Numb to the Marrow Suppression:** Icebound Might's circle suppresses every enemy inside it at 40% for the two rounds after the cast while all four self damage buffs reach 40% (Glacial Volley, Blue Crimson, Arctic Frost, Quintessential Flake), each multiplying matching hits in its window by ×1.40 before the bloodline passive multiplies. Unblinking Sapphire is the fourth purchase for exposure and guard at 37%; Honed Crescent (+2 Damage on five rows) is the offensive alternative.
- **Glacier Does Not Yield Bulwark:** The only route whose primary rows need no weapon: both Decrease Damage Taken rows reach 45% (SELF rows realized on the caster at cast, live the two following rounds; Quintessential Flake's is not tile-bound) and the three exposure rows reach 40%. Sapphire Edge is the fourth purchase for 37% self damage buffs and 32% suppression; Thirst of the Frost (Lifesteal 42%) is the sustain alternative.
- **Winter Takes Its Due Drain:** Arctic Frost opens a drain window for the two rounds after its cast: 45% of every hit the caster lands (the +5% hard ceiling; pierce included, 60% leech cap) returns as HP while its own exposure row, Blade Resonance and Sapphire Command sit at 42%. Hoarfrost Bulwark is the fourth purchase so the guard rows reach 40%; Sapphire Edge (37% self damage buffs) is the offensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Suppression | Bulwark | Drain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Icebound Might | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Icebound Might | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Icebound Might | 2 | Decrease Damage Given | enemy | 30% | 32% (+2) | 40% (+10) | 32% (+2) | 30% |
| Glacial Volley | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Glacial Volley | 1 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Glacial Volley | 2 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Ice Shackles | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Ice Shackles | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Blade Resonance | 0 | Damage | enemy | 45 | 50 (+5) | 45 | 45 | 45 |
| Blade Resonance | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 42% (+7) |
| Blue Crimson | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 | 40 |
| Blue Crimson | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Blue Crimson | 2 | wound (unsupported) | enemy | 35% | 35% | 35% | 35% | 35% |
| Quintessential Flake | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 40% (+5) |
| Quintessential Flake | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Quintessential Flake | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Sapphire Command | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 42% (+7) |
| Sapphire Command | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 40% (+5) |
| Sapphire Command | 2 | redirection (unsupported) | enemy | 3 | 3 | 3 | 3 | 3 |
| Arctic Frost | 0 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 37% (+2) | 35% |
| Arctic Frost | 1 | Lifesteal | self | 40% | 40% | 40% | 40% | 45% (+5) |
| Arctic Frost | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 42% (+7) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +7% Increase Damage Taken, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Stroke That Splits Stone: +5 Damage (0 + 2 + 3; on band)
  - Route Numb to the Marrow: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Glacier Does Not Yield: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Winter Takes Its Due: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 16 (DMG 5, DDG 1, DDT 2, IDG 4, IDT 3, LS 1)
- Strongest full build by row-weighted total: Sapphire Edge, Unblinking Sapphire, Hoarfrost Bulwark, Glacier Does Not Yield (raw +19, row-weighted 45)
- Lowest row-weighted node: Thirst of the Frost (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Icebound Might#0

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Sapphire Edge, Honed Crescent, Stroke That Splits Stone, Frostbitten Grip | +5 Damage, +2% IDG, +5% DDG |
| 2 | Sapphire Edge, Honed Crescent, Stroke That Splits Stone, Unblinking Sapphire | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT |
| 3 | Sapphire Edge, Honed Crescent, Frostbitten Grip, Numb to the Marrow | +2 Damage, +5% IDG, +10% DDG |
| 4 | Sapphire Edge, Honed Crescent, Frostbitten Grip, Unblinking Sapphire | +2 Damage, +2% IDG, +5% DDG, +2% IDT, +2% DDT |
| 5 | Sapphire Edge, Honed Crescent, Unblinking Sapphire, Hoarfrost Bulwark | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Sapphire Edge, Honed Crescent, Unblinking Sapphire, Thirst of the Frost | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Sapphire Edge, Frostbitten Grip, Numb to the Marrow, Unblinking Sapphire | +5% IDG, +10% DDG, +2% IDT, +2% DDT |
| 8 | Sapphire Edge, Frostbitten Grip, Unblinking Sapphire, Hoarfrost Bulwark | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 9 | Sapphire Edge, Frostbitten Grip, Unblinking Sapphire, Thirst of the Frost | +2% IDG, +5% DDG, +2% IDT, +2% DDT, +2% LS |
| 10 | Sapphire Edge, Unblinking Sapphire, Hoarfrost Bulwark, Glacier Does Not Yield | +2% IDG, +2% DDG, +5% IDT, +10% DDT |
| 11 | Sapphire Edge, Unblinking Sapphire, Hoarfrost Bulwark, Thirst of the Frost | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Sapphire Edge, Unblinking Sapphire, Thirst of the Frost, Winter Takes Its Due | +2% IDG, +2% DDG, +7% IDT, +2% DDT, +5% LS |
| 13 | Unblinking Sapphire, Hoarfrost Bulwark, Glacier Does Not Yield, Thirst of the Frost | +5% IDT, +10% DDT, +2% LS |
| 14 | Unblinking Sapphire, Hoarfrost Bulwark, Thirst of the Frost, Winter Takes Its Due | +7% IDT, +5% DDT, +5% LS |

## Design notes

- Shape follows Taiyo Kami (2F/4H/4A; +2%/+2% Foundations, Damage +2 → +3, percentage routes +2% / +3% / +5% with a +3% secondary). Departures: Sapphire Edge (Increase Damage Given + Decrease Damage Given) roots the Burst (Honed Crescent → Stroke That Splits Stone) and Suppression (Frostbitten Grip → Numb to the Marrow) routes; Unblinking Sapphire (Increase Damage Taken + Decrease Damage Taken) roots Bulwark and Drain. Lifesteal replaces Afterburn (no Afterburn rows).
- Routes (RUL-2026-10-03-005): Burst +5 Damage on five rows; Suppression +10% Decrease Damage Given (Sapphire Edge +2%, Frostbitten Grip +3%, Numb to the Marrow +5%); Bulwark +10% Decrease Damage Taken (Unblinking Sapphire +2%, Hoarfrost Bulwark +3%, Glacier Does Not Yield +5%); Drain +5% Lifesteal (Thirst of the Frost +2%, Winter Takes Its Due +3%) with a +5% Increase Damage Taken secondary. Glue maxima over every legal allocation: Increase Damage Given +5%, Increase Damage Taken +7% (Unblinking Sapphire plus Winter Takes Its Due).
- Recalibration: Numb to the Marrow's Decrease Damage Given +4% → +5% and Glacier Does Not Yield's Decrease Damage Taken +3% → +5% put both routes on +10% (the earlier item-gate and two-row discounts no longer apply); Lifesteal fell from +8% to the +5% hard ceiling (Thirst +3% → +2%, Winter +5% → +3%), and Winter's Increase Damage Taken secondary rose from +3% to +5% to keep the Drain route's weight. All 14 legal full builds remain non-dominated.
- Castability: six of eight jutsu need one of two HAND-slot bloodline weapons to be cast (The Threefold Gaze: Icebound Might, Glacial Volley, Ice Shackles; The Blue Blade: Blade Resonance, Blue Crimson, Arctic Frost); no node lists an item as a prerequisite and no bonus is limited by one. Castable rows: Threefold Gaze = Damage 3, IDG 2, DDG 1, IDT 1, DDT 2; Blue Blade = Damage 2, IDG 3, IDT 3, DDT 2, Lifesteal 1; no weapon = IDG 1, IDT 1, DDT 2. Dual wielding was not read at the pin. The ungated jutsu are buffs: no attack without a weapon.
- Resolver: the 25% + 0.15/level IDG passive multiplies enhanced Damage rows downstream. Nine of eleven buff/debuff rows have a stat filter but no element, so getEfficiencyRatio (SOURCE_MECHANICS §3) matches them to every element-less hit and to elemental hits of a listed stat type; they act on Ice hits, normal jutsu, weapons and basic attacks alike. Blade Resonance IDT and Arctic Frost IDG carry Earth/Ice/None/Water/Wind. IDG/IDT/DDG/DDT skip pierce; lifesteal includes it.
- Delivery: cooldown 7 on every jutsu; damage casts cost 60 AP, the rest 40 AP; percentage rows live the 2 rounds after the cast (§3b), so Glacial Volley's and Blue Crimson's own IDG never boosts their own hit. Quintessential Flake targets EMPTY_GROUND, but its guard and damage buff are SELF rows realized on the caster at cast, not through the tile (actions.ts 980-1004); only the unsupported move row is tile-based. Icebound Might's Damage row (friendly fire none = ALL) is the one ally-hazard row.
- Fourth purchases: Burst adds Unblinking Sapphire or Frostbitten Grip; Suppression adds Unblinking Sapphire or Honed Crescent; Bulwark adds Sapphire Edge or Thirst of the Frost; Drain adds Hoarfrost Bulwark or Sapphire Edge. All 14 allocations are non-dominated; every node is used. Strongest unadvertised builds by row weight (40): Sapphire Edge, Honed Crescent, Frostbitten Grip, Numb to the Marrow, and Drain with Sapphire Edge; Stroke That Splits Stone + Frostbitten Grip is the strongest unadvertised Damage build.

## Risks and unproven interactions

- Classification: Ice is shared with Hyouga Yui, Teno Yuki and other census bloodlines (expected under RUL-2026-10-03-005). 7 of 16 kit rows carry Ice; the other nine need the proposed jutsu-classification resolver, and Quintessential Flake and Sapphire Command (no Ice row) additionally need an authored Ice jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Ice coverage is unverified.
- Castability: 12 of 16 supported rows sit on weapon-gated jutsu. All Damage, Decrease Damage Given and Lifesteal rows are gated, so one weapon casts three (The Threefold Gaze) or two (The Blue Blade) of the five Damage rows, Suppression's row is cast with The Threefold Gaze and Drain's with The Blue Blade; only Bulwark's primary rows need no weapon. Gates decide castability, not eligibility; if both weapons can be wielded at once (not read at the pin), all five Damage rows are live.
- Ally hazard: Icebound Might row 0 (Damage, AOE_CIRCLE_SPAWN, friendly fire none = ALL) hits allies in the circle, never the caster; Honed Crescent and Stroke That Splits Stone raise that to 42 / 45 EP for allies inside. Blue Crimson's Damage row is ENEMIES-only (its wound row is unsupported). Sapphire Command's exposure row (friendly fire none, single target) exposes an ally at 37–42% if cast on one.
- Increase Damage Given stacking: four self rows reach 40% each at the maximum and all stack (process.ts 1109-1117). Blue Crimson, Arctic Frost and Quintessential Flake (140 AP) timed to share a round compound to ×1.40³ ≈ ×2.74 on matching hits (×2.46 unmodified); all four (both weapons, 200 AP) to ×1.40⁴ ≈ ×3.84; the 28.75% passive then multiplies (SOURCE_MECHANICS §3b). Increase Damage Given is held to +5% for this reason.
- Lifesteal: Arctic Frost's leech reaches 45% of every hit landed in its two-round window (all four stat types, no element: Ice hits, normal jutsu, weapons and basic attacks qualify; pierce included). It shares the 60%-of-pre-shield-damage budget with vamp; the kit has no vamp row, so other leech saturates after 15 more points. Needs both combatants alive; healprevent on the caster blocks it.
- Suppression and guard: Decrease Damage Given is one AOE row on a 60 AP, cooldown-7 cast (40% at maximum; value scales with enemies inside). Decrease Damage Taken is two 35% SELF rows on 40 AP casts, live the two rounds after cast and not tile-bound; cast together or in consecutive rounds they share a round, so matching non-pierce hits take ×0.55 × 0.55 ≈ ×0.30 at the +10% route maximum (×0.65 × 0.65 ≈ ×0.42 unmodified; damage never falls below 10% of the boosted, system-reduced hit). Not simulated.
- No adverse rows, hidden rows, mode restrictions or injected children exist; the unsupported shield, buffprevent, stun, wound, move and redirection rows are unchanged and pierce is absent. Skill-tree and bloodline effects are suppressed in ranked modes. No combat simulation: non-dominance of the 14 allocations is an arithmetic result over per-row additions, not evidence of equal combat strength.
- Rank context: Blue Blade Eyes is an S-rank bloodline with a 28.75% Increase Damage Given passive at jutsu level 25 and a 100 regen bonus; this tree equalises marginal opportunity against the reference, not final strength. Cross-bloodline comparison is deferred to the roster review.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Ice jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

