# Rank frame plates - canonical listing-icon borders

The listing-icon border is COMPOSITED, not generated. Evidence: across the nine
live D-rank framed icons supplied by dauntless 2026-08-30, per-pixel standard
deviation in the border band is 3.8 versus 40.4 in the interior - the frame is
pixel-identical in all nine, so the original pipeline laid one plate over each
generated interior. We reproduce that rather than re-generating a frame per icon.

`frame_wood_D.png` is the median of those nine with the border-connected
low-variance region kept and the interior alphaed out. It IS the live D-rank
frame, not an imitation of it.

RULED 2026-08-30 (dauntless): border encodes quest rank.
  D wood (this plate, already live on ~20 missions - no rework)
  C copper/bronze     B silver     A gold

Metal plates are generated over lime, keyed, then MASKED WITH THIS PLATE'S ALPHA
so all four share pixel-identical geometry - band width, corner brackets, rivet
placement. The generation supplies material and lighting only; it never decides
the silhouette.

Open interior rect (fully clear of the plate): x 69-425, y 75-410. Subjects stay
inside it. Interiors generate full-bleed at 512x512; the plate covers the outer band.

Exposure: judge every composited icon with
  rawqc.py ICON.png --opaque --band listing_icon_framed
The band is measured off these same nine (see 25x_DATA_art_spec.json ->
exposure_bands) and is PROPOSED, not ratified.
