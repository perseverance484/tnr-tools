# Art request: village bloodline scroll icons (6)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude Code, at dauntless's request (2026-10-20)
- **Status:** APPROVED as written by dauntless, 2026-10-20 (RUL-2026-10-20-005): the silhouette,
  per-scroll treatments, palettes and style lock below. The rendered style is still locked by the
  director's visual approval of icon 1.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec authority: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ICON`.
- **Live-game requests/writes:** 0. Nothing here uploads anything.

**Delivered (2026-10-21):** 1 Oblivion Seal and 2 Shinseina Ki (`_b`), director-approved; files in `art/village_bloodline_scrolls/`, sent for review as push/154. Icon 1 locks **pixel-art rendering** and the silhouette: a painted Shinseina Ki v1 was rejected for that reason. Fittings are per scroll (silver on Oblivion Seal, gold on Shinseina Ki, both approved), so section 3's "aged gold" is a default, not a rule.

## 1. Why

Six legendary scrolls each grant a different A-rank village bloodline, but all six use **the same
image file** (2026-10-20 public read), so a player cannot tell them apart in the inventory or a
reward list. Each needs its own icon that names its bloodline's element at a glance.

## 2. Targets

| # | Item | Grants (village) | Element (from the bloodline) | Delivery filename |
|---|---|---|---|---|
| 1 | Shadow Scroll: Oblivion Seal | Oblivion Seal (Syndicate) | Shadow | `icon-village-scroll-oblivion-seal.webp` |
| 2 | Wood Scroll: Shinseina Ki | Shinseina Ki (Tsukimori) | Wood | `icon-village-scroll-shinseina-ki.webp` |
| 3 | Storm Scroll: Arashima | Arashima (Akasumi, formerly Shroud) | Storm | `icon-village-scroll-arashima.webp` |
| 4 | Sun Scroll: Taiyo Kami | Taiyo Kami (Shirohana, formerly Shine) | Scorch | `icon-village-scroll-taiyo-kami.webp` |
| 5 | Wind Scroll: Aerathiel | Aerathiel (Akikaze, formerly Current) | Dust | `icon-village-scroll-aerathiel.webp` |
| 6 | Ice Scroll: Hyouga Yui | Hyouga Yui (Hyorin, formerly Glacier) | Ice | `icon-village-scroll-hyouga-yui.webp` |

Ids and current icon URLs are in the 2026-10-20 public read and are added by script when the release
manifest is built; they are not needed to draw.

## 3. Style lock (from the approved crafting caches set)

Taken from the director-approved item icons in `art/crafting_caches/` (Medicine Inro, Shinobi Tool
Pouch, Sage's Strongbox; director-approved 2026-10-13, provenance in `art/crafting_caches/README.md`):

- painted rendering with a crisp dark outline, soft rim light, no hard cast shadow;
- dark lacquer, wood and paper materials with **aged gold** fittings;
- one bold readable silhouette, 3/4 view at eye level, centred; transparent background.

**References per session (pass the actual image bytes, individually, never a collage):**
1. `art/crafting_caches/icon-shinobi-tool-pouch.webp`: **style/material only**.
2. After approval, icon 1: **style and scroll silhouette only** (sessions 2-6).

Do not pass the current shared scroll icon, and do not pass the Bloodright glyph art
(`art/bloodright/*/foundation.webp`): its diamond glyphs would pull in an ornamental symbol (P0 D).
Palettes below are taken from that art as text only.

## 4. Design (approved)

**Silhouette (all six).** One closed handscroll (makimono) lying on a slight diagonal: two lacquered
wooden end rollers with gold caps, the paper rolled tight and bound by a cord tied in a knot. The
same silhouette and camera at every scroll, so the set reads as a family; each bloodline is told
apart by **colour, cord and one element effect**, never by a symbol.

| # | Scroll | Palette | Treatment |
|---|---|---|---|
| 1 | Oblivion Seal | deep violet on black | black lacquer rollers, violet cord, thin wisps of violet shadow seeping from the paper's seam |
| 2 | Shinseina Ki | leaf green and gold | living-wood rollers sprouting two or three small leaves, green cord, soft green glow along the seam |
| 3 | Arashima | storm grey with white-blue | storm-grey paper, silver caps, small white-blue lightning arcs jumping between the two end caps |
| 4 | Taiyo Kami | orange and sun gold | gold sun-disc end caps, orange cord, ember glow and heat shimmer along the paper's edge |
| 5 | Aerathiel | pale sand with pale cyan | sand-coloured paper, pale cyan cord, a thin spiral of wind carrying dust grains around the scroll |
| 6 | Hyouga Yui | deep ice blue and white | frosted rollers, deep blue cord, small ice crystals forming on the paper |

Arashima and Aerathiel both lean cyan in their Bloodright art; here Arashima keeps the **grey and
lightning**, Aerathiel the **sand and dust**, so the two stay apart at 125 px.

## 5. Spec values (`targets.ICON`)

| Field | Value |
|---|---|
| aspect | 1:1, tolerance 2% (the game stretches icons; non-square distorts) |
| recommended source | 256x256 (minimum 160 px wide) |
| delivered / displayed width | 125 px / 160 px |
| format | WebP, lossless |
| byte ceiling | 460,800 bytes |
| padding | transparent margin so the rarity frame behind the icon still reads |
| background | native transparency preferred; otherwise lime `#00FF00` key (scroll 2 is green, so use magenta `#FF00FF` for it) |

## 6. Prompts

**Shared style clause (proposal; icon 1 locks it):**
`game item icon, painted digital illustration with a crisp dark outline, dark lacquered wood and paper with aged gold fittings, soft rim light, camera at eye level, 3/4 view, no foreshortening, strong readable silhouette, centered, single object`

**Shared negative:**
`no text, no letters, no kanji, no writing on the paper, no symbols, no glyphs, no runes, no seals with markings, no labels, no UI, no frame, no circular medal, no watermark, no asset sheet, no multiple objects, no open or unrolled scroll, no hands, no person, no surface or table under it, no shadow on the background, no glow halo or light disc, no franchise insignia`

**Subject lines** (one per session; append the style clause, then the background clause):

| # | Subject |
|---|---|
| 1 | a closed rolled handscroll lying on a slight diagonal, black lacquered end rollers with gold caps, bound by a violet cord, thin wisps of violet shadow seeping from the seam of the paper |
| 2 | the same closed handscroll with living-wood end rollers sprouting a few small green leaves, bound by a green cord, a soft green glow along the seam |
| 3 | the same closed handscroll with storm-grey paper and silver caps, bound by a grey cord, small white-blue lightning arcs jumping between the end caps |
| 4 | the same closed handscroll with gold sun-disc end caps, bound by an orange cord, ember glow and heat shimmer along the edge of the paper |
| 5 | the same closed handscroll with pale sand-coloured paper, bound by a pale cyan cord, a thin spiral of wind carrying dust grains around it |
| 6 | the same closed handscroll with frosted end rollers, bound by a deep blue cord, small ice crystals forming on the paper |

**Background clause:** `transparent background` where the generator supports it; otherwise
`on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard`
(magenta `#FF00FF` for scroll 2).

## 7. Process

1. **Icon 1 (Oblivion Seal) first.** One image per session. Show it to the director and wait for
   approval: it locks the style clause and the scroll silhouette.
2. Icons 2-6, each with the tool pouch plus approved icon 1 as references, nothing else.
3. Two wrong-subject results in one session: close it and start clean (protocol section 3).
4. **Raw QC before processing:** square, one complete closed scroll, no writing, symbols or glyphs,
   no halo or glow disc, not sitting on a surface, background truly flat or transparent.
5. **Processing at intake:** key or keep native alpha, clamp spill, pad to square, lossless WebP,
   check edges on a dark composite, then `artpreflight.py --type ICON`.

## 8. Delivery and next step

- Return each approved original with its filename exactly as in section 2. A correction gets a fresh
  name (`_b`, `_c`).
- Include a ledger row per file: filename, type `ICON`, pixel size, bytes.
- After intake and preflight, the six icons go to the review desk as one Forge suggest-mode ticket
  (category VISUAL, title "Update icon", one rationale per scroll).

## 9. Director decisions

Approved as written on 2026-10-20 (items 1 to 3).

1. One shared handscroll silhouette, told apart by colour, cord and element effect (section 4).
2. The six palettes and treatments in section 4.
3. Style follows the crafting caches set (section 3).
