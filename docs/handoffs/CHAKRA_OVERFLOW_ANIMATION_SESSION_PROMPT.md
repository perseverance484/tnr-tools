# Chakra Overflow animation: art session prompt (route A, keyframes plus layers)

- **Basis:** `docs/handoffs/CHAKRA_OVERFLOW_ANIMATION_ART_REQUEST.md` (how animations work, the brief, routes). Director chose
  route A, 2026-10-23.
- **Zip:** `chakra_overflow_animation.zip`. **Intake:** deliveries to `art/jutsu_icons/chakra_overflow/animation/raws/`;
  Claude Code keys, registers, tweens, stacks the strip, runs `artpreflight.py --type ANIMATION` and previews it at 50 px.

## Paste into a new art-director session

~~~text
You are the art director for The Ninja RPG. This session makes the CAST ANIMATION for Chakra Overflow, the most-used
jutsu in the game, to go with its new icon "the rising star". Treat it with the same care as the icon: it plays every
time almost any player casts their most common buff.

Attached (chakra_overflow_animation.zip):
- CHAKRA_OVERFLOW_ANIMATION_ART_REQUEST.md: how animations work in the game, the storyboard (section 4) and the rules.
  Read it first.
- raw_chakra_overflow_v1.png: the APPROVED icon. It is the target final pose of the animation and the reference for
  palette, shapes and placement. You may attach it to generations.
- anim_chakra_overflow_proto_preview.gif and anim_chakra_overflow_proto_frames.png: a script-made feasibility prototype
  (the icon zooming in, holding, fading). It shows timing and size only; it is NOT the look. Beat it.
- current_spellcast_violet_frames.png: the stock violet animation this replaces (off-palette, shared by seven jutsu).

How it plays in the game: a vertical strip of square frames, played ONCE over the caster's tile when the jutsu is cast,
at about 50 ms per frame, drawn at only 50 px in battle (112 px in content lists). Normal alpha blending over every
battle biome (dark, grassy, snowy), so every frame needs real transparency and no dark halo.

THE ANIMATION: "the rising star comes to life" (about 1.3 s)
1. Ignition: a white-hot point flashes at the center.
2. The star flares: the four-point star snaps open, its upper ray shooting up longest.
3. The wings rise: deep blue chakra sweeps up and out from beneath the star into the two wings, burning gold toward the
   heart, until the icon's silhouette is complete.
4. Overflow: the emblem glows at full strength while gold and blue sparks stream upward past it.
5. Release: the emblem lifts slightly and dissolves upward into rising sparks (a dissolve, never a gray fade).

ROUTE A: you deliver KEY POSES and LAYERS; Claude Code tweens the in-between frames and composites them by script. So
registration matters more than anything: every image must use the SAME square canvas, the SAME scale and the SAME
center as the approved icon, so the pieces line up frame to frame.

Deliver these, each a square 512 x 512 image, emblem centered exactly as in the approved icon, on a flat pure lime
#00FF00 background (or true transparency if your tool supports it), no lime inside the art, no shadows or vignette:

Key poses (full composed frames):
- K1 IGNITION: only the white-hot point and a small burst of light at the center.
- K2 STAR FLARE: the four-point star fully open, long upper ray, no wings yet; a few sparks.
- K3 WINGS RISING: the star plus the wings about halfway up, mid-sweep, motion streaks trailing below them.
- K4 OVERFLOW (peak): the complete emblem matching the approved icon, at its brightest, with gold and blue sparks
  streaming upward around it.
- K5 RELEASE: the emblem breaking apart upward into streams of sparks, about half dissolved.

Layers (each alone on lime, same canvas and center):
- L1 STAR: the four-point star only, at full size.
- L2 WINGS: the two blue-to-gold wings only, at full size, no star.
- L3 FLASH: a soft round core flash of white-gold light (for ignition and peak).
- L4 SPARKS: a scatter of 15-25 sparks, mixed gold and deep blue, each a clear separate dot or short streak, spread
  over the upper two-thirds of the canvas.

Rules for every image:
- Palette and shapes from the approved icon: deep chakra blue (never cyan), gold, white-hot core; the four-point star
  with the long upper ray; two upswept wings.
- Bold enough to read at 50 px: big shapes, strong value contrast, a few large sparks rather than many tiny ones.
- Nothing touches the canvas edges; keep the whole emblem inside the central 80%.
- No fire or flame tongues, no figure or hands, no text or runes, no spiral or ring, no franchise looks (Eight Gates,
  Rasengan, Super Saiyan aura).
- Lime only as flat background: no lime-tinted glow or edges in the art (Claude Code keys it out).

Fail-fast before returning: check each image against the approved icon for registration (same center and scale) and
palette, and view it at 64 px. Regenerate anything that is off-center, off-palette, or reads as fire.

Return all nine files unprocessed, named anim_co_K1.png ... anim_co_K5.png and anim_co_L1_star.png, anim_co_L2_wings.png,
anim_co_L3_flash.png, anim_co_L4_sparks.png, with one line each on anything notable. Do not assemble the strip.

Live-game requests/writes: 0. No credentials. Do not upload anything.
~~~
