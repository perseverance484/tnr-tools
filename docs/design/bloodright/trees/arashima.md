# Arashima — Reaper's Tempest

**Bloodline:** Arashima (BR-005, rank A, `9F6Ruhuf82gSzpZcsUaPW`) · **Revision:** Draft 3 / Storm classification / forked tree · **Classification:** Storm (element) · **Engine status:** proposal_requires_resolver_adjustment

**Emphasis:** primary Lifesteal (sustain; the kit's identity, +10 ceiling) · secondary Decrease Damage Taken and Decrease Damage Given (co-primary fortress and suppression routes, +10 ceilings) · tertiary Damage (Storm AoE burst, +5 ceiling) and Increase Damage Given (glue across routes, +5 ceiling).

Stormsinger is the kit's identity: one 40 AP self-cast carries Lifesteal 40%, Increase Damage Given 35% and Decrease Damage Taken 35% for two rounds, so sustain is the primary emphasis and the lifesteal route is the deepest commitment (40% -> 50%, still under the 60% leech cap). Reapers Storm and Demons Strike are the only Damage rows (45 each, Storm, AoE circle spawn, 60 AP) and form the burst route. Death's Storm's Decrease Damage Given 30% is the kit's only enemy debuff and anchors the suppression route; its pierce row is unsupported and untouched. Increase Damage Given is kept as the Foundation-only support tag so that capstone secondaries never duplicate a sibling Hidden Art and every hybrid allocation stays non-dominated. 'Primary' here names the kit's identity, not the largest addition: the validated maxima are Lifesteal +10, DDT +10 and DDG +10, so the fortress and suppression routes reach the same ceiling as the sustain route, while Damage (+5 on two 45-power rows) and IDG (+5) are the lower-ceiling tags.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Storm-classified Arashima jutsu under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Tempest Hymn | Foundation | None | +2% Increase Damage Given (self buff); +2% Lifesteal (self buff) | Stormsinger / 2 |
| 02 | Gathering Thunderhead | Hidden Art | Tempest Hymn | +2 Damage power (damage) | Demons Strike, Reapers Storm / 2 |
| 03 | Sundered Sky | Advanced Art | Gathering Thunderhead | +3 Damage power (damage) | Demons Strike, Reapers Storm / 2 |
| 04 | Crimson Downpour | Hidden Art | Tempest Hymn | +3% Lifesteal (self buff) | Stormsinger / 1 |
| 05 | Reaper's Harvest | Advanced Art | Crimson Downpour | +5% Lifesteal (self buff); +3% Increase Damage Given (self buff) | Stormsinger / 2 |
| 06 | Stillness in the Squall | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Death’s Storm, Stormsinger / 2 |
| 07 | Stormwarden's Hide | Hidden Art | Stillness in the Squall | +3% Decrease Damage Taken (self buff) | Stormsinger / 1 |
| 08 | Unbroken Horizon | Advanced Art | Stormwarden's Hide | +5% Decrease Damage Taken (self buff); +3% Increase Damage Given (self buff) | Stormsinger / 2 |
| 09 | Deadwind Dirge | Hidden Art | Stillness in the Squall | +3% Decrease Damage Given (enemy debuff) | Death’s Storm / 1 |
| 10 | Silence After Thunder | Advanced Art | Deadwind Dirge | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff); +2% Lifesteal (self buff) | Death’s Storm, Stormsinger / 3 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Tempest Hymn** — The storm sings through Arashima blood; every verse is a wound and a drink. Stormsinger rows 1 (IDG 35%) and 0 (Lifesteal 40%), self buff, 2 rounds per 40 AP cast; no gates, no adverse rows.
- **Gathering Thunderhead** — Clouds mass over the field, heavy with what is about to fall. Reapers Storm and Demons Strike Damage 45 (Storm, AoE circle spawn, 60 AP); the pierce row on Death's Storm is unsupported.
- **Sundered Sky** — The whole sky comes down at once. Nothing beneath it is spared. Same two Storm Damage rows: 45 -> 50 with Gathering Thunderhead; both are AoE, so every enemy in the circle takes the full power.
- **Crimson Downpour** — The rain that follows the storm runs red, and it runs toward the singer. Stormsinger row 0 Lifesteal 40%; leech shares the 60%-of-damage cap with vamp, so 40 + 5 = 45% stays below it.
- **Reaper's Harvest** — What the storm cuts down, the reaper gathers in. Stormsinger Lifesteal 40% and IDG 35%; the full route reaches 50% lifesteal and 40% IDG, both under the 60% leech cap and the 100 cap.
- **Stillness in the Squall** — At the heart of the tempest there is a calm that belongs to Arashima alone. Stormsinger row 2 DDT 35% (self, 2 rounds) and Death's Storm row 1 DDG 30% (enemy, AoE, 2 rounds, debuff-prevent gated; ally hazard).
- **Stormwarden's Hide** — Years of standing in the gale leave skin the wind no longer bites. Stormsinger row 2 DDT 35% (self, 2 rounds); four stat types, so it covers every incoming damage row with a stat type; pierce bypasses DDT.
- **Unbroken Horizon** — The storm has raged all night; at dawn the line still holds. Stormsinger DDT 35% -> 45% on the full route and IDG 35% -> 40% with Tempest Hymn; both ride the same 2-round cast window.
- **Deadwind Dirge** — The wind after Death's Storm carries the strength out of every arm it touches. Death's Storm row 1 DDG 30%, 2 rounds, everyone in the circle (allies too: ally hazard); needs the 60 AP cast, debuff-prevent gated.
- **Silence After Thunder** — When the thunder stops, only the Arashima still has the will to strike. Death's Storm DDG 30% -> 40% on the full route (ally hazard in the circle); Stormsinger DDT and Lifesteal +2 each, below the +3 Hidden Arts.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | DDT | LS |
|---|---|---:|---:|---:|---:|---:|
| Reaper's Harvest (Sustain) | Tempest Hymn, Crimson Downpour, Reaper's Harvest, Stillness in the Squall | — | +5% | +2% | +2% | +10% |
| Sundered Sky (Burst) | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Stillness in the Squall | +5 | +2% | +2% | +2% | +2% |
| Unbroken Horizon (Fortress) | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon | — | +5% | +2% | +10% | +2% |
| Silence After Thunder (Suppression) | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder | — | +2% | +10% | +4% | +4% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Reaper's Harvest:** The full lifesteal route takes Stormsinger from 40% to 50% leech and 35% to 40% IDG for the same two-round window. The enhanced IDG lifts both Storm Damage rows and any normal jutsu that uses your highest offence stat or carries no element (not Death's Storm's pierce, which bypasses damage modifiers); the enhanced leech draws from nearly every damage row (its row lists all four stat types), including Death's Storm's 58-power pierce, which the engine feeds into lifesteal at full ratio. Stillness in the Squall is the fourth purchase: it adds 2% DDT on the same cast and 2% DDG on Death's Storm, rounding a duelist who out-sustains the exchange rather than ending it quickly.
- **Sundered Sky:** Damage +5 lifts Reapers Storm and Demons Strike from 45 to 50 power on every enemy in their circles, and the bloodline's own Storm IDG passive multiplies that raw power downstream. Tempest Hymn is a required ancestor and adds 2% IDG and 2% lifesteal; Stillness in the Squall is the fourth purchase for a little mitigation. This is the burst option: it gives up the deep sustain and the fortress entirely.
- **Unbroken Horizon:** The DDT route takes Stormsinger from 35% to 45% damage reduction for its two rounds, and the capstone's 3% IDG plus Tempest Hymn's 2% give 40% IDG on the same cast: a fortified-offence build that tanks the trade and answers it. Lifesteal stays at 42% and Death's Storm's debuff at 32%, so it is clearly not the sustain or suppression build.
- **Silence After Thunder:** The DDG route takes Death's Storm's enemy debuff from 30% to 40% on every enemy in its circle for two rounds, and the capstone's small DDT and lifesteal secondaries plus Tempest Hymn leave Stormsinger at 44% lifesteal, 37% IDG and 39% DDT. It suppresses groups rather than killing them; the alternative fourth purchase (Stormwarden's Hide instead of Tempest Hymn) is the pure turtle at 42% DDT / 40% DDG.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustain | Burst | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Stormsinger | 0 | Lifesteal | self | 40% | 50% (+10) | 42% (+2) | 42% (+2) | 44% (+4) |
| Stormsinger | 1 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 40% (+5) | 37% (+2) |
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
- Maximum individually achievable additions: Damage +5, Increase Damage Given +5%, Decrease Damage Given +10%, Decrease Damage Taken +10%, Lifesteal +10% (not jointly attainable)
- Supported rows in kit: 6 (DMG 2, DDG 1, DDT 1, IDG 1, LS 1)
- Strongest full build by row-weighted total: Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder (raw +20, row-weighted 20)
- Lowest row-weighted node: Crimson Downpour (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Death’s Storm#1

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Crimson Downpour | DMG +5, IDG +2, LS +5 |
| 2 | Tempest Hymn, Gathering Thunderhead, Sundered Sky, Stillness in the Squall | DMG +5, IDG +2, DDG +2, DDT +2, LS +2 |
| 3 | Tempest Hymn, Gathering Thunderhead, Crimson Downpour, Reaper's Harvest | DMG +2, IDG +5, LS +10 |
| 4 | Tempest Hymn, Gathering Thunderhead, Crimson Downpour, Stillness in the Squall | DMG +2, IDG +2, DDG +2, DDT +2, LS +5 |
| 5 | Tempest Hymn, Gathering Thunderhead, Stillness in the Squall, Stormwarden's Hide | DMG +2, IDG +2, DDG +2, DDT +5, LS +2 |
| 6 | Tempest Hymn, Gathering Thunderhead, Stillness in the Squall, Deadwind Dirge | DMG +2, IDG +2, DDG +5, DDT +2, LS +2 |
| 7 | Tempest Hymn, Crimson Downpour, Reaper's Harvest, Stillness in the Squall | IDG +5, DDG +2, DDT +2, LS +10 |
| 8 | Tempest Hymn, Crimson Downpour, Stillness in the Squall, Stormwarden's Hide | IDG +2, DDG +2, DDT +5, LS +5 |
| 9 | Tempest Hymn, Crimson Downpour, Stillness in the Squall, Deadwind Dirge | IDG +2, DDG +5, DDT +2, LS +5 |
| 10 | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon | IDG +5, DDG +2, DDT +10, LS +2 |
| 11 | Tempest Hymn, Stillness in the Squall, Stormwarden's Hide, Deadwind Dirge | IDG +2, DDG +5, DDT +5, LS +2 |
| 12 | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder | IDG +2, DDG +10, DDT +4, LS +4 |
| 13 | Stillness in the Squall, Stormwarden's Hide, Unbroken Horizon, Deadwind Dirge | IDG +3, DDG +5, DDT +10 |
| 14 | Stillness in the Squall, Stormwarden's Hide, Deadwind Dirge, Silence After Thunder | DDG +10, DDT +7, LS +2 |

## Design notes

- Node split: four routes map one-to-one onto the kit's four distinct non-glue tags (Lifesteal, Damage, DDT, DDG). Increase Damage Given appears only on Foundation 01 and as a +3 secondary on the lifesteal and DDT capstones, never on a Hidden Art, so no capstone secondary equals a sibling Hidden Art's value and all 14 full-budget allocations stay numerically non-dominated. Silence After Thunder's secondaries (+2 DDT, +2 Lifesteal) are deliberately one point below the +3 Hidden Arts for the same reason.
- Calibration against Taiyo Kami: Foundations +2/+2, Hidden Arts +2 Damage (2 rows) or +3 on a single-row percentage tag, capstones +3 Damage or +5 primary with a +3 (or two +2) secondaries. Damage reaches two rows here instead of Taiyo's three, so the +5 total is relatively slightly stronger per row (45 -> 50, +11%) and comparable per kit; a +3 Hidden Art (total +6) is the obvious tuning lever if the burst route under-performs in review.
- Interaction with the main tree and passives: Stormsinger's IDG, DDT and Lifesteal rows are self buffs with two-round durations, so enhancing them also reaches normal jutsu and weapons used inside that window, subject to efficiency matching (see risks): the Lifesteal row lists all four stat types and so draws from every damage row that declares a stat type plus all pierce (including Death's Storm's own unsupported pierce row, which the engine feeds into lifesteal); the DDT row lists the same four stat types and reduces every incoming damage row that declares a stat type but never pierce, which the engine applies after the damage-modifier pass (so no IDG, DDT or DDG node touches a pierce hit); the IDG row's single 'Highest' stat type reaches the kit's two Storm Damage rows and any damage row that uses the caster's highest offence stat or carries no element. The bloodline's own IDG passive (25% + 0.15/level on Water/Lightning/Storm/None) multiplies the enhanced Damage rows downstream. Death's Storm's DDG is an enemy debuff, so it also softens enemy normal jutsu (not enemy pierce) against allies. None of these downstream effects were simulated.
- Delivery and uptime: every Stormsinger-row node shares one 40 AP cast with a 7-round cooldown and a 2-round buff, so a sustain or fortress build's realised value is capped by that window; the Damage rows cost 60 AP on 7-round cooldowns and are AoE circle spawns, so their raw-power bonus is paid once per enemy hit; DDG requires landing the 60 AP Death's Storm and is debuff-prevent gated. Skill-tree effects (and therefore Bloodright potency) are skipped in RANKED_PVP and RANKED_SPARRING at the pin.
- Fourth-purchase choices: after any 3 BP route the natural fourth is the other Foundation (+2/+2 on two more rows). Hybrids with no Advanced Art (e.g. 01+02+04+06: +2 Damage, +5 Lifesteal, +2 IDG/DDT/DDG) and the all-defence 06+07+09+10 (+7 DDT, +10 DDG, +2 Lifesteal) are legal and non-dominated; 01+02+04+05 is the strongest unadvertised sustain build (+2 Damage, +10 Lifesteal, +5 IDG) at the cost of any mitigation.
- Presentation: the renderer prints full jutsu names for this kit because 'Reapers Storm' and 'Death's Storm' would both abbreviate to 'Storm', which is also the classification label; JSON and Markdown always carried full names.
- Open balance decision (user-owned, not applied in this draft): Sundered Sky is the lowest-value capstone by row weight (6 against 8, 8 and 9; full-build totals Burst 18 against 19, 19 and 20) and Unbroken Horizon's +3 IDG secondary ties Reaper's Harvest for the best IDG capstone. Options: raise Gathering Thunderhead to +3 Damage (burst route total +6, at the guardrail), or move the +3 IDG secondary from Unbroken Horizon onto Sundered Sky; or keep the present values for Taiyo Kami parity (Sovereign Sun +5 DDT / +3 IDG, Solar Cataclysm +3 Damage on three rows). Neither alternative was re-validated for non-dominance.

## Risks and unproven interactions

- Classification: Storm is not exclusive in the census (Godstorm Eclipse, Shinrai Ou and deferred Stormboat Willy carry Storm damage rows), and whether any NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carries Storm is unverified. The tree assumes a bloodline-scoped whole-kit classification; a bare element match would leak to those kits.
- Resolver: 4 of the 6 supported rows (all Stormsinger rows and Death's Storm DDG) have no element and fall back to None under the current resolver, so they are unreachable without the proposed classification change; reaching them with affectedElements including None would also reach every non-elemental row on any jutsu the player casts.
- Lifesteal cap: lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit. The route tops out at 50%, leaving 10 points of headroom; a player who also carries vamp from the normal tree or items may saturate the cap and lose part of the +10. Lifesteal requires both combatants alive and is blocked by healprevent on the caster. Verified at the pin: pierce is written through damageUser as consequence.damage with 'pierce' among its types (tags.ts 1539, 1566–1615); process.ts 563–585 runs pierce before the post-damage pass so that lifesteal includes it; the lifesteal handler (tags.ts 2028–2054) has no pierce exclusion, unlike recoil (1958–1959) and afterburn (1993–1994); and getEfficiencyRatio returns 1 for any pierce effect (3478–3479). Stormsinger's enhanced leech therefore also draws from Death's Storm's 58-power pierce at full ratio; at 50% it stays inside the cap.
- Efficiency matching (verified at the pin, tags.ts 3477–3510 and 97): a 'Highest' stat type resolves to the caster's highest offence stat, which realizeTag copies onto the effect from the user, and an effect with no elements carries the tag 'None'. Stormsinger's IDG row (statTypes ['Highest'], no elements) therefore matches the kit's own Storm damage rows (statTypes ['Highest'] on the same caster) and any damage row that uses that stat type or carries no element, but not a normal jutsu that uses a different single stat type and carries an element. The Lifesteal row lists all four stat types, so it matches every damage row that declares a stat type and all pierce (ratio forced to 1), missing only a stat-less elemental row; the DDT row lists the same four stat types and matches every incoming damage row that declares a stat type but never pierce: process.ts 418–432 and 563–575 apply pierce after the damage-modifier pass (480), so adjustDamageTaken (tags.ts 1002–1065) never sees a pierce consequence; IDG and DDG likewise never touch pierce. Per-row stat types are auditable in docs/design/bloodright/evidence/kit_snapshot.json; the kit dossier tables do not yet print them (extending audit_kits.py to emit statTypes/generalTypes for every kit is a tooling follow-up outside this tree's correction scope).
- Stacking: BATTLE_TAG_STACKING is true at the pin, so a Bloodright potency effect stacks with any other potency source rather than being deduplicated; the combined budget with a future normal-tree potency policy is unaudited.
- No adverse rows, hidden rows, item gates, mode restrictions or injected children exist in this kit (the one ally-hazard row is covered below); the unsupported drain, pierce, poison, increasepoolcost, shield and move rows are unchanged by every node.
- No combat simulation: non-dominance of the 14 allocations is an arithmetic result over per-row additions, not evidence of equal combat strength; AoE target counts, uptime, AP economy and the Storm IDG passive's multiplication were not modelled.
- Ally hazard: Death's Storm row 1 DDG is an AOE_CIRCLE_SPAWN row with friendly fire none (=ALL), so allies, and the caster if inside the circle, also take the debuff for its 2 rounds; nodes 06, 09 and 10 raise it on them too (30% -> up to 40%). The pierce row (friendly fire ENEMIES) is unaffected. Positioning decides; the route is worth less when allies share the circle. Not simulated.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Arashima jutsu inherit Storm potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

