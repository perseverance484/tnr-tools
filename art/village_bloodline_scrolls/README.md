# Village bloodline scroll icons

Brief: `docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md` (RUL-2026-10-20-005). Icon 1
locks the style and the scroll silhouette for icons 2-6.

| # | Scroll | Raw | Export | Status |
|---|---|---|---|---|
| 1 | Oblivion Seal | `raws/raw_village_scroll_oblivion_seal_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `09d2bdcbbd8f855bd571843cef31cf151c116b67aa695e2852f8d59030a53515`) | `exports/icon-village-scroll-oblivion-seal.webp` (256x256 lossless WebP RGBA, 48,584 bytes, sha256 `e8954f17c32bbe915a43e08395fca67460dcac7fba71170c99710ab15f2381a4`) | Director-approved 2026-10-21; locks the pixel-art rendering and silhouette for the set. Silver fittings |
| 2 | Shinseina Ki | `raws/raw_village_scroll_shinseina_ki_b.png` (PNG 1254x1254 RGBA, native transparency, sha256 `8136c2e2c23799727b04e95621d2af3b0cfa8aee9c914c0a6d617903d25fb6f5`) | `exports/icon-village-scroll-shinseina-ki_b.webp` (256x256 lossless WebP RGBA, 55,370 bytes, sha256 `c0eb91f83b16e022434babee01303ac857f441e5fab327bfe777c84db11046aa`) | Director-approved 2026-10-21. v1 was rejected as painted, not pixel art, and is not kept; `_b` is pixel art. Gold fittings and cream paper approved by the director, so fittings are per scroll, not locked to icon 1's silver |

## Processing

Both raws have native transparency, no chroma key. Resize to 256x256 (Pillow LANCZOS), then hard pixel-art alpha:
alpha below 96 to 0, 160 and above to 255 (icon 1: 24,131 of 65,536 pixels; icon 2: 25,576; the scroll
bodies were 252-253 in the raws, about 1% see-through). Three bright-magenta glow pixels pulled to violet (red capped at 214) so
preflight's key-residual check passes; the art was never keyed. Partial-alpha share 1.96% and 2.01%. Icon 2 needed no key nudge.
`artpreflight.py --type ICON`: 0 errors, 0 warnings. Composited on white, gold and dark: no fringe.

Icons 1 and 2 go to the review desk as push/154 (dauntless, 2026-10-21); icons 3-6 follow in a later ticket.
