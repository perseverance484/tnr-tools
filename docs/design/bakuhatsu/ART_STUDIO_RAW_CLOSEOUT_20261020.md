# Bakuhatsu — Art Studio RAW Closeout (2026-10-20)

**Workstream:** A/S/H Bakuhatsu / BR-008 / A-rank BLOODLINE jutsu images (NOT Bloodright tier emblems).
**Lead:** Art Director | Support: Image Production.
**Status:** **STUDIO RAW ART COMPLETE — 5/5 DIRECTOR-APPROVED.** Downstream production/export/gallery gates pending.
**Repository:** `perseverance484/tnr-tools`.
**Main verified at closeout:** `02a288e966db27f427508734a6223e0e583b081a`.
**Frozen evidence head before this closeout note:** `chatgpt/bakuhatsu-jutsu-art-studio-20261019@68cff7db7d5cbac0db8e88e74f8dfe6a4b2ba5b4`.
**Machine-readable source:** `docs/design/bakuhatsu/JUTSU_TARGET_LOCKS.json` blob `726e754752348aadc4585a1c02670a3d24777240` (5/5 direction locks APPROVED).
**Register:** `docs/design/bakuhatsu/JUTSU_ICON_REGISTER.md` blob `8291888826afa78764e66e0c49e6c58897c69ae1`.
**Approved source ZIP:** `BR-008_Bakuhatsu.zip`, 381668 bytes, SHA-256 `7944d75ab09950d89fa927fec9fe5421d58eb29de36dd986e17c420ad2d18a24`, intake 5/5 IDs and original assets verified, historical capture only.
**Exact studio-closeout archive:** `bakuhatsu_Art_Studio_Closeout_5of5_20261020.zip`, **11377968 bytes**, SHA-256 **`c66853c6009e4de3d5bd901b26ab10e4c1f155d88ed079b5aa63e442b6e574cc`**. Contains 29 members: README, original source ZIP, five exact approved raw images, five individual reference originals plus bloodline identity, original manifest, canonical `approved.json`, byte-exact `locks.json`, `source_index.json`, `studio_ledger.json`, provenance/approval evidence, rejected/supersession notes, real doctor/intake/lock-check/verify-approved receipts, SHA256SUMS, and the **DRAFT** non-generative raw-only 3+2 SVG/PNG preview.

## Five final director-approved raw-art mappings

| Jutsu | ID | Final raw source (actual decoded format) | Raw SHA-256 | P0 direction |
| --- | --- | --- | --- | --- |
| Blast Shield | `Awyd1k1-tw4uzn-PLbcdP` | `raw_bakuhatsu_blast_shield_v1.jpg` (JPEG) | `f2167a947f77c56f39a6d24b8af0660406cf7654872fdf88407333f0539be308` | APPROVED v1 |
| Inferno Cataclysm | `FTTl_wnTlbvOfOyiGCc-b` | `raw_bakuhatsu_inferno_cataclysm_v1.jpg` (JPEG) | `6bdaaf03a35532b0cfa3bc64150187540a2b4bbcaf87b283d0f6d09e0828e214` | APPROVED v1 |
| Kinetic Nova | `y8y01n9jz16bz5EBzl4wr` | `raw_bakuhatsu_kinetic_nova_v1.jpg` (JPEG) | `7bfdcfaeb20a026f5f98a5381ac564f8a6d441ab8b024f1c7d39a84237bc5050` | APPROVED v1 |
| Charge 4 Explosion | `rOqCTqNBSW_A-QYesFBw9` | `raw_bakuhatsu_charge_4_explosion_v1.jpg` (JPEG; direction v2 C4) | `619bc4f7a86adfdbdf98a124a2f816911e199389ae26240cb04a56c8bb1bdd8a` | APPROVED v2 |
| Howitzer Crash | `hW4IV1Hp59BqVFx0u-gTd` | `raw_bakuhatsu_howitzer_crash_v3.png` (PNG) | `e410b382b9e268efdad878f80d9f97ce21b70a289350674c3c18c7ec9a39727c` | APPROVED v3 Mach-Shear |

**Director evidence:** raw approvals recorded in persistent Studio conversation on October 19–20, with individual candidate filenames and exact SHA-256s in `evidence/APPROVAL_AND_PROVENANCE.json` inside archive. Rejected Howitzer v1/v2 and superseded Charge 4 v1 direction are **not approved current artwork**.

## Actual checks performed (NO production processing)

- Original source ZIP: CRC PASS, 5/5 image members hashed/decoded/identity-mapped.
- Approved raws: 5/5 exact source hashes matched and decoded; four RGB JPEG 1536x1536 and one RGB PNG 1254x1254. Original bytes unchanged, including formerly mismatched uploaded `.png` labels on JPEGs.
- `jutsu_studio.py doctor`: **RUN_CAPABLE_CANONICAL** (environment readiness; synthetic probe only).
- `jutsu_studio.py lock-check ... --source-index source_index.json`: **PASS, 5/5 DIRECTION_APPROVED** (final pins).
- `jutsu_studio.py verify-approved approved.json --source-index source_index.json --locks locks.json`: **PASS, 5/5 raw hashes, roster and lock identities**. Attempt log omitted by design: **NOT_RECORDED**, not a fabricated canonical pass.
- ZIP: `zipfile.testzip()` CRC PASS; all 29 archive member SHA-256s re-read against staging; 28 SHA256SUMS payload entries matched (SHA256SUMS does not hash itself).
- Plain SVG preview: embedded base64 bytes of every tile matched accepted raw SHA-256. Preview is **DRAFT** and NOT the export-based final family showcase. The earlier decorated *generative* five-icon collage is invalid as preservation evidence.

## Separate K gates at studio closeout

| Gate | Actual state |
| --- | --- |
| ORIGINAL_SOURCE_VERIFIED | VERIFIED 5/5 |
| DIRECTION_APPROVED | APPROVED 5/5 |
| RAW_VISUAL_APPROVED | APPROVED 5/5 |
| OUTPUT_LOCAL_QC | NOT_RUN |
| CANONICAL_PREFLIGHT | NOT_RUN (do not infer from doctor) |
| FAMILY_SHOWCASE_ACCEPTED | NOT_BUILT / PENDING (raw-only DRAFT preview exists) |
| ZIP_DELIVERED | BUILT; link delivery occurs in Studio chat |
| GIT_BINARY_PIN | NOT_PERFORMED (repo stores records, not these approved image bytes) |
| USER_UPLOAD_READBACK | NOT_PERFORMED |

**Handoff:** Master Processing Station receives this *raw* closeout ZIP as one intake for Bakuhatsu. The processor owns mechanical lossless `JUTSU_ICON` WebP export, actual canonical `artpreflight.py --type JUTSU_ICON` on exports, and export-pixel-audited 3+2 family gallery. Separate director gallery acceptance and user-only live upload/readback must follow. This Art Studio did **not** process or publish images and had **0 live-game requests / 0 writes**, **no credentials**. No game action authorized.
