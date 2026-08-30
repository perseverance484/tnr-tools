# Rank listing icons - four shared quest.image assets

One icon per quest rank, wired on every mission of that rank, present and future.
quest.image is a RAW URL (@img: resolves direct, no gameAsset record), STATIC, 1:1.

## Method RULED 2026-08-30 (dauntless)
FULLY GENERATED, frame and letter included - not composited. This SUPERSEDES the
frame-plate method for the rank icons specifically.

Claude argued against it: four independent generations cannot converge on identical
frame geometry, and generators mangle text. The first full generation disproved the
concern in practice - with the composited mockup attached as reference, the frame came
back with correct proportions, correct bracket-and-rivet construction, no rivets on the
bands, and a crisp unmistakable letter. Recorded because the reasoning was wrong on the
evidence, and because the reference image is what did the constraining: fresh prompts
without it should NOT be expected to behave the same way.

CONSEQUENCE ACCEPTED: these frames are generated, so they do NOT match the ~20 live
wood-framed per-mission icons pixel for pixel. The rank set is its own family. Every
rank after D must chain off the approved D image as reference, never a fresh prompt,
or the four will not match each other either.

The frame plates in ../frames/ remain banked and valid - they are the fallback if the
generated chain drifts, and they are still the method for any future per-mission icon.

## Brightness grade of record
Raws come back dark. A gamma lift is applied deterministically after generation rather
than asking for a brighter gen, which would risk the approved frame and letter.
GRADE RULED 2026-08-30: gamma 0.88 ("light"). Applied identically to all four ranks.
  D raw    median luma 0.094  dark share 0.766
  D graded median luma 0.121  dark share 0.682   rawqc ACCEPT on listing_icon_framed
Candidates measured and rejected: 0.78 (0.156/0.600), 0.68 (0.197/0.506) - both inside
the band, both brighter than wanted.

## Design
Overhead mission brief on a dark desk, large round hanko seal pressed in cinnabar,
rank letter centred in the seal in heavy serif. Seal ~40% of image width - below that
the letter dies at the 125px display size. Dark wood margin around the sheet inside
the frame; without it the paper glares.

## State
  D  DONE   icon_rank_D.png / .webp (raw: icon_rank_D_raw.png)   512x512, webp 81KB
  C  todo   red-brown lacquer frame register
  B  todo
  A  todo
