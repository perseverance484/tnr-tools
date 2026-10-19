# Bloodright rebalance (scorer v1)

Cumulative Bloodright bonuses per build, prerequisites included (RUL-2026-10-18-001 presentation). Weight = seven-round HP-equivalent value / 50.5 (1 = 1% of a level-100 health pool), scored by `scripts/bloodright_balance/` against a mirror of the kit. Pierce and Heal bonuses are flat power: +5 Pierce adds 5 power to each pierce hit, +5 Heal adds 50 HP per heal tick.


## Aerathiel

Weakest completed path is 86% of the strongest; weakest add-on 42% of the strongest; average full build 4.71 Weight (before: 6.09).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Withering Breath: +2% DDG | Strength to Dust: +3% DDG | Total Disintegration: +5% DDG | +10% DDG |
| p2 | Eroding Touch: +2% IDT | Particulate Fracture: +3% IDT | Atomic Reprisal: +0.6 Damage | +0.6 Damage, +5% IDT |
| p3 | Compressed Mote: +0.2 Damage | Hollowing Wind: +0.8 Damage | Dustfall Rupture: +5% IDG | +1 Damage, +5% IDG |
| p4 | Rebounding Motes: +2% Reflect | Returning Gale: +3% Reflect | Resonant Dust Reprisal: +5% Reflect | +10% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% DDG, +5% IDT
- p1 + p3: +1 Damage, +10% DDG
- p1 + p4: +10% DDG, +5% Reflect
- p2 + p1: +0.6 Damage, +5% DDG, +5% IDT
- p2 + p3: +1.6 Damage, +5% IDT
- p2 + p4: +0.6 Damage, +5% IDT, +5% Reflect
- p3 + p1: +1 Damage, +5% DDG, +5% IDG
- p3 + p2: +1 Damage, +5% IDG, +5% IDT
- p3 + p4: +1 Damage, +5% IDG, +5% Reflect
- p4 + p1: +5% DDG, +10% Reflect
- p4 + p2: +5% IDT, +10% Reflect
- p4 + p3: +1 Damage, +10% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Total Disintegration: +0.4 Damage, +5% IDG -> +5% DDG
- p2_t3 Atomic Reprisal: +5% DDG, +5% Reflect -> +0.6 Damage
- p3_t3 Dustfall Rupture: +0.6 Damage, +5% IDT -> +5% IDG
- p4_t3 Resonant Dust Reprisal: +5% IDG, +5% Reflect -> +5% Reflect

## Arashima

Weakest completed path is 90% of the strongest; weakest add-on 22% of the strongest; average full build 3.92 Weight (before: 2.52).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Thunderseed: +0.4 Damage | Gathering Thunderhead: +0.8 Damage | Reaper's Stormlance: +25 Drain, +5 Pierce power | +1.2 Damage, +25 Drain, +5 Pierce power |
| p2 | Stormveil: +2% Lifesteal | Rainbound Mantle: +3% Lifesteal | The Storm's Due: +5% Lifesteal, +5% Poison | +10% Lifesteal, +5% Poison |
| p3 | Storm Needle: +2 Pierce power | Cloudsplitter: +3 Pierce power | Unleashed Thunderhead: +25 Drain, +5% IDG | +25 Drain, +5% IDG, +5 Pierce power |
| p4 | Deadwind Breath: +2% Poison | Deadwind Dirge: +3% Poison | Tempest Breaks Through: +5 Pierce power, +5% Poison | +5 Pierce power, +10% Poison |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +25 Drain, +5% Lifesteal, +5 Pierce power
- p1 + p3: +1.2 Damage, +25 Drain, +10 Pierce power
- p1 + p4: +1.2 Damage, +25 Drain, +5 Pierce power, +5% Poison
- p2 + p1: +1.2 Damage, +10% Lifesteal, +5% Poison
- p2 + p3: +10% Lifesteal, +5 Pierce power, +5% Poison
- p2 + p4: +10% Lifesteal, +10% Poison
- p3 + p1: +1.2 Damage, +25 Drain, +5% IDG, +5 Pierce power
- p3 + p2: +25 Drain, +5% IDG, +5% Lifesteal, +5 Pierce power
- p3 + p4: +25 Drain, +5% IDG, +5 Pierce power, +5% Poison
- p4 + p1: +1.2 Damage, +5 Pierce power, +10% Poison
- p4 + p2: +5% Lifesteal, +5 Pierce power, +10% Poison
- p4 + p3: +10 Pierce power, +10% Poison

Nodes whose effects changed (names need review):

- p2_t1 Stormveil: +2% DDT -> +2% Lifesteal
- p2_t2 Rainbound Mantle: +3% DDT -> +3% Lifesteal
- p2_t3 The Storm's Due: +5% DDG, +25 Drain -> +5% Lifesteal, +5% Poison
- p3_t3 Unleashed Thunderhead: +0.8 Damage, +5% IDG -> +25 Drain, +5% IDG
- p4_t1 Deadwind Breath: +2% DDG -> +2% Poison
- p4_t2 Deadwind Dirge: +3% DDG -> +3% Poison
- p4_t3 Tempest Breaks Through: +5% IDG, +2 Pierce power -> +5 Pierce power, +5% Poison

## Bakuhatsu

Weakest completed path is 67% of the strongest; weakest add-on 79% of the strongest; average full build 5.54 Weight (before: 7.42).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Trigger Spark: +2% Afterburn | Primed Detonation: +3% Afterburn | Shelter at Ground Zero: +0.4 Damage, +5% Afterburn | +0.4 Damage, +10% Afterburn |
| p2 | Packed Charge: +0.4 Damage | Powder Keg: +0.8 Damage | Critical Mass: +5% Afterburn | +1.2 Damage, +5% Afterburn |
| p3 | Stress Crack: +2% IDT | Fractured Casing: +3% IDT | Siege Battery: +0.4 Damage | +0.4 Damage, +5% IDT |
| p4 | Blast Padding: +2% DDT | Layered Casing: +3% DDT | Bastion of Shrapnel: +5% DDT | +10% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.6 Damage, +10% Afterburn
- p1 + p3: +0.4 Damage, +10% Afterburn, +5% IDT
- p1 + p4: +0.4 Damage, +10% Afterburn, +5% DDT
- p2 + p1: +1.2 Damage, +10% Afterburn
- p2 + p3: +1.2 Damage, +5% Afterburn, +5% IDT
- p2 + p4: +1.2 Damage, +5% Afterburn, +5% DDT
- p3 + p1: +0.4 Damage, +5% Afterburn, +5% IDT
- p3 + p2: +1.6 Damage, +5% IDT
- p3 + p4: +0.4 Damage, +5% DDT, +5% IDT
- p4 + p1: +5% Afterburn, +10% DDT
- p4 + p2: +1.2 Damage, +10% DDT
- p4 + p3: +10% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Shelter at Ground Zero: +5% Afterburn, +5% DDT -> +0.4 Damage, +5% Afterburn
- p2_t3 Critical Mass: +5% IDG -> +5% Afterburn
- p3_t3 Siege Battery: +0.4 Damage, +5% Afterburn -> +0.4 Damage
- p4_t3 Bastion of Shrapnel: +5% DDT, +5% IDT -> +5% DDT

## Blood-Enchanted Eyes

Weakest completed path is 90% of the strongest; weakest add-on 63% of the strongest; average full build 5.37 Weight (before: 6.35).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sanguine Edge: +0.2 Damage | Crimson Cleave: +0.8 Damage | Covenant of Blunted Blades: +5% DDG | +1 Damage, +5% DDG |
| p2 | Hungry Pulse: +2% Lifesteal | Crimson Thirst: +3% Lifesteal | Feast of the Fallen: +5% Afterburn, +5% Vamp | +5% Afterburn, +5% Lifesteal, +5% Vamp |
| p3 | Coagulated Mantle: +2% DDT | Clotted Aegis: +3% DDT | Bloodfed Bastion: +5% Absorb | +5% Absorb, +5% DDT |
| p4 | Withering Gaze: +2 Pierce power | Sanguine Oppression: +3 Pierce power | Rending Crimson Brand: +5% Afterburn, +5 Pierce power | +5% Afterburn, +10 Pierce power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% DDG, +5% Lifesteal
- p1 + p3: +1 Damage, +5% DDG, +5% DDT
- p1 + p4: +1 Damage, +5% DDG, +5 Pierce power
- p2 + p1: +1 Damage, +5% Afterburn, +5% Lifesteal, +5% Vamp
- p2 + p3: +5% Afterburn, +5% DDT, +5% Lifesteal, +5% Vamp
- p2 + p4: +5% Afterburn, +5% Lifesteal, +5 Pierce power, +5% Vamp
- p3 + p1: +1 Damage, +5% Absorb, +5% DDT
- p3 + p2: +5% Absorb, +5% DDT, +5% Lifesteal
- p3 + p4: +5% Absorb, +5% DDT, +5 Pierce power
- p4 + p1: +1 Damage, +5% Afterburn, +10 Pierce power
- p4 + p2: +5% Afterburn, +5% Lifesteal, +10 Pierce power
- p4 + p3: +5% Afterburn, +5% DDT, +10 Pierce power

Nodes whose effects changed (names need review):

- p1_t3 Covenant of Blunted Blades: +5% DDG, +5% DDT -> +5% DDG
- p2_t3 Feast of the Fallen: +5% DDT, +5% Vamp -> +5% Afterburn, +5% Vamp
- p3_t3 Bloodfed Bastion: +5% Absorb, +5% DDT -> +5% Absorb
- p4_t1 Withering Gaze: +2% DDG -> +2 Pierce power
- p4_t2 Sanguine Oppression: +3% DDG -> +3 Pierce power

## Blue Blade Eyes

Weakest completed path is 90% of the strongest; weakest add-on 11% of the strongest; average full build 11.42 Weight (before: 8.83).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostbound Grip: +2% DDG | Deepening Numbness: +3% DDG | Numbing Sapphire Feast: +5% DDG, +5% IDG | +10% DDG, +5% IDG |
| p2 | Sapphire Edge: +0.2 Damage | Honed Crescent: +0.4 Damage | Glacial Aegis: +5% IDG | +0.6 Damage, +5% IDG |
| p3 | Frost Mantle: +2% DDT | Hoarfrost Bulwark: +3% DDT | Glacier Unleashed: +5% DDG, +5% IDT | +5% DDG, +5% DDT, +5% IDT |
| p4 | Hungry Rime: +2% Lifesteal | Thirst of the Frost: +3% Lifesteal | Sapphire Reveals the Flaw: +5% IDT | +5% IDT, +5% Lifesteal |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.6 Damage, +10% DDG, +5% IDG
- p1 + p3: +10% DDG, +5% DDT, +5% IDG
- p1 + p4: +10% DDG, +5% IDG, +5% Lifesteal
- p2 + p1: +0.6 Damage, +5% DDG, +5% IDG
- p2 + p3: +0.6 Damage, +5% DDT, +5% IDG
- p2 + p4: +0.6 Damage, +5% IDG, +5% Lifesteal
- p3 + p1: +10% DDG, +5% DDT, +5% IDT
- p3 + p2: +0.6 Damage, +5% DDG, +5% DDT, +5% IDT
- p3 + p4: +5% DDG, +5% DDT, +5% IDT, +5% Lifesteal
- p4 + p1: +5% DDG, +5% IDT, +5% Lifesteal
- p4 + p2: +0.6 Damage, +5% IDT, +5% Lifesteal
- p4 + p3: +5% DDT, +5% IDT, +5% Lifesteal

Nodes whose effects changed (names need review):

- p1_t3 Numbing Sapphire Feast: +5% DDG, +5% Lifesteal -> +5% DDG, +5% IDG
- p2_t3 Glacial Aegis: +5% DDT -> +5% IDG
- p3_t3 Glacier Unleashed: +5% IDG -> +5% DDG, +5% IDT

## Cosmic Ascendant

Weakest completed path is 95% of the strongest; weakest add-on 65% of the strongest; average full build 2.41 Weight (before: 2.38).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Astral Resonance: +2% Afterburn | Resonance Cascade: +3% Afterburn | Supernova's Feast: +0.8 Damage, +5% IDG | +0.8 Damage, +5% Afterburn, +5% IDG |
| p2 | Stellar Focus: +2% IDG | Stellar Ascendance: +3% IDG | Voidburst Resonance: +5% IDG, +5% Lifesteal | +10% IDG, +5% Lifesteal |
| p3 | Gravity Knot: +0.4 Damage | Collapsing Star: +0.8 Damage | Hunger of the Singularity: +5% Afterburn, +5% DDT | +1.2 Damage, +5% Afterburn, +5% DDT |
| p4 | Orbiting Veil: +2% DDT | Celestial Mantle: +3% DDT | Unyielding Radiance: +0.8 Damage, +5% DDT | +0.8 Damage, +10% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% Afterburn, +10% IDG
- p1 + p3: +2 Damage, +5% Afterburn, +5% IDG
- p1 + p4: +0.8 Damage, +5% Afterburn, +5% DDT, +5% IDG
- p2 + p1: +5% Afterburn, +10% IDG, +5% Lifesteal
- p2 + p3: +1.2 Damage, +10% IDG, +5% Lifesteal
- p2 + p4: +5% DDT, +10% IDG, +5% Lifesteal
- p3 + p1: +1.2 Damage, +10% Afterburn, +5% DDT
- p3 + p2: +1.2 Damage, +5% Afterburn, +5% DDT, +5% IDG
- p3 + p4: +1.2 Damage, +5% Afterburn, +10% DDT
- p4 + p1: +0.8 Damage, +5% Afterburn, +10% DDT
- p4 + p2: +0.8 Damage, +10% DDT, +5% IDG
- p4 + p3: +2 Damage, +10% DDT

Nodes whose effects changed (names need review):

- p1_t3 Supernova's Feast: +5% Afterburn, +5% Lifesteal -> +0.8 Damage, +5% IDG
- p2_t3 Voidburst Resonance: +0.4 Damage, +5% Afterburn -> +5% IDG, +5% Lifesteal
- p3_t3 Hunger of the Singularity: +5% IDG, +5% Lifesteal -> +5% Afterburn, +5% DDT
- p4_t3 Unyielding Radiance: +5% DDT, +5% IDG -> +0.8 Damage, +5% DDT

## Crystal Essence

Weakest completed path is 91% of the strongest; weakest add-on 64% of the strongest; average full build 3.88 Weight (before: 3.78).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mirror Facet: +2% Reflect | Light Turned Back: +3% Reflect | Citadel of Returning Light: +5% IDG, +5% Reflect | +5% IDG, +10% Reflect |
| p2 | Jade Lattice: +2% DDT | Layered Lattice: +3% DDT | Armored Radiance: +0.6 Damage, +5% IDG | +0.6 Damage, +5% DDT, +5% IDG |
| p3 | Prismatic Focus: +2% IDG | Radiant Convergence: +3% IDG | Shardstorm Reprisal: +0.4 Damage, +5% DDT | +0.4 Damage, +5% DDT, +5% IDG |
| p4 | Keen Shard: +0.4 Damage | Razor Shards: +0.6 Damage | Adamant Lance: +5% DDT, +5% Reflect | +1 Damage, +5% DDT, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDT, +5% IDG, +10% Reflect
- p1 + p3: +10% IDG, +10% Reflect
- p1 + p4: +1 Damage, +5% IDG, +10% Reflect
- p2 + p1: +0.6 Damage, +5% DDT, +5% IDG, +5% Reflect
- p2 + p3: +0.6 Damage, +5% DDT, +10% IDG
- p2 + p4: +1.6 Damage, +5% DDT, +5% IDG
- p3 + p1: +0.4 Damage, +5% DDT, +5% IDG, +5% Reflect
- p3 + p2: +0.4 Damage, +10% DDT, +5% IDG
- p3 + p4: +1.4 Damage, +5% DDT, +5% IDG
- p4 + p1: +1 Damage, +5% DDT, +10% Reflect
- p4 + p2: +1 Damage, +10% DDT, +5% Reflect
- p4 + p3: +1 Damage, +5% DDT, +5% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Citadel of Returning Light: +5% DDT, +5% Reflect -> +5% IDG, +5% Reflect
- p2_t3 Armored Radiance: +5% DDT, +5% IDG -> +0.6 Damage, +5% IDG
- p3_t3 Shardstorm Reprisal: +0.4 Damage, +5% Reflect -> +0.4 Damage, +5% DDT
- p4_t3 Adamant Lance: +0.8 Damage, +5% DDT -> +5% DDT, +5% Reflect

## Ethereal Monarch

Weakest completed path is 96% of the strongest; weakest add-on 67% of the strongest; average full build 4.41 Weight (before: 2.06).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Soul Splinter: +2% Afterburn | Tear in the Soul: +3% Afterburn | Heaven's Mirrored Crown: +1.2 Damage, +5% Afterburn | +1.2 Damage, +10% Afterburn |
| p2 | Astral Veil: +2% IDT | Woven Starlight: +3% IDT | Heaven's Wardbreaker: +5% Afterburn, +5% Reflect | +5% Afterburn, +5% IDT, +5% Reflect |
| p3 | Claimed Stardust: +2% Reflect | Soulwoven Aegis: +3% Reflect | Thronebreaker of Heaven: +5 Pierce power, +5% Reflect | +5 Pierce power, +10% Reflect |
| p4 | Ethereal Needle: +2 Pierce power | Veil-Piercing Ray: +3 Pierce power | Spoils of the Celestial Throne: +1.2 Damage, +5 Pierce power | +1.2 Damage, +10 Pierce power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +10% Afterburn, +5% IDT
- p1 + p3: +1.2 Damage, +10% Afterburn, +5% Reflect
- p1 + p4: +1.2 Damage, +10% Afterburn, +5 Pierce power
- p2 + p1: +10% Afterburn, +5% IDT, +5% Reflect
- p2 + p3: +5% Afterburn, +5% IDT, +10% Reflect
- p2 + p4: +5% Afterburn, +5% IDT, +5 Pierce power, +5% Reflect
- p3 + p1: +5% Afterburn, +5 Pierce power, +10% Reflect
- p3 + p2: +5% IDT, +5 Pierce power, +10% Reflect
- p3 + p4: +10 Pierce power, +10% Reflect
- p4 + p1: +1.2 Damage, +5% Afterburn, +10 Pierce power
- p4 + p2: +1.2 Damage, +5% IDT, +10 Pierce power
- p4 + p3: +1.2 Damage, +10 Pierce power, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t1 Soul Splinter: +0.2 Damage -> +2% Afterburn
- p1_t2 Tear in the Soul: +0.6 Damage -> +3% Afterburn
- p1_t3 Heaven's Mirrored Crown: +5% DDT, +5% Reflect -> +1.2 Damage, +5% Afterburn
- p2_t1 Astral Veil: +2% DDT -> +2% IDT
- p2_t2 Woven Starlight: +3% DDT -> +3% IDT
- p2_t3 Heaven's Wardbreaker: +5% DDT, +3 Pierce power -> +5% Afterburn, +5% Reflect
- p3_t1 Claimed Stardust: +2% Consume -> +2% Reflect
- p3_t2 Soulwoven Aegis: +3% Consume -> +3% Reflect
- p3_t3 Thronebreaker of Heaven: +0.6 Damage, +3 Pierce power -> +5 Pierce power, +5% Reflect
- p4_t3 Spoils of the Celestial Throne: +0.4 Damage, +5% Consume -> +1.2 Damage, +5 Pierce power

## Eyes of the Forsaken King

Weakest completed path is 89% of the strongest; weakest add-on 45% of the strongest; average full build 3.87 Weight (before: 3.67).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Tarnished Edge: +0.2 Damage | Edge of the Regalia: +0.8 Damage | Throne of Broken Light: +5% Afterburn | +1 Damage, +5% Afterburn |
| p2 | Exile's Mantle: +2% DDT | Halo of the Unbowed: +3% DDT | Judgment of the Forsaken: +5% IDG, +5% Reflect | +5% DDT, +5% IDG, +5% Reflect |
| p3 | Royal Resolve: +2% Reflect | Radiant Decree: +3% Reflect | Kingdom of One: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +5% Reflect |
| p4 | Brand of Exile: +2% Afterburn | Condemnation in Light: +3% Afterburn | Usurper's Reckoning: +0.6 Damage, +5% IDG | +0.6 Damage, +5% Afterburn, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% Afterburn, +5% DDT
- p1 + p3: +1 Damage, +5% Afterburn, +5% Reflect
- p1 + p4: +1 Damage, +10% Afterburn
- p2 + p1: +1 Damage, +5% DDT, +5% IDG, +5% Reflect
- p2 + p3: +5% DDT, +5% IDG, +10% Reflect
- p2 + p4: +5% Afterburn, +5% DDT, +5% IDG, +5% Reflect
- p3 + p1: +1.4 Damage, +5% Afterburn, +5% Reflect
- p3 + p2: +0.4 Damage, +5% Afterburn, +5% DDT, +5% Reflect
- p3 + p4: +0.4 Damage, +10% Afterburn, +5% Reflect
- p4 + p1: +1.6 Damage, +5% Afterburn, +5% IDG
- p4 + p2: +0.6 Damage, +5% Afterburn, +5% DDT, +5% IDG
- p4 + p3: +0.6 Damage, +5% Afterburn, +5% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Throne of Broken Light: +5% IDG -> +5% Afterburn
- p2_t3 Judgment of the Forsaken: +0.4 Damage, +5% Afterburn -> +5% IDG, +5% Reflect
- p3_t1 Royal Resolve: +2% IDG -> +2% Reflect
- p3_t2 Radiant Decree: +3% IDG -> +3% Reflect
- p3_t3 Kingdom of One: +0.6 Damage, +5% Reflect -> +0.4 Damage, +5% Afterburn
- p4_t3 Usurper's Reckoning: +5% DDT, +5% Reflect -> +0.6 Damage, +5% IDG

## Heavenly Sonata

Weakest completed path is 87% of the strongest; weakest add-on 79% of the strongest; average full build 2.74 Weight (before: 2.73).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Opening Measure: +2% DDT | Rising Crescendo: +3% DDT | Discordant Sanctuary: +5% DDT, +5% IDT | +10% DDT, +5% IDT |
| p2 | Striking Note: +0.4 Damage | Dissonant Chord: +0.8 Damage | Sanctuary of Waning Breath: +5% DDG, +25 Drain | +1.2 Damage, +5% DDG, +25 Drain |
| p3 | Fracturing Tone: +2% IDT | Unraveling Harmony: +3% IDT | Anthem of Ascendancy: +25 Drain, +5% IDT | +25 Drain, +10% IDT |
| p4 | Muted Note: +2% DDG | Muted Strings: +3% DDG | Dirge of Dwindling Strength: +5% DDG, +5% DDT | +10% DDG, +5% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +10% DDT, +5% IDT
- p1 + p3: +10% DDT, +10% IDT
- p1 + p4: +5% DDG, +10% DDT, +5% IDT
- p2 + p1: +1.2 Damage, +5% DDG, +5% DDT, +25 Drain
- p2 + p3: +1.2 Damage, +5% DDG, +25 Drain, +5% IDT
- p2 + p4: +1.2 Damage, +10% DDG, +25 Drain
- p3 + p1: +5% DDT, +25 Drain, +10% IDT
- p3 + p2: +1.2 Damage, +25 Drain, +10% IDT
- p3 + p4: +5% DDG, +25 Drain, +10% IDT
- p4 + p1: +10% DDG, +10% DDT
- p4 + p2: +1.2 Damage, +10% DDG, +5% DDT
- p4 + p3: +10% DDG, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t1 Opening Measure: +2% IDG -> +2% DDT
- p1_t2 Rising Crescendo: +3% IDG -> +3% DDT
- p2_t3 Sanctuary of Waning Breath: +5% DDT, +25 Drain -> +5% DDG, +25 Drain
- p3_t3 Anthem of Ascendancy: +5% DDG, +5% IDG -> +25 Drain, +5% IDT
- p4_t3 Dirge of Dwindling Strength: +5% DDG, +25 Drain -> +5% DDG, +5% DDT

## Houkyuken

Weakest completed path is 89% of the strongest; weakest add-on 57% of the strongest; average full build 4.42 Weight (before: 4.51).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Lodestone Knuckle: +0.2 Damage | Polarized Fist: +0.6 Damage | Starfall Hammer: +5% DDT, +5% IDG | +0.8 Damage, +5% DDT, +5% IDG |
| p2 | Repelling Field: +2% DDT | Reversed Polarity: +3% DDT | Inexorable Pull: +5% DDT, +5% Reflect | +10% DDT, +5% Reflect |
| p3 | Aligned Force: +2% IDG | Lodestone Resonance: +3% IDG | Aegis of Reversed Force: +5% IDG | +10% IDG |
| p4 | Rebounding Field: +2% Reflect | Like Poles Repel: +3% Reflect | Violent Repulsion: +0.4 Damage, +5% IDT | +0.4 Damage, +5% IDT, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +10% DDT, +5% IDG
- p1 + p3: +0.8 Damage, +5% DDT, +10% IDG
- p1 + p4: +0.8 Damage, +5% DDT, +5% IDG, +5% Reflect
- p2 + p1: +0.8 Damage, +10% DDT, +5% Reflect
- p2 + p3: +10% DDT, +5% IDG, +5% Reflect
- p2 + p4: +10% DDT, +10% Reflect
- p3 + p1: +0.8 Damage, +10% IDG
- p3 + p2: +5% DDT, +10% IDG
- p3 + p4: +10% IDG, +5% Reflect
- p4 + p1: +1.2 Damage, +5% IDT, +5% Reflect
- p4 + p2: +0.4 Damage, +5% DDT, +5% IDT, +5% Reflect
- p4 + p3: +0.4 Damage, +5% IDG, +5% IDT, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Starfall Hammer: +0.6 Damage, +5% IDG -> +5% DDT, +5% IDG
- p2_t3 Inexorable Pull: +0.4 Damage, +5% IDT -> +5% DDT, +5% Reflect
- p3_t3 Aegis of Reversed Force: +5% DDT, +5% Reflect -> +5% IDG
- p4_t3 Violent Repulsion: +5% IDT, +5% Reflect -> +0.4 Damage, +5% IDT

## Hyouga Yui

Weakest completed path is 72% of the strongest; weakest add-on 60% of the strongest; average full build 4.52 Weight (before: 4.71).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Rime Shell: +2% DDT | Glacial Rampart: +3% DDT | Avalanche Bastion: +0.4 Damage, +5% IDT | +0.4 Damage, +5% DDT, +5% IDT |
| p2 | Purgatory's Chill: +2% IDG | Deepening Frost: +3% IDG | The Glacier Advances: +5% IDG | +10% IDG |
| p3 | Icebound Point: +0.4 Damage | Glacial Fang: +0.8 Damage | Spear Behind the Icewall: +5% DDT, +5% IDT | +1.2 Damage, +5% DDT, +5% IDT |
| p4 | Brittle Rime: +2% IDT | Purgatory's Fracture: +3% IDT | Bastion of Broken Ice: +5% DDT | +5% DDT, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.4 Damage, +5% DDT, +5% IDG, +5% IDT
- p1 + p3: +1.6 Damage, +5% DDT, +5% IDT
- p1 + p4: +0.4 Damage, +5% DDT, +10% IDT
- p2 + p1: +5% DDT, +10% IDG
- p2 + p3: +1.2 Damage, +10% IDG
- p2 + p4: +10% IDG, +5% IDT
- p3 + p1: +1.2 Damage, +10% DDT, +5% IDT
- p3 + p2: +1.2 Damage, +5% DDT, +5% IDG, +5% IDT
- p3 + p4: +1.2 Damage, +5% DDT, +10% IDT
- p4 + p1: +10% DDT, +5% IDT
- p4 + p2: +5% DDT, +5% IDG, +5% IDT
- p4 + p3: +1.2 Damage, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Avalanche Bastion: +5% DDT, +5% IDG -> +0.4 Damage, +5% IDT
- p2_t3 The Glacier Advances: +0.4 Damage, +5% IDT -> +5% IDG
- p3_t3 Spear Behind the Icewall: +0.8 Damage, +5% DDT -> +5% DDT, +5% IDT
- p4_t3 Bastion of Broken Ice: +5% DDT, +5% IDT -> +5% DDT

## Itojinsei

Weakest completed path is 89% of the strongest; weakest add-on 35% of the strongest; average full build 4.01 Weight (before: 3.06).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Exposing Thread: +2% IDT | Razor Strands: +3% IDT | Severing Lattice: +5% DDG, +5% IDT | +5% DDG, +10% IDT |
| p2 | Taut Filament: +2% IDG | Threadbound Vigor: +3% IDG | Weaver Ascendant: +5% IDG | +10% IDG |
| p3 | Wire Edge: +0.2 Damage | Keen Filament: +0.8 Damage | The Severing Thread: +5% IDG, +5% IDT | +1 Damage, +5% IDG, +5% IDT |
| p4 | Tightening Snare: +2% DDG | Constricting Coils: +3% DDG | Iron Stranglehold: +5% DDG | +10% DDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDG, +5% IDG, +10% IDT
- p1 + p3: +1 Damage, +5% DDG, +10% IDT
- p1 + p4: +10% DDG, +10% IDT
- p2 + p1: +10% IDG, +5% IDT
- p2 + p3: +1 Damage, +10% IDG
- p2 + p4: +5% DDG, +10% IDG
- p3 + p1: +1 Damage, +5% IDG, +10% IDT
- p3 + p2: +1 Damage, +10% IDG, +5% IDT
- p3 + p4: +1 Damage, +5% DDG, +5% IDG, +5% IDT
- p4 + p1: +10% DDG, +5% IDT
- p4 + p2: +10% DDG, +5% IDG
- p4 + p3: +1 Damage, +10% DDG

Nodes whose effects changed (names need review):

- p1_t3 Severing Lattice: +5% IDT -> +5% DDG, +5% IDT
- p3_t3 The Severing Thread: +0.6 Damage -> +5% IDG, +5% IDT

## Kyuko-sei

Weakest completed path is 94% of the strongest; weakest add-on 25% of the strongest; average full build 4.76 Weight (before: 7.33).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Dense Starmote: +0.2 Damage | Shattered Firmament: +0.6 Damage | Mantle of the Dying Star: +5% DDT | +0.8 Damage, +5% DDT |
| p2 | Fading Force: +2% DDG | Entropic Weakening: +3% DDG | Frailty of Ages: +5% IDG | +5% DDG, +5% IDG |
| p3 | Dust Shroud: +2% DDT | Aeonic Mantle: +3% DDT | Sanctuary of Erosion: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% DDT |
| p4 | Eroded Seam: +2% IDG | Crumbling Firmament: +3% IDG | Dominion of Entropy: +0.4 Damage | +0.4 Damage, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +5% DDT
- p1 + p3: +0.8 Damage, +10% DDT
- p1 + p4: +0.8 Damage, +5% DDT, +5% IDG
- p2 + p1: +0.8 Damage, +5% DDG, +5% IDG
- p2 + p3: +5% DDG, +5% DDT, +5% IDG
- p2 + p4: +5% DDG, +10% IDG
- p3 + p1: +1.2 Damage, +5% DDG, +5% DDT
- p3 + p2: +0.4 Damage, +10% DDG, +5% DDT
- p3 + p4: +0.4 Damage, +5% DDG, +5% DDT, +5% IDG
- p4 + p1: +1.2 Damage, +5% IDG
- p4 + p2: +0.4 Damage, +5% DDG, +5% IDG
- p4 + p3: +0.4 Damage, +5% DDT, +5% IDG

Nodes whose effects changed (names need review):

- p1_t3 Mantle of the Dying Star: +5% DDT, +5% IDG -> +5% DDT
- p2_t3 Frailty of Ages: +5% DDG, +5% IDT -> +5% IDG
- p3_t3 Sanctuary of Erosion: +5% DDT, +5% IDT -> +0.4 Damage, +5% DDG
- p4_t1 Eroded Seam: +2% IDT -> +2% IDG
- p4_t2 Crumbling Firmament: +3% IDT -> +3% IDG
- p4_t3 Dominion of Entropy: +5% DDG, +5% IDG -> +0.4 Damage

## Oblivion Seal

Weakest completed path is 98% of the strongest; weakest add-on 72% of the strongest; average full build 4.68 Weight (before: 4.33).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Umbral Vigor: +2% IDG | Umbral Claws: +3% IDG | Absolute Erasure: +5% IDG, +5 Pierce power | +10% IDG, +5 Pierce power |
| p2 | Eroding Curse: +2% IDT | Shadow-Laid Fracture: +3% IDT | Brand of Oblivion: +5% IDG, +5% IDT | +5% IDG, +10% IDT |
| p3 | Void Needle: +2% DDT | Wardrending Shade: +3% DDT | Sanguine Seal of Shelter: +5% DDT, +5% Lifesteal | +10% DDT, +5% Lifesteal |
| p4 | Darkened Edge: +0.2 Damage | Rending Sigil: +0.8 Damage | Wardbreaker in Shadow: +5% DDT, +5% IDT | +1 Damage, +5% DDT, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% IDG, +5% IDT, +5 Pierce power
- p1 + p3: +5% DDT, +10% IDG, +5 Pierce power
- p1 + p4: +1 Damage, +10% IDG, +5 Pierce power
- p2 + p1: +10% IDG, +10% IDT
- p2 + p3: +5% DDT, +5% IDG, +10% IDT
- p2 + p4: +1 Damage, +5% IDG, +10% IDT
- p3 + p1: +10% DDT, +5% IDG, +5% Lifesteal
- p3 + p2: +10% DDT, +5% IDT, +5% Lifesteal
- p3 + p4: +1 Damage, +10% DDT, +5% Lifesteal
- p4 + p1: +1 Damage, +5% DDT, +5% IDG, +5% IDT
- p4 + p2: +1 Damage, +5% DDT, +10% IDT
- p4 + p3: +1 Damage, +10% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p2_t3 Brand of Oblivion: +5% IDT -> +5% IDG, +5% IDT
- p3_t1 Void Needle: +2 Pierce power -> +2% DDT
- p3_t2 Wardrending Shade: +3 Pierce power -> +3% DDT
- p4_t3 Wardbreaker in Shadow: +5% DDT, +2 Pierce power -> +5% DDT, +5% IDT

## Shadow Weaver

Weakest completed path is 89% of the strongest; weakest add-on 29% of the strongest; average full build 4.18 Weight (before: 3.27).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sharpened Shadow: +0.2 Damage | Barbed Thread: +0.6 Damage | Night Unraveled: +5% DDG, +5% IDG | +0.8 Damage, +5% DDG, +5% IDG |
| p2 | Tension in the Dark: +2% IDG | Empowered Stitch: +3% IDG | A Thousand Striking Threads: +0.4 Damage, +5% DDT | +0.4 Damage, +5% DDT, +5% IDG |
| p3 | Dampening Thread: +2% DDG | Frayed Resolve: +3% DDG | Strings Cut Short: +5% DDG, +5% DDT | +10% DDG, +5% DDT |
| p4 | Warding Stitch: +2% DDT | Tightened Weave: +3% DDT | Seamless Shroud: +5% IDG | +5% DDT, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +10% IDG
- p1 + p3: +0.8 Damage, +10% DDG, +5% IDG
- p1 + p4: +0.8 Damage, +5% DDG, +5% DDT, +5% IDG
- p2 + p1: +1.2 Damage, +5% DDT, +5% IDG
- p2 + p3: +0.4 Damage, +5% DDG, +5% DDT, +5% IDG
- p2 + p4: +0.4 Damage, +10% DDT, +5% IDG
- p3 + p1: +0.8 Damage, +10% DDG, +5% DDT
- p3 + p2: +10% DDG, +5% DDT, +5% IDG
- p3 + p4: +10% DDG, +10% DDT
- p4 + p1: +0.8 Damage, +5% DDT, +5% IDG
- p4 + p2: +5% DDT, +10% IDG
- p4 + p3: +5% DDG, +5% DDT, +5% IDG

Nodes whose effects changed (names need review):

- p1_t3 Night Unraveled: +0.6 Damage -> +5% DDG, +5% IDG
- p2_t3 A Thousand Striking Threads: +5% IDG -> +0.4 Damage, +5% DDT
- p3_t3 Strings Cut Short: +5% DDG -> +5% DDG, +5% DDT
- p4_t3 Seamless Shroud: +5% DDT -> +5% IDG

## Shakunetsu Sakura

Weakest completed path is 85% of the strongest; weakest add-on 58% of the strongest; average full build 4.69 Weight (before: 4.84).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Kindled Bud: +2% IDG | Kindled Boughs: +3% IDG | Dragon in Full Blossom: +0.8 Damage, +5% DDG | +0.8 Damage, +5% DDG, +5% IDG |
| p2 | Petal Needle: +2 Pierce power | Blossom Through Iron: +3 Pierce power | Scorching Hanami: +5% DDG | +5% DDG, +5 Pierce power |
| p3 | Restoring Bud: +2 Heal power | Mending Petal Rain: +3 Heal power | Dragon's Wardrending Bloom: +1.2 Damage | +1.2 Damage, +5 Heal power |
| p4 | Scorching Petal: +2% IDT | Blazing Petal Torrent: +3% IDT | Oppressive Dragon's Breath: +0.4 Damage, +5% IDG | +0.4 Damage, +5% IDG, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +5% IDG, +5 Pierce power
- p1 + p3: +0.8 Damage, +5% DDG, +5 Heal power, +5% IDG
- p1 + p4: +0.8 Damage, +5% DDG, +5% IDG, +5% IDT
- p2 + p1: +5% DDG, +5% IDG, +5 Pierce power
- p2 + p3: +5% DDG, +5 Heal power, +5 Pierce power
- p2 + p4: +5% DDG, +5% IDT, +5 Pierce power
- p3 + p1: +1.2 Damage, +5 Heal power, +5% IDG
- p3 + p2: +1.2 Damage, +5 Heal power, +5 Pierce power
- p3 + p4: +1.2 Damage, +5 Heal power, +5% IDT
- p4 + p1: +0.4 Damage, +10% IDG, +5% IDT
- p4 + p2: +0.4 Damage, +5% IDG, +5% IDT, +5 Pierce power
- p4 + p3: +0.4 Damage, +5 Heal power, +5% IDG, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Dragon in Full Blossom: +0.4 Damage, +5% IDG -> +0.8 Damage, +5% DDG
- p2_t3 Scorching Hanami: +5 Pierce power -> +5% DDG
- p3_t3 Dragon's Wardrending Bloom: +5% IDG, +0.4 Pierce power -> +1.2 Damage
- p4_t1 Scorching Petal: +0.6 Damage -> +2% IDT
- p4_t2 Blazing Petal Torrent: +1.2 Damage -> +3% IDT
- p4_t3 Oppressive Dragon's Breath: +5% DDG, +2 Pierce power -> +0.4 Damage, +5% IDG

## Shinrai Ou

Weakest completed path is 57% of the strongest; weakest add-on 20% of the strongest; average full build 4.70 Weight (before: 5.23).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Vajra Spark: +0.2 Damage | Vajra Tempering: +0.4 Damage | Thunder King's Wrath: +0.6 Damage, +5% IDT | +1.2 Damage, +5% IDT |
| p2 | Gathering Voltage: +2% IDG | Crown of Lightning: +3% IDG | Judgement from Above: +0.4 Damage | +0.4 Damage, +5% IDG |
| p3 | Echoing Spark: +2% Reflect | Returning Thunder: +3% Reflect | Heaven's Reprisal: +5% Reflect | +10% Reflect |
| p4 | Conductive Flaw: +2% IDT | Storm-Laid Fracture: +3% IDT | Thunder King's Condemnation: +5% IDT | +10% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +5% IDG, +5% IDT
- p1 + p3: +1.2 Damage, +5% IDT, +5% Reflect
- p1 + p4: +1.2 Damage, +10% IDT
- p2 + p1: +1 Damage, +5% IDG
- p2 + p3: +0.4 Damage, +5% IDG, +5% Reflect
- p2 + p4: +0.4 Damage, +5% IDG, +5% IDT
- p3 + p1: +0.6 Damage, +10% Reflect
- p3 + p2: +5% IDG, +10% Reflect
- p3 + p4: +5% IDT, +10% Reflect
- p4 + p1: +0.6 Damage, +10% IDT
- p4 + p2: +5% IDG, +10% IDT
- p4 + p3: +10% IDT, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Thunder King's Wrath: +0.6 Damage -> +0.6 Damage, +5% IDT
- p2_t3 Judgement from Above: +5% IDG -> +0.4 Damage

## Shinseina Ki

Weakest completed path is 93% of the strongest; weakest add-on 14% of the strongest; average full build 6.37 Weight (before: 7.55).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Heartwood Edge: +0.2 Damage | Tempered Heartwood: +0.6 Damage | Sundering Heartwood: +0.8 Damage, +5% IDT | +1.6 Damage, +5% IDT |
| p2 | Sapborne Vigor: +2% IDG | Fangs of Heartwood: +3% IDG | The Forest Strikes: +0.4 Damage | +0.4 Damage, +5% IDG |
| p3 | Exposing Root: +2% IDT | Rootbound Prey: +3% IDT | Venomous Judgment of the Grove: +5% IDT, +5% Poison | +10% IDT, +5% Poison |
| p4 | Bitter Sap: +2% Poison | Burden of the Bitter Boughs: +3% Poison | Dominion of the Venomwood: +5% IDG | +5% IDG, +5% Poison |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.6 Damage, +5% IDG, +5% IDT
- p1 + p3: +1.6 Damage, +10% IDT
- p1 + p4: +1.6 Damage, +5% IDT, +5% Poison
- p2 + p1: +1.2 Damage, +5% IDG
- p2 + p3: +0.4 Damage, +5% IDG, +5% IDT
- p2 + p4: +0.4 Damage, +5% IDG, +5% Poison
- p3 + p1: +0.8 Damage, +10% IDT, +5% Poison
- p3 + p2: +5% IDG, +10% IDT, +5% Poison
- p3 + p4: +10% IDT, +10% Poison
- p4 + p1: +0.8 Damage, +5% IDG, +5% Poison
- p4 + p2: +10% IDG, +5% Poison
- p4 + p3: +5% IDG, +5% IDT, +5% Poison

Nodes whose effects changed (names need review):

- p2_t3 The Forest Strikes: +0.4 Damage, +5% IDG -> +0.4 Damage
- p4_t3 Dominion of the Venomwood: +5% IDG, +5% Poison -> +5% IDG

## Shiroi Youso

Unchanged. Fewer than four eligible root effects for four distinct paths (eligible: Afterburn, DDT, Heal). Needs its element decided first.


## Suragu

Weakest completed path is 96% of the strongest; weakest add-on 79% of the strongest; average full build 3.89 Weight (before: 3.58).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Molten Needle: +2% DDT | Slagbreaker: +3% DDT | Feast of the Resonant Caldera: +5% IDG, +5% Poison | +5% DDT, +5% IDG, +5% Poison |
| p2 | Softened Crust: +2% IDT | Fractured Slag: +3% IDT | Venomous Feast of the Mountain: +5% Afterburn, +5 Pierce power | +5% Afterburn, +5% IDT, +5 Pierce power |
| p3 | Hungry Ember: +0.4 Damage | Molten Draught: +0.8 Damage | Heart of the Caldera: +1.2 Damage, +5% Poison | +2.4 Damage, +5% Poison |
| p4 | Stoked Furnace: +2% IDG | Magmatic Surge: +3% IDG | Wardrending Hunger: +0.8 Damage, +5 Pierce power | +0.8 Damage, +5% IDG, +5 Pierce power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDT, +5% IDG, +5% IDT, +5% Poison
- p1 + p3: +1.2 Damage, +5% DDT, +5% IDG, +5% Poison
- p1 + p4: +5% DDT, +10% IDG, +5% Poison
- p2 + p1: +5% Afterburn, +5% DDT, +5% IDT, +5 Pierce power
- p2 + p3: +1.2 Damage, +5% Afterburn, +5% IDT, +5 Pierce power
- p2 + p4: +5% Afterburn, +5% IDG, +5% IDT, +5 Pierce power
- p3 + p1: +2.4 Damage, +5% DDT, +5% Poison
- p3 + p2: +2.4 Damage, +5% IDT, +5% Poison
- p3 + p4: +2.4 Damage, +5% IDG, +5% Poison
- p4 + p1: +0.8 Damage, +5% DDT, +5% IDG, +5 Pierce power
- p4 + p2: +0.8 Damage, +5% IDG, +5% IDT, +5 Pierce power
- p4 + p3: +2 Damage, +5% IDG, +5 Pierce power

Nodes whose effects changed (names need review):

- p1_t1 Molten Needle: +2 Pierce power -> +2% DDT
- p1_t2 Slagbreaker: +3 Pierce power -> +3% DDT
- p1_t3 Feast of the Resonant Caldera: +5% Afterburn, +5% Lifesteal -> +5% IDG, +5% Poison
- p2_t3 Venomous Feast of the Mountain: +5% Lifesteal, +5% Poison -> +5% Afterburn, +5 Pierce power
- p3_t1 Hungry Ember: +2% Lifesteal -> +0.4 Damage
- p3_t2 Molten Draught: +3% Lifesteal -> +0.8 Damage
- p3_t3 Heart of the Caldera: +5% DDT, +5% Lifesteal -> +1.2 Damage, +5% Poison
- p4_t3 Wardrending Hunger: +5% Lifesteal, +0.4 Pierce power -> +0.8 Damage, +5 Pierce power

## Taiyo Kami

Weakest completed path is 87% of the strongest; weakest add-on 60% of the strongest; average full build 4.39 Weight (before: 4.23).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Breaking Point: +0.4 Damage | Crown of Cinders: +0.6 Damage | Solar Cataclysm: +5% Afterburn, +5% IDG | +1 Damage, +5% Afterburn, +5% IDG |
| p2 | Ember Seed: +2% Afterburn | Emberwake: +3% Afterburn | Eternal Noon: +0.6 Damage, +5% IDG | +0.6 Damage, +5% Afterburn, +5% IDG |
| p3 | Dawnward: +2% DDT | Golden Mantle: +3% DDT | Sovereign Sun: +0.6 Damage, +5% DDG | +0.6 Damage, +5% DDG, +5% DDT |
| p4 | Dawnheart: +2% IDT | Heart of the Sun: +3% IDT | Zenith Incarnate: +5% Afterburn, +5% DDG | +5% Afterburn, +5% DDG, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +10% Afterburn, +5% IDG
- p1 + p3: +1 Damage, +5% Afterburn, +5% DDT, +5% IDG
- p1 + p4: +1 Damage, +5% Afterburn, +5% IDG, +5% IDT
- p2 + p1: +1.6 Damage, +5% Afterburn, +5% IDG
- p2 + p3: +0.6 Damage, +5% Afterburn, +5% DDT, +5% IDG
- p2 + p4: +0.6 Damage, +5% Afterburn, +5% IDG, +5% IDT
- p3 + p1: +1.6 Damage, +5% DDG, +5% DDT
- p3 + p2: +0.6 Damage, +5% Afterburn, +5% DDG, +5% DDT
- p3 + p4: +0.6 Damage, +5% DDG, +5% DDT, +5% IDT
- p4 + p1: +1 Damage, +5% Afterburn, +5% DDG, +5% IDT
- p4 + p2: +10% Afterburn, +5% DDG, +5% IDT
- p4 + p3: +5% Afterburn, +5% DDG, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Solar Cataclysm: +0.8 Damage, +5% DDG -> +5% Afterburn, +5% IDG
- p2_t3 Eternal Noon: +0.8 Damage, +5% DDT -> +0.6 Damage, +5% IDG
- p3_t3 Sovereign Sun: +0.4 Damage, +5% IDT -> +0.6 Damage, +5% DDG
- p4_t1 Dawnheart: +2% DDG -> +2% IDT
- p4_t2 Heart of the Sun: +3% DDG -> +3% IDT

## Teno Yuki

Weakest completed path is 89% of the strongest; weakest add-on 84% of the strongest; average full build 3.88 Weight (before: 3.31).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostborne Vigor: +2% IDG | Killing Frost: +3% IDG | Hunger of the Winter Crown: +5% IDG, +5% IDT | +10% IDG, +5% IDT |
| p2 | Ice Splinter: +0.4 Damage | Glacial Lance: +0.8 Damage | Palace of Consuming Ice: +5% Absorb, +5% IDT | +1.2 Damage, +5% Absorb, +5% IDT |
| p3 | Snowbound Mantle: +2% IDT | Permafrost Mantle: +3% IDT | Winter's Sheltering Verdict: +5 Heal power | +5 Heal power, +5% IDT |
| p4 | Siphoning Snow: +2% Absorb | Ravenous Snowfall: +3% Absorb | Winter's Exposing Command: +5% Absorb, +5% IDG | +10% Absorb, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +10% IDG, +5% IDT
- p1 + p3: +10% IDG, +10% IDT
- p1 + p4: +5% Absorb, +10% IDG, +5% IDT
- p2 + p1: +1.2 Damage, +5% Absorb, +5% IDG, +5% IDT
- p2 + p3: +1.2 Damage, +5% Absorb, +10% IDT
- p2 + p4: +1.2 Damage, +10% Absorb, +5% IDT
- p3 + p1: +5 Heal power, +5% IDG, +5% IDT
- p3 + p2: +1.2 Damage, +5 Heal power, +5% IDT
- p3 + p4: +5% Absorb, +5 Heal power, +5% IDT
- p4 + p1: +10% Absorb, +10% IDG
- p4 + p2: +1.2 Damage, +10% Absorb, +5% IDG
- p4 + p3: +10% Absorb, +5% IDG, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Hunger of the Winter Crown: +5% Absorb, +5% IDG -> +5% IDG, +5% IDT
- p2_t3 Palace of Consuming Ice: +5% Absorb, +5% DDT -> +5% Absorb, +5% IDT
- p3_t1 Snowbound Mantle: +2% DDT -> +2% IDT
- p3_t2 Permafrost Mantle: +3% DDT -> +3% IDT
- p3_t3 Winter's Sheltering Verdict: +5% DDT, +5% IDT -> +5 Heal power
- p4_t3 Winter's Exposing Command: +5% IDG, +5% IDT -> +5% Absorb, +5% IDG

## Tenohira Musei

Weakest completed path is 89% of the strongest; weakest add-on 62% of the strongest; average full build 5.98 Weight (before: 6.28).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Quieting Touch: +2% DDG | Silencing Pressure: +3% DDG | Hushed Ruin: +5% DDG, +5% IDT | +10% DDG, +5% IDT |
| p2 | Gathered Palm: +0.4 Damage | Condensed Force: +0.8 Damage | Tipping the Balance: +5% DDG, +5% IDG | +1.2 Damage, +5% DDG, +5% IDG |
| p3 | Centered Intent: +2% IDG | Gathered Force: +3% IDG | The Silent Impact: +0.4 Damage, +5% IDG | +0.4 Damage, +10% IDG |
| p4 | Exposing Palm: +2% IDT | Fracture in Stillness: +3% IDT | Eclipse in Hand: +0.4 Damage, +5% IDT | +0.4 Damage, +10% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +10% DDG, +5% IDT
- p1 + p3: +10% DDG, +5% IDG, +5% IDT
- p1 + p4: +10% DDG, +10% IDT
- p2 + p1: +1.2 Damage, +10% DDG, +5% IDG
- p2 + p3: +1.2 Damage, +5% DDG, +10% IDG
- p2 + p4: +1.2 Damage, +5% DDG, +5% IDG, +5% IDT
- p3 + p1: +0.4 Damage, +5% DDG, +10% IDG
- p3 + p2: +1.6 Damage, +10% IDG
- p3 + p4: +0.4 Damage, +10% IDG, +5% IDT
- p4 + p1: +0.4 Damage, +5% DDG, +10% IDT
- p4 + p2: +1.6 Damage, +10% IDT
- p4 + p3: +0.4 Damage, +5% IDG, +10% IDT

Nodes whose effects changed (names need review):

- p3_t3 The Silent Impact: +5% IDG, +5% IDT -> +0.4 Damage, +5% IDG

## Vaporia

Weakest completed path is 96% of the strongest; weakest add-on 81% of the strongest; average full build 4.04 Weight (before: 4.79).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mending Vapor: +2% Lifesteal | Restorative Mist: +3% Lifesteal | Scald-Laid Weakness: +5% IDT | +5% IDT, +5% Lifesteal |
| p2 | Pressurized Drop: +0.2 Damage | Geyser Fist: +0.8 Damage | Steamclad Wardbreaker: +5% DDT, +5 Pierce power | +1 Damage, +5% DDT, +5 Pierce power |
| p3 | Resonant Heat: +2% Afterburn | Scalding Resonance: +3% Afterburn | Bastion of Returning Steam: +5% IDG | +5% Afterburn, +5% IDG |
| p4 | Scalded Seam: +2 Pierce power | Deepening Scald: +3 Pierce power | Dragon's Siphoning Fang: +0.4 Damage, +5% Reflect | +0.4 Damage, +5 Pierce power, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +5% IDT, +5% Lifesteal
- p1 + p3: +5% Afterburn, +5% IDT, +5% Lifesteal
- p1 + p4: +5% IDT, +5% Lifesteal, +5 Pierce power
- p2 + p1: +1 Damage, +5% DDT, +5% Lifesteal, +5 Pierce power
- p2 + p3: +1 Damage, +5% Afterburn, +5% DDT, +5 Pierce power
- p2 + p4: +1 Damage, +5% DDT, +10 Pierce power
- p3 + p1: +5% Afterburn, +5% IDG, +5% Lifesteal
- p3 + p2: +1 Damage, +5% Afterburn, +5% IDG
- p3 + p4: +5% Afterburn, +5% IDG, +5 Pierce power
- p4 + p1: +0.4 Damage, +5% Lifesteal, +5 Pierce power, +5% Reflect
- p4 + p2: +1.4 Damage, +5 Pierce power, +5% Reflect
- p4 + p3: +0.4 Damage, +5% Afterburn, +5 Pierce power, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t1 Mending Vapor: +2 Heal power -> +2% Lifesteal
- p1_t2 Restorative Mist: +3 Heal power -> +3% Lifesteal
- p3_t3 Bastion of Returning Steam: +5% DDT, +5% Reflect -> +5% IDG
- p4_t1 Scalded Seam: +2% IDT -> +2 Pierce power
- p4_t2 Deepening Scald: +3% IDT -> +3 Pierce power
- p4_t3 Dragon's Siphoning Fang: +5% Lifesteal, +2 Pierce power -> +0.4 Damage, +5% Reflect
