# Tempest Cleave pilot: art session prompt (round 1, v2)

- **Project:** `docs/design/icon_overhaul/tempest_cleave/PILOT.md`.
- **v2 (2026-10-24):** rewritten for RUL-2026-10-24-003 (upgrade the original, keep the people, palette from the original)
  and RUL-2026-10-24-004 (the icon shows the battle line). v1, a whirlwind without a figure, is in git history and is
  not to be run.
- **The moment (draft battle line, `docs/design/icon_overhaul/TEXT_AND_ICON_ROUND1.md` section 1):** "%user plants their
  feet and turns once, and the storm answers: the sky wheels into a great vortex above them as the wind around them hardens
  into a spinning wall of razor air, lightning crackling through its arms. The tempest bursts outward in a howling ring..."
- **How to use:** paste section 1 into a new art-director session. It runs each brief in section 2 in its own isolated
  generation session (`docs/workflows/ISOLATED_ART_GENERATION.md`) and returns the raws only. Claude Code does everything
  after.
- **Live-game requests/writes:** 0. Credentials: none.

## 1. Session prompt (paste into the art-director session)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes round 1 of ONE
jutsu icon, the pilot of the icon overhaul: Tempest Cleave. Read docs/design/icon_overhaul/tempest_cleave/PILOT.md and
docs/design/icon_overhaul/TEXT_AND_ICON_ROUND1.md section 1 first.

The direction: a premium upgrade of the ORIGINAL icon that shows the jutsu's battle text in action, rebuilt so it reads
as an icon at thumbnail size (45 px on a phone).

The moment to draw (from the battle text): "%user plants their feet and turns once, and the storm answers: the sky wheels
into a great vortex above them as the wind around them hardens into a spinning wall of razor air, lightning crackling
through its arms. The tempest bursts outward in a howling ring and carves through everything within its reach."

References (attach both, with these roles):
1. art/jutsu_icons/tempest_cleave/refs/ref_tc_live_original.webp - SUBJECT: the character and palette. A fox-masked
   fighter (white fox mask with red markings, glowing cyan eyes), dark segmented armour, a white scarf, cyan lightning
   crackling from the hands, a storm vortex wheeling in the sky. Use the character, NOT its scene (no torii, no burning
   village, no cliff).
2. art/jutsu_icons/tempest_cleave/refs/ref_tc_older_version_crop.png - ELEMENT: the whirlwind. A blue-white spiral with
   ink-dark streaks on its outer arms, forked lightning and small traditional cloud curls; one long sweeping arm; an
   off-centre eye. Players liked it.

Put them together: the masked fighter at the eye of the whirlwind, braced low and twisted mid-turn, scarf and coat
whipped around by the spin; the spiral wheeling around and behind them with its eye at the fighter's head; the arms of the
spiral drawn as thick ribbons of wind with sharp white razor edges; forked cyan lightning running along the arms and
sparking from the hands; the outer arms bursting outward past the fighter towards the frame edges.

Visual design (non-negotiable):
- Reads at 45 px as "a masked ninja in a whirlwind". The fighter fills 55-70% of the tile height, centred slightly high;
  the fighter is dark against the bright wind (backlit), with a crisp rim light from the top-left; mask and scarf are the
  lightest points of the figure.
- One silhouette: the figure's twisted, braced pose inside one asymmetric spiral. Thick wind ribbons (three to five), not
  thin streaks; no texture filling the frame.
- Not a shuriken: no rigid radial blades, no rotational symmetry, no metal blades.
- Palette from the original: storm slate #554c5a and near-black for the ground and armour; electric cyan #62f8fc and
  sea-cyan #4fc7b1 for lightning and the eyes; blue #2382d9 to blue-white and white for the wind and its razor edges; white
  mask and scarf with small red mask markings. No orange fire, no green. The brightest values: the wind's razor edges and
  the lightning.
- Background: the storm sky only, dark, simple; no buildings, gates, cliffs or fire.
- Premium TNR pixel art: retro 32-bit, hard pixel edges, about 48-64 art pixels across, clean clusters, no gradients, no
  blur, no painterly brushwork, mature proportions, dynamic foreshortened pose.
- Head, mask and hands in the upper and central 60-70%; the bottom-left and bottom-right corners hold only wind tails or
  darkness (badges cover them); nothing touches the edges. Square, opaque, full-bleed.
- No text, kanji or runes; no franchise look (no Rasengan or Rasenshuriken, no anime ANBU insignia); one figure only; no
  frame or UI.

Never attach or imitate our previous version (a ring of steel blades with orange edges): players read it as a shuriken.

Run the four briefs in docs/handoffs/TEMPEST_CLEAVE_PILOT_SESSION_PROMPT.md section 2, ONE per isolated generation
session, one square candidate each. Return the raw images only, named by brief id, e.g. raw_tempest_cleave_TC-1.png.
Do not process, crop, upscale or upload anything. Fail fast: regenerate a brief once if the figure is small, the wind is
thin wisps, it reads as a shuriken at thumbnail size, there is scenery, or the anatomy is broken.
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
References: ref_tc_live_original.webp (SUBJECT: the fox-masked fighter and palette, not the scene);
ref_tc_older_version_crop.png (ELEMENT: the whirlwind's spiral, ink streaks, lightning, cloud curls)
Subject (the battle line's moment): the fox-masked fighter planted at the eye of a whirlwind, turning once; thick ribbons
of razor wind with white edges spinning around and behind them, forked cyan lightning along the arms and sparking from the
hands, the outer arms bursting outward towards the frame edges
Rendering lock: premium TNR pixel art, retro 32-bit, hard pixel edges, about 48-64 art pixels across, no gradients or
blur, rim light top-left, backlit figure; square, opaque, full-bleed
Palette lock: storm slate #554c5a, near-black, cyan #62f8fc / #4fc7b1, blue #2382d9 to white; white mask and scarf, small
red markings; no orange fire, no green
Composition: figure 55-70% of tile height, centred slightly high, inside one asymmetric spiral; bottom corners only wind
tails or darkness; nothing touching the edges
Negatives: no torii, buildings, cliff or fire; no shuriken or radial blades; no text or symbols; no extra figures; no
franchise look; no frame or UI; no broken anatomy
Generate exactly ONE square icon candidate. No collage. Do not process or upload it.
~~~

| Brief | Framing (add to the header) |
|---|---|
| **TC-1 Faithful** | The original's stance and three-quarter view, cropped in to knees-up, now at the centre of the whirlwind: one arm thrown out trailing lightning, the other drawn back, the spiral's long arm sweeping across the lower left. Closest to the original. |
| **TC-2 Mid-turn** | Full figure, low camera, caught halfway through the turn: back half-turned to the viewer, mask looking over the shoulder, scarf whipping in a long arc that becomes one of the wind ribbons. The most dynamic silhouette. |
| **TC-3 Eye of the storm** | Seen from slightly above: the fighter small-but-clear at the centre (55% height), the whirlwind's full spiral wheeling around them with the older version's ink streaks and cloud curls on the outer arms. The most faithful to the older whirlwind. |
| **TC-4 Burst** | Knees-up, the instant the ring bursts outward: arms flung wide, the wind ribbons exploding outward in an asymmetric burst, lightning forking from both hands, the fighter dark against the brightest wind. The strongest contrast. |

## 3. Intake (Claude Code)

1. Save raws to `art/jutsu_icons/tempest_cleave/candidates/round1/` as delivered.
2. No pixel conversion (RUL-2026-10-24-005): resize each raw to 256 px for review; the approved one is exported as
   lossless WebP and checked with `artpreflight.py --type JUTSU_ICON`.
3. Build the round sheet with `docs/design/icon_overhaul/gate_sheet.py` (the original and the older version as reference
   rows) and send it to the director with notes against `PILOT.md`'s acceptance criteria; log the round there.
