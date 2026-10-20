# Living Lineages — Reference-First Presentation V2

**Status:** **DIRECTOR-APPROVED V2 REFERENCE-FIRST STRUCTURE — ALL 19 ORIGINAL ART SOURCES PLACED INTO 26 SVG SLOTS** (2026-10-20). Populated sheet still awaits final visual acceptance; no game-upload readiness.  
**Owner:** Art Director / ChatGPT workdesk; no Fable code changes.  
**Supersession:** **RUL-2026-10-20-006** locks the 2048×1980 reference-first V2 as the **current director-approved poster structure**. The previously accepted 1536×1024 V1 remains historically approved/unchanged, but is no longer the active sheet. V2 acceptance is not automatic acceptance of the filled poster.  
**Output:** Approved structure `TNR_Living_Lineages_Kitsune_Concept_Flow_Structural_V2_20261020.svg` (2048×1980; original SVG SHA-256 `af59059ec42d6c4768a8eea70e315b897f43a58f2a5f20e95c7dba34ebaf0969`). Filled self-contained editable vector poster `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_20261020.svg` (SHA-256 `09c59f759ed3c7a33c408cba39232feff6eddeb02546fe7f2fc2478496d6cb00`) plus PNG and exact-source ZIP. Binary files are **conversation deliverables, not Git-pinned**; source hashes and placement metadata live in the repository. The unfilled source template contains zero animal illustrations.

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

**V2 status:** exact structure **DIRECTOR APPROVED** by “Structure approved. Insert images.” (RUL-2026-10-20-006). The approved source geometry is preserved and source-filled with 19 exact-origin animal images/26 locations. The whole **populated sheet** still awaits a separate director acceptance. The earlier V1 SVG/slot map stay intact as archived accepted direction.

## New artwork received during this redesign

The director supplied five files accompanying “Here's the rest.” Four are individual original Moonlit R2/R3 and Jade R2/R3 images. The fifth is a **single wide image with both Obsidian forms side-by-side**. All five decode as JPEG/RGB with opaque black backgrounds despite `.png` names. See [variant intake record](LIVING_LINEAGES_VARIANTS_R2_R3_INTAKE_20261020.md) for byte hashes and source limitations.

**Historical intake clarification (now resolved):** At the time of that first group upload, only one paired Obsidian file existed. The director **subsequently supplied two separate full-size original Obsidian images**, which are now used independently: `1000018916.png` (R2 Scout; JPEG SHA-256 `70c541d0b0a3e6167f60bf5b5c5edf77a18983223dd2976ac3ad9f997db8278b`) and `1000018917.png` (R3 Tracker; JPEG SHA-256 `20ce9623607b6e1aef6e143003b88162036605b0bb7c7bd77b8af79ab1a27602`). **No crops from the old two-creature composite were used.**

**Visual acceptance remains distinct:** Species reference plus four individual Rank 1 founders = **5 explicitly approved originals**. Ember R2–R9 (8), Moonlit/Jade R2–R3 (4), and Obsidian separate R2/R3 (2) are **selected and inserted** at the director's instruction but not retroactively tagged with independent game-ready art approvals. 19/19 originals now exist; the **filled poster's final visual signoff** and any production asset preflight remain pending.

## Production boundary

Director explicitly accepted **relaxed style/QC for exploratory art batches**; this does not waive truthful source provenance, accepted-asset records, deterministic poster assembly or the game's actual upload rules. The proposed rank-image inheritance is an explanatory model, not tool execution evidence. No game requests/writes, player attempts, credentials, content publication, or source-avatar repaints.

## Frozen populated V2 delivery and traceable source composition

**Current source-of-truth delivery document:** [Kitsune V2 Filled Poster Source/Placement Evidence](LIVING_LINEAGES_KITSUNE_POSTER_V2_FILLED_DELIVERY_20261020.md). Its source SHA table includes every original and the new standalone Obsidian R2/R3 files, while the [approved V2 placement map](LIVING_LINEAGES_KITSUNE_CONCEPT_FLOW_V2_SLOT_MAP_20261020.json) binds **19 originals to 26 display slots** and identifies each deterministic cutout SHA.

**Self-contained SVG:** `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_20261020.svg` (SHA-256 `09c59f759ed3c7a33c408cba39232feff6eddeb02546fe7f2fc2478496d6cb00`). Its **19 unique cutout PNGs are embedded once in SVG defs**, then referenced by 26 SVG use nodes: no regenerated artwork or pasted screenshot. The original accepted V2 headings, input choices, official rank labels, arrows, three-section organization and precise slot geometry are visually unchanged.

**Source archive:** `TNR_Living_Lineages_Kitsune_Poster_V2_FILLED_Sources_20261020.zip` (SHA-256 `347dc2d10b6a5335b3e0b0411e01abebf16ad6911c101586b98f787c93e9b01c`), containing 19 exact original RGB JPEGs, 19 presenter-only alpha derivatives, preview, SVG, original structural source, manifest and local rebuilding instructions. This archive is a **conversation deliverable**, not a Git binary pin.

**Acceptance ledger:** Structural design = **APPROVED**; inserting these original images = **DIRECTOR AUTHORIZED and COMPLETE**; fully composed poster visual acceptance = **PENDING**; TNR production export/preflight/live-game deployment = **NOT RUN / NOT AUTHORIZED**.
