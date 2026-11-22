"""Light-first FX drawing for TNR battle clips (2026-11-21).

Every frame is two passes at SS x supersampling, reduced to the delivered size at the end:
- matter (normal alpha): scorch, rock, dust - things that occlude;
- light: a greyscale intensity mask (tapered strokes, soft blobs), bloomed with stacked Gaussian blurs and mapped
  through a colour ramp; alpha follows intensity. Battle clips draw with normal alpha, so the glow is baked and kept
  coloured (a dark halo turns to mud on sand).
"""
import math
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

SS = 4

# icon palette: deep violet -> violet -> lilac-pink -> white-hot
STORM_RAMP = [(0.0, (112, 36, 224)), (0.35, (142, 62, 250)), (0.6, (192, 116, 255)), (0.8, (234, 188, 255)),
              (0.93, (252, 238, 255)), (1.0, (255, 255, 255))]
# floor: never reaches white
FLOOR_RAMP = [(0.0, (96, 30, 200)), (0.5, (140, 64, 246)), (0.8, (178, 104, 255)), (1.0, (206, 150, 255))]


def lut(ramp):
    out = []
    for i in range(256):
        v = i / 255
        for (a, ca), (b, cb) in zip(ramp, ramp[1:]):
            if v <= b:
                t = (v - a) / (b - a) if b > a else 0
                out.append(tuple(int(ca[k] + (cb[k] - ca[k]) * t) for k in range(3)))
                break
        else:
            out.append(ramp[-1][1])
    return out


STORM_LUT, FLOOR_LUT = lut(STORM_RAMP), lut(FLOOR_RAMP)


def jag(a, b, amp, rnd, depth=5):
    """Midpoint-displacement path from a to b, end points fixed."""
    pts = [a, b]
    for d in range(depth):
        out = [pts[0]]
        for p, q in zip(pts, pts[1:]):
            mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
            dx, dy = q[0] - p[0], q[1] - p[1]
            ln = math.hypot(dx, dy) or 1
            off = rnd.uniform(-1, 1) * amp * ln / (1.7 ** d) / 2
            out += [(mx - dy / ln * off, my + dx / ln * off), q]
        pts = out
    return pts


def wobble(pts, rnd, amp):
    """Small per-frame shimmer on a fixed path: same shape, alive (end points held)."""
    return [pts[0]] + [(x + rnd.uniform(-amp, amp), y + rnd.uniform(-amp, amp)) for x, y in pts[1:-1]] + [pts[-1]]


class Frame:
    def __init__(self, n):
        self.n, self.W = n, n * SS
        self.light = Image.new("L", (self.W, self.W), 0)
        self.soft = Image.new("L", (self.W, self.W), 0)     # pre-blurred light (blobs, flashes)
        self.matter = Image.new("RGBA", (self.W, self.W), (0, 0, 0, 0))
        self.dl, self.ds = ImageDraw.Draw(self.light), ImageDraw.Draw(self.soft)
        self.dm = ImageDraw.Draw(self.matter)

    # coordinates are in delivered px; widths in delivered px
    def stroke(self, pts, w0, w1, val=255, upto=1.0):
        pts = pts[:max(2, int(round(len(pts) * upto)))]
        n = len(pts)
        for i, (p, q) in enumerate(zip(pts, pts[1:])):
            w = (w0 + (w1 - w0) * i / max(1, n - 2)) * SS
            P, Q = (p[0] * SS, p[1] * SS), (q[0] * SS, q[1] * SS)
            self.dl.line([P, Q], fill=int(val), width=max(1, int(round(w))))
            r = w / 2
            self.dl.ellipse((Q[0] - r, Q[1] - r, Q[0] + r, Q[1] + r), fill=int(val))

    def blob(self, cx, cy, rx, ry, val=255, blur=0.35):
        """A soft light ellipse; blur as a fraction of rx."""
        layer = Image.new("L", (self.W, self.W), 0)
        ImageDraw.Draw(layer).ellipse(((cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS), fill=int(val))
        if blur:
            layer = layer.filter(ImageFilter.GaussianBlur(rx * blur * SS))
        self.soft = ImageChops.lighter(self.soft, layer)
        self.ds = ImageDraw.Draw(self.soft)

    def ring(self, cx, cy, rx, ry, w, val=255):
        self.dl.ellipse(((cx - rx) * SS, (cy - ry) * SS, (cx + rx) * SS, (cy + ry) * SS), outline=int(val),
                        width=max(1, int(w * SS)))

    def poly_matter(self, pts, fill, rim=None):
        P = [(x * SS, y * SS) for x, y in pts]
        self.dm.polygon(P, fill=fill)
        if rim:
            # lit edge on the upper side (the light comes from the lightning above)
            top = sorted(P, key=lambda p: p[1])[:max(2, len(P) // 2)]
            top.sort(key=lambda p: p[0])
            self.dm.line(top, fill=rim, width=max(1, SS))

    def paste_matter(self, im, xy):
        big = im.resize((im.width * SS, im.height * SS), Image.LANCZOS)
        self.matter.alpha_composite(big, (int(xy[0] * SS), int(xy[1] * SS)))

    def render(self, lut_=STORM_LUT, bloom=((1.5, 0.8), (5, 0.55), (13, 0.4)), gain=1.0, cap=1.0):
        inten = ImageChops.lighter(self.light, self.soft)
        out = inten
        for r, k in bloom:
            b = inten.filter(ImageFilter.GaussianBlur(r * SS)).point(lambda v, k=k: min(255, int(v * k * 2.2)))
            out = ImageChops.lighter(out, b)
        out = out.resize((self.n, self.n), Image.LANCZOS)
        if gain != 1.0 or cap != 1.0:
            out = out.point(lambda v: int(min(255 * cap, v * gain)))
        rgb = Image.merge("RGB", [out.point([c[i] for c in lut_]) for i in range(3)])
        alpha = out.point(lambda v: min(255, int(255 * (v / 255) ** 0.8 * 1.1)))
        light = rgb.convert("RGBA")
        light.putalpha(alpha)
        img = self.matter.resize((self.n, self.n), Image.LANCZOS)
        img.alpha_composite(light)
        return img


def rock(rnd, x, y, r):
    k = rnd.randrange(4, 7)
    angs = sorted(rnd.uniform(0, 2 * math.pi) for _ in range(k))
    return [(x + math.cos(a) * r * rnd.uniform(0.65, 1.1), y + math.sin(a) * r * rnd.uniform(0.6, 1.0)) for a in angs]


ROCK, ROCK_RIM = (28, 20, 40, 255), (168, 110, 240, 255)


def debris(fr, seed, origin, t, n=6, speed=(1.6, 3.2), size=(2.2, 3.6), ground=None):
    """Chunks thrown up and out from origin; t in frames since launch; they fall back to the ground line."""
    rnd = random.Random(seed)
    gy = origin[1] if ground is None else ground
    for _ in range(n):
        vx, vy = rnd.uniform(-1, 1) * speed[1], -rnd.uniform(*speed) * 1.6
        r = rnd.uniform(*size)
        x, y = origin[0] + vx * t, origin[1] + vy * t + 0.9 * t * t
        if t < 0 or y > gy + 2:
            continue
        fr.poly_matter(rock(random.Random(int(r * 100 + vx * 10)), x, y, r), ROCK, ROCK_RIM)


def sparks(fr, seed, origin, t, n=8, reach=26, flat=0.5, val=230):
    """Short bright streaks flying out and down, shrinking."""
    rnd = random.Random(seed)
    for _ in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        sp = rnd.uniform(0.5, 1.0) * reach
        k = t / 5
        if k > 1:
            continue
        x0, y0 = origin[0] + math.cos(a) * sp * k, origin[1] + math.sin(a) * sp * k * flat - 6 * k + 9 * k * k
        x1, y1 = origin[0] + math.cos(a) * sp * (k + 0.12), origin[1] + math.sin(a) * sp * (k + 0.12) * flat
        fr.stroke([(x1, y1), (x0, y0)], 1.4 * (1 - k) + 0.3, 0.3, val * (1 - 0.6 * k))
