# Art request: Ghost Ship chest icons (12)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-20)
- **Status:** APPROVED direction (RUL-2026-10-20-002), **amended 2026-10-20** after director geometry-reset and five-tier family-binding decisions (RUL-2026-10-20-006). The original six candidate visuals were subsequently **REVOKED for duplicated lid bands**: **3/12 director VISUAL approvals**: Common Hunter `1000018956.png`, Common Gatherer `1000018960.png`, and the new Rare Hunter bronze/talon artwork approved 2026-10-20. **Rare Hunter's claimed RGBA PNG ORIGINAL has not been byte-verified**: the chat-attached image is a different JPEG preview; see `docs/design/ghost_ship_chests/RARE_HUNTER_BRONZE_APPROVAL_AND_INTAKE_20261020.md`. **0/12 production-ready/preflight-valid exports**. The premium pixel-art register, two-end-hoop geometry, Hunter motif, and **short upper-front binding** are now **locked by the director-approved updated Common Hunter `1000018956.png`** (actual JPEG/RGB 1536×1536; raw SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`). The earlier long-leather `1000018935.png` remains style precedent only, NOT the current geometry reference. Earlier Gatherer candidate `1000018939.png` was unapproved (overlong rope) and is **NOT** a generation reference; director-approved short-latch replacement Gatherer `1000018960.png` has a compact knot and correct exposed leaf-brand front. This brief is the operative art-direction owner; its original approval history remains intact.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec authority: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ICON`.
- **Live-game requests/writes:** 0. Nothing here uploads anything.

## 1. Why

Ten of these chests are the rewards of the Ghost Ship (Hunt) and Ghost Ship (Gather) quests: each
quest gives its own Common, Rare, Epic and Legendary tier plus Ornate and Mystery. The Rusted pair is
not a quest reward, but uses the same old icons and is included so the set stays consistent. The
quests got the Ghost Ship / Skyglass art update (`art/ghost_ship_skyglass/`); the chests did not, and
still use the older pixel-art icons. Two further problems:

- **Hunter's and Gatherer's chests are indistinguishable.** At every tier the two share the exact same
  image file, so a player cannot tell them apart in the inventory, although one holds creature
  materials and the other herbs and ores.
- **Mystery Chest** carries a painted red question mark, and **Ornate Chest** is drawn open with
  treasure spilling out. Both break the icon rules (no symbols or text, no open lids or spilled
  contents).

The Mystery Chest can also roll the **Skyglass Reliquary**, which is already in the new style. The new
chests must read as the same family as the Reliquary without looking like it.

## 2. Targets

| # | Item | Holds | Delivery filename |
|---|---|---|---|
| 1 | Common Hunter's Chest | Common hunting materials | `icon-gs-chest-hunter-common.webp` |
| 2 | Common Gatherer's Chest | Common gathering materials | `icon-gs-chest-gatherer-common.webp` |
| 3 | Rare Hunter's Chest | Rare hunting materials | `icon-gs-chest-hunter-rare.webp` |
| 4 | Rare Gatherer's Chest | Rare gathering materials | `icon-gs-chest-gatherer-rare.webp` |
| 5 | Epic Hunter's Chest | Epic hunting materials | `icon-gs-chest-hunter-epic.webp` |
| 6 | Epic Gatherer's Chest | Epic gathering materials | `icon-gs-chest-gatherer-epic.webp` |
| 7 | Legendary Hunter's Chest | Legendary hunting materials | `icon-gs-chest-hunter-legendary.webp` |
| 8 | Legendary Gatherer's Chest | Legendary gathering materials | `icon-gs-chest-gatherer-legendary.webp` |
| 9 | Rusted Hunter's Chest | Furs, pelts, shells, antlers; small chance of Rare Jewels | `icon-gs-chest-hunter-rusted.webp` |
| 10 | Rusted Gatherer's Chest | Herbs, ores, Mosswolf Tuft; small chance of Rare Jewels | `icon-gs-chest-gatherer-rusted.webp` |
| 11 | Ornate Chest | Imperial Gold, Unobtanium, Rare Jewels, Lion Token | `icon-gs-chest-ornate.webp` |
| 12 | Mystery Chest | The Common to Legendary Hunter's and Gatherer's chests, Ornate, Mystery itself and the Skyglass Reliquary (not the Rusted pair) | `icon-gs-chest-mystery.webp` |

Ids and current icon URLs are in the 2026-10-20 public read and are added by script when the release
manifest is built; they are not needed to draw.

## 3. Style lock (from the approved Ghost Ship set)

Taken from the director-approved icons in `art/ghost_ship_skyglass/` (crown, crystal, filament,
katana, reliquary, serum):

- near-black dark wood and **two existing fixed-shape metal end bands with unchanged corner reinforcement geometry**; their metal material/finish varies by named tier (pitted iron / blackened steel / burnished dark bronze / polished silver / pale iridescent starsteel), while the underlying outline remains unchanged;
- **one accent: pale cyan skyglass crystal**, faceted, with a soft inner glow;
- tiny engraved four-point star rune motifs MAY appear sparingly on the existing metal surface when suitable, **never as large added armor plates or the principal rarity signal**;
- **premium high-quality pixel art** with **crisp pixel lineart, flat cel shading, limited palette, deliberately shaped pixel clusters**, defined tonal ramps and **restrained painterly depth**; no smooth digital-paint blending, airbrush gradients, glossy photoreal texturing, blurry antialiasing or bloom;
- soft even lighting and a restrained cool edge accent (no hard cast shadow or broad rim-light halo);
- 3/4 view at eye level, the same camera as the Reliquary; transparent background.

**References per session (pass the actual image bytes, individually, never a collage):**
1. `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`: **style/material only**.
2. **NEXT icon 4 (Rare Gatherer):** attach original Reliquary (MATERIAL/PALETTE ONLY) + new approved short-latch **Common Gatherer `1000018960.png`** (Gatherer identity, pixel style, camera, fixed geometry). The new bronze-bound Rare Hunter design is conveyed in **text only, never as a third image reference**. For subsequent Hunter/Gatherer icons use Reliquary plus one approved same-family geometry-correct predecessor; never attach a rejected old icon or collage. Rare Hunter's actual original PNG is not yet intake-verified and must NOT be silently treated as an eligible byte-verified reference.

Do not pass the old pre-Ghost-Ship pixel-art chest icons (wrong family register), any of the six geometry-revoked images, or the smooth-painted Common Hunter candidate. Their rejection does **not** permit smooth painterly rendering: the **pixel art quality/style requirement above is binding**.

## 4. Director-approved chest geometry and rarity materials (amended 2026-10-20)

**Silhouette.** A classic closed domed-lid chest, distinct from the Reliquary's flat lid. **Director-locked construction (2026-10-20 geometry reset and follow-up): exactly ONE continuous metal reinforcement hoop near the outer left end of the lid and ONE near the outer right end, plus ONE separate centered family binding (Hunter flat hide/leather strap or Gatherer round fiber/silk rope) that CROSSES ONLY THE LID AND ENDS AT A SECURED FRONT-EDGE KEEPER JUST BELOW THE UPPER LID SEAM. The leather/rope MUST NOT run down the full front face or reach the bottom.** No extra parallel hoop beside the left or right hoop (the observed defect that invalidated six prior raws). All rarities **retain the EXACT Common chest shape**: two outer lid hoops with the same widths, bends, rivet/corner fixture layout and overall body silhouette. Only MATERIAL/FINISH/DELICATE SURFACE DETAILS change on existing metal; no oversized armor plates, layered structural reinforcements or enlarged corner blocks. No third/fourth hoop or parallel strip. Binding edge-stitching and rope knots must not masquerade as additional hoops. Verify physical band continuity in the original pixels before style/tier acceptance. See `docs/design/ghost_ship_chests/GEOMETRY_RESTART_20261020.md` for provenance and the invalidated image ledger.

**Family motif** (must read at 125 px):

| Family | Brand on the front panel, in skyglass light | Wrap |
|---|---|---|
| Hunter's | three parallel claw gouges | a SINGLE flat leather/hide strap, short upper-front clasp, and exactly ONE tier-specific trophy (bone/fang/talon/horn/tusk; see §4b) |
| Gatherer's | a single leaf | a coiled rope binding, a small sprig tucked under it |

**Approved metal material ladder — material substitution, NOT structural redesign.** Exactly the same two end-band shapes, corner fittings, body, closure geometry, camera and size at every named tier. Rarity should read through the finish/material of EXISTING metal, the single family binding, one trophy or small botanical sprig, and the crystal/controlled light:

| Named tier | Material of the same two outer metal bands and corner fittings | Crystal / light / fine ornament |
|---|---|---|
| Rusted | **Corroded, pitted iron** | Flaking/worn SURFACE, cracked dull crystal, no glow. Keep solid chest geometry. |
| Common | **Blackened steel** | Plain finish, one small cyan clasp, no seam/brand glow. |
| Rare | **Burnished DARK BRONZE** | Brighter cyan clasp and narrow faint closed-lid cyan seam light; minimal engravings, NO large star emblems/added armor. |
| Epic | **Polished SILVER** | Refinement of existing bands, larger faceted crystal, family front brand glowing; no new hoops. |
| Legendary | **Iridescent PALE STARSTEEL** | Finest fine-line detail/filigree IN existing metal, brightest controlled skyglass, small previously approved lid crystal cluster as a nonstructural mounted ornament; no altered lid/corner assembly. |

**Aged gold is reserved for Ornate Chest**, NOT Rare bronze. The previous Rare design with extra riveted angular cold-gunmetal armor blocks and oversized star ornamentation is REJECTED and superseded by the director-approved bronze material treatment. Details: `docs/design/ghost_ship_chests/RARITY_MATERIAL_AND_TROPHY_REFINEMENT_20261020.md`.

### 4a. Director-approved central binding materials (2026-10-20 amendment)

**Only ONE centered family binding per chest.** Hunter always uses a **single broad FLAT hide/leather strap ending at the compact upper keeper with ONE matching tier-specific monster trophy (bone, fang, talon, horn or tusk from §4b)**; Gatherer always uses **a single ROUND twisted/braided rope with a tucked botanical sprig**. These materials are visual/texture descriptors, **not new item or loot-material records**. At 125px, keep the binding's different **base tone, width, and fiber/finish** readable; tiny threads may simplify. No binding is an extra metal hoop.

| Named tier | Hunter center strap, one flat hide/leather binding | Gatherer center rope, one round fiber/silk binding |
|---|---|---|
| **Rusted** | **Cracked ash-brown rawhide**, peeling/frayed edges, dull worn fang attachment. | **Rotting gray hemp**, rough fuzzy/unraveling fibers, one withered tucked sprig. |
| **Common** | **Smooth saddle-brown tanned leather**, broad plain flat hide, no silver stitching, simple bone/fang clasp. | **Honey-tan coarse three-strand twisted jute**, visibly rounded cord and simple knot, small fresh tucked green sprig. |
| **Rare** | **Smoky charcoal-brown pebbled salt-cured hide**, a few subtle tidy dark-steel eyelets/stitches integrated in the same flat strap. | **Slate-blue waxed flax** in a tighter herringbone braid, neat bound knot, tucked green sprig. |
| **Epic** | **Glossy near-black polished leather**, visible **silver saddle-stitching WITHIN the same strap's edges** and recognizable fang clasp. | **Pale silver-gray braided sea-silk**, subtle silver threads woven within the one continuous rope, green sprig retained. |
| **Legendary** | **Midnight-blue scale-embossed fine leather**, refined silver embroidery and *fine* integrated cyan skyglass thread, refined fang clasp. | **Storm-indigo braided silk** with fine silver strands and restrained cyan skyglass filaments integrated within the same cord; ornate knot and tucked green sprig. |

**Structural prohibition:** neither silver stitching nor flax braid forms an extra parallel arched band. Rusted fraying and Legendary thread are surface treatments of the **same central binding**. The Rare/Epic/Legendary metal appearance is a MATERIAL REPLACEMENT on the SAME two original-shaped hoops and unchanged corner geometry. Only subtle surface ornament/edge highlights are permitted: **NO tier may add bulky plates, another metal band or new corner armor shape**. Ornate and Mystery retain their separately approved special designs and are **not** automatically assigned Hunter leather or Gatherer rope.

**Source/provenance:** director-approved proposal recorded in `docs/design/ghost_ship_chests/CHEST_BINDING_MATERIAL_LADDER_PROPOSAL_20261020.md` and the geometry reset record. The operative art-direction rule is **this brief**, not its proposal.

### 4b. Director-approved upper-latch termination and motif evolution (2026-10-20)

**Binding termination is a hard physical rule for all ten Hunter/Gatherer variants:** the single center strap or rope runs over the closed domed lid, turns over the **front lip**, and **terminates at a compact keeper/lock on the upper front directly below the lid seam**. On Hunter, the short end is fastened by **ONE tier-specific monster trophy accessory** (bone/fang/talon/horn/tusk per the locked table below) integrated with the front skyglass lock. On Gatherer, a **single compact knot** secures the jute/flax/silk rope at the same upper-front receiver, with only very short tucked ends. **No leather or rope continuing down the bottom half of the front panel or the base of the chest**. This makes the clasp's lid-retaining function clear and leaves the clan/family brand on the lower front wood unobscured. Do not confuse the binding with the two structurally continuous OUTER METAL end hoops, which may still run down the corners.

**Director-locked rarity trophy progression:** exactly ONE prominent Hunter trophy at the upper latch, **different by tier**, alongside the corresponding approved leather material (§4a). This replaces the old fixed-ivory-fang / larger-ivory-fang path. Hunter still has exactly three front-panel claw gouges. These are **visual descriptors only** (not new named monsters/materials, recipes or loot). Gatherer's small tucked botanical accessory remains flexible in exact leaf structure and finish, while its one carved leaf emblem stays constant; shape suggestions for leaves are NOT anatomy locks.

| Named tier | Hunter: EXACTLY ONE trophy accessory (director approved) | Gatherer: compact tucked sprig / leaf design latitude |
|---|---|---|
| Rusted | **Short chipped weathered bone**. | Sparse wilted, curled brown-green leaves. |
| Common | **Small ivory monster fang**. | Simple fresh green leaves, clean pointed shapes. |
| Rare | **Distinct sharply hooked MONSTER TALON** (NOT just another ivory fang), modestly mounted at upper bronze clasp. | More distinctive veins/leaf serrations, compact fresh sprig; keep one leaf front brand UNLIT. |
| Epic | **Ridged, curved MONSTER HORN** on refined silver keeper. | Rich emerald shaped leaves, restrained silver vein/edge accents, still a compact sprig. |
| Legendary | **Elaborate fossilized TUSK with restrained skyglass inlays** on starsteel keeper. | Compact dark-jade branching detail, delicate silver/cyan vein accents, not a large canopy. |

Exactly ONE Hunter trophy object, never a tooth row or multiple accessories. The Gatherer botanical sprig must not hide the front leaf brand, crystal or shape of the chest. Both families keep the shortened binding terminating at the upper receiver.

**Visual QC:** at 125px, verify **unchanged Common chest geometry**, TWO outer bands with no doubled right side/oversized plate, one short upper-front binding/keeper, the proper tier metal COLOR/FINISH and single Hunter TROPHY or Gatherer botanical accessory. Family front emblem, crystal and restrained tier illumination remain readable. Trophy changes ADD to the approved §4a leather/rope ladder, without changing physical construction.

**Source:** initial upper-latch/fang-and-leaf direction was approved 2026-10-20; the later explicit **metal material and specific Hunter accessory ladder** approval narrows that earlier optional progression. `docs/design/ghost_ship_chests/FRONT_LATCH_AND_MOTIF_REFINEMENT_20261020.md` retains the earlier decision; `docs/design/ghost_ship_chests/RARITY_MATERIAL_AND_TROPHY_REFINEMENT_20261020.md` records the more recent specific director lock. No game changes.

**Ornate Chest.** The grandest chest in the set, closed: heavy silver filigree and several inset
skyglass gems. Proposal: allow **aged gold** as a second accent, because its loot is Imperial Gold;
otherwise it stays skyglass-only.

**Mystery Chest.** Closed and sealed: crossed chains and a heavy lock, with skyglass mist curling from
the lid seam. **No question mark**, since symbols and lettering are out. If the director wants a
"?" kept, that is an explicit exception.

## 5. Spec values (`targets.ICON`)

| Field | Value |
|---|---|
| aspect | 1:1, tolerance 2% (the game stretches icons; non-square distorts) |
| recommended source | 256x256 (minimum 160 px wide) |
| delivered / displayed width | 125 px / 160 px |
| format | WebP, lossless |
| byte ceiling | 460,800 bytes |
| padding | transparent margin so the rarity frame behind the icon still reads |
| background | native transparency strongly preferred. Default flat lime `#00FF00` key; when the image includes a Gatherer green sprig, the spec's foliage-safe alternative is flat magenta `#FF00FF` (record this exception at intake). Opaque black is not accepted as a key. |

## 6. Prompts

**Shared pixel-rendering style clause (director locked by new Common Hunter):**
`premium high-quality TNR pixel-art game item icon, crisp pixel lineart and intentional clean pixel clusters, flat cel shading with restrained painterly depth, limited controlled dark palette and defined hard-edged shadow shapes, near-black iron and dark wood, one restrained pale-cyan faceted skyglass crystal accent with internal facet light, soft even cool edge lighting, eye-level flat 3/4 view, no foreshortening, single complete centered object with a strong readable silhouette, genuine transparent background`

**Shared negative:**
`no text, no letters, no question mark, no symbols other than the brand described, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open lid, no contents spilling out, no loose items around it, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Subject lines** (one per session; append the style clause, then the background clause). For the ten family-tier targets, explicitly apply the **one-central-binding materials** in section 4a. Geometry is fixed at exactly **one left and one right outer metal hoop**, never a duplicate.

| # | Subject |
|---|---|
| 1 | a closed domed-lid chest of dark wood with exactly one plain blackened iron lid hoop at each outer end (two total), no extra parallel arch, ONE centered broad flat smooth saddle-brown tanned leather strap crossing the lid and **TERMINATING at the upper-front keeper beneath the lid seam**, secured by one simple bone fang clasp and small pale-cyan skyglass gem, three parallel claw gouges branded on the exposed lower front wood (NO leather to base) |
| 2 | a closed domed-lid chest of dark wood with exactly one plain blackened iron lid hoop at each outer end (two total), no extra parallel arch, ONE centered thick round three-strand honey-tan jute rope traveling over the lid and **ENDING in one compact upper-front securing knot directly below the lid seam**, short tucked rope ends, a small green sprig tucked beside the knot, one small pale-cyan skyglass clasp, and one non-glowing leaf brand clearly carved on the exposed wooden lower front (NO rope to base) |
| 3-8 | as the exact SAME Common-shaped Hunter/Gatherer subject with Rare/Epic/Legendary **metal replacement** from §4, corresponding single leather/rope from §4a and exactly ONE Hunter trophy or small Gatherer sprig from §4b; unchanged two hoop shapes/corners/short upper latch, no extra armor |
| 9-10 | as the exact SAME Common-shaped Hunter/Gatherer subject with Rusted **pitted iron** from §4 and matching Rusted center binding/trophy/sprig from §§4a–4b, unchanged hoops/corners/short upper latch |
| 11 | a closed, grand domed-lid treasure chest with heavy silver filigree and several inset skyglass gems, aged gold trim |
| 12 | a closed domed-lid chest bound by crossed iron chains and a heavy lock, faint skyglass mist curling from the lid seam |

**Background clause:** `transparent background` where the generator supports it; otherwise
`on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`.

**Foliage exception:** Gatherer sprigs contain green leaves. When genuinely native alpha is unavailable, the canonical art spec's foliage-safe **flat magenta `#FF00FF`** key takes precedence over lime; declare this explicitly for that isolated generation and record the deviation at intake. A black JPEG background is **not** a native-alpha source or flat key.

## 7. Process

1. **Common Hunter (icon 1): DIRECTOR VISUALLY APPROVED, now conforming to premium pixel art + short upper latch (2026-10-20).** Director replied “Yes, next” after seeing short-latch pixel source `1000018956.png` (actual JPEG/RGB 1536×1536, 276722 bytes, exact SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`). It has one metal hoop per outer lid end, one smooth saddle-brown flat leather over the lid **ending at the upper-front fang/skyglass clasp**, exposed lower wood with exactly three claw gouges and premium crisp pixel clusters. **Rejected/reference-ineligible history:** first six double-band raws, smooth-painted `1000018934.png` and `1000018947.png`; long-leather pixel source `1000018935.png` remains a former style exemplar but NOT correct geometry. **This approval is visual only:** the new source is JPEG with black opaque matte, so alpha/key processing, lossless WebP, dark-composite QC, `artpreflight.py --type ICON` and uploads are all NOT_RUN.
2. **Common Gatherer (icon 2): DIRECTOR VISUALLY APPROVED, geometry and premium pixel style now locked for BOTH families (2026-10-20).** Director said “Approved, next” for corrected `1000018960.png`, true JPEG/RGB 1536×1536, 283293 bytes, SHA-256 `7721f96c04fe1c13475a0d7428b77a64999de70a69a822c5ec379d1faf8a961d`. It has exactly two outer metal hoops and a single round honey-tan three-strand JUTE rope ending in a compact upper-front securing knot with short tucked ends, green sprig, one unlit leaf wood brand and small cyan clasp. Full-size visual and **125px side-by-side** vs approved Common Hunter confirmed distinct family brands/bindings at matching 3/4 scale and consistent premium pixel clusters; 64/32px stress views checked. The old long-rope `1000018939.png` remains UNAPPROVED and prohibited as reference. JPEG/black source is not production ready: alpha/key, WebP export, dark-composite edge checks and artpreflight NOT_RUN.
3. **Rare Hunter (icon 3) — DIRECTOR VISUAL APPROVAL for the NEW burnished-bronze/talon direction (2026-10-20).** The director expressly approved `rare_hunter_s_bronze_bound_chest.png`, described as a PNG/RGBA 1254×1254, 1,349,268 bytes, SHA-256 `99ca6f817fe390b0c9aff16cdc2016f70d897f44dbda2e06b511696a5da94f08` (**ORIGINAL BYTES NOT YET VERIFIED IN THIS STUDIO**). The attached `1000018962.png` is actually an opaque JPEG/RGB 1536×1536, 301659 bytes, SHA-256 `6c7c4d879f9261c6cd3b03c8a461053363b13293f42a1ba8aefd0de221babfd6`, a NONIDENTICAL PREVIEW. **Do not claim source-intake PASS or production-ready.** Visual approval: same Common geometry, burnished dark-bronze hoops and corner fittings, single charcoal pebbled-leather strap ending upper front, ONE sharp hooked talon, brighter cyan crystal, faint lid-seam light and THREE unlit claw marks, premium pixel art. Old cold-gunmetal oversized-armor / star-icon candidate REJECTED. See `RARE_HUNTER_BRONZE_APPROVAL_AND_INTAKE_20261020.md` for source discrepancy and gate evidence.
4. **NEXT: Rare Gatherer (icon 4)** — one NEW isolated generation session attaching **exactly TWO original images**: (A) original Skyglass Reliquary (materials/palette ONLY) and (B) newly approved short-latch Common Gatherer `1000018960.png` (pixel rendering, identical fixed geometry, camera and Gatherer family ONLY). Bronze metal/richer sprig/slate-blue flax/bright gem/faint seam direction comes from this brief in TEXT ONLY; **do not attach the Rare Hunter as a third image**. See `docs/design/ghost_ship_chests/RARE_GATHERER_BRONZE_SHORT_LATCH_ISOLATED_BRIEF_20261020.md`. Then Epic, Legendary and Rusted pairs, Ornate/Mystery separately. For all family generations, maintain exactly two images max and geometry-first QC; special Ornate/Mystery references remain director owned.
5. Two wrong-subject results in one session: close it and start clean (protocol section 3).
6. **Raw QC before processing:** square, one complete closed chest, **exactly two outer metal end hoops + one centered family binding that ends at the UPPER FRONT LATCH rather than the lower panel, with no duplicate side band**, tier-appropriate center material from section 4a, **premium crisp pixel linework/flat cel tonal clusters/limited palette (reject smooth painterly look)**, no text or extra symbols, no halo or glow disc, not sitting on a surface, background truly flat and keyable or genuinely transparent. JPEG on opaque black is NOT production-ready even when director visually approves the pixel art.
7. **Processing at intake:** key or keep native alpha, clamp spill, pad to square, lossless WebP,
   check edges on a dark composite, then `artpreflight.py --type ICON`.

## 8. Delivery and next step

- Return each approved original to the studio with its filename exactly as in section 2. A
  correction gets a fresh name (`_b`, `_c`).
- Include a ledger row per file: filename, type `ICON`, pixel size, bytes.
- After intake and preflight, the twelve icons go to the review desk as one Forge suggest-mode
  ticket (category VISUAL, title "Update icon", one rationale per chest).

## 9. Director decisions

Original family/tier/special designs were approved 2026-10-20 (items 1–4). **Same-day amendment**: director confirmed two end hoops/no duplicate side band and approved the five-level center binding material ladder in section 4a. Six historical duplicated-band images remain revoked. Two Common originals have exact verified source hashes and approved pixel-art short-latch visuals; Rare Hunter's NEW bronze/talon design is DIRECTOR VISUALLY APPROVED (3/12) but its claimed RGBA ORIGINAL has not been received for byte verification. Rare Gatherer is next. Actual item rarity remains a separate director decision (now decision item 9).

1. Family motifs: three front claw gouges + one flat leather strap + ONE tier-specific trophy (bone/fang/talon/horn/tusk) for Hunter; carved leaf + one round rope + compact tucked sprig for Gatherer.
2. Director-approved tier-specific METAL MATERIAL ladder in §4 (Rusted pitted iron, Common blackened steel, Rare burnished dark bronze, Epic polished silver, Legendary iridescent pale starsteel), preserving identical Common hoop and corner geometry; supersedes the previous structural-armor emphasis.
3. Aged gold as a second accent on the Ornate Chest.
4. Mystery Chest without a question mark.
5. **Amendment approved 2026-10-20 (RUL-2026-10-20-006):** one arched metal lid hoop per outer end plus ONE centered family binding, no duplicate parallel bands; the Rusted/Common/Rare/Epic/Legendary flat leather vs round rope material ladder in section 4a. These decisions invalidate the six historical chest image approvals, not the art-direction motifs.
6. **Upper-front binding termination and upgraded Hunter accessory ladder (2026-10-20):** the single center leather/rope terminates at the short upper-front latch, never to the base. One Hunter trophy changes by tier: chipped bone / ivory fang / hooked talon / ridged horn / fossilized tusk with subtle skyglass; Gatherer sprig evolves in shape/detail without changing its carved leaf emblem. §4b owns the operative table. The director approves final pixels per icon.
7. **Premium pixel-art rendering is mandatory (2026-10-20):** conform to `25x_DATA_art_spec.json` (`house_style`, ICON scaffold). The director rejected smooth-painted candidates, accepted long-strap pixel-style exemplar `1000018935.png` for style only, then explicitly **approved final short-latch pixel Common Hunter `1000018956.png`**. Its pixels lock the family rendering standard and corrected upper-latch geometry; the raw is still opaque JPEG and alpha/export/preflight remain pending.
8. **New Rare Hunter visual approved + next target (2026-10-20):** new burnished-bronze, charcoal-hide, hooked-talon Rare Hunter preserves Common geometry and premium pixel style. Director approved art, NOT raw intake (original PNG hash unverified). Reject prior oversized gunmetal/large-star Rare design. Next Rare Gatherer uses Reliquary + approved Common Gatherer only, with Rare bronze finish described in text.
9. Separate, not part of this request: all twelve chests are rarity COMMON, including the
   "Legendary" ones. Rarity is a director call.
