#!/usr/bin/env python3
"""v23 inbetweening test: (a) one flame drawing kept alive by a slow rising flow warp (no scaling or rotating);
(b) optical-flow inbetweens between two flame drawings. Prototype only (OpenCV/NumPy)."""
import os
import cv2
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.join(HERE, "..", "v20", "sprites")
BG = (22, 18, 34)


def load(n, size=220):
    im = Image.open(os.path.join(SPR, f"flame_{n:02d}.png")).convert("RGBA")
    c = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    im.thumbnail((size - 20, size - 20))
    c.alpha_composite(im, ((size - im.width) // 2, size - im.height - 6))
    return np.asarray(c).astype(np.float32) / 255


def noise(shape, scale, rng):
    h, w = shape
    n = rng.standard_normal((h // scale + 3, w // scale + 3)).astype(np.float32)
    return cv2.resize(n, (w + 3 * scale, h + 3 * scale), interpolation=cv2.INTER_CUBIC)


def flow_flame(img, frames, rng):
    """Advect a smooth noise field upward; displacement grows toward the tip (the base stays planted)."""
    h, w = img.shape[:2]
    nx, ny = noise((h * 3, w), 40, rng), noise((h * 3, w), 40, rng)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    tip = (1 - yy / h) ** 1.5                               # 0 at the base, 1 at the top
    out = []
    for f in range(frames):
        off = int(f * 3.2) % (h * 2)                       # the field rises ~3 px a frame
        dx = nx[h * 2 - off: h * 3 - off, :w] * 7 * tip
        dy = ny[h * 2 - off: h * 3 - off, :w] * 4 * tip
        warped = cv2.remap(img, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        out.append(warped)
    return out


def morph(a, b, steps):
    """Optical-flow inbetweens: warp a forward and b backward along the flow, then cross-dissolve."""
    ga, gb = [(cv2.cvtColor(x[..., :3], cv2.COLOR_RGB2GRAY) * x[..., 3] * 255).astype(np.uint8) for x in (a, b)]
    fab = cv2.calcOpticalFlowFarneback(ga, gb, None, 0.5, 4, 25, 5, 7, 1.5, 0)
    fba = cv2.calcOpticalFlowFarneback(gb, ga, None, 0.5, 4, 25, 5, 7, 1.5, 0)
    h, w = ga.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    out = []
    for i in range(steps + 1):
        t = i / steps
        wa = cv2.remap(a, xx - fab[..., 0] * t, yy - fab[..., 1] * t, cv2.INTER_LINEAR)
        wb = cv2.remap(b, xx - fba[..., 0] * (1 - t), yy - fba[..., 1] * (1 - t), cv2.INTER_LINEAR)
        out.append(wa * (1 - t) + wb * t)
    return out


def on_bg(x):
    rgb, a = x[..., :3], x[..., 3:4]
    return Image.fromarray(np.clip((rgb * a + np.array(BG) / 255 * (1 - a)) * 255, 0, 255).astype(np.uint8))


rng = np.random.default_rng(23)
A = flow_flame(load(9), 60, rng)                           # 60 frames at 20 ms = 1.2 s of one drawing alive
B = morph(load(9), load(2), 12) + morph(load(2), load(9), 12)[1:]
frames = []
for i in range(60):
    a, b = on_bg(A[i]), on_bg(B[min(i // 2, len(B) - 1) if i < 50 else len(B) - 1 - (i - 50)])
    s = Image.new("RGB", (460, 230), BG)
    s.paste(a, (5, 5)); s.paste(b, (235, 5))
    frames.append(s)
frames[0].save(os.path.join(HERE, "inbetween_test.gif"), save_all=True, append_images=frames[1:], duration=20, loop=0)
print("ok")
