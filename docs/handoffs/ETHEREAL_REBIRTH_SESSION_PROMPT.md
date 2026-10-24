# Ethereal Rebirth: art session prompt (round 1)

- **Project:** `docs/design/icon_overhaul/ethereal_rebirth/PROJECT.md` (the original, why it blurs at size, the upgrade,
  acceptance criteria). Direction: RUL-2026-10-24-003 (keep the people; clear silhouette; palette from the original).
- **How to use:** paste section 1 into a new art-director session. It runs each brief in section 2 in its own isolated
  generation session (`docs/workflows/ISOLATED_ART_GENERATION.md`) and returns the raws only. Claude Code does everything
  after.
- **The icon shows the battle line (RUL-2026-10-24-004).** Draft text and the text-to-icon mapping:
  `docs/design/icon_overhaul/TEXT_AND_ICON_ROUND1.md` section 2. The moment: "%user throws their arms wide and the seal upon
  their soul cracks open, a golden core blazing to life at their chest. Fire, water and lightning pour out of them in
  spinning ribbons that lash across the battlefield..."
- **Live-game requests/writes:** 0. Credentials: none.

## 1. Session prompt (paste into the art-director session)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes round 1 of ONE
jutsu icon: Ethereal Rebirth. Read docs/design/icon_overhaul/ethereal_rebirth/PROJECT.md first.

The direction: a premium upgrade of the ORIGINAL icon. Same character, same moment, same colours, rebuilt so it reads
as an icon at thumbnail size (45 px on a phone). Players love the original; it fails only because the figure is small
and the scenery around it is as busy as the figure.

The original (attach as the SUBJECT reference): art/jutsu_icons/ethereal_rebirth/refs/ref_er_original.webp
A white-haired warrior in deep blue armour with a crimson scarf, mid-air above a stone bridge, arms spread, a gold-white
core blazing at the chest, ribbons of cyan water-light and orange fire spinning around the body, small seal rings at the
hands. The jutsu: an S-rank forbidden technique; the user cracks open the seal on their own soul, the elements burn
through them, and their body remakes itself.

The icon must show this exact moment from the jutsu's battle text: "%user throws their arms wide and the seal upon their
soul cracks open, a golden core blazing to life at their chest. Fire, water and lightning pour out of them in spinning
ribbons that lash across the battlefield." So: arms flung wide; the gold-white core at the chest with thin cracks of light
spreading across the armour; thick ribbons of orange fire and cyan water-light with forked lightning along them; one
ribbon whipping out past the frame edge towards an unseen enemy; flecks of light peeling from the body's edges into the
ribbons (the body remaking itself).

Keep: the character (white hair, crimson scarf, blue armour), the chest core, the spinning cyan and orange elements, the
mid-air power-up moment, the palette (navy #00336a, cyan #1891c8 to #7ff8ff, crimson #870e2d, fire orange #ec5f36, core
gold #ffe04f, white hair).

Change, so it reads at 45 px:
- Crop in: the warrior fills 65-75% of the tile height, centred slightly high.
- One clear silhouette: white hair and crimson scarf streaming to one side, arms flung wide, body slightly turned; it must
  read as a flat shape at 32 px.
- Two or three THICK spinning ribbons (cyan water-light, orange fire) in one clear tilted loop around the body, wide
  enough to survive at 45 px. The gold-white chest core is the brightest point and the only glow.
- Remove the bridge, tree, cliffs, buildings and sunset. Background: dark dusk navy, flat or two-tone, at most a faint
  warm glow behind the figure.
- Values: dark background; figure in mid and dark navy with a crisp rim light from the top-left; ribbons bright; core
  brightest. No green anywhere.
- Premium TNR pixel art: retro 32-bit, hard pixel edges, about 48-64 art pixels across, clean clusters, no gradients,
  no blur, no painterly brushwork, mature proportions, a dynamic, slightly foreshortened pose.
- Head, core and arms in the upper and central 60-70%; bottom-left and bottom-right corners hold only ribbon tails or
  darkness (badges cover them); nothing touches the edges. Square, opaque, full-bleed.
- No text, kanji, runes or readable symbols; no franchise look; no frame or UI; one figure only.

Never attach or imitate our previous version (a pillar of green flame from broken stone): it scored 0/10.

Run the four briefs in docs/handoffs/ETHEREAL_REBIRTH_SESSION_PROMPT.md section 2, ONE per isolated generation session,
one square candidate each. Return the raw images only, named by brief id, e.g. raw_ethereal_rebirth_ER-1.png. Do not
process, crop, upscale or upload anything. Fail fast: regenerate a brief once if the figure is small, the background has
scenery, the ribbons are thin wisps, there is green, or the anatomy is broken (hands, extra limbs).
~~~

## 2. Isolated generation briefs (one per session)

Shared header for every brief:

~~~text
Repository: perseverance484/tnr-tools
Workstream: icon overhaul, Ethereal Rebirth (docs/design/icon_overhaul/ethereal_rebirth/PROJECT.md)
Target: Ethereal Rebirth
Jutsu target lock: jutsu ID K0t6Z-Q4lau1jFt8Tkpot, display name Ethereal Rebirth; forbidden jutsu, no bloodline
Session: ISOLATED GENERATION, one asset only; exploratory until the director approves
Live-game requests/writes: 0. Credentials: none.
Reference: ref_er_original.webp (SUBJECT: character, costume, pose energy, elements, palette; NOT its scenery or framing)
Subject (the battle line's moment): the white-haired warrior in deep blue armour and crimson scarf, mid-air, arms flung
wide, the soul's seal cracking open as a gold-white core at the chest with thin cracks of light across the armour; thick
ribbons of orange fire and cyan water-light, forked lightning along them, spinning around the body, one ribbon whipping
out past the frame edge; flecks of light peeling from the body into the ribbons
Rendering lock: premium TNR pixel art, retro 32-bit, hard pixel edges, about 48-64 art pixels across, no gradients or
blur, rim light top-left, one glow source (the chest core); square, opaque, full-bleed
Palette lock: navy #00336a, cyan #1891c8 to #7ff8ff, crimson #870e2d, orange #ec5f36, gold #ffe04f, white; dark dusk-navy
background; no green
Composition: figure 65-75% of tile height, centred slightly high; one tilted loop of thick ribbons; bottom corners only
ribbon tails or darkness; nothing touching the edges
Negatives: no bridge, tree, cliffs, buildings or sunset; no text, runes or symbols; no extra figures; no franchise look;
no frame or UI; no broken anatomy
Generate exactly ONE square icon candidate. No collage. Do not process or upload it.
~~~

| Brief | Framing (add to the header) |
|---|---|
| **ER-1 Faithful** | The original's pose, cropped in to knees-up: arms spread wide, head tilted back slightly, hair and scarf streaming to the right, ribbons looping around the waist and shoulders. The closest to the original. |
| **ER-2 Rising** | Full figure rising, seen from slightly below (foreshortened): arms flung up and out, hair and scarf streaming upward, the ribbon loop spiralling up around the body like a rising helix. The most dynamic silhouette. |
| **ER-3 Core close-up** | Waist-up, larger: arms flung wide to the frame's sides, the chest core cracking open with gold-white light at the centre, cracks of light across the armour, the ribbons sweeping in a big tilted ellipse behind and in front of the figure. The most readable at 45 px. |
| **ER-4 Backlit** | Knees-up, the figure mostly in dark navy silhouette with a crisp rim light, the spinning cyan and orange ribbons and the gold core blazing against it; hair and scarf catch the light. The strongest dark-against-light contrast (the house look for figure icons). |

## 3. Intake (Claude Code)

1. Save raws to `art/jutsu_icons/ethereal_rebirth/candidates/round1/` as delivered.
2. Run each through `skills/producing-tnr-art/scripts/pixelsnap.py` (on `fable/pixel-art-snap` until it merges).
3. Build the round sheet with `docs/design/icon_overhaul/gate_sheet.py`, the original as a reference row, and send it to
   the director with notes against acceptance criteria A1–A7; log the round in `PROJECT.md` section 5.
