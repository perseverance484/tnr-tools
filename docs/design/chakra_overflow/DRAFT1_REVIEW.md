# Chakra Overflow draft 1: review and path to the premier icon

- **Subject:** the director's first draft, `art/jutsu_icons/chakra_overflow/candidates/raw_chakra_overflow_draft1.png`
  (2026-10-23): a central gold-white flame flanked by two blue flame wings, on black.
- **Method:** four independent reviews run in parallel (small-size readability, art direction against the brief,
  distinctness against 52 house icons and the 40 most-used live icons, and Pillow edit experiments), checked against
  the brief's acceptance criteria (`CHAKRA_OVERFLOW_ICON_PROJECT.md` section 3) and the battle UI sizes from the game
  source. Evidence sheets are in `review/`.
- **Status:** analysis for the director. Every art decision stays the director's (CLAUDE.md section 10).

## 1. Verdict

A striking image with the right color story and the right brightness, but it is **a fire, not the jutsu**, and it
**fails the composition lock**. It should be regenerated with this draft's strengths carried over, not patched.

## 2. What to keep

| Strength | Evidence |
|---|---|
| **Gold is the brightest value and the eye goes to the center first** | at 32 px the gold averages luminance 194 against 77 for the blue (2.5x); center 150 against 66 for the outer ring |
| **It is the brightest tile in the bar** (criterion 5) | mean luminance 87 against 65-80 for the approved icons |
| **Upward motion** reads as rising energy at 70 and 112 px | the central gold spike survives at 32 px |
| **The blue and gold pairing is new to the house set** | no approved icon pairs them; it does not blend into the orange fire tiles |

## 3. What fails, against the acceptance criteria

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Reads as "power up" at 32 px | **Fails** | at 32 px the silhouette reads as a fleur-de-lis, lotus or trident: a three-pronged plant (`review/draft1_32px.png`). The gold core is a thin stalk (4-8 px wide over 25 rows at 32 px), more candle than surge. |
| 2 | One silhouette in grayscale | **Fails** | blurred, it fills 28-30 of 32 columns from row 10 down: a lit block, not an emblem. 54% of the frame is lit. |
| 3 | Unique in the bar | **Fails** | in grayscale it is nearly the same picture as **Ethereal Rebirth** (silhouette match 0.82, the highest of 92 icons compared: flame tongues fanning up from a bright base). It shares Vaporia Scorch Break's blue-meets-orange look (combined match 0.66), and live Luminous Illusion Bind and Yin-Yang Cascade use the same pairing. |
| 3 | Not fire, not a ring of fire | **Fails** | it is drawn as flames, so it reads as a **fire-element** jutsu (Chakra Overflow has no element); the blue wings curl around the center, close to the banned ring of fire. |
| 4 | Clear of the badge corners | **Fails** | the flame base and its horizontal spray sit across the bottom band where the level and count badges go (`review/draft1_in_context.png`, 112 px tile); the brightest corners are the bottom ones. |
| 6 | House rendering | **Partial** | a smooth digital painting with fractal wisps and no hard rim-lit outline. The approved icons are painterly too, but each has a defined form with a crisp edge; this has none. |
| - | Composition lock (bounded, about 70%, above center) | **Fails** | the art spans the frame edge to edge (x 8-246, y 2-254 at 256); the tip touches the top edge and the border clips it; the brightness center sits below middle (y 143 of 256). |
| - | Concept: chakra past its limit | **Not told** | there is no vessel or core, so nothing overflows. It sits nearest D2, but the brief's "compact white-hot core with a crown of flame-tongues" became a bonfire fanning from the bottom edge. |
| - | Color C: blue **erupting into** gold | **Split, not a transition** | blue and gold sit side by side as separate fires. The blue is bright cyan, closer to ice or lightning fire than deep chakra blue. |

## 4. What the edit experiments showed (`review/draft1_mockups.png`)

Six edits of the draft were rendered in the in-game preview. **Framing fixed the most; color edits did almost nothing.**

| Edit | Badge corners lit (BL / BR) | Focal contrast | Takeaway |
|---|---|---|---|
| draft as is | 22% / 21% | 142 | baseline |
| **bounded** (art scaled into the center with dark space) | **0% / 0%** | **162** | clean emblem at 45 px; brightness center rises to middle. Best single fix. |
| **corners** (darken bottom corners and edge) | 0% / 0% | 159 | keeps the art large; the base still meets the tile edge |
| value (darker blue) | 19% / 19% | 142 | barely visible: the blue's bright veins are near white-cyan, so only regeneration can fix it |
| core (boost white-hot origin) | 22% / 21% | 142 | no change: the origin is already white, it just sits too low (81% down) |
| bounded + corners + value + core | 0% / 0% | 155 | clean, but at 72% scale it looks small and dim beside full neighbors |

The lesson: **the problem is composition and concept, not detail.** About 80-85% scale with dark corners balances
presence against clarity; posterizing the detail made 112 px muddier without helping 32 px.

## 5. How to make it the premier icon (ranked)

1. **Restore the vessel.** Move to the **hybrid (CO-H1 / CO-H2)**: a bounded deep-blue orb of chakra whose crown bursts
   open into one gold-white flare rising upward. One shape then holds both "overflow" (the vessel breaking) and
   "power up" (the rising flare). This is also the strongest way out of the fire family and Ethereal Rebirth: a sphere
   is a hard geometric form that no flame icon has.
2. **Make the color a transition.** Deep cobalt or indigo blue inside the orb, shifting to gold and white-hot exactly
   at the rupture. One boundary between blue below and gold above, not interleaved flames.
3. **Give the flare a strong upward point.** Carry over this draft's central gold spike as the flare, but make it a
   bold, wide shape (35-45% of the width) with a pointed tip or a rising chevron, its brightest point at or just above
   center (about 43-47% down). Upward chevrons are the universal power-up sign, and no house icon uses one.
4. **Enforce the frame.** Emblem inside the central 75-85%, at least 20 px of dark at 256 on every side, bottom corners
   black, tip clear of the top edge. Lit coverage about 30-40%.
5. **Hard, rim-lit silhouette.** A crisp orb outline and a clean flare edge, with far fewer fractal wisps; Hemocure's
   sphere (BEE) shows the rendering quality, in a different hue.
6. **Pass the grayscale test.** With color removed, the shape must differ from Ethereal Rebirth, Particle Cannon and
   Drops of Renewal (silhouette match under 0.6; script from the distinctness review can be re-run).

## 6. Round 2 brief (replaces section 2 of the round-1 prompt for the next generations)

Use the round-1 shared header and exclusions unchanged, plus:

~~~text
Lessons from draft 1 (director's first draft, reviewed 2026-10-23): keep its gold-as-brightest value and its
rising central spike; drop the flame wings and the full-frame bonfire. It read as a fire-element jutsu and matched
the Ethereal Rebirth flame pillar in grayscale.

Dominant silhouette: ONE deep cobalt-blue sphere of chakra, crisp rim-lit edge, filling about 55% of the frame
width, sitting in the lower-middle of the frame (its base no lower than 80% down). Its crown has burst open: from
the rupture one bold gold-to-white-hot flare rises straight up, wide at the base (about 40% of the frame width) and
narrowing to a sharp point well clear of the top edge, shaped like an upward arrowhead or a crown of three tongues.
Blue turns to gold exactly at the rupture; a little glowing gold overflow runs down the sphere's upper sides. The
brightest point is where the flare leaves the sphere, near the center of the frame.

Composition: whole emblem inside the central 80%; dark navy-to-black space on every side; both bottom corners empty
and dark; nothing touches any edge. Reads as "a power-up" at 32 px in grayscale.

Avoid: flame wings or side flames, a bonfire spreading from the bottom, cyan or ice-blue fire, fractal wisp texture
filling the frame, spirals, rings of fire, and any pillar rising from broken stone.
~~~

Variants worth one generation each: **R2-a** flare as a crown of three tongues; **R2-b** flare as a single upward
arrowhead; **R2-c** sphere cracked with fine gold fissures below the rupture (more "breaking vessel").

## 7. Evidence

| File | What it shows |
|---|---|
| `review/draft1_in_context.png` | the draft (top) and the current icon (bottom) in the mobile and desktop battle bars, a 112 px tile with level badge, 32 px, and the silhouette test |
| `review/draft1_32px.png`, `review/draft1_45px.png` | the draft at in-game sizes, enlarged without smoothing |
| `review/draft1_grayscale_neighbors.png` | grayscale strip: the draft beside its nearest house and live neighbors |
| `review/draft1_mockups.png` | the six edit experiments in the in-game preview |
