# One Perfect Crop — launch-final combat avatars

**Status:** launch-final art record  
**Scope owner:** dauntless / art direction and final acceptance  
**Implementation:** ChatGPT  
**Live requests / writes:** none

## Road Bandit

Launch-final uses the director-approved Road Bandit AI design.

- accepted raw source: `1000017466.png`
- raw-source SHA-256: `150215b94c96ff1ba562a2cc946c9a01ae3d762353cb16d23c00d3d224bb3d27`
- raw QC: 1024x1024, lime coverage 0.477, 2px border-ring purity 1.000 — ACCEPT
- keyed master: transparent RGBA lossless WebP; the accepted processing pass had no enclosed background and no residual lime/magenta contamination
- launch-final repo asset: `art/one_perfect_crop/one_perfect_crop_road_bandit_avatar.webp`
- launch-final dimensions: 320x320
- launch-final format: lossless WebP with alpha
- launch-final bytes: 11268
- launch-final SHA-256: `fed328dc1fcfec1b5aeb4a452f2562d24b6495fa3bf7386abb4352d253aebf26`
- immutable launch-final image-pack commit: `6a4f439a77517b23935c17058c2ec644f280e91e`

The launch-final file is a deterministic delivery-size derivative of the accepted transparent
master, reduced with nearest-neighbour sampling and a constrained palette. It preserves the
approved silhouette while matching the game's 320px delivered AI-avatar width.

## Harvest Boar

**2026-09-26 director ruling:** reuse the existing Wild Boar avatar. Do not generate or upload
a separate Harvest Boar image.

Launch-final Harvest Boar avatar value:

`https://utfs.io/f/Hzww9EQvYURJmjlQbElHE4IMO5Goa7cgLxPJ0VC6lU8vbt1A`

That URL is treated as an existing-content reuse value, not an `@img` upload. It therefore does
not appear in the launch-final `imagePack` or `imgSizes`. The imagePack also contains the two
already-made accepted scene-character files documented in
`state/one_perfect_crop_launch_final_art.md`.

## Manifest contract

Combat-art assertions in the revised launch-final manifest remain:

- edit the existing hidden Road Bandit AI and bind
  `@img:one_perfect_crop_road_bandit_avatar.webp`;
- edit the existing hidden Harvest Boar AI and set its avatar directly to the approved Wild Boar
  URL above;
- create no new AI and no Cabbage Seed art.

The revised launch-final manifest separately creates the two already-made accepted hidden
SCENE_CHARACTER gameAssets. Their provenance and exact bytes are owned by
`state/one_perfect_crop_launch_final_art.md`.

Repo-native art preflight is a release gate and is reported in the frozen implementation handoff.
