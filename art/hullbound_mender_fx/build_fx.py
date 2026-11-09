#!/usr/bin/env python3
"""The Hullbound Mender (Skyglass legendary boss) combat clips from dauntless's eight paintings, one hex, soft light.
Paintings are light on pure black; the black is lifted to alpha (alpha = brightest channel, colour unpremultiplied)
and the pieces are animated in code. Geometry: every clip frame is a square 2.5 hex-heights wide centred on the hex
(docs/design/COMBAT_ANIMATION_ENGINE.md 3.1), so in a 150 px cell the hex footprint is 120 x 60 centred.

    python3 art/hullbound_mender_fx/build_fx.py --src /mnt/project-files/tnr/art/mender_inbox [--preview DIR]
"""
import argparse, json, math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "exports")
S = 150                       # cell
CX, CY = 75, 75               # hex centre
HW, HH = 120, 60              # hex footprint
SPEED = 50                    # ms per frame
VER = "v1"


def lift(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(np.float32)
    m = a.max(axis=2)
    al = np.clip((m - 10.0) / 235.0, 0, 1)
    rgb = np.where(al[..., None] > 0, a / np.maximum(al[..., None], 1e-3), 0)
    rgb = np.clip(rgb, 0, 255)
    out = np.dstack([rgb, al * 255]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    bb = Image.fromarray((al > 0.06).astype(np.uint8) * 255).getbbox()
    return im.crop(bb)


def fit(im, w, h, keep=True):
    if keep:
        k = min(w / im.width, h / im.height)
        return im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    return im.resize((w, h), Image.LANCZOS)


def scale_a(im, k):
    if k >= 0.999:
        return im
    r, g, b, a = im.split()
    a = a.point(lambda v: int(v * max(0.0, k)))
    return Image.merge("RGBA", (r, g, b, a))


def brighten(im, k):
    """Push colour toward white by k (0..1), alpha untouched: a flash."""
    if k <= 0:
        return im
    arr = np.asarray(im).astype(np.float32)
    arr[..., :3] = arr[..., :3] + (255 - arr[..., :3]) * k
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8), "RGBA")


def flash(src, size):
    """The painting's bright heart under a soft round mask: an impact spark with no hard edge."""
    w, h = src.size
    c = src.crop((int(w * 0.3), int(h * 0.1), int(w * 0.7), int(h * 0.7)))
    c = fit(c, size, size, keep=False)
    m = Image.new("L", c.size, 0)
    ImageDraw.Draw(m).ellipse((size * 0.18, size * 0.18, size * 0.82, size * 0.82), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(size * 0.12))
    r, g, b, a = c.split()
    a = Image.fromarray((np.asarray(a).astype(np.float32) * np.asarray(m).astype(np.float32) / 255).astype(np.uint8))
    return Image.merge("RGBA", (r, g, b, a))


def blank():
    return Image.new("RGBA", (S, S), (0, 0, 0, 0))


def put(f, piece, cx, cy):
    """Composite piece centred at (cx, cy), clipped to the frame."""
    x, y = round(cx - piece.width / 2), round(cy - piece.height / 2)
    box = (max(0, -x), max(0, -y), min(piece.width, S - x), min(piece.height, S - y))
    if box[0] < box[2] and box[1] < box[3]:
        f.alpha_composite(piece.crop(box), (x + box[0], y + box[1]))


def hex_mask(feather=3, inset=2):
    m = Image.new("L", (S, S), 0)
    w, h = HW / 2 - inset, HH / 2 - inset
    ImageDraw.Draw(m).polygon([(CX - w, CY), (CX - w / 2, CY - h), (CX + w / 2, CY - h), (CX + w, CY),
                               (CX + w / 2, CY + h), (CX - w / 2, CY + h)], fill=255)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m


HEX = None


def in_hex(f):
    r, g, b, a = f.split()
    a = Image.fromarray((np.asarray(a).astype(np.float32) * np.asarray(HEX).astype(np.float32) / 255).astype(np.uint8))
    return Image.merge("RGBA", (r, g, b, a))


def ease_out(t):
    return 1 - (1 - t) ** 3


def strip(frames):
    sh = Image.new("RGBA", (S, S * len(frames)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sh.paste(f, (0, i * S))
    return sh


# ------------------------------------------------------------------------------------------------ clips
def a1_hull_omen(P):
    seams = fit(P["P1"], HW - 8, HH - 6, keep=False)          # laid flat on the deck
    out = []
    n = 24
    for i in range(n):
        ph = i / n
        k = 0.7 + 0.3 * (0.5 - 0.5 * math.cos(2 * math.pi * ph))
        f = blank()
        put(f, brighten(scale_a(seams, k), 0.4 * k), CX, CY)
        out.append(in_hex(f))
    return out, "loop"


def a2_hull_close(P):
    plates = fit(P["P2"], 92, 92)
    floor = fit(P["P2"], HW - 6, HH - 4, keep=False)
    base = CY + 22                                            # plates stand on the hex, base below centre
    out = []
    n = 20
    for i in range(n):
        f = blank()
        if i <= 5:                                            # punch up through the deck
            t = ease_out((i + 1) / 6)
            up = round((1 - t) * plates.height)
            pc = plates.crop((0, 0, plates.width, plates.height - up)) if up < plates.height else None
            if pc is not None and pc.height > 0:
                g = Image.new("RGBA", (S, S), (0, 0, 0, 0))
                g.alpha_composite(pc, (round(CX - pc.width / 2), base - pc.height))
                f.alpha_composite(brighten(g, 0.3 * (1 - t)))
        elif i <= 8:                                          # lock: hold bright
            g = blank()
            g.alpha_composite(plates, (round(CX - plates.width / 2), base - plates.height))
            f.alpha_composite(brighten(g, 0.35 if i == 6 else 0.1))
        else:                                                 # sink into a faint glass-grown floor
            t = (i - 8) / (n - 9)
            g = blank()
            g.alpha_composite(scale_a(plates, 1 - t), (round(CX - plates.width / 2), base - plates.height + round(14 * t)))
            fl = blank()
            put(fl, scale_a(floor, 0.18 + 0.5 * (1 - t) * 0.4), CX, CY)
            f.alpha_composite(in_hex(fl))
            f.alpha_composite(g)
        out.append(f)
    return out, "appear"


def a2_hull_floor(P):
    floor = fit(P["P2"], HW - 6, HH - 4, keep=False)
    out = []
    n = 16
    for i in range(n):
        k = 0.18 + 0.04 * math.sin(2 * math.pi * i / n)
        f = blank()
        put(f, scale_a(floor, k), CX, CY)
        out.append(in_hex(f))
    return out, "loop"


def a3_split_omen(P):
    line = fit(P["P3"].rotate(90, expand=True), HW, 26, keep=False)
    dust = line.filter(ImageFilter.GaussianBlur(2))
    out = []
    n = 24
    for i in range(n):
        f = blank()
        if i < 3:                                             # the snap
            put(f, brighten(fit(line, round(HW * (0.5 + 0.25 * (i + 1))), 26, keep=False), 0.6 - 0.15 * i), CX, CY)
        else:
            t = (i - 3) / (n - 3)
            put(f, scale_a(dust, 0.55 * (1 - t)), CX, CY - 2 - round(10 * t))     # chalk dust lifts
            put(f, scale_a(line, 0.8 + 0.15 * math.cos(2 * math.pi * t)), CX, CY)
        out.append(in_hex(f) if i >= 3 else f)
    return out, "loop"


def a4_split_break(P):
    burst = fit(P["P4"], 104, 90)
    out = []
    n = 18
    for i in range(n):
        f = blank()
        if i <= 5:
            t = ease_out((i + 1) / 6)
            b = fit(burst, max(2, round(burst.width * (0.3 + 0.7 * t))), max(2, round(burst.height * (0.3 + 0.7 * t))), keep=False)
            put(f, brighten(b, 0.4 * (1 - t)), CX, CY + 18 - b.height / 2)
        elif i <= 9:
            put(f, burst, CX, CY + 18 - burst.height / 2)
        else:
            t = (i - 9) / (n - 10)
            put(f, scale_a(burst, 1 - t), CX, CY + 18 - burst.height / 2 - round(8 * t))
        out.append(f)
    return out, "appear"


def a5_plank(P):
    plank = fit(P["P5"], 104, 60)
    out = []
    n = 24
    for i in range(n):
        ph = i / n
        k = 0.82 + 0.18 * (0.5 - 0.5 * math.cos(2 * math.pi * ph))
        f = blank()
        put(f, brighten(scale_a(plank, k), 0.12 * (k - 0.82) / 0.18), CX, CY - 4 - round(1.5 * math.sin(2 * math.pi * ph)))
        out.append(f)
    return out, "loop"


def a6_hammerfall(P):
    ring = fit(P["P6"], 146, 146)
    out = []
    n = 18
    for i in range(n):
        f = blank()
        if i <= 9:
            t = ease_out((i + 1) / 10)
            r = fit(ring, round(ring.width * (0.2 + 0.8 * t)), round(ring.height * (0.2 + 0.8 * t)), keep=False)
            put(f, brighten(r, 0.45 * (1 - t)), CX, CY)
        elif i > 9:
            t = (i - 9) / (n - 10)
            r = fit(ring, round(ring.width * (1 + 0.06 * t)), round(ring.height * (1 + 0.06 * t)), keep=False)
            put(f, scale_a(r, 1 - t), CX, CY)
        out.append(f)
    return out, "appear"


def a7_rivets(P):
    rv = fit(P["P7"], 60, 60)
    base_ang = math.degrees(math.atan2(P["P7"].height, P["P7"].width))   # painted flight angle (down-right)
    hit = flash(P["P6"], 54)
    tgt = (CX, CY - 11)                                       # on the body, 15% above frame centre
    shots = [(-48, -48, -8, -2), (-56, -30, 7, 5), (-36, -56, 1, -9)]
    out = []
    n = 22
    for i in range(n):
        f = blank()
        for k, (sx, sy, ox, oy) in enumerate(shots):
            j = i - k * 4
            tx, ty = tgt[0] + ox, tgt[1] + oy
            if 0 <= j < 4:                                    # flight
                t = (j + 1) / 4
                ang = math.degrees(math.atan2(-sy - oy, -sx - ox))
                p = rv.rotate(base_ang - ang, expand=True, resample=Image.BICUBIC)
                hx, hy = tx + sx * (1 - t), ty + sy * (1 - t)
                put(f, p, hx - 18 * math.cos(math.radians(ang)), hy - 18 * math.sin(math.radians(ang)))
            elif 4 <= j < 8:                                  # punch in
                t = (j - 4) / 4
                put(f, brighten(scale_a(fit(hit, round(32 + 30 * t), round(32 + 30 * t)), 1 - t * t), 0.3), tx, ty)
        out.append(f)
    return out, "appear"


def a8_aura(P):
    rnd = random.Random(13)
    crys = [fit(P["P2"].rotate(rnd.uniform(-30, 30), expand=True, resample=Image.BICUBIC), s, s) for s in (12, 15, 18, 14, 11)]
    mote = fit(P["P3"], 7, 26, keep=False)
    parts = []
    for j in range(14):
        pc = crys[j % len(crys)] if j % 2 == 0 else mote
        parts.append((rnd.uniform(CX - 30, CX + 30), rnd.random(), pc, rnd.uniform(-25, 25)))
    out = []
    n = 24
    for i in range(n):
        f = blank()
        for x, ph, pc, spin in parts:
            t = (ph + i / n) % 1.0
            y = 118 - 92 * t
            a = math.sin(math.pi * t)
            put(f, scale_a(pc.rotate(spin * t, expand=True, resample=Image.BICUBIC), 0.85 * a), x + 4 * math.sin(6.28 * t + x), y)
        out.append(f)
    return out, "loop"


CLIPS = [("a1_hull_omen", a1_hull_omen), ("a2_hull_close", a2_hull_close), ("a2_hull_floor", a2_hull_floor),
         ("a3_split_omen", a3_split_omen), ("a4_split_break", a4_split_break), ("a5_fresh_plank", a5_plank),
         ("a6_hammerfall", a6_hammerfall), ("a7_rivet_volley", a7_rivets), ("a8_last_tier_aura", a8_aura)]


def main():
    global HEX
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--preview")
    a = ap.parse_args()
    HEX = hex_mask()
    names = {"P1": "P1_hull_omen", "P2": "P2_hull_closes", "P3": "P3_chalk_line", "P4": "P4_deck_splits",
             "P5": "P5_fresh_plank", "P6": "P6_hammerfall", "P7": "P7_rivet"}
    P = {k: lift(os.path.join(a.src, v + ".png")) for k, v in names.items()}
    meta = []
    allframes = {}
    for key, fn in CLIPS:
        frames, kind = fn(P)
        fname = f"anim_mender_{key}_{VER}.webp"
        sh = strip(frames)
        p = os.path.join(OUT, fname)
        sh.save(p, "WEBP", lossless=True, quality=100, method=6)
        meta.append({"key": key, "file": fname, "kind": kind, "frames": len(frames), "speed": SPEED,
                     "size": list(sh.size), "bytes": os.path.getsize(p)})
        allframes[key] = frames
    with open(os.path.join(OUT, f"mender_fx_{VER}.json"), "w") as fh:
        json.dump({"source": "art/hullbound_mender_fx/build_fx.py", "cell": S, "clips": meta}, fh, indent=1)
        fh.write("\n")
    for m in meta:
        print(m["file"], m["frames"], m["size"], m["bytes"])
    if a.preview:
        preview(allframes, a.preview)


LABELS = {"a1_hull_omen": "Hull omen (loop)", "a2_hull_close": "Hull closes", "a2_hull_floor": "Glass-grown floor (loop)",
          "a3_split_omen": "Keel Splitter omen (loop)", "a4_split_break": "Keel Splitter breaks", "a5_fresh_plank": "Fresh Plank (loop)",
          "a6_hammerfall": "Hammerfall", "a7_rivet_volley": "Rivet Volley", "a8_last_tier_aura": "Last tier aura (loop)"}


def board_tile(z):
    """A dark deck patch with the hex outline, at zoom z."""
    t = Image.new("RGBA", (S * z, S * z), (20, 24, 32, 255))
    d = ImageDraw.Draw(t)
    for dx, dy in [(0, 0), (-90, -30), (90, -30), (-90, 30), (90, 30), (0, -60), (0, 60)]:
        cx, cy, w, h = (CX + dx) * z, (CY + dy) * z, HW / 2 * z, HH / 2 * z
        d.polygon([(cx - w, cy), (cx - w / 2, cy - h), (cx + w / 2, cy - h), (cx + w, cy), (cx + w / 2, cy + h),
                   (cx - w / 2, cy + h)], outline=(60, 70, 88, 255), fill=(30, 34, 44, 255))
    return t


def preview(allframes, d):
    os.makedirs(d, exist_ok=True)
    z = 2
    keys = list(allframes)
    n = max(len(v) for v in allframes.values())
    cols = 3
    rows = math.ceil(len(keys) / cols)
    bt = board_tile(z)
    gif = []
    for i in range(n):
        sheet = Image.new("RGBA", (cols * S * z, rows * (S * z + 18)), (10, 12, 16, 255))
        dr = ImageDraw.Draw(sheet)
        for k, key in enumerate(keys):
            fr = allframes[key]
            x, y = (k % cols) * S * z, (k // cols) * (S * z + 18)
            tile = bt.copy()
            tile.alpha_composite(fr[i % len(fr)].resize((S * z, S * z), Image.LANCZOS))
            sheet.paste(tile, (x, y + 18))
            dr.text((x + 6, y + 3), LABELS.get(key, key), fill=(220, 230, 240, 255))
        gif.append(sheet.convert("RGB"))
    gif[0].save(os.path.join(d, f"mender_fx_{VER}_preview.webp"), save_all=True, append_images=gif[1:], duration=SPEED,
                loop=0, lossless=False, quality=80)
    # contact sheet: every 3rd frame of each clip
    rowsimg = []
    for key in keys:
        fr = allframes[key][::3]
        r = Image.new("RGBA", (len(fr) * S, S + 14), (10, 12, 16, 255))
        ImageDraw.Draw(r).text((4, 1), key, fill=(220, 230, 240, 255))
        bt1 = board_tile(1)
        for j, f in enumerate(fr):
            t = bt1.copy(); t.alpha_composite(f); r.paste(t, (j * S, 14))
        rowsimg.append(r)
    W = max(r.width for r in rowsimg)
    cs = Image.new("RGBA", (W, sum(r.height for r in rowsimg)), (10, 12, 16, 255))
    y = 0
    for r in rowsimg:
        cs.paste(r, (0, y)); y += r.height
    cs.convert("RGB").save(os.path.join(d, f"mender_fx_{VER}_contact.png"))


if __name__ == "__main__":
    main()
