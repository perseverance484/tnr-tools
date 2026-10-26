# Art request: Ethereal Rebirth cast animation (ribbons wrapping the avatar)

- **For:** the art director
- **From:** Fable / Claude Code, at the director's request (2026-10-24): "Now we need a custom animation for ethereal
  rebirth. The ribbons themselves wrapping around the players avatar in battle. Use the chakra overflow rising star
  workflow as the exemplar, that turned out very well."
- **Exemplar:** the Chakra Overflow animation (`docs/handoffs/CHAKRA_OVERFLOW_ANIMATION_ART_REQUEST.md` and
  `CHAKRA_OVERFLOW_CROWN_LAYERS_ART_REQUEST.md`; build script `art/jutsu_icons/chakra_overflow/animation/build_strip.py`).
  Same route: the art director paints separate layers; Claude Code animates them by script on continuous curves and
  previews them in battle.
- **Companions:** the icon (`docs/design/icon_overhaul/ethereal_rebirth/`, round 2) and the non-elemental text draft
  (`TEXT_V2.md`). The animation shows the same moment: the seal at the chest cracks open, ribbons of pale soul-light pour
  out and spin around the user, one lashes out at the enemy, and the user is remade.
- **Source basis:** game source `studie-tech/theninjarpg` (local checkout `a744c04`; files cited unchanged in substance
  since the pinned `107d7a8`); the art spec target `ANIMATION`; the public read of the jutsu (2026-10-23).
- **Status:** analysis and brief. Art direction and acceptance are the director's (CLAUDE.md section 10).
- **Live-game requests/writes:** 0.

## 1. How the game plays it

| Fact | Detail | Source |
|---|---|---|
| Format | one vertical strip of square frames; `frames` 1–100; `speed` = ms per frame (1–100); plays once | `libs/threejs/util.ts` `showAnimation`; `SpriteMixer.ts` |
| Size and place | drawn as a **50 px** square centred on the caster's tile, **on top of the avatar** (layer 5 in the tile's effect group) | `libs/threejs/combat.ts:109`, `:646` |
| The avatar | a round token whose centre sits **0.283** of the frame from the top, radius **0.248** (measured from the director's battle recording for Chakra Overflow) | `build_strip.py` constants |
| Nothing goes behind the avatar | one sprite, drawn over the token; anything drawn inside the token's circle covers the portrait | same |
| Trigger | an effect's `appearAnimation` plays at its recipient's tile when the effect is new. Ethereal Rebirth's **absorb** effect targets **SELF** (the user, 3 rounds) and has no animation today, so the new strip goes there and plays on the caster. `disappearAnimation` can play when the absorb ends | `libs/combat/process.ts:1559-1575`; jutsu record |
| The hit on the enemy | the damage effect already plays `iDv3rjj81rRgD10shRqSn` on the target; unchanged unless the director wants a matching hit later | jutsu record |
| Limits | lossless WebP under **460,800 bytes**; real transparency (normal alpha blending, so glow must not leave dark halos over grass or snow) | `25x` ANIMATION target; `SpriteMixer.ts` |

## 2. The wrap illusion (proven by script)

Because nothing can pass behind the token, the token is kept as a **clear window**, as in Chakra Overflow's crown layout:

- **far side of the spin** (going behind the user): drawn only **outside** the token circle, dimmer and thinner, so it
  reads as passing behind;
- **near side** (coming round the front): drawn **across** the token, but only below face height, or turned see-through
  where it crosses the face;
- the **seal's core burst** sits at the chest, on the lower part of the token, never on the face.

Feasibility prototype (scripted, not art): `art/jutsu_icons/ethereal_rebirth/animation/prototype_wrap.py` →
`docs/design/ethereal_rebirth_animation/` (`proto_frames.png`, `proto_preview.gif` at 128 and 50 px over dark, grass and
snow with a stand-in token, `proto_strip.webp`: 40 frames of 128 px at 60 ms = 2.4 s, 199,762 bytes, under the ceiling).
Layout: `layout_guide.png`.

What it proves: the wrap reads at 50 px, and fits the budget. What it lacks: real ribbons (it draws flat strokes), and the
pale ribbons **wash out over the snow biome**: the painted ribbons need a saturated mid-tone edge.

## 3. Storyboard (about 2.4 s; ~40 frames at 60 ms)

| Beat | Time | What happens |
|---|---|---|
| 1. The seal breaks | 0–0.4 s | a white-gold point flares at the user's chest and cracks of light spread from it |
| 2. Ribbons pour out | 0.2–1.2 s | two ribbons of soul-light, one warm gold, one cool blue-white, pour out of the core and begin to spin around the user, near side in front, far side behind |
| 3. The spin rises | 0.4–2.0 s | the spin widens and climbs from the waist to above the head, one and a half turns |
| 4. One lashes out | 1.3–1.9 s | the gold ribbon breaks from the spin and whips out of the frame (towards the enemy; the hit itself is the damage effect's animation) |
| 5. Remade | 1.6–2.4 s | the spin dissolves upward into flecks of light; flecks peel from around the user and drift up |

Optional **disappear** strip (when the absorb ends, 3 rounds later): the last beat alone, a short upward dissolve of a few
flecks, 8–10 frames.

## 4. Deliverables (layers, route A)

Each on transparent (or flat lime `#00FF00`), 1254 px wide, same palette and finish as the round-2 icon:

| Layer | What | Why this shape |
|---|---|---|
| **R1 RIBBON GOLD** | one long ribbon of warm gold soul-light, painted **straight and horizontal**, about 1254 × 260 px, both ends tapering, a white-hot centre line, a saturated amber edge, a few frayed wisps along it | Claude Code bends it along the spin path by script, so it moves smoothly (Chakra Overflow lesson: animate one drawing on continuous curves, never cross-fade between separate drawings) |
| **R2 RIBBON BLUE** | the same in cool blue-white, with a saturated azure edge | the second ribbon |
| **C1 CORE** | the seal breaking: a white-gold burst with six to eight cracks of light, about 400 px, centred | scaled up and faded by script |
| **F1 FLECKS** | a sheet of 8–10 separate flecks of light (gold and blue-white), small diamonds and sparks, spaced apart | scattered and drifted by script |
| **K1 PEAK (reference only)** | one composed frame over `layout_guide.png`: the spin at its peak around the token, near side in front, far side behind, the lash leaving the frame | to agree the look; not animated |

Rules for all layers:
- **Non-elemental** (director, 2026-10-24): no fire, water, lightning, flames, droplets or bolts. Soul-light only.
- Each ribbon keeps a **saturated mid-tone edge** (amber, azure) so it holds over the snow biome; glows fade to
  transparency without dark fringes.
- Big, bold forms that read at 50 px; few large flecks rather than many tiny ones.
- No text, runes, symbols, figures or franchise looks.

## 5. Intake and delivery (Claude Code)

1. Raws to `art/jutsu_icons/ethereal_rebirth/animation/raws/` as delivered.
2. `build_strip.py` (Pillow only) maps R1 and R2 along the spin path, applies the window rule, adds C1 and F1, and writes the
   strip to `exports/`; previews at 128 and 50 px over three backgrounds, and over a battle recording if the director sends
   one. Revisions follow the Chakra Overflow rhythm (smoothness, timing, hold, a glint).
3. `artpreflight.py --type ANIMATION` (its `soft_edges` check is a known gap for glow effects, as on Chakra Overflow).
4. Delivery: create the new `ANIMATION` game asset (direct, as push/226 did), then set the **absorb** effect's
   `appearAnimation` (and optionally `disappearAnimation`) in the same suggestion that carries Ethereal Rebirth's new icon
   and text (one open suggestion per record), re-sending the live effects array and `injectableInBattle` (law 20).
