# Village bloodline scroll icons

Brief: `docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md` (RUL-2026-10-20-005). Icon 1
locks the style and the scroll silhouette for icons 2-6.

| # | Scroll | Raw | Export | Status |
|---|---|---|---|---|
| 1 | Oblivion Seal | `raws/raw_village_scroll_oblivion_seal_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `09d2bdcbbd8f855bd571843cef31cf151c116b67aa695e2852f8d59030a53515`) | `exports/icon-village-scroll-oblivion-seal.webp` (256x256 lossless WebP RGBA, 48,584 bytes, sha256 `e8954f17c32bbe915a43e08395fca67460dcac7fba71170c99710ab15f2381a4`) | Director-approved 2026-10-21; locks the pixel-art rendering and silhouette for the set. Silver fittings |
| 2 | Shinseina Ki | `raws/raw_village_scroll_shinseina_ki_b.png` (PNG 1254x1254 RGBA, native transparency, sha256 `8136c2e2c23799727b04e95621d2af3b0cfa8aee9c914c0a6d617903d25fb6f5`) | `exports/icon-village-scroll-shinseina-ki_b.webp` (256x256 lossless WebP RGBA, 55,370 bytes, sha256 `c0eb91f83b16e022434babee01303ac857f441e5fab327bfe777c84db11046aa`) | Director-approved 2026-10-21. v1 was rejected as painted, not pixel art, and is not kept; `_b` is pixel art. Gold fittings and cream paper approved by the director, so fittings are per scroll, not locked to icon 1's silver |
| 3 | Arashima | `raws/raw_village_scroll_arashima_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `60d20d69a44aada5ce3c4f723e23b062943709cfe7a94c2ff2e6280928950953`) | `exports/icon-village-scroll-arashima.webp` (256x256 lossless WebP RGBA, 49,682 bytes, sha256 `95b0226858f21dae4c2c1c9cfae175a78dec41d5a2617f33271b0f2a647d5c46`) | Director-supplied 2026-10-21. Silver fittings |
| 4 | Taiyo Kami | `raws/raw_village_scroll_taiyo_kami_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `cbe5e10a0e52e9cf7649260ecdab4dcb247c911d77337ed06517b523ce42e83c`) | `exports/icon-village-scroll-taiyo-kami.webp` (256x256 lossless WebP RGBA, 55,798 bytes, sha256 `f44f49821fbfc5b3427b39994cbd3cb764caefb1dc1480f134b3177bfd60b09e`) | Director-supplied 2026-10-21. Gold sun-disc caps |
| 5 | Aerathiel | `raws/raw_village_scroll_aerathiel_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `d2a16161287b93a346ee3727d8babf39a04df1d98d852f4e9d54a6459322cd0f`) | `exports/icon-village-scroll-aerathiel.webp` (256x256 lossless WebP RGBA, 64,602 bytes, sha256 `f14ccd79d905a24ef9a7072d181409331ef1c003417888acf86fb986fa02b327`) | Director-supplied 2026-10-21. Gold fittings; translucent wind streaks |
| 6 | Hyouga Yui | `raws/raw_village_scroll_hyouga_yui_v1.png` (PNG 1254x1254 RGBA, native transparency, sha256 `08e21dbfd33ead1d9fbc6bf665cb9343bfdc90d209f23fd4320896e85eb918ba`) | `exports/icon-village-scroll-hyouga-yui.webp` (256x256 lossless WebP RGBA, 58,422 bytes, sha256 `e5237f8db9fb287642f3d8a9f4e297ef2c675f1c1a9ccf449f302ea7c5cf726b`) | Director-supplied 2026-10-21. Silver fittings |

## Processing

Both raws have native transparency, no chroma key. Resize to 256x256 (Pillow LANCZOS), then hard pixel-art alpha:
alpha below 96 to 0, 160 and above to 255 (icon 1: 24,131 of 65,536 pixels; icon 2: 25,576; icon 3: 23,836; icon 4: 24,204; icon 6: 24,135; the scroll
bodies were 252-253 in the raws, about 1% see-through). Three bright-magenta glow pixels pulled to violet (red capped at 214) so
preflight's key-residual check passes; the art was never keyed. Partial-alpha share 1.96%, 2.01%, 1.60%, 2.25% and (icon 6) 1.67%. Icons 2-6 needed no key nudge. Icon 5 (Aerathiel) uses a narrower band, below 112 to 0 and 144 and above to 255 (28,654 pixels), because its translucent wind streaks left 5.93% partial alpha at the default band; it lands at 2.93% with the streaks intact.
`artpreflight.py --type ICON`: 0 errors, 0 warnings. Composited on white, gold and dark: no fringe.

Icons 1-2 go to the review desk as push/154, 3-4 as push/155 and 5-6 as push/156 (dauntless, 2026-10-21). All six delivered.
