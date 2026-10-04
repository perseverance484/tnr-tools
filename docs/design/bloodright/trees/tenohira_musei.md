# Tenohira Musei — The Voiceless Hand

**Bloodline:** Tenohira Musei (BR-078, rank A, `18Byy1tMXkQETmB88JLl5`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Yin-Yang classification / forked tree · **Classification:** Yin-Yang (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage multipliers: self Increase Damage Given (Silent Rift, Yin-Yang Cascade) and enemy Increase Damage Taken (Moonlit Inferno, Yin-Yang Cascade) · secondary Suppression (Decrease Damage Given on Moonlit Inferno) · tertiary A controlled +2 Damage burst on the three 40 EP Yin-Yang strikes.

Eight supported rows sit on four casts: three 40 EP Yin-Yang Damage rows, two 35% self Increase Damage Given rows (Silent Rift, Yin-Yang Cascade), two 35% enemy Increase Damage Taken rows (Moonlit Inferno, Cascade) and one 35% Decrease Damage Given row (Moonlit Inferno). Waxing Crescent answers "How do I make my own strikes count for more?": Tipping the Balance charges both self buffs, Deafening Silence opens the target and lands heavier strikes. Waning Crescent answers "How do I turn Moonlit Inferno on them?": Eclipse in Hand blunts their hits, Stillness Breaks bares them to every hit. The Defensive and Control rows (seal, buff and debuff prevention, move) are unsupported. Potency reaches matching supported tags on all Yin-Yang jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Waxing Crescent | Foundation | How do I make my own strikes count for more: charge my hand or open them for the blow? |
| Waning Crescent | Foundation | How do I turn Moonlit Inferno on them: blunt their strikes or bare them to every hit? |
| Deafening Silence | Advanced Art | burst: exposure set up, controlled raw-Damage payoff on the cast itself |
| Tipping the Balance | Advanced Art | sustained self amplification, solo and area |
| Eclipse in Hand | Advanced Art | suppression |
| Stillness Breaks | Advanced Art | exposure: one target bared to the whole party |

- Concern: Stillness Breaks is +4% (Exposure +9%) so Exposure + Waxing Crescent does not out-damage Amplifier + Quiet Opening on a single target on top of its party reach; +5% (45%) restores the round number if the director prefers it.
- Concern: Deafening Silence is a lean payoff (+2 EP on three cooldown-7 attacks); +3 (40 → 43) would still cross no tier if the director wants a sharper burst.
- Concern: Quiet Opening puts an enemy debuff under the self-side Foundation as the Burst setup, which also lets Amplifier take exposure 38% as its fourth.
- Concern: Only Suppression is defensive; the kit's Defensive and Control rows cannot be reached by potency.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yin-Yang jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Waxing Crescent | Foundation | None | +3% Increase Damage Given (self buff) | Silent Rift, Yin-Yang Cascade / 2 |
| 02 | Quiet Opening | Hidden Art | Waxing Crescent | +3% Increase Damage Taken (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 2 |
| 03 | Deafening Silence | Advanced Art | Quiet Opening | +2 Damage (damage) | Silent Palm Strike, Silent Rift, Yin-Yang Cascade / 3 |
| 04 | Held Breath | Hidden Art | Waxing Crescent | +2% Increase Damage Given (self buff) | Silent Rift, Yin-Yang Cascade / 2 |
| 05 | Tipping the Balance | Advanced Art | Held Breath | +5% Increase Damage Given (self buff); +2% Decrease Damage Given (enemy debuff) | Moonlit Inferno, Silent Rift, Yin-Yang Cascade / 3 |
| 06 | Waning Crescent | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 3 |
| 07 | Hushed Inferno | Hidden Art | Waning Crescent | +3% Decrease Damage Given (enemy debuff) | Moonlit Inferno / 1 |
| 08 | Eclipse in Hand | Advanced Art | Hushed Inferno | +5% Decrease Damage Given (enemy debuff); +2% Increase Damage Given (self buff) | Moonlit Inferno, Silent Rift, Yin-Yang Cascade / 3 |
| 09 | Bared to the Moon | Hidden Art | Waning Crescent | +3% Increase Damage Taken (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 2 |
| 10 | Stillness Breaks | Advanced Art | Bared to the Moon | +4% Increase Damage Taken (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Waxing Crescent** — The hand opens as the moon fills; what it gathers, it does not yet spend. Both self damage buffs 35 → 38% for 2 rounds: Silent Rift (Highest or element-less hits) and Yin-Yang Cascade (Fire/Lightning/Yin-Yang or element-less hits).
- **Quiet Opening** — The palm says nothing. It only finds where the guard is thin. Burst setup: Moonlit Inferno (all four stat types) and Yin-Yang Cascade (Highest or element-less hits) Increase Damage Taken 35 → 38%, 40% with Waning Crescent.
- **Deafening Silence** — The quietest strike leaves the loudest ruin. Burst payoff: Silent Rift (per enemy in its circle), Yin-Yang Cascade and Silent Palm Strike Yin-Yang Damage 40 → 42 EP, below the 45 High tier; it lands on the cast itself, with no window to wait for.
- **Held Breath** — Between one breath and the next, the rift widens. Both self damage buffs 40% with Waxing Crescent; 2 rounds per 60 AP cast, and both can be live on the caster at once.
- **Tipping the Balance** — Yin drains from the enemy; yang pools in the open hand. Amplifier route total +10%: both self damage buffs 35 → 45%; plus Moonlit Inferno suppression 35 → 37% (39% with Waning Crescent).
- **Waning Crescent** — Under the thinning moon the enemy's fire gutters and their guard slips. Moonlit Inferno exposure and suppression 35 → 37% (all four stat types, 40 AP); Yin-Yang Cascade exposure 35 → 37% (Highest or element-less hits).
- **Hushed Inferno** — A blaze can be silenced like any other voice. Moonlit Inferno Decrease Damage Given only: 40% with Waning Crescent; one row, 2 rounds per 40 AP cast, cooldown 7.
- **Eclipse in Hand** — Close the fingers and the enemy's light goes out; keep what spills. Suppression route total +10%: Moonlit Inferno Decrease Damage Given 35 → 45%; both self damage buffs 35 → 37% (40% with Waxing Crescent).
- **Bared to the Moon** — Stillness strips the guard away and leaves them bare under the moon. Both enemy exposure rows 40% with Waning Crescent: Moonlit Inferno (all four stat types) and Yin-Yang Cascade (Highest or element-less); both can sit on one target.
- **Stillness Breaks** — Their stillness breaks, and every hand that follows finds them open. Exposure route total +9%: Moonlit Inferno and Yin-Yang Cascade Increase Damage Taken 35 → 44% on one target, ×1.44 × 1.44 ≈ ×2.07 on every matching hit from the caster and allies.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT |
|---|---|---:|---:|---:|---:|
| Deafening Silence (Burst) | Waxing Crescent, Quiet Opening, Deafening Silence, Waning Crescent | +2 | +3% | +2% | +5% |
| Tipping the Balance (Amplifier) | Waxing Crescent, Held Breath, Tipping the Balance, Quiet Opening | — | +10% | +2% | +3% |
| Eclipse in Hand (Suppression) | Waning Crescent, Hushed Inferno, Eclipse in Hand, Waxing Crescent | — | +5% | +10% | +2% |
| Stillness Breaks (Exposure) | Waning Crescent, Bared to the Moon, Stillness Breaks, Waxing Crescent | — | +3% | +2% | +9% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Deafening Silence:** Silent Rift, Yin-Yang Cascade and Silent Palm Strike 40 → 42 EP from the cast itself, with both exposure rows at 40% and both self buffs at 38%. Open with Moonlit Inferno and Cascade in one turn (100 AP); Rift and Palm Strike in the next two rounds land ×1.40 × 1.40 = ×1.96 from exposure and ×1.38 more from Cascade's buff. Waning Crescent is the fourth purchase (it also puts Moonlit suppression at 37%); Held Breath (self buffs 40%) is the alternative.
- **Tipping the Balance:** Both self Increase Damage Given rows at 45% (+10%), each live the two rounds after its 60 AP cast; Rift and Cascade need two turns, so in the round both are live a hit lands ×1.45 × 1.45 ≈ ×2.10 from the caster's side alone, on any target and every enemy in Rift's circle; Moonlit suppression 37%. Quiet Opening is the fourth purchase (both exposure rows 38%); Waning Crescent (exposure 37%, suppression 39%) is the safer alternative.
- **Eclipse in Hand:** Moonlit Inferno's Decrease Damage Given at 45% for the two rounds after one 40 AP cast: the target's non-pierce hits on anyone land ×0.55 instead of ×0.65, with exposure 37% on the same cast. Waxing Crescent is the fourth purchase and lifts both self buffs to 40% with the capstone's rider; Bared to the Moon (exposure 40%) is the alternative.
- **Stillness Breaks:** Moonlit Inferno and Yin-Yang Cascade Increase Damage Taken at 44%; cast together in one turn (100 AP), they make every matching hit on the target in the next two rounds land ×1.44 × 1.44 ≈ ×2.07, from the caster and allies alike; Moonlit suppression 37%. Waxing Crescent is the fourth purchase (self buffs 38%); Hushed Inferno (suppression 40%) is the control alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Amplifier | Suppression | Exposure |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Moonlit Inferno | 0 | Decrease Damage Given | enemy | 35% | 37% (+2) | 37% (+2) | 45% (+10) | 37% (+2) |
| Moonlit Inferno | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 38% (+3) | 37% (+2) | 44% (+9) |
| Silent Rift | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Silent Rift | 1 | Increase Damage Given | self | 35% | 38% (+3) | 45% (+10) | 40% (+5) | 38% (+3) |
| Silent Rift | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Yin-Yang Cascade | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Yin-Yang Cascade | 1 | Increase Damage Taken | enemy | 35% | 40% (+5) | 38% (+3) | 37% (+2) | 44% (+9) |
| Yin-Yang Cascade | 2 | Increase Damage Given | self | 35% | 38% (+3) | 45% (+10) | 40% (+5) | 38% (+3) |
| Silent Palm Strike | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Silent Palm Strike | 1 | seal (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Eternal Stillness | 0 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Eternal Stillness | 1 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +10% Increase Damage Given, +10% Decrease Damage Given, +9% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Deafening Silence: +2 Damage (0 + 0 + 2; off band)
  - Route Tipping the Balance: +10% Increase Damage Given (3 + 2 + 5; on band)
  - Route Eclipse in Hand: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Stillness Breaks: +9% Increase Damage Taken (2 + 3 + 4; off band)
- Supported rows in kit: 8 (DMG 3, DDG 1, IDG 2, IDT 2)
- Strongest full build by row-weighted total: Waxing Crescent, Held Breath, Tipping the Balance, Waning Crescent (raw +16, row-weighted 28)
- Lowest row-weighted node: Hushed Inferno (3)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Silent Rift | 0 | 40 (Normal) | 42 (Normal) |
| Yin-Yang Cascade | 0 | 40 (Normal) | 42 (Normal) |
| Silent Palm Strike | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Deafening Silence | +2 Damage, +3% IDG, +3% IDT | Held Breath | +2 Damage, +5% IDG, +3% IDT | 22 |
| Deafening Silence | +2 Damage, +3% IDG, +3% IDT | Waning Crescent *(highest diagnostic)* | +2 Damage, +3% IDG, +2% DDG, +5% IDT | 24 |
| Tipping the Balance | +10% IDG, +2% DDG | Quiet Opening | +10% IDG, +2% DDG, +3% IDT | 28 |
| Tipping the Balance | +10% IDG, +2% DDG | Waning Crescent *(highest diagnostic)* | +10% IDG, +4% DDG, +2% IDT | 28 |
| Eclipse in Hand | +2% IDG, +10% DDG, +2% IDT | Waxing Crescent | +5% IDG, +10% DDG, +2% IDT | 24 |
| Eclipse in Hand | +2% IDG, +10% DDG, +2% IDT | Bared to the Moon *(highest diagnostic)* | +2% IDG, +10% DDG, +5% IDT | 24 |
| Stillness Breaks | +2% DDG, +9% IDT | Waxing Crescent *(highest diagnostic)* | +3% IDG, +2% DDG, +9% IDT | 26 |
| Stillness Breaks | +2% DDG, +9% IDT | Hushed Inferno | +5% DDG, +9% IDT | 23 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Waxing Crescent, Quiet Opening, Deafening Silence, Held Breath | +2 Damage, +5% IDG, +3% IDT |
| 2 | Waxing Crescent, Quiet Opening, Deafening Silence, Waning Crescent | +2 Damage, +3% IDG, +2% DDG, +5% IDT |
| 3 | Waxing Crescent, Quiet Opening, Held Breath, Tipping the Balance | +10% IDG, +2% DDG, +3% IDT |
| 4 | Waxing Crescent, Quiet Opening, Held Breath, Waning Crescent | +5% IDG, +2% DDG, +5% IDT |
| 5 | Waxing Crescent, Quiet Opening, Waning Crescent, Hushed Inferno | +3% IDG, +5% DDG, +5% IDT |
| 6 | Waxing Crescent, Quiet Opening, Waning Crescent, Bared to the Moon | +3% IDG, +2% DDG, +8% IDT |
| 7 | Waxing Crescent, Held Breath, Tipping the Balance, Waning Crescent | +10% IDG, +4% DDG, +2% IDT |
| 8 | Waxing Crescent, Held Breath, Waning Crescent, Hushed Inferno | +5% IDG, +5% DDG, +2% IDT |
| 9 | Waxing Crescent, Held Breath, Waning Crescent, Bared to the Moon | +5% IDG, +2% DDG, +5% IDT |
| 10 | Waxing Crescent, Waning Crescent, Hushed Inferno, Eclipse in Hand | +5% IDG, +10% DDG, +2% IDT |
| 11 | Waxing Crescent, Waning Crescent, Hushed Inferno, Bared to the Moon | +3% IDG, +5% DDG, +5% IDT |
| 12 | Waxing Crescent, Waning Crescent, Bared to the Moon, Stillness Breaks | +3% IDG, +2% DDG, +9% IDT |
| 13 | Waning Crescent, Hushed Inferno, Eclipse in Hand, Bared to the Moon | +2% IDG, +10% DDG, +5% IDT |
| 14 | Waning Crescent, Hushed Inferno, Bared to the Moon, Stillness Breaks | +5% DDG, +9% IDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). Kept: graph, Foundations, Amplifier, Suppression, the Exposure Hidden Art and every name except 02. Changed: Unspoken Blow (+2 Damage) becomes Quiet Opening (+3% Increase Damage Taken); Deafening Silence +3 → +2 Damage; Stillness Breaks +5% Increase Damage Taken and +2 Damage → +4% Increase Damage Taken. The old +5 Damage route lifted Silent Rift, Yin-Yang Cascade and Silent Palm Strike 40 → 45, a full tier on all three, and Damage on the Exposure capstone let the highest-leverage route also buy raw Damage.
- Burst follows the director's exposure-into-Damage pattern: the Hidden Art opens the target and the Advanced Art pays a controlled +2 EP that works on the cast itself, where the other offense routes need a window. Exposure stops at +9% rather than Amplifier's +10%: its rows also multiply allies' hits, and Moonlit Inferno plus Cascade (100 AP) put both live for two rounds from one turn, while Rift and Cascade need two turns and overlap for one round. Maxima over every legal allocation: Damage +2 (40 → 42, no tier crossing), Increase Damage Given +10%, Decrease Damage Given +10%, Increase Damage Taken +9%.
- Resolver and delivery (§3, §3b, §4b): every percentage row is element-less or lists None, so stat filters are not binding; Moonlit Inferno's two debuffs list all four stat types and match every non-pierce hit. All five casts have cooldown 7; attacks cost 60 AP and Moonlit Inferno 40 AP. Each row is live the two rounds after its cast, never on its own hit; Rift's self buff is realized on the caster at cast (actions.ts 980–1004). IDG and IDT rows compound: four 35% rows on one hit are ×1.35⁴ ≈ ×3.32 before potency.
- Fourth purchases: Burst → Waning Crescent (exposure 40%) or Held Breath (self buffs 40%); Amplifier → Quiet Opening (exposure 38%) or Waning Crescent; Suppression → Waxing Crescent (self buffs 40%) or Bared to the Moon (exposure 40%); Exposure → Waxing Crescent (self buffs 38%) or Hushed Inferno (suppression 40%). Only Deafening Silence carries Damage. Amplifier + Quiet Opening (+10%/+3%) and Exposure + Waxing Crescent (+9%/+3%) mirror each other, and Burst + Waning Crescent trades multiplier points for +2 EP on the strikes, so no fourth makes one route automatic.

## Risks and unproven interactions

- Classification: Yin-Yang is shared with other bloodlines (expected under RUL-2026-10-03-005). 4 of 8 supported rows carry Yin-Yang; Moonlit Inferno has no Yin-Yang row, so in-kit it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1), and it carries all of Suppression and half of Exposure. Off-kit Yin-Yang coverage is unverified; Deafening Silence's +2 reaches any such Yin-Yang Damage row.
- Exposure downstream: at 44% Moonlit Inferno's debuff multiplies every non-pierce hit on the target from the caster, allies and weapons, and Cascade's (Highest, element-less) adds a second ×1.44 for matching hits, so its value grows with party size. It is single-target, two rounds per cooldown 7.
- Self-buff reach: Rift's buff (Highest, no element) and Cascade's (Fire/Lightning/Yin-Yang/None) raise every matching hit the caster lands, on any target and every enemy in Rift's circle, basic attacks included. The 25% + 0.15/level Increase Damage Given passive multiplies last.
- Suppression rests on one Decrease Damage Given row (Moonlit Inferno, single target, two rounds per cooldown 7) and does not reduce pierce. It is the tree's only defensive route.
- Off-trait: seal (Silent Palm Strike), buff and debuff prevention (Eternal Stillness) and move (Silent Rift) are unsupported, so no route strengthens the bloodline's Defensive and Control traits and Eternal Stillness is untouched. Skill-tree and bloodline effects are skipped in ranked modes. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Yin-Yang jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

