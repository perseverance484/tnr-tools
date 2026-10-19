# Isolated Image Generation — TNR Art Studio Protocol

**Status:** FINAL. Director-approved 2026-10-14 (RUL-2026-10-14-001); jutsu-icon P0 visual-quality and gallery gates approved 2026-10-19 (RUL-2026-10-19-003); tooling contract integrated 2026-10-17 (PR #34). Further substantive protocol changes need a new director ruling; JUTSU_ICON tooling changes go through Lane A review.  
**Owner:** Art Studio coordination and Image Production under director acceptance.  
**Routes from:** docs/00_INDEX.md and docs/workflows/ART_PRODUCTION.md.  
**Scope:** assisted creation of one production art asset at a time, in any collection. Proven on the Blue Blade Eyes (BBE) jutsu-icon collection, completed 2026-10 (register: docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md, kept as the worked example).

This is an **art-session coordination protocol**, not a replacement for skills/producing-tnr-art/SKILL.md, the current 25x_DATA_art_spec.json, docs/DOCTRINE.md, generated game contracts, or the user-controlled live upload path.

## 1. Session separation

| Session | Responsibility | Deliberately excluded |
| --- | --- | --- |
| **Art Studio / workspace** (persistent, can be reopened) | Reconstruct repo state; maintain an approved identity register and source ledger; decide next subject; write individual briefs; compare against the family; intake, verify, process, QC, package and record files | Image generation, silently changing accepted art, live-game requests/writes |
| **Isolated Generation** (new conversation for each asset) | Ingest one small art brief and one or two **individual** approved references; generate **one candidate at a time** for that subject; obtain director visual approval; return the original image | Other assets, icon sheets, broad repository writes, batch generation, processing, publishing |

The studio retains the full family overview; the generation session deliberately does not. One jutsu/asset per generation conversation. Revisions for that same asset may stay in its isolated session while the target remains stable; repeated wrong-subject generation means **close and restart clean**, not longer prompts in a polluted context.

A new Art Studio conversation reconstructs status from live main, the applicable role and workflow documents, and the durable per-workstream register. Do not rely on conversation memory or old SHAs as canon.

## 2. Studio → generator gate

Before opening the fresh generation session, the studio establishes and records:

1. Exact target identity, meaning/action and client field; refer to captured record or user-supplied evidence, not a guessed effect.
2. **One primary silhouette**; one supporting effect; distinctive direction/visual motion; main focal hierarchy, including clear dark/light separation.
3. The full existing-family **exclusion list**: which shapes belong to the other approved icons and must not appear in this target.
4. Approved **material/palette treatment** derived from the applicable workstream register.
5. **At most two approved, individual images** selected for style or specific object identity. State explicitly whether each reference is **style-only**, **material-only**, or **subject reference**. Never use a sheet/contact collage, a rejected-generation image, or an unrelated previous jutsu as implicit composition.
6. The expected small-size display and restrictions: no labels, titles, UI frames, franchise insignia, watermarks or irrelevant character scenes.

### Jutsu-icon TARGET LOCK (P0 A/B)

For each `jutsu.image` generation, the brief must lock these facts **before** rendering:

- **Immutable identity:** exact bloodline ID, jutsu ID and display name; specific source-supported combat technique/action and the source's evidence level (historical captures are not current-live checks).
- **Composition before effects:** one reserved dominant technique silhouette, what it **does**, its **camera/perspective and motion axis**, focal direction/negative space, and one secondary effect. Set the action/geometry first; palette, chakra material and particles dress this composition, never replace it.
- **Family exclusions and references:** each other family member's reserved primary silhouette/action, target-specific wrong-subject exclusions, and the role of each actually attached individual reference (identity-only versus style/material-only or true subject). Keep the rendering lock and approved constraints short and concrete.

A static brief/checklist validator may catch missing identity or camera fields, but it cannot prove that a generated image depicts the right technique.

The studio produces a copy-ready brief. Pass the actual selected image bytes with the prompt: a source filename or URL alone does not prove the generator saw the pixels. If the reference's bytes are not available, say so and do not claim a faithful reference-conditioned result.

## 3. Isolated generation contract

Open a **new project conversation**. Read the current TNR bootstrap and art authority without feeding an entire art library into image generation. Supply only the target brief and the selected one or two image references.

**Generate exactly one square, single-icon candidate**; no sheets or multi-icon panels. Use composition first, then apply rendering treatment:

- **Subject/action**: what the technique does in combat.
- **Silhouette**: the large-scale shape must be identifiable before decoration.
- **Rendering**: apply only the approved bloodline/material palette.
- **Chakra vocabulary**: motion blur, strike trails, binding structures, protective reinforcement, resonance or targeting only when appropriate to that jutsu. No mandatory chakra ring.
- **Exclusions**: forbid the concrete wrong compositions and actors that would erase the intended distinction.

### Jutsu-icon candidate fail-fast gate (P0 A–E)

Inspect **each actually rendered candidate** against the target lock before seeking director judgment:

1. **Target and action:** use the tool's visible result description only as an early wrong-target hint, then inspect the **pixels**. Reject immediately if the candidate is another jutsu, a generic object/effect instead of the locked technique, or has the wrong camera/geometry. The hidden image-generator prompt is not inspectable; do not infer what it was. If the UI already auto-displayed the bad result, mark it rejected without asking the director to diagnose it.
2. **Distinctness:** compare its primary geometry **and technique action** against **all** sibling silhouette reservations, including 125/64/32-pixel previews when obtainable, before promoting it as a viable candidate. Reject a reasonable sibling-technique lookalike; matching color or elemental materials alone is **not** grounds for rejection. This is visual/art-direction judgment, not an automatic color-score rule. Final side-by-side review of actual approved family assets still occurs at studio intake.
3. **Technique-first, anatomy-off by default:** no full actor, face, body, hand, fingers or limb fragments for jutsu icons unless the director approves an exception for **that exact target** and it is genuinely useful to the action. A specifically approved abstract five-digit contact handprint is not general approval to depict anatomical hands. When literal anatomy is expressly authorized, inspect digit count, thumb placement and proportions; discard malformed results and normally return to actor-free presentation.
4. **Chakra, not invented magic:** physical silhouettes such as triangles are allowed when they are the *working attack/protection structure*, not a disembodied glyph. Reject unsupported ornamental frames, spell circles, runes, polished gold corner artifacts or floating geometric symbols. Example: a frontal charged triangular aperture firing a near-camera particle beam is a technique; a floating ornamental triangle is not.

**Approval loop:** show one viable candidate; director accepts, rejects or requests a same-subject revision. After **two** wrong-subject/composition failures, stop and open a **new clean isolated conversation** with exactly the original jutsu image (identity only) and, if available, one truly approved individual family raw (style/material only). Do not reuse rejected images or pile up longer negative prompts. Once accepted, preserve the **original source bytes**, not a screenshot or a regenerated approximation, and return them to the studio with the target name and approval status.

The generator does not mark an image upload-ready, does not run game writes, and does not quietly alter the jutsu's mechanics.

### Copy-ready isolated-session brief

~~~text
Repository: perseverance484/tnr-tools
Workstream: <bloodline / collection>
Target: <single jutsu or asset>
Jutsu target lock (if jutsu.image): bloodline ID <exact>, jutsu ID <exact>, display name <exact>
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION — one asset only
State: exploratory until director approves
Live-game requests/writes: 0
Credentials: none

Initialize from live repository; verify main and read TNR art authorities.
Read the cited collection register for this one target.
Goal/action: <what the technique does>
Dominant silhouette: <one unmistakable shape and its technique action>
Camera/perspective and motion axis: <orientation, focal direction, near/far>
Secondary effect: <one supporting action cue>
Rendering lock: <exact palette/material/texture guidance from the register>
References attached: <one or two individually, each labeled style-only/material-only/subject>
Composition: <orientation, negative space, focal hierarchy>
Distinctiveness exclusions: <all reserved sibling primary silhouettes/actions + wrong-subject forms>
Other negatives: no unrelated actors, no text, no UI, no franchise imagery.

Generate exactly ONE square icon candidate for review.
Do not generate other techniques or a collage.
Do not process or upload the image.
Return the original asset after director visual approval.
~~~

## 4. Studio intake and visual gates

On receiving the approved candidate:

1. Resolve the **actual source file bytes**, inspect MIME/decoder, dimensions, alpha and hash; do not trust filename extension (a .png name can carry JPEG bytes). Record origin, SHA-256, format, and whether the source bytes are truly pinned in Git.
2. Review the candidate *beside the other approved family icons* at **125, 64 and 32 pixels**. The normal TNR icon delivery field is 125px; 64/32px are additional stress tests, not assumptions about the client.
3. Evaluate silhouette recognition and pairwise confusion **before** granting the set-readability gate. Background noise, chakra decoration and fine crystal ornament must not drown the dominant subject.
4. Preserve the visually approved raw original. Changes requiring regeneration return to a dedicated generation session; mechanical corrections use a new versioned export filename.
5. Update the collection register: approval and raw acceptance are distinct from production QC, @img binding, and live publishing.

Do not promote 'visually approved' or 'file < byte cap' to 'upload-ready'. Record each check separately.

## 4a. Jutsu-icon family gallery — deterministic-only (P0 F)

An `icon sheet`, `family showcase` or `closeout collage` is a **non-generative** QC/presentation work mode, not another image-generation job:

1. Require the full current **N/N director-approved raws** and the accessible exact corresponding **processed WebP bytes**. Preserve their hashes. If an input is missing, label any partial sheet **DRAFT**; it is not final acceptance evidence.
2. Compose only those files through a deterministic, count-adaptive, balanced equal-tile layout (for N=5, **3+2 centered**). Scale presentation copies uniformly using a recorded filter; do not invent, repaint, recolor, retouch, crop or regenerate artwork. The game-ready exported WebPs themselves remain unmodified.
3. Include exact display names and **actual export bytes/1000 (decimal kB)**, not guessed sizes; record gallery and member SHA-256s, tile layout/positions and resampling parameters. Verify that each displayed tile is pixel-equal to the corresponding recorded resampling of the **actual exported** pixels, and inspect 125/64/32 thumbnail QC for the whole family.
4. A gallery made using a generative image tool is **INVALID** even if visually attractive, because it cannot prove preservation of approved icon pixels. Rebuild it by exact-source compositing; never treat a generated imitation as the family sheet.
5. **Final gallery director acceptance is separate** from N/N raw visual approvals, local export QC and canonical `artpreflight.py --type JUTSU_ICON` acceptance. New/changed source bytes invalidate the prior gallery and require rebuilt evidence and fresh gallery signoff. A closed art studio may truthfully record gallery acceptance **PENDING**.

No gallery step authorizes a game upload or publication. Gallery layout/compositor tooling is Fable-owned Lane A implementation; this protocol sets the visual acceptance rule.

## 5. Jutsu icon background and processing policy (director decision)

**Director decision (2026-10-14): newly authored TNR jutsu icons have designed backgrounds; transparency is NOT a required presentation property for jutsu icons.** Do not remove the designed background or create fake alpha just to satisfy a generic checker. This is a **jutsu-field decision**; do not generalize it to item, bloodline, avatar or character art, and do not retroactively rewrite existing live icons.

**Mechanical contract:** jutsu.image has its own spec target, **JUTSU_ICON**, in skills/producing-tnr-art/data/25x_DATA_art_spec.json. Its `alpha` policy is `optional`: scripts/artpreflight.py accepts an opaque RGB export and skips the alpha, soft-edge and residual-key checks that only apply to keyed art; a transparent jutsu icon is still held to every keyed check. Item and bloodline icons remain on shared **ICON** and still require alpha. Before that split, an opaque jutsu icon drew an **alpha** error and, on any near-lime colour in the design, a false **spill** error; treat any preflight record made before the split accordingly. The validator's verdict is still not a live-upload verification.

**Workstream byte caps.** A collection may set an export ceiling stricter than the spec's; record it in that collection's register and check it with `artpreflight.py --max-bytes N`, which fails a file of N bytes or more ("under N"). BBE's was under 80,000 bytes. A workstream cap never replaces the generic repo upload caps. Derive all other export numbers from the current spec; JUTSU_ICON recommends 256×256 and requires square lossless WebP with at least 160px width.

Use repository processing tools where their contract applies. **Do not run lime chroma key over an opaque designed background.** The opaque export is Pillow RGB resizing to 256×256 and lossless WebP export, followed by `artpreflight.py --type JUTSU_ICON [--max-bytes N]`. Always pass `--type` in this workflow: filename inference is a convenience that only accepts an allow-listed `<name>_jutsu[_icon]` / `jutsu_<name>` style name and refuses anything doubtful. If the export needs lossy encoding or destructive palette loss to meet a byte cap, present the visible quality tradeoff rather than silently changing the approved look.

### Production QC record

- Square/size checked against current target specification.
- Lossless WebP verified from actual container/codec (not extension alone).
- Background appearance and focal contrast visually checked at 125/64/32.
- Workstream byte cap, if the register sets one, checked with `--max-bytes`.
- Source and final SHA-256, dimensions, byte count and versioned filenames captured.
- artpreflight invoked with `--type JUTSU_ICON` (plus the workstream `--max-bytes`, if any) and full results recorded.
- Output @img filename identical to eventual manifest reference; ZIP entries and checksums checked when packaged.
- No upload, publication or game-state claim without the user-controlled game workflow.

The JUTSU_ICON acceptance path is Lane A tooling owned by Fable; further changes to it go through Lane A review. The studio does not silently patch the shared validator.

## 6. Repository evidence and handoffs

Keep collection-specific identity, silhouette ledger, approval state, byte cap and source evidence in that collection's register under docs/design/<collection>/ (worked example: docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md and SOURCE_EVIDENCE.json). If exact approved reference bytes are only in a conversation, label **conversation source / Git intake pending**, even if the local file was hashed. A reproducible future generation session needs an actual attached or repo-pinned reference image, not merely its SHA or a text description. Intake source binaries on a dedicated art branch when separately assigned; do not invent CDN URLs or overwrite approved files.

**Studio → generation:** one compact fenced brief and 1–2 approved individual references.  
**Generation → studio:** original candidate, exact target, approval status, generation/creation evidence if available.  
**Studio → operator/Fable:** versioned filename, type, bytes, SHA-256, QC and preflight verdict, remaining contract issues, @img wiring needs if any.  
**End of isolated session:** close after one accepted/rejected target. Do not reuse the thread for the next asset.

**Closing a collection:** when the director reports the collection done, mark its register CLOSED with the date and what the repository does and does not hold as evidence (exports, preflight records, uploads). Do not back-fill evidence that was never recorded.

This workflow changes neither the normal branch-ownership rules nor the user-only live-game upload boundary.
