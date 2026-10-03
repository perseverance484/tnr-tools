# Arashima — Reaper's Tempest

**Bloodline:** Arashima (BR-005, rank A, `9F6Ruhuf82gSzpZcsUaPW`) · **Revision:** Draft 4 / Storm classification / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Storm (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Lifesteal (sustain; the kit's identity, at the +5% hard ceiling) · secondary Decrease Damage Taken and Decrease Damage Given (fortress and suppression routes, +10% each) · tertiary Damage (Storm AoE burst, +5) and Increase Damage Given (glue across routes, up to +8%).

Stormsinger is the kit's identity: one 40 AP self-cast carries Lifesteal 40%, Increase Damage Given 35% and Decrease Damage Taken 35% for two rounds, so sustain is the primary emphasis. Lifesteal is held to the +5% hard ceiling (40 → 45%, well under the 60% leech cap), so the Sustain route pairs it with the tree's largest Increase Damage Given gain (43% with Tempest Hymn): bigger hits feed the leech. Reapers Storm and Demons Strike are the only Damage rows (45 EP each, Storm, AoE circle spawn, 60 AP) and form the burst route. Death's Storm's Decrease Damage Given 30% is the kit's only enemy debuff and anchors the suppression route; its pierce row is unsupported and untouched. 'Primary' names the kit's identity, not the largest addition: the fortress and suppression routes reach +10% on their tags.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Storm jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempest Hymn | Foundation | None | +3% Increase Damage Given (self buff) | Stormsinger / 1 |
| 02 | Gathering Thunderhead | Hidden Art | Tempest Hymn | +2 Damage (damage) | Demons Strike, Reapers Storm / 2 |
| 03 | Sundered Sky | Advanced Art | Gathering Thunderhead | +3 Damage (damage) | Demons Strike, Reapers Storm / 2 |
| 04 | Crimson Downpour | Hidden Art | Tempest Hymn | +2% Lifesteal (self buff) | Stormsinger / 1 |
| 05 | Reaper's Harvest | Advanced Art | Crimson Downpour | +3% Lifesteal (self buff); +5% Increase Damage Given (self buff) | Stormsinger / 2 |
| 06 | Stillness in the Squall | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Death’s Storm, Stormsinger / 2 |
| 07 | Stormwarden's Hide | Hidden Art | Stillness in the Squall | +3% Decrease Damage Taken (self buff) | Stormsinger / 1 |
| 08 | Unbroken Horizon | Advanced Art | Stormwarden's Hide | +5% Decrease Damage Taken (self buff); +2% Increase Damage Given (self buff) | Stormsinger / 2 |
| 09 | Deadwind Dirge | Hidden Art | Stillness in the Squall | +3% Decrease Damage Given (enemy debuff) | Death’s Storm / 1 |
| 10 | Silence After Thunder | Advanced Art | Deadwind Dirge | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff) | Death’s Storm, Stormsinger / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempest Hymn** — The storm sings through Arashima blood; every verse is a wound and a drink. Stormsinger Increase Damage Given 35 → 38% (self buff, 2 rounds per 40 AP cast); no gates, no adverse rows.
- **Gathering Thunderhead** — Clouds mass over the field, heavy with what is about to fall. Reapers Storm and Demons Strike Storm Damage 45 → 47 EP (AoE circle spawns, 60 AP); Death's Storm's pierce row is unsupported.
- **Sundered Sky** — The whole sky comes down at once. Nothing beneath it is spared. Damage route total +5: both Storm Damage rows 45 → 50 EP; both are AoE, so every enemy in the circle takes the full gain.
- **Crimson Downpour** — The rain that follows the storm runs red, and it runs toward the singer. Stormsinger Lifesteal 40 → 42%; leech shares the 60%-of-damage cap with vamp.
- **Reaper's Harvest** — What the storm cuts down, the reaper gathers in. Lifesteal route total +5% (Stormsinger 40 → 45%, the hard ceiling) and Increase Damage Given 35 → 43% with Tempest Hymn, on the same 2-round cast.
- **Stillness in the Squall** — At the heart of the tempest there is a calm that belongs to Arashima alone. Stormsinger Decrease Damage Taken 35 → 37% (self, 2 rounds) and Death's Storm Decrease Damage Given 30 → 32% (enemy, AoE, 2 rounds, debuff-prevent gated; ally hazard).
- **Stormwarden's Hide** — Years of standing in the gale leave skin the wind no longer bites. Stormsinger Decrease Damage Taken 40% with Stillness in the Squall (self, 2 rounds); four stat types and no element, so it covers almost every incoming hit; pierce bypasses it.
- **Unbroken Horizon** — The storm has raged all night; at dawn the line still holds. Decrease Damage Taken route total +10% (Stormsinger 35 → 45%); Increase Damage Given 40% with Tempest Hymn; both ride the same 2-round cast window.
- **Deadwind Dirge** — The wind after Death's Storm carries the strength out of every arm it touches. Death's Storm Decrease Damage Given 35% with Stillness in the Squall, 2 rounds, everyone in the circle (allies too: ally hazard); needs the 60 AP cast, debuff-prevent gated.
- **Silence After Thunder** — When the thunder stops, only the Arashima still has the will to strike. Decrease Damage Given route total +10% (Death's Storm 30 → 40%, ally hazard in the circle); Stormsinger Decrease Damage Taken +2% (39% with Stillness in the Squall).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT | LS |
|---|---|---:|---:|---:|---:|---:|
| Reaper's Harvest (Sustain) | Tempest Hymn, Crimson Downpour, Reaper's Harvest, Stillness in the Squall | — | +8% | +2% | +2% | +5% |
| Sundered Sky (Burst) | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Stillness in the Squall | +5 | +3% | +2% | +2% | — |
| Unbroken Horizon (Fortress) | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon | — | +5% | +2% | +10% | — |
| Silence After Thunder (Suppression) | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder | — | +3% | +10% | +4% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Reaper's Harvest:** The Lifesteal route takes Stormsinger from 40% to 45% leech (the +5% hard ceiling) and its Increase Damage Given from 35% to 43% for the same two-round window. The enhanced Increase Damage Given lifts both Storm Damage rows and any hit that uses your highest offence stat or carries no element (not Death's Storm's pierce, which bypasses damage modifiers); the leech draws from nearly every damage row, including Death's Storm's 58 EP pierce at full ratio. Stillness in the Squall is the fourth purchase (Decrease Damage Taken 37%, Death's Storm's debuff 32%): a duelist who out-sustains the exchange rather than ending it quickly.
- **Sundered Sky:** +5 Damage lifts Reapers Storm and Demons Strike from 45 to 50 EP on every enemy in their circles, and the bloodline's own Storm Increase Damage Given passive multiplies that downstream. Tempest Hymn is the required ancestor (Increase Damage Given 38%); Stillness in the Squall is the fourth purchase for a little mitigation. This is the burst option: it gives up the sustain and the fortress entirely.
- **Unbroken Horizon:** The Decrease Damage Taken route takes Stormsinger from 35% to 45% for its two rounds, and Tempest Hymn's +3% plus the Advanced Art's +2% give 40% Increase Damage Given on the same cast: a fortified-offence build that tanks the trade and answers it. Lifesteal stays at 40% and Death's Storm's debuff at 32%, so it is clearly not the sustain or suppression build.
- **Silence After Thunder:** The Decrease Damage Given route takes Death's Storm's enemy debuff from 30% to 40% on every enemy in its circle for two rounds; the Advanced Art's +2% and Stillness in the Squall leave Stormsinger at 39% Decrease Damage Taken, and Tempest Hymn adds 38% Increase Damage Given. It suppresses groups rather than killing them; Stormwarden's Hide instead of Tempest Hymn is the pure turtle at 42% Decrease Damage Taken / 40% Decrease Damage Given.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustain | Burst | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Stormsinger | 0 | Lifesteal | self | 40% | 45% (+5) | 40% | 40% | 40% |
| Stormsinger | 1 | Increase Damage Given | self | 35% | 43% (+8) | 38% (+3) | 40% (+5) | 38% (+3) |
| Stormsinger | 2 | Decrease Damage Taken | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 39% (+4) |
| Sounds of Tempest | 0 | poison (unsupported) | enemy | 50% | 50% | 50% | 50% | 50% |
| Sounds of Tempest | 1 | increasepoolcost (unsupported) | enemy | 80% | 80% | 80% | 80% | 80% |
| Reapers Storm | 0 | Damage | enemy | 45 | 45 | 50 (+5) | 45 | 45 |
| Reapers Storm | 1 | drain (unsupported) | enemy | 250 | 250 | 250 | 250 | 250 |
| Demons Strike | 0 | Damage | enemy | 45 | 45 | 50 (+5) | 45 | 45 |
| Demons Strike | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Demons Strike | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Death’s Storm | 0 | pierce (unsupported) | enemy | 58 | 58 | 58 | 58 | 58 |
| Death’s Storm | 1 | Decrease Damage Given | enemy | 30% | 32% (+2) | 32% (+2) | 32% (+2) | 40% (+10) |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +8% Increase Damage Given, +10% Decrease Damage Given, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Sundered Sky: +5 Damage (0 + 2 + 3; on band)
  - Route Reaper's Harvest: +5% Lifesteal (0 + 2 + 3; on band)
  - Route Unbroken Horizon: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Silence After Thunder: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 6 (DMG 2, DDG 1, DDT 1, IDG 1, LS 1)
- Strongest full build by row-weighted total: Tempest Hymn, Crimson Downpour, Reaper's Harvest, Stillness in the Squall (raw +17, row-weighted 17)
- Lowest row-weighted node: Crimson Downpour (2)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Death’s Storm#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Crimson Downpour | +5 Damage, +3% IDG, +2% LS |
| 2 | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Stillness in the Squall | +5 Damage, +3% IDG, +2% DDG, +2% DDT |
| 3 | Tempest Hymn, Gathering Thunderhead, Crimson Downpour, Reaper's Harvest | +2 Damage, +8% IDG, +5% LS |
| 4 | Tempest Hymn, Gathering Thunderhead, Crimson Downpour, Stillness in the Squall | +2 Damage, +3% IDG, +2% DDG, +2% DDT, +2% LS |
| 5 | Tempest Hymn, Gathering Thunderhead, Stillness in the Squall, Stormwarden's Hide | +2 Damage, +3% IDG, +2% DDG, +5% DDT |
| 6 | Tempest Hymn, Gathering Thunderhead, Stillness in the Squall, Deadwind Dirge | +2 Damage, +3% IDG, +5% DDG, +2% DDT |
| 7 | Tempest Hymn, Crimson Downpour, Reaper's Harvest, Stillness in the Squall | +8% IDG, +2% DDG, +2% DDT, +5% LS |
| 8 | Tempest Hymn, Crimson Downpour, Stillness in the Squall, Stormwarden's Hide | +3% IDG, +2% DDG, +5% DDT, +2% LS |
| 9 | Tempest Hymn, Crimson Downpour, Stillness in the Squall, Deadwind Dirge | +3% IDG, +5% DDG, +2% DDT, +2% LS |
| 10 | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon | +5% IDG, +2% DDG, +10% DDT |
| 11 | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Deadwind Dirge | +3% IDG, +5% DDG, +5% DDT |
| 12 | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder | +3% IDG, +10% DDG, +4% DDT |
| 13 | Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon, Deadwind Dirge | +2% IDG, +5% DDG, +10% DDT |
| 14 | Stillness in the Squall, Stormwarden's Hide, Deadwind Dirge, Silence After Thunder | +10% DDG, +7% DDT |

## Design notes

- Node split: four routes map one-to-one onto the kit's four distinct non-glue tags (Damage, Lifesteal, Decrease Damage Taken, Decrease Damage Given). Increase Damage Given is the glue (Tempest Hymn +3%, Reaper's Harvest +5%, Unbroken Horizon +2%) and never sits on a Hidden Art. Lifesteal sits only on the Sustain route, so no legal allocation exceeds the +5% hard ceiling.
- Routes (RUL-2026-10-03-005): Burst +5 Damage (Gathering Thunderhead +2, Sundered Sky +3) on two rows; Sustain +5% Lifesteal (Crimson Downpour +2%, Reaper's Harvest +3%) with a +5% Increase Damage Given secondary; Fortress +10% Decrease Damage Taken and Suppression +10% Decrease Damage Given (Stillness in the Squall +2%, Hidden Art +3%, Advanced Art +5%). Maxima over every legal allocation: Damage +5, Lifesteal +5%, Decrease Damage Taken +10%, Decrease Damage Given +10%, Increase Damage Given +8% (Tempest Hymn plus Reaper's Harvest).
- Recalibration: Lifesteal left Tempest Hymn and Silence After Thunder and the Sustain route fell from +10% to +5%; Reaper's Harvest's Increase Damage Given rose to +5% and Tempest Hymn's to +3% (Unbroken Horizon's fell to +2%) so the four example builds each total 17 row-weighted points and all 14 legal full builds stay non-dominated.
- Interaction with the main tree and passives: Stormsinger's Increase Damage Given, Decrease Damage Taken and Lifesteal rows are self buffs with two-round durations, so enhancing them also reaches normal jutsu and weapons used inside that window, subject to efficiency matching (see risks): the Lifesteal row lists all four stat types and so draws from every damage row that declares a stat type plus all pierce (including Death's Storm's own unsupported pierce row, which the engine feeds into lifesteal); the DDT row lists the same four stat types and reduces every incoming damage row that declares a stat type but never pierce, which the engine applies after the damage-modifier pass (so no IDG, DDT or DDG node touches a pierce hit); the IDG row's single 'Highest' stat type reaches the kit's two Storm Damage rows and any damage row that uses the caster's highest offence stat or carries no element. The bloodline's own IDG passive (25% + 0.15/level on Water/Lightning/Storm/None) multiplies the enhanced Damage rows downstream. Death's Storm's DDG is an enemy debuff, so it also softens enemy normal jutsu (not enemy pierce) against allies. None of these downstream effects were simulated.
- Delivery and uptime: every Stormsinger-row node shares one 40 AP cast with a 7-round cooldown and a 2-round buff, so a sustain or fortress build's realised value is capped by that window; the Damage rows cost 60 AP on 7-round cooldowns and are AoE circle spawns, so their raw EP bonus is paid once per enemy hit; DDG requires landing the 60 AP Death's Storm and is debuff-prevent gated. Skill-tree effects (and therefore Bloodright potency) are skipped in RANKED_PVP and RANKED_SPARRING at the pin.
- Fourth-purchase choices: after any 3 BP route the natural fourth is the other Foundation. Hybrids with no Advanced Art (e.g. 01+02+04+06: +2 Damage, +2% Lifesteal, +3% IDG, +2% DDT/DDG) and the all-defence 06+07+09+10 (+7% DDT, +10% DDG) are legal and non-dominated; 01+02+04+05 is the strongest unadvertised sustain build (+2 Damage, +5% Lifesteal, +8% IDG) at the cost of any mitigation.
- Presentation: the renderer prints full jutsu names for this kit because 'Reapers Storm' and 'Death's Storm' would both abbreviate to 'Storm', which is also the classification label; JSON and Markdown always carried full names.

## Risks and unproven interactions

- Classification: Storm is shared with Godstorm Eclipse, Shinrai Ou and Stormboat Willy (expected under RUL-2026-10-03-005). 2 of 6 kit rows carry Storm; Death's Storm's Decrease Damage Given row and Stormsinger's three rows need the proposed jutsu-classification resolver, and Stormsinger (no Storm row) additionally needs an authored Storm jutsu classification (ENGINE_GAP_REGISTER G1). Off-kit Storm coverage is unverified.
- Lifesteal cap: lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit. The route tops out at 45%, leaving 15 points of headroom for vamp from the main tree or items. Lifesteal requires both combatants alive and is blocked by healprevent on the caster. Verified at the pin: pierce runs before the post-damage pass (process.ts 563–585), the lifesteal handler has no pierce exclusion (tags.ts 2028–2054, unlike recoil and afterburn) and getEfficiencyRatio returns 1 for pierce (3478–3479), so Stormsinger's leech also draws from Death's Storm's 58 EP pierce at full ratio.
- Efficiency matching (tags.ts 3477–3510, G15): Stormsinger's Increase Damage Given row (statTypes ['Highest'], no elements) matches the kit's Storm Damage rows and any hit that uses the caster's highest offence stat or carries no element, but not an elemental hit of a different stat type. The Lifesteal and Decrease Damage Taken rows list all four stat types and no element, so they match almost every hit; Decrease Damage Taken never sees pierce (pierce is applied after the damage-modifier pass), and Increase Damage Given and Decrease Damage Given never touch pierce either.
- Stacking: BATTLE_TAG_STACKING is true at the pin, so a Bloodright potency effect stacks with any other potency source rather than being deduplicated.
- No adverse rows, hidden rows, item gates, mode restrictions or injected children exist in this kit (the one ally-hazard row is covered below); the unsupported drain, pierce, poison, increasepoolcost, shield and move rows are unchanged by every node.
- No combat simulation: non-dominance of the 14 allocations is an arithmetic result over per-row additions, not evidence of equal combat strength; AoE target counts, uptime, AP economy and the Storm Increase Damage Given passive's multiplication were not modelled.
- Ally hazard: Death's Storm row 1 Decrease Damage Given is an OTHER_USER AOE_CIRCLE_SPAWN row with friendly fire none (=ALL), so allies inside the circle also take the debuff for its 2 rounds (the caster never does, §4b); nodes 06, 09 and 10 raise it on them too (30% → up to 40%). The pierce row (friendly fire ENEMIES) is unaffected. Positioning decides; not simulated.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Storm jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

