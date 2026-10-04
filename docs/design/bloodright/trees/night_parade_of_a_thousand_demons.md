# Night Parade of A Thousand Demons — The Lantern Procession

**Bloodline:** Night Parade of A Thousand Demons (BR-051, rank H, `r_99Xg8SIOYw2awCMSR7e`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Shadow classification / forked tree · **Classification:** Shadow (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Otherworldly Conduit self buffs (Hour of the Ox): sustain offense on Lifesteal with Increase Damage Given, or a Decrease Damage Taken fortress · secondary Burst from Oni's Heavy Hand: Herald of the Black Night exposure set up on the Hidden Art, paid off with +2 Damage on Possessing Yurei and Oni Hammer Swing (45 → 47) · tertiary Suppression on Oni Hammer Swing's Decrease Damage Given (ally hazard).

Three of the seven supported rows ride one 40 AP self cast, Otherworldly Conduit (Increase Damage Given 35%, Decrease Damage Taken 35%, Lifesteal 40% at jutsu level 25, live for the 2 rounds after the cast), so root A, Hour of the Ox, is the Conduit: "How do I let the Conduit carry me through the fight: feed on it or wall it out?" Feast of a Thousand Mouths feeds (Lifesteal to the +5% ceiling with Increase Damage Given) and Barred Gate of Yomi walls (+10% Decrease Damage Taken, nothing else). Root B, Oni's Heavy Hand, works only on the enemy: "How do I break the enemy: mark them for the kill or crush the strength out of them?" March of a Thousand Demons is burst, with Marked by the Herald setting up exposure and a controlled +2 Damage on the two 45 EP Shadow hits as the payoff. Toll of the Night Bell is suppression on Oni Hammer Swing. Root A touches only Conduit rows and root B only enemy-side rows. Marked by the Herald's +3% is March's setup, the Opened Veins step of the Blood-Enchanted Eyes pattern (RUL-2026-10-04-001), not an exposure route: the Herald reaches 35 → 40% on one row (×1.037, under Shakunetsu Sakura's ×1.075). Potency reaches matching supported tags on all Shadow jutsu (RUL-2026-10-03-005). Stun, buffprevent and summon are unsupported and untouched.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Hour of the Ox | Foundation | How do I let the Conduit carry me through the fight: feed on it or wall it out? |
| Oni's Heavy Hand | Foundation | How do I break the enemy: mark them for the kill or crush the strength out of them? |
| Feast of a Thousand Mouths | Advanced Art | sustain offense |
| Barred Gate of Yomi | Advanced Art | fortress |
| March of a Thousand Demons | Advanced Art | burst: exposure set up, controlled raw-Damage payoff |
| Toll of the Night Bell | Advanced Art | suppression |

- Concern: The old Pressure route (+10% Herald exposure) is dropped; the Herald serves as Burst's setup, 35 → 40% (×1.037). A dedicated exposure route, if the director wants one, needs the one Herald row that Marked by the Herald already sets up, so Burst would lose its setup or the two Hidden Arts would twin; at +10% it would be ×1.074, Shakunetsu Sakura's level.
- Concern: Burst's distinct value is narrow. Suppression's realistic fourth (Marked by the Herald, 06, 07, 09, 10) takes Burst's whole 40% exposure setup, so against Burst with Dread of the Procession (06, 07, 08, 09) the only difference is +2 EP (×1.044 on two 60 AP, cooldown 7 hits) versus +5% Hammer suppression. This mirrors the director-accepted Blood-Enchanted Eyes pattern (Feast of the Fallen with Opened Veins). A larger mark would not separate them, since Toll buys the same mark as a fourth; Marked stays a +3% setup and March's +2 Damage remains the payoff that defines Burst. Not simulated.
- Concern: Barred Gate of Yomi and Toll of the Night Bell are single-tag capstones, lighter than the Blood-Enchanted Eyes and Arashima fortress / suppression capstones. Each rider the kit offers either stacks with a sibling route within 4 BP (Lifesteal or Increase Damage Given on the Fortress into Feast via Hungry Ghost's Draught, which shares Hour of the Ox with the Fortress, whereas Arashima's Lifesteal Hidden Art sits under the other root; Decrease Damage Given on the Fortress and Decrease Damage Taken on Toll into each other across the roots; Increase Damage Taken on Toll into Burst via Marked by the Herald) or hands one route's payoff to another (flat Damage; Lifesteal on Toll).
- Concern: Feast keeps +3% Increase Damage Given (route +5%), below the +5% capstone in the Blood-Enchanted Eyes and Arashima templates. At +5% Feast with Oni's Heavy Hand (×1.42 × 1.37 ≈ ×1.95 with 45% Lifesteal) would come within 3% of Burst with Hour of the Ox (≈ ×2.00) on the two kit hits and pass it on every other hit; the director may still prefer the template value.
- Concern: Off-kit Shadow Damage rows are unverified: March's +2 would take a 50 EP Shadow jutsu to 52 (the Blood-Enchanted Eyes precedent, RUL-2026-10-04-001) and a 38 EP one to 40 (Light to Normal). The kit's two 45 EP rows cross no tier.
- Concern: Suppression raises the Hammer's ally-hazard Decrease Damage Given to 40% for allies standing in the circle as well as enemies.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Hour of the Ox | Foundation | None | +2% Increase Damage Given (self buff); +2% Decrease Damage Taken (self buff) | Otherworldly Conduit / 2 |
| 02 | Hungry Ghost's Draught | Hidden Art | Hour of the Ox | +2% Lifesteal (self buff) | Otherworldly Conduit / 1 |
| 03 | Feast of a Thousand Mouths | Advanced Art | Hungry Ghost's Draught | +3% Lifesteal (self buff); +3% Increase Damage Given (self buff) | Otherworldly Conduit / 2 |
| 04 | Hide of the Oni | Hidden Art | Hour of the Ox | +3% Decrease Damage Taken (self buff) | Otherworldly Conduit / 1 |
| 05 | Barred Gate of Yomi | Advanced Art | Hide of the Oni | +5% Decrease Damage Taken (self buff) | Otherworldly Conduit / 1 |
| 06 | Oni's Heavy Hand | Foundation | None | +2% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Herald of the Black Night, Oni Hammer Swing / 2 |
| 09 | Marked by the Herald | Hidden Art | Oni's Heavy Hand | +3% Increase Damage Taken (enemy debuff) | Herald of the Black Night / 1 |
| 08 | March of a Thousand Demons | Advanced Art | Marked by the Herald | +2 Damage (damage) | Oni Hammer Swing, Possessing Yurei / 2 |
| 07 | Dread of the Procession | Hidden Art | Oni's Heavy Hand | +3% Decrease Damage Given (enemy debuff) | Oni Hammer Swing / 1 |
| 10 | Toll of the Night Bell | Advanced Art | Dread of the Procession | +5% Decrease Damage Given (enemy debuff) | Oni Hammer Swing / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→09, 09→08, 06→07, 07→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Hour of the Ox** — At the hour of the ox the veil thins, and what crosses it walks beside you. Otherworldly Conduit self buffs: Increase Damage Given 35 → 37%, Decrease Damage Taken 35 → 37%; one 40 AP self cast, 2 rounds, non-pierce hits.
- **Hungry Ghost's Draught** — The hungry dead drink what you spill, and leave a share for the one who opened the way. Otherworldly Conduit Lifesteal only, 40 → 42%: a share of every hit you land (pierce included) for 2 rounds; 60% leech cap shared with vamp. The Sustain route's setup; Lifesteal appears on no other route.
- **Feast of a Thousand Mouths** — A thousand mouths at the table, and every one of them feeds you. Sustain offense: Conduit Lifesteal 40 → 45% on the full route (the +5% hard ceiling, inside the 60% leech budget) and Increase Damage Given 35 → 40% with Hour of the Ox; same 40 AP cast.
- **Hide of the Oni** — An oni's hide turns the blade that would have split a lesser thing. Otherworldly Conduit Decrease Damage Taken only: 37 → 40% with Hour of the Ox; every non-pierce hit of any stat type, 2 rounds per 40 AP cast.
- **Barred Gate of Yomi** — Yomi's gate is barred from the inside; what stands behind it does not come to harm. Fortress: Conduit Decrease Damage Taken 35 → 45% on the full route, against every non-pierce hit for the 2 rounds after one 40 AP self cast. No Lifesteal: that belongs to Feast of a Thousand Mouths.
- **Oni's Heavy Hand** — The oni does not lift the hammer. The hammer lifts the oni, and comes down. Oni Hammer Swing Decrease Damage Given 30 → 32% on its radius-1 circle (allies too); Herald of the Black Night exposure 35 → 37% on its circle (enemies only).
- **Marked by the Herald** — The herald names you to the parade, and the parade remembers. Burst setup for March's +2 Damage: Herald of the Black Night exposure 37 → 40% with Oni's Heavy Hand (one row, ×1.037 over the kit's 35%; radius-1 circle at range 5, enemies only, 40 AP, 2 rounds).
- **March of a Thousand Demons** — The lanterns bob, the drums roll, and the whole procession walks over you. Burst payoff: Possessing Yurei (single target) and Oni Hammer Swing (radius-1 circle) Shadow Damage 45 → 47 EP, still High tier; Herald exposure 40% on the full route.
- **Dread of the Procession** — Those who watch the parade pass find their arms too heavy to lift. Oni Hammer Swing Decrease Damage Given 32 → 35% with Oni's Heavy Hand, on everyone in its radius-1 circle (allies too), for 2 rounds.
- **Toll of the Night Bell** — When the night bell tolls, every hand raised against the procession falters. Suppression: Oni Hammer Swing Decrease Damage Given 30 → 40% on the full route, on everyone in its radius-1 circle (allies too) for 2 rounds; a suppressed enemy's hits are cut ×0.60 against the whole team.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Feast of a Thousand Mouths (Sustain offense) | Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Hide of the Oni | — | +5% | — | — | +5% | +5% |
| Barred Gate of Yomi (Fortress) | Hour of the Ox, Hide of the Oni, Barred Gate of Yomi, Oni's Heavy Hand | — | +2% | +2% | +2% | +10% | — |
| March of a Thousand Demons (Burst) | Oni's Heavy Hand, Marked by the Herald, March of a Thousand Demons, Hour of the Ox | +2 | +2% | +2% | +5% | +2% | — |
| Toll of the Night Bell (Suppression) | Oni's Heavy Hand, Dread of the Procession, Toll of the Night Bell, Marked by the Herald | — | — | +10% | +5% | — | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Feast of a Thousand Mouths:** One 40 AP Conduit cast carries the route: Lifesteal 45% (+5%, the hard ceiling, inside the 60% leech budget shared with vamp) and Increase Damage Given 40% for the 2 rounds after the cast, so every hit lands harder and heals more. Hide of the Oni is the realistic fourth (Decrease Damage Taken 40% on the same cast); Oni's Heavy Hand (01, 02, 03, 06) trades it for 32% Hammer suppression and 37% Herald exposure. No other allocation passes 42% Lifesteal.
- **Barred Gate of Yomi:** Decrease Damage Taken on the Conduit reaches 45% (+10%) against every non-pierce hit for the 2 rounds after the cast, with Increase Damage Given 37%; Lifesteal stays at 40%. Oni's Heavy Hand is the realistic fourth: a hit from an enemy under the 32% Hammer suppression is cut ×0.68 × 0.55 ≈ ×0.37, and the Herald exposes at 37%. Hungry Ghost's Draught (01, 02, 04, 05) adds only Lifesteal 42%, so the fortress does not take over the Sustain route.
- **March of a Thousand Demons:** Mark, then crush: the Herald exposes every enemy in its circle at 40% for 2 rounds, and Possessing Yurei and Oni Hammer Swing land at 47 EP (+2, still High tier; ×1.044 per hit, since formula damage is linear in EP). On a marked target inside the Conduit window the jutsu modifiers compound ×1.40 × 1.37 ≈ ×1.92 (×2.00 with the +2 EP) before the bloodline passive multiplies last. Hour of the Ox is the realistic fourth for that frame (37% given, 37% taken); Dread of the Procession (06, 07, 08, 09) adds 35% Hammer suppression instead.
- **Toll of the Night Bell:** Oni Hammer Swing's suppression reaches 40% (+10%) on everyone in its circle for 2 rounds, allies included, so a suppressed enemy's hits are cut ×0.60 against the whole team. Marked by the Herald is the fourth that works both sides of the exchange (Herald exposure 40%, Burst's full setup). Hour of the Ox (01, 06, 07, 10) adds the Conduit instead (37% given and taken): a suppressed enemy's hit inside the Conduit window is cut ×0.60 × 0.63 ≈ ×0.38.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustain offense | Fortress | Burst | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Possessing Yurei | 0 | Damage | enemy | 45 | 45 | 45 | 47 (+2) | 45 |
| Possessing Yurei | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Oni Hammer Swing | 0 | Damage | enemy | 45 | 45 | 45 | 47 (+2) | 45 |
| Oni Hammer Swing | 1 | Decrease Damage Given | enemy | 30% | 30% | 32% (+2) | 32% (+2) | 40% (+10) |
| Otherworldly Conduit | 0 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 37% (+2) | 35% |
| Otherworldly Conduit | 1 | Decrease Damage Taken | self | 35% | 40% (+5) | 45% (+10) | 37% (+2) | 35% |
| Otherworldly Conduit | 2 | Lifesteal | self | 40% | 45% (+5) | 40% | 40% | 40% |
| Summoning: Underworld Gate | 0 | summon (unsupported) | self | 100% | 100% | 100% | 100% | 100% |
| Herald of the Black Night | 0 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Herald of the Black Night | 1 | Increase Damage Taken | enemy | 35% | 35% | 37% (+2) | 40% (+5) | 40% (+5) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Feast of a Thousand Mouths: +5% Lifesteal (0 + 2 + 3; on band)
  - Route Barred Gate of Yomi: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route March of a Thousand Demons: +2 Damage (0 + 0 + 2; off band)
  - Route Toll of the Night Bell: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 7 (DMG 2, DDG 1, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Oni's Heavy Hand (raw +16, row-weighted 16)
- Lowest row-weighted node: Hungry Ghost's Draught (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Oni Hammer Swing#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Possessing Yurei | 0 | 45 (High) | 47 (High) |
| Oni Hammer Swing | 0 | 45 (High) | 47 (High) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Feast of a Thousand Mouths | +5% IDG, +2% DDT, +5% LS | Hide of the Oni | +5% IDG, +5% DDT, +5% LS | 15 |
| Feast of a Thousand Mouths | +5% IDG, +2% DDT, +5% LS | Oni's Heavy Hand *(highest diagnostic)* | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +5% LS | 16 |
| Barred Gate of Yomi | +2% IDG, +10% DDT | Hungry Ghost's Draught | +2% IDG, +10% DDT, +2% LS | 14 |
| Barred Gate of Yomi | +2% IDG, +10% DDT | Oni's Heavy Hand *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% DDT | 16 |
| March of a Thousand Demons | +2 Damage, +2% DDG, +5% IDT | Hour of the Ox *(highest diagnostic)* | +2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT | 15 |
| March of a Thousand Demons | +2 Damage, +2% DDG, +5% IDT | Dread of the Procession | +2 Damage, +5% DDG, +5% IDT | 14 |
| Toll of the Night Bell | +10% DDG, +2% IDT | Hour of the Ox *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +2% DDT | 16 |
| Toll of the Night Bell | +10% DDG, +2% IDT | Marked by the Herald | +10% DDG, +5% IDT | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Hide of the Oni | +5% IDG, +5% DDT, +5% LS |
| 2 | Hour of the Ox, Hungry Ghost's Draught, Feast of a Thousand Mouths, Oni's Heavy Hand | +5% IDG, +2% DDG, +2% IDT, +2% DDT, +5% LS |
| 3 | Hour of the Ox, Hungry Ghost's Draught, Hide of the Oni, Barred Gate of Yomi | +2% IDG, +10% DDT, +2% LS |
| 4 | Hour of the Ox, Hungry Ghost's Draught, Hide of the Oni, Oni's Heavy Hand | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +2% LS |
| 5 | Hour of the Ox, Hungry Ghost's Draught, Oni's Heavy Hand, Dread of the Procession | +2% IDG, +5% DDG, +2% IDT, +2% DDT, +2% LS |
| 6 | Hour of the Ox, Hungry Ghost's Draught, Oni's Heavy Hand, Marked by the Herald | +2% IDG, +2% DDG, +5% IDT, +2% DDT, +2% LS |
| 7 | Hour of the Ox, Hide of the Oni, Barred Gate of Yomi, Oni's Heavy Hand | +2% IDG, +2% DDG, +2% IDT, +10% DDT |
| 8 | Hour of the Ox, Hide of the Oni, Oni's Heavy Hand, Dread of the Procession | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 9 | Hour of the Ox, Hide of the Oni, Oni's Heavy Hand, Marked by the Herald | +2% IDG, +2% DDG, +5% IDT, +5% DDT |
| 10 | Hour of the Ox, Oni's Heavy Hand, Dread of the Procession, Marked by the Herald | +2% IDG, +5% DDG, +5% IDT, +2% DDT |
| 11 | Hour of the Ox, Oni's Heavy Hand, Dread of the Procession, Toll of the Night Bell | +2% IDG, +10% DDG, +2% IDT, +2% DDT |
| 12 | Hour of the Ox, Oni's Heavy Hand, March of a Thousand Demons, Marked by the Herald | +2 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT |
| 13 | Oni's Heavy Hand, Dread of the Procession, March of a Thousand Demons, Marked by the Herald | +2 Damage, +5% DDG, +5% IDT |
| 14 | Oni's Heavy Hand, Dread of the Procession, Marked by the Herald, Toll of the Night Bell | +10% DDG, +5% IDT |

## Design notes

- Node split: two roots, four Hidden Arts, four Advanced Arts, every capstone 3 BP deep, two capstones 5 BP under one root or 6 across roots. Hour of the Ox (+2% Increase Damage Given, +2% Decrease Damage Taken on the Conduit) forks into Sustain offense (Hungry Ghost's Draught +2% Lifesteal → Feast of a Thousand Mouths +3% Lifesteal, +3% Increase Damage Given) and Fortress (Hide of the Oni +3% Decrease Damage Taken → Barred Gate of Yomi +5% Decrease Damage Taken). Oni's Heavy Hand (+2% Decrease Damage Given on the Hammer, +2% Increase Damage Taken on the Herald) forks into Burst (Marked by the Herald +3% Increase Damage Taken → March of a Thousand Demons +2 Damage) and Suppression (Dread of the Procession +3% Decrease Damage Given → Toll of the Night Bell +5% Decrease Damage Given). Root A touches only Conduit rows; root B only the two hits, the Hammer's suppression and the Herald's exposure.
- 2026-10-04 rebalance. Root B: the old Burst route (Grip of the Yurei +2, March +3 Damage) lifted both 45 EP hits to 50, turning two semi-nukes into nukes, and put flat Damage on a Hidden Art. March is now the only Damage node (+2, 45 → 47, no tier change) and pays off the exposure that Marked by the Herald sets up. The old Pressure route (Marked by the Herald → Toll, +10% Increase Damage Taken) is gone: the Herald is root B's only percentage row besides the Hammer's suppression, so Marked became Burst's +3% setup (route 35 → 40%, ×1.037) rather than a twin Hidden Art on the same row; Grip of the Yurei is renamed Dread of the Procession and leads Suppression. After review, Barred Gate of Yomi lost its +2% Lifesteal rider (with Hungry Ghost's Draught the Fortress fourth reached 44% Lifesteal and out-sustained Feast) and Toll of the Night Bell lost its +2% Conduit Decrease Damage Taken rider (it did not answer root B's sentence and pulled Suppression toward Fortress). Roster pass: checked against the roster conventions with no value or structure change. The kit's two Damage rows are 45 EP, and March's +2 (45 → 47, Arashima's High-tier value) is already the controlled payoff after a percentage setup. Final cleanup: prose only; Marked's +3% is justified by its setup role, and exposure is stated by compounded factor (×1.037 against Shakunetsu Sakura ×1.075 and Blood-Enchanted Eyes ×1.115).
- Maxima over every legal allocation: Damage +2 (March only); Lifesteal +5% (Feast route only; any other allocation reaches +2% at most, Hungry Ghost's Draught); Decrease Damage Taken +10% (Fortress only; +5% elsewhere at most, Hour of the Ox with Hide of the Oni); Decrease Damage Given +10% (Suppression only); Increase Damage Given +5%; Increase Damage Taken +5%. Top offensive package (Increase Damage Given × Taken, all windows live): ×1.052 (Burst with Hour of the Ox, or Feast with Oni's Heavy Hand), under Blood-Enchanted Eyes' ×1.234.
- Fourth purchases: Sustain offense takes Hide of the Oni (40% given, 40% taken, 45% Lifesteal) or Oni's Heavy Hand. Fortress takes Oni's Heavy Hand (32% suppression, 37% exposure) or Hungry Ghost's Draught (42% Lifesteal). In an even trade of raw damage D, Feast with Hide heals 0.45 × 1.40D ≈ 0.63D and takes 0.60D; Fortress with Hungry Ghost's Draught heals 0.42 × 1.37D ≈ 0.58D and takes 0.55D, so Feast nets more while trading and Fortress wins once incoming raw damage passes about 1.1× outgoing. Burst takes Hour of the Ox (Conduit 37% given / taken) or Dread of the Procession (35% suppression). Suppression takes Marked by the Herald (40% exposure, Burst's whole setup) or Hour of the Ox (Conduit 37% given / taken). Three capstones carry one tag each and Feast's Increase Damage Given rider stacks only with its own Foundation, so no fourth carries a tag past its own route.
- Interactions: every non-damage supported row is element-less and lists all four stat types, so at the pin the Conduit's buffs, the Herald's exposure and the Hammer's suppression match every non-pierce hit of any stat type (Lifesteal also counts pierce). Formula damage is linear in EP (tags.ts powerEffect), so +2 EP is ×47/45 ≈ ×1.044 on each 45 EP hit; the sqrt scaling applies to stats, not EP. Jutsu Increase Damage Given and Increase Damage Taken compound (×1.40 × 1.37 ≈ ×1.92 on a marked target in the Burst build with Hour of the Ox); Decrease Damage Given and Decrease Damage Taken apply in sequence. The bloodline passive (Increase Damage Given 25% + 0.15/level) is not a potency target and multiplies last.
- Delivery and uptime: the Conduit is a SELF cast realized on the caster at cast time; 40 AP, cooldown 7, live for the 2 rounds after the cast. Herald of the Black Night (OTHER_USER, AOE_CIRCLE_SPAWN radius 1, range 5, 40 AP, cooldown 7) exposes each living enemy on the tiles; the caster is never a target. Oni Hammer Swing (OPPONENT, same method, range 4, 60 AP, cooldown 7) damages enemies only; its Decrease Damage Given rider (friendly fire none) reaches allies on the tiles too.

## Risks and unproven interactions

- Classification: Shadow is shared with other bloodlines (expected under RUL-2026-10-03-005). 2 of 7 kit rows carry Shadow; Otherworldly Conduit, Herald of the Black Night and Summoning: Underworld Gate carry no element on any row, so in-kit they qualify only through an authored Shadow jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Shadow coverage is unverified; March's +2 would lift any off-kit 50 EP Shadow row to 52.
- Ally hazard: Oni Hammer Swing row 1 (Decrease Damage Given 30%) is an INHERIT row on an OPPONENT AOE_CIRCLE_SPAWN with friendly fire none, so allies on the radius-1 tiles around the target receive it too; the caster never does. Oni's Heavy Hand gives 32%, Dread of the Procession 35%, and the full Suppression route 40% for allies and enemies alike. Positioning decides; solo it is pure gain.
- Increase Damage Taken reach: the Herald's exposure applies to every non-pierce hit an exposed enemy takes for 2 rounds (allies, weapons, normal jutsu, the Underworld Gate summon), and one cast can expose several enemies. The tree has no dedicated exposure route: Oni's Heavy Hand gives +2% and Marked by the Herald, Burst's setup, +3%, so Herald reaches 35 → 40% at most (×1.037) in any allocation that holds both, Burst capstone or not.
- Lifesteal budget: the 60%-of-pre-shield-damage leech cap is shared with vamp, so Feast's 45% leaves 15 points of headroom. healprevent on the caster blocks it; the kit applies none.
- Realized value: the four supported-row jutsu share cooldown 7 (the Underworld Gate summon is 10) and both damage casts cost 60 AP, so one rotation rarely fits the Conduit window, the Herald's exposure and both hits. Buffs and debuffs act only in the rounds after their cast round (SOURCE_MECHANICS §3b). Formula damage is linear in EP (powerEffect), so March's +2 is ×1.044 on each 45 EP hit before Increase Damage Given / Taken and the passive multiply it; the sqrt applies to stats, not EP. Nothing was simulated.
- Unsupported rows and modes: Possessing Yurei's stun, Herald of the Black Night's buffprevent (itself an ally-hazard row) and the Underworld Gate summon receive nothing. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING.

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

