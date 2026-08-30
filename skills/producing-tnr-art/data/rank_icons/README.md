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

## State - SET COMPLETE 2026-08-30, all four rawqc ACCEPT on listing_icon_framed
  rank  file                median luma  dark share  frame-band bright  webp
  D     icon_rank_D.*          0.121       0.682         0.0059          81KB
  C     icon_rank_C.*          0.098       0.733         0.0045          80KB
  B     icon_rank_B.*          0.126       0.641         0.0792          85KB
  A     icon_rank_A.*          0.151       0.609         0.0361          98KB
Raws kept as icon_rank_<R>_raw.png. Contact sheet: rank_icon_sheet.png.

C, B and A were generated with TWO references attached: the finished D (composition,
lighting, sheet, seal) plus that rank's flattened frame plate from ../frames/. Every
one came back on-composition first try - sheet extents within a few px of D's.

Frame-band bright share is the rank-legibility proxy. B's mother-of-pearl inlay
overshoots at 0.079 - it is the loudest frame in the set and outruns A's gold at
0.036. LEFT AS IS, ruled: the inlay is the only frame identifiable at 125px without
looking, which is the point of the set, and B otherwise came back clean. Revisit only
if the four read uneven in the live list.

NOT SHIPPED: upload + wire to twelve missions still pending.
  C x4  Chalk and Corner, The Empty Contract, Protection, The Waystation
  B x4  Nothing to Report, The Loud Way, Copies Not Thefts, Witness Detail
  A x4  Three Rounds, The Long Winter, Old Ghost, The Tenth Name
No D-rank mission in scope; D exists for the rank set and future missions.
