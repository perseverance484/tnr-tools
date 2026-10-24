# Tempest Cleave pilot: art session prompt (round 1)

- **Project:** `docs/design/icon_overhaul/tempest_cleave/PILOT.md` (read it first: the jutsu, the older version to beat,
  acceptance criteria A1–A8, the process).
- **How to use:** paste section 1 into a new art-director session. That session runs each brief in section 2 in its own
  isolated generation session (`docs/workflows/ISOLATED_ART_GENERATION.md`), one candidate per session, and returns the
  raws only. Claude Code does everything after (pixel snapping, gate sheets, previews).
- **Live-game requests/writes:** 0. Credentials: none.

## 1. Session prompt (paste into the art-director session)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes round 1 of ONE
icon, the pilot of the jutsu icon overhaul: Tempest Cleave. The director wants it worked until it is the best, most
fitting premium pixel-art icon we can make. Read docs/design/icon_overhaul/tempest_cleave/PILOT.md first.

What the jutsu does: an A-rank event jutsu. The user turns once and the air becomes a blade: a storm of razor wind erupts
outward in a howling ring and cuts everyone near them, friend and foe; the cuts keep "singing with the wind" afterwards.
The icon must say: a spinning storm of razor wind, dangerous to everything near it.

The target to beat (attach as the SUBJECT reference where a brief says so):
art/jutsu_icons/tempest_cleave/refs/ref_tc_older_version_crop.png - an older version players liked. A blue-white
whirlwind spiralling into an off-centre eye, dark ink-like streaks on its outer arms, thin forked lightning, small
traditional cloud curls along the lower right. Keep its spirit: flowing wind arms (not rigid blades), storm, lightning,
cloud curls, an asymmetric spiral with one long sweeping arm. Improve: premium pixel rendering, strong value contrast
(dark storm ground, white cutting edges), menace.

Never attach or imitate our previous version (a ring of steel blades with orange edges): players read it as a shuriken.

Visual design (non-negotiable):
- Reads at 45 px on a phone as a whirlwind or wind storm. One silhouette: an asymmetric spiral, a clear eye, one dominant
  sweeping arm. Two to four big shapes; no texture filling the frame.
- Not a shuriken: no rigid radial blades, no points in rotational symmetry, no metal, no perfect symmetry.
- Value plan: a dark storm-navy to charcoal background (flat or two-tone, no scenery; brief TC-1 alone keeps the older
  version's slate-blue ground); the wind arms mid blue-grey; the
  brightest values are the razor edges of the arms and the eye. One glow source: the eye. Palette: storm navy, slate,
  blue-white, white, pale electric cyan for the lightning. No red, no orange, no teal, no green.
- Rim light from the top-left. Premium TNR pixel art: retro 32-bit, hard pixel edges, no gradients, no blur, no painterly
  brushwork, no photorealism; about 48-64 art pixels across, clean clusters, little or no dithering.
- The eye and the main arm sit in the upper and central 60-70% of the frame; the bottom-left and bottom-right corners stay
  low-detail (badges cover them); nothing touches the edges. Square, opaque, full-bleed.
- No text, kanji, runes or symbols; no figure; no franchise imagery (no Rasengan or Rasenshuriken look); no frame or UI.

Run the six briefs in docs/handoffs/TEMPEST_CLEAVE_PILOT_SESSION_PROMPT.md section 2, ONE per isolated generation
session, one square candidate each. Return the raw images only, named by brief id, e.g. raw_tempest_cleave_TC-1.png.
Do not process, crop, upscale, key or upload anything. Fail fast before returning: regenerate a brief once if the raw reads
as a shuriken, saw blade or portal at thumbnail size, is symmetric, uses red/orange/teal, or has a busy background.
~~~

## 2. Isolated generation briefs (one per session)

Shared header for every brief:

~~~text
Repository: perseverance484/tnr-tools
Workstream: icon overhaul pilot, Tempest Cleave (docs/design/icon_overhaul/tempest_cleave/PILOT.md)
Target: Tempest Cleave
Jutsu target lock: jutsu ID Ul83iTziN__Z0i_UOzZTK, display name Tempest Cleave; event jutsu, no bloodline
Session: ISOLATED GENERATION, one asset only; exploratory until the director approves
Live-game requests/writes: 0. Credentials: none.
Goal: an abstract emblem of a spinning storm of razor wind that cuts everything around it
Rendering lock: premium TNR pixel art, retro 32-bit, hard pixel edges, about 48-64 art pixels across, no gradients or
blur, rim light top-left, one glow source (the eye); square, opaque, full-bleed
Palette lock: storm navy and charcoal ground; slate and blue-grey wind; blue-white and white razor edges; pale electric
cyan lightning; nothing red, orange, teal or green
Composition: one asymmetric spiral, off-centre eye in the upper-central area, one dominant sweeping arm; bottom corners
low-detail; nothing touching the edges
Negatives: no shuriken, saw or rigid radial blades; no rotational symmetry; no metal; no figure; no text, runes or
symbols; no Rasengan/Rasenshuriken look; no scenery; no frame or UI
Generate exactly ONE square icon candidate. No collage. Do not process or upload it.
~~~

| Brief | Reference (role) | Direction (add to the header) |
|---|---|---|
| **TC-1 Faithful upgrade** | `ref_tc_older_version_crop.png` (SUBJECT: composition and motifs) | The older version, same layout and motifs, rebuilt as premium pixel art: the blue-white spiral into an off-centre eye, ink-dark streaks on the outer arms, thin forked lightning, the small cloud curls at lower right. **Keep the older version's slate-blue storm ground** (the one exception to the dark-ground lock: it makes the icon stand out in a bar of black-ground icons); push the arms' dark ink streaks and white edges harder so the spiral still pops. |
| **TC-2 Razor arms** | older version (SUBJECT: spirit only) | The spiral built from four or five long, tapering ribbons of wind, each with a thin white razor edge on its leading side, like blades of air, not metal. One arm much longer, sweeping out to the lower left. Seen from directly above, like a cyclone on a weather map. |
| **TC-3 Storm wall** | older version (SUBJECT: spirit only) | A three-quarter view: a towering funnel of storm wind, its dark eye at upper centre, razor-edged ribbons spiralling out around it, two forked lightning bolts crackling inside the wall. Tall oval silhouette, heavy and menacing. |
| **TC-4 Ink storm** | older version (SUBJECT: style of its ink streaks) | Lean into the older version's ink look: bold, dark, brush-like streaks of wind (drawn as hard-edged pixel clusters, not soft brushwork) spiralling around a white-hot eye, with blue-white edges and sparse lightning. The most dramatic contrast of the six. |
| **TC-5 Cloud curls** | older version (SUBJECT: the cloud curls) | The whirlwind framed by bold traditional cloud curls: one curl cluster at upper left, one at lower right, pulled into the spiral as it turns. The curls give the silhouette a unique, Japanese shape; the spiral arms stay razor-edged. |
| **TC-6 Lightning eye** | older version (SUBJECT: spirit only) | A crackling knot of electric cyan lightning in the eye, the wind arms whipping out from it in a fast, tight spiral with long trailing tails. The lightning is the single glow source; wind stays the dominant shape. |

## 3. Intake (Claude Code)

1. Save raws to `art/jutsu_icons/tempest_cleave/candidates/round1/` as delivered.
2. Run each through `skills/producing-tnr-art/scripts/pixelsnap.py` (on `fable/pixel-art-snap` until it merges) and
   build the round-1 gate sheet: each candidate raw and snapped, at 45 px with its blurred grey silhouette, in a mobile bar
   beside kept icons, as a 112 px tile with badge, at 32 px, beside the older version and the live icon.
3. Send the sheet to the director with notes against acceptance criteria A1–A8; log the round in `PILOT.md` section 5.
