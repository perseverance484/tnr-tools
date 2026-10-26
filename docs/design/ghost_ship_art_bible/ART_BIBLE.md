# Ghost Ship / Skyglass art bible (v0.2)

**Status:** director-directed 2026-10-26 (RUL-2026-10-26-002); open to the art director's review. Collection register for
every Ghost Ship, Skyglass Wreck, treasure-hunt and Crownhold image (`docs/workflows/ISOLATED_ART_GENERATION.md`
section 1).
**Brand:** **Edo-era Japanese fantasy ninja pixel art.**
**Anchor (the look to match):** the original Skyglass crew, **Deck Warden to the Crowned Captain** (ten files in
`art/ghost_ship_skyglass/`), their four scene portraits and the ten ship scenes. Their palette and rendering are correct;
newer art that departs from them is not a reference (section 12).
**Sits under:** `spec.house_style` in `skills/producing-tnr-art/data/25x_DATA_art_spec.json`. Where they differ, the spec
wins until the spec is changed.
**Prompt text:** `blocks.json` in this folder is the only copy. The batch builder pastes it verbatim; this file explains it.
**Sheets:** `ref_characters_on_model.webp` (anchor crew), `ref_portraits_on_model.webp`, `ref_scenes_on_model.webp`,
`ref_icons_on_model.webp`, `ref_drift_do_not.webp`, `palette_measured.webp`.

---

## 1. The world

An Edo-era Japanese fantasy. The Skyglass Project was a secret shogunate programme that learned to bind chakra into a pale
cyan crystal, skyglass. Its warship lies wrecked on a beach; its mountain castle, Crownhold, went dark. What walks there
now are **chakra impressions**: shinobi recalled from the crystal's memory, still obeying the last order. Everything is
hand-made from wood, rope, iron, lacquer, paper and cloth. Skyglass is the only wonder, and it is always a crystal object.

## 2. Technology ceiling (hard rule)

| Allowed | Redo on sight |
|---|---|
| Wood, rope, iron, lacquer, leather, cloth, washi paper, stone, tatami, shoji, fusuma | Screens, terminals, switches, cables, wires, capacitors, glowing panels |
| Paper and skyglass lanterns, candles, braziers, taiko signal drums, bells, banners, nobori flags, kites | Glass tanks, vats, observation glass, operating theatres, laboratories |
| Scrolls, ledgers, brushes and ink, abacus, seal stamps, paper sealing tags | Lab coats, clipboards, headsets, serial plates, automatons, mech parts |
| Katana, wakizashi, yari, naginata, kusarigama, kunai, shuriken, tetsubo, ono | Guns, sci-fi or energy weapons |

## 3. Rendering and pixel density (anchor, measured)

- **Characters:** ~1200 px square canvas, delivered at native size as lossless WebP, **217-255 colours**, about **3-4
  screen pixels per art pixel** (~300-400 art pixels across), no fixed grid.
- **Value:** median brightness **0.17-0.25** (0.20 typical); **50-78%** of pixels darker than 0.25 (63% typical).
  Saturation median **0.25-0.60** (0.40 typical).
- **Edges:** hard; the best anchors (Captain, Deck Warden, Oathkeeper, Sealwright) have no partial-alpha edge at all.
- **Line and shade:** dark outlines about one art pixel wide, flat cel shading in 2-3 steps per material; no airbrush,
  bloom or painterly gradients. Not chunky low-res pixel art, not smooth illustration.
- **Scenes:** 1536 x 1024, ~4-6 px per art pixel, night palette (median value ~0.15 indoors).
- **Icons:** 1024-1254 px raw, 256 px lossless export, one object.

## 4. Palette (anchor crew, `palette_measured.webp`)

| Role | Hex | Use |
|---|---|---|
| Night ink | `#08080d` `#0b0c15` `#10131a` | outlines, deep shadow, most of the garment |
| Deep indigo | `#111b2e` `#1e2d46` `#2f445e` | kimono, hakama, obi, banners |
| Storm-grey lacquer and iron | `#2e2d3a` `#5c6474` `#86858a` | sode, kote, kabuto, bands, rivets |
| Weathered leather and rope | `#413335` `#624c49` `#4c444c` | straps, rope cords, wraps, scabbards |
| Skyglass cyan (house accent) | `#98c1cc` brightening to near-white | crystal, lantern cores, blade edges, lit eyes |

1. One accent per character (spec `house_style.palette`): trim, a carried object or a chakra effect, never a field. The
   crew's accent is skyglass cyan. Crownhold officers each have a named accent, used as small as the crew's cyan.
2. **No gold, no filigree, no tassels, no jewels.** Fittings are dull iron. (This retires Arakane's gold; section 12.)
3. Crownhold adds mountain-stone greys to the base and keeps the indigo.

## 5. Motifs

- **The Skyglass emblem:** a four-point star in a diamond or circle, on banners, chests, vials, the reliquary. A mark,
  never text.
- **Skyglass:** a faceted pale cyan crystal object (lantern core, blade edge, bead, vial, seal stone); never a body, skin,
  vein or cloud.
- **Moon over black water**, wet planks reflecting cyan, tall indigo banners, skyglass lanterns, paper tags on cords,
  rope lashings, tattered hems, salt and weather.

## 6. Characters

### 6.1 Edo costume vocabulary

Built on the anchor crew (hoods, cloth masks, indigo sash, rope belt, lacquered plates, wrapped shins) and pushed to
read as Edo-period shinobi. `blocks.json` `costume_character` is the prompt text.

| Part | Use |
|---|---|
| Body | layered dark kimono, haori or a short wrapped jacket, hakama or tapered trousers |
| Waist | indigo obi with a hanging tail, knotted rope cord, inro or pouches |
| Armour | plain lacquered sode (shoulder), kote (forearm), haidate (thigh) plates, laced not riveted where possible |
| Legs and feet | kyahan shin guards over closed tabi boots, or waraji over tabi; never bare toes |
| Head | hood, tenugui headwrap, kasa or jingasa hat, plain kabuto for heavy fighters |
| Face | cloth mask or menpo over nose and mouth, eyes lit by pale chakra |
| Weapons | katana, wakizashi, yari, naginata, kusarigama, kunai, tetsubo, ono |

Hard negatives (spec `costume_grammar`): no headband, no forehead protector, no clan or village symbol.

### 6.2 Faces, heads, hands

- Faces covered; eyes lit (cyan for the crew, the accent for Crownhold). Only unique named characters show more.
- **Every officer's head reads distinct** (hood, tenugui, kasa, jingasa, kabuto with menpo). No two share a head.
- **Hands are normal gloved hands**, solid, five fingers, inside the silhouette. Never skeletal, translucent or ghostly.
- Grounded adult proportions. Ninja first: lean, practical, quiet. Heavy armour only where the role demands it, and even
  then plain and dark, not parade samurai.

### 6.3 The chakra impression

Two small signs only: chakra-lit eyes, and a faint haze of the accent at torn cloth edges (`blocks.json` `impression`).
Never seams, veins, translucency, crystal bodies, glitching, flicker bands, floating parts or threads from the head.

### 6.4 Chakra effects

On a real object only: a thin flame-like edge along a blade, or a small ball of chakra above an open gloved palm with the
hand drawn normally (`blocks.json` `chakra`). Compact; it must not reach the frame edge or bridge to the key colour.
One effect per character.

### 6.5 Ranks

| Rank | Read |
|---|---|
| Regular | crew vocabulary, one accent, one weapon or tool, standard lean build |
| Commander | bigger and heavier, heavier layered haori or cloak with a high collar, more plates and wraps, commanding stance, a unique head (`blocks.json` `commander`) |
| Unique | a signature no one else may borrow: the Captain (white mask, long hair, katana); Arakane's Command Crown |

## 7. Scenes

The beached wreck and its coves at night (as the ten anchor scenes), and **Crownhold as an Edo mountain castle**: stone
walls and gates, wooden halls with tatami and shoji, armouries of racked yari and katana, archives of scroll shelves,
signal towers with taiko drums and nobori flags, a war-council hall, the summit keep. Night or dusk, moon, cold blue
fill, skyglass lanterns as focal light, wet floors. Wide 3:2, eye level, lower-left and lower-right thirds readable, no
people.

## 8. Item icons

One object, 3/4 at eye level, centred, readable at 125 px; blue-black wood, storm-grey iron, one skyglass accent, the
emblem where it belongs; lime key; no frame, text or halo. Approved family: `ref_icons_on_model.webp` (the seven anchor
icons plus #1-#4 of this batch).

## 9. References

- **New character:** attach `avatar_ghost_ship_deck_warden.webp` only (director, 2026-10-26), with the role in
  `blocks.json` `reference_character`: the crew's look, a different person. A strongly unique reference gets copied (the
  Captain twice; Arakane's gold into every officer), so never use the Captain or Arakane. If the Deck Warden's hood and
  spear start repeating, fall back to the Seal Charge (an object, nothing to copy).
- **Redraw of an existing item:** that item as subject, plus the Seal Charge for rendering.
- **Scene:** one anchor scene for light and palette.
- No sheets or collages. Never list features "not to copy". One image per **fresh** session.

## 10. Prompt blocks

`blocks.json`: `style_character`, `costume_character`, `impression`, `chakra`, `commander`, `negative_character`,
`key_avatar`, `reference_character`. Scene and icon blocks are added when those images are next generated.

## 11. QA checklist (studio, before showing the director)

1. Beside `ref_characters_on_model.webp` at combat size: same crew, same darkness, same density.
2. Reads Edo-period ninja (section 6.1), not samurai parade, not sci-fi, not fantasy-gold.
3. Tech ceiling held (section 2).
4. Face covered, eyes lit, head distinct.
5. Hands normal, feet in closed footwear.
6. One accent, no gold.
7. Impression shown only by eyes and edge haze.
8. Not a copy of any reference.
9. Key clean on dark and light; nothing touches the frame edge.

## 12. Off-model art (not references; redo queue)

Director, 2026-10-26: these approved images veer from the anchor.

| Image | Why | Consequence |
|---|---|---|
| Arakane (`art/crownhold/avatar_crownhold_arakane.webp`, live) | gold, ornate | redraw; his Command Crown design follows (RUL-2026-10-25-011), so the Crownbreaker badge, the Countermand icon and his jutsu icons wait for it |
| Master of Arms (#8) | samurai, heavy orange | redraw |
| Foundry Warden (#7) | brown, off-palette | redraw |
| Crownbreaker badge (#5) | smooth gold medal | redraw after the new crown |

Kept: item icons #1-#4.

### Drift log

| Drift | Rule |
|---|---|
| Head thread read as an antenna | 6.3 |
| Blue energy ghosts (seams, translucency, crystal bodies, glitch) | 6.3 |
| Gold, tassels, crowns everywhere (Arakane as reference) | 4.2, 9 |
| Sci-fi subjects (lab coat, containment suit, automaton, tech rig) | 2 |
| Copy of the Captain, twice | 9 |
| Plain regular, bare toes, mummy-bandaged face | 6.1, 6.2, 6.5 |
| Ghost hand | 6.4 |
| Samurai parade armour, heavy orange (Master of Arms) | 6.2, 4.1 |

**Pending scene rewrites (section 2):** Armory, Research and High Command terminals; Test gallery (capacitor cables); Vat
halls (specimen tanks); Reconstruction theatre (observation glass); High Command signal room (relay board, paper tape).

## 13. Open questions

1. **Seal:** one mark for ship and castle (the Skyglass four-point star), or a separate Crownhold seal?
2. **Accents:** one per officer (current) or one per division?
3. **"Terminal" in the quest text:** rename to an Edo object (command shrine, signal altar, seal desk)?
4. **Arakane's redraw:** keep the Command Crown concept (floating skyglass blades, seal ring) in dark iron and skyglass
   instead of gold?
