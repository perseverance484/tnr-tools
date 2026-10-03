# Cosmic Ascendant — Weight of the Stars

**Bloodline:** Cosmic Ascendant (BR-018, rank S, `osVXxtyW61gr-bx5v5ys2`) · **Revision:** Draft 3 / Cosmic Ascendant classification / forked tree · **Classification:** Cosmic Ascendant (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Exposure into burst: Increase Damage Taken (2 rows, +5 ceiling) feeding Cosmic Explosion Damage (1 row, +6 ceiling) · secondary Decrease Damage Taken (Defensive; 3 rows on Cosmic Chains, Cosmic Energy and Cosmic Aura; +6 ceiling) · tertiary Cosmic Intent's Afterburn (+10 ceiling) and Lifesteal (+8 ceiling) as rival capstones; Increase Damage Given (+5) and Decrease Damage Given (+5) as glue.

Cosmic Ascendant is a rank S kit tagged Burst and Defensive with 10 supported rows on five jutsu. Its only Damage row is Cosmic Explosion (50 at level 25, 60 AP), so burst here is exposure first: Cosmic Intent and Cosmic Chains each carry a 35% Increase Damage Taken row that lists all four stat types with no element and therefore amplifies every non-pierce hit the target takes. Decrease Damage Taken sits on three separate 40 AP jutsu (Chains 35%, Energy 35%, Aura 30%, all 2 rounds on a 7-round cooldown), which is the broadest tag in the kit and the Defensive trait's engine. Cosmic Intent is the signature A-rank cast (IDT 35%, Afterburn 35%, Lifesteal 40% in one 40 AP action), so its burn and its leech are offered as two rival capstones a player cannot own together.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Cosmic Ascendant jutsu (bloodline-keyed classification, proposed extension) under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Celestial Alignment | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Increase Damage Given (self buff) | Cosmic Chains, Cosmic Energy, Cosmic Intent / 3 |
| 02 | Collapsing Star | Hidden Art | Celestial Alignment | +3 Damage power (damage) | Cosmic Explosion / 1 |
| 03 | Supernova Unbound | Advanced Art | Collapsing Star | +3 Damage power (damage); +3% Increase Damage Taken (enemy debuff) | Cosmic Chains, Cosmic Explosion, Cosmic Intent / 3 |
| 04 | Searing Starlight | Hidden Art | Celestial Alignment | +3% Afterburn (enemy debuff) | Cosmic Intent / 1 |
| 05 | Light of Dead Stars | Advanced Art | Searing Starlight | +7% Afterburn (enemy debuff); +3% Increase Damage Taken (enemy debuff) | Cosmic Chains, Cosmic Intent / 3 |
| 06 | Gravity Well | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 4 |
| 07 | Event Horizon | Hidden Art | Gravity Well | +2% Decrease Damage Taken (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 3 |
| 08 | Heart of the Singularity | Advanced Art | Event Horizon | +2% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Cosmic Aura, Cosmic Chains, Cosmic Energy / 4 |
| 09 | Stellar Siphon | Hidden Art | Gravity Well | +3% Lifesteal (self buff) | Cosmic Intent / 1 |
| 10 | Hunger of the Void | Advanced Art | Stellar Siphon | +5% Lifesteal (self buff); +3% Decrease Damage Given (enemy debuff) | Cosmic Aura, Cosmic Intent / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Celestial Alignment** — When the stars fall into line, the enemy is laid bare and the ascendant burns brighter. IDT 35% -> 37% on Cosmic Intent and Cosmic Chains (enemy, 2 rounds, 40 AP); IDG 35% -> 37% on Cosmic Energy (self buff at cast time).
- **Collapsing Star** — A star does not go quietly. It folds inward, and the folding is the first blow. Damage on Cosmic Explosion 50 -> 53 (60 AP, range 4, single target); its Wound row is unsupported and unchanged.
- **Supernova Unbound** — What was held inside the star is held no longer. Cosmic Explosion 50 -> 56 on the route; IDT on Cosmic Intent and Cosmic Chains 35% -> 40% with Celestial Alignment.
- **Searing Starlight** — Starlight is old fire. It keeps burning long after it has arrived. Cosmic Intent row 1 Afterburn 35% -> 38% (enemy, 2 rounds, 40 AP, range 5); every non-pierce hit that target takes feeds it.
- **Light of Dead Stars** — The star is gone. Its light still reaches you, and it still burns. Cosmic Intent Afterburn 35% -> 45% on the route (60% per-hit cap); IDT on Intent and Chains 35% -> 40% with Celestial Alignment.
- **Gravity Well** — Everything thrown at the ascendant bends, slows, and arrives lighter than it left. DDT 35% -> 37% on Cosmic Chains and Cosmic Energy, 30% -> 32% on Cosmic Aura (self, 2 rounds); DDG on Aura 30% -> 32% (enemy).
- **Event Horizon** — Past this line, nothing reaches the center whole. DDT on Chains and Energy 35% -> 39%, Aura 30% -> 34% with Gravity Well; all three are cast-time self buffs (2 rounds, 40 AP).
- **Heart of the Singularity** — At the center nothing escapes, and everything that falls in becomes more force. DDT on Chains and Energy 35% -> 41%, Aura 30% -> 36% on the route; IDG on Cosmic Energy 35% -> 40% with Celestial Alignment.
- **Stellar Siphon** — The ascendant drinks the light it tears loose. Cosmic Intent row 2 Lifesteal 40% -> 43% (self, 2 rounds, 40 AP); shares the 60% leech cap with vamp; pierce hits count.
- **Hunger of the Void** — The void is not empty. It is hungry, and it is patient. Cosmic Intent Lifesteal 40% -> 48% on the route (60% cap shared with vamp); DDG on Cosmic Aura 30% -> 35% with Gravity Well.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT | AB | LS |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Supernova Unbound (Burst) | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | +6 | +2% | +2% | +5% | +2% | — | — |
| Light of Dead Stars (Burn pressure) | Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well | — | +2% | +2% | +5% | +2% | +10% | — |
| Heart of the Singularity (Fortress) | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | — | +5% | +2% | +2% | +6% | — | — |
| Hunger of the Void (Sustain) | Celestial Alignment, Gravity Well, Stellar Siphon, Hunger of the Void | — | +2% | +5% | +2% | +2% | — | +8% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Supernova Unbound:** Damage +6 takes Cosmic Explosion from 50 to 56 (60 AP, the kit's only damage row) and Celestial Alignment plus the capstone's +3 put Increase Damage Taken on Cosmic Intent and Cosmic Chains at 40%, so an Explosion cast in a round after either 40 AP opener lands into that exposure; the bloodline's own IDG passive (25% + 0.15/level across Earth, Fire, Lightning, None and Wind) multiplies the enhanced hit downstream. Gravity Well is the fourth purchase for 2% DDT on three rows and 2% DDG. It is the pure burst option and leaves the burn at 35%, the leech at 40% and mitigation at its lowest.
- **Light of Dead Stars:** Cosmic Intent's Afterburn goes from 35% to 45% for its two rounds, so every non-pierce hit the burning target takes (Cosmic Explosion, weapons, normal jutsu, allies) carries up to 45% extra inside the 60% per-hit cap, and the capstone's +3 IDT with Celestial Alignment takes Intent's and Chains' exposure to 40% as well. Gravity Well rounds it out with 2% DDT and 2% DDG. This is single-target pressure that follows the one enemy Intent struck; Explosion's raw power and the leech are untouched.
- **Heart of the Singularity:** Decrease Damage Taken +6 lifts Cosmic Chains and Cosmic Energy from 35% to 41% and Cosmic Aura from 30% to 36%: three separate 40 AP casts on 7-round cooldowns whose self buffs are realized at cast and live for the two following rounds, so staggered casts cover six rounds in every seven. The capstone's +3 IDG with Celestial Alignment takes Energy's self IDG to 40% for the same two rounds, wherever its circle is placed. It is the tank who hits harder while guarded: Explosion stays at 50, Afterburn at 35% and Lifesteal at 40%, so it is clearly neither the burst nor the sustain build.
- **Hunger of the Void:** The leech route takes Cosmic Intent's Lifesteal from 40% to 48%, twelve points under the 60% cap shared with vamp, and draws from every damage instance the caster lands during the two rounds after Intent's cast, pierce included, while the capstone's +3 DDG with Gravity Well takes Cosmic Aura's Decrease Damage Given on its target to 35%. Celestial Alignment adds 2% exposure and 2% IDG for the fourth purchase. The alternative fourth, Event Horizon instead of Celestial Alignment, is the tank-siphon variant (DDT 39%/34%, DDG 35%, no exposure).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Burn pressure | Fortress | Sustain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Cosmic Intent | 0 | Increase Damage Taken | enemy | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 37% (+2) |
| Cosmic Intent | 1 | Afterburn | enemy | 35% | 35% | 45% (+10) | 35% | 35% |
| Cosmic Intent | 2 | Lifesteal | self | 40% | 40% | 40% | 40% | 48% (+8) |
| Cosmic Explosion | 0 | Damage | enemy | 50 | 56 (+6) | 50 | 50 | 50 |
| Cosmic Explosion | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |
| Cosmic Chains | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 41% (+6) | 37% (+2) |
| Cosmic Chains | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 37% (+2) |
| Cosmic Energy | 0 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 40% (+5) | 37% (+2) |
| Cosmic Energy | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 41% (+6) | 37% (+2) |
| Cosmic Energy | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Cosmic Aura | 0 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 35% (+5) |
| Cosmic Aura | 1 | Decrease Damage Taken | self | 30% | 32% (+2) | 32% (+2) | 36% (+6) | 32% (+2) |
| Cosmic Aura | 2 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +6, Increase Damage Given +5%, Decrease Damage Given +5%, Increase Damage Taken +5%, Decrease Damage Taken +6%, Afterburn +10%, Lifesteal +8% (not jointly attainable)
- Supported rows in kit: 10 (AB 1, DMG 1, DDG 1, DDT 3, IDG 1, IDT 2, LS 1)
- Strongest full build by row-weighted total: Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well (raw +21, row-weighted 30)
- Lowest row-weighted node: Collapsing Star (3)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Celestial Alignment, Collapsing Star, Supernova Unbound, Searing Starlight | DMG +6, IDG +2, IDT +5, AB +3 |
| 2 | Celestial Alignment, Collapsing Star, Supernova Unbound, Gravity Well | DMG +6, IDG +2, DDG +2, IDT +5, DDT +2 |
| 3 | Celestial Alignment, Collapsing Star, Searing Starlight, Light of Dead Stars | DMG +3, IDG +2, IDT +5, AB +10 |
| 4 | Celestial Alignment, Collapsing Star, Searing Starlight, Gravity Well | DMG +3, IDG +2, DDG +2, IDT +2, DDT +2, AB +3 |
| 5 | Celestial Alignment, Collapsing Star, Gravity Well, Event Horizon | DMG +3, IDG +2, DDG +2, IDT +2, DDT +4 |
| 6 | Celestial Alignment, Collapsing Star, Gravity Well, Stellar Siphon | DMG +3, IDG +2, DDG +2, IDT +2, DDT +2, LS +3 |
| 7 | Celestial Alignment, Searing Starlight, Light of Dead Stars, Gravity Well | IDG +2, DDG +2, IDT +5, DDT +2, AB +10 |
| 8 | Celestial Alignment, Searing Starlight, Gravity Well, Event Horizon | IDG +2, DDG +2, IDT +2, DDT +4, AB +3 |
| 9 | Celestial Alignment, Searing Starlight, Gravity Well, Stellar Siphon | IDG +2, DDG +2, IDT +2, DDT +2, AB +3, LS +3 |
| 10 | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity | IDG +5, DDG +2, IDT +2, DDT +6 |
| 11 | Celestial Alignment, Gravity Well, Event Horizon, Stellar Siphon | IDG +2, DDG +2, IDT +2, DDT +4, LS +3 |
| 12 | Celestial Alignment, Gravity Well, Stellar Siphon, Hunger of the Void | IDG +2, DDG +5, IDT +2, DDT +2, LS +8 |
| 13 | Gravity Well, Event Horizon, Heart of the Singularity, Stellar Siphon | IDG +3, DDG +2, DDT +6, LS +3 |
| 14 | Gravity Well, Event Horizon, Stellar Siphon, Hunger of the Void | DDG +5, DDT +4, LS +8 |

## Design notes

- Reference reuse: topology and both Foundations copy Taiyo Kami (Celestial Alignment = Dawnheart, Gravity Well = Sunward Oath, both +2/+2), as do Searing Starlight (+3 Afterburn) and the +7 Afterburn capstone. Departures: Damage 3/3 on one row (Taiyo 2/3 on three) with +3 IDT on its capstone; Light of Dead Stars drops Eternal Noon's IDG; DDT 2/2/2 on three rows (Taiyo 2/3/5 on one); the fourth route is Lifesteal, as DDG is one Aura row. Same tag families and Burst/Defensive split: the shape fits.
- Calibration: single-row Damage is 3/3 (+6, the guardrail): Cosmic Explosion is the kit's only damage row, where Taiyo's +5 reaches three. Three-row DDT is 2/2/2 (+6), the Tetsugan three-row convention, under Godstorm's two-row +7 and Taiyo's single-row +10; two-row IDT stops at +5. Afterburn 3/7 (+10), Lifesteal 3/5 (+8). Row-weighted: burn 30, fortress 29, burst 26, sustain 25 (Taiyo 31). Burst stays primary: its Damage and team-wide IDT sit at their ceilings, so row weight understates it.
- Passives and main tree: the bloodline IDG passive (Highest; None among its five elements) multiplies the enhanced Explosion downstream. Both IDT rows and the IDG row list all four stat types with no element, so they match every element-less hit and elemental hits of any listed stat type: the exposure amplifies allies', weapon and normal-jutsu damage on that enemy; Energy's IDG raises the caster's own hits for two rounds. Lifesteal includes pierce; Afterburn and the four damage modifiers skip it.
- Delivery and uptime: all five jutsu have a 7-round cooldown and cost 40 AP except Cosmic Explosion (60 AP, range 4); every buff/debuff row is live the two rounds after its cast round. Cosmic Energy is an EMPTY_GROUND circle, but its IDG and DDT rows are target SELF and land on the caster at cast time wherever the circle is placed; only its unsupported move row is positional (INHERIT ground). Staggered DDT casts cover six rounds in seven; overlap: Stacking risk. Ranked modes skip skills.
- Fourth-purchase choices: after any 3 BP route the natural fourth is the other Foundation. Unadvertised legal builds include 01+02+04+05 (burn with +3 Damage and 40% exposure, no mitigation), 01+02+03+04 (burst with 38% Afterburn), 06+07+08+09 (pure fortress: DDT +6, IDG +3, Lifesteal +3) and 06+07+09+10 (tank-siphon: Lifesteal +8, DDG +5, DDT +4). No-capstone hybrids such as 01+02+06+07 (+3 Damage, +4 DDT, +2 IDT/IDG/DDG) are legal; all 14 allocations are non-dominated, every node used.
- Four examples: each capstone answers a different role: Damage (Burst), Afterburn (pressure), DDT (Defensive) and Lifesteal (sustain); the Intent capstones are rivals. User-owned tuning left open: Supernova Unbound +3 vs +2 Damage (route +6 vs +5); Heart of the Singularity ships +2 DDT (three-row route +6), with +3 (route +7) as the explicit upgrade since Energy's DDT is an unconditional self buff; whether Light of Dead Stars should carry IDT given the burst capstone already does.

## Risks and unproven interactions

- Classification: no row in the kit carries an element (every damage, buff and debuff row is element-less), so no existing element can isolate it; a bloodline-keyed classification extension is required, not a bare element label. Targeting 'None' would reach every non-elemental row in the game. Collision with normal jutsu under such a label is unverified (no non-bloodline row catalog).
- Resolver: under the current resolver all 10 supported rows fall back to None; nothing in this tree is reachable exclusively today. The tree assumes the proposed whole-kit classification and the bloodline-keyed label; the engine status is proposal_requires_resolver_adjustment_and_classification_extension.
- Exposure breadth: both IDT rows list Bukijutsu, Genjutsu, Ninjutsu and Taijutsu with no element, so getEfficiencyRatio matches essentially every non-pierce hit the target takes from anyone for two rounds. The +5 ceiling (40% on two 40 AP casts) is therefore a team-wide amplifier, not a bloodline-only one. Pierce hits are not amplified by IDT, DDT, IDG or DDG.
- Afterburn: the +10 route is one application row on a single-target 40 AP cast; its value is downstream on every non-pierce hit that one enemy takes for two rounds, capped at 60% of each hit, so other Afterburn sources saturate quickly. The kit has only one damage row of its own to feed it (Cosmic Explosion); the rest comes from weapons, normal jutsu and allies. Not simulated.
- Lifesteal: the route tops out at 48%, twelve points under the 60%-of-pre-shield-damage leech budget shared with vamp; vamp from the normal tree or items can saturate the cap and waste part of the +8. It needs both combatants alive and is blocked by healprevent on the caster. In-kit feed is Cosmic Explosion alone; the rest is normal jutsu, weapons and basic attacks, pierce included.
- Delivery: Cosmic Energy's IDG and DDT are SELF rows realized on the caster at cast time (actions.ts 980-1004), in the circle or not; only its unsupported move row is an INHERIT ground effect (enemy hazard). Chains and Aura are OTHER_USER casts: their self DDT needs a living non-caster target in range 4; aimed at an ally, their IDT or DDG lands on that ally (§3b). No ally-hazard rows.
- Stacking: same-tag effects all apply (process.ts 1109-1117); at the pin the damage pipeline compounds jutsu IDG/IDT/DDG/DDT (process.ts 469, 1732-1767; tags.ts adjusters only log, 478-540). Two IDT at 40%: x1.96 (base x1.82). Chains+Energy in one round (80 of 100 AP, util.ts 2520), Aura the next: all three DDT live, x0.59x0.59x0.64=0.22 (base 0.30), under the 90% reduction cap (constants.ts 3096).
- No combat simulation: non-dominance of the 14 allocations and row-weighted totals are per-row arithmetic, not evidence of equal combat strength. Collapsing Star reaches one jutsu (Explosion, 60 AP); the Burst example is 26 by row weight, below Burn pressure (30) and Fortress (29), above Sustain (25), so its +6 Damage sits at the guardrail by design. No adverse, hidden, gated or injected rows.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Cosmic Ascendant jutsu inherit Cosmic Ascendant potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

