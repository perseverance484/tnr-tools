# Isolated generation 01R — Common Hunter's Chest (geometry restart)

**Status:** READY FOR NEW CLEAN ISOLATED GENERATION — director-approved geometry AND binding material ladder (RUL-2026-10-20-005); replacement image acceptance PENDING  
**Lead:** Image Production · **Support:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Reset authority:** `GEOMETRY_RESTART_20261020.md` (director withdrew visual approval from all 6 former raws)
**Binding material ruling:** `CHEST_BINDING_MATERIAL_LADDER_PROPOSAL_20261020.md` (director-approved material proposal, details canonized in `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` §4a; RUL-2026-10-20-005)  
**Approved broader art direction:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md`, `RUL-2026-10-20-002`  
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Target:** Common Hunter's Chest · `item.image` · `ICON`  
**Eventual production filename:** `icon-gs-chest-hunter-common.webp`  
**Live-game requests/writes:** 0/0, credentials none. No generation in persistent studio, no upload, publication or game requests.

## Why this is a clean restart

The director discovered a recurring incorrect **extra metal band beside the right lid hoop**, amplified into adjacent double-arch reinforcement at higher tiers. All six earlier Common/Rare/Epic Hunter and Gatherer originals are **REVOKED**, including the previously accepted Common Hunter. **Do not attach or imitate any of those rejected originals**. Previous “approved” labels, source hashes or reference status in older prompts do not authorize reuse. Cancel the earlier Legendary Hunter generation too.

**Director geometry confirmation (2026-10-20):** “Sure, that looks fine. It was the double band on one side that threw it off.” This **approves** the corrected physical topology: one **left end hoop** and one **right end hoop**, plus the separate **central leather family strap**. The extra side-by-side *independent* band on one end was the actual defect. A metal edge highlight or trim on the same hoop is permissible only if it does **not** form a new parallel band volume. This confirmation is **not** approval of a yet-to-be-generated replacement image.

## Director-approved binding material for Common Hunter

**Binding identity is now deliberately tier-specific; this is not permission to add straps.** See `CHEST_BINDING_MATERIAL_LADDER_PROPOSAL_20261020.md`. Common Hunter uses **one smooth, medium-warm saddle-brown tanned leather strap**: broad, flat, visibly simple, with a small bone fang clasp and no visible decorative silver stitching. It contrasts with Common Gatherer's proposed **one golden-tan chunky twisted jute rope**, rounded and fibrous, with a tucked green sprig.

The remaining named tiers have their **own director-approved** Hunter hide / Gatherer rope materials (Rusted ruined rawhide / hemp; Rare pebbled smoky hide / waxed slate flax; Epic glossy black silver-stitched leather / pale silver sea-silk; Legendary midnight scale-embossed silver/cyan-thread leather / indigo silk with cyan filaments). These later-tier materials are **excluded from Common**. The approved material ladder **does not alter** the confirmed single-left-hoop/single-right-hoop/one-central-family-binding geometry.

## Geometry lock — solve object structure BEFORE ornament

- One **complete closed domed lid** made of curved dark-wood staves running coherently from front to back. Lid arches smoothly without a broken/duplicated volume, irregular side panel or false horizon line.
- **Exactly TWO external metal end hoops TOTAL**, one left and one right on the curved lid. Each hoop is one physically continuous band across the lid's curvature; each enters or aligns with one set of matching reinforced front/side corner fixtures.
- **Only one metal arch per end**. At the camera-right end, the rim of the existing band may have a *thin highlight* on its own surface, but **NOT a second parallel detached metal strip with its own thickness and shadow**. The camera-left end has the same constraint.
- **ONE central smooth saddle-brown tanned LEATHER strap**, broad **flat band of hide** across the crown and down the front, distinct from the two metal end hoops, terminating at a simple visible **bone/fang clasp** above the front cyan skyglass crystal. Keep the leather **plain, unembossed and without silver stitching** at Common; this material is visibly different from Gatherer's **single thick round honey-tan jute rope**. One leather strap only; its edges are **part of the same strap**, not two additional metal arches. No extra band copied from a style reference.
- The front face carries **exactly three diagonal parallel claw gouges**, visibly carved in dark wood with earthy exposed wood inside; neither glowing nor replaced by a leaf.
- One **small faceted pale-cyan skyglass crystal clasp** in a compact dark metal setting on the central front. No extra large gem or seam glow.
- Camera eye-level 3/4; one chest; dark wood and blackened plain iron; solid single silhouette, centered, transparent margin for the inventory rarity frame.

**Critical pass/fail:** Before showing any image to the director, inspect the full-resolution pixels of **both** end hoops, their endpoints, the side panel and the **ONE distinct flat smooth saddle-brown leather center strap**. Reject a chest with an added narrow parallel metal arch (especially right), a second leather strap, or leather rendered as rope. Check again at **125 px**. A correct color palette is not enough. Verify that the Common leather has **no Rare/Epic/Legendary material ornament**.

## Actual reference bytes — ONE image only

**Original Skyglass Reliquary:** `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`, Git blob `eefd3e22c2fff6255f231b5402697b68f5fd7577`.

**ROLE: MATERIAL / RENDERING ONLY.** Inspect its dark wood, near-black metal, rivet treatment, cyan faceted crystal, crisp painted outlines and cool highlights. **IGNORE ALL BOX/LID SHAPES, CLASPS, STRAPS AND METAL-BAND LAYOUT FROM THE RELIQUARY.** No Sage's Strongbox, former Ghost Ship chest, old pixel-art chest, rejected attempt or image collage attached.

A style-reference image is **not** an assembly blueprint. If the Reliquary visibly biases the rendering back toward the duplicated band, stop and propose a clean text-only regeneration plan rather than adding more failed reference images.

## Subject + approved style (geometry confirmed; use in a fresh isolated conversation)

**Subject:**

`one closed domed-lid Common Hunter's Chest built from curved dark wood staves, EXACTLY ONE plain blackened iron arched end hoop at each outside end of the lid (one on the left and one on the right, no adjacent duplicate or extra steel arc), ONE separate centered broad FLAT SMOOTH SADDLE-BROWN TANNED LEATHER STRAP curving over the dome and down the front, plain natural hide with no embossing or silver stitching, secured by a simple bone fang clasp above ONE small pale-cyan faceted skyglass crystal clasp, exactly THREE parallel diagonal claw gouges carved into the front dark wood, coherent physically connected chest construction, restrained Common-tier hardware and no external seam glow`

**Canonical shared style clause (unchanged):**

`game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Background:** `transparent background` with true native alpha. If native alpha is not possible, `on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`. **Reject opaque black.**

**Canonical shared negative clause (unchanged):**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Additional geometry/material negatives:** no double bands on right, no second thin parallel arched steel strip adjacent to either end hoop, no floating/disconnected side rail, no mirrored duplicate leather strap, no two leather center straps, no rope-like braid or tan twisted cord on Hunter, no rawhide decay (Rusted), no pebbled salt-cured hide/steel eyelets (Rare), no glossy black leather/silver stitching (Epic), no scale-embossed midnight hide/cyan-inlaid thread (Legendary), no reinforced multilayer Rare plates on Common, no glowing claw mark, no silver Epic trim, no Legendary filigree/crystal crown, no Gatherer's leaf/rope/sprig, no flat Reliquary silhouette.

## Isolated session boundary and return

- **Director confirmed the geometry lock** and subsequently **approved the binding material ladder** on 2026-10-20. Both direction gates are cleared. Generate **ONE** square, centered, closed chest in a **NEW CLEAN GENERATION CONVERSATION**, not this persistent studio.
- Fail fast on structural geometry before seeking director judgment; then check family motif, style, background and 125px recognizability. If a wrong-subject/composition error repeats twice, close and start a new clean isolated conversation.
- The director must approve the *corrected geometry* visibly before treating this as a replacement for Common Hunter. Prior approval of the invalidated image is not transferrable.
- Return exact original source bytes with approval and target name. Do not process, crop, export lossless WebP, run preflight or upload in the isolated session.
- After a corrected Common Hunter is visually accepted, create a NEW Common Gatherer isolated brief and reference the original Reliquary plus **corrected** Common Hunter only. Never use an invalidated raw as an image reference.
