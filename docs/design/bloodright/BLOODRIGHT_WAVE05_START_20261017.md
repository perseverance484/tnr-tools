# Bloodright Tier-Emblem Art Studio — Wave 05

**Status:** SESSION INITIALIZED / SOURCE-ART INTAKE PENDING. **Zero Wave05 icons produced, zero visual treatments proposed or approved.**
**Date:** 2026-10-17.
**Role:** Art Director (lead), Image Production (support). **Tooling/Forge:** Fable technical ownership.
**Repository:** `perseverance484/tnr-tools`.
**Branch:** `chatgpt/bloodright-wave05-art-studio-20261017`.
**Exact base:** `chatgpt/bloodright-wave04-art-studio-20261017@374589b77410a42384e9fe15ca625aa5913f5b0a` — Wave04 art closeout, frozen and not modified by Wave05.
**Main last verified:** `9a0970002a80531078ac5e4b0f72578d3f7855f5`; merge-base with art lineage `99e86dc549b86f1f4a5846c0e509fa6bc15b3463`. Reverify before handoff/integration.
**Authorities:** `docs/00_INDEX.md` (routing/evidence), `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/agents/ART_DIRECTOR.md`, `docs/agents/IMAGE_PRODUCTION.md`, `docs/workflows/BLOODRIGHT_ICON_STUDIO.md`, `docs/workflows/ART_PRODUCTION.md`, `skills/producing-tnr-art/SKILL.md`.
**Membership/kit snapshot:** `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866` / `docs/design/bloodright/roster.json`; queued order in `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md`.
**Prior approved state:** `docs/design/bloodright/BLOODRIGHT_WAVE04_CLOSEOUT_20261017.md`, `BLOODRIGHT_WAVE04_APPROVED_QC_20261017.json`.

## Confirmed baseline

- Exactly **20/29 Bloodright bloodlines visually approved, 60/87 universal tier icons visually approved** after Wave04; remaining **9 families / 27 icons**. These are **visual acceptance counts**, not game-ready technical preflight/Forge status.
- Wave04 five fully accepted families and their **15 exact original PNGs/15 lossless WebPs are frozen**. Their exact approved materials: Shinseina Ki Verdant Heartwood; Bakuhatsu explosive Red-Core V02; Oblivion Seal Voidscar Amethyst V02; Shadow Weaver near-black **Ebony Silk V03**; Heavenly Sonata Celestial Harmonics.
- **Wave04 geometry technical exception remains OPEN/RED:** nine visually accepted images (all three each of Shinseina Ki, Bakuhatsu red-core V02, Ebony Silk Shadow Weaver V03) **are not pixel-exact to the three universal geometry masters**. Do not secretly change or regenerate director-accepted artwork. Exact mask for Oblivion Seal and Heavenly Sonata is PASS (6/15).
- Wave02 Shiroi Youso has the **approved Hidden Art↔Advanced Art tier-role swap**, source bytes unchanged (`RoleSwap_v02`). Retain this role mapping.
- **Opaque black** background visually approved. **Three geometries locked:** Foundation nested elongated diamond; Hidden Art paired crescents and nested diamond; Advanced Art multipoint starburst and nested diamond. Only source-backed palette, material, contained texture and restrained chakra edge glow may change. Do not invent glyph geometry, exterior subjects, letters, rarity frame or redesigned jutsu imagery.
- A reusable deterministic general geometry-mask processor, `skillTree.image` field preflight, immutable binary Git pins and Forge imagePack bindings are NOT completed by visuals. The `JUTSU_ICON` optional-alpha spec governs `jutsu.image` only. No live requests or writes.

## Wave 05 — five upcoming source-art families (first 5 of remaining 9)

| Queue | ID | Bloodline | Rank | Pinned original public jutsu count | Elemental category *for navigation only* | Intake ZIP expected |
|---:|---|---|:---:|---:|---|---|
| 21 | BR-078 | Tenohira Musei | A | 5 | Yin-Yang | `BR-078_Tenohira_Musei.zip` |
| 22 | BR-005 | Arashima | A | 5 | Storm | `BR-005_Arashima.zip` |
| 23 | BR-065 | Shinrai Ou | A | 5 | Storm | `BR-065_Shinrai_Ou.zip` |
| 24 | BR-034 | Hyouga Yui | A | 5 | Ice | `BR-034_Hyouga_Yui.zip` |
| 25 | BR-077 | Teno Yuki | A | 5 | Ice | `BR-077_Teno_Yuki.zip` |

**Expected intake:** 5 original source-art ZIPs containing **25 actual jutsu images**, plus bloodline identity images if present. **None supplied for Wave05 at initialization.** The ZIP names above are suggested filenames, **not file-existence evidence**. Do not derive new treatment colors from name/classification alone.

### Source image evidence questions to resolve after receiving ZIPs

- **Tenohira Musei vs Heavenly Sonata:** both have Yin-Yang category; inspect specific material, emphasis and chroma before choosing a treatment distinct from Heavenly's indigo/cyan/rose/gold.
- **Arashima vs Shinrai Ou:** both Storm-category A ranks. Compare actual lightning/wind/cloud/energy textures and accent palettes across both original kits **in the same art-direction review**; avoid producing two nearly identical blue bolts or Godstorm Eclipse clones.
- **Hyouga Yui vs Teno Yuki:** both Ice-category A ranks. Compare actual crystal/frost/water/fan/combat signature across both original kits against **Blue Blade Eyes**' already-approved sapphire ice tier visuals; preserve three distinct identities.
- Compositional identity is universal three-tier geometry, not unique jutsu scenes; internal material and color differences must be legible at **125/64/32px**. User remains final art acceptance authority.

## Portable Wave 05 starter (not source intake)

`Bloodright_Wave05_Production_Starter_20261017.zip`, **SHA-256 `5054109d3142154f668ba60d8b0d201971d4b2a2e03fcf6f408dbf5568605a4b`**, **8,001,320 bytes**. Contains the **three exact individually approved 1254px geometry masters** (SHA pinned in Wave04 QC) + the **15 exact accepted Wave04 RGB lossless 256px WebP icons** for cross-family contrast, plus source hashes, Wave04 visual acceptance ledger, and programmatic showcase / thumbnail QC. **Does not contain any Wave05 original jutsu art, new emblems or game requests.** Files are conversation portable assets, NOT immutable Git image binaries.

## Workstation production and approval gates

1. **Receive ZIPs** from the director (individual or one larger ZIP). Inspect safe paths, ZIP CRC, name, bloodline ID/rank, individual jutsu IDs, image MIME/format/dimensions and raw SHA-256 hashes against manifests and pinned `roster.json`. No live-game requests.
2. **Inspect real source imagery**, ideally bloodline identity and 2–4 original jutsu icons each, then produce five compact, evidence-grounded palette/material cards with pairwise contrast to already-approved families. Do not assume palette from elemental tags.
3. Obtain **director treatment approval** for all five. No tier-emblem generation before treatment decision.
4. Produce **one coordinated family production pass** per bloodline, with **three individually saved original PNGs**, same accepted treatment recipe, and **frozen exact master silhouettes and negative space**. Use deterministic master-based material treatment rather than freeform regeneration by default. Every visual candidate must preserve correct tier assignment; no new imagery around tier geometry.
5. After each family: **programmatically** compose exact saved originals into family comparison; inspect at 125/64/32px and against neighboring visual identities. Director accepts/rejects each family specifically.
6. Preserve exact approved source bytes; produce lossless 256×256 RGB WebP exports and full SHA-256/decoded pixel/format/byte/CRC/geometry QC. **If a director visually accepts an image with non-exact geometry, record that disagreement and block strict-geometry claims; do not quietly alter it**.
7. After 4–6-family approval batch, assemble a **programmatic five-by-three** comparison and full/raw/WebP delivery. Fable owns reusable mask tooling, strict `skillTree.image` field technical acceptance, immutable Git art pins, Forge packages and structural evidence. User owns hidden import, read-back, live-game actions and final publishing.

## Following Wave 05

Remaining last four if Wave05 is completed: **BR-033 Houkyuken**, **BR-036 Itojinsei** (magnet comparison), **BR-002 Aerathiel**, **BR-040 Kyuko-sei** (dust comparison). These will be Wave06 or adjusted by the director; no art production without original source files.

**Safety/integration:** game reads 0; game writes 0; credentials none. The art branch's `RUL-2026-10-17-004` (reskin-factory ruling) has an ID collision with `main`'s independent `RUL-2026-10-17-004` (placeholder-element import); reconcile both user decisions before proposing a merge. Wave05 branch must not modify Fable's separate implementation branch.

## Immediate next action

**Request all five original Wave05 bloodline art ZIPs** from the operator. No Wave05 source intake or visual treatment review has occurred yet. When supplied, verify and open real artwork, propose a five-family treatment card batch for explicit director approval, then start BR-078 Tenohira Musei's isolated three-emblem production.
