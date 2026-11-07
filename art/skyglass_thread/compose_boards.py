#!/usr/bin/env python3
"""Compose the salvager's-thread boards: scene backgrounds for Wreck Sighted and At the Salvager's Fire.

    python3 art/skyglass_thread/compose_boards.py            -> art/skyglass_thread/exports/board-*.webp (+ preview.png)

Each board is the shore scene (art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp) with a driftwood board and
pinned paper cards. Cards carry EXISTING item icons and one or two words in Silkscreen (OFL, font/OFL.txt), so nothing
here is generated art and the icons match what players see in their inventory.

Frame rules (docs/ENGINE_LAWS.md 48-51, 79; layout/Logbook.tsx QuestDialogScene): the scene is 3:2, delivered at 512 px
wide; the salvager covers the left 40% and the dialog box the bottom third. Every card sits in the clear zone
x 41-97%, y 3-64%. Boards are authored at the delivered size (512x341) so the pixel font stays crisp.
Design: docs/design/SKYGLASS_TEXT.md section 1b; RUL-2026-11-07-136. Pillow only.
"""
import os
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
OUT = os.path.join(HERE, "exports")
W, H = 512, 341
ZONE = (int(W * 0.41), int(H * 0.03), int(W * 0.97), int(H * 0.64))  # x0, y0, x1, y1
PAPER, INK, TACK, SHADOW = (227, 214, 184), (42, 32, 24), (127, 211, 232), (20, 14, 9)
GLOW = (127, 211, 232)

ICON = {
    "tide": "skyglass_event_icons/exports/icon-tide-chart.webp",
    "roster": "skyglass_event_icons/exports/icon-watch-roster.webp",
    "cache": "skyglass_event_icons/exports/icon-chart-buried-cache.webp",
    "foundry": "skyglass_event_icons/exports/icon-chart-drowned-foundry.webp",
    "archive": "skyglass_event_icons/exports/icon-chart-quarantined-archive.webp",
    "watch": "skyglass_event_icons/exports/icon-chart-captains-watch.webp",
    "seal": "skyglass_event_icons/exports/icon-reliquary-seal.webp",
    "rseal": "skyglass_event_icons/exports/icon-rotted-reliquary-seal.webp",
    "heading": "skyglass_event_icons/exports/icon-the-last-heading.webp",
    "rheading": "skyglass_event_icons/exports/icon-the-rotted-heading.webp",
    "rot": "skyglass_event_icons/exports/icon-core-rot.webp",
    "ledger": "skyglass_event_icons/exports/icon-ledger-page.webp",
    "manifest": "skyglass_event_icons/exports/icon-stores-manifest.webp",
    "token": "skyglass_event_icons/exports/icon-skyglass-token.webp",
    "coffer": "skyglass_event_icons/exports/icon-skyglass-coffer.webp",
    "treasury": "skyglass_event_icons/exports/icon-sealed-treasury.webp",
    "stores": "skyglass_event_icons/exports/icon-galley-stores.webp",
    "hoard": "skyglass_event_icons/exports/icon-crowns-hoard.webp",
    "chest": "skyglass_event_icons/exports/icon-rare-hunters-chest.webp",
    "katana": "ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp",
    "keel": "mother_of_echoes/exports/icon-shard-keel.webp",
    "crown": "mother_of_echoes/exports/icon-shard-crown.webp",
    "tideshard": "mother_of_echoes/exports/icon-shard-tide.webp",
    "ledgershard": "mother_of_echoes/exports/icon-shard-ledger.webp",
    "log": "skyglass_journal/exports/icon-quest-watch-log.webp",
}
PICTURE = {  # scene art used as small framed pictures
    "wreck": "ghost_ship_skyglass/structure/structure_skyglass_wreck_beached_v1.png",
    "gate": "crownhold/scenes/exports/scene_bg_crownhold_gate.webp",
    "throne": "crownhold/scenes/exports/scene_bg_crownhold_throne_room.webp",
}
BASE = "ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp"


def font(size, bold=False):
    return ImageFont.truetype(os.path.join(HERE, "font", f"Silkscreen-{'700' if bold else '400'}.ttf"), size)


def load(rel, size=None, crop_box=None):
    im = Image.open(os.path.join(ART, rel)).convert("RGBA")
    if crop_box:
        im = im.crop(crop_box)
    if size:
        im = im.resize(size, Image.LANCZOS)
    return im


def base():
    """The shore, darkened, with a driftwood board filling the clear zone."""
    im = load(BASE, (W, H)).convert("RGB")
    im = ImageEnhance.Brightness(im).enhance(0.62)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = ZONE[0] - 8, ZONE[1] - 6, ZONE[2] + 8, ZONE[3] + 8
    rnd = random.Random(7)
    plank_h = (y1 - y0) // 4
    for i in range(4):
        top = y0 + i * plank_h
        bot = y1 if i == 3 else top + plank_h
        tone = (60 + i % 2 * 6, 44 + i % 2 * 4, 30 + i % 2 * 3)
        d.rectangle([x0 + rnd.randint(0, 3), top, x1 - rnd.randint(0, 3), bot - 1], fill=tone)
        for _ in range(40):  # grain
            gx = rnd.randint(x0 + 4, x1 - 24)
            gy = rnd.randint(top + 2, bot - 3)
            d.line([gx, gy, gx + rnd.randint(8, 24), gy], fill=(tone[0] - 10, tone[1] - 8, tone[2] - 6))
        d.line([x0, bot - 1, x1, bot - 1], fill=(30, 21, 14))
    d.rectangle([x0, y0, x1, y1], outline=(28, 20, 13), width=2)
    for px in (x0 + 6, x1 - 8):  # posts' nails
        for py in (y0 + 6, y1 - 8):
            d.rectangle([px, py, px + 1, py + 1], fill=(150, 160, 170))
    return im


def card(im, x, y, w, h, icon=None, label=None, sub=None, picture=None, tilt=0, dim=False):
    layer = Image.new("RGBA", (w + 4, h + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rectangle([2, 3, w + 1, h + 2], fill=SHADOW + (200,))
    d.rectangle([0, 0, w - 1, h - 1], fill=PAPER + (255,), outline=(120, 100, 74, 255))
    text_h = (9 if label else 0) + (8 if sub else 0)
    if picture:
        pic = load(PICTURE[picture]).convert("RGBA")
        pw, ph = w - 6, h - 6 - text_h
        pic = pic.resize((pw, ph), Image.LANCZOS) if picture != "wreck" else _fit(pic, pw, ph)
        if dim:
            pic = ImageEnhance.Brightness(pic).enhance(0.55)
        layer.alpha_composite(pic, (3, 3))
    if icon:
        size = min(w - 8, h - 6 - text_h)
        ic = load(ICON[icon], (size, size))
        if dim:
            ic = ImageEnhance.Brightness(ic).enhance(0.55)
        layer.alpha_composite(ic, ((w - size) // 2, 3 + max(0, (h - 6 - text_h - size) // 2)))
    ty = h - text_h - 2
    if label:
        _center(d, w, ty, label, font(8, True))
        ty += 9
    if sub:
        _center(d, w, ty, sub, font(8))
    d.rectangle([w // 2 - 2, 0, w // 2 + 1, 2], fill=TACK + (255,))
    if tilt:
        layer = layer.rotate(tilt, resample=Image.BICUBIC, expand=True)
    im.paste(layer, (x, y), layer)


def _fit(pic, w, h):
    pic.thumbnail((w, h), Image.LANCZOS)
    canvas = Image.new("RGBA", (w, h), (30, 40, 55, 255))
    canvas.alpha_composite(pic, ((w - pic.width) // 2, (h - pic.height) // 2))
    return canvas


def _center(d, w, y, text, f):
    tw = d.textlength(text, font=f)
    d.text(((w - tw) // 2, y), text, font=f, fill=INK + (255,))


def label(im, x, y, text, size=8, color=PAPER, bold=True, anchor="la"):
    ImageDraw.Draw(im).text((x, y), text, font=font(size, bold), fill=color, anchor=anchor)


def arrow(im, x0, y0, x1, y1):
    d = ImageDraw.Draw(im)
    d.line([x0, y0, x1, y1], fill=GLOW, width=2)
    if abs(x1 - x0) >= abs(y1 - y0):
        s = 1 if x1 > x0 else -1
        d.polygon([(x1 + 4 * s, y1), (x1 - 2 * s, y1 - 4), (x1 - 2 * s, y1 + 4)], fill=GLOW)
    else:
        s = 1 if y1 > y0 else -1
        d.polygon([(x1, y1 + 4 * s), (x1 - 4, y1 - 2 * s), (x1 + 4, y1 - 2 * s)], fill=GLOW)


def figure(im, cx, top, scale=1):
    d = ImageDraw.Draw(im)
    r = 5 * scale
    d.ellipse([cx - r, top, cx + r, top + 2 * r], fill=INK)
    d.rounded_rectangle([cx - 8 * scale, top + 2 * r + 2, cx + 8 * scale, top + 2 * r + 24 * scale], radius=4, fill=INK)


# --- the boards -----------------------------------------------------------------------------------------------------
X0, Y0, X1, Y1 = ZONE
ZW, ZH = X1 - X0, Y1 - Y0


def b_menu(im):
    cols, rows, gap = 4, 2, 6
    cw, ch = (ZW - gap * (cols - 1)) // cols, (ZH - gap * (rows - 1)) // rows
    items = [("ABOARD", None, "wreck"), ("CHARTS", "tide", None), ("THE DEEP", "seal", None), ("THE HAUL", "ledger", None),
             ("SHARDS", "crown", None), ("TRADE", "token", None), ("THE LOG", "log", None)]
    for i, (name, ic, pic) in enumerate(items):
        r, c = divmod(i, cols)
        card(im, X0 + c * (cw + gap), Y0 + r * (ch + gap), cw, ch, icon=ic, picture=pic, label=name)


def b_threes(im):
    card(im, X0 + 20, Y0 + 6, ZW - 40, ZH - 16)
    cx = X0 + ZW // 2
    for dx in (-38, 0, 38):
        figure(im, cx + dx, Y0 + 22, scale=2)
    label(im, cx, Y0 + 104, "GO IN THREES", 16, color=INK, anchor="mm")
    label(im, cx, Y0 + 124, "SECTOR 210", 8, color=INK, bold=False, anchor="mm")


def b_hulls(im):
    cw = (ZW - 10) // 2
    card(im, X0, Y0 + 4, cw, ZH - 10, picture="wreck", dim=True, label="FADED", sub="LV 40-60  16/6")
    card(im, X0 + cw + 10, Y0 + 4, cw, ZH - 10, picture="wreck", label="SKYGLASS", sub="LV 100  15/6")


def b_loot(im):
    card(im, X0, Y0 + 4, 80, 44, label="RYO", sub="+ EXP")
    icons = ["tide", "roster", "cache", "stores"]
    cw = (ZW - 8 * 3) // 4
    for i, ic in enumerate(icons):
        card(im, X0 + i * (cw + 8), Y0 + 62, cw, cw + 6, icon=ic)
    label(im, X0 + 90, Y0 + 18, "EVERY CLEAR", 8)
    label(im, X0, Y0 + ZH - 12, "CHARTS CAN DROP", 8)


def b_once(im):
    card(im, X0 + 2, Y0 + 20, 74, 86, icon="tide", label="CHART")
    arrow(im, X0 + 84, Y0 + 62, X0 + 108, Y0 + 62)
    card(im, X0 + 118, Y0 + 20, 92, 86, label="BATTLE", sub="ARENA")
    figure(im, X0 + 164, Y0 + 36, scale=1)
    label(im, X0 + 220, Y0 + 52, "SOLO", 8)
    label(im, X0 + 2, Y0 + ZH - 26, "SPENT AT THE START", 8)
    label(im, X0 + 2, Y0 + ZH - 14, "A LOSS ENDS THE RUN", 8)


def _rung(im, y, name, icons, size=34):
    label(im, X0 + 60, y + size // 2, name, 8, anchor="rm")
    for i, ic in enumerate(icons):
        card(im, X0 + 66 + i * (size + 8), y, size + 4, size + 4, icon=ic)


def b_ladder(im):
    _rung(im, Y0 + 2, "LOW TIDE", ["tide", "roster"])
    arrow(im, X0 + 150, Y0 + 42, X0 + 150, Y0 + 52)
    _rung(im, Y0 + 56, "THE CREW", ["cache", "foundry", "archive", "watch"])
    arrow(im, X0 + 150, Y0 + 96, X0 + 150, Y0 + 106)
    _rung(im, Y0 + 110, "THE DEEP", ["seal", "heading"])


def b_pick(im):
    label(im, X0 + ZW // 2, Y0 + 10, "WIN: PICK ONE", 16, anchor="mm")
    cw = (ZW - 20) // 3
    for i, ic in enumerate(["coffer", "token", "stores"]):
        card(im, X0 + i * (cw + 10), Y0 + 24, cw, cw + 4, icon=ic)
    label(im, X0 + ZW // 2, Y0 + ZH - 10, "DIFFICULTY: * * * * *", 8, anchor="mm")


def b_seals(im):
    cw = (ZW - 12) // 2
    card(im, X0, Y0 + 4, cw, ZH - 10, icon="seal", label="RELIQUARY")
    card(im, X0 + cw + 12, Y0 + 4, cw, ZH - 10, icon="heading", label="THE FALL")


def b_rot(im):
    card(im, X0, Y0 + 30, 62, 70, icon="seal", label="EPIC")
    label(im, X0 + 70, Y0 + 64, "+", 12, anchor="lm")
    for i in range(3):
        card(im, X0 + 84 + i * 30, Y0 + 44, 28, 34, icon="rot")
    arrow(im, X0 + 178, Y0 + 64, X0 + 200, Y0 + 64)
    card(im, X0 + 210, Y0 + 30, 62, 70, icon="rseal", label="TAINTED")
    label(im, X0 + ZW // 2, Y0 + ZH - 16, "WIN A FIGHT TO STEEP IT", 8, anchor="mm")
    label(im, X0 + ZW // 2, Y0 + ZH - 4, "TAINTED RUNS: PICK TWO", 8, anchor="mm")


def b_lantern(im):
    card(im, X0, Y0 + 26, 84, 84, label="LASTLIGHT", sub="LANTERN")
    d = ImageDraw.Draw(im)
    cx, cy = X0 + 42, Y0 + 52
    d.rectangle([cx - 8, cy - 10, cx + 8, cy + 12], outline=INK, width=2)
    d.rectangle([cx - 4, cy - 6, cx + 4, cy + 8], fill=(240, 220, 150))
    d.line([cx - 5, cy - 14, cx + 5, cy - 14], fill=INK, width=2)
    arrow(im, X0 + 94, Y0 + 68, X0 + 122, Y0 + 68)
    card(im, X0 + 132, Y0 + 4, ZW - 132, ZH - 10, picture="gate", label="CROWNHOLD")


def b_haul(im):
    card(im, X0, Y0 + 20, 70, 84, icon="ledger", label="PAGE")
    steps = ["CRATE", "LOCKER", "CUT", "LEAVE"]
    for i, s in enumerate(steps):
        label(im, X0 + 86, Y0 + 26 + i * 18, f"> {s}", 8)
    card(im, X0 + 170, Y0 + 20, 72, 84, icon="chest", label="UP TO 5")
    label(im, X0 + ZW // 2, Y0 + ZH - 8, "DEEPER = BIGGER CHESTS", 8, anchor="mm")


def b_shards4(im):
    names = [("keel", "KEEL"), ("crown", "CROWN"), ("tideshard", "TIDE"), ("ledgershard", "LEDGER")]
    cw = (ZW - 18) // 4
    for i, (ic, n) in enumerate(names):
        card(im, X0 + i * (cw + 6), Y0 + 20, cw, cw + 16, icon=ic, label=n)
    label(im, X0 + ZW // 2, Y0 + ZH - 14, "SAME GLASS", 16, anchor="mm")


def b_below(im):
    card(im, X0 + 70, Y0 + 4, ZW - 140, ZH - 10, picture="throne", dim=True)
    d = ImageDraw.Draw(im)
    cx, cy = X0 + ZW // 2, Y0 + ZH // 2 - 6
    d.ellipse([cx - 16, cy - 20, cx + 16, cy + 20], fill=(10, 8, 14), outline=GLOW, width=2)
    label(im, cx, cy, "?", 12, color=GLOW, anchor="mm")
    for i, ic in enumerate(["keel", "crown", "tideshard", "ledgershard"]):
        x = X0 + 2 if i < 2 else X1 - 58
        card(im, x, Y0 + 14 + (i % 2) * 64, 56, 56, icon=ic)
    label(im, cx, Y0 + ZH - 4, "ALONE. ALL FOUR SPENT", 8, anchor="mm")


def b_trade(im):
    cw = (ZW - 24) // 4
    for i, ic in enumerate(["tide", "rot", "crown", "token"]):
        card(im, X0 + i * (cw + 8), Y0 + 22, cw, cw + 2, icon=ic)
    label(im, X0 + ZW // 2, Y0 + 10, "EVERY CHART HAS A BUYER", 8, anchor="mm")
    label(im, X0 + ZW // 2, Y0 + ZH - 8, "HOARD: NOT FOR TRADE", 8, anchor="mm")


def b_token(im):
    card(im, X0 + 6, Y0 + 20, 84, 96, icon="token", label="TOKEN")
    arrow(im, X0 + 100, Y0 + 66, X0 + 126, Y0 + 66)
    card(im, X0 + 136, Y0 + 20, 84, 96, icon="katana", label="12 SKINS")
    label(im, X0 + ZW // 2, Y0 + ZH - 8, "ON A WEAPON YOU OWN", 8, anchor="mm")


def b_logboard(im):
    card(im, X0 + ZW // 2 - 50, Y0 + 6, 100, 104, icon="log", label="THIS WEEKEND")
    label(im, X0 + ZW // 2, Y0 + ZH - 24, "INFORMATION BOARD", 16, anchor="mm")
    label(im, X0 + ZW // 2, Y0 + ZH - 7, "TAKE IT FIRST", 8, anchor="mm")


def b_orders(im):
    card(im, X0, Y0 + 8, 92, 104, icon="log")
    for i in range(4):
        label(im, X0 + 102, Y0 + 18 + i * 16, f"[ ] ORDER {i + 1}", 8)
    card(im, X0 + 214, Y0 + 30, 58, 70, icon="token", label="ALL")
    label(im, X0 + ZW // 2, Y0 + ZH - 8, "CLOSES TUE 00:00 UTC", 8, anchor="mm")


BOARDS = {
    "menu": b_menu, "threes": b_threes, "hulls": b_hulls, "loot": b_loot, "once": b_once, "ladder": b_ladder,
    "pick": b_pick, "seals": b_seals, "rot": b_rot, "lantern": b_lantern, "haul": b_haul, "shards": b_shards4,
    "below": b_below, "trade": b_trade, "token": b_token, "logboard": b_logboard, "orders": b_orders,
}


def main():
    os.makedirs(OUT, exist_ok=True)
    sheet = Image.new("RGB", (W * 3 + 16, (H + 8) * ((len(BOARDS) + 2) // 3) + 8), (11, 15, 20))
    for i, (name, fn) in enumerate(BOARDS.items()):
        im = base()
        fn(im)
        path = os.path.join(OUT, f"board-{name}.webp")
        im.save(path, "WEBP", quality=90, method=6)
        r, c = divmod(i, 3)
        sheet.paste(im, (8 + c * (W + 4), 8 + r * (H + 8)))
        print(f"{os.path.relpath(path, os.path.dirname(ART))}: {os.path.getsize(path)} bytes")
    sheet.save(os.path.join(HERE, "preview.png"))


if __name__ == "__main__":
    main()
