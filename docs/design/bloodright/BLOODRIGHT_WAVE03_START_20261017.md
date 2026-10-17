# Bloodright Tier-Emblem Art Studio — Wave 03 Intake

**Status:** INITIALIZED / SOURCE ART PACKS NOT YET SUPPLIED — no visual treatment or generated icon approved for this wave.
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

## Immediate next action

Request the five original bloodline art ZIPs, or a single outer ZIP containing them, then begin verification and issue the five **source-grounded** treatment cards. No generated Wave 3 artwork exists yet.

**Live game requests/writes:** 0/0. **Credentials:** none.
