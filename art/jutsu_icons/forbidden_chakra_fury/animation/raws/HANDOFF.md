# Forbidden Chakra Fury — animation source-art handoff

Source brief: `perseverance484/tnr-tools/docs/handoffs/FORBIDDEN_CHAKRA_FURY_ANIMATION_ART_REQUEST.md` (read 2026-11-16).

These are **four separately painted 1254 × 1254 RGBA PNG source artworks**, not completed animated WebP strips. They are intended for the repository's script-assisted assembly workflow. The uploaded jutsu icon was used as an energy-palette and rendering reference only; no character, weapon, text or symbol was copied.

| File | Purpose | Intended final playback | Composition |
| --- | --- | --- | --- |
| `A_fury_burst_keypose.png` | Recoil appear, full detonation hero pose | About 24 frames × 42 ms; scale 1.75 | White-lilac core, jagged ring, six forked bolts, chakra lashes, one crimson streak; can drive draw-in, outward surge, crack flash and ember dissolve |
| `B_scorched_ground_tile.png` | Persistent recoil ground image | Static for both recoil rounds | Charred irregular six-sided earth, strong violet veins, soft alpha edges |
| `C_fade_overlay.png` | Recoil disappear | About 12 frames × 50 ms; shared scale 1.75 | Lower-frame split arcs, vein glints and rising sparks; animate with flicker and dissolve |
| `D_crackle_overlay.png` | Optional recoil static animation | About 12 frames × 60 ms; shared scale 1.75 | Very small lower-frame hopping micro-arcs; can be omitted if too quiet at actual rendered size |

## Art specifications

- All source dimensions are 1254 × 1254; actual alpha transparency verified with both fully transparent and nontransparent pixels. None has an opaque background.
- Raw non-elemental chakra, **not fire**. Violet `#9b4dff`–`#c58bff`, core `#f4eaff`, indigo `#24093f`; crimson `#d11f35` appears only as one minimal stroke in A.
- Deliberately crisp fantasy RPG pixel clusters, shaped lightning forks, restrained dither, no letters, figures, glyphs or border.
- C and D are transparent overlays **without any painted stone**, so they should composite over B without repeating the tile.

## Suggested animation treatment

1. For A: frames 1–3 draw motes inward; 4–7 reveal/expand the ring and bolts hard; 6–14 sweep the arc clusters; 12–18 flash ground cracks; 18–24 progressively dissolve into a few violet motes (never a grey fade).
2. Hold B as the `staticAssetPath` of recoil effect 2. Preserve its unscaled tile footprint.
3. C: give the smaller arcs 2–3 brief snaps and flicker the vein highlights while sparks move upward and disappear; keep the animation low in the frame.
4. D: move its isolated bridges between crack positions with gaps and uneven brightness, in a seamless short loop. Keep subtle over B; drop if not discernible or if it distracts.

## Game integration notes from the brief

- Target recoil effect 2's `appearAnimation`, `staticAssetPath`, `disappearAnimation`, and possibly `staticAnimation`, with `animationScale = 1.75`. No gameplay/balance changes.
- Final animation outputs (to be assembled separately) should be single-column, top-to-bottom square-frame strips in **lossless WebP**, each **under 460,800 bytes**, with each frame at least 128 px. Ground image should be a transparent WebP.
- Before any live upload, run the documented **50px rendition sharpness probe**, then inspect final animations on dark, midtone and bright maps at 1.75× scale and obtain director approval.
- The potential clearing of effect 1's overlapping stock zap is a separate art-direction approval; retain its sound. No live asset or jutsu record was changed in this handoff.

## Final art prompt set (normalized)

- **A:** High-end 32-bit pixel-art radial violet chakra detonation; white-lilac center, incomplete shockwave, six long branched lightning bolts, blade-stroke energy arcs, one hairline crimson lash, lower ground flares and embers, isolated transparent alpha.
- **B:** Slight-top-down hex-footprint charred earth decal with legible violet-energy vein cracks, faint motes, irregular feathered-alpha outer edges, no flames or rectangular backdrop.
- **C:** Small low-frame ending layer, discontinuous violet crack pulses, two or three snapping micro-arcs, a few ascending sparks, no ground plate, true transparency.
- **D:** Extremely sparse low-frame little violet electric bridges and points as an optional loop overlay over B, no land/stone, no large blast, true transparency.

Creation mode: built-in image generation; reference: supplied jutsu icon. Basic alpha, dimensions and small-scale readability were checked locally. This handoff provides **art sources only**; it does not claim that final animation strips or live integration exist.
