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

### v5 six bands (2026-10-24)

Director: "I feel like there are more ribbons in the icon, there's only 2 in this one." The icon has about six bands:
three gold (the crescent over the head, the whip to the upper right, the long low sweep) and three blue (the loop behind
the shoulders, the loop behind the right arm, the band across the legs). `V5_BANDS` in `build_strip.py` now lays six:
the original pair plus four from the director's wavier `b` layers, on orbits tilted and set at different heights, each
pouring out a moment after the last. Front passes never cross the face (upper half of the portrait): there a band goes
behind and the portrait mask hides it, so the high bands show as arcs above and beside the head, as in the icon. Each band
is drawn on its own layers and laid over the others normally (a per-channel max turned gold-over-blue pink). The added
bands fade in from a minimum length (no loose scraps). 348,568 bytes. Checked at 4x over the real portrait
(`v5_zoom.png`, frames 4-36).

### v5 ending trimmed (2026-10-24)

Director: a new gold ribbon started forming as the animation ended, briefly flaring at the top right over the portrait;
"lets cut that out". It was the gold crescent band (V5_BANDS[2]) coming round to a front pass in frames 35-38. The four
added bands now fade out over t 0.74-0.86, before that pass; the ending is only the gold whip leaving to the upper right.
Measured: no alpha inside the portrait from frame 35 on. 305,488 bytes.

## loop1: the passive loop while the absorb is active (2026-10-24)

Director: "We need a static animation for it too that is a subtler effect of the same ribbons. We want to show them
passively orbiting and protecting the player so long as the absorb is active." Game source (a744c04,
`libs/threejs/combat.ts:667`): an effect's `staticAnimation` is drawn like the cast animation (50 px over the avatar,
layer 5) with `showAnimation(playInfinite)`, so it loops while the effect stands. It is added in the same pass as the
`appearAnimation`, so the loop and the cast start together and overlap for the cast's 2.4 s.

`build_strip.py --set loop1 --frames 48 --ms 80`: one gold and one blue v5 band (the flatter `a` layers), 0.85x thickness,
alpha 0.55-0.60, on a steady tilted orbit round the portrait, half an orbit apart; one full orbit per loop (3.84 s); the
twist travels along each band once per loop; six sparkles twinkle in turn; front passes stay off the face; back passes
under the portrait mask; edge fade. No burst. Seamless: the frame 48 -> frame 1 change (34) is below the mean step (67).
179,956 bytes. Preview with the cast on top, as the battle plays them: `loop1_in_battle.gif`
(`battle_preview.py`); stills `loop1_zoom.png`.

### v5 starburst from the icon (2026-10-24)

Director: "I want the animation's starburst to more closely resemble the icons." Art director's layers (brief
`docs/handoffs/ETHEREAL_REBIRTH_ANIMATION_STARBURST_ART_REQUEST.md`): `raws/anim_er_v6_C2_glow_rays.png` (white-hot
glow with fine rays) and `raws/anim_er_v6_C3_cracks.png` (branching cracks of light), both 1254 x 1254, real alpha.
`burst_v6()` replaces the v1 core in v5: the cracks spread out from the portrait's centre by a soft radial wipe (canvas
radius 0.30 of the frame, so the tips stay inside the portrait) and fade over the burst's 0.60-0.85; the glow and rays
flare from half size (canvas radius 0.24, alpha lifted 1.6x so the hair-thin rays read at 50 px) and fade over 0.45-0.75.
Unmasked top layer at the portrait centre, first 0.45 of the cast. 333,928 bytes. Zoom: `v5_burst_zoom.png`.

## v6 + loop2: fluidity pass (2026-10-24)

Director: "polish the animations for appear and static so they are very smooth, seamlessly flow behind and in front of
the avatar and transition from one to the next smoothly." Same art and design as v5 / loop1; motion only.
- **Frame rate:** both strips now 36 ms per frame (about 28 fps; were 60 and 80 ms): the cast 66 frames (2.4 s), the loop
  100 frames (3.6 s, the game's maximum frame count), at 112 px (the art spec's minimum, ContentImage's canvas).
- **Front and behind:** the face rule was a hard switch (a band's front pass cut off where it met the upper portrait);
  it is now a soft change-over in height and at the rim, so the band fades round behind the face.
- **Cast into loop:** the game starts both strips on the same tick (combat.ts adds the appear and static animations in
  one pass), so cast frame f lines up with loop frame f. Over the cast's t 0.60-0.90 its blue band eases its spin down to
  the loop's rate (integrated, no jolt) and its orbit, tilt, height, length, thickness, twist and alpha onto the loop's
  blue band; its phase is chosen so it lands exactly on it; then it fades over the loop's copy (`v6_handoff_zoom.png`,
  cast + loop composited, frames 40-70). Shared constants: `MS`, `CAST_N`, `LOOP_N`, `LOOP_BANDS` in `build_strip.py`.
- **Bytes:** alpha under 4/255 cleared before saving (invisible glow tails): cast 422,488, loop 257,236.
- **Measured** (frames composited over a flat background, mean absolute change per frame): cast mean step 10.1, max 25.7
  (v5: 15.5, 34.3); loop mean 2.5, max 3.3, seam (last frame to first) 2.6. Exported as `anim_ethereal_rebirth_v6.webp`
  and `anim_ethereal_rebirth_loop2.webp` (new filenames, law 32). Preview: `v6_in_battle.gif`.

## hit1: the attack's impact on the enemy (2026-10-24)

Director: "What about an animation for the attack itself? ... Keep in mind the enemy portrait ... Maybe an impact beam of
spiraling ribbons hitting their portrait?"; then "Go, corkscrew from the top, timed to the lash". The damage effect's
`appearAnimation` plays once over the target's portrait (process.ts:1559 -> combat.ts:646); nothing can travel between
tiles. The hit and the cast are started in the same `drawCombatEffects` pass (combat.ts:482; movement queues only SFX),
so they share a clock: `build_strip.py --set hit1 --frames 66 --ms 36 --size 112`.
- 0-1.2 s: seven sparkles gather round the portrait, twinkling, closing in (the light finds them).
- 1.18-1.58 s: the gold and blue v5 bands, wound round each other (helix radius 0.075, 2.5 turns, the whole band along
  the braid, whip tips leading), drill down from the top edge (a touch right of centre), accelerating; the braid narrows
  to the impact point at the portrait's centre. The cast's gold lash leaves the caster's frame at about 1.5 s.
- 1.58 s (frame 44): a flash (the starburst C2 layer, radius 0.27), two rings of ribbon light (gold, then blue) blast
  outward round the portrait (back halves under the portrait mask), and the two ribbons spring apart and curl round the
  portrait in opposite directions (one continuous route per ribbon: down the axis, then out on a spiral), the braid's tail
  still pouring in from the top; sparkles scatter.
- to 2.4 s: everything fades; the portrait is clear at the end.
132,072 bytes. Zoom `hit1_zoom.png`; both tiles on one clock: `hit1_duel.gif` (`duel_preview.py`; the director's
portrait stands in for the enemy's, same token geometry). Replaces the generic hit `iDv3rjj81rRgD10shRqSn` on approval.
