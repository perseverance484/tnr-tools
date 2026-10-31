# Art request: Patient Zero battle animations (Plague Bile + Infected Bite)

- **For:** the art director (Art Director role, then Image Production)
- **From:** Fable / Claude, at dauntless's request (2026-10-30)
- **Status:** PROPOSAL. Direction (sections 3 and 4) awaits director approval before any generation.
- **Event:** Zombie Outbreak (Vanquish the Horde battle pyramid `0U8N6218b095-TQbWlCep`).
- **Boss:** Patient Zero `Pe5J6m1sc1IMpF2HF6Rby` (hidden, level 30 CHUNIN, push/336).
- **Jutsu (both hidden, AI-only, created by push/335):**
  - **Plague Bile** `2lWcedG9Dw528HGO4eI6R`: range 4, SINGLE; damage 40, poison 20% for 2 rounds, heal cut 30% for 2 rounds.
  - **Infected Bite** `HrNA9mD5WW2uaCdkq7Iao`: range 2, SINGLE; damage 60, wound 15% for 2 rounds.
- **Style reference (attach, STYLE ONLY):** `art/halloween_zombie_outbreak/patient_zero_avatar.webp`. Its palette is
  near-black and plum cloth, crimson sash and scarf, grey-green rotting skin, glowing red eyes, and bone teeth.
- **Roles:** the art director paints transparent layers. Claude Code animates them by script (the Hellfire Harvest /
  Skyglass route: Pillow compositing, 50 px frames), previews them on a hex board and builds the manifest.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`, one layer per fresh session. Spec:
  `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `ANIMATION`.
- **Live-game requests/writes:** 0.

## 1. Why these two

Patient Zero's three signature jutsu were created with every animation and sound slot empty, so his big moves
currently play with no visual at all. His other three moves (Warrior's Poise, Heavy Cut, Recoil Slam) are shared pool
jutsu used by other enemies and must not be re-skinned.

- **Plague Bile** is the boss's signature and the image the event brief asked for ("spitting zombie bile"). Its poison
  makes the infection visibly linger.
- **Infected Bite** is his heaviest single hit and the most memorable moment of the fight.

The third signature, **Festering Claws** `ydcbW8BIAKyYxHpnz7SDw`, reuses Skyglass's rot-claw strip (dauntless,
2026-10-30). The strip is `art/skyglass_boss_fx/exports/anim_rot_claw_v1.webp`, drawn for Splintered Grasp. It has
never been uploaded, so this event's manifest creates it as a shared hidden ANIMATION asset that Skyglass can reuse
later. It needs no new art and goes on Festering Claws' damage effect only.

## 2. How the game draws it (spec `ANIMATION`; Skyglass and Hellfire measurements)

- **Appear (`appearAnimation`):** a vertical strip played ONCE on the target's hex when the effect lands. The CDN
  serves it at 50 px, so frames are authored natively at 50 x 50.
- **Placement:**
  - The hex covers about 36 x 18 px of the frame (flat-topped, 2:1).
  - The strip draws OVER the characters, so a one-shot hit can be bold.
  - three.js filters linearly, so the RGB under transparent pixels is filled from the nearest drawn pixel, and every
    frame keeps a 1 px clear margin.
- **Loop (`staticAnimation`):** a strip that loops on the hex for the effect's duration. It sits over the fighter for
  2 rounds, so it must stay small, low and dull, or it buries the target (Aura of Despair needed a v2 for this).
- **Hard pixels:** alpha is stepped (0 / 130 / 255), with no gradients, no anti-aliasing and no bloom.
- **Slot placement** (the Hellfire lesson: never stack the same art on every effect):
  - The appear animation and sound go on the **damage** effect only.
  - Plague Bile's loop goes on the **poison** effect only.
  - The heal-cut and wound effects carry nothing.

## 3. Direction (director to approve)

**Shared rules**
- Crisp pixel rendering matching the Patient Zero avatar, dark one-pixel outlines, flat cel steps.
- Glow is edge light only, never a painted disc or halo.
- No text, runes, symbols or franchise insignia.
- The two moves must never read as the same attack. Bile is green, wet and splashing. The bite is red, bone and
  snapping.

**Palette**

| Role | Colours |
|---|---|
| Rot black | `#120c10` |
| Plum shadow | `#3a1f33` |
| Crimson | `#c3141b` |
| Blood dark | `#6e0d12` |
| Skin grey-green | `#8a9a7a` |
| Bone | `#d9cfb4` |
| Eye glow | `#ff3b2f` |
| Bile (Plague Bile ONLY) | `#3d4a12`, `#6b8f1e`, `#a8c23a`, highlight `#d8e86a` |

### 3a. Plague Bile, "Plague Spatter"

**Appear** (about 10 frames, about 0.5 s):
1. A wet glob of bile arcs in from the upper left, with a dark core, a sickly green body and a crimson-tinged rim.
2. It bursts on the hex into a ragged splatter with droplets flying outward.
3. A brief curl of greenish fume rises.
4. The splatter shrinks into a small puddle that hands over to the loop.

**Loop "Festering Pool"** (6 frames, plays for the 2 rounds of poison):
- A small, low, dull bile puddle on the hex.
- One or two bubbles swell and pop.
- A faint fume wisp rises.
- It stays dark and low-contrast, and never covers the fighter's face.

### 3b. Infected Bite, "Death Snap"

**Appear** (about 9 frames, about 0.45 s):
1. A spectral zombie jaw opens over the target, with rotten bone teeth, grey-green gums and torn lips.
2. Two red eye-glints flicker above it, as the boss's mark.
3. The jaw SNAPS shut, with a hard 1-frame impact and a slight frame shake.
4. A crimson blood spray bursts from the bite point.
5. A few dark droplets fall, then everything fades out.

No loop: the wound needs no lingering art.

## 4. Deliverables (each on a fully transparent canvas; one element per image, never a sheet)

| Layer | What | Size |
|---|---|---|
| **PB1 BILE GLOB** | one wet glob of zombie bile in flight, a teardrop with a trailing tail, dark core, green body, crimson-tinged rim, glossy highlight pixels | 1254 x 1254 |
| **PB2 SPLATTER** | a flat ragged bile splatter burst seen slightly from above, irregular arms and a few detached droplets | 1254 x 1254 |
| **PB3 BUBBLES** | 6 to 8 separate bile bubbles, mixed sizes (40 to 160 px), two of them mid-pop, spaced apart | 1254 x 1254 |
| **PB4 FUME** | 3 to 4 separate thin wisps of sickly green-grey fume, curling upward | 1254 x 1254 |
| **IB1 UPPER JAW** | a spectral zombie upper jaw alone, front view, rotten uneven bone teeth, grey-green gum, ragged lip edge, open | 1254 x 1254 |
| **IB2 LOWER JAW** | the matching lower jaw alone, same style and scale as IB1 | 1254 x 1254 |
| **IB3 BLOOD SPRAY** | a burst of crimson blood spray radiating from one point, with a few heavier drops | 1254 x 1254 |
| **IB4 EYE GLINTS** | two small glowing red eye-glints with a short hard flare, light only, no face or skull | 1254 x 1254 |

Rules:
- Real transparency, with no grey or tinted backing, no dark fringe and no checkerboard.
- If transparency is unavailable, use the **magenta** key only. Lime is forbidden here because bile is green.
- Two wrong-subject results in one session: close it and start clean. Do not lengthen the prompt.

## 5. Intake (Claude Code)

1. Raws go to `art/halloween_zombie_outbreak/fx/raws/`, with raw QC per layer.
2. Composite the strips by script, with 50 px frames and 50 ms per frame:
   - `anim_pz_plague_spatter.webp` (appear)
   - `anim_pz_festering_pool.webp` (loop)
   - `anim_pz_death_snap.webp` (appear)
   - `anim_rot_claw_v1.webp` (appear, reused as is for Festering Claws)
   Each must pass `artpreflight.py --type ANIMATION`.
3. Preview:
   - A GIF of each strip on a hex board over the pyramid background, with a fighter on the target hex.
   - For the loop, the full 2-round hold, to prove it does not bury the fighter.
4. Manifest:
   - Four hidden ANIMATION gameAsset creates in folder `Halloween2026` (three new strips plus the reused rot claw).
   - Then unequip Patient Zero, edit the three jutsu, and re-equip (law 18/60, two runs).
   - Sound candidates (live SFX assets, to confirm by ear): WaterSFX `NThXOSKNDXPwNnGxDtH0Z` for Plague Bile, and
     Growler `yIwD2VXIm-x4EF3O8LN8E` for Infected Bite.

## 6. Director decisions

1. The two directions as described (section 3), including the Festering Pool loop.
2. The bile-green accent, used on Plague Bile only.
3. The sound picks (section 5.4).
4. ~~Festering Claws~~ DECIDED 2026-10-30: reuse Skyglass's rot claw (section 1).
