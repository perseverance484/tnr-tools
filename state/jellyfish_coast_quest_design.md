# Jellyfish Coast — candidate quest package

**Status:** CANDIDATE / AWAITING DIRECTOR FINAL ACCEPTANCE  
**Repository baseline:** `ff347191848648c80731436f530fca0a688a77e8`  
**Live-game requests/writes:** 0 / 0

## Quest

**Name:** The Crown in the Surf  
**Type:** event  
**Publishing:** hidden on create  
**Rewards:** none (`content.reward = {}`)  
**Scene characters:** none  
**Scene background:** one Tidewatch Beach `SCENE_BACKGROUND` on every scene-bearing objective  
**Structure:** two dialog-gated battles; loss shows retreat prose and resets to the pre-fight dialog.

Flow:

`Beach arrival -> Jellyfish reveal -> Jellyfish battle -> Royal reveal -> Royal battle -> shore reopens -> win`

Both battles use `opponent_scaled_to_user: true` and one enemy. The manifest deliberately does not add a rank, required level, currency, experience, item, token, prestige, or other reward/gate value that the director did not request.

## AI — Jellyfish

**Role:** Standard PvE Enemy  
**Record level:** 100 reusable AI record  
**Rank:** JONIN  
**Element:** Water  
**Preferred stat:** Ninjutsu  
**Preferred generals:** Intelligence / Willpower  
**Regeneration:** 60  
**Pools multiplier:** 1  
**Stats multiplier:** 1  
**Stat ratio:** uniform across all twelve fields  
**Quest use:** player-scaled encounter  
**Avatar:** `avatar_basic_jellyfish_v1.webp`

Shared-pool kit, in rule priority order:

| Code | Jutsu | AP | Cooldown | Effect summary |
|---|---|---:|---:|---|
| EW02 | Deluge Breaker | 60 | 5 | damage 60; shield 100/2r |
| S29 | Venom Strike | 60 | 5 | damage 40; poison 20/2r |
| S08 | Numbing Shot | 60 | 4 | damage 40; stun 30/1r |
| S28 | Enervating Strike | 60 | 4 | damage 40; decrease stat 15/2r |
| EW01 | Tide Bolt | 60 | 3 | damage 45 |

Rules are generated from the pool's exact range gates and end with `move_towards_opponent`. `includeDefaultRules` remains false, matching the current project AI generator path.

## AI — Royal Jellyfish

**Role:** Boss PvE Enemy  
**Record level:** 100 reusable AI record  
**Rank:** ELITE JONIN  
**Element:** Water  
**Preferred stat:** Ninjutsu  
**Preferred generals:** Intelligence / Willpower  
**Regeneration:** 60  
**Pools multiplier:** 2  
**Stats multiplier:** 3  
**Stat ratio:** uniform across all twelve fields  
**Quest use:** player-scaled boss encounter  
**Avatar:** `avatar_royal_jellyfish_v1.webp`

Shared-pool kit, in rule priority order:

| Code | Jutsu | AP | Cooldown | Effect summary |
|---|---|---:|---:|---|
| B16 | Sovereign Fetters | 60 | 10 | damage 60; stun 100/2r; seal 100/2r |
| B03 | Sovereign Undertow | 60 | 6 | redirection 3 |
| B29 | Devouring Wave | 60 | 6 | damage 55; absorb 15/2r |
| B12 | Sovereign Ruin | 60 | 10 | damage-given down x2; healing down |
| EW02 | Deluge Breaker | 60 | 5 | damage 60; shield 100/2r |
| B02 | Annihilating Wave | 60 | 8 | damage 70 |

The boss uses no event-only jutsu. This keeps the content on the current shared-AI-pool doctrine and avoids creating another isolated kit family.

## Art files

- `avatar_basic_jellyfish_v1.webp` — processed AI avatar
- `avatar_royal_jellyfish_v1.webp` — processed AI avatar
- `scene_bg_tidewatch_beach_v1.webp` — approved beach background processed to 3:2 lossy WebP q85

The candidate manifest currently uses Forge's manual-picker fallback with exact `imgSizes`. A repo-backed `imagePack` should be added only after these exact approved bytes are committed at an immutable SHA.

## Implementation source

- Generator: `push/61_jellyfish_coast_quest.gen.py`
- Generated manifest: `push/61_jellyfish_coast_quest.json`

The generator uses `Factory`, `enemy.py`, and `32b_DATA_pool.json`; no jutsu payloads are hand-authored.
