# Subaku Palace: the centre payoff (sigil, oni gates, palace beat)

Jutsu: Subaku Palace `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, AOE_SPIRAL_SHOOT, range 4). SELF +30% damage given for
2 rounds; ground: enemies -15% damage given for 3 rounds. The domain floor is the other half (`art/subaku_palace/`,
whose `TIMING.md` v2 owns the shared clock, palette and target geometry). Design doc:
`docs/design/SUBAKU_PALACE_ANIMATION.md`. Live-game requests: 0. No jutsu mechanics changed.

## What ships

| File | Geometry | Frames x ms | Bytes | Build |
|---|---|---|---|---|
| `exports/anim_sbk_gates_rise_v4.webp` | **shipping**: clip 2.5 hex heights, players as LPC character avatars (TIMING.md v2) | 38 x 50 | 4,548 | `build_gates.py` |
| `exports/anim_sbk_gates_rise_v3.webp` | note only: clip 1 hex height (338126cb, which the director expects to be reverted) | 38 x 50 | 3,930 | `build_gates_ratio1.py` |

Slot: `appearAnimation` on the existing SELF `increasedamagegiven` effect. `staticAnimation` and `staticAssetPath`
stay empty. Director, 2026-11-05: the sigil is symbolic and fades within the cast; there is no dais and no buff loop.

v2, the earlier 2.5 strip, was gated against the old portrait disc. It is superseded after QA and deleted (it is in
git history at 012a7890). The filename changes so no cached copy of v2 can be served.

## The beat (TIMING.md v2: ring 1 lands on 7, the seal peaks on 20)

| Ticks | Centre |
|---|---|
| 0-5 | The burning-gold sigil kindles either side of the caster's feet and spirals out round them. |
| 6 | The bands flash white-hot to the hex's four side edge midpoints and run past them. |
| 7-12 | On ring 1, two red sandstone oni gates tear up on either side of the caster. Each has a flared roof with upturned eaves, a horn-crested lintel, and a two-tone snarling face (10 x 11 px: light plate, dark V brows and maw, bright eyes, gold fangs, ember throat). Stone chips fly outward. |
| 13-19 | The palace rises behind them: two three-tier pagoda towers, roof wings running into a solid two-tone demon-gold moon-gate arch that frames the caster (traced up from its base on 15-18). |
| 20-21 | The held beat on the seal peak. Ridges, arch, finials and eyes are white-hot on 20 only; nothing moves. |
| 22-35 | The palace sinks (22-27), the gates sink back into the floor shedding embers (24-32), and the sigil cools to demon gold and goes out. |
| 36-37 | Empty. Nothing lingers. |

## Geometry and keep-clear zones (50 px frame = 2.5 h, so h = 20 px)

The hex box is x 5-45, y 15-35. The LPC caster comes from theninjarpg `combatActors.ts:604-618`, `character.ts:56` and
`combatActors.ts:98` at cb755375. Its 1.35 h frame is centred 0.825 h above the hex bottom. A typical body, mapped by
LPC rows, spans x 20-29 (head) and 18-31 (arms), from y 5 (headgear) to the feet at y 30.

Gated at 0% on every frame (`build_gates.py` exits otherwise):
- **The caster's LPC envelope:** crown x 22-27 y 5-7, head x 20-29 y 8-17, torso and arms x 18-31 y 17-27, legs x 20-29
  y 27-31. It is the union of real LPC rows and the QA harness's LPC stand-in. The sigil's back arc and the palace
  pass behind the figure; nothing draws over it.
- **The lower neighbour's HP/SP/CP rows:** they fall inside this clip at 0.2-0.6 h above this hex's bottom (x 15-34,
  y 23-31). The sigil's front arc sits above them at y 22.5. The bottom band and the hex's bottom midpoint are not used.

**Accepted exception (director, 2026-11-05: "keep the arch"):** the caster's own meter rows (x 15-34, y 3-11). They are
shown only on hover or selection. The arch top and roof wings cross them on ticks 15-24 (up to 36.7% of the rows).
This is reported in `sbk_gates_v4.json`, not gated.

The composition is mirror-symmetric about x -> 49 - x (the clip centre lies between pixels 24 and 25), inside a 2 px
margin.

## Other checks

- Every opaque pixel is in the TIMING.md v2 palette. Alpha is hard.
- White-hot appears on ticks 6 and 20 only.
- There are no ember dashes at the gates' feet; the torn lip is basalt only.
- `artpreflight.py --type ANIMATION`: 0 errors, 0 warnings (`_provenance/`).

## Previews

The previews are true scale:
- the clip is 165 px on a 132 x 66 hex;
- the caster is an LPC stand-in drawn to LPC rows;
- the domain floor, seal and band waves come from `art/subaku_palace/exports`;
- the scenes cover even and odd columns, light and dark.

The script is in the session scratchpad (`sbk_view/preview_r25.py`) and imports `qa_preview.py` read-only. The raw
frames with both keep-clear zones outlined are in `_provenance/raw_frames_x4.png`.

## Open

- **Painted layers.** The optional request in `docs/handoffs/SUBAKU_PALACE_GATES_ART_REQUEST.md` targets the 2.5 geometry
  again.
