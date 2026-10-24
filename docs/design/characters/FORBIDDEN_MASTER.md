# The Forbidden Master

- **Ruling:** RUL-2026-10-24-007 (director, 2026-10-24): one masked character for every Forbidden jutsu render; "the mask
  is the silhouette now".
- **Status:** design open. Round 1 is a model sheet (`docs/handoffs/FORBIDDEN_MASTER_MODEL_SHEET_SESSION_PROMPT.md`).
  Every design decision is the director's; this brief proposes.
- **Roles:** the art director makes the raws; Claude Code writes the briefs, processes and reviews.
- **Live-game requests/writes:** 0.

## 1. References (`art/characters/forbidden_master/refs/`)

| File | Role | What to take |
|---|---|---|
| `ref_fm_identity_tempest_cleave.webp` | **IDENTITY** | the masked fighter of the Tempest Cleave original: a fox (kitsune) mask, dark segmented armour, a white scarf, glowing eyes, power crackling from the hands, a storm-dark mood |
| `ref_fm_render_weapon_master_full.png` | **RENDERING GOAL** (character) | the full-body render: bold clean ink outlines, cel shading with painterly texture, a dynamic low lunge, torn cloth flying, a high-contrast limited palette, hard bright energy arcs |
| `ref_fm_render_weapon_master_icon_slash.png`, `..._icon_guard.png` | **RENDERING GOAL** (icon finish) | how the Weapon Master reads as a jutsu icon: the figure large and dark against a simple dark ground, one bright effect, the glowing eyes the focal point of the head |
| `ref_fm_render_weapon_master_old_icon.webp` | context | the older Weapon Master icon |

## 2. Who they are

The master of the arts the villages sealed away. Every Forbidden jutsu in the game is theirs. They should look like the
most dangerous person in any room: composed, powerful, unhurried, never flailing.

| | Proposal |
|---|---|
| **Build** | tall, broad-shouldered, lean and hard; mature adult proportions; slightly heroic scale (about 8 heads) |
| **The mask (the silhouette)** | a **kitsune-shaped mask** after Tempest Cleave's (pointed ears, a tapered snout), but **black**: matte or lacquered near-black, so from any distance the face is a dark shape, as the Weapon Master's void face was. Two **glowing eye slits** are its only light. Thin markings on it in the accent colour. The mask's outline (ears, snout) is the character's signature shape at 45 px |
| **Eyes** | white-hot by default; in a jutsu icon they may take that jutsu's energy colour (gold for Ethereal Rebirth, for example) |
| **Hair** | dark, long and wild, tied back high (shared shape language with the Weapon Master, so the two read as one family), streaming behind the mask |
| **Costume** | dark segmented armour over a black gi (Tempest Cleave), a long, heavy, tattered dark coat or half-cloak that flares in motion (imposing mass), bandaged forearms and shins (Weapon Master), a **white scarf** (Tempest Cleave) torn at the ends |
| **Accent** | one colour besides black and white. Proposal: **bone white + deep crimson** markings on the mask and the scarf's lining, so the character sits under any jutsu's palette (fire, lightning, water, light) without clashing, and stays distinct from the Weapon Master's bright red scarf |
| **Presence** | calm, braced, economical poses; power radiates from them rather than effort; the energy of each jutsu is what moves, not the master |

**How they differ from the Weapon Master** (same family, not the same person): a mask instead of a void face; a white
scarf instead of red; armour and a heavy coat instead of a light gi; no sword as a signature (each jutsu decides what
they hold).

## 3. Rules for every Forbidden jutsu render

1. The master is always the figure; the jutsu's own effect, palette and moment come from its original icon and its text
   (RUL-2026-10-24-003, -004). Element must match the jutsu (Ethereal Rebirth and Ethereal Nexus are non-elemental).
2. The mask is always on; the face is never shown.
3. Icon rules stand: the figure large and readable at 45 px, a calm dark ground, one brightest point, the badge corners
   clear, no text, runes or symbols, no franchise looks.
4. Same costume, mask, hair and build in every render (the model sheet is the reference attached to every brief).

## 4. Where they appear (the Forbidden jutsu, public read 2026-10-23)

| Jutsu | Id | Rank | Element | Live |
|---|---|---|---|---|
| Black Crow | `c-yTyBUJil8MzlAIHApUG` | D | Earth | yes |
| Dark World | `p4N7lt4QgQjLytzkXJTz9` | S | Lightning | yes |
| Dragon King's Impact | `FytS2iqFInf1go6WhOvUU` | S | Fire | yes |
| Ethereal Nexus | `iktsCP-RjIhlYlsTg-JTN` | S | None | yes |
| Ethereal Rebirth | `K0t6Z-Q4lau1jFt8Tkpot` | S | None | yes |
| Fury of The White Tiger | `QXE9J0fnu1t-DAGTGbaCX` | S | Wind | yes |
| Gaze into Yomi | `UXXs6CZ8NZNjLs9175yZ4` | S | Water | yes |
| Summoning: Momo | `_mTOi6z16b3PNyCSaKcs9` | S | none | yes |
| Forbidden Art: Black Sun Funeral | `-MW2e9hVW8rCagtqIAKzU` | S | Explosion, Scorch | hidden |
| Forbidden Art: Eclipse Nerve Sutra | `QLERxmHCk2XohG9aiNQ8P` | S | Shadow, Yin-Yang | hidden |
| Forbidden Art: Grave Lotus Detonation | `VPx4R9rWKxsx91kVCPgot` | S | Explosion, Fire | hidden |
| Forbidden Art: Soul Furnace Reversal | `TW3ESJVx6dQ5o-_-QXSMi` | S | Light, Yin-Yang | hidden |

## 5. Open decisions (the director's)

1. **The mask:** black kitsune (proposed), or another shape; round 1 shows three.
2. **The accent colour:** bone white + crimson (proposed), or another.
3. **Ethereal Rebirth:** its approved icon shows the white-haired warrior; under this ruling it is redrawn with the master
   (its round-4 prompt is paused). push/236 still carries the approved icon: ship it now and replace the icon later, or
   hold it for the master's version.
4. **"Our characters":** whether the Weapon Master's own renders are later redrawn with a mask too (rule 1 of the ruling).
5. **Tempest Cleave** (an Event jutsu, the identity source): keeps its own fox-masked fighter, or becomes the master too.

## 6. Acceptance for the model sheet

| # | Criterion |
|---|---|
| M1 | At 45 px the head reads as a masked ninja (the mask's outline and the two eye slits), not a face and not a void |
| M2 | Intimidating and imposing: the build, stance and coat give mass; calm, not frantic |
| M3 | The Weapon Master's rendering quality: clean ink outlines, cel shading, a limited high-contrast palette |
| M4 | The Tempest Cleave identity is recognisable: the kitsune mask shape, the armour, the white scarf |
| M5 | Clearly a different person from the Weapon Master, of the same family |
| M6 | No text, runes, symbols or franchise looks (no Naruto ANBU masks or insignia) |

## 7. Log

| Round | Date | What happened |
|---|---|---|
| 0 | 2026-10-24 | Director defines the character (RUL-2026-10-24-007); references saved; brief and round-1 model-sheet prompt written. |
