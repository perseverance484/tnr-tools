# Bloodright cross-bloodline balance matrix

Same access budget (4 BP, 1 BP per once-only skill, forks only) for every tree. Raw flat total sums every static addition in a legal full allocation; row-weighted total multiplies each addition by the number of supported kit rows it reaches. Both are structural/arithmetic measures, not combat strength. Inherited kit strength (rank, row count, baseline values) is listed separately from the Bloodright additions.

Reference: Taiyo Kami (docs/design/bloodright/examples/taiyo_kami.json). Trees present: 5 of 43 approved remaining bloodlines; without a tree: Ancient Tailed Demon, Bakuhatsu, Blue Blade Eyes, Cosmic Ascendant, Crystal Essence, Ethereal Monarch, Eyes of the Forsaken King, Godstorm Eclipse, Ha Yanagi, Heavenly Sonata, Houkyuken, Hyouga Yui, Itojinsei, Kyuko-sei, Loup-Garou, Lycanthropy, Megumi Kijo, Musashi Ken, Namikaze, Night Parade of A Thousand Demons, Oblivion Seal, Primal Radiance, Reptilian, Sands of Time, Sea-King's Blessing, Shadow Weaver, Shakunetsu Sakura, Shinrai Ou, Shinseina Ki, Shiroi Youso, Suragu, Teno Yuki, Tenohira Musei, Terra Nova, Tetsugan, Vaporia, Voltara Divine, Yaketsuku Netsu. No combat simulation was performed.

## Structure and access

| Bloodline | Rank | Jutsu | Supp. rows | Adverse | Label (kind) | Nodes F/H/A | Legal 4-BP | Non-dom | Max adv | Min 2-adv cost | Depth | Errors |
|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| Taiyo Kami (reference) | A | 5 | 9 | 0 | Scorch () | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Aerathiel | A | 5 | 9 | 0 | Dust (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Arashima | A | 5 | 6 | 0 | Storm (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Blood-Enchanted Eyes | S | 8 | 15 | 0 | Shadow (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Dai Kenja | D | 3 | 6 | 1 | Dai Kenja (ext) | 2/4/4 | 14 | 13 | 1 | 5 | 3 | 0 |
| Nature's Blessing | B | 3 | 5 | 0 | Wood (element) | 2/3/3 | 8 | 7 | 1 | 5 | 3 | 0 |

## Added strength (Bloodright only)

| Bloodline | Emphasis (P / S / T) | Max per-tag additions | Max raw total | Δ vs ref | Max row-weighted | Δ vs ref | Strongest full build | Lowest node |
|---|---|---|---:|---:|---:|---:|---|---|
| Taiyo Kami | — / — / — | DMG +5, IDG +5, DDG +10, IDT +7, DDT +10, AB +10 | 24 | +0 | 31 | +0 | Dawnheart, Crown of Cinders, Emberwake, Eternal Noon (DMG +2, IDG +5, IDT +5, AB +10) | Emberwake (3) |
| Aerathiel | Damage (Dust attacks) / Increase Damage Taken (AOE exposure) / Reflect and Decrease Damage Given (Atomic Shield / Windshear control) | DMG +5, IDG +5, DDG +10, IDT +7, REF +10 | 19 | -5 | 30 | -1 | Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay (DMG +2, IDG +5, IDT +7) | Particulate Ward (3) |
| Arashima | Lifesteal (sustain; the kit's identity, +10 ceiling) / Decrease Damage Taken and Decrease Damage Given (co-primary fortress and suppression routes, +10 ceilings) / Damage (Storm AoE burst, +5 ceiling) and Increase Damage Given (glue across routes, +5 ceiling) | DMG +5, IDG +5, DDG +10, DDT +10, LS +10 | 20 | -4 | 20 | -11 | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder (IDG +2, DDG +10, DDT +4, LS +4) | Crimson Downpour (3) |
| Blood-Enchanted Eyes | Damage (Shadow; two castable rows per keystone) / Enemy exposure (Increase Damage Taken + Afterburn) / Self sustain (Decrease Damage Taken, Lifesteal) with Increase/Decrease Damage Given support | DMG +6, IDG +5, DDG +5, IDT +5, DDT +8, AB +10, LS +8 | 21 | -3 | 42 | +11 | Scarlet Gaze, Opened Veins, Rite of Exsanguination, Iron in the Blood (DMG +6, IDG +2, DDG +2, IDT +2, DDT +2) | Carrion Fever (3) |
| Dai Kenja | Overloaded Impact offense (Damage and Increase Damage Given) / Decrease Damage Given (Chakra Overload / Chakra Cannon suppression) / Increase Damage Taken (Chakra Overload exposure; adverse on Overloaded Impact) | DMG +6, IDG +10, DDG +8, IDT +5 | 14 | -10 | 24 | -7 | Sage's Rebuke, Smothered Current, Cracked Vessel, Shattered Vessel (DDG +7, IDT +5) | Brimming Cup (3) |
| Nature's Blessing | Co-primary — Sustain (Verdant Bastion Heal and Increase Heal) and Wood damage (Nature's Fury, Nature's Curse) / Exposure — Increase Damage Taken (Nature's Fury) / None — absorb and drain on Nature's Curse are unsupported | DMG +6, IDT +7, IH +8, HEAL +5 | 16 | -8 | 18 | -13 | Thorn and Rot, Ironwood Lash, Old Growth's Wrath, Sap of the Grove (DMG +6, IDT +2, IH +2, HEAL +2) | Stripped Bark (2) |

## Example builds

| Bloodline | Build | Purchases | Raw total | Row-weighted | Bonuses |
|---|---|---|---:|---:|---|
| Taiyo Kami | Solar Cataclysm (Burst) | 01, 02, 03, 06 | 13 | 25 | DMG +5, IDG +2, DDG +2, IDT +2, DDT +2 |
| Taiyo Kami | Eternal Noon (Burn pressure) | 01, 04, 05, 06 | 24 | 29 | IDG +5, DDG +2, IDT +5, DDT +2, AB +10 |
| Taiyo Kami | Sovereign Sun (Fortified offense) | 01, 06, 07, 08 | 19 | 24 | IDG +5, DDG +2, IDT +2, DDT +10 |
| Taiyo Kami | Dying Light (Suppression) | 06, 07, 09, 10 | 20 | 20 | DDG +10, IDT +5, DDT +5 |
| Aerathiel | Total Disintegration (Burst) | 01, 02, 03, 06 | 13 | 27 | DMG +5, IDG +2, DDG +2, IDT +2, REF +2 |
| Aerathiel | Terminal Decay (Pressure) | 01, 02, 04, 05 | 14 | 30 | DMG +2, IDG +5, IDT +7 |
| Aerathiel | Atomic Reprisal (Fortified) | 01, 06, 07, 08 | 19 | 26 | IDG +5, DDG +2, IDT +2, REF +10 |
| Aerathiel | Requiem of Dust (Suppression) | 01, 06, 09, 10 | 18 | 24 | IDG +2, DDG +10, IDT +4, REF +2 |
| Arashima | Reaper's Harvest (Sustain) | 01, 04, 05, 06 | 19 | 19 | IDG +5, DDG +2, DDT +2, LS +10 |
| Arashima | Sundered Sky (Burst) | 01, 02, 03, 06 | 13 | 18 | DMG +5, IDG +2, DDG +2, DDT +2, LS +2 |
| Arashima | Unbroken Horizon (Fortress) | 01, 06, 07, 08 | 19 | 19 | IDG +5, DDG +2, DDT +10, LS +2 |
| Arashima | Silence After Thunder (Suppression) | 01, 06, 09, 10 | 20 | 20 | IDG +2, DDG +10, DDT +4, LS +4 |
| Blood-Enchanted Eyes | Rite of Exsanguination (Burst) | 01, 02, 03, 06 | 14 | 42 | DMG +6, IDG +2, DDG +2, IDT +2, DDT +2 |
| Blood-Enchanted Eyes | Red Pestilence (Plague) | 01, 04, 05, 06 | 21 | 37 | IDG +2, DDG +2, IDT +5, DDT +2, AB +10 |
| Blood-Enchanted Eyes | Feast of the Fallen (Sustain) | 01, 06, 09, 10 | 19 | 32 | IDG +5, DDG +2, IDT +2, DDT +2, LS +8 |
| Blood-Enchanted Eyes | Deathless Vitality (Fortress) | 01, 06, 07, 08 | 17 | 36 | IDG +2, DDG +5, IDT +2, DDT +8 |
| Dai Kenja | Breaking Point (Burst) | 01, 02, 03, 06 | 13 | 15 | DMG +6, IDG +5, DDG +2 |
| Dai Kenja | Boundless Reservoir (Amplifier) | 01, 04, 05, 06 | 12 | 14 | IDG +10, DDG +2 |
| Dai Kenja | Edict of Silence (Suppression) | 01, 06, 07, 08 | 11 | 19 | IDG +3, DDG +8 |
| Dai Kenja | Shattered Vessel (Exposure) | 06, 07, 09, 10 | 12 | 24 | DDG +7, IDT +5 |
| Nature's Blessing | Old Growth's Wrath (Burst) | 01, 02, 03, 06 | 12 | 18 | DMG +6, IDT +2, IH +2, HEAL +2 |
| Nature's Blessing | Blight and Harvest (Exposure) | 01, 04, 05, 06 | 15 | 16 | DMG +1, IDT +7, IH +5, HEAL +2 |
| Nature's Blessing | Everbloom Sanctuary (Sustain) | 01, 06, 07, 08 | 16 | 17 | DMG +1, IDT +2, IH +8, HEAL +5 |

## Coverage gaps and exceptions

- **Aerathiel:** classification label shared with 2 other census bloodline(s)
- **Arashima:** classification label shared with 3 other census bloodline(s)
- **Blood-Enchanted Eyes:** classification label shared with 13 other census bloodline(s)
- **Dai Kenja:** 1 adverse supported row(s) in kit
- **Nature's Blessing:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on five rows (Damage x2, Increase Damage Taken x1, Increase Heal x1, Heal x1). The enemy-facing root (Thorn and Rot) forks into a damage route and an exposure route; the self-facing root (Sap of the Grove) is a single Foundation → Hidden → Advanced chain. A second sustain Hidden Art or capstone under Sap of the Grove would breach the +5 Heal / +10 Increase Heal guardrails in a full build. A damage or exposure Hidden Art or capstone under Sap of the Grove is structurally possible (any two Advanced Arts would still cost at least 5 BP) but would duplicate the Thorn and Rot routes and open a second path to the Damage and Increase Damage Taken ceilings; the design declines that by choice so that Old Growth's Wrath and Blight and Harvest remain the only ways to +6 Damage and +7 IDT. Draft 1's Thorned Bloom (+2 Damage under Sap of the Grove, an exact twin of Ironwood Lash whose builds tied Ironwood Lash builds on every bonus vector) was removed for that reason. Three distinct complete builds (Burst, Exposure, Sustain) exist; Burst and Exposure each have two fourth-purchase choices, and Sustain's fourth purchase is always Thorn and Rot (06,07,08 plus 01 is legal and non-dominated).; classification label shared with 1 other census bloodline(s)

Reading guide: a higher row-weighted total means the same static additions touch more effect rows; it says nothing about delivery, uptime, action cost, duration, caps (percentage tags cap at 100; Afterburn, Reflect and the lifesteal/vamp leech budget cap at 60% of a hit) or the combat multiplication that follows. Mechanical legality and numerical non-dominance do not prove combat balance.

