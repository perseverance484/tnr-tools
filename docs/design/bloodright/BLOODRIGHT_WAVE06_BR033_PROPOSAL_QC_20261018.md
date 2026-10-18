# Bloodright Wave 06 — BR-033 Houkyuken Ferroflux Polarity v02 Proposal

**State:** MATERIAL DIRECTION **DIRECTOR APPROVED** (2026-10-18); the actual three tier-icon images are **PROPOSED — AWAITING DIRECTOR VISUAL ACCEPTANCE**. No source-art or export-image acceptance may be inferred from the direction approval.
**Lead:** Image Production · **Lens:** Art Director.
**Production branch:** `chatgpt/bloodright-wave06-art-studio-20261018`; parent Wave05 closeout `5512aa0e8faad6153e13122c262e5277e58c6a08`; material approval `c2651f7067be8f1be5d05e1d5568e53007f51e2a`.

## Approved direction and candidate method

- Director-approved **Ferroflux Polarity** for **BR-033 Houkyuken**, drawn from four visually inspected original jutsu/identity images in `BLOODRIGHT_WAVE06_SOURCE_INTAKE_20261018.md`.
- Opaque black background; geometry-locked nested pointed diamond, inward crescents/crosspieces and sharp starburst in Foundation/Hidden/Advanced respectively. Same cross-woven magnetic-polarity treatment on all three: hard scarlet red against cold blue-cyan over dark conductor facets. This is distinct from previously accepted BR-078 Tenohira Musei's left/right blue/orange split. **No jutsu icons are being replaced.**
- Deterministic offline image production from the starter's **three exact individual 1254×1254 tier geometry masters**; no generative sheet and no hand-redrawn silhouettes. A first private v01 looked too peach; only v02 is presented for director review.
- The v02 recipe preserves **every individual pixel's master `max(R,G,B)` intensity exactly**, rather than merely an approximate silhouette mask. Nine binary intensity masks tested at 1/8/16/32/64/128/192/240/254; equality PASS 3/3 × all thresholds.
- Exact source geometry masters: Foundation `bb3a3e331e5913fa527049980e2738c151b85eb54ef579cd468126b10039cea2`; Hidden Art `97ac6df359070f885d8d5545060b788bbd8d374fdfd181c90c60976560a213fc`; Advanced Art `0e97566732f8ade28eedb1b18f77a666b9804f9467198f9574e3757d940cd014`.
- Verified operator ZIP `BR-033_Houkyuken.zip` SHA-256 `b2c9d2f1f15a30e0bbe2284a145aadc5b1e15a91757d44281ec2c6f74f11b343`; approved-source starter SHA-256 `9898257e9ab3bc03e2339c4cb3ee6ae228643a362e18e4de271ea40be5d4938e`. The portable proposal ZIP includes both exact original reference archive and all three masters.

## Independent offline export QA

**96 assertions PASS, 0 FAIL**, on a second read-only auditor distinct from the icon producer. Checks: source/geometry input SHA, original ZIP safety and CRC, 3 exact master whole-pixel maxRGB geometries, 27 threshold mask equalities, raw PNG RGB/1254px decoder, 3 256×256 opaque RGB lossless VP8L WebP containers, decoded WebP pixels exactly matching intended Lanczos resizes of exact source PNGs, black/near-black corners, **460800-byte reference ICON ceiling**, 125/64/32 px resized contrast, archive CRC, 16 exact expected ZIP members, and all 3 raw/3 exported image member SHA integrity. This is offline validation of source/file geometry, **NOT** a formal `skillTree.image` field preflight.

| Tier | Raw PNG SHA-256 | WebP SHA-256 | WebP bytes | Exact master geometry |
|---|---|---|---:|---|
| Foundation | `a6188df598e10979e1a74ab49ad81d89a0a3b409d6f955c116dbe14213e51f45` | `70035a46420660ef2fbacca62926aead7bf26de4a8489cbdbba9d67e0fc8eebb` | 42,818 | PASS |
| Hidden Art | `d6487f3bfbe9ed2924e60642da167ad9007365fed84b117414e8b671639e85c6` | `19fa3844e04c8ce42534f95d40809d8f8beeeb515def72c9b18676091dc77f9b` | 69,280 | PASS |
| Advanced Art | `7e5b510d1a16210b921c3e63388ac56b0a50fbf12b29aef09a699f4da8bb30f2` | `e3d9d4ad3dc83211652c9c565d343bcb601333a5d36c4408466854e9d7b23a1a` | 59,602 | PASS |

**Exact portable conversation artifacts (not Git-pinned binaries):**

- `BR-033_Houkyuken_Ferroflux_v02_Proposed_Production_Pack_20261018.zip`: SHA-256 `c56140a7c5e704b367951b87495837867924c784e284a8c9b174bc1442cfb8cb` (16 entries: three geometry masters, source ZIP, recipe, three independent PNGs, three independent lossless WebPs, QC report, manifest intake audit, two non-generative QC previews, README). Internal QC ran 83 prepackaging checks; external QC added 13 ZIP/member checks = 96 total.
- `BR-033_Houkyuken_Ferroflux_v02_3_WebPs_PROPOSED_20261018.zip`: SHA-256 `544c3102637f816e7d9d74c33be10585b66bf1c631bf028f0c99db304d481ae2`.
- `BR-033_Houkyuken_Ferroflux_Three_Tiers_PROPOSED_v02_20261018.png`: SHA-256 `e91f070207141795ddcde66d4deba9a35f1fce8733bd10c33bc7a146cb1ec68a`.
- `BR-033_Houkyuken_Ferroflux_vs_Tenohira_Comparison_20261018.png`: SHA-256 `31eb498c5e8c48c257ee72fe52757fd6cc51ee7afee3ce05809f29a9151681b2`.
- Producer script within archive SHA-256 `afc88ed067b996f8cf3c7615d35cc35e553844b3bbd4479a18d154fdd2365c82`.

## Required decision and technical boundary

**NOW:** request the director's visual approval/rework of this specific three-artwork v02 trio. If approved, lock these exact raw and WebP SHA-256 bytes, then proceed to Itojinsei under the already-approved wave direction.

**OPEN, do not claim green:** `skillTree.image` specific image/alpha acceptance and production `artpreflight.py` unresolved; generic `ICON` still requires alpha whereas director-approved Bloodright icons have intentionally opaque black backgrounds. No independent field-specific preflight was run here. Forge imagePack, Git immutable binary source pinning, any prior 12 visual-approved Wave04/05 geometry discrepancies, and historical art-lineage-vs-main ruling-ID conflict remain unresolved. The candidate is **NOT upload-ready**, regardless of offline pass.

**Live-game requests/writes: 0/0 · Credentials: none.**
