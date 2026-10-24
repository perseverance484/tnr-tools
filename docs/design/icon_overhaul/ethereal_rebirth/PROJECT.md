# Ethereal Rebirth: premium upgrade of the original

- **Director, 2026-10-24 (RUL-2026-10-24-003):** "We keep the people but make it read well as an icon at thumbnail size.
  Give each a clear silhouette and color palette based on the original. This way players get to see their favorite skills
  with a premium upgrade AND our icons read well at size. Let's prepare ethereal rebirth next."
- **Session prompt:** `docs/handoffs/ETHEREAL_REBIRTH_SESSION_PROMPT.md`.
- **Roles:** the art director makes the raws; Claude Code does everything after (RUL-2026-10-23-008 amendment 1).
  Every decision on the art is the director's.
- **Live-game requests/writes:** 0.

## 1. The jutsu

| | |
|---|---|
| Id | `K0t6Z-Q4lau1jFt8Tkpot` |
| Live data | FORBIDDEN, S rank, 60 AP; one opponent at range 4; damage; the user absorbs damage and the target deals less |
| Battle text (live) | "%user cracks open the seal upon their own soul, and the elements burn through them in a roar of green flame that erupts outward to strike %target. In the fire's wake %user's body begins to unmake and remake itself, turning every wound..." |

The live text mentions green flame; the original art (which players prefer) shows fire, water and lightning swirling
around the user. **Premium text is drafted in `../TEXT_AND_ICON_ROUND1.md` section 2, and the icon draws its battle line's
moment** (RUL-2026-10-24-004).

## 2. The original, and why it fails at size

`art/jutsu_icons/ethereal_rebirth/refs/ref_er_original.webp` (live now). Reference sheet at real size: `refs_gate.png`.

| Keep (the identity players like) | Fix (why it blurs at 45 px) |
|---|---|
| a white-haired warrior in deep blue armour with a crimson scarf, mid-air, arms spread | the figure fills about a third of the tile; the stone bridge, cliffs, tree, houses and sunset take the rest |
| a gold-white core blazing at the chest (the soul's seal breaking open) | the environment is as detailed and as contrasty as the figure, so the 45 px silhouette is a smudge |
| ribbons of cyan water-light and orange fire spinning around the body, small seal rings at the hands | the energy ribbons are thin; at 45 px they turn to specks |
| the palette: navy, cyan, crimson, orange, gold, white | the moss-green ground and sunset add two more hue families |

Measured palette of the original (figure area): navy `#00336a` (dominant), cyan `#1891c8` and `#7ff8ff`, crimson
`#870e2d` (scarf), fire orange `#ec5f36`, core gold `#ffe04f`, hair white `#feffff` to grey `#a8a7ac`. The moss green
`#53753c` is environment and goes.

Our reverted version (a pillar of green flame) scored 0/10 and is never attached or imitated.

## 3. The upgrade

**Same character, same moment, same colours, rebuilt as an icon.**

1. **Crop in:** the warrior fills 65–75% of the tile height (knees or full body), centred slightly high.
2. **One silhouette:** streaming white hair and the crimson scarf flying to one side, arms flung wide, the body slightly
   turned. It must read as "a warrior bursting with power" as a flat shape at 32 px.
3. **The energy carries the shape:** two or three **thick** spinning ribbons (cyan water-light and orange fire) circling
   the body in one clear, tilted loop, wide enough to survive at 45 px; the gold-white core at the chest is the single
   brightest point and the only glow source.
4. **Background:** no bridge, tree or buildings. A dark dusk navy, flat or two-tone, with at most a faint warm glow
   behind the figure (an echo of the original's sunset).
5. **Values:** dark background; the figure in mid and dark navy with a crisp rim light from the top-left; the ribbons
   bright; the core brightest. Hair and scarf give the head a clear read.
6. **Rendering:** premium TNR pixel art: retro 32-bit, hard pixel edges, about 48–64 art pixels across, 16–24 colours
   after `pixelsnap.py`, no gradients or blur, mature proportions, a dynamic, slightly foreshortened pose (the game's own
   art guide).
7. **Safe area:** head, core and arms in the upper and central 60–70%; the bottom corners (badges) hold only ribbon tails
   or darkness.
8. **Distinct from** Crystal Sphere (a figure inside a closed crystal dome) and Ethereal Nexus (the other Forbidden jutsu):
   here the energy is open, spinning ribbons, and the figure rises.

## 4. Acceptance criteria

| # | Criterion | Check |
|---|---|---|
| A1 | At 45 px a viewer says "a warrior powering up" or "a fighter surrounded by elemental energy" | name test (G1) |
| A2 | The blurred 45 px silhouette is a clear figure inside a loop of light | silhouette (G2) |
| A3 | Recognisably the same character and moment as the original: hair, scarf, armour, core, the spinning elements | director, side by side |
| A4 | Palette within the original's (navy, cyan, crimson, orange, gold, white); no green | director |
| A5 | Background calm and dark; nothing in it competes with the figure | silhouette, bar test (G4) |
| A6 | Premium pixel art on one grid, 16–24 colours | pixel integrity (G6) |
| A7 | Head, core and arms clear of the badge corners | 112 px tile (G5) |

## 5. Log

| Round | Date | What happened |
|---|---|---|
| 0 | 2026-10-24 | Project opened; original measured at real size (`refs_gate.png`); round-1 prompt written. |
| 0 | 2026-10-24 | Premium text drafted; round-1 prompt tied to the battle line's moment (arms wide, seal cracking, ribbons). |
| 1 | 2026-10-24 | Texts approved by the director; round-1 art session started by the director. Waiting for raws. |
