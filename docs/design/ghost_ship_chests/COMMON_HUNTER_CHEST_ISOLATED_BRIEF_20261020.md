# Isolated generation 01 — Ghost Ship Common Hunter's Chest

**Status:** READY FOR ISOLATED GENERATION · **raw approval:** PENDING  
**Lead:** Image Production · **Supporting lens:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical approved brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (sections 2–7)  
**Director approval of direction:** `RUL-2026-10-20-002`  
**Isolated-generation protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Art spec:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → target `ICON`  
**Live-game requests/writes:** 0/0. No credentials, repository art writes, uploads or publication in this generation session.

## Identity lock

- **Target:** Common Hunter's Chest, Ghost Ship item reward chest.
- **Target field/type:** `item.image` → `ICON`, not `JUTSU_ICON`.
- **Delivery filename after studio processing:** `icon-gs-chest-hunter-common.webp`.
- **Role within set:** first of 12. Director approval of the original is the **rendered style lock and Hunter's family motif lock**. Do not treat generation as that approval.
- **Composition identity:** one complete **closed, domed-lid** chest (not the Reliquary's flat lid), viewed eye-level in 3/4. One focal chest silhouette, front panel with **three prominent parallel claw gouges**, leather strap with **bone fang clasp**, one **small** skyglass crystal clasp; no competing large objects.
- **Tier identity:** Common = plain blackened iron bands on dark wood; no Rare rivet escalation, Epic silver trim or glowing brand, Legendary filigree/crystal cluster, or Rusted distress.
- **Readability:** chest shape and claw-gouge Hunter's emblem visible at 125px, clean outer outline and transparent margin. A future Gatherer's twin must read as a different family at the same display size.

## Reference — ONE individual image attached

**Actual attached image bytes required:** `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`, pinned at repository `main@4e8346ba71e4f72d3b14a81bd1ec2a5e92b921bc`; Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`.

**Role:** **STYLE / MATERIAL ONLY**. Follow near-black wood/iron, restrained cyan crystal, riveted hardware, cool highlights, crisp dark edges and camera. **Do not** reproduce the reference's flat-topped geometry, large hanging vertical crystal lock or box silhouette. No old chest/pixel-art reference. Do not attach another image, collage, thumbnail or previous failed attempt. A URL/file path in the prompt does **not** count as a pixel reference: attach the actual original image file.

## Positive prompt (use exactly the approved subject line and shared style clause)

`a closed domed-lid chest of plain blackened iron bands on dark wood, one small skyglass crystal clasp, a leather strap with a bone fang clasp, three parallel claw gouges branded on the front panel, game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object, transparent background`

**Shared negative (exact approved clause):**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

The Common tier is **not** externally radiant: the crystal can show gentle light *within its facets* per the shared material style clause, but do **not** cast a visible halo, seam glow, luminous claw brand or large light field. The director visually judges the candidate and locks how this register looks before future icons.

**Background fallback only if true alpha is unsupported:**

`on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`

## Generation and return gate

1. Generate **exactly ONE** square, single-object candidate for the Common Hunter's Chest and visually inspect the actual resulting pixels for correct subject, closed domed lid, Hunter's leather/fang/claw motifs, camera and transparent/lime field.
2. Show the single candidate for **director visual approval**. Same-target revision is allowed within this session; after two wrong-subject/composition results, **stop and restart a fresh isolated session** rather than stacking rejected-image references.
3. The generator **does not** key backgrounds, edit transparency, crop, export game-ready WebP, execute `artpreflight.py`, make repository changes or upload anything. Preserve and return the **original source bytes** (not screenshot), target name and director approval status to the persistent Art Studio.
4. Studio intake then performs raw QC, provenance/hash, alpha or chroma processing, pad to square, lossless WebP export, dark composite, 125/64/32px readability and `artpreflight.py --type ICON`. This delivery is not finished before those checks.

**Next gate after icon 01 acceptance:** prepare icon 02 (Common Gatherer's) in a **new** generation session, attaching only this same Reliquary source plus the director-approved original icon 01.
