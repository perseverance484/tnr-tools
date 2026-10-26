# Ethereal Rebirth: art session prompt (round 2)

- **Project:** `docs/design/icon_overhaul/ethereal_rebirth/PROJECT.md`; round-1 review `ROUND1_REVIEW.md`; text and
  icon mapping `TEXT_V2.md` (non-elemental, draft).
- **Base:** round 1's r1b (`art/jutsu_icons/ethereal_rebirth/candidates/round1/raw_ethereal_rebirth_r1b.png`): the gold and
  blue soul-light direction. **No elements** (director, 2026-10-24: "this is a non-elemental attack so using elements is a
  no-go"): no fire, no water, no lightning.
- **How to use:** paste section 1 into the art-director session. It runs each brief in section 2 in its own isolated
  generation session and returns the raws only. Claude Code does everything after (no pixel conversion,
  RUL-2026-10-24-005).
- **Live-game requests/writes:** 0. Credentials: none.

## 1. Session prompt (paste into the art-director session)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session makes round 2 of the
Ethereal Rebirth jutsu icon. Read docs/design/icon_overhaul/ethereal_rebirth/ROUND1_REVIEW.md and TEXT_V2.md first.

Start from round 1's r1b (attach as the SUBJECT reference):
art/jutsu_icons/ethereal_rebirth/candidates/round1/raw_ethereal_rebirth_r1b.png
Keep: the white-haired warrior, gold eyes, crimson scarf and sash, the seal rings at the open hands, the arms-wide mid-air
pose, and above all the chest core: a white-gold burst with cracks of light spreading across the armour. Keep the
ribbons as pale gold and blue-white SOUL-LIGHT.

This is a NON-ELEMENTAL technique. No fire, no water, no lightning, no flames, no droplets, no electric bolts. The energy
is the user's own soul-light.

The moment to draw (the jutsu's battle text): "%user throws their arms wide and the seal upon their soul cracks open, a
golden core blazing to life at their chest. Ribbons of pale soul-light pour out of them and spin around their body before
one lashes out to strike %target. Within that whirling light %user's body unmakes and remakes itself."

Fix what failed in round 1 (both candidates), so it reads at 45 px on a phone:
1. The body disappears: change the armour from near-black to the original icon's deep NAVY BLUE (#00336a family) with a
   crisp rim light from the top-left, so the figure separates from the dark background.
2. The ribbons hide the body: the ribbons spin mostly BEHIND the torso and arms; where one crosses in front (at the legs),
   it turns see-through so the body shows through it.
3. The loop is closed: break it. One ribbon breaks away from the spin and whips out past the frame edge, towards the
   unseen enemy (the "lashes out to strike" in the text). The rest of the spin stays open, not a full oval.
4. The head is small: crop to knees-up so the head, core and arms are larger (head about 12-15% of the tile height).
5. The ribbons are too pale at phone size: make two or three ribbons thicker and brighter (warm gold and cool blue-white),
   while keeping them luminous and ethereal. The chest core stays the single brightest point.
6. "Unmakes and remakes itself": a few flecks of light peel from the warrior's edges and drift into the ribbons.

Unchanged rules: dark dusk-navy background, flat or two-tone, no scenery; palette navy, crimson, white hair, warm gold,
blue-white (no green, no orange flame); premium TNR pixel art as drawn (retro 32-bit, hard pixel edges, no gradients or
blur, no painterly brushwork); head, core and arms in the upper and central 60-70%, bottom corners only ribbon tails or
darkness; nothing touching the edges except the one ribbon that whips out of frame; square, opaque, full-bleed; no text,
runes or symbols; one figure; no franchise look; no broken anatomy.

Run the three briefs in docs/handoffs/ETHEREAL_REBIRTH_ROUND2_SESSION_PROMPT.md section 2, ONE per isolated generation
session, one square candidate each. Return the raw images only, named by brief id, e.g. raw_ethereal_rebirth_R2-1.png.
Fail fast: regenerate a brief once if there is any fire, water or lightning, if the armour is near-black, if the ribbons
cover the torso, if the spin closes into a full oval, or if the anatomy is broken.
~~~

## 2. Isolated generation briefs (one per session)

Shared header for every brief:

~~~text
Repository: perseverance484/tnr-tools
Workstream: icon overhaul, Ethereal Rebirth round 2 (docs/design/icon_overhaul/ethereal_rebirth/ROUND1_REVIEW.md)
Target: Ethereal Rebirth
Jutsu target lock: jutsu ID K0t6Z-Q4lau1jFt8Tkpot, display name Ethereal Rebirth; forbidden jutsu, NON-ELEMENTAL
Session: ISOLATED GENERATION, one asset only; exploratory until the director approves
Live-game requests/writes: 0. Credentials: none.
Reference: raw_ethereal_rebirth_r1b.png (SUBJECT: the character, pose, chest core and soul-light ribbons)
Subject (the battle line's moment): the white-haired warrior, arms flung wide, the seal on their soul cracking open as a
white-gold core with cracks of light across navy-blue armour; thick ribbons of pale gold and blue-white soul-light spinning
mostly behind the body, see-through where they cross the legs; one ribbon whipping out of frame; flecks of light peeling
from the body into the ribbons
Rendering lock: premium TNR pixel art as drawn, retro 32-bit, hard pixel edges, no gradients or blur, rim light top-left,
one glow source (the chest core); square, opaque, full-bleed
Palette lock: deep navy armour (#00336a family), crimson scarf and sash, white hair, gold eyes, warm gold and blue-white
light, dark dusk-navy background; no fire, water, lightning, green or orange flame
Composition: knees-up, figure filling the frame, head 12-15% of the height; an open spin, one ribbon out of frame; bottom
corners only ribbon tails or darkness
Negatives: no elements of any kind; no near-black armour; no ribbons over the torso; no closed oval; no scenery; no text,
runes or symbols; no extra figures; no franchise look; no frame or UI; no broken anatomy
Generate exactly ONE square icon candidate. No collage. Do not process or upload it.
~~~

| Brief | Framing (add to the header) |
|---|---|
| **R2-1 Direct fix** | r1b's composition with the six fixes applied: a three-quarter view, arms wide, the spin wheeling behind the body, the breakaway ribbon whipping out to the upper right. |
| **R2-2 Backlit** | The same moment with the figure in a dark navy silhouette edged by a strong gold rim light, the soul-light and the core blazing against it. The strongest contrast at 45 px. |
| **R2-3 Rising helix** | Seen from slightly below: the ribbons spiralling upward behind the body like a rising helix, open at the top where one ribbon breaks away and whips out of frame. The most upward, "rebirth" feeling. |

## 3. Intake (Claude Code)

1. Save raws to `art/jutsu_icons/ethereal_rebirth/candidates/round2/` as delivered.
2. No pixel conversion (RUL-2026-10-24-005): resize to 256 px for review.
3. Build the round sheet with `docs/design/icon_overhaul/gate_sheet.py` (the original and r1b as reference rows) and send it
   to the director with notes against `PROJECT.md` section 4 and `TEXT_V2.md`; log the round in `PROJECT.md`.
