# Starter jutsu icons (Academy Student and Genin)

Register and direction: `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md` (RUL-2026-10-20-003).

| Jutsu | Raw | Export | Status |
|---|---|---|---|
| Replacement Technique | `raws/raw_starter_replacement_technique_v1.png` (PNG 1254x1254, sha256 `90e98a48298c81569d169f3413962425dcc35ce7e89c7237c4c7e0a082102893`) | `exports/icon-starter-replacement-technique.webp` (256x256 lossless WebP, 99,508 bytes, sha256 `d4a5fbb72cf887677665aafd9321651da6bd64c95bfb0c4d866206cf68d7d36b`) | Director-approved 2026-10-21 as an **exception** to the register's reserved silhouette (RUL-2026-10-21-001): a log in swirling smoke with two blue chakra arrows |
| Searing Might | `raws/raw_starter_searing_might_v1.png` (PNG 1254x1254, sha256 `b3e48c60d42f3814c01d1533da243cda272f4c5db3172ca7fe056377c988a097`) | `exports/icon-starter-searing-might.webp` (256x256 lossless WebP, 125,244 bytes, sha256 `b6a7f586f5b454e602d621b9fb9effbedce683e5227739a3cdadcce226fefe47`) | Director-supplied 2026-10-21; matches the register's reserved silhouette (a front-on shield of interlocking ember-hot plates) |

## Processing

Each export is its raw resized to 256x256 (Pillow LANCZOS), saved as lossless WebP, opaque RGB; no
retouching. `artpreflight.py --type JUTSU_ICON`: 0 errors, 0 warnings. The other four Phase 1 icons
and the 3+3 family gallery are still to come.
