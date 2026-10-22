# Two Tails armor icons

Request: `docs/handoffs/TWO_TAILS_ARMOR_ICONS_ART_REQUEST.md` (RUL-2026-10-22-001). Director prompt:
`docs/handoffs/TWO_TAILS_ARMOR_ICONS_DIRECTOR_PROMPT.md`.

`refs/` holds the seven Kitsune armor icons, the style reference, downloaded 2026-10-22 from the image URLs in
the push/204 capture (`harvests/inbox/tnr_results_1792629744565.json`), byte-identical (250x250 RGBA WebP).
Hashes in `SHA256SUMS`. Raws and exports for the five Two Tails pieces are added here after director approval.

## Pieces

All five director-approved 2026-10-22 (Shozoku first, as the style lock; the other four sent together with
"Here's the rest"). Raws are the delivered PNGs, byte-identical.

| Piece | Raw | Background | Export |
|---|---|---|---|
| Shozoku | `raws/raw_two_tails_shozoku_v1.png` (1254x1254, sha256 `eee0f42973729079…`) | native alpha (piece at 252-253, snapped to 255) | `exports/icon-two-tails-shozoku.webp` (256x256 lossless WebP RGBA, 56,424 bytes) |
| Zukin | `raws/raw_two_tails_zukin_v1.png` (1254x1254, sha256 `eab868ac0dc09cdb…`) | native alpha | `exports/icon-two-tails-zukin.webp` (256x256 lossless WebP RGBA, 44,944 bytes) |
| Tekkou | `raws/raw_two_tails_tekkou_v1.png` (1254x1254, sha256 `01cebf58a342e426…`) | native alpha | `exports/icon-two-tails-tekkou.webp` (256x256 lossless WebP RGBA, 43,160 bytes) |
| Tabi | `raws/raw_two_tails_tabi_v1.png` (1254x1254, sha256 `8839c7b6d512908a…`) | delivered RGB on near-black (0-1); background removed by edge flood fill at max channel <= 8, checked on grey and light composites | `exports/icon-two-tails-tabi.webp` (256x256 lossless WebP RGBA, 37,068 bytes) |
| Jaki-Tabi | `raws/raw_two_tails_jaki_tabi_v1.png` (1254x1254, sha256 `a990640a66725710…`) | native alpha | `exports/icon-two-tails-jaki-tabi.webp` (256x256 lossless WebP RGBA, 51,016 bytes) |

## Processing

Alpha at or above 240 snapped to 255; cropped to the piece and padded to a square at 80% fill (the Kitsune icons
fill 59-86%); resized to 256x256 with premultiplied Lanczos; edge band tightened (alpha below 80 to 0, 176 and
above to 255) so soft edges stay under the ICON 5% ceiling; lossless WebP. `artpreflight.py --type ICON`: 0
errors, 0 warnings on all five. Showcase: `showcase/two_tails_showcase_v1.png` (icons, game sizes, Kitsune
counterparts) and `showcase/two_tails_light_qc_v1.png` (edges on a light ground).
