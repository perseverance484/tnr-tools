# Chakra Overflow draft 1: review and path to the premier icon

- **Subject:** the director's first draft, `art/jutsu_icons/chakra_overflow/candidates/raw_chakra_overflow_draft1.png`
  (2026-10-23): a central gold-white flame flanked by two blue flame wings, on black.
- **Method:** four independent reviews run in parallel (small-size readability, art direction against the brief,
  distinctness against 52 house icons and the 40 most-used live icons, and Pillow edit experiments), checked against
  the brief's acceptance criteria (`CHAKRA_OVERFLOW_ICON_PROJECT.md` section 3) and the battle UI sizes from the game
  source. Evidence sheets are in `review/`.
- **Status:** analysis for the director. Every art decision stays the director's (CLAUDE.md section 10).

## 1. Verdict

A striking image with the right color story and the right brightness, but it is **a fire, not boundless chakra**,
and it **fails the composition lock**. It should be regenerated with this draft's strengths carried over, not patched.

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
| - | Concept: boundless chakra (director, 2026-10-23) | **Partly told** | the energy does pour upward, but as flames: it says "a fire is burning", not "chakra without limit is flowing". It sits nearest D2, but the brief's "compact white-hot core with a crown of flame-tongues" became a bonfire fanning from the bottom edge. |
| - | Color C: blue **intensifying into** gold | **Split, not a transition** | blue and gold sit side by side as separate fires instead of one energy getting hotter toward its source. The blue is bright cyan, closer to ice or lightning fire than deep chakra blue. |

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

**Concept correction (director, 2026-10-23):** "An item doesnt need to overflow, the chakra we're depicting is what's
overflowing. You're activating this flow of energy by using the technique. So we want to convey boundless chakra with
this icon." There is no vessel, orb or container: **the subject is the chakra itself, flowing without limit.** The
review's earlier "restore the vessel" recommendation is withdrawn; D1's breaking vessel and the CO-H hybrids are retired.

1. **Draw chakra as energy, not flame.** Boundless chakra pours from a white-hot source as luminous currents, rays and
   crackling streams with clean, smooth edges, never as flame tongues. This is what separates it from every fire icon,
   from Ethereal Rebirth's flame pillar, and from a fire-element reading. Energy cues: light rays, smooth flowing
   ribbons, an electric or plasma rim, sparks streaming upward.
2. **One source, flowing out without end.** A compact white-hot heart near the center from which the chakra surges
   outward and upward; the streams thin and fade into the dark before they reach the edges, so the flow reads as
   endless while the emblem stays a bounded shape on screen. "Boundless" is told by motion and fade, not by filling
   the frame.
3. **Color as intensity.** Calm deep chakra blue at the outer reaches of the flow, growing hotter toward the source
   until it turns gold and then white-hot: one energy, rising in power, not two fires side by side.
4. **A strong upward weight.** The flow is strongest and longest upward, so the overall silhouette points up
   (a crown-like burst or a rising arrowhead): the universal power-up sign, and the draft's best feature (its rising
   central spike), kept. Brightest point at or just above center (about 43-47% down).
5. **Enforce the frame.** Emblem inside the central 75-85%, at least 20 px of dark at 256 on every side, bottom corners
   black, nothing touching an edge. Lit coverage about 30-40%.
6. **Crisp, rim-lit form** with far fewer fractal wisps, so the shape survives at 32 px.
7. **Pass the grayscale test.** With color removed, the shape must differ from Ethereal Rebirth, Particle Cannon and
   Drops of Renewal (silhouette match under 0.6; the distinctness script can be re-run).

## 6. Round 2 brief (replaces section 2 of the round-1 prompt for the next generations)

Use the round-1 shared header and exclusions unchanged, plus:

~~~text
Concept (director, 2026-10-23): BOUNDLESS CHAKRA. Using the technique opens a flow of chakra without limit; the
chakra itself is what overflows. There is no vessel, orb, container or object of any kind: the energy is the subject.

Lessons from draft 1: keep its gold-as-brightest value and its rising central spike; drop the flame tongues, the
side flame wings and the full-frame bonfire. Drawn as fire, it read as a fire-element jutsu and matched the Ethereal
Rebirth flame pillar in grayscale.

Dominant silhouette: a compact white-hot source of chakra just above the center of the frame, from which chakra
surges outward and upward without end, as luminous energy (smooth flowing currents, light rays, crackling plasma
edges, sparks streaming upward), NEVER as flame tongues. The flow is strongest and longest upward, so the whole
emblem points up. Color is intensity: deep chakra blue at the outer reaches, hotter toward the source, turning gold
and then white-hot at the heart. The streams thin and fade into the dark before they reach the frame edges, so the
flow feels endless while the emblem stays one bounded shape.

Composition: whole emblem inside the central 80%; dark navy-to-black space on every side; both bottom corners empty
and dark; nothing touches any edge. Reads as "a power-up" at 32 px in grayscale.

Avoid: flames or flame tongues of any kind, fire, a bonfire spreading from the bottom, side flame wings, cyan or
ice-blue fire, an orb, sphere, vessel or any object, a body or aura outline of a person, fractal wisp texture filling
the frame, spirals, vortices, rings, and any pillar rising from broken stone.
~~~

Variants worth one generation each:

- **R2-a, chakra nova:** the source bursts outward in every direction as luminous streams, the upward ones longest,
  forming a crown-shaped starburst.
- **R2-b, rising torrent:** a wide surge of chakra currents rushes upward from the source and converges into one
  sharp upward arrowhead, sparks streaming off its point.
- **R2-c, power flare:** a tall teardrop flare of crackling chakra energy with a white-hot heart and an electric rim,
  shedding rising streams from its tip (an energy flare, not a flame, and no figure inside it).

## 7. Evidence

| File | What it shows |
|---|---|
| `review/draft1_in_context.png` | the draft (top) and the current icon (bottom) in the mobile and desktop battle bars, a 112 px tile with level badge, 32 px, and the silhouette test |
| `review/draft1_32px.png`, `review/draft1_45px.png` | the draft at in-game sizes, enlarged without smoothing |
| `review/draft1_grayscale_neighbors.png` | grayscale strip: the draft beside its nearest house and live neighbors |
| `review/draft1_mockups.png` | the six edit experiments in the in-game preview |
