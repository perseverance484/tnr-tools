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

| Layer | What | Size |
|---|---|---|
| **M1 CRESCENT** | the icon's crescent moon alone: glassy, translucent, swirling lighter streaks inside, crisp near-white edge, soft blue glow; a C shape opening to the right, horns tapering to fine points | 1254 x 1254 |
| **D1 DROP** | one teardrop of starlight, point up: glassy, a bright highlight, a soft blue glow, a short faint trail of sparkle above it | 600 x 1254 |
| **S1 SPLASH** | the icon's splash alone, side view: a low dome-shaped crown of glassy water-light with a few droplets thrown up, ripple rings on the ground below it | 1600 x 700 |
| **W1 WARD** | a celestial ward seen from the front: a round dome or sphere shell of light, almost clear in the middle, bright near-white rim, a few faint swirling streaks like the crescent's, two or three tiny stars on it | 1254 x 1254 |
| **P1 GLINTS** | 10-12 separate small pieces, spaced apart: four-point stars (thin, long points) and round glassy bubbles, mixed sizes (40-140 px) | 1254 x 1254 |
| **X1 SHARDS** | 8-10 separate curved shards of the ward's glassy light, glowing edges, mixed sizes, spaced apart (for the ward shattering) | 1254 x 1254 |

Rules: match the icon's finish; real transparency (glows fade to clear, no grey or tinted panel, no dark fringe); no
text, runes, symbols or figures.

## Intake (Claude Code)

Raws to `art/jutsu_icons/celestial_dew/animation/raws/`. `build_strip.py` builds four strips (heal appear, shield appear,
shield static loop, shield disappear) on one clock at 36 ms per frame, 112 px frames; previews over the director's
avatar; then the asset creates (hidden), the unhide and the jutsu suggestion (heal appear; shield appear, static and
disappear), re-sending the live effects array.
