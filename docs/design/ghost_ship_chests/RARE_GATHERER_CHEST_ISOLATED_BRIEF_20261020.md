# Isolated generation 04 — Ghost Ship Rare Gatherer's Chest

## GEOMETRY-RESET OVERRIDE — PREVIOUS APPROVAL REVOKED (2026-10-20)

The director has rescinded the visual acceptance of this chest and **all six** earlier Common/Rare/Epic originals because an **extra/duplicated curved metal lid band** was propagated through the family. This prompt and any “approved” notes below are **historical only**; the pictured raw is **REJECTED AND PROHIBITED AS A FUTURE REFERENCE**, even if otherwise visually attractive. Read `GEOMETRY_RESTART_20261020.md` and the reset studio register. Rebuild this slot with corrected physical band continuity and a NEW raw source; use only the original Reliquary (style/material only) and **newly** geometry-correct predecessors as appropriate. Preserve prior hashes/decisions as evidence, but do not count them as currently approved or game-ready.

**Status:** REVOKED — GEOMETRY INVALID, historical design/approval record only; new corrected raw required
**Lead:** Image Production · **Supporting lens:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (sections 2–7), director ruling `RUL-2026-10-20-002`  
**Workflow:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Type:** `ICON` (`item.image`); **delivery filename:** `icon-gs-chest-gatherer-rare.webp`  
**Live-game requests/writes:** 0/0; no credentials, repository art writes, uploads, publishing.

## Target identity and composition

One **closed, domed-lid Rare Gatherer's Chest**, framed exactly like the approved Common Gatherer's Chest. Match the approved Ghost Ship / Skyglass painted material register, eye-level 3/4 camera, comparable size and restrained dark wood.

**Gatherer's identity must be the first read at 125 px:**
- **A single prominent leaf brand** engraved/branded on the front wood panel, still visible and recognizable.
- **A coiled, textured rope binding** over the lid and around the front.
- **A small gathered green sprig tucked beneath the rope**, the same botanical vocabulary as approved Common Gatherer; do not let metal reinforcement cover it.
- **One faceted pale-cyan skyglass clasp**, now brighter with a visibly more robust mounting.

**Rare-tier evolution, approved after Rare Hunter iterations:**
- **Structurally reinforced**: layered/stepped raised steel lid bands, enlarged/angular riveted steel armor at the upper corners/shoulders, and a more elaborate protective housing for the skyglass clasp.
- **Visibly different material COLOR from Common**: brighter *cold steel / gunmetal* reinforcement plates against the near-black wood/iron base. This must read as an upgrade even in grayscale; not merely cyan lighting pasted over the Common chest.
- **Small four-point star rune motifs** discreetly engraved into some reinforced steel plates or clasp housing, echoing the approved Rare Hunter visual treatment. They remain supporting ornamentation, *not* the front-panel family emblem, and do not become silver filigree.
- **Narrow, faint cyan light along the closed lid seam**. No blue light stripes crossing the whole body, magical aura, glowing leaf brand, or Epic/Legendary radiant decoration.

The completed pair should read **Rare Hunter = fortified cold-steel/rune Hunter chest with claws and fang** versus **Rare Gatherer = equally fortified cold-steel/rune Gatherer chest with leaf, rope and sprig**. The first identity difference must remain obvious at **125 px**.

## References — attach exactly TWO individual approved images

1. `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp` (original repo source; Git blob `eefd3e22c2fff6255f231b5402697b68f5fd7577`): **STYLE/MATERIAL ONLY**. Match near-black iron/dark wood, cyan crystal, restrained rim highlights and crisp painted silhouette. **Do not** imitate its flat lid.
2. **Director-approved Common Gatherer's Chest**, source conversation attachment `1000018926.png`, SHA-256 `acb6f618cdbc3b5414a3bfbfaabc682b9e03403141fe0d8b7b8c0a4a5356381a` (actual decoded file is JPEG/RGB despite name): **SAME-SUBJECT, FAMILY-MOTIF, SILHOUETTE, CAMERA AND SCALE REFERENCE**. Preserve rope/leaf/sprig; evolve the material treatment. Its opaque black matte **is not** a reference for a valid icon background.

**Do not attach the approved Rare Hunter's Chest as a third reference**; its approved Rare-tier material/color/motif treatment is conveyed by this brief in words only. Do not attach old pixel art, rejected candidates, contact sheets or collages. A URL/filename alone is insufficient: actual image bytes must be attached.

## Generation prompt

**Subject (the approved Gatherer's subject with the approved Rare treatment):**

`a closed domed-lid Gatherer's chest of dark wood with layered cold gunmetal steel reinforcement bands, riveted angular corner armor and a reinforced faceted pale-cyan skyglass crystal clasp, a coiled rope binding with a small green sprig tucked under it, a single leaf branded clearly on the front panel, subtle engraved four-point star runes on a few steel plates, faint cyan illumination along the closed lid seam`

**Shared style clause (canonical, unchanged):**

`game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Background clause:** `transparent background`. If and only if true transparency cannot be generated, use `on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`. Do not reproduce the black opaque matte from the Common reference.

**Shared negative clause (canonical, unchanged):**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Additional family/tier exclusions:**
- No three claw marks, leather straps, fang/bone clasp, or other Hunter motifs.
- No obscure leaf brand, missing rope/sprig, or metal plating over the Gatherer identity.
- No plain-Common nearly identical hardware with only blue light added.
- No Epic silver trim or glowing leaf brand; no Legendary filigree or lid-mounted crystal clusters; no Ornate gold; no Mystery crossed chains and lock; no Rusted distress or cracked crystal.
- No runic symbols standing in for a leaf brand, no oversized four-point star on the front, no excessive cyan illumination, no low angle.

## Isolated generation gate / return

1. Generate **exactly ONE square icon candidate**, one closed chest, and inspect the rendered pixels for Gatherer identity, visible Rare-tier structural/material/color upgrade, camera, background and no prohibited elements.
2. Compare mentally against Common Gatherer at **125 px**. Distinguish Rare by structure *and* cold gunmetal/runes, not only stronger lighting; preserve equivalence in rarity strength with approved Rare Hunter despite that approved Hunter image **not** being an attached reference.
3. Present this one candidate for **director visual approval**. Same-subject revisions may remain in this conversation; after two wrong-subject/composition generations, close it and restart clean.
4. On approval, return the **original exact image bytes** to the persistent Art Studio. **Do not** process, convert to game WebP, construct a collage, commit art or upload. Studio will record MIME/size/hash, complete raw QC, resolve native-alpha/flat-lime key, pad to square, run 125/64/32px family comparisons and `artpreflight.py --type ICON` on the final lossless WebP.
5. Following approval, the next distinct session is **Epic Hunter's Chest**, with Reliquary + approved Hunter-family image as its only two references.

## Director visual acceptance and studio intake (2026-10-20)

**Director:** “Approved, next.” This records visual acceptance of the Rare Gatherer's Chest as supplied; it does **not** certify production readiness.

- **Received conversation source:** `1000018930.png` (extension is misleading: Pillow decodes **JPEG**). RGB, **1536×1536**, **420968 raw bytes**, exact SHA-256 `d5e44dba4c5947067ee0da8cef1d7e326a1aafbec7d85c21e6eba76db33a31a4`.
- **Visual subject:** single complete closed domed-lid chest, substantially reinforced polished cold-gunmetal/steel lid bands and corner rivets, engraved small star-rune motifs, brighter enlarged cyan clasp, narrow cyan seam light; Gatherer leaf on front panel and rope/sprig retained and distinguish it from Hunter.
- **125 px visual pair gate:** inspected alongside director-approved Common Gatherer's in a deterministic Lanczos-downsampled two-icon comparison. Reinforced silver-cold metal and seam differentiate Rare from Common; leaf/rope/sprig family identity remains visible. 64/32 px stress-preview images also made; they are visual aids, not mechanical preflight.
- **File/background gate remains BLOCKED:** raw is JPEG RGB with **opaque black matte**, no alpha and no compliant flat lime `#00FF00` key. Producing a transparent alpha matte requires separate, verified handling of near-black chest edges; do **not** blindly key black and damage the accepted wood/metal details.
- **Not done:** no production-ready 256×256 lossless WebP, dark-composite alpha-edge QC, canonical `artpreflight.py --type ICON` run, `imagePack`, Forge ticket, or game upload. Actual delivered raw remains conversation-supplied; no Git binary pin.
- **Next session:** Epic Hunter's Chest (separate conversation), using only original Skyglass Reliquary + director-approved **Rare Hunter's Chest** as individual references; see `EPIC_HUNTER_CHEST_ISOLATED_BRIEF_20261020.md`.
