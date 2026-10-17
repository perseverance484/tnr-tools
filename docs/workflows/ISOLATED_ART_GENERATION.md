# Isolated Image Generation — TNR Art Studio Protocol

**Status:** Director-approved operating model, 2026-10-14 (RUL-2026-10-14-001).  
**Owner:** Art Studio coordination and Image Production under director acceptance.  
**Routes from:** docs/00_INDEX.md and docs/workflows/ART_PRODUCTION.md.  
**Scope:** ChatGPT-assisted creation of one production art asset at a time; Blue Blade Eyes (BBE) jutsu icons are the first proven case.

This is an **art-session coordination protocol**, not a replacement for skills/producing-tnr-art/SKILL.md, the current 25x_DATA_art_spec.json, docs/DOCTRINE.md, generated game contracts, or the user-controlled live upload path.

## 1. Session separation

| Session | Responsibility | Deliberately excluded |
| --- | --- | --- |
| **Art Studio / workspace** (persistent, can be reopened) | Reconstruct repo state; maintain an approved identity register and source ledger; decide next subject; write individual briefs; compare against the family; intake, verify, process, QC, package and record files | Image generation, silently changing accepted art, live-game requests/writes |
| **Isolated Generation** (new conversation for each asset) | Ingest one small art brief and one or two **individual** approved references; generate **one candidate at a time** for that subject; obtain director visual approval; return the original image | Other jutsu, icon sheets, broad repository writes, batch generation, processing, publishing |

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

The studio produces a copy-ready brief. Pass the actual selected image bytes with the prompt: a source filename or URL alone does not prove the generator saw the pixels. If the reference's bytes are not available, say so and do not claim a faithful reference-conditioned result.

## 3. Isolated generation contract

Open a **new project conversation**. Read the current TNR bootstrap and art authority without feeding an entire art library into image generation. Supply only the target brief and the selected one or two image references.

**Generate exactly one square, single-icon candidate**; no sheets or multi-icon panels. Use composition first, then apply rendering treatment:

- **Subject/action**: what the technique does in combat.
- **Silhouette**: the large-scale shape must be identifiable before decoration.
- **Rendering**: apply only the approved bloodline/material palette.
- **Chakra vocabulary**: motion blur, strike trails, binding structures, protective reinforcement, resonance or targeting only when appropriate to that jutsu. No mandatory chakra ring.
- **Exclusions**: forbid the concrete wrong compositions and actors that would erase the intended distinction.

**Approval loop:** show one candidate; director accepts, rejects or requests a same-subject revision. After two wrong-subject/composition failures, stop and reinitialize in a new isolated conversation. Once accepted, preserve the **original source bytes**, not a screenshot or a regenerated approximation, and return them to the studio with the target name and approval status.

The generator does not mark an image upload-ready, does not run game writes, and does not quietly alter the jutsu's mechanics.

### Copy-ready isolated-session brief

~~~text
Repository: perseverance484/tnr-tools
Workstream: <bloodline / collection>
Target: <single jutsu or asset>
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION — one asset only
State: exploratory until director approves
Live-game requests/writes: 0
Credentials: none

Initialize from live repository; verify main and read TNR art authorities.
Read the cited collection register for this one target.
Goal/action: <what the technique does>
Dominant silhouette: <one unmistakable shape>
Secondary effect: <one supporting action cue>
Rendering lock: <exact palette/material/facet/frost guidance>
References attached: <one or two individually, each labeled style-only/material-only/subject>
Composition: <orientation, negative space, focal hierarchy>
Distinctiveness exclusions: <already-used silhouettes + wrong-subject forms>
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

## 5. Jutsu icon background and processing policy (director decision)

**Director decision (2026-10-14): newly authored TNR jutsu icons have designed backgrounds; transparency is NOT a required presentation property for jutsu icons.** Do not remove the frosted background or create fake alpha just to satisfy a generic checker. This is a **jutsu-field decision**; do not generalize it to item, bloodline, avatar or character art, and do not retroactively rewrite existing live icons.

**Mechanical contract:** jutsu.image has its own spec target, **JUTSU_ICON**, in skills/producing-tnr-art/data/25x_DATA_art_spec.json. Its `alpha` policy is `optional`: scripts/artpreflight.py accepts an opaque RGB export and skips the alpha, soft-edge and residual-key checks that only apply to keyed art; a transparent jutsu icon is still held to every keyed check. Item and bloodline icons remain on shared **ICON** and still require alpha. Before that split, an opaque jutsu icon drew an **alpha** error and, on any near-lime colour in the design, a false **spill** error; treat any preflight record made before the split accordingly. The validator's verdict is still not a live-upload verification.

For **BBE**, the additional director-imposed export ceiling is **strictly less than 80,000 bytes** (more conservative than either 80,000 or 80 KiB at the boundary). This is a workstream limit, not an unapproved replacement for the generic repo upload caps; check it with `artpreflight.py --max-bytes 80000`, which fails a file of 80,000 bytes or more. Derive all other export numbers from the current spec; JUTSU_ICON recommends 256×256 and requires square lossless WebP with at least 160px width.

Use repository processing tools where their contract applies. **Do not run lime chroma key over an opaque designed background.** The opaque export is Pillow RGB resizing to 256×256 and lossless WebP export, followed by `artpreflight.py --type JUTSU_ICON --max-bytes 80000` (the type is inferred only from an allow-listed `<name>_jutsu[_icon]` style name with no evidence for any other target; otherwise pass `--type`, which is always safe). If the export needs lossy encoding or destructive palette loss to meet 80,000 bytes, present the visible quality tradeoff rather than silently changing the approved look.

### Production QC record

- Square/size checked against current target specification.
- Lossless WebP verified from actual container/codec (not extension alone).
- Background appearance and focal contrast visually checked at 125/64/32.
- Strict BBE 80,000-byte ceiling checked.
- Source and final SHA-256, dimensions, byte count and versioned filenames captured.
- artpreflight invoked against JUTSU_ICON (with the workstream `--max-bytes`) and full results recorded.
- Output @img filename identical to eventual manifest reference; ZIP entries and checksums checked when packaged.
- No upload, publication or game-state claim without the user-controlled game workflow.

The JUTSU_ICON acceptance path is Lane A tooling owned by Fable; further changes to it go through Lane A review. The studio does not silently patch the shared validator.

## 6. Repository evidence and handoffs

Keep collection-specific identity/approval/source-evidence in its register (for the pilot: docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md and SOURCE_EVIDENCE.json). If exact approved reference bytes are only in a conversation, label **conversation source / Git intake pending**, even if the local file was hashed. A reproducible future generation session needs an actual attached or repo-pinned reference image, not merely its SHA or a text description. Intake source binaries on a dedicated art branch when separately assigned; do not invent CDN URLs or overwrite approved files.

**Studio → generation:** one compact fenced brief and 1–2 approved individual references.  
**Generation → studio:** original candidate, exact target, approval status, generation/creation evidence if available.  
**Studio → operator/Fable:** versioned filename, type, bytes, SHA-256, QC and preflight verdict, remaining contract issues, @img wiring needs if any.  
**End of isolated session:** close after one accepted/rejected target. Do not reuse the thread for the next jutsu.

This workflow changes neither the normal branch-ownership rules nor the user-only live-game upload boundary.
