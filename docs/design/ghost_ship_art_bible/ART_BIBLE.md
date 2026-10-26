# Ghost Ship / Skyglass art bible (v0.4, PROPOSED)

**Status:** PROPOSED v0.4 from the art director handoff of 2026-10-26, implemented on `fable/skyglass-art-bible-v04` for
independent review and director acceptance. v0.3 (RUL-2026-10-26-001 to -003) stays in force until then. Collection
register for every Ghost Ship, Skyglass Wreck, treasure-hunt and Crownhold image
(`docs/workflows/ISOLATED_ART_GENERATION.md` section 1).
**Brand:** **Edo-era Japanese fantasy ninja pixel art.**
**Anchor (the look to match):** the original Skyglass crew, **Deck Warden to the Crowned Captain** (ten files in
`art/ghost_ship_skyglass/`), their four scene portraits and the ten ship scenes. Newer art that departs from them is not
a reference (section 12).
**Sits under:** `spec.house_style` in `skills/producing-tnr-art/data/25x_DATA_art_spec.json`. Where they differ, the spec
wins until the spec is changed.
**Single sources:** `blocks.json` holds every shared prompt sentence; `roster.json` holds every Crownhold character's
head, weapon or prop, stance and constraints. `state/skyglass_art/build_art_batch.py` pastes both verbatim;
`state/skyglass_art/check_art_batch.py` proves the output agrees. This file explains them and repeats no prompt text.
**Sheets:** `ref_characters_on_model.webp` (anchor crew), `ref_portraits_on_model.webp`, `ref_scenes_on_model.webp`,
`ref_icons_on_model.webp`, `ref_drift_do_not.webp` (review only, never a generation reference), `palette_measured.webp`.

---

## 1. The world

An Edo-era Japanese fantasy. The Skyglass Project was a secret shogunate programme that learned to bind chakra into a pale
cyan crystal, skyglass. Its warship lies wrecked on a beach; its mountain castle, Crownhold, went dark. What walks there
now are **chakra impressions**: shinobi recalled from the crystal's memory, still obeying the last order. Research and
command spaces are Edo sealing, medical, archive and war-council rooms, never laboratories or control rooms.

## 2. Technology ceiling (hard rule)

| Allowed | Redo on sight |
|---|---|
| Wood, iron, rope, bamboo, stone, lacquer, leather, cloth, washi paper, ceramics, hand-made vessels, tatami, shoji | Electronic equipment, terminals, screens, cables, switches, capacitors, glowing panels |
| Paper and skyglass lanterns, candles, braziers, taiko drums, bells, banners, nobori flags | Glass tanks, vats, observation glass, operating theatres, laboratory machinery |
| Scrolls, ledgers, brushes and ink, abacus, seal stamps, paper sealing tags, handcrafted sealing apparatus | Lab coats, clipboards, headsets, serial plates, automatons, industrial pipes and valves |
| Period weapons (katana, tachi, wakizashi, tanto, yari, naginata, nagamaki, kusarigama, sai, jitte, kunai, tetsubo, ono, bokken) | Guns, futuristic or energy weapons |
| Skyglass as a physical faceted crystal set in crafted objects | Skyglass as skin, veins, bodies or clouds |

## 3. Rendering and pixel density (anchor, measured)

- **Characters:** ~1200 px square canvas, delivered at native size as lossless WebP, **217-255 colours**, about **3-4
  screen pixels per art pixel**, no fixed grid. Fine, deliberate pixel clusters; hard dark outlines about one art pixel
  wide; flat cel shading in 2-3 value steps per material. Not chunky retro sprites, not smoothed, no bloom or airbrush.
- **Value:** median brightness **0.17-0.25**; **50-78%** of pixels darker than 0.25. Saturation median **0.25-0.60**.
- **Edges:** hard; the best anchors (Captain, Deck Warden, Oathkeeper, Sealwright) have no partial-alpha edge at all.
- **Composition:** full body, eye level, front three-quarter, grounded adult anatomy, readable at ~125 px.
- **Scenes:** 1536 x 1024, ~4-6 px per art pixel, night palette. **Icons:** 1024-1254 px raw, 256 px export.

## 4. Colour contract

| Role | Hex | Use |
|---|---|---|
| Night ink | `#08080D` `#10131A` | outlines, deep shadow, most of the garment |
| Deep indigo | `#111B2E` `#1E2D46` | kimono, hakama, sash, banners |
| Storm-grey metal | `#2E2D3A` `#5C6474` | plates, bracers, helmets, fittings |
| Leather and rope | `#413335` `#624C49` | straps, functional lashings, scabbards |
| **Skyglass (universal, the only luminous colour)** | `#98C1CC`, brighter highlights sparingly | crystal, eyes, chakra-worked edges |

**Division material identifiers** (PROPOSED v0.4; non-emissive, existing material shades, not secondary glows):

| Division | Material | Hex |
|---|---|---|
| I Armoury | weathered forge-rust | `#624C49` |
| II Research | muted ink-mauve | `#4C444C` |
| III High Command | storm-slate | `#5C6474` |
| IV Sanctum | pale iron-ash | `#86858A` |

These replace the v0.3 per-character accents (forge-orange, pale violet, lightning gold ...). No gold, ornate trim,
jewellery, filigree or broad character-specific rainbow accents. Rope is for functional lashings and containers, not
decorative harnessing.

## 5. Motifs

- **The Skyglass emblem, the one seal** (RUL-2026-10-26-004): a four-point star in a diamond or circle. Ship and castle
  share it: banners, chests, vials, the Countermand tablet, the Sealbearer's tablet. A mark, never text; no other seal.
- **Skyglass:** a faceted pale cyan crystal object; never a body, skin, vein or cloud.
- **Moon over black water**, wet planks reflecting cyan, tall indigo banners, skyglass lanterns, paper tags, rope
  lashings, tattered hems, salt and weather.

## 6. Characters

### 6.1 Shared costume grammar

Common crew language, not a uniform (`blocks.json` `costume_character`): Edo shinobi layered kimono, haori, hakama or
fitted wraps; a cloth mask; a hood, headwrap or hat; an indigo waist sash; closed tabi with wrapped shins; practical arm
protection; plain lacquered armour only where the role needs it, never ornate parade armour; torn hems and sash ends may
show movement; **one dominant weapon or working tool**. Each character's head (from the register) replaces the default.
Hard negatives (spec `costume_grammar`): no headband, no forehead protector, no clan or village symbol.

### 6.2 Silhouette, pose and build

- **Generally lean and agile**; controlled specialist variation is allowed (the Stonebound's one earth-armoured arm).
- **Battle-ready with the weapon, or actively using the role-defining combat tool** (the Signaller's gunbai, the
  Sealbearer's tablet). No idle poses, never hands behind the back.
- At combat size every character has a **unique head + weapon/prop + stance** (section 6.6).

### 6.3 Rank

| Rank | Read (`blocks.json`) |
|---|---|
| Regular (`regular`) | lean and agile; head, weapon or tool and action carry the identity |
| Commander (`commander`) | about 8-12% taller than a regular, **not wider**: structured raised collar, longer split haori, controlled battle stance, no oversized shoulder plates |
| Final boss | Arakane: the tallest, lean, commanding; the Command Crown is his alone (section 6.7) |
| Unique signatures | the Captain (white mask, long hair, katana); Arakane's Command Crown. No one else borrows them |

### 6.4 Division silhouettes (`blocks.json` `division_I`-`division_IV`)

| Division | Silhouette |
|---|---|
| I Armoury | angular, aggressive, short split coats, weapons prominent |
| II Research | narrow, vertical, asymmetric, scroll and seal equipment |
| III High Command | clean directional silhouettes, hats, disciplined weapons, flags, restrained straight coat panels |
| IV Sanctum | severe enclosed silhouettes, darkest clothing, straight seal panels, almost no accessories |

### 6.5 Chakra impressions and chakra effects

- Fully solid shinobi with normal anatomy and equipment. The only tells: small chakra-lit eyes and a faint haze at torn
  cloth. No transparent bodies, floating limbs, ghost hands, glowing seams, crystal skin, glitch effects or threads.
- Chakra is compact and purposeful, at a working blade, tool or hand; no free-floating spell spectacle.

### 6.6 Identity register (`roster.json`)

Twenty reserved identities: the nineteen Crownhold officers (batch #8-#26) and Arakane (prerequisite brief A, outside
the 79). Each entry carries title, division, rank, head, weapon or prop, stance, the division's material accent and its
constraints, plus the batch number, game slot and delivery file (unchanged from v0.3). Live usernames stay in
`push/crownhold.gen.py` (`USERNAME`); the register never repeats them. The checker proves all 20 heads, all 20 props
and all 20 head + prop pairs are distinct.

### 6.7 Arakane's Command Crown (design lock)

Defined once in `roster.json` (`crown`): a thin **closed ring of blackened iron** with seven blunt seal notches and one
small faceted cyan seal stone at the front; above it, with a small gap, **seven separate floating skyglass blades** (one
central upright, paired inner and outer diagonals, two shorter flanking blades), dark-outlined and cel shaded. No gold,
glowing strings, crystal debris, jewels, halo, radiant ghost body or ornate armour. He outranks the Crowned Captain by
disciplined seven-blade geometry and posture, not size or decoration; at 125 px the crown reads as one powerful head
silhouette. The Crowned Captain is unchanged. Every crown-derived image (#5 Crownbreaker, #46 The Last Directive, #47
Extermination Order, #48 Countermand) is BLOCKED until brief A is approved; the builder then attaches the approved avatar
as their subject.

## 7. Scenes

The beached wreck and its coves at night, and **Crownhold as an Edo mountain castle**: stone walls and gates, wooden halls
with tatami and shoji, armouries of racked weapons, archives of scroll shelves and paper-tagged crystal boxes, sealing-jar
halls, a recall chamber, signal towers with bells, cords and taiko drums, a war-council hall, carved command shrines, the
summit keep. Night or dusk, cold blue fill, skyglass lanterns as focal light. Wide 3:2, eye level, lower thirds readable,
no people. v0.4 rewrote the seven futuristic Crownhold briefs and the industrial wording in three hunt scenes; locations,
story beats, files and node ids are unchanged. The quest text says "command shrine" too (RUL-2026-10-26-004).

## 8. Item icons

One object, 3/4 at eye level, centred, readable at 125 px; blue-black wood, storm-grey iron, one skyglass accent; lime key
(magenta when green); no frame, text or halo. Approved family: `ref_icons_on_model.webp`.

## 9. References

- **Characters:** one reference only, `avatar_ghost_ship_deck_warden.webp`, role `blocks.json` `reference_character`
  (the crew's look; a different person). Never the Captain or Arakane.
- **Objects and pixel redraws:** the subject image plus the Seal Charge, role `reference_object`. Never the old Arakane.
- **Scenes:** one anchor scene for light and palette, plus the Captain's portrait for pixel rendering.
- The drift sheet is for review only. No sheets, collages or rosters as references. One image per **fresh** session.

## 10. Prompt blocks

`blocks.json` 0.4: `style_character`, `costume_character`, `regular`, `commander`, `division_I`-`division_IV`,
`material_accent`, `impression`, `chakra`, `negative_character`, `key_avatar`, `reference_character`,
`reference_object`. A character brief is: subject (from the register, plus rank, division and material blocks), then
style, costume, impression, chakra, key and negative.

## 11. QA checklist (studio, before showing the director)

1. Beside `ref_characters_on_model.webp` at combat size: same crew, same darkness, same density.
2. Reads Edo-period ninja, not samurai parade, sci-fi or fantasy-gold.
3. Head, weapon or prop and stance match the register; none matches another officer.
4. Rank and division read from the silhouette; commanders taller, not wider.
5. Face covered, eyes lit; hands normal; feet in closed tabi.
6. Only skyglass glows; the division material reads as a dull shade; no gold.
7. Not a copy of any reference.
8. Key clean on dark and light; nothing touches the frame edge.

## 12. Off-model art and drift log

| Image | Why | Consequence |
|---|---|---|
| Arakane (`avatar_crownhold_arakane.webp`, live) | gold, ornate | brief A redraws him as `avatar_crownhold_arakane_v2.webp`; the old file is kept |
| Master of Arms / Armsmaster (#8) | samurai, heavy orange | redraw |
| Foundry Warden (#7) | brown, off-palette | redraw (brief aligned to the crew) |
| Crownbreaker badge (#5) | smooth gold medal | redraw after brief A |

Kept: item icons #1-#4.

| Drift | Rule |
|---|---|
| Head thread read as an antenna | 6.5 |
| Blue energy ghosts (seams, translucency, crystal bodies, glitch) | 6.5 |
| Gold, tassels, crowns everywhere (Arakane as reference) | 4, 9 |
| Sci-fi subjects and rooms | 2, 7 |
| Copy of the Captain, twice | 9 |
| Plain regular, bare toes, mummy-bandaged face | 6.1, 6.3 |
| Ghost hand | 6.5 |
| Samurai parade armour, heavy orange | 6.1, 4 |
| Squat, static, brown-and-brass, no weapon (Grand Marshal v1) | 6.2, 6.3 |

### Corrections in v0.4 (rationale)

1. "Every character lean and tall" became "generally lean and agile; controlled specialist variation; commanders taller
   not wider": the rule was forcing one body for twenty roles.
2. "Weapon drawn" became "weapon or actively used role tool": a herald, a signaller and a sealbearer fight with their tools.
3. The four costume marks are a shared language, not identical heads and coats.
4. Rope allowed for functional lashings and containers.
5. Chakra allowed at working blades, tools and hands; no free-floating spell effects.
6. Commanders gain length (collar, haori), not bulk.
7. Skyglass stays a physical crystal; impression bodies stay solid.
8. Handcrafted sealing apparatus is distinct from machinery.
9. Primary silhouettes are reserved across the whole roster.
10. Arakane is the only crown.

## 13. Open questions and contract issues

1. **Division materials (PROPOSED):** accept the four division material shades in place of per-character accents?
2. ~~Seal~~ **Decided** (RUL-2026-10-26-004): one shared seal, the Skyglass emblem.
3. ~~"Terminal" in the quest text~~ **Decided** (RUL-2026-10-26-004): command shrine, renamed in push/273 on main.
4. **Chroma key contract:** `25x_DATA_art_spec.json` declares **lime** for `AI_AVATAR`; this batch has generated and keyed
   every avatar on **magenta** (`blocks.json` `key_avatar`, `chroma.py --key magenta`). Resolve in the spec's owner before
   more processing; not changed here.
5. **Ruling ids:** `docs/RULINGS.md` holds two RUL-2026-10-26-001 and two -002 (Forge budget/guard gaps and the Skyglass
   art rulings). Reported, not renumbered here.
