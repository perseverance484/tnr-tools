# Art request (optional): Subaku Palace domain floor, painted finish

- **Context:** the domain floor ships as a programmatic tile (`art/subaku_palace/floor.py`, 'bold flow'):
  - exact edge-midpoint joins (RUL-2026-11-05-125);
  - dark basalt flagstones with ember joints;
  - one bold bevelled demon-gold current per hex, with one spiral curl.
- **Why optional:** the game delivers static art at a 50 px rendition (engine doc 3.4), so painted detail finer than
  1/50 of the tile is lost. Run this only if the director wants richer stone and gold texture at that scale.
- **Why components, not a finished tile:** the joins depend on exact geometry, which a generator cannot hit.
  `floor.py` will map S3 onto the hex lattice (an affine map of a seamless square texture is lattice-periodic) and
  warp B3 along the exact current and curl paths.
- **Live-game requests/writes:** 0.

~~~text
2 separate images for The Ninja RPG's Subaku Palace jutsu (the demon palace's floor). One asset per image, never a
sheet. Attach the current Subaku domain tile (ref_domain_tile_a_256) as STYLE ONLY.

SHARED STYLE
High-quality pixel-art game asset. Crisp hard-edged pixels at about 4 screen pixels per art pixel, clean dark 1-pixel
outlines, flat cel shading in 3-4 steps per colour, limited palette, deliberate highlight pixels, dithering only at soft
edges. Premium, readable at small size. No text, letters, runes, symbols, logos, faces, UI, borders or characters.
Palette: basalt #1f1111 #2c2624 #342d2a #3a322e, mortar #0e0908, ember #6e0c08 #b81c10 #ff4a1c,
demon gold #54320c #7c5014 #9c6c22 #ba8c3a #d8b266, outline #281506.

1. S3_DEMON_BASALT — 1024 x 1024, FULL BLEED (no transparency, fills the canvas to every edge), seamless when tiled in
   both directions. Seen from directly above: irregular dark basalt flagstones with a faint warm red-sandstone cast,
   bevelled edges catching one highlight pixel line from the upper left, narrow mortar joints, about one joint in
   three glowing ember red deep inside, a few hairline cracks. Dark and quiet overall. No objects.

2. B3_DEMON_GOLD_CURRENT — 2048 x 256, transparent background. ONE inlaid band of burnished demon gold running
   perfectly straight and horizontal, edge to edge, centred vertically, seamless left-to-right, and symmetric top to
   bottom (the top half mirrors the bottom half). Dark outline, a bevelled rim one step darker, a burnished face with
   slow lengthwise streaks, and a single engraved channel line along its exact centre. Seen from directly above.
   Nothing touches the top or bottom edge.

Return each image as soon as it is made, labelled S3_DEMON_BASALT and B3_DEMON_GOLD_CURRENT. Do not process or upload.
~~~

## Intake (Claude Code)

1. Raw QC: S3 is full bleed and seamless; B3 has real alpha, is symmetric top to bottom, and is seamless left to right.
2. `floor.py`:
   - samples S3 through the lattice map in place of the Voronoi stone, keeping the ember-joint mask;
   - warps B3 along the current (with its width swell) and the curl, with the profile centred so the
     joins stay exact;
   - re-exports the 150 px tile and rebuilds the strips from the same field.
3. Rebuild the true-scale composites and get director acceptance before upload.
