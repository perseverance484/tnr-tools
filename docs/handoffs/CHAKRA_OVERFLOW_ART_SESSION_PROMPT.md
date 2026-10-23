# Chakra Overflow: art session prompt (round 1)

- **Decisions (director, 2026-10-23; RUL-2026-10-23-002):** color **C** (chakra blue erupting into gold where it overflows);
  concept directions **D1, the breaking vessel**, and **D2, the flare**, plus a hybrid of the two.
- **Project brief (read first):** `docs/design/chakra_overflow/CHAKRA_OVERFLOW_ICON_PROJECT.md`.
- **How to use:** paste section 1 into a new art-director session. That session runs each brief in section 2 in its own
  isolated generation session (`docs/workflows/ISOLATED_ART_GENERATION.md`), one candidate per session, and returns
  the raws. Claude Code then runs every raw through `art/jutsu_icons/chakra_overflow/preview_in_context.py` for the
  director's side-by-side review.

## 1. Session prompt (paste into the art-director session)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session runs round 1 of the
Chakra Overflow icon project: docs/design/chakra_overflow/CHAKRA_OVERFLOW_ICON_PROJECT.md. Read it first.

Why this matters: Chakra Overflow is the most-used jutsu in the game (107,720 battle uses, 6.6% of all jutsu use;
1.6x the next). It is the universal damage buff that nearly every player opens with, so its icon is the most-seen icon
in the game. The director's words: "the most important icon in the game... Needs to be the best, most iconic, high
quality icon we do. Nothing less will suffice."

What the jutsu does: the user forces their chakra past its natural limit; for a short time every attack they make hits
far harder. It is a self buff (no target, no projectile). The icon must read as "POWER UP" before anything else.

Approved direction (director, 2026-10-23):
- Color C: a body of deep chakra blue that erupts into blazing gold and white-hot light where it overflows. Blue is
  the contained chakra; gold is the power breaking its limit. The gold must be the brightest thing in the frame.
- D1 "The breaking vessel": a brimming orb of chakra cracking open, light bursting through its fissures and spilling
  over its rim. It must read as power escaping, never as an object breaking (no debuff reading).
- D2 "The flare": a compact white-hot core with a crown of flame-tongues erupting upward, like a solar flare rising.
  Upward and explosive. It must read as chakra, never as a fireball.
- Hybrid: an orb whose overflow erupts upward as a flare.

Where players see it (game source): about 45 px wide in a mobile battle bar, 70 px on desktop, 112 px in the default
grid. Every tile has rounded corners and a border, and jutsu lists cover the BOTTOM-LEFT and BOTTOM-RIGHT corners with
28 px badges. The emblem therefore lives in the central area, bounded, glowing against dark space, and must read as one
shape at 32 px.

House style: the approved JUTSU_ICON standard. Detailed pixel-art rendering, crisp edges, strong rim light, luminous
core, high contrast, full-bleed dark designed background (opaque). One bold emblem that is the ability's metaphor (the
BEE lesson): the energy is the subject. References for rendering only (never copy their compositions):
art/style_refs/jutsu_icons/bee/icon_bee_unholy_enhancement_v2.webp and
art/jutsu_icons/scroll_jutsu/exports/icon_jutsu_celestial_dew_v1.webp.

Hard exclusions: no ninja, body, face, hands, fists or limbs; no text, kanji, runes, seals, mandalas or eye emblems; no
frame or UI; no franchise imagery (no Eight Gates, no Rasengan sphere with rotating lines, no Super Saiyan aura); no
spiral or vortex (the set already has three); no crescent, dragon, ring of fire, black sun, droplet, or pillar rising from
broken stone (all reserved by approved icons). Never attach the current Chakra Overflow icon to a generation.

Run the eight briefs in docs/handoffs/CHAKRA_OVERFLOW_ART_SESSION_PROMPT.md section 2, ONE per isolated generation
session, one square candidate each. Do not process, crop, upscale or upload anything. Return every raw with its brief id
(CO-D1a ... CO-H2) as the filename, e.g. raw_chakra_overflow_CO-D1a.png. Fail-fast before returning: reject any raw with
anatomy, glyphs, a spiral, or an emblem touching the frame edges, and regenerate that brief once.
~~~

## 2. Isolated generation briefs (one per session)

Shared header for every brief:

~~~text
Repository: perseverance484/tnr-tools
Workstream: Chakra Overflow icon project, round 1 (docs/design/chakra_overflow/CHAKRA_OVERFLOW_ICON_PROJECT.md)
Target: Chakra Overflow
Jutsu target lock: jutsu ID e2eC-x4UXc5m6QexNbx8w, display name Chakra Overflow; no bloodline
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION, one asset only
State: exploratory until the director approves
Live-game requests/writes: 0. Credentials: none.
Goal/action: self power-up; the user's chakra breaks past its limit and every attack hits far harder for a short time
Rendering lock: approved JUTSU_ICON standard; detailed pixel art, crisp edges, strong rim light, luminous core, high
contrast; full-bleed dark designed background (deep navy to black); opaque; reads as one shape at 32 px
Color lock (C): deep chakra blue body erupting into blazing gold and white-hot light where it overflows; gold is the
brightest value in the frame
References attached: icon_bee_unholy_enhancement_v2.webp and icon_jutsu_celestial_dew_v1.webp (rendering, contrast and
rim light only; not their composition)
Composition: one bounded emblem centered slightly above middle, filling about 70% of the frame; dark negative space on
all sides; nothing in the bottom-left or bottom-right corners; nothing touching the edges
Negatives: no ninja, body, face, hands or limbs; no text, kanji, runes, seals, mandalas or eye emblems; no frame or UI; no
franchise imagery; no spiral or vortex; no crescent, dragon, ring of fire, droplet, or pillar from broken stone
Generate exactly ONE square icon candidate. No collage. Do not process or upload it.
~~~

| Brief | Direction | Dominant silhouette and motion (add to the header) |
|---|---|---|
| **CO-D1a** | D1 breaking vessel | A perfect sphere of deep blue chakra, brimming and luminous, with jagged fissures across its upper half through which white-gold light blasts outward in sharp rays. Light spills over its top edge like liquid fire. Front-on, symmetrical, motion bursting outward from the cracks. |
| **CO-D1b** | D1 breaking vessel | A blue chakra orb seen from slightly below, its crown split wide open like a blooming bud; a geyser of gold-white light pours up and over the rim and cascades down its sides in glowing streams. Motion: up, then over and down. |
| **CO-D1c** | D1 breaking vessel | A heavy blue chakra orb straining at its limit: a web of bright gold fracture lines covers it, and gold light leaks from every seam in a radiant halo, the moment before it bursts. Motion: pressure pushing outward evenly. Must read as power, not damage. |
| **CO-D2a** | D2 flare | A small, intensely white-hot core low in the frame, from which a crown of gold flame-tongues shoots straight upward, edged in blue chakra, like a solar flare. Symmetrical, tall, explosive. Motion: vertical, rising. |
| **CO-D2b** | D2 flare | A blue chakra core with a tall gold-white flare erupting from its top in one great rising tongue, flanked by two smaller tongues, sparks streaming upward. Slight forward lean, like a rocket of power. Motion: upward with a slight lean right. |
| **CO-D2c** | D2 flare | A starburst core of white-gold light whose rays are all swept upward into a crown shape, blue chakra wisps trailing at the base. Reads as an upward-pointing burst, like a power-up spark. Motion: radial burst biased upward. |
| **CO-H1** | hybrid | A deep blue chakra orb whose top has burst open; from the opening a gold-white flare erupts straight upward in a crown of flame-tongues, while glowing overflow spills down the orb's sides. The orb is the body, the flare is the climax. Motion: up and out. |
| **CO-H2** | hybrid | A blue chakra orb cracked with gold light, its overflow gathering above it into one rising gold flare shaped like an upward arrowhead, sparks streaming off. Clear upward point at 32 px. Motion: rising. |

## 3. Intake (Claude Code)

1. Save raws to `art/jutsu_icons/chakra_overflow/candidates/` as delivered.
2. Run `python3 art/jutsu_icons/chakra_overflow/preview_in_context.py <sheet.png> <all raws> art/jutsu_icons/batch1/originals_live/original_chakra_overflow.webp`
   and send the sheet to the director, with notes against the brief's acceptance criteria (section 3).
3. The director shortlists one or two; round 2 briefs refine only those.
