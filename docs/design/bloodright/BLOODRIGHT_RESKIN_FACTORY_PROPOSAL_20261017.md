# Bloodright Emblem Reskin Factory — Proposed Method for Remaining 26 Bloodlines

**Status: PROPOSED — director acceptance required before replacing the present production protocol.**
**Date:** 2026-10-17. **Lead:** ChatGPT Art Director / Image Production; **support:** Fable only for durable, reusable image tooling and Forge structural import.
**Repository refs verified for proposal:** `main@b0267998bca90c128f10b591c862b79caec9b764`; approved Ethereal QC branch `chatgpt/ethereal-monarch-bloodright-art-qc-20261017@4cb46b4ee2076aaf3b122d197cb4c615d24c08eb`.
**Governing art process:** `docs/workflows/BLOODRIGHT_ICON_STUDIO.md` on this branch; status/roster `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md`.
**Prioritization:** director's Bloodright structural-rollout direction at `chatgpt/bloodright-structural-priority-20261017@620223109623ab044f0580b78ad1ebe5eac2b83c`. This plan does not replace the separately routed jutsu-icon redesign workflow.

## Director-supplied operating constraints

- **Opaque solid black/near-black backgrounds are approved and intentional.** Do not manufacture alpha, chroma-key them, or make rarity-frame clearance a creative design requirement. Jutsu source-image rarity/background considerations do not determine Bloodright tier art.
- The 29 public A/S/H Bloodright bloodlines use exactly **three universal tier emblems each**: Foundation nested pointed diamond, Hidden Art nested diamond with paired inward crescents/crosspieces, Advanced Art nested diamond with fixed multipoint starburst. **Only appearance is reskinned; geometry/layout never changes.** Each icon is used across the corresponding tier's skill nodes.
- This is **not a rework of the existing bloodline jutsu icons**. Their packs supply palette/material/identity evidence only.
- Approved visual/output count at proposal time: **BEE 3 + BBE 3 + Ethereal Monarch 3 = 9/87**. Remaining **26 bloodlines / 78 tier emblems**. Preserve the nine accepted outputs; do not regenerate them to fit a later batch.
- The actual shared `ICON` preflight still demands RGBA and is not the field-verified acceptance rule for `skillTree.image`. **This is a separate Fable technical gate, not a request for a second art-direction decision and not a reason to delay production of approved RGB masters.** No bundle can be represented as formally preflight-clear or live until applicable evidence exists.

## Proposed strategy: fixed-geometry template reskins, not 78 freeform redraws

**Core idea:** Freeze **three high-resolution approved source images as the tier geometry masters**, each with a stable foreground silhouette/bright-detail mask, black negative-space mask and glow mask. The accepted Ethereal Monarch 1254×1254 individual raw trio is a presently available, hashed **provisional** template source; BEE and BBE are additional visual anchors. Verify and durably pin actual master bytes before promising reproducible rebuilding; re-encoded conversation screenshots must never silently become the canonical originals.

Then generate each bloodline family from one coordinated **theme recipe**, applying that recipe to the **same three masters**:
1. Color-transfer/hue/luminance mapping based on the actual bloodline ZIP, maintaining shadow separation and white-hot focal sparkle hierarchy. Preserve source coordinates and edges.
2. Adjust the material appearance by **masked treatments** (e.g., glass/frost, molten fissures, polished metal, jade, radiant filigree), but only within the locked emblem geometry and pre-existing approved glow envelope. These do not create new shapes, rings, weapons, characters, runes, ornaments or different negative space.
3. If deterministic recolor/material treatment cannot faithfully express a theme at premium quality, use a **focused reference-conditioned image edit** or isolated generation for that bloodline, with exact shape master(s) attached. Result still must pass geometry QC and separate asset acceptance. Never solve a reskin by image-generating a three-icon contact sheet: previous sheet attempts changed the emblems.
4. **Three independent square originals are the only accepted art artifacts.** Any preview sheet is a **programmatically composited QC preview** of those exact three files, never a fourth generative interpretation.

The strict shape lock is the scalability gain: a director review should answer **“does this bloodline look right?”**, not **“did the model redraw the tier symbol?”**

## Intake and wave plan

**Input from operator:** existing bloodline art ZIPs, optionally as **one outer ZIP containing the remaining 26 inner ZIPs**, or in mobile-friendly **waves of roughly 5–6 bloodlines**. Do not make a bespoke Forge capture or master reference-library download a prerequisite now that the operator already holds the image packs.

**Safe source intake:** unpack with a ZIP path/size safety gate; verify `manifest.json` where supplied against actual bytes and SHA-256, exact bloodline/jutsu identities against the approved 29-cohort tracker; reject ambiguous extras or missing images; inspect a representative 2–4 **individual** jutsu images and the identity image for each bloodline; do not treat jutsu names as color evidence. Log exact originals, not re-encoded screenshots, and do not feed all reference images into an image generator.

**Treatment cards:** Before processing a wave, propose a compact table of the 5–6 bloodlines: sampled palette anchors, primary/secondary accents, material and glow treatment, nearest competing bloodline/overlap risks, selected source image IDs and any uncertain reference. Director can approve/revise theme cards as a wave without opening 26 separate art-direction discussions.

**Batch previews:** Produce **three independently saved images per bloodline** from the locked masters, then a compact matrix **rows = bloodlines / columns = Foundation, Hidden Art, Advanced Art** for user comparison. Mark each row as PROPOSED; the user accepts/revises/rejects **per bloodline**. A wave approval never silently approves an uninspected output. Edit only the rejected families and never mutate a frozen approval.

**Pilot the factory on two contrasting unapproved bloodlines**—prefer **Taiyo Kami** plus a strongly non-solar example such as **Godstorm Eclipse** once both supplied source ZIPs have been inspected—to verify that the same shapes can support different material identities. After director acceptance of pilot method, repeat across the remaining 24 bloodlines in practical waves aligned with Forge import readiness.

**Single-session option:** The user's previously tested practice of *one fresh, dedicated production conversation per bloodline* producing the coordinated 3-icon trio is preferred here **only if the director approves this factory protocol update**. The current `BLOODRIGHT_ICON_STUDIO.md` still says **one isolated generation conversation per individual tier image**, so change that workflow explicitly after method approval; do **not** silently treat the art-factory proposal as a canonical exception. A deterministic no-generation pass may batch all three pixels together under one theme recipe.

## Acceptance, files, and delivery

For each bloodline, preserve and verify:
- **Source pack:** exact ZIP hash, per-jutsu manifest/image hashes, approved bloodline ID/rank.
- **Geometry lock:** same centered diamond/crescent/starburst silhouette masks, outer bounds and primary landmarks as the frozen tier master; clean black negative space. Reject changed layouts or added halos/rings. Measure foreground-mask overlap at several brightness thresholds (with tolerances for glow/color changes) and inspect images at the actual display scale.
- **Appearance:** matched material/palette across trio; cross-bloodline distinction (especially Ice/Storm/Magnet/Shadow/Yin-Yang comparisons); bright central sparkle and clear hierarchy. No rarity-frame design work.
- **Export:** source raw saved intact; independent `256×256` lossless RGB WebPs (unless the field-verified spec later instructs otherwise), appropriate byte ceiling, exact versioned filenames/sha256s; review at **125/64/32** pixel sizes. Verify decoded equality against deliberately resized approved sources, ZIP membership and CRC.
- **Evidence:** `VISUAL APPROVED`, `SOURCE HASH VERIFIED`, `WEBP/THUMBNAIL/ZIP QC PASSED`, `PREFLIGHT FIELD-CONTRACT STATUS`, `GIT/IMMUTABLE PACK BINDING` and `OPERATOR GAME READBACK` are distinct fields. Never promote any status without its own evidence.

**Output per bloodline**:
```text
BR-XXX_<Bloodline>_Bloodright_Approved.zip
  approved_raw/{foundation,hidden_art,advanced_art}.png
  webp256/brXXX_<slug>_{foundation,hidden_art,advanced_art}_v01.webp
  qc/{family_125_64_32.png}
  treatment.json
  manifest.json
```
An optional aggregated `Bloodright_Emblems_Approved_Wave_N.zip` contains the individually approved packages; the final collection of **all 29 sets (87 icons)** is a packaging/export convenience, not an additional live-game step. Preserve BEE/BBE/Ethereal source/bytes rather than reinterpreting them. If their earlier accepted original bytes cannot be recovered, explicitly mark incomplete archive provenance rather than filling gaps with new approximations.

**Parallel structural lane:** Fable can take each completed **three-WebP package** and prepare the matching Forge tier-category `icons`/immutable imagePack binding in parallel with art waves. Current importer supports the three tier categories, but hidden structural import still separately needs valid five-BP trees, names, prerequisite wiring, accepted potency effects, explicit Seichi Silver/rounds per node and operator-controlled validation. `20` Silver / `99` rounds is **BEE only**, not an automatic global default. **No live-game requests/writes or publication** by this proposal or the art-production agent.

## Proposed action after director approval

1. Reconcile canonical geometry master binaries, record exact hashes, and test a **two-bloodline contrasting pilot** with the operator's source packs.
2. Director reviews the six independent outputs in one composed QC matrix; revise only appearance/geometry faults.
3. Freeze the factory settings and adopt the *one bloodline / three-emblem coordinated reskin* exception in the owning workflow (with the director's approval); implement repeatable processor/gates under proper writer/review ownership if code is needed.
4. Work through the remaining 24 families in grouped previews and exports; feed approved 3-icon outputs to Fable for import packaging as soon as ready.
