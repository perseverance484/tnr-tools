**Request: make battle effect animations scale with the tile**

Hey! Small request from the content side.

Right now every effect animation in battle (the appear, static and disappear animations on jutsu effects) is drawn at a
fixed 50 px, no matter how big the battlefield is on the player's screen. Everything else on the tile (the avatar, the
marker, the star, the health bar) scales with the tile size, which grows with the battle canvas width.

The result is that our animations only line up with the player's portrait on one screen size. On a small phone the
effect is about 1.5 tiles wide and centred below the portrait; on desktop it's about two-thirds of a tile and sits low on
the avatar. So an effect designed to wrap around the portrait (a shield ring, a halo, ribbons circling the player) can't
fit everyone. Same goes for the existing animations, they just look bigger or smaller depending on the device.

**The ask:** size the effect animation from the tile instead of a fixed number. It's in `libs/threejs/combat.ts`, in
`drawCombatEffect`, where `showAnimation` is called with `scale: EFFECT_ANIMATION_SIZE` (once for the appear animation,
once for the static one). Something like `scale: h * 2.5` would do it (`h` is the tile height already in scope there).
That keeps today's size on a typical phone (canvas around 375 px) and makes it grow and shrink with everything else
on other screens.

That's all it needs. The BattlefieldPreview page mentions the 50 px size in its help text, so that line would want a
small tweak too.

Thanks!
