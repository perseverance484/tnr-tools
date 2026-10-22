# Art request: scroll icons, set 3 (9 icons)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-22)
- **Direction:** RUL-2026-10-22-006; plan and colour slots in `docs/design/scroll_icons/SCROLL_ICON_ROADMAP.md`.
  Each raw still needs the director's visual approval; the palettes below are the agreed slots, not final art.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ICON` (item icon, alpha required).
- **After delivery:** Fable processes the raws (key, clean alpha, 256 px lossless WebP, preflight) and builds **one**
  suggest-mode manifest with one suggestion per scroll.
- **Live-game requests/writes:** 0. Nothing here uploads anything.

**Delivered:** 3/9. #1 Scroll of Shadows (`raw_scroll_of_shadows_b.png` → `icon_scroll_of_shadows_b.webp`); #2 Scroll of Hollow Veil (`raw_scroll_of_hollow_veil_b.png` → `icon_scroll_of_hollow_veil_b.webp`); #3 Scroll of Cleave (`raw_scroll_of_cleave_b.png` → `icon_scroll_of_cleave_b.webp`). All native alpha, preflight clean, 2026-10-22.

## 1. Why

Every jutsu and bloodline scroll must read as a different scroll at icon size (125 px). Today three of our new
scrolls share KGK's violet-on-black (Oblivion Seal, Scroll of Shadows, Scroll of Hollow Veil), Cleave shares
Aerathiel's teal wind, Dragon's Scroll reuses the KGK Black Fang Lance image, and the Forbidden, Metal and Time
scrolls are small, low-detail parchment. Sheets: `docs/design/scroll_icons/sheet_*.png`.

## 2. The two silhouettes (locked)

| Shape | Used for | Look | Style reference (pass the image bytes, one file, never a collage) |
|---|---|---|---|
| **Jutsu scroll** | scrolls that teach a jutsu | fat closed scroll at 45 degrees, heavy steel end caps with claw-cut rims, braided cord with a round knot medallion and two tassels, effect swirling around it | `art/item_icons/event_scrolls/raws/raw_scroll_of_bastion_v1.png` |
| **Bloodline scroll** (universal; was "village") | scrolls that grant a bloodline | long thin handscroll on a shallow diagonal, tight cord wraps, small end caps, effect along the seam | `art/village_bloodline_scrolls/raws/raw_village_scroll_oblivion_seal_v1.png` |

Both are **pixel-art rendering** (crisp dark outline, hard pixel edges, limited shading), as in the approved sets.
Reference images are for **shape, rendering and construction only**: never copy their colours.

**Taken (do not reuse):** violet on black lacquer = KGK. Leaf green = Shinseina Ki. Teal wind on cream = Aerathiel.
Sun gold-orange = Taiyo Kami. Electric white-blue on grey = Arashima. Deep ice blue = Hyouga Yui. Aqua water =
Renewal. Fang red-orange flame = Blazing. Pearl white with starlight = Celestial Dew. Earth brown = Bastion.

## 3. Targets

| # | Item (id) | Shape | Palette (slot) | Effect / detail | Delivery filename |
|---|---|---|---|---|---|
| 1 | Scroll of Shadows (`uLLAWOSCFeDz9Mc3d0rKw`), teaches Aegis of Shadows | jutsu | **oxblood crimson on black** | black paper, oxblood cord and tassels, dark red shadow wisps curling into a shield-like ring around the scroll; no violet anywhere | `icon_scroll_of_shadows_b.webp` |
| 2 | Scroll of Hollow Veil (`4huDnXDq5zInzZ3dLgykM`), teaches Hollow Veil | jutsu | **ash grey and bone white** | bone-white paper, grey cord, a translucent ash-grey veil of mist wrapping the scroll; desaturated; no violet, no blue | `icon_scroll_of_hollow_veil_b.webp` |
| 3 | Scroll of Cleave (`K5j9Hq19eRftSFDyIX6TN`), teaches Tempest Cleave | jutsu | **steel silver with orange edge** | recolour of the current Cleave: keep the composition, make the wind blades steel/white-silver with hot orange cutting edges; cord and tassels gunmetal grey; **no teal** | `icon_scroll_of_cleave_b.webp` |
| 4 | Shadow Scroll: Oblivion Seal (`7tZoY3uG2Jxg8Fp0dZlwE`), grants Oblivion Seal | bloodline | **indigo-black void** | recolour of the current Oblivion Seal: black lacquer stays, the violet becomes deep indigo; seam wisps read as a dark void rather than violet glow | `icon-bloodline-scroll-oblivion-seal_b.webp` |
| 5 | Scroll of Metal (`Kzx7F3FsKMqfWNNVhpMbG`), grants Tetsugan | bloodline | **dark iron / gunmetal, rust-red cord** | riveted iron bands on the rollers, iron-grey paper with a faint forged texture, small sparks at one cap | `icon-bloodline-scroll-tetsugan.webp` |
| 6 | Scroll of Time (`_M2UwSUpP_szhbuicUoSC`), grants Sands of Time | bloodline | **sand and aged bronze** | bronze caps, sand-coloured paper, a thin stream of falling sand along the seam, a tiny bronze hourglass charm on the cord | `icon-bloodline-scroll-sands-of-time.webp` |
| 7 | Dragon's Scroll (`mDBpVrKfygS5V5EZgvcn1`), grants the item Colored Jewel of the Dragon's Neck (EPIC) | jutsu | **jade green with a gold pearl** | a small jade dragon coiled around the scroll holding a glowing pearl; jade is deep and bluish, clearly not leaf green | `icon_dragons_scroll.webp` |
| 8 | Forbidden Jutsu Scroll: Nexus (`XZfVErGEkHpPiPtPa7_VC`), grants Ethereal Nexus | jutsu, **forbidden variant** | **magenta seals** | the scroll bound by black iron chains and paper seal tags marked in magenta; magenta energy leaking between the chain links | `icon_forbidden_scroll_nexus.webp` |
| 9 | Forbidden Jutsu Scroll: Rebirth (`X5q3Ww-yfCeJ3m6ZqPmmz`), grants Ethereal Rebirth | jutsu, **forbidden variant** | **scarlet seals** | the same chains and seal tags as #8, marked in scarlet, with a single pale ember rising from the seam | `icon_forbidden_scroll_rebirth.webp` |

**Forbidden variant:** jutsu silhouette plus chains and seal tags; #8 and #9 must match each other in construction and
differ only in colour and their one effect. Approve #8 first; it locks the pair.

## 4. Prompt template (one session per icon)

Attach the shape reference from section 2 (for #3 and #4, also attach the current icon being recoloured:
`art/item_icons/event_scrolls/raws/raw_scroll_of_cleave_v1.png` /
`art/village_bloodline_scrolls/raws/raw_village_scroll_oblivion_seal_v1.png`).

~~~text
Target: <item name>, a legendary ninja scroll item. One square 1:1 game item icon.

Reference image attached: match its SHAPE, PIXEL-ART RENDERING and CONSTRUCTION exactly (<jutsu scroll: fat closed
scroll at 45 degrees with heavy steel end caps, braided cord, round knot medallion and two tassels | bloodline
scroll: long thin handscroll on a shallow diagonal with tight cord wraps and small end caps>). Do NOT copy its colours.

Palette: <palette from section 3>. Detail: <effect / detail from section 3>.

One empty scroll, centred, filling about 85% of the canvas, crisp dark outline, hard pixel edges.

Background: transparent. If transparency is not possible, a true solid flat lime-green (#00FF00) key over the whole
canvas (for #7, which is green, use magenta #FF00FF), not a checkerboard and not black.

Avoid: text, kanji, readable symbols or runes; hands, people; a scene, ground or cast shadow; frames, UI, watermarks;
more than one item; painterly or photoreal rendering; any colour listed as taken by another scroll.

Generate ONE image. Do not upload or process it.
~~~

For a recolour (#3, #4): "Recolour the attached icon only: keep every shape, line and effect; change the palette to
<palette>."

## 5. Order and approvals

1. #1 Shadows, #2 Hollow Veil, #3 Cleave (jutsu shape).
2. #4 Oblivion Seal recolour (bloodline shape).
3. #5 Metal, #6 Time (bloodline shape).
4. #7 Dragon's Scroll; #8 then #9 (forbidden pair).

Two wrong-subject results in one session: close it and start clean. Raw QC per icon: correct shape; palette inside its
slot and outside every taken slot; readable at 125 px; transparent or flat-key background.

## 6. Delivery

Return each director-approved original under its exact filename (section 3; a correction gets `_c`, `_d`), PNG or
WebP at any size of 1024 px or more, square. Include a ledger row per file: filename, item, pixel size, bytes. Do not
process or upload anything: intake, preflight and the review-desk ticket are Fable's.

**Ticket note (Fable):** the push/215 suggestions for Shadows, Hollow Veil and Cleave were submitted 2026-10-22. The
desk allows one open suggestion per record, so those three must be approved or rejected before the new ticket covers
them; the other six have none open.
