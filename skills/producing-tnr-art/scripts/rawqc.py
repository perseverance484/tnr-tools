#!/usr/bin/env python3
"""rawqc.py - mechanical raw-generation QC before any human look (WO-11).

Three zero-human checks on a generated PNG, all pure stdlib (struct + zlib,
no PIL): the numbers come from 25x_DATA_art_spec.json and the target type is
inferred from the filename exactly like artpreflight (avatar_ / sprite /
scene_ / icon_ / pin_ / bg_).

  ASPECT    IHDR width/height vs the spec's target ratio - counters the
            square editor preview that has already caused one wrong re-export.
  COVERAGE  fraction of pixels on the chroma key (lime #00FF00 default,
            magenta #FF00FF autodetected) within tolerance; too little means
            the subject fills the frame (crop risk), too much means a near-
            empty generation.
  RING      purity of the 2px border ring: every ring pixel should be key.
            Non-key ring pixels mean the subject touches the edge or a matte
            fringe survived - both invisible on the white preview.

Ledger: every judged generation appends one line to data/art_ledger.jsonl
({scaffold, ts, verdict, reasons}) so scaffold editing becomes an evidence
loop; `--stats` prints per-scaffold accept rates and flags candidates for a
reference-image escalation (the escalation RULE itself is still an open art
ruling - this builds the evidence, not the policy).

Usage
  python3 rawqc.py IMAGE.png --scaffold fsw_faceless_stray
  python3 rawqc.py IMAGE.png --scaffold X --record      # append verdict
  python3 rawqc.py --stats                              # ledger summary
  python3 rawqc.py --selftest                           # synthesized red/green

Supports 8-bit RGB/RGBA PNGs (what the generators emit); anything else is
reported as MANUAL (not judged), never silently passed. Exit 1 on any REJECT.
"""
import json
import os
import struct
import sys
import time
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.abspath(os.path.join(HERE, ".."))
SPEC = os.path.join(SKILL, "data", "25x_DATA_art_spec.json")
LEDGER = os.path.join(SKILL, "data", "art_ledger.jsonl")

KEYS = {"lime": (0, 255, 0), "magenta": (255, 0, 255)}
TOL = 24            # per-channel tolerance for "on key"
COVER_BAND = (0.30, 0.92)   # sane background share for a keyed subject


# ------------------------------------------------------------- PNG decode

def read_png(path):
    b = open(path, "rb").read()
    if b[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    pos, ihdr, idat = 8, None, b""
    while pos < len(b):
        ln, typ = struct.unpack(">I4s", b[pos:pos + 8])
        data = b[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            ihdr = struct.unpack(">IIBBBBB", data)
        elif typ == b"IDAT":
            idat += data
        elif typ == b"IEND":
            break
        pos += 12 + ln
    w, h, depth, ctype, _, _, interlace = ihdr
    if depth != 8 or ctype not in (2, 6) or interlace:
        return w, h, None      # MANUAL path
    ch = 3 if ctype == 2 else 4
    raw = zlib.decompress(idat)
    stride = w * ch
    px = bytearray(h * stride)
    prev = bytearray(stride)

    def paeth(a, bb, c):
        p = a + bb - c
        pa, pb, pc = abs(p - a), abs(p - bb), abs(p - c)
        return a if pa <= pb and pa <= pc else (bb if pb <= pc else c)

    off = 0
    for y in range(h):
        f = raw[off]; off += 1
        line = bytearray(raw[off:off + stride]); off += stride
        for x in range(stride):
            a = line[x - ch] if x >= ch else 0
            up = prev[x]
            c = prev[x - ch] if x >= ch else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + up) & 255
            elif f == 3: line[x] = (line[x] + (a + up) // 2) & 255
            elif f == 4: line[x] = (line[x] + paeth(a, up, c)) & 255
        px[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, (bytes(px), ch)


def write_png(path, w, h, rgb_rows):
    """Selftest helper: minimal RGB writer."""
    raw = b"".join(b"\x00" + bytes(r) for r in rgb_rows)

    def chunk(t, d):
        c = t + d
        return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c))
    open(path, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b""))


# ------------------------------------------------------------- the checks

def infer_type(name):
    """Filename -> spec target key, same fragments artpreflight keys on."""
    n = os.path.basename(name).lower()
    for frag, t in (("avatar_", "AI_AVATAR"), ("sprite", "SCENE_CHARACTER"),
                    ("scene_", "SCENE_CHARACTER"), ("bg_", "SCENE_BACKGROUND"),
                    ("icon_", "ICON"), ("pin_", "ICON")):
        if frag in n:
            return t
    return None


def spec_aspect(atype):
    """-> (ratio, tolerance) from the spec's aspect entry, or None.
    Entries are {value: "W:H", tolerance: f}; rule-based entries (scene
    characters use a framing rule, not a fixed ratio) return None and the
    aspect stays a human judgement, stated in the notes."""
    try:
        t = json.load(open(SPEC))["targets"].get(atype) or {}
    except Exception:
        return None
    a = t.get("aspect") or {}
    v, tol = a.get("value"), a.get("tolerance", 0.02)
    if isinstance(v, str) and ":" in v and v.replace(":", "").replace(".", "").isdigit():
        x, y = v.split(":")
        return float(x) / float(y), float(tol)
    return None


def near(px, i, key):
    return (abs(px[i] - key[0]) <= TOL and abs(px[i + 1] - key[1]) <= TOL
            and abs(px[i + 2] - key[2]) <= TOL)


def judge(path):
    reasons, notes = [], []
    w, h, dec = read_png(path)
    atype = infer_type(path)
    sa = spec_aspect(atype) if atype else None
    if sa:
        want, tol = sa
        got = w / h
        if abs(got - want) / want > tol:
            reasons.append("wrong-aspect %dx%d (%.3f vs spec %.3f for %s)"
                           % (w, h, got, want, atype))
    elif atype:
        notes.append("no spec aspect for %s - aspect unjudged" % atype)
    else:
        notes.append("type not inferable from filename - aspect unjudged")
    if dec is None:
        notes.append("MANUAL: unsupported PNG flavor (need 8-bit RGB/RGBA); "
                     "pixel checks skipped, human QC required")
        return reasons, notes, {"w": w, "h": h}
    px, ch = dec
    counts = {k: 0 for k in KEYS}
    step = max(1, (w * h) // 20000)        # sample for speed on big images
    total = 0
    for p in range(0, w * h, step):
        i = p * ch
        total += 1
        for kn, kv in KEYS.items():
            if near(px, i, kv):
                counts[kn] += 1
                break
    keyname = max(counts, key=counts.get)
    key = KEYS[keyname]
    cover = counts[keyname] / max(1, total)
    if cover < COVER_BAND[0]:
        reasons.append("low-coverage %.0f%% %s key (subject overfills or key "
                       "missing)" % (cover * 100, keyname))
    elif cover > COVER_BAND[1]:
        reasons.append("empty-frame %.0f%% key (generation likely blank)"
                       % (cover * 100))
    ring_bad = ring_n = 0
    for y in range(h):
        for x in range(w):
            if 2 <= x < w - 2 and 2 <= y < h - 2:
                continue
            ring_n += 1
            if not near(px, (y * w + x) * ch, key):
                ring_bad += 1
    purity = 1 - ring_bad / max(1, ring_n)
    if purity < 0.98:
        reasons.append("dirty-ring %.1f%% border off-key (edge contact or "
                       "matte fringe)" % ((1 - purity) * 100))
    return reasons, notes, {"w": w, "h": h, "key": keyname,
                            "coverage": round(cover, 3),
                            "ring_purity": round(purity, 4)}


def record(scaffold, verdict, reasons):
    row = {"scaffold": scaffold, "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "verdict": verdict, "reasons": reasons}
    with open(LEDGER, "a") as f:
        f.write(json.dumps(row) + "\n")


def stats():
    if not os.path.exists(LEDGER):
        print("ledger empty (%s)" % os.path.relpath(LEDGER, SKILL))
        return 0
    agg = {}
    for ln in open(LEDGER):
        try:
            r = json.loads(ln)
        except Exception:
            continue
        a = agg.setdefault(r.get("scaffold", "?"), [0, 0, {}])
        a[0] += 1
        if r.get("verdict") == "accept":
            a[1] += 1
        for rs in r.get("reasons") or []:
            code = rs.split()[0]
            a[2][code] = a[2].get(code, 0) + 1
    print("scaffold                    n   accept  top reasons")
    for sc, (n, ok, rs) in sorted(agg.items()):
        top = ", ".join("%s x%d" % kv for kv in
                        sorted(rs.items(), key=lambda x: -x[1])[:2])
        flag = "  <- reference-escalation candidate" if n >= 3 and ok / n < 0.5 else ""
        print("%-26s %3d   %4.0f%%  %s%s" % (sc[:26], n, 100 * ok / n, top, flag))
    return 0


def selftest():
    import tempfile
    ok = True
    with tempfile.TemporaryDirectory() as td:
        K = KEYS["lime"]
        def img(name, w, h, subject=(8, 20), dirty_ring=False, no_key=False):
            rows = []
            for y in range(h):
                row = []
                for x in range(w):
                    inside = w // 3 <= x < 2 * w // 3 and h // 4 <= y < h - subject[0] // 4
                    on_ring = x < 2 or y < 2 or x >= w - 2 or y >= h - 2
                    if no_key:
                        row += [120, 60, 30]
                    elif dirty_ring and on_ring and (x + y) % 3 == 0:
                        row += [40, 40, 40]
                    elif inside:
                        row += [140, 70, 40]
                    else:
                        row += list(K)
                rows.append(row)
            p = os.path.join(td, name)
            write_png(p, w, h, rows)
            return p
        cases = [
            ("clean",  img("avatar_clean.png", 60, 60), 0),
            ("aspect", img("avatar_bad.png", 60, 40), 1),
            ("nokey",  img("avatar_nokey.png", 60, 60, no_key=True), 1),
            ("ring",   img("avatar_ring.png", 60, 60, dirty_ring=True), 1),
        ]
        for name, p, want in cases:
            reasons, _, m = judge(p)
            got = 1 if reasons else 0
            state = "PASS" if got == want else "FAIL"
            if got != want:
                ok = False
            print("%s  %-6s reject=%d want=%d  %s" %
                  (state, name, got, want, "; ".join(reasons)[:60]))
    print("selftest %s" % ("OK" if ok else "FAILED"))
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if not a or a[0] == "--help":
        print(__doc__)
        return 0
    if a[0] == "--selftest":
        return selftest()
    if a[0] == "--stats":
        return stats()
    path = a[0]
    scaffold = a[a.index("--scaffold") + 1] if "--scaffold" in a else "unlabeled"
    reasons, notes, metrics = judge(path)
    for n in notes:
        print("note    " + n)
    for r in reasons:
        print("REJECT  " + r)
    verdict = "reject" if reasons else "accept"
    print("%s  %s  %s" % (verdict.upper(), os.path.basename(path),
                          json.dumps(metrics)))
    if "--record" in a:
        record(scaffold, verdict, reasons)
        print("ledger + %s -> %s" % (scaffold, verdict))
    return 1 if reasons else 0


if __name__ == "__main__":
    sys.exit(main())
