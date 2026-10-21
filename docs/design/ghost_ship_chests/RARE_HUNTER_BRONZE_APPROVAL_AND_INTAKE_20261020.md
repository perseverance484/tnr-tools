# Rare Hunter's Chest — bronze-bound director approval and raw-source intake hold

**Status:** DIRECTOR VISUAL APPROVAL CONFIRMED · EXACT APPROVED RAW NOT YET RECEIVED/VERIFIED · preflight NOT_RUN  
**Lead:** Art Director · **Support:** Image Production  
**Canonical operative direction:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md` §§3–7; supporting design record `RARITY_MATERIAL_AND_TROPHY_REFINEMENT_20261020.md`.  
**Target:** Rare Hunter's Chest · `item.image` · `ICON`  
**Final delivery filename:** `icon-gs-chest-hunter-rare.webp`  
**Restrictions:** zero live-game requests/writes, no credentials, no publishing or game upload. No item rarity adjustment.

## Director approval: art direction + depicted Rare Hunter design

The director's handoff explicitly states **“APPROVED — NEW CHEST RARITY DIRECTION”** and **“RARE HUNTER — DIRECTOR APPROVED.”**

**Approved appearance:** the unchanged short-latch Common Hunter dome, TWO original-shape outer metal hoops and corner fixtures, single smoky charcoal pebbled-leather upper-front strap, **BURNISHED DARK BRONZE** metal (not cold gunmetal or silver), precisely ONE prominent **sharp hooked monster talon** instead of a generic Common ivory fang, small stronger cyan faceted clasp, faint thin cyan lid-seam light, THREE carved unlit front claws, exposed dark wood and premium crisp pixel-art clusters. Director REJECTED the preceding structural redesign with oversized angular gunmetal armor blocks and large star ornaments. Later rarity should also retain the same physical chest template and change materials/accessories instead of constructing larger bands.

The attached visual is consistent at inspection scale with the approved bronze-bound design; this is **visual approval evidence only**, not proof of raw-byte identity, mechanical transparency compliance, or game readiness.

## Critical source discrepancy — cannot pass original-intake identity gate

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

**Consequence:** Do not label the screenshot/preview as the director's **exact approved original** or record the expected SHA as byte-verified. Do not attempt to create a “matching” PNG from the preview, retroactively claim exact provenance, key black destructively, or mark the source as intake PASS. **Request the actual `rare_hunter_s_bronze_bound_chest.png` original file** (the specified PNG/RGBA 1254×1254) for the studio to decode/hash/inspect. It may be uploaded now or later; Rare Gatherer generation does NOT depend on Rare Hunter source pixels.

## Preview-only comparison and QC (not canonical raw QC)

The studio used the actual **JPEG display preview** and the director-approved Common Hunter source `1000018956.png` (true JPEG/RGB, SHA-256 `a46aa0279a7ba45784f397417c5fd4b8a5fb40ebde3a71074699d35ffdb7562c`) for deterministic **125, 64 and 32 px** reductions. No generation or manipulation of raw source colors/geometry occurred; comparison is a visualization aid, not a substitute for original intake.

- **125px preview visual QC:** bronze bands and corner metal clearly distinct from Common black steel, same basic domed silhouette, central charcoal leather, prominent single hooked talon, cyan gem and three claw marks; no large added plates or duplicated hoop. **Preview composition/style PASS**, but does NOT establish whether the claimed original differs at its actual native pixels.
- **64px stress view:** bronze material separation and general chest still read; small details naturally simplify.
- **32px stress view:** hardware and trim/accessory details heavily compressed; game inventory's **125 px** gate is controlling.
- **Original-source alpha, full-resolution visual QC, edge-clamp/keying, lossless WebP/export byte ceiling, dark composite, `artpreflight.py --type ICON`: NOT_RUN.**

## Intake and downstream

1. Obtain `rare_hunter_s_bronze_bound_chest.png` as a discrete original file, not an app screenshot or recompressed JPEG. Check it actually decodes as PNG/RGBA 1254×1254 with 1,349,268 bytes and SHA-256 matching the director's stated `99ca6f...` hash. If it differs, **record and explain** discrepancy before proceeding; don't silently conflate files.
2. Inspect PNG alpha histogram for actual transparency (RGBA mode alone is insufficient), crop/pad/square alpha margin, visible dark-edge spill, pixel-art quality, and 125/64/32px family comparisons.
3. Once approved original passes raw QC, create lossless `ICON` WebP at 256×256 recommended (must stay **below 460800 bytes**), with alpha padding, dark-composite edge inspection and canonical `artpreflight.py --type ICON`; save full output, final bytes and export hash in studio ledger. No game upload/publishing.
4. **Rare Gatherer generation has since been visually approved** (2026-10-21): `1000018969.png` actually JPEG/RGB 1536×1536, 304581 bytes, SHA-256 `c421c5ff3cc2e26eb7fb3a7f2c881196fa21d559c3119cc65384eedac2eeca9a`, alpha/preflight pending. **NEXT intended generation is Epic Hunter, BLOCKED until this approved Rare Hunter PNG original is actually supplied and byte verified as the second reference.** Only after PASS attach original Reliquary + the verified Rare Hunter PNG to the isolated session. No user-authorized fallback to Common Hunter or the nonidentical Rare JPEG preview exists. See `EPIC_HUNTER_SILVER_HORN_SHORT_LATCH_ISOLATED_BRIEF_20261021.md`.
