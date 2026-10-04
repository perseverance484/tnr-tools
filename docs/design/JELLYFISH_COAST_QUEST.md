# Jellyfish Coast — quest + enemy package

**Status:** CANDIDATE FOR DIRECTOR REVIEW  
**Quest:** `The Crown in the Surf`  
**Manifest:** `push/61_jellyfish_coast_quest.json`  
**Generator:** `push/61_jellyfish_coast_quest.gen.py`

## Director-set constraints

- Use the approved basic Jellyfish AI avatar.
- Use the approved Royal Jellyfish avatar as the boss for the same quest.
- Use the approved TNR beach scene.
- No scene characters.
- No rewards.

All creates stay `hidden: true`. No live-game action is part of this package.

## Quest concept

A normally quiet stretch of Tidewatch Beach has been closed after luminous jellyfish begin
drifting into the shallows. The player clears one Jellyfish, discovers the swarm is following
a much larger crowned specimen, and defeats the Royal Jellyfish so the swarm disperses back
into deep water.

The story is deliberately compact. It is a small coastal incident rather than a lore-heavy
arc: visual escalation and the two fights carry the quest.

### Objective flow

```text
jelly_o0  Beach closure / assignment
  -> jelly_o1  Basic Jellyfish appears
     -> jelly_b1  Fight: 1 Jellyfish
        win  -> jelly_o2  Swarm retreats / boss reveal
        lose -> jelly_f1 -> jelly_r1 -> reset to jelly_o1
  -> jelly_o3  Royal Jellyfish confrontation
     -> jelly_b2  Fight: 1 Royal Jellyfish
        win  -> jelly_o4  Swarm disperses
        lose -> jelly_f2 -> jelly_r2 -> reset to jelly_o3
  -> jelly_win
```

Both fights use `opponent_scaled_to_user: true` and `keepOriginalPools: false`.
The quest is an `event` with no authored level/rank gate, one completion, and no reward
payload beyond the explicit empty object `{}`.

Every visible quest dialog uses `@scene:jelly_scene_bg_tidewatch`; every
`sceneCharacters` array is empty.

## AI profile — Jellyfish

| Field | Value |
| --- | --- |
| Role | Standard |
| Stored level | 100 |
| Rank | JONIN |
| Primary element | Water |
| Regeneration | 60 |
| Pools multiplier | 1 |
| Stats multiplier | 1 |
| Stat weights | Uniform, 100 in all 12 fields |
| Preferred stat | Ninjutsu |
| Preferred generals | Intelligence / Willpower |
| Avatar | `@img:avatar_basic_jellyfish_v1.webp` |
| Rules | One shared-pool use rule per kit entry, then move-towards fallback |
| Default rules | Off |

### Jellyfish kit

| Code | Jutsu | AP | Cooldown | Range/gate | Effects |
| --- | --- | ---: | ---: | --- | --- |
| EW03 | Springguard | 40 | 4 | self | Absorb 20 / 2r |
| S29 | Venom Strike | 60 | 5 | r5 / gate 6 | Damage 40; Poison 20 / 2r |
| EW01 | Tide Bolt | 60 | 3 | r5 / gate 6 | Damage 45 |
| S08 | Numbing Shot | 60 | 4 | r5 / gate 6 | Damage 40; Stun 30 / 1r |
| EW02 | Deluge Breaker | 60 | 5 | r3 / gate 4 | Damage 60; Shield 100 / 2r |

The 40 AP Springguard supplies the stance half of the 100 AP round economy while the
attacks express the creature as water pressure, venom and numbing stings.

## AI profile — Royal Jellyfish

| Field | Value |
| --- | --- |
| Role | Boss |
| Stored level | 100 |
| Rank | ELITE JONIN |
| Primary element | Water |
| Regeneration | 60 |
| Pools multiplier | 2 |
| Stats multiplier | 3 |
| Stat weights | Uniform, 100 in all 12 fields |
| Preferred stat | Ninjutsu |
| Preferred generals | Intelligence / Willpower |
| Avatar | `@img:avatar_royal_jellyfish_v1.webp` |
| Rules | One shared-pool use rule per kit entry, then move-towards fallback |
| Default rules | Off |

### Royal Jellyfish kit

| Code | Jutsu | AP | Cooldown | Range/gate | Effects |
| --- | --- | ---: | ---: | --- | --- |
| B20 | Surging Overflow | 40 | 5 | self | Damage given +30 / 3r; stats +25 / 3r |
| B03 | Sovereign Undertow | 60 | 6 | r5 / gate 6 | Redirection 3 |
| B29 | Devouring Wave | 60 | 6 | r5 / gate 6 | Damage 55; Absorb 15 / 2r |
| B16 | Sovereign Fetters | 60 | 10 | r5 / gate 6 | Damage 60; Stun 100 / 2r; Seal 100 / 2r |
| EW02 | Deluge Breaker | 60 | 5 | r3 / gate 4 | Damage 60; Shield 100 / 2r |
| B02 | Annihilating Wave | 60 | 8 | r5 / gate 6 | Damage 70 |

The boss keeps the same water identity but upgrades from nuisance control into undertow,
absorption, hard control and heavier wave pressure. No bespoke jutsu records are created;
both kits resolve entirely from the canonical shared AI pool.

## Art contract

| Logical file | Target | Bytes |
| --- | --- | ---: |
| `avatar_basic_jellyfish_v1.webp` | AI_AVATAR | 155014 |
| `avatar_royal_jellyfish_v1.webp` | AI_AVATAR | 299490 |
| `scene_bg_tidewatch_beach_v1.webp` | SCENE_BACKGROUND | 202578 |

The manifest carries matching `imgSizes` entries. The files are not yet committed to an
immutable repository ref, so this candidate deliberately uses Forge's manual-picker fallback.
Before a production run, bind the accepted bytes through `imagePack` or explicitly accept the
fallback workflow; do not substitute different bytes under these filenames.

## Validation

The generator was executed on GitHub Actions at source SHA
`618768406da4dad1fcf972feb31e28c6d4c7f638`.

`validate.py` result:

- **0 errors**
- 3 build-order warnings caused by the validator normalizing manifest `asset` to
  `gameAsset` before applying its hard-coded order table, which only contains `asset`.
  The canonical factory build-order check accepted the package and emitted
  `asset -> ai -> ai -> quest`.
- Generated manifest SHA-256:
  `f2b5e9402c6d0fceaa31ae084e74d7fbb91ffd3bd309d71e1ab5ac0f8b6caeef`.
- The committed manifest is byte-identical to that validated output.

This is repository validation only. Live-game requests/writes: **0 / 0**.
