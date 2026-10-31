# Skyglass art request: shared direction for the generation sessions

- **For:** the art director (ChatGPT generates; Claude does intake afterwards)
- **Scope:** every Skyglass asset still marked NEEDS ART in `docs/design/SKYGLASS_ART_AUDIT.md` after the director
  decisions RUL-2026-10-30-061 (end section of the audit), plus the seven variant-token motif versions
- **Prompts:** `docs/handoffs/SKYGLASS_ART_PROMPTS.md` (one paste-ready block per asset)
- **Register:** `docs/design/skyglass_art/ART_REGISTER.md` (status per asset)
- **References:** `skyglass_art_refs.zip`, numbered folders; each prompt names the folder and the exact files to attach
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (RUL-2026-10-14-001)
- **Live-game requests/writes:** 0. **Credentials:** none.

This file owns no rule. It collects the direction already ruled elsewhere so each session can start from one page.
Where it disagrees with `docs/RULINGS.md`, `skills/producing-tnr-art/data/25x_DATA_art_spec.json` or
`docs/design/ghost_ship_art_bible/`, those win and this file is corrected.

## 1. How a session runs

1. **One asset per fresh chat.** Open a new chat, paste exactly one block from the prompts file, attach the files it
   names, and nothing else.
2. **At most two reference images**, each attached as its own image with the role the block states:
   - **SUBJECT:** the object or design to keep (the base weapon of a variant, the approved token base).
   - **STYLE-ONLY:** rendering, outline weight, palette and pixel density. Never copy its subject or composition.
   - **MATERIAL-ONLY:** how a material looks (skyglass crystal, iron, glass). Never copy its shape.
   Never attach a contact sheet, a whole folder, another asset's prompt or a rejected image.
3. **One candidate at a time.** Show it, then approve, reject or ask for a same-subject revision.
4. **Two wrong-subject or wrong-composition results in one chat: close it and start a clean one** with the same block.
   Do not lengthen the prompt and do not carry the rejected image forward.
5. **Order matters in two places.** VT00 (the variant-token base) must be approved before VT01-VT07, because each motif
   version attaches it. Start each family with its first block (IC01 for the charts, AV01 for the avatars) and judge
   the rest against the approved first image.

## 2. Style anchor

**Edo-era Japanese fantasy ninja pixel art, anchored on the original Ghost Ship crew** (Deck Warden to the Crowned
Captain), their portraits and the ten ship scenes (RUL-2026-10-26-002; `docs/design/ghost_ship_art_bible/ART_BIBLE.md`).

- **Rendering:** crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel
  shading in two or three steps per material, limited palette, soft even lighting. No airbrush, bloom or painterly
  gradients. Not chunky low-res pixel art, not smooth illustration (spec `house_style`).
- **World:** everything is hand-made from wood, rope, iron, lacquer, paper and cloth. **Technology ceiling** (bible §2):
  no screens, terminals, switches, cables, glass tanks or vats, laboratories, guns or machines. Crownhold has command
  **shrines**, sealing **jars**, bell-cords and a spear gallery (RUL-2026-10-26-004/-005).
- **Accent:** skyglass, a faceted pale cyan crystal. It is always an object or inlay (lantern core, blade edge, bead,
  seal stone), never a body, skin, vein, cloud or glowing field.
- **The Skyglass emblem:** a four-point star in a diamond or circle (RUL-2026-10-26-004). It is the only mark allowed on
  any image, on banners, chests, seals, tablets and tokens. Never text, kanji, runes or any other symbol.
- **No gold and no filigree** on characters and fittings (bible §4.2); fittings are dull iron, brass only on one or two
  small fittings of a character. The single exception is the **Epic seal colour** on the two Epic charts (§4).
- **No crowns on Crownhold officers**, no thread or line from any head, no glowing seams, no translucent or crystal
  bodies (RUL-2026-10-26-001). Officers are solid shinobi recalled as chakra impressions: chakra-lit eyes and a faint
  haze of their accent at torn cloth edges, nothing more.
- **No franchise insignia, ever:** no headband, forehead protector, clan or village symbol, real-world logo (spec
  `hard_negatives`).

## 3. Palette

From the anchor crew (`docs/design/ghost_ship_art_bible/palette_measured.webp`, bible §4), with the FX families from
`docs/design/SKYGLASS_BOSS_ANIMATIONS.md`:

| Role | Hex | Use |
|---|---|---|
| Night ink | `#08080d` `#0b0c15` `#10131a` | outlines, deep shadow, most of a garment |
| Deep indigo | `#111b2e` `#1e2d46` `#2f445e` | kimono, hakama, obi, banners, chart cloth |
| Storm-grey lacquer and iron | `#2e2d3a` `#5c6474` `#86858a` | plates, bands, rivets, fittings |
| Weathered leather and rope | `#413335` `#624c49` `#4c444c` | straps, cords, wraps, scabbards |
| Skyglass cyan (house accent) | `#98c1cc` brightening to near-white | crystal, inlay, lantern cores, blade edges, lit eyes |
| FX heavy (ember) | ember red into white-hot | heavy damage, the ember tile |
| FX control (violet) | violet into ink | control / lock (Hexweave) |
| FX lingering (bile) | bile green | rot, pools, the Core Horror's spit and enrage |
| FX safe | skyglass cyan | safe hexes, the Skyglass emblem |

One accent per character or object, as trim, inlay or a single carried object, never a field (spec
`house_style.palette`). Crownhold officers each carry their own named accent, used as small as the crew's cyan.

## 4. Tier seals (RUL-2026-10-28-028 item 4, tiers per RUL-2026-10-29-058, scope per RUL-2026-10-30-061 item 4)

| Rarity | Seal on the icon | New assets in this request |
|---|---|---|
| Common | plain: an undyed dark wax dab or no seal | Tide Chart, Watch Roster |
| Rare | cyan: a small pale skyglass-cyan wax seal | Galley Stores (chests take their tier the same way) |
| Epic | gold: a small deep amber-gold wax seal, the only gold on the object | Reliquary Seal, The Last Heading |
| Legendary | no coloured seal: the game's Legendary rarity frame does it (composited behind the icon) | the two Haul page bases, Skyglass Token, the variant-token base and motifs, The Little Horror's Jar, Crown's Hoard |
| Legendary, tainted | rot-green seal, **only** on the two tainted charts | Rotted Reliquary Seal, The Rotted Heading (Claude derives both by script, §7) |

Existing live chart and chest icons are not redrawn to fit the scheme (RUL-2026-10-30-061 item 4). Core Rot (a
reagent), Countermand (an AI-held item) and the variant skins carry no tier seal. **Leave a small even margin on every
item icon** so the rarity frame behind it reads (spec `ICON.padding_rule`).

## 5. Variant rule (RUL-2026-10-29-049 item 3; `SKYGLASS_TEXT.md` §5)

- Every variant keeps its **base weapon's silhouette**; the base's live icon is attached as the SUBJECT.
- Skyglass appears **only as inlay and accents** (a vein, beads, a stud, a star, a seal disc).
- **The Skyglass Katana stays the only all-crystal blade.** No variant may read as a crystal sword, and no blade is
  turned to crystal, even when the base already has a coloured or glowing blade: keep the base's own blade treatment.
- The six bases that carry two variants (Aetherion, Thornsilver, Stormrender, Oathbinder, The Unwritten, Warden's
  Bracers) must read clearly apart at 125 px; generate the Skyglass set first, then the boss set beside it.
- The variant-token motifs (VT01-VT07) change only the motif on the approved VT00 token; the token itself stays fixed.

## 6. Canvas and background per type (`25x_DATA_art_spec.json` governs; this is the summary)

| Type (client field) | Generate at | Background | Claude delivers |
|---|---|---|---|
| ICON (`item.image`, item-variant image) | 1024 x 1024, one object, small even margin | transparent; else a true flat **lime** `#00FF00` key. **Magenta** `#FF00FF` when the subject is green or rot-coloured (marked in the block) | 256 px lossless webp |
| JUTSU_ICON (`jutsu.image`) | 1024 x 1024 | a designed opaque dark background (RUL-2026-10-14-001); no key | 256 px lossless webp |
| SCENE_CHARACTER (`sceneCharacters[]`) | 1024 x 1536 (2:3 full body) | transparent; else flat **lime** | 2:3 lossless webp |
| AI_AVATAR (`userData.avatar`) | 1024 x 1024 | flat **magenta** `#FF00FF` (the Skyglass/Crownhold batch rule) | square lossless webp |
| SCENE_BACKGROUND (`sceneBackground`) | 1536 x 1024 (3:2) | none; no people or creatures; lower-left (and lower-right) kept open for the dialog portrait | 512+ px wide lossy webp |
| ANIMATION raw layer (`gameAsset` ANIMATION / STATIC) | 1254 x 1254, one element per canvas | transparent; else flat **magenta** (the boss-FX raws are magenta; never lime: bile is green) | strips of 50 px frames built by `art/skyglass_boss_fx/` |

Keyed images: the key covers the whole canvas, is not a checkerboard, carries no shadow, and fills every enclosed space
(inside rings, loops and handles). Glow is a thin edge light only, never a painted disc, halo or light field: a glow
that bridges to the key is keyed away with it (spec `chroma.unprocessable`).

## 7. What Claude derives by script (no prompt)

| Derived asset | From | How |
|---|---|---|
| Rotted Reliquary Seal (`2sGi5SZXh2UutHmM-mIMD`) | approved IC03 Reliquary Seal | the amber-gold seal recoloured to rot-green; nothing else changes |
| The Rotted Heading (`U2yJbBM6_N1xBBf0ez96F`) | approved IC04 The Last Heading | same |
| Ledger Page: The Bone Store (`uu6ETQimuBJ69jwr76IIi`), Ledger Page: The Snare Room (`6QgcnW0v6gZeHY474BjR0`) | approved IC06 Ledger Page (= The Trophy Hold) | the tie cord and wax dab recoloured, one colour per page |
| Stores Manifest: The Ore Vault (`9j4IErGW1gmZ-5FNjZMEQ`), Stores Manifest: The Bloom Cellar (`7Sz2ttMScKH8b10XYS12I`) | approved IC07 Stores Manifest (= The Overgrown Stores) | same |

The art spec does not prevent this: the ICON target is a keyed 256 px lossless export, so a hue shift confined to one
isolated region (the seal, the cord) keeps the edges and alpha exact. That is why IC03/IC04 keep the seal the only
gold on the object and IC06/IC07 carry one coloured cord. If a returned base makes the region hard to isolate, Claude
says so at intake rather than forcing the recolour.

Not in this request: the neutral Elemental Tool Pouch redraw (still a director call, audit D4) and every asset already
finished or reused (the audit's uploads list).

## 8. Return contract

- **Return each director-approved original, unprocessed:** no crop, key, resize, recompression or screenshot. The PNG
  the generator produced, as downloaded.
- **Name it by asset code first,** then the raw name the block gives, e.g. `IC01_raw_icon-tide-chart.png`. A
  same-asset revision gets `_b`, `_c`.
- Add one line per file: code, asset name, approved (yes / approved with note), and the note.
- Do not upload anything or touch the game. Claude does raw QC (`rawqc.py`), keying (`chroma.py --target`), padding,
  `artpreflight.py`, contact sheets at 125/64/32 px, the register update and the image-swap manifests; the director
  runs the builder.
