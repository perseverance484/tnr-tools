# Jutsu icons: visual design deep dive

- **Asked by the director, 2026-10-24:** "Do a deep dive on visual design and best possible art direction for the icons."
- **Builds on:** RUL-2026-10-24-001 (icons depict the move) and its people decision ("show people wherever the move needs them").
- **Evidence used:**
  1. our own 51 reverted icons measured at phone size against the director's scores;
  2. how the game draws icons and the game's own art guide (game source `studie-tech/theninjarpg`, local checkout at
     `a744c04`; the files cited are unchanged since the pinned `107d7a8` except an unrelated config line);
  3. a research brief on how other games design ability icons.
- **Status:** analysis and proposed art direction. Art direction is the director's (CLAUDE.md section 10); section 8 lists
  the choices to make. Live-game requests/writes: 0.

## 1. Findings in brief

1. **Shape carries the read, not detail or colour.** At 45 px, our icons that became full-frame texture (all of Blue Blade
   Eyes, Aerathiel and Vaporia) blur into blobs. The originals with a person keep a readable human shape. The clearest
   single icon in the set is the original **Blast Shield**: a dark ninja against a bright dome.
2. **The icons the director scored 10 are darker and calmer.** Mean brightness at 45 px is 0.23 for the 10/10 icons and
   0.35 for the 0–4 icons; contrast spread is 0.21 against 0.28. Glow and brightness everywhere hurt.
3. **Simple pixel measurements do not predict the scores well** (the strongest correlation is about 0.4). The scores
   follow the *subject*: a concrete thing or action scores well; an abstract effect does not. That is the director's
   conclusion, and the data backs it.
4. **Other games converge on the same rules.** A unique silhouette per icon; value over hue; low detail; quiet
   backgrounds; show the doer at the moment of the move, cropped to the telling detail. Blizzard abandoned painterly
   Diablo IV icons because they "don't come across as well... in the UI", and toned their backgrounds down. Riot redrew
   Caitlyn's ultimate to show "the champion's eye behind her rifle scope" instead of the shot.
5. **Our "pixel art" was not real pixel art.** Image models paint pseudo-pixels at mixed sizes ("mixels") with
   bloated palettes. That likely explains much of "doesn't read as premium pixel art".
6. **The game shrinks icons smoothly.** The browser scales the 256 px file to 45 px with smoothing (no `pixelated`), so
   anything thinner than about 6 px at 256 vanishes on a phone. Only two to four big value shapes survive.
7. **The game's own art guide fits the old icons, not ours.** It asks for retro 32-bit pixel art, hard pixel edges, no
   gradients or blur, rim lighting, dynamic ninja action poses. Its icon line, though, says "energy bursts, chakra seals,
   elemental FX", which is the abstract direction the director has now ruled out.

## 2. Our icons at 45 px

`thumb_test_45px.png` shows every reverted icon at the real phone size, ours and the original, each with a blurred grey copy
(the silhouette test), sorted by score. `analyze_icons.py` → `analysis_45px.json` holds the measurements.

| Observation | Examples |
|---|---|
| **One bold concrete shape survives** blurring and scored well | Blazing Fang Strike (an S-shaped dragon), Celestial Dew (a crescent), Crimson Tithe (a chalice), Reaper's Embrace (a scythe arc), Prism (one diagonal beam) |
| **Full-frame texture turns into fog** | Ice Shackles, Quintessential Flake, Icebound Might, Glacial Volley (ours); Drowning Strike, Azure Dragon Palm; Death's March |
| **Centred radial shapes all look alike** | Abyss of Shadows, Atomic Shield, Tempest Cleave, Ethereal Nexus, Ring of Spilled Blood |
| **A figure survives when it is big and dark against bright energy** | Blast Shield, Inferno Cataclysm, Poisonous Senbon, Venomous Phobia (originals) |
| **A figure fails when it is small or lost in a scene** | Subaku Palace, Ethereal Rebirth, Celestial Dew (originals) |

Measured means at 45 px (0–1 scale):

| Measure | Ours, 10/10 | Ours, 0–4 | Originals |
|---|---|---|---|
| Mean brightness | 0.23 | 0.35 | 0.25 |
| Contrast spread | 0.21 | 0.28 | 0.19 |
| Edge density (busyness) | 0.30 | 0.37 | 0.31 |

Caveat: 51 icons in families that were scored together, so family effects mix in (all BEE scored 10). Read these as
supporting evidence, not proof.

## 3. How the game shows an icon

| Fact | Source (game) | Consequence |
|---|---|---|
| Tiles: 45 px mobile bar, 70 px desktop bar, 112 px default grid; rounded-xl corners and a 2 px border | `combat/page.tsx`, `CombatActions.tsx`, `ContentImage.tsx` | judge at 45 px; keep the corners free |
| Lists cover the bottom-left and bottom-right corners with 28 px badges | `CombatActions.tsx` | focal mass in the upper and central 60–70% |
| Images are served unoptimised and scaled by the browser with default smoothing; no `image-rendering: pixelated` anywhere | `next.config.mjs` (`images.unoptimized: true`), no `pixelated` in `app/src` | 256 → 45 px is ×0.18: a 6 px detail at 256 (about 28 px in a 1254 px raw) becomes under one screen pixel |

## 4. The game's own art guide

`app/src/libs/imagePrompts.ts` is the prompt the game uses for its own generated art.

- **Rendering:** "Retro 32-bit pixel art... Hard pixel edges, stylized shading, no smoothing... Sharp contrast, rim
  lighting, dramatic angles... Avoid: Gradients, blurs, pastel tones, painterly effects, photorealism."
- **Characters:** "mature human proportions, dynamic ninja action pose... strong silhouette with cloak or scarf or weapon";
  "Twisted action angles: jumping, casting, charging, spinning; limbs foreshortened for depth; framing objects: scarf,
  blade, cape, aura."
- **Jutsu icons:** "Perspective: Centered or angled. Style: Energy bursts, chakra seals, elemental FX. Examples: fireball,
  wind shuriken, cursed mask, chakra rune."
- **Element FX table:** fire "jagged orange flame, ash pixel trail, burn ring"; water "wave ripple arcs, flowing blue
  pixels, droplet shine"; wind "air slice rings, cloth motion blur (pixelated), sand streaks"; shadow "black aura, smoke
  claws"; chakra "glowing sigils, ripple rings, aura flames"; lightning "blue surge veins, flash glow core, forked edges".

**Use:** the rendering, character and FX lines as the house style (the old icons players miss follow them). **Do not use**
the jutsu-icon line; RUL-2026-10-24-001 replaces it for our work. Note for the director: anyone generating icons with the
game's built-in prompt is still steered towards abstract icons; changing that is a game-repository matter, outside this repo.

## 5. What other games do (research brief, summarised)

Sources are listed in section 9. Points marked *observed* describe shipped icons rather than a published statement.

| Principle | Evidence |
|---|---|
| Unique silhouette per icon | Game Developer: "easy to distinguish from all others by its shape alone"; Riot: silhouette is "the single most important thing" for recognition |
| Value over hue | Valve's Dota 2 guidance: contrast and value are critical; "patches of small detail... become hard to read" |
| Low detail | NN/g: "Intricate details are difficult to distinguish at smaller sizes"; Game Developer: more elements, less contrast, slower identification |
| Quiet backgrounds | Blizzard toned down Diablo IV icon backgrounds after painterly icons read badly in the UI |
| Show the doer, cropped to the telling detail | Riot's Caitlyn ultimate: the eye behind the scope, not the shot; *observed*: Darkest Dungeon (the hero performing the skill, tightly cropped, near-monochrome on dark), Dota 2 and League (hero, weapon or summon mid-action), Naruto mobile games (the user, the hand seal or the summon) |
| Attention matches importance | Riot: "the amount of attention an ability grabs should match its level of importance"; flashiness "comes at a cost" |
| Family = shared rendering; individual = shape | "One scale, one palette, one light"; Guild Wars 2 colours skills by profession or type; "avoid similar shapes for different icons" |
| Real pixel art | Model output has an uneven grid, bleeding pseudo-pixels and huge palettes; fix by snapping to one grid, quantising the palette and cleaning strays (Pixel Logic: never mix resolutions) |
| Test at the smallest size | "Design at the largest size, judge at the smallest"; silhouette fill, blur, greyscale and squint tests; NN/g's five-second meaning test |

## 6. Proposed art direction

### 6.1 The formula

**One actor, one action, one moment, two to four big shapes, one light.**

1. **Subject:** who does what to whom, from the battle text (RUL-2026-10-24-001). At most two actors plus one prop or effect.
2. **Crop:** the smallest slice that still tells the move: hands forming the seal; the fist meeting the target; the ninja
   springing from the log; a small user under a huge summon.
3. **Silhouette:** design it first, as flat black on grey. It must read at 32 px with no interior detail.
4. **Values:** three bands. A dark, low-detail ground; a mid or dark body; one brightest accent on the focal point.
5. **Backlight:** the most readable arrangement in our data is a **dark figure against the brightest energy** (the original
   Blast Shield and Inferno Cataclysm). Use it for most figure icons.
6. **Line of action:** off-centre and diagonal, with exaggerated, foreshortened poses (the game's guide: "twisted action
   angles"). Avoid centred radial bursts and swirls.
7. **Glow:** one source per icon, where the move's energy is. No ambient halos.
8. **Background:** flat or two-tone, tinted by the family; no scenery clutter, particle fields or texture.
9. **Rendering:** the game's house style: retro 32-bit pixel art, hard edges, no gradients or blur, rim light from top-left,
   exterior outlines (a darker shade of the object, black where contrast needs it), 16–24 colours per icon, no dithering
   noise.
10. **Safe area:** the focal mass in the upper and central 60–70%; bottom corners empty.

### 6.2 Composition archetypes

Every move falls into one of seven layouts. Giving siblings different archetypes keeps a family distinct at 45 px.

| Code | Archetype | Layout | Fits |
|---|---|---|---|
| **A** | Strike | user (or their fist/weapon) entering from one side, target on the other, impact flash at the contact point; diagonal | punches, palms, blade strikes |
| **B** | Projectile | thrower small in a lower corner or out of frame; the projectile big on a diagonal, about to hit | senbon, beams, lances, chains, thrown chakra |
| **C** | Self-power | figure centred and braced; the effect forming on or around the body; backlit | armour, shields, buffs, transformations |
| **D** | Affliction | target silhouette afflicted; the source from above or one side | debuffs, curses, drains, freezes |
| **E** | Summon | small user, huge creature looming behind; scale contrast is the message | summons, guardian creatures |
| **F** | Eruption | low camera; the effect erupting from the ground around or in front of the user | area jutsu, ground blasts, gates |
| **G** | Movement | figure in motion with a trail from where they were; the origin visible | dashes, substitutions, surfing |

### 6.3 Assignments

| Family | Jutsu → archetype | Distinctness check |
|---|---|---|
| Event | Abyss of Shadows **D**, Drops of Renewal **C**, Earthen Bastion **C**, Hollow Veil **D**, Subaku Palace **F**, Tempest Cleave **F** | the two Cs differ by element and shape (rain spiral vs stone plates); the two Ds by source (black sun above vs shroud draped) |
| Forbidden | Ethereal Nexus **A/B**, Ethereal Rebirth **C** | outward strike vs inward transformation |
| Normal | Poisonous Senbon **B**, Searing Might **C**, Soul Shackles **B**, Venomous Phobia. **D** | the two Bs: needles on a diagonal vs chains straight across |
| Bakuhatsu | Blast Shield **C**, Charge 4 Explosion **F**, Howitzer Crash **G→A**, Inferno Cataclysm **F**, Kinetic Nova **B** | the two Fs: a low horizontal chain of small blasts vs one tall column |
| Aerathiel | Atomic Shield **C**, Death's March **D**, Decaying Touch **A**, Particle Cannon **B**, Windshear Decay **B** | five layouts for the five former swirls; the two Bs: one beam through a triangle vs many parallel slashes |
| Vaporia | Azure Dragon Palm **E/A**, Drowning Strike **A**, Liquid Ember Shell **C**, Scorch Break **A**, Surfing Strike **G** | the two As must differ: Drowning Strike is a close-up of a water fist meeting a face; Scorch Break is a burning fist breaking a wall of water |
| Blue Blade Eyes | Arctic Frost **C** (the blade icing in the hand), Blade Resonance **A**, Blue Crimson **G**, Glacial Volley **B**, Ice Shackles **D**, Icebound Might **E**, Quintessential Flake **F**, Sapphire Command **D** | the two Ds: encased from the ground up (vertical) vs a wave passing through (horizontal) |

### 6.4 Pixel rendering and processing (Claude Code)

The art director returns raws; Claude Code processes them (RUL-2026-10-23-008, amendment 1).

1. **Snap to a true grid:** detect the pseudo-pixel size, resample to one grid with nearest-neighbour or dominant colour,
   remove stray pixels.
2. **Quantise** to 16–24 colours per icon (the family palette plus accents).
3. **Export** 256 px lossless WebP; run `artpreflight --type JUTSU_ICON`.
4. **Gate at real size** (section 7).

Steps 1–2 need a processing script that does not exist in the repository yet. That is tooling work (Lane A: its own branch,
review and handoff), proposed in section 8.

## 7. Acceptance gates for every icon

| Gate | Test | Pass |
|---|---|---|
| G1 Name test | show the 45 px icon without its name | a viewer says who does what in about five seconds |
| G2 Silhouette | blurred greyscale copy at 45 px | one dominant shape, recognisable |
| G3 Family lineup | the whole family side by side at 45 px | no two share a silhouette or layout |
| G4 Bar test | in a mobile bar between kept icons (`preview_in_context.py`) | reads, and does not shout louder than its importance |
| G5 Safe area | 112 px tile with level badge | focal mass clear of the bottom corners |
| G6 Pixel integrity | 256 px master at 100% and 400% | one grid, no mixels, no gradient banding, 24 colours or fewer |
| G7 Backgrounds | on dark, mid and light panels | the subject separates on all three |

Claude Code runs G2–G7 automatically on intake and reports G1 to the director with the sheet.

## 8. Choices for the director

| # | Choice | Options | Recommendation |
|---|---|---|---|
| C1 | **Pixel grid density** | a) about 32 art pixels across (each one at least 1 screen pixel at 45 px; boldest, least detail); b) about 48–64 across (richer at 112 px, softer on mobile); c) b) plus a hand-tuned small version | **b)**, judged by gates G1 and G2 at 45 px. The game shows one file at every size, so c) would need game support. |
| C2 | **Processing tool** | build a snap-and-quantise script (Lane A, reviewed) / process by hand per icon | build it: 35 icons in one batch, and it makes "real pixel art" repeatable |
| C3 | **Backlit silhouette as the house look for figure icons** | adopt / case by case | adopt for archetypes A, C, E and G |
| C4 | **The game's built-in icon prompt** still asks for abstract icons | raise it with the game team / leave it | raise it, so new icons made in-game follow the same rule |

## 9. Sources (research brief)

- Game Developer, *Icon design rules you should know*: https://www.gamedeveloper.com/design/icon-design-rules-you-should-know
- Riot, *Clarity in League*: https://www.leagueoflegends.com/en-gb/news/dev/clarity-in-league/
- Riot ability-icon updates: https://riftfeed.gg/champions/lol-outdated-champions-to-receive-small-yet-meaningful-updates ;
  Caitlyn icons: https://dotesports.com/league-of-legends/news/riot-changes-the-icons-of-various-items-and-caitlyns-abilities-on-league-pbe
- Blizzard, Diablo IV quarterly update (icons): https://news.blizzard.com/en-us/diablo4/23308274/diablo-iv-quarterly-update-february-2020
- Valve guidance as quoted on Polycount: https://polycount.com/discussion/comment/1888930/
- NN/g, *Icon usability*: https://www.nngroup.com/articles/icon-usability/
- Made Good Designs on in-game icons: https://madegooddesigns.com/?p=5494
- Lospec, pixel-art outlines: https://lospec.com/articles/pixel-art-outlines and https://lospec.com/articles/pixel-art-outlines-part-2-using-color
- PixelJoint tutorial: https://pixeljoint.com/forum/forum_posts.asp?TID=11299
- Wayline pixel-art and UI lessons: https://www.wayline.io/learn/pixel-art/4 and https://www.wayline.io/learn/game-ui-art/4
- AI pixel-art cleanup: https://dev.to/jenissimo/how-to-tame-your-ai-pixel-art-3pk5 ; https://www.spritecook.ai/blog/why-ai-cant-match-pixel-art-resolution
- Integer scaling: https://tanalin.com/en/articles/integer-scaling/
- Readability tests: https://gamineai.com/blog/creating-game-icons-and-logos-design-principles-game-branding ; https://bugnet.io/blog/readable-game-art-why-clarity-beats-detail
- Guild Wars 2 skill icons: https://wiki.guildwars2.com/wiki/Skill_icon

The brief found no first-party write-ups on ability icons from Blizzard (WoW), Square Enix, Valve, Supergiant, Red Hook,
Motion Twin, Mega Crit or the Naruto mobile studios; observations of their icons are noted as such.
