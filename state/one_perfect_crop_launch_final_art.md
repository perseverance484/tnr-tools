# One Perfect Crop — launch-final art set

**Status:** IMPLEMENTED / pending exact-SHA independent review  
**Art direction / final acceptance:** dauntless  
**Repository implementation:** ChatGPT  
**Live-game requests / writes:** none

## 2026-09-27 scope clarification

The director clarified that the earlier "battle AI art only" instruction limited **new art
production**. It did not remove scene-character art that had already been made and accepted.

The launch-final art set therefore includes the existing accepted Ittetsu and Waystation Keeper
scene characters, while the Road Bandit scene character remains intentionally skipped and
nonblocking.

## Ittetsu scene character

Accepted source recovered from the prior art session:

- source name: `1000014011.png`
- source dimensions: 1024x1536
- source bytes: 183499
- source SHA-256: `4f30f186a56731442c574da1967ae66b158aef245772478ccd5fac6db7e7a306`
- source treatment: historical accepted black-background generation; do not redesign

Launch-final derivative:

- repository path: `art/one_perfect_crop/one_perfect_crop_ittetsu_scene.webp`
- dimensions: 341x512
- format: RGBA lossless WebP
- bytes: 24838
- SHA-256: `13c978641f10a412c47185c1efa591e1a7cb0f1963ab4a530a0b1cb7170cea61`
- visible bbox in the 341x512 canvas: `(66, 1, 269, 508)`
- partial-alpha share: 0.0%

## Waystation Keeper scene character

Accepted source recovered from the prior art session:

- source name: `1000014012.png`
- source dimensions: 1024x1536
- source bytes: 190949
- source SHA-256: `e46ca903e83a04a86015efb29c9b44fd9e9568ad8a542004727652365ddc6361`
- source treatment: historical accepted black-background generation; do not redesign

Launch-final derivative:

- repository path: `art/one_perfect_crop/one_perfect_crop_waystation_keeper_scene.webp`
- dimensions: 341x512
- format: RGBA lossless WebP
- bytes: 25104
- SHA-256: `a64b6a5f26a3264a31f5a787c14470d1eb84b423a4dc6920e7cdef50df3ae624`
- visible bbox in the 341x512 canvas: `(71, 1, 273, 506)`
- partial-alpha share: 0.0%

## Processing provenance

These two accepted sources predate the current chroma-native workflow and arrived on black rather
than #00FF00. They were recovered without redesign:

1. flood the contiguous near-black background from the image border (max RGB <= 20);
2. preserve the subject, including black outlines, by expanding the foreground mask by 3 px;
3. export a binary alpha mask;
4. resize 1024x1536 to the engine-native 341x512 SCENE_CHARACTER delivery size with
   nearest-neighbour sampling;
5. constrain the palette and export lossless WebP.

The q24 derivatives above were selected after visual QC. The more aggressive q16 variants were
rejected as over-posterized. Final repository acceptance is gated by repo-native
`artpreflight.py` against `push/54_one_perfect_crop_launch_final.json`.

## Other launch-final art

- Road Bandit AI avatar:
  `art/one_perfect_crop/one_perfect_crop_road_bandit_avatar.webp`; provenance remains in
  `state/one_perfect_crop_combat_avatars.md`.
- Harvest Boar AI avatar: director-approved reuse of the existing Wild Boar avatar:
  `https://utfs.io/f/Hzww9EQvYURJmjlQbElHE4IMO5Goa7cgLxPJ0VC6lU8vbt1A`.
- Market Clerk: reuse existing gameAsset `XsLLy8awDAtaE6hXVIi_0`.
- Road Bandit SCENE_CHARACTER: intentionally skipped.
- Harvest Boar SCENE_CHARACTER: not required.
- Cabbage Seed art: skipped.
- Quest/listing icon: not part of the current launch-final scope.
- Backgrounds: existing captured scene backgrounds only; no new background generation.

## Immutable pack

All three repo-backed launch-final image files are present at immutable commit:

`6a4f439a77517b23935c17058c2ec644f280e91e`

That commit is the imagePack ref for the revised launch-final manifest.
