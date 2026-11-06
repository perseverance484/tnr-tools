# Subaku Palace: shared timing and palette (domain floor and centre payoff)

Status: v5, 2026-11-06 (the bloom polished: overlapping blooms; RUL-2026-11-06-128). The domain-floor half (`build_domain.py`, `floor.py`) owns this file. The centre half
(`gates/`) syncs to it. Change it only by agreement. Live-game requests: 0.

Build target (director, 2026-11-05): clips at **2.5 tile heights** (338126cb, the ratio-1 change, is to be reverted
upstream), **LPC character avatars** for players (1.35 h tall, feet at groundY 0.234 h, i.e. 0.266 h below the hex
centre). The ratio-1 build is kept only as a note (design doc).

## Clock

- 50 ms per tick. Every record of the cast starts on the same tick (one snapshot). Tick 0 is the first frame after the
  textures are ready.
- The floor (static art on the ground tag) is under everything from tick 0. Each band strip covers its WHOLE hex with
  the floor without any gold (no keep-out, director 2026-11-05), so tick 0 shows the domain as bare stone. The gold
  blooms outward as one wave. Rings ignite 4 ticks apart, and inside each hex the head runs from the centre to the
  edges in 8 ticks, so each ring ignites when the previous ring's head is halfway out and the blooms overlap into one
  front. Where the head passes the cover opens on the real tile; a 3-tick lit-rail trail follows.

| Tick | Domain floor (`exports/`) | Centre (`gates/exports/anim_sbk_gates_rise_v5.webp`, SELF appear) |
|---|---|---|
| 0-6 | The domain is bare stone (no gold on the 56 band hexes). | The sigil kindles (0-5); its bands flash at the edge midpoints (6). |
| **7** | **Ring 1 ignites** (band 1.0). | **Gates on ring 1 tear up.** |
| 9 / 11 / 13 / 15 / 17 / 19 | Bands 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 ignite. Each hex: head centre -> edges over 8 ticks, then a 3-tick trail. | The palace rises. |
| 27 | The last head reaches the rim. | |
| **28-30** | **The final pulse (the seal, ground appear, all 60 hexes):** every rail face burns solid, the channels white-hot on 29. The last band clip ends on 30. | **Held beat 29-30.** |
| 31-43 | The floor is static. | The settle (v5 runs to 43). |
| ≥ 44 | The floor is static for 3 rounds. | Nothing lingers. |

Ignition tick of band b: whole b = d at `3 + 4*d`. Half b = d + 0.5 at `5 + 4*d`, exactly between its two rings
(100 ms late on one parity, 100 ms early on the other). Strip lengths: band and seal strips 36 frames; the centre
strip 44 (v5).
Fighters standing in the domain are covered by its stone from tick 0 until the bloom passes them: at most 29 ticks
(1.45 s, ring 4). The director accepted this.

## Geometry (true scale in the previews)

- Tile box 132 x 66 px. Clip 165 px square, from the 50 px rendition, linear.
- Frames are authored on the 50 px grid with hard alpha (no dither) and exported x3 nearest (150 px). The floor tile is
  128 px.
- The caster's own hex is NOT in the AOE_SPIRAL_SHOOT footprint (`targeting.ts:56-58`). After the cast it shows the
  bare board (no dais, no mechanic change, director 2026-11-05).

## Palette (no green)

| Role | Hex |
|---|---|
| shadow / veil | `#160a09` |
| stone (basalt, 7 tones, plus grain) | `#302c2e` `#282527` `#383232` `#2c2828` `#342f2e` `#242123` `#3c3635`; mortar `#0c0808` / red-lit `#1e0808` |
| floor joints (tapered ember) | `#5c0a06` `#a8180c` `#ee3c16` `#ff7832` |
| red sandstone (gates) | `#5a1e14` `#7a2a1c` `#a8432a` `#c9653d` `#e3906a` |
| demon gold (floor rails, double rail) | outline `#221206`, groove `#46280a`, rail `#764a12` `#b07c28` `#deac4c` `#fadc96` |
| demon gold (lit body) | `#8a5a12` `#c48a1c` `#e8b43a` |
| burning gold (energy) | `#ffcf4a` `#ffe58a` `#fff4c8` (white-hot only in the head) |
| ember (cracks) | `#6e0c08` `#b81c10` `#ff4a1c` `#ff963c` |

Reserved: cyan (safe hexes elsewhere). No violet, no bile or acid green.
