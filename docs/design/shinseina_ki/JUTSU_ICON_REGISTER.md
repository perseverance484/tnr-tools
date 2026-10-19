# Shinseina Ki — Jutsu Icon Register

**Studio:** Persistent ZIP-first Art Studio, not Bloodright tier emblems.
**Lead:** Art Director; **support:** Image Production.
**Director decisions (2026-10-19):** Sacred Heartwood treatment and five reserved technique silhouettes APPROVED; Guardian's Grove and Exploding Wood Serpent both received individual raw visual approval. Forest Wisdom is next.
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

## Raw visual approvals — 2/5

| Jutsu | Approved raw (user-uploaded bytes) | Director | Export QC | Canonical preflight | Final gallery | Git raw pin |
|---|---|---|---|---|---|---|
| Guardian's Grove | `raw_shinseina_ki_guardians_grove_v1.jpg`; JPEG RGB 1536×1536; 663,598 bytes; SHA-256 `814225c19ea175f0eefd71bc747b1d69cdd5b170b76b5d6b9971b8e68dffeff8` | APPROVED | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |
| Exploding Wood Serpent | `raw_shinseina_ki_exploding_wood_serpent_v1.jpg`; JPEG RGB 1536×1536; 645,451 bytes; SHA-256 `311dd5adbd377cf1189ffdd6c990a1aab7a9667fffc032083fac90254e626d54` | APPROVED | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |
| Forest Wisdom / Wood Warrior Summon / Eternal Forest | Not generated/approved | PENDING | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |

**Raw provenance:** The uploaded filenames end with `.png`, but actual decoded formats are **JPEG**; both original byte streams are preserved unmodified with `.jpg` suffixes in Studio checkpoint archives. User-upload receipts and approvals are recorded, not proven generator-native source/attempt evidence. Neither binary is Git-pinned.

**125/64/32 pairwise visual check:** Actual `jutsu_studio.py compare` on the approved original raws was inspected. Serpent's exploding S-shaped wood strike and Guardian's closing arched cavern are recognizably distinct. This is a non-generative review aid, **not** a final family gallery. N/N comparison remains pending.

**Recovery checkpoints:** `shinseina_ki_guardians_grove_checkpoint_v2_20261019.zip` (historical, one approved raw); `shinseina_ki_studio_checkpoint_2of5_20261019.zip` (two approved raw sources with SHA-256 evidence, locks, 125/64/32 review aid). Neither is a final closeout or upload-ready WebP delivery.

## Target locks

`docs/design/shinseina_ki/JUTSU_TARGET_LOCKS.json` contains all five source-mapped technique locks; 3/5 now have hash-bound `DIRECTION_APPROVED` (Guardian, Serpent, Forest Wisdom) by the director-approved family silhouette ledger and successive instructions to proceed. No unquoted separate SHA-specific approval is asserted. `jutsu_studio.py lock-check --source-index`: PASS (2026-10-19). The other two await individual advancement.

## Next — Forest Wisdom

**Jutsu:** `zZ-QZGRXC-aUiskpZ4Z_3` (D, BLOODLINE). October 17 historical `jutsu.get`: “Listen to your ancestors and learn from their previous battles,” SELF-targeted, with recorded `increasedamagegiven` rows. Source identity member: `images/zZ-QZGRXC-aUiskpZ4Z_3_Forest_Wisdom.png`, SHA-256 `565db6d95e497e5e8611f479bc63ca6d93f61ad2eddbf5a6a10a41e82cbf9ded`.

**Technique and composition:** Accumulated ancestral combat knowledge as a **physical, solid ancient heartwood cross-section** whose *real irregular growth rings* channel jade chakra **inward** to a concentrated central pulse. Close slightly elevated camera, large solid cut face occupying the frame, coarse bark edge; no hollow portal, decorative rings, spell circle, magic shield, glyph, free-floating disk or generic forest landscape. Readable self-enhancement, **not an attack**. Keep the no-anatomy default despite figures in the legacy identity artwork.

**References:** 1) original Forest Wisdom PNG — IDENTITY ONLY; 2) approved Serpent source JPEG — STYLE/MATERIAL ONLY, never S-curve strike/explosion conditioning. Exactly two actual individually attached image files; not ZIPs/URLs/contact sheets. Forest Wisdom lock SHA-256 `e71d8d04618d0464739b0d94cd8dc7e8a43ade7db102abaa861187c62252b293`, direction APPROVED.

**Other sibling exclusions:** Guardian's Grove arched cavern closing inward, Serpent's S-shaped impact, Wood Warrior Summon's vertical armour assembly, Eternal Forest's V-shaped repeating corridor.

## Production gates

ORIGINAL_SOURCE_VERIFIED: PASS (October historical roster, not live); DIRECTION_APPROVED: 3/5; RAW_VISUAL_APPROVED: 2/5; OUTPUT_LOCAL_QC: NOT_RUN; CANONICAL_PREFLIGHT: NOT_RUN; FAMILY_SHOWCASE_ACCEPTED: PENDING; ZIP_DELIVERED (final N/N): NOT_PERFORMED; GIT_BINARY_PIN: NOT_PERFORMED; USER_UPLOAD_READBACK: NOT_PERFORMED. No game requests/writes. Credentials: none.
