# Subaku Palace: shared timing and palette (domain floor and centre payoff)

Status: v3, 2026-11-05 (the director's arrival; QA on be8646d1). The domain-floor half (`build_domain.py`, `floor.py`) owns this file. The centre half
(`gates/`) syncs to it. Change it only by agreement. Live-game requests: 0.

Build target (director, 2026-11-05): clips at **2.5 tile heights** (338126cb, the ratio-1 change, is to be reverted
upstream), **LPC character avatars** for players (1.35 h tall, feet at groundY 0.234 h, i.e. 0.266 h below the hex
centre). The ratio-1 build is kept only as a note (design doc).

## Clock

- 50 ms per tick. Every record of the cast starts on the same tick (one snapshot). Tick 0 is the first frame after the
  textures are ready.
- The floor (static art on the ground tag) is under everything from tick 0. Each band strip covers its own hex
  (keep-outs aside) with the floor's gold engraved but unlit. On its landing tick the gold forms outward. The strip
  ends on the floor's look and dissolves to the real tile.

| Tick | Domain floor (`exports/`) | Centre (`gates/exports/anim_sbk_gates_rise_v4.webp`, SELF appear) |
|---|---|---|
| 0 to land - 1 | The band hexes are dark stone, the rails engraved but unlit. | The sigil kindles (0-5). |
| 6 | | The sigil's bands flash at the edge midpoints. |
| 7 / 8 / 10 / 11 / 13 / 14 / 16 | Bands 1.0 / 1.5 / 2.0 / 2.5 / 3.0 / 3.5 / 4.0 land. Gold forms from the hex centre over 3 ticks (white-hot head, burning trail, cracks flaring), the formed floor shows on the 4th, and an ordered dissolve takes 3 ticks. | Gates on ring 1 tear up (7-12); the palace rises (13-19). |
| 19-21 | The seal (ground appear, all 60 hexes): every rail face burns solid, the channels white-hot on 20. | **Held beat 20-21** |
| 23 | Ring 4's dissolve ends. Nothing on the floor animates after this. | The settle: the gates sink (22-37). |
| ≥ 38 | The floor is static for 3 rounds. | Nothing lingers: no buff loop, no dais. |

Landing tick of band b: whole b lands at `4 + 3*b`. Half b = d + 0.5 lands at `3*d + 5`, rounded toward the earlier ring
(50 ms late on one parity, 100 ms early on the other). Strip lengths: band and seal strips 32 frames; the centre
strip 38.

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
