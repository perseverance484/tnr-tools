# Art request: Hellfire Harvest field animation layers

- **For:** the art director (Art Director role, then Image Production)
- **From:** Fable / Claude, at dauntless's request (2026-10-26)
- **Status:** DIRECTOR-APPROVED (2026-10-26). Section 6 choices are settled; each layer still requires individual visual acceptance. Phase 2 smoulder is deferred.
- **Jutsu:** Hellfire Harvest `XVJb8MfFvIKe4GOgBaqXO`, the Headless Rider's (`eaMN5CfciNlxfezSKemJ6`) signature: target
  GROUND, method ALL, every tile of the field; damage 25 Fire, recoil 60% and heal cut 60% for 3 rounds, enemies only
  (push/285, push/287).
- **Style reference (attach, style only):** `art/halloween_headless_rider/headless_rider_avatar.webp` (the Rider:
  near-black, hellfire orange-red, bone, jack-o-lantern head). Scene palette: `headless_rider_horror_04_river.webp`.
- **Roles:** the art director paints transparent layers; Claude Code animates them by script (the Celestial Dew /
  Ethereal Rebirth route: `build_strip.py`, Pillow), previews them in a battle and builds the manifests.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`, one layer per fresh session. Spec:
  `skills/producing-tnr-art/data/25x_DATA_art_spec.json` targets `STATIC` and `ANIMATION`.
- **Live-game requests/writes:** 0.

## 1. What it uses now, and why it is replaced

| Slot | Current asset | Problem |
|---|---|---|
| static tile (`staticAssetPath`) | "Shadow field" `y1hrYiCnjmJM-wK5IIWHa`, 256 px still, 6.8 KB | generic dark wash, not fire or the Rider; on both lasting effects, so every tile stacks two copies |
| appear (`appearAnimation`) | Black Thorn Rose's `zRK4rRgCRjoWlyQj0gsNw` | another jutsu's vine art; on all three effects, so it plays three times per tile |
| appear sound (`appearSfx`) | `4iG_WpgEmPGUzHn8z129r` "Heal" | a healing chime on a fire attack, three times over |

The slot clean-up ships with the art manifest (director, 2026-10-26): appear animation and sound on the **damage** effect
only, static tile on the **recoil** effect only, sound swapped to **FireSFX** `9-b8hbTXA019dgn8yyr3j`.

## 2. How the game draws it (TheNinjaRPG 58801f9, `libs/threejs/combat.ts` 610-680, `libs/combat/process.ts` 1644)

- **Static tile:** one still sprite stretched to each tile's hex box, on **every tile** for the 3 rounds. The whole board
  is covered, so it must be low-contrast or it buries the fighters, and neighbouring tiles must blend into one field.
- **Appear animation:** a vertical frame strip played once at `EFFECT_ANIMATION_SIZE` = **50 px**, centred on each
  tile, **on every tile at the same moment**. Read together, it is one swing across the whole field.
- **Optional looping static (`staticAnimation`):** a strip that loops on every tile for the 3 rounds, layered over the
  still. Proposed as phase 2.

## 3. Direction (director-approved 2026-10-26)

**Palette:** char black `#0d0908`, ember brown `#3a1a10`, hellfire red `#c3141b`, pumpkin orange `#ff6a1a`, flame gold
`#ffb347`, ash grey `#6d6158`. One accent family (orange to gold); no blue, green or purple.

**Static tile "Harvest Scorch":** charred, cracked earth seen from above; thin ember-orange fissures glow in the cracks;
a faint scorched crescent where the scythe passed; a few ash flecks. Content inside the inscribed circle, edges fading to
transparent so tiles merge. Mostly dark: the fissures are the only bright pixels.

**Appear animation "Harvest Swing"** (~10 frames, ~0.4 s):
1. A burning scythe blade sweeps across the tile, left to right.
2. The cut leaves a blazing crescent slash that ignites the ground.
3. Flames burst upward: pumpkin-orange core, red edges, black smoke.
4. A jack-o-lantern grin flickers in the smoke for two frames (the Rider's mark).
5. It collapses into embers that settle onto the scorch tile.

**Phase 2 loop "Smoulder"** (6 frames): the fissures pulse and a few embers rise, so the field visibly burns for the 3
rounds.

## 4. Deliverables (each on a fully transparent canvas; nothing else on it)

| Layer | What | Size |
|---|---|---|
| **T1 SCORCH** | the static tile: charred cracked earth from above, glowing ember fissures, a faint scorched crescent, ash flecks; edges fade to clear | 1024 x 1024 |
| **B1 SCYTHE BLADE** | the Rider's scythe blade alone (no handle needed past the curve), curved edge wreathed in flame, side view, blade pointing right | 1254 x 1254 |
| **C1 SLASH ARC** | a blazing crescent slash trail, thick at its middle, tapering to points, orange core and red edge | 1254 x 1254 |
| **F1 FLAME BURST** | an upward burst of flame from a flat base, front view, orange core, red edges, a curl of black smoke at the top | 1254 x 1254 |
| **G1 GRIN** | a carved jack-o-lantern grin and two triangle eyes made of light only, floating, no pumpkin body | 1254 x 1254 |
| **E1 EMBERS** | 12-16 separate glowing embers and ash flecks, mixed sizes (30-120 px), spaced apart | 1254 x 1254 |

Rules (art bible v0.3 and the spec): crisp pixel rendering matching the Rider avatar; glow is rim light only, never a
painted disc or panel (`spec.chroma.unprocessable`); real transparency, no grey or tinted backing, no dark fringe; no
text, runes, symbols or figures beyond the grin; no franchise insignia. Native transparency preferred; otherwise a lime
key (no green in this palette).

## 5. Intake (Claude Code)

1. Raws to `art/halloween_headless_rider/hellfire_harvest/raws/`; raw QC per layer.
2. **T1** processed to the `STATIC` target: 256 x 256 lossless WebP, circle-safe, `artpreflight.py --type STATIC`.
3. **B1, C1, F1, G1, E1** composited by script into the appear strip: square frames at 112 px (spec `ANIMATION`
   minimum), vertical strip, lossless WebP under 460,800 bytes, frames and speed recorded;
   `artpreflight.py --type ANIMATION`.
4. Preview: a GIF of the strip at 50 px on a 13 x 7 hex board over the River background, every tile at once, plus one
   tile under a player portrait, for director acceptance.
5. Manifest (with the slot fix in section 1): two hidden gameAsset creates (STATIC, ANIMATION) in folder
   `HeadlessRiderHorror`, then the Rider unequip, the jutsu edit (appear + FireSFX on damage, static on recoil) and the
   re-equip (law 18/60, two runs).

## 6. Director decisions — APPROVED (2026-10-26)

1. **APPROVED:** Harvest Scorch tile and the five-stage Harvest Swing exactly as described in section 3.
2. **APPROVED:** The listed char/ember/hellfire palette and the two-frame jack-o'-lantern grin as the Rider's signature mark.
3. **DEFERRED TO PHASE 2:** The six-frame Smoulder loop. Do not include it in the current six-layer production pass; revisit after the first combat preview.

**Production gate:** No remaining section-6 art-direction revisions. Produce one raw candidate at a time in a **fresh isolated conversation for each of T1, B1, C1, F1, G1 and E1**, attaching the actual Rider avatar image once per conversation as **STYLE ONLY**. Show each candidate for separate director visual acceptance before the next layer. Preserve approved originals; leave compositing, QC, manifests and all live-game action outside the generation sessions. Approval here is not raw-asset approval or permission for live-game requests/writes.
