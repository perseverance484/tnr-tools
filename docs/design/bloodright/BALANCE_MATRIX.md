# Bloodright cross-bloodline balance matrix

Same access budget (4 BP, 1 BP per once-only skill, forks only) for every tree. Raw flat total sums every static addition in a legal full allocation; row-weighted total multiplies each addition by the number of supported kit rows it reaches. Both are structural/arithmetic measures, not combat strength. Inherited kit strength (rank, row count, baseline values) is listed separately from the Bloodright additions.

Reference: Taiyo Kami (docs/design/bloodright/examples/taiyo_kami.json). Trees present: 34 of 43 approved remaining bloodlines; without a tree: Ethereal Monarch, Eyes of the Forsaken King, Hyouga Yui, Kyuko-sei, Night Parade of A Thousand Demons, Shadow Weaver, Teno Yuki, Voltara Divine, Yaketsuku Netsu. No combat simulation was performed.

## Structure and access

| Bloodline | Rank | Jutsu | Supp. rows | Adverse | Label (kind) | Nodes F/H/A | Legal 4-BP | Non-dom | Max adv | Min 2-adv cost | Depth | Errors |
|---|---|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---|
| Taiyo Kami (reference) | A | 5 | 9 | 0 | Scorch () | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Aerathiel | A | 5 | 9 | 0 | Dust (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Ancient Tailed Demon | B | 3 | 5 | 0 | Ancient Tailed Demon (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Arashima | A | 5 | 6 | 0 | Storm (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Bakuhatsu | A | 5 | 8 | 0 | Explosion (element) | 2/4/3 | 12 | 12 | 1 | 5 | 3 | 0 |
| Blood-Enchanted Eyes | S | 8 | 15 | 0 | Shadow (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Blue Blade Eyes | S | 8 | 16 | 0 | Ice (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Cosmic Ascendant | S | 5 | 10 | 0 | Cosmic Ascendant (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Crystal Essence | A | 5 | 8 | 0 | Crystal (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Dai Kenja | D | 3 | 6 | 1 | Dai Kenja (ext) | 2/4/4 | 14 | 13 | 1 | 5 | 3 | 0 |
| Godstorm Eclipse | H | 12 | 16 | 0 | Godstorm Eclipse (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Ha Yanagi | D | 3 | 6 | 0 | Ha Yanagi (ext) | 2/4/4 | 14 | 13 | 1 | 5 | 3 | 0 |
| Heavenly Sonata | A | 5 | 7 | 0 | Yin-Yang (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Houkyuken | A | 5 | 10 | 0 | Magnet (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Itojinsei | A | 5 | 9 | 0 | Magnet (element) | 2/4/4 | 14 | 13 | 1 | 5 | 3 | 0 |
| Loup-Garou | D | 3 | 4 | 0 | Loup-Garou (ext) | 2/3/3 | 8 | 7 | 1 | 5 | 3 | 0 |
| Lycanthropy | B | 3 | 5 | 0 | Lycanthropy (ext) | 2/3/2 | 7 | 7 | 1 | 5 | 3 | 0 |
| Megumi Kijo | B | 3 | 5 | 0 | Megumi Kijo (ext) | 2/3/3 | 8 | 8 | 1 | 5 | 3 | 0 |
| Musashi Ken | D | 3 | 6 | 0 | Musashi Ken (ext) | 2/3/3 | 8 | 7 | 1 | 5 | 3 | 0 |
| Namikaze | C | 4 | 8 | 0 | Namikaze (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Nature's Blessing | B | 3 | 5 | 0 | Wood (element) | 2/3/3 | 8 | 7 | 1 | 5 | 3 | 0 |
| Oblivion Seal | A | 5 | 7 | 0 | Shadow (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Primal Radiance | C | 3 | 6 | 0 | Primal Radiance (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Reptilian | B | 3 | 4 | 0 | Reptilian (ext) | 2/3/3 | 8 | 8 | 1 | 5 | 3 | 0 |
| Sands of Time | H | 5 | 9 | 0 | Sand (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Sea-King's Blessing | C | 3 | 5 | 0 | Sea-King's Blessing (ext) | 2/3/3 | 8 | 8 | 1 | 5 | 3 | 0 |
| Shakunetsu Sakura | A | 5 | 7 | 0 | Scorch (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Shinrai Ou | A | 5 | 9 | 0 | Storm (element) | 2/3/3 | 8 | 8 | 1 | 5 | 3 | 0 |
| Shinseina Ki | A | 5 | 6 | 0 | Wood (element) | 2/3/3 | 8 | 8 | 1 | 5 | 3 | 0 |
| Shiroi Youso | S | 6 | 11 | 0 | Shiroi Youso (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Suragu | A | 5 | 7 | 0 | Lava (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Tenohira Musei | A | 5 | 8 | 0 | Yin-Yang (element) | 2/4/4 | 14 | 12 | 1 | 5 | 3 | 0 |
| Terra Nova | C | 3 | 5 | 0 | Terra Nova (ext) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Tetsugan | H | 11 | 20 | 0 | Metal (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |
| Vaporia | A | 5 | 10 | 0 | Boil (element) | 2/4/4 | 14 | 14 | 1 | 5 | 3 | 0 |

## Added strength (Bloodright only)

| Bloodline | Emphasis (P / S / T) | Max per-tag additions | Max raw total | Δ vs ref | Max row-weighted | Δ vs ref | Per supported row | Median build | Strongest full build | Lowest node |
|---|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Taiyo Kami | — / — / — | DMG +5, IDG +5, DDG +10, IDT +7, DDT +10, AB +10 | 24 | +0 | 31 | +0 | 3.44 | 21 | Dawnheart, Crown of Cinders, Emberwake, Eternal Noon (DMG +2, IDG +5, IDT +5, AB +10) | Emberwake (3) |
| Aerathiel | Damage (Dust attacks) / Increase Damage Taken (AOE exposure) / Reflect and Decrease Damage Given (Atomic Shield / Windshear control) | DMG +5, IDG +5, DDG +10, IDT +7, REF +10 | 19 | -5 | 30 | -1 | 3.33 | 24 | Entropic Grasp, Particle Collapse, Hollowing Wind, Terminal Decay (DMG +2, IDG +5, IDT +7) | Particulate Ward (3) |
| Ancient Tailed Demon | Enemy pressure — Afterburn and Increase Damage Taken on Demonic Embrace / Sustained damage — Increase Damage Given on Demonic Vitae; burst — Damage on Ancient Demon Roar / Defense — Decrease Damage Taken on Demonic Vitae | DMG +6, IDG +10, IDT +5, DDT +10, AB +10 | 19 | -5 | 19 | -12 | 3.8 | 16 | Demon's Grasp, Festering Brand, Consuming Malice, Demon's Marrow (IDG +2, IDT +5, DDT +2, AB +10) | Rending Bellow (3) |
| Arashima | Lifesteal (sustain; the kit's identity, +10 ceiling) / Decrease Damage Taken and Decrease Damage Given (co-primary fortress and suppression routes, +10 ceilings) / Damage (Storm AoE burst, +5 ceiling) and Increase Damage Given (glue across routes, +5 ceiling) | DMG +5, IDG +5, DDG +10, DDT +10, LS +10 | 20 | -4 | 20 | -11 | 3.33 | 18 | Tempest Hymn, Stillness in the Squall, Deadwind Dirge, Silence After Thunder (IDG +2, DDG +10, DDT +4, LS +4) | Crimson Downpour (3) |
| Bakuhatsu | Damage (Explosion area attacks) / Afterburn and Increase Damage Taken (Charge 4 Explosion pressure) / Decrease Damage Taken and Increase Damage Given (Blast Shield / charge buffs) | DMG +5, IDG +5, IDT +5, DDT +10, AB +10 | 19 | -5 | 27 | -4 | 3.38 | 19 | Primed Fuse, Shaped Charge, Ground Zero, Powder Keg (DMG +5, IDG +5, IDT +2) | Hardened Casing (3) |
| Blood-Enchanted Eyes | Damage (Shadow; two castable rows per keystone) / Enemy exposure (Increase Damage Taken + Afterburn) / Self sustain (Decrease Damage Taken, Lifesteal) with Increase/Decrease Damage Given support | DMG +6, IDG +5, DDG +5, IDT +5, DDT +8, AB +10, LS +8 | 21 | -3 | 42 | +11 | 2.8 | 30 | Scarlet Gaze, Opened Veins, Rite of Exsanguination, Iron in the Blood (DMG +6, IDG +2, DDG +2, IDT +2, DDT +2) | Carrion Fever (3) |
| Blue Blade Eyes | Burst offense (Damage on five Ice rows; Increase Damage Given on four self rows) / Control (Increase Damage Taken on three enemy rows; Decrease Damage Given on Icebound Might) / Self preservation and sustain (Decrease Damage Taken on the two ungated casts; Lifesteal on Arctic Frost) | DMG +5, IDG +5, DDG +9, IDT +5, DDT +8, LS +8 | 19 | -5 | 45 | +14 | 2.81 | 36 | Sapphire Edge, Honed Crescent, Stroke That Splits Stone, Unblinking Sapphire (DMG +5, IDG +2, DDG +2, IDT +2, DDT +2) | Frostbitten Grip (3) |
| Cosmic Ascendant | Exposure into burst: Increase Damage Taken (2 rows, +5 ceiling) feeding Cosmic Explosion Damage (1 row, +6 ceiling) / Decrease Damage Taken (Defensive; 3 rows on Cosmic Chains, Cosmic Energy and Cosmic Aura; +7 ceiling) / Cosmic Intent's Afterburn (+10 ceiling) and Lifesteal (+8 ceiling) as rival capstones; Increase Damage Given (+5) and Decrease Damage Given (+5) as glue | DMG +6, IDG +5, DDG +5, IDT +5, DDT +7, AB +10, LS +8 | 21 | -3 | 32 | +1 | 3.2 | 25 | Celestial Alignment, Gravity Well, Event Horizon, Heart of the Singularity (IDG +5, DDG +2, IDT +2, DDT +7) | Collapsing Star (3) |
| Crystal Essence | Damage (Crystal burst on all three attacks, +5 ceiling) / Increase Damage Taken (Crystal Sphere and Crystal Cave exposure, two rows, +7 ceiling) / Decrease Damage Taken (Crystal Sphere, +10 ceiling) and Reflect (Crystal Cave, +10 ceiling), with Increase Damage Given as route glue (+5 ceiling on Kōsai Shippū) | DMG +5, IDG +5, IDT +7, DDT +10, REF +10 | 19 | -5 | 25 | -6 | 3.12 | 20 | Prismatic Focus, Razor Lattice, Flaw in the Stone, Break Along the Flaw (DMG +2, IDG +5, IDT +7) | Flawless Sphere (3) |
| Dai Kenja | Overloaded Impact offense (Damage and Increase Damage Given) / Decrease Damage Given (Chakra Overload / Chakra Cannon suppression) / Increase Damage Taken (Chakra Overload exposure; adverse on Overloaded Impact) | DMG +6, IDG +10, DDG +8, IDT +5 | 14 | -10 | 24 | -7 | 4.0 | 14 | Sage's Rebuke, Smothered Current, Cracked Vessel, Shattered Vessel (DDG +7, IDT +5) | Brimming Cup (3) |
| Godstorm Eclipse | Damage (Burst Heavy; five Shadow/Storm damage rows, +5 ceiling) / Lifesteal (Sustain, Tempest, +10 ceiling) and Decrease Damage Taken (Tank, Gate and Bulwark, +7 ceiling) / Afterburn pressure (Tempest, +10 ceiling); Increase Damage Given (+5 on four rows) and Increase Damage Taken (+5 on three rows) as glue | DMG +5, IDG +5, IDT +5, DDT +7, AB +10, LS +10 | 21 | -3 | 45 | +14 | 2.81 | 34 | Black Sun Rising, Hammer of the Heavens, Total Eclipse, Stormgod's Marrow (DMG +5, IDG +2, IDT +2, DDT +2, LS +2) | Charged Firmament (3) |
| Ha Yanagi | Enemy debuff control: Decrease Damage Given (Wailing Bark, Petal Nightmare) and Increase Damage Taken (Blighted Tree) / Raw power on the two damage casts (Blighted Tree formula 40, Petal Nightmare static 40) / Self amplification: the single Increase Damage Given row on Wailing Bark | DMG +5, IDG +10, DDG +8, IDT +8 | 15 | -9 | 20 | -11 | 3.33 | 15 | Mourning Boughs, Veil of Falling Petals, Blight Takes Root, Hollow at the Heart (DDG +6, IDT +8) | Blight Takes Root (3) |
| Heavenly Sonata | Decrease Damage Taken and Decrease Damage Given (Celestial Harmony Shield fortress, Harmonic Chamber suppression) / Damage (three Yin-Yang Genjutsu attacks) / Increase Damage Taken and Increase Damage Given (Foreboding Interlude exposure, Lullaby empowerment) | DMG +5, IDG +5, DDG +10, IDT +7, DDT +10 | 18 | -6 | 23 | -8 | 3.29 | 17 | Opening Measure, Rising Crescendo, Fortissimo Finale, Harmonic Balance (DMG +5, IDG +2, DDG +2, IDT +2, DDT +2) | Dissonant Chord (2) |
| Houkyuken | Magnet burst (Damage on four casts; self Increase Damage Given on Houkyuken: Magnetic Assignment and Houkyu Dance) / Enemy exposure (Increase Damage Taken on Morning Star and Houkyuken: Magnetic Assignment) / Self defense (Decrease Damage Taken on Houkyuken: Magnetic Assignment; Reflect on Rising Star) | DMG +5, IDG +4, IDT +7, DDT +10, REF +10 | 18 | -6 | 32 | +1 | 3.2 | 23 | Lodestone Draw, Polarized Fist, Starfall Hammer, Repelling Field (DMG +5, IDG +2, IDT +2, DDT +2, REF +2) | Magnetized Guard (3) |
| Itojinsei | Magnet burst (Damage on all four casts: Iron Web Entrapment, Wire Blast Plus, Spiraling Wires, Lightning Threads) / Enemy suppression (Decrease Damage Given on Wire Blast Plus and Eternal Embrace) / Wielder amplification and exposure (self Increase Damage Given on Spiraling Wires and Eternal Embrace; Increase Damage Taken on Lightning Threads) | DMG +5, IDG +7, DDG +9, IDT +10 | 17 | -7 | 32 | +1 | 3.56 | 24 | Taut Filament, Razor Strands, Severing Lattice, Tangling Snare (DMG +5, IDG +2, DDG +3, IDT +2) | Conductive Seam (3) |
| Loup-Garou | Self amplification — Increase Damage Given (Nature's Hunter self buff) / Exposure — Increase Damage Taken (Life reaver) and Damage (Nature's Hunter) / Sustain — Heal (Nature's Hunter) | DMG +6, IDG +8, IDT +7, HEAL +5 | 16 | -8 | 16 | -15 | 4.0 | 13 | Scent of Blood, Hunter's Moon, Feral Frenzy, Beast Unchained (DMG +1, IDG +8, IDT +2, HEAL +5) | Rending Claws (2) |
| Lycanthropy | Frenzy — Increase Damage Given (Frenzy Assault, Feral Wrath; two self rows) / Taijutsu damage — Moonlit Fury and Feral Wrath (two formula rows) / Sustain — Heal (Frenzy Assault; one static row) | DMG +6, IDG +7, HEAL +5 | 10 | -14 | 20 | -11 | 4.0 | 18 | The Beast Within, Gnashing Fangs, Jaws of the Alpha, Blood on the Wind (DMG +6, IDG +4) | Moonbound Vigor (2) |
| Megumi Kijo | Genjutsu damage — Damage on Phantom Realm Oblivion and Onibaba's Laughter (2 rows) / Control — Decrease Damage Given on Phantom Realm Oblivion (1 row) / Sustain — Heal on Onibaba's Laughter and Increase Heal on Kijo's Benevolence (1 row each) | DMG +6, DDG +10, IH +8, HEAL +5 | 17 | -7 | 18 | -13 | 3.6 | 17 | Hagmother's Welcome, Numbing Lullaby, Cradle of the Kijo, Mountain Hag's Mercy (DMG +1, DDG +10, IH +2, HEAL +4) | Numbing Lullaby (3) |
| Musashi Ken | Bukijutsu tempo — Increase Damage Given (Heiho, Iaido, Iaijutsu; three self rows) / Quick-draw damage — Iaido and Iaijutsu (two formula rows) / Guard — Decrease Damage Taken (Heiho; one row) | DMG +6, IDG +6, DDT +10 | 15 | -9 | 24 | -7 | 4.0 | 22 | Drawn Steel, Reading the Field, Unbroken Guard, Victory in the Sheath (DMG +1, IDG +4, DDT +10) | Unbroken Guard (3) |
| Namikaze | Wind offense — Damage on Cutting Tempest, Tempest Shroud and Wind Step; self Increase Damage Given on Cutting Tempest (and the hidden Soaring Fujin) / Pressure — Afterburn on Tempest Shroud's circle (enemy debuff, ally hazard) / Control — self Decrease Damage Taken on Tempest Shroud; enemy Decrease Damage Given on Wind Step's circle | DMG +5, IDG +5, DDG +10, DDT +10, AB +10 | 19 | -5 | 26 | -5 | 3.25 | 19 | Wind at the Back, Razor Crosswind, Searing Squall, Fanning the Flames (DMG +2, IDG +5, AB +10) | Searing Squall (3) |
| Nature's Blessing | Co-primary — Sustain (Verdant Bastion Heal and Increase Heal) and Wood damage (Nature's Fury, Nature's Curse) / Exposure — Increase Damage Taken (Nature's Fury) / None — absorb and drain on Nature's Curse are unsupported | DMG +6, IDT +7, IH +8, HEAL +5 | 16 | -8 | 18 | -13 | 3.6 | 16 | Thorn and Rot, Ironwood Lash, Old Growth's Wrath, Sap of the Grove (DMG +6, IDT +2, IH +2, HEAL +2) | Stripped Bark (2) |
| Oblivion Seal | Damage (three Shadow attacks) / Increase Damage Taken and Increase Damage Given (Shadowrend exposure, Cursed Beast Form empowerment) / Shadow Surge sustain (Decrease Damage Taken, Lifesteal) | DMG +5, IDG +5, IDT +7, DDT +10, LS +10 | 19 | -5 | 23 | -8 | 3.29 | 17 | Brand of Oblivion, Umbral Claws, Absolute Erasure, Umbral Refuge (DMG +5, IDG +2, IDT +2, DDT +2, LS +2) | Unraveled Wards (2) |
| Primal Radiance | Offense — Fire damage (Fire Style: Beast, Fire Style: Squirrel) and Beast's self Increase Damage Given / Pressure — Afterburn and Increase Damage Taken (Primal Incineration) / Defense — Decrease Damage Taken (Fire Style: Squirrel circle) | DMG +6, IDG +10, IDT +5, DDT +10, AB +10 | 20 | -4 | 21 | -10 | 3.5 | 17 | Hunter's Brand, Smoldering Trail, Pyre of the Hunted, Hide and Fang (DMG +1, IDG +2, IDT +5, DDT +2, AB +10) | Smoldering Trail (3) |
| Reptilian | Increase Damage Given — two stacking 35% rows (Reptile Chimera self, Cool-Blooded Empowerment circle) / Decrease Damage Taken — Reptile Chimera hide (single row, +10 ceiling) / Lifesteal — Cool-Blooded Empowerment feeding (single ally/self row, +10 ceiling) | IDG +7, DDT +10, LS +10 | 17 | -7 | 21 | -10 | 5.25 | 19 | Chimeric Blood, Apex Instinct, Jaws of the Chimera, Hardened Scales (IDG +7, DDT +5, LS +2) | Hardened Scales (3) |
| Sands of Time | Control — Increase Damage Taken (Timeshift, Momentum Shift; two enemy rows) and Decrease Damage Given (Timelapse circle) / Tank — Decrease Damage Taken (Timelapse self row) and Heal (Cellular Regeneration) / Sand damage (Timeshift 40, Eternity Flux 50, Timelapse 40) and the Momentum Shift self Increase Damage Given | DMG +5, IDG +5, DDG +8, IDT +7, DDT +10, HEAL +5 | 19 | -5 | 25 | -6 | 2.78 | 20 | Borrowed Hours, Grinding Sands, Brittle with Age, The Inevitable Hour (DMG +2, IDG +5, IDT +7) | Held in Stasis (3) |
| Sea-King's Blessing | Increase Damage Taken — Crushing Abyss's broad circle exposure and Water Dome's Water-filtered exposure (two rows, +7 ceiling) / Water damage — Sea King's Armor and Crushing Abyss (two formula rows at 38, +6 ceiling) / Decrease Damage Taken — Sea King's Armor's self reduction (one row, +10 ceiling) | DMG +6, IDT +7, DDT +10 | 14 | -10 | 20 | -11 | 4.0 | 18 | Scales of the Deep, Salt in the Wound, Dragged Under, Wrath of the Sea-King (DMG +2, IDT +7, DDT +2) | Deepwater Carapace (3) |
| Shakunetsu Sakura | Scorch area damage on the Hiru-Sakura circles (Sakuragari, Sakura-ame) / Increase Damage Taken exposure (Sakuragari circle, Sakura Dragon Tree) and the Sakura Dragon Tree self Increase Damage Given / Decrease Damage Given suppression (Sakura-ame) and Heal (Sakura Dragon Pearl) | DMG +6, IDG +10, DDG +10, IDT +6, HEAL +5 | 18 | -6 | 22 | -9 | 3.14 | 18 | Ember Dragon's Roots, Branded by Petals, Scorching Hanami, Falling Ember Petals (DMG +1, IDG +4, DDG +2, IDT +6, HEAL +2) | Kindled Boughs (3) |
| Shinrai Ou | Damage (Storm burst on all four attacks, +6 ceiling) / Increase Damage Taken (Izanagi's Hammer exposure, +10 ceiling) and Reflect (Indra's Storm Cloak, +10 ceiling) / Increase Damage Given (glue across routes, +5 ceiling on a doubled-row cast) | DMG +6, IDG +5, IDT +10, REF +10 | 18 | -6 | 34 | +3 | 3.78 | 31 | Mandate of Thunder, Vajra Tempering, Wrath of the Thunder King, Raiment of Storms (DMG +6, IDG +2, IDT +2, REF +2) | Lightning Rod (3) |
| Shinseina Ki | Wood damage — Exploding Wood Serpent, Guardian's Grove, Eternal Forest (three formula rows, +6 ceiling) / Increase Damage Given — Forest Wisdom's two self rows on one 40 AP cast (+7 ceiling) / Increase Damage Taken — Guardian's Grove's area exposure (one row, +10 ceiling) | DMG +6, IDG +7, IDT +10 | 14 | -10 | 26 | -5 | 4.33 | 20 | Hallowed Seed, Fangs of Heartwood, The Forest Devours, Rooted in Wisdom (DMG +6, IDG +4) | Grasping Roots (2) |
| Shiroi Youso | Elemental amplification (self Increase Damage Given on Fire Release and Wind Release's circle; enemy Increase Damage Taken on Fire Release and Element Divine's area) / Burst and burn (Damage on Lightning Release 40 and Element Divine 45; Afterburn on the same two casts, 35% and 30%) / Defensive control (ground Decrease Damage Taken on Wind Release and Earth Release; static Heal on Water Release) | DMG +6, IDG +5, IDT +6, DDT +7, AB +7, HEAL +5 | 17 | -7 | 32 | +1 | 2.91 | 26 | Fivefold Kindling, Charred Current, White Immolation, Bedrock and Tide (IDG +2, IDT +4, DDT +2, AB +7, HEAL +2) | Tidal Mending (3) |
| Suragu | Infernal Stream sustain and burst (Lifesteal +10 ceiling, Damage +5 on two Lava rows) / Decrease Damage Taken on Lava Wave (+10 ceiling) and Afterburn pressure on Eruption Strike (+10 ceiling) / Increase Damage Given (Lava Wave) and Increase Damage Taken (Blow of Devastation) as glue, +5 each | DMG +5, IDG +5, IDT +5, DDT +10, AB +10, LS +10 | 24 | +0 | 24 | -7 | 3.43 | 18 | Magma Vein, Clinging Slag, The Mountain Wakes, Cooling Crust (IDG +5, IDT +5, DDT +2, AB +10, LS +2) | Clinging Slag (3) |
| Tenohira Musei | Yin-Yang offense (Damage on three casts; self Increase Damage Given on Silent Rift and Yin-Yang Cascade) / Enemy exposure (Increase Damage Taken on Moonlit Inferno and Yin-Yang Cascade) / Suppression (Decrease Damage Given on Moonlit Inferno) | DMG +5, IDG +7, DDG +10, IDT +7 | 17 | -7 | 28 | -3 | 3.5 | 22 | Waxing Crescent, Waning Crescent, Bared to the Moon, Stillness Breaks (DMG +2, IDG +3, DDG +2, IDT +7) | Hushed Inferno (3) |
| Terra Nova | Damage (Earth attacks: Earthen Fortitude, Terra Spire) / Decrease Damage Taken (Earth Wall fortification) / Decrease Damage Given (Earthen Fortitude suppression) and Increase Damage Given (Earth Wall, Earth hits only) | DMG +6, IDG +10, DDG +10, DDT +10 | 17 | -7 | 18 | -13 | 3.6 | 17 | Fault Line, Bedrock Stance, Rampart Discipline, Unmoved Mountain (DMG +1, IDG +4, DDG +2, DDT +10) | Burden of Stone (3) |
| Tetsugan | Damage (seven Metal weapon strikes, +5 ceiling) / Decrease Damage Taken and Increase Damage Given (the Middle Guard Stance / Inner Peace / Pivoting Fortress stance buffs) / Increase Damage Taken and Afterburn exposure (Phantom Slash, Equilibrium Guard Strike, Vacuum Fan, Crimson Thrust); Reflect and Decrease Damage Given counter-play (Harmonious Slash, Tranquil Guard, Vacuum Fan) | DMG +5, IDG +5, DDG +5, IDT +5, DDT +6, AB +10, REF +8 | 21 | -3 | 57 | +26 | 2.85 | 39 | Tempered Stance, Eye of Iron, Honed Edge, One Cut Decides (DMG +5, IDG +2, DDG +2, IDT +2, DDT +2) | Resonant Parry (3) |
| Vaporia | Boil damage — Damage on three Taijutsu formula rows (Drowning Strike 40, Surfing Strike 45, Scorch Break 40) / Liquid Ember Shell window — Afterburn (enemy) with Increase Damage Given and Lifesteal (self) on one 40 AP cast / Steam body — Decrease Damage Taken (Surfing Strike), Reflect (Scorch Break), Heal (Azure Dragon Palm); Drowning Strike's exposure as glue | DMG +5, IDG +5, IDT +5, DDT +5, AB +10, LS +8, REF +8, HEAL +5 | 24 | +0 | 26 | -5 | 2.6 | 18 | Rising Steam, Geyser Fist, Blistering Mist, Boiling Point (DMG +2, IDG +5, IDT +5, AB +10) | Blistering Mist (3) |

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
| Ancient Tailed Demon | Howl of Annihilation (Roar burst) | 01, 02, 03, 06 | 16 | 16 | DMG +6, IDG +2, IDT +4, DDT +2, AB +2 |
| Ancient Tailed Demon | Consuming Malice (Burn pressure) | 01, 04, 05, 06 | 19 | 19 | IDG +2, IDT +5, DDT +2, AB +10 |
| Ancient Tailed Demon | Unyielding Husk (Fortified) | 01, 06, 07, 08 | 18 | 18 | IDG +4, IDT +2, DDT +10, AB +2 |
| Ancient Tailed Demon | Primordial Rampage (Empowered) | 01, 06, 09, 10 | 18 | 18 | IDG +10, IDT +2, DDT +4, AB +2 |
| Arashima | Reaper's Harvest (Sustain) | 01, 04, 05, 06 | 19 | 19 | IDG +5, DDG +2, DDT +2, LS +10 |
| Arashima | Sundered Sky (Burst) | 01, 02, 03, 06 | 13 | 18 | DMG +5, IDG +2, DDG +2, DDT +2, LS +2 |
| Arashima | Unbroken Horizon (Fortress) | 01, 06, 07, 08 | 19 | 19 | IDG +5, DDG +2, DDT +10, LS +2 |
| Arashima | Silence After Thunder (Suppression) | 01, 06, 09, 10 | 20 | 20 | IDG +2, DDG +10, DDT +4, LS +4 |
| Bakuhatsu | Ground Zero (Burst) | 01, 02, 03, 04 | 12 | 27 | DMG +5, IDG +5, IDT +2 |
| Bakuhatsu | Chain Reaction (Pressure) | 05, 08, 09, 01 | 19 | 21 | IDG +2, IDT +5, DDT +2, AB +10 |
| Bakuhatsu | Siege Battery (Fortified) | 05, 06, 07, 01 | 18 | 22 | IDG +4, IDT +2, DDT +10, AB +2 |
| Blood-Enchanted Eyes | Rite of Exsanguination (Burst) | 01, 02, 03, 06 | 14 | 42 | DMG +6, IDG +2, DDG +2, IDT +2, DDT +2 |
| Blood-Enchanted Eyes | Red Pestilence (Plague) | 01, 04, 05, 06 | 21 | 37 | IDG +2, DDG +2, IDT +5, DDT +2, AB +10 |
| Blood-Enchanted Eyes | Feast of the Fallen (Sustain) | 01, 06, 09, 10 | 19 | 32 | IDG +5, DDG +2, IDT +2, DDT +2, LS +8 |
| Blood-Enchanted Eyes | Deathless Vitality (Fortress) | 01, 06, 07, 08 | 17 | 36 | IDG +2, DDG +5, IDT +2, DDT +8 |
| Blue Blade Eyes | Stroke That Splits Stone Burst (Burst) | 01, 02, 03, 06 | 13 | 45 | DMG +5, IDG +2, DDG +2, IDT +2, DDT +2 |
| Blue Blade Eyes | Numb to the Marrow Suppression (Suppression) | 01, 04, 05, 06 | 18 | 39 | IDG +5, DDG +9, IDT +2, DDT +2 |
| Blue Blade Eyes | Glacier Does Not Yield Bulwark (Bulwark) | 01, 06, 07, 08 | 17 | 41 | IDG +2, DDG +2, IDT +5, DDT +8 |
| Blue Blade Eyes | Winter Takes Its Due Drain (Drain) | 06, 07, 09, 10 | 18 | 33 | IDT +5, DDT +5, LS +8 |
| Cosmic Ascendant | Supernova Unbound (Burst) | 01, 02, 03, 06 | 17 | 26 | DMG +6, IDG +2, DDG +2, IDT +5, DDT +2 |
| Cosmic Ascendant | Light of Dead Stars (Burn pressure) | 01, 04, 05, 06 | 21 | 30 | IDG +2, DDG +2, IDT +5, DDT +2, AB +10 |
| Cosmic Ascendant | Heart of the Singularity (Fortress) | 01, 06, 07, 08 | 16 | 32 | IDG +5, DDG +2, IDT +2, DDT +7 |
| Cosmic Ascendant | Hunger of the Void (Sustain) | 01, 06, 09, 10 | 19 | 25 | IDG +2, DDG +5, IDT +2, DDT +2, LS +8 |
| Crystal Essence | Splintered Mountain Heart (Burst) | 01, 02, 03, 04 | 11 | 25 | DMG +5, IDG +2, IDT +4 |
| Crystal Essence | Break Along the Flaw (Exposure) | 01, 04, 05, 02 | 14 | 25 | DMG +2, IDG +5, IDT +7 |
| Crystal Essence | Adamant Core (Bastion) | 06, 07, 08, 01 | 19 | 21 | IDG +5, IDT +2, DDT +10, REF +2 |
| Crystal Essence | Entombed in Crystal (Reprisal) | 06, 09, 10, 01 | 19 | 21 | IDG +5, IDT +2, DDT +2, REF +10 |
| Dai Kenja | Breaking Point (Burst) | 01, 02, 03, 06 | 13 | 15 | DMG +6, IDG +5, DDG +2 |
| Dai Kenja | Boundless Reservoir (Amplifier) | 01, 04, 05, 06 | 12 | 14 | IDG +10, DDG +2 |
| Dai Kenja | Edict of Silence (Suppression) | 01, 06, 07, 08 | 11 | 19 | IDG +3, DDG +8 |
| Dai Kenja | Shattered Vessel (Exposure) | 06, 07, 09, 10 | 12 | 24 | DDG +7, IDT +5 |
| Godstorm Eclipse | Total Eclipse (Burst) | 01, 02, 03, 06 | 13 | 45 | DMG +5, IDG +2, IDT +2, DDT +2, LS +2 |
| Godstorm Eclipse | Lingering Corona (Burn pressure) | 01, 04, 05, 06 | 21 | 39 | IDG +2, IDT +5, DDT +2, AB +10, LS +2 |
| Godstorm Eclipse | Pillar of Heaven (Fortified off.) | 01, 06, 07, 08 | 16 | 42 | IDG +5, IDT +2, DDT +7, LS +2 |
| Godstorm Eclipse | Eater of Suns (Sustain) | 01, 06, 09, 10 | 20 | 38 | IDG +4, IDT +2, DDT +2, AB +2, LS +10 |
| Ha Yanagi | Grave Willow's Hush (Suppression) | 01, 02, 03, 06 | 11 | 19 | IDG +3, DDG +8 |
| Ha Yanagi | Hollow at the Heart (Exposure) | 01, 02, 04, 05 | 14 | 20 | DDG +6, IDT +8 |
| Ha Yanagi | Nightmare in Bloom (Burst) | 06, 07, 08, 09 | 13 | 18 | DMG +5, IDG +8 |
| Ha Yanagi | Thousand-Leaf Dream (Amplifier) | 06, 09, 10, 01 | 12 | 14 | IDG +10, DDG +2 |
| Heavenly Sonata | Fortissimo Finale (Burst) | 01, 02, 03, 06 | 13 | 23 | DMG +5, IDG +2, DDG +2, IDT +2, DDT +2 |
| Heavenly Sonata | Prelude to Ruin (Exposure) | 01, 04, 05, 06 | 16 | 16 | IDG +5, DDG +2, IDT +7, DDT +2 |
| Heavenly Sonata | Celestial Sanctum (Fortress) | 06, 07, 08, 09 | 17 | 17 | DDG +7, DDT +10 |
| Heavenly Sonata | Final Rest (Suppression) | 01, 06, 09, 10 | 18 | 18 | IDG +2, DDG +10, IDT +2, DDT +4 |
| Houkyuken | Starfall Hammer (Burst) | 01, 02, 03, 06 | 13 | 32 | DMG +5, IDG +2, IDT +2, DDT +2, REF +2 |
| Houkyuken | Inexorable Pull (Exposure) | 01, 04, 05, 06 | 15 | 26 | IDG +4, IDT +7, DDT +2, REF +2 |
| Houkyuken | Absolute Alignment (Bulwark) | 06, 07, 08, 01 | 18 | 24 | IDG +4, IDT +2, DDT +10, REF +2 |
| Houkyuken | Violent Repulsion (Counterstrike) | 06, 09, 10, 07 | 17 | 17 | DDT +7, REF +10 |
| Itojinsei | Severing Lattice (Burst) | 01, 02, 03, 06 | 12 | 32 | DMG +5, IDG +2, DDG +3, IDT +2 |
| Itojinsei | Weaver Ascendant (Amplifier) | 01, 04, 05, 06 | 14 | 24 | IDG +7, DDG +3, IDT +4 |
| Itojinsei | Iron Cocoon (Suppression) | 06, 07, 08, 01 | 15 | 26 | IDG +2, DDG +9, IDT +4 |
| Itojinsei | Galvanic Marionette (Exposure) | 06, 09, 10, 01 | 17 | 24 | IDG +2, DDG +5, IDT +10 |
| Loup-Garou | Killing Bite (Burst) | 01, 02, 03, 06 | 12 | 12 | DMG +6, IDG +2, IDT +2, HEAL +2 |
| Loup-Garou | The Pack Closes (Exposure) | 01, 04, 05, 06 | 15 | 15 | DMG +1, IDG +5, IDT +7, HEAL +2 |
| Loup-Garou | Beast Unchained (Frenzy) | 01, 06, 07, 08 | 16 | 16 | DMG +1, IDG +8, IDT +2, HEAL +5 |
| Lycanthropy | Jaws of the Alpha (Burst) | 01, 02, 03, 06 | 10 | 18 | DMG +6, IDG +2, HEAL +2 |
| Lycanthropy | Red Moon Rising (Frenzy) | 01, 04, 05, 06 | 10 | 18 | DMG +1, IDG +7, HEAL +2 |
| Lycanthropy | Lick the Wound (Sustain) | 01, 04, 06, 07 | 10 | 15 | DMG +1, IDG +4, HEAL +5 |
| Megumi Kijo | Appetite of Oblivion (Burst) | 01, 02, 03, 06 | 12 | 18 | DMG +6, DDG +2, IH +2, HEAL +2 |
| Megumi Kijo | Cradle of the Kijo (Suppression) | 01, 04, 05, 06 | 17 | 18 | DMG +1, DDG +10, IH +2, HEAL +4 |
| Megumi Kijo | Laughter That Mends (Sustain) | 01, 06, 07, 08 | 16 | 17 | DMG +1, DDG +2, IH +8, HEAL +5 |
| Musashi Ken | Cut of No Return (Burst) | 01, 02, 03, 06 | 10 | 20 | DMG +6, IDG +2, DDT +2 |
| Musashi Ken | Two Heavens as One (Tempo) | 01, 04, 05, 06 | 11 | 24 | DMG +1, IDG +6, DDT +4 |
| Musashi Ken | Victory in the Sheath (Guard) | 01, 06, 07, 08 | 15 | 24 | DMG +1, IDG +4, DDT +10 |
| Namikaze | Cleaving Cyclone (Burst) | 01, 02, 03, 06 | 12 | 25 | DMG +5, IDG +3, DDG +2, DDT +2 |
| Namikaze | Fanning the Flames (Burn pressure) | 01, 04, 05, 06 | 19 | 24 | IDG +5, DDG +2, DDT +2, AB +10 |
| Namikaze | Heart of the Tempest (Fortress) | 06, 07, 08, 01 | 17 | 22 | IDG +5, DDG +2, DDT +10 |
| Namikaze | Dead Calm (Suppression) | 06, 09, 10, 07 | 16 | 18 | DMG +1, DDG +10, DDT +5 |
| Nature's Blessing | Old Growth's Wrath (Burst) | 01, 02, 03, 06 | 12 | 18 | DMG +6, IDT +2, IH +2, HEAL +2 |
| Nature's Blessing | Blight and Harvest (Exposure) | 01, 04, 05, 06 | 15 | 16 | DMG +1, IDT +7, IH +5, HEAL +2 |
| Nature's Blessing | Everbloom Sanctuary (Sustain) | 01, 06, 07, 08 | 16 | 17 | DMG +1, IDT +2, IH +8, HEAL +5 |
| Oblivion Seal | Absolute Erasure (Burst) | 01, 02, 03, 06 | 13 | 23 | DMG +5, IDG +2, IDT +2, DDT +2, LS +2 |
| Oblivion Seal | Writ of Oblivion (Exposure) | 01, 04, 05, 06 | 16 | 16 | IDG +5, IDT +7, DDT +2, LS +2 |
| Oblivion Seal | Sealed Against Ruin (Fortress) | 01, 06, 07, 08 | 19 | 19 | IDG +5, IDT +2, DDT +10, LS +2 |
| Oblivion Seal | Maw of Oblivion (Sustain) | 01, 06, 09, 10 | 18 | 18 | IDG +2, IDT +2, DDT +4, LS +10 |
| Primal Radiance | Apex Conflagration (Burst) | 01, 02, 03, 06 | 12 | 18 | DMG +6, IDG +2, IDT +2, DDT +2 |
| Primal Radiance | Pyre of the Hunted (Burn pressure) | 01, 04, 05, 06 | 20 | 21 | DMG +1, IDG +2, IDT +5, DDT +2, AB +10 |
| Primal Radiance | Den of Embers (Fortified) | 01, 06, 07, 08 | 17 | 18 | DMG +1, IDG +4, IDT +2, DDT +10 |
| Primal Radiance | Primal Rampage (Buff window) | 01, 06, 09, 10 | 17 | 18 | DMG +1, IDG +10, IDT +2, DDT +4 |
| Reptilian | Jaws of the Chimera (Predation) | 01, 02, 03, 04 | 14 | 21 | IDG +7, DDT +5, LS +2 |
| Reptilian | Basilisk Carapace (Fortress) | 01, 04, 05, 06 | 17 | 19 | IDG +2, DDT +10, LS +5 |
| Reptilian | Feast of Scales (Pack sustain) | 01, 06, 07, 08 | 16 | 18 | IDG +2, DDT +4, LS +10 |
| Sands of Time | Erosion of Eternity (Burst) | 01, 02, 03, 06 | 13 | 25 | DMG +5, IDG +2, IDT +2, DDT +2, HEAL +2 |
| Sands of Time | The Inevitable Hour (Exposure) | 01, 04, 05, 06 | 16 | 23 | IDG +5, IDT +7, DDT +2, HEAL +2 |
| Sands of Time | Timeless Bastion (Fortress) | 01, 06, 07, 08 | 19 | 21 | IDG +2, IDT +2, DDT +10, HEAL +5 |
| Sands of Time | Stilled Hourglass (Suppression) | 01, 06, 09, 10 | 18 | 20 | IDG +2, DDG +8, IDT +2, DDT +4, HEAL +2 |
| Sea-King's Blessing | Weight of the Trench (Burst) | 01, 02, 03, 06 | 10 | 18 | DMG +6, IDT +2, DDT +2 |
| Sea-King's Blessing | Hull of the Leviathan (Bulwark) | 01, 04, 05, 06 | 14 | 18 | DMG +2, IDT +2, DDT +10 |
| Sea-King's Blessing | Wrath of the Sea-King (Exposure) | 01, 06, 07, 08 | 11 | 20 | DMG +2, IDT +7, DDT +2 |
| Shakunetsu Sakura | Conflagration in Bloom (Burst) | 01, 06, 07, 08 | 12 | 18 | DMG +6, IDG +2, DDG +2, HEAL +2 |
| Shakunetsu Sakura | Scorching Hanami (Exposure) | 01, 04, 05, 06 | 15 | 22 | DMG +1, IDG +4, DDG +2, IDT +6, HEAL +2 |
| Shakunetsu Sakura | Dragon in Full Blossom (Amplifier) | 01, 02, 03, 04 | 17 | 19 | IDG +10, IDT +2, HEAL +5 |
| Shakunetsu Sakura | Deluge of Burning Petals (Suppression) | 06, 07, 09, 10 | 14 | 18 | DMG +4, DDG +10 |
| Shinrai Ou | Wrath of the Thunder King (Burst) | 01, 02, 03, 06 | 12 | 34 | DMG +6, IDG +2, IDT +2, REF +2 |
| Shinrai Ou | Judgement from Above (Exposure) | 01, 02, 04, 05 | 17 | 33 | DMG +2, IDG +5, IDT +10 |
| Shinrai Ou | Thunder Answers Thunder (Bulwark) | 01, 06, 07, 08 | 18 | 31 | DMG +1, IDG +5, IDT +2, REF +10 |
| Shinseina Ki | The Forest Devours (Burst) | 01, 02, 03, 06 | 10 | 24 | DMG +6, IDG +2, IDT +2 |
| Shinseina Ki | Heartwood Awakened (Amplification) | 01, 04, 05, 06 | 10 | 19 | DMG +1, IDG +7, IDT +2 |
| Shinseina Ki | Judgement of the Grove (Exposure) | 01, 06, 07, 08 | 14 | 20 | DMG +2, IDG +2, IDT +10 |
| Shiroi Youso | Divine Convergence (Burst) | 01, 02, 03, 06 | 14 | 26 | DMG +6, IDG +2, IDT +2, DDT +2, HEAL +2 |
| Shiroi Youso | White Immolation (Burn pressure) | 01, 04, 05, 06 | 17 | 32 | IDG +2, IDT +4, DDT +2, AB +7, HEAL +2 |
| Shiroi Youso | Eye of the Tempest (Fortified) | 01, 06, 07, 08 | 16 | 30 | IDG +5, IDT +2, DDT +7, HEAL +2 |
| Shiroi Youso | Pull of the Undertow (Control) | 01, 06, 09, 10 | 17 | 29 | IDG +2, IDT +6, DDT +4, HEAL +5 |
| Suragu | Pyroclastic Surge (Burst) | 01, 02, 03, 06 | 15 | 20 | DMG +5, IDG +2, IDT +2, DDT +2, LS +4 |
| Suragu | The Mountain Wakes (Burn pressure) | 01, 04, 05, 06 | 24 | 24 | IDG +5, IDT +5, DDT +2, AB +10, LS +2 |
| Suragu | Heart of the Caldera (Fortified off.) | 01, 06, 07, 08 | 19 | 19 | IDG +5, IDT +2, DDT +10, LS +2 |
| Suragu | Unquenchable Furnace (Sustain) | 01, 06, 09, 10 | 18 | 18 | IDG +2, IDT +2, DDT +4, LS +10 |
| Tenohira Musei | Deafening Silence (Burst) | 01, 02, 03, 06 | 12 | 27 | DMG +5, IDG +3, DDG +2, IDT +2 |
| Tenohira Musei | Tipping the Balance (Amplifier) | 01, 04, 05, 06 | 13 | 22 | IDG +7, DDG +4, IDT +2 |
| Tenohira Musei | Eclipse in Hand (Suppression) | 06, 07, 08, 01 | 17 | 24 | IDG +5, DDG +10, IDT +2 |
| Tenohira Musei | Stillness Breaks (Exposure) | 06, 09, 10, 07 | 14 | 25 | DMG +2, DDG +5, IDT +7 |
| Terra Nova | Continental Rift (Burst) | 01, 02, 03, 06 | 12 | 18 | DMG +6, IDG +2, DDG +2, DDT +2 |
| Terra Nova | Pressure of Ages (Suppression) | 01, 04, 05, 06 | 16 | 18 | DMG +2, IDG +2, DDG +10, DDT +2 |
| Terra Nova | Unmoved Mountain (Fortified) | 01, 06, 07, 08 | 17 | 18 | DMG +1, IDG +4, DDG +2, DDT +10 |
| Terra Nova | Landslide Momentum (Amplify) | 01, 06, 09, 10 | 17 | 18 | DMG +1, IDG +10, DDG +2, DDT +4 |
| Tetsugan | One Cut Decides (Burst) | 01, 06, 07, 08 | 13 | 57 | DMG +5, IDG +2, DDG +2, IDT +2, DDT +2 |
| Tetsugan | Hammer and Anvil (Fortified) | 01, 02, 03, 06 | 15 | 43 | IDG +5, DDG +2, IDT +2, DDT +6 |
| Tetsugan | Branding Iron (Burn pressure) | 01, 06, 09, 10 | 21 | 41 | IDG +2, DDG +2, IDT +5, DDT +2, AB +10 |
| Tetsugan | Every Blow Returned (Counter) | 01, 04, 05, 06 | 19 | 36 | IDG +2, DDG +5, IDT +2, DDT +2, REF +8 |
| Vaporia | Caldera Burst (Burst) | 01, 02, 03, 06 | 13 | 23 | DMG +5, IDG +2, IDT +2, DDT +2, HEAL +2 |
| Vaporia | Boiling Point (Pressure) | 01, 04, 05, 06 | 24 | 24 | IDG +5, IDT +5, DDT +2, AB +10, HEAL +2 |
| Vaporia | Dew of the Dragon (Sustain) | 01, 06, 07, 08 | 19 | 19 | IDG +2, IDT +2, DDT +2, LS +8, HEAL +5 |
| Vaporia | Wall of Steam (Bulwark) | 06, 07, 09, 10 | 18 | 18 | DDT +5, LS +3, REF +8, HEAL +2 |

## Coverage gaps and exceptions

- **Aerathiel:** classification label shared with 2 other census bloodline(s)
- **Arashima:** classification label shared with 3 other census bloodline(s)
- **Bakuhatsu:** narrow-kit exception: Nine nodes rather than ten. The kit's five supported tags (Damage 3 rows, Increase Damage Given 2, Increase Damage Taken 1, Decrease Damage Taken 1, Afterburn 1) give three distinct Advanced routes (burst, pressure, fortified). The only unused candidate for a fourth capstone is Increase Damage Taken, which sits on the same Charge 4 Explosion cast, target and two-round window as the Afterburn route; a second capstone there would duplicate the pressure route rather than add a choice. Powder Keg is kept as a leaf Hidden Art so the burst route has an all-in fourth purchase and the charge buffs have an owner. Three complete builds are distinct.; classification label shared with 1 other census bloodline(s)
- **Blood-Enchanted Eyes:** classification label shared with 13 other census bloodline(s)
- **Blue Blade Eyes:** classification label shared with 7 other census bloodline(s)
- **Crystal Essence:** classification label shared with 1 other census bloodline(s)
- **Dai Kenja:** 1 adverse supported row(s) in kit
- **Godstorm Eclipse:** classification label shared with 16 other census bloodline(s)
- **Heavenly Sonata:** classification label shared with 8 other census bloodline(s)
- **Houkyuken:** classification label shared with 1 other census bloodline(s)
- **Itojinsei:** classification label shared with 1 other census bloodline(s)
- **Loup-Garou:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on four rows, one row each (Damage, Increase Damage Given and Heal on Nature's Hunter; Increase Damage Taken on Life reaver); the Wolf Companion summon and Life reaver's absorb are unsupported. The enemy-facing root (Scent of Blood) forks into a damage route and an exposure route; the self-facing root (Hunter's Moon) is a single Foundation → Hidden → Advanced chain because its two rows share one cast and Heal is exhausted at +5 (the guardrail) after two purchases, so a second sustain Hidden Art or capstone would have to breach it or carry only Increase Damage Given, which would duplicate Feral Frenzy and open a second path to the IDG maximum. A damage or exposure branch under Hunter's Moon is structurally legal but would twin Rending Claws or Run to Ground on the same single rows, so it is declined. Three distinct complete builds (Burst, Exposure, Frenzy) exist; Burst and Exposure each have two fourth-purchase choices, Frenzy's fourth purchase is always Scent of Blood. 8 legal full-budget allocations, every node in a non-dominated one.
- **Lycanthropy:** narrow-kit exception: Seven nodes and two Advanced Arts rather than ten and four. The kit has three supported tags on five rows (Damage x2, Increase Damage Given x2, Heal x1). The Beast Within forks into a damage route (Gnashing Fangs → Jaws of the Alpha, +6 at the two-row Damage guardrail) and a frenzy route (Blood on the Wind → Red Moon Rising, +7 on two self rows that can stack). Heal is one static row with a +5 guardrail, so it supports only a Foundation → Hidden Art side chain (Moonbound Vigor → Lick the Wound, 420 → 450 HP); a third Advanced Art would have to be a Heal capstone worth +10 to +20 HP per cast (filler) or a duplicate Damage / Increase Damage Given capstone reached through heal purchases, and Draft 1 declines both so that Jaws of the Alpha and Red Moon Rising stay the only ways to +6 Damage and +7 Increase Damage Given. Because the sustain side has two nodes, every legal 4 BP build contains The Beast Within; on five rows there is no second four-node subtree that would avoid that without filler. Three distinct complete builds exist (Burst, Frenzy, and a Sustain hybrid without an Advanced Art); Burst and Frenzy each have two fourth-purchase choices and the sustain hybrid has two forms.
- **Megumi Kijo:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on five rows (Damage x2, Decrease Damage Given x1, Increase Heal x1, Heal x1). The enemy-facing root (Hagmother's Welcome) forks into a damage route and a suppression route; the self-facing root (Mountain Hag's Mercy) is a single Foundation → Hidden → Advanced chain. A fourth route would have to split Heal from Increase Heal: a Heal-led Hidden Art under Mercy (+3) would already sit at the +5 guardrail with the Foundation's +2, so it could carry no capstone, and an Increase Heal-led second route would duplicate Nursed by Demon Hands. A Damage or Decrease Damage Given Hidden Art under Mercy is structurally legal (any two Advanced Arts would still cost 5 BP or more) but would duplicate the Welcome routes and open a second path to the +6 Damage / +10 DDG ceilings, so it is declined by choice. Three distinct complete builds exist (Burst, Suppression, Sustain); Burst and Suppression each have two fourth-purchase choices, and Sustain's fourth purchase is always Hagmother's Welcome (01,06,07,08 is legal and non-dominated).
- **Musashi Ken:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on six rows (Increase Damage Given x3, Damage x2, Decrease Damage Taken x1); Iaijutsu's move row is unsupported. Drawn Steel forks into a damage route (Single Stroke → Cut of No Return, +6 with Reading the Field, the two-row Damage guardrail) and a tempo route (Second Sword → Two Heavens as One, +6 on three self rows that can stack). Decrease Damage Taken is one row, so Reading the Field runs a single chain (Unbroken Guard → Victory in the Sheath, 35→45%, the Taiyo Kami +10 shape); a fourth Advanced Art would need a second branch under Reading the Field that twins Single Stroke or Second Sword on the same rows, or a guard capstone past +10, and Draft 1 declines both so that each route is the only way to its tag maximum. Because the guard side has three nodes, every legal 4 BP build contains Drawn Steel; a mirrored layout only moves the universal node to the other root. Three distinct complete builds exist (Burst, Tempo, Guard); Burst and Tempo each have two fourth-purchase choices, Guard's fourth purchase is always Drawn Steel. 8 legal full allocations, 7 non-dominated, every node in at least one.
- **Namikaze:** classification label shared with 28 other census bloodline(s)
- **Nature's Blessing:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on five rows (Damage x2, Increase Damage Taken x1, Increase Heal x1, Heal x1). The enemy-facing root (Thorn and Rot) forks into a damage route and an exposure route; the self-facing root (Sap of the Grove) is a single Foundation → Hidden → Advanced chain. A second sustain Hidden Art or capstone under Sap of the Grove would breach the +5 Heal / +10 Increase Heal guardrails in a full build. A damage or exposure Hidden Art or capstone under Sap of the Grove is structurally possible (any two Advanced Arts would still cost at least 5 BP) but would duplicate the Thorn and Rot routes and open a second path to the Damage and Increase Damage Taken ceilings; the design declines that by choice so that Old Growth's Wrath and Blight and Harvest remain the only ways to +6 Damage and +7 IDT. Draft 1's Thorned Bloom (+2 Damage under Sap of the Grove, an exact twin of Ironwood Lash whose builds tied Ironwood Lash builds on every bonus vector) was removed for that reason. Three distinct complete builds (Burst, Exposure, Sustain) exist; Burst and Exposure each have two fourth-purchase choices, and Sustain's fourth purchase is always Thorn and Rot (06,07,08 plus 01 is legal and non-dominated).; classification label shared with 1 other census bloodline(s)
- **Oblivion Seal:** classification label shared with 13 other census bloodline(s)
- **Primal Radiance:** classification label shared with 29 other census bloodline(s)
- **Reptilian:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on four rows (Increase Damage Given x2 on Reptile Chimera and Cool-Blooded Empowerment; Decrease Damage Taken x1 on Reptile Chimera; Lifesteal x1 on Cool-Blooded Empowerment); Summoning: Reptile Zoo and its injected Reptile King carry only summon, injectjutsus and visual rows. The self-facing root (Chimeric Blood) forks into an Increase Damage Given route and a Decrease Damage Taken route; the circle-facing root (Blood of the Brood) is a single Foundation → Hidden → Advanced lifesteal chain. A fourth route would have to repeat one of the three tags: a second IDG Hidden Art under Blood of the Brood would twin Apex Instinct and open a second path past the +7 two-row ceiling, and a second DDT or Lifesteal chain would breach the +10 single-row guardrail in a full build or duplicate an existing route on the same single row, so it is declined. Three distinct complete builds (Predation, Fortress, Pack sustain) exist; Predation and Fortress each have two fourth-purchase choices, Pack sustain's fourth purchase is always Chimeric Blood. 8 legal full-budget allocations, all 8 non-dominated.
- **Sea-King's Blessing:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on five rows (Damage x2, Increase Damage Taken x2, Decrease Damage Taken x1), so it supports exactly three routes: Scales of the Deep forks into a Water damage route (Grip of the Riptide → Weight of the Trench, +6 at the Damage guardrail) and an Armor route (Deepwater Carapace → Hull of the Leviathan, +10 on the single reduction row); Salt in the Wound → Dragged Under → Wrath of the Sea-King is a single chain on the kit's two enemy debuffs (+7, the two-row ceiling). A fourth route needs a fourth tag the kit does not have (absorb and shield are not potency targets). The consequence is that Scales of the Deep is in every legal full build and the exposure route's fourth purchase is always Scales of the Deep, while Burst and Bulwark each have two fourth-purchase choices. Three distinct complete builds exist, one per Advanced Art.; classification label shared with 23 other census bloodline(s)
- **Shakunetsu Sakura:** classification label shared with 1 other census bloodline(s)
- **Shinrai Ou:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has four supported tags on nine rows (Damage x4, Increase Damage Given x3, Increase Damage Taken x1, Reflect x1). The enemy-facing root (Mandate of Thunder) forks into a damage route and an exposure route; the self-facing root (Raiment of Storms) is a single Foundation -> Hidden -> Advanced chain on Reflect. Increase Damage Given is the only tag left for a fourth route, and it is deliberately not given one: two of its three rows sit on the same 40 AP Storm Cloak cast and the bloodline passive multiplies it again, so a dedicated route would either push IDG past the +5 that Taiyo Kami's doubled-row Celestial Ignition tolerates, or need a +3-primary capstone that only mirrors the Reflect capstone's secondary. A second Hidden Art under Raiment of Storms was also rejected: a +2 IDG or +2 IDT support node is dominated by Mandate of Thunder as the bulwark's fourth purchase, and a +2 Damage node would be a twin of Vajra Tempering opening a second path to the +6 Damage ceiling without an Advanced Art. The consequence is that the bulwark route's fourth purchase is always Mandate of Thunder (06, 07, 08 plus 01 is legal and non-dominated), while Burst and Exposure each have two fourth-purchase choices. Three distinct complete builds exist.; classification label shared with 3 other census bloodline(s)
- **Shinseina Ki:** narrow-kit exception: Eight nodes and three Advanced Arts rather than ten and four. The kit has three supported tags on six rows (Damage x3, Increase Damage Given x2, Increase Damage Taken x1), so it supports exactly three routes: Hallowed Seed forks into a Wood damage route (Fangs of Heartwood → The Forest Devours, +6 at the Damage guardrail) and a Forest Wisdom route (Rooted in Wisdom → Heartwood Awakened, +7 on two self rows that are always up together); Grasping Roots → Rootbound Prey → Judgement of the Grove is a single chain on the kit's only enemy debuff. A fourth route would need a fourth tag the kit does not have. A second Hidden Art under Grasping Roots was rejected: a +2 Damage node is a twin of Fangs of Heartwood (identical bonus totals for 01,06,07,09 and 01,02,06,07), and a +2 IDG or +2 IDT node is dominated by Hallowed Seed or Rootbound Prey as a fourth purchase. The consequence is that Hallowed Seed is in every legal full build and the exposure route's fourth purchase is always Hallowed Seed, while Burst and Amplification each have two fourth-purchase choices. Three distinct complete builds exist, one per Advanced Art.; classification label shared with 1 other census bloodline(s)
- **Shiroi Youso:** classification label shared with 34 other census bloodline(s)
- **Suragu:** classification label shared with 1 other census bloodline(s)
- **Tenohira Musei:** classification label shared with 8 other census bloodline(s)
- **Terra Nova:** classification label shared with 23 other census bloodline(s)

## Outliers by per-row intensity (reference 3.44)

- Above 125% of the reference: Reptilian (5.25), Shinseina Ki (4.33)
- Below 75% of the reference: none

Reading guide: a higher row-weighted total means the same static additions touch more effect rows; it says nothing about delivery, uptime, action cost, duration, caps (percentage tags cap at 100; Afterburn, Reflect and the lifesteal/vamp leech budget cap at 60% of a hit) or the combat multiplication that follows. Mechanical legality and numerical non-dominance do not prove combat balance.

