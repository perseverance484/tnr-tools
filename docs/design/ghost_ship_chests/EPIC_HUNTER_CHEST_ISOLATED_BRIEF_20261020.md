# Isolated generation 05 — Ghost Ship Epic Hunter's Chest

**Status:** DIRECTOR VISUALLY APPROVED (2026-10-20); production-alpha/export/preflight PENDING  
**Lead:** Image Production · **Supporting lens:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (sections 2–7), director ruling `RUL-2026-10-20-002`  
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Asset type/client field:** `ICON` / `item.image`  
**Required delivery filename (after studio processing):** `icon-gs-chest-hunter-epic.webp`  
**Live-game requests/writes:** 0/0; no credentials, image processing, game uploads, publishing or repository writes in the isolated generation conversation.

## Composition and subject lock

Depict **ONE complete, closed domed-lid Epic Hunter's Chest**. In the same painted Ghost Ship / Skyglass art register and eye-level 3/4 camera as the approved Rare Hunter; dark wood, cold metal, rivets, cool restrained rim light, crisp dark painted outline, recognizable at 125px.

**Hunter family motif must survive clearly:** the *same three parallel front-panel claw gouges*, leather lid strap with a bone/fang clasp, and a centered faceted pale-cyan skyglass crystal clasp. The front brand must not be hidden behind enlarged hardware. No rope, sprig or leaf motifs.

**The Epic tier must read as an actual quality upgrade beyond Rare, not another Rare with brighter cyan lighting:**

1. **Silver-trimmed reinforcement.** Upgrade Rare's layered gunmetal armor into intentionally crafted, polished **silver-edged bands and angular fittings**. Silver should create clear metallic-value separation from Rare across the curved lid bands and high-level corners without replacing the dark-wood/black-iron foundation. Use defined physical trim and refined workmanship, not generic bloom.
2. **Larger faceted skyglass crystal.** Make a visibly enlarged high-quality cyan centerpiece within a strengthened metal clasp housing; crystal remains a single main clasp gem, **not** a lid crown cluster.
3. **Glowing three-claw Hunter brand.** The three carved claw gouges on the front wood panel should now be **recognizably illuminated from within in pale cyan skyglass light**, not plain brown slashes. This is the Epic distinguishing motif at 125 px; preserve the exact three-gouge geometry and avoid turning it into a random glowing glyph. Soft localized in-groove light only, no halo or projected lighting disc.
4. **Visual hierarchy:** closed domed chest silhouette first; **glowing triple claw brand and enlarged cyan clasp** as two restrained focal details; fine silver-edged reinforced metalwork as the main material-tier upgrade. Spare four-point stars from Rare may remain in minor metal details but must not displace the Hunter brand. Same overall chest scale/camera as the family.

**Preserve room above Epic:** Legendary is reserved for extensive **silver filigree**, a **small skyglass crystal cluster crowning the lid**, and its brightest glow. No gold (Ornate-only), no chains or mist (Mystery), no corrosion (Rusted), no floating runes/spell effects.

## References — attach exactly TWO separately

1. **Original Skyglass Reliquary:** `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`, Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`. **STYLE/MATERIAL ONLY** for paint, dark wood/iron, pale cyan faceted skyglass and cool edges; **not** flat-lidded chest shape or oversized hanging gem silhouette.
2. **Director-approved Rare Hunter's Chest:** studio-returned `1000018929.png` (actual decoded JPEG/RGB 1536x1536, raw SHA-256 `bb2d7affc025c49e21111f8db8f4a0bbc15b3930f96193a2c13ec9430c21793c`). **SAME-SUBJECT, FAMILY MOTIF, SCALE, CAMERA and RARE STARTING-POINT REFERENCE**. Retain claw/leather/fang and fortified silhouette; advance the metal craft and crystal/brand to Epic. Its black background is not a valid production-background reference.

Attach **actual original image bytes** individually, not just URLs/filenames; no rejected Rare candidates, Common Hunter as a third reference, Gatherer icons or collage. The visual intention may be communicated in words; only these two images may be passed as references.

## Generation text

**Subject line (approved Hunter's subject + Epic-tier treatment):**

`a closed domed-lid Epic Hunter's chest of dark wood, refined reinforced steel bands with visibly polished silver trim and silver-edged riveted corner armor, a larger faceted pale-cyan skyglass crystal clasp in a substantial crafted metal housing, a brown leather strap with a bone fang clasp, three parallel claw gouges on the front wood panel glowing softly pale cyan from within`

**Canonical shared style clause:**

`game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Background:** `transparent background` (genuine alpha required where possible). **If true transparency is unsupported**, use only `on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`. Opaque black is not an acceptable production background; reference-black should not be copied.

**Canonical shared negative clause (verbatim):**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Additional target/tier exclusions:** no leaf, rope or sprig; no glowing leaf; no flat Reliquary lid; no multiple standalone gems, elaborate silver filigree, crystal cluster on lid, gold plating, giant metallic wing shapes, overblown blue stripes, glowing magic sigils or a bright aura. No brand made of anything except the required **three claw gouges**.

## Gate and handback

1. Generate **exactly ONE square, complete Epic Hunter candidate** in a new isolated session. Inspect its actual pixels before presenting.
2. Compare with the approved Rare Hunter reference at **125px**: is the silver-trimmed construction visibly new, is the crystal larger, and do the three claw marks actually glow? A simple cyan tint pass or unmodified Rare construction is not an Epic pass.
3. Director visual approval is mandatory. Same-subject revisions stay in the isolated session; after two wrong-subject/composition attempts close and restart clean. Do not generate a second chest or a sheet.
4. Return **original raw image bytes**, target name and director approval state to persistent studio. Isolated generation does **not** export production WebP, key alpha, crop, run `artpreflight.py`, commit art, upload or publish.
5. Studio intake must decode true image MIME, record SHA-256/bytes, run 125/64/32 family QC, complete native-alpha or exact-lime chroma processing, pad transparently to square, lossless WebP (`ICON` spec: 256×256 recommended, under 460800 bytes), inspect dark composite and run canonical `artpreflight.py --type ICON`.
6. After approval move to the separate **Epic Gatherer's Chest** generation conversation, using the Reliquary and the approved **Rare Gatherer's Chest** as its two individual references. Preserve botanical family identity, describe Epic-tier upgrades in text only.

## Director-approved Epic Hunter original and visual gate (2026-10-20)

**Director:** “Approved, next.” This is visual acceptance of the displayed candidate; **not** a production/preflight approval.

- **Actual conversation original:** `1000018931.png`; despite `.png` extension it decodes as **JPEG**, RGB, 1536×1536, **498203 bytes**, raw SHA-256 `9cdded700f3027e2788ba040cc1995667afb322ef229476d51436728e02d0339`. Source remains attached in the conversation; **not Git-pinned**.
- **Approved appearance:** closed Hunter domed lid, brown leather/bone-fang clasp, recognizable **three bright cyan-glowing claw gouges**, visibly **polished silver trim** on raised armored lid bands/corner hardware, enlarged faceted cyan skyglass clasp, controlled star-rune insets. This advances Common → Rare → Epic by visible structural/material and focal-motif changes; does not introduce Legendary's lid crystal cluster or extensive filigree.
- **Visual size gate:** compared source images for Common Hunter / Rare Hunter / Epic Hunter at **125px** using deterministic Lanczos reduction; physical bright silver vs cold gunmetal and the triple glowing claw brand remain prominent. Additional **64px and 32px** stress previews constructed, not game-scale assertions and not final QC for alpha/compositing. Review images are mechanical composites of unchanged source pixels, **not input references for isolated generation**.
- **Production concern (unchanged from siblings):** opaque **black JPEG matte**, no true alpha, no approved uniform chroma-key background; original does **not** meet `ICON` transparency requirements. Requires separate approved safe matting/alpha restoration or a valid transparent original, avoiding loss of dark outlines. Final lossless WebP, actual byte cap, dark-background alpha-edge QC and canonical `artpreflight.py --type ICON` are **NOT_RUN**.
- **Next isolated target:** Epic Gatherer's Chest. Only the original Skyglass Reliquary and director-approved **Rare Gatherer's Chest** are image references; Epic Hunter's visual-tier upgrade is communicated **in text only**, never attached as a third image. See `EPIC_GATHERER_CHEST_ISOLATED_BRIEF_20261020.md`.
