# Bloodright Tier-Emblem Art Studio — Wave 05

**Status:** Five original reference ZIPs verified, all five material treatments director approved. BR-078 Tenohira Musei and BR-005 Arashima **Stormcloud V02** complete three-icon families specifically VISUALLY APPROVED and exact original art bytes preserved; overall **22/29 families, 66/87 tier icons** accepted. BR-065 Shinrai Ou Raijin Whitebolt complete three-icon geometry-exact proposal and lossless WebP exports QA PASSED, awaiting specific director visual acceptance. Arashima V02 raw geometry differs from locked pixel masters; strict mechanical gate remains BLOCKED (12 visually accepted exception icons across Waves 4/5).
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

## 2026-10-17 — Arashima Stormcloud V02 acceptance / Shinrai Whitebolt proposal

- **Arashima BR-005 director approval:** earlier Midnight Tempest V01 marine-blue rain-glass icons were visually rejected as too similar to Blue Blade Eyes. The director requested heavier **storm cloud** material and then approved three newly generated cloud-and-blue-lightning images with **“Perfect. Approved, next”**. Exact original PNGs were recovered from each individual generated image's saved backing file ID (including the advanced image originally sharing a local filename with Hidden Art); all three sources are preserved **byte-for-byte unchanged** and processed into three RGB 256px VP8L lossless WebPs. Both original PNGs and WebPs passed source SHA, decoder, raw resizing pixel equality, file cap, corner black and ZIP CRC. `BR-005_Arashima_Bloodright_Approved_Stormcloud_v02_3_Icons.zip`, SHA-256 `50d3f7bce75f789ffd2a48bb334a6480170cee01112781a1791585c6ea91b09b`. Durable per-tier hashes, originating file IDs and approval: `BLOODRIGHT_WAVE05_BR005_STORMCLOUD_V02_APPROVED_QC_20261017.json`; previous V01 QC marked rejected/historical.
- **Geometry exception:** Arashima's three exact user-approved original V02 PNGs **FAIL** per-pixel universal master maxRGB and mask threshold overlap (threshold-128 IoU approx 0.458, 0.504, 0.597). This is **not** silently forgiven by visual acceptance and does not authorize a pixel-altering correction without renewed director review. Together with Wave04's 9 accepted-but-nonexact images, there are **12 image icons with exact-master geometry red** pending separate resolution.
- **BR-065 Shinrai Ou:** approved **Raijin Whitebolt** material recipe applied in one coordinated deterministic image-processing pass to all three **exact 1254px frozen Ethereal tier masters**; cobalt thundersteel and bright silver-white electrical seams make a deliberate contrast with Arashima's raincloud energy. Three individually saved original PNGs, 3 lossless RGB 256px WebPs; original 5-jutsu+identity pack manifest/CRC/bytes/decoder PASS. Pixelwise original master maxRGB EXACT 3/3; six binary intensity thresholds IoU 1.0 per tier; WebP decoder/pixel resized equality, black corners and byte cap PASS. Programmatic exact-source 3-icon comparison, 125/64/32px QC and direct Arashima Stormcloud vs Shinrai and Tenohira foundation comparison. No newly generated icon collage.
- **Independent archive QA:** separate auditor completed **188 assertions PASS, 0 FAIL** across accepted Arashima V02 and Shinrai proposal, explicitly checking Arashima's **failure** and Shinrai's **pass** on geometry. Shinrai proposed ZIP `BR-065_Shinrai_Ou_Bloodright_Proposed_3_Icons.zip` SHA-256 `1122bf2caf0a3a6262e9f189eb1bb9c31403978e505447c59fe402efe19bbfae`. Full tier hashes in `BLOODRIGHT_WAVE05_BR065_PROPOSAL_QC_20261017.json`. **Final Shinrai artwork acceptance PENDING**, no count increase from its three proposals.
- **Visual progress:** 22/29 Bloodright families accepted, 66/87 tier icons; 7 families / 21 icons remain, including the three pending Shinrai images. Strict `skillTree.image` field preflight, immutable Git art binary pins, Forge imagePack/structural import, and all operator game actions remain NOT DONE. No live requests/writes, no credentials.

## 2026-10-17 — Tenohira art approval / Arashima proposed

- **Tenohira Musei APPROVED:** director accepted the exact previously submitted three-image Equinox Rift family. No raw source or WebP artwork bytes modified, and all six SHA-256s unchanged from reviewed proposal. Approved portable archive `BR-078_Tenohira_Musei_Bloodright_Approved_3_Icons.zip` SHA-256 `e6694ecad239bb6a61ef89a79992b5b71ea0e26560f49cd7230384b9a9a95180`. Per-tier hashes `BLOODRIGHT_WAVE05_BR078_PROPOSAL_QC_20261017.json`; acceptance/showcase manifest labels updated, preview constructed programmatically from saved approved originals.
- **Arashima Midnight Tempest:** original five-jutsu + identity source ZIP SHA `75cb6c9d01f77164819a19e5cfae8c6409a4bf89e3461393cc9d48f3accc922d` revalidated offline. A coordinated marine/cyan rainstorm material recipe generated **three independent 1254×1254 original PNGs and separate 256×256 RGB lossless WebPs** from the approved universal Ethereal tier geometry masters. **All three pixelwise source master maxRGB masks exact** (6 absolute thresholds each). Programmatic family/125-64-32/adjacent family comparison from exact saved images only; no generated comparison reinterpretation. Independent offline audit passed **115 file/source/format/binary preservation/geometry assertions, 0 failures** including the six already-accepted Tenohira binaries unchanged.
- **Proposal only:** `BR-005_Arashima_Bloodright_Proposed_3_Icons.zip` SHA-256 `3c7be6392908fa7f74a28e8a5cbb34f6d4acb8f09dbc5af3367b112bc95a99bc`. Contains exact separate originals/exports, original source ZIP, all three master references, programmatic QC views, production script and independently verifying auditor. Raw/export per-tier SHA-256 and field gates recorded in `BLOODRIGHT_WAVE05_BR005_PROPOSAL_QC_20261017.json`. Director **specific trio visual acceptance required**; do not count until approved.
- **Progress:** 21/29 families, 63/87 visual icon approvals; 8 families / 24 icons remaining. BR-005 is not counted. `skillTree.image` field-specific preflight/alpha question, immutably Git-pinned art binaries and Forge imagePack remain open Fable gates; nine Wave04 visually approved/geometry-nonexact icons unchanged. No game reads/writes or credentials.

## 2026-10-17 — Five theme cards approved / Tenohira Musei produced

- The director **approved all five source-grounded material treatments**: Equinox Rift, Midnight Tempest, Raijin Whitebolt, Cerulean Shatter, Winterglass Sanctum. This is palette/material approval only, not specific finished image acceptance.
- **BR-078 Tenohira Musei:** its actual source-art ZIP was re-opened, verified against SHA-256 `24d390da8c756f2707b09249fbffe637083b42f389eaebac1d4e980d07d64f92`, CRC, five expected jutsu IDs, source image bytes/MIME and six declared dimensions. A single deterministic fixed-mask appearance recipe produced separate **Foundation, Hidden Art and Advanced Art original 1254px PNG files**, each with electric blue LEFT and solar-orange RIGHT chakra currents and moon-white original crossing glow. Geometry matches the three approved Ethereal masters at **every per-pixel maximum RGB channel and all six exact intensity threshold masks**, all tiers.
- Each raw original has a **256px lossless RGB VP8L WebP**, original PNG raw bytes untouched. QC sheets at 125/64/32px and cross-family **Vaporia / Heavenly Sonata** comparison are programmatically composed, never newly drawn. Independent offline checker completed **109 assertions PASS / 0 FAIL** for source ZIP, raw SHA/bytes, exact master geometry, lossless decoded equality, black corners, 460800-byte working cap and portable package original-member integrity.
- Proposed family package `BR-078_Tenohira_Musei_Bloodright_Proposed_3_Icons.zip` SHA-256 `10e7a5262b8b5dc708086915b5f0f1e4313a51fac68fbb4fa9b1dbbabb068573` (10,078,736 bytes), includes all raw/WebP assets, source and geometry references, manifest, reproducing Python script, independent auditor and QC. Detailed immutable raw/export hash evidence: `BLOODRIGHT_WAVE05_BR078_PROPOSAL_QC_20261017.json`. **Director final trio artwork acceptance is still PENDING**, so overall visually approved totals remain 20/29 families, 60/87 icons.
- **Separate technical gates:** actual `skillTree.image` field validator/preflight remains unknown and unrun; approved opaque-black art does not waive alpha rule; Git art binary/source pin, immutable Forge imagePack, structural import and live-game readback remain Fable/operator tasks and uncompleted. Previously approved nine Wave04 nonexact-master geometry icons unchanged. No game requests/writes.

## 2026-10-17 — Verified intake and treatment proposals

- All five original Wave05 bloodline art ZIPs are now received and safely inspected offline. **305 checks passed, zero failures** across archive CRC/path integrity, actual image SHA-256 and bytes, decoded format/dimensions, pinned bloodline and jutsu IDs. **25 original jutsu images + five identity images** inspected. The historic game-capture metadata in archive manifests remains a provenance claim, not a new live request.
- Five proposed visual treatments: **Equinox Rift** (Tenohira Musei), **Midnight Tempest** (Arashima), **Raijin Whitebolt** (Shinrai Ou), **Cerulean Shatter** (Hyouga Yui), **Winterglass Sanctum** (Teno Yuki). Each is grounded in real supplied imagery; the storm pair and ice pair need side-by-side thumbnail contrast.
- Canonical evidence: `BLOODRIGHT_WAVE05_SOURCE_INTAKE_20261017.json`. Full source-grounded cards: `BLOODRIGHT_WAVE05_TREATMENTS_PROPOSED_20261017.md`.
- Portable file: `Bloodright_Wave05_Source_Intake_And_Treatment_Proposals_20261017.zip`; SHA-256 `378f26713655c449084750d35265a9390b394b1bfee66eb590bb8057adefcc29`. All five exact source ZIPs, prior approved geometry masters/reference bundle, original-art boards, package manifest and treatment cards. Conversation artifact, **not Git-pinned accepted binary art**.
- **Director palette/material approval PENDING. No Wave05 tier icons produced; no game requests/writes.**

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

Tenohira Musei and revised stormcloud Arashima families are director visually approved, with their raw art bytes preserved. **Present Shinrai Ou's complete three-icon Raijin Whitebolt fixed-geometry family preview for director visual acceptance**, with direct programmatic Stormcloud Arashima comparison and 125/64/32 QC. Once accepted, retain Shinrai exact original PNG/WebP SHA-256s and proceed to Hyouga Yui (approved Cerulean Shatter) and its contrasting ice peer Teno Yuki. Do not mark 3 proposed Shinrai icons accepted early. Strict `skillTree.image` preflight, Git source pin, Forge imagePack and live operations remain separate.
