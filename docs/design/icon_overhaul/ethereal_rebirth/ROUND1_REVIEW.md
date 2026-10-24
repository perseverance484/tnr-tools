# Ethereal Rebirth round 1: review against the original

- **Candidate:** `art/jutsu_icons/ethereal_rebirth/candidates/round1/raw_ethereal_rebirth_r1a.png` (1254 px, sha256
  `3aec6893369f5e88…`), delivered by the director 2026-10-24.
- **Sheets:** `round1_gate.png` (original, raw and pixel-snapped at real sizes); `round1_grid_density.png` (raw vs
  pixelsnap at 64, 96 and 128 art pixels across).
- **Verdict on the art is the director's.** This is Claude Code's assessment against `PROJECT.md` section 4 and the approved
  battle line.

## Against the original

| | Original | Round 1 |
|---|---|---|
| Figure size | about a third of the tile; scenery fills the rest | fills the frame head to foot (big improvement) |
| Background | bridge, tree, cliffs, sunset, as busy as the figure | flat dark navy (fixed) |
| 45 px | a muddy smudge | bright and distinct in the bar; reads as "a figure in a swirl of fire and water" |
| Character | white hair, crimson scarf, blue armour, gold chest core | white hair, crimson scarf and sash, gold eyes, gold core; armour is **charcoal-black instead of the original's blue** |
| Elements | thin cyan and orange ribbons | thick fire and water ribbons with leaf-shaped flecks (fixed) |

## Against the approved battle line

| Beat | In the icon? |
|---|---|
| "throws their arms wide" | yes, arms wide, palms open, gold seal rings at both hands |
| "the seal upon their soul cracks open, a golden core blazing to life at their chest" | yes, and it is the best part: a white-gold burst with cracks of light spreading across the chest |
| "fire, water and lightning pour out of them in spinning ribbons" | fire and water yes; **no lightning** |
| "lash across the battlefield to strike %target" | partly: ribbons reach the frame edges, none clearly whips out of frame |
| "unmakes and remakes itself" | the flecks peeling off the ribbons suggest it |

## Acceptance criteria (PROJECT.md section 4)

| # | Criterion | Result |
|---|---|---|
| A1 | at 45 px "a warrior powering up" | **partial:** the swirl reads first; the warrior second |
| A2 | blurred silhouette = a clear figure inside a loop of light | **fail:** a closed oval blob; the dark body disappears against the dark ground and under the ribbons crossing in front of it |
| A3 | same character and moment as the original | pass (armour colour aside) |
| A4 | palette from the original, no green | pass, except the armour should be the original's navy blue |
| A5 | calm dark background | pass |
| A6 | premium pixel art on one grid | the raw has fine, clean pseudo-pixels (about 100 across); see the pixel-density finding below |
| A7 | head, core and arms clear of the badge corners | pass |

## Findings

1. **The body gets lost.** Dark armour on a dark ground, with two ribbons crossing in front of the torso and legs, so at
   45 px only the head, the core and the ribbons survive.
2. **The loop is closed.** The ribbons form a full oval. At 45 px, in the bar, it rhymes with **Crystal Sphere**, the
   kept icon next to it: also a round blue-and-orange shape.
3. **The head is small** (about 8% of the height in a full-body pose): about 4 px at 45 px.
4. **Pixel density (affects the approved C1 setting).** Snapping this raw to 64 art pixels across destroys the face and
   hands; 96 and 128 keep more, and even 128 loses the face. At 45 px all four look the same. So for figure icons the
   approved 48–64 density costs the large-size detail that makes the upgrade premium, and buys nothing at phone size.

## Proposed round 2 (one change set)

1. Armour back to the **original's navy blue**, with a crisp top-left rim light, so the body separates from the ground.
2. Ribbons pass **behind** the torso and arms and cross in front only at the legs; leave dark space around the head and
   arms. **Break the loop**: one ribbon whips out of frame (towards the unseen target).
3. Crop **knees-up** so the head and core are larger (head about 12–15% of the height).
4. Add **forked lightning** along one ribbon (the battle line names it).
5. Keep: the core burst, the gold eyes, the seal rings, the scarf, the flecks.

## Decision for the director: pixel density for figure icons

| Option | Effect |
|---|---|
| a) keep 48–64 (as approved) | consistent chunky pixels; faces and hands lost at 112 px and on the jutsu card |
| b) raise to about 128 for figure icons (256 / 128 = 2 px per art pixel) | keeps most detail and still cleans the colours and the grid |
| c) no snapping for figure icons; the raw downsized to 256 | keeps all the model's detail; less uniform across the set |

Recommendation: **b)**.
