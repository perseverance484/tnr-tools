# Forbidden Chakra Fury — painted floor ripple source art (section 7)

Based on `perseverance484/tnr-tools/docs/handoffs/FORBIDDEN_CHAKRA_FURY_ANIMATION_ART_REQUEST.md`, section 7 (2026-11-16).

These are two **separately painted, 1254 × 1254, transparent RGBA PNG** key layers for the `build_strips.py --v2` floor-ripple pass. They are not animations or live game uploads.

| Source PNG | Role | Distinguishing features |
| --- | --- | --- |
| `E1_Ripple_Web.png` | First radial floor ripple | Nine jagged violet branches with uneven forks; heavier, more violent trunks and fine tips |
| `E2_Second_Wave.png` | Chasing ripple | A separate nine-ray topology with different angles/forks, cleaner and visibly thinner, brighter lilac cores |

## Rigging and compositing

- Source viewpoint is **flat orthographic straight above**. Both layers are **unsquashed** squares. The script applies the 2:1 floor squash; do not pre-flatten the source PNGs.
- Both webs radiate from their shared exact center at approximately (627,627), reaching about 45% of the full canvas width in each direction.
- Reveal the ripple outward from that point with a sharp white-hot leading edge (as specified by section 7).
- The imagery comprises only independent free-standing violet lightning paths. There is **no ground tile**, filled backdrop, ring, explosion, character, symbol or text on either layer.
- Palette: `#9b4dff` to `#c58bff` bodies, `#f4eaff` bright cores, sparse deep-violet shading `#24093f`. **No crimson**. Raw chakra, not fire.
- Both retain genuine zero-alpha negative space and narrow translucent glow close to the lightning, so the battlefield underneath remains visible.

## Checks

- Native dimensions and genuine transparency verified by image inspection.
- Previewed at the intended 2:1 floor squeeze against a medium-toned battlefield. E1 and E2 have distinct shapes; E2 is thinner. Final quality and timing should still be checked in the game's scripted reveal and board preview before any upload.
- No repository, jutsu or live-asset changes were made.

## Final generation prompts (normalized)

- **E1:** Flat-on unsquashed web of nine violent jagged violet chakra branches from the exact canvas center, each with 1–3 forks, thick near the origin tapering to fine ends at about 45% canvas-width radius, crisp white-lilac filament cores and narrow translucent violet halos, fully transparent outside.
- **E2:** A distinct brighter, thinner chasing web with nine new radial branch angles and different forks, the same central alignment and radial reach, and clear negative spaces with no tinted ground or burst.

Created with built-in image generation, using the A Fury Burst artwork as a style reference for E1 and selecting an independently rendered E2 to keep its lines visually distinct.
