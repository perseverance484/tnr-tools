# Shinseina Ki — Jutsu Icon Register

**Studio:** Persistent ZIP-first Art Studio, not Bloodright tier emblems.
**Lead:** Art Director; **support:** Image Production.
**Director decisions (2026-10-19):** Sacred Heartwood family treatment and all five technique silhouette reservations APPROVED; all **five individual original image raws visually approved (5/5)**. The deterministic processed family gallery is **PENDING exact director signoff**. Do not confuse these gates.
**Studio baseline:** `main@4e674234d0539b7010c34025034330980a38b196`. No live game requests.
**Family:** Shinseina Ki / BR-066 / A rank / bloodline ID `vA8I_7iBNgvkuKOpnG1yD`.

## Evidence and limits

- Original source ZIP: `BR-066_Shinseina_Ki.zip` SHA-256 `7b5260dd7f2e389763d3339edb967c08485b29426a143f02df255da0fbba0e39`; safe canonical intake, CRC, decoding and five exact ID/name mappings PASSED. Captured evidence is **historical**, not current-live verification.
- Historical dossier: `docs/design/bloodright/kits/shinseina_ki.json@7c1dfdd5e3ee163b90c22694dbb2de94ede08866` (2026-10-01). October 17 read-only `jutsu.get` capture: `harvests/inbox/tnr_results_1792216630441.json` (blob `2a0d87ccc947271701462c24d4de428cf0b0532a`), via `push/107_bloodright_reference_capture_batch_4.json`. IDs, names and BLOODLINE type match. Classification differs between historical sources for four jutsu; preserve as an evidence discrepancy, not an art identity mismatch.
- Production authority: `docs/workflows/ISOLATED_ART_GENERATION.md` (P0 A–F), `docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md`, `docs/workflows/JUTSU_ICON_SHOWCASE.md` and `skills/producing-tnr-art/`.
- Tooling: `jutsu_studio.py doctor` RUN_CAPABLE_CANONICAL on 2026-10-19; canonical ZIP intake passed. Doctor does **not** certify final exports.
- No current-live request, live write, upload, credential or publication is authorized.

## Family treatment — APPROVED

**Sacred Heartwood:** dark amber-gold interlocked heartwood and umber bark, jade/emerald chakra moving through fractures, restrained warm-gold highlights; deep charcoal/forest-black designed backgrounds; premium crisp pixel-art/cel-shaded rendering. Wood is the owned combat material, not an obligation to produce generic forest scenery. Technique-first, opaque backgrounds allowed, no actors/anatomy unless an individual exception is approved, no glyphs/runes/spell circles/text/UI.

## Five techniques and reserved silhouettes — family reservations APPROVED

| ID | Jutsu (rank; type) | Dominant action and silhouette | Camera / motion axis | Supporting effect | Excludes |
|---|---|---|---|---|---|
| `8MRWPNK3lOxCLVqWrE-xJ` | **Exploding Wood Serpent** (B; BLOODLINE) | A segmented **S-shaped wood strike** hurtling forward and detonating | Three-quarter; lower-left → upper-right | Amber bark splinters at impact, narrow jade fissures | All arches/prisons, flat disk, rising wood armour, endless corridor |
| `6jxreCs3oWJ9sKPB9Sw4b` | **Guardian's Grove** (B; BLOODLINE) | Thick **U-shaped/arched root cavern** closing around a poisoned trap | Three-quarter inward view; both walls squeeze toward center | Poisonous emerald haze contained within opening | Serpent, disk, upright guardian, repeating corridor |
| `zZ-QZGRXC-aUiskpZ4Z_3` | **Forest Wisdom** (D; BLOODLINE) | Physical **heartwood growth-ring cross-section** accumulating self-enhancement | Close elevated view; chakra concentrates inward | One small stored jade chakra pulse | Serpent, cavern, armour, corridor |
| `LnzsA7WDqi06AU0s7yrVP` | **Wood Style: Wood Warrior Summon** (A; BLOODLINE) | A single **upright armour-like heartwood pillar** assembling from erupting roots | Frontal three-quarter; vertical emergence | Narrow lit joining seams | Serpent, cavern, flat ring, corridor; no literal warrior anatomy yet |
| `D3t1nlaVAw8kLfjDO5Wvy` | **Eternal Forest** (A; BLOODLINE) | Vast **V-shaped repeating tree-wall corridor** closing toward distant space | Look down long corridor; walls converge inward and into depth | One jagged woody fracture indicating attack | Serpent, U-shaped immediate cavern, disk, guardian |

Lookalike action/silhouette is a failure even if palettes differ. Stress-test 125/64/32px. BBE's under-80,000-byte rule does **not** apply automatically.

## Raw visual approvals — 5/5

All five user-approved source image uploads are decoded JPEG RGB 1536×1536 despite their `.png` upload filenames. The exact uploaded bytes were preserved unmodified under accurate `.jpg` file extensions; raw/attempt generator-native provenance remains UNVERIFIED and should not be silently invented.

| Jutsu | Exact approved raw SHA-256 | Director raw | Local export QC | Canonical preflight | Final family acceptance | Git binary pin |
|---|---|---|---|---|---|---|
| Guardian's Grove | `814225c19ea175f0eefd71bc747b1d69cdd5b170b76b5d6b9971b8e68dffeff8` | APPROVED | PASS | PASS | PENDING | NOT_PERFORMED |
| Exploding Wood Serpent | `311dd5adbd377cf1189ffdd6c990a1aab7a9667fffc032083fac90254e626d54` | APPROVED | PASS | PASS | PENDING | NOT_PERFORMED |
| Forest Wisdom | `9d2d1077c62ec9f375b82deff148fa9b3efc347c965e50e56d6d1344ef181556` | APPROVED | PASS | PASS | PENDING | NOT_PERFORMED |
| Wood Style: Wood Warrior Summon | `fc930c256b259328336dd48e068b4f28417bf7f090a39155686bda1bd9454086` | APPROVED | PASS | PASS | PENDING | NOT_PERFORMED |
| Eternal Forest | `156cf603e729c96fa2a28a427b0e94040bb7d51a201d485c84e184f937e5b8ff` | APPROVED | PASS | PASS | PENDING | NOT_PERFORMED |

**Eternal Forest evidence:** 2026-10-19 director supplied `1000018844.png` and said “Approved, next”. Decoded JPEG 1536×1536 RGB, 848808 bytes. The resulting V-shaped long converging timber corridor is different in perspective/action from Guardian's Grove's compact U-shaped poison trap. This specific image is visually approved; not yet user-accepted as part of the complete processed gallery.

**Wood Warrior anatomy exception gap:** The approved Wood Warrior image visibly depicts a guardian with head-/shoulder-/arm-like structures, contrary to the pre-generation lock's explicit no-anatomy restriction. Preserve the original lock, the director's individual visual approval, and this conflict. Do **not** treat the approval as permission for anatomy in other jutsu; director can explicitly confirm this **specific** image's anatomical exception at the gallery signoff. Until then, separate formal exception evidence is OPEN.

## Canonical mechanical processing — 2026-10-19

- **Tool:** Official `jutsu_studio.py` 1.1.0, doctor RUN_CAPABLE_CANONICAL; self-tests 191/0; `artpreflight_selftest` 98/0. Five-source roster and all five hash-bound direction locks checked.
- **Approved raws:** 5/5. The `tnr.jutsu-studio.approved/1` ledger records each user's individual approval, exact raw SHA, no quantization, no family-specific byte cap.
- **Export:** Five square opaque RGB **256×256 lossless VP8L WebPs** using LANCZOS resize from exact approved sources. Five export/local decoder/pixel checks PASS; no creative edits, quantization or keying.
- **Canonical `artpreflight.py --type JUTSU_ICON`: PASS, exit 0.** Exact script blob `71ed409853c8b3da6f5b66c5c3db5ab2c9274bb4`, art spec blob `8536cd9b81da4c8f88a095af89026437a25a2c15`, pinned in `preflight_pins.json`.
- **Gallery:** Deterministic **3+2 centered** tile layout of exact processed WebPs. Written-PNG pixel-audit `VALID`; all 5 tile pixels `FAITHFUL`, layout `CONFORMING`. Captions reflect actual decimal kB, and the separate 125/64/32 thumbnail comparison is retained.
- **Gallery SHA-256:** `2606f5c7fa545a305417de4eb5e287d7c04e815e0bd76fce4a04b209b0cbe252`.
- **Gallery decoded pixel SHA-256:** `4da47c596f74b0596fd1a74a1104a6194bfe6fb926c2886fc16a5269a1082816`.
- **Members SHA-256:** `470a549a5155e8d63df939e605d30636496b2f28ddbb831f3a8e0e5c3c1dd550`.
- **Full output evidence:** `docs/design/shinseina_ki/PRODUCTION_EVIDENCE_V1.json` stores exact export filenames, sizes, hashes, proof boundaries and built-but-unaccepted archive hashes. Human-friendly archival filename prefix `shinseina_ki` avoids collisions with other bloodline abbreviated slugs.
- **Full closeout build:** `shinseina_ki_jutsu_icons_closeout_v1.zip`, 7128174 bytes, SHA-256 `a036b44fd8715fde75a743fe6362d41c2c44e64908c0c91769033ebf5abd9067`; contains approved raws, five exports, deterministic gallery, source/lock evidence, production QC and checksums, but **family acceptance PENDING**.
- **Flat WebP build:** `shinseina_ki_jutsu_icons_webps_PREFLIGHT_PASS_5webp_v1.zip`, 629139 bytes, SHA-256 `ab96c433235136b2db5085346fb7c5d9a8708ec184cf28ce057d8e6d09f90c28`. `PREFLIGHT_PASS` means canonical file QC, not director-gallery approval, game upload or publication.
- **Git pin:** Only written text evidence and SHA commitments live on `chatgpt/shinseina-ki-jutsu-art-studio-20261019`. **Source/export/gallery/ZIP binary bytes are NOT Git-pinned.** Keep the actual generated local artifacts/recovery ZIPs until delivered; a Git document cannot reconstruct their image pixels.

## Next — Exact family showcase acceptance

**Review image:** `shinseina_ki_jutsu_showcase_v1.png`, SHA-256 `2606f5c7fa545a305417de4eb5e287d7c04e815e0bd76fce4a04b209b0cbe252`. Director must review the rendered **exact-WebP** gallery (not a generated remake), and separately confirm that Wood Warrior's visually approved humanoid/sentinel structure is accepted **as a target-specific exception** despite the earlier no-anatomy direction. If director accepts, copy `gallery.sha256`, optional `gallery.pixels_sha256` and `members_sha256` into `approved.json.family_acceptance` with exact human evidence, then run pinned `finalize` with a **fresh label** (v2) to produce acceptance-sealed archives. Audit the new gallery. Do not modify any accepted raw or WebP bytes. If rejected, stop and return only the affected icon(s) to isolated generation.

Final delivery is to the operator's bloodline ZIP processing/master collection workflow. Final director gallery acceptance, ZIP user delivery, Git binary pin and live upload/readback are not automatic consequences of these tests.

## Gate summary

`ORIGINAL_SOURCE_VERIFIED`: PASS (2026-10-17 historical capture/ZIP, **not current live**).
`DIRECTION_APPROVED`: 5/5 hash-bound locks approved.
`RAW_VISUAL_APPROVED`: 5/5 approved.
`OUTPUT_LOCAL_QC`: 5/5 PASS.
`CANONICAL_PREFLIGHT`: PASS 5/5, script/spec pins matched.
`FAMILY_SHOWCASE_ACCEPTED`: PENDING director acceptance.
`ZIP_DELIVERED`: v1 archives BUILT_NOT_DELIVERED at this checkpoint.
`GIT_BINARY_PIN`: NOT_PERFORMED.
`USER_UPLOAD_READBACK`: NOT_PERFORMED.
Live-game requests/writes: 0/0; credentials: none.

## Separate companion — Ancient Wood Golem AI avatar (2026-10-19)

**Director instruction:** Add one additional **AI portrait**, not a sixth jutsu, to the Shinseina Ki showcase. The supplied file `1000018846.png` is actually a JPEG (1536×1536, SHA-256 `0ef0dab603449d759eb1db0d62a10be72693b482741388794f21959c664e3832`); its exact uploaded bytes are retained in the companion review package. No AI record ID/game binding has been established.

**Mechanical AI_AVATAR export:** `ai_shinseina_ki_ancient_wood_golem_v1.webp`, 608×608 RGBA **lossless VP8L WebP**, 426,438 bytes, SHA-256 `231984d61ff33560024c32a0c5b8af5bfc09a475a64dd00de3ddff153693983e`. The black original background needed a **documented border-connected near-black matte removal**, then the official `chroma.py --target AI_AVATAR --key magenta` final exporter, with magenta override to preserve jade chakra. This is a one-off transparent-source preparation, **not** an unreviewed change to the canonical processing script. The export required no quantization and the script/spec blobs match the pins. The actual `artpreflight.py --type AI_AVATAR` returned **0 errors and 0 warnings**. Dark and 320px light/dark/white composites were inspected. Source art already touches its lower edge at the feet; do not claim cropping was repaired.

**Extended visual board:** `Shinseina_Ki_Showcase_with_AI_Avatar_v2.png`, SHA-256 `0ef87a13bb64da6c3e826af245da31ff9dc739d89626e62b7f6c6ef1933f861f`, is a **separate 3+3 companion showcase** with **5 JUTSU_ICON + 1 AI_AVATAR**, assembled only from the exact six processed WebPs. Pixel-equality verification PASS 6/6. **Do not submit this image to the P1 five-jutsu `audit-gallery` as though the avatar were a jutsu.** The original five-icon audited gallery (`2606f5c7fa545a305417de4eb5e287d7c04e815e0bd76fce4a04b209b0cbe252`) and its five-member P1 commitment remain unchanged and **director acceptance PENDING**.

**Companion delivery:** `Shinseina_Ki_AI_Avatar_Companion_REVIEW_v1.zip`, 6,825,125 bytes, SHA-256 `0cf78c68ca1b1191e29fd592da1c35ce9b14f41cc2790626eed2472dee70aa28`. This **REVIEW** package is not the five-icon master processing closeout, and image bytes are not Git-pinned. Its SHA evidence and remaining gates are in `AI_AVATAR_COMPANION_V1.json`.

**Director gates remain separate:** Processed AI avatar and extended showcase visual acceptance PENDING; original exact five-jutsu gallery acceptance PENDING; formal Wood Warrior anatomy exception confirmation PENDING; AI record-ID binding and user-only live upload/readback NOT_PERFORMED. Live-game requests/writes: 0/0; credentials: none.
