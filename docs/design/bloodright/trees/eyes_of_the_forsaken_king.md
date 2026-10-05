# Eyes of the Forsaken King — Court in Exile

**Bloodline:** Eyes of the Forsaken King (BR-027, rank S, `r3nBY_Th4_ZAIUfhx1jdy`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Light classification / forked tree · **Classification:** Light (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst and branding: a self-buff setup paid off by a controlled +2 Damage on the three Light strikes (Throne of Broken Light), or Afterburn on Imperial Swords (Judgment of the Forsaken) · secondary Self defence on illuminance and Lux (Decrease Damage Taken, Reflect) · tertiary Exposure (Increase Damage Taken) at the Foundation only.

Ten supported rows across five casts. The kit's Burst trait lives in its three 60 AP Light strikes (Shattered Reflection 40, Lux 50 on an AOE line, Imperial Swords 40 EP at jutsu level 25) and in its multipliers: three 35% Increase Damage Taken rows (two on Chrono Stasis, landing together on one target; one on Imperial Swords) compound on every non-pierce hit the target takes (×1.35³ ≈ ×2.46), and illuminance's 35% Increase Damage Given (Fire/Light/Lightning/Wind/None, no stat filter) multiplies every caster strike for two rounds. Exposure is already the kit's strongest lever, so the tree raises it only at the Foundation (+2%, ≈ ×1.045 on the three rows). The offensive root splits by who gains: the caster's strikes (illuminance's buff as the setup, then a controlled +2 Damage: Lux 50 → 52, the 40 EP strikes 42, on the Blood-Enchanted Eyes / Shakunetsu Sakura precedent) or the branded target (Imperial Swords' Afterburn, 25%, 2 rounds). illuminance's 30% Decrease Damage Taken and Lux's 40% Reflect form the defensive root. Mirror, move and timedilation are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Gaze of the Deposed | Foundation | How do I win offensively: make my own strikes land harder, or brand the target so every hit on it burns? |
| Mantle of Exile | Foundation | How do I win defensively: outlast the blow, or return it? |
| Throne of Broken Light | Advanced Art | burst: self-buff setup, controlled +2 Damage payoff on the three Light strikes |
| Judgment of the Forsaken | Advanced Art | branding: every attacker's hits on one target burn |
| Kingdom of One | Advanced Art | fortress |
| Usurper's Reckoning | Advanced Art | retaliation |

**Director review recommended:** Roster questions: DQ-A (Throne of Broken Light +2 Damage after the Edge of the Regalia setup, Lux 50 → 52 on an AOE line that also hits allies in it, kept for the dossier's Burst trait; see above_nuke_rationale).

- Concern: Exposure is held at the Foundation's +2% on purpose; the two all-offence builds that share Gaze, Edge and Searing trade on paper within a few percent (Throne ahead on every kit strike against a target that is not burning, Judgment ahead on burning targets and on allies' hits), but rotation and uptime were not simulated.
- Concern: Kingdom of One is a single-tag fortress (reduction 40%) with no rider: the kit has no Lifesteal, Heal or Decrease Damage Given, and its one other defensive tag is Usurper's Reflect. With Gaze it gives up 3 points of damage buff (37% against 40%) and the +2 Damage to Throne with Mantle (≈ ×1.07 on the 40 EP strikes, ×1.06 on Lux, ×1.02 on the caster's other hits in the window) for ×0.60 against ×0.68 on each hit taken; trading on paper, not simulated.
- Concern: Judgment's Afterburn, Kingdom's reduction, Usurper's Reflect and two of the three exposure rows depend on the proposed jutsu-classification resolver (G1); under the current resolver the three Damage rows (Throne's payoff), illuminance's damage buff and Chrono Stasis row 1 are reachable.
- Concern: The defensive fourths overlap by design (Kingdom with Mirrored Crown and Usurper with Halo of the Unbowed both hold reduction and Reflect); the choice is which one is primary.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Light jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Gaze of the Deposed | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Chrono Stasis, Imperial Swords, illuminance / 4 |
| 02 | Edge of the Regalia | Hidden Art | Gaze of the Deposed | +3% Increase Damage Given (self buff) | illuminance / 1 |
| 03 | Throne of Broken Light | Advanced Art | Edge of the Regalia | +2 Damage (damage) | Imperial Swords, Lux, Shattered Reflection / 3 |
| 04 | Searing Afterimage | Hidden Art | Gaze of the Deposed | +3% Afterburn (enemy debuff) | Imperial Swords / 1 |
| 05 | Judgment of the Forsaken | Advanced Art | Searing Afterimage | +7% Afterburn (enemy debuff) | Imperial Swords / 1 |
| 06 | Mantle of Exile | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Reflect (self buff) | Lux, illuminance / 2 |
| 07 | Halo of the Unbowed | Hidden Art | Mantle of Exile | +3% Decrease Damage Taken (self buff) | illuminance / 1 |
| 08 | Kingdom of One | Advanced Art | Halo of the Unbowed | +5% Decrease Damage Taken (self buff) | illuminance / 1 |
| 09 | Mirrored Crown | Hidden Art | Mantle of Exile | +3% Reflect (self buff) | Lux / 1 |
| 10 | Usurper's Reckoning | Advanced Art | Mirrored Crown | +5% Reflect (self buff) | Lux / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Gaze of the Deposed** — What the fallen king looks upon, he still judges. illuminance self damage buff 35 → 37% (self at cast, 2 rounds); Chrono Stasis ×2 and Imperial Swords enemy exposure 35 → 37% each (2 rounds; ≈ ×1.045 compounded on the three rows, under Shakunetsu Sakura's ×1.075), the tree's only exposure bonus.
- **Edge of the Regalia** — The crown jewels were always blades. Setup for Throne of Broken Light: illuminance self damage buff 35 → 38% (40% with Gaze of the Deposed), live the 2 rounds after each 40 AP cast; it multiplies every Light, Fire, Lightning, Wind and element-less hit the caster lands in that window, on any target.
- **Throne of Broken Light** — The throne lies in shards, and every shard still answers his hand. Burst payoff: +2 Damage on all three Light strikes, Lux 50 → 52 EP (past the 50 Nuke tier; its AOE line also hits allies in it) and Shattered Reflection and Imperial Swords 40 → 42 EP (still Normal), each a 60 AP cast. With the path's 40% self buff that is ≈ ×1.09 on the 40 EP strikes and ≈ ×1.08 on Lux against unbuilt, on any target, no mark needed.
- **Searing Afterimage** — Look away; the image stays, and it burns. Imperial Swords Afterburn only (25 → 28%, the 2 rounds after each 60 AP cast); its value is every later non-pierce hit the target takes.
- **Judgment of the Forsaken** — No court will hear the appeal; the sentence is light. Imperial Swords Afterburn route total +10% (25 → 35%): every later non-pierce hit on the branded target, from any attacker, adds 35% of the hit instead of 25% (×1.35 against ×1.25, ≈ +8%) for the 2 rounds after a 60 AP cast; well under the 60% per-hit cap.
- **Mantle of Exile** — Stripped of the crown, he kept the light it cast. illuminance self damage reduction 30 → 32% (all non-pierce damage, 2 rounds); Lux self Reflect 40 → 42% of each hit, pierce included (2 rounds).
- **Halo of the Unbowed** — A king without a kingdom still refuses to kneel. illuminance self damage reduction only (35% with Mantle of Exile); one row, all non-pierce damage, 2 rounds per 40 AP cast.
- **Kingdom of One** — One subject, one sovereign, one light that answers to him. Single-tag fortress: illuminance damage reduction route total +10% (30 → 40%: each non-pierce hit taken falls from ×0.70 to ×0.60, ≈ 14% less); one 40 AP cast, 2 rounds, cooldown 7. It adds nothing to the strikes.
- **Mirrored Crown** — Strike the crown and meet your own blow in its facets. Lux self Reflect only (45% with Mantle of Exile); one row, every hit incl. pierce, 60% per-hit cap, 2 rounds per 60 AP cast, cooldown 7.
- **Usurper's Reckoning** — Every hand raised against the king is counted, and repaid. Lux Reflect route total +10% (40 → 50% of each hit taken, pierce included: a quarter more returned), 10 points under the 60% per-hit cap; 2 rounds per 60 AP cast, cooldown 7, and only when struck in that window.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | DDT | AB | REF |
|---|---|---:|---:|---:|---:|---:|---:|
| Throne of Broken Light (Burst) | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Searing Afterimage | +2 | +5% | +2% | — | +3% | — |
| Judgment of the Forsaken (Branding) | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Judgment of the Forsaken | — | +5% | +2% | — | +10% | — |
| Kingdom of One (Fortress) | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Kingdom of One | — | +2% | +2% | +10% | — | +2% |
| Usurper's Reckoning (Counter) | Mantle of Exile, Halo of the Unbowed, Mirrored Crown, Usurper's Reckoning | — | — | — | +5% | — | +10% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · AB = Afterburn · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Throne of Broken Light:** Cast illuminance, then strike: Edge of the Regalia holds the self buff at 40%, and Throne adds +2 Damage to all three Light strikes (Shattered Reflection and Imperial Swords 40 → 42 EP, Lux 50 → 52 across its whole line, allies in it included), on any target and with no mark needed: ≈ ×1.09 on the 40 EP strikes and ≈ ×1.08 on Lux against unbuilt from the self buff and the +2 alone (≈ ×1.14 and ×1.13 with the Foundation's 37% exposure counted). Searing Afterimage is the strongest fourth (Afterburn 28%); Mantle of Exile (reduction 32%, Reflect 42%) is the safer one.
- **Judgment of the Forsaken:** Imperial Swords as the brand: Afterburn 35% (+10%), so every non-pierce hit on the target in the two rounds after the cast, the caster's or an ally's, burns for 35% of the hit (Imperial Swords' own hit does not). Edge of the Regalia is the strongest fourth (self buff 40%): against Throne with Searing it wins on a burning target (a fully marked caster strike ×1.40 × 1.37³ × 1.35 ≈ ×4.86 against ×1.05 × 1.40 × 1.37³ × 1.28 ≈ ×4.84) and on every ally's hit there, and loses every kit strike on a target that is not burning (no +2 Damage). Mantle of Exile is the defensive alternative.
- **Kingdom of One:** illuminance as a two-round fortress buff: damage reduction 40% (+10%; each non-pierce hit taken ×0.60 against ×0.70 unbuilt) for the two rounds after one 40 AP cast, with Reflect at 42%. Gaze of the Deposed is the offensive fourth (damage buff and exposure 37%), still 3 points under the burst path's 40% buff and without its +2 Damage; Mirrored Crown (Reflect 45%) is the defensive alternative.
- **Usurper's Reckoning:** The counter-punch build: Lux's Reflect reaches 50% (+10%) of every hit taken for two rounds after each cast, and illuminance's reduction sits at 35%. Halo of the Unbowed is the fourth purchase because it keeps the caster standing through the window; Gaze of the Deposed (buff and exposure 37%) is the aggressive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Branding | Fortress | Counter |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Shattered Reflection | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Shattered Reflection | 1 | mirror (unsupported) | enemy | 100% | 100% | 100% | 100% | 100% |
| Lux | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Lux | 1 | Reflect | self | 40% | 40% | 40% | 42% (+2) | 50% (+10) |
| illuminance | 0 | Increase Damage Given | self | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 35% |
| illuminance | 1 | Decrease Damage Taken | self | 30% | 30% | 30% | 40% (+10) | 35% (+5) |
| illuminance | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Chrono Stasis | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |
| Chrono Stasis | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |
| Chrono Stasis | 2 | timedilation (unsupported) | self | 100% | 100% | 100% | 100% | 100% |
| Imperial Swords | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Imperial Swords | 1 | Afterburn | enemy | 25% | 28% (+3) | 35% (+10) | 25% | 25% |
| Imperial Swords | 2 | Increase Damage Taken | enemy | 35% | 37% (+2) | 37% (+2) | 37% (+2) | 35% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +2% Increase Damage Taken, +10% Decrease Damage Taken, +10% Afterburn, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Throne of Broken Light: +2 Damage (0 + 0 + 2; off band)
  - Route Judgment of the Forsaken: +10% Afterburn (0 + 3 + 7; on band)
  - Route Kingdom of One: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Usurper's Reckoning: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 10 (AB 1, DMG 3, DDT 1, IDG 1, IDT 3, REF 1)
- Strongest full build by row-weighted total: Gaze of the Deposed, Searing Afterimage, Judgment of the Forsaken, Mantle of Exile (raw +18, row-weighted 22)
- Lowest row-weighted node: Edge of the Regalia (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Lux 50 -> 52
- ally-hazard area rows amplified (friendly fire none/ALL): Lux#0

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Shattered Reflection | 0 | 40 (Normal) | 42 (Normal) |
| Lux | 0 | 50 (Nuke) | **52 (above Nuke)** |
| Imperial Swords | 0 | 40 (Normal) | 42 (Normal) |

Above-Nuke rationale: Fable proposal following the director precedent of RUL-2026-10-04-001 (Blood-Enchanted Eyes, Reaper's Embrace 50 → 52) and RUL-2026-10-04-002 (Shakunetsu Sakura, Sakura-ame 50 → 52). Kit fact (R1″): the dossier's Traits line is Burst, and that trait is the deciding fact. The two-prong test is not relied on: the finisher prong holds (Lux is the unique A-rank strike; Shattered Reflection is B, Imperial Swords D) but the strike-led prong fails (2 of 5 offensive percentage rows sit on a Damage jutsu; illuminance's damage buff and Chrono Stasis's exposure rows do not). Lux is the kit's only 50 EP row (60 AP, cooldown 7, an AOE line at range 4). Throne of Broken Light's controlled +2 Damage, the payoff of Edge of the Regalia's +3% self Increase Damage Given setup on illuminance, lifts Lux 50 → 52, past the 50 Nuke tier. The full path (Gaze, Edge, Throne) is ≈ ×1.084 in percentages (self buff 35 → 40%, ×1.037; exposure 35 → 37% on three rows, ×1.045) and ≈ ×1.13 on Lux with the +2, under Blood-Enchanted Eyes' Rite of Exsanguination (≈ ×1.19 on Reaper's Embrace). Throne is the tree's only Damage node and an Advanced Art, so no legal allocation adds more than +2 and none without it exceeds 50; Shattered Reflection and Imperial Swords go 40 → 42 and stay Normal. Lux's line also hits allies standing in it. Pending director review (DQ-A).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Throne of Broken Light | +2 Damage, +5% IDG, +2% IDT | Searing Afterimage | +2 Damage, +5% IDG, +2% IDT, +3% AB | 20 |
| Throne of Broken Light | +2 Damage, +5% IDG, +2% IDT | Mantle of Exile *(highest diagnostic)* | +2 Damage, +5% IDG, +2% IDT, +2% DDT, +2% REF | 21 |
| Judgment of the Forsaken | +2% IDG, +2% IDT, +10% AB | Edge of the Regalia | +5% IDG, +2% IDT, +10% AB | 21 |
| Judgment of the Forsaken | +2% IDG, +2% IDT, +10% AB | Mantle of Exile *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% AB, +2% REF | 22 |
| Kingdom of One | +10% DDT, +2% REF | Gaze of the Deposed *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT, +2% REF | 20 |
| Kingdom of One | +10% DDT, +2% REF | Mirrored Crown | +10% DDT, +5% REF | 15 |
| Usurper's Reckoning | +2% DDT, +10% REF | Gaze of the Deposed *(highest diagnostic)* | +2% IDG, +2% IDT, +2% DDT, +10% REF | 20 |
| Usurper's Reckoning | +2% DDT, +10% REF | Halo of the Unbowed | +5% DDT, +10% REF | 15 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Searing Afterimage | +2 Damage, +5% IDG, +2% IDT, +3% AB |
| 2 | Gaze of the Deposed, Edge of the Regalia, Throne of Broken Light, Mantle of Exile | +2 Damage, +5% IDG, +2% IDT, +2% DDT, +2% REF |
| 3 | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Judgment of the Forsaken | +5% IDG, +2% IDT, +10% AB |
| 4 | Gaze of the Deposed, Edge of the Regalia, Searing Afterimage, Mantle of Exile | +5% IDG, +2% IDT, +2% DDT, +3% AB, +2% REF |
| 5 | Gaze of the Deposed, Edge of the Regalia, Mantle of Exile, Halo of the Unbowed | +5% IDG, +2% IDT, +5% DDT, +2% REF |
| 6 | Gaze of the Deposed, Edge of the Regalia, Mantle of Exile, Mirrored Crown | +5% IDG, +2% IDT, +2% DDT, +5% REF |
| 7 | Gaze of the Deposed, Searing Afterimage, Judgment of the Forsaken, Mantle of Exile | +2% IDG, +2% IDT, +2% DDT, +10% AB, +2% REF |
| 8 | Gaze of the Deposed, Searing Afterimage, Mantle of Exile, Halo of the Unbowed | +2% IDG, +2% IDT, +5% DDT, +3% AB, +2% REF |
| 9 | Gaze of the Deposed, Searing Afterimage, Mantle of Exile, Mirrored Crown | +2% IDG, +2% IDT, +2% DDT, +3% AB, +5% REF |
| 10 | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Kingdom of One | +2% IDG, +2% IDT, +10% DDT, +2% REF |
| 11 | Gaze of the Deposed, Mantle of Exile, Halo of the Unbowed, Mirrored Crown | +2% IDG, +2% IDT, +5% DDT, +5% REF |
| 12 | Gaze of the Deposed, Mantle of Exile, Mirrored Crown, Usurper's Reckoning | +2% IDG, +2% IDT, +2% DDT, +10% REF |
| 13 | Mantle of Exile, Halo of the Unbowed, Kingdom of One, Mirrored Crown | +10% DDT, +5% REF |
| 14 | Mantle of Exile, Halo of the Unbowed, Mirrored Crown, Usurper's Reckoning | +5% DDT, +10% REF |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). First pass: removed all flat Damage (the old +5 route lifted Lux 50 → 55 and Shattered Reflection and Imperial Swords 40 → 45) and turned Edge of the Regalia → Throne of Broken Light into +3% / +5% Increase Damage Given on illuminance's one row; after independent review Judgment of the Forsaken and Usurper's Reckoning dropped their exposure secondaries (+3% and +2%) and Kingdom of One's damage buff fell +3% → +2%. Roster pass (ROSTER_RULES R1/R2): the dossier's Traits line is Burst and Lux is the kit's only 50 EP strike, so Throne returns to a controlled +2 Damage payoff (Lux 50 → 52, the 40 EP strikes 42) after Edge of the Regalia's unchanged +3% self-buff setup, the Blood-Enchanted Eyes pattern (RUL-2026-10-04-001/002), and drops its +5% Increase Damage Given. Final review: Kingdom of One drops its +2% damage buff rider, which put the fortress with Gaze at 39% against the burst path's 40% and left Throne's offensive edge at the +2 Damage alone; the fortress is now single-tag. Structure (01→02→03, 01→04→05, 06→07→08, 06→09→10) and names are kept. Final cleanup: no values changed; above_nuke_rationale names the Burst trait, director_review names DQ-A, and exposure is stated by compounded factor. Consistency pass: no values changed; above_nuke_rationale labels the deciding fact R1″ (the Burst trait).
- Gaze of the Deposed splits offence by who gains. Edge of the Regalia → Throne of Broken Light pays off the caster's own strikes: illuminance's buff at 40% is the setup, and +2 Damage lands on all three Light strikes on every target they reach (Lux's whole line included). Searing Afterimage → Judgment of the Forsaken pays off the target's side: Imperial Swords' Afterburn reaches 35%, one row that adds to every non-pierce hit anyone lands on the target for two rounds. Exposure (three native 35% rows that compound on every attacker's hits, ×1.35³ ≈ ×2.46) is the kit's highest-leverage tag, so nothing past the Foundation raises it: Gaze's +2% (35 → 37% on three rows, ≈ ×1.045 over unbuilt, under Shakunetsu Sakura's ×1.075 and Blood-Enchanted Eyes' ×1.115) is the tree's only exposure bonus. The burst setup is therefore a self buff, not Blood-Enchanted Eyes' exposure setup, so Judgment's obvious fourth (Edge) never stacks exposure on its own brand. Maxima over every legal allocation: Damage +2, Increase Damage Given +5%, Increase Damage Taken +2%, Afterburn +10%, Decrease Damage Taken +10%, Reflect +10%. The top offensive package (Gaze + Edge: ×1.037 × 1.045 ≈ ×1.084; with Throne's +2 ≈ ×1.14 on the 40 EP strikes, ≈ ×1.13 on Lux) stays under Blood-Enchanted Eyes' ×1.234.
- Damage tiers (ROSTER_RULES R5/R6): Throne's +2 is the tree's only flat Damage and sits on the Advanced Art. Shattered Reflection and Imperial Swords stay Normal (40 → 42); Lux goes 50 → 52, past the Nuke tier, recorded in above_nuke_rationale and director_review. No allocation crosses 40 → 45 or reaches 55.
- Interactions: illuminance's damage buff (no stat filter) multiplies the caster's Light, Fire, Lightning, Wind and element-less hits; the bloodline passive (25% + 0.15/level, same elements) is bloodline-sourced and applies last (computeDamagePacket, §3b). Throne's +2 Damage raises the strikes' raw power, so the buff, exposure and the passive all scale it. Chrono Stasis row 0 and Imperial Swords row 2 (four stat types, no element) raise every non-pierce hit on the target; Chrono Stasis row 1 skips Water, Earth and other unlisted elements. Afterburn is taken from the amplified hit.
- Delivery and uptime: every cast has cooldown 7. The three damage casts cost 60 AP at range 4 (Lux is an AOE line); Throne's +2 Damage is instant on each of them and needs no window. illuminance (40 AP EMPTY_GROUND circle) and Lux's Reflect are SELF rows realized on the caster at cast; Chrono Stasis (40 AP, single target, range 5) carries both exposure rows. Each buff or debuff is live only in the two rounds after its cast round. Fully stacked exposure needs Chrono Stasis and Imperial Swords (100 AP); nothing was simulated.
- Fourth purchases: Throne takes Searing Afterimage (Afterburn 28%) or Mantle of Exile (reduction 32%, Reflect 42%); Judgment takes Edge of the Regalia (self buff 40%) or Mantle of Exile; Kingdom of One takes Gaze of the Deposed (buff and exposure 37%) or Mirrored Crown (Reflect 45%); Usurper's Reckoning takes Halo of the Unbowed (reduction 35%) or Gaze of the Deposed (buff and exposure 37%). The two all-offence builds share Gaze, Edge and Searing and differ only in the capstone: +2 Damage on the caster's three strikes against +7% Afterburn on the brand. Throne with Searing wins every kit strike on a target that is not burning (×1.05 on the 40 EP strikes, ×1.04 on Lux, everything else equal); Judgment with Edge wins on a burning target (a fully marked caster strike ×1.40 × 1.37³ × 1.35 ≈ ×4.86 against ×1.05 × 1.40 × 1.37³ × 1.28 ≈ ×4.84, Lux ×4.79) and on every ally's hit there (×1.37³ × 1.35 ≈ ×3.47 against ×1.37³ × 1.28 ≈ ×3.29). No fourth makes a route automatic, and no full allocation is dominated.
- Secondaries: no Advanced Art carries one. Throne's setup already sits on its Hidden Art; the only target-side secondary in the kit is exposure, and on the counter route it would have made a defensive build the tree's exposure peak. Kingdom of One has no defensive rider to take (the kit has no Lifesteal, Heal or Decrease Damage Given, and a Reflect rider would make Kingdom with Mirrored Crown a copy of Usurper with Halo), and an offensive rider would be the burst route's setup tag. Throne with Mantle (buff 40%, +2 Damage, reduction 32%) and Kingdom with Gaze (buff 37%, reduction 40%) trade ≈ ×1.07 on the 40 EP strikes (×1.06 on Lux, ×1.02 on the caster's other hits in the window) for ×0.68 against ×0.60 on each hit taken.
- Single-row routes at +10% (impact envelope). Judgment: 35% Afterburn is ≈ +8% on each hit landed on the burning target in two rounds per 60 AP cast, far under the 60% per-hit cap and the +15% Afterburn limit. Kingdom: 40% reduction takes each non-pierce hit taken from ×0.70 to ×0.60 (≈ 14% less) for two rounds per 40 AP cast on cooldown 7; no other reduction row exists in the kit. Usurper: 50% Reflect returns a quarter more of each blow, only when struck in the two rounds after a 60 AP Lux cast, and stays 10 points under the cap. Throne's path stops at +5% Increase Damage Given on illuminance's one row because its payoff is the +2 Damage, not the buff.

## Risks and unproven interactions

- Ally hazard (Lux#0): Lux's AOE line Damage row has no friendlyFire value (ALL at the pin), so allies in the line take its 50 EP, 52 under Throne of Broken Light; positioning decides. Shattered Reflection, Chrono Stasis and Imperial Swords are single-target; illuminance's supported rows are SELF, so its ground circle carries no amplified hazard.
- Exposure stacking (SOURCE_MECHANICS §3b): Chrono Stasis's two rows and Imperial Swords' row all apply to one target and compound: ×1.35³ ≈ ×2.46 unbuilt, ×1.37³ ≈ ×2.57 with Gaze of the Deposed (≈ ×1.045 over unbuilt), the tree's only exposure bonus, in the two rounds after their casts (not on Imperial Swords' own hit). Every attacker benefits, and Afterburn is taken from the amplified hits. This native multiplier is why nothing past the Foundation raises exposure; not simulated.
- Reflect near cap: Lux's Reflect reaches 50% at the route maximum against the engine's 60% per-hit cap (process.ts), so a main-tree or equipment Reflect source stacking on it saturates quickly; the buff lasts 2 rounds per 60 AP Lux cast on cooldown 7, so the Counter build's value depends on being hit inside that window. Lux must be aimed at a living non-caster user to realize it.
- Downstream reach and pierce: illuminance's damage buff also raises the caster's non-bloodline Fire/Lightning/Wind and element-less hits in its window; enemy-side exposure and Afterburn amplify allies' and weapons' damage against the marked target. Stat filters on element-less rows are not binding (SOURCE_MECHANICS §3). Damage modifiers never touch pierce hits; Reflect includes pierce; Afterburn skips it.
- Classification: element-wide Light scope (RUL-2026-10-03-005): matching supported tags on all Light jutsu, whatever their source; sharing Light with other bloodlines is expected. Only 5 of the 10 supported rows carry Light: the three Damage rows (Throne's payoff), illuminance's damage buff (Gaze and Edge) and Chrono Stasis row 1 are reachable today; the other two exposure rows, the Afterburn, the reduction and the Reflect need the proposed jutsu-classification resolver (ENGINE_GAP_REGISTER G1). Off-kit Light coverage (NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu) is unverified, and Throne's +2 Damage reaches any off-kit Light Damage row too.
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

