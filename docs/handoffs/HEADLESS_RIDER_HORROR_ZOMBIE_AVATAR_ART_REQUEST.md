# Art request: Zombie Villager avatar upgrade (1)

- **For:** the art director and one isolated generation session
- **From:** Fable / Claude, at dauntless's request (2026-10-26)
- **Status:** PROPOSAL. Look and accent await director approval.
- **Target record:** Zombie Villager, AI `nqL-uL-Z_7I0iuowlpBDx` (director-supplied). The quest's three
  ruined-village fights reference `C2npKrdVww2J9EKsJpa1W`; `push/262` confirms whether that is the same
  zombie. If it is not, the fights are re-pointed or both records get this avatar.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. Spec authority:
  `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `AI_AVATAR`.
- **Live-game requests/writes:** 0.

## 1. Who he is

From the quest (objectives Vah2P to dKZp2): the undead of a village the Headless Rider destroyed
years ago. They shuffle out after sunset, keep standing back up after being cut down, and crumble to
ash if they pass the village gate. Rural villagers, not warriors.

## 2. Target

| Field | Value |
|---|---|
| filename | `avatar_hrh_zombie_villager.webp` |
| aspect | 1:1 exact (the client stretches avatars) |
| source | 640x640, minimum 320 |
| format | WebP lossless, under 460,800 bytes |
| background | GPT native transparency preferred; otherwise **magenta `#FF00FF`** key, not lime: rotting skin and moss read green and lime would eat them (`spec.chroma.magenta_when`) |
| padding | transparent to exact square after keying, subject centred |

## 3. Direction (director to approve)

- **Matches the Headless Rider avatar's register** (style-only reference): painted figure with pixel
  discipline, dark low-value palette, crisp outline.
- **Subject:** a gaunt undead Edo-era farmer in a torn, faded kosode and straw sandals, grey-blue
  decaying skin, hunched forward, arms reaching, one sleeve burnt.
- **One accent: dim ember-orange eyes**, tying him to the Rider's hellfire curse. Rim light only, no
  glow field.
- **Not:** a samurai, a ninja, a western-style zombie in modern clothes, gore or exposed organs. No
  headband, plate or village symbol.

## 4. Prompt

Scaffold `spec.prompt_scaffolds.scaffolds.AI_AVATAR`, with the key swapped to magenta.

**Positive:**
`single undead villager character, full body, SUBJECT: a gaunt undead Edo-era farmer in a torn faded kosode and straw sandals, grey-blue decaying skin, hunched forward with both arms reaching, one sleeve burnt, dim ember-orange eyes, crisp pixel lineart, flat cel shading, limited palette, soft even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, at most one restrained glow accent as rim light on edges only, centered, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the magenta`

**Negative:**
`no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no aura, no halo, no light field, no glow disc, no magenta spill on the character, no multiple characters, no checkerboard background, no white or grey background, no gradient, no asset sheet, no grid, no labels, no franchise insignia, no headband, no gore, no exposed organs, no weapon, nothing resting on a surface`

**Reference (bytes attached individually):** `art/halloween_headless_rider/headless_rider_avatar.webp`,
**style only**. Not its subject, pose, horse or fire.

## 5. Intake

1. `python3 skills/producing-tnr-art/scripts/rawqc.py <raw> --scaffold hrh_zombie_avatar --record`
2. `python3 skills/producing-tnr-art/scripts/chroma.py <raw> avatar_hrh_zombie_villager.webp --target AI_AVATAR --key magenta --qc qc.png`, then look at the dark composite.
3. `python3 skills/producing-tnr-art/scripts/artpreflight.py avatar_hrh_zombie_villager.webp --type AI_AVATAR`, 0 errors.
4. Commit under `art/halloween_headless_rider/`; Fable builds the avatar edit from the push/262 read
   with an image pack (kit and items re-sent unchanged).
