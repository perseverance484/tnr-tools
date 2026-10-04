# Godstorm Eclipse — Throne of the Black Sun

**Bloodline:** Godstorm Eclipse (BR-029, rank H, `szai-IgtB7PLubojIIlh-`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance / Shadow + Storm classification / forked tree · **Classification:** Shadow + Storm (multi-element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Burst, two ways: exposure (Increase Damage Taken on Event Horizon Gate, Sky-Splitting Wall and Storm-God's Heart; Total Eclipse, +8%) or self-amplification (Increase Damage Given on Wall, Tempest, Bulwark and Marrow Mantle; Storm-God Ascendant, +7%); no flat Damage · secondary Endurance: Decrease Damage Taken on Gate or Bulwark (Pillar of Heaven, +10%) and Tempest Lifesteal (Eater of Suns, +5%) · tertiary Lifesteal and Increase Damage Given riders on the endurance routes; Afterburn and Damage left unamplified.

Godstorm Eclipse is a rank H kit whose traits read Sustain / Burst Heavy / Tank, split across two keystones worn one at a time: Eclipse Marrow is needed to cast Gate, Marrow Mantle and the Shadow attacks (Tomb 40, Palm 45, Cataract 45, Midnight Verdict pierce); Godstorm Aegis is needed to cast the six Godstorm Mantle jutsu (Wall, Tempest, Bulwark, Heart 45, Raijin's Cage 50, Heavenbreaker Verdict pierce). Raijin's Cage already sits at the 50 Nuke tier and potency is element-wide, so any flat Damage pushes it past 50; this tree adds none and carries Burst through damage multipliers instead. Black Sun Rising answers "How do I hit harder: amplify my own strikes, or expose the target to everyone's?" (Storm-God Ascendant / Total Eclipse); Stormgod's Marrow answers "How do I outlast them: refuse the blow, or drink it back?" (Pillar of Heaven / Eater of Suns). Potency reaches matching supported tags on all Shadow and Storm jutsu (RUL-2026-10-03-005; multi-element, director review).

**Review status:** Fable proposal (2026-10-04 batch rebalance); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Black Sun Rising | Foundation | How do I hit harder: amplify my own strikes, or expose the target to everyone's? |
| Stormgod's Marrow | Foundation | How do I outlast them: refuse the blow, or drink it back? |
| Total Eclipse | Advanced Art | exposure: the marked target takes more from every source, allies included |
| Storm-God Ascendant | Advanced Art | self-amplification: three compounding Mantle buffs raise every hit I land, on any target |
| Pillar of Heaven | Advanced Art | fortress |
| Eater of Suns | Advanced Art | sustain offense |

**Director review recommended:** The Shadow + Storm multi-element classification (one element, both or an extension) is the only director decision here; no value needs an exception and no Damage row moves (Raijin's Cage stays at 50).

- Concern: Damage and Afterburn are supported tags with no node: flat Damage would put Raijin's Cage above 50 because potency cannot separate the keystone sides, and Afterburn does the exposure job.
- Concern: Storm-God Ascendant leads on the caster's own Aegis hits (×1.20 against ×1.17 at 3 BP) and Total Eclipse on allies' hits and on Eclipse Marrow; the split rests on a two-round multiplier model with every buff live.
- Concern: Storm-God Ascendant prints +3% Increase Damage Given, the same as Eater of Suns' rider; its value is the route total (+7%, 42%) on three compounding Aegis rows.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Shadow and Storm jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Black Sun Rising | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Event Horizon Gate, Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Storm-God's Heart, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark, Marrow Eclipse Mantle / 7 |
| 02 | Hammer of the Heavens | Hidden Art | Black Sun Rising | +2% Increase Damage Taken (enemy debuff) | Event Horizon Gate, Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Storm-God's Heart / 3 |
| 03 | Total Eclipse | Advanced Art | Hammer of the Heavens | +4% Increase Damage Taken (enemy debuff) | Event Horizon Gate, Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Storm-God's Heart / 3 |
| 04 | Charged Firmament | Hidden Art | Black Sun Rising | +2% Increase Damage Given (self buff) | Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark, Marrow Eclipse Mantle / 4 |
| 05 | Storm-God Ascendant | Advanced Art | Charged Firmament | +3% Increase Damage Given (self buff) | Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark, Marrow Eclipse Mantle / 4 |
| 06 | Stormgod's Marrow | Foundation | None | +2% Decrease Damage Taken (self buff) | Event Horizon Gate, Godstorm Mantle: Thunder-Crowned Bulwark / 2 |
| 07 | Obsidian Skin | Hidden Art | Stormgod's Marrow | +3% Decrease Damage Taken (self buff) | Event Horizon Gate, Godstorm Mantle: Thunder-Crowned Bulwark / 2 |
| 08 | Pillar of Heaven | Advanced Art | Obsidian Skin | +5% Decrease Damage Taken (self buff); +2% Lifesteal (self buff) | Event Horizon Gate, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark / 3 |
| 09 | Devouring Eclipse | Hidden Art | Stormgod's Marrow | +2% Lifesteal (self buff) | Godstorm Mantle: Tempest / 1 |
| 10 | Eater of Suns | Advanced Art | Devouring Eclipse | +3% Lifesteal (self buff); +3% Increase Damage Given (self buff) | Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark, Marrow Eclipse Mantle / 5 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Black Sun Rising** — The eclipse crowns the storm, and whatever it looks upon is laid bare. Increase Damage Given 35 → 37% on Wall, Tempest, Bulwark and Marrow Mantle (self, 2 rounds); Increase Damage Taken 35 → 37% on Gate (ally hazard), Wall and Storm-God's Heart (enemy, 2 rounds).
- **Hammer of the Heavens** — The first stroke of the sky's hammer does not kill. It cracks the shell for the next. Exposure setup: Gate (ally hazard), Wall and Storm-God's Heart Increase Damage Taken 37 → 39% with Black Sun Rising (enemy, 2 rounds).
- **Total Eclipse** — For one breath the sun is gone, and nothing it shone on has anywhere left to hide. Exposure 35 → 43% on the full route: Gate on Eclipse Marrow (ally hazard), Wall and Heart on Godstorm Aegis. Every hit the marked target takes, allies' included, is ×1.43 per live row instead of ×1.35; Wall and Heart together ×2.04 against ×1.82. No flat Damage: Raijin's Cage stays 50.
- **Charged Firmament** — The sky above the storm-god hums with held lightning, and every strike draws on it. Self-amplification setup: Increase Damage Given 37 → 39% with Black Sun Rising on Wall, Tempest and Bulwark (Godstorm Aegis) and Marrow Mantle (Eclipse Marrow); self, 2 rounds.
- **Storm-God Ascendant** — The storm stops answering the sky and answers its wearer instead. Self-amplification 35 → 42% on the full route: Wall, Tempest and Bulwark on Godstorm Aegis, Marrow Mantle on Eclipse Marrow. Three live Aegis buffs give ×2.86 against ×2.46 (×1.16) on every hit the caster lands, on any target; allies gain nothing.
- **Stormgod's Marrow** — The storm lives in the bone, and the bone does not break beneath it. Decrease Damage Taken 35 → 37% on Event Horizon Gate (Eclipse Marrow) or Thunder-Crowned Bulwark (Godstorm Aegis); self rows on the caster at cast, 2 rounds.
- **Obsidian Skin** — Cooled from godfire, the Eclipse's hide turns blades the way glass turns light. Gate or Bulwark Decrease Damage Taken 37 → 40% with Stormgod's Marrow; self rows, not positional.
- **Pillar of Heaven** — Immovable beneath the whole weight of the sky; what breaks against it only feeds it. Fortress: Gate or Bulwark Decrease Damage Taken 35 → 45% on the full route (×0.55 instead of ×0.65 on hits taken); Tempest Lifesteal 40 → 42%.
- **Devouring Eclipse** — The moon does not merely cover the sun. It feeds. Tempest Lifesteal 40 → 42% (self, 2 rounds); pierce hits count.
- **Eater of Suns** — What the eclipse swallows, the storm-god keeps for good. Sustain offense: Tempest Lifesteal 40 → 45% on the full route (hard ceiling, 15 under the 60% leech budget); Increase Damage Given 35 → 38% on Wall, Tempest, Bulwark and Marrow Mantle, raising the hits it drinks from.

## Complete four-purchase examples

| Build | Purchases | IDG | IDT | DDT | LS |
|---|---|---:|---:|---:|---:|
| Total Eclipse (Exposure) | Black Sun Rising, Hammer of the Heavens, Total Eclipse, Stormgod's Marrow | +2% | +8% | +2% | — |
| Storm-God Ascendant (Amplify) | Black Sun Rising, Hammer of the Heavens, Charged Firmament, Storm-God Ascendant | +7% | +4% | — | — |
| Pillar of Heaven (Fortress) | Black Sun Rising, Stormgod's Marrow, Obsidian Skin, Pillar of Heaven | +2% | +2% | +10% | +2% |
| Eater of Suns (Sustain) | Black Sun Rising, Stormgod's Marrow, Devouring Eclipse, Eater of Suns | +5% | +2% | +2% | +5% |

Abbreviations: IDG = Increase Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken · LS = Lifesteal. Values are per-matching-row static additions, not final combat percentages.

- **Total Eclipse:** Exposure 35 → 43% on Gate, Wall and Storm-God's Heart, so every hit the marked target takes, allies' included, grows; self buffs 37%. Stormgod's Marrow is the fourth purchase (Decrease Damage Taken 37%), which on Eclipse Marrow lifts both of Gate's rows. Charged Firmament is the all-in alternative (self buffs 39%, ×1.22 on the caster's Aegis hits).
- **Storm-God Ascendant:** Increase Damage Given 35 → 42% on Wall, Tempest, Bulwark and Marrow Mantle; three live Aegis buffs give ×2.86 on every hit the caster lands, on any target. Hammer of the Heavens is the fourth purchase (exposure 39%, ×1.23 on the caster's Aegis hits); Stormgod's Marrow is the defensive alternative.
- **Pillar of Heaven:** Gate or Bulwark Decrease Damage Taken 35 → 45%, Tempest Lifesteal 42%; Black Sun Rising is the fourth purchase (self buffs and exposure 37%). Devouring Eclipse instead takes Lifesteal to 44%.
- **Eater of Suns:** Tempest Lifesteal 40 → 45%, self buffs 40% and Decrease Damage Taken 37%, with Black Sun Rising as the fourth purchase (exposure 37%); Obsidian Skin instead gives Decrease Damage Taken 40% and self buffs 38%.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Exposure | Amplify | Fortress | Sustain |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Event Horizon Gate | 0 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 45% (+10) | 37% (+2) |
| Event Horizon Gate | 1 | Increase Damage Taken | enemy | 35% | 43% (+8) | 39% (+4) | 37% (+2) | 37% (+2) |
| Event Horizon Gate | 2 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Godstorm Mantle: Storm-God's Heart | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Godstorm Mantle: Storm-God's Heart | 1 | Increase Damage Taken | enemy | 35% | 43% (+8) | 39% (+4) | 37% (+2) | 37% (+2) |
| Godstorm Mantle: Heavenbreaker Verdict | 0 | pierce (unsupported) | enemy | 60 | 60 | 60 | 60 | 60 |
| Godstorm Mantle: Heavenbreaker Verdict | 1 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |
| Godstorm Mantle: Raijin's Cage | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Godstorm Mantle: Raijin's Cage | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Godstorm Mantle: Tempest | 0 | Afterburn | enemy | 35% | 35% | 35% | 35% | 35% |
| Godstorm Mantle: Tempest | 1 | Lifesteal | self | 40% | 40% | 40% | 42% (+2) | 45% (+5) |
| Godstorm Mantle: Tempest | 2 | Increase Damage Given | self | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 40% (+5) |
| Godstorm Mantle: Sky-Splitting Wall | 0 | Increase Damage Given | self | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 40% (+5) |
| Godstorm Mantle: Sky-Splitting Wall | 1 | Increase Damage Taken | enemy | 35% | 43% (+8) | 39% (+4) | 37% (+2) | 37% (+2) |
| Godstorm Mantle: Sky-Splitting Wall | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Godstorm Mantle: Thunder-Crowned Bulwark | 0 | Increase Damage Given | self | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 40% (+5) |
| Godstorm Mantle: Thunder-Crowned Bulwark | 1 | Decrease Damage Taken | self | 35% | 37% (+2) | 35% | 45% (+10) | 37% (+2) |
| Godstorm Mantle: Thunder-Crowned Bulwark | 2 | move (unsupported) | self | 1 | 1 | 1 | 1 | 1 |
| Obsidian Tomb | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Obsidian Tomb | 1 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Obsidian Tomb | 2 | debuffprevent (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Midnight Verdict | 0 | pierce (unsupported) | enemy | 66 | 66 | 66 | 66 | 66 |
| Midnight Verdict | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Corona Devourer Palm | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Corona Devourer Palm | 1 | recoil (unsupported) | enemy | 35% | 35% | 35% | 35% | 35% |
| Marrow Eclipse Mantle | 0 | absorb (unsupported) | self | 35% | 35% | 35% | 35% | 35% |
| Marrow Eclipse Mantle | 1 | Increase Damage Given | self | 35% | 37% (+2) | 42% (+7) | 37% (+2) | 40% (+5) |
| Black Sun Cataract | 0 | Damage | enemy | 45 | 45 | 45 | 45 | 45 |
| Black Sun Cataract | 1 | drain (unsupported) | enemy | 250 | 250 | 250 | 250 | 250 |
| Black Sun Cataract | 2 | wound (unsupported) | enemy | 30% | 30% | 30% | 30% | 30% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 12; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +7% Increase Damage Given, +8% Increase Damage Taken, +10% Decrease Damage Taken, +5% Lifesteal (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Total Eclipse: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Storm-God Ascendant: +7% Increase Damage Given (2 + 2 + 3; off band)
  - Route Pillar of Heaven: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Eater of Suns: +5% Lifesteal (0 + 2 + 3; on band)
- Supported rows in kit: 16 (AB 1, DMG 5, DDT 2, IDG 4, IDT 3, LS 1)
- Supported tags present but not targeted: afterburn, damage
- Strongest full build by row-weighted total: Black Sun Rising, Hammer of the Heavens, Total Eclipse, Charged Firmament (raw +12, row-weighted 40)
- Lowest row-weighted node: Devouring Eclipse (2)

Validator warnings:

- classification status: multi-element: director review (director decision)
- ally-hazard area rows amplified (friendly fire none/ALL): Event Horizon Gate#1
- supported tags present in kit but not targeted by any node: afterburn, damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Godstorm Mantle: Storm-God's Heart 45 (High), Godstorm Mantle: Raijin's Cage 50 (Nuke), Obsidian Tomb 40 (Normal), Corona Devourer Palm 45 (High), Black Sun Cataract 45 (High)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Total Eclipse | +2% IDG, +8% IDT | Charged Firmament *(highest diagnostic)* | +4% IDG, +8% IDT | 40 |
| Total Eclipse | +2% IDG, +8% IDT | Stormgod's Marrow | +2% IDG, +8% IDT, +2% DDT | 36 |
| Storm-God Ascendant | +7% IDG, +2% IDT | Hammer of the Heavens *(highest diagnostic)* | +7% IDG, +4% IDT | 40 |
| Storm-God Ascendant | +7% IDG, +2% IDT | Stormgod's Marrow | +7% IDG, +2% IDT, +2% DDT | 38 |
| Pillar of Heaven | +10% DDT, +2% LS | Black Sun Rising *(highest diagnostic)* | +2% IDG, +2% IDT, +10% DDT, +2% LS | 36 |
| Pillar of Heaven | +10% DDT, +2% LS | Devouring Eclipse | +10% DDT, +4% LS | 24 |
| Eater of Suns | +3% IDG, +2% DDT, +5% LS | Black Sun Rising *(highest diagnostic)* | +5% IDG, +2% IDT, +2% DDT, +5% LS | 35 |
| Eater of Suns | +3% IDG, +2% DDT, +5% LS | Obsidian Skin | +3% IDG, +5% DDT, +5% LS | 27 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Black Sun Rising, Hammer of the Heavens, Total Eclipse, Charged Firmament | +4% IDG, +8% IDT |
| 2 | Black Sun Rising, Hammer of the Heavens, Total Eclipse, Stormgod's Marrow | +2% IDG, +8% IDT, +2% DDT |
| 3 | Black Sun Rising, Hammer of the Heavens, Charged Firmament, Storm-God Ascendant | +7% IDG, +4% IDT |
| 4 | Black Sun Rising, Hammer of the Heavens, Charged Firmament, Stormgod's Marrow | +4% IDG, +4% IDT, +2% DDT |
| 5 | Black Sun Rising, Hammer of the Heavens, Stormgod's Marrow, Obsidian Skin | +2% IDG, +4% IDT, +5% DDT |
| 6 | Black Sun Rising, Hammer of the Heavens, Stormgod's Marrow, Devouring Eclipse | +2% IDG, +4% IDT, +2% DDT, +2% LS |
| 7 | Black Sun Rising, Charged Firmament, Storm-God Ascendant, Stormgod's Marrow | +7% IDG, +2% IDT, +2% DDT |
| 8 | Black Sun Rising, Charged Firmament, Stormgod's Marrow, Obsidian Skin | +4% IDG, +2% IDT, +5% DDT |
| 9 | Black Sun Rising, Charged Firmament, Stormgod's Marrow, Devouring Eclipse | +4% IDG, +2% IDT, +2% DDT, +2% LS |
| 10 | Black Sun Rising, Stormgod's Marrow, Obsidian Skin, Pillar of Heaven | +2% IDG, +2% IDT, +10% DDT, +2% LS |
| 11 | Black Sun Rising, Stormgod's Marrow, Obsidian Skin, Devouring Eclipse | +2% IDG, +2% IDT, +5% DDT, +2% LS |
| 12 | Black Sun Rising, Stormgod's Marrow, Devouring Eclipse, Eater of Suns | +5% IDG, +2% IDT, +2% DDT, +5% LS |
| 13 | Stormgod's Marrow, Obsidian Skin, Pillar of Heaven, Devouring Eclipse | +10% DDT, +4% LS |
| 14 | Stormgod's Marrow, Obsidian Skin, Devouring Eclipse, Eater of Suns | +3% IDG, +5% DDT, +5% LS |

## Design notes

- Structure unchanged (01→02→03, 01→04→05, 06→07→08, 06→09→10). Black Sun Rising forks into exposure (Total Eclipse, Increase Damage Taken 2 + 2 + 4) and self-amplification (Storm-God Ascendant, Increase Damage Given 2 + 2 + 3); Stormgod's Marrow forks into a wall (Pillar of Heaven, Decrease Damage Taken 2 + 3 + 5 with a +2% Lifesteal rider) and leech (Eater of Suns, Lifesteal 2 + 3 with a +3% Increase Damage Given rider, since Lifesteal is at its hard ceiling).
- Exposure versus self-amplification: Increase Damage Taken multiplies every hit the marked target takes, from any source, allies included; Increase Damage Given multiplies only the caster's hits, but on every target. Godstorm Aegis carries three Increase Damage Given rows against two exposure rows, so the self route is calibrated one point lower (+7% against +8%).
- Damage: no node adds flat Damage. The previous +5 Damage route took Raijin's Cage 50 → 55, Heart, Cataract and Palm 45 → 50 and Tomb 40 → 45; even +2 Damage would put Cage at 52.
- Afterburn has no node. Its one row (Tempest) enlarges every non-pierce hit the target takes, which is the exposure job; as a capstone it duplicated Total Eclipse, and as a rider it would either rejoin that axis or raise the offensive ceiling.
- Keystones are exclusive per battle (ENGINE_GAP_REGISTER G7). In-kit, Wall, Tempest, Bulwark and Heart need Godstorm Aegis to cast and Gate and Marrow Mantle need Eclipse Marrow, so an Aegis player has three own Increase Damage Given rows, two exposure rows and one Decrease Damage Taken row live, and an Eclipse Marrow player one of each. Off-kit Shadow or Storm jutsu with these rows (unverified) would also benefit.
- Maxima over every legal allocation: Increase Damage Taken +8% (01+02+03), Increase Damage Given +7% (01+04+05), Decrease Damage Taken +10%, Lifesteal +5%; no Afterburn.
- Fourth purchases never add to a capstone's own primary. Aegis model (caster's hits on the target, Wall, Tempest, Bulwark and Heart live): Storm-God Ascendant ×1.20 at 3 BP and ×1.23 with Hammer of the Heavens (the tree's offensive ceiling, level with the previous ×1.23); Total Eclipse ×1.17 and ×1.22 with Charged Firmament. Allies' hits on the target: Total Eclipse ×1.12 against ×1.03 (×1.12 against ×1.06 with those fourths). On Eclipse Marrow Total Eclipse leads, ×1.075 against ×1.067. Pillar of Heaven + Devouring Eclipse caps Lifesteal at 44%.
- Delivery: buff casts are 40 AP, Damage casts 60 AP, cooldowns 7. Decrease Damage Taken, Increase Damage Given and Lifesteal rows land on the caster at cast and are live the two rounds after; no buff or debuff helps a hit in its cast round (§3b). The bloodline Increase Damage Given passive multiplies last. Ranked modes skip skill-tree effects.

## Risks and unproven interactions

- Classification (multi-element, director review): Shadow and Storm both sit on the kit's Damage rows, so the proposal reaches matching supported tags on all Shadow and all Storm jutsu; one element, both or an extension is the director's call. Gate, Tempest, Wall, Bulwark and Marrow Mantle carry no Shadow or Storm row, so in-kit they qualify only through an authored jutsu classification (ENGINE_GAP_REGISTER G1); 11 of 16 supported rows are unreachable by the current row-element resolver. Off-kit coverage is unverified.
- Ally hazard: Event Horizon Gate's exposure (friendly fire none = ALL) also lands on allies in its radius-1 circle, up to 43% on Total Eclipse; the caster is never a target.
- Keystone split: in-kit, an Eclipse Marrow player casts only Gate (exposure, Decrease Damage Taken) and Marrow Mantle (self buff) among this tree's rows, so Total Eclipse, Storm-God Ascendant and Pillar of Heaven each reach one row there. The only Lifesteal row is on Tempest, which needs Godstorm Aegis to cast; on Eclipse Marrow, Eater of Suns' route still gives +3% Increase Damage Given on Marrow Mantle and +2% Decrease Damage Taken on Gate. Whether a keystone can be swapped mid-battle was not read at the pin.
- Compounding: same-tag rows stack (BATTLE_TAG_STACKING true). Three live Aegis self buffs give ×2.46 at 35%, ×2.74 at 40% (Eater of Suns with Black Sun Rising) and ×2.86 at 42% (Storm-God Ascendant) on a hit all three cover, and exposure multiplies on top. Lifesteal shares the 60% leech budget with vamp and counts pierce hits (Heavenbreaker Verdict on the same keystone). The route comparisons are a two-round multiplier model with every buff live, not a combat simulation; uptime, AP and AoE target counts were not modelled.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Shadow and Storm jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

