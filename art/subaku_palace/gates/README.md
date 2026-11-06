# Subaku Palace: the centre payoff (sigil, gates, palace, the master's buff)

Jutsu: Subaku Palace `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, 40 AP, AOE_SPIRAL_SHOOT, range 4). SELF +30% damage given
for 2 rounds; ground: enemies -15% damage given for 3 rounds. Battle text (`EVENT_JUTSU_STORY_TEXT.md`): "a sigil of
burning gold spirals outward ... gates of red sandstone carved with snarling faces tear free of the ground, and the
shadow of the demon palace falls across the field". The domain floor is the other half (`art/subaku_palace/`,
`TIMING.md` owns the shared clock and palette). Live-game requests: 0. No jutsu mechanics changed.

Build: `python3 art/subaku_palace/gates/build_gates.py [--sheet PNG]` (Pillow only) writes `exports/` and
`exports/sbk_gates_v2.json`.

## Assets

| File | Type | Frames x ms | Bytes | Slot (proposed) |
|---|---|---|---|---|
| `exports/anim_sbk_gates_rise_v2.webp` | ANIMATION | 38 x 50 (1.9 s) | 6,374 | `appearAnimation` on the SELF `increasedamagegiven` effect |
| `exports/anim_sbk_master_loop_v2.webp` | ANIMATION | 16 x 50 (0.8 s loop) | 994 | `staticAnimation` on the same effect (2 rounds) |
| `exports/tile_sbk_dais_v2.webp` | STATIC | 1 | 1,042 | `staticAssetPath` on the same effect |

All three hang off the one existing SELF effect, so no tag is added. The director has accepted extra SELF visual tags if
they are wanted later, for example a split appear. Assets are created hidden and unhidden by a follow-up (engine doc
5.2).

## The beat (ticks of 50 ms; TIMING.md v1: ring 1 lands on 7, the seal pulse peaks on 20)

| Ticks | Centre |
|---|---|
| 0-5 | The sigil kindles at the caster's feet: a spark, then two burning-gold arms spiral out and the bevelled outer ring closes. The back arc passes behind the portrait. |
| 6 | The six bands flash white-hot along the edge midpoints and run past the hex edge. The energy leaves the hex the tick before ring 1. |
| 7-12 | Ring 1 lands. Two red sandstone gates tear up out of the stone with an overshoot. Each is crowned with a snarling oni face: V brows, slanted burning eyes, upper and lower fangs, an ember throat, a demon-gold collar. The torn lip glows with embers and chips arc out and fall back. |
| 13-19 | The palace rises behind the caster: two three-tier pagoda towers (shadow roofs, demon-gold ridges with upturned tips, ember windows) and a lacquered wall with a moon gate whose round door is cut round the caster's pin. The gold arch traces up from both jambs to a horned oni crest. |
| 20-21 | The held beat, on the seal peak. Nothing moves. Ridges, crest and eyes are white-hot on 20 only, then burning gold on 21. |
| 22-37 | The settle. The palace sinks back (22-27) and the gates sink into the floor (24-32), shedding embers. The sigil cools from burning to demon gold, and its last frames match the dais under it, so the appear ends on the floor's look. |
| 0 onward | The buff loop runs on the same clock (it draws over the appear): ember licks along both flanks, motes rising, demon-gold glints at the hex's side vertices on the beat (peak frame 0). |

## Rules this meets (checked by the build; it exits non-zero otherwise)

- **Clip square:** 2.5 hex heights, authored on the 50 px rendition grid and exported x3 nearest (150 px frames). No pixel
  is within 2 px of the frame edge on any frame, so nothing clips.
- **The caster stays readable:** the moon gate's door, the sigil's back arc and the sinking palace all keep the avatar
  disc (r 8) clear. It is covered 0% on every frame. The build fails above 8%.
- **The loop is restrained:** 1.2-2.5% of the frame, peaking on frame 0. Nothing falls inside this hex's pin box, the
  pin of the hex below, or the clan badge (`build_fx.portrait_mask` geometry).
- **Palette:** every opaque pixel is from `TIMING.md` (shadow, red sandstone x5, demon gold x3, burning gold x3, ember
  x4) or the domain tile's basalt (`#1f1111 #2b1c1a #362521`). White-hot `#fff4c8` appears on ticks 6 and 20 only. There
  is no green, violet or cyan.
- **Overdraw:** alpha is hard (0/255) everywhere, so an extra copy of a frame changes nothing. The appear plays once
  anyway: it is on a damage-modifier tag, which the client draws once (engine doc 0.4).
- **Preflight:** `artpreflight.py --type ANIMATION` (2 strips) and `--type STATIC` (dais) both return 0 errors and
  0 warnings. The reports are in `_provenance/`, with `SHA256SUMS`.

## Composite order (a note for the floor's preview)

Within one sync, ground effects are created before user effects (`combatEffects.ts:55-66`, engine doc 3.2). That
covers the ground tag's records, its server `visual`s and the band visual tags. So the SELF appear and loop draw over
the seal and band clips, not under them. The previews here use that order.

## Previews (true scale, the shared harness `scratchpad/custom/qa_preview.py`, imported unmodified)

The arena is 12 x 10, with the caster plus three enemies, on the domain half's WIP floor (`tile_sbk_domain_v3`, band
waves, seal) for both column parities. GIFs and key sheets are in the handoff. `keys_phone_59px.png` shows the 59 px
clip of a 400 px phone canvas, the 50 px read.

## Open (user-owned decisions; proposals only)

1. **The dais lasts 2 rounds and the floor 3.** In round 3 the caster's hex goes back to bare board inside the domain. Options:
   - accept it, as a tell that the buff ended;
   - put the dais on a zero-impact SELF visual tag with rounds 3 (a record change for the director).
2. **The dais follows the caster.** It is a user effect, drawn on the target's current hex. A caster who walks away
   carries the hub and leaves a bare hole at the domain's centre. The alternative is a COORDINATES carrier at the cast
   hex, which also changes the record.
3. **TIMING.md's centre column** (gates 17-24, hold 24-30, settle 30-38) predates the coordinator's ruling: gates on
   ring 1 (tick 7), hold on the seal peak (tick 20). These assets follow the ruling. The floor half owns TIMING.md and
   should update that column.
4. **Dais exits.** The six bands leave at the edge midpoints, matching the approved exact-geometry floor's interlock. If
   the final floor tile moves its band exits, re-sync `EDGE_MID` and rebuild (one constant).
5. **Painted layers (optional upgrade):** `docs/handoffs/SUBAKU_PALACE_GATES_ART_REQUEST.md`. The programmatic version
   ships meanwhile.
