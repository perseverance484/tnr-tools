# Art request: Zombie Villager avatar (1)

- **For:** the art director and one isolated generation session
- **From:** Fable / Claude, at dauntless's request (2026-10-26)
- **Status:** PROPOSAL. The look, the accent and the two bible exceptions in section 3 await director approval.
- **Target record:** Zombie Villager, AI `nqL-uL-Z_7I0iuowlpBDx` (level 25 Genin, wave enemy in the three
  ruined-village fights of Headless Rider Horror!, `0lNDtE_VYJOCy8JZQI_sI`; push/266).
- **Style authority:** `docs/design/ghost_ship_art_bible/ART_BIBLE.md` v0.3 and `blocks.json` 0.3 (RUL-2026-10-26-002/003),
  applied here outside its Ghost Ship collection at the director's request. Spec `25x_DATA_art_spec.json` target
  `AI_AVATAR` wins on delivery numbers.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one image, fresh session, show and wait).
- **Live-game requests/writes:** 0.

## 1. Who he is

From the quest: the undead of a farming village the Headless Rider destroyed years ago. They shuffle out after sunset,
stand back up after being cut down, and crumble to ash past the village gate. Peasants, not shinobi. His only weapon is
his claws (Zombie Claws, push/264).

## 2. What the bible gives him

| Bible rule | Applies as |
|---|---|
| Brand: Edo-era Japanese fantasy pixel art (header) | yes: Edo farmer, period cloth, no modern objects |
| Rendering and density (section 3): hard pixels, ~1 px dark outline, 2-3 step cel shading, no airbrush or bloom | yes, verbatim from `style_character` |
| Value (section 3): median brightness 0.17-0.25, most of the figure dark | yes |
| Palette (section 4): night ink and deep indigo base, storm-grey, weathered leather and rope | yes; the kosode is faded indigo |
| One accent, never a field, no gold (section 4) | yes; the accent is **dim ember-orange eyes**, tying him to the Rider's curse (replaces skyglass cyan, which is the Ghost Ship crew's) |
| Lean, tall, battle-ready (section 6.0) | adapted: gaunt and tall, hunched forward, both clawed hands reaching, a stance of attack rather than a drawn weapon |
| Camera, framing, full body with a margin, arms inside the silhouette | yes |
| Key (`key_avatar`): magenta `#FF00FF`, 1024 x 1024 | yes; magenta also protects grey-green rot from a lime key |

## 3. Two bible exceptions (director to approve)

1. **Undead imagery.** `negative_character` bans "rot, bones, skulls or grave motifs" because Ghost Ship enemies are
   solid chakra impressions. A zombie is the subject, so that clause is dropped for this image only. Kept restrained:
   grey-blue decaying skin and a sunken face; no gore, no exposed organs, no skeleton.
2. **Ninja costume.** `costume_character` (hood, cloth mask, sash, tabi) is for shinobi. He gets villager costume
   instead: torn faded kosode, rope belt, straw sandals over wrapped feet (closed footwear holds, section 6.1), face
   uncovered so the eyes and rot read.

## 4. Prompt (paste as one block)

`Style: Edo-era Japanese fantasy, premium pixel art: crisp hard-edged pixels at medium-high density, clean dark outlines about one art pixel wide, flat cel shading in two or three steps per material, limited palette, no airbrush, no bloom, no painterly gradients. Subject: a single undead Edo-era farmer, a zombie villager: gaunt and tall, hunched forward, both hands reaching out with long cracked fingernails, grey-blue decaying skin, sunken face, dim ember-orange eyes. Costume: a torn and faded indigo kosode, a knotted rope belt, straw waraji sandals over wrapped feet, one sleeve burnt at the hem. Colour: near-black and faded indigo cloth, grey-blue skin, the ember-orange eyes the only accent. Camera at eye level, front three-quarter view, full body inside the frame with a clear margin, grounded adult proportions, both arms within the silhouette. On a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.`

`Negative: no modern objects, no weapons, no gore, no exposed organs, no skeleton, no glowing seams or veins, no translucent or ghost body parts, no floating parts, no gold, no headband, no forehead protector, no clan or village symbol, no text, no bare toes, no aura or halo, no glow disc, no realistic or smooth painterly rendering, no anime-scaled eyes, no blur, no scenery, no floor, no cast shadow on the key colour, no key-colour spill, no second character, no horse, no rider, no pumpkin, no fire, no sheet, no grid.`

## 5. Reference

Attach `art/halloween_headless_rider/headless_rider_avatar.webp` once, labelled:

`STYLE: rendering, palette, outline weight and darkness only. This is a different character, described by the text.`

Bible section 9 warns that a strongly unique reference gets copied. The Rider is one (horse, fire, pumpkin head), so the
negative bans those three. If any of them shows up, close the session and restart clean; do not lengthen the prompt
(protocol section 3).

## 6. QA before showing the director (bible section 11, adapted)

1. Beside the Rider avatar at combat size: same darkness and density.
2. Reads Edo peasant zombie: not western, not samurai, not a ninja.
3. One accent (the eyes), no gold, no fire.
4. Hands normal-shaped with five fingers; feet in sandals, no bare toes.
5. Undead kept restrained: no gore, no bones.
6. No horse, rider or pumpkin copied from the reference.
7. Key clean; nothing touches the frame edge.

## 7. Intake

| Field | Value |
|---|---|
| filename | `avatar_hrh_zombie_villager.webp` |
| aspect | 1:1 exact (the client stretches avatars) |
| source | 1024 x 1024 (bible `key_avatar`); spec minimum 320 |
| format | WebP lossless, under 460,800 bytes; quantize only if over |

1. `python3 skills/producing-tnr-art/scripts/rawqc.py <raw> --scaffold hrh_zombie_avatar --record`
2. `python3 skills/producing-tnr-art/scripts/chroma.py <raw> avatar_hrh_zombie_villager.webp --target AI_AVATAR --key magenta --qc qc.png`, then check the dark composite.
3. `python3 skills/producing-tnr-art/scripts/artpreflight.py avatar_hrh_zombie_villager.webp --type AI_AVATAR`, 0 errors.
4. Commit under `art/halloween_headless_rider/`. Fable builds the avatar edit from the push/262 read with an image pack
   (Zombie Claws re-sent unchanged, no other field).
