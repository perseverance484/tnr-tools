#!/usr/bin/env python3
"""FCF v23: v22 re-animated from key poses (2026-11-22).

Flames, whips, seal tags, smoke and impact bursts now play inbetweened key-pose sequences (v23/seq, from
inbetween.py) placed once and left alone: no wobble, no pulsing size, no swapping drawings. Lightning keeps its
strobe (real lightning is one flash and a decay). The rest of v22 follows.

    python3 .../v20/slice_kit.py && python3 .../v22/slice_kit2.py && python3 .../v22/fcf_v22.py

Built on v21's polish (timing, value tiers, contrast) plus the second kit (seal tags, ash, script cracks, chakra
whips, whip bursts). Real board size, 50 ms frames. Beats (1.45 s):
  0-300     THE SEAL BREAKS  eight paper seal tags stand round the user's tile (never over the fighter) over a
                             ground seal; at 150 they catch violet fire and peel ash; script cracks split the seal
  300       ERUPTION         the last tags tear to ash; chakra flame tongues burst up round the user's feet
  400       FURY BEAT 1      three chakra whips lash out to one side, each snapping with a crack burst at its tip
  550       FURY BEAT 2      three more lash the other way
  700       FURY BEAT 3      the CLIMAX: the dark frame, starburst, seven bolts in every direction, shockwave
  750-850   flicker / restrike; 800-950 stragglers fill the gaps
  950-1450  fade: ash drifts, flames die, a little smoke
Rhythm: hit ... hit ... HIT. Writes fcf_v23_real.gif, fcf_v23_2x.gif, fcf_v23_beats.png.
"""
import glob
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "v21"))
sys.path.insert(0, os.path.join(HERE, "..", "v22"))
import dress_v21 as D  # noqa: E402

V, M, BV = D.V, D.M, D.BV
W, H, TW, TH, SRC, GROUND = D.W, D.H, D.TW, D.TH, D.SRC, D.GROUND
SQ, xform, put, SEC, SEAL_R = D.SQ, D.xform, D.put, D.SEC, D.SEAL_R
STEP = int(os.environ.get("FCF_STEP", "20"))   # ms per frame; the engine takes 1-100, the display caps it
K2 = {}
for f in sorted(glob.glob(os.path.join(HERE, "..", "v22", "sprites", "*.png"))):
    K2.setdefault(os.path.basename(f).split("_")[0], []).append(Image.open(f).convert("RGBA"))
TAGS, BURNING, ASH, CRACKS, WHIPS, BURSTS = (K2["tag"][:4], K2["tag"][4:], K2["ash"], K2["crack"], K2["whip"],
                                             K2["burst"])
CLIMAX = 700
import json  # noqa: E402
SEQ_META = json.load(open(os.path.join(HERE, "seq", "index.json")))
SEQ = {k: [Image.open(os.path.join(HERE, "seq", f"{k}_{i:03d}.png")).convert("RGBA") for i in range(m["frames"])]
       for k, m in SEQ_META.items()}
_pc = {}


def seq_frame(kind, p):
    """The sequence frame at progress p (0-1; wraps for cyclic sequences)."""
    fr = SEQ[kind]
    if SEQ_META[kind]["cyclic"]:
        return int(p * len(fr)) % len(fr)
    return max(0, min(len(fr) - 1, int(round(p * (len(fr) - 1)))))


def place(fr, kind, idx, at, scale, angle=0.0, alpha=1.0, flip=False, thin=1.0):
    """Draw sequence frame idx with its anchor on point at, scaled, rotated about the anchor (degrees, screen)."""
    key = (kind, idx, round(scale, 3), round(angle), flip, thin)
    spr = _pc.get(key)
    if spr is None:
        img = SEQ[kind][idx]
        ax, ay = SEQ_META[kind]["anchor"]
        if flip:
            img, ay = img.transpose(Image.FLIP_TOP_BOTTOM), img.height - ay
        w, h = max(2, int(img.width * scale)), max(2, int(img.height * scale * thin))   # thin: across the stroke
        img, ax, ay = img.resize((w, h), Image.LANCZOS), ax * scale, ay * scale * thin
        r = int(math.ceil(max(math.hypot(cx - ax, cy - ay) for cx in (0, w) for cy in (0, h)))) + 2
        c = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
        c.alpha_composite(img, (int(round(r - ax)), int(round(r - ay))))
        spr = c.rotate(-angle, Image.BICUBIC) if angle else c
        if len(_pc) > 5000:
            _pc.clear()
        _pc[key] = spr
    if alpha < 1:
        spr = spr.copy()
        spr.putalpha(spr.getchannel("A").point(lambda v: int(v * alpha)))
    fr.alpha_composite(spr, (int(round(at[0] - spr.width / 2)), int(round(at[1] - spr.height / 2))))


def _whip_reach():
    """Anchor-to-tip vector of the fully extended whip key (key 2), in key pixels."""
    import numpy as np
    a = np.asarray(Image.open(os.path.join(HERE, "keys", "whip_2.png")).getchannel("A"))
    ys, xs = np.nonzero(a > 80)
    ax, ay = SEQ_META["whip"]["anchor"]
    i = int(np.argmax((xs - ax) ** 2 + (ys - ay) ** 2))
    return xs[i] - ax, ys[i] - ay


WHIP_DX, WHIP_DY = _whip_reach()
THIN = 0.42          # the painted whip is fat for its length; thin it across the stroke
WHIP_EXT = 0.5          # progress of the extended key in the whip sequence (key 2 of 0-4)


def dim_area(fr, k):
    m = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(m)
    for kk in M.AREA + [M.CASTER]:
        x, y = M.TILES[kk]
        md.polygon([(x - TW / 2, y), (x - TW / 4, y - TH / 2), (x + TW / 4, y - TH / 2), (x + TW / 2, y),
                    (x + TW / 4, y + TH / 2), (x - TW / 4, y + TH / 2)], fill=255)
    dark = Image.new("RGBA", (W, H), (8, 3, 18, 0))
    dark.putalpha(m.filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v * k)))
    fr.alpha_composite(dark)


def whip(img, a, b, alpha, grow=1.0, flip=False):
    """A whip sprite from a (its thick end) to b (its tip); grow reveals it from the thick end."""
    L = math.hypot(b[0] - a[0], b[1] - a[1])
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    body = img.transpose(Image.FLIP_TOP_BOTTOM) if flip else img
    body = body.resize((max(2, int(L)), max(2, int(min(L * body.height / body.width * 0.8, TH * 0.9)))), Image.LANCZOS)
    if grow < 1:
        m = Image.new("L", body.size, 0)
        ImageDraw.Draw(m).rectangle((0, 0, int(body.width * grow), body.height), fill=255)
        m = m.filter(ImageFilter.GaussianBlur(max(2, body.width * 0.05)))
        from PIL import ImageChops
        body.putalpha(ImageChops.multiply(body.getchannel("A"), m))
    if alpha < 1:
        body.putalpha(body.getchannel("A").point(lambda v: int(v * alpha)))
    r = body.rotate(-ang, Image.BICUBIC, expand=True)
    return r, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def main(seed=22):
    rnd = random.Random(seed)
    # --- v21's climax set, shifted to CLIMAX
    by_sec = {s: [] for s in range(8)}
    for k in M.AREA:
        x, y = M.TILES[k]
        a = math.atan2(y - SRC[1], x - SRC[0])
        by_sec[int(((a + math.pi / 8) % (2 * math.pi)) // (math.pi / 4))].append(k)
    far = [sorted(by_sec[s], key=lambda k: -BV.dist(k, M.CASTER))[0] for s in range(8) if by_sec[s]]
    mains = far[:7]
    main_angles = sorted(math.atan2(M.TILES[k][1] - SRC[1], M.TILES[k][0] - SRC[0]) for k in mains)
    gaps = sorted(((main_angles[(i + 1) % len(main_angles)] - main_angles[i]) % (2 * math.pi), i)
                  for i in range(len(main_angles)))[::-1][:4]
    strag = []
    for g, i in gaps:
        mid = main_angles[i] + g / 2
        cands = [k for k in M.AREA if BV.dist(k, M.CASTER) >= 3 and k not in mains and k not in strag]
        strag.append(min(cands, key=lambda k: abs(((math.atan2(M.TILES[k][1] - SRC[1], M.TILES[k][0] - SRC[0])
                                                     - mid + math.pi) % (2 * math.pi)) - math.pi)))

    def end(k, extra=1.06):
        x, y = M.TILES[k]
        return (SRC[0] + (x - SRC[0]) * extra, SRC[1] + (y - SRC[1]) * extra)
    mb = [(end(k), rnd.choice(V.BOLTS), rnd.random() < 0.5, TH * rnd.uniform(1.4, 1.8)) for k in mains]
    sb = [(CLIMAX + 100 + i * 50, end(k), rnd.choice(V.BOLTS), rnd.random() < 0.5, TH * rnd.uniform(1.2, 1.5))
          for i, k in enumerate(strag)]
    # --- fury beats: whips to one side, then the other (to mid/far tiles)
    def side(lo, hi, n):
        ks = [k for k in M.AREA if BV.dist(k, M.CASTER) >= 3 and k not in mains
              and lo <= math.degrees(math.atan2(M.TILES[k][1] - SRC[1], M.TILES[k][0] - SRC[0])) % 360 < hi]
        rnd.shuffle(ks)
        return ks[:n]
    beat1 = [(400 + i * 25, end(k, 1.12), rnd.choice(WHIPS), rnd.random() < 0.5) for i, k in enumerate(side(290, 430, 3))]
    beat2 = [(550 + i * 25, end(k, 1.12), rnd.choice(WHIPS), rnd.random() < 0.5) for i, k in enumerate(side(110, 250, 3))]
    whips = beat1 + beat2
    # --- tags round the user's tile, on the ground ellipse; front ones drawn after the fighter's feet line
    tag_r = TW * 0.95                      # wide enough that no tag stands on the fighter
    tags = [(i * 45 + 22.5, TAGS[i % 4], BURNING[i % 4]) for i in range(8)]
    ash = [(rnd.uniform(0, 360), rnd.choice(ASH), rnd.uniform(150, 320), rnd.uniform(-1, 1), rnd.uniform(0.6, 1.1))
           for _ in range(26)]
    cracks = [(i * 72 + rnd.uniform(-15, 15), CRACKS[i % len(CRACKS)]) for i in range(5)]
    flames = [(i * 30 + rnd.uniform(-8, 8), rnd.choice(V.FLAMES), rnd.uniform(0.9, 1.3)) for i in range(12)]
    smoke = [(i * 1.26, rnd.choice(V.SMOKE)) for i in range(5)]
    sparks = [(e, rnd.uniform(0, 2 * math.pi), rnd.choice(V.SPARKS)) for e, _, _, _ in mb for _ in range(2)]
    shards = [(i * math.pi / 4 + 0.3, D.SHARDS[i]) for i in range(8)]
    frames, labels = [], []
    for t in range(0, 1350, STEP):
        w50 = (t // 50) * 50                       # which 50 ms window (lightning strobes hold per window)
        fr = D.board()
        beat = ""
        dim = 0
        if CLIMAX <= t < CLIMAX + 250:
            dim = 0.55 * (1 - V.ease_out((t - CLIMAX) / 250)) + 0.12 * ((t - CLIMAX) / 250 < 1)
        if 0 < t < CLIMAX:
            dim = max(dim, 0.18 * min(1, t / 300))       # the area hushes while the seal breaks
        if dim:
            dim_area(fr, dim)
        # ------------------------------------------------ the ground seal and its cracks (secondary)
        if t < 400:
            u = min(1, t / 250)
            put(fr, xform(D.OUTER, TW * 2.2 * (1.1 - 0.1 * u), t * 0.1, SEC * u * (1 if t < 300 else 1 - (t - 300) / 100), SQ),
                *GROUND)
            put(fr, xform(D.RUNES, TW * 1.5, -t * 0.15, SEC * u * (1 if t < 300 else 1 - (t - 300) / 100), SQ), *GROUND)
        if 200 <= t < 650:
            g = min(1, (t - 200) / 100)
            f = 1 if t < 450 else 1 - (t - 450) / 200
            for a, img in cracks:
                x = GROUND[0] + math.cos(math.radians(a)) * TW * 0.55
                y = GROUND[1] + math.sin(math.radians(a)) * TW * 0.55 * SQ
                put(fr, xform(img, TW * 0.9 * g, a, 0.8 * f, SQ), x, y)
        # ------------------------------------------------ seal tags (behind the fighter: back half first)
        if t < 380:
            beat = "SEAL BREAKS" if t < 300 else ""
            burning = t >= 150
            for a, *_ in sorted(tags, key=lambda x: math.sin(math.radians(x[0]))):
                x = GROUND[0] + math.cos(math.radians(a)) * tag_r
                y = GROUND[1] + math.sin(math.radians(a)) * tag_r * SQ
                p = max(0.0, (t - 110 - (a % 90) * 0.4) / 220)        # each tag catches a moment apart
                sc = TH * 0.95 / 225                                   # the paper is ~225 px tall in the key
                place(fr, "tag", seq_frame("tag", p), (x, y - TH * 0.15 - TH * 0.95), sc,
                      alpha=min(1.0, t / 60) * (1 if p < 1 else 0))
        for a, img, t0, drift, sc in ash:                 # ash peels up off the burning tags
            u = (t - t0) / 600
            if 0 <= u <= 1:
                x = GROUND[0] + math.cos(math.radians(a)) * tag_r + drift * 30 * u
                y = GROUND[1] + math.sin(math.radians(a)) * tag_r * SQ - TH * 0.6 - TH * 1.8 * u
                put(fr, xform(img, TW * 0.16 * sc, u * 300 * drift, 0.9 * (1 - u)), x, y)
        # ------------------------------------------------ eruption: chakra flames at the feet
        if 300 <= t < 1100:
            if 300 <= t < 360:
                beat = "ERUPTION"
                put(fr, xform(V.FLASH[2], TW * (1.2 + (t - 300) / 200), 0, 0.9 * (1 - (t - 300) / 60)), *SRC)
            for a, img, sc in flames:
                e = min(1, (t - 300) / 100) * (1 if t < 900 else 1 - (t - 900) / 200)
                x = GROUND[0] + math.cos(math.radians(a)) * TW * 0.6
                y = GROUND[1] + math.sin(math.radians(a)) * TW * 0.6 * SQ
                front = math.sin(math.radians(a)) > 0.2          # in front of the fighter: keep them low
                hgt = TH * (0.55 if front else 1.3) * sc
                place(fr, "flame", seq_frame("flame", (t - 300) / 620 + a / 97.0), (x, y), hgt / 225, alpha=0.95 * e)
        # ------------------------------------------------ fury beats 1 and 2: whips
        for t0, e, img, flip in whips:
            ph = t - t0
            if 0 <= ph < 310:
                if ph < STEP:
                    beat = beat or ("FURY 1" if t0 < 550 else "FURY 2")
                # fast uncoil to the snap at 70 ms, then a slower recoil and fade
                p = WHIP_EXT * V.ease_out(ph / 70) if ph < 70 else WHIP_EXT + (1 - WHIP_EXT) * (ph - 70) / 180
                dy = -WHIP_DY if flip else WHIP_DY
                reach = math.hypot(e[0] - SRC[0], e[1] - SRC[1])
                ang = math.degrees(math.atan2(e[1] - SRC[1], e[0] - SRC[0]) - math.atan2(dy * THIN, WHIP_DX))
                place(fr, "whip", seq_frame("whip", p), SRC, reach / math.hypot(WHIP_DX, WHIP_DY * THIN), ang,
                      alpha=1.0 if ph < 200 else 1 - (ph - 200) / 50, flip=flip, thin=THIN)
                if 60 <= ph < 310:
                    place(fr, "burst", seq_frame("burst", (ph - 60) / 250), (e[0], e[1] + TH * 0.15), TW * 0.85 / 260)
        # ------------------------------------------------ fury beat 3: the climax (v21)
        if CLIMAX <= t < CLIMAX + 50:
            beat = "CLIMAX"
            for e, img, flip, th in mb:
                s, c = D.bolt_sprite(img, SRC, e, th * 1.15, 1.0 - (t - CLIMAX) / 150, flip)
                put(fr, s, *c)
            put(fr, xform(V.FLASH[3], TW * (1.7 + (t - CLIMAX) / 80), 0, 0.92 * (1 - (t - CLIMAX) / 70)), *SRC)
        if CLIMAX <= t < CLIMAX + 400:
            u = (t - CLIMAX) / 400
            for a, img in shards:
                rr = SEAL_R * (0.3 + 0.9 * u)
                put(fr, xform(img, SEAL_R * 0.26 * (1 - 0.4 * u), (t - CLIMAX) * 0.6, SEC * (1 - u) ** 1.2, 0.7),
                    GROUND[0] + math.cos(a) * rr, GROUND[1] + math.sin(a) * rr * SQ - TH * 0.6 * math.sin(math.pi * u))
        if CLIMAX + 50 <= t < CLIMAX + 200:
            beat = beat or "FLICKER"
            k, w = {CLIMAX + 50: (0.45, 0.8), CLIMAX + 100: (1.0, 1.0), CLIMAX + 150: (0.18, 0.7)}[w50]
            k *= 1 - (t - w50) / 120             # each restrike decays inside its window
            for e, img, flip, th in mb:
                s, c = D.bolt_sprite(img, SRC, e, th * w, k, flip)
                put(fr, s, *c)
        if CLIMAX <= t < CLIMAX + 200:
            u = V.ease_out((t - CLIMAX) / 200)
            put(fr, xform(D.RING, TW * (2 + 9.4 * u), 0, SEC * (1 - u * 0.8), SQ), *GROUND)
        for t0, e, img, flip, th in sb:
            ph = t - t0
            if 0 <= ph < 100:
                k = 1.0 - ph / 140 if ph < 50 else 0.4 * (1 - (ph - 50) / 60)
                s, c = D.bolt_sprite(img, SRC, e, th * (1 if ph < 50 else 0.8), k, flip)
                put(fr, s, *c)
                if ph < STEP:
                    beat = beat or "STRAGGLERS"
        if CLIMAX < t < CLIMAX + 300:
            u = (t - CLIMAX) / 300
            for e, *_ in mb:
                place(fr, "burst", seq_frame("burst", u), (e[0], e[1] + TH * 0.15), TW * 0.9 / 260)
        if CLIMAX + 200 <= t < CLIMAX + 650:
            beat = beat or "FADE-OUT"
            u = (t - CLIMAX - 200) / 450
            for i, (a, _) in enumerate(smoke):
                q = (t - CLIMAX - 200 - i * 40) / 400
                if 0 <= q <= 1:
                    place(fr, "smoke", seq_frame("smoke", q), (GROUND[0] + math.cos(a) * SEAL_R * 0.45,
                          GROUND[1] + math.sin(a) * SEAL_R * 0.22 - TH * 0.4 - 12 * q), TW * 1.25 / 250, alpha=0.32)
        frames.append(fr.convert("RGB").resize((W // 2, H // 2), Image.LANCZOS))
        labels.append((t, beat))
    frames[0].save(os.path.join(HERE, "fcf_v23_real.gif"), save_all=True, append_images=frames[1:], duration=STEP,
                   loop=0)
    big = [f.resize((f.width * 2, f.height * 2), Image.LANCZOS) for f in frames]
    big[0].save(os.path.join(HERE, "fcf_v23_2x.gif"), save_all=True, append_images=big[1:], duration=STEP, loop=0)
    import subprocess
    tmp = os.path.join(HERE, "_mp4")
    os.makedirs(tmp, exist_ok=True)
    for i, f in enumerate(big):
        f.save(os.path.join(tmp, f"{i:03d}.png"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(1000 / STEP), "-i", os.path.join(tmp, "%03d.png"),
                    "-vf", "loop=2:size=%d" % len(big), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16",
                    os.path.join(HERE, "fcf_v23_2x.mp4")], check=True)
    for f in glob.glob(os.path.join(tmp, "*.png")):
        os.remove(f)
    os.rmdir(tmp)
    keep = [i for i, (t, _) in enumerate(labels) if t % 50 == 0]      # the sheet stays at 50 ms steps
    big, labels = [big[i] for i in keep], [labels[i] for i in keep]
    cols = 4
    fw, fh = big[0].size
    sheet = Image.new("RGB", (fw * cols, (fh + 14) * ((len(big) + cols - 1) // cols)), (12, 12, 12))
    sd = ImageDraw.Draw(sheet)
    for i, (f, (t, b)) in enumerate(zip(big, labels)):
        x, y = (i % cols) * fw, (i // cols) * (fh + 14)
        sheet.paste(f, (x, y + 14))
        sd.text((x + 3, y + 1), f"{t} ms  {b}", fill=(255, 220, 90))
    sheet.save(os.path.join(HERE, "fcf_v23_beats.png"))
    print(len(frames), "frames")


if __name__ == "__main__":
    main()
