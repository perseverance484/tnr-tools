# Bloodright rebalance (scorer v1)

Cumulative Bloodright bonuses per build, prerequisites included (RUL-2026-10-18-001 presentation). Weight = seven-round HP-equivalent value / 50.5 (1 = 1% of a level-100 health pool), scored by `scripts/bloodright_balance/` against a mirror of the kit.


## Aerathiel

Paths within 91% of each other; weakest add-on 64% of the strongest; average full build 5.37 Weight (before: 5.62).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Withering Breath: +2% IDG | Strength to Dust: +3% IDG | Total Disintegration: +5% IDG | +10% IDG |
| p2 | Eroding Touch: +2% IDT | Particulate Fracture: +3% IDT | Atomic Reprisal: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% IDT |
| p3 | Compressed Mote: +0.4 Damage | Hollowing Wind: +0.8 Damage | Dustfall Rupture: +5% IDT | +1.2 Damage, +5% IDT |
| p4 | Rebounding Motes: +2% Reflect | Returning Gale: +3% Reflect | Resonant Dust Reprisal: +5% Reflect | +10% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% IDG, +5% IDT
- p1 + p3: +1.2 Damage, +10% IDG
- p1 + p4: +10% IDG, +5% Reflect
- p2 + p1: +0.4 Damage, +5% DDG, +5% IDG, +5% IDT
- p2 + p3: +1.6 Damage, +5% DDG, +5% IDT
- p2 + p4: +0.4 Damage, +5% DDG, +5% IDT, +5% Reflect
- p3 + p1: +1.2 Damage, +5% IDG, +5% IDT
- p3 + p2: +1.2 Damage, +10% IDT
- p3 + p4: +1.2 Damage, +5% IDT, +5% Reflect
- p4 + p1: +5% IDG, +10% Reflect
- p4 + p2: +5% IDT, +10% Reflect
- p4 + p3: +1.2 Damage, +10% Reflect

Nodes whose effects changed (names need review):

- p1_t1 Withering Breath: +2% DDG -> +2% IDG
- p1_t2 Strength to Dust: +3% DDG -> +3% IDG
- p1_t3 Total Disintegration: +0.4 Damage, +5% IDG -> +5% IDG
- p2_t3 Atomic Reprisal: +5% DDG, +5% Reflect -> +0.4 Damage, +5% DDG
- p3_t3 Dustfall Rupture: +0.6 Damage, +5% IDT -> +5% IDT
- p4_t3 Resonant Dust Reprisal: +5% IDG, +5% Reflect -> +5% Reflect

## Arashima

Paths within 98% of each other; weakest add-on 60% of the strongest; average full build 4.66 Weight (before: 3.82).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Thunderseed: +2% IDG | Gathering Thunderhead: +3% IDG | Reaper's Stormlance: +0.8 Damage, +5% Poison | +0.8 Damage, +5% IDG, +5% Poison |
| p2 | Stormveil: +2% Lifesteal | Rainbound Mantle: +3% Lifesteal | The Storm's Due: +5% DDG, +25 Drain | +5% DDG, +25 Drain, +5% Lifesteal |
| p3 | Storm Needle: +2% Pierce | Cloudsplitter: +3% Pierce | Unleashed Thunderhead: +5% Poison | +5% Pierce, +5% Poison |
| p4 | Deadwind Breath: +2% DDG | Deadwind Dirge: +3% DDG | Tempest Breaks Through: +5% DDG, +5% Lifesteal | +10% DDG, +5% Lifesteal |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% IDG, +5% Lifesteal, +5% Poison
- p1 + p3: +0.8 Damage, +5% IDG, +5% Pierce, +5% Poison
- p1 + p4: +0.8 Damage, +5% DDG, +5% IDG, +5% Poison
- p2 + p1: +5% DDG, +25 Drain, +5% IDG, +5% Lifesteal
- p2 + p3: +5% DDG, +25 Drain, +5% Lifesteal, +5% Pierce
- p2 + p4: +10% DDG, +25 Drain, +5% Lifesteal
- p3 + p1: +5% IDG, +5% Pierce, +5% Poison
- p3 + p2: +5% Lifesteal, +5% Pierce, +5% Poison
- p3 + p4: +5% DDG, +5% Pierce, +5% Poison
- p4 + p1: +10% DDG, +5% IDG, +5% Lifesteal
- p4 + p2: +10% DDG, +10% Lifesteal
- p4 + p3: +10% DDG, +5% Lifesteal, +5% Pierce

Nodes whose effects changed (names need review):

- p1_t1 Thunderseed: +0.4 Damage -> +2% IDG
- p1_t2 Gathering Thunderhead: +1.2 Damage -> +3% IDG
- p1_t3 Reaper's Stormlance: +25 Drain, +5% Pierce -> +0.8 Damage, +5% Poison
- p2_t1 Stormveil: +2% DDT -> +2% Lifesteal
- p2_t2 Rainbound Mantle: +3% DDT -> +3% Lifesteal
- p3_t3 Unleashed Thunderhead: +0.8 Damage, +5% IDG -> +5% Poison
- p4_t3 Tempest Breaks Through: +5% IDG, +2% Pierce -> +5% DDG, +5% Lifesteal

## Bakuhatsu

Paths within 81% of each other; weakest add-on 88% of the strongest; average full build 5.15 Weight (before: 6.43).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Trigger Spark: +2% Afterburn | Primed Detonation: +3% Afterburn | Shelter at Ground Zero: +5% Afterburn | +10% Afterburn |
| p2 | Packed Charge: +0.2 Damage | Powder Keg: +0.8 Damage | Critical Mass: +5% DDT | +1 Damage, +5% DDT |
| p3 | Stress Crack: +2% IDT | Fractured Casing: +3% IDT | Siege Battery: +5% IDT | +10% IDT |
| p4 | Blast Padding: +2% DDT | Layered Casing: +3% DDT | Bastion of Shrapnel: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +5% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +10% Afterburn
- p1 + p3: +10% Afterburn, +5% IDT
- p1 + p4: +10% Afterburn, +5% DDT
- p2 + p1: +1 Damage, +5% Afterburn, +5% DDT
- p2 + p3: +1 Damage, +5% DDT, +5% IDT
- p2 + p4: +1 Damage, +10% DDT
- p3 + p1: +5% Afterburn, +10% IDT
- p3 + p2: +1 Damage, +10% IDT
- p3 + p4: +5% DDT, +10% IDT
- p4 + p1: +0.4 Damage, +10% Afterburn, +5% DDT
- p4 + p2: +1.4 Damage, +5% Afterburn, +5% DDT
- p4 + p3: +0.4 Damage, +5% Afterburn, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Shelter at Ground Zero: +5% Afterburn, +5% DDT -> +5% Afterburn
- p2_t3 Critical Mass: +5% IDG -> +5% DDT
- p3_t3 Siege Battery: +0.4 Damage, +5% Afterburn -> +5% IDT
- p4_t3 Bastion of Shrapnel: +5% DDT, +5% IDT -> +0.4 Damage, +5% Afterburn

## Blood-Enchanted Eyes

Paths within 92% of each other; weakest add-on 77% of the strongest; average full build 5.69 Weight (before: 7.49).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sanguine Edge: +2% Afterburn | Crimson Cleave: +3% Afterburn | Covenant of Blunted Blades: +5% DDT | +5% Afterburn, +5% DDT |
| p2 | Hungry Pulse: +2% Lifesteal | Crimson Thirst: +3% Lifesteal | Feast of the Fallen: +5% Vamp | +5% Lifesteal, +5% Vamp |
| p3 | Coagulated Mantle: +2% DDT | Clotted Aegis: +3% DDT | Bloodfed Bastion: +5% Absorb | +5% Absorb, +5% DDT |
| p4 | Withering Gaze: +2% DDG | Sanguine Oppression: +3% DDG | Rending Crimson Brand: +0.8 Damage | +0.8 Damage, +5% DDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% Afterburn, +5% DDT, +5% Lifesteal
- p1 + p3: +5% Afterburn, +10% DDT
- p1 + p4: +5% Afterburn, +5% DDG, +5% DDT
- p2 + p1: +5% Afterburn, +5% Lifesteal, +5% Vamp
- p2 + p3: +5% DDT, +5% Lifesteal, +5% Vamp
- p2 + p4: +5% DDG, +5% Lifesteal, +5% Vamp
- p3 + p1: +5% Absorb, +5% Afterburn, +5% DDT
- p3 + p2: +5% Absorb, +5% DDT, +5% Lifesteal
- p3 + p4: +5% Absorb, +5% DDG, +5% DDT
- p4 + p1: +0.8 Damage, +5% Afterburn, +5% DDG
- p4 + p2: +0.8 Damage, +5% DDG, +5% Lifesteal
- p4 + p3: +0.8 Damage, +5% DDG, +5% DDT

Nodes whose effects changed (names need review):

- p1_t1 Sanguine Edge: +0.2 Damage -> +2% Afterburn
- p1_t2 Crimson Cleave: +0.6 Damage -> +3% Afterburn
- p1_t3 Covenant of Blunted Blades: +5% DDG, +5% DDT -> +5% DDT
- p2_t3 Feast of the Fallen: +5% DDT, +5% Vamp -> +5% Vamp
- p3_t3 Bloodfed Bastion: +5% Absorb, +5% DDT -> +5% Absorb
- p4_t3 Rending Crimson Brand: +5% Afterburn, +5% Pierce -> +0.8 Damage

## Blue Blade Eyes

Paths within 90% of each other; weakest add-on 44% of the strongest; average full build 9.91 Weight (before: 8.90).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostbound Grip: +2% DDG | Deepening Numbness: +3% DDG | Numbing Sapphire Feast: +5% DDG, +5% IDT | +10% DDG, +5% IDT |
| p2 | Sapphire Edge: +0.2 Damage | Honed Crescent: +0.6 Damage | Glacial Aegis: +5% DDT, +5% Lifesteal | +0.8 Damage, +5% DDT, +5% Lifesteal |
| p3 | Frost Mantle: +2% DDT | Hoarfrost Bulwark: +3% DDT | Glacier Unleashed: +5% IDG | +5% DDT, +5% IDG |
| p4 | Hungry Rime: +2% Lifesteal | Thirst of the Frost: +3% Lifesteal | Sapphire Reveals the Flaw: +5% IDT | +5% IDT, +5% Lifesteal |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +10% DDG, +5% IDT
- p1 + p3: +10% DDG, +5% DDT, +5% IDT
- p1 + p4: +10% DDG, +5% IDT, +5% Lifesteal
- p2 + p1: +0.8 Damage, +5% DDG, +5% DDT, +5% Lifesteal
- p2 + p3: +0.8 Damage, +10% DDT, +5% Lifesteal
- p2 + p4: +0.8 Damage, +5% DDT, +10% Lifesteal
- p3 + p1: +5% DDG, +5% DDT, +5% IDG
- p3 + p2: +0.8 Damage, +5% DDT, +5% IDG
- p3 + p4: +5% DDT, +5% IDG, +5% Lifesteal
- p4 + p1: +5% DDG, +5% IDT, +5% Lifesteal
- p4 + p2: +0.8 Damage, +5% IDT, +5% Lifesteal
- p4 + p3: +5% DDT, +5% IDT, +5% Lifesteal

Nodes whose effects changed (names need review):

- p1_t3 Numbing Sapphire Feast: +5% DDG, +5% Lifesteal -> +5% DDG, +5% IDT
- p2_t3 Glacial Aegis: +5% DDT -> +5% DDT, +5% Lifesteal

## Cosmic Ascendant

Paths within 91% of each other; weakest add-on 30% of the strongest; average full build 4.37 Weight (before: 2.80).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Astral Resonance: +2% Afterburn | Resonance Cascade: +3% Afterburn | Supernova's Feast: +5% IDT, +5% Lifesteal | +5% Afterburn, +5% IDT, +5% Lifesteal |
| p2 | Stellar Focus: +2% IDG | Stellar Ascendance: +3% IDG | Voidburst Resonance: +5% Afterburn, +5% IDG | +5% Afterburn, +10% IDG |
| p3 | Gravity Knot: +0.4 Damage | Collapsing Star: +0.8 Damage | Hunger of the Singularity: +5% DDG, +5% IDT | +1.2 Damage, +5% DDG, +5% IDT |
| p4 | Orbiting Veil: +2% IDT | Celestial Mantle: +3% IDT | Unyielding Radiance: +0.8 Damage, +5% DDT | +0.8 Damage, +5% DDT, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% Afterburn, +5% IDG, +5% IDT, +5% Lifesteal
- p1 + p3: +1.2 Damage, +5% Afterburn, +5% IDT, +5% Lifesteal
- p1 + p4: +5% Afterburn, +10% IDT, +5% Lifesteal
- p2 + p1: +10% Afterburn, +10% IDG
- p2 + p3: +1.2 Damage, +5% Afterburn, +10% IDG
- p2 + p4: +5% Afterburn, +10% IDG, +5% IDT
- p3 + p1: +1.2 Damage, +5% Afterburn, +5% DDG, +5% IDT
- p3 + p2: +1.2 Damage, +5% DDG, +5% IDG, +5% IDT
- p3 + p4: +1.2 Damage, +5% DDG, +10% IDT
- p4 + p1: +0.8 Damage, +5% Afterburn, +5% DDT, +5% IDT
- p4 + p2: +0.8 Damage, +5% DDT, +5% IDG, +5% IDT
- p4 + p3: +2 Damage, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Supernova's Feast: +5% Afterburn, +5% Lifesteal -> +5% IDT, +5% Lifesteal
- p2_t3 Voidburst Resonance: +0.4 Damage, +5% Afterburn -> +5% Afterburn, +5% IDG
- p3_t3 Hunger of the Singularity: +5% IDG, +5% Lifesteal -> +5% DDG, +5% IDT
- p4_t1 Orbiting Veil: +2% DDT -> +2% IDT
- p4_t2 Celestial Mantle: +3% DDT -> +3% IDT
- p4_t3 Unyielding Radiance: +5% DDT, +5% IDG -> +0.8 Damage, +5% DDT

## Crystal Essence

Paths within 88% of each other; weakest add-on 64% of the strongest; average full build 4.39 Weight (before: 3.74).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mirror Facet: +2% Reflect | Light Turned Back: +3% Reflect | Citadel of Returning Light: +5% DDT, +5% Reflect | +5% DDT, +10% Reflect |
| p2 | Jade Lattice: +2% DDT | Layered Lattice: +3% DDT | Armored Radiance: +5% IDT | +5% DDT, +5% IDT |
| p3 | Prismatic Focus: +2% IDG | Radiant Convergence: +3% IDG | Shardstorm Reprisal: +0.4 Damage, +5% IDT | +0.4 Damage, +5% IDG, +5% IDT |
| p4 | Keen Shard: +0.4 Damage | Razor Shards: +0.6 Damage | Adamant Lance: +5% IDG, +5% Reflect | +1 Damage, +5% IDG, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% DDT, +10% Reflect
- p1 + p3: +5% DDT, +5% IDG, +10% Reflect
- p1 + p4: +1 Damage, +5% DDT, +10% Reflect
- p2 + p1: +5% DDT, +5% IDT, +5% Reflect
- p2 + p3: +5% DDT, +5% IDG, +5% IDT
- p2 + p4: +1 Damage, +5% DDT, +5% IDT
- p3 + p1: +0.4 Damage, +5% IDG, +5% IDT, +5% Reflect
- p3 + p2: +0.4 Damage, +5% DDT, +5% IDG, +5% IDT
- p3 + p4: +1.4 Damage, +5% IDG, +5% IDT
- p4 + p1: +1 Damage, +5% IDG, +10% Reflect
- p4 + p2: +1 Damage, +5% DDT, +5% IDG, +5% Reflect
- p4 + p3: +1 Damage, +10% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p2_t3 Armored Radiance: +5% DDT, +5% IDG -> +5% IDT
- p3_t3 Shardstorm Reprisal: +0.4 Damage, +5% Reflect -> +0.4 Damage, +5% IDT
- p4_t3 Adamant Lance: +0.8 Damage, +5% DDT -> +5% IDG, +5% Reflect

## Ethereal Monarch

Paths within 69% of each other; weakest add-on 58% of the strongest; average full build 4.84 Weight (before: 5.33).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Soul Splinter: +0.4 Damage | Tear in the Soul: +0.8 Damage | Heaven's Mirrored Crown: +5% Consume, +5% IDT | +1.2 Damage, +5% Consume, +5% IDT |
| p2 | Astral Veil: +2% DDT | Woven Starlight: +3% DDT | Heaven's Wardbreaker: +0.4 Damage, +5% IDT | +0.4 Damage, +5% DDT, +5% IDT |
| p3 | Claimed Stardust: +2% IDT | Soulwoven Aegis: +3% IDT | Thronebreaker of Heaven: +0.4 Damage, +5% Reflect | +0.4 Damage, +5% IDT, +5% Reflect |
| p4 | Ethereal Needle: +2% Afterburn | Veil-Piercing Ray: +3% Afterburn | Spoils of the Celestial Throne: +0.4 Damage, +5% Consume | +0.4 Damage, +5% Afterburn, +5% Consume |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +5% Consume, +5% DDT, +5% IDT
- p1 + p3: +1.2 Damage, +5% Consume, +10% IDT
- p1 + p4: +1.2 Damage, +5% Afterburn, +5% Consume, +5% IDT
- p2 + p1: +1.6 Damage, +5% DDT, +5% IDT
- p2 + p3: +0.4 Damage, +5% DDT, +10% IDT
- p2 + p4: +0.4 Damage, +5% Afterburn, +5% DDT, +5% IDT
- p3 + p1: +1.6 Damage, +5% IDT, +5% Reflect
- p3 + p2: +0.4 Damage, +5% DDT, +5% IDT, +5% Reflect
- p3 + p4: +0.4 Damage, +5% Afterburn, +5% IDT, +5% Reflect
- p4 + p1: +1.6 Damage, +5% Afterburn, +5% Consume
- p4 + p2: +0.4 Damage, +5% Afterburn, +5% Consume, +5% DDT
- p4 + p3: +0.4 Damage, +5% Afterburn, +5% Consume, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Heaven's Mirrored Crown: +5% DDT, +5% Reflect -> +5% Consume, +5% IDT
- p2_t3 Heaven's Wardbreaker: +5% DDT, +3% Pierce -> +0.4 Damage, +5% IDT
- p3_t1 Claimed Stardust: +2% Consume -> +2% IDT
- p3_t2 Soulwoven Aegis: +3% Consume -> +3% IDT
- p3_t3 Thronebreaker of Heaven: +0.6 Damage, +3% Pierce -> +0.4 Damage, +5% Reflect
- p4_t1 Ethereal Needle: +2% Pierce -> +2% Afterburn
- p4_t2 Veil-Piercing Ray: +3% Pierce -> +3% Afterburn

## Eyes of the Forsaken King

Paths within 99% of each other; weakest add-on 40% of the strongest; average full build 4.98 Weight (before: 4.55).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Tarnished Edge: +0.2 Damage | Edge of the Regalia: +0.8 Damage | Throne of Broken Light: +5% Afterburn | +1 Damage, +5% Afterburn |
| p2 | Exile's Mantle: +2% DDT | Halo of the Unbowed: +3% DDT | Judgment of the Forsaken: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +5% DDT |
| p3 | Royal Resolve: +2% Reflect | Radiant Decree: +3% Reflect | Kingdom of One: +5% Reflect | +10% Reflect |
| p4 | Brand of Exile: +2% Afterburn | Condemnation in Light: +3% Afterburn | Usurper's Reckoning: +0.6 Damage, +5% IDG | +0.6 Damage, +5% Afterburn, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% Afterburn, +5% DDT
- p1 + p3: +1 Damage, +5% Afterburn, +5% Reflect
- p1 + p4: +1 Damage, +10% Afterburn
- p2 + p1: +1.4 Damage, +5% Afterburn, +5% DDT
- p2 + p3: +0.4 Damage, +5% Afterburn, +5% DDT, +5% Reflect
- p2 + p4: +0.4 Damage, +10% Afterburn, +5% DDT
- p3 + p1: +1 Damage, +10% Reflect
- p3 + p2: +5% DDT, +10% Reflect
- p3 + p4: +5% Afterburn, +10% Reflect
- p4 + p1: +1.6 Damage, +5% Afterburn, +5% IDG
- p4 + p2: +0.6 Damage, +5% Afterburn, +5% DDT, +5% IDG
- p4 + p3: +0.6 Damage, +5% Afterburn, +5% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Throne of Broken Light: +5% IDG -> +5% Afterburn
- p3_t1 Royal Resolve: +2% IDG -> +2% Reflect
- p3_t2 Radiant Decree: +3% IDG -> +3% Reflect
- p3_t3 Kingdom of One: +0.6 Damage, +5% Reflect -> +5% Reflect
- p4_t3 Usurper's Reckoning: +5% DDT, +5% Reflect -> +0.6 Damage, +5% IDG

## Heavenly Sonata

Paths within 84% of each other; weakest add-on 83% of the strongest; average full build 3.80 Weight (before: 3.85).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Opening Measure: +2% IDG | Rising Crescendo: +3% IDG | Discordant Sanctuary: +25 Drain, +5% IDT | +25 Drain, +5% IDG, +5% IDT |
| p2 | Striking Note: +2% DDT | Dissonant Chord: +3% DDT | Sanctuary of Waning Breath: +5% DDT, +25 Drain | +10% DDT, +25 Drain |
| p3 | Fracturing Tone: +2% IDT | Unraveling Harmony: +3% IDT | Anthem of Ascendancy: +5% DDG, +5% IDG | +5% DDG, +5% IDG, +5% IDT |
| p4 | Muted Note: +2% DDG | Muted Strings: +3% DDG | Dirge of Dwindling Strength: +5% DDG, +5% DDT | +10% DDG, +5% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDT, +25 Drain, +5% IDG, +5% IDT
- p1 + p3: +25 Drain, +5% IDG, +10% IDT
- p1 + p4: +5% DDG, +25 Drain, +5% IDG, +5% IDT
- p2 + p1: +10% DDT, +25 Drain, +5% IDG
- p2 + p3: +10% DDT, +25 Drain, +5% IDT
- p2 + p4: +5% DDG, +10% DDT, +25 Drain
- p3 + p1: +5% DDG, +10% IDG, +5% IDT
- p3 + p2: +5% DDG, +5% DDT, +5% IDG, +5% IDT
- p3 + p4: +10% DDG, +5% IDG, +5% IDT
- p4 + p1: +10% DDG, +5% DDT, +5% IDG
- p4 + p2: +10% DDG, +10% DDT
- p4 + p3: +10% DDG, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Discordant Sanctuary: +5% DDT, +5% IDT -> +25 Drain, +5% IDT
- p2_t1 Striking Note: +0.4 Damage -> +2% DDT
- p2_t2 Dissonant Chord: +1.2 Damage -> +3% DDT
- p4_t3 Dirge of Dwindling Strength: +5% DDG, +25 Drain -> +5% DDG, +5% DDT

## Houkyuken

Paths within 85% of each other; weakest add-on 72% of the strongest; average full build 5.11 Weight (before: 5.14).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Lodestone Knuckle: +0.2 Damage | Polarized Fist: +0.8 Damage | Starfall Hammer: +5% DDT, +5% IDG | +1 Damage, +5% DDT, +5% IDG |
| p2 | Repelling Field: +2% IDT | Reversed Polarity: +3% IDT | Inexorable Pull: +5% IDT | +10% IDT |
| p3 | Aligned Force: +2% IDG | Lodestone Resonance: +3% IDG | Aegis of Reversed Force: +5% IDG | +10% IDG |
| p4 | Rebounding Field: +2% Reflect | Like Poles Repel: +3% Reflect | Violent Repulsion: +5% Reflect | +10% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% DDT, +5% IDG, +5% IDT
- p1 + p3: +1 Damage, +5% DDT, +10% IDG
- p1 + p4: +1 Damage, +5% DDT, +5% IDG, +5% Reflect
- p2 + p1: +1 Damage, +10% IDT
- p2 + p3: +5% IDG, +10% IDT
- p2 + p4: +10% IDT, +5% Reflect
- p3 + p1: +1 Damage, +10% IDG
- p3 + p2: +10% IDG, +5% IDT
- p3 + p4: +10% IDG, +5% Reflect
- p4 + p1: +1 Damage, +10% Reflect
- p4 + p2: +5% IDT, +10% Reflect
- p4 + p3: +5% IDG, +10% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Starfall Hammer: +0.6 Damage, +5% IDG -> +5% DDT, +5% IDG
- p2_t1 Repelling Field: +2% DDT -> +2% IDT
- p2_t2 Reversed Polarity: +3% DDT -> +3% IDT
- p2_t3 Inexorable Pull: +0.4 Damage, +5% IDT -> +5% IDT
- p3_t3 Aegis of Reversed Force: +5% DDT, +5% Reflect -> +5% IDG
- p4_t3 Violent Repulsion: +5% IDT, +5% Reflect -> +5% Reflect

## Hyouga Yui

Paths within 63% of each other; weakest add-on 57% of the strongest; average full build 5.27 Weight (before: 6.58).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Rime Shell: +2% DDT | Glacial Rampart: +3% DDT | Avalanche Bastion: +5% DDT | +10% DDT |
| p2 | Purgatory's Chill: +2% IDG | Deepening Frost: +3% IDG | The Glacier Advances: +0.4 Damage | +0.4 Damage, +5% IDG |
| p3 | Icebound Point: +0.4 Damage | Glacial Fang: +0.8 Damage | Spear Behind the Icewall: +5% IDT | +1.2 Damage, +5% IDT |
| p4 | Brittle Rime: +2% IDT | Purgatory's Fracture: +3% IDT | Bastion of Broken Ice: +0.4 Damage, +5% DDT | +0.4 Damage, +5% DDT, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% DDT, +5% IDG
- p1 + p3: +1.2 Damage, +10% DDT
- p1 + p4: +10% DDT, +5% IDT
- p2 + p1: +0.4 Damage, +5% DDT, +5% IDG
- p2 + p3: +1.6 Damage, +5% IDG
- p2 + p4: +0.4 Damage, +5% IDG, +5% IDT
- p3 + p1: +1.2 Damage, +5% DDT, +5% IDT
- p3 + p2: +1.2 Damage, +5% IDG, +5% IDT
- p3 + p4: +1.2 Damage, +10% IDT
- p4 + p1: +0.4 Damage, +10% DDT, +5% IDT
- p4 + p2: +0.4 Damage, +5% DDT, +5% IDG, +5% IDT
- p4 + p3: +1.6 Damage, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Avalanche Bastion: +5% DDT, +5% IDG -> +5% DDT
- p2_t3 The Glacier Advances: +0.4 Damage, +5% IDT -> +0.4 Damage
- p3_t3 Spear Behind the Icewall: +0.8 Damage, +5% DDT -> +5% IDT
- p4_t3 Bastion of Broken Ice: +5% DDT, +5% IDT -> +0.4 Damage, +5% DDT

## Itojinsei

Paths within 94% of each other; weakest add-on 45% of the strongest; average full build 5.26 Weight (before: 4.18).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Exposing Thread: +2% IDT | Razor Strands: +3% IDT | Severing Lattice: +5% DDG, +5% IDT | +5% DDG, +10% IDT |
| p2 | Taut Filament: +2% IDG | Threadbound Vigor: +3% IDG | Weaver Ascendant: +5% IDG | +10% IDG |
| p3 | Wire Edge: +0.2 Damage | Keen Filament: +0.6 Damage | The Severing Thread: +5% IDG, +5% IDT | +0.8 Damage, +5% IDG, +5% IDT |
| p4 | Tightening Snare: +2% DDG | Constricting Coils: +3% DDG | Iron Stranglehold: +5% DDG | +10% DDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDG, +5% IDG, +10% IDT
- p1 + p3: +0.8 Damage, +5% DDG, +10% IDT
- p1 + p4: +10% DDG, +10% IDT
- p2 + p1: +10% IDG, +5% IDT
- p2 + p3: +0.8 Damage, +10% IDG
- p2 + p4: +5% DDG, +10% IDG
- p3 + p1: +0.8 Damage, +5% IDG, +10% IDT
- p3 + p2: +0.8 Damage, +10% IDG, +5% IDT
- p3 + p4: +0.8 Damage, +5% DDG, +5% IDG, +5% IDT
- p4 + p1: +10% DDG, +5% IDT
- p4 + p2: +10% DDG, +5% IDG
- p4 + p3: +0.8 Damage, +10% DDG

Nodes whose effects changed (names need review):

- p1_t3 Severing Lattice: +5% IDT -> +5% DDG, +5% IDT
- p3_t3 The Severing Thread: +0.6 Damage -> +5% IDG, +5% IDT

## Kyuko-sei

Paths within 95% of each other; weakest add-on 49% of the strongest; average full build 4.46 Weight (before: 5.53).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Dense Starmote: +0.2 Damage | Shattered Firmament: +0.6 Damage | Mantle of the Dying Star: +5% DDG, +5% DDT | +0.8 Damage, +5% DDG, +5% DDT |
| p2 | Fading Force: +2% IDG | Entropic Weakening: +3% IDG | Frailty of Ages: +5% DDG | +5% DDG, +5% IDG |
| p3 | Dust Shroud: +2% DDT | Aeonic Mantle: +3% DDT | Sanctuary of Erosion: +0.4 Damage, +5% DDT | +0.4 Damage, +10% DDT |
| p4 | Eroded Seam: +2% IDT | Crumbling Firmament: +3% IDT | Dominion of Entropy: +0.4 Damage | +0.4 Damage, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +5% DDT, +5% IDG
- p1 + p3: +0.8 Damage, +5% DDG, +10% DDT
- p1 + p4: +0.8 Damage, +5% DDG, +5% DDT, +5% IDT
- p2 + p1: +0.8 Damage, +5% DDG, +5% IDG
- p2 + p3: +5% DDG, +5% DDT, +5% IDG
- p2 + p4: +5% DDG, +5% IDG, +5% IDT
- p3 + p1: +1.2 Damage, +10% DDT
- p3 + p2: +0.4 Damage, +10% DDT, +5% IDG
- p3 + p4: +0.4 Damage, +10% DDT, +5% IDT
- p4 + p1: +1.2 Damage, +5% IDT
- p4 + p2: +0.4 Damage, +5% IDG, +5% IDT
- p4 + p3: +0.4 Damage, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Mantle of the Dying Star: +5% DDT, +5% IDG -> +5% DDG, +5% DDT
- p2_t1 Fading Force: +2% DDG -> +2% IDG
- p2_t2 Entropic Weakening: +3% DDG -> +3% IDG
- p2_t3 Frailty of Ages: +5% DDG, +5% IDT -> +5% DDG
- p3_t3 Sanctuary of Erosion: +5% DDT, +5% IDT -> +0.4 Damage, +5% DDT
- p4_t3 Dominion of Entropy: +5% DDG, +5% IDG -> +0.4 Damage

## Oblivion Seal

Paths within 89% of each other; weakest add-on 83% of the strongest; average full build 4.92 Weight (before: 5.88).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Umbral Vigor: +2% DDT | Umbral Claws: +3% DDT | Absolute Erasure: +5% DDT | +10% DDT |
| p2 | Eroding Curse: +2% IDT | Shadow-Laid Fracture: +3% IDT | Brand of Oblivion: +5% IDT | +10% IDT |
| p3 | Void Needle: +2% Pierce | Wardrending Shade: +3% Pierce | Sanguine Seal of Shelter: +5% Pierce | +10% Pierce |
| p4 | Darkened Edge: +0.4 Damage | Rending Sigil: +0.8 Damage | Wardbreaker in Shadow: +5% IDG | +1.2 Damage, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% DDT, +5% IDT
- p1 + p3: +10% DDT, +5% Pierce
- p1 + p4: +1.2 Damage, +10% DDT
- p2 + p1: +5% DDT, +10% IDT
- p2 + p3: +10% IDT, +5% Pierce
- p2 + p4: +1.2 Damage, +10% IDT
- p3 + p1: +5% DDT, +10% Pierce
- p3 + p2: +5% IDT, +10% Pierce
- p3 + p4: +1.2 Damage, +10% Pierce
- p4 + p1: +1.2 Damage, +5% DDT, +5% IDG
- p4 + p2: +1.2 Damage, +5% IDG, +5% IDT
- p4 + p3: +1.2 Damage, +5% IDG, +5% Pierce

Nodes whose effects changed (names need review):

- p1_t1 Umbral Vigor: +2% IDG -> +2% DDT
- p1_t2 Umbral Claws: +3% IDG -> +3% DDT
- p1_t3 Absolute Erasure: +5% IDG, +0.4% Pierce -> +5% DDT
- p3_t3 Sanguine Seal of Shelter: +5% DDT, +5% Lifesteal -> +5% Pierce
- p4_t3 Wardbreaker in Shadow: +5% DDT, +2% Pierce -> +5% IDG

## Shadow Weaver

Paths within 57% of each other; weakest add-on 30% of the strongest; average full build 4.18 Weight (before: 3.86).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sharpened Shadow: +0.2 Damage | Barbed Thread: +0.6 Damage | Night Unraveled: +5% DDG, +5% DDT | +0.8 Damage, +5% DDG, +5% DDT |
| p2 | Tension in the Dark: +2% IDG | Empowered Stitch: +3% IDG | A Thousand Striking Threads: +0.4 Damage | +0.4 Damage, +5% IDG |
| p3 | Dampening Thread: +2% DDG | Frayed Resolve: +3% DDG | Strings Cut Short: +5% IDG | +5% DDG, +5% IDG |
| p4 | Warding Stitch: +2% DDT | Tightened Weave: +3% DDT | Seamless Shroud: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +5% DDT, +5% IDG
- p1 + p3: +0.8 Damage, +10% DDG, +5% DDT
- p1 + p4: +0.8 Damage, +5% DDG, +10% DDT
- p2 + p1: +1.2 Damage, +5% IDG
- p2 + p3: +0.4 Damage, +5% DDG, +5% IDG
- p2 + p4: +0.4 Damage, +5% DDT, +5% IDG
- p3 + p1: +0.8 Damage, +5% DDG, +5% IDG
- p3 + p2: +5% DDG, +10% IDG
- p3 + p4: +5% DDG, +5% DDT, +5% IDG
- p4 + p1: +1.2 Damage, +5% DDG, +5% DDT
- p4 + p2: +0.4 Damage, +5% DDG, +5% DDT, +5% IDG
- p4 + p3: +0.4 Damage, +10% DDG, +5% DDT

Nodes whose effects changed (names need review):

- p1_t3 Night Unraveled: +0.6 Damage -> +5% DDG, +5% DDT
- p2_t3 A Thousand Striking Threads: +5% IDG -> +0.4 Damage
- p3_t3 Strings Cut Short: +5% DDG -> +5% IDG
- p4_t3 Seamless Shroud: +5% DDT -> +0.4 Damage, +5% DDG

## Shakunetsu Sakura

Paths within 92% of each other; weakest add-on 30% of the strongest; average full build 4.57 Weight (before: 7.05).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Kindled Bud: +2% IDG | Kindled Boughs: +3% IDG | Dragon in Full Blossom: +5% IDG | +10% IDG |
| p2 | Petal Needle: +2% DDG | Blossom Through Iron: +3% DDG | Scorching Hanami: +1.2 Damage, +5% IDG | +1.2 Damage, +5% DDG, +5% IDG |
| p3 | Restoring Bud: +2% Heal | Mending Petal Rain: +3% Heal | Dragon's Wardrending Bloom: +0.8 Damage, +5% DDG | +0.8 Damage, +5% DDG, +5% Heal |
| p4 | Scorching Petal: +0.4 Damage | Blazing Petal Torrent: +0.6 Damage | Oppressive Dragon's Breath: +5% DDG, +5% Heal | +1 Damage, +5% DDG, +5% Heal |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDG, +10% IDG
- p1 + p3: +5% Heal, +10% IDG
- p1 + p4: +1 Damage, +10% IDG
- p2 + p1: +1.2 Damage, +5% DDG, +10% IDG
- p2 + p3: +1.2 Damage, +5% DDG, +5% Heal, +5% IDG
- p2 + p4: +2.2 Damage, +5% DDG, +5% IDG
- p3 + p1: +0.8 Damage, +5% DDG, +5% Heal, +5% IDG
- p3 + p2: +0.8 Damage, +10% DDG, +5% Heal
- p3 + p4: +1.8 Damage, +5% DDG, +5% Heal
- p4 + p1: +1 Damage, +5% DDG, +5% Heal, +5% IDG
- p4 + p2: +1 Damage, +10% DDG, +5% Heal
- p4 + p3: +1 Damage, +5% DDG, +10% Heal

Nodes whose effects changed (names need review):

- p1_t3 Dragon in Full Blossom: +0.4 Damage, +5% IDG -> +5% IDG
- p2_t1 Petal Needle: +2% Pierce -> +2% DDG
- p2_t2 Blossom Through Iron: +3% Pierce -> +3% DDG
- p2_t3 Scorching Hanami: +5% Pierce -> +1.2 Damage, +5% IDG
- p3_t3 Dragon's Wardrending Bloom: +5% IDG, +0.4% Pierce -> +0.8 Damage, +5% DDG
- p4_t3 Oppressive Dragon's Breath: +5% DDG, +2% Pierce -> +5% DDG, +5% Heal

## Shinrai Ou

Paths within 83% of each other; weakest add-on 39% of the strongest; average full build 4.77 Weight (before: 4.65).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Vajra Spark: +0.2 Damage | Vajra Tempering: +0.6 Damage | Thunder King's Wrath: +5% Reflect | +0.8 Damage, +5% Reflect |
| p2 | Gathering Voltage: +2% IDG | Crown of Lightning: +3% IDG | Judgement from Above: +5% IDT | +5% IDG, +5% IDT |
| p3 | Echoing Spark: +2% Reflect | Returning Thunder: +3% Reflect | Heaven's Reprisal: +0.4 Damage | +0.4 Damage, +5% Reflect |
| p4 | Conductive Flaw: +2% IDT | Storm-Laid Fracture: +3% IDT | Thunder King's Condemnation: +0.4 Damage, +5% IDG | +0.4 Damage, +5% IDG, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% IDG, +5% Reflect
- p1 + p3: +0.8 Damage, +10% Reflect
- p1 + p4: +0.8 Damage, +5% IDT, +5% Reflect
- p2 + p1: +0.8 Damage, +5% IDG, +5% IDT
- p2 + p3: +5% IDG, +5% IDT, +5% Reflect
- p2 + p4: +5% IDG, +10% IDT
- p3 + p1: +1.2 Damage, +5% Reflect
- p3 + p2: +0.4 Damage, +5% IDG, +5% Reflect
- p3 + p4: +0.4 Damage, +5% IDT, +5% Reflect
- p4 + p1: +1.2 Damage, +5% IDG, +5% IDT
- p4 + p2: +0.4 Damage, +10% IDG, +5% IDT
- p4 + p3: +0.4 Damage, +5% IDG, +5% IDT, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Thunder King's Wrath: +0.6 Damage -> +5% Reflect
- p2_t3 Judgement from Above: +5% IDG -> +5% IDT
- p3_t3 Heaven's Reprisal: +5% Reflect -> +0.4 Damage
- p4_t3 Thunder King's Condemnation: +5% IDT -> +0.4 Damage, +5% IDG

## Shinseina Ki

Paths within 94% of each other; weakest add-on 50% of the strongest; average full build 5.12 Weight (before: 6.53).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Heartwood Edge: +0.4 Damage | Tempered Heartwood: +0.8 Damage | Sundering Heartwood: +5% Poison | +1.2 Damage, +5% Poison |
| p2 | Sapborne Vigor: +2% IDG | Fangs of Heartwood: +3% IDG | The Forest Strikes: +0.4 Damage | +0.4 Damage, +5% IDG |
| p3 | Exposing Root: +2% IDT | Rootbound Prey: +3% IDT | Venomous Judgment of the Grove: +0.4 Damage, +5% IDT | +0.4 Damage, +10% IDT |
| p4 | Bitter Sap: +2% Poison | Burden of the Bitter Boughs: +3% Poison | Dominion of the Venomwood: +0.4 Damage, +5% Poison | +0.4 Damage, +10% Poison |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +5% IDG, +5% Poison
- p1 + p3: +1.2 Damage, +5% IDT, +5% Poison
- p1 + p4: +1.2 Damage, +10% Poison
- p2 + p1: +1.6 Damage, +5% IDG
- p2 + p3: +0.4 Damage, +5% IDG, +5% IDT
- p2 + p4: +0.4 Damage, +5% IDG, +5% Poison
- p3 + p1: +1.6 Damage, +10% IDT
- p3 + p2: +0.4 Damage, +5% IDG, +10% IDT
- p3 + p4: +0.4 Damage, +10% IDT, +5% Poison
- p4 + p1: +1.6 Damage, +10% Poison
- p4 + p2: +0.4 Damage, +5% IDG, +10% Poison
- p4 + p3: +0.4 Damage, +5% IDT, +10% Poison

Nodes whose effects changed (names need review):

- p1_t3 Sundering Heartwood: +0.8 Damage, +5% IDT -> +5% Poison
- p2_t3 The Forest Strikes: +0.4 Damage, +5% IDG -> +0.4 Damage
- p3_t3 Venomous Judgment of the Grove: +5% IDT, +5% Poison -> +0.4 Damage, +5% IDT
- p4_t3 Dominion of the Venomwood: +5% IDG, +5% Poison -> +0.4 Damage, +5% Poison

## Shiroi Youso

Unchanged. Fewer than four eligible root effects for four distinct paths (eligible: Afterburn, DDT, Heal). Needs its element decided first.


## Suragu

Paths within 98% of each other; weakest add-on 73% of the strongest; average full build 5.02 Weight (before: 5.27).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Molten Needle: +0.4 Damage | Slagbreaker: +0.8 Damage | Feast of the Resonant Caldera: +1.2 Damage, +5% IDT | +2.4 Damage, +5% IDT |
| p2 | Softened Crust: +2% IDT | Fractured Slag: +3% IDT | Venomous Feast of the Mountain: +0.8 Damage, +5% Pierce | +0.8 Damage, +5% IDT, +5% Pierce |
| p3 | Hungry Ember: +2% Lifesteal | Molten Draught: +3% Lifesteal | Heart of the Caldera: +5% DDT, +5% Lifesteal | +5% DDT, +10% Lifesteal |
| p4 | Stoked Furnace: +2% DDT | Magmatic Surge: +3% DDT | Wardrending Hunger: +0.6 Damage, +5% DDT | +0.6 Damage, +10% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +2.4 Damage, +10% IDT
- p1 + p3: +2.4 Damage, +5% IDT, +5% Lifesteal
- p1 + p4: +2.4 Damage, +5% DDT, +5% IDT
- p2 + p1: +2 Damage, +5% IDT, +5% Pierce
- p2 + p3: +0.8 Damage, +5% IDT, +5% Lifesteal, +5% Pierce
- p2 + p4: +0.8 Damage, +5% DDT, +5% IDT, +5% Pierce
- p3 + p1: +1.2 Damage, +5% DDT, +10% Lifesteal
- p3 + p2: +5% DDT, +5% IDT, +10% Lifesteal
- p3 + p4: +10% DDT, +10% Lifesteal
- p4 + p1: +1.8 Damage, +10% DDT
- p4 + p2: +0.6 Damage, +10% DDT, +5% IDT
- p4 + p3: +0.6 Damage, +10% DDT, +5% Lifesteal

Nodes whose effects changed (names need review):

- p1_t1 Molten Needle: +2% Pierce -> +0.4 Damage
- p1_t2 Slagbreaker: +3% Pierce -> +0.8 Damage
- p1_t3 Feast of the Resonant Caldera: +5% Afterburn, +5% Lifesteal -> +1.2 Damage, +5% IDT
- p2_t3 Venomous Feast of the Mountain: +5% Lifesteal, +5% Poison -> +0.8 Damage, +5% Pierce
- p4_t1 Stoked Furnace: +2% IDG -> +2% DDT
- p4_t2 Magmatic Surge: +3% IDG -> +3% DDT
- p4_t3 Wardrending Hunger: +5% Lifesteal, +0.4% Pierce -> +0.6 Damage, +5% DDT

## Taiyo Kami

Paths within 93% of each other; weakest add-on 65% of the strongest; average full build 4.69 Weight (before: 4.69).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Breaking Point: +0.4 Damage | Crown of Cinders: +0.6 Damage | Solar Cataclysm: +5% Afterburn, +5% DDG | +1 Damage, +5% Afterburn, +5% DDG |
| p2 | Ember Seed: +2% Afterburn | Emberwake: +3% Afterburn | Eternal Noon: +5% DDT | +5% Afterburn, +5% DDT |
| p3 | Dawnward: +2% DDT | Golden Mantle: +3% DDT | Sovereign Sun: +0.4 Damage, +5% IDT | +0.4 Damage, +5% DDT, +5% IDT |
| p4 | Dawnheart: +2% IDT | Heart of the Sun: +3% IDT | Zenith Incarnate: +0.6 Damage, +5% Afterburn | +0.6 Damage, +5% Afterburn, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +10% Afterburn, +5% DDG
- p1 + p3: +1 Damage, +5% Afterburn, +5% DDG, +5% DDT
- p1 + p4: +1 Damage, +5% Afterburn, +5% DDG, +5% IDT
- p2 + p1: +1 Damage, +5% Afterburn, +5% DDT
- p2 + p3: +5% Afterburn, +10% DDT
- p2 + p4: +5% Afterburn, +5% DDT, +5% IDT
- p3 + p1: +1.4 Damage, +5% DDT, +5% IDT
- p3 + p2: +0.4 Damage, +5% Afterburn, +5% DDT, +5% IDT
- p3 + p4: +0.4 Damage, +5% DDT, +10% IDT
- p4 + p1: +1.6 Damage, +5% Afterburn, +5% IDT
- p4 + p2: +0.6 Damage, +10% Afterburn, +5% IDT
- p4 + p3: +0.6 Damage, +5% Afterburn, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Solar Cataclysm: +0.8 Damage, +5% DDG -> +5% Afterburn, +5% DDG
- p2_t3 Eternal Noon: +0.8 Damage, +5% DDT -> +5% DDT
- p4_t1 Dawnheart: +2% DDG -> +2% IDT
- p4_t2 Heart of the Sun: +3% DDG -> +3% IDT
- p4_t3 Zenith Incarnate: +5% Afterburn, +5% DDG -> +0.6 Damage, +5% Afterburn

## Teno Yuki

Paths within 98% of each other; weakest add-on 73% of the strongest; average full build 4.52 Weight (before: 3.93).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostborne Vigor: +2% IDG | Killing Frost: +3% IDG | Hunger of the Winter Crown: +5% Absorb, +5% IDG | +5% Absorb, +10% IDG |
| p2 | Ice Splinter: +0.2 Damage | Glacial Lance: +0.8 Damage | Palace of Consuming Ice: +5% Absorb, +5% IDT | +1 Damage, +5% Absorb, +5% IDT |
| p3 | Snowbound Mantle: +2% IDT | Permafrost Mantle: +3% IDT | Winter's Sheltering Verdict: +0.4 Damage, +5% Heal | +0.4 Damage, +5% Heal, +5% IDT |
| p4 | Siphoning Snow: +2% Absorb | Ravenous Snowfall: +3% Absorb | Winter's Exposing Command: +5% Heal | +5% Absorb, +5% Heal |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% Absorb, +10% IDG
- p1 + p3: +5% Absorb, +10% IDG, +5% IDT
- p1 + p4: +10% Absorb, +10% IDG
- p2 + p1: +1 Damage, +5% Absorb, +5% IDG, +5% IDT
- p2 + p3: +1 Damage, +5% Absorb, +10% IDT
- p2 + p4: +1 Damage, +10% Absorb, +5% IDT
- p3 + p1: +0.4 Damage, +5% Heal, +5% IDG, +5% IDT
- p3 + p2: +1.4 Damage, +5% Heal, +5% IDT
- p3 + p4: +0.4 Damage, +5% Absorb, +5% Heal, +5% IDT
- p4 + p1: +5% Absorb, +5% Heal, +5% IDG
- p4 + p2: +1 Damage, +5% Absorb, +5% Heal
- p4 + p3: +5% Absorb, +5% Heal, +5% IDT

Nodes whose effects changed (names need review):

- p2_t3 Palace of Consuming Ice: +5% Absorb, +5% DDT -> +5% Absorb, +5% IDT
- p3_t1 Snowbound Mantle: +2% DDT -> +2% IDT
- p3_t2 Permafrost Mantle: +3% DDT -> +3% IDT
- p3_t3 Winter's Sheltering Verdict: +5% DDT, +5% IDT -> +0.4 Damage, +5% Heal
- p4_t3 Winter's Exposing Command: +5% IDG, +5% IDT -> +5% Heal

## Tenohira Musei

Paths within 94% of each other; weakest add-on 49% of the strongest; average full build 5.08 Weight (before: 5.50).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Quieting Touch: +2% DDG | Silencing Pressure: +3% DDG | Hushed Ruin: +5% DDG, +5% IDT | +10% DDG, +5% IDT |
| p2 | Gathered Palm: +0.2 Damage | Condensed Force: +0.8 Damage | Tipping the Balance: +5% DDG, +5% IDG | +1 Damage, +5% DDG, +5% IDG |
| p3 | Centered Intent: +2% IDG | Gathered Force: +3% IDG | The Silent Impact: +0.6 Damage, +5% IDG | +0.6 Damage, +10% IDG |
| p4 | Exposing Palm: +2% IDT | Fracture in Stillness: +3% IDT | Eclipse in Hand: +5% IDT | +10% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +10% DDG, +5% IDT
- p1 + p3: +10% DDG, +5% IDG, +5% IDT
- p1 + p4: +10% DDG, +10% IDT
- p2 + p1: +1 Damage, +10% DDG, +5% IDG
- p2 + p3: +1 Damage, +5% DDG, +10% IDG
- p2 + p4: +1 Damage, +5% DDG, +5% IDG, +5% IDT
- p3 + p1: +0.6 Damage, +5% DDG, +10% IDG
- p3 + p2: +1.6 Damage, +10% IDG
- p3 + p4: +0.6 Damage, +10% IDG, +5% IDT
- p4 + p1: +5% DDG, +10% IDT
- p4 + p2: +1 Damage, +10% IDT
- p4 + p3: +5% IDG, +10% IDT

Nodes whose effects changed (names need review):

- p3_t3 The Silent Impact: +5% IDG, +5% IDT -> +0.6 Damage, +5% IDG
- p4_t3 Eclipse in Hand: +0.4 Damage, +5% IDT -> +5% IDT

## Vaporia

Paths within 92% of each other; weakest add-on 87% of the strongest; average full build 5.08 Weight (before: 5.67).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mending Vapor: +2% IDG | Restorative Mist: +3% IDG | Scald-Laid Weakness: +5% IDT | +5% IDG, +5% IDT |
| p2 | Pressurized Drop: +0.2 Damage | Geyser Fist: +0.8 Damage | Steamclad Wardbreaker: +5% DDT, +5% Pierce | +1 Damage, +5% DDT, +5% Pierce |
| p3 | Resonant Heat: +2% Afterburn | Scalding Resonance: +3% Afterburn | Bastion of Returning Steam: +0.4 Damage, +5% Pierce | +0.4 Damage, +5% Afterburn, +5% Pierce |
| p4 | Scalded Seam: +2% IDT | Deepening Scald: +3% IDT | Dragon's Siphoning Fang: +5% Heal | +5% Heal, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% IDG, +5% IDT
- p1 + p3: +5% Afterburn, +5% IDG, +5% IDT
- p1 + p4: +5% IDG, +10% IDT
- p2 + p1: +1 Damage, +5% DDT, +5% IDG, +5% Pierce
- p2 + p3: +1 Damage, +5% Afterburn, +5% DDT, +5% Pierce
- p2 + p4: +1 Damage, +5% DDT, +5% IDT, +5% Pierce
- p3 + p1: +0.4 Damage, +5% Afterburn, +5% IDG, +5% Pierce
- p3 + p2: +1.4 Damage, +5% Afterburn, +5% Pierce
- p3 + p4: +0.4 Damage, +5% Afterburn, +5% IDT, +5% Pierce
- p4 + p1: +5% Heal, +5% IDG, +5% IDT
- p4 + p2: +1 Damage, +5% Heal, +5% IDT
- p4 + p3: +5% Afterburn, +5% Heal, +5% IDT

Nodes whose effects changed (names need review):

- p1_t1 Mending Vapor: +2% Heal -> +2% IDG
- p1_t2 Restorative Mist: +3% Heal -> +3% IDG
- p3_t3 Bastion of Returning Steam: +5% DDT, +5% Reflect -> +0.4 Damage, +5% Pierce
- p4_t3 Dragon's Siphoning Fang: +5% Lifesteal, +2% Pierce -> +5% Heal
