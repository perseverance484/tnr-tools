# Batch art prompt: Headless Rider animation layers (10)

- **Director, 2026-10-26:** "Analyze everything created and submit a batch art prompt for the 10 assets. Just
  prioritize high quality pixel art effects." Batching is the director's explicit call, replacing the one-layer-per-
  session rhythm for this set (`ISOLATED_ART_GENERATION.md` allows it on approval).
- **Built from:** the approved T1 scorch raw (`hellfire_harvest/raws/T1_scorch_raw.png`), the Rider avatar, the
  Hellfire Harvest request and the director-locked Aura of Despair request (PR #115, RUL-2026-10-26-009).
- **Measured palettes:** T1 base `#080000` `#130604` `#1e0b08` `#2a1611` `#492219` `#603325` `#965e2f`, cracks
  `#640705` to hot red, orange and yellow cores; Rider `#010101` `#160201` `#500203` `#a50c0b` `#f60e10` `#c13217`
  `#bf6538` `#f0c377`.
- Generate each asset as its **own separate image**. Attach the Rider avatar (and T1 for Hellfire assets) as style
  references. Return every image unprocessed, named by its code.

~~~text
BATCH: 10 separate images, one asset per image, for The Ninja RPG. Generate them one after another in this
conversation. Never put two assets on one canvas, never a sheet or grid.

SHARED STYLE (applies to all 10)
High-quality pixel-art VFX sprite, game-ready. Crisp hard-edged pixels at roughly 4 screen pixels per art pixel,
clean dark 1-pixel outlines on solid shapes, flat cel shading in 3-4 value steps per colour, limited palette,
deliberate hand-placed highlight pixels, subtle dithering only at soft edges. Bold readable silhouette that still
reads when shrunk to 50 px. Light is shown with bright core pixels and rim-lit edges, never a smooth airbrushed glow,
lens bloom, painted disc or halo. Square 1254 x 1254 canvas, fully transparent background (real alpha, no backing
colour, no checkerboard, no dark fringe), the element centred with a clear transparent margin, nothing touching the
edges. No text, letters, runes, symbols, logos, UI, frames, characters, hands or weapons other than those named.
References attached: the Headless Rider avatar = STYLE ONLY (rendering, outline weight, colour); for assets 1-5 also
the scorched-ground tile = STYLE/PALETTE ONLY. Do not copy either image's subject or composition.

SET A — HELLFIRE HARVEST (fast, violent, bright hellfire; the Rider's scythe)
Palette: char black #080000, ember brown #2a1611 and #603325, hellfire red #a50c0b and #f60e10, flame orange #ff6a1a,
hot gold #ffd23a, near-white hot core #fff3d0 used sparingly.

1. B1_SCYTHE_BLADE — The Headless Rider's scythe blade alone, side view, the long curved blade pointing right, a short
   stub of dark iron haft at the left. Pitted blackened iron, a bright honed edge, tongues of hellfire licking off the
   curved edge in stepped pixel flames. Menacing, sharp silhouette.
2. C1_SLASH_ARC — A single blazing crescent slash trail left by a scythe swing, sweeping left to right, thick and hot
   in the middle and tapering to two sharp points. Yellow-white core, orange body, red outer edge, a few sparks
   peeling off the trailing side. Motion-smear feel built from stepped pixel bands, not blur.
3. F1_FLAME_BURST — A tall burst of hellfire erupting upward from a flat ground line, front view, shaped like a
   flame column splitting into three to five licking tongues. Yellow-white base, orange body, red tips, a curl of
   black smoke above the tips. Iconic, chunky pixel-art flame shapes.
4. G1_GRIN — A floating carved jack-o-lantern face made only of fire light: two triangle eyes and a wide jagged grin,
   glowing orange-yellow with red edges, flickering pixel flames along the cut edges. No pumpkin body, no head, just
   the glowing cut-out shapes in empty space. Evil, gleeful.
5. E1_EMBERS — A scatter of 14 separate glowing embers and ash flecks of mixed sizes (small 3-6 art-pixel sparks up to
   larger 12-20 art-pixel tumbling coals), each with a hot core and a darker rim, a few grey ash flakes, all spaced
   well apart on the canvas so each can be cut out individually.

SET B — AURA OF DESPAIR (slow, low, cold, heavy; the Rider's dead lantern light; quiet, not fiery)
Palette: night ink #08080d, grave grey #2e2d3a and #4a4656, mist bone #cfc6b8 (sparse, low contrast), one restrained
accent: dull lantern red #7a1a1f, with #c3141b only for tiny accents in asset 7. ABSOLUTELY NO orange, gold, yellow,
flames, embers, cracks, scythes or pumpkins in set B.

6. M1_MIST_POOL — Seen from directly above: a flat, mottled pool of dark ground mist, round-ish with an irregular
   feathered rim, translucent toward the edges so it fades to clear. Inside, slow swirls of night ink and grave grey,
   a very faint dull-red underlight showing through in a few patches, three or four thin wisp tendrils curling at the
   rim. Calm and sparse in the centre so a character standing on it stays readable. No cracks, no bright centre.
7. L1_LANTERN_FLARE — A brief pulse of dead lantern light: a ring of broken crimson edge-light pixels and 8-12 thin
   sparse rays radiating from an empty centre, with lots of negative space between rays. Dull red #7a1a1f with a few
   #c3141b highlight pixels. No lantern object, no filled circle, no solid glow disc.
8. R1_MIST_RING — A ragged, uneven ring of black-red ground mist rolling outward, seen from slightly above, the centre
   completely open and empty. Billowing pixel-art fog lumps around the ring, dark grave-grey tops, faint dull-red
   underlight on the inner side. Must read as fog spreading along the ground, not a slash, magic circle or fire.
9. W1_WISPS — Eight separate pale bone-grey smoke wisps, each a tall thin rising curl of translucent mist, spaced well
   apart. Exactly two of them show a faint hollow mournful face in the smoke (two dark eye hollows and an open wailing
   mouth, soft and ghostly, sad not scary-funny). The other six are plain wisps.
10. D1_GUTTER — A low patch of subdued dull-red underlight as if a dying lantern glows beneath mist: broken,
   translucent red light catching the undersides of a few thin dark mist strands, uneven and patchy, fading to clear at
   the edges. Not a flat red spot, not a disc.

RETURN each image as soon as it is made, labelled with its code (B1_SCYTHE_BLADE ... D1_GUTTER). Do not process,
crop, resize or upload anything.
~~~

## Intake (Claude Code)

Per image: raw QC (transparency, edges, wrong-subject check against this prompt and the Hellfire/Aura distinction),
then the strips by script at 112 px square frames, the T1/M1 static tiles at 256 px, the hex-board previews over the
River background for director acceptance, then the manifests (assets hidden; Rider unequip, jutsu edits with the slot
fixes and the approved Aura text, re-equip).
