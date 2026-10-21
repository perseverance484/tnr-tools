# Art request: Ghost Ship chest icons (12)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-20)
- **Status:** APPROVED direction (RUL-2026-10-20-002), **amended 2026-10-20** after director geometry-reset and five-tier family-binding decisions (RUL-2026-10-20-006). The original six candidate visuals were subsequently **REVOKED for duplicated lid bands**: **2/12 currently conforming director visual approvals**: short-latch premium-pixel Common Hunter `1000018956.png` and Common Gatherer `1000018960.png` accepted 2026-10-20; 0/12 finished/preflight-valid exports. The premium pixel-art register, two-end-hoop geometry, Hunter motif, and **short upper-front binding** are now **locked by the director-approved updated Common Hunter `1000018956.png`** (actual JPEG/RGB 1536×1536; raw SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`). The earlier long-leather `1000018935.png` remains style precedent only, NOT the current geometry reference. Earlier Gatherer candidate `1000018939.png` was unapproved (overlong rope) and is **NOT** a generation reference; director-approved short-latch replacement Gatherer `1000018960.png` has a compact knot and correct exposed leaf-brand front. This brief is the operative art-direction owner; its original approval history remains intact.
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

- near-black iron and dark wood, low overall value; blackened iron banding with rivets;
- **one accent: pale cyan skyglass crystal**, faceted, with a soft inner glow;
- engraved four-point star rune motif on metal (sparingly);
- **premium high-quality pixel art** with **crisp pixel lineart, flat cel shading, limited palette, deliberately shaped pixel clusters**, defined tonal ramps and **restrained painterly depth**; no smooth digital-paint blending, airbrush gradients, glossy photoreal texturing, blurry antialiasing or bloom;
- soft even lighting and a restrained cool edge accent (no hard cast shadow or broad rim-light halo);
- 3/4 view at eye level, the same camera as the Reliquary; transparent background.

**References per session (pass the actual image bytes, individually, never a collage):**
1. `art/ghost_ship_skyglass/icon_ghost_ship_skyglass_reliquary.webp`: **style/material only**.
2. **For icon 3 (Rare Hunter):** the new approved short-latch Common Hunter **`1000018956.png`** is the **same-family Hunter motif, pixel-rendering, camera, geometry and scale reference**; original Reliquary is material/palette only. The newly approved Common Gatherer **`1000018960.png`** is **NOT** a third image reference. **From icon 4 onward**, use Reliquary + one NEW director-approved geometry-and-pixel-correct predecessor **of the target's exact Hunter/Gatherer family**, never an unapproved/revoked old icon, and never a third reference. The accepted Common Gatherer establishes the Gatherer motif and can be used as the same-family second image for future Gatherer tiers.

Do not pass the old pre-Ghost-Ship pixel-art chest icons (wrong family register), any of the six geometry-revoked images, or the smooth-painted Common Hunter candidate. Their rejection does **not** permit smooth painterly rendering: the **pixel art quality/style requirement above is binding**.

## 4. Design proposal (director to approve)

**Silhouette.** A classic closed domed-lid chest, distinct from the Reliquary's flat lid. **Director-locked construction (2026-10-20 geometry reset and follow-up): exactly ONE continuous metal reinforcement hoop near the outer left end of the lid and ONE near the outer right end, plus ONE separate centered family binding (Hunter flat hide/leather strap or Gatherer round fiber/silk rope) that CROSSES ONLY THE LID AND ENDS AT A SECURED FRONT-EDGE KEEPER JUST BELOW THE UPPER LID SEAM. The leather/rope MUST NOT run down the full front face or reach the bottom.** No extra parallel hoop beside the left or right hoop (the observed defect that invalidated six prior raws). Any Rare/Epic/Legendary layered plating, silver trim or filigree must be **on the surfaces of the existing TWO hoops**, never a third/fourth hoop or duplicate independent curved strip. Binding edge-stitching and rope knots must not masquerade as additional hoops. Verify physical band continuity in the original pixels before style/tier acceptance. See `docs/design/ghost_ship_chests/GEOMETRY_RESTART_20261020.md` for provenance and the invalidated image ledger.

**Family motif** (must read at 125 px):

| Family | Brand on the front panel, in skyglass light | Wrap |
|---|---|---|
| Hunter's | three parallel claw gouges | a leather strap with a bone or fang clasp |
| Gatherer's | a single leaf | a coiled rope binding, a small sprig tucked under it |

**Tier ladder** (same camera and size at every tier; escalation by material, ornament and crystal):

| Tier | Treatment |
|---|---|
| Rusted | pitted, corroded iron, flaking bands, cracked dull crystal, no glow |
| Common | plain blackened iron bands, one small crystal clasp, no glow |
| Rare | reinforced bands with steel rivets, brighter crystal clasp, faint glow along the lid seam |
| Epic | silver-trimmed bands, a larger faceted crystal, the family brand glowing |
| Legendary | silver filigree, a small skyglass crystal cluster crowning the lid, the brightest glow (still rim light, never a halo) |

### 4a. Director-approved central binding materials (2026-10-20 amendment)

**Only ONE centered family binding per chest.** Hunter always uses a **single broad FLAT hide/leather strap with a bone/fang clasp**; Gatherer always uses **a single ROUND twisted/braided rope with a tucked botanical sprig**. These materials are visual/texture descriptors, **not new item or loot-material records**. At 125px, keep the binding's different **base tone, width, and fiber/finish** readable; tiny threads may simplify. No binding is an extra metal hoop.

| Named tier | Hunter center strap, one flat hide/leather binding | Gatherer center rope, one round fiber/silk binding |
|---|---|---|
| **Rusted** | **Cracked ash-brown rawhide**, peeling/frayed edges, dull worn fang attachment. | **Rotting gray hemp**, rough fuzzy/unraveling fibers, one withered tucked sprig. |
| **Common** | **Smooth saddle-brown tanned leather**, broad plain flat hide, no silver stitching, simple bone/fang clasp. | **Honey-tan coarse three-strand twisted jute**, visibly rounded cord and simple knot, small fresh tucked green sprig. |
| **Rare** | **Smoky charcoal-brown pebbled salt-cured hide**, a few subtle tidy dark-steel eyelets/stitches integrated in the same flat strap. | **Slate-blue waxed flax** in a tighter herringbone braid, neat bound knot, tucked green sprig. |
| **Epic** | **Glossy near-black polished leather**, visible **silver saddle-stitching WITHIN the same strap's edges** and recognizable fang clasp. | **Pale silver-gray braided sea-silk**, subtle silver threads woven within the one continuous rope, green sprig retained. |
| **Legendary** | **Midnight-blue scale-embossed fine leather**, refined silver embroidery and *fine* integrated cyan skyglass thread, refined fang clasp. | **Storm-indigo braided silk** with fine silver strands and restrained cyan skyglass filaments integrated within the same cord; ornate knot and tucked green sprig. |

**Structural prohibition:** neither silver stitching nor flax braid forms an extra parallel arched band. Rusted fraying and Legendary thread are surface treatments of the **same central binding**. The Rare/Epic/Legendary armor, silverwork and filigree are separately applied **on the two existing metal end hoops**. Ornate and Mystery retain their separately approved special designs and are **not** automatically assigned Hunter leather or Gatherer rope.

**Source/provenance:** director-approved proposal recorded in `docs/design/ghost_ship_chests/CHEST_BINDING_MATERIAL_LADDER_PROPOSAL_20261020.md` and the geometry reset record. The operative art-direction rule is **this brief**, not its proposal.

### 4b. Director-approved upper-latch termination and motif evolution (2026-10-20)

**Binding termination is a hard physical rule for all ten Hunter/Gatherer variants:** the single center strap or rope runs over the closed domed lid, turns over the **front lip**, and **terminates at a compact keeper/lock on the upper front directly below the lid seam**. On Hunter, the short end is fastened by **one bone/fang clasp** integrated with the front skyglass lock. On Gatherer, a **single compact knot** secures the jute/flax/silk rope at the same upper-front receiver, with only very short tucked ends. **No leather or rope continuing down the bottom half of the front panel or the base of the chest**. This makes the clasp's lid-retaining function clear and leaves the clan/family brand on the lower front wood unobscured. Do not confuse the binding with the two structurally continuous OUTER METAL end hoops, which may still run down the corners.

**Director-approved design latitude:** the **single tooth/fang on Hunter's front keeper and botanical leaves in Gatherer's tucked sprig may evolve in SHAPE, SIZE, FINISH and restrained detail at each named tier** to signal increasing rarity. Do not force the same unchanging fang/leaf form on every chest. **A recognizable fang/focal leaf sprig remains present; the fixed family front brands remain exactly three Hunter claw gouges vs one Gatherer leaf.** The Hunter fang must not multiply into a mouth or a row of teeth; Gatherer foliage must remain small and tucked near the upper rope, never obscure the lid or crystal. This is **permission for graded art direction**, not an approved new game material, named monster source or loot rule.

**Suggested motif progression (visual candidate guidance, not rigid anatomy or final asset acceptance):**

| Named tier | Hunter's front tooth / fang — ONE recognizable focal piece | Gatherer's tucked botanical leaves / sprig — small, attached |
|---|---|---|
| Rusted | Short chipped, weathered tooth, dull/cracked keeper. | Withered, curled brown-green leaves, sparse and brittle. |
| Common | Small plain smooth ivory tooth; uncomplicated tooth silhouette. | Two or three simple fresh green leaves, clean pointed shapes. |
| Rare | Slightly larger hooked, polished tooth with restrained steel collar. | Denser veined three-leaf sprig with distinct serrated/pointed edges. |
| Epic | Elegant longer swept fang with refined silver mounting; no extra fang row. | Rich emerald lance-shaped leaves with selected cool-silver vein/edge accents, not glowing leaf-brand substitutes. |
| Legendary | Distinctive elegantly curved, scale-marked or delicately silver-inlaid fang with a tiny controlled cyan accent. | Compact branching dark-jade sprig with varied leaf shapes, fine silver/cyan vein accents; never a large magical canopy or lid-top crystal cluster. |

**Visual QC:** at 125px, verify **one ending/keeper**, not a full-body wrap; the family brand, central skyglass clasp and rare-tier ornament must each remain readable. The motif variations supplement, not replace, the already-approved tier-specific **strap/rope material** ladder in §4a and rare/epic/legendary metal/crystal treatments.

**Source:** director's 2026-10-20 reply approving upper-front termination for both families and authorizing changing leaves/monster tooth designs with tier as needed. This does NOT retroactively approve the images with long lower-front leather/rope. See `docs/design/ghost_ship_chests/FRONT_LATCH_AND_MOTIF_REFINEMENT_20261020.md` for the studio decision record.

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
| 3-8 | as the corresponding Hunter/Gatherer family subject with the original tier treatment from section 4 **AND the exact Rare/Epic/Legendary center binding materials from section 4a**, keeping the confirmed two-end-hoop geometry |
| 9-10 | as the corresponding Hunter/Gatherer family subject with the Rusted treatment from section 4 **AND the exact Rusted center binding materials from section 4a**, keeping the confirmed two-end-hoop geometry |
| 11 | a closed, grand domed-lid treasure chest with heavy silver filigree and several inset skyglass gems, aged gold trim |
| 12 | a closed domed-lid chest bound by crossed iron chains and a heavy lock, faint skyglass mist curling from the lid seam |

**Background clause:** `transparent background` where the generator supports it; otherwise
`on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`.

**Foliage exception:** Gatherer sprigs contain green leaves. When genuinely native alpha is unavailable, the canonical art spec's foliage-safe **flat magenta `#FF00FF`** key takes precedence over lime; declare this explicitly for that isolated generation and record the deviation at intake. A black JPEG background is **not** a native-alpha source or flat key.

## 7. Process

1. **Common Hunter (icon 1): DIRECTOR VISUALLY APPROVED, now conforming to premium pixel art + short upper latch (2026-10-20).** Director replied “Yes, next” after seeing short-latch pixel source `1000018956.png` (actual JPEG/RGB 1536×1536, 276722 bytes, exact SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`). It has one metal hoop per outer lid end, one smooth saddle-brown flat leather over the lid **ending at the upper-front fang/skyglass clasp**, exposed lower wood with exactly three claw gouges and premium crisp pixel clusters. **Rejected/reference-ineligible history:** first six double-band raws, smooth-painted `1000018934.png` and `1000018947.png`; long-leather pixel source `1000018935.png` remains a former style exemplar but NOT correct geometry. **This approval is visual only:** the new source is JPEG with black opaque matte, so alpha/key processing, lossless WebP, dark-composite QC, `artpreflight.py --type ICON` and uploads are all NOT_RUN.
2. **Common Gatherer (icon 2): DIRECTOR VISUALLY APPROVED, geometry and premium pixel style now locked for BOTH families (2026-10-20).** Director said “Approved, next” for corrected `1000018960.png`, true JPEG/RGB 1536×1536, 283293 bytes, SHA-256 `7721f96c04fe1c13475a0d7428b77a64999de70a69a822c5ec379d1faf8a961d`. It has exactly two outer metal hoops and a single round honey-tan three-strand JUTE rope ending in a compact upper-front securing knot with short tucked ends, green sprig, one unlit leaf wood brand and small cyan clasp. Full-size visual and **125px side-by-side** vs approved Common Hunter confirmed distinct family brands/bindings at matching 3/4 scale and consistent premium pixel clusters; 64/32px stress views checked. The old long-rope `1000018939.png` remains UNAPPROVED and prohibited as reference. JPEG/black source is not production ready: alpha/key, WebP export, dark-composite edge checks and artpreflight NOT_RUN.
3. **NEXT: Rare Hunter (icon 3)** — one NEW isolated session using **only** original Skyglass Reliquary (material/palette) + new director-approved short-latch Common Hunter `1000018956.png` (same Hunter family, camera, geometry and premium pixel style). See `docs/design/ghost_ship_chests/RARE_HUNTER_SHORT_LATCH_PIXEL_ART_ISOLATED_BRIEF_20261020.md`. Rare advances via raised riveted cold-gunmetal ARMOR ON each existing outer hoop (never duplicate hoops), a brighter compact skyglass gem, faint seam glow, **one charcoal-brown pebbled leather strap ending at the upper keeper**, moderately polished hooked fang and sparse four-point metal runes. Front THREE claw gouges remain UNLIT (glow reserved for Epic). Then follow with Rare Gatherer, Epic, Legendary and Rusted pairs, Ornate and Mystery. Each Hunter/Gatherer generation gets Reliquary plus the approved same-family predecessor only; Ornate/Mystery reference roles require a separate director decision before those sessions.
4. Two wrong-subject results in one session: close it and start clean (protocol section 3).
5. **Raw QC before processing:** square, one complete closed chest, **exactly two outer metal end hoops + one centered family binding that ends at the UPPER FRONT LATCH rather than the lower panel, with no duplicate side band**, tier-appropriate center material from section 4a, **premium crisp pixel linework/flat cel tonal clusters/limited palette (reject smooth painterly look)**, no text or extra symbols, no halo or glow disc, not sitting on a surface, background truly flat and keyable or genuinely transparent. JPEG on opaque black is NOT production-ready even when director visually approves the pixel art.
6. **Processing at intake:** key or keep native alpha, clamp spill, pad to square, lossless WebP,
   check edges on a dark composite, then `artpreflight.py --type ICON`.

## 8. Delivery and next step

- Return each approved original to the studio with its filename exactly as in section 2. A
  correction gets a fresh name (`_b`, `_c`).
- Include a ledger row per file: filename, type `ICON`, pixel size, bytes.
- After intake and preflight, the twelve icons go to the review desk as one Forge suggest-mode
  ticket (category VISUAL, title "Update icon", one rationale per chest).

## 9. Director decisions

Original family/tier/special designs were approved 2026-10-20 (items 1–4). **Same-day amendment**: director confirmed two end hoops/no duplicate side band and approved the five-level center binding material ladder in section 4a. Six historical duplicated-band images remain revoked; two corrected short-latch premium-pixel originals (Common Hunter and Common Gatherer) now have conforming **director visual approvals (2/12)** and Rare Hunter is next. Item 8 (actual game rarity) stays open.

1. Family motifs: claw gouges + leather and fang for Hunter's, leaf + rope and sprig for Gatherer's.
2. The tier ladder in section 4.
3. Aged gold as a second accent on the Ornate Chest.
4. Mystery Chest without a question mark.
5. **Amendment approved 2026-10-20 (RUL-2026-10-20-006):** one arched metal lid hoop per outer end plus ONE centered family binding, no duplicate parallel bands; the Rusted/Common/Rare/Epic/Legendary flat leather vs round rope material ladder in section 4a. These decisions invalidate the six historical chest image approvals, not the art-direction motifs.
6. **Upper-front binding termination and graduated organic motifs (2026-10-20):** the one central leather/rope binding terminates at the short latch just below the lid's front edge; it does not run to the base. Director authorized evolving the tooth/fang and botanical leaves by named tier while keeping Hunter/Gatherer family marks and the single central binding. See §4b; final motif pixels still require per-icon director acceptance.
7. **Premium pixel-art rendering is mandatory (2026-10-20):** conform to `25x_DATA_art_spec.json` (`house_style`, ICON scaffold). The director rejected smooth-painted candidates, accepted long-strap pixel-style exemplar `1000018935.png` for style only, then explicitly **approved final short-latch pixel Common Hunter `1000018956.png`**. Its pixels lock the family rendering standard and corrected upper-latch geometry; the raw is still opaque JPEG and alpha/export/preflight remain pending.
8. Separate, not part of this request: all twelve chests are rarity COMMON, including the
   "Legendary" ones. Rarity is a director call.
