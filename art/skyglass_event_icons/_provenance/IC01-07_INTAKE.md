# Skyglass IC01-IC07 intake and DR01-DR06 recolours (2026-10-31)

- **Raws:** `raw/IC0n_raw_*.png`, the director-approved originals copied byte-for-byte (1254 x 1254 RGBA PNG). Hashes:
  `IC01-07_SHA256SUMS.txt` (`sha256sum -c` from the repo root).
- **Background:** all seven carry real (native) alpha, not a key. Subject alpha sits at 250-254, plus a faint alpha 1-24
  haze over the canvas; no lime or magenta field. So no keying: `state/skyglass_art/ic01_07_intake.py` clears the haze
  (alpha <= 24 to 0), makes the subject solid (alpha >= 232 to 255), removes detached islands under 64 px, trims, pads
  square with a small even margin (subject long side 92% of the canvas, so about 10 px each side at 256), resizes to
  256 px, firms the alpha and writes lossless webp. chroma.py is not run: with no key it would only quantize the whole
  1254 px image to 255 colours.
- **rawqc.py:** it has no native-alpha path, so it rejects every one of these at 0% coverage / 100% dirty ring. That is
  a known false reject, like the frame-plate gap in `skills/producing-tnr-art/data/frames/README.md`, so nothing was
  recorded to the scaffold ledger. An alpha-aware check was run instead: border ring clear 98-99.8% (the haze only), no
  subject touching the edge, a handful of near-key pixels inside the haze, none in the subject.
- **Recolours:** the same pipeline runs on the base raw after one region is recoloured: the gold seal (a seeded flood,
  stopped by the black outline) or the cord plus its wax dab (a hue band). Masked pixels are remapped by luminance onto
  a three-stop ramp, so the shading steps are kept. `--check` result: each derived export has alpha identical to its
  base, and visible changes only inside the seal or cord area.
- **Preflight:** `artpreflight.py --type ICON`: 0 errors, 0 warnings, 13 files (`IC01-07_artpreflight.json`). Soft
  edges 0.9-2.1%.
- **Ledger:** `IC01-07_ART_LEDGER.csv` (code, item id, filename, dimensions, bytes, sha256).
- **Upload:** push/352 (`push/skyglass_chart_icons.gen.py`). No live requests or uploads happened at intake.
