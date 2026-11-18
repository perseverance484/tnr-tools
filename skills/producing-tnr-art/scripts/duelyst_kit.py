#!/usr/bin/env python3
"""Duelyst kit: OpenDuelyst's CC0 effects and units as a searchable, remixable library for TNR battle art.

    python3 duelyst_kit.py fetch                     # pinned sparse clone into the cache (network: GitHub only)
    python3 duelyst_kit.py catalog [--out PATH]      # (re)build the catalogue from the cache
    python3 duelyst_kit.py find [--kind fx|unit] [--hue teal] [--shape tall] [--min-frames N]
                                [--max-frames N] [--action idle] [TERMS..]
    python3 duelyst_kit.py sheet [find options] --out matches.gif     # animated contact sheet of the matches
    python3 duelyst_kit.py strip SHEET[:PREFIX] out.webp [--size 288] [--fit 1.0] [--dy 0] [--tint R,G,B]
                                [--swap LO:HI:HUE] [--nearest]
    python3 duelyst_kit.py --selftest

Source: github.com/open-duelyst/duelyst, pinned at PIN, released CC0 1.0 after the game closed (2020); record it in
the asset's licenseDetails. The assets (~70 MB) live in a cache OUTSIDE the repository: $TNR_DUELYST, default
~/.cache/tnr-duelyst. The repository carries only this script and data/duelyst_catalog.json.

Sheets are cocos2d plists (format 2): each frame has a `frame` rect in the atlas (`rotated` = stored 90 degrees
clockwise) and a `sourceColorRect` placing the trimmed pixels in `sourceSize`. One sheet can hold several
animations (units: idle, run, attack, hit, death, breathing, caststart, cast, castend...), named by frame prefix;
`frameDelay` per animation comes from app/data/resources.js. Pixel art: scale by whole steps with NEAREST
(--nearest, or --size a multiple of the source) to keep it crisp. How to use it: references/combat_fx.md, section
"Duelyst library (CC0)".
"""
import argparse
import colorsys
import json
import os
import plistlib
import re
import subprocess
import sys

PIN = "df697549cad25dae6f7a2a863989e2e380841a5b"
REPO = "https://github.com/open-duelyst/duelyst.git"
KINDS = {"fx": "app/resources/fx", "unit": "app/resources/units"}  # particles/ are emitter configs, not sheets
HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(HERE, "..", "data", "duelyst_catalog.json")
HUES = [("red", 0, 15), ("orange", 15, 40), ("yellow", 40, 70), ("green", 70, 150), ("teal", 150, 195),
        ("blue", 195, 250), ("purple", 250, 290), ("pink", 290, 345), ("red", 345, 361)]
NUM = re.compile(r"(\d+)")


def cache_dir():
    return os.environ.get("TNR_DUELYST") or os.path.expanduser("~/.cache/tnr-duelyst")


def app_dir(cache=None):
    return os.path.join(cache or cache_dir(), "app")


# ------------------------------------------------------------------------------------------------- fetch
def fetch(cache=None):
    """Blobless sparse clone at PIN: effects, units and the data folder (resources.js)."""
    cache = cache or cache_dir()
    if not os.path.isdir(os.path.join(cache, ".git")):
        subprocess.run(["git", "clone", "-q", "--filter=blob:none", "--sparse", "--no-checkout", REPO, cache],
                       check=True)
    subprocess.run(["git", "-C", cache, "sparse-checkout", "set", "--no-cone", "app/data/*",
                    *(p + "/*" for p in KINDS.values())], check=True)
    subprocess.run(["git", "-C", cache, "checkout", "-q", PIN], check=True)
    head = subprocess.check_output(["git", "-C", cache, "rev-parse", "HEAD"]).decode().strip()
    if head != PIN:
        raise SystemExit(f"cache at {head}, expected {PIN}")
    print(f"duelyst cache ready at {cache} @ {PIN[:10]}")


# ----------------------------------------------------------------------------------------------- reading
def _nums(s):
    return [int(float(x)) for x in re.findall(r"-?\d+\.?\d*", s)]


def pixels(im):
    """Pixel tuples (Pillow 12+ get_flattened_data, older getdata)."""
    return list(im.get_flattened_data() if hasattr(im, "get_flattened_data") else im.getdata())


def natural(k):
    return [int(t) if t.isdigit() else t for t in NUM.split(k)]


def split(name):
    """`sheet` or `sheet:prefix`."""
    sheet, _, prefix = name.partition(":")
    return sheet, prefix


def locate(sheet, app=None):
    app = app or app_dir()
    for kind, sub in KINDS.items():
        p = os.path.join(app, sub.replace("app/", "", 1), sheet + ".plist")
        if os.path.exists(p):
            return kind, p
    raise SystemExit(f"no sheet {sheet!r} in {app} (run fetch; names are file stems, e.g. fx_bluewatersplash)")


def read_plist(path):
    return plistlib.load(open(path, "rb"))


def sequences_of(plist):
    out = {}
    for k in plist.get("frames", {}):
        pre = re.sub(r"\d+\.png$", "", k)
        out[pre] = out.get(pre, 0) + 1
    return out


def frames(name, app=None):
    """Full-size RGBA frames of one sheet (or `sheet:prefix` animation), in order."""
    from PIL import Image
    sheet, prefix = split(name)
    _, path = locate(sheet, app)
    d = read_plist(path)
    seqs = sequences_of(d)
    if not prefix and len(seqs) > 1:
        raise SystemExit(f"{sheet} holds several animations, pick one as {sheet}:<prefix>: {sorted(seqs)}")
    atlas = Image.open(path[:-6] + ".png").convert("RGBA")
    out = []
    for k in sorted(d["frames"], key=natural):
        if prefix and not k.startswith(prefix):
            continue
        v = d["frames"][k]
        x, y, w, h = _nums(v["frame"])[:4]
        piece = (atlas.crop((x, y, x + h, y + w)).rotate(90, expand=True) if v.get("rotated")
                 else atlas.crop((x, y, x + w, y + h)))
        sw, sh = _nums(v["sourceSize"])[:2]
        cx, cy = _nums(v["sourceColorRect"])[:2]
        full = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
        full.paste(piece, (cx, cy))
        out.append(full)
    if not out:
        raise SystemExit(f"no frames for {name}")
    return out


def delays(app=None):
    """{(plist stem, framePrefix): ms} from resources.js."""
    path = os.path.join(app or app_dir(), "data", "resources.js")
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8", errors="replace"):
        m = re.search(r"framePrefix:\s*'([^']+)'.*?frameDelay:\s*([0-9.]+).*?plist:\s*'[^']*/([^/']+)\.plist'", line)
        if m:
            out[(m.group(3), m.group(1))] = int(round(float(m.group(2)) * 1000))
    return out


def delay_ms(name, table=None, default=80):
    sheet, prefix = split(name)
    table = table if table is not None else delays()
    if prefix:
        return table.get((sheet, prefix), default)
    hits = [v for (s, _), v in table.items() if s == sheet]
    return hits[0] if hits else default


# ----------------------------------------------------------------------------------------------- shaping
def squared(frs):
    from PIL import Image
    s = max(max(f.width for f in frs), max(f.height for f in frs))
    out = []
    for f in frs:
        c = Image.new("RGBA", (s, s), (0, 0, 0, 0))
        c.paste(f, ((s - f.width) // 2, (s - f.height) // 2))
        out.append(c)
    return out


def tint(im, rgb):
    """Recolour by luminance into a ramp dark -> rgb -> white (keeps the drawing, swaps the palette)."""
    from PIL import Image, ImageOps
    r, g, b, a = im.split()
    lum = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))
    col = ImageOps.colorize(lum, black=tuple(int(255 * c * 0.25) for c in rgb),
                            mid=tuple(int(255 * c) for c in rgb), white=(250, 244, 255), midpoint=110)
    out = col.convert("RGBA")
    out.putalpha(a)
    return out


def hue_swap(im, lo, hi, new, min_sat=0.2):
    """Move pixels whose hue is in [lo, hi] degrees (wrapping) to hue `new`, keeping lightness and saturation.
    For a selective recolour: Reefward Bastion moved the gold ring (0-100) to coral (352) and left the water blue."""
    from PIL import Image
    px = im.convert("RGBA")
    data = []
    for r, g, b, a in pixels(px):
        if a:
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            hd = h * 360
            inside = lo <= hd <= hi if lo <= hi else (hd >= lo or hd <= hi)
            if inside and s > min_sat:
                nr, ng, nb = colorsys.hls_to_rgb(new / 360, l, s)
                r, g, b = int(nr * 255), int(ng * 255), int(nb * 255)
        data.append((r, g, b, a))
    out = Image.new("RGBA", px.size)
    out.putdata(data)
    return out


def place(frs, size_px, fit=1.0, dy=0.0, tint_rgb=None, swap=None, nearest=False):
    """Square TNR frames of `size_px`: art scaled to `fit` of the frame, shifted dy (fraction, + = down)."""
    from PIL import Image
    sq = squared(frs)
    s = sq[0].width
    target = max(1, int(size_px * fit))
    out = []
    for f in sq:
        if swap:
            f = hue_swap(f, *swap)
        if tint_rgb:
            f = tint(f, tint_rgb)
        resample = Image.NEAREST if (nearest or target % s == 0) else Image.LANCZOS
        g = f.resize((target, target), resample)
        c = Image.new("RGBA", (size_px, size_px), (0, 0, 0, 0))
        c.alpha_composite(g, ((size_px - target) // 2, (size_px - target) // 2 + int(dy * size_px)))
        out.append(c)
    return out


def write_strip(frs, path, size_px):
    """One-column vertical strip, lossless WebP (the TNR ANIMATION format)."""
    from PIL import Image
    sheet = Image.new("RGBA", (size_px, size_px * len(frs)), (0, 0, 0, 0))
    for i, f in enumerate(frs):
        sheet.paste(f, (0, i * size_px))
    sheet.save(path, "WEBP", lossless=True, method=6)
    return os.path.getsize(path)


# ---------------------------------------------------------------------------------------------- catalogue
def hue_name(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    if l > 0.85 and s < 0.35 or s < 0.12:
        return "white" if l > 0.5 else "dark"
    hd = h * 360
    return next(n for n, lo, hi in HUES if lo <= hd < hi)


def stats(frs):
    """Dominant hue bucket (opaque pixels, weighted by alpha), union-bbox shape, mean coverage of the square."""
    from collections import Counter
    sq = squared(frs)
    s = sq[0].width
    counts, cover, union = Counter(), 0.0, None
    step = max(1, len(sq) // 8)
    for f in sq[::step]:
        small = f.resize((32, 32))
        for r, g, b, a in pixels(small):
            if a > 40:
                counts[hue_name(r, g, b)] += a
        bb = f.getbbox()
        if bb:
            union = bb if union is None else (min(union[0], bb[0]), min(union[1], bb[1]),
                                              max(union[2], bb[2]), max(union[3], bb[3]))
        cover += sum(1 for v in pixels(f.getchannel("A").resize((32, 32))) if v > 40) / 1024
    top = [n for n, _ in counts.most_common(2)]
    if union:
        w, h = union[2] - union[0], union[3] - union[1]
        shape = "tall" if h > 1.4 * w else "wide" if w > 1.4 * h else "round"
    else:
        shape = "empty"
    return {"hue": top, "shape": shape, "cover": round(cover / len(sq[::step]), 2), "px": s}


def catalog(out=None, app=None):
    app = app or app_dir()
    table = delays(app)
    entries = []
    for kind, sub in KINDS.items():
        folder = os.path.join(app, sub.replace("app/", "", 1))
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".plist") or not os.path.exists(os.path.join(folder, fn[:-6] + ".png")):
                continue
            stem = fn[:-6]
            try:
                d = read_plist(os.path.join(folder, fn))
            except Exception:  # noqa: BLE001 - a malformed sheet is skipped and reported below
                print(f"skip {stem}: unreadable plist", file=sys.stderr)
                continue
            seqs = sequences_of(d)
            if not seqs:
                continue
            row = {"name": stem, "kind": kind, "seq": {}}
            for pre, n in sorted(seqs.items()):
                action = pre[len(stem):].strip("_") if pre.startswith(stem) else pre.strip("_")
                row["seq"][pre] = {"action": action or "main", "frames": n,
                                   "ms": table.get((stem, pre), 80)}
            first = sorted(seqs)[0] if len(seqs) > 1 else ""
            pick = next((p for p in seqs if p.endswith("idle_")), first)
            try:
                row.update(stats(frames(stem + (":" + pick if len(seqs) > 1 else ""), app)))
            except SystemExit as e:
                print(f"skip stats {stem}: {e}", file=sys.stderr)
            entries.append(row)
    data = {"source": REPO, "pin": PIN, "license": "CC0 1.0 (OpenDuelyst)",
            "note": "Built by duelyst_kit.py catalog; do not hand-edit. Assets live in the cache, not the repo.",
            "entries": entries}
    out = out or CATALOG
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
        fh.write("\n")
    by = {k: sum(1 for e in entries if e["kind"] == k) for k in KINDS}
    print(f"catalogue: {len(entries)} sheets {by} -> {out} ({os.path.getsize(out)} bytes)")
    return data


def load_catalog(path=None):
    path = path or CATALOG
    if not os.path.exists(path):
        raise SystemExit(f"no catalogue at {path}: run fetch, then catalog")
    return json.load(open(path))


def find(cat, kind=None, hue=None, shape=None, terms=(), min_frames=None, max_frames=None, action=None):
    out = []
    for e in cat["entries"]:
        if kind and e["kind"] != kind:
            continue
        if hue and hue not in e.get("hue", []):
            continue
        if shape and e.get("shape") != shape:
            continue
        if terms and not all(t.lower() in e["name"].lower() for t in terms):
            continue
        for pre, s in e["seq"].items():
            if action and s["action"] != action:
                continue
            if min_frames and s["frames"] < min_frames or max_frames and s["frames"] > max_frames:
                continue
            ref = e["name"] + (":" + pre if len(e["seq"]) > 1 else "")
            out.append((ref, e, s))
    return out


def contact(refs, out, app=None, cell=150, cols=5):
    """Animated contact sheet: every match plays on its own clock, with a short gap between plays."""
    from PIL import Image, ImageDraw
    table = delays(app)
    clips = []
    for ref in refs:
        frs = squared(frames(ref, app))
        s = frs[0].width
        clips.append((ref.split(":")[-1].replace("fx_", "")[:26],
                      [f.resize((cell, cell), Image.NEAREST if s <= cell else Image.LANCZOS) for f in frs],
                      delay_ms(ref, table)))
    rows = (len(clips) + cols - 1) // cols
    W, H = cols * cell, rows * (cell + 14)
    shots = []
    for t in range(0, 2400, 40):
        im = Image.new("RGB", (W, H), (34, 36, 32))
        d = ImageDraw.Draw(im)
        for i, (label, frs, ms) in enumerate(clips):
            x, y = (i % cols) * cell, (i // cols) * (cell + 14)
            k = (t // ms) % (len(frs) + 6)
            if k < len(frs):
                im.paste(frs[k], (x, y + 14), frs[k])
            d.text((x + 3, y + 1), label, fill=(220, 220, 220))
        shots.append(im)
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=40, loop=0, optimize=True)
    return out


# ------------------------------------------------------------------------------------------------ selftest
def selftest():
    """No network: a synthetic two-animation sheet (one rotated frame) through frames/sequences/place/strip,
    catalog on a temp app tree, find, hue_swap and delays."""
    import tempfile
    from PIL import Image
    tmp = tempfile.mkdtemp()
    app = os.path.join(tmp, "app")
    for sub in KINDS.values():
        os.makedirs(os.path.join(tmp, sub), exist_ok=True)
    os.makedirs(os.path.join(app, "data"), exist_ok=True)
    atlas = Image.new("RGBA", (40, 20), (0, 0, 0, 0))
    atlas.paste((255, 200, 0, 255), (0, 0, 10, 20))     # frame a_idle_0: 10x20 at (0,0), not rotated
    atlas.paste((0, 120, 255, 255), (10, 0, 30, 10))    # frame a_hit_0: stored rotated, 10x20 source
    atlas.save(os.path.join(app, "resources", "units", "a.png"))
    frames_d = {
        "a_idle_0.png": {"frame": "{{0,0},{10,20}}", "rotated": False, "sourceSize": "{30,30}",
                         "sourceColorRect": "{{10,5},{10,20}}"},
        "a_hit_0.png": {"frame": "{{10,0},{10,20}}", "rotated": True, "sourceSize": "{30,30}",
                        "sourceColorRect": "{{10,5},{10,20}}"},
    }
    plistlib.dump({"frames": frames_d, "metadata": {"format": 2}},
                  open(os.path.join(app, "resources", "units", "a.plist"), "wb"))
    open(os.path.join(app, "data", "resources.js"), "w").write(
        "  aIdle: { name: 'aIdle', framePrefix: 'a_idle_', frameDelay: 0.12, img: 'resources/units/a.png', "
        "plist: 'resources/units/a.plist',\n")
    assert sequences_of(read_plist(os.path.join(app, "resources", "units", "a.plist"))) == {"a_idle_": 1, "a_hit_": 1}
    try:
        frames("a", app)
        raise AssertionError("multi-animation sheet without a prefix must refuse")
    except SystemExit:
        pass
    idle = frames("a:a_idle_", app)
    hit = frames("a:a_hit_", app)
    assert idle[0].size == (30, 30) and idle[0].getpixel((12, 10))[:3] == (255, 200, 0)
    assert hit[0].size == (30, 30) and hit[0].getbbox() == (10, 5, 20, 25), hit[0].getbbox()
    assert delay_ms("a:a_idle_", delays(app)) == 120 and delay_ms("a:a_hit_", delays(app)) == 80
    placed = place(idle, 90, nearest=True)
    assert placed[0].size == (90, 90) and placed[0].getpixel((45, 40))[:3] == (255, 200, 0)
    sw = hue_swap(idle[0], 0, 100, 352)
    h = colorsys.rgb_to_hls(*(c / 255 for c in sw.getpixel((12, 10))[:3]))[0] * 360
    assert abs(h - 352) < 2, h
    p = os.path.join(tmp, "s.webp")
    write_strip(placed, p, 90)
    assert Image.open(p).size == (90, 90)
    cat = catalog(os.path.join(tmp, "cat.json"), app)
    assert len(cat["entries"]) == 1 and cat["entries"][0]["seq"]["a_idle_"]["ms"] == 120
    hits = find(cat, kind="unit", action="hit")
    assert [r for r, _, _ in hits] == ["a:a_hit_"], hits
    print("duelyst_kit selftest: PASS")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--selftest", action="store_true")
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("fetch")
    c = sp.add_parser("catalog")
    c.add_argument("--out")
    for name in ("find", "sheet"):
        f = sp.add_parser(name)
        f.add_argument("terms", nargs="*")
        f.add_argument("--kind", choices=list(KINDS))
        f.add_argument("--hue", choices=sorted({n for n, _, _ in HUES} | {"white", "dark"}))
        f.add_argument("--shape", choices=["tall", "wide", "round"])
        f.add_argument("--action")
        f.add_argument("--min-frames", type=int)
        f.add_argument("--max-frames", type=int)
        f.add_argument("--limit", type=int, default=40)
        if name == "sheet":
            f.add_argument("--out", required=True)
    s = sp.add_parser("strip")
    s.add_argument("name")
    s.add_argument("out")
    s.add_argument("--size", type=int, default=288)
    s.add_argument("--fit", type=float, default=1.0)
    s.add_argument("--dy", type=float, default=0.0)
    s.add_argument("--tint")
    s.add_argument("--swap", help="LO:HI:HUE in degrees, e.g. 0:100:352 (gold -> coral)")
    s.add_argument("--nearest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.cmd == "fetch":
        return fetch()
    if a.cmd == "catalog":
        return catalog(a.out)
    if a.cmd in ("find", "sheet"):
        hits = find(load_catalog(), a.kind, a.hue, a.shape, a.terms, a.min_frames, a.max_frames, a.action)
        hits = hits[:a.limit]
        for ref, e, s in hits:
            print(f"{ref:58s} {e['kind']:8s} {s['frames']:3d}f {s['ms']:4d}ms {e.get('px', '?'):>4}px "
                  f"{'/'.join(e.get('hue', [])):14s} {e.get('shape', '')}")
        print(f"{len(hits)} match(es)")
        if a.cmd == "sheet" and hits:
            print(contact([r for r, _, _ in hits], a.out))
        return
    if a.cmd == "strip":
        rgb = tuple(float(x) for x in a.tint.split(",")) if a.tint else None
        swap = tuple(float(x) for x in a.swap.split(":")) if a.swap else None
        frs = place(frames(a.name), a.size, a.fit, a.dy, rgb, swap, a.nearest)
        b = write_strip(frs, a.out, a.size)
        print(f"{a.out}: {len(frs)} frames x {delay_ms(a.name)} ms, {a.size}px, {b} bytes")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
