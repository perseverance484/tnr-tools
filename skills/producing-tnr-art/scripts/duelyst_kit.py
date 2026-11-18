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
`frameDelay` per animation comes from app/data/resources.js (a sequence with no entry there falls back to 80 ms,
marked `"msFrom": "default"` in the catalogue). Pixel art: scale by whole steps with NEAREST
(--nearest, or --size a multiple of the source) to keep it crisp. How to use it: references/combat_fx.md, section
"Duelyst library (CC0)".
"""
import argparse
import bisect
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


def prefix_of(key):
    """Animation prefix of a frame key: `neutral_ion_attack_projectile_003.png` -> `neutral_ion_attack_projectile_`."""
    return re.sub(r"\d+\.png$", "", key)


def sequences_of(plist):
    out = {}
    for k in plist.get("frames", {}):
        pre = prefix_of(k)
        out[pre] = out.get(pre, 0) + 1
    return out


def actions_of(stem, seqs):
    """{prefix: action}. Several animations: the action is what follows their shared prefix (cut at an underscore),
    because upstream stems and frame prefixes differ (f2_hammonnladeseeker holds f2_hammonbladeseeker_attack_,
    neutral_dilotas_attack holds neutral_dilotas_idle_). One animation: what follows the stem, else `main`."""
    pres = sorted(seqs)
    if len(pres) == 1:
        pre = pres[0]
        return {pre: (pre[len(stem):].strip("_") if pre.startswith(stem) else "") or "main"}
    common = os.path.commonprefix(pres)
    common = common[:common.rfind("_") + 1]
    return {pre: pre[len(common):].strip("_") or "main" for pre in pres}


def frames(name, app=None):
    """Full-size RGBA frames of one sheet (or `sheet:prefix` animation), in order."""
    from PIL import Image
    sheet, prefix = split(name)
    _, path = locate(sheet, app)
    d = read_plist(path)
    seqs = sequences_of(d)
    if not prefix and len(seqs) > 1:
        raise SystemExit(f"{sheet} holds several animations, pick one as {sheet}:<prefix>: {sorted(seqs)}")
    if prefix and prefix not in seqs:
        raise SystemExit(f"{sheet} has no animation {prefix!r} (prefixes are exact): {sorted(seqs)}")
    atlas = Image.open(path[:-6] + ".png").convert("RGBA")
    out = []
    for k in sorted(d["frames"], key=natural):
        if prefix and prefix_of(k) != prefix:
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


ENTRY = re.compile(r"\{([^{}]*)\}", re.S)
PROP = re.compile(r"""\b(framePrefix|plist)\s*:\s*(['"])(.*?)\2""", re.S)
DELAY = re.compile(r"\bframeDelay\s*:\s*([0-9]*\.?[0-9]+)")


def parse_delays(text):
    """{(plist stem, framePrefix): ms} from resources.js text: each `{...}` entry is read whole, so property order,
    line breaks and quote style do not matter. Entries missing any of the three properties are ignored."""
    out = {}
    for body in ENTRY.findall(text):
        props = {k: v for k, _, v in PROP.findall(body)}
        m = DELAY.search(body)
        if m and "framePrefix" in props and props.get("plist", "").endswith(".plist"):
            stem = os.path.basename(props["plist"])[:-6]
            out[(stem, props["framePrefix"])] = int(round(float(m.group(1)) * 1000))
    return out


def delays(app=None):
    path = os.path.join(app or app_dir(), "data", "resources.js")
    if not os.path.exists(path):
        return {}
    return parse_delays(open(path, encoding="utf-8", errors="replace").read())


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


WEBP_MAX = 16383   # WebP's dimension limit
TEXTURE_MAX = 4096  # phones: a taller battle strip on a native host draws as a black box (combat_fx.md section 3)


def strip_height_problem(size_px, n, allow_tall=False):
    """None, or why a size_px x n-frame strip cannot ship, with the largest frame size that fits."""
    h = size_px * n
    limit = WEBP_MAX if allow_tall else TEXTURE_MAX
    if h <= limit:
        return None
    if allow_tall:
        why = "WebP cannot encode it"
    else:
        why = "phones cannot load a battle texture that tall" + (" and WebP cannot encode it" if h > WEBP_MAX else "")
    return (f"{n} frames x {size_px} px = {h} px tall: {why} (limit {limit}). Use --size {limit // n} or fewer "
            f"frames (keep {limit // size_px} at this size).")


def write_strip(frs, path, size_px, allow_tall=False):
    """One-column vertical strip, lossless WebP (the TNR ANIMATION format). Refuses a strip over 4096 px tall
    (allow_tall: only for Bunny-hosted art, which the game shrinks to 50 px wide) or over WebP's 16383."""
    from PIL import Image
    problem = strip_height_problem(size_px, len(frs), allow_tall)
    if problem:
        raise SystemExit(problem)
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
    entries, skipped = [], []

    def skip(stem, kind, why):
        skipped.append({"name": stem, "kind": kind, "why": why})
        print(f"skip {kind}/{stem}: {why}", file=sys.stderr)

    for kind, sub in KINDS.items():
        folder = os.path.join(app, sub.replace("app/", "", 1))
        for fn in sorted(os.listdir(folder)):
            if not fn.endswith(".plist"):
                continue
            stem = fn[:-6]
            if not os.path.exists(os.path.join(folder, stem + ".png")):
                skip(stem, kind, "no matching .png in the cache")
                continue
            try:
                d = read_plist(os.path.join(folder, fn))
            except Exception:  # noqa: BLE001 - a malformed sheet is skipped and reported
                skip(stem, kind, "unreadable plist")
                continue
            seqs = sequences_of(d)
            if not seqs:
                skip(stem, kind, "no frames")
                continue
            row = {"name": stem, "kind": kind, "seq": {}}
            acts = actions_of(stem, seqs)
            for pre, n in sorted(seqs.items()):
                ms = table.get((stem, pre))
                row["seq"][pre] = {"action": acts[pre], "frames": n, "ms": ms or 80,
                                   "msFrom": "resources.js" if ms else "default"}
            first = sorted(seqs)[0] if len(seqs) > 1 else ""
            pick = next((p for p in seqs if p.endswith("idle_")), first)
            try:
                row.update(stats(frames(stem + (":" + pick if len(seqs) > 1 else ""), app)))
            except SystemExit as e:
                print(f"skip stats {stem}: {e}", file=sys.stderr)
            entries.append(row)
    data = {"source": REPO, "pin": PIN, "license": "CC0 1.0 (OpenDuelyst)",
            "note": "Built by duelyst_kit.py catalog; do not hand-edit. Assets live in the cache, not the repo.",
            "entries": entries, "skipped": skipped}
    out = out or CATALOG
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w") as fh:
        json.dump(data, fh, separators=(",", ":"))
        fh.write("\n")
    by = {k: sum(1 for e in entries if e["kind"] == k) for k in KINDS}
    print(f"catalogue: {len(entries)} sheets {by}, {len(skipped)} skipped -> {out} ({os.path.getsize(out)} bytes)")
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


GAP = 6               # blank frames after each play in a contact sheet
PREVIEW_MAX_MS = 20000    # longest sheet, in preview time
GIF_MIN_MS = 20           # GIF delays are whole centiseconds; browsers clamp anything under 20 ms


def contact_plan(clips_ms_frames):
    """Schedule a contact sheet on source-frame boundaries, so no frame is skipped.

    Every clip plays once with its gap. A clip faster than GIF_MIN_MS per frame cannot be shown at true speed, so the
    whole sheet is slowed by one factor until the fastest frame lasts GIF_MIN_MS. Shots start at every clip's frame
    boundary (rounded to 10 ms; a frame of 20 ms or more always keeps a slot of its own). Returns
    (shots, notes): shots = [(duration ms, [frame index per clip, or None in the gap])], notes = adjustments made."""
    notes = []
    fastest = min(ms for ms, _ in clips_ms_frames)
    slow = GIF_MIN_MS / fastest if fastest < GIF_MIN_MS else 1.0
    if slow > 1:
        notes.append(f"slowed x{slow:g}: the fastest clip runs {fastest} ms/frame, under the {GIF_MIN_MS} ms a GIF "
                     f"can show")
    scaled = [ms * slow for ms, _ in clips_ms_frames]
    total = max((n + GAP) * m for (_, n), m in zip(clips_ms_frames, scaled))
    if total > PREVIEW_MAX_MS:
        notes.append(f"cut at {PREVIEW_MAX_MS} ms of {round(total)}: later frames of the longest clips are not shown")
        total = PREVIEW_MAX_MS
    total = int(round(total / 10) * 10)
    r10 = lambda t: int(round(t / 10) * 10)
    starts = []  # per clip: rounded start time of each frame slot (frames then gap, repeating)
    for (_, n), m in zip(clips_ms_frames, scaled):
        st, k = [], 0
        while r10(k * m) < total:
            st.append(r10(k * m))
            k += 1
        starts.append(st)
    cuts = sorted({0, total} | {t for st in starts for t in st})
    shots = []
    for t0, t1 in zip(cuts, cuts[1:]):
        idx = []
        for (_, n), st in zip(clips_ms_frames, starts):
            k = (bisect.bisect_right(st, t0) - 1) % (n + GAP)
            idx.append(k if k < n else None)
        if shots and shots[-1][1] == idx:
            shots[-1] = (shots[-1][0] + t1 - t0, idx)
        else:
            shots.append((t1 - t0, idx))
    return shots, notes


def contact(refs, out, app=None, cell=150, cols=5):
    """Animated contact sheet: every match plays through once on its own clock, then a short gap. Prints any timing
    adjustment (contact_plan)."""
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
    plan, notes = contact_plan([(ms, len(frs)) for _, frs, ms in clips])
    for n in notes:
        print(f"contact sheet: {n}", file=sys.stderr)
    shots, durs = [], []
    for dur, idx in plan:
        im = Image.new("RGB", (W, H), (34, 36, 32))
        d = ImageDraw.Draw(im)
        for i, ((label, frs, _), k) in enumerate(zip(clips, idx)):
            x, y = (i % cols) * cell, (i // cols) * (cell + 14)
            if k is not None:
                im.paste(frs[k], (x, y + 14), frs[k])
            d.text((x + 3, y + 1), label, fill=(220, 220, 220))
        shots.append(im)
        durs.append(dur)
    shots[0].save(out, save_all=True, append_images=shots[1:], duration=durs, loop=0, optimize=False)
    return out


def plan_shows_every_frame(plan, n_frames):
    """For each clip, whether every source frame index appears in some shot (selftest helper)."""
    seen = [set() for _ in n_frames]
    for _, idx in plan:
        for c, k in enumerate(idx):
            if k is not None:
                seen[c].add(k)
    return [s == set(range(n)) for s, n in zip(seen, n_frames)]


# ------------------------------------------------------------------------------------------------ selftest
def selftest():
    """No network. Synthetic sheets through frames/sequences/place/strip, catalog on a temp app tree, find, hue_swap,
    delays and the contact-sheet schedule. Fixtures are asymmetric so a reversed rotation or a wrong order fails."""
    import tempfile
    from PIL import Image
    tmp = tempfile.mkdtemp()
    app = os.path.join(tmp, "app")
    for sub in KINDS.values():
        os.makedirs(os.path.join(tmp, sub), exist_ok=True)
    os.makedirs(os.path.join(app, "data"), exist_ok=True)
    units = os.path.join(app, "resources", "units")
    RED, BLUE, GOLD = (255, 0, 0, 255), (0, 120, 255, 255), (255, 200, 0, 255)

    # Sheet "a": idle (plain) and hit (stored rotated). The hit source is 10x20, blue with a red top-left pixel;
    # the atlas holds it turned 90 degrees clockwise, as cocos2d stores `rotated` frames.
    src = Image.new("RGBA", (10, 20), BLUE)
    src.putpixel((0, 0), RED)
    atlas = Image.new("RGBA", (40, 20), (0, 0, 0, 0))
    atlas.paste(GOLD, (0, 0, 10, 20))
    atlas.paste(src.rotate(-90, expand=True), (10, 0))       # 20x10 at (10,0)
    atlas.save(os.path.join(units, "a.png"))
    plistlib.dump({"frames": {
        "a_idle_0.png": {"frame": "{{0,0},{10,20}}", "rotated": False, "sourceSize": "{30,30}",
                         "sourceColorRect": "{{10,5},{10,20}}"},
        "a_hit_0.png": {"frame": "{{10,0},{10,20}}", "rotated": True, "sourceSize": "{30,30}",
                        "sourceColorRect": "{{10,5},{10,20}}"},
    }, "metadata": {"format": 2}}, open(os.path.join(units, "a.plist"), "wb"))

    # Sheet "u_stem" (stem differs from its prefixes, like f2_hammonnladeseeker): u_attack_ has frames 2 and 10
    # (natural order 2 < 10; red then gold), u_attack_projectile_ overlaps its prefix, u_idle_ is one frame.
    atlas = Image.new("RGBA", (40, 10), (0, 0, 0, 0))
    for i, c in enumerate((RED, GOLD, BLUE, BLUE)):
        atlas.paste(c, (i * 10, 0, i * 10 + 10, 10))
    atlas.save(os.path.join(units, "u_stem.png"))
    fr = lambda i: {"frame": "{{%d,0},{10,10}}" % (i * 10), "rotated": False, "sourceSize": "{10,10}",
                    "sourceColorRect": "{{0,0},{10,10}}"}
    plistlib.dump({"frames": {"u_attack_10.png": fr(1), "u_attack_2.png": fr(0), "u_attack_projectile_0.png": fr(2),
                              "u_idle_0.png": fr(3)}, "metadata": {"format": 2}},
                  open(os.path.join(units, "u_stem.plist"), "wb"))
    # A plist with no atlas: skipped and reported.
    plistlib.dump({"frames": {}}, open(os.path.join(units, "orphan.plist"), "wb"))

    # resources.js: plist first and single quotes, a multiline double-quoted entry, and one entry lacking a delay.
    open(os.path.join(app, "data", "resources.js"), "w").write(
        "  aIdle: {\n    name: 'aIdle', img: 'resources/units/a.png', plist: 'resources/units/a.plist', "
        "framePrefix: 'a_idle_', frameDelay: 0.12,\n  },\n"
        '  uAttack: {\n    framePrefix: "u_attack_",\n    plist: "resources/units/u_stem.plist",\n'
        "    frameDelay: 1,\n  },\n"
        "  uIdle: { framePrefix: 'u_idle_', plist: 'resources/units/u_stem.plist' },\n")
    table = delays(app)
    assert table == {("a", "a_idle_"): 120, ("u_stem", "u_attack_"): 1000}, table

    assert sequences_of(read_plist(os.path.join(units, "a.plist"))) == {"a_idle_": 1, "a_hit_": 1}
    for bad in ("a", "u_stem:u_att", "u_stem:u_"):
        try:
            frames(bad, app)
            raise AssertionError(f"{bad} must refuse (no prefix on a multi-animation sheet, or a partial prefix)")
        except SystemExit:
            pass
    idle = frames("a:a_idle_", app)
    hit = frames("a:a_hit_", app)
    assert idle[0].size == (30, 30) and idle[0].getpixel((12, 10)) == GOLD
    assert hit[0].getbbox() == (10, 5, 20, 25), hit[0].getbbox()
    assert hit[0].getpixel((10, 5)) == RED and hit[0].getpixel((19, 24)) == BLUE, "rotated frame reversed"
    atk = frames("u_stem:u_attack_", app)
    assert len(atk) == 2 and atk[0].getpixel((5, 5)) == RED and atk[1].getpixel((5, 5)) == GOLD, "order or prefix"
    assert len(frames("u_stem:u_attack_projectile_", app)) == 1
    assert delay_ms("a:a_idle_", table) == 120 and delay_ms("a:a_hit_", table) == 80
    assert actions_of("u_stem", {"u_attack_": 2, "u_attack_projectile_": 1, "u_idle_": 1}) == {
        "u_attack_": "attack", "u_attack_projectile_": "attack_projectile", "u_idle_": "idle"}
    assert actions_of("fx_x", {"fx_x_": 4}) == {"fx_x_": "main"}

    placed = place(idle, 90, nearest=True)
    assert placed[0].size == (90, 90) and placed[0].getpixel((45, 40)) == GOLD
    sw = hue_swap(idle[0], 0, 100, 352)
    h = colorsys.rgb_to_hls(*(c / 255 for c in sw.getpixel((12, 10))[:3]))[0] * 360
    assert abs(h - 352) < 2, h
    p = os.path.join(tmp, "s.webp")
    write_strip(placed, p, 90)
    assert Image.open(p).size == (90, 90)
    assert strip_height_problem(144, 28) is None and "--size 66" in strip_height_problem(288, 62)
    assert "WebP" in strip_height_problem(288, 62, allow_tall=True)
    try:
        write_strip(placed * 50, p, 90)
        raise AssertionError("a 4500 px strip must refuse")
    except SystemExit:
        pass

    plan, notes = contact_plan([(80, 62), (80, 10)])
    assert sum(d for d, _ in plan) == (62 + GAP) * 80 and not notes
    assert plan_shows_every_frame(plan, [62, 10]) == [True, True]
    plan, notes = contact_plan([(10, 54), (80, 12), (33, 7)])   # fx_fluid_puff runs 54 frames at 10 ms
    assert plan_shows_every_frame(plan, [54, 12, 7]) == [True, True, True], "frames dropped"
    assert all(d >= 10 and d % 10 == 0 for d, _ in plan) and "slowed x2" in notes[0], notes
    plan, notes = contact_plan([(1000, 30)])
    assert sum(d for d, _ in plan) == PREVIEW_MAX_MS and "cut at" in notes[0]

    cat = catalog(os.path.join(tmp, "cat.json"), app)
    by = {e["name"]: e for e in cat["entries"]}
    assert set(by) == {"a", "u_stem"} and cat["skipped"] == [
        {"name": "orphan", "kind": "unit", "why": "no matching .png in the cache"}], cat["skipped"]
    assert by["a"]["seq"]["a_idle_"] == {"action": "idle", "frames": 1, "ms": 120, "msFrom": "resources.js"}
    assert by["a"]["seq"]["a_hit_"]["msFrom"] == "default"
    assert by["u_stem"]["seq"]["u_attack_"]["ms"] == 1000
    assert [r for r, _, _ in find(cat, kind="unit", action="attack")] == ["u_stem:u_attack_"]
    assert [r for r, _, _ in find(cat, kind="unit", action="hit")] == ["a:a_hit_"]
    here = os.getcwd()
    try:
        os.chdir(tmp)
        catalog("bare.json", app)  # basename-only --out
        assert os.path.exists(os.path.join(tmp, "bare.json"))
    finally:
        os.chdir(here)
    real = app_dir()
    if os.path.exists(os.path.join(real, "resources", "fx", "fx_fluid_puff.plist")):
        n = len(frames("fx_fluid_puff", real))
        ms = delay_ms("fx_fluid_puff", delays(real))
        assert (n, ms) == (54, 10), (n, ms)
        plan, _ = contact_plan([(ms, n)])
        assert plan_shows_every_frame(plan, [n]) == [True], "real fx_fluid_puff: frames dropped"
        print("duelyst_kit selftest: real-source fx_fluid_puff 54 x 10 ms, every frame scheduled")
    else:
        print("duelyst_kit selftest: no cache, real-source cases skipped")
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
    s.add_argument("--allow-tall", action="store_true",
                   help="allow strips over 4096 px tall (Bunny-hosted art only; never for a native host)")
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
        src = frames(a.name)
        problem = strip_height_problem(a.size, len(src), a.allow_tall)
        if problem:
            raise SystemExit(problem)
        frs = place(src, a.size, a.fit, a.dy, rgb, swap, a.nearest)
        b = write_strip(frs, a.out, a.size, a.allow_tall)
        print(f"{a.out}: {len(frs)} frames x {delay_ms(a.name)} ms, {a.size}px, {b} bytes")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
