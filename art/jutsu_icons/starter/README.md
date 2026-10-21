# Starter jutsu icons (Academy Student and Genin)

Register and direction: `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md` (RUL-2026-10-20-003).

| Jutsu | Raw | Export | Status |
|---|---|---|---|
| Replacement Technique | `raws/raw_starter_replacement_technique_v1.png` (PNG 1254x1254, sha256 `90e98a48298c81569d169f3413962425dcc35ce7e89c7237c4c7e0a082102893`) | `exports/icon-starter-replacement-technique.webp` (256x256 lossless WebP, 99,508 bytes, sha256 `d4a5fbb72cf887677665aafd9321651da6bd64c95bfb0c4d866206cf68d7d36b`) | Director-approved 2026-10-21 as an **exception** to the register's reserved silhouette (RUL-2026-10-21-001): a log in swirling smoke with two blue chakra arrows |
| Searing Might | `raws/raw_starter_searing_might_v1.png` (PNG 1254x1254, sha256 `b3e48c60d42f3814c01d1533da243cda272f4c5db3172ca7fe056377c988a097`) | `exports/icon-starter-searing-might.webp` (256x256 lossless WebP, 125,244 bytes, sha256 `b6a7f586f5b454e602d621b9fb9effbedce683e5227739a3cdadcce226fefe47`) | Director-supplied 2026-10-21; matches the register's reserved silhouette (a front-on shield of interlocking ember-hot plates) |
| Poisonous Senbon | `raws/raw_starter_poisonous_senbon_v1.png` (PNG 1254x1254, sha256 `0430d63cbeeb33bc394434fb6c33eae094e4af3c51fa85aeb74eb0c697b4f1bc`) | `exports/icon-starter-poisonous-senbon.webp` (256x256 lossless WebP, 29,498 bytes, sha256 `d7624bcba78984ab589fbbe48131696612363e5fbb1e8f79f2b3af01631aea22`) | Director-supplied 2026-10-21; matches the register's reserved silhouette (three venom-dripping senbon on a rising diagonal). Plain black ground rather than a designed atmosphere |
| Sonic Slash | `raws/raw_starter_sonic_slash_v1.png` (PNG 1254x1254, sha256 `35ef5ca0272407b38912d158e24605da126068c51a051f6df5e3fe84b62e1e1d`) | `exports/icon-starter-sonic-slash.webp` (256x256 lossless WebP, 83,022 bytes, sha256 `b27435b3828906e3179ffa9309e71121b9b7d2e6e85f4540905fa3b63781ad65`) | Director-supplied 2026-10-21; matches the register's reserved silhouette (one crescent cut with concentric shock rings) |
| Soul Shackles | `raws/raw_starter_soul_shackles_v1.png` (PNG 1254x1254, sha256 `9782cc04b95ba609d6c40cf65832a34660abb255e0fb4defe9c4ef6a2f99e101`) | `exports/icon-starter-soul-shackles.webp` (256x256 lossless WebP, 117,478 bytes, sha256 `3a4a6a2899528cf2d7491d878ccdc1c2145b0c406ed7c19c4e73c67fdeda64ac`) | Director-supplied 2026-10-21; matches the register's reserved silhouette (spectral chains shooting near to far into a wisp of soul flame) |

## Processing

Each export is its raw resized to 256x256 (Pillow LANCZOS), saved as lossless WebP, opaque RGB; no
retouching. `artpreflight.py --type JUTSU_ICON`: 0 errors, 0 warnings. The other two Phase 1 icons
and the 3+3 family gallery are still to come.
