# Village bloodline scroll icons

Brief: `docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md` (RUL-2026-10-20-005). Icon 1
locks the style and the scroll silhouette for icons 2-6.

| # | Scroll | Raw | Export | Status |
|---|---|---|---|---|
| 1 | Oblivion Seal | `raws/raw_village_scroll_oblivion_seal_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `09d2bdcbbd8f855bd571843cef31cf151c116b67aa695e2852f8d59030a53515`) | `exports/icon-village-scroll-oblivion-seal.webp` (256x256 lossless WebP RGBA, 53,350 bytes, sha256 `e8954f17c32bbe915a43e08395fca67460dcac7fba71170c99710ab15f2381a4`) | Director-supplied 2026-10-21; locks the set. Fittings are silver rather than the brief's aged gold; icons 2-6 follow icon 1 |

## Processing (icon 1)

Native transparency, no chroma key. Resize to 256x256 (Pillow LANCZOS), then hard pixel-art alpha:
alpha below 96 to 0, 160 and above to 255 (24,131 of 65,536 pixels; the scroll body was 252-253 in the
raw, about 1% see-through). Three bright-magenta glow pixels pulled to violet (red capped at 214) so
preflight's key-residual check passes; the art was never keyed. Partial-alpha share 1.96%.
`artpreflight.py --type ICON`: 0 errors, 0 warnings. Composited on white, gold and dark: no fringe.

All six go to the review desk as one Forge suggest-mode ticket once delivered.
