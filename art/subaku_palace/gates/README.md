# Subaku Palace: the centre payoff (sigil, oni gates, palace beat)

Jutsu: Subaku Palace `jELEiw5W3N4m2R3oJm3Pk` (player EVENT, AOE_SPIRAL_SHOOT, range 4). SELF +30% damage given for
2 rounds; ground: enemies -15% damage given for 3 rounds. The domain floor is the other half (`art/subaku_palace/`;
`TIMING.md` owns the shared clock and palette). Live-game requests: 0. No jutsu mechanics changed.

Director, 2026-11-05: the sigil is symbolic. It plays in the cast and fades within it. There is no dais tile and no
lingering buff loop. Combatants are character avatars, not portraits.

## Assets

| File | Geometry | Frames x ms | Bytes | Build |
|---|---|---|---|---|
| `exports/anim_sbk_gates_rise_v3.webp` | **main** (1 hex-height clip, LPC character avatars) | 38 x 50 | 3,930 | `build_gates.py` |
| `exports/anim_sbk_gates_rise_v2.webp` | fallback for **3314d122** (2.5 hex-height clip, portrait marker and disc) | 38 x 50 | 6,374 | `build_gates_ratio25.py` |

Proposed slot: `appearAnimation` on the existing SELF `increasedamagegiven` effect. Leave its `staticAnimation` and
`staticAssetPath` empty. Ship exactly one of the two strips, the one that matches the deployed geometry.

## Engine geometry (theninjarpg origin/main cb755375, fetched from GitHub)

| Fact | Source |
|---|---|
| The effect clip is ONE hex height square (`EFFECT_ANIMATION_HEX_RATIO = 1`; it was 2.5 at 3314d122, changed in 338126cb, 2026-11-02) | `app/src/libs/rendering/animation.ts:72` |
| The clip is centred on the hex, anchor 0.5, fetched as a 50 px rendition and sampled linearly | `scenes/combatEffects.ts:126,130`; `primitives/animation.ts:16,65` |
| The hex is w = 2h (`HEX_ASPECT_RATIO = 0.5`), so the clip spans the hex from its flat top edge to its flat bottom edge, across the middle half of its width | `app/drizzle/constants.ts:941` |
| Static ground art (`staticAssetPath`) is sized to the hex box (`size: tile.height, width: tile.width`) at any clip ratio, and draws under the fighters | `scenes/combatEffects.ts:139-152`, z 5.25 (`:23`) |
| Clips draw over the fighters AND their HP/SP/CP meters (effects are the last child of the world) | `scenes/combat.ts:172-174` |
| Player with `spriteAppearance` (303c6cbc, 2026-10-30): a layered LPC character 1.35h square, centred at 0.825h above the hex bottom | `scenes/combatActors.ts:36,604-618` |
| LPC layers are 64 px frames scaled 1/64 into a unit square; feet at row 60, so groundY = 0.234h | `primitives/character.ts:56`; `combatActors.ts:98` |
| The footprint varies: headgear fills the frame top (`:262`); oversized weapons use larger sheets that overrun the unit square (`character.ts:34`); facing changes with movement | |
| Player without `spriteAppearance`: the old marker (h wide) plus a masked disc | `combatActors.ts:620-636` |
| AI originals: 1.6h tall, preserveAspect, centred 0.9h | `combatActors.ts:595` |
| The clan badge sits at x = 0.9w, outside a 1-hex clip | `combatActors.ts:646` |

On the 50 px frame of a 1-hex clip, a typical LPC body (LPC px x 18-46, y 10-62) covers x 10-40 from above the
frame down to y 40, with the feet at y 38. The head and shoulders are above the clip.

## The beat (v3; TIMING.md v1: ring 1 lands on 7, the seal pulse peaks on 20)

| Ticks | Centre |
|---|---|
| 0-5 | The burning-gold sigil kindles at the caster's feet and spirals out over the ground around them. |
| 6 | The bands flash white-hot and run out of the frame toward the hex's lower edges: the energy leaves the hex. |
| 7-12 | On ring 1, two red sandstone gates, each crowned with a snarling oni face, tear up on either side of the caster, throwing chips. |
| 13-19 | Pagoda roofs stack on both gates (gold ridges, upturned outer tips, finials). The two gate-towers flanking the caster are the palace's front. |
| 20-21 | The held beat on the seal peak. Nothing moves. Ridges, finials and oni eyes are white-hot on 20 only. |
| 22-35 | The roofs fold, the gates sink back into the floor shedding embers, and the sigil cools to demon gold and goes out. |
| 36-37 | Empty. Nothing lingers. |

**Limit of the 1-hex clip:** nothing can draw above the hex's top edge, while the character stands about 1.2h tall. So
the gate-towers top out around the caster's chest, and no palace can rise behind or above them. The 2.5 fallback
(v2) has room for a full palace and moon gate. A taller centre beat on main would need a different carrier, such as
neighbouring-hex visual tags. That is a director decision.

## Checks (`build_gates.py` exits non-zero otherwise)

- No pixel is within 2 px of the frame edge on any frame.
- Every opaque pixel is in the TIMING.md palette (plus two basalt shades from the domain tile). Alpha is hard (0/255).
- White-hot appears on ticks 6 and 20 only. The last two frames are empty.
- **LPC head/torso core** (x 14-36): 0% covered on every frame. **Whole LPC envelope** (arms to x 10-40): at most 10%. That
  is the gates standing in front of the arms' outer edges, which they physically do (gate base y 45, feet y 38). The
  cap is 12%.
- Legacy marker coverage, for a player without a character appearance, is 26.5% at most. It is reported, not gated:
  the marker spans the whole clip width.
- The envelope is a model, not real LPC art (none is in the repo). Headgear and oversized weapons extend it.
- `artpreflight.py --type ANIMATION` on both strips: 0 errors, 0 warnings (`_provenance/`).

## Previews

The main-geometry preview draws:
- the clip at 66 px on a 132 x 66 hex;
- an LPC stand-in caster mapped by LPC rows;
- AI enemies at 1.6h;
- the floor half's static tile.

The floor's wave and seal clips are left out: they were authored for a 2.5h clip. The script lives in the session
scratchpad, `sbk_view/preview_main.py`, and imports `qa_preview.py` with `CLIP_RATIO=1`.

The harness itself is not modified. Note that its `LPC=1` stand-in draws the body over the whole 1.35h frame, which
puts the head too high and the feet too low.

## Open

1. **Which geometry is deployed.** Character avatars are confirmed live (so 303c6cbc is deployed). The 1-hex clip
   (338126cb) is assumed live until confirmed.
2. **TIMING.md's centre column** predates the ruling that puts the gates on ring 1 and the hold on the seal peak. The
   floor half owns that file.
3. **Painted layers (optional):** `docs/handoffs/SUBAKU_PALACE_GATES_ART_REQUEST.md`. Those were sized for the 2.5 clip; at
   1 hex the gate is 7 x 26 px, so painting buys little.
