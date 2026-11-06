# Subaku Palace: shared timing and palette (domain floor and centre payoff)

Status: v6, 2026-11-06 (QA r3 on 0534902e: rail-width seal ramp, 4-tick hex run, node head; RUL-2026-11-06-128). The domain-floor half (`build_domain.py`, `floor.py`) owns this file. The centre half
(`gates/`) syncs to it. Change it only by agreement. Live-game requests: 0.

Build target (director, 2026-11-05): clips at **2.5 tile heights** (338126cb, the ratio-1 change, is to be reverted
upstream), **LPC character avatars** for players (1.35 h tall, feet at groundY 0.234 h, i.e. 0.266 h below the hex
centre). The ratio-1 build is kept only as a note (design doc).

## Clock

- 50 ms per tick. One snapshot creates every record of the cast, but each record's clip starts when its own images
  are ready, so records can start a few ticks apart (QA B4). Tick 0 is the first frame after the
  textures are ready.
- The floor (static art on the ground tag) is under everything from tick 0. Each band strip covers its WHOLE hex with
  the floor without any gold (no keep-out, director 2026-11-05), so tick 0 shows the domain as bare stone. The gold
  blooms outward as one wave. Rings ignite 4 ticks apart, and inside each hex the light runs along the rails from the
  centre to the edge midpoints in 4 ticks, so each ring's rails reach the next ring's as it ignites. The head is a
  bright node filling the rail. Where it passes the cover opens on the real tile; a 2-tick trail follows on the rail.

| Tick | Domain floor (`exports/`) | Centre (`gates/exports/anim_sbk_gates_rise_v6.webp`, SELF appear) |
|---|---|---|
| 0-6 | The domain is bare stone (no gold on the 56 band hexes). | The sigil kindles (0-5); its bands flash at the edge midpoints (6). |
| **7** | **Ring 1 ignites** (band 1.0). | **Gates on ring 1 tear up.** |
| 9 / 11 / 13 / 15 / 17 / 19 | Bands 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 ignite. Each hex: head centre -> edge midpoints over 4 ticks, then a 2-tick trail. | The palace rises. |
| 23 | The last head reaches the rim; the last band clip ends on 25. | |
| **27-32** | **The final pulse (the seal, ground appear, all 60 hexes):** the rails light at their own width, ramping 40 / 75 / 100 / 70 / 40 / 15 %, white-hot on 29, off the fighter standing areas and meter rows. | **Held beat 29-30.** |
| 31-43 | The floor is static. | The settle (v5 runs to 43). |
| ≥ 44 | The floor is static for 3 rounds. | Nothing lingers. |

Ignition tick of band b: whole b = d at `3 + 4*d`. Half b = d + 0.5 at `5 + 4*d`, exactly between its two rings
(100 ms late on one parity, 100 ms early on the other). Strip lengths: band and seal strips 36 frames; the centre
strip 44 (v5).
Fighters standing in the domain are covered by its stone from tick 0 until the bloom passes them: at most 24 ticks
(1.2 s, ring 4). The director accepted this. The ring-1 cover has a notch at its bottom centre that keeps the
caster's head and meter rows clear during the anticipation.

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
