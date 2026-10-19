# Shinseina Ki — Jutsu Icon Register

**Studio:** Persistent ZIP-first Art Studio, not Bloodright tier emblems.
**Lead:** Art Director; **support:** Image Production.
**Director decisions (2026-10-19):** Sacred Heartwood treatment and the five family technique silhouette reservations APPROVED. Guardian's Grove, Exploding Wood Serpent, Forest Wisdom and Wood Warrior Summon have individual director-approved raw images (4/5). Eternal Forest is next.
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

## Raw visual approvals — 4/5

| Jutsu | Director-approved uploaded raw, actual decoded bytes | Raw acceptance | Local export QC | Canonical preflight | Gallery acceptance | Git binary pin |
|---|---|---|---|---|---|---|
| Guardian's Grove | JPEG 1536×1536, 663598 bytes; SHA-256 `814225c19ea175f0eefd71bc747b1d69cdd5b170b76b5d6b9971b8e68dffeff8` | APPROVED | NOT_RUN | NOT_RUN | PENDING | NOT_PERFORMED |
| Exploding Wood Serpent | JPEG 1536×1536, 645451 bytes; SHA-256 `311dd5adbd377cf1189ffdd6c990a1aab7a9667fffc032083fac90254e626d54` | APPROVED | NOT_RUN | NOT_RUN | PENDING | NOT_PERFORMED |
| Forest Wisdom | JPEG 1536×1536, 763252 bytes; SHA-256 `9d2d1077c62ec9f375b82deff148fa9b3efc347c965e50e56d6d1344ef181556` | APPROVED | NOT_RUN | NOT_RUN | PENDING | NOT_PERFORMED |
| Wood Style: Wood Warrior Summon | Uploaded `1000018841.png` contains **JPEG** 1536×1536 RGB, 792381 bytes; SHA-256 `fc930c256b259328336dd48e068b4f28417bf7f090a39155686bda1bd9454086` | APPROVED | NOT_RUN | NOT_RUN | PENDING | NOT_PERFORMED |
| Eternal Forest | None | PENDING | NOT_RUN | NOT_RUN | PENDING | NOT_PERFORMED |

**Preservation:** The four director-approved upload files all had a `.png` filename but contain JPEG bytes; store their **exact original bytes**, under accurate `.jpg` names, in the local Studio recovery checkpoint. This is not proof of generator-native original-file or session/attempt provenance. Binary Git pins have not been performed. No re-encoding or mechanical export has occurred.

**Wood Warrior's target-scoped art-direction deviation:** The accepted candidate portrays a head-like wooden crest, shoulders and limb-like bark armour. The originally approved pre-generation v1 lock explicitly excluded humanoid anatomy. The director visually approved **this exact image**, so record the acceptance and this narrow, target-specific visible exception together; do **not** silently recast the locked negatives, claim a separate verbal exception, or treat it as approval of anatomy in Eternal Forest or future icons. If formal P0 evidence requires a separately stated exception, flag this unresolved distinction at closeout; do not promote raw acceptance to all-gates PASS.

**125/64/32 QC:** The actual repository `jutsu_studio.py compare` tool was run on the newly approved JPEG and all three previously approved raw JPEGs, with direct pixel inspection. Wood Warrior's rising armoured sentinel has a distinct upright mass; Guardian's Grove is the closing U-shaped cavern, Serpent is the exploding S-strike, and Forest Wisdom is a solid growth-ring disk. Review PNG SHA-256 `daefd709dc6bb0582f12d58c836435f0eded7311510e02ca41706335a43dfa7a`. This non-generative comparison is **not a final family showcase** or WebP QC.

**Recovery:** `shinseina_ki_studio_checkpoint_4of5_20261019.zip` preserves four unchanged approved JPEG byte streams, the historical source index, target locks, hashes and non-generative compare records, plus the original identity art for the final target. This ZIP is **not** a full-family closeout or final WebP delivery.

## Target locks

`docs/design/shinseina_ki/JUTSU_TARGET_LOCKS.json` is the `tnr.jutsu-studio.locks/1` source. All five target locks are complete and now have director-grounded direction approvals (approved five-family silhouette ledger and successive “Approved, next” instructions). This binds exact jutsu IDs, action, camera, motion, sibling exclusions and reference roles; the actual rendered pixels require separate human judgment. `jutsu_studio.py lock-check --source-index`: PASS on the five mapped roster targets. The Eternal Forest lock's v1 SHA-256 is `9a18d583149d0cacf490f48ec9a3af4b83569f85611ad7e7180d73a81eab29ed`, with Forest Wisdom's raw JPG as STYLE/MATERIAL ONLY.

## Next — Eternal Forest (fifth and final technique)

**Identity:** `D3t1nlaVAw8kLfjDO5Wvy`, A-rank BLOODLINE, Shinseina Ki / `vA8I_7iBNgvkuKOpnG1yD`.

**Historical combat evidence:** October 17 read-only `jutsu.get` describes “Trap your enemy in a never ending Forest.” Its authored rows show one Wood-element damage hit and a wound effect, target `OTHER_USER`, method `SINGLE`. Neither is current-live proof of exact behavior. Original PNG member: `images/D3t1nlaVAw8kLfjDO5Wvy_Eternal_Forest.png`, original SHA-256 `92e1555eb68748287c1dbefa2b497980a5484237cef6681c7997a35fbe3956ac`.

**Approved dominant technique and silhouette:** A vast **V-shaped, repeating corridor of immense ancient tree walls** forms an apparently endless wood-and-chakra prison. Camera looks deep between **converging walls**, vanishing into a thin distant seam. Walls are physical thick bark/heartwood and advance inward around the unseen victim (no characters); the foreground becomes a strong V that compresses toward far distance. Motion: opposing walls press from sides toward the center while recurring trunk ribs shrink down the depth axis. A single jagged root edge or splintering pressure seam provides the wound/attack cue. Strong foreground root masses + small distant dark pocket, minimal emerald lighting along forced-in seams. Not a natural forest vista.

**Critical distinctness:** **NOT Guardian's Grove** — which has a near, fully enclosed U-shaped cavern and green toxic hollow; Eternal Forest is long-range forced perspective with repeated wall pairs and no rounded entrance/cave arch. NOT Forest Wisdom's solid circular disk/chakra core, Serpent's attack coil/explosion, Wood Warrior's giant vertical humanoid construct.

**Art controls:** Sacred Heartwood amber-gold heartwood, dark umber roots, restrained jade-green flowing chakra against deep charcoal. Premium controlled pixel-detail, no text/UI/symbols/runes/spell circles/actors/anatomy. No decorative endless glade/forest ambience, central standing fighter, circular chakra ring or magical vortex. Thumbnail-readability 125/64/32.

**Attached references (at most two):**
1. Exact `92e1555eb687_D3t1nlaVAw8kLfjDO5Wvy_Eternal_Forest.png` — **IDENTITY ONLY** (never copy its human or luminous circular floor effect).
2. Exact `raw_shinseina_ki_forest_wisdom_v1.jpg` — **STYLE/MATERIAL ONLY** (do not copy its round tree slice or central vortex).

## Remaining production gates

ORIGINAL_SOURCE_VERIFIED: PASS with historical roster, no live check. DIRECTION_APPROVED: 5/5. RAW_VISUAL_APPROVED: 4/5. OUTPUT_LOCAL_QC: NOT_RUN. CANONICAL_PREFLIGHT: NOT_RUN; a successful `doctor` only establishes capability. FAMILY_SHOWCASE_ACCEPTED: PENDING, not built. ZIP_DELIVERED: CHECKPOINT_ONLY (no N/N closeout). GIT_BINARY_PIN: NOT_PERFORMED. USER_UPLOAD_READBACK: NOT_PERFORMED. Live-game requests/writes: 0/0; credentials: none.
