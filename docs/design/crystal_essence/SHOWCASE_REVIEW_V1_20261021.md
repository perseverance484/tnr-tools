# Crystal Essence — five-jutsu showcase review v1 (2026-10-21)

**State:** **ALL FIVE ORIGINAL RAW CANDIDATES DIRECTOR-APPROVED / OUTPUT_LOCAL_QC PASS / CANONICAL_PREFLIGHT PASS / DETERMINISTIC GALLERY AUDIT VALID / FAMILY SHOWCASE ACCEPTANCE PENDING**. The director approved the final Summoning: Jade raw and asked **"Create showcase png"**, *not* "I accept this exact gallery". No in-game actions occurred.

## Source and approved member ledger

- Bloodline: Crystal Essence (A), `ssevlOGQ4JjPn2sHZtq0c`, BR-020.
- Prior original-art ZIP: `BR-020_Crystal_Essence.zip`, SHA-256 `0a6acc8fb678b1030f1ada358b7fd522cf531b0dfb2f49f2bf0a0a969f5329af`, N=5, five exact IDs/names `MANIFEST_VERIFIED` against historical read-only `jutsu.get` capture. Not a fresh current-live census.
- Approved target locks: all 5/5 `DIRECTION_APPROVED` with exact Git lock blob `d89496208992bcb865bb9cd78f1e25f742207911`; local source-index SHA-256 `469a07aa25b5299af3aa5aff953c73b4dc173fe6f23605fb6787476c0ab30a39`.
- Approved raw bytes: all five true-format **JPEG RGB 1536×1536**, each manually accepted by director, individual approval docs already recorded. The incoming filenames ending in `.png` contain JPEG bytes; a `.jpg` alias has exactly identical bytes. Final **Summoning: Jade raw** (incoming `1000018983.png`) SHA-256 `cd26fffc70e4a6bd831a296bed8face1bf15dcb122ff6f0d16c6ee45fb4363c3`, director evidence `SUMMONING_JADE_RAW_APPROVAL_20261021.md`.
- Five **unmodified approved raw originals** were exported via the official `jutsu_studio.py finalize`, with **Pillow LANCZOS 1536→256 RGB, lossless VP8L WebP (`method=6`)**, no opacity stripping, destructive quantization or generative modification. The approved raws themselves are unchanged. Version `v1`. `family_byte_cap_exclusive=null` (BBE-only 80 kB cap does not apply).

| Exact jutsu | ID | Approved raw SHA-256 | Exported 256px VP8L WebP | WebP bytes | Export SHA-256 |
| --- | --- | --- | --- | ---: | --- |
| Kōsai Shippū (D) | `igPSz82fa_L2XPrtnMvnz` | `84a523fbc5fab3e3eb6f43ff3bf88682643477cf54154d1e0bc3b151353f8ee5` | `icon_crystal_essence_kosai_shippu_v1.webp` | 132006 | `d898935117d7060301fc33aab6c1d6e3c8ba446f6175abe184e7d9ada493aa38` |
| Crystal Sphere (C) | `zKK0rjIJqbpSiTw7McDAv` | `077cff98ed9767e673da0aef3a9f95cd7817b2d026c9ac82cdbcfa697ce986c4` | `icon_crystal_essence_crystal_sphere_v1.webp` | 137364 | `01da7cbe28cffcafb4a32af396db9c04f6887ed0a42df7e07d62fe375ec00ec6` |
| Crystal Cave (B) | `AggTDO90TarIRTPqGdvvY` | `223af5ff36f525cfc93b4df798388f4c1925fe78809efd462c5bcd60a5e1cc34` | `icon_crystal_essence_crystal_cave_v1.webp` | 149250 | `08b145a85d9ffe79bad1b02505d1f7e9b935d04e1fbd71a483e4f1f05b72ad6e` |
| Prism (A) | `6XpY1m4rAwrBHBKYsPRDJ` | `139b38821597ea04ccf0550a5ef72c19b7c16c739c47cab611773a82ef2380d1` | `icon_crystal_essence_prism_v1.webp` | 125930 | `d3addfc1847cb7b699a69e5969413ce8d1a31be1876a1e78d111167827b2d77f` |
| Summoning: Jade (A) | `yuJn_D_zPlHV0xJW01JRA` | `cd26fffc70e4a6bd831a296bed8face1bf15dcb122ff6f0d16c6ee45fb4363c3` | `icon_crystal_essence_summoning_jade_v1.webp` | 141678 | `2aa3b5ae715b09a9763d01139ccf5a41cefaaf24d5ad64ea82026a32bdb57adb` |

## Official mechanical evidence (local, not Git binary-pinned)

**Verified art tool:** official `dist/producing-tnr-art.zip` bundle (SHA-256 `73dd4228131dc8cbf112fc89466160eb604857c856419db5e664bc516a0727ed`, Git blob `746a4460b59bb8b805bdd64837f738b3618d0b82`); `jutsu_studio.py` blob `952236b57017930338e24dd1ddeb1840b6a0895b`. Pillow **12.3.0**, libwebp **1.6.0**.
- `jutsu_studio.py doctor`: **RUN_CAPABLE_CANONICAL** (exit 0). Actual `lock-check`: **exit 0, 5/5 DIRECTION_APPROVED** against intake index.
- `jutsu_studio.py verify-approved approved.json --source-index ... --locks ...`: **exit 0, N=5/5 RAW_VISUAL_APPROVED**, five verified exact incoming-byte hashes. No fabricated per-generation `attempts.json` was supplied; `--attempts` not passed (optional), so it was **NOT_VERIFIED**.
- `jutsu_studio.py finalize approved.json --out final --label v1 --source-index ... --locks ...`: **PASS**, five RGB square lossless VP8L WebPs, each **256×256**, all spec byte ceilings PASS, pixel-equal decoder round-trip on actual outputs. `export_qc_v1.json` all five `PASS`, encoder repeatability probe PASS.
- **Actual pinned `artpreflight.py --type JUTSU_ICON`: canonical PASS**, exit 0, **0 errors, 0 warnings**; canonical pins `artpreflight.py` Git blob `71ed409853c8b3da6f5b66c5c3db5ab2c9274bb4`, art spec `8536cd9b81da4c8f88a095af89026437a25a2c15`, from pinned main `f620db3d934fbb5a13effa5f90ed25bf16a33718`.
- **Official deterministic full family PNG:** `crystal_essence_jutsu_showcase_v1.png`, **1162×912**, 3+2 **centered** arrangement, 350px equal square tiles, 28px gutters, label bands with exact names/export sizes, source artwork only from **actual five exported WebP bytes**; PNG SHA-256 `5e41ef69da7d829d1391e916e243211d9cfb2e741240ea9c5fba7a9c39f524a4`. **Gallery manifest SHA-256** `ef450fc22c81458bc7161ba2b4a2c226fce67d0fef97f56673e20a81aa512420`; **decoded gallery pixels SHA-256** `dd596c90dac5f7dcba45edcdb9bc14f01a4f5c69c2b833477ac66483d4d33c71`; **member-set commitment** `a0adc8588fcf62210c67f3d204dfbadc92b7a7631d8fb8a3cf1a53ad1fcb9153`.
- **Independent official `jutsu_studio.py audit-gallery`: VALID, tile `pixel_fidelity=FAITHFUL`, `layout=CONFORMING`**, gallery file hash verified. Full collection 125/64/32 thumbnail QC SHA-256 `dc686e4ea9181cd758df32a441a826ad198dddb56120ae8bdf22a16c2797615f`.
- Generated read-only delivery candidates locally: `crystal_essence_jutsu_icons_closeout_v1.zip` SHA-256 `804f09a864549e97fb24f34597ece976040765e8bd52ffc50641d664c2550414`; flat `crystal_essence_jutsu_icons_webps_PREFLIGHT_PASS_5webp_v1.zip` SHA-256 `a74c18cc75dbc4741a0f7831edcfe948753b2febea5f074d3831c6abbd8d0b98`. No gallery acceptance/upload asserted; packages remain local until appropriate handoff.

## Caption font defect — explicit separate review preview

The canonical P1 CLI `jutsu_studio.py` uses Pillow's **default font**, which lacks visible glyph support for the macrons in **Kōsai Shippū**. The **canonical `audit-gallery VALID`** PNG therefore contains replacement/tofu glyph boxes in that name, despite the manifest carrying the exact Unicode name. This is a real **display quality defect in captions**, **not** an artwork-tiles problem; do not silently claim the published caption is correct.

A second file `Crystal_Essence_Jutsu_Showcase_Readable_Review_v1.png`, SHA-256 `86bac476ccf3d5490a93820999de2d09efeca419a0811bd2291e95d7ef17b6a5`, was made as a **non-generative readable-caption REVIEW preview**: only the label bands were re-rendered deterministically with an installed Unicode-capable DejaVuSans font; all **five art tiles were independently compared byte-for-byte at the decoded-pixel level** against exact LANCZOS resizes of the five exported VP8L WebPs, and tile geometry/layout match the canonical gallery. **This readable-preview PNG is NOT itself the exact canonical P1 audited gallery and has NOT passed official `audit-gallery`**; never substitute its hash for the canonical gallery hash. It must remain **REVIEW ONLY** unless Fable updates the canonical caption font handling under the separate Lane A implementation/review process and the fixed gallery is re-built/audited.

This issue is for future tool/UX follow-up: a correct readable final gallery must support diacritics in exact names **without** touching the approved artwork pixels, compromising exact export-byte ties, or weakening `audit-gallery`.

## Current acceptance boundaries / next action

`ORIGINAL_SOURCE_VERIFIED=VERIFIED 5/5`, `DIRECTION_APPROVED=APPROVED 5/5`, `RAW_VISUAL_APPROVED=APPROVED 5/5`, `OUTPUT_LOCAL_QC=PASS 5/5`, `CANONICAL_PREFLIGHT=PASS`, **`FAMILY_SHOWCASE_ACCEPTED=PENDING`**, `ZIP_DELIVERED=BUILT_NOT_DELIVERED`, `GIT_BINARY_PIN=NOT_PERFORMED` for raw/export/gallery files, `USER_UPLOAD_READBACK=NOT_PERFORMED`.

Next: director reviews exact gallery, but **do not bind an ACCEPTED verdict to the readable preview** or assume the canonical tofu-caption PNG is visually acceptable. Prefer approved tooling font-glyph repair and subsequent fresh canonical audit before final exact-member/gallery director acceptance. Until then, the true status is **VISUAL_REVIEW_AVAILABLE / OFFICIAL SOURCE-TILE AUDIT PASS / EXACT FINAL SHOWCASE ACCEPTANCE PENDING**.

**Studio did no image generation. Live-game requests/writes: 0/0. Credentials: none.**
