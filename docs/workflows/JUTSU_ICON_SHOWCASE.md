# Workflow — Bloodline Jutsu Icon Family Showcase

**Status:** DIRECTOR-DIRECTED final Art Studio presentation/acceptance stage, 2026-10-15.  
**Lead:** Art Director (final composition/family review); **support:** Image Production (deterministic composition and technical evidence).  
**Applies to:** completed TNR bloodline *jutsu-icon families*, starting with the eight-icon BEE family. This is a final workstation artifact, **not** a replacement for the game icon exports, the Bloodright poster workflow, the art skill, or live publication.

**Route:** `docs/workflows/ART_PRODUCTION.md` -> `docs/workflows/ISOLATED_ART_GENERATION.md` -> **this workflow** once a family is ready for collective acceptance. `docs/00_INDEX.md`, `docs/DOCTRINE.md`, the current `skills/producing-tnr-art/` spec/scripts and the director's specific collection register retain their existing authority.

## 1. Purpose and end-to-end stage order

A bloodline Art Studio is not visually closed merely because its icon briefs have been generated separately. Its **last art/presentation phase** is a single labeled showcase of the *entire current family*, used to catch silhouette confusion, color/material drift and incorrect delivery metadata before the director signs off.

The normal sequence is:

1. Director individually accepts each **exact raw source**; resolve all reworks/withdrawn approvals. Record original filename, actual decoded format, raw hash and jutsu ID in the collection's source register.
2. Process **only currently approved source bytes** into versioned, spec-compliant jutsu-icon exports. Retain the source-to-export mapping, decoded format, dimensions, codec, byte length and SHA-256.
3. Inspect the processed icons individually and side-by-side at **125 / 64 / 32px**. Require a recognizable primary silhouette for each and no pairwise confusion with another approved icon.
4. **Generate one complete, neutral, labeled showcase of the actual N-icon family** in an adaptive, balanced grid from the exact processed outputs. The 4-columns x 2-rows BBE design applies **only** when N=8; smaller or larger bloodlines use count-appropriate layouts. The showcase is **composited deterministically**, not regenerated or repainted by an image model.
5. Director reviews the *entire set and the layout together*: all icons correctly named, in intended roster order, visually coherent and individually distinct. Accept/rework explicitly. If a jutsu changes, regenerate its export, pairwise QC and showcase; do not retain a stale accepted montage.
6. Record the accepted showcase, companion manifest, final per-file QC/preflight verdicts and any package evidence in the collection closeout. Close the *art-direction work* only after family acceptance. Live publishing remains a separate operator action.

**Showcase approval is not mechanical preflight.** A polished montage may be accepted as a presentation artifact while the approved opaque-background jutsu/export path is still blocked by the shared ICON alpha rule. Record the distinction; never claim `PREFLIGHT CLEAR`, `UPLOAD READY`, or `LIVE` without those separate gates actually passing.

## 2. BBE example — presentation pattern, not an approved final BBE pack

The director-supplied BBE example screenshot `1000018422.png` is **layout reference only**: the exact received image decodes as JPEG RGB, **1536 x 854px**, 484,739 bytes, SHA-256 `4eb7d3bca3f68dba02c81b4dbbdb1c3b65479bc1d08e03376dfa084f57c9026f`. Its eight icy examples do **not** establish final BBE artwork approval or delivery readiness. The BBE repository closeout records a separate 7/8-approval situation and an obsolete eight-file export bundle; do not override that evidence based on the screenshot.

The BBE-specific **eight-icon reference layout** is four columns x two rows on a **1536 x 854px** landscape canvas. It uses four square ~350px tiles per row, near x=24/404/784/1164 with y~24/442 and one caption beneath each tile. This is the precedent **for eight icons only**, not a rule about how many jutsu a bloodline has. The transferable presentation contract is balanced placement, identically sized square tiles, exact names/file sizes, and neutral gutters; the grid and canvas adapt to the bloodline's verified roster.
- **Plain dark navy/charcoal background**, no thematic poster illustration, decorative logo, title banner, rarity plate or card frame. Icon colors remain those of the approved individual assets. Do not add glow, sharpen, recolor, or alter any icon.
- One short, legible line under each tile: **exact approved jutsu display name + actual processed-file size**, e.g. `Blue Crimson 59.6kB`. Print **decimal kB = bytes / 1000**, rounded to one decimal (not KiB), taken from the inspected *current WebP file*. No guessed dimensions, effects or file sizes. All text belongs to the showcase only, **never** to a game icon.
- Keep caption font, position, contrast and spacing consistent. Fit the full jutsu name rather than cropping it. Use a consistent sans-serif typeface with a recorded rendering setup; no need to embed or distribute fonts.
- Render presentation copies of the exact **processed 256px exports** at equal square tile sizes with one consistent, inspected resampling method; the presentation resampling does not change the underlying delivery files.

## 2a. Variable-size bloodline families — adaptive layout rule

**Director correction (2026-10-15): bloodline jutsu count is NOT universally eight.** Many A-rank bloodlines have five jutsu; S-rank rosters vary, and all ranks must use the actual authoritative bloodline roster. **Never derive N from rank, assume a fixed template count, invent extra icons, silently omit a jutsu, or pad with fake empty showcase slots.** Resolve the exact current approved roster N before selecting the showcase grid.

The **number of icons determines the grid and canvas**, not the other way around. A balanced layout should give every icon the same square size and a readable caption, using centered incomplete rows. The following are **recommended starting arrangements**, subject to director approval for each bloodline:

| Exact roster count | Suggested composition | Notes |
| --- | --- | --- |
| 1–2 | Single row, N columns | Only the actual icons; no filler tiles. |
| 3 | One row of three | Equal square tiles and captions. |
| 4 | Two rows of two | Balanced compact square grid. |
| **5 (common A-rank)** | **Three across, two centered beneath (3 + 2)** | Keeps all five prominent, no blank placeholder. |
| 6 | Three across, three across (3 + 3) | Balanced two-row sheet. |
| 7 | Four across, three centered beneath (4 + 3) | No fake eighth tile. |
| **8 (BBE/BEE example)** | **Four across, four across (4 + 4)** | This alone uses the 1536 x 854 reference layout. |
| 9 | Three rows of three (3 + 3 + 3) | Avoid tiny five-across tiles. |
| 10–12 | Up to four per row, final incomplete row centered | E.g. 10 = 4 + 4 + 2; 11 = 4 + 4 + 3; 12 = 4 + 4 + 4. |
| 13 or more | Up to four columns, enough rows for all N | Extend canvas height. If too tall to review legibly, **ask the director** before splitting into multiple sheets. |

**Canvas rule:** size the presentation canvas **from the chosen column count and row count**. Do not crop, stretch, downsize to unreadability, or force every set onto a 1536 x 854 canvas. A close BBE-compatible example with 350px square tiles, 30px horizontal gaps, 44px caption bands, 24px vertical row gaps, 23px side margins, 24px top and 18px bottom margins yields:

- **Width = 46 + 350 × C + 30 × (C − 1)** pixels; with C=4, width=1536.
- **Height = 24 + (350 + 44) × R + 24 × (R − 1) + 18** pixels; with R=2, height=854.
- Center a partial row's complete group of tiles **within the same available grid width** rather than inserting empty/fake icon cards. Keep source square frames intact and exactly equal in presentation size.

The compositor may adjust tile/gutter/caption geometry **for an actual roster** with long labels or mobile legibility, but must record exact row lengths, canvas dimensions, tile size, caption placement and resampling method in the companion manifest. The director signs off on the layout along with the whole family. This is presentation guidance, **not implemented or tested as a reusable renderer**.

The BBE screenshot supplies **information layout**, not style conditioning for new BEE artwork. Never attach this contact sheet to an isolated icon-generation conversation.

## 3. Showcase input gate (hard stop)

For a family of N jutsu, before publishing a **final** showcase require:

| Check | Evidence |
| --- | --- |
| N/N exact individual raw approvals | Director decisions in the collection register; no current outstanding/shelved/unapproved slot |
| N/N current final processed files exist | Read and decode the actual bytes; expected filenames and SHA-256 match the source/output manifest |
| N/N correct identities | Jutsu name, ID, accepted raw version and processed WebP mapping agree |
| N/N export QC recorded | Square, current required size, codec, per-bloodline byte ceiling where one was actually approved, source-to-export provenance |
| 125 / 64 / 32 review complete | Thumbnail and pairwise confusion checks on the **processed** files |
| Preflight verdict is honest | `PASS`, actual `FAIL`, or explicit `BLOCKED` with exact cause; **not** silently treated as green |

If inputs are incomplete, a **clearly labeled internal draft contact sheet** is allowed for art comparison, but it cannot be titled "final showcase," accepted as final family evidence or presented with invented size labels. Do not place unapproved, superseded, rejected or mere original-game-reference pictures into a final family showcase.

## 4. Deterministic composition and review

- Compose **locally** from exact final WebP bytes (Pillow or an equivalently deterministic image compositor), never via image generation. The input family manifest defines order, source paths, checksums, actual processed byte sizes and names. The output must contain **only the roster's N current files once each**.
- Preserve the original square frames and full-bleed icon presentation, without cropping. Keep all icons comparable in scale. Inspect the final full-resolution contact sheet **and** a phone-sized/downscaled view, so captions and icon distinction survive a realistic Discord/mobile display.
- The director judges **family consistency and differentiation**, not just whether every tile looks attractive alone. Pay special attention to any adjacent icon pair with similar direction, silhouette or dominant focal shape. Revise the underlying individual icon in its isolated generation session if necessary—never use collage retouching to conceal a weak silhouette.
- Names and file-size captions must match the authoritative manifest. A caption `59.6kB` is valid only if the actual file is approximately 59,600 decimal bytes; screenshot text is never a source of file truth.
- Keep the showcase's own file **outside** the game-upload pack and out of any `@img` mapping. It is a QC/presentation deliverable, not the `jutsu.image` payload.

## 5. Deliverables and closure record

Use versioned, bloodline-qualified filenames (examples, not claims of existing outputs):

- `<slug>_jutsu_icon_showcase_v1.png` — lossless final **presentation image**.
- `<slug>_jutsu_icon_showcase_v1.manifest.json` — machine-readable provenance/inspection record.
- `<slug>_jutsu_icons_v1.zip` — **optional**, separate exact WebP package; never quietly substitute the screenshot for production files.
- Collection-specific `SHOWCASE_READINESS_*.md` or closeout document — what passed, director acceptance, what remains blocked.

The sidecar manifest must record: **actual N (count from the verified bloodline roster), complete row lengths and adaptive grid/canvas geometry**, bloodline name/ID, roster order with jutsu names/IDs, studio branch and **frozen source SHA**, for each tile the exact approved raw SHA-256, processed WebP filename/SHA-256/byte count/decoded dimensions and display label, canvas/layout settings, output PNG SHA-256, software/resampling configuration, 125/64/32 review evidence, director showcase acceptance status, and **independent** per-file preflight/package/live statuses. Null/unavailable values stay null, never fabricated.

Verify the showcase image and manifest against each other after rendering; if packaged, check ZIP entries, CRC and member bytes, and preserve the package SHA. A change to any approved source, export filename or bytes **invalidates** earlier showcase acceptance and requires regeneration/re-review.

**Closure verdict vocabulary:** `SHOWCASE NOT READY`, `SHOWCASE READY FOR DIRECTOR REVIEW`, `SHOWCASE ACCEPTED / EXPORT-OR-PREFLIGHT BLOCKED`, `ART STUDIO CLOSED — TECHNICAL DELIVERY OPEN`, and `DELIVERY ELIGIBLE` only when all actual export/preflight gates pass. Never conflate these with a live-game upload/readback.

## 6. Boundaries and code ownership

The user owns layout/art acceptance and all live-game actions. The Art Studio maintains records, guides production and creates an accurate showcase when the inputs are ready. The repository art skill owns the production spec; `docs/00_INDEX.md` owns routing and precedence. The current opaque jutsu background versus generic ICON alpha preflight mismatch **must remain recorded as blocked** until a separate reviewed contract/tool change or approved evidence-backed exception resolves it. Do not force transparent corners or report false clean results.

A reusable script/tool or change to canonical validator behaviour is **Lane A implementation** normally owned by Fable, with ChatGPT independent review, unless the director separately assigns implementation. This workflow specifies the showcase requirement; it does **not** claim that a general-purpose showcase builder has been implemented or tested.
