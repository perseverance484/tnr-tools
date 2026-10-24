# Lane A handoff: pixelsnap (generated raw → real pixel art)

```text
Repository: perseverance484/tnr-tools
Branch: fable/pixel-art-snap
Base: aa57a04b (main at branch creation)
Implementation commit: daaef03b
Head: the commit that adds this file (FROZEN for review; exact SHA reported in the handoff message)
Integration target: main
```

## Objective

A deterministic processing step that turns an image model's "pixel art style" raw into genuine pixel art: one true
grid, a 16–24 colour palette, no speckle, exported at 256 px. Approved by the director as deep-dive choice C2
(RUL-2026-10-24-002; analysis in `docs/design/icon_overhaul/VISUAL_DESIGN_DEEP_DIVE.md` §4–6.4).

## Changed

| File | Change |
|---|---|
| `skills/producing-tnr-art/scripts/pixelsnap.py` | new tool (CLI + importable functions) |
| `skills/producing-tnr-art/scripts/pixelsnap_selftest.py` | new socket-free exit test (25 checks) |
| `skills/producing-tnr-art/SKILL.md` | one row in the scripts table |

Behaviour:

1. **detect:** periodic peaks of the column and row edge profiles (Pillow `ImageChops.difference` + BOX resize, so the
   heavy work runs in C); comb search over cell sizes 2–64 px in quarter-pixel steps; the smallest period within 90% of the
   best score; `detected` when the score ≥ 1.35. Advisory only.
2. **grid:** `--grid auto` aligns to the detected grid only when it gives 48–64 whole cells across; otherwise the
   **full frame** is divided into 64 cells (no cropping). `--grid N` and `--cell/--phase-x/--phase-y` override.
3. **cells:** optional median denoise (`--denoise`, default 5); each cell takes the most frequent colour of its inner 50%
   (25% margin per side), voting with a 96-colour median-cut palette.
4. **palette:** the final `--colors` palette (default 24) is chosen from the cell image (`MAXCOVERAGE`, `kmeans=4`, no
   dither), so small areas keep their colour.
5. **clean:** a pixel matching none of its four edge neighbours, where one colour holds ≥5 of its eight neighbours, takes
   that colour (lines survive). `--no-clean` skips.
6. **export:** nearest-neighbour to `--size` (default 256); `.png` or lossless `.webp` (`exact=True`); JSON report with
   input/output SHA-256, detection, region, grid source, colours used, cleaned count and notes (uneven scale, grid or colour
   outside the approved range, no grid detected).
7. **refusals** (exit 1, nothing written): missing or undecodable raw; transparency; unsupported output extension;
   `--colors` outside 2–256; bad `--grid`; even or <3 `--denoise`; raw smaller than the grid; `--size` below the grid;
   `--cell` out of range.

## Verification

| Command | Result |
|---|---|
| `python3 skills/producing-tnr-art/scripts/pixelsnap_selftest.py` (any cwd) | PASS, 25/25: grid 24 px and offset (7, 11) found; 50-cell art recovered at 100% match; 4×4 blocks exact on the 64 grid; palette ≤ `--colors`; small brown area kept; speck cleaned, 1 px line kept; painterly raw → no grid, full frame; 30-cell grid reported but not cropped to; manual override; 7 refusals write nothing; byte-identical reruns; export passes `artpreflight.py --type JUTSU_ICON` |
| `cd skills/producing-tnr-art/data && python3 ../scripts/artpreflight_selftest.py` | 98 passed, 0 failed (unchanged) |
| `python3 skills/producing-tnr-art/scripts/jutsu_studio_selftest.py` | 191 passed, 0 failed (unchanged) |
| `cd skills/building-tnr-content/scripts && python3 doctrinemap.py` | 0 errors, 0 warnings |
| `python3 render_doctrine.py --check` | all projections current (exit 0) |
| `python3 build_packs.py --check` | all packs and TOCs current (exit 0) |
| `python3 lawmap.py` | 0 errors, 5 warnings; the same 5 warnings on base `aa57a04b` (law-matrix citations, unrelated) |
| `python3 -m py_compile` on both new files | ok |
| Real raws (`art/jutsu_icons/chakra_overflow/raws/raw_chakra_overflow_v1.png`, `art/jutsu_icons/starter/raws/raw_starter_{replacement_technique,soul_shackles}_v1.png`) | ~2 s each; all three exports pass `artpreflight --type JUTSU_ICON` with 0 errors, 0 warnings; visual check: the log stays brown, sparkles no longer speckle |

## Source / provenance

- No game-source dependency. The 48–64 grid and 16–24 colour ranges come from RUL-2026-10-24-002 and are constants at the
  top of the file (`APPROVED_GRID`, `APPROVED_COLORS`); outside them the tool still runs and adds a note.
- Pillow only (approved dependency, CLAUDE.md §9); no NumPy. `get_flattened_data` is used when Pillow provides it, with a
  fallback to `getdata` for older versions.
- No generated artifacts.

## Risk / debt (attack these)

1. **Detection is heuristic.** On generated raws it rarely finds a meaningful grid in the approved range. Their
   pseudo-pixels run about 9–11 px (run-length histogram of the starter raws), and large periods (40–55 px) can score as
   "detected" by chance. Mitigation: alignment and cropping happen only when the detected grid gives 48–64 whole cells
   across; every other case uses the full frame. A false positive inside that band would crop by less than one cell per
   side.
2. **Busy raws stay busy.** The tool does not simplify composition. The Soul Shackles raw stays noisy at 64 cells; the art
   direction's gates (45 px recognition, silhouette) are meant to reject such raws upstream.
3. **Uneven scale.** Grids that do not divide 256 (e.g. 55) give 4–5 px art pixels at 256. This is reported, not
   prevented; the game downsizes every display anyway (≤160 px).
4. **Palette loss is now routine for jutsu icons.** `jutsu_studio.py finalize` treats quantisation as needing per-icon
   director approval. RUL-2026-10-24-002 approves 16–24 colours for this overhaul; pixelsnap runs before finalize and does
   not change that tool's policy. Reviewer: confirm this separation is acceptable.
5. Speed: ~2 s per 1254 px raw in pure-Python loops (per-cell voting and cleanup). Fine for a 35-icon batch.

## Live-game statement

Zero live requests, zero game writes, no credentials or session material. No browser checks: the tool is offline image
processing.

## Not begun / out of scope

- Wiring pixelsnap into `jutsu_studio.py finalize` or `artpreflight.py`.
- A pixel-integrity gate (deep dive G6) in artpreflight.
- Processing any production icon: no rework raws exist yet.
