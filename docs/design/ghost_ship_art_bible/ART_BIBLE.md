# Ghost Ship / Skyglass art bible (DRAFT v0.1)

**Status:** DRAFT for the director and the art director to review. Not yet binding. Once approved it becomes the
collection register for every Ghost Ship, Skyglass Wreck, treasure-hunt and Crownhold image (the "approved identity
register" that `docs/workflows/ISOLATED_ART_GENERATION.md` section 1 asks each collection to keep).
**Requested by:** director, 2026-10-26: "create an art Bible for all ghost ship image generation that locks in style,
pixel density, palettes, motifs, etc. Edo era Japanese fantasy pixel art ninja game."
**Sits under:** `spec.house_style` in `skills/producing-tnr-art/data/25x_DATA_art_spec.json` (the TNR-wide style
authority). This file specialises it for one collection; where they differ, the spec wins until the spec is changed.
**Measured from:** the 34 director-approved Ghost Ship files in `art/ghost_ship_skyglass/` plus the approved batch art
(Arakane, Master of Arms, Foundry Warden, item icons #1-#4). Every number below comes from those files.
**Sheets in this folder:** `ref_characters_on_model.webp`, `ref_portraits_on_model.webp`, `ref_scenes_on_model.webp`,
`ref_icons_on_model.webp`, `ref_drift_do_not.webp`, `palette_measured.webp`.

---

## 1. The world in one paragraph

An **Edo-era Japanese fantasy**. The Skyglass Project was a secret shogunate-era naval and fortress programme that learned
to bind chakra into a pale cyan crystal, skyglass. Its warship now lies wrecked and beached; its mountain fortress,
Crownhold, went dark. What walks there now are **chakra impressions**: shinobi recalled from the crystal's memory, still
obeying the last order. Everything is made by hand from wood, rope, iron, lacquer, paper and cloth. The only "advanced"
material is skyglass, and it is always a crystal object, never a machine.

## 2. Technology ceiling (hard rule)

| Allowed | Not allowed (redo on sight) |
|---|---|
| Wood, rope, iron, bronze, dull brass, lacquer, leather, cloth, washi paper, stone, tatami, shoji | Screens, terminals, switches, cables, wires, capacitors, circuitry, glowing panels |
| Paper lanterns and skyglass lanterns, candles, braziers, signal drums, bells, flags, kites | Glass specimen tanks, vats, observation glass, operating theatres, laboratories |
| Scrolls, ledgers, brushes and ink, abacus, seal stamps, paper sealing tags | Lab coats, clipboards, headsets, serial plates, automatons, mech parts |
| Katana, wakizashi, yari, naginata, kunai, shuriken, kusarigama, axes, tetsubo | Guns, sci-fi blades, energy weapons not held as chakra on a real weapon |
| Ship parts: masts, rigging, hull planks, capstans, cannon-free decks, cargo crates | Modern objects of any kind (spec `policy_defects`) |

Several prompts already written for Crownhold scenes break this rule ("command terminal", "relay board", "paper tape",
"specimen tanks", "operating theatre", "capacitor cables"). They are listed in section 12 for rewrite.

## 3. Rendering and pixel density (measured)

| Property | Characters (crew avatars) | Scenes | Item icons |
|---|---|---|---|
| Generated canvas | ~1200 px square | 1536 x 1024 | 1024-1254 px square |
| Delivered | native size, lossless WebP | 512 x 341 WebP | 256 px lossless WebP |
| Effective detail | ~3-4 screen px per art pixel (about 300-400 art pixels across the canvas); no fixed grid | ~4-6 px per art pixel | ~3 px per art pixel at full size |
| Colours after processing | 217-255 (palette-quantized by `chroma.py`) | 40k-130k (not quantized) | 256 px export, ~15-18k |
| Median value (brightness, 0-1) | 0.17-0.25 | 0.11-0.34 (night ~0.15) | 0.21-0.69 |
| Share of pixels darker than 0.25 | 50-80% | 60-80% interiors | 17-61% |
| Soft (partial-alpha) edge share | 0 on the best (Captain, Deck Warden, Oathkeeper, Sealwright) | n/a | under 3% |

What that means in plain words:

- **Pixel art in look, not on a fixed grid.** Crisp dark outlines about one art pixel wide, flat cel shading in 2-3 steps
  per material, hard edges, no airbrush, no bloom, no painterly gradients (spec `house_style.rendering` and
  `shading`).
- **Dark.** Most of every character is near-black ink and deep indigo. Light comes from one accent and the skyglass.
- **Medium-high density.** Fine rope twists, rivets and cloth tears are readable; it is not chunky low-res pixel art
  (spec `rejected_registers.chunky_low_res_pixel`) and not smooth illustration (`soft_ai_painterly`, `anime_cel`).

## 4. Palette

Measured from the crew avatars and the ten approved scenes (`palette_measured.webp`). Roles:

| Role | Hex (measured) | Use |
|---|---|---|
| Night ink | `#08080d` `#0a0c14` `#10131b` | outlines, deepest shadow, most of the garment |
| Deep indigo cloth | `#111c30` `#1c314e` `#304762` | robes, sashes, banners, the crew's blue |
| Storm-grey iron and lacquer | `#30303c` `#5d6676` `#84878d` | plates, bracers, helmets, bands, rivets |
| Weathered leather and rope | `#453535` `#5a4a4c` | belts, straps, rope wraps, scabbards |
| Moonlit blue (scenes) | `#2c4972` `#4e607b` `#6c8eaf` | sky, sea, wet planks, cold fill light |
| **Skyglass cyan (the house accent)** | `#94c3cf` (mid), brightening to near-white at the core | crystal, lanterns, blade edges, lit eyes |

Rules:

1. **One accent per character** on top of the base (spec `house_style.palette`): piping, trim, a carried object or a
   weapon, never a field. Crew accent is skyglass cyan or the indigo sash. Crownhold officers each have their own named
   accent (forge-orange, pale violet, muted brass ...).
2. **No gold filigree, no tassels, no jewels.** Brass appears only as dull fittings (buckles, ring ends, rivets).
3. **Crownhold sub-palette:** add mountain-stone greys to the base; keep the indigo. Arakane alone wears blackened gold
   (his Command Crown).
4. Skyglass cyan is the brightest thing in most images. Do not out-shine it with a second glow.

## 5. Motifs and the visual vocabulary

- **The Skyglass emblem:** a four-point star inside a diamond (or a circle). It is on the ship's banners, chests, vials
  and the reliquary. Use it wherever the Project's ownership needs to show. It is a mark, never text.
- **Crownhold's seal:** currently "a plain circled cross" in some prompts (Countermand, Honor Guard). Open question
  (section 13): use the Skyglass emblem instead, so the fortress and the ship share one mark.
- **Skyglass** is always a faceted pale cyan crystal object: a lantern core, a blade's edge, a bead on a cord, a vial, a
  seal stone. It is never a body, a skin, veins or a cloud.
- **Moon and water:** a full moon over black water is the collection's signature sky. Wet planks reflect cyan light.
- **Lanterns:** square-framed skyglass lanterns with cyan cores; paper lanterns are allowed for Crownhold.
- **Banners:** tall indigo banners with the emblem.
- **Paper tags** on cords and sealing tags on scroll cases (blank or with unreadable brush marks, never real text).
- **Tattered cloth:** hems, sashes and cloaks end in ragged tears. Weathering, salt stain, scratches.
- **Rope:** knotted rope belts, rope-wrapped shins and forearms, rope lashings on crates.

## 6. Characters

### 6.1 Costume grammar (every crew member and every Crownhold officer)

From the approved crew: hood or cloth headwrap; a cloth face mask over nose and mouth; a dark layered wrap robe or
jacket; an indigo sash with a hanging tail; a knotted rope belt; plain lacquered shoulder and forearm plates; wrapped
shins over **closed tabi boots or waraji over tabi** (no bare toes); paper tags on cords. It matches spec
`costume_grammar` and keeps its hard negatives: **no headband, no forehead protector, no clan or village symbol**.

### 6.2 Faces, heads and hands

- **Faces are covered.** Cloth mask, half-mask or face guard, with **eyes lit pale chakra** (cyan for the crew, the
  character's accent for Crownhold). Only named unique characters show more (the Captain's white mask and long hair are
  his alone; Arakane's mask and crown are his alone).
- **Heads read distinct per character:** a hood, a headwrap, an iron half-helm, a wide travelling hat, a kabuto. Never two
  officers with the same head.
- **Hands are normal gloved hands**, solid, five fingers, held within the silhouette (spec `house_style.silhouette`). No
  skeletal, translucent or ghost hands.
- **Grounded adult proportions**; commanders are visibly bigger and heavier.

### 6.3 The chakra impression (how "recalled, not alive" shows)

Only two signs, both small:

1. eyes lit with pale chakra;
2. a faint haze of chakra at the cloth's ragged edges (a few pixels of the accent colour on torn hems).

Never: glowing seams or veins, translucent or crystal bodies, glitching, flicker bands, floating parts, threads or lines
rising from the head, ghost tails. They are solid ninjas.

### 6.4 Chakra effects

Chakra is shown **on or around a real object**, not as a body part:

- on a weapon: a thin flame-like edge of the element's colour along a blade or spear;
- in a hand: a **small ball or flame of chakra held above an open gloved palm**, the hand itself drawn normally;
- around a tool: wisps curling off a lantern, a seal jar, a scroll.

Keep it compact (it must not touch the frame edge or bridge to the key background: spec glow rule, `prompts.md`
section 4). One chakra effect per character.

### 6.5 Ranks

| Rank | Read | Examples |
|---|---|---|
| Regular | crew grammar, one accent, one weapon or tool, standard build | Deck Warden, Wayfinder, Oathkeeper, Sealwright |
| Commander | bigger and heavier, heavier layered coat or cloak with a high collar, more plates and wraps, commanding stance, a head no one else has | Master of Arms, the Captain |
| Unique | a signature no one else may borrow | the Captain (white mask, long hair, katana), Arakane (Command Crown) |

## 7. Scenes

- **Places:** the beached wreck (decks, holds, keel, flooded lower hull, chart room, helm), the night coves, and
  Crownhold as an **Edo mountain castle** (stone walls and gates, wooden halls, armouries, archives of scrolls, signal
  towers with drums and flags, a war-council hall, the summit keep).
- **Light:** night or dusk, full moon, cold blue fill, skyglass lanterns as the warm-cold focal points, wet reflective
  floors.
- **Composition:** wide 3:2, eye-level, deep one-point perspective into the room; **lower-left and lower-right thirds kept
  readable** for dialog portraits (spec `SCENE_BACKGROUND`); no people.
- **Density:** props in the middle ground (crates, rope coils, banners, scrolls); floors and ceilings simple.

## 8. Item icons

- One object, 3/4 view at eye level, centered, small even margin, readable at 125 px.
- Materials as section 4: blue-black wood, storm-grey iron, one skyglass accent, the emblem where it belongs.
- Lime key (magenta when the object is green); no frame, no text, no glow halo.
- Approved family: `ref_icons_on_model.webp`.

## 9. References: what to attach

Learned the hard way in this batch:

- **A character reference gets copied.** The Captain as "style only" produced the Captain twice (mask, topknot, katanas)
  even when told not to; Arakane as "style only" made every officer gold-tasselled and crowned.
- **For a new character,** attach a crew **object** for rendering: `avatar_ghost_ship_seal_charge.webp`. The figure comes
  from the text. This worked first time (Master of Arms).
- **For a redraw of an existing item**, attach that exact item as the subject plus the Seal Charge for rendering.
- **For a scene,** attach one approved scene as the light/palette reference.
- Never attach a sheet or collage. Never name features "not to copy": naming them brings them in.
- Run each image in a **fresh session**; a reused session edits its last image.

## 10. Canonical prompt blocks (to be wired into the batch builder once approved)

~~~text
STYLE (character): Edo-era Japanese fantasy, premium pixel art: crisp hard-edged pixels at medium-high density, clean
dark outlines one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush,
no bloom, no painterly gradients. Dark overall: night-ink and deep indigo base, storm-grey lacquered plates, weathered
leather and rope, dull brass fittings only. One accent colour (named in the subject) as trim, a carried object or a
chakra effect. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded
adult proportions, both arms within the silhouette.

COSTUME: hood or cloth headwrap and a cloth face mask with eyes lit by pale chakra; dark layered wrap robe or jacket;
indigo sash and knotted rope belt; plain lacquered shoulder and forearm plates; wrapped shins over closed tabi boots;
paper tags on cords. Solid gloved hands with five fingers.

IMPRESSION: he is a solid ninja recalled as a chakra impression; the only signs are chakra-lit eyes and a faint haze of
the accent colour at the cloth's torn edges.

CHAKRA: any chakra is a compact flame-like glow on a weapon's edge or a small ball of chakra held above an open gloved
palm; the hand is drawn normally.

NEGATIVE (character): no modern or sci-fi objects, no machines, cables or glowing panels, no glowing seams or veins, no
translucent, crystal or ghost body parts, no floating parts, no thread or line from the head, no gold filigree, no
tassels, no crown, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo,
no realistic or smooth painterly rendering, no anime-scaled eyes, no blur.
~~~

Scene and icon blocks follow the same pattern from sections 7 and 8.

## 11. QA checklist (studio, before showing the director)

1. Edo tech ceiling held (section 2).
2. Reads as the same crew at combat size beside `ref_characters_on_model.webp`.
3. Face covered, eyes lit, head distinct from every other officer.
4. Hands normal; feet in closed footwear.
5. One accent; no gold, tassels or crowns (Arakane excepted).
6. Impression shown only by eyes and edge haze.
7. Not a copy of the reference (compare side by side).
8. Key clean on dark and light; nothing touches the frame edge.

## 12. Drift log (why each rule exists)

| Drift | Seen in | Rule |
|---|---|---|
| Thread rising from the head reads as an antenna on the moving sprite | first commanders | 6.3 |
| Blue energy ghosts: glowing seams, translucency, crystal bodies, glitch | first officers #8-#20 | 6.3 |
| Gold tassels, filigree and crowns everywhere | Arakane used as style reference | 4.2, 9 |
| Sci-fi subjects (lab coat, containment suit, automaton, tech rig) | first officer prompts | 2 |
| Copy of the Captain (mask, topknot, katanas), twice | Captain as style reference | 9 |
| Plain regular look, bare toes, mummy-bandaged face | Replicant Zero v1 | 6.2, 6.5 |
| Skeletal / ghost glowing hand | Replicant Zero v1-v2 | 6.4 |
| Smoother illustration than the set | Crownbreaker badge (accepted as is) | 3 |

**Pending rewrites under section 2** (Crownhold scenes in the batch bible): Armory command terminal, Research command
terminal, High Command terminal (a "terminal" is not Edo), Test gallery (capacitor cables), Vat halls (specimen tanks),
Reconstruction theatre (observation glass, operating theatre), High Command signal room (relay board, paper tape). The
quest text may use the same words; renaming them there is a content decision.

## 13. Open questions for the director and the art director

1. **Seal:** one mark for the ship and the fortress (the Skyglass four-point star), or keep a separate Crownhold seal?
2. **Crownhold accent colours:** keep one named accent per officer (current), or tie accents to divisions (I orange, II
   violet, III brass, IV red)?
3. **Pixel density:** lock the crew's ~3-4 px per art pixel, or push towards a stricter grid (true pixel art) with a
   snap step in processing? RUL-2026-10-24-005 rejected snapping for jutsu icons; this would be characters only.
4. **"Terminal" in quest text:** rename to an Edo object (command shrine, signal altar, seal desk)?
5. **Reference:** keep the Seal Charge as the single rendering reference for all new characters?
