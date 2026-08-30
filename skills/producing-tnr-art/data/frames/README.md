# Rank frame plates - canonical listing-icon borders

The listing-icon border is COMPOSITED, not generated. Evidence: across the nine
live D-rank framed icons supplied by dauntless 2026-08-30, per-pixel standard
deviation in the border band is 3.8 versus 40.4 in the interior - the frame is
pixel-identical in all nine, so the original pipeline laid one plate over each
generated interior. We reproduce that rather than re-generating a frame per icon.

`frame_wood_D.png` is the median of those nine with the border-connected
low-variance region kept and the interior alphaed out. It IS the live D-rank
frame, not an imitation of it.

## Rank scheme
RULED 2026-08-30 (dauntless): quest rank is encoded by the frame's FINISH, not by
different materials - riveted metal banding was rejected as off-register for the
setting. All four are wood with dark iron corner brackets; only the finish changes.

  D  frame_wood_D.png      bare unfinished wood (already live on ~20 missions)
  C  frame_lacquer_C.png   dark red-brown urushi lacquer
  B  frame_lacquer_B.png   black lacquer, thin mother-of-pearl inlay stripe
  A  frame_lacquer_A.png   black lacquer, broad worn gold-leaf band + gilt brackets

SUPERSEDED 2026-08-30: an earlier metal scheme (copper/silver/gold banding with
rivets along the bands) was generated and dropped. Rivets exist ONLY on the corner
brackets, matching the live wood frame.

## Geometry
All four share one alpha. The metal/lacquer generations supply material and light
only; they never decide the silhouette. Each raw is keyed, edge-filled inward from
the nearest non-key pixel, masked to the shared alpha, then spill-scrubbed.

The shared alpha was softened 2026-08-30: the extraction's ragged inner boundary was
variance noise, not art (interior art bleeds under the frame edge, so the low-variance
mask frayed there). A radius-9 opening removes the spikes, the outer 12px shell is
restored unchanged, and a 1.2px blur softens the result. Plate share 0.3399 -> 0.3351.
Re-softening requires rebuilding all four from `raws/`.

## Measured state at bank time (2026-08-30)
  plate              median luma   bright>0.45 share   residual green
  frame_wood_D          0.082          0.0052                2
  frame_lacquer_C       0.065          0.0057                0
  frame_lacquer_B       0.078          0.0703                0
  frame_lacquer_A       0.078          0.0306                0
Bright share is the rank-legibility proxy: D and C sit low, B and A sit high and
roughly level. An earlier A candidate measured 0.0015 and read as the QUIETEST frame
in the set - the ladder was inverted - and a second candidate lost its black ground
and collided with D on hue. The banked A is the third.

## QC
Judge composited icons with
  rawqc.py ICON.png --opaque --band listing_icon_framed
The band is measured off the original nine (see 25x_DATA_art_spec.json ->
exposure_bands) and is PROPOSED, not ratified.

KNOWN GAP: a frame plate is keyed but runs to the image edge, so rawqc's RING check
rejects every one of them at 100% dirty-ring. The check assumes a subject floating in
key. All four plates were hand-verified on aspect and coverage instead. Needs a
`--frame` path alongside `--opaque`; not yet written.

OWED: the compositing pipeline above ran ad hoc with PIL/numpy. The toolchain is
stdlib-only, so it is NOT yet a repo script. Port before the next frame wave.
