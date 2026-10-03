# Cosmic Ascendant — Weight of the Stars

**Bloodline:** Cosmic Ascendant (BR-018, rank S, `osVXxtyW61gr-bx5v5ys2`) · **Revision:** Draft 4 / Cosmic Ascendant classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Cosmic Ascendant (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Exposure into burst: Increase Damage Taken (2 rows, up to +5%) feeding Cosmic Explosion Damage (1 row, +5) · secondary Decrease Damage Taken (Defensive; 3 rows on Cosmic Chains, Cosmic Energy and Cosmic Aura; +10%) · tertiary Cosmic Intent's Afterburn (+10%) and Lifesteal (+5%) as rival Advanced Arts; Increase Damage Given (+5%) and Decrease Damage Given (+7%) as glue.

Cosmic Ascendant is a rank S kit tagged Burst and Defensive with 10 supported rows on five jutsu. Its only Damage row is Cosmic Explosion (50 EP at level 25, 60 AP), so burst here is exposure first: Cosmic Intent and Cosmic Chains each carry a 35% Increase Damage Taken row that lists all four stat types with no element and therefore amplifies every non-pierce hit the target takes. Decrease Damage Taken sits on three separate 40 AP jutsu (Chains 35%, Energy 35%, Aura 30%, all 2 rounds on a 7-round cooldown), which is the broadest tag in the kit and the Defensive trait's engine. Cosmic Intent is the signature A-rank cast (Increase Damage Taken 35%, Afterburn 35%, Lifesteal 40% in one 40 AP action), so its burn and its leech are offered as two rival Advanced Arts a player cannot own together.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Cosmic Ascendant-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Celestial Alignment | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Cosmic Chains, Cosmic Energy, Cosmic Intent / 3 |
| 02 | Collapsing Star | Hidden Art | Celestial Alignment | +2 Damage (damage) | Cosmic Explosion / 1 |
| 03 | Supernova Unbound | Advanced Art | Collapsing Star | +3 Damage (damage); +3% Increase Damage Taken (enemy debuff) | Cosmic Chains, Cosmic Explosion, Cosmic Intent / 3 |
| 04 | Searing Starlight | Hidden Art | Celestial Alignment | +3% Afterburn (enemy debuff) | Cosmic Intent / 1 |
| 05 | Light of Dead Stars | Advanced Art | Searing Starlight | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Cosmic Chains, Cosmic Intent / 3 |
| 06 | Gravity Well | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 4 |
| 07 | Event Horizon | Hidden Art | Gravity Well | +3% Decrease Damage Taken (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 3 |
| 08 | Heart of the Singularity | Advanced Art | Event Horizon | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 4 |
| 09 | Stellar Siphon | Hidden Art | Gravity Well | +2% Lifesteal (self buff) | Cosmic Intent / 1 |
| 10 | Hunger of the Void | Advanced Art | Stellar Siphon | +3% Lifesteal (self buff); +5% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Intent / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Celestial Alignment** — When the stars fall into line, the enemy is laid bare and the ascendant burns brighter. Increase Damage Taken 35 → 37% on Cosmic Intent and Cosmic Chains (enemy, 2 rounds, 40 AP); Increase Damage Given 35 → 37% on Cosmic Energy (self buff at cast time).
- **Collapsing Star** — A star does not go quietly. It folds inward, and the folding is the first blow. Cosmic Explosion Damage 50 → 52 EP (60 AP, range 4, single target); its Wound row is unsupported and unchanged.
- **Supernova Unbound** — What was held inside the star is held no longer. Damage route total +5: Cosmic Explosion 50 → 55 EP; Increase Damage Taken on Cosmic Intent and Cosmic Chains 40% with Celestial Alignment.
- **Searing Starlight** — Starlight is old fire. It keeps burning long after it has arrived. Cosmic Intent Afterburn 35 → 38% (enemy, 2 rounds, 40 AP, range 5); every non-pierce hit that target takes feeds it.
- **Light of Dead Stars** — The star is gone. Its light still reaches you, and it still burns. Afterburn route total +10% (Cosmic Intent 35 → 45%, 60% per-hit cap); Increase Damage Taken on Intent and Chains 40% with Celestial Alignment.
- **Gravity Well** — Everything thrown at the ascendant bends, slows, and arrives lighter than it left. Decrease Damage Taken 35 → 37% on Cosmic Chains and Cosmic Energy, 30 → 32% on Cosmic Aura (self, 2 rounds); Decrease Damage Given on Aura 30 → 32% (enemy).
- **Event Horizon** — Past this line, nothing reaches the center whole. Decrease Damage Taken on Chains and Energy 40%, Aura 35% with Gravity Well; all three are cast-time self buffs (2 rounds, 40 AP).
- **Heart of the Singularity** — At the center nothing escapes, and everything that falls in becomes more force. Decrease Damage Taken route total +10%: Chains and Energy 35 → 45%, Aura 30 → 40%; Increase Damage Given on Cosmic Energy 40% with Celestial Alignment.
- **Stellar Siphon** — The ascendant drinks the light it tears loose. Cosmic Intent Lifesteal 40 → 42% (self, 2 rounds, 40 AP); shares the 60% leech cap with vamp; pierce hits count.
- **Hunger of the Void** — The void is not empty. It is hungry, and it is patient. Lifesteal route total +5% (Cosmic Intent 40 → 45%, the hard ceiling); Decrease Damage Given on Cosmic Aura 37% with Gravity Well.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Supernova Unbound (Burst) | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +5 | +2% | +2% | +5% | +2% | — | — |
| Light of Dead Stars (Burn pressure) | Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well | — | +2% | +2% | +5% | +2% | +10% | — |
| Heart of the Singularity (Fortress) | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | — | +5% | +2% | +2% | +10% | — | — |
| Hunger of the Void (Sustain) | Celestial Alignment, Gravity Well, Stellar Siphon, Hunger of the Void | — | +2% | +7% | +2% | +2% | — | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Supernova Unbound:** +5 Damage takes Cosmic Explosion from 50 to 55 EP (60 AP, the kit's only Damage row), and Celestial Alignment plus the Advanced Art's +3% put Increase Damage Taken on Cosmic Intent and Cosmic Chains at 40%, so an Explosion cast in a round after either 40 AP opener lands into that exposure; the bloodline's own Increase Damage Given passive (25% + 0.15/level across Earth, Fire, Lightning, None and Wind) multiplies the enhanced hit downstream. Gravity Well is the fourth purchase for +2% Decrease Damage Taken on three rows and +2% Decrease Damage Given. It is the pure burst option and leaves the burn at 35%, the leech at 40% and mitigation at its lowest.
- **Light of Dead Stars:** Cosmic Intent's Afterburn goes from 35% to 45% for its two rounds, so every non-pierce hit the burning target takes (Cosmic Explosion, weapons, normal jutsu, allies) carries up to 45% extra inside the 60% per-hit cap, and the Advanced Art's +3% Increase Damage Taken with Celestial Alignment takes Intent's and Chains' exposure to 40% as well. Gravity Well rounds it out with +2% Decrease Damage Taken and Decrease Damage Given. This is single-target pressure that follows the one enemy Intent struck; Explosion's EP and the leech are untouched.
- **Heart of the Singularity:** Decrease Damage Taken +10% lifts Cosmic Chains and Cosmic Energy from 35% to 45% and Cosmic Aura from 30% to 40%: three separate 40 AP casts on 7-round cooldowns whose self buffs are realized at cast and live for the two following rounds, so staggered casts cover six rounds in every seven. The Advanced Art's +3% Increase Damage Given with Celestial Alignment takes Energy's self buff to 40% for the same two rounds, wherever its circle is placed. It is the tank who hits harder while guarded: Explosion stays at 50 EP, Afterburn at 35% and Lifesteal at 40%, so it is clearly neither the burst nor the sustain build.
- **Hunger of the Void:** The leech route takes Cosmic Intent's Lifesteal from 40% to 45% (the +5% hard ceiling, fifteen points under the 60% cap shared with vamp) and draws from every damage instance the caster lands during the two rounds after Intent's cast, pierce included, while the Advanced Art's +5% Decrease Damage Given with Gravity Well takes Cosmic Aura's debuff on its target to 37%. Celestial Alignment adds +2% exposure and Increase Damage Given as the fourth purchase. The alternative fourth, Event Horizon instead of Celestial Alignment, is the tank-siphon variant (Decrease Damage Taken 40% / 35%, Decrease Damage Given 37%, no exposure).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Sustain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Cosmic Intent | 0 | Increase Damage Taken | enemy | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 37% (+2) |
| Cosmic Intent | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Cosmic Intent | 2 | Lifesteal | self | 40% | 40% | 40% | 40% | 45% (+5) |
| Cosmic Explosion | 0 | Damage | enemy | 50 | 55 (+5) | 50 | 50 | 50 |
| Cosmic Explosion | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Cosmic Chains | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 37% (+2) |
| Cosmic Chains | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 37% (+2) |
| Cosmic Energy | 0 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 37% (+2) |
| Cosmic Energy | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 37% (+2) |
| Cosmic Energy | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Cosmic Aura | 0 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 37% (+7) |
| Cosmic Aura | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 32% (+2) |
| Cosmic Aura | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +5% Increase Damage Given, +7% Decrease Damage Given, +5% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Supernova Unbound: +5 Damage (0 + 2 + 3; on band)
  - Route Light of Dead Stars: +10% Afterburn (0 + 3 + 7; on band)
  - Route Heart of the Singularity: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Hunger of the Void: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 10 (AB 1, DMG 1, DDG 1, DDT 3, IDG 1, IDT 2, LS 1)
- Strongest full build by row-weighted total: Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity (raw +19, row-weighted 41)
- Lowest row-weighted node: Collapsing Star (2)

Validator warnings:

- classification status: requires classification extension (director decision)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Celestial Alignment, Collapsing Star, Supernova Unbound, Searing Starlight | +5 Damage, +2% IDG, +5% IDT, +3% AB |
| 2 | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +5 Damage, +2% IDG, +2% DDG, +5% IDT, +2% DDT |
| 3 | Celestial Alignment, Collapsing Star, Searing Starlight, Light of Dead Stars | +2 Damage, +2% IDG, +5% IDT, +10% AB |
| 4 | Celestial Alignment, Collapsing Star, Searing Starlight, Gravity Well | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB |
| 5 | Celestial Alignment, Collapsing Star, Gravity Well, Event Horizon | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Celestial Alignment, Collapsing Star, Gravity Well, Stellar Siphon | +2 Damage, +2% IDG, +2% DDG, +2% IDT, +2% DDT, +2% LS |
| 7 | Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well | +2% IDG, +2% DDG, +5% IDT, +2% DDT, +10% AB |
| 8 | Celestial Alignment, Searing Starlight, Gravity Well, Event Horizon | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +3% AB |
| 9 | Celestial Alignment, Searing Starlight, Gravity Well, Stellar Siphon | +2% IDG, +2% DDG, +2% IDT, +2% DDT, +3% AB, +2% LS |
| 10 | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | +5% IDG, +2% DDG, +2% IDT, +10% DDT |
| 11 | Celestial Alignment, Gravity Well, Event Horizon, Stellar Siphon | +2% IDG, +2% DDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Celestial Alignment, Gravity Well, Stellar Siphon, Hunger of the Void | +2% IDG, +7% DDG, +2% IDT, +2% DDT, +5% LS |
| 13 | Gravity Well, Event Horizon, Heart of the Singularity, Stellar Siphon | +3% IDG, +2% DDG, +10% DDT, +2% LS |
| 14 | Gravity Well, Event Horizon, Stellar Siphon, Hunger of the Void | +7% DDG, +5% DDT, +5% LS |

## Design notes

- Reference reuse: topology and both Foundations copy Taiyo Kami (Celestial Alignment = Dawnheart, Gravity Well = Sunward Oath, both +2%/+2%), as do Searing Starlight (+3% Afterburn), the +7% Afterburn Advanced Art, the Hidden +2 / Advanced +3 Damage route and the +2% / +3% / +5% Decrease Damage Taken route. Departures: Supernova Unbound adds +3% Increase Damage Taken; Light of Dead Stars drops Eternal Noon's Increase Damage Given; the fourth route is Lifesteal, as Decrease Damage Given is one Aura row.
- Routes (RUL-2026-10-03-005): Burst +5 Damage on one row (Collapsing Star +2, Supernova Unbound +3); Burn pressure +10% Afterburn (Searing Starlight +3%, Light of Dead Stars +7%); Fortress +10% Decrease Damage Taken on three rows (Gravity Well +2%, Event Horizon +3%, Heart of the Singularity +5%); Sustain +5% Lifesteal (Stellar Siphon +2%, Hunger of the Void +3%) with a +5% Decrease Damage Given secondary. Glue maxima over every legal allocation: Increase Damage Taken +5%, Increase Damage Given +5%, Decrease Damage Given +7%.
- Recalibration: Collapsing Star +3 → +2 Damage (route +6 → +5); Event Horizon +2% → +3% and Heart of the Singularity +2% → +5% Decrease Damage Taken (route +6 → +10%; the earlier three-row discount is superseded); Stellar Siphon +3% → +2% and Hunger of the Void +5% → +3% Lifesteal (route +8% → +5%), with Hunger's Decrease Damage Given +3% → +5% to keep the Sustain route's weight. All 14 legal full builds remain non-dominated.
- Passives and main tree: the bloodline Increase Damage Given passive (Highest; None among its five elements) multiplies the enhanced Explosion downstream. Both Increase Damage Taken rows and the Increase Damage Given row list all four stat types with no element, so they match every element-less hit and elemental hits of any listed stat type: the exposure amplifies allies', weapon and normal-jutsu damage on that enemy; Energy's Increase Damage Given raises the caster's own hits for two rounds. Lifesteal includes pierce; Afterburn and the four damage modifiers skip it.
- Delivery and uptime: all five jutsu have a 7-round cooldown and cost 40 AP except Cosmic Explosion (60 AP, range 4); every buff/debuff row is live the two rounds after its cast round. Cosmic Energy is an EMPTY_GROUND circle, but its Increase Damage Given and Decrease Damage Taken rows are target SELF and land on the caster at cast time wherever the circle is placed; only its unsupported move row is positional (INHERIT ground). Staggered Decrease Damage Taken casts cover six rounds in seven; overlap: Stacking risk. Ranked modes skip skills.
- Fourth-purchase choices: after any 3 BP route the natural fourth is the other Foundation. Unadvertised legal builds include 01+02+04+05 (burn with +2 Damage and 40% exposure, no mitigation), 01+02+03+04 (burst with 38% Afterburn), 06+07+08+09 (pure fortress: Decrease Damage Taken +10%, Increase Damage Given +3%, Lifesteal +2%) and 06+07+09+10 (tank-siphon: Lifesteal +5%, Decrease Damage Given +7%, Decrease Damage Taken +5%). No-Advanced-Art hybrids such as 01+02+06+07 (+2 Damage, +5% Decrease Damage Taken, +2% IDT/IDG/DDG) are legal; all 14 allocations are non-dominated, every node used.
- Four examples: each Advanced Art answers a different role: Damage (Burst), Afterburn (pressure), Decrease Damage Taken (Defensive) and Lifesteal (sustain); the two Cosmic Intent Advanced Arts are rivals.

## Risks and unproven interactions

- Classification: no kit row carries an element, so 'Cosmic Ascendant' is the placeholder name of a new jutsu classification (requires classification extension), not a bloodline-id selector; which jutsu carry it is a director/engine decision. All five kit jutsu qualify only through that authored jutsu classification (ENGINE_GAP_REGISTER G1); targeting None instead would reach every non-elemental row. Off-kit coverage is unverified.
- Exposure breadth: both Increase Damage Taken rows list Bukijutsu, Genjutsu, Ninjutsu and Taijutsu with no element, so getEfficiencyRatio matches essentially every non-pierce hit the target takes from anyone for two rounds. The +5% maximum (40% on two 40 AP casts) is therefore a team-wide amplifier on that enemy. Pierce hits are not amplified by Increase Damage Taken, Decrease Damage Taken, Increase Damage Given or Decrease Damage Given.
- Afterburn: the +10% route is one application row on a single-target 40 AP cast; its value is downstream on every non-pierce hit that one enemy takes for two rounds, capped at 60% of each hit, so other Afterburn sources saturate quickly. The kit has only one Damage row of its own to feed it (Cosmic Explosion); the rest comes from weapons, normal jutsu and allies. Not simulated.
- Lifesteal: the route tops out at 45%, fifteen points under the 60%-of-pre-shield-damage leech budget shared with vamp; vamp from the normal tree or items can saturate the cap. It needs both combatants alive and is blocked by healprevent on the caster. In-kit feed is Cosmic Explosion alone; the rest is normal jutsu, weapons and basic attacks, pierce included.
- Delivery: Cosmic Energy's Increase Damage Given and Decrease Damage Taken are SELF rows realized on the caster at cast time (actions.ts 980-1004), in the circle or not; only its unsupported move row is an INHERIT ground effect (enemy hazard). Chains and Aura are OTHER_USER casts: their self Decrease Damage Taken needs a living non-caster target in range 4; aimed at an ally, their Increase Damage Taken or Decrease Damage Given lands on that ally (§3b). No ally-hazard rows.
- Stacking: same-tag effects all apply (process.ts 1109-1117); at the pin the damage pipeline compounds jutsu IDG/IDT/DDG/DDT (process.ts 469, 1732-1767; tags.ts adjusters only log, 478-540). Two Increase Damage Taken rows at 40%: x1.96 (base x1.82). Chains+Energy in one round (80 of 100 AP, util.ts 2520), Aura the next: all three Decrease Damage Taken rows live, x0.55x0.55x0.60=0.18 at the +10% route maximum (base 0.30), under the 90% reduction cap (constants.ts 3096).
- Row weight: Fortress (41) leads Burn pressure (30), Burst (25) and Sustain (24) because Decrease Damage Taken sits on three casts; those casts are usually staggered for uptime rather than stacked, so row weight overstates it. If the director wants closer parity, Heart of the Singularity's +3% Increase Damage Given secondary is the first trim.
- No combat simulation: non-dominance of the 14 allocations and row-weighted totals are per-row arithmetic, not evidence of equal combat strength. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No adverse, hidden, gated or injected rows.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Cosmic Ascendant-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

