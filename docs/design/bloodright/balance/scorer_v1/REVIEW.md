# Bloodright rebalance (scorer v1)

Cumulative Bloodright bonuses per build, prerequisites included (RUL-2026-10-18-001 presentation). Weight = seven-round HP-equivalent value / 50.5 (1 = 1% of a level-100 health pool), scored by `scripts/bloodright_balance/` against a mirror of the kit. Pierce and Heal bonuses are flat power: +5 Pierce adds 5 power to each pierce hit, +5 Heal adds 50 HP per heal tick.

Strength target: an average full build of 5.24 Weight, today's Bloodright power level (the roster median of the round-totals rules without a strength pull). Rules (RUL-2026-10-19-001): every finished build totals a multiple of 5 for each percentage effect (at most 20), paths step +2/+3, +4/+6 or +6/+9, capstones +5 or +10; Damage and Pierce use clean power steps.


## Aerathiel

Weakest completed path is 91% of the strongest; weakest add-on 53% of the strongest; average full build 5.81 Weight (before: 6.45).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Withering Breath: +2% DDG | Strength to Dust: +3% DDG | Total Disintegration: +0.4 Damage, +5% Reflect | +0.4 Damage, +5% DDG, +5% Reflect |
| p2 | Eroding Touch: +2% IDT | Particulate Fracture: +3% IDT | Atomic Reprisal: +5% Reflect | +5% IDT, +5% Reflect |
| p3 | Compressed Mote: +2% IDG | Hollowing Wind: +3% IDG | Dustfall Rupture: +1.2 Damage | +1.2 Damage, +5% IDG |
| p4 | Rebounding Motes: +2% Reflect | Returning Gale: +3% Reflect | Resonant Dust Reprisal: +0.6 Damage, +5% DDG | +0.6 Damage, +5% DDG, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.4 Damage, +5% DDG, +5% IDT, +5% Reflect
- p1 + p3: +0.4 Damage, +5% DDG, +5% IDG, +5% Reflect
- p1 + p4: +0.4 Damage, +5% DDG, +10% Reflect
- p2 + p1: +5% DDG, +5% IDT, +5% Reflect
- p2 + p3: +5% IDG, +5% IDT, +5% Reflect
- p2 + p4: +5% IDT, +10% Reflect
- p3 + p1: +1.2 Damage, +5% DDG, +5% IDG
- p3 + p2: +1.2 Damage, +5% IDG, +5% IDT
- p3 + p4: +1.2 Damage, +5% IDG, +5% Reflect
- p4 + p1: +0.6 Damage, +10% DDG, +5% Reflect
- p4 + p2: +0.6 Damage, +5% DDG, +5% IDT, +5% Reflect
- p4 + p3: +0.6 Damage, +5% DDG, +5% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Total Disintegration: +0.4 Damage, +5% IDG -> +0.4 Damage, +5% Reflect
- p2_t3 Atomic Reprisal: +5% DDG, +5% Reflect -> +5% Reflect
- p3_t1 Compressed Mote: +0.2 Damage -> +2% IDG
- p3_t2 Hollowing Wind: +0.4 Damage -> +3% IDG
- p3_t3 Dustfall Rupture: +0.6 Damage, +5% IDT -> +1.2 Damage
- p4_t3 Resonant Dust Reprisal: +5% IDG, +5% Reflect -> +0.6 Damage, +5% DDG

## Arashima

Weakest completed path is 90% of the strongest; weakest add-on 64% of the strongest; average full build 2.39 Weight (before: 2.32).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Thunderseed: +0.4 Damage | Gathering Thunderhead: +0.8 Damage | Reaper's Stormlance: +25 Drain, +1.2 Pierce power | +1.2 Damage, +25 Drain, +1.2 Pierce power |
| p2 | Stormveil: +4% Poison | Rainbound Mantle: +6% Poison | The Storm's Due: +0.8 Damage, +25 Drain | +0.8 Damage, +25 Drain, +10% Poison |
| p3 | Storm Needle: +0.8 Pierce power | Cloudsplitter: +1.2 Pierce power | Unleashed Thunderhead: +1.2 Damage, +10% IDG | +1.2 Damage, +10% IDG, +2 Pierce power |
| p4 | Deadwind Breath: +4% IDG | Deadwind Dirge: +6% IDG | Tempest Breaks Through: +10% IDG, +10% Poison | +20% IDG, +10% Poison |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +25 Drain, +1.2 Pierce power, +10% Poison
- p1 + p3: +1.2 Damage, +25 Drain, +3.2 Pierce power
- p1 + p4: +1.2 Damage, +25 Drain, +10% IDG, +1.2 Pierce power
- p2 + p1: +2 Damage, +25 Drain, +10% Poison
- p2 + p3: +0.8 Damage, +25 Drain, +2 Pierce power, +10% Poison
- p2 + p4: +0.8 Damage, +25 Drain, +10% IDG, +10% Poison
- p3 + p1: +2.4 Damage, +10% IDG, +2 Pierce power
- p3 + p2: +1.2 Damage, +10% IDG, +2 Pierce power, +10% Poison
- p3 + p4: +1.2 Damage, +20% IDG, +2 Pierce power
- p4 + p1: +1.2 Damage, +20% IDG, +10% Poison
- p4 + p2: +20% IDG, +20% Poison
- p4 + p3: +20% IDG, +2 Pierce power, +10% Poison

Nodes whose effects changed (names need review):

- p2_t1 Stormveil: +2% DDT -> +4% Poison
- p2_t2 Rainbound Mantle: +3% DDT -> +6% Poison
- p2_t3 The Storm's Due: +5% DDG, +25 Drain -> +0.8 Damage, +25 Drain
- p4_t1 Deadwind Breath: +2% DDG -> +4% IDG
- p4_t2 Deadwind Dirge: +3% DDG -> +6% IDG
- p4_t3 Tempest Breaks Through: +5% IDG, +2 Pierce power -> +10% IDG, +10% Poison

## Bakuhatsu

Weakest completed path is 89% of the strongest; weakest add-on 47% of the strongest; average full build 5.26 Weight (before: 6.69).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Trigger Spark: +2% Afterburn | Primed Detonation: +3% Afterburn | Shelter at Ground Zero: +0.6 Damage, +5% IDT | +0.6 Damage, +5% Afterburn, +5% IDT |
| p2 | Packed Charge: +0.2 Damage | Powder Keg: +0.8 Damage | Critical Mass: +10% Afterburn | +1 Damage, +10% Afterburn |
| p3 | Stress Crack: +2% IDT | Fractured Casing: +3% IDT | Siege Battery: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +5% IDT |
| p4 | Blast Padding: +2% DDT | Layered Casing: +3% DDT | Bastion of Shrapnel: +0.6 Damage | +0.6 Damage, +5% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.6 Damage, +5% Afterburn, +5% IDT
- p1 + p3: +0.6 Damage, +5% Afterburn, +10% IDT
- p1 + p4: +0.6 Damage, +5% Afterburn, +5% DDT, +5% IDT
- p2 + p1: +1 Damage, +15% Afterburn
- p2 + p3: +1 Damage, +10% Afterburn, +5% IDT
- p2 + p4: +1 Damage, +10% Afterburn, +5% DDT
- p3 + p1: +0.4 Damage, +10% Afterburn, +5% IDT
- p3 + p2: +1.4 Damage, +5% Afterburn, +5% IDT
- p3 + p4: +0.4 Damage, +5% Afterburn, +5% DDT, +5% IDT
- p4 + p1: +0.6 Damage, +5% Afterburn, +5% DDT
- p4 + p2: +1.6 Damage, +5% DDT
- p4 + p3: +0.6 Damage, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Shelter at Ground Zero: +5% Afterburn, +5% DDT -> +0.6 Damage, +5% IDT
- p2_t3 Critical Mass: +5% IDG -> +10% Afterburn
- p4_t3 Bastion of Shrapnel: +5% DDT, +5% IDT -> +0.6 Damage

## Blood-Enchanted Eyes

Weakest completed path is 93% of the strongest; weakest add-on 37% of the strongest; average full build 5.41 Weight (before: 6.78).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sanguine Edge: +0.2 Damage | Crimson Cleave: +0.6 Damage | Covenant of Blunted Blades: +5% DDG, +0.4 Pierce power | +0.8 Damage, +5% DDG, +0.4 Pierce power |
| p2 | Hungry Pulse: +2% Lifesteal | Crimson Thirst: +3% Lifesteal | Feast of the Fallen: +5% Afterburn, +5% Vamp | +5% Afterburn, +5% Lifesteal, +5% Vamp |
| p3 | Coagulated Mantle: +2% DDT | Clotted Aegis: +3% DDT | Bloodfed Bastion: +5% Absorb, +0.4 Pierce power | +5% Absorb, +5% DDT, +0.4 Pierce power |
| p4 | Withering Gaze: +2% Vamp | Sanguine Oppression: +3% Vamp | Rending Crimson Brand: +10% Afterburn | +10% Afterburn, +5% Vamp |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +5% Lifesteal, +0.4 Pierce power
- p1 + p3: +0.8 Damage, +5% DDG, +5% DDT, +0.4 Pierce power
- p1 + p4: +0.8 Damage, +5% DDG, +0.4 Pierce power, +5% Vamp
- p2 + p1: +0.8 Damage, +5% Afterburn, +5% Lifesteal, +5% Vamp
- p2 + p3: +5% Afterburn, +5% DDT, +5% Lifesteal, +5% Vamp
- p2 + p4: +5% Afterburn, +5% Lifesteal, +10% Vamp
- p3 + p1: +0.8 Damage, +5% Absorb, +5% DDT, +0.4 Pierce power
- p3 + p2: +5% Absorb, +5% DDT, +5% Lifesteal, +0.4 Pierce power
- p3 + p4: +5% Absorb, +5% DDT, +0.4 Pierce power, +5% Vamp
- p4 + p1: +0.8 Damage, +10% Afterburn, +5% Vamp
- p4 + p2: +10% Afterburn, +5% Lifesteal, +5% Vamp
- p4 + p3: +10% Afterburn, +5% DDT, +5% Vamp

Nodes whose effects changed (names need review):

- p1_t3 Covenant of Blunted Blades: +5% DDG, +5% DDT -> +5% DDG, +0.4 Pierce power
- p2_t3 Feast of the Fallen: +5% DDT, +5% Vamp -> +5% Afterburn, +5% Vamp
- p3_t3 Bloodfed Bastion: +5% Absorb, +5% DDT -> +5% Absorb, +0.4 Pierce power
- p4_t1 Withering Gaze: +2% DDG -> +2% Vamp
- p4_t2 Sanguine Oppression: +3% DDG -> +3% Vamp
- p4_t3 Rending Crimson Brand: +5% Afterburn, +5 Pierce power -> +10% Afterburn

## Blue Blade Eyes

Weakest completed path is 55% of the strongest; weakest add-on 43% of the strongest; average full build 9.01 Weight (before: 9.77).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostbound Grip: +6% DDG | Deepening Numbness: +9% DDG | Numbing Sapphire Feast: +5% DDG, +5% Lifesteal | +20% DDG, +5% Lifesteal |
| p2 | Sapphire Edge: +0.2 Damage | Honed Crescent: +0.4 Damage | Glacial Aegis: +5% DDT, +5% Lifesteal | +0.6 Damage, +5% DDT, +5% Lifesteal |
| p3 | Frost Mantle: +2% DDT | Hoarfrost Bulwark: +3% DDT | Glacier Unleashed: +0.4 Damage, +5% DDT | +0.4 Damage, +10% DDT |
| p4 | Hungry Rime: +2% Lifesteal | Thirst of the Frost: +3% Lifesteal | Sapphire Reveals the Flaw: +5% IDT | +5% IDT, +5% Lifesteal |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.6 Damage, +20% DDG, +5% Lifesteal
- p1 + p3: +20% DDG, +5% DDT, +5% Lifesteal
- p1 + p4: +20% DDG, +10% Lifesteal
- p2 + p1: +0.6 Damage, +15% DDG, +5% DDT, +5% Lifesteal
- p2 + p3: +0.6 Damage, +10% DDT, +5% Lifesteal
- p2 + p4: +0.6 Damage, +5% DDT, +10% Lifesteal
- p3 + p1: +0.4 Damage, +15% DDG, +10% DDT
- p3 + p2: +1 Damage, +10% DDT
- p3 + p4: +0.4 Damage, +10% DDT, +5% Lifesteal
- p4 + p1: +15% DDG, +5% IDT, +5% Lifesteal
- p4 + p2: +0.6 Damage, +5% IDT, +5% Lifesteal
- p4 + p3: +5% DDT, +5% IDT, +5% Lifesteal

Nodes whose effects changed (names need review):

- p2_t3 Glacial Aegis: +5% DDT -> +5% DDT, +5% Lifesteal
- p3_t3 Glacier Unleashed: +5% IDG -> +0.4 Damage, +5% DDT

## Cosmic Ascendant

Weakest completed path is 96% of the strongest; weakest add-on 54% of the strongest; average full build 4.71 Weight (before: 2.56).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Astral Resonance: +4% Afterburn | Resonance Cascade: +6% Afterburn | Supernova's Feast: +0.8 Damage, +10% IDG | +0.8 Damage, +10% Afterburn, +10% IDG |
| p2 | Stellar Focus: +4% IDG | Stellar Ascendance: +6% IDG | Voidburst Resonance: +10% DDT | +10% DDT, +10% IDG |
| p3 | Gravity Knot: +2% IDT | Collapsing Star: +3% IDT | Hunger of the Singularity: +5% DDG, +10% DDT | +5% DDG, +10% DDT, +5% IDT |
| p4 | Orbiting Veil: +4% DDT | Celestial Mantle: +6% DDT | Unyielding Radiance: +1.2 Damage, +10% Afterburn | +1.2 Damage, +10% Afterburn, +10% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +10% Afterburn, +20% IDG
- p1 + p3: +0.8 Damage, +10% Afterburn, +10% IDG, +5% IDT
- p1 + p4: +0.8 Damage, +10% Afterburn, +10% DDT, +10% IDG
- p2 + p1: +10% Afterburn, +10% DDT, +10% IDG
- p2 + p3: +10% DDT, +10% IDG, +5% IDT
- p2 + p4: +20% DDT, +10% IDG
- p3 + p1: +10% Afterburn, +5% DDG, +10% DDT, +5% IDT
- p3 + p2: +5% DDG, +10% DDT, +10% IDG, +5% IDT
- p3 + p4: +5% DDG, +20% DDT, +5% IDT
- p4 + p1: +1.2 Damage, +20% Afterburn, +10% DDT
- p4 + p2: +1.2 Damage, +10% Afterburn, +10% DDT, +10% IDG
- p4 + p3: +1.2 Damage, +10% Afterburn, +10% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Supernova's Feast: +5% Afterburn, +5% Lifesteal -> +0.8 Damage, +10% IDG
- p2_t3 Voidburst Resonance: +0.4 Damage, +5% Afterburn -> +10% DDT
- p3_t1 Gravity Knot: +0.4 Damage -> +2% IDT
- p3_t2 Collapsing Star: +1.2 Damage -> +3% IDT
- p3_t3 Hunger of the Singularity: +5% IDG, +5% Lifesteal -> +5% DDG, +10% DDT
- p4_t3 Unyielding Radiance: +5% DDT, +5% IDG -> +1.2 Damage, +10% Afterburn

## Crystal Essence

Weakest completed path is 94% of the strongest; weakest add-on 58% of the strongest; average full build 5.45 Weight (before: 4.39).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mirror Facet: +2% Reflect | Light Turned Back: +3% Reflect | Citadel of Returning Light: +5% Reflect | +10% Reflect |
| p2 | Jade Lattice: +4% DDT | Layered Lattice: +6% DDT | Armored Radiance: +0.8 Damage, +5% DDT | +0.8 Damage, +15% DDT |
| p3 | Prismatic Focus: +4% IDG | Radiant Convergence: +6% IDG | Shardstorm Reprisal: +0.8 Damage | +0.8 Damage, +10% IDG |
| p4 | Keen Shard: +2% IDT | Razor Shards: +3% IDT | Adamant Lance: +5% IDG | +5% IDG, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% DDT, +10% Reflect
- p1 + p3: +10% IDG, +10% Reflect
- p1 + p4: +5% IDT, +10% Reflect
- p2 + p1: +0.8 Damage, +15% DDT, +5% Reflect
- p2 + p3: +0.8 Damage, +15% DDT, +10% IDG
- p2 + p4: +0.8 Damage, +15% DDT, +5% IDT
- p3 + p1: +0.8 Damage, +10% IDG, +5% Reflect
- p3 + p2: +0.8 Damage, +10% DDT, +10% IDG
- p3 + p4: +0.8 Damage, +10% IDG, +5% IDT
- p4 + p1: +5% IDG, +5% IDT, +5% Reflect
- p4 + p2: +10% DDT, +5% IDG, +5% IDT
- p4 + p3: +15% IDG, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Citadel of Returning Light: +5% DDT, +5% Reflect -> +5% Reflect
- p2_t3 Armored Radiance: +5% DDT, +5% IDG -> +0.8 Damage, +5% DDT
- p3_t3 Shardstorm Reprisal: +0.4 Damage, +5% Reflect -> +0.8 Damage
- p4_t1 Keen Shard: +0.2 Damage -> +2% IDT
- p4_t2 Razor Shards: +0.6 Damage -> +3% IDT
- p4_t3 Adamant Lance: +0.8 Damage, +5% DDT -> +5% IDG

## Ethereal Monarch

Weakest completed path is 92% of the strongest; weakest add-on 76% of the strongest; average full build 5.07 Weight (before: 2.58).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Soul Splinter: +2% IDT | Tear in the Soul: +3% IDT | Heaven's Mirrored Crown: +1.2 Damage, +0.4 Pierce power | +1.2 Damage, +5% IDT, +0.4 Pierce power |
| p2 | Astral Veil: +6% DDT | Woven Starlight: +9% DDT | Heaven's Wardbreaker: +5% DDT, +5% Reflect | +20% DDT, +5% Reflect |
| p3 | Claimed Stardust: +6% Consume | Soulwoven Aegis: +9% Consume | Thronebreaker of Heaven: +0.4 Damage, +5% Consume | +0.4 Damage, +20% Consume |
| p4 | Ethereal Needle: +2% Afterburn | Veil-Piercing Ray: +3% Afterburn | Spoils of the Celestial Throne: +1.6 Pierce power, +10% Reflect | +5% Afterburn, +1.6 Pierce power, +10% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +15% DDT, +5% IDT, +0.4 Pierce power
- p1 + p3: +1.2 Damage, +15% Consume, +5% IDT, +0.4 Pierce power
- p1 + p4: +1.2 Damage, +5% Afterburn, +5% IDT, +0.4 Pierce power
- p2 + p1: +20% DDT, +5% IDT, +5% Reflect
- p2 + p3: +15% Consume, +20% DDT, +5% Reflect
- p2 + p4: +5% Afterburn, +20% DDT, +5% Reflect
- p3 + p1: +0.4 Damage, +20% Consume, +5% IDT
- p3 + p2: +0.4 Damage, +20% Consume, +15% DDT
- p3 + p4: +0.4 Damage, +5% Afterburn, +20% Consume
- p4 + p1: +5% Afterburn, +5% IDT, +1.6 Pierce power, +10% Reflect
- p4 + p2: +5% Afterburn, +15% DDT, +1.6 Pierce power, +10% Reflect
- p4 + p3: +5% Afterburn, +15% Consume, +1.6 Pierce power, +10% Reflect

Nodes whose effects changed (names need review):

- p1_t1 Soul Splinter: +0.2 Damage -> +2% IDT
- p1_t2 Tear in the Soul: +0.6 Damage -> +3% IDT
- p1_t3 Heaven's Mirrored Crown: +5% DDT, +5% Reflect -> +1.2 Damage, +0.4 Pierce power
- p2_t3 Heaven's Wardbreaker: +5% DDT, +3 Pierce power -> +5% DDT, +5% Reflect
- p3_t3 Thronebreaker of Heaven: +0.6 Damage, +3 Pierce power -> +0.4 Damage, +5% Consume
- p4_t1 Ethereal Needle: +2 Pierce power -> +2% Afterburn
- p4_t2 Veil-Piercing Ray: +3 Pierce power -> +3% Afterburn
- p4_t3 Spoils of the Celestial Throne: +0.4 Damage, +5% Consume -> +1.6 Pierce power, +10% Reflect

## Eyes of the Forsaken King

Weakest completed path is 87% of the strongest; weakest add-on 57% of the strongest; average full build 5.24 Weight (before: 3.78).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Tarnished Edge: +0.2 Damage | Edge of the Regalia: +0.8 Damage | Throne of Broken Light: +10% IDG, +10% Reflect | +1 Damage, +10% IDG, +10% Reflect |
| p2 | Exile's Mantle: +4% Reflect | Halo of the Unbowed: +6% Reflect | Judgment of the Forsaken: +5% Afterburn | +5% Afterburn, +10% Reflect |
| p3 | Royal Resolve: +4% IDG | Radiant Decree: +6% IDG | Kingdom of One: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +10% IDG |
| p4 | Brand of Exile: +2% Afterburn | Condemnation in Light: +3% Afterburn | Usurper's Reckoning: +5% DDT, +5% Reflect | +5% Afterburn, +5% DDT, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +10% IDG, +20% Reflect
- p1 + p3: +1 Damage, +20% IDG, +10% Reflect
- p1 + p4: +1 Damage, +5% Afterburn, +10% IDG, +10% Reflect
- p2 + p1: +1 Damage, +5% Afterburn, +10% Reflect
- p2 + p3: +5% Afterburn, +10% IDG, +10% Reflect
- p2 + p4: +10% Afterburn, +10% Reflect
- p3 + p1: +1.4 Damage, +5% Afterburn, +10% IDG
- p3 + p2: +0.4 Damage, +5% Afterburn, +10% IDG, +10% Reflect
- p3 + p4: +0.4 Damage, +10% Afterburn, +10% IDG
- p4 + p1: +1 Damage, +5% Afterburn, +5% DDT, +5% Reflect
- p4 + p2: +5% Afterburn, +5% DDT, +15% Reflect
- p4 + p3: +5% Afterburn, +5% DDT, +10% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Throne of Broken Light: +5% IDG -> +10% IDG, +10% Reflect
- p2_t1 Exile's Mantle: +2% DDT -> +4% Reflect
- p2_t2 Halo of the Unbowed: +3% DDT -> +6% Reflect
- p2_t3 Judgment of the Forsaken: +0.4 Damage, +5% Afterburn -> +5% Afterburn
- p3_t3 Kingdom of One: +0.6 Damage, +5% Reflect -> +0.4 Damage, +5% Afterburn

## Heavenly Sonata

Weakest completed path is 100% of the strongest; weakest add-on 61% of the strongest; average full build 4.76 Weight (before: 2.77).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Opening Measure: +6% IDG | Rising Crescendo: +9% IDG | Discordant Sanctuary: +5% DDG, +5% IDG | +5% DDG, +20% IDG |
| p2 | Striking Note: +6% DDT | Dissonant Chord: +9% DDT | Sanctuary of Waning Breath: +0.4 Damage, +5% IDT | +0.4 Damage, +15% DDT, +5% IDT |
| p3 | Fracturing Tone: +6% IDT | Unraveling Harmony: +9% IDT | Anthem of Ascendancy: +5% DDT, +5% IDT | +5% DDT, +20% IDT |
| p4 | Muted Note: +6% DDG | Muted Strings: +9% DDG | Dirge of Dwindling Strength: +0.4 Damage, +5% IDG | +0.4 Damage, +15% DDG, +5% IDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% DDG, +15% DDT, +20% IDG
- p1 + p3: +5% DDG, +20% IDG, +15% IDT
- p1 + p4: +20% DDG, +20% IDG
- p2 + p1: +0.4 Damage, +15% DDT, +15% IDG, +5% IDT
- p2 + p3: +0.4 Damage, +15% DDT, +20% IDT
- p2 + p4: +0.4 Damage, +15% DDG, +15% DDT, +5% IDT
- p3 + p1: +5% DDT, +15% IDG, +20% IDT
- p3 + p2: +20% DDT, +20% IDT
- p3 + p4: +15% DDG, +5% DDT, +20% IDT
- p4 + p1: +0.4 Damage, +15% DDG, +20% IDG
- p4 + p2: +0.4 Damage, +15% DDG, +15% DDT, +5% IDG
- p4 + p3: +0.4 Damage, +15% DDG, +5% IDG, +15% IDT

Nodes whose effects changed (names need review):

- p1_t3 Discordant Sanctuary: +5% DDT, +5% IDT -> +5% DDG, +5% IDG
- p2_t1 Striking Note: +0.4 Damage -> +6% DDT
- p2_t2 Dissonant Chord: +1.2 Damage -> +9% DDT
- p2_t3 Sanctuary of Waning Breath: +5% DDT, +25 Drain -> +0.4 Damage, +5% IDT
- p3_t3 Anthem of Ascendancy: +5% DDG, +5% IDG -> +5% DDT, +5% IDT
- p4_t3 Dirge of Dwindling Strength: +5% DDG, +25 Drain -> +0.4 Damage, +5% IDG

## Houkyuken

Weakest completed path is 91% of the strongest; weakest add-on 61% of the strongest; average full build 5.11 Weight (before: 5.46).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Lodestone Knuckle: +2% IDT | Polarized Fist: +3% IDT | Starfall Hammer: +0.6 Damage, +5% Reflect | +0.6 Damage, +5% IDT, +5% Reflect |
| p2 | Repelling Field: +2% DDT | Reversed Polarity: +3% DDT | Inexorable Pull: +5% Reflect | +5% DDT, +5% Reflect |
| p3 | Aligned Force: +2% IDG | Lodestone Resonance: +3% IDG | Aegis of Reversed Force: +5% IDG | +10% IDG |
| p4 | Rebounding Field: +2% Reflect | Like Poles Repel: +3% Reflect | Violent Repulsion: +0.4 Damage, +5% IDG | +0.4 Damage, +5% IDG, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.6 Damage, +5% DDT, +5% IDT, +5% Reflect
- p1 + p3: +0.6 Damage, +5% IDG, +5% IDT, +5% Reflect
- p1 + p4: +0.6 Damage, +5% IDT, +10% Reflect
- p2 + p1: +5% DDT, +5% IDT, +5% Reflect
- p2 + p3: +5% DDT, +5% IDG, +5% Reflect
- p2 + p4: +5% DDT, +10% Reflect
- p3 + p1: +10% IDG, +5% IDT
- p3 + p2: +5% DDT, +10% IDG
- p3 + p4: +10% IDG, +5% Reflect
- p4 + p1: +0.4 Damage, +5% IDG, +5% IDT, +5% Reflect
- p4 + p2: +0.4 Damage, +5% DDT, +5% IDG, +5% Reflect
- p4 + p3: +0.4 Damage, +10% IDG, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t1 Lodestone Knuckle: +0.2 Damage -> +2% IDT
- p1_t2 Polarized Fist: +0.4 Damage -> +3% IDT
- p1_t3 Starfall Hammer: +0.6 Damage, +5% IDG -> +0.6 Damage, +5% Reflect
- p2_t3 Inexorable Pull: +0.4 Damage, +5% IDT -> +5% Reflect
- p3_t3 Aegis of Reversed Force: +5% DDT, +5% Reflect -> +5% IDG
- p4_t3 Violent Repulsion: +5% IDT, +5% Reflect -> +0.4 Damage, +5% IDG

## Hyouga Yui

Weakest completed path is 80% of the strongest; weakest add-on 43% of the strongest; average full build 5.28 Weight (before: 6.94).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Rime Shell: +2% DDT | Glacial Rampart: +3% DDT | Avalanche Bastion: +0.4 Damage | +0.4 Damage, +5% DDT |
| p2 | Purgatory's Chill: +2% IDG | Deepening Frost: +3% IDG | The Glacier Advances: +0.4 Damage, +5% IDT | +0.4 Damage, +5% IDG, +5% IDT |
| p3 | Icebound Point: +0.4 Damage | Glacial Fang: +0.8 Damage | Spear Behind the Icewall: +5% DDT | +1.2 Damage, +5% DDT |
| p4 | Brittle Rime: +2% IDT | Purgatory's Fracture: +3% IDT | Bastion of Broken Ice: +5% IDT | +10% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.4 Damage, +5% DDT, +5% IDG
- p1 + p3: +1.6 Damage, +5% DDT
- p1 + p4: +0.4 Damage, +5% DDT, +5% IDT
- p2 + p1: +0.4 Damage, +5% DDT, +5% IDG, +5% IDT
- p2 + p3: +1.6 Damage, +5% IDG, +5% IDT
- p2 + p4: +0.4 Damage, +5% IDG, +10% IDT
- p3 + p1: +1.2 Damage, +10% DDT
- p3 + p2: +1.2 Damage, +5% DDT, +5% IDG
- p3 + p4: +1.2 Damage, +5% DDT, +5% IDT
- p4 + p1: +5% DDT, +10% IDT
- p4 + p2: +5% IDG, +10% IDT
- p4 + p3: +1.2 Damage, +10% IDT

Nodes whose effects changed (names need review):

- p1_t3 Avalanche Bastion: +5% DDT, +5% IDG -> +0.4 Damage
- p3_t3 Spear Behind the Icewall: +0.8 Damage, +5% DDT -> +5% DDT
- p4_t3 Bastion of Broken Ice: +5% DDT, +5% IDT -> +5% IDT

## Itojinsei

Weakest completed path is 82% of the strongest; weakest add-on 51% of the strongest; average full build 5.12 Weight (before: 3.79).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Exposing Thread: +4% IDT | Razor Strands: +6% IDT | Severing Lattice: +10% IDT | +20% IDT |
| p2 | Taut Filament: +2% IDG | Threadbound Vigor: +3% IDG | Weaver Ascendant: +5% IDG | +10% IDG |
| p3 | Wire Edge: +0.2 Damage | Keen Filament: +0.8 Damage | The Severing Thread: +5% IDG, +5% IDT | +1 Damage, +5% IDG, +5% IDT |
| p4 | Tightening Snare: +2% DDG | Constricting Coils: +3% DDG | Iron Stranglehold: +5% DDG | +10% DDG |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +5% IDG, +20% IDT
- p1 + p3: +1 Damage, +20% IDT
- p1 + p4: +5% DDG, +20% IDT
- p2 + p1: +10% IDG, +10% IDT
- p2 + p3: +1 Damage, +10% IDG
- p2 + p4: +5% DDG, +10% IDG
- p3 + p1: +1 Damage, +5% IDG, +15% IDT
- p3 + p2: +1 Damage, +10% IDG, +5% IDT
- p3 + p4: +1 Damage, +5% DDG, +5% IDG, +5% IDT
- p4 + p1: +10% DDG, +10% IDT
- p4 + p2: +10% DDG, +5% IDG
- p4 + p3: +1 Damage, +10% DDG

Nodes whose effects changed (names need review):

- p3_t3 The Severing Thread: +0.6 Damage -> +5% IDG, +5% IDT

## Kyuko-sei

Weakest completed path is 84% of the strongest; weakest add-on 59% of the strongest; average full build 6.55 Weight (before: 7.97).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Dense Starmote: +2% IDG | Shattered Firmament: +3% IDG | Mantle of the Dying Star: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% IDG |
| p2 | Fading Force: +6% DDG | Entropic Weakening: +9% DDG | Frailty of Ages: +5% DDG | +20% DDG |
| p3 | Dust Shroud: +2% DDT | Aeonic Mantle: +3% DDT | Sanctuary of Erosion: +5% DDT | +10% DDT |
| p4 | Eroded Seam: +2% IDT | Crumbling Firmament: +3% IDT | Dominion of Entropy: +0.6 Damage | +0.6 Damage, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.4 Damage, +20% DDG, +5% IDG
- p1 + p3: +0.4 Damage, +5% DDG, +5% DDT, +5% IDG
- p1 + p4: +0.4 Damage, +5% DDG, +5% IDG, +5% IDT
- p2 + p1: +20% DDG, +5% IDG
- p2 + p3: +20% DDG, +5% DDT
- p2 + p4: +20% DDG, +5% IDT
- p3 + p1: +10% DDT, +5% IDG
- p3 + p2: +15% DDG, +10% DDT
- p3 + p4: +10% DDT, +5% IDT
- p4 + p1: +0.6 Damage, +5% IDG, +5% IDT
- p4 + p2: +0.6 Damage, +15% DDG, +5% IDT
- p4 + p3: +0.6 Damage, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t1 Dense Starmote: +0.2 Damage -> +2% IDG
- p1_t2 Shattered Firmament: +0.6 Damage -> +3% IDG
- p1_t3 Mantle of the Dying Star: +5% DDT, +5% IDG -> +0.4 Damage, +5% DDG
- p2_t3 Frailty of Ages: +5% DDG, +5% IDT -> +5% DDG
- p3_t3 Sanctuary of Erosion: +5% DDT, +5% IDT -> +5% DDT
- p4_t3 Dominion of Entropy: +5% DDG, +5% IDG -> +0.6 Damage

## Oblivion Seal

Weakest completed path is 97% of the strongest; weakest add-on 81% of the strongest; average full build 4.79 Weight (before: 4.16).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Umbral Vigor: +2% IDG | Umbral Claws: +3% IDG | Absolute Erasure: +0.6 Damage, +10% Lifesteal | +0.6 Damage, +5% IDG, +10% Lifesteal |
| p2 | Eroding Curse: +2% Lifesteal | Shadow-Laid Fracture: +3% Lifesteal | Brand of Oblivion: +10% IDG, +1.6 Pierce power | +10% IDG, +5% Lifesteal, +1.6 Pierce power |
| p3 | Void Needle: +4% DDT | Wardrending Shade: +6% DDT | Sanguine Seal of Shelter: +0.6 Damage, +10% IDG | +0.6 Damage, +10% DDT, +10% IDG |
| p4 | Darkened Edge: +0.4 Damage | Rending Sigil: +0.6 Damage | Wardbreaker in Shadow: +10% Lifesteal, +1.6 Pierce power | +1 Damage, +10% Lifesteal, +1.6 Pierce power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.6 Damage, +5% IDG, +15% Lifesteal
- p1 + p3: +0.6 Damage, +10% DDT, +5% IDG, +10% Lifesteal
- p1 + p4: +1.6 Damage, +5% IDG, +10% Lifesteal
- p2 + p1: +15% IDG, +5% Lifesteal, +1.6 Pierce power
- p2 + p3: +10% DDT, +10% IDG, +5% Lifesteal, +1.6 Pierce power
- p2 + p4: +1 Damage, +10% IDG, +5% Lifesteal, +1.6 Pierce power
- p3 + p1: +0.6 Damage, +10% DDT, +15% IDG
- p3 + p2: +0.6 Damage, +10% DDT, +10% IDG, +5% Lifesteal
- p3 + p4: +1.6 Damage, +10% DDT, +10% IDG
- p4 + p1: +1 Damage, +5% IDG, +10% Lifesteal, +1.6 Pierce power
- p4 + p2: +1 Damage, +15% Lifesteal, +1.6 Pierce power
- p4 + p3: +1 Damage, +10% DDT, +10% Lifesteal, +1.6 Pierce power

Nodes whose effects changed (names need review):

- p1_t3 Absolute Erasure: +5% IDG, +0.4 Pierce power -> +0.6 Damage, +10% Lifesteal
- p2_t1 Eroding Curse: +2% IDT -> +2% Lifesteal
- p2_t2 Shadow-Laid Fracture: +3% IDT -> +3% Lifesteal
- p2_t3 Brand of Oblivion: +5% IDT -> +10% IDG, +1.6 Pierce power
- p3_t1 Void Needle: +2 Pierce power -> +4% DDT
- p3_t2 Wardrending Shade: +3 Pierce power -> +6% DDT
- p3_t3 Sanguine Seal of Shelter: +5% DDT, +5% Lifesteal -> +0.6 Damage, +10% IDG
- p4_t3 Wardbreaker in Shadow: +5% DDT, +2 Pierce power -> +10% Lifesteal, +1.6 Pierce power

## Shadow Weaver

Weakest completed path is 93% of the strongest; weakest add-on 44% of the strongest; average full build 4.81 Weight (before: 3.75).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sharpened Shadow: +0.2 Damage | Barbed Thread: +0.8 Damage | Night Unraveled: +5% IDG | +1 Damage, +5% IDG |
| p2 | Tension in the Dark: +2% IDG | Empowered Stitch: +3% IDG | A Thousand Striking Threads: +5% DDG | +5% DDG, +5% IDG |
| p3 | Dampening Thread: +4% DDG | Frayed Resolve: +6% DDG | Strings Cut Short: +5% DDT | +10% DDG, +5% DDT |
| p4 | Warding Stitch: +2% DDT | Tightened Weave: +3% DDT | Seamless Shroud: +5% DDG, +5% DDT | +5% DDG, +10% DDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1 Damage, +10% IDG
- p1 + p3: +1 Damage, +10% DDG, +5% IDG
- p1 + p4: +1 Damage, +5% DDT, +5% IDG
- p2 + p1: +1 Damage, +5% DDG, +5% IDG
- p2 + p3: +15% DDG, +5% IDG
- p2 + p4: +5% DDG, +5% DDT, +5% IDG
- p3 + p1: +1 Damage, +10% DDG, +5% DDT
- p3 + p2: +10% DDG, +5% DDT, +5% IDG
- p3 + p4: +10% DDG, +10% DDT
- p4 + p1: +1 Damage, +5% DDG, +10% DDT
- p4 + p2: +5% DDG, +10% DDT, +5% IDG
- p4 + p3: +15% DDG, +10% DDT

Nodes whose effects changed (names need review):

- p1_t3 Night Unraveled: +0.6 Damage -> +5% IDG
- p2_t3 A Thousand Striking Threads: +5% IDG -> +5% DDG
- p3_t3 Strings Cut Short: +5% DDG -> +5% DDT
- p4_t3 Seamless Shroud: +5% DDT -> +5% DDG, +5% DDT

## Shakunetsu Sakura

Weakest completed path is 92% of the strongest; weakest add-on 68% of the strongest; average full build 5.74 Weight (before: 5.00).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Kindled Bud: +4% IDG | Kindled Boughs: +6% IDG | Dragon in Full Blossom: +5% IDG | +15% IDG |
| p2 | Petal Needle: +2% IDT | Blossom Through Iron: +3% IDT | Scorching Hanami: +5 Heal power | +5 Heal power, +5% IDT |
| p3 | Restoring Bud: +2 Heal power | Mending Petal Rain: +3 Heal power | Dragon's Wardrending Bloom: +5% IDG, +0.4 Pierce power | +5 Heal power, +5% IDG, +0.4 Pierce power |
| p4 | Scorching Petal: +4% DDG | Blazing Petal Torrent: +6% DDG | Oppressive Dragon's Breath: +0.4 Damage, +1.6 Pierce power | +0.4 Damage, +10% DDG, +1.6 Pierce power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +15% IDG, +5% IDT
- p1 + p3: +5 Heal power, +15% IDG
- p1 + p4: +10% DDG, +15% IDG
- p2 + p1: +5 Heal power, +10% IDG, +5% IDT
- p2 + p3: +10 Heal power, +5% IDT
- p2 + p4: +10% DDG, +5 Heal power, +5% IDT
- p3 + p1: +5 Heal power, +15% IDG, +0.4 Pierce power
- p3 + p2: +5 Heal power, +5% IDG, +5% IDT, +0.4 Pierce power
- p3 + p4: +10% DDG, +5 Heal power, +5% IDG, +0.4 Pierce power
- p4 + p1: +0.4 Damage, +10% DDG, +10% IDG, +1.6 Pierce power
- p4 + p2: +0.4 Damage, +10% DDG, +5% IDT, +1.6 Pierce power
- p4 + p3: +0.4 Damage, +10% DDG, +5 Heal power, +1.6 Pierce power

Nodes whose effects changed (names need review):

- p1_t3 Dragon in Full Blossom: +0.4 Damage, +5% IDG -> +5% IDG
- p2_t1 Petal Needle: +2 Pierce power -> +2% IDT
- p2_t2 Blossom Through Iron: +3 Pierce power -> +3% IDT
- p2_t3 Scorching Hanami: +5 Pierce power -> +5 Heal power
- p4_t1 Scorching Petal: +0.6 Damage -> +4% DDG
- p4_t2 Blazing Petal Torrent: +1.2 Damage -> +6% DDG
- p4_t3 Oppressive Dragon's Breath: +5% DDG, +2 Pierce power -> +0.4 Damage, +1.6 Pierce power

## Shinrai Ou

Weakest completed path is 93% of the strongest; weakest add-on 25% of the strongest; average full build 5.93 Weight (before: 5.56).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Vajra Spark: +0.2 Damage | Vajra Tempering: +0.6 Damage | Thunder King's Wrath: +5% IDT, +5% Reflect | +0.8 Damage, +5% IDT, +5% Reflect |
| p2 | Gathering Voltage: +2% IDG | Crown of Lightning: +3% IDG | Judgement from Above: +0.4 Damage | +0.4 Damage, +5% IDG |
| p3 | Echoing Spark: +2% Reflect | Returning Thunder: +3% Reflect | Heaven's Reprisal: +0.4 Damage, +5% Reflect | +0.4 Damage, +10% Reflect |
| p4 | Conductive Flaw: +2% IDT | Storm-Laid Fracture: +3% IDT | Thunder King's Condemnation: +0.4 Damage, +10% IDT | +0.4 Damage, +15% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% IDG, +5% IDT, +5% Reflect
- p1 + p3: +0.8 Damage, +5% IDT, +10% Reflect
- p1 + p4: +0.8 Damage, +10% IDT, +5% Reflect
- p2 + p1: +1.2 Damage, +5% IDG
- p2 + p3: +0.4 Damage, +5% IDG, +5% Reflect
- p2 + p4: +0.4 Damage, +5% IDG, +5% IDT
- p3 + p1: +1.2 Damage, +10% Reflect
- p3 + p2: +0.4 Damage, +5% IDG, +10% Reflect
- p3 + p4: +0.4 Damage, +5% IDT, +10% Reflect
- p4 + p1: +1.2 Damage, +15% IDT
- p4 + p2: +0.4 Damage, +5% IDG, +15% IDT
- p4 + p3: +0.4 Damage, +15% IDT, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t3 Thunder King's Wrath: +0.6 Damage -> +5% IDT, +5% Reflect
- p2_t3 Judgement from Above: +5% IDG -> +0.4 Damage
- p3_t3 Heaven's Reprisal: +5% Reflect -> +0.4 Damage, +5% Reflect
- p4_t3 Thunder King's Condemnation: +5% IDT -> +0.4 Damage, +10% IDT

## Shinseina Ki

Weakest completed path is 64% of the strongest; weakest add-on 26% of the strongest; average full build 5.90 Weight (before: 7.98).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Heartwood Edge: +0.2 Damage | Tempered Heartwood: +0.6 Damage | Sundering Heartwood: +5% IDT | +0.8 Damage, +5% IDT |
| p2 | Sapborne Vigor: +2% IDG | Fangs of Heartwood: +3% IDG | The Forest Strikes: +5% Poison | +5% IDG, +5% Poison |
| p3 | Exposing Root: +2% IDT | Rootbound Prey: +3% IDT | Venomous Judgment of the Grove: +0.6 Damage | +0.6 Damage, +5% IDT |
| p4 | Bitter Sap: +6% Poison | Burden of the Bitter Boughs: +9% Poison | Dominion of the Venomwood: +5% IDT, +5% Poison | +5% IDT, +20% Poison |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% IDG, +5% IDT
- p1 + p3: +0.8 Damage, +10% IDT
- p1 + p4: +0.8 Damage, +5% IDT, +15% Poison
- p2 + p1: +0.8 Damage, +5% IDG, +5% Poison
- p2 + p3: +5% IDG, +5% IDT, +5% Poison
- p2 + p4: +5% IDG, +20% Poison
- p3 + p1: +1.4 Damage, +5% IDT
- p3 + p2: +0.6 Damage, +5% IDG, +5% IDT
- p3 + p4: +0.6 Damage, +5% IDT, +15% Poison
- p4 + p1: +0.8 Damage, +5% IDT, +20% Poison
- p4 + p2: +5% IDG, +5% IDT, +20% Poison
- p4 + p3: +10% IDT, +20% Poison

Nodes whose effects changed (names need review):

- p1_t3 Sundering Heartwood: +0.8 Damage, +5% IDT -> +5% IDT
- p2_t3 The Forest Strikes: +0.4 Damage, +5% IDG -> +5% Poison
- p3_t3 Venomous Judgment of the Grove: +5% IDT, +5% Poison -> +0.6 Damage
- p4_t3 Dominion of the Venomwood: +5% IDG, +5% Poison -> +5% IDT, +5% Poison

## Shiroi Youso

Unchanged. Fewer than four eligible root effects for four distinct paths (eligible: Afterburn, DDT, Heal). Needs its element decided first.


## Suragu

Weakest completed path is 93% of the strongest; weakest add-on 76% of the strongest; average full build 4.97 Weight (before: 5.11).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Molten Needle: +4% DDT | Slagbreaker: +6% DDT | Feast of the Resonant Caldera: +5% IDT | +10% DDT, +5% IDT |
| p2 | Softened Crust: +2% IDT | Fractured Slag: +3% IDT | Venomous Feast of the Mountain: +5% Lifesteal, +5% Poison | +5% IDT, +5% Lifesteal, +5% Poison |
| p3 | Hungry Ember: +2% Lifesteal | Molten Draught: +3% Lifesteal | Heart of the Caldera: +0.4 Damage, +5% IDG | +0.4 Damage, +5% IDG, +5% Lifesteal |
| p4 | Stoked Furnace: +2% IDG | Magmatic Surge: +3% IDG | Wardrending Hunger: +5% Lifesteal, +0.4 Pierce power | +5% IDG, +5% Lifesteal, +0.4 Pierce power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% DDT, +10% IDT
- p1 + p3: +10% DDT, +5% IDT, +5% Lifesteal
- p1 + p4: +10% DDT, +5% IDG, +5% IDT
- p2 + p1: +10% DDT, +5% IDT, +5% Lifesteal, +5% Poison
- p2 + p3: +5% IDT, +10% Lifesteal, +5% Poison
- p2 + p4: +5% IDG, +5% IDT, +5% Lifesteal, +5% Poison
- p3 + p1: +0.4 Damage, +10% DDT, +5% IDG, +5% Lifesteal
- p3 + p2: +0.4 Damage, +5% IDG, +5% IDT, +5% Lifesteal
- p3 + p4: +0.4 Damage, +10% IDG, +5% Lifesteal
- p4 + p1: +10% DDT, +5% IDG, +5% Lifesteal, +0.4 Pierce power
- p4 + p2: +5% IDG, +5% IDT, +5% Lifesteal, +0.4 Pierce power
- p4 + p3: +5% IDG, +10% Lifesteal, +0.4 Pierce power

Nodes whose effects changed (names need review):

- p1_t1 Molten Needle: +2 Pierce power -> +4% DDT
- p1_t2 Slagbreaker: +3 Pierce power -> +6% DDT
- p1_t3 Feast of the Resonant Caldera: +5% Afterburn, +5% Lifesteal -> +5% IDT
- p3_t3 Heart of the Caldera: +5% DDT, +5% Lifesteal -> +0.4 Damage, +5% IDG

## Taiyo Kami

Weakest completed path is 95% of the strongest; weakest add-on 76% of the strongest; average full build 4.77 Weight (before: 4.51).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Breaking Point: +2% IDG | Crown of Cinders: +3% IDG | Solar Cataclysm: +0.8 Damage, +5% DDG | +0.8 Damage, +5% DDG, +5% IDG |
| p2 | Ember Seed: +2% IDT | Emberwake: +3% IDT | Eternal Noon: +10% IDG | +10% IDG, +5% IDT |
| p3 | Dawnward: +2% DDT | Golden Mantle: +3% DDT | Sovereign Sun: +0.4 Damage, +5% DDT | +0.4 Damage, +10% DDT |
| p4 | Dawnheart: +2% DDG | Heart of the Sun: +3% DDG | Zenith Incarnate: +0.6 Damage, +5% IDT | +0.6 Damage, +5% DDG, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +0.8 Damage, +5% DDG, +5% IDG, +5% IDT
- p1 + p3: +0.8 Damage, +5% DDG, +5% DDT, +5% IDG
- p1 + p4: +0.8 Damage, +10% DDG, +5% IDG
- p2 + p1: +15% IDG, +5% IDT
- p2 + p3: +5% DDT, +10% IDG, +5% IDT
- p2 + p4: +5% DDG, +10% IDG, +5% IDT
- p3 + p1: +0.4 Damage, +10% DDT, +5% IDG
- p3 + p2: +0.4 Damage, +10% DDT, +5% IDT
- p3 + p4: +0.4 Damage, +5% DDG, +10% DDT
- p4 + p1: +0.6 Damage, +5% DDG, +5% IDG, +5% IDT
- p4 + p2: +0.6 Damage, +5% DDG, +10% IDT
- p4 + p3: +0.6 Damage, +5% DDG, +5% DDT, +5% IDT

Nodes whose effects changed (names need review):

- p1_t1 Breaking Point: +0.2 Damage -> +2% IDG
- p1_t2 Crown of Cinders: +0.6 Damage -> +3% IDG
- p2_t1 Ember Seed: +2% Afterburn -> +2% IDT
- p2_t2 Emberwake: +3% Afterburn -> +3% IDT
- p2_t3 Eternal Noon: +0.8 Damage, +5% DDT -> +10% IDG
- p3_t3 Sovereign Sun: +0.4 Damage, +5% IDT -> +0.4 Damage, +5% DDT
- p4_t3 Zenith Incarnate: +5% Afterburn, +5% DDG -> +0.6 Damage, +5% IDT

## Teno Yuki

Weakest completed path is 96% of the strongest; weakest add-on 84% of the strongest; average full build 4.88 Weight (before: 3.46).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostborne Vigor: +2% IDG | Killing Frost: +3% IDG | Hunger of the Winter Crown: +5% IDG, +10% IDT | +10% IDG, +10% IDT |
| p2 | Ice Splinter: +2% IDT | Glacial Lance: +3% IDT | Palace of Consuming Ice: +1.2 Damage, +10% IDG | +1.2 Damage, +10% IDG, +5% IDT |
| p3 | Snowbound Mantle: +6% DDT | Permafrost Mantle: +9% DDT | Winter's Sheltering Verdict: +1.2 Damage, +10% IDT | +1.2 Damage, +15% DDT, +10% IDT |
| p4 | Siphoning Snow: +2% Absorb | Ravenous Snowfall: +3% Absorb | Winter's Exposing Command: +0.8 Damage, +5 Heal power | +0.8 Damage, +5% Absorb, +5 Heal power |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +10% IDG, +15% IDT
- p1 + p3: +15% DDT, +10% IDG, +10% IDT
- p1 + p4: +5% Absorb, +10% IDG, +10% IDT
- p2 + p1: +1.2 Damage, +15% IDG, +5% IDT
- p2 + p3: +1.2 Damage, +15% DDT, +10% IDG, +5% IDT
- p2 + p4: +1.2 Damage, +5% Absorb, +10% IDG, +5% IDT
- p3 + p1: +1.2 Damage, +15% DDT, +5% IDG, +10% IDT
- p3 + p2: +1.2 Damage, +15% DDT, +15% IDT
- p3 + p4: +1.2 Damage, +5% Absorb, +15% DDT, +10% IDT
- p4 + p1: +0.8 Damage, +5% Absorb, +5 Heal power, +5% IDG
- p4 + p2: +0.8 Damage, +5% Absorb, +5 Heal power, +5% IDT
- p4 + p3: +0.8 Damage, +5% Absorb, +15% DDT, +5 Heal power

Nodes whose effects changed (names need review):

- p1_t3 Hunger of the Winter Crown: +5% Absorb, +5% IDG -> +5% IDG, +10% IDT
- p2_t1 Ice Splinter: +0.2 Damage -> +2% IDT
- p2_t2 Glacial Lance: +1.2 Damage -> +3% IDT
- p2_t3 Palace of Consuming Ice: +5% Absorb, +5% DDT -> +1.2 Damage, +10% IDG
- p3_t3 Winter's Sheltering Verdict: +5% DDT, +5% IDT -> +1.2 Damage, +10% IDT
- p4_t3 Winter's Exposing Command: +5% IDG, +5% IDT -> +0.8 Damage, +5 Heal power

## Tenohira Musei

Weakest completed path is 86% of the strongest; weakest add-on 47% of the strongest; average full build 5.82 Weight (before: 7.75).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Quieting Touch: +4% DDG | Silencing Pressure: +6% DDG | Hushed Ruin: +5% DDG | +15% DDG |
| p2 | Gathered Palm: +0.4 Damage | Condensed Force: +0.8 Damage | Tipping the Balance: +5% IDG | +1.2 Damage, +5% IDG |
| p3 | Centered Intent: +2% IDG | Gathered Force: +3% IDG | The Silent Impact: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% IDG |
| p4 | Exposing Palm: +2% IDT | Fracture in Stillness: +3% IDT | Eclipse in Hand: +0.4 Damage | +0.4 Damage, +5% IDT |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +15% DDG
- p1 + p3: +15% DDG, +5% IDG
- p1 + p4: +15% DDG, +5% IDT
- p2 + p1: +1.2 Damage, +10% DDG, +5% IDG
- p2 + p3: +1.2 Damage, +10% IDG
- p2 + p4: +1.2 Damage, +5% IDG, +5% IDT
- p3 + p1: +0.4 Damage, +15% DDG, +5% IDG
- p3 + p2: +1.6 Damage, +5% DDG, +5% IDG
- p3 + p4: +0.4 Damage, +5% DDG, +5% IDG, +5% IDT
- p4 + p1: +0.4 Damage, +10% DDG, +5% IDT
- p4 + p2: +1.6 Damage, +5% IDT
- p4 + p3: +0.4 Damage, +5% IDG, +5% IDT

Nodes whose effects changed (names need review):

- p1_t3 Hushed Ruin: +5% DDG, +5% IDT -> +5% DDG
- p2_t3 Tipping the Balance: +5% DDG, +5% IDG -> +5% IDG
- p3_t3 The Silent Impact: +5% IDG, +5% IDT -> +0.4 Damage, +5% DDG
- p4_t3 Eclipse in Hand: +0.4 Damage, +5% IDT -> +0.4 Damage

## Vaporia

Weakest completed path is 95% of the strongest; weakest add-on 86% of the strongest; average full build 5.30 Weight (before: 5.48).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mending Vapor: +2% IDG | Restorative Mist: +3% IDG | Scald-Laid Weakness: +5% IDG | +10% IDG |
| p2 | Pressurized Drop: +0.4 Damage | Geyser Fist: +0.8 Damage | Steamclad Wardbreaker: +5% IDT | +1.2 Damage, +5% IDT |
| p3 | Resonant Heat: +2% Afterburn | Scalding Resonance: +3% Afterburn | Bastion of Returning Steam: +5% IDT, +0.4 Pierce power | +5% Afterburn, +5% IDT, +0.4 Pierce power |
| p4 | Scalded Seam: +2% IDT | Deepening Scald: +3% IDT | Dragon's Siphoning Fang: +5% DDT, +5% Reflect | +5% DDT, +5% IDT, +5% Reflect |

5-BP builds (completed path + another path's Foundation and Hidden Art):

- p1 + p2: +1.2 Damage, +10% IDG
- p1 + p3: +5% Afterburn, +10% IDG
- p1 + p4: +10% IDG, +5% IDT
- p2 + p1: +1.2 Damage, +5% IDG, +5% IDT
- p2 + p3: +1.2 Damage, +5% Afterburn, +5% IDT
- p2 + p4: +1.2 Damage, +10% IDT
- p3 + p1: +5% Afterburn, +5% IDG, +5% IDT, +0.4 Pierce power
- p3 + p2: +1.2 Damage, +5% Afterburn, +5% IDT, +0.4 Pierce power
- p3 + p4: +5% Afterburn, +10% IDT, +0.4 Pierce power
- p4 + p1: +5% DDT, +5% IDG, +5% IDT, +5% Reflect
- p4 + p2: +1.2 Damage, +5% DDT, +5% IDT, +5% Reflect
- p4 + p3: +5% Afterburn, +5% DDT, +5% IDT, +5% Reflect

Nodes whose effects changed (names need review):

- p1_t1 Mending Vapor: +2 Heal power -> +2% IDG
- p1_t2 Restorative Mist: +3 Heal power -> +3% IDG
- p1_t3 Scald-Laid Weakness: +5% IDT -> +5% IDG
- p2_t3 Steamclad Wardbreaker: +5% DDT, +5 Pierce power -> +5% IDT
- p3_t3 Bastion of Returning Steam: +5% DDT, +5% Reflect -> +5% IDT, +0.4 Pierce power
- p4_t3 Dragon's Siphoning Fang: +5% Lifesteal, +2 Pierce power -> +5% DDT, +5% Reflect
