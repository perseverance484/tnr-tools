# Living Lineages — Kitsune four-lineage demonstration

**Status:** VISUAL PILOT ACTIVE — **19 unique art images** required for the final two-panel sheet (instead of original 37). Juvenile master plus Ember and Moonlit Rank 1 visually approved; **Jade Rank 1 next**. SVG template is STRUCTURAL DRAFT pending director acceptance; no game writes or transparent production exports.  
**Lead:** Art Director; support: Image Production.  
**Ownership:** This register + [37-slot machine-readable history ledger, 19 active assets](LIVING_LINEAGES_KITSUNE_SLOTS_20261020.json), [editable SVG layout](LIVING_LINEAGES_KITSUNE_SHEET_STRUCTURAL_20261020.svg), and [26-placement slot map](LIVING_LINEAGES_KITSUNE_SHEET_SLOT_MAP_20261020.json) belong to the ChatGPT-owned workdesk branch. The JSON ledger owns approval and parentage; this register owns direction; the SVG/slot map own presentation structure. No Fable-branch or game-state writes.  
**Scope:** Concept-art proof, not deployed generation behavior, live records, balance or publishing. **Live-game requests/writes: 0. Credentials: none.**

## Evidence and pinned authority

- Shared repository baseline verified on 2026-10-20: `main@e13bc9fa085b37bd84ab7736256da8d1ad2a4a99`.
- Pet research and juvenile restart source: `chatgpt/premium-pet-visual-prompt-proposal-20261020@f8059013dc44f26e4e0bd6f09bfec4b7fb6dc601`, merge-base `e13bc9fa085b37bd84ab7736256da8d1ad2a4a99`.
- Public **pinned source**, **not** a live species capture: `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11`: `app/drizzle/migrations/0090_pet_companions.sql` seeds `pet-species-65` as LEGENDARY Kitsune, a mythical fox spirit with multiple distinct attached bushy tails; `app/drizzle/constants.ts` gives exactly ten named pet ranks; `app/src/libs/pets/catalogue.ts` supplies the saved cosmetic indices/wording; `app/src/libs/pets/appearance.ts` describes current renderer behavior.
- Proposal hierarchy: [one-page reference evolution](PET_ART_REFERENCE_EVOLUTION_ONE_PAGE.md) and [juvenile reset](KITSUNE_JUVENILE_GROWTH_METAMORPHOSIS_RESTART_20261020.md). The old [R1–R3 lock](KITSUNE_RANK_1_TO_3_EVOLUTION_LOCK_PROPOSAL.md) is **RETIRED** as an evolution specification. The user-supplied one-page PDF (2026-10-20) has SHA-256 `21d35178c528ee675d2ee818795aa7f7d21cfb637f4d34714e1106bcd65cac4c`.
- Production governance: `docs/00_INDEX.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/workflows/ART_PRODUCTION.md`, `docs/workflows/ISOLATED_ART_GENERATION.md`, `skills/producing-tnr-art/SKILL.md` and current `25x_DATA_art_spec.json`. **AI_AVATAR** is the closest current asset target: square, lossless WebP, minimum width 320px, byte ceiling 460800 and a transparent cutout. These are production export constraints, **not** what the raw concept-art input has already passed.

## Species reference gate: APPROVED FOR VISUAL CONDITIONING (not a production export)

**Director-supplied conversation image:** `1000018892.png` (attachment from this workdesk initialization).

| Check | Verified evidence |
| --- | --- |
| SHA-256 (original bytes) | `8b32ed6bb9ba4ea919fb18812fbdece4a845c49ec6a3c85a45610ec022c59dc9` |
| Actual decoder/bytes | **JPEG**, 1536 × 1536, RGB, 236666 bytes; `.png` filename is misleading |
| Alpha/transparency | **Absent**; solid black background (corner pixel 0,0,0) |
| Visual concept | Youthful, expressive fox, visibly two attached bushy tails, fox body and ears; orange/cream coat, not neutral-grey |
| Director approval | **APPROVED 2026-10-20 FOR SPECIES SHAPE/STYLE REFERENCE** — the director answered “Approved” to the species-reference gate. This does not assert transparency or mechanical compliance |
| Raw/QC status | Identity inspected; **not** a compliant transparent cutout and not production-preflight accepted |
| Durable image bytes | **CONVERSATION SOURCE ONLY**, with byte-identical source copied into the director-downloadable intake ZIP `TNR_Living_Lineages_Kitsune_Reference_Intake_20261020.zip` (SHA-256 `4432ccd3172b41e09f1f89a2bb83a7b31a471d8b107456eacdd6921aea9a51ff`); **not pinned in Git**. Actual image bytes must still be attached to the isolated R1 session |
| Risk | Black ground may contaminate reference-conditioned generations; orange coat may bias non-Ember variants. Treat the base's colours as **non-binding** |

**Decision (2026-10-20): APPROVED as the visual species master** despite its JPEG/opaque-black source. The black background remains a conditioning risk; never claim a filename rename creates alpha. Every new Rank 1 must independently satisfy the transparent-cutout visual brief, with mechanical production QC tracked separately.

## Four demonstration identity locks (source-verified indices)

| Lineage | Palette | Marking / characteristic | Aura | Identity emphasis |
| --- | --- | --- | --- | --- |
| **A · Ember** | **Ember (0)** — warm russet, charcoal and amber | **Pale tips (10)** — light-coloured tips on ears or limbs | **Wind (0)** — a few subtle pale wind wisps close to body | Intentional charcoal placement + restrained light tips; do not turn Wind into fire |
| **B · Moonlit** | **Moonlit (1)** — silver, slate and pale blue | **Crescent marking (1)** — small crescent forehead marking | **Moon (5)** — faint cool moonlit glow at silhouette | Forehead crescent readable at 160px |
| **C · Jade** | **Jade (10)** — jade green, dark teal and cream | **Mismatched eyes (5)** — two distinct harmonious eye colours | **Lightning (4)** — a few short gentle violet sparks | Eye mismatch present without exaggerated eye anatomy |
| **D · Obsidian** | **Obsidian (9)** — black, dark violet and silver | **Dappled accents (9)** — small contrasting spots | **Spirit (7)** — a few faint pearl-coloured spirit motes | Readable dark fur planes and preserved dapples |

These are **mock identity test vectors**, not rolled player records. No variant may borrow another's actual image.

## Unified Kitsune Rank 1–9 morphology roadmap — DIRECTOR-APPROVED FOR VISUAL PILOT

**Common form design lock (2026-10-20 visual pilot):** one fox head, connected quadrupedal torso, four functional fox legs and paws, one muzzle, two ears, every tail individually attached at the rump. No humanoid hands, extra limb types, wings, feathers, disconnected tails, costume armour, jewelry, horns, scenes or emblems. Palette/characteristic/aura are individual traits, not fixed by the species base. Every rank shares the exact same morphology concept across all four lineages. The director **approved the nine-stage morphology and 2/2/3/3/4/5/6/7/8 tail-count progression** for this demonstration on 2026-10-20. Further changes require an explicit new decision; the roadmap is not a production generator contract.

| Rank / game label | Phase / anatomy and signature silhouette | Attached tails | Visual acceptance difference from previous rank |
| --- | --- | ---: | --- |
| **1 · Companion** | **Juvenile pup:** compact short-legged fox, large but natural ears, rounder short muzzle, small cheek ruff, slim chest, playful poised stance. No mature mane, dorsal crest, mantle or ornaments. | **2** modest, separate plumes | Distinct from species neutral reference through a genuinely newly drawn pose, facial micro-identity and the individual cosmetic set; *not* an evolved form |
| **2 · Scout** | **Yearling:** longer lower legs and more lifted sternum, slightly leaner muzzle, longer springy spine and raised ear carriage; still youthful with no mantle. | **2** lengthened but modest | Body becomes leggier and less pup-like at equal camera scale; no mere enlargement |
| **3 · Tracker** | **Adolescent runner:** significantly longer torso, strong swept hindquarters and larger functional rear paws, alert low hunting stride; face notably less round; tail-base fur broadens. | **3** distinct rump-rooted plumes | Low elongated runner profile + organic emergence of third tail visibly distinguishes R2 |
| **4 · Guardian** | **Young adult fox:** taller forequarters, balanced athletic four-leg stance, adult muzzle, first deliberate but shallow natural chest/cheek ruff; no heroic mane or crown. | **3** separated, fuller plumes | Upright adult proportions vs R3's low adolescent running shape; final ordinary growth |
| **5 · Hunter** | **FIRST MAJOR METAMORPHOSIS — battle fox:** rebuild torso into a longer high-shouldered hunter with arched spine, noticeably lengthened neck, swept angular head-to-shoulder fur crest and projecting paired side-fur mantle; longer defined limbs with widened paws. Distinct creature architecture, not normal adult with decorative lines. | **4** flared rear-quarter plumes | The crown-to-back and shoulder outline acquires a fundamentally **new tier**; compare R4/R5 black silhouettes at 160px |
| **6 · Warden** | **Battle-form development:** substantially deeper chest, functional broad forepaws, natural protective double-layer shoulder/neck fur, continuous integrated crest from R5; weight-bearing fox anatomy remains visible. | **5** fuller layered plumes | Clear forequarter mass/paired fur shielding; not an R5 colour, glow or pose update |
| **7 · Sentinel** | **SECOND MAJOR METAMORPHOSIS — high guardian:** restructure into an imposing, tall-chested four-legged guardian with markedly broader neck-root, wider angular shoulder-mantle wings **made only of fur**, pillar-like native forelegs and a high-sweeping tiered rear tail display. Long head/neck remain vulpine. | **6** separately rooted tails in high paired arcs | A distinct **towering front / arcing rear** geometry, not merely R6 made larger |
| **8 · Mythic** | **Guardian-form development:** sustained sentinel shoulder volume; taller multi-layer **fur** ridges along neck and upper spine, finer elongated face, sculpted haunch muscles, a second inner contour within the rear fan. | **7** attached plumes in layered fan | Developed dorsal crest and dual-depth tail fan while R7 identity anchors remain |
| **9 · Sovereign** | **THIRD MAJOR METAMORPHOSIS — sovereign fox:** rebuild upper body into a regal apex prow: dramatically raised integrated tripartite head/neck **fur** crown, deep projecting multi-tier chest mantle, formidable weight-bearing paws and broad anchored hindquarters, paired with a vast **two-tier** tail fan behind. No external armour or supernatural appendages. | **8** individually attached tails with two large contour levels | Entire head-to-chest-to-fan outer outline changes into a new form; never accept R8 + longer fur/glow alone |

**Rank 10 · Celestial** is deliberately **OUT OF SCOPE** for images. A proposed nine-tail culmination exists in the juvenile restart document; **nothing here approves it**. R9's eight-tail choice intentionally leaves headroom. A later nine-tail-at-R9 change would require a new director decision and a deliberate coordinated roadmap revision, not an improvisation in a generation session.

### Progression acceptance locks

- **Growth R1–R4:** head-to-body ratio, muzzle shape, torso, shoulder/haunch geometry and leg length advance meaningfully. Tail addition alone is insufficient.
- **Metamorphosis R5/R7/R9:** must **replace** significant portions of the contour and internal architecture, like a distinct monster-evolution stage, while preserving the fox body plan. Distinctness judged at full resolution and 160px against **the immediate accepted parent** and earlier major milestone silhouettes.
- **Development R6/R8:** recognizable continuation of the preceding major form with conspicuous anatomical development; no backwards regression.
- **Individual continuity:** preserve the same face/muzzle identity and exact saved palette placement, characteristic and aura accent in each lineage. No copied appearances from other players, no base image on later ranks.
- **Camera/art:** elevated three-quarter fox, consistent camera and reasonable margins, complete paws and separate tails. Crisp premium TNR pixel clusters/cel shading, not painterly blur; alpha cutout, no background, black void, floor or cast/contact shadow.
- **Source of rank art:** R1 receives **one actual species master**; R2–R9 receive **only the immediately prior approved image of the same individual**. Parent image SHA-256 is recorded before opening the isolated session. A generation is **not approved** merely because a candidate exists.
- **Direction checks:** do not approve R5/R7/R9 until a true **structural** change survives a 160px side-by-side check. Subtle aura or more ornament is not a substitute for form change.

## Mature-form comparator intake — director supplied 2026-10-20

The director provided **five previously generated mature Kitsune illustrations** and described them as potentially useful **around Rank 5–6**. These are **visual vocabulary and QA comparators**, *not* retroactively accepted Rank 5/6 assets. They are **not parent images** in any of the 36 individual lineage slots and **must not replace** the one-image inheritance chain.

| Intake (misleading `.png` name; actual JPEG) | Recognizable visual family | Source SHA-256 |
| --- | --- | --- |
| `1000018893.png` | Jade/teal with mismatched eyes and violet sparks | `2126971390351dfee90f24fd8cedbf8f0a2733bd6116041189fced60b923f602` |
| `1000018894.png` | Obsidian/violet with dapples and pearl spirit motes | `f8790f02c227e74676cfec63ff6187cb9a71e226b1fc77fe558cd8f2a193c5e9` |
| `1000018895.png` | Moonlit silver/pale blue with forehead crescent | `1c6fcd98a1e85734df66f34496bf4ee2bdfa47c180eff13342cf8115def55db7` |
| `1000018896.png` | Dark warm Ember palette, russet/charcoal and light wind wisps | `8cf0e8b82978589a0b8e6057e8042eec8f766198968dbb6ddbb0bf828f0cda9f` |
| `1000018897.png` | Additional pale gold/cream mature comparator; exact cosmetic assignment unverified | `275c6f1ba2f65e7003021c7b8de09bded3d145eb9aa4eb8e98c07d52a8f2ebd6` |

**Actual bytes:** all five are 1536×1536 **JPEG/RGB**, opaque black background despite `.png` filenames. Their originals were preserved byte-for-byte in the companion intake ZIP with corrected `.jpg` names and a manifest; archive SHA-256 `4432ccd3172b41e09f1f89a2bb83a7b31a471d8b107456eacdd6921aea9a51ff`. The ZIP is a **conversation artifact**, not a Git-pinned binary. Do not treat those images as preflight-passed transparent sprites.

**What to learn:** These strong mature-form examples supply a useful **R5→R6 visual maturity envelope**—a clear adult muzzle, established layered cheek/chest fur, dramatic but connected fox tails and immediately legible individual palettes/markings. The five images also share almost the same mature anatomy and orientation. The new system must NOT copy that anatomy unchanged across its late ranks. **R5** should establish the new battle-fox structure without reaching the full giant mantle; **R6** can achieve the richer mature layering. **R7 and R9 must then exceed these comparators through true new body architecture**, not simply more surface detail or glow. Precise tail count still comes from the approved **rank table**, not from overlapping tails in these comparator images.

**One-image conditioning remains inviolable:** At R5 and R6, generator input is still only that lineage's immediate accepted previous-rank image. The old mature pictures inform **workdesk art direction and post-generation comparison**, not an extra image input. If a prompt concept changes after visual comparison, revise it centrally and obtain director approval before resuming that rank.

## Rank 1 approval intake — Ember (A_R01), 2026-10-20

**Director decision:** “Approved, next,” supplied with the image of the new juvenile Ember Companion. This is **the first of four unique Rank 1 lineage images**, not a Rank 2 evolution. **Next: Moonlit Rank 1**, again from the ORIGINAL species master.

| Intake field | Value / evidence |
| --- | --- |
| Current asset | `A_R01` — Ember · Rank 1 Companion |
| Parent identity expected | `SPECIES_REF`, source SHA-256 `8b32ed6bb9ba4ea919fb18812fbdece4a845c49ec6a3c85a45610ec022c59dc9` |
| Actual generator reference-use proof | **NOT independently verifiable** from this returned image; the isolated-session prompt required the species master, but the tool invocation/actual image attachment was not supplied in the intake |
| Original upload | `1000018898.png` — **actually JPEG/RGB**, 1536×1536, **opaque black background**, 318746 bytes |
| Approved raw original SHA-256 | `b49354012e173291b415383cf4aca91942d921297041e232d9ef3dd057058470` |
| Byte-identical corrected extension | `kitsune_ember_rank1_approved_source_20261020.jpg` (conversation artifact; **not Git-pinned**) |
| Dedicated 2-image source/parent archive | `TNR_Living_Lineages_Ember_Rank1_Approved_Source_Intake_20261020.zip`, SHA-256 `9c7483429eab15859c5ccc9b032f0d6c5b4cc6c59a8dc7e0b3896de434ba4640`, 557250 bytes; source bytes verified against manifest |
| Visual verdict | **DIRECTOR APPROVED**. At full size and a 160px side-by-side, clearly new playful juvenile fox pose with two separate tails; warm russet/charcoal/amber palette, pale tips and restrained pale Wind wisps remain visible |
| Mechanical QC | **NOT PRODUCTION READY**: raw is opaque RGB/JPEG with black background. No transparent cutout, lossless WebP export, canonical preflight, or upload check |
| Parent for A Rank 2 | This exact approved Ember image SHA-256 `b493...8470`, not the species base. Rank 2 stays blocked until Moonlit/Jade/Obsidian Rank 1 are also approved. |

**Anatomy note:** The approved Ember has a fuller juvenile chest ruff and slightly fuller tail arcs than the original species master but remains youthful; the rank-1 visual gate was settled by the director. The same approved Rank 1 concept applies to each other variant—do not copy Ember's colours, markings, pose, or raw image as their conditioning input.

**Next generation lock:** `B_R01` **Moonlit Companion**. Attach only `SPECIES_REF` (exact approved source SHA above), with **Moonlit (1)** silver/slate/pale blue coat; **Crescent marking (1)** small forehead crescent; **Moon aura (5)** faint cool halo at silhouette. Retain juvenile two-tail fox structure and premium pixel clusters; compose a **new individual**, not a recolour of Ember or the base. The next new approved image will become `B_R01`'s unique Rank 2 parent. Director review required before advancing to Jade.

## Rank 1 approval intake — Moonlit (B_R01), 2026-10-20

**Director decision:** “Approved, next,” accompanying the distinct Moonlit juvenile. This accepts Moonlit's original illustration as **raw visual art only**; it does not prove upload-readiness or the internal generation tool's actual reference use.

| Intake field | Evidence |
| --- | --- |
| Individual | `B_R01`, Rank 1 Companion; source file `1000018899.png` (decoder says JPEG RGB, 1536×1536, opaque black, 345097 bytes) |
| Approved original source SHA-256 | `f42524d1be91e8e92dee9ae4bd2140374907431c2ee431621f36cf84dc5619b1` |
| Corrected filename | `kitsune_moonlit_rank1_approved_source_20261020.jpg` — identical original bytes, conversation artifact, not Git-pinned |
| Expected sole parent | Species reference `SPECIES_REF`, SHA-256 `8b32ed6bb9ba4ea919fb18812fbdece4a845c49ec6a3c85a45610ec022c59dc9`. Generator's actual use of attached pixels **unverified** |
| Visual verdict | **Director-approved**: youthful two-tail fox, silver/slate/pale-blue coat, readable small forehead crescent and restrained cool moon aura; clearly not the Ember individual |
| Small-size test | **PASS** at 160px; exact-file resample/QC artifact recorded in the machine tracker |
| Intake ZIP | `TNR_Living_Lineages_Moonlit_Rank1_Approved_Source_Intake_20261020.zip`, SHA-256 `0d30357be3536db51a796566db8c872ef0f7ce12d1718bb4569c08c8a1c1c6f0` (conversation artifact, **not Git-pinned**) |
| Mechanical gate | **NOT RUN** — source retains opaque background; no transparent cutout, final WebP or artpreflight |

**Next generation:** `C_R01`, **Jade Rank 1**, conditioned on the **exact shared juvenile master**, *not* Moonlit or Ember. Locked traits: Jade (10), Mismatched eyes (5), Lightning (4). Exact approved Jade source will become `C_R02`'s only conditioning reference after the Rank 1 family is complete.

## Director-revised final sheet: 19 distinct images / 26 placements (2026-10-20)

The director supplied a 1536×1024 reference composition and explicitly changed the demonstration deliverable. **Do not produce an unnecessary nine-rank chain for Moonlit, Jade or Obsidian.** The full ranked chain now belongs to **Ember only**. The other three lineages appear only at Ranks 1–3 to demonstrate individuality and early inheritable growth.

**Two-panel placement plan:**

- **Upper overview:** 10 columns in order — **Species reference** (not a rank), then **Ember Rank 1 Companion → Rank 2 Scout → Rank 3 Tracker → Rank 4 Guardian → Rank 5 Hunter → Rank 6 Warden → Rank 7 Sentinel → Rank 8 Mythic → Rank 9 Sovereign**. The supplied layout incorrectly repeated **Rank 4** in the sixth position; this SVG corrects it to **Rank 5**. Use exact TNR game rank names rather than the example's unofficial names.
- **Lower comparison matrix:** columns **Shared Species Reference | Rank 1 Companion | Rank 2 Scout | Rank 3 Tracker**, with rows **Ember / Moonlit / Jade / Obsidian** and their exact persisted palette, marking and aura names. Each "Species Reference" image is **the same original master**, not a palette-specific imitation.
- **Count:** **1** species image + **9** Ember Rank 1–9 images + **3×3 = 9** other individual Rank 1–3 images = **19 unique approved images**. The SVG contains **26 placements** because the species master is reused four additional times and Ember R1–3 are repeated once in the bottom comparison. **No duplication in generation.**
- **Source-safe showcaser:** assemble from actual individually approved files using deterministic image placement, alpha/cutout processing if required, and source hashes; no image generation of the composite and no retouching inside the presentation. Raw JPEG with opaque black backgrounds must never be misreported as transparent production-ready artwork.
- **No format invention:** SVG [structural template](LIVING_LINEAGES_KITSUNE_SHEET_STRUCTURAL_20261020.svg) has editable labeled art placeholders and 1536×1024 geometry; [slot map](LIVING_LINEAGES_KITSUNE_SHEET_SLOT_MAP_20261020.json) binds all slots to their 19 canonical asset IDs. The image reference itself is a **layout example**, not source art.
- **Approval gates:** Current structural sheet is a **DRAFT**, pending the director's visual approval of layout, spacing and text. Its creation does NOT approve missing pet illustrations or their future processed art.

**Working sequence:** Finish Jade/Obsidian R1 first. Produce R2 for all four from their own **accepted R1**, then R3 for all four from their own **accepted R2**. After four R3 approvals, proceed with **Ember R4→R5→R6→R7→R8→R9** only, preserving one immediate, approved Ember parent image at each rank. Old mature reference images are **style comparators only** at Ember R5/R6. Shared rank concepts remain the director-approved species roadmap, even though only Ember exercises ranks 4–9 in this particular sheet.

**Ledger integrity:** Keep the initial **37 IDs** for traceability, but mark the **18 non-Ember R4–R9** IDs `OUT_OF_SCOPE_FOR_APPROVED_SHEET`—they are not rejections, missing deliverables, or a reason to generate more images. The **active 19** source assets and **26 placements** control completion.

## Revised production order and acceptance rules

1. **COMPLETE:** The director accepted the juvenile visual source and the common nine-rank Kitsune form milestones/tail curve `2,2,3,3,4,5,6,7,8`.
2. **Rank 1 family (4/4 required):** Ember **APPROVED**; Moonlit **APPROVED**; Jade **NEXT**; Obsidian **PENDING**. Each is generated with **exactly one source image: the species master**.
3. **Rank 2 family (4/4 required):** Each individual uses only its own director-approved Rank 1; inspect at full and 160px for genuine youth-to-yearling growth.
4. **Rank 3 family (4/4 required):** Each individual uses only its own director-approved Rank 2; third attached tail and adolescent runner anatomy must be visible.
5. **Ember Rank 4–9 only:** Sequential new images using the immediately preceding accepted Ember source, with **major metamorphoses at R5/R7/R9**. Each distinct parent-child link must have its own source hashes and approvals. The other three lineages are finished at Rank 3 for this sheet.
6. **Deterministic final comparison:** Fill the approved structural SVG using actual accepted assets and verify 26 slot-to-source bindings, with **19 unique SHA-backed source assets** and no regenerated compositions. Director approves the resulting populated sheet separately.

**Every stage retains separate gates:** original source bytes and parent identity, visual director acceptance, 160px QC, transparency and mechanical export processing, gallery exact-source placement, and final showcase acceptance. A render that looks convincing is not evidence of the live pet generator's behavior.

## Known implementation conflicts (not solved by visual approval)

The pinned game's `app/src/libs/pets/appearance.ts` explicitly forces **natural adult proportions** over words such as “young” or “small”, and its current `RANK_APPEARANCES` is geared to adult/heavy development. It also requests uniform gray `#f0f0f0` staging and restricts exterior aura effects, whereas this proof-of-concept requires a **transparent final cutout** and tests the existing Wind/Moon/Lightning/Spirit cosmetic catalogue descriptions. Current saved-rank redraw and per-pet reference usage should not be conflated with an implemented editable species-rank concept feature. **Do not assert the live game can create this juvenile chain unchanged.** Fable owns any later prompt/editor/schema/tooling implementation, on an independently reviewed branch, after director design acceptance.

## Immediate workdesk checkpoint (2026-10-20)

- Structural SVG: **DRAFT CREATED** at `LIVING_LINEAGES_KITSUNE_SHEET_STRUCTURAL_20261020.svg`, awaiting director layout approval; overview shows **Species Reference → Rank 1 → ... → Rank 9**, with **Rank 5 Hunter correctly present**.
- Target: **19 unique images**, not the original 37. **26 placements**; retained ledger keeps 18 out-of-scope history slots.
- Director-approved raw visuals: **3/19** — species master + **Ember Rank 1** + **Moonlit Rank 1**. No final transparent production exports or gallery QC claimed.
- Next isolated generation: **C · Jade / Rank 1 Companion** from the exact juvenile master, then Obsidian Rank 1; all four R2 and R3 before Ember R4–R9.
- Exact parent image intended on each individual R1 was the species master; actual tool-side conditioning ingestion remains independently **UNVERIFIED**. No live-game calls, player pet attempts, credentials or publication.

## Structural SVG verification (2026-10-20)

- **Director acceptance:** PENDING. This is an editable **structural-only** poster and contains **zero artwork pixels**; no unapproved or prior example creatures are embedded.
- **Exact committed SVG:** `LIVING_LINEAGES_KITSUNE_SHEET_STRUCTURAL_20261020.svg`; Git blob SHA-1 `c1e44dd0459a667d6b40c55c0153accd8054cced`. Downloadable conversation SVG checked **byte-for-byte identical** against that repository blob (via `git hash-object`).
- **Visual/mechanical structural QC:** XML parsed successfully; CairoSVG generated an inspected **1536×1024** PNG; 26 unique placement IDs map to exactly 19 asset IDs; `SPECIES_REF` has five identical-source placement requirements; A Rank 1–3 repeat once below; all nine top rank labels and game names are source-verified and **A_R05 Hunter appears between A_R04 Guardian and A_R06 Warden**. Long cosmetic labels and metamorphosis captions were adjusted for 1536px legibility.
- **Distribution:** `TNR_Living_Lineages_Kitsune_Structural_Sheet_Package_20261020.zip`, SHA-256 `6166e76cbed4b57fb4eac5b178b6392897dc19cea20612c7e9745f356d8ae74a`, contains source SVG, PNG preview, mapping JSON and notes. ZIP is conversation deliverable; committed canonical geometry is SVG + JSON slot map on the workdesk branch.
- **Rulings:** Visual foundation `RUL-2026-10-20-002`, updated scope `RUL-2026-10-20-003`. Current live `main@02a288e966db27f427508734a6223e0e583b081a` independently added `RUL-2026-10-20-001` for schema adoption, so we renumbered this branch's art rulings to avoid duplicate IDs. Branch is **not merged**; main was 12 commits ahead of the workdesk merge-base when checked. **Re-verify/reconcile main and RULINGS before a PR/merge**; do not overwrite new main decisions with the branch's older RULINGS file.
- **Safety:** Git-only design records, no live-game requests/writes, credentials, player image-generation attempts, or art production preflight.
