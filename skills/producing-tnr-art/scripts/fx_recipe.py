#!/usr/bin/env python3
"""Battle animations from a JSON recipe: Duelyst (CC0) layers -> TNR strips, a real-geometry board preview and a lock
file with everything the upload job needs. The recipe replaces most per-jutsu build scripts (references/duelyst.md).

    python3 fx_recipe.py build RECIPE.json [--out DIR] [--no-board] [--shrink 0.75]
    python3 fx_recipe.py check RECIPE.json          # validate the recipe only (no cache needed)
    python3 fx_recipe.py example                    # print a commented example recipe
    python3 fx_recipe.py --selftest                 # no network; golden White Tiger check when the cache is present

A recipe has clips; a clip is one ANIMATION asset (one strip) and has layers; a layer is one Duelyst animation placed
on the clip's canvas. Geometry is the engine's (combat_fx.md section 2): a clip is a square of `scale` tile heights
centred on its hex; a fighter's feet sit 0.4 tile heights below that centre and the head about 1.2 above it.

Recipe:
  name, slug                      jutsu name; slug names the files (anim_<slug>_<clip>_<px>.webp)
  jutsuId                         optional, recorded in the lock file
  clips[]:
    id                            short name, part of the filename
    role                          caster | target | field     (where the preview draws it)
    slot                          appear | loop | end         (default appear; loop repeats from t=0, as the engine)
    effect                        optional note: which effect tag carries it (e.g. "damage", "increasedamagegiven")
    scale                         animationScale 1-3 (preview size; the strip itself is scale-free)
    ms                            ms per frame for the whole clip (one clock; layers hold frames to slow down)
    lead                          blank frames before anything draws (tells flight time across clips)
    maxPx                         optional cap on the frame size (default: native, then the 4096 px rule)
    upscale                       optional whole-number NEAREST upscale for small pixel art (2, 3); lowered to
                                  the largest multiple the 4096 px rule allows
    layers[]:
      sheet                       Duelyst animation, `sheet` or `sheet:prefix` (duelyst_kit.py find prints them)
      frames                      "a-b" or [i, ...] source indices (default all); drop: [i, ...] removed after
      reverse, flip               bool
      recolour[]                  {"op": "gradient", "lo": 330, "hi": 90, "a": 200, "b": -0.6, "minSat": 0.12}
                                    hue h in [lo, hi] (wrapping; h >= lo counts as h - 360) -> (a + b h) mod 360
                                  {"op": "hue_swap", "lo": 0, "hi": 100, "to": 352, "minSat": 0.2}
                                  {"op": "tint", "rgb": [0.55, 0.3, 1.0]}     whole luminance ramp
      anchor                      {"row": <source px row>, "at": "feet" | "body" | "top" | "centre" | <tile heights>}
                                  (+ is down; feet 0.4, body -0.4, top -1.2, centre 0). Default: frame centre.
      factor                      clip side / source frame side (default 1; 1.3 = the art fills 1/1.3 of the clip)
      dx                          horizontal offset in tile widths (default 0)
      start, hold                 first clip frame (after lead) and clip frames per source frame (default 0, 1)
The first layer sets the native canvas (source side x factor); later layers are resampled onto it.
"""
import argparse
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import duelyst_kit as K  # noqa: E402

AT = {"feet": 0.4, "body": -0.4, "top": -1.2, "centre": 0.0}
ROLES = ("caster", "target", "field")
SLOTS = ("appear", "loop", "end")
OPS = {"gradient": ("lo", "hi", "a", "b"), "hue_swap": ("lo", "hi", "to"), "tint": ("rgb",)}
LICENSE = "CC0 1.0 - OpenDuelyst (open-duelyst/duelyst), {sheets}, adapted for TNR"

EXAMPLE = {
    "name": "Fury of The White Tiger", "slug": "white_tiger", "jutsuId": "QXE9J0fnu1t-DAGTGbaCX",
    "clips": [
        {"id": "gates", "role": "caster", "effect": "increasedamagegiven", "scale": 3, "ms": 70,
         "layers": [{"sheet": "fx_f2_eightgates_teallotus", "frames": "1-33", "drop": [14, 17, 20, 23],
                     "recolour": [{"op": "gradient", "lo": 330, "hi": 90, "a": 200, "b": -0.6, "minSat": 0.12}],
                     "anchor": {"row": 160, "at": "feet"}, "factor": 1.3}]},
        {"id": "tiger", "role": "target", "effect": "damage", "scale": 3, "ms": 80, "lead": 10,
         "layers": [{"sheet": "fx_f2_saberspineseal", "frames": "0-29",
                     "recolour": [{"op": "gradient", "lo": 330, "hi": 90, "a": 200, "b": -0.6, "minSat": 0.12}],
                     "anchor": {"row": 97, "at": "body"}, "factor": 1.4}]},
    ],
}


# ------------------------------------------------------------------------------------------------- recipe
def check(r):
    """List of problems (empty = valid). Structural only; sheets are resolved at build."""
    bad = []
    for k in ("name", "slug", "clips"):
        if k not in r:
            bad.append(f"missing {k}")
    if bad:
        return bad
    if not str(r["slug"]).replace("_", "").isalnum():
        bad.append("slug: letters, digits and _ only")
    ids = set()
    for i, c in enumerate(r["clips"]):
        w = f"clips[{i}]"
        if c.get("id") in ids or not c.get("id"):
            bad.append(f"{w}: id missing or repeated")
        ids.add(c.get("id"))
        if c.get("role") not in ROLES:
            bad.append(f"{w}: role must be one of {ROLES}")
        if c.get("slot", "appear") not in SLOTS:
            bad.append(f"{w}: slot must be one of {SLOTS}")
        if not 1 <= c.get("scale", 0) <= 3:
            bad.append(f"{w}: scale 1-3")
        if not 1 <= c.get("ms", 0) <= 100:
            bad.append(f"{w}: ms 1-100 (the engine's speed range)")
        if not c.get("layers"):
            bad.append(f"{w}: no layers")
        for j, ly in enumerate(c.get("layers", [])):
            v = f"{w}.layers[{j}]"
            if not ly.get("sheet"):
                bad.append(f"{v}: sheet missing")
            for op in ly.get("recolour", []):
                need = OPS.get(op.get("op"))
                if need is None:
                    bad.append(f"{v}: recolour op must be one of {sorted(OPS)}")
                elif any(k not in op for k in need):
                    bad.append(f"{v}: {op['op']} needs {need}")
            at = ly.get("anchor", {}).get("at", "centre")
            if not isinstance(at, (int, float)) and at not in AT:
                bad.append(f"{v}: anchor.at must be one of {sorted(AT)} or a number")
            if ly.get("factor", 1) <= 0 or ly.get("hold", 1) < 1 or ly.get("start", 0) < 0:
                bad.append(f"{v}: factor > 0, hold >= 1, start >= 0")
    return bad


def pick(n, spec, drop=()):
    if spec is None:
        idx = list(range(n))
    elif isinstance(spec, str):
        a, b = (int(x) for x in spec.split("-"))
        idx = list(range(a, b + 1))
    else:
        idx = list(spec)
    if any(i < 0 or i >= n for i in idx):
        raise SystemExit(f"frame index out of range 0-{n - 1}: {spec}")
    return [i for i in idx if i not in set(drop)]


def gradient(im, lo, hi, a, b, min_sat=0.12):
    """Hue h in [lo, hi] (wrapping; h >= lo is read as h - 360 when the range wraps) -> (a + b h) mod 360, keeping
    lightness and saturation. White Tiger: lo 330, hi 90, a 200, b -0.6 turns fire into blue, teal and jade."""
    import colorsys
    from PIL import Image
    px = im.convert("RGBA")
    data = []
    wraps = lo > hi
    for r, g, bl, al in K.pixels(px):
        if al:
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, bl / 255)
            hd = h * 360
            if wraps and hd >= lo:
                hd -= 360
            inside = (hd <= hi) if wraps else (lo <= hd <= hi)
            if inside and s > min_sat:
                nr, ng, nb = colorsys.hls_to_rgb(((a + b * hd) % 360) / 360, l, s)
                r, g, bl = int(nr * 255), int(ng * 255), int(nb * 255)
        data.append((r, g, bl, al))
    out = Image.new("RGBA", px.size)
    out.putdata(data)
    return out


def recolour(im, ops):
    for op in ops:
        if op["op"] == "gradient":
            im = gradient(im, op["lo"], op["hi"], op["a"], op["b"], op.get("minSat", 0.12))
        elif op["op"] == "hue_swap":
            im = K.hue_swap(im, op["lo"], op["hi"], op["to"], op.get("minSat", 0.2))
        elif op["op"] == "tint":
            im = K.tint(im, op["rgb"])
    return im


def union_bbox(frs):
    boxes = [f.getbbox() for f in frs if f.getbbox()]
    if not boxes:
        return (0, 0, frs[0].width, frs[0].height)
    return (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))


def render_clip(c, app=None, log=None):
    """Native-size frames for one clip, the native side, and rows cut at the canvas top/bottom per layer."""
    from PIL import Image, ImageOps
    scale = c["scale"]
    W = None
    timelines, cuts = [], []
    for ly in c["layers"]:
        src = K.squared(K.frames(ly["sheet"], app))
        frs = [src[i] for i in pick(len(src), ly.get("frames"), ly.get("drop", ()))]
        if ly.get("reverse"):
            frs = frs[::-1]
        frs = [recolour(f, ly.get("recolour", [])) for f in frs]
        if ly.get("flip"):
            frs = [ImageOps.mirror(f) for f in frs]
        s = frs[0].width
        factor = ly.get("factor", 1.0)
        if W is None:
            W = int(round(s * factor))
        side = int(round(W / factor))
        ratio = side / s
        if side != s:
            rs = Image.NEAREST if (side % s == 0) else Image.LANCZOS
            frs = [f.resize((side, side), rs) for f in frs]
        u = union_bbox(frs)
        anchor = ly.get("anchor", {})
        row = anchor.get("row", s / 2) * ratio
        at = anchor.get("at", "centre")
        at_h = AT[at] if isinstance(at, str) else float(at)
        target_row = W / 2 + at_h / scale * W
        ox = int(round(W / 2 + ly.get("dx", 0) * 2 * W / scale - (u[0] + u[2]) / 2))
        oy = int(round(target_row - row))
        cuts.append((max(0, -(oy + u[1])), max(0, oy + u[3] - W)))
        start, hold = c.get("lead", 0) + ly.get("start", 0), ly.get("hold", 1)
        timelines.append((frs, ox, oy, start, hold))
    n = max(start + len(frs) * hold for frs, _, _, start, hold in timelines)
    out = []
    for t in range(n):
        cv = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        for frs, ox, oy, start, hold in timelines:
            k = (t - start) // hold
            if t >= start and k < len(frs):
                layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
                layer.paste(frs[k], (ox, oy), frs[k])
                cv.alpha_composite(layer)
        out.append(cv)
    if log and any(a or b for a, b in cuts):
        log(f"clip {c['id']}: rows cut (top, bottom) per layer {cuts}: the art leaves the clip square")
    return out, W, cuts


def deliver(frs, W, max_px=None, upscale=1):
    """Frame size for the strip: native (times a whole NEAREST upscale where the 4096 px rule leaves room), capped by
    maxPx and by the 4096 px rule (frame px x frames), even."""
    from PIL import Image
    limit = K.TEXTURE_MAX // len(frs)
    if max_px:
        limit = min(limit, max_px)
    k = max(1, min(int(upscale), limit // W))
    if k > 1:
        frs, W = [f.resize((W * k, W * k), Image.NEAREST) for f in frs], W * k
    px = min(W, limit)
    px -= px % 2
    if px == W:
        return frs, px
    return [f.resize((px, px), Image.LANCZOS) for f in frs], px


# -------------------------------------------------------------------------------------------------- board
def hex_poly(x, y, w, h):
    return [(x - w / 2, y), (x - w / 4, y - h / 2), (x + w / 4, y - h / 2), (x + w / 2, y), (x + w / 4, y + h / 2),
            (x - w / 4, y + h / 2)]


def cube(c, r):
    x = c
    z = r - (c - (c & 1)) // 2
    return x, -x - z, z


def hex_dist(a, b):
    ax, ay, az = cube(*a)
    bx, by, bz = cube(*b)
    return max(abs(ax - bx), abs(ay - by), abs(az - bz))


def board(clips, out, title="", cols=12, rows=8, caster=(3, 4), target=(7, 3), radius=4, px=2, shrink=0.75,
          loops=2):
    """Real-board preview: 2:1 hexes at phone width (360 CSS px), stand-in fighters at engine geometry, every clip on
    one clock from the strike (t = 0): appears once, loops repeat `loops` times from t = 0, ends after the loops.
    clips: [(clip dict, frames at delivered size)]."""
    from PIL import Image, ImageDraw
    STACK = 0.25
    hs = 360 / (cols - STACK * (cols - 1))
    w, h = hs * px, hs * 0.5 * px
    W, H = int(360 * px), int((rows + 0.5) * h)
    tiles = {(c, r): (c * w * (1 - STACK) + w / 2, r * h + h / 2 + (h / 2 if c % 2 else 0))
             for c in range(cols) for r in range(rows)}
    field = [k for k in tiles if k != caster and hex_dist(k, caster) <= radius]
    base = Image.new("RGBA", (W, H), (36, 40, 36, 255))
    d = ImageDraw.Draw(base)
    for (x, y) in tiles.values():
        d.polygon(hex_poly(x, y, w, h), outline=(255, 255, 255, 30))
    for (cx, cy) in (tiles[caster], tiles[target]):     # feet 0.4 h below the hex centre, head ~1.2 h above
        feet, top = cy + 0.4 * h, cy - 1.2 * h
        d.ellipse((cx - w * 0.16, feet - h * 0.09, cx + w * 0.16, feet + h * 0.09), fill=(0, 0, 0, 80))
        d.rounded_rectangle((cx - w * 0.085, top + w * 0.16, cx + w * 0.085, feet - 3), radius=6,
                            fill=(66, 64, 78, 255))
        d.ellipse((cx - w * 0.1, top, cx + w * 0.1, top + w * 0.2), fill=(66, 64, 78, 255))
    lay = []
    for c, frs in clips:
        e = int(round(h * c["scale"]))
        frs = [f.resize((e, e), Image.LANCZOS) for f in frs]
        where = {"caster": [tiles[caster]], "target": [tiles[target]],
                 "field": sorted((tiles[k] for k in field), key=lambda p: p[1])}[c["role"]]
        lay.append((c, frs, e, where))
    run = lambda c, frs: len(frs) * c["ms"]  # noqa: E731
    lasting = max([run(c, f) * loops for c, f, _, _ in lay if c.get("slot") == "loop"] or [0])
    ends = [(c, f, e, wh) for c, f, e, wh in lay if c.get("slot") == "end"]
    total = max([run(c, f) for c, f, _, _ in lay if c.get("slot", "appear") == "appear"] + [lasting] +
                [lasting + run(c, f) for c, f, _, _ in ends]) + 400
    marks = {0, total}
    for c, frs, _, _ in lay:
        t0 = lasting if c.get("slot") == "end" else 0
        t1 = lasting if c.get("slot") == "loop" else t0 + run(c, frs)
        marks |= set(range(t0, t1 + 1, c["ms"]))
    times = sorted(m for m in marks if m <= total)
    shots, durs = [], []
    for t0, t1 in zip(times, times[1:]):
        im = base.copy()
        for c, frs, e, where in sorted(lay, key=lambda x: ROLES.index(x[0]["role"]), reverse=True):
            slot = c.get("slot", "appear")
            if slot == "loop":
                k = (t0 // c["ms"]) % len(frs) if t0 < lasting else None
            elif slot == "end":
                k = (t0 - lasting) // c["ms"] if lasting <= t0 < lasting + run(c, frs) else None
            else:
                k = t0 // c["ms"] if t0 < run(c, frs) else None
            if k is None:
                continue
            for (x, y) in where:
                im.alpha_composite(frs[k], (int(x - e / 2), int(y - e / 2)))
        ImageDraw.Draw(im).text((6, 4), f"{title}  t={t0} ms", fill=(255, 255, 255, 220))
        im = im.convert("RGB")
        if shrink != 1:
            im = im.resize((int(W * shrink), int(H * shrink)), Image.LANCZOS)
        shots.append(im)
        durs.append(t1 - t0)
    q, acc, done = [], 0, 0          # GIF delays are whole centiseconds: carry the rounding
    for dm in durs:
        acc += dm
        step = max(20, int(round((acc - done) / 10.0)) * 10)
        q.append(step)
        done += step
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=q, loop=0, optimize=True)
    return len(shots)


# -------------------------------------------------------------------------------------------------- build
def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build(recipe_path, out=None, preview=True, shrink=0.75, app=None, log=print):
    r = json.load(open(recipe_path))
    bad = check(r)
    if bad:
        raise SystemExit("recipe problems:\n  " + "\n  ".join(bad))
    out = out or os.path.join(os.path.dirname(os.path.abspath(recipe_path)), r["slug"])
    os.makedirs(out, exist_ok=True)
    rows, built = [], []
    for c in r["clips"]:
        frs, W, cuts = render_clip(c, app, log)
        frs, px = deliver(frs, W, c.get("maxPx"), c.get("upscale", 1))
        fn = f"anim_{r['slug']}_{c['id']}_{px}.webp"
        p = os.path.join(out, fn)
        b = K.write_strip(frs, p, px)
        sheets = sorted({ly["sheet"].split(":")[0] for ly in c["layers"]})
        rows.append({"clip": c["id"], "role": c["role"], "slot": c.get("slot", "appear"),
                     "effect": c.get("effect", ""), "scale": c["scale"], "file": fn, "frames": len(frs),
                     "speed": c["ms"], "px": px, "nativePx": W, "height": px * len(frs), "bytes": b,
                     "sha256": sha(p), "licenseDetails": LICENSE.format(sheets=" / ".join(sheets)),
                     "rowsCut": cuts})
        built.append((c, frs))
        log(f"{fn}: {len(frs)} frames x {c['ms']} ms, {px} px ({px * len(frs)} px tall), {b} bytes")
    lock = {"recipe": os.path.basename(recipe_path), "recipeSha256": sha(recipe_path), "name": r["name"],
            "jutsuId": r.get("jutsuId", ""), "duelystPin": K.PIN, "clips": rows}
    lp = os.path.join(out, "recipe.lock.json")
    json.dump(lock, open(lp, "w"), indent=1, ensure_ascii=False)
    open(lp, "a").write("\n")
    log(f"lock: {lp}")
    if preview:
        g = os.path.join(out, f"preview_{r['slug']}_board.gif")
        n = board(built, g, title=r["name"], shrink=shrink)
        log(f"board: {g} ({n} frames)")
    return lock


# ------------------------------------------------------------------------------------------------ selftest
def selftest():
    """No network. Synthetic sheets through render/deliver/build/board; the White Tiger golden when the cache and the
    repository's committed strips are both present."""
    import plistlib
    import tempfile
    from PIL import Image
    assert check(EXAMPLE) == [], check(EXAMPLE)
    bad = check({"name": "x", "slug": "x y", "clips": [{"id": "a", "role": "side", "scale": 4, "ms": 0,
                                                         "layers": [{"recolour": [{"op": "blur"}]}]}]})
    assert len(bad) == 6, bad
    assert pick(10, "2-5", [3]) == [2, 4, 5] and pick(4, None) == [0, 1, 2, 3]

    # gradient: pure red (h 0) -> 200; pure green (h 120) outside [330, 90] stays.
    im = Image.new("RGBA", (2, 1))
    im.putdata([(255, 0, 0, 255), (0, 255, 0, 255)])
    import colorsys
    g = gradient(im, 330, 90, 200, -0.6)
    hue = lambda p: colorsys.rgb_to_hls(*(v / 255 for v in p[:3]))[0] * 360  # noqa: E731
    assert abs(hue(g.getpixel((0, 0))) - 200) < 1.5 and g.getpixel((1, 0)) == (0, 255, 0, 255)

    # a synthetic 3-frame fx sheet (20 x 20, a 4 px block at the bottom centre) in a temp app tree
    tmp = tempfile.mkdtemp()
    app = os.path.join(tmp, "app")
    fx = os.path.join(app, "resources", "fx")
    os.makedirs(fx)
    os.makedirs(os.path.join(app, "data"))
    open(os.path.join(app, "data", "resources.js"), "w").write("")
    atlas = Image.new("RGBA", (60, 20), (0, 0, 0, 0))
    for i in range(3):
        atlas.paste((255, 60 * i, 0, 255), (i * 20 + 8, 14, i * 20 + 12, 18))
    atlas.save(os.path.join(fx, "fx_t.png"))
    plistlib.dump({"frames": {f"fx_t_{i}.png": {"frame": "{{%d,0},{20,20}}" % (i * 20), "rotated": False,
                                                   "sourceSize": "{20,20}", "sourceColorRect": "{{0,0},{20,20}}"}
                              for i in range(3)}, "metadata": {"format": 2}}, open(os.path.join(fx, "fx_t.plist"), "wb"))
    clip = {"id": "c", "role": "target", "scale": 2, "ms": 80, "lead": 2,
            "layers": [{"sheet": "fx_t", "anchor": {"row": 18, "at": "feet"}, "factor": 2},
                       {"sheet": "fx_t", "frames": [0], "start": 1, "hold": 3, "factor": 4}]}
    frs, W, cuts = render_clip(clip, app)
    assert W == 40 and len(frs) == 2 + 1 + 3 and frs[0].getbbox() is None, (W, len(frs))
    # layer 1: source row 18 lands on the feet: 40/2 + 0.4/2*40 = 28 -> the block's bottom edge at row 28
    bb = frs[2].getbbox()
    assert bb[3] == 28 and (bb[0] + bb[2]) / 2 == 20, bb
    # layer 2 (factor 4: half size, centred on the frame) holds 3 clip frames from lead + 1; frame 5 is it alone
    b5 = frs[5].getbbox()
    assert b5 and (b5[0] + b5[2]) / 2 == 20 and b5[2] - b5[0] <= 4, b5
    big = [frs[0]] * 40
    _, px = deliver(big, 200)
    assert px * 40 <= 4096 and px % 2 == 0
    _, px = deliver(frs, W, max_px=30)
    assert px == 30
    up, px = deliver(frs, W, upscale=3)                     # 6 frames x 120 px fits under 4096: NEAREST x3
    assert px == 120 and up[2].getpixel((60, 60)) == frs[2].resize((120, 120), Image.NEAREST).getpixel((60, 60))
    _, px = deliver([frs[0]] * 40, W, upscale=3)           # 40 frames: 4096 // 40 = 102 -> x2 (80 px)
    assert px == 80

    rp = os.path.join(tmp, "r.json")
    json.dump({"name": "Test", "slug": "test", "clips": [clip, dict(clip, id="f", role="field", slot="loop"),
                                                      dict(clip, id="k", role="caster")]}, open(rp, "w"))
    lock = build(rp, os.path.join(tmp, "o"), preview=True, app=app, log=lambda *_: None)
    row = lock["clips"][0]
    assert row["file"] == "anim_test_c_40.webp" and row["frames"] == 6 and row["speed"] == 80
    assert row["licenseDetails"] == "CC0 1.0 - OpenDuelyst (open-duelyst/duelyst), fx_t, adapted for TNR"
    assert Image.open(os.path.join(tmp, "o", row["file"])).size == (40, 240)
    assert os.path.exists(os.path.join(tmp, "o", "preview_test_board.gif"))

    # golden: the White Tiger recipe reproduces the strips shipped on 2026-11-17 (art/duelyst_fx/showcase/final)
    repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    final = os.path.join(repo, "art", "duelyst_fx", "showcase", "final")
    golden = os.path.join(final, "anim_white_tiger_gates_140.webp")
    real = K.app_dir()
    if os.path.exists(golden) and os.path.exists(os.path.join(real, "resources", "fx")):
        rp = os.path.join(tmp, "white_tiger.json")
        json.dump(EXAMPLE, open(rp, "w"))
        lock = build(rp, os.path.join(tmp, "wt"), preview=False, log=lambda *_: None)
        for row, ref in zip(lock["clips"], ("anim_white_tiger_gates_140.webp", "anim_white_tiger_tiger_102.webp")):
            assert row["file"] == ref, (row["file"], ref)
            a = Image.open(os.path.join(tmp, "wt", row["file"])).convert("RGBA")
            b = Image.open(os.path.join(final, ref)).convert("RGBA")
            assert a.size == b.size and a.tobytes() == b.tobytes(), f"{ref}: pixels differ from the shipped strip"
        print("fx_recipe selftest: golden White Tiger strips reproduced pixel for pixel")
    else:
        print("fx_recipe selftest: no cache or no committed strips, golden case skipped")
    print("fx_recipe selftest: PASS")


def main():
    if "--selftest" in sys.argv:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    b.add_argument("recipe")
    b.add_argument("--out")
    b.add_argument("--no-board", action="store_true")
    b.add_argument("--shrink", type=float, default=0.75)
    c = sub.add_parser("check")
    c.add_argument("recipe")
    sub.add_parser("example")
    a = ap.parse_args()
    if a.cmd == "build":
        build(a.recipe, a.out, not a.no_board, a.shrink)
    elif a.cmd == "check":
        bad = check(json.load(open(a.recipe)))
        print("\n".join(bad) if bad else "recipe OK")
        sys.exit(1 if bad else 0)
    else:
        print(json.dumps(EXAMPLE, indent=1))


if __name__ == "__main__":
    main()
