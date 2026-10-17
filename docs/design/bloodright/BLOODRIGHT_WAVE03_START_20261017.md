# Bloodright Tier-Emblem Art Studio — Wave 03 Intake

**Status:** WAVE 3 ORIGINAL REFERENCES VERIFIED AND FIVE PALETTE TREATMENTS DIRECTOR-APPROVED. BR-083 and BR-064 completed families visually approved (**12/29 families; 36/87 icons**). BR-020 Crystal Essence trio PROPOSED / final per-icon director acceptance PENDING.
**Date:** 2026-10-17
**Lead:** ChatGPT Art Director; **support:** Image Production.
**Branch:** `chatgpt/bloodright-wave03-art-studio-20261017`
**Exact base:** `chatgpt/bloodright-wave02-art-closeout-20261017@8009ebad7d45a1046b550542d4e89071c22f4dd6`
**Main last verified at initialization:** `9a0970002a80531078ac5e4b0f72578d3f7855f5` (main has moved independently; reverify before integration).
**Pinned membership evidence:** `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866`, `docs/design/bloodright/roster.json`.
**Owning workflow:** `docs/workflows/BLOODRIGHT_ICON_STUDIO.md` and `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md` on this branch; preserve `docs/design/bloodright/BLOODRIGHT_WAVE02_BR067_ROLE_SWAP_20261017.json` as the current Shiroi tier-role mapping.

## Completion brought forward

- Wave 1/pilot: **5/29** visually approved families / **15/87** icons.
- Wave 2: **5/5** individually accepted families / **15/15** icons, including BR-067's **director-authorized Hidden Art ↔ Advanced Art role-file swap without pixel edits**, approved as `RoleSwap_v02`. Do not reuse earlier pre-swap category role assignments.
- Overall before Wave 3: **10/29 families, 30/87 icons** visually approved; **19 families, 57 icons** not yet produced or visually accepted.
- Existing acceptance of artwork is not `skillTree.image` preflight success, Git-binary pin, an immutable Forge imagePack, or a live-game action.

## Wave 3 — first five remaining in the pinned production tracker

| Order | ID | Bloodline | Rank | Original public jutsu | Mechanics classification (reference, not art palette) | Reference ZIP expected |
|---:|---|---|:---:|---:|---|---|
| 11 | BR-083 | Tetsugan | H | 11 | Metal | `BR-083_Tetsugan.zip` |
| 12 | BR-064 | Shakunetsu Sakura | A | 5 | Scorch | `BR-064_Shakunetsu_Sakura.zip` |
| 13 | BR-020 | Crystal Essence | A | 5 | Crystal | `BR-020_Crystal_Essence.zip` |
| 14 | BR-074 | Suragu | A | 5 | Lava | `BR-074_Suragu.zip` |
| 15 | BR-090 | Vaporia | A | 5 | Boil | `BR-090_Vaporia.zip` |

**Expected input:** five original bloodline source-art ZIPs with **31 jutsu images** and, if supplied, five identity images. None of these five ZIPs has been attached/inspected in this wave yet. Filenames are suggested intake labels, not proof of file existence.

**Distinguishability questions to assess only after inspecting actual pixels:** Tetsugan vs magnet bloodlines (Houkyuken/Itojinsei); Shakunetsu Sakura vs previously approved solar Taiyo Kami and lava Suragu; Crystal Essence vs icy Blue Blade Eyes; Suragu vs other orange/thermal themes; Vaporia vs ice/water/steam themes. Do not choose palettes, symbols or textures from classification/name alone.

## 2026-10-17 — Shakunetsu visual acceptance; Crystal Essence production checkpoint

- **Shakunetsu Sakura (BR-064):** Director accepted all 3 Midnight Blossomfire tiers. Raw PNG and lossless WebP bytes were not changed from the previously reviewed proposal. `BR-064_Shakunetsu_Sakura_Bloodright_Approved_3_Icons.zip` SHA-256 `ec1723a199b104737fcbb278de5f785898cfb280e1bb94377de4f413f0395463`. Full per-tier hashes and approval evidence in `BLOODRIGHT_WAVE03_BR064_PROPOSAL_QC_20261017.json`.
- **Crystal Essence (BR-020):** Director-approved Prismatic Jadeglass recipe converted into 3 separate tier-emblem original 1254px PNGs plus 3 256px lossless RGB WebPs. Source ZIP 5 jutsu + identity independently SHA/manifest/format-verified. Exact brightness/foreground geometry preserved for each tier against approved Ethereal master; maxRGB matches at all 1254² pixels for all 3, IoU 1.0 at thresholds 1/16/64/128/192/240. Under working byte cap, WebP decoder and resize equality pass; QC contact/125-32px/neighbor comparisons programmatic only.
- **Crystal family archive:** `BR-020_Crystal_Essence_Bloodright_Proposed_3_Icons.zip` SHA-256 `a9f128fb80718044086f86a0f0f05c10310d9079c4735600e8ded40f68ab31bc` (5,507,297 bytes). Per-tier hashes and technical status in `BLOODRIGHT_WAVE03_BR020_PROPOSAL_QC_20261017.json`. **Pending director acceptance of the actual three images**; never auto-promote palette approval to artwork approval.
- **Progress: 12/29 families, 36/87 icons accepted; 17/29 / 51 icons remain.** All current binary artwork is still in conversation output packages, not Git-pinned artifacts. Strict skillTree.image validator, immutable imagePack, and live-game import/readback remain separate gates. No live requests/writes.

## 2026-10-17 — Tetsugan approval / Shakunetsu production checkpoint

- **BR-083 Tetsugan:** Director accepted all three Ward-Forged Steel tier images in the last review. Source PNG and WebP hashes remain exactly those independently reported at proposal; no approved artwork regenerated. Approved portable package `BR-083_Tetsugan_Bloodright_Approved_3_Icons.zip` SHA-256 `e9c209e4eb9dad187256b83d740463bf0414684fb628686dc6d7b651cd0351e3`; source hashes in `BLOODRIGHT_WAVE03_BR083_PROPOSAL_QC_20261017.json`. Original binaries in conversation portable archive, not immutable Git content.
- **BR-064 Shakunetsu Sakura:** Director-approved Midnight Blossomfire recipe applied in one coordinated local appearance pass to three verified Ethereal geometry masters. Three individual source PNGs, three lossless RGB 256px WebPs, programmatically composed 3-icon family preview, 125/64/32px QC and neighbor comparison. Each new tier exactly matches its master's maxRGB at every source pixel with threshold IoU=1.0; output hashes and QA status in `BLOODRIGHT_WAVE03_BR064_PROPOSAL_QC_20261017.json`. Portable family ZIP SHA-256 `e8a384182a4d927c42ac590ac7c91a7cbecc5bd7811dc2bce6340a1907d828b6`. **No BR-064 artwork accepted until director reviews the specific completed trio.**
- **Art acceptance:** 11/29 complete, 33/87 tier artworks; 18 families / 54 icons remain, inclusive of BR-064 pending. Strict `skillTree.image` field preflight, git-binary binding, immutable Forge imagePack, hidden import/readback and live publication are separate and remain open. Zero live requests/writes.

## 2026-10-17 — Reference intake completed

**Received directly from the operator:** all five expected ZIPs. Verified 5/5 ZIP archive CRC/path checks, 5/5 bloodline ID/rank and current tracked member identities, 31/31 jutsu source images and 5/5 identity image SHA-256/declared decoder format/dimensions; **36 individual source originals preserved without re-encoding**. Reviewed four individual jutsu sources and identity image for each family; inspected palette/material evidence rather than guessing from element names.

**Five themes proposed (not approved):** Tetsugan Ward-Forged Steel; Shakunetsu Sakura Midnight Blossomfire; Crystal Essence Prismatic Jadeglass; Suragu Obsidian Magma; Vaporia Hydrothermal Crucible. See `BLOODRIGHT_WAVE03_SOURCE_INTAKE_20261017.json` and `BLOODRIGHT_WAVE03_TREATMENTS_PROPOSED_20261017.md` for source hashes and full cards.

**Source-kit portable archive:** `Bloodright_Wave03_Source_Intake_And_Treatment_Proposals_20261017.zip` SHA-256 `27017bf5558e4dfad54695ebd18b93724f6ec5e71efc4cb6bb986d4476627844` (11,798,447 bytes), containing all five exact source-art ZIPs, previously verified geometry/reference starter, original-art comparison board, offline manifest/hash QC and treatment cards. Conversation binary, **not a Git-pinned source-art object**. ZIP CRC/member byte equality PASS.

**Next gate:** director review of BR-083 Tetsugan's complete Foundation/Hidden Art/Advanced Art trio. Exact per-tier raw/WebP SHA-256, source ZIP, QC and package hash are recorded in `BLOODRIGHT_WAVE03_BR083_PROPOSAL_QC_20261017.json`. Themes for all five families are approved; 1 family produced but no Wave 03 art is accepted yet.

## Input and production gates

1. **Source intake:** operator supplies original ZIPs; safe ZIP path/size inspection; validate source names, bloodline IDs, jutsu record IDs, manifests/individual image SHA-256 and ZIP CRC; open **2–4 actual jutsu images and bloodline identity art (if present)** for each family. No game/CDN request.
2. **Treatment proposal:** one compact five-bloodline source-grounded palette/material card each, with anchors and neighboring-family distinction. Director approves/revises the five cards; this is not automatically granted by prior Wave 2 palette approval.
3. **Three individual emblems per family:** Foundation elongated nested diamond; Hidden Art nested diamond + paired crescents/crosspieces; Advanced Art nested diamond + fixed multipoint starburst. Use verified 1254x1254 Ethereal approved reference masters and preserve fixed silhouette/landmarks/negative space. Only color, material, internal texture and controlled glow change. Opaque black remains approved.
4. **One coordinated production session per bloodline:** three separate original images; **no generatively drawn contact sheet**; apply a single approved treatment recipe. Compare each trio at 125/64/32px; do not relabel mismatched geometry without correct tier-to-file evidence.
5. **Comparative review:** programmatically compose a five-row × three-tier contact sheet from **exact, saved outputs**. Director accepts/rejects each bloodline separately. Preserve accepted raw bytes immutably; only revise rejected families.
6. **Offline export/QC:** three individual lossless RGB WebPs per approved family, currently 256x256 working format; codec, dimensions, SHA-256, byte caps, decoded pixel match to intentionally resized raws, black background and archive CRC. Run actual field-specific preflight when implemented, report errors honestly.
7. **Distribution boundary:** source-art Git binary pin, `skillTree.image` field preflight, Forge immutable imagePack, five-BP structural content and user-run hidden import/read-back are **Fable/operator gates**, not resolved by approving art. Zero live-game requests/writes.

**Current technical-source divergence:** new `JUTSU_ICON` alpha-optional target integrated on current `main` applies to **`jutsu.image` only**; it does **not** resolve the opaque RGB `skillTree.image` contract. This Wave 3 branch is descended from a separate art-lineage ref with older copies of generic art spec. At packaging, verify latest canonical spec/code; do not treat the older branch spec as a new authority.

**Repository integration caution:** the art branch carries an art-studio `RUL-2026-10-17-004` whose identifier conflicts with `main`'s unrelated import `RUL-2026-10-17-004`. Resolve ruling IDs and any authority differences before recommending merge; do not rewrite user decisions merely to silence a conflict. This branch is not yet an integration candidate.

## Portable reference starter (locally QC-verified)

- Conversation deliverable (not a Git binary): `Bloodright_Wave03_Production_Starter_20261017.zip`
- **SHA-256:** `baa13be126891971564952387e771a56a02aef0280fa2ee516b8ec60f04f8f30` (**6,395,153 bytes**)
- Contains **three separate 1254px verified geometry-reference masters** plus **21 previously accepted 256px lossless WebP comparisons** (six pilot, 15 Wave 02 including corrected Shiroi v02 role assignment).
- Manifest SHA-256s verified against preserved original source-package bytes; ZIP CRC and decoder/format checks pass. The package is intentionally light and contains **no Wave 03 jutsu source images** and **no newly generated icons**.
- All five Wave 03 source reference ZIPs have since been supplied, safely inspected and SHA/manifest-verified; see the intake checkpoint above. The previous-approved family colors are comparison evidence, not a palette prescription for an unseen target.
- The portable starter is not an immutable Git `imagePack` or technical sign-off for `skillTree.image`.

## Immediate next action

The director approved BR-083 Tetsugan and BR-064 Shakunetsu Sakura. **Present BR-020 Crystal Essence's three separately saved proposed Foundation / Hidden Art / Advanced Art images for director acceptance.** If approved, preserve their exact raw PNG and WebP hashes, package as accepted and continue with BR-074 Suragu using the verified source ZIP. No additional user palette ruling is necessary.

**Live game requests/writes:** 0/0. **Credentials:** none.
