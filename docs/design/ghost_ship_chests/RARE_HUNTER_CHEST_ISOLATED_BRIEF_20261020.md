# Isolated generation 03 — Ghost Ship Rare Hunter's Chest

## GEOMETRY-RESET OVERRIDE — PREVIOUS APPROVAL REVOKED (2026-10-20)

The director has rescinded the visual acceptance of this chest and **all six** earlier Common/Rare/Epic originals because an **extra/duplicated curved metal lid band** was propagated through the family. This prompt and any “approved” notes below are **historical only**; the pictured raw is **REJECTED AND PROHIBITED AS A FUTURE REFERENCE**, even if otherwise visually attractive. Read `GEOMETRY_RESTART_20261020.md` and the reset studio register. Rebuild this slot with corrected physical band continuity and a NEW raw source; use only the original Reliquary (style/material only) and **newly** geometry-correct predecessors as appropriate. Preserve prior hashes/decisions as evidence, but do not count them as currently approved or game-ready.

**Status:** REVOKED — GEOMETRY INVALID, historical design/approval record only; new corrected raw required
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

## Candidate 1 review and revision (2026-10-20; same subject)

**Director feedback:** “Kinda looks identical to common other than the blue tinge.” This is **NOT APPROVED** as the Rare tier visual. Correct Hunter's subject; inadequate *material/structural* progression, so revise **within the same isolated session**. It is not a wrong-subject failure.

The first candidate repeats Common's domed lid, leather/fang and central gem, claw marks, two hoop bands and metal corner blocks essentially unchanged; the biggest new feature is blue seam stripes. At 125 pixels and in grayscale, it is nearly the same chest. Do **not** fix this with more glow or a brighter crystal alone.

**Targeted revision:** keep family shape/identity, camera and scale, but visibly armor the lid and upper body: **layered stepped steel plates overlaying each curved hoop band**, **larger distinct riveted shoulder/corner reinforcement plates** that expand the mechanical upper outline, and **a stronger steel backing/housing for the skyglass clasp**. Keep the claw gouges fully visible, as well as leather strap and fang. These are *structural* Rare-tier upgrades, not Epic silver filigree or decoration. Reduce the bright cyan strips to **one delicate lid-seam glow**. Pass a comparison against approved Common Hunter at 125 px **and grayscale** before seeking director acceptance.

First candidate actual bytes: studio attachment `1000018927.png`, JPEG/RGB despite extension, 1536×1536, 372094 bytes, SHA-256 `dfdce5512e8f4d826519fd13550723297bcde17e881356b354cb958b07e416ce`. Black matte fails native-alpha/flat-lime production input requirement. Preserve this failure record; do not use failed image as a new reference attachment and do not claim it passed production QC.


## Candidate 2 — structural revision, not approved (2026-10-20)

After candidate 1 failed for appearing like Common with extra cyan, candidate 2 introduced substantially stronger stepped steel bands, angular reinforced corners, and a larger protected skyglass clasp. **Director feedback:** “there needs to be some sort of color or icon differentiation too, it still looks too similar.” **Result: NOT APPROVED.** Structural reinforcement alone was still insufficient. Correct subject, same-target revision rather than a wrong-subject strike.

Received source `1000018928.png`, actual decoder JPEG/RGB with opaque black matte, 1536×1536, 436920 bytes, SHA-256 `e99dfb130700ace9428e2f0f740b5328b9a402e2c6057c66b917902d06c9836a`. Candidate is rejected, NOT approved and must not be used as a generation reference.

**Director-directed Rare refinement:** retain mechanical armor, visibly distinguish Rare's reinforcement with **lighter cold-steel/gunmetal material**, and incorporate small engraved **four-point star rune details** on metal plates or skyglass crystal housing. Restrain seam glow and preserve Epic/Legendary escalation.

## Candidate 3 — visually approved Rare Hunter (2026-10-20)

**Director approval:** “There we go, approved.”

- Original conversation attachment: `1000018929.png`; actual decoded type **JPEG**, RGB, 1536×1536, 473394 bytes; SHA-256 `bb2d7affc025c49e21111f8db8f4a0bbc15b3930f96193a2c13ec9430c21793c`.
- **Approved visual content:** closed domed dark-wood Hunter's Chest, clear three claw gouges, brown leather strap and fang clasp, reinforced stepped cold-steel bands, angular armor/corner plates, substantial cyan crystal housing, four-point star engravings with restrained cyan insets, narrow cyan lid-seam light. Distinct from Common in both armor and palette/motifs.
- **Tier style lock for subsequent Rare Gatherer:** strengthened cold gunmetal plates and star-rune ornament as a **controlled Rare material/ornament identity** on top of the originally approved Rare rivets, gem and seam light. This is a **director refinement specific to this collection**, not permission to copy Hunter claw/fang motifs onto Gatherer.
- Compared the approved candidate with Common Hunter at **125 px** (deterministic Lanczos resampling); the structural/metal/rune differences survive reduction. **Visual gate approved by director**, not a mechanical icon-art production PASS.
- **Production issue:** raw file contains **black matte and no alpha**, not the specified transparent or true flat-lime background. Its file extension `.png` must not be trusted as PNG; retain exact JPEG bytes as the raw source. **Raw mechanical alpha/key gate BLOCKED**, processed lossless WebP absent, dark-composite alpha-edge check NOT_RUN, `artpreflight.py --type ICON` NOT_RUN, game upload/publishing NONE. Resolve background independently without repainting the accepted subject or silently accepting chewed dark edges.

**Next independent generation:** Rare Gatherer's Chest, in a NEW conversation with only the original Skyglass Reliquary and the director-approved Common Gatherer's Chest as individually attached references. The approved Rare Hunter's *tier treatment* is specified in text; it must **not** become a third image reference.
