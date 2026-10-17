# Bloodright Tier-Emblem Art — Wave 04 Closeout

**Status:** CLOSED — all 5 family trios and 15 separate tier emblems **director VISUALLY APPROVED**; archive/export QC PASS; strict pixel-master geometry **6 PASS / 9 FAIL**; game-field and Forge delivery gates OPEN.

**Date:** 2026-10-17.
**Repository:** `perseverance484/tnr-tools` · `chatgpt/bloodright-wave04-art-studio-20261017`.
**Base:** `chatgpt/bloodright-wave03-art-studio-20261017@47e6a374478654d93fdf7d6d15e3f1ee68730955`.
**Main last verified:** `9a0970002a80531078ac5e4b0f72578d3f7855f5`; merge-base `99e86dc549b86f1f4a5846c0e509fa6bc15b3463`; this art branch is not an approved integration candidate.
**Canonical art evidence:** `BLOODRIGHT_WAVE04_APPROVED_QC_20261017.json`; per-family SHA ledgers `BLOODRIGHT_WAVE04_BR066_APPROVED_QC_20261017.json`, `BR008_REVISED_APPROVED_QC`, `BR053_PROPOSAL_QC`, `BR063_EBONY_SILK_APPROVED_QC`, `BR032_PROPOSAL_QC` under `docs/design/bloodright/`. Visual progress tracked in `ICON_PRODUCTION_TRACKER.md`.

## Five accepted families

| ID | Family | Approved treatment | Director art accepted | Pixel-exact original master |
|---|---|---|---|---|
| BR-066 | Shinseina Ki | Verdant Heartwood | 3/3 | **FAIL 3/3** |
| BR-008 | Bakuhatsu | Detonation Core — bright red-edge/white-core V02 | 3/3; V01 rejected | **FAIL 3/3** |
| BR-053 | Oblivion Seal | Voidscar Amethyst V02 | 3/3 | **PASS 3/3** |
| BR-063 | Shadow Weaver | Ebony Silk V03 | 3/3; white/violet alternatives rejected | **FAIL 3/3** |
| BR-032 | Heavenly Sonata | Celestial Harmonics | 3/3 | **PASS 3/3** |

**Wave 04 visuals: 5/5 families, 15/15 icons. Overall: 20/29 families, 60/87 icons (68.97%). Remaining: 9 families, 27 icons.** Approval of accepted artwork does not imply machine geometry or upload readiness.

All 15 high-res 1254×1254 RGB original PNGs and 15 WebP 256×256 lossless RGB VP8L exports preserved byte-identically from director-accepted images. Heavenly Sonata's metadata-only approval update preserved all six earlier proposed PNG/WebP members unchanged; the normalized current manifest contains original-proposal hash provenance. The original 5 source art ZIPs contain 25 jutsu reference icons and five identity images, but no individual jutsu icon was redesigned. The full 5×3 showcase and multi-size review were assembled **programmatically from accepted original pixels**, not generated interpretations.

## Verified conversation deliverables (not Git-pinned assets)

| Asset | SHA-256 |
|---|---|
| `BR-032_Heavenly_Sonata_Bloodright_Approved_3_Icons.zip` | `91ea1253be0762f17c45f622a4b323ceefda2c9bcdf91aa1a16a817742e637ef` |
| `Bloodright_Wave04_Approved_All_5_Bloodlines_15_Icons_20261017.zip` | `ff6df940762527f1d9e8e083b93989de26379224f858266a04fae15d93cffd38` |
| `Bloodright_Wave04_Approved_15_WebPs_256px_20261017.zip` | `7270fa9bd79f4171724031207fd3b3d84eb0057322875a9e8c1824f4aa093d51` |
| `Bloodright_Wave04_Approved_Showcase_20261017.png` | `31775e64947bda98a22956e99a74f3c46afbf13177b9de9d4c5fc9a86ae8458d` |
| `Bloodright_Wave04_Approved_125_64_32_QC_20261017.png` | `4d93c07372f25c4e2c661693f0ee9c9a8f64ad48582ca5ebb2e0cd42ca8277a8` |

**QC:** 510 offline checks passed, 0 failed: all five source art ZIP SHA/CRC checks, 15 raw PNG source hashes, 15 lossless WebP export hashes, decoded WebP pixels equal to Lanczos-resized raw, <460800 byte working ceiling, black corners, precise expected master geometry PASS/FAIL and output archive memberships, plus programmatically composed comparison checks. Report: conversation artifact `Bloodright_Wave04_Approved_20261017/WAVE04_APPROVED_QC_REPORT.json`.

### Technical gates — not waived

1. **Strict geometry:** Nine visually accepted freeform images are **not** pixel-exact universal masks (all Shinseina/Bakuhatsu V02/Shadow Weaver V03). Preserve accepted originals; changing pixels requires new user visual acceptance. Do not automatically remask or substitute rejected versions.
2. **Formal game field:** `skillTree.image` validator/preflight remains unverified. The `jutsu.image`-only `JUTSU_ICON` optional alpha rule does not authorize opaque RGB Bloodright skill-tree art upload; generic ICON alpha contract conflict remains open.
3. **Immutable evidence/operation:** Original approved binary assets, exact geometry masters and source packs are **not Git pinned**; immutable Forge imagePack/structural validation and operator-controlled hidden import/readback/publication are **not done**. Fable remains technical implementation owner. User remains final authority over live game operations.
4. **Integration:** Art branch `RUL-2026-10-17-004` (reskin factory) and `main`'s `RUL-2026-10-17-004` (placeholder element import) disagree in ID ownership; reconcile without overwriting either ruling before proposing a merge.

**Game requests/writes: 0/0. Credentials: none.**

## Wave 05 next (not yet art-generated)

From the approved tracker: BR-078 Tenohira Musei (Yin-Yang), BR-005 Arashima (Storm), BR-065 Shinrai Ou (Storm), BR-034 Hyouga Yui (Ice), BR-077 Teno Yuki (Ice). Each A-rank with 5 documented original public jutsu. **Obtain the actual five original jutsu-art ZIPs and inspect exact images** before approving any treatment, particularly the matched storm pair and matched ice pair. The current source-art archive does NOT contain these five Wave 05 families. Portable starter `Bloodright_Wave05_Production_Starter_20261017.zip` SHA-256 `5054109d3142154f668ba60d8b0d201971d4b2a2e03fcf6f408dbf5568605a4b` carries the three verified masters and 15 Wave04 accepted WebP comparison icons only.
