# Common Hunter's Chest — upper-latch binding revision (2026-10-20)

**Status:** SAME-SUBJECT PIXEL-STYLE CORRECTION REQUIRED — first short-latch candidate fixed leather termination but drifted into smooth painterly rendering; NO FINAL APPROVAL; fresh director visual acceptance required  
**Lead:** Image Production · **Support:** Art Director  
**Target:** Common Hunter's Chest · `item.image` · `ICON`  
**Future delivery filename:** `icon-gs-chest-hunter-common.webp`  
**Director-approved operative specification:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` §§4, 4a, 4b, 6 · RUL-2026-10-20-006  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Workflow:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Live-game requests/writes:** 0/0. Credentials, uploads, publishing: none.

## What is wrong and what remains approved

The director previously accepted the premium TNR pixel-art Common Hunter original `1000018935.png` (source JPEG/RGB 1536×1536, 257500 bytes, SHA-256 `23038075363dc9ccafd4f4fb2ead70183704015ecb8f4abd66ad00bd8c23933a`). Its *pixel rendering, chest proportions, camera, one left/right metal hoop, saddle-brown leather material, one ivory fang, three front claw gouges and small cyan gem* are visually strong. The director **subsequently approved a functional geometry correction:** the long vertical leather strip must **stop at a compact upper-front keeper just below the front edge of the domed lid** rather than continue down toward the base. Previously accepted pixels are therefore a **same-subject edit source**, not a finished, fully conforming icon or a future Gatherer reference until the edited pixels are re-approved.

## ONE precise change (preserve everything else)

- The **single broad flat saddle-brown leather strap** runs over the domed lid, folds over its front lip and **ENDS in a short fitted receiver/latch at the UPPER FRONT, immediately beneath the lid seam**, secured by the existing simple ivory monster tooth/fang and small faceted cyan skyglass clasp as one coherent locking assembly.
- Remove the **entire long leather continuation beneath that upper front locking assembly**. After the short keeper, the lower front is exposed uninterrupted **DARK WOOD**; no dangling leather tail or second buckle to the bottom edge. Do not replace the missing leather with a metal vertical rail.
- Keep the **three diagonal claw gouges on the front-left wooden panel** unobstructed. Keep **one smooth plain Common ivory fang**, not a more exotic Rare/Epic tooth. Keep the single compact cyan clasp.
- Preserve exactly **ONE separate left outer metal lid hoop and ONE separate right outer metal lid hoop**, connected to their corner fittings, and only ONE leather center strap. Do not create a double right-side arch, duplicate strap, extra clasp, or double-layered band.
- Keep the same eye-level 3/4 chest footprint and **premium high-quality TNR pixel-art**: crisp stepped intentional pixel clusters, limited dark palette, flat cel-shaded tonal ramps, no photoreal gloss or airbrushed smoothing. This is a **targeted geometry edit** rather than a visual redesign.

## Reference / execution discipline

Prefer revising the existing Common Hunter image in its **original isolated generation session**, where it is already the same-subject source. Make exactly ONE edited candidate. The original Skyglass Reliquary remains MATERIAL/PALETTE ONLY; **do not attach any of the six earlier geometry-revoked chest images**, the smooth-painted Common Hunter, or unrelated references. If the edit surface cannot preserve the pixel-art register and rest of the geometry, restart a **clean isolated generation** using only the original Reliquary plus this brief, NOT a rejected prior image as a style template.

**Concise edit instruction for the isolated session:**

> Preserve the entire approved premium pixel-art Common Hunter's Chest—its camera, domed shape, EXACTLY two outer metal lid hoops, dark wood, single broad saddle-brown leather strap over the lid, white monster fang, compact cyan crystal clasp and three claw gouges. Change ONLY the strap fastening: the leather folds over the front lip and terminates in a short functional upper-front keeper immediately below the lid seam, secured by the existing fang/crystal assembly. Remove the long strip of leather from below the upper latch down to the bottom of the chest, exposing dark wooden front planks in its place. No extra straps, dangling tails or vertical metal replacements. Same crisp TNR pixel-art clusters, cel-shading and limited palette, single centered square icon.

**Negative:** no strap continuing into bottom half of chest, no second center strap, no extra parallel metal hoops, no down-to-base rope/strap, no missing tooth or crystal, no displaced claws, no new glowing claw brand, no Rare/Epic/Legendary motif details, no labels/UI/halo.

## Acceptance / next gate

1. Inspect at original source and **125 px** for a visibly **short** leather binding ending at the upper front latch. Confirm no additional metal bands, no extra leather; all physical parts attach plausibly. Verify front panel is open below the clasp and three claw marks clear.
2. Present ONE candidate for **fresh director visual acceptance**; don't equate the historical 1000018935 approval with acceptance of the edited image. The Common Hunter pixel-rendering register remains the style goal.
3. If approved, return exact source bytes, true MIME, dimensions, SHA-256, and user approval. Preserve previous JPEG raw as historical provenance; output correct lossless WebP through studio processing only after native-alpha/key cleanup and `artpreflight.py --type ICON`.
4. Only after the director approves this shortened-latch Hunter may the studio issue a **fresh corrected Common Gatherer isolated brief** using original Reliquary + *new Hunter* as the two reference images. Common Gatherer must terminate its jute rope in a compact front-upper knot, with no thick rope continuation to the base. Both fronts keep their distinct claw/leaf brands.

## First short-latch candidate — geometry better, style wrong (2026-10-20)

- **Candidate:** `1000018947.png`; actual JPEG RGB 1536×1536, 374075 bytes, SHA-256 `8e05446eef6d5866c04a066f2d798d8cf8ae5570e4943ba50f334ca4099afa7e`; black opaque background, alpha/preflight NOT_RUN.
- **Director:** “That looks better.” This expresses improvement in shortening the long leather strap but **does not explicitly approve this candidate**.
- **Art-director review:** The long lower-front leather is now removed, exposing front wood; upper fang/crystal latch, original single left/right metal hoops and three front claws remain recognizable. **This geometry change is directionally successful.** However, the entire new image is rendered as a smooth/high-frequency painted fantasy illustration, with gradients and antialiasing, rather than the mandatory ratified **premium TNR pixel-art** style. It closely resembles the earlier smooth-painted rejected raw `1000018934.png`. The intended pixel-art style reference is `1000018935.png`, the director's explicitly approved premium pixel source.
- **Do not copy the paint regression into any future family reference.** This image is a **nonapproved** style-mismatch candidate. Do not use it to launch Common Gatherer.
- **Precise next action:** Modify the **pixel-art original `1000018935.png`** at the central leather area only: take out the long lower-front leather tail, replace it with the existing dark wood treatment, and terminate the single flat brown strap in a short receiver just under the lid seam. Preserve the *actual chunky, intentional pixel clusters*, crisp stepped lineart, flat cel ramps, shading, face, fang, gem, dark wood and proportions. **Do not restart by editing the older smooth-painted image `1000018934.png` or the latest painted short-latch candidate `1000018947.png`.** After producing one candidate, inspect style and geometry at full resolution and 125px before seeking renewed director acceptance. No game interaction/processing.
