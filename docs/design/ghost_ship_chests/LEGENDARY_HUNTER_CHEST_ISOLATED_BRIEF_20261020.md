# Isolated generation 07 — Ghost Ship Legendary Hunter's Chest

**Status:** READY FOR ISOLATED GENERATION; director visual approval PENDING  
**Lead:** Image Production · **Supporting lens:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical approved direction:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (sections 2–7), `RUL-2026-10-20-002`  
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Art spec:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → `targets.ICON`  
**Target/client field:** `Legendary Hunter's Chest`, `item.image` → `ICON`  
**Required delivery filename (after studio processing):** `icon-gs-chest-hunter-legendary.webp`  
**Live-game requests/writes:** 0/0; credentials none; no image processing, repository art writes, game upload or publishing in isolated generation.

## Composition / identity lock

Create **one complete closed domed-lid Legendary Hunter's Chest**, eye-level 3/4 view, **same chest footprint, overall size and camera as the approved Epic Hunter's Chest**. Keep the Ghost Ship / Skyglass palette of dark wood, blackened iron, bright silver craftsmanship and faceted pale-cyan skyglass, painted crisp dark outlines, restrained cool highlights.

**Hunter identity remains fixed and unmistakable at 125 px:**
- **Three parallel claw gouges branded into the front wood panel**, glowing from within pale cyan as established on Epic Hunter. The scratches are the Hunter family mark, not arbitrary blue streaks, not a Gatherer leaf.
- Brown **leather strap over the domed lid with the bone/fang clasp**. Preserve its authentic leather/bone look; the Legendary trim must **not** cover it.
- Large front-centered skyglass clasp gem and strong metal housing, as Epic's counterpart, now exceptionally refined but still distinct from the **new small crystal group on top of the lid**.

## The approved Legendary upgrade — ABOVE Epic in materials AND silhouette

**The critical new Legendary silhouette feature is a SMALL PHYSICALLY MOUNTED CLUSTER of faceted skyglass crystals crowning the top ridge of the domed lid.** Build it as a compact arrangement, approximately one taller central cyan shard with two smaller flanking shards, rising just above the lid outline. Secure it in a delicate reinforced silver base fixed to the chest; do not depict floating crystals or a huge spiky crown. Position it where it is **clearly visible at 125 px** without obscuring the leather strap/fang clasp or overpowering the rest of the chest. This must be recognizable beyond the silver color increase.

**Secondary new Legendary material language:** refined **silver filigree** engraved and interwoven over the existing Epic silver-edged reinforcement plates, especially on selected curved lid bands, corner faces and crystal mounts. It must read as exquisite deliberate craftsmanship rather than a washed-out white chest, cluttered metal plating or the ornate goldwork reserved for the separate Ornate Chest. Some four-point star rune details may survive as minor metal engravings; do not let runes replace the claw emblem.

**Legendary illumination:** the **brightest pale-cyan skyglass treatment in the normal tier ladder**, focused within the new lid shards, front gem, and three carved claw marks, with thin localized cool edge highlights. The shine is intrinsic to crystal facets and engravings; no broad light halo/disc, glowing background, solid magical beams, fog, stars orbiting the chest, or field of particles. Keep the chest unmistakably dark wood and near-black iron under the silver.

**Reserved elements:** Ornate is a separate, grander chest with heavy silver filigree **and aged gold**; Legendary must **not** add gold. Mystery is defined by crossed chains, a heavy lock and skyglass mist; do not borrow it. Rusted corrosion, Gatherer leaf/rope/sprig, open lid or spilled treasure are forbidden.

## Exactly TWO separately attached reference images

1. **Original Skyglass Reliquary:** repository `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`, Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`. **STYLE / MATERIAL ONLY** (dark wood, near-black iron, cyan faceted skyglass, crisp painted edge, cool rim light); its **flat-lidded box and central hanging-clasp silhouette are not subject references**.
2. **Director-approved Epic Hunter's Chest:** original source attachment `1000018931.png`, actual JPEG/RGB 1536×1536 despite name, SHA-256 `9cdded700f3027e2788ba040cc1995667afb322ef229476d51436728e02d0339`. **SAME-SUBJECT / HUNTER FAMILY MOTIF / CAMERA / SCALE / PRIOR-TIER STARTING POINT**. Preserve brown leather/fang strap, glowing three-claw brand, dark wood, silver-edged armored bands and central crystal. Evolve it via **physically mounted lid shard cluster, silver filigree and controlled brighter crystal treatment**. Reference's **black matte is not a valid production background**.

Attach the **actual individual original image bytes**. Do not attach Rare Hunter, Gatherer icons, rejected candidates, a gallery/contact sheet or a third image. URLs and hashes in the written prompt do not prove that reference pixels were ingested.

## Approved subject and rendering prompt

**Subject line (Hunter's established subject, with the approved Legendary treatment):**

`a closed domed-lid Legendary Hunter's chest of near-black iron and dark wood, exquisite engraved silver filigree decorating silver-edged reinforced lid bands and riveted corner fittings, a small physically mounted cluster of three faceted pale-cyan skyglass crystals crowning the curved top ridge of the lid, one prominent refined faceted cyan skyglass crystal clasp on the front, a brown leather strap with a bone fang clasp, three parallel claw gouges branded into the front wood panel glowing pale cyan from within, the brightest tier of restrained crystal illumination with no halo`

**Canonical shared style clause, verbatim:**

`game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Background clause:** `transparent background` with **actual native alpha preferred**. If genuine alpha cannot be produced, use the canonical workstream fallback `on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`. Do NOT reproduce the opaque black matte of the Epic reference; this has blocked all earlier `ICON` production preflights.

**Canonical shared negative clause, verbatim:**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Additional wrong-subject/tier negatives:** no leaf, rope, sprig, woven greenery (Gatherer); no flat Reliquary lid; no gold accents or lavish ornamental gold (Ornate); no chains, oversized lock or curling mist (Mystery); no broken/rusted metal, cracked/dull crystal (Rusted); no gigantic crystalline hedgehog, horns, decorative magic sigils, separate hovering items or a crystal field. No chest so silver-white that dark wood disappears.

## Visual and isolation gates

1. Generate **exactly ONE square original candidate** depicting only the Legendary Hunter's Chest. One target per isolated conversation, no collage, sheet, mockup or processing.
2. **Pass the 125px recognition test against approved Epic Hunter:** lid-mounted **small shard cluster must visibly change the top silhouette**; fine silver filigree must read as physical material craft and support a brighter yet restrained glow. A mere glow/color adjustment is insufficient (Rare tier differentiation lesson).
3. Preserve recognizable three glowing claw gouges, leather strap and bone fang clasp. Show candidate for **director visual acceptance**. Same-target revisions may remain in the same session; **two wrong-subject/composition failures** mean close and open a fresh clean conversation.
4. Return original exact source bytes, intended filename and director approval status to the persistent studio. The generator must **not** key/crop/export WebP, commit binaries, alter manifests, call the live game or upload.
5. At studio intake separately check decoder/MIME, dimensions, true alpha/chroma field and SHA-256; compare 125/64/32px previews against approved family originals; preserve the approved raw; process with canonical `ICON` key/alpha/pad/resize pipeline, output lossless WebP **256×256 recommended, under 460800 bytes**, inspect dark composite edges and run `artpreflight.py --type ICON`. Do **not** equate director visual approval with upload readiness.
6. Next distinct session, after Legendary Hunter approval: **Legendary Gatherer's Chest**. It will reference only the original Reliquary and approved **Epic Gatherer's Chest**, transferring Legendary's silver filigree/lid crystal cluster/tier brightness into the botanical family **in text** rather than attaching Hunter as a third image.
