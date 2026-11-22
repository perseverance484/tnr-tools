#!/usr/bin/env python3
"""Fetch every consumable's current icon and build comparison contact sheets.

Input: consumables.json (id, name, rarity, hidden, image) read live from item.getAll.
Output (next to this file): icons/<sha>.<ext> raw bytes, index.csv, index.md,
sheet_NN.png contact sheets (each under 4096 px tall). Runs in GitHub Actions,
because the cloud workspace's proxy refuses the image hosts.
"""
import csv, hashlib, io, json, pathlib, sys, urllib.request
from PIL import Image, ImageDraw, ImageFont

HERE = pathlib.Path(__file__).resolve().parent
ICONS = HERE / "icons"; ICONS.mkdir(exist_ok=True)
rows = json.loads((HERE / "consumables.json").read_text())
RANK = {"LEGENDARY": 0, "EPIC": 1, "RARE": 2, "COMMON": 3}
rows.sort(key=lambda r: (r["hidden"], RANK.get(r["rarity"], 9), r["name"].lower()))

cache = {}
def fetch(url):
    if url in cache: return cache[url]
    out = {"ok": False}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "tnr-tools-contact-sheet"})
        data = urllib.request.urlopen(req, timeout=30).read()
        h = hashlib.sha1(url.encode()).hexdigest()[:12]
        im = Image.open(io.BytesIO(data)); im.load()
        ext = (im.format or "bin").lower().replace("jpeg", "jpg")
        p = ICONS / f"{h}.{ext}"; p.write_bytes(data)
        alpha = im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info
        out = {"ok": True, "file": f"icons/{p.name}", "w": im.width, "h": im.height,
               "fmt": ext, "bytes": len(data), "alpha": alpha, "img": im.convert("RGBA")}
    except Exception as e:
        out["err"] = f"{type(e).__name__}: {e}"[:120]
    cache[url] = out
    return out

shared = {}
for r in rows: shared[r["image"]] = shared.get(r["image"], 0) + 1

with open(HERE / "index.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["n", "id", "name", "rarity", "hidden", "w", "h", "format", "bytes", "alpha", "shared_by", "image_url", "local_file", "error"])
    md = ["| # | Name | Rarity | Hidden | Size | Format | KB | Alpha | Shared | Image |", "|---|---|---|---|---|---|---|---|---|---|"]
    for n, r in enumerate(rows, 1):
        f = fetch(r["image"]); r["n"] = n; r["f"] = f
        w.writerow([n, r["id"], r["name"], r["rarity"], r["hidden"], f.get("w", ""), f.get("h", ""), f.get("fmt", ""),
                    f.get("bytes", ""), f.get("alpha", ""), shared[r["image"]], r["image"], f.get("file", ""), f.get("err", "")])
        md.append(f"| {n} | {r['name']} | {r['rarity']} | {'yes' if r['hidden'] else ''} | "
                  f"{f.get('w','?')}x{f.get('h','?')} | {f.get('fmt','FAIL')} | {round(f.get('bytes',0)/1024,1)} | "
                  f"{'yes' if f.get('alpha') else 'no'} | {shared[r['image']]} | [link]({r['image']}) |")
(HERE / "index.md").write_text("\n".join(md) + "\n")

# contact sheets: 8 columns, 160 px icon cell on mid-dark grey, label under it
COLS, CELL, ICON, LAB = 8, 176, 144, 46
ROWS_PER = (4000 - 60) // (CELL + LAB)
try: font = ImageFont.truetype("DejaVuSans.ttf", 12); bold = ImageFont.truetype("DejaVuSans-Bold.ttf", 13)
except Exception: font = bold = ImageFont.load_default()
RC = {"LEGENDARY": (240, 170, 40), "EPIC": (180, 110, 240), "RARE": (90, 160, 250), "COMMON": (190, 190, 190)}
per = COLS * ROWS_PER
for s in range(0, len(rows), per):
    chunk = rows[s:s + per]; nrows = -(-len(chunk) // COLS)
    sheet = Image.new("RGB", (COLS * CELL, 60 + nrows * (CELL + LAB)), (28, 28, 32))
    d = ImageDraw.Draw(sheet)
    d.text((10, 18), f"TNR consumable icons {s+1}-{s+len(chunk)} of {len(rows)}  (grey ground, native pixels scaled to {ICON}px)", fill=(230, 230, 230), font=bold)
    for i, r in enumerate(chunk):
        x, y = (i % COLS) * CELL, 60 + (i // COLS) * (CELL + LAB)
        d.rectangle([x + 6, y + 6, x + CELL - 6, y + CELL - 6], fill=(70, 70, 76), outline=RC.get(r["rarity"]), width=3)
        f = r["f"]
        if f["ok"]:
            im = f["img"].copy(); im.thumbnail((ICON, ICON), Image.LANCZOS)
            if im.width < ICON and im.height < ICON:
                sc = ICON / max(im.width, im.height); im = f["img"].resize((round(im.width * sc), round(im.height * sc)), Image.NEAREST)
            sheet.paste(im, (x + (CELL - im.width) // 2, y + (CELL - im.height) // 2), im)
        else:
            d.text((x + 20, y + CELL // 2), "FETCH FAILED", fill=(255, 90, 90), font=font)
        tag = f"#{r['n']}" + (" HIDDEN" if r["hidden"] else "") + (f" x{shared[r['image']]}" if shared[r["image"]] > 1 else "")
        d.text((x + 8, y + CELL - 2), tag, fill=RC.get(r["rarity"]), font=font)
        name = r["name"] if len(r["name"]) <= 24 else r["name"][:23] + "…"
        d.text((x + 8, y + CELL + 14), name, fill=(235, 235, 235), font=font)
        if f["ok"]: d.text((x + 8, y + CELL + 28), f"{f['w']}x{f['h']} {f['fmt']} {round(f['bytes']/1024)}KB", fill=(150, 150, 150), font=font)
    sheet.save(HERE / f"sheet_{s // per + 1:02d}.png", optimize=True)

ok = sum(1 for v in cache.values() if v["ok"])
print(f"{len(rows)} items, {len(cache)} distinct images, {ok} fetched, {len(cache) - ok} failed")
if ok == 0: sys.exit(1)
