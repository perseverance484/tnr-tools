# Forbidden Chakra Fury v11: designed whole, then cut into engine clips (2026-11-21)

Director: "design the animation as a whole first, then figure out what individual animations are needed to make it
work within the engine." Fit the description and the icon; something that would sit in a Naruto fighting game.

## Source

- Record: GROUND, `AOE_SPIRAL_SHOOT`, range 4. That is every tile within four hexes of the caster except the caster's
  own (60 tiles). Tags: `damage` (rounds 0) and `recoil` (rounds 2). A `visual` tag carries the caster clip.
- Description: the user's chakra lashes out at everyone nearby, seeks targets on its own, fast and powerful. Battle
  text: a battle cry, a raging storm of chakra, a relentless barrage.
- Icon: a crouched ninja (katana low, red scarf). Behind them the ground is shattered rock, and violet lightning with
  white-hot cores tears up out of every crack.

## The whole move (one shot, about 2 s)

1. **Charge (0-0.4 s).** The user crouches into the gate fire. Lightning crawls over the body and bites the ground,
   and cracks start at their feet.
2. **Fury (0.4 s).** A battle-cry burst: a white flash and the violet nova explosion on the user. A column of chakra
   lightning tears straight up into the sky.
3. **Shatter (0.4-0.8 s).** A shockwave runs out across the whole area. Behind it the ground fractures into one
   continuous web of glowing cracks spreading from the user, like the icon's floor.
4. **Storm (0.6-1.6 s).** The barrage. Lightning erupts up out of the cracks all over the area, and seeking bolts fall
   from the sky onto the ground with rubble flying. They land at scattered moments, not in rows, so it reads as
   autonomous chakra hunting targets.
5. **Settle (1.4-2.2 s).** The bolts flicker out, the cracks cool from white to violet to embers, and the floor fades.

## Engine constraints that shaped it

- Every area tile plays the same clip, centred on that tile. A clip can't point at the caster: the only per-tile
  changes are mirroring (left/right), an alternate clip, a hashed start offset (stagger) and a delay per hex from the
  caster (ripple). So nothing in the tiles is directional. The cracks radiate from each tile's centre and meet the
  neighbours at the edge midpoints, lightning goes up, bolts come down. Anything aimed at the caster comes from ripple
  timing alone.
- The caster clip is three tile heights square. It can't reach the area's edge, so the sky column goes up, not out.
- Each strip is at most 4096 px tall: 168 px frames, 24 frames at most.

## Cut into clips

| Layer | Tag | Scale | Clips | Settings | Job in the shot |
|---|---|---|---|---|---|
| Caster | visual (self) | 3 | caster | none | charge, fury burst, sky column, cracks on the user's own tile |
| Floor | recoil | 2 | floor A, floor B (alternate) | mirror, ripple 70, stagger 40 | shockwave band, then one cracked floor joined across every hex edge, cooling out |
| Storm | damage | 3 | eruption A, seeker B (alternate) | mirror, ripple 60, stagger 320 | lightning out of the cracks / bolts from the sky with rubble, scattered in time |

The floor fills each hex edge to edge with no rim, and both of its patterns meet all six edge midpoints. That way
neighbouring tiles join into one surface and the ripple turns the arrival into a single outward wave. The storm's
large stagger is what makes the barrage feel autonomous. With ripple added, its farthest tile starts at most 560 ms
after the nearest.
