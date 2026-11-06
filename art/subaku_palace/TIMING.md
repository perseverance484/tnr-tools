# Subaku Palace: shared timing and palette (domain floor ↔ centre payoff)

Status: v1, 2026-11-05. The domain-floor half (Fable, `build_domain.py`) owns this file. The centre-payoff half (the
second agent: sigil, gates and palace on the caster, the self-buff look) syncs to it. Change it only by agreement.
Live-game requests: 0.

## Clock

- 50 ms per tick. All records of the cast start on the same tick (one snapshot). Tick 0 is the first frame after the
  textures are ready.
- The ground floor (static art) is visible from tick 0 on all 60 hexes. The engine cannot delay static art, so the
  spread is drawn as clips over it: a dark veil per hex that lifts when its ring lands.

| Tick | Domain floor (this half) | Centre (second agent) |
|---|---|---|
| 0-5 | All 56 band hexes veiled dark (alpha 0.55); the floor shows dim through it | anticipation: the sigil kindles at the caster's feet |
| 6 | | the sigil's first spiral turn leaves the caster's hex |
| 7 | band 1.0 lands (ring 1) | |
| 9 | band 1.5 lands | |
| 10 | band 2.0 lands (ring 2) | |
| 12 | band 2.5 lands | |
| 13 | band 3.0 lands (ring 3) | |
| 15 | band 3.5 lands | |
| 16 | band 4.0 lands (ring 4, the rim) | |
| 18-28 | seal: one soft pulse along every band on all 60 hexes, peak tick 20 (the ground tag's own appear) | gates rise 17-24, tear free of the earth |
| 24-30 | | **held beat**: the palace stands |
| 30-38 | floor settled: static floor only | settle: the gates sink into the floor; settle frames end on the floor's look |
| ≥ 40 | nothing animates; floor static for 3 rounds | buff: self-buff loop + dais tile (2 rounds) |

Landing tick of a band b (mean hex distance over the two column parities): `int(4 + 3*b + 0.5)`.
On landing, each hex ignites in three levels from its centre to its edges, 0.75 tick apart (gold bands first, cracks
half a tick later): white-hot one tick, burning gold, then decaying to ember by about +10 ticks.

Strip lengths: band and seal strips 32 frames. The centre appear may run to 40 frames (2.0 s). Keep it ≤ 80 frames.

## Geometry (true scale used in previews)

Tile box 132 x 66 px; clip 165 px square (2.5 tile heights), from the 50 px rendition, linear. Authoring at 100 px
per frame: the hex box is 80 x 40 centred; at the 50 px rendition 40 x 20. The caster's own hex is NOT in the
AOE_SPIRAL_SHOOT footprint (`targeting.ts:56-58`): the domain has a hole under the caster. That hex belongs to the
centre half (SELF static art = the dais).

## Palette (no green)

| Role | Hex |
|---|---|
| shadow / veil | `#160a09` |
| stone (warm basalt, from the director's tile) | dark grey with a red-sandstone cast |
| red sandstone (gates) | `#5a1e14` `#7a2a1c` `#a8432a` `#c9653d` `#e3906a` |
| demon gold (bands at rest) | `#8a5a12` `#c48a1c` `#e8b43a` |
| burning gold (energy) | `#ffcf4a` `#ffe58a` `#fff4c8` (white-hot, one tick only) |
| ember (cracks) | `#6e0c08` `#b81c10` `#ff4a1c` `#ff963c` |

Reserved: cyan (safe hexes elsewhere), no violet, no bile/acid green.
