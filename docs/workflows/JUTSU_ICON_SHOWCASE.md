# Bloodline Jutsu Icon Family Showcase — deterministic, count-adaptive

**Status:** 2026-10-17 workflow consolidation from the director-directed BEE showcase protocol on `chatgpt/bee-jutsu-art-studio-20261014@1f6010be0967d1ed42645a1a7476b8a1ec2a75e2`, with the current `JUTSU_ICON` contract used instead of 2026-10-15 legacy generic-ICON/alpha assumptions.
**Scope:** visual family QC and final director acceptance for individually redesigned **jutsu.image** icons. **Not** fixed three-symbol Bloodright tier art or a production game upload image. Canonical source and art rules remain docs/00_INDEX.md, docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md, docs/workflows/ISOLATED_ART_GENERATION.md and the current producing-tnr-art skill/spec.

## Input gate

Require the exact verified full family of **N** current jutsu IDs and names from the bloodline's actual authoritative roster; do **not** assume N=8 or N=5 from bloodline rank or pack file count. All N current individual raw images must be director-approved, SHA-bound and present as actual accessible files. Every export must have an exact output filename/SHA, actual file bytes, decoded dimensions/VP8L status and separate preflight state. Obsolete/rejected/withdrawn candidates and old WebP versions are **not** members.

If any prerequisite is incomplete, an **internal DRAFT / incomplete** sheet for critique may be created, but never call it a final accepted gallery or invent missing tiles/data.

## Layout algorithm

All icons occupy **equal square presentation tiles** with a consistent caption band and neutral dark navy/charcoal gutters, no poster hero art, label banner, decorative frames, rarity UI or added backgrounds. No icon is cropped, repainted, sharpened, desaturated, recolored, composited with new glow or regenerated. Use the **exact accepted processed WebP bytes** and enlarge presentation copies uniformly with a recorded LANCZOS or comparably explicit resampling mode. The approved game's original exports remain unchanged.

Use a balanced adaptive grid:
- N=1–2: one row; N=3: 3; N=4: 2+2;
- N=5: **3+2 with the second row centered** (Vaporia precedent);
- N=6: 3+3; N=7: 4+3 centered; N=8: **4+4** (BBE/BEE precedent);
- N=9: 3+3+3; N=10–12: at most four per row, final shorter row centered;
- N>=13: at most four columns, extend canvas height. Ask the director before splitting the gallery across sheets for mobile legibility.

Choose canvas from row/column count, tile dimensions and captions; do not stretch a five-icon set to an eight-icon 1536x854 template. Proven prior canvases: BEE 8 (4+4), 1536x854; Vaporia 5 (3+2), 1156x854. These examples are **not** required sizes for other N. Record row lengths and coordinates in the companion manifest.

Each caption must contain the exact approved jutsu display name and the **current output WebP byte size in decimal kB rounded to one decimal**. This is bytes/1000, **not KiB**, and never a guessed raw-image size. Ensure long names fit and remain legible on mobile.

## Pixel/source assurance

A generated AI collage is **not** a valid showcase, even if the illustrations look similar: BEE demonstrated that a generator may replace individual icon artwork and invent size captions. Assemble with code only. Preserve the exact current output files as source assets; include manifest file/member SHA-256s and an assertion that every tile's pixels equal the corresponding processed WebP resized by the logged method. No wrong jutsu ordering, duplicated tiles or alternate versions.

Produce one full-resolution PNG gallery, one smaller phone review copy and optionally a **125/64/32-pixel QC composite** of actual WebPs. Inspect all views, particularly pairwise silhouette collisions and loss of contrast. The director accepts, rejects or requests targeted revisions **for the entire family**. If even one current approved icon changes, invalidate the old accepted gallery, re-export only the changed file, regenerate QC/sheet and ask for a fresh family acceptance; preserve the original accepted artifacts and their hashes as history.

## Output and status boundary

Companion manifest: `tnr.jutsu-showcase/1`, bloodline ID/name, exact N, array of {jutsu_id, jutsu_name, approved_raw_sha256, output_filename, output_sha256, output_bytes, position}, row lengths, canvas/padding/tile/caption geometry, compositor/resampler/version, gallery SHA, phone preview SHA, thumbnail QC, director family acceptance status and **separately recorded** `JUTSU_ICON` canonical preflight results.

Art studio closeout requires a director family-acceptance record or an explicit **family acceptance pending** status. The art direction may close despite that pending status, but cannot truthfully advertise *final gallery accepted*. Independent technical acceptance remains separate from artist acceptance.

The **current JUTSU_ICON** target permits opaque designed jutsu-image backgrounds and is distinct from item/bloodline ICON; historical claims that generic ICON alpha blocks opaque jutsu are superseded. The actual `artpreflight.py --type JUTSU_ICON` still must **run** on the current exported files before a formal zero-error preflight is claimed. A local pixel/ZIP pass, even 74 checks, cannot impersonate it.

The gallery/showcase itself is **not** placed inside a flat WebP-only game upload pack and is **never** a game `@img` replacement. User exclusively controls live-game actions and publication.
