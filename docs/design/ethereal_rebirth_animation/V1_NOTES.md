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

## v3 (2026-10-24)

Director: the gold ribbon jumped when it came round to the right, and "do the original starburst core on the newer
ribbons, with the full polish". Cause of the jump: the v1/v2 lash was a second gold ribbon that appeared at the upper
right while the spinning one faded behind. `build_strip.py --set v3`: v2 ribbons and flecks, the v1 starburst core; the
spin runs the other way and the gold ribbon's head peels off the spin at t = 0.55 and flies out along the departure
tangent, curling upward, its body following the same path (one drawing throughout); the opening stays behind the token
(per-pixel mask). 40 frames of 128 px at 60 ms, 253,444 bytes. Preview over the director's avatar:
`v3_over_avatar.gif`. Shipped by push/233.

### v3 portrait mask (2026-10-24)

Director: the ribbons still touched the portrait in places (the opening gold ribbon animated in front). Every layer is
now cut by one portrait mask (the token plus its white rim, radius 0.254 of the frame) on the finished frame, so nothing
(ribbons, core, flecks, glow) ever draws on the portrait. Check over all 40 frames of the 128 px export: maximum alpha
inside the portrait 4 of 255 (a resampling edge). The starburst core now shows only where it reaches past the portrait's
lower edge. 200,870 bytes.

### v3 burst on top, mask extended (2026-10-24)

Director: the burst goes above the mask, unaffected; the gold ribbon still showed in front of the bottom of the avatar.
The burst (and its glow) now draws on a top layer composited after the portrait mask. The mask is extended over the
rank star and its mount hanging below the portrait (measured from the recording: star x 0.47-0.54, y 0.57-0.63 of the
frame): a rounded block x 0.5 +/- 0.07 from y 0.43 to 0.67. 220,904 bytes.

### v3 opening fixed, all-layer mask reverted (2026-10-24)

Director: the all-layer mask cut the ribbons where they should pass in front; revert it and fix the opening, where the
gold ribbon's lower edge still showed over the bottom of the avatar. Now: the front layer (the near side of the wrap) is
unmasked again; the behind layer, its glow and the flecks are hidden by the whole portrait (rim and rank star); the burst
stays on top. Until the spin has risen (t < 0.45) every ribbon is on the behind layer. Check, burst excluded: inside the
portrait the opening frames hold nothing above the mask's 1 px soft edge (max 37 of 255); ribbons appear in front only
from frame 20, as designed. 245,764 bytes.

### v3 portrait edge re-measured (2026-10-24)

The gold ribbon still showed at the bottom of the portrait in the opening. Root cause: the mask followed the portrait's
white ring (radius 26 px in the recording) when the real edge is the dark outline outside it (centre (206, 181.6),
radius 28.6 px, measured by hand from brightness profiles: 0.296 / 0.272 of the frame). The mask stopped about 2.5 px
short at the bottom, and the numeric checks passed because they tested against the same wrong circle. Mask now: centre
0.296, radius 0.287 (real edge + about 1.5 px), plus the rank-star block. Verified by eye on 6x zooms of frames 4-15 and
20-32 over the real portrait (`v3_opening_zoom.png`). 238,636 bytes.

## v4 (2026-10-24)

Director: "The ribbon doesnt even open up rotating the avatar entirely as it should. It needs to wrap from behind then
come in front. Just create the animation centered on where the portrait will be first, the entire thing. Then do the
mask and have it only apply to ribbons who are passing behind the avatar." `build_strip.py --set v4` (v3 layers):
the orbit's axis runs through the portrait centre (0.296); it is wider than the portrait (horizontal radius 0.36-0.40),
crosses the portrait's middle and rises from chest to brow; both ribbons start on the far side, behind the avatar, and
come round in front; front passes draw over the portrait, back passes (and their glow and the flecks) are hidden by the
portrait mask; no special opening rule is needed. The gold ribbon leaves the orbit on the front right at t = 0.58 and
lashes out. Burst on top at the portrait centre. 40 frames of 128 px at 60 ms, 213,904 bytes. Checked by eye over the
real portrait (`v4_zoom.png`, frames 8-30); GIF `v4_over_avatar.gif`.

## v5 (2026-10-24)

Director: "Draw the ribbons as they appear in the icon. Exactly." Art director's v5 layers in `raws/`:
`anim_er_v5_R1_band_gold_{a,b}.png`, `anim_er_v5_R2_band_blue_{a,b}.png` (2172 x 724, real alpha; `a` flatter, `b` wavier;
v5 uses `a`, straightened as before) and `anim_er_v5_S1_sparkles.png` (1254 x 1254, ten four-point stars).
`build_strip.py --set v5`: the v4 orbit, now tilted more steeply (vertical radius 0.17) so the front pass stays on the
lower half of the portrait and the back pass shows above the head, as the icon's loops do; blue sits higher, gold lower,
and the gold whips out to the upper right. Each band rolls along its length (scripted twist): it narrows to a bright
near-white line where it turns edge-on and its back face is a shade darker. Bands 1.6x the v4 thickness. Sparkles twinkle
once each in a ring round the user. The v1 burst stays on top. Everything fades over the outer 7% of the frame, so the
whip leaves without a hard cut at the sprite edge. 40 frames of 128 px at 60 ms, 242,800 bytes. Checked by eye at 5x over
the real portrait (`v5_zoom.png`, frames 4-18): nothing behind the avatar shows over it. GIF `v5_over_avatar.gif`.
Preflight `--type ANIMATION`: 1 error, `soft_edges` 79.3% (the known gap for glow effects, as on every earlier version).
