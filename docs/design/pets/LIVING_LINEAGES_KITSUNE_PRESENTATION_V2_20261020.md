# Living Lineages — Reference-First Presentation V2

**Status:** DIRECTOR-DIRECTED STRUCTURAL REDESIGN, **DRAFT AWAITING LAYOUT ACCEPTANCE** (2026-10-20).  
**Owner:** Art Director / ChatGPT workdesk; no Fable code changes.  
**Supersession:** Preserve the director-approved 1536×1024 V1 SVG and ruling RUL-2026-10-20-004 intact. **V2 is a new draft, not a silent replacement.**  
**Output:** `TNR_Living_Lineages_Kitsune_Concept_Flow_Structural_V2_20261020.svg` (2048×1980), its deterministic PNG preview and 26-slot map, created as conversation artifacts. **The SVG binaries/source are not yet pinned in Git; once the director accepts V2, archive the exact version rather than recreating a generative composite.** The template contains zero animal illustrations.

## Director's presentation correction

The poster should first teach **what the proposed system does**, not jump directly to a grid of rank pictures. There is **ONE APPROVED SPECIES REFERENCE** for Kitsune (a neutral juvenile fox master; not a rank). Each player independently supplies **their actual supported cosmetic selections**: palette, characteristic/marking, aura. The same base **plus those selections and the staff-authored Rank 1 concept** generates unique player-owned Rank 1 art. The resulting companion has its own unique image; each further rank-up uses **its own previous appearance**, not the common species master and not another player's pet.

All four variant images are **example outcomes**, not actual player records and not fixed species-specific presets. Do not imply the supplied art proves the **live generator already supports** this proposed source-image/staff-editable rank-concept workflow.

## V2 structural narrative — three educational sections

**01 — ONE SPECIES → PLAYER INPUTS → FOUR EXAMPLE RANK 1 OUTPUTS**

One visually distinct master image `SPECIES_REF` sits on the left with label **“Not a rank · no fixed palette”**. A central player-selection block explicitly shows **Palette / Characteristic / Aura**. Four labelled **EXAMPLE** cards branch to `A_R01` Ember, `B_R01` Moonlit, `C_R01` Jade and `D_R01` Obsidian. Each example prints the exact cosmetic choices (table below). Never recolour the shared species master into four different “species references.”

**02 — FOUR INDIVIDUAL IMAGE INHERITANCE PATHS, RANKS 1–3**

Four rows (Ember, Moonlit, Jade, Obsidian); three columns:
- Rank 1 **Companion:** species base + player cosmetic choices -> an individually generated fox.
- Rank 2 **Scout:** this **individual's accepted Rank 1** + shared Scout morphological concept -> a growing yearling, two tails.
- Rank 3 **Tracker:** this **individual's accepted Rank 2** + shared Tracker morphological concept -> an adolescent runner, three tails.

The original species master is **not repeated** in every lineage row: the common foundation is already shown once above. Same image source reused in multiple slots is an exact source file, never a new generated approximation.

**03 — ONE LONG-TERM EXAMPLE: EMBER RANK 1–9**

Nine sequential art slots `A_R01` through `A_R09`, using the game names `Companion, Scout, Tracker, Guardian, Hunter, Warden, Sentinel, Mythic, Sovereign`. **Growth R1–4**, followed by **metamorphosis/development R5–9**. Milestone emphasis: **Hunter R5, Sentinel R7 and Sovereign R9**. Rank 10 out of scope. Ember is the only full nine-rank example; other lineages are deliberately R1–3 only for this presentation.

| Example | Palette | Characteristic / marking | Aura |
| --- | --- | --- | --- |
| Ember | Ember (0) | Pale tips (10) | Wind (0) |
| Moonlit | Moonlit (1) | Crescent marking (1) | Moon (5) |
| Jade | Jade (10) | Mismatched eyes (5) | Lightning (4) |
| Obsidian | Obsidian (9) | Dappled accents (9) | Spirit (7) |

**Rank and cosmetic authority:** `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11`, `app/drizzle/constants.ts` and `app/src/libs/pets/catalogue.ts`. These are example saved-choice combinations, not live player capture/rolls.

## Exact-source placement plan

V2 uses **26 SVG image placements** backed by **19 distinct asset IDs**:
- Foundation: **1** shared species reference (shown exactly once).
- Four R1 example cards: **4**.
- Four rows × R1/R2/R3: **12**.
- Ember R1–R9 full path: **9**.

Duplicated appearances (e.g. Ember R1 in example card, R1–3 comparison, and full path) must use the **same exact artwork** and remain traceable in the slot map. No generated poster recomposition.

**V2 status:** structurally drafted, XML parsed and preview rendered at 2048×1980; final director visual acceptance **PENDING**. V1's approved SVG/slot map stay untouched. If accepted, V2 becomes the current presentation direction via a new durable ruling.

## New artwork received during this redesign

The director supplied five files accompanying “Here's the rest.” Four are individual original Moonlit R2/R3 and Jade R2/R3 images. The fifth is a **single wide image with both Obsidian forms side-by-side**. All five decode as JPEG/RGB with opaque black backgrounds despite `.png` names. See [variant intake record](LIVING_LINEAGES_VARIANTS_R2_R3_INTAKE_20261020.md) for byte hashes and source limitations.

**Do not count the five sources as six independent original images.** Proposed left Obsidian image = R2 and right = R3, but separate original images are absent. Before deterministic final population choose either separately supplied originals or a **director-authorized exact-source split/crop** with derived-source hashes. Do not invent Obsidian artwork or mark cropped substitutes as untouched originals.

**Visual acceptance remains distinct:** Previous species + four founders = 5 director-approved. Ember R2–R9 remains an eight-image provisional batch pending explicit director acceptance (workdesk source status). Four new Moonlit/Jade rank images and Obsidian composite remain submitted candidates, not automatically approved or game-export ready.

## Production boundary

Director explicitly accepted **relaxed style/QC for exploratory art batches**; this does not waive truthful source provenance, accepted-asset records, deterministic poster assembly or the game's actual upload rules. The proposed rank-image inheritance is an explanatory model, not tool execution evidence. No game requests/writes, player attempts, credentials, content publication, or source-avatar repaints.
