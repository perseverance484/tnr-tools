# Bloodright Tier-Emblem Art Studio — Wave 04 Start

**Status:** SOURCE INTAKE VERIFIED / FIVE MATERIAL TREATMENTS PROPOSED / DIRECTOR DECISION REQUIRED. **Wave 04 art generated: 0/15.**
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

## Next production gate

**Director approval of the five Wave 04 material/appearance treatment cards** is needed before generating any emblems. Once approved: one clean coordinated production session per bloodline with **three individually saved tier originals**; same approved recipe across Foundation/Hidden Art/Advanced Art; machine compare to the exact masters, inspect 125/64/32px and adjacent families. Compose a 5×3 batch review **programmatically** from the exact saved images. Director accepts **each trio separately**, and accepted source bytes are preserved immutable. Lossless WebP export, final package QC and original SHA manifest follow acceptance.

**Technical boundary:** `JUTSU_ICON` alpha-optional rule on current `main` applies to `jutsu.image`, not the future Bloodright `skillTree.image` field. Strict field-specific `skillTree.image` preflight, immutable art/source Git pins, Forge imagePack and hidden structural imports remain Fable/operator-owned and **not done**. The art-lineage `RUL-2026-10-17-004` conflicts with current main's unrelated same-number Bloodright placeholder-element ruling; preserve both and reconcile before any merge.

**Live-game requests/writes:** 0/0. **Credentials:** none. **Repository integration or live-game publication:** not authorized.
