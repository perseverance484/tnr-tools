"""Key a white background off an opaque render: colour-to-alpha (unmix white) on the border-connected light region only,
crop to the subject, pad to a transparent square with a margin, resize to 256, export lossless WebP."""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, dst, qc = sys.argv[1:4]
a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
light = a.min(axis=2) > float(sys.argv[4]) if len(sys.argv) > 4 else a.min(axis=2) > 170                     # candidate background / glow pixels
lab, _ = ndimage.label(light)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border))
# colour-to-alpha against white, only inside the border-connected light region
al = (255 - a).max(axis=2) / 255.0
al = np.where(bg, al, 1.0)
al = np.where(bg & (al < 0.035), 0.0, al)       # kill JPEG-ish noise in the field
safe = np.maximum(al, 1e-6)[..., None]
rgb = np.where(bg[..., None], (a - 255 * (1 - safe)) / safe, a)
rgb = np.clip(rgb, 0, 255)
out = np.dstack([rgb, al * 255]).astype(np.uint8)
im = Image.fromarray(out, "RGBA")
bbox = Image.fromarray((al > 0.04).astype(np.uint8) * 255).getbbox()
im = im.crop(bbox)
side = int(max(im.size) * 1.08)
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2))
sq = sq.resize((256, 256), Image.LANCZOS)
# Harden alpha: glow on white has no recoverable colour, so keep the subject and a thin anti-aliased rim only.
arr = np.asarray(sq).copy()
A = arr[..., 3].astype(np.float32)
A = np.where(A < 90, 0, np.where(A > 170, 255, (A - 90) * 255 / 80))
solid = ndimage.binary_erosion(A >= 255, iterations=1)
rim = (A > 0) & ~solid
A = np.where(ndimage.binary_dilation(solid, iterations=1) | (A >= 255), A, 0)
arr[..., 3] = A.astype(np.uint8)
arr[arr[..., 3] == 0, :3] = 0
sq = Image.fromarray(arr, "RGBA")
sq.save(dst, "WEBP", lossless=True, method=6)
dark = Image.new("RGBA", (256, 256), (24, 24, 28, 255)); dark.alpha_composite(sq)
mid = Image.new("RGBA", (256, 256), (120, 70, 20, 255)); mid.alpha_composite(sq)
row = Image.new("RGB", (512, 256)); row.paste(dark.convert("RGB"), (0, 0)); row.paste(mid.convert("RGB"), (256, 0))
row.save(qc)
