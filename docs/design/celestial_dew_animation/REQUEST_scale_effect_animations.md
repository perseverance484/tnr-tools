**Request: scale battle effect animations with the tile**

**What:** In `libs/threejs/combat.ts` (`drawCombatEffect`), change the two `showAnimation` calls from
`scale: EFFECT_ANIMATION_SIZE` to `scale: h * 2.5`.

**Why:** Effect animations are drawn at a fixed 50 px, but the tile and avatar scale with the battle canvas width. So
animations only line up with the portrait on one screen size. `h * 2.5` matches today's 50 px on a typical phone and
scales correctly on every other screen.
