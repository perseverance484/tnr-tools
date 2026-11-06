# Art request: Subaku Palace centre payoff, painted layers (optional upgrade)

- **For:** the art director (Image Production)
- **From:** Fable / Claude (2026-11-05)
- **Status:** OPTIONAL. The programmatic strip ships now: `art/subaku_palace/gates/exports/anim_sbk_gates_rise_v5.webp` (2.5 hex-height clip, LPC caster; see the gates README). Painted gate, palace and sigil layers would be reduced to the same 50 px grid, keep-clear zones and beat.
- **Jutsu:** Subaku Palace `jELEiw5W3N4m2R3oJm3Pk` (player EVENT). Battle text: "gates of red sandstone carved with snarling
  faces tear free of the ground, and the shadow of the demon palace falls across the field".
- **Style references (attach, style only):** `art/subaku_palace/refs/ref_domain_tile_c_1254.png` (material: charcoal
  basalt, red-glow cracks, bevelled burnished gold); `art/jutsu_icons/scroll_jutsu/originals_live/live_subaku_palace.webp`
  (the gates' subject: red sandstone slabs crowned with oni faces).
- **Palette:** `art/subaku_palace/TIMING.md` only: red sandstone `#5a1e14 #7a2a1c #a8432a #c9653d #e3906a`; demon gold
  `#8a5a12 #c48a1c #e8b43a`; burning gold `#ffcf4a #ffe58a`; ember `#6e0c08 #b81c10 #ff4a1c #ff963c`; shadow
  `#160a09`. No green, violet or cyan.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`, one layer per fresh session; raw QC with `rawqc.py` before
  processing. Native transparency preferred, otherwise a lime key.
- **Live-game requests/writes:** 0.

## Why a painted layer helps, and its limit

The clip is delivered at 50 px, so a gate is about 12 x 20 source pixels and its face about 10 x 9. A painted
source helps only if it is drawn for that size: big flat planes, one strong light from the top left, and a face built
from four shapes (V brows, slanted eyes, fangs, a dark maw). Detail finer than that is averaged away.

## Layers (each on a fully transparent canvas, nothing else on it)

| Layer | Prompt | Size |
|---|---|---|
| **G1 ONI GATE** | Premium retro 32-bit pixel art, hard pixel edges, no gradients or blur, 16-24 colours, rim light from the top left. A single upright slab gate of red sandstone, front view, tall rectangle (proportion 3 wide : 5 tall). Its top third is carved into a snarling oni demon face: heavy V-shaped brows, two slanted eyes glowing burning gold, a broad snout, a wide open maw with two upper and two lower gold fangs and ember-red light in the throat, two short curved gold horns at the top corners. A band of burnished demon gold under the face. Below it, a carved double door panel with gold studs and a thin ember crack down the middle. Big flat planes, chunky readable shapes, dark outline. Nothing behind it, no ground, no shadow, no glow halo. | 1254 x 1254 |
| **P1 MOON-GATE PALACE** | Same style and palette. A demon palace gatehouse, front view, symmetric: two slim three-tier pagoda towers with near-black roofs edged in burnished gold and upturned tips, red-lacquer walls, small ember-lit windows; between them a lacquered wall pierced by a large perfectly round moon gate, the round opening EMPTY and fully transparent, ringed by a thin gold arch with a small horned oni crest at its top. Strong silhouette, flat planes, dark outline. Nothing in the round opening; no ground, no sky, no glow halo. | 1254 x 1254 |
| **S1 SIGIL** | Same style and palette. Seen from directly above: a ritual sigil of burnished, bevelled gold bands: an outer ring, an inner ring, two spiral arms turning out from the centre, six straight bands leaving the outer ring at even 60 degree intervals, thin ember-red cracks between them. No runes, letters or symbols. No background, no stone. | 1254 x 1254 |

Rules (art bible and spec): glow is rim light on edges only, never a painted disc, halo or panel; enclosed openings (the
moon gate, the rings' interiors) must be transparent or the key colour; no text, kanji or runes; no franchise
insignia.

## What Claude does with them

Raw QC, key, crop. Reduce G1 to 12 x 20 and P1 to the 42 x 28 palace box on the 50 px grid, with a palette lock to
TIMING.md. Swap them into `build_gates.py` for the hand-placed `GATE_MAP` and `palace_sprite`, keeping the moon-gate cut
round the caster's pin. Rebuild with the same checks (2 px margin, palette, white-hot ticks, 0% avatar-disc cover).
Re-preview with the shared harness. New filenames (`_v3`).
