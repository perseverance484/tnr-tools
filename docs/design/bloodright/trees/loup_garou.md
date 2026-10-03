# Loup-Garou — Blood and Moon

**Bloodline:** Loup-Garou (BR-042, rank D, `C4q1pAltRIEaI5WrNVAAC`) · **Revision:** Draft 3 / Loup-Garou classification / forked tree · **Classification:** Loup-Garou (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Self amplification — Increase Damage Given (Nature's Hunter self buff) · secondary Exposure — Increase Damage Taken (Life reaver) and Damage (Nature's Hunter) · tertiary Sustain — Heal (Nature's Hunter).

The kit has four supported rows, one per tag, on two single-target jutsu with cooldown 6: Nature's Hunter (A-rank, 60 AP, Jonin-gated) carries Damage 40 plus a 35% Increase Damage Given self buff and a static Heal 25 (250 HP per tick) for the 2 rounds after the cast; Life reaver (C-rank, 40 AP) carries a 35% Increase Damage Taken debuff for the 2 rounds after its cast. Buffs and debuffs never act in their cast round (tags.ts 925/1010) and cooldown 6 keeps the next Nature's Hunter outside the window, so the self buff never reaches the kit's own hit: it is primary because, on a Taijutsu bloodline with a 15% Taijutsu IDG passive, it adds 35% of the staged base to every element-less or Taijutsu non-pierce basic attack, weapon and normal-jutsu hit the wolf lands in those two rounds. Exposure is the other 2-round window and reaches Nature's Hunter when it is cast in either round after Life reaver; the damage row is one hit every 6 rounds, so they share second place. Heal is held at the +5 guardrail (+50 HP per tick) as tertiary. Absorb on Life reaver and the Wolf Companion summon are unsupported.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported rows, one per tag (Damage, Increase Damage Given and Heal on Nature's Hunter; Increase Damage Taken on Life reaver); the Wolf Companion summon and Life reaver's absorb are unsupported. Scent of Blood is a universal node (in all 8 legal 4-BP builds) because Hunter's Moon roots a 3-node chain, and no leaf Hidden Art under Hunter's Moon earns its cost: Heal there breaches the +5 guardrail beside Beast Unchained; IDG lifts the declared primary above +8 and duplicates Feral Frenzy; Damage +2 or IDT +3 reproduces Rending Claws' or Run to Ground's bonus vectors in the mixed builds (IDT +3 also lifts 01,04,06,leaf to IDT +8); Damage +3 or IDT +2 opens a second path to the +6/+7 maximum; smaller flats leave the leaf builds dominated; a Damage/IDT pair re-sells Scent of Blood. So every build buys Scent of Blood (Frenzy's only exposure). Three distinct complete builds (Burst, Exposure, Frenzy) exist; Burst and Exposure each have two fourth-purchase choices, Frenzy's is always Scent of Blood. 8 legal full-budget allocations, every node in a non-dominated one.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses are static additions to existing supported tags of Loup-Garou jutsu (bloodline-keyed classification, proposed extension) under the proposed classification behavior; no row's combat scope changes. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Scent of Blood | Foundation | None | +2% Increase Damage Taken (enemy debuff); +1 Damage power (damage) | Life reaver, Nature's Hunter / 2 |
| 02 | Rending Claws | Hidden Art | Scent of Blood | +2 Damage power (damage) | Nature's Hunter / 1 |
| 03 | Killing Bite | Advanced Art | Rending Claws | +3 Damage power (damage) | Nature's Hunter / 1 |
| 04 | Run to Ground | Hidden Art | Scent of Blood | +3% Increase Damage Taken (enemy debuff) | Life reaver / 1 |
| 05 | The Pack Closes | Advanced Art | Run to Ground | +2% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Life reaver, Nature's Hunter / 2 |
| 06 | Hunter's Moon | Foundation | None | +2% Increase Damage Given (self buff); +2 Heal power (self buff) | Nature's Hunter / 2 |
| 07 | Feral Frenzy | Hidden Art | Hunter's Moon | +3% Increase Damage Given (self buff) | Nature's Hunter / 1 |
| 08 | Beast Unchained | Advanced Art | Feral Frenzy | +3 Heal power (self buff); +3% Increase Damage Given (self buff) | Nature's Hunter / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Scent of Blood** — One drop on the wind and the quarry is already chosen. Life reaver exposure 35→37% (1 target, 2 rounds); Nature's Hunter damage 40→41 (Jonin-gated jutsu). 2 rows, no item gates, no adverse rows.
- **Rending Claws** — Flesh parts where the claws pass; the hunt leaves no clean wounds. Nature's Hunter damage 40→43 power with Scent of Blood (formula calc, Taijutsu / Speed, Strength). 1 row, one hit per 6 rounds.
- **Killing Bite** — The jaws close on the throat and the chase is over. Nature's Hunter damage 40→46 power on the full route (+6, the single-row guardrail). 1 row; route total is the only way to +6.
- **Run to Ground** — Tired prey stumbles. The wolf does not. Life reaver exposure 35→40% with Scent of Blood; adds to element-less or Taijutsu non-pierce hits on that target for 2 rounds. 1 row.
- **The Pack Closes** — Every howl answered; every flank taken. Nothing leaves the circle. Life reaver exposure 35→42% on the route (Taiyo Kami's +7 IDT ceiling); Nature's Hunter self buff 35→38%. 2 rows, both 2-round windows.
- **Hunter's Moon** — Under the autumn moon the blood runs hot and the wounds knit shut. Nature's Hunter self buff 35→37% and Heal 25→27 power (270 HP per tick, 2 rounds, before the 10% Increase Heal passive). 2 rows.
- **Feral Frenzy** — Reason leaves with the first taste of blood; only hunger steers the claws. Nature's Hunter self buff 35→40% with Hunter's Moon; raises element-less or Taijutsu non-pierce hits the caster lands in the 2 rounds after.
- **Beast Unchained** — The curse is no longer worn. It is answered, and it answers back. Nature's Hunter Heal 25→30 power (300 HP per tick, the +5 guardrail) and self buff 35→43% on the route. 2 rows, one 2-round window.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | HEAL |
|---|---|---:|---:|---:|---:|
| Killing Bite (Burst) | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | +6 | +2% | +2% | +2 |
| The Pack Closes (Exposure) | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | +1 | +5% | +7% | +2 |
| Beast Unchained (Frenzy) | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | +1 | +8% | +2% | +5 |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Killing Bite:** The +6 power route on Nature's Hunter (40→46 raw; the 15% Taijutsu passive then multiplies the hit by 1.15, and Scent of Blood's 37% exposure adds 37% of the staged base when Life reaver was cast in one of the two rounds before). Nature's Hunter's own buff never reaches this hit: it is live only on the two rounds after the cast. Hunter's Moon is the fourth purchase so the same cast also buffs 37% for the following two rounds and heals 270 HP per tick; Run to Ground (exposure 40%) is the all-offence alternative.
- **The Pack Closes:** Life reaver's exposure at 42% for the 2 rounds after its cast on one target, adding to the wolf's and its allies' element-less or Taijutsu non-pierce hits there, including Nature's Hunter when it follows in either of those rounds; then Nature's Hunter's own buff at 40% (3 from the capstone, 2 from Hunter's Moon) and 270 HP heal ticks for the 2 rounds after that. Rending Claws (damage 43) is the alternative fourth purchase for a solo hunter.
- **Beast Unchained:** Nature's Hunter's self buff at 43% and heal at 300 HP per tick for the 2 rounds after the cast: the werewolf adds 43% of the staged base to every element-less or Taijutsu non-pierce basic attack, weapon and normal jutsu in that window and shrugs off the trade. The buff never reaches Nature's Hunter's own hit, so this route's value is wholly on non-kit hits. Scent of Blood is the only possible fourth purchase (37% exposure, 41 damage); the build has no second route.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Frenzy |
|---|---:|---|---|---:|---:|---:|---:|
| Nature's Hunter | 0 | Damage | enemy | 40 | 46 (+6) | 41 (+1) | 41 (+1) |
| Nature's Hunter | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 43% (+8) |
| Nature's Hunter | 2 | Heal | self | 25 | 27 (+2) | 27 (+2) | 30 (+5) |
| Summon Wolf Companion | 0 | summon (unsupported) **adverse** | enemy | 75% | 75% | 75% | 75% |
| Life reaver | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 42% (+7) | 37% (+2) |
| Life reaver | 1 | absorb (unsupported) | self | 30% | 30% | 30% | 30% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions: Damage +6, Increase Damage Given +8%, Increase Damage Taken +7%, Heal +5 (not jointly attainable)
- Supported rows in kit: 4 (DMG 1, HEAL 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained (raw +16, row-weighted 16)
- Lowest row-weighted node: Rending Claws (2)

Validator warnings:

- universal node: 01 (Scent of Blood) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Scent of Blood, Rending Claws, Killing Bite, Run to Ground | DMG +6, IDT +5 |
| 2 | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | DMG +6, IDG +2, IDT +2, HEAL +2 |
| 3 | Scent of Blood, Rending Claws, Run to Ground, The Pack Closes | DMG +3, IDG +3, IDT +7 |
| 4 | Scent of Blood, Rending Claws, Run to Ground, Hunter's Moon | DMG +3, IDG +2, IDT +5, HEAL +2 |
| 5 | Scent of Blood, Rending Claws, Hunter's Moon, Feral Frenzy | DMG +3, IDG +5, IDT +2, HEAL +2 |
| 6 | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | DMG +1, IDG +5, IDT +7, HEAL +2 |
| 7 | Scent of Blood, Run to Ground, Hunter's Moon, Feral Frenzy | DMG +1, IDG +5, IDT +5, HEAL +2 |
| 8 | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | DMG +1, IDG +8, IDT +2, HEAL +5 |

## Design notes

- Node split: the roots mirror the kit's two faces. Scent of Blood (enemy-facing) raises Life reaver's exposure and Nature's Hunter's hit, then forks into Rending Claws → Killing Bite (damage) and Run to Ground → The Pack Closes (exposure). Hunter's Moon (self-facing) raises both of Nature's Hunter's self rows and runs one chain through Feral Frenzy → Beast Unchained. 2 Foundations, 3 Hidden Arts, 3 Advanced Arts; every Advanced Art is 3 BP deep; any two cost 5 BP (shared root) or 6 BP.
- Flats and reference reuse: Rending Claws → Killing Bite copies Taiyo's Crown of Cinders → Solar Cataclysm (+2/+3 Damage) verbatim, and Hunter's Moon (+2/+2) and the +3 Hidden Arts reuse Taiyo's Foundation and Hidden shapes. Departures: one 40-power row, so Scent of Blood's +1 makes the route +6 (the guardrail, as Dai Kenja's single damage row); IDT stops at Taiyo's +7 ceiling (2+3+2, 35→42%), so The Pack Closes carries +2 IDT/+3 IDG, as Eternal Noon's secondaries, not a +5 primary.
- IDG and Heal flats: Increase Damage Given is single-row and the bloodline's theme stat (15% Taijutsu passive), so the Frenzy chain carries 2+3+3 = +8 (35→43%), below the +10 guardrail that Dai Kenja's single IDG row uses, with +3 on The Pack Closes as that route's secondary (maximum 5 there with Hunter's Moon). Heal is single-row raw power at the +5 guardrail (2 on the Foundation, 3 on the capstone): 25→30 power, 250→300 HP per tick, so the self chain cannot be deeper than three nodes.
- Main tree and passives: the 15% Taijutsu passive is bloodline-sourced, so it multiplies the damage by 1.15 (tags.ts 937-960; gated on allowBloodlineDamageIncrease, true on the Hunter hit); jutsu-sourced buffs and exposure add power/100 of the staged base, and same-tag effects all apply (process.ts 1109-1117): a 43% buff beside another 35% IDG adds 78%. +6 raw on the 40 row beats +6 final damage. Both rows match element-less hits of any stat type plus Taijutsu elemental hits, never pierce.
- Delivery and uptime: both carriers single-target, range 4, cooldown 6; 350 chakra/stamina, -10 per jutsu level (100 at level 25, floor 0; actions.ts 773-784). Buffs/debuffs skip their cast round (tags.ts 925/1010) and live on the 2 following rounds: Life reaver (40 AP) in round R, Nature's Hunter (60 AP) in R+1 or R+2 so the hit lands in the exposure; buff and heal then cover the next 2 rounds. Each window: 2 of 6 rounds. Heal ticks 250 HP (275 with the 10% Increase Heal passive; 330 at +5).
- Fourth purchases: Burst (01,02,03) takes Hunter's Moon for a rounded cast (37% buff, 270 HP ticks) or Run to Ground for 40% exposure and no sustain. Exposure (01,04,05) takes Hunter's Moon (buff 40%, heal 270) or Rending Claws (damage 43). Frenzy (06,07,08) can only add Scent of Blood. The hybrids 01,02,04,06 and 01,02,06,07 are legal and non-dominated; 01,04,06,07 is dominated by The Pack Closes build, as expected when a hybrid skips its capstone. Nothing changes AP, cooldown or the summon.

## Risks and unproven interactions

- Classification: every supported row is element-less, so no existing element isolates this kit. Under the current resolver these rows are reachable only with affectedElements including None, which also reaches every non-elemental row on any jutsu the player casts. The tree assumes the proposed bloodline-keyed classification extension (label Loup-Garou). Normal-jutsu collision is unverified.
- Broad self amplification: Beast Unchained puts Nature's Hunter's Increase Damage Given at 43% for the 2 rounds after the cast; it adds 43% of the staged base to every element-less or Taijutsu non-pierce hit the caster lands there (basic attacks, weapons, normal jutsu), never the kit's own hit. Other IDG sources add their percentages (process.ts 1109-1117); the 15% passive multiplies on top.
- Broad enemy exposure: The Pack Closes puts Life reaver's Increase Damage Taken at 42% on one target for the 2 rounds after its cast; it adds 42% of the staged base to every qualifying hit from the kit, normal jutsu, weapons and allies (element-less hits of any stat, Taijutsu elemental hits, never pierce). Other exposure on that target adds too. One cast per 6 rounds.
- Value decision (user-owned): node for node both capstones carry +3 IDG, but at build level the self route stacks the IDG maximum (+8) and the only Heal maximum (+5) in Beast Unchained (row-weighted 16 vs 15); the exposure route (+7 IDT, +5 IDG, no Heal) is the counterweight. In-guardrail alternatives: IDG +10 (Feral Frenzy +3, Beast Unchained +5) or IDT +8 (Run to Ground +3, The Pack Closes +3).
- Damage route (user-owned): the hit is formula-calculated, x1.15 by the Taijutsu passive, raised by live exposure, never by its own buff; +6 raw is not +6 damage. One hit per 6 rounds leaves Killing Bite the weakest capstone (row-weighted 12 vs 15/16; bare +3 on one row; Dai Kenja's Breaking Point pairs +3 Damage with +2 IDG). Option: a +2 secondary (IDG or IDT) on Killing Bite, Damage kept at +6.
- Heal and targeting: Heal (rounds 2) ticks on the 2 rounds after the cast (tags.ts 1763-1767), power x10 HP; the 10% Increase Heal passive adds 10% per tick (tags.ts 1117-1128), off in ranked (routers/combat.ts 3051-3069). Both carriers are OTHER_USER: aimed at an ally, Nature's Hunter's Damage (friendly fire ALL) hits it, buff and heal still land on the caster, and Life reaver exposes it.
- Unsupported rows: the Wolf Companion summon (75% at level 25, marked adverse in the dossier as an enemy-side summon row) and Life reaver's 30% absorb receive nothing. No ally-hazard, hidden, item-gated or mode-restricted rows exist in this kit. No combat simulation was performed.
- Rank gate: Nature's Hunter is requiredRank JONIN in the snapshot (Life reaver GENIN), so Hunter's Moon, Feral Frenzy, Beast Unchained, Rending Claws and Killing Bite are inert below Jonin, and Scent of Blood, Run to Ground and The Pack Closes act only through Life reaver's exposure until then. A realized-value restriction, not an item gate: the kit has no item gates.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Loup-Garou jutsu inherit Loup-Garou potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

