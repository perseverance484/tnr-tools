# Loup-Garou — Blood and Moon

**Bloodline:** Loup-Garou (BR-042, rank D, `C4q1pAltRIEaI5WrNVAAC`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Loup-Garou classification / forked tree · **Classification:** Loup-Garou (classification extension) · **Engine status:** proposal_requires_jutsu_classification_resolver_and_classification_extension

**Emphasis:** primary The hunt's two windows — Increase Damage Given (Nature's Hunter self buff) and Increase Damage Taken (Life reaver), one high-leverage 2-round window each · secondary The kill that feeds — Damage on Nature's Hunter's strike (40 → 43, Killing Bite only, no tier crossed) with the same cast's Heal as the route's setup and rider · tertiary Sustain — Nature's Hunter's static Heal (Rending Claws, Killing Bite and Hunter's Moon; 250 → 330 HP per tick at most).

Four supported rows, one per tag, on two single-target cooldown-6 casts. Nature's Hunter (60 AP, Jonin) strikes for 40 EP and gives the caster a 35% Increase Damage Given buff and a 250 HP static Heal tick for the 2 rounds after; Life reaver (40 AP) puts 35% Increase Damage Taken on one target for the 2 rounds after. Neither window acts in its cast round, so the buff never reaches the strike, while the exposure does when Life reaver comes first. The two windows are the kit's leverage: each multiplies every element-less or Taijutsu non-pierce hit in it (the exposure also allies' hits and the strike), and both together cost 100 AP. The tree gives each phase of the hunt one capstone: the strike (Killing Bite), the mark (The Pack Closes) and the frenzy after the strike (Beast Unchained). Absorb and the Wolf Companion summon are unsupported.

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Scent of Blood | Foundation | How do I bring down the marked quarry: kill and feed on it myself, or open it to the pack? |
| Hunter's Moon | Foundation | How do I unleash the beast in myself? |
| Killing Bite | Advanced Art | burst that feeds: the strike's flat-Damage payoff and the kit's largest heal on one cast (the sustain hunter) |
| The Pack Closes | Advanced Art | exposure: one marked target takes more from every attacker, allies included |
| Beast Unchained | Advanced Art | sustained amplification: the frenzy after the strike, every own hit on any target |

**Director review recommended:** Two departures to confirm; neither changes the graph. (1) Exposure: The Pack Closes keeps single-row team exposure at +10% (Life reaver 35 → 45% on one target; ×1.45 / ×1.35 ≈ ×1.074 on every qualifying non-pierce hit from the whole party, the strike included), twice the +5% exposure maximum of Blood-Enchanted Eyes and Shakunetsu Sakura. Confirm it with the roster's other exposure routes above +5%, or trim The Pack Closes to +3% (route +8%, Life reaver 43%). (2) Damage: Killing Bite's +3 on Nature's Hunter (40 → 43, still Normal) is one above the anchors' +2, kept because it is the kit's only Damage row and strikes once per 6 rounds; the lever is Killing Bite +2 (40 → 42). Beast Unchained's bare +10% self buff (one row, 35 → 45%) mirrors The Pack Closes and would move with it (Beast Unchained +3%, route +8%).

- Concern: Killing Bite is the sustain route and lighter in throughput than The Pack Closes solo or in a team: with Hunter's Moon as the fourth its strike is 43 × 1.37 ≈ 58.9 (60.2 with the Run to Ground fourth instead, at 310 HP ticks) against The Pack Closes' 40 × 1.45 = 58.0, but the 45% mark is ×1.058 ahead on every other hit on the target. Its case is +120 HP per cast (330 against 270 HP per tick, both with Hunter's Moon) plus that slightly harder strike; Heal at 10 HP per tick per point is low-leverage.
- Concern: Beast Unchained is a bare single-row +10% self buff (Nature's Hunter 35 → 45%) whose only rider is Hunter's Moon's +2% Heal; neither anchor has one (Shakunetsu's +10% route carries a +5% Heal rider, Arashima stops at +8%). It stays because it is one self row on a 2-of-6-round window that never reaches the strike, it mirrors The Pack Closes' more leveraged team-wide +10%, and its old +3% Heal rider moved to Killing Bite to give that route its identity. Beast Unchained +3% (route +8%) is the lever and moves with The Pack Closes.
- Concern: Killing Bite's +3 Damage on the kit's one 40 EP row is one above the roster's +2 default for Normal rows; the reason is one row, one strike per 6 rounds, and 43 under the 45 High tier. A director who prefers the default would set Killing Bite to +2 (40 → 42).
- Concern: The Pack Closes holds single-row team exposure at +10% (Life reaver 35 → 45% on one target, allies' hits included). One-row routes may reach +10%, but the director templates keep exposure near +5% as a secondary, so this tree moves with the roster-wide exposure question rather than alone.
- Concern: Scent of Blood is universal (Hunter's Moon roots a single chain), so Frenzy's fourth purchase is fixed.
- Concern: The 'Loup-Garou' classification extension and off-kit coverage remain director/engine decisions.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported rows, one per tag, on two casts (Damage, Increase Damage Given and Heal on Nature's Hunter; Increase Damage Taken on Life reaver); the Wolf Companion summon and Life reaver's absorb are unsupported. Three identities exist, one per phase of the hunt: the kill that feeds (Damage with the same cast's Heal), the mark (Increase Damage Taken) and the frenzy (Increase Damage Given). A fourth capstone would twin one of them on the same row or stand on Heal alone (10 HP per tick per point); that filler is declined. Scent of Blood is a universal node (in all 8 legal 4-BP builds) because Hunter's Moon roots a single 3-node chain, so every build carries +2% exposure and Frenzy's fourth purchase is fixed.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Loup-Garou-classified jutsu (requires classification extension). Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Scent of Blood | Foundation | None | +2% Increase Damage Taken (enemy debuff) | Life reaver / 1 |
| 02 | Rending Claws | Hidden Art | Scent of Blood | +3% Heal (self buff) | Nature's Hunter / 1 |
| 03 | Killing Bite | Advanced Art | Rending Claws | +3 Damage (damage); +3% Heal (self buff) | Nature's Hunter / 2 |
| 04 | Run to Ground | Hidden Art | Scent of Blood | +3% Increase Damage Taken (enemy debuff) | Life reaver / 1 |
| 05 | The Pack Closes | Advanced Art | Run to Ground | +5% Increase Damage Taken (enemy debuff) | Life reaver / 1 |
| 06 | Hunter's Moon | Foundation | None | +2% Increase Damage Given (self buff); +2% Heal (self buff) | Nature's Hunter / 2 |
| 07 | Feral Frenzy | Hidden Art | Hunter's Moon | +3% Increase Damage Given (self buff) | Nature's Hunter / 1 |
| 08 | Beast Unchained | Advanced Art | Feral Frenzy | +5% Increase Damage Given (self buff) | Nature's Hunter / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Scent of Blood** — One drop on the wind and the quarry is already chosen. Life reaver exposure 35 → 37% on one target for the 2 rounds after the cast. 1 row.
- **Rending Claws** — Flesh parts where the claws pass, and every wound torn in the quarry closes one on the wolf. Commitment to the kill: Nature's Hunter Heal 25 → 28 (280 HP per tick for the 2 rounds after the cast); Killing Bite pays it off. 1 row.
- **Killing Bite** — The jaws close on the throat; the chase ends and the feeding begins. Burst that feeds: Nature's Hunter 40 → 43 EP (still Normal, two under the 45 High tier) and Heal 25 → 31 on the full route (310 HP per tick for the 2 rounds after; 330 with Hunter's Moon). 2 rows, one cast.
- **Run to Ground** — Tired prey stumbles. The wolf does not. Life reaver exposure 37 → 40% with Scent of Blood. 1 row.
- **The Pack Closes** — Every howl answered; every flank taken. Nothing leaves the circle. Exposure: Life reaver 35 → 45% on the full route, raising every element-less or Taijutsu non-pierce hit on that target for 2 rounds, allies' hits and Nature's Hunter's strike included. 1 row.
- **Hunter's Moon** — Under the autumn moon the blood runs hot and the wounds knit shut. Nature's Hunter self buff 35 → 37% and Heal 25 → 27 (270 HP per tick), both for the 2 rounds after the cast. 2 rows.
- **Feral Frenzy** — Reason leaves with the first taste of blood; only hunger steers the claws. Nature's Hunter self buff 37 → 40% with Hunter's Moon. 1 row.
- **Beast Unchained** — The curse is no longer worn. It is answered, and it answers back. Sustained amplification: Nature's Hunter self buff 35 → 45% on the full route, raising every element-less or Taijutsu non-pierce hit the caster lands on any target in the 2 rounds after (never the strike itself). 1 row.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | IDT | HEAL |
|---|---|---:|---:|---:|---:|
| Killing Bite (Burst) | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | +3 | +2% | +2% | +8% |
| The Pack Closes (Exposure) | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | — | +2% | +10% | +2% |
| Beast Unchained (Frenzy) | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | — | +10% | +2% | +2% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · IDT = Increase Damage Taken · HEAL = Heal. Values are per-matching-row static additions, not final combat percentages.

- **Killing Bite:** Life reaver first, Nature's Hunter in one of the 2 rounds after: the strike lands at 43 EP into 37% exposure (43 × 1.37 against 40 × 1.35 at base, about +9% on the hit before the 15% passive), then heals 330 HP per tick (Rending Claws and Killing Bite +3% each, Hunter's Moon +2%; 660 HP per cast against 500 at base, 726 with the 10% Increase Heal passive) with the self buff at 37%. Hunter's Moon is the fourth purchase that completes the Nature's Hunter cast; Run to Ground (strike 43 × 1.40 ≈ 60.2 against The Pack Closes' 40 × 1.45 = 58, 310 HP ticks) is the all-offence alternative.
- **The Pack Closes:** Life reaver's exposure at 45% on one target for the 2 rounds after the cast, multiplying every qualifying hit on it from the caster, the strike and allies. With Hunter's Moon as the fourth purchase, both casts in one round (100 AP) give the next 2 rounds ×1.45 × 1.37 ≈ ×1.99 on the caster's hits on that target (×1.82 at base) and 270 HP heal ticks. Rending Claws (280 HP ticks, no offence) is the defensive alternative fourth.
- **Beast Unchained:** Nature's Hunter's self buff at 45% for the 2 rounds after the cast: every element-less or Taijutsu non-pierce hit the caster lands, on any target, is multiplied by 1.45 (1.35 at base), never the strike itself. Scent of Blood is the only legal fourth purchase (Life reaver exposure 37% on its one marked target), so this mirrors the Exposure build: ×1.45 on the caster's hits on every target, and ×1.45 × 1.37 ≈ ×1.99 only on the marked target while both windows are up, with 270 HP heal ticks. The Exposure build's ×1.99 is also one target only, but its 45% mark reaches allies' hits and the strike.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Frenzy |
|---|---:|---|---|---:|---:|---:|---:|
| Nature's Hunter | 0 | Damage | enemy | 40 | 43 (+3) | 40 | 40 |
| Nature's Hunter | 1 | Increase Damage Given | self | 35% | 37% (+2) | 37% (+2) | 45% (+10) |
| Nature's Hunter | 2 | Heal | self | 25 | 33 (+8) | 27 (+2) | 27 (+2) |
| Summon Wolf Companion | 0 | summon (unsupported) **adverse** | enemy | 75% | 75% | 75% | 75% |
| Life reaver | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 45% (+10) | 37% (+2) |
| Life reaver | 1 | absorb (unsupported) | self | 30% | 30% | 30% | 30% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +3 Damage, +10% Increase Damage Given, +10% Increase Damage Taken, +8% Heal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Killing Bite: +3 Damage (0 + 0 + 3; off band)
  - Route The Pack Closes: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Beast Unchained: +10% Increase Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 4 (DMG 1, HEAL 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon (raw +15, row-weighted 15)
- Lowest row-weighted node: Scent of Blood (2)

Validator warnings:

- classification status: requires classification extension (director decision)
- universal node: 01 (Scent of Blood) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +3 Damage |
|---|---:|---|---|
| Nature's Hunter | 0 | 40 (Normal) | 43 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Killing Bite | +3 Damage, +2% IDT, +6% HEAL | Run to Ground | +3 Damage, +5% IDT, +6% HEAL | 14 |
| Killing Bite | +3 Damage, +2% IDT, +6% HEAL | Hunter's Moon *(highest diagnostic)* | +3 Damage, +2% IDG, +2% IDT, +8% HEAL | 15 |
| The Pack Closes | +10% IDT | Rending Claws | +10% IDT, +3% HEAL | 13 |
| The Pack Closes | +10% IDT | Hunter's Moon *(highest diagnostic)* | +2% IDG, +10% IDT, +2% HEAL | 14 |
| Beast Unchained | +10% IDG, +2% HEAL | Scent of Blood *(highest diagnostic)* | +10% IDG, +2% IDT, +2% HEAL | 14 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Scent of Blood, Rending Claws, Killing Bite, Run to Ground | +3 Damage, +5% IDT, +6% HEAL |
| 2 | Scent of Blood, Rending Claws, Killing Bite, Hunter's Moon | +3 Damage, +2% IDG, +2% IDT, +8% HEAL |
| 3 | Scent of Blood, Rending Claws, Run to Ground, The Pack Closes | +10% IDT, +3% HEAL |
| 4 | Scent of Blood, Rending Claws, Run to Ground, Hunter's Moon | +2% IDG, +5% IDT, +5% HEAL |
| 5 | Scent of Blood, Rending Claws, Hunter's Moon, Feral Frenzy | +5% IDG, +2% IDT, +5% HEAL |
| 6 | Scent of Blood, Run to Ground, The Pack Closes, Hunter's Moon | +2% IDG, +10% IDT, +2% HEAL |
| 7 | Scent of Blood, Run to Ground, Hunter's Moon, Feral Frenzy | +5% IDG, +5% IDT, +2% HEAL |
| 8 | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained | +10% IDG, +2% IDT, +2% HEAL |

## Design notes

- Structure (unchanged graph): Scent of Blood (+2% Increase Damage Taken) forks into Rending Claws → Killing Bite (the kill that feeds) and Run to Ground → The Pack Closes (the mark); Hunter's Moon (+2% Increase Damage Given, +2% Heal) carries Feral Frenzy → Beast Unchained (the frenzy). Any two Advanced Arts cost 5 BP (shared root) or 6 BP.
- 2026-10-04 rebalance: Burst drops from +5 Damage (Nature's Hunter 40 → 45, Normal to High tier on the kit's only strike) to +3, all on Killing Bite (40 → 43). The Pack Closes drops its +3% Increase Damage Given: with Hunter's Moon it lifted the Exposure build's own buff to 40% (×1.45 × 1.40 ≈ ×2.03), the strongest build; it is now ×1.45 × 1.37 ≈ ×1.99. Beast Unchained is now +5% Increase Damage Given alone and its +3% Heal rider moved to Killing Bite, so Exposure and Frenzy are mirrors at 45% / 37%. Maxima over every legal allocation: Damage +3, Increase Damage Given +10%, Increase Damage Taken +10%, Heal +8%.
- Roster pass: Rending Claws' +1 Damage moved onto Killing Bite (flat Damage is the Advanced payoff, never a Hidden Art) and Rending Claws now commits to the feeding with +3% Heal. The percentage setups both fail on this branch: Increase Damage Taken would twin Run to Ground and stack with The Pack Closes as its fourth (+13%), and Increase Damage Given never reaches the strike, so it would not serve Killing Bite, and as The Pack Closes' fourth it would edge past Hunter's Moon (×1.45 × 1.38 ≈ ×2.00 against ×1.99). The Pack Closes' Rending Claws fourth is now sustain only, not a stronger strike.
- Damage magnitude: +3 on a 40 EP row is one above the roster's +2 default for Normal rows. Reason: Nature's Hunter is the kit's only Damage row, it strikes once per 6 rounds, and 43 stays two points under the 45 High tier. The kit has no 50 EP row, so no above-Nuke payoff arises.
- Arithmetic: each live window multiplies a hit by (1 + p/100) in turn and the 15% Taijutsu passive applies last; both rows are element-less, so their Taijutsu filter matches every element-less hit of any stat type plus Taijutsu elemental hits, never pierce. Static Heal is 10 HP per point per tick (2 ticks per cast); the 10% Increase Heal passive adds 10% outside ranked.
- Delivery: both casts are single target, range 4, cooldown 6, so each window covers 2 of 6 rounds. Life reaver then Nature's Hunter lands the strike in the exposure; both in one round (100 AP) overlaps the two windows for the next 2 rounds but leaves the strike unexposed.
- Fourth purchases: Burst (01, 02, 03) takes Hunter's Moon (buff 37%, Heal 330 HP per tick) or Run to Ground (exposure 40%, 310 HP). Exposure (01, 04, 05) takes Hunter's Moon (buff 37%, 270 HP) or Rending Claws (280 HP, no offence). Frenzy (06, 07, 08) can only add Scent of Blood. No fourth purchase lifts a capstone's own tag past +10%, and no route but Killing Bite can buy flat Damage. The Killing Bite + Hunter's Moon build tops the row-weighted diagnostic (15) only because its 8 Heal points count like percentage points; +8% Heal is 80 HP per tick.

## Risks and unproven interactions

- Classification: no kit row carries a non-None element, so the tree requires a classification extension: 'Loup-Garou' is the placeholder name of a new jutsu classification assigned to jutsu records, not a bloodline-id selector; which jutsu carry it is a director/engine decision. All three kit jutsu qualify only through it (ENGINE_GAP_REGISTER G1). Targeting None instead would reach every non-elemental row in the game. Off-kit coverage is unverified.
- Window breadth: Beast Unchained's 45% buff reaches basic attacks, weapons and element-less normal jutsu on every target; The Pack Closes' 45% exposure reaches every qualifying hit on one target from anyone, allies included. Other same-tag effects compound with them. Which mirror is stronger depends on team play and area hits; not simulated.
- Burst value: +3 EP is about +7.5% on one strike per 6 rounds and the route's +6% Heal is 120 HP per cast (132 with the passive; +8% and 160 HP with Hunter's Moon). On the same Life reaver → Nature's Hunter sequence with Hunter's Moon as each fourth, Killing Bite's strike is only about 1.6% harder (43 × 1.37 ≈ 58.9 against The Pack Closes' 40 × 1.45 = 58.0), while the 45% mark is ×1.45 / ×1.37 ≈ ×1.058 ahead on every other qualifying hit the caster lands on the target in the window, and allies' hits gain too. Killing Bite is lighter in throughput solo or in a team; its case is +120 HP per cast (330 against 270 HP per tick) plus a slightly harder strike.
- Targeting: both casts are OTHER_USER. Aimed at an ally, Nature's Hunter's Damage (friendly fire ALL) hits it while buff and Heal still land on the caster, and Life reaver exposes it.
- Rank gate: Nature's Hunter is requiredRank JONIN in the snapshot (Life reaver GENIN), so below Jonin only Scent of Blood, Run to Ground and The Pack Closes act; a realized-value restriction, not an item gate.
- Unsupported rows: the Wolf Companion summon (marked adverse in the dossier) and Life reaver's 30% absorb receive nothing. Skill-tree and bloodline effects are skipped in ranked PvP / sparring at the pin. No combat simulation was performed.

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

