# Loup-Garou — Blood and Moon

**Bloodline:** Loup-Garou (BR-042, rank D, `C4q1pAltRIEaI5WrNVAAC`) · **Revision:** Draft 1 / Loup-Garou classification / forked tree · **Classification:** Loup-Garou (bloodline-keyed extension) · **Engine status:** proposal_requires_resolver_adjustment_and_classification_extension

**Emphasis:** primary Self amplification — Increase Damage Given (Nature's Hunter self buff) · secondary Exposure — Increase Damage Taken (Life reaver) and Damage (Nature's Hunter) · tertiary Sustain — Heal (Nature's Hunter).

The kit has four supported rows, one per tag, on two single-target jutsu with cooldown 6: Nature's Hunter (A-rank, 60 AP) carries Damage 40, a 35% Increase Damage Given self buff for 2 rounds and a static Heal 25 (250 HP per tick) for 2 rounds; Life reaver (C-rank, 40 AP) carries a 35% Increase Damage Taken debuff for 2 rounds. The bloodline is Taijutsu with a 15% Taijutsu Increase Damage Given passive, so the self buff is the lever that scales every element-less or Taijutsu hit the wolf lands in its window and is primary. Exposure is the other 2-round window and the one damage row is a single hit every 6 rounds, so they share second place; Heal is held at the +5 guardrail (+50 HP per tick) as tertiary. Absorb on Life reaver and the Wolf Companion summon are unsupported.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on four rows, one row each (Damage, Increase Damage Given and Heal on Nature's Hunter; Increase Damage Taken on Life reaver); the Wolf Companion summon and Life reaver's absorb are unsupported. The enemy-facing root (Scent of Blood) forks into a damage route and an exposure route; the self-facing root (Hunter's Moon) is a single Foundation → Hidden → Advanced chain because its two rows share one cast and Heal is exhausted at +5 (the guardrail) after two purchases, so a second sustain Hidden Art or capstone would have to breach it or carry only Increase Damage Given, which would duplicate Feral Frenzy and open a second path to the IDG maximum. A damage or exposure branch under Hunter's Moon is structurally legal but would twin Rending Claws or Run to Ground on the same single rows, so it is declined. Three distinct complete builds (Burst, Exposure, Frenzy) exist; Burst and Exposure each have two fourth-purchase choices, Frenzy's fourth purchase is always Scent of Blood. 8 legal full-budget allocations, every node in a non-dominated one.

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

- **Scent of Blood** — One drop on the wind and the quarry is already chosen. Life reaver exposure 35→37% (one target, 2 rounds); Nature's Hunter damage 40→41 power. 2 rows, no gates, no adverse rows.
- **Rending Claws** — Flesh parts where the claws pass; the hunt leaves no clean wounds. Nature's Hunter damage 40→43 power with Scent of Blood (formula calc, Taijutsu / Speed, Strength). 1 row, one hit per 6 rounds.
- **Killing Bite** — The jaws close on the throat and the chase is over. Nature's Hunter damage 40→46 power on the full route (+6, the single-row guardrail). 1 row; route total is the only way to +6.
- **Run to Ground** — Tired prey stumbles. The wolf does not. Life reaver exposure 35→40% with Scent of Blood; amplifies element-less or Taijutsu non-pierce hits on that target for 2 rounds. 1 row.
- **The Pack Closes** — Every howl answered; every flank taken. Nothing leaves the circle. Life reaver exposure 35→42% on the route (Taiyo Kami's +7 IDT ceiling); Nature's Hunter self buff 35→38%. 2 rows, both 2-round windows.
- **Hunter's Moon** — Under the autumn moon the blood runs hot and the wounds knit shut. Nature's Hunter self buff 35→37% and Heal 25→27 power (270 HP per tick, 2 rounds, before the 10% Increase Heal passive). 2 rows.
- **Feral Frenzy** — Reason leaves with the first taste of blood; only hunger steers the claws. Nature's Hunter self buff 35→40% with Hunter's Moon; raises every element-less or Taijutsu non-pierce hit the caster lands for 2 rounds.
- **Beast Unchained** — The curse is no longer worn. It is answered, and it answers back. Nature's Hunter Heal 25→30 power (300 HP per tick, the +5 guardrail) and self buff 35→43% on the route. 2 rows, one cast, one 2-round window

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | HEAL |
|---|---|---:|---:|---:|---:|
| Killing Bite (Burst) | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | +6 | +2% | +2% | +2 |
| The Pack Closes (Exposure) | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | +1 | +5% | +7% | +2 |
| Beast Unchained (Frenzy) | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | +1 | +8% | +2% | +5 |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Killing Bite:** The +6 power route on Nature's Hunter (40→46 before the Taijutsu Increase Damage Given passive and the buff multiply it) with Scent of Blood's 37% exposure. Hunter's Moon is the fourth purchase so the same cast also buffs 37% and heals 270 HP per tick; Run to Ground (exposure 40%) is the all-offence alternative.
- **The Pack Closes:** Life reaver's exposure at 42% for 2 rounds on one target, amplifying the wolf's and its allies' element-less or Taijutsu hits, with Nature's Hunter's self buff at 40% (3 from the capstone, 2 from Hunter's Moon) and 270 HP heal ticks. Rending Claws (damage 43) is the alternative fourth purchase for a solo hunter.
- **Beast Unchained:** Nature's Hunter's self buff at 43% and heal at 300 HP per tick for its 2 rounds: the werewolf hits harder with everything and shrugs off the trade. Scent of Blood is the only possible fourth purchase (37% exposure, 41 damage); the build has no second route.

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
- Damage and IDT flats: Damage reaches one 40-power row, so the route is 1+2+3 = +6 (the guardrail; Dai Kenja's single damage row uses the same total) and the Foundation's +1 is the sliver that keeps the Taiyo +2/+3 Hidden/Advanced shape. Increase Damage Taken is a single row but broad exposure, so it is held to Taiyo Kami's +7 IDT ceiling (2+3+2, 35→42%): the Hidden Art at the single-row +3, the capstone's +2 IDT paired with +3 IDG as in Taiyo's Eternal Noon.
- IDG and Heal flats: Increase Damage Given is single-row and the bloodline's theme stat (15% Taijutsu passive), so the Frenzy chain carries 2+3+3 = +8 (35→43%), below the +10 guardrail that Dai Kenja's single IDG row uses, with +3 on The Pack Closes as that route's secondary (maximum 5 there with Hunter's Moon). Heal is single-row raw power at the +5 guardrail (2 on the Foundation, 3 on the capstone): 25→30 power, 250→300 HP per tick, so the self chain cannot be deeper than three nodes.
- Main tree and passives: the 15% Taijutsu IDG passive and Nature's Hunter's own buff each add percentage points of the staged base to a qualifying hit, so +6 power on the 40 row is worth more than +6 after them. The self buff (statTypes Taijutsu, no element) multiplies every element-less damage effect of any stat type the caster deals in its 2 rounds (basic attacks, weapons, non-elemental jutsu) plus Taijutsu elemental hits; not other elemental hits or pierce. Life reaver's exposure filters alike
- Delivery and uptime: both carriers are single-target, range 4, cooldown 6, 350 chakra and 350 stamina. Nature's Hunter costs 60 AP and Life reaver 40 AP, so both fit one round, but whether a same-round buff or debuff already applies to that round's hits was not verified; windows are 2 following rounds. One cast per 6 rounds means at most 2 of 6 rounds carry the buff, heal ticks or exposure. Heal is static ×10 (250 HP per tick); the 10% Increase Heal passive adjusts heal_hp: ~275 now, 330 at +5
- Fourth purchases: Burst (01,02,03) takes Hunter's Moon for a rounded cast (37% buff, 270 HP ticks) or Run to Ground for 40% exposure and no sustain. Exposure (01,04,05) takes Hunter's Moon (buff 40%, heal 270) or Rending Claws (damage 43). Frenzy (06,07,08) can only add Scent of Blood. The hybrids 01,02,04,06 and 01,02,06,07 are legal and non-dominated; 01,04,06,07 is dominated by The Pack Closes build, as expected when a hybrid skips its capstone. Nothing changes AP, cooldown or the summon.

## Risks and unproven interactions

- Classification: every supported row is element-less, so no existing element isolates this kit. Under the current resolver these rows are reachable only with affectedElements including None, which also reaches every non-elemental row on any jutsu the player casts. The tree assumes the proposed bloodline-keyed classification extension (label Loup-Garou). Normal-jutsu collision is unverified.
- Broad self amplification: Beast Unchained puts Nature's Hunter's Increase Damage Given at 43% for 2 rounds; that percentage multiplies every element-less or Taijutsu non-pierce hit the caster lands in the window from any source (basic attacks, weapons, normal jutsu), not only the kit. BATTLE_TAG_STACKING is on at the pin, so it stacks with the 15% Taijutsu passive and other IDG sources.
- Broad enemy exposure: The Pack Closes puts Life reaver's Increase Damage Taken at 42% for 2 rounds on one target; the added points amplify every qualifying hit from the kit, normal jutsu, weapons and allies (element-less hits of any stat type, Taijutsu elemental hits, pierce excluded). It stacks with other exposure on that target. One cast per 6 rounds limits self-stacking.
- Value decision (user-owned): IDG route maximum is +8, not the +10 guardrail Dai Kenja's single IDG row uses, so the self-facing capstone does not out-bid the exposure capstone on the theme stat; +10 (Feral Frenzy +3, Beast Unchained +5) stays inside the guardrail if a stronger Frenzy route is preferred. IDT is held at Taiyo Kami's +7; +8 (Run to Ground +3, The Pack Closes +3) is the alternative.
- Damage is formula-calculated (sqrt stat scaling on Taijutsu / Speed, Strength) and then multiplied by the Taijutsu IDG passive and any active buff or exposure, so +6 raw power is not a linear +6 damage. The damage route is one hit every 6 rounds, so Killing Bite is the weakest capstone in reach (6 raw on 1 row) and is kept only because the kit has no other burst lever.
- Heal timing and ticks: Nature's Hunter's Heal has rounds 2, so by the heal handler it applies on following rounds, read here as two ticks of power ×10 HP; the tick count and whether the 10% Increase Heal passive adjusts each tick were not simulated. Heal is a self row on an OTHER_USER jutsu, so it needs a legal enemy target to be cast.
- Unsupported rows: the Wolf Companion summon (75% at level 25, marked adverse in the dossier as an enemy-side summon row) and Life reaver's 30% absorb receive nothing. No ally-hazard, hidden, item-gated or mode-restricted rows exist in this kit. No combat simulation was performed.

## Limits

- Proposed potency classification behavior; not implemented or verified in the live engine.
- All existing supported tags of Loup-Garou jutsu inherit Loup-Garou potency eligibility; original combat elements and target scopes stay intact.
- Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power, not final-damage percentages; percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

