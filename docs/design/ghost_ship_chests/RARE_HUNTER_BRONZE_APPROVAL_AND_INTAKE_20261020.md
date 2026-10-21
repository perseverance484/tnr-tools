# Rare Hunter's Chest — bronze-bound director approval and verified original intake

**Status:** DIRECTOR VISUAL APPROVAL + EXACT PNG ORIGINAL BYTE/FORMAT/ALPHA INTAKE **PASS (2026-10-21)** · approved reference UNBLOCKED · production alpha cleanup/export/preflight NOT_RUN  
**Lead:** Art Director · **Support:** Image Production  
**Canonical operative direction:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` §§3–7; supporting design record `RARITY_MATERIAL_AND_TROPHY_REFINEMENT_20261020.md`.  
**Target:** Rare Hunter's Chest · `item.image` · `ICON`  
**Final delivery filename:** `icon-gs-chest-hunter-rare.webp`  
**Restrictions:** zero live-game requests/writes, no credentials, no publishing or game upload. No item rarity adjustment.

## Verified original ZIP intake — PASS (2026-10-21)

**Source:** director uploaded **`Rare_Hunter_Approved_Original_PNG.zip`**, ZIP SHA-256 `c4cf58e360c42dcca9be629a090cff49147ef28afd559e271d0ea3ba56a7e044`. ZIP contained **exactly one** regular, non-symlinked entry with no path traversal: `rare_hunter_s_bronze_bound_chest.png`. The studio read the member's raw bytes without format conversion and preserved an exact copy in this conversation at `/mnt/data/rare_hunter_s_bronze_bound_chest.png`. **Neither ZIP nor PNG was written to the Git repository.**

| Check | Independently observed | Verdict |
|---|---|---|
| Filename inside ZIP | `rare_hunter_s_bronze_bound_chest.png` | **PASS** |
| Raw byte count | **1,349,268** | **PASS — equals director report** |
| SHA-256 of extracted PNG bytes | **`99ca6f817fe390b0c9aff16cdc2016f70d897f44dbda2e06b511696a5da94f08`** | **PASS — exact match** |
| Image signature and decoder | PNG / **RGBA** | **PASS — not recompressed JPEG** |
| Original pixel dimensions | **1254 × 1254** (square) | **PASS** |
| Real native alpha (not just RGBA label) | 734,780 alpha=0 pixels; 837,182 alpha=1…254; 554 alpha=255 | **PASS — genuine transparency** |
| Fully transparent corners | All four are RGBA `(0,0,0,0)` | **PASS** |
| High-opacity (>8) subject bounds | `(68, 193, 1173, 1141)` in original 1254² canvas | Margin present; see production note |
| Source visual / family subject | Verified original depicts the director-approved Rare bronze hoops, same chest body, single short charcoal strap, hooked talon, unlit 3 claws, cyan gem and faint seam; premium pixel clusters | **PASS for same-family generation reference** |
| Source visual QC scales | Original reduced to **125px / 64px / 32px** using non-destructive Lanczos resampling | **Performed; 125px is controlling** |
| End-to-end production clean edges / final ICON WebP / byte limit / `artpreflight.py --type ICON` | Not yet performed | **NOT_RUN** |

**Alpha nuance:** most nonzero-alpha pixels are partially transparent rather than exactly 255. Stray **alpha=1** pixels touch the left and bottom boundaries even though the clearly visible subject has a margin. Before any game delivery, inspect/clamp tiny alpha spill, check dark/light composite outlines, and ensure sufficient transparent padding on a final 256×256 lossless WebP; no silent alteration to the original source. This is **NOT a source-reference blocker**, but production QC has NOT passed.

**Gate disposition:** **RAW IDENTITY + TRUE ALPHA + APPROVED VISUAL REFERENCE PASS. Epic Hunter isolated generation UNBLOCKED.** This does NOT mean the Rare Hunter icon is mechanically production-ready, uploaded, published, or finally accepted as a processed asset.

## Director approval: art direction + depicted Rare Hunter design

The director's handoff explicitly states **“APPROVED — NEW CHEST RARITY DIRECTION”** and **“RARE HUNTER — DIRECTOR APPROVED.”**

**Approved appearance:** the unchanged short-latch Common Hunter dome, TWO original-shape outer metal hoops and corner fixtures, single smoky charcoal pebbled-leather upper-front strap, **BURNISHED DARK BRONZE** metal (not cold gunmetal or silver), precisely ONE prominent **sharp hooked monster talon** instead of a generic Common ivory fang, small stronger cyan faceted clasp, faint thin cyan lid-seam light, THREE carved unlit front claws, exposed dark wood and premium crisp pixel-art clusters. Director REJECTED the preceding structural redesign with oversized angular gunmetal armor blocks and large star ornaments. Later rarity should also retain the same physical chest template and change materials/accessories instead of constructing larger bands.

The attached visual is consistent at inspection scale with the approved bronze-bound design; this is **visual approval evidence only**, not proof of raw-byte identity, mechanical transparency compliance, or game readiness.

## Historical pre-ZIP source discrepancy — RESOLVED 2026-10-21

**This section records the earlier failed JPEG attempts and their pre-ZIP status; the operative PNG PASS is documented above.** The JPEG hash remains separate and MUST NOT replace the verified original PNG.


The director's handoff identifies the **approved ORIGINAL** as:

| Field | User-supplied expected original (UNVERIFIED) |
|---|---|
| Filename | `rare_hunter_s_bronze_bound_chest.png` |
| True decoder format / channels (stated) | PNG / RGBA |
| Pixel dimensions (stated) | 1254×1254 |
| Raw bytes (stated) | 1,349,268 |
| Raw SHA-256 (stated) | `99ca6f817fe390b0c9aff16cdc2016f70d897f44dbda2e06b511696a5da94f08` |
| Byte-equivalent file available to the studio? | **NO — NOT RECEIVED, NOT VERIFIED** |

The **actual attached chat image** is NOT that original:

| Field | Verified supplied visual (PREVIEW ONLY) |
|---|---|
| Mount / uploaded display filename | `/mnt/data/1000018962.png` |
| Actual decoder format / channels | **JPEG / RGB, opaque** despite `.png` suffix |
| Pixel dimensions | **1536×1536** |
| Raw bytes | **301,659** |
| SHA-256 of these attached bytes | `6c7c4d879f9261c6cd3b03c8a461053363b13293f42a1ba8aefd0de221babfd6` |
| Real alpha? | **NO**, JPEG/RGB black matte; NOT valid transparent ICON production input |
| Equal to the claimed RGBA PNG original? | **NO** |

**Historical consequence, now satisfied:** Before ZIP intake, the JPEG preview could NOT establish the approved original's identity. It remains a SEPARATE lower-fidelity JPEG and is NEVER relabeled or used as the approved PNG. The authentic `rare_hunter_s_bronze_bound_chest.png` has **now arrived inside ZIP** and matches every reported field; see the PASS record above. The preview discrepancy is resolved rather than concealed.

## Preview-only comparison and QC (not canonical raw QC)

The studio used the actual **JPEG display preview** and the director-approved Common Hunter source `1000018956.png` (true JPEG/RGB, SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`) for deterministic **125, 64 and 32 px** reductions. No generation or manipulation of raw source colors/geometry occurred; comparison is a visualization aid, not a substitute for original intake.

- **125px preview visual QC:** bronze bands and corner metal clearly distinct from Common black steel, same basic domed silhouette, central charcoal leather, prominent single hooked talon, cyan gem and three claw marks; no large added plates or duplicated hoop. **Preview composition/style PASS**, but does NOT establish whether the claimed original differs at its actual native pixels.
- **64px stress view:** bronze material separation and general chest still read; small details naturally simplify.
- **32px stress view:** hardware and trim/accessory details heavily compressed; game inventory's **125 px** gate is controlling.
- **Historical preview-only check.** The authentic source was later separately opened and reviewed at full resolution and 125/64/32px. PNG source identity/alpha existence PASSED; edge cleanup, final lossless WebP/dark-composite output QC and `artpreflight.py --type ICON` remain NOT_RUN.

## Intake and downstream

1. **DONE / SOURCE IDENTITY PASS (2026-10-21):** received `Rare_Hunter_Approved_Original_PNG.zip` containing exactly one regular-file member named `rare_hunter_s_bronze_bound_chest.png`, uncompressed size 1,349,268 bytes. Independent SHA-256 matches `99ca6f817fe390b0c9aff16cdc2016f70d897f44dbda2e06b511696a5da94f08` and decoder confirms PNG/RGBA 1254×1254.
2. **PARTIAL PASS (raw inspection):** genuine alpha confirmed (734,780 pixels alpha=0; 837,182 partially transparent; 554 alpha=255), source visually inspected and 125/64/32px reductions made without changing original pixels. Significant *partial alpha across painted subject* and isolated alpha=1 noise at left/bottom canvas edges require final edge cleanup/dark composite QC; **no source file was modified**.
3. Once approved original passes raw QC, create lossless `ICON` WebP at 256×256 recommended (must stay **below 460800 bytes**), with alpha padding, dark-composite edge inspection and canonical `artpreflight.py --type ICON`; save full output, final bytes and export hash in studio ledger. No game upload/publishing.
4. **Rare Gatherer was visually approved** (2026-10-21): `1000018969.png` is JPEG/RGB 1536×1536, 304581 bytes, SHA-256 `c421c5ff3cc2e26eb7fb3a7f2c881196fa21d559c3119cc65384eedac2eeca9a`, alpha/preflight pending. **NEXT Epic Hunter generation is now READY:** reference original PNG input gate PASS. Attach exactly (A) original Skyglass Reliquary (material/palette only) + (B) this verified Rare Hunter original (same-family geometry/style). The JPEG preview is still prohibited as a substitute; see the updated `EPIC_HUNTER_SILVER_HORN_SHORT_LATCH_ISOLATED_BRIEF_20261021.md`.
