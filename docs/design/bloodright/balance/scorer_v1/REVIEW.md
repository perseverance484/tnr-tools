# Bloodright rebalance (scorer v1)

Cumulative Bloodright bonuses per build, prerequisites included (RUL-2026-10-18-001 presentation). Weight = seven-round HP-equivalent value / 50.5 (1 = 1% of a level-100 health pool), scored by `scripts/bloodright_balance/` against a mirror of the kit. Pierce and Heal bonuses are flat power: +5 Pierce adds 5 power to each pierce hit, +5 Heal adds 50 HP per heal tick.

Strength target: an average full build of 5.24 Weight, today's Bloodright power level (the roster median of the round-totals rules without a strength pull). Rules (RUL-2026-10-19-001): every finished build totals a multiple of 5 for each percentage effect (at most 20), paths step +2/+3, +4/+6 or +6/+9, capstones +5 or +10; Damage and Pierce use clean power steps.


## Aerathiel

Weakest completed path is 91% of the strongest; weakest add-on 53% of the strongest; average full build 5.81 Weight (before: 6.45).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Withering Breath: +2% DDG | Strength to Dust: +3% DDG | Dust Devil's Backlash: +0.4 Damage, +5% Reflect | +0.4 Damage, +5% DDG, +5% Reflect |
| p2 | Eroding Touch: +2% IDT | Particulate Fracture: +3% IDT | Atomic Reprisal: +5% Reflect | +5% IDT, +5% Reflect |
| p3 | Sharpened Grit: +2% IDG | Scouring Gale: +3% IDG | Particle Annihilation: +1.2 Damage | +1.2 Damage, +5% IDG |
| p4 | Rebounding Motes: +2% Reflect | Returning Gale: +3% Reflect | Enervating Dust Blast: +0.6 Damage, +5% DDG | +0.6 Damage, +5% DDG, +5% Reflect |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Dust Devil's Backlash (was Total Disintegration): +0.4 Damage, +5% IDG -> +0.4 Damage, +5% Reflect. A whirling dust devil strikes with added force and its backlash hurls incoming damage back at attackers.
- p2_t3 Atomic Reprisal (kept): +5% DDG, +5% Reflect -> +5% Reflect. Atomic imagery fits the dust kit and reprisal still signals returning damage to attackers; no weakening is implied.
- p3_t1 Sharpened Grit (was Compressed Mote): +0.2 Damage -> +2% IDG. Grit honed to an edge makes every dust-borne attack bite harder.
- p3_t2 Scouring Gale (was Hollowing Wind): +0.4 Damage -> +3% IDG. A full scouring gale is the grander form of sharpened grit, driving attacks to hit harder still.
- p3_t3 Particle Annihilation (was Dustfall Rupture): +0.6 Damage, +5% IDT -> +1.2 Damage. Annihilation echoes Particle Cannon and signals sheer raw strike power.
- p4_t3 Enervating Dust Blast (was Resonant Dust Reprisal): +5% IDG, +5% Reflect -> +0.6 Damage, +5% DDG. The blast strikes with added force while the enervating dust saps the enemy's attacks.

## Arashima

Weakest completed path is 90% of the strongest; weakest add-on 64% of the strongest; average full build 2.39 Weight (before: 2.32).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Thunderseed: +0.4 Damage | Gathering Thunderhead: +0.8 Damage | Reaper's Stormlance: +25 Drain, +1.2 Pierce power | +1.2 Damage, +25 Drain, +1.2 Pierce power |
| p2 | Static Taint: +4% Poison | Lightning in the Veins: +6% Poison | Reaper's Downpour: +0.8 Damage, +25 Drain | +0.8 Damage, +25 Drain, +10% Poison |
| p3 | Storm Needle: +0.8 Pierce power | Cloudsplitter: +1.2 Pierce power | Unleashed Thunderhead: +1.2 Damage, +10% IDG | +1.2 Damage, +10% IDG, +2 Pierce power |
| p4 | Rising Gale: +4% IDG | Howling Tempest: +6% IDG | Thunder Through the Marrow: +10% IDG, +10% Poison | +20% IDG, +10% Poison |

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

Nodes whose effects changed (drafted names, for review):

- p2_t1 Static Taint (was Stormveil): +2% DDT -> +4% Poison. Storm static seeps into the foe, so every surge of chakra or stamina they spend jolts them back.
- p2_t2 Lightning in the Veins (was Rainbound Mantle): +3% DDT -> +6% Poison. The taint deepens into living lightning in the blood, punishing every exertion of the target's pools more severely.
- p2_t3 Reaper's Downpour (was The Storm's Due): +5% DDG, +25 Drain -> +0.8 Damage, +25 Drain. A pounding downpour signals heavier raw blows while the reaper's rain keeps sapping the target's health every round.
- p4_t1 Rising Gale (was Deadwind Breath): +2% DDG -> +4% IDG. A gale gathering behind each strike signals attacks that land harder.
- p4_t2 Howling Tempest (was Deadwind Dirge): +3% DDG -> +6% IDG. The rising gale grows into a howling tempest, driving every attack home with greater force.
- p4_t3 Thunder Through the Marrow (was Tempest Breaks Through): +5% IDG, +2 Pierce power -> +10% IDG, +10% Poison. Thunder that crashes through to the marrow evokes harder-hitting attacks that leave static lodged in the foe to punish their chakra and stamina use.

## Bakuhatsu

Weakest completed path is 89% of the strongest; weakest add-on 47% of the strongest; average full build 5.26 Weight (before: 6.69).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Trigger Spark: +2% Afterburn | Primed Detonation: +3% Afterburn | Breaching Charge: +0.6 Damage, +5% IDT | +0.6 Damage, +5% Afterburn, +5% IDT |
| p2 | Packed Charge: +0.2 Damage | Powder Keg: +0.8 Damage | Chain Reaction: +10% Afterburn | +1 Damage, +10% Afterburn |
| p3 | Stress Crack: +2% IDT | Fractured Casing: +3% IDT | Siege Battery: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +5% IDT |
| p4 | Blast Padding: +2% DDT | Layered Casing: +3% DDT | Shrapnel Storm: +0.6 Damage | +0.6 Damage, +5% DDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Breaching Charge (was Shelter at Ground Zero): +5% Afterburn, +5% DDT -> +0.6 Damage, +5% IDT. A breaching charge blasts the target's cover open, signalling exposure to follow-up hits alongside raw explosive power.
- p2_t3 Chain Reaction (was Critical Mass): +5% IDG -> +10% Afterburn. A chain reaction keeps detonating after the first blast, signalling burning damage stacked on top of each hit.
- p4_t3 Shrapnel Storm (was Bastion of Shrapnel): +5% DDT, +5% IDT -> +0.6 Damage. A storm of shrapnel conveys pure raw explosive striking power, with no defensive bastion implied.

## Blood-Enchanted Eyes

Weakest completed path is 93% of the strongest; weakest add-on 37% of the strongest; average full build 5.41 Weight (before: 6.78).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sanguine Edge: +0.2 Damage | Crimson Cleave: +0.6 Damage | Reaper's Enfeebling Lance: +5% DDG, +0.4 Pierce power | +0.8 Damage, +5% DDG, +0.4 Pierce power |
| p2 | Hungry Pulse: +2% Lifesteal | Crimson Thirst: +3% Lifesteal | Feast of Burning Blood: +5% Afterburn, +5% Vamp | +5% Afterburn, +5% Lifesteal, +5% Vamp |
| p3 | Coagulated Mantle: +2% DDT | Clotted Aegis: +3% DDT | Bloodfed Impaler: +5% Absorb, +0.4 Pierce power | +5% Absorb, +5% DDT, +0.4 Pierce power |
| p4 | Crimson Sip: +2% Vamp | Blooddrinker's Gaze: +3% Vamp | Brand of Boiling Blood: +10% Afterburn | +10% Afterburn, +5% Vamp |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Reaper's Enfeebling Lance (was Covenant of Blunted Blades): +5% DDG, +5% DDT -> +5% DDG, +0.4 Pierce power. Enfeebling signals the Reaper sapping the enemy's strikes; the lance signals hits that drive past defenses.
- p2_t3 Feast of Burning Blood (was Feast of the Fallen): +5% DDT, +5% Vamp -> +5% Afterburn, +5% Vamp. The feast signals the strike healing its bearer; burning blood signals scorching damage that lingers on the target's wounds.
- p3_t3 Bloodfed Impaler (was Bloodfed Bastion): +5% Absorb, +5% DDT -> +5% Absorb, +0.4 Pierce power. Bloodfed signals turning incoming hits into health; impaler signals strikes that run straight through defenses.
- p4_t1 Crimson Sip (was Withering Gaze): +2% DDG -> +2% Vamp. A first sip of blood signals the strike healing its user.
- p4_t2 Blooddrinker's Gaze (was Sanguine Oppression): +3% DDG -> +3% Vamp. The crimson eyes now drink deeply, signalling a stronger strike that heals its user.
- p4_t3 Brand of Boiling Blood (was Rending Crimson Brand): +5% Afterburn, +5 Pierce power -> +10% Afterburn. A brand that sets the target's blood boiling signals heavy burning damage on top of every hit it takes.

## Blue Blade Eyes

Weakest completed path is 55% of the strongest; weakest add-on 43% of the strongest; average full build 9.01 Weight (before: 9.77).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostbound Grip: +6% DDG | Deepening Numbness: +9% DDG | Numbing Sapphire Feast: +5% DDG, +5% Lifesteal | +20% DDG, +5% Lifesteal |
| p2 | Sapphire Edge: +0.2 Damage | Honed Crescent: +0.4 Damage | Bloodfrost Aegis: +5% DDT, +5% Lifesteal | +0.6 Damage, +5% DDT, +5% Lifesteal |
| p3 | Frost Mantle: +2% DDT | Hoarfrost Bulwark: +3% DDT | Rampart of Blue Blades: +0.4 Damage, +5% DDT | +0.4 Damage, +10% DDT |
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

Nodes whose effects changed (drafted names, for review):

- p2_t3 Bloodfrost Aegis (was Glacial Aegis): +5% DDT -> +5% DDT, +5% Lifesteal. An aegis guards against incoming damage while the blood-drinking frost heals from the damage dealt.
- p3_t3 Rampart of Blue Blades (was Glacier Unleashed): +5% IDG -> +0.4 Damage, +5% DDT. The rampart caps the guarding path while its sapphire blades lend added strike power.

## Cosmic Ascendant

Weakest completed path is 96% of the strongest; weakest add-on 54% of the strongest; average full build 4.71 Weight (before: 2.56).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Astral Resonance: +4% Afterburn | Resonance Cascade: +6% Afterburn | Force of the Supernova: +0.8 Damage, +10% IDG | +0.8 Damage, +10% Afterburn, +10% IDG |
| p2 | Stellar Focus: +4% IDG | Stellar Ascendance: +6% IDG | Event Horizon: +10% DDT | +10% DDT, +10% IDG |
| p3 | Tidal Strain: +2% IDT | Starrending Pull: +3% IDT | Gravity Well Sanctum: +5% DDG, +10% DDT | +5% DDG, +10% DDT, +5% IDT |
| p4 | Orbiting Veil: +4% DDT | Celestial Mantle: +6% DDT | Starfire Cataclysm: +1.2 Damage, +10% Afterburn | +1.2 Damage, +10% Afterburn, +10% DDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Force of the Supernova (was Supernova's Feast): +5% Afterburn, +5% Lifesteal -> +0.8 Damage, +10% IDG. The raw force of a supernova expresses both greater native strike power and attacks that hit harder.
- p2_t3 Event Horizon (was Voidburst Resonance): +0.4 Damage, +5% Afterburn -> +10% DDT. Nothing crosses an event horizon, so incoming damage is swallowed before it fully reaches the user.
- p3_t1 Tidal Strain (was Gravity Knot): +0.4 Damage -> +2% IDT. Gravitational tides strain the target's body and guard, leaving it exposed to more damage.
- p3_t2 Starrending Pull (was Collapsing Star): +1.2 Damage -> +3% IDT. The strain grows into a pull strong enough to rend stars, tearing the target wide open to incoming damage.
- p3_t3 Gravity Well Sanctum (was Hunger of the Singularity): +5% IDG, +5% Lifesteal -> +5% DDG, +10% DDT. A gravity well drags the force out of the enemy's blows while its sanctum shields the user from what remains.
- p4_t3 Starfire Cataclysm (was Unyielding Radiance): +5% DDT, +5% IDG -> +1.2 Damage, +10% Afterburn. A cataclysmic blow of starfire evokes heavy raw strike power and lingering burning damage.

## Crystal Essence

Weakest completed path is 94% of the strongest; weakest add-on 58% of the strongest; average full build 5.45 Weight (before: 4.39).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Mirror Facet: +2% Reflect | Light Turned Back: +3% Reflect | Infinite Refraction: +5% Reflect | +10% Reflect |
| p2 | Jade Lattice: +4% DDT | Layered Lattice: +6% DDT | Spiked Jade Bulwark: +0.8 Damage, +5% DDT | +0.8 Damage, +15% DDT |
| p3 | Prismatic Focus: +4% IDG | Radiant Convergence: +6% IDG | Crystal Avalanche: +0.8 Damage | +0.8 Damage, +10% IDG |
| p4 | Hairline Flaw: +2% IDT | Flawed to the Core: +3% IDT | Lance of Gathered Light: +5% IDG | +5% IDG, +5% IDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Infinite Refraction (was Citadel of Returning Light): +5% DDT, +5% Reflect -> +5% Reflect. Endlessly refracting light conveys incoming damage turned back on the attacker, without the mitigation implied by a citadel.
- p2_t3 Spiked Jade Bulwark (was Armored Radiance): +5% DDT, +5% IDG -> +0.8 Damage, +5% DDT. The jade bulwark shields against incoming damage while its spikes add raw striking power.
- p3_t3 Crystal Avalanche (was Shardstorm Reprisal): +0.4 Damage, +5% Reflect -> +0.8 Damage. A crashing avalanche of crystal expresses raw striking power, with no reprisal implied.
- p4_t1 Hairline Flaw (was Keen Shard): +0.2 Damage -> +2% IDT. A hairline flaw opened in the target, like a crack in crystal, signals greater vulnerability to damage.
- p4_t2 Flawed to the Core (was Razor Shards): +0.6 Damage -> +3% IDT. The flaw runs through the target's core, a deeper weakness that leaves it more exposed to damage.
- p4_t3 Lance of Gathered Light (was Adamant Lance): +0.8 Damage, +5% DDT -> +5% IDG. Light gathered through the prism into a lance makes every attack hit harder, without implying resilience.

## Ethereal Monarch

Weakest completed path is 92% of the strongest; weakest add-on 76% of the strongest; average full build 5.07 Weight (before: 2.58).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Starlit Flaw: +2% IDT | Soul Laid Bare: +3% IDT | Sovereign Starspear: +1.2 Damage, +0.4 Pierce power | +1.2 Damage, +5% IDT, +0.4 Pierce power |
| p2 | Astral Veil: +6% DDT | Woven Starlight: +9% DDT | Mirrorveil of Heaven: +5% DDT, +5% Reflect | +20% DDT, +5% Reflect |
| p3 | Claimed Stardust: +6% Consume | Soulwoven Aegis: +9% Consume | Conqueror's Star Aegis: +0.4 Damage, +5% Consume | +0.4 Damage, +20% Consume |
| p4 | Smoldering Stardust: +2% Afterburn | Searing Starfall: +3% Afterburn | Heaven's Returning Lance: +1.6 Pierce power, +10% Reflect | +5% Afterburn, +1.6 Pierce power, +10% Reflect |

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

Nodes whose effects changed (drafted names, for review):

- p1_t1 Starlit Flaw (was Soul Splinter): +0.2 Damage -> +2% IDT. Starlight reveals a flaw in the target, signalling that it is exposed and takes more damage.
- p1_t2 Soul Laid Bare (was Tear in the Soul): +0.6 Damage -> +3% IDT. The target's soul is laid fully bare, signalling deeper exposure to incoming damage.
- p1_t3 Sovereign Starspear (was Heaven's Mirrored Crown): +5% DDT, +5% Reflect -> +1.2 Damage, +0.4 Pierce power. A sovereign's spear of starlight signals overwhelming raw force that pierces past any defense.
- p2_t3 Mirrorveil of Heaven (was Heaven's Wardbreaker): +5% DDT, +3 Pierce power -> +5% DDT, +5% Reflect. The veil guards its bearer against harm while its mirrored face returns damage to attackers.
- p3_t3 Conqueror's Star Aegis (was Thronebreaker of Heaven): +0.6 Damage, +3 Pierce power -> +0.4 Damage, +5% Consume. The conqueror's heavier blows are forged into a starlit aegis, signalling raw power whose damage becomes a shield.
- p4_t1 Smoldering Stardust (was Ethereal Needle): +2 Pierce power -> +2% Afterburn. Stardust that smolders in the wound signals burning damage on top of the hits the target takes.
- p4_t2 Searing Starfall (was Veil-Piercing Ray): +3 Pierce power -> +3% Afterburn. A falling rain of searing stars signals a stronger burn layered over each hit.
- p4_t3 Heaven's Returning Lance (was Spoils of the Celestial Throne): +0.4 Damage, +5% Consume -> +1.6 Pierce power, +10% Reflect. Heaven returns every blow to its sender while the lance pierces past all defenses.

## Eyes of the Forsaken King

Weakest completed path is 87% of the strongest; weakest add-on 57% of the strongest; average full build 5.24 Weight (before: 3.78).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Tarnished Edge: +0.2 Damage | Edge of the Regalia: +0.8 Damage | Mirror-Crowned Wrath: +10% IDG, +10% Reflect | +1 Damage, +10% IDG, +10% Reflect |
| p2 | Exile's Mirror: +4% Reflect | Hall of Royal Mirrors: +6% Reflect | Searing Verdict: +5% Afterburn | +5% Afterburn, +10% Reflect |
| p3 | Royal Resolve: +4% IDG | Radiant Decree: +6% IDG | Burning Crown's Blade: +0.4 Damage, +5% Afterburn | +0.4 Damage, +5% Afterburn, +10% IDG |
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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Mirror-Crowned Wrath (was Throne of Broken Light): +5% IDG -> +10% IDG, +10% Reflect. A mirror crown turns attacks back on their source while royal wrath makes the king's attacks hit harder.
- p2_t1 Exile's Mirror (was Exile's Mantle): +2% DDT -> +4% Reflect. The exile's mirror returns a share of incoming damage to the attacker.
- p2_t2 Hall of Royal Mirrors (was Halo of the Unbowed): +3% DDT -> +6% Reflect. A whole hall of royal mirrors is the grander form of the exile's mirror, returning more damage.
- p2_t3 Searing Verdict (was Judgment of the Forsaken): +0.4 Damage, +5% Afterburn -> +5% Afterburn. Judgment rendered in light leaves the condemned searing with burning damage after each hit.
- p3_t3 Burning Crown's Blade (was Kingdom of One): +0.6 Damage, +5% Reflect -> +0.4 Damage, +5% Afterburn. The crown's blade strikes with added force and leaves its target burning.

## Heavenly Sonata

Weakest completed path is 100% of the strongest; weakest add-on 61% of the strongest; average full build 4.76 Weight (before: 2.77).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Opening Measure: +6% IDG | Rising Crescendo: +9% IDG | Crescendo and Hush: +5% DDG, +5% IDG | +5% DDG, +20% IDG |
| p2 | Guarding Refrain: +6% DDT | Choral Bulwark: +9% DDT | Shattering Cadence: +0.4 Damage, +5% IDT | +0.4 Damage, +15% DDT, +5% IDT |
| p3 | Fracturing Tone: +6% IDT | Unraveling Harmony: +9% IDT | Aegis of Dissonance: +5% DDT, +5% IDT | +5% DDT, +20% IDT |
| p4 | Muted Note: +6% DDG | Muted Strings: +9% DDG | Fortissimo Finale: +0.4 Damage, +5% IDG | +0.4 Damage, +15% DDG, +5% IDG |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Crescendo and Hush (was Discordant Sanctuary): +5% DDT, +5% IDT -> +5% DDG, +5% IDG. Your crescendo makes attacks land harder while the hush falls over the enemy, quieting the force of their blows.
- p2_t1 Guarding Refrain (was Striking Note): +0.4 Damage -> +6% DDT. A steady refrain wraps the user in protective sound that softens incoming damage.
- p2_t2 Choral Bulwark (was Dissonant Chord): +1.2 Damage -> +9% DDT. The lone refrain swells into a full chorus that stands as a bulwark against incoming damage.
- p2_t3 Shattering Cadence (was Sanctuary of Waning Breath): +5% DDT, +25 Drain -> +0.4 Damage, +5% IDT. A cadence struck hard enough to shatter delivers a raw blow and leaves the target's defenses broken open to further damage.
- p3_t3 Aegis of Dissonance (was Anthem of Ascendancy): +5% DDG, +5% IDG -> +5% DDT, +5% IDT. Harmony becomes an aegis that guards the user while its dissonance unravels the enemy, exposing them to more damage.
- p4_t3 Fortissimo Finale (was Dirge of Dwindling Strength): +5% DDG, +25 Drain -> +0.4 Damage, +5% IDG. The final fortissimo is a forceful raw strike played at full volume so every attack hits harder.

## Houkyuken

Weakest completed path is 91% of the strongest; weakest add-on 61% of the strongest; average full build 5.11 Weight (before: 5.46).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Lodestone Mark: +2% IDT | Drawn to the Fist: +3% IDT | Starfall Rebound: +0.6 Damage, +5% Reflect | +0.6 Damage, +5% IDT, +5% Reflect |
| p2 | Repelling Field: +2% DDT | Reversed Polarity: +3% DDT | Magnetic Backlash: +5% Reflect | +5% DDT, +5% Reflect |
| p3 | Aligned Force: +2% IDG | Lodestone Resonance: +3% IDG | Perfect Alignment: +5% IDG | +10% IDG |
| p4 | Rebounding Field: +2% Reflect | Like Poles Repel: +3% Reflect | Overcharged Lodestar: +0.4 Damage, +5% IDG | +0.4 Damage, +5% IDG, +5% Reflect |

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

Nodes whose effects changed (drafted names, for review):

- p1_t1 Lodestone Mark (was Lodestone Knuckle): +0.2 Damage -> +2% IDT. A lodestone mark assigns the target a polarity that draws blows in, signalling vulnerability to damage.
- p1_t2 Drawn to the Fist (was Polarized Fist): +0.4 Damage -> +3% IDT. The magnetized target is pulled into every punch, a stronger exposure to incoming damage.
- p1_t3 Starfall Rebound (was Starfall Hammer): +0.6 Damage, +5% IDG -> +0.6 Damage, +5% Reflect. Starfall carries the raw crushing force of the star-weapon while rebound signals returning damage to attackers.
- p2_t3 Magnetic Backlash (was Inexorable Pull): +0.4 Damage, +5% IDT -> +5% Reflect. A magnetic backlash hurls force back at whoever strikes the field, signalling returned damage.
- p3_t3 Perfect Alignment (was Aegis of Reversed Force): +5% DDT, +5% Reflect -> +5% IDG. Completing the aligned-force path, perfectly aligned poles make every attack hit harder.
- p4_t3 Overcharged Lodestar (was Violent Repulsion): +5% IDT, +5% Reflect -> +0.4 Damage, +5% IDG. An overcharged lodestar both empowers every attack and adds raw striking force, with no reflection implied.

## Hyouga Yui

Weakest completed path is 80% of the strongest; weakest add-on 43% of the strongest; average full build 5.28 Weight (before: 6.94).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Rime Shell: +2% DDT | Glacial Rampart: +3% DDT | Weight of the Avalanche: +0.4 Damage | +0.4 Damage, +5% DDT |
| p2 | Purgatory's Chill: +2% IDG | Deepening Frost: +3% IDG | The Glacier Advances: +0.4 Damage, +5% IDT | +0.4 Damage, +5% IDG, +5% IDT |
| p3 | Icebound Point: +0.4 Damage | Glacial Fang: +0.8 Damage | Wall of Cocytus: +5% DDT | +1.2 Damage, +5% DDT |
| p4 | Brittle Rime: +2% IDT | Purgatory's Fracture: +3% IDT | Shatterpoint of Cocytus: +5% IDT | +10% IDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Weight of the Avalanche (was Avalanche Bastion): +5% DDT, +5% IDG -> +0.4 Damage. The crushing weight of an avalanche signals greater raw striking power.
- p3_t3 Wall of Cocytus (was Spear Behind the Icewall): +0.8 Damage, +5% DDT -> +5% DDT. The frozen wall of Cocytus signals a guard that reduces incoming damage.
- p4_t3 Shatterpoint of Cocytus (was Bastion of Broken Ice): +5% DDT, +5% IDT -> +5% IDT. Finding the target's shatterpoint signals that it is left exposed and takes more damage.

## Itojinsei

Weakest completed path is 82% of the strongest; weakest add-on 51% of the strongest; average full build 5.12 Weight (before: 3.79).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Exposing Thread: +4% IDT | Razor Strands: +6% IDT | Severing Lattice: +10% IDT | +20% IDT |
| p2 | Taut Filament: +2% IDG | Threadbound Vigor: +3% IDG | Weaver Ascendant: +5% IDG | +10% IDG |
| p3 | Wire Edge: +0.2 Damage | Keen Filament: +0.8 Damage | Flaying Iron Web: +5% IDG, +5% IDT | +1 Damage, +5% IDG, +5% IDT |
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

Nodes whose effects changed (drafted names, for review):

- p3_t3 Flaying Iron Web (was The Severing Thread): +0.6 Damage -> +5% IDG, +5% IDT. The iron web flays the target open to further harm while its wires make every attack cut deeper.

## Kyuko-sei

Weakest completed path is 84% of the strongest; weakest add-on 59% of the strongest; average full build 6.55 Weight (before: 7.97).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Honed Stardust: +2% IDG | Meteoric Edge: +3% IDG | Dimming Starfall: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% IDG |
| p2 | Fading Force: +6% DDG | Entropic Weakening: +9% DDG | Frailty of Ages: +5% DDG | +20% DDG |
| p3 | Dust Shroud: +2% DDT | Aeonic Mantle: +3% DDT | Aegis of the Aeons: +5% DDT | +10% DDT |
| p4 | Eroded Seam: +2% IDT | Crumbling Firmament: +3% IDT | Weight of Dead Stars: +0.6 Damage | +0.6 Damage, +5% IDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t1 Honed Stardust (was Dense Starmote): +0.2 Damage -> +2% IDG. Stardust honed to a fine edge makes each attack bite harder.
- p1_t2 Meteoric Edge (was Shattered Firmament): +0.6 Damage -> +3% IDG. Honed dust becomes a meteor's edge, driving attacks home with far greater force.
- p1_t3 Dimming Starfall (was Mantle of the Dying Star): +5% DDT, +5% IDG -> +0.4 Damage, +5% DDG. A falling star strikes with raw force and dims the enemy's strength, weakening the attacks they make.
- p2_t3 Frailty of Ages (kept): +5% DDG, +5% IDT -> +5% DDG. The ages wear the enemy into frailty, which still signals their attacks losing strength.
- p3_t3 Aegis of the Aeons (was Sanctuary of Erosion): +5% DDT, +5% IDT -> +5% DDT. A shield that endures the aeons cannot be eroded, signalling sharply reduced incoming damage.
- p4_t3 Weight of Dead Stars (was Dominion of Entropy): +5% DDG, +5% IDG -> +0.6 Damage. The crushing weight of collapsed stars expresses pure native strike power.

## Oblivion Seal

Weakest completed path is 97% of the strongest; weakest add-on 81% of the strongest; average full build 4.79 Weight (before: 4.16).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Umbral Vigor: +2% IDG | Umbral Claws: +3% IDG | Cursed Beast's Feast: +0.6 Damage, +10% Lifesteal | +0.6 Damage, +5% IDG, +10% Lifesteal |
| p2 | Siphoning Curse: +2% Lifesteal | Hunger of the Seal: +3% Lifesteal | Spear of Unmaking: +10% IDG, +1.6 Pierce power | +10% IDG, +5% Lifesteal, +1.6 Pierce power |
| p3 | Umbral Veil: +4% DDT | Cocoon of Endless Night: +6% DDT | Wrath of the Unsealed: +0.6 Damage, +10% IDG | +0.6 Damage, +10% DDT, +10% IDG |
| p4 | Darkened Edge: +0.4 Damage | Rending Sigil: +0.6 Damage | Wardpiercing Hunger: +10% Lifesteal, +1.6 Pierce power | +1 Damage, +10% Lifesteal, +1.6 Pierce power |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Cursed Beast's Feast (was Absolute Erasure): +5% IDG, +0.4 Pierce power -> +0.6 Damage, +10% Lifesteal. The cursed beast feeds on what it tears, signalling healing from damage dealt along with raw striking power.
- p2_t1 Siphoning Curse (was Eroding Curse): +2% IDT -> +2% Lifesteal. A curse that siphons life from the victim signals healing from damage dealt.
- p2_t2 Hunger of the Seal (was Shadow-Laid Fracture): +3% IDT -> +3% Lifesteal. The seal itself hungers and feeds on every wound, a stronger healing from damage dealt.
- p2_t3 Spear of Unmaking (was Brand of Oblivion): +5% IDT -> +10% IDG, +1.6 Pierce power. A spear pierces through defenses while unmaking signals attacks that hit far harder.
- p3_t1 Umbral Veil (was Void Needle): +2 Pierce power -> +4% DDT. A veil of shadow wrapped around the user signals reduced incoming damage.
- p3_t2 Cocoon of Endless Night (was Wardrending Shade): +3 Pierce power -> +6% DDT. A full cocoon of night is a heavier shroud, signalling stronger reduction of incoming damage.
- p3_t3 Wrath of the Unsealed (was Sanguine Seal of Shelter): +5% DDT, +5% Lifesteal -> +0.6 Damage, +10% IDG. Unsealed wrath conveys both empowered attacks and heavier raw strikes, with no shelter implied.
- p4_t3 Wardpiercing Hunger (was Wardbreaker in Shadow): +5% DDT, +2 Pierce power -> +10% Lifesteal, +1.6 Pierce power. Wardpiercing signals damage that ignores defenses while hunger signals healing from damage dealt.

## Shadow Weaver

Weakest completed path is 93% of the strongest; weakest add-on 44% of the strongest; average full build 4.81 Weight (before: 3.75).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Sharpened Shadow: +0.2 Damage | Barbed Thread: +0.8 Damage | Night's Drawn Garrote: +5% IDG | +1 Damage, +5% IDG |
| p2 | Tension in the Dark: +2% IDG | Empowered Stitch: +3% IDG | Threads That Bind Blades: +5% DDG | +5% DDG, +5% IDG |
| p3 | Dampening Thread: +4% DDG | Frayed Resolve: +6% DDG | Cocoon of Night: +5% DDT | +10% DDG, +5% DDT |
| p4 | Warding Stitch: +2% DDT | Tightened Weave: +3% DDT | Shroud That Smothers Blades: +5% DDG, +5% DDT | +5% DDG, +10% DDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Night's Drawn Garrote (was Night Unraveled): +0.6 Damage -> +5% IDG. A shadow thread drawn tight as a garrote signals attacks that bite harder.
- p2_t3 Threads That Bind Blades (was A Thousand Striking Threads): +5% IDG -> +5% DDG. Shadow threads binding the enemy's blades signal weakened enemy attacks.
- p3_t3 Cocoon of Night (was Strings Cut Short): +5% DDG -> +5% DDT. A cocoon woven of night signals a guard that reduces the damage its bearer takes.
- p4_t3 Shroud That Smothers Blades (was Seamless Shroud): +5% DDT -> +5% DDG, +5% DDT. The shroud guards its wearer while smothering enemy blades, signalling both reduced incoming damage and weakened enemy attacks.

## Shakunetsu Sakura

Weakest completed path is 92% of the strongest; weakest add-on 68% of the strongest; average full build 5.74 Weight (before: 5.00).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Kindled Bud: +4% IDG | Kindled Boughs: +6% IDG | Dragon in Full Blossom: +5% IDG | +15% IDG |
| p2 | Blistering Pollen: +2% IDT | Blossoms Bare the Wound: +3% IDT | Dragon Tree's Renewal: +5 Heal power | +5 Heal power, +5% IDT |
| p3 | Restoring Bud: +2 Heal power | Mending Petal Rain: +3 Heal power | Dragon's Wardrending Bloom: +5% IDG, +0.4 Pierce power | +5 Heal power, +5% IDG, +0.4 Pierce power |
| p4 | Wilting Heat: +4% DDG | Enfeebling Ember Dance: +6% DDG | Armor-Melting Dragon Breath: +0.4 Damage, +1.6 Pierce power | +0.4 Damage, +10% DDG, +1.6 Pierce power |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Dragon in Full Blossom (kept): +0.4 Damage, +5% IDG -> +5% IDG. Full blossom still crowns the kindled bud-and-bough path, signalling attacks that hit harder.
- p2_t1 Blistering Pollen (was Petal Needle): +2 Pierce power -> +2% IDT. Scorching pollen blisters the target's skin, leaving it exposed to more damage.
- p2_t2 Blossoms Bare the Wound (was Blossom Through Iron): +3 Pierce power -> +3% IDT. Where the blistering pollen settles, the full blossoms lay the wound open so the target takes more damage.
- p2_t3 Dragon Tree's Renewal (was Scorching Hanami): +5 Pierce power -> +5 Heal power. Echoing the Sakura Dragon Tree, the renewal signals health restored over time.
- p4_t1 Wilting Heat (was Scorching Petal): +0.6 Damage -> +4% DDG. Blossom-scorching heat wilts the enemy's strength, weakening its attacks.
- p4_t2 Enfeebling Ember Dance (was Blazing Petal Torrent): +1.2 Damage -> +6% DDG. Echoing Dancing Embers, the swirling embers enfeeble the enemy more deeply than wilting heat.
- p4_t3 Armor-Melting Dragon Breath (was Oppressive Dragon's Breath): +5% DDG, +2 Pierce power -> +0.4 Damage, +1.6 Pierce power. Dragon breath strikes with raw force and melts through armor so the damage ignores defenses.

## Shinrai Ou

Weakest completed path is 93% of the strongest; weakest add-on 25% of the strongest; average full build 5.93 Weight (before: 5.56).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Vajra Spark: +0.2 Damage | Vajra Tempering: +0.6 Damage | Raijin's Sundering Retort: +5% IDT, +5% Reflect | +0.8 Damage, +5% IDT, +5% Reflect |
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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Raijin's Sundering Retort (was Thunder King's Wrath): +0.6 Damage -> +5% IDT, +5% Reflect. Raijin's retort hurls attackers' damage back at them while his sundering lightning leaves the target exposed.
- p2_t3 Judgement from Above (kept): +5% IDG -> +0.4 Damage. A bolt of judgement hurled from the heavens still reads as a direct raw lightning strike.
- p3_t3 Heaven's Reprisal (kept): +5% Reflect -> +0.4 Damage, +5% Reflect. Heaven's reprisal returns damage to attackers and answers with a strike of its own, matching reflect plus raw damage.
- p4_t3 Thunder King's Condemnation (kept): +5% IDT -> +0.4 Damage, +10% IDT. The Thunder King's condemnation still marks the target as exposed, now sealed with a strike of lightning.

## Shinseina Ki

Weakest completed path is 64% of the strongest; weakest add-on 26% of the strongest; average full build 5.90 Weight (before: 7.98).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Heartwood Edge: +0.2 Damage | Tempered Heartwood: +0.6 Damage | Roots Through Armor: +5% IDT | +0.8 Damage, +5% IDT |
| p2 | Sapborne Vigor: +2% IDG | Fangs of Heartwood: +3% IDG | Thorns in Every Motion: +5% Poison | +5% IDG, +5% Poison |
| p3 | Exposing Root: +2% IDT | Rootbound Prey: +3% IDT | Fall of the Elderwood: +0.6 Damage | +0.6 Damage, +5% IDT |
| p4 | Bitter Sap: +6% Poison | Burden of the Bitter Boughs: +9% Poison | Snare of the Venomwood: +5% IDT, +5% Poison | +5% IDT, +20% Poison |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Roots Through Armor (was Sundering Heartwood): +0.8 Damage, +5% IDT -> +5% IDT. Roots splitting the enemy's armor open signal greater vulnerability to damage.
- p2_t3 Thorns in Every Motion (was The Forest Strikes): +0.4 Damage, +5% IDG -> +5% Poison. Thorns that bite whenever the target moves signal harm each time it spends chakra or stamina.
- p3_t3 Fall of the Elderwood (was Venomous Judgment of the Grove): +5% IDT, +5% Poison -> +0.6 Damage. The crushing fall of ancient elderwood conveys sheer raw striking power, with no venom implied.
- p4_t3 Snare of the Venomwood (was Dominion of the Venomwood): +5% IDG, +5% Poison -> +5% IDT, +5% Poison. The snare holds the enemy exposed to damage while venomwood burdens every chakra or stamina expenditure.

## Shiroi Youso

Unchanged. Fewer than four eligible root effects for four distinct paths (eligible: Afterburn, DDT, Heal). Needs its element decided first.


## Suragu

Weakest completed path is 93% of the strongest; weakest add-on 76% of the strongest; average full build 4.97 Weight (before: 5.11).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Basalt Skin: +4% DDT | Obsidian Carapace: +6% DDT | Fissure of the Caldera: +5% IDT | +10% DDT, +5% IDT |
| p2 | Softened Crust: +2% IDT | Fractured Slag: +3% IDT | Venomous Feast of the Mountain: +5% Lifesteal, +5% Poison | +5% IDT, +5% Lifesteal, +5% Poison |
| p3 | Hungry Ember: +2% Lifesteal | Molten Draught: +3% Lifesteal | Erupting Mountain Fury: +0.4 Damage, +5% IDG | +0.4 Damage, +5% IDG, +5% Lifesteal |
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

Nodes whose effects changed (drafted names, for review):

- p1_t1 Basalt Skin (was Molten Needle): +2 Pierce power -> +4% DDT. Cooled lava hardening into basalt skin signals reduced incoming damage.
- p1_t2 Obsidian Carapace (was Slagbreaker): +3 Pierce power -> +6% DDT. A full obsidian carapace signals a stronger guard against incoming damage.
- p1_t3 Fissure of the Caldera (was Feast of the Resonant Caldera): +5% Afterburn, +5% Lifesteal -> +5% IDT. The caldera splits the target open along a molten fissure, signalling that it is exposed and takes more damage.
- p3_t3 Erupting Mountain Fury (was Heart of the Caldera): +5% DDT, +5% Lifesteal -> +0.4 Damage, +5% IDG. A mountain's eruption signals both raw striking power and attacks that hit harder.

## Taiyo Kami

Weakest completed path is 95% of the strongest; weakest add-on 76% of the strongest; average full build 4.77 Weight (before: 4.51).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Daybreak Fervor: +2% IDG | Corona's Fury: +3% IDG | Solar Cataclysm: +0.8 Damage, +5% DDG | +0.8 Damage, +5% DDG, +5% IDG |
| p2 | Sunburnt Hide: +2% IDT | Bared to the Sun: +3% IDT | Eternal Noon: +10% IDG | +10% IDG, +5% IDT |
| p3 | Dawnward: +2% DDT | Golden Mantle: +3% DDT | Solar Flare Bulwark: +0.4 Damage, +5% DDT | +0.4 Damage, +10% DDT |
| p4 | Dawnheart: +2% DDG | Heart of the Sun: +3% DDG | Unshadowed Zenith Strike: +0.6 Damage, +5% IDT | +0.6 Damage, +5% DDG, +5% IDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t1 Daybreak Fervor (was Breaking Point): +0.2 Damage -> +2% IDG. The rising sun's fervor drives the first harder-hitting attacks.
- p1_t2 Corona's Fury (was Crown of Cinders): +0.6 Damage -> +3% IDG. The blazing corona is the grander fury of daybreak, making attacks hit harder still.
- p2_t1 Sunburnt Hide (was Ember Seed): +2% Afterburn -> +2% IDT. Sun-burnt skin turns tender, leaving the target exposed to more damage.
- p2_t2 Bared to the Sun (was Emberwake): +3% Afterburn -> +3% IDT. Stripped of all shade, the target is laid fully open to the sun and takes more damage.
- p2_t3 Eternal Noon (kept): +0.8 Damage, +5% DDT -> +10% IDG. The sun held forever at its fiercest height still signals attacks that hit harder; it does not extend duration.
- p3_t3 Solar Flare Bulwark (was Sovereign Sun): +0.4 Damage, +5% IDT -> +0.4 Damage, +5% DDT. The bulwark crowns the warding path while its solar flare adds raw strike power.
- p4_t3 Unshadowed Zenith Strike (was Zenith Incarnate): +5% Afterburn, +5% DDG -> +0.6 Damage, +5% IDT. At the zenith no shadow hides the target, exposing it to more damage beneath a powerful solar strike.

## Teno Yuki

Weakest completed path is 96% of the strongest; weakest add-on 84% of the strongest; average full build 4.88 Weight (before: 3.46).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Frostborne Vigor: +2% IDG | Killing Frost: +3% IDG | Crown of Brittle Frost: +5% IDG, +10% IDT | +10% IDG, +10% IDT |
| p2 | Rimebrittle Touch: +2% IDT | Shatterpoint Frost: +3% IDT | Imperial Avalanche: +1.2 Damage, +10% IDG | +1.2 Damage, +10% IDG, +5% IDT |
| p3 | Snowbound Mantle: +6% DDT | Permafrost Mantle: +9% DDT | Winter's Breaking Verdict: +1.2 Damage, +10% IDT | +1.2 Damage, +15% DDT, +10% IDT |
| p4 | Siphoning Snow: +2% Absorb | Ravenous Snowfall: +3% Absorb | Avalanche and Thaw: +0.8 Damage, +5 Heal power | +0.8 Damage, +5% Absorb, +5 Heal power |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 Crown of Brittle Frost (was Hunger of the Winter Crown): +5% Absorb, +5% IDG -> +5% IDG, +10% IDT. The winter crown empowers the user's attacks while its brittle frost leaves the target exposed to shattering blows.
- p2_t1 Rimebrittle Touch (was Ice Splinter): +0.2 Damage -> +2% IDT. A touch of rime turns the target brittle, so it takes more damage.
- p2_t2 Shatterpoint Frost (was Glacial Lance): +1.2 Damage -> +3% IDT. Frost spreads to the target's shatterpoints, exposing it to much heavier damage.
- p2_t3 Imperial Avalanche (was Palace of Consuming Ice): +5% Absorb, +5% DDT -> +1.2 Damage, +10% IDG. An imperial avalanche combines crushing raw strike power with attacks that hit harder.
- p3_t3 Winter's Breaking Verdict (was Winter's Sheltering Verdict): +5% DDT, +5% IDT -> +1.2 Damage, +10% IDT. Winter's verdict lands as a heavy raw blow that breaks the target open to more damage.
- p4_t3 Avalanche and Thaw (was Winter's Exposing Command): +5% IDG, +5% IDT -> +0.8 Damage, +5 Heal power. The avalanche delivers the strike and the thaw that follows restores health over time.

## Tenohira Musei

Weakest completed path is 86% of the strongest; weakest add-on 47% of the strongest; average full build 5.82 Weight (before: 7.75).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Quieting Touch: +4% DDG | Silencing Pressure: +6% DDG | All Blows Fall Silent: +5% DDG | +15% DDG |
| p2 | Gathered Palm: +0.4 Damage | Condensed Force: +0.8 Damage | Tipping the Balance: +5% IDG | +1.2 Damage, +5% IDG |
| p3 | Centered Intent: +2% IDG | Gathered Force: +3% IDG | Strike That Stills: +0.4 Damage, +5% DDG | +0.4 Damage, +5% DDG, +5% IDG |
| p4 | Exposing Palm: +2% IDT | Fracture in Stillness: +3% IDT | Moonfall Palm: +0.4 Damage | +0.4 Damage, +5% IDT |

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

Nodes whose effects changed (drafted names, for review):

- p1_t3 All Blows Fall Silent (was Hushed Ruin): +5% DDG, +5% IDT -> +5% DDG. Every enemy blow falling silent conveys sharply weakened enemy attacks, without implying exposure.
- p2_t3 Tipping the Balance (kept): +5% DDG, +5% IDG -> +5% IDG. Tipping the Yin-Yang balance in the user's favor still reads cleanly as stronger friendly attacks.
- p3_t3 Strike That Stills (was The Silent Impact): +5% IDG, +5% IDT -> +0.4 Damage, +5% DDG. The strike carries raw force while stilling the foe signals weakened enemy attacks.
- p4_t3 Moonfall Palm (was Eclipse in Hand): +0.4 Damage, +5% IDT -> +0.4 Damage. A palm landing with the weight of a falling moon expresses raw striking power, with no exposure implied.

## Vaporia

Weakest completed path is 95% of the strongest; weakest add-on 86% of the strongest; average full build 5.30 Weight (before: 5.48).

| Path | Foundation | Hidden Art | Advanced Art | Completed path (3 BP) |
|---|---|---|---|---|
| p1 | Building Pressure: +2% IDG | Boiling Point: +3% IDG | Azure Dragon's Fury: +5% IDG | +10% IDG |
| p2 | Pressurized Drop: +0.4 Damage | Geyser Fist: +0.8 Damage | Flesh Scalded Raw: +5% IDT | +1.2 Damage, +5% IDT |
| p3 | Resonant Heat: +2% Afterburn | Scalding Resonance: +3% Afterburn | Armor-Boiling Lance: +5% IDT, +0.4 Pierce power | +5% Afterburn, +5% IDT, +0.4 Pierce power |
| p4 | Scalded Seam: +2% IDT | Deepening Scald: +3% IDT | Recoiling Steam Mantle: +5% DDT, +5% Reflect | +5% DDT, +5% IDT, +5% Reflect |

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

Nodes whose effects changed (drafted names, for review):

- p1_t1 Building Pressure (was Mending Vapor): +2 Heal power -> +2% IDG. Steam pressure building behind each strike signals attacks that hit harder.
- p1_t2 Boiling Point (was Restorative Mist): +3 Heal power -> +3% IDG. Reaching the boiling point signals the pressure peaking into still harder attacks.
- p1_t3 Azure Dragon's Fury (was Scald-Laid Weakness): +5% IDT -> +5% IDG. The Azure Dragon's fury signals the bloodline's attacks striking with their greatest force.
- p2_t3 Flesh Scalded Raw (was Steamclad Wardbreaker): +5% DDT, +5 Pierce power -> +5% IDT. Flesh scalded raw signals a target left exposed to take more damage.
- p3_t3 Armor-Boiling Lance (was Bastion of Returning Steam): +5% DDT, +5% Reflect -> +5% IDT, +0.4 Pierce power. A lance of steam boils through armor, signalling strikes that ignore defenses and leave the target exposed.
- p4_t3 Recoiling Steam Mantle (was Dragon's Siphoning Fang): +5% Lifesteal, +2 Pierce power -> +5% DDT, +5% Reflect. A mantle of steam guards its bearer and recoils blows back onto attackers, signalling reduced damage taken and reflection.
