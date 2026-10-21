# Rare Gatherer's Chest — bronze-bound premium pixel-art isolated generation

**Status:** READY FOR FRESH ISOLATED GENERATION; director visual approval PENDING  
**Lead:** Image Production · **Support:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical operative design:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` §§3–7; `RUL-2026-10-20-002` and `RUL-2026-10-20-006` (new metal/trophy amendment).  
**Supporting studio decision:** `docs/design/ghost_ship_chests/RARITY_MATERIAL_AND_TROPHY_REFINEMENT_20261020.md`  
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Art spec:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → `targets.ICON` / premium `house_style`  
**Target:** Rare Gatherer's Chest · client field `item.image` · `ICON`  
**Final delivery filename after studio processing:** `icon-gs-chest-gatherer-rare.webp`  
**Live-game requests/writes:** 0/0; credentials none; no processing, game upload, publishing or repository binary writes inside isolated generation.

## Exactly TWO individual references — attach ACTUAL approved source bytes

1. **Original Skyglass Reliquary** — `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`, Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`. **MATERIAL + PALETTE ONLY**: low-value dark wood, dark iron, cyan faceted skyglass, cool edge lighting. NOT geometry: no flat lid, no box/clasp layout copying; do not imitate any smooth-paint conflict with the premium pixel-art house style.
2. **Director-approved SHORT-LATCH Common Gatherer's Chest** — source attachment `1000018960.png`, real decoded **JPEG/RGB despite .png extension**, 1536×1536, 283293 bytes, exact SHA-256 `7721f96c04fe1c13475a0d7428b77a64999de70a69a822c5ec379d1faf8a961d`. **APPROVED SAME FAMILY/GATHERER IDENTITY, TNR PIXEL STYLE, EYE-LEVEL 3/4 CAMERA, SCALE, AND FIXED TWO-END-HOOP/SHORT ROPE LATCH GEOMETRY ONLY**. Upgrade the material treatment to Rare, not the underlying object shape. Its black JPEG background does not establish acceptable final alpha.

**Forbidden attachments:** Rare Hunter (including the new bronze design/preview), old rejected armor Rare Hunter, Common Hunter, long-rope Gatherer `1000018939.png`, old duplicated-band chest variants, Sage's Strongbox, multiple-image collages, contact sheets or any third image. **Rare Hunter material colors are described in TEXT ONLY.** Reference #2 must be the approved short-latch Gatherer original, not a re-saved thumbnail. The two references have distinct, limited roles.

## Nonnegotiable closed-chest geometry — IDENTICAL TO COMMON

- One complete **CLOSED DOMED-LID** chest of low-value dark-wood staves, flat eye-level 3/4 camera, same overall shape and scale as approved Common Gatherer; one clear lower wooden front panel.
- **EXACTLY TWO EXISTING OUTER METAL END HOOPS**: ONE on left and ONE on right, SAME width/arching curvature, corner caps, rivet locations and underlying structural silhouette as the Common reference. Each physically joins its corner fixture. **NO extra adjacent band on either side.**
- Rare metal progression is **MATERIAL SUBSTITUTION ONLY**: replace Common's blackened steel surface with clearly **BURNISHED DARK BRONZE** on the SAME hoop and corner metal surfaces. Deliberate warm metal color and restrained bright edges, visibly Rare at 125 px **without adding armored blocks, oversized rivets, attached steel plates, large four-point stars, gold-colored Ornate elements, or new lid shapes**. A tiny surface engraving can be subordinate, but never the focal rarity marker.
- **Exactly ONE central Gatherer's rope**: a distinctly **ROUND SLATE-BLUE WAXED FLAX binding in a NEAT TIGHT HERRINGBONE BRAID**, noticeably cooler/darker and finer than Common's thick honey-tan twisted jute; preserve the same centered ROPE route over the lid and **one COMPACT KNOT ending at the UPPER-FRONT KEEPER just below the lid seam**. Any tail ends SHORT and tucked. **No rope continuing down the lower front to the base**, no second rope arch, no flat leather strap.
- **One small upgraded botanical sprig** tucked beside the upper knot: recognizable **more detailed green foliage**, perhaps three veined/pointed leaves with a slightly serrated outline. Modest increase in leaf detail/shape is allowed, **not** a large plant canopy or extra free-floating object. No Hunter trophy tooth/talon/horn/tusk.
- **ONE SINGLE LEAF BRAND** carved into the unobscured exposed **LOWER FRONT WOOD**, unlit at Rare. Keep it recognizable at 125 px, warm natural wood carving, no glowing leaf (Epic onward).
- **ONE brighter pale-cyan FACETED SKYGLASS CLASP GEM** at the existing upper-front keeper (same physical location/shape of housing as Common, with more careful material finish). **Very faint narrow cyan glow at the closed lid seam only**. No big blue lighting field, magic aura or luminous leaf brand.
- Preserve natural Gatherer identity, concise dark palette and the original chest footprint. This must read as **the same Gatherer's Chest built with bronze metal and finer blue waxed rope**, not a different chest shape.

## Mandatory premium TNR pixel art — not digital painting

Match the Common Gatherer reference's **crisp intentional pixel clusters and stepped lineart, limited dark palette, flat cel-shading with discrete tone ramps and hard shadow shapes**, even and controlled cool edge lighting, single restrained cyan crystal accent. Keep detail purposeful at 125px; not crude blocky 8-bit. **No** smooth photoreal 3D metal, airbrush textures, continuous photographic gradients, painterly blur, uncontrolled antialias halos or neon bloom.

## Positive prompt — one clean isolated icon

`one closed domed-lid RARE GATHERER'S CHEST with EXACTLY the same two arched outer metal bands, front corner blocks and shape as the approved Common Gatherer's Chest, the SAME fixed geometry but existing blackened steel metal replaced by burnished DARK BRONZE, ONE centered round SLATE-BLUE WAXED FLAX ROPE in a tidy herringbone braid wrapping OVER the lid and terminating in ONE COMPACT KNOT at an UPPER-FRONT CLASP immediately below the lid seam (NO rope down the bottom half of the front), one small distinctive veined green three-leaf botanical sprig tucked beside the upper knot, one unlit LEAF BRAND carved into the exposed lower front dark wood, one slightly brighter cyan faceted skyglass gem at the upper keeper, only a subtle THIN cyan seam light, premium high-quality TNR pixel art, crisp stepped pixel lineart and deliberate clean pixel clusters, flat cel-shaded dark palette, defined shadow shapes, restrained even cool edge highlights, eye-level flat 3/4 view, centered single complete chest`

**Background:** genuine native alpha/transparency preferred. If transparency cannot be generated, subject contains **green foliage**, so use TRUE FLAT solid **MAGENTA `#FF00FF`** full-canvas key per art spec foliage exception (not lime, not fake checkerboard). Opaque black JPEG matte NOT production conformant.

**Canonical negatives:** no text, letters, question mark, title, additional logos/symbols, UI/frame/medal, watermark, asset sheet, multiple objects, open lid, spilled items, table/surface, background cast shadow, glow halo/light disc, franchise insignia.

**Rare Gatherer-specific exclusions:** NO Hunter claws, leather or talon; no ivory tooth/fang/horn; no extra metal arch or added hoop; no oversized stepped steel armor plates, no huge angular corners/rivets, no dominant star emblems, no gold (reserved Ornate), no silver (reserved Epic), no iridescent pale starsteel (reserved Legendary), no long rope tail/down-to-base, no glowing leaf brand, no crystal lid cluster, no heavy magical bloom, no smooth digital paint.

## Isolated-session acceptance and return

1. Generate **exactly ONE square original candidate**, never another tier or a collage. Verify source imagery and that the only two attachments are original Reliquary + approved short-latch Common Gatherer.
2. QC in this order: (A) **EXACT Common geometry/two unchanged outer hoop shapes**, (B) round single slate-blue upper-front short-knot braid, (C) unobscured leaf brand/sprig and correct skyglass clasp, (D) **bronze material visibly distinct from blackened steel at 125px**, (E) controlled faint cyan seam and PREMIUM TNR pixel clusters.
3. Show for **director visual approval**. Same subject may be revised in this isolated conversation. After two wrong-subject/composition failures, CLOSE and restart clean.
4. On approval hand back exact ORIGINAL candidate bytes, actual decoded type, dimensions, alpha evidence and raw SHA-256 to persistent Art Studio. Never key/export/preflight, commit image binaries, upload or publish from generation session.
5. Studio performs separate raw/QC, independent 125/64/32px compare, genuine alpha/chroma + spill clamp + transparent square margin, **lossless 256×256 WebP recommended below 460800 bytes**, dark-composite edge check, and canonical `artpreflight.py --type ICON`. Visual approval alone is not preflight PASS.
6. After Rare Gatherer approval, next workstream target is **Epic Hunter**. The original director-approved Rare Hunter PNG `rare_hunter_s_bronze_bound_chest.png` must first be actually supplied and verified before it can serve as the approved same-family Epic Hunter reference. The chat-displayed JPEG preview is NOT byte-equivalent to that reported RGBA source and MUST NOT substitute for it.
