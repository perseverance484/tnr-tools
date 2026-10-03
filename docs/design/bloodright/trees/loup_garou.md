# Loup-Garou — Blood and Moon

**Bloodline:** Loup-Garou (BR-042, rank D, `C4q1pAltRIEaI5WrNVAAC`) · **Revision:** Draft 4 / Loup-Garou classification extension / forked tree (RUL-2026-10-03-005 recalibration) · **Classification:** Loup-Garou (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary Self amplification — Increase Damage Given (Nature's Hunter self buff) · secondary Exposure — Increase Damage Taken (Life reaver) and Damage (Nature's Hunter) · tertiary Sustain — Heal (Nature's Hunter).

The kit has four supported rows, one per tag, on two single-target jutsu with cooldown 6: Nature's Hunter (A-rank, 60 AP, Jonin-gated) carries Damage 40 plus a 35% Increase Damage Given self buff and a static Heal 25 (250 HP per tick) for the 2 rounds after the cast; Life reaver (C-rank, 40 AP) carries a 35% Increase Damage Taken debuff for the 2 rounds after its cast. Buffs and debuffs never act in their cast round (tags.ts 925/1010) and cooldown 6 keeps the next Nature's Hunter outside the window, so the self buff never reaches the kit's own hit: it is primary because, on a Taijutsu bloodline with a 15% Taijutsu IDG passive, it multiplies every element-less or Taijutsu non-pierce basic attack, weapon and normal-jutsu hit the wolf lands in those two rounds by 1 + its percentage. Exposure is the other 2-round window and reaches Nature's Hunter when it is cast in either round after Life reaver; the damage row is one hit every 6 rounds, so they share second place. Heal is held to +5% (+50 HP per tick) as the Frenzy capstone's secondary. Absorb on Life reaver and the Wolf Companion summon are unsupported.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported rows, one per tag, on two casts (Damage, Increase Damage Given and Heal on Nature's Hunter; Increase Damage Taken on Life reaver); the Wolf Companion summon and Life reaver's absorb are unsupported. Three distinct routes exist: Burst (Damage), Exposure (Increase Damage Taken) and Frenzy (Increase Damage Given, with Heal as the secondary on the same Nature's Hunter self window). A fourth route or a leaf Hidden Art under Hunter's Moon would either repeat an existing single-row vector (Damage, Increase Damage Given or Increase Damage Taken) or split Heal from the buff it shares a cast and window with, leaving a capstone on one static row worth 10 HP per tick per +1%; that filler is declined. Scent of Blood is a universal node (in all 8 legal 4-BP builds) because Hunter's Moon roots a single 3-node chain. Burst and Exposure each have two fourth-purchase choices; Frenzy's is always Scent of Blood.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Loup-Garou-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Scent of Blood | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Life reaver / 1 |
| 02 | Rending Claws | Hidden Art | Scent of Blood | +2 Damage (damage) | Nature's Hunter / 1 |
| 03 | Killing Bite | Advanced Art | Rending Claws | +3 Damage (damage) | Nature's Hunter / 1 |
| 04 | Run to Ground | Hidden Art | Scent of Blood | +3% Increase Damage Taken (enemy debuff) | Life reaver / 1 |
| 05 | The Pack Closes | Advanced Art | Run to Ground | +5% Increase Damage Taken (enemy debuff); +3% Increase Damage Given (self buff) | Life reaver, Nature's Hunter / 2 |
| 06 | Hunter's Moon | Foundation | None | +2% Increase Damage Given (self buff); +2% Heal (self buff) | Nature's Hunter / 2 |
| 07 | Feral Frenzy | Hidden Art | Hunter's Moon | +3% Increase Damage Given (self buff) | Nature's Hunter / 1 |
| 08 | Beast Unchained | Advanced Art | Feral Frenzy | +5% Increase Damage Given (self buff); +3% Heal (self buff) | Nature's Hunter / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Scent of Blood** — One drop on the wind and the quarry is already chosen. Life reaver exposure 35 → 37% (1 target, 2 rounds). 1 row, no item gates, no adverse rows.
- **Rending Claws** — Flesh parts where the claws pass; the hunt leaves no clean wounds. Nature's Hunter Damage 40 → 42 EP (formula calc, Taijutsu / Speed, Strength). 1 row, one hit per 6 rounds.
- **Killing Bite** — The jaws close on the throat and the chase is over. Route total +5 Damage: Nature's Hunter 40 → 45 EP. 1 row, Jonin-gated jutsu.
- **Run to Ground** — Tired prey stumbles. The wolf does not. Life reaver exposure 37 → 40% with Scent of Blood; amplifies element-less or Taijutsu non-pierce hits on that target for 2 rounds. 1 row.
- **The Pack Closes** — Every howl answered; every flank taken. Nothing leaves the circle. Route total +10%: Life reaver exposure 35 → 45%; Nature's Hunter self buff +3% (40% with Hunter's Moon). 2 rows, both 2-round windows.
- **Hunter's Moon** — Under the autumn moon the blood runs hot and the wounds knit shut. Nature's Hunter self buff 35 → 37% and Heal 25 → 27 (270 HP per tick, 2 rounds, before the 10% Increase Heal passive). 2 rows.
- **Feral Frenzy** — Reason leaves with the first taste of blood; only hunger steers the claws. Nature's Hunter self buff 37 → 40% with Hunter's Moon; raises element-less or Taijutsu non-pierce hits the caster lands in the 2 rounds after.
- **Beast Unchained** — The curse is no longer worn. It is answered, and it answers back. Route total +10%: Nature's Hunter self buff 35 → 45%; Heal 25 → 30 with Hunter's Moon (300 HP per tick). 2 rows, one 2-round window.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | HEAL |
|---|---|---:|---:|---:|---:|
| Killing Bite (Burst) | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | +5 | +2% | +2% | +2% |
| The Pack Closes (Exposure) | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | — | +5% | +10% | +2% |
| Beast Unchained (Frenzy) | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | — | +10% | +2% | +5% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Killing Bite:** +5 Damage on Nature's Hunter (40 → 45 EP; the 15% Taijutsu passive then multiplies the hit by 1.15, and Scent of Blood's 37% exposure multiplies it by 1.37 when Life reaver was cast in one of the two rounds before). Nature's Hunter's own buff never reaches this hit: it is live only on the two rounds after the cast. Hunter's Moon is the fourth purchase so the same cast also buffs 37% for the following two rounds and heals 270 HP per tick; Run to Ground (exposure 40%) is the all-offence alternative.
- **The Pack Closes:** Life reaver's exposure at 45% for the 2 rounds after its cast on one target, adding to the wolf's and its allies' element-less or Taijutsu non-pierce hits there, including Nature's Hunter when it follows in either of those rounds; then Nature's Hunter's own buff at 40% (3 from the capstone, 2 from Hunter's Moon) and 270 HP heal ticks for the 2 rounds after that. Rending Claws (Nature's Hunter 42 EP) is the alternative fourth purchase for a solo hunter.
- **Beast Unchained:** Nature's Hunter's self buff at 45% and heal at 300 HP per tick for the 2 rounds after the cast: every element-less or Taijutsu non-pierce basic attack, weapon and normal jutsu the werewolf lands in that window is multiplied by 1.45 and shrugs off the trade. The buff never reaches Nature's Hunter's own hit, so this route's value is wholly on non-kit hits. Scent of Blood is the only possible fourth purchase (exposure 37%); the build has no second route.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Frenzy |
|---|---:|---|---|---:|---:|---:|---:|
| Nature's Hunter | 0 | Damage | enemy | 40 | 45 (+5) | 40 | 40 |
| Nature's Hunter | 1 | Increase Damage Given | self | 35% | 37% (+2) | 40% (+5) | 45% (+10) |
| Nature's Hunter | 2 | Heal | self | 25 | 27 (+2) | 27 (+2) | 30 (+5) |
| Summon Wolf Companion | 0 | summon (unsupported) **adverse** | enemy | 75% | 75% | 75% | 75% |
| Life reaver | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) |
| Life reaver | 1 | absorb (unsupported) | self | 30% | 30% | 30% | 30% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 7; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +5 Damage, +10% Increase Damage Given, +10% Increase Damage Taken, +5% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Killing Bite: +5 Damage (0 + 2 + 3; on band)
  - Route The Pack Closes: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Beast Unchained: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 4 (DMG 1, HEAL 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon (raw +17, row-weighted 17)
- Lowest row-weighted node: Scent of Blood (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Scent of Blood) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Scent of Blood, Rending Claws, Killing Bite, Run to Ground | +5 Damage, +5% IDT |
| 2 | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | +5 Damage, +2% IDG, +2% IDT, +2% HEAL |
| 3 | Scent of Blood, Rending Claws, Run to Ground, The Pack Closes | +2 Damage, +3% IDG, +10% IDT |
| 4 | Scent of Blood, Rending Claws, Run to Ground, Hunter's Moon | +2 Damage, +2% IDG, +5% IDT, +2% HEAL |
| 5 | Scent of Blood, Rending Claws, Hunter's Moon, Feral Frenzy | +2 Damage, +5% IDG, +2% IDT, +2% HEAL |
| 6 | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | +5% IDG, +10% IDT, +2% HEAL |
| 7 | Scent of Blood, Run to Ground, Hunter's Moon, Feral Frenzy | +5% IDG, +5% IDT, +2% HEAL |
| 8 | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | +10% IDG, +2% IDT, +5% HEAL |

## Design notes

- Node split: the roots mirror the kit's two faces. Scent of Blood (enemy-facing) raises Life reaver's exposure, then forks into Rending Claws → Killing Bite (Damage) and Run to Ground → The Pack Closes (exposure). Hunter's Moon (self-facing) raises both of Nature's Hunter's self rows and runs one chain through Feral Frenzy → Beast Unchained. 2 Foundations, 3 Hidden Arts, 3 Advanced Arts; every Advanced Art is 3 BP deep; any two cost 5 BP (shared root) or 6 BP.
- Recalibration (RUL-2026-10-03-005): Scent of Blood's +1 Damage is removed, so Burst is the default +5 route (Rending Claws +2, Killing Bite +3; Nature's Hunter 40 → 45 EP); The Pack Closes' Increase Damage Taken rises from +2% to +5%, so Exposure lands on +10% (Scent of Blood +2%, Run to Ground +3%, The Pack Closes +5%; Life reaver 35 → 45%); Beast Unchained now leads with Increase Damage Given, raised from +3% to +5%, so Frenzy lands on +10% (Hunter's Moon +2%, Feral Frenzy +3%, Beast Unchained +5%; 35 → 45%) with Heal +3% as its secondary.
- Maxima over every legal allocation: Damage +5, Increase Damage Given +10% (+5% on the Exposure build: The Pack Closes' +3% secondary and Hunter's Moon), Increase Damage Taken +10%, Heal +5%. Heal is a static row: each +1% adds 1 to its 25 base (10 HP per tick), so +5% is 250 → 300 HP per tick (display noted in OPEN_DECISIONS D18).
- Main tree and passives: the 15% Taijutsu passive is bloodline-sourced and applies last in the damage pipeline (×1.15; process.ts 1592–1825; gated on allowBloodlineDamageIncrease, true on the Hunter hit); jutsu-sourced buffs and exposure each multiply the hit in turn (×(1 + p/100)), and same-tag effects all apply (process.ts 1109-1117): a 45% buff beside another 35% IDG gives ×1.45 × 1.35 ≈ ×1.96. Both rows match element-less hits of any stat type plus Taijutsu elemental hits, never pierce.
- Delivery and uptime: both carriers single-target, range 4, cooldown 6; 350 chakra/stamina, -10 per jutsu level (100 at level 25, floor 0; actions.ts 773-784). Buffs/debuffs skip their cast round (tags.ts 925/1010) and live on the 2 following rounds: Life reaver (40 AP) in round R, Nature's Hunter (60 AP) in R+1 or R+2 so the hit lands in the exposure; buff and heal then cover the next 2 rounds. Each window: 2 of 6 rounds. Heal ticks 250 HP (275 with the 10% Increase Heal passive; 330 at +5%).
- Fourth purchases: Burst (01,02,03) takes Hunter's Moon for a rounded cast (37% buff, 270 HP ticks) or Run to Ground for 40% exposure and no sustain. Exposure (01,04,05) takes Hunter's Moon (buff 40%, heal 270 HP) or Rending Claws (Nature's Hunter 42 EP). Frenzy (06,07,08) can only add Scent of Blood. The hybrids 01,02,04,06 and 01,02,06,07 are legal and non-dominated; 01,04,06,07 is dominated by The Pack Closes build, as expected when a hybrid skips its capstone. Nothing changes AP, cooldown or the summon.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Loup-Garou' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. Potency reaches matching supported tags on every jutsu given that classification, whatever its source; all three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Broad self amplification: Beast Unchained puts Nature's Hunter's Increase Damage Given at 45% for the 2 rounds after the cast; it multiplies every element-less or Taijutsu non-pierce hit the caster lands there by 1.45 (basic attacks, weapons, normal jutsu), never the kit's own hit. Other IDG sources each multiply in turn (process.ts 1109-1117); the 15% passive applies last.
- Broad enemy exposure: The Pack Closes puts Life reaver's Increase Damage Taken at 45% on one target for the 2 rounds after its cast; it multiplies every qualifying hit from the kit, normal jutsu, weapons and allies (element-less hits of any stat, Taijutsu elemental hits, never pierce) by 1.45. Other exposure on that target compounds with it. One cast per 6 rounds.
- Value (user-owned): Frenzy holds the Increase Damage Given maximum (+10%) and the Heal maximum (+5%) on one cast; Exposure (+10% IDT, +5% IDG with Hunter's Moon) is the counterweight.
- Damage route (user-owned): the hit is formula-calculated, ×1.15 by the Taijutsu passive, raised by live exposure, never by its own buff; +5 EP is not +5 damage. One hit per 6 rounds leaves Killing Bite the weakest capstone (+3 Damage on one row). Option: a +2% secondary (IDG or IDT) on Killing Bite, both within the +10% ceiling; Damage stays at the +5 ceiling.
- Heal and targeting: Heal (rounds 2) ticks on the 2 rounds after the cast (tags.ts 1763-1767), ×10 HP per point; the 10% Increase Heal passive adds 10% per tick (tags.ts 1117-1128), off in ranked (routers/combat.ts 3051-3069). Both carriers are OTHER_USER: aimed at an ally, Nature's Hunter's Damage (friendly fire ALL) hits it, buff and heal still land on the caster, and Life reaver exposes it.
- Unsupported rows: the Wolf Companion summon (75% at level 25, marked adverse in the dossier as an enemy-side summon row) and Life reaver's 30% absorb receive nothing. No ally-hazard, hidden, item-gated or mode-restricted rows exist in this kit. No combat simulation was performed.
- Rank gate: Nature's Hunter is requiredRank JONIN in the snapshot (Life reaver GENIN), so Hunter's Moon, Feral Frenzy, Beast Unchained, Rending Claws, Killing Bite and The Pack Closes' IDG secondary are inert below Jonin; Scent of Blood, Run to Ground and The Pack Closes' exposure act through Life reaver. A realized-value restriction, not an item gate: the kit has no item gates.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Loup-Garou-classified jutsu (requires classification extension). Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

