# Isonade combat animations v1

Eight animations for the Isonade boss fight (nine strips: Bite of the Ship is a one-shot bite plus a looping drip). Built in code, offline: no live-game requests, nothing uploaded.

Rebuild: `python3 build_isonade_anims.py` (Pillow only; reads the Skyglass strips and the battle still from the tnr-tools checkout at `$TNR_REPO`, default `/home/user/tnr-tools`).

## Strips

All: vertical strip of square 128 px frames, lossless WebP with real alpha, `speed` 50 ms per frame, drawn for `animationScale` 3. Limits checked by the build (it fails otherwise): height <= 4096 px (<= 32 frames of 128 px) and file < 460,800 bytes.

| File | Engine slot | Frames | Frame | Height px | Bytes | Loops | Length | What it shows |
|---|---|---|---|---|---|---|---|---|
| `anim_isonade_body_water_v1.webp` | `staticAnimation`: Body water ground effect on the 6 hexes round Isonade, from round 1, all fight | 32 | 128 x 128 | 4096 | 89,468 | yes | 1600 ms | Black water churning with wet arm coils breaking the surface; blue-black only, no red/green/cyan |
| `anim_isonade_slam_v1.webp` | `appearAnimation`: Slam damage effect on each hex marked red the turn before | 14 | 128 x 128 | 1792 | 33,850 | no | 700 ms | A thick dark arm crashes down: white flash, splinters and spray thrown up, crater; the arm hauls back up |
| `anim_isonade_brine_v1.webp` | `staticAnimation`: Brine pool lingering ground effect (3 rounds), created by the Slam | 24 | 128 x 128 | 3072 | 45,356 | yes | 1200 ms | Green-black brine bubbling up through broken floorboards; tg_linger green family, pulse peaks on frame 0 |
| `anim_isonade_arm_burst_v1.webp` | `appearAnimation`: Summon flourish where a Grasping Arm appears | 16 | 128 x 128 | 2048 | 32,494 | no | 800 ms | The deck heaves and bursts, black water spouts, an arm rises and hooks, then dissolves to leave the summon |
| `anim_isonade_arm_lash_v1.webp` | `appearAnimation`: Grasping Arm's attack damage effect on the hexes round its own hex | 10 | 128 x 128 | 1280 | 25,162 | no | 500 ms | A quick sideways swipe of the arm with a motion smear, hit spark and brine spray |
| `anim_isonade_surge_v1.webp` | `appearAnimation`: Black Water damage effect on every hex but the safe crates, the turn after the room goes red | 24 | 128 x 128 | 3072 | 60,372 | no | 1200 ms | A flat-topped wall of black water a little wider than the hex rises to head height with rolling foam, tins and splinters churning, crashes down in rounded spray plumes, then drains (rises and falls; no teeth, no mound, unlike Maw) |
| `anim_isonade_eye_v1.webp` | `staticAnimation`: Open eye: buff/visual on Isonade's own hex for the 1-round punish window | 16 | 128 x 128 | 2048 | 48,950 | yes | 800 ms | The great pale eye, open, iris drifting, slit pupil breathing, in a pale cyan halo; a cyan ring of light pulses on the floor and spreads each beat |
| `anim_isonade_bite_v1.webp` | `appearAnimation`: Bite of the Ship at half health (appear of the same effect that carries the rot drip) | 20 | 128 x 128 | 2560 | 61,030 | no | 1000 ms | Hull planks rip inward, jaws of black hide snap on them, white flash, shockwave rings spread, rot starts to seep |
| `anim_isonade_rot_drip_v1.webp` | `staticAnimation`: Rot drip aura on Isonade for the rest of the fight (static of the Bite effect) | 24 | 128 x 128 | 3072 | 26,708 | yes | 1200 ms | Rot-green ooze on the rim of the portrait drips to a puddle on the floor; motes rise |

Shared cadence: the eye loop is the 0.8 s beat (16 frames); body water 1.6 s (two beats); brine and drip 1.2 s (as tg_linger). Every loop is seamless: each moving part is periodic in the loop length.

## Previews (`previews/`)

Battle frame: `docs/design/celestial_dew_animation/battle_still_2026-10-24b.png` (the real battle still the Skyglass previews use; hex 132 x 66 px), clips at tile.height x 3 = 198 px centred on their hexes and drawn over the characters, as the pixi renderer does. Each strip is first reduced to the 50 px-wide rendition the battle CDN serves and magnified bilinearly, so the softness shown is the delivered softness. The body water runs under every preview (it stays all fight). Tokens: the player token cut from the still (three players), a dark placeholder token with a pale eye for Isonade, and a dark placeholder for the Grasping Arm.

- `previews/isonade_body_water_v1.gif` (96 frames at 50 ms, 3,387,725 bytes)
- `previews/isonade_slam_v1.gif` (22 frames at 50 ms, 981,958 bytes)
- `previews/isonade_brine_v1.gif` (72 frames at 50 ms, 2,720,995 bytes)
- `previews/isonade_arm_burst_v1.gif` (26 frames at 50 ms, 1,088,397 bytes)
- `previews/isonade_arm_lash_v1.gif` (20 frames at 50 ms, 943,479 bytes)
- `previews/isonade_surge_v1.gif` (34 frames at 50 ms, 2,594,126 bytes)
- `previews/isonade_eye_v1.gif` (64 frames at 50 ms, 2,307,676 bytes)
- `previews/isonade_bite_v1.gif` (68 frames at 50 ms, 2,449,704 bytes)
- `previews/isonade_seq_slam_v1.gif` (94 frames at 50 ms, 4,392,674 bytes)
- `previews/isonade_seq_slam_brine_after_v1.gif` (94 frames at 50 ms, 4,414,368 bytes)
- `previews/isonade_seq_black_water_v1.gif` (66 frames at 50 ms, 4,025,241 bytes)

QC sheets (every frame on dark, mid and bright grounds): `previews/qc_body_water.png`, `previews/qc_slam.png`, `previews/qc_brine.png`, `previews/qc_arm_burst.png`, `previews/qc_arm_lash.png`, `previews/qc_surge.png`, `previews/qc_eye.png`, `previews/qc_bite.png`, `previews/qc_rot_drip.png`

## Weak spots, guesses, and what is not done

- **Slam vs brine (the main open decision).** If the brine pool is a loop created by the same action as the slam, the engine starts it at the strike and draws it ON TOP of the slam (every loop above every appear). On a marked field the brine then hides the arms' lower halves, the white flash and the crater: see `isonade_seq_slam_v1.gif`. `isonade_seq_slam_brine_after_v1.gif` shows the same slam with the brine starting as the slam ends, which reads far better. Ways to get there: the brine on a later action, or the brine pool as a still `staticAssetPath` ground image (drawn under characters and clips) with only the bubbles as a loop. Not built: it changes how the effect is authored, which is a content decision.
- **Filled ground loops cover the head of the character in the hex below.** Clips draw over characters, and a pool that fills its hex reaches into the portrait of whoever stands one row in front (tg_heavy avoids this by being a hollow ring). Body water and brine keep a translucent middle (alpha 118 and 150) so the portrait shows through, but a dark rim still crosses it. The same `staticAssetPath` route would put them under the characters.
- **Frame size.** Existing Skyglass strips are 50 px (tg_*) or 150 px (AN01-AN09) frames. These are 128 px per the brief, so 32 frames fit the 4096 px rule. Outline weight (3 px at 128, about 1 px at the 50 px battle rendition), hex footprint (about 85 x 43 px at scale 3, the size tg_heavy reads at) and palette follow the Skyglass set; the drawing is smooth cel-shaded, not the 50 px pixel grid of tg_*.
- **animationScale 3 is a recommendation**, not checked against live records (none exist yet).
- **Black Water vs Maw.** Maw (`anim_maw_v1`) is a round teal mound with a dark mouth and teeth. The surge is a flat-topped, steep-sided navy wall slightly wider than the hex (so neighbours join into one flood) with rolling white-grey foam lobes, tins and splinters; it falls back with rounded spray plumes (no spikes) and drains. At battle size the field reads as a room flooding; individual tiles still show as stacked blocks, which is the weakest look of the set.
- **Safe crates during the surge.** Walls on the hexes in front of a crate rise over the crate hex's lower half; the tg_safe star stays visible above them. The preview keeps tg_safe standing through the surge; whether the mark survives into the detonation round, and the draw order between the two effects, were not checked.
- **Open eye is one looping strip** (eye open the whole time). An eye-opening appear was not built: a loop of the same action draws on top of it, so the opening would be hidden.
- **Bite + drip** are meant as the appear and static of one effect (the drip draws on top from the strike, as previewed). The drip runs on both sides of the portrait circle, whose place (centre about 21 px above the hex centre in the frame, radius 21) is measured from the player token on the still; an Isonade avatar framed differently may need the drip nudged. The rot drip is green (as the brief asks; the Core Horror enrage aura AN04 set that precedent), so it shares the linger colour.
- **Arm lash** plays the same swipe, left to right, on every hex round the arm (the engine cannot vary it per hex). It is mostly a pale slash with a thin dark arm tip so six copies do not bury the characters.
- **Backgrounds and tokens.** The only real battle frame in the repo is the snowy Celestial Dew still; there is no flooded-storeroom battle background yet, so contrast on a dark wooden floor is untested. Isonade and the Grasping Arm have no avatars: their tokens are placeholders.
- **Byte counts** are the files as they sit on disk. This file store appends a C2PA provenance chunk (about 5.8 KB) to each image after it is written, so a file is a few KB larger than the encoder's output; both are in `isonade_anims_v1.json`. Every file is far under the 460,800-byte ceiling either way.
- **Preflight:** `artpreflight.py --type ANIMATION` passes width, aspect and bytes but flags `soft_edges` on every strip (7-40% partial-alpha pixels against a 5% ceiling). That gate targets chroma-keyed art; here the partial alpha is deliberate (stepped anti-aliased edges, translucent pool middles, dissolves). The approved tg_linger_v2 and tg_safe_v2 strips fail the same gate (25% and 53%).
- **Not done:** no upload, no gameAsset rows, no manifest, no check in a real browser battle (the skill asks for one hidden test strip in a real battle before trusting fine detail). Filenames are new (`_v1`); a corrected strip needs a fresh name.
