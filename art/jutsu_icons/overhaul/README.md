# Player jutsu overhaul icons

Register and direction: `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md`.

| Jutsu | Raw | Export | Status |
|---|---|---|---|
| Water's Domain | `raws/raw_waters_domain_v1.png` (PNG 1254x1254, sha256 `0067166e5540c2f1d9f24d4b53a2bdb0f27b46e51526fcf9f000dfb3239a9a4d`) | `exports/icon-jutsu-waters-domain.webp` (256x256 lossless WebP, 116,394 bytes, sha256 `f25305856592d39414a741c2b28b94aa35ec53e3daab93b05fb00d2717bf6b43`) | Director-approved 2026-10-21 ("Honestly this one is approved, it matches the art style enough"). Direction I1 (RUL-2026-10-21-007): a whirlpool with a foam rim and a glowing aqua centre. This is "Image B" in `docs/reviews/WATERS_DOMAIN_PIXEL_STYLE_ANALYSIS_2026-10-21.md`, whose noted gaps (coarser pixels than Vaporia, foam to the edges) the director accepted |

## Processing

Each export is its raw resized to 256x256 (Pillow LANCZOS), saved as lossless WebP, opaque RGB; no
retouching. `artpreflight.py --type JUTSU_ICON` (run from `skills/producing-tnr-art/data/`): 0 errors,
0 warnings.
