# Starter jutsu icons — identity register and art request

**Status:** PHASE 1 OPEN (2026-10-20). Reference families extended by RUL-2026-10-20-004. Direction approved by dauntless: the approved jutsu-icon
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

## Approved comparison families

Besides the pinned BBE and BEE library (`art/style_refs/jutsu_icons/`), dauntless has approved three
more bloodline sets as part of the standard (2026-10-20): **Vaporia**, **Bakuhatsu** and
**Aerathiel**. All are pinned in the repository under `art/jutsu_icons/`.

- **Vaporia** and **Aerathiel:** director-approved WebP exports (2026-10-19). They are byte-identical
  to the live icons in the 2026-10-20 public read (256x256, opaque RGB).
- **Bakuhatsu:** the approved set is the **2026-10-19 "Concussive Fracture" raws** in
  `art/jutsu_icons/bakuhatsu/raws/`, not the live icons. The live Bakuhatsu icons are the old
  figure-silhouette set, superseded and **not** a reference. The raws, their WebP exports
  (`art/jutsu_icons/bakuhatsu/exports/`) and the family showcase are all director-approved
  (2026-10-20); push/142 sends the exports to the review desk.

| Family | Jutsu | What it shows | Pinned file |
|---|---|---|---|
| Vaporia | Azure Dragon Palm | a coiling water dragon | `art/jutsu_icons/vaporia/vaporia_azure_dragon_palm_jutsu_icon_v1.webp` |
| Vaporia | Drowning Strike | a crushing water column | `art/jutsu_icons/vaporia/vaporia_drowning_strike_jutsu_icon_v1.webp` |
| Vaporia | Liquid Ember Shell | a water sphere with an ember core | `art/jutsu_icons/vaporia/vaporia_liquid_ember_shell_jutsu_icon_v1.webp` |
| Vaporia | Scorch Break | a fire fissure splitting water | `art/jutsu_icons/vaporia/vaporia_scorch_break_jutsu_icon_v1.webp` |
| Vaporia | Surfing Strike | a breaking wave with an ember edge | `art/jutsu_icons/vaporia/vaporia_surfing_strike_jutsu_icon_v1.webp` |
| Bakuhatsu | Blast Shield | a circular fire barrier deflecting debris | `art/jutsu_icons/bakuhatsu/raws/raw_bakuhatsu_blast_shield_v1.jpg` |
| Bakuhatsu | Charge 4 Explosion | linked micro-detonations tracing a "C4" on cracked ground | `art/jutsu_icons/bakuhatsu/raws/raw_bakuhatsu_charge_4_explosion_v1.jpg` |
| Bakuhatsu | Howitzer Crash | a V-shaped bow shock converging on one point | `art/jutsu_icons/bakuhatsu/raws/raw_bakuhatsu_howitzer_crash_v3.png` |
| Bakuhatsu | Inferno Cataclysm | a fire pillar erupting from a fissure, tilted stone slabs | `art/jutsu_icons/bakuhatsu/raws/raw_bakuhatsu_inferno_cataclysm_v1.jpg` |
| Bakuhatsu | Kinetic Nova | an airborne cluster of many small explosions | `art/jutsu_icons/bakuhatsu/raws/raw_bakuhatsu_kinetic_nova_v1.jpg` |
| Aerathiel | Atomic Shield | a swirling energy sphere | `art/jutsu_icons/aerathiel/Aerathiel_Atomic_Shield_jutsu_v1.webp` |
| Aerathiel | Death's March | a rising vortex column with debris | `art/jutsu_icons/aerathiel/Aerathiel_Deaths_March_jutsu_v1.webp` |
| Aerathiel | Decaying Touch | a glowing open handprint with particles | `art/jutsu_icons/aerathiel/Aerathiel_Decaying_Touch_jutsu_v1.webp` |
| Aerathiel | Particle Cannon | a triangular aperture firing a beam | `art/jutsu_icons/aerathiel/Aerathiel_Particle_Cannon_jutsu_v1.webp` |
| Aerathiel | Windshear Decay | a spiralling shear wind | `art/jutsu_icons/aerathiel/Aerathiel_Windshear_Decay_jutsu_v1.webp` |

What they add to the standard:

- All three are technique-first with no figure, like BBE and BEE: one bold element shape on a dark
  ground.
- **Vaporia** shows a two-colour element pairing (water with an ember accent) that still reads at
  small sizes. **Aerathiel** is the best cyan energy and wind rendering. **Bakuhatsu** is the best
  pure fire and explosion rendering: molten orange and gold sparks, cracked ground, flying debris.
- **Aerathiel's Decaying Touch** (an open handprint) is a family-specific approval, not general
  approval for hands.
- Every listed silhouette is **reserved by its family**: use these for rendering, material and
  palette handling only, never as a composition to copy.

## References (pass actual bytes, individually)

- Each session attaches **one** approved exemplar as **style/material only**, chosen for the theme:

  | Theme | Exemplar | Why |
  |---|---|---|
  | Poison, shadow / spirit | BEE `icon_bee_hemocure_v1.webp` | best dark-ground focal contrast and rim light |
  | Plain chakra | Aerathiel Windshear Decay or Particle Cannon | cyan energy rendering |
  | Fire | Vaporia Scorch Break, or Bakuhatsu Kinetic Nova | ember material on a dark ground; Kinetic Nova for bursts and explosions |
  | Water | Vaporia Surfing Strike | water and foam rendering |
  | Wind | Aerathiel Windshear Decay | moving air and debris |

  Use the pinned files listed above. Never attach the old live Bakuhatsu icons. Searing Might keeps
  Scorch Break, because Bakuhatsu's only shield (Blast Shield) is the shape it must avoid.
- **Do not attach the current starter icons.** `style_refs.py select` normally pairs the legacy
  identity icon with one exemplar, but these legacy icons are actor scenes and would pull the
  generator back to a ninja figure. Identity is carried by the target lock text instead.

## Phase 1: Academy Student jutsu (6)

| # | Jutsu | Id | What it does (live) | Theme | Reserved silhouette and action | Delivery filename |
|---|---|---|---|---|---|---|
| 1 | Poisonous Senbon | `H9XLJiU1YEro03QJ2mH8q` | 60 AP single-target damage | Poison | a tight volley of **three thin senbon needles** in flight on a rising diagonal, each trailing a venom drip | `icon-starter-poisonous-senbon.webp` |
| 2 | Replacement Technique | `clh4d6pok0002tb0hx1bxro6l` | 20 AP move to an empty tile | Plain chakra | a **dissolving chakra afterimage outline** bursting into smoke, with a sharp displacement streak leaving it | `icon-starter-replacement-technique.webp` |
| 3 | Searing Might | `clh4d6q1j0008tb0hzthddb6m` | 40 AP self buff: less damage taken | Fire | a **convex shield of interlocking ember-hot chakra plates**, front-on, heat shimmer at the rim | `icon-starter-searing-might.webp` |
| 4 | Sonic Slash | `clh4d6pxd0006tb0h4y1yudi5` | 60 AP single-target damage | Plain chakra | **one razor-thin crescent cut** crossing the frame, with **concentric shock rings** bursting from its leading edge | `icon-starter-sonic-slash.webp` |
| 5 | Soul Shackles | `clh4d6psu0004tb0hsa5cshh6` | 60 AP damage in a straight line | Shadow / spirit | **spectral chains shooting forward in a straight line** from near to far, snaring a torn wisp of soul flame | `icon-starter-soul-shackles.webp` |
| 6 | Venomous Phobia | `9oirFnLa0wejelNYpewq6` | 40 AP debuff: target takes more damage | Poison | a **coiling cloud of venom miasma** forming a looming, fanged dread-mask shape that closes in | `icon-starter-venomous-phobia.webp` |

**Delivered:** 3 Searing Might, 2026-10-21, to its reserved silhouette (push/149). 2 Replacement Technique, 2026-10-21, approved as an **exception** (RUL-2026-10-21-001): a log in swirling smoke with two chakra arrows instead of the afterimage silhouette below. Files in `art/jutsu_icons/starter/`; sent for review as push/148. The exception does not carry over: the remaining icons keep their reserved silhouettes and the no-log, no-symbol rules, and none may use smoke (still owned by icon 2).

**Style anchor per Phase 1 icon:** Hemocure for 1, 5 and 6; Aerathiel Windshear Decay for 2;
Vaporia Scorch Break for 3; Aerathiel Particle Cannon for 4.

**Distinction ledger (pass the other five as text exclusions in each brief):**

- 1 owns *needles*; 6 owns *a looming miasma mask*. Both are poison-green, so neither may borrow the
  other's shape: no needles in 6, no fog face in 1.
- 2 owns *afterimage plus smoke*; no smoke in any other icon.
- 3 owns *a shield*; no shield or armour anywhere else. It must also not look like Bakuhatsu's Blast
  Shield (a circular fire barrier) or Vaporia's Liquid Ember Shell (a sphere): plates, front-on, not a dome or orb.
- 4 owns *a crescent cut with shock rings*; no other icon uses an arc slash or rings. Not Aerathiel's
  Particle Cannon triangle or beam.
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
References attached: <the one exemplar named for this jutsu> (style/material only: rendering,
contrast, rim light; not its composition or reserved silhouette)
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
