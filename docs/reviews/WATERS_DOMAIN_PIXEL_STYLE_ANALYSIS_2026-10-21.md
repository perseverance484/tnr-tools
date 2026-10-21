# Water's Domain icon: why the first generation missed TNR's pixel-art look

- **For:** the art director and dauntless
- **Asked by:** Art Director handoff "TNR JUTSU ICON ART — PIXEL-ART STYLE CORRECTION", 2026-10-21, at main `48ff947`
- **Status:** analysis and proposals. The durable changes in section 6 wait for the director; nothing in the
  spec, registers or skills was changed.
- **Live-game requests/writes:** 0. No image generated, processed or uploaded.

## 1. Inputs (verified)

| Item | Evidence |
|---|---|
| Image A, first generation (director: "Good start but it does not match TNR's pixel art design.") | 1254x1254 PNG, sha256 `dd4e3a948d52fa51df9eebe6b2c357a030a04125b6450796bb81201159a7a9f9` (matches the handoff) |
| Image B, revision (director: "Wow, much better.", preferred, not production-approved) | 1254x1254 PNG, sha256 `0067166e5540c2f1d9f24d4b53a2bdb0f27b46e51526fcf9f000dfb3239a9a4d` (matches) |
| Approved comparison set | all 32 files read as pixels, 256x256 RGB: `art/jutsu_icons/vaporia/` (5), `art/jutsu_icons/aerathiel/` (5), `art/jutsu_icons/starter/exports/` (6), `art/style_refs/jutsu_icons/bbe/` (8), `art/style_refs/jutsu_icons/bee/` (8) |
| Brief that produced A | `docs/handoffs/WATERS_DOMAIN_ICON_DIRECTOR_PROMPT.md` at `d24ba83` (written by Fable) |

Both diagnostic images are kept out of the repository; their hashes above identify them. Neither may be
passed as a generation reference (A is rejected; B is preferred but not approved).

## 2. What the approved icons actually look like

Looked at side by side at 256 px, as 4x zooms of a 64 px crop, and at 64 and 32 px:

- **Vaporia, Aerathiel and the six starter icons** (the most recent director approvals) share one register:
  **high-resolution pixel art**. Fine clusters of one or two pixels at 256, crisp stepped contours,
  hand-placed highlights, several flat value bands per colour, and dark gaps or outlines separating
  masses (Surfing Strike's water strands are split by near-black navy). Light is a bright core plus lit
  edges, not haze. Negative space falls to near-black at the corners. Replacement Technique, the
  most literal pixel-art icon, is still fine-grained, not chunky.
- **BBE and BEE** (the 16 pinned `style_refs`, RUL-2026-10-17-021) are a **different register**: smooth
  painted glow art. BEE in particular is airbrushed red bloom on black. These are approved icons, but
  for the pixel look the director now asks for, they pull the wrong way.

Simple measurements over the 256 px versions agree (`flat` = share of horizontal neighbours within 4
luminance levels; `hard` = share differing by 24 or more; `runs` = share of exactly equal neighbours at
native size, a sign of large flat pixel blocks):

| Group | flat | hard | runs |
|---|---|---|---|
| Vaporia (5) | 0.18–0.34 | 0.29–0.41 | 0.04–0.15 |
| Aerathiel (5) | 0.23–0.36 | 0.27–0.37 | 0.06–0.13 |
| BBE (8) | 0.13–0.29 | 0.23–0.39 | 0.05–0.11 |
| BEE (8) | 0.38–0.66 | 0.06–0.22 | 0.10–0.30 |
| **Image A** | 0.28 | **0.24** | 0.14 |
| **Image B** | 0.39 | **0.23** | **0.40** |

Read with care: these are rough signals over lossy, AI-made images, not a style test. They do not
separate BBE from Vaporia (BBE's crystal edges are hard too); the 4x zoom does, where BBE shows smooth
painted shading rather than pixel clusters. What they do show: Vaporia and Aerathiel are dense with hard edges and have almost no flat pixel blocks. Image A
has fewer hard edges and more soft gradient. Image B's hard-edge share is no higher than A's, but it is
built from large flat blocks (runs of 7–8 equal pixels at 1254 px, so about 160 pixel cells across),
which the approved icons are not.

## 3. Why Image A failed

1. **The brief never said "pixel art".** The Water's Domain director prompt asked for "the approved
   jutsu-icon standard", "one bold luminous silhouette", a centre that "glows" and a glow that "rises".
   No rendering words at all. The generator filled the gap with its default: smooth fantasy concept art.
2. **The words it did use pull toward painting.** "Luminous", "glow" and "rim light" are the words the
   art spec already struck from the character house style because they "produced the soft AI-painterly
   register" (`25x_DATA_art_spec.json`, `house_style.struck_clauses`). The jutsu-icon registers still use
   them ("luminous technique-specific silhouette", "strong rim light").
3. **The written standard has no rendering clause.** `targets.JUTSU_ICON.art_direction` defers to the
   registers; the starter register's "Collection-wide visual lock" describes silhouette, colour and
   background but not rendering. The only place that says "pixel art" for icons is the generic ICON
   scaffold and the skill's one-line description. The same failure has happened before: the village
   scroll set's painted Shinseina Ki v1 was rejected because "Icon 1 locks pixel-art rendering"
   (`docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md`), and that lesson stayed in one
   collection's notes.
4. **Half the approved references are painted.** BBE and BEE are the pinned jutsu-icon `style_refs`.
   A session that reads "approved standard" and samples the pinned library gets painted glow art as
   its model of what is approved.
5. **No proof the reference pixels reached the generator.** The prompt named a path for Surfing Strike.
   The protocol is explicit that a path or filename does not prove the generator saw the pixels
   (`ISOLATED_ART_GENERATION.md`). Image A shows none of Surfing Strike's stepped pixel structure, so
   either the bytes were not attached or the prose overrode them.
6. **No visual check before generating.** Nobody compared the brief's words with the reference
   image's actual rendering, so the mismatch between "luminous glow" and a crisp pixel reference went
   unnoticed.

## 4. Why Image B is better, and what it still lacks

**What B got right, consistent with the approved pixel icons:** visible pixel clusters, stepped hard
contours, foam as distinct hard white shapes, clearer separation between blue bands, stronger
blue/white contrast, a distinct aqua centre, no mist or bloom, and the I1 composition kept.

**Where B still differs from the approved icons:**

1. **Pixels a little too coarse.** About 160 cells across, against Surfing Strike's near-native one-to-two
   pixel clusters at 256. At 256 the cells are about 1.6 px, a non-integer step that will soften when
   exported. The target is finer: "high-resolution pixel art", not chunky retro pixels. The art spec
   already lists `chunky_low_res_pixel` as a rejected register for characters.
2. **No dark negative space.** Foam reaches all four edges; the approved icons let corners fall to
   near-black. The brief's "nothing touching the edges" was ignored.
3. **No dark separation lines.** Approved water is split by near-black navy gaps between strands; B's
   bands meet as mid-blue on mid-blue, so the mass flattens at 32 px.
4. **Weak focal point.** The aqua eye is small and no brighter than the foam. At 32 px B reads as "blue
   swirl", not "whirlpool with a glowing heart".
5. **Noise.** Evenly scattered square specks and droplets add texture that vanishes at icon size.
6. **Nearly flat-on.** It reads closer to a front-facing spiral than a low 3/4 basin. See the silhouette
   note below.

**Silhouette note for the director (missed when I1 was proposed):** BEE's Ring of Spilled Blood
(`icon_bee_ring_of_spilled_blood_v2.webp`) is already a flat spiral vortex. The registers treat each
approved silhouette as reserved by its family. Water's Domain stays distinct if it is clearly a **3/4
basin with a raised foam rim and a glowing eye**, not a flat-on spiral. The prompt below makes that
explicit. If you consider the two too close anyway, I2 (ring of water walls around a glowing pool) is
the fallback.

## 5. Improved prompts

**Reference to attach (actual bytes, one file):** `art/jutsu_icons/vaporia/vaporia_surfing_strike_jutsu_icon_v1.webp`,
style/material only. Do not attach Image A, Image B, the current live icon, or any BBE/BEE file.

### 5a. Fresh isolated session (recommended)

~~~text
Target: Water's Domain (jutsu ID -8W4JOqG3Cb-oPQtF9rMs). One square 1:1 game icon.

Reference image attached: copy its RENDERING only. Fine pixel clusters, crisp stepped edges,
near-black navy gaps between water strands, near-black corners. Do not copy its breaking-wave shape
or its ember streak.

Subject: a whirlpool basin seen from a low three-quarter angle, so it reads as an oval bowl, turning
clockwise. A raised rim of white foam crests around the outer edge. Bands of deep and mid blue spiral
down into a calm centre that glows aqua-teal. A few aqua droplets rise from the centre.

Rendering: high-resolution pixel art, about 256 pixels across. Small 1-2 pixel clusters, crisp
stepped contours, hand-placed highlights. Cel shading with 4-5 flat value bands per colour and no
gradients. Hard white foam shapes with dark navy outlines between foam and water. Light only as a
bright core and lit edges, never a haze.

Composition: the basin fills about 80% of the frame, centred slightly low. The corners and top edge
fall to near-black navy. The aqua centre is the brightest point and must still read at 32 px.

Palette: near-black navy, deep blue, mid blue, white foam, one aqua-teal accent.

Avoid: smooth digital painting, airbrushed gradients, soft blur, bloom, mist or smoke, photorealistic
water, concept-art lighting. Also avoid chunky 8-bit or retro low-resolution pixels, big square
blocks, dithering noise, scattered square specks. No characters, hands, text, symbols, runes, seals,
frames or franchise imagery. Not a dragon, a water column, a sphere, a single breaking wave, a
shield, chains, or a flat front-facing spiral.

Generate ONE image. Do not upload or process it.
~~~

### 5b. Same session, revising Image B (if the director wants to keep its composition)

~~~text
Keep this exact composition and palette. Change only the rendering:
- finer pixels: about twice as many across, 1-2 pixel clusters like the reference;
- pull the foam back from the frame edges so all four corners fall to near-black navy;
- add dark navy outlines between the foam and the water bands;
- tilt the view lower so it reads as an oval basin seen from the side, not a flat spiral;
- make the aqua centre larger and the brightest point in the image;
- remove most of the scattered square specks.
No blur, no gradients, no bloom. One image.
~~~

## 6. Proposed durable changes (for director approval; not made)

1. **Give JUTSU_ICON a rendering lock** in `skills/producing-tnr-art/data/25x_DATA_art_spec.json`
   (`targets.JUTSU_ICON`), measured from the Vaporia, Aerathiel and starter exports, with the same
   shape as `house_style`:
   - rendering: "high-resolution pixel art, 1-2 px clusters at 256, crisp stepped contours, cel
     shading with flat value bands, dark separation lines, near-black negative space";
   - accent: "light as a bright core and lit edges only, no haze or bloom";
   - rejected registers: `soft_ai_painterly` (Image A) and `chunky_low_res_pixel` (too coarse);
   - struck words: "luminous", "glow" without "core and edges", "strong rim light".
   The registers and briefs then cite it instead of restating style.
2. **Split the reference library by register.** Mark Vaporia, Aerathiel and the starter exports as the
   pixel-art style references for new jutsu icons. Keep BBE and BEE as approved icons, but tell
   sessions not to use them as style references for the pixel look. Whether BBE/BEE stay style
   references at all is your call.
3. **Fix the brief templates.** In `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md` (visual lock
   and copy-ready brief) and the overhaul register's brief: replace "luminous silhouette / strong rim
   light" with the rendering lock, and add the rendering negatives (painterly and chunky).
4. **Add a pre-generation check** to `docs/workflows/ISOLATED_ART_GENERATION.md`: before generating,
   confirm the reference bytes are attached and that the brief's rendering words describe what that
   reference actually looks like. At raw QC, zoom a crop to 4x: soft gradients or blur fail; blocks
   larger than about 2 px at 256 fail.
5. **Correct the Water's Domain director prompt** (`docs/handoffs/WATERS_DOMAIN_ICON_DIRECTOR_PROMPT.md`)
   to 5a, noting that the first version lacked the pixel-art lock.

## 7. Minimal reusable block for any jutsu icon brief (until 6.1 lands)

~~~text
Rendering: high-resolution pixel art, about 256 px across, 1-2 px clusters, crisp stepped contours,
cel shading with 4-5 flat value bands per colour, dark outlines between masses, near-black corners.
Light only as a bright core and lit edges.
Avoid: smooth painting, gradients, blur, bloom, mist, photorealism; and chunky 8-bit pixels, big
blocks, dithering noise.
Reference: attach one Vaporia, Aerathiel or starter export as real image bytes, rendering only.
~~~
