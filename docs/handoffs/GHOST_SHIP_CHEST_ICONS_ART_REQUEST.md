# Art request: Ghost Ship chest icons (12)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-20)
- **Status:** APPROVED direction (RUL-2026-10-20-002), **amended 2026-10-20** after director geometry-reset and five-tier family-binding decisions (RUL-2026-10-20-006). The original six candidate visuals were subsequently **REVOKED for duplicated lid bands**: 1/12 currently valid visual approvals (geometry- and pixel-correct Common Hunter), but 0/12 finished/preflight-valid exports. The rendered premium pixel-art style, chest geometry and Hunter motif are now **visually locked by the newly approved Common Hunter**; Gatherer motif and twin readability await fresh icon 2 approval. This brief is the operative art-direction owner; its original approval history remains intact.
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
2. **For icon 2:** the new approved Common Hunter is **pixel-rendering, size, camera, geometry and overall chest-family construction reference ONLY**. Its claw brand, leather strap and fang are **not Gatherer subject references**. **From icon 3 onward**, use one NEW director-approved geometry-and-pixel-correct predecessor **of that exact Hunter/Gatherer family**, style and family motif only. **Never attach any of the six revoked images or the smooth-painted rejected Common Hunter**.

Do not pass the old pre-Ghost-Ship pixel-art chest icons (wrong family register), any of the six geometry-revoked images, or the smooth-painted Common Hunter candidate. Their rejection does **not** permit smooth painterly rendering: the **pixel art quality/style requirement above is binding**.

## 4. Design proposal (director to approve)

**Silhouette.** A classic closed domed-lid chest, distinct from the Reliquary's flat lid. **Director-locked construction (2026-10-20 geometry reset): exactly ONE continuous metal reinforcement hoop near the outer left end of the lid and ONE near the outer right end, plus ONE separate centered family binding (Hunter flat hide/leather strap or Gatherer round fiber/silk rope).** No extra parallel hoop beside the left or right hoop (the observed defect that invalidated six prior raws). Any Rare/Epic/Legendary layered plating, silver trim or filigree must be **on the surfaces of the existing TWO hoops**, never a third/fourth hoop or duplicate independent curved strip. Binding edge-stitching and rope knots must not masquerade as additional hoops. Verify physical band continuity in the original pixels before style/tier acceptance. See `docs/design/ghost_ship_chests/GEOMETRY_RESTART_20261020.md` for provenance and the invalidated image ledger.

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
| 1 | a closed domed-lid chest of dark wood with exactly one plain blackened iron lid hoop at each outer end (two total), no extra parallel arch, ONE separate centered broad flat smooth saddle-brown tanned leather strap, secured by a simple bone fang clasp, one small pale-cyan skyglass crystal clasp, three parallel claw gouges branded on the front panel |
| 2 | a closed domed-lid chest of dark wood with exactly one plain blackened iron lid hoop at each outer end (two total), no extra parallel arch, ONE separate centered thick round three-strand honey-tan jute rope secured by one front knot with a small green sprig tucked under it, one small pale-cyan skyglass crystal clasp, a single leaf branded on the front panel |
| 3-8 | as the corresponding Hunter/Gatherer family subject with the original tier treatment from section 4 **AND the exact Rare/Epic/Legendary center binding materials from section 4a**, keeping the confirmed two-end-hoop geometry |
| 9-10 | as the corresponding Hunter/Gatherer family subject with the Rusted treatment from section 4 **AND the exact Rusted center binding materials from section 4a**, keeping the confirmed two-end-hoop geometry |
| 11 | a closed, grand domed-lid treasure chest with heavy silver filigree and several inset skyglass gems, aged gold trim |
| 12 | a closed domed-lid chest bound by crossed iron chains and a heavy lock, faint skyglass mist curling from the lid seam |

**Background clause:** `transparent background` where the generator supports it; otherwise
`on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`.

**Foliage exception:** Gatherer sprigs contain green leaves. When genuinely native alpha is unavailable, the canonical art spec's foliage-safe **flat magenta `#FF00FF`** key takes precedence over lime; declare this explicitly for that isolated generation and record the deviation at intake. A black JPEG background is **not** a native-alpha source or flat key.

## 7. Process

1. **New pixel-art Common Hunter's Chest (icon 1) visually APPROVED on 2026-10-20:** new source `1000018935.png` (actually JPEG/RGB 1536×1536, 257500 bytes, SHA-256 `23038075363dc9ccafd4f4fb2ead70183704015ecb8f4abd66ad00bd8c23933a`). The director: “Now this is approved and perfect. Next.” This candidate has geometry-correct left/right single hoops, one saddle-brown flat leather/fang binding, three claw gouges, a small crystal and **intentional premium pixel rendering**. The original six candidates remain **rejected geometry-invalid**; the later smooth-painted Common Hunter `1000018934.png` is **style rejected**. Neither may be attached as a reference. **This new director visual approval locks the rendered pixel style/Hunter motif and approved geometry**, NOT alpha/export/preflight readiness.
2. **NEXT: Icon 2 (Common Gatherer's)**, in ONE NEW CLEAN isolated session using exactly **two individual actual images**: original Reliquary (**style/material only**) plus the newly approved **Common Hunter `1000018935.png`** (**premium pixel rendering, camera, geometry, scale only; NOT Hunter claw/leather/fang subject**). Enforce **one thick round honey-tan three-strand jute rope + tucked green sprig + one leaf brand**, two end hoops/no doubles, small skyglass crystal, and matching intentionally pixelated shade clusters. Director approval locks Gatherer motif and confirms distinctness at 125px in both front brand and physical binding.
3. Then Rare, Epic, Legendary and Rusted pairs, then Ornate and Mystery. For Hunter/Gatherer family icons, each session gets the Reliquary plus **one newly approved geometry-correct same-family predecessor** (max two separate individual images); do not attach revoked images or a collage. For standalone Ornate/Mystery, which have no same-family predecessor, settle the second-reference role explicitly before launching those sessions.
4. Two wrong-subject results in one session: close it and start clean (protocol section 3).
5. **Raw QC before processing:** square, one complete closed chest, **exactly two outer metal end hoops + one centered family binding with no duplicate side band**, tier-appropriate center material from section 4a, **premium crisp pixel linework/flat cel tonal clusters/limited palette (reject smooth painterly look)**, no text or extra symbols, no halo or glow disc, not sitting on a surface, background truly flat and keyable or genuinely transparent. JPEG on opaque black is NOT production-ready even when director visually approves the pixel art.
6. **Processing at intake:** key or keep native alpha, clamp spill, pad to square, lossless WebP,
   check edges on a dark composite, then `artpreflight.py --type ICON`.

## 8. Delivery and next step

- Return each approved original to the studio with its filename exactly as in section 2. A
  correction gets a fresh name (`_b`, `_c`).
- Include a ledger row per file: filename, type `ICON`, pixel size, bytes.
- After intake and preflight, the twelve icons go to the review desk as one Forge suggest-mode
  ticket (category VISUAL, title "Update icon", one rationale per chest).

## 9. Director decisions

Original family/tier/special designs were approved 2026-10-20 (items 1–4). **Same-day amendment**: director confirmed two end hoops/no duplicate side band and approved the five-level center binding material ladder in section 4a. Six visually accepted source images from before this correction were revoked; fresh geometry-correct approvals are pending. Item 5 stays open.

1. Family motifs: claw gouges + leather and fang for Hunter's, leaf + rope and sprig for Gatherer's.
2. The tier ladder in section 4.
3. Aged gold as a second accent on the Ornate Chest.
4. Mystery Chest without a question mark.
5. **Amendment approved 2026-10-20 (RUL-2026-10-20-006):** one arched metal lid hoop per outer end plus ONE centered family binding, no duplicate parallel bands; the Rusted/Common/Rare/Epic/Legendary flat leather vs round rope material ladder in section 4a. These decisions invalidate the six historical chest image approvals, not the art-direction motifs.
6. **Premium pixel-art rendering is mandatory (2026-10-20):** conform to `25x_DATA_art_spec.json` (`house_style`, ICON scaffold). The director rejected the smooth-painted geometry-correct candidate and approved new Common Hunter `1000018935.png`; **its pixels lock the rendered family style**, but its opaque JPEG black background means output alpha/export/preflight remain pending.
7. Separate, not part of this request: all twelve chests are rarity COMMON, including the
   "Legendary" ones. Rarity is a director call.
