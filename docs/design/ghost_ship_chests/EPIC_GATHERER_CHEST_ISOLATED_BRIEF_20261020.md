# Isolated generation 06 — Ghost Ship Epic Gatherer's Chest

**Status:** READY FOR ISOLATED GENERATION; director visual approval PENDING  
**Lead:** Image Production · **Supporting lens:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical approved art brief:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (sections 2–7), director ruling `RUL-2026-10-20-002`  
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Spec authority:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → `targets.ICON`  
**Client field:** `item.image`; **delivery filename after studio processing:** `icon-gs-chest-gatherer-epic.webp`  
**Live-game requests/writes:** 0/0. No credentials, processing, publishing or repository art commits in isolated generation.

## Target lock

A **single, closed, domed-lid Epic Gatherer's Chest** in the approved Ghost Ship / Skyglass rendering language, eye-level three-quarter view at the same scale/camera as Rare Gatherer. Clear foreground face, dark wood with reinforced dark iron, polished silver trim, one large faceted pale-cyan skyglass crystal clasp, crisp dark outline, soft cool light. Centered complete object, no surface or background scenery.

**Preserve the Gatherer's family identity (first read at 125 px):**
- A **single unmistakable leaf brand carved into the front wooden panel**, now **glowing softly from within its leaf-shaped engraving in pale cyan skyglass light**. The glowing leaf is the Epic Gatherer's distinct front-facing emblem; retain the leaf's veins/outline and do not turn it into an arbitrary angular rune.
- An **obvious coiled brown rope binding** crossing the lid and secured over the front, with a **small botanical green sprig tucked under the rope**. The rope/sprig remain tactile and natural, not a Hunter's leather strap/fang. Silver armor and bright gem must NOT obscure either the sprig or the glowing leaf.
- A center-mounted **larger high-quality skyglass crystal clasp** in a refined substantial silver-trimmed frame, in the same relative position as Rare Gatherer.

**Epic-tier advance beyond the approved Rare Gatherer (structure/material, not only bloom):**
1. **Silver-edged reinforced lid bands**: physically visible polished silver trim framing Rare's stepped/armored cold gunmetal strips and shoulder/corner plates. Distinguish craftsmanship by actual silver edging; retain the near-black/dark-wood core and do not turn the whole box metallic white.
2. **Enlarged faceted pale-cyan crystal**: noticeably bigger central clasp gemstone, more intricate/silver-edged mounting. **Single clasp jewel only**; keep lid clear of Legendary's crystal crown cluster.
3. **Glowing leaf brand**: clearly illuminated *inside its carved front-panel leaf shape*, neither merely a cyan haze nor a floating magic glyph. Readable at 125 px. Keep the sprig green and real.
4. **Focal hierarchy**: silhouette first, glowing botanical brand and central skyglass second, silver trim as prestige reinforcement. Four-point star rune decorations from Rare are permitted as minor accents on steel plates, not substitutes for the leaf motif.

**Tier ceiling:** no extensive silver filigree, no crystal cluster crowning lid, no brightest Legendary treatment; Ornate gold and Mystery chains/lock/mist reserved to their own icons. No cliff of magical bloom, halo, field or external light disc.

## Approved image references — attach EXACTLY TWO, separately

1. **Skyglass Reliquary:** original repository image `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`, Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`. **STYLE / MATERIAL ONLY** (blackened iron, dark wood, pale-cyan crystal, cool highlights, crisp painted silhouette). Its **flat lid and suspended vertical lock composition must not be copied**.
2. **Director-approved Rare Gatherer's Chest:** conversation-returned original `1000018930.png`, true JPEG/RGB 1536×1536 despite the filename, raw SHA-256 `d5e44dba4c5947067ee0da8cef1d7e326a1aafbec7d85c21e6eba76db33a31a4`. **SAME FAMILY/SUBJECT / COMPOSITION / MOTIF / CAMERA / TIER FOUNDATION reference**. Keep rope, tucked sprig and leaf, and advance metalwork/leaf/crystal beyond Rare. Its black matte is **NOT** a valid background reference.

**Do not attach** approved Epic Hunter as a third image, rejected candidates, old pixel icons, a contact sheet or collage. The accepted Epic Hunter's tier treatment is communicated in words, not as a third source image. Actual approved image bytes must be attached individually; a filename/URL alone does not prove ingestion.

## Approved composition and generation language

**Subject line (approved Gatherer's subject, escalated per approved Epic treatment):**

`a closed domed-lid Epic Gatherer's chest of dark wood with refined reinforced blackened iron bands edged in polished silver trim, silver-edged angular riveted corner armor, one larger faceted pale-cyan skyglass crystal clasp in a refined metal housing, coiled natural brown rope binding around the lid with a small green sprig tucked underneath, a single prominent leaf-shaped brand carved into the front panel and glowing softly pale cyan from within`

**Canonical shared style clause, verbatim:**

`game item icon, painted digital illustration with a crisp dark outline, near-black iron and dark wood, one accent of pale cyan faceted skyglass crystal with a soft inner glow, soft cool rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Background clause:** `transparent background` with *genuine native alpha* preferred. The approved workstream fallback says lime `#00FF00`, but the actual Gatherer has **green foliage** (sprig) and the current art skill/spec directs **magenta `#FF00FF` key for foliage**. This is a mechanical source discrepancy to preserve explicitly, not silently blend: if native alpha is unavailable, use a **true solid flat magenta `#FF00FF` chroma background** without gradient/checkerboard/shadow and flag the fallback exception at intake. The studio must adjudicate color-key compliance before treating an export as production-ready; do not presume the workstream's lime suggestion is safe for green leaves. An **opaque black background is not production conformant** (same defect as prior approved raws). Neither fallback is an excuse to alter the accepted art design.

**Canonical shared negative, verbatim:**

`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Additional wrong-subject/tier exclusions:**
- No three claw gouges, fang/bone clasp, animal tooth, or leather strap (all Hunter's).
- No reduction/omission of **leaf**, **rope**, **tucked sprig**; no oversized plate covering them.
- No merely Rare chest with extra cyan seam lines; require **physical polished silver trim**, **noticeably larger clasp gem**, **glowing leaf brand**.
- No Legendary silver filigree all over box, lid crystal cluster, excessive glow; no Ornate aged gold; no Mystery chains, lock and floating mist; no Rusted corrosion.
- No flat-lidded Skyglass Reliquary silhouette; no open lid, extra objects, actor, scenery, sheet or text.

## Isolated-session and delivery gate

1. Generate **exactly ONE square icon candidate**, single complete closed domed chest. Do not generate other icons or any family sheet.
2. Inspect the candidate's actual pixels for Epic vs Rare structural/material differentiation, bright silver trim, enlarged clasp jewel, **recognizably glowing leaf**, and retained Gatherer's rope/sprig. The identity and new tier must survive visually at **125 px**, not depend solely on color bloom.
3. Present **one candidate** for the director's visual approval; same-target revisions can stay in this isolated conversation. After two **wrong-subject/composition** failures, stop, close and restart fresh.
4. On approval return the **original exact source bytes** (not screenshot) with target/filename and approval status to persistent Art Studio. Do **not** crop, process, convert to final WebP, commit, publish or upload in the isolated session.
5. Studio then decodes real MIME/dimensions/alpha, hashes source, checks family at **125/64/32px**, keys genuine flat-color background or keeps native alpha, transparent square-pads, exports lossless `ICON` WebP (256×256 recommended; under 460800 bytes), dark-composite edge QC, and runs canonical `artpreflight.py --type ICON`. Visual approval alone is not production-ready.
6. After approval: separate isolated **Legendary Hunter's Chest** generation, referencing only the Reliquary plus the approved same-family Epic Hunter (not this Gatherer as a third image).
