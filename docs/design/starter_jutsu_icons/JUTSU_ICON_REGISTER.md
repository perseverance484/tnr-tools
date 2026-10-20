# Starter jutsu icons — identity register and art request

**Status:** PHASE 1 OPEN (2026-10-20). Direction approved by dauntless: the approved jutsu-icon
standard (technique first, no ninja figure, one bold silhouette per jutsu, element-themed colour),
starting with the six Academy Student jutsu. Per-jutsu silhouettes below are proposals; the director's
visual approval of each raw locks it.
**Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one jutsu per generation session, jutsu
TARGET LOCK, P0 fail-fast gates). Worked example: `docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md`.
**Spec:** `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `JUTSU_ICON`.
**Source basis:** the public `jutsu.getAll` read of 2026-10-20 (see `docs/reviews/QA_LIVE_2026-10-20.md`).
**Live-game requests/writes:** 0. Nothing here uploads, edits or publishes.

## Why

The 62 visible NORMAL jutsu that Academy Students and Genin learn are the first icons every player
sees, and the weakest in the game. Nearly all are small pixel-art scenes of the same generic ninja
posing in a landscape: at 64 px and below they collapse into look-alike blobs, the technique itself
is a small streak, and the actor breaks the current jutsu-icon rules (anatomy off by default, P0 C).

## Collection-wide visual lock

- **Rendering:** the approved JUTSU_ICON standard (`art/style_refs/jutsu_icons/`, RUL-2026-10-17-021):
  one luminous technique-specific silhouette, one supporting effect, strong rim light, high contrast,
  clean dark negative space, reads as one shape at 32 px.
- **No actor:** no ninja, face, body, hands or limbs. The technique alone.
- **Colour by theme** (these jutsu carry no element classification, so colour follows the technique):

  | Theme | Palette |
  |---|---|
  | Fire | ember orange and molten gold on charcoal |
  | Water | deep blue and white foam |
  | Wind | pale jade and white air on slate |
  | Earth | ochre stone and dust on umber |
  | Lightning | violet-white arcs on indigo |
  | Poison | sickly green with a bruise-violet accent |
  | Shadow / genjutsu / spirit | violet and spectral teal on black |
  | Plain chakra | cyan and white on deep navy |

- **Background:** full-bleed designed dark atmosphere in the theme palette; opaque is approved,
  transparency not required (RUL-2026-10-14-001). Do not fake transparency.
- **Avoid:** actors, text, frames, grids, mandatory circular seals, floating runes or ornamental
  glyphs (P0 D), franchise imagery. In particular no log-swap substitution trope.

## References (pass actual bytes, individually)

- **Style anchor for every Phase 1 icon:** `art/style_refs/jutsu_icons/bee/icon_bee_hemocure_v1.webp`,
  **style/material only** (value contrast, rim light, focal hierarchy). Not its red palette, and not
  its orb-in-claws composition, which BEE reserves.
- **Do not attach the current icons.** `style_refs.py select` normally pairs the legacy identity icon
  with one exemplar, but these legacy icons are actor scenes and would pull the generator back to a
  ninja figure. Identity is carried by the target lock text instead.

## Phase 1: Academy Student jutsu (6)

| # | Jutsu | Id | What it does (live) | Theme | Reserved silhouette and action | Delivery filename |
|---|---|---|---|---|---|---|
| 1 | Poisonous Senbon | `H9XLJiU1YEro03QJ2mH8q` | 60 AP single-target damage | Poison | a tight volley of **three thin senbon needles** in flight on a rising diagonal, each trailing a venom drip | `icon-starter-poisonous-senbon.webp` |
| 2 | Replacement Technique | `clh4d6pok0002tb0hx1bxro6l` | 20 AP move to an empty tile | Plain chakra | a **dissolving chakra afterimage outline** bursting into smoke, with a sharp displacement streak leaving it | `icon-starter-replacement-technique.webp` |
| 3 | Searing Might | `clh4d6q1j0008tb0hzthddb6m` | 40 AP self buff: less damage taken | Fire | a **convex shield of interlocking ember-hot chakra plates**, front-on, heat shimmer at the rim | `icon-starter-searing-might.webp` |
| 4 | Sonic Slash | `clh4d6pxd0006tb0h4y1yudi5` | 60 AP single-target damage | Plain chakra | **one razor-thin crescent cut** crossing the frame, with **concentric shock rings** bursting from its leading edge | `icon-starter-sonic-slash.webp` |
| 5 | Soul Shackles | `clh4d6psu0004tb0hsa5cshh6` | 60 AP damage in a straight line | Shadow / spirit | **spectral chains shooting forward in a straight line** from near to far, snaring a torn wisp of soul flame | `icon-starter-soul-shackles.webp` |
| 6 | Venomous Phobia | `9oirFnLa0wejelNYpewq6` | 40 AP debuff: target takes more damage | Poison | a **coiling cloud of venom miasma** forming a looming, fanged dread-mask shape that closes in | `icon-starter-venomous-phobia.webp` |

**Distinction ledger (pass the other five as text exclusions in each brief):**

- 1 owns *needles*; 6 owns *a looming miasma mask*. Both are poison-green, so neither may borrow the
  other's shape: no needles in 6, no fog face in 1.
- 2 owns *afterimage plus smoke*; no smoke in any other icon.
- 3 owns *a shield*; no shield or armour anywhere else.
- 4 owns *a crescent cut with shock rings*; no other icon uses an arc slash or rings.
- 5 owns *chains*; no chains or bindings elsewhere.

**Text notes for a later ticket (not art):** Poisonous Senbon's description says venom, but its only
effect is plain damage; "Venomous Phobia." has a stray full stop in its name.

## Copy-ready isolated-session brief (fill per jutsu)

~~~text
Repository: perseverance484/tnr-tools
Workstream: Starter jutsu icons, Phase 1 (docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md)
Target: <jutsu name>
Jutsu target lock: jutsu ID <id>, display name <exact name>; no bloodline
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION, one asset only
State: exploratory until director approves
Live-game requests/writes: 0. Credentials: none.

Goal/action: <what it does, from the register>
Dominant silhouette: <reserved silhouette from the register>
Camera/perspective and motion axis: <e.g. rising diagonal, near-to-far, front-on>
Secondary effect: <one supporting cue>
Rendering lock: approved JUTSU_ICON standard; <theme palette from the register>; full-bleed dark
designed background; opaque is fine; reads as one shape at 32 px
References attached: icon_bee_hemocure_v1.webp (style/material only: contrast, rim light, focal
hierarchy; not its palette, not its orb-in-claws composition)
Composition: one centred-to-diagonal focal shape, clear negative space, nothing touching the edges
Distinctiveness exclusions: <the other five reserved silhouettes from the ledger>
Other negatives: no ninja, no face, no body, no hands or limbs, no text, no UI, no frame, no circular
seal or floating runes, no franchise imagery, no log substitution

Generate exactly ONE square icon candidate for review.
Do not generate other techniques or a collage.
Do not process or upload the image.
Return the original asset after director visual approval.
~~~

## Intake and delivery

- Raw QC (protocol section 3 fail-fast): right technique, distinct from the other five at 125/64/32 px,
  no anatomy, no ornamental glyphs.
- Processing: square lossless WebP, 256x256 recommended, at least 160 px, under 460,800 bytes;
  `artpreflight.py --type JUTSU_ICON`; family gallery through `jutsu_studio.py finalize` once all six
  are approved (gallery layout 3+3).
- Delivery names exactly as in the table; corrections get a fresh name (`_b`, `_c`).
- After intake the six icons go to the content review desk as one Forge suggest-mode ticket
  (category VISUAL, title "Update icon", one rationale per jutsu). Jutsu equipped on AIs need the
  unequip/re-equip sequence (laws 18/60); these six are not equipped on any captured AI.

## Later phases (Genin, 56 jutsu)

Batched by theme, 6 to 10 per phase, each with its own distinction ledger: wind, water, lightning,
earth, fire, taijutsu and body techniques, shadow and genjutsu, and utility. The roster is in the
2026-10-20 read; the phase tables are written when Phase 1 is approved.

## Status ledger

| # | Jutsu | Status |
|---|---|---|
| 1 | Poisonous Senbon | NOT STARTED |
| 2 | Replacement Technique | NOT STARTED |
| 3 | Searing Might | NOT STARTED |
| 4 | Sonic Slash | NOT STARTED |
| 5 | Soul Shackles | NOT STARTED |
| 6 | Venomous Phobia | NOT STARTED |
