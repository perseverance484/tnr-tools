# Itojinsei — The Iron Loom

**Bloodline:** Itojinsei (BR-036, rank A, `j4_9ypNqYq8Ifbqf-9D2r`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Magnet classification / forked tree · **Classification:** Magnet (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Wielder offense (Taut Filament): raw Damage on all four Magnet strikes, or the two compounding self Increase Damage Given buffs (Spiraling Wires, Eternal Embrace) · secondary Binding the target (Tangling Snare): Decrease Damage Given on Wire Blast Plus and Eternal Embrace, or Increase Damage Taken on Lightning Threads · tertiary Mirror riders: each control capstone carries +2% of its sibling's tag.

Nine supported rows sit on five casts, all cooldown 7: four Magnet Bukijutsu Damage rows (Iron Web Entrapment 45; Wire Blast Plus, Spiraling Wires and Lightning Threads 40), two 35% self Increase Damage Given rows (Spiraling Wires, Eternal Embrace) that compound on a hit both cover, two universal Decrease Damage Given rows (Wire Blast Plus 30%, an ally-hazard circle; Eternal Embrace 35%) and one 35% Increase Damage Taken row on Lightning Threads. Taut Filament answers "How do I make my own wires cut harder: a keener strand, or a stronger hand?": Severing Lattice adds a controlled +3 Damage to every Magnet strike with no setup window (no tier crossed), and Weaver Ascendant raises both self buffs to 43%. Tangling Snare answers "How do I bind the target: blunt its blows, or lay it open to ours?": Iron Cocoon takes both suppression rows +10% and Galvanic Marionette takes Lightning Threads' exposure +10%, each with a +2% rider of the other's tag. The kit has no Decrease Damage Taken, Reflect, Lifesteal or Heal row, so there is no self-defensive route. Potency reaches matching supported tags on all Magnet jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Taut Filament | Foundation | How do I make my own wires cut harder: a keener strand, or a stronger hand? |
| Tangling Snare | Foundation | How do I bind the target: blunt its blows, or lay it open to ours? |
| Severing Lattice | Advanced Art | burst: raw Damage on every Magnet strike, every cast, no setup window |
| Weaver Ascendant | Advanced Art | sustained amplification: both self buffs compound on every own hit in the window |
| Iron Cocoon | Advanced Art | suppression: every enemy caught in the circles hits softer, for the whole party |
| Galvanic Marionette | Advanced Art | exposure: one target marked for every attacker |

- Concern: Burst is +3 Damage (+1 Hidden, +2 Advanced) rather than the exemplars' +2 behind a percentage setup: this root's only self tags are Damage and Increase Damage Given, and an Increase Damage Given setup would duplicate Threadbound Vigor. No tier is crossed (40 → 43, 45 → 48); if +2 is wanted as the ceiling, Severing Lattice drops to +1.
- Concern: The control capstones mirror each other's riders (the Iron in the Blood pattern), so with the sibling Hidden Art they converge at 4 BP on +10% / +7% of the same two tags; each still leans its own way.
- Concern: Increase Damage Taken stays at +10% on one row because that row multiplies every matching hit on the target from every attacker; its party value was not simulated.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Magnet jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Taut Filament | Foundation | None | +2% Increase Damage Given (self buff) | Eternal Embrace, Spiraling Wires / 2 |
| 02 | Razor Strands | Hidden Art | Taut Filament | +1 Damage (damage) | Iron Web Entrapment, Lightning Threads, Spiraling Wires, Wire Blast Plus / 4 |
| 03 | Severing Lattice | Advanced Art | Razor Strands | +2 Damage (damage) | Iron Web Entrapment, Lightning Threads, Spiraling Wires, Wire Blast Plus / 4 |
| 04 | Threadbound Vigor | Hidden Art | Taut Filament | +2% Increase Damage Given (self buff) | Eternal Embrace, Spiraling Wires / 2 |
| 05 | Weaver Ascendant | Advanced Art | Threadbound Vigor | +4% Increase Damage Given (self buff) | Eternal Embrace, Spiraling Wires / 2 |
| 06 | Tangling Snare | Foundation | None | +2% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Eternal Embrace, Lightning Threads, Wire Blast Plus / 3 |
| 07 | Constricting Coils | Hidden Art | Tangling Snare | +3% Decrease Damage Given (enemy debuff) | Eternal Embrace, Wire Blast Plus / 2 |
| 08 | Iron Cocoon | Advanced Art | Constricting Coils | +5% Decrease Damage Given (enemy debuff); +2% Increase Damage Taken (enemy debuff) | Eternal Embrace, Lightning Threads, Wire Blast Plus / 3 |
| 09 | Conductive Seam | Hidden Art | Tangling Snare | +3% Increase Damage Taken (enemy debuff) | Lightning Threads / 1 |
| 10 | Galvanic Marionette | Advanced Art | Conductive Seam | +5% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Eternal Embrace, Lightning Threads, Wire Blast Plus / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Taut Filament** — Draw the wire tight and every tremor on the line is yours to read. Both self damage buffs 35 → 37% (Spiraling Wires, Eternal Embrace), each live the two rounds after its cast; they compound on a hit both cover.
- **Razor Strands** — Fine enough to vanish, keen enough to part iron. Commits to the edge: Iron Web Entrapment 45 → 46; Wire Blast Plus, Spiraling Wires and Lightning Threads 40 → 41 EP on every cast.
- **Severing Lattice** — Where the web closes, nothing leaves in one piece. Burst: all four Magnet Damage rows +3 EP on the full route, every cast, no window: Iron Web Entrapment 45 → 48, the other three 40 → 43 (no tier crossed). Stun, redirection and decrease-heal are unsupported.
- **Threadbound Vigor** — Each strand feeds the wielder's arm; the pull becomes the strike. Both self buffs 37 → 39% with Taut Filament (×1.39² ≈ ×1.93 on a hit both cover).
- **Weaver Ascendant** — The loom no longer needs hands. It needs only a will. Sustained amplification: both self buffs 35 → 43% on the full route; a hit both cover (the four Magnet strikes, any element-less hit) lands ×1.43² ≈ ×2.04 (×1.82 at base).
- **Tangling Snare** — A caught thing fights the wire, and the wire does not tire. Wire Blast Plus 30 → 32% and Eternal Embrace 35 → 37% Decrease Damage Given (the Wire Blast circle is an ally hazard); Lightning Threads exposure 35 → 37%.
- **Constricting Coils** — Every struggle draws the knot a little tighter. Wire Blast Plus 32 → 35% and Eternal Embrace 37 → 40% with Tangling Snare; two-round enemy debuffs on a 60 AP and a 40 AP circle.
- **Iron Cocoon** — Wrapped, stilled, and kept: a silence spun from steel. Suppression: Wire Blast Plus 30 → 40% and Eternal Embrace 35 → 45% on the full route (an enemy under both deals ×0.33, ×0.455 at base); Lightning Threads exposure 39% with Tangling Snare.
- **Conductive Seam** — Lightning runs the thread and finds the fault beneath the skin. Lightning Threads exposure only: 37 → 40% with Tangling Snare; one row, 2 rounds per 60 AP single-target cast, cooldown 7.
- **Galvanic Marionette** — Strung and sparking, the enemy dances to a current not its own. Exposure: Lightning Threads 35 → 45% on the full route, for every Lightning, Magnet, Wind or element-less non-pierce hit on the target, allies' included; both suppression rows 34% / 39% with Tangling Snare.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT |
|---|---|---:|---:|---:|---:|
| Severing Lattice (Burst) | Taut Filament, Razor Strands, Severing Lattice, Tangling Snare | +3 | +2% | +2% | +2% |
| Weaver Ascendant (Amplifier) | Taut Filament, Threadbound Vigor, Weaver Ascendant, Tangling Snare | — | +8% | +2% | +2% |
| Iron Cocoon (Suppression) | Tangling Snare, Constricting Coils, Iron Cocoon, Taut Filament | — | +2% | +10% | +4% |
| Galvanic Marionette (Exposure) | Tangling Snare, Conductive Seam, Galvanic Marionette, Constricting Coils | — | — | +7% | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Severing Lattice:** +3 Damage on all four Magnet strikes, every cast and in or out of a buff window (Iron Web Entrapment 45 → 48; Wire Blast Plus, Spiraling Wires and Lightning Threads 40 → 43 EP), with both self buffs at 37%. Tangling Snare is the fourth purchase because the rotation already casts Lightning Threads, Wire Blast Plus and Eternal Embrace: exposure 37%, suppression 32%/37%. Threadbound Vigor (both buffs 39%) is the all-offense alternative.
- **Weaver Ascendant:** Both self buffs 35 → 43% (+8%): Spiraling Wires and Eternal Embrace fit one 100 AP round and open two rounds in which every hit both cover (the four Magnet strikes, any element-less hit) lands ×1.43² ≈ ×2.04 (×1.82 at base), before the bloodline passive. Tangling Snare is the fourth purchase: Lightning Threads' exposure 37% compounds with both buffs on the caster's strikes (×1.43² × 1.37 ≈ ×2.80, ×2.46 at base) and suppression reaches 32%/37%. Razor Strands (+1 Damage) is the all-offense alternative.
- **Iron Cocoon:** Both Decrease Damage Given rows at the route maximum: Wire Blast Plus 30 → 40% and Eternal Embrace 35 → 45%, so an enemy caught by both deals ×0.60 × 0.55 = ×0.33 of its non-pierce damage to anyone for two rounds (×0.455 at base). Lightning Threads exposure 39% (Tangling Snare and the capstone). Taut Filament is the fourth purchase (both self buffs 37%); Conductive Seam (exposure 42%) is the lockdown alternative.
- **Galvanic Marionette:** Lightning Threads' exposure at the route maximum 45% (+10%): for two rounds every Lightning, Magnet, Wind or element-less non-pierce hit on the target, from the caster or allies, lands ×1.45 (×1.35 at base). Constricting Coils is the fourth purchase, so the same rotation also suppresses at 37%/42% (Tangling Snare +2%, Coils +3%, the capstone +2%). Taut Filament (both self buffs 37%) is the solo alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Amplifier | Suppression | Exposure |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Iron Web Entrapment | 0 | Damage | enemy | 45 | 48 (+3) | 45 | 45 | 45 |
| Iron Web Entrapment | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Wire Blast Plus | 0 | Damage | enemy | 40 | 43 (+3) | 40 | 40 | 40 |
| Wire Blast Plus | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 40% (+10) | 37% (+7) |
| Spiraling Wires | 0 | Damage | enemy | 40 | 43 (+3) | 40 | 40 | 40 |
| Spiraling Wires | 1 | Increase Damage Given | self | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 35% |
| Spiraling Wires | 2 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Lightning Threads | 0 | Damage | enemy | 40 | 43 (+3) | 40 | 40 | 40 |
| Lightning Threads | 1 | decreaseheal (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Lightning Threads | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 39% (+4) | 45% (+10) |
| Eternal Embrace | 0 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Eternal Embrace | 1 | Decrease Damage Given | enemy | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 42% (+7) |
| Eternal Embrace | 2 | Increase Damage Given | self | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +3 Damage, +8% Increase Damage Given, +10% Decrease Damage Given, +10% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Severing Lattice: +3 Damage (0 + 1 + 2; off band)
  - Route Weaver Ascendant: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Iron Cocoon: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Galvanic Marionette: +10% Increase Damage Taken (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 4, DDG 2, IDG 2, IDT 1)
- Strongest full build by row-weighted total: Taut Filament, Tangling Snare, Constricting Coils, Iron Cocoon (raw +16, row-weighted 28)
- Lowest row-weighted node: Conductive Seam (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Wire Blast Plus#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +1 Damage | +3 Damage |
|---|---:|---|---|---|
| Iron Web Entrapment | 0 | 45 (High) | 46 (High) | 48 (High) |
| Wire Blast Plus | 0 | 40 (Normal) | 41 (Normal) | 43 (Normal) |
| Spiraling Wires | 0 | 40 (Normal) | 41 (Normal) | 43 (Normal) |
| Lightning Threads | 0 | 40 (Normal) | 41 (Normal) | 43 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Severing Lattice | +3 Damage, +2% IDG | Threadbound Vigor | +3 Damage, +4% IDG | 20 |
| Severing Lattice | +3 Damage, +2% IDG | Tangling Snare *(highest diagnostic)* | +3 Damage, +2% IDG, +2% DDG, +2% IDT | 22 |
| Weaver Ascendant | +8% IDG | Razor Strands | +1 Damage, +8% IDG | 20 |
| Weaver Ascendant | +8% IDG | Tangling Snare *(highest diagnostic)* | +8% IDG, +2% DDG, +2% IDT | 22 |
| Iron Cocoon | +10% DDG, +4% IDT | Taut Filament *(highest diagnostic)* | +2% IDG, +10% DDG, +4% IDT | 28 |
| Iron Cocoon | +10% DDG, +4% IDT | Conductive Seam | +10% DDG, +7% IDT | 27 |
| Galvanic Marionette | +4% DDG, +10% IDT | Taut Filament | +2% IDG, +4% DDG, +10% IDT | 22 |
| Galvanic Marionette | +4% DDG, +10% IDT | Constricting Coils *(highest diagnostic)* | +7% DDG, +10% IDT | 24 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Taut Filament, Razor Strands, Severing Lattice, Threadbound Vigor | +3 Damage, +4% IDG |
| 2 | Taut Filament, Razor Strands, Severing Lattice, Tangling Snare | +3 Damage, +2% IDG, +2% DDG, +2% IDT |
| 3 | Taut Filament, Razor Strands, Threadbound Vigor, Weaver Ascendant | +1 Damage, +8% IDG |
| 4 | Taut Filament, Razor Strands, Threadbound Vigor, Tangling Snare | +1 Damage, +4% IDG, +2% DDG, +2% IDT |
| 5 | Taut Filament, Razor Strands, Tangling Snare, Constricting Coils | +1 Damage, +2% IDG, +5% DDG, +2% IDT |
| 6 | Taut Filament, Razor Strands, Tangling Snare, Conductive Seam | +1 Damage, +2% IDG, +2% DDG, +5% IDT |
| 7 | Taut Filament, Threadbound Vigor, Weaver Ascendant, Tangling Snare | +8% IDG, +2% DDG, +2% IDT |
| 8 | Taut Filament, Threadbound Vigor, Tangling Snare, Constricting Coils | +4% IDG, +5% DDG, +2% IDT |
| 9 | Taut Filament, Threadbound Vigor, Tangling Snare, Conductive Seam | +4% IDG, +2% DDG, +5% IDT |
| 10 | Taut Filament, Tangling Snare, Constricting Coils, Iron Cocoon | +2% IDG, +10% DDG, +4% IDT |
| 11 | Taut Filament, Tangling Snare, Constricting Coils, Conductive Seam | +2% IDG, +5% DDG, +5% IDT |
| 12 | Taut Filament, Tangling Snare, Conductive Seam, Galvanic Marionette | +2% IDG, +4% DDG, +10% IDT |
| 13 | Tangling Snare, Constricting Coils, Iron Cocoon, Conductive Seam | +10% DDG, +7% IDT |
| 14 | Tangling Snare, Constricting Coils, Conductive Seam, Galvanic Marionette | +7% DDG, +10% IDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Structure, names and edges unchanged (01→02→03, 01→04→05, 06→07→08, 06→09→10). Burst: Razor Strands +2 → +1 Damage and Severing Lattice +3 → +2 Damage; the +5 route lifted Wire Blast Plus, Spiraling Wires and Lightning Threads 40 → 45 (a full tier) and Iron Web Entrapment, the kit's stun line, 45 → 50 (semi-nuke to Nuke). Amplifier: Threadbound Vigor +3% → +2% and Weaver Ascendant +5% → +4% Increase Damage Given; Weaver Ascendant drops its +2% Increase Damage Taken rider. The Tangling Snare branch keeps its Draft 4 values.
- Maxima over every legal allocation: Damage +3 (40 → 43, 45 → 48; no tier crossed, nothing reaches 50), Increase Damage Given +8%, Decrease Damage Given +10%, Increase Damage Taken +10%. Not jointly attainable.
- Sized by leverage, not printed totals. The two self buffs compound on a hit both cover, so +8% takes ×1.82 to ×2.04 (+12%); +10% would reach ×2.10. Severing Lattice's +3 EP is +7.5% on a 40 EP strike and +6.7% on Iron Web Entrapment (formula damage is linear in EP: tags.ts powerEffect), on every cast, including the setup casts no buff reaches in their own round. The two Decrease Damage Given rows reduce in sequence: +10% takes an enemy under both from ×0.455 to ×0.33 of its damage, the magnitude approved for Blood-Enchanted Eyes' Red Pestilence on the same 35%/30% pair. Increase Damage Taken has one row but multiplies every matching hit on the target, so it is a route of its own; the amplifier no longer carries it as glue.
- Filters (SOURCE_MECHANICS §3): Spiraling Wires' self buff (Bukijutsu/Speed/Strength, no element) reaches every Bukijutsu-typed or element-less hit, weapons and basic attacks included; Eternal Embrace's reaches Lightning, Magnet, Wind and element-less hits; both cover the four kit strikes, and the 25% + 0.15/level bloodline passive multiplies last. Both Decrease Damage Given rows list all four stat types and no element, so they reach every non-pierce hit; Lightning Threads' exposure lists Lightning, Magnet, Wind and None.
- Delivery (§3b, §4b): every cast is cooldown 7 and every percentage row is live the two rounds after its cast, never on its own hit. Spiraling Wires (60 AP) and Eternal Embrace (40 AP) open both self buffs in one round; Wire Blast Plus and Eternal Embrace do the same for both suppression rows. The four Damage casts are 60 AP, one per turn. All five jutsu are OTHER_USER.
- Fourth purchases: Burst takes Tangling Snare or Threadbound Vigor; Amplifier takes Razor Strands or Tangling Snare; Suppression takes Taut Filament or Conductive Seam; Exposure takes Constricting Coils or Taut Filament. The two all-offense builds share Taut Filament, Razor Strands and Threadbound Vigor and differ only in the capstone: a 40 EP kit strike under both buffs is 43 × 1.39² ≈ 83 (Burst) against 41 × 1.43² ≈ 84 (Amplifier), so neither is automatic; Burst keeps +3 EP outside the windows, Amplifier wins on element-less hits such as basic attacks inside them. The two control capstones with the sibling Hidden Art mirror each other (+10% / +7%).

## Risks and unproven interactions

- Self-buff reach: both self Increase Damage Given rows reach beyond the kit (Spiraling Wires: any Bukijutsu-typed or element-less hit; Eternal Embrace: any Lightning, Magnet, Wind or element-less hit), so the +8% maximum also raises matching normal jutsu, weapons and basic attacks in each window; where both windows overlap they compound (×1.43² ≈ ×2.04) before the passive. Uptime not simulated.
- Ally hazard: Wire Blast Plus row 1 (Decrease Damage Given) is an OTHER_USER AOE_CIRCLE_SPAWN with friendly fire none (=ALL), so allies in the radius-1 circle also receive it, up to 40% at the Suppression maximum; the caster is never a target (SOURCE_MECHANICS §4b). Eternal Embrace's row is friendly fire ENEMIES. Positioning decides.
- Exposure concentration: one row (Lightning Threads, 60 AP, single target, 2 rounds) reaches 45% and multiplies every matching non-pierce hit on the target, the party's included; on the caster's hits it compounds with the self buffs. Party value was not simulated.
- Damage: +3 EP on four Magnet rows keeps Iron Web Entrapment's stun line at High tier (48); the hits are formula-calculated and the self buffs and passive multiply them, so +3 EP is not +3 damage. Not simulated.
- Eternal Embrace delivery: the self buff is realized on the caster at cast time (actions.ts 980–1004/1060–1075; SOURCE_MECHANICS §3b) whenever the circle spawn has a legal target, an ally included; the Decrease Damage Given row (friendly fire ENEMIES) hits each living enemy in the circle once. Buffprevent is unsupported.
- Classification: Magnet is shared with Houkyuken (expected under RUL-2026-10-03-005). The Damage rows, Eternal Embrace's self buff and Lightning Threads' exposure carry Magnet; Spiraling Wires' self buff and both Decrease Damage Given rows carry no element, so the Suppression route and half the Amplifier depend on the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Magnet coverage is unverified.
- No self-defensive route: the kit has no Decrease Damage Taken, Reflect, Lifesteal or Heal row (the 15% Lightning Decrease Damage Taken passive is not a jutsu row); stun, redirection, decrease-heal and buffprevent receive nothing.
- Skill-tree and bloodline effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Magnet jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

