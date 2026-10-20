# Living Lineages — Kitsune four-lineage demonstration

**Status:** MASTER WORKDESK OPEN; all visual milestones below are **PROPOSED, NOT DIRECTOR-LOCKED**. No new rank images generated or approved by this workdesk.  
**Lead:** Art Director; support: Image Production.  
**Ownership:** This register + [37-slot machine-readable ledger](LIVING_LINEAGES_KITSUNE_SLOTS_20261020.json) belong to the ChatGPT-owned workdesk branch; do not alter the separate pet-proposal branch or active Fable branches. The JSON ledger owns per-image status, bytes and parentage; this file owns creative direction and process.  
**Scope:** Concept-art proof, not deployed generation behavior, live records, balance or publishing. **Live-game requests/writes: 0. Credentials: none.**

## Evidence and pinned authority

- Shared repository baseline verified on 2026-10-20: `main@e13bc9fa085b37bd84ab7736256da8d1ad2a4a99`.
- Pet research and juvenile restart source: `chatgpt/premium-pet-visual-prompt-proposal-20261020@f8059013dc44f26e4e0bd6f09bfec4b7fb6dc601`, merge-base `e13bc9fa085b37bd84ab7736256da8d1ad2a4a99`.
- Public **pinned source**, **not** a live species capture: `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11`: `app/drizzle/migrations/0090_pet_companions.sql` seeds `pet-species-65` as LEGENDARY Kitsune, a mythical fox spirit with multiple distinct attached bushy tails; `app/drizzle/constants.ts` gives exactly ten named pet ranks; `app/src/libs/pets/catalogue.ts` supplies the saved cosmetic indices/wording; `app/src/libs/pets/appearance.ts` describes current renderer behavior.
- Proposal hierarchy: [one-page reference evolution](PET_ART_REFERENCE_EVOLUTION_ONE_PAGE.md) and [juvenile reset](KITSUNE_JUVENILE_GROWTH_METAMORPHOSIS_RESTART_20261020.md). The old [R1–R3 lock](KITSUNE_RANK_1_TO_3_EVOLUTION_LOCK_PROPOSAL.md) is **RETIRED** as an evolution specification. The user-supplied one-page PDF (2026-10-20) has SHA-256 `21d35178c528ee675d2ee818795aa7f7d21cfb637f4d34714e1106bcd65cac4c`.
- Production governance: `docs/00_INDEX.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/workflows/ART_PRODUCTION.md`, `docs/workflows/ISOLATED_ART_GENERATION.md`, `skills/producing-tnr-art/SKILL.md` and current `25x_DATA_art_spec.json`. **AI_AVATAR** is the closest current asset target: square, lossless WebP, minimum width 320px, byte ceiling 460800 and a transparent cutout. These are production export constraints, **not** what the raw concept-art input has already passed.

## Species reference gate: received, not yet locked

**Director-supplied conversation image:** `1000018892.png` (attachment from this workdesk initialization).

| Check | Verified evidence |
| --- | --- |
| SHA-256 (original bytes) | `8b32ed6bb9ba4ea919fb18812fbdece4a845c49ec6a3c85a45610ec022c59dc9` |
| Actual decoder/bytes | **JPEG**, 1536 × 1536, RGB, 236666 bytes; `.png` filename is misleading |
| Alpha/transparency | **Absent**; solid black background (corner pixel 0,0,0) |
| Visual concept | Youthful, expressive fox, visibly two attached bushy tails, fox body and ears; orange/cream coat, not neutral-grey |
| Director approval | **PENDING EXPLICIT LOCK OF THESE EXACT BYTES**; supplied/reference-intended does not by itself prove signoff |
| Raw/QC status | Identity inspected; **not** a compliant transparent cutout and not production-preflight accepted |
| Durable image bytes | **CONVERSATION SOURCE ONLY**; no Git binary pin; source hash alone cannot supply a reference to a later generation |
| Risk | Black ground may contaminate reference-conditioned generations; orange coat may bias non-Ember variants. Treat the base's colours as **non-binding** |

**Acceptance question:** may this exact JPEG be locked as a **shape/style-only conditioning reference** despite its opaque black background, or will the director supply/approve a transparent corrected juvenile original? Never pretend a filename rename creates alpha. In either case, new Rank 1 assets must actually meet the transparent-cutout visual brief; production-ready status requires separate QC.

## Four demonstration identity locks (source-verified indices)

| Lineage | Palette | Marking / characteristic | Aura | Identity emphasis |
| --- | --- | --- | --- | --- |
| **A · Ember** | **Ember (0)** — warm russet, charcoal and amber | **Pale tips (10)** — light-coloured tips on ears or limbs | **Wind (0)** — a few subtle pale wind wisps close to body | Intentional charcoal placement + restrained light tips; do not turn Wind into fire |
| **B · Moonlit** | **Moonlit (1)** — silver, slate and pale blue | **Crescent marking (1)** — small crescent forehead marking | **Moon (5)** — faint cool moonlit glow at silhouette | Forehead crescent readable at 160px |
| **C · Jade** | **Jade (10)** — jade green, dark teal and cream | **Mismatched eyes (5)** — two distinct harmonious eye colours | **Lightning (4)** — a few short gentle violet sparks | Eye mismatch present without exaggerated eye anatomy |
| **D · Obsidian** | **Obsidian (9)** — black, dark violet and silver | **Dappled accents (9)** — small contrasting spots | **Spirit (7)** — a few faint pearl-coloured spirit motes | Readable dark fur planes and preserved dapples |

These are **mock identity test vectors**, not rolled player records. No variant may borrow another's actual image.

## Unified Kitsune Rank 1–9 morphology roadmap — PROPOSED, director approval required

**Common form law (proposed):** one fox head, connected quadrupedal torso, four functional fox legs and paws, one muzzle, two ears, every tail individually attached at the rump. No humanoid hands, extra limb types, wings, feathers, disconnected tails, costume armour, jewelry, horns, scenes or emblems. Palette/characteristic/aura are individual traits, not fixed by the species base. Every rank shares the exact same morphology concept across all four lineages. Tail counts and every shape milestone below require director lock **before** they become generation rules.

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

**Rank 10 · Celestial** is deliberately **OUT OF SCOPE** for images. A proposed nine-tail culmination exists in the juvenile restart document; **nothing here approves it**. R9's eight-tail choice intentionally leaves headroom. A director who prefers nine tails at R9 can change the proposal before production, but the scheme must be decided together, not improvised by separate generators.

### Progression acceptance locks

- **Growth R1–R4:** head-to-body ratio, muzzle shape, torso, shoulder/haunch geometry and leg length advance meaningfully. Tail addition alone is insufficient.
- **Metamorphosis R5/R7/R9:** must **replace** significant portions of the contour and internal architecture, like a distinct monster-evolution stage, while preserving the fox body plan. Distinctness judged at full resolution and 160px against **the immediate accepted parent** and earlier major milestone silhouettes.
- **Development R6/R8:** recognizable continuation of the preceding major form with conspicuous anatomical development; no backwards regression.
- **Individual continuity:** preserve the same face/muzzle identity and exact saved palette placement, characteristic and aura accent in each lineage. No copied appearances from other players, no base image on later ranks.
- **Camera/art:** elevated three-quarter fox, consistent camera and reasonable margins, complete paws and separate tails. Crisp premium TNR pixel clusters/cel shading, not painterly blur; alpha cutout, no background, black void, floor or cast/contact shadow.
- **Source of rank art:** R1 receives **one actual species master**; R2–R9 receive **only the immediately prior approved image of the same individual**. Parent image SHA-256 is recorded before opening the isolated session. A generation is **not approved** merely because a candidate exists.
- **Direction checks:** do not approve R5/R7/R9 until a true **structural** change survives a 160px side-by-side check. Subtle aura or more ornament is not a substitute for form change.

## Ordered production and 37-slot acceptance ledger

**One species reference + four Rank 1 pets + eight more ranks × four pets = 37 images.** All 37 slots already exist in [the JSON ledger](LIVING_LINEAGES_KITSUNE_SLOTS_20261020.json). No generated lineage images are accepted at initialization. Source receipt is not signoff.

1. Director explicitly locks the species-reference exact bytes/transparent handling and this proposed **nine-rank morphology/tail roadmap**.
2. Produce **A Rank 1** in its own isolated session from the species master and A's exact traits. Inspect full-size and 160px; director accepts. Repeat **B/C/D Rank 1**, always using the same species master, never A.
3. Continue strictly **one rank across all four pets at a time**: A Rank 2 from A Rank 1, then B/C/D Rank 2 from their own accepted R1; repeat until Rank 9. Stop if any sibling is unapproved. A single shared concept per rank; changes are proposed/approved centrally, not silently customized.
4. Every approved generation records actual source bytes/MIME/size/alpha/SHA-256, exactly one accepted parent SHA-256, isolated session reference, director approval, 160px identity/progression judgments and separate art processing/preflight results. Missing bytes, hash mismatch or wrong parent **BLOCK** the next evolution.
5. Deterministically assemble four sections from **the exact approved files**, never a generated imitation: (A) reference and R1, (B) growth R1–4, (C) metamorphosis R5–9, (D) full 4-column × 9-rank grid; include ancestry diagrams, cosmetic values, and meaningful R4→5/R6→7/R8→9 comparisons.

**Order clarification:** The earlier juvenile restart suggested piloting Ember all the way through R5 before the other colours; the current **director-supplied master-workdesk sequence expressly says all four pets per rank**. Follow this newer task-level instruction for the demonstration. Do not blend the two routes.

## Known implementation conflicts (not solved by visual approval)

The pinned game's `app/src/libs/pets/appearance.ts` explicitly forces **natural adult proportions** over words such as “young” or “small”, and its current `RANK_APPEARANCES` is geared to adult/heavy development. It also requests uniform gray `#f0f0f0` staging and restricts exterior aura effects, whereas this proof-of-concept requires a **transparent final cutout** and tests the existing Wind/Moon/Lightning/Spirit cosmetic catalogue descriptions. Current saved-rank redraw and per-pet reference usage should not be conflated with an implemented editable species-rank concept feature. **Do not assert the live game can create this juvenile chain unchanged.** Fable owns any later prompt/editor/schema/tooling implementation, on an independently reviewed branch, after director design acceptance.

## Immediate workdesk checkpoint (2026-10-20)

- Reference: received and byte-identified; explicit visual lock + transparent/reference handling **PENDING**.
- Morphology/tail curve: nine rank concepts **PROPOSED / awaiting director approval**.
- Rank images: **0/36** approved; full target **0/37** approved (species candidate received, not counted as accepted).
- Pending generation: **A · Ember / Rank 1 Companion**, **BLOCKED** on reference and rank-roadmap director locks. Copy-ready isolated brief may be prepared without rendering.
- No art generation, no live-game requests, no pet attempts, no game changes, no credentials, no production preflight.
