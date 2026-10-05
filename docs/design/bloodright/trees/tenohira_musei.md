# Tenohira Musei — The Voiceless Hand

**Bloodline:** Tenohira Musei (BR-078, rank A, `18Byy1tMXkQETmB88JLl5`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Yin-Yang classification / forked tree · **Classification:** Yin-Yang (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Damage multipliers: self Increase Damage Given (Silent Rift, Yin-Yang Cascade) and enemy Increase Damage Taken (Moonlit Inferno, Yin-Yang Cascade) · secondary Suppression (Decrease Damage Given on Moonlit Inferno) · tertiary A burst: Unspoken Blow sets up +2% exposure on Moonlit Inferno and Yin-Yang Cascade, Deafening Silence pays it off with +2 Damage on the three 40 EP Yin-Yang strikes, 40 → 42, every cast.

Eight supported rows sit on four casts: three 40 EP Yin-Yang Damage rows, two 35% self Increase Damage Given rows (Silent Rift, Yin-Yang Cascade), two 35% enemy Increase Damage Taken rows (Moonlit Inferno, Cascade) and one 35% Decrease Damage Given row (Moonlit Inferno). Waxing Crescent answers "How do I make my own strikes count for more?": Deafening Silence's route opens the target, then hits harder on every cast, Tipping the Balance charges both self buffs for their windows. Waning Crescent answers "How do I weaken them?": Eclipse in Hand blunts their hits, Stillness Breaks bares them to every hit. The Defensive and Control rows (seal, buff and debuff prevention, move) are unsupported. Potency reaches matching supported tags on all Yin-Yang jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Waxing Crescent | Foundation | How do I make my own strikes count for more: open the target for a heavier blow, or charge my hand for the window? |
| Waning Crescent | Foundation | How do I weaken them: blunt their strikes or bare them to every hit? |
| Deafening Silence | Advanced Art | burst: Unspoken Blow's +2% exposure set up on Moonlit Inferno and Cascade, controlled +2 Damage payoff on all three Yin-Yang strikes (40 → 42, no tier crossed) |
| Tipping the Balance | Advanced Art | sustained amplification: both self buffs lift every own hit in their windows; +2% suppression rider as the yin-yang balance |
| Eclipse in Hand | Advanced Art | suppression: the target hits softer on everyone; single-tag capstone |
| Stillness Breaks | Advanced Art | exposure: every matching hit on the marked target lands harder, allies' included (×1.122 for the caster with both rows live; Moonlit Inferno's ×1.059 on allies' non-pierce hits) |

**Director review recommended:** Roster questions: DQ-B (Stillness Breaks +8% Increase Damage Taken on 2 rows: Moonlit Inferno 35 → 43%; Yin-Yang Cascade 35 → 43%; ≈ ×1.122, against Shakunetsu Sakura ×1.075 and Blood-Enchanted Eyes ×1.115); trim option 2/2/3 (≈ ×1.106), which would put the capstone-free 01+02+06+09 (+6%) within 1 point again, so Unspoken Blow's setup would drop to +1% (R9′ setup size).

- Concern: In the solo rotation Burst + Waning Crescent (305.5) and Exposure + Waxing Crescent (305.6) lead Amplifier + Waning Crescent (300.9) by about 1.5%; the Amplifier's lead is reach: its 43% buffs lift every own hit on any target while live (×1.044 over the other builds' 37%).
- Concern: Unspoken Blow and Bared to the Moon carry the same +2% exposure on the same two rows in different branches; they meet only in the capstone-free 01+02+06+09 (+6%), and outside the burst route Unspoken Blow is outbid or only ties (01+02+04+05 loses to Waning Crescent and 01+02+06+09 to Stillness Breaks; elsewhere it ties Bared to the Moon), so the setup is bought for its payoff.
- Concern: Only Suppression is defensive, now single-tag; the kit's Defensive and Control rows cannot be reached by potency.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yin-Yang jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Waxing Crescent | Foundation | None | +2% Increase Damage Given (self buff) | Silent Rift, Yin-Yang Cascade / 2 |
| 02 | Unspoken Blow | Hidden Art | Waxing Crescent | +2% Increase Damage Taken (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 2 |
| 03 | Deafening Silence | Advanced Art | Unspoken Blow | +2 Damage (damage) | Silent Palm Strike, Silent Rift, Yin-Yang Cascade / 3 |
| 04 | Held Breath | Hidden Art | Waxing Crescent | +2% Increase Damage Given (self buff) | Silent Rift, Yin-Yang Cascade / 2 |
| 05 | Tipping the Balance | Advanced Art | Held Breath | +4% Increase Damage Given (self buff); +2% Decrease Damage Given (enemy debuff) | Moonlit Inferno, Silent Rift, Yin-Yang Cascade / 3 |
| 06 | Waning Crescent | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 3 |
| 07 | Hushed Inferno | Hidden Art | Waning Crescent | +3% Decrease Damage Given (enemy debuff) | Moonlit Inferno / 1 |
| 08 | Eclipse in Hand | Advanced Art | Hushed Inferno | +5% Decrease Damage Given (enemy debuff) | Moonlit Inferno / 1 |
| 09 | Bared to the Moon | Hidden Art | Waning Crescent | +2% Increase Damage Taken (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 2 |
| 10 | Stillness Breaks | Advanced Art | Bared to the Moon | +4% Increase Damage Taken (enemy debuff) | Moonlit Inferno, Yin-Yang Cascade / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Waxing Crescent** — The hand opens as the moon fills; what it gathers, it does not yet spend. Both self damage buffs 35 → 37% for 2 rounds: Silent Rift (Highest or element-less hits) and Yin-Yang Cascade (Fire/Lightning/Yin-Yang or element-less hits).
- **Unspoken Blow** — No cry, no warning. The palm has already landed, and the guard behind it is gone. Burst setup for Deafening Silence: Moonlit Inferno and Yin-Yang Cascade exposure 35 → 37% (39% with Waning Crescent) on one target for the two rounds after each cast, so the strikes that follow land into it.
- **Deafening Silence** — The quietest strike leaves the loudest ruin. Burst payoff: Silent Rift (per enemy in its circle), Yin-Yang Cascade and Silent Palm Strike 40 → 42 EP on every cast, no tier crossed; a strike with both of Unspoken Blow's 37% exposure rows live lands ×1.05 × (1.37/1.35)² ≈ ×1.081 over the base kit.
- **Held Breath** — Between one breath and the next, the rift widens. Both self damage buffs 39% with Waxing Crescent; 2 rounds per 60 AP cast. Rift and Cascade cost 120 AP together, so they need two turns and are live together for one round.
- **Tipping the Balance** — Yin drains from the enemy; yang pools in the open hand. Amplifier route total +8%: both self damage buffs 35 → 43%; rider: Moonlit Inferno suppression 35 → 37% (39% with Waning Crescent).
- **Waning Crescent** — Under the thinning moon the enemy's fire gutters and their guard slips. Moonlit Inferno exposure and suppression 35 → 37% (all four stat types, 40 AP); Yin-Yang Cascade exposure 35 → 37% (Highest or element-less hits).
- **Hushed Inferno** — A blaze can be silenced like any other voice. Moonlit Inferno Decrease Damage Given only: 40% with Waning Crescent; one row, 2 rounds per 40 AP cast, cooldown 7.
- **Eclipse in Hand** — Close the fingers and the enemy's light goes out. Suppression route total +10%: Moonlit Inferno Decrease Damage Given 35 → 45% on one target for 2 rounds per 40 AP cast (its hits ×0.55/0.65 ≈ ×0.846); single-tag capstone.
- **Bared to the Moon** — Stillness strips the guard away and leaves them bare under the moon. Both enemy exposure rows 39% with Waning Crescent: Moonlit Inferno (all four stat types) and Yin-Yang Cascade (Highest or element-less); both can sit on one target.
- **Stillness Breaks** — Their stillness breaks, and every hand that follows finds them open. Exposure route total +8%: Moonlit Inferno and Yin-Yang Cascade Increase Damage Taken 35 → 43% on one target; with both live the caster's hits land ×(1.43/1.35)² ≈ ×1.122 against the unmodified kit (anchors: Shakunetsu ×1.075, Blood-Enchanted Eyes ×1.115). An ally's non-pierce hit gets Moonlit's ×1.059, and Cascade's only if it is element-less or uses the caster's highest offence stat.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT |
|---|---|---:|---:|---:|---:|
| Deafening Silence (Burst) | Waxing Crescent, Unspoken Blow, Deafening Silence, Waning Crescent | +2 | +2% | +2% | +4% |
| Tipping the Balance (Amplifier) | Waxing Crescent, Held Breath, Tipping the Balance, Waning Crescent | — | +8% | +4% | +2% |
| Eclipse in Hand (Suppression) | Waning Crescent, Hushed Inferno, Eclipse in Hand, Waxing Crescent | — | +2% | +10% | +2% |
| Stillness Breaks (Exposure) | Waning Crescent, Bared to the Moon, Stillness Breaks, Waxing Crescent | — | +2% | +2% | +8% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Deafening Silence:** Silent Rift, Yin-Yang Cascade and Silent Palm Strike 40 → 42 EP on every cast, the opener included, with both exposure rows at 39% and both self buffs at 37%. Open with Moonlit Inferno and Cascade in one turn (100 AP); Rift and Palm Strike in the next two rounds land ×1.39 × 1.39 ≈ ×1.93 from exposure and ×1.37 more from Cascade's buff (Palm Strike also gets Rift's), and every extra enemy in Rift's circle takes the +2. Waning Crescent is the fourth purchase (exposure 39%, Moonlit suppression 37%); Held Breath (self buffs 39%) is the solo alternative.
- **Tipping the Balance:** Both self Increase Damage Given rows at 43% (+8%), each live the two rounds after its 60 AP cast. Rift and Cascade cost 120 AP together, so their windows overlap one round; in that round a hit lands ×1.43 × 1.43 ≈ ×2.04 from the caster's side alone, on any target. Rift's own buff never touches Rift's hit, so its circle gets ×1.43 from Cascade's buff when Cascade opens. Waning Crescent is the fourth purchase (exposure 37%, Moonlit suppression 39%); Unspoken Blow gives the same 37% exposure without Waning Crescent's extra +2% suppression (37% instead of 39%).
- **Eclipse in Hand:** Moonlit Inferno's Decrease Damage Given at 45% for the two rounds after one 40 AP cast: the target's non-pierce hits on anyone land ×0.55 instead of ×0.65, with exposure 37% on the same cast. Waxing Crescent is the fourth purchase (self buffs 37%); Bared to the Moon (exposure 39%) is the alternative.
- **Stillness Breaks:** Moonlit Inferno and Yin-Yang Cascade Increase Damage Taken at 43%; cast together in one turn (100 AP), they make the caster's hits on the target in the next two rounds land ×1.43 × 1.43 ≈ ×2.04, ×1.122 over the unmodified kit's ×1.82. Every non-pierce ally hit on the target gets Moonlit's 43%; Cascade's applies only to an ally's element-less hits or hits of the caster's highest offence stat. Moonlit suppression 37%. Waxing Crescent is the fourth purchase (self buffs 37%); Hushed Inferno (suppression 40%) is the control alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Amplifier | Suppression | Exposure |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Moonlit Inferno | 0 | Decrease Damage Given | enemy | 35% | 37% (+2) | 39% (+4) | 45% (+10) | 37% (+2) |
| Moonlit Inferno | 1 | Increase Damage Taken | enemy | 35% | 39% (+4) | 37% (+2) | 37% (+2) | 43% (+8) |
| Silent Rift | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Silent Rift | 1 | Increase Damage Given | self | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 37% (+2) |
| Silent Rift | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Yin-Yang Cascade | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Yin-Yang Cascade | 1 | Increase Damage Taken | enemy | 35% | 39% (+4) | 37% (+2) | 37% (+2) | 43% (+8) |
| Yin-Yang Cascade | 2 | Increase Damage Given | self | 35% | 37% (+2) | 43% (+8) | 37% (+2) | 37% (+2) |
| Silent Palm Strike | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Silent Palm Strike | 1 | seal (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Eternal Stillness | 0 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Eternal Stillness | 1 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +8% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Deafening Silence: +2 Damage (0 + 0 + 2; off band)
  - Route Tipping the Balance: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Eclipse in Hand: +10% Decrease Damage Given (2 + 3 + 5; on band)
  - Route Stillness Breaks: +8% Increase Damage Taken (2 + 2 + 4; off band)
- Supported rows in kit: 8 (DMG 3, DDG 1, IDG 2, IDT 2)
- Strongest full build by row-weighted total: Waxing Crescent, Held Breath, Tipping the Balance, Waning Crescent (raw +14, row-weighted 24)
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
| Deafening Silence | +2 Damage, +2% IDG, +2% IDT | Held Breath | +2 Damage, +4% IDG, +2% IDT | 18 |
| Deafening Silence | +2 Damage, +2% IDG, +2% IDT | Waning Crescent *(highest diagnostic)* | +2 Damage, +2% IDG, +2% DDG, +4% IDT | 20 |
| Tipping the Balance | +8% IDG, +2% DDG | Unspoken Blow | +8% IDG, +2% DDG, +2% IDT | 22 |
| Tipping the Balance | +8% IDG, +2% DDG | Waning Crescent *(highest diagnostic)* | +8% IDG, +4% DDG, +2% IDT | 24 |
| Eclipse in Hand | +10% DDG, +2% IDT | Waxing Crescent | +2% IDG, +10% DDG, +2% IDT | 18 |
| Eclipse in Hand | +10% DDG, +2% IDT | Bared to the Moon *(highest diagnostic)* | +10% DDG, +4% IDT | 18 |
| Stillness Breaks | +2% DDG, +8% IDT | Waxing Crescent *(highest diagnostic)* | +2% IDG, +2% DDG, +8% IDT | 22 |
| Stillness Breaks | +2% DDG, +8% IDT | Hushed Inferno | +5% DDG, +8% IDT | 21 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Waxing Crescent, Unspoken Blow, Deafening Silence, Held Breath | +2 Damage, +4% IDG, +2% IDT |
| 2 | Waxing Crescent, Unspoken Blow, Deafening Silence, Waning Crescent | +2 Damage, +2% IDG, +2% DDG, +4% IDT |
| 3 | Waxing Crescent, Unspoken Blow, Held Breath, Tipping the Balance | +8% IDG, +2% DDG, +2% IDT |
| 4 | Waxing Crescent, Unspoken Blow, Held Breath, Waning Crescent | +4% IDG, +2% DDG, +4% IDT |
| 5 | Waxing Crescent, Unspoken Blow, Waning Crescent, Hushed Inferno | +2% IDG, +5% DDG, +4% IDT |
| 6 | Waxing Crescent, Unspoken Blow, Waning Crescent, Bared to the Moon | +2% IDG, +2% DDG, +6% IDT |
| 7 | Waxing Crescent, Held Breath, Tipping the Balance, Waning Crescent | +8% IDG, +4% DDG, +2% IDT |
| 8 | Waxing Crescent, Held Breath, Waning Crescent, Hushed Inferno | +4% IDG, +5% DDG, +2% IDT |
| 9 | Waxing Crescent, Held Breath, Waning Crescent, Bared to the Moon | +4% IDG, +2% DDG, +4% IDT |
| 10 | Waxing Crescent, Waning Crescent, Hushed Inferno, Eclipse in Hand | +2% IDG, +10% DDG, +2% IDT |
| 11 | Waxing Crescent, Waning Crescent, Hushed Inferno, Bared to the Moon | +2% IDG, +5% DDG, +4% IDT |
| 12 | Waxing Crescent, Waning Crescent, Bared to the Moon, Stillness Breaks | +2% IDG, +2% DDG, +8% IDT |
| 13 | Waning Crescent, Hushed Inferno, Eclipse in Hand, Bared to the Moon | +10% DDG, +4% IDT |
| 14 | Waning Crescent, Hushed Inferno, Bared to the Moon, Stillness Breaks | +5% DDG, +8% IDT |

## Design notes

- 2026-10-04 rebalance (BALANCE_REVIEW_METHOD.md). First pass: the old +5 Damage route lifted Silent Rift, Yin-Yang Cascade and Silent Palm Strike 40 → 45, a full tier on all three, and Stillness Breaks lost its Damage. Roster pass: Quiet Opening (+3% Increase Damage Taken) returned to its pre-batch name and job as Unspoken Blow (+1 Damage) and Deafening Silence went +2 → +1 (route +2); Waxing Crescent +3 → +2% and Tipping the Balance +5 → +4% (Amplifier +10 → +8%); Bared to the Moon +3 → +2% and Stillness Breaks +4 → +3% (Exposure +9 → +7%). The final review raised Deafening Silence back to +2 (route +3); the final cleanup returns it to +1 (edge route +2, 40 → 42) under the batch's +2 flat-Damage limit, and Eclipse in Hand drops its +2% Increase Damage Given rider (no offensive rider on a suppression capstone). Consistency pass: Stillness Breaks +3 → +4% (Exposure +7 → +8%, R19), which clears the near-tie that had kept the edge commit, so Unspoken Blow became a +2% Increase Damage Taken setup and Deafening Silence +2 Damage (burst, 40 → 42). Graph and names unchanged.
- Burst setup (R9′, checked with near_tie.py): Unspoken Blow carries +2% Increase Damage Taken on Moonlit Inferno and Cascade. The capstone-free 01+02+06+09 reaches +6% against Stillness Breaks' +8%, two points clear (at +7% it was a near-tie); Bared to the Moon sits in the other branch and is never a legal fourth for the burst route, nor Unspoken Blow for Stillness Breaks, so they are not twins. Increase Damage Given would be a stacking twin of Held Breath (01+02+04+05 at +10%). Deafening Silence pays off with +2 Damage on all three strikes; the kit has no 50 EP row, so 40 → 42 crosses no tier.
- Magnitudes: the two self buffs and the two exposure debuffs each compound on one hit, so Amplifier and Exposure are both +8% on two rows (×(1.43/1.35)² ≈ ×1.122; anchors Shakunetsu ×1.075, Blood-Enchanted Eyes ×1.115). R19 lets exposure match the amplifier: Moonlit Inferno and Cascade (100 AP) put both exposure rows live for the same two rounds from one turn and also lift allies' hits, while Rift and Cascade (120 AP) need two turns and overlap one round but reach every own hit on any target. Suppression is one single-target row, so it keeps +10% (×0.846) with no rider. Tipping the Balance's +2% Decrease Damage Given is the yin-yang 'balance' (yang pools in the hand as yin drains from the target), a small defensive secondary on the Moonlit cast the route already wants. Maxima over every legal allocation: Damage +2 (40 → 42), Increase Damage Given +8%, Decrease Damage Given +10%, Increase Damage Taken +8%; the top offensive package is ×1.156 (01+04+05+06, 01+02+04+05 or 01+06+09+10), and the burst package 01+02+03+06 is ×1.146 with its +2 Damage (R14′, under ×1.234).
- Resolver and delivery (§3, §3b, §4b): stat filters on an element-less row bind only on elemental hits. Such a row matches every element-less hit of any stat type, and an elemental hit only when the row lists that hit's stat type; 'Highest' is the caster's highest offence, also on an enemy debuff. Moonlit Inferno's two debuffs list all four stat types, so they match every non-pierce hit. Cascade's exposure row (Highest) matches the caster's own strikes, but an ally's elemental hit only if it uses the Tenohira caster's highest offence stat. All five casts have cooldown 7; attacks cost 60 AP and Moonlit Inferno 40 AP. Each row is live the two rounds after its cast, never on its own hit; Rift's self buff is realized on the caster at cast (actions.ts 980–1004). IDG and IDT rows compound: four 35% rows on one hit are ×1.35⁴ ≈ ×3.32 before potency.
- Fourth purchases: Burst → Waning Crescent or Held Breath; Amplifier → Waning Crescent (Unspoken Blow adds the same exposure without Waning Crescent's extra +2% suppression (37% instead of 39%)); Suppression → Waxing Crescent or Bared to the Moon; Exposure → Waxing Crescent or Hushed Inferno. In the in-kit solo rotation (R1 Moonlit Inferno + Cascade at 100 AP, R2 Rift, R3 Palm Strike; compounding IDG/IDT on the strikes) the three offense packages total 305.5 (Burst + Waning Crescent; 303.9 with Held Breath), 300.9 (Amplifier + Waning Crescent) and 305.6 (Exposure + Waxing Crescent) strike power against a 271.3 baseline; the best capstone-less build (01+02+06+09) gives 298.2. No fourth makes one route automatic. The burst adds +2 EP to every Yin-Yang cast in or out of a window, the opener included, and Rift's circle (57.5 per extra enemy against 57.2 for Amplifier + Waning Crescent); the Amplifier's 43% buffs lift every other own hit while live (basic attacks, weapons, element-less hits, any target) ×1.43/1.37 ≈ ×1.044 over the burst and exposure builds; Exposure's edge is a party.

## Risks and unproven interactions

- Classification: Yin-Yang is shared with other bloodlines (expected under RUL-2026-10-03-005). 4 of 8 supported rows carry Yin-Yang; Moonlit Inferno has no Yin-Yang row, so in-kit it qualifies only through an authored jutsu classification (ENGINE_GAP_REGISTER G1), and it carries all of Suppression and half of Exposure. Off-kit Yin-Yang coverage is unverified; the burst route's +2 reaches any such Yin-Yang Damage row (an off-kit 50 EP one would read 52).
- Exposure downstream: at 43% (×1.059 over the kit's 35%) Moonlit Inferno's debuff multiplies every non-pierce hit on the target from the caster, allies and weapons, so its value grows with party size. Cascade's (Highest, element-less) adds a second factor for the caster's strikes and for allies' element-less hits or hits of the caster's highest offence stat only. It is single-target, two rounds per cooldown 7.
- Self-buff reach: Rift's buff (Highest, no element) and Cascade's (Fire/Lightning/Yin-Yang/None) raise every matching hit the caster lands while live, on any target, basic attacks included. Neither touches its own cast's hit, so Rift's circle gets only Cascade's buff, when Cascade was cast in an earlier round. The 25% + 0.15/level Increase Damage Given passive multiplies last.
- Suppression rests on one Decrease Damage Given row (Moonlit Inferno, single target, two rounds per cooldown 7) and does not reduce pierce. It is the tree's only defensive route.
- Off-trait: seal (Silent Palm Strike), buff and debuff prevention (Eternal Stillness) and move (Silent Rift) are unsupported, so no route strengthens the bloodline's Defensive and Control traits and Eternal Stillness is untouched. Skill-tree and bloodline effects are skipped in ranked modes. No combat simulation was performed beyond the in-kit rotation arithmetic in the design notes.

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

