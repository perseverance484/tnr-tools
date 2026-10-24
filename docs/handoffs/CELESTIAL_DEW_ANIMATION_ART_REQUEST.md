# Art request: Celestial Dew animation layers

- **Director, 2026-10-24:** crescent moon above the player, a single celestial drop falls at their feet and splashes, a
  celestial ward appears, and a subtle celestial shield shows while the shield lasts.
- **Project:** `docs/design/celestial_dew_animation/PROJECT.md` (storyboard, how the game plays each slot, layout).
- **Reference (attach):** the live icon `art/jutsu_icons/celestial_dew/refs/ref_cd_live_icon.webp`, the look every layer
  must match: a glassy, translucent white-blue crescent with swirling lighter streaks inside, a single drop falling from
  its lower tip, a dome-shaped splash below with ripples, small four-point stars and round glassy bubbles.
- **Roles:** the art director paints the layers; Claude Code animates them (bends, scales, moves, times) by script.
- **Live-game requests/writes:** 0.

## Palette (from the icon)

Near-white `#f4f8ff`, ice blue `#bcd7ff`, sky blue `#8ab8ff`, deep glow blue `#2f5fe0`; white highlights. No other hues.

## Deliverables (each on a fully transparent canvas; nothing else on it)

How they are used (proposed motion): the crescent rests on top of the player's round portrait; a drop falls into the
portrait's centre and splashes; ripple rings spread outward and, reaching the portrait's edge, light it up as a ring of
celestial light (the ward). The layers also serve the alternative (the drop runs round the portrait's edge, splashes
below it, and the ward forms).

| Layer | What | Size |
|---|---|---|
| **M1 CRESCENT** | the icon's crescent moon alone: glassy, translucent, swirling lighter streaks inside, crisp near-white edge, soft blue glow; a C shape opening to the right, horns tapering to fine points | 1254 x 1254 |
| **D1 DROP** | one teardrop of starlight, point up: glassy, a bright highlight, a soft blue glow, a short faint sparkle trail above it | 600 x 1254 |
| **S1 SPLASH** | a small crown splash of glassy water-light seen from the front and slightly above, a few droplets thrown up, like the icon's splash | 1254 x 1254 |
| **R1 RIPPLES** | three concentric ripple rings of light seen face-on (round, flat, thin bright crests fading inward), nothing in the middle | 1254 x 1254 |
| **W1 WARD RING** | the ward as a ring: a soft glowing band of celestial light, a crisp near-white inner edge, faint swirling streaks like the crescent's inside the band, two or three tiny stars on it; the middle completely empty | 1254 x 1254, ring about 80% of the canvas, band about 8% thick |
| **P1 GLINTS** | 10-12 separate small pieces, spaced apart: four-point stars (thin, long points) and round glassy bubbles, mixed sizes (40-140 px) | 1254 x 1254 |
| **X1 SHARDS** | 8-10 separate curved shards of the ward ring's light, glowing edges, mixed sizes, spaced apart (for the ward breaking) | 1254 x 1254 |

Rules: match the icon's finish; real transparency (glows fade to clear, no grey or tinted panel, no dark fringe); no
text, runes, symbols or figures.

## Intake (Claude Code)

Raws to `art/jutsu_icons/celestial_dew/animation/raws/`. `build_strip.py` builds four strips (heal appear, shield appear,
shield static loop, shield disappear) on one clock at 36 ms per frame, 112 px frames; previews over the director's
avatar; then the asset creates (hidden), the unhide and the jutsu suggestion (heal appear; shield appear, static and
disappear), re-sending the live effects array.
