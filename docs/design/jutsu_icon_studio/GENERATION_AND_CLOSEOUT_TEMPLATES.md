# Bloodline Jutsu Art Studio — Minimal Handoff Templates

**Status:** templates for docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md. Replace only named fields; use the Studio's verified source evidence, not guesses or old conversation context.

## A. Studio → ONE isolated image-generation conversation

~~~text
Repository: perseverance484/tnr-tools
Role: IMAGE PRODUCTION — one target
Session: ISOLATED JUTSU ICON GENERATION
Workflow: docs/workflows/ISOLATED_ART_GENERATION.md
Studio ref: <exact branch@SHA>
Bloodline: <name + ID>
Target jutsu: <name + exact ID>
Historical source/effect evidence: <pin/capture + gate>
Art state: DIRECTION APPROVED, RAW NOT YET ACCEPTED

Technique/action: <1 sentence supported by source>
Dominant unique silhouette: <one main shape>
Motion / one supporting effect: <one line>
Composition / negative space: <one line>
Shared family palette/material: <one line>
Other family silhouettes already reserved:
<brief conflicting-shape exclusions>
References attached individually:
1. <exact file> — IDENTITY ONLY (old jutsu)
2. <exact file if needed> — STYLE/MATERIAL ONLY
(Real image files must be attached, not just named.)
Requirements: square high-quality premium TNR icon,
technique-first, readable at 125/64/32; opaque designed
background allowed; no unrelated actor/text/UI/branding.

Generate exactly ONE candidate for this jutsu.
Ask for director acceptance; do not edit other jutsu.
No file compression, preflight, montage, live-game
operations or repo modifications in this thread.
~~~

**On return to Studio:** attach/locate the exact generated raw file, director yes/no, file MIME/dimensions/bytes/SHA and any withdrawn predecessor. Do not treat a screenshot as byte-identical raw evidence.

## B. Studio checkpoint after one jutsu

~~~text
Bloodline / ID: <...>
Jutsu / ID: <...>
Primary silhouette: <...>
Status: RAW VISUAL APPROVED | REVISION REQUESTED
Approved source: <filename, actual MIME, WxH, SHA-256>
Previous source superseded: <name/hash or none>
Family style: <short locked palette/material>
N current raw approved: <n>/<N>
Next isolated target: <name/ID>
Live requests/writes: 0/0
~~~

**Commit/record checkpoint only when meaningful:** family style lock; accepted raw batch; final accepted gallery/closeout. Avoid a new Git commit on every speculative prompt or wrong-icon revision.

## C. Full family closeout — keep it fielded

~~~text
Repository: perseverance484/tnr-tools
Workstream: BLOODLINE JUTSU ICONS (NOT Bloodright)
Bloodline / ID: <...>
Branch: <...>
Base / Merge-base: <...>
Frozen Head: <...>
Director raw approvals: <N>/<N>
Family showcase acceptance: APPROVED | PENDING
Source archive: <filename/bytes/SHA>
Export archive: <filename/bytes/SHA>
Exports: <N> VP8L lossless 256x256 RGB WebPs
Current spec ref: <...>
Workstream max bytes: <actual cap or none>
SHA/ZIP/125-64-32 QC: <actual verdict and evidence>
artpreflight --type JUTSU_ICON: <command/exit/verdict>
Binary Git pin: <yes exact ref or no>
Live requests/writes: 0/0
Uploads/readback: NOT PERFORMED | proven capture
Credentials: none
Next: <new bloodline Studio ZIP intake or exact missing gate>
~~~

## D. Expected final single family archive

Built by `jutsu_studio.py finalize` (docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md §8); deterministic, CRC- and hash-verified:

~~~text
<family>_jutsu_icons_closeout_<label>.zip
  manifest/studio_ledger.json   # exact jutsu_id -> raw/export hashes and every gate
  manifest/approved.json        # the Studio's approval record, exact bytes
  raws/                         # exact approved original bytes, never rewritten
  exports/                      # only the current accepted 256px VP8L WebPs
  qc/export_qc_<label>.json
  qc/preflight_<label>.json     # real artpreflight command, exit code, output
  showcase/<family>_jutsu_showcase_<label>.png (+ _phone.png)
  showcase/<family>_jutsu_thumbs_125_64_32_<label>.png
  showcase/showcase_manifest.json   # tnr.jutsu-showcase/1
  SHA256SUMS
~~~

**Companion:** `<family>_jutsu_icons_upload_<N>webp_<label>.zip` containing only the N flat game-size WebPs for mobile asset selection. Neither ZIP implies any in-game upload, publication or live read-back. Preserve any previous accepted or withdrawn version separately outside the active ZIP.

**Acceptance gating:** record current source/effect identity, individual raw approval, exact processed output, canonical preflight, family showcase and actual game record status separately. Do not call a family “finished in game” from an art closeout.
