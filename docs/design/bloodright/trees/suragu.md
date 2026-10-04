# Suragu — Blood of the Caldera

**Bloodline:** Suragu (BR-074, rank A, `Ksb6ogNqc5mp4l_hRgPuW`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Lava classification / forked tree · **Classification:** Lava (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Offense from Magma Vein: a Lava Wave buff window into a narrow +2 Damage burst, or Eruption Strike Afterburn pressure (+10% route) · secondary Survival from Cooling Crust: Lava Wave's Decrease Damage Taken tile (+10% route) or Infernal Stream Lifesteal sustain (+5% ceiling) · tertiary Increase Damage Taken on Blow of Devastation as Foundation glue only (+2%, ×1.015); Increase Damage Given as the Burst setup.

Suragu is a rank A Sustained DPS kit with one supported row per percentage tag and two Lava Damage rows (Infernal Stream 40, Magma Slayer 45 in PVP only). Magma Vein answers "How do I win offensively: empower my own Lava strikes or set the enemy burning?": Pyroclastic Surge builds Lava Wave's self buff to 43% and pays off with +2 Damage (Infernal Stream 40 → 42, Magma Slayer 45 → 47; no tier crossing), while The Mountain Wakes takes Eruption Strike's Afterburn to 45%, which every later non-pierce hit on the target feeds. Cooling Crust answers "How do I stay standing in a long fight: harden the crust or drink the flow?": Heart of the Caldera makes Lava Wave a 40% mitigation tile, and Unquenchable Furnace takes Infernal Stream's Lifesteal to the +5% ceiling with a light mitigation rider. Potency reaches matching supported tags on all Lava jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Magma Vein | Foundation | How do I win offensively: empower my own Lava strikes or set the enemy burning? |
| Cooling Crust | Foundation | How do I stay standing in a long fight: harden the crust or drink the flow? |
| Pyroclastic Surge | Advanced Art | burst: self-buff setup on Scalding Tide, controlled +2 Damage payoff on both Lava strikes |
| The Mountain Wakes | Advanced Art | burn pressure: one Eruption makes every later hit on the target burn, allies' included |
| Heart of the Caldera | Advanced Art | fortress: a team mitigation tile |
| Unquenchable Furnace | Advanced Art | sustain: leech and endure |

- Concern: Burst and Burn with their natural fourths are within about 2–3% on the caster's hits while all three windows are live (Burst ahead on Lava strikes, Burn on element-less hits). Burst's edge is the +2 Damage, which needs no window (Infernal Stream 42, Magma Slayer 47 in PVP), and its 43% buff outside Eruption's window; Burn's is the 45% burn on allies' hits and on hits Lava Wave's buff does not match in the 2 rounds after Eruption. Rotation, AP and uptime were not simulated.
- Concern: Only Burst works under the current resolver (Lava Wave's buff row and both Damage rows carry Lava); Burn, Fortress, Sustain and Blow's exposure need the jutsu-classification resolver (G1 for Blow).
- Concern: +2 Damage reaches every Lava Damage row in scope; off-kit Lava jutsu are unverified, so an off-kit 50 EP Lava attack would become 52.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Lava jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Magma Vein | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Blow of Devastation, Lava Wave / 2 |
| 02 | Scalding Tide | Hidden Art | Magma Vein | +3% Increase Damage Given (self buff) | Lava Wave / 1 |
| 03 | Pyroclastic Surge | Advanced Art | Scalding Tide | +3% Increase Damage Given (self buff); +2 Damage (damage) | Infernal Stream, Lava Wave, Magma Slayer / 3 |
| 04 | Clinging Slag | Hidden Art | Magma Vein | +3% Afterburn (enemy debuff) | Eruption Strike / 1 |
| 05 | The Mountain Wakes | Advanced Art | Clinging Slag | +7% Afterburn (enemy debuff) | Eruption Strike / 1 |
| 06 | Cooling Crust | Foundation | None | +2% Decrease Damage Taken (self buff) | Lava Wave / 1 |
| 07 | Igneous Shell | Hidden Art | Cooling Crust | +3% Decrease Damage Taken (self buff) | Lava Wave / 1 |
| 08 | Heart of the Caldera | Advanced Art | Igneous Shell | +5% Decrease Damage Taken (self buff) | Lava Wave / 1 |
| 09 | Molten Draught | Hidden Art | Cooling Crust | +2% Lifesteal (self buff) | Infernal Stream / 1 |
| 10 | Unquenchable Furnace | Advanced Art | Molten Draught | +3% Lifesteal (self buff); +2% Decrease Damage Taken (self buff) | Infernal Stream, Lava Wave / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Magma Vein** — The mountain's blood runs in Suragu veins, and it does not cool. Lava Wave Increase Damage Given 35 → 37% (SELF at cast, live 2 rounds after, not positional); Blow of Devastation exposure 35 → 37% (enemy, 2 rounds).
- **Scalding Tide** — Wade out on the scalding tide, and every blow that follows lands hotter. Lava Wave self buff 37 → 40% with Magma Vein (SELF at cast, live the 2 rounds after; matches Lava, Earth, Fire and element-less hits).
- **Pyroclastic Surge** — The slope gives way and the whole burning hillside comes down at once. Burst: Lava Wave self buff 35 → 43% on the full route; Infernal Stream 40 → 42 and Magma Slayer 45 → 47 EP (PVP only). No tier crossing.
- **Clinging Slag** — Lava does not splash and vanish. It clings, and it keeps burning. Eruption Strike Afterburn 35 → 38% (enemy, 2 rounds after cast; ally hazard in the circle, never the caster); non-pierce hits feed it.
- **The Mountain Wakes** — The ground remembers every eruption. It has been patient long enough. Burn pressure: Eruption Strike Afterburn 35 → 45% on the full route (+10%; 60% per-hit cap), fed by every later non-pierce hit on the target from any source, allies included.
- **Cooling Crust** — Black stone over a red heart: the crust shields, the heat beneath sustains. Lava Wave Decrease Damage Taken 30 → 32% (ground row: self and allies on the circle, from the round after it lands).
- **Igneous Shell** — Stone born of fire turns the blade, the fist and the flame alike. Lava Wave Decrease Damage Taken +3% (35% with Cooling Crust); ground row: self and allies on the circle; move row unchanged.
- **Heart of the Caldera** — Stand where the earth itself is molten, and nothing reaches you unburned. Fortress: Lava Wave Decrease Damage Taken 30 → 40% on the full route (+10%; ground row: self and allies on the circle, from the round after it lands).
- **Molten Draught** — The flow swallows what it touches, and the Suragu grow stronger for it. Infernal Stream Lifesteal 40 → 42% (SELF, 2 rounds after cast, never its own hit); 60% cap shared with vamp; pierce counts.
- **Unquenchable Furnace** — Every wound stoked, every blow fed back into a furnace that never cools. Sustain: Infernal Stream Lifesteal 40 → 45% on the full route (+5%); Lava Wave Decrease Damage Taken +2% (34% with Cooling Crust, 37% with Igneous Shell).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|
| Pyroclastic Surge (Burst) | Magma Vein, Scalding Tide, Pyroclastic Surge, Clinging Slag | +2 | +8% | +2% | — | +3% | — |
| The Mountain Wakes (Burn pressure) | Magma Vein, Clinging Slag, The Mountain Wakes, Scalding Tide | — | +5% | +2% | — | +10% | — |
| Heart of the Caldera (Fortress) | Magma Vein, Cooling Crust, Igneous Shell, Heart of the Caldera | — | +2% | +2% | +10% | — | — |
| Unquenchable Furnace (Sustain) | Magma Vein, Cooling Crust, Molten Draught, Unquenchable Furnace | — | +2% | +2% | +4% | — | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Pyroclastic Surge:** Lava Wave's self buff reaches 43% for the two rounds after its cast, and +2 Damage lands Infernal Stream at 42 and Magma Slayer at 47 EP in PVP (no tier crossing; in PVE only Infernal Stream gains). On a Lava strike inside the window against an enemy under Blow's 37% exposure the two compound (×1.43 × 1.37 ≈ ×1.96), and the bloodline passive multiplies last. Clinging Slag is the strongest fourth (Afterburn 38%); Cooling Crust (Decrease Damage Taken 32%) is the safer one. It gives up the deep burn, the fortress tile and the deep leech.
- **The Mountain Wakes:** Eruption Strike's Afterburn goes from 35% to 45% for the two rounds after its cast, so every non-pierce hit the burning enemy takes then (Infernal Stream, Magma Slayer in PVP, basic attacks, weapons, normal jutsu, allies) adds 45% of its damage, inside the 60% per-hit cap; Eruption Strike's own pierce never feeds it. Scalding Tide is the strongest fourth: on the caster's hits Lava Wave's 40% buff, Blow's 37% exposure and the burn compound (×1.40 × 1.37 × 1.45 ≈ ×2.78). Cooling Crust is the alternative. Damage is untouched, and the burn circle is an ally hazard: allies standing in it also receive the enhanced debuff; the caster never does.
- **Heart of the Caldera:** Lava Wave's ground row goes from 30% to 40% mitigation for the caster and any ally standing in the circle, from the round after it lands and only while on it, so one 40 AP cast becomes a team fortress tile. The capstone carries no offensive rider. Magma Vein is the strongest fourth (Lava Wave's SELF buff 37%, exposure 37%); Molten Draught (Lifesteal 42%) is the sustain-leaning alternative. Afterburn stays at 35%, and Damage is untouched.
- **Unquenchable Furnace:** The Lifesteal route takes Infernal Stream's leech from 40% to 45% (the +5% ceiling), fifteen points under the 60% budget shared with vamp, and draws from every hit the caster lands in the two rounds after the cast (never Infernal Stream's own hit), including Eruption Strike's unsupported 58-power pierce. The capstone's +2% with Cooling Crust leaves Lava Wave at 34% mitigation, and Magma Vein adds a 37% buff and 37% exposure. Igneous Shell instead of Magma Vein is the tank-sustain variant (Decrease Damage Taken 37%, still under the Fortress's 40%). Damage is untouched.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Sustain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Lava Wave | 0 | Increase Damage Given | self | 35% | 43% (+8) | 40% (+5) | 37% (+2) | 37% (+2) |
| Lava Wave | 1 | Decrease Damage Taken | self | 30% | 30% | 30% | 40% (+10) | 34% (+4) |
| Lava Wave | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Blow of Devastation | 0 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Blow of Devastation | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 37% (+2) |
| Eruption Strike | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Eruption Strike | 1 | Afterburn | enemy | 35% | 38% (+3) | 45% (+10) | 35% | 35% |
| Magma Slayer | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Magma Slayer | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Infernal Stream | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Infernal Stream | 1 | Lifesteal | self | 40% | 40% | 40% | 40% | 45% (+5) |
| Infernal Stream | 2 | poison (unsupported) | enemy | 50% | 50% | 50% | 50% | 50% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +8% Increase Damage Given, +2% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Pyroclastic Surge: +8% Increase Damage Given (2 + 3 + 3; off band)
  - Route The Mountain Wakes: +10% Afterburn (0 + 3 + 7; on band)
  - Route Heart of the Caldera: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Unquenchable Furnace: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 7 (AB 1, DMG 2, DDT 1, IDG 1, IDT 1, LS 1)
- Strongest full build by row-weighted total: Magma Vein, Scalding Tide, Clinging Slag, The Mountain Wakes (raw +17, row-weighted 17)
- Lowest row-weighted node: Cooling Crust (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Eruption Strike#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Magma Slayer | 0 | 45 (High) | 47 (High) |
| Infernal Stream | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Pyroclastic Surge | +2 Damage, +8% IDG, +2% IDT | Clinging Slag *(highest diagnostic)* | +2 Damage, +8% IDG, +2% IDT, +3% AB | 17 |
| Pyroclastic Surge | +2 Damage, +8% IDG, +2% IDT | Cooling Crust | +2 Damage, +8% IDG, +2% IDT, +2% DDT | 16 |
| The Mountain Wakes | +2% IDG, +2% IDT, +10% AB | Scalding Tide *(highest diagnostic)* | +5% IDG, +2% IDT, +10% AB | 17 |
| The Mountain Wakes | +2% IDG, +2% IDT, +10% AB | Cooling Crust | +2% IDG, +2% IDT, +2% DDT, +10% AB | 16 |
| Heart of the Caldera | +10% DDT | Magma Vein *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT | 14 |
| Heart of the Caldera | +10% DDT | Molten Draught | +10% DDT, +2% LS | 12 |
| Unquenchable Furnace | +4% DDT, +5% LS | Magma Vein *(highest diagnostic)* | +2% IDG, +2% IDT, +4% DDT, +5% LS | 13 |
| Unquenchable Furnace | +4% DDT, +5% LS | Igneous Shell | +7% DDT, +5% LS | 12 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Magma Vein, Scalding Tide, Pyroclastic Surge, Clinging Slag | +2 Damage, +8% IDG, +2% IDT, +3% AB |
| 2 | Magma Vein, Scalding Tide, Pyroclastic Surge, Cooling Crust | +2 Damage, +8% IDG, +2% IDT, +2% DDT |
| 3 | Magma Vein, Scalding Tide, Clinging Slag, The Mountain Wakes | +5% IDG, +2% IDT, +10% AB |
| 4 | Magma Vein, Scalding Tide, Clinging Slag, Cooling Crust | +5% IDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Magma Vein, Scalding Tide, Cooling Crust, Igneous Shell | +5% IDG, +2% IDT, +5% DDT |
| 6 | Magma Vein, Scalding Tide, Cooling Crust, Molten Draught | +5% IDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust | +2% IDG, +2% IDT, +2% DDT, +10% AB |
| 8 | Magma Vein, Clinging Slag, Cooling Crust, Igneous Shell | +2% IDG, +2% IDT, +5% DDT, +3% AB |
| 9 | Magma Vein, Clinging Slag, Cooling Crust, Molten Draught | +2% IDG, +2% IDT, +2% DDT, +3% AB, +2% LS |
| 10 | Magma Vein, Cooling Crust, Igneous Shell, Heart of the Caldera | +2% IDG, +2% IDT, +10% DDT |
| 11 | Magma Vein, Cooling Crust, Igneous Shell, Molten Draught | +2% IDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Magma Vein, Cooling Crust, Molten Draught, Unquenchable Furnace | +2% IDG, +2% IDT, +4% DDT, +5% LS |
| 13 | Cooling Crust, Igneous Shell, Heart of the Caldera, Molten Draught | +10% DDT, +2% LS |
| 14 | Cooling Crust, Igneous Shell, Molten Draught, Unquenchable Furnace | +7% DDT, +5% LS |

## Design notes

- Structure: two Foundations, each forking into two Hidden → Advanced routes. Magma Vein (Increase Damage Given and Increase Damage Taken glue) holds the offensive pair, Burst (Lava Wave self buff into +2 Damage) and Burn pressure (Afterburn); Cooling Crust (Decrease Damage Taken) holds the survival pair, Fortress (Decrease Damage Taken) and Sustain (Lifesteal). Increase Damage Taken stays Foundation glue at +2% (Blow 35 → 37%, ×1.37/1.35 ≈ ×1.015, under Shakunetsu Sakura's ×1.075): one exposure row, and no route needs more.
- 2026-10-04 rebalance: the Burst route was +5 Damage (Scalding Tide +2, Pyroclastic Surge +3), lifting Infernal Stream 40 → 45 (a whole tier) and Magma Slayer 45 → 50 (semi-nuke to Nuke). Scalding Tide is now a +3% Increase Damage Given setup and Pyroclastic Surge pays off with +3% Increase Damage Given and +2 Damage; its +1% Lifesteal filler left. The Mountain Wakes dropped its +3% Increase Damage Taken and +3% Increase Damage Given riders: with them the burn route compounded three tags (40/40/45%), and with Scalding Tide's old +2 Damage as its fourth it out-damaged the Burst build on every hit, Infernal Stream included. Heart of the Caldera's Increase Damage Given rider went from +3% to +2%. Roster pass: values unchanged. The kit has no 50 EP Damage row, and the Burst route already has the shape of Arashima's Sundered Sky (an Increase Damage Given setup on the Hidden Art, then +3% and +2 Damage on the Advanced Art; 45 → 47). Final cleanup: Heart of the Caldera's +2% Increase Damage Given rider is removed, so the Fortress capstone is single-tag (+5% Decrease Damage Taken) with no offensive rider.
- Fourth-BP audit: Burst's strongest fourth is Clinging Slag (Afterburn 38%) and Burn's is Scalding Tide (Increase Damage Given 40%); each borrows the sibling Hidden Art, so the all-in offensive builds are 43% buff + 38% burn + 2 Damage against 40% buff + 45% burn. With Lava Wave's, Blow's and Eruption's windows all live they are within about 2–3% on the caster's hits: Infernal Stream 42 × 1.43 × 1.37 × 1.38 ≈ 114 against 40 × 1.40 × 1.37 × 1.45 ≈ 111 and Magma Slayer ≈ 127 against 125 favour Burst, while an element-less basic attack (×2.70 against ×2.78) favours Burn. Burst's edge is the +2 Damage, which needs no window (Infernal Stream 42, Magma Slayer 47 in PVP), and its 43% buff outside Eruption's window; Burn's is the 45% burn on allies' hits and on hits Lava Wave's buff does not match in the 2 rounds after Eruption. Fortress's strongest fourth is Magma Vein (buff 37%, exposure 37%) or Molten Draught (Lifesteal 42%); Sustain's is Magma Vein or Igneous Shell (Decrease Damage Taken 37%). Top offensive package: the Burst path (Magma Vein, Scalding Tide, Pyroclastic Surge; no fourth adds to it), Increase Damage Given 35 → 43% and exposure 35 → 37% (×1.059 × 1.015 ≈ ×1.075; ≈ ×1.13 on Infernal Stream with 40 → 42), under Blood-Enchanted Eyes' ×1.234.
- Passives and arithmetic: the bloodline Increase Damage Given passive (25% + 0.15/level on Lava, Earth, Fire, None) multiplies last. Kit Increase Damage Given and Increase Damage Taken rows each multiply a matching hit by 1 + power/100 and compound (Lava Wave 43% with Blow 37%: ×1.43 × 1.37 ≈ ×1.96); Afterburn adds a share of the already-multiplied hit; the Decrease Damage Taken row multiplies matching incoming hits by 1 − power/100. Lava Wave's buff lists Earth, Fire, Lava and None, so it also raises element-less basic attacks and weapons. Lifesteal counts pierce; the rest skip it.
- Delivery and timing: all cooldowns are 7; nothing is item-gated or hidden. Buff/debuff rows act only in the two rounds after their cast round, so no cast benefits from its own row. Lava Wave (40 AP, range 5): its buff is SELF, on the caster at cast wherever they stand; only the Decrease Damage Taken row is a ground effect (INHERIT, FRIENDLY), re-applied each round to the caster and allies on the circle. Others cost 60 AP, Blow 40. Ranked PVP and ranked sparring skip the tree.

## Risks and unproven interactions

- Classification: Lava is the single qualifying element (Magma Slayer and Infernal Stream Damage, Eruption Strike pierce); sharing it with Amaterasu is expected (RUL-2026-10-03-005). 3 of 7 kit rows carry Lava (both Damage rows and Lava Wave's buff), so only the Burst route works under the current resolver; the element-less rows behind Burn, Fortress, Sustain and the exposure glue need the proposed jutsu-classification resolver, and Blow of Devastation qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Lava coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN) is unverified.
- Ally hazard (validator warns): Eruption Strike row 1 Afterburn (AOE_CIRCLE_SPAWN on the enemy, friendly fire none) is raised by Clinging Slag and The Mountain Wakes; allies standing in that circle also receive the enhanced burn, so positioning decides; the caster is never a target of an OTHER_USER circle.
- Mode restriction: Magma Slayer (Damage 45, wound) is PVP-only, so in PVE the +2 Damage reaches only Infernal Stream (40 → 42); the Burst route's 43% buff carries it in that mode.
- Lifesteal: the route tops out at 45% (+5%, the hard ceiling), fifteen points under the 60%-of-pre-shield-damage leech budget shared with vamp; vamp from the normal tree or items can still saturate the cap. It needs both combatants alive and is blocked by healprevent on the caster.
- Afterburn: the +10% route is one application row on a 60 AP cast whose own damage is pierce (58) and never feeds the burn; its value rests on Infernal Stream, Magma Slayer (PVP), weapons, normal jutsu and allies hitting the burning enemy in the two rounds after the cast, capped at 60% of each hit. Not simulated.
- Stacking: BATTLE_TAG_STACKING is true at the pin, so these potency effects stack with other potency sources and same-tag combat effects from other jutsu, recasts or allies all apply (process.ts 1109-1117).
- No combat simulation: non-dominance of the full allocations and the row-weighted totals are arithmetic over per-row additions, not evidence of equal combat strength. Lava Wave's tile uptime, Blow of Devastation's recoil, Magma Slayer's wound, Infernal Stream's poison, Eruption Strike's pierce and AP economy were not modelled.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Lava jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

