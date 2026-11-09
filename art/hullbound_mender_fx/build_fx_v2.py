#!/usr/bin/env python3
"""The Hullbound Mender combat clips, v2: built piece by piece from dauntless's paintings, in the approved Mother of
Echoes v9 painted-light method (tnr-animation/v9: kit9.py, pieces13.py, build_painted_moves.py).

Why v2: v1 mostly scaled, slid or faded one whole painting. Here every painting is cut into its own pieces (connected
components lifted off the black, plus angular / radial / along-axis splits of the big connected bodies), and each
piece gets its own timing, easing and path: plates punch up one after another and overshoot, cracks propagate along
their own axis behind a white front, shards fly on ballistic arcs with spin, sparks and motes rise on their own
phases, light builds before every hit and decays after it. Loops are periodic in every term, so they wrap seamlessly.

Light model (kit9): pieces are light on black, screened onto a 3x supersampled frame, bloomed, then turned into
colour + alpha (alpha from energy) so it reads as additive soft light over the dark board. Appears are drawn twice
stacked by the renderer, so their alpha is pre-compensated (a' = 1 - sqrt(1 - a)); loops are drawn once.

Geometry and export match v1 (mender_fx_v1.json): 150 px square frames, a vertical strip, 50 ms per frame, the hex
footprint 120 x 60 centred (2.5 hex-height clip, SKYGLASS_MENDER_PITCH.md section 9), lossless webp, 24 frames
(3600 px strip, under the 4096 px phone texture limit), each strip under 450 KB.

    python3 art/hullbound_mender_fx/build_fx_v2.py --src /mnt/project-files/tnr/art/mender_inbox \
        [--preview DIR] [--only key,key]
"""
import argparse, json, math, os, random, subprocess, shutil
from collections import deque
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "exports")
VER = "v2"
S, SS = 150, 3                 # output cell, supersampling
HI = S * SS
CX, CY = 75.0, 75.0            # hex centre (output px)
HW, HH = 120, 60               # hex footprint
SPEED = 50
N = 24                         # frames per clip
TAU = 2 * math.pi
WS = 502                       # working size the 1254 px paintings are cut at

CYAN = (.62, .86, 1.0)
GOLD = (1.0, .74, .32)
EMBER = (1.0, .55, .18)
SMOKE = (.70, .78, .84)


# ---------------------------------------------------------------------------------------------------- easing
def cl(t): return max(0.0, min(1.0, t))
def ease_out(t): t = cl(t); return 1 - (1 - t) ** 3
def ease_in(t): t = cl(t); return t ** 2.4
def ease_io(t): t = cl(t); return t * t * (3 - 2 * t)
def back_out(t, o=1.9):
    t = cl(t) - 1
    return 1 + t * t * ((o + 1) * t + o)
def bump(t, a, b):
    if t <= a or t >= b: return 0.0
    return math.sin(math.pi * (t - a) / (b - a))
def frac(x): return x - math.floor(x)


# ---------------------------------------------------------------------------------------------------- pieces
class Piece:
    """A light piece cut from a painting: rgb (light on black), its crop box centre c in working coords, plus maps
    (same shape as rgb[..., 0]) cropped from full-painting fields: t (along an axis), d (distance from a base), etc."""
    def __init__(self, rgb, box, **meta):
        self.rgb = rgb; self.box = box
        x0, y0, x1, y1 = box
        self.c = ((x0 + x1) / 2, (y0 + y1) / 2)
        self.maps = {}
        self.__dict__.update(meta)

    def crop(self, name, field):
        x0, y0, x1, y1 = self.box
        self.maps[name] = field[y0:y1, x0:x1]
        return self.maps[name]


def lift(path):
    im = Image.open(path).convert("RGB").resize((WS, WS), Image.LANCZOS)
    a = np.asarray(im, float) / 255
    m = a.max(axis=2, keepdims=True)
    return a * np.clip((m - .02) / .05, 0, 1)                    # true black, soft floor, no grey haze


def label(mask):
    """8-connected components of a bool mask -> (labels, [dict(id, n, x0, y0, x1, y1)])."""
    H, W = mask.shape
    lab = np.zeros((H, W), np.int32); comps = []; n = 0
    ys, xs = np.nonzero(mask)
    for y, x in zip(ys, xs):
        if lab[y, x]: continue
        n += 1; q = deque([(y, x)]); lab[y, x] = n; cnt = 0; bx0 = bx1 = x; by0 = by1 = y
        while q:
            a, b = q.popleft(); cnt += 1
            bx0 = min(bx0, b); bx1 = max(bx1, b); by0 = min(by0, a); by1 = max(by1, a)
            for c in (a - 1, a, a + 1):
                for d in (b - 1, b, b + 1):
                    if 0 <= c < H and 0 <= d < W and mask[c, d] and not lab[c, d]:
                        lab[c, d] = n; q.append((c, d))
        comps.append(dict(id=n, n=cnt, x0=bx0, y0=by0, x1=bx1, y1=by1))
    return lab, sorted(comps, key=lambda c: -c["n"])


def grow(mask, r):
    im = Image.fromarray((mask * 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.MaxFilter(2 * r + 1)), float) / 255


def soft(w, r):
    return np.asarray(Image.fromarray((np.clip(w, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r)), float) / 255


def cut(img, w, pad=4, **meta):
    a = img * w[..., None]
    ys, xs = np.nonzero(a.max(axis=2) > .02)
    if len(ys) == 0: return None
    x0, x1 = max(0, xs.min() - pad), min(WS, xs.max() + pad + 1)
    y0, y1 = max(0, ys.min() - pad), min(WS, ys.max() + pad + 1)
    return Piece(a[y0:y1, x0:x1].copy(), (x0, y0, x1, y1), **meta)


def comp_weight(lab, ids, grow_r=2, blur=1.5):
    m = np.isin(lab, ids).astype(float)
    return soft(grow(m, grow_r), blur) if grow_r else m


def partition(field, bounds, s):
    """Soft partition of unity over a scalar field split at `bounds` (sorted), edge softness s."""
    def step(x): return 1 / (1 + np.exp(-x / s))
    ws = []
    edges = [-1e9] + list(bounds) + [1e9]
    for lo, hi in zip(edges, edges[1:]):
        a = step(field - lo) if lo > -1e8 else 1.0
        b = step(field - hi) if hi < 1e8 else 0.0
        ws.append(np.clip(a - b, 0, 1))
    return ws


def valleys(field, weight, lo, hi, k, sep, smooth=5):
    """Pick up to k split values in [lo, hi] at the low points of the weight histogram over `field`."""
    bins = np.linspace(lo, hi, int(hi - lo) + 1)
    h, _ = np.histogram(field.ravel(), bins=bins, weights=weight.ravel())
    ker = np.ones(smooth) / smooth; h = np.convolve(h, ker, mode="same")
    cs = np.cumsum(h); tot = cs[-1]
    cand = [j for j in range(2, len(h) - 2) if h[j] <= h[j - 1] and h[j] <= h[j + 1]
            and .04 * tot < cs[j] < .96 * tot]
    cand.sort(key=lambda j: h[j])
    pick = []
    for j in cand:
        if all(abs(j - p) >= sep for p in pick): pick.append(j)
        if len(pick) >= k: break
    return sorted(bins[j] + .5 for j in pick)


def pca_t(img, mask=None, head_right=True):
    """Projection of every pixel on the bright pixels' main axis, 0 at one end, 1 at the other (right end = 1)."""
    lum = img.max(axis=2) if mask is None else mask
    ys, xs = np.nonzero(lum > .08); wts = lum[ys, xs]
    mx, my = np.average(xs, weights=wts), np.average(ys, weights=wts)
    cov = np.cov(np.vstack([xs - mx, ys - my]), aweights=wts)
    ev, evec = np.linalg.eigh(cov); v = evec[:, -1]
    if (v[0] < 0) == head_right: v = -v
    YY, XX = np.mgrid[0:WS, 0:WS]
    p = (XX - mx) * v[0] + (YY - my) * v[1]
    pv = (xs - mx) * v[0] + (ys - my) * v[1]
    lo, hi = np.percentile(pv, 1), np.percentile(pv, 99)
    return (p - lo) / (hi - lo), v, (mx, my)


def local_peaks(lum, k, sep, thr=.5):
    """Up to k bright points at least sep px apart (glint spots)."""
    ys, xs = np.nonzero(lum > thr)
    order = np.argsort(-lum[ys, xs])
    pts = []
    for o in order:
        x, y = xs[o], ys[o]
        if all((x - a) ** 2 + (y - b) ** 2 >= sep * sep for a, b in pts): pts.append((x, y))
        if len(pts) >= k: break
    return pts


def tint(rgb, col, white=.45):
    lum = rgb.max(axis=2, keepdims=True)
    c = np.array(col, float).reshape(1, 1, 3)
    return np.clip(lum * c + white * np.clip(lum - .55, 0, 1) ** 1.5 * 2.2, 0, 1)


def hot(rgb, h):
    """Burn toward white by h (scalar or HxW): the hot front of a crack, a flash on arrival."""
    if np.isscalar(h):
        if h <= 0: return rgb
        h = np.full(rgb.shape[:2], h)
    h = np.clip(h, 0, 1)[..., None]
    lum = rgb.max(axis=2, keepdims=True)
    return np.clip(rgb * (1 - h) + np.minimum(1, lum * 1.25) * h, 0, 1)


def blurred(rgb, r, gain=1.0):
    im = Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r))
    return np.clip(np.asarray(im, float) / 255 * gain, 0, 1)


def dot(r=6, col=CYAN, core=.6):
    """A soft round mote: a gaussian with a hot centre."""
    y, x = np.mgrid[-2 * r:2 * r + 1, -2 * r:2 * r + 1]
    g = np.exp(-(x * x + y * y) / (2 * (r / 2.0) ** 2))
    c = np.array(col).reshape(1, 1, 3)
    return np.clip(g[..., None] * c + core * g[..., None] ** 3, 0, 1)


class Kit:
    """Everything cut from the paintings, with the fields the clips animate."""
    def __init__(self, src):
        rnd = random.Random(7)
        L = lambda n: lift(os.path.join(src, n + ".png"))
        self.YY, self.XX = np.mgrid[0:WS, 0:WS]

        # P1: three frost seams (the three largest components), each with an along-seam field for crack propagation.
        p1 = L("P1_hull_omen"); self.p1 = p1
        lab, cs = label(p1.max(axis=2) > .16)
        big = cs[:3]
        rest = [c["id"] for c in cs[3:]]
        self.seams = []
        for c in sorted(big, key=lambda c: c["y0"]):
            w = comp_weight(lab, [c["id"]], 3, 2)
            t, v, _ = pca_t(p1 * w[..., None])
            pc = cut(p1, w); pc.crop("t", t)
            pc.glints = local_peaks((p1 * w[..., None]).max(axis=2), 4, 40, .6)
            self.seams.append(pc)
        self.p1_box = self._bbox(p1)
        self.p1_glow = blurred(p1, 18, 2.2)

        # P2: the crystal cluster split into plates by angle round its base; small components are chips.
        p2 = L("P2_hull_closes"); self.p2 = p2
        lab, cs = label(p2.max(axis=2) > .14)
        body = comp_weight(lab, [cs[0]["id"]], 3, 1.5)
        lum = p2.max(axis=2) * body
        ys, xs = np.nonzero(lum > .15)
        by = ys.max() - 6
        low = lum[by - 40:by + 6]
        bx = np.average(np.arange(WS)[None, :].repeat(low.shape[0], 0), weights=low + 1e-9)
        self.p2_base = (bx, by)
        ang = np.degrees(np.arctan2(-(self.YY - by), self.XX - bx))
        dist = np.hypot(self.XX - bx, self.YY - by)
        bounds = valleys(np.where(dist > 40, ang, -999), lum * (dist > 40), 5, 175, 6, 9)
        self.plates = []
        for w in partition(ang, bounds, 2.2):
            pc = cut(p2, w * body)
            if pc is None: continue
            sub = (p2.max(axis=2) * w * body)
            if sub.sum() < 50: continue
            th = np.degrees(np.arctan2(-(np.average(self.YY, weights=sub + 1e-9) - by), np.average(self.XX, weights=sub + 1e-9) - bx))
            pc.theta = th
            pc.crop("d", dist); pc.length = float(np.percentile(dist[sub > .2], 99))
            self.plates.append(pc)
        self.p2_chips = [cut(p2, comp_weight(lab, [c["id"]], 2, 1)) for c in cs[1:16]]
        self.p2_box = self._bbox(p2)

        # P3: the chalk line, laid along x (rotated 90 deg): hot core, dust halo, loose specks.
        p3 = np.rot90(L("P3_chalk_line"), -1).copy()
        lum = p3.max(axis=2)
        core_w = soft(np.clip((lum - .45) / .25, 0, 1), 1.2)
        lab, cs = label(lum > .12)
        line_w = comp_weight(lab, [cs[0]["id"]], 4, 2)
        tx = (self.XX - self.XX[lum > .1].min()) / (self.XX[lum > .1].max() - self.XX[lum > .1].min())
        self.line_core = cut(p3, core_w * line_w, 6); self.line_core.crop("t", tx)
        self.line_halo = cut(p3, np.clip(line_w - core_w, 0, 1), 6); self.line_halo.crop("t", tx)
        self.line_halo_blur = cut(blurred(p3 * np.clip(line_w - core_w, 0, 1)[..., None], 3, 1.6), np.ones((WS, WS)), 8)
        self.line_specks = [cut(p3, comp_weight(lab, [c["id"]], 2, .8), 3) for c in cs[1:40] if c["n"] >= 3]
        self.p3_vert = np.rot90(self.line_core.rgb, 1).copy()                    # the core standing upright

        # P4: deck burst. The big body is split into wedges by angle round its base; loose shards are components.
        p4 = L("P4_deck_splits"); self.p4 = p4
        lab, cs = label(p4.max(axis=2) > .12)
        body = comp_weight(lab, [cs[0]["id"]], 2, 1.2)
        lum = p4.max(axis=2) * body
        ys, xs = np.nonzero(lum > .2)
        by = ys.max() - 4
        low = lum[by - 30:by + 4]
        bx = np.average(np.arange(WS)[None, :].repeat(low.shape[0], 0), weights=low + 1e-9)
        self.p4_base = (bx, by)
        ang = np.degrees(np.arctan2(-(self.YY - by), self.XX - bx))
        dist = np.hypot(self.XX - bx, self.YY - by)
        bounds = valleys(np.where(dist > 30, ang, -999), lum * (dist > 30), 5, 175, 7, 10)
        self.wedges = []
        for w in partition(ang, bounds, 2.5):
            sub = p4.max(axis=2) * w * body
            if sub.sum() < 50: continue
            pc = cut(p4, w * body)
            pc.theta = float(np.degrees(np.arctan2(-(np.average(self.YY, weights=sub + 1e-9) - by), np.average(self.XX, weights=sub + 1e-9) - bx)))
            pc.crop("d", dist); pc.length = float(np.percentile(dist[sub > .2], 99))
            self.wedges.append(pc)
        self.shards = [cut(p4, comp_weight(lab, [c["id"]], 1, .8), 3) for c in cs[1:46] if c["n"] >= 6]
        self.p4_box = self._bbox(p4)
        self.p4_root = cut(p4, soft((dist < 70).astype(float), 8) * body, 4)    # the hot split root
        self.p4_root.crop("d", dist)

        # P5: plank body and its embers.
        p5 = L("P5_fresh_plank"); self.p5 = p5
        labw, csw = label(p5.max(axis=2) > .40)                 # the wood itself, without the sparks above it
        w = comp_weight(labw, [csw[0]["id"]], 4, 2)
        t, v, _ = pca_t(p5 * w[..., None])
        self.plank = cut(p5, w); self.plank.crop("t", t)
        self.plank_glow = blurred(tint(self.plank.rgb, GOLD, .2), 10, 1.4)
        self.plank_corners = local_peaks(p5.max(axis=2) * w, 5, 50, .75)
        lab, cs = label((p5.max(axis=2) > .2) & (w < .05))
        self.embers = [cut(p5, comp_weight(lab, [c["id"]], 2, .8), 3) for c in cs[:12] if c["n"] >= 2]
        self.embers = [e for e in self.embers if e is not None]
        self.p5_box = self._bbox(p5 * w[..., None])

        # P6: hammerfall, split by elliptical radius: the star, the floor cracks, the ring; loose debris.
        p6 = L("P6_hammerfall"); self.p6 = p6
        lab, cs = label(p6.max(axis=2) > .12)
        body = comp_weight(lab, [cs[0]["id"]], 2, 1.2)
        b = cs[0]
        rx = (b["x1"] - b["x0"]) / 2; ry = rx * .37
        ccx = (b["x0"] + b["x1"]) / 2; ccy = b["y1"] - ry - 4
        self.p6_c = (ccx, ccy); self.p6_r = (rx, ry)
        rho = np.hypot((self.XX - ccx) / rx, (self.YY - ccy) / ry)
        spike = ((self.YY < ccy) & (np.abs(self.XX - ccx) < 22)).astype(float)
        spike = soft(spike * (self.YY > ccy - 130), 6)
        wst, wcr, wring = partition(rho, [.30, .72], .045)
        wst = np.clip(wst + spike * (rho < .9), 0, 1); wcr = wcr * (1 - spike); wring = wring * (1 - spike)
        self.star = cut(p6, wst * body, 6)
        self.cracks6 = cut(p6, wcr * body, 4); self.cracks6.crop("rho", rho)
        self.ring = cut(p6, wring * body, 4)
        angf = np.degrees(np.arctan2((self.YY - ccy) / ry, (self.XX - ccx) / rx)) % 360
        self.ring.crop("ang", angf)
        self.debris6 = [cut(p6, comp_weight(lab, [c["id"]], 1, .8), 3) for c in cs[1:40] if c["n"] >= 4]
        self.debris6 = [d for d in self.debris6 if d is not None]
        self.star_glow = blurred(self.star.rgb, 12, 2.0)

        # P7: rivet split along its flight axis into head and trail; loose chips.
        p7 = L("P7_rivet"); self.p7 = p7
        lab, cs = label(p7.max(axis=2) > .12)
        body = comp_weight(lab, [cs[0]["id"]], 2, 1.2)
        t, v, _ = pca_t(p7 * body[..., None])
        self.rivet_axis = v
        wtrail, whead = partition(t, [.70], .03)
        self.rivet_head = cut(p7, whead * body, 4)
        self.rivet_trail = cut(p7, wtrail * body, 4); self.rivet_trail.crop("t", t)
        self.rivet_chips = [cut(p7, comp_weight(lab, [c["id"]], 1, .8), 3) for c in cs[1:14] if c["n"] >= 4]
        self.rivet_angle = math.degrees(math.atan2(-v[1], v[0]))                # painted flight direction (deg, y up)

        # extras: grey smoke wisps (four columns) and teal cracks (three), used as dust and floor cracks.
        sm = L("extra_grey_smoke")
        lab, cs = label(sm.max(axis=2) > .10)
        cols = sorted(cs[:4], key=lambda c: c["x0"])
        self.smoke = [cut(sm, comp_weight(lab, [c["id"]], 3, 2), 4) for c in cols]
        for s in self.smoke: s.crop("v", (self.YY - s.box[1]) / max(1, s.box[3] - s.box[1]))
        self.smoke_soft = []                                    # blurred and greyed: dust puffs, not thin squiggles
        for s in self.smoke:
            q = Piece(np.clip(blurred(s.rgb, 13, 2.6) * np.array(SMOKE), 0, 1), s.box); q.maps = s.maps
            self.smoke_soft.append(q)
        self.star_cyan = tint(self.star.rgb, CYAN, .3)
        self.star_glow_cyan = tint(self.star_glow, CYAN, .1)
        tc = L("extra_teal_cracks")
        lab, cs = label(tc.max(axis=2) > .10)
        cols = sorted(cs[:3], key=lambda c: c["x0"])
        self.tcracks = []
        for c in cols:
            w = comp_weight(lab, [c["id"]], 3, 1.5)
            pc = cut(tc, w, 4)
            rgb = np.rot90(tint(pc.rgb, CYAN, .5), -1).copy()                  # lying along x
            h, wd = rgb.shape[:2]
            self.tcracks.append(Piece(rgb, (0, 0, wd, h)))
            self.tcracks[-1].maps["t"] = np.tile(np.linspace(0, 1, wd)[None, :], (h, 1))

        self.dot_s = dot(6, (.55, .62, .68), core=0.0)
        self.dot_c = dot(6, CYAN); self.dot_g = dot(6, EMBER); self.dot_w = dot(6, (.9, .95, 1.0))

    def _bbox(self, img):
        ys, xs = np.nonzero(img.max(axis=2) > .06)
        return xs.min(), ys.min(), xs.max(), ys.max()


# ---------------------------------------------------------------------------------------------------- frame
def hex_mask(feather=3, inset=2):
    m = Image.new("L", (HI, HI), 0)
    w, h = (HW / 2 - inset) * SS, (HH / 2 - inset) * SS
    cx, cy = CX * SS, CY * SS
    ImageDraw.Draw(m).polygon([(cx - w, cy), (cx - w / 2, cy - h), (cx + w / 2, cy - h), (cx + w, cy),
                               (cx + w / 2, cy + h), (cx - w / 2, cy + h)], fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(feather * SS)), float)[..., None] / 255


HEXM = hex_mask()
_rs = {}


def _resize(arr, w, h, rot, flat):
    key = (id(arr), w, h, round(rot, 2), round(flat, 3))
    if key in _rs: return _rs[key][1]
    im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
    if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
    if flat != 1.0: im = im.resize((im.width, max(1, int(im.height * flat))), Image.LANCZOS)
    a = np.asarray(im, float) / 255
    if len(_rs) > 600: _rs.clear()
    _rs[key] = (arr, a)                       # keep arr alive so its id is not reused
    return a


class Frame:
    def __init__(self):
        self.layers = {"L": np.zeros((HI, HI, 3)), "F": np.zeros((HI, HI, 3))}   # F = floor, clipped to the hex

    def layer(self, name):
        if name not in self.layers: self.layers[name] = np.zeros((HI, HI, 3))
        return self.layers[name]

    def put(self, src, cx, cy, scale, k=1.0, rot=0.0, sx=1.0, sy=1.0, flat=1.0, mask=None, heat=None,
            layer="L", clipy=None, wave=None):
        """Screen a light piece at (cx, cy) output px, `scale` output px per source px, times k.
        rot (deg, ccw) is applied after scaling, then `flat` squashes the result vertically (floor perspective).
        mask/heat are per-pixel maps on the source; clipy hides everything below that frame y (a deck line);
        wave(xn) -> dy output px displaces columns (a vibrating string)."""
        if k <= 0.004: return
        arr = src.rgb if isinstance(src, Piece) else src
        dyn = mask is not None or heat is not None
        if mask is not None: arr = arr * np.clip(mask, 0, None)[..., None]
        if heat is not None: arr = hot(arr, heat)
        w = max(2, int(arr.shape[1] * scale * SS * sx)); h = max(2, int(arr.shape[0] * scale * SS * sy))
        if dyn:
            im = Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.LANCZOS)
            if rot: im = im.rotate(rot, Image.BICUBIC, expand=True)
            if flat != 1.0: im = im.resize((im.width, max(1, int(im.height * flat))), Image.LANCZOS)
            a = np.asarray(im, float) / 255
        else:
            a = _resize(arr, w, h, rot, flat)
        if wave is not None:
            hh, ww = a.shape[:2]; pad = int(8 * SS)
            b = np.zeros((hh + 2 * pad, ww, 3))
            for x in range(ww):
                dy = int(round(wave(x / max(1, ww - 1)) * SS))
                b[pad + dy:pad + dy + hh, x] = a[:, x]
            a = b
        hh, ww = a.shape[:2]
        x0 = int(cx * SS - ww / 2); y0 = int(cy * SS - hh / 2)
        xs, ys = max(0, x0), max(0, y0); xe, ye = min(HI, x0 + ww), min(HI, y0 + hh)
        if xe <= xs or ye <= ys: return
        s = a[ys - y0:ye - y0, xs - x0:xe - x0] * k
        if clipy is not None:
            yy = np.arange(ys, ye)[:, None, None]
            s = s * np.clip((clipy * SS - yy) / (1.5 * SS), 0, 1)
        L = self.layer(layer)
        L[ys:ye, xs:xe] = 1 - (1 - L[ys:ye, xs:xe]) * (1 - np.clip(s, 0, 1))

    def modulate(self, layer, fn):
        """Multiply a layer by fn(X, Y) (output px grids)."""
        Y, X = np.mgrid[0:HI, 0:HI] / SS
        self.layers[layer] = np.clip(self.layers[layer] * fn(X, Y)[..., None], 0, 1)

    def merge(self, name, into="L"):
        a = self.layers.pop(name)
        L = self.layer(into); self.layers[into] = 1 - (1 - L) * (1 - a)

    def bloom(self, r=2.2, g=.85):
        L = 1 - (1 - self.layers["L"]) * (1 - self.layers["F"] * HEXM)
        for name in list(self.layers):
            if name not in ("L", "F"): L = 1 - (1 - L) * (1 - self.layers[name])
        b = np.stack([np.asarray(Image.fromarray((L[..., c] * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(r * SS)), float) / 255
                      for c in range(3)], axis=2)
        self.out = 1 - (1 - L) * (1 - np.clip(b * g, 0, 1))
        return self

    def finish(self, stacked, amul=1.7):
        L = self.out
        A = np.clip(L.max(axis=2, keepdims=True) * amul, 0, 1)
        P = np.clip(L, 0, 1)
        e = np.minimum(np.arange(HI), np.arange(HI)[::-1]) / SS
        f = np.clip(e / 6.0, 0, 1); f = f * f * (3 - 2 * f); f = np.minimum(f[None, :], f[:, None])[..., None]
        P = P * f; A = A * f
        if stacked:
            A2 = 1 - np.sqrt(np.clip(1 - A, 0, 1)); P = P * (A2 / np.maximum(A, 1e-6)); A = A2
        def down(x): return x.reshape(S, SS, S, SS, x.shape[2]).mean(axis=(1, 3))
        Ad = down(A); C = down(P) / np.maximum(Ad, 1e-6)
        o = np.zeros((S, S, 4), np.uint8)
        o[..., :3] = np.clip(C * 255 + .5, 0, 255); o[..., 3] = np.clip(Ad[..., 0] * 255 + .5, 0, 255)
        o[o[..., 3] < 5] = 0
        o[..., :3] = (o[..., :3] // 4) * 4; o[..., 3] = (o[..., 3] // 2) * 2
        o[:1] = 0; o[-1:] = 0; o[:, :1] = 0; o[:, -1:] = 0
        return Image.fromarray(o, "RGBA")


def blank(): return Image.new("RGBA", (S, S), (0, 0, 0, 0))


def tf(origin, anchor, g, flat=1.0):
    """Working coords -> frame coords: origin (working) lands on anchor (frame), scale g, vertical squash flat."""
    ox, oy = origin; ax, ay = anchor
    return lambda x, y: (ax + (x - ox) * g, ay + (y - oy) * g * flat)


# ---------------------------------------------------------------------------------------------------- clips
def a1_hull_omen(K):
    """Loop. Three frost seams lie in the deck. Each breathes open on its own phase while a white front runs along it
    (lower left to upper right); frost tips twinkle; cold motes lift off the seams; a cold under-glow pulses."""
    x0, y0, x1, y1 = K.p1_box
    g = 110 / (x1 - x0); fl = .56
    T = tf(((x0 + x1) / 2, (y0 + y1) / 2), (CX, CY), g, fl)
    rnd = random.Random(11)
    motes = []
    for j in range(14):
        sm = K.seams[j % 3]
        ys, xs = np.nonzero(sm.rgb.max(axis=2) > .5)
        q = rnd.randrange(len(xs))
        motes.append((sm.box[0] + xs[q], sm.box[1] + ys[q], rnd.random(), rnd.choice((1, 1, 2)), rnd.uniform(2.2, 3.6)))
    def f(i):
        F = Frame(); ph = i / N
        F.put(K.p1_glow, CX, CY + 2, g * 1.05, .22 + .12 * math.sin(TAU * ph), flat=fl, layer="F")
        for j, sm in enumerate(K.seams):
            off = j / 3
            br = .5 + .5 * math.sin(TAU * (ph + off))
            u = -.3 + 1.9 * frac(ph + off * .7)                 # the lit trail is gone past t=1 before it wraps
            t = sm.maps["t"]
            band = np.exp(-((t - u) / .10) ** 2)
            trail = np.clip(1 - (u - t) / .5, 0, 1) * (t < u)               # the seam stays lit behind the front
            m = .30 + .25 * br + 1.5 * band + .35 * trail
            x, y = T(*sm.c)
            F.put(sm, x, y, g, 1.0, flat=fl * (1 + .14 * br), mask=m, heat=band * .85, layer="F")
            for gx, gy in sm.glints:
                p = (gx * .013 + gy * .021 + j * .37) % 1
                tw = max(0.0, math.sin(TAU * (2 * ph + p))) ** 6
                gx2, gy2 = T(gx, gy)
                F.put(K.star.rgb, gx2, gy2, 9 / K.star.rgb.shape[1], 1.3 * tw, rot=45 * p)
        for mx, my, p, r, sz in motes:
            a = frac(ph * r + p)
            x, y = T(mx, my)
            F.put(K.dot_c, x + 2.5 * math.sin(TAU * (a + p)), y - 16 * ease_out(a), sz / 12, .9 * math.sin(math.pi * a) ** 1.5)
        return F.bloom(2.0, .8).finish(False)
    return f, "loop"


def plate_layout(K, height, base):
    x0, y0, x1, y1 = K.p2_box
    g = height / (y1 - y0)
    return g, tf(K.p2_base, base, g)


def a2_hull_close(K):
    """Appear. Light runs in along the seams and gathers at one point; the skyglass plates punch up through the deck
    one by one (centre first), each growing from the base along its own axis, overshooting and flashing as it lands;
    chips burst off; a lock flash rings the base and a light band sweeps the plates; then they sink back in turn
    and leave the faint glass-grown floor."""
    base = (CX, CY + 16)
    g, T = plate_layout(K, 78, base)
    order = sorted(range(len(K.plates)), key=lambda j: abs(K.plates[j].theta - 90))
    start = {j: 4.0 + r * .9 for r, j in enumerate(order)}
    sink = {j: 13.0 + r * .8 for r, j in enumerate(order[::-1])}
    sx0, sy0, sx1, sy1 = K.p1_box; gs = 108 / (sx1 - sx0)
    Ts = tf(((sx0 + sx1) / 2, (sy0 + sy1) / 2), (CX, CY + 2), gs, .5)
    rnd = random.Random(5)
    conv = [(rnd.uniform(0, TAU), rnd.uniform(36, 52), rnd.uniform(0, 1.2)) for _ in range(10)]
    chips = []
    for c in K.p2_chips:
        if c is None: continue
        px, py = T(*c.c); dx, dy = px - base[0], py - base[1]
        chips.append((c, dx, dy, rnd.uniform(4.5, 7.0), rnd.uniform(-40, 40)))
    floor = a2_floor_pieces(K)
    def f(i):
        F = Frame()
        # anticipation: the seams light from their ends toward the middle, a glow gathers, motes converge
        if i <= 7:
            a = ease_in(cl((i + 1) / 5)) * (1 - ease_io(cl((i - 4) / 3)))
            for sm in K.seams:
                t = sm.maps["t"]; u = .5 * ease_io(cl((i + 1) / 5))
                front = np.exp(-((np.minimum(t, 1 - t) - u) / .08) ** 2)
                x, y = Ts(*sm.c)
                F.put(sm, x, y, gs, 1.0, flat=.5, mask=(.35 + 1.4 * front) * a, heat=front * .7, layer="F")
            gk = (.2, .45, .8, 1.2, 1.7, 2.0, 1.2, .5)[i]
            F.put(K.star_glow, base[0], base[1] - 2, 46 / K.star_glow.shape[1], gk, flat=.45)
            for ang, r0, p in conv:
                u = ease_in(cl((i + p) / 5.5))
                r = r0 * (1 - u)
                if u < 1: F.put(K.dot_c, base[0] + r * math.cos(ang), base[1] - 4 + r * math.sin(ang) * .45, .25, 1.1 * math.sin(math.pi * min(1, u * 1.1 + .05)))
        # the plates
        P = F.layer("P")
        for j, pc in enumerate(K.plates):
            s = (i - start[j]) / 3.2
            if s <= 0: continue
            rise = back_out(s, 2.2)
            dn = ease_in(cl((i - sink[j]) / 5.5))
            if dn >= 1: continue
            grow_ = max(0.0, min(1.12, rise)) * (1 - dn)
            th = math.radians(pc.theta)
            off = (1 - min(rise, 1.0) + dn * .6) * pc.length * g * .55
            x, y = T(*pc.c)
            x -= math.cos(th) * off; y += math.sin(th) * off + dn * 4
            reveal = np.clip((grow_ * pc.length * 1.06 - pc.maps["d"]) / 10 + 1, 0, 1)
            land = math.exp(-((i - start[j] - 3.0) / 1.1) ** 2)
            tilt = (pc.theta - 90) * .12 * (1 - ease_out(cl(s * 1.4)))
            k = (1.0 + .6 * land) * (1 - .35 * dn)
            F.put(pc, x, y, g, k, rot=-tilt, mask=reveal, heat=.35 * land + .4 * dn, layer="P", clipy=base[1] + 3)
        # lock: a light band sweeps the plates left to right, a ring flashes at the base
        if 9 <= i <= 15:
            u = -20 + 190 * ease_io((i - 9) / 5)
            F.modulate("P", lambda X, Y: 1 + 1.2 * np.exp(-(((X - u) + (Y - base[1]) * .55) / 13) ** 2))
        F.merge("P")
        if 9 <= i <= 14:
            v = ease_out((i - 9) / 5)
            F.put(K.ring, base[0], base[1] + 1, (56 + 50 * v) / K.ring.rgb.shape[1], 1.8 * (1 - v) ** 1.2, flat=.6)
        # chips burst off the base on arcs
        for c, dx, dy, sp, spin in chips:
            tt = i - 5.5
            if tt <= 0 or tt > 13: continue
            u = ease_out(tt / 5)
            x = base[0] + dx * (.3 + 1.2 * u); y = base[1] + dy * (.2 + 1.0 * u) + .5 * .9 * max(0, tt - 3) ** 2
            F.put(c, x, y, g * 1.2, 1.5 * (1 - tt / 13) ** 1.2, rot=spin * tt / 6)
        # the glass-grown floor forms as the plates go down
        if i >= 12:
            fk = ease_io(cl((i - 12) / 6)) * (1 - ease_in(cl((i - 18) / 5)))
            floor(F, (i % N) / N, fk * 1.25)
        # frost motes rise in the follow-through
        for j in range(8):
            tt = i - 10 - j * .7
            if 0 < tt < 12:
                F.put(K.dot_c, base[0] - 34 + j * 9.5, base[1] - 4 - 2.2 * tt, .22, .9 * math.sin(math.pi * tt / 12))
        return F.bloom(2.2, .85).finish(True)
    return f, "appear"


def a2_floor_pieces(K):
    """The lasting floor: each skyglass plate laid flat in the deck as a facet radiating from the centre."""
    n = len(K.plates)
    rnd = random.Random(3)
    lay = []
    for j, pc in enumerate(K.plates):
        a = 360 * j / n + rnd.uniform(-12, 12)
        r = rnd.uniform(14, 22)
        lay.append((pc, a, r, rnd.random()))
    g = 46 / max(pc.length for pc in K.plates)
    sx0, sy0, sx1, sy1 = K.p1_box; gs = 104 / (sx1 - sx0)
    Ts = tf(((sx0 + sx1) / 2, (sy0 + sy1) / 2), (CX, CY), gs, .5)
    def draw(F, ph, k, glints=True):
        for sm in K.seams:
            x, y = Ts(*sm.c)
            F.put(sm, x, y, gs, .16 * k, flat=.5, layer="F")
        for pc, a, r, p in lay:
            pulse = .5 + .5 * math.sin(TAU * (ph + p))
            a2 = a + 4 * math.sin(TAU * (ph + p * .5))               # each facet turns a little on its own phase
            ar = math.radians(a2); rr = r * (1 + .08 * pulse)
            x = CX + rr * math.cos(ar); y = CY - rr * math.sin(ar) * .5
            F.put(pc, x, y, g, (.22 + .32 * pulse) * k, rot=a2 - pc.theta, flat=.5, layer="F", heat=.25 * pulse ** 4)
        if glints:
            for pc, a, r, p in lay:
                tw = max(0.0, math.sin(TAU * (ph * 2 + p))) ** 8
                ar = math.radians(a); rr = r + pc.length * g * .55
                F.put(K.star.rgb, CX + rr * math.cos(ar), CY - rr * math.sin(ar) * .5, 10 / K.star.rgb.shape[1], 1.3 * tw * k, rot=30 * p)
    return draw


def a2_hull_floor(K):
    """Loop. Skyglass plates lie flat in the deck as facets; each breathes on its own phase, a specular band crosses
    the glass once per loop, facet tips twinkle, a few cold motes lift."""
    draw = a2_floor_pieces(K)
    rnd = random.Random(21)
    motes = [(rnd.uniform(CX - 44, CX + 44), rnd.uniform(CY - 14, CY + 14), rnd.random(), rnd.choice((1, 2))) for _ in range(7)]
    def f(i):
        F = Frame(); ph = i / N
        draw(F, ph, 1.0)
        u = -40 + 230 * ph                                       # band position (wraps off-hex at both ends)
        F.modulate("F", lambda X, Y: 1 + 2.0 * np.exp(-(((X - u) - (Y - CY) * 1.2) / 12) ** 2))
        for x, y, p, r in motes:
            a = frac(ph * r + p)
            F.put(K.dot_c, x + 2 * math.sin(TAU * (a + p)), y - 14 * ease_out(a), .2, .75 * math.sin(math.pi * a) ** 1.5)
        return F.bloom(2.0, .8).finish(False)
    return f, "loop"


LINE_Y = 80.0


def line_geo(K, width=116):
    pc = K.line_core
    g = width / pc.rgb.shape[1]
    return g


def a3_split_omen(K):
    """Loop. A chalk line lies along the keel. Once a loop it is snapped: a white front runs end to end, the line
    twangs (a decaying standing wave), chalk dust puffs off where the front passed and drifts up, the halo lifts and
    settles, a cold glow under the line swells and ebbs; the end points glint."""
    g = line_geo(K)
    rnd = random.Random(9)
    specks = []
    for j in range(26):
        sp = K.line_specks[j % len(K.line_specks)].rgb if j % 3 == 0 else K.dot_c
        tx = rnd.uniform(.04, .96)
        specks.append((sp, tx, rnd.uniform(-5, 5), rnd.uniform(10, 22), rnd.uniform(.4, .68), rnd.uniform(-30, 30),
                       rnd.uniform(.18, .3)))
    glow = blurred(K.line_core.rgb, 6, 2.0)
    def f(i):
        F = Frame(); ph = i / N
        u = -.2 + 1.4 * ease_in(cl(ph / .28))                   # the snap front, first 28% of the loop
        env = bump(ph, .06, .75) * (1 - ph)                      # the twang after it
        def wave(xn): return 4.0 * env * math.sin(math.pi * xn) * math.cos(TAU * 5 * ph)
        t = K.line_core.maps["t"]
        band = np.exp(-((t - u) / .06) ** 2)
        lit = .7 + .3 * env + .4 * np.clip(1 - np.abs(t - u) / .5, 0, 1) * (t < u)
        F.put(glow, CX, LINE_Y + 1, g, .35 + .45 * env, sy=2.4, layer="F")
        th = K.line_halo.maps["t"]
        F.put(K.line_halo, CX, LINE_Y, g, .6 + .4 * env, sy=1.4, mask=.7 + 1.4 * np.exp(-((th - u) / .1) ** 2), wave=wave)
        F.put(K.line_core, CX, LINE_Y, g, 1.1, sy=1.7, mask=lit + 2.0 * band, heat=band, wave=wave)
        F.put(K.line_halo_blur, CX, LINE_Y - 3 - 7 * env, g, .7 * env, sy=1.2 + 2.5 * env)
        for sp, tx, dx, rise, life, spin, sz in specks:
            born = cl((tx + .2) / 1.4) ** (1 / 2.4) * .28       # when the front passed this point
            age = frac(ph - born)
            if age >= life: continue
            a = age / life
            x = CX - 58 + 116 * tx + dx * a
            sc = sz if sp is K.dot_c else g * 2.2
            F.put(sp, x, LINE_Y - 1 - rise * ease_out(a), sc, 1.3 * (1 - a) ** 1.3 * min(1, a * 6), rot=spin * a)
        for tx, p in ((0.02, 0), (0.98, .5)):
            tw = .4 + .6 * max(0.0, math.sin(TAU * (ph + p))) ** 4
            F.put(K.star.rgb, CX - 58 + 116 * tx, LINE_Y, 12 / K.star.rgb.shape[1], 1.2 * tw, rot=20 * p)
        return F.bloom(2.0, .8).finish(False)
    return f, "loop"


def a4_split_break(K):
    """Appear. Three teal cracks run along the chalk line behind a white front while light gathers in the middle;
    a white flash; the deck bursts: wedges of splintered deck and glass erupt from the root one after another
    (middle first) and overshoot, loose shards fly on ballistic arcs with spin, then the wedges topple outward and
    fall, the floor crack glow flickers down and dust smoke rises and thins."""
    g_line = line_geo(K); fl = .55
    base = (CX, LINE_Y + 2)
    x0, y0, x1, y1 = K.p4_box
    g = 78 / (y1 - y0)
    T = tf(K.p4_base, base, g)
    order = sorted(range(len(K.wedges)), key=lambda j: abs(K.wedges[j].theta - 90))
    start = {j: 5.0 + r * .7 for r, j in enumerate(order)}
    rnd = random.Random(4)
    topple = {j: (12.0 + rnd.uniform(0, 3), rnd.uniform(14, 28)) for j in range(len(K.wedges))}
    shards = []
    for sh in K.shards:
        if sh is None: continue
        px, py = T(*sh.c)
        shards.append((sh, px - base[0], py - base[1], 5.0 + rnd.uniform(0, 2.5), rnd.uniform(-60, 60)))
    cr = [(K.tcracks[j], -26 + 26 * j + rnd.uniform(-4, 4), (-2.5, 1.5, -1)[j], j * .9) for j in range(3)]
    def f(i):
        F = Frame()
        # cracks along the line
        crk = 1.0 if i <= 6 else max(0.0, 1 - (i - 6) / 15) * (.8 + .2 * math.sin(i * 2.3))
        for pc, dx, dy, lag in cr:
            u = ease_io(cl((i + 1 - lag) / 4.5)) * 1.15
            t = pc.maps["t"]
            front = np.exp(-((t - u) / .07) ** 2) * (i <= 6)
            m = np.clip((u - t) / .05 + 1, 0, 1) * (1.0 + 1.2 * front)
            gg = 52 / pc.rgb.shape[1]
            F.put(pc, base[0] + dx, base[1] + dy, gg, 1.4 * crk, flat=.5, mask=m, heat=front, layer="F")
        if i <= 7:
            lk = (.6, .8, 1.0, 1.3, 1.6, 2.0, 1.2, .5)[i]
            F.put(K.line_core, CX, LINE_Y, g_line, lk, sy=1.7, heat=cl((i - 2) / 3) * .6)
            F.put(K.star_glow, base[0], base[1] - 3, (24 + 10 * i) / K.star_glow.shape[1], (.3 + .3 * i) if i < 5 else 2.2 * (1 - (i - 5) / 3), flat=.6)
        if i in (5, 6):
            F.put(K.star.rgb, base[0], base[1] - 8, (62 if i == 5 else 50) / K.star.rgb.shape[1], 2.1 if i == 5 else 1.4)
        # the root glow under the burst
        if i >= 5:
            rk = (2.0, 1.7, 1.4)[i - 5] if i <= 7 else 1.2 * max(0, 1 - (i - 7) / 13) * (.85 + .15 * math.sin(i * 3.1))
            x, y = T(*K.p4_root.c)
            F.put(K.p4_root, x, y, g, rk, heat=.5 if i <= 6 else 0)
        # wedges erupt and topple
        for j, pc in enumerate(K.wedges):
            s = (i - start[j]) / 2.6
            if s <= 0: continue
            rise = back_out(s, 2.0)
            t0, tilt = topple[j]
            tp = ease_in(cl((i - t0) / 8))
            if tp >= 1: continue
            th = math.radians(pc.theta)
            side = 1 if pc.theta < 90 else -1
            off = (1 - min(rise, 1.0)) * pc.length * g * .5
            x, y = T(*pc.c)
            x -= math.cos(th) * off; y += math.sin(th) * off
            x += side * 10 * tp; y += 16 * tp * tp
            reveal = np.clip((max(0.0, min(1.1, rise)) * pc.length * 1.05 - pc.maps["d"]) / 9 + 1, 0, 1)
            land = math.exp(-((i - start[j] - 2.4) / 1.0) ** 2)
            F.put(pc, x, y, g, (1.2 + .9 * land) * (1 - tp), rot=-side * tilt * tp, mask=reveal, heat=.55 * land,
                  clipy=base[1] + 4 + 30 * tp)
        # loose shards on ballistic arcs
        for sh, dx, dy, t0, spin in shards:
            tt = i - t0
            if tt <= 0 or tt > 14: continue
            u = ease_out(tt / 4)
            x = base[0] + dx * (.15 + 1.05 * u) + dx * .03 * max(0, tt - 4)
            y = base[1] + dy * (.1 + 1.0 * u) + .55 * max(0, tt - 3.5) ** 2
            F.put(sh, x, y, g * 1.15, 1.6 * (1 - tt / 14) ** 1.1, rot=spin * tt / 8)
        # dust smoke rises from the split and thins
        for j, (dx, sc, lag) in enumerate(((-24, 44, 0), (20, 48, 1.5), (-4, 52, 3), (34, 40, 2))):
            tt = i - 8 - lag
            if tt <= 0: continue
            a = cl(tt / 14)
            sm = K.smoke_soft[j % 4]
            rv = np.clip((ease_out(cl(tt / 6)) * 1.1 - (1 - sm.maps["v"])) / .2 + 1, 0, 1)
            h = sc * (1 + .4 * a) / sm.rgb.shape[0]
            F.put(sm, base[0] + dx + (2 if dx > 0 else -2) * tt * .5, base[1] - sc * .45 - 8 * a, h,
                  .45 * math.sin(math.pi * cl(tt / 15)), mask=rv, sx=1.7 + .7 * a)
        return F.bloom(2.2, .85).finish(True)
    return f, "appear"


def a5_fresh_plank(K):
    """Loop. The new-cut plank floats and breathes (bob and tilt on separate phases), a warm sheen runs along its
    grain once a loop, its gold under-glow pulses, embers rise off it on their own paths, corner glints twinkle."""
    x0, y0, x1, y1 = K.p5_box
    g = 100 / (x1 - x0)
    pc = K.plank
    rnd = random.Random(15)
    ys, xs = np.nonzero(pc.rgb.max(axis=2) > .5)
    top = [(pc.box[0] + x, pc.box[1] + y) for x, y in zip(xs, ys) if y < np.percentile(ys, 35)]
    embers = []
    for j in range(14):
        ex, ey = top[rnd.randrange(len(top))]
        spr = K.embers[j % len(K.embers)].rgb if j % 2 == 0 and K.embers else K.dot_g
        embers.append((ex, ey, rnd.random(), rnd.choice((1, 1, 2)), rnd.uniform(22, 36), rnd.uniform(-1, 1), spr))
    T = tf(pc.c, (CX, CY - 2), g)
    def f(i):
        F = Frame(); ph = i / N
        bob = -1.8 * math.sin(TAU * ph); tilt = 1.4 * math.sin(TAU * ph + 1.1)
        F.put(K.plank_glow, CX, CY + 5 + bob * .3, g * 1.18, .22 + .16 * math.sin(TAU * ph + .6), flat=.8)
        u = -.35 + 1.7 * frac(ph + .15)
        t = pc.maps["t"]
        band = np.exp(-((t - u) / .09) ** 2)
        F.put(pc, CX, CY - 2 + bob, g, .82, rot=tilt, mask=1 + .55 * band, heat=.35 * band)
        for cx_, cy_ in K.plank_corners[:3]:
            p = (cx_ * .017 + cy_ * .011) % 1
            tw = max(0.0, math.sin(TAU * (ph * 2 + p))) ** 8
            x, y = T(cx_, cy_)
            F.put(K.star.rgb, x, y + bob, 10 / K.star.rgb.shape[1], 1.0 * tw, rot=40 * p)
        for ex, ey, p, r, rise, sway, spr in embers:
            a = frac(ph * r + p)
            x, y = T(ex, ey)
            sc = (6 if spr is K.dot_g else 9) / spr.shape[1]
            F.put(spr, x + 4 * sway * math.sin(TAU * (a + p)) + 3 * sway * a, y + bob - rise * ease_out(a), sc,
                  1.4 * math.sin(math.pi * a) ** 1.2 * (.8 + .2 * math.sin(TAU * 3 * a)))
        return F.bloom(1.8, .4).finish(False)
    return f, "loop"


def a6_hammerfall(K):
    """Appear. A falling streak of light drops onto the spot as a pressure glint swells (anticipation); impact: the
    white star and flash hold two frames; the shockwave ring runs out with a fainter echo ring behind it; the floor
    cracks open outward from the centre and flicker down; debris hops outward and falls; dust smoke rolls up off the
    rim; the star decays."""
    c = (CX, 82.0)
    rx, ry = K.p6_r
    g = 132 / (2 * rx)
    T = tf(K.p6_c, c, g)
    rnd = random.Random(8)
    puffs = [(rnd.uniform(0, TAU), rnd.uniform(.82, 1.08), rnd.uniform(0, 3), rnd.uniform(7, 11), rnd.uniform(4, 12)) for _ in range(40)]
    deb = []
    for d in K.debris6:
        px, py = T(*d.c)
        deb.append((d, px - c[0], py - c[1], rnd.uniform(4, 11), rnd.uniform(-90, 90), rnd.uniform(0, 1.5)))
    def f(i):
        F = Frame()
        if i <= 4:                                               # the fall streak and the pressure glint
            u = ease_in(cl((i + 1) / 4))
            hgt = 70
            v = K.p3_vert
            msk = np.clip((u * 1.2 - (1 - np.linspace(1, 0, v.shape[0])[:, None])) / .25 + 1, 0, 1) * np.ones(v.shape[:2])
            msk = np.clip((u * 1.15 - np.linspace(0, 1, v.shape[0])[:, None] * np.ones(v.shape[:2])) / .2 + 1, 0, 1)
            F.put(v, c[0], c[1] - hgt / 2 - 4, hgt / v.shape[0], 1.5 * (1 - cl((i - 3) / 2)), sx=1.6, mask=msk, heat=.5)
            F.put(K.star.rgb, c[0], c[1] - 6, (10 + 9 * i) / K.star.rgb.shape[1], .35 + .3 * i)
        if 4 <= i <= 10:                                         # impact: flash and star, held two frames
            k = (2.3, 2.0, 1.3, .9, .6, .35, .15)[i - 4]
            F.put(K.star_glow if i <= 5 else K.star_glow_cyan, c[0], c[1] - 4, 90 / K.star_glow.shape[1], k * .9, flat=.75)
            F.put(K.star if i <= 6 else K.star_cyan, c[0], c[1] - 6 - 2 * (i - 4) * .3, (70 - 2 * (i - 4)) / K.star.rgb.shape[1],
                  k if i <= 6 else k * .8, heat=.6 if i <= 5 else 0)
        if i >= 4:                                               # shockwave ring and its echo
            for lag, kk, grow_ in ((0, 1.0, 1.0), (2, .55, 1.12)):
                tt = i - 4 - lag
                if tt < 0: continue
                v = ease_out(cl(tt / 8))
                k = kk * (1.9 if tt < 2 else 1.6 * (1 - ease_in(cl((tt - 2) / 13))))
                F.put(K.ring, c[0], c[1] + 2 * v, g * (.3 + .7 * v) * grow_, k, heat=.5 * (1 - v))
        if i >= 5:                                               # floor cracks open outward from the centre
            u = ease_out(cl((i - 4) / 6)) * 1.15
            rho = K.cracks6.maps["rho"]
            m = np.clip((u - rho) / .08 + 1, 0, 1) * (1 + 1.2 * np.exp(-((rho - u) / .07) ** 2))
            fk = 1.5 if i < 11 else 1.5 * max(0, 1 - (i - 11) / 11) * (.75 + .25 * math.sin(i * 2.7))
            x, y = T(*K.cracks6.c)
            F.put(K.cracks6, x, y, g, fk, mask=m, layer="F")
        for d, dx, dy, hop, spin, lag in deb:                    # debris hops outward and falls
            tt = i - 5 - lag
            if tt <= 0 or tt > 15: continue
            u = ease_out(tt / 7)
            x = c[0] + dx * (.35 + .95 * u); y = c[1] + dy * (.35 + .95 * u) - hop * math.sin(math.pi * cl(tt / 9))
            F.put(d, x, y, g * 1.25, 1.5 * (1 - tt / 15) ** 1.1, rot=spin * tt / 10)
        for ang, r0, lag, sz, rise in puffs:                    # dust kicked up round the rim, rolling out and up
            tt = i - 6 - lag
            if tt <= 0 or tt > 17: continue
            a = tt / 17
            v = ease_out(cl(tt / 9))
            x = c[0] + math.cos(ang) * 66 * r0 * (.55 + .55 * v); y = c[1] + 2 + math.sin(ang) * 24 * r0 * (.55 + .55 * v) - rise * ease_out(a)
            F.put(K.dot_s, x, y, sz * (1 + 1.0 * a) / 12, .26 * math.sin(math.pi * min(1, a * 1.15)) ** .8)
        for j, (dx, lag) in enumerate(((-40, 3), (38, 4.5))):
            tt = i - 9 - lag
            if tt <= 0: continue
            a = cl(tt / 12)
            sm = K.smoke_soft[j]
            rv = np.clip((ease_out(cl(tt / 5)) * 1.1 - (1 - sm.maps["v"])) / .2 + 1, 0, 1)
            F.put(sm, c[0] + dx * (1 + .2 * a), c[1] - 18 - 6 * a, 40 / sm.rgb.shape[0], .3 * math.sin(math.pi * a), mask=rv, sx=2.2)
        return F.bloom(2.2, .85).finish(True)
    return f, "appear"


def a7_rivet_volley(K):
    """Appear. Three skyglass rivets, staggered: a glint marks each launch point, the rivet streaks in (its trail
    stretches out behind the head, the head accelerates), it punches in with a white star and a small ring, chips
    spray back, the head stays embedded glowing and cools, then all three fade."""
    tgt = (CX, CY - 8)
    shots = [(0, (-44, -40), (-7, 2)), (4, (-52, -14), (8, 6)), (8, (-26, -50), (1, -8))]
    hd = K.rivet_head; tr = K.rivet_trail
    gh = 24 / hd.rgb.shape[1]
    rnd = random.Random(2)
    chips = [(K.rivet_chips[j % len(K.rivet_chips)], rnd.uniform(-60, 60), rnd.uniform(5, 13), rnd.uniform(-90, 90)) for j in range(6)]
    def f(i):
        F = Frame()
        for s0, (ox, oy), (dx, dy) in shots:
            tx, ty = tgt[0] + dx, tgt[1] + dy
            sx, sy = tx + ox, ty + oy
            ang = math.degrees(math.atan2(-(ty - sy), tx - sx))           # flight direction, y up
            rot = ang - K.rivet_angle
            j = i - s0
            if 0 <= j <= 1:                                             # launch glint
                F.put(K.star.rgb, sx, sy, (8 + 6 * j) / K.star.rgb.shape[1], .9 + .5 * j)
            if 1 <= j <= 4:                                             # flight
                u = ease_in((j - .5) / 3.5)
                hx, hy = sx + (tx - sx) * u, sy + (ty - sy) * u
                L = 10 + 30 * min(1, u * 1.4)
                t = tr.maps["t"]
                m = np.clip((t - (.70 - L / 60)) / .15, 0, 1)
                d = math.radians(ang); back = 16 * gh / .3 * .0
                trail_len = tr.rgb.shape[1] * gh
                F.put(tr, hx - math.cos(d) * trail_len * .42, hy + math.sin(d) * trail_len * .42, gh, 1.3, rot=rot, mask=m)
                F.put(hd, hx, hy, gh, 1.4, rot=rot, heat=.2)
            if j >= 5:                                                  # impact, embed, cool
                tt = j - 5
                if tt <= 2:
                    F.put(K.star.rgb, tx, ty, (40 - 6 * tt) / K.star.rgb.shape[1], (2.2, 1.6, 1.0)[tt], heat=.6)
                    F.put(K.star_glow, tx, ty, 34 / K.star_glow.shape[1], (1.4, 1.0, .6)[tt])
                v = ease_out(cl(tt / 6))
                F.put(K.ring, tx, ty + 2, (14 + 26 * v) / K.ring.rgb.shape[1], 1.4 * (1 - v) ** 1.3)
                cool = cl(tt / 10)
                emb = (1 - ease_in(cl((i - 17) / 6)))
                d = math.radians(ang)
                F.put(hd, tx - math.cos(d) * 3, ty + math.sin(d) * 3, gh * .8, (1.3 - .5 * cool) * emb, rot=rot, heat=.5 * (1 - cool))
                for cc, da, sp, spin in chips[:4]:
                    if tt > 9: break
                    a2 = math.radians(ang + 180 + da)
                    q = ease_out(tt / 6)
                    F.put(cc, tx + math.cos(a2) * sp * q, ty - math.sin(a2) * sp * q + .4 * tt * tt, gh * 1.6, 1.4 * (1 - tt / 9), rot=spin * tt / 6)
        return F.bloom(2.0, .85).finish(True)
    return f, "appear"


def a8_last_tier_aura(K):
    """Loop. Round the Mender in the last tier: a floor ring whose light runs round it, glass plates and shards
    rising on both sides on their own phases and spins, cyan sawdust motes, glints that twinkle."""
    rnd = random.Random(31)
    pcs = [p for p in K.plates] + [s for s in K.shards[:12] if s is not None]
    risers = []
    for j in range(16):
        pc = pcs[j % len(pcs)]
        side = -1 if j % 2 == 0 else 1
        x = CX + side * rnd.uniform(18, 50)
        h = rnd.uniform(9, 15) if j < len(K.plates) else rnd.uniform(6, 10)
        risers.append((pc, x, rnd.random(), rnd.choice((1, 1, 2)), h / max(pc.rgb.shape[:2]), rnd.uniform(-60, 60), rnd.uniform(0, 1)))
    motes = [(rnd.uniform(CX - 54, CX + 54), rnd.random(), rnd.choice((1, 2, 2)), rnd.uniform(.16, .26)) for _ in range(18)]
    rw = K.ring.rgb.shape[1]
    def f(i):
        F = Frame(); ph = i / N
        ang = K.ring.maps["ang"]
        hd = (ang - 360 * ph) % 360
        run = np.exp(-(np.minimum(hd, 360 - hd) / 40) ** 2) + np.exp(-(np.minimum((hd + 180) % 360, 360 - (hd + 180) % 360) / 40) ** 2)
        F.put(K.ring, CX, CY + 22, 118 / rw, .55, flat=.85, mask=.45 + 1.6 * run, heat=.4 * run)
        for pc, x, p, r, sc, spin, sw in risers:
            a = frac(ph * r + p)
            y = 104 - 92 * a
            k = 1.2 * math.sin(math.pi * a) ** 1.3
            F.put(pc, x + 4 * math.sin(TAU * (a + sw)), y, sc, k, rot=spin * a + 360 * sw * 0, heat=.4 * max(0.0, math.sin(TAU * (2 * a + sw))) ** 6)
        for x, p, r, sz in motes:
            a = frac(ph * r + p)
            F.put(K.dot_c, x + 3 * math.sin(TAU * (a + p)), 106 - 90 * a, sz, .9 * math.sin(math.pi * a))
        for j in range(5):
            p = j / 5
            tw = max(0.0, math.sin(TAU * (ph * 2 + p * 1.7))) ** 8
            F.put(K.star.rgb, CX + (-46, 40, -24, 30, 52)[j], (52, 34, 18, 62, 80)[j], 11 / K.star.rgb.shape[1], 1.2 * tw, rot=30 * j)
        return F.bloom(2.0, .8).finish(False)
    return f, "loop"


CLIPS = [("a1_hull_omen", a1_hull_omen), ("a2_hull_close", a2_hull_close), ("a2_hull_floor", a2_hull_floor),
         ("a3_split_omen", a3_split_omen), ("a4_split_break", a4_split_break), ("a5_fresh_plank", a5_fresh_plank),
         ("a6_hammerfall", a6_hammerfall), ("a7_rivet_volley", a7_rivet_volley), ("a8_last_tier_aura", a8_last_tier_aura)]

LABELS = {"a1_hull_omen": "Hull omen (loop)", "a2_hull_close": "Hull closes", "a2_hull_floor": "Glass-grown floor (loop)",
          "a3_split_omen": "Keel Splitter omen (loop)", "a4_split_break": "Keel Splitter breaks",
          "a5_fresh_plank": "Fresh Plank (loop)", "a6_hammerfall": "Hammerfall", "a7_rivet_volley": "Rivet Volley",
          "a8_last_tier_aura": "Last tier aura (loop)"}


def strip(frames):
    sh = Image.new("RGBA", (S, S * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames): sh.paste(f, (0, i * S))
    return sh


def render(K, only=None):
    out = {}
    for key, fn in CLIPS:
        if only and key not in only: continue
        f, kind = fn(K)
        if kind == "appear":
            frames = [f(i) for i in range(N - 1)] + [blank()]          # appears end empty (the loop takes over)
        else:
            frames = [f(i) for i in range(N)]
        out[key] = (frames, kind)
        print("rendered", key, kind, len(frames), flush=True)
    return out


def export(clips):
    meta = []
    for key, (frames, kind) in clips.items():
        fname = f"anim_mender_{key}_{VER}.webp"
        sh = strip(frames); p = os.path.join(OUT, fname)
        sh.save(p, "WEBP", lossless=True, quality=100, method=6)
        b = os.path.getsize(p)
        assert len(frames) <= 127 and sh.size[1] <= 4096 and b <= 450_000, (key, len(frames), sh.size, b)
        meta.append({"key": key, "file": fname, "kind": kind, "frames": len(frames), "speed": SPEED,
                     "size": list(sh.size), "bytes": b})
        print(fname, len(frames), sh.size, b)
    with open(os.path.join(OUT, f"mender_fx_{VER}.json"), "w") as fh:
        json.dump({"source": "art/hullbound_mender_fx/build_fx_v2.py", "cell": S, "clips": meta}, fh, indent=1)
        fh.write("\n")


# ---------------------------------------------------------------------------------------------------- previews
def board_tile(z):
    """The dark battle-grid patch from v1, the clip's hex in the middle, at zoom z."""
    t = Image.new("RGBA", (S * z, S * z), (20, 24, 32, 255))
    d = ImageDraw.Draw(t)
    for dx, dy in [(0, 0), (-90, -30), (90, -30), (-90, 30), (90, 30), (0, -60), (0, 60)]:
        cx, cy, w, h = (CX + dx) * z, (CY + dy) * z, HW / 2 * z, HH / 2 * z
        d.polygon([(cx - w, cy), (cx - w / 2, cy - h), (cx + w / 2, cy - h), (cx + w, cy), (cx + w / 2, cy + h),
                   (cx - w / 2, cy + h)], outline=(60, 70, 88, 255), fill=(30, 34, 44, 255))
    return t


def over(tile, fr, z, times=1):
    t = tile.copy(); f = fr.resize((S * z, S * z), Image.LANCZOS) if z != 1 else fr
    for _ in range(times): t.alpha_composite(f)
    return t


def font(sz):
    for p in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()


def ffmpeg_bin():
    b = shutil.which("ffmpeg")
    if b: return b
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def preview_mp4(clips, path, z=2, plays=4, gap=10):
    keys = [k for k, _ in CLIPS if k in clips]
    cell = S * z; lab = 26; cols = 3; rows = math.ceil(len(keys) / cols)
    W, H = cols * cell, rows * (cell + lab)
    W += W % 2; H += H % 2
    cyc = N + gap
    total = plays * cyc
    tile = board_tile(z); fnt = font(15)
    head = Image.new("RGB", (W, H), (10, 12, 16)); d = ImageDraw.Draw(head)
    for k, key in enumerate(keys):
        x, y = (k % cols) * cell, (k // cols) * (cell + lab)
        d.text((x + 8, y + 5), LABELS[key], fill=(220, 230, 240), font=fnt)
    cmd = [ffmpeg_bin(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
           "-r", str(1000 // SPEED), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "20",
           "-pix_fmt", "yuv420p", "-movflags", "+faststart", path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(total):
        im = head.copy()
        for k, key in enumerate(keys):
            frames, kind = clips[key]
            x, y = (k % cols) * cell, (k // cols) * (cell + lab) + lab
            if kind == "loop": fr = frames[i % len(frames)]
            else:
                j = i % cyc
                fr = frames[j] if j < len(frames) else blank()
            im.paste(over(tile, fr, z, 2 if kind == "appear" else 1).convert("RGB"), (x, y))
        pr.stdin.write(im.tobytes())
    pr.stdin.close(); pr.wait()
    print("mp4", path, os.path.getsize(path))


def frame_sheet(clips, path, step=2):
    keys = [k for k, _ in CLIPS if k in clips]
    tile = board_tile(1); lab = 18; fnt = font(12)
    ncol = N // step
    W, H = ncol * S, len(keys) * (S + lab)
    sh = Image.new("RGB", (W, H), (10, 12, 16)); d = ImageDraw.Draw(sh)
    for r, key in enumerate(keys):
        frames, kind = clips[key]
        y = r * (S + lab)
        d.text((4, y + 2), f"{key}  ({kind}, {len(frames)} x {SPEED} ms; every {step}nd frame, numbered)", fill=(220, 230, 240), font=fnt)
        for c in range(ncol):
            j = c * step
            if j >= len(frames): break
            sh.paste(over(tile, frames[j], 1, 2 if kind == "appear" else 1).convert("RGB"), (c * S, y + lab))
            d.text((c * S + 3, y + lab + 2), str(j), fill=(150, 160, 175), font=fnt)
    sh.save(path)
    print("sheet", path, sh.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--preview")
    ap.add_argument("--only")
    ap.add_argument("--no-export", action="store_true")
    a = ap.parse_args()
    K = Kit(a.src)
    print("pieces: seams", len(K.seams), "plates", len(K.plates), "wedges", len(K.wedges), "shards", len(K.shards),
          "specks", len(K.line_specks), "embers", len(K.embers), "debris", len(K.debris6), "rivet chips", len(K.rivet_chips))
    only = set(a.only.split(",")) if a.only else None
    clips = render(K, only)
    if not a.no_export and not only: export(clips)
    if a.preview:
        os.makedirs(a.preview, exist_ok=True)
        preview_mp4(clips, os.path.join(a.preview, f"hullbound_mender_preview_{VER}.mp4"))
        frame_sheet(clips, os.path.join(a.preview, f"hullbound_mender_frames_{VER}.png"))


if __name__ == "__main__":
    main()
