# BR-015 Blue Blade Eyes — Midnight Blade Alloy, Foundation Geometry-Locked Pilot

**Date:** 2026-10-18 · **Status:** **ONE FOUNDATION ICON PROPOSED, NOT DIRECTOR-APPROVED.** Full-resolution fixed geometry, 9/9 masks and file-format QC PASS; **game `skillTree.image` preflight NOT RUN/NOT CLEARED**.
**Lead:** Image Production · **Support:** Art Director.
**Repository:** `perseverance484/tnr-tools`; **branch:** `chatgpt/bbe-midnight-alloy-foundation-pilot-20261018`; **base:** diagnosis `chatgpt/bbe-tier-geometry-diagnosis-20261018@65132ecfae542d56c9f17422ca473c9e29d776f2`. User-directed step after repeated freehand shape failures: "Proceed" with a **single fixed-mask BBE Foundation proof**, *not* permission to accept or automatically generate the other two tiers.

## Source, workflow and distinctness

- **Source image**: exact independent `Ethereal_Monarch_Foundation_TEAL_1254.png` from director-supplied `Bloodright_Wave06_Production_Starter_20261018.zip`, SHA-256 **`9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`**, master SHA-256 **`bb3a3e331e5913fa527049980e2738c151b85eb54ef579cd468126b10039cea2`**, 1254×1254 opaque RGB. The source is unchanged. No reinterpreted sigil or image-generator sheet enters this file.
- **Approved family comparator originals**: BR-034 Hyouga Yui Cerulean Shatter (cobalt fractured ice), BR-077 Teno Yuki Winterglass Sanctum (near-white frost), BR-065 Shinrai Ou Raijin Whitebolt (pale white-blue conductor) and BR-083 Tetsugan Ward-Forged Steel (light metallic/cyan). The four exact already approved individual WebPs were decoded from `Bloodright_78_Approved_Original_WebPs_256px_20261018.zip` SHA-256 `af836e30dbbcc605e1c955ad3436912ac24c9eeb2e9a674cbd45f08a1d987af7`; they were inspected alongside the new result and left untouched.
- **New treatment:** **Midnight Blade Alloy V03** — concentrated dark-ultramarine/sapphire facets, restrained silver-blue blade-edge reflections and deep navy negative-space hierarchy. No pale-white family-level ice treatment, no bright cyan glacier fields, no violet dominant cast, no added pupil, blade glyph, orbit, frame, label, or sparkle. It preserves the original underlying ornamental master faceting (the source is itself crystalline); subjective *metal versus ice* separation remains the director's final art judgment.
- **Evidence limitation:** historical BBE tier originals are only SHA-identified in `docs/design/bloodright/BBE_ICON_OUTPUT_QC_20261008.json`, not recovered as binary sources in this conversation; the **six BBE jutsu reference images are not locally available**. This candidate is calibrated to the historical BBE identity/approved family examples and the director-requested distinctive material direction, **not represented as source-jutsu-pixel matched**.

## Exact proposed artwork — ONE tier only

| Tier | File | Actual SHA-256 | Bytes | Decoder/geometry |
|---|---|---|---:|---|
| Foundation raw | `br015_bbe_foundation_midnight_blade_alloy_v03_1254.png` | **`6a15c3f0548a36dd3f381d88bdeacdeb26ca49c09d82199326c7f0897488c042`** | **1,171,155** | 1254×1254 RGB PNG; exact master maxRGB at every pixel |
| Foundation processed | `br015_bbe_foundation_midnight_blade_alloy_v03_256.webp` | **`d35c63b986f36484a7c7c1c6e7197c55f6e30bbf8c6520e22077be4fd12709f3`** | **47,132** | 256×256 RGB WebP / RIFF VP8L lossless |

**Independent offline QC: 46/46 test assertions PASS, 0 FAIL**. Verifies parent starter SHA and CRC, source SHA, byte-identical master extraction, raw/output dimensions and modes, **full 1,572,516-pixel max(R,G,B) equality**, original black void untouched, exact masks at nine thresholds **1, 8, 16, 32, 64, 128, 192, 240, 254 (IoU=1.0 each)**, original raw and 256px WebP SHA, lossless RIFF `VP8L` codec, pixelwise decoded WebP equality to `Pillow LANCZOS` downsize, <=460800-byte generic-icon reference cap, four original-source comparator decodes, black/near-black corners, and 125/64/32 legibility tests. An independent clean-directory rerun of the included material processor **reproduced both original PNG and WebP exact SHA-256s**. Prior 78 WebP archive remains unaltered.

**Source geometry classification:** this exact strict intensity test is stronger than approximate outer outline tolerance; it guarantees every source pixel's maximum RGB brightness and every threshold mask exactly. This does **not** claim the newly proposed color treatment looks distinct enough to the director; no art acceptance or replacement of historical BBE art is inferred.

## Portable artwork and review evidence

- **Proposed art + verifiable source + deterministic producer + QC archive:** `BR-015_BBE_Foundation_Midnight_Blade_Alloy_v03_PROPOSED_20261018.zip`; SHA-256 **`33b1b1983d627ee70f4b48501d3a388247099f1063db6a928b3791656d07dc1c`**, **3,149,526 bytes**, 10 ZIP entries, CRC PASS, **two independent deterministic pack rebuilds yielded identical SHA**.
- Full-resolution proposed Foundation raw: standalone `br015_bbe_foundation_midnight_blade_alloy_v03_1254.png` (art candidate, no labels).
- Processed review icon: standalone `br015_bbe_foundation_midnight_blade_alloy_v03_256.webp`.
- Programmatic comparison from *saved actual source pixels only*: `qc/BBE_Foundation_v03_Approved_Neighbor_Contrast_QC.png` SHA `8747a3dbed141ed4d40be441362e08db06f564396492e2481905c466391dc0a1`; master/original geometry comparison `qc/BBE_Foundation_v03_Master_Geometry_Comparison.png` SHA `d544b9532a7b8af0ba6d6379856574c8c37c6fc87f27c45530afe8b663977e08`; thumbnail stress `qc/BBE_Foundation_v03_125_64_32_QC.png` SHA `a6bf0efeb104fdd1b6db7b617feef6f1f3d3e9615d685555f08538638cfa44d9`.
- Exact 46-check report `qc/BR015_Foundation_v03_Independent_QC.json` and reproducible source `producer/produce_foundation_v03.py` included in archive.

## Acceptance and explicit technical boundaries

**NEXT director gate:** review the *actual single Foundation candidate*, preferably at 125/64/32 and beside Hyouga/Teno/Shinrai/Tetsugan. Director either accepts Midnight Blade Alloy material/quality for Foundation or requests modifications. **Hidden Art and Advanced Art were NOT produced**; only after this style checkpoint may the same appearance recipe be applied to their two **independent** 1254px verified tier geometry masters, with all geometry tests repeated independently.

**No mechanical upload-ready declaration:** current shared `ICON` alpha/chroma requirements are for `item.image,bloodline.image`; current `JUTSU_ICON` optional-alpha is solely `jutsu.image`, not `skillTree.image`. Future Bloodright tier icon client field is **unverified** for this art studio; formal `artpreflight.py` on the actual field target was **not run** and must be treated as pending Fable-owned review. Opaque black RGB is the director-approved Bloodright visual appearance and must not be silently changed to satisfy another target. All former 78 recovered approved images and historical BBE visuals remain unchanged; not an 79/87 approved delivery yet. **Live game requests/writes 0/0; credentials none**.
