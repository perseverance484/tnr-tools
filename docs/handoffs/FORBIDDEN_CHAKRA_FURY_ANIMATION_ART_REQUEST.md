# Art request: Forbidden Chakra Fury, the fury burst and its scorched ground

- **For:** the art director (visual partner).
- **From:** Claude Code, at dauntless's request (2026-11-16): "a high quality animation and ground effect for Forbidden
  Chakra Fury... No balance changes. We should be able to attach the effect to the recoil tag itself as the animation and
  ground tiles... animate the forbidden chakra fury body explosion."
- **Status:** brief. Art direction and acceptance are the director's (CLAUDE.md section 10).
- **Live-game requests/writes:** reads only (`jutsu.getAll`, `gameAsset.get` x3, 2026-11-16). No writes.
- **Source basis:** studie-tech/TheNinjaRPG at `f6a51fac5` (2026-11-15), Pixi renderer:
  `src/libs/rendering/scenes/combatEffects.ts`, `src/libs/rendering/animation.ts`,
  `src/libs/rendering/primitives/animation.ts`, `src/libs/combat/actions.ts`.

## 1. The jutsu today (`Lg_thN-MB8FRAr_Agf9tn`)

Bloodline (Yaketsuku Netsu) Bukijutsu, Chunin, target **Ground**, method **Area: spiral**, range 4, cooldown 7.

| Effect | Mechanics (unchanged) | Art today |
|---|---|---|
| 1. damage | power 35 (+0.4/lvl), rounds 0, formula, Speed + Strength | appear `X32FgBGqES-eDreOlVb6X` "zap_B_small_red" (stock, 8 frames x 50 ms, S3-hosted), appear SFX `yGzPWg1cLQc6dYd1EpCsl` |
| 2. recoil | 30% (+0.4/lvl), rounds 2, percentage | appear `9_cyb-wLxSYQA_jMaNtwR` "earth_spikes_small_red" (stock, 32 x 50 ms); ground `y1hrYiCnjmJM-wK5IIWHa` "Shadow field" (STATIC, folder Fields) |

Icon: a swordsman crouched in a storm of **violet lightning**, a **red scarf** streaming. The stock art is red and
earthen; nothing matches.

## 2. Where the art plays (why the recoil tag carries it)

- With target INHERIT, every effect of a Ground jutsu is placed **on each tile of the spiral** (`actions.ts` ~1100), so
  the recoil sits on every struck tile for its 2 rounds.
- Per effect the renderer draws: **appear** once at cast, **static** looping while the effect lasts, **disappear** once
  when it ends, and the **ground image** (`staticAssetPath`) flat under the tile while it lasts (`combatEffects.ts`).
- The jutsu has no effect on the caster, so there is no self cast clip; the moment to own is the burst on the tiles.
- Clip size = tile height x the effect's `animationScale` (1 to 3); **one scale per effect**, shared by its appear,
  static and disappear clips. The ground image is always one tile, unscaled.
- No mechanic changes: the recoil's power, rounds and targeting stay exactly as they are; only its art fields change.

## 3. The brief

**Concept:** the fury lashing out. Chakra tears out of the user's body in a violent violet storm that strikes every
enemy in reach, then leaves the ground scorched and crackling for two rounds.

**Palette (from the icon):** violet lightning `#9b4dff` to `#c58bff`, white-lilac core `#f4eaff`, deep indigo shadow
`#24093f`, and a **sparing** crimson accent `#d11f35` (the scarf; a streak, never a wash). Non-elemental read: this is raw
chakra, not fire.

### A. Fury Burst (recoil **appear**) - the hero clip
About 1.0 s: **24 frames at 42 ms**. Planned scale **1.75** (struck tiles overlap into one storm).

| Beat | Frames | What happens |
|---|---|---|
| 1. Draw-in | 1-3 | violet motes and thin arcs rush inward to a white-lilac point; a brief darkening |
| 2. Detonation | 4-7 | the point bursts: a hard shockwave ring and 5-7 forked lightning bolts lash outward in every direction |
| 3. The lash | 6-14 | chakra whips like blade-strokes across the burst, one crimson streak cutting through, arcs crawling along the ground |
| 4. Scorch | 12-18 | the ground under it cracks and flares violet (hands off to the ground image), arcs snap and settle |
| 5. Embers | 18-24 | the storm breaks into rising violet embers and dissolves (dissolve, never a grey fade) |

### B. Scorched ground (recoil **ground image**, STATIC)
One tile: charred, cracked earth with **violet chakra veins glowing in the cracks**, a few faint embers. Seen from the
battlefield's slight top-down angle. **Soft transparent edges** so it sits on grass, sand or snow; the footprint fits a
hex tile (no square corners). Readable at tile size (about 50 px in battle).

### C. Fade (recoil **disappear**)
About 0.6 s: **12 frames at 50 ms**, drawn small and low in the frame (the scale is shared with A): the veins flicker,
two or three last arcs snap between cracks, sparks rise and wink out.

### D. Optional: crackle loop (recoil **static**)
12 frames looping at 60 ms, small and low in the frame: little arcs hopping between the cracks while the field lasts.
Include only if it reads cleanly over B; skip it if it competes.

**Damage effect (effect 1):** its stock zap would fire on the same tiles at the same moment. Proposed: clear its appear
animation so the Fury Burst plays alone; keep its sound. (Art only; the damage is unchanged.)

## 4. Deliverables and format

- Painted key poses or layers on a 1254 px canvas, as the earlier animation requests did; Claude Code assembles the
  frames by script (`art/jutsu_icons/chakra_overflow/animation/build_strip.py` pattern) and previews them on dark, mid
  and bright battle ground at 1.75x before anything is uploaded.
- Final clips: **one vertical strip** (one column, square frames, top to bottom), lossless WebP with real transparency,
  **under 460,800 bytes** per strip, frames at least 128 px (content lists show 112 px).
- Ground image: transparent WebP, square canvas, tile-sized subject.
- No text, no figures, no symbols. Premium TNR finish matching the icon.

## 5. Checks before the live edit

1. **Sharpness probe (hidden, before upload of finals):** the renderer fetches clip sheets at a 50 px-wide rendition
   (`createClipTextures`, rendition default 50). Per our art notes (`processing.md` laws 79 and 84) a link with a file
   extension is resized by the CDN while an extensionless key is served whole. Upload one test strip hidden, read the
   delivered size the way job 589 checked the Mother's clips, and size the finals to what players actually receive.
2. **Preview on the director's screen** (Duet or a practice battle) before the edit goes live.
3. **The live edit (separate job, director go):** a new hidden asset per clip and the ground image, unhidden after
   upload (law 16); then one `jutsu.update` of the full record changing only effect 2's `appearAnimation`,
   `staticAssetPath`, `disappearAnimation` (and `staticAnimation` if D ships) plus `animationScale` 1.75, and effect 1's
   `appearAnimation` cleared if approved. Read back afterwards. This jutsu is a player bloodline jutsu, not an AI's, so
   law 18 does not apply; nothing hidden is saved onto it.

## 6. Assembly result (2026-11-16)

Sources received (`art/jutsu_icons/forbidden_chakra_fury/animation/raws/`, art director handoff). Assembled by
`build_strips.py`: burst 24 frames x 42 ms, fade 12 x 50 ms, crackle loop 12 x 60 ms (128 px, lossless; 323 KB, 17 KB,
3 KB), ground image cropped to its painted footprint at its own aspect (the renderer stretches it to the tile's width x
height).

**Scale changed to 3.0.** The game-geometry board (`--board`, Headless Rider `fxkit` layout: flat hexes squashed 2:1)
shows that a clip is sized from the tile's *height*, half its width: at 1.75 each burst is narrower than its tile and the
spiral reads as separate columns; at 3.0 the bursts merge into one storm. Previews: `preview/fcf_board_light_stills.png`
(1.75 vs 3.0), `preview/fcf_preview_frames.png`.
