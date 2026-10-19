# Shinseina Ki — Jutsu Icon Register

**Studio:** Persistent ZIP-first Art Studio, not Bloodright tier emblems.
**Lead:** Art Director; **support:** Image Production.
**Director decisions (2026-10-19):** Sacred Heartwood treatment and five reserved technique silhouettes APPROVED; Guardian's Grove, Exploding Wood Serpent and Forest Wisdom now have individual raw visual approval (3/5). Wood Warrior Summon is next.
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

## Raw visual approvals — 3/5

| Jutsu | Approved raw (uploaded bytes) | Director | Local export QC | Canonical preflight | Family gallery | Git binary pin |
|---|---|---|---|---|---|---|
| Guardian's Grove | JPEG RGB 1536×1536, 663,598 bytes; SHA-256 `814225c19ea175f0eefd71bc747b1d69cdd5b170b76b5d6b9971b8e68dffeff8` | APPROVED | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |
| Exploding Wood Serpent | JPEG RGB 1536×1536, 645,451 bytes; SHA-256 `311dd5adbd377cf1189ffdd6c990a1aab7a9667fffc032083fac90254e626d54` | APPROVED | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |
| Forest Wisdom | JPEG RGB 1536×1536, 763,252 bytes; SHA-256 `9d2d1077c62ec9f375b82deff148fa9b3efc347c965e50e56d6d1344ef181556` | APPROVED | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |
| Wood Warrior Summon / Eternal Forest | No accepted raw yet | PENDING | NOT_RUN | NOT_RUN | NOT_BUILT | NOT_PERFORMED |

**Raw preservation:** Uploaded filenames `1000018837.png`, `1000018839.png`, `1000018840.png` all contain **JPEG bytes**, not PNG. Preserve exact source bytes as `raw_shinseina_ki_guardians_grove_v1.jpg`, `raw_shinseina_ki_exploding_wood_serpent_v1.jpg`, `raw_shinseina_ki_forest_wisdom_v1.jpg`. Original user uploads and approvals are verified; generator-native session/attempt provenance remains UNVERIFIED, and raw binaries are NOT pinned in Git.

**Visual QC:** The official `jutsu_studio.py compare` generated a non-generative 125/64/32 review aid comparing Forest Wisdom against Guardian's Grove and Exploding Wood Serpent. The solid heartwood disk/core, enclosing root cavern and exploding S-strike are visually distinct at all three sizes. Compare PNG SHA-256 `4152ff617e3c32ce2ee8fcbf93e8eed161c1c6a6ff53a20c6497aa91ef8b8417`. This **does not** certify final exported WebPs or gallery acceptance.

**Recovery:** `shinseina_ki_studio_checkpoint_3of5_20261019.zip` preserves the three approved raw sources, byte hashes, source mapping, lock register, reference for the next target, and comparative review aid. Earlier checkpoints are historical. The checkpoint is NOT a P1 final production closeout or flat preflight-PASS export ZIP.

## Target locks

`docs/design/shinseina_ki/JUTSU_TARGET_LOCKS.json` is the `tnr.jutsu-studio.locks/1` register. All five locks are complete; four now have hash-bound direction approval grounded in the approved family reservations and sequential “Approved, next” instructions: Guardian's Grove, Exploding Wood Serpent, Forest Wisdom and Wood Warrior Summon. No separate individually quoted SHA acceptance is invented. `jutsu_studio.py lock-check --source-index`: PASS (2026-10-19), validating four approved locks and five complete roster identities. Eternal Forest remains direction PENDING.

## Next — Wood Style: Wood Warrior Summon

**Jutsu:** `LnzsA7WDqi06AU0s7yrVP` — A-rank BLOODLINE. The historical October 17 `jutsu.get` describes summoning one's ancestors' sacred guardian, with `target: EMPTY_GROUND` and a `summon` effect. It is not a broad forest trap, serpent or buff. Not proven against the current-live game.

**Approved target lock:** A **single angular armoured heartwood war-pillar** visibly assembling upward from a burst of interlocking roots. Camera frontal three-quarter, motion bottom-to-top. Thick bark plates slot into a defined upright guardian/war-effigy silhouette, with **one** restrained jade chakra channel glowing through fitted seams. Powerful vertical architecture and a strong dark background; crisply readable at 125/64/32px.

**Important technique constraint:** The old original shows a humanoid tree guardian; it is **identity reference only**. No literal body, human/wooden face, eyes, hands, arms or limbs are approved for this target. The guardian concept must read through wood-armour **construction and summoned emergence**, not anatomy. If actor-free composition proves inadequate, seek a target-specific director exception rather than assuming approval.

**Sibling exclusions:** No Forest Wisdom solid ringed disk/central vortex, Guardian's Grove closing U-shaped root cavern, Serpent's attacking S-shaped coil/detonation, or Eternal Forest's V-shaped endless tree corridor. No runes, spells, floating sigils, text or UI.

**References:** Individually attach the **original Wood Warrior Summon PNG** (IDENTITY ONLY), SHA-256 `cc3db58546880fcd77c009eb1c4b46cc93898544fa3dfb6528da3a95b14d30b4`, and the **approved Guardian's Grove JPEG** (STYLE/MATERIAL ONLY), SHA-256 `814225c19ea175f0eefd71bc747b1d69cdd5b170b76b5d6b9971b8e68dffeff8`. Never copy its root-arch prison silhouette. Each actual image must be attached to the isolated generator, no ZIP or URL-only conditioning.

**Lock v1 SHA-256:** `44b877dfc1339c45ea1e2f0cfe45950ac5aa917e36b813ece229ee9472bfd27b`.

## Outstanding production gates

ORIGINAL_SOURCE_VERIFIED: PASS (historical; not current live). DIRECTION_APPROVED: 4/5. RAW_VISUAL_APPROVED: 3/5. OUTPUT_LOCAL_QC: NOT_RUN. CANONICAL_PREFLIGHT: NOT_RUN (no final WebPs). FAMILY_SHOWCASE_ACCEPTED: PENDING. ZIP_DELIVERED (final N/N closeout): NOT_PERFORMED. GIT_BINARY_PIN: NOT_PERFORMED. USER_UPLOAD_READBACK: NOT_PERFORMED. Live-game requests/writes: 0/0; credentials: none.
