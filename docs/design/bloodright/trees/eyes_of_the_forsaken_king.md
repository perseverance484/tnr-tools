# Eyes of the Forsaken King — Court in Exile

**Bloodline:** Eyes of the Forsaken King (BR-027, rank S, `r3nBY_Th4_ZAIUfhx1jdy`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Light classification / forked tree · **Classification:** Light (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst on two sides: amplify the caster (Increase Damage Given on illuminance) or brand the target (Afterburn on Imperial Swords) · secondary Self defence on illuminance and Lux (Decrease Damage Taken, Reflect) · tertiary Exposure (Increase Damage Taken) at the Foundation only.

Ten supported rows across five casts. The kit's Burst trait lives in its multipliers: three 35% Increase Damage Taken rows (two on Chrono Stasis, landing together on one target; one on Imperial Swords) compound on every non-pierce hit the target takes (×1.35³ ≈ ×2.46), and illuminance's 35% Increase Damage Given (Fire/Light/Lightning/Wind/None, no stat filter) multiplies every caster strike for two rounds. Exposure is already the kit's strongest lever, so the tree raises it only at the Foundation (+2%) and splits the offensive routes between the caster's buff and Imperial Swords' Afterburn (25%, 2 rounds). The three Light Damage rows (Shattered Reflection 40, Lux 50 on an AOE line, Imperial Swords 40 EP at jutsu level 25) take no flat Damage: Lux is already a 50 Nuke, so any bonus passes the tier. illuminance's 30% Decrease Damage Taken and Lux's 40% Reflect form the defensive root. Mirror, move and timedilation are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Gaze of the Deposed | Foundation | How do I win offensively: amplify my own strikes, or brand the target so every hit on it burns? |
| Mantle of Exile | Foundation | How do I win defensively: outlast the blow, or return it? |
| Throne of Broken Light | Advanced Art | self-amplification: my own hits on any target, no mark needed |
| Judgment of the Forsaken | Advanced Art | branding: every attacker's hits on one target burn |
| Kingdom of One | Advanced Art | fortress that still strikes |
| Usurper's Reckoning | Advanced Art | retaliation |

- Concern: No flat Damage on a Burst-trait kit: Lux is a 50 EP Nuke, so any Damage bonus passes the tier. If the director prefers the Blood-Enchanted Eyes pattern, a +2 Damage payoff would sit on Throne of Broken Light (Lux 50 → 52, Shattered Reflection and Imperial Swords 40 → 42).
- Concern: Exposure is held at the Foundation's +2% on purpose; the offensive routes trade on paper within a few percent (Throne with Searing ahead on targets that are not burning, Judgment with Edge ahead on burning ones), but rotation and uptime were not simulated.
- Concern: Judgment's Afterburn, Kingdom's reduction, Usurper's Reflect and two of the three exposure rows depend on the proposed jutsu-classification resolver (G1); under the current resolver only illuminance's damage buff (Throne's payoff and Kingdom's secondary) and Chrono Stasis row 1 are reachable.
- Concern: The defensive fourths overlap by design (Kingdom with Mirrored Crown and Usurper with Halo of the Unbowed both hold reduction and Reflect); the choice is which one is primary.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Light jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Gaze of the Deposed | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Chrono Stasis, Imperial Swords, illuminance / 4 |
| 02 | Edge of the Regalia | Hidden Art | Gaze of the Deposed | +3% Increase Damage Given (self buff) | illuminance / 1 |
| 03 | Throne of Broken Light | Advanced Art | Edge of the Regalia | +5% Increase Damage Given (self buff) | illuminance / 1 |
| 04 | Searing Afterimage | Hidden Art | Gaze of the Deposed | +3% Afterburn (enemy debuff) | Imperial Swords / 1 |
| 05 | Judgment of the Forsaken | Advanced Art | Searing Afterimage | +7% Afterburn (enemy debuff) | Imperial Swords / 1 |
| 06 | Mantle of Exile | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Lux, illuminance / 2 |
| 07 | Halo of the Unbowed | Hidden Art | Mantle of Exile | +3% Decrease Damage Taken (self buff) | illuminance / 1 |
| 08 | Kingdom of One | Advanced Art | Halo of the Unbowed | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | illuminance / 2 |
| 09 | Mirrored Crown | Hidden Art | Mantle of Exile | +3% Reflect (self buff) | Lux / 1 |
| 10 | Usurper's Reckoning | Advanced Art | Mirrored Crown | +5% Reflect (self buff) | Lux / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Gaze of the Deposed** — What the fallen king looks upon, he still judges. illuminance self damage buff 35 → 37% (self at cast, 2 rounds); Chrono Stasis ×2 and Imperial Swords enemy exposure 35 → 37% each (2 rounds), the tree's only exposure bonus.
- **Edge of the Regalia** — The crown jewels were always blades. illuminance self damage buff 35 → 38% (40% with Gaze of the Deposed), live the 2 rounds after each 40 AP cast; it multiplies every Light, Fire, Lightning, Wind and element-less hit the caster lands in that window, on any target.
- **Throne of Broken Light** — The throne lies in shards, and every shard still answers his hand. Self-buff payoff: illuminance's damage buff 35 → 45% on the full route (×1.45 against ×1.35 unbuilt, ≈ +7% on every Light, Fire, Lightning, Wind and element-less hit the caster lands, on any target, in the 2 rounds after a 40 AP cast). No mark needed; no Damage row changes.
- **Searing Afterimage** — Look away; the image stays, and it burns. Imperial Swords Afterburn only (25 → 28%, the 2 rounds after each 60 AP cast); its value is every later non-pierce hit the target takes.
- **Judgment of the Forsaken** — No court will hear the appeal; the sentence is light. Imperial Swords Afterburn route total +10% (25 → 35%): every later non-pierce hit on the branded target, from any attacker, adds 35% of the hit instead of 25% (×1.35 against ×1.25, ≈ +8%) for the 2 rounds after a 60 AP cast; well under the 60% per-hit cap.
- **Mantle of Exile** — Stripped of the crown, he kept the light it cast. illuminance self damage reduction 30 → 32% (all non-pierce damage, 2 rounds); Lux self Reflect 40 → 42% of each hit, pierce included (2 rounds).
- **Halo of the Unbowed** — A king without a kingdom still refuses to kneel. illuminance self damage reduction only (35% with Mantle of Exile); one row, all non-pierce damage, 2 rounds per 40 AP cast.
- **Kingdom of One** — One subject, one sovereign, one light that answers to him. illuminance damage reduction route total +10% (30 → 40%: each non-pierce hit taken falls from ×0.70 to ×0.60, ≈ 14% less) and self damage buff +2% (37%; 39% with Gaze of the Deposed); one 40 AP cast, 2 rounds, cooldown 7.
- **Mirrored Crown** — Strike the crown and meet your own blow in its facets. Lux self Reflect only (45% with Mantle of Exile); one row, every hit incl. pierce, 60% per-hit cap, 2 rounds per 60 AP cast, cooldown 7.
- **Usurper's Reckoning** — Every hand raised against the king is counted, and repaid. Lux Reflect route total +10% (40 → 50% of each hit taken, pierce included: a quarter more returned), 10 points under the 60% per-hit cap; 2 rounds per 60 AP cast, cooldown 7, and only when struck in that window.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|
| Throne of Broken Light (Self-amplification) | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Searing Afterimage | +10% | +2% | — | +3% | — |
| Judgment of the Forsaken (Branding) | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Judgment of the Forsaken | +5% | +2% | — | +10% | — |
| Kingdom of One (Fortress) | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Kingdom of One | +4% | +2% | +10% | — | +2% |
| Usurper's Reckoning (Counter) | Mantle of Exile, Halo of the Unbowed, Mirrored Crown, Usurper's Reckoning | — | — | +5% | — | +10% |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Throne of Broken Light:** Cast illuminance, then strike: the self buff reaches 45%, so every hit the caster lands in its two-round window, on any target and with no mark needed (Lux's line included), takes ×1.45 against ×1.35 unbuilt (≈ +7%), with every Damage row left at 40/50/40 EP and exposure at the Foundation's 37%. Searing Afterimage is the strongest fourth (Afterburn 28%); Mantle of Exile (reduction 32%, Reflect 42%) is the safer one.
- **Judgment of the Forsaken:** Imperial Swords as the brand: Afterburn 35% (+10%), so every non-pierce hit on the target in the two rounds after the cast, the caster's or an ally's, burns for 35% of the hit (Imperial Swords' own hit does not). Edge of the Regalia is the strongest fourth (self buff 40%): against Throne with Searing it wins on a burning target (fully marked, ×1.40 × 1.37³ × 1.35 ≈ ×4.86 against ×1.45 × 1.37³ × 1.28 ≈ ×4.77) and loses on any target that is not burning (×1.40 against ×1.45). Mantle of Exile is the defensive alternative.
- **Kingdom of One:** illuminance as a two-round fortress buff: damage reduction 40% (+10%; each non-pierce hit taken ×0.60 against ×0.70 unbuilt) and damage buff 39% for the two rounds after one 40 AP cast, with exposure at 37% and Reflect at 42%. Gaze of the Deposed is the fourth purchase because it lifts illuminance's buff and the exposure rows; Mirrored Crown (Reflect 45%) is the defensive alternative.
- **Usurper's Reckoning:** The counter-punch build: Lux's Reflect reaches 50% (+10%) of every hit taken for two rounds after each cast, and illuminance's reduction sits at 35%. Halo of the Unbowed is the fourth purchase because it keeps the caster standing through the window; Gaze of the Deposed (buff and exposure 37%) is the aggressive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Self-amplification | Branding | Fortress | Counter |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Shattered Reflection | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Shattered Reflection | 1 | mirror (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Lux | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Lux | 1 | Reflect | self | 40% | 40% | 40% | 42% (+2) | 50% (+10) |
| illuminance | 0 | Increase Damage Given | self | 35% | 45% (+10) | 40% (+5) | 39% (+4) | 35% |
| illuminance | 1 | Decrease Damage Taken | self | 30% | 30% | 30% | 40% (+10) | 35% (+5) |
| illuminance | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Chrono Stasis | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |
| Chrono Stasis | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |
| Chrono Stasis | 2 | timedilation (unsupported) | self | 100% | 100% | 100% | 100% | 100% |
| Imperial Swords | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Imperial Swords | 1 | Afterburn | enemy | 25% | 28% (+3) | 35% (+10) | 25% | 25% |
| Imperial Swords | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +10% Increase Damage Given, +2% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Throne of Broken Light: +10% Increase Damage Given (2 + 3 + 5; on band)
  - Route Judgment of the Forsaken: +10% Afterburn (0 + 3 + 7; on band)
  - Route Kingdom of One: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Usurper's Reckoning: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (AB 1, DMG 3, DDT 1, IDG 1, IDT 3, REF 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Gaze of the Deposed, Searing Afterimage, Judgment of the Forsaken, Mantle of Exile (raw +18, row-weighted 22)
- Lowest row-weighted node: Edge of the Regalia (3)

Validator warnings:

- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Shattered Reflection 40 (Normal), Lux 50 (Nuke), Imperial Swords 40 (Normal)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Throne of Broken Light | +10% IDG, +2% IDT | Searing Afterimage | +10% IDG, +2% IDT, +3% AB | 19 |
| Throne of Broken Light | +10% IDG, +2% IDT | Mantle of Exile *(highest diagnostic)* | +10% IDG, +2% IDT, +2% DDT, +2% REF | 20 |
| Judgment of the Forsaken | +2% IDG, +2% IDT, +10% AB | Edge of the Regalia | +5% IDG, +2% IDT, +10% AB | 21 |
| Judgment of the Forsaken | +2% IDG, +2% IDT, +10% AB | Mantle of Exile *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% AB, +2% REF | 22 |
| Kingdom of One | +2% IDG, +10% DDT, +2% REF | Gaze of the Deposed *(highest diagnostic)* | +4% IDG, +2% IDT, +10% DDT, +2% REF | 22 |
| Kingdom of One | +2% IDG, +10% DDT, +2% REF | Mirrored Crown | +2% IDG, +10% DDT, +5% REF | 17 |
| Usurper's Reckoning | +2% DDT, +10% REF | Gaze of the Deposed *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% REF | 20 |
| Usurper's Reckoning | +2% DDT, +10% REF | Halo of the Unbowed | +5% DDT, +10% REF | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Searing Afterimage | +10% IDG, +2% IDT, +3% AB |
| 2 | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Mantle of Exile | +10% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Judgment of the Forsaken | +5% IDG, +2% IDT, +10% AB |
| 4 | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Mantle of Exile | +5% IDG, +2% IDT, +2% DDT, +3% AB, +2% REF |
| 5 | Gaze of the Deposed, Edge of the Regalia, Mantle of Exile, Halo of the Unbowed | +5% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Gaze of the Deposed, Edge of the Regalia, Mantle of Exile, Mirrored Crown | +5% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Gaze of the Deposed, Searing Afterimage, Judgment of the Forsaken, Mantle of Exile | +2% IDG, +2% IDT, +2% DDT, +10% AB, +2% REF |
| 8 | Gaze of the Deposed, Searing Afterimage, Mantle of Exile, Halo of the Unbowed | +2% IDG, +2% IDT, +5% DDT, +3% AB, +2% REF |
| 9 | Gaze of the Deposed, Searing Afterimage, Mantle of Exile, Mirrored Crown | +2% IDG, +2% IDT, +2% DDT, +3% AB, +5% REF |
| 10 | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Kingdom of One | +4% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Mirrored Crown | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Gaze of the Deposed, Mantle of Exile, Mirrored Crown, Usurper's Reckoning | +2% IDG, +2% IDT, +2% DDT, +10% REF |
| 13 | Mantle of Exile, Halo of the Unbowed, Kingdom of One, Mirrored Crown | +2% IDG, +10% DDT, +5% REF |
| 14 | Mantle of Exile, Halo of the Unbowed, Mirrored Crown, Usurper's Reckoning | +5% DDT, +10% REF |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Removed all flat Damage: Edge of the Regalia +2 Damage → +3% Increase Damage Given; Throne of Broken Light +3 Damage → +5% Increase Damage Given. The old +5 route lifted Lux 50 → 55 and Shattered Reflection and Imperial Swords 40 → 45, and even +2 lifts Lux past the 50 Nuke tier. After independent review, Judgment of the Forsaken and Usurper's Reckoning drop their exposure secondaries (+3% and +2%) and Kingdom of One's damage buff falls +3% → +2%. Structure (01→02→03, 01→04→05, 06→07→08, 06→09→10) and names are kept.
- Gaze of the Deposed splits offence by who gains. Edge of the Regalia → Throne of Broken Light pays off the caster's side: illuminance's damage buff reaches 45%, one row, but one cast multiplies every hit the caster lands, on any target, for two rounds. Searing Afterimage → Judgment of the Forsaken pays off the target's side: Imperial Swords' Afterburn reaches 35%, one row that adds to every non-pierce hit anyone lands on the target for two rounds. Exposure (three native 35% rows that compound on every attacker's hits, ×1.35³ ≈ ×2.46) is the kit's highest-leverage tag and its native burst, so no capstone raises it: the Foundation's +2% (×1.37³ ≈ ×2.57) is the tree's only exposure bonus. Maxima over every legal allocation: Increase Damage Given +10%, Increase Damage Taken +2%, Afterburn +10%, Decrease Damage Taken +10%, Reflect +10%, no Damage.
- Interactions: illuminance's damage buff (no stat filter) multiplies the caster's Light, Fire, Lightning, Wind and element-less hits; the bloodline passive (25% + 0.15/level, same elements) is bloodline-sourced and applies last (computeDamagePacket, §3b). Chrono Stasis row 0 and Imperial Swords row 2 (four stat types, no element) raise every non-pierce hit on the target; Chrono Stasis row 1 skips Water, Earth and other unlisted elements. Afterburn is taken from the amplified hit.
- Delivery and uptime: every cast has cooldown 7. The three damage casts cost 60 AP at range 4 (Lux is an AOE line); illuminance (40 AP EMPTY_GROUND circle) and Lux's Reflect are SELF rows realized on the caster at cast; Chrono Stasis (40 AP, single target, range 5) carries both exposure rows. Each buff or debuff is live only in the two rounds after its cast round. Fully stacked exposure needs Chrono Stasis and Imperial Swords (100 AP); nothing was simulated.
- Fourth purchases: Throne takes Searing Afterimage (Afterburn 28%) or Mantle of Exile; Judgment takes Edge of the Regalia (self buff 40%) or Mantle of Exile; Kingdom of One takes Gaze of the Deposed (buff 39%, exposure 37%) or Mirrored Crown (Reflect 45%); Usurper's Reckoning takes Halo of the Unbowed (reduction 35%) or Gaze of the Deposed (buff and exposure 37%). The two all-offence builds share Gaze, Edge and Searing and split on who gains. Throne with Searing wins every caster hit on a target that is not burning (×1.45 against ×1.40 on any target, Lux's line included; ×1.45 × 1.37² ≈ ×2.72 against ×2.63 when Chrono Stasis leads). Judgment with Edge wins on a burning target (fully marked, ×1.40 × 1.37³ × 1.35 ≈ ×4.86 against ×1.45 × 1.37³ × 1.28 ≈ ×4.77) and on every ally's hit there (×1.37³ × 1.35 ≈ ×3.47 against ×1.37³ × 1.28 ≈ ×3.29). No fourth makes a route automatic, and no full allocation is dominated.
- Secondaries: Kingdom of One carries damage buff +2% because illuminance is one cast holding both self rows, so the fortress cast still sharpens the strikes made under it (39% with Gaze), below Edge of the Regalia's +3% commitment and Throne's 45%. Judgment and Usurper's Reckoning carry none: the only target-side secondary in the kit is exposure, and on the counter route it would have made a defensive build the tree's exposure peak.
- Single-row routes at +10% (impact envelope). Throne: one 40 AP cast multiplies every caster hit on every target for two rounds (≈ +7% per hit) and does not compound with itself. Judgment: 35% Afterburn is ≈ +8% on each hit landed on the burning target in two rounds per 60 AP cast, far under the 60% per-hit cap and the +15% Afterburn limit. Kingdom: 40% reduction takes each non-pierce hit taken from ×0.70 to ×0.60 (≈ 14% less) for two rounds per 40 AP cast on cooldown 7; no other reduction row exists in the kit. Usurper: 50% Reflect returns a quarter more of each blow, only when struck in the two rounds after a 60 AP Lux cast, and stays 10 points under the cap.

## Risks and unproven interactions

- Ally hazard (Lux#0): Lux's AOE line Damage row has no friendlyFire value (ALL at the pin), so allies in the line take its 50 EP; no node changes that row. Shattered Reflection, Chrono Stasis and Imperial Swords are single-target; illuminance's supported rows are SELF, so its ground circle carries no amplified hazard.
- Exposure stacking (SOURCE_MECHANICS §3b): Chrono Stasis's two rows and Imperial Swords' row all apply to one target and compound: ×1.35³ ≈ ×2.46 unbuilt, ×1.37³ ≈ ×2.57 with Gaze of the Deposed, the tree's only exposure bonus, in the two rounds after their casts (not on Imperial Swords' own hit). Every attacker benefits, and Afterburn is taken from the amplified hits. This native burst is why no capstone raises exposure; not simulated.
- Reflect near cap: Lux's Reflect reaches 50% at the route maximum against the engine's 60% per-hit cap (process.ts), so a main-tree or equipment Reflect source stacking on it saturates quickly; the buff lasts 2 rounds per 60 AP Lux cast on cooldown 7, so the Counter build's value depends on being hit inside that window. Lux must be aimed at a living non-caster user to realize it.
- Downstream reach and pierce: illuminance's damage buff also raises the caster's non-bloodline Fire/Lightning/Wind and element-less hits in its window; enemy-side exposure and Afterburn amplify allies' and weapons' damage against the marked target. Stat filters on element-less rows are not binding (SOURCE_MECHANICS §3). Damage modifiers never touch pierce hits; Reflect includes pierce; Afterburn skips it.
- Classification: element-wide Light scope (RUL-2026-10-03-005): matching supported tags on all Light jutsu, whatever their source; sharing Light with other bloodlines is expected. Only 5 of the 10 supported rows carry Light: illuminance's damage buff (Throne's payoff row) and Chrono Stasis row 1 are reachable today; the other exposure rows, the Afterburn, the reduction and the Reflect need the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Light coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu) is unverified.
- Afterburn: one application row (Imperial Swords, 25% for 2 rounds per 60 AP cast; 35% at the route maximum); its value is downstream, depends on hits landed in the window, skips pierce, and the 60% per-hit cap means stacked Afterburn sources saturate. No proc or uptime simulation was performed.
- Rank context: an S-rank bloodline whose native kit (three 60 AP Damage casts, triple exposure, a 25%+ damage-buff passive) is strong before any node; the tree prices marginal opportunity, not final strength. Ranked modes suppress skill-tree effects; normal-tree potency policy is unapproved, so a stacking audit precedes implementation.
- Unsupported rows untouched: Shattered Reflection's mirror (100%), illuminance's move (1) and Chrono Stasis's timedilation (100%) receive no bonus. No adverse rows exist in this kit; no row is hidden, item-gated or mode-restricted.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Light jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

