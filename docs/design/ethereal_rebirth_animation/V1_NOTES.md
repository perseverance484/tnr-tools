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
