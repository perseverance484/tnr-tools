# Night Parade of A Thousand Demons — The Lantern Procession

**Bloodline:** Night Parade of A Thousand Demons (BR-051, rank H, `r_99Xg8SIOYw2awCMSR7e`) · **Revision:** Draft 2 / Shadow classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Shadow (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Otherworldly Conduit self buffs: Decrease Damage Taken (+10% route) and Lifesteal (+5% route), with Increase Damage Given as +5% glue · secondary Damage on the two Shadow hits, Possessing Yurei and Oni Hammer Swing (+5) · tertiary Enemy debuffs: Herald of the Black Night exposure (Increase Damage Taken, +10% route) with Oni Hammer Swing suppression (Decrease Damage Given, +5%, ally hazard).

Three of the seven supported rows ride one 40 AP self cast, Otherworldly Conduit (Increase Damage Given 35%, Decrease Damage Taken 35%, Lifesteal 40% at jutsu level 25, 2 rounds, realized on the caster at cast time), so the Conduit is the kit's engine and root A buffs it: Decrease Damage Taken and Lifesteal each take a route, Increase Damage Given is Foundation-plus-capstone glue. The two Shadow Damage rows (Possessing Yurei single target, Oni Hammer Swing radius-1 circle; 45 EP, 60 AP, cooldown 7) are the only direct damage and take the Damage route under root B, whose Foundation carries the two enemy debuffs: Oni Hammer Swing's 30% Decrease Damage Given and Herald of the Black Night's 35% Increase Damage Taken (element-less, all four stat types, friendly fire ENEMIES, radius-1 circle at range 5 for 40 AP). The Herald's exposure is the fourth route; it amplifies every non-pierce hit on exposed enemies from any source, the summoned Underworld Gate ally included. Potency reaches matching supported tags on all Shadow jutsu (RUL-2026-10-03-005). Stun, buffprevent and summon are unsupported and untouched.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hour of the Ox | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Otherworldly Conduit / 2 |
| 02 | Hungry Ghost's Draught | Hidden Art | Hour of the Ox | +2% Lifesteal (self buff) | Otherworldly Conduit / 1 |
| 03 | Feast of a Thousand Mouths | Advanced Art | Hungry Ghost's Draught | +3% Lifesteal (self buff); +3% Increase Damage Given (self buff) | Otherworldly Conduit / 2 |
| 04 | Hide of the Oni | Hidden Art | Hour of the Ox | +3% Decrease Damage Taken (self buff) | Otherworldly Conduit / 1 |
| 05 | Barred Gate of Yomi | Advanced Art | Hide of the Oni | +5% Decrease Damage Taken (self buff); +2% Lifesteal (self buff) | Otherworldly Conduit / 2 |
| 06 | Oni's Heavy Hand | Foundation | None | +2% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Herald of the Black Night, Oni Hammer Swing / 2 |
| 07 | Grip of the Yurei | Hidden Art | Oni's Heavy Hand | +2 Damage (damage) | Oni Hammer Swing, Possessing Yurei / 2 |
| 08 | March of a Thousand Demons | Advanced Art | Grip of the Yurei | +3 Damage (damage) | Oni Hammer Swing, Possessing Yurei / 2 |
| 09 | Marked by the Herald | Hidden Art | Oni's Heavy Hand | +3% Increase Damage Taken (enemy debuff) | Herald of the Black Night / 1 |
| 10 | Toll of the Night Bell | Advanced Art | Marked by the Herald | +5% Increase Damage Taken (enemy debuff); +3% Decrease Damage Given (enemy debuff) | Herald of the Black Night, Oni Hammer Swing / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hour of the Ox** — At the hour of the ox the veil thins, and what crosses it walks beside you. Otherworldly Conduit self buffs: Increase Damage Given 35 → 37%, Decrease Damage Taken 35 → 37%; one 40 AP self cast, 2 rounds, non-pierce hits.
- **Hungry Ghost's Draught** — The hungry dead drink what you spill, and leave a share for the one who opened the way. Otherworldly Conduit Lifesteal only, 40 → 42%: a share of every hit you land (pierce included) for 2 rounds; 60% leech cap shared with vamp.
- **Feast of a Thousand Mouths** — A thousand mouths at the table, and every one of them feeds you. Conduit Lifesteal to 45% (route +5%, the hard ceiling; 15 points under the 60% leech cap) and its Increase Damage Given +3% (40% with Hour of the Ox); same 40 AP cast.
- **Hide of the Oni** — An oni's hide turns the blade that would have split a lesser thing. Otherworldly Conduit Decrease Damage Taken only: 37 → 40% with Hour of the Ox; every non-pierce hit of any stat type, 2 rounds per 40 AP cast.
- **Barred Gate of Yomi** — Yomi's gate is barred from the inside; what stands behind it does not come to harm. Conduit Decrease Damage Taken to 45% (route +10%) and Lifesteal +2% (42%, or 44% with Hungry Ghost's Draught); one 40 AP self cast, 2 rounds.
- **Oni's Heavy Hand** — The oni does not lift the hammer. The hammer lifts the oni, and comes down. Oni Hammer Swing Decrease Damage Given 30 → 32% on its radius-1 circle (allies too); Herald of the Black Night exposure 35 → 37% on its circle (enemies only).
- **Grip of the Yurei** — A yurei's fingers close where the heart used to be, and do not let go. Possessing Yurei (single target) and Oni Hammer Swing (radius-1 circle) Shadow Damage 45 → 47 EP; range 4, 60 AP, CD 7.
- **March of a Thousand Demons** — The lanterns bob, the drums roll, and the whole procession walks over you. Same two Shadow Damage rows; route total +5 Damage (45 → 50 EP at jutsu level 25). Yurei's stun and the Hammer's rider unchanged.
- **Marked by the Herald** — The herald names you to the parade, and the parade remembers. Herald of the Black Night exposure only, 37 → 40% with Oni's Heavy Hand: radius-1 circle at range 5 (friendly fire ENEMIES), 40 AP; every non-pierce hit, 2 rounds.
- **Toll of the Night Bell** — When the night bell tolls, every hand raised against you weakens and every wound deepens. Herald exposure to 45% (route +10%) and Oni Hammer Swing Decrease Damage Given +3% (35% with Oni's Heavy Hand; allies in its circle too).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Feast of a Thousand Mouths (Sustain) | Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Hide of the Oni | — | +5% | — | — | +5% | +5% |
| Barred Gate of Yomi (Fortress) | Hour of the Ox, Hide of the Oni, Barred Gate of Yomi, Oni's Heavy Hand | — | +2% | +2% | +2% | +10% | +2% |
| March of a Thousand Demons (Burst) | Oni's Heavy Hand, Grip of the Yurei, March of a Thousand Demons, Hour of the Ox | +5 | +2% | +2% | +2% | +2% | — |
| Toll of the Night Bell (Pressure) | Oni's Heavy Hand, Marked by the Herald, Toll of the Night Bell, Grip of the Yurei | +2 | — | +5% | +10% | — | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Feast of a Thousand Mouths:** The whole Conduit, raised: one 40 AP self cast now gives Lifesteal 45% (+5%, the hard ceiling, under the 60% leech cap), Increase Damage Given 40% (+5%) and Decrease Damage Taken 40% (+5%) for 2 rounds, so every hit the caster lands in the window hits harder and heals more while taking less. Hide of the Oni is the fourth purchase because it deepens the same cast; Oni's Heavy Hand (01, 02, 03, 06) trades that for a 32% Hammer suppression and 37% Herald exposure.
- **Barred Gate of Yomi:** Decrease Damage Taken on the Conduit reaches 45% (+10%, the Golden Mantle / Sovereign Sun shape) against every non-pierce hit of any stat type, with Lifesteal 42% and Increase Damage Given 37% from the same cast. Oni's Heavy Hand is the cross-root fourth purchase: the Hammer's suppression at 32% and the Herald's exposure at 37%. Hungry Ghost's Draught (01, 02, 04, 05) is the pure-Conduit alternative at 45% reduction and 44% lifesteal.
- **March of a Thousand Demons:** The two-row Damage route in full: Possessing Yurei and Oni Hammer Swing 45 → 50 EP (+5) before the bloodline's Increase Damage Given passive and the Conduit buff multiply them, with the Hammer's suppression at 32% and the Herald's exposure at 37%. Hour of the Ox is the fourth purchase so the Conduit frames the hits (37% given, 37% taken); Marked by the Herald (06, 07, 08, 09) is the all-offence alternative that exposes the targets at 40% first.
- **Toll of the Night Bell:** Herald of the Black Night exposes every enemy in its circle at 45% (+10%) for 2 rounds and the Hammer's suppression reaches 35% (+5%): the marked take more from every source, the kit, normal jutsu, weapons, allies and the Underworld Gate summon, and deal less back. Grip of the Yurei is the fourth purchase (both hits 47 EP) so the caster has something heavier to land in the window; Hour of the Ox (06, 09, 10, 01) is the Conduit alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustain | Fortress | Burst | Pressure |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Possessing Yurei | 0 | Damage | enemy | 45 | 45 | 45 | 50 (+5) | 47 (+2) |
| Possessing Yurei | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Oni Hammer Swing | 0 | Damage | enemy | 45 | 45 | 45 | 50 (+5) | 47 (+2) |
| Oni Hammer Swing | 1 | Decrease Damage Given | enemy | 30% | 30% | 32% (+2) | 32% (+2) | 35% (+5) |
| Otherworldly Conduit | 0 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Otherworldly Conduit | 1 | Decrease Damage Taken | self | 35% | 40% (+5) | 45% (+10) | 37% (+2) | 35% |
| Otherworldly Conduit | 2 | Lifesteal | self | 40% | 45% (+5) | 42% (+2) | 40% | 40% |
| Summoning: Underworld Gate | 0 | summon (unsupported) | self | 100% | 100% | 100% | 100% | 100% |
| Herald of the Black Night | 0 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Herald of the Black Night | 1 | Increase Damage Taken | enemy | 35% | 35% | 37% (+2) | 37% (+2) | 45% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 13; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +5% Decrease Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Feast of a Thousand Mouths: +5% Lifesteal (0 + 2 + 3; on band)
  - Route Barred Gate of Yomi: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route March of a Thousand Demons: +5 Damage (0 + 2 + 3; on band)
  - Route Toll of the Night Bell: +10% Increase Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 7 (DMG 2, DDG 1, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Hour of the Ox, Oni's Heavy Hand, Marked by the Herald, Toll of the Night Bell (raw +19, row-weighted 19)
- Lowest row-weighted node: Hungry Ghost's Draught (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Oni Hammer Swing#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Hide of the Oni | +5% IDG, +5% DDT, +5% LS |
| 2 | Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Oni's Heavy Hand | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +5% LS |
| 3 | Hour of the Ox, Hungry Ghost's Draught, Hide of the Oni, Barred Gate of Yomi | +2% IDG, +10% DDT, +4% LS |
| 4 | Hour of the Ox, Hungry Ghost's Draught, Hide of the Oni, Oni's Heavy Hand | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +2% LS |
| 5 | Hour of the Ox, Hungry Ghost's Draught, Oni's Heavy Hand, Grip of the Yurei | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +2% LS |
| 6 | Hour of the Ox, Hungry Ghost's Draught, Oni's Heavy Hand, Marked by the Herald | +2% IDG, +2% DDG, +5% IDT, +2% DDT, +2% LS |
| 7 | Hour of the Ox, Hide of the Oni, Barred Gate of Yomi, Oni's Heavy Hand | +2% IDG, +2% DDG, +2% IDT, +10% DDT, +2% LS |
| 8 | Hour of the Ox, Hide of the Oni, Oni's Heavy Hand, Grip of the Yurei | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 9 | Hour of the Ox, Hide of the Oni, Oni's Heavy Hand, Marked by the Herald | +2% IDG, +2% DDG, +5% IDT, +5% DDT |
| 10 | Hour of the Ox, Oni's Heavy Hand, Grip of the Yurei, March of a Thousand Demons | +5 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT |
| 11 | Hour of the Ox, Oni's Heavy Hand, Grip of the Yurei, Marked by the Herald | +2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT |
| 12 | Hour of the Ox, Oni's Heavy Hand, Marked by the Herald, Toll of the Night Bell | +2% IDG, +5% DDG, +10% IDT, +2% DDT |
| 13 | Oni's Heavy Hand, Grip of the Yurei, March of a Thousand Demons, Marked by the Herald | +5 Damage, +2% DDG, +5% IDT |
| 14 | Oni's Heavy Hand, Grip of the Yurei, Marked by the Herald, Toll of the Night Bell | +2 Damage, +5% DDG, +10% IDT |

## Design notes

- Node split: two roots, four Hidden Arts, four Advanced Arts, every capstone 3 BP deep, two capstones 5 BP under one root or 6 across roots. Root A (Hour of the Ox, +2% Increase Damage Given and +2% Decrease Damage Taken on the Conduit) forks into Lifesteal (+2%, then +3% with +3% Increase Damage Given) and Decrease Damage Taken (+3%, then +5% with +2% Lifesteal). Root B (Oni's Heavy Hand, +2% Decrease Damage Given on the Hammer and +2% Increase Damage Taken on the Herald) forks into Damage (+2, then +3) and Increase Damage Taken (+3%, then +5% with +3% Decrease Damage Given).
- Recalibration (RUL-2026-10-03-005): Oni's Heavy Hand trades its +1 Damage for +2% Increase Damage Taken, so Burst is the default +5 Damage (Grip of the Yurei +2, March of a Thousand Demons +3; 45 → 50 EP); Lifesteal drops to the +5% hard ceiling (Hungry Ghost's Draught +3% → +2%, Feast of a Thousand Mouths +5% → +3%; 40 → 45%); Toll of the Night Bell's Increase Damage Taken rises from +4% to +5%, so with the Foundation's +2% Pressure lands on +10% (35 → 45%). Fortress is unchanged at +10% Decrease Damage Taken (2/3/5; 35 → 45%).
- Maxima over every legal allocation: Damage +5, Lifesteal +5% (Feast route; Barred Gate of Yomi's +2% with Hungry Ghost's Draught reaches 4%), Increase Damage Taken +10%, Decrease Damage Taken +10%, Increase Damage Given +5%, Decrease Damage Given +5%.
- Capstone secondaries never out-bid a sibling Hidden Art: Barred Gate of Yomi's +2% Lifesteal equals Hungry Ghost's Draught; Feast of a Thousand Mouths takes +3% Increase Damage Given, a tag no Hidden Art carries; Toll of the Night Bell takes +3% Decrease Damage Given, which otherwise only the root carries. March of a Thousand Demons is Damage-only, like Solar Cataclysm.
- Interactions: every non-damage supported row is element-less and lists all four stat types, so at the pin the Conduit's buffs, the Herald's exposure and the Hammer's suppression match every non-pierce hit of any stat type (Lifesteal also counts pierce). The bloodline passive (Increase Damage Given 25% + 0.15/level; Earth, None, Shadow, Water, Wind) is not a potency target; it multiplies last (fromType bloodline) and compounds with the Conduit buff, which is its own stage-2 multiplier (§3b). Damage modifiers skip pierce.
- Delivery and uptime: the Conduit is a SELF cast, so its three rows are realized on the caster at cast time (not positional); 40 AP, cooldown 7, 2 rounds, so at most 2 of 7 rounds. Herald of the Black Night (OTHER_USER, AOE_CIRCLE_SPAWN radius 1, range 5, 40 AP, cooldown 7) applies its exposure once to each living enemy on the tiles; the caster is never a target. Oni Hammer Swing (OPPONENT, same method, range 4, 60 AP) damages enemies only; its Decrease Damage Given rider (friendly fire none) reaches allies too.
- Fourth purchases: Sustain (01, 02, 03) takes Hide of the Oni (40% reduction) or Oni's Heavy Hand (32% suppression, 37% exposure); Fortress (01, 04, 05) takes Oni's Heavy Hand or Hungry Ghost's Draught (44% lifesteal); Burst (06, 07, 08) takes Hour of the Ox (37% given / taken) or Marked by the Herald (40% exposure); Pressure (06, 09, 10) takes Grip of the Yurei (47 EP) or Hour of the Ox. Capstone-less hybrids are enumerated by the validator; see the audit.

## Risks and unproven interactions

- Classification: Shadow is shared with other bloodlines (expected under RUL-2026-10-03-005). 2 of 7 kit rows carry Shadow; the other five need the proposed jutsu-classification resolver, and Otherworldly Conduit, Herald of the Black Night and Summoning: Underworld Gate carry no element on any row, so in-kit they qualify only through an authored Shadow jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Shadow coverage is unverified.
- Ally hazard (accepted, small): Oni Hammer Swing row 1 (Decrease Damage Given 30%) is an INHERIT row on an OPPONENT AOE_CIRCLE_SPAWN with friendly fire none, so allies on the radius-1 tiles around the target receive the suppression too; the caster never does. Oni's Heavy Hand (+2%) and Toll of the Night Bell (+3%) raise it to 35% for allies and enemies alike. Positioning decides; solo it is gain.
- Increase Damage Taken reach: the Herald's exposure (element-less, all four stat types) amplifies every non-pierce hit each exposed enemy takes for 2 rounds from any source (allies, weapons, normal jutsu, the Underworld Gate summon), and one cast can expose several enemies, so per-row weight understates the Pressure route's +10% (35 → 45%). Oni's Heavy Hand's +2% also reaches every root-B build.
- Lifesteal budget: the 60%-of-pre-shield-damage leech cap is shared with vamp, so 45% leaves 15 points of headroom and any vamp from equipment or the main tree erodes the capstone's value. healprevent on the caster blocks it entirely; the kit itself applies none. Lifesteal includes pierce hits, which the kit does not have, so only weapons or normal jutsu with pierce feed it that way.
- Increase Damage Given stacking: the +5% glue raises the Conduit's 35% self buff to 40% (×1.40 on matching hits instead of ×1.35), which compounds with the bloodline passive (applied last, honouring allowBloodlineDamageIncrease), any exposure on the target and any main-tree or gear modifiers, each its own multiplier (§3b). Combined final damage was not simulated.
- Realized value: all five jutsu share cooldown 7 and both damage casts cost 60 AP, so the Conduit's 2-round window rarely covers both hits and the Herald's exposure in one rotation; per-row numbers overstate per-round value. Buffs and debuffs act only in the rounds after their cast round (SOURCE_MECHANICS §3b). Nothing was simulated.
- Damage is formula-calculated (sqrt scaling on Highest / Highest) and then multiplied by the Increase Damage Given passive, the Conduit buff and any exposure, so +5 raw EP is not a linear +5 damage. Each Damage row fires at most once per 7 rounds.
- Unsupported rows and modes: Possessing Yurei's stun, Herald of the Black Night's buffprevent (itself an ally-hazard row, unchanged by any node) and the Underworld Gate summon receive nothing. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING, so no node applies there.

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

