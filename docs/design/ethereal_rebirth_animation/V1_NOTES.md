# Ethereal Rebirth cast animation: v1 build notes

- **Art:** the art director's sheet `art/jutsu_icons/ethereal_rebirth/animation/raws/anim_er_sheet_v1.png` (1536 × 1024,
  delivered 2026-10-24): R1 gold ribbon, R2 blue ribbon, C1 core, F1 flecks and K1 peak reference, on grey glow-tinted
  panels (not transparent).
- **Cut out:** `extract_layers.py` keeps the saturated or near-white painted forms and drops the panels and the baked
  glow (the build adds its own); `layers/` holds the results; check sheet `layers_extracted_check.png` (dark, grass, snow).
- **Built:** `build_strip.py` → `exports/anim_ethereal_rebirth_v1.webp`: 40 frames of 128 px, intended speed 60 ms
  (2.4 s), 302,386 bytes (ceiling 460,800). Preview `v1_preview.gif` (128 and 50 px over dark, grass and snow, stand-in
  token), frames `v1_frames.png`.
- **Method:** each ribbon painting is straightened (its painted wave braided on a curve), shrunk, and warped onto the
  spin path as a chain of edge-sharing quads (perspective transform per quad, Pillow only): one drawing per ribbon on
  continuous curves. Soft front/back crossover; the far side fades out inside the token; the near side goes see-through
  over the face; soft ends.
- **Preflight:** `artpreflight.py --type ANIMATION`: 1 error, `soft_edges` 72.6% partial alpha against a 5% ceiling. The
  same known validator gap as Chakra Overflow (glow effects are semi-transparent by design; the stock animation it
  replaced scored 51%). Not an art defect; a tooling fix would be Lane A work.
- **Known v1 limits:** fine striping shows in the gold ribbon where the path turns edge-on (the painting's own strands;
  invisible at 50 px); no battle recording yet, so the preview uses a stand-in token.

## v2 (2026-10-24)

- **Art:** five separate transparent layers from the art director (`raws/anim_er_v2_{R1_ribbon_gold,R2_ribbon_blue,
  C1_core,F1_flecks,K1_peak}.png`; ribbons 1254 × 260, the rest 1254 px square), crisper pixel art with less baked glow.
  No cut-out needed.
- **Built:** `build_strip.py --set v2` (same motion, timing and wrap rule as v1) → `exports/anim_ethereal_rebirth_v2.webp`:
  40 frames of 128 px at 60 ms (2.4 s), 263,544 bytes. Preview `v2_preview.gif`; v1 against v2 at 384 px over dark and snow:
  `v1_vs_v2_frames.png`.
- **Difference:** harder edges, a cleaner star-shaped core, diamond flecks; ribbons slightly thinner and less luminous on
  screen. Not shipped yet: the live asset `HwkXTjErL_Laxs8WtqBiI` still carries v1. Shipping v2 is an edit of that asset
  with a new image filename (law 32), with `hidden: false` kept.
