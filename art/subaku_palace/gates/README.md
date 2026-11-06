# Subaku Palace: the centre payoff (sigil, oni gates, palace beat)

Jutsu: Subaku Palace `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, AOE_SPIRAL_SHOOT, range 4). SELF +30% damage given for
2 rounds; ground: enemies -15% damage given for 3 rounds. The domain floor is the other half (`art/subaku_palace/`,
whose `TIMING.md` v5 owns the shared clock, palette and target geometry). Design doc:
`docs/design/SUBAKU_PALACE_ANIMATION.md`. Live-game requests: 0. No jutsu mechanics changed.

## What ships

| File | Geometry | Frames x ms | Bytes | Build |
|---|---|---|---|---|
| `exports/anim_sbk_gates_rise_v6.webp` | **shipping**: clip 2.5 hex heights, players as LPC character avatars (TIMING.md v5) | 44 x 50 | 4,304 | `build_gates.py` |
| `exports/anim_sbk_gates_rise_v3.webp` | note only: clip 1 hex height (338126cb, which the director expects to be reverted) | 38 x 50 | 3,930 | `build_gates_ratio1.py` |

Slot: `appearAnimation` on the existing SELF `increasedamagegiven` effect. `staticAnimation` and `staticAssetPath`
stay empty. Director, 2026-11-05: the sigil is symbolic and fades within the cast; there is no dais and no buff loop.

Superseded and deleted (in git history): v2, gated against the old portrait disc (012a7890); v4, before the
QA round on the sigil and the slow bloom (81f4bd93); v5, the flat-plank sigil and dark chips (eb17ebc0). Each change takes a new filename so no cached copy is served.

## The beat (TIMING.md v5: ring 1 ignites on 7, the floor's final pulse peaks on 29)

| Ticks | Centre |
|---|---|
| 0-5 | The sigil burns into the ground round the caster's feet: a spark in front of them, two arcs sweeping round to close a bevelled ring 30 x 8 px (0-0.4 h above the hex bottom; only the stretch of its back arc behind the legs is hidden), then ember cracks and a swell. |
| 6 | The bands flash white-hot to the hex's edge midpoints and run past them. |
| 7-9 | Ring 1 ignites. Two red sandstone oni gates tear up on either side of the caster in three heaves (25 %, 60 %, 100 %), 2 px sandstone shards knocked off each top and falling. The ring draws in to 18 x 8 px (8-9), so it stays whole between the standing gates through tick 20. Flared roofs with upturned eaves, a horn-crested lintel, a two-tone snarling face (10 x 11 px: light plate, dark V brows and maw, bright eyes, gold fangs, ember throat). |
| 14-20 | As the bloom spreads, the palace rises behind them: two three-tier pagoda towers. |
| 21-23 | The sigil cools to demon gold; it is out from 24 (director: it fades within the cast). |
| 22-26 | The solid two-tone demon-gold moon-gate arch traces up round the caster as the bloom reaches the rim. |
| 29-30 | The held beat on the floor's final pulse. Ridges, arch, finials and eyes are white-hot on 29 only; nothing moves. |
| 31-41 | The palace sinks (31-36); the gates sink into the floor (33-41). |
| 42-43 | Empty. Nothing lingers. |

## Geometry and keep-clear zones (50 px frame = 2.5 h, so h = 20 px)

The hex box is x 5-45, y 15-35. The LPC caster comes from theninjarpg `combatActors.ts:604-618`, `character.ts:56` and
`combatActors.ts:98` at cb755375. Its 1.35 h frame is centred 0.825 h above the hex bottom. A typical body, mapped by
LPC rows, spans x 20-29 (head) and 18-31 (arms), from y 5 (headgear) to the feet at y 30.

Gated at 0% on every frame (`build_gates.py` exits otherwise):
- **The caster's LPC envelope:** crown x 22-27 y 5-7, head x 20-29 y 8-17, torso and arms x 18-31 y 17-27, legs x 20-29
  y 27-31. It is the union of real LPC rows and the QA harness's LPC stand-in. The sigil's back arc and the palace
  pass behind the figure; nothing draws over it.
- **The lower neighbour's HP/SP/CP rows**, for everything except the sigil: they fall inside this clip at 0.2-0.6 h above
  this hex's bottom (x 15-34, y 23-31). The gates, palace and shards never touch them.

Reported, not gated (QA r3, 2026-11-06: the sigil is a real ground ring, hidden only behind the legs): the sigil's
back arc and flanks cross the lower neighbour's meter rows on ticks 4-23, up to 16.1 % of the rows. A neighbour's
rows are always visible when that neighbour is the viewer's own character (see the correction below).

**Accepted exception (director, 2026-11-05: "keep the arch"):** the caster's own meter rows (x 15-34, y 3-11). Only
the moon-gate arch's top crosses them, on ticks 24-33 (the roof wings sit below the rows). The build's rectangle gives
up to 33.3 % of the rows; the reviewer's renderer measured 40 % on v4 and should re-measure v6. It is reported in
`sbk_gates_v6.json`, not gated.

Correction to the premise: these rows are **always visible to the casting player**, not only on hover or selection.
theninjarpg cb755375 `combat.ts:420` passes the viewer's own userId as `selectedId`, and `combatActors.ts:516-520`
shows a fighter's meters when it is selected or hovered. Other viewers see the caster's rows only on hover or
selection. The director's acceptance should be re-confirmed on this basis.

The composition is mirror-symmetric about x -> 49 - x (the clip centre lies between pixels 24 and 25), inside a 2 px
margin.

## Other checks

- Every opaque pixel is in the TIMING.md v5 palette. Alpha is hard.
- White-hot appears on ticks 6 and 29 only.
- There are no ember specks or dashes at the gates' feet; the torn lip is basalt only.
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
