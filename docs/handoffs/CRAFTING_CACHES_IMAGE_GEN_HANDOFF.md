# Image generation handoff: three crafting-cache chest icons

- **For:** the image-generation agent
- **From:** Fable / Claude Code
- **Date:** 2026-10-13
- **Repository:** `perseverance484/tnr-tools`, branch `claude/crafting-recipe-census-pln5za`
- **Supersedes:** `docs/handoffs/CRAFTING_CACHES_ART_HANDOFF.md`. Its subject briefs are carried
  forward here, along with ready-to-run prompts and the spec values.
- **Self-contained:** you can work without the repository. If you do have it, the authority is
  `skills/producing-tnr-art/` (see §6).

## 1. Job

Make **three item icons**, one per new loot chest in The Ninja RPG (TNR), a browser game. The
names are approved by dauntless (RUL-2026-10-13-001):

| # | Item name | What it is in game | Delivery filename |
| --- | --- | --- | --- |
| 1 | **Medicine Inro** | Drops reagents for pills | `icon-medicine-inro.webp` |
| 2 | **Shinobi Tool Pouch** | Drops reagents for kunai | `icon-shinobi-tool-pouch.webp` |
| 3 | **Sage's Strongbox** | Drops rare reagents for Legendary consumables | `icon-sages-strongbox.webp` |

All three drop from the same quest vault, so they are a **matched set**:
- the same camera, lighting and rendering;
- a shared near-black lacquer, wood and leather base;
- **one accent colour each**: jade (Inro), copper and steel (Pouch), aged gold (Strongbox).

The accent colours are a proposal. dauntless approves them when approving icon 1.

## 2. Spec values

These are excerpts from `skills/producing-tnr-art/data/25x_DATA_art_spec.json` (sha256
`69766443…f0ae3af`, last changed in commit `16bc4792`). If the repository is available and the
file differs, the file wins.

| Field (`targets.ICON`) | Value |
| --- | --- |
| aspect | 1:1 (square), tolerance 2% |
| recommended source size | 256×256 |
| minimum width | 160 px |
| delivered / displayed width in game | 125 px / 160 px |
| format | WebP, lossless |
| byte ceiling | 460,800 bytes (450 KB working ceiling under a 512 KB hard upload cap) |
| padding | pad with transparency to an exact square, leaving a small margin so the game's rarity frame behind the icon still reads |
| chroma | lime `#00FF00` by default; **magenta `#FF00FF` when the subject carries foliage, jade or green** (`chroma.magenta_when`). **Native transparency is preferred over either key** (`chroma.preferred`). |

The game stretches icons to a square with no `object-fit`, so a non-square image distorts.

## 3. Prompts

Each prompt is built from the spec's `ICON` scaffold plus the house-style clauses. Only the
subject is hand-written.

**Two scaffold defects are corrected below. They are flagged for the art owner, not decided
here:**
- The house-style `silhouette` clause ("both arms held within the subject's own silhouette…") is
  written for characters and has been removed. Objects have no arms, and the clause invites the
  generator to draw some.
- The scaffold says "dark background", but the icon target needs a keyable or transparent result.
  Each prompt below replaces it with a chroma-key background clause.

**Shared style** (house style, in the spec's order, without the silhouette clause):
`crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level,
flat 3/4 view, no low angle and no foreshortening, at most one restrained elemental glow accent,
as rim light on edges only`

**Negative** (ICON negative plus the shared negatives, de-duplicated):
`no asset sheet, no grid, no circular medal frame, no labels, no title text, no UI caption, no
multiple icons, no franchise insignia, no text, no UI, no watermark, no open lid, no contents
spilling out, no loose items around the object, no surface or table under it, no shadow on the
background, no glow halo or light disc`

### Icon 1: Medicine Inro (generate this first; it locks the style)
```
open square pixel-art icon of a lacquered Japanese inro pill case: four stacked tiers, silk cord with a round bead, carved toggle on top, near-black lacquer with one small jade leaf crest, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, at most one restrained elemental glow accent, as rim light on edges only, strong readable silhouette, centered, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no frame, no text
```
**Background:** magenta, because the jade accent would be eaten by a lime key. Use native
transparency instead if the generator offers it.

### Icon 2: Shinobi Tool Pouch
```
open square pixel-art icon of a stiff dark leather ninja hip pouch with a buckled flap and belt loop, iron rivets, copper buckle, the steel ring handles of three kunai poking out from under the flap, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, at most one restrained elemental glow accent, as rim light on edges only, strong readable silhouette, centered, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard, no frame, no text
```

### Icon 3: Sage's Strongbox
```
open square pixel-art icon of a small closed iron-banded hardwood strongbox, near-black wood, aged gold corner bands and a heavy gold lock plate, white paper ofuda seal strips across the lid seam, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, at most one restrained elemental glow accent, as rim light on edges only, strong readable silhouette, centered, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard, no frame, no text
```
The seal strips must have no legible kanji or symbols, because invented text is always wrong.
Blank or abstract brush marks only.

## 4. Process

1. **One image per generation.** Generate icon 1, run the raw QC below, and show it to dauntless.
   **Wait for approval.** Approval locks the style.
2. Generate icons 2 and 3 to match the approved icon. Pass the approved icon as an image reference
   when the surface accepts one. Pass it as an individual image, never a collage.
3. **Containers are a known weak spot.** The spec records that generators "reliably fail on
   packaging formats". If a subject comes back wrong three times in a row, stop re-describing it.
   Switch to reference-image prompting, for example a photo of a real inrō, a leather tool pouch
   or a strongbox.
4. **Start each icon in a clean context** carrying only its own references. Carried-over images
   have displaced icon requests before.

**Raw QC, before any processing.** Reject and regenerate instead of repairing when any of these
fails:
- the image is square, holds one complete object, and is not a crop from a sheet;
- there are no text, labels, watermarks, UI, borders or grids;
- the key background is a true solid flat colour across the whole canvas: no checkerboard, no
  gradient, no shadow cast onto it;
- **there is no painted glow disc or halo, and the object is not sitting on a surface.** Both are
  unprocessable (`chroma.unprocessable`);
- the accent is only an accent, not a field of colour.

**Processing:**
1. Key the background to transparency.
2. Clamp the spill.
3. Pad to an exact square with a small transparent margin.
4. Export lossless WebP at no less than 160 px wide (256×256 recommended).
5. Keep each file under the byte ceiling.
6. **Composite onto a dark background and check the edges before handing over.** Spill and chewed
   edges are invisible on white.

If you have the repository, use the skill's own pipeline instead of improvising this
(`skills/producing-tnr-art/references/processing.md`).

## 5. Delivery

- Return the three files to dauntless, named **exactly** as below. Put the names in a code block
  so they are copied, not retyped. They become `@img:` references in the release manifest.
  ```
  icon-medicine-inro.webp
  icon-shinobi-tool-pouch.webp
  icon-sages-strongbox.webp
  ```
- **Corrections get a fresh name** (`icon-medicine-inro_b.webp`, then `_c`). Never reuse a name,
  because CDN and picker caching would serve the old bytes.
- Include a small ledger with one row per file: slug, type `ICON`, filename, pixel dimensions,
  bytes and KB.
- Do not upload to the game and do not commit the image files. dauntless uploads them through the
  builder in the release push.

## 6. If you have the repository

- Spec: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`. Read `targets.ICON`,
  `house_style`, `chroma` and `prompt_scaffolds`.
- Process: `skills/producing-tnr-art/SKILL.md`, `references/prompts.md` and
  `references/processing.md`.
- Design context: `docs/design/crafting_caches/CRAFTING_CACHES_DRAFT.md`.

## 7. Out of scope

- Loot tables, item text, the release manifest and any live upload or push.
- Scene art and avatars.
- The other Ghost Ship content.
