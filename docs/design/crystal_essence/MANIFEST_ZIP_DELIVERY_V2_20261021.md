# Crystal Essence — five manifest-ready WebPs (v2)

**Date:** 2026-10-21. **User request:** “Approved, give me all 5 in a zip for a manifest.” **Production lead:** Image Production · Art Director.

## Output

**Flat ZIP:** `Crystal_Essence_5_Jutsu_Manifest_Ready_v2.zip` — **688,777 bytes**, SHA-256 `7dd5a25b50077daf68d051b0d10198fc6e47b2910dae9cb49f3c8e208f1c8350`. This is a byte-identical copy of official `jutsu_studio.py finalize` flat distribution artifact `crystal_essence_jutsu_icons_webps_PREFLIGHT_PASS_5webp_v2.zip`. The flat archive has **exactly five root-level .webp members**; CRC verifies. It has NO JSON/readme inside, allowing a clean mobile/WebP picker workflow.

**Companion operator map:** `Crystal_Essence_Manifest_Mapping_v2.json` (separate JSON file). It maps exact jutsu ID/name/rank/BLOODLINE and `jutsu.image` field to WebP file, SHA-256, bytes and 256px dimensions. This is **not a live write manifest**: real uploaded WebP URLs/asset identifiers must come from subsequent operator-approved upload/readback. Do not fabricate URLs or game pushes from filenames.

| Jutsu | Exact jutsu ID | WebP filename in flat ZIP | bytes | SHA-256 |
|---|---|---|---:|---|
| Kōsai Shippū (D) | `igPSz82fa_L2XPrtnMvnz` | `icon_crystal_essence_kosai_shippu_v1.webp` | 132006 | `d898935117d7060301fc33aab6c1d6e3c8ba446f6175abe184e7d9ada493aa38` |
| Crystal Sphere (C) | `zKK0rjIJqbpSiTw7McDAv` | `icon_crystal_essence_crystal_sphere_v1.webp` | 137364 | `01da7cbe28cffcafb4a32af396db9c04f6887ed0a42df7e07d62fe375ec00ec6` |
| Crystal Cave (B) | `AggTDO90TarIRTPqGdvvY` | `icon_crystal_essence_crystal_cave_v1.webp` | 149250 | `08b145a85d9ffe79bad1b02505d1f7e9b935d04e1fbd71a483e4f1f05b72ad6e` |
| Prism (A) | `6XpY1m4rAwrBHBKYsPRDJ` | `icon_crystal_essence_prism_v1.webp` | 125930 | `d3addfc1847cb7b699a69e5969413ce8d1a31be1876a1e78d111167827b2d77f` |
| Summoning: Jade (A) **VISIBLE WARRIOR v2** | `yuJn_D_zPlHV0xJW01JRA` | `icon_crystal_essence_summoning_jade_v2.webp` | 143196 | `2ebe9cc487e7c71852c318688bfdf13c79ac4ab2fa25d3e56054ed32887fb032` |

## Source approval and production evidence

- All five original jutsu IDs/names/types correspond to historical director/source ZIP `BR-020_Crystal_Essence.zip` (source SHA-256 `0a6acc8fb678b1030f1ada358b7fd522cf531b0dfb2f49f2bf0a0a969f5329af`, actual latest local intake 5/5 MANIFEST_VERIFIED, complete mapping, zero issues). Historical source is not a 2026-10-21 live census.
- All five **approved raw** candidates independently received director acceptance; **Summoning: Jade actor-free JPEG v1 was superseded**. Exact revised warrior-containing Jade source is PNG RGB 1254² SHA-256 `0d214b55d628b24dbe76dd690abcbd4ffe993f63080bde977b999a68a7a39e9e`. Director specifically authorized a visible Jade warrior and approved the resulting candidate. See `SUMMONING_JADE_WARRIOR_V2_APPROVAL_20261021.md`.
- **Jade-only target lock v2**, amended per director decision to permit the summoned character, SHA-256 `de06a99cc314e95e8f1a0f554d4340c7ad2dadf85d8e15a2802262271ca7a365`; four sibling locks unchanged. Previous actor-free Jade P0 version 1 is superseded.
- Official Git-pinned `producing-tnr-art` tool bundle validated via doctor: **RUN_CAPABLE_CANONICAL** (Pillow 12.3.0 / libwebp 1.6.0). `jutsu_studio.py intake` exit 0, source-index SHA-256 `b1be52ac3165015bd50deb3b8399be3ada20404d17f92e456a9484083db9e3ee`, five `MANIFEST_VERIFIED`.
- `jutsu_studio.py verify-approved` and `finalize` on the exact five raw files with `--source-index` returned **PASS**; approved ledger SHA-256 `bea8f2e8608b61a7bb1e03e4c68e52b8f5e8423c3deb1dc3f0c3b58a3f46fcf9`. The `--locks` and `--attempts` optional checks were **not invoked in this export run**, so neither is claimed as an executed CLI result for v2.
- All five resulting RGB 256×256 WebPs have **VP8L lossless codec**, and their actual decoded pixels match the approved-source resizing. No quantization and no chroma key; designed opaque backgrounds retained. `artpreflight.py --type JUTSU_ICON` **CANONICAL PASS** on actual outputs, exit 0, **zero errors/warnings**; recorded preflight SHA-256 `2ea1efc19d7142a42f21f22c6d6898ea941f310dd2008a13c48110b36d6ba406`.
- Separate deterministic v2 PNG (not included in flat WebP ZIP) was built from these five exact exports, 3+2 centered; `audit-gallery` returned **VALID, FAITHFUL, CONFORMING**, gallery SHA-256 `a727b41810d7759d8a4c92f5e483e8d42a3cbcbb2dd3508288e927bb37c2e752`. The director's approval of Jade raw is **not acceptance** of the altered five-icon gallery, which is still **PENDING**. Previous accepted member-set/hash would be invalidated even if there were one.
- ZIP is produced and offered for direct download in this chat. `GIT_BINARY_PIN=NOT_PERFORMED` for the new raw/export/distribution binary files; `USER_UPLOAD_READBACK=NOT_PERFORMED`; no in-game uploads or writes.

**Operator next:** Upload each WebP through the existing user-owned game asset process; capture resulting actual game asset URLs/IDs; prepare/validate the `jutsu.image` update manifest from the companion mapping; user approves live pushes. Note the Jade v2 filename is intentionally different from the earlier pre-revision `v1` export.

**Live-game requests/writes: 0/0. Credentials: none.**
