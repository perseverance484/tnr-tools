# Director prompt: starter jutsu icons, Phase 1 (Academy Student)

- **For:** the art director, to paste into a generation session
- **Brief:** `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md` (RUL-2026-10-20-003, -004)
- **Status:** approved for main by dauntless, 2026-10-20
- **Live-game requests/writes:** 0

~~~text
You are the art director's generation session for The Ninja RPG. Task: new icons for the six
Academy Student jutsu (starter jutsu icons, Phase 1).

Read first (repo perseverance484/tnr-tools, branch main):
- docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md   (approved direction, RUL-2026-10-20-003/004)
- docs/workflows/ISOLATED_ART_GENERATION.md                (one jutsu per session, TARGET LOCK, P0 gates)
- skills/producing-tnr-art/data/25x_DATA_art_spec.json, target JUTSU_ICON

Standard: the approved jutsu-icon standard. Technique first, with NO ninja, face, body, hands or
limbs. One bold luminous silhouette plus one supporting effect, colour from the jutsu's theme,
full-bleed dark designed background (opaque is fine; don't fake transparency), and it must read as
one shape at 32 px. No text, frames, circular seals, floating runes or glyphs, franchise imagery,
or log-swap trope.

The six (reserved silhouettes from the register; each owns its shape, and the other five go in as
text exclusions):
1. Poisonous Senbon (poison: sickly green, bruise-violet accent): three thin senbon needles in
   flight on a rising diagonal, each trailing a venom drip.
2. Replacement Technique (plain chakra: cyan and white on deep navy): a dissolving chakra afterimage
   outline bursting into smoke, with a sharp displacement streak leaving it.
3. Searing Might (fire: ember orange and molten gold on charcoal): a convex shield of interlocking
   ember-hot chakra plates, front-on, heat shimmer at the rim. Not a dome or orb.
4. Sonic Slash (plain chakra): one razor-thin crescent cut crossing the frame, concentric shock rings
   bursting from its leading edge.
5. Soul Shackles (shadow/spirit: violet and spectral teal on black): spectral chains shooting forward
   in a straight line, near to far, snaring a torn wisp of soul flame.
6. Venomous Phobia (poison): a coiling cloud of venom miasma forming a looming, fanged dread-mask
   shape that closes in.

Reference per session: attach exactly ONE, as style/material only (rendering, contrast, rim light;
never its composition):
- 1, 5, 6: art/style_refs/jutsu_icons/bee/icon_bee_hemocure_v1.webp
- 2:       art/jutsu_icons/aerathiel/Aerathiel_Windshear_Decay_jutsu_v1.webp
- 3:       art/jutsu_icons/vaporia/vaporia_scorch_break_jutsu_icon_v1.webp
- 4:       art/jutsu_icons/aerathiel/Aerathiel_Particle_Cannon_jutsu_v1.webp
Never attach the current starter icons (they're ninja scenes) or the old live Bakuhatsu icons.

How:
1. One jutsu per session, using the register's "Copy-ready isolated-session brief". Fill in the
   target lock (jutsu id and exact name from the Phase 1 table), the silhouette, the camera/motion
   axis, the palette, the one reference, and the other five silhouettes as exclusions.
2. Generate exactly ONE square candidate. Show it to the director and wait for approval before the
   next jutsu. Two wrong-subject results in one session means close it and start clean.
3. Raw QC: right technique; distinct from the other five at 125/64/32 px; no anatomy; no ornamental
   glyphs.

Deliver: each approved original under its exact filename (icon-starter-<slug>.webp, as in the
register table; a correction gets _b, _c), plus a ledger row per file (filename, type JUTSU_ICON,
pixel size, bytes). Do not process or upload anything. Intake, preflight, the 3+3 family gallery and
the review-desk ticket happen afterwards in the studio.
~~~
