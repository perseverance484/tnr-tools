# Ethereal Rebirth animation: art session prompt

- **Brief:** `docs/handoffs/ETHEREAL_REBIRTH_ANIMATION_ART_REQUEST.md` (how the game plays it, the wrap illusion, the
  storyboard, the layers). Exemplar: the Chakra Overflow animation.
- **How to use:** paste the block below into a new art-director session. Return the raws only; Claude Code animates them.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session paints the LAYERS for a
custom battle animation: Ethereal Rebirth's cast. Read docs/handoffs/ETHEREAL_REBIRTH_ANIMATION_ART_REQUEST.md first.

The animation (2.4 s, played over the caster's avatar in battle at 50 px): the seal on the user's soul cracks open at
their chest; two ribbons of pale soul-light (warm gold, cool blue-white) pour out and spin around the avatar, rising from
the waist to above the head; the gold ribbon breaks away and lashes out of the frame towards the enemy; the spin dissolves
upward into flecks of light. It matches the jutsu's icon (round 2) and its battle text.

The game draws the animation ON TOP of the avatar's round token, so Claude Code makes the ribbons look like they wrap
around it by script (far side hidden inside the token, near side crossing in front). You paint the pieces; you do not
paint the animation frames.

Paint these layers, each on transparent (or flat lime #00FF00), 1254 px wide, in the round-2 icon's palette and finish:
1. R1 RIBBON GOLD: one long ribbon of warm gold soul-light, painted STRAIGHT and HORIZONTAL, about 1254 x 260 px, both
   ends tapering, a white-hot centre line, a saturated amber edge, a few frayed wisps.
2. R2 RIBBON BLUE: the same in cool blue-white with a saturated azure edge.
3. C1 CORE: the seal breaking: a white-gold burst with six to eight cracks of light, about 400 px, centred.
4. F1 FLECKS: a sheet of 8-10 separate flecks of light (gold and blue-white), small diamonds and sparks, spaced apart.
5. K1 PEAK (reference only): one composed frame drawn over docs/design/ethereal_rebirth_animation/layout_guide.png: the
   spin at its peak around the token (red circle), near side in front, far side behind, the lash leaving the frame.

Rules: NON-ELEMENTAL (no fire, water, lightning, flames, droplets or bolts; soul-light only). Ribbons keep a saturated
mid-tone edge so they hold over bright snow backgrounds; glow fades to transparency with no dark fringe. Big, bold forms
that read at 50 px. Premium TNR pixel art: hard pixel edges, no gradients or blur in the forms. No text, runes, symbols,
figures or franchise looks.

Return the raw images only, named anim_er_R1_ribbon_gold.png, anim_er_R2_ribbon_blue.png, anim_er_C1_core.png,
anim_er_F1_flecks.png, anim_er_K1_peak.png. Do not process, crop, key or upload anything.
~~~
