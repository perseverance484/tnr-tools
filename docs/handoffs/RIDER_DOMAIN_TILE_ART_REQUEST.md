# Art request: The Headless Rider's domain tile (pumpkin patch)

- **Director, 2026-10-26:** a "domain" tile that fills the hex, repeats across the whole battlefield with a visually
  attractive hex pattern, themed for the event ("Make it pumpkins"). Reference for finish and framing: the Subaku domain
  tile (a dark stone floor crossed by bands that join from hex to hex).
- **Replaces:** Hellfire Harvest's static tile (`staticAssetPath` on the recoil effect). Every tile of the board shows it
  for 3 rounds, under the units.
- **Prototype:** `art/halloween_headless_rider/fx/previews/pumpkin_domain_board.png` (programmatic placeholder art; the
  geometry is final, the drawing is not).
- **Why components, not one finished tile:** the pattern only joins if every vine meets the hex edge at its exact
  midpoint, square to the edge, and the hex is stretched corner to corner in the square canvas. A generator cannot hit
  those coordinates. So the art director paints three high-quality pieces; `fx/domain_tile.py` bends the vine along the
  exact curves, lays the floor, plants the pumpkin and cuts the hex, so the seams are perfect.
- **Live-game requests/writes:** 0.

~~~text
3 separate images for The Ninja RPG's Halloween event (the Headless Rider's pumpkin-patch domain). One asset per image,
never a sheet. Attach the Headless Rider avatar as STYLE ONLY.

SHARED STYLE
High-quality pixel-art game asset. Crisp hard-edged pixels at about 4 screen pixels per art pixel, clean dark 1-pixel
outlines, flat cel shading in 3-4 steps per colour, limited palette, deliberate highlight pixels, dithering only at soft
edges. Rich, readable, premium. No text, letters, symbols, logos, UI, borders, frames or characters.
Palette: soil black #0e0806 and #2a1611, ember red #a50c0b, pumpkin #b8460c #ee8020 #ffba50, candle core #ffe9a8,
vine #142a10 #26461a #42702a, leaf highlight #6a9c38.

1. S1_CURSED_SOIL — 1024 x 1024, FULL BLEED (no transparency, fills the canvas to every edge), seamless when tiled in
   both directions. Seen from directly above: dark cursed farm soil, clods and cracked earth with thin glowing
   ember-red seams in the cracks, a few scattered dead leaves and tiny pumpkin seeds. Low contrast and dark overall so
   things placed on it stand out. No objects larger than a clod, no plants, no pumpkins.

2. V1_VINE — 2048 x 384, transparent background. ONE pumpkin vine running perfectly straight and horizontal, edge to edge,
   centred vertically, seamless left-to-right (the left end continues the right end). Thick twisted dark-green stem with
   a darker outline and a lighter top highlight, small thorny bumps, broad pumpkin leaves alternating above and below the
   stem every ~400 px, and a few curling tendrils. Seen from above. Nothing touches the top or bottom edge.

3. P1_JACK_O_LANTERN — 1254 x 1254, transparent background. One carved jack-o-lantern pumpkin, seen from the front and
   slightly above, sitting upright, centred with a clear margin. Deep ribbed orange body with strong cel-shaded lobes, a
   short curled dark-green stem with one small leaf, a menacing carved face (angled triangle eyes, jagged grin) glowing
   from inside with candle-gold light, a few singed scorch marks on the skin. Glow stays inside the carved cuts and as rim
   light on the edges; no halo, no glow disc, no light on the ground, no shadow, nothing under it.

Return each image as soon as it is made, labelled S1_CURSED_SOIL, V1_VINE, P1_JACK_O_LANTERN. Do not process or upload.
~~~

## Intake (Claude Code)

1. Raw QC (S1 full bleed and seamless; V1 and P1 real alpha, nothing touching the edges).
2. `domain_tile.py` assembles the tile at 1024: S1 as the floor; V1 warped along the three Truchet curves (the small arc
   round corner 0 and the two large crossing arcs on edges 1-3 and 2-4), the over/under weave preserved; P1 planted at
   the centre and pre-stretched 2x tall against the game's 2:1 squash; the dark bevelled hex rim; cut to the hex corner
   to corner; box-reduced to 256 lossless WebP.
3. Board simulation (12 x 10, units on top, the Aura of Despair mist over it) for director acceptance before upload.
4. Upload as a hidden STATIC gameAsset in `HeadlessRiderHorror`; set as Hellfire Harvest's still in the jutsu edit that
   carries the other animation slot fixes.

---

# Variant B: "Hellfire Ironwork" (no pumpkins)

- **Director, 2026-10-26:** an alternative domain that is just an attractive design in the event's colours.
- **Look:** a floor of fire-blackened obsidian flagstones with molten seams, crossed by braided channels of wrought
  iron carrying hellfire, riveted, with a forged boss where two channels cross. The Rider's iron, chains and fire,
  no figures. Same Truchet geometry as the pumpkin variant (the braid prototype:
  `fx/previews/braid_domain_board.png`), so the channels weave into a continuous chain-link lattice across the board.
- **Components, assembled by `domain_tile.py`:** S2 floor, B2 channel (bent along the curves), K2 boss (placed on the
  crossing, pre-stretched against the 2:1 squash).

~~~text
3 separate images for The Ninja RPG's Halloween event (the Headless Rider's domain floor, ornamental version). One asset
per image, never a sheet. Attach the Headless Rider avatar as STYLE ONLY.

SHARED STYLE
High-quality pixel-art game asset. Crisp hard-edged pixels at about 4 screen pixels per art pixel, clean dark 1-pixel
outlines, flat cel shading in 3-4 steps per colour, limited palette, deliberate highlight pixels, dithering only at soft
edges. Ornate, premium, readable at small size. No text, letters, runes, symbols, logos, skulls, faces, UI, borders or
characters.
Palette: obsidian #0a0607 #1a0f0e #2e1c19, cooled iron #2b2422 #4a3c36 #6e5a4e, rivet highlight #9a8070,
hellfire #6e0806 #c3141b #f05a14 #ffb347, white-hot core #fff0c8 (sparingly).

1. S2_OBSIDIAN_FLOOR — 1024 x 1024, FULL BLEED (no transparency, fills the canvas to every edge), seamless when tiled in
   both directions. Seen from directly above: irregular fire-blackened obsidian flagstones, slightly glossy edges with a
   single highlight pixel line, narrow mortar gaps with a faint molten-red glow deep inside, a few hairline cracks and
   ash specks. Dark and quiet so the channels lead.

2. B2_HELLFIRE_CHANNEL — 2048 x 320, transparent background. ONE ornamental channel running perfectly straight and
   horizontal, edge to edge, centred vertically, seamless left-to-right. Two parallel rails of blackened wrought iron
   with a bevelled top highlight and evenly spaced square rivets, and between them a recessed groove of flowing
   hellfire: dark red at the walls, orange, then a thin white-hot core line, with small pixel flame licks and flow
   streaks. Seen from directly above. Nothing touches the top or bottom edge.

3. K2_FORGED_BOSS — 1024 x 1024, transparent background. One forged iron boss seen from directly above: a round
   riveted iron rosette with eight short petals, a bevelled rim, and a single faceted ember-red gem glowing at its centre
   (glow inside the gem and as rim light only). Centred with a clear margin. No halo, no glow disc, no shadow.

Return each image as soon as it is made, labelled S2_OBSIDIAN_FLOOR, B2_HELLFIRE_CHANNEL, K2_FORGED_BOSS. Do not process
or upload.
~~~

**Intake** as the pumpkin variant: QC, assembly at 1024 (S2 floor; B2 warped along the three curves with the weave;
K2 on the crossing of the two large arcs, pre-stretched 2x tall; hex rim; cut; 256 lossless), board simulation, then the
director picks pumpkin or ironwork.
