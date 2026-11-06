# Subaku Palace: shared timing and palette (domain floor and centre payoff)

Status: v2, 2026-11-05. The domain-floor half (`build_domain.py`, `floor.py`) owns this file. The centre half
(`gates/`) syncs to it. Change it only by agreement. Live-game requests: 0.

Build target (director, 2026-11-05): clips at **2.5 tile heights** (338126cb, the ratio-1 change, is to be reverted
upstream), **LPC character avatars** for players (1.35 h tall, feet at groundY 0.234 h, i.e. 0.266 h below the hex
centre). The ratio-1 build is kept only as a note (design doc).

## Clock

- 50 ms per tick. Every record of the cast starts on the same tick (one snapshot). Tick 0 is the first frame after the
  textures are ready.
- The floor (static art on the ground tag) is visible from tick 0 on all 60 hexes. The game has no per-tag delay,
  so the spread is drawn by clips over it. Each band strip holds its own hex in shadow until its band lands.

| Tick | Domain floor (`exports/`) | Centre (`gates/exports/anim_sbk_gates_rise_v2.webp`, SELF appear) |
|---|---|---|
| 0-5 | The 56 band hexes are veiled (a 50 % dither). The floor shows dim through it. | The sigil kindles at the caster's feet. |
| 6 | | The sigil's bands flash at the edge midpoints. |
| 7 | Band 1.0 lands (ring 1): its veil lifts and the current starts at each hex centre. | Gates on ring 1 tear up (7-12). |
| 9 / 10 / 12 / 13 / 15 / 16 | Bands 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 land. | The palace rises (13-19). |
| 18-26 | The seal: one breath through every channel on all 60 hexes, peak tick 20 (ground appear). | **Held beat 20-21** |
| 22-37 | The currents decay to the static floor. | The settle: the gates sink (22-37). |
| ≥ 38 | Nothing animates. The floor is static for 3 rounds. | Nothing lingers: no buff loop, no dais. |

Landing tick of band b (the mean hex distance over the two column parities): `int(4 + 3*b + 0.5)`.
The current travels from the hex centre at one hex pitch per 3 ticks. That is the ring spacing, so each band's front
reaches the next band's hex centres as they land. It overshoots its own hex edge by 0.3 hex radius, fading.
The cracks flare one tick behind the head. Strip lengths: band and seal strips 32 frames; the centre strip 38.

## Geometry (true scale in the previews)

- Tile box 132 x 66 px. Clip 165 px square, from the 50 px rendition, linear.
- Frames are authored on the 50 px grid with hard alpha and exported x3 nearest (150 px).
- The caster's own hex is NOT in the AOE_SPIRAL_SHOOT footprint (`targeting.ts:56-58`). After the cast it shows the
  bare board (no dais, no mechanic change, director 2026-11-05).

## Palette (no green)

| Role | Hex |
|---|---|
| shadow / veil | `#160a09` |
| stone (warm basalt, from the director's tile) | `#2a2422` `#322b28` `#241f1e` `#38302c` |
| red sandstone (gates) | `#5a1e14` `#7a2a1c` `#a8432a` `#c9653d` `#e3906a` |
| demon gold at rest (floor bands, bevelled) | outline `#281506`, `#603a0e` `#8c5c18` `#b4802a` `#d6a446` `#f0cc7c` |
| demon gold (lit body) | `#8a5a12` `#c48a1c` `#e8b43a` |
| burning gold (energy) | `#ffcf4a` `#ffe58a` `#fff4c8` (white-hot only in the head) |
| ember (cracks) | `#6e0c08` `#b81c10` `#ff4a1c` `#ff963c` |

Reserved: cyan (safe hexes elsewhere). No violet, no bile or acid green.
