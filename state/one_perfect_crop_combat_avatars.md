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
- immutable image-pack commit: `ae2c51642c59a339326b7312f750543a1f50dcda`

The launch-final file is a deterministic delivery-size derivative of the accepted transparent
master, reduced with nearest-neighbour sampling and a constrained palette. It preserves the
approved silhouette while matching the game's 320px delivered AI-avatar width.

## Harvest Boar

**2026-09-26 director ruling:** reuse the existing Wild Boar avatar. Do not generate or upload
a separate Harvest Boar image.

Launch-final Harvest Boar avatar value:

`https://utfs.io/f/Hzww9EQvYURJmjlQbElHE4IMO5Goa7cgLxPJ0VC6lU8vbt1A`

That URL is treated as an existing-content reuse value, not an `@img` upload. It therefore does
not appear in the launch-final `imagePack` or `imgSizes`; only the new Road Bandit file does.

## Manifest contract

The launch-final manifest must:

- edit the existing hidden Road Bandit AI and bind the repo-backed Road Bandit avatar through
  `@img:one_perfect_crop_road_bandit_avatar.webp`;
- edit the existing hidden Harvest Boar AI and set its avatar directly to the approved Wild Boar
  URL above;
- create no art/gameAsset records;
- create no Cabbage Seed art;
- create no scene-character art.

The exact Road Bandit delivery file is release-gated with repo-native `artpreflight.py` against
the launch-final manifest. Gate results belong in the implementation/review handoff rather than
being copied into this source record.
