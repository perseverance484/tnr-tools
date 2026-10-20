# Isolated generation 03 — Ghost Ship Rare Hunter's Chest

**Status:** READY FOR ISOLATED GENERATION; director visual approval PENDING  
**Lead:** Image Production · **Supporting lens:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical approved direction:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (sections 2–7), `RUL-2026-10-20-002`  
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Art target:** `ICON` (`item.image`); production filename `icon-gs-chest-hunter-rare.webp`  
**Live-game requests/writes:** 0/0; no credentials, game uploads, publishing, or repository writes from isolated generation.

## Target and approved evolution

- One **complete closed domed-lid** Hunter's Chest; **three clear parallel claw gouges** on the front, **leather strap and bone/fang clasp** on the lid/front, one faceted skyglass crystal clasp. Preserve the approved Common Hunter's family silhouette, camera, distinctive object parts, and scale.
- **Rare-tier upgrade only:** reinforced dark iron bands with **steel rivets**, a **brighter** pale-cyan faceted skyglass crystal clasp, and **faint skyglass light along the lid seam**. Maintain dominant dark iron/dark wood. Hardware and seam should make it perceptibly finer than Common at 125 px, but not as ornate as Epic.
- **Do not introduce** Gatherer's leaf, rope or sprig; **do not** introduce Epic silver trim/glowing claw brand, Legendary silver filigree/lid crystal cluster, Rusted corrosion or broken crystal, Ornate aged gold, or Mystery chains/mist.
- Composition: eye-level 3/4, the same silhouette scale as Common, centered as a single isolated holdable chest; front claw scratches clearly readable, face unobscured, no table, no backdrop, no external glow halo.

## Attach exactly TWO individual approved images

1. **Skyglass Reliquary**, exact repository source `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp` (original style/material only; Git blob `eefd3e22c2fff6255f231b5402697b68f5fd7577`). Use near-black iron/dark wood, restrained cyan glass, crisp edges and cool rim highlights. **Do not** copy its flat lid or hanging vertical clasp composition.
2. **Approved Common Hunter's Chest**, original conversation attachment `1000018925.png`; decoded format **JPEG** despite `.png` name; 1536×1536, SHA-256 `b341d9e939d7a5cb182ac8576ab97777b36cfea607a3e4d6768052554ea3e4f3`. **Subject/family motif, camera, scale and rendered style reference only.** Preserve three claw gouges and leather/fang identity. Upgrade the materials instead of duplicating Common. **Its opaque black matte is not part of the visual style to copy.**

The full individual image **bytes** must be attached to the new conversation. Text names/URLs or a contact sheet do not substitute for images. Never attach Common Gatherer's art to this Rare Hunter generation.

## Approved subject + shared style + background

**Positive prompt:**

`a closed domed-lid Hunter's chest of dark wood with reinforced blackened iron bands and steel rivets, a brighter small faceted skyglass crystal clasp, a leather strap with a bone fang clasp, three parallel claw gouges branded on the front panel, a faint pale cyan glow along the closed lid seam, game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object, transparent background`

**Shared negative, verbatim:**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Tier/family exclusions:** no leaf brand, rope binding, sprig, silver ornamental borders or filigree, gilding, crown/lid crystal cluster, oversized magic glow, chains, rust, corrosion, cracked gem. No flat-lidded Reliquary silhouette.

**Background:** native transparency preferred; black opaque matte **not accepted for production**. If native transparency is unsupported, use only the approved alternative `on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`. Never blend the black matte from the Hunter reference into the new output.

## Isolated generation and return

1. Generate **ONE** square, complete, single-subject Rare Hunter's Chest candidate; inspect the actual pixels before showing to director.
2. Seek **director visual approval**, which is distinct from processing/preflight. Same-subject revision stays here; **two wrong-subject results** mean stop and relaunch clean.
3. Return **original source image bytes**, target name, approval status and filename to Art Studio. **Do not** process, claim production-ready, create icon sheets or upload.
4. Art Studio logs decoded MIME/dimensions/SHA, checks 125/64/32px size and family distinctions, resolves native alpha/flat lime key, pad square, lossless WebP (~256×256 and <460800 bytes), checks dark composite, and runs canonical `artpreflight.py --type ICON`.
5. Next generation session after approval: **Rare Gatherer's Chest**, using Reliquary + approved **Common Gatherer's Chest** as the two image references. Its rarity treatment must match Rare Hunter's, but do not include Hunter as a third reference.
