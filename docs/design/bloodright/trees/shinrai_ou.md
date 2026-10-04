# Shinrai Ou — Throne of Thunder

**Bloodline:** Shinrai Ou (BR-065, rank A, `xO4Dycx7FFEqxwvAEXBxY`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Storm classification / forked tree · **Classification:** Storm (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Increase Damage Given (Burst: the Storm Cloak's two self buffs and Raijin's compound; +7% route) · secondary Increase Damage Taken (Izanagi's Hammer area exposure, +10% route) and Reflect (Indra's Storm Cloak retaliation, +10% route) · tertiary Damage has no node: every flat bonus would lift Daibutsu Thunder past the 50 Nuke tier.

Shinrai Ou is a rank-A Burst kit whose four Storm attacks are 50, 45, 40 and 40 EP (60 AP, cooldown 7). Flat Damage reaches all four, so any bonus pushes Daibutsu Thunder past 50 and the earlier +5 route also lifted Railgun to 50 and both 40s a tier; the Burst identity is carried by Increase Damage Given instead, whose three 35% rows (two on the 40 AP Storm Cloak, one on Raijin) compound on every hit in their windows. Mandate of Thunder answers "How do I make my thunder land harder: charge myself or expose them?": Thunder King's Wrath charges the self buffs (+7%), Judgement from Above widens Hammer's area exposure (+10%). Raiment of Storms answers "How do I make attackers pay for striking me?" with the Cloak's Reflect (+10%). Potency reaches matching supported tags on all Storm jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Mandate of Thunder | Foundation | How do I make my thunder land harder: charge myself or expose them? |
| Raiment of Storms | Foundation | How do I make attackers pay for striking me? |
| Thunder King's Wrath | Advanced Art | burst: the Cloak and Raijin self buffs compound on every hit in their windows |
| Judgement from Above | Advanced Art | exposure: Hammer marks the field and every matching hit on it lands harder, allies' included |
| Thunder Answers Thunder | Advanced Art | retaliation: the Storm Cloak returns half of every blow |

- Concern: Damage is a supported tag with no node; the kit's Burst trait is expressed through compounding Increase Damage Given. The Blood-Enchanted Eyes pattern (+2 Damage capstone) would put Daibutsu Thunder at 52.
- Concern: Thunder King's Wrath is held at +7% Increase Damage Given because three rows compound (×1.16 when the Cloak and Raijin windows overlap); it remains the strongest solo route.
- Concern: Mandate of Thunder is universal, so the Retaliation route's fourth purchase is forced; the kit has no second defensive tag for a leaf under Raiment of Storms.
- Concern: The Reflect row and two of the three Increase Damage Given rows are element-less and depend on the proposed jutsu-classification resolver.

> **Narrow-kit exception:** Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on nine rows (Damage x4, Increase Damage Given x3, Increase Damage Taken x1, Reflect x1), and Damage is deliberately left without a node because every flat bonus reaches Daibutsu Thunder at 50. That leaves three tags and three identities: self-amplification, exposure and retaliation; a fourth Advanced Art would twin one of them. Mandate of Thunder forks into the two offensive routes and Raiment of Storms carries the single Reflect chain, so Mandate of Thunder is a universal node (in all 8 legal full builds): Raiment's 3-BP chain needs a fourth purchase and Mandate is the only prerequisite-closed one. A Hidden Art leaf under Raiment would be a one- or two-point sliver of a tag another node already owns. Burst and Exposure each keep two fourth-purchase choices; Retaliation has one.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Storm jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Mandate of Thunder | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Indra's Storm Cloak, Izanagi's Hammer, Strike: Raijin / 4 |
| 02 | Vajra Tempering | Hidden Art | Mandate of Thunder | +2% Increase Damage Given (self buff) | Indra's Storm Cloak, Strike: Raijin / 3 |
| 03 | Thunder King's Wrath | Advanced Art | Vajra Tempering | +3% Increase Damage Given (self buff) | Indra's Storm Cloak, Strike: Raijin / 3 |
| 04 | Lightning Rod | Hidden Art | Mandate of Thunder | +3% Increase Damage Taken (enemy debuff) | Izanagi's Hammer / 1 |
| 05 | Judgement from Above | Advanced Art | Lightning Rod | +5% Increase Damage Taken (enemy debuff) | Izanagi's Hammer / 1 |
| 06 | Raiment of Storms | Foundation | None | +2% Reflect (self buff) | Indra's Storm Cloak / 1 |
| 07 | Galvanic Rebuke | Hidden Art | Raiment of Storms | +3% Reflect (self buff) | Indra's Storm Cloak / 1 |
| 08 | Thunder Answers Thunder | Advanced Art | Galvanic Rebuke | +5% Reflect (self buff) | Indra's Storm Cloak / 1 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08. Advanced Arts: 3; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Mandate of Thunder** — Heaven names its king in thunder; the storm answers before the title is spoken. Storm Cloak Increase Damage Given rows 0 and 2 and Raijin's 35 → 37% (self, 2 rounds); Hammer exposure 35 → 37% (area enemies, 2 rounds).
- **Vajra Tempering** — The king's own storm tempers the thunderbolt, again and again, until nothing it strikes stays standing. Storm Cloak Increase Damage Given rows 0 and 2 and Raijin's self buff 37 → 39% with Mandate of Thunder (self, 2 rounds); the two Cloak rows compound on every matching hit.
- **Thunder King's Wrath** — When the king's patience ends, the sky itself is the weapon. Burst: all three Increase Damage Given rows 35 → 42% on the full route (+7%); a hit inside both the Cloak and Raijin windows goes ×1.35³ ≈ ×2.46 → ×1.42³ ≈ ×2.86.
- **Lightning Rod** — Mark the foe as the tallest thing on the field and let the storm choose. Hammer exposure row only: +3% (40% with Mandate of Thunder) on Lightning/None/Storm/Water hits against enemies on its spiral tiles, 2 rounds after the cast.
- **Judgement from Above** — The exposed are not struck once; every bolt that follows finds them first. Exposure: Hammer 35 → 45% Increase Damage Taken on the full route (+10%), on every enemy on its spiral tiles for 2 rounds; allies' matching hits gain too.
- **Raiment of Storms** — A cloak of living lightning: it bites whoever touches it and sharpens every bolt. Storm Cloak Reflect 40 → 42% (self, 2 rounds, all four stat types).
- **Galvanic Rebuke** — Strike the storm and the storm strikes back, charge for charge. Storm Cloak Reflect row only: +3% (45% with Raiment of Storms; pierce included, 60% cap); 40 AP self cast, cooldown 7, 2 rounds.
- **Thunder Answers Thunder** — Every blow against the king is a confession, and the sky passes sentence. Retaliation: Storm Cloak Reflect 40 → 50% on the full route (+10%), ten points under the 60% per-hit cap.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | REF |
|---|---|---:|---:|---:|
| Thunder King's Wrath (Burst) | Mandate of Thunder, Vajra Tempering, Thunder King's Wrath, Lightning Rod | +7% | +5% | — |
| Judgement from Above (Exposure) | Mandate of Thunder, Lightning Rod, Judgement from Above, Vajra Tempering | +4% | +10% | — |
| Thunder Answers Thunder (Retaliation) | Mandate of Thunder, Raiment of Storms, Galvanic Rebuke, Thunder Answers Thunder | +2% | +2% | +10% |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Thunder King's Wrath:** All three Increase Damage Given rows reach 42% (+7%): the two Cloak rows alone take a matching hit from ×1.82 to ×2.02 (×1.11), and with Raijin's window overlapping from ×2.46 to ×2.86 (×1.16), before the bloodline passive. Lightning Rod is the strongest fourth (Hammer exposure 40%); Raiment of Storms (Reflect 42%) is the alternative. No Storm attack changes tier.
- **Judgement from Above:** Hammer's area Increase Damage Taken reaches 45% (+10%), live in the two rounds after Hammer's cast on every enemy on its spiral tiles and never on Hammer's own hit, so every matching Storm, Lightning, Water or element-less hit on them lands ×1.074 harder, allies' included. Vajra Tempering is the strongest fourth (self buffs 39%, ×1.06 from the Cloak); Raiment of Storms (Reflect 42%) suits a support player.
- **Thunder Answers Thunder:** Indra's Storm Cloak reflects 50% of every hit the caster takes in the two rounds after its cast (+10%), bypassing shields and ten points under the 60% per-hit cap. Mandate of Thunder is the only closed fourth purchase (the universal node; see the narrow-kit exception) and adds +2% to the self buffs and Hammer's exposure (37%).

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Retaliation |
|---|---:|---|---|---:|---:|---:|---:|
| Storm Style: Daibutsu Thunder | 0 | Damage | enemy | 50 | 50 | 50 | 50 |
| Storm Style: Daibutsu Thunder | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% |
| Izanagi's Hammer | 0 | Damage | enemy | 40 | 40 | 40 | 40 |
| Izanagi's Hammer | 1 | move (unsupported) | self | 1 | 1 | 1 | 1 |
| Izanagi's Hammer | 2 | Increase Damage Taken | enemy | 35% | 40% (+5) | 45% (+10) | 37% (+2) |
| Indra's Storm Cloak | 0 | Increase Damage Given | self | 35% | 42% (+7) | 39% (+4) | 37% (+2) |
| Indra's Storm Cloak | 1 | Reflect | self | 40% | 40% | 40% | 50% (+10) |
| Indra's Storm Cloak | 2 | Increase Damage Given | self | 35% | 42% (+7) | 39% (+4) | 37% (+2) |
| Storm Style: Divine Railgun | 0 | Damage | enemy | 45 | 45 | 45 | 45 |
| Storm Style: Divine Railgun | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 |
| Strike: Raijin | 0 | Damage | enemy | 40 | 40 | 40 | 40 |
| Strike: Raijin | 1 | Increase Damage Given | self | 35% | 42% (+7) | 39% (+4) | 37% (+2) |
| Strike: Raijin | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 4, 3: 7, 4: 8
- Full-budget allocations: 8; numerically non-dominated (per-tag totals): 8; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +7% Increase Damage Given, +10% Increase Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Thunder King's Wrath: +7% Increase Damage Given (2 + 2 + 3; off band)
  - Route Judgement from Above: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Thunder Answers Thunder: +10% Reflect (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 4, IDG 3, IDT 1, REF 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Mandate of Thunder, Vajra Tempering, Thunder King's Wrath, Lightning Rod (raw +12, row-weighted 26)
- Lowest row-weighted node: Raiment of Storms (2)

Validator warnings:

- universal node: 01 (Mandate of Thunder) appears in every legal full-budget allocation (acknowledged in narrow_kit_exception)
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Storm Style: Daibutsu Thunder 50 (Nuke), Izanagi's Hammer 40 (Normal), Storm Style: Divine Railgun 45 (High), Strike: Raijin 40 (Normal)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Thunder King's Wrath | +7% IDG, +2% IDT | Lightning Rod *(highest diagnostic)* | +7% IDG, +5% IDT | 26 |
| Thunder King's Wrath | +7% IDG, +2% IDT | Raiment of Storms | +7% IDG, +2% IDT, +2% REF | 25 |
| Judgement from Above | +2% IDG, +10% IDT | Vajra Tempering *(highest diagnostic)* | +4% IDG, +10% IDT | 22 |
| Judgement from Above | +2% IDG, +10% IDT | Raiment of Storms | +2% IDG, +10% IDT, +2% REF | 18 |
| Thunder Answers Thunder | +10% REF | Mandate of Thunder *(highest diagnostic)* | +2% IDG, +2% IDT, +10% REF | 18 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Mandate of Thunder, Vajra Tempering, Thunder King's Wrath, Lightning Rod | +7% IDG, +5% IDT |
| 2 | Mandate of Thunder, Vajra Tempering, Thunder King's Wrath, Raiment of Storms | +7% IDG, +2% IDT, +2% REF |
| 3 | Mandate of Thunder, Vajra Tempering, Lightning Rod, Judgement from Above | +4% IDG, +10% IDT |
| 4 | Mandate of Thunder, Vajra Tempering, Lightning Rod, Raiment of Storms | +4% IDG, +5% IDT, +2% REF |
| 5 | Mandate of Thunder, Vajra Tempering, Raiment of Storms, Galvanic Rebuke | +4% IDG, +2% IDT, +5% REF |
| 6 | Mandate of Thunder, Lightning Rod, Judgement from Above, Raiment of Storms | +2% IDG, +10% IDT, +2% REF |
| 7 | Mandate of Thunder, Lightning Rod, Raiment of Storms, Galvanic Rebuke | +2% IDG, +5% IDT, +5% REF |
| 8 | Mandate of Thunder, Raiment of Storms, Galvanic Rebuke, Thunder Answers Thunder | +2% IDG, +2% IDT, +10% REF |

## Design notes

- Damage: no node adds flat Damage. The Storm Damage rows are Daibutsu Thunder 50, Divine Railgun 45, Izanagi's Hammer 40 and Strike: Raijin 40 EP, and a flat bonus reaches all four, so even +1 lifts Daibutsu Thunder past the 50 Nuke tier; the earlier +5 route also took Railgun 45 → 50 and both 40s to 45. Maxima over every legal allocation: Increase Damage Given +7%, Increase Damage Taken +10%, Reflect +10%, Damage none.
- Increase Damage Given leverage: both Cloak rows match the kit's Storm hits (row 0 via its Highest stat filter, row 2 via Storm) and compound with Raijin's row, so each point counts two or three times on one hit: the Cloak alone goes ×1.35² ≈ ×1.82 → ×1.42² ≈ ×2.02 at +7%, all three ×2.46 → ×2.86. The Burst route therefore stops at +7%, not +10%; the bloodline passive (25 + 0.15/lvl) multiplies last. The buffs also reach normal jutsu and weapons (row 0 and Raijin: Highest-stat or element-less hits; row 2: Storm, Lightning, Water or element-less).
- Fourth purchases: Burst (01, 02, 03) takes Lightning Rod (+7% IDG, +5% IDT) or Raiment of Storms; Exposure (01, 04, 05) takes Vajra Tempering (+4% IDG, +10% IDT) or Raiment of Storms; Retaliation (06, 07, 08) takes only Mandate of Thunder. The offensive capstones cross through their sibling Hidden Arts but keep their lean: Burst with Lightning Rod is stronger on the caster's own hits in the buff windows (×1.11 versus ×1.06 from the Cloak), Exposure with Vajra Tempering on exposed enemies outside them and for allies (×1.074 versus ×1.037). No capstone shares a tag with its sibling Hidden Art.
- Uptime: cooldown 7 on all five jutsu (attacks 60 AP, Cloak 40 AP). Each buff and the exposure is live only in the two rounds after its cast, never on its own jutsu's hit. The Cloak and Raijin buffs land on the caster at cast time; Hammer's exposure is a ground effect on its spiral around the caster, re-applied to enemies standing there.
- Reflect and untouched rows: the Cloak Reflect row lists all four stat types and no element, so it matches effectively every hit the caster takes; the return bypasses shields, and other Reflect sources add to it up to the 60%-of-hit cap. Daibutsu's recoil 40%, Railgun's stun 100 and the two move rows are unsupported and unchanged; the bloodline passives (Increase Damage Given; 15% Decrease Damage Taken against Lightning) are not potency targets.

## Risks and unproven interactions

- Classification: Storm is the single qualifying element; sharing it with Arashima, Godstorm Eclipse and Stormboat Willy is expected (RUL-2026-10-03-005). 6 of 9 kit rows carry Storm; the Cloak Reflect row and two of the three Increase Damage Given rows (Cloak row 0, Raijin) are element-less, so Retaliation and most of Burst need the proposed jutsu-classification resolver. Off-kit Storm coverage is unverified.
- Increase Damage Given stacking: with both Cloak rows and Raijin live, a matching hit is ×1.42³ ≈ ×2.86 at the +7% maximum before the bloodline passive multiplies. Each row stays far below the 100 cap, but the combined amplification was not simulated against peer kits.
- Exposure: Hammer's area Increase Damage Taken reaches 45% at the route maximum on every enemy on its tiles, and allies' matching hits on them gain too. Not simulated.
- Reflect: other Reflect sources add to the Cloak's 50% and could saturate the 60%-of-pre-shield-damage cap. Reflect pays only when the caster is hit in the two rounds after the Cloak's cast, and the kit has no Decrease Damage Taken row to pair it with.
- Universal node: Mandate of Thunder is in all 8 legal full-budget builds because the Retaliation chain has no other prerequisite-closed fourth purchase, so a Retaliation player always takes +2% Increase Damage Given / Increase Damage Taken. Accepted under the narrow-kit exception.
- Delivery: Daibutsu Thunder (radius-1 spawn on an OTHER_USER target), Raijin (ground circle spawn) and Hammer (spiral around the caster) are area deliveries; realized hits and exposure depend on positioning. Every harmful row is friendly fire ENEMIES, so no ally hazards. Skill-tree effects are off in RANKED_PVP and RANKED_SPARRING; no combat simulation was performed.

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

