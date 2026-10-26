# Art request: Ethereal Rebirth animation, the icon's starburst (C2 and C3)

- **Director, 2026-10-24:** "I want the animation's starburst to more closely resemble the icons. Lets get a handoff for
  the art director."
- **For:** the art director. **From:** Fable / Claude Code. Art acceptance is the director's (CLAUDE.md section 10).
- **References (attach):** the approved icon `art/jutsu_icons/ethereal_rebirth/candidates/round3/raw_ethereal_rebirth_final.png`
  and its close-up `art/jutsu_icons/ethereal_rebirth/animation/raws/ref_icon_starburst.png` (the seal breaking at the
  chest). **Do not imitate** the current animation core, `animation/layers/anim_er_C1_core.png`.
- **Kept:** the v5 animation (six bands, motion, portrait mask). Only the burst at the start changes.
- **Live-game requests/writes:** 0.

## What differs

| The icon's starburst (the target) | The current core (to replace) |
|---|---|
| a **soft, round, white-hot glow** at the centre, fading through pale gold to clear | a hard white point inside a hazy yellow cloud |
| **fine, straight rays** radiating evenly from the centre, like a lens star: many thin lines, a few longer than the rest | a few **chunky, jagged gold shards**, like broken crystal |
| **cracks of light** branching outward like veins or cracks in porcelain: thick at the root, splitting into finer forks, wandering slightly, ending in hair-thin tips | no cracks |
| nothing loose around it | chips and flecks scattered around |
| colours: white `#ffffff` core, cream `#fff6c8`, pale gold `#ffe27a`, warm amber edge `#f0a030` on the cracks | saturated orange-gold |

## How the animation uses it

The burst plays in the first 0.45 s, centred on the player's portrait, drawn above everything (unmasked). It peaks at about
**30–40% of the 50 px frame width** (15–20 px on screen), so it must hold at that size: **bold main forms, fine detail second**.

Two layers, so the script can animate them separately:
1. **C2 GLOW + RAYS** flares up, then fades.
2. **C3 CRACKS** spread outward from the centre (revealed by radius), glow, then fade, so the seal visibly *cracks open*.

## Deliverables (transparent PNG, nothing else on the canvas)

| Layer | What | Size |
|---|---|---|
| **C2 GLOW + RAYS** | the icon's centre: a soft round white-hot glow (about a third of the canvas across, fading to clear) and 12–16 thin straight rays radiating evenly from it, mixed lengths, the longest four reaching near the canvas edge, tapering to points. Warm white to pale gold. No shards, no flecks. | 1254 × 1254, centred |
| **C3 CRACKS** | the icon's cracks of light alone, with no glow in the middle: 6–8 main cracks radiating from the centre, each **bold at the root** (about 24–30 px wide) and tapering, branching two or three times into finer forks, wandering slightly like cracks in porcelain, reaching about 85% of the way to the edge. White-hot inner line, pale-gold body, thin warm-amber edge. | 1254 × 1254, the cracks' common origin exactly at the centre |

Rules: premium TNR pixel art matching the icon's finish; real transparency (glow fades to clear, no grey or tinted panel,
no border, no dark fringe); **non-elemental**: the cracks must read as cracks of light in porcelain, **not lightning bolts**
(no zigzag bolts, no electric blue, no fire); no text, figures, runes or symbols.

## Intake (Claude Code)

Raws go to `art/jutsu_icons/ethereal_rebirth/animation/raws/` as delivered. `build_strip.py --set v5` replaces the v1 core
with C2 (scaled up, flared, faded) and C3 (revealed outward by a radial wipe, then faded), both on the unmasked top
layer at the portrait centre. Preview over the director's avatar (`avatar_preview.py`), with zoomed frames of the
opening. Then rebuild push/233 (the strip is pinned by SHA-256), run both gates, update `push/README.md`.
