# Jellyfish Coast — quest + enemy package

**Status:** CANDIDATE / READY FOR DIRECTOR REVIEW  
**Quest:** `The Crown in the Surf`  
**Manifest:** `push/61_jellyfish_coast_quest.json`  
**Generator:** `push/61_jellyfish_coast_quest.gen.py`  
**Live-game requests/writes:** 0 / 0

## Director constraints

- Basic Jellyfish and Royal Jellyfish are the two combat AIs.
- Royal Jellyfish is the boss escalation.
- Use the approved Tidewatch beach scene.
- No scene characters.
- No rewards.
- All creates remain hidden. Publishing is separate.

## Quest flow

A quiet beach has been closed after luminous jellyfish begin occupying the shallows.
The player clears one Jellyfish, discovers the swarm is following a larger crowned
specimen, then defeats the Royal Jellyfish so the swarm returns to deep water.

```text
Beach arrival
  -> Jellyfish reveal
  -> Jellyfish battle
     lose -> retreat dialog -> reset to Jellyfish reveal
     win  -> swarm gathers offshore
  -> Royal Jellyfish reveal
  -> Royal Jellyfish battle
     lose -> retreat dialog -> reset to Royal reveal
     win  -> swarm disperses
  -> completion dialog
  -> win
```

Both battles are one-enemy, dialog-gated `start_battle` nodes with
`opponent_scaled_to_user: true`, `keepOriginalPools: false`, and explicit failure routing.
Every visible scene uses `@scene:jelly_scene_bg_tidewatch`; all `sceneCharacters` arrays are empty.
The quest is an `event` with no authored progression gate. `content.reward` is exactly `{}`.

## Jellyfish

- role: Standard PvE Enemy
- stored level: 100
- rank: JONIN
- element: Water
- preferred stat: Ninjutsu
- preferred generals: Intelligence / Willpower
- regeneration: 60
- pools multiplier: 1
- stats multiplier: 1
- stat ratio: uniform
- avatar: `@img:avatar_basic_jellyfish_v1.webp`

Shared-pool kit:

| Code | Jutsu | AP | CD | Effects |
| --- | --- | ---: | ---: | --- |
| EW03 | Springguard | 40 | 4 | Absorb 20 / 2r |
| S29 | Venom Strike | 60 | 5 | Damage 40; Poison 20 / 2r |
| EW01 | Tide Bolt | 60 | 3 | Damage 45 |
| S08 | Numbing Shot | 60 | 4 | Damage 40; Stun 30 / 1r |
| EW02 | Deluge Breaker | 60 | 5 | Damage 60; Shield 100 / 2r |

Rules are generated from the pool's exact distance gates and end in an unconditional
`move_towards_opponent` fallback.

## Royal Jellyfish

- role: Boss PvE Enemy
- stored level: 100
- rank: ELITE JONIN
- element: Water
- preferred stat: Ninjutsu
- preferred generals: Intelligence / Willpower
- regeneration: 60
- pools multiplier: 2
- stats multiplier: 3
- stat ratio: uniform
- avatar: `@img:avatar_royal_jellyfish_v1.webp`

Shared-pool kit:

| Code | Jutsu | AP | CD | Effects |
| --- | --- | ---: | ---: | --- |
| B20 | Surging Overflow | 40 | 5 | Damage given +30 / 3r; stats +25 / 3r |
| B03 | Sovereign Undertow | 60 | 6 | Redirection 3 |
| B29 | Devouring Wave | 60 | 6 | Damage 55; Absorb 15 / 2r |
| B16 | Sovereign Fetters | 60 | 10 | Damage 60; Stun 100 / 2r; Seal 100 / 2r |
| EW02 | Deluge Breaker | 60 | 5 | Damage 60; Shield 100 / 2r |
| B02 | Annihilating Wave | 60 | 8 | Damage 70 |

No bespoke jutsu are created; both enemies use the canonical shared AI pool.

## Art contract

| Logical file | Type | Bytes |
| --- | --- | ---: |
| `avatar_basic_jellyfish_v1.webp` | AI_AVATAR | 155014 |
| `avatar_royal_jellyfish_v1.webp` | AI_AVATAR | 299490 |
| `scene_bg_tidewatch_beach_v1.webp` | SCENE_BACKGROUND | 202578 |

The manifest carries these exact `imgSizes`. The files are supplied through Forge's manual-picker
fallback for this candidate; no live upload or live game action has been performed.

## Validation performed

The final manifest was rebuilt on a clean branch from the previously factory-generated shape,
with kit ids/rules resolved directly from `32b_DATA_pool.json`.

Checks completed before commit:

- exactly 4 entries in canonical build order: asset -> AI -> AI -> quest;
- zero new jutsu records;
- shared-pool codes resolve to literal live ids;
- one unconditional movement fallback ends each AI rule chain;
- exact range gates come from the shared pool;
- quest graph has one start and no dangling edges;
- both battles are dialog-gated, scaled, one-enemy fights with fail routes;
- reset targets are already in-flow;
- no scene characters;
- reward object exactly `{}`;
- no player-facing em/en dashes;
- no repository answer-layer name collision for either AI, the quest, or the background asset.

The earlier full repository validator run on the same factory-generated quest/AI shape reported
0 errors; its three build-order warnings were traced to the validator's asset -> gameAsset
normalization occurring before a lint table that still names asset. That validator defect does
not change the manifest order accepted by Factory.
