# Subaku Palace: shared timing and palette (domain floor and centre payoff)

Status: v7.1, 2026-11-06 (QA r4: tile v4 with bleed, uncut pulse with pre-step) (the director's pick: light-only, no spill, his own tile; RUL-2026-11-06-128). The domain-floor half
(`build_domain.py`, `classic.py`) owns this file. The centre half
(`gates/`) syncs to it. Change it only by agreement. Live-game requests: 0.

Build target (director, 2026-11-05): clips at **2.5 tile heights** (338126cb, the ratio-1 change, is to be reverted
upstream), **LPC character avatars** for players (1.35 h tall, feet at groundY 0.234 h, i.e. 0.266 h below the hex
centre). The ratio-1 build is kept only as a note (design doc).

## Clock

- 50 ms per tick. One snapshot creates every record of the cast, but each record's clip starts when its own images
  are ready, so records can start a few ticks apart (QA B4). Tick 0 is the first frame after the
  textures are ready.
- The floor (static art on the ground tag) is the director's own tile at rest, under everything from tick 0 on all
  60 hexes. There is no cover. The band strips draw only on the bands: the light runs out from each hex centre along
  the bands (4 ticks centre to edge, on into the neighbours to 1.5 hex radii), rings igniting 4 ticks apart, so it
  reads as one outward wave. The head is the band white-hot; the band cools over 3 ticks back to his gold.

| Tick | Domain floor (`exports/`) | Centre (`gates/exports/anim_sbk_gates_rise_v6.webp`, SELF appear) |
|---|---|---|
| 0-6 | The domain rests: his floor, unlit. | The sigil kindles (0-5); its bands flash at the edge midpoints (6). |
| **7** | **Ring 1 ignites** (band 1.0). | **Gates on ring 1 tear up.** |
| 9 / 11 / 13 / 15 / 17 / 19 | Bands 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 ignite. | The palace rises. |
| 23-25 | The last head reaches the rim (ring 4's light stays in its own hexes: no spill); the last band clip ends on 25. | |
| **26-32** | **The final pulse (the seal, ground appear, all 60 hexes):** every band flares uncut on its core, ramping 18 / 40 / 75 / 100 / 70 / 40 / 15 %, white-hot on 29. | **Held beat 29-30.** |
| 33-43 | The floor rests. | The settle (v6 runs to 43). |
| ≥ 44 | The floor is static for 3 rounds. | Nothing lingers. |

Ignition tick of band b: whole b = d at `3 + 4*d`. Half b = d + 0.5 at `5 + 4*d`, exactly between its two rings
(100 ms late on one parity, 100 ms early on the other). Strip lengths: band and seal strips 36 frames; the centre
strip 44 (v6). Fighters are never covered by a cover: only band pixels are drawn (LPC body at most 23 %; the wide AI avatar beside the caster 33 % on 6 frames).

## Geometry (true scale in the previews)

- Tile box 132 x 66 px. Clip 165 px square, from the 50 px rendition, linear.
- Frames are authored on the 50 px grid with hard alpha (no dither) and exported x3 nearest (150 px). The floor tile is
  128 px.
- The caster's own hex is NOT in the AOE_SPIRAL_SHOOT footprint (`targeting.ts:56-58`). After the cast it shows the
  bare board (no dais, no mechanic change, director 2026-11-05).

## Palette (no green)

| Role | Hex |
|---|---|
| stone, mortar glow, resting gold | the director's tile (ref c), unchanged colours |
| red sandstone (gates) | `#5a1e14` `#7a2a1c` `#a8432a` `#c9653d` `#e3906a` |
| band outline / groove (redrawn bands) | `#1c1008` / `#22140a`; rails textured with his gold |
| cooling band (the trail) | `#ffe58a` -> `#ffcf4a` -> `#f0ba54` |
| burning gold (energy) | `#ffcf4a` `#ffe58a` `#fff4c8` (white-hot only in the head) |
| ember (cracks) | `#6e0c08` `#b81c10` `#ff4a1c` `#ff963c` |

Reserved: cyan (safe hexes elsewhere). No violet, no bile or acid green.
