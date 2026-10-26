"""Pixel-art icon export: keyed full-size RGBA (chroma.py output, <=255 colours) -> 256 px, hard alpha edge,
re-mapped onto the source's OWN palette. Resizing alone (LANCZOS) blends edges back into ~17k colours; a fresh
small-palette quantize after the resize drops small accents (gold coins went grey at 96 colours). Mapping back to
the full-size palette keeps every accent and keeps edges crisp.
usage: icon_export.py KEYED_SRC DST"""
import sys
from PIL import Image
src, dst = sys.argv[1], sys.argv[2]
full = Image.open(src).convert("RGBA")
pal_src = full.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
im = full.resize((256, 256), Image.LANCZOS)
a = im.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
rgb = im.convert("RGB").quantize(palette=pal_src, dither=Image.Dither.NONE).convert("RGB")
out = rgb.convert("RGBA"); out.putalpha(a)
out = Image.composite(out, Image.new("RGBA", out.size, (0, 0, 0, 0)), a)  # clear RGB under transparent pixels
out.save(dst, "WEBP", lossless=True, method=6)
print(dst, len(out.getcolors(1 << 24)), "colours")
