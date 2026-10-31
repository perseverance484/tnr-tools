# Session prompt: Patient Zero animation layers (Plague Bile + Infected Bite)

Paste the block below to the art director. It covers every raw layer for both animations.

~~~text
Repository: perseverance484/tnr-tools. Verify main at the latest head.
Role: Art Director, then Image Production. Live-game requests/writes: 0. Credentials: none.

READ FIRST
1. docs/handoffs/PATIENT_ZERO_ANIMATIONS_ART_REQUEST.md (sections 3 and 4 are the direction and the layer list)
2. docs/workflows/ISOLATED_ART_GENERATION.md
3. skills/producing-tnr-art/data/25x_DATA_art_spec.json, target ANIMATION

WORK ORDER (one fresh isolated session per layer, one candidate at a time, show me and wait)

Plague Bile: wet, splashing, sickly green; bile green is used ONLY in these four layers.
  1. PB1 BILE GLOB  - one wet glob of zombie bile in flight, a teardrop with a trailing tail, dark core, sickly
                      green body, crimson-tinged rim, a few glossy highlight pixels.
  2. PB2 SPLATTER   - a flat ragged bile splatter seen slightly from above, irregular arms, a few detached droplets.
  3. PB3 BUBBLES    - 6-8 separate bile bubbles, mixed sizes 40-160 px, two mid-pop, spaced apart.
  4. PB4 FUME       - 3-4 separate thin wisps of green-grey fume curling upward.

Infected Bite: red, bone, snapping; NO green in any of these layers.
  5. IB1 UPPER JAW  - a spectral zombie upper jaw alone, front view, rotten uneven bone teeth, grey-green gum, ragged
                      lip edge, open.
  6. IB2 LOWER JAW  - the matching lower jaw alone, same style and scale as IB1 (attach IB1 as STYLE/SCALE reference).
  7. IB3 BLOOD SPRAY - a burst of crimson blood spray radiating from one point, a few heavier drops.
  8. IB4 EYE GLINTS - two small glowing red eye-glints with a short hard flare, light only, no face or skull.

References per session: art/halloween_zombie_outbreak/patient_zero_avatar.webp, STYLE ONLY, never as composition.

PALETTE
rot black #120c10, plum shadow #3a1f33, crimson #c3141b, blood dark #6e0d12, skin grey-green #8a9a7a,
bone #d9cfb4, eye glow #ff3b2f; bile (PB layers only) #3d4a12 #6b8f1e #a8c23a, highlight #d8e86a.

RULES FOR EVERY LAYER
- 1254 x 1254, one element per canvas, nothing else on it.
- Native transparency: real alpha, no grey or tinted backing, no dark fringe, no checkerboard. If transparency is
  unavailable, use a MAGENTA key only. Never lime: bile is green.
- Crisp pixel rendering matching the Patient Zero avatar; dark one-pixel outlines; flat cel steps; no airbrush, no bloom.
- Glow is edge light only, never a painted disc, panel or halo.
- No text, runes, symbols or franchise insignia. No full faces or skulls; the jaws and eye-glints are the only
  anatomy.
- Two wrong-subject results in one session: close it and start clean; do not lengthen the prompt.

RETURN
- Each director-approved original, unprocessed, named by layer (PB1_..., IB1_..., etc.), with its approval note.
- I (Fable) do raw QC, build the strips by script (50 px frames), preview them on a hex board over the pyramid
  background, and build the manifest. Do not process or upload anything.
~~~
