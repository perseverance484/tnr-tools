# Bloodright Tier-Emblem Art Studio — Wave 04 Start

**Status:** FIVE VERIFIED SOURCE PACKS, FIVE MATERIAL TREATMENTS DIRECTOR APPROVED. BR-066 SHINSEINA KI 3/3 VISUALLY APPROVED (accepted originals preserved) / STRICT GEOMETRY-MASTER QC FAIL; BR-008 BAKUHATSU 3/3 PROPOSED WITH EXACT GEOMETRY QC PASS, DIRECTOR ART ACCEPTANCE PENDING. Overall 16/29 families and 48/87 icons VISUALLY APPROVED; game preflight unverified.
**Date:** 2026-10-17
**Lead:** ChatGPT Art Director · **Support:** Image Production · **Technical implementation:** Fable / Claude Code
**Repository:** `perseverance484/tnr-tools`
**Studio branch:** `chatgpt/bloodright-wave04-art-studio-20261017`
**Base:** `chatgpt/bloodright-wave03-art-studio-20261017@47e6a374478654d93fdf7d6d15e3f1ee68730955` (frozen Wave 03 art closeout).
**Main verified:** `9a0970002a80531078ac5e4b0f72578d3f7855f5`; branches diverge at `99e86dc549b86f1f4a5846c0e509fa6bc15b3463`.
**Authority:** `docs/00_INDEX.md`, `docs/workflows/BLOODRIGHT_ICON_STUDIO.md`, `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md`, `docs/design/bloodright/BLOODRIGHT_RESKIN_FACTORY_PROPOSAL_20261017.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md` and `skills/producing-tnr-art/SKILL.md`.
**Source-ID pin:** `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866` (`docs/design/bloodright/roster.json`). Neither this historical pinned roster nor jutsu artwork automatically approves gameplay mechanics.

## Brought forward, frozen

- **15/29 bloodlines, 45/87 universal tier emblems individually visually approved** through Wave 03 (51.72%). **14 families / 42 icons remain.** No old artwork to regenerate.
- Wave 02 BR-067 Shiroi Youso: Hidden Art and Advanced Art **source-file tier roles swapped only**, not image pixels; final portable names `RoleSwap_v02` remain the accepted binding. No mechanical permission inferred.
- One original per tier/bloodline: Foundation = long nested diamond; Hidden Art = diamond + paired inward-curved crescents/crosspieces; Advanced Art = nested diamond + multipoint starburst. **The three geometries, spacing, negative space and tier-role mapping are LOCKED.** Only palette/material/internal texture and restrained glow vary.
- Opaque black / near-black backgrounds are approved. No image generation contact sheets, external subjects, fantasy glyph reinvention, letterforms, UI frames, rarity backgrounds or rework of the original bloodline jutsu icons.

## Wave 04 original-art intake — verified

| ID | Family | Rank | Jutsu ZIP | Treatment proposal |
|---|---|---|---|---|
| BR-066 | Shinseina Ki | A | `BR-066_Shinseina_Ki.zip` | **Verdant Heartwood** — amber wood, jade/chartreuse living sap and gold tree-bark reflections |
| BR-008 | Bakuhatsu | A | `BR-008_Bakuhatsu.zip` | **Detonation Core** — scorched copper, contained kinetic orange, white-hot flare, rare blue static |
| BR-053 | Oblivion Seal | A | `BR-053_Oblivion_Seal.zip` | **Voidscar Amethyst** — black-violet cursed stone, saturated ultraviolet cracklight, pale lavender fractures |
| BR-063 | Shadow Weaver | A | `BR-063_Shadow_Weaver.zip` | **Moonless Filament** — near-monochrome smoky graphite with subtle silver/lilac internal filaments |
| BR-032 | Heavenly Sonata | A | `BR-032_Heavenly_Sonata.zip` | **Celestial Harmonics** — indigo opal, cyan-blue resonance, rose and amber-gold overtones |

All five operator-provided original source ZIPs were opened **offline**, CRC/path/member-safety checked, and independently matched against their internal image SHA-256/byte/decoder/dimension manifests and against the approved pinned bloodline IDs + exact jutsu IDs. **195 checks passed, zero failures**. The verified set contains **25 original bloodline jutsu images and five identity images**. Individual identity and several original jutsu images per family were opened and visually inspected; contact boards re-display those exact pixels resized, not AI-redrawn variants. Source pack manifests carry historical live capture references, but their original capture bundles were **not re-harvested or separately authenticated in this pass**.

### Important art distinctions

- **Shinseina Ki** reads as warm carved heartwood with green sap; avoid Crystal Essence's transparent aqua/jade glass or literal tree branches beyond the glyph.
- **Bakuhatsu** is a concentrated detonation, not a Taiyo solar disc or Suragu molten basalt. An optional tiny blue accent is justified by Charge 4 Explosion, but orange/white firepower remains dominant.
- **Oblivion Seal** is *bright violet curse fractures*; **Shadow Weaver** is a *restrained charcoal/silver-lilac weave*. Comparing these two at 125/64/32px is mandatory to prevent two indistinguishable purple-shadow sets. No external spider webs, portals, weapons or living actors.
- **Heavenly Sonata** is harmonically tuned blue/rose/gold opal. The original musical note imagery supplies color/energy behavior, **not permission to insert musical-note shapes** into our locked emblems.

## Portable intake evidence

`Bloodright_Wave04_Source_Intake_And_Treatment_Proposals_20261017.zip` **SHA-256 `2c069292bce539e6cf323be12d354df41465f81299e6e62fb3bf5417ae18bd8a`** (10,246,336 bytes) contains original five ZIPs, complete `SOURCE_INTAKE_QC.json` including 30 individual pixel hashes, full treatment cards, programmatically composed source-and-palette board, the **three exact approved geometry-reference masters** and 15 accepted Wave 03 WebP comparison assets. Package manifest gives exact bytes/SHA of every member. Conversation deliverable, **not Git-pinned binary source**. Canonical ledger: `BLOODRIGHT_WAVE04_SOURCE_INTAKE_20261017.json`.

## 2026-10-17 — First Wave 04 family approved; next fixed-geometry trio produced

- **Director approved all five source-grounded treatments.** Any prior intake headings saying "proposed / approval needed" refer only to the initial gate and are superseded by this production checkpoint; only specific new artworks remain individually subject to director review.
- **Shinseina Ki:** image-generated Foundation, Hidden Art, Advanced Art individually saved as exact original PNG bytes (1254px) with original image-generation IDs captured. Visually approved as a family. 3 lossless 256px RGB WebPs exported from these exact raw files; source ZIP hash, VP8L lossless, pixel equality, byte caps and 125/64/32 thumbnail QC pass. Portable `BR-066_Shinseina_Ki_Bloodright_Approved_3_Icons.zip` SHA-256 `70df07a09b2e06d17705ea08871bf6b2b8e081fee1a5364e0baa0702c0397085`. **Exact master geometry QC FAIL for all three**, despite visual approval (they are coherent interpretations of the glyphs, but they did not preserve the source brightness mask pixelwise). Details/IoU in `BLOODRIGHT_WAVE04_BR066_APPROVED_QC_20261017.json`. **Do not silently alter approved raw bytes**, and do not treat visual approval or size/export validity as `skillTree.image` technical acceptance. If strict shape fidelity is needed for binding, correction requires a separate director-approved rework.
- **Bakuhatsu:** approved Detonation Core palette applied with a **deterministic pixel-brightness-preserving** appearance transform of all three master raw PNGs. Individually saved 1254px RGB originals and 256px lossless RGB WebPs; all maxRGB pixels match their original approved tier masters, threshold IoU=1.0 at six levels for each of three icons; source art ZIP hash, image decoder/CRC, WebP pixel equality, byte budget and black corners passed. Preview and neighboring-family comparison composed only from exact saved outputs, never generated as new art. Portable proposal `BR-008_Bakuhatsu_Bloodright_Proposed_3_Icons.zip` SHA-256 `4b1e32cea6e2100aedd80fdafadbd0e35a16077c14918bf6ecd0c30299863c99`. Raw/export hashes and status in `BLOODRIGHT_WAVE04_BR008_PROPOSAL_QC_20261017.json`. **Director final image approval PENDING.** Note visual proximity to Suragu's source-grounded orange magma and assess contrast during review before freezing.
- **Counts:** visually approved `16/29` families and `48/87` symbols; Wave 04 produced six individual raw artwork candidates, three accepted, three proposed, zero family-specific `skillTree.image` preflights complete. Git art binary pins and Forge binding remain independent Fable tasks; no game requests/writes.

## Next production gate

**Director review of BR-008 Bakuhatsu's exact three individually saved proposed emblems is next.** All five Wave 04 source-backed palette/material treatments were already approved. The BR-066 Shinseina trio has been director visually approved and byte-preserved, but its machine-exact geometry gate is still RED. Keep that exception visible; do not silently stencil approved raw pixels or mark the set Forge-ready. Once Bakuhatsu is approved/revised, proceed to BR-053 Oblivion Seal's approved Voidscar Amethyst treatment. Continue per-family acceptance, 125/64/32px/neighbor contrast QC and programmatic five-family comparisons from approved originals.

**Technical boundary:** `JUTSU_ICON` alpha-optional rule on current `main` applies to `jutsu.image`, not the future Bloodright `skillTree.image` field. Strict field-specific `skillTree.image` preflight, immutable art/source Git pins, Forge imagePack and hidden structural imports remain Fable/operator-owned and **not done**. The art-lineage `RUL-2026-10-17-004` conflicts with current main's unrelated same-number Bloodright placeholder-element ruling; preserve both and reconcile before any merge.

**Live-game requests/writes:** 0/0. **Credentials:** none. **Repository integration or live-game publication:** not authorized.
