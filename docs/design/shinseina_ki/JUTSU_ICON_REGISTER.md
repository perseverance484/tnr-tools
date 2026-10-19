# Shinseina Ki — Jutsu Icon Register

**Studio:** Persistent ZIP-first Art Studio, not Bloodright tier emblems.
**Lead:** Art Director; **support:** Image Production.
**Director decision (2026-10-19):** Sacred Heartwood family treatment and the five primary silhouette/action reservations APPROVED. Guardian's Grove target approved individually; the returned artwork was subsequently director-approved with “Approved, next”.
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

## Raw visual approvals

| Jutsu | Director direction | Approved raw source | Raw visual | Local export QC | Canonical preflight | Family gallery | Git binary pin |
|---|---|---|---|---|---|---|---|
| Guardian's Grove | APPROVED | 2026-10-19 user-uploaded candidate; **decoded JPEG** (despite upload ending .png), 1536×1536 RGB, **663,598 bytes**, SHA-256 `814225c19ea175f0eefd71bc747b1d69cdd5b170b76b5d6b9971b8e68dffeff8` | **APPROVED (1/5)** | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |
| Other four | Family reservations approved; individual hash-bound locks pending | none | PENDING (0/4) | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |

**Guardian raw provenance:** The exact *uploaded file bytes* were preserved without recompression in a `.jpg`-suffixed studio copy. The repository contains the evidence SHA and decision but **not those binary bytes**; do not assert a Git pin. Generator-native original-file or attempt/session provenance was **not** independently proven. A standalone deterministic 125/64/32 raw thumbnail composite was made; full pairwise visual QC remains pending.

**Stable recovery checkpoint:** `shinseina_ki_guardians_grove_checkpoint_20261019.zip` was delivered in the 2026-10-19 Studio conversation; includes exact user-uploaded approved JPG bytes, checksum-bound receipt, target-lock draft and non-generative thumbnail composite. This checkpoint is **not** the full-family closeout or a production export.

## Next — Exploding Wood Serpent

Source evidence (Oct 17, historical capture): technique description **“Summon an exploding wooden serpent”**; single-enemy Wood damage, additional recoil effect recorded. Original member `images/8MRWPNK3lOxCLVqWrE-xJ_Exploding_Wood_Serpent.png`, SHA-256 `f76461fc436bfd5e8631c586cf664a12c69d7cb42b7784bf66c7de98cd300123`. Next image must be a distinct S-shaped **striking-and-detonating** articulated heartwood serpent; not another enclosing ring or forest. No animal face/eyes/teeth or anatomical limbs unless the director approves that exact exception. The prior family reservation is director-approved; per-target v1 lock SHA `9d1a37f2d6c030a69f6ff8c0195f7a833cc51316143efbed15e78d223d60601f` is mechanically complete but **individual hash-bound direction approval remains PENDING**.

**Generator references (maximum 2 individual images):** the original Exploding Wood Serpent PNG (IDENTITY ONLY), and accepted Guardian's Grove source JPEG (STYLE/MATERIAL ONLY, no cavern/arch composition). Each requires actual attached bytes; a path or image URL does not establish conditioning.

**Attempts log:** NOT_RECORDED. No assertion of independent generator-session provenance. **N/N processing, `verify-approved`/`finalize`, local export QC, canonical `artpreflight --type JUTSU_ICON`, deterministic final showcase, director gallery acceptance, ZIP delivered, Git pin and user upload/readback remain separate future gates.**
