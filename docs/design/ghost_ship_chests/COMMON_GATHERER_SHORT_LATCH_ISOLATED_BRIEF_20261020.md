# Isolated generation 02 — Common Gatherer's Chest (short-latch premium pixel-art restart)

**Status:** READY FOR CLEAN ISOLATED GENERATION; director visual approval PENDING  
**Lead:** Image Production · **Support:** Art Director  
**Repository:** `perseverance484/tnr-tools`  
**Studio branch:** `chatgpt/ghost-ship-chest-icon-art-studio-20261020`  
**Canonical direction:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` (§§3–7); RUL-2026-10-20-002 and RUL-2026-10-20-006  
**Workflow:** `docs/workflows/ISOLATED_ART_GENERATION.md`  
**Spec:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json` → `targets.ICON` / `house_style`  
**Target:** Common Gatherer's Chest · client field `item.image` · type `ICON`  
**Final delivery filename AFTER studio processing:** `icon-gs-chest-gatherer-common.webp`  
**Live-game requests/writes:** 0/0. Credentials none; no upload, publication or repository art-binary writes.

## Exact two image references (attach actual individual source bytes)

1. **Original Skyglass Reliquary:** `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp` (Git blob SHA `eefd3e22c2fff6255f231b5402697b68f5fd7577`). **Material/palette only**: dark wood, near-black iron, pale-cyan faceted skyglass and cool highlights. **Never copy its flat lid, structural band pattern or rendering when it conflicts with premium pixel art.**
2. **NEW director-approved Common Hunter, correct SHORT UPPER LATCH and pixel art:** conversation source `1000018956.png` (actual JPEG/RGB despite suffix, 1536×1536, 276722 bytes; exact SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`). **Premium pixel clusters, cel-shading, composition, proportions, camera, EXACTLY two outer metal hoops, upper-front binding endpoint and scale ONLY.** Do **not** copy Hunter's flat saddle leather, fang, or three-claw wood brand into Gatherer. Its black JPEG background is NOT a production-alpha reference.

**Do not attach:** the earlier pixel Hunter `1000018935.png` (long leather to base), smooth-painted Hunter `1000018947.png`, six old duplicated-band chests, unapproved long-rope Gatherer `1000018939.png`, Sage's Strongbox, collage/sheet, or any third image. The approved `1000018956.png` is the **only** valid Hunter chest reference for this new generation.

## Composition / physical geometry lock — highest priority

- **One complete CLOSED DOMED-LID chest**, eye-level flat three-quarter view, same framing and physical proportion as approved short-latch Common Hunter. Dark wood staves, plain blackened iron, crisp dark silhouette.
- **EXACTLY TWO independent metal end hoops TOTAL:** **ONE** curved arch near left end of lid and **ONE** near right. Each joins the existing chest corner fittings with physical continuity; **no extra thin/parallel arch** on either end, no double-right band. Rim highlights live on the band itself and are not a third strip.
- **EXACTLY ONE distinct central Gatherer's binding:** **thick rounded HONEY-TAN COARSE THREE-STRAND TWISTED JUTE ROPE**, clearly fibrous and round in section (not a flat Hunter leather strap). It travels over the curved lid, rounds its front lip, and **ENDS IN ONE COMPACT SECURING KNOT at the UPPER-FRONT KEEPER immediately below the lid seam**. Any rope ends are SHORT and tucked beneath this upper knot. **NO vertical rope down the wooden lower front; NO rope continuing to the bottom; NO second rope strap.**
- **ONE small fresh GREEN SPRIG** (roughly 2–3 clean leaves) tucked neatly under the knot near the lid/front junction; not a large floating plant and not a second separate object.
- **ONE readable single LEAF BRAND** burned/carved into the **exposed lower front wood panel**, with vein silhouette; warm unlit wood at Common, **not** a glowing Epic emblem. The lower panel must be unobstructed by the rope.
- **ONE small pale-cyan FACETED SKYGLASS GEM** in a compact plain dark-metal upper latch near the jute knot, crystal bright within its facets but **no external aura, seam glow or radiant leaf**.
- Do not depict any Hunter triple-claw marks, leather, bone fang, or claw motif. The Gatherer must read unmistakably distinct from the approved Hunter at **125px** through leaf + round jute + green sprig.

## Locked premium TNR pixel-art rendering

Match approved short-latch Hunter **`1000018956.png`** precisely in:
**crisp stepped pixel lineart, coherent intentional square pixel clusters, controlled limited dark palette, flat cel-shading with sharply defined tone ramps, subtle cool edge light, and small faceted cyan crystal highlights**. Refined high-quality game pixel art, not crude 8-bit; **no** smooth digital painting, glossy photoreal/3-D rendering, airbrush gradients, blur, cinematic bloom, or soft pasted-on brush textures.

**Concise subject + style clause for the generator:**

`one closed domed-lid Common Gatherer's Chest made from dark wood with exactly one continuous blackened-iron curved end band on each side (TWO total), one centered thick round honey-tan three-strand twisted JUTE ROPE traveling over the lid and terminating in ONE COMPACT KNOT at the UPPER-FRONT LATCH just below the lid seam (NO rope down the front panel), a small tucked fresh green leafy sprig next to the knot, one single carved non-glowing leaf brand clearly visible on the exposed lower front wood panel, one compact faceted pale-cyan skyglass crystal lock, premium high-quality TNR pixel art, crisp stepped pixel outlines, clean deliberate pixel clusters, limited dark palette, flat cel shading, soft even cool highlights, strong readable silhouette, eye-level flat 3/4 view, centered single complete object`

**Background:** Genuine native transparency if available. If native alpha is unsupported, use a **TRUE SOLID FLAT MAGENTA `#FF00FF`** background for foliage (spec exception to workstream default lime), with no gradients/shadows/checkerboard. **Opaque black backgrounds are not mechanically compliant with item ICON preflight.** Reference B's opaque JPEG is strictly a visual-style reference, not a valid background.

**Canonical negatives:** no text, letters, question mark, additional symbols, labels, UI, frame, medal, watermark, asset sheet, multiple objects, open lid, spilled loot, table, ground, cast-background shadow, glow halo or disc, franchise insignia.

**Specific negatives:** no long rope down front or reaching bottom, double rope, secondary binding, loose hanging rope tails, second curved metal band adjacent to either outer hoop, Hunter claws/fang/leather, silver Epic trim, Rare reinforced armor/star runes, Legendary filigree/crystal group, glowing leaf, painted/smoothed texture.

## Isolated generation, director acceptance and studio return

1. Open **ONE NEW isolated generation conversation** for exactly one Common Gatherer's Chest image. Attach only the two eligible original individual references above.
2. Inspect actual source pixels in order: **two end hoops/no duplicates → short rope knot at upper front/exposed lower wood → leaf/sprig/crystal → premium pixel clustering**. Compare with approved short-latch Hunter at **125px** for scale and unmistakable family difference.
3. Present ONE candidate for **director visual approval**. Same-target revisions may remain here; after TWO wrong-subject/composition results close and restart clean. No other chest/tier image is authorized.
4. On approval return exact raw source bytes, actual decoder format, dimensions, SHA-256 and target to persistent Art Studio. The studio alone handles native alpha / safe chroma processing, transparent square padding, lossless WebP (256×256 recommended, <460800 bytes), dark-composite edge QC, 125/64/32px tests and `artpreflight.py --type ICON`. **No preflight result or game upload is implied by director visual approval.**
5. Next slot only after this approved Gatherer: Rare Hunter (new clean isolated generation with original Reliquary plus the **approved short-latch Common Hunter**, never the unapproved Gatherer as a third reference). Tier ornaments sit **on existing two end hoops**; center leather/fang changes to approved Rare material/motif.
