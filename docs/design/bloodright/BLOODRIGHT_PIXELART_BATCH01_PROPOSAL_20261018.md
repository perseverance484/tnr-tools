# Bloodright — Premium Pixel-Art Style Unification, Batch 01 (10 Proposals)

**Date:** 2026-10-18. **Status:** FIRST 10 INDIVIDUAL STYLE-REVISION IMAGES PROPOSED, **0/10 NEW VERSIONS DIRECTOR-ACCEPTED**. Earlier bloodline/tier visual approvals remain untouched. **Lead:** Image Production · **Support:** Art Director.
**Repository:** `perseverance484/tnr-tools`; branch `chatgpt/bloodright-pixelart-wave01-20261018`; parent `chatgpt/bloodright-wave06-art-studio-20261018@b9150dd7c05701fe443c8b41472a2cfc9744057a`.
**User visual direction:** premium TNR Ghost-Ship-quality pixel art, **no inherited Ghost Ship color or subject palette**, crisp clustered pixels/cel material separation, strong tier silhouette/negative space, controlled edge highlights, **no default sparkles, floating glitter or decorative VFX**. User authorized first batch of up to ten. Final revisions need **fresh director visual approval**.

## Honest original-art recovery boundary

Source for all ten actual approved icon bytes: exact `Bloodright_Wave06_Production_Starter_20261018.zip` SHA-256 `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`, containing the 15 Wave05 approved **256×256 VP8L lossless WebP** comparators. All 10 specific archived source files were extracted without changes and preserved inside the proposed portable pack, per-file SHA recorded in `PROPOSAL_QC_MANIFEST.json`.

The first 10 in this session are **ten byte-recovered, already-approved Wave05 comparison icons**, not silently described as the first 10 chronological designs in the complete 87-icon roster. Earlier Wave01–04 original binary archives are **not present in this conversation container, nor Git-pinned**, and may require separate operator archival intake before safe conversion. We intentionally skipped `BR-005 Arashima Stormcloud V02` because its accepted art is already **nonexact** to the universal raw mask and must not be silently reshaped or swapped. We chose three geometry-regular complete families plus one next-family Foundation:

| Family | Icons transformed | Existing accepted material preserved |
|---|---:|---|
| BR-078 Tenohira Musei | 3: Foundation, Hidden Art, Advanced Art | dual azure + ember Equinox Rift |
| BR-065 Shinrai Ou | 3: all tiers | white-cobalt conductor Raijin Whitebolt |
| BR-034 Hyouga Yui | 3: all tiers | deeply saturated cerulean fractured ice |
| BR-077 Teno Yuki | 1: Foundation only | pale Winterglass Sanctum frost |
| **Total** | **10** | No color/theme restrictions imported from Ghost Ship |

The user-approved raw 1254px art, where historically available, has **not been recovered for these ten in this conversation**. These are honest original-approved-WebP-to-new-256px style **proposal translations**, not a claim of perfect high-resolution art regeneration. The project repo's `house_style` clauses support crisp pixel linework / flat cel-shading / limited palettes, but **no exact individual Ghost Ship art exemplar was supplied or verified here**, so the Ghost Ship match is **a qualitative target, not a measured historical-pixel equivalence**.

## Processing and non-generative geometry safety

Processing source file: `tools/produce_batch01.py` inside portable ZIP; no original member is overwritten. Derives one limited shared chromatic palette **per bloodline** from the three actual approved 256px inputs; combines **128px working pixel-cluster grid → 256px nearest-neighbor**, source-driven stepped cel contrast, clipped tonal changes. It adds **no particles, effects, borders, words, rune changes or newly lit background pixels**. All colors are sourced from each family's original approved work; Ghost Ship palette not imposed.

- All 10 candidates are individually saved **256×256 RGB PNG and RGB lossless VP8L WebP**. Decoder/readback pixel equality with PNG: 10/10 exact; RIFF chunk `VP8L` verified.
- Every output channel value outside its source's >5 brightness support is **zero**: 10/10 **zero newly lit pixels outside original source support**. Main negative-space holes remain black. The original source is never in-place overwritten.
- A brightness-change check (expected during pixel remastering): **minimum IoU 0.92759 at intensity threshold 32** over all ten icons. Do **not** misrepresent this as pixel-exact 1254px master geometry preservation or mask identity at every brightness level. Geometry is source-contained but stylized output still requires director visual review.
- Lossless output file sizes span **3,850 to 12,660 bytes** (generic 460,800-byte ICON reference ceiling check passes); 125/64/32 thumbnails made from actual saved candidate WebPs. **No successful field-specific `skillTree.image` preflight** is claimed.
- Source originals were Wave05 art visual-approved. **New pixel versions 0/10 approved**; small-size stress preview is a mechanically composed sheet, not standalone director signoff.

## Portable artifacts / provenance

| Artifact | Exact SHA-256 | Purpose |
|---|---|---|
| `Bloodright_PixelArt_Batch01_10_PROPOSED_20261018.zip` | `089f0bbf2f848306d5579fb3e5cbf1d7a7b1210c320327dc948e7edef5a50780` | 10 exact source WebPs, 10 proposed PNGs, 10 proposed lossless WebPs, producer code, manifests and display QC |
| `Bloodright_PixelArt_Batch01_10_WebPs_PROPOSED_20261018.zip` | `111d4fc135b49866e153724b32a5528e0ba21923020d4c1d6c4f9255d525f6bf` | 10 individually accessible proposed game-sized VP8L WebPs |
| `qc/Bloodright_Batch01_10_Pixel_Art_Proposals.png` | `92a6c8a1242d490d40500eec0e0ac5b75a39c402caf018db80fdbde0b2f2bb77` | Non-generative visual sheet built from exact candidate pixels |
| `qc/Bloodright_Batch01_10_125_64_32_QC.png` | `e0ea43fe7e93ad15a0c57ca7d8041735fe35dde3e45ce39ddd8d757acdf9270d` | Small-size stress view |
| `qc/Bloodright_Batch01_10_Before_After.png` | `96ecb8504d2de75b515879d65a157c022fe0e3a02d903b817dbc14ae81710566` | Approved earlier WebPs beside exact candidate revisions |
| `qc/PROPOSAL_QC_MANIFEST.json` | `b933294897f3ad751d6402402c16d7930167f2cfb6f62460b911d7c8613b23ed` | Detailed per-icon source/output file names, SHA, codec, size, mask IoUs and status |

**Image-generation exploratory gallery:** a separate style ideation render introduced new pictorial subjects and ornate UI frames. Its geometry and characters **DO NOT match the fixed Bloodright tier masters**, so it is intentionally **REJECTED AS SOURCE ART**, excluded from these packages and not treated as approval evidence. The ten actual proposed candidates in the ZIP are sourced from the approved individual icons and mechanically constrained instead.

## Director gate / workflow safety

**Next:** review this ten-image pixel-art conversion together at 125/64/32. Director can accept the common pixel rendering style, request higher detail/bolder cel facets/cleaner contrast, or reject it; **do not run the other ~77 transformations before style direction/quality is settled**. If approved, obtain existing accepted art binary packs for first 1–20 icons in chronological roster before production, and continue with a consistent split between art revision, geometry checks and formally valid game import files. No original accepted SHA changes and no unauthorized write to Fable's branches.

**Unresolved cross-cutting blockers unchanged:** Itojinsei Blackwire accepted composite lacks three independent geometry-verified sources; 12 earlier visually approved icons nonexact original high-res masters; `skillTree.image` RGB opaque field/preflight semantics; immutable art Git binaries; Forge imagePack; independent art-lineage ruling-ID collision with main. No claim of in-game wiring, import, update, live readback, publish or active deployment. **Live-game requests/writes 0/0 · Credentials none.**
