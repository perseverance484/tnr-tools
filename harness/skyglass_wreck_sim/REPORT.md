# Skyglass Wreck offline simulation: report 2 (2026-10-28)

All fights are engine-native and offline: the game source at origin/main `c86f43f4`, an exported copy, battles in memory.
There were zero live requests. Inputs are committed captures plus two values the director read in game: the live damage
settings and the solo-Captain anchor. Raw numbers are in `results/live_*.json`, `results/calibration_solo_captain.json`
and `results/probe_mechanics.json`. Report 1's runs (code-default damage settings, gear stand-ins) remain in
`results/` without the `live_` prefix; they are superseded.

## What changed since report 1

- **Live damage settings** are the default for every battle (`data/dmg_config_live.json`, written to
  `battle.extraState.dmgConfig`). The values are curve 2, gen_weight 1, advantage_min 0; the code defaults are 1.6, 2
  and 0.01.
- **Real player build** (director's "average", the endgame party member):
  - Level-100 JONIN with stats at the JONIN caps.
  - The **full Kitsune armour set**: all 6 slots, from push/204 (`tnr_results_1792629744565.json`). The capture holds
    every set piece (Mask, Armor, Gauntlets, Belt, Pants, Tabi-Shoes; Pants-F is an identical alternate), so no piece
    is missing.
  - The set is worn as real item rows through the engine's item path. Realised in battle: +50 points damage given and
    +30 points damage reduction in the pre-battle gear pools, +1,200 max HP (static, 20 rounds), 4× increasestat 20%,
    and absorb 30% for 5 rounds.
  - **9 PvE-usable jutsu at the Jonin level cap 25.** The Elite Jonin cap of 30 applies only to ELITE JONIN-rank jutsu,
    so it does not apply here. All 9 load in battle (none gated); Fire/Wind elements:
    - Chakra Overflow
    - Typhon Burst (AOE)
    - Tempestual Fury (AOE)
    - Burning Coil
    - Gale Force Blast
    - Scorching Sun Strike
    - Wind Style: Sky Dragon
    - Phoenix Flame Strike
    - Stunning Jab
  - The strongest raw PvE entries are not used:
    - Torturing Flame Coil needs Scorch, a bloodline element.
    - Sonic Slash and Soul Shackles deal a flat (static) 100 damage, which is weak at endgame.
- **Reference build:** `noarmor` is the same build without the set.

## Solo-Captain anchor check (60 seeds; one player vs the live The Captain; plain QUEST battle)

Director anchor: "good players beat it in 8-10 rounds, some fewer; a tough fight".

| Build | Wins | Rounds (wins) | HP left at the win | Losses |
|---|---:|---:|---:|---|
| **average (Kitsune set)** | **60/60** | **8** (every seed) | **71.6%** | none |
| noarmor | 0/60 | - | - | dies in round 3; Captain at 81% HP |

- **Speed:** the real build matches the anchor's 8-10 rounds, at the fast end.
- **Survival:** it is more comfortable than "a tough fight", ending at ~72% HP. That makes it mildly stronger than the
  anchor on survival, not far stronger. It was not tuned down.
- **Why there is no spread:** the solo fight is almost deterministic. The only randomness is the spawn tile.
- **What the set does:** the Captain's hits drop to about 1/5. The set's +30 damage reduction stacks linearly with the
  engine's base 50, so 80% of damage is removed.

## Endgame runs (live settings; 30 seeded runs per party)

Minutes are medians at 10 / 15 / 20 s per player turn. AI turns cost 0 s, plus 30 s per floor battle. For runs that never
clear, minutes are the time until the run is abandoned after 4 wipes.

| Layout | Party | Clears | Runs with a wipe | Rounds (median) | Min @10 / 15 / 20 s |
|---|---|---:|---:|---:|---|
| Live 16 waves (push/263) | average | 0/30 | 100% | 40.5 | dies on F1W2 (118/120 attempts) |
| | noarmor | 0/30 | 100% | 8 | dies on F1W1 |
| candidate_target20 (5 waves of 2, crew pools 1.5, Crowned pools 4) | average | 30/30 | 10% | 21.5 | 12.0 / 16.8 / 21.5 |
| candidate_target20_soft (+ crew bonus damage +150%) | average | 30/30 | 0% | 21 | 12.0 / 16.8 / 21.5 |
| director_layout (as given, crew unchanged) | average | 0/30 | 100% | 84 | dies on F3W1 (62/62) |
| director_layout_v2 (RUL-2026-10-28-003 + Core Rupture edit) | average | 0/30 | 100% | 91 | dies on F3W1 (81/82) |
| | noarmor | 0/30 | 100% | 8 | dies on F1W1 |
| **dense_a** (mine: 1 wave of 3-4 per floor) | **average** | **30/30** | **13%** | **30** | **16.1 / 22.9 / 29.7** |
| dense_b (director layout + dense_a stats) | average | 30/30 | 10% | 41 | 21.7 / 31.3 / 40.8 |
| **dense_b_v2** (director_layout_v2 + dense_a stats) | **average** | **30/30** | **0%** | **38.5** | **20.9 / 30.1 / 39.3** |
| | noarmor | 0/30 | 100% | 36 | dies on F2W2 / F3 |

`noarmor` fails every layout.

**Stat changes in dense_a and dense_b, all storable values:**
- Crew AIs: `poolsMultiplier` 1.5 (7,575 HP), and the innate damage given replaced by a single +150%. Captured is
  +350-450% across stacked rows.
- Crowned Captain: pools 4.
- Sealwright: pools 2.5 (12,625 HP).

### Per-wave rounds, average party (median [min-max]; clears / attempts; wipes)

**director_layout_v2** (crew as live):

| Wave | Enemies | Result |
|---|---|---|
| F1W1 | DW x3 + Seal Charge | 9 [3-13]; 112/118; 6 wipes |
| F2W1 | DW + Seal Charge x2 | 4 [3-6]; 112/112 |
| F2W2 | DW x3 | 8 [4-13]; 82/112; 30 wipes |
| F3W1 | Sentinel + First Blade + DW | 6; 1/82; **81 wipes** |
| F4W1 | DW x2 + Oathkeeper | 9; 3/3 |
| F4W2 | Wayfinder + Core Horror | 0/3 |

Unchanged crew stats end the run at floor 3. The party reaches it on ~31% HP, because pools refill only between floors.

**dense_b_v2** (same layout, tuned crew stats):

| Wave | Rounds | Party HP lost % |
|---|---|---:|
| F1W1 | 6 [3-7] | 24 |
| F2W1 | 3 [3-4] | 3 |
| F2W2 | 7 [4-8] | 15 |
| F3W1 | 5 [4-6] | 33 |
| F4W1 | 5 [4-6] | 26 |
| F4W2 | 5 [3-6] | 11 |
| F5W1 | 6 [4-8] | 16 |
| F5W2 | 5 [4-6] | 31 |

Floor totals are 6 / 9 / 5 / 9 / 11 rounds. All 30 runs clear, with no wipe.

**dense_a:**

| Wave | Enemies | Rounds | Wipes |
|---|---|---|---:|
| F1 | DW x3 + Seal Charge | 6 [3-8] | 0 |
| F2 | Oathkeeper + DW x2 + Seal Charge | 6 [3-8] | 0 |
| F3 | Sentinel + First Blade + DW | 5 [3-6] | 0 |
| F4 | The Captain + Wayfinder + DW | 4 [3-6] | 0 |
| F5 | Crowned + Sealwright + Core Canister x2 | 9 [6-11] | 4 |

13% of runs wipe once.

### Reading against the target (15-20 min, about 1 run in 5 wipes once)

- **dense_a:** 23 min at 15 s per turn and 16 min at 10 s; 13% of runs wipe. Closest to target on both time and risk.
- **The director's layout** (8 waves) costs ~38-41 rounds even when tuned (dense_b_v2 ≈ 30 min at 15 s, 21 at 10 s),
  and it is safe at that tuning (0% wipes). Reaching 15-20 min at 15 s per turn needs ≈20-27 rounds, i.e. 5-6 waves or
  lower crew HP.
- **"Two-enemy waves are light work" is confirmed:** in target20 they take 3-4 rounds each. 3-enemy waves take 5-7 rounds
  at pools 1.5.

## Wave-2 opener fix (`round_lower_than 2` rules on wave-2 units)

Windlash Focus has cooldown 4. Fire counts are per appearance of the wave-2 unit.

| Variant | F2W2 Deck Warden x3: never / once / 2+ | F4W2 Wayfinder: never / once / 2+ |
|---|---|---|
| as live (round < 2) | 100% / 0 / 0 (303 of 303 never) | 100% never (dense_b) |
| (a) first, no condition | 0 / 32-49% / 51-68% | 0 / 100% / 0 |
| (b) first, gated distance_higher_than 5 to CLOSEST_OPPONENT | 92-94% / 6-8% / 0 | 100% never |

- **(a)** always fires on arrival, then again every 4 rounds while the unit lives. Waves last 5-7 rounds, so Deck Wardens
  usually cast it twice.
- **(b)** almost never fires. Wave-2 units spawn after the players have advanced to within 5 hexes.
- To get "exactly once on arrival", (a) needs a cooldown at least as long as the wave. Alternatively, gate it on the
  unit not yet having the buff (`has_effect increasedamagegiven` below its total), since the opener is self-buff IDG.

Data: `results/live_director_layout_opener_*.json`, `results/live_dense_b_opener_*.json`, field
`ruleFireDist`. On the as-given director layout the party never reaches F4, which is why dense_b carries the Wayfinder test.

## Mechanics probes (`results/probe_mechanics.json`, `engine/probe_mechanics.ts`; 3 seeds each)

The setup is one average player vs one probe enemy, with the Deck Warden row carrying only the probe jutsu. Rule 0 casts
the probe jutsu; the engine backup rules stay on. All jutsu are real captured records.

### 1. Movement jutsu on an AI

**Verdict: AIs can use movement jutsu.**
- The `ai_v2.ts` filter that drops move/summon jutsu applies only to ids containing `user_`, i.e. auto-combat humans.
- **Replacement Technique** (range 1, cd 2):
  - At EMPTY_GROUND_CLOSEST_TO_OPPONENT it fires every time it is off cooldown (3 casts in 6 rounds) and hops one hex.
  - At CLOSEST_OPPONENT it **never** fires: the player's occupied tile is not EMPTY_GROUND, and the engine rejects the
    pick and falls through to the next rule.
- **Body Flicker** (range 5, move + AOE damage 20):
  - At EMPTY_GROUND_CLOSEST_TO_OPPONENT it fires (2 per 6 rounds), crosses up to 5 hexes and lands beside the player
    (one cast hit the player for 245).
  - At CLOSEST_OPPONENT it fires once and **lands on the player's own tile** (3/3 seeds). On its next turn the enemy finds
    no valid action and the engine's give-up path kills it (`curHealth = 0`, `ai_v2.ts` "exhausted and has to give up").
  - Cause: the `move` tag (`tags.ts` `move`, ~l.2439-2443) sets the target coordinates unconditionally. Its comment
    promises a nearest-free-tile fallback that the code does not do.
  - **Do not target movement jutsu at an occupant.**

### 2. Summon jutsu on an AI

**Verdict: AI summons work** (the captured Hell Hound record, aiId changed to Seal Charge / Core Canister, cast at
EMPTY_GROUND_CLOSEST_TO_OPPONENT).
- **Firing:** fires once in round 1 and spawns 1 unit on the chosen empty tile in range, which was 1 hex from the
  player in these seeds.
- **The summon:** HP = the effect's `aiHp` (3,000). It lives `rounds` = 2 rounds, then leaves.
- **It acts on its own AI profile:**
  - The summoned Seal Charge waited 2 rounds, then fired Core Rupture in round 3. That dealt 5,234 to the player plus a
    stun, and destroyed itself.
  - The Core Canister only waited, since its own rule gate never held.
- The engine loads summon templates through `processUsersForBattle`'s `summonTemplateCache` (a DB read live). The
  harness pre-seeds that cache from the captured AI rows.

### 3. Ground AOE with a damage effect lasting 2+ rounds

Jutsu: Drowning Mire (PvE: damage 15 + IDT 15, 2 rounds, circle). Toxic Pool is PVP-only and the engine filters it out
of QUEST battles even for AIs.

**Timing:**
- Damage lands **in the cast round** on everyone on the 14 cells, the caster included: the AI hurt itself for 1,842.
- It then ticks **at the start of each affected unit's turn** while the unit stands on it: rounds +1 and +2 for
  `rounds 2`.
- Stepping onto another cell of the pool applies it again.

**Leaving the pool:**
- **Stepping off stops it.** The player who walked off in round 3 took no tick in round 4. The ground effect does not
  follow the unit.
- A COORDINATE target on the player's tile behaves the same as EMPTY_GROUND_CLOSEST_TO_OPPONENT once the caster is in
  range.

### 4. Barrier

Jutsu: Adamantine Fortress (AOE_LARGE_WALL_SHOOT, range 1).
- **Casting:** the AI casts it when gated to a player within 2. The wall is a 6-9 cell line through the targeted empty
  tile, lasting 2 rounds; seed 1 drew a full column.
- **Player response:** the players' auto-combat profile never attacked a barrier in these seeds. It kept attacking the
  enemy, which stayed reachable around or beside the wall.
- Players do carry the engine's backup rule (attack BARRIER_BLOCKING_CLOSEST_OPPONENT), but it is last in the list.

### 5. Clone

Jutsu: Clone Technique (range 2, rounds 2).
- **Appearance:** the clone appears on the tile with the caster's full HP (12,625).
- **Behaviour:** it acts on the caster's rule list (walked in, basic-attacked).
- **Damage:** it deals very little in this probe (31 per basic attack). The cause was not traced.
- **Lifetime:** it expires on schedule, absent from round 4 on.

## Faithful vs approximated (changes from report 1)

**Now engine-faithful:**
- Live damage settings.
- Real armour through the item path and the engine's gear pools.
- Real level-25 PvE kit with element gating.
- Summons through the engine's own template cache.
- Mini-boss retry rule (a wipe on F4 retries F4).

**Still approximated:**
- Players are driven by auto-combat with a declared rotation.
- No bloodline, keystone or weapon on the player.
- Seeded spawn tiles.
- The hazards' new rules from the encounters doc are not applied; v2 changes only the layout and Core Rupture.
- The old reference tiers' gear knobs go through one synthetic ARMOR row. The engine realises percentage damage-given
  above 100 on that row as 100, so `strong`/`elite` damage given is effectively +100. Reference only.
- Per-wave rounds count the spawn round, so neighbouring waves overlap by one round. Floor totals are exact.
