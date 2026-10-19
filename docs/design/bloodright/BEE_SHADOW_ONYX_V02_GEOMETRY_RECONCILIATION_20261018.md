# BR-011 BEE — Director-Approved Onyx Visual Source and Geometry-Locked V02 Trio

**Date:** 2026-10-18.
**Lead:** Image Production · **Supporting:** Art Director.
**Source branch:** `chatgpt/bee-bloodright-tier-studio-20261018`, art lineage based on `chatgpt/bbe-pale-blue-source-correction-20261018@557ed266567d45324b746a40e467c0f0635ae8ce`.
**STATUS:** The director specifically VISUALLY APPROVED ALL THREE corrected **Bloodwoven Onyx Shadow V02** tier images on 2026-10-18 (reply “Approved”). All three previously proposed original PNG and lossless WebP image bytes remain unchanged and geometry-exact. The previously approved freehand Foundation remains preserved only as historical visual reference because it FAILS original-master geometry. 84/87 approved standalone image bytes now consolidated. Game-field/upload preflight still OPEN.

## Director decision and explicit geometry distinction

The user rejected the weak-on-onyx Bloodwoven Onyx V01 Foundation and requested **“Work some shadow energy into the design.”** A new digitally rendered freehand black obsidian / crimson chakra Foundation looked much closer to the intended onyx identity. The user replied **“Now we're talking. Make sure it respects the geometry and proceed,”** and subsequently **“Perfect. Approved”** to the revised **single raw image** `blood_obsidian_crystal_crest.png`.

**Exact director-approved source image:** `blood_obsidian_crystal_crest.png`, **1254×1254 RGB PNG**, SHA-256 **`97778194f3efeeb24d25fdba4a3160bef19e08bb1ab7bef87a26eb27fdbdb002`**. Preserve these bytes unchanged. The preceding image `blood_red_obsidian_arcane_sigil.png` SHA `bacaf49cfd44165cd657da1237b79c7cc2a86fcab1632335a86ea8d0b84d91fc` is a prior exploration, **not** the latest director-accepted exact image.

**Critical evidence boundary:** The director's visible-image acceptance **does not magically make freehand generation pixel-identical to the canonical master**. Independent per-pixel analysis comparing the approved source to the 1254px Foundation `max(R,G,B)` master finds only **56.119% exact pixel maximum intensities** and binary mask IoU **0.851 at threshold 1**, **0.6862 at 32**, **0.3768 at 128** (the full report contains 1/8/16/32/64/128/192/240/254). Some external smokelike wisps and part of the bright edge fall outside the source-master support. A screenshot resembling a nested diamond is NOT sufficient to certify the original geometry. **The approved image is an immutable VISUAL REFERENCE, not a game-compliant master-matched source.** This conflict was not glossed over or silently waived.

The original earlier **strict-master Bloodwoven Onyx V01** (Foundation PNG SHA `56805f654f184ad3810153690a63be95b50128a9c8ba7f71f22b7e622edc6fc4`, WebP SHA `43b407e93744ee3c312c47e181faf55dd467b04ebc01c468be84d5f921e5658d`) passed its geometric QA but was **not** director-approved; its palette did not convey enough genuine black onyx/shadow. Keep only as historical rejected/pending material exploration; never substitute it as the accepted source.

## One reproducible, canonical-shape reinterpretation — all three tiers PROPOSED

The subsequent user **“Proceed”** authorized continuation of matching Bloodwoven Onyx Shadow material across Hidden/Advanced and the necessary exact-geometry correction. To avoid another freehand failure, the approved `blood_obsidian_crystal_crest.png` is used **solely as a local material/chroma identity reference**; its shapes do not control any tier geometry. An original source-master-driven deterministic script transfers its scarlet/onyx color treatment **only to luminous original-master pixels**, with narrow existing onyx facet, ruby channel and red shadow patterns inside them. This necessarily trims external shadow wisps and remaps some bright features. **Foundation changes are NOT automatically accepted under the earlier raw-image approval**.

Original actual individual Ethereal Monarch geometry masters are read from the user-supplied `Bloodright_Wave06_Production_Starter_20261018.zip` SHA-256 `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`:

| Tier master | Original SHA-256 |
|---|---|
| Foundation | `bb3a3e331e5913fa527049980e2738c151b85eb54ef579cd468126b10039cea2` |
| Hidden Art | `97ac6df359070f885d8d5545060b788bbd8d374fdfd181c90c60976560a213fc` |
| Advanced Art | `0e97566732f8ade28eedb1b18f77a666b9804f9467198f9574e3757d940cd014` |

Each output is separately saved 1254×1254 opaque RGB PNG, independently downscaled with Pillow LANCZOS to separate 256×256 RGB **VP8L lossless** WebP. Every candidate pixel's full-resolution `max(R,G,B)` exactly equals the corresponding tier master's original value, all **27/27 threshold masks** at 1,8,16,32,64,128,192,240,254 match pixel-for-pixel. No new shape, text, outer ring, eye, particle field, halo or edited existing WebP is smuggled into the game-asset files.

| Tier | NEW proposed source PNG SHA-256 | NEW proposed VP8L WebP SHA-256 | WebP bytes | Art status |
|---|---|---|---:|---|
| Foundation (strict correction) | `5f14a070ab2a6eba9f88913e111908a3065efcd4f897803bc5f04267e77b292c` | `ad76fc20e1082da7d8c5e53019f20b5caa3a1afc13c20252fad4dd1071431dc4` | 47,304 | **PROPOSED — new modified pixels require director review** |
| Hidden Art | `e4194a7d84570379a99948085aef693e98ad2bf2b58d12c1ff5f940fe763f406` | `8819cadf0d95ad68665885709846d41297497085fe2fa42dbeed71246e7a32e2` | 73,666 | **PROPOSED** |
| Advanced Art | `1ae46a8bd072088169df427ec3fa8bb746a333e0f238bde5304053a7a53de631` | `e38feaf77ec28442095aab9307e888db481fa2b98da4196f1a4cea85a0b4e021` | 64,576 | **PROPOSED** |

**Independent offline QC:** **139/139 checks PASS, 0 FAIL**, including exact BEE 8-jutsu/identity original archive SHA/CRC, 9 image SHA/bytes/decoder tests, exact onyx director-approved raw source SHA unchanged, original 81 approved WebP ZIP unchanged SHA `ae5211a787b95025881a112f41701ae23629865d0ac4a9aeda67cde6c8887bd1`, three real master original SHA, full RGB 1254 master intensity equality + 27 binary-mask tests, three output PNG decode, three output VP8L codec + WebP decoded pixelwise equality to intended LANCZOS source resize, 4 black corners each, 125/64/32 thumbnail signal checks, deterministic six-art-file recipe replay in clean directory, ZIP CRC/duplicate/membership/member-byte equivalence. These checks do not certify visual acceptance or the client image field.

### Portable exact files

- Three new V02 *proposed-only* WebPs in a flat ZIP: `BR011_BEE_Bloodwoven_Onyx_Shadow_v02_3_WebPs_PROPOSED_20261018.zip` SHA-256 **`a6874a7eef20434bcb84442a6c9e6e91b219fdbbfda1a2aa4fa067bd67928894`** (186,196 bytes).
- Full portable V02 source/art/QC bundle: `BR011_BEE_Bloodwoven_Onyx_Shadow_v02_Complete_QC_PROPOSED_20261018.zip` SHA-256 **`21f2e98960c06df1c07d8d0aa6227175224545106e9329c5863ef9e8e08dac74`** (15,794,562 bytes), includes approved original freehand unchanged, exact BEE reference ZIP, exact starter/master ZIP, replayable producer, 3 independent source PNG + 3 WebPs, QC and visual proof.
- `qc/BEE_Shadow_Onyx_v02_Three_Tier_REVIEW.png` — programmatically composed from the three separate saved VP8L WebPs; no image generator redraw in the sheet.
- `qc/BEE_Bloodwoven_Onyx_Approved_Source_vs_Strict_Geometry_v02.png` — displays the exact director-approved freehand Foundation beside the genuinely corrected Foundation, Hidden Art and Advanced Art.
- `qc/BEE_Shadow_Onyx_v02_125_64_32_QC.png`, `qc/BEE_Shadow_Onyx_v02_Neighbor_Contrast_QC.png`, and `qc/BEE_Shadow_Onyx_v02_Independent_QC.json`.

## User decision and safety holds

**NEXT:** Ask director to accept/rework the actual three master-corrected V02 icons as a coherent set, **explicitly including the geometry-corrected Foundation**. Earlier raw freehand Foundation stays approved *as a visual reference* regardless of decision; approval cannot be silently transferred to the changed strict version. If user wants the exact raw freehand Foundation in the game instead, that is a separate **explicit geometry-exception decision** to surface, not an implicit waiver.

**Counts remain 81/87 independently accepted standalone WebPs.** Do not add BEE's three new unapproved V02 files to the approved 81 pack or call the new full trio finished. The other missing family is BR-036 Itojinsei Blackwire with director-approved three-emblem single-sheet visual identity but no separately source-/geometry-accepted raw PNG+WebP pair.

**Field preflight:** `skillTree.image` actual opaque-background RGB consumer/alpha contract has not been verified. Shared generic `ICON` still expects keyed alpha, and `JUTSU_ICON` alpha-optional only covers `jutsu.image`. No successful `artpreflight.py` field-specific run is claimed; neither the original approved image nor the three proposed versions are cleared for live upload. The earlier 21 accepted source-master-nonexact images, immutable Git art pins, Forge imagePack, art-lineage RUL-ID collision with `main` remain unresolved. **No live-game reads, writes, uploads, or credentials**.

## 2026-10-18 — Director V02 trio acceptance, verified output bytes and 84-icon consolidation

The user replied **“Approved”** to the explicit question **“Do you approve all three geometry-corrected Bloodwoven Onyx icons? That includes the revised Foundation, which differs slightly from the original you approved.”** This definitively approves the exact **Foundation, Hidden Art and Advanced Art V02 corrected artworks** pictured in this document, not only the material concept or previous freehand original. Their **three full-size PNG SHA-256 and three lossless 256px WebP SHA-256** values are unchanged from the proposal table. No redrawing, recoloring, regeneration or geometry exception was introduced during acceptance.

**Archived approval and download evidence:**
- `BR011_BEE_Bloodwoven_Onyx_Shadow_v02_3_WebPs_APPROVED_20261018.zip`, SHA-256 **`a6874a7eef20434bcb84442a6c9e6e91b219fdbbfda1a2aa4fa067bd67928894`**, 186,196 bytes. The ZIP and its three VP8L members are byte-for-byte the proposal archive and exact director-reviewed pixels; only the outer delivery filename has changed.
- `BR011_BEE_Bloodwoven_Onyx_Shadow_v02_APPROVED_Source_QC_20261018.zip`, SHA-256 **`8eaa9c855d3dbdce903dc92c48a0124a4d1c424df7c2a43588dea6095f78f650`**, includes all **16 original proposal members byte-identical**, plus `DIRECTOR_APPROVAL_20261018.json` and `README_APPROVED.txt`. Original README and QC remain intact as historical records of candidate status at the time, superseded as image acceptance only by the later director decision.
- `Bloodright_84_Approved_Original_WebPs_256px_20261018.zip`, SHA-256 **`c2d4eb48d16531f3ea27a270e86f435cd438ff1a58e3e5500f06fba03e5b82bc`**, 5,248,019 bytes, contains **84 individual original named VP8L RGB WebPs across 28 families**: all previously accepted 81 images bit-for-bit unchanged, plus these three BEE V02 exact approved WebPs. No duplicates, no alpha fabrication.
- `Bloodright_84_Approved_Icons_SHA256_Manifest_20261018.json` provides the 84 file identities, sources and SHA; `Bloodright_84_Approved_Icon_Consolidation_QC_20261018.json` records a fresh **424/424 passed / 0 failed** post-approval read-only audit on the original 81 ledger and bytes, BEE source/master hash, full 1254px exact maxRGB, 27/27 threshold masks, VP8L decoded Lanczos equality, black corners, archive CRC/member byte preservation, deterministic pack rebuilds and exact accepted source SHA. The original 139/139 BEE V02 production checks remain separate prior proof.

**Now 84/87 individual art files director accepted, 28/29 complete families.** The only three remaining independent art assets are **BR-036 Itojinsei Blackwire**, visually accepted as a single composite (three visual designs) but not yet accepted as three geometry-verified independent source PNG + WebP images. Its rejected pale silver Tensionwire V01 files must NOT be silently substituted. All earlier 21 historically visually accepted strict-master-nonexact original assets stay byte-identical and retain their separate technical warnings.

**Remaining RED:** `skillTree.image` field-specific opaque RGB acceptance/preflight is unverified; generic `ICON` alpha key exception is not established for it; immutable source Git pins, Forge imagePack, art-lineage ruling-ID conflict, and any user-operated live game import/readback remain future gates. **Game reads 0, writes 0, uploads 0, credentials none.**
