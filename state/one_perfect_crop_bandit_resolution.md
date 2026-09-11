# One Perfect Crop — Road Bandit AI reuse resolution

**Status:** resolved from fresh Forge 0.4.0 protected full capture.  
**Live-state evidence:** `harvests/inbox/tnr_results_1789124514980.json`.  
**Decision:** create a NEW generic Road Bandit AI + AiProfile for One Perfect Crop. Do not edit any shared live AI.

## Probe result

The read-only probe `push/04_one_perfect_crop_bandit_ai_probe.json` completed successfully in Forge 0.4.0 with five requested `profile.getAi` full captures persisted and zero items / zero mutations.

Candidate results:

| Candidate | Live result | Compatibility result |
| --- | --- | --- |
| Bandit 1 (`sJOmHYaUnJfh9-zbNL_4b`) | `data: null` | REJECT — catalog id no longer resolves to a live AI record. |
| Bandit Leader (`OACGO0AM5yBQkxlOs_rI_`) | `data: null` | REJECT — catalog id no longer resolves to a live AI record. |
| Marauder (`n8EP0t5NN3zhzxXiDdZIY`) | live AI | REJECT — CHUNIN, level 25, and equipped with one `Opening Strike` jutsu. This already disagrees with the approved JONIN three-move Road Bandit contract, so its AiProfile does not need a follow-up capture for reuse evaluation. |
| Mercenary Ronin (`Tnkm2Xk9EthSa2z_0LfFM`) | `data: null` | REJECT — catalog id no longer resolves to a live AI record. |
| Seichi Bandit (`UrAEVY5QvtQqKs-XB92PX`) | live AI | REJECT — GENIN, level 15, no equipped jutsu, and `aiProfileId: null`. It is not close enough to the approved contract for reuse. |

## Approved new Road Bandit contract

Create one new generic Road Bandit AI/profile using the already-approved event spec:

- technical rank: `JONIN`
- scale to user: ON
- element: `None`
- standard/default stored stat ratios and pools; no bespoke stat or pool bias
- stat multiplier: 1x
- pool multiplier: 1x
- default regeneration
- no armor bias beyond the event-approved standard/default choice
- no passive AI tags
- preferred combat identity: Bukijutsu flavor
- kit exactly:
  - S27 Weakening Strike — `YiRdVytsdxFzZtqkEDs5Q`
  - S41 Steady Strike — `fKvCGRgzGNskgFWocQCAg`
  - S40 Measured Strike — `kkGDat1XWUxhOQ1_T5025`
- behavior intent:
  1. move into range
  2. use Weakening Strike when available
  3. use Steady Strike
  4. use Measured Strike
  5. strongest legal fallback
- no stun, poison, wound, pierce, shields, healing, buffs, seals, adaptive counterplay, or bespoke signature jutsu
- one enemy in the F2 battle
- battle loss hard-routes to FAIL

No new jutsu are created. The shared pool jutsu are referenced by existing ids.

## Art consequence

Because the AI is new, One Perfect Crop requires both:

- `one_perfect_crop_road_bandit_scene.webp` — SCENE_CHARACTER
- `one_perfect_crop_road_bandit_avatar.webp` — AI avatar

`Nameless Ninja` remains explicitly rejected for visual reuse as deprecated / below the current quality bar.

## Next build gate

The combat-record decision is no longer blocking final design freeze. Remaining blockers are:

1. missing production art: Road Bandit scene + avatar, Harvest Boar avatar, Cabbage Seed item icon;
2. repository-native art QC/preflight for the already-processed Ittetsu, Waystation Keeper, and quest icon;
3. content-admin fields intentionally left open in `state/one_perfect_crop_content_admin_open.md`.

Once those are resolved, freeze `state/prompt_one_perfect_crop.md` for Fable manifest implementation.